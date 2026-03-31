#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_silhouette_distinctiveness.py — v2.0.0 (Cycle 51, Kai Nakamura)

Character Silhouette Distinctiveness Tool.

Renders each character as a black silhouette at multiple scales (100%, 50%, 25%)
and measures how distinguishable they are from each other. Designed to catch the
problem where characters (e.g. Cosmo and Miri) have nearly identical silhouettes.

Metrics:
  For each character pair at each scale:
    1. Silhouette Overlap Ratio (SOR):
       SOR = intersection_pixels / min(pixels_A, pixels_B)
       High SOR = silhouettes share most of their mass = BAD.

    2. Width Profile Correlation (WPC):
       For each row, count horizontal extent of the silhouette.
       Compute Pearson correlation between two characters' width profiles.
       High WPC = silhouettes have the same outline shape = BAD.

    3. Centroid Spread:
       Checks that characters occupy distinct spatial extents after
       alignment to same bounding box height.

  Combined Distinctiveness Score:
    DS = 1.0 - (0.5 * SOR + 0.5 * WPC)
    DS near 1.0 = very distinct. DS near 0.0 = nearly identical.

Thresholds:
  FAIL: DS < 0.15 — silhouettes are nearly identical
  WARN: DS < 0.30 — silhouettes marginally distinct
  PASS: DS >= 0.30 — silhouettes read as distinct

Input: Individual character PNGs (turnaround front views or lineup extractions).
       Can also accept a directory and auto-discover character files.

Output:
  - Text report with pairwise distinctiveness scores at each scale.
  - Optional multi-scale silhouette contact sheet PNG.
  - JSON output via --json flag.

Usage:
  python3 LTG_TOOL_silhouette_distinctiveness.py <dir_or_files...>
          [--scales 1.0,0.5,0.25]
          [--bg-tolerance 45]
          [--output silhouette_report.png]
          [--json]
          [--report path/to/report.md]

v2.0.0 C51 — scikit-image morphological ops for silhouette cleanup (binary_fill_holes,
             remove_small_objects). Shapely Polygon for IoU/area computation —
             faster and more accurate than pixel-counting. New metric: Hausdorff
             distance between silhouette outlines via Shapely.

Author: Kai Nakamura — Cycle 50 (v1), Cycle 51 (v2)
Date: 2026-03-30
"""

import sys
import os
import argparse
import json
import math
import random
import numpy as np
from PIL import Image, ImageDraw

try:
    from scipy.ndimage import binary_fill_holes
    from skimage.morphology import remove_small_objects
    from skimage.measure import find_contours, label, regionprops
    _SKIMAGE_AVAILABLE = True
except ImportError:
    _SKIMAGE_AVAILABLE = False

try:
    from shapely.geometry import Polygon as ShapelyPolygon, MultiPolygon
    from shapely.ops import unary_union
    _SHAPELY_AVAILABLE = True
except ImportError:
    _SHAPELY_AVAILABLE = False

# ─── CONFIG ──────────────────────────────────────────────────────────────────

BG_SAMPLE_SIZE = 8
BG_TOLERANCE = 45
FAIL_THRESHOLD = 0.15
WARN_THRESHOLD = 0.30
DEFAULT_SCALES = [1.0, 0.5, 0.25]
CANONICAL_HEIGHT = 400  # Normalize all silhouettes to this height for comparison

# ─── SILHOUETTE EXTRACTION ──────────────────────────────────────────────────


def detect_background_color(img):
    """Sample corners to determine background color."""
    w, h = img.size
    pixels = []
    for cx, cy in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        for dx in range(min(BG_SAMPLE_SIZE, w)):
            for dy in range(min(BG_SAMPLE_SIZE, h)):
                px = img.getpixel((min(cx + dx, w - 1), min(cy + dy, h - 1)))
                if isinstance(px, int):
                    px = (px, px, px)
                pixels.append(px[:3])
    if not pixels:
        return (255, 255, 255)
    r = sum(p[0] for p in pixels) // len(pixels)
    g = sum(p[1] for p in pixels) // len(pixels)
    b = sum(p[2] for p in pixels) // len(pixels)
    return (r, g, b)


def extract_silhouette(img, bg_color=None, bg_tolerance=BG_TOLERANCE):
    """Convert image to binary silhouette mask (1 = character, 0 = background).
    Returns numpy array of shape (H, W) with uint8 values 0 or 1.

    v2.0.0: When scikit-image is available, applies binary_fill_holes (to close
    interior gaps from highlights/transparency) and remove_small_objects (to
    eliminate stray noise pixels). This produces cleaner silhouettes.
    """
    if bg_color is None:
        bg_color = detect_background_color(img)

    rgb = img.convert("RGB")
    arr = np.array(rgb, dtype=np.int16)
    bg = np.array(bg_color, dtype=np.int16).reshape(1, 1, 3)

    diff = np.abs(arr - bg)
    is_bg = np.all(diff <= bg_tolerance, axis=2)
    mask = (~is_bg).astype(np.uint8)

    if _SKIMAGE_AVAILABLE:
        # Fill interior holes (e.g., eyes, highlight spots)
        mask_bool = mask.astype(bool)
        mask_bool = binary_fill_holes(mask_bool)
        # Remove small noise objects (< 50 pixels)
        mask_bool = remove_small_objects(mask_bool, min_size=50)
        mask = mask_bool.astype(np.uint8)

    return mask


def get_bounding_box(mask):
    """Get tight bounding box of non-zero pixels. Returns (x0, y0, x1, y1) or None."""
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not np.any(rows):
        return None
    y0, y1 = np.where(rows)[0][[0, -1]]
    x0, x1 = np.where(cols)[0][[0, -1]]
    return (int(x0), int(y0), int(x1 + 1), int(y1 + 1))


def normalize_silhouette(mask, target_height=CANONICAL_HEIGHT):
    """Crop to bounding box, then resize to canonical height preserving aspect ratio.
    Returns normalized mask as numpy array."""
    bbox = get_bounding_box(mask)
    if bbox is None:
        return np.zeros((target_height, target_height // 2), dtype=np.uint8)

    x0, y0, x1, y1 = bbox
    cropped = mask[y0:y1, x0:x1]

    h, w = cropped.shape
    if h == 0:
        return np.zeros((target_height, target_height // 2), dtype=np.uint8)

    scale = target_height / h
    new_w = max(1, int(w * scale))

    img = Image.fromarray(cropped * 255)
    img = img.resize((new_w, target_height), Image.NEAREST)
    result = (np.array(img) > 127).astype(np.uint8)
    return result


def scale_silhouette(mask, scale_factor):
    """Resize a normalized silhouette by scale_factor."""
    h, w = mask.shape
    new_h = max(1, int(h * scale_factor))
    new_w = max(1, int(w * scale_factor))
    img = Image.fromarray(mask * 255)
    img = img.resize((new_w, new_h), Image.NEAREST)
    return (np.array(img) > 127).astype(np.uint8)


# ─── METRICS ────────────────────────────────────────────────────────────────


def pad_to_same_size(mask_a, mask_b):
    """Center-pad both masks to the same canvas size."""
    h_a, w_a = mask_a.shape
    h_b, w_b = mask_b.shape
    h = max(h_a, h_b)
    w = max(w_a, w_b)

    def center_pad(m, target_h, target_w):
        mh, mw = m.shape
        pad_top = (target_h - mh) // 2
        pad_left = (target_w - mw) // 2
        result = np.zeros((target_h, target_w), dtype=np.uint8)
        result[pad_top:pad_top + mh, pad_left:pad_left + mw] = m
        return result

    return center_pad(mask_a, h, w), center_pad(mask_b, h, w)


def silhouette_overlap_ratio(mask_a, mask_b):
    """Compute SOR = intersection / min(area_A, area_B)."""
    a, b = pad_to_same_size(mask_a, mask_b)
    intersection = np.sum(a & b)
    area_a = np.sum(a)
    area_b = np.sum(b)
    min_area = min(area_a, area_b)
    if min_area == 0:
        return 0.0
    return float(intersection) / float(min_area)


def width_profile(mask):
    """Compute per-row width (rightmost - leftmost non-zero pixel + 1). Returns 1D array."""
    h, w = mask.shape
    profile = np.zeros(h, dtype=np.float64)
    for row in range(h):
        cols = np.where(mask[row] > 0)[0]
        if len(cols) > 0:
            profile[row] = cols[-1] - cols[0] + 1
    return profile


def width_profile_correlation(mask_a, mask_b):
    """Pearson correlation of width profiles."""
    a, b = pad_to_same_size(mask_a, mask_b)
    prof_a = width_profile(a)
    prof_b = width_profile(b)

    # Only compare rows where at least one has content
    valid = (prof_a > 0) | (prof_b > 0)
    if np.sum(valid) < 3:
        return 0.0

    pa = prof_a[valid]
    pb = prof_b[valid]

    std_a = np.std(pa)
    std_b = np.std(pb)
    if std_a < 1e-9 or std_b < 1e-9:
        return 1.0  # Both constant width = identical profile

    corr = np.corrcoef(pa, pb)[0, 1]
    if np.isnan(corr):
        return 0.0
    return float(corr)


def mask_to_shapely_polygon(mask):
    """Convert a binary mask to a Shapely polygon for geometric operations.
    Returns a Shapely Polygon/MultiPolygon or None if mask is empty."""
    if not _SHAPELY_AVAILABLE or not _SKIMAGE_AVAILABLE:
        return None
    contours = find_contours(mask.astype(float), level=0.5)
    polys = []
    for c in contours:
        if len(c) < 4:
            continue
        # Close the contour
        coords = [(float(p[1]), float(p[0])) for p in c]
        if coords[0] != coords[-1]:
            coords.append(coords[0])
        try:
            poly = ShapelyPolygon(coords)
            if poly.is_valid and poly.area > 10:
                polys.append(poly)
        except Exception:
            continue
    if not polys:
        return None
    if len(polys) == 1:
        return polys[0]
    return unary_union(polys)


def shapely_iou(mask_a, mask_b):
    """Compute IoU (Intersection over Union) using Shapely polygons.
    More geometrically accurate than pixel counting for scaled silhouettes."""
    poly_a = mask_to_shapely_polygon(mask_a)
    poly_b = mask_to_shapely_polygon(mask_b)
    if poly_a is None or poly_b is None:
        return 0.0
    try:
        inter = poly_a.intersection(poly_b).area
        union = poly_a.union(poly_b).area
        if union < 1e-9:
            return 0.0
        return inter / union
    except Exception:
        return 0.0


def shapely_hausdorff(mask_a, mask_b):
    """Hausdorff distance between silhouette outlines via Shapely.
    Normalized by the diagonal of the bounding box.
    High value = very different outlines = more distinct."""
    poly_a = mask_to_shapely_polygon(mask_a)
    poly_b = mask_to_shapely_polygon(mask_b)
    if poly_a is None or poly_b is None:
        return 0.0
    try:
        hd = poly_a.hausdorff_distance(poly_b)
        # Normalize by combined bounding box diagonal
        bounds = poly_a.union(poly_b).bounds
        diag = math.sqrt((bounds[2] - bounds[0]) ** 2 + (bounds[3] - bounds[1]) ** 2)
        if diag < 1e-9:
            return 0.0
        return hd / diag
    except Exception:
        return 0.0


def distinctiveness_score(sor, wpc, hausdorff_norm=None):
    """Combined distinctiveness: DS = 1.0 - (0.5*SOR + 0.5*max(0,WPC)).

    v2.0.0: When hausdorff_norm is provided (from Shapely), it acts as a bonus
    that can rescue borderline cases. Hausdorff > 0.15 adds up to +0.10 to DS.
    """
    wpc_clamped = max(0.0, wpc)  # Negative correlation = very distinct, treat as 0
    ds = 1.0 - (0.5 * sor + 0.5 * wpc_clamped)
    if hausdorff_norm is not None and hausdorff_norm > 0.15:
        bonus = min(0.10, (hausdorff_norm - 0.15) * 0.5)
        ds = min(1.0, ds + bonus)
    return ds


def verdict(ds):
    if ds < FAIL_THRESHOLD:
        return "FAIL"
    elif ds < WARN_THRESHOLD:
        return "WARN"
    else:
        return "PASS"


# ─── BATCH ANALYSIS ─────────────────────────────────────────────────────────


def load_character(filepath, bg_tolerance=BG_TOLERANCE):
    """Load image, extract and normalize silhouette. Returns (name, normalized_mask)."""
    img = Image.open(filepath).convert("RGB")
    bg = detect_background_color(img)
    mask = extract_silhouette(img, bg, bg_tolerance)
    norm = normalize_silhouette(mask)
    name = os.path.splitext(os.path.basename(filepath))[0]
    # Clean up common prefixes for display
    for prefix in ["LTG_CHAR_", "LTG_"]:
        if name.startswith(prefix):
            name = name[len(prefix):]
    return name, norm


def analyze_pair(name_a, mask_a, name_b, mask_b, scales=None):
    """Analyze a pair of characters at multiple scales. Returns dict of results."""
    if scales is None:
        scales = DEFAULT_SCALES

    results = {
        "pair": f"{name_a} vs {name_b}",
        "name_a": name_a,
        "name_b": name_b,
        "scales": {},
        "worst_ds": 1.0,
        "worst_scale": None,
        "verdict": "PASS",
    }

    for s in scales:
        scaled_a = scale_silhouette(mask_a, s) if s != 1.0 else mask_a
        scaled_b = scale_silhouette(mask_b, s) if s != 1.0 else mask_b

        sor = silhouette_overlap_ratio(scaled_a, scaled_b)
        wpc = width_profile_correlation(scaled_a, scaled_b)

        # Shapely metrics (when available)
        hd_norm = None
        iou = None
        if _SHAPELY_AVAILABLE and _SKIMAGE_AVAILABLE:
            padded_a, padded_b = pad_to_same_size(scaled_a, scaled_b)
            hd_norm = shapely_hausdorff(padded_a, padded_b)
            iou = shapely_iou(padded_a, padded_b)

        ds = distinctiveness_score(sor, wpc, hd_norm)
        v = verdict(ds)

        scale_key = f"{int(s * 100)}%"
        scale_result = {
            "overlap_ratio": round(sor, 4),
            "width_profile_corr": round(wpc, 4),
            "distinctiveness": round(ds, 4),
            "verdict": v,
        }
        if hd_norm is not None:
            scale_result["hausdorff_norm"] = round(hd_norm, 4)
        if iou is not None:
            scale_result["shapely_iou"] = round(iou, 4)

        results["scales"][scale_key] = scale_result

        if ds < results["worst_ds"]:
            results["worst_ds"] = round(ds, 4)
            results["worst_scale"] = scale_key
            results["verdict"] = v

    return results


def run_analysis(filepaths, scales=None, bg_tolerance=BG_TOLERANCE):
    """Run full pairwise analysis on a list of character image files."""
    if scales is None:
        scales = DEFAULT_SCALES

    characters = []
    for fp in filepaths:
        try:
            name, mask = load_character(fp, bg_tolerance)
            characters.append((name, mask, fp))
        except Exception as e:
            print(f"WARNING: Could not load {fp}: {e}", file=sys.stderr)

    if len(characters) < 2:
        return {"error": "Need at least 2 characters", "pairs": [], "characters": [c[0] for c in characters]}

    pairs = []
    for i in range(len(characters)):
        for j in range(i + 1, len(characters)):
            na, ma, _ = characters[i]
            nb, mb, _ = characters[j]
            result = analyze_pair(na, ma, nb, mb, scales)
            pairs.append(result)

    # Summary
    fail_count = sum(1 for p in pairs if p["verdict"] == "FAIL")
    warn_count = sum(1 for p in pairs if p["verdict"] == "WARN")
    pass_count = sum(1 for p in pairs if p["verdict"] == "PASS")

    overall = "PASS"
    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0:
        overall = "WARN"

    return {
        "characters": [c[0] for c in characters],
        "character_paths": {c[0]: c[2] for c in characters},
        "scales": [f"{int(s * 100)}%" for s in scales],
        "pairs": pairs,
        "summary": {
            "total_pairs": len(pairs),
            "pass": pass_count,
            "warn": warn_count,
            "fail": fail_count,
            "overall": overall,
        },
    }


# ─── CONTACT SHEET ──────────────────────────────────────────────────────────


def generate_contact_sheet(filepaths, output_path, scales=None, bg_tolerance=BG_TOLERANCE):
    """Generate a multi-scale silhouette contact sheet showing all characters at all scales."""
    if scales is None:
        scales = DEFAULT_SCALES

    characters = []
    for fp in filepaths:
        try:
            name, mask = load_character(fp, bg_tolerance)
            characters.append((name, mask))
        except Exception:
            pass

    if not characters:
        return

    n_chars = len(characters)
    n_scales = len(scales)

    cell_h = CANONICAL_HEIGHT
    cell_w = max(m.shape[1] for _, m in characters) + 20
    margin = 10
    label_h = 30

    sheet_w = margin + n_chars * (cell_w + margin)
    sheet_h = margin + n_scales * (cell_h + label_h + margin)

    # Cap to 1280px
    if sheet_w > 1280:
        scale_down = 1280 / sheet_w
        cell_w = int(cell_w * scale_down)
        cell_h = int(cell_h * scale_down)
        margin = int(margin * scale_down)
        label_h = int(label_h * scale_down)
        sheet_w = 1280
        sheet_h = margin + n_scales * (cell_h + label_h + margin)
    if sheet_h > 1280:
        sheet_h = 1280

    sheet = Image.new("RGB", (sheet_w, sheet_h), (255, 255, 255))
    draw = ImageDraw.Draw(sheet)

    for si, s in enumerate(scales):
        scale_label = f"{int(s * 100)}%"
        y_base = margin + si * (cell_h + label_h + margin)

        for ci, (name, mask) in enumerate(characters):
            x_base = margin + ci * (cell_w + margin)

            # Draw label
            draw.text((x_base + 2, y_base), f"{name} @{scale_label}", fill=(0, 0, 0))

            # Draw silhouette
            scaled = scale_silhouette(mask, s)
            sh, sw = scaled.shape
            # Center in cell
            ox = x_base + max(0, (cell_w - sw) // 2)
            oy = y_base + label_h + max(0, (cell_h - sh) // 2)

            if oy + sh <= sheet_h and ox + sw <= sheet_w:
                sil_img = Image.fromarray((1 - scaled) * 255).convert("L")
                # Paste as black silhouette on white
                for py in range(min(sh, sheet_h - oy)):
                    for px in range(min(sw, sheet_w - ox)):
                        if scaled[py, px]:
                            sheet.putpixel((ox + px, oy + py), (0, 0, 0))

    sheet.save(output_path)
    return output_path


# ─── TEXT REPORT ─────────────────────────────────────────────────────────────


def format_report(results):
    """Format results as human-readable text."""
    lines = []
    lines.append("=" * 70)
    lines.append("SILHOUETTE DISTINCTIVENESS REPORT")
    lines.append("=" * 70)
    lines.append(f"Characters: {', '.join(results.get('characters', []))}")
    lines.append(f"Scales: {', '.join(results.get('scales', []))}")
    lines.append("")

    for pair in results.get("pairs", []):
        lines.append(f"--- {pair['pair']} ---")
        lines.append(f"  Overall: {pair['verdict']} (worst DS={pair['worst_ds']:.4f} at {pair['worst_scale']})")
        for scale_key, metrics in pair["scales"].items():
            v = metrics["verdict"]
            ds = metrics["distinctiveness"]
            sor = metrics["overlap_ratio"]
            wpc = metrics["width_profile_corr"]
            flag = " <<<" if v in ("FAIL", "WARN") else ""
            lines.append(f"  {scale_key}: DS={ds:.4f} (SOR={sor:.4f}, WPC={wpc:.4f}) [{v}]{flag}")
        lines.append("")

    summary = results.get("summary", {})
    lines.append(f"SUMMARY: {summary.get('total_pairs', 0)} pairs — "
                 f"PASS={summary.get('pass', 0)} WARN={summary.get('warn', 0)} FAIL={summary.get('fail', 0)}")
    lines.append(f"OVERALL: {summary.get('overall', 'N/A')}")
    lines.append("=" * 70)
    return "\n".join(lines)


def format_markdown_report(results):
    """Format results as markdown."""
    lines = []
    lines.append("# Silhouette Distinctiveness Report")
    lines.append("")
    lines.append(f"**Characters:** {', '.join(results.get('characters', []))}")
    lines.append(f"**Scales:** {', '.join(results.get('scales', []))}")
    lines.append("")

    summary = results.get("summary", {})
    lines.append(f"**Overall: {summary.get('overall', 'N/A')}** — "
                 f"{summary.get('pass', 0)} PASS, {summary.get('warn', 0)} WARN, {summary.get('fail', 0)} FAIL "
                 f"out of {summary.get('total_pairs', 0)} pairs")
    lines.append("")

    lines.append("## Pairwise Results")
    lines.append("")
    lines.append("| Pair | Scale | DS | SOR | WPC | Verdict |")
    lines.append("|------|-------|----|-----|-----|---------|")

    for pair in results.get("pairs", []):
        for scale_key, metrics in pair["scales"].items():
            lines.append(
                f"| {pair['pair']} | {scale_key} | "
                f"{metrics['distinctiveness']:.4f} | {metrics['overlap_ratio']:.4f} | "
                f"{metrics['width_profile_corr']:.4f} | {metrics['verdict']} |"
            )

    lines.append("")
    lines.append("## Metric Definitions")
    lines.append("- **DS** (Distinctiveness Score): 1.0 = completely distinct, 0.0 = identical. DS = 1 - (0.5*SOR + 0.5*WPC)")
    lines.append("- **SOR** (Silhouette Overlap Ratio): intersection / min(area). High = similar.")
    lines.append("- **WPC** (Width Profile Correlation): Pearson r of per-row width. High = similar shape.")
    lines.append("- **Thresholds**: FAIL < 0.15, WARN < 0.30, PASS >= 0.30")
    return "\n".join(lines)


# ─── AUTO-DISCOVER ───────────────────────────────────────────────────────────


def discover_character_files(directory):
    """Find character turnaround/lineup PNGs in a directory."""
    candidates = []
    for f in sorted(os.listdir(directory)):
        if not f.lower().endswith(".png"):
            continue
        # Prefer turnaround front views or standalone character images
        fp = os.path.join(directory, f)
        candidates.append(fp)
    return candidates


# ─── CLI ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Character Silhouette Distinctiveness Tool")
    parser.add_argument("inputs", nargs="+", help="Character image files or directories")
    parser.add_argument("--scales", default="1.0,0.5,0.25", help="Comma-separated scale factors")
    parser.add_argument("--bg-tolerance", type=int, default=BG_TOLERANCE)
    parser.add_argument("--output", help="Output contact sheet PNG path")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--report", help="Write markdown report to file")
    args = parser.parse_args()

    scales = [float(s.strip()) for s in args.scales.split(",")]

    # Collect files
    filepaths = []
    for inp in args.inputs:
        if os.path.isdir(inp):
            filepaths.extend(discover_character_files(inp))
        elif os.path.isfile(inp):
            filepaths.append(inp)
        else:
            print(f"WARNING: {inp} not found, skipping", file=sys.stderr)

    if len(filepaths) < 2:
        print("ERROR: Need at least 2 character images.", file=sys.stderr)
        sys.exit(1)

    results = run_analysis(filepaths, scales, args.bg_tolerance)

    if args.json:
        # Remove non-serializable items
        out = {k: v for k, v in results.items() if k != "character_paths"}
        print(json.dumps(out, indent=2))
    else:
        print(format_report(results))

    if args.output:
        generate_contact_sheet(filepaths, args.output, scales, args.bg_tolerance)
        print(f"\nContact sheet saved: {args.output}")

    if args.report:
        md = format_markdown_report(results)
        os.makedirs(os.path.dirname(args.report) or ".", exist_ok=True)
        with open(args.report, "w") as f:
            f.write(md)
        print(f"Report saved: {args.report}")

    # Exit code based on overall verdict
    overall = results.get("summary", {}).get("overall", "PASS")
    if overall == "FAIL":
        sys.exit(2)
    elif overall == "WARN":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
