#!/usr/bin/env python3
"""
LTG_TOOL_bg_school_hallway_v001.py — Millbrook School Hallway Background
"Luma & the Glitchkin" — Background & Environment Design
Artist: Jordan Reed | Cycle 17

Used in: A1-03, A1-05 (Act 1 transition / locker scenes)
Narrative: Mundane school interior. Normal life before the Glitchkin adventure.
           The real world at its most institutional.

Tone: Fluorescent cool-green institutional lighting + warm window shafts.
      3-point perspective, slight low angle (hallway feels large).
      Real World palette ONLY — zero Glitch palette.

Environment spec:
  - Rows of metal lockers both sides (two alternating colors: sage + dusty lavender)
  - Linoleum floor: cream + sage checkerboard tile pattern with scuff marks
  - Fluorescent overhead lights — slightly greenish cool cast
  - Bulletin boards above lockers with posters, hand-lettered club signs
  - Windows at far end — daylight pulling focus forward
  - T-intersection at end with school seal on wall
  - Trophy case in background, "MMMS" banner on right wall

Camera: 3-point perspective. Low angle (camera ~4ft high) so hallway feels
        large and slightly imposing. Slight low-angle hero perspective.
        Viewer looks down the hallway toward the daylit far end.

Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_school_hallway_v001.png
"""

import math
import random
import os
from PIL import Image, ImageDraw

W, H = 1280, 720

# ── Real World Palette (NO Glitch colors) ────────────────────────────────────
# Walls
WALL_LAVENDER     = (168, 155, 191)   # RW-08 dusty lavender — hallway walls
WALL_SHADOW       = (120, 108, 145)   # wall in shadow
WALL_NEAR         = (185, 172, 205)   # near wall, slightly brighter

# Ceiling
CEIL_TILE         = (216, 212, 192)   # acoustic tile (aged cream, RW spec)
CEIL_GRID         = (144, 152, 152)   # ceiling grid metal (cool silver-grey)
CEIL_FIXTURE      = (232, 240, 232)   # fluorescent fixture (near white, slight green)

# Floor
FLOOR_CREAM       = (216, 206, 176)   # cream tile (RW spec D8CEB0 adjusted)
FLOOR_SAGE        = (138, 158, 136)   # sage tile (RW spec 8A9E88 adjusted)
FLOOR_WORN_PATH   = (228, 220, 192)   # worn center path (lighter/more reflective)
FLOOR_FLUORO_ZONE = (208, 220, 208)   # floor under fluorescent (cool green cast)
FLOOR_WIN_ZONE    = (232, 216, 168)   # floor under window light (warm amber cast)
FLOOR_SCUFF       = (190, 178, 148)   # scuff marks (darker than floor)

# Fluorescent light on floor
FLUORO_POOL       = (220, 235, 220)   # soft oval light pool under each fixture

# Window daylight (far end)
WIN_DAYLIGHT      = (210, 230, 245)   # windows at T-intersection: sky
WIN_GLOW          = (240, 235, 200)   # warm daylight glow from far end
SUNLIGHT_SHAFT    = (232, 201,  90)   # RW-02 soft gold — light shaft from side window

# Lockers (two alternating colors)
LOCKER_SAGE       = (122, 154, 122)   # primary locker color (sage green faded)
LOCKER_SAGE_DARK  = ( 74, 107,  78)   # locker shadow side
LOCKER_LAV        = (168, 155, 191)   # accent locker color (dusty lavender)
LOCKER_LAV_DARK   = (120, 108, 145)   # lavender locker shadow
LOCKER_VENT       = ( 74,  96,  74)   # locker vent slots (dark sage)
LOCKER_HANDLE     = (144, 144, 144)   # locker handle (cool grey metal)
LOCKER_NUM        = (220, 212, 190)   # locker number tag (pale cream)
LOCKER_STICKER_R  = (188,  72,  52)   # sticker accent red
LOCKER_STICKER_Y  = (210, 178,  68)   # sticker accent yellow
LOCKER_BACKPACK   = ( 92, 112, 148)   # backpack hanging on handle (blue-grey)

# Bulletin board
BULLETIN_CORK     = (192, 168, 112)   # cork board natural tan
BULLETIN_PAPER    = (200, 168,  80)   # faded goldenrod backing paper
POSTER_BG1        = (118, 148, 118)   # poster — sage green
POSTER_BG2        = (185, 130,  88)   # poster — warm orange
POSTER_BG3        = (148, 128, 172)   # poster — lavender
POSTER_TEXT       = (240, 232, 210)   # poster text (pale cream)

# Banner
BANNER_FADED      = (190, 176, 160)   # "MILLBROOK MIDDLE" banner faded

# T-intersection far wall
FAR_WALL          = (220, 210, 185)   # far hallway end wall (warm cream — daylit)
SCHOOL_SEAL_BG    = (180, 162, 128)   # school seal circle
SCHOOL_SEAL_RING  = (140, 118,  82)   # seal border

# Trophy case
TROPHY_GLASS      = (190, 208, 220)   # glass front (cool blue-grey)
TROPHY_FRAME      = ( 90,  80,  65)   # trophy case wood frame
TROPHY_GOLD       = (200, 172,  68)   # trophy body (warm gold)

# Door (terracotta per spec)
DOOR_COLOR        = (192,  88,  56)   # RW-04 terracotta (C05838 adjusted)
DOOR_SHADOW       = (140,  58,  34)   # RW-05 rust shadow
DOOR_GLASS        = (176, 196, 208)   # door window glass (cool grey)

# Shadow / line tones
LINE_DARK         = ( 59,  40,  32)   # RW-11 Deep Cocoa
FLUORO_SHADOW     = (122, 144, 128)   # fluorescent zone shadows (cool sage-grey)
WIN_SHADOW        = (168, 155, 191)   # window zone shadows (dusty lavender)

# ── Perspective helpers ───────────────────────────────────────────────────────

rng = random.Random(88)

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))

def lerp_pt(p1, p2, t):
    return (lerp(p1[0], p2[0], t), lerp(p1[1], p2[1], t))

def draw_rect(draw, x0, y0, x1, y1, fill, outline=None, width=1):
    draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)

def soft_overlay(img, x0, y0, x1, y1, color, max_alpha=50):
    """Soft rectangular glow overlay."""
    if x1 <= x0 or y1 <= y0:
        return
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    w_ = x1 - x0
    h_ = y1 - y0
    steps = 10
    for i in range(steps):
        t = i / steps
        a = int(max_alpha * (1.0 - t))
        shrink_x = int(w_ * t * 0.5)
        shrink_y = int(h_ * t * 0.5)
        rx0 = x0 + shrink_x
        ry0 = y0 + shrink_y
        rx1 = x1 - shrink_x
        ry1 = y1 - shrink_y
        if rx1 > rx0 and ry1 > ry0:
            ld.rectangle([rx0, ry0, rx1, ry1], fill=color + (a,))
    img.alpha_composite(layer)

def gradient_rect_h(img, x0, y0, x1, y1, col_l, col_r):
    if x1 <= x0 or y1 <= y0:
        return
    w_ = x1 - x0
    h_ = y1 - y0
    layer = Image.new("RGBA", (w_, h_), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for col in range(w_):
        t = col / max(w_ - 1, 1)
        c = lerp_color(col_l, col_r, t)
        ld.line([(col, 0), (col, h_ - 1)], fill=c + (255,), width=1)
    img.alpha_composite(layer, dest=(x0, y0))

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


# ── Main draw function ────────────────────────────────────────────────────────

def draw_school_hallway():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # ── PERSPECTIVE SETUP ─────────────────────────────────────────────────────
    # 3-point perspective. Camera low (slight upward tilt — hallway feels large).
    # Primary VP: center of far end (where T-intersection / windows are)
    # Secondary VPs: off-frame left and right for locker walls
    # Camera eye-level ~= lower 35% of frame height (low angle)

    VP_CX = W // 2        # center VP X (far end)
    VP_CY = int(H * 0.40) # center VP Y (horizon line, low-ish angle)

    # Near floor corners
    FL_NEAR_L = (0,      H)
    FL_NEAR_R = (W,      H)
    # Far floor line (at T-intersection)
    FAR_W = 180           # width of hallway at far end (perspective-narrowed)
    FAR_H_FLOOR = VP_CY + 75   # far floor Y
    FAR_H_CEIL  = VP_CY - 130  # far ceiling Y

    FL_FAR_L  = (VP_CX - FAR_W // 2, FAR_H_FLOOR)
    FL_FAR_R  = (VP_CX + FAR_W // 2, FAR_H_FLOOR)
    CEIL_FAR_L = (VP_CX - FAR_W // 2 - 8, FAR_H_CEIL)
    CEIL_FAR_R = (VP_CX + FAR_W // 2 + 8, FAR_H_CEIL)
    CEIL_NEAR_L = (0, int(H * 0.12))
    CEIL_NEAR_R = (W, int(H * 0.12))

    # Wall top and bottom perspective lines (left wall and right wall)
    # Left wall: from near-left to far-left
    WALL_L_TOP_NEAR = (0, int(H * 0.12))
    WALL_L_TOP_FAR  = FL_FAR_L
    WALL_L_BOT_NEAR = FL_NEAR_L
    WALL_L_BOT_FAR  = FL_FAR_L

    WALL_R_TOP_NEAR = (W, int(H * 0.12))
    WALL_R_TOP_FAR  = FL_FAR_R
    WALL_R_BOT_NEAR = FL_NEAR_R
    WALL_R_BOT_FAR  = FL_FAR_R

    # ── 1. FLOOR ──────────────────────────────────────────────────────────────
    floor_pts = [FL_NEAR_L, FL_NEAR_R, FL_FAR_R, FL_FAR_L]
    draw.polygon(floor_pts, fill=FLOOR_CREAM)
    draw = ImageDraw.Draw(img)

    # Floor tiles — checkerboard, perspective-projected rows and columns
    # Rows recede toward VP
    n_rows = 18
    n_cols = 12
    # Build row Y positions (perspective spacing — closer = larger gaps)
    row_ys = []
    for i in range(n_rows + 1):
        t = i / n_rows
        # Non-linear — more spacing at near end
        t_persp = t ** 0.6
        y = int(lerp(FL_FAR_L[1], FL_NEAR_L[1], t_persp))
        row_ys.append(y)

    # For each row, compute left and right X by interpolating wall lines
    def wall_x_at_y(y, near_pt, far_pt):
        """Find X on a perspective wall line at a given Y."""
        if far_pt[1] == near_pt[1]:
            return near_pt[0]
        t = (y - near_pt[1]) / (far_pt[1] - near_pt[1])
        t = max(0, min(1, t))
        return lerp(near_pt[0], far_pt[0], t)

    def floor_left_x(y):
        return wall_x_at_y(y, FL_NEAR_L, FL_FAR_L)

    def floor_right_x(y):
        return wall_x_at_y(y, FL_NEAR_R, FL_FAR_R)

    for ri in range(n_rows):
        y_near = row_ys[ri + 1]
        y_far  = row_ys[ri]
        xl_near = floor_left_x(y_near)
        xr_near = floor_right_x(y_near)
        xl_far  = floor_left_x(y_far)
        xr_far  = floor_right_x(y_far)
        for ci in range(n_cols):
            tl = ci / n_cols
            tr = (ci + 1) / n_cols
            # Quad corners
            p_bl = (lerp(xl_near, xr_near, tl), y_near)
            p_br = (lerp(xl_near, xr_near, tr), y_near)
            p_tr = (lerp(xl_far,  xr_far,  tr), y_far)
            p_tl = (lerp(xl_far,  xr_far,  tl), y_far)
            is_sage = (ri + ci) % 2 == 1
            tile_col = FLOOR_SAGE if is_sage else FLOOR_CREAM
            draw.polygon([p_bl, p_br, p_tr, p_tl], fill=tile_col)

    # Worn center path overlay (lighter strip down center)
    worn_pts = [
        (floor_left_x(H) + (floor_right_x(H) - floor_left_x(H)) * 0.28,     H),
        (floor_right_x(H) - (floor_right_x(H) - floor_left_x(H)) * 0.28,    H),
        (VP_CX + 25, FAR_H_FLOOR),
        (VP_CX - 25, FAR_H_FLOOR),
    ]
    worn_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(worn_layer)
    wd.polygon(worn_pts, fill=FLOOR_WORN_PATH + (60,))
    img.alpha_composite(worn_layer)
    draw = ImageDraw.Draw(img)

    # Scuff marks (random darkened tile patches near center)
    for _ in range(18):
        sx = int(rng.gauss(W // 2, 130))
        sy = rng.randint(FAR_H_FLOOR + 20, H - 50)
        sw = rng.randint(12, 40)
        sh = rng.randint(4, 12)
        scuff_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(scuff_layer)
        sd.ellipse([sx - sw, sy - sh, sx + sw, sy + sh],
                   fill=FLOOR_SCUFF + (55,))
        img.alpha_composite(scuff_layer)
        draw = ImageDraw.Draw(img)

    # ── 2. CEILING ────────────────────────────────────────────────────────────
    ceil_pts = [CEIL_NEAR_L, CEIL_NEAR_R, CEIL_FAR_R, CEIL_FAR_L]
    draw.polygon(ceil_pts, fill=CEIL_TILE)

    # Ceiling grid — metal strips, perspective
    # Cross strips (perpendicular to hallway)
    for ri in range(n_rows + 1):
        t = ri / n_rows
        t_p = t ** 0.6
        y = int(lerp(CEIL_FAR_L[1], CEIL_NEAR_L[1], t_p))
        xl = int(wall_x_at_y(y, CEIL_NEAR_L, CEIL_FAR_L))
        xr = int(wall_x_at_y(y, CEIL_NEAR_R, CEIL_FAR_R))
        draw.line([(xl, y), (xr, y)], fill=CEIL_GRID, width=1)

    # Lengthwise strips (parallel to hallway)
    for ci in range(n_cols + 1):
        t = ci / n_cols
        x_near = lerp(CEIL_NEAR_L[0], CEIL_NEAR_R[0], t)
        x_far  = lerp(CEIL_FAR_L[0],  CEIL_FAR_R[0],  t)
        draw.line([(int(x_near), CEIL_NEAR_L[1]),
                   (int(x_far),  CEIL_FAR_L[1])],
                  fill=CEIL_GRID, width=1)

    # Fluorescent light fixtures embedded in ceiling grid
    # Two parallel rows, evenly spaced
    n_fixtures = 8
    for fi in range(n_fixtures):
        t_near = (fi + 1) / (n_fixtures + 1)
        t_far  = (fi + 0.6) / (n_fixtures + 1)
        y_near = int(lerp(CEIL_FAR_L[1], CEIL_NEAR_L[1], t_near ** 0.5))
        y_far  = int(lerp(CEIL_FAR_L[1], CEIL_NEAR_L[1], t_far ** 0.5))
        # Width of ceiling at this y
        xl_n = int(wall_x_at_y(y_near, CEIL_NEAR_L, CEIL_FAR_L))
        xr_n = int(wall_x_at_y(y_near, CEIL_NEAR_R, CEIL_FAR_R))
        cw = xr_n - xl_n
        # Left fixture — ensure y0 <= y1
        fx0_l = int(xl_n + cw * 0.12)
        fx1_l = int(xl_n + cw * 0.30)
        fy_top = min(y_far, y_near)
        fy_bot = max(y_far, y_near)
        if fy_bot - fy_top >= 3 and fx1_l > fx0_l:
            draw_rect(draw, fx0_l, fy_top + 1, fx1_l, fy_bot - 1, CEIL_FIXTURE)
        # Right fixture
        fx0_r = int(xl_n + cw * 0.70)
        fx1_r = int(xl_n + cw * 0.88)
        if fy_bot - fy_top >= 3 and fx1_r > fx0_r:
            draw_rect(draw, fx0_r, fy_top + 1, fx1_r, fy_bot - 1, CEIL_FIXTURE)

        # Fluorescent pool on floor below each fixture
        floor_y_fi = int(lerp(FAR_H_FLOOR, H, t_near ** 0.5))
        floor_xl = int(floor_left_x(floor_y_fi))
        floor_xr = int(floor_right_x(floor_y_fi))
        pool_cx = (floor_xl + floor_xr) // 2
        pool_rx = (floor_xr - floor_xl) // 4
        pool_ry = max(12, (H - floor_y_fi) // 10 + 8)
        pool_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        pd = ImageDraw.Draw(pool_layer)
        pd.ellipse([pool_cx - pool_rx, floor_y_fi - pool_ry,
                    pool_cx + pool_rx, floor_y_fi + pool_ry],
                   fill=FLUORO_POOL + (55,))
        img.alpha_composite(pool_layer)
        draw = ImageDraw.Draw(img)

    # ── 3. LEFT WALL ──────────────────────────────────────────────────────────
    left_wall_pts = [
        WALL_L_TOP_NEAR,
        WALL_L_TOP_FAR,
        (FL_FAR_L[0], FAR_H_CEIL),
        FL_FAR_L,
        FL_NEAR_L,
        FL_NEAR_L,
    ]
    draw.polygon([WALL_L_TOP_NEAR, (FL_FAR_L[0], FAR_H_CEIL),
                  FL_FAR_L, FL_NEAR_L], fill=WALL_NEAR)

    # ── 4. RIGHT WALL ─────────────────────────────────────────────────────────
    draw.polygon([WALL_R_TOP_NEAR, (FL_FAR_R[0], FAR_H_CEIL),
                  FL_FAR_R, FL_NEAR_R], fill=WALL_LAVENDER)

    # ── 5. LOCKERS ────────────────────────────────────────────────────────────
    # Left wall lockers: from near to far, projecting inward
    # Right wall lockers: mirroring
    n_lockers_visible = 10   # per side

    def draw_locker_row(side="left"):
        """Draw a row of lockers on left or right wall."""
        for li in range(n_lockers_visible):
            # t=0 is near end, t=1 is far end
            t_near = li / n_lockers_visible
            t_far  = (li + 1) / n_lockers_visible

            # Locker base: floor-to-locker-top (lockers ~80% of wall height)
            # Project Y for top and bottom of locker face
            if side == "left":
                # Left wall: x goes from 0 (near) toward VP_CX (far)
                near_x = int(lerp(0,     FL_FAR_L[0], t_near))
                far_x  = int(lerp(0,     FL_FAR_L[0], t_far))
                near_floor_y = int(lerp(H, FL_FAR_L[1], t_near))
                far_floor_y  = int(lerp(H, FL_FAR_L[1], t_far))
                # Ceiling on left wall
                near_ceil_y  = int(lerp(CEIL_NEAR_L[1], CEIL_FAR_L[1], t_near))
                far_ceil_y   = int(lerp(CEIL_NEAR_L[1], CEIL_FAR_L[1], t_far))
            else:
                near_x = int(lerp(W,     FL_FAR_R[0], t_near))
                far_x  = int(lerp(W,     FL_FAR_R[0], t_far))
                near_floor_y = int(lerp(H, FL_FAR_R[1], t_near))
                far_floor_y  = int(lerp(H, FL_FAR_R[1], t_far))
                near_ceil_y  = int(lerp(CEIL_NEAR_R[1], CEIL_FAR_R[1], t_near))
                far_ceil_y   = int(lerp(CEIL_NEAR_R[1], CEIL_FAR_R[1], t_far))

            # Locker top = ~75% of wall height from floor
            locker_top_near = int(lerp(near_floor_y, near_ceil_y, 0.28))
            locker_top_far  = int(lerp(far_floor_y,  far_ceil_y,  0.28))

            # Alternate locker colors
            is_lav = (li % 3 == 2)
            locker_face_col = LOCKER_LAV if is_lav else LOCKER_SAGE
            locker_dark_col = LOCKER_LAV_DARK if is_lav else LOCKER_SAGE_DARK

            # Draw locker face quad
            locker_pts = [
                (near_x, near_floor_y),
                (far_x,  far_floor_y),
                (far_x,  locker_top_far),
                (near_x, locker_top_near),
            ]
            draw.polygon(locker_pts, fill=locker_face_col)

            # Locker edge / depth (thin dark strip on leading edge)
            edge_w = max(2, abs(far_x - near_x) // 6)
            if side == "left":
                edge_pts = [
                    (near_x, near_floor_y),
                    (near_x + edge_w, near_floor_y),
                    (near_x + edge_w, locker_top_near),
                    (near_x, locker_top_near),
                ]
            else:
                edge_pts = [
                    (near_x, near_floor_y),
                    (near_x - edge_w, near_floor_y),
                    (near_x - edge_w, locker_top_near),
                    (near_x, locker_top_near),
                ]
            draw.polygon(edge_pts, fill=locker_dark_col)

            # Locker vent slots (top and bottom of each locker)
            face_h = near_floor_y - locker_top_near
            face_w = abs(far_x - near_x)
            if face_w > 10 and face_h > 25:
                slot_y_top   = locker_top_near + max(4, face_h // 8)
                slot_y_bot   = near_floor_y    - max(4, face_h // 8)
                slot_w       = max(4, int(face_w * 0.55))
                if side == "left":
                    slot_x0 = near_x + max(2, int(face_w * 0.18))
                else:
                    slot_x0 = near_x - max(2, int(face_w * 0.73))
                # Top vent
                for sv in range(3):
                    vy = slot_y_top + sv * max(2, int(face_h * 0.025))
                    draw.line([(slot_x0, vy), (slot_x0 + slot_w, vy)],
                              fill=LOCKER_VENT, width=1)
                # Bottom vent
                for sv in range(3):
                    vy = slot_y_bot - sv * max(2, int(face_h * 0.025))
                    draw.line([(slot_x0, vy), (slot_x0 + slot_w, vy)],
                              fill=LOCKER_VENT, width=1)

                # Handle (small rectangle)
                handle_y = (locker_top_near + near_floor_y) // 2
                handle_cx = (near_x + far_x) // 2
                draw.rectangle([handle_cx - 3, handle_y - 6,
                                 handle_cx + 3, handle_y + 6],
                                fill=LOCKER_HANDLE, outline=LINE_DARK, width=1)

                # Locker number label (small rect near top)
                num_y = locker_top_near + max(3, face_h // 10)
                num_w = max(6, int(face_w * 0.35))
                draw.rectangle([handle_cx - num_w // 2, num_y,
                                 handle_cx + num_w // 2, num_y + max(4, face_h // 12)],
                                fill=LOCKER_NUM)

                # Occasional sticker on near lockers
                if li < 4 and rng.random() > 0.5:
                    stk_y = locker_top_near + face_h // 3
                    stk_col = rng.choice([LOCKER_STICKER_R, LOCKER_STICKER_Y])
                    draw.ellipse([handle_cx - 8, stk_y - 8,
                                  handle_cx + 8, stk_y + 8],
                                 fill=stk_col)

                # Backpack hanging on nearest locker handle
                if li == 0 and side == "right":
                    bp_cx = handle_cx
                    bp_y0 = handle_y + 6
                    bp_y1 = bp_y0 + max(20, face_h // 4)
                    draw.ellipse([bp_cx - max(10, face_w // 4), bp_y0,
                                  bp_cx + max(10, face_w // 4), bp_y1],
                                 fill=LOCKER_BACKPACK, outline=LINE_DARK, width=1)

            # Above-locker strip (bulletin board zone)
            # (will be drawn separately as bulletin boards)

    draw_locker_row("left")
    draw_locker_row("right")
    draw = ImageDraw.Draw(img)

    # ── 6. BULLETIN BOARDS (above lockers) ───────────────────────────────────
    # Strip above the lockers on both walls
    # Left wall bulletin board
    bb_strips = [
        # (wall side, t_start, t_end) — these are perspective t values
        ("left",  0.0, 0.5),
        ("right", 0.0, 0.5),
    ]

    def get_wall_band(side, t_near, t_far, fraction_top, fraction_bot):
        """Get a wall band quad between t_near and t_far, at fraction of wall."""
        if side == "left":
            nx = int(lerp(0, FL_FAR_L[0], t_near))
            fx = int(lerp(0, FL_FAR_L[0], t_far))
            n_floor = int(lerp(H, FL_FAR_L[1], t_near))
            f_floor = int(lerp(H, FL_FAR_L[1], t_far))
            n_ceil  = int(lerp(CEIL_NEAR_L[1], CEIL_FAR_L[1], t_near))
            f_ceil  = int(lerp(CEIL_NEAR_L[1], CEIL_FAR_L[1], t_far))
        else:
            nx = int(lerp(W, FL_FAR_R[0], t_near))
            fx = int(lerp(W, FL_FAR_R[0], t_far))
            n_floor = int(lerp(H, FL_FAR_R[1], t_near))
            f_floor = int(lerp(H, FL_FAR_R[1], t_far))
            n_ceil  = int(lerp(CEIL_NEAR_R[1], CEIL_FAR_R[1], t_near))
            f_ceil  = int(lerp(CEIL_NEAR_R[1], CEIL_FAR_R[1], t_far))
        n_top = int(lerp(n_floor, n_ceil, fraction_top))
        f_top = int(lerp(f_floor, f_ceil, fraction_top))
        n_bot = int(lerp(n_floor, n_ceil, fraction_bot))
        f_bot = int(lerp(f_floor, f_ceil, fraction_bot))
        return [(nx, n_bot), (fx, f_bot), (fx, f_top), (nx, n_top)]

    # Left bulletin board strip (above lockers, below ceiling)
    for t_s in [0.0, 0.15, 0.30]:
        t_e = t_s + 0.15
        bb_pts = get_wall_band("left", t_s, t_e, 0.65, 0.90)
        draw.polygon(bb_pts, fill=BULLETIN_PAPER)
        # Poster shapes on bulletin board
        mid_t = (t_s + t_e) / 2
        poster_pts = get_wall_band("left", t_s + 0.02, t_e - 0.02, 0.67, 0.88)
        p_col = rng.choice([POSTER_BG1, POSTER_BG2, POSTER_BG3])
        draw.polygon(poster_pts, fill=p_col)

    # Right bulletin board strip
    for t_s in [0.0, 0.15, 0.30]:
        t_e = t_s + 0.15
        bb_pts = get_wall_band("right", t_s, t_e, 0.65, 0.90)
        draw.polygon(bb_pts, fill=BULLETIN_PAPER)
        poster_pts = get_wall_band("right", t_s + 0.02, t_e - 0.02, 0.67, 0.88)
        p_col = rng.choice([POSTER_BG1, POSTER_BG2, POSTER_BG3])
        draw.polygon(poster_pts, fill=p_col)

    # "MILLBROOK MIDDLE" banner on right wall (upper strip, faded)
    banner_pts = get_wall_band("right", 0.05, 0.45, 0.90, 0.98)
    draw.polygon(banner_pts, fill=BANNER_FADED)

    # ── 7. CLASSROOM DOORS (in right wall between lockers) ───────────────────
    door_positions = [0.22, 0.40]
    for dp in door_positions:
        door_pts = get_wall_band("right", dp, dp + 0.10, 0.28, 0.68)
        draw.polygon(door_pts, fill=DOOR_COLOR)
        # Door shadow edge
        shadow_pts = get_wall_band("right", dp + 0.08, dp + 0.10, 0.28, 0.68)
        draw.polygon(shadow_pts, fill=DOOR_SHADOW)
        # Door window (small rectangle in upper part)
        win_pts = get_wall_band("right", dp + 0.02, dp + 0.07, 0.50, 0.62)
        draw.polygon(win_pts, fill=DOOR_GLASS)

    # ── 8. FAR WALL (T-intersection) ─────────────────────────────────────────
    far_wall_pts = [
        (VP_CX - FAR_W // 2 - 8, FAR_H_CEIL),
        (VP_CX + FAR_W // 2 + 8, FAR_H_CEIL),
        FL_FAR_R,
        FL_FAR_L,
    ]
    draw.polygon(far_wall_pts, fill=FAR_WALL)

    # Windows at far end — daylight source
    n_far_wins = 3
    win_strip_y0 = FAR_H_CEIL + 10
    win_strip_y1 = FAR_H_FLOOR - 18
    win_h = win_strip_y1 - win_strip_y0
    for wi in range(n_far_wins):
        t_l = (wi + 0.1) / n_far_wins
        t_r = (wi + 0.9) / n_far_wins
        wx0 = int(lerp(FL_FAR_L[0], FL_FAR_R[0], t_l))
        wx1 = int(lerp(FL_FAR_L[0], FL_FAR_R[0], t_r))
        wy0 = win_strip_y0 + 5
        wy1 = win_strip_y0 + int(win_h * 0.72)
        draw_rect(draw, wx0, wy0, wx1, wy1, WIN_DAYLIGHT)
        # Window frame cross
        draw.line([(wx0, (wy0 + wy1) // 2), (wx1, (wy0 + wy1) // 2)],
                  fill=FAR_WALL, width=2)
        draw.line([((wx0 + wx1) // 2, wy0), ((wx0 + wx1) // 2, wy1)],
                  fill=FAR_WALL, width=2)

    # School seal on far wall center (circle with marlin)
    seal_cx = VP_CX
    seal_cy = FAR_H_CEIL + int(win_h * 0.50)
    seal_r  = max(12, FAR_W // 6)
    draw.ellipse([seal_cx - seal_r, seal_cy - seal_r,
                  seal_cx + seal_r, seal_cy + seal_r],
                 fill=SCHOOL_SEAL_BG, outline=SCHOOL_SEAL_RING, width=2)
    # Inner circle
    draw.ellipse([seal_cx - seal_r + 4, seal_cy - seal_r + 4,
                  seal_cx + seal_r - 4, seal_cy + seal_r - 4],
                 outline=SCHOOL_SEAL_RING, width=1)

    # ── 9. TROPHY CASE (left wall near far end) ───────────────────────────────
    tc_pts = get_wall_band("left", 0.55, 0.70, 0.18, 0.68)
    if len(tc_pts) == 4:
        draw.polygon(tc_pts, fill=TROPHY_FRAME)
        inner_pts = get_wall_band("left", 0.56, 0.69, 0.20, 0.66)
        draw.polygon(inner_pts, fill=TROPHY_GLASS)
        # Simple trophy shapes inside
        trophy_y_mid = (tc_pts[0][1] + tc_pts[2][1]) // 2
        for ti in range(3):
            t_ti = (ti + 0.3) / 3
            tx = int(lerp(tc_pts[0][0], tc_pts[1][0], t_ti))
            draw.polygon([
                (tx, trophy_y_mid - 8),
                (tx - 5, trophy_y_mid + 5),
                (tx + 5, trophy_y_mid + 5),
            ], fill=TROPHY_GOLD)

    # ── 10. WARM WINDOW LIGHT SHAFT (from left-wall high window) ──────────────
    # Shaft comes from upper-left, falls diagonally across floor and lockers
    # Represents a high window above the lockers
    shaft_near_x = int(W * 0.12)
    shaft_pts_floor = [
        (0, int(H * 0.55)),
        (shaft_near_x, int(H * 0.42)),
        (shaft_near_x + 140, H),
        (0, H),
    ]
    shaft_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sld = ImageDraw.Draw(shaft_layer)
    sld.polygon(shaft_pts_floor, fill=SUNLIGHT_SHAFT + (42,))
    img.alpha_composite(shaft_layer)
    draw = ImageDraw.Draw(img)

    # Warm light on locker faces in shaft zone
    lit_locker_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lld = ImageDraw.Draw(lit_locker_overlay)
    lld.polygon([
        (0, int(H * 0.42)),
        (shaft_near_x + 50, int(H * 0.42)),
        (shaft_near_x + 50, H),
        (0, H),
    ], fill=SUNLIGHT_SHAFT + (22,))
    img.alpha_composite(lit_locker_overlay)
    draw = ImageDraw.Draw(img)

    # Daylight warm glow from far end windows pulling toward VP
    far_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fg_draw = ImageDraw.Draw(far_glow)
    # Gradient glow emanating from far end
    for ri in range(25):
        t = ri / 25
        rx = int(FAR_W // 2 * (1 + t * 3.5))
        ry = int((FAR_H_FLOOR - FAR_H_CEIL) // 2 * (1 + t * 2.5))
        a = int(35 * (1 - t))
        fg_draw.ellipse([VP_CX - rx, VP_CY - ry, VP_CX + rx, VP_CY + ry],
                        fill=WIN_GLOW + (a,))
    img.alpha_composite(far_glow)
    draw = ImageDraw.Draw(img)

    # ── 11. ATMOSPHERIC DEPTH (slight cool haze in far hallway) ───────────────
    # Interior atmospheric perspective: far end gets a very faint cool overlay
    haze_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    haze_d = ImageDraw.Draw(haze_layer)
    # Subtle cool fog that increases toward VP
    for ri in range(20):
        t = ri / 20
        rx = int(FAR_W // 2 * (1 + (1 - t) * 4))
        ry = int((FAR_H_FLOOR - FAR_H_CEIL) // 2 * (1 + (1 - t) * 2))
        a = int(18 * t)
        haze_d.ellipse([VP_CX - rx, VP_CY - ry, VP_CX + rx, VP_CY + ry],
                       fill=(180, 190, 200) + (a,))
    img.alpha_composite(haze_layer)
    draw = ImageDraw.Draw(img)

    # ── 12. OUTLINE / LINE WORK ───────────────────────────────────────────────
    # Floor-wall seams
    draw.line([FL_NEAR_L, FL_FAR_L], fill=LINE_DARK, width=2)
    draw.line([FL_NEAR_R, FL_FAR_R], fill=LINE_DARK, width=2)
    # Ceiling-wall seam
    draw.line([CEIL_NEAR_L, CEIL_FAR_L], fill=LINE_DARK, width=1)
    draw.line([CEIL_NEAR_R, CEIL_FAR_R], fill=LINE_DARK, width=1)
    # Far wall outline
    draw.line([FL_FAR_L, (FL_FAR_L[0], FAR_H_CEIL)], fill=LINE_DARK, width=1)
    draw.line([FL_FAR_R, (FL_FAR_R[0], FAR_H_CEIL)], fill=LINE_DARK, width=1)
    draw.line([(FL_FAR_L[0], FAR_H_CEIL), (FL_FAR_R[0], FAR_H_CEIL)],
              fill=LINE_DARK, width=1)

    # ── OUTPUT ────────────────────────────────────────────────────────────────
    out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_school_hallway_v001.png"
    img.convert("RGB").save(out_path)
    print(f"Saved: {out_path}")
    return out_path


if __name__ == "__main__":
    draw_school_hallway()
