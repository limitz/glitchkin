#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_colorkey_glitch_covetous_gen.py
Color Key Generator — COVETOUS Glitch Style Frame
"Luma & the Glitchkin"

Author: Sam Kowalski, Color & Style Artist
Date: 2026-03-30
Cycle: 41

Purpose:
  Generates a 640×360 color key thumbnail for the COVETOUS Glitch style frame.
  Scene: Glitch alone at the threshold — watching Real World warmth from the void.
  Requested by Alex Chen per Jayden Torres C16 critique (79/100 on Glitch,
  called COVETOUS "the strongest new design moment in the pitch").

  Color logic:
  - Void Black (GL-08) base fill — the digital void
  - UV Purple (GL-04) as dominant ambient — Glitch Layer identity
  - No warm light on Glitch's body — the entire premise is the separation
  - Real World warm glow (RW-02 Soft Gold / RW-03 Sunlit Amber) ONLY in right 25%
    of frame — visible through the threshold, never touching Glitch
  - Corrupt Amber (GL-07) — Glitch's body fill, the canonical expression color
  - Acid Green (GL-03) — Glitch's COVETOUS target-lock eyes (bilateral — interior state)
  - Threshold edge: thin ELEC_CYAN luminous line as the barrier itself

  Staging:
  - Camera: Low angle (eye-level to Glitch)
  - Glitch: Left-center, COVETOUS state, +12° tilt toward threshold
  - Right 25%: Warm Real World glow — soft radial, alpha max ~90, falls to 0 before midframe
  - Background: UV Purple atmospheric depth over Void Black base

Output:
  output/color/color_keys/LTG_COLOR_colorkey_glitch_covetous.png (640×360)

Usage:
  python3 LTG_TOOL_colorkey_glitch_covetous_gen.py

Cycle 41: Initial creation. Sam Kowalski.
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
from __future__ import annotations
import os
import math
import random
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH = output_dir('color', 'color_keys', 'LTG_COLOR_colorkey_glitch_covetous.png')
W, H = 640, 360  # 16:9 thumbnail

# ── Palette constants — all named, no undocumented inline tuples ──────────────

# Glitch Layer environment
VOID_BLACK         = ( 10,  10,  20)   # GL-08 — primary base fill
BELOW_VOID_BLACK   = (  5,   5,   8)   # GL-08a — deepest void anchor (ground plane)
UV_PURPLE          = (123,  47, 190)   # GL-04 — Glitch Layer ambient
DEEP_DIGITAL_VOID  = ( 58,  16,  96)   # GL-04a — darkest UV zone / deep background
ATMO_DEPTH_PURPLE  = ( 74,  24, 128)   # GL-04b — mid-void atmospheric band
ELEC_CYAN          = (  0, 240, 255)   # GL-01 — threshold barrier edge
HOT_MAGENTA        = (255,  45, 107)   # GL-02 — Glitch crack (always present)
ACID_GREEN         = ( 57, 255,  20)   # GL-03 — COVETOUS eye color (bilateral)

# Glitch character colors
CORRUPT_AMBER      = (255, 140,   0)   # GL-07 — Glitch primary body fill
CORRUPT_AMB_HL     = (255, 185,  80)   # GL-07 lightened — highlight facet (upper-left)
CORRUPT_AMB_SH     = (168,  76,   0)   # GL-07a — Corrupt Amber shadow / ambient dim pixels
VOID_BLACK_OUTLINE = ( 10,  10,  20)   # GL-08 — Glitch body outline (same as VOID_BLACK)

# Real World warmth (threshold bleed — right zone only)
SOFT_GOLD          = (232, 201,  90)   # RW-02 — warm key at threshold (brightest warm point)
SUNLIT_AMBER       = (212, 146,  58)   # RW-03 — warm secondary volume

# Palette strip border
SWATCH_OUTLINE     = ( 50,  45,  70)   # Deep purple-grey — not a pure grey (construction value)


def load_font(size: int = 13, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Load a system TrueType font; fall back to default if unavailable."""
    paths = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
         else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def lbl(draw: ImageDraw.ImageDraw, x: int, y: int, text: str,
        font: ImageFont.FreeTypeFont,
        fg: Tuple[int, int, int] = (220, 240, 255),
        bg: Tuple[int, int, int] | None = None) -> None:
    """Draw a label with optional background box."""
    if bg is not None:
        bb = draw.textbbox((x, y), text, font=font)
        draw.rectangle([bb[0] - 2, bb[1] - 1, bb[2] + 2, bb[3] + 1], fill=bg)
    draw.text((x, y), text, fill=fg, font=font)


def palette_strip(draw: ImageDraw.ImageDraw,
                  swatches: List[Tuple[Tuple[int, int, int], str]],
                  x: int, y: int, sw: int = 34, sh: int = 24, gap: int = 3) -> None:
    """Draw a labeled row of color swatches."""
    font = load_font(9)
    for i, (col, name) in enumerate(swatches):
        sx = x + i * (sw + gap)
        draw.rectangle([sx, y, sx + sw, y + sh], fill=col)
        draw.rectangle([sx, y, sx + sw, y + sh], outline=SWATCH_OUTLINE, width=1)
        r, g, b = col
        lum = 0.299 * r / 255 + 0.587 * g / 255 + 0.114 * b / 255
        tc = (10, 10, 20) if lum > 0.40 else (210, 235, 255)
        draw.text((sx + 2, y + 14), name[:5], fill=tc, font=font)


def draw_glitch_body(draw: ImageDraw.ImageDraw,
                     cx: int, cy: int,
                     rx: int = 28, ry: int = 32,
                     tilt_deg: float = 12.0,
                     spike_h: int = 12) -> None:
    """
    Draw Glitch in COVETOUS state:
      - body_tilt = +12° (appetitive lean toward threshold / right)
      - spike_h = 12 (forward-focused per glitch.md §3.1)
      - arm_l_dy = -8, arm_r_dy = -6 (both slightly raised — reaching forward)
      - Eyes: COVETOUS acid slit bilateral [[5,5,5],[0,5,0],[0,0,0]]
      - Confetti: minimal UV_PURPLE only (interior state, count=4)
    """
    tilt = math.radians(tilt_deg)
    tilt_off = int(tilt * rx * 0.40)  # spike lean offset

    # ── Diamond body vertices ─────────────────────────────────────────────────
    # Per glitch.md §2.1 construction formula
    top   = (cx + int(rx * 0.15 * math.sin(tilt)),
             cy - ry + int(rx * 0.15 * math.cos(tilt)))
    right = (cx + int(rx * math.cos(-tilt)),
             cy + int(rx * 0.2 * math.sin(-tilt)))
    bot   = (cx - int(rx * 0.15 * math.sin(tilt)),
             cy + int(ry * 1.15))
    left  = (cx - int(rx * math.cos(-tilt)),
             cy - int(rx * 0.2 * math.sin(-tilt)))

    # ── Shadow offset (UV Purple, +3 right +4 down) ───────────────────────────
    shadow_pts = [
        (top[0] + 3,   top[1] + 4),
        (right[0] + 3, right[1] + 4),
        (bot[0] + 3,   bot[1] + 4),
        (left[0] + 3,  left[1] + 4),
    ]
    draw.polygon(shadow_pts, fill=UV_PURPLE)

    # ── Main body fill (CORRUPT_AMBER) ───────────────────────────────────────
    body_pts = [top, right, bot, left]
    draw.polygon(body_pts, fill=CORRUPT_AMBER)

    # ── Highlight facet (upper-left triangle) ────────────────────────────────
    # ctr = just above center; mid_tl = midpoint of top-left edge
    ctr    = (cx, cy - ry // 4)
    mid_tl = ((top[0] + left[0]) // 2, (top[1] + left[1]) // 2)
    draw.polygon([top, ctr, mid_tl], fill=CORRUPT_AMB_HL)

    # ── Outline ───────────────────────────────────────────────────────────────
    draw.polygon(body_pts, outline=VOID_BLACK_OUTLINE, width=2)

    # ── HOT_MAG crack ─────────────────────────────────────────────────────────
    cs = (cx - rx // 2, cy - ry // 3)  # crack start: upper-left quadrant
    ce = (cx + rx // 3, cy + ry // 2)  # crack end:   lower-right quadrant
    draw.line([cs, ce], fill=HOT_MAGENTA, width=2)
    mid_c = ((cs[0] + ce[0]) // 2, (cs[1] + ce[1]) // 2)
    fork  = (cx + rx // 2, cy - ry // 4)
    draw.line([mid_c, fork], fill=HOT_MAGENTA, width=1)

    # ── Top spike (5-point crown, spike_h=12) ────────────────────────────────
    cy_top = top[1]
    sx = cx + tilt_off
    spike_pts = [
        (sx - spike_h // 2, cy_top),
        (sx - spike_h,      cy_top - spike_h),
        (sx,                cy_top - spike_h * 2),  # tip
        (sx + spike_h,      cy_top - spike_h),
        (sx + spike_h // 2, cy_top),
    ]
    draw.polygon(spike_pts, fill=CORRUPT_AMBER, outline=VOID_BLACK_OUTLINE)
    # HOT_MAG spark at spike tip
    draw.line([(sx, cy_top - spike_h * 2 - 4), (sx, cy_top - spike_h * 2)],
              fill=HOT_MAGENTA, width=2)

    # ── Bottom spike (hover point) ────────────────────────────────────────────
    cy_bot = bot[1]
    bspts = [
        (cx - spike_h // 2, cy_bot),
        (cx + spike_h // 2, cy_bot),
        (cx, cy_bot + spike_h + 4),
    ]
    draw.polygon(bspts, fill=CORRUPT_AMB_SH, outline=VOID_BLACK_OUTLINE)

    # ── Arm-spikes (COVETOUS: arm_l_dy=-8, arm_r_dy=-6) ─────────────────────
    arm_l_dy = -8
    arm_r_dy = -6

    # Left arm-spike
    ax_l  = left[0] - 6
    ay_l  = cy + arm_l_dy
    tip_l = (ax_l - 14, ay_l - 8)
    draw.polygon([(ax_l, ay_l - 5), (ax_l, ay_l + 5), tip_l],
                 fill=CORRUPT_AMBER, outline=VOID_BLACK_OUTLINE)

    # Right arm-spike (reaching slightly toward threshold)
    ax_r  = right[0] + 6
    ay_r  = cy + arm_r_dy
    tip_r = (ax_r + 14, ay_r - 8)
    draw.polygon([(ax_r, ay_r - 5), (ax_r, ay_r + 5), tip_r],
                 fill=CORRUPT_AMBER, outline=VOID_BLACK_OUTLINE)

    # ── Pixel eyes — COVETOUS bilateral: [[5,5,5],[0,5,0],[0,0,0]] ───────────
    # Both eyes identical = interior state (bilateral rule)
    face_cy = cy - ry // 6
    cell = 5  # pixel cell size at this render scale

    # Left eye
    leye_x = cx - rx // 2 - cell * 3 // 2
    leye_y = face_cy - cell * 3 // 2

    # Right eye
    reye_x = cx + rx // 2 - cell * 3 // 2
    reye_y = face_cy - cell * 3 // 2

    # COVETOUS glyph: [[5,5,5],[0,5,0],[0,0,0]] — 5=ACID_GREEN, 0=VOID_BLACK
    COVETOUS_GLYPH = [
        [5, 5, 5],
        [0, 5, 0],
        [0, 0, 0],
    ]
    CELL_COLORS = {
        0: VOID_BLACK,
        5: ACID_GREEN,
    }

    for eye_x, eye_y in [(leye_x, leye_y), (reye_x, reye_y)]:
        for row in range(3):
            for col in range(3):
                state = COVETOUS_GLYPH[row][col]
                cx_cell = eye_x + col * cell
                cy_cell = eye_y + row * cell
                draw.rectangle([cx_cell, cy_cell, cx_cell + cell - 1, cy_cell + cell - 1],
                                fill=CELL_COLORS[state])

    # ── Confetti (COVETOUS: minimal UV_PURPLE — count=4, spread=18px) ─────────
    rng = random.Random(41_002)  # deterministic, C41 covetous seed
    for _ in range(4):
        px = cx + rng.randint(-18, 18)
        py = cy_bot + rng.randint(4, 18)
        col = UV_PURPLE if rng.random() < 0.7 else CORRUPT_AMB_SH
        sz = rng.randint(2, 3)
        draw.rectangle([px, py, px + sz, py + sz], fill=col)


def generate_covetous_colorkey() -> Image.Image:
    """
    Generate the COVETOUS Glitch style frame color key thumbnail.

    Composition:
    - Vast void background (GL-08 Void Black + GL-04 UV Purple ambient)
    - Right 25%: Real World warm glow bleeding through threshold
    - Threshold edge: thin GL-01 Electric Cyan vertical line
    - Left-center: Glitch in COVETOUS state (+12° tilt toward threshold)
    - Palette strip at bottom

    Key principle: Glitch is in pure void light. It sees warmth. It does not touch warmth.
    """
    rng = random.Random(41_001)  # deterministic seed — C41 covetous scene

    img = Image.new("RGB", (W, H), VOID_BLACK)
    draw = ImageDraw.Draw(img)

    # ── BACKGROUND: UV Purple atmospheric void ────────────────────────────────
    # Gradient from near-void (top) to UV ambient (mid) to deep void (bottom)
    for row in range(H):
        t = row / H
        if t < 0.50:
            # Upper half: Void Black → UV Purple (subtly — ambient only)
            t2 = t / 0.50
            r = int(VOID_BLACK[0] + t2 * (DEEP_DIGITAL_VOID[0] - VOID_BLACK[0]))
            g = int(VOID_BLACK[1] + t2 * (DEEP_DIGITAL_VOID[1] - VOID_BLACK[1]))
            b = int(VOID_BLACK[2] + t2 * (DEEP_DIGITAL_VOID[2] - VOID_BLACK[2]))
        else:
            # Lower half: Deep Digital Void → Atmospheric Depth Purple (ground zone)
            t2 = (t - 0.50) / 0.50
            r = int(DEEP_DIGITAL_VOID[0] + t2 * (ATMO_DEPTH_PURPLE[0] - DEEP_DIGITAL_VOID[0]))
            g = int(DEEP_DIGITAL_VOID[1] + t2 * (ATMO_DEPTH_PURPLE[1] - DEEP_DIGITAL_VOID[1]))
            b = int(DEEP_DIGITAL_VOID[2] + t2 * (ATMO_DEPTH_PURPLE[2] - DEEP_DIGITAL_VOID[2]))
        # Only draw to left 75% of frame (right side gets warm treatment)
        draw.line([(0, row), (int(W * 0.75), row)], fill=(r, g, b))

    # ── VOID STRUCTURE: faint platform silhouette at base ────────────────────
    # Glitch is hovering above a Glitch Layer void platform (barely visible)
    plat_y = int(H * 0.82)
    plat_col = DEEP_DIGITAL_VOID  # barely distinct from background
    draw.rectangle([0, plat_y, int(W * 0.78), H - 34], fill=plat_col)
    # Platform circuit trace (faint ELEC_CYAN line at top edge)
    draw.line([(0, plat_y), (int(W * 0.75), plat_y)], fill=UV_PURPLE, width=1)

    # ── SPARSE VOID ARTIFACTS: distant structural hints ───────────────────────
    # Very faint UV Purple slab outlines in far void (Glitch Layer depth indicators)
    far_slabs = [
        (int(W * 0.04), int(H * 0.22), int(W * 0.18), int(H * 0.34)),
        (int(W * 0.52), int(H * 0.16), int(W * 0.68), int(H * 0.28)),
        (int(W * 0.20), int(H * 0.38), int(W * 0.36), int(H * 0.50)),
    ]
    SLAB_OUTLINE = ( 40,  16,  62)  # UV Purple at ~33% — construction value (faint void structure)
    for x0, y0, x1, y1 in far_slabs:
        draw.rectangle([x0, y0, x1, y1], fill=VOID_BLACK, outline=SLAB_OUTLINE, width=1)

    # ── REAL WORLD THRESHOLD: right 25% warm glow ────────────────────────────
    # The threshold zone: RW-02 Soft Gold + RW-03 Sunlit Amber radial bleed
    # This warmth is NOT a light source on Glitch. It is purely in the right zone.
    threshold_x = int(W * 0.75)  # the boundary x position

    # Warm base fill for right 25%
    for row in range(H - 34):
        # Vertical gradient: Sunlit Amber top → Soft Gold mid → Sunlit Amber bottom
        t = row / (H - 34)
        if t < 0.40:
            t2 = t / 0.40
            r_col = int(SUNLIT_AMBER[0] + t2 * (SOFT_GOLD[0] - SUNLIT_AMBER[0]))
            g_col = int(SUNLIT_AMBER[1] + t2 * (SOFT_GOLD[1] - SUNLIT_AMBER[1]))
            b_col = int(SUNLIT_AMBER[2] + t2 * (SOFT_GOLD[2] - SUNLIT_AMBER[2]))
        else:
            t2 = (t - 0.40) / 0.60
            r_col = int(SOFT_GOLD[0] + t2 * (SUNLIT_AMBER[0] - SOFT_GOLD[0]))
            g_col = int(SOFT_GOLD[1] + t2 * (SUNLIT_AMBER[1] - SOFT_GOLD[1]))
            b_col = int(SOFT_GOLD[2] + t2 * (SUNLIT_AMBER[2] - SOFT_GOLD[2]))
        draw.line([(threshold_x + 2, row), (W, row)], fill=(r_col, g_col, b_col))

    # Warm radial bleed leftward into void — using RGBA composite approach
    # Draw on a separate RGBA layer and paste with transparency falloff
    warm_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    warm_draw = ImageDraw.Draw(warm_layer)
    bleed_width = 120  # warm light bleeds up to 120px left of threshold
    for offset in range(bleed_width):
        # Alpha falls off from 90 at threshold to 0 at 120px left
        alpha = int(90 * (1.0 - offset / bleed_width))
        x_pos = threshold_x - offset
        if x_pos < 0:
            break
        warm_draw.line([(x_pos, 0), (x_pos, H - 34)], fill=(SOFT_GOLD[0], SOFT_GOLD[1], SOFT_GOLD[2], alpha))

    # Convert base image to RGBA for paste
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, warm_layer)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)  # refresh draw context after paste

    # ── THRESHOLD EDGE: thin GL-01 ELEC_CYAN line (the barrier itself) ───────
    # 2px width — luminous boundary between worlds
    draw.line([(threshold_x, 0), (threshold_x, H - 34)], fill=ELEC_CYAN, width=2)
    # Subtle ELEC_CYAN glow halo around barrier edge (1px each side, dim)
    THRESHOLD_GLOW = ( 0, 60, 64)  # ELEC_CYAN very dim — construction value (threshold halo)
    draw.line([(threshold_x - 2, 0), (threshold_x - 2, H - 34)], fill=THRESHOLD_GLOW, width=1)
    draw.line([(threshold_x + 2, 0), (threshold_x + 2, H - 34)], fill=THRESHOLD_GLOW, width=1)

    # ── GLITCH CHARACTER: COVETOUS state, left-center ────────────────────────
    glitch_cx = int(W * 0.30)
    glitch_cy = int(H * 0.52)
    draw_glitch_body(draw, glitch_cx, glitch_cy, rx=28, ry=32,
                     tilt_deg=12.0, spike_h=12)

    # ── ANNOTATION: "NO WARM LIGHT ON GLITCH" marker ─────────────────────────
    ann_font = load_font(9)
    lbl(draw, int(W * 0.03), int(H * 0.04),
        "COVETOUS — Interior State", ann_font, fg=ACID_GREEN, bg=None)
    lbl(draw, int(W * 0.03), int(H * 0.09),
        "No warm light on Glitch body", ann_font,
        fg=(200, 90, 40), bg=None)  # warm-orange warning text

    # Warm zone annotation
    lbl(draw, threshold_x + 4, int(H * 0.04),
        "RW WARM", ann_font, fg=SOFT_GOLD, bg=None)
    lbl(draw, threshold_x + 4, int(H * 0.09),
        "BLEED", ann_font, fg=SOFT_GOLD, bg=None)
    lbl(draw, threshold_x + 4, int(H * 0.14),
        "ONLY", ann_font, fg=SOFT_GOLD, bg=None)

    # ── PALETTE STRIP ─────────────────────────────────────────────────────────
    strip_y = H - 34
    draw.rectangle([0, strip_y - 2, W, H], fill=VOID_BLACK)

    title_font = load_font(11, bold=True)
    lbl(draw, 4, strip_y - 16, "COVETOUS Glitch — Color Key v001 (C41)",
        title_font, fg=CORRUPT_AMBER, bg=None)

    # Primary zone swatches (Glitch Layer side)
    primary_swatches = [
        (VOID_BLACK,      "Void*"),
        (UV_PURPLE,       "UV*"),
        (DEEP_DIGITAL_VOID, "DVoid"),
        (CORRUPT_AMBER,   "CA*"),
        (ACID_GREEN,      "AG*"),
        (HOT_MAGENTA,     "Crack"),
    ]
    palette_strip(draw, primary_swatches, x=4, y=strip_y, sw=34, sh=24, gap=3)

    # Threshold / RW side swatches
    rw_swatches = [
        (ELEC_CYAN,    "Thr*"),
        (SOFT_GOLD,    "RW*"),
        (SUNLIT_AMBER, "Amb"),
    ]
    palette_strip(draw, rw_swatches, x=int(W * 0.68), y=strip_y, sw=34, sh=24, gap=3)

    # ── THUMBNAIL RULE: ≤ 1280px in both dimensions ───────────────────────────
    img.thumbnail((1280, 1280), Image.LANCZOS)

    return img


def main() -> None:
    out_dir = os.path.dirname(OUTPUT_PATH)
    os.makedirs(out_dir, exist_ok=True)

    img = generate_covetous_colorkey()
    img.save(OUTPUT_PATH)

    print(f"Saved: {OUTPUT_PATH}")
    print(f"Size: {img.size[0]}x{img.size[1]}")
    print("Color key: COVETOUS Glitch — UV Purple void + Corrupt Amber character + RW warm threshold")
    print("Glitch body: GL-07 Corrupt Amber, COVETOUS state (+12° tilt, acid-slit bilateral eyes)")
    print("Threshold: GL-01 ELEC_CYAN barrier edge, RW-02 Soft Gold warm bleed (right 25% only)")
    print("Zero warm light on Glitch body — separation is the premise.")


if __name__ == "__main__":
    main()
