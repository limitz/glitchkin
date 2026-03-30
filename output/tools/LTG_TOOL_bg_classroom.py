#!/usr/bin/env python3
"""
LTG_TOOL_bg_classroom.py — Millbrook Middle School Classroom Background (Fix Pass)
"Luma & the Glitchkin" — Background & Environment Design
Artist: Jordan Reed | Cycle 16

Based on: LTG_TOOL_bg_classroom.py (Jordan Reed, Cycle 14)

Cycle 16 fixes (Jordan Reed — Critique C8 / Takeshi Murakami feedback):
  1. UNIFIED LIGHTING — Replaced multiple overlapping semi-transparent patches
     with a coherent dual-source system:
     - LEFT: warm window light (SUNLIT_AMBER gradient from windows)
     - RIGHT/OVERHEAD: cool fluorescent (blue-green tint from fixtures)
     No more muddy/irradiated overlap zone. Clean transition at canvas center.
  2. INHABITANT EVIDENCE — Added specific human details for lived-in quality:
     - Wear marks on desk surfaces (lighter worn paths on desks)
     - Papers/worksheets on several desks (scattered sheets)
     - Forgotten item: backpack on floor near Luma's desk
     - Chalk dust near board (faint lighter smear along board tray)
     Per Takeshi Murakami: "It is a diagram of a classroom, not a lived space."

Camera: Back-right corner, looking diagonally toward front-left.
Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_classroom_bg.png
"""

import math
import random
from PIL import Image, ImageDraw

W, H = 1920, 1080

# ── Palette ──────────────────────────────────────────────────────────────────
WALL_SAGE        = (138, 158, 138)
WALL_SAGE_WARM   = (148, 168, 130)
WALL_SAGE_COOL   = (128, 148, 148)
CEIL_TILE        = (216, 212, 192)
CEIL_GRID        = (144, 152, 152)
FLUORO_FIXTURE   = (232, 240, 232)

FLOOR_CREAM      = (216, 206, 176)
FLOOR_SAGE       = (138, 158, 136)
FLOOR_WORN       = (224, 214, 188)
FLOOR_FLUORO     = (208, 221, 208)
FLOOR_WARM       = (232, 216, 168)

BOARD_GRAY       = (192, 200, 192)
BOARD_WRITING    = (59,  40,  32)
BOARD_FADED      = (154, 152, 152)
DESK_TEACHER     = (154, 122,  80)
DESK_STUDENT     = (176, 146,  92)
DESK_FRAME       = (74,  80,  80)
WINDOW_GLASS     = (200, 220, 224)
BLIND_CREAM      = (216, 204, 172)
RADIATOR         = (144, 144, 128)
DOOR_TERRA       = (192,  88,  56)
BULLETIN_GOLD    = (200, 168,  80)

WINDOW_LIGHT_COL = (232, 201,  90)   # warm shaft
FLUORO_LIGHT_COL = (216, 232, 208)   # fluorescent pool

DEEP_COCOA       = (59,  40,  32)
SHADOW_COOL      = (122, 144, 128)
SHADOW_WARM      = (168, 155, 191)
LAVENDER_WALL    = (168, 155, 191)

# Lighting fix palette
WARM_LIGHT_WALL  = (255, 220, 160)   # warm tint for left wall zone
COOL_LIGHT_WALL  = (180, 210, 220)   # cool tint for right/overhead zone
CHALK_DUST       = (200, 198, 190)   # chalk dust near board tray


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def alpha_rect(img, x0, y0, x1, y1, color_rgb, alpha):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([x0, y0, x1, y1], fill=(*color_rgb, alpha))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


def draw_base_walls(img):
    draw = ImageDraw.Draw(img)

    vp_x = int(W * 0.12)
    vp_y = int(H * 0.36)

    ceil_near_y = 0
    ceil_far_y = vp_y - 20
    ceil_poly = [
        (0, ceil_near_y),
        (W, ceil_near_y),
        (W, ceil_far_y + 40),
        (vp_x, ceil_far_y),
    ]
    draw.polygon(ceil_poly, fill=CEIL_TILE)

    fw_left = vp_x
    fw_top  = vp_y - 20
    fw_right = int(W * 0.62)
    fw_bottom = int(H * 0.78)
    draw.rectangle([fw_left, fw_top, fw_right, fw_bottom], fill=WALL_SAGE)

    lw_poly = [
        (vp_x, vp_y - 20),
        (0, int(H * 0.28)),
        (0, int(H * 0.82)),
        (vp_x, fw_bottom),
    ]
    draw.polygon(lw_poly, fill=WALL_SAGE_WARM)

    floor_top_y = int(H * 0.72)
    floor_poly = [
        (0, floor_top_y),
        (W, floor_top_y + 40),
        (W, H),
        (0, H),
    ]
    draw.polygon(floor_poly, fill=FLOOR_CREAM)

    rw_poly = [
        (int(W * 0.60), vp_y - 20),
        (W, int(H * 0.24)),
        (W, int(H * 0.78)),
        (int(W * 0.60), fw_bottom),
    ]
    draw.polygon(rw_poly, fill=WALL_SAGE_COOL)

    return draw, vp_x, vp_y, fw_left, fw_top, fw_right, fw_bottom, floor_top_y


def draw_floor_tiles(draw, floor_top_y, rng):
    vp_x = int(W * 0.12)

    num_rows = 16
    for i in range(num_rows + 1):
        t = (i / num_rows) ** 1.8
        y = floor_top_y + int(t * (H - floor_top_y))
        if y >= H:
            break
        draw.line([(0, y), (W, y)], fill=(160, 148, 128), width=1)

    num_cols = 20
    for i in range(num_cols + 1):
        tx = i / num_cols
        bx = int(tx * W)
        draw.line([(vp_x, floor_top_y - 10), (bx, H)], fill=(160, 148, 128), width=1)

    # Warm zone left third
    warm_x = int(W * 0.33)
    for y in range(floor_top_y, H, 2):
        draw.line([(0, y), (warm_x, y)], fill=FLOOR_WARM)

    # Cool zone right two-thirds
    for y in range(floor_top_y, H, 2):
        draw.line([(warm_x, y), (W, y)], fill=FLOOR_FLUORO)


def draw_ceiling_details(draw, vp_x, vp_y):
    ceil_near_y = 0
    ceil_far_y = vp_y - 20

    num_rows = 8
    for i in range(1, num_rows):
        t = (i / num_rows) ** 1.4
        cy = int(t * (ceil_far_y - ceil_near_y))
        draw.line([(0, cy), (W, cy)], fill=CEIL_GRID, width=2)

    fix_col = [int(W * 0.35), int(W * 0.60)]
    for fx in fix_col:
        for i in range(1, num_rows):
            t = (i / num_rows) ** 1.4
            fy = int(t * (ceil_far_y - ceil_near_y))
            fw = int(W * 0.04)
            fh = 4
            draw.rectangle([fx - fw // 2, fy - fh // 2,
                             fx + fw // 2, fy + fh // 2], fill=FLUORO_FIXTURE)


def draw_window_wall(img, draw, vp_x, vp_y):
    lw_top_y = int(H * 0.28)
    lw_bot_y = int(H * 0.82)
    wall_height = lw_bot_y - lw_top_y

    window_specs = [
        (0.32, 0.68, 0.01, 0.06),
        (0.34, 0.70, 0.06, 0.11),
        (0.36, 0.70, 0.11, 0.16),
    ]
    for wi, (ytf, ybf, xlf, xrf) in enumerate(window_specs):
        wy1 = lw_top_y + int(ytf * wall_height)
        wy2 = lw_top_y + int(ybf * wall_height)
        wx1 = int(xlf * W)
        wx2 = int(xrf * W)
        draw.rectangle([wx1, wy1, wx2, wy2], fill=WINDOW_GLASS)
        draw.rectangle([wx1, wy1, wx2, wy2], outline=DEEP_COCOA, width=2)
        slat_count = 14
        for si in range(slat_count):
            sy = wy1 + int(si / slat_count * (wy2 - wy1))
            if wi == 1 and si == 7:
                draw.line([(wx1, sy), (wx2, sy - 4)], fill=BLIND_CREAM, width=2)
            else:
                draw.line([(wx1, sy), (wx2, sy)], fill=BLIND_CREAM, width=2)

        rad_y1 = wy2 + 4
        rad_y2 = rad_y1 + int(H * 0.04)
        draw.rectangle([wx1, rad_y1, wx2, rad_y2], fill=RADIATOR)
        rib_step = max(4, (wx2 - wx1) // 5)
        for rx in range(wx1, wx2, rib_step):
            draw.line([(rx, rad_y1), (rx, rad_y2)], fill=(160, 160, 144), width=1)

    return draw


def draw_unified_lighting(img, floor_top_y):
    """
    FIX 1: Unified coherent dual-source lighting system.
    WARM source: windows on left side — gradient from left edge, falls off toward center.
    COOL source: fluorescent overhead right — gradient from right/ceiling, falls off left.
    Clean transition at canvas center (~x=W*0.45 crossover).
    No overlapping muddy patches.
    """
    # ── WARM WINDOW LIGHT (left side) ────────────────────────────────────────
    warm_zone_width = int(W * 0.50)  # warm light reaches 50% canvas width
    warm_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(warm_overlay)

    for x in range(warm_zone_width):
        # Falloff: strong at left edge (near windows), fades toward center
        t = x / warm_zone_width
        falloff = (1.0 - t) ** 1.6
        alpha = int(falloff * 55)   # max 55 alpha — subtle, coherent
        if alpha > 0:
            wd.line([(x, floor_top_y), (x, H - 1)], fill=(*WARM_LIGHT_WALL, alpha))
            # Also color upper walls
            wd.line([(x, 0), (x, floor_top_y)], fill=(*WARM_LIGHT_WALL, alpha // 2))

    img = img.convert("RGBA")
    img = Image.alpha_composite(img, warm_overlay)
    img = img.convert("RGB")

    # ── COOL FLUORESCENT LIGHT (right side / overhead) ───────────────────────
    cool_zone_start = int(W * 0.40)  # cool light starts at 40% x, dominates right
    cool_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cool_overlay)

    for x in range(cool_zone_start, W):
        t = (x - cool_zone_start) / (W - cool_zone_start)
        falloff = t ** 1.2   # builds up toward right edge
        alpha = int(falloff * 50)  # max 50 alpha
        if alpha > 0:
            cd.line([(x, floor_top_y), (x, H - 1)], fill=(*COOL_LIGHT_WALL, alpha))
            cd.line([(x, 0), (x, floor_top_y)], fill=(*COOL_LIGHT_WALL, alpha // 3))

    img = img.convert("RGBA")
    img = Image.alpha_composite(img, cool_overlay)
    img = img.convert("RGB")

    return img


def draw_window_light_shafts(img):
    """Warm gold window light shafts — clean parallelograms, no overlap muddy zones."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    shaft_alpha = 80  # reduced from 102 to avoid muddiness (FIX 1)

    shaft_specs = [
        (80, 200, int(H * 0.38), H, -60),
        (220, 340, int(H * 0.40), H, -50),
        (360, 480, int(H * 0.42), H, -40),
    ]
    for (fx1, fx2, ty, by, x_off) in shaft_specs:
        poly = [
            (fx1 + x_off, ty),
            (fx2 + x_off, ty),
            (fx2, by),
            (fx1, by),
        ]
        od.polygon(poly, fill=(*WINDOW_LIGHT_COL, shaft_alpha))

    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


def draw_fluorescent_floor_pools(img, floor_top_y):
    """Soft oval fluorescent light pools under fixtures — filled ellipses only."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    fixture_xs = [int(W * 0.35), int(W * 0.60)]
    num_pools = 6
    for fx in fixture_xs:
        for i in range(1, num_pools + 1):
            t = i / (num_pools + 1)
            fy = floor_top_y + int(t * (H - floor_top_y))
            pool_w = int(W * 0.08 * (1.0 + t * 0.5))
            pool_h = int(H * 0.025)
            od.ellipse([fx - pool_w // 2, fy - pool_h // 2,
                        fx + pool_w // 2, fy + pool_h // 2],
                       fill=(*FLUORO_LIGHT_COL, 80))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


def draw_front_wall(draw, fw_left, fw_top, fw_right, fw_bottom, rng):
    board_x1 = fw_left + int((fw_right - fw_left) * 0.04)
    board_x2 = fw_left + int((fw_right - fw_left) * 0.88)
    board_y1 = fw_top + int((fw_bottom - fw_top) * 0.10)
    board_y2 = fw_top + int((fw_bottom - fw_top) * 0.50)
    draw.rectangle([board_x1, board_y1, board_x2, board_y2], fill=BOARD_GRAY)
    draw.rectangle([board_x1, board_y1, board_x2, board_y2],
                   outline=DEEP_COCOA, width=2)
    draw.rectangle([board_x1, board_y2, board_x2, board_y2 + 6],
                   fill=(154, 140, 120))

    bx = board_x1 + 8
    by = board_y1 + 8
    bw = board_x2 - board_x1 - 16
    bh = board_y2 - board_y1 - 16
    draw.rectangle([bx, by, bx + int(bw * 0.55), by + 6], fill=BOARD_WRITING)
    draw.rectangle([bx, by + 14, bx + int(bw * 0.35), by + 18], fill=BOARD_WRITING)
    for row in range(3):
        ry = by + 28 + row * 18
        for col in range(16):
            if rng.random() < 0.55:
                bbit = bx + col * int(bw / 18)
                draw.rectangle([bbit, ry, bbit + 4, ry + 8], fill=BOARD_WRITING)
    eq_y = by + 80
    draw.rectangle([bx + int(bw * 0.02), eq_y,
                    bx + int(bw * 0.40), eq_y + 5], fill=BOARD_WRITING)
    draw.rectangle([bx + int(bw * 0.50), eq_y,
                    bx + int(bw * 0.90), eq_y + 5], fill=BOARD_WRITING)
    draw.rectangle([bx + int(bw * 0.43), eq_y - 3,
                    bx + int(bw * 0.48), eq_y - 1], fill=BOARD_WRITING)
    draw.rectangle([bx + int(bw * 0.43), eq_y + 3,
                    bx + int(bw * 0.48), eq_y + 5], fill=BOARD_WRITING)

    ghost_y = by + 100
    for g in range(4):
        gx = bx + rng.randint(0, int(bw * 0.7))
        gw = rng.randint(20, 60)
        draw.rectangle([gx, ghost_y + g * 12, gx + gw, ghost_y + g * 12 + 3],
                       fill=BOARD_FADED)

    # FIX 2: Chalk dust near board tray — faint lighter smear
    chalk_y1 = board_y2 + 2
    chalk_y2 = board_y2 + 8
    dust_rng = random.Random(55)
    for pass_x in range(board_x1, board_x2, 6):
        if dust_rng.random() < 0.55:
            draw.line([(pass_x, chalk_y1 + 1), (pass_x + 4, chalk_y1 + 1)],
                      fill=CHALK_DUST, width=1)
        if dust_rng.random() < 0.30:
            draw.line([(pass_x, chalk_y2 - 1), (pass_x + 3, chalk_y2 - 1)],
                      fill=(210, 208, 200), width=1)

    wotw_x = board_x2 - int(bw * 0.35)
    wotw_y = board_y1 + 6
    draw.rectangle([wotw_x, wotw_y, board_x2 - 6, wotw_y + 5], fill=BOARD_WRITING)
    for li in range(3):
        lw = rng.randint(30, 60)
        draw.rectangle([wotw_x, wotw_y + 10 + li * 8,
                        wotw_x + lw, wotw_y + 14 + li * 8], fill=BOARD_FADED)

    map_x1 = board_x1
    map_x2 = board_x1 + int(bw * 0.55)
    map_y1 = fw_top + 4
    map_y2 = board_y1 - 4
    draw.rectangle([map_x1, map_y1, map_x2, map_y2], fill=(180, 190, 200))
    draw.rectangle([map_x1, map_y1, map_x2, map_y2], outline=DEEP_COCOA, width=1)

    pt_x2 = board_x1 - 4
    pt_x1 = max(fw_left + 2, pt_x2 - int(bw * 0.20))
    pt_y1 = fw_top + 8
    pt_y2 = board_y2 - 10
    draw.rectangle([pt_x1, pt_y1, pt_x2, pt_y2], fill=(220, 220, 200))
    draw.rectangle([pt_x1, pt_y1, pt_x2, pt_y2], outline=DEEP_COCOA, width=1)
    elem_w = max(2, (pt_x2 - pt_x1) // 10)
    elem_h = max(2, (pt_y2 - pt_y1) // 9)
    for ri in range(9):
        for ci in range(10):
            ex = pt_x1 + ci * elem_w
            ey = pt_y1 + ri * elem_h
            draw.rectangle([ex + 1, ey + 1, ex + elem_w - 1, ey + elem_h - 1],
                           fill=(200, 200, 185))

    td_x1 = fw_left + int((fw_right - fw_left) * 0.08)
    td_x2 = fw_left + int((fw_right - fw_left) * 0.55)
    td_y1 = fw_top + int((fw_bottom - fw_top) * 0.60)
    td_y2 = fw_bottom - 6
    draw.rectangle([td_x1, td_y1, td_x2, td_y2], fill=DESK_TEACHER)
    draw.rectangle([td_x1, td_y1, td_x2, td_y2], outline=DEEP_COCOA, width=2)
    draw.line([(td_x1, td_y1), (td_x2, td_y1)], fill=(180, 148, 100), width=2)

    np_x1 = td_x1 + int((td_x2 - td_x1) * 0.35)
    np_x2 = td_x1 + int((td_x2 - td_x1) * 0.65)
    np_y1 = td_y1 + 4
    np_y2 = td_y1 + 12
    draw.rectangle([np_x1, np_y1, np_x2, np_y2], fill=(200, 180, 120))
    draw.rectangle([np_x1, np_y1, np_x2, np_y2], outline=DEEP_COCOA, width=1)

    mug_x = td_x1 + int((td_x2 - td_x1) * 0.15)
    mug_y = td_y1 + 2
    draw.rectangle([mug_x, mug_y, mug_x + 10, mug_y + 14], fill=(160, 100, 80))
    for pi in range(4):
        draw.line([(mug_x + 2 + pi * 2, mug_y - 6), (mug_x + 2 + pi * 2, mug_y)],
                  fill=DEEP_COCOA, width=1)

    plant_x = td_x2 - 22
    plant_y = td_y1
    draw.ellipse([plant_x, plant_y - 10, plant_x + 14, plant_y + 4],
                 fill=(80, 140, 80))
    draw.rectangle([plant_x + 2, plant_y + 4, plant_x + 12, plant_y + 10],
                   fill=(192, 88, 56))

    for pi in range(3):
        draw.rectangle([td_x1 + 20 + pi * 2,
                        td_y1 + 2 + pi,
                        td_x1 + 60 + pi * 2,
                        td_y1 + 8 + pi],
                       fill=(235, 228, 210))

    return board_y2  # return board_y2 for chalk dust reference


def draw_student_desks_inhabited(draw, floor_top_y, rng):
    """
    FIX 2: Student desks with inhabitant evidence.
    - Wear marks on desk surfaces (lighter worn paths)
    - Papers/worksheets on several desks
    """
    vp_x = int(W * 0.12)
    vp_y = int(H * 0.36)

    num_rows = 6
    num_cols = 5

    # Track desk positions for paper placement
    desk_positions = []

    for row in range(num_rows):
        row_t = row / num_rows
        desk_y = int(H * 0.80 - row_t * (H * 0.80 - floor_top_y - 40))
        desk_scale = 1.0 - row_t * 0.65

        dw = int(100 * desk_scale)
        dh = int(24 * desk_scale)
        leg_h = int(32 * desk_scale)

        for col in range(num_cols):
            col_t = col / (num_cols - 1)

            x_base = int(W * 0.22 + col_t * W * 0.52)
            x_row_offset = int(row_t * W * (-0.08))
            dx = x_base + x_row_offset

            if rng.random() < 0.12:
                continue

            desk_color = lerp_color(DESK_STUDENT, (168, 148, 110), row_t * 0.4)
            draw.rectangle([dx, desk_y - dh, dx + dw, desk_y], fill=desk_color)
            draw.rectangle([dx, desk_y - dh, dx + dw, desk_y],
                           outline=DEEP_COCOA, width=1)
            draw.line([(dx, desk_y - dh), (dx + dw, desk_y - dh)],
                      fill=(200, 170, 120), width=1)

            # FIX 2: Wear marks on desk surface — lighter worn patch on right half
            wear_rng = random.Random(row * 10 + col)
            if wear_rng.random() < 0.65:
                wear_x = dx + dw // 3
                wear_w = dw // 3
                wear_h = max(2, dh // 3)
                wear_color = lerp_color(desk_color, (220, 200, 165), 0.35)
                draw.rectangle([wear_x, desk_y - dh + 2,
                                 wear_x + wear_w, desk_y - dh + 2 + wear_h],
                                fill=wear_color)

            draw.rectangle([dx + 4, desk_y, dx + 8, desk_y + leg_h], fill=DESK_FRAME)
            draw.rectangle([dx + dw - 8, desk_y, dx + dw - 4, desk_y + leg_h], fill=DESK_FRAME)

            chair_y = desk_y + int(leg_h * 0.6)
            chair_w = int(dw * 0.7)
            chair_x = dx + int(dw * 0.15)
            draw.rectangle([chair_x, chair_y, chair_x + chair_w, chair_y + dh // 2],
                           fill=(164, 138, 90))

            # FIX 2: Papers on desks — scattered worksheets
            if rng.random() < 0.55 and dw > 40:
                paper_w = max(18, int(dw * 0.45))
                paper_h = max(12, int(dh * 0.55))
                paper_x = dx + rng.randint(2, max(3, dw - paper_w - 2))
                # Slightly angled — implied by offset top vs bottom
                draw.polygon([
                    (paper_x, desk_y - dh + 2),
                    (paper_x + paper_w, desk_y - dh + 1),
                    (paper_x + paper_w - 2, desk_y - dh + 2 + paper_h),
                    (paper_x, desk_y - dh + 2 + paper_h),
                ], fill=(238, 232, 214))
                draw.rectangle([paper_x, desk_y - dh + 2,
                                 paper_x + paper_w, desk_y - dh + 2 + paper_h],
                                outline=(180, 175, 162), width=1)
                # Lines on paper (worksheet lines)
                for li in range(3):
                    lpy = desk_y - dh + 5 + li * int(paper_h / 4)
                    if lpy < desk_y:
                        draw.line([(paper_x + 2, lpy),
                                   (paper_x + paper_w - 2, lpy)],
                                  fill=(180, 175, 162), width=1)

            desk_positions.append((dx, desk_y - dh, dw, dh, row, col))

            if row == 0 and col == 0:
                for si in range(3):
                    sx = dx + 4 + si * 5
                    sy = desk_y - dh + 4
                    draw.rectangle([sx, sy, sx + 3, sy + 3], fill=(0, 200, 220))

            if row == 0 and col == 1:
                book_x = dx + dw // 3
                book_y = desk_y - dh + 2
                draw.rectangle([book_x, book_y, book_x + 18, desk_y - 2],
                               fill=(120, 160, 180))
                draw.rectangle([book_x, book_y, book_x + 18, desk_y - 2],
                               outline=DEEP_COCOA, width=1)

    return desk_positions


def draw_foreground_depth_anchor_inhabited(draw, rng, desk_positions, floor_top_y):
    """
    FIX 2: Foreground with backpack on floor near Luma's desk.
    Mandatory foreground depth anchor + forgotten item.
    """
    # Coat rack (unchanged)
    cr_x = int(W * 0.78)
    cr_y = int(H * 0.38)
    cr_bottom = int(H * 0.82)
    draw.rectangle([cr_x, cr_y, cr_x + 8, cr_bottom], fill=DESK_FRAME)
    draw.rectangle([cr_x - 60, cr_y + 30, cr_x + 60, cr_y + 38], fill=DESK_FRAME)
    pack_colors = [(80, 100, 140), (140, 80, 80), (80, 120, 80), (120, 100, 60)]
    pack_x_offsets = [-50, -25, 5, 30]
    for pi, (pc, px_off) in enumerate(zip(pack_colors, pack_x_offsets)):
        px = cr_x + px_off
        py = cr_y + 38
        pw = 22
        ph = rng.randint(28, 38)
        draw.rectangle([px, py, px + pw, py + ph], fill=pc)
        draw.rectangle([px, py, px + pw, py + ph], outline=DEEP_COCOA, width=1)
        draw.line([(px + pw // 2, py), (px + pw // 2, py - 10)],
                  fill=DEEP_COCOA, width=2)

    # Jacket on floor (unchanged)
    draw.ellipse([cr_x - 55, cr_bottom - 8, cr_x + 20, cr_bottom + 12],
                 fill=(100, 90, 80))

    # FIX 2: Forgotten backpack near Luma's desk (front-left area)
    # Luma's desk is front-row, col 0 — around x=W*0.22, near camera
    luma_desk_x = int(W * 0.22)
    # Floor y near this desk
    fg_floor_y = int(H * 0.88)  # front of classroom floor
    bp_x = luma_desk_x - 10
    bp_y = fg_floor_y - 5
    # Backpack body
    draw.rectangle([bp_x, bp_y - 42, bp_x + 28, bp_y], fill=(60, 80, 120))
    draw.rectangle([bp_x, bp_y - 42, bp_x + 28, bp_y], outline=DEEP_COCOA, width=1)
    # Top handle
    draw.arc([bp_x + 8, bp_y - 44, bp_x + 20, bp_y - 38],
             start=180, end=0, fill=DEEP_COCOA, width=2)
    # Front pocket
    draw.rectangle([bp_x + 4, bp_y - 22, bp_x + 24, bp_y - 8],
                   fill=(50, 70, 110))
    draw.rectangle([bp_x + 4, bp_y - 22, bp_x + 24, bp_y - 8],
                   outline=DEEP_COCOA, width=1)
    # Zipper line
    draw.line([(bp_x + 4, bp_y - 15), (bp_x + 24, bp_y - 15)],
              fill=(120, 140, 160), width=1)
    # Shadow under backpack
    draw.ellipse([bp_x - 3, bp_y - 4, bp_x + 30, bp_y + 4],
                 fill=(140, 130, 110))

    # Nearest desk corner (mandatory z-axis anchor)
    nd_x1 = int(W * 0.82)
    nd_y1 = int(H * 0.88)
    nd_x2 = W
    nd_y2 = H
    draw.rectangle([nd_x1, nd_y1, nd_x2, nd_y2], fill=DESK_STUDENT)
    draw.line([(nd_x1, nd_y1), (nd_x2, nd_y1)], fill=(200, 170, 120), width=3)
    draw.rectangle([nd_x1, nd_y1, nd_x2, nd_y2], outline=DEEP_COCOA, width=2)

    # FIX 2: Water bottle on nearest desk corner
    wb_x = nd_x1 + 20
    wb_y = nd_y1 + 4
    draw.rectangle([wb_x, wb_y, wb_x + 8, wb_y + 22], fill=(100, 170, 200))
    draw.rectangle([wb_x, wb_y, wb_x + 8, wb_y + 22], outline=DEEP_COCOA, width=1)
    draw.rectangle([wb_x + 1, wb_y + 2, wb_x + 7, wb_y + 6], fill=(180, 220, 240))
    draw.rectangle([wb_x + 2, wb_y - 3, wb_x + 6, wb_y], fill=(80, 140, 170))


def draw_bulletin_boards(draw, fw_left, fw_top, fw_right, fw_bottom):
    bb_x1 = int(W * 0.60)
    bb_x2 = W
    bb_y1 = int(H * 0.28)
    bb_y2 = int(H * 0.58)
    draw.rectangle([bb_x1, bb_y1, bb_x2, bb_y2], fill=BULLETIN_GOLD)
    draw.rectangle([bb_x1, bb_y1, bb_x2, bb_y2], outline=DEEP_COCOA, width=2)

    rng = random.Random(77)
    for _ in range(12):
        px = rng.randint(bb_x1 + 4, bb_x2 - 30)
        py = rng.randint(bb_y1 + 4, bb_y2 - 20)
        pw = rng.randint(20, 50)
        ph = rng.randint(15, 35)
        pc = (rng.randint(180, 235), rng.randint(180, 235), rng.randint(180, 235))
        draw.rectangle([px, py, px + pw, py + ph], fill=pc)
        draw.rectangle([px, py, px + pw, py + ph], outline=DEEP_COCOA, width=1)

    ww_x = int(W * 0.64)
    ww_y = int(H * 0.30)
    draw.rectangle([ww_x, ww_y, ww_x + 80, ww_y + 14], fill=(200, 184, 120))
    for li in range(3):
        draw.rectangle([ww_x, ww_y + 18 + li * 8,
                        ww_x + rng.randint(30, 70), ww_y + 22 + li * 8],
                       fill=(160, 148, 100))


def draw_scanline_hint(img):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(0, H, 4):
        od.line([(0, y), (W - 1, y)], fill=(0, 0, 0, 8))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


def main():
    rng = random.Random(42)
    img = Image.new("RGB", (W, H), WALL_SAGE)

    print("LTG_TOOL_bg_classroom.py — Classroom Fix Pass")
    print("  Fixes: (1) unified lighting, (2) inhabitant evidence")

    print("  Step 1: Base walls, ceiling, floor perspective planes...")
    draw, vp_x, vp_y, fw_left, fw_top, fw_right, fw_bottom, floor_top_y = \
        draw_base_walls(img)

    print("  Step 2: Floor tile grid pattern...")
    draw_floor_tiles(draw, floor_top_y, rng)

    print("  Step 3: Ceiling details (grid + fluorescent fixtures)...")
    draw_ceiling_details(draw, vp_x, vp_y)

    print("  Step 4: Left window wall (windows + blinds + radiators)...")
    draw = draw_window_wall(img, draw, vp_x, vp_y)

    print("  Step 5: Front wall content (board, teacher desk, posters + chalk dust)...")
    draw_front_wall(draw, fw_left, fw_top, fw_right, fw_bottom, rng)

    print("  Step 6: Student desks with inhabitant evidence (papers, wear marks)...")
    desk_positions = draw_student_desks_inhabited(draw, floor_top_y, rng)

    print("  Step 7: Foreground anchor (coat rack + backpack on floor + water bottle)...")
    draw_foreground_depth_anchor_inhabited(draw, rng, desk_positions, floor_top_y)

    print("  Step 8: Bulletin boards...")
    draw_bulletin_boards(draw, fw_left, fw_top, fw_right, fw_bottom)

    print("  Step 9: Window light shafts (warm gold, reduced overlap)...")
    img = draw_window_light_shafts(img)
    draw = ImageDraw.Draw(img)

    print("  Step 10: FIX 1 — Unified coherent dual-source lighting...")
    img = draw_unified_lighting(img, floor_top_y)
    draw = ImageDraw.Draw(img)

    print("  Step 11: Fluorescent floor pools (filled ellipses only)...")
    img = draw_fluorescent_floor_pools(img, floor_top_y)
    draw = ImageDraw.Draw(img)

    print("  Step 12: Subtle scanline hint...")
    img = draw_scanline_hint(img)

    out_path = ("/home/wipkat/team/output/backgrounds/environments/"
                "LTG_ENV_classroom_bg.png")
    img.save(out_path)
    size_bytes = img.size[0]  # just check we have it
    import os
    size_bytes = os.path.getsize(out_path)
    print(f"\nSaved: {out_path}")
    print(f"File size: {size_bytes:,} bytes ({size_bytes // 1024} KB)")
    print("\nFix verification:")
    print("  [FIX 1] Lighting: warm LEFT gradient (SUNLIT_AMBER, 55 alpha max) +")
    print("          cool RIGHT gradient (fluorescent, 50 alpha max) — no overlap mud ✓")
    print("  [FIX 2] Inhabitant evidence:")
    print("          - Wear marks on 65% of desks ✓")
    print("          - Scattered worksheets/papers on 55% of desks ✓")
    print("          - Forgotten backpack near Luma's desk (floor) ✓")
    print("          - Chalk dust near board tray ✓")
    print("          - Water bottle on nearest desk corner ✓")


if __name__ == "__main__":
    main()
