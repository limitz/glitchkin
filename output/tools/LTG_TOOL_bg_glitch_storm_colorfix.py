#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_bg_glitch_storm_colorfix.py
Style Frame 02 — "Glitch Storm" Background-Only Generator (Color Fix)
"Luma & the Glitchkin" — Cycle 13

Author: Jordan Reed, Background & Environment Artist
Date: 2026-03-29
Based on: LTG_TOOL_style_frame_02_glitch_storm.py (Cycle 12)

Color Fix (ENV-06 Terracotta — Naomi CRITICAL):
  The building terracotta wall color RGB(154, 140, 138) in v001 was WRONG.
  Under Electric Cyan key light, G and B channels must individually exceed R
  for the surface to read cool/cyan-tinted rather than warm grey.

  v001 value: RGB(154, 140, 138) — G=140 < R=154, B=138 < R=154  [FAILS: reads warm grey]

  Fix derivation (starting from unlit terracotta ~RGB(180, 120, 90)):
    R: 180 - 30 = 150
    G: 120 + 52 = 172
    B:  90 + 72 = 162
  TERRACOTTA_CYAN_LIT = RGB(150, 172, 162)
  Verify: G=172 > R=150 [PASS], B=162 > R=150 [PASS], G+B=334 > R+R=300 [PASS]

  Named constant TERRACOTTA_CYAN_LIT is exported for Alex Chen to incorporate
  when compositing characters in the v002 style frame.

Changes from v001:
  - TERRA_CYAN_LIT renamed to TERRACOTTA_CYAN_LIT with corrected value
  - Characters and townspeople REMOVED (background-only for compositing)
  - Output filename: LTG_ENV_glitch_storm_bg.png (ENV category, bg-only)
  - No title bar (standalone BG exports do not get title bars)

Coordination note for Alex Chen (LTG_TOOL_style_frame_02_glitch_storm.py):
  Import or copy TERRACOTTA_CYAN_LIT = (150, 172, 162) from this file.
  Replace TERRA_CYAN_LIT = (154, 140, 138) with TERRACOTTA_CYAN_LIT everywhere.

Output: /home/wipkat/team/output/backgrounds/environments/
        LTG_ENV_glitch_storm_bg.png  (1920x1080, background only, no characters)

Usage: python3 LTG_TOOL_bg_glitch_storm_colorfix.py
"""

import os
import math
import random
from PIL import Image, ImageDraw

# ── Output ────────────────────────────────────────────────────────────────────
OUTPUT_PATH = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_glitch_storm_bg.png"
W, H = 1920, 1080

# ── Master Palette — from master_palette.md ───────────────────────────────────
# Real World
WARM_CREAM      = (250, 240, 220)
SOFT_GOLD       = (232, 201,  90)
SUNLIT_AMBER    = (212, 146,  58)
TERRACOTTA      = (199,  91,  57)
SAGE_GREEN      = (122, 158, 126)
DUSTY_LAVENDER  = (168, 155, 191)

# Glitch Layer
VOID_BLACK      = ( 10,  10,  20)   # GL-01
ELEC_CYAN       = (  0, 240, 255)   # GL-02  #00F0FF
ACID_GREEN      = ( 57, 255,  20)   # GL-03  (NOT used in storm confetti)
DATA_BLUE       = ( 43, 127, 255)   # GL-04  #2B7FFF
UV_PURPLE       = (123,  47, 190)   # GL-05  #7B2FBE
HOT_MAGENTA     = (255,  45, 107)   # GL-06  #FF2D6B
STATIC_WHITE    = (240, 240, 240)   # GL-07  #F0F0F0
CORRUPT_AMBER   = (255, 140,   0)   # GL-08  #FF8C00

# Scene-specific ENV colors (from style_frame_02_glitch_storm.md)
NIGHT_SKY_DEEP  = ( 26,  20,  40)   # ENV base — deep blue-purple night  #1A1428
DARK_ASPHALT    = ( 42,  42,  56)   # ENV-01 road base (nighttime)
CYAN_ROAD       = ( 42,  90, 106)   # ENV-02 road under cyan pool
WARM_ROAD       = ( 74,  58,  42)   # ENV-03 road under warm window light
COOL_SIDEWALK   = ( 58,  56,  72)   # ENV-04 sidewalk

# ENV-06 CORRECTED — terracotta wall under Electric Cyan key light
# WRONG (v001): TERRA_CYAN_LIT = (154, 140, 138)  — G < R, B < R — reads warm grey
# CORRECT: derived from unlit terracotta ~(180,120,90): R-30, G+52, B+72
# G=172 > R=150 [PASS], B=162 > R=150 [PASS], G+B=334 > R+R=300 [PASS]
TERRACOTTA_CYAN_LIT = (150, 172, 162)   # ENV-06 — cyan-lit terracotta (Cycle 13 fix)

DEEP_WARM_SHAD  = ( 90,  56,  32)   # ENV-07 walls facing away from storm
ROOF_EDGE       = ( 26,  24,  32)   # ENV-08 roof lines
DEEP_COCOA      = ( 59,  40,  32)   # character hair, power lines


# ── Seeded RNG ────────────────────────────────────────────────────────────────
RNG = random.Random(42)


# ── Helpers ───────────────────────────────────────────────────────────────────

def lerp_color(c1, c2, t):
    """Linear interpolate between two RGB tuples."""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def alpha_paste(base, overlay_rgba):
    """Alpha-composite an RGBA overlay onto a base RGB image. Returns new RGB image."""
    base_rgba = base.convert("RGBA")
    base_rgba.alpha_composite(overlay_rgba)
    return base_rgba.convert("RGB")


# ── Layer 1: Sky ──────────────────────────────────────────────────────────────

def draw_sky(img):
    """Renders the storm sky: deep night gradient, UV purple cloud masses, crack."""
    draw = ImageDraw.Draw(img)

    # Base gradient: top = VOID_BLACK, mid/lower = NIGHT_SKY_DEEP
    for y in range(H):
        t = y / H
        col = lerp_color(VOID_BLACK, NIGHT_SKY_DEEP, min(t * 2.5, 1.0))
        draw.line([(0, y), (W, y)], fill=col)

    # UV_PURPLE cloud masses
    _draw_uv_cloud_masses(img)

    # Atmosphere haze at horizon
    _draw_horizon_haze(img)

    # Primary crack
    _draw_main_crack(img)

    # Secondary sub-cracks
    _draw_sub_cracks(img)

    # Storm edge HOT_MAGENTA burn lines
    _draw_storm_edges(img)

    return img


def _draw_uv_cloud_masses(img):
    """Angular, blocky UV Purple cloud masses in the upper sky."""
    draw = ImageDraw.Draw(img)

    cloud_shapes = [
        (0,    0,  520, 220),
        (80,  60,  380, 160),
        (20, 120,  260,  80),
        (460,  0,  200, 140),
        (380, 80,  180, 120),
    ]
    for (cx, cy, cw, ch) in cloud_shapes:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle([cx, cy, cx + cw, cy + ch], fill=(*UV_PURPLE, 200))
        bite_x = cx + int(cw * 0.55)
        bite_y = cy + int(ch * 0.30)
        od.rectangle([bite_x, bite_y, cx + cw, bite_y + int(ch * 0.40)],
                     fill=(*VOID_BLACK, 255))
        img = alpha_paste(img, overlay)
        draw = ImageDraw.Draw(img)

    cloud_shapes_r = [
        (1380,  0,  540, 300),
        (1500, 60,  420, 200),
        (1620, 20,  300, 160),
        (1760, 80,  160, 240),
        (1350, 160, 380, 140),
    ]
    for (cx, cy, cw, ch) in cloud_shapes_r:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle([cx, cy, cx + cw, cy + ch], fill=(*UV_PURPLE, 210))
        core_x = cx + int(cw * 0.25)
        core_y = cy + int(ch * 0.25)
        od.rectangle([core_x, core_y, core_x + int(cw * 0.50),
                      core_y + int(ch * 0.50)], fill=(*VOID_BLACK, 255))
        img = alpha_paste(img, overlay)
        draw = ImageDraw.Draw(img)

    return img


def _draw_horizon_haze(img):
    """Faint UV purple haze above rooftops (lower sky zone)."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    horizon_y = int(H * 0.55)
    haze_height = int(H * 0.15)
    for dy in range(haze_height):
        t = 1.0 - (dy / haze_height)
        a = int(40 * t)
        od.line([(0, horizon_y - dy), (W, horizon_y - dy)],
                fill=(*UV_PURPLE, a))
    return alpha_paste(img, overlay)


def _draw_main_crack(img):
    """Primary sky crack: upper-right to lower-center. ELEC_CYAN + HOT_MAGENTA edges."""
    crack_pts = [
        (1820, 0),
        (1700, 80),
        (1700, 140),
        (1600, 220),
        (1520, 220),
        (1460, 340),
        (1380, 420),
        (1380, 500),
        (1280, 580),
        (1200, 640),
    ]

    glow_specs = [
        (HOT_MAGENTA, 18, 80),
        (ELEC_CYAN,   12, 180),
        (ELEC_CYAN,    6, 240),
        (STATIC_WHITE, 3, 220),
    ]

    for (color, half_w, alpha) in glow_specs:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        for i in range(len(crack_pts) - 1):
            x0, y0 = crack_pts[i]
            x1, y1 = crack_pts[i + 1]
            od.line([(x0, y0), (x1, y1)], fill=(*color, alpha), width=half_w * 2)
        img = alpha_paste(img, overlay)

    return img


def _draw_sub_cracks(img):
    """Secondary branching cracks from main crack."""
    sub_cracks = [
        (1700, 140, 1750, 50),
        (1600, 220, 1560, 160),
        (1460, 340, 1520, 400),
        (1380, 420, 1320, 380),
        (1280, 580, 1240, 520),
        (1380, 500, 1440, 560),
        (1200, 640, 1160, 680),
    ]

    for (x0, y0, x1, y1) in sub_cracks:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.line([(x0, y0), (x1, y1)], fill=(*ELEC_CYAN, 160), width=4)
        mid_x = (x0 + x1) // 2
        mid_y = (y0 + y1) // 2
        od.line([(mid_x, mid_y), (x1, y1)], fill=(*DATA_BLUE, 120), width=2)
        img = alpha_paste(img, overlay)

    return img


def _draw_storm_edges(img):
    """HOT_MAGENTA burn lines along cloud mass edges."""
    draw = ImageDraw.Draw(img)
    burn_lines = [
        ((460,  0), (520, 30)),
        ((380, 80), (440, 110)),
        ((80,  60), (110, 90)),
        ((1380, 0), (1360, 50)),
        ((1500, 60), (1480, 110)),
        ((1760, 80), (1720, 130)),
        ((1350, 160), (1380, 200)),
    ]
    for pt1, pt2 in burn_lines:
        draw.line([pt1, pt2], fill=HOT_MAGENTA, width=3)
    return img


# ── Layer 2: Pixel Confetti (storm zone) ─────────────────────────────────────

def draw_storm_confetti(img):
    """
    Storm confetti: ELEC_CYAN, STATIC_WHITE, HOT_MAGENTA, UV_PURPLE only.
    ACID_GREEN FORBIDDEN (master_palette Forbidden #8).
    """
    draw = ImageDraw.Draw(img)
    confetti_colors = [ELEC_CYAN, STATIC_WHITE, HOT_MAGENTA, UV_PURPLE]

    for _ in range(240):
        cx = RNG.randint(1100, 1900)
        cy = RNG.randint(0, int(H * 0.55))
        dist = math.sqrt((cx - 1400) ** 2 + (cy - 300) ** 2)
        max_dist = 700.0
        t = clamp(dist / max_dist, 0.0, 1.0)
        size = int(15 - (15 - 3) * t)
        color = RNG.choice(confetti_colors)
        draw.rectangle([cx, cy, cx + size, cy + size], fill=color)

    for _ in range(160):
        cx = RNG.randint(600, 1900)
        cy = RNG.randint(int(H * 0.25), int(H * 0.60))
        size = RNG.randint(3, 8)
        color = RNG.choice(confetti_colors)
        alpha_draw = RNG.randint(140, 220)
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle([cx, cy, cx + size, cy + size], fill=(*color, alpha_draw))
        img = alpha_paste(img, overlay)

    draw = ImageDraw.Draw(img)
    for _ in range(80):
        cx = RNG.randint(300, 900)
        cy = RNG.randint(int(H * 0.65), H)
        size = RNG.randint(2, 4)
        color = RNG.choice(confetti_colors)
        draw.rectangle([cx, cy, cx + size, cy + size], fill=color)

    return img


# ── Layer 3: Town Silhouette ──────────────────────────────────────────────────

def draw_town_silhouette(img):
    """
    Millbrook at night: rooftops, chimneys, clock tower, power lines.
    Warm window glows. Buildings lit by Cyan key on right-facing walls.
    Uses TERRACOTTA_CYAN_LIT (Cycle 13 fix) — G and B both exceed R.
    """
    draw = ImageDraw.Draw(img)

    horizon_y = int(H * 0.58)

    buildings = [
        (0,      horizon_y - 160, 180, horizon_y, DEEP_WARM_SHAD),
        (150,    horizon_y - 200, 320, horizon_y, DEEP_WARM_SHAD),
        (300,    horizon_y - 140, 440, horizon_y, TERRACOTTA_CYAN_LIT),   # cyan-lit face (FIXED)
        (420,    horizon_y - 260, 560, horizon_y, DEEP_WARM_SHAD),
        (540,    horizon_y - 180, 680, horizon_y, TERRACOTTA_CYAN_LIT),   # FIXED
        (660,    horizon_y - 340, 760, horizon_y, DEEP_WARM_SHAD),
        (690,    horizon_y - 420, 730, horizon_y - 340, DEEP_WARM_SHAD),
        (760,    horizon_y - 190, 900, horizon_y, TERRACOTTA_CYAN_LIT),   # FIXED
        (880,    horizon_y - 150, 1020, horizon_y, DEEP_WARM_SHAD),
        (1000,   horizon_y - 220, 1140, horizon_y, TERRACOTTA_CYAN_LIT),  # FIXED
        (1120,   horizon_y - 170, 1260, horizon_y, DEEP_WARM_SHAD),
        (1240,   horizon_y - 240, 1380, horizon_y, TERRACOTTA_CYAN_LIT),  # FIXED
        (1360,   horizon_y - 130, 1500, horizon_y, DEEP_WARM_SHAD),
        (1480,   horizon_y - 200, 1620, horizon_y, TERRACOTTA_CYAN_LIT),  # FIXED
        (1600,   horizon_y - 160, 1740, horizon_y, DEEP_WARM_SHAD),
        (1720,   horizon_y - 210, W,    horizon_y, TERRACOTTA_CYAN_LIT),  # FIXED
    ]

    for (lx, ry, rx, gy, col) in buildings:
        draw.rectangle([lx, ry, rx, gy], fill=col)

    chimneys = [
        (200, horizon_y - 220, 215, horizon_y - 190),
        (380, horizon_y - 215, 395, horizon_y - 190),
        (480, horizon_y - 280, 495, horizon_y - 250),
        (870, horizon_y - 210, 885, horizon_y - 180),
        (1050, horizon_y - 240, 1065, horizon_y - 210),
        (1300, horizon_y - 260, 1315, horizon_y - 230),
        (1550, horizon_y - 220, 1565, horizon_y - 190),
    ]
    for (x0, y0, x1, y1) in chimneys:
        draw.rectangle([x0, y0, x1, y1], fill=DEEP_COCOA)

    _draw_building_windows(img, buildings, horizon_y)
    _draw_power_lines(img, horizon_y)

    draw = ImageDraw.Draw(img)
    for (x0, y0, x1, y1) in chimneys[:3]:
        draw.line([(x0, y0), (x0, y1)], fill=(*ELEC_CYAN, 60), width=1)

    return img


def _draw_building_windows(img, buildings, horizon_y):
    """Warm window glows on building faces."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    win_colors = [(*SOFT_GOLD, 180), (*WARM_CREAM, 160)]

    for (lx, ry, rx, gy, _) in buildings:
        bld_w = rx - lx
        bld_h = gy - ry
        if bld_w < 60 or bld_h < 60:
            continue
        win_w = max(12, bld_w // 5)
        win_h = max(10, bld_h // 6)
        for row in range(2):
            for col in range(2):
                wx = lx + int(bld_w * (0.2 + col * 0.45))
                wy = ry + int(bld_h * (0.20 + row * 0.40))
                col_choice = RNG.choice(win_colors)
                if RNG.random() < 0.35:
                    continue
                od.rectangle([wx, wy, wx + win_w, wy + win_h], fill=col_choice)

    img = alpha_paste(img, overlay)
    return img


def _draw_power_lines(img, horizon_y):
    """Thin catenary power lines between buildings."""
    draw = ImageDraw.Draw(img)
    poles = [120, 320, 520, 760, 950, 1150, 1350, 1550, 1750]
    wire_y = horizon_y - 100
    for i in range(len(poles) - 1):
        x0, x1 = poles[i], poles[i + 1]
        sag = int((x1 - x0) * 0.06)
        pts = []
        for s in range(6):
            t = s / 5.0
            x = int(x0 + t * (x1 - x0))
            y = wire_y + int(sag * 4 * t * (1 - t))
            pts.append((x, y))
        for j in range(len(pts) - 1):
            draw.line([pts[j], pts[j + 1]], fill=DEEP_COCOA, width=1)
    return img


# ── Layer 4: Street ───────────────────────────────────────────────────────────

def draw_street(img):
    """Road surface, sidewalk, cyan light pool, warm window spill zones."""
    draw = ImageDraw.Draw(img)

    horizon_y = int(H * 0.58)
    street_bottom = H

    draw.rectangle([0, horizon_y, W, street_bottom], fill=DARK_ASPHALT)

    sidewalk_top = horizon_y
    sidewalk_bottom = horizon_y + int((street_bottom - horizon_y) * 0.12)
    draw.rectangle([0, sidewalk_top, W, sidewalk_bottom], fill=COOL_SIDEWALK)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    crack_floor_x = 1200
    pool_width = 560
    pool_height = int((street_bottom - horizon_y) * 0.7)
    for col in range(pool_width):
        t = col / pool_width
        falloff = (1 - t) ** 2.0
        a = int(55 * falloff)
        x = crack_floor_x - col
        od.line([(x, horizon_y), (x, horizon_y + pool_height)],
                fill=(*CYAN_ROAD, a))
    img = alpha_paste(img, overlay)

    overlay2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od2 = ImageDraw.Draw(overlay2)
    spill_w = 420
    spill_h = int((street_bottom - horizon_y) * 0.35)
    for col in range(spill_w):
        t = col / spill_w
        falloff = (1 - t) ** 2.2
        a = int(40 * falloff)
        od2.line([(col, sidewalk_bottom), (col, sidewalk_bottom + spill_h)],
                 fill=(*SOFT_GOLD, a))
    img = alpha_paste(img, overlay2)

    draw = ImageDraw.Draw(img)
    draw.line([(0, sidewalk_bottom), (W, sidewalk_bottom)], fill=VOID_BLACK, width=2)

    return img


# ── Layer 5: Shattered Storefront (right foreground) ─────────────────────────

def draw_storefront(img):
    """Right foreground: shattered storefront window."""
    draw = ImageDraw.Draw(img)

    horizon_y = int(H * 0.58)
    sf_left  = int(W * 0.80)
    sf_right = W
    sf_top   = horizon_y - 80
    sf_bot   = horizon_y + int((H - horizon_y) * 0.55)

    MUTED_TEAL = (91, 140, 138)

    draw.rectangle([sf_left, sf_top, sf_right, sf_bot], outline=MUTED_TEAL, width=6)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([sf_left + 6, sf_top + 6, sf_right - 6, sf_bot - 6],
                 fill=(*VOID_BLACK, 200))
    interior_cx = (sf_left + sf_right) // 2
    interior_cy = (sf_top + sf_bot) // 2
    for r in range(60, 0, -10):
        a = int(30 * (1 - r / 60.0))
        od.ellipse([interior_cx - r, interior_cy - r,
                    interior_cx + r, interior_cy + r],
                   fill=(*UV_PURPLE, a))
    img = alpha_paste(img, overlay)
    draw = ImageDraw.Draw(img)

    glass_shards = [
        [(sf_left + 20, sf_top + 10), (sf_left + 60, sf_top + 8),
         (sf_left + 35, sf_top + 45)],
        [(sf_left + 80, sf_top + 5), (sf_left + 130, sf_top + 12),
         (sf_left + 100, sf_top + 55)],
        [(sf_left + 50, sf_top + 30), (sf_left + 90, sf_top + 25),
         (sf_left + 70, sf_top + 70)],
        [(sf_left + 10, sf_top + 50), (sf_left + 45, sf_top + 45),
         (sf_left + 25, sf_top + 85)],
    ]
    for shard in glass_shards:
        draw.polygon(shard, fill=STATIC_WHITE, outline=(*ELEC_CYAN, 180))

    crack_origins = [
        (sf_left + 40, sf_top + 20),
        (sf_left + 110, sf_top + 30),
        (sf_left, sf_top + 60),
    ]
    for (ox, oy) in crack_origins:
        for angle_offset in [-30, 0, 30]:
            angle = math.radians(200 + angle_offset)
            length = RNG.randint(60, 120)
            ex = int(ox + math.cos(angle) * length)
            ey = int(oy + math.sin(angle) * length)
            draw.line([(ox, oy), (ex, ey)], fill=HOT_MAGENTA, width=3)
            draw.line([(ox, oy), (ex, ey)], fill=ELEC_CYAN, width=1)
        for _ in range(8):
            px = ox + RNG.randint(-30, 30)
            py = oy + RNG.randint(-20, 40)
            ps = RNG.randint(3, 8)
            col = RNG.choice([ELEC_CYAN, HOT_MAGENTA, UV_PURPLE, STATIC_WHITE])
            draw.rectangle([px, py, px + ps, py + ps], fill=col)

    return img


# ── Layer 6: Ground Lighting ──────────────────────────────────────────────────

def draw_ground_lighting(img):
    """Strong cyan pool on tarmac directly below crack, fading left."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    horizon_y = int(H * 0.58)

    crack_x = 1300
    for col in range(700):
        x = crack_x - col
        if x < 0:
            break
        t = col / 700.0
        falloff = (1 - t) ** 1.8
        a = int(45 * falloff)
        od.line([(x, horizon_y), (x, H)], fill=(*ELEC_CYAN, a))

    img = alpha_paste(img, overlay)
    return img


# ── Layer 7: Dutch Angle (4 degrees clockwise) ───────────────────────────────

def apply_dutch_angle(img, degrees=4.0):
    """4-degree clockwise camera tilt. Expand then center-crop to 1920x1080."""
    rotated = img.rotate(-degrees, expand=True, resample=Image.BICUBIC,
                         fillcolor=VOID_BLACK)
    rw, rh = rotated.size
    cx, cy = rw // 2, rh // 2
    left   = cx - W // 2
    top    = cy - H // 2
    return rotated.crop((left, top, left + W, top + H))


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("LTG_TOOL_bg_glitch_storm_colorfix.py")
    print("Rendering Glitch Storm background (ENV-06 color fix, BG only)...")
    print(f"TERRACOTTA_CYAN_LIT = {TERRACOTTA_CYAN_LIT}")
    print(f"  G={TERRACOTTA_CYAN_LIT[1]} > R={TERRACOTTA_CYAN_LIT[0]}: "
          f"{'PASS' if TERRACOTTA_CYAN_LIT[1] > TERRACOTTA_CYAN_LIT[0] else 'FAIL'}")
    print(f"  B={TERRACOTTA_CYAN_LIT[2]} > R={TERRACOTTA_CYAN_LIT[0]}: "
          f"{'PASS' if TERRACOTTA_CYAN_LIT[2] > TERRACOTTA_CYAN_LIT[0] else 'FAIL'}")
    g_plus_b = TERRACOTTA_CYAN_LIT[1] + TERRACOTTA_CYAN_LIT[2]
    r_plus_r = TERRACOTTA_CYAN_LIT[0] * 2
    print(f"  G+B={g_plus_b} > R+R={r_plus_r}: "
          f"{'PASS' if g_plus_b > r_plus_r else 'FAIL'}")

    img = Image.new("RGB", (W, H), VOID_BLACK)

    print("  [1/7] Sky gradient + UV cloud masses + crack...")
    img = draw_sky(img)

    print("  [2/7] Storm pixel confetti...")
    img = draw_storm_confetti(img)

    print("  [3/7] Town silhouette (TERRACOTTA_CYAN_LIT applied)...")
    img = draw_town_silhouette(img)

    print("  [4/7] Street surface + light pools...")
    img = draw_street(img)

    print("  [5/7] Ground lighting (cyan pool)...")
    img = draw_ground_lighting(img)

    print("  [6/7] Shattered storefront (right foreground)...")
    img = draw_storefront(img)

    print("  [7/7] Dutch angle (4-degree clockwise)...")
    img = apply_dutch_angle(img, degrees=4.0)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img.save(OUTPUT_PATH, "PNG")
    print(f"\nSaved: {OUTPUT_PATH}")
    print(f"Size: {img.size[0]}x{img.size[1]}")

    size_bytes = os.path.getsize(OUTPUT_PATH)
    print(f"File size: {size_bytes:,} bytes ({size_bytes // 1024} KB)")
    print("\nDone. Background only — no characters. Alex Chen to composite on top.")
    print("Coordination: use TERRACOTTA_CYAN_LIT = (150, 172, 162) in v002.")


if __name__ == "__main__":
    main()
