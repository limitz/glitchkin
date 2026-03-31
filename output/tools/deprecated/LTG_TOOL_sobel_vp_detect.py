#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sobel_vp_detect.py
Sobel Vanishing Point Detector — "Luma & the Glitchkin"
Author: Kai Nakamura / Cycle 42
Brief: members/kai_nakamura/inbox/20260330_2300_producer_c42_brief.md

Uses Sobel edge detection + Hough probabilistic line transform (or numpy fallback) to
estimate the dominant vanishing point (VP) in an environment background image. Outputs
VP_X, VP_Y in pixel coordinates and a confidence score (0.0–1.0).

Accepts optional expected VP coordinates for direct QA comparison, emitting
PASS / WARN / FAIL based on the distance between detected and expected VP.

Algorithm
---------
1. Load image → grayscale numpy array (downscale to ≤640px for speed)
2. Gaussian blur (5×5, sigma=1.5) to suppress noise
3. Compute Sobel gradients in X and Y (cv2 or numpy fallback)
4. Apply Canny edge detection threshold (cv2) or magnitude threshold (fallback)
5. Detect line segments via HoughLinesP (cv2) or skeleton approach (fallback)
6. For each pair of non-parallel line segments, compute the intersection point
7. Cluster intersection points using a 2D histogram (grid cells ~5% of image size)
8. The dominant cluster peak → estimated VP_X, VP_Y
9. Confidence = (peak_cluster_votes / total_line_pairs) clamped to [0.0, 1.0]
   Threshold: confidence ≥ 0.15 → VP is "detected" (VP001 PASS)
10. If --vp-x-expected and --vp-y-expected are given:
    distance = sqrt((VP_X - expected_X)² + (VP_Y - expected_Y)²)
    PASS  if distance ≤ tolerance_px (default 80px)
    WARN  if distance ≤ 2 × tolerance_px
    FAIL  if distance > 2 × tolerance_px
    Also FAIL if VP001 fails (no VP detected)

Checks
------
VP001  Vanishing point detected
       FAIL  — no dominant VP found (confidence < 0.15 or fewer than 4 line segments)
       PASS  — dominant VP cluster found
VP002  VP matches expected position (only when --vp-x-expected / --vp-y-expected given)
       PASS  — VP within tolerance_px of expected
       WARN  — VP within 2 × tolerance_px of expected
       FAIL  — VP further than 2 × tolerance_px from expected, or VP001 failed

Known-spec VP positions (Real World environments)
--------------------------------------------------
  Kitchen:       VP_X=960 VP_Y=540  (centred, old 1920×1080)
  Classroom:     VP_X=192 VP_Y=230  (3/4 back-right, 1280×720)
  School Hallway: VP_X=640 VP_Y=160 (3-point, low camera)
  Tech Den:      VP_X=960 VP_Y=360  (approximately centred)
  Main Street:   VP_X=640 VP_Y=270  (two-point, street)
  SF01/SF04:     VP_X=640 VP_Y=360  (kitchen centred)
  SF02:          VP_X=640 VP_Y=310  (street, dutch-tilted)
(These are approximate reference values; pass --vp-x-expected / --vp-y-expected at runtime.)

Usage
-----
    # Detect only (no comparison)
    python LTG_TOOL_sobel_vp_detect.py LTG_ENV_classroom_bg.png

    # With expected VP comparison
    python LTG_TOOL_sobel_vp_detect.py LTG_ENV_classroom_bg.png \\
        --vp-x-expected 192 --vp-y-expected 230

    # Custom tolerance
    python LTG_TOOL_sobel_vp_detect.py LTG_ENV_classroom_bg.png \\
        --vp-x-expected 192 --vp-y-expected 230 --tolerance 120

    # Batch directory scan
    python LTG_TOOL_sobel_vp_detect.py output/backgrounds/ \\
        --save-report output/tools/sobel_vp_report.txt

    # Batch with auto VP-spec lookup (v1.1.0+)
    python LTG_TOOL_sobel_vp_detect.py output/backgrounds/environments/ \\
        --vp-config output/tools/vp_spec_config.json \\
        --save-report output/tools/sobel_vp_report.txt

    # Debug: save annotated VP image
    python LTG_TOOL_sobel_vp_detect.py LTG_ENV_classroom_bg.png --debug-png vp_debug.png

API
---
    from LTG_TOOL_sobel_vp_detect import (detect_vp, detect_vp_batch, format_report,
        load_vp_config, lookup_vp_spec, detect_vp_batch_with_config)

    result = detect_vp("LTG_ENV_classroom_bg.png",
                       vp_x_expected=192, vp_y_expected=230, tolerance_px=80)
    # result keys: file, vp_x, vp_y, confidence, grade, issues,
    #              vp_x_expected, vp_y_expected, distance_px, tolerance_px,
    #              image_width, image_height, skipped_reason

    results = detect_vp_batch("output/backgrounds/",
                               vp_x_expected=None, vp_y_expected=None)
    print(format_report(results))

Changelog
---------
v1.1.0 (C44): Added vp_spec_config.json support.
    load_vp_config(config_path) — load and index the JSON config by output_filename.
    lookup_vp_spec(config, image_path) — auto-resolve VP_X/VP_Y/tolerance for a given image.
    detect_vp_batch_with_config(directory, config_path) — batch using per-file VP specs.
    CLI: --vp-config PATH flag auto-fills --vp-x-expected/--vp-y-expected per file in batch mode.
    Known-spec comment updated to refer to vp_spec_config.json as canonical source.
v1.0.0 (C42): Initial implementation.
    Sobel → Canny → HoughLinesP → pairwise intersection clustering.
    cv2 required for Hough; numpy-only fallback uses angle histogram + gradient centroid.
    --vp-x-expected / --vp-y-expected / --tolerance flags.
    --debug-png for annotated output.
    Full API: detect_vp(), detect_vp_batch(), format_report().

Dependencies
------------
    numpy  — required
    cv2 (OpenCV) — strongly recommended; numpy fallback available but less accurate
    Pillow — for image loading and debug-PNG output
"""

__version__ = "1.1.0"

import os
import sys
import math
import json
import glob as _glob
from collections import defaultdict

try:
    import numpy as np
    _NP_AVAILABLE = True
except ImportError:
    np = None
    _NP_AVAILABLE = False

try:
    import cv2
    _CV2_AVAILABLE = True
except ImportError:
    cv2 = None
    _CV2_AVAILABLE = False

from PIL import Image, ImageDraw


# ── Constants ─────────────────────────────────────────────────────────────────

_DETECT_SIZE = 640          # downscale target for analysis (px)
_MIN_CONFIDENCE = 0.15      # VP001 PASS threshold
_MIN_LINE_SEGMENTS = 4      # VP001 requires at least this many lines found
_DEFAULT_TOLERANCE_PX = 80  # PASS/WARN/FAIL threshold (before coordinate rescale)

# Hough parameters
_HOUGH_RHO = 1
_HOUGH_THETA = math.pi / 180.0
_HOUGH_THRESHOLD = 30
_HOUGH_MIN_LINE_LENGTH = 40
_HOUGH_MAX_LINE_GAP = 10

# Intersection clustering: grid cell size as fraction of image dimension
_GRID_CELL_FRACTION = 0.05


# ── Image loading + preprocessing ─────────────────────────────────────────────

def _load_gray(image_path):
    """
    Load image, downscale to ≤_DETECT_SIZE px, return (gray_np_uint8, scale_x, scale_y).
    scale_x / scale_y: factor to multiply analysis coords back to original pixels.
    Returns (None, 1, 1) on failure.
    """
    if not _NP_AVAILABLE:
        return None, 1.0, 1.0
    try:
        pil_img = Image.open(image_path).convert("L")
        orig_w, orig_h = pil_img.size
        pil_img.thumbnail((_DETECT_SIZE, _DETECT_SIZE), Image.LANCZOS)
        small_w, small_h = pil_img.size
        gray_np = np.array(pil_img, dtype=np.uint8)
        scale_x = orig_w / small_w
        scale_y = orig_h / small_h
        return gray_np, scale_x, scale_y
    except Exception:
        return None, 1.0, 1.0


# ── Hough-based line detection (cv2 path) ────────────────────────────────────

def _detect_lines_hough(gray_np):
    """
    Apply Canny + HoughLinesP. Returns list of (x1, y1, x2, y2) tuples in analysis coords.
    Requires cv2.
    """
    blurred = cv2.GaussianBlur(gray_np, (5, 5), 1.5)
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(
        edges,
        rho=_HOUGH_RHO,
        theta=_HOUGH_THETA,
        threshold=_HOUGH_THRESHOLD,
        minLineLength=_HOUGH_MIN_LINE_LENGTH,
        maxLineGap=_HOUGH_MAX_LINE_GAP,
    )
    if lines is None:
        return []
    result = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        result.append((int(x1), int(y1), int(x2), int(y2)))
    return result


def _detect_lines_numpy_fallback(gray_np):
    """
    Numpy-only fallback: Sobel gradient → magnitude threshold → extract strong edge pixels.
    Builds a synthetic set of 'line segments' by grouping high-magnitude edge pixels by
    dominant gradient angle. Less accurate than Hough but usable for detection.
    Returns list of (x1, y1, x2, y2) approximate segments.
    """
    # Sobel gradients
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
    ky = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float64)
    gray_f = gray_np.astype(np.float64)
    h, w = gray_f.shape

    padded = np.pad(gray_f, 1, mode='edge')
    Gx = np.zeros((h, w), dtype=np.float64)
    Gy = np.zeros((h, w), dtype=np.float64)
    for kr in range(3):
        for kc in range(3):
            Gx += kx[kr, kc] * padded[kr:kr + h, kc:kc + w]
            Gy += ky[kr, kc] * padded[kr:kr + h, kc:kc + w]

    mag = np.sqrt(Gx ** 2 + Gy ** 2)
    threshold = mag.max() * 0.25
    ys, xs = np.where(mag > threshold)

    if len(xs) == 0:
        return []

    # Angle for each edge pixel (perpendicular direction: line direction = angle + 90°)
    angles = np.degrees(np.arctan2(Gy[ys, xs], Gx[ys, xs])) % 180.0

    # Group pixels into 12 angle bins (15° each). Each group becomes one synthetic segment.
    segments = []
    n_bins = 12
    for b in range(n_bins):
        lo = b * 15.0
        hi = lo + 15.0
        mask = (angles >= lo) & (angles < hi)
        if mask.sum() < 5:
            continue
        bxs = xs[mask]
        bys = ys[mask]
        # Segment from centroid-left to centroid-right
        cx = int(bxs.mean())
        cy = int(bys.mean())
        std_x = max(1, int(bxs.std()))
        std_y = max(1, int(bys.std()))
        angle_rad = math.radians((lo + hi) / 2.0)
        dx = int(std_x * math.cos(angle_rad))
        dy = int(std_y * math.sin(angle_rad))
        segments.append((cx - dx, cy - dy, cx + dx, cy + dy))

    return segments


# ── Intersection computation ──────────────────────────────────────────────────

def _line_intersection(seg1, seg2):
    """
    Compute the intersection of two line segments (treated as infinite lines).
    Returns (x, y) or None if lines are parallel / near-parallel.
    """
    x1, y1, x2, y2 = seg1
    x3, y3, x4, y4 = seg2

    dx1 = x2 - x1
    dy1 = y2 - y1
    dx2 = x4 - x3
    dy2 = y4 - y3

    denom = dx1 * dy2 - dy1 * dx2
    if abs(denom) < 1e-6:
        return None  # parallel

    t = ((x3 - x1) * dy2 - (y3 - y1) * dx2) / denom

    ix = x1 + t * dx1
    iy = y1 + t * dy1
    return (ix, iy)


def _segment_angle_deg(seg):
    """Return the angle of a segment in degrees [0, 180)."""
    x1, y1, x2, y2 = seg
    dx = x2 - x1
    dy = y2 - y1
    return math.degrees(math.atan2(dy, dx)) % 180.0


def _compute_intersections(segments, img_w, img_h):
    """
    Compute all pairwise intersections between non-parallel line segments.
    Only keeps intersections within a generous bounding box around the image
    (VP may be outside frame, but we bound at ±3× image dimensions to avoid outliers).

    Returns list of (ix, iy) points.
    """
    bounds_x = (-3 * img_w, 4 * img_w)
    bounds_y = (-3 * img_h, 4 * img_h)

    intersections = []
    n = len(segments)
    for i in range(n):
        for j in range(i + 1, n):
            # Skip near-parallel segments (angle difference < 10°)
            a1 = _segment_angle_deg(segments[i])
            a2 = _segment_angle_deg(segments[j])
            diff = abs(a1 - a2) % 180.0
            if diff > 90.0:
                diff = 180.0 - diff
            if diff < 10.0:
                continue  # parallel, skip

            pt = _line_intersection(segments[i], segments[j])
            if pt is None:
                continue
            ix, iy = pt
            if (bounds_x[0] <= ix <= bounds_x[1]) and (bounds_y[0] <= iy <= bounds_y[1]):
                intersections.append((ix, iy))

    return intersections


# ── Clustering ────────────────────────────────────────────────────────────────

def _cluster_intersections(intersections, img_w, img_h):
    """
    Cluster intersection points into a 2D histogram.
    Grid cell size: _GRID_CELL_FRACTION × (img_w, img_h).

    Returns (vp_x, vp_y, confidence) where:
        vp_x, vp_y  — centre of dominant cluster cell (analysis-space coords)
        confidence  — peak_count / total_intersections (clamped 0–1)
    Returns (None, None, 0.0) if no intersections.
    """
    if not intersections:
        return None, None, 0.0

    cell_w = max(1, img_w * _GRID_CELL_FRACTION)
    cell_h = max(1, img_h * _GRID_CELL_FRACTION)

    # Offset grid so that bounds_x min (-3*img_w) maps to cell 0
    offset_x = 3 * img_w
    offset_y = 3 * img_h

    counts = defaultdict(int)
    for (ix, iy) in intersections:
        ci = int((ix + offset_x) / cell_w)
        cj = int((iy + offset_y) / cell_h)
        counts[(ci, cj)] += 1

    if not counts:
        return None, None, 0.0

    best_cell, peak_count = max(counts.items(), key=lambda kv: kv[1])
    ci, cj = best_cell

    # Centre of cell in analysis space
    vp_x = (ci + 0.5) * cell_w - offset_x
    vp_y = (cj + 0.5) * cell_h - offset_y

    confidence = min(1.0, peak_count / max(1, len(intersections)))
    return vp_x, vp_y, confidence


# ── Core detection function ───────────────────────────────────────────────────

def detect_vp(image_path, vp_x_expected=None, vp_y_expected=None, tolerance_px=None):
    """
    Detect the dominant vanishing point in an environment image.

    Parameters
    ----------
    image_path : str
        Path to the PNG image file.
    vp_x_expected : int or None
        Expected VP X coordinate in original image pixels. If None, VP002 is skipped.
    vp_y_expected : int or None
        Expected VP Y coordinate in original image pixels. If None, VP002 is skipped.
    tolerance_px : int or None
        Distance tolerance for VP002 PASS/WARN/FAIL (default: _DEFAULT_TOLERANCE_PX).
        Applied in original image pixel scale.

    Returns
    -------
    dict with keys:
        file             — input path
        vp_x             — detected VP X (original image pixels) or None
        vp_y             — detected VP Y (original image pixels) or None
        confidence       — float [0.0, 1.0]; higher = more line agreement
        n_lines          — number of line segments found
        n_intersections  — number of pairwise intersections computed
        grade            — "PASS" / "WARN" / "FAIL"
        issues           — list of issue strings
        vp_x_expected    — passed-in expected X or None
        vp_y_expected    — passed-in expected Y or None
        distance_px      — Euclidean distance (original px) or None
        tolerance_px     — tolerance used for VP002
        image_width      — original image width
        image_height     — original image height
        skipped_reason   — non-empty string if detection was skipped
    """
    if tolerance_px is None:
        tolerance_px = _DEFAULT_TOLERANCE_PX

    result = {
        "file": image_path,
        "vp_x": None,
        "vp_y": None,
        "confidence": 0.0,
        "n_lines": 0,
        "n_intersections": 0,
        "grade": "FAIL",
        "issues": [],
        "vp_x_expected": vp_x_expected,
        "vp_y_expected": vp_y_expected,
        "distance_px": None,
        "tolerance_px": tolerance_px,
        "image_width": None,
        "image_height": None,
        "skipped_reason": "",
    }

    if not _NP_AVAILABLE:
        result["skipped_reason"] = "numpy not available"
        result["issues"].append("VP001 SKIP — numpy not installed")
        return result

    if not os.path.isfile(image_path):
        result["skipped_reason"] = "file not found"
        result["issues"].append("VP001 FAIL — file not found")
        return result

    # Get original size before downscale
    try:
        with Image.open(image_path) as _probe:
            orig_w, orig_h = _probe.size
    except Exception as e:
        result["skipped_reason"] = f"cannot open image: {e}"
        result["issues"].append(f"VP001 FAIL — cannot open image: {e}")
        return result

    result["image_width"] = orig_w
    result["image_height"] = orig_h

    gray_np, scale_x, scale_y = _load_gray(image_path)
    if gray_np is None:
        result["skipped_reason"] = "image load failed"
        result["issues"].append("VP001 FAIL — image load failed")
        return result

    small_h, small_w = gray_np.shape

    # Detect line segments
    if _CV2_AVAILABLE:
        segments = _detect_lines_hough(gray_np)
    else:
        segments = _detect_lines_numpy_fallback(gray_np)
        result["issues"].append("VP001 WARN — cv2 not available; using numpy fallback (less accurate)")

    result["n_lines"] = len(segments)

    if len(segments) < _MIN_LINE_SEGMENTS:
        result["grade"] = "FAIL"
        result["issues"].append(
            f"VP001 FAIL — only {len(segments)} line segment(s) detected "
            f"(min {_MIN_LINE_SEGMENTS} required)"
        )
        return result

    # Compute pairwise intersections
    intersections = _compute_intersections(segments, small_w, small_h)
    result["n_intersections"] = len(intersections)

    if not intersections:
        result["grade"] = "FAIL"
        result["issues"].append("VP001 FAIL — no valid intersection points found (all lines parallel)")
        return result

    # Cluster to find dominant VP
    vp_x_small, vp_y_small, confidence = _cluster_intersections(intersections, small_w, small_h)
    result["confidence"] = round(confidence, 4)

    if vp_x_small is None or confidence < _MIN_CONFIDENCE:
        result["grade"] = "FAIL"
        result["issues"].append(
            f"VP001 FAIL — VP confidence {confidence:.3f} below threshold {_MIN_CONFIDENCE}"
        )
        return result

    # Scale VP back to original image coordinates
    vp_x_orig = round(vp_x_small * scale_x)
    vp_y_orig = round(vp_y_small * scale_y)
    result["vp_x"] = vp_x_orig
    result["vp_y"] = vp_y_orig

    result["issues"].append(
        f"VP001 PASS — VP detected at ({vp_x_orig}, {vp_y_orig}) "
        f"conf={confidence:.3f} lines={len(segments)}"
    )

    # VP002: comparison to expected
    if vp_x_expected is not None and vp_y_expected is not None:
        dx = vp_x_orig - vp_x_expected
        dy = vp_y_orig - vp_y_expected
        dist = math.sqrt(dx * dx + dy * dy)
        result["distance_px"] = round(dist, 1)

        if dist <= tolerance_px:
            result["grade"] = "PASS"
            result["issues"].append(
                f"VP002 PASS — distance {dist:.1f}px ≤ tolerance {tolerance_px}px "
                f"(expected {vp_x_expected},{vp_y_expected})"
            )
        elif dist <= 2 * tolerance_px:
            result["grade"] = "WARN"
            result["issues"].append(
                f"VP002 WARN — distance {dist:.1f}px within 2× tolerance {tolerance_px}px "
                f"(expected {vp_x_expected},{vp_y_expected})"
            )
        else:
            result["grade"] = "FAIL"
            result["issues"].append(
                f"VP002 FAIL — distance {dist:.1f}px > 2× tolerance {tolerance_px}px "
                f"(expected {vp_x_expected},{vp_y_expected}; "
                f"detected {vp_x_orig},{vp_y_orig})"
            )
    else:
        # No expected VP — grade solely on VP001
        result["grade"] = "PASS"

    return result


# ── Batch detection ───────────────────────────────────────────────────────────

def detect_vp_batch(directory, vp_x_expected=None, vp_y_expected=None, tolerance_px=None):
    """
    Run detect_vp() on all PNG files in a directory.

    Parameters
    ----------
    directory : str
        Path to directory containing PNG files.
    vp_x_expected, vp_y_expected : int or None
        If provided, passed to detect_vp() for every image (global expected VP).
        Individual file comparison is better done with a config JSON; this is a
        convenience mode for scenes sharing the same VP spec.
    tolerance_px : int or None
        Tolerance override. Defaults to _DEFAULT_TOLERANCE_PX.

    Returns
    -------
    list of result dicts (one per PNG found)
    """
    results = []
    if not os.path.isdir(directory):
        return results
    pattern = os.path.join(directory, "*.png")
    paths = sorted(_glob.glob(pattern))
    for p in paths:
        r = detect_vp(p, vp_x_expected=vp_x_expected,
                      vp_y_expected=vp_y_expected, tolerance_px=tolerance_px)
        results.append(r)
    return results


# ── VP config JSON support ───────────────────────────────────────────────────

def load_vp_config(config_path):
    """Load and index vp_spec_config.json by output_filename.

    Parameters
    ----------
    config_path : str
        Path to vp_spec_config.json (or a compatible JSON with an "environments" list).

    Returns
    -------
    dict  mapping output_filename (str) → environment spec dict.
          Returns empty dict on any load/parse error.
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        index = {}
        for env in data.get("environments", []):
            fname = env.get("output_filename")
            if fname:
                index[fname] = env
        return index
    except Exception as e:
        sys.stderr.write(f"[sobel_vp_detect] load_vp_config failed: {e}\n")
        return {}


def lookup_vp_spec(config_index, image_path):
    """Look up VP spec for a given image path using a loaded config index.

    Matches by the basename of image_path against the output_filename keys
    in the config index.

    Parameters
    ----------
    config_index : dict
        Return value of load_vp_config().
    image_path : str
        Path to image file (basename is used for matching).

    Returns
    -------
    tuple (vp_x, vp_y, tolerance_px, world_type)
        vp_x / vp_y — int or None (None for glitch_layer environments).
        tolerance_px — int, from config or _DEFAULT_TOLERANCE_PX fallback.
        world_type — str or None.
    If no match found, returns (None, None, _DEFAULT_TOLERANCE_PX, None).
    """
    fname = os.path.basename(image_path)
    spec = config_index.get(fname)
    if spec is None:
        return None, None, _DEFAULT_TOLERANCE_PX, None
    vp_x = spec.get("vp_x")     # may be None for glitch_layer
    vp_y = spec.get("vp_y")
    tol = spec.get("tolerance_px") or _DEFAULT_TOLERANCE_PX
    world_type = spec.get("world_type")
    return vp_x, vp_y, tol, world_type


def detect_vp_batch_with_config(directory, config_path, tolerance_px=None):
    """Run detect_vp() on all PNG files in a directory using per-file VP specs.

    Each file's expected VP is looked up from config_path by output_filename.
    Files with world_type=="glitch_layer" are skipped (no VP expected).
    Files not found in the config are run without VP comparison (VP001 only).

    Parameters
    ----------
    directory : str
        Directory containing PNG files.
    config_path : str
        Path to vp_spec_config.json.
    tolerance_px : int or None
        Global tolerance override (overrides per-file config tolerance if set).

    Returns
    -------
    list of result dicts (same format as detect_vp()).
    Each result gains an extra key: "world_type" (str or None).
    """
    config_index = load_vp_config(config_path)
    results = []
    pattern = os.path.join(directory, "*.png")
    paths = sorted(_glob.glob(pattern))
    for p in paths:
        vp_x, vp_y, file_tol, world_type = lookup_vp_spec(config_index, p)
        if world_type == "glitch_layer":
            # Skip VP detection for abstract environments
            r = {
                "file": p,
                "vp_x": None, "vp_y": None, "confidence": 0.0,
                "n_lines": 0, "n_intersections": 0,
                "grade": "PASS",  # no VP requirement = not a failure
                "issues": ["VP001 SKIP — glitch_layer world type; no perspective VP expected"],
                "vp_x_expected": None, "vp_y_expected": None,
                "distance_px": None, "tolerance_px": file_tol,
                "image_width": None, "image_height": None,
                "skipped_reason": "glitch_layer — VP not applicable",
                "world_type": world_type,
            }
            results.append(r)
            continue
        used_tol = tolerance_px if tolerance_px is not None else file_tol
        r = detect_vp(p, vp_x_expected=vp_x, vp_y_expected=vp_y, tolerance_px=used_tol)
        r["world_type"] = world_type
        results.append(r)
    return results


# ── Report formatting ─────────────────────────────────────────────────────────

def format_report(results, include_pass=True):
    """
    Format a list of detect_vp() results as a human-readable string.

    Parameters
    ----------
    results : list of dict
        Output from detect_vp_batch() or [detect_vp(...)].
    include_pass : bool
        If False, only WARN and FAIL results are included (default: True — show all).

    Returns
    -------
    str
    """
    if not results:
        return "No results.\n"

    n_pass = sum(1 for r in results if r["grade"] == "PASS")
    n_warn = sum(1 for r in results if r["grade"] == "WARN")
    n_fail = sum(1 for r in results if r["grade"] == "FAIL")
    n_skip = sum(1 for r in results if r["skipped_reason"])

    lines = []
    lines.append("=" * 70)
    lines.append("LTG Sobel VP Detect Report")
    lines.append(f"  Total: {len(results)}  PASS: {n_pass}  WARN: {n_warn}  "
                 f"FAIL: {n_fail}  SKIP: {n_skip}")
    lines.append("=" * 70)

    for r in results:
        if not include_pass and r["grade"] == "PASS" and not r["skipped_reason"]:
            continue
        fname = os.path.basename(r["file"])
        lines.append("")
        lines.append(f"[{r['grade']}] {fname}")
        if r["skipped_reason"]:
            lines.append(f"  Skipped: {r['skipped_reason']}")
        else:
            vp_str = (f"  VP: ({r['vp_x']}, {r['vp_y']})  conf={r['confidence']:.3f}"
                      f"  lines={r['n_lines']}  intersections={r['n_intersections']}")
            if r["image_width"]:
                vp_str += f"  image={r['image_width']}×{r['image_height']}"
            lines.append(vp_str)
            if r["distance_px"] is not None:
                lines.append(f"  Distance to expected ({r['vp_x_expected']},{r['vp_y_expected']}): "
                             f"{r['distance_px']}px  tolerance={r['tolerance_px']}px")
        for issue in r["issues"]:
            lines.append(f"  {issue}")

    lines.append("")
    lines.append("=" * 70)
    return "\n".join(lines) + "\n"


# ── Debug PNG output ──────────────────────────────────────────────────────────

def save_debug_png(image_path, result, output_path):
    """
    Save an annotated PNG overlaying the detected VP (and expected VP if present)
    as crosshairs on the original image. Useful for visual validation.

    Parameters
    ----------
    image_path : str
        Original image path.
    result : dict
        Return value of detect_vp().
    output_path : str
        Where to save the annotated PNG (must be ≤1280px — thumbnail applied).
    """
    try:
        img = Image.open(image_path).convert("RGB")
        img.thumbnail((1280, 1280), Image.LANCZOS)
        draw = ImageDraw.Draw(img)

        # Scale VP coordinates to thumbnail size
        orig_w = result.get("image_width") or img.width
        orig_h = result.get("image_height") or img.height
        thumb_w, thumb_h = img.size
        sx = thumb_w / orig_w
        sy = thumb_h / orig_h

        def crosshair(cx, cy, color, size=20, width=2):
            cx = int(cx * sx)
            cy = int(cy * sy)
            draw.line([(cx - size, cy), (cx + size, cy)], fill=color, width=width)
            draw.line([(cx, cy - size), (cx, cy + size)], fill=color, width=width)
            draw.ellipse([(cx - size // 2, cy - size // 2),
                          (cx + size // 2, cy + size // 2)], outline=color, width=width)

        # Expected VP: green crosshair
        if result["vp_x_expected"] is not None and result["vp_y_expected"] is not None:
            crosshair(result["vp_x_expected"], result["vp_y_expected"],
                      color=(0, 220, 80), size=24, width=3)

        # Detected VP: colour by grade (blue=PASS, yellow=WARN, red=FAIL)
        if result["vp_x"] is not None and result["vp_y"] is not None:
            grade_color = {"PASS": (80, 160, 255), "WARN": (255, 200, 0), "FAIL": (255, 50, 50)}
            color = grade_color.get(result["grade"], (200, 200, 200))
            crosshair(result["vp_x"], result["vp_y"], color=color, size=18, width=2)

        img.save(output_path)
    except Exception as e:
        sys.stderr.write(f"[sobel_vp_detect] debug PNG failed: {e}\n")


# ── CLI ───────────────────────────────────────────────────────────────────────

def _parse_args(argv):
    """Minimal argument parser (stdlib only)."""
    args = {
        "target": None,
        "vp_x_expected": None,
        "vp_y_expected": None,
        "tolerance": _DEFAULT_TOLERANCE_PX,
        "vp_config": None,
        "save_report": None,
        "debug_png": None,
        "include_pass": True,
    }

    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == "--vp-x-expected" and i + 1 < len(argv):
            args["vp_x_expected"] = int(argv[i + 1]); i += 2
        elif arg == "--vp-y-expected" and i + 1 < len(argv):
            args["vp_y_expected"] = int(argv[i + 1]); i += 2
        elif arg == "--tolerance" and i + 1 < len(argv):
            args["tolerance"] = int(argv[i + 1]); i += 2
        elif arg == "--vp-config" and i + 1 < len(argv):
            args["vp_config"] = argv[i + 1]; i += 2
        elif arg == "--save-report" and i + 1 < len(argv):
            args["save_report"] = argv[i + 1]; i += 2
        elif arg == "--debug-png" and i + 1 < len(argv):
            args["debug_png"] = argv[i + 1]; i += 2
        elif arg == "--no-pass":
            args["include_pass"] = False; i += 1
        elif not arg.startswith("--"):
            args["target"] = arg; i += 1
        else:
            i += 1

    return args


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 2:
        print(f"LTG_TOOL_sobel_vp_detect.py  v{__version__}")
        print("Usage: python LTG_TOOL_sobel_vp_detect.py <image_or_dir>")
        print("       [--vp-x-expected X] [--vp-y-expected Y] [--tolerance PX]")
        print("       [--vp-config vp_spec_config.json]")
        print("       [--save-report PATH] [--debug-png PATH] [--no-pass]")
        print()
        print("--vp-config: auto-fills VP_X/VP_Y/tolerance per file from JSON spec.")
        print("             Use with a directory target for fully automated batch QA.")
        return 0

    args = _parse_args(argv)
    target = args["target"]
    if not target:
        print("Error: no target file or directory specified.", file=sys.stderr)
        return 2

    vp_x = args["vp_x_expected"]
    vp_y = args["vp_y_expected"]
    tol = args["tolerance"]
    vp_config = args["vp_config"]

    if os.path.isdir(target):
        if vp_config:
            # Config-aware batch: per-file VP lookup
            results = detect_vp_batch_with_config(target, vp_config,
                                                  tolerance_px=vp_x and tol)
        else:
            results = detect_vp_batch(target, vp_x_expected=vp_x,
                                      vp_y_expected=vp_y, tolerance_px=tol)
    elif os.path.isfile(target):
        if vp_config:
            # Single file + config: look up this file's spec
            config_index = load_vp_config(vp_config)
            spec_vp_x, spec_vp_y, spec_tol, world_type = lookup_vp_spec(config_index, target)
            # CLI explicit flags override config
            used_x = vp_x if vp_x is not None else spec_vp_x
            used_y = vp_y if vp_y is not None else spec_vp_y
            used_tol = tol if args["tolerance"] != _DEFAULT_TOLERANCE_PX else spec_tol
            results = [detect_vp(target, vp_x_expected=used_x,
                                 vp_y_expected=used_y, tolerance_px=used_tol)]
        else:
            results = [detect_vp(target, vp_x_expected=vp_x,
                                 vp_y_expected=vp_y, tolerance_px=tol)]
        if args["debug_png"] and results:
            save_debug_png(target, results[0], args["debug_png"])
            print(f"Debug PNG saved to {args['debug_png']}")
    else:
        print(f"Error: '{target}' is not a file or directory.", file=sys.stderr)
        return 2

    report = format_report(results, include_pass=args["include_pass"])
    print(report)

    if args["save_report"]:
        try:
            with open(args["save_report"], "w") as f:
                f.write(report)
            print(f"Report saved to {args['save_report']}")
        except Exception as e:
            print(f"Warning: could not save report: {e}", file=sys.stderr)

    # Exit code: 0=all PASS, 1=any WARN, 2=any FAIL
    if any(r["grade"] == "FAIL" for r in results):
        return 2
    if any(r["grade"] == "WARN" for r in results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
