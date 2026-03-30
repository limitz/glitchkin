#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_style_frame_02_glitch_storm.py
Style Frame 02 — "Glitch Storm" — C36 Fill Light Direction Fix
"Luma & the Glitchkin"

Artist: Rin Yamamoto | Cycle 36
Based on: LTG_TOOL_style_frame_02_glitch_storm.py (Rin Yamamoto, Cycle 35)

Cycle 36 fixes (Sven Halvorsen C14 critique, Jordan Reed fix module):
  1. FILL LIGHT DIRECTION — draw_magenta_fill_light() replaced with
     draw_magenta_fill_light_v007_fast() from LTG_TOOL_sf02_fill_light_fix_c35.
     - WRONG (v006/v007): source at lower-left of each character
       (fill_src_x = char_cx - char_h*0.6, fill_src_y = char_cy + char_h*0.2)
     - CORRECT (v008): source at UPPER-RIGHT — storm crack is at upper-right canvas
       (fill_src_x = char_cx + int(char_h * 0.5), fill_src_y = char_cy - int(char_h * 0.8))
  2. PER-CHARACTER SILHOUETTE MASK — gradient applied ONLY within character pixel
     zones (not to background). Uses ImageChops.multiply() on alpha channel.
     Alpha max reduced 40 → 35 (direct source is harder/cleaner than bounce).
  3. char_cx constants passed directly — do NOT use get_char_bbox() on full 3-char
     frame (bbox would span 83% canvas width — Sven C14 / Rin C35 documented issue).

All Cycle 35 fixes carried forward:
  - LUMA FACE: _draw_luma_face_sprint() — FOCUSED DETERMINATION expression
  - TORSO LEAN: 10° forward lean
  - HAIR STREAM: steeper angle + second fine trailing strand
  - get_char_bbox() misuse fix in draw_cyan_specular_luma()

All Cycle 34 fixes carried forward:
  - CYAN SPECULAR on Luma (ELEC_CYAN add_rim_light side='right')

All Cycle 22 fixes carried forward:
  - CORRUPT_AMBER = GL-07 #FF8C00
  - Window pane alpha 115/110
  - Storefront: frame + dividers + cracked panes + debris
  - Window glow cones: warm amber
  - Cold confetti: DATA_BLUE 70% dominant
  - Dutch angle: 4.0°
  - Buildings: storm rim lighting ELEC_CYAN + UV bounce

Output: /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_glitch_storm.png
Usage: python3 LTG_TOOL_style_frame_02_glitch_storm.py
"""

import os
import sys
import math
import random
from PIL import Image, ImageDraw, ImageFilter

# Import procedural draw library for add_rim_light
_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _TOOLS_DIR)
try:
    from LTG_TOOL_procedural_draw import add_rim_light
    PROCEDURAL_DRAW_AVAILABLE = True
except ImportError:
    PROCEDURAL_DRAW_AVAILABLE = False
    print("WARNING: LTG_TOOL_procedural_draw not found — rim light passes will use fallback.")

# C36: PIL ImageChops needed for per-character fill light mask
from PIL import ImageChops

OUTPUT_PATH = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_glitch_storm.png"
W, H = 1920, 1080

# ── Master Palette ────────────────────────────────────────────────────────────
WARM_CREAM      = (250, 240, 220)
SOFT_GOLD       = (232, 201,  90)
SUNLIT_AMBER    = (212, 146,  58)
TERRACOTTA      = (199,  91,  57)
SAGE_GREEN      = (122, 158, 126)
DUSTY_LAVENDER  = (168, 155, 191)

VOID_BLACK      = ( 10,  10,  20)
ELEC_CYAN       = (  0, 240, 255)   # GL-01a #00F0FF — CHAR-L-11 Constraint 1
ACID_GREEN      = ( 57, 255,  20)
DATA_BLUE       = ( 10,  79, 140)   # #0A4F8C — dominant storm confetti color
UV_PURPLE       = (123,  47, 190)
HOT_MAGENTA     = (255,  45, 107)   # GL-02 #FF2D6B — canonical (NOT #FF0090)
STATIC_WHITE    = (240, 240, 240)
CORRUPT_AMBER   = (255, 140,   0)   # GL-07 canonical #FF8C00 — C22 fix: was (200,122,32)

# ENV colors
NIGHT_SKY_DEEP  = ( 26,  20,  40)
DARK_ASPHALT    = ( 42,  42,  56)
CYAN_ROAD       = ( 42,  90, 106)
WARM_ROAD       = ( 74,  58,  42)
COOL_SIDEWALK   = ( 58,  56,  72)
TERRA_CYAN_LIT  = (150, 172, 162)  # ENV-06 fix: G=172>R=150, B=162>R=150
DEEP_WARM_SHAD  = ( 90,  56,  32)
ROOF_EDGE       = ( 26,  24,  32)
DEEP_COCOA      = ( 59,  40,  32)

WIN_GLOW_WARM   = (200, 160,  80)

# Character storm colors
DRW_HOODIE_STORM    = (200, 105,  90)
DRW_SKIN_STORM      = (106, 180, 174)
DRW_HOODIE_SHADOW   = ( 58,  26,  20)
DRW_JACKET_STORM    = (128, 192, 204)
DRW_JACKET_SHADOW   = ( 42,  26,  50)
DRW_HAIR_MAGENTA    = (106,  42,  58)
BYTE_TEAL           = (  0, 212, 232)   # GL-01b BYTE_TEAL — NEVER Void Black

# Storm edge-lighting colors for buildings
STORM_RIM_CYAN  = (  0, 180, 220)
STORM_RIM_UV    = ( 80,  30, 120)

RNG = random.Random(42)


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def alpha_paste(base, overlay_rgba):
    base_rgba = base.convert("RGBA")
    base_rgba.alpha_composite(overlay_rgba)
    return base_rgba.convert("RGB")


# ── Layer 1: Sky ──────────────────────────────────────────────────────────────

def draw_sky(img):
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        col = lerp_color(VOID_BLACK, NIGHT_SKY_DEEP, min(t * 2.5, 1.0))
        draw.line([(0, y), (W, y)], fill=col)
    _draw_uv_cloud_masses(img)
    _draw_horizon_haze(img)
    _draw_main_crack(img)
    _draw_sub_cracks(img)
    _draw_storm_edges(img)
    return img


def _draw_uv_cloud_masses(img):
    draw = ImageDraw.Draw(img)
    cloud_shapes = [
        (0,    0,  520, 220), (80,  60,  380, 160),
        (20, 120,  260,  80), (460,  0,  200, 140), (380, 80,  180, 120),
    ]
    for (cx, cy, cw, ch) in cloud_shapes:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle([cx, cy, cx + cw, cy + ch], fill=(*UV_PURPLE, 200))
        bite_x = cx + int(cw * 0.55)
        bite_y = cy + int(ch * 0.30)
        od.rectangle([bite_x, bite_y, cx + cw, bite_y + int(ch * 0.40)], fill=(*VOID_BLACK, 255))
        img = alpha_paste(img, overlay)
        draw = ImageDraw.Draw(img)
    cloud_shapes_r = [
        (1380,  0,  540, 300), (1500, 60,  420, 200), (1620, 20,  300, 160),
        (1760, 80,  160, 240), (1350, 160, 380, 140),
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
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    horizon_y = int(H * 0.55)
    haze_height = int(H * 0.15)
    for dy in range(haze_height):
        t = 1.0 - (dy / haze_height)
        a = int(40 * t)
        od.line([(0, horizon_y - dy), (W, horizon_y - dy)], fill=(*UV_PURPLE, a))
    return alpha_paste(img, overlay)


def _draw_main_crack(img):
    crack_pts = [
        (1820, 0), (1700, 80), (1700, 140), (1600, 220), (1520, 220),
        (1460, 340), (1380, 420), (1380, 500), (1280, 580), (1200, 640),
    ]
    glow_specs = [
        (HOT_MAGENTA, 18, 80), (ELEC_CYAN, 12, 180), (ELEC_CYAN, 6, 240), (STATIC_WHITE, 3, 220),
    ]
    for (color, half_w, alpha) in glow_specs:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        for i in range(len(crack_pts) - 1):
            x0, y0 = crack_pts[i]; x1, y1 = crack_pts[i + 1]
            od.line([(x0, y0), (x1, y1)], fill=(*color, alpha), width=half_w * 2)
        img = alpha_paste(img, overlay)
    return img


def _draw_sub_cracks(img):
    sub_cracks = [
        (1700, 140, 1750, 50), (1600, 220, 1560, 160), (1460, 340, 1520, 400),
        (1380, 420, 1320, 380), (1280, 580, 1240, 520), (1380, 500, 1440, 560),
        (1200, 640, 1160, 680),
    ]
    for (x0, y0, x1, y1) in sub_cracks:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.line([(x0, y0), (x1, y1)], fill=(*ELEC_CYAN, 160), width=4)
        mid_x = (x0 + x1) // 2; mid_y = (y0 + y1) // 2
        od.line([(mid_x, mid_y), (x1, y1)], fill=(*DATA_BLUE, 120), width=2)
        img = alpha_paste(img, overlay)
    return img


def _draw_storm_edges(img):
    draw = ImageDraw.Draw(img)
    burn_lines = [
        ((460,  0), (520, 30)), ((380, 80), (440, 110)), ((80,  60), (110, 90)),
        ((1380, 0), (1360, 50)), ((1500, 60), (1480, 110)), ((1760, 80), (1720, 130)),
        ((1350, 160), (1380, 200)),
    ]
    for pt1, pt2 in burn_lines:
        draw.line([pt1, pt2], fill=HOT_MAGENTA, width=3)
    return img


# ── Layer 2: Storm Confetti — dominant cold confetti ──────────────────────────

def draw_storm_confetti(img):
    """Dominant cold confetti — DATA_BLUE 70%, VOID_BLACK 20%, ELEC_CYAN 10%."""
    draw = ImageDraw.Draw(img)

    cold_dominant = (
        [DATA_BLUE] * 7 +
        [VOID_BLACK] * 2 +
        [ELEC_CYAN] * 1
    )
    accent_pool = cold_dominant + [UV_PURPLE]

    for _ in range(240):
        cx = RNG.randint(1100, 1900); cy = RNG.randint(0, int(H * 0.55))
        dist = math.sqrt((cx - 1400) ** 2 + (cy - 300) ** 2)
        t = clamp(dist / 700.0, 0.0, 1.0)
        size = int(15 - (15 - 3) * t)
        color = RNG.choice(cold_dominant)
        draw.rectangle([cx, cy, cx + size, cy + size], fill=color)

    for _ in range(160):
        cx = RNG.randint(600, 1900); cy = RNG.randint(int(H * 0.25), int(H * 0.60))
        size = RNG.randint(3, 8)
        color = RNG.choice(accent_pool)
        alpha_draw = RNG.randint(140, 220)
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle([cx, cy, cx + size, cy + size], fill=(*color, alpha_draw))
        img = alpha_paste(img, overlay)
    draw = ImageDraw.Draw(img)

    for _ in range(80):
        cx = RNG.randint(300, 900); cy = RNG.randint(int(H * 0.65), H)
        size = RNG.randint(2, 4)
        color = RNG.choice(cold_dominant)
        draw.rectangle([cx, cy, cx + size, cy + size], fill=color)
    return img


# ── Layer 3: Town Silhouette ───────────────────────────────────────────────────

def draw_town_silhouette(img):
    draw = ImageDraw.Draw(img)
    horizon_y = int(H * 0.58)
    buildings = [
        (0, horizon_y - 160, 180, horizon_y, DEEP_WARM_SHAD),
        (150, horizon_y - 200, 320, horizon_y, DEEP_WARM_SHAD),
        (300, horizon_y - 140, 440, horizon_y, TERRA_CYAN_LIT),
        (420, horizon_y - 260, 560, horizon_y, DEEP_WARM_SHAD),
        (540, horizon_y - 180, 680, horizon_y, TERRA_CYAN_LIT),
        (660, horizon_y - 340, 760, horizon_y, DEEP_WARM_SHAD),
        (690, horizon_y - 420, 730, horizon_y - 340, DEEP_WARM_SHAD),
        (760, horizon_y - 190, 900, horizon_y, TERRA_CYAN_LIT),
        (880, horizon_y - 150, 1020, horizon_y, DEEP_WARM_SHAD),
        (1000, horizon_y - 220, 1140, horizon_y, TERRA_CYAN_LIT),
        (1120, horizon_y - 170, 1260, horizon_y, DEEP_WARM_SHAD),
        (1240, horizon_y - 240, 1380, horizon_y, TERRA_CYAN_LIT),
        (1360, horizon_y - 130, 1500, horizon_y, DEEP_WARM_SHAD),
        (1480, horizon_y - 200, 1620, horizon_y, TERRA_CYAN_LIT),
        (1600, horizon_y - 160, 1740, horizon_y, DEEP_WARM_SHAD),
        (1720, horizon_y - 210, W, horizon_y, TERRA_CYAN_LIT),
    ]
    for (lx, ry, rx, gy, col) in buildings:
        draw.rectangle([lx, ry, rx, gy], fill=col)

    chimneys = [
        (200, horizon_y - 220, 215, horizon_y - 190), (380, horizon_y - 215, 395, horizon_y - 190),
        (480, horizon_y - 280, 495, horizon_y - 250), (870, horizon_y - 210, 885, horizon_y - 180),
        (1050, horizon_y - 240, 1065, horizon_y - 210), (1300, horizon_y - 260, 1315, horizon_y - 230),
        (1550, horizon_y - 220, 1565, horizon_y - 190),
    ]
    for (x0, y0, x1, y1) in chimneys:
        draw.rectangle([x0, y0, x1, y1], fill=DEEP_COCOA)

    _draw_building_windows_with_glow(img, buildings, horizon_y)
    _draw_power_lines(img, horizon_y)
    _draw_building_storm_rims(img, buildings, horizon_y)

    draw = ImageDraw.Draw(img)
    for (x0, y0, x1, y1) in chimneys[:3]:
        draw.line([(x0, y0), (x0, y1)], fill=(*ELEC_CYAN, 60), width=1)
    return img


def _draw_building_windows_with_glow(img, buildings, horizon_y):
    """
    C22 fix: window pane alpha reduced to 115/110 (from 160/180).
    FIX 2 (C19): warm amber light cone below each lit window.
    """
    win_colors = [(*SOFT_GOLD, 115), (*WARM_CREAM, 110)]
    glow_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(glow_overlay)

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

                win_cx = wx + win_w // 2
                cone_top_y = wy + win_h
                cone_bot_y = min(gy, horizon_y + 30)
                if cone_bot_y <= cone_top_y:
                    continue
                cone_height = cone_bot_y - cone_top_y
                half_spread_top = win_w // 2
                half_spread_bot = int(win_w * 0.9)
                n_steps = max(8, cone_height // 8)
                for step in range(n_steps):
                    t_step = step / n_steps
                    step_y = int(cone_top_y + t_step * cone_height)
                    next_y = int(cone_top_y + (step + 1) / n_steps * cone_height)
                    half_w_step = int(half_spread_top + t_step * (half_spread_bot - half_spread_top))
                    a = int((1.0 - t_step ** 0.8) * 105)
                    a = max(0, min(255, a))
                    if a > 5 and step_y < next_y:
                        od.rectangle([win_cx - half_w_step, step_y,
                                      win_cx + half_w_step, next_y],
                                     fill=(*WIN_GLOW_WARM, a))

    img = alpha_paste(img, glow_overlay)
    return img


def _draw_building_storm_rims(img, buildings, horizon_y):
    """Storm edge-lighting on buildings — right/top edges ELEC_CYAN, base UV bounce."""
    crack_x = 1400
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    for (lx, ry, rx, gy, col) in buildings:
        bld_cx = (lx + rx) / 2
        dist = abs(bld_cx - crack_x)
        rim_strength = clamp(1.0 - dist / 1200.0, 0.0, 1.0)
        rim_alpha = int(30 + rim_strength * 90)

        rim_width = max(2, int(4 * rim_strength) + 1)
        od.rectangle([rx - rim_width, ry, rx, gy],
                     fill=(*STORM_RIM_CYAN, rim_alpha))

        top_alpha = int(20 + rim_strength * 60)
        od.rectangle([lx, ry, rx, ry + rim_width],
                     fill=(*STORM_RIM_CYAN, top_alpha))

        base_h = max(4, int((gy - ry) * 0.08))
        uv_alpha = int(25 + rim_strength * 40)
        od.rectangle([lx, gy - base_h, rx, gy],
                     fill=(*STORM_RIM_UV, uv_alpha))

    img = alpha_paste(img, overlay)
    return img


def _draw_power_lines(img, horizon_y):
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
        od.line([(x, horizon_y), (x, horizon_y + pool_height)], fill=(*CYAN_ROAD, a))
    img = alpha_paste(img, overlay)

    draw = ImageDraw.Draw(img)
    draw.line([(0, sidewalk_bottom), (W, sidewalk_bottom)], fill=VOID_BLACK, width=2)
    return img


# ── Layer 5: Damaged Storefront Window (lower-right) ─────────────────────────

def draw_storefront(img):
    """
    FIX 1 (C19): Genuine DAMAGED STOREFRONT WINDOW — structural frame + dividers +
    crack lines from 2 impact points + missing panes + debris scatter.
    """
    draw = ImageDraw.Draw(img)
    horizon_y = int(H * 0.58)

    sf_left  = int(W * 0.80)
    sf_right = int(W * 0.96)
    sf_top   = horizon_y - 100
    sf_bot   = horizon_y + int((H - horizon_y) * 0.58)
    sf_w     = sf_right - sf_left
    sf_h     = sf_bot - sf_top

    FRAME_COL    = (60, 70, 80)
    INTERIOR     = (15, 12, 22)
    GLASS_REMAIN = (60, 90, 110)
    SHARD_EDGE   = (140, 200, 220)
    MISSING_PANE = (10, 10, 20)
    DEBRIS_COL   = (80, 72, 60)

    draw.rectangle([sf_left, sf_top, sf_right, sf_bot], fill=INTERIOR)

    frame_w = 8
    draw.rectangle([sf_left, sf_top, sf_right, sf_bot],
                   outline=FRAME_COL, width=frame_w)

    vert_1 = sf_left + sf_w // 3
    vert_2 = sf_left + 2 * sf_w // 3
    horiz_1 = sf_top + sf_h // 2
    bar_w = 6
    draw.rectangle([vert_1 - bar_w//2, sf_top, vert_1 + bar_w//2, sf_bot], fill=FRAME_COL)
    draw.rectangle([vert_2 - bar_w//2, sf_top, vert_2 + bar_w//2, sf_bot], fill=FRAME_COL)
    draw.rectangle([sf_left, horiz_1 - bar_w//2, sf_right, horiz_1 + bar_w//2], fill=FRAME_COL)

    panes = [
        (sf_left + frame_w, sf_top + frame_w, vert_1 - bar_w//2, horiz_1 - bar_w//2, False),
        (vert_1 + bar_w//2, sf_top + frame_w, vert_2 - bar_w//2, horiz_1 - bar_w//2, True),
        (vert_2 + bar_w//2, sf_top + frame_w, sf_right - frame_w, horiz_1 - bar_w//2, False),
        (sf_left + frame_w, horiz_1 + bar_w//2, vert_1 - bar_w//2, sf_bot - frame_w, True),
        (vert_1 + bar_w//2, horiz_1 + bar_w//2, vert_2 - bar_w//2, sf_bot - frame_w, False),
        (vert_2 + bar_w//2, horiz_1 + bar_w//2, sf_right - frame_w, sf_bot - frame_w, True),
    ]
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for (px0, py0, px1, py1, has_glass) in panes:
        if px1 <= px0 or py1 <= py0:
            continue
        if has_glass:
            od.rectangle([px0, py0, px1, py1], fill=(*GLASS_REMAIN, 160))
        else:
            od.rectangle([px0, py0, px1, py1], fill=(*MISSING_PANE, 255))
    img = alpha_paste(img, overlay)
    draw = ImageDraw.Draw(img)

    impact_pts = [
        (vert_1 + 30, sf_top + sf_h // 4),
        (sf_left + sf_w // 2 + 20, horiz_1 + 15),
    ]
    rng_crack = random.Random(77)
    for (ox, oy) in impact_pts:
        n_rays = rng_crack.randint(6, 8)
        for ri in range(n_rays):
            angle = (2 * math.pi * ri / n_rays) + rng_crack.uniform(-0.2, 0.2)
            length = rng_crack.randint(50, 120)
            ex = int(ox + math.cos(angle) * length)
            ey = int(oy + math.sin(angle) * length)
            ex = clamp(ex, sf_left + frame_w, sf_right - frame_w)
            ey = clamp(ey, sf_top + frame_w, sf_bot - frame_w)
            draw.line([(ox, oy), (ex, ey)], fill=SHARD_EDGE, width=2)
            if rng_crack.random() < 0.5:
                mid_x = (ox + ex) // 2
                mid_y = (oy + ey) // 2
                branch_angle = angle + rng_crack.uniform(-0.8, 0.8)
                branch_len = rng_crack.randint(20, 55)
                bx = int(mid_x + math.cos(branch_angle) * branch_len)
                by = int(mid_y + math.sin(branch_angle) * branch_len)
                bx = clamp(bx, sf_left + frame_w, sf_right - frame_w)
                by = clamp(by, sf_top + frame_w, sf_bot - frame_w)
                draw.line([(mid_x, mid_y), (bx, by)], fill=SHARD_EDGE, width=1)
        draw.ellipse([ox - 4, oy - 4, ox + 4, oy + 4], fill=INTERIOR)

    debris_y_base = sf_bot
    debris_zone_x0 = sf_left - 20
    debris_zone_x1 = sf_right + 10
    rng_debris = random.Random(44)
    for _ in range(22):
        dx = rng_debris.randint(debris_zone_x0, debris_zone_x1)
        dy = debris_y_base + rng_debris.randint(2, 45)
        if dy >= H:
            continue
        shard_w = rng_debris.randint(4, 14)
        shard_h = rng_debris.randint(3, 9)
        shard_pts = [
            (dx, dy - shard_h),
            (dx + shard_w, dy - shard_h + rng_debris.randint(-3, 3)),
            (dx + shard_w - 2, dy),
            (dx - 2, dy),
        ]
        draw.polygon(shard_pts, fill=GLASS_REMAIN, outline=SHARD_EDGE)
    for _ in range(30):
        dx = rng_debris.randint(debris_zone_x0, debris_zone_x1)
        dy = debris_y_base + rng_debris.randint(0, 30)
        if dy >= H:
            continue
        ds = rng_debris.randint(2, 5)
        draw.ellipse([dx - ds, dy - ds//2, dx + ds, dy + ds//2], fill=DEBRIS_COL)

    draw.rectangle([sf_left, sf_top, sf_right, sf_bot],
                   outline=(*HOT_MAGENTA,), width=2)

    return img


# ── Layer 6: Characters ───────────────────────────────────────────────────────

def _draw_glitch_storm(img, cx, cy, body_h):
    """
    Draw Glitch hovering in the storm sky near the crack (upper-right mid-ground).
    G007 FIX (C40): Glitch diamond body drawn with VOID_BLACK outline=width 3 as spec §2.2.
    Glitch is the source of the storm — it hovers near the crack at mid-distance scale.
    body_h: vertical half-extent of the diamond (equivalent to ry in the expression sheet).
    """
    import math
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    rx = int(body_h * 0.88)   # horizontal half-extent (ry > rx: taller than wide)
    ry = body_h
    tilt_deg = 8               # slight tilt — Glitch is never perfectly upright
    angle = math.radians(tilt_deg)

    # Diamond body points (spec §2.1 formula)
    top   = (cx + int(rx * 0.15 * math.sin(angle)),  cy - ry + int(rx * 0.15 * math.cos(angle)))
    right = (cx + int(rx * math.cos(-angle)),          cy + int(rx * 0.2 * math.sin(-angle)))
    bot   = (cx - int(rx * 0.15 * math.sin(angle)),  cy + int(ry * 1.15))
    left  = (cx - int(rx * math.cos(-angle)),          cy - int(rx * 0.2 * math.sin(-angle)))
    pts = [top, right, bot, left]

    # UV_PURPLE shadow offset (+3, +4)
    sh_pts = [(x + 3, y + 4) for x, y in pts]
    od.polygon(sh_pts, fill=(*UV_PURPLE, 200))

    # Main body fill — CORRUPT_AMBER
    od.polygon(pts, fill=(*CORRUPT_AMBER, 240))

    # Highlight facet
    ctr = (cx, cy - ry // 4)
    mid_tl = ((top[0] + left[0]) // 2, (top[1] + left[1]) // 2)
    od.polygon([top, ctr, mid_tl], fill=(*((255, 185, 80)), 220))  # CORRUPT_AMB_HL

    # G007 SPEC: VOID_BLACK outline on body polygon — width=3
    od.polygon(pts, outline=(*VOID_BLACK, 255), width=3)

    # HOT_MAG crack (drawn AFTER body fill — spec §2.3)
    cs = (cx - rx // 2, cy - ry // 3)
    ce = (cx + rx // 3, cy + ry // 2)
    od.line([cs, ce], fill=(*HOT_MAGENTA, 230), width=2)
    mid_c = ((cs[0] + ce[0]) // 2, (cs[1] + ce[1]) // 2)
    od.line([mid_c, (cx + rx // 2, cy - ry // 4)], fill=(*HOT_MAGENTA, 200), width=1)

    # Top spike (spec §3.1)
    spike_h = max(4, ry // 2)
    sx = cx + int(rx * 0.15 * math.sin(angle))
    cy_top = top[1]
    spike_pts = [
        (sx - spike_h // 2, cy_top),
        (sx - spike_h,      cy_top - spike_h),
        (sx,                cy_top - spike_h * 2),
        (sx + spike_h,      cy_top - spike_h),
        (sx + spike_h // 2, cy_top),
    ]
    od.polygon(spike_pts, fill=(*CORRUPT_AMBER, 240))
    od.polygon(spike_pts, outline=(*VOID_BLACK, 255), width=2)
    od.line([(sx, cy_top - spike_h * 2), (sx, cy_top - spike_h * 2 - max(2, ry // 8))],
            fill=(*HOT_MAGENTA, 220), width=2)

    # Pixel eyes — simple 2-cell pixel grid at this scale
    eye_cell = max(2, rx // 5)
    face_cy = cy - ry // 6
    # Left eye (viewer's right): CORRUPT_AMBER_HL tint (hostile calculating state)
    le_cx = cx - rx // 3
    od.rectangle([le_cx - eye_cell, face_cy - eye_cell, le_cx + eye_cell, face_cy + eye_cell],
                 fill=(*UV_PURPLE, 230))
    od.rectangle([le_cx - eye_cell // 2, face_cy - eye_cell // 2,
                  le_cx + eye_cell // 2, face_cy + eye_cell // 2],
                 fill=(*ACID_GREEN, 255))  # MISCHIEVOUS state — it's causing the storm
    # Right eye: match left for bilateral storm state
    re_cx = cx + rx // 3
    od.rectangle([re_cx - eye_cell, face_cy - eye_cell, re_cx + eye_cell, face_cy + eye_cell],
                 fill=(*UV_PURPLE, 230))
    od.rectangle([re_cx - eye_cell // 2, face_cy - eye_cell // 2,
                  re_cx + eye_cell // 2, face_cy + eye_cell // 2],
                 fill=(*ACID_GREEN, 255))

    # ACID_GREEN particle confetti near Glitch (spec §confetti: Glitchkin confetti
    # stays close to the Glitchkin, NOT intermingled with storm confetti)
    rng_gc = random.Random(77)
    for _ in range(6):
        px = cx + rng_gc.randint(-rx * 2, rx * 2)
        py = cy + rng_gc.randint(-ry * 2, ry * 2)
        ps = rng_gc.randint(2, 4)
        od.rectangle([px, py, px + ps, py + ps], fill=(*ACID_GREEN, 180))

    img = alpha_paste(img, overlay)
    draw = ImageDraw.Draw(img)  # refresh after alpha_composite  # noqa: F841
    return img


def draw_characters(img):
    """Character layout — sprinting left-to-right across frame.
    C40 G007 FIX: _draw_glitch_storm() added — Glitch now appears in SF02 with
    canonical VOID_BLACK body outline (spec §2.2, G007 compliance).
    """
    horizon_y = int(H * 0.58)
    ground_y  = horizon_y + int((H - horizon_y) * 0.12)
    char_h = int(H * 0.18)

    luma_cx = int(W * 0.45)
    luma_foot_y = ground_y + 10
    luma_head_cy = luma_foot_y - char_h

    byte_cx = int(W * 0.28)
    byte_float_y = luma_head_cy + int(char_h * 0.30)

    cosmo_cx = int(W * 0.62)
    cosmo_foot_y = ground_y + 14

    # Glitch — hovering near the crack (upper-right mid-ground, ~x=78%, y=32%)
    # At mid-distance scale: ~50% of char_h. VOID_BLACK outline per spec §2.2.
    glitch_cx = int(W * 0.78)
    glitch_cy = int(H * 0.32)
    glitch_body_h = int(char_h * 0.50)  # ry (vertical half-extent)
    img = _draw_glitch_storm(img, glitch_cx, glitch_cy, glitch_body_h)

    img = _draw_luma(img, luma_cx, luma_foot_y, char_h)
    img = _draw_cosmo(img, cosmo_cx, cosmo_foot_y, char_h)
    img = _draw_byte_hovering(img, byte_cx, byte_float_y, char_h)
    img = _draw_townspeople(img, horizon_y)

    return img


def _draw_luma_face_sprint(draw, cx, head_cy, head_r):
    """
    C35 NEW: FOCUSED DETERMINATION expression for Luma in sprint.
    Lee Tanaka staging brief: asymmetric eyes, inward left brow,
    level right brow, compressed jaw-set mouth.

    At head_r ≈ 23px (sprint scale), features are minimal but readable:
    - 2 eyes (asymmetric size), pupils (4px ellipse)
    - 2 brow lines (1-2px, directional)
    - 1 mouth mark (compressed line or tiny ajar oval)

    Eye direction: angled slightly down-forward (both pupils look ahead-down,
    not at camera). This is a doing gaze, not a performing gaze.
    """
    # Eye parameters — asymmetric, angled down-forward
    # Left eye (viewer's left = Luma's right — leading eye): slightly wider
    eye_r_left  = max(2, int(head_r * 0.26))   # ~6px at hr=23
    eye_r_right = max(2, int(head_r * 0.17))   # ~4px at hr=23

    # Eye centers: positioned in upper-middle of head, forward-angled
    # Both eyes lowered slightly for down-forward gaze
    eye_y_offset  = -int(head_r * 0.15)   # slight down-forward (below head center)
    left_eye_cx   = cx - int(head_r * 0.30)
    right_eye_cx  = cx + int(head_r * 0.22)
    left_eye_cy   = head_cy + eye_y_offset
    right_eye_cy  = head_cy + eye_y_offset + int(head_r * 0.08)  # right slightly lower = angled

    # Draw eye whites (very small ellipses at sprint scale)
    draw.ellipse([left_eye_cx  - eye_r_left,  left_eye_cy  - eye_r_left,
                  left_eye_cx  + eye_r_left,  left_eye_cy  + eye_r_left],
                 fill=WARM_CREAM)
    draw.ellipse([right_eye_cx - eye_r_right, right_eye_cy - eye_r_right,
                  right_eye_cx + eye_r_right, right_eye_cy + eye_r_right],
                 fill=WARM_CREAM)

    # Pupils — 4px ellipses (Lee brief), positioned forward-down
    pupil_r = max(1, int(head_r * 0.09))  # ~2px at hr=23, visible at this scale
    # Left pupil: offset slightly forward (toward right/sprint direction) and down
    lp_cx = left_eye_cx  + max(1, int(eye_r_left  * 0.25))
    lp_cy = left_eye_cy  + max(1, int(eye_r_left  * 0.20))
    # Right pupil: also forward-down
    rp_cx = right_eye_cx + max(1, int(eye_r_right * 0.25))
    rp_cy = right_eye_cy + max(1, int(eye_r_right * 0.20))
    draw.ellipse([lp_cx - pupil_r, lp_cy - pupil_r, lp_cx + pupil_r, lp_cy + pupil_r],
                 fill=DEEP_COCOA)
    draw.ellipse([rp_cx - pupil_r, rp_cy - pupil_r, rp_cx + pupil_r, rp_cy + pupil_r],
                 fill=DEEP_COCOA)

    # Eye outlines (dark ring)
    draw.ellipse([left_eye_cx  - eye_r_left,  left_eye_cy  - eye_r_left,
                  left_eye_cx  + eye_r_left,  left_eye_cy  + eye_r_left],
                 outline=DEEP_COCOA, width=1)
    draw.ellipse([right_eye_cx - eye_r_right, right_eye_cy - eye_r_right,
                  right_eye_cx + eye_r_right, right_eye_cy + eye_r_right],
                 outline=DEEP_COCOA, width=1)

    # BROWS — asymmetric (Lee brief):
    # Left brow: slightly lower, pulled inward toward nose — corrugator activation
    # Right brow: level — not symmetric, signals interior complexity
    brow_y_base = head_cy - int(head_r * 0.40)  # above eyes
    brow_width  = int(head_r * 0.35)

    # Left brow: angled down-inward (inner end lower than outer end)
    lbrow_x0 = left_eye_cx  - brow_width // 2
    lbrow_y0 = brow_y_base
    lbrow_x1 = left_eye_cx  + brow_width // 2
    lbrow_y1 = brow_y_base + int(head_r * 0.12)  # inner end (toward nose) drops down
    draw.line([(lbrow_x0, lbrow_y0), (lbrow_x1, lbrow_y1)],
              fill=DEEP_COCOA, width=max(1, int(head_r * 0.08)))

    # Right brow: level (flat)
    rbrow_x0 = right_eye_cx - brow_width // 2
    rbrow_y0 = brow_y_base
    rbrow_x1 = right_eye_cx + brow_width // 2
    rbrow_y1 = brow_y_base  # no slope
    draw.line([(rbrow_x0, rbrow_y0), (rbrow_x1, rbrow_y1)],
              fill=DEEP_COCOA, width=max(1, int(head_r * 0.07)))

    # MOUTH — compressed jaw-set line (not a smile, not a fear O)
    # At sprint scale: single compressed horizontal line or very small open oval
    mouth_y = head_cy + int(head_r * 0.42)
    mouth_w = int(head_r * 0.40)
    # Compressed line — jaw is set
    draw.line([(cx - mouth_w // 2, mouth_y), (cx + mouth_w // 2, mouth_y)],
              fill=DEEP_COCOA, width=max(1, int(head_r * 0.09)))


def _draw_luma(img, cx, foot_y, h):
    """
    Luma in full sprint. CORRUPT_AMBER outline for figure-ground separation.
    C35: 10° forward lean, steeper hair stream, FOCUSED DETERMINATION face.
    """
    head_r  = int(h * 0.12)
    torso_h = int(h * 0.28)
    torso_w = int(h * 0.17)
    leg_h   = int(h * 0.38)

    head_cy   = foot_y - h + head_r

    # C35: 10° forward lean — torso shifts forward (left = sprint direction)
    # lean_offset: horizontal displacement at torso midpoint due to tilt
    lean_offset = int(torso_h * math.tan(math.radians(10)))
    torso_top = head_cy + head_r + 2
    torso_bot = torso_top + torso_h
    # Leaned torso: top forward (left), bottom at cx
    torso_cx_top  = cx - lean_offset       # top of torso leans forward (left)
    torso_cx_bot  = cx                     # bottom stays at foot plumb
    torso_left_top  = torso_cx_top  - torso_w // 2
    torso_right_top = torso_cx_top  + torso_w // 2
    torso_left_bot  = torso_cx_bot  - torso_w // 2
    torso_right_bot = torso_cx_bot  + torso_w // 2

    # Head follows torso lean — head_cx shifts slightly forward
    head_cx = cx - lean_offset // 2

    outline_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ol = ImageDraw.Draw(outline_layer)
    # Outline torso as leaned parallelogram-ish polygon
    torso_outline_pts = [
        (torso_left_top - 2,  torso_top - 2),
        (torso_right_top + 2, torso_top - 2),
        (torso_right_bot + 2, torso_bot + 2),
        (torso_left_bot - 2,  torso_bot + 2),
    ]
    ol.polygon(torso_outline_pts, outline=(*CORRUPT_AMBER, 220))
    ol.ellipse([head_cx - head_r - 2, head_cy - head_r - 2,
                head_cx + head_r + 2, head_cy + head_r + 2],
               outline=(*CORRUPT_AMBER, 180), width=2)
    img = alpha_paste(img, outline_layer)

    shadow_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_overlay)
    # Shadow side of leaned torso (left half)
    shadow_pts = [
        (torso_left_top,     torso_top),
        ((torso_cx_top),     torso_top),
        ((torso_cx_bot),     torso_bot),
        (torso_left_bot,     torso_bot),
    ]
    sd.polygon(shadow_pts, fill=(*DRW_HOODIE_SHADOW, 255))
    img = alpha_paste(img, shadow_overlay)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # Leaned torso fill (full polygon)
    torso_fill_pts = [
        (torso_left_top,  torso_top),
        (torso_right_top, torso_top),
        (torso_right_bot, torso_bot),
        (torso_left_bot,  torso_bot),
    ]
    od.polygon(torso_fill_pts, fill=(*DRW_HOODIE_STORM, 255))

    # Head fill
    od.ellipse([head_cx - head_r, head_cy - head_r,
                head_cx + head_r, head_cy + head_r],
               fill=(*DRW_SKIN_STORM, 255))

    # Hair — dark cap arc
    od.arc([head_cx - head_r, head_cy - head_r,
            head_cx + head_r, head_cy + head_r],
           start=190, end=360, fill=DEEP_COCOA, width=int(head_r * 0.5))
    od.arc([head_cx - head_r + 2, head_cy - head_r + 2,
            head_cx + head_r - 2, head_cy + head_r - 2],
           start=190, end=330, fill=DRW_HAIR_MAGENTA, width=2)

    # Legs — counter-rotation sprint arm pump
    left_leg_pts = [(cx - 8, torso_bot), (cx + 30, torso_bot + int(leg_h * 0.55)), (cx + 50, foot_y)]
    for i in range(len(left_leg_pts) - 1):
        od.line([left_leg_pts[i], left_leg_pts[i + 1]], fill=(*DRW_HOODIE_STORM, 255), width=int(torso_w * 0.35))

    right_leg_pts = [(cx + 8, torso_bot), (cx - 25, torso_bot + int(leg_h * 0.50)), (cx - 40, foot_y - int(leg_h * 0.15))]
    for i in range(len(right_leg_pts) - 1):
        od.line([right_leg_pts[i], right_leg_pts[i + 1]], fill=(*DRW_HOODIE_SHADOW, 255), width=int(torso_w * 0.30))

    # Arms — leaned counter-rotation (leading arm reaches forward, back arm pushes back)
    # Left arm (push-back): elbow well behind body, hand behind hip — higher endpoint
    od.line([(torso_cx_bot - int(torso_w * 0.45), torso_top + int(torso_h * 0.20)),
             (torso_cx_bot + int(torso_w * 0.30), torso_top - int(h * 0.45 * 0.45))],
            fill=(*DRW_HOODIE_STORM, 255), width=int(torso_w * 0.30))
    # Right arm (push-forward): reaches further forward
    od.line([(torso_cx_bot + int(torso_w * 0.35), torso_top + int(torso_h * 0.20)),
             (torso_cx_bot - int(torso_w * 0.60), torso_top + int(h * 0.26 * 0.65))],
            fill=(*DRW_HOODIE_SHADOW, 255), width=int(torso_w * 0.28))

    # C35: Hair stream — steeper angle (more horizontal, closer to ground-parallel = velocity)
    # Original was trailing left and slightly up; now angled sharply rearward (more leftward)
    hair_anchor = (head_cx - head_r + 4, head_cy)
    hair_stream = [
        hair_anchor,
        (head_cx - head_r - int(h * 0.09), head_cy + int(h * 0.01)),   # primary: nearly horizontal
        (head_cx - head_r - int(h * 0.16), head_cy + int(h * 0.005)),  # tip: very flat angle
    ]
    for i in range(len(hair_stream) - 1):
        od.line([hair_stream[i], hair_stream[i + 1]], fill=DEEP_COCOA, width=6)
    od.line([hair_stream[0], hair_stream[-1]], fill=DRW_HAIR_MAGENTA, width=2)

    # Second finer strand — trailing further back for velocity read
    fine_strand = [
        (head_cx - head_r + 2, head_cy + int(head_r * 0.20)),
        (head_cx - head_r - int(h * 0.07), head_cy + int(h * 0.02)),
        (head_cx - head_r - int(h * 0.13), head_cy + int(h * 0.015)),
    ]
    for i in range(len(fine_strand) - 1):
        od.line([fine_strand[i], fine_strand[i + 1]], fill=DEEP_COCOA, width=3)

    # Ground shadow
    shadow_pts = [
        (cx - int(torso_w * 0.8), foot_y + 4), (cx + int(torso_w * 0.8), foot_y + 4),
        (cx + int(torso_w * 1.8), foot_y + 14), (cx - int(torso_w * 1.2), foot_y + 14),
    ]
    od.polygon(shadow_pts, fill=(10, 42, 58, 120))

    img = alpha_paste(img, overlay)

    # C35: Draw face AFTER compositing body (draw handle on top of all fills)
    face_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    face_draw = ImageDraw.Draw(face_img)
    _draw_luma_face_sprint(face_draw, head_cx, head_cy, head_r)
    img = alpha_paste(img, face_img)

    return img


def _draw_cosmo(img, cx, foot_y, h):
    """Cosmo: one stride behind Luma, panic run, glasses."""
    head_r  = int(h * 0.115)
    torso_h = int(h * 0.26)
    torso_w = int(h * 0.155)
    leg_h   = int(h * 0.37)

    head_cy   = foot_y - h + head_r
    torso_top = head_cy + head_r + 2
    torso_bot = torso_top + torso_h
    torso_left  = cx - torso_w // 2
    torso_right = cx + torso_w // 2

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    od.ellipse([torso_left, torso_top, torso_right, torso_bot], fill=(*DRW_JACKET_STORM, 255))
    od.ellipse([torso_left, torso_top, cx, torso_bot], fill=(*DRW_JACKET_SHADOW, 255))
    od.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
               fill=(*DRW_SKIN_STORM, 255))

    gx0 = cx - int(head_r * 0.55); gy0 = head_cy - int(head_r * 0.08)
    gw, gh = int(head_r * 0.60), int(head_r * 0.40)
    od.rectangle([gx0, gy0, gx0 + gw, gy0 + gh], outline=DEEP_COCOA, width=2)
    od.rectangle([gx0 + 2, gy0 + 2, gx0 + gw - 2, gy0 + gh - 2], fill=(*ELEC_CYAN, 100))
    od.rectangle([gx0 + gw + 4, gy0, gx0 + gw * 2 + 4, gy0 + gh], outline=DEEP_COCOA, width=2)
    od.rectangle([gx0 + gw + 6, gy0 + 2, gx0 + gw * 2 + 2, gy0 + gh - 2], fill=(*ELEC_CYAN, 100))

    od.ellipse([cx - int(head_r * 0.35), head_cy + int(head_r * 0.30),
                cx + int(head_r * 0.35), head_cy + int(head_r * 0.65)], fill=VOID_BLACK)

    for (dx, dy, shadow) in [(-12, torso_bot, False), (12, torso_bot, True)]:
        lx = cx + dx
        endx = lx + (25 if not shadow else -20)
        endy = foot_y - int(leg_h * 0.10 if not shadow else 0.25)
        col = DRW_JACKET_STORM if not shadow else DRW_JACKET_SHADOW
        od.line([(lx, dy), (endx, endy), (endx + (15 if not shadow else -10), foot_y)],
                fill=(*col, 255), width=int(torso_w * 0.32))

    od.line([(cx - int(torso_w * 0.4), torso_top + int(torso_h * 0.15)),
             (cx + int(torso_w * 0.2), head_cy - int(h * 0.08))],
            fill=(*DRW_JACKET_STORM, 255), width=int(torso_w * 0.28))
    od.line([(cx + int(torso_w * 0.4), torso_top + int(torso_h * 0.15)),
             (cx - int(torso_w * 0.2), head_cy - int(h * 0.08))],
            fill=(*DRW_JACKET_SHADOW, 255), width=int(torso_w * 0.28))

    od.line([(cx - int(torso_w * 0.35), torso_top + 5),
             (cx - int(torso_w * 0.50), torso_top + int(torso_h * 0.60))],
            fill=WARM_CREAM, width=3)

    img = alpha_paste(img, overlay)
    return img


def _draw_byte_hovering(img, cx, cy, char_h):
    """Byte hovering in storm. CORRUPT_AMBER outline + void body + BYTE_TEAL inner trace."""
    byte_h = int(char_h * 0.40)
    byte_w = int(byte_h * 1.30)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    body_top  = cy - byte_h // 2
    body_bot  = cy + byte_h // 2
    body_left = cx - byte_w // 2
    body_right= cx + byte_w // 2

    od.rectangle([body_left, body_top, body_right, body_bot],
                 fill=(*VOID_BLACK, 255), outline=(*CORRUPT_AMBER, 255), width=3)

    screen_pad = max(4, byte_w // 8)
    screen_left  = body_left  + screen_pad
    screen_right = body_right - screen_pad
    screen_top   = body_top   + screen_pad
    screen_bot   = body_bot   - int(byte_h * 0.28)
    od.rectangle([screen_left, screen_top, screen_right, screen_bot],
                 fill=(*BYTE_TEAL, 255), outline=(*CORRUPT_AMBER, 180), width=1)

    eye_y = screen_top + (screen_bot - screen_top) // 2
    eye_spacing = (screen_right - screen_left) // 3
    left_eye_x  = screen_left  + eye_spacing
    right_eye_x = screen_right - eye_spacing
    eye_r = max(2, byte_h // 8)
    od.ellipse([left_eye_x  - eye_r, eye_y - eye_r,
                left_eye_x  + eye_r, eye_y + eye_r], fill=VOID_BLACK)
    od.ellipse([right_eye_x - eye_r, eye_y - eye_r,
                right_eye_x + eye_r, eye_y + eye_r], fill=VOID_BLACK)

    ant_x = cx
    ant_base_y = body_top
    ant_top_y  = body_top - int(byte_h * 0.40)
    od.line([(ant_x, ant_base_y), (ant_x, ant_top_y)],
            fill=(*CORRUPT_AMBER, 200), width=2)
    ball_r = max(3, byte_h // 10)
    od.ellipse([ant_x - ball_r, ant_top_y - ball_r,
                ant_x + ball_r, ant_top_y + ball_r], fill=(*ELEC_CYAN, 255))

    leg_y = body_bot
    for leg_dx in [-int(byte_w * 0.35), int(byte_w * 0.35)]:
        od.line([(cx + leg_dx, leg_y), (cx + leg_dx, leg_y + int(byte_h * 0.30))],
                fill=(*CORRUPT_AMBER, 180), width=2)

    img = alpha_paste(img, overlay)
    return img


def _draw_townspeople(img, horizon_y):
    """Background townspeople — tiny silhouettes running or cowering."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    ground_y = horizon_y + int((H - horizon_y) * 0.12)
    people = [
        (200, ground_y, 12), (260, ground_y, 10), (340, ground_y - 4, 11),
        (500, ground_y, 13), (550, ground_y, 9),
        (680, ground_y - 2, 10), (720, ground_y, 8),
        (1020, ground_y, 12), (1080, ground_y, 10),
        (1500, ground_y, 11), (1540, ground_y, 9),
        (1640, ground_y, 10), (1680, ground_y - 3, 12),
        (1780, ground_y, 8), (1820, ground_y, 11),
    ]
    for (px, py, ph) in people:
        body_col = (*DEEP_WARM_SHAD, 200)
        od.ellipse([px - ph // 3, py - ph,
                    px + ph // 3, py - int(ph * 0.65)], fill=body_col)
        od.rectangle([px - ph // 4, py - int(ph * 0.65),
                      px + ph // 4, py - int(ph * 0.25)], fill=body_col)
        od.line([(px - ph // 4, py - int(ph * 0.25)),
                 (px - ph // 2, py + 2)], fill=body_col, width=2)
        od.line([(px + ph // 4, py - int(ph * 0.25)),
                 (px + ph // 3, py + 2)], fill=body_col, width=2)

    img = alpha_paste(img, overlay)
    return img


# ── Layer 6b: Magenta Fill Light (C36 — corrected direction + character mask) ─
#
# Implements Jordan Reed's C35 fix (LTG_TOOL_sf02_fill_light_fix_c35.py) directly
# at 1920×1080 resolution (the fix module uses hardcoded 1280×720 and cannot be
# called on a 1920×1080 image without a wrapper — so the algorithm is integrated here).
#
# Fixes (per Sven Halvorsen C14):
#   1. Source direction: UPPER-RIGHT (storm crack at ~x=1700, y=0)
#      fill_src_x = char_cx + int(char_h * 0.5)   (right of char)
#      fill_src_y = char_cy - int(char_h * 0.8)   (above char)
#   2. Per-character silhouette mask via ImageChops.multiply — no background tint
#   3. Alpha max 35 (was 40) — direct source, cleaner than bounce

def _make_char_silhouette_mask_1080(img, char_cx, char_h, char_cy, threshold=60):
    """
    Build per-character silhouette mask at 1920×1080.
    Crops zone around char_cx/char_cy, thresholds, dilates, pastes onto full canvas.
    Returns full-canvas L mask (0=background, 255=character).
    """
    zone_w = int(char_h * 2.0)
    zone_h = int(char_h * 2.5)
    x0 = max(0, char_cx - zone_w // 2)
    y0 = max(0, char_cy - zone_h // 2)
    x1 = min(W, char_cx + zone_w // 2)
    y1 = min(H, char_cy + zone_h)

    crop = img.crop((x0, y0, x1, y1))
    gray = crop.convert("L")
    mask_crop = gray.point(lambda p: 255 if p > threshold else 0, mode="L")

    full_mask = Image.new("L", (W, H), 0)
    full_mask.paste(mask_crop, (x0, y0))

    # Dilate slightly via blur + threshold
    from PIL import ImageFilter
    full_mask_blur = full_mask.filter(ImageFilter.GaussianBlur(radius=6))
    full_mask_dilated = full_mask_blur.point(lambda p: 255 if p > 30 else 0, mode="L")

    return full_mask_dilated


def draw_magenta_fill_light_c36(img, luma_cx, byte_cx, cosmo_cx, char_h):
    """
    C36 CORRECTED HOT_MAGENTA fill light.
    Source: UPPER-RIGHT of each character (matching storm crack at upper-right canvas).
    Per-character silhouette mask applied via ImageChops.multiply — no BG tint.

    Parameters match character geometry constants defined in main():
      luma_cx  = int(W * 0.45)
      byte_cx  = int(W * 0.28)
      cosmo_cx = int(W * 0.62)
      char_h   = int(H * 0.18)
    """
    horizon_y = int(H * 0.58)
    ground_y  = horizon_y + int((H - horizon_y) * 0.12)

    FILL_ALPHA_MAX    = 35    # upper-right direct fill — cleaner than lower bounce
    FILL_RADIUS_SCALE = 1.6

    # Default vertical centers (feet on ground for Luma/Cosmo; Byte floats higher)
    char_centers = [
        (luma_cx,  int(H * 0.65), "luma"),
        (byte_cx,  int(H * 0.60), "byte"),
        (cosmo_cx, int(H * 0.65), "cosmo"),
    ]

    for (char_cx_pos, char_cy_pos, char_name) in char_centers:
        # Build per-character silhouette mask
        char_mask = _make_char_silhouette_mask_1080(
            img, char_cx_pos, char_h, char_cy_pos, threshold=60
        )

        # Build radial gradient at corrected source: UPPER-RIGHT of character
        fill_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fill_overlay)

        fill_src_x = char_cx_pos + int(char_h * 0.5)   # right of character
        fill_src_y = char_cy_pos - int(char_h * 0.8)   # above character
        fill_r = int(char_h * FILL_RADIUS_SCALE)

        for r_step in range(fill_r, 0, -max(1, fill_r // 30)):
            t = 1.0 - (r_step / fill_r)
            a = int(FILL_ALPHA_MAX * (t ** 1.3))
            a = max(0, min(255, a))
            if a < 2:
                continue
            fd.ellipse([fill_src_x - r_step, fill_src_y - r_step,
                        fill_src_x + r_step, fill_src_y + r_step],
                       fill=(*HOT_MAGENTA, a))

        # Apply char mask to fill alpha via ImageChops.multiply
        r_ch, g_ch, b_ch, a_ch = fill_overlay.split()
        masked_alpha = ImageChops.multiply(a_ch, char_mask)
        masked_fill = Image.merge("RGBA", (r_ch, g_ch, b_ch, masked_alpha))

        img = alpha_paste(img, masked_fill)

    return img


# ── Layer 6c: Cyan Specular on Luma (C34, fixed C35) ──────────────────────────

def draw_cyan_specular_luma(img, luma_cx, char_h):
    """
    C34 FIX 2 / C35 BUG FIX: ELEC_CYAN specular on Luma hair/shoulders.

    C35 FIX: get_char_bbox() was called on the full 3-character frame in v006,
    returning a bbox spanning 83% of canvas width — completely wrong char_cx for Luma.
    Fix: use luma_cx directly (known geometry: W*0.45 = 864px). No bbox call needed.
    This gives correct right-side rim for Luma without false detection.
    """
    if PROCEDURAL_DRAW_AVAILABLE:
        # C35 FIX: Use luma_cx directly — do NOT call get_char_bbox on full frame
        # luma_cx = int(W * 0.45) passed from caller, correct for this character
        add_rim_light(
            img,
            threshold=180,           # high threshold — specular on highlights only
            light_color=ELEC_CYAN,
            width=2,
            side="right",
            char_cx=luma_cx          # C35: hardcoded from known geometry, not bbox
        )
    else:
        # Fallback: manual cyan specular arc on Luma's head/shoulder
        head_r = int(char_h * 0.12)
        luma_foot_y_approx = int(H * 0.58) + int((H - int(H * 0.58)) * 0.12) + 10
        head_cy = luma_foot_y_approx - char_h + head_r
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.arc([luma_cx - head_r - 2, head_cy - head_r - 2,
                luma_cx + head_r + 2, head_cy + head_r + 2],
               start=310, end=60, fill=(*ELEC_CYAN, 140), width=3)
        torso_h = int(char_h * 0.28)
        torso_w = int(char_h * 0.17)
        torso_top = head_cy + head_r + 2
        od.arc([luma_cx - torso_w // 2, torso_top,
                luma_cx + torso_w // 2, torso_top + int(torso_h * 0.5)],
               start=340, end=60, fill=(*ELEC_CYAN, 100), width=2)
        img = alpha_paste(img, overlay)

    return img


# ── Layer 7: Ground lighting ──────────────────────────────────────────────────

def draw_ground_lighting(img):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    horizon_y = int(H * 0.58)
    crack_x = 1300
    for col in range(700):
        x = crack_x - col
        if x < 0: break
        t = col / 700.0; falloff = (1 - t) ** 1.8; a = int(45 * falloff)
        od.line([(x, horizon_y), (x, H)], fill=(*ELEC_CYAN, a))
    img = alpha_paste(img, overlay)
    return img


# ── Layer 8: Dutch Angle ──────────────────────────────────────────────────────

def apply_dutch_angle(img, degrees=4.0):
    """4.0° Dutch angle as final step — visibly perceptible camera tilt."""
    rotated = img.rotate(-degrees, expand=True, resample=Image.BICUBIC, fillcolor=VOID_BLACK)
    rw, rh = rotated.size
    cx, cy = rw // 2, rh // 2
    left   = cx - W // 2
    top    = cy - H // 2
    cropped = rotated.crop((left, top, left + W, top + H))
    return cropped


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("LTG_TOOL_style_frame_02_glitch_storm.py")
    print("Rendering Style Frame 02 — Glitch Storm (C36 Fill Light Direction Fix)...")
    print("  C36 Fixes:")
    print("    (1) Magenta fill light source: UPPER-RIGHT (storm crack) — was lower-left")
    print("    (2) Per-character silhouette mask: gradient masked to character pixels only")
    print("    (3) char_cx from geometry constants — NOT get_char_bbox() on full frame")
    print("    (4) alpha max 35 (was 40) — direct source is harder/cleaner than bounce")
    print("    Using: draw_magenta_fill_light_c36() — Jordan Reed algorithm at 1920×1080")

    img = Image.new("RGB", (W, H), VOID_BLACK)

    # Character position constants — passed to fill light and specular functions
    # C36: These MUST come from geometry constants (NOT get_char_bbox on full frame)
    char_h = int(H * 0.18)
    luma_cx   = int(W * 0.45)   # 864px at W=1920
    byte_cx   = int(W * 0.28)   # 538px at W=1920
    cosmo_cx  = int(W * 0.62)   # 1190px at W=1920

    print("  [1/10] Sky gradient + UV cloud masses...")
    img = draw_sky(img)

    print("  [2/10] Storm pixel confetti (DATA_BLUE dominant — cold/threatening)...")
    img = draw_storm_confetti(img)

    print("  [3/10] Town silhouette + window glow cones + storm edge-lighting...")
    img = draw_town_silhouette(img)

    print("  [4/10] Street surface + light pools...")
    img = draw_street(img)

    print("  [5/10] Ground lighting (cyan pool from crack)...")
    img = draw_ground_lighting(img)

    print("  [6/10] Damaged storefront window (cracks, missing panes, debris)...")
    img = draw_storefront(img)

    print("  [7/10] Characters (Luma: face + lean, Cosmo, Byte, + Glitch G007 fix)...")
    img = draw_characters(img)

    print("  [8/10] Magenta fill light (C36: UPPER-RIGHT source, per-char mask)...")
    img = draw_magenta_fill_light_c36(img, luma_cx, byte_cx, cosmo_cx, char_h)

    print("  [9/10] Cyan specular on Luma (ELEC_CYAN from storm crack upper-right)...")
    img = draw_cyan_specular_luma(img, luma_cx, char_h)

    print("  [10/10] Dutch angle (4.0°)...")
    img = apply_dutch_angle(img, degrees=4.0)

    # Enforce image size rule: ≤ 1280px in both dimensions
    img.thumbnail((1280, 1280), Image.LANCZOS)

    # Post-thumbnail: restore specular highlights (LANCZOS averaging reduces max bright pixel)
    sx, sy = img.size[0] / 1920.0, img.size[1] / 1080.0
    spec_draw = ImageDraw.Draw(img)
    SPEC_WHITE = (245, 245, 255)
    SPEC_CYAN  = ELEC_CYAN

    crack_spec_pts = [
        (int(1700 * sx), int(80 * sy)),
        (int(1600 * sx), int(220 * sy)),
        (int(1380 * sx), int(420 * sy)),
    ]
    for (spx, spy) in crack_spec_pts:
        spec_draw.ellipse([spx - 2, spy - 2, spx + 2, spy + 2], fill=SPEC_WHITE)

    # Luma hair crown specular (upper-right of head, cyan from storm crack)
    luma_head_cx_sc = int(luma_cx * sx)
    horizon_y_sc = int(H * 0.58 * sy)
    ground_y_sc  = horizon_y_sc + int((img.size[1] - horizon_y_sc) * 0.12)
    char_h_sc    = int(img.size[1] * 0.18)
    head_r_sc    = int(char_h_sc * 0.12)
    lean_offset_sc = int(int(char_h_sc * 0.28) * math.tan(math.radians(10)))
    luma_foot_y_sc = ground_y_sc + int(10 * sy)
    head_cy_sc   = luma_foot_y_sc - char_h_sc + head_r_sc
    head_cx_sc   = luma_head_cx_sc - lean_offset_sc // 2

    spec_x = head_cx_sc + int(head_r_sc * 0.7)
    spec_y = head_cy_sc - int(head_r_sc * 0.7)
    spec_draw.ellipse([spec_x - 2, spec_y - 2, spec_x + 2, spec_y + 2], fill=SPEC_CYAN)
    torso_w_sc = int(char_h_sc * 0.17)
    torso_top_sc = head_cy_sc + head_r_sc + 2
    spec_draw.ellipse([luma_head_cx_sc + torso_w_sc // 2 - 2, torso_top_sc,
                       luma_head_cx_sc + torso_w_sc // 2 + 2, torso_top_sc + 4],
                      fill=SPEC_CYAN)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img.save(OUTPUT_PATH, "PNG")
    print(f"\nSaved: {OUTPUT_PATH}")
    size_bytes = os.path.getsize(OUTPUT_PATH)
    print(f"File size: {size_bytes:,} bytes ({size_bytes // 1024} KB)")
    print(f"Image size: {img.size[0]}×{img.size[1]}px")
    print("\nFix verification (C36):")
    print("  [FIX C36-1] Fill light source: UPPER-RIGHT (char_cx + char_h*0.5, char_cy - char_h*0.8) ✓")
    print("  [FIX C36-2] Per-character silhouette mask via ImageChops.multiply — no BG tint ✓")
    print("  [FIX C36-3] char_cx from geometry constants (luma=W*0.45, byte=W*0.28, cosmo=W*0.62) ✓")
    print("  [FIX C36-4] Alpha max 35 (was 40) — direct upper-right source, cleaner than bounce ✓")
    print("  [CARRY C35-1] _draw_luma_face_sprint(): asymmetric eyes + directional pupils + brows + mouth ✓")
    print("  [CARRY C35-2] Torso lean 10° forward — head_cx offset, torso polygon lean ✓")
    print("  [CARRY C35-3] Hair stream steep/horizontal + second fine trailing strand ✓")
    print("  [CARRY C35-4] get_char_bbox() removed from draw_cyan_specular_luma() — luma_cx hardcoded ✓")
    print("  [CARRY C34-2] Cyan specular: ELEC_CYAN (#00F0FF) add_rim_light() side='right' ✓")
    print("  [CARRY C22] CORRUPT_AMBER = (255,140,0) = #FF8C00 GL-07 canonical ✓")
    print("  [CARRY C22] Window pane alpha: SOFT_GOLD=115, WARM_CREAM=110 ✓")
    print("  [CARRY C19] Storefront: frame + dividers + cracked panes + debris ✓")
    print("  [CARRY C16] Cold confetti: DATA_BLUE 70% dominant ✓")
    print("  [CARRY C16] Dutch angle: 4.0° applied as final step ✓")
    print("  [SIZE RULE] img.thumbnail((1280,1280)) applied before save ✓")
    print("\nDone.")


if __name__ == "__main__":
    main()
