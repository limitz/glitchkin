#!/usr/bin/env python3
"""
LTG_TOOL_expression_silhouette_v003.py
Expression Silhouette Differentiation Test — v003 (Cycle 36, Maya Santos)

BREAKING CHANGE from v002:
  The IoM (Intersection over Minimum) metric used in v001/v002 is BROKEN for
  human characters. Because a standing figure always contains a shared torso
  column, if one silhouette is a geometric subset of the other, IoM reports
  100% similarity — even if the arms are in completely different positions.
  This is a mathematical bias, not a design defect.

NEW METRIC — Regional Pose Delta (RPD):
  Divides each panel silhouette into three horizontal zones:
    HEAD zone     — top 25% of silhouette bounding box height
    ARMS zone     — middle 50% (torso/waist where arms attach and extend)
    LEGS zone     — bottom 25% (stance, leg spread, footing)

  For each zone, computes a column-projection histogram (vertical sum of
  character pixels per x-column). The histogram captures where mass extends
  left/right, which encodes arm extension, lean, stance, etc.

  Zone similarity = normalized cross-correlation of the two histograms
  (high correlation = similar shape in that zone).

  Combined similarity = weighted average of zone similarities:
    RPD = 0.35×HEAD + 0.45×ARMS + 0.20×LEGS

  Weighting rationale:
    ARMS gets the most weight (0.45) — arm position is the primary
    expression differentiator; a wide arm vs tucked arm vs raised arm all
    read differently in silhouette.
    HEAD gets 0.35 — head tilt, turn, and profile are the secondary
    differentiator; face direction encodes expression quality.
    LEGS gets 0.20 — stance (spread, lean, pivot) contributes but is
    less expressive than arms or head.

  Unlike IoM, RPD is NOT biased by subset relationships. Two poses with
  identical trunks but different arm extensions will produce low ARMS
  correlation (low similarity = good differentiation), correctly reading
  as distinct.

Arms mode (--mode arms):
  Isolates only the ARMS zone (same 50% horizontal band as in full-mode
  ARMS zone). Applies center masking (--center-mask, default 0.30) to
  remove the shared torso column before computing the column projection.
  This gives the cleanest arm-only comparison.

  In arms mode, similarity is computed as column-projection correlation
  on the masked arm band only (no HEAD or LEGS contribution).

Thresholds (updated for RPD metric):
  FAIL  ≥ 0.85  — expressions too similar; must redesign pose
  WARN  ≥ 0.70  — marginally distinct; consider a bolder arm/head difference
  PASS  < 0.70  — expressions read as distinct in silhouette

Usage:
  python3 LTG_TOOL_expression_silhouette_v003.py expression_sheet.png
          [--rows R] [--cols C]
          [--mode full|arms]
          [--arms-top 0.25] [--arms-bot 0.75] [--center-mask 0.30]
          [--threshold 0.85] [--warn-threshold 0.70]
          [--output silhouettes.png] [--json] [--output-zones] [--viz-rpd]

  --mode arms     Isolates arm/shoulder region only (no HEAD/LEGS contribution).
  --arms-top      Top of arm zone as fraction of bounding-box height (default 0.25).
  --arms-bot      Bottom of arm zone as fraction of bounding-box height (default 0.75).
  --center-mask   Fraction of band width masked from center (trunk exclusion, default 0.30).
  --output-zones  Adds colored zone overlay bars to the --output contact sheet (full mode only):
                    HEAD zone = blue left bar (top 25%)
                    ARMS zone = orange left bar (middle 50%)
                    LEGS zone = green left bar (bottom 25%)
                  Helps designers instantly see which zone drove a WARN/FAIL result.
                  Added in C37 (actioned ideabox idea, Maya Santos).

Auto-detects rows/cols from common LTG sheet sizes. Override with --rows / --cols.

Output:
  - Text PASS/WARN/FAIL report to stdout.
  - Optional: silhouette contact sheet PNG showing zone overlays.
  - JSON output via --json flag.
  - Exit codes: 0=PASS, 1=WARN, 2=FAIL.

Author: Maya Santos — Cycle 36 Task 1 (C35 IoM metric root-cause fix)
Date: 2026-03-30
  --viz-rpd   For each FAIL/WARN pair, generates a side-by-side pixel difference
              heatmap PNG showing exactly which pixels differ between the two
              silhouettes, colorized by zone contribution:
                HEAD zone pixels = blue tint
                ARMS zone pixels = orange tint
                LEGS zone pixels = green tint
              Panel A pixels only = bright red overlay
              Panel B pixels only = bright cyan overlay
              Shared pixels = light grey
              Output: <--output-base>_pair_XX_YY_vizdiff.png per flagged pair.
              Requires --output (used as base path for generated files).
              Added in C39 (actioned ideabox, Maya Santos).

Author: Maya Santos — Cycle 36 Task 1 (C35 IoM metric root-cause fix)
  --viz-rpd added: Cycle 39 (actioned ideabox idea, Maya Santos)
Date: 2026-03-30
"""

import sys
import os
import argparse
import json
import math
from itertools import combinations
from PIL import Image, ImageDraw


# ─── CONFIG ──────────────────────────────────────────────────────────────────

FAIL_THRESHOLD      = 0.85   # RPD similarity above this → FAIL pair
WARN_THRESHOLD      = 0.70   # RPD similarity above this → WARN pair
BG_SAMPLE_SIZE      = 8      # px square at corners for BG detection
BG_TOLERANCE        = 45     # per-channel tolerance for background classification
MIN_CHAR_FRACTION   = 0.01   # if silhouette occupies < 1% of panel → skip (empty)
PAD_FRACTION        = 0.03   # fraction of panel to ignore as padding

# Zone weights for RPD metric (must sum to 1.0)
WEIGHT_HEAD  = 0.35
WEIGHT_ARMS  = 0.45
WEIGHT_LEGS  = 0.20

# Zone boundaries as fractions of silhouette BOUNDING BOX height
# (measured from the top of the bounding box, not panel top)
ZONE_HEAD_TOP  = 0.00
ZONE_HEAD_BOT  = 0.25
ZONE_ARMS_TOP  = 0.25
ZONE_ARMS_BOT  = 0.75
ZONE_LEGS_TOP  = 0.75
ZONE_LEGS_BOT  = 1.00

# Arms mode defaults
ARMS_TOP_FRAC       = 0.25   # arm region starts here (fraction of panel height)
ARMS_BOT_FRAC       = 0.75   # arm region ends here
CENTER_MASK_FRAC    = 0.30   # fraction of band width to mask from center

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
    """Return (rows, cols, panel_w, panel_h, pad_x, pad_y, header_h)."""
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

def extract_panels(img, rows, cols, panel_w, panel_h, pad_x, pad_y, header_h):
    """Return list of (index, row, col, panel_img) for each panel slot."""
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
    Convert a single panel into a binary (0=character/black, 255=background/white)
    silhouette image.
    """
    rgb = panel.convert("RGB")
    w, h = rgb.size
    bg_color = detect_panel_bg(rgb, sheet_bg)

    pix = rgb.load()
    sil = Image.new("L", (w, h), 255)
    sil_arr = sil.load()

    for y in range(h):
        for x in range(w):
            p = pix[x, y][:3]
            is_panel_bg = _is_bg(p, bg_color)
            is_sheet_bg = sheet_bg and _is_bg(p, sheet_bg)
            if not is_panel_bg and not is_sheet_bg:
                sil_arr[x, y] = 0  # character pixel

    return sil


def silhouette_area(sil: Image.Image) -> int:
    """Count black (character) pixels."""
    arr = sil.load()
    w, h = sil.size
    return sum(1 for y in range(h) for x in range(w) if arr[x, y] == 0)


# ─── BOUNDING BOX ────────────────────────────────────────────────────────────

def bounding_box(sil: Image.Image):
    """
    Return (x_min, y_min, x_max, y_max) of character pixels in the silhouette.
    Returns None if no character pixels found.
    """
    arr = sil.load()
    w, h = sil.size
    xs = [x for y in range(h) for x in range(w) if arr[x, y] == 0]
    ys = [y for y in range(h) for x in range(w) if arr[x, y] == 0]
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


# ─── COLUMN PROJECTION HISTOGRAM ─────────────────────────────────────────────

def column_projection(sil: Image.Image, y_top: int, y_bot: int,
                      x_left: int = 0, x_right: int = None,
                      center_mask_frac: float = 0.0) -> list:
    """
    Compute a column-projection histogram over the region [y_top..y_bot, x_left..x_right].
    Each bin = count of character pixels in that x-column within the y range.

    center_mask_frac: if > 0, zero out the central fraction of columns (trunk exclusion).

    Returns a list of floats (normalized so max=1.0, or all zeros if empty).
    """
    arr = sil.load()
    w, h = sil.size
    if x_right is None:
        x_right = w

    y_top = max(0, y_top)
    y_bot = min(h, y_bot)
    x_left = max(0, x_left)
    x_right = min(w, x_right)

    ncols = x_right - x_left
    if ncols <= 0 or y_bot <= y_top:
        return []

    hist = [0.0] * ncols
    for x in range(x_left, x_right):
        count = sum(1 for y in range(y_top, y_bot) if arr[x, y] == 0)
        hist[x - x_left] = float(count)

    # Apply center mask (trunk exclusion)
    if center_mask_frac > 0.0:
        center = ncols // 2
        half_mask = int(ncols * center_mask_frac / 2)
        for i in range(max(0, center - half_mask), min(ncols, center + half_mask)):
            hist[i] = 0.0

    # Normalize
    max_val = max(hist) if hist else 0.0
    if max_val > 0:
        hist = [v / max_val for v in hist]

    return hist


# ─── HISTOGRAM CORRELATION ───────────────────────────────────────────────────

def histogram_correlation(hist_a: list, hist_b: list) -> float:
    """
    Normalized cross-correlation between two 1D histograms.
    Returns a value in [0.0, 1.0]:
      1.0 = histograms are identical shape
      0.0 = completely uncorrelated

    If either histogram is all-zero (no character pixels in zone),
    returns 1.0 (treat as "same empty zone" — no pose difference detectable).

    Algorithm: Pearson correlation clamped to [0, 1].
    Negative correlation is treated as 0 (no-similarity bonus for inverted shapes).
    """
    n = len(hist_a)
    if n == 0 or len(hist_b) != n:
        # Mismatched lengths — resample b to length of a
        if len(hist_b) == 0 or n == 0:
            return 1.0
        # Simple linear resampling
        hist_b = _resample(hist_b, n)

    sum_a = sum(hist_a)
    sum_b = sum(hist_b)
    if sum_a == 0 and sum_b == 0:
        return 1.0  # both empty zones — indistinguishable (no info)
    if sum_a == 0 or sum_b == 0:
        return 0.0  # one has content, other is empty — maximally different

    mean_a = sum_a / n
    mean_b = sum_b / n

    num = sum((a - mean_a) * (b - mean_b) for a, b in zip(hist_a, hist_b))
    var_a = sum((a - mean_a) ** 2 for a in hist_a)
    var_b = sum((b - mean_b) ** 2 for b in hist_b)

    denom = math.sqrt(var_a * var_b)
    if denom < 1e-9:
        # Both histograms are flat (constant) — correlation undefined
        # Treat as similar (both constant → same structural zone)
        return 1.0

    pearson = num / denom
    # Clamp to [0, 1]: negative correlation = distinct = 0 similarity
    return max(0.0, min(1.0, pearson))


def _resample(hist: list, target_len: int) -> list:
    """Linear resampling of a histogram to a new length."""
    n = len(hist)
    if n == 0:
        return [0.0] * target_len
    result = []
    for i in range(target_len):
        src_f = i * (n - 1) / max(1, target_len - 1)
        src_i = int(src_f)
        frac = src_f - src_i
        if src_i + 1 < n:
            result.append(hist[src_i] * (1 - frac) + hist[src_i + 1] * frac)
        else:
            result.append(hist[src_i])
    return result


# ─── REGIONAL POSE DELTA (RPD) ───────────────────────────────────────────────

def rpd_similarity_full(sil_a: Image.Image, sil_b: Image.Image) -> dict:
    """
    Compute Regional Pose Delta (RPD) similarity between two full-panel silhouettes.

    Divides each silhouette into three zones based on bounding box:
      HEAD zone  — ZONE_HEAD_TOP .. ZONE_HEAD_BOT of bounding box height
      ARMS zone  — ZONE_ARMS_TOP .. ZONE_ARMS_BOT of bounding box height
      LEGS zone  — ZONE_LEGS_TOP .. ZONE_LEGS_BOT of bounding box height

    For each zone: column projection histogram → Pearson correlation.
    Combined RPD = WEIGHT_HEAD×HEAD + WEIGHT_ARMS×ARMS + WEIGHT_LEGS×LEGS.

    Returns dict with keys:
      head_sim, arms_sim, legs_sim, combined
    where combined is the RPD score (0=distinct, 1=identical).
    """
    # Normalize both silhouettes to the same size
    wa, ha = sil_a.size
    wb, hb = sil_b.size
    if (wa, ha) != (wb, hb):
        sil_b = sil_b.resize((wa, ha), Image.LANCZOS)

    # Get bounding boxes
    bb_a = bounding_box(sil_a)
    bb_b = bounding_box(sil_b)

    if bb_a is None or bb_b is None:
        return {"head_sim": 1.0, "arms_sim": 1.0, "legs_sim": 1.0, "combined": 1.0}

    # Use the union bounding box so both characters are measured in the same coordinate space
    x_min = min(bb_a[0], bb_b[0])
    y_min = min(bb_a[1], bb_b[1])
    x_max = max(bb_a[2], bb_b[2])
    y_max = max(bb_a[3], bb_b[3])
    bb_h = y_max - y_min
    if bb_h <= 0:
        return {"head_sim": 1.0, "arms_sim": 1.0, "legs_sim": 1.0, "combined": 1.0}

    # Zone y-bounds (absolute pixel positions)
    head_top = y_min + int(bb_h * ZONE_HEAD_TOP)
    head_bot = y_min + int(bb_h * ZONE_HEAD_BOT)
    arms_top = y_min + int(bb_h * ZONE_ARMS_TOP)
    arms_bot = y_min + int(bb_h * ZONE_ARMS_BOT)
    legs_top = y_min + int(bb_h * ZONE_LEGS_TOP)
    legs_bot = y_min + int(bb_h * ZONE_LEGS_BOT)

    # Compute zone histograms for both silhouettes
    head_a = column_projection(sil_a, head_top, head_bot, x_min, x_max)
    head_b = column_projection(sil_b, head_top, head_bot, x_min, x_max)
    arms_a = column_projection(sil_a, arms_top, arms_bot, x_min, x_max)
    arms_b = column_projection(sil_b, arms_top, arms_bot, x_min, x_max)
    legs_a = column_projection(sil_a, legs_top, legs_bot, x_min, x_max)
    legs_b = column_projection(sil_b, legs_top, legs_bot, x_min, x_max)

    head_sim = histogram_correlation(head_a, head_b)
    arms_sim = histogram_correlation(arms_a, arms_b)
    legs_sim = histogram_correlation(legs_a, legs_b)

    combined = WEIGHT_HEAD * head_sim + WEIGHT_ARMS * arms_sim + WEIGHT_LEGS * legs_sim

    return {
        "head_sim": round(head_sim, 4),
        "arms_sim": round(arms_sim, 4),
        "legs_sim": round(legs_sim, 4),
        "combined": round(combined, 4),
    }


def rpd_similarity_arms(sil_a: Image.Image, sil_b: Image.Image,
                        arms_top_frac: float = ARMS_TOP_FRAC,
                        arms_bot_frac: float = ARMS_BOT_FRAC,
                        center_mask_frac: float = CENTER_MASK_FRAC) -> dict:
    """
    Compute RPD similarity for the arms zone only.
    Used in --mode arms.

    Crops the arm band [arms_top_frac .. arms_bot_frac] of panel height,
    applies center masking (trunk exclusion), and computes column-projection
    correlation on the masked band.

    Returns dict with keys: arms_sim, combined (== arms_sim for this mode).
    """
    # Normalize
    wa, ha = sil_a.size
    wb, hb = sil_b.size
    if (wa, ha) != (wb, hb):
        sil_b = sil_b.resize((wa, ha), Image.LANCZOS)

    h = ha
    w = wa
    y_top = int(h * arms_top_frac)
    y_bot = int(h * arms_bot_frac)

    # Column projections with center mask
    arms_a = column_projection(sil_a, y_top, y_bot, center_mask_frac=center_mask_frac)
    arms_b = column_projection(sil_b, y_top, y_bot, center_mask_frac=center_mask_frac)

    arms_sim = histogram_correlation(arms_a, arms_b)

    return {
        "arms_sim": round(arms_sim, 4),
        "combined": round(arms_sim, 4),
    }


# ─── ARM REGION CROP (for contact sheet display) ─────────────────────────────

def crop_arm_region_display(sil: Image.Image,
                             arms_top_frac: float = ARMS_TOP_FRAC,
                             arms_bot_frac: float = ARMS_BOT_FRAC,
                             center_mask_frac: float = CENTER_MASK_FRAC) -> Image.Image:
    """
    Crop the arm region of a silhouette for display purposes.
    Used when building the contact sheet in arms mode.
    Does NOT affect metric computation.
    """
    w, h = sil.size
    top = int(h * arms_top_frac)
    bot = int(h * arms_bot_frac)
    arm_band = sil.crop((0, max(0, top), w, min(h, bot)))

    if center_mask_frac > 0:
        bw, bh = arm_band.size
        center_x = bw // 2
        half_mask = int(bw * center_mask_frac / 2)
        arr = arm_band.load()
        for y in range(bh):
            for x in range(max(0, center_x - half_mask), min(bw, center_x + half_mask)):
                arr[x, y] = 255
    return arm_band


# ─── CONTACT SHEET ───────────────────────────────────────────────────────────

def draw_zone_overlays(img: Image.Image, sil: Image.Image, x0: int, y0: int,
                        panel_w: int, panel_h: int) -> None:
    """
    Draw colored zone overlay rectangles on the contact sheet canvas at (x0, y0).

    Zone colors (semi-transparent style via blended fill lines):
      HEAD zone  — blue   (0, 80, 200)
      ARMS zone  — orange (200, 100, 0)
      LEGS zone  — green  (0, 140, 60)

    Each zone is indicated by a colored left-edge bar (4px wide) and a
    right-aligned label, so the silhouette itself remains fully legible.
    The overlay does NOT obscure the silhouette content — it uses border lines only.
    """
    draw = ImageDraw.Draw(img)

    # Derive zone pixel boundaries from the bounding box of character pixels in the
    # scaled silhouette panel. Fall back to panel-proportional bands if no bbox found.
    bb = bounding_box(sil)
    if bb is not None:
        # Map bbox to the scaled display panel coordinates
        sil_w, sil_h = sil.size
        scale_x = panel_w / max(1, sil_w)
        scale_y = panel_h / max(1, sil_h)
        bb_y_min = y0 + int(bb[1] * scale_y)
        bb_h     = max(1, int((bb[3] - bb[1]) * scale_y))
    else:
        # No character found — use full panel height as fallback
        bb_y_min = y0
        bb_h     = panel_h

    # Zone y-pixel positions (display space)
    head_top_px = bb_y_min + int(bb_h * ZONE_HEAD_TOP)
    head_bot_px = bb_y_min + int(bb_h * ZONE_HEAD_BOT)
    arms_top_px = bb_y_min + int(bb_h * ZONE_ARMS_TOP)
    arms_bot_px = bb_y_min + int(bb_h * ZONE_ARMS_BOT)
    legs_top_px = bb_y_min + int(bb_h * ZONE_LEGS_TOP)
    legs_bot_px = bb_y_min + int(bb_h * ZONE_LEGS_BOT)

    # Draw left-edge zone bars (4px wide colored rectangles)
    BAR_W = 4
    zones = [
        (head_top_px, head_bot_px, (0,  80, 200), "H"),   # HEAD — blue
        (arms_top_px, arms_bot_px, (200, 100, 0), "A"),   # ARMS — orange
        (legs_top_px, legs_bot_px, (0,  140,  60), "L"),  # LEGS — green
    ]
    for (zt, zb, col, ltr) in zones:
        zt = max(y0, min(y0 + panel_h, zt))
        zb = max(y0, min(y0 + panel_h, zb))
        if zb <= zt:
            continue
        draw.rectangle([x0, zt, x0 + BAR_W - 1, zb], fill=col)
        # Small letter label at top of bar
        mid_y = (zt + zb) // 2 - 5
        draw.text((x0 + BAR_W + 1, mid_y), ltr, fill=col)


def make_silhouette_contact_sheet(silhouettes: list, rows: int, cols: int,
                                   panel_w: int, panel_h: int,
                                   labels: list = None,
                                   mode: str = "full",
                                   output_zones: bool = False) -> Image.Image:
    """Build a contact sheet showing all silhouettes in a grid.

    Parameters:
      output_zones — if True, draw colored zone overlay bars on each panel:
                     HEAD zone (blue left bar), ARMS zone (orange left bar),
                     LEGS zone (green left bar). Only meaningful in --mode full.
    """
    LABEL_H = 22
    PAD = 8
    mode_label = f"Mode: {mode.upper()}  |  Metric: Regional Pose Delta (RPD) v3"
    if output_zones and mode == "full":
        mode_label += "  |  ZONES ON"
    total_w = cols * (panel_w + PAD) + PAD
    total_h = rows * (panel_h + LABEL_H + PAD) + PAD + 46
    out = Image.new("RGB", (total_w, total_h), (245, 245, 245))
    draw = ImageDraw.Draw(out)

    draw.text((PAD, 6),  "Expression Silhouette Test — RPD v3", fill=(30, 30, 30))
    draw.text((PAD, 24), mode_label, fill=(80, 80, 180))

    for idx, sil in enumerate(silhouettes):
        r = idx // cols
        c = idx % cols
        x0 = PAD + c * (panel_w + PAD)
        y0 = 46 + PAD + r * (panel_h + LABEL_H + PAD)
        sil_rgb = sil.convert("RGB")
        sil_rgb = sil_rgb.resize((panel_w, panel_h), Image.LANCZOS)
        out.paste(sil_rgb, (x0, y0))
        if output_zones and mode == "full":
            draw_zone_overlays(out, sil, x0, y0, panel_w, panel_h)
        label = labels[idx] if labels and idx < len(labels) else f"P{idx:02d}"
        draw.text((x0, y0 + panel_h + 2), label[:22], fill=(60, 60, 60))

    out.thumbnail((1280, 1280), Image.LANCZOS)
    return out


# ─── RPD PAIR DIFF VISUALIZATION (--viz-rpd) ─────────────────────────────────

def _zone_color_for_y(y: int, bb_y_min: int, bb_h: int,
                      a_only_col=(220, 60, 40),
                      b_only_col=(40, 200, 220)) -> tuple:
    """
    Return the zone-tint color based on y position within the bounding box.
    HEAD zone (top 25%)  → blue tint
    ARMS zone (mid 50%)  → orange tint
    LEGS zone (bot 25%)  → green tint
    """
    if bb_h <= 0:
        frac = 0.5
    else:
        frac = (y - bb_y_min) / bb_h
    frac = max(0.0, min(1.0, frac))

    if frac <= ZONE_HEAD_BOT:
        return (80, 120, 220)    # HEAD — blue
    elif frac <= ZONE_ARMS_BOT:
        return (220, 110, 40)    # ARMS — orange
    else:
        return (60, 180, 80)     # LEGS — green


def viz_rpd_pair(sil_a: Image.Image, sil_b: Image.Image,
                 label_a: str = "A", label_b: str = "B",
                 rpd_score: float = None,
                 zone_scores: dict = None) -> Image.Image:
    """
    Generate a side-by-side pixel difference heatmap for a pair of silhouettes.

    Layout (horizontal strip, 3 panels):
      [Silhouette A]  [Silhouette B]  [Diff Heatmap]

    Diff heatmap pixel coding:
      Pixels only in A     → bright red   (220, 60, 40)
      Pixels only in B     → bright cyan  (40, 200, 220)
      Pixels in both       → zone color, muted grey-tint:
                              HEAD zone → blue-grey  (120, 140, 200)
                              ARMS zone → orange-grey (200, 150, 100)
                              LEGS zone → green-grey  (100, 180, 110)
      No character pixel   → white (255, 255, 255)

    Zone colors are derived from the union bounding box to be consistent
    with the RPD zone definitions.

    Returns an RGB image ≤ 1280px wide.
    """
    # Normalize both to same size
    wa, ha = sil_a.size
    wb, hb = sil_b.size
    if (wa, ha) != (wb, hb):
        sil_b_r = sil_b.resize((wa, ha), Image.LANCZOS)
    else:
        sil_b_r = sil_b

    w, h = wa, ha

    # Get bounding box (union)
    bb_a = bounding_box(sil_a)
    bb_b = bounding_box(sil_b_r)
    if bb_a and bb_b:
        bb_y_min = min(bb_a[1], bb_b[1])
        bb_y_max = max(bb_a[3], bb_b[3])
        bb_h     = bb_y_max - bb_y_min
    else:
        bb_y_min = 0
        bb_h     = h

    # Build diff image
    arr_a = sil_a.load()
    arr_b = sil_b_r.load()
    diff  = Image.new("RGB", (w, h), (255, 255, 255))
    diff_arr = diff.load()

    for y in range(h):
        zone_col = _zone_color_for_y(y, bb_y_min, bb_h)
        for x in range(w):
            a_char = (arr_a[x, y] == 0)
            b_char = (arr_b[x, y] == 0)

            if a_char and b_char:
                # shared pixel — zone tint, slightly muted
                r = min(255, zone_col[0] + 80)
                g = min(255, zone_col[1] + 80)
                b_val = min(255, zone_col[2] + 80)
                diff_arr[x, y] = (r, g, b_val)
            elif a_char:
                diff_arr[x, y] = (220, 60, 40)    # A only — red
            elif b_char:
                diff_arr[x, y] = (40, 200, 220)   # B only — cyan

    # Build 3-panel strip
    LABEL_H = 28
    MARGIN   = 6
    strip_w  = w * 3 + MARGIN * 4
    strip_h  = h + LABEL_H + MARGIN * 2
    strip    = Image.new("RGB", (strip_w, strip_h), (230, 228, 224))
    draw     = ImageDraw.Draw(strip)

    try:
        from PIL import ImageFont
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
        font_sm = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except Exception:
        from PIL import ImageFont
        font    = ImageFont.load_default()
        font_sm = font

    panels = [
        (sil_a.convert("RGB"),  f"A: {label_a}", (60, 60, 60)),
        (sil_b.convert("RGB"),  f"B: {label_b}", (60, 60, 60)),
        (diff,                  "DIFF (red=A-only, cyan=B-only, zone-tinted=shared)", (40, 80, 160)),
    ]
    for i, (panel_img, plabel, pcol) in enumerate(panels):
        x0 = MARGIN + i * (w + MARGIN)
        y0 = MARGIN
        sil_disp = panel_img.resize((w, h), Image.LANCZOS) if panel_img.size != (w, h) else panel_img
        strip.paste(sil_disp, (x0, y0))
        draw.rectangle([x0, y0, x0 + w - 1, y0 + h - 1], outline=(160, 155, 148), width=1)
        draw.text((x0, y0 + h + 3), plabel, fill=pcol, font=font)

    # Add score info in bottom-right
    score_txt = ""
    if rpd_score is not None:
        score_txt += f"RPD={rpd_score:.1%}"
    if zone_scores:
        parts = [f"{k.replace('_sim','').upper()}={v:.0%}" for k, v in zone_scores.items()]
        score_txt += "  " + "  ".join(parts)
    if score_txt:
        draw.text((MARGIN, y0 + h + 16), score_txt, fill=(100, 80, 60), font=font_sm)

    # Zone legend
    legend_x = MARGIN + 2 * (w + MARGIN) + 4
    draw.text((legend_x, y0 + h + 3), "H=blue  A=orange  L=green", fill=(100, 100, 100), font=font_sm)

    strip.thumbnail((1280, 1280), Image.LANCZOS)
    return strip


def generate_viz_rpd(result: dict,
                     silhouettes: list,
                     panel_labels: list,
                     output_base: str,
                     verbose: bool = True):
    """
    For every FAIL or WARN pair in result["pairs"], generate a viz-rpd diff PNG.
    Files are saved as: <output_base_no_ext>_pair_XX_YY_vizdiff.png

    Parameters:
      result      — dict returned by run_test()
      silhouettes — list of silhouette images indexed by panel number
      panel_labels— list of panel label strings indexed by panel number
      output_base — path used as the base for output filenames
                    (extension stripped, _pair_XX_YY_vizdiff.png appended)
    """
    base, _ = os.path.splitext(output_base)
    flagged  = [p for p in result["pairs"] if p["status"] != "PASS"]

    if not flagged:
        if verbose:
            print("--viz-rpd: No FAIL/WARN pairs to visualize.")
        return

    saved = []
    for p in flagged:
        ia = p["panel_a"]
        ib = p["panel_b"]
        la = panel_labels[ia] if ia < len(panel_labels) else f"P{ia:02d}"
        lb = panel_labels[ib] if ib < len(panel_labels) else f"P{ib:02d}"

        sil_a = silhouettes[ia]
        sil_b = silhouettes[ib]

        img = viz_rpd_pair(
            sil_a, sil_b,
            label_a=la, label_b=lb,
            rpd_score=p.get("rpd"),
            zone_scores=p.get("zone_scores"),
        )
        out_path = f"{base}_pair_{ia:02d}_{ib:02d}_{p['status'].lower()}_vizdiff.png"
        img.save(out_path)
        saved.append(out_path)
        if verbose:
            print(f"  viz-rpd [{p['status']}] P{ia:02d}↔P{ib:02d}  RPD={p['rpd']:.1%} → {out_path}")

    if verbose:
        print(f"--viz-rpd: {len(saved)} diff image(s) generated.")
    return saved


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
             center_mask_frac: float = CENTER_MASK_FRAC,
             output_zones: bool = False,
             viz_rpd: bool = False) -> dict:
    """
    Run silhouette differentiation test on an expression sheet.

    Parameters:
      mode          — "full" (default) or "arms"
                      full: compares complete panel silhouettes via RPD (3 zones)
                      arms: compares only the arm/shoulder band via RPD (1 zone)

    Returns dict with keys:
      sheet, rows, cols, panel_count, active_panels, mode,
      pairs (list of {panel_a, panel_b, iom (=rpd score), status, zone_scores}),
      overall, worst_iom (=worst_rpd), worst_pair
    """
    if mode not in ("full", "arms"):
        raise ValueError(f"Unknown mode: {mode!r}. Use 'full' or 'arms'.")

    img = Image.open(sheet_path).convert("RGB")

    rows, cols, panel_w, panel_h, pad_x, pad_y, header_h = detect_grid(
        img, rows_override, cols_override
    )

    panels = extract_panels(img, rows, cols, panel_w, panel_h, pad_x, pad_y, header_h)

    silhouettes = []
    display_sils = []   # for contact sheet (arm crops in arms mode)
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
        if mode == "arms":
            display_sils.append(crop_arm_region_display(sil, arms_top_frac, arms_bot_frac, center_mask_frac))
        else:
            display_sils.append(sil)

        panel_labels.append(f"P{idx:02d} R{r}C{c}")
        if is_active:
            active_indices.append(idx)

    # Compare all active pairs
    pair_results = []
    worst_rpd = 0.0
    worst_pair = None

    for i, j in combinations(active_indices, 2):
        if mode == "arms":
            scores = rpd_similarity_arms(
                silhouettes[i], silhouettes[j],
                arms_top_frac, arms_bot_frac, center_mask_frac
            )
            zone_scores = {"arms_sim": scores["arms_sim"]}
        else:
            scores = rpd_similarity_full(silhouettes[i], silhouettes[j])
            zone_scores = {
                "head_sim": scores["head_sim"],
                "arms_sim": scores["arms_sim"],
                "legs_sim": scores["legs_sim"],
            }

        rpd = scores["combined"]

        if rpd >= fail_threshold:
            status = "FAIL"
        elif rpd >= warn_threshold:
            status = "WARN"
        else:
            status = "PASS"

        pair_results.append({
            "panel_a": i,
            "panel_b": j,
            "iom": round(rpd, 4),    # key kept as "iom" for backward compat
            "rpd": round(rpd, 4),
            "status": status,
            "zone_scores": zone_scores,
        })

        if rpd > worst_rpd:
            worst_rpd = rpd
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
        "metric": "RPD_v3",
        "pairs": pair_results,
        "overall": overall,
        "worst_iom": round(worst_rpd, 4),   # kept for backward compat
        "worst_rpd": round(worst_rpd, 4),
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
        arm_h = int(panel_h * (arms_bot_frac - arms_top_frac)) if mode == "arms" else panel_h
        contact = make_silhouette_contact_sheet(
            display_sils, rows, cols, panel_w, arm_h if mode == "arms" else panel_h,
            panel_labels, mode=mode, output_zones=output_zones
        )
        contact.save(output_path)
        if verbose:
            print(f"\nSilhouette contact sheet saved: {output_path}")
            if output_zones and mode == "full":
                print("Zone overlays: H=blue (HEAD top 25%), A=orange (ARMS mid 50%), L=green (LEGS bot 25%)")

    if viz_rpd and output_path:
        if verbose:
            print("\n--viz-rpd: Generating RPD pair diff images for FAIL/WARN pairs...")
        generate_viz_rpd(
            result=result,
            silhouettes=silhouettes,
            panel_labels=panel_labels,
            output_base=output_path,
            verbose=verbose,
        )
    elif viz_rpd and not output_path:
        if verbose:
            print("WARNING: --viz-rpd requires --output to be set (used as base filename). Skipping.")

    return result


def _print_report(result: dict, fail_threshold: float, warn_threshold: float,
                  mode: str = "full"):
    print("=" * 65)
    print(f"EXPRESSION SILHOUETTE TEST — Regional Pose Delta (RPD) v3")
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
    if mode == "full":
        print(f"Zone weights: HEAD={WEIGHT_HEAD:.0%}  ARMS={WEIGHT_ARMS:.0%}  LEGS={WEIGHT_LEGS:.0%}")
    print("-" * 65)

    if mode == "arms":
        print("Comparing arm/shoulder region only (trunk masked, RPD histogram correlation).")
        print("PASS = arm shape differs; FAIL = arm regions indistinguishable.")
    else:
        print("RPD = column-projection correlation per zone, weighted HEAD/ARMS/LEGS.")
        print("Low RPD = distinct poses. High RPD = too similar.")
    print("-" * 65)

    fail_pairs = [p for p in result["pairs"] if p["status"] != "PASS"]
    if fail_pairs:
        print("FLAGGED PAIRS:")
        for p in sorted(fail_pairs, key=lambda x: -x["rpd"]):
            zones = p.get("zone_scores", {})
            zone_str = "  ".join(f"{k.replace('_sim','').upper()}={v:.0%}" for k, v in zones.items())
            print(f"  [{p['status']:4s}]  Panel {p['panel_a']:02d} ↔ Panel {p['panel_b']:02d}"
                  f"  RPD={p['rpd']:.1%}  [{zone_str}]")
    else:
        print("All panel pairs: PASS (poses sufficiently distinct)")

    print("-" * 65)
    print(f"Worst pair:   Panels {result['worst_pair']} — RPD {result['worst_rpd']:.1%}"
          if result["worst_pair"] else "Worst pair:   N/A (< 2 active panels)")
    print(f"OVERALL:      {result['overall']}")
    print("=" * 65)


# ─── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "LTG Expression Silhouette Test v003 — Regional Pose Delta (RPD) metric.\n\n"
            "Replaces the IoM metric used in v001/v002, which was biased toward\n"
            "high similarity on human characters due to shared trunk mass.\n\n"
            "RPD divides each silhouette into HEAD / ARMS / LEGS zones and computes\n"
            "column-projection histogram correlation per zone. Zone weights:\n"
            "  HEAD 35%%  ARMS 45%%  LEGS 20%%\n\n"
            "Two modes:\n"
            "  full  — full-panel RPD (3 zones, default)\n"
            "  arms  — arm/shoulder band only (1 zone, trunk masked)\n\n"
            "PASS < 70%%  WARN 70-85%%  FAIL >= 85%% (all as RPD score)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("sheet", help="Path to expression sheet PNG")
    parser.add_argument("--rows", type=int, default=None)
    parser.add_argument("--cols", type=int, default=None)
    parser.add_argument(
        "--mode", choices=["full", "arms"], default="full",
        help="'full' = full-panel RPD (default). 'arms' = arm band only.",
    )
    parser.add_argument("--arms-top", type=float, default=ARMS_TOP_FRAC, metavar="FRAC",
                        help=f"Arms mode: top of arm region (default {ARMS_TOP_FRAC})")
    parser.add_argument("--arms-bot", type=float, default=ARMS_BOT_FRAC, metavar="FRAC",
                        help=f"Arms mode: bottom of arm region (default {ARMS_BOT_FRAC})")
    parser.add_argument("--center-mask", type=float, default=CENTER_MASK_FRAC, metavar="FRAC",
                        help=f"Trunk exclusion mask fraction (default {CENTER_MASK_FRAC})")
    parser.add_argument("--threshold", type=float, default=FAIL_THRESHOLD,
                        help=f"RPD fail threshold (default {FAIL_THRESHOLD})")
    parser.add_argument("--warn-threshold", type=float, default=WARN_THRESHOLD,
                        help=f"RPD warn threshold (default {WARN_THRESHOLD})")
    parser.add_argument("--output", "-o", default=None,
                        help="Save silhouette contact sheet PNG to this path")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON result to stdout (in addition to report)")
    parser.add_argument("--output-zones", action="store_true",
                        help=(
                            "Draw colored zone overlay bars on each panel in the contact sheet. "
                            "HEAD zone = blue left bar, ARMS zone = orange left bar, "
                            "LEGS zone = green left bar. Only active in --mode full. "
                            "Requires --output to save the contact sheet. "
                            "Helps designers immediately see which zone drove a WARN/FAIL."
                        ))
    parser.add_argument("--viz-rpd", action="store_true",
                        help=(
                            "For each FAIL/WARN pair, generate a side-by-side pixel diff "
                            "heatmap PNG showing which pixels drove the RPD score. "
                            "Pixels unique to A = red, unique to B = cyan, shared = "
                            "zone-tinted (blue=HEAD, orange=ARMS, green=LEGS). "
                            "Requires --output (used as base path for generated files). "
                            "Output: <base>_pair_XX_YY_<status>_vizdiff.png per flagged pair. "
                            "Added C39 (actioned ideabox, Maya Santos)."
                        ))
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
        output_zones=args.output_zones,
        viz_rpd=args.viz_rpd,
    )

    if args.json:
        print(json.dumps(result, indent=2))

    if result["overall"] == "FAIL":
        sys.exit(2)
    elif result["overall"] == "WARN":
        sys.exit(1)
    else:
        sys.exit(0)
