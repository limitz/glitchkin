#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_construction_stiffness.py — v2.0.0 (Cycle 51, Kai Nakamura)

Construction Stiffness Detector.

Analyzes character outlines for straight-line runs. Long straight edges indicate
geometric/stiff construction. Organic cartoon characters should have minimal
straight-line runs — curves should dominate the outline.

How it works:
  1. Extracts character silhouette from image (bg detection + thresholding).
  2. Runs Canny edge detection on the silhouette to get the outline.
  3. Traces contour points along the outline.
  4. For each consecutive run of N points, measures the deviation from a
     straight line (max perpendicular distance / run length).
  5. If deviation < straightness_threshold for a run of >= min_run_length pixels,
     that run is classified as "straight."
  6. Reports: total outline pixels, straight-run pixels, curved pixels,
     straight percentage.

Metrics:
  - Straight Percentage (SP): fraction of outline that is straight runs.
  - Longest Straight Run (LSR): longest single straight segment in pixels.
  - Stiffness Score: weighted combination = 0.6*SP + 0.4*(LSR/outline_length).

Thresholds:
  FAIL: Stiffness > 0.40 — too geometric, needs organic curves
  WARN: Stiffness > 0.25 — marginally stiff, could benefit from curve work
  PASS: Stiffness <= 0.25 — adequately organic outline

Input: Character PNG (single character or expression sheet panels).
Output: Per-image stiffness metrics. Optional visualization showing straight
        runs in red and curves in green overlaid on the silhouette.

Usage:
  python3 LTG_TOOL_construction_stiffness.py <images...>
          [--min-run 8]
          [--straightness 0.02]
          [--output viz.png]
          [--json]
          [--report path/to/report.md]

  --min-run         Minimum consecutive pixels for a "straight run" (default 8).
  --straightness    Max deviation ratio for straight classification (default 0.02).

v2.0.0 C51 — scikit-image backend: Canny via skimage.feature.canny, contour tracing
             via skimage.measure.find_contours. Produces cleaner contours with
             sub-pixel accuracy. Falls back to cv2 then PIL if skimage unavailable.
             Shapely LineString used for contour straightness analysis when available
             (faster, more numerically stable simplify-based detection).

Author: Kai Nakamura — Cycle 50 (v1), Cycle 51 (v2)
Date: 2026-03-30
"""

import sys
import os
import argparse
import json
import math
import numpy as np
from PIL import Image, ImageDraw

try:
    import cairo as _cairo_mod
    _CAIRO_AVAILABLE = True
except ImportError:
    _CAIRO_AVAILABLE = False

try:
    from skimage.feature import canny as skimage_canny
    from skimage.measure import find_contours as skimage_find_contours
    from skimage.filters import gaussian as skimage_gaussian
    _SKIMAGE_AVAILABLE = True
except ImportError:
    _SKIMAGE_AVAILABLE = False

try:
    from shapely.geometry import LineString as ShapelyLineString
    _SHAPELY_AVAILABLE = True
except ImportError:
    _SHAPELY_AVAILABLE = False

try:
    import cv2
    _CV2_AVAILABLE = True
except ImportError:
    _CV2_AVAILABLE = False

# ─── CONFIG ──────────────────────────────────────────────────────────────────

BG_SAMPLE_SIZE = 8
BG_TOLERANCE = 45
DEFAULT_MIN_RUN = 8
DEFAULT_STRAIGHTNESS = 0.02  # max deviation/run_length ratio

FAIL_THRESHOLD = 0.40
WARN_THRESHOLD = 0.25


# ─── CAIRO SURFACE SUPPORT ─────────────────────────────────────────────────

def _ensure_pil_image(obj, mode="RGB"):
    """Accept PIL Image, cairo ImageSurface, or file path. Returns PIL Image.

    Cairo ARGB32 surfaces are converted via BGRA→RGBA byte swap + PIL.Image.fromarray.
    File paths are opened with Image.open().
    """
    if isinstance(obj, Image.Image):
        return obj.convert(mode)
    if isinstance(obj, (str, os.PathLike)):
        return Image.open(obj).convert(mode)
    if _CAIRO_AVAILABLE and isinstance(obj, _cairo_mod.ImageSurface):
        w = obj.get_width()
        h = obj.get_height()
        buf = obj.get_data()
        arr = np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 4).copy()
        rgba = np.stack([arr[:, :, 2], arr[:, :, 1], arr[:, :, 0], arr[:, :, 3]], axis=2)
        img = Image.fromarray(rgba, "RGBA")
        return img.convert(mode)
    raise TypeError(f"Unsupported input type: {type(obj)}. Expected PIL Image, cairo ImageSurface, or file path.")


# ─── OUTLINE EXTRACTION ────────────────────────────────────────────────────


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


def extract_silhouette_mask(img, bg_tolerance=BG_TOLERANCE):
    """Extract binary silhouette mask. Returns numpy uint8 array (0 or 255)."""
    bg = detect_background_color(img)
    rgb = img.convert("RGB")
    arr = np.array(rgb, dtype=np.int16)
    bg_arr = np.array(bg, dtype=np.int16).reshape(1, 1, 3)
    diff = np.abs(arr - bg_arr)
    is_bg = np.all(diff <= bg_tolerance, axis=2)
    mask = (~is_bg).astype(np.uint8) * 255
    return mask


def extract_outline_skimage(mask):
    """Use scikit-image Canny + find_contours for sub-pixel outline extraction.
    Returns list of contour point arrays (each Nx2, dtype float) and edge image."""
    # Normalize mask to float [0,1]
    mask_f = (mask > 127).astype(np.float64)
    # Smooth slightly before edge detection
    smoothed = skimage_gaussian(mask_f, sigma=1.0, preserve_range=True)
    edges = skimage_canny(smoothed, sigma=0.5, low_threshold=0.3, high_threshold=0.7)
    # find_contours returns list of (N,2) arrays in (row, col) order
    contours_rc = skimage_find_contours(mask_f, level=0.5)
    # Convert to (x, y) format for compatibility
    contours = []
    for c in contours_rc:
        if len(c) < 3:
            continue
        # c is (row, col) -> convert to (x, y) = (col, row)
        xy = np.column_stack([c[:, 1], c[:, 0]])
        contours.append(xy)
    edge_img = (edges * 255).astype(np.uint8)
    return contours, edge_img


def extract_outline_cv2(mask):
    """Use OpenCV Canny + contour finding to get outline points.
    Returns list of contour point arrays and the edge image."""
    # Apply slight blur to reduce noise
    blurred = cv2.GaussianBlur(mask, (3, 3), 0)
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours, edges


def extract_outline_pil(mask_np):
    """Fallback outline extraction without OpenCV using erosion-based approach.
    Returns list of (y, x) outline pixel coordinates and edge mask."""
    h, w = mask_np.shape

    # Simple erosion: a pixel is on the outline if it's foreground and has
    # at least one background neighbor (4-connected)
    fg = mask_np > 127
    outline = np.zeros_like(mask_np)

    # Pad to avoid boundary issues
    padded = np.pad(fg, 1, mode='constant', constant_values=False)

    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        shifted = padded[1 + dy:h + 1 + dy, 1 + dx:w + 1 + dx]
        # Foreground pixel with at least one bg neighbor
        boundary = fg & (~shifted)
        outline = outline | (boundary.astype(np.uint8) * 255)

    # Get coordinates
    ys, xs = np.where(outline > 0)
    points = list(zip(ys.tolist(), xs.tolist()))
    return points, outline


# ─── STRAIGHTNESS ANALYSIS ──────────────────────────────────────────────────


def analyze_contour_straightness_shapely(points, min_run=DEFAULT_MIN_RUN,
                                          straightness_threshold=DEFAULT_STRAIGHTNESS):
    """Shapely-based straightness analysis using Douglas-Peucker simplification.

    Strategy: simplify the contour with a tight tolerance. Long segments in the
    simplified line correspond to straight runs in the original. We map each
    original point to its nearest simplified segment and measure deviation.

    This is faster and more numerically stable than the sliding-window approach
    for large contours."""
    n = len(points)
    if n < min_run:
        return {
            "total_pixels": n,
            "straight_pixels": 0,
            "curved_pixels": n,
            "straight_pct": 0.0,
            "longest_straight_run": 0,
            "straight_runs": [],
        }

    line = ShapelyLineString(points)
    # Simplify with tolerance proportional to straightness_threshold * typical segment length
    # A tighter tolerance means more segments kept = more curves detected
    avg_seg_len = line.length / max(n - 1, 1)
    tolerance = straightness_threshold * avg_seg_len * min_run
    simplified = line.simplify(tolerance, preserve_topology=True)
    simp_coords = list(simplified.coords)

    # Build segments from simplified line
    segments = []
    for i in range(len(simp_coords) - 1):
        x1, y1 = simp_coords[i]
        x2, y2 = simp_coords[i + 1]
        seg_len = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        segments.append((x1, y1, x2, y2, seg_len))

    # Map original points to simplified segments
    is_straight = [False] * n
    straight_runs = []
    current_run_start = None
    current_seg_idx = 0

    for i, (px, py) in enumerate(points):
        # Find nearest simplified segment
        best_seg = 0
        best_dist = float('inf')
        for si, (x1, y1, x2, y2, sl) in enumerate(segments):
            d = _point_to_seg_dist(px, py, x1, y1, x2, y2)
            if d < best_dist:
                best_dist = d
                best_seg = si

        seg = segments[best_seg]
        # A point is on a "straight" segment if the segment is long enough
        if seg[4] >= min_run:
            is_straight[i] = True

    # Extract runs
    run_start = None
    for i in range(n):
        if is_straight[i]:
            if run_start is None:
                run_start = i
        else:
            if run_start is not None:
                run_len = i - run_start
                if run_len >= min_run:
                    straight_runs.append({
                        "start": run_start,
                        "end": i,
                        "length": run_len,
                    })
                run_start = None
    if run_start is not None:
        run_len = n - run_start
        if run_len >= min_run:
            straight_runs.append({
                "start": run_start,
                "end": n,
                "length": run_len,
            })

    # Recompute is_straight based on valid runs only
    is_straight_final = [False] * n
    longest_run = 0
    for run in straight_runs:
        for k in range(run["start"], min(run["end"], n)):
            is_straight_final[k] = True
        longest_run = max(longest_run, run["length"])

    straight_count = sum(is_straight_final)
    return {
        "total_pixels": n,
        "straight_pixels": straight_count,
        "curved_pixels": n - straight_count,
        "straight_pct": straight_count / n if n > 0 else 0.0,
        "longest_straight_run": longest_run,
        "straight_runs": straight_runs,
        "is_straight": is_straight_final,
    }


def _point_to_seg_dist(px, py, x1, y1, x2, y2):
    """Distance from point to line segment (not infinite line)."""
    dx, dy = x2 - x1, y2 - y1
    length_sq = dx * dx + dy * dy
    if length_sq < 1e-9:
        return math.sqrt((px - x1) ** 2 + (py - y1) ** 2)
    t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / length_sq))
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    return math.sqrt((px - proj_x) ** 2 + (py - proj_y) ** 2)


def point_to_line_distance(px, py, x1, y1, x2, y2):
    """Perpendicular distance from point (px,py) to line through (x1,y1)-(x2,y2)."""
    dx = x2 - x1
    dy = y2 - y1
    length_sq = dx * dx + dy * dy
    if length_sq < 1e-9:
        return math.sqrt((px - x1) ** 2 + (py - y1) ** 2)
    # Cross product magnitude / line length
    cross = abs(dy * px - dx * py + x2 * y1 - y2 * x1)
    return cross / math.sqrt(length_sq)


def analyze_contour_straightness(points, min_run=DEFAULT_MIN_RUN,
                                  straightness_threshold=DEFAULT_STRAIGHTNESS):
    """Analyze a sequence of contour points for straight runs.

    Args:
        points: list of (x, y) tuples in contour order
        min_run: minimum points for a "straight run"
        straightness_threshold: max deviation/length ratio

    Returns:
        dict with straight_pixels, curved_pixels, total_pixels,
        straight_pct, longest_straight_run, straight_runs list
    """
    n = len(points)
    if n < min_run:
        return {
            "total_pixels": n,
            "straight_pixels": 0,
            "curved_pixels": n,
            "straight_pct": 0.0,
            "longest_straight_run": 0,
            "straight_runs": [],
        }

    is_straight = [False] * n
    straight_runs = []
    longest_run = 0

    # Sliding window: for each start point, extend the run as long as all
    # intermediate points are within straightness_threshold of the start-end line
    i = 0
    while i < n:
        best_end = i  # best end of straight run starting at i

        for j in range(i + min_run, min(n + 1, i + n)):
            # Line from points[i] to points[j-1]
            x1, y1 = points[i]
            x2, y2 = points[(j - 1) % n]
            run_length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if run_length < 1.0:
                continue

            # Check all intermediate points
            all_close = True
            for k in range(i + 1, j - 1):
                px, py = points[k % n]
                dist = point_to_line_distance(px, py, x1, y1, x2, y2)
                if dist / run_length > straightness_threshold:
                    all_close = False
                    break

            if all_close:
                best_end = j
            else:
                break

        run_len = best_end - i
        if run_len >= min_run:
            for k in range(i, best_end):
                if k < n:
                    is_straight[k] = True
            straight_runs.append({
                "start": i,
                "end": best_end,
                "length": run_len,
            })
            longest_run = max(longest_run, run_len)
            i = best_end
        else:
            i += 1

    straight_count = sum(is_straight)
    curved_count = n - straight_count

    return {
        "total_pixels": n,
        "straight_pixels": straight_count,
        "curved_pixels": curved_count,
        "straight_pct": straight_count / n if n > 0 else 0.0,
        "longest_straight_run": longest_run,
        "straight_runs": straight_runs,
        "is_straight": is_straight,
    }


# ─── STIFFNESS SCORE ────────────────────────────────────────────────────────


def stiffness_score(straight_pct, longest_run, total_pixels):
    """Combined stiffness score: 0.6*SP + 0.4*(LSR/total)."""
    lsr_ratio = longest_run / total_pixels if total_pixels > 0 else 0.0
    return 0.6 * straight_pct + 0.4 * lsr_ratio


def verdict(score):
    if score > FAIL_THRESHOLD:
        return "FAIL"
    elif score > WARN_THRESHOLD:
        return "WARN"
    return "PASS"


# ─── IMAGE ANALYSIS ─────────────────────────────────────────────────────────


def analyze_image(filepath_or_surface, min_run=DEFAULT_MIN_RUN,
                  straightness=DEFAULT_STRAIGHTNESS):
    """Analyze a single character image for construction stiffness.

    Accepts file path (str/Path), PIL Image, or cairo.ImageSurface.
    Backend priority: skimage > cv2 > PIL fallback.
    Straightness analysis: Shapely (if available) > sliding-window.
    """
    img = _ensure_pil_image(filepath_or_surface, mode="RGB")
    mask = extract_silhouette_mask(img)

    total_straight = 0
    total_curved = 0
    total_pixels = 0
    longest_run = 0
    all_runs = []
    backend_name = "pil"

    # Choose straightness analyzer
    use_shapely = _SHAPELY_AVAILABLE
    straightness_fn = (analyze_contour_straightness_shapely if use_shapely
                       else analyze_contour_straightness)

    if _SKIMAGE_AVAILABLE:
        backend_name = "skimage" + ("+shapely" if use_shapely else "")
        contours, edges = extract_outline_skimage(mask)
        for contour in contours:
            n_pts = len(contour)
            if n_pts < min_run:
                total_curved += n_pts
                total_pixels += n_pts
                continue
            pts = [(float(p[0]), float(p[1])) for p in contour]
            result = straightness_fn(pts, min_run, straightness)
            total_straight += result["straight_pixels"]
            total_curved += result["curved_pixels"]
            total_pixels += result["total_pixels"]
            longest_run = max(longest_run, result["longest_straight_run"])
            all_runs.extend(result["straight_runs"])

    elif _CV2_AVAILABLE:
        backend_name = "cv2" + ("+shapely" if use_shapely else "")
        contours, edges = extract_outline_cv2(mask)
        for contour in contours:
            if len(contour) < min_run:
                total_curved += len(contour)
                total_pixels += len(contour)
                continue
            pts = [(int(p[0][0]), int(p[0][1])) for p in contour]
            result = straightness_fn(pts, min_run, straightness)
            total_straight += result["straight_pixels"]
            total_curved += result["curved_pixels"]
            total_pixels += result["total_pixels"]
            longest_run = max(longest_run, result["longest_straight_run"])
            all_runs.extend(result["straight_runs"])
    else:
        # PIL fallback
        points, edge_mask = extract_outline_pil(mask)
        total_pixels = len(points)
        if total_pixels >= min_run:
            result = analyze_contour_straightness(points, min_run, straightness)
            total_straight = result["straight_pixels"]
            total_curved = result["curved_pixels"]
            longest_run = result["longest_straight_run"]
            all_runs = result["straight_runs"]
        else:
            total_straight = 0
            total_curved = total_pixels
            longest_run = 0
            all_runs = []

    sp = total_straight / total_pixels if total_pixels > 0 else 0.0
    ss = stiffness_score(sp, longest_run, total_pixels)
    v = verdict(ss)

    return {
        "file": os.path.basename(str(filepath_or_surface)) if isinstance(filepath_or_surface, (str, os.PathLike)) else "<surface>",
        "filepath": str(filepath_or_surface) if isinstance(filepath_or_surface, (str, os.PathLike)) else "<surface>",
        "total_outline_pixels": total_pixels,
        "straight_pixels": total_straight,
        "curved_pixels": total_curved,
        "straight_pct": round(sp, 4),
        "longest_straight_run": longest_run,
        "stiffness_score": round(ss, 4),
        "verdict": v,
        "num_straight_runs": len(all_runs),
        "backend": backend_name,
    }


def analyze_batch(filepaths, min_run=DEFAULT_MIN_RUN, straightness=DEFAULT_STRAIGHTNESS):
    """Analyze multiple images."""
    results = []
    for fp in filepaths:
        try:
            result = analyze_image(fp, min_run, straightness)
            results.append(result)
        except Exception as e:
            results.append({"file": os.path.basename(fp), "error": str(e)})
    return results


# ─── VISUALIZATION ──────────────────────────────────────────────────────────


def generate_visualization(filepath, output_path, min_run=DEFAULT_MIN_RUN,
                           straightness=DEFAULT_STRAIGHTNESS):
    """Generate visualization with straight runs in red, curves in green."""
    img = Image.open(filepath).convert("RGB")
    mask = extract_silhouette_mask(img)

    # Create dark version of original for overlay
    w, h = img.size
    viz = Image.new("RGB", (w, h), (30, 30, 30))

    # Draw silhouette as dark grey using numpy for speed
    viz_arr = np.array(viz)
    fg = mask > 127
    viz_arr[fg] = [60, 60, 60]

    use_shapely = _SHAPELY_AVAILABLE
    straightness_fn = (analyze_contour_straightness_shapely if use_shapely
                       else analyze_contour_straightness)

    def _draw_contour_on_arr(pts, is_straight_flags, arr, width, height):
        """Draw contour points onto numpy array: red=straight, green=curved."""
        for idx, (px_f, py_f) in enumerate(pts):
            px, py = int(round(px_f)), int(round(py_f))
            if 0 <= px < width and 0 <= py < height:
                if idx < len(is_straight_flags) and is_straight_flags[idx]:
                    arr[py, px] = [255, 50, 50]   # Red = straight
                else:
                    arr[py, px] = [0, 200, 0]      # Green = curved

    if _SKIMAGE_AVAILABLE:
        contours, edges = extract_outline_skimage(mask)
        for contour in contours:
            n_pts = len(contour)
            if n_pts < min_run:
                for p in contour:
                    px, py = int(round(p[0])), int(round(p[1]))
                    if 0 <= px < w and 0 <= py < h:
                        viz_arr[py, px] = [0, 200, 0]
                continue
            pts = [(float(p[0]), float(p[1])) for p in contour]
            result = straightness_fn(pts, min_run, straightness)
            is_straight = result.get("is_straight", [False] * len(pts))
            _draw_contour_on_arr(pts, is_straight, viz_arr, w, h)

    elif _CV2_AVAILABLE:
        contours, edges = extract_outline_cv2(mask)
        for contour in contours:
            if len(contour) < min_run:
                for p in contour:
                    px, py = int(p[0][0]), int(p[0][1])
                    if 0 <= px < w and 0 <= py < h:
                        viz_arr[py, px] = [0, 200, 0]
                continue
            pts = [(int(p[0][0]), int(p[0][1])) for p in contour]
            result = straightness_fn(pts, min_run, straightness)
            is_straight = result.get("is_straight", [False] * len(pts))
            _draw_contour_on_arr(pts, is_straight, viz_arr, w, h)
    else:
        points, edge_mask = extract_outline_pil(mask)
        for y_pt, x_pt in points:
            if 0 <= x_pt < w and 0 <= y_pt < h:
                viz_arr[y_pt, x_pt] = [0, 200, 0]

    viz = Image.fromarray(viz_arr)

    # Ensure within 1280px
    vw, vh = viz.size
    if vw > 1280 or vh > 1280:
        scale = min(1280 / vw, 1280 / vh)
        viz = viz.resize((int(vw * scale), int(vh * scale)), Image.BILINEAR)

    viz.save(output_path)
    return output_path


# ─── TEXT REPORT ─────────────────────────────────────────────────────────────


def format_report(results):
    """Format results as text."""
    lines = []
    lines.append("=" * 70)
    lines.append("CONSTRUCTION STIFFNESS REPORT")
    lines.append("=" * 70)
    if _SKIMAGE_AVAILABLE:
        be = "scikit-image" + (" + Shapely" if _SHAPELY_AVAILABLE else "")
    elif _CV2_AVAILABLE:
        be = "OpenCV (cv2)" + (" + Shapely" if _SHAPELY_AVAILABLE else "")
    else:
        be = "PIL fallback (reduced accuracy)"
    lines.append(f"Backend: {be}")
    lines.append("")

    for r in results:
        if "error" in r:
            lines.append(f"{r['file']}: ERROR — {r['error']}")
            continue

        v = r["verdict"]
        flag = " <<<" if v in ("FAIL", "WARN") else ""
        lines.append(f"{r['file']}:")
        lines.append(f"  Outline: {r['total_outline_pixels']}px | "
                     f"Straight: {r['straight_pixels']}px ({r['straight_pct']:.1%}) | "
                     f"Curved: {r['curved_pixels']}px")
        lines.append(f"  Longest straight run: {r['longest_straight_run']}px | "
                     f"Straight segments: {r['num_straight_runs']}")
        lines.append(f"  Stiffness Score: {r['stiffness_score']:.4f} [{v}]{flag}")
        lines.append("")

    # Summary
    verdicts = [r["verdict"] for r in results if "verdict" in r]
    fail_count = verdicts.count("FAIL")
    warn_count = verdicts.count("WARN")
    pass_count = verdicts.count("PASS")
    overall = "FAIL" if fail_count else ("WARN" if warn_count else "PASS")

    lines.append(f"SUMMARY: {len(verdicts)} images — PASS={pass_count} WARN={warn_count} FAIL={fail_count}")
    lines.append(f"OVERALL: {overall}")
    lines.append("=" * 70)
    return "\n".join(lines)


def format_markdown_report(results):
    """Format results as markdown."""
    lines = []
    lines.append("# Construction Stiffness Report")
    lines.append("")
    if _SKIMAGE_AVAILABLE:
        be = "scikit-image" + (" + Shapely" if _SHAPELY_AVAILABLE else "")
    elif _CV2_AVAILABLE:
        be = "OpenCV (cv2)" + (" + Shapely" if _SHAPELY_AVAILABLE else "")
    else:
        be = "PIL fallback"
    lines.append(f"**Backend:** {be}")
    lines.append("")

    lines.append("| File | Outline px | Straight % | Longest Run | Stiffness | Verdict |")
    lines.append("|------|-----------|------------|-------------|-----------|---------|")

    for r in results:
        if "error" in r:
            lines.append(f"| {r['file']} | ERROR | — | — | — | — |")
            continue
        lines.append(
            f"| {r['file']} | {r['total_outline_pixels']} | "
            f"{r['straight_pct']:.1%} | {r['longest_straight_run']}px | "
            f"{r['stiffness_score']:.4f} | {r['verdict']} |"
        )

    lines.append("")
    lines.append("## Metric Definitions")
    lines.append("- **Straight %**: Fraction of outline pixels in straight runs (min run length, max deviation threshold).")
    lines.append("- **Longest Run**: Longest single straight segment in pixels.")
    lines.append("- **Stiffness Score**: 0.6 * Straight% + 0.4 * (LongestRun / TotalOutline). Higher = stiffer.")
    lines.append(f"- **Thresholds**: FAIL > {FAIL_THRESHOLD}, WARN > {WARN_THRESHOLD}, PASS <= {WARN_THRESHOLD}")
    lines.append("- Organic cartoon characters should have low stiffness. Red = straight runs (bad), Green = curves (good).")
    return "\n".join(lines)


# ─── CLI ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Construction Stiffness Detector")
    parser.add_argument("inputs", nargs="+", help="Character image PNGs or directories")
    parser.add_argument("--min-run", type=int, default=DEFAULT_MIN_RUN,
                        help=f"Min straight run length (default {DEFAULT_MIN_RUN})")
    parser.add_argument("--straightness", type=float, default=DEFAULT_STRAIGHTNESS,
                        help=f"Straightness threshold (default {DEFAULT_STRAIGHTNESS})")
    parser.add_argument("--output", help="Visualization output path (first image only)")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--report", help="Write markdown report to file")
    args = parser.parse_args()

    # Collect files
    filepaths = []
    for inp in args.inputs:
        if os.path.isdir(inp):
            for f in sorted(os.listdir(inp)):
                if f.lower().endswith(".png"):
                    filepaths.append(os.path.join(inp, f))
        elif os.path.isfile(inp):
            filepaths.append(inp)

    if not filepaths:
        print("ERROR: No valid input files.", file=sys.stderr)
        sys.exit(1)

    results = analyze_batch(filepaths, args.min_run, args.straightness)

    if args.json:
        # Remove non-serializable items
        clean = []
        for r in results:
            c = {k: v for k, v in r.items() if k != "filepath"}
            clean.append(c)
        print(json.dumps(clean, indent=2))
    else:
        print(format_report(results))

    if args.output and filepaths:
        generate_visualization(filepaths[0], args.output, args.min_run, args.straightness)
        print(f"\nVisualization saved: {args.output}")

    if args.report:
        md = format_markdown_report(results)
        os.makedirs(os.path.dirname(args.report) or ".", exist_ok=True)
        with open(args.report, "w") as f:
            f.write(md)
        print(f"Report saved: {args.report}")

    # Exit code
    verdicts = [r["verdict"] for r in results if "verdict" in r]
    if "FAIL" in verdicts:
        sys.exit(2)
    elif "WARN" in verdicts:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
