#!/usr/bin/env python3
"""
LTG_TOOL_bg_tech_den_v001.py — Cosmo's Tech Den Background (Daylight)
"Luma & the Glitchkin" — Background & Environment Design
Artist: Jordan Reed | Cycle 17

Used in: A2-01, A2-03, A2-04, A2-05
Narrative: Cosmo's bedroom repurposed as tech workspace. Daylight version.
           This is where Luma finds Cosmo for her plan at the start of Act 2.

Tone: Warm daylight from left window + cool monitor glow on desk zone.
      Lived-in, loved, ordered chaos. NOT sterile.
      Real World palette ONLY — zero Glitch palette colors.

Environment spec:
  - Small bedroom turned tech workspace
  - Bed pushed to right wall (background, not dominant)
  - Desk dominant foreground-left: CRT monitors + flat panel, oscilloscope,
    breadboards, cables, soldering kit
  - Shelving on back wall: vintage computers, game cartridges, component bins
  - Papers tacked to walls: coding printouts, hand-drawn circuit diagram
  - Window LEFT SIDE: natural daylight (warm gold/amber)
  - Monitor glow: blue-white, fills desk zone
  - Cosmo's jacket (dusty lavender, RW-08) on chair back

Camera: Slight 3/4 angle from doorway. Desk fills left 60%, bed right 40%.
        Low-ish angle — room feels small but packed.

Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_tech_den_v001.png
"""

import math
import random
import os
from PIL import Image, ImageDraw

W, H = 1280, 720

# ── Real World Palette (NO Glitch colors) ────────────────────────────────────
# Walls, floor, ceiling
WALL_WARM         = (240, 228, 200)   # warm cream wall base (RW-01 family)
WALL_SHADOW       = (208, 192, 162)   # wall in shade areas
WALL_WINDOW_LIGHT = (252, 242, 210)   # wall catching window light
CEILING           = (244, 236, 212)   # off-white ceiling
FLOOR_WOOD        = (158, 118,  68)   # hardwood floor planks
FLOOR_WOOD_DARK   = (128,  90,  48)   # floor plank darker variant
FLOOR_WORN        = (172, 132,  82)   # worn traffic path (lighter, more reflective)
SKIRTING          = (190, 155, 105)   # baseboard/skirting boards

# Window / natural light
WINDOW_SKY        = (188, 218, 240)   # sky through window
WINDOW_FRAME      = (222, 200, 158)   # painted wood window frame
SUNLIGHT_GOLD     = (255, 210,  90)   # RW-02 bright sunlight shafts
SUNLIT_AMBER      = (212, 146,  58)   # RW-03 warm amber midtone on lit surfaces
WALL_SUNLIT       = (252, 238, 190)   # wall where sun falls

# Desk and tech equipment
DESK_WOOD_TOP     = (148, 105,  58)   # desk surface (dark wood)
DESK_WOOD_SHADOW  = (108,  72,  36)   # desk underside / shadow edge
DESK_FRAME        = ( 80,  62,  44)   # desk legs / metal frame
CABLE_DARK        = ( 58,  48,  38)   # dark cable tangles
CABLE_MED         = ( 90,  72,  52)   # mid-tone cables
CABLE_GREY        = (110, 108, 102)   # grey power cables

# CRT monitor (muted teal casing — RW-12)
CRT_CASING        = ( 91, 140, 138)   # RW-12 muted teal CRT body
CRT_SHADOW        = ( 58,  90,  88)   # RW-12a dark teal shadow side
CRT_SCREEN_OFF    = ( 28,  34,  40)   # CRT screen dark (not glowing)
CRT_BEZEL         = ( 72, 110, 108)   # CRT bezel/front face

# Flat monitor (modern but not sleek — secondhand)
FLAT_MON_BODY     = (110, 108, 102)   # flat monitor dark grey body
FLAT_MON_SCREEN   = ( 24,  28,  36)   # flat screen dark
FLAT_MON_STAND    = ( 88,  84,  78)   # stand

# Monitor glow (blue-white, real-world — not Glitch cyan)
MON_GLOW_BRIGHT   = (200, 218, 240)   # brightest monitor glow (blue-white)
MON_GLOW_MID      = (170, 190, 220)   # mid monitor glow
MON_GLOW_SOFT     = (140, 162, 195)   # soft outer glow

# Oscilloscope (dark green-on-black analogue unit)
OSCOPE_BODY       = ( 72,  74,  68)   # oscilloscope housing
OSCOPE_SCREEN     = ( 18,  28,  18)   # dark green screen
OSCOPE_KNOBS      = ( 98,  88,  68)   # bakelite-look knobs

# Breadboards and components
BREADBOARD        = (220, 210, 185)   # cream-white breadboard
BREADBOARD_LINES  = (190, 178, 150)   # grid lines
COMPONENT_RED     = (185,  62,  42)   # resistor band
COMPONENT_ORANGE  = (200, 120,  50)   # capacitor
COMPONENT_BLUE    = (100, 128, 168)   # blue component (real-world blue, not Glitch)
SOLDER_SILVER     = (180, 180, 168)   # solder joints / wire ends
WIRE_COPPER       = (168, 112,  52)   # copper wire

# Shelving on back wall
SHELF_WOOD        = (148, 108,  62)   # shelf boards (same family as desk)
SHELF_BRACKET     = ( 90,  75,  58)   # metal shelf bracket
# Vintage computers (boxes, beige-grey)
VINTAGE_PC_BEIGE  = (215, 205, 185)   # old beige PC case
VINTAGE_PC_SHADOW = (175, 162, 140)   # shadow side
VINTAGE_PC_VENT   = (160, 148, 125)   # vent slots
# Game cartridges (colorful little slabs)
CART_YELLOW       = (210, 178,  68)   # cartridge warm yellow
CART_RED          = (188,  72,  52)   # cartridge red
CART_GREY         = (165, 162, 155)   # cartridge grey
CART_BLUE         = (100, 130, 162)   # cartridge blue (real-world, desaturated)
# Component bins (labeled plastic)
BIN_PLASTIC       = (195, 185, 165)   # clear/beige plastic bin
BIN_LABEL         = (240, 232, 210)   # white label on bin

# Wall papers / pinned items
PAPER_WHITE       = (242, 238, 225)   # paper / printout
PAPER_YELLOW      = (235, 218, 148)   # sticky note yellow
CIRCUIT_DIAG_BG   = (228, 220, 195)   # hand-drawn circuit diagram paper (aged)
INK_LINE          = ( 58,  48,  38)   # pen/ink on paper
PUSHPIN_RED       = (188,  58,  42)   # red pushpin

# Bed (pushed to right wall)
BED_FRAME         = (105,  78,  48)   # wooden bed frame
MATTRESS          = (215, 205, 188)   # mattress / base cover
DUVET_BLUE        = (152, 162, 185)   # duvet cover (cool-ish, Cosmo's palette)
PILLOW_CREAM      = (232, 224, 205)   # pillow

# Chair
CHAIR_FABRIC      = (178, 168, 148)   # worn desk chair fabric
CHAIR_FRAME       = ( 75,  62,  48)   # chair frame

# Cosmo's jacket on chair (RW-08 Dusty Lavender)
JACKET_LAV        = (168, 155, 191)   # RW-08 dusty lavender
JACKET_SHADOW     = (120, 110, 145)   # jacket in shadow

# Soldering kit
SOLDER_IRON_TIP   = (190, 165, 100)   # iron tip (warm brass-ish)
SOLDER_IRON_BODY  = (100,  90,  80)   # iron handle
SOLDER_WIRE_SPOOL = (195, 170, 100)   # solder wire spool

# Line / shadow / outline
LINE_DARK         = ( 59,  40,  32)   # RW-11 Deep Cocoa — universal line
SHADOW_COOL       = (168, 155, 191)   # RW-08 cool shadow on warm surfaces
SHADOW_WARM       = (180, 148, 100)   # warm shadow under desk, floor

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
    """Vertical gradient fill in a rectangle using alpha_composite."""
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
    """Horizontal gradient fill."""
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
    """Soft elliptical glow overlay using alpha_composite."""
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

# ── Main draw function ────────────────────────────────────────────────────────

def draw_tech_den():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # ── PERSPECTIVE SETUP ─────────────────────────────────────────────────────
    # Room: left wall (with window) angled slightly. Desk area left ~60% of frame.
    # VP roughly at center-right of frame for mild 3/4 perspective.
    VP_X = 820   # vanishing point X (right of center — camera from left side)
    VP_Y = 295   # vanishing point Y (slightly above center)

    # Floor plane corners: left=far, right=near
    FLOOR_Y_FAR  = 340    # floor line at back wall
    FLOOR_Y_NEAR = H      # floor extends to bottom of frame
    CEIL_Y_FAR   = 210    # ceiling at back wall
    CEIL_Y_NEAR  = -20    # ceiling above frame (cut off)

    # Back wall horizontal extent
    BACK_WALL_LEFT  = 60
    BACK_WALL_RIGHT = 840

    # ── BASE LAYERS ───────────────────────────────────────────────────────────

    # 1. Back wall — warm cream, gradient left (sunlit) to right (cooler)
    gradient_rect_h(img, 0, CEIL_Y_FAR, BACK_WALL_RIGHT, FLOOR_Y_FAR,
                    WALL_WINDOW_LIGHT, WALL_SHADOW)
    draw = ImageDraw.Draw(img)

    # Right side wall (visible from camera angle — leads off to right)
    right_wall_pts = [
        (BACK_WALL_RIGHT, CEIL_Y_FAR),
        (W, CEIL_Y_NEAR),
        (W, H),
        (BACK_WALL_RIGHT, FLOOR_Y_FAR),
    ]
    draw.polygon(right_wall_pts, fill=WALL_SHADOW)

    # Ceiling — light warm cream
    ceil_pts = [
        (0, 0),
        (W, 0),
        (W, CEIL_Y_NEAR),
        (BACK_WALL_RIGHT, CEIL_Y_FAR),
        (0, CEIL_Y_FAR),
    ]
    draw.polygon(ceil_pts, fill=CEILING)
    draw = ImageDraw.Draw(img)

    # Floor — hardwood planks, perspective trapezoid
    floor_pts = [
        (0, FLOOR_Y_FAR),
        (BACK_WALL_RIGHT, FLOOR_Y_FAR),
        (W, H),
        (0, H),
    ]
    draw.polygon(floor_pts, fill=FLOOR_WOOD)

    # Floor plank lines (perspective)
    n_planks = 14
    for i in range(n_planks):
        t = i / n_planks
        # interpolate left edge
        lx = int(0 + t * 0)
        ly = int(FLOOR_Y_FAR + t * (H - FLOOR_Y_FAR))
        rx = int(BACK_WALL_RIGHT + t * (W - BACK_WALL_RIGHT))
        ry = ly
        draw.line([(0, ly), (W, ry)], fill=FLOOR_WOOD_DARK, width=1)

    # Vertical plank dividers fanning from VP area
    for i in range(8):
        t = i / 7
        fx = int(t * W)
        draw.line([(fx, FLOOR_Y_FAR), (fx, H)], fill=FLOOR_WOOD_DARK, width=1)

    # Worn traffic path — slightly lighter strip on floor
    draw_rect(draw, 0, FLOOR_Y_FAR + 30, 500, H, FLOOR_WORN)
    draw = ImageDraw.Draw(img)

    # Skirting board (baseboard along back wall)
    draw_rect(draw, 0, FLOOR_Y_FAR - 14, BACK_WALL_RIGHT, FLOOR_Y_FAR, SKIRTING)

    # ── LEFT WINDOW ───────────────────────────────────────────────────────────
    # Window on left side wall, natural daylight source
    WIN_X0 = 0
    WIN_X1 = 115
    WIN_Y0 = CEIL_Y_FAR + 35
    WIN_Y1 = FLOOR_Y_FAR - 18

    # Window reveal / jamb (angled left wall section)
    left_wall_win_pts = [
        (0, CEIL_Y_FAR),
        (WIN_X1, CEIL_Y_FAR + 10),
        (WIN_X1, FLOOR_Y_FAR - 5),
        (0, FLOOR_Y_FAR),
    ]
    draw.polygon(left_wall_win_pts, fill=WALL_WARM)

    # Window frame
    draw_rect(draw, WIN_X0, WIN_Y0, WIN_X1, WIN_Y1, WINDOW_FRAME)
    # Sky pane
    draw_rect(draw, WIN_X0 + 8, WIN_Y0 + 8, WIN_X1 - 4, WIN_Y1 - 8, WINDOW_SKY)
    # Window cross bar
    mid_y = (WIN_Y0 + WIN_Y1) // 2
    draw_rect(draw, WIN_X0, mid_y - 3, WIN_X1, mid_y + 3, WINDOW_FRAME)
    # Outer glow — sunlight spill on wall around window
    draw = ImageDraw.Draw(img)
    soft_glow_overlay(img, WIN_X1 + 30, (WIN_Y0 + WIN_Y1) // 2, 160, 120,
                      SUNLIGHT_GOLD, max_alpha=55)
    draw = ImageDraw.Draw(img)

    # Sunlight shaft on floor from window
    shaft_pts = [
        (WIN_X0, mid_y),
        (WIN_X1, mid_y - 30),
        (WIN_X1 + 260, FLOOR_Y_FAR + 80),
        (WIN_X0, FLOOR_Y_FAR + 120),
    ]
    shaft_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shaft_draw = ImageDraw.Draw(shaft_layer)
    shaft_draw.polygon(shaft_pts, fill=SUNLIGHT_GOLD + (38,))
    img.alpha_composite(shaft_layer)
    draw = ImageDraw.Draw(img)

    # ── BACK WALL DETAILS ─────────────────────────────────────────────────────

    # Pinned papers on back wall — coding printouts, circuit diagram
    papers = [
        (120, 228, 200, 295, PAPER_WHITE),   # wide printout (code)
        (335, 235, 430, 295, CIRCUIT_DIAG_BG),  # circuit diagram
        (455, 240, 530, 290, PAPER_WHITE),   # another printout
        (150, 300, 260, 350, PAPER_YELLOW),  # sticky note cluster
    ]
    for (px0, py0, px1, py1, pcol) in papers:
        draw_rect(draw, px0, py0, px1, py1, pcol, outline=LINE_DARK, width=1)
        # Pushpin
        draw.ellipse([px0 + 5, py0 - 4, px0 + 12, py0 + 3], fill=PUSHPIN_RED)

    # Fake code lines on printout paper
    for row in range(6):
        lx = 125
        ly = 240 + row * 8
        draw.line([(lx, ly), (lx + rng.randint(40, 70), ly)],
                  fill=INK_LINE, width=1)

    # Circuit diagram lines on paper
    cx0, cy0 = 340, 240
    circuit_pts = [
        (cx0 + 10, cy0 + 10), (cx0 + 30, cy0 + 10),
        (cx0 + 30, cy0 + 20), (cx0 + 60, cy0 + 20),
        (cx0 + 60, cy0 + 35), (cx0 + 20, cy0 + 35),
        (cx0 + 20, cy0 + 50),
    ]
    draw.line(circuit_pts, fill=INK_LINE, width=1)
    # Component symbol (resistor box)
    draw_rect(draw, cx0 + 35, cy0 + 15, cx0 + 50, cy0 + 25, PAPER_WHITE,
              outline=INK_LINE, width=1)

    # ── SHELVING ON BACK WALL ─────────────────────────────────────────────────
    SHELF_Y1 = 248   # bottom of top shelf
    SHELF_Y2 = 310   # bottom of second shelf

    # Shelf boards
    draw_rect(draw, 540, 200, BACK_WALL_RIGHT + 10, SHELF_Y1, SHELF_WOOD)
    draw_rect(draw, 540, 260, BACK_WALL_RIGHT + 10, SHELF_Y2, SHELF_WOOD)

    # Shelf bracket
    draw_rect(draw, 580, CEIL_Y_FAR + 15, 598, SHELF_Y2, SHELF_BRACKET)
    draw_rect(draw, 720, CEIL_Y_FAR + 15, 738, SHELF_Y2, SHELF_BRACKET)

    # Vintage PC cases on top shelf
    pc_positions = [(545, CEIL_Y_FAR + 16, 620, SHELF_Y1 - 2),
                    (625, CEIL_Y_FAR + 22, 690, SHELF_Y1 - 2)]
    for (bx0, by0, bx1, by1) in pc_positions:
        draw_rect(draw, bx0, by0, bx1, by1, VINTAGE_PC_BEIGE, outline=LINE_DARK, width=1)
        draw_rect(draw, bx1 - 8, by0, bx1, by1, VINTAGE_PC_SHADOW)
        # Vent slots
        for vi in range(3):
            vy = by0 + 8 + vi * 5
            draw.line([(bx0 + 4, vy), (bx0 + 16, vy)], fill=VINTAGE_PC_VENT, width=1)
        # Disk drive slot
        drive_y = (by0 + by1) // 2
        draw_rect(draw, bx0 + 5, drive_y - 2, bx0 + 22, drive_y + 2,
                  VINTAGE_PC_VENT)

    # Game cartridges on second shelf (row of small slabs)
    cart_colors = [CART_YELLOW, CART_RED, CART_GREY, CART_BLUE, CART_YELLOW,
                   CART_RED, CART_GREY]
    for i, cc in enumerate(cart_colors):
        cx_ = 548 + i * 30
        draw_rect(draw, cx_, SHELF_Y1 + 4, cx_ + 22, SHELF_Y2 - 4,
                  cc, outline=LINE_DARK, width=1)

    # Component bins (labeled) on second shelf far right
    for bi in range(3):
        bx_ = 700 + bi * 42
        draw_rect(draw, bx_, SHELF_Y1 + 4, bx_ + 36, SHELF_Y2 - 3,
                  BIN_PLASTIC, outline=LINE_DARK, width=1)
        draw_rect(draw, bx_ + 3, SHELF_Y1 + 8, bx_ + 33, SHELF_Y1 + 18,
                  BIN_LABEL)

    # ── DESK (left to center, dominant) ───────────────────────────────────────
    # Desk occupies left ~55% of frame, foreground area
    DESK_TOP_Y    = 395   # desk surface Y
    DESK_LEFT     = 0
    DESK_RIGHT    = 720
    DESK_FRONT_Y  = H - 80   # desk front edge
    DESK_DEPTH    = 80    # perspective depth of desk top

    # Desk surface — trapezoid for perspective
    desk_top_pts = [
        (DESK_LEFT, DESK_TOP_Y),
        (DESK_RIGHT, DESK_TOP_Y),
        (DESK_RIGHT - 40, DESK_TOP_Y - DESK_DEPTH),
        (DESK_LEFT, DESK_TOP_Y - DESK_DEPTH),
    ]
    draw.polygon(desk_top_pts, fill=DESK_WOOD_TOP)
    # Desk front face
    draw_rect(draw, DESK_LEFT, DESK_TOP_Y, DESK_RIGHT, DESK_FRONT_Y, DESK_WOOD_SHADOW)

    # Desk edge highlight
    draw.line([(DESK_LEFT, DESK_TOP_Y), (DESK_RIGHT, DESK_TOP_Y)],
              fill=lerp_color(DESK_WOOD_TOP, (255, 255, 200), 0.3), width=2)

    # Desk legs
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
    # Two CRTs: left (larger, primary) and center-left (older, smaller)

    def draw_crt(draw, img, cx, cy, w_=160, h_=130):
        """Draw a CRT monitor centered at cx, cy."""
        # Body (back bulge)
        body_pts = [
            (cx - w_ // 2 - 18, cy - h_ // 2 + 20),
            (cx + w_ // 2 + 18, cy - h_ // 2 + 20),
            (cx + w_ // 2 + 25, cy + h_ // 2 + 25),
            (cx - w_ // 2 - 25, cy + h_ // 2 + 25),
        ]
        draw.polygon(body_pts, fill=CRT_CASING)
        # Shadow side
        draw.polygon([
            (cx + w_ // 2 + 5, cy - h_ // 2 + 20),
            (cx + w_ // 2 + 18, cy - h_ // 2 + 20),
            (cx + w_ // 2 + 25, cy + h_ // 2 + 25),
            (cx + w_ // 2 + 5, cy + h_ // 2 + 25),
        ], fill=CRT_SHADOW)
        # Bezel front
        draw_rect(draw, cx - w_ // 2, cy - h_ // 2, cx + w_ // 2, cy + h_ // 2,
                  CRT_BEZEL)
        # Screen (slightly inset, slightly curved appearance with round rect)
        sw = w_ - 16
        sh = h_ - 14
        draw_rect(draw, cx - sw // 2, cy - sh // 2, cx + sw // 2, cy + sh // 2,
                  CRT_SCREEN_OFF)
        # Screen glow (blue-white monitor light — real world, NOT glitch cyan)
        glow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow_layer)
        gd.ellipse([cx - sw // 2 - 2, cy - sh // 2 - 2,
                    cx + sw // 2 + 2, cy + sh // 2 + 2],
                   fill=MON_GLOW_BRIGHT + (180,))
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

    # Primary CRT (left, larger)
    CRT1_CX, CRT1_CY = 195, DESK_TOP_Y - 88
    draw = draw_crt(draw, img, CRT1_CX, CRT1_CY, w_=175, h_=140)

    # Secondary CRT (center, slightly smaller, older-looking)
    CRT2_CX, CRT2_CY = 420, DESK_TOP_Y - 75
    draw = draw_crt(draw, img, CRT2_CX, CRT2_CY, w_=150, h_=120)

    # ── FLAT PANEL MONITOR ────────────────────────────────────────────────────
    # Flat panel to the right of the CRTs
    FP_X0, FP_Y0 = 580, DESK_TOP_Y - 130
    FP_X1, FP_Y1 = 690, DESK_TOP_Y - 18
    draw_rect(draw, FP_X0, FP_Y0, FP_X1, FP_Y1, FLAT_MON_BODY, outline=LINE_DARK, width=1)
    draw_rect(draw, FP_X0 + 5, FP_Y0 + 5, FP_X1 - 5, FP_Y1 - 8, FLAT_MON_SCREEN)
    # Stand
    fp_cx = (FP_X0 + FP_X1) // 2
    draw_rect(draw, fp_cx - 8, FP_Y1, fp_cx + 8, FP_Y1 + 15, FLAT_MON_STAND)
    draw_rect(draw, fp_cx - 18, FP_Y1 + 12, fp_cx + 18, FP_Y1 + 18, FLAT_MON_STAND)
    # Screen glow overlay (same blue-white as CRTs)
    soft_glow_overlay(img, fp_cx, (FP_Y0 + FP_Y1) // 2, 80, 70,
                      MON_GLOW_MID, max_alpha=60)
    draw = ImageDraw.Draw(img)

    # ── OSCILLOSCOPE ──────────────────────────────────────────────────────────
    OSC_X0, OSC_Y0 = 60, DESK_TOP_Y - 80
    OSC_X1, OSC_Y1 = 160, DESK_TOP_Y - 5
    draw_rect(draw, OSC_X0, OSC_Y0, OSC_X1, OSC_Y1, OSCOPE_BODY, outline=LINE_DARK, width=1)
    # Screen
    draw_rect(draw, OSC_X0 + 6, OSC_Y0 + 6, OSC_X0 + 52, OSC_Y1 - 8, OSCOPE_SCREEN)
    # Oscilloscope trace (green waveform on screen — dark green, not Glitch)
    TRACE_GREEN = (58, 120, 48)
    trace_pts = []
    for xi in range(0, 46, 3):
        tx = OSC_X0 + 9 + xi
        ty = OSC_Y0 + 25 + int(10 * math.sin(xi * 0.4))
        trace_pts.append((tx, ty))
    if len(trace_pts) >= 2:
        draw.line(trace_pts, fill=TRACE_GREEN, width=1)
    # Knobs
    for ki in range(4):
        kx = OSC_X0 + 62 + ki * 22
        ky = OSC_Y0 + 20
        draw.ellipse([kx - 6, ky - 6, kx + 6, ky + 6], fill=OSCOPE_KNOBS,
                     outline=LINE_DARK, width=1)
    # Bottom knobs row
    for ki in range(3):
        kx = OSC_X0 + 62 + ki * 25
        ky = OSC_Y0 + 48
        draw.ellipse([kx - 5, ky - 5, kx + 5, ky + 5], fill=OSCOPE_KNOBS,
                     outline=LINE_DARK, width=1)

    # ── BREADBOARDS ON DESK ───────────────────────────────────────────────────
    BB_X0, BB_Y0 = 62, DESK_TOP_Y - 4
    BB_X1, BB_Y1 = 145, DESK_TOP_Y + 18
    draw_rect(draw, BB_X0, BB_Y0, BB_X1, BB_Y1, BREADBOARD)
    # Grid lines
    for gi in range(0, BB_X1 - BB_X0, 6):
        draw.line([(BB_X0 + gi, BB_Y0), (BB_X0 + gi, BB_Y1)],
                  fill=BREADBOARD_LINES, width=1)
    # Components on breadboard
    draw.rectangle([BB_X0 + 12, BB_Y0 + 4, BB_X0 + 22, BB_Y0 + 8],
                   fill=COMPONENT_RED)
    draw.ellipse([BB_X0 + 32, BB_Y0 + 3, BB_X0 + 42, BB_Y0 + 11],
                 fill=COMPONENT_ORANGE)
    draw.line([(BB_X0 + 48, BB_Y0 + 2), (BB_X0 + 48, BB_Y0 + 14)],
              fill=WIRE_COPPER, width=1)
    draw.line([(BB_X0 + 58, BB_Y0 + 2), (BB_X0 + 58, BB_Y0 + 14)],
              fill=WIRE_COPPER, width=1)

    # Second breadboard, overlapping
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
    # Iron handle
    draw_rect(draw, SOL_X, SOL_Y - 8, SOL_X + 50, SOL_Y, SOLDER_IRON_BODY)
    # Iron tip (angled)
    draw.polygon([(SOL_X + 50, SOL_Y - 8), (SOL_X + 50, SOL_Y),
                  (SOL_X + 68, SOL_Y - 4)], fill=SOLDER_IRON_TIP)
    # Solder wire spool next to iron
    draw.ellipse([SOL_X - 28, SOL_Y - 14, SOL_X - 4, SOL_Y + 5],
                 fill=SOLDER_WIRE_SPOOL, outline=LINE_DARK, width=1)
    draw.ellipse([SOL_X - 22, SOL_Y - 10, SOL_X - 10, SOL_Y + 1],
                 fill=CABLE_DARK)

    # ── DESK CHAIR ────────────────────────────────────────────────────────────
    # Visible at right edge of desk area, below monitors
    CH_CX = 660
    CH_SEAT_Y = DESK_TOP_Y + 50
    # Seat
    draw.ellipse([CH_CX - 55, CH_SEAT_Y - 15, CH_CX + 55, CH_SEAT_Y + 20],
                 fill=CHAIR_FABRIC)
    # Chair back
    draw_rect(draw, CH_CX - 38, CH_SEAT_Y - 80, CH_CX + 38, CH_SEAT_Y - 15,
              CHAIR_FABRIC, outline=LINE_DARK, width=1)
    # Cosmo's jacket draped over chair back (dusty lavender)
    draw_rect(draw, CH_CX - 50, CH_SEAT_Y - 75, CH_CX - 32, CH_SEAT_Y + 10,
              JACKET_LAV, outline=LINE_DARK, width=1)
    draw_rect(draw, CH_CX + 30, CH_SEAT_Y - 75, CH_CX + 48, CH_SEAT_Y + 10,
              JACKET_SHADOW, outline=LINE_DARK, width=1)
    # Chair post / base
    draw_rect(draw, CH_CX - 5, CH_SEAT_Y + 18, CH_CX + 5, CH_SEAT_Y + 55,
              CHAIR_FRAME)
    # Caster base (simplified cross)
    draw.line([(CH_CX - 35, CH_SEAT_Y + 55), (CH_CX + 35, CH_SEAT_Y + 55)],
              fill=CHAIR_FRAME, width=4)
    draw.line([(CH_CX, CH_SEAT_Y + 45), (CH_CX, CH_SEAT_Y + 65)],
              fill=CHAIR_FRAME, width=4)

    # ── BED (pushed to right wall) ────────────────────────────────────────────
    BED_X0 = 740
    BED_Y0 = 310
    BED_X1 = W - 10
    BED_Y1 = H - 60

    # Bed frame
    draw_rect(draw, BED_X0, BED_Y0, BED_X1, BED_Y1, BED_FRAME)
    # Mattress / base
    draw_rect(draw, BED_X0 + 8, BED_Y0 + 15, BED_X1 - 5, BED_Y1 - 8, MATTRESS)
    # Duvet / covers (slightly messy — lived in)
    draw_rect(draw, BED_X0 + 10, BED_Y0 + 18, BED_X1 - 8, BED_Y0 + 140,
              DUVET_BLUE, outline=LINE_DARK, width=1)
    # Duvet fold / crease
    draw.line([(BED_X0 + 20, BED_Y0 + 60), (BED_X1 - 18, BED_Y0 + 55)],
              fill=lerp_color(DUVET_BLUE, LINE_DARK, 0.3), width=2)
    draw.line([(BED_X0 + 30, BED_Y0 + 90), (BED_X1 - 25, BED_Y0 + 85)],
              fill=lerp_color(DUVET_BLUE, LINE_DARK, 0.2), width=1)
    # Pillows
    draw_rect(draw, BED_X0 + 10, BED_Y0 + 18, BED_X0 + 180, BED_Y0 + 70,
              PILLOW_CREAM, outline=LINE_DARK, width=1)
    draw_rect(draw, BED_X0 + 190, BED_Y0 + 18, BED_X0 + 360, BED_Y0 + 68,
              PILLOW_CREAM, outline=LINE_DARK, width=1)
    # Headboard
    draw_rect(draw, BED_X0, BED_Y0 - 55, BED_X1, BED_Y0 + 20, BED_FRAME)
    draw_rect(draw, BED_X0 + 4, BED_Y0 - 50, BED_X1 - 4, BED_Y0 + 15, MATTRESS)

    # Book / device on bed
    draw_rect(draw, BED_X0 + 30, BED_Y0 + 100, BED_X0 + 90, BED_Y0 + 130,
              CART_GREY, outline=LINE_DARK, width=1)

    # ── MONITOR GLOW AMBIENT LIGHT ────────────────────────────────────────────
    # Wide soft glow from monitors onto wall and ceiling above desk
    soft_glow_overlay(img, 350, DESK_TOP_Y - 100, 350, 200,
                      MON_GLOW_SOFT, max_alpha=45)
    draw = ImageDraw.Draw(img)
    # Glow on desk surface
    glow_desk = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd2 = ImageDraw.Draw(glow_desk)
    gd2.ellipse([80, DESK_TOP_Y - 20, 660, DESK_TOP_Y + 60],
                fill=MON_GLOW_BRIGHT + (28,))
    img.alpha_composite(glow_desk)
    draw = ImageDraw.Draw(img)

    # Warm sunlight overlay on left portion of room (window side)
    sun_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sl = ImageDraw.Draw(sun_layer)
    # Gradient warm wash on left 30% of frame
    for col in range(0, 320):
        t = 1.0 - col / 320
        a = int(28 * t)
        sl.line([(col, 0), (col, H)],
                fill=SUNLIT_AMBER + (a,), width=1)
    img.alpha_composite(sun_layer)
    draw = ImageDraw.Draw(img)

    # ── FINAL LINE WORK / OUTLINES ────────────────────────────────────────────
    # Desk top edge
    draw.line([(DESK_LEFT, DESK_TOP_Y), (DESK_RIGHT, DESK_TOP_Y)],
              fill=LINE_DARK, width=2)
    # Back wall floor line
    draw.line([(0, FLOOR_Y_FAR), (BACK_WALL_RIGHT, FLOOR_Y_FAR)],
              fill=LINE_DARK, width=1)
    # Back wall ceiling line
    draw.line([(0, CEIL_Y_FAR), (BACK_WALL_RIGHT, CEIL_Y_FAR)],
              fill=LINE_DARK, width=1)
    # Shelf top edges
    draw.line([(540, 200), (BACK_WALL_RIGHT + 10, 200)], fill=LINE_DARK, width=1)
    draw.line([(540, 260), (BACK_WALL_RIGHT + 10, 260)], fill=LINE_DARK, width=1)
    draw.line([(540, SHELF_Y2), (BACK_WALL_RIGHT + 10, SHELF_Y2)],
              fill=LINE_DARK, width=1)

    # ── OUTPUT ────────────────────────────────────────────────────────────────
    out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_tech_den_v001.png"
    img.convert("RGB").save(out_path)
    print(f"Saved: {out_path}")
    return out_path


if __name__ == "__main__":
    draw_tech_den()
