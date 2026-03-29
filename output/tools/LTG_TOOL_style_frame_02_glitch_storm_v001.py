#!/usr/bin/env python3
"""
LTG_TOOL_style_frame_02_glitch_storm_v001.py
Style Frame 02 — "Glitch Storm" Background Generator
"Luma & the Glitchkin" — Cycle 12

Author: Jordan Reed, Background & Environment Artist
Date: 2026-03-29
Spec: /output/color/style_frames/style_frame_02_glitch_storm.md (Sam Kowalski, v2.0)

Renders the Glitch Storm compositing-ready background for Style Frame 02.
Includes: sky (storm + crack), town silhouette, main street, characters, storefront.
4-degree Dutch angle applied as final camera tilt.

Output: /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v001.png

Usage: python3 LTG_TOOL_style_frame_02_glitch_storm_v001.py
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

# ── Output ────────────────────────────────────────────────────────────────────
OUTPUT_PATH = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v001.png"
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
TERRA_CYAN_LIT  = (154, 140, 138)   # ENV-06 terracotta wall under cyan key
DEEP_WARM_SHAD  = ( 90,  56,  32)   # ENV-07 walls facing away from storm
ROOF_EDGE       = ( 26,  24,  32)   # ENV-08 roof lines
DEEP_COCOA      = ( 59,  40,  32)   # character hair, power lines

# Derived character storm colors
DRW_HOODIE_STORM    = (192, 122, 112)   # Luma hoodie under cyan key  DRW-07
DRW_SKIN_STORM      = (106, 180, 174)   # Luma skin under cyan key    DRW-08
DRW_HOODIE_SHADOW   = ( 58,  26,  20)   # Luma hoodie shadow side     DRW-03
DRW_JACKET_STORM    = (128, 192, 204)   # Cosmo jacket under cyan     DRW-09
DRW_JACKET_SHADOW   = ( 42,  26,  50)   # Cosmo jacket shadow         DRW-10
DRW_HAIR_MAGENTA    = (106,  42,  58)   # Luma hair magenta rim        DRW-17


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

    # UV_PURPLE cloud masses — angular, blocky, fractal silhouettes
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

    # Cloud mass 1 — upper left block cluster
    cloud_shapes = [
        # (x, y, w, h) rectangles approximating cloud silhouettes
        (0,    0,  520, 220),
        (80,  60,  380, 160),
        (20, 120,  260,  80),
        (460,  0,  200, 140),
        (380, 80,  180, 120),
    ]
    for (cx, cy, cw, ch) in cloud_shapes:
        # UV purple fill with some void black cutouts (fractal feel)
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle([cx, cy, cx + cw, cy + ch], fill=(*UV_PURPLE, 200))
        # Blocky bite out of edges
        bite_x = cx + int(cw * 0.55)
        bite_y = cy + int(ch * 0.30)
        od.rectangle([bite_x, bite_y, cx + cw, bite_y + int(ch * 0.40)],
                     fill=(*VOID_BLACK, 255))
        img = alpha_paste(img, overlay)
        draw = ImageDraw.Draw(img)

    # Cloud mass 2 — upper right (source side of crack)
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
        # Void core (deeper darkness inside storm)
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
    horizon_y = int(H * 0.55)   # where rooftops will be
    haze_height = int(H * 0.15)
    for dy in range(haze_height):
        t = 1.0 - (dy / haze_height)
        a = int(40 * t)
        od.line([(0, horizon_y - dy), (W, horizon_y - dy)],
                fill=(*UV_PURPLE, a))
    return alpha_paste(img, overlay)


def _draw_main_crack(img):
    """
    The primary sky crack: descends from upper-right corner to lower-center.
    Core: ELEC_CYAN max luminance
    Inner core: STATIC_WHITE overexposed center
    Edges: HOT_MAGENTA burn
    Geometry: partly orthogonal (90-degree angles mixed with diagonals)
    """
    # Crack path — list of (x, y) control points
    crack_pts = [
        (1820, 0),
        (1700, 80),
        (1700, 140),   # orthogonal drop
        (1600, 220),
        (1520, 220),   # orthogonal left
        (1460, 340),
        (1380, 420),
        (1380, 500),   # orthogonal drop
        (1280, 580),
        (1200, 640),
    ]

    # Draw glow passes: wide HOT_MAGENTA, medium ELEC_CYAN, thin STATIC_WHITE
    glow_specs = [
        (HOT_MAGENTA, 18, 80),   # color, half-width, alpha
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
        # (start_x, start_y, end_x, end_y)
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
        # Thinner: ELEC_CYAN fading to DATA_BLUE at tips
        od.line([(x0, y0), (x1, y1)], fill=(*ELEC_CYAN, 160), width=4)
        # Tip in DATA_BLUE
        mid_x = (x0 + x1) // 2
        mid_y = (y0 + y1) // 2
        od.line([(mid_x, mid_y), (x1, y1)], fill=(*DATA_BLUE, 120), width=2)
        img = alpha_paste(img, overlay)

    return img


def _draw_storm_edges(img):
    """HOT_MAGENTA burn lines along cloud mass edges."""
    draw = ImageDraw.Draw(img)
    # Short diagonal burn strokes along cloud perimeters
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
    Pixel confetti: ELEC_CYAN, STATIC_WHITE, HOT_MAGENTA, UV_PURPLE only.
    Acid Green FORBIDDEN in storm confetti (master_palette Forbidden #8).
    Size: 10–15px near crack, 2–4px at street level (governing physics: source-distance).
    """
    draw = ImageDraw.Draw(img)
    confetti_colors = [ELEC_CYAN, STATIC_WHITE, HOT_MAGENTA, UV_PURPLE]

    # High-altitude large particles — near crack zone (upper-right quadrant)
    for _ in range(240):
        cx = RNG.randint(1100, 1900)
        cy = RNG.randint(0, int(H * 0.55))
        # Distance from crack center (1400, 300) approximation
        dist = math.sqrt((cx - 1400) ** 2 + (cy - 300) ** 2)
        max_dist = 700.0
        t = clamp(dist / max_dist, 0.0, 1.0)
        size = int(15 - (15 - 3) * t)
        color = RNG.choice(confetti_colors)
        draw.rectangle([cx, cy, cx + size, cy + size], fill=color)

    # Mid-altitude scattered particles across storm zone
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

    # Low-altitude (street level) small particles near characters
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
    """
    draw = ImageDraw.Draw(img)

    horizon_y = int(H * 0.58)   # base of skyline = ground level top

    # ── Building roster (left to right) ──
    buildings = [
        # (left_x, roof_y, right_x, gutter_y, wall_color)
        (0,      horizon_y - 160, 180, horizon_y, DEEP_WARM_SHAD),       # left anchor
        (150,    horizon_y - 200, 320, horizon_y, DEEP_WARM_SHAD),
        (300,    horizon_y - 140, 440, horizon_y, TERRA_CYAN_LIT),       # cyan-lit face
        (420,    horizon_y - 260, 560, horizon_y, DEEP_WARM_SHAD),       # tall building
        (540,    horizon_y - 180, 680, horizon_y, TERRA_CYAN_LIT),
        # Clock tower center
        (660,    horizon_y - 340, 760, horizon_y, DEEP_WARM_SHAD),       # tower base
        (690,    horizon_y - 420, 730, horizon_y - 340, DEEP_WARM_SHAD), # tower spire
        # Right buildings (storm-lit terracotta facades)
        (760,    horizon_y - 190, 900, horizon_y, TERRA_CYAN_LIT),
        (880,    horizon_y - 150, 1020, horizon_y, DEEP_WARM_SHAD),
        (1000,   horizon_y - 220, 1140, horizon_y, TERRA_CYAN_LIT),
        (1120,   horizon_y - 170, 1260, horizon_y, DEEP_WARM_SHAD),
        (1240,   horizon_y - 240, 1380, horizon_y, TERRA_CYAN_LIT),
        (1360,   horizon_y - 130, 1500, horizon_y, DEEP_WARM_SHAD),
        (1480,   horizon_y - 200, 1620, horizon_y, TERRA_CYAN_LIT),
        (1600,   horizon_y - 160, 1740, horizon_y, DEEP_WARM_SHAD),
        (1720,   horizon_y - 210, W,    horizon_y, TERRA_CYAN_LIT),
    ]

    for (lx, ry, rx, gy, col) in buildings:
        draw.rectangle([lx, ry, rx, gy], fill=col)

    # Chimney stacks
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

    # Window glows — warm interior lights
    _draw_building_windows(img, buildings, horizon_y)

    # Power lines — 1px thin catenary arcs
    _draw_power_lines(img, horizon_y)

    # Cyan reflections on rain-wet chimney faces
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
        # 2 rows of windows, 2 windows wide (simplified)
        win_w = max(12, bld_w // 5)
        win_h = max(10, bld_h // 6)
        for row in range(2):
            for col in range(2):
                wx = lx + int(bld_w * (0.2 + col * 0.45))
                wy = ry + int(bld_h * (0.20 + row * 0.40))
                col_choice = RNG.choice(win_colors)
                # Some windows dark (evacuated)
                if RNG.random() < 0.35:
                    continue
                od.rectangle([wx, wy, wx + win_w, wy + win_h], fill=col_choice)

    img = alpha_paste(img, overlay)
    return img


def _draw_power_lines(img, horizon_y):
    """Thin catenary power lines between buildings."""
    draw = ImageDraw.Draw(img)
    # Pole positions
    poles = [120, 320, 520, 760, 950, 1150, 1350, 1550, 1750]
    wire_y = horizon_y - 100   # attachment height
    for i in range(len(poles) - 1):
        x0, x1 = poles[i], poles[i + 1]
        # Catenary approximation: sag at midpoint
        sag = int((x1 - x0) * 0.06)
        # Draw as polyline with 5 segments
        pts = []
        for s in range(6):
            t = s / 5.0
            x = int(x0 + t * (x1 - x0))
            # Parabolic sag
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

    # Base road — dark asphalt
    draw.rectangle([0, horizon_y, W, street_bottom], fill=DARK_ASPHALT)

    # Sidewalk strip (slightly lighter, cool)
    sidewalk_top = horizon_y
    sidewalk_bottom = horizon_y + int((street_bottom - horizon_y) * 0.12)
    draw.rectangle([0, sidewalk_top, W, sidewalk_bottom], fill=COOL_SIDEWALK)

    # Cyan light pool — below the crack (upper-right source)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    crack_floor_x = 1200   # crack lands around x=1200
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

    # Warm window spill on left sidewalk (from building interiors)
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

    # Road gutter lines
    draw = ImageDraw.Draw(img)
    draw.line([(0, sidewalk_bottom), (W, sidewalk_bottom)], fill=VOID_BLACK, width=2)

    return img


# ── Layer 5: Shattered Storefront (right foreground) ─────────────────────────

def draw_storefront(img):
    """
    Right foreground: shattered Millbrook Hardware storefront window.
    Frame: muted teal. Broken glass: STATIC_WHITE + ELEC_CYAN.
    Glitch cracks: ELEC_CYAN core, HOT_MAGENTA edge.
    """
    draw = ImageDraw.Draw(img)

    horizon_y = int(H * 0.58)
    # Storefront occupies right edge foreground
    sf_left  = int(W * 0.80)
    sf_right = W
    sf_top   = horizon_y - 80
    sf_bot   = horizon_y + int((H - horizon_y) * 0.55)

    MUTED_TEAL = (91, 140, 138)

    # Window frame
    draw.rectangle([sf_left, sf_top, sf_right, sf_bot], outline=MUTED_TEAL, width=6)

    # Interior glow (being consumed by glitch)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([sf_left + 6, sf_top + 6, sf_right - 6, sf_bot - 6],
                 fill=(*VOID_BLACK, 200))
    # Faint UV purple glow inside
    interior_cx = (sf_left + sf_right) // 2
    interior_cy = (sf_top + sf_bot) // 2
    for r in range(60, 0, -10):
        a = int(30 * (1 - r / 60.0))
        od.ellipse([interior_cx - r, interior_cy - r,
                    interior_cx + r, interior_cy + r],
                   fill=(*UV_PURPLE, a))
    img = alpha_paste(img, overlay)
    draw = ImageDraw.Draw(img)

    # Broken glass shards (static white + cyan reflections)
    glass_shards = [
        # triangular shards as polygons
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

    # Glitch cracks spreading from window
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
            # HOT_MAGENTA edge
            draw.line([(ox, oy), (ex, ey)], fill=HOT_MAGENTA, width=3)
            # ELEC_CYAN core
            draw.line([(ox, oy), (ex, ey)], fill=ELEC_CYAN, width=1)
        # Pixel confetti erupting from crack points
        for _ in range(8):
            px = ox + RNG.randint(-30, 30)
            py = oy + RNG.randint(-20, 40)
            ps = RNG.randint(3, 8)
            col = RNG.choice([ELEC_CYAN, HOT_MAGENTA, UV_PURPLE, STATIC_WHITE])
            draw.rectangle([px, py, px + ps, py + ps], fill=col)

    return img


# ── Layer 6: Characters ───────────────────────────────────────────────────────

def draw_characters(img):
    """
    Luma (left-third, sprint), Cosmo (behind/right of Luma), Byte (on Luma's left shoulder).
    Wide shot — characters small (~15% frame height), readable silhouettes.
    Simplified cartoon geometry: circles, polygons, ellipses.
    """
    draw = ImageDraw.Draw(img)

    horizon_y = int(H * 0.58)
    ground_y  = horizon_y + int((H - horizon_y) * 0.12)   # sidewalk surface

    # Luma center position — left third, slightly below mid-height
    luma_cx = int(W * 0.30)
    luma_foot_y = ground_y + 10
    char_h = int(H * 0.15)   # ~15% frame height = 162px
    luma_head_cy = luma_foot_y - char_h

    _draw_luma(img, luma_cx, luma_foot_y, char_h)
    _draw_cosmo(img, luma_cx + int(char_h * 0.55), luma_foot_y, char_h)
    _draw_byte_on_shoulder(img, luma_cx - int(char_h * 0.18),
                           luma_head_cy + int(char_h * 0.22), char_h)
    _draw_townspeople(img, horizon_y)

    return img


def _draw_luma(img, cx, foot_y, h):
    """Luma in full sprint — left foot forward, arms pumping, face turned back."""
    draw = ImageDraw.Draw(img)

    head_r = int(h * 0.12)
    torso_h = int(h * 0.28)
    torso_w = int(h * 0.17)
    leg_h   = int(h * 0.38)
    arm_h   = int(h * 0.26)

    # Torso base y
    head_cy = foot_y - h + head_r
    torso_top = head_cy + head_r + 2
    torso_bot = torso_top + torso_h
    torso_left  = cx - torso_w // 2
    torso_right = cx + torso_w // 2

    # ── Shadow (left/shadow side) ──
    # Torso
    shadow_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_overlay)
    sd.ellipse([torso_left, torso_top, cx, torso_bot], fill=(*DRW_HOODIE_SHADOW, 255))
    img = alpha_paste(img, shadow_overlay)
    draw = ImageDraw.Draw(img)

    # ── Lit side (right/cyan key) ──
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # Torso — hoodie (storm-modified orange)
    od.ellipse([torso_left, torso_top, torso_right, torso_bot],
               fill=(*DRW_HOODIE_STORM, 255))

    # Head
    od.ellipse([cx - head_r, head_cy - head_r,
                cx + head_r, head_cy + head_r],
               fill=(*DRW_SKIN_STORM, 255))

    # Hair — deep cocoa with magenta rim
    od.arc([cx - head_r, head_cy - head_r,
            cx + head_r, head_cy + head_r],
           start=190, end=360, fill=DEEP_COCOA, width=int(head_r * 0.5))
    # Magenta rim on hair top
    od.arc([cx - head_r + 2, head_cy - head_r + 2,
            cx + head_r - 2, head_cy + head_r - 2],
           start=190, end=330, fill=DRW_HAIR_MAGENTA, width=2)

    # Legs — sprint pose
    # Left leg forward (toward right)
    left_leg_pts = [
        (cx - 8, torso_bot),
        (cx + 30, torso_bot + int(leg_h * 0.55)),
        (cx + 50, foot_y),
    ]
    for i in range(len(left_leg_pts) - 1):
        od.line([left_leg_pts[i], left_leg_pts[i + 1]],
                fill=(*DRW_HOODIE_STORM, 255), width=int(torso_w * 0.35))

    # Right leg back (streaming behind)
    right_leg_pts = [
        (cx + 8, torso_bot),
        (cx - 25, torso_bot + int(leg_h * 0.50)),
        (cx - 40, foot_y - int(leg_h * 0.15)),
    ]
    for i in range(len(right_leg_pts) - 1):
        od.line([right_leg_pts[i], right_leg_pts[i + 1]],
                fill=(*DRW_HOODIE_SHADOW, 255), width=int(torso_w * 0.30))

    # Arms — pumping
    # Left arm forward (toward upper-right, pumping)
    larm_pts = [
        (cx - int(torso_w * 0.45), torso_top + int(torso_h * 0.20)),
        (cx + int(torso_w * 0.30), torso_top - int(arm_h * 0.45)),
    ]
    od.line(larm_pts, fill=(*DRW_HOODIE_STORM, 255), width=int(torso_w * 0.30))

    # Right arm back (streaming behind)
    rarm_pts = [
        (cx + int(torso_w * 0.35), torso_top + int(torso_h * 0.20)),
        (cx - int(torso_w * 0.50), torso_top + int(arm_h * 0.65)),
    ]
    od.line(rarm_pts, fill=(*DRW_HOODIE_SHADOW, 255), width=int(torso_w * 0.28))

    # Hair streaming behind (wind motion)
    hair_stream = [
        (cx - head_r + 4, head_cy),
        (cx - head_r - int(h * 0.06), head_cy - int(h * 0.04)),
        (cx - head_r - int(h * 0.11), head_cy + int(h * 0.01)),
    ]
    for i in range(len(hair_stream) - 1):
        od.line([hair_stream[i], hair_stream[i + 1]], fill=DEEP_COCOA, width=6)
    od.line([hair_stream[0], hair_stream[-1]], fill=DRW_HAIR_MAGENTA, width=2)

    # Cast shadow on road
    shadow_pts = [
        (cx - int(torso_w * 0.8), foot_y + 4),
        (cx + int(torso_w * 0.8), foot_y + 4),
        (cx + int(torso_w * 1.8), foot_y + 14),
        (cx - int(torso_w * 1.2), foot_y + 14),
    ]
    od.polygon(shadow_pts, fill=(10, 42, 58, 120))

    img = alpha_paste(img, overlay)
    return img


def _draw_cosmo(img, cx, foot_y, h):
    """Cosmo one stride behind — less graceful run, glasses, panic expression."""
    head_r = int(h * 0.115)
    torso_h = int(h * 0.26)
    torso_w = int(h * 0.155)
    leg_h   = int(h * 0.37)

    head_cy = foot_y - h + head_r
    torso_top = head_cy + head_r + 2
    torso_bot = torso_top + torso_h
    torso_left  = cx - torso_w // 2
    torso_right = cx + torso_w // 2

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # Torso (jacket — storm-modified lavender)
    od.ellipse([torso_left, torso_top, torso_right, torso_bot],
               fill=(*DRW_JACKET_STORM, 255))
    # Shadow side
    od.ellipse([torso_left, torso_top, cx, torso_bot],
               fill=(*DRW_JACKET_SHADOW, 255))

    # Head
    od.ellipse([cx - head_r, head_cy - head_r,
                cx + head_r, head_cy + head_r],
               fill=(*DRW_SKIN_STORM, 255))

    # Glasses — ELEC_CYAN reflections on lens faces
    gx0 = cx - int(head_r * 0.55)
    gy0 = head_cy - int(head_r * 0.08)
    gw, gh = int(head_r * 0.60), int(head_r * 0.40)
    # Left lens
    od.rectangle([gx0, gy0, gx0 + gw, gy0 + gh], outline=DEEP_COCOA, width=2)
    od.rectangle([gx0 + 2, gy0 + 2, gx0 + gw - 2, gy0 + gh - 2],
                 fill=(*ELEC_CYAN, 100))
    # Right lens
    od.rectangle([gx0 + gw + 4, gy0, gx0 + gw * 2 + 4, gy0 + gh],
                 outline=DEEP_COCOA, width=2)
    od.rectangle([gx0 + gw + 6, gy0 + 2, gx0 + gw * 2 + 2, gy0 + gh - 2],
                 fill=(*ELEC_CYAN, 100))

    # Wide open mouth (panic)
    od.ellipse([cx - int(head_r * 0.35), head_cy + int(head_r * 0.30),
                cx + int(head_r * 0.35), head_cy + int(head_r * 0.65)],
               fill=VOID_BLACK)

    # Legs — over-enthusiastic bad form
    # Both arms pumping too high
    for (dx, dy, shadow) in [(-12, torso_bot, False), (12, torso_bot, True)]:
        lx = cx + dx
        endx = lx + (25 if not shadow else -20)
        endy = foot_y - int(leg_h * 0.10 if not shadow else 0.25)
        col = DRW_JACKET_STORM if not shadow else DRW_JACKET_SHADOW
        od.line([(lx, dy), (endx, endy), (endx + (15 if not shadow else -10), foot_y)],
                fill=(*col, 255), width=int(torso_w * 0.32))

    # Arms too high
    od.line([(cx - int(torso_w * 0.4), torso_top + int(torso_h * 0.15)),
             (cx + int(torso_w * 0.2), head_cy - int(h * 0.08))],
            fill=(*DRW_JACKET_STORM, 255), width=int(torso_w * 0.28))
    od.line([(cx + int(torso_w * 0.4), torso_top + int(torso_h * 0.15)),
             (cx - int(torso_w * 0.2), head_cy - int(h * 0.08))],
            fill=(*DRW_JACKET_SHADOW, 255), width=int(torso_w * 0.28))

    # Jacket flapping open (visible at collar)
    od.line([(cx - int(torso_w * 0.35), torso_top + 5),
             (cx - int(torso_w * 0.50), torso_top + int(torso_h * 0.60))],
            fill=WARM_CREAM, width=3)

    img = alpha_paste(img, overlay)
    return img


def _draw_byte_on_shoulder(img, cx, cy, char_h):
    """
    Byte clinging to Luma's LEFT shoulder — tiny oval body, Corrupted Amber outline.
    Cracked eye (HOT_MAGENTA) faces right (toward crack/danger).
    Cyan eye faces left (toward Luma).
    """
    byte_h = int(char_h * 0.18)   # tiny in wide shot
    byte_w = int(byte_h * 1.3)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # Corrupted Amber outline (2px — Byte Visibility rule)
    od.ellipse([cx - byte_w // 2 - 2, cy - byte_h // 2 - 2,
                cx + byte_w // 2 + 2, cy + byte_h // 2 + 2],
               fill=(*CORRUPT_AMBER, 255))

    # Void black body
    od.ellipse([cx - byte_w // 2, cy - byte_h // 2,
                cx + byte_w // 2, cy + byte_h // 2],
               fill=(*VOID_BLACK, 255))

    # Inner cyan glow traces
    od.ellipse([cx - byte_w // 2 + 3, cy - byte_h // 2 + 2,
                cx + byte_w // 2 - 3, cy + byte_h // 2 - 2],
               outline=(*ELEC_CYAN, 80), width=2)

    # Cracked eye RIGHT (toward crack/danger) — HOT_MAGENTA
    ex_r = cx + int(byte_w * 0.25)
    ey   = cy - int(byte_h * 0.05)
    er   = max(2, int(byte_h * 0.14))
    od.ellipse([ex_r - er, ey - er, ex_r + er, ey + er], fill=(*HOT_MAGENTA, 255))
    # Crack line through eye
    od.line([(ex_r - er, ey - er), (ex_r + er, ey + er)], fill=VOID_BLACK, width=1)

    # Cyan eye LEFT (toward Luma)
    ex_l = cx - int(byte_w * 0.25)
    od.ellipse([ex_l - er, ey - er, ex_l + er, ey + er], fill=(*ELEC_CYAN, 255))

    # Claws gripping hoodie
    claw_y = cy + byte_h // 2
    for dx in [-int(byte_w * 0.30), int(byte_w * 0.30)]:
        od.line([(cx + dx, claw_y), (cx + dx - 3, claw_y + 5)],
                fill=(*ELEC_CYAN, 200), width=1)
        od.line([(cx + dx, claw_y), (cx + dx + 3, claw_y + 5)],
                fill=(*ELEC_CYAN, 200), width=1)

    # Flat back ears (scared)
    for side in [-1, 1]:
        ear_cx = cx + side * int(byte_w * 0.45)
        od.line([(cx + side * int(byte_w * 0.35), cy - byte_h // 2),
                 (ear_cx, cy - byte_h // 2 - int(byte_h * 0.4))],
                fill=(*CORRUPT_AMBER, 200), width=2)

    img = alpha_paste(img, overlay)
    return img


def _draw_townspeople(img, horizon_y):
    """3–5 background townspeople — simplified desaturated silhouettes."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    NIGHT_SILHOUETTE = (42, 42, 56, 200)
    ground_y = horizon_y

    townspeople = [
        (120, ground_y, int(H * 0.06)),    # in doorway
        (280, ground_y, int(H * 0.055)),   # pressed against wall
        (680, ground_y - 20, int(H * 0.05)),  # at window above
        (900, ground_y, int(H * 0.065)),   # running away
        (1050, ground_y, int(H * 0.055)),  # standing in doorway
    ]

    for (px, py, ph) in townspeople:
        pw = int(ph * 0.40)
        # Head
        head_r = int(ph * 0.13)
        head_cy = py - ph + head_r
        od.ellipse([px - head_r, head_cy - head_r,
                    px + head_r, head_cy + head_r], fill=NIGHT_SILHOUETTE)
        # Body
        od.rectangle([px - pw // 2, head_cy + head_r,
                      px + pw // 2, py], fill=NIGHT_SILHOUETTE)
        # Warm window light on faces
        od.ellipse([px - head_r, head_cy - head_r,
                    px + head_r, head_cy + head_r],
                   fill=(*SOFT_GOLD, 40))

    img = alpha_paste(img, overlay)
    return img


# ── Layer 7: Cyan Light Pool on Ground ───────────────────────────────────────

def draw_ground_lighting(img):
    """Strong cyan pool on tarmac directly below crack, fading left."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    horizon_y = int(H * 0.58)

    crack_x = 1300   # where crack hits ground level
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


# ── Layer 8: Dutch Angle (4° clockwise) ──────────────────────────────────────

def apply_dutch_angle(img, degrees=4.0):
    """
    Rotate the full composition by 4° clockwise — the camera tilt.
    Expand to avoid cropping, then crop back to 1920x1080.
    """
    rotated = img.rotate(-degrees, expand=True, resample=Image.BICUBIC,
                         fillcolor=VOID_BLACK)
    # Center-crop back to original size
    rw, rh = rotated.size
    cx, cy = rw // 2, rh // 2
    left   = cx - W // 2
    top    = cy - H // 2
    cropped = rotated.crop((left, top, left + W, top + H))
    return cropped


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("LTG_TOOL_style_frame_02_glitch_storm_v001.py")
    print("Rendering Style Frame 02 — Glitch Storm background...")

    # Build scene on RGB canvas
    img = Image.new("RGB", (W, H), VOID_BLACK)

    # Layer order (back to front)
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

    print("  [7/8] Characters (Luma, Cosmo, Byte)...")
    img = draw_characters(img)

    print("  [8/8] Dutch angle (4° clockwise)...")
    img = apply_dutch_angle(img, degrees=4.0)

    # Save
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img.save(OUTPUT_PATH, "PNG")
    print(f"\nSaved: {OUTPUT_PATH}")
    print(f"Size: {img.size[0]}x{img.size[1]}")

    import os as _os
    size_bytes = _os.path.getsize(OUTPUT_PATH)
    print(f"File size: {size_bytes:,} bytes ({size_bytes // 1024} KB)")
    print("\nDone.")


if __name__ == "__main__":
    main()
