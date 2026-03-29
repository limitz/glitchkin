#!/usr/bin/env python3
"""
LTG_TOOL_bg_tech_den_v002.py — Cosmo's Tech Den Background v002 (Daylight)
"Luma & the Glitchkin" — Background & Environment Design
Artist: Jordan Reed | Cycle 20

Critique fix pass (Takeshi Murakami C+):
  1. Window light shaft: trapezoid of warm amber (SUNLIT_AMBER ~212,172,100)
     falling across floor + desk, feathered soft edge, ~15 dust motes in beam
  2. Monitor glow spill: blue-white (180,200,210, alpha 40-60) cast onto chair
     back/seat, desk surface in front of monitors, nearest shelving face
  3. Right half completion: explicit bedding/pillow polygon, device on mattress
     edge, wall above bed with poster + 2 taped printouts
  4. Cosmo's jacket: dusty lavender (RW-08, ~160,150,175) clearly draped over
     chair back as readable silhouette

Rules:
  - Real World palette ONLY — zero Glitch palette colors
  - After img.paste() / alpha_composite: refresh draw = ImageDraw.Draw(img)
  - Never overwrite outputs — versioned v002

Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_tech_den_v002.png
"""

import math
import random
import os
from PIL import Image, ImageDraw, ImageFilter

W, H = 1280, 720

# ── Real World Palette (NO Glitch colors) ────────────────────────────────────
WALL_WARM         = (240, 228, 200)
WALL_SHADOW       = (208, 192, 162)
WALL_WINDOW_LIGHT = (252, 242, 210)
CEILING           = (244, 236, 212)
FLOOR_WOOD        = (158, 118,  68)
FLOOR_WOOD_DARK   = (128,  90,  48)
FLOOR_WORN        = (172, 132,  82)
SKIRTING          = (190, 155, 105)

# Window / natural light
WINDOW_SKY        = (188, 218, 240)
WINDOW_FRAME      = (222, 200, 158)
SUNLIGHT_GOLD     = (255, 210,  90)
SUNLIT_AMBER      = (212, 172, 100)   # per Takeshi brief: warm amber shaft RGB ~212,172,100
WALL_SUNLIT       = (252, 238, 190)

# Desk and tech equipment
DESK_WOOD_TOP     = (148, 105,  58)
DESK_WOOD_SHADOW  = (108,  72,  36)
DESK_FRAME        = ( 80,  62,  44)
CABLE_DARK        = ( 58,  48,  38)
CABLE_MED         = ( 90,  72,  52)
CABLE_GREY        = (110, 108, 102)

# CRT monitor (muted teal casing — RW-12)
CRT_CASING        = ( 91, 140, 138)
CRT_SHADOW        = ( 58,  90,  88)
CRT_SCREEN_OFF    = ( 28,  34,  40)
CRT_BEZEL         = ( 72, 110, 108)

# Flat monitor
FLAT_MON_BODY     = (110, 108, 102)
FLAT_MON_SCREEN   = ( 24,  28,  36)
FLAT_MON_STAND    = ( 88,  84,  78)

# Monitor glow (blue-white, real-world — not Glitch cyan)
# Sam's brief: monitor glow ambient = RGB(184,200,212), R:184 keeps warm presence
MON_GLOW_BRIGHT   = (200, 218, 240)
MON_GLOW_MID      = (180, 200, 210)   # exact from Sam's brief for spill
MON_GLOW_SOFT     = (170, 188, 205)

# Oscilloscope
OSCOPE_BODY       = ( 72,  74,  68)
OSCOPE_SCREEN     = ( 18,  28,  18)
OSCOPE_KNOBS      = ( 98,  88,  68)

# Breadboards and components
BREADBOARD        = (220, 210, 185)
BREADBOARD_LINES  = (190, 178, 150)
COMPONENT_RED     = (185,  62,  42)
COMPONENT_ORANGE  = (200, 120,  50)
COMPONENT_BLUE    = (100, 128, 168)
SOLDER_SILVER     = (180, 180, 168)
WIRE_COPPER       = (168, 112,  52)

# Shelving
SHELF_WOOD        = (148, 108,  62)
SHELF_BRACKET     = ( 90,  75,  58)
VINTAGE_PC_BEIGE  = (215, 205, 185)
VINTAGE_PC_SHADOW = (175, 162, 140)
VINTAGE_PC_VENT   = (160, 148, 125)
CART_YELLOW       = (210, 178,  68)
CART_RED          = (188,  72,  52)
CART_GREY         = (165, 162, 155)
CART_BLUE         = (100, 130, 162)
BIN_PLASTIC       = (195, 185, 165)
BIN_LABEL         = (240, 232, 210)

# Wall papers
PAPER_WHITE       = (242, 238, 225)
PAPER_YELLOW      = (235, 218, 148)
CIRCUIT_DIAG_BG   = (228, 220, 195)
INK_LINE          = ( 58,  48,  38)
PUSHPIN_RED       = (188,  58,  42)

# Bed
BED_FRAME         = (105,  78,  48)
MATTRESS          = (215, 205, 188)
DUVET_BLUE        = (152, 162, 185)
PILLOW_CREAM      = (232, 224, 205)
# Additional bedding
BEDDING_MUTED     = (168, 172, 185)   # muted cool bedding fold
BLANKET_GREY      = (175, 168, 155)   # extra blanket on bed

# Chair
CHAIR_FABRIC      = (178, 168, 148)
CHAIR_FRAME       = ( 75,  62,  48)

# Cosmo's jacket (RW-08 Dusty Lavender) — spec: approx RGB 160,150,175
JACKET_LAV        = (160, 150, 175)   # RW-08 per Takeshi / task spec
JACKET_SHADOW     = (120, 110, 145)
JACKET_HIGHLIGHT  = (188, 178, 200)

# Soldering kit
SOLDER_IRON_TIP   = (190, 165, 100)
SOLDER_IRON_BODY  = (100,  90,  80)
SOLDER_WIRE_SPOOL = (195, 170, 100)

# Poster / printout colors for wall above bed
POSTER_BLUE       = (120, 148, 185)
POSTER_GREEN      = (130, 158, 128)
PRINTOUT_CREAM    = (230, 222, 200)
PRINTOUT_WARM     = (225, 205, 170)
CIRCUIT_BG        = (210, 200, 180)

# Line / shadow
LINE_DARK         = ( 59,  40,  32)
SHADOW_COOL       = (168, 155, 191)
SHADOW_WARM       = (180, 148, 100)

# Monitor glow spill color (on surrounding surfaces)
MON_SPILL         = (180, 200, 210)   # RGB(180,200,210), alpha 40-60

# Dust mote color (warm white)
DUST_MOTE         = (255, 248, 230)

# ── Helper functions ──────────────────────────────────────────────────────────
rng = random.Random(42)

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))

def draw_rect(draw, x0, y0, x1, y1, fill, outline=None, width=1):
    draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)

def draw_line_seg(draw, pts, fill, width=1):
    if len(pts) >= 2:
        draw.line(pts, fill=fill, width=width)

def gradient_rect_v(img, x0, y0, x1, y1, col_top, col_bot):
    if x1 <= x0 or y1 <= y0:
        return
    w_ = x1 - x0
    h_ = y1 - y0
    layer = Image.new("RGBA", (w_, h_), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for row in range(h_):
        t = row / max(h_ - 1, 1)
        c = lerp_color(col_top, col_bot, t)
        ld.line([(0, row), (w_ - 1, row)], fill=c + (255,), width=1)
    img.alpha_composite(layer, dest=(x0, y0))

def gradient_rect_h(img, x0, y0, x1, y1, col_left, col_right):
    if x1 <= x0 or y1 <= y0:
        return
    w_ = x1 - x0
    h_ = y1 - y0
    layer = Image.new("RGBA", (w_, h_), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for col in range(w_):
        t = col / max(w_ - 1, 1)
        c = lerp_color(col_left, col_right, t)
        ld.line([(col, 0), (col, h_ - 1)], fill=c + (255,), width=1)
    img.alpha_composite(layer, dest=(x0, y0))

def soft_glow_overlay(img, cx, cy, rx, ry, color, max_alpha=80):
    """Soft elliptical glow overlay."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    steps = 12
    for i in range(steps, 0, -1):
        t = i / steps
        a = int(max_alpha * (1 - t) * 2.0)
        a = min(max_alpha, a)
        sx = int(rx * t)
        sy = int(ry * t)
        c = color + (a,)
        ld = ImageDraw.Draw(layer)
        ld.ellipse([cx - sx, cy - sy, cx + sx, cy + sy], fill=c)
    img.alpha_composite(layer)


def draw_light_shaft(img, shaft_pts, shaft_color, alpha_peak=110):
    """
    Draw a trapezoid light shaft with feathered (soft) edges.
    Uses multiple passes with decreasing alpha for the feather effect.
    """
    # Draw solid core at ~60% of peak alpha
    core_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(core_layer)
    cd.polygon(shaft_pts, fill=shaft_color + (int(alpha_peak * 0.60),))
    img.alpha_composite(core_layer)

    # Feather by blurring an alpha mask
    feather_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    fd = ImageDraw.Draw(feather_layer)
    fd.polygon(shaft_pts, fill=shaft_color + (int(alpha_peak * 0.45),))
    feather_blurred = feather_layer.filter(ImageFilter.GaussianBlur(radius=18))
    img.alpha_composite(feather_blurred)


def draw_dust_motes(img, shaft_pts, n=15, seed=99):
    """
    Draw ~n small dust mote circles within the bounding box of shaft_pts.
    Alpha 60–80, warm white color.
    """
    r = random.Random(seed)
    # Compute axis-aligned bounding box of shaft
    xs = [p[0] for p in shaft_pts]
    ys = [p[1] for p in shaft_pts]
    bx0, bx1 = min(xs), max(xs)
    by0, by1 = min(ys), max(ys)

    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)

    drawn = 0
    attempts = 0
    while drawn < n and attempts < n * 8:
        attempts += 1
        mx = r.randint(bx0, bx1)
        my = r.randint(by0, by1)
        # Simple point-in-polygon test using winding
        # For the shaft trapezoid (4 points) we use the bounding box + linear edge test
        # Actually use a simple linear interpolation test for trapezoid inclusion
        if _point_in_quad(mx, my, shaft_pts):
            rad = r.randint(2, 5)
            alpha = r.randint(60, 80)
            ld.ellipse([mx - rad, my - rad, mx + rad, my + rad],
                       fill=DUST_MOTE + (alpha,))
            drawn += 1

    img.alpha_composite(layer)


def _point_in_quad(px, py, pts):
    """Simple point-in-polygon for a convex quad (4 points)."""
    n = len(pts)
    inside = True
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        # Cross product sign check
        cross = (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)
        if cross < 0:
            inside = False
            break
    return inside


# ── Main draw function ────────────────────────────────────────────────────────

def draw_tech_den():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # ── PERSPECTIVE SETUP ─────────────────────────────────────────────────────
    VP_X = 820
    VP_Y = 295

    FLOOR_Y_FAR  = 340
    FLOOR_Y_NEAR = H
    CEIL_Y_FAR   = 210
    CEIL_Y_NEAR  = -20

    BACK_WALL_LEFT  = 60
    BACK_WALL_RIGHT = 840

    # ── BASE LAYERS ───────────────────────────────────────────────────────────

    # 1. Back wall — warm cream, gradient left (sunlit) to right (cooler)
    gradient_rect_h(img, 0, CEIL_Y_FAR, BACK_WALL_RIGHT, FLOOR_Y_FAR,
                    WALL_WINDOW_LIGHT, WALL_SHADOW)
    draw = ImageDraw.Draw(img)

    # Right side wall
    right_wall_pts = [
        (BACK_WALL_RIGHT, CEIL_Y_FAR),
        (W, CEIL_Y_NEAR),
        (W, H),
        (BACK_WALL_RIGHT, FLOOR_Y_FAR),
    ]
    draw.polygon(right_wall_pts, fill=WALL_SHADOW)

    # Ceiling
    ceil_pts = [
        (0, 0),
        (W, 0),
        (W, CEIL_Y_NEAR),
        (BACK_WALL_RIGHT, CEIL_Y_FAR),
        (0, CEIL_Y_FAR),
    ]
    draw.polygon(ceil_pts, fill=CEILING)
    draw = ImageDraw.Draw(img)

    # Floor
    floor_pts = [
        (0, FLOOR_Y_FAR),
        (BACK_WALL_RIGHT, FLOOR_Y_FAR),
        (W, H),
        (0, H),
    ]
    draw.polygon(floor_pts, fill=FLOOR_WOOD)

    # Floor plank lines
    n_planks = 14
    for i in range(n_planks):
        t = i / n_planks
        ly = int(FLOOR_Y_FAR + t * (H - FLOOR_Y_FAR))
        draw.line([(0, ly), (W, ly)], fill=FLOOR_WOOD_DARK, width=1)

    for i in range(8):
        t = i / 7
        fx = int(t * W)
        draw.line([(fx, FLOOR_Y_FAR), (fx, H)], fill=FLOOR_WOOD_DARK, width=1)

    draw_rect(draw, 0, FLOOR_Y_FAR + 30, 500, H, FLOOR_WORN)
    draw = ImageDraw.Draw(img)

    # Skirting board
    draw_rect(draw, 0, FLOOR_Y_FAR - 14, BACK_WALL_RIGHT, FLOOR_Y_FAR, SKIRTING)

    # ── LEFT WINDOW ───────────────────────────────────────────────────────────
    WIN_X0 = 0
    WIN_X1 = 115
    WIN_Y0 = CEIL_Y_FAR + 35
    WIN_Y1 = FLOOR_Y_FAR - 18

    # Window reveal / jamb
    left_wall_win_pts = [
        (0, CEIL_Y_FAR),
        (WIN_X1, CEIL_Y_FAR + 10),
        (WIN_X1, FLOOR_Y_FAR - 5),
        (0, FLOOR_Y_FAR),
    ]
    draw.polygon(left_wall_win_pts, fill=WALL_WARM)

    # Window frame
    draw_rect(draw, WIN_X0, WIN_Y0, WIN_X1, WIN_Y1, WINDOW_FRAME)
    draw_rect(draw, WIN_X0 + 8, WIN_Y0 + 8, WIN_X1 - 4, WIN_Y1 - 8, WINDOW_SKY)
    mid_y = (WIN_Y0 + WIN_Y1) // 2
    draw_rect(draw, WIN_X0, mid_y - 3, WIN_X1, mid_y + 3, WINDOW_FRAME)

    # Outer glow on wall around window
    draw = ImageDraw.Draw(img)
    soft_glow_overlay(img, WIN_X1 + 30, (WIN_Y0 + WIN_Y1) // 2, 160, 120,
                      SUNLIGHT_GOLD, max_alpha=55)
    draw = ImageDraw.Draw(img)

    # ── WINDOW LIGHT SHAFT (Fix 1) ────────────────────────────────────────────
    # Trapezoid shaft falling from window across floor and desk surface.
    # Near edge (bottom) is wider; far edge (near window) is narrower.
    # Shaft begins at window mid-height, fans out to the right and down onto floor.
    SHAFT_TOP_LEFT  = (WIN_X0,       mid_y - 40)   # window left edge, upper
    SHAFT_TOP_RIGHT = (WIN_X1 + 10,  mid_y - 60)   # window right reveal, upper
    SHAFT_BOT_RIGHT = (WIN_X1 + 320, FLOOR_Y_FAR + 110)  # far beam edge on floor/desk
    SHAFT_BOT_LEFT  = (WIN_X0,       FLOOR_Y_FAR + 140)  # near beam edge left

    shaft_pts = [SHAFT_TOP_LEFT, SHAFT_TOP_RIGHT, SHAFT_BOT_RIGHT, SHAFT_BOT_LEFT]

    draw_light_shaft(img, shaft_pts, SUNLIT_AMBER, alpha_peak=115)
    draw = ImageDraw.Draw(img)

    # Dust motes inside beam
    draw_dust_motes(img, shaft_pts, n=15, seed=77)
    draw = ImageDraw.Draw(img)

    # ── BACK WALL DETAILS ─────────────────────────────────────────────────────
    papers = [
        (120, 228, 200, 295, PAPER_WHITE),
        (335, 235, 430, 295, CIRCUIT_DIAG_BG),
        (455, 240, 530, 290, PAPER_WHITE),
        (150, 300, 260, 350, PAPER_YELLOW),
    ]
    for (px0, py0, px1, py1, pcol) in papers:
        draw_rect(draw, px0, py0, px1, py1, pcol, outline=LINE_DARK, width=1)
        draw.ellipse([px0 + 5, py0 - 4, px0 + 12, py0 + 3], fill=PUSHPIN_RED)

    for row in range(6):
        lx = 125
        ly = 240 + row * 8
        draw.line([(lx, ly), (lx + rng.randint(40, 70), ly)],
                  fill=INK_LINE, width=1)

    cx0, cy0 = 340, 240
    circuit_pts = [
        (cx0 + 10, cy0 + 10), (cx0 + 30, cy0 + 10),
        (cx0 + 30, cy0 + 20), (cx0 + 60, cy0 + 20),
        (cx0 + 60, cy0 + 35), (cx0 + 20, cy0 + 35),
        (cx0 + 20, cy0 + 50),
    ]
    draw.line(circuit_pts, fill=INK_LINE, width=1)
    draw_rect(draw, cx0 + 35, cy0 + 15, cx0 + 50, cy0 + 25, PAPER_WHITE,
              outline=INK_LINE, width=1)

    # ── SHELVING ON BACK WALL ─────────────────────────────────────────────────
    SHELF_Y1 = 248
    SHELF_Y2 = 310

    draw_rect(draw, 540, 200, BACK_WALL_RIGHT + 10, SHELF_Y1, SHELF_WOOD)
    draw_rect(draw, 540, 260, BACK_WALL_RIGHT + 10, SHELF_Y2, SHELF_WOOD)

    draw_rect(draw, 580, CEIL_Y_FAR + 15, 598, SHELF_Y2, SHELF_BRACKET)
    draw_rect(draw, 720, CEIL_Y_FAR + 15, 738, SHELF_Y2, SHELF_BRACKET)

    pc_positions = [(545, CEIL_Y_FAR + 16, 620, SHELF_Y1 - 2),
                    (625, CEIL_Y_FAR + 22, 690, SHELF_Y1 - 2)]
    for (bx0, by0, bx1, by1) in pc_positions:
        draw_rect(draw, bx0, by0, bx1, by1, VINTAGE_PC_BEIGE, outline=LINE_DARK, width=1)
        draw_rect(draw, bx1 - 8, by0, bx1, by1, VINTAGE_PC_SHADOW)
        for vi in range(3):
            vy = by0 + 8 + vi * 5
            draw.line([(bx0 + 4, vy), (bx0 + 16, vy)], fill=VINTAGE_PC_VENT, width=1)
        drive_y = (by0 + by1) // 2
        draw_rect(draw, bx0 + 5, drive_y - 2, bx0 + 22, drive_y + 2,
                  VINTAGE_PC_VENT)

    cart_colors = [CART_YELLOW, CART_RED, CART_GREY, CART_BLUE, CART_YELLOW,
                   CART_RED, CART_GREY]
    for i, cc in enumerate(cart_colors):
        cx_ = 548 + i * 30
        draw_rect(draw, cx_, SHELF_Y1 + 4, cx_ + 22, SHELF_Y2 - 4,
                  cc, outline=LINE_DARK, width=1)

    for bi in range(3):
        bx_ = 700 + bi * 42
        draw_rect(draw, bx_, SHELF_Y1 + 4, bx_ + 36, SHELF_Y2 - 3,
                  BIN_PLASTIC, outline=LINE_DARK, width=1)
        draw_rect(draw, bx_ + 3, SHELF_Y1 + 8, bx_ + 33, SHELF_Y1 + 18,
                  BIN_LABEL)

    # ── DESK (left to center, dominant) ───────────────────────────────────────
    DESK_TOP_Y    = 395
    DESK_LEFT     = 0
    DESK_RIGHT    = 720
    DESK_FRONT_Y  = H - 80
    DESK_DEPTH    = 80

    desk_top_pts = [
        (DESK_LEFT, DESK_TOP_Y),
        (DESK_RIGHT, DESK_TOP_Y),
        (DESK_RIGHT - 40, DESK_TOP_Y - DESK_DEPTH),
        (DESK_LEFT, DESK_TOP_Y - DESK_DEPTH),
    ]
    draw.polygon(desk_top_pts, fill=DESK_WOOD_TOP)
    draw_rect(draw, DESK_LEFT, DESK_TOP_Y, DESK_RIGHT, DESK_FRONT_Y, DESK_WOOD_SHADOW)
    draw.line([(DESK_LEFT, DESK_TOP_Y), (DESK_RIGHT, DESK_TOP_Y)],
              fill=lerp_color(DESK_WOOD_TOP, (255, 255, 200), 0.3), width=2)

    leg_positions = [(35, DESK_TOP_Y, 55, H),
                     (640, DESK_TOP_Y, 660, H)]
    for (lx0, ly0, lx1, ly1) in leg_positions:
        draw_rect(draw, lx0, ly0, lx1, ly1, DESK_FRAME)

    # ── CABLES ON DESK ────────────────────────────────────────────────────────
    rng2 = random.Random(17)
    for _ in range(14):
        sx = rng2.randint(80, 600)
        sy = DESK_TOP_Y - rng2.randint(5, 40)
        ex = sx + rng2.randint(-80, 80)
        ey = sy + rng2.randint(10, 50)
        mid_x = (sx + ex) // 2 + rng2.randint(-20, 20)
        mid_y = max(sy, ey) + rng2.randint(5, 25)
        col = rng2.choice([CABLE_DARK, CABLE_MED, CABLE_GREY])
        draw.line([(sx, sy), (mid_x, mid_y), (ex, ey)], fill=col, width=2)

    # ── CRT MONITORS ──────────────────────────────────────────────────────────
    def draw_crt(draw, img, cx, cy, w_=160, h_=130):
        body_pts = [
            (cx - w_ // 2 - 18, cy - h_ // 2 + 20),
            (cx + w_ // 2 + 18, cy - h_ // 2 + 20),
            (cx + w_ // 2 + 25, cy + h_ // 2 + 25),
            (cx - w_ // 2 - 25, cy + h_ // 2 + 25),
        ]
        draw.polygon(body_pts, fill=CRT_CASING)
        draw.polygon([
            (cx + w_ // 2 + 5, cy - h_ // 2 + 20),
            (cx + w_ // 2 + 18, cy - h_ // 2 + 20),
            (cx + w_ // 2 + 25, cy + h_ // 2 + 25),
            (cx + w_ // 2 + 5, cy + h_ // 2 + 25),
        ], fill=CRT_SHADOW)
        draw_rect(draw, cx - w_ // 2, cy - h_ // 2, cx + w_ // 2, cy + h_ // 2,
                  CRT_BEZEL)
        sw = w_ - 16
        sh = h_ - 14
        draw_rect(draw, cx - sw // 2, cy - sh // 2, cx + sw // 2, cy + sh // 2,
                  CRT_SCREEN_OFF)
        # Screen glow — active monitor light (blue-white, real-world safe)
        glow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow_layer)
        gd.ellipse([cx - sw // 2 - 2, cy - sh // 2 - 2,
                    cx + sw // 2 + 2, cy + sh // 2 + 2],
                   fill=MON_GLOW_BRIGHT + (190,))
        img.alpha_composite(glow_layer)
        draw = ImageDraw.Draw(img)
        # Screen reflection glint
        draw.line([(cx - sw // 2 + 5, cy - sh // 2 + 5),
                   (cx - sw // 2 + 20, cy - sh // 2 + 5)],
                  fill=(230, 240, 255), width=2)
        # Base/stand
        draw_rect(draw, cx - 18, cy + h_ // 2, cx + 18, cy + h_ // 2 + 18,
                  CRT_SHADOW)
        draw_rect(draw, cx - 28, cy + h_ // 2 + 14, cx + 28, cy + h_ // 2 + 22,
                  CRT_CASING)
        return draw

    CRT1_CX, CRT1_CY = 195, DESK_TOP_Y - 88
    draw = draw_crt(draw, img, CRT1_CX, CRT1_CY, w_=175, h_=140)

    CRT2_CX, CRT2_CY = 420, DESK_TOP_Y - 75
    draw = draw_crt(draw, img, CRT2_CX, CRT2_CY, w_=150, h_=120)

    # ── FLAT PANEL MONITOR ────────────────────────────────────────────────────
    FP_X0, FP_Y0 = 580, DESK_TOP_Y - 130
    FP_X1, FP_Y1 = 690, DESK_TOP_Y - 18
    draw_rect(draw, FP_X0, FP_Y0, FP_X1, FP_Y1, FLAT_MON_BODY, outline=LINE_DARK, width=1)
    draw_rect(draw, FP_X0 + 5, FP_Y0 + 5, FP_X1 - 5, FP_Y1 - 8, FLAT_MON_SCREEN)
    fp_cx = (FP_X0 + FP_X1) // 2
    draw_rect(draw, fp_cx - 8, FP_Y1, fp_cx + 8, FP_Y1 + 15, FLAT_MON_STAND)
    draw_rect(draw, fp_cx - 18, FP_Y1 + 12, fp_cx + 18, FP_Y1 + 18, FLAT_MON_STAND)
    soft_glow_overlay(img, fp_cx, (FP_Y0 + FP_Y1) // 2, 80, 70,
                      MON_GLOW_MID, max_alpha=60)
    draw = ImageDraw.Draw(img)

    # ── OSCILLOSCOPE ──────────────────────────────────────────────────────────
    OSC_X0, OSC_Y0 = 60, DESK_TOP_Y - 80
    OSC_X1, OSC_Y1 = 160, DESK_TOP_Y - 5
    draw_rect(draw, OSC_X0, OSC_Y0, OSC_X1, OSC_Y1, OSCOPE_BODY, outline=LINE_DARK, width=1)
    draw_rect(draw, OSC_X0 + 6, OSC_Y0 + 6, OSC_X0 + 52, OSC_Y1 - 8, OSCOPE_SCREEN)
    TRACE_GREEN = (58, 120, 48)
    trace_pts = []
    for xi in range(0, 46, 3):
        tx = OSC_X0 + 9 + xi
        ty = OSC_Y0 + 25 + int(10 * math.sin(xi * 0.4))
        trace_pts.append((tx, ty))
    if len(trace_pts) >= 2:
        draw.line(trace_pts, fill=TRACE_GREEN, width=1)
    for ki in range(4):
        kx = OSC_X0 + 62 + ki * 22
        ky = OSC_Y0 + 20
        draw.ellipse([kx - 6, ky - 6, kx + 6, ky + 6], fill=OSCOPE_KNOBS,
                     outline=LINE_DARK, width=1)
    for ki in range(3):
        kx = OSC_X0 + 62 + ki * 25
        ky = OSC_Y0 + 48
        draw.ellipse([kx - 5, ky - 5, kx + 5, ky + 5], fill=OSCOPE_KNOBS,
                     outline=LINE_DARK, width=1)

    # ── BREADBOARDS ON DESK ───────────────────────────────────────────────────
    BB_X0, BB_Y0 = 62, DESK_TOP_Y - 4
    BB_X1, BB_Y1 = 145, DESK_TOP_Y + 18
    draw_rect(draw, BB_X0, BB_Y0, BB_X1, BB_Y1, BREADBOARD)
    for gi in range(0, BB_X1 - BB_X0, 6):
        draw.line([(BB_X0 + gi, BB_Y0), (BB_X0 + gi, BB_Y1)],
                  fill=BREADBOARD_LINES, width=1)
    draw.rectangle([BB_X0 + 12, BB_Y0 + 4, BB_X0 + 22, BB_Y0 + 8],
                   fill=COMPONENT_RED)
    draw.ellipse([BB_X0 + 32, BB_Y0 + 3, BB_X0 + 42, BB_Y0 + 11],
                 fill=COMPONENT_ORANGE)
    draw.line([(BB_X0 + 48, BB_Y0 + 2), (BB_X0 + 48, BB_Y0 + 14)],
              fill=WIRE_COPPER, width=1)
    draw.line([(BB_X0 + 58, BB_Y0 + 2), (BB_X0 + 58, BB_Y0 + 14)],
              fill=WIRE_COPPER, width=1)

    BB2_X0, BB2_Y0 = 240, DESK_TOP_Y - 8
    BB2_X1, BB2_Y1 = 330, DESK_TOP_Y + 14
    draw_rect(draw, BB2_X0, BB2_Y0, BB2_X1, BB2_Y1, BREADBOARD)
    for gi in range(0, BB2_X1 - BB2_X0, 6):
        draw.line([(BB2_X0 + gi, BB2_Y0), (BB2_X0 + gi, BB2_Y1)],
                  fill=BREADBOARD_LINES, width=1)
    draw.rectangle([BB2_X0 + 8, BB2_Y0 + 3, BB2_X0 + 18, BB2_Y0 + 7],
                   fill=COMPONENT_BLUE)

    # ── SOLDERING KIT ─────────────────────────────────────────────────────────
    SOL_X = 525
    SOL_Y = DESK_TOP_Y + 5
    draw_rect(draw, SOL_X, SOL_Y - 8, SOL_X + 50, SOL_Y, SOLDER_IRON_BODY)
    draw.polygon([(SOL_X + 50, SOL_Y - 8), (SOL_X + 50, SOL_Y),
                  (SOL_X + 68, SOL_Y - 4)], fill=SOLDER_IRON_TIP)
    draw.ellipse([SOL_X - 28, SOL_Y - 14, SOL_X - 4, SOL_Y + 5],
                 fill=SOLDER_WIRE_SPOOL, outline=LINE_DARK, width=1)
    draw.ellipse([SOL_X - 22, SOL_Y - 10, SOL_X - 10, SOL_Y + 1],
                 fill=CABLE_DARK)

    # ── DESK CHAIR ────────────────────────────────────────────────────────────
    CH_CX = 660
    CH_SEAT_Y = DESK_TOP_Y + 50

    # Seat
    draw.ellipse([CH_CX - 55, CH_SEAT_Y - 15, CH_CX + 55, CH_SEAT_Y + 20],
                 fill=CHAIR_FABRIC)
    # Chair back
    draw_rect(draw, CH_CX - 38, CH_SEAT_Y - 80, CH_CX + 38, CH_SEAT_Y - 15,
              CHAIR_FABRIC, outline=LINE_DARK, width=1)

    # ── COSMO'S JACKET ON CHAIR (Fix 4) ──────────────────────────────────────
    # Dusty lavender jacket draped prominently over chair back.
    # Use RW-08 spec: RGB(160,150,175). Draw as distinct layered polygon shape.
    # Main jacket body draped over the chair back — wider, clearly lavender
    jacket_pts = [
        (CH_CX - 52, CH_SEAT_Y - 85),   # top-left shoulder
        (CH_CX + 50, CH_SEAT_Y - 85),   # top-right shoulder
        (CH_CX + 58, CH_SEAT_Y - 20),   # right hem
        (CH_CX + 42, CH_SEAT_Y + 18),   # right tail draping down
        (CH_CX - 44, CH_SEAT_Y + 18),   # left tail draping down
        (CH_CX - 60, CH_SEAT_Y - 20),   # left hem
    ]
    jacket_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    jd = ImageDraw.Draw(jacket_layer)
    jd.polygon(jacket_pts, fill=JACKET_LAV + (255,))
    img.alpha_composite(jacket_layer)
    draw = ImageDraw.Draw(img)

    # Shadow side (right half of jacket — away from window)
    jacket_shadow_pts = [
        (CH_CX + 10, CH_SEAT_Y - 85),
        (CH_CX + 50, CH_SEAT_Y - 85),
        (CH_CX + 58, CH_SEAT_Y - 20),
        (CH_CX + 42, CH_SEAT_Y + 18),
        (CH_CX + 10, CH_SEAT_Y + 18),
    ]
    shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_layer)
    sd.polygon(jacket_shadow_pts, fill=JACKET_SHADOW + (120,))
    img.alpha_composite(shadow_layer)
    draw = ImageDraw.Draw(img)

    # Jacket collar detail (darker notch at top center)
    draw.polygon([
        (CH_CX - 10, CH_SEAT_Y - 85),
        (CH_CX + 10, CH_SEAT_Y - 85),
        (CH_CX + 6, CH_SEAT_Y - 68),
        (CH_CX - 6, CH_SEAT_Y - 68),
    ], fill=JACKET_SHADOW)

    # Jacket outline
    draw.polygon(jacket_pts, outline=LINE_DARK, fill=None)

    # Chair post / base
    draw_rect(draw, CH_CX - 5, CH_SEAT_Y + 18, CH_CX + 5, CH_SEAT_Y + 55,
              CHAIR_FRAME)
    draw.line([(CH_CX - 35, CH_SEAT_Y + 55), (CH_CX + 35, CH_SEAT_Y + 55)],
              fill=CHAIR_FRAME, width=4)
    draw.line([(CH_CX, CH_SEAT_Y + 45), (CH_CX, CH_SEAT_Y + 65)],
              fill=CHAIR_FRAME, width=4)

    # ── BED AREA — RIGHT HALF COMPLETION (Fix 3) ──────────────────────────────
    BED_X0 = 740
    BED_Y0 = 310
    BED_X1 = W - 10
    BED_Y1 = H - 60

    # Bed frame
    draw_rect(draw, BED_X0, BED_Y0, BED_X1, BED_Y1, BED_FRAME)

    # Headboard (prominent, wood-grain feel)
    draw_rect(draw, BED_X0, BED_Y0 - 60, BED_X1, BED_Y0 + 22, BED_FRAME)
    draw_rect(draw, BED_X0 + 5, BED_Y0 - 55, BED_X1 - 5, BED_Y0 + 16, MATTRESS)

    # Mattress base
    draw_rect(draw, BED_X0 + 8, BED_Y0 + 16, BED_X1 - 5, BED_Y1 - 8, MATTRESS)

    # Bedding polygon — rumpled duvet (not flat rectangle, polygon shape)
    duvet_pts = [
        (BED_X0 + 10, BED_Y0 + 20),   # top-left corner
        (BED_X1 - 8,  BED_Y0 + 17),   # top-right corner
        (BED_X1 - 6,  BED_Y0 + 145),  # right side
        (BED_X0 + 60, BED_Y0 + 152),  # lower right of duvet
        (BED_X0 + 10, BED_Y0 + 148),  # lower left
    ]
    draw.polygon(duvet_pts, fill=DUVET_BLUE, outline=LINE_DARK)
    draw = ImageDraw.Draw(img)

    # Duvet folds/creases (lived-in)
    draw.line([(BED_X0 + 22, BED_Y0 + 62), (BED_X1 - 20, BED_Y0 + 57)],
              fill=lerp_color(DUVET_BLUE, LINE_DARK, 0.3), width=2)
    draw.line([(BED_X0 + 35, BED_Y0 + 95), (BED_X1 - 30, BED_Y0 + 90)],
              fill=lerp_color(DUVET_BLUE, LINE_DARK, 0.2), width=1)
    draw.line([(BED_X0 + 15, BED_Y0 + 130), (BED_X0 + 220, BED_Y0 + 125)],
              fill=lerp_color(DUVET_BLUE, LINE_DARK, 0.25), width=1)

    # Pillow shapes (two pillows visible)
    draw_rect(draw, BED_X0 + 10, BED_Y0 + 20, BED_X0 + 188, BED_Y0 + 72,
              PILLOW_CREAM, outline=LINE_DARK, width=1)
    draw_rect(draw, BED_X0 + 196, BED_Y0 + 18, BED_X0 + 380, BED_Y0 + 70,
              PILLOW_CREAM, outline=LINE_DARK, width=1)
    # Pillow stitching / edge
    draw.line([(BED_X0 + 20, BED_Y0 + 30), (BED_X0 + 178, BED_Y0 + 28)],
              fill=lerp_color(PILLOW_CREAM, LINE_DARK, 0.2), width=1)

    # Blanket fold at foot of bed (slightly off to one side — casually kicked)
    blanket_pts = [
        (BED_X0 + 10, BED_Y0 + 145),
        (BED_X0 + 200, BED_Y0 + 140),
        (BED_X0 + 180, BED_Y1 - 15),
        (BED_X0 + 10,  BED_Y1 - 12),
    ]
    draw.polygon(blanket_pts, fill=BEDDING_MUTED, outline=LINE_DARK)
    draw = ImageDraw.Draw(img)

    # Device/tablet on mattress edge (Fix 3 — "device or book on mattress edge")
    # A handheld device/book lying flat at the edge of the bed
    DEVICE_X0 = BED_X0 + 220
    DEVICE_Y0 = BED_Y0 + 152
    DEVICE_X1 = DEVICE_X0 + 80
    DEVICE_Y1 = DEVICE_Y0 + 52
    # Device body
    draw_rect(draw, DEVICE_X0, DEVICE_Y0, DEVICE_X1, DEVICE_Y1,
              (88, 82, 76), outline=LINE_DARK, width=1)
    # Screen
    draw_rect(draw, DEVICE_X0 + 4, DEVICE_Y0 + 4, DEVICE_X1 - 4, DEVICE_Y1 - 6,
              (42, 48, 58))
    # Faint screen glow
    dev_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    devd = ImageDraw.Draw(dev_layer)
    devd.rectangle([DEVICE_X0 + 4, DEVICE_Y0 + 4, DEVICE_X1 - 4, DEVICE_Y1 - 6],
                   fill=MON_GLOW_SOFT + (40,))
    img.alpha_composite(dev_layer)
    draw = ImageDraw.Draw(img)

    # ── WALL ABOVE BED — POSTERS / PRINTOUTS (Fix 3) ─────────────────────────
    # Wall above bed headboard: one poster + 2 taped printouts
    WALL_BED_Y_TOP = CEIL_Y_FAR  # top of wall in this zone
    WALL_BED_Y_BOT = BED_Y0 - 60  # top of headboard

    # Larger poster (left side, code-inspired blue circuit diagram look)
    POST_X0 = BED_X0 + 15
    POST_Y0 = WALL_BED_Y_TOP + 25
    POST_X1 = BED_X0 + 155
    POST_Y1 = POST_Y0 + 95
    draw_rect(draw, POST_X0, POST_Y0, POST_X1, POST_Y1, POSTER_BLUE,
              outline=LINE_DARK, width=2)
    # Poster content: circuit diagram lines
    for row in range(5):
        py = POST_Y0 + 12 + row * 14
        draw.line([(POST_X0 + 8, py), (POST_X1 - 8, py)],
                  fill=lerp_color(POSTER_BLUE, (240, 240, 255), 0.6), width=1)
    # A few vertical connector lines on poster
    for col_idx in range(3):
        px = POST_X0 + 20 + col_idx * 38
        draw.line([(px, POST_Y0 + 12), (px, POST_Y1 - 10)],
                  fill=lerp_color(POSTER_BLUE, (240, 240, 255), 0.5), width=1)
    # Tape marks (corner tape)
    draw_rect(draw, POST_X0 - 3, POST_Y0 - 4, POST_X0 + 12, POST_Y0 + 4,
              (220, 215, 195))
    draw_rect(draw, POST_X1 - 12, POST_Y0 - 4, POST_X1 + 3, POST_Y0 + 4,
              (220, 215, 195))

    # Printout 1 — code printout (cream/warm white)
    PRINT1_X0 = BED_X0 + 175
    PRINT1_Y0 = WALL_BED_Y_TOP + 20
    PRINT1_X1 = PRINT1_X0 + 100
    PRINT1_Y1 = PRINT1_Y0 + 72
    draw_rect(draw, PRINT1_X0, PRINT1_Y0, PRINT1_X1, PRINT1_Y1, PRINTOUT_CREAM,
              outline=(180, 170, 150), width=1)
    # Code lines on printout
    rng3 = random.Random(55)
    for row in range(8):
        lx0 = PRINT1_X0 + 5
        ly  = PRINT1_Y0 + 8 + row * 7
        lx1 = lx0 + rng3.randint(30, 88)
        draw.line([(lx0, ly), (lx1, ly)], fill=INK_LINE + (180,), width=1)
    # Tape mark on top
    draw_rect(draw, PRINT1_X0 + 30, PRINT1_Y0 - 4, PRINT1_X0 + 70, PRINT1_Y0 + 4,
              (220, 215, 195))

    # Printout 2 — schematic / hand-drawn component layout (warmer cream)
    PRINT2_X0 = PRINT1_X0 + 8
    PRINT2_Y0 = PRINT1_Y1 + 8
    PRINT2_X1 = PRINT2_X0 + 88
    PRINT2_Y1 = PRINT2_Y0 + 58
    draw_rect(draw, PRINT2_X0, PRINT2_Y0, PRINT2_X1, PRINT2_Y1, PRINTOUT_WARM,
              outline=(180, 165, 140), width=1)
    # Hand-drawn look: a few irregular schematic shapes
    sch_pts = [
        (PRINT2_X0 + 8, PRINT2_Y0 + 15),
        (PRINT2_X0 + 25, PRINT2_Y0 + 15),
        (PRINT2_X0 + 25, PRINT2_Y0 + 30),
        (PRINT2_X0 + 50, PRINT2_Y0 + 30),
        (PRINT2_X0 + 50, PRINT2_Y0 + 45),
    ]
    draw.line(sch_pts, fill=INK_LINE, width=1)
    draw_rect(draw, PRINT2_X0 + 32, PRINT2_Y0 + 24, PRINT2_X0 + 46, PRINT2_Y0 + 36,
              PRINTOUT_WARM, outline=INK_LINE, width=1)
    draw.ellipse([PRINT2_X0 + 55, PRINT2_Y0 + 18, PRINT2_X0 + 72, PRINT2_Y0 + 34],
                 outline=INK_LINE)
    # Pin / tape mark
    draw.ellipse([PRINT2_X0 + 40, PRINT2_Y0 - 4, PRINT2_X0 + 50, PRINT2_Y0 + 4],
                 fill=(220, 215, 195))

    # ── MONITOR GLOW AMBIENT LIGHT (Fix 2 — spill onto surfaces) ─────────────
    # The monitors (CRT1, CRT2, flat panel) face roughly forward/right.
    # Spill falls onto: chair back/seat, desk surface in front of monitors,
    # nearest shelving face (right side of shelves at ~540–840 x).

    # 1. Wide soft glow from monitors onto wall + ceiling above desk
    soft_glow_overlay(img, 350, DESK_TOP_Y - 100, 350, 200,
                      MON_GLOW_SOFT, max_alpha=50)
    draw = ImageDraw.Draw(img)

    # 2. Desk surface in front of monitors — brightened blue-white zone
    glow_desk = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd2 = ImageDraw.Draw(glow_desk)
    # Elliptical pool on desk surface, centered forward of monitors
    gd2.ellipse([60, DESK_TOP_Y - 15, 680, DESK_TOP_Y + 55],
                fill=MON_SPILL + (50,))
    img.alpha_composite(glow_desk)
    draw = ImageDraw.Draw(img)

    # 3. Chair back spill — blue-white tint on the chair surface facing monitors
    chair_spill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    csd = ImageDraw.Draw(chair_spill)
    # Chair back faces the monitors; left face of chair back receives spill
    csd.ellipse([CH_CX - 50, CH_SEAT_Y - 90, CH_CX + 15, CH_SEAT_Y + 25],
                fill=MON_SPILL + (45,))
    img.alpha_composite(chair_spill)
    draw = ImageDraw.Draw(img)

    # 4. Shelving face spill — right-facing shelves (x ~540–840) nearest monitors
    # Shelf right side catches monitor glow since monitors face roughly toward them
    shelf_spill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ssd = ImageDraw.Draw(shelf_spill)
    # Lower face of shelves (SHELF_Y1 to SHELF_Y2 zone, x: 540–700)
    ssd.rectangle([540, CEIL_Y_FAR + 15, 720, SHELF_Y2 + 10],
                  fill=MON_SPILL + (38,))
    img.alpha_composite(shelf_spill)
    draw = ImageDraw.Draw(img)

    # ── WARM SUNLIGHT OVERLAY — left portion (window zone) ───────────────────
    sun_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sl = ImageDraw.Draw(sun_layer)
    for col in range(0, 320):
        t = 1.0 - col / 320
        a = int(30 * t)
        sl.line([(col, 0), (col, H)],
                fill=SUNLIT_AMBER + (a,), width=1)
    img.alpha_composite(sun_layer)
    draw = ImageDraw.Draw(img)

    # ── FINAL LINE WORK / OUTLINES ────────────────────────────────────────────
    draw.line([(DESK_LEFT, DESK_TOP_Y), (DESK_RIGHT, DESK_TOP_Y)],
              fill=LINE_DARK, width=2)
    draw.line([(0, FLOOR_Y_FAR), (BACK_WALL_RIGHT, FLOOR_Y_FAR)],
              fill=LINE_DARK, width=1)
    draw.line([(0, CEIL_Y_FAR), (BACK_WALL_RIGHT, CEIL_Y_FAR)],
              fill=LINE_DARK, width=1)
    draw.line([(540, 200), (BACK_WALL_RIGHT + 10, 200)], fill=LINE_DARK, width=1)
    draw.line([(540, 260), (BACK_WALL_RIGHT + 10, 260)], fill=LINE_DARK, width=1)
    draw.line([(540, SHELF_Y2), (BACK_WALL_RIGHT + 10, SHELF_Y2)],
              fill=LINE_DARK, width=1)

    # ── OUTPUT ────────────────────────────────────────────────────────────────
    out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_tech_den_v002.png"
    img.convert("RGB").save(out_path)
    print(f"Saved: {out_path}")
    return out_path


if __name__ == "__main__":
    draw_tech_den()
