#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_expression_range_metric.py — v1.0.0 (Cycle 50, Kai Nakamura)

Expression Range Metric Tool.

For each expression sheet, measures how much the face region ACTUALLY CHANGES
between panels. Quantifies pixel-level difference magnitude to catch the problem
where expressions are labeled differently but look nearly identical.

Unlike expression_silhouette.py (which measures pose/silhouette similarity),
this tool focuses on the FACE REGION specifically and measures absolute
change magnitude — not just correlation.

Metrics per expression pair:
  1. Face Region Pixel Delta (FRPD):
     Mean absolute pixel difference in the face region (cropped to head zone).
     Normalized to 0.0-1.0 where 0.0 = identical, 1.0 = completely different.

  2. Structural Change Index (SCI):
     Fraction of face-region pixels that change by more than a noise threshold.
     Low SCI = only minor tonal shifts. High SCI = real structural change
     (eyebrows moved, mouth shape changed, eyes widened, etc.)

  3. Expression Range Score (ERS):
     Per-sheet aggregate: average FRPD across all unique pairs.
     Tells you "how expressive is this character's expression set overall."

Thresholds:
  Per-pair FRPD:
    FAIL < 0.03 — expressions are pixel-identical in face region
    WARN < 0.08 — very minor change (likely just color tint, not shape)
    PASS >= 0.08 — meaningful face change
  Per-pair SCI:
    FAIL < 0.05 — less than 5% of face pixels changed structurally
    WARN < 0.15 — weak structural change
    PASS >= 0.15 — real structural change

  Per-sheet ERS:
    FAIL < 0.05 — sheet has almost no expression range
    WARN < 0.10 — limited range
    PASS >= 0.10 — adequate range

Input: Expression sheet PNGs (grid layout).
Output: Per-pair and per-sheet metrics. Optional heatmap visualization.

Usage:
  python3 LTG_TOOL_expression_range_metric.py <expression_sheet.png>
          [--rows R] [--cols C]
          [--head-zone 0.40]
          [--noise-threshold 15]
          [--output heatmap.png]
          [--json]
          [--report path/to/report.md]

  --head-zone     Fraction of panel height considered "face region" (from top). Default 0.40.
  --noise-threshold  Per-channel pixel diff below this = noise, not structural change. Default 15.

Author: Kai Nakamura — Cycle 50
Date: 2026-03-30
"""

import sys
import os
import argparse
import json
import math
import numpy as np
from itertools import combinations
from PIL import Image, ImageDraw

# ─── CONFIG ──────────────────────────────────────────────────────────────────

BG_SAMPLE_SIZE = 8
BG_TOLERANCE = 45
MIN_CHAR_FRACTION = 0.01

# Head zone: top portion of panel treated as face region
DEFAULT_HEAD_ZONE = 0.40

# Noise threshold: per-channel pixel diff below this is noise
DEFAULT_NOISE_THRESHOLD = 15

# Per-pair thresholds
FRPD_FAIL = 0.03
FRPD_WARN = 0.08
SCI_FAIL = 0.05
SCI_WARN = 0.15

# Per-sheet ERS thresholds
ERS_FAIL = 0.05
ERS_WARN = 0.10

# Known grid sizes keyed by (width, height) → (rows, cols)
KNOWN_GRIDS = {
    (1200, 900): (3, 3),
    (1200, 800): (3, 2),
    (800, 800): (2, 2),
    (900, 600): (2, 3),
    (1200, 400): (1, 3),
    (712, 1280): (4, 3),
    (1182, 1114): (3, 3),  # Cosmo expression sheet
}


# ─── GRID DETECTION ─────────────────────────────────────────────────────────


def detect_grid(img, rows_override=None, cols_override=None):
    """Detect or use override for grid layout."""
    w, h = img.size
    if rows_override and cols_override:
        return rows_override, cols_override

    key = (w, h)
    if key in KNOWN_GRIDS:
        return KNOWN_GRIDS[key]

    # Heuristic: try common grids
    for r, c in [(3, 3), (2, 3), (3, 2), (2, 2), (4, 3), (1, 3)]:
        pw = w // c
        ph = h // r
        if pw >= 100 and ph >= 100:
            return r, c

    return 2, 3  # fallback


def extract_panels(img, rows, cols):
    """Split image into grid panels. Returns list of (label, PIL.Image)."""
    w, h = img.size
    pw = w // cols
    ph = h // rows
    panels = []
    idx = 0
    for r in range(rows):
        for c in range(cols):
            x0 = c * pw
            y0 = r * ph
            panel = img.crop((x0, y0, x0 + pw, y0 + ph))
            panels.append((f"P{idx}", panel))
            idx += 1
    return panels


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


def is_empty_panel(panel_img, bg_tolerance=BG_TOLERANCE):
    """Check if panel is mostly background (empty)."""
    bg = detect_background_color(panel_img)
    arr = np.array(panel_img.convert("RGB"), dtype=np.int16)
    bg_arr = np.array(bg, dtype=np.int16).reshape(1, 1, 3)
    diff = np.abs(arr - bg_arr)
    is_bg = np.all(diff <= bg_tolerance, axis=2)
    char_fraction = 1.0 - np.mean(is_bg)
    return char_fraction < MIN_CHAR_FRACTION


# ─── FACE REGION EXTRACTION ────────────────────────────────────────────────


def extract_face_region(panel_img, head_zone_frac=DEFAULT_HEAD_ZONE, bg_tolerance=BG_TOLERANCE):
    """Extract the face/head region from a panel.
    Takes the top `head_zone_frac` of the character's bounding box.
    Returns numpy array (RGB, float64, 0-1 range) or None if empty."""
    rgb = panel_img.convert("RGB")
    arr = np.array(rgb, dtype=np.int16)
    bg = detect_background_color(panel_img)
    bg_arr = np.array(bg, dtype=np.int16).reshape(1, 1, 3)

    diff = np.abs(arr - bg_arr)
    is_char = ~np.all(diff <= bg_tolerance, axis=2)

    rows_any = np.any(is_char, axis=1)
    if not np.any(rows_any):
        return None

    y_indices = np.where(rows_any)[0]
    y_top = y_indices[0]
    y_bot = y_indices[-1]
    char_height = y_bot - y_top + 1

    # Head zone
    head_bot = y_top + int(char_height * head_zone_frac)
    head_bot = min(head_bot, y_bot + 1)

    # Find horizontal extent in head zone
    head_region = is_char[y_top:head_bot, :]
    cols_any = np.any(head_region, axis=0)
    if not np.any(cols_any):
        return None

    x_indices = np.where(cols_any)[0]
    x_left = x_indices[0]
    x_right = x_indices[-1]

    face_arr = np.array(rgb, dtype=np.float64)[y_top:head_bot, x_left:x_right + 1, :] / 255.0
    return face_arr


def resize_to_match(arr_a, arr_b):
    """Resize both face arrays to same dimensions (use the smaller)."""
    h_a, w_a = arr_a.shape[:2]
    h_b, w_b = arr_b.shape[:2]
    h = min(h_a, h_b)
    w = min(w_a, w_b)
    if h < 4 or w < 4:
        return None, None

    img_a = Image.fromarray((arr_a * 255).astype(np.uint8))
    img_b = Image.fromarray((arr_b * 255).astype(np.uint8))
    img_a = img_a.resize((w, h), Image.BILINEAR)
    img_b = img_b.resize((w, h), Image.BILINEAR)

    return np.array(img_a, dtype=np.float64) / 255.0, np.array(img_b, dtype=np.float64) / 255.0


# ─── METRICS ────────────────────────────────────────────────────────────────


def face_region_pixel_delta(face_a, face_b):
    """FRPD: Mean absolute pixel difference in face region, normalized to 0-1."""
    a, b = resize_to_match(face_a, face_b)
    if a is None:
        return 0.0
    diff = np.abs(a - b)
    return float(np.mean(diff))


def structural_change_index(face_a, face_b, noise_threshold=DEFAULT_NOISE_THRESHOLD):
    """SCI: Fraction of face pixels with per-channel diff > noise threshold."""
    a, b = resize_to_match(face_a, face_b)
    if a is None:
        return 0.0
    diff = np.abs(a - b) * 255.0  # Back to 0-255 for threshold comparison
    # A pixel counts as "structurally changed" if ANY channel exceeds threshold
    changed = np.any(diff > noise_threshold, axis=2)
    return float(np.mean(changed))


def pair_verdict(frpd, sci):
    """Determine verdict for an expression pair."""
    if frpd < FRPD_FAIL or sci < SCI_FAIL:
        return "FAIL"
    elif frpd < FRPD_WARN or sci < SCI_WARN:
        return "WARN"
    return "PASS"


def ers_verdict(ers):
    if ers < ERS_FAIL:
        return "FAIL"
    elif ers < ERS_WARN:
        return "WARN"
    return "PASS"


# ─── ANALYSIS ───────────────────────────────────────────────────────────────


def analyze_expression_sheet(filepath, rows=None, cols=None, head_zone=DEFAULT_HEAD_ZONE,
                              noise_threshold=DEFAULT_NOISE_THRESHOLD):
    """Analyze a single expression sheet. Returns results dict."""
    img = Image.open(filepath).convert("RGB")
    r, c = detect_grid(img, rows, cols)
    panels = extract_panels(img, r, c)

    # Filter empty panels
    valid_panels = []
    for label, panel in panels:
        if not is_empty_panel(panel):
            face = extract_face_region(panel, head_zone)
            if face is not None:
                valid_panels.append((label, panel, face))

    if len(valid_panels) < 2:
        return {
            "file": os.path.basename(filepath),
            "grid": f"{r}x{c}",
            "valid_panels": len(valid_panels),
            "error": "Need at least 2 non-empty panels with detectable faces",
            "pairs": [],
            "ers": 0.0,
            "ers_verdict": "FAIL",
        }

    # Pairwise analysis
    pairs = []
    frpd_values = []

    for i, j in combinations(range(len(valid_panels)), 2):
        label_a, _, face_a = valid_panels[i]
        label_b, _, face_b = valid_panels[j]

        frpd = face_region_pixel_delta(face_a, face_b)
        sci = structural_change_index(face_a, face_b, noise_threshold)
        v = pair_verdict(frpd, sci)
        frpd_values.append(frpd)

        pairs.append({
            "pair": f"{label_a} vs {label_b}",
            "frpd": round(frpd, 4),
            "sci": round(sci, 4),
            "verdict": v,
        })

    ers = float(np.mean(frpd_values)) if frpd_values else 0.0

    fail_count = sum(1 for p in pairs if p["verdict"] == "FAIL")
    warn_count = sum(1 for p in pairs if p["verdict"] == "WARN")
    pass_count = sum(1 for p in pairs if p["verdict"] == "PASS")

    return {
        "file": os.path.basename(filepath),
        "grid": f"{r}x{c}",
        "valid_panels": len(valid_panels),
        "pairs": pairs,
        "ers": round(ers, 4),
        "ers_verdict": ers_verdict(ers),
        "summary": {
            "total_pairs": len(pairs),
            "pass": pass_count,
            "warn": warn_count,
            "fail": fail_count,
        },
    }


def analyze_batch(filepaths, rows=None, cols=None, head_zone=DEFAULT_HEAD_ZONE,
                  noise_threshold=DEFAULT_NOISE_THRESHOLD):
    """Analyze multiple expression sheets."""
    results = []
    for fp in filepaths:
        try:
            result = analyze_expression_sheet(fp, rows, cols, head_zone, noise_threshold)
            results.append(result)
        except Exception as e:
            results.append({"file": os.path.basename(fp), "error": str(e)})
    return results


# ─── HEATMAP VISUALIZATION ──────────────────────────────────────────────────


def generate_diff_heatmap(filepath, output_path, rows=None, cols=None,
                          head_zone=DEFAULT_HEAD_ZONE):
    """Generate a heatmap showing face region differences between all panels.
    The heatmap contact sheet shows the absolute diff amplified for visibility."""
    img = Image.open(filepath).convert("RGB")
    r, c = detect_grid(img, rows, cols)
    panels = extract_panels(img, r, c)

    valid = []
    for label, panel in panels:
        if not is_empty_panel(panel):
            face = extract_face_region(panel, head_zone)
            if face is not None:
                valid.append((label, face))

    if len(valid) < 2:
        return None

    # Build a grid of diff heatmaps: n*(n-1)/2 cells
    n = len(valid)
    n_pairs = n * (n - 1) // 2
    cols_out = min(n_pairs, 4)
    rows_out = math.ceil(n_pairs / cols_out)

    # Determine cell size from first face
    ref_h, ref_w = valid[0][1].shape[:2]
    cell_w = min(ref_w, 200)
    cell_h = min(ref_h, 200)
    label_h = 20
    margin = 5

    sheet_w = margin + cols_out * (cell_w + margin)
    sheet_h = margin + rows_out * (cell_h + label_h + margin)

    if sheet_w > 1280:
        sheet_w = 1280
    if sheet_h > 1280:
        sheet_h = 1280

    sheet = Image.new("RGB", (sheet_w, sheet_h), (40, 40, 40))
    draw = ImageDraw.Draw(sheet)

    idx = 0
    for i, j in combinations(range(n), 2):
        label_a, face_a = valid[i]
        label_b, face_b = valid[j]

        a, b = resize_to_match(face_a, face_b)
        if a is None:
            idx += 1
            continue

        diff = np.abs(a - b)
        # Amplify for visibility: multiply by 4, clamp to 1.0
        amplified = np.clip(diff * 4.0, 0.0, 1.0)
        heatmap = (amplified * 255).astype(np.uint8)
        heat_img = Image.fromarray(heatmap).resize((cell_w, cell_h), Image.BILINEAR)

        row = idx // cols_out
        col = idx % cols_out
        x = margin + col * (cell_w + margin)
        y = margin + row * (cell_h + label_h + margin)

        if y + label_h + cell_h <= sheet_h and x + cell_w <= sheet_w:
            draw.text((x + 2, y), f"{label_a}-{label_b}", fill=(255, 255, 255))
            sheet.paste(heat_img, (x, y + label_h))
            draw = ImageDraw.Draw(sheet)

        idx += 1

    sheet.save(output_path)
    return output_path


# ─── TEXT REPORT ─────────────────────────────────────────────────────────────


def format_report(results_list):
    """Format batch results as text."""
    lines = []
    lines.append("=" * 70)
    lines.append("EXPRESSION RANGE METRIC REPORT")
    lines.append("=" * 70)

    for result in results_list:
        lines.append("")
        lines.append(f"--- {result['file']} ---")
        if "error" in result:
            lines.append(f"  ERROR: {result['error']}")
            continue

        lines.append(f"  Grid: {result['grid']} | Valid panels: {result['valid_panels']}")
        lines.append(f"  Expression Range Score (ERS): {result['ers']:.4f} [{result['ers_verdict']}]")

        for pair in result.get("pairs", []):
            v = pair["verdict"]
            flag = " <<<" if v in ("FAIL", "WARN") else ""
            lines.append(f"  {pair['pair']}: FRPD={pair['frpd']:.4f} SCI={pair['sci']:.4f} [{v}]{flag}")

        summary = result.get("summary", {})
        lines.append(f"  Pairs: PASS={summary.get('pass', 0)} WARN={summary.get('warn', 0)} "
                     f"FAIL={summary.get('fail', 0)}")

    lines.append("")
    lines.append("=" * 70)
    return "\n".join(lines)


def format_markdown_report(results_list):
    """Format batch results as markdown."""
    lines = []
    lines.append("# Expression Range Metric Report")
    lines.append("")

    for result in results_list:
        lines.append(f"## {result['file']}")
        if "error" in result:
            lines.append(f"**Error:** {result['error']}")
            lines.append("")
            continue

        lines.append(f"**Grid:** {result['grid']} | **Valid panels:** {result['valid_panels']}")
        lines.append(f"**Expression Range Score (ERS):** {result['ers']:.4f} **[{result['ers_verdict']}]**")
        lines.append("")

        if result.get("pairs"):
            lines.append("| Pair | FRPD | SCI | Verdict |")
            lines.append("|------|------|-----|---------|")
            for pair in result["pairs"]:
                lines.append(f"| {pair['pair']} | {pair['frpd']:.4f} | {pair['sci']:.4f} | {pair['verdict']} |")
            lines.append("")

    lines.append("## Metric Definitions")
    lines.append("- **FRPD** (Face Region Pixel Delta): Mean absolute pixel difference in face. 0=identical, 1=totally different.")
    lines.append("- **SCI** (Structural Change Index): Fraction of face pixels with per-channel diff > noise threshold.")
    lines.append("- **ERS** (Expression Range Score): Average FRPD across all pairs. Aggregate expressiveness.")
    lines.append(f"- **FRPD thresholds**: FAIL < {FRPD_FAIL}, WARN < {FRPD_WARN}, PASS >= {FRPD_WARN}")
    lines.append(f"- **SCI thresholds**: FAIL < {SCI_FAIL}, WARN < {SCI_WARN}, PASS >= {SCI_WARN}")
    lines.append(f"- **ERS thresholds**: FAIL < {ERS_FAIL}, WARN < {ERS_WARN}, PASS >= {ERS_WARN}")
    return "\n".join(lines)


# ─── CLI ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Expression Range Metric Tool")
    parser.add_argument("inputs", nargs="+", help="Expression sheet PNG(s)")
    parser.add_argument("--rows", type=int, help="Grid rows override")
    parser.add_argument("--cols", type=int, help="Grid cols override")
    parser.add_argument("--head-zone", type=float, default=DEFAULT_HEAD_ZONE,
                        help=f"Face region fraction (default {DEFAULT_HEAD_ZONE})")
    parser.add_argument("--noise-threshold", type=int, default=DEFAULT_NOISE_THRESHOLD,
                        help=f"Noise threshold per channel (default {DEFAULT_NOISE_THRESHOLD})")
    parser.add_argument("--output", help="Diff heatmap output path (first sheet only)")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--report", help="Write markdown report to file")
    args = parser.parse_args()

    filepaths = [f for f in args.inputs if os.path.isfile(f)]
    if not filepaths:
        print("ERROR: No valid input files.", file=sys.stderr)
        sys.exit(1)

    results = analyze_batch(filepaths, args.rows, args.cols,
                            args.head_zone, args.noise_threshold)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_report(results))

    if args.output and filepaths:
        generate_diff_heatmap(filepaths[0], args.output, args.rows, args.cols, args.head_zone)
        print(f"\nHeatmap saved: {args.output}")

    if args.report:
        md = format_markdown_report(results)
        os.makedirs(os.path.dirname(args.report) or ".", exist_ok=True)
        with open(args.report, "w") as f:
            f.write(md)
        print(f"Report saved: {args.report}")

    # Exit code
    any_fail = any(r.get("ers_verdict") == "FAIL" or "error" in r for r in results)
    any_warn = any(r.get("ers_verdict") == "WARN" for r in results)
    if any_fail:
        sys.exit(2)
    elif any_warn:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
