#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_char_compare.py — v1.0.0 (Cycle 50, Morgan Walsh)

Before/After Character Comparison Tool.

Takes two character renders (old vs new approach) and produces:
  1. Side-by-side comparison PNG with labeled versions
  2. Pixel-level difference heatmap
  3. Quantitative metrics (SSIM, pixel delta %, silhouette overlap)

Designed for evaluating character quality improvements (Maya/Rin prototypes).

Usage:
  python3 LTG_TOOL_char_compare.py <old.png> <new.png> [options]

  --output PATH       Output comparison PNG (default: LTG_COMP_<old>_vs_<new>.png)
  --label-old TEXT     Label for old image (default: "OLD")
  --label-new TEXT     Label for new image (default: "NEW")
  --crop X,Y,W,H      Crop both images to region before comparing
  --json              Print metrics as JSON to stdout
  --report PATH       Write markdown report to PATH

Programmatic API:
  compare_characters(old_path, new_path, **kwargs) -> dict
  generate_comparison_png(old_img, new_img, metrics, output_path, **kwargs)

Metrics returned:
  - ssim: Structural Similarity Index (0-1, higher = more similar)
  - pixel_delta_pct: % of pixels differing by > threshold
  - mean_abs_diff: Mean absolute pixel difference (0-255)
  - silhouette_iou: Intersection over Union of foreground masks
  - fg_pixel_delta: % of FOREGROUND pixels that changed (ignores bg)
  - hue_shift_mean: Mean hue shift in changed foreground regions (degrees)
  - value_shift_mean: Mean value shift in changed foreground regions

Author: Morgan Walsh — Cycle 50
Date: 2026-03-30
"""

import sys
import os
import json
import math
import argparse
from pathlib import Path
from typing import Optional, Tuple, Dict

from PIL import Image, ImageDraw, ImageFont
import numpy as np

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

# ── Constants ────────────────────────────────────────────────────────────────
MAX_DIM = 1280
BG_TOLERANCE = 40          # per-channel tolerance for background detection
BG_SAMPLE_SIZE = 15        # corner sample region for bg detection
DIFF_THRESHOLD = 20        # pixel diff > this counts as "changed"
HEATMAP_COLORMAP = cv2.COLORMAP_JET if HAS_CV2 else None

# ── Background detection ─────────────────────────────────────────────────────

def _detect_bg(img_arr: np.ndarray) -> np.ndarray:
    """Detect background color from corner samples. Returns (R, G, B)."""
    h, w = img_arr.shape[:2]
    s = min(BG_SAMPLE_SIZE, h // 4, w // 4)
    corners = [
        img_arr[:s, :s],
        img_arr[:s, w-s:],
        img_arr[h-s:, :s],
        img_arr[h-s:, w-s:],
    ]
    samples = np.concatenate([c.reshape(-1, 3) for c in corners], axis=0)
    return np.median(samples, axis=0).astype(np.uint8)


def _fg_mask(img_arr: np.ndarray, bg_color: np.ndarray) -> np.ndarray:
    """Return boolean mask where True = foreground pixel."""
    diff = np.abs(img_arr.astype(np.int16) - bg_color.astype(np.int16))
    return np.any(diff > BG_TOLERANCE, axis=2)


# ── Metrics ──────────────────────────────────────────────────────────────────

def _compute_ssim_gray(old_gray: np.ndarray, new_gray: np.ndarray) -> float:
    """Compute SSIM between two grayscale arrays. Uses cv2 if available, else manual."""
    if HAS_CV2:
        from skimage.metrics import structural_similarity
        try:
            return float(structural_similarity(old_gray, new_gray))
        except ImportError:
            pass
    # Manual SSIM (simplified Wang et al. 2004)
    C1 = (0.01 * 255) ** 2
    C2 = (0.03 * 255) ** 2
    mu_x = old_gray.astype(np.float64).mean()
    mu_y = new_gray.astype(np.float64).mean()
    sig_x = old_gray.astype(np.float64).var()
    sig_y = new_gray.astype(np.float64).var()
    sig_xy = ((old_gray.astype(np.float64) - mu_x) *
              (new_gray.astype(np.float64) - mu_y)).mean()
    num = (2 * mu_x * mu_y + C1) * (2 * sig_xy + C2)
    den = (mu_x ** 2 + mu_y ** 2 + C1) * (sig_x + sig_y + C2)
    return float(num / den) if den != 0 else 1.0


def _compute_metrics(old_arr: np.ndarray, new_arr: np.ndarray) -> Dict:
    """Compute all comparison metrics between two RGB arrays of same size."""
    # Grayscale
    old_gray = np.mean(old_arr.astype(np.float64), axis=2).astype(np.uint8)
    new_gray = np.mean(new_arr.astype(np.float64), axis=2).astype(np.uint8)

    # SSIM
    ssim_val = _compute_ssim_gray(old_gray, new_gray)

    # Pixel delta
    abs_diff = np.abs(old_arr.astype(np.int16) - new_arr.astype(np.int16))
    max_channel_diff = np.max(abs_diff, axis=2)
    changed_mask = max_channel_diff > DIFF_THRESHOLD
    total_px = old_arr.shape[0] * old_arr.shape[1]
    pixel_delta_pct = float(np.sum(changed_mask) / total_px * 100)
    mean_abs_diff = float(np.mean(abs_diff))

    # Foreground masks
    old_bg = _detect_bg(old_arr)
    new_bg = _detect_bg(new_arr)
    old_fg = _fg_mask(old_arr, old_bg)
    new_fg = _fg_mask(new_arr, new_bg)

    # Silhouette IoU
    intersection = np.sum(old_fg & new_fg)
    union = np.sum(old_fg | new_fg)
    sil_iou = float(intersection / union) if union > 0 else 1.0

    # Foreground-only pixel delta
    fg_union = old_fg | new_fg
    fg_changed = changed_mask & fg_union
    fg_total = np.sum(fg_union)
    fg_pixel_delta = float(np.sum(fg_changed) / fg_total * 100) if fg_total > 0 else 0.0

    # Hue/value shift in changed foreground regions
    hue_shift_mean = 0.0
    value_shift_mean = 0.0
    if HAS_CV2 and np.sum(fg_changed) > 0:
        old_hsv = cv2.cvtColor(old_arr, cv2.COLOR_RGB2HSV).astype(np.float64)
        new_hsv = cv2.cvtColor(new_arr, cv2.COLOR_RGB2HSV).astype(np.float64)
        # Hue is 0-179 in OpenCV
        hue_diff = np.abs(old_hsv[:, :, 0] - new_hsv[:, :, 0])
        hue_diff = np.minimum(hue_diff, 180.0 - hue_diff) * 2.0  # scale to 0-360 range
        hue_shift_mean = float(np.mean(hue_diff[fg_changed]))
        val_diff = new_hsv[:, :, 2] - old_hsv[:, :, 2]
        value_shift_mean = float(np.mean(val_diff[fg_changed]))

    return {
        "ssim": round(ssim_val, 4),
        "pixel_delta_pct": round(pixel_delta_pct, 2),
        "mean_abs_diff": round(mean_abs_diff, 2),
        "silhouette_iou": round(sil_iou, 4),
        "fg_pixel_delta": round(fg_pixel_delta, 2),
        "hue_shift_mean": round(hue_shift_mean, 2),
        "value_shift_mean": round(value_shift_mean, 2),
    }


# ── Diff heatmap ─────────────────────────────────────────────────────────────

def _make_diff_heatmap(old_arr: np.ndarray, new_arr: np.ndarray) -> np.ndarray:
    """Generate a difference heatmap as an RGB array."""
    abs_diff = np.max(np.abs(old_arr.astype(np.int16) - new_arr.astype(np.int16)), axis=2)
    # Normalize to 0-255
    max_val = abs_diff.max()
    if max_val == 0:
        norm = np.zeros_like(abs_diff, dtype=np.uint8)
    else:
        norm = (abs_diff.astype(np.float64) / max_val * 255).astype(np.uint8)

    if HAS_CV2:
        heatmap_bgr = cv2.applyColorMap(norm, cv2.COLORMAP_JET)
        heatmap_rgb = cv2.cvtColor(heatmap_bgr, cv2.COLOR_BGR2RGB)
    else:
        # Fallback: grayscale heatmap
        heatmap_rgb = np.stack([norm, norm, norm], axis=2)
    return heatmap_rgb


# ── Comparison PNG generation ────────────────────────────────────────────────

def generate_comparison_png(
    old_img: Image.Image,
    new_img: Image.Image,
    metrics: Dict,
    output_path: str,
    label_old: str = "OLD",
    label_new: str = "NEW",
) -> str:
    """
    Generate a side-by-side comparison PNG: [OLD | NEW | DIFF HEATMAP]
    with labels and metrics summary strip at bottom.

    Returns output path.
    """
    # Ensure same size
    w = max(old_img.width, new_img.width)
    h = max(old_img.height, new_img.height)

    # Pad smaller image to match
    def _pad(img, tw, th):
        if img.width == tw and img.height == th:
            return img
        padded = Image.new("RGB", (tw, th), (200, 200, 200))
        padded.paste(img, ((tw - img.width) // 2, (th - img.height) // 2))
        return padded

    old_padded = _pad(old_img, w, h)
    new_padded = _pad(new_img, w, h)

    # Diff heatmap
    old_arr = np.array(old_padded)
    new_arr = np.array(new_padded)
    heatmap_arr = _make_diff_heatmap(old_arr, new_arr)
    heatmap_img = Image.fromarray(heatmap_arr)

    # Layout: 3 panels side by side + labels (30px) + metrics strip (60px)
    label_h = 30
    metrics_h = 60
    gap = 4
    panel_w = w
    total_w = panel_w * 3 + gap * 2
    total_h = label_h + h + metrics_h

    # Enforce max dim
    scale = 1.0
    if total_w > MAX_DIM or total_h > MAX_DIM:
        scale = min(MAX_DIM / total_w, MAX_DIM / total_h)
        panel_w = int(w * scale)
        ph = int(h * scale)
        old_padded = old_padded.resize((panel_w, ph), Image.LANCZOS)
        new_padded = new_padded.resize((panel_w, ph), Image.LANCZOS)
        heatmap_img = heatmap_img.resize((panel_w, ph), Image.LANCZOS)
        total_w = panel_w * 3 + gap * 2
        total_h = label_h + ph + metrics_h
        h = ph

    canvas = Image.new("RGB", (total_w, total_h), (40, 40, 40))
    draw = ImageDraw.Draw(canvas)

    # Try to load a font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except (IOError, OSError):
        font = ImageFont.load_default()
        font_sm = font

    # Draw labels
    x_offsets = [0, panel_w + gap, (panel_w + gap) * 2]
    labels = [label_old, label_new, "DIFF"]
    colors = [(255, 120, 120), (120, 255, 120), (120, 180, 255)]
    for i, (xo, lbl, col) in enumerate(zip(x_offsets, labels, colors)):
        draw.text((xo + 8, 6), lbl, fill=col, font=font)

    # Paste panels
    canvas.paste(old_padded, (x_offsets[0], label_h))
    draw = ImageDraw.Draw(canvas)
    canvas.paste(new_padded, (x_offsets[1], label_h))
    draw = ImageDraw.Draw(canvas)
    canvas.paste(heatmap_img, (x_offsets[2], label_h))
    draw = ImageDraw.Draw(canvas)

    # Metrics strip
    my = label_h + h + 8
    metrics_text = (
        f"SSIM: {metrics['ssim']:.3f}  |  "
        f"Pixel Delta: {metrics['pixel_delta_pct']:.1f}%  |  "
        f"FG Delta: {metrics['fg_pixel_delta']:.1f}%  |  "
        f"Silhouette IoU: {metrics['silhouette_iou']:.3f}"
    )
    draw.text((8, my), metrics_text, fill=(220, 220, 220), font=font_sm)
    if metrics.get("hue_shift_mean", 0) > 0 or metrics.get("value_shift_mean", 0) != 0:
        line2 = (
            f"Hue Shift: {metrics['hue_shift_mean']:.1f} deg  |  "
            f"Value Shift: {metrics['value_shift_mean']:+.1f}"
        )
        draw.text((8, my + 18), line2, fill=(180, 180, 180), font=font_sm)

    canvas.save(output_path)
    return output_path


# ── Main API ─────────────────────────────────────────────────────────────────

def compare_characters(
    old_path: str,
    new_path: str,
    crop: Optional[Tuple[int, int, int, int]] = None,
    label_old: str = "OLD",
    label_new: str = "NEW",
    output_path: Optional[str] = None,
) -> Dict:
    """
    Compare two character renders. Returns metrics dict.

    Parameters
    ----------
    old_path : str
        Path to old/reference render.
    new_path : str
        Path to new/candidate render.
    crop : tuple, optional
        (x, y, w, h) to crop both images before comparing.
    label_old, label_new : str
        Labels for the comparison PNG.
    output_path : str, optional
        Path for comparison PNG. Auto-generated if None.

    Returns
    -------
    dict
        Metrics dict plus "comparison_png" path and "grade" (IMPROVED/SIMILAR/REGRESSED).
    """
    old_img = Image.open(old_path).convert("RGB")
    new_img = Image.open(new_path).convert("RGB")

    if crop:
        x, y, w, h = crop
        old_img = old_img.crop((x, y, x + w, y + h))
        new_img = new_img.crop((x, y, x + w, y + h))

    # Resize to match if different sizes
    if old_img.size != new_img.size:
        target_w = max(old_img.width, new_img.width)
        target_h = max(old_img.height, new_img.height)
        old_img = old_img.resize((target_w, target_h), Image.LANCZOS)
        new_img = new_img.resize((target_w, target_h), Image.LANCZOS)

    old_arr = np.array(old_img)
    new_arr = np.array(new_img)

    metrics = _compute_metrics(old_arr, new_arr)

    # Grade: heuristic based on foreground change + silhouette stability
    if metrics["fg_pixel_delta"] < 5.0 and metrics["silhouette_iou"] > 0.95:
        grade = "SIMILAR"
    elif metrics["silhouette_iou"] < 0.7:
        grade = "MAJOR_CHANGE"
    else:
        grade = "MODIFIED"

    metrics["grade"] = grade

    # Generate comparison PNG
    if output_path is None:
        old_stem = Path(old_path).stem
        new_stem = Path(new_path).stem
        output_path = f"LTG_COMP_{old_stem}_vs_{new_stem}.png"

    png_path = generate_comparison_png(
        old_img, new_img, metrics, output_path,
        label_old=label_old, label_new=label_new,
    )
    metrics["comparison_png"] = png_path

    return metrics


def generate_report(metrics: Dict, old_path: str, new_path: str) -> str:
    """Generate a markdown report from comparison metrics."""
    lines = [
        "# Character Comparison Report",
        "",
        f"**Old:** `{old_path}`",
        f"**New:** `{new_path}`",
        f"**Grade:** {metrics['grade']}",
        "",
        "## Metrics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| SSIM | {metrics['ssim']:.4f} |",
        f"| Pixel Delta | {metrics['pixel_delta_pct']:.1f}% |",
        f"| Mean Abs Diff | {metrics['mean_abs_diff']:.1f} |",
        f"| Silhouette IoU | {metrics['silhouette_iou']:.4f} |",
        f"| FG Pixel Delta | {metrics['fg_pixel_delta']:.1f}% |",
        f"| Hue Shift (mean) | {metrics['hue_shift_mean']:.1f} deg |",
        f"| Value Shift (mean) | {metrics['value_shift_mean']:+.1f} |",
        "",
        f"**Comparison PNG:** `{metrics.get('comparison_png', 'N/A')}`",
        "",
        "## Interpretation",
        "",
    ]
    if metrics["grade"] == "SIMILAR":
        lines.append("Changes are minimal. Old and new renders are nearly identical.")
    elif metrics["grade"] == "MAJOR_CHANGE":
        lines.append("Significant silhouette change detected. Verify character identity is preserved.")
    else:
        lines.append("Moderate changes detected. Review comparison PNG for visual quality assessment.")

    if metrics["silhouette_iou"] < 0.8:
        lines.append("")
        lines.append("**WARNING:** Silhouette IoU below 0.80 — character shape changed significantly.")
    if metrics["hue_shift_mean"] > 15.0:
        lines.append("")
        lines.append("**NOTE:** Mean hue shift > 15 degrees — color palette may have shifted.")

    return "\n".join(lines)


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Before/after character comparison tool")
    parser.add_argument("old", help="Path to old/reference render")
    parser.add_argument("new", help="Path to new/candidate render")
    parser.add_argument("--output", default=None, help="Output comparison PNG path")
    parser.add_argument("--label-old", default="OLD", help="Label for old image")
    parser.add_argument("--label-new", default="NEW", help="Label for new image")
    parser.add_argument("--crop", default=None,
                        help="Crop region: X,Y,W,H")
    parser.add_argument("--json", action="store_true", help="Print metrics as JSON")
    parser.add_argument("--report", default=None, help="Write markdown report to PATH")

    args = parser.parse_args()

    crop = None
    if args.crop:
        crop = tuple(int(x) for x in args.crop.split(","))
        if len(crop) != 4:
            print("ERROR: --crop must be X,Y,W,H (4 integers)", file=sys.stderr)
            sys.exit(2)

    metrics = compare_characters(
        args.old, args.new,
        crop=crop,
        label_old=args.label_old,
        label_new=args.label_new,
        output_path=args.output,
    )

    if args.json:
        print(json.dumps(metrics, indent=2))
    else:
        print(f"Grade: {metrics['grade']}")
        print(f"SSIM: {metrics['ssim']:.4f}")
        print(f"Pixel Delta: {metrics['pixel_delta_pct']:.1f}%")
        print(f"FG Delta: {metrics['fg_pixel_delta']:.1f}%")
        print(f"Silhouette IoU: {metrics['silhouette_iou']:.4f}")
        print(f"Hue Shift: {metrics['hue_shift_mean']:.1f} deg")
        print(f"Value Shift: {metrics['value_shift_mean']:+.1f}")
        print(f"Comparison PNG: {metrics['comparison_png']}")

    if args.report:
        report_md = generate_report(metrics, args.old, args.new)
        with open(args.report, "w") as f:
            f.write(report_md)
        print(f"Report written to: {args.report}")


if __name__ == "__main__":
    main()
