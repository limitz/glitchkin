#!/usr/bin/env python3
"""
LTG_TOOL_style_frame_01_discovery_v003.py
Style Frame 01 — The Discovery (Rendered Composite)
"Luma & the Glitchkin" — Cycle 13

Art Director: Alex Chen
Date: 2026-03-30
Cycle 13 changes (Alex Chen):
  - Ghost Byte ALPHA CALIBRATION FIX (Victoria Ashford B+→A+ P1):
    Ghost body alpha raised 55→90. Eye glint alphas raised 65–70→105.
    Calibrated for pitch conditions: 800–1000px wide projected frame.
    Alpha 55 was invisible at presentation scale. 90/105 are perceptible on first look.
  - Ghost screen RELOCATION: top-left monitor (monitor_specs[0]) removed.
    Warm amber lamp glow bleeds into that screen's contrast zone — ghost form was unreadable.
    Replaced: now mid-right (monitor_specs[3]) and top-right (monitor_specs[2]) only.
    Two ghosts instead of three. Two that land > three where one is lost.

Prior cycle history preserved below:

Cycle 12 changes (Alex Chen):
  - Mid-air transition element added. Screen pixel figures scaled 7px→15px.
Cycle 11 changes (Sam Kowalski):
  - HOODIE_AMBIENT arithmetic corrected. Overlay boundary analysis corrected.
Cycle 10 changes (Alex Chen):
  - Luma lean 28px→48px. Screen content added.
Cycle 9 changes (Alex Chen):
  - HOODIE_AMBIENT finalized. Couch scale fixed. Submerge/glow draw order fixed.
    Overlay draw order fixed (before characters, not after). False comment corrected.

Output: /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_discovery_v003.png
Usage: python3 LTG_TOOL_style_frame_01_discovery_v003.py
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH_V003 = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_discovery_v003.png"
W, H = 1920, 1080

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
# HOODIE_AMBIENT = CHAR-L-08 (#B36250) — corrected Cycle 10
HOODIE_AMBIENT  = (179,  98,  80)
JEANS           = ( 58,  90, 140)
JEANS_SH        = ( 38,  62, 104)
COUCH_BODY      = (107,  48,  24)
COUCH_BACK      = (128,  60,  28)
COUCH_ARM       = (115,  52,  26)
BLUSH_LEFT      = (220,  80,  50)
BLUSH_RIGHT     = (208,  72,  48)
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
        er  = max(1, int(rx * t))
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
    ceiling_y = int(H * 0.12)
    draw.rectangle([0, 0, W, ceiling_y], fill=(90, 55, 22))
    draw.line([(0, ceiling_y), (W, ceiling_y)], fill=(60, 36, 14), width=4)

    wall_top_y = ceiling_y
    wall_bot_y = int(H * 0.54)
    far_wall   = (228, 185, 120)
    base_wall  = (212, 146,  58)
    for y in range(wall_top_y, wall_bot_y):
        t = (y - wall_top_y) / max(1, wall_bot_y - wall_top_y)
        r_v = int(far_wall[0] + (base_wall[0] - far_wall[0]) * t)
        g_v = int(far_wall[1] + (base_wall[1] - far_wall[1]) * t)
        b_v = int(far_wall[2] + (base_wall[2] - far_wall[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r_v, g_v, b_v))

    draw.rectangle([0, int(H * 0.54), W, int(H * 0.75)], fill=(140, 90, 26))
    draw.line([(0, int(H * 0.54)), (W, int(H * 0.54))], fill=(100, 64, 18), width=3)
    draw.rectangle([0, int(H * 0.75), W, H], fill=(90, 56, 32))
    for y in range(int(H * 0.75), H, 28):
        draw.line([(0, y), (W, y)], fill=RUST_SHADOW, width=1)
    for y in range(int(H * 0.76), H, 56):
        draw.line([(0, y + 4), (W, y + 4)], fill=(110, 70, 42), width=1)

    # Monitor wall
    mw_x  = int(W * 0.50)
    mw_y  = ceiling_y + 5
    mw_w  = int(W * 0.46)
    mw_h  = int(H * 0.57)
    draw.rectangle([mw_x, mw_y, mw_x + mw_w, mw_y + mw_h], fill=(14, 10, 22))

    monitor_specs = [
        (mw_x +  40, mw_y +  20, 260, 150),   # [0] top-left — WARM ZONE (lamp bleed)
        (mw_x + 330, mw_y +  15, 320, 180),   # [1] top-center
        (mw_x + 680, mw_y +  28, 230, 140),   # [2] top-right — ghost
        (mw_x +  50, mw_y + 190, 280, 165),   # [3] mid-left — ghost
        (mw_x + 360, mw_y + 215, 300, 170),   # [4] mid-center
        (mw_x + 685, mw_y + 185, 210, 150),   # [5] mid-right
    ]

    cx_glow = mw_x + mw_w // 2
    cy_glow = mw_y + mw_h // 2
    draw_filled_glow(draw, cx_glow, cy_glow,
                     rx=720, ry=420,
                     glow_rgb=(0, 60, 100),
                     bg_rgb=(14, 10, 22),
                     steps=16)

    for mx, my, mw_s, mh_s in monitor_specs:
        draw.rectangle([mx - 6, my - 6, mx + mw_s + 6, my + mh_s + 6],
                       fill=(12, 10, 18), outline=(28, 22, 40), width=2)
        draw.rectangle([mx, my, mx + mw_s, my + mh_s], fill=ELEC_CYAN)
        cx_m = mx + mw_s // 2
        cy_m = my + mh_s // 2
        draw_filled_glow(draw, cx_m, cy_m,
                         mw_s // 2, mh_s // 2,
                         glow_rgb=(180, 255, 255),
                         bg_rgb=ELEC_CYAN,
                         steps=8)
        for sy in range(my + 3, my + mh_s, 5):
            draw.line([(mx, sy), (mx + mw_s, sy)], fill=(0, 168, 180), width=1)
        draw.line([(mx, my), (mx + mw_s, my)], fill=(40, 40, 60), width=2)

    # ── Cycle 13 FIX: Ghost Byte ALPHA CALIBRATION + RELOCATION ──────────────────
    # Victoria Ashford B+→A+ critique (Cycle 12):
    # - Alpha 55/60–70 was calibrated for close inspection; invisible at pitch scale.
    # - Top-left monitor (specs[0]) lost in warm lamp bleed — relocated.
    # Selection: specs[2] (top-right, fully in cold zone) + specs[3] (mid-left, away from lamp).
    # Two strong instances > three where one is unreadable.
    # Ghost body alpha: 55 → 90. Eye glint alpha: 65–70 → 105.
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
        # Ghost body: alpha 90 (was 55) — perceptible at pitch/projector scale
        ghost_draw.ellipse([g_cx - g_rx, g_cy - g_ry, g_cx + g_rx, g_cy + g_ry],
                           fill=(0, 53, 58, 90))
        # Eye glints: alpha 105 (was 65–70) — reads at presentation size
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

    # CRT screen
    crt_x  = mw_x + int(mw_w * 0.22)
    crt_y  = mw_y + int(mw_h * 0.08)
    crt_w  = int(mw_w * 0.52)
    crt_h  = int(mw_h * 0.62)
    draw.rectangle([crt_x - 10, crt_y - 10, crt_x + crt_w + 10, crt_y + crt_h + 20],
                   fill=(44, 36, 56), outline=(30, 24, 42), width=3)
    draw.rectangle([crt_x + crt_w // 3, crt_y + crt_h + 18,
                    crt_x + crt_w * 2 // 3, crt_y + crt_h + 40],
                   fill=(36, 28, 46))
    scr_pad = 24
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
    fig_x = scr_x0 + 14
    fig_y = scr_y0 + 12
    fig_color = (0, 80, 100)
    draw.rectangle([fig_x + 5, fig_y,      fig_x + 10, fig_y + 4],  fill=fig_color)
    draw.rectangle([fig_x + 3, fig_y + 4,  fig_x + 12, fig_y + 9],  fill=fig_color)
    draw.rectangle([fig_x,     fig_y + 4,  fig_x + 3,  fig_y + 6],  fill=fig_color)
    draw.rectangle([fig_x + 12, fig_y + 4, fig_x + 15, fig_y + 6],  fill=fig_color)
    draw.rectangle([fig_x + 3,  fig_y + 9, fig_x + 6,  fig_y + 14], fill=fig_color)
    draw.rectangle([fig_x + 9,  fig_y + 9, fig_x + 12, fig_y + 14], fill=fig_color)

    fig_x2 = scr_x1 - 30
    fig_y2 = scr_y0 + 10
    fig_color2 = (0, 60, 80)
    draw.rectangle([fig_x2 + 5, fig_y2,     fig_x2 + 10, fig_y2 + 4],  fill=fig_color2)
    draw.rectangle([fig_x2 + 3, fig_y2 + 4, fig_x2 + 12, fig_y2 + 9],  fill=fig_color2)
    draw.rectangle([fig_x2 - 6, fig_y2 + 4, fig_x2 + 3, fig_y2 + 6],   fill=fig_color2)
    draw.rectangle([fig_x2 + 12, fig_y2 + 4, fig_x2 + 15, fig_y2 + 6], fill=fig_color2)
    draw.rectangle([fig_x2 + 3,  fig_y2 + 9, fig_x2 + 6,  fig_y2 + 14], fill=fig_color2)
    draw.rectangle([fig_x2 + 9,  fig_y2 + 9, fig_x2 + 12, fig_y2 + 14], fill=fig_color2)

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
    draw.ellipse([emerge_cx - emerge_rx - 8, emerge_cy - emerge_ry - 8,
                  emerge_cx + emerge_rx + 8, emerge_cy + emerge_ry + 8],
                 outline=DEEP_CYAN, width=4)
    draw.ellipse([emerge_cx - emerge_rx - 14, emerge_cy - emerge_ry - 14,
                  emerge_cx + emerge_rx + 14, emerge_cy + emerge_ry + 14],
                 outline=(0, 80, 100), width=2)
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1], outline=DEEP_CYAN, width=5)
    for sy in range(scr_y0 + 4, scr_y1, 7):
        draw.line([(scr_x0, sy), (scr_x1, sy)], fill=(0, 168, 180), width=1)

    rng_confetti = random.Random(42)
    for _ in range(80):
        px = rng_confetti.randint(scr_x0 - 120, scr_x1 + 60)
        py = rng_confetti.randint(scr_y0 - 80, int(H * 0.75))
        ps = rng_confetti.choice([3, 4, 5, 6])
        pc = rng_confetti.choice([ELEC_CYAN, STATIC_WHITE, BYTE_TEAL, (0, 200, 220)])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)

    floor_glow_pts = [
        (crt_x,            int(H * 0.75)),
        (crt_x + crt_w,    int(H * 0.75)),
        (crt_x + crt_w + 160, H),
        (crt_x - 100,      H),
    ]
    draw.polygon(floor_glow_pts, fill=(0, 22, 38))
    draw_filled_glow(draw, mw_x - 20, mw_y + mw_h // 2,
                     rx=160, ry=220,
                     glow_rgb=(0, 40, 70),
                     bg_rgb=(180, 130, 60),
                     steps=10)

    # Window
    win_x0, win_y0 = 60, ceiling_y + 20
    win_x1, win_y1 = 340, ceiling_y + 260
    draw.rectangle([win_x0 - 30, win_y0 - 10, win_x0 + 14, win_y1 + 20], fill=(168, 108, 48))
    draw.rectangle([win_x1 - 14, win_y0 - 10, win_x1 + 30, win_y1 + 20], fill=(168, 108, 48))
    draw.rectangle([win_x0, win_y0, win_x1, win_y1], fill=SOFT_GOLD)
    draw.rectangle([win_x0, win_y0, win_x1, win_y1], outline=DEEP_COCOA, width=4)
    mid_win_x = (win_x0 + win_x1) // 2
    mid_win_y = (win_y0 + win_y1) // 2
    draw.line([(mid_win_x, win_y0), (mid_win_x, win_y1)], fill=DEEP_COCOA, width=3)
    draw.line([(win_x0, mid_win_y), (win_x1, mid_win_y)], fill=DEEP_COCOA, width=3)

    # Bookshelves
    shelf_x = int(W * 0.20)
    shelf_y = ceiling_y
    shelf_w = int(W * 0.28)
    shelf_h = int(H * 0.45)
    draw.rectangle([shelf_x, shelf_y, shelf_x + shelf_w, shelf_y + shelf_h], fill=SUNLIT_AMBER)
    book_colors = [TERRACOTTA, SAGE_GREEN, DUSTY_LAVENDER, OCHRE_BRICK,
                   RUST_SHADOW, (96, 144, 180), (184, 160, 100)]
    for row in range(shelf_y + 4, shelf_y + shelf_h, 50):
        draw.line([(shelf_x, row + 44), (shelf_x + shelf_w, row + 44)], fill=DEEP_COCOA, width=2)
        col_idx = 0
        bx = shelf_x + 8
        while bx + 20 < shelf_x + shelf_w:
            bw = rng.randint(18, 36)
            bc = book_colors[col_idx % len(book_colors)]
            draw.rectangle([bx, row + 4, bx + bw, row + 42], fill=bc)
            draw.line([(bx, row + 4), (bx, row + 42)], fill=DEEP_COCOA, width=1)
            bx += bw + 2
            col_idx += 1

    # Desk
    desk_y = int(H * 0.60)
    desk_x0 = mw_x - 80
    desk_x1 = W
    draw.rectangle([desk_x0, desk_y, desk_x1, desk_y + 70], fill=OCHRE_BRICK)
    draw.line([(desk_x0, desk_y), (desk_x1, desk_y)], fill=DEEP_COCOA, width=3)
    draw.rectangle([desk_x0 + 30, desk_y + 10, desk_x0 + 240, desk_y + 46],
                   fill=DUSTY_LAVENDER, outline=DEEP_COCOA, width=2)
    for ky in range(desk_y + 16, desk_y + 40, 10):
        for kx in range(desk_x0 + 38, desk_x0 + 234, 18):
            draw.rectangle([kx, ky, kx + 14, ky + 7], fill=(148, 135, 175))
    draw.rectangle([desk_x0 + 260, desk_y + 8, desk_x0 + 310, desk_y + 55],
                   fill=TERRACOTTA, outline=DEEP_COCOA, width=2)
    draw.arc([desk_x0 + 308, desk_y + 20, desk_x0 + 332, desk_y + 44],
             start=270, end=90, fill=DEEP_COCOA, width=3)
    cable_colors = [ELEC_CYAN, HOT_MAGENTA, CABLE_BRONZE, CABLE_DATA_CYAN]
    for ci, cc in enumerate(cable_colors):
        cx_s = desk_x0 + 40 + ci * 60
        cx_e = desk_x0 + 120 + ci * 80
        draw.arc([cx_s, desk_y + 50, cx_e, desk_y + 100], 0, 180, fill=cc, width=2)

    # Lamp
    lamp_x = int(W * 0.40)
    lamp_y = ceiling_y + 18
    draw_filled_glow(draw, lamp_x + 32, lamp_y + 50,
                     rx=180, ry=110,
                     glow_rgb=LAMP_PEAK,
                     bg_rgb=base_wall,
                     steps=12)
    draw.rectangle([lamp_x, lamp_y, lamp_x + 64, lamp_y + 86], fill=(245, 200, 66), outline=DEEP_COCOA, width=2)
    draw.ellipse([lamp_x + 12, lamp_y + 80, lamp_x + 52, lamp_y + 96], fill=SUNLIT_AMBER)
    draw_filled_glow(draw, lamp_x + 32, int(H * 0.85),
                     rx=120, ry=44,
                     glow_rgb=LAMP_PEAK,
                     bg_rgb=(90, 56, 32),
                     steps=10)

    # Cable clutter foreground
    draw.rectangle([0, int(H * 0.92), W, H], fill=(42, 26, 16))
    fg_cables = [
        (80,   460, int(H*0.935), 60,  ELEC_CYAN,          2),
        (240,  780, int(H*0.950), 85,  HOT_MAGENTA,        2),
        (420,  980, int(H*0.930), 44,  CABLE_BRONZE,       2),
        (600, 1200, int(H*0.960), 70,  CABLE_DATA_CYAN,    1),
        (840, 1500, int(H*0.940), 92,  SOFT_GOLD,          2),
        (980, 1720, int(H*0.952), 52,  CABLE_MAG_PURP,     1),
        (1200,1880, int(H*0.928), 74,  ELEC_CYAN,          2),
        (1460,1920, int(H*0.962), 38,  HOT_MAGENTA,        1),
        (100,  600, int(H*0.970), 32,  CABLE_NEUTRAL_PLUM, 1),
    ]
    for x0c, x1c, base_yc, arc_r, color, thickness in fg_cables:
        pts = []
        for s in range(31):
            t = s / 30
            px = int(x0c + (x1c - x0c) * t)
            sag = int(arc_r * 4 * t * (1 - t))
            pts.append((px, base_yc + sag))
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=color, width=thickness)

    # Mid-air transition element (Cycle 11 fix)
    air_rng = random.Random(77)
    zone_x0 = int(W * 0.40)
    zone_x1 = int(W * 0.50)
    zone_mid = (zone_x0 + zone_x1) // 2
    for _ in range(60):
        px = air_rng.randint(zone_x0 - 20, zone_x1 + 20)
        py = air_rng.randint(200, 700)
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
    }


def draw_luma_body(draw, luma_cx, luma_base_y, facing_monitor_x):
    luma_x = luma_cx
    y_base = luma_base_y
    lean_offset = 48

    draw.polygon([
        (luma_x - 48, y_base), (luma_x - 20, y_base),
        (luma_x - 15, y_base - 90), (luma_x - 50, y_base - 88),
    ], fill=JEANS)
    draw.polygon([
        (luma_x + 14, y_base), (luma_x + 44, y_base - 4),
        (luma_x + 46, y_base - 84), (luma_x + 12, y_base - 86),
    ], fill=JEANS)
    draw.polygon([
        (luma_x - 50, y_base - 88), (luma_x - 48, y_base),
        (luma_x - 34, y_base - 2), (luma_x - 32, y_base - 86),
    ], fill=JEANS_SH)
    draw.rectangle([luma_x - 60, y_base - 10, luma_x - 8, y_base + 22], fill=WARM_CREAM)
    draw.rectangle([luma_x - 62, y_base + 16, luma_x - 6, y_base + 26], fill=DEEP_COCOA)
    draw.rectangle([luma_x + 2, y_base - 10, luma_x + 58, y_base + 20], fill=WARM_CREAM)
    draw.rectangle([luma_x, y_base + 16, luma_x + 60, y_base + 26], fill=DEEP_COCOA)

    torso_height = 170
    torso_top    = y_base - 260
    torso_bot    = y_base - 90
    torso_half_w = 44
    for row in range(torso_bot, torso_top, -1):
        t_y = (torso_bot - row) / max(1, torso_bot - torso_top)
        row_lean = int(lean_offset * t_y)
        x_left   = luma_x - torso_half_w + row_lean
        x_right  = luma_x + torso_half_w + row_lean
        width    = x_right - x_left
        for col in range(x_left, x_right + 1):
            t_x = (col - x_left) / max(1, width)
            r_v = int(HOODIE_ORANGE[0] * (1 - t_x) + HOODIE_CYAN_LIT[0] * t_x)
            g_v = int(HOODIE_ORANGE[1] * (1 - t_x) + HOODIE_CYAN_LIT[1] * t_x)
            b_v = int(HOODIE_ORANGE[2] * (1 - t_x) + HOODIE_CYAN_LIT[2] * t_x)
            draw.point((col, row), fill=(r_v, g_v, b_v))

    draw.polygon([
        (luma_x - torso_half_w, torso_bot - 8), (luma_x - torso_half_w, torso_bot),
        (luma_x + torso_half_w, torso_bot), (luma_x + torso_half_w, torso_bot - 8),
    ], fill=HOODIE_AMBIENT)

    rng_px = random.Random(55)
    for i in range(7):
        ppx = luma_x - torso_half_w + lean_offset + rng_px.randint(4, torso_half_w * 2 - 8)
        ppy = torso_top + rng_px.randint(4, 30)
        pps = rng_px.choice([4, 6, 8])
        draw.rectangle([ppx, ppy, ppx + pps, ppy + pps], fill=ELEC_CYAN)

    head_cx = luma_x + lean_offset
    head_cy = torso_top - 70
    draw.rectangle([head_cx - 6, torso_top, head_cx + 6, torso_top + 30], fill=HOODIE_ORANGE)

    neck_pts = [
        (luma_x - 18 + lean_offset, torso_top + 2),
        (luma_x + 18 + lean_offset, torso_top + 2),
        (head_cx + 14, head_cy + 60),
        (head_cx - 14, head_cy + 60),
    ]
    for row in range(torso_top + 2, head_cy + 60):
        t_n = (row - (torso_top + 2)) / max(1, (head_cy + 60) - (torso_top + 2))
        t_x = (lean_offset - 18) + (lean_offset - 14) * t_n / 2
        draw.line([(luma_x - 18 + int(t_n * 4), row),
                   (luma_x + 18 + int(t_n * 4), row)], fill=HOODIE_ORANGE, width=1)

    # Warm lit arm
    arm_shoulder_x = luma_x - 20 + lean_offset
    arm_shoulder_y = torso_top + 30
    arm_target_x = facing_monitor_x
    arm_target_y = torso_top + 60
    elbow_x = (arm_shoulder_x + arm_target_x) // 2 + 20
    elbow_y = arm_shoulder_y - 40
    for seg in [(arm_shoulder_x, arm_shoulder_y, elbow_x, elbow_y),
                (elbow_x, elbow_y, arm_target_x, arm_target_y)]:
        draw.line([seg[:2], seg[2:]], fill=CYAN_SKIN, width=18)

    hand_cx = arm_target_x
    hand_cy = arm_target_y
    draw.ellipse([hand_cx - 14, hand_cy - 14, hand_cx + 14, hand_cy + 14], fill=CYAN_SKIN)
    draw.line([(hand_cx - 8, hand_cy - 10), (hand_cx - 14, hand_cy - 22)], fill=CYAN_SKIN, width=7)
    draw.line([(hand_cx, hand_cy - 12), (hand_cx + 2, hand_cy - 24)], fill=CYAN_SKIN, width=7)
    draw.line([(hand_cx + 8, hand_cy - 10), (hand_cx + 16, hand_cy - 20)], fill=CYAN_SKIN, width=7)
    draw.ellipse([hand_cx - 10, hand_cy - 10, hand_cx + 10, hand_cy + 10],
                 outline=(0, 180, 200), width=2)

    return {
        "head_cx": head_cx, "head_cy": head_cy,
        "hand_cx": hand_cx, "hand_cy": hand_cy,
    }


def draw_luma_head(draw, cx, cy, scale=1.0):
    def p(n): return int(n * scale)
    head_r = p(72)
    for row in range(cy - head_r, cy + head_r):
        t_y = (row - cy) / head_r
        rx = int(head_r * math.sqrt(max(0, 1 - t_y * t_y)))
        if rx < 1:
            continue
        for col in range(cx - rx, cx + rx + 1):
            t_x = (col - cx) / max(1, rx)
            w_f = 0.5 + 0.5 * t_x
            r_v = int(SKIN[0] * (1 - w_f) + SKIN_HL[0] * w_f)
            g_v = int(SKIN[1] * (1 - w_f) + SKIN_HL[1] * w_f)
            b_v = int(SKIN[2] * (1 - w_f) + SKIN_HL[2] * w_f)
            draw.point((col, row), fill=(r_v, g_v, b_v))
    draw.ellipse([cx - head_r, cy - head_r, cx + head_r, cy + head_r], outline=LINE, width=3)
    draw.chord([cx - head_r, cy - head_r + p(20), cx + head_r, cy + p(20)],
               start=190, end=350, fill=HAIR_COLOR)
    draw.arc([cx - head_r, cy - head_r + p(20), cx + head_r, cy + p(20)],
             start=190, end=350, fill=LINE, width=4)

    EYE_W_C = (242, 240, 248)
    EYE_IRIS = (58, 32, 18)
    EYE_PUP  = (20, 12, 8)
    lex = cx - p(26)
    ley = cy - p(10)
    rex = cx + p(28)
    rey = cy - p(8)
    ew  = p(18)
    leh = p(30)
    draw.ellipse([lex - ew, ley - leh, lex + ew, ley + leh], fill=EYE_W_C, outline=LINE, width=2)
    iris_r = p(15)
    draw.chord([lex - iris_r, ley - iris_r + p(2), lex + iris_r, ley + iris_r + p(2)],
               start=15, end=345, fill=EYE_IRIS)
    draw.ellipse([lex - p(9), ley - p(7), lex + p(9), ley + p(9)], fill=EYE_PUP)
    draw.ellipse([lex + p(4), ley - p(10), lex + p(12), ley - p(2)], fill=EYE_W_C)
    draw.arc([lex - ew, ley - leh, lex + ew, ley + leh], start=200, end=340, fill=LINE, width=4)

    reh = p(26)
    draw.ellipse([rex - ew, rey - reh, rex + ew, rey + reh], fill=EYE_W_C, outline=LINE, width=2)
    draw.chord([rex - iris_r, rey - iris_r + p(2), rex + iris_r, rey + iris_r + p(2)],
               start=15, end=345, fill=EYE_IRIS)
    pupil_shift = p(5)
    draw.ellipse([rex - p(9) + pupil_shift, rey - p(7), rex + p(9) + pupil_shift, rey + p(9)], fill=EYE_PUP)
    draw.ellipse([rex + p(4) + pupil_shift, rey - p(10), rex + p(12) + pupil_shift, rey - p(2)], fill=EYE_W_C)
    draw.arc([rex - ew, rey - reh, rex + ew, rey + reh], start=200, end=340, fill=LINE, width=4)
    draw.ellipse([lex - p(9) + pupil_shift, ley - p(7), lex + p(9) + pupil_shift, ley + p(9)], fill=EYE_PUP)

    l_brow = [(lex - p(30), ley - p(42)), (lex - p(5), ley - p(52)), (lex + p(22), ley - p(39))]
    draw.line(l_brow, fill=HAIR_COLOR, width=5)
    r_brow = [(rex - p(22), rey - p(34)), (rex - p(5), rey - p(40)), (rex + p(28), rey - p(32))]
    draw.line(r_brow, fill=HAIR_COLOR, width=5)

    draw.ellipse([cx - p(8), cy + p(8), cx - p(2), cy + p(14)], fill=SKIN_SH)
    draw.ellipse([cx + p(2), cy + p(8), cx + p(8), cy + p(14)], fill=SKIN_SH)

    m_off = -p(6)
    draw.arc([cx - p(45) + m_off, cy + p(18), cx + p(45) + m_off, cy + p(70)],
             start=5, end=175, fill=LINE, width=4)
    draw.chord([cx - p(42) + m_off, cy + p(22), cx + p(42) + m_off, cy + p(65)],
               start=7, end=173, fill=(250, 246, 238))
    draw.arc([cx - p(42) + m_off, cy + p(22), cx + p(42) + m_off, cy + p(65)],
             start=7, end=173, fill=LINE, width=2)

    base_img = draw._image
    blush_layer = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    blush_draw  = ImageDraw.Draw(blush_layer)
    blush_draw.ellipse([cx - head_r + p(6), cy + p(4), cx - head_r + p(62), cy + p(40)],
                       fill=(*BLUSH_LEFT, 80))
    blush_draw.ellipse([cx + head_r - p(62), cy + p(4), cx + head_r - p(6), cy + p(40)],
                       fill=(*BLUSH_RIGHT, 80))
    base_rgba = base_img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, blush_layer)
    base_img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(base_img)  # W004 fix (C32): refresh after paste

    draw.arc([cx - p(60), cy - p(195), cx - p(10), cy - p(140)], start=30, end=200, fill=HAIR_COLOR, width=8)
    draw.arc([cx - p(20), cy - p(190), cx + p(40), cy - p(130)], start=10, end=190, fill=HAIR_COLOR, width=7)

    collar_offset = p(6)
    draw.ellipse([cx - p(90) + collar_offset, cy + head_r + p(10),
                  cx + p(90) + collar_offset, cy + head_r + p(80)], fill=HOODIE_ORANGE)
    draw.arc([cx - p(90) + collar_offset, cy + head_r + p(10),
              cx + p(90) + collar_offset, cy + head_r + p(80)],
             start=180, end=360, fill=LINE, width=3)


def draw_byte(draw, emerge_cx, emerge_cy, emerge_rx, emerge_ry, luma_hand_x, luma_hand_y):
    byte_cx = emerge_cx
    byte_cy = emerge_cy - int(emerge_ry * 0.20)
    byte_rx = int(emerge_rx * 0.78)
    byte_ry = int(emerge_ry * 0.80)

    for i in range(3):
        dist_rx = byte_rx + 12 + i * 10
        dist_ry = byte_ry + 8 + i * 7
        draw.ellipse([byte_cx - dist_rx, byte_cy - dist_ry,
                      byte_cx + dist_rx, byte_cy + dist_ry],
                     outline=(0, 168 + i * 20, 180 + i * 18), width=2)

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
    for row_offset in range(0, int(byte_ry * 0.38), 4):
        y_row = submerge_y + row_offset
        t_fade = row_offset / max(1, int(byte_ry * 0.38))
        fade_rx = int(byte_rx * (1 - t_fade * 0.3))
        col = (
            int(VOID_POCKET[0] * t_fade + BYTE_TEAL[0] * (1 - t_fade)),
            int(VOID_POCKET[1] * t_fade + BYTE_TEAL[1] * (1 - t_fade)),
            int(VOID_POCKET[2] * t_fade + BYTE_TEAL[2] * (1 - t_fade)),
        )
        draw.line([(byte_cx - fade_rx, y_row), (byte_cx + fade_rx, y_row)], fill=col, width=4)

    underbody_cx = byte_cx
    underbody_cy = byte_cy + int(byte_ry * 0.55)
    screen_glow_rx = int(byte_rx * 0.80)
    screen_glow_ry = int(byte_ry * 0.30)
    draw_filled_glow(draw, underbody_cx, underbody_cy,
                     screen_glow_rx, screen_glow_ry,
                     glow_rgb=ELEC_CYAN, bg_rgb=BYTE_TEAL, steps=8)

    draw_amber_outline(draw, byte_cx, byte_cy, byte_rx, byte_ry, width=3)

    eye_size = max(8, int(byte_rx * 0.22))
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
                 fill=(240, 240, 245), outline=LINE, width=2)
    pupil_r = int(r_eye_w * 0.55)
    draw.ellipse([rex_b - pupil_r - 4, rey_b - pupil_r, rex_b + pupil_r - 4, rey_b + pupil_r], fill=LINE)
    draw.ellipse([rex_b - int(r_eye_w * 0.2) - 4, rey_b - int(r_eye_h * 0.4),
                  rex_b + int(r_eye_w * 0.1) - 4, rey_b], fill=ELEC_CYAN)

    scar_x = byte_cx + int(byte_rx * 0.10)
    scar_y = byte_cy - int(byte_ry * 0.30)
    draw.line([(scar_x, scar_y), (scar_x + int(byte_rx * 0.18), scar_y + int(byte_ry * 0.22))],
              fill=SCAR_MAG, width=3)
    draw.line([(scar_x + int(byte_rx * 0.06), scar_y + int(byte_ry * 0.08)),
               (scar_x + int(byte_rx * 0.24), scar_y + int(byte_ry * 0.16))],
              fill=SCAR_MAG, width=2)

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
        px = int((1-t)**2 * arm_start_x + 2*(1-t)*t * cp1x + t**2 * target_x)
        py = int((1-t)**2 * arm_start_y + 2*(1-t)*t * cp1y + t**2 * target_y)
        tendril_pts.append((px, py))
    for i in range(len(tendril_pts) - 1):
        thickness = max(2, int(8 * (1 - i / len(tendril_pts))))
        draw.line([tendril_pts[i], tendril_pts[i+1]], fill=BYTE_TEAL, width=thickness)
    if tendril_pts:
        tx, ty = tendril_pts[-1]
        draw.ellipse([tx - 8, ty - 8, tx + 8, ty + 8], fill=ELEC_CYAN)

    gap_cx = (tendril_pts[-1][0] + luma_hand_x) // 2 if tendril_pts else luma_hand_x - 40
    gap_cy = (tendril_pts[-1][1] + luma_hand_y) // 2 if tendril_pts else luma_hand_y
    draw_filled_glow(draw, gap_cx, gap_cy, rx=55, ry=38,
                     glow_rgb=(180, 255, 255), bg_rgb=(40, 30, 50), steps=10)
    rng_gap = random.Random(77)
    for _ in range(18):
        spx = gap_cx + rng_gap.randint(-52, 52)
        spy = gap_cy + rng_gap.randint(-32, 32)
        sps = rng_gap.choice([2, 3, 4])
        spc = rng_gap.choice([ELEC_CYAN, STATIC_WHITE, (180, 255, 255)])
        draw.rectangle([spx, spy, spx + sps, spy + sps], fill=spc)


def draw_lighting_overlay(img, W, H, lamp_x, lamp_y, monitor_cx, monitor_cy):
    warm_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    warm_draw  = ImageDraw.Draw(warm_layer)
    lamp_glow_cx = lamp_x + 32
    lamp_glow_cy = lamp_y + int(H * 0.35)
    for step in range(14, 0, -1):
        t   = step / 14
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
        t   = step / 14
        rx  = int(W * 0.55 * t)
        ry  = int(H * 0.65 * t)
        alpha = int(60 * (1 - t))
        cold_draw.ellipse([monitor_cx - rx, monitor_cy - ry,
                           monitor_cx + rx, monitor_cy + ry],
                          fill=(*ELEC_CYAN, alpha))
    cold_np    = cold_layer.crop((W // 2 - 80, 0, W, H))
    base_right = img.crop((W // 2 - 80, 0, W, H)).convert("RGBA")
    composited_right = Image.alpha_composite(base_right, cold_np)
    img.paste(composited_right.convert("RGB"), (W // 2 - 80, 0))
    # W004 fix (C32): no draw variable in scope here (uses local warm_draw/cold_draw only).
    # Caller must refresh draw = ImageDraw.Draw(img) after this call.
    return img


def draw_couch(draw, luma_cx, luma_base_y):
    couch_left  = int(W * 0.16)
    couch_right = int(W * 0.38)
    couch_y_bot = luma_base_y + 44
    couch_y_top = luma_base_y - 40
    seat_pts = [
        (couch_left,  couch_y_bot + 10), (couch_left,  couch_y_bot - 60),
        (couch_right, couch_y_top - 40), (couch_right, couch_y_bot + 4),
    ]
    draw.polygon(seat_pts, fill=(107, 48, 24))
    draw.polygon(seat_pts, outline=(70, 30, 14), width=3)
    mid_couch_x = (couch_left + couch_right) // 2
    draw.line([(mid_couch_x - 10, couch_y_bot - 20), (mid_couch_x, couch_y_top - 30)],
              fill=(80, 36, 14), width=2)
    back_left_inner = int(W * 0.22)
    back_pts = [
        (couch_left, couch_y_bot - 60), (couch_left, couch_y_bot - 150),
        (back_left_inner, couch_y_top - 120), (back_left_inner, couch_y_top - 50),
    ]
    draw.polygon(back_pts, fill=(128, 60, 28))
    draw.polygon(back_pts, outline=(80, 40, 16), width=2)
    arm_pts = [
        (couch_right, couch_y_bot + 4), (couch_right, couch_y_bot - 70),
        (couch_right + 40, couch_y_bot - 60), (couch_right + 40, couch_y_bot + 14),
    ]
    draw.polygon(arm_pts, fill=(115, 52, 26))
    draw.polygon(arm_pts, outline=(80, 36, 14), width=2)
    draw.line([(couch_left, couch_y_bot - 60), (couch_left, couch_y_bot + 10)],
              fill=SOFT_GOLD, width=4)


def generate():
    os.makedirs(os.path.dirname(OUTPUT_PATH_V003), exist_ok=True)

    img = Image.new("RGB", (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # STEP 1: Background + ghost Byte
    bg_data = draw_background(draw, img)
    scr_x0 = bg_data["scr_x0"]; scr_y0 = bg_data["scr_y0"]
    scr_x1 = bg_data["scr_x1"]; scr_y1 = bg_data["scr_y1"]
    emerge_cx = bg_data["emerge_cx"]; emerge_cy = bg_data["emerge_cy"]
    emerge_rx = bg_data["emerge_rx"]; emerge_ry = bg_data["emerge_ry"]

    # STEP 2: Couch
    luma_cx     = int(W * 0.29)
    luma_base_y = int(H * 0.90)
    draw_couch(draw, luma_cx, luma_base_y)

    # STEP 3: Three-light atmospheric overlay (BEFORE characters)
    mw_x = bg_data["mw_x"]; mw_y = bg_data["mw_y"]
    mw_w = bg_data["mw_w"]; mw_h = bg_data["mw_h"]
    lamp_x_pos = int(W * 0.40)
    lamp_y_pos = bg_data["ceiling_y"] + 18
    monitor_cx_pos = mw_x + mw_w // 2
    monitor_cy_pos = mw_y + mw_h // 2
    img = draw_lighting_overlay(img, W, H,
                                lamp_x=lamp_x_pos, lamp_y=lamp_y_pos,
                                monitor_cx=monitor_cx_pos, monitor_cy=monitor_cy_pos)
    draw = ImageDraw.Draw(img)

    # STEP 4: Luma's Body
    arm_target_x = scr_x0 - 20
    arm_target_y = emerge_cy + int(emerge_ry * 0.10)
    body_data = draw_luma_body(draw, luma_cx, luma_base_y, arm_target_x)

    # STEP 5: Luma's Head
    head_cx = body_data["head_cx"]
    head_cy = body_data["head_cy"]
    draw_luma_head(draw, head_cx, head_cy, scale=0.92)

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
    font_xs = load_font(16)
    draw.rectangle([0, H - 40, W, H], fill=(20, 12, 8))
    draw.text((20, H - 32),
              "LUMA & THE GLITCHKIN — Frame 01: The Discovery  |  Cycle 13 — Ghost Byte v003 (alpha calibrated)",
              fill=(180, 150, 100), font=font_xs)

    img.save(OUTPUT_PATH_V003, "PNG")
    print(f"Saved: {OUTPUT_PATH_V003}")
    return OUTPUT_PATH_V003


if __name__ == "__main__":
    generate()
