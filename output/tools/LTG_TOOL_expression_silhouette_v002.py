#!/usr/bin/env python3
"""
LTG_TOOL_expression_silhouette_v002.py
Expression Silhouette Differentiation Test — v002 (Cycle 34, Maya Santos)

Adds --mode flag with two modes:
  full  (default) — full-panel silhouette comparison (v001 behaviour)
  arms             — isolates the arm/shoulder region of each panel and compares
                     only that cropped zone. Identifies which expression pairs
                     differ in body language vs face only.

Algorithm (full mode):
  1. Detect panel grid (rows × cols) from expression sheet.
  2. For each panel: crop the panel, detect background color (border sampling),
     classify background pixels by tolerance → binary silhouette.
  3. For each pair of panels: compute combined similarity =
       0.6 × IoM + 0.4 × XOR_similarity
  4. Flag pairs exceeding FAIL/WARN thresholds.

Algorithm (arms mode):
  Same as full mode through step 2, then:
  2b. From each panel silhouette, extract the arm/shoulder region by cropping
      a horizontal band spanning panel_y [ARMS_TOP_FRAC … ARMS_BOT_FRAC].
      This band contains the torso-to-waist region where arms are typically
      visible; the head (top) and legs (bottom) are excluded.
      Within this band, the left and right arm zones (outside CENTER_MASK_FRAC
      of the band width) are preserved while the body center is masked to white
      (background) to eliminate the shared body column from the comparison.
  3. Compute combined similarity on the cropped arm-region silhouettes.

The arm/shoulder crop constants are tuned for LTG full-body character panels
at 1200×900 (3×3 grid) with characters occupying roughly the central 80% of
panel height. They can be overridden via --arms-top / --arms-bot / --center-mask.

Usage:
  python3 LTG_TOOL_expression_silhouette_v002.py expression_sheet.png
          [--rows R] [--cols C]
          [--mode full|arms]
          [--arms-top 0.20] [--arms-bot 0.70] [--center-mask 0.28]
          [--threshold 0.85] [--warn-threshold 0.72]
          [--output silhouettes.png] [--json]

  --mode arms   Isolates arm/shoulder region — identifies body-language
                differences vs face-only differences.

  --arms-top    Fraction of panel height where arm region starts (default 0.20).
  --arms-bot    Fraction of panel height where arm region ends (default 0.70).
  --center-mask Fraction of panel width to mask from center (body trunk excluded).
                Set to 0.0 to keep full width (default 0.28).

Auto-detects rows/cols from common LTG sheet sizes. Override with --rows / --cols.

Output:
  - Text PASS/WARN/FAIL report to stdout.
  - Optional: silhouette contact sheet PNG showing arm-region crops.
  - JSON output via --json flag.
  - Exit codes: 0=PASS, 1=WARN, 2=FAIL.

Author: Maya Santos — Cycle 34 Task 1 (C33 Ideabox --mode arms extension)
Date: 2026-03-29
"""

import sys
import os
import argparse
import json
from itertools import combinations
from PIL import Image, ImageDraw


# ─── CONFIG ──────────────────────────────────────────────────────────────────

FAIL_THRESHOLD      = 0.85   # similarity above this → FAIL pair
WARN_THRESHOLD      = 0.72   # similarity above this → WARN pair
BG_SAMPLE_SIZE      = 8      # px square at corners for BG detection
BG_TOLERANCE        = 45     # per-channel tolerance for background classification
MIN_CHAR_FRACTION   = 0.01   # if silhouette occupies < 1% of panel → likely empty, skip
PAD_FRACTION        = 0.03   # fraction of panel to ignore as padding on each edge

# Arms-mode region defaults (fractions of panel height/width)
ARMS_TOP_FRAC       = 0.20   # arm region starts here (20% down — below head top)
ARMS_BOT_FRAC       = 0.70   # arm region ends here (70% down — above legs)
CENTER_MASK_FRAC    = 0.28   # mask this fraction of center width (body trunk excluded)

# Known grid sizes keyed by (width, height) → (rows, cols)
KNOWN_GRIDS = {
    (1200, 900):  (3, 3),
    (1200, 800):  (3, 2),
    (800, 800):   (2, 2),
    (900, 600):   (2, 3),
    (1200, 400):  (1, 3),
    (712, 1280):  (4, 3),   # Byte v005 vertical sheet
}


# ─── GRID DETECTION ──────────────────────────────────────────────────────────

def detect_grid(img: Image.Image, rows_override=None, cols_override=None):
    """Return (rows, cols, panel_w, panel_h, pad_x, pad_y, header_h) for image."""
    w, h = img.size
    rows = rows_override or KNOWN_GRIDS.get((w, h), (None, None))[0] or 3
    cols = cols_override or KNOWN_GRIDS.get((w, h), (None, None))[1] or 3

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
    """Detect the per-panel background color via corner sampling."""
    arr = panel.load()
    w, h = panel.size
    s = BG_SAMPLE_SIZE

    tl_samples = [arr[x, y][:3] for x in range(min(s, w)) for y in range(min(s, h))]
    bl_samples = [arr[x, y][:3] for x in range(min(s, w)) for y in range(max(0, h - s), h)]
    br_samples = [arr[x, y][:3] for x in range(max(0, w - s), w) for y in range(max(0, h - s), h)]

    all_samples = tl_samples + bl_samples + br_samples

    if all_samples:
        r_vals = sorted(p[0] for p in all_samples)
        g_vals = sorted(p[1] for p in all_samples)
        b_vals = sorted(p[2] for p in all_samples)
        mid = len(r_vals) // 2
        corner_bg = (r_vals[mid], g_vals[mid], b_vals[mid])
    else:
        corner_bg = sheet_bg or (235, 224, 206)

    return corner_bg


def make_silhouette(panel: Image.Image, sheet_bg: tuple = None) -> Image.Image:
    """
    Convert a single panel into a binary (black=character, white=background) silhouette.
    """
    rgb = panel.convert("RGB")
    w, h = rgb.size

    bg_color = detect_panel_bg(rgb, sheet_bg)

    pix = rgb.load()
    sil = Image.new("L", (w, h), 255)   # white background
    sil_arr = sil.load()

    for y in range(h):
        for x in range(w):
            p = pix[x, y][:3]
            is_panel_bg = _is_bg(p, bg_color)
            is_sheet_bg = sheet_bg and _is_bg(p, sheet_bg)
            if not is_panel_bg and not is_sheet_bg:
                sil_arr[x, y] = 0   # character pixel → black

    return sil  # 0=character (black), 255=background (white)


def crop_arm_region(sil: Image.Image,
                    arms_top_frac: float = ARMS_TOP_FRAC,
                    arms_bot_frac: float = ARMS_BOT_FRAC,
                    center_mask_frac: float = CENTER_MASK_FRAC) -> Image.Image:
    """
    Extract the arm/shoulder region from a full-panel silhouette.

    Crops a horizontal band spanning [arms_top_frac … arms_bot_frac] of panel
    height. This preserves the torso-to-waist region where arm silhouettes live
    while excluding the head (top) and legs (bottom).

    Within the band, masks the central body trunk (center ± center_mask_frac/2
    of band width) to white, so the comparison focuses on the arm extensions
    rather than the shared trunk mass.

    Algorithm detail: after masking the trunk, the comparison operates on the
    outer arm zones only. The metric is more meaningful when CENTER_MASK_FRAC
    is set wide enough to fully exclude the shared torso column. Typical torso
    occupies ~25–35% of panel width for LTG characters; a mask of 0.28 partially
    covers it. For cleaner arm-only comparison use --center-mask 0.36.

    Parameters:
      arms_top_frac    — fraction of panel height where arm band starts (default 0.20)
      arms_bot_frac    — fraction of panel height where arm band ends (default 0.70)
      center_mask_frac — fraction of band width to mask from center (default 0.28)
                         Set to 0.0 to preserve full width.
                         Set to 0.36 for tighter torso exclusion.

    Returns a new L-mode Image containing only the arm region.
    """
    w, h = sil.size
    top = int(h * arms_top_frac)
    bot = int(h * arms_bot_frac)
    top = max(0, top)
    bot = min(h, bot)

    # Crop the band
    arm_band = sil.crop((0, top, w, bot))

    # Optionally mask body trunk (center column)
    if center_mask_frac > 0:
        bw, bh = arm_band.size
        center_x = bw // 2
        mask_half = int(bw * center_mask_frac / 2)
        mask_left  = max(0, center_x - mask_half)
        mask_right = min(bw, center_x + mask_half)

        arr = arm_band.load()
        for y in range(bh):
            for x in range(mask_left, mask_right):
                arr[x, y] = 255  # erase trunk → background

    return arm_band


def silhouette_area(sil: Image.Image) -> int:
    """Count black (character) pixels."""
    arr = sil.load()
    w, h = sil.size
    return sum(1 for y in range(h) for x in range(w) if arr[x, y] == 0)


def silhouette_intersection(sil_a: Image.Image, sil_b: Image.Image) -> int:
    """Count pixels that are black in BOTH silhouettes."""
    wa, ha = sil_a.size
    wb, hb = sil_b.size
    if (wa, ha) != (wb, hb):
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
    XOR similarity: 1.0 = identical, 0.0 = completely different.
    Low value = distinct (good). High value = too similar (bad).
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
        if (a_arr[x, y] < 128) != (b_arr[x, y] < 128)
    )
    xor_fraction = differ / total
    return 1.0 - xor_fraction  # 0=distinct, 1=identical


def combined_similarity(sil_a: Image.Image, sil_b: Image.Image) -> float:
    """
    Combined similarity: 0.6 × IoM + 0.4 × XOR_similarity.
    Higher = more similar (problematic). FAIL ≥ 0.85, WARN ≥ 0.72.
    """
    iom = iom_score(sil_a, sil_b)
    xor_sim = xor_similarity(sil_a, sil_b)
    return 0.6 * iom + 0.4 * xor_sim


# ─── CONTACT SHEET ───────────────────────────────────────────────────────────

def make_silhouette_contact_sheet(silhouettes: list, rows: int, cols: int,
                                   panel_w: int, panel_h: int,
                                   labels: list = None,
                                   mode: str = "full") -> Image.Image:
    """
    Build a contact sheet PNG showing all silhouettes in a grid.
    In arms mode, each cell shows the arm-region crop (will be shorter than
    the original panel height).
    """
    LABEL_H = 22
    PAD = 8
    mode_label = f"Mode: {mode.upper()}"
    total_w = cols * (panel_w + PAD) + PAD
    total_h = rows * (panel_h + LABEL_H + PAD) + PAD + 46  # 46 for title + mode line
    out = Image.new("RGB", (total_w, total_h), (245, 245, 245))
    draw = ImageDraw.Draw(out)

    draw.text((PAD, 6),  "Expression Silhouette Differentiation Test", fill=(30, 30, 30))
    draw.text((PAD, 24), mode_label, fill=(80, 80, 180))

    for idx, sil in enumerate(silhouettes):
        r = idx // cols
        c = idx % cols
        x0 = PAD + c * (panel_w + PAD)
        y0 = 46 + PAD + r * (panel_h + LABEL_H + PAD)
        # Scale sil to fit panel cell
        sil_rgb = sil.convert("RGB")
        sil_rgb = sil_rgb.resize((panel_w, panel_h), Image.LANCZOS)
        out.paste(sil_rgb, (x0, y0))
        label = labels[idx] if labels and idx < len(labels) else f"P{idx:02d}"
        draw.text((x0, y0 + panel_h + 2), label[:22], fill=(60, 60, 60))

    out.thumbnail((1280, 1280), Image.LANCZOS)
    return out


# ─── MAIN TEST RUNNER ────────────────────────────────────────────────────────

def run_test(sheet_path: str,
             rows_override=None,
             cols_override=None,
             fail_threshold=FAIL_THRESHOLD,
             warn_threshold=WARN_THRESHOLD,
             output_path=None,
             verbose=True,
             mode: str = "full",
             arms_top_frac: float = ARMS_TOP_FRAC,
             arms_bot_frac: float = ARMS_BOT_FRAC,
             center_mask_frac: float = CENTER_MASK_FRAC) -> dict:
    """
    Run silhouette differentiation test on an expression sheet.

    Parameters:
      mode          — "full" (default) or "arms"
                      full: compares complete panel silhouettes (v001 behaviour)
                      arms: compares only the arm/shoulder region of each panel,
                            helping identify body-language vs face-only differences.

      arms_top_frac — start of arm region (fraction of panel height, default 0.20)
      arms_bot_frac — end of arm region (fraction of panel height, default 0.70)
      center_mask_frac — fraction of band width masked from center (default 0.28)

    Returns dict with keys:
      sheet, rows, cols, panel_count, active_panels, mode,
      pairs (list of {panel_a, panel_b, iom, status}),
      overall, worst_iom, worst_pair
    """
    if mode not in ("full", "arms"):
        raise ValueError(f"Unknown mode: {mode!r}. Use 'full' or 'arms'.")

    img = Image.open(sheet_path).convert("RGB")

    rows, cols, panel_w, panel_h, pad_x, pad_y, header_h = detect_grid(
        img, rows_override, cols_override
    )

    panels = extract_panels(img, rows, cols, panel_w, panel_h, pad_x, pad_y, header_h)

    silhouettes = []        # full silhouettes (for contact sheet reference)
    compare_sils = []       # silhouettes used for comparison (full or arm crops)
    panel_labels = []
    active_indices = []

    sheet_bg = _sample_bg(img)

    for idx, r, c, panel in panels:
        sil = make_silhouette(panel, sheet_bg=sheet_bg)
        area = silhouette_area(sil)
        panel_area = panel.width * panel.height
        fill_fraction = area / panel_area if panel_area > 0 else 0
        is_active = fill_fraction >= MIN_CHAR_FRACTION

        silhouettes.append(sil)

        # For arms mode, derive the comparison silhouette from the arm region
        if mode == "arms":
            cmp_sil = crop_arm_region(sil, arms_top_frac, arms_bot_frac, center_mask_frac)
        else:
            cmp_sil = sil

        compare_sils.append(cmp_sil)
        panel_labels.append(f"P{idx:02d} R{r}C{c}")
        if is_active:
            active_indices.append(idx)

    # Compare all active pairs on the appropriate silhouettes
    pair_results = []
    worst_iom = 0.0
    worst_pair = None

    for i, j in combinations(active_indices, 2):
        score = combined_similarity(compare_sils[i], compare_sils[j])
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
        "mode": mode,
        "pairs": pair_results,
        "overall": overall,
        "worst_iom": round(worst_iom, 4),
        "worst_pair": worst_pair,
    }

    if mode == "arms":
        result["arms_region"] = {
            "top_frac": arms_top_frac,
            "bot_frac": arms_bot_frac,
            "center_mask_frac": center_mask_frac,
        }

    if verbose:
        _print_report(result, fail_threshold, warn_threshold, mode)

    if output_path:
        # In arms mode, show the arm-region crops; in full mode show full silhouettes
        display_sils = compare_sils if mode == "arms" else silhouettes
        arm_h = int(panel_h * (arms_bot_frac - arms_top_frac)) if mode == "arms" else panel_h
        contact = make_silhouette_contact_sheet(
            display_sils, rows, cols, panel_w, arm_h if mode == "arms" else panel_h,
            panel_labels, mode=mode
        )
        contact.save(output_path)
        if verbose:
            print(f"\nSilhouette contact sheet saved: {output_path}")

    return result


def _print_report(result: dict, fail_threshold: float, warn_threshold: float,
                  mode: str = "full"):
    print("=" * 60)
    print(f"EXPRESSION SILHOUETTE DIFFERENTIATION TEST")
    print(f"Mode:         {mode.upper()}", end="")
    if mode == "arms" and "arms_region" in result:
        ar = result["arms_region"]
        print(f"  (top={ar['top_frac']:.0%}, bot={ar['bot_frac']:.0%}, "
              f"center_mask={ar['center_mask_frac']:.0%})")
    else:
        print()
    print(f"Sheet:        {result['sheet']}")
    print(f"Grid:         {result['rows']}×{result['cols']} "
          f"({result['panel_count']} panels, {result['active_panels']} active)")
    print(f"Thresholds:   WARN ≥ {warn_threshold:.0%}  FAIL ≥ {fail_threshold:.0%}")
    print("-" * 60)

    if mode == "arms":
        print("Comparing arm/shoulder region only (body trunk masked).")
        print("PASS = arms differ in shape; FAIL = arms identical (face-only expression).")
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
        description=(
            "LTG Expression Silhouette Differentiation Test v002.\n\n"
            "Compares expression panel silhouettes to ensure body-language\n"
            "differentiation. Two modes:\n"
            "  full  — full panel comparison (default, v001 behaviour)\n"
            "  arms  — isolates arm/shoulder region to identify face-only\n"
            "          expressions that share identical body language.\n\n"
            "Arms mode crops each panel to [--arms-top … --arms-bot] of panel\n"
            "height and optionally masks the central body trunk with --center-mask."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("sheet", help="Path to expression sheet PNG")
    parser.add_argument("--rows", type=int, default=None,
                        help="Override row count (auto-detected from image size)")
    parser.add_argument("--cols", type=int, default=None,
                        help="Override column count (auto-detected from image size)")
    parser.add_argument(
        "--mode", choices=["full", "arms"], default="full",
        help=(
            "Comparison mode. 'full' = full panel (default). "
            "'arms' = arm/shoulder region only. "
            "Use 'arms' to identify face-only expressions with identical body language."
        ),
    )
    parser.add_argument(
        "--arms-top", type=float, default=ARMS_TOP_FRAC, metavar="FRAC",
        help=(
            f"Arms mode: top of arm region as fraction of panel height "
            f"(default {ARMS_TOP_FRAC}). 0.0 = panel top."
        ),
    )
    parser.add_argument(
        "--arms-bot", type=float, default=ARMS_BOT_FRAC, metavar="FRAC",
        help=(
            f"Arms mode: bottom of arm region as fraction of panel height "
            f"(default {ARMS_BOT_FRAC}). 1.0 = panel bottom."
        ),
    )
    parser.add_argument(
        "--center-mask", type=float, default=CENTER_MASK_FRAC, metavar="FRAC",
        help=(
            f"Arms mode: fraction of band width masked from center to exclude body trunk "
            f"(default {CENTER_MASK_FRAC}). Set 0.0 to disable masking."
        ),
    )
    parser.add_argument("--threshold", type=float, default=FAIL_THRESHOLD,
                        help=f"Similarity fail threshold (default {FAIL_THRESHOLD})")
    parser.add_argument("--warn-threshold", type=float, default=WARN_THRESHOLD,
                        help=f"Similarity warn threshold (default {WARN_THRESHOLD})")
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
        mode=args.mode,
        arms_top_frac=args.arms_top,
        arms_bot_frac=args.arms_bot,
        center_mask_frac=args.center_mask,
    )

    if args.json:
        print(json.dumps(result, indent=2))

    if result["overall"] == "FAIL":
        sys.exit(2)
    elif result["overall"] == "WARN":
        sys.exit(1)
    else:
        sys.exit(0)
