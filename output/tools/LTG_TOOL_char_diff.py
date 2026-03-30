#!/usr/bin/env python3
"""
LTG_TOOL_char_diff.py
Character Proportion Diff Tool — Luma & the Glitchkin

Given two character sheet PNGs (reference and candidate), samples pixels to
estimate key character proportion metrics and produces a diff report.

Metrics extracted:
  - head_height_px   : topmost dense non-background region height
  - figure_height_px : total non-background vertical span
  - head_body_ratio  : figure_height / head_height
  - eye_width_px     : widest horizontal dark feature in the head region
  - eye_head_ratio   : eye_width / head_height

Usage:
  python3 LTG_TOOL_char_diff.py reference.png candidate.png [x y w h]

  Optional bbox: x y w h — pixel bounding box (top-left corner x, y, width, height)
  to crop to a single character area within a multi-panel sheet.

Output:
  JSON report + human-readable PASS/WARN/FAIL summary printed to stdout.
  WARN = ±10% deviation from reference. FAIL = ±20% deviation.

Author: Maya Santos — C31 Ideabox Implementation
Date: 2026-03-29
"""

import sys
import json
from typing import Optional, Tuple
from PIL import Image


# ─── CONFIG ──────────────────────────────────────────────────────────────────

WARN_THRESHOLD = 0.10   # 10% deviation from reference → WARN
FAIL_THRESHOLD = 0.20   # 20% deviation from reference → FAIL

# Background detection: pixel is "background" if all channels within this
# tolerance of the detected background color.
BG_SAMPLE_REGION_SIZE = 20   # px square in corners used to determine BG color
BG_TOLERANCE = 30            # per-channel tolerance for "is background" test

# Minimum horizontal run of foreground pixels to count as a "figure row"
MIN_ROW_DENSITY = 0.04       # fraction of bbox width that must be foreground

# Minimum fraction of figure height for a region to count as the "head"
# The head is identified as the TOPMOST contiguous dense region before a gap
HEAD_GAP_MIN_PX = 3          # gap rows needed to separate head from body

# Dark feature detection for eye width
# We scan the head region for the widest horizontal run of "dark" pixels.
# "Dark" = all channels < DARK_THRESHOLD
DARK_THRESHOLD = 100         # pixels with ALL channels < this are candidate eye pixels
                              # 100 catches dark-brown lines after LANCZOS downsampling
MIN_EYE_RUN = 2              # minimum run of dark pixels to count as eye feature
MAX_EYE_FRACTION = 0.35      # max fraction of image width that a single eye run can be
                              # (runs wider than this are structural lines, not eyes)


# ─── IMAGE LOADING & CROPPING ────────────────────────────────────────────────

def load_region(path: str, bbox: Optional[Tuple]) -> Image.Image:
    """Load image and optionally crop to bbox (x, y, w, h)."""
    img = Image.open(path).convert("RGB")
    if bbox:
        x, y, w, h = bbox
        img = img.crop((x, y, x + w, y + h))
    return img


# ─── BACKGROUND COLOR DETECTION ──────────────────────────────────────────────

def detect_background_color(img: Image.Image) -> tuple:
    """
    Sample the four corners of the image to determine background color.
    Returns (R, G, B) as the median of corner samples.
    """
    w, h = img.size
    s = BG_SAMPLE_REGION_SIZE
    corners = [
        img.crop((0, 0, s, s)),
        img.crop((w - s, 0, w, s)),
        img.crop((0, h - s, s, h)),
        img.crop((w - s, h - s, w, h)),
    ]
    r_vals, g_vals, b_vals = [], [], []
    for corner in corners:
        pixels = list(corner.getdata())
        for r, g, b in pixels:
            r_vals.append(r)
            g_vals.append(g)
            b_vals.append(b)
    r_vals.sort(); g_vals.sort(); b_vals.sort()
    n = len(r_vals) // 2
    return (r_vals[n], g_vals[n], b_vals[n])


def is_background(pixel: tuple, bg: tuple, tol: int = BG_TOLERANCE) -> bool:
    """Return True if pixel is within tolerance of background color."""
    return all(abs(int(pixel[i]) - int(bg[i])) <= tol for i in range(3))


# ─── FIGURE DETECTION ────────────────────────────────────────────────────────

def get_row_foreground_counts(img: Image.Image, bg: tuple) -> list:
    """
    For each row, return count of non-background pixels.
    Returns list of ints, one per row.
    """
    w, h = img.size
    pixels = img.load()
    counts = []
    for y in range(h):
        count = 0
        for x in range(w):
            if not is_background(pixels[x, y], bg):
                count += 1
        counts.append(count)
    return counts


def find_figure_span(row_counts: list, img_width: int) -> tuple:
    """
    Find the topmost and bottommost rows with meaningful foreground content.
    Returns (top_row, bottom_row) inclusive, or (None, None) if not found.
    """
    threshold = max(1, int(img_width * MIN_ROW_DENSITY))
    top = None
    bottom = None
    for y, count in enumerate(row_counts):
        if count >= threshold:
            if top is None:
                top = y
            bottom = y
    return top, bottom


def find_head_span(row_counts: list, img_width: int, figure_top: int, figure_bottom: int) -> tuple:
    """
    Find the head region — topmost contiguous dense block of foreground rows
    before the first gap (HEAD_GAP_MIN_PX consecutive sparse rows).

    Returns (head_top, head_bottom) inclusive.
    """
    threshold = max(1, int(img_width * MIN_ROW_DENSITY))
    # Walk from figure_top downward; head ends at the first gap of HEAD_GAP_MIN_PX
    # consecutive sparse rows.
    head_top = figure_top
    head_bottom = figure_top
    gap_run = 0

    for y in range(figure_top, figure_bottom + 1):
        if row_counts[y] >= threshold:
            if gap_run == 0:
                # still in (or back in) the head region
                head_bottom = y
            else:
                # We are past the first gap — this is body territory
                break
            gap_run = 0
        else:
            gap_run += 1
            if gap_run >= HEAD_GAP_MIN_PX:
                break

    return head_top, head_bottom


# ─── EYE WIDTH DETECTION ─────────────────────────────────────────────────────

def estimate_eye_width(img: Image.Image, head_top: int, head_bottom: int) -> int:
    """
    Scan the head region for the widest horizontal run of dark pixels that
    plausibly represents an eye feature (capped at MAX_EYE_FRACTION of width).

    Returns width in pixels of the widest qualifying dark run found.

    Only scans the middle 50% of the head height (vertically) to avoid
    picking up the head outline or hair outlines at top/bottom.
    Runs wider than MAX_EYE_FRACTION of image width are skipped — these are
    structural lines (panel borders, label bars), not eyes.
    """
    w, _h = img.size
    pixels = img.load()
    max_eye_px = int(w * MAX_EYE_FRACTION)

    head_h = head_bottom - head_top
    scan_top = head_top + int(head_h * 0.25)
    scan_bot = head_top + int(head_h * 0.65)

    max_run = 0

    for y in range(scan_top, scan_bot + 1):
        run = 0
        run_start = 0
        for x in range(w):
            r, g, b = pixels[x, y]
            if r < DARK_THRESHOLD and g < DARK_THRESHOLD and b < DARK_THRESHOLD:
                if run == 0:
                    run_start = x
                run += 1
            else:
                if MIN_EYE_RUN <= run <= max_eye_px:
                    if run > max_run:
                        max_run = run
                run = 0
        # Handle run ending at edge
        if MIN_EYE_RUN <= run <= max_eye_px and run > max_run:
            max_run = run

    return max_run


# ─── METRIC EXTRACTION ───────────────────────────────────────────────────────

def extract_metrics(path: str, bbox: Optional[Tuple]) -> dict:
    """
    Load image (optionally cropped), detect background, and compute all metrics.
    Returns dict with keys: head_height_px, figure_height_px, head_body_ratio,
    eye_width_px, eye_head_ratio, image_size, bbox_used, bg_color.
    """
    img = load_region(path, bbox)
    w, h = img.size
    bg = detect_background_color(img)

    row_counts = get_row_foreground_counts(img, bg)
    fig_top, fig_bot = find_figure_span(row_counts, w)

    if fig_top is None:
        return {
            "error": "No figure detected — image may be all background or bbox is incorrect.",
            "image_size": [w, h],
            "bbox_used": bbox,
            "bg_color": list(bg),
        }

    figure_height_px = fig_bot - fig_top + 1
    head_top, head_bot = find_head_span(row_counts, w, fig_top, fig_bot)
    head_height_px = head_bot - head_top + 1

    # Safety: head must be at least 10% and not more than 60% of figure
    if head_height_px < max(5, int(figure_height_px * 0.10)):
        head_height_px = max(5, int(figure_height_px * 0.25))  # fallback estimate
    if head_height_px > int(figure_height_px * 0.60):
        head_height_px = int(figure_height_px * 0.35)

    head_body_ratio = round(figure_height_px / head_height_px, 3) if head_height_px > 0 else None

    eye_width_px = estimate_eye_width(img, head_top, head_top + head_height_px - 1)
    eye_head_ratio = round(eye_width_px / head_height_px, 3) if (head_height_px > 0 and eye_width_px > 0) else None

    return {
        "image_size": [w, h],
        "bbox_used": list(bbox) if bbox else None,
        "bg_color": list(bg),
        "figure_top_row": fig_top,
        "figure_bottom_row": fig_bot,
        "figure_height_px": figure_height_px,
        "head_top_row": head_top,
        "head_bottom_row": head_top + head_height_px - 1,
        "head_height_px": head_height_px,
        "head_body_ratio": head_body_ratio,
        "eye_width_px": eye_width_px,
        "eye_head_ratio": eye_head_ratio,
    }


# ─── DIFF & REPORTING ────────────────────────────────────────────────────────

METRICS_TO_COMPARE = [
    ("figure_height_px",  "Figure Height",       "px"),
    ("head_height_px",    "Head Height",          "px"),
    ("head_body_ratio",   "Head-to-Body Ratio",   "ratio"),
    ("eye_width_px",      "Eye Width",            "px"),
    ("eye_head_ratio",    "Eye-to-Head Ratio",    "ratio"),
]


def grade(ref_val, cand_val) -> tuple:
    """
    Compare candidate to reference.
    Returns (status, deviation_pct) where status is PASS / WARN / FAIL.
    """
    if ref_val is None or cand_val is None:
        return ("SKIP", None)
    if ref_val == 0:
        return ("SKIP", None)
    deviation = abs(cand_val - ref_val) / abs(ref_val)
    if deviation <= WARN_THRESHOLD:
        status = "PASS"
    elif deviation <= FAIL_THRESHOLD:
        status = "WARN"
    else:
        status = "FAIL"
    return (status, round(deviation * 100, 1))


def build_report(ref_metrics: dict, cand_metrics: dict, ref_path: str, cand_path: str) -> dict:
    """Build full JSON-compatible report dict."""
    report = {
        "tool": "LTG_TOOL_char_diff",
        "reference": ref_path,
        "candidate": cand_path,
        "thresholds": {
            "warn_pct": int(WARN_THRESHOLD * 100),
            "fail_pct": int(FAIL_THRESHOLD * 100),
        },
        "reference_metrics": ref_metrics,
        "candidate_metrics": cand_metrics,
        "diff": {},
    }

    for key, label, unit in METRICS_TO_COMPARE:
        ref_val = ref_metrics.get(key)
        cand_val = cand_metrics.get(key)
        status, dev_pct = grade(ref_val, cand_val)
        report["diff"][key] = {
            "label": label,
            "unit": unit,
            "reference": ref_val,
            "candidate": cand_val,
            "deviation_pct": dev_pct,
            "status": status,
        }

    # Overall result
    statuses = [v["status"] for v in report["diff"].values()]
    if "FAIL" in statuses:
        report["overall"] = "FAIL"
    elif "WARN" in statuses:
        report["overall"] = "WARN"
    elif all(s in ("PASS", "SKIP") for s in statuses):
        report["overall"] = "PASS"
    else:
        report["overall"] = "SKIP"

    return report


def print_human_summary(report: dict) -> None:
    """Print human-readable summary to stdout."""
    STATUS_ICONS = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]", "SKIP": "[SKIP]"}

    print()
    print("=" * 60)
    print("  LTG CHARACTER PROPORTION DIFF — v001")
    print("=" * 60)
    print(f"  REF  : {report['reference']}")
    print(f"  CAND : {report['candidate']}")
    print(f"  WARN at >{report['thresholds']['warn_pct']}% | FAIL at >{report['thresholds']['fail_pct']}%")
    print("-" * 60)

    ref_m = report["reference_metrics"]
    if "error" in ref_m:
        print(f"  ERROR (reference): {ref_m['error']}")
        return
    cand_m = report["candidate_metrics"]
    if "error" in cand_m:
        print(f"  ERROR (candidate): {cand_m['error']}")
        return

    print(f"  REF  image size : {ref_m['image_size'][0]}x{ref_m['image_size'][1]}  bbox: {ref_m['bbox_used']}")
    print(f"  CAND image size : {cand_m['image_size'][0]}x{cand_m['image_size'][1]}  bbox: {cand_m['bbox_used']}")
    print("-" * 60)
    print(f"  {'METRIC':<26} {'REF':>8} {'CAND':>8} {'DEV%':>7}  STATUS")
    print("-" * 60)

    for key, entry in report["diff"].items():
        icon = STATUS_ICONS.get(entry["status"], "[ ?? ]")
        ref_v  = f"{entry['reference']}" if entry['reference'] is not None else "N/A"
        cand_v = f"{entry['candidate']}" if entry['candidate'] is not None else "N/A"
        dev    = f"{entry['deviation_pct']:.1f}%" if entry['deviation_pct'] is not None else "—"
        label  = entry['label'][:26]
        print(f"  {label:<26} {ref_v:>8} {cand_v:>8} {dev:>7}  {icon}")

    print("-" * 60)
    overall_icon = STATUS_ICONS.get(report["overall"], "[ ?? ]")
    print(f"  OVERALL RESULT: {overall_icon}")
    print("=" * 60)
    print()


# ─── MAIN ────────────────────────────────────────────────────────────────────

def parse_args(argv: list) -> tuple:
    """Parse command-line arguments. Returns (ref_path, cand_path, bbox_or_None)."""
    if len(argv) < 3:
        print("Usage: python3 LTG_TOOL_char_diff.py reference.png candidate.png [x y w h]")
        sys.exit(1)
    ref_path = argv[1]
    cand_path = argv[2]
    bbox = None
    if len(argv) >= 7:
        try:
            bbox = (int(argv[3]), int(argv[4]), int(argv[5]), int(argv[6]))
        except ValueError:
            print("Error: bbox must be four integers: x y w h")
            sys.exit(1)
    return ref_path, cand_path, bbox


def main():
    ref_path, cand_path, bbox = parse_args(sys.argv)

    print(f"\nExtracting metrics from reference: {ref_path}")
    ref_metrics = extract_metrics(ref_path, bbox)

    print(f"Extracting metrics from candidate:  {cand_path}")
    cand_metrics = extract_metrics(cand_path, bbox)

    report = build_report(ref_metrics, cand_metrics, ref_path, cand_path)

    # JSON output
    print("\n--- JSON REPORT ---")
    print(json.dumps(report, indent=2))

    # Human-readable summary
    print_human_summary(report)

    # Exit code: 0=PASS, 1=WARN, 2=FAIL
    exit_codes = {"PASS": 0, "WARN": 1, "FAIL": 2, "SKIP": 0}
    sys.exit(exit_codes.get(report["overall"], 0))


if __name__ == "__main__":
    main()
