#!/usr/bin/env python3
"""
LTG_TOOL_style_frame_02_glitch_storm_v002.py
Style Frame 02 — "Glitch Storm" — Character Composite Pass
"Luma & the Glitchkin" — Cycle 13

Art Director: Alex Chen
Date: 2026-03-30
Based on: LTG_TOOL_style_frame_02_glitch_storm_v001.py (Jordan Reed, Cycle 12)

Cycle 13 changes (Alex Chen — Victoria Ashford BLOCKER resolution):
  v001 had Byte on Luma's left shoulder, Cosmo immediately behind Luma.
  v002 fully composites three characters sprinting left-to-right across frame:
    - Byte: hovering LEFT of Luma (~28% from left), floating above ground.
      Narrative: Byte scouts ahead (or flanks), classic mid-air float posture.
      VOID_BLACK body fill (see Naomi Bridges / byte.md for storm-scene rationale).
      Corrupted Amber 2px outline per GL-07 visibility rule.
    - Luma: CENTER (~45% from left). Sprint pose — decisive, urgent.
      Corrupted Amber 2px outline where hoodie meets dark BG.
    - Cosmo: RIGHT of Luma (~62% from left). One stride behind.
      Running with less grace — panic + glasses.
  All characters share the 4° Dutch angle via apply_dutch_angle() at end.
  Char height: ~18% frame height (was 15%) — more readable wide shot.

Output: /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v002.png
Usage: python3 LTG_TOOL_style_frame_02_glitch_storm_v002.py
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_PATH = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v002.png"
W, H = 1920, 1080

# ── Master Palette ────────────────────────────────────────────────────────────
WARM_CREAM      = (250, 240, 220)
SOFT_GOLD       = (232, 201,  90)
SUNLIT_AMBER    = (212, 146,  58)
TERRACOTTA      = (199,  91,  57)
SAGE_GREEN      = (122, 158, 126)
DUSTY_LAVENDER  = (168, 155, 191)

VOID_BLACK      = ( 10,  10,  20)
ELEC_CYAN       = (  0, 240, 255)
ACID_GREEN      = ( 57, 255,  20)
DATA_BLUE       = ( 43, 127, 255)
UV_PURPLE       = (123,  47, 190)
HOT_MAGENTA     = (255,  45, 107)
STATIC_WHITE    = (240, 240, 240)
CORRUPT_AMBER   = (255, 140,   0)

# ENV colors
NIGHT_SKY_DEEP  = ( 26,  20,  40)
DARK_ASPHALT    = ( 42,  42,  56)
CYAN_ROAD       = ( 42,  90, 106)
WARM_ROAD       = ( 74,  58,  42)
COOL_SIDEWALK   = ( 58,  56,  72)
TERRA_CYAN_LIT  = (150, 172, 162)  # ENV-06 fix (Cycle 13, Jordan Reed): G=172>R=150, B=162>R=150 — cyan-tinted. Old (154,140,138) was warm grey.
DEEP_WARM_SHAD  = ( 90,  56,  32)
ROOF_EDGE       = ( 26,  24,  32)
DEEP_COCOA      = ( 59,  40,  32)

# Character storm colors
DRW_HOODIE_STORM    = (192, 122, 112)
DRW_SKIN_STORM      = (106, 180, 174)
DRW_HOODIE_SHADOW   = ( 58,  26,  20)
DRW_JACKET_STORM    = (128, 192, 204)
DRW_JACKET_SHADOW   = ( 42,  26,  50)
DRW_HAIR_MAGENTA    = (106,  42,  58)
BYTE_TEAL           = (  0, 212, 232)

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


# ── Layer 2: Storm Confetti ───────────────────────────────────────────────────

def draw_storm_confetti(img):
    draw = ImageDraw.Draw(img)
    confetti_colors = [ELEC_CYAN, STATIC_WHITE, HOT_MAGENTA, UV_PURPLE]
    for _ in range(240):
        cx = RNG.randint(1100, 1900); cy = RNG.randint(0, int(H * 0.55))
        dist = math.sqrt((cx - 1400) ** 2 + (cy - 300) ** 2)
        t = clamp(dist / 700.0, 0.0, 1.0)
        size = int(15 - (15 - 3) * t)
        color = RNG.choice(confetti_colors)
        draw.rectangle([cx, cy, cx + size, cy + size], fill=color)
    for _ in range(160):
        cx = RNG.randint(600, 1900); cy = RNG.randint(int(H * 0.25), int(H * 0.60))
        size = RNG.randint(3, 8); color = RNG.choice(confetti_colors)
        alpha_draw = RNG.randint(140, 220)
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle([cx, cy, cx + size, cy + size], fill=(*color, alpha_draw))
        img = alpha_paste(img, overlay)
    draw = ImageDraw.Draw(img)
    for _ in range(80):
        cx = RNG.randint(300, 900); cy = RNG.randint(int(H * 0.65), H)
        size = RNG.randint(2, 4); color = RNG.choice(confetti_colors)
        draw.rectangle([cx, cy, cx + size, cy + size], fill=color)
    return img


# ── Layer 3: Town Silhouette ──────────────────────────────────────────────────

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
    _draw_building_windows(img, buildings, horizon_y)
    _draw_power_lines(img, horizon_y)
    draw = ImageDraw.Draw(img)
    for (x0, y0, x1, y1) in chimneys[:3]:
        draw.line([(x0, y0), (x0, y1)], fill=(*ELEC_CYAN, 60), width=1)
    return img


def _draw_building_windows(img, buildings, horizon_y):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    win_colors = [(*SOFT_GOLD, 180), (*WARM_CREAM, 160)]
    for (lx, ry, rx, gy, _) in buildings:
        bld_w = rx - lx; bld_h = gy - ry
        if bld_w < 60 or bld_h < 60:
            continue
        win_w = max(12, bld_w // 5); win_h = max(10, bld_h // 6)
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
    horizon_y = int(H * 0.58); street_bottom = H
    draw.rectangle([0, horizon_y, W, street_bottom], fill=DARK_ASPHALT)
    sidewalk_top = horizon_y
    sidewalk_bottom = horizon_y + int((street_bottom - horizon_y) * 0.12)
    draw.rectangle([0, sidewalk_top, W, sidewalk_bottom], fill=COOL_SIDEWALK)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    crack_floor_x = 1200; pool_width = 560
    pool_height = int((street_bottom - horizon_y) * 0.7)
    for col in range(pool_width):
        t = col / pool_width; falloff = (1 - t) ** 2.0; a = int(55 * falloff)
        x = crack_floor_x - col
        od.line([(x, horizon_y), (x, horizon_y + pool_height)], fill=(*CYAN_ROAD, a))
    img = alpha_paste(img, overlay)

    overlay2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od2 = ImageDraw.Draw(overlay2)
    spill_w = 420; spill_h = int((street_bottom - horizon_y) * 0.35)
    for col in range(spill_w):
        t = col / spill_w; falloff = (1 - t) ** 2.2; a = int(40 * falloff)
        od2.line([(col, sidewalk_bottom), (col, sidewalk_bottom + spill_h)], fill=(*SOFT_GOLD, a))
    img = alpha_paste(img, overlay2)

    draw = ImageDraw.Draw(img)
    draw.line([(0, sidewalk_bottom), (W, sidewalk_bottom)], fill=VOID_BLACK, width=2)
    return img


# ── Layer 5: Shattered Storefront ────────────────────────────────────────────

def draw_storefront(img):
    draw = ImageDraw.Draw(img)
    horizon_y = int(H * 0.58)
    sf_left  = int(W * 0.80); sf_right = W
    sf_top   = horizon_y - 80; sf_bot = horizon_y + int((H - horizon_y) * 0.55)
    MUTED_TEAL = (91, 140, 138)
    draw.rectangle([sf_left, sf_top, sf_right, sf_bot], outline=MUTED_TEAL, width=6)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([sf_left + 6, sf_top + 6, sf_right - 6, sf_bot - 6], fill=(*VOID_BLACK, 200))
    interior_cx = (sf_left + sf_right) // 2; interior_cy = (sf_top + sf_bot) // 2
    for r in range(60, 0, -10):
        a = int(30 * (1 - r / 60.0))
        od.ellipse([interior_cx - r, interior_cy - r, interior_cx + r, interior_cy + r],
                   fill=(*UV_PURPLE, a))
    img = alpha_paste(img, overlay)
    draw = ImageDraw.Draw(img)

    glass_shards = [
        [(sf_left + 20, sf_top + 10), (sf_left + 60, sf_top + 8), (sf_left + 35, sf_top + 45)],
        [(sf_left + 80, sf_top + 5), (sf_left + 130, sf_top + 12), (sf_left + 100, sf_top + 55)],
        [(sf_left + 50, sf_top + 30), (sf_left + 90, sf_top + 25), (sf_left + 70, sf_top + 70)],
        [(sf_left + 10, sf_top + 50), (sf_left + 45, sf_top + 45), (sf_left + 25, sf_top + 85)],
    ]
    for shard in glass_shards:
        draw.polygon(shard, fill=STATIC_WHITE, outline=(*ELEC_CYAN, 180))
    crack_origins = [(sf_left + 40, sf_top + 20), (sf_left + 110, sf_top + 30), (sf_left, sf_top + 60)]
    for (ox, oy) in crack_origins:
        for angle_offset in [-30, 0, 30]:
            angle = math.radians(200 + angle_offset)
            length = RNG.randint(60, 120)
            ex = int(ox + math.cos(angle) * length); ey = int(oy + math.sin(angle) * length)
            draw.line([(ox, oy), (ex, ey)], fill=HOT_MAGENTA, width=3)
            draw.line([(ox, oy), (ex, ey)], fill=ELEC_CYAN, width=1)
        for _ in range(8):
            px = ox + RNG.randint(-30, 30); py = oy + RNG.randint(-20, 40); ps = RNG.randint(3, 8)
            col = RNG.choice([ELEC_CYAN, HOT_MAGENTA, UV_PURPLE, STATIC_WHITE])
            draw.rectangle([px, py, px + ps, py + ps], fill=col)
    return img


# ── Layer 6: Characters (v002 — repositioned composite) ──────────────────────

def draw_characters(img):
    """
    Cycle 13 v002 character layout — sprinting left-to-right across frame.
    Positions changed from v001 (Byte was on shoulder; Cosmo immediately behind Luma):

    v002 layout (per Victoria Ashford BLOCKER direction + Art Director brief):
      - Byte: hovering LEFT at ~28% canvas width, floating above ground level
        Body fill: VOID_BLACK (narrative decision, see byte.md — storm-scene variant)
        CORRUPT_AMBER outline applied for figure-ground separation.
      - Luma: CENTER at ~45% canvas width, sprint pose.
        CORRUPT_AMBER 2px outline on hoodie silhouette edges.
      - Cosmo: RIGHT at ~62% canvas width, one stride behind.

    Dutch angle: applied by apply_dutch_angle() after this layer.
    Character height: ~18% frame height (was 15%) for wider-shot readability.
    """
    horizon_y = int(H * 0.58)
    ground_y  = horizon_y + int((H - horizon_y) * 0.12)
    char_h = int(H * 0.18)   # 18% frame height — more readable than v001's 15%

    # Luma: CENTER
    luma_cx = int(W * 0.45)
    luma_foot_y = ground_y + 10
    luma_head_cy = luma_foot_y - char_h

    # Byte: hovering LEFT — floats at ~35% character height above ground
    byte_cx = int(W * 0.28)
    byte_float_y = luma_head_cy + int(char_h * 0.30)  # shoulder height, but free-floating

    # Cosmo: RIGHT, one stride behind
    cosmo_cx = int(W * 0.62)
    cosmo_foot_y = ground_y + 14   # slightly behind (higher y = more bg)

    img = _draw_luma(img, luma_cx, luma_foot_y, char_h)
    img = _draw_cosmo(img, cosmo_cx, cosmo_foot_y, char_h)
    img = _draw_byte_hovering(img, byte_cx, byte_float_y, char_h)
    img = _draw_townspeople(img, horizon_y)

    return img


def _draw_luma(img, cx, foot_y, h):
    """Luma in full sprint — left foot forward, arms pumping.
    Corrupted Amber 2px outline on hoodie edges for figure-ground separation."""
    head_r  = int(h * 0.12)
    torso_h = int(h * 0.28)
    torso_w = int(h * 0.17)
    leg_h   = int(h * 0.38)

    head_cy   = foot_y - h + head_r
    torso_top = head_cy + head_r + 2
    torso_bot = torso_top + torso_h
    torso_left  = cx - torso_w // 2
    torso_right = cx + torso_w // 2

    # Corrupted Amber outline (figure-ground vs dark storm BG)
    outline_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ol = ImageDraw.Draw(outline_layer)
    # Torso outline
    ol.ellipse([torso_left - 2, torso_top - 2, torso_right + 2, torso_bot + 2],
               outline=(*CORRUPT_AMBER, 220), width=2)
    # Head outline
    ol.ellipse([cx - head_r - 2, head_cy - head_r - 2, cx + head_r + 2, head_cy + head_r + 2],
               outline=(*CORRUPT_AMBER, 180), width=2)
    img = alpha_paste(img, outline_layer)

    # Shadow side
    shadow_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_overlay)
    sd.ellipse([torso_left, torso_top, cx, torso_bot], fill=(*DRW_HOODIE_SHADOW, 255))
    img = alpha_paste(img, shadow_overlay)

    # Lit side
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    od.ellipse([torso_left, torso_top, torso_right, torso_bot], fill=(*DRW_HOODIE_STORM, 255))
    od.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
               fill=(*DRW_SKIN_STORM, 255))

    # Hair
    od.arc([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
           start=190, end=360, fill=DEEP_COCOA, width=int(head_r * 0.5))
    od.arc([cx - head_r + 2, head_cy - head_r + 2, cx + head_r - 2, head_cy + head_r - 2],
           start=190, end=330, fill=DRW_HAIR_MAGENTA, width=2)

    # Legs — sprint, left foot forward
    left_leg_pts = [(cx - 8, torso_bot), (cx + 30, torso_bot + int(leg_h * 0.55)), (cx + 50, foot_y)]
    for i in range(len(left_leg_pts) - 1):
        od.line([left_leg_pts[i], left_leg_pts[i + 1]], fill=(*DRW_HOODIE_STORM, 255), width=int(torso_w * 0.35))

    right_leg_pts = [(cx + 8, torso_bot), (cx - 25, torso_bot + int(leg_h * 0.50)), (cx - 40, foot_y - int(leg_h * 0.15))]
    for i in range(len(right_leg_pts) - 1):
        od.line([right_leg_pts[i], right_leg_pts[i + 1]], fill=(*DRW_HOODIE_SHADOW, 255), width=int(torso_w * 0.30))

    # Arms pumping
    od.line([(cx - int(torso_w * 0.45), torso_top + int(torso_h * 0.20)),
             (cx + int(torso_w * 0.30), torso_top - int(h * 0.45 * 0.45))],
            fill=(*DRW_HOODIE_STORM, 255), width=int(torso_w * 0.30))
    od.line([(cx + int(torso_w * 0.35), torso_top + int(torso_h * 0.20)),
             (cx - int(torso_w * 0.50), torso_top + int(h * 0.26 * 0.65))],
            fill=(*DRW_HOODIE_SHADOW, 255), width=int(torso_w * 0.28))

    # Hair streaming
    hair_stream = [
        (cx - head_r + 4, head_cy),
        (cx - head_r - int(h * 0.06), head_cy - int(h * 0.04)),
        (cx - head_r - int(h * 0.11), head_cy + int(h * 0.01)),
    ]
    for i in range(len(hair_stream) - 1):
        od.line([hair_stream[i], hair_stream[i + 1]], fill=DEEP_COCOA, width=6)
    od.line([hair_stream[0], hair_stream[-1]], fill=DRW_HAIR_MAGENTA, width=2)

    # Cast shadow
    shadow_pts = [
        (cx - int(torso_w * 0.8), foot_y + 4), (cx + int(torso_w * 0.8), foot_y + 4),
        (cx + int(torso_w * 1.8), foot_y + 14), (cx - int(torso_w * 1.2), foot_y + 14),
    ]
    od.polygon(shadow_pts, fill=(10, 42, 58, 120))

    img = alpha_paste(img, overlay)
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

    # Glasses
    gx0 = cx - int(head_r * 0.55); gy0 = head_cy - int(head_r * 0.08)
    gw, gh = int(head_r * 0.60), int(head_r * 0.40)
    od.rectangle([gx0, gy0, gx0 + gw, gy0 + gh], outline=DEEP_COCOA, width=2)
    od.rectangle([gx0 + 2, gy0 + 2, gx0 + gw - 2, gy0 + gh - 2], fill=(*ELEC_CYAN, 100))
    od.rectangle([gx0 + gw + 4, gy0, gx0 + gw * 2 + 4, gy0 + gh], outline=DEEP_COCOA, width=2)
    od.rectangle([gx0 + gw + 6, gy0 + 2, gx0 + gw * 2 + 2, gy0 + gh - 2], fill=(*ELEC_CYAN, 100))

    # Panic mouth
    od.ellipse([cx - int(head_r * 0.35), head_cy + int(head_r * 0.30),
                cx + int(head_r * 0.35), head_cy + int(head_r * 0.65)], fill=VOID_BLACK)

    # Legs
    for (dx, dy, shadow) in [(-12, torso_bot, False), (12, torso_bot, True)]:
        lx = cx + dx
        endx = lx + (25 if not shadow else -20)
        endy = foot_y - int(leg_h * 0.10 if not shadow else 0.25)
        col = DRW_JACKET_STORM if not shadow else DRW_JACKET_SHADOW
        od.line([(lx, dy), (endx, endy), (endx + (15 if not shadow else -10), foot_y)],
                fill=(*col, 255), width=int(torso_w * 0.32))

    # Arms too high (panic run)
    od.line([(cx - int(torso_w * 0.4), torso_top + int(torso_h * 0.15)),
             (cx + int(torso_w * 0.2), head_cy - int(h * 0.08))],
            fill=(*DRW_JACKET_STORM, 255), width=int(torso_w * 0.28))
    od.line([(cx + int(torso_w * 0.4), torso_top + int(torso_h * 0.15)),
             (cx - int(torso_w * 0.2), head_cy - int(h * 0.08))],
            fill=(*DRW_JACKET_SHADOW, 255), width=int(torso_w * 0.28))

    # Jacket collar flap
    od.line([(cx - int(torso_w * 0.35), torso_top + 5),
             (cx - int(torso_w * 0.50), torso_top + int(torso_h * 0.60))],
            fill=WARM_CREAM, width=3)

    img = alpha_paste(img, overlay)
    return img


def _draw_byte_hovering(img, cx, cy, char_h):
    """
    Byte hovering LEFT of Luma — free-floating sprint companion.
    Narrative decision (Cycle 13, Alex Chen / Naomi Bridges flag):
      Byte uses VOID_BLACK body fill in SF02 rather than canonical Byte Teal (#00D4E8).
      This is INTENTIONAL — Byte is nearly consumed by the Void during the Glitch Storm.
      His teal identity is suppressed; he is visible only by his Corrupted Amber warning outline.
      This is a strong narrative color statement: Byte is most at risk in this scene.
      He fights through the storm visible only as an amber-outlined void shape.
      See byte.md Section 'Storm-Scene Variant' for full documentation.
    CORRUPT_AMBER 2px outline is mandatory here for figure-ground legibility.
    """
    byte_h = int(char_h * 0.40)    # Byte is ~40% of Luma's height
    byte_w = int(byte_h * 1.30)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # Corrupted Amber outer glow — makes him visible against storm sky
    for offset in [4, 3, 2]:
        od.ellipse([cx - byte_w // 2 - offset, cy - byte_h // 2 - offset,
                    cx + byte_w // 2 + offset, cy + byte_h // 2 + offset],
                   outline=(*CORRUPT_AMBER, 200 - offset * 30), width=1)

    # VOID_BLACK body — storm-scene variant (intentional, not an error)
    od.ellipse([cx - byte_w // 2, cy - byte_h // 2,
                cx + byte_w // 2, cy + byte_h // 2],
               fill=(*VOID_BLACK, 255))

    # Inner cyan glow traces — faint traces of teal identity surviving
    od.ellipse([cx - byte_w // 2 + 3, cy - byte_h // 2 + 2,
                cx + byte_w // 2 - 3, cy + byte_h // 2 - 2],
               outline=(*ELEC_CYAN, 60), width=2)

    # RIGHT eye (facing direction of sprint): HOT_MAGENTA cracked — danger ahead
    eye_r = max(3, int(byte_h * 0.14))
    ex_r = cx + int(byte_w * 0.25)
    ey   = cy - int(byte_h * 0.05)
    od.ellipse([ex_r - eye_r, ey - eye_r, ex_r + eye_r, ey + eye_r], fill=(*HOT_MAGENTA, 255))
    od.line([(ex_r - eye_r, ey - eye_r), (ex_r + eye_r, ey + eye_r)], fill=VOID_BLACK, width=1)

    # LEFT eye (away from danger): ELEC_CYAN — his remaining digital identity
    ex_l = cx - int(byte_w * 0.25)
    od.ellipse([ex_l - eye_r, ey - eye_r, ex_l + eye_r, ey + eye_r], fill=(*ELEC_CYAN, 255))

    # Sprint ears — pressed back in wind
    for side in [-1, 1]:
        ear_cx = cx + side * int(byte_w * 0.45)
        od.line([(cx + side * int(byte_w * 0.35), cy - byte_h // 2),
                 (ear_cx, cy - byte_h // 2 - int(byte_h * 0.4))],
                fill=(*CORRUPT_AMBER, 200), width=2)

    # Floating pixel confetti trail below Byte
    float_rng = random.Random(99)
    for _ in range(8):
        px = cx + float_rng.randint(-byte_w // 2, byte_w // 2)
        py = cy + byte_h // 2 + float_rng.randint(4, 20)
        ps = float_rng.choice([3, 4, 5])
        pc = float_rng.choice([ELEC_CYAN, CORRUPT_AMBER, HOT_MAGENTA])
        od.rectangle([px, py, px + ps, py + ps], fill=(*pc, 180))

    img = alpha_paste(img, overlay)
    return img


def _draw_townspeople(img, horizon_y):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    NIGHT_SILHOUETTE = (42, 42, 56, 200)
    ground_y = horizon_y
    townspeople = [
        (120, ground_y, int(H * 0.06)), (280, ground_y, int(H * 0.055)),
        (680, ground_y - 20, int(H * 0.05)), (900, ground_y, int(H * 0.065)),
        (1050, ground_y, int(H * 0.055)),
    ]
    for (px, py, ph) in townspeople:
        pw = int(ph * 0.40)
        head_r = int(ph * 0.13)
        head_cy = py - ph + head_r
        od.ellipse([px - head_r, head_cy - head_r, px + head_r, head_cy + head_r],
                   fill=NIGHT_SILHOUETTE)
        od.rectangle([px - pw // 2, head_cy + head_r, px + pw // 2, py], fill=NIGHT_SILHOUETTE)
        od.ellipse([px - head_r, head_cy - head_r, px + head_r, head_cy + head_r],
                   fill=(*SOFT_GOLD, 40))
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
    rotated = img.rotate(-degrees, expand=True, resample=Image.BICUBIC, fillcolor=VOID_BLACK)
    rw, rh = rotated.size
    cx, cy = rw // 2, rh // 2
    left   = cx - W // 2
    top    = cy - H // 2
    cropped = rotated.crop((left, top, left + W, top + H))
    return cropped


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("LTG_TOOL_style_frame_02_glitch_storm_v002.py")
    print("Rendering Style Frame 02 — Glitch Storm (Character Composite Pass)...")

    img = Image.new("RGB", (W, H), VOID_BLACK)

    print("  [1/8] Sky gradient + UV cloud masses...")
    img = draw_sky(img)

    print("  [2/8] Storm pixel confetti...")
    img = draw_storm_confetti(img)

    print("  [3/8] Town silhouette...")
    img = draw_town_silhouette(img)

    print("  [4/8] Street surface + light pools...")
    img = draw_street(img)

    print("  [5/8] Ground lighting (cyan pool)...")
    img = draw_ground_lighting(img)

    print("  [6/8] Shattered storefront (right foreground)...")
    img = draw_storefront(img)

    print("  [7/8] Characters (Byte L, Luma C, Cosmo R — sprint composite)...")
    img = draw_characters(img)

    print("  [8/8] Dutch angle (4° clockwise)...")
    img = apply_dutch_angle(img, degrees=4.0)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img.save(OUTPUT_PATH, "PNG")
    print(f"\nSaved: {OUTPUT_PATH}")
    size_bytes = os.path.getsize(OUTPUT_PATH)
    print(f"File size: {size_bytes:,} bytes ({size_bytes // 1024} KB)")
    print("\nDone.")


if __name__ == "__main__":
    main()
