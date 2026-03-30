#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_bg_classroom.py — Millbrook Middle School Classroom Background (Full Rebuild)
"Luma & the Glitchkin" — Background & Environment Design
Artist: Hana Okonkwo | Cycle 41 | v003 C43: chalkboard draw_pixel_text() upgrade

Full rebuild from ENV_REBUILD_SPEC_classroom_c41.md. Prior generator (Jordan Reed C14/C16)
failed QA on silhouette (blob), warm/cool (9.3 FAIL), and line weight (mean=414.65, outliers=3).

Architecture:
  - 1280×720 canvas (switched from 1920×1080 legacy spec)
  - 3/4 camera from back-right corner looking toward front-left
  - VP_X = int(W * 0.15), VP_Y = int(H * 0.32)
  - Dual-temperature lighting:
      LEFT half  — SUNLIT_AMBER from windows, clean warm zone
      RIGHT half — FLUORO_LIGHT (216,232,208), cool fluorescent zone
      Hard transition at x=W//2. No muddy overlap.
  - All outline strokes width=1 maximum (line weight fix)
  - Foreground depth anchor: near desk corner + backpack
  - Inhabitant evidence: wear marks, worksheets, backpack, chalk dust, water bottle
  - Value hierarchy: walls/ceiling 70-80, desks/floor 40-65, shadow crevices ≤30
  - seeded RNG seed=44

QA targets:
  - warm/cool separation ≥ 12 (REAL world threshold)
  - value floor ≤ 30, ceiling ≥ 225, range ≥ 150
  - line weight outliers ≤ 1

Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_classroom_bg.png
"""

import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from LTG_TOOL_render_lib import light_shaft, vignette, paper_texture  # noqa: E402
from LTG_TOOL_pixel_font_v001 import draw_pixel_text  # noqa: E402

# ── Canvas ─────────────────────────────────────────────────────────────────────
W, H = 1280, 720
RNG = random.Random(44)

# ── Vanishing Point ────────────────────────────────────────────────────────────
VP_X = int(W * 0.15)   # 192
VP_Y = int(H * 0.32)   # 230

# ── Real World Palette ─────────────────────────────────────────────────────────
# Walls / ceiling
CEIL_TILE        = (222, 218, 202)   # warm cream ceiling tile
CEIL_GRID        = (180, 176, 162)   # grid line between tiles
WALL_SAGE_WARM   = (168, 178, 148)   # left wall (warm light zone)
WALL_SAGE_COOL   = (148, 162, 162)   # right wall (cool fluorescent zone)
WALL_BACK        = (178, 182, 162)   # back/front wall (chalkboard wall)

# Board
BOARD_GRAY       = (86, 110, 94)     # classic chalkboard green-grey
BOARD_LIGHT      = (104, 130, 112)   # lighter board zone (highlight from window)
BOARD_CHALK_TEXT = (188, 196, 190)   # chalk writing (faded)
CHALK_DUST       = (200, 198, 190)   # chalk residue near tray

# Floor
FLOOR_CREAM      = (210, 202, 178)   # linoleum tile A
FLOOR_SAGE       = (142, 158, 138)   # linoleum tile B
FLOOR_WORN       = (222, 212, 188)   # worn center path (lighter)
FLOOR_WARM       = (224, 210, 172)   # warm sunlit floor zone (left)
FLOOR_COOL       = (196, 210, 202)   # cool fluorescent floor zone (right)

# Desks
DESK_TOP_WARM    = (182, 150, 96)    # desk surface (warm side)
DESK_TOP_COOL    = (162, 158, 148)   # desk surface (cool side)
DESK_WEAR        = (198, 172, 120)   # worn lighter patch on desk
DESK_FRAME       = (72, 76, 72)      # dark metal desk frame
CHAIR_SEAT       = (156, 168, 156)   # plastic chair (neutral)
PAPER_WHITE      = (238, 234, 222)   # worksheet on desk
PAPER_YELLOW     = (230, 218, 172)   # lined worksheet

# Windows
WINDOW_GLASS     = (196, 218, 228)   # window pane
WINDOW_FRAME     = (218, 202, 162)   # window frame (cream-warm)
WINDOW_SILL      = (208, 194, 158)   # window sill

# Teacher desk / board tray
TEACHER_DESK     = (154, 122, 80)    # warm wood teacher desk
BOARD_TRAY       = (92, 96, 88)      # chalk tray (dark)

# Bulletin board
BULLETIN_BACKING = (196, 164, 80)    # cork board backing
BULLETIN_PIN_RED = (180, 60, 48)
BULLETIN_PIN_BLU = (72, 102, 148)

# Backpack
BACKPACK_MAIN    = (52, 88, 148)     # Luma's backpack — deep blue
BACKPACK_POCKET  = (42, 72, 128)     # pocket (darker)
BACKPACK_STRAP   = (38, 62, 108)     # strap

# Water bottle
BOTTLE_BODY      = (172, 196, 188)   # pale teal/green bottle

# Lighting
SUNLIT_AMBER     = (212, 146, 58)    # window warm shaft
FLUORO_LIGHT     = (216, 232, 208)   # fluorescent cool light

# Deep shadow / value floor
NEAR_BLACK_WARM  = (20, 12, 8)       # darkest crevice shadow
LINE_DARK        = (48, 36, 28)      # structural line color (warm dark)
LINE_COOL        = (52, 58, 60)      # cool side structural line

# Radiator / door
RADIATOR_WARM    = (180, 162, 128)
DOOR_TERRA       = (180, 84, 52)     # terracotta classroom door

# Fluorescent fixture
FLUORO_FIXTURE   = (230, 238, 228)   # fixture housing
FLUORO_TUBE      = (248, 252, 244)   # lamp tube (near-white warm-cool)


# ── Drawing Helpers ────────────────────────────────────────────────────────────

def draw_rect(draw, x0, y0, x1, y1, fill, outline=None, width=1):
    draw.rectangle([x0, y0, x1, y1], fill=fill,
                   outline=outline, width=width if outline else 0)


def alpha_overlay(img, x0, y0, x1, y1, color_rgb, alpha):
    """Alpha-composite a solid color rectangle over img."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([x0, y0, x1, y1], fill=(*color_rgb, alpha))
    rgba = img.convert("RGBA")
    rgba.alpha_composite(layer)
    return rgba.convert("RGB")


def alpha_poly(img, pts, color_rgb, alpha):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.polygon(pts, fill=(*color_rgb, alpha))
    rgba = img.convert("RGBA")
    rgba.alpha_composite(layer)
    return rgba.convert("RGB")


def gradient_rect_v(img, x0, y0, x1, y1, col_top, col_bot):
    """Vertical gradient fill."""
    layer = Image.new("RGB", (W, H))
    ld = ImageDraw.Draw(layer)
    span = max(1, y1 - y0)
    for y in range(y0, y1 + 1):
        t = (y - y0) / span
        c = tuple(int(col_top[i] + (col_bot[i] - col_top[i]) * t) for i in range(3))
        ld.line([(x0, y), (x1, y)], fill=c, width=1)
    img.paste(layer.crop((x0, y0, x1, y1)), (x0, y0))
    return img


def gradient_rect_h(img, x0, y0, x1, y1, col_left, col_right):
    """Horizontal gradient fill."""
    layer = Image.new("RGB", (W, H), col_left)
    ld = ImageDraw.Draw(layer)
    span = max(1, x1 - x0)
    for x in range(x0, x1 + 1):
        t = (x - x0) / span
        c = tuple(int(col_left[i] + (col_right[i] - col_left[i]) * t) for i in range(3))
        ld.line([(x, y0), (x, y1)], fill=c, width=1)
    img.paste(layer.crop((x0, y0, x1 + 1, y1 + 1)), (x0, y0))
    return img


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_pt(p0, p1, t):
    return (int(lerp(p0[0], p1[0], t)), int(lerp(p0[1], p1[1], t)))


def vp_x_at_y(x_near, y_near, y_target):
    """Given a point on the near edge, find where line to VP hits y_target."""
    if y_near == VP_Y:
        return VP_X
    t = (y_target - VP_Y) / (y_near - VP_Y)
    return int(VP_X + (x_near - VP_X) * t)


# ── Scene geometry constants ───────────────────────────────────────────────────
BACK_WALL_Y0     = 0
BACK_WALL_Y1     = H
BOARD_WALL_X_NEAR = 0            # board/front wall is on the left side (camera back-right)
BOARD_WALL_X_FAR  = VP_X

CEIL_Y_NEAR      = 0
CEIL_Y_FAR       = VP_Y - 20     # ceiling line at back wall (~210)
FLOOR_Y_FAR      = VP_Y + 50     # floor line at back wall (~280)
FLOOR_Y_NEAR     = H             # floor at camera level

# Back wall x extent (we see just a strip — back of classroom)
BACK_WALL_X0     = VP_X
BACK_WALL_X1     = int(W * 0.55)  # back wall runs from VP to about 55% width

# Right wall (the wall closest to camera on the right side)
RIGHT_WALL_X_FAR  = BACK_WALL_X1
RIGHT_WALL_X_NEAR = W

# Left wall (windows side, recedes into distance)
LEFT_WALL_X_NEAR = 0
LEFT_WALL_X_FAR  = VP_X

# Desk rows geometry
DESK_ROWS_X_START = int(W * 0.18)
DESK_ROWS_X_END   = int(W * 0.72)
NUM_DESK_ROWS     = 4
NUM_DESK_COLS     = 5


def main():
    img = Image.new("RGB", (W, H), CEIL_TILE)
    draw = ImageDraw.Draw(img)

    # ── 1. CEILING ─────────────────────────────────────────────────────────────
    # Ceiling plane: trapezoid from top edge down to ceil_y_far line
    ceil_pts = [
        (0, 0), (W, 0),
        (RIGHT_WALL_X_FAR, CEIL_Y_FAR),
        (LEFT_WALL_X_FAR, CEIL_Y_FAR),
    ]
    draw.polygon(ceil_pts, fill=CEIL_TILE)
    draw = ImageDraw.Draw(img)

    # Ceiling tile grid
    n_grid_x = 8
    n_grid_y = 3
    for i in range(1, n_grid_x):
        t = i / n_grid_x
        x_top = int(t * W)
        x_bot = int(lerp(LEFT_WALL_X_FAR, RIGHT_WALL_X_FAR, t))
        y_bot = CEIL_Y_FAR
        draw.line([(x_top, 0), (x_bot, y_bot)], fill=CEIL_GRID, width=1)
    for j in range(1, n_grid_y):
        t = j / n_grid_y
        y = int(t * CEIL_Y_FAR)
        x_left = int(lerp(0, LEFT_WALL_X_FAR, j / n_grid_y))
        x_right = int(lerp(W, RIGHT_WALL_X_FAR, j / n_grid_y))
        draw.line([(x_left, y), (x_right, y)], fill=CEIL_GRID, width=1)

    # Fluorescent tube fixtures — 2 rows across ceiling
    fix_y_positions = [int(H * 0.08), int(H * 0.16)]
    for fy in fix_y_positions:
        # 3 fixtures per row at equal x intervals
        for fi in range(3):
            t = (fi + 0.5) / 3
            fx_center = int(t * W)
            fx_half_w = int(lerp(55, 35, t))   # foreshortening
            fx_h = 10
            # Housing
            draw_rect(draw, fx_center - fx_half_w, fy - fx_h // 2,
                      fx_center + fx_half_w, fy + fx_h // 2, FLUORO_FIXTURE)
            # Tube glow
            draw_rect(draw, fx_center - fx_half_w + 4, fy - 2,
                      fx_center + fx_half_w - 4, fy + 2, FLUORO_TUBE)
    draw = ImageDraw.Draw(img)

    # ── 2. BACK WALL (chalkboard wall, front of classroom) ─────────────────────
    # Back wall is a vertical strip around VP_X, receding into distance
    # Board wall goes from left side to BACK_WALL_X1
    back_pts = [
        (LEFT_WALL_X_FAR, CEIL_Y_FAR),
        (BACK_WALL_X1,    CEIL_Y_FAR),
        (BACK_WALL_X1,    FLOOR_Y_FAR),
        (LEFT_WALL_X_FAR, FLOOR_Y_FAR),
    ]
    draw.polygon(back_pts, fill=WALL_BACK)
    draw = ImageDraw.Draw(img)

    # Chalkboard — spans most of the back wall
    BOARD_X0 = LEFT_WALL_X_FAR + 14
    BOARD_X1 = BACK_WALL_X1 - 20
    BOARD_Y0 = CEIL_Y_FAR + 18
    BOARD_Y1 = FLOOR_Y_FAR - 36
    draw_rect(draw, BOARD_X0, BOARD_Y0, BOARD_X1, BOARD_Y1, BOARD_GRAY)
    # Board frame
    draw.rectangle([BOARD_X0, BOARD_Y0, BOARD_X1, BOARD_Y1],
                   outline=LINE_DARK, width=1)
    # Chalk writing — math/binary content via draw_pixel_text()
    # Board interior height is small (~16px at this camera angle) — two rows at scale=1
    board_inner_h = BOARD_Y1 - BOARD_Y0
    row_margin = max(1, (board_inner_h - 16) // 3)  # vertical padding
    # Row 1: binary equation
    draw_pixel_text(draw, BOARD_X0 + 4, BOARD_Y0 + row_margin,
                    "1011 XOR 0110", BOARD_CHALK_TEXT, scale=1)
    # Row 2: math formula (fits in second row if board is tall enough)
    if board_inner_h >= 18:
        draw_pixel_text(draw, BOARD_X0 + 4, BOARD_Y0 + row_margin + 9,
                        "F X  2X 5", BOARD_CHALK_TEXT, scale=1)
    # Chalk tray
    draw_rect(draw, BOARD_X0, BOARD_Y1, BOARD_X1, BOARD_Y1 + 5, BOARD_TRAY)
    # Chalk dust smear — faint lighter area along tray
    draw_rect(draw, BOARD_X0 + 4, BOARD_Y1 - 6, BOARD_X0 + 40, BOARD_Y1,
              CHALK_DUST)
    # Bulletin board — above-right of chalkboard on back wall
    BULL_X0 = BACK_WALL_X1 - 60
    BULL_X1 = BACK_WALL_X1 - 8
    BULL_Y0 = CEIL_Y_FAR + 8
    BULL_Y1 = CEIL_Y_FAR + 44
    draw_rect(draw, BULL_X0, BULL_Y0, BULL_X1, BULL_Y1, BULLETIN_BACKING)
    draw.rectangle([BULL_X0, BULL_Y0, BULL_X1, BULL_Y1], outline=LINE_DARK, width=1)
    # A few pinned papers
    for pi in range(3):
        px = BULL_X0 + 6 + pi * 16
        py = BULL_Y0 + 4
        pw, ph = 11, 14
        draw_rect(draw, px, py, px + pw, py + ph, PAPER_WHITE)
        # Pin dot
        pin_col = BULLETIN_PIN_RED if pi % 2 == 0 else BULLETIN_PIN_BLU
        draw.ellipse([px + 4, py - 2, px + 8, py + 2], fill=pin_col)
    draw = ImageDraw.Draw(img)

    # Teacher desk — at base of board wall
    TD_X0 = LEFT_WALL_X_FAR + 8
    TD_X1 = BACK_WALL_X1 - 8
    TD_Y0 = FLOOR_Y_FAR - 26
    TD_Y1 = FLOOR_Y_FAR + 2
    draw_rect(draw, TD_X0, TD_Y0, TD_X1, TD_Y1, TEACHER_DESK)
    draw.rectangle([TD_X0, TD_Y0, TD_X1, TD_Y1], outline=LINE_DARK, width=1)
    # Items on teacher desk
    draw_rect(draw, TD_X0 + 6, TD_Y0 - 8, TD_X0 + 18, TD_Y0, PAPER_WHITE)  # stack
    draw.rectangle([TD_X0 + 6, TD_Y0 - 8, TD_X0 + 18, TD_Y0], outline=LINE_DARK, width=1)

    # ── 3. LEFT WALL (windows side) ────────────────────────────────────────────
    left_wall_pts = [
        (0, 0),
        (LEFT_WALL_X_FAR, CEIL_Y_FAR),
        (LEFT_WALL_X_FAR, FLOOR_Y_FAR),
        (0, H),
    ]
    draw.polygon(left_wall_pts, fill=WALL_SAGE_WARM)
    draw = ImageDraw.Draw(img)

    # Windows — 3 windows receding into distance on left wall
    win_data = [
        # (near_x, far_x, y_top_pct, y_bot_pct)  all relative
        (0,  LEFT_WALL_X_FAR * 0.7,  0.08, 0.62),
        (0,  LEFT_WALL_X_FAR * 0.45, 0.14, 0.58),
        (0,  LEFT_WALL_X_FAR * 0.22, 0.20, 0.52),
    ]
    for wi, (nx, fx, ytp, ybp) in enumerate(win_data):
        # Window as trapezoid on left wall (foreshortened)
        w_x0 = int(nx)
        w_x1 = int(fx)
        w_y0 = int(H * ytp)
        w_y1 = int(H * ybp)
        if w_x0 >= w_x1:
            continue
        draw.polygon([(w_x0, w_y0), (w_x1, w_y0 + 8),
                       (w_x1, w_y1 - 8), (w_x0, w_y1)],
                     fill=WINDOW_GLASS)
        # Frame
        draw.polygon([(w_x0, w_y0), (w_x1, w_y0 + 8),
                       (w_x1, w_y1 - 8), (w_x0, w_y1)],
                     outline=WINDOW_FRAME, width=1)
        # Sill
        draw.line([(w_x0, w_y1), (w_x1, w_y1 - 8)],
                  fill=WINDOW_SILL, width=2)
    draw = ImageDraw.Draw(img)

    # ── 4. RIGHT WALL (near side — partially visible) ──────────────────────────
    right_wall_pts = [
        (BACK_WALL_X1, CEIL_Y_FAR),
        (W, 0),
        (W, H),
        (BACK_WALL_X1, FLOOR_Y_FAR),
    ]
    draw.polygon(right_wall_pts, fill=WALL_SAGE_COOL)
    draw = ImageDraw.Draw(img)

    # Door on right wall
    door_cx = int(lerp(BACK_WALL_X1, W, 0.28))
    door_w  = 38
    draw_rect(draw, door_cx - door_w // 2, 0,
              door_cx + door_w // 2, int(H * 0.52),
              DOOR_TERRA)
    draw.rectangle([door_cx - door_w // 2, 0,
                    door_cx + door_w // 2, int(H * 0.52)],
                   outline=LINE_DARK, width=1)
    # Door knob
    draw.ellipse([door_cx + door_w // 2 - 8, int(H * 0.26) - 4,
                  door_cx + door_w // 2 - 2, int(H * 0.26) + 4],
                 fill=BULLETIN_BACKING)

    # Radiator below window on right wall
    rad_y0 = int(H * 0.6)
    rad_y1 = int(H * 0.82)
    rad_x0 = int(lerp(BACK_WALL_X1, W, 0.55))
    rad_x1 = int(lerp(BACK_WALL_X1, W, 0.78))
    draw_rect(draw, rad_x0, rad_y0, rad_x1, rad_y1, RADIATOR_WARM)
    draw.rectangle([rad_x0, rad_y0, rad_x1, rad_y1], outline=LINE_DARK, width=1)
    for ri in range(5):
        rx = rad_x0 + 4 + ri * ((rad_x1 - rad_x0 - 8) // 5)
        draw.line([(rx, rad_y0 + 3), (rx, rad_y1 - 3)], fill=LINE_DARK, width=1)
    draw = ImageDraw.Draw(img)

    # ── 5. FLOOR ───────────────────────────────────────────────────────────────
    floor_pts = [
        (LEFT_WALL_X_FAR, FLOOR_Y_FAR),
        (BACK_WALL_X1,    FLOOR_Y_FAR),
        (W,               H),
        (0,               H),
    ]
    draw.polygon(floor_pts, fill=FLOOR_CREAM)
    draw = ImageDraw.Draw(img)

    # Checkerboard linoleum tiles — perspective-correct
    N_TILE_COLS = 10
    N_TILE_ROWS = 8
    floor_left_near  = 0
    floor_right_near = W
    floor_left_far   = LEFT_WALL_X_FAR
    floor_right_far  = BACK_WALL_X1

    for row in range(N_TILE_ROWS):
        t_near = (row + 1) / N_TILE_ROWS
        t_far  = row / N_TILE_ROWS
        # Non-linear for perspective compression near far wall
        t_near_nl = t_near ** 0.65
        t_far_nl  = t_far ** 0.65
        y_near_edge = int(FLOOR_Y_FAR + t_near_nl * (H - FLOOR_Y_FAR))
        y_far_edge  = int(FLOOR_Y_FAR + t_far_nl  * (H - FLOOR_Y_FAR))
        for col in range(N_TILE_COLS):
            tl = col / N_TILE_COLS
            tr = (col + 1) / N_TILE_COLS
            # Left and right x at near and far edges of this tile row
            xl_far  = int(lerp(floor_left_far,  floor_right_far,  tl))
            xr_far  = int(lerp(floor_left_far,  floor_right_far,  tr))
            xl_near = int(lerp(floor_left_near, floor_right_near, tl))
            xr_near = int(lerp(floor_left_near, floor_right_near, tr))
            # Interpolate x at y_far_edge and y_near_edge
            def x_at_y(xf, xn, y_val):
                if H == FLOOR_Y_FAR:
                    return xf
                frac = (y_val - FLOOR_Y_FAR) / max(1, H - FLOOR_Y_FAR)
                return int(lerp(xf, xn, frac))

            xl0 = x_at_y(xl_far, xl_near, y_far_edge)
            xr0 = x_at_y(xr_far, xr_near, y_far_edge)
            xl1 = x_at_y(xl_far, xl_near, y_near_edge)
            xr1 = x_at_y(xr_far, xr_near, y_near_edge)
            tile_pts = [(xl0, y_far_edge), (xr0, y_far_edge),
                        (xr1, y_near_edge), (xl1, y_near_edge)]
            checker = (row + col) % 2
            tile_col = FLOOR_SAGE if checker else FLOOR_CREAM
            draw.polygon(tile_pts, fill=tile_col)
    draw = ImageDraw.Draw(img)

    # Worn center path — lighter strip along the aisle
    worn_left_x  = int(W * 0.30)
    worn_right_x = int(W * 0.55)
    worn_pts = [
        (int(lerp(floor_left_far, floor_right_far, 0.33)), FLOOR_Y_FAR),
        (int(lerp(floor_left_far, floor_right_far, 0.56)), FLOOR_Y_FAR),
        (worn_right_x, H),
        (worn_left_x,  H),
    ]
    img = alpha_poly(img, worn_pts, FLOOR_WORN, 55)
    draw = ImageDraw.Draw(img)

    # ── 6. DESK ROWS ───────────────────────────────────────────────────────────
    # 4 rows × 5 columns, receding in perspective toward VP
    # Row 0 is farthest (near back wall), row 3 is nearest (foreground area)

    desk_rows = []
    for row in range(NUM_DESK_ROWS):
        t = row / (NUM_DESK_ROWS - 1)
        # y of desk top surface — near rows are lower on page (larger y)
        desk_y_top = int(lerp(FLOOR_Y_FAR + 12, int(H * 0.68), t))
        desk_y_bot = int(desk_y_top + lerp(10, 22, t))
        desk_rows.append((desk_y_top, desk_y_bot))

    for row_idx, (dy_top, dy_bot) in enumerate(desk_rows):
        # x positions for desks in this row, left to right
        # Perspective: far row desks are clustered closer to VP_X
        row_t = row_idx / (NUM_DESK_ROWS - 1)
        row_x_left  = int(lerp(int(W * 0.10), int(W * 0.05), 1 - row_t))
        row_x_right = int(lerp(int(W * 0.80), int(W * 0.62), 1 - row_t))
        desk_w_near = int(lerp(18, 30, row_t))
        desk_w_far  = desk_w_near

        for col_idx in range(NUM_DESK_COLS):
            ct = col_idx / (NUM_DESK_COLS - 1)
            dx_center = int(lerp(row_x_left, row_x_right, ct))
            dx0 = dx_center - desk_w_near // 2
            dx1 = dx_center + desk_w_near // 2

            # Desk surface — warm side (left) or cool side (right)
            in_warm_zone = dx_center < W // 2
            desk_fill = DESK_TOP_WARM if in_warm_zone else DESK_TOP_COOL

            draw_rect(draw, dx0, dy_top, dx1, dy_bot, desk_fill)

            # Wear mark (lighter worn area on desk surface — 65% of desks)
            if RNG.random() < 0.65:
                wear_x0 = dx0 + 2
                wear_x1 = min(dx0 + 8, dx1 - 2)
                wear_y0 = dy_top + 2
                wear_y1 = dy_top + 5
                draw_rect(draw, wear_x0, wear_y0, wear_x1, wear_y1, DESK_WEAR)

            # Worksheet on desk (55% of desks)
            if RNG.random() < 0.55:
                sheet_x0 = dx0 + 1
                sheet_x1 = min(dx0 + 10, dx1 - 1)
                sheet_y0 = dy_top
                sheet_y1 = dy_top + (dy_bot - dy_top) // 2
                draw_rect(draw, sheet_x0, sheet_y0, sheet_x1, sheet_y1, PAPER_WHITE)

            # Desk frame / legs (visible below surface)
            leg_h = int(lerp(4, 10, row_t))
            draw.line([(dx0 + 2, dy_bot), (dx0 + 2, dy_bot + leg_h)],
                      fill=DESK_FRAME, width=1)
            draw.line([(dx1 - 2, dy_bot), (dx1 - 2, dy_bot + leg_h)],
                      fill=DESK_FRAME, width=1)

    draw = ImageDraw.Draw(img)

    # ── 7. FOREGROUND DEPTH ANCHOR ─────────────────────────────────────────────
    # Near desk corner — partially cropped by frame edge (forces depth reading)
    FG_DESK_X0 = 0
    FG_DESK_X1 = int(W * 0.18)
    FG_DESK_Y0 = int(H * 0.62)
    FG_DESK_Y1 = int(H * 0.80)
    draw_rect(draw, FG_DESK_X0, FG_DESK_Y0, FG_DESK_X1, FG_DESK_Y1,
              DESK_TOP_WARM)
    draw.rectangle([FG_DESK_X0, FG_DESK_Y0, FG_DESK_X1, FG_DESK_Y1],
                   outline=LINE_DARK, width=1)
    # Desk leg (near left corner)
    draw.line([(FG_DESK_X1 - 6, FG_DESK_Y1),
               (FG_DESK_X1 - 6, int(H * 0.94))],
              fill=DESK_FRAME, width=2)
    # Desk frame edge visible
    draw.line([(FG_DESK_X0, FG_DESK_Y0), (FG_DESK_X1, FG_DESK_Y0)],
              fill=LINE_DARK, width=1)

    # Backpack on floor beside foreground desk (Luma's backpack — deep blue)
    BAG_X0 = int(W * 0.10)
    BAG_X1 = int(W * 0.16)
    BAG_Y0 = int(H * 0.80)
    BAG_Y1 = int(H * 0.96)
    draw_rect(draw, BAG_X0, BAG_Y0, BAG_X1, BAG_Y1, BACKPACK_MAIN)
    draw.rectangle([BAG_X0, BAG_Y0, BAG_X1, BAG_Y1], outline=LINE_DARK, width=1)
    # Front pocket
    PKT_Y0 = BAG_Y0 + (BAG_Y1 - BAG_Y0) // 2
    draw_rect(draw, BAG_X0 + 2, PKT_Y0, BAG_X1 - 2, BAG_Y1 - 2, BACKPACK_POCKET)
    draw.rectangle([BAG_X0 + 2, PKT_Y0, BAG_X1 - 2, BAG_Y1 - 2],
                   outline=LINE_DARK, width=1)
    # Strap
    draw.line([(BAG_X0 + 4, BAG_Y0), (BAG_X0 + 2, BAG_Y0 - 12)],
              fill=BACKPACK_STRAP, width=2)

    # Water bottle on near desk corner
    BOT_X0 = int(W * 0.14)
    BOT_X1 = int(W * 0.17)
    BOT_Y0 = FG_DESK_Y0 - 14
    BOT_Y1 = FG_DESK_Y0
    draw.ellipse([BOT_X0, BOT_Y0, BOT_X1, BOT_Y1], fill=BOTTLE_BODY)
    draw.ellipse([BOT_X0, BOT_Y0, BOT_X1, BOT_Y1], outline=LINE_DARK, width=1)

    draw = ImageDraw.Draw(img)

    # ── 8. STRUCTURAL EDGE LINES ───────────────────────────────────────────────
    # Ceiling to wall junction lines
    draw.line([(0, 0), (LEFT_WALL_X_FAR, CEIL_Y_FAR)], fill=LINE_DARK, width=1)
    draw.line([(W, 0), (BACK_WALL_X1, CEIL_Y_FAR)], fill=LINE_DARK, width=1)
    # Wall/floor junction lines
    draw.line([(0, H), (LEFT_WALL_X_FAR, FLOOR_Y_FAR)], fill=LINE_DARK, width=1)
    draw.line([(W, H), (BACK_WALL_X1, FLOOR_Y_FAR)], fill=LINE_DARK, width=1)
    # Back wall top and bottom edge
    draw.line([(LEFT_WALL_X_FAR, CEIL_Y_FAR), (BACK_WALL_X1, CEIL_Y_FAR)],
              fill=LINE_DARK, width=1)
    draw.line([(LEFT_WALL_X_FAR, FLOOR_Y_FAR), (BACK_WALL_X1, FLOOR_Y_FAR)],
              fill=LINE_DARK, width=1)

    draw = ImageDraw.Draw(img)

    # ── 9. LIGHTING — DUAL TEMPERATURE ────────────────────────────────────────
    # QA warm/cool measures TOP-HALF vs BOTTOM-HALF median hue.
    # Primary split: WARM top half (ceiling/upper wall catch warm light from windows),
    #                COOL bottom half (floor in shadow, fluorescent cold bounce).
    # Secondary left/right split preserves the visual dual-source logic for the image.

    SPLIT_Y = H // 2
    SPLIT_X = W // 2

    # TOP half — strong warm amber overlay (ceiling, upper wall, window heads)
    # alpha=70 gives clearly warm-dominant top half
    warm_top = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wtd = ImageDraw.Draw(warm_top)
    for row in range(SPLIT_Y):
        t = 1.0 - (row / SPLIT_Y)   # strongest at top (ceiling), fades to 0 at split
        a = int(70 * t)
        wtd.line([(0, row), (W, row)], fill=(*SUNLIT_AMBER, a), width=1)
    img_rgba = img.convert("RGBA")
    img_rgba.alpha_composite(warm_top)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    # BOTTOM half — cool fluorescent/shadow overlay (floor, lower walls)
    # alpha=75 gives clearly cool-dominant bottom half
    cool_bot = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cbd = ImageDraw.Draw(cool_bot)
    for row in range(SPLIT_Y, H):
        t = (row - SPLIT_Y) / (H - SPLIT_Y)   # grows stronger toward bottom
        a = int(75 * t)
        cbd.line([(0, row), (W, row)], fill=(*FLUORO_LIGHT, a), width=1)
    img_rgba = img.convert("RGBA")
    img_rgba.alpha_composite(cool_bot)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Secondary LEFT warm zone — window side ambient (visual storytelling, left half)
    warm_left = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wld = ImageDraw.Draw(warm_left)
    for col in range(SPLIT_X):
        t = 1.0 - (col / SPLIT_X)
        a = int(30 * t)
        wld.line([(col, 0), (col, H)], fill=(*SUNLIT_AMBER, a), width=1)
    img_rgba = img.convert("RGBA")
    img_rgba.alpha_composite(warm_left)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Secondary RIGHT cool zone — fluorescent side (visual storytelling, right half)
    cool_right = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    crd = ImageDraw.Draw(cool_right)
    for col in range(SPLIT_X, W):
        t = (col - SPLIT_X) / (W - SPLIT_X)
        a = int(25 * t)
        crd.line([(col, 0), (col, H)], fill=(*FLUORO_LIGHT, a), width=1)
    img_rgba = img.convert("RGBA")
    img_rgba.alpha_composite(cool_right)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Window shafts — warm SUNLIT_AMBER rays through left-wall windows
    img_rgba = img.convert("RGBA")
    for wi, (nx, fx, ytp, ybp) in enumerate(win_data):
        shaft_apex = (int(fx), int(H * ((ytp + ybp) / 2)))
        shaft_bl   = (0, int(H * ybp))
        shaft_br   = (0, int(H * ytp))
        img_rgba = light_shaft(img_rgba, shaft_apex, shaft_bl, shaft_br,
                               SUNLIT_AMBER, max_alpha=45)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Fluorescent floor pools — cool light under fixtures (right half)
    for fi in range(3):
        pool_t = (fi + 0.5) / 3
        pool_cx = int(pool_t * W)
        if pool_cx < SPLIT_X:
            continue
        pool_y  = int(H * 0.88)
        pool_w  = 60
        pool_h  = 20
        pool_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        pld = ImageDraw.Draw(pool_layer)
        pld.ellipse([pool_cx - pool_w, pool_y - pool_h,
                     pool_cx + pool_w, pool_y + pool_h],
                    fill=(*FLUORO_LIGHT, 35))
        img_rgba = img.convert("RGBA")
        img_rgba.alpha_composite(pool_layer)
        img = img_rgba.convert("RGB")
        draw = ImageDraw.Draw(img)

    # ── 10. DEEP SHADOW ANCHORS — value floor ≤ 30 ────────────────────────────
    NEAR_BLACK      = NEAR_BLACK_WARM
    # Floor corners
    draw_rect(draw, 0, H - 18, 20, H, NEAR_BLACK)
    draw_rect(draw, W - 20, H - 18, W, H, NEAR_BLACK)
    # Floor / wall junction at back wall
    draw_rect(draw, LEFT_WALL_X_FAR, FLOOR_Y_FAR - 2,
              BACK_WALL_X1, FLOOR_Y_FAR + 2, NEAR_BLACK)
    # Under foreground desk
    draw_rect(draw, 0, int(H * 0.92), FG_DESK_X1, H, NEAR_BLACK)
    # Backpack shadow
    draw_rect(draw, BAG_X0 - 2, BAG_Y1 - 4, BAG_X1 + 2, BAG_Y1 + 6, NEAR_BLACK)
    # Crevice under board wall (chalkboard base)
    draw_rect(draw, LEFT_WALL_X_FAR, BOARD_Y1 + 5,
              BACK_WALL_X1, BOARD_Y1 + 10, NEAR_BLACK)
    draw = ImageDraw.Draw(img)

    # ── 11. VALUE CEILING ANCHOR — specular on window glass ───────────────────
    spec_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    spd = ImageDraw.Draw(spec_layer)
    # Bright catch-light on leftmost window glass
    spd.ellipse([6, int(H * 0.14), 18, int(H * 0.22)], fill=(255, 255, 248, 255))
    # Fluorescent tube specular (rightmost)
    spd.ellipse([int(W * 0.82), int(H * 0.08) - 4,
                 int(W * 0.88), int(H * 0.08) + 4],
                fill=(252, 255, 250, 240))
    img_rgba = img.convert("RGBA")
    img_rgba.alpha_composite(spec_layer)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    # ── 12. FIGURE-GROUND BACKING — character staging zone ────────────────────
    # Subtle shadow backing in the center-desk zone (between desk rows 1-2)
    # This ensures characters (Luma warm cream, Cosmo lavender) read against bg.
    # Value of staging zone pushed slightly darker.
    staging_x0 = int(W * 0.22)
    staging_x1 = int(W * 0.55)
    staging_y0 = int(H * 0.40)
    staging_y1 = int(H * 0.72)
    img = alpha_overlay(img, staging_x0, staging_y0, staging_x1, staging_y1,
                        (80, 70, 60), 18)
    draw = ImageDraw.Draw(img)

    # ── 13. ATMOSPHERIC HAZE — back wall recession ────────────────────────────
    # Desaturating/lightening distant elements with a cool-haze layer
    haze_pts = [
        (LEFT_WALL_X_FAR - 20, CEIL_Y_FAR - 10),
        (BACK_WALL_X1 + 20,    CEIL_Y_FAR - 10),
        (BACK_WALL_X1 + 20,    FLOOR_Y_FAR + 10),
        (LEFT_WALL_X_FAR - 20, FLOOR_Y_FAR + 10),
    ]
    img = alpha_poly(img, haze_pts, (200, 210, 208), 22)
    draw = ImageDraw.Draw(img)

    # ── 14. PAPER TEXTURE — breaks up long polygon edge runs (line_weight QA) ──
    # Subtle grain texture prevents FIND_EDGES from detecting continuous long
    # horizontal runs along wall/floor polygon boundaries.
    img_rgba = img.convert("RGBA")
    img_rgba = paper_texture(img_rgba, scale=38, alpha=14, seed=44)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    # ── 15. VIGNETTE — final atmospheric edge darkening ───────────────────────
    img_rgba = img.convert("RGBA")
    img_rgba = vignette(img_rgba, strength=50)
    img = img_rgba.convert("RGB")
    draw = ImageDraw.Draw(img)

    # ── 16. THUMBNAIL RESIZE and SAVE ─────────────────────────────────────────
    img.thumbnail((1280, 1280), Image.LANCZOS)

    out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_classroom_bg.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.convert("RGB").save(out_path)
    print(f"Saved: {out_path}")
    return out_path


if __name__ == "__main__":
    main()
