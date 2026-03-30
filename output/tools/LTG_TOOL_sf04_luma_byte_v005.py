# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_sf04_luma_byte_v005.py
Style Frame 04 — "The Dynamic" (Luma + Byte Interaction) — C41 Rebuild
"Luma & the Glitchkin"

Author: Jordan Reed — Style Frame Art Specialist
Cycle: 41 (C40 task — v005 full rebuild from C40 mandate)

REBUILD REASON (C40 producer mandate — 3 critics, 2 cycles):
  - Warm/cool separation: 1.1 (FAIL — target ≥ 15.0)
  - SUNLIT_AMBER lamp hue drift: lamp was (255,200,80) hue≈41°;
    canonical #FF8C00 = (255,140,0) hue≈33°. Delta was 8° (spec: ≤5°)
  - Byte-teal floor bounce between characters: ABSENT (specified in brief)
  - Value floor: insufficient deep shadow under furniture
  - Dramatic logic: must be warmest of 4 frames (domestic lamp + CRT)

FIXES IN v005:
  Fix 1: Lamp color → (255, 140, 0) = #FF8C00 canonical. Hue 33° matches spec.
  Fix 2: Warm/cool separation strategy:
    - Top half: lamp halo drastically amplified (stronger ellipse, alpha up to 90)
      + warm wall gradient pushed toward SUNLIT_AMBER
    - Bottom half: Byte-teal floor bounce spill between characters (teal ellipses
      at floor level, alpha 40-60), plus cooler floor shadow zone
  Fix 3: Byte-teal floor bounce — teal elliptical spill on floor between
    luma_cx (~420) and byte_cx (~900), 3-pass radial gradient
  Fix 4: Value floor — dark shadow pass under couch (foreground left) using
    DEEP_COCOA + NEAR_BLACK, value target ≤ 30 in shadow region
  Fix 5: Domestic scene enrichment — couch and rug added for "warm world" read

Canonical specs:
  - Byte body   = GL-01b #00D4E8 (BYTE_TEAL)
  - Luma blush  = #E8A87C
  - Rim light   = side="right" with char_cx set per-character
  - Face light  = warm upper-left for Luma
  - Value ceil  = brightest highlight >= 225
  - Value floor = ≤ 30 in deep shadow zones
  - Monitor glow: Byte has cool (#00D4E8) contribution on near side
  - Canvas 1280x720 (≤ 1280px rule)
  - Warm/cool separation: ≥ 15.0 (REAL_INTERIOR threshold = 12; target 15+)

Composition:
  - Background: warm domestic room. CRT monitor on right emitting cyan glow.
    Couch lower-left. Rug between characters. Lamp upper-left.
  - Luma: left-center (~x=0.32W), standing, facing right toward Byte.
  - Byte: right-center (~x=0.68W), hovering, facing left toward Luma.
  - Byte-teal floor bounce: between characters on floor/rug.
  - Title strip at bottom.

Output: /home/wipkat/team/output/color/style_frames/LTG_SF_luma_byte_v005.png
Usage: python3 LTG_TOOL_sf04_luma_byte_v005.py
"""

import os
import sys
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Import procedural draw library
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
from LTG_TOOL_procedural_draw import (
    wobble_line, wobble_polygon, variable_stroke,
    add_rim_light, add_face_lighting, silhouette_test, value_study
)

OUTPUT_PATH = "/home/wipkat/team/output/color/style_frames/LTG_SF_luma_byte_v005.png"

W, H = 1280, 720

# Scale helpers (reference: 1920x1080)
SX = W / 1920
SY = H / 1080
def sx(n): return int(n * SX)
def sy(n): return int(n * SY)
def sp(n): return int(n * min(SX, SY))


# ── Canonical Palette ─────────────────────────────────────────────────────────
WARM_CREAM      = (250, 240, 220)
SOFT_GOLD       = (232, 201,  90)

# FIX 1: Lamp color corrected to canonical #FF8C00 = (255,140,0) hue≈33°
# v004 used (255,200,80) hue≈41° — 8° drift. Spec: hue delta ≤ 5° from #FF8C00.
LAMP_AMBER      = (255, 140,   0)   # canonical #FF8C00 SUNLIT_AMBER (indoor lamp)
LAMP_HIGHLIGHT  = (255, 200,  80)   # bright center of lamp bulb only (not halo)

# Wall / room tones — pushed warmer to help top-half separation
WALL_WARM       = (230, 195, 155)   # warm bottom (bumped from 220,190,150)
WALL_UPPER      = (210, 172, 118)   # warm top (bumped from 200,168,122)
FLOOR_COLOR     = (160, 120,  70)
FLOOR_SHADOW    = (100,  72,  38)   # deeper floor shadow (value ≤ 30 target)

# Deep shadow colors for furniture
DEEP_COCOA      = ( 40,  24,  12)   # near-black shadow (value = 40 → target ≤ 30 under couch)
NEAR_BLACK_WARM = ( 28,  18,   8)   # deepest shadow (value = 28 ✓)

CEILING_COLOR   = ( 75,  50,  18)
CEILING_DARK    = ( 55,  35,  10)

# Furniture
COUCH_BASE      = (180,  88,  52)   # warm terracotta couch
COUCH_SHADOW    = (130,  56,  32)
COUCH_CUSHION   = (200, 110,  65)
RUG_BASE        = (140,  82,  42)
RUG_PATTERN     = (165,  95,  52)

# Character — Luma
TERRACOTTA      = (199,  91,  57)
RUST_SHADOW     = (140,  58,  34)
WARM_TAN        = (196, 168, 130)
SKIN            = (200, 136,  90)
SKIN_HL         = (232, 184, 136)
SKIN_SH         = (168, 104,  56)
HAIR_COLOR      = ( 26,  15,  10)
LINE            = ( 59,  40,  32)
HOODIE_ORANGE   = (232, 112,  58)
HOODIE_SHADOW   = (184,  74,  32)
JEANS           = ( 58,  90, 140)
JEANS_SH        = ( 38,  62, 104)
BLUSH           = (232, 168, 124)   # #E8A87C canonical

# Character — Byte
BYTE_TEAL       = (  0, 212, 232)   # GL-01b body fill
BYTE_HL         = (  0, 240, 255)   # ELEC_CYAN highlight
BYTE_SH         = (  0, 144, 176)
BYTE_OUTLINE    = (  0, 100, 130)
MONITOR_GLOW    = (  0, 212, 232)

ELEC_CYAN       = (  0, 240, 255)
HOT_MAGENTA     = (255,  45, 107)
UV_PURPLE       = (123,  47, 190)
VOID_BLACK      = ( 10,  10,  20)
CORRUPTED_AMBER = (255, 140,   0)

# Bright specular — value ceiling guarantee (>= 225)
SPECULAR_WHITE  = (255, 252, 240)
SPECULAR_CYAN   = (180, 248, 255)


def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def draw_background(img, draw):
    """
    Draw warm domestic room background with CRT monitor on right.
    FIX 2: Warm/cool separation strategy:
      - Top half receives strong LAMP_AMBER halo (alpha up to 90)
      - Bottom half receives Byte-teal floor bounce (separate pass, see draw_floor_bounce)
    """
    rng = random.Random(42)

    ceiling_y = sy(130)
    floor_y   = sy(680)

    # Ceiling strip (warm dark wood)
    draw.rectangle([0, 0, W, ceiling_y], fill=CEILING_DARK)
    draw.line([(0, ceiling_y), (W, ceiling_y)], fill=(45, 28, 8), width=sp(4))
    # Ceiling warm glow near lamp side
    for i in range(ceiling_y):
        t = i / max(1, ceiling_y)
        r_v = int(CEILING_DARK[0] + (CEILING_COLOR[0] - CEILING_DARK[0]) * t)
        g_v = int(CEILING_DARK[1] + (CEILING_COLOR[1] - CEILING_DARK[1]) * t)
        b_v = int(CEILING_DARK[2] + (CEILING_COLOR[2] - CEILING_DARK[2]) * t)
        draw.line([(0, i), (W, i)], fill=(r_v, g_v, b_v))

    # Back wall — warm gradient (vertical) — bumped warmer in v005
    for row in range(ceiling_y, floor_y):
        t = (row - ceiling_y) / max(1, floor_y - ceiling_y)
        r = int(WALL_UPPER[0] + (WALL_WARM[0] - WALL_UPPER[0]) * t)
        g = int(WALL_UPPER[1] + (WALL_WARM[1] - WALL_UPPER[1]) * t)
        b = int(WALL_UPPER[2] + (WALL_WARM[2] - WALL_UPPER[2]) * t)
        draw.line([(0, row), (W, row)], fill=(r, g, b))

    # Floor base
    draw.rectangle([0, floor_y, W, H - 30], fill=FLOOR_COLOR)
    # Floor shadow at wall base (first band dark, target value ≤ 30)
    for i in range(sp(28)):
        alpha_frac = 1.0 - i / sp(28)
        dark = int(60 * alpha_frac)
        r_ = max(0, FLOOR_COLOR[0] - dark)
        g_ = max(0, FLOOR_COLOR[1] - dark)
        b_ = max(0, FLOOR_COLOR[2] - dark)
        draw.line([(0, floor_y + i), (W, floor_y + i)], fill=(r_, g_, b_))

    # ── Rug (between characters — Byte-teal spill will land here) ────────────
    rug_x0 = sx(300)
    rug_x1 = sx(1050)
    rug_y0 = floor_y - sp(4)
    rug_y1 = floor_y + sp(26)
    draw.rectangle([rug_x0, rug_y0, rug_x1, rug_y1], fill=RUG_BASE)
    # Rug border pattern (warm stripes)
    for stripe_x in range(rug_x0 + sp(8), rug_x1, sp(40)):
        draw.rectangle([stripe_x, rug_y0 + sp(4), stripe_x + sp(14), rug_y1 - sp(4)],
                       fill=RUG_PATTERN)
    draw.rectangle([rug_x0, rug_y0, rug_x1, rug_y1],
                   outline=(120, 68, 32), width=sp(2))

    # ── Couch (lower-left foreground — adds deep shadow, domestic read) ──────
    couch_x0 = sx(-40)
    couch_x1 = sx(560)
    couch_y0 = floor_y - sp(88)
    couch_y1 = floor_y + sp(10)
    couch_arm_w = sp(28)

    # Couch seat
    draw.rectangle([couch_x0, couch_y0 + sp(32), couch_x1, couch_y1],
                   fill=COUCH_BASE)
    # Couch back
    draw.rectangle([couch_x0, couch_y0, couch_x1, couch_y0 + sp(34)],
                   fill=COUCH_SHADOW)
    # Couch cushions
    cushion_w = int((couch_x1 - couch_x0 - couch_arm_w * 2) / 2)
    for ci in range(2):
        cx0 = couch_x0 + couch_arm_w + ci * cushion_w
        cx1 = cx0 + cushion_w - sp(4)
        cy0 = couch_y0 + sp(34)
        cy1 = couch_y1
        draw.rectangle([cx0, cy0, cx1, cy1], fill=COUCH_CUSHION)
        draw.line([(cx0, cy0), (cx0, cy1)], fill=COUCH_SHADOW, width=sp(2))
    # Couch outline
    draw.rectangle([couch_x0, couch_y0, couch_x1, couch_y1],
                   outline=COUCH_SHADOW, width=sp(2))

    # ── Deep shadow under couch (value floor — FIX 4) ─────────────────────────
    # Alpha-composite dark shadow band under couch to hit value ≤ 30 in shadow zone
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow_draw  = ImageDraw.Draw(shadow_layer)
    # Shadow beneath couch (very dark — NEAR_BLACK_WARM base)
    for i in range(sp(18)):
        frac = 1.0 - i / sp(18)
        alpha = int(200 * frac)   # alpha 200 on top → near-black composited
        shadow_draw.line([(couch_x0, couch_y1 - i), (couch_x1, couch_y1 - i)],
                         fill=(*NEAR_BLACK_WARM, alpha))
    # Front shadow of couch (below, on floor)
    for i in range(sp(14)):
        frac = 1.0 - i / sp(14)
        alpha = int(160 * frac)
        shadow_draw.line([(couch_x0, couch_y1 + i), (couch_x1, couch_y1 + i)],
                         fill=(*DEEP_COCOA, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, shadow_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # ── CRT monitor on right side ─────────────────────────────────────────────
    mon_cx = sx(1330)
    mon_cy = sy(440)
    mon_w  = sx(310)
    mon_h  = sy(220)
    mon_x0 = mon_cx - mon_w // 2
    mon_y0 = mon_cy - mon_h // 2
    mon_x1 = mon_cx + mon_w // 2
    mon_y1 = mon_cy + mon_h // 2
    frame_pad = sp(18)

    # Monitor housing (dark plastic)
    draw.rectangle([mon_x0 - frame_pad, mon_y0 - frame_pad,
                    mon_x1 + frame_pad, mon_y1 + frame_pad + sp(30)],
                   fill=(38, 34, 28))
    # Screen glow (BYTE_TEAL gradient — brightest center)
    for step in range(16, 0, -1):
        t = step / 16
        g_r = int(BYTE_TEAL[0] * t * 0.4)
        g_g = int(BYTE_TEAL[1] * t * 0.9)
        g_b = int(BYTE_TEAL[2] * t * 0.95)
        ex = int(mon_w // 2 * t)
        ey = int(mon_h // 2 * t)
        draw.ellipse([mon_cx - ex, mon_cy - ey, mon_cx + ex, mon_cy + ey],
                     fill=(g_r, g_g, g_b))
    # Screen rim
    draw.rectangle([mon_x0, mon_y0, mon_x1, mon_y1],
                   outline=(60, 50, 40), width=sp(3))
    # Screen specular dot (value ceiling >= 225)
    spec_x = mon_cx - mon_w // 4
    spec_y = mon_cy - mon_h // 4
    draw.ellipse([spec_x - sp(6), spec_y - sp(4),
                  spec_x + sp(6), spec_y + sp(4)],
                 fill=SPECULAR_CYAN)

    # Monitor stand
    stand_x = mon_cx - sp(14)
    stand_bot = mon_y1 + frame_pad + sp(30)
    draw.rectangle([stand_x, stand_bot, stand_x + sp(28), stand_bot + sp(18)],
                   fill=(50, 44, 36))
    draw.rectangle([stand_x - sp(20), stand_bot + sp(18),
                    stand_x + sp(48), stand_bot + sp(28)],
                   fill=(44, 38, 30))

    # Monitor ambient glow radiating onto wall / floor (BYTE_TEAL spill)
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw  = ImageDraw.Draw(glow_layer)
    glow_steps = 12
    for gs in range(glow_steps, 0, -1):
        t = gs / glow_steps
        alpha = int(55 * t * t)
        gr  = int(BYTE_TEAL[0] * 0.1)
        gg  = int(BYTE_TEAL[1] * 0.85 * t)
        gb  = int(BYTE_TEAL[2] * 0.90 * t)
        ex  = int(mon_w * 0.9 * (1.0 + (1 - t) * 1.5))
        ey  = int(mon_h * 0.9 * (1.0 + (1 - t) * 1.5))
        glow_draw.ellipse([mon_cx - ex, mon_cy - ey, mon_cx + ex, mon_cy + ey],
                          fill=(gr, gg, gb, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # ── Lamp (upper left) — warm domestic source — FIX 1 ─────────────────────
    # CANONICAL LAMP_AMBER = (255,140,0) = #FF8C00 hue≈33° — replaces (255,200,80)
    lamp_x = sx(200)
    lamp_y = ceiling_y + sy(30)
    # Lamp shade
    shade_pts = [
        (lamp_x - sx(50), lamp_y + sy(40)),
        (lamp_x + sx(50), lamp_y + sy(40)),
        (lamp_x + sx(30), lamp_y),
        (lamp_x - sx(30), lamp_y),
    ]
    draw.polygon(shade_pts, fill=(220, 190, 110))
    draw.polygon(shade_pts, outline=(160, 130, 60), width=sp(2))
    # Lamp bulb (bright warm highlight — >= 225 for value ceiling)
    draw.ellipse([lamp_x - sp(8), lamp_y + sy(28),
                  lamp_x + sp(8), lamp_y + sy(40)],
                 fill=SPECULAR_WHITE)
    # Lamp base
    draw.rectangle([lamp_x - sp(6), lamp_y + sy(40),
                    lamp_x + sp(6), lamp_y + sy(70)],
                   fill=(140, 110, 60))

    # FIX 2: Strong lamp halo — SUNLIT_AMBER canonical (212,146,58), alpha up to 90
    # This dominates the TOP HALF of the image, driving warm/cool separation.
    # v004 used alpha max 40 → insufficient. v005: alpha max 90.
    # Use canonical SUNLIT_AMBER (212,146,58) for color fidelity ΔE compliance.
    # LAMP_AMBER (255,140,0) is reserved for the bright lamp bulb center only.
    SUNLIT_AMBER_CANONICAL = (212, 146, 58)   # RW-03 #D4923A — canonical SUNLIT_AMBER
    lamp_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lamp_draw  = ImageDraw.Draw(lamp_layer)
    for ls in range(20, 0, -1):
        t = ls / 20
        alpha = int(90 * t * t)
        ex = int(sx(200) * (1.0 + (1 - t) * 2.5))
        ey = int(sy(150) * (1.0 + (1 - t) * 2.5))
        lamp_draw.ellipse([lamp_x - ex, lamp_y - ey, lamp_x + ex, lamp_y + ey],
                          fill=(*SUNLIT_AMBER_CANONICAL, alpha))
    # Warm wash across entire top half — drives median hue warm for separation
    # Use SUNLIT_AMBER_CANONICAL for color fidelity compliance
    top_half_y = H // 2
    for row in range(ceiling_y, top_half_y):
        dist_from_lamp = abs(row - lamp_y)
        t = max(0.0, 1.0 - dist_from_lamp / (top_half_y - ceiling_y))
        alpha = int(40 * t * t)
        if alpha > 0:
            lamp_draw.line([(0, row), (W, row)],
                           fill=(*SUNLIT_AMBER_CANONICAL, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, lamp_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    return {
        "ceiling_y": ceiling_y,
        "floor_y":   floor_y,
        "mon_cx":    mon_cx,
        "mon_cy":    mon_cy,
        "mon_x0":    mon_x0,
        "mon_y0":    mon_y0,
        "mon_x1":    mon_x1,
        "mon_y1":    mon_y1,
        "lamp_x":    lamp_x,
        "lamp_y":    lamp_y,
        "couch_x1":  couch_x1,
        "couch_y0":  couch_y0,
        "rug_x0":    rug_x0,
        "rug_x1":    rug_x1,
    }


def draw_floor_bounce(img, draw, bg_data):
    """
    FIX 3: Byte-teal floor bounce between Luma and Byte.
    Specified in scene brief but absent in v004.
    Teal elliptical spill on floor/rug between luma_cx (~420) and byte_cx (~900).

    This also drives warm/cool separation:
    - Bottom half receives a broad teal wash (BYTE_TEAL alpha 85) across the
      entire bottom half. This is the dominant cool source. Floor is warm wood
      → cool must overpower it (C35 lesson: alpha 90 for cool bottom pass).
    - This reads narratively: Byte's digital presence fills the room floor with
      teal light — the physical floor takes on the digital character's glow.

    Separation strategy (C35 proven approach):
      Top half = LAMP_AMBER (hue ~33°, warm)   → high alpha warm wash
      Bottom half = BYTE_TEAL (hue ~185°, cool) → alpha 85 teal wash
      Expected separation: ~150 PIL units (well above 15.0 target)
    """
    floor_y  = bg_data["floor_y"]
    luma_cx  = sx(420)
    byte_cx  = sx(900)
    bounce_cx = (luma_cx + byte_cx) // 2   # midpoint between characters

    bounce_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bounce_draw  = ImageDraw.Draw(bounce_layer)

    # ── Broad teal wash across entire bottom half ─────────────────────────────
    # C35 lesson: "cool must be stronger to dominate the warm floor"
    # alpha 85 — same magnitude as C35 kitchen cool bottom pass (alpha 90)
    # Use BYTE_TEAL (0,212,232) directly — canonical color, passes ΔE check.
    mid_y = H // 2
    for row in range(mid_y, H - 30):
        # Alpha fades gently from full at mid to lighter at bottom edge
        t = (row - mid_y) / max(1, H - 30 - mid_y)
        # Peak alpha at ~60% into bottom half, fade at edges
        fade_t = min(t * 2, 1.0) * min((1.0 - t) * 4, 1.0)
        alpha = int(85 * max(0.4, fade_t))   # minimum 0.4 factor = alpha 34
        bounce_draw.line([(0, row), (W, row)],
                         fill=(*BYTE_TEAL, alpha))

    # ── Radial glow at bounce center (Byte → floor → rug) ────────────────────
    # Brighter teal at bounce source (BYTE_TEAL, more saturated)
    bounce_cy = floor_y + sp(12)
    for bs in range(12, 0, -1):
        t = bs / 12
        alpha = int(90 * t * t)
        ex = int(sx(350) * (1.0 + (1 - t) * 0.5))
        ey = int(sp(50)  * (1.0 + (1 - t) * 0.5))
        gr  = int(BYTE_TEAL[0] * 0.08)
        gg  = int(BYTE_TEAL[1] * 0.90 * t)
        gb  = int(BYTE_TEAL[2] * 0.95 * t)
        bounce_draw.ellipse([bounce_cx - ex, bounce_cy - ey,
                             bounce_cx + ex, bounce_cy + ey],
                            fill=(gr, gg, gb, alpha))

    # Bright teal core on rug (confirms teal source visually)
    bounce_draw.ellipse([bounce_cx - sx(70), bounce_cy - sp(14),
                         bounce_cx + sx(70), bounce_cy + sp(14)],
                        fill=(*BYTE_TEAL, 70))

    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, bounce_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)


def draw_luma(img, draw, bg_data):
    """Draw Luma: left-center, standing, facing right toward Byte."""
    rng = random.Random(100)

    luma_cx   = sx(420)
    floor_y   = bg_data["floor_y"]
    luma_base = floor_y
    head_r    = sp(64)

    def p(n): return int(n * min(SX, SY))

    # Body height: 3.2 heads.
    total_body_h = int(head_r * 6.4)
    head_cy = luma_base - total_body_h + head_r
    head_cx = luma_cx + sp(12)  # slight lean toward Byte

    # ── Legs ──────────────────────────────────────────────────────────────────
    leg_top   = luma_base - int(head_r * 2.5)
    leg_w     = sp(22)
    draw.rectangle([luma_cx - leg_w - sp(4), leg_top,
                    luma_cx - sp(4),          luma_base],
                   fill=JEANS)
    draw.rectangle([luma_cx - leg_w - sp(4), leg_top,
                    luma_cx - sp(4),          leg_top + sp(8)],
                   fill=JEANS_SH)
    draw.rectangle([luma_cx + sp(4),     leg_top,
                    luma_cx + leg_w + sp(4), luma_base],
                   fill=JEANS)
    draw.rectangle([luma_cx + sp(4),     leg_top,
                    luma_cx + leg_w + sp(4), leg_top + sp(8)],
                   fill=JEANS_SH)
    # Shoes
    draw.ellipse([luma_cx - leg_w - sp(10), luma_base - sp(6),
                  luma_cx - sp(4) + sp(10),  luma_base + sp(8)],
                 fill=LINE)
    draw.ellipse([luma_cx + sp(4) - sp(4),  luma_base - sp(6),
                  luma_cx + leg_w + sp(14),  luma_base + sp(8)],
                 fill=LINE)

    # ── Torso / Hoodie ────────────────────────────────────────────────────────
    torso_top = luma_base - int(head_r * 4.2)
    torso_bot = luma_base - int(head_r * 2.5)
    torso_hw  = sp(52)
    wobble_polygon(
        draw,
        [(luma_cx - torso_hw, torso_top), (luma_cx + torso_hw, torso_top),
         (luma_cx + torso_hw + sp(6), torso_bot), (luma_cx - torso_hw - sp(6), torso_bot)],
        color=HOODIE_SHADOW,
        width=sp(3),
        amplitude=sp(2),
        frequency=4,
        seed=200,
        fill=HOODIE_ORANGE,
    )
    draw = ImageDraw.Draw(img)

    # Hoodie pixel-pattern stripe (cyan/teal accent on chest)
    stripe_y = torso_top + int((torso_bot - torso_top) * 0.3)
    for px_i in range(0, torso_hw * 2, sp(6)):
        col = px_i % (sp(12))
        if col < sp(6):
            draw.rectangle([luma_cx - torso_hw + px_i, stripe_y,
                            luma_cx - torso_hw + px_i + sp(4), stripe_y + sp(4)],
                           fill=(0, 180, 210))

    # ── Left arm (reaching right toward Byte) ─────────────────────────────────
    arm_x0 = luma_cx + torso_hw
    arm_y0 = torso_top + int((torso_bot - torso_top) * 0.25)
    arm_x1 = arm_x0 + sp(70)
    arm_y1 = arm_y0 + sp(20)
    draw.rectangle([arm_x0, arm_y0, arm_x1, arm_y1 + sp(10)], fill=HOODIE_ORANGE)
    draw.ellipse([arm_x1 - sp(8), arm_y1 - sp(10),
                  arm_x1 + sp(14), arm_y1 + sp(14)],
                 fill=SKIN)

    # ── Right arm (down at side) ──────────────────────────────────────────────
    arm2_x0 = luma_cx - torso_hw - sp(6)
    arm2_y0 = torso_top + int((torso_bot - torso_top) * 0.2)
    arm2_x1 = arm2_x0 - sp(10)
    arm2_y1 = torso_bot + sp(10)
    draw.rectangle([arm2_x1, arm2_y0, arm2_x0, arm2_y1], fill=HOODIE_ORANGE)

    # ── Neck ──────────────────────────────────────────────────────────────────
    neck_w = sp(18)
    draw.rectangle([head_cx - neck_w, torso_top - sp(16),
                    head_cx + neck_w, torso_top + sp(6)],
                   fill=SKIN)

    # ── Head ──────────────────────────────────────────────────────────────────
    for row in range(head_cy - head_r, head_cy + head_r):
        t_y = (row - head_cy) / max(1, head_r)
        rx_row = int(head_r * math.sqrt(max(0, 1 - t_y * t_y)))
        if rx_row < 1:
            continue
        for col in range(head_cx - rx_row, head_cx + rx_row + 1):
            t_x = (col - head_cx) / max(1, rx_row)
            w_f = 0.5 + 0.5 * t_x
            r_v = int(SKIN[0] * (1 - w_f) + SKIN_HL[0] * w_f)
            g_v = int(SKIN[1] * (1 - w_f) + SKIN_HL[1] * w_f)
            b_v = int(SKIN[2] * (1 - w_f) + SKIN_HL[2] * w_f)
            draw.point((col, row), fill=(r_v, g_v, b_v))

    # Head outline (wobble)
    num_pts = 20
    head_pts = []
    for i in range(num_pts):
        angle = (2 * math.pi * i / num_pts) - math.pi / 2
        hx = head_cx + head_r * math.cos(angle)
        hy = head_cy + head_r * math.sin(angle)
        head_pts.append((hx, hy))
    wobble_polygon(draw, head_pts, color=LINE, width=sp(3),
                   amplitude=sp(2), frequency=5, seed=101, fill=None)
    draw = ImageDraw.Draw(img)

    # Variable stroke arcs
    for arc_i in range(8):
        start_a = (2 * math.pi * arc_i / 8) - math.pi / 2
        end_a   = (2 * math.pi * (arc_i + 1) / 8) - math.pi / 2
        a_p1 = (head_cx + (head_r + sp(1)) * math.cos(start_a),
                head_cy + (head_r + sp(1)) * math.sin(start_a))
        a_p2 = (head_cx + (head_r + sp(1)) * math.cos(end_a),
                head_cy + (head_r + sp(1)) * math.sin(end_a))
        variable_stroke(img, a_p1, a_p2,
                        max_width=sp(5), min_width=sp(1),
                        color=LINE, seed=300 + arc_i)
    draw = ImageDraw.Draw(img)

    # Hair
    draw.chord([head_cx - head_r, head_cy - head_r + p(20),
                head_cx + head_r, head_cy + p(20)],
               start=190, end=350, fill=HAIR_COLOR)
    draw.arc([head_cx - head_r, head_cy - head_r + p(20),
              head_cx + head_r, head_cy + p(20)],
             start=190, end=350, fill=LINE, width=p(4))
    for curl_i, (ca, cr_scale) in enumerate([
        (220, 0.28), (250, 0.24), (280, 0.26), (310, 0.22), (340, 0.24)
    ]):
        ca_rad = math.radians(ca)
        cx_ = head_cx + int(head_r * 0.85 * math.cos(ca_rad))
        cy_ = head_cy + int(head_r * 0.85 * math.sin(ca_rad))
        cr  = int(head_r * cr_scale)
        draw.ellipse([cx_ - cr, cy_ - cr, cx_ + cr, cy_ + cr], fill=HAIR_COLOR)
        draw.ellipse([cx_ - cr, cy_ - cr, cx_ + cr, cy_ + cr],
                     outline=LINE, width=p(3))

    # Eyes (canonical ew = int(head_r * 0.22))
    ew = int(head_r * 0.22)
    eye_y  = head_cy - int(head_r * 0.10)
    eye_lx = head_cx - int(head_r * 0.30)
    eye_rx = head_cx + int(head_r * 0.28)

    EYE_W_C  = (242, 240, 248)
    EYE_IRIS = ( 58,  32,  18)

    for ex_, ey_  in [(eye_lx, eye_y), (eye_rx, eye_y)]:
        draw.ellipse([ex_ - ew, ey_ - int(ew * 1.1),
                      ex_ + ew, ey_ + int(ew * 1.1)],
                     fill=EYE_W_C, outline=LINE, width=p(2))
        draw.ellipse([ex_ - int(ew * 0.55), ey_ - int(ew * 0.55),
                      ex_ + int(ew * 0.55), ey_ + int(ew * 0.55)],
                     fill=EYE_IRIS)
        draw.ellipse([ex_ - int(ew * 0.22), ey_ - int(ew * 0.40),
                      ex_ + int(ew * 0.22), ey_ - int(ew * 0.08)],
                     fill=SPECULAR_WHITE)

    # Blush (#E8A87C canonical)
    blush_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    blush_draw  = ImageDraw.Draw(blush_layer)
    blush_rx = int(head_r * 0.30)
    blush_ry = int(head_r * 0.14)
    blush_y  = eye_y + int(head_r * 0.22)
    blush_draw.ellipse([eye_lx - blush_rx, blush_y - blush_ry,
                        eye_lx + blush_rx, blush_y + blush_ry],
                       fill=(*BLUSH, 65))
    blush_draw.ellipse([eye_rx - blush_rx, blush_y - blush_ry,
                        eye_rx + blush_rx, blush_y + blush_ry],
                       fill=(*BLUSH, 65))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, blush_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Nose hint
    draw.ellipse([head_cx - p(4), head_cy + p(8),
                  head_cx + p(8), head_cy + p(16)],
                 fill=(168, 104, 68))

    # Brows
    wobble_line(draw,
                (eye_lx - ew, eye_y - int(ew * 1.5)),
                (eye_lx + ew, eye_y - int(ew * 1.1)),
                color=LINE, width=p(3), amplitude=p(2), frequency=3, seed=41)
    wobble_line(draw,
                (eye_rx - ew, eye_y - int(ew * 1.1)),
                (eye_rx + ew, eye_y - int(ew * 1.5)),
                color=LINE, width=p(3), amplitude=p(2), frequency=3, seed=51)

    # Smile (open, curious/delighted)
    mouth_cx = head_cx + p(4)
    mouth_y  = head_cy + int(head_r * 0.38)
    draw.arc([mouth_cx - int(head_r * 0.28), mouth_y - p(12),
              mouth_cx + int(head_r * 0.28), mouth_y + p(12)],
             start=10, end=170, fill=LINE, width=p(3))

    return head_cx, head_cy, head_r


def draw_byte(img, draw, bg_data):
    """Draw Byte: right-center, hovering, facing left toward Luma."""
    rng = random.Random(200)

    byte_cx = sx(900)
    floor_y = bg_data["floor_y"]
    byte_cy = floor_y - sp(220)

    body_rx = sp(68)
    body_ry = sp(80)

    # ── Body fill — GL-01b BYTE_TEAL ──────────────────────────────────────────
    for row in range(byte_cy - body_ry, byte_cy + body_ry):
        t_y = (row - byte_cy) / max(1, body_ry)
        rx_row = int(body_rx * math.sqrt(max(0, 1 - t_y * t_y)))
        if rx_row < 1:
            continue
        for col in range(byte_cx - rx_row, byte_cx + rx_row + 1):
            t_x = (col - byte_cx) / max(1, rx_row)
            glow_t = max(0.0, -t_x)
            lit_t  = max(0.0,  t_x)
            r_v = int(BYTE_TEAL[0] * 0.6 + BYTE_TEAL[0] * 0.4 * (1 - lit_t)
                      + 0 * glow_t)
            g_v = int(BYTE_TEAL[1] * 0.6 + BYTE_TEAL[1] * 0.4 * (1 - lit_t)
                      + int(BYTE_TEAL[1] * 0.4) * glow_t)
            b_v = int(BYTE_TEAL[2] * 0.6 + BYTE_TEAL[2] * 0.4 * (1 - lit_t)
                      + int(BYTE_TEAL[2] * 0.4) * glow_t)
            draw.point((col, row), fill=(r_v, g_v, b_v))

    # Outline
    wobble_polygon(
        draw,
        [(byte_cx + body_rx * math.cos(math.radians(a)),
          byte_cy + body_ry * math.sin(math.radians(a)))
         for a in range(0, 360, 18)],
        color=BYTE_OUTLINE,
        width=sp(3),
        amplitude=sp(2),
        frequency=5,
        seed=210,
        fill=None,
    )
    draw = ImageDraw.Draw(img)

    # ── Antenna ────────────────────────────────────────────────────────────────
    antenna_base_x = byte_cx + sp(10)
    antenna_base_y = byte_cy - body_ry
    antenna_tip_x  = antenna_base_x + sp(8)
    antenna_tip_y  = antenna_base_y - sp(44)
    wobble_line(draw,
                (antenna_base_x, antenna_base_y),
                (antenna_tip_x, antenna_tip_y),
                color=BYTE_OUTLINE, width=sp(3), amplitude=sp(2), frequency=3, seed=221)
    draw.ellipse([antenna_tip_x - sp(8), antenna_tip_y - sp(8),
                  antenna_tip_x + sp(8), antenna_tip_y + sp(8)],
                 fill=ELEC_CYAN, outline=BYTE_OUTLINE, width=sp(2))
    draw.ellipse([antenna_tip_x - sp(3), antenna_tip_y - sp(5),
                  antenna_tip_x + sp(3), antenna_tip_y - sp(1)],
                 fill=SPECULAR_WHITE)

    # ── Arms ───────────────────────────────────────────────────────────────────
    arm_lx0 = byte_cx - body_rx
    arm_ly0 = byte_cy + sp(10)
    arm_lx1 = arm_lx0 - sp(50)
    arm_ly1 = arm_ly0 + sp(12)
    draw.rectangle([arm_lx1, arm_ly0 - sp(10), arm_lx0, arm_ly1 + sp(10)],
                   fill=BYTE_TEAL)
    draw.rectangle([arm_lx1, arm_ly0 - sp(10), arm_lx0, arm_ly1 + sp(10)],
                   outline=BYTE_OUTLINE, width=sp(2))
    draw.ellipse([arm_lx1 - sp(14), arm_ly1 - sp(14),
                  arm_lx1 + sp(6),  arm_ly1 + sp(6)],
                 fill=BYTE_TEAL, outline=BYTE_OUTLINE, width=sp(2))

    arm_rx0 = byte_cx + body_rx
    arm_ry0 = byte_cy + sp(10)
    arm_rx1 = arm_rx0 + sp(36)
    arm_ry1 = arm_ry0 + sp(40)
    draw.rectangle([arm_rx0, arm_ry0 - sp(10), arm_rx1, arm_ry1],
                   fill=BYTE_TEAL)
    draw.rectangle([arm_rx0, arm_ry0 - sp(10), arm_rx1, arm_ry1],
                   outline=BYTE_OUTLINE, width=sp(2))

    # ── Face / Display screen ─────────────────────────────────────────────────
    face_rx = int(body_rx * 0.62)
    face_ry = int(body_ry * 0.58)
    face_x0 = byte_cx - face_rx
    face_y0 = byte_cy - face_ry
    face_x1 = byte_cx + face_rx
    face_y1 = byte_cy + face_ry

    draw.rounded_rectangle([face_x0 - sp(4), face_y0 - sp(4),
                             face_x1 + sp(4), face_y1 + sp(4)],
                            radius=sp(8), fill=VOID_BLACK)
    for gs in range(10, 0, -1):
        t = gs / 10
        g_r = int(BYTE_TEAL[0] * 0.15 * t)
        g_g = int(BYTE_TEAL[1] * 0.85 * t)
        g_b = int(BYTE_TEAL[2] * 0.90 * t)
        ex  = int(face_rx * t)
        ey  = int(face_ry * t)
        draw.ellipse([byte_cx - ex, byte_cy - ey, byte_cx + ex, byte_cy + ey],
                     fill=(g_r, g_g, g_b))

    # Eye pixel grid (5x5 system)
    def draw_pixel_eye(ex_center, ey_center, pattern, color, bg_color=VOID_BLACK, cell=sp(8)):
        ox = ex_center - cell * 2
        oy = ey_center - cell * 2
        for row_i, row_str in enumerate(pattern):
            for col_i, ch in enumerate(row_str):
                px = ox + col_i * cell
                py = oy + row_i * cell
                if ch == '1':
                    draw.rectangle([px, py, px + cell - 1, py + cell - 1], fill=color)
                elif ch == 'H':
                    mid_c = tuple(int((a + b) / 2) for a, b in zip(color, bg_color))
                    draw.rectangle([px, py, px + cell - 1, py + cell - 1], fill=mid_c)

    eye_pattern_open = [
        "01110",
        "11111",
        "11111",
        "11111",
        "01110",
    ]
    eye_cy_ = byte_cy - int(body_ry * 0.12)
    eye_lx_ = byte_cx - int(body_rx * 0.36)
    eye_rx_ = byte_cx + int(body_rx * 0.30)
    draw_pixel_eye(eye_lx_, eye_cy_, eye_pattern_open, ELEC_CYAN)
    eye_pattern_mag = [
        "00000",
        "01100",
        "11100",
        "01110",
        "00110",
    ]
    draw_pixel_eye(eye_rx_, eye_cy_, eye_pattern_mag, HOT_MAGENTA)

    draw.ellipse([byte_cx - face_rx + sp(8), byte_cy - face_ry + sp(6),
                  byte_cx - face_rx + sp(16), byte_cy - face_ry + sp(12)],
                 fill=SPECULAR_CYAN)

    # ── Monitor contribution glow on Byte's near side ─────────────────────────
    mon_glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    mon_glow_draw  = ImageDraw.Draw(mon_glow_layer)
    for gs in range(8, 0, -1):
        t = gs / 8
        alpha = int(50 * t * t)
        ex  = int(body_rx * 0.8 * (2.0 - t))
        ey  = int(body_ry * 0.5 * (2.0 - t))
        mon_glow_draw.ellipse([byte_cx, byte_cy - ey, byte_cx + ex, byte_cy + ey],
                              fill=(*BYTE_TEAL, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, mon_glow_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Hover shadow on floor
    shadow_y = floor_y + sp(6)
    shadow_rx = int(body_rx * 0.85)
    shadow_ry = sp(12)
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow_draw  = ImageDraw.Draw(shadow_layer)
    shadow_draw.ellipse([byte_cx - shadow_rx, shadow_y - shadow_ry,
                         byte_cx + shadow_rx, shadow_y + shadow_ry],
                        fill=(20, 20, 15, 80))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, shadow_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    return byte_cx, byte_cy


def generate():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    img  = Image.new("RGB", (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # STEP 1: Background (room + couch + rug + monitor + lamp)
    bg_data = draw_background(img, draw)
    draw = ImageDraw.Draw(img)

    # STEP 2: Byte-teal floor bounce (before characters, so characters sit on top)
    draw_floor_bounce(img, draw, bg_data)
    draw = ImageDraw.Draw(img)

    # STEP 3: Luma
    luma_head_cx, luma_head_cy, luma_head_r = draw_luma(img, draw, bg_data)
    draw = ImageDraw.Draw(img)

    # STEP 4: Luma face lighting — warm upper-left lamp
    add_face_lighting(
        img,
        face_center=(luma_head_cx, luma_head_cy),
        face_radius=(luma_head_r, luma_head_r),
        light_dir=(-1.0, -1.0),
        shadow_color=SKIN_SH,
        highlight_color=SKIN_HL,
        seed=500,
    )
    draw = ImageDraw.Draw(img)

    # STEP 5: Luma rim light — cool CRT/monitor teal from right
    add_rim_light(
        img,
        threshold=185,
        light_color=(0, 212, 232),
        width=sp(3),
        side="right",
        char_cx=luma_head_cx,
    )
    draw = ImageDraw.Draw(img)

    # STEP 6: Byte
    byte_cx, byte_cy = draw_byte(img, draw, bg_data)
    draw = ImageDraw.Draw(img)

    # STEP 7: Byte rim light — warm lamp glow from left
    add_rim_light(
        img,
        threshold=185,
        light_color=LAMP_AMBER,       # FIX 1: canonical #FF8C00 instead of (255,200,80)
        width=sp(2),
        side="left",
        char_cx=byte_cx,
    )
    draw = ImageDraw.Draw(img)

    # STEP 8: Interaction spark between Luma's hand and Byte's arm
    spark_x = int((luma_head_cx + sp(130) + byte_cx - sp(68)) / 2)
    spark_y = int(bg_data["floor_y"] - sp(180))
    spark_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    spark_draw  = ImageDraw.Draw(spark_layer)
    for gs in range(8, 0, -1):
        t = gs / 8
        alpha = int(120 * t * t)
        ex = int(sp(30) * (2.0 - t))
        ey = int(sp(20) * (2.0 - t))
        spark_draw.ellipse([spark_x - ex, spark_y - ey, spark_x + ex, spark_y + ey],
                           fill=(200, 248, 255, alpha))
    spark_draw.ellipse([spark_x - sp(6), spark_y - sp(4),
                        spark_x + sp(6), spark_y + sp(4)],
                       fill=(*SPECULAR_WHITE, 200))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, spark_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # STEP 9: Top/bottom vignette
    vignette = Image.new("RGB", (W, H), (0, 0, 0))
    v_alpha  = Image.new("L", (W, H), 0)
    v_draw   = ImageDraw.Draw(v_alpha)
    for i in range(60):
        t = 1.0 - i / 60.0
        alpha_val = int(70 * t)
        v_draw.line([(0, i), (W, i)], fill=alpha_val)
        v_draw.line([(0, H - 1 - i), (W, H - 1 - i)], fill=alpha_val)
    img = Image.composite(vignette, img, v_alpha)
    draw = ImageDraw.Draw(img)

    # STEP 10: Title strip
    font_xs = load_font(11)
    draw.rectangle([0, H - 30, W, H], fill=(20, 12, 8))
    draw.text((10, H - 22),
              "LUMA & THE GLITCHKIN — Frame 04: The Dynamic  |  C41 — Full Rebuild v005",
              fill=(180, 150, 100), font=font_xs)

    # STEP 11: Image size rule
    if img.width > 1280 or img.height > 1280:
        img.thumbnail((1280, 1280), Image.LANCZOS)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  ({img.width}x{img.height})")

    # ── Inline QA diagnostics ─────────────────────────────────────────────────
    import colorsys

    pixels = list(img.getdata())
    max_brightness = max(max(r, g, b) for r, g, b in pixels)
    min_brightness = min(max(r, g, b) for r, g, b in pixels)
    print(f"Value ceiling (max channel): {max_brightness}  (need >= 225)")
    print(f"Value floor   (max channel): {min_brightness}  (target <= 30)")
    if max_brightness >= 225:
        print("  VALUE CEILING: PASS")
    else:
        print("  VALUE CEILING: FAIL")
    if min_brightness <= 30:
        print("  VALUE FLOOR: PASS")
    else:
        print("  VALUE FLOOR: WARN (check deep shadow zones)")

    # Warm/cool separation: top half vs bottom half median hue
    mid_y = img.height // 2
    top_hues = []
    bot_hues = []
    for idx, (r_val, g_val, b_val) in enumerate(pixels):
        row = idx // img.width
        h_s_v = colorsys.rgb_to_hsv(r_val / 255, g_val / 255, b_val / 255)
        if h_s_v[1] > 0.05 and h_s_v[2] > 0.1:   # skip grey/black pixels
            hue_pil = h_s_v[0] * 255   # convert to PIL 0–255 hue scale
            if row < mid_y:
                top_hues.append(hue_pil)
            else:
                bot_hues.append(hue_pil)

    if top_hues and bot_hues:
        top_hues.sort()
        bot_hues.sort()
        top_median = top_hues[len(top_hues) // 2]
        bot_median = bot_hues[len(bot_hues) // 2]
        separation = abs(top_median - bot_median)
        print(f"Warm/cool separation: {separation:.1f} PIL units  (top={top_median:.1f} bot={bot_median:.1f})")
        print(f"  Threshold (REAL_INTERIOR): 12.0  |  Target: >= 15.0")
        if separation >= 15.0:
            print("  WARM/COOL: PASS (>= 15.0 target)")
        elif separation >= 12.0:
            print("  WARM/COOL: PASS (>= 12.0 threshold, but below 15.0 target)")
        else:
            print(f"  WARM/COOL: FAIL ({separation:.1f} < 12.0)")
    else:
        print("  WARM/COOL: could not compute (insufficient colored pixels)")

    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
