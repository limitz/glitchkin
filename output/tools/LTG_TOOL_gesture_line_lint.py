#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_gesture_line_lint.py — v1.0.0 (Cycle 51, Lee Tanaka)

Automated gesture line straightness detector for expression sheets and
single-character renders.

Given an expression sheet PNG (or single character PNG), this tool:
  1. Detects panel grid (expression sheet) or treats whole image as one panel
  2. For each panel, extracts the character silhouette (largest non-BG region)
  3. Computes centroid at 4 vertical levels (head, shoulder, hip, foot)
  4. Fits a bezier curve through the 4 centroids
  5. Measures max deviation from a straight vertical line
  6. Grades: FAIL (<= 3px), WARN (3-8px), PASS (> 8px)

Uses bezier library (via LTG_TOOL_curve_utils) for curvature analysis when
available; falls back to simple deviation measurement otherwise.

CLI usage:
  python3 LTG_TOOL_gesture_line_lint.py <image.png>
  python3 LTG_TOOL_gesture_line_lint.py <image.png> --single    # single character, not grid
  python3 LTG_TOOL_gesture_line_lint.py --self-test             # synthetic validation
  python3 LTG_TOOL_gesture_line_lint.py --batch f1.png f2.png   # multiple files

Module API:
  from LTG_TOOL_gesture_line_lint import lint_gesture_line, lint_expression_sheet

Output:
  - Console: per-panel PASS/WARN/FAIL with deviation values
  - PNG: annotated overlay showing gesture lines (saved as LTG_SNAP_gesture_lint_<name>.png)

Dependencies: Pillow, NumPy. Optional: bezier (via LTG_TOOL_curve_utils), Shapely.
"""

import argparse
import math
import os
import sys
from typing import Dict, List, Optional, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ─── Path setup ────────────────────────────────────────────────────────────
_TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_TOOL_DIR, "..", ".."))
if _TOOL_DIR not in sys.path:
    sys.path.insert(0, _TOOL_DIR)

# ─── Optional imports from curve_utils ─────────────────────────────────────
_CURVE_UTILS_AVAILABLE = False
try:
    from LTG_TOOL_curve_utils import (
        curvature_at_t,
        arc_length,
        make_curve,
        BEZIER_AVAILABLE,
    )
    _CURVE_UTILS_AVAILABLE = BEZIER_AVAILABLE
except ImportError:
    pass

# ─── Constants ─────────────────────────────────────────────────────────────
# Vertical level fractions for centroid sampling (0.0 = top, 1.0 = bottom)
HEAD_FRAC = 0.10      # top 10% of bounding box
SHOULDER_FRAC = 0.25   # 25% down
HIP_FRAC = 0.60       # 60% down
FOOT_FRAC = 0.90      # bottom 10%

# Grading thresholds (max deviation from vertical in pixels)
FAIL_THRESHOLD = 3.0   # <= 3px = straight = FAIL
WARN_THRESHOLD = 8.0   # 3-8px = mild curve = WARN
# > 8px = readable gesture = PASS

# Colors for annotation
GESTURE_PASS = (60, 180, 80, 200)      # green
GESTURE_WARN = (255, 180, 40, 200)     # amber
GESTURE_FAIL = (220, 50, 40, 200)      # red
VERTICAL_REF = (180, 180, 180, 120)    # ghost gray
CENTROID_DOT = (255, 255, 255, 255)    # white
BG_TOLERANCE = 30  # max per-channel diff from corner color to count as BG


# ═══════════════════════════════════════════════════════════════════════════
#  SECTION 1: Silhouette extraction
# ═══════════════════════════════════════════════════════════════════════════

def _detect_bg_color(img_arr):
    """Detect background color from corner pixels."""
    h, w = img_arr.shape[:2]
    corners = [
        img_arr[0, 0],
        img_arr[0, w - 1],
        img_arr[h - 1, 0],
        img_arr[h - 1, w - 1],
    ]
    # Use median of corners (robust to one corner being on the character)
    return np.median(corners, axis=0).astype(np.uint8)


def _extract_silhouette_mask(img_arr, bg_color=None):
    """Create a binary mask: 1 = character, 0 = background.

    Uses per-channel distance from bg_color with BG_TOLERANCE threshold.
    """
    if bg_color is None:
        bg_color = _detect_bg_color(img_arr)
    # Work with RGB only (drop alpha if present)
    rgb = img_arr[:, :, :3] if img_arr.ndim == 3 else img_arr
    bg = bg_color[:3] if len(bg_color) >= 3 else bg_color

    diff = np.abs(rgb.astype(np.int16) - bg.astype(np.int16))
    max_diff = np.max(diff, axis=2)
    mask = (max_diff > BG_TOLERANCE).astype(np.uint8)
    return mask


def _bounding_box(mask):
    """Get tight bounding box of foreground pixels. Returns (x0, y0, x1, y1) or None."""
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not np.any(rows):
        return None
    y0, y1 = np.where(rows)[0][[0, -1]]
    x0, x1 = np.where(cols)[0][[0, -1]]
    return (int(x0), int(y0), int(x1), int(y1))


def _centroid_at_level(mask, y_frac, bbox):
    """Compute x-centroid of foreground pixels at a vertical level.

    y_frac: 0.0 = top of bbox, 1.0 = bottom of bbox.
    Returns (cx, cy) or None if no foreground at that level.
    """
    x0, y0, x1, y1 = bbox
    h = y1 - y0
    if h < 4:
        return None

    # Sample a band of pixels (5% of bbox height, min 2px)
    band_h = max(2, int(h * 0.05))
    center_y = int(y0 + y_frac * h)
    band_top = max(y0, center_y - band_h // 2)
    band_bot = min(y1, band_top + band_h)

    band = mask[band_top:band_bot, :]
    fg_cols = np.where(np.any(band, axis=0))[0]
    if len(fg_cols) == 0:
        return None

    # Weighted centroid (by pixel count per column)
    col_counts = band.sum(axis=0)
    total = col_counts.sum()
    if total == 0:
        return None
    cx = np.sum(np.arange(mask.shape[1]) * col_counts) / total
    cy = (band_top + band_bot) / 2.0
    return (float(cx), float(cy))


# ═══════════════════════════════════════════════════════════════════════════
#  SECTION 2: Gesture line measurement
# ═══════════════════════════════════════════════════════════════════════════

def _measure_deviation(centroids):
    """Measure max deviation of centroids from a straight vertical line.

    The reference line connects the head centroid to the foot centroid.
    Returns max perpendicular distance from this line across all 4 points.
    """
    if len(centroids) < 2:
        return 0.0

    # Reference: straight line from first to last centroid
    p0 = centroids[0]
    p1 = centroids[-1]
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    line_len = math.sqrt(dx * dx + dy * dy)
    if line_len < 1e-6:
        return 0.0

    max_dev = 0.0
    for pt in centroids[1:-1]:
        # Perpendicular distance from point to line
        # |cross product| / |line direction|
        cross = abs((pt[0] - p0[0]) * dy - (pt[1] - p0[1]) * dx)
        dist = cross / line_len
        if dist > max_dev:
            max_dev = dist

    return max_dev


def _measure_curvature(centroids):
    """Measure curvature using bezier library if available.

    Returns (max_curvature, arc_len, deviation) or None if bezier unavailable.
    """
    if not _CURVE_UTILS_AVAILABLE or len(centroids) < 3:
        return None

    try:
        # Fit a cubic bezier through the 4 centroids
        # Use centroids as control points for a cubic curve
        if len(centroids) == 4:
            cp = centroids
        else:
            # Pad to 4 points by interpolation
            cp = list(centroids)
            while len(cp) < 4:
                mid = ((cp[-2][0] + cp[-1][0]) / 2, (cp[-2][1] + cp[-1][1]) / 2)
                cp.insert(-1, mid)

        curve_len = arc_length(cp)

        # Sample curvature at multiple points
        max_k = 0.0
        for t in [0.2, 0.35, 0.5, 0.65, 0.8]:
            k = curvature_at_t(cp, t)
            if k > max_k:
                max_k = k

        # Deviation
        dev = _measure_deviation(centroids)

        return (max_k, curve_len, dev)
    except Exception:
        return None


def _grade(deviation, scale_factor=1.0):
    """Grade a gesture line deviation.

    scale_factor: adjusts thresholds for image size. Default thresholds
    are calibrated for ~400px tall characters. For larger images, increase.
    """
    fail_t = FAIL_THRESHOLD * scale_factor
    warn_t = WARN_THRESHOLD * scale_factor
    if deviation <= fail_t:
        return "FAIL"
    elif deviation <= warn_t:
        return "WARN"
    else:
        return "PASS"


# ═══════════════════════════════════════════════════════════════════════════
#  SECTION 3: Grid detection (expression sheet panels)
# ═══════════════════════════════════════════════════════════════════════════

def _detect_grid(img_arr):
    """Detect panel grid in an expression sheet by finding separator lines.

    Returns list of (x0, y0, x1, y1) bounding boxes for each panel cell.
    If no grid detected, returns [(0, 0, w, h)] (single panel).
    """
    h, w = img_arr.shape[:2]
    bg = _detect_bg_color(img_arr)

    # Detect horizontal separator rows (rows where >90% of pixels match BG)
    rgb = img_arr[:, :, :3] if img_arr.ndim == 3 else img_arr
    row_bg_frac = np.zeros(h)
    for y in range(h):
        diff = np.abs(rgb[y].astype(np.int16) - bg[:3].astype(np.int16))
        max_diff = np.max(diff, axis=1)
        row_bg_frac[y] = np.mean(max_diff < BG_TOLERANCE)

    # Detect vertical separator columns
    col_bg_frac = np.zeros(w)
    for x in range(w):
        diff = np.abs(rgb[:, x].astype(np.int16) - bg[:3].astype(np.int16))
        max_diff = np.max(diff, axis=1)
        col_bg_frac[x] = np.mean(max_diff < BG_TOLERANCE)

    # Find separator bands (>85% BG, at least 3px wide)
    def _find_separators(bg_frac, min_width=3, threshold=0.85):
        separators = []
        in_sep = False
        start = 0
        for i in range(len(bg_frac)):
            if bg_frac[i] >= threshold:
                if not in_sep:
                    in_sep = True
                    start = i
            else:
                if in_sep:
                    if i - start >= min_width:
                        separators.append((start, i))
                    in_sep = False
        if in_sep and len(bg_frac) - start >= min_width:
            separators.append((start, len(bg_frac)))
        return separators

    h_seps = _find_separators(row_bg_frac)
    v_seps = _find_separators(col_bg_frac)

    # Build grid cells from separators
    # Add image edges as implicit separators
    y_boundaries = [0]
    for s, e in h_seps:
        mid = (s + e) // 2
        if mid > y_boundaries[-1] + 20:  # min cell height 20px
            y_boundaries.append(mid)
    if y_boundaries[-1] < h - 20:
        y_boundaries.append(h)

    x_boundaries = [0]
    for s, e in v_seps:
        mid = (s + e) // 2
        if mid > x_boundaries[-1] + 20:
            x_boundaries.append(mid)
    if x_boundaries[-1] < w - 20:
        x_boundaries.append(w)

    # If we got a useful grid (at least 2x1 or 1x2)
    if len(y_boundaries) < 2 or len(x_boundaries) < 2:
        return [(0, 0, w, h)]

    cells = []
    for r in range(len(y_boundaries) - 1):
        for c in range(len(x_boundaries) - 1):
            x0 = x_boundaries[c]
            y0 = y_boundaries[r]
            x1 = x_boundaries[c + 1]
            y1 = y_boundaries[r + 1]
            # Only include cells that are big enough to contain a character
            if (x1 - x0) > 40 and (y1 - y0) > 40:
                cells.append((x0, y0, x1, y1))

    return cells if cells else [(0, 0, w, h)]


# ═══════════════════════════════════════════════════════════════════════════
#  SECTION 4: Main lint functions
# ═══════════════════════════════════════════════════════════════════════════

def lint_gesture_line(img_arr, label="panel"):
    """Lint gesture line for a single character image.

    Args:
        img_arr: numpy array (H, W, 3 or 4)
        label: identifier for reporting

    Returns:
        dict with keys: label, grade, deviation, centroids, bbox, curvature_info
    """
    mask = _extract_silhouette_mask(img_arr)
    bbox = _bounding_box(mask)
    if bbox is None:
        return {
            "label": label,
            "grade": "SKIP",
            "deviation": 0.0,
            "centroids": [],
            "bbox": None,
            "curvature_info": None,
            "reason": "No foreground pixels detected",
        }

    x0, y0, x1, y1 = bbox
    char_h = y1 - y0
    if char_h < 20:
        return {
            "label": label,
            "grade": "SKIP",
            "deviation": 0.0,
            "centroids": [],
            "bbox": bbox,
            "curvature_info": None,
            "reason": "Character too small (height < 20px)",
        }

    # Extract centroids at 4 levels
    centroids = []
    for frac in [HEAD_FRAC, SHOULDER_FRAC, HIP_FRAC, FOOT_FRAC]:
        c = _centroid_at_level(mask, frac, bbox)
        if c is not None:
            centroids.append(c)

    if len(centroids) < 3:
        return {
            "label": label,
            "grade": "SKIP",
            "deviation": 0.0,
            "centroids": centroids,
            "bbox": bbox,
            "curvature_info": None,
            "reason": "Insufficient centroid points (need >= 3, got %d)" % len(centroids),
        }

    # Scale factor: thresholds calibrated for ~400px character height
    scale = char_h / 400.0

    deviation = _measure_deviation(centroids)
    grade = _grade(deviation, scale_factor=scale)
    curvature_info = _measure_curvature(centroids)

    return {
        "label": label,
        "grade": grade,
        "deviation": round(deviation, 2),
        "centroids": centroids,
        "bbox": bbox,
        "curvature_info": curvature_info,
        "char_height": char_h,
        "scale_factor": round(scale, 3),
    }


def lint_expression_sheet(path, single=False):
    """Lint an expression sheet or single character image.

    Args:
        path: path to PNG file
        single: if True, treat whole image as one panel (skip grid detection)

    Returns:
        list of per-panel result dicts from lint_gesture_line
    """
    img = Image.open(path).convert("RGBA")
    img_arr = np.array(img)

    if single:
        cells = [(0, 0, img.width, img.height)]
    else:
        cells = _detect_grid(img_arr)

    results = []
    for i, (x0, y0, x1, y1) in enumerate(cells):
        cell_arr = img_arr[y0:y1, x0:x1]
        label = "P%d" % (i + 1) if len(cells) > 1 else os.path.basename(path)
        result = lint_gesture_line(cell_arr, label=label)
        result["cell_bbox"] = (x0, y0, x1, y1)
        results.append(result)

    return results


# ═══════════════════════════════════════════════════════════════════════════
#  SECTION 5: Annotation overlay
# ═══════════════════════════════════════════════════════════════════════════

def _draw_annotation(img, results):
    """Draw gesture line annotations on the image.

    Returns annotated PIL Image.
    """
    overlay = img.copy().convert("RGBA")
    ann = Image.new("RGBA", overlay.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(ann)

    for r in results:
        if r["grade"] == "SKIP" or not r["centroids"]:
            continue

        cell = r.get("cell_bbox", (0, 0, img.width, img.height))
        cx0, cy0 = cell[0], cell[1]
        centroids = r["centroids"]

        # Offset centroids to image coordinates
        pts = [(c[0] + cx0, c[1] + cy0) for c in centroids]

        # Draw vertical reference line (head to foot, straight)
        if len(pts) >= 2:
            ref_x = pts[0][0]
            draw.line(
                [(ref_x, pts[0][1]), (ref_x, pts[-1][1])],
                fill=VERTICAL_REF,
                width=1,
            )

        # Draw gesture line
        grade_color = {
            "PASS": GESTURE_PASS,
            "WARN": GESTURE_WARN,
            "FAIL": GESTURE_FAIL,
        }.get(r["grade"], GESTURE_FAIL)

        for i in range(len(pts) - 1):
            draw.line(
                [pts[i], pts[i + 1]],
                fill=grade_color,
                width=3,
            )

        # Draw centroid dots
        for pt in pts:
            x, y = int(pt[0]), int(pt[1])
            draw.ellipse(
                [x - 3, y - 3, x + 3, y + 3],
                fill=CENTROID_DOT,
                outline=grade_color,
            )

        # Draw grade label
        label_text = "%s: %s (dev=%.1fpx)" % (r["label"], r["grade"], r["deviation"])
        lx = cx0 + 4
        ly = cy0 + 4
        draw.rectangle([lx - 1, ly - 1, lx + len(label_text) * 7 + 4, ly + 14], fill=(0, 0, 0, 160))
        draw.text((lx + 2, ly), label_text, fill=(255, 255, 255, 255))

    result = Image.alpha_composite(overlay, ann)
    return result


# ═══════════════════════════════════════════════════════════════════════════
#  SECTION 6: Self-test (synthetic validation)
# ═══════════════════════════════════════════════════════════════════════════

def _run_self_test():
    """Generate synthetic test cases and validate PASS/WARN/FAIL grading."""
    print("=== GESTURE LINE LINT — SELF-TEST ===\n")
    results = []

    # Test 1: Straight vertical character (FAIL expected)
    img1 = Image.new("RGB", (200, 500), (230, 230, 230))
    d1 = ImageDraw.Draw(img1)
    # Straight vertical rectangle
    cx = 100
    d1.ellipse([cx - 20, 30, cx + 20, 70], fill=(200, 136, 90))  # head
    d1.rectangle([cx - 25, 70, cx + 25, 250], fill=(150, 175, 200))  # torso
    d1.rectangle([cx - 15, 250, cx - 2, 420], fill=(42, 40, 80))  # leg L
    d1.rectangle([cx + 2, 250, cx + 15, 420], fill=(42, 40, 80))  # leg R
    d1.ellipse([cx - 15, 420, cx - 2, 440], fill=(60, 45, 35))  # foot L
    d1.ellipse([cx + 2, 420, cx + 15, 440], fill=(60, 45, 35))  # foot R

    r1 = lint_gesture_line(np.array(img1), label="TEST_STRAIGHT")
    expected1 = "FAIL"
    actual1 = r1["grade"]
    status1 = "PASS" if actual1 == expected1 else "FAIL"
    print("Test 1 (straight vertical): expected=%s, got=%s, dev=%.2f → %s" % (
        expected1, actual1, r1["deviation"], status1))
    results.append(status1 == "PASS")

    # Test 2: Strong S-curve character (PASS expected)
    img2 = Image.new("RGB", (200, 500), (230, 230, 230))
    d2 = ImageDraw.Draw(img2)
    # Head offset right
    d2.ellipse([120, 30, 160, 70], fill=(200, 136, 90))
    # Torso offset left
    d2.rectangle([70, 70, 120, 250], fill=(150, 175, 200))
    # Hips shifted right
    d2.rectangle([100, 250, 140, 300], fill=(150, 175, 200))
    # Legs under hips
    d2.rectangle([105, 300, 118, 420], fill=(42, 40, 80))
    d2.rectangle([122, 300, 135, 420], fill=(42, 40, 80))
    d2.ellipse([105, 420, 118, 440], fill=(60, 45, 35))
    d2.ellipse([122, 420, 135, 440], fill=(60, 45, 35))

    r2 = lint_gesture_line(np.array(img2), label="TEST_S_CURVE")
    expected2 = "PASS"
    actual2 = r2["grade"]
    status2 = "PASS" if actual2 == expected2 else "FAIL"
    print("Test 2 (S-curve): expected=%s, got=%s, dev=%.2f → %s" % (
        expected2, actual2, r2["deviation"], status2))
    results.append(status2 == "PASS")

    # Test 3: Mild lean (WARN expected)
    img3 = Image.new("RGB", (200, 500), (230, 230, 230))
    d3 = ImageDraw.Draw(img3)
    # Slight lean: head 5px right of center
    d3.ellipse([105, 30, 145, 70], fill=(200, 136, 90))  # head slightly right
    d3.rectangle([90, 70, 140, 250], fill=(150, 175, 200))  # torso slightly right
    d3.rectangle([88, 250, 101, 420], fill=(42, 40, 80))
    d3.rectangle([104, 250, 117, 420], fill=(42, 40, 80))
    d3.ellipse([88, 420, 101, 440], fill=(60, 45, 35))
    d3.ellipse([104, 420, 117, 440], fill=(60, 45, 35))

    r3 = lint_gesture_line(np.array(img3), label="TEST_MILD_LEAN")
    # WARN or PASS both acceptable for mild offset
    expected3_options = ["WARN", "PASS"]
    actual3 = r3["grade"]
    status3 = "PASS" if actual3 in expected3_options else "FAIL"
    print("Test 3 (mild lean): expected=%s, got=%s, dev=%.2f → %s" % (
        "/".join(expected3_options), actual3, r3["deviation"], status3))
    results.append(status3 == "PASS")

    # Test 4: Empty image (SKIP expected)
    img4 = Image.new("RGB", (200, 500), (230, 230, 230))
    r4 = lint_gesture_line(np.array(img4), label="TEST_EMPTY")
    expected4 = "SKIP"
    actual4 = r4["grade"]
    status4 = "PASS" if actual4 == expected4 else "FAIL"
    print("Test 4 (empty): expected=%s, got=%s → %s" % (expected4, actual4, status4))
    results.append(status4 == "PASS")

    # Summary
    print("\n--- Self-test: %d/%d PASS ---" % (sum(results), len(results)))
    all_pass = all(results)
    if all_pass:
        print("ALL SELF-TESTS PASSED.")
    else:
        print("SOME SELF-TESTS FAILED.")
    return all_pass


# ═══════════════════════════════════════════════════════════════════════════
#  SECTION 7: CLI
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Gesture line straightness linter for expression sheets")
    parser.add_argument("images", nargs="*", help="PNG file(s) to lint")
    parser.add_argument("--single", action="store_true",
                        help="Treat image as single character (skip grid detection)")
    parser.add_argument("--self-test", action="store_true",
                        help="Run synthetic self-test")
    parser.add_argument("--batch", action="store_true",
                        help="Batch mode: lint multiple files")
    parser.add_argument("--no-overlay", action="store_true",
                        help="Skip annotation overlay PNG generation")
    parser.add_argument("--output-dir", type=str, default=None,
                        help="Directory for overlay PNGs (default: output/production/)")
    args = parser.parse_args()

    if args.self_test:
        success = _run_self_test()
        sys.exit(0 if success else 1)

    if not args.images:
        parser.error("No images specified. Use --self-test or provide PNG files.")

    output_dir = args.output_dir or os.path.join(_PROJECT_ROOT, "output", "production")
    os.makedirs(output_dir, exist_ok=True)

    all_results = []
    for path in args.images:
        if not os.path.exists(path):
            print("WARNING: %s not found, skipping." % path)
            continue

        print("\n=== %s ===" % os.path.basename(path))
        results = lint_expression_sheet(path, single=args.single)

        for r in results:
            grade = r["grade"]
            dev = r.get("deviation", 0.0)
            label = r["label"]
            ci = r.get("curvature_info")

            if grade == "SKIP":
                print("  %s: SKIP — %s" % (label, r.get("reason", "unknown")))
            else:
                curvature_str = ""
                if ci:
                    curvature_str = " | max_curvature=%.4f, arc_len=%.1f" % (ci[0], ci[1])
                scale_str = ""
                if "scale_factor" in r:
                    scale_str = " | scale=%.2f" % r["scale_factor"]
                print("  %s: %s (deviation=%.2fpx%s%s)" % (
                    label, grade, dev, scale_str, curvature_str))

        all_results.extend(results)

        # Generate overlay
        if not args.no_overlay:
            try:
                img = Image.open(path).convert("RGBA")
                annotated = _draw_annotation(img, results)
                base = os.path.splitext(os.path.basename(path))[0]
                out_path = os.path.join(output_dir, "LTG_SNAP_gesture_lint_%s.png" % base)
                annotated.save(out_path)
                print("  Overlay saved: %s" % out_path)
            except Exception as e:
                print("  WARNING: Could not save overlay: %s" % e)

    # Summary
    grades = [r["grade"] for r in all_results if r["grade"] != "SKIP"]
    if grades:
        n_pass = grades.count("PASS")
        n_warn = grades.count("WARN")
        n_fail = grades.count("FAIL")
        print("\n--- SUMMARY: %d PASS / %d WARN / %d FAIL ---" % (n_pass, n_warn, n_fail))
        if n_fail > 0:
            sys.exit(1)
        elif n_warn > 0:
            sys.exit(0)  # WARN is not blocking
        else:
            sys.exit(0)
    else:
        print("\n--- No panels to lint (all SKIP). ---")
        sys.exit(0)


if __name__ == "__main__":
    main()
