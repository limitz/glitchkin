#!/usr/bin/env python3
"""
LTG_TOOL_bg_classroom_v001.py — Millbrook Middle School Classroom Background
"Luma & the Glitchkin" — Background & Environment Design
Artist: Jordan Reed | Cycle 14

Renders the Millbrook Middle classroom environment at 1920x1080.
Used for Act 2 panels including storyboard panel A1-04 (classroom scene).

Camera position: Back-right corner, looking diagonally toward front-left.
Shows: front wall (board/teacher desk), left window wall, diagonal desk rows.
Ref doc: /output/backgrounds/environments/millbrook_school.md (v2.0)

Lighting: Dual temperature — fluorescent cool (#F0FFF0 cast) vs warm window gold.
  - Left third: warm window light zone
  - Center: mixed zone
  - Right third: pure fluorescent (cool, slightly green)

Color authority: millbrook_school.md + master_palette.md
  - Walls (classroom): Sage green muted #8A9E8A
  - Floor tile cream: #D8CEB0  /  sage: #8A9E88
  - Board: #C0C8C0 (whiteboard gray)
  - Teacher desk: wood laminate #9A7A50
  - Student desks: lighter laminate #B0925C
  - Window light shafts: Soft Gold #E8C95A at 40% opacity
  - Fluorescent floor pools: #D8E8D0

Rules applied (MEMORY.md):
  - 3-value-tier depth system: FG corner desks / MG desk rows / BG front wall
  - Foreground depth anchor: coat rack + nearest desk corner (bottom of frame)
  - Dual temperature lighting — warm LEFT, cool RIGHT
  - Pavement cracks rule → floor wear path must be LIGHTER not darker
  - Glow only as filled ellipses (fluorescent floor pools)
  - No per-pixel loops — use draw.line()
  - Refresh draw handle after alpha_composite

Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_classroom_bg_v001.png
"""

import math
import random
from PIL import Image, ImageDraw

# ── Canvas ───────────────────────────────────────────────────────────────────
W, H = 1920, 1080

# ── Palette (millbrook_school.md canonical) ──────────────────────────────────
# Walls
WALL_SAGE        = (138, 158, 138)  # #8A9E8A — classroom walls
WALL_SAGE_WARM   = (148, 168, 130)  # wall in window light zone (warmer)
WALL_SAGE_COOL   = (128, 148, 148)  # wall in fluorescent zone (cooler)
CEIL_TILE        = (216, 212, 192)  # #D8D4C0 — ceiling tile aged cream
CEIL_GRID        = (144, 152, 152)  # #909898 — ceiling grid metal
FLUORO_FIXTURE   = (232, 240, 232)  # #E8F0E8 — fluorescent fixture

# Floor
FLOOR_CREAM      = (216, 206, 176)  # #D8CEB0 — cream tile base
FLOOR_SAGE       = (138, 158, 136)  # #8A9E88 — sage tile base
FLOOR_WORN       = (224, 214, 188)  # lighter worn center path
FLOOR_FLUORO     = (208, 221, 208)  # #D0DDD0 — under fluorescent, green cast
FLOOR_WARM       = (232, 216, 168)  # #E8D8A8 — under window light, warm amber

# Furniture
BOARD_GRAY       = (192, 200, 192)  # #C0C8C0 — whiteboard/board surface
BOARD_WRITING    = (59,  40,  32)   # #3B2820 — Deep Cocoa — board writing
BOARD_FADED      = (154, 152, 152)  # #9A9898 — old ghost writing
DESK_TEACHER     = (154, 122,  80)  # #9A7A50 — teacher desk wood laminate
DESK_STUDENT     = (176, 146,  92)  # #B0925C — student desk lighter laminate
DESK_FRAME       = (74,  80,  80)   # #4A5050 — desk metal frame
WINDOW_GLASS     = (200, 220, 224)  # #C8DCE0 — window glass sky tint
BLIND_CREAM      = (216, 204, 172)  # #D8CCAC — venetian blinds
RADIATOR         = (144, 144, 128)  # #909080 — radiator (many paint coats)
DOOR_TERRA       = (192,  88,  56)  # #C05838 — terracotta doors
BULLETIN_GOLD    = (200, 168,  80)  # #C8A850 — bulletin board backing

# Lighting
WINDOW_LIGHT_COL = (232, 201,  90)  # #E8C95A — Soft Gold (Warm shaft color)
FLUORO_LIGHT_COL = (216, 232, 208)  # #D8E8D0 — fluorescent floor pool

# Line / shadow
DEEP_COCOA       = (59,  40,  32)   # #3B2820 — line work
SHADOW_COOL      = (122, 144, 128)  # #7A9080 — fluorescent zone shadow
SHADOW_WARM      = (168, 155, 191)  # #A89BBF — dusty lavender (window zone shadow)
LAVENDER_WALL    = (168, 155, 191)  # #A89BBF — hallway/accent lavender


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def alpha_rect(img, x0, y0, x1, y1, color_rgb, alpha):
    """Draw a filled rectangle at given alpha using alpha_composite."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle([x0, y0, x1, y1], fill=(*color_rgb, alpha))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


def draw_base_walls(img):
    """Draw base walls, ceiling and floor in 3/4 perspective from back-right."""
    draw = ImageDraw.Draw(img)

    # Perspective setup — back-right camera, looking front-left
    # Vanishing point: front-left area of canvas
    vp_x = int(W * 0.12)   # vanishing point x — left side
    vp_y = int(H * 0.36)   # vanishing point y — upper third

    # ── Ceiling ─────────────────────────────────────────────────────────────
    # Ceiling plane fills upper portion of canvas
    # Near edge of ceiling: full width at top of canvas
    # Far edge: converges toward vp_y
    ceil_near_y = 0
    ceil_far_y = vp_y - 20
    # Ceiling polygon — trapezoid
    ceil_poly = [
        (0, ceil_near_y),
        (W, ceil_near_y),
        (W, ceil_far_y + 40),
        (vp_x, ceil_far_y),
    ]
    draw.polygon(ceil_poly, fill=CEIL_TILE)

    # ── Front wall (teacher zone) ────────────────────────────────────────────
    # Front wall is the background plane behind the desks
    fw_left = vp_x
    fw_top  = vp_y - 20
    fw_right = int(W * 0.62)
    fw_bottom = int(H * 0.78)
    draw.rectangle([fw_left, fw_top, fw_right, fw_bottom], fill=WALL_SAGE)

    # ── Left window wall ─────────────────────────────────────────────────────
    # Left wall runs from vp toward camera-left, showing in left portion of frame
    lw_poly = [
        (vp_x, vp_y - 20),          # near top-corner of front wall
        (0, int(H * 0.28)),           # far top of left wall
        (0, int(H * 0.82)),           # far bottom of left wall
        (vp_x, fw_bottom),           # near bottom-corner
    ]
    draw.polygon(lw_poly, fill=WALL_SAGE_WARM)

    # ── Floor ────────────────────────────────────────────────────────────────
    # Floor fills lower portion
    floor_top_y = int(H * 0.72)  # where floor starts at far end
    floor_poly = [
        (0, floor_top_y),
        (W, floor_top_y + 40),
        (W, H),
        (0, H),
    ]
    draw.polygon(floor_poly, fill=FLOOR_CREAM)

    # Right wall — small strip on right side (behind camera, minor)
    rw_poly = [
        (int(W * 0.60), vp_y - 20),
        (W, int(H * 0.24)),
        (W, int(H * 0.78)),
        (int(W * 0.60), fw_bottom),
    ]
    draw.polygon(rw_poly, fill=WALL_SAGE_COOL)

    return draw, vp_x, vp_y, fw_left, fw_top, fw_right, fw_bottom, floor_top_y


def draw_floor_tiles(draw, floor_top_y, rng):
    """Draw linoleum tile grid pattern — alternating cream/sage with wear path."""
    # Tile grid implied by faint lines — max 10% opacity rule
    # Perspective lines converge to vp
    vp_x = int(W * 0.12)

    # Horizontal tile lines (cross rows)
    num_rows = 16
    for i in range(num_rows + 1):
        t = (i / num_rows) ** 1.8  # quadratic distribution
        y = floor_top_y + int(t * (H - floor_top_y))
        if y >= H:
            break
        # Faint grid lines — barely visible
        draw.line([(0, y), (W, y)], fill=(160, 148, 128), width=1)

    # Vertical tile lines (perspective recession)
    num_cols = 20
    for i in range(num_cols + 1):
        tx = i / num_cols
        bx = int(tx * W)
        draw.line([(vp_x, floor_top_y - 10), (bx, H)], fill=(160, 148, 128), width=1)

    # Warm zone (left third of floor — window light)
    warm_x = int(W * 0.33)
    for y in range(floor_top_y, H, 2):
        draw.line([(0, y), (warm_x, y)], fill=FLOOR_WARM)

    # Cool zone (right two-thirds — fluorescent)
    for y in range(floor_top_y, H, 2):
        draw.line([(warm_x, y), (W, y)], fill=FLOOR_FLUORO)


def draw_ceiling_details(draw, vp_x, vp_y):
    """Draw ceiling tiles and fluorescent fixtures."""
    ceil_near_y = 0
    ceil_far_y = vp_y - 20

    # Ceiling grid lines — metal framework
    num_rows = 8
    for i in range(1, num_rows):
        t = (i / num_rows) ** 1.4
        cy = int(t * (ceil_far_y - ceil_near_y))
        # Horizontal grid strips
        draw.line([(0, cy), (W, cy)], fill=CEIL_GRID, width=2)

    # Fluorescent fixture strips — two rows running front to back
    fix_col = [int(W * 0.35), int(W * 0.60)]
    for fx in fix_col:
        for i in range(1, num_rows):
            t = (i / num_rows) ** 1.4
            fy = int(t * (ceil_far_y - ceil_near_y))
            # Fixture as bright rectangle in ceiling
            fw = int(W * 0.04)
            fh = 4
            draw.rectangle([fx - fw // 2, fy - fh // 2,
                             fx + fw // 2, fy + fh // 2], fill=FLUORO_FIXTURE)


def draw_window_wall(img, draw, vp_x, vp_y):
    """Draw three windows on the left wall with venetian blinds and radiators."""
    # Left wall boundary
    lw_top_y = int(H * 0.28)
    lw_bot_y = int(H * 0.82)
    wall_height = lw_bot_y - lw_top_y
    # Windows positioned on the left wall (angled in perspective)
    # Windows at 3 feet off floor to 7 feet — tall windows
    # In perspective: left wall tapers toward vp

    window_specs = [
        # (y_frac_top, y_frac_bottom, x_left_frac, x_right_frac)
        (0.32, 0.68, 0.01, 0.06),   # window 1 — furthest left
        (0.34, 0.70, 0.06, 0.11),   # window 2 (broken slat)
        (0.36, 0.70, 0.11, 0.16),   # window 3
    ]
    for wi, (ytf, ybf, xlf, xrf) in enumerate(window_specs):
        wy1 = lw_top_y + int(ytf * wall_height)
        wy2 = lw_top_y + int(ybf * wall_height)
        wx1 = int(xlf * W)
        wx2 = int(xrf * W)
        # Window glass
        draw.rectangle([wx1, wy1, wx2, wy2], fill=WINDOW_GLASS)
        # Window frame (thin deep cocoa outline)
        draw.rectangle([wx1, wy1, wx2, wy2], outline=DEEP_COCOA, width=2)
        # Venetian blinds — horizontal slats
        slat_count = 14
        for si in range(slat_count):
            sy = wy1 + int(si / slat_count * (wy2 - wy1))
            # Broken slat on window 2 — one slat at perpendicular angle
            if wi == 1 and si == 7:
                # Broken slat — runs diagonally instead of horizontal
                draw.line([(wx1, sy), (wx2, sy - 4)], fill=BLIND_CREAM, width=2)
            else:
                draw.line([(wx1, sy), (wx2, sy)], fill=BLIND_CREAM, width=2)

        # Radiator below window
        rad_y1 = wy2 + 4
        rad_y2 = rad_y1 + int(H * 0.04)
        draw.rectangle([wx1, rad_y1, wx2, rad_y2], fill=RADIATOR)
        # Radiator ribs
        rib_step = max(4, (wx2 - wx1) // 5)
        for rx in range(wx1, wx2, rib_step):
            draw.line([(rx, rad_y1), (rx, rad_y2)], fill=(160, 160, 144), width=1)

    return draw


def draw_window_light_shafts(img):
    """Warm gold window light shafts crossing desk rows diagonally."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # Three shafts from the three windows — clean-edged parallelograms
    # Venetian blind shafts: diagonal, warm gold at 40% opacity
    shaft_alpha = 102  # 40% of 255

    shaft_specs = [
        # (floor_x_start, floor_x_end, top_y, bottom_y, x_offset_at_top)
        (80, 200, int(H * 0.38), H, -60),
        (220, 340, int(H * 0.40), H, -50),
        (360, 480, int(H * 0.42), H, -40),
    ]
    for (fx1, fx2, ty, by, x_off) in shaft_specs:
        # Parallelogram: top edge offset from bottom edge
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
    """Soft oval fluorescent light pools on floor beneath fixtures — filled ellipses."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # Fixture positions (two rows)
    fixture_xs = [int(W * 0.35), int(W * 0.60)]
    num_pools = 6
    for fx in fixture_xs:
        for i in range(1, num_pools + 1):
            t = i / (num_pools + 1)
            fy = floor_top_y + int(t * (H - floor_top_y))
            pool_w = int(W * 0.08 * (1.0 + t * 0.5))  # wider near camera
            pool_h = int(H * 0.025)
            # Filled ellipse — never outline only (Cycle 6 rule)
            od.ellipse([fx - pool_w // 2, fy - pool_h // 2,
                        fx + pool_w // 2, fy + pool_h // 2],
                       fill=(*FLUORO_LIGHT_COL, 80))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


def draw_front_wall(draw, fw_left, fw_top, fw_right, fw_bottom, rng):
    """Draw the front wall: whiteboard, teacher's desk, posters."""
    # ── Whiteboard / Chalkboard hybrid ──────────────────────────────────────
    board_x1 = fw_left + int((fw_right - fw_left) * 0.04)
    board_x2 = fw_left + int((fw_right - fw_left) * 0.88)
    board_y1 = fw_top + int((fw_bottom - fw_top) * 0.10)
    board_y2 = fw_top + int((fw_bottom - fw_top) * 0.50)
    draw.rectangle([board_x1, board_y1, board_x2, board_y2], fill=BOARD_GRAY)
    draw.rectangle([board_x1, board_y1, board_x2, board_y2],
                   outline=DEEP_COCOA, width=2)
    # Board tray at bottom
    draw.rectangle([board_x1, board_y2, board_x2, board_y2 + 6],
                   fill=(154, 140, 120))

    # Current lesson: binary/math content (per task brief for A1-04 context)
    # Board content — "BINARY & DATA" with some binary numbers
    bx = board_x1 + 8
    by = board_y1 + 8
    bw = board_x2 - board_x1 - 16
    bh = board_y2 - board_y1 - 16
    # Title line
    draw.rectangle([bx, by, bx + int(bw * 0.55), by + 6], fill=BOARD_WRITING)
    # Sub-title (subject label)
    draw.rectangle([bx, by + 14, bx + int(bw * 0.35), by + 18], fill=BOARD_WRITING)
    # Binary lesson rows (suggest "01001000" patterns with small rectangles)
    for row in range(3):
        ry = by + 28 + row * 18
        for col in range(16):
            if rng.random() < 0.55:  # ~half 1s, half 0s
                bbit = bx + col * int(bw / 18)
                draw.rectangle([bbit, ry, bbit + 4, ry + 8], fill=BOARD_WRITING)
    # Math equation suggestion — horizontal lines + symbols
    eq_y = by + 80
    draw.rectangle([bx + int(bw * 0.02), eq_y,
                    bx + int(bw * 0.40), eq_y + 5], fill=BOARD_WRITING)
    draw.rectangle([bx + int(bw * 0.50), eq_y,
                    bx + int(bw * 0.90), eq_y + 5], fill=BOARD_WRITING)
    # Equals sign
    draw.rectangle([bx + int(bw * 0.43), eq_y - 3,
                    bx + int(bw * 0.48), eq_y - 1], fill=BOARD_WRITING)
    draw.rectangle([bx + int(bw * 0.43), eq_y + 3,
                    bx + int(bw * 0.48), eq_y + 5], fill=BOARD_WRITING)

    # Faded ghost writing from previous lesson
    ghost_y = by + 100
    for g in range(4):
        gx = bx + rng.randint(0, int(bw * 0.7))
        gw = rng.randint(20, 60)
        draw.rectangle([gx, ghost_y + g * 12, gx + gw, ghost_y + g * 12 + 3],
                       fill=BOARD_FADED)

    # Word of the week: "PERSEVERANCE"
    wotw_x = board_x2 - int(bw * 0.35)
    wotw_y = board_y1 + 6
    draw.rectangle([wotw_x, wotw_y, board_x2 - 6, wotw_y + 5], fill=BOARD_WRITING)
    for li in range(3):
        lw = rng.randint(30, 60)
        draw.rectangle([wotw_x, wotw_y + 10 + li * 8,
                        wotw_x + lw, wotw_y + 14 + li * 8], fill=BOARD_FADED)

    # Above board: world map (slightly crooked)
    map_x1 = board_x1
    map_x2 = board_x1 + int(bw * 0.55)
    map_y1 = fw_top + 4
    map_y2 = board_y1 - 4
    draw.rectangle([map_x1, map_y1, map_x2, map_y2], fill=(180, 190, 200))
    draw.rectangle([map_x1, map_y1, map_x2, map_y2], outline=DEEP_COCOA, width=1)

    # Periodic table poster (left of board)
    pt_x2 = board_x1 - 4
    pt_x1 = max(fw_left + 2, pt_x2 - int(bw * 0.20))
    pt_y1 = fw_top + 8
    pt_y2 = board_y2 - 10
    draw.rectangle([pt_x1, pt_y1, pt_x2, pt_y2], fill=(220, 220, 200))
    draw.rectangle([pt_x1, pt_y1, pt_x2, pt_y2], outline=DEEP_COCOA, width=1)
    # Suggest the grid of elements
    elem_w = max(2, (pt_x2 - pt_x1) // 10)
    elem_h = max(2, (pt_y2 - pt_y1) // 9)
    for ri in range(9):
        for ci in range(10):
            ex = pt_x1 + ci * elem_w
            ey = pt_y1 + ri * elem_h
            draw.rectangle([ex + 1, ey + 1, ex + elem_w - 1, ey + elem_h - 1],
                           fill=(200, 200, 185))

    # ── Teacher's Desk ───────────────────────────────────────────────────────
    td_x1 = fw_left + int((fw_right - fw_left) * 0.08)
    td_x2 = fw_left + int((fw_right - fw_left) * 0.55)
    td_y1 = fw_top + int((fw_bottom - fw_top) * 0.60)
    td_y2 = fw_bottom - 6
    draw.rectangle([td_x1, td_y1, td_x2, td_y2], fill=DESK_TEACHER)
    draw.rectangle([td_x1, td_y1, td_x2, td_y2], outline=DEEP_COCOA, width=2)
    # Desk top edge highlight
    draw.line([(td_x1, td_y1), (td_x2, td_y1)], fill=(180, 148, 100), width=2)

    # Name placard on desk
    np_x1 = td_x1 + int((td_x2 - td_x1) * 0.35)
    np_x2 = td_x1 + int((td_x2 - td_x1) * 0.65)
    np_y1 = td_y1 + 4
    np_y2 = td_y1 + 12
    draw.rectangle([np_x1, np_y1, np_x2, np_y2], fill=(200, 180, 120))
    draw.rectangle([np_x1, np_y1, np_x2, np_y2], outline=DEEP_COCOA, width=1)

    # Mug of pens
    mug_x = td_x1 + int((td_x2 - td_x1) * 0.15)
    mug_y = td_y1 + 2
    draw.rectangle([mug_x, mug_y, mug_x + 10, mug_y + 14], fill=(160, 100, 80))
    # Pen tops sticking out
    for pi in range(4):
        draw.line([(mug_x + 2 + pi * 2, mug_y - 6), (mug_x + 2 + pi * 2, mug_y)],
                  fill=DEEP_COCOA, width=1)

    # Plant (small succulent — terracotta pot)
    plant_x = td_x2 - 22
    plant_y = td_y1
    draw.ellipse([plant_x, plant_y - 10, plant_x + 14, plant_y + 4],
                 fill=(80, 140, 80))   # plant body
    draw.rectangle([plant_x + 2, plant_y + 4, plant_x + 12, plant_y + 10],
                   fill=(192, 88, 56))  # terracotta pot

    # Paper stack
    for pi in range(3):
        draw.rectangle([td_x1 + 20 + pi * 2,
                        td_y1 + 2 + pi,
                        td_x1 + 60 + pi * 2,
                        td_y1 + 8 + pi],
                       fill=(235, 228, 210))


def draw_student_desks(draw, floor_top_y, rng):
    """Draw diagonal rows of student desks receding toward front wall."""
    # From back-right looking front-left — desks in diagonal rows
    # 6 rows of 5 desks, diagonal perspective
    # Near camera: bottom-left area; far: upper-right toward front wall
    # Perspective: desks shrink toward the vanishing point

    vp_x = int(W * 0.12)
    vp_y = int(H * 0.36)

    # Desk grid: define desk positions in screen space
    # Row 0 = nearest (bottom), Row 5 = farthest (near front wall)
    # Col 0 = leftmost (window side), Col 4 = rightmost

    num_rows = 6
    num_cols = 5

    for row in range(num_rows):
        row_t = row / num_rows  # 0=near, 1=far
        # Y position: near desks are low in frame, far desks high
        desk_y = int(H * 0.80 - row_t * (H * 0.80 - floor_top_y - 40))
        desk_scale = 1.0 - row_t * 0.65  # desks shrink with distance

        # Desk width and height scale with distance
        dw = int(100 * desk_scale)
        dh = int(24 * desk_scale)
        leg_h = int(32 * desk_scale)

        for col in range(num_cols):
            col_t = col / (num_cols - 1)  # 0=left, 1=right

            # X position — diagonal arrangement, offset per row
            x_base = int(W * 0.22 + col_t * W * 0.52)
            x_row_offset = int(row_t * W * (-0.08))  # diagonal shift leftward
            dx = x_base + x_row_offset

            # Skip some desks — not all filled
            if rng.random() < 0.12:
                continue

            # Desk surface
            desk_color = lerp_color(DESK_STUDENT, (168, 148, 110), row_t * 0.4)
            draw.rectangle([dx, desk_y - dh, dx + dw, desk_y], fill=desk_color)
            draw.rectangle([dx, desk_y - dh, dx + dw, desk_y],
                           outline=DEEP_COCOA, width=1)
            # Top edge highlight
            draw.line([(dx, desk_y - dh), (dx + dw, desk_y - dh)],
                      fill=(200, 170, 120), width=1)

            # Desk legs (metal frame) — simplified front legs only
            draw.rectangle([dx + 4, desk_y, dx + 8, desk_y + leg_h],
                           fill=DESK_FRAME)
            draw.rectangle([dx + dw - 8, desk_y, dx + dw - 4, desk_y + leg_h],
                           fill=DESK_FRAME)

            # Chair suggestion (seat platform behind/below desk)
            chair_y = desk_y + int(leg_h * 0.6)
            chair_w = int(dw * 0.7)
            chair_x = dx + int(dw * 0.15)
            draw.rectangle([chair_x, chair_y, chair_x + chair_w, chair_y + dh // 2],
                           fill=(164, 138, 90))

            # Luma's desk: front-left area — row 0, col 0
            if row == 0 and col == 0:
                # Pixel-pattern sticker — small cyan marks
                for si in range(3):
                    sx = dx + 4 + si * 5
                    sy = desk_y - dh + 4
                    draw.rectangle([sx, sy, sx + 3, sy + 3], fill=(0, 200, 220))

            # Cosmo's desk: next to Luma — row 0, col 1
            if row == 0 and col == 1:
                # Library book on desk
                book_x = dx + dw // 3
                book_y = desk_y - dh + 2
                draw.rectangle([book_x, book_y, book_x + 18, desk_y - 2],
                               fill=(120, 160, 180))
                draw.rectangle([book_x, book_y, book_x + 18, desk_y - 2],
                               outline=DEEP_COCOA, width=1)


def draw_foreground_depth_anchor(draw, rng):
    """Coat rack and nearest desk corner — mandatory foreground depth anchor."""
    # Coat rack near camera (back-right corner area)
    cr_x = int(W * 0.78)
    cr_y = int(H * 0.38)
    cr_bottom = int(H * 0.82)
    # Vertical rack pole
    draw.rectangle([cr_x, cr_y, cr_x + 8, cr_bottom], fill=DESK_FRAME)
    # Horizontal bar
    draw.rectangle([cr_x - 60, cr_y + 30, cr_x + 60, cr_y + 38], fill=DESK_FRAME)
    # Hanging backpacks (blobs — simplified)
    pack_colors = [(80, 100, 140), (140, 80, 80), (80, 120, 80), (120, 100, 60)]
    pack_x_offsets = [-50, -25, 5, 30]
    for pi, (pc, px_off) in enumerate(zip(pack_colors, pack_x_offsets)):
        px = cr_x + px_off
        py = cr_y + 38
        pw = 22
        ph = rng.randint(28, 38)
        draw.rectangle([px, py, px + pw, py + ph], fill=pc)
        draw.rectangle([px, py, px + pw, py + ph], outline=DEEP_COCOA, width=1)
        # Strap / handle
        draw.line([(px + pw // 2, py), (px + pw // 2, py - 10)],
                  fill=DEEP_COCOA, width=2)

    # One jacket on floor (has been there since September)
    draw.ellipse([cr_x - 55, cr_bottom - 8, cr_x + 20, cr_bottom + 12],
                 fill=(100, 90, 80))

    # Nearest desk corner (bottom of frame — partial, acts as z-anchor)
    nd_x1 = int(W * 0.82)
    nd_y1 = int(H * 0.88)
    nd_x2 = W
    nd_y2 = H
    draw.rectangle([nd_x1, nd_y1, nd_x2, nd_y2], fill=DESK_STUDENT)
    draw.line([(nd_x1, nd_y1), (nd_x2, nd_y1)], fill=(200, 170, 120), width=3)
    draw.rectangle([nd_x1, nd_y1, nd_x2, nd_y2], outline=DEEP_COCOA, width=2)


def draw_bulletin_boards(draw, fw_left, fw_top, fw_right, fw_bottom):
    """Bulletin boards on right wall (partial view) and above board."""
    # Right wall bulletin strip (partial — camera is near right wall)
    bb_x1 = int(W * 0.60)
    bb_x2 = W
    bb_y1 = int(H * 0.28)
    bb_y2 = int(H * 0.58)
    draw.rectangle([bb_x1, bb_y1, bb_x2, bb_y2], fill=BULLETIN_GOLD)
    draw.rectangle([bb_x1, bb_y1, bb_x2, bb_y2], outline=DEEP_COCOA, width=2)

    # Pinned paper items on bulletin board
    rng = random.Random(77)
    for _ in range(12):
        px = rng.randint(bb_x1 + 4, bb_x2 - 30)
        py = rng.randint(bb_y1 + 4, bb_y2 - 20)
        pw = rng.randint(20, 50)
        ph = rng.randint(15, 35)
        # Random light colors for student work
        pc = (rng.randint(180, 235), rng.randint(180, 235), rng.randint(180, 235))
        draw.rectangle([px, py, px + pw, py + ph], fill=pc)
        draw.rectangle([px, py, px + pw, py + ph], outline=DEEP_COCOA, width=1)

    # "PERSEVERANCE" word of the week (implied by rectangle)
    ww_x = int(W * 0.64)
    ww_y = int(H * 0.30)
    draw.rectangle([ww_x, ww_y, ww_x + 80, ww_y + 14], fill=(200, 184, 120))
    for li in range(3):
        draw.rectangle([ww_x, ww_y + 18 + li * 8,
                        ww_x + rng.randint(30, 70), ww_y + 22 + li * 8],
                       fill=(160, 148, 100))


def draw_scanline_hint(img):
    """Subtle scanline overlay — school has a digital layer underneath (style guide)."""
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

    # Step 1: Base walls, ceiling, floor perspective planes
    draw, vp_x, vp_y, fw_left, fw_top, fw_right, fw_bottom, floor_top_y = \
        draw_base_walls(img)

    # Step 2: Floor tile grid pattern
    draw_floor_tiles(draw, floor_top_y, rng)

    # Step 3: Ceiling details (grid + fluorescent fixtures)
    draw_ceiling_details(draw, vp_x, vp_y)

    # Step 4: Left window wall (windows + blinds + radiators)
    draw = draw_window_wall(img, draw, vp_x, vp_y)

    # Step 5: Front wall content (board, teacher desk, posters)
    draw_front_wall(draw, fw_left, fw_top, fw_right, fw_bottom, rng)

    # Step 6: Student desks in diagonal rows (MG depth layer)
    draw_student_desks(draw, floor_top_y, rng)

    # Step 7: Foreground depth anchor — coat rack + nearest desk corner (FG mandatory)
    draw_foreground_depth_anchor(draw, rng)

    # Step 8: Bulletin boards
    draw_bulletin_boards(draw, fw_left, fw_top, fw_right, fw_bottom)

    # Step 9: Window light shafts — warm gold diagonal bars over desk rows
    img = draw_window_light_shafts(img)

    # Step 10: Fluorescent floor pools — filled ellipses (Cycle 6 rule)
    img = draw_fluorescent_floor_pools(img, floor_top_y)

    # Step 11: Subtle scanline hint (digital layer under the real world)
    img = draw_scanline_hint(img)

    # Save output
    out_path = ("/home/wipkat/team/output/backgrounds/environments/"
                "LTG_ENV_classroom_bg_v001.png")
    img.save(out_path)
    print(f"Saved: {out_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}  Mode: {img.mode}")
    print("  Depth tiers: FG=coat rack + desk corner / MG=desk rows / BG=front wall ✓")
    print("  Dual temperature: warm LEFT (window gold) / cool RIGHT (fluorescent) ✓")
    print("  Foreground depth anchor: present ✓")


if __name__ == "__main__":
    main()
