#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_proportion_verify.py
-----------------------------------
PNG proportion verifier for "Luma & the Glitchkin" characters.

Given a PNG file and an approximate character bounding box (x, y, w, h):
  - Detects the character's head by scanning for the topmost dense cluster
    of non-background pixels.
  - Measures head height (px) and total character height (px) within the box.
  - Reports the head-to-body ratio and whether it matches the canonical
    3.2-head spec (±5% tolerance).
  - Optionally accepts eye_width_px and head_height_px to compute ew/HR ratio
    against the canonical ew = HR * 0.22 spec (±5% tolerance).

Output: plain text report with PASS / FAIL / WARN per metric.

Usage:
    python LTG_TOOL_proportion_verify.py <png_file> <x> <y> <w> <h>
                                               [--ew <eye_width_px>]
                                               [--hr <head_height_px>]

    x, y: top-left of bounding box (pixels, 0-indexed)
    w, h: width and height of bounding box (pixels)

    --ew   eye width in pixels (optional; enables ew/HR ratio check)
    --hr   override head height in pixels (optional; skips auto-detect for
           head height, used together with --ew)

Algorithm:
  1. Crop the image to the bounding box.
  2. Convert to RGBA.  Background is detected as the most common edge colour
     (left column, right column, top row, bottom row).
  3. Scan rows from top.  A row is "occupied" if it contains at least
     DENSITY_THRESHOLD non-background pixels (alpha > 128, colour distance
     from BG > BG_DIST_THRESHOLD).
  4. First occupied row = top of character.  Last occupied row = bottom of
     character.  Total character height = bottom - top + 1.
  5. Head detection: starting from the first occupied row, find the first
     gap in occupied rows that is wider than HEAD_GAP_ROWS.  Everything
     before the gap is "head".  Head height = gap_start_row - top + 1.
     Fallback: if no gap is found, head height = total_height / 3.2.
  6. Compute ratio = total_height / head_height.
  7. Compare to canonical 3.2 (±5%).
  8. If --ew and --hr given, compute ew / hr and compare to canonical 0.22 (±5%).

Requires only Pillow (PIL).  No Claude vision API calls.
"""

import sys
import argparse
import collections
import math
from PIL import Image

__version__ = "1.0.0"

# ─── Tuning constants ────────────────────────────────────────────────────────

DENSITY_THRESHOLD = 3       # min non-BG pixels in a row to count as "occupied"
BG_DIST_THRESHOLD = 20      # RGB Euclidean distance to classify a pixel as non-BG
ALPHA_THRESHOLD   = 128     # pixels below this alpha are treated as transparent
HEAD_GAP_ROWS     = 4       # a gap of at least this many empty rows separates head from neck
CANONICAL_RATIO   = 3.2     # canonical head-to-body ratio
RATIO_TOLERANCE   = 0.05    # ±5% tolerance
CANONICAL_EW_HR   = 0.22    # canonical eye-width / head-height ratio
EW_HR_TOLERANCE   = 0.05    # ±5% tolerance

# ─── Helpers ─────────────────────────────────────────────────────────────────

def rgb_dist(a, b):
    """Euclidean distance in RGB space."""
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)


def detect_background(img_rgba, sample_width=5):
    """
    Estimate background colour from the image edges.
    Returns an (R, G, B) tuple.
    """
    W, H = img_rgba.size
    pixels = img_rgba.load()
    samples = []
    for y in range(H):
        for dx in range(min(sample_width, W)):
            p = pixels[dx, y]
            if p[3] > ALPHA_THRESHOLD:
                samples.append(p[:3])
        for dx in range(min(sample_width, W)):
            x = W - 1 - dx
            p = pixels[x, y]
            if p[3] > ALPHA_THRESHOLD:
                samples.append(p[:3])
    for x in range(W):
        for dy in range(min(sample_width, H)):
            p = pixels[x, dy]
            if p[3] > ALPHA_THRESHOLD:
                samples.append(p[:3])
        for dy in range(min(sample_width, H)):
            y = H - 1 - dy
            p = pixels[x, y]
            if p[3] > ALPHA_THRESHOLD:
                samples.append(p[:3])
    if not samples:
        return (255, 255, 255)
    counter = collections.Counter(samples)
    return counter.most_common(1)[0][0]


def occupied_rows(img_rgba, bg_color):
    """
    Returns a list of booleans: True if row i is "occupied" (has enough
    non-background, non-transparent pixels).
    """
    W, H = img_rgba.size
    pixels = img_rgba.load()
    result = []
    for y in range(H):
        count = 0
        for x in range(W):
            p = pixels[x, y]
            if p[3] < ALPHA_THRESHOLD:
                continue
            if rgb_dist(p[:3], bg_color) > BG_DIST_THRESHOLD:
                count += 1
            if count >= DENSITY_THRESHOLD:
                break
        result.append(count >= DENSITY_THRESHOLD)
    return result


def find_character_extent(occ):
    """
    Given the boolean row occupancy list, return (top_row, bottom_row) or
    None if no occupied rows found.
    """
    tops = [i for i, v in enumerate(occ) if v]
    if not tops:
        return None
    return tops[0], tops[-1]


def find_head_height(occ, top_row):
    """
    Starting from top_row, find the first gap of >= HEAD_GAP_ROWS consecutive
    empty rows.  The head occupies rows [top_row, gap_start_row).
    Returns head_height (pixels) and a string describing the method used.
    """
    H = len(occ)
    consecutive_empty = 0
    gap_start = None
    for y in range(top_row, H):
        if not occ[y]:
            if consecutive_empty == 0:
                gap_start = y
            consecutive_empty += 1
            if consecutive_empty >= HEAD_GAP_ROWS:
                # gap_start is the first empty row of the gap
                return gap_start - top_row, "gap-detection"
        else:
            consecutive_empty = 0
            gap_start = None
    # No clear gap found — fall back
    return None, "no-gap"


# ─── Main report ─────────────────────────────────────────────────────────────

def proportion_report(png_path, bx, by, bw, bh,
                      eye_width_px=None, head_height_px_override=None):
    """
    Generate and return the text report.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("LTG Proportion Verifier v{0}".format(__version__))
    lines.append("=" * 60)
    lines.append("File   : {0}".format(png_path))
    lines.append("BBox   : x={0} y={1} w={2} h={3}".format(bx, by, bw, bh))
    lines.append("")

    # Load image
    try:
        img = Image.open(png_path).convert("RGBA")
    except Exception as e:
        lines.append("ERROR: Could not open image: {0}".format(e))
        return "\n".join(lines)

    W, H = img.size
    lines.append("Image size : {0}×{1}px".format(W, H))

    # Clamp bbox
    bx2 = max(0, min(bx, W))
    by2 = max(0, min(by, H))
    bx3 = max(0, min(bx + bw, W))
    by3 = max(0, min(by + bh, H))
    if bx3 <= bx2 or by3 <= by2:
        lines.append("ERROR: Bounding box is outside image bounds or zero-size.")
        return "\n".join(lines)

    crop = img.crop((bx2, by2, bx3, by3))
    lines.append("Crop size  : {0}×{1}px".format(crop.size[0], crop.size[1]))
    lines.append("")

    # Background detection
    bg = detect_background(crop)
    lines.append("Detected BG colour: RGB{0}".format(bg))
    lines.append("")

    # Row occupancy
    occ = occupied_rows(crop, bg)
    extent = find_character_extent(occ)

    if extent is None:
        lines.append("ERROR: No occupied rows found — bounding box may not contain a character.")
        return "\n".join(lines)

    top_row, bottom_row = extent
    total_height = bottom_row - top_row + 1
    lines.append("Character extent (within crop):")
    lines.append("  Top row    : {0}".format(top_row))
    lines.append("  Bottom row : {0}".format(bottom_row))
    lines.append("  Total h    : {0}px".format(total_height))
    lines.append("")

    # Head height
    if head_height_px_override is not None:
        head_height = head_height_px_override
        method = "user-supplied"
    else:
        head_height, method = find_head_height(occ, top_row)
        if head_height is None:
            # Fallback: estimate from canonical ratio
            head_height = int(round(total_height / CANONICAL_RATIO))
            method = "fallback-estimate (no neck gap detected)"
            lines.append("WARN: No neck gap detected — head height estimated from canonical ratio.")
            lines.append("      Consider supplying --hr <head_height_px> for a precise check.")
            lines.append("")

    lines.append("Head detection method: {0}".format(method))
    lines.append("Head height : {0}px".format(head_height))
    lines.append("")

    # ─── Metric 1: Head-to-body ratio ────────────────────────────────────
    lines.append("─" * 40)
    lines.append("METRIC 1 — Head-to-Body Ratio")
    lines.append("─" * 40)

    if head_height <= 0:
        lines.append("  WARN: Head height is zero — cannot compute ratio.")
        ratio = None
    else:
        ratio = total_height / head_height
        low  = CANONICAL_RATIO * (1 - RATIO_TOLERANCE)
        high = CANONICAL_RATIO * (1 + RATIO_TOLERANCE)
        pct_off = (ratio - CANONICAL_RATIO) / CANONICAL_RATIO * 100

        lines.append("  Measured ratio  : {0:.3f}  ({1}px / {2}px)".format(
            ratio, total_height, head_height))
        lines.append("  Canonical target: {0:.1f}  (±{1:.0f}%)".format(
            CANONICAL_RATIO, RATIO_TOLERANCE * 100))
        lines.append("  Acceptable range: {0:.3f} – {1:.3f}".format(low, high))
        lines.append("  Deviation       : {0:+.1f}%".format(pct_off))
        lines.append("")

        if method == "fallback-estimate (no neck gap detected)":
            lines.append("  RESULT: WARN — head height estimated (no neck gap); ratio measurement unreliable.")
        elif low <= ratio <= high:
            lines.append("  RESULT: PASS — ratio {0:.3f} is within ±5% of 3.2-head spec.".format(ratio))
        else:
            severity = "FAIL" if abs(pct_off) > 10 else "WARN"
            lines.append("  RESULT: {0} — ratio {1:.3f} deviates {2:+.1f}% from 3.2-head spec.".format(
                severity, ratio, pct_off))
    lines.append("")

    # ─── Metric 2: Eye-width / Head-height ratio ─────────────────────────
    lines.append("─" * 40)
    lines.append("METRIC 2 — Eye-Width / Head-Height Ratio")
    lines.append("─" * 40)

    if eye_width_px is None:
        lines.append("  SKIP — no --ew value supplied.")
    elif head_height is None or head_height <= 0:
        lines.append("  SKIP — head height unavailable.")
    else:
        ew_ratio = eye_width_px / head_height
        low_ew  = CANONICAL_EW_HR * (1 - EW_HR_TOLERANCE)
        high_ew = CANONICAL_EW_HR * (1 + EW_HR_TOLERANCE)
        pct_ew  = (ew_ratio - CANONICAL_EW_HR) / CANONICAL_EW_HR * 100

        lines.append("  Eye width       : {0}px".format(eye_width_px))
        lines.append("  Head height     : {0}px".format(head_height))
        lines.append("  Measured ew/HR  : {0:.4f}".format(ew_ratio))
        lines.append("  Canonical target: {0:.2f}  (±{1:.0f}%)".format(
            CANONICAL_EW_HR, EW_HR_TOLERANCE * 100))
        lines.append("  Acceptable range: {0:.4f} – {1:.4f}".format(low_ew, high_ew))
        lines.append("  Deviation       : {0:+.1f}%".format(pct_ew))
        lines.append("")

        if low_ew <= ew_ratio <= high_ew:
            lines.append("  RESULT: PASS — ew/HR {0:.4f} is within ±5% of canonical 0.22.".format(ew_ratio))
        else:
            severity = "FAIL" if abs(pct_ew) > 10 else "WARN"
            lines.append("  RESULT: {0} — ew/HR {1:.4f} deviates {2:+.1f}% from canonical 0.22.".format(
                severity, ew_ratio, pct_ew))
    lines.append("")

    lines.append("=" * 60)
    lines.append("END OF REPORT")
    lines.append("=" * 60)
    return "\n".join(lines)


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="LTG PNG proportion verifier — checks head-to-body ratio against 3.2-head spec."
    )
    parser.add_argument("png", help="Path to the PNG file to inspect.")
    parser.add_argument("x",   type=int, help="Bounding box left edge (px).")
    parser.add_argument("y",   type=int, help="Bounding box top edge (px).")
    parser.add_argument("w",   type=int, help="Bounding box width (px).")
    parser.add_argument("h",   type=int, help="Bounding box height (px).")
    parser.add_argument("--ew", type=float, default=None,
                        dest="eye_width_px",
                        help="Eye width in pixels — enables ew/HR ratio check.")
    parser.add_argument("--hr", type=float, default=None,
                        dest="head_height_px",
                        help="Override head height in pixels (skips auto-detect).")

    args = parser.parse_args()

    report = proportion_report(
        png_path=args.png,
        bx=args.x,
        by=args.y,
        bw=args.w,
        bh=args.h,
        eye_width_px=args.eye_width_px,
        head_height_px_override=args.head_height_px,
    )
    print(report)


if __name__ == "__main__":
    main()
