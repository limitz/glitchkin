#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_construction_stiffness.py — v1.0.0 (Cycle 50, Kai Nakamura)

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

Author: Kai Nakamura — Cycle 50
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


def analyze_image(filepath, min_run=DEFAULT_MIN_RUN,
                  straightness=DEFAULT_STRAIGHTNESS):
    """Analyze a single character image for construction stiffness."""
    img = Image.open(filepath).convert("RGB")
    mask = extract_silhouette_mask(img)

    all_points = []

    if _CV2_AVAILABLE:
        contours, edges = extract_outline_cv2(mask)
        for contour in contours:
            if len(contour) < min_run:
                continue
            pts = [(int(p[0][0]), int(p[0][1])) for p in contour]
            all_points.extend(pts)

        # Analyze each contour separately and aggregate
        total_straight = 0
        total_curved = 0
        total_pixels = 0
        longest_run = 0
        all_runs = []

        for contour in contours:
            if len(contour) < min_run:
                total_curved += len(contour)
                total_pixels += len(contour)
                continue
            pts = [(int(p[0][0]), int(p[0][1])) for p in contour]
            result = analyze_contour_straightness(pts, min_run, straightness)
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
            # Sort points for contour ordering (simple row-major, not ideal but functional)
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
        "file": os.path.basename(filepath),
        "filepath": filepath,
        "total_outline_pixels": total_pixels,
        "straight_pixels": total_straight,
        "curved_pixels": total_curved,
        "straight_pct": round(sp, 4),
        "longest_straight_run": longest_run,
        "stiffness_score": round(ss, 4),
        "verdict": v,
        "num_straight_runs": len(all_runs),
        "backend": "cv2" if _CV2_AVAILABLE else "pil",
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

    # Draw silhouette as dark grey
    mask_img = Image.fromarray(mask)
    for y in range(h):
        for x in range(w):
            if mask[y, x] > 127:
                viz.putpixel((x, y), (60, 60, 60))

    draw = ImageDraw.Draw(viz)

    if _CV2_AVAILABLE:
        contours, edges = extract_outline_cv2(mask)
        for contour in contours:
            if len(contour) < min_run:
                # Draw all as green (curved)
                for p in contour:
                    px, py = int(p[0][0]), int(p[0][1])
                    if 0 <= px < w and 0 <= py < h:
                        viz.putpixel((px, py), (0, 200, 0))
                continue

            pts = [(int(p[0][0]), int(p[0][1])) for p in contour]
            result = analyze_contour_straightness(pts, min_run, straightness)
            is_straight = result.get("is_straight", [False] * len(pts))

            for idx, (px, py) in enumerate(pts):
                if 0 <= px < w and 0 <= py < h:
                    if idx < len(is_straight) and is_straight[idx]:
                        viz.putpixel((px, py), (255, 50, 50))  # Red = straight
                    else:
                        viz.putpixel((px, py), (0, 200, 0))    # Green = curved
    else:
        points, edge_mask = extract_outline_pil(mask)
        # All green for PIL fallback (no contour ordering = unreliable straight detection)
        for y, x in points:
            if 0 <= x < w and 0 <= y < h:
                viz.putpixel((x, y), (0, 200, 0))

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
    lines.append(f"Backend: {'OpenCV (cv2)' if _CV2_AVAILABLE else 'PIL fallback (reduced accuracy)'}")
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
    lines.append(f"**Backend:** {'OpenCV (cv2)' if _CV2_AVAILABLE else 'PIL fallback'}")
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
