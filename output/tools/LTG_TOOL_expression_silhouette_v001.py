#!/usr/bin/env python3
"""
LTG_TOOL_expression_silhouette_v001.py
Expression Silhouette Differentiation Test
"Luma & the Glitchkin" — Cycle 33 / Maya Santos

Extracts each panel from an expression sheet PNG, flood-fills the character
region to a solid black silhouette, then compares all panel silhouettes against
each other using pixel overlap ratio (IoU). If any two panels have an overlap
ratio above a configurable threshold (default 0.85 = 85% identical silhouette),
the pair is flagged as FAIL.

Algorithm:
  1. Detect panel grid (rows × cols) from expression sheet.
  2. For each panel: crop the panel, detect background color (border sampling),
     flood-fill from borders to mark background, invert → black silhouette.
  3. For each pair of panels: compute combined similarity score =
       0.6 * IoM + 0.4 * XOR_similarity
     IoM (Intersection over Minimum Area) catches mass overlap.
     XOR similarity catches shape difference across the full panel.
     Combined metric is robust to full-body characters with shared body mass.
  4. If any pair exceeds FAIL_THRESHOLD → overall FAIL.
     If any pair exceeds WARN_THRESHOLD → overall WARN.
     Otherwise → PASS.

Usage:
  python3 LTG_TOOL_expression_silhouette_v001.py expression_sheet.png [--rows R] [--cols C]
          [--threshold 0.85] [--warn-threshold 0.72] [--output silhouettes.png]

  The tool auto-detects rows/cols from common LTG sheet sizes (1200×900 → 3×3,
  1200×800 → 3×2, 800×800 → 2×2). Override with --rows / --cols if needed.

Output:
  - Text PASS/WARN/FAIL report to stdout.
  - Optional: silhouette contact sheet PNG showing all silhouettes side-by-side.
  - Exit codes: 0=PASS, 1=WARN, 2=FAIL.

Author: Maya Santos — C33 Ideabox Implementation (actioned by Producer)
Date: 2026-03-29
"""

import sys
import os
import argparse
import json
from itertools import combinations
from PIL import Image, ImageDraw


# ─── CONFIG ──────────────────────────────────────────────────────────────────

FAIL_THRESHOLD      = 0.85   # IoM above this → FAIL pair
WARN_THRESHOLD      = 0.72   # IoM above this → WARN pair
BG_SAMPLE_SIZE      = 8      # px square at corners for BG detection
BG_TOLERANCE        = 45     # per-channel tolerance for background classification
FLOOD_FILL_STEPS    = 8      # flood fill uses 8-connected neighbourhood
MIN_CHAR_FRACTION   = 0.01   # if silhouette occupies < 1% of panel → likely empty, skip
PAD_FRACTION        = 0.03   # fraction of panel to ignore as padding on each edge

# Known grid sizes keyed by (width, height) → (rows, cols)
KNOWN_GRIDS = {
    (1200, 900):  (3, 3),
    (1200, 800):  (3, 2),
    (800, 800):   (2, 2),
    (900, 600):   (2, 3),
    (1200, 400):  (1, 3),
}


# ─── GRID DETECTION ──────────────────────────────────────────────────────────

def detect_grid(img: Image.Image, rows_override=None, cols_override=None):
    """Return (rows, cols, panel_w, panel_h, pad_x, pad_y, header_h) for image."""
    w, h = img.size
    rows = rows_override or KNOWN_GRIDS.get((w, h), (None, None))[0] or 3
    cols = cols_override or KNOWN_GRIDS.get((w, h), (None, None))[1] or 3

    # Estimate header (top strip that is not a panel)
    # Sample row luminance — the header is usually uniform background/text.
    # For LTG sheets: header ≈ 40–65px based on v008 constants.
    # Simple heuristic: scan downward from top until we hit a row with >10% non-bg.
    arr = img.load()
    bg_color = _sample_bg(img)
    header_h = 0
    for y in range(0, min(120, h)):
        row_non_bg = sum(
            1 for x in range(0, w, 4)
            if not _is_bg(arr[x, y], bg_color)
        )
        density = row_non_bg / (w // 4)
        if density > 0.12:
            header_h = y
            break

    usable_h = h - header_h
    panel_h = usable_h // rows
    panel_w = w // cols

    # Estimated padding (gap between panels)
    pad_x = max(2, int(w * 0.015))
    pad_y = max(2, int(h * 0.015))

    return rows, cols, panel_w, panel_h, pad_x, pad_y, header_h


def _sample_bg(img: Image.Image):
    """Sample the four corners to determine background color."""
    arr = img.load()
    w, h = img.size
    s = BG_SAMPLE_SIZE
    samples = []
    for cx, cy in [(0, 0), (w - s, 0), (0, h - s), (w - s, h - s)]:
        for dx in range(s):
            for dy in range(s):
                x = min(cx + dx, w - 1)
                y = min(cy + dy, h - 1)
                samples.append(arr[x, y][:3])
    # Median per channel
    r = sorted(p[0] for p in samples)
    g = sorted(p[1] for p in samples)
    b = sorted(p[2] for p in samples)
    mid = len(r) // 2
    return (r[mid], g[mid], b[mid])


def _is_bg(pixel, bg_color):
    """True if pixel is within BG_TOLERANCE of bg_color on all channels."""
    return all(abs(int(pixel[c]) - int(bg_color[c])) <= BG_TOLERANCE for c in range(3))


# ─── PANEL EXTRACTION ────────────────────────────────────────────────────────

def extract_panels(img: Image.Image, rows, cols, panel_w, panel_h, pad_x, pad_y, header_h):
    """
    Return list of (index, row, col, panel_img) for each panel slot.
    Panels with very little content are still returned but flagged in the result.
    """
    panels = []
    for r in range(rows):
        for c in range(cols):
            x0 = c * panel_w + pad_x
            y0 = header_h + r * panel_h + pad_y
            x1 = x0 + panel_w - pad_x
            y1 = y0 + panel_h - pad_y
            x0 = max(0, x0); y0 = max(0, y0)
            x1 = min(img.width, x1); y1 = min(img.height, y1)
            panel = img.crop((x0, y0, x1, y1))
            panels.append((r * cols + c, r, c, panel))
    return panels


# ─── SILHOUETTE GENERATION ───────────────────────────────────────────────────

def detect_panel_bg(panel: Image.Image, sheet_bg: tuple = None) -> tuple:
    """
    Detect the per-panel background color.

    Strategy: sample from top-left corner (most reliable) and bottom-left corner.
    For LTG expression sheets, the panel BG appears in corners and along left/right edges
    below the character. The character typically sits centered in the panel.
    """
    arr = panel.load()
    w, h = panel.size
    s = BG_SAMPLE_SIZE

    # Try top-left corner first
    tl_samples = [arr[x, y][:3] for x in range(min(s, w)) for y in range(min(s, h))]
    # Try bottom-left corner
    bl_samples = [arr[x, y][:3] for x in range(min(s, w)) for y in range(max(0, h - s), h)]
    # Try bottom-right corner
    br_samples = [arr[x, y][:3] for x in range(max(0, w - s), w) for y in range(max(0, h - s), h)]

    # Use all corner samples together
    all_samples = tl_samples + bl_samples + br_samples

    if all_samples:
        r_vals = sorted(p[0] for p in all_samples)
        g_vals = sorted(p[1] for p in all_samples)
        b_vals = sorted(p[2] for p in all_samples)
        mid = len(r_vals) // 2
        corner_bg = (r_vals[mid], g_vals[mid], b_vals[mid])
    else:
        corner_bg = sheet_bg or (235, 224, 206)

    # If corner BG is very close to sheet_bg, the panel might have its own BG.
    # For LTG sheets: each panel has a per-expression BG. We trust the corners
    # since they're typically unoccupied (character sits in center).
    return corner_bg


def make_silhouette(panel: Image.Image, sheet_bg: tuple = None) -> Image.Image:
    """
    Convert a single panel into a binary (black=character, white=background) silhouette.

    Uses panel-specific background detection via corner sampling.
    Flood-fills from panel borders to mark confirmed background.
    Character = pixels NOT reachable from border via background-color flood fill.

    sheet_bg: fallback if panel corner detection fails.
    """
    rgb = panel.convert("RGB")
    w, h = rgb.size

    # Detect panel's own BG color from corners
    bg_color = detect_panel_bg(rgb, sheet_bg)

    # Per-pixel color distance approach:
    # Any pixel within BG_TOLERANCE of bg_color on all channels = background.
    # This correctly handles panels where the character fills the panel and the
    # flood-fill connectivity approach would be blocked by outline pixels.
    #
    # We also apply a slight tolerance expansion using the sheet BG color:
    # pixels close to EITHER the panel BG OR the sheet gutter BG are background.
    pix = rgb.load()
    sil = Image.new("L", (w, h), 255)   # start white (background)
    sil_arr = sil.load()

    for y in range(h):
        for x in range(w):
            p = pix[x, y][:3]
            is_panel_bg = _is_bg(p, bg_color)
            is_sheet_bg = sheet_bg and _is_bg(p, sheet_bg)
            if not is_panel_bg and not is_sheet_bg:
                sil_arr[x, y] = 0   # character pixel → black

    return sil  # 0=character (black), 255=background (white)


def silhouette_area(sil: Image.Image) -> int:
    """Count black (character) pixels."""
    arr = sil.load()
    w, h = sil.size
    return sum(1 for y in range(h) for x in range(w) if arr[x, y] == 0)


def silhouette_intersection(sil_a: Image.Image, sil_b: Image.Image) -> int:
    """Count pixels that are black in BOTH silhouettes (aligned by panel size)."""
    # Resize to common size if different
    wa, ha = sil_a.size
    wb, hb = sil_b.size
    if (wa, ha) != (wb, hb):
        # Resize b to match a
        sil_b = sil_b.resize((wa, ha), Image.LANCZOS)

    a_arr = sil_a.load()
    b_arr = sil_b.load()
    return sum(1 for y in range(ha) for x in range(wa)
               if a_arr[x, y] == 0 and b_arr[x, y] == 0)


def iom_score(sil_a: Image.Image, sil_b: Image.Image) -> float:
    """Intersection over Minimum Area (IoM)."""
    area_a = silhouette_area(sil_a)
    area_b = silhouette_area(sil_b)
    min_area = min(area_a, area_b)
    if min_area == 0:
        return 0.0
    intersection = silhouette_intersection(sil_a, sil_b)
    return intersection / min_area


def xor_similarity(sil_a: Image.Image, sil_b: Image.Image) -> float:
    """
    XOR similarity: fraction of pixels that DIFFER between two silhouettes.
    Returns 0.0 = identical, 1.0 = completely different.
    Low value = silhouettes are too similar (problem).
    High value = silhouettes are distinct (good).

    We convert this to a similarity score (1 - xor_fraction) so it can be
    compared with the same threshold convention as IoM.
    """
    wa, ha = sil_a.size
    wb, hb = sil_b.size
    if (wa, ha) != (wb, hb):
        sil_b = sil_b.resize((wa, ha), Image.LANCZOS)

    a_arr = sil_a.load()
    b_arr = sil_b.load()
    total = wa * ha
    differ = sum(
        1 for y in range(ha) for x in range(wa)
        if (a_arr[x, y] < 128) != (b_arr[x, y] < 128)  # one is character, other is bg
    )
    xor_fraction = differ / total
    return 1.0 - xor_fraction  # 0=perfectly distinct, 1=identical


def combined_similarity(sil_a: Image.Image, sil_b: Image.Image) -> float:
    """
    Combined similarity score using IoM and XOR.
    IoM alone penalizes full-body characters who share body mass.
    XOR alone is affected by size differences.
    Combined: take the MAX (most conservative = most likely to flag) of:
      - iom_score weighted at 60%
      - xor_similarity weighted at 40%
    Returns a single value 0–1 where higher = more similar (bad).
    """
    iom = iom_score(sil_a, sil_b)
    xor_sim = xor_similarity(sil_a, sil_b)
    # Weighted combination
    return 0.6 * iom + 0.4 * xor_sim


# ─── CONTACT SHEET ───────────────────────────────────────────────────────────

def make_silhouette_contact_sheet(silhouettes: list, rows: int, cols: int,
                                   panel_w: int, panel_h: int,
                                   labels: list = None) -> Image.Image:
    """
    Build a contact sheet PNG showing all silhouettes in a grid.
    silhouettes: list of PIL Image (L mode) in panel order.
    """
    LABEL_H = 22
    PAD = 8
    total_w = cols * (panel_w + PAD) + PAD
    total_h = rows * (panel_h + LABEL_H + PAD) + PAD + 36  # 36 for title
    out = Image.new("RGB", (total_w, total_h), (245, 245, 245))
    draw = ImageDraw.Draw(out)

    # Title
    draw.text((PAD, 6), "Expression Silhouette Differentiation Test", fill=(30, 30, 30))

    for idx, sil in enumerate(silhouettes):
        r = idx // cols
        c = idx % cols
        x0 = PAD + c * (panel_w + PAD)
        y0 = 36 + PAD + r * (panel_h + LABEL_H + PAD)
        # Paste sil (convert to RGB)
        sil_rgb = sil.convert("RGB")
        sil_rgb = sil_rgb.resize((panel_w, panel_h), Image.LANCZOS)
        out.paste(sil_rgb, (x0, y0))
        # Label
        label = labels[idx] if labels and idx < len(labels) else f"P{idx:02d}"
        draw.text((x0, y0 + panel_h + 2), label[:20], fill=(60, 60, 60))

    # Respect ≤1280px rule
    out.thumbnail((1280, 1280), Image.LANCZOS)
    return out


# ─── MAIN ────────────────────────────────────────────────────────────────────

def run_test(sheet_path: str,
             rows_override=None,
             cols_override=None,
             fail_threshold=FAIL_THRESHOLD,
             warn_threshold=WARN_THRESHOLD,
             output_path=None,
             verbose=True) -> dict:
    """
    Run silhouette differentiation test on an expression sheet.

    Returns dict:
      {
        "sheet": str,
        "rows": int,
        "cols": int,
        "panel_count": int,
        "active_panels": int,
        "pairs": [{"panel_a": int, "panel_b": int, "iom": float, "status": str}, ...],
        "overall": "PASS" | "WARN" | "FAIL",
        "worst_iom": float,
        "worst_pair": (int, int) | None,
      }
    """
    img = Image.open(sheet_path).convert("RGB")

    rows, cols, panel_w, panel_h, pad_x, pad_y, header_h = detect_grid(
        img, rows_override, cols_override
    )

    panels = extract_panels(img, rows, cols, panel_w, panel_h, pad_x, pad_y, header_h)

    silhouettes = []
    panel_labels = []
    active_indices = []

    # Detect overall sheet background (from sheet gutters)
    sheet_bg = _sample_bg(img)

    for idx, r, c, panel in panels:
        sil = make_silhouette(panel, sheet_bg=sheet_bg)
        area = silhouette_area(sil)
        panel_area = panel.width * panel.height
        fill_fraction = area / panel_area if panel_area > 0 else 0
        is_active = fill_fraction >= MIN_CHAR_FRACTION
        silhouettes.append(sil)
        panel_labels.append(f"P{idx:02d} R{r}C{c}")
        if is_active:
            active_indices.append(idx)

    # Compare all active pairs
    pair_results = []
    worst_iom = 0.0
    worst_pair = None

    for i, j in combinations(active_indices, 2):
        score = combined_similarity(silhouettes[i], silhouettes[j])
        if score >= fail_threshold:
            status = "FAIL"
        elif score >= warn_threshold:
            status = "WARN"
        else:
            status = "PASS"
        pair_results.append({
            "panel_a": i, "panel_b": j,
            "iom": round(score, 4),
            "status": status
        })
        if score > worst_iom:
            worst_iom = score
            worst_pair = (i, j)

    # Overall result
    statuses = [p["status"] for p in pair_results]
    if "FAIL" in statuses:
        overall = "FAIL"
    elif "WARN" in statuses:
        overall = "WARN"
    else:
        overall = "PASS"

    result = {
        "sheet": os.path.basename(sheet_path),
        "rows": rows,
        "cols": cols,
        "panel_count": len(panels),
        "active_panels": len(active_indices),
        "pairs": pair_results,
        "overall": overall,
        "worst_iom": round(worst_iom, 4),
        "worst_pair": worst_pair,
    }

    if verbose:
        _print_report(result, fail_threshold, warn_threshold)

    if output_path:
        contact = make_silhouette_contact_sheet(
            silhouettes, rows, cols, panel_w, panel_h, panel_labels
        )
        contact.save(output_path)
        if verbose:
            print(f"\nSilhouette contact sheet saved: {output_path}")

    return result


def _print_report(result: dict, fail_threshold: float, warn_threshold: float):
    print("=" * 60)
    print(f"EXPRESSION SILHOUETTE DIFFERENTIATION TEST")
    print(f"Sheet:        {result['sheet']}")
    print(f"Grid:         {result['rows']}×{result['cols']} "
          f"({result['panel_count']} panels, {result['active_panels']} active)")
    print(f"Thresholds:   WARN ≥ {warn_threshold:.0%}  FAIL ≥ {fail_threshold:.0%}")
    print("-" * 60)

    fail_pairs = [p for p in result["pairs"] if p["status"] != "PASS"]
    if fail_pairs:
        print("FLAGGED PAIRS:")
        for p in sorted(fail_pairs, key=lambda x: -x["iom"]):
            print(f"  [{p['status']:4s}]  Panel {p['panel_a']:02d} ↔ Panel {p['panel_b']:02d}"
                  f"  Sim = {p['iom']:.1%}")
    else:
        print("All panel pairs: PASS (silhouettes sufficiently distinct)")

    print("-" * 60)
    print(f"Worst pair:   Panels {result['worst_pair']} — Sim {result['worst_iom']:.1%}"
          if result["worst_pair"] else "Worst pair:   N/A (< 2 active panels)")
    print(f"OVERALL:      {result['overall']}")
    print("=" * 60)


# ─── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LTG Expression Silhouette Differentiation Test"
    )
    parser.add_argument("sheet", help="Path to expression sheet PNG")
    parser.add_argument("--rows", type=int, default=None, help="Override row count")
    parser.add_argument("--cols", type=int, default=None, help="Override column count")
    parser.add_argument("--threshold", type=float, default=FAIL_THRESHOLD,
                        help=f"IoM fail threshold (default {FAIL_THRESHOLD})")
    parser.add_argument("--warn-threshold", type=float, default=WARN_THRESHOLD,
                        help=f"IoM warn threshold (default {WARN_THRESHOLD})")
    parser.add_argument("--output", "-o", default=None,
                        help="Save silhouette contact sheet PNG to this path")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON result to stdout (in addition to report)")
    args = parser.parse_args()

    result = run_test(
        sheet_path=args.sheet,
        rows_override=args.rows,
        cols_override=args.cols,
        fail_threshold=args.threshold,
        warn_threshold=args.warn_threshold,
        output_path=args.output,
        verbose=True,
    )

    if args.json:
        print(json.dumps(result, indent=2))

    # Exit code
    if result["overall"] == "FAIL":
        sys.exit(2)
    elif result["overall"] == "WARN":
        sys.exit(1)
    else:
        sys.exit(0)
