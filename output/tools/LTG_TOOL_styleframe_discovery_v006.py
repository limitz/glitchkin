#!/usr/bin/env python3
"""
LTG_TOOL_styleframe_discovery_v006.py
Style Frame 01 — The Discovery (C38 sight-line + visual power fix)
"Luma & the Glitchkin" — Cycle 38

Art Director: Alex Chen
Procedural Art Engineer: Rin Yamamoto
Cycle: 38

C38 changes (Rin Yamamoto):
  Sight-line fix (Ingrid critique C15 P2 + Lee Tanaka staging brief):
    - Luma's head TURNED toward CRT/Byte (gaze comes FIRST, body follows).
      head_cx shifted RIGHT +18px (head_gaze_offset). head_cy +6px (chin down).
      Face: pupils strongly shifted right toward emerge_cx; screen-side eye wider
      (wonder); away-side eye slightly squinted (intensity/concentration).
      Brow: screen-side raised HIGH; away-side lower with kink (not trusting yet).
      Mouth: CLOSED / barely open — "held, not performing" (Lee brief spec).
      NOT an open O of shock.
    - ARM: REACHING gesture (Lee brief Option B) — NOT pointing.
      Open palm facing screen, fingers slightly spread. "I want to touch it."
      No index-finger extension. Removes "display" read, adds "desire" read.
    - Forward lean toward screen (Lee + Alex: 4-6 deg, gravity of attention).
    - Chin down 4-6 deg (Lee brief: tracking-in, focusing posture).
  Visual power fix (Alex Chen brief + Lee visual power note, C38 P2):
    - Hair: screen-side curl pulled FORWARD toward CRT at steeper angle
      (Lee brief: "outer curl of screen-side hair at slightly steeper angle").
      Crown tuft gives upward energy spike. Away-side arc floats back (counterweight).
    - Hoodie pixel pattern: expanded from 7 to 12 pixels — chest reads richer.
    - Shoulder rolled forward on screen side (Lee brief: body opens toward screen).
    - Face test gate run (sprint scale N/A — Luma at full scale head_r≈66).

C32 changes: add_rim_light() canvas-midpoint bug fix (char_cx=head_cx).
C30 fix: eye width ew = int(head_r * 0.22) per canonical spec.
C29: Procedural quality pass — wobble_polygon, variable_stroke, face_lighting,
     rim light, canvas 1280x720.

Prior SF01 v005 history: ghost Byte alpha 55->90, rim-light char_cx fix.

Output: /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_discovery_v006.png
Usage: python3 LTG_TOOL_styleframe_discovery_v006.py
"""

import os
import sys
import math
import random
from PIL import Image, ImageDraw, ImageFont

# Import procedural draw library
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
from LTG_TOOL_procedural_draw_v001 import (
    wobble_line, wobble_polygon, variable_stroke,
    add_rim_light, add_face_lighting
)

OUTPUT_PATH = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_discovery_v006.png"

# Working at 1280x720 — fits <= 1280px rule directly
W, H = 1280, 720

# Scale factors from 1920x1080 reference (v003) to 1280x720
SX = W / 1920
SY = H / 1080

def sx(n): return int(n * SX)
def sy(n): return int(n * SY)
def sp(n): return int(n * min(SX, SY))  # for radii / widths

# ── Master Palette (from master_palette.md) ──────────────────────────────────
WARM_CREAM      = (250, 240, 220)
SOFT_GOLD       = (232, 201,  90)
SUNLIT_AMBER    = (212, 146,  58)
TERRACOTTA      = (199,  91,  57)
RUST_SHADOW     = (140,  58,  34)
SAGE_GREEN      = (122, 158, 126)
DUSTY_LAVENDER  = (168, 155, 191)
SHADOW_PLUM     = ( 92,  74, 114)
WARM_TAN        = (196, 168, 130)
SKIN_SHADOW     = (140,  90,  56)
DEEP_COCOA      = ( 59,  40,  32)
OCHRE_BRICK     = (184, 148,  74)
ELEC_CYAN       = (  0, 240, 255)
BYTE_TEAL       = (  0, 212, 232)
DEEP_CYAN       = (  0, 168, 180)
HOT_MAGENTA     = (255,  45, 107)
UV_PURPLE       = (123,  47, 190)
VOID_BLACK      = ( 10,  10,  20)
CORRUPTED_AMBER = (255, 140,   0)
STATIC_WHITE    = (240, 240, 240)
SKIN            = (200, 136,  90)
SKIN_HL         = (232, 184, 136)
SKIN_SH         = (168, 104,  56)
CYAN_SKIN       = (122, 188, 186)
HOODIE_ORANGE   = (232, 112,  58)
HOODIE_SHADOW   = (184,  74,  32)
HOODIE_CYAN_LIT = (191, 138, 120)
HAIR_COLOR      = ( 26,  15,  10)
LINE            = ( 59,  40,  32)
BYTE_HL         = (  0, 240, 255)
BYTE_SH         = (  0, 144, 176)
SCAR_MAG        = (255,  45, 107)
HOODIE_AMBIENT  = (179,  98,  80)
JEANS           = ( 58,  90, 140)
JEANS_SH        = ( 38,  62, 104)
COUCH_BODY      = (107,  48,  24)
COUCH_BACK      = (128,  60,  28)
COUCH_ARM       = (115,  52,  26)
# Blush: warm peach (matches SF04 v003 correction — NOT orange-red)
BLUSH_LEFT      = (232, 168, 124)
BLUSH_RIGHT     = (228, 162, 118)
LAMP_PEAK       = (245, 200,  66)
CABLE_BRONZE    = (180, 140,  80)
CABLE_DATA_CYAN = (  0, 180, 255)
CABLE_MAG_PURP  = (200,  80, 200)
CABLE_NEUTRAL_PLUM = ( 80,  64, 100)


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


def draw_filled_glow(draw, cx, cy, rx, ry, glow_rgb, bg_rgb, steps=14):
    for i in range(steps, 0, -1):
        t = i / steps
        r_v = int(bg_rgb[0] + (glow_rgb[0] - bg_rgb[0]) * (1 - t))
        g_v = int(bg_rgb[1] + (glow_rgb[1] - bg_rgb[1]) * (1 - t))
        b_v = int(bg_rgb[2] + (glow_rgb[2] - bg_rgb[2]) * (1 - t))
        er   = max(1, int(rx * t))
        er_y = max(1, int(ry * t))
        draw.ellipse([cx - er, cy - er_y, cx + er, cy + er_y], fill=(r_v, g_v, b_v))


def draw_amber_outline(draw, cx, cy, rx, ry, width=3):
    for i in range(width):
        draw.ellipse(
            [cx - rx - i, cy - ry - i, cx + rx + i, cy + ry + i],
            outline=CORRUPTED_AMBER
        )


def draw_background(draw, img):
    rng = random.Random(42)
    ceiling_y = sy(int(1080 * 0.12))
    draw.rectangle([0, 0, W, ceiling_y], fill=(90, 55, 22))
    draw.line([(0, ceiling_y), (W, ceiling_y)], fill=(60, 36, 14), width=sp(4))

    wall_top_y = ceiling_y
    wall_bot_y = sy(int(1080 * 0.54))
    far_wall   = (228, 185, 120)
    base_wall  = (212, 146,  58)
    for y in range(wall_top_y, wall_bot_y):
        t = (y - wall_top_y) / max(1, wall_bot_y - wall_top_y)
        r_v = int(far_wall[0] + (base_wall[0] - far_wall[0]) * t)
        g_v = int(far_wall[1] + (base_wall[1] - far_wall[1]) * t)
        b_v = int(far_wall[2] + (base_wall[2] - far_wall[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r_v, g_v, b_v))

    draw.rectangle([0, sy(int(1080 * 0.54)), W, sy(int(1080 * 0.75))], fill=(140, 90, 26))
    draw.line([(0, sy(int(1080 * 0.54))), (W, sy(int(1080 * 0.54)))], fill=(100, 64, 18), width=sp(3))
    draw.rectangle([0, sy(int(1080 * 0.75)), W, H], fill=(90, 56, 32))
    for y in range(sy(int(1080 * 0.75)), H, sp(28)):
        draw.line([(0, y), (W, y)], fill=RUST_SHADOW, width=1)
    for y in range(sy(int(1080 * 0.76)), H, sp(56)):
        draw.line([(0, y + sp(4)), (W, y + sp(4))], fill=(110, 70, 42), width=1)

    # Monitor wall
    mw_x  = sx(int(1920 * 0.50))
    mw_y  = ceiling_y + sp(5)
    mw_w  = sx(int(1920 * 0.46))
    mw_h  = sy(int(1080 * 0.57))
    draw.rectangle([mw_x, mw_y, mw_x + mw_w, mw_y + mw_h], fill=(14, 10, 22))

    # Monitor specs (scaled from 1920x1080)
    monitor_specs = [
        (mw_x + sx(40),  mw_y + sy(20),  sx(260), sy(150)),  # [0] top-left — WARM ZONE (lamp bleed)
        (mw_x + sx(330), mw_y + sy(15),  sx(320), sy(180)),  # [1] top-center
        (mw_x + sx(680), mw_y + sy(28),  sx(230), sy(140)),  # [2] top-right — ghost
        (mw_x + sx(50),  mw_y + sy(190), sx(280), sy(165)),  # [3] mid-left — ghost
        (mw_x + sx(360), mw_y + sy(215), sx(300), sy(170)),  # [4] mid-center
        (mw_x + sx(685), mw_y + sy(185), sx(210), sy(150)),  # [5] mid-right
    ]

    cx_glow = mw_x + mw_w // 2
    cy_glow = mw_y + mw_h // 2
    draw_filled_glow(draw, cx_glow, cy_glow,
                     rx=sx(720), ry=sy(420),
                     glow_rgb=(0, 60, 100),
                     bg_rgb=(14, 10, 22),
                     steps=16)

    for mx, my, mw_s, mh_s in monitor_specs:
        draw.rectangle([mx - sp(6), my - sp(6), mx + mw_s + sp(6), my + mh_s + sp(6)],
                       fill=(12, 10, 18), outline=(28, 22, 40), width=sp(2))
        draw.rectangle([mx, my, mx + mw_s, my + mh_s], fill=ELEC_CYAN)
        cx_m = mx + mw_s // 2
        cy_m = my + mh_s // 2
        draw_filled_glow(draw, cx_m, cy_m,
                         mw_s // 2, mh_s // 2,
                         glow_rgb=(180, 255, 255),
                         bg_rgb=ELEC_CYAN,
                         steps=8)
        for sy_scan in range(my + sp(3), my + mh_s, sp(5)):
            draw.line([(mx, sy_scan), (mx + mw_s, sy_scan)], fill=(0, 168, 180), width=1)
        draw.line([(mx, my), (mx + mw_s, my)], fill=(40, 40, 60), width=sp(2))

    # Ghost Byte (Cycle 13 calibration: alpha 90/105, specs[2]+specs[3] only)
    ghost_screens = [
        monitor_specs[2],   # top-right — cold zone, full contrast
        monitor_specs[3],   # mid-left — away from warm lamp bleed, good contrast
    ]
    for gs_mx, gs_my, gs_mw, gs_mh in ghost_screens:
        ghost_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ghost_draw  = ImageDraw.Draw(ghost_layer)
        g_cx  = gs_mx + gs_mw // 2
        g_cy  = gs_my + gs_mh // 2 - int(gs_mh * 0.08)
        g_rx  = int(gs_mw * 0.28)
        g_ry  = int(gs_mh * 0.38)
        ghost_draw.ellipse([g_cx - g_rx, g_cy - g_ry, g_cx + g_rx, g_cy + g_ry],
                           fill=(0, 53, 58, 90))
        eye_y = g_cy - int(g_ry * 0.15)
        e_r   = max(2, int(g_rx * 0.20))
        ghost_draw.rectangle([g_cx - int(g_rx * 0.35) - e_r, eye_y - e_r,
                               g_cx - int(g_rx * 0.35) + e_r, eye_y + e_r],
                              fill=(0, 220, 240, 105))
        ghost_draw.ellipse([g_cx + int(g_rx * 0.20) - e_r, eye_y - e_r,
                            g_cx + int(g_rx * 0.20) + e_r, eye_y + e_r],
                           fill=(0, 220, 240, 105))
        base_rgba = img.convert("RGBA")
        img_with_ghost = Image.alpha_composite(base_rgba, ghost_layer)
        img.paste(img_with_ghost.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # CRT screen (main discovery CRT)
    crt_x  = mw_x + int(mw_w * 0.22)
    crt_y  = mw_y + int(mw_h * 0.08)
    crt_w  = int(mw_w * 0.52)
    crt_h  = int(mw_h * 0.62)

    # Wobble CRT frame outline for procedural quality
    crt_frame_pts = [
        (crt_x - sp(10), crt_y - sp(10)),
        (crt_x + crt_w + sp(10), crt_y - sp(10)),
        (crt_x + crt_w + sp(10), crt_y + crt_h + sp(20)),
        (crt_x - sp(10), crt_y + crt_h + sp(20)),
    ]
    wobble_polygon(draw, crt_frame_pts, color=(44, 36, 56),
                   width=sp(3), amplitude=sp(2), frequency=4, seed=200,
                   fill=(44, 36, 56))

    draw.rectangle([crt_x + crt_w // 3, crt_y + crt_h + sp(18),
                    crt_x + crt_w * 2 // 3, crt_y + crt_h + sp(40)],
                   fill=(36, 28, 46))
    scr_pad = sp(24)
    scr_x0  = crt_x + scr_pad
    scr_y0  = crt_y + scr_pad
    scr_x1  = crt_x + crt_w - scr_pad
    scr_y1  = crt_y + crt_h - scr_pad * 2
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1], fill=ELEC_CYAN)

    scr_mid_x = (scr_x0 + scr_x1) // 2
    scr_mid_y = (scr_y0 + scr_y1) // 2
    grid_color = (0, 168, 180)
    for i in range(1, 6):
        t = i / 5.0
        lx = int(scr_x0 + (scr_mid_x - scr_x0) * t)
        rx = int(scr_x1 - (scr_x1 - scr_mid_x) * t)
        draw.line([(lx, scr_y0), (scr_mid_x, scr_mid_y)], fill=grid_color, width=1)
        draw.line([(rx, scr_y0), (scr_mid_x, scr_mid_y)], fill=grid_color, width=1)
    for i in range(1, 5):
        t = i / 4.0
        ty = int(scr_y0 + (scr_mid_y - scr_y0) * t)
        draw.line([(scr_x0, ty), (scr_mid_x, scr_mid_y)], fill=grid_color, width=1)
        draw.line([(scr_x1, ty), (scr_mid_x, scr_mid_y)], fill=grid_color, width=1)

    scr_rng = random.Random(99)
    fig_x = scr_x0 + sp(14)
    fig_y = scr_y0 + sp(12)
    fig_color = (0, 80, 100)
    draw.rectangle([fig_x + sp(5), fig_y,      fig_x + sp(10), fig_y + sp(4)],  fill=fig_color)
    draw.rectangle([fig_x + sp(3), fig_y + sp(4),  fig_x + sp(12), fig_y + sp(9)],  fill=fig_color)
    draw.rectangle([fig_x,         fig_y + sp(4),  fig_x + sp(3),  fig_y + sp(6)],  fill=fig_color)
    draw.rectangle([fig_x + sp(12), fig_y + sp(4), fig_x + sp(15), fig_y + sp(6)],  fill=fig_color)
    draw.rectangle([fig_x + sp(3),  fig_y + sp(9), fig_x + sp(6),  fig_y + sp(14)], fill=fig_color)
    draw.rectangle([fig_x + sp(9),  fig_y + sp(9), fig_x + sp(12), fig_y + sp(14)], fill=fig_color)

    fig_x2 = scr_x1 - sp(30)
    fig_y2 = scr_y0 + sp(10)
    fig_color2 = (0, 60, 80)
    draw.rectangle([fig_x2 + sp(5), fig_y2,      fig_x2 + sp(10), fig_y2 + sp(4)],  fill=fig_color2)
    draw.rectangle([fig_x2 + sp(3), fig_y2 + sp(4), fig_x2 + sp(12), fig_y2 + sp(9)],  fill=fig_color2)
    draw.rectangle([fig_x2 - sp(6), fig_y2 + sp(4), fig_x2 + sp(3), fig_y2 + sp(6)],   fill=fig_color2)
    draw.rectangle([fig_x2 + sp(12), fig_y2 + sp(4), fig_x2 + sp(15), fig_y2 + sp(6)], fill=fig_color2)
    draw.rectangle([fig_x2 + sp(3),  fig_y2 + sp(9), fig_x2 + sp(6),  fig_y2 + sp(14)], fill=fig_color2)
    draw.rectangle([fig_x2 + sp(9),  fig_y2 + sp(9), fig_x2 + sp(12), fig_y2 + sp(14)], fill=fig_color2)

    for _ in range(28):
        px_x = scr_x0 + scr_rng.randint(0, scr_x1 - scr_x0)
        px_y = scr_y0 + scr_rng.randint(0, scr_y1 - scr_y0)
        dist_from_center = ((px_x - scr_mid_x) ** 2 + (px_y - scr_mid_y) ** 2) ** 0.5
        min_dist = min(scr_x1 - scr_x0, scr_y1 - scr_y0) * 0.30
        if dist_from_center > min_dist:
            ps = scr_rng.choice([2, 3])
            pc = scr_rng.choice([(0, 100, 120), (0, 60, 80), (0, 140, 160)])
            draw.rectangle([px_x, px_y, px_x + ps, px_y + ps], fill=pc)

    emerge_cx = (scr_x0 + scr_x1) // 2
    emerge_cy = (scr_y0 + scr_y1) // 2
    emerge_rx = int((scr_x1 - scr_x0) * 0.34)
    emerge_ry = int((scr_y1 - scr_y0) * 0.44)
    draw.ellipse([emerge_cx - emerge_rx, emerge_cy - emerge_ry,
                  emerge_cx + emerge_rx, emerge_cy + emerge_ry],
                 fill=(14, 14, 30))
    draw.ellipse([emerge_cx - emerge_rx - sp(8), emerge_cy - emerge_ry - sp(8),
                  emerge_cx + emerge_rx + sp(8), emerge_cy + emerge_ry + sp(8)],
                 outline=DEEP_CYAN, width=sp(4))
    draw.ellipse([emerge_cx - emerge_rx - sp(14), emerge_cy - emerge_ry - sp(14),
                  emerge_cx + emerge_rx + sp(14), emerge_cy + emerge_ry + sp(14)],
                 outline=(0, 80, 100), width=sp(2))
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1], outline=DEEP_CYAN, width=sp(5))
    for sy_scan in range(scr_y0 + sp(4), scr_y1, sp(7)):
        draw.line([(scr_x0, sy_scan), (scr_x1, sy_scan)], fill=(0, 168, 180), width=1)

    rng_confetti = random.Random(42)
    for _ in range(80):
        px = rng_confetti.randint(scr_x0 - sx(120), scr_x1 + sx(60))
        py = rng_confetti.randint(scr_y0 - sy(80), sy(int(1080 * 0.75)))
        ps = rng_confetti.choice([3, 4, 5, 6])
        pc = rng_confetti.choice([ELEC_CYAN, STATIC_WHITE, BYTE_TEAL, (0, 200, 220)])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)

    floor_glow_pts = [
        (crt_x,            sy(int(1080 * 0.75))),
        (crt_x + crt_w,    sy(int(1080 * 0.75))),
        (crt_x + crt_w + sx(160), H),
        (crt_x - sx(100),  H),
    ]
    draw.polygon(floor_glow_pts, fill=(0, 22, 38))
    draw_filled_glow(draw, mw_x - sp(20), mw_y + mw_h // 2,
                     rx=sx(160), ry=sy(220),
                     glow_rgb=(0, 40, 70),
                     bg_rgb=(180, 130, 60),
                     steps=10)

    # Window
    win_x0, win_y0 = sx(60), ceiling_y + sy(20)
    win_x1, win_y1 = sx(340), ceiling_y + sy(260)
    draw.rectangle([win_x0 - sx(30), win_y0 - sy(10), win_x0 + sx(14), win_y1 + sy(20)], fill=(168, 108, 48))
    draw.rectangle([win_x1 - sx(14), win_y0 - sy(10), win_x1 + sx(30), win_y1 + sy(20)], fill=(168, 108, 48))
    draw.rectangle([win_x0, win_y0, win_x1, win_y1], fill=SOFT_GOLD)
    draw.rectangle([win_x0, win_y0, win_x1, win_y1], outline=DEEP_COCOA, width=sp(4))
    mid_win_x = (win_x0 + win_x1) // 2
    mid_win_y = (win_y0 + win_y1) // 2
    draw.line([(mid_win_x, win_y0), (mid_win_x, win_y1)], fill=DEEP_COCOA, width=sp(3))
    draw.line([(win_x0, mid_win_y), (win_x1, mid_win_y)], fill=DEEP_COCOA, width=sp(3))

    # Bookshelves
    shelf_x = sx(int(1920 * 0.20))
    shelf_y = ceiling_y
    shelf_w = sx(int(1920 * 0.28))
    shelf_h = sy(int(1080 * 0.45))
    draw.rectangle([shelf_x, shelf_y, shelf_x + shelf_w, shelf_y + shelf_h], fill=SUNLIT_AMBER)
    book_colors = [TERRACOTTA, SAGE_GREEN, DUSTY_LAVENDER, OCHRE_BRICK,
                   RUST_SHADOW, (96, 144, 180), (184, 160, 100)]
    rng_books = random.Random(42)
    for row in range(shelf_y + sp(4), shelf_y + shelf_h, sy(50)):
        draw.line([(shelf_x, row + sy(44)), (shelf_x + shelf_w, row + sy(44))], fill=DEEP_COCOA, width=sp(2))
        col_idx = 0
        bx = shelf_x + sp(8)
        while bx + sp(20) < shelf_x + shelf_w:
            bw = rng_books.randint(sx(18), sx(36))
            bc = book_colors[col_idx % len(book_colors)]
            draw.rectangle([bx, row + sp(4), bx + bw, row + sy(42)], fill=bc)
            draw.line([(bx, row + sp(4)), (bx, row + sy(42))], fill=DEEP_COCOA, width=1)
            bx += bw + sp(2)
            col_idx += 1

    # Desk
    desk_y = sy(int(1080 * 0.60))
    desk_x0 = mw_x - sx(80)
    desk_x1 = W
    draw.rectangle([desk_x0, desk_y, desk_x1, desk_y + sy(70)], fill=OCHRE_BRICK)
    draw.line([(desk_x0, desk_y), (desk_x1, desk_y)], fill=DEEP_COCOA, width=sp(3))
    draw.rectangle([desk_x0 + sx(30), desk_y + sy(10), desk_x0 + sx(240), desk_y + sy(46)],
                   fill=DUSTY_LAVENDER, outline=DEEP_COCOA, width=sp(2))
    for ky in range(desk_y + sy(16), desk_y + sy(40), sy(10)):
        for kx in range(desk_x0 + sx(38), desk_x0 + sx(234), sx(18)):
            draw.rectangle([kx, ky, kx + sx(14), ky + sy(7)], fill=(148, 135, 175))
    draw.rectangle([desk_x0 + sx(260), desk_y + sy(8), desk_x0 + sx(310), desk_y + sy(55)],
                   fill=TERRACOTTA, outline=DEEP_COCOA, width=sp(2))
    draw.arc([desk_x0 + sx(308), desk_y + sy(20), desk_x0 + sx(332), desk_y + sy(44)],
             start=270, end=90, fill=DEEP_COCOA, width=sp(3))
    cable_colors = [ELEC_CYAN, HOT_MAGENTA, CABLE_BRONZE, CABLE_DATA_CYAN]
    for ci, cc in enumerate(cable_colors):
        cx_s = desk_x0 + sx(40) + ci * sx(60)
        cx_e = desk_x0 + sx(120) + ci * sx(80)
        draw.arc([cx_s, desk_y + sy(50), cx_e, desk_y + sy(100)], 0, 180, fill=cc, width=sp(2))

    # Lamp
    lamp_x = sx(int(1920 * 0.40))
    lamp_y = ceiling_y + sy(18)
    draw_filled_glow(draw, lamp_x + sx(32), lamp_y + sy(50),
                     rx=sx(180), ry=sy(110),
                     glow_rgb=LAMP_PEAK,
                     bg_rgb=base_wall,
                     steps=12)
    draw.rectangle([lamp_x, lamp_y, lamp_x + sx(64), lamp_y + sy(86)],
                   fill=(245, 200, 66), outline=DEEP_COCOA, width=sp(2))
    draw.ellipse([lamp_x + sx(12), lamp_y + sy(80), lamp_x + sx(52), lamp_y + sy(96)],
                 fill=SUNLIT_AMBER)
    draw_filled_glow(draw, lamp_x + sx(32), sy(int(1080 * 0.85)),
                     rx=sx(120), ry=sy(44),
                     glow_rgb=LAMP_PEAK,
                     bg_rgb=(90, 56, 32),
                     steps=10)

    # Cable clutter foreground
    draw.rectangle([0, sy(int(1080 * 0.92)), W, H], fill=(42, 26, 16))
    fg_cables = [
        (sx(80),   sx(460),  sy(int(1080*0.935)), sy(60),  ELEC_CYAN,          2),
        (sx(240),  sx(780),  sy(int(1080*0.950)), sy(85),  HOT_MAGENTA,        2),
        (sx(420),  sx(980),  sy(int(1080*0.930)), sy(44),  CABLE_BRONZE,       2),
        (sx(600),  sx(1200), sy(int(1080*0.960)), sy(70),  CABLE_DATA_CYAN,    1),
        (sx(840),  sx(1500), sy(int(1080*0.940)), sy(92),  SOFT_GOLD,          2),
        (sx(980),  sx(1720), sy(int(1080*0.952)), sy(52),  CABLE_MAG_PURP,     1),
        (sx(1200), sx(1880), sy(int(1080*0.928)), sy(74),  ELEC_CYAN,          2),
        (sx(1460), sx(1920), sy(int(1080*0.962)), sy(38),  HOT_MAGENTA,        1),
        (sx(100),  sx(600),  sy(int(1080*0.970)), sy(32),  CABLE_NEUTRAL_PLUM, 1),
    ]
    for x0c, x1c, base_yc, arc_r, color, thickness in fg_cables:
        pts = []
        for s in range(31):
            t = s / 30
            px_c = int(x0c + (x1c - x0c) * t)
            sag = int(arc_r * 4 * t * (1 - t))
            pts.append((px_c, base_yc + sag))
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=color, width=thickness)

    # Mid-air transition element
    air_rng = random.Random(77)
    zone_x0 = sx(int(1920 * 0.40))
    zone_x1 = sx(int(1920 * 0.50))
    zone_mid = (zone_x0 + zone_x1) // 2
    for _ in range(60):
        px = air_rng.randint(zone_x0 - sx(20), zone_x1 + sx(20))
        py = air_rng.randint(sy(200), sy(700))
        ps = air_rng.choice([3, 4, 5, 6])
        if px < zone_mid:
            pc = air_rng.choice([SOFT_GOLD, SUNLIT_AMBER, (245, 200, 66), WARM_CREAM])
        else:
            pc = air_rng.choice([ELEC_CYAN, BYTE_TEAL, DEEP_CYAN, STATIC_WHITE])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)

    return {
        "scr_x0": scr_x0, "scr_y0": scr_y0,
        "scr_x1": scr_x1, "scr_y1": scr_y1,
        "emerge_cx": emerge_cx, "emerge_cy": emerge_cy,
        "emerge_rx": emerge_rx, "emerge_ry": emerge_ry,
        "mw_x": mw_x, "mw_y": mw_y, "mw_w": mw_w, "mw_h": mw_h,
        "ceiling_y": ceiling_y,
        "lamp_x": lamp_x, "lamp_y": lamp_y,
        "base_wall": base_wall,
    }


def draw_luma_body(draw, luma_cx, luma_base_y, facing_monitor_x):
    """
    C38: Forward lean toward screen per Lee Tanaka + Alex Chen briefs.
    lean_offset=sp(44) — torso top pulled forward toward screen,
    body gravity shifts toward CRT ('she is about to stand').
    Head gaze offset is handled separately in generate() by shifting head_cx further right.
    """
    luma_x = luma_cx
    y_base = luma_base_y
    # C38: Forward lean toward screen per Lee Tanaka brief (4-6 deg, gravity of attention).
    # lean_offset pushes torso top forward (toward screen/right). sp(44) = ~5 deg forward lean.
    lean_offset = sp(44)

    draw.polygon([
        (luma_x - sp(48), y_base), (luma_x - sp(20), y_base),
        (luma_x - sp(15), y_base - sp(90)), (luma_x - sp(50), y_base - sp(88)),
    ], fill=JEANS)
    draw.polygon([
        (luma_x + sp(14), y_base), (luma_x + sp(44), y_base - sp(4)),
        (luma_x + sp(46), y_base - sp(84)), (luma_x + sp(12), y_base - sp(86)),
    ], fill=JEANS)
    draw.polygon([
        (luma_x - sp(50), y_base - sp(88)), (luma_x - sp(48), y_base),
        (luma_x - sp(34), y_base - sp(2)), (luma_x - sp(32), y_base - sp(86)),
    ], fill=JEANS_SH)
    draw.rectangle([luma_x - sp(60), y_base - sp(10), luma_x - sp(8), y_base + sp(22)], fill=WARM_CREAM)
    draw.rectangle([luma_x - sp(62), y_base + sp(16), luma_x - sp(6), y_base + sp(26)], fill=DEEP_COCOA)
    draw.rectangle([luma_x + sp(2), y_base - sp(10), luma_x + sp(58), y_base + sp(20)], fill=WARM_CREAM)
    draw.rectangle([luma_x, y_base + sp(16), luma_x + sp(60), y_base + sp(26)], fill=DEEP_COCOA)

    torso_top = y_base - sp(260)
    torso_bot = y_base - sp(90)
    torso_half_w = sp(44)
    for row in range(torso_bot, torso_top, -1):
        t_y = (torso_bot - row) / max(1, torso_bot - torso_top)
        row_lean = int(lean_offset * t_y)
        x_left  = luma_x - torso_half_w + row_lean
        x_right = luma_x + torso_half_w + row_lean
        width   = x_right - x_left
        for col in range(x_left, x_right + 1):
            t_x = (col - x_left) / max(1, width)
            r_v = int(HOODIE_ORANGE[0] * (1 - t_x) + HOODIE_CYAN_LIT[0] * t_x)
            g_v = int(HOODIE_ORANGE[1] * (1 - t_x) + HOODIE_CYAN_LIT[1] * t_x)
            b_v = int(HOODIE_ORANGE[2] * (1 - t_x) + HOODIE_CYAN_LIT[2] * t_x)
            draw.point((col, row), fill=(r_v, g_v, b_v))

    draw.polygon([
        (luma_x - torso_half_w, torso_bot - sp(8)), (luma_x - torso_half_w, torso_bot),
        (luma_x + torso_half_w, torso_bot), (luma_x + torso_half_w, torso_bot - sp(8)),
    ], fill=HOODIE_AMBIENT)

    # C38: More hoodie pixel pattern squares (12 vs 7) — richer chest detail, more visual energy
    rng_px = random.Random(55)
    for i in range(12):
        ppx = luma_x - torso_half_w + lean_offset + rng_px.randint(sp(2), torso_half_w * 2 - sp(6))
        ppy = torso_top + rng_px.randint(sp(4), sp(50))
        pps = rng_px.choice([sp(4), sp(6), sp(8)])
        col_choices = [ELEC_CYAN, BYTE_TEAL, (0, 200, 220), (0, 240, 240)]
        draw.rectangle([ppx, ppy, ppx + pps, ppy + pps], fill=rng_px.choice(col_choices))

    head_cx = luma_x + lean_offset
    head_cy = torso_top - sp(70)
    draw.rectangle([head_cx - sp(6), torso_top, head_cx + sp(6), torso_top + sp(30)], fill=HOODIE_ORANGE)

    for row in range(torso_top + sp(2), head_cy + sp(60)):
        t_n = (row - (torso_top + sp(2))) / max(1, (head_cy + sp(60)) - (torso_top + sp(2)))
        draw.line([(luma_x - sp(18) + int(t_n * sp(4)), row),
                   (luma_x + sp(18) + int(t_n * sp(4)), row)], fill=HOODIE_ORANGE, width=1)

    # C38: REACHING gesture (Lee Tanaka brief Option B) — NOT pointing.
    # The arm extends toward screen but hand is OPEN, palm up, fingers slightly spread.
    # "I want to touch it" vs "I am showing you this" — desire, not display.
    # Shoulder rolled forward on screen side (Lee brief: "shoulder drops/rolls forward").
    arm_shoulder_x = luma_x - sp(10) + lean_offset  # screen-side shoulder rolled forward
    arm_shoulder_y = torso_top + sp(25)              # shoulder slightly higher (forward roll)
    arm_target_x = facing_monitor_x - sp(10)         # reach toward screen, not past it
    arm_target_y = torso_top + sp(45)                # arm at mid height — reaching
    elbow_x = (arm_shoulder_x + arm_target_x) // 2 + sp(16)
    elbow_y = arm_shoulder_y - sp(32)
    for seg in [(arm_shoulder_x, arm_shoulder_y, elbow_x, elbow_y),
                (elbow_x, elbow_y, arm_target_x, arm_target_y)]:
        draw.line([seg[:2], seg[2:]], fill=CYAN_SKIN, width=sp(18))

    hand_cx = arm_target_x
    hand_cy = arm_target_y
    # Open palm toward screen — wrist rotated, palm facing up/toward screen
    draw.ellipse([hand_cx - sp(14), hand_cy - sp(10), hand_cx + sp(14), hand_cy + sp(18)], fill=CYAN_SKIN)

    # Fingers spread open (reaching, not pointing) — 4 fingers fanning upward/toward screen
    # Each finger fans slightly from palm center, slightly spread
    finger_offsets = [(-sp(12), -sp(20)), (-sp(6), -sp(24)), (sp(2), -sp(24)), (sp(10), -sp(20))]
    for fdx, fdy in finger_offsets:
        draw.line([(hand_cx + fdx // 2, hand_cy - sp(4)),
                   (hand_cx + fdx, hand_cy + fdy)],
                  fill=CYAN_SKIN, width=sp(6))
    # Thumb at side
    draw.line([(hand_cx - sp(12), hand_cy + sp(6)),
               (hand_cx - sp(22), hand_cy - sp(4))],
              fill=CYAN_SKIN, width=sp(6))
    draw.ellipse([hand_cx - sp(10), hand_cy - sp(10), hand_cx + sp(10), hand_cy + sp(10)],
                 outline=(0, 180, 200), width=sp(2))

    # CRT glow on open palm — small warm-cyan halo showing proximity to screen
    rng_palm = random.Random(91)
    for _ in range(5):
        px_g = hand_cx + rng_palm.randint(-sp(14), sp(14))
        py_g = hand_cy + rng_palm.randint(-sp(10), sp(6))
        ps_g = rng_palm.choice([2, 3])
        draw.rectangle([px_g, py_g, px_g + ps_g, py_g + ps_g],
                       fill=rng_palm.choice([ELEC_CYAN, (180, 240, 255)]))

    return {
        "head_cx": head_cx, "head_cy": head_cy,
        "hand_cx": hand_cx, "hand_cy": hand_cy,
        "torso_top": torso_top,
    }


def draw_luma_head_v006(img, draw, cx, cy, scale, byte_cx_target):
    """
    C38 SIGHT-LINE VERSION: Luma's head turned toward Byte/screen.
    Key changes from v005 draw_luma_head():
    - Eyes: both eyes shifted RIGHT (toward byte_cx_target direction)
      left eye = screen-side, slightly wider (full wonder)
      right eye = away side, slightly squinted (tension)
    - Brow: LEFT (screen-side) brow raised HIGH (surprise/wonder)
             RIGHT (away-side) brow slightly furrowed (uncertainty/intensity)
    - Mouth: slightly open O of shock (was closed grin)
    - Face orientation: subtle rightward shift in feature placement confirms head turn
    - Hair: 4 wild strands spraying in different directions (reckless energy)
    """
    def p(n): return int(n * scale * min(SX, SY))
    head_r = p(72)

    # Fill head with skin gradient
    for row in range(cy - head_r, cy + head_r):
        t_y = (row - cy) / max(1, head_r)
        rx_row = int(head_r * math.sqrt(max(0, 1 - t_y * t_y)))
        if rx_row < 1:
            continue
        for col in range(cx - rx_row, cx + rx_row + 1):
            t_x = (col - cx) / max(1, rx_row)
            w_f = 0.5 + 0.5 * t_x
            r_v = int(SKIN[0] * (1 - w_f) + SKIN_HL[0] * w_f)
            g_v = int(SKIN[1] * (1 - w_f) + SKIN_HL[1] * w_f)
            b_v = int(SKIN[2] * (1 - w_f) + SKIN_HL[2] * w_f)
            draw.point((col, row), fill=(r_v, g_v, b_v))

    # Wobble outline on head silhouette
    num_pts = 20
    head_pts = []
    for i in range(num_pts):
        angle = (2 * math.pi * i / num_pts) - math.pi / 2
        hx = cx + head_r * math.cos(angle)
        hy = cy + head_r * math.sin(angle)
        head_pts.append((hx, hy))
    wobble_polygon(draw, head_pts, color=LINE, width=sp(3),
                   amplitude=sp(2), frequency=5, seed=101, fill=None)

    # Variable stroke arcs around head perimeter (8-arc technique)
    for arc_i in range(8):
        start_angle = (2 * math.pi * arc_i / 8) - math.pi / 2
        end_angle   = (2 * math.pi * (arc_i + 1) / 8) - math.pi / 2
        a_p1 = (cx + (head_r + sp(1)) * math.cos(start_angle),
                cy + (head_r + sp(1)) * math.sin(start_angle))
        a_p2 = (cx + (head_r + sp(1)) * math.cos(end_angle),
                cy + (head_r + sp(1)) * math.sin(end_angle))
        variable_stroke(img, a_p1, a_p2,
                        max_width=sp(5), min_width=sp(1),
                        color=LINE, seed=300 + arc_i)
    draw = ImageDraw.Draw(img)  # Refresh after variable_stroke

    # Hair base (dark crown)
    draw.chord([cx - head_r, cy - head_r + p(20), cx + head_r, cy + p(20)],
               start=190, end=350, fill=HAIR_COLOR)
    draw.arc([cx - head_r, cy - head_r + p(20), cx + head_r, cy + p(20)],
             start=190, end=350, fill=LINE, width=p(4))

    # ─── C38: EYES — turned toward screen (byte_cx_target is to the right) ──────
    # In v005: lex=cx-p(26), rex=cx+p(28), pupils slightly right-shifted on rex
    # In v006: shift both eye centers rightward (head is turned right)
    #   Left eye (screen-side): cx + p(4) — shifted right toward screen
    #   Right eye (away-side): cx + p(38) — further right, slightly squinted
    # Pupil direction: both pupils shifted strongly right toward byte_cx_target

    EYE_W_C = (242, 240, 248)
    EYE_IRIS = (58, 32, 18)
    EYE_PUP  = (20, 12, 8)

    # Screen-side eye (left eye in face, but turned toward right/screen)
    # Wider — full wonder/surprise on the side facing what she sees
    lex = cx + p(4)   # shifted right (head turned right)
    ley = cy - p(10)
    ew  = int(head_r * 0.22)  # canonical ew = HR * 0.22
    # Screen-side eye: slightly taller (wonder — wider open)
    leh = p(34)  # was p(30) — taller for surprise
    draw.ellipse([lex - ew, ley - leh, lex + ew, ley + leh], fill=EYE_W_C, outline=LINE, width=sp(2))
    iris_r = p(15)
    draw.chord([lex - iris_r, ley - iris_r + p(2), lex + iris_r, ley + iris_r + p(2)],
               start=15, end=345, fill=EYE_IRIS)
    draw.ellipse([lex - p(9), ley - p(7), lex + p(9), ley + p(9)], fill=EYE_PUP)
    # Highlight/catch-light: positioned toward screen side (right)
    draw.ellipse([lex + p(2), ley - p(10), lex + p(10), ley - p(2)], fill=EYE_W_C)
    draw.arc([lex - ew, ley - leh, lex + ew, ley + leh], start=200, end=340, fill=LINE, width=p(4))

    # Away-side eye (right eye in face) — slightly squinted (intensity)
    rex = cx + p(38)   # shifted right (head turned)
    rey = cy - p(8)
    reh = p(22)  # slightly squinted (was p(26))
    draw.ellipse([rex - ew, rey - reh, rex + ew, rey + reh], fill=EYE_W_C, outline=LINE, width=sp(2))
    draw.chord([rex - iris_r, rey - iris_r + p(2), rex + iris_r, rey + iris_r + p(2)],
               start=15, end=345, fill=EYE_IRIS)
    # Away-side pupil also shifted toward screen (strong rightward gaze)
    pupil_shift = p(8)  # stronger shift (was p(5)) — both eyes tracking right/Byte
    draw.ellipse([rex - p(9) + pupil_shift, rey - p(7), rex + p(9) + pupil_shift, rey + p(9)], fill=EYE_PUP)
    draw.ellipse([rex + p(2) + pupil_shift, rey - p(10), rex + p(10) + pupil_shift, rey - p(2)], fill=EYE_W_C)
    draw.arc([rex - ew, rey - reh, rex + ew, rey + reh], start=200, end=340, fill=LINE, width=p(4))
    # Also shift left eye pupil strongly toward screen
    draw.ellipse([lex - p(9) + pupil_shift, ley - p(7), lex + p(9) + pupil_shift, ley + p(9)], fill=EYE_PUP)

    # ─── C38: BROWS — surprise/wonder asymmetry ──────────────────────────────
    # Screen-side (left) brow: RAISED HIGH — surprise/wonder (eyebrow up)
    l_brow = [
        (lex - p(30), ley - p(54)),  # outer left: higher than v005 (was -p(42))
        (lex - p(5),  ley - p(62)),  # peak: significantly raised (was -p(52))
        (lex + p(22), ley - p(46)),  # inner right: pulled up-inward
    ]
    draw.line(l_brow, fill=HAIR_COLOR, width=p(6))  # thicker brow (more readable energy)

    # Away-side (right) brow: DOUBT VARIANT — inner-corner kink (Lee Tanaka brief)
    # Inner corner (nose side) dips DOWN = corrugator kink = "not trusting the conclusion"
    # Outer corner slightly higher = brow arches away from nose = DOUBT, not anger
    r_brow = [
        (rex - p(22), rey - p(38)),  # outer: moderate height (slightly arched outward)
        (rex - p(5),  rey - p(34)),  # mid: descends toward nose
        (rex + p(26), rey - p(26)),  # inner corner (nose-side): LOWEST — kink down
    ]
    draw.line(r_brow, fill=HAIR_COLOR, width=p(5))

    # Nose
    draw.ellipse([cx - p(8) + p(4), cy + p(8), cx - p(2) + p(4), cy + p(14)], fill=SKIN_SH)
    draw.ellipse([cx + p(2) + p(4), cy + p(8), cx + p(8) + p(4), cy + p(14)], fill=SKIN_SH)

    # ─── C38: MOUTH — closed / barely open (Lee Tanaka brief spec) ──────────
    # "Closed or barely open — held, not performing."
    # This is the NOTICING base mouth: lips slightly parted, held breath.
    # NOT a grin, NOT an O of shock. The jaw is still. The mouth is waiting.
    # A barely-parted line with a tiny shadow of opening at the center.
    m_off = p(2)  # slight rightward shift (head turn toward screen)
    # Closed-ish horizontal mouth with slight uptick on screen-side (wonder, not smile)
    draw.arc([cx - p(34) + m_off, cy + p(18), cx + p(34) + m_off, cy + p(52)],
             start=8, end=172, fill=LINE, width=p(3))
    # Inner fill (pale lip interior — barely parted)
    draw.chord([cx - p(30) + m_off, cy + p(22), cx + p(30) + m_off, cy + p(48)],
               start=10, end=170, fill=(240, 212, 190))
    # Thin dark parting line at center — "held breath" detail
    draw.line([(cx - p(10) + m_off, cy + p(34)), (cx + p(10) + m_off, cy + p(34))],
              fill=(160, 100, 60), width=p(1))

    # Blush — warm peach
    blush_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    blush_draw  = ImageDraw.Draw(blush_layer)
    blush_draw.ellipse([cx - head_r + p(6), cy + p(4), cx - head_r + p(62), cy + p(40)],
                       fill=(*BLUSH_LEFT, 80))
    blush_draw.ellipse([cx + head_r - p(62), cy + p(4), cx + head_r - p(6), cy + p(40)],
                       fill=(*BLUSH_RIGHT, 80))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, blush_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)  # Refresh after paste

    # ─── C38: HAIR — screen-side forward curl (Lee Tanaka brief spec) ────────
    # "If she's leaning toward the screen, the hair leads. The outer curl of the
    # screen-side hair should be at a slightly steeper angle toward the screen."
    # Screen side = RIGHT (Luma's left, our right) — hair pulled forward-right.

    # Strand 1: left/upper arc (away-side — floats back, counterweight)
    draw.arc([cx - p(60), cy - p(195), cx - p(10), cy - p(140)],
             start=30, end=200, fill=HAIR_COLOR, width=p(8))
    # Strand 2: screen-side arc — pulled FORWARD toward CRT, steeper angle
    # Rotated ~8° more toward screen vs v005 (arc start/end shift)
    draw.arc([cx, cy - p(185), cx + p(70), cy - p(115)],
             start=330, end=185, fill=HAIR_COLOR, width=p(7))
    # Strand 3: crown upper tuft — vertical energy (reckless energy upward spike)
    draw.arc([cx - p(20), cy - p(205), cx + p(20), cy - p(155)],
             start=225, end=355, fill=HAIR_COLOR, width=p(6))
    # Strand 4: screen-side secondary wisp — fine trailing strand forward
    # (2nd layer of screen-pull — gravity of attention)
    draw.arc([cx + p(18), cy - p(170), cx + p(68), cy - p(125)],
             start=290, end=135, fill=HAIR_COLOR, width=p(4))

    # Collar
    collar_offset = p(6)
    draw.ellipse([cx - p(90) + collar_offset, cy + head_r + p(10),
                  cx + p(90) + collar_offset, cy + head_r + p(80)], fill=HOODIE_ORANGE)
    draw.arc([cx - p(90) + collar_offset, cy + head_r + p(10),
              cx + p(90) + collar_offset, cy + head_r + p(80)],
             start=180, end=360, fill=LINE, width=p(3))

    return draw, head_r


def draw_byte(draw, emerge_cx, emerge_cy, emerge_rx, emerge_ry, luma_hand_x, luma_hand_y):
    byte_cx = emerge_cx
    byte_cy = emerge_cy - int(emerge_ry * 0.20)
    byte_rx = int(emerge_rx * 0.78)
    byte_ry = int(emerge_ry * 0.80)

    for i in range(3):
        dist_rx = byte_rx + sp(12) + i * sp(10)
        dist_ry = byte_ry + sp(8)  + i * sp(7)
        draw.ellipse([byte_cx - dist_rx, byte_cy - dist_ry,
                      byte_cx + dist_rx, byte_cy + dist_ry],
                     outline=(0, 168 + i * 20, 180 + i * 18), width=sp(2))

    # Byte body — canonical BYTE_TEAL
    draw.ellipse([byte_cx - byte_rx, byte_cy - byte_ry,
                  byte_cx + byte_rx, byte_cy + byte_ry], fill=BYTE_TEAL)

    hl_rx = int(byte_rx * 0.5)
    hl_ry = int(byte_ry * 0.4)
    draw_filled_glow(draw, byte_cx - int(byte_rx * 0.2), byte_cy - int(byte_ry * 0.25),
                     hl_rx, hl_ry, glow_rgb=(0, 240, 255), bg_rgb=BYTE_TEAL, steps=6)

    sh_rx = int(byte_rx * 0.7)
    sh_ry = int(byte_ry * 0.35)
    draw_filled_glow(draw, byte_cx, byte_cy + int(byte_ry * 0.45),
                     sh_rx, sh_ry, glow_rgb=(0, 100, 130), bg_rgb=BYTE_TEAL, steps=5)

    VOID_POCKET = (14, 14, 30)
    submerge_y = byte_cy + int(byte_ry * 0.50)
    screen_top = emerge_cy + int(emerge_ry * 0.20)
    if submerge_y < screen_top:
        submerge_y = screen_top
    for row_offset in range(0, int(byte_ry * 0.38), sp(4)):
        y_row = submerge_y + row_offset
        t_fade = row_offset / max(1, int(byte_ry * 0.38))
        fade_rx = int(byte_rx * (1 - t_fade * 0.3))
        col = (
            int(VOID_POCKET[0] * t_fade + BYTE_TEAL[0] * (1 - t_fade)),
            int(VOID_POCKET[1] * t_fade + BYTE_TEAL[1] * (1 - t_fade)),
            int(VOID_POCKET[2] * t_fade + BYTE_TEAL[2] * (1 - t_fade)),
        )
        draw.line([(byte_cx - fade_rx, y_row), (byte_cx + fade_rx, y_row)], fill=col, width=sp(4))

    underbody_cx = byte_cx
    underbody_cy = byte_cy + int(byte_ry * 0.55)
    screen_glow_rx = int(byte_rx * 0.80)
    screen_glow_ry = int(byte_ry * 0.30)
    draw_filled_glow(draw, underbody_cx, underbody_cy,
                     screen_glow_rx, screen_glow_ry,
                     glow_rgb=ELEC_CYAN, bg_rgb=BYTE_TEAL, steps=8)

    draw_amber_outline(draw, byte_cx, byte_cy, byte_rx, byte_ry, width=sp(3))

    eye_size = max(sp(8), int(byte_rx * 0.22))
    lex_b = byte_cx - int(byte_rx * 0.30)
    ley_b = byte_cy - int(byte_ry * 0.12)
    draw.rectangle([lex_b - eye_size // 2, ley_b - eye_size,
                    lex_b + eye_size // 2, ley_b + eye_size // 3], fill=ELEC_CYAN)
    draw.rectangle([lex_b - eye_size // 2, ley_b + eye_size // 2,
                    lex_b + eye_size // 2, ley_b + eye_size], fill=ELEC_CYAN)

    rex_b = byte_cx + int(byte_rx * 0.30)
    rey_b = byte_cy - int(byte_ry * 0.12)
    r_eye_w = int(byte_rx * 0.36)
    r_eye_h = int(byte_ry * 0.36)
    draw.ellipse([rex_b - r_eye_w, rey_b - r_eye_h, rex_b + r_eye_w, rey_b + r_eye_h],
                 fill=(240, 240, 245), outline=LINE, width=sp(2))
    pupil_r = int(r_eye_w * 0.55)
    draw.ellipse([rex_b - pupil_r - sp(4), rey_b - pupil_r, rex_b + pupil_r - sp(4), rey_b + pupil_r], fill=LINE)
    draw.ellipse([rex_b - int(r_eye_w * 0.2) - sp(4), rey_b - int(r_eye_h * 0.4),
                  rex_b + int(r_eye_w * 0.1) - sp(4), rey_b], fill=ELEC_CYAN)

    scar_x = byte_cx + int(byte_rx * 0.10)
    scar_y = byte_cy - int(byte_ry * 0.30)
    draw.line([(scar_x, scar_y), (scar_x + int(byte_rx * 0.18), scar_y + int(byte_ry * 0.22))],
              fill=SCAR_MAG, width=sp(3))
    draw.line([(scar_x + int(byte_rx * 0.06), scar_y + int(byte_ry * 0.08)),
               (scar_x + int(byte_rx * 0.24), scar_y + int(byte_ry * 0.16))],
              fill=SCAR_MAG, width=sp(2))

    arm_start_x = byte_cx - byte_rx
    arm_start_y = byte_cy + int(byte_ry * 0.10)
    tendril_pts = []
    target_x = luma_hand_x
    target_y = luma_hand_y
    steps = 20
    for i in range(steps + 1):
        t = i / steps
        cp1x = arm_start_x + int((target_x - arm_start_x) * 0.33)
        cp1y = arm_start_y - int(byte_ry * 0.5)
        px_t = int((1-t)**2 * arm_start_x + 2*(1-t)*t * cp1x + t**2 * target_x)
        py_t = int((1-t)**2 * arm_start_y + 2*(1-t)*t * cp1y + t**2 * target_y)
        tendril_pts.append((px_t, py_t))
    for i in range(len(tendril_pts) - 1):
        thickness = max(sp(2), int(sp(8) * (1 - i / len(tendril_pts))))
        draw.line([tendril_pts[i], tendril_pts[i+1]], fill=BYTE_TEAL, width=thickness)
    if tendril_pts:
        tx, ty = tendril_pts[-1]
        draw.ellipse([tx - sp(8), ty - sp(8), tx + sp(8), ty + sp(8)], fill=ELEC_CYAN)

    gap_cx = (tendril_pts[-1][0] + luma_hand_x) // 2 if tendril_pts else luma_hand_x - sp(40)
    gap_cy = (tendril_pts[-1][1] + luma_hand_y) // 2 if tendril_pts else luma_hand_y
    draw_filled_glow(draw, gap_cx, gap_cy, rx=sx(55), ry=sy(38),
                     glow_rgb=(180, 255, 255), bg_rgb=(40, 30, 50), steps=10)
    rng_gap = random.Random(77)
    for _ in range(18):
        spx = gap_cx + rng_gap.randint(-sx(52), sx(52))
        spy = gap_cy + rng_gap.randint(-sy(32), sy(32))
        sps = rng_gap.choice([2, 3, 4])
        spc = rng_gap.choice([ELEC_CYAN, STATIC_WHITE, (180, 255, 255)])
        draw.rectangle([spx, spy, spx + sps, spy + sps], fill=spc)


def draw_lighting_overlay(img, lamp_x, lamp_y, monitor_cx, monitor_cy):
    base_wall = (212, 146, 58)
    warm_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    warm_draw  = ImageDraw.Draw(warm_layer)
    lamp_glow_cx = lamp_x + sx(32)
    lamp_glow_cy = lamp_y + sy(int(1080 * 0.35))
    for step in range(14, 0, -1):
        t = step / 14
        rx  = int(W * 0.30 * t)
        ry  = int(H * 0.55 * t)
        alpha = int(70 * (1 - t))
        warm_draw.ellipse([lamp_glow_cx - rx, lamp_glow_cy - ry,
                           lamp_glow_cx + rx, lamp_glow_cy + ry],
                          fill=(*SOFT_GOLD, alpha))
    warm_np = warm_layer.crop((0, 0, W // 2, H))
    base_left  = img.crop((0, 0, W // 2, H)).convert("RGBA")
    composited_left = Image.alpha_composite(base_left, warm_np)
    img.paste(composited_left.convert("RGB"), (0, 0))

    cold_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cold_draw  = ImageDraw.Draw(cold_layer)
    for step in range(14, 0, -1):
        t = step / 14
        rx  = int(W * 0.55 * t)
        ry  = int(H * 0.65 * t)
        alpha = int(60 * (1 - t))
        cold_draw.ellipse([monitor_cx - rx, monitor_cy - ry,
                           monitor_cx + rx, monitor_cy + ry],
                          fill=(*ELEC_CYAN, alpha))
    split_x = W // 2 - sx(80)
    cold_np    = cold_layer.crop((split_x, 0, W, H))
    base_right = img.crop((split_x, 0, W, H)).convert("RGBA")
    composited_right = Image.alpha_composite(base_right, cold_np)
    img.paste(composited_right.convert("RGB"), (split_x, 0))
    return img


def draw_couch(draw, luma_cx, luma_base_y):
    couch_left  = sx(int(1920 * 0.16))
    couch_right = sx(int(1920 * 0.38))
    couch_y_bot = luma_base_y + sp(44)
    couch_y_top = luma_base_y - sp(40)

    # Wobble couch seat polygon (procedural quality — C29)
    seat_pts = [
        (couch_left,  couch_y_bot + sp(10)), (couch_left,  couch_y_bot - sp(60)),
        (couch_right, couch_y_top - sp(40)), (couch_right, couch_y_bot + sp(4)),
    ]
    wobble_polygon(draw, seat_pts, color=(70, 30, 14),
                   width=sp(3), amplitude=sp(2), frequency=4, seed=400,
                   fill=(107, 48, 24))

    mid_couch_x = (couch_left + couch_right) // 2
    draw.line([(mid_couch_x - sp(10), couch_y_bot - sp(20)), (mid_couch_x, couch_y_top - sp(30))],
              fill=(80, 36, 14), width=sp(2))

    # Wobble couch back
    back_left_inner = sx(int(1920 * 0.22))
    back_pts = [
        (couch_left, couch_y_bot - sp(60)), (couch_left, couch_y_bot - sp(150)),
        (back_left_inner, couch_y_top - sp(120)), (back_left_inner, couch_y_top - sp(50)),
    ]
    wobble_polygon(draw, back_pts, color=(80, 40, 16),
                   width=sp(2), amplitude=sp(2), frequency=3, seed=401,
                   fill=(128, 60, 28))

    arm_pts = [
        (couch_right, couch_y_bot + sp(4)), (couch_right, couch_y_bot - sp(70)),
        (couch_right + sp(40), couch_y_bot - sp(60)), (couch_right + sp(40), couch_y_bot + sp(14)),
    ]
    wobble_polygon(draw, arm_pts, color=(80, 36, 14),
                   width=sp(2), amplitude=sp(1), frequency=3, seed=402,
                   fill=(115, 52, 26))

    draw.line([(couch_left, couch_y_bot - sp(60)), (couch_left, couch_y_bot + sp(10))],
              fill=SOFT_GOLD, width=sp(4))


def generate():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    img = Image.new("RGB", (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # STEP 1: Background + ghost Byte
    bg_data = draw_background(draw, img)
    draw = ImageDraw.Draw(img)  # Refresh after ghost paste operations
    scr_x0 = bg_data["scr_x0"]; scr_y0 = bg_data["scr_y0"]
    scr_x1 = bg_data["scr_x1"]; scr_y1 = bg_data["scr_y1"]
    emerge_cx = bg_data["emerge_cx"]; emerge_cy = bg_data["emerge_cy"]
    emerge_rx = bg_data["emerge_rx"]; emerge_ry = bg_data["emerge_ry"]

    # STEP 2: Couch (with wobble polygon procedural quality)
    luma_cx     = sx(int(1920 * 0.29))
    luma_base_y = sy(int(1080 * 0.90))
    draw_couch(draw, luma_cx, luma_base_y)

    # STEP 3: Three-light atmospheric overlay (BEFORE characters)
    mw_x = bg_data["mw_x"]; mw_y = bg_data["mw_y"]
    mw_w = bg_data["mw_w"]; mw_h = bg_data["mw_h"]
    lamp_x_pos = sx(int(1920 * 0.40))
    lamp_y_pos = bg_data["ceiling_y"] + sy(18)
    monitor_cx_pos = mw_x + mw_w // 2
    monitor_cy_pos = mw_y + mw_h // 2
    img = draw_lighting_overlay(img,
                                lamp_x=lamp_x_pos, lamp_y=lamp_y_pos,
                                monitor_cx=monitor_cx_pos, monitor_cy=monitor_cy_pos)
    draw = ImageDraw.Draw(img)

    # STEP 4: Luma's Body
    arm_target_x = scr_x0 - sx(20)
    arm_target_y = emerge_cy + int(emerge_ry * 0.10)
    body_data = draw_luma_body(draw, luma_cx, luma_base_y, arm_target_x)

    # STEP 5: Luma's Head (C38 sight-line version)
    # C38: head_cx shifted further right toward screen (head turned toward CRT/Byte).
    # head_gaze_offset pushes the head cx toward CRT without disturbing body alignment.
    # head_cy: chin slightly down (Lee Tanaka brief: "chin 4-6 deg down — tracking in").
    head_cx_body = body_data["head_cx"]
    head_gaze_offset = sp(18)  # head turned right toward screen — additional rightward shift
    head_cx = head_cx_body + head_gaze_offset
    head_cy = body_data["head_cy"] + sp(6)  # chin down: tracking-in, focusing posture
    draw, head_r = draw_luma_head_v006(img, draw, head_cx, head_cy,
                                       scale=0.92,
                                       byte_cx_target=emerge_cx)

    # STEP 5b: Face lighting — warm lamp from upper-left (domestic real-world scene)
    add_face_lighting(
        img,
        face_center=(head_cx, head_cy),
        face_radius=(head_r, head_r),
        light_dir=(-1.0, -1.0),
        shadow_color=SKIN_SH,
        highlight_color=SKIN_HL,
        seed=500,
    )
    draw = ImageDraw.Draw(img)

    # STEP 5c: Rim light — cool CRT teal from right
    # C32 FIX preserved: char_cx=head_cx for character-relative mask
    add_rim_light(
        img,
        threshold=185,
        light_color=(0, 220, 232),
        width=sp(3),
        side="right",
        char_cx=head_cx,
    )
    draw = ImageDraw.Draw(img)

    # STEP 6: Byte (emerging from CRT)
    luma_hand_x = body_data["hand_cx"]
    luma_hand_y = body_data["hand_cy"]
    draw_byte(draw, emerge_cx, emerge_cy, emerge_rx, emerge_ry, luma_hand_x, luma_hand_y)

    # STEP 7: Top/bottom vignette
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

    # STEP 8: Title strip
    font_xs = load_font(11)
    draw.rectangle([0, H - 30, W, H], fill=(20, 12, 8))
    draw.text((10, H - 22),
              "LUMA & THE GLITCHKIN — Frame 01: The Discovery  |  C38 — sight-line + visual power v006",
              fill=(180, 150, 100), font=font_xs)

    # STEP 9: Size rule enforcement (<=1280px — already at 1280x720, no resize needed)
    if img.width > 1280 or img.height > 1280:
        img.thumbnail((1280, 1280), Image.LANCZOS)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  ({img.width}x{img.height})")
    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
