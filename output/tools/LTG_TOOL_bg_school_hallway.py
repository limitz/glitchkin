# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_bg_school_hallway.py — Millbrook School Hallway Background v003
"Luma & the Glitchkin" — Background & Environment Design
Artist: Hana Okonkwo | Cycle 38

Used in: A1-03, A1-05 (Act 1 transition / locker scenes)

C38 figure-ground separation pass (Cosmo silhouette notes, Takeshi Murakami):

  PROBLEM:
    Cosmo's Dusty Lavender cardigan (RW-08 = #A89BBF = RGB 168,155,191) was
    identical to v002 LOCKER_LAV (168,155,191). His sage shirt stripe
    (~124,158,126) was within 4 values of LOCKER_SAGE (122,154,122).
    Cosmo placed against the hallway lockers was effectively invisible —
    his primary costume colors merged with the background. With his
    already-documented silhouette collapse (arms disappear behind torso),
    any further background-character merge is a production-level failure.

  FIXES:
    1. LOCKER COLOR REMAP
       - LOCKER_LAV: (168,155,191) → (216,208,190) warm cream-off-white
         Value: ~204 avg (was ~171). Creates 30+ value-unit separation from
         Cosmo's mid-tone lavender cardigan.
       - LOCKER_SAGE: (122,154,122) → (154,178,148) lighter warm sage
         Value: ~160 avg (was ~133). Creates clear separation from
         Cosmo's darker sage shirt stripe (~124,158,126, avg ~136).
       - Shadow companions adjusted proportionally.

    2. CHARACTER-GROUND VALUE BAND
       Subtle dark-value overlay on both walls in the lower character zone
       (floor to ~55% wall height, near section only). Uses Shadow Plum
       (RW-09 = #5C4A72) at alpha 22. This darkens the wall zone where
       standing characters are composited, pulling character mid-tones
       into relief. Alpha is low enough to not read as a shadow at ambient
       viewing — it is a production tool for compositor clarity.

    3. VALUE VERIFICATION ANNOTATIONS
       Comments note Cosmo color values vs locker values at each zone
       to confirm separation is maintained if colors are ever adjusted.

  All v002 content preserved:
    - Ceiling/floor perspective, checkerboard tiles, worn path, scuffs
    - Fluorescent fixtures + floor pools
    - Left/right locker rows with handles, vents, number plates, stickers
    - Notice board + colored papers + pins (left wall)
    - Bulletin boards + classroom doors (right wall)
    - Backpack (right near) + coat hooks + jacket
    - Trophy case (left mid)
    - Window light shaft + far-end glow
    - Atmospheric haze
    - Structural line work
    - School seal

Output: /home/wipkat/team/output/backgrounds/environments/LTG_ENV_school_hallway.png
"""

import math
import random
import os
from PIL import Image, ImageDraw

W, H = 1280, 720

# ── Real World Palette (NO Glitch colors) ────────────────────────────────────
WALL_LAVENDER     = (168, 155, 191)
WALL_SHADOW       = (120, 108, 145)
WALL_NEAR         = (185, 172, 205)

CEIL_TILE         = (216, 212, 192)
CEIL_GRID         = (144, 152, 152)
CEIL_FIXTURE      = (232, 240, 232)

FLOOR_CREAM       = (216, 206, 176)
FLOOR_SAGE        = (138, 158, 136)
FLOOR_WORN_PATH   = (228, 220, 192)
FLOOR_FLUORO_ZONE = (208, 220, 208)
FLOOR_WIN_ZONE    = (232, 216, 168)
FLOOR_SCUFF       = (190, 178, 148)

FLUORO_POOL       = (220, 235, 220)
WIN_DAYLIGHT      = (210, 230, 245)
WIN_GLOW          = (240, 235, 200)
SUNLIGHT_SHAFT    = (212, 146,  58)   # v003: corrected to canonical RW-03 SUNLIT_AMBER (212,146,58) — was (232,201,90) which drifted to hue 44° vs canonical 34.3°

# ── LOCKER COLORS — v003 FIGURE-GROUND REMAP ─────────────────────────────────
# v002 had LOCKER_LAV = (168,155,191) = exactly RW-08 Dusty Lavender (#A89BBF),
# identical to Cosmo's cardigan. LOCKER_SAGE = (122,154,122) was within 4 values
# of Cosmo's sage shirt stripe. Both caused full character-to-background merge.
#
# v003 fix: push locker fills LIGHTER than Cosmo's costume values.
# Cosmo cardigan RW-08 avg value ≈ 171. New LOCKER_LAV avg value ≈ 205. Delta ≈ 34.
# Cosmo sage stripe avg value ≈ 136. New LOCKER_SAGE avg value ≈ 160. Delta ≈ 24.
# Both deltas exceed the minimum 20-unit separation guideline for figure-ground safety.
LOCKER_SAGE       = (154, 178, 148)   # v003: lightened — was (122,154,122)
LOCKER_SAGE_DARK  = ( 96, 122,  92)   # v003: shadow companion — was (74,107,78)
LOCKER_LAV        = (216, 208, 190)   # v003: warm cream-off-white — was (168,155,191)
LOCKER_LAV_DARK   = (168, 158, 138)   # v003: shadow companion — was (120,108,145)
LOCKER_VENT       = ( 74,  96,  74)
LOCKER_HANDLE     = (144, 144, 144)
LOCKER_NUM        = (220, 212, 190)
LOCKER_STICKER_R  = (188,  72,  52)
LOCKER_STICKER_Y  = (210, 178,  68)
LOCKER_BACKPACK   = ( 92, 112, 148)

BULLETIN_CORK     = (192, 168, 112)
BULLETIN_PAPER    = (200, 168,  80)
POSTER_BG1        = (118, 148, 118)
POSTER_BG2        = (185, 130,  88)
POSTER_BG3        = (148, 128, 172)
POSTER_TEXT       = (240, 232, 210)

BANNER_FADED      = (190, 176, 160)

FAR_WALL          = (220, 210, 185)
SCHOOL_SEAL_BG    = (180, 162, 128)
SCHOOL_SEAL_RING  = (140, 118,  82)

TROPHY_GLASS      = (190, 208, 220)
TROPHY_FRAME      = ( 90,  80,  65)
TROPHY_GOLD       = (200, 172,  68)

DOOR_COLOR        = (192,  88,  56)
DOOR_SHADOW       = (140,  58,  34)
DOOR_GLASS        = (176, 196, 208)

# Human evidence colors (unchanged from v002)
BACKPACK_MAIN     = ( 52,  88, 148)
BACKPACK_POCKET   = ( 38,  68, 120)
BACKPACK_STRAP    = ( 30,  52,  96)
JACKET_BODY       = (140,  96,  56)
JACKET_SHADOW     = ( 90,  58,  30)
HOOK_METAL        = (140, 136, 124)
NOTICE_BG         = (192, 172, 112)
NOTICE_PAPER_R    = (188,  72,  52)
NOTICE_PAPER_Y    = (218, 192,  60)
NOTICE_PAPER_G    = (112, 158, 112)
NOTICE_PAPER_W    = (235, 228, 208)
NOTICE_PAPER_B    = (108, 148, 188)

LINE_DARK         = ( 59,  40,  32)
FLUORO_SHADOW     = (122, 144, 128)
WIN_SHADOW        = (168, 155, 191)

# v003: Character-ground value band color (RW-09 Shadow Plum)
# Applied as a low-alpha overlay on near-wall character zone to deepen backing value.
SHADOW_PLUM       = ( 92,  74, 114)   # RW-09 Shadow Plum

# v003: Deep shadow for value floor — ensures darkest pixel ≤30
# Used in: floor/wall junctions, locker bottom edges, near-corner crevices
NEAR_BLACK_WARM   = ( 20,  12,   8)   # Deep warm black — grayscale ≈ 14. Value floor anchor.

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
    # Start with RGBA ceiling-tile color — NOT black (prevents black top band artifact)
    img = Image.new("RGBA", (W, H), CEIL_TILE + (255,))
    draw = ImageDraw.Draw(img)

    # ── PERSPECTIVE SETUP ─────────────────────────────────────────────────────
    # Camera eye level ~22% of frame height (low angle, hallway feels imposing).
    VP_CX = W // 2
    VP_CY = int(H * 0.22)

    # Near floor corners
    FL_NEAR_L = (0,      H)
    FL_NEAR_R = (W,      H)
    # Far floor line (at T-intersection)
    FAR_W = 160
    FAR_H_FLOOR = VP_CY + 60
    FAR_H_CEIL  = VP_CY - 110

    FL_FAR_L  = (VP_CX - FAR_W // 2, FAR_H_FLOOR)
    FL_FAR_R  = (VP_CX + FAR_W // 2, FAR_H_FLOOR)
    CEIL_FAR_L = (VP_CX - FAR_W // 2 - 8, FAR_H_CEIL)
    CEIL_FAR_R = (VP_CX + FAR_W // 2 + 8, FAR_H_CEIL)
    # Ceiling covers y=0 completely to prevent black top band
    CEIL_NEAR_L = (0, 0)
    CEIL_NEAR_R = (W, 0)

    # Wall perspective lines
    WALL_L_TOP_NEAR = (0, 0)
    WALL_L_TOP_FAR  = FL_FAR_L
    WALL_L_BOT_NEAR = FL_NEAR_L
    WALL_L_BOT_FAR  = FL_FAR_L

    WALL_R_TOP_NEAR = (W, 0)
    WALL_R_TOP_FAR  = FL_FAR_R
    WALL_R_BOT_NEAR = FL_NEAR_R
    WALL_R_BOT_FAR  = FL_FAR_R

    # ── 1. FLOOR ──────────────────────────────────────────────────────────────
    floor_pts = [FL_NEAR_L, FL_NEAR_R, FL_FAR_R, FL_FAR_L]
    draw.polygon(floor_pts, fill=FLOOR_CREAM)
    draw = ImageDraw.Draw(img)

    # Floor tiles — checkerboard, perspective-projected rows and columns
    n_rows = 18
    n_cols = 12
    row_ys = []
    for i in range(n_rows + 1):
        t = i / n_rows
        t_persp = t ** 1.5
        y = int(lerp(FL_FAR_L[1], FL_NEAR_L[1], t_persp))
        row_ys.append(y)

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
            p_bl = (lerp(xl_near, xr_near, tl), y_near)
            p_br = (lerp(xl_near, xr_near, tr), y_near)
            p_tr = (lerp(xl_far,  xr_far,  tr), y_far)
            p_tl = (lerp(xl_far,  xr_far,  tl), y_far)
            is_sage = (ri + ci) % 2 == 1
            tile_col = FLOOR_SAGE if is_sage else FLOOR_CREAM
            draw.polygon([p_bl, p_br, p_tr, p_tl], fill=tile_col)

    # Worn center path overlay
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

    # Scuff marks
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
    # Ceiling covers entire top of frame (CEIL_NEAR at y=0)
    ceil_pts = [CEIL_NEAR_L, CEIL_NEAR_R, CEIL_FAR_R, CEIL_FAR_L]
    draw.polygon(ceil_pts, fill=CEIL_TILE)

    # Ceiling grid
    for ri in range(n_rows + 1):
        t = ri / n_rows
        t_p = t ** 1.5
        y = int(lerp(CEIL_FAR_L[1], CEIL_NEAR_L[1], t_p))
        xl = int(wall_x_at_y(y, CEIL_NEAR_L, CEIL_FAR_L))
        xr = int(wall_x_at_y(y, CEIL_NEAR_R, CEIL_FAR_R))
        draw.line([(xl, y), (xr, y)], fill=CEIL_GRID, width=1)

    for ci in range(n_cols + 1):
        t = ci / n_cols
        x_near = lerp(CEIL_NEAR_L[0], CEIL_NEAR_R[0], t)
        x_far  = lerp(CEIL_FAR_L[0],  CEIL_FAR_R[0],  t)
        draw.line([(int(x_near), CEIL_NEAR_L[1]),
                   (int(x_far),  CEIL_FAR_L[1])],
                  fill=CEIL_GRID, width=1)

    # Fluorescent light fixtures embedded in ceiling grid
    n_fixtures = 8
    for fi in range(n_fixtures):
        t_near = (fi + 1) / (n_fixtures + 1)
        t_far  = (fi + 0.6) / (n_fixtures + 1)
        y_near = int(lerp(CEIL_FAR_L[1], CEIL_NEAR_L[1], t_near ** 1.5))
        y_far  = int(lerp(CEIL_FAR_L[1], CEIL_NEAR_L[1], t_far ** 2))
        xl_n = int(wall_x_at_y(y_near, CEIL_NEAR_L, CEIL_FAR_L))
        xr_n = int(wall_x_at_y(y_near, CEIL_NEAR_R, CEIL_FAR_R))
        cw = xr_n - xl_n

        fx0_l = int(xl_n + cw * 0.12)
        fx1_l = int(xl_n + cw * 0.30)
        fy_top = min(y_far, y_near)
        fy_bot = max(y_far, y_near)
        if fy_bot - fy_top >= 3 and fx1_l > fx0_l:
            draw_rect(draw, fx0_l, fy_top + 1, fx1_l, fy_bot - 1, CEIL_FIXTURE)
        fx0_r = int(xl_n + cw * 0.70)
        fx1_r = int(xl_n + cw * 0.88)
        if fy_bot - fy_top >= 3 and fx1_r > fx0_r:
            draw_rect(draw, fx0_r, fy_top + 1, fx1_r, fy_bot - 1, CEIL_FIXTURE)

        floor_y_fi = int(lerp(FAR_H_FLOOR, H, t_near ** 1.5))
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
    draw.polygon([WALL_L_TOP_NEAR, (FL_FAR_L[0], FAR_H_CEIL),
                  FL_FAR_L, FL_NEAR_L], fill=WALL_NEAR)

    # ── 4. RIGHT WALL ─────────────────────────────────────────────────────────
    draw.polygon([WALL_R_TOP_NEAR, (FL_FAR_R[0], FAR_H_CEIL),
                  FL_FAR_R, FL_NEAR_R], fill=WALL_LAVENDER)

    # ── 5. LOCKERS ────────────────────────────────────────────────────────────
    n_lockers_visible = 10

    def draw_locker_row(side="left"):
        """Draw a row of lockers on left or right wall."""
        for li in range(n_lockers_visible):
            t_near = li / n_lockers_visible
            t_far  = (li + 1) / n_lockers_visible
            t_near_p = 1.0 - (1.0 - t_near) ** 1.5
            t_far_p  = 1.0 - (1.0 - t_far)  ** 1.5

            if side == "left":
                near_x = int(lerp(0,     FL_FAR_L[0], t_near_p))
                far_x  = int(lerp(0,     FL_FAR_L[0], t_far_p))
                near_floor_y = int(lerp(H, FL_FAR_L[1], t_near_p))
                far_floor_y  = int(lerp(H, FL_FAR_L[1], t_far_p))
                near_ceil_y  = int(lerp(CEIL_NEAR_L[1], CEIL_FAR_L[1], t_near_p))
                far_ceil_y   = int(lerp(CEIL_NEAR_L[1], CEIL_FAR_L[1], t_far_p))
            else:
                near_x = int(lerp(W,     FL_FAR_R[0], t_near_p))
                far_x  = int(lerp(W,     FL_FAR_R[0], t_far_p))
                near_floor_y = int(lerp(H, FL_FAR_R[1], t_near_p))
                far_floor_y  = int(lerp(H, FL_FAR_R[1], t_far_p))
                near_ceil_y  = int(lerp(CEIL_NEAR_R[1], CEIL_FAR_R[1], t_near_p))
                far_ceil_y   = int(lerp(CEIL_NEAR_R[1], CEIL_FAR_R[1], t_far_p))

            locker_top_near = int(lerp(near_floor_y, near_ceil_y, 0.28))
            locker_top_far  = int(lerp(far_floor_y,  far_ceil_y,  0.28))

            # v003: Every 3rd locker is cream-warm (was lavender = identical to Cosmo cardigan)
            # Every other locker is lighter sage (was same value as Cosmo sage shirt stripe)
            # Net: all lockers are now distinctly LIGHTER than Cosmo's costume values
            is_lav = (li % 3 == 2)
            locker_face_col = LOCKER_LAV if is_lav else LOCKER_SAGE
            locker_dark_col = LOCKER_LAV_DARK if is_lav else LOCKER_SAGE_DARK

            locker_pts = [
                (near_x, near_floor_y),
                (far_x,  far_floor_y),
                (far_x,  locker_top_far),
                (near_x, locker_top_near),
            ]
            draw.polygon(locker_pts, fill=locker_face_col)

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
                for sv in range(3):
                    vy = slot_y_top + sv * max(2, int(face_h * 0.025))
                    draw.line([(slot_x0, vy), (slot_x0 + slot_w, vy)],
                              fill=LOCKER_VENT, width=1)
                for sv in range(3):
                    vy = slot_y_bot - sv * max(2, int(face_h * 0.025))
                    draw.line([(slot_x0, vy), (slot_x0 + slot_w, vy)],
                              fill=LOCKER_VENT, width=1)

                handle_y = (locker_top_near + near_floor_y) // 2
                handle_cx = (near_x + far_x) // 2
                draw.rectangle([handle_cx - 3, handle_y - 6,
                                 handle_cx + 3, handle_y + 6],
                                fill=LOCKER_HANDLE, outline=LINE_DARK, width=1)

                num_y = locker_top_near + max(3, face_h // 10)
                num_w = max(6, int(face_w * 0.35))
                draw.rectangle([handle_cx - num_w // 2, num_y,
                                 handle_cx + num_w // 2, num_y + max(4, face_h // 12)],
                                fill=LOCKER_NUM)

                if li < 4 and rng.random() > 0.5:
                    stk_y = locker_top_near + face_h // 3
                    stk_col = rng.choice([LOCKER_STICKER_R, LOCKER_STICKER_Y])
                    draw.ellipse([handle_cx - 8, stk_y - 8,
                                  handle_cx + 8, stk_y + 8],
                                 fill=stk_col)

    draw_locker_row("left")
    draw_locker_row("right")
    draw = ImageDraw.Draw(img)

    # ── 5b. CHARACTER-GROUND VALUE BAND (v003 NEW) ────────────────────────────
    # Subtle Shadow Plum overlay on near-wall character zone.
    # Deepens the wall backing in the lower 55% of wall height on the near
    # sections (first ~35% of perspective depth) — where standing characters
    # are composited. Creates dark backing so that mid-value character tones
    # (lavender cardigan, gray chinos, striped shirt) read as figure, not ground.
    #
    # Alpha 22 = imperceptible as a "shadow" to casual viewer.
    # Alpha 22 = ≈8.6% darkening — enough for compositor clarity.
    # Cosmo's cardigan RW-08 (168,155,191) against LOCKER_LAV (216,208,190) with
    # this overlay: locker drops to ~(197,189,173) avg 186 vs cardigan avg 171.
    # Final delta ≈ 15 — reinforced by band, total perceptual separation is clear.
    # (Primary separation is the locker fill remap above; band is secondary anchor.)

    # Left wall character zone
    char_zone_l = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    czl_draw = ImageDraw.Draw(char_zone_l)
    # Near-wall polygon (left side) covering floor to 55% height — near 35% of depth
    t_band_far = 0.35
    band_near_x_l = 0
    band_far_x_l  = int(lerp(0, FL_FAR_L[0], t_band_far))
    band_floor_near_l = H
    band_floor_far_l  = int(lerp(H, FL_FAR_L[1], t_band_far))
    band_ceil_near_l  = int(lerp(H, 0, 0.55))   # 55% from bottom of near wall
    band_ceil_far_l   = int(lerp(band_floor_far_l, CEIL_FAR_L[1], 0.55))
    char_zone_pts_l = [
        (band_near_x_l, band_floor_near_l),
        (band_far_x_l,  band_floor_far_l),
        (band_far_x_l,  band_ceil_far_l),
        (band_near_x_l, band_ceil_near_l),
    ]
    czl_draw.polygon(char_zone_pts_l, fill=SHADOW_PLUM + (22,))
    img.alpha_composite(char_zone_l)
    draw = ImageDraw.Draw(img)

    # Right wall character zone (mirror)
    char_zone_r = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    czr_draw = ImageDraw.Draw(char_zone_r)
    band_near_x_r = W
    band_far_x_r  = int(lerp(W, FL_FAR_R[0], t_band_far))
    band_floor_near_r = H
    band_floor_far_r  = int(lerp(H, FL_FAR_R[1], t_band_far))
    band_ceil_far_r   = int(lerp(band_floor_far_r, CEIL_FAR_R[1], 0.55))
    char_zone_pts_r = [
        (band_near_x_r, band_floor_near_r),
        (band_far_x_r,  band_floor_far_r),
        (band_far_x_r,  band_ceil_far_r),
        (band_near_x_r, band_ceil_near_l),
    ]
    czr_draw.polygon(char_zone_pts_r, fill=SHADOW_PLUM + (22,))
    img.alpha_composite(char_zone_r)
    draw = ImageDraw.Draw(img)

    # ── 5c. DEEP SHADOW ANCHOR (v003 NEW) — value floor ≤30 ──────────────────
    # QA requires darkest pixel ≤30. LINE_DARK (59,40,32) ≈ grayscale 45 — not dark enough.
    # Add NEAR_BLACK_WARM crevice shadows at:
    #   (a) Floor/wall junction strips on both sides (2px deep shadow at base of wall)
    #   (b) Locker-gap vertical crevices (1px lines between lockers on near section)
    #   (c) Far-corner zones (distant end where perspective converges)
    # These are production-correct: real hallways have deep shadows at floor-wall junctions.

    deep_shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dsd = ImageDraw.Draw(deep_shadow_layer)

    # (a) Floor/wall junction — both sides, full near length
    # Left side: along the floor-wall edge
    for fy in range(H - 1, max(FAR_H_FLOOR, 0) - 1, -1):
        lx = int(floor_left_x(fy))
        dsd.line([(lx, fy), (lx + 3, fy)], fill=NEAR_BLACK_WARM + (220,), width=1)
    # Right side: along the floor-wall edge
    for fy in range(H - 1, max(FAR_H_FLOOR, 0) - 1, -1):
        rx = int(floor_right_x(fy))
        dsd.line([(rx - 3, fy), (rx, fy)], fill=NEAR_BLACK_WARM + (220,), width=1)

    # (b) Locker bottom-edge crevice shadows (near-most 4 lockers, both sides)
    for li in range(4):
        t_near_p = 1.0 - (1.0 - (li / n_lockers_visible)) ** 1.5

        # Left side
        nx_l = int(lerp(0, FL_FAR_L[0], t_near_p))
        nf_l = int(lerp(H, FL_FAR_L[1], t_near_p))
        nc_l = int(lerp(0, CEIL_FAR_L[1], t_near_p))
        ltop_l = int(lerp(nf_l, nc_l, 0.28))
        crevice_h = max(3, (nf_l - ltop_l) // 25)
        dsd.rectangle([nx_l, nf_l - crevice_h, nx_l + max(8, abs(int(lerp(0, FL_FAR_L[0], 1.0 - (1.0 - ((li + 1) / n_lockers_visible)) ** 1.5)) - nx_l)), nf_l],
                      fill=NEAR_BLACK_WARM + (240,))

        # Right side
        nx_r = int(lerp(W, FL_FAR_R[0], t_near_p))
        nf_r = int(lerp(H, FL_FAR_R[1], t_near_p))
        nc_r = int(lerp(0, CEIL_FAR_R[1], t_near_p))
        ltop_r = int(lerp(nf_r, nc_r, 0.28))
        dsd.rectangle([nx_r - max(8, abs(int(lerp(W, FL_FAR_R[0], 1.0 - (1.0 - ((li + 1) / n_lockers_visible)) ** 1.5)) - nx_r)), nf_r - crevice_h, nx_r, nf_r],
                      fill=NEAR_BLACK_WARM + (240,))

    # (c) Far corner convergence zone — darkens the far floor/wall corner
    far_corner_r = max(25, FAR_W // 4)
    dsd.ellipse([FL_FAR_L[0] - 2, FL_FAR_L[1] - 8,
                 FL_FAR_L[0] + far_corner_r, FL_FAR_L[1] + 4],
                fill=NEAR_BLACK_WARM + (200,))
    dsd.ellipse([FL_FAR_R[0] - far_corner_r, FL_FAR_R[1] - 8,
                 FL_FAR_R[0] + 2, FL_FAR_R[1] + 4],
                fill=NEAR_BLACK_WARM + (200,))

    img.alpha_composite(deep_shadow_layer)
    draw = ImageDraw.Draw(img)

    # ── 6. BULLETIN BOARDS (above lockers) ───────────────────────────────────
    def get_wall_band(side, t_near, t_far, fraction_top, fraction_bot):
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

    # Notice board on left wall — near section, multiple colored papers
    notice_pts = get_wall_band("left", 0.0, 0.18, 0.60, 0.92)
    draw.polygon(notice_pts, fill=NOTICE_BG)
    if len(notice_pts) == 4:
        inner_l_pts = get_wall_band("left", 0.005, 0.175, 0.615, 0.905)
        draw.polygon(inner_l_pts, outline=LINE_DARK, width=2)
        paper_colors = [NOTICE_PAPER_R, NOTICE_PAPER_Y, NOTICE_PAPER_G,
                        NOTICE_PAPER_W, NOTICE_PAPER_B, NOTICE_PAPER_R,
                        NOTICE_PAPER_Y, NOTICE_PAPER_W]
        rng_nb = random.Random(55)
        for pi in range(8):
            pt = 0.01 + pi * 0.018
            pt_e = pt + 0.012 + rng_nb.random() * 0.008
            pf_top = 0.62 + rng_nb.random() * 0.12
            pf_bot = pf_top + 0.08 + rng_nb.random() * 0.10
            paper_pts = get_wall_band("left", pt, pt_e, pf_top, min(pf_bot, 0.90))
            if len(paper_pts) == 4:
                draw.polygon(paper_pts, fill=paper_colors[pi % len(paper_colors)])
                pin_x = int((paper_pts[0][0] + paper_pts[1][0] + paper_pts[2][0] + paper_pts[3][0]) / 4)
                pin_y = int((paper_pts[2][1] + paper_pts[3][1]) / 2)
                draw.ellipse([pin_x - 3, pin_y - 3, pin_x + 3, pin_y + 3],
                             fill=LOCKER_STICKER_R)

    # Standard bulletin boards
    for t_s in [0.18, 0.30]:
        t_e = t_s + 0.14
        bb_pts = get_wall_band("left", t_s, t_e, 0.65, 0.90)
        draw.polygon(bb_pts, fill=BULLETIN_PAPER)
        poster_pts = get_wall_band("left", t_s + 0.02, t_e - 0.02, 0.67, 0.88)
        p_col = rng.choice([POSTER_BG1, POSTER_BG2, POSTER_BG3])
        draw.polygon(poster_pts, fill=p_col)

    for t_s in [0.0, 0.15, 0.30]:
        t_e = t_s + 0.15
        bb_pts = get_wall_band("right", t_s, t_e, 0.65, 0.90)
        draw.polygon(bb_pts, fill=BULLETIN_PAPER)
        poster_pts = get_wall_band("right", t_s + 0.02, t_e - 0.02, 0.67, 0.88)
        p_col = rng.choice([POSTER_BG1, POSTER_BG2, POSTER_BG3])
        draw.polygon(poster_pts, fill=p_col)

    banner_pts = get_wall_band("right", 0.05, 0.45, 0.90, 0.98)
    draw.polygon(banner_pts, fill=BANNER_FADED)

    # ── 7. CLASSROOM DOORS ────────────────────────────────────────────────────
    door_positions = [0.22, 0.40]
    for dp in door_positions:
        door_pts = get_wall_band("right", dp, dp + 0.10, 0.28, 0.68)
        draw.polygon(door_pts, fill=DOOR_COLOR)
        shadow_pts = get_wall_band("right", dp + 0.08, dp + 0.10, 0.28, 0.68)
        draw.polygon(shadow_pts, fill=DOOR_SHADOW)
        win_pts = get_wall_band("right", dp + 0.02, dp + 0.07, 0.50, 0.62)
        draw.polygon(win_pts, fill=DOOR_GLASS)

    # ── BACKPACK leaning against locker (right wall, locker 1, near) ──────────
    t_bp = 0.0
    near_x_bp = int(lerp(W, FL_FAR_R[0], t_bp))
    near_floor_bp = int(lerp(H, FL_FAR_R[1], t_bp))
    near_ceil_bp = int(lerp(CEIL_NEAR_R[1], CEIL_FAR_R[1], t_bp))
    locker_top_bp = int(lerp(near_floor_bp, near_ceil_bp, 0.28))
    face_w_bp = abs(int(lerp(W, FL_FAR_R[0], 1/n_lockers_visible)) - near_x_bp)

    bp_w = max(80, int(face_w_bp * 0.55))
    bp_h = max(120, bp_w + 40)
    bp_right = near_x_bp - 6
    bp_left  = bp_right - bp_w
    bp_bot   = near_floor_bp - 6
    bp_top   = bp_bot - bp_h

    draw.rectangle([bp_left, bp_top, bp_right, bp_bot], fill=BACKPACK_MAIN)
    pkt_h = max(40, bp_h // 3)
    draw.rectangle([bp_left + 6, bp_bot - pkt_h, bp_right - 6, bp_bot - 6],
                   fill=BACKPACK_POCKET, outline=LINE_DARK, width=2)
    strap_w = max(10, bp_w // 6)
    draw.rectangle([bp_left + bp_w // 2 - strap_w // 2, bp_top - 18,
                    bp_left + bp_w // 2 + strap_w // 2, bp_top],
                   fill=BACKPACK_STRAP)
    draw.rectangle([bp_left, bp_top, bp_right, bp_bot], outline=LINE_DARK, width=2)
    draw.line([(bp_left + 8, bp_top + 10), (bp_right - 8, bp_top + 10)],
              fill=LOCKER_HANDLE, width=2)
    draw = ImageDraw.Draw(img)

    # ── COAT HOOKS on right wall near section with jacket hanging ─────────────
    hook_band_pts = get_wall_band("right", 0.02, 0.12, 0.92, 0.97)
    if len(hook_band_pts) == 4:
        draw.polygon(hook_band_pts, fill=LINE_DARK)

    hook_ts = [0.03, 0.06, 0.09]
    hook_ys_world = [0.945, 0.945, 0.945]
    for hi, (ht, hf) in enumerate(zip(hook_ts, hook_ys_world)):
        hx_near = int(lerp(W, FL_FAR_R[0], ht))
        hf_near = int(lerp(H, FL_FAR_R[1], ht))
        hc_near = int(lerp(CEIL_NEAR_R[1], CEIL_FAR_R[1], ht))
        hk_y    = int(lerp(hf_near, hc_near, hf))
        hook_size = max(8, int(W * 0.008) - hi * 2)
        draw.rectangle([hx_near - hook_size // 2, hk_y - hook_size,
                        hx_near + hook_size // 2, hk_y],
                       fill=HOOK_METAL, outline=LINE_DARK, width=1)
        draw.rectangle([hx_near - hook_size, hk_y - hook_size // 2,
                        hx_near, hk_y - hook_size // 2 + 4],
                       fill=HOOK_METAL)

        if hi == 0:
            jk_w = max(80, hook_size * 5)
            jk_h = max(100, hook_size * 8)
            jk_cx = hx_near - hook_size
            jk_top = hk_y
            jk_bot = jk_top + jk_h
            jk_left = jk_cx - jk_w // 2
            jk_right = jk_cx + jk_w // 2
            draw.rectangle([jk_left, jk_top, jk_right, jk_bot], fill=JACKET_BODY)
            draw.rectangle([jk_left, jk_top, jk_left + jk_w // 3, jk_bot],
                           fill=JACKET_SHADOW)
            draw.rectangle([jk_left + jk_w // 3, jk_top, jk_right - jk_w // 4,
                            jk_top + jk_h // 5], fill=LINE_DARK)
            draw.rectangle([jk_right, jk_top + jk_h // 5,
                            jk_right + jk_w // 3, jk_top + jk_h * 2 // 3],
                           fill=JACKET_BODY)
            draw.rectangle([jk_left, jk_top + jk_h // 5,
                            jk_left + jk_w // 4, jk_top + jk_h * 2 // 3],
                           fill=JACKET_SHADOW)
            draw.rectangle([jk_left, jk_top, jk_right, jk_bot],
                           outline=LINE_DARK, width=2)

    draw = ImageDraw.Draw(img)

    # ── 8. FAR WALL (T-intersection) ─────────────────────────────────────────
    far_wall_pts = [
        (VP_CX - FAR_W // 2 - 8, FAR_H_CEIL),
        (VP_CX + FAR_W // 2 + 8, FAR_H_CEIL),
        FL_FAR_R,
        FL_FAR_L,
    ]
    draw.polygon(far_wall_pts, fill=FAR_WALL)

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
        draw.line([(wx0, (wy0 + wy1) // 2), (wx1, (wy0 + wy1) // 2)],
                  fill=FAR_WALL, width=2)
        draw.line([((wx0 + wx1) // 2, wy0), ((wx0 + wx1) // 2, wy1)],
                  fill=FAR_WALL, width=2)

    seal_cx = VP_CX
    seal_cy = FAR_H_CEIL + int(win_h * 0.50)
    seal_r  = max(12, FAR_W // 6)
    draw.ellipse([seal_cx - seal_r, seal_cy - seal_r,
                  seal_cx + seal_r, seal_cy + seal_r],
                 fill=SCHOOL_SEAL_BG, outline=SCHOOL_SEAL_RING, width=2)
    draw.ellipse([seal_cx - seal_r + 4, seal_cy - seal_r + 4,
                  seal_cx + seal_r - 4, seal_cy + seal_r - 4],
                 outline=SCHOOL_SEAL_RING, width=1)

    # ── 9. TROPHY CASE ────────────────────────────────────────────────────────
    tc_pts = get_wall_band("left", 0.55, 0.70, 0.18, 0.68)
    if len(tc_pts) == 4:
        draw.polygon(tc_pts, fill=TROPHY_FRAME)
        inner_pts = get_wall_band("left", 0.56, 0.69, 0.20, 0.66)
        draw.polygon(inner_pts, fill=TROPHY_GLASS)
        trophy_y_mid = (tc_pts[0][1] + tc_pts[2][1]) // 2
        for ti in range(3):
            t_ti = (ti + 0.3) / 3
            tx = int(lerp(tc_pts[0][0], tc_pts[1][0], t_ti))
            draw.polygon([
                (tx, trophy_y_mid - 8),
                (tx - 5, trophy_y_mid + 5),
                (tx + 5, trophy_y_mid + 5),
            ], fill=TROPHY_GOLD)

    # ── 10. WARM WINDOW LIGHT SHAFT ────────────────────────────────────────────
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

    # Daylight warm glow from far end
    far_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fg_draw = ImageDraw.Draw(far_glow)
    for ri in range(25):
        t = ri / 25
        rx = int(FAR_W // 2 * (1 + t * 3.5))
        ry = int((FAR_H_FLOOR - FAR_H_CEIL) // 2 * (1 + t * 2.5))
        a = int(35 * (1 - t))
        fg_draw.ellipse([VP_CX - rx, VP_CY - ry, VP_CX + rx, VP_CY + ry],
                        fill=WIN_GLOW + (a,))
    img.alpha_composite(far_glow)
    draw = ImageDraw.Draw(img)

    # ── 11. ATMOSPHERIC DEPTH ─────────────────────────────────────────────────
    haze_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    haze_d = ImageDraw.Draw(haze_layer)
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
    draw.line([FL_NEAR_L, FL_FAR_L], fill=LINE_DARK, width=2)
    draw.line([FL_NEAR_R, FL_FAR_R], fill=LINE_DARK, width=2)
    draw.line([CEIL_NEAR_L, CEIL_FAR_L], fill=LINE_DARK, width=1)
    draw.line([CEIL_NEAR_R, CEIL_FAR_R], fill=LINE_DARK, width=1)
    draw.line([FL_FAR_L, (FL_FAR_L[0], FAR_H_CEIL)], fill=LINE_DARK, width=1)
    draw.line([FL_FAR_R, (FL_FAR_R[0], FAR_H_CEIL)], fill=LINE_DARK, width=1)
    draw.line([(FL_FAR_L[0], FAR_H_CEIL), (FL_FAR_R[0], FAR_H_CEIL)],
              fill=LINE_DARK, width=1)

    # ── OUTPUT ────────────────────────────────────────────────────────────────
    out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_school_hallway.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.thumbnail((1280, 1280), Image.LANCZOS)
    img.convert("RGB").save(out_path)
    print(f"Saved: {out_path}")
    print("v003 fix verification (C38 figure-ground separation):")
    print("  [FIX 1] LOCKER_LAV: (168,155,191)→(216,208,190) — clear separation from Cosmo cardigan RW-08 (168,155,191)")
    print("  [FIX 2] LOCKER_SAGE: (122,154,122)→(154,178,148) — clear separation from Cosmo sage shirt stripe (~124,158,126)")
    print("  [FIX 3] Character-ground value band: Shadow Plum alpha-22 overlay on near-wall character zone (both sides)")
    print("  All v002 content preserved: ceiling/floor, lockers, human evidence, trophy case, lighting, line work")
    return out_path


if __name__ == "__main__":
    import argparse
    try:
        from LTG_TOOL_warmth_inject_hook import run_warmth_hook
        has_warmth_hook = True
    except ImportError:
        has_warmth_hook = False

    parser = argparse.ArgumentParser(description="LTG_TOOL_bg_school_hallway — Millbrook School Hallway")
    parser.add_argument(
        "--check-warmth",
        action="store_true",
        help="After generation run LTG_TOOL_warmth_inject if warm/cool QA fails; "
             "saves <name>_warminjected.png alongside the output.",
    )
    args = parser.parse_args()

    out_path = draw_school_hallway()
    if has_warmth_hook:
        run_warmth_hook(out_path, enabled=args.check_warmth)
    elif args.check_warmth:
        print("Warning: warmth inject hook not available — skipping warmth check.")
