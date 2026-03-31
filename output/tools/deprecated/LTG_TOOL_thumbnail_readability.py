#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_thumbnail_readability.py — v1.0.0 (Cycle 50, Morgan Walsh)

Thumbnail Readability Test for Character Assets.

Renders character images at multiple scales (128px, 64px, 32px height) and
evaluates whether the character remains identifiable at each scale using
automated metrics:

  1. Silhouette Preservation: Does the character's silhouette survive downscaling?
     Measured by IoU of foreground mask at full-res vs downscaled-then-upscaled.
  2. Feature Retention: How much structural detail survives?
     Measured by edge pixel preservation ratio (Canny edges at each scale).
  3. Color Identity: Does the character's dominant color survive?
     Measured by top-3 hue bucket stability across scales.
  4. Expression Readability: At each scale, is there enough detail in the
     head region to convey expression? Measured by edge density in head bbox.

Output:
  - Multi-scale contact sheet PNG showing character at each test scale
  - JSON/text metrics per scale
  - PASS/WARN/FAIL per scale

Thresholds:
  128px: PASS >= 0.70 silhouette IoU, WARN >= 0.50, FAIL < 0.50
   64px: PASS >= 0.55 silhouette IoU, WARN >= 0.35, FAIL < 0.35
   32px: PASS >= 0.40 silhouette IoU, WARN >= 0.25, FAIL < 0.25
  Expression (edge density in head region):
   128px: PASS >= 0.08, WARN >= 0.04
    64px: PASS >= 0.05, WARN >= 0.02
    32px: informational only (expression unreadable at 32px is expected)

Usage:
  python3 LTG_TOOL_thumbnail_readability.py <character.png> [options]

  --scales 128,64,32   Comma-separated target heights (default: 128,64,32)
  --output PATH        Output contact sheet PNG
  --json               Print metrics as JSON
  --report PATH        Write markdown report
  --all-in-dir DIR     Run on all character PNGs in directory

Programmatic API:
  test_readability(img_path, scales=[128,64,32]) -> dict
  generate_contact_sheet(img_path, results, output_path) -> str

Author: Morgan Walsh — Cycle 50
Date: 2026-03-30
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont
import numpy as np

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

# ── Constants ────────────────────────────────────────────────────────────────
MAX_DIM = 1280
BG_TOLERANCE = 40
BG_SAMPLE_SIZE = 15
DEFAULT_SCALES = [128, 64, 32]

# Per-scale thresholds: {height: (pass_sil, warn_sil, pass_expr, warn_expr)}
THRESHOLDS = {
    128: {"sil_pass": 0.70, "sil_warn": 0.50, "expr_pass": 0.08, "expr_warn": 0.04},
    64:  {"sil_pass": 0.55, "sil_warn": 0.35, "expr_pass": 0.05, "expr_warn": 0.02},
    32:  {"sil_pass": 0.40, "sil_warn": 0.25, "expr_pass": 0.0,  "expr_warn": 0.0},
}

# Fallback thresholds for non-standard scales (interpolated)
def _get_thresholds(height: int) -> Dict:
    if height in THRESHOLDS:
        return THRESHOLDS[height]
    # Linear interpolation between closest known scales
    known = sorted(THRESHOLDS.keys())
    if height >= known[-1]:
        return THRESHOLDS[known[-1]]
    if height <= known[0]:
        return THRESHOLDS[known[0]]
    for i in range(len(known) - 1):
        if known[i] <= height <= known[i + 1]:
            lo, hi = known[i], known[i + 1]
            t = (height - lo) / (hi - lo)
            result = {}
            for k in THRESHOLDS[lo]:
                result[k] = THRESHOLDS[lo][k] + t * (THRESHOLDS[hi][k] - THRESHOLDS[lo][k])
            return result
    return THRESHOLDS[known[-1]]


# ── Background / foreground detection ────────────────────────────────────────

def _detect_bg(img_arr: np.ndarray) -> np.ndarray:
    h, w = img_arr.shape[:2]
    s = min(BG_SAMPLE_SIZE, h // 4, w // 4)
    if s < 1:
        s = 1
    corners = [
        img_arr[:s, :s],
        img_arr[:s, w-s:],
        img_arr[h-s:, :s],
        img_arr[h-s:, w-s:],
    ]
    samples = np.concatenate([c.reshape(-1, 3) for c in corners], axis=0)
    return np.median(samples, axis=0).astype(np.uint8)


def _fg_mask(img_arr: np.ndarray, bg_color: np.ndarray) -> np.ndarray:
    diff = np.abs(img_arr.astype(np.int16) - bg_color.astype(np.int16))
    return np.any(diff > BG_TOLERANCE, axis=2)


def _fg_bbox(mask: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
    """Get bounding box of foreground: (y_min, y_max, x_min, x_max)."""
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not np.any(rows):
        return None
    y_min, y_max = np.where(rows)[0][[0, -1]]
    x_min, x_max = np.where(cols)[0][[0, -1]]
    return (int(y_min), int(y_max), int(x_min), int(x_max))


# ── Edge detection ───────────────────────────────────────────────────────────

def _edge_density(img_arr: np.ndarray) -> float:
    """Fraction of pixels that are edge pixels (Canny)."""
    if HAS_CV2:
        gray = cv2.cvtColor(img_arr, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        return float(np.sum(edges > 0) / edges.size)
    else:
        # Fallback: simple gradient magnitude
        gray = np.mean(img_arr.astype(np.float64), axis=2)
        gx = np.abs(np.diff(gray, axis=1))
        gy = np.abs(np.diff(gray, axis=0))
        gx_pad = np.pad(gx, ((0, 0), (0, 1)), mode='constant')
        gy_pad = np.pad(gy, ((0, 1), (0, 0)), mode='constant')
        mag = np.sqrt(gx_pad ** 2 + gy_pad ** 2)
        threshold = 30.0
        return float(np.sum(mag > threshold) / mag.size)


def _edge_preservation(full_arr: np.ndarray, small_arr: np.ndarray) -> float:
    """Ratio of edge pixels preserved after downscale+upscale vs original."""
    full_density = _edge_density(full_arr)
    if full_density == 0:
        return 1.0
    # Upscale small back to full size for comparison
    if HAS_CV2:
        h, w = full_arr.shape[:2]
        upscaled = cv2.resize(small_arr, (w, h), interpolation=cv2.INTER_NEAREST)
    else:
        small_img = Image.fromarray(small_arr)
        upscaled = np.array(small_img.resize((full_arr.shape[1], full_arr.shape[0]),
                                              Image.NEAREST))
    small_density = _edge_density(upscaled)
    return min(1.0, small_density / full_density)


# ── Hue bucket stability ────────────────────────────────────────────────────

def _top_hue_buckets(img_arr: np.ndarray, fg_mask: np.ndarray, n_buckets: int = 12) -> np.ndarray:
    """Return histogram of hue distribution in foreground pixels (n_buckets bins)."""
    if not np.any(fg_mask):
        return np.zeros(n_buckets, dtype=np.float64)
    if HAS_CV2:
        hsv = cv2.cvtColor(img_arr, cv2.COLOR_RGB2HSV)
        hues = hsv[:, :, 0][fg_mask].astype(np.float64) * 2.0  # 0-360
    else:
        # Manual hue extraction
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        fg_r = r[fg_mask].astype(np.float64)
        fg_g = g[fg_mask].astype(np.float64)
        fg_b = b[fg_mask].astype(np.float64)
        cmax = np.maximum(np.maximum(fg_r, fg_g), fg_b)
        cmin = np.minimum(np.minimum(fg_r, fg_g), fg_b)
        delta = cmax - cmin
        hues = np.zeros_like(fg_r)
        mask_r = (cmax == fg_r) & (delta > 0)
        mask_g = (cmax == fg_g) & (delta > 0) & ~mask_r
        mask_b = (delta > 0) & ~mask_r & ~mask_g
        hues[mask_r] = 60.0 * (((fg_g[mask_r] - fg_b[mask_r]) / delta[mask_r]) % 6)
        hues[mask_g] = 60.0 * ((fg_b[mask_g] - fg_r[mask_g]) / delta[mask_g] + 2)
        hues[mask_b] = 60.0 * ((fg_r[mask_b] - fg_g[mask_b]) / delta[mask_b] + 4)

    hist, _ = np.histogram(hues, bins=n_buckets, range=(0, 360))
    total = hist.sum()
    if total == 0:
        return np.zeros(n_buckets, dtype=np.float64)
    return hist.astype(np.float64) / total


def _hue_stability(full_arr: np.ndarray, small_arr: np.ndarray,
                   full_fg: np.ndarray, small_fg: np.ndarray) -> float:
    """Cosine similarity of hue distributions between full and small."""
    h1 = _top_hue_buckets(full_arr, full_fg)
    h2 = _top_hue_buckets(small_arr, small_fg)
    dot = np.dot(h1, h2)
    n1 = np.linalg.norm(h1)
    n2 = np.linalg.norm(h2)
    if n1 == 0 or n2 == 0:
        return 1.0
    return float(dot / (n1 * n2))


# ── Head region detection ───────────────────────────────────────────────────

def _estimate_head_region(fg_mask: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
    """Estimate head bounding box as top 25-30% of figure height."""
    bbox = _fg_bbox(fg_mask)
    if bbox is None:
        return None
    y_min, y_max, x_min, x_max = bbox
    fig_h = y_max - y_min + 1
    head_h = max(1, int(fig_h * 0.28))
    return (y_min, y_min + head_h, x_min, x_max)


# ── Per-scale evaluation ────────────────────────────────────────────────────

def _evaluate_scale(
    full_arr: np.ndarray,
    full_fg: np.ndarray,
    target_height: int,
) -> Dict:
    """Evaluate character readability at a given scale height."""
    h_orig, w_orig = full_arr.shape[:2]
    if h_orig == 0:
        return {"scale": target_height, "grade": "FAIL", "error": "empty image"}

    scale_ratio = target_height / h_orig
    target_width = max(1, int(w_orig * scale_ratio))

    # Downscale
    full_img = Image.fromarray(full_arr)
    small_img = full_img.resize((target_width, target_height), Image.LANCZOS)
    small_arr = np.array(small_img)

    bg_small = _detect_bg(small_arr)
    small_fg = _fg_mask(small_arr, bg_small)

    # 1. Silhouette preservation (IoU of upscaled-small-fg vs full-fg)
    if HAS_CV2:
        small_fg_up = cv2.resize(small_fg.astype(np.uint8), (w_orig, h_orig),
                                  interpolation=cv2.INTER_NEAREST).astype(bool)
    else:
        small_fg_img = Image.fromarray(small_fg.astype(np.uint8) * 255)
        small_fg_up = np.array(
            small_fg_img.resize((w_orig, h_orig), Image.NEAREST)
        ) > 127

    intersection = np.sum(full_fg & small_fg_up)
    union = np.sum(full_fg | small_fg_up)
    sil_iou = float(intersection / union) if union > 0 else 1.0

    # 2. Edge preservation
    edge_pres = _edge_preservation(full_arr, small_arr)

    # 3. Hue stability
    hue_stab = _hue_stability(full_arr, small_arr, full_fg, small_fg)

    # 4. Expression readability (edge density in head region at this scale)
    head_bbox = _estimate_head_region(small_fg)
    expr_density = 0.0
    if head_bbox is not None:
        hy0, hy1, hx0, hx1 = head_bbox
        hy1 = min(hy1, small_arr.shape[0])
        hx1 = min(hx1, small_arr.shape[1])
        if hy1 > hy0 and hx1 > hx0:
            head_region = small_arr[hy0:hy1, hx0:hx1]
            expr_density = _edge_density(head_region)

    # Grading
    thresholds = _get_thresholds(target_height)
    if sil_iou >= thresholds["sil_pass"]:
        sil_grade = "PASS"
    elif sil_iou >= thresholds["sil_warn"]:
        sil_grade = "WARN"
    else:
        sil_grade = "FAIL"

    expr_grade = "INFO"
    if thresholds["expr_pass"] > 0:
        if expr_density >= thresholds["expr_pass"]:
            expr_grade = "PASS"
        elif expr_density >= thresholds["expr_warn"]:
            expr_grade = "WARN"
        else:
            expr_grade = "FAIL"

    # Overall = worst of silhouette and expression grades
    grade_order = {"FAIL": 0, "WARN": 1, "INFO": 2, "PASS": 3}
    overall = min([sil_grade, expr_grade], key=lambda g: grade_order.get(g, 2))
    if overall == "INFO":
        overall = sil_grade  # INFO doesn't affect overall

    return {
        "scale": target_height,
        "scale_ratio": round(scale_ratio, 4),
        "silhouette_iou": round(sil_iou, 4),
        "silhouette_grade": sil_grade,
        "edge_preservation": round(edge_pres, 4),
        "hue_stability": round(hue_stab, 4),
        "expression_density": round(expr_density, 4),
        "expression_grade": expr_grade,
        "overall_grade": overall,
        "thumbnail_size": (target_width, target_height),
    }


# ── Contact sheet generation ────────────────────────────────────────────────

def generate_contact_sheet(
    img_path: str,
    results: Dict,
    output_path: str,
) -> str:
    """Generate a multi-scale contact sheet showing character at each test scale."""
    full_img = Image.open(img_path).convert("RGB")

    # Enforce max dim on source
    if full_img.width > MAX_DIM or full_img.height > MAX_DIM:
        full_img.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)

    scales = results["scales"]
    n_scales = len(scales)

    # Layout: each scale gets a column with: actual-size thumbnail + 4x magnified version
    mag = 4  # magnification factor for display
    col_width = 160
    header_h = 40
    label_h = 60
    row_h = 200
    total_w = min(MAX_DIM, col_width * (n_scales + 1) + 20)
    total_h = min(MAX_DIM, header_h + row_h * 2 + label_h + 20)

    canvas = Image.new("RGB", (total_w, total_h), (30, 30, 30))
    draw = ImageDraw.Draw(canvas)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except (IOError, OSError):
        font = ImageFont.load_default()
        font_sm = font

    # Title
    name = Path(img_path).stem
    draw.text((10, 8), f"Thumbnail Readability: {name}", fill=(255, 255, 255), font=font)

    # Reference column
    ref_x = 10
    ref_y = header_h + 10
    ref_thumb = full_img.copy()
    ref_thumb.thumbnail((col_width - 20, row_h - 20), Image.LANCZOS)
    canvas.paste(ref_thumb, (ref_x, ref_y))
    draw = ImageDraw.Draw(canvas)
    draw.text((ref_x, ref_y + ref_thumb.height + 4), "FULL", fill=(180, 180, 180), font=font_sm)

    # Scale columns
    for i, scale_result in enumerate(scales):
        sx = ref_x + col_width * (i + 1)
        sy = header_h + 10

        target_h = scale_result["scale"]
        tw, th = scale_result["thumbnail_size"]

        # Actual size thumbnail
        thumb = full_img.resize((tw, th), Image.LANCZOS)

        # Magnified version
        mag_w = min(tw * mag, col_width - 10)
        mag_h = min(th * mag, row_h - 40)
        mag_img = thumb.resize((mag_w, mag_h), Image.NEAREST)

        # Paste magnified
        canvas.paste(mag_img, (sx, sy))
        draw = ImageDraw.Draw(canvas)

        # Paste actual size below
        actual_y = sy + mag_h + 8
        canvas.paste(thumb, (sx, actual_y))
        draw = ImageDraw.Draw(canvas)

        # Grade label
        grade = scale_result["overall_grade"]
        grade_colors = {"PASS": (100, 255, 100), "WARN": (255, 200, 50), "FAIL": (255, 80, 80), "INFO": (150, 150, 255)}
        gc = grade_colors.get(grade, (200, 200, 200))

        label_y = actual_y + th + 6
        draw.text((sx, label_y), f"{target_h}px: {grade}", fill=gc, font=font_sm)
        draw.text((sx, label_y + 14),
                  f"Sil: {scale_result['silhouette_iou']:.2f}",
                  fill=(160, 160, 160), font=font_sm)
        draw.text((sx, label_y + 26),
                  f"Edge: {scale_result['edge_preservation']:.2f}",
                  fill=(160, 160, 160), font=font_sm)
        draw.text((sx, label_y + 38),
                  f"Expr: {scale_result['expression_density']:.3f}",
                  fill=(160, 160, 160), font=font_sm)

    canvas.save(output_path)
    return output_path


# ── Main API ─────────────────────────────────────────────────────────────────

def test_readability(
    img_path: str,
    scales: List[int] = None,
) -> Dict:
    """
    Test character readability at multiple thumbnail scales.

    Parameters
    ----------
    img_path : str
        Path to character PNG.
    scales : list of int
        Target heights to test (default: [128, 64, 32]).

    Returns
    -------
    dict
        {
          "file": str,
          "scales": list of per-scale result dicts,
          "overall_grade": "PASS" | "WARN" | "FAIL",
          "pass_count": int,
          "warn_count": int,
          "fail_count": int,
        }
    """
    if scales is None:
        scales = DEFAULT_SCALES

    img = Image.open(img_path).convert("RGB")
    if img.width > MAX_DIM or img.height > MAX_DIM:
        img.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)

    img_arr = np.array(img)
    bg = _detect_bg(img_arr)
    fg = _fg_mask(img_arr, bg)

    scale_results = []
    for target_h in sorted(scales, reverse=True):
        result = _evaluate_scale(img_arr, fg, target_h)
        scale_results.append(result)

    # Aggregate
    grades = [r["overall_grade"] for r in scale_results]
    pass_count = grades.count("PASS")
    warn_count = grades.count("WARN")
    fail_count = grades.count("FAIL")

    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0:
        overall = "WARN"
    else:
        overall = "PASS"

    return {
        "file": img_path,
        "scales": scale_results,
        "overall_grade": overall,
        "pass_count": pass_count,
        "warn_count": warn_count,
        "fail_count": fail_count,
    }


def batch_test(directory: str, scales: List[int] = None) -> List[Dict]:
    """Run readability test on all character PNGs in a directory."""
    results = []
    p = Path(directory)
    for png in sorted(p.glob("*.png")):
        try:
            r = test_readability(str(png), scales)
            results.append(r)
        except Exception as e:
            results.append({"file": str(png), "error": str(e), "overall_grade": "ERROR"})
    return results


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Thumbnail readability test for character assets")
    parser.add_argument("input", help="Character PNG or directory")
    parser.add_argument("--scales", default="128,64,32",
                        help="Comma-separated target heights (default: 128,64,32)")
    parser.add_argument("--output", default=None, help="Output contact sheet PNG path")
    parser.add_argument("--json", action="store_true", help="Print metrics as JSON")
    parser.add_argument("--report", default=None, help="Write markdown report to PATH")

    args = parser.parse_args()
    scales = [int(x) for x in args.scales.split(",")]

    input_path = args.input
    if os.path.isdir(input_path):
        results = batch_test(input_path, scales)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for r in results:
                name = Path(r["file"]).name
                grade = r.get("overall_grade", "ERROR")
                print(f"{name}: {grade}")
                for sr in r.get("scales", []):
                    print(f"  {sr['scale']}px: {sr['overall_grade']} "
                          f"(sil={sr['silhouette_iou']:.2f}, "
                          f"edge={sr['edge_preservation']:.2f}, "
                          f"expr={sr['expression_density']:.3f})")
    else:
        result = test_readability(input_path, scales)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"File: {Path(input_path).name}")
            print(f"Overall: {result['overall_grade']}")
            for sr in result["scales"]:
                print(f"  {sr['scale']}px: {sr['overall_grade']} "
                      f"(sil={sr['silhouette_iou']:.2f}, "
                      f"edge={sr['edge_preservation']:.2f}, "
                      f"expr={sr['expression_density']:.3f})")

        # Contact sheet
        if args.output:
            generate_contact_sheet(input_path, result, args.output)
            print(f"Contact sheet: {args.output}")

    if args.report:
        # Generate markdown report
        if os.path.isdir(input_path):
            all_results = results
        else:
            all_results = [result]
        lines = ["# Thumbnail Readability Report", "", f"**Date:** 2026-03-30", ""]
        for r in all_results:
            name = Path(r["file"]).name
            lines.append(f"## {name}")
            lines.append(f"**Overall:** {r.get('overall_grade', 'ERROR')}")
            lines.append("")
            lines.append("| Scale | Grade | Silhouette IoU | Edge Pres | Hue Stab | Expr Density |")
            lines.append("|-------|-------|---------------|-----------|----------|-------------|")
            for sr in r.get("scales", []):
                lines.append(
                    f"| {sr['scale']}px | {sr['overall_grade']} | "
                    f"{sr['silhouette_iou']:.3f} | "
                    f"{sr['edge_preservation']:.3f} | "
                    f"{sr['hue_stability']:.3f} | "
                    f"{sr['expression_density']:.4f} |"
                )
            lines.append("")
        with open(args.report, "w") as f:
            f.write("\n".join(lines))
        print(f"Report: {args.report}")


if __name__ == "__main__":
    main()
