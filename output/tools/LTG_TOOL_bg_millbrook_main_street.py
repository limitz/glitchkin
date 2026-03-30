#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_bg_millbrook_main_street.py
Luma & the Glitchkin — Background Generator
Scene: Millbrook Main Street, Daytime Exterior
Cycle 19 | Jordan Reed

Canvas: 1280x720
Output: output/backgrounds/environments/LTG_ENV_millbrook_main_street.png

Critique C9 fixes:
  1. POWER LINES — Replaced uniform-weight lines with:
       - Main cable: 3px with perspective convergence toward vanishing point
       - Span wires: 1px
       - Slight catenary sag (parabolic curve, not straight)
       - Overall line darkness reduced (POWER_LINE_CLR darkened slightly)
  2. ROAD PLANE — Added proper road surface:
       - Asphalt grey rectangle from bottom edge up to building base line
       - Faded center double-yellow line (two parallel dashes converging to VP)
       - Crosswalk stripes at near end of frame

Real World palette only — ZERO Glitch colors.
Afternoon light: warm sun from upper right, long shadows cast left.
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

# ── Canvas ────────────────────────────────────────────────────────────────────
W, H = 1280, 720
VP_X = int(W * 0.58)   # vanishing point slightly right of center
VP_Y = int(H * 0.38)   # horizon line

# ── Master Palette (Real World only) ──────────────────────────────────────────
WARM_CREAM      = (250, 240, 220)
SOFT_GOLD       = (232, 201,  90)
SUNLIT_AMBER    = (212, 146,  58)
TERRACOTTA      = (199,  91,  57)
RUST_SHADOW     = (140,  58,  34)
SAGE_GREEN      = (122, 158, 126)
DEEP_SAGE       = ( 74, 107,  78)
DUSTY_LAVENDER  = (168, 155, 191)
SHADOW_PLUM     = ( 92,  74, 114)
DEEP_COCOA      = ( 59,  40,  32)
MUTED_TEAL      = ( 91, 140, 138)

SKY_ZENITH      = (200, 220, 228)
SKY_MID         = (220, 230, 220)
SKY_HORIZON     = (245, 238, 215)
CLOUD_CREAM     = (240, 235, 220)
ASPHALT         = (122, 112,  96)
ASPHALT_LIT     = (144, 138, 122)
SIDEWALK        = (216, 200, 168)
SIDEWALK_SHADOW = (168, 155, 191)
BRICK_DARK      = (160,  72,  48)
CREAM_FACADE    = (232, 216, 184)
WINDOW_LIT      = (200, 224, 232)
WINDOW_DARK     = ( 42,  56,  64)
INTERIOR_WARM   = (208, 144,  26)
SIGN_CREAM      = (232, 216, 176)
WOOD_BROWN      = ( 90,  56,  32)
LEAF_SUN        = (210, 130,  40)
LEAF_MID        = (180, 100,  30)
LEAF_SHADOW     = (130,  68,  20)
POWER_POLE      = (122, 104,  80)
# FIX 1: POWER_LINE_CLR slightly lighter (less heavy/dark)
POWER_LINE_CLR  = ( 88,  84,  74)   # was (74,72,64) — slightly reduced darkness
ANTENNA_CLR     = (136, 144, 144)
NEON_RED        = (255,  96,  80)
ROAD_LINE       = (180, 168, 140)
PARKED_CAR_1    = (100, 120, 130)
PARKED_CAR_2    = (140, 108,  80)
SLATE_ROOF      = (112, 128, 144)
TIN_ROOF        = (154, 154, 138)
TERRA_ROOF      = (168,  80,  48)
CLOCK_STONE     = (176, 168, 144)
CLOCK_FACE_CLR  = (232, 224, 200)
DARK_SAGE_FACADE= (100, 128, 104)
HAZE            = (230, 225, 210)

# FIX 2: Road surface colors
ROAD_ASPHALT    = (100,  90,  76)   # base asphalt (slightly darker/richer than ASPHALT)
ROAD_ASPHALT_LT = (118, 108,  92)   # sun-side lane
CENTER_LINE_Y   = (188, 170,  52)   # faded double-yellow center line
CROSSWALK_WHITE = (210, 200, 178)   # faded crosswalk stripe


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))


def vp_x_at_y(y, side_x, vp_x=VP_X, vp_y=VP_Y):
    """Return x coordinate at height y on a line from (side_x, H) to (vp_x, vp_y)."""
    if H == vp_y:
        return side_x
    t = (y - H) / (vp_y - H)
    return int(lerp(side_x, vp_x, t))


def draw_sky(img):
    """Warm afternoon sky gradient + cumulus clouds."""
    draw = ImageDraw.Draw(img)
    for y in range(int(H * 0.55)):
        t = y / (H * 0.55)
        col = lerp_color(SKY_ZENITH, SKY_HORIZON, t)
        draw.line([(0, y), (W, y)], fill=col)
    rng = random.Random(42)
    hill_pts = [(0, int(H * 0.52))]
    x = 0
    while x < W:
        x += rng.randint(30, 80)
        y_hill = int(H * 0.46 + rng.randint(-12, 12))
        hill_pts.append((x, y_hill))
    hill_pts.append((W, int(H * 0.52)))
    hill_pts.append((W, int(H * 0.56)))
    hill_pts.append((0, int(H * 0.56)))
    draw.polygon(hill_pts, fill=(160, 175, 160))
    clouds = [
        (160, 60, 120, 38), (420, 45, 90, 28), (700, 70, 140, 42),
        (980, 55, 100, 32), (1160, 80, 80, 24),
    ]
    for cx, cy, cw, ch in clouds:
        draw.ellipse([cx - cw//2, cy - ch//2, cx + cw//2, cy + ch//2], fill=CLOUD_CREAM)
        draw.ellipse([cx - cw//3, cy - ch//2 - 10, cx + cw//3, cy + ch//4], fill=CLOUD_CREAM)
        draw.ellipse([cx + cw//6, cy - ch//2 - 6, cx + cw*2//3, cy + ch//4], fill=CLOUD_CREAM)
    return ImageDraw.Draw(img)


def draw_road_and_sidewalks(img):
    """
    FIX 2: Draw road surface with asphalt + double-yellow center line + crosswalk.
    Replaces the v001 road that had only faded dashes (not a full solid road plane).
    """
    draw = ImageDraw.Draw(img)
    road_near_l = int(W * 0.18)
    road_near_r = int(W * 0.82)
    road_far_l  = vp_x_at_y(VP_Y + 4, road_near_l)
    road_far_r  = vp_x_at_y(VP_Y + 4, road_near_r)

    # FIX 2: Full asphalt road surface — solid trapezoid
    road_poly = [
        (road_near_l, H),
        (road_near_r, H),
        (road_far_r,  VP_Y + 4),
        (road_far_l,  VP_Y + 4),
    ]
    draw.polygon(road_poly, fill=ROAD_ASPHALT)

    # Sun-side lighter strip (right lane, afternoon sun from right)
    sun_strip = [
        (road_near_l + (road_near_r - road_near_l)//2, H),
        (road_near_r, H),
        (road_far_r, VP_Y + 4),
        (road_far_l + (road_far_r - road_far_l)//2, VP_Y + 4),
    ]
    draw.polygon(sun_strip, fill=ROAD_ASPHALT_LT)

    # Sidewalk left
    sw_l_edge = int(W * 0.03)
    swl_poly = [
        (sw_l_edge, H),
        (road_near_l, H),
        (vp_x_at_y(VP_Y + 4, road_near_l), VP_Y + 4),
        (vp_x_at_y(VP_Y + 4, sw_l_edge),    VP_Y + 4),
    ]
    draw.polygon(swl_poly, fill=SIDEWALK)

    # Sidewalk right
    sw_r_edge = int(W * 0.97)
    swr_poly = [
        (road_near_r, H),
        (sw_r_edge, H),
        (vp_x_at_y(VP_Y + 4, sw_r_edge),    VP_Y + 4),
        (vp_x_at_y(VP_Y + 4, road_near_r), VP_Y + 4),
    ]
    draw.polygon(swr_poly, fill=SIDEWALK)

    # FIX 2: Double-yellow center line — two parallel perspective-correct lines
    # Center of road at vanishing point
    rng = random.Random(7)
    n_segs = 14
    for line_offset in [-3, 3]:   # two lines side by side = double yellow
        pts = []
        for i in range(n_segs + 1):
            t = i / n_segs
            y = int(lerp(H, VP_Y + 4, t))
            road_left_x  = vp_x_at_y(y, road_near_l)
            road_right_x = vp_x_at_y(y, road_near_r)
            cx = (road_left_x + road_right_x) // 2
            # Offset by perspective-scaled amount
            scale = 1.0 - t * 0.8
            offset = int(line_offset * scale)
            pts.append((cx + offset, y))
        # Draw as dashed line (alternate segments)
        for i in range(0, len(pts) - 1, 2):
            lw = max(1, int(lerp(2, 1, i / n_segs)))
            # Fade paint with distance
            fade = 0.5 + 0.5 * (1.0 - i / n_segs)
            col = lerp_color(CENTER_LINE_Y, ROAD_ASPHALT, 1.0 - fade)
            draw.line([pts[i], pts[i + 1]], fill=col, width=lw)

    # FIX 2: Crosswalk stripes at near end (bottom of frame)
    cw_y_top = int(H * 0.88)
    cw_y_bot = H - 8
    road_l_at_cw = vp_x_at_y(cw_y_top, road_near_l)
    road_r_at_cw = vp_x_at_y(cw_y_top, road_near_r)
    road_w_at_cw = road_r_at_cw - road_l_at_cw
    n_stripes = 8
    stripe_w = max(8, road_w_at_cw // (n_stripes * 2))
    for si in range(n_stripes):
        # Start position of each stripe — evenly spaced across road width
        sx_t = (si * 2 + 0.3) / (n_stripes * 2)
        sx_near = int(road_l_at_cw + sx_t * road_w_at_cw)
        sx_far_t = sx_t + stripe_w / road_w_at_cw
        sx_near_r = int(road_l_at_cw + sx_far_t * road_w_at_cw)
        # Trapezoid stripe projecting toward VP
        road_l_bot = vp_x_at_y(cw_y_bot, road_near_l)
        road_r_bot = vp_x_at_y(cw_y_bot, road_near_r)
        road_w_bot = road_r_bot - road_l_bot
        sy_bt = sx_t
        sy_bt_r = sx_far_t
        sx_bot = int(road_l_bot + sy_bt * road_w_bot)
        sx_bot_r = int(road_l_bot + sy_bt_r * road_w_bot)
        stripe_pts = [
            (sx_bot, cw_y_bot),
            (sx_bot_r, cw_y_bot),
            (sx_near_r, cw_y_top),
            (sx_near, cw_y_top),
        ]
        draw.polygon(stripe_pts, fill=CROSSWALK_WHITE)

    # Sidewalk cracks (left)
    rng2 = random.Random(13)
    for _ in range(18):
        cx_c = rng2.randint(int(W * 0.04), int(W * 0.17))
        cy_c = rng2.randint(int(H * 0.65), H - 5)
        cl = rng2.randint(8, 28)
        ang = rng2.uniform(0, math.pi)
        ex = int(cx_c + math.cos(ang) * cl)
        ey = int(cy_c + math.sin(ang) * cl * 0.4)
        draw.line([(cx_c, cy_c), (ex, ey)], fill=SIDEWALK_SHADOW, width=1)
    for _ in range(14):
        cx_c = rng2.randint(int(W * 0.83), int(W * 0.96))
        cy_c = rng2.randint(int(H * 0.65), H - 5)
        cl = rng2.randint(6, 22)
        ang = rng2.uniform(0, math.pi)
        ex = int(cx_c + math.cos(ang) * cl)
        ey = int(cy_c + math.sin(ang) * cl * 0.4)
        draw.line([(cx_c, cy_c), (ex, ey)], fill=SIDEWALK_SHADOW, width=1)

    # Curb lines (road edge lines)
    draw.line([(road_near_l, H), (road_far_l, VP_Y + 4)], fill=SIDEWALK_SHADOW, width=2)
    draw.line([(road_near_r, H), (road_far_r, VP_Y + 4)], fill=SIDEWALK_SHADOW, width=2)

    return ImageDraw.Draw(img)


def rect_in_perspective(left_x, right_x, top_y, bot_y):
    return [(left_x, bot_y), (right_x, bot_y), (right_x, top_y), (left_x, top_y)]


# ── Building helpers ───────────────────────────────────────────────────────────

def draw_building(draw, img,
                  x0, x1, y_base, y_roof,
                  wall_col, shadow_col, roof_col,
                  lean=0, has_upper=True, upper_floors=1):
    lean_px = int(lean * (y_base - y_roof) / 200)
    pts = [(x0 + lean_px, y_base),
           (x1 + lean_px, y_base),
           (x1, y_roof),
           (x0, y_roof)]
    draw.polygon(pts, fill=wall_col)
    shadow_w = int((x1 - x0) * 0.18)
    shd_pts = [(x0 + lean_px, y_base),
               (x0 + lean_px + shadow_w, y_base),
               (x0 + shadow_w, y_roof),
               (x0, y_roof)]
    draw.polygon(shd_pts, fill=shadow_col)
    draw.rectangle([x0, y_roof - 6, x1, y_roof], fill=roof_col)
    return lean_px


def draw_window(draw, x, y, w, h, col=WINDOW_LIT, frame_col=CREAM_FACADE, curtain=False):
    draw.rectangle([x, y, x + w, y + h], fill=col)
    draw.rectangle([x - 2, y - 2, x + w + 2, y + h + 2], outline=frame_col, width=2)
    if curtain:
        draw.rectangle([x + 2, y + h//2, x + w - 2, y + h - 2],
                       fill=lerp_color(col, WARM_CREAM, 0.4))


def draw_awning(draw, ax, ay, aw, depth, col, shadow_col):
    front_y = ay + depth
    draw.polygon([(ax, ay), (ax + aw, ay), (ax + aw, front_y), (ax, front_y)], fill=col)
    draw.rectangle([ax, front_y - 4, ax + aw, front_y], fill=shadow_col)
    n_stripes = max(2, aw // 20)
    for i in range(n_stripes):
        sx = ax + i * (aw // n_stripes)
        draw.line([(sx, ay), (sx, front_y)], fill=shadow_col, width=1)


def draw_sign_board(draw, x, y, w, h, text_lines, bg_col=SIGN_CREAM, text_col=DEEP_COCOA):
    draw.rectangle([x, y, x + w, y + h], fill=bg_col)
    draw.rectangle([x, y, x + w, y + h], outline=text_col, width=2)
    rng_s = random.Random(hash(str(text_lines)))
    line_h = max(3, (h - 8) // max(1, len(text_lines)))
    for i, line in enumerate(text_lines):
        ly = y + 4 + i * line_h
        word_x = x + 4
        for word in line.split():
            ww = rng_s.randint(6, max(7, w // 4))
            ww = min(ww, x + w - word_x - 4)
            if ww > 2:
                draw.rectangle([word_x, ly + 1, word_x + ww, ly + line_h - 2],
                                fill=text_col)
            word_x += ww + 3
            if word_x > x + w - 8:
                break


# ── LEFT SIDE BUILDINGS ────────────────────────────────────────────────────────

def draw_left_buildings(img):
    draw = ImageDraw.Draw(img)

    bx0, bx1 = -10, 210
    by_base = H
    by_roof = int(H * 0.26)
    lean = draw_building(draw, img, bx0, bx1, by_base, by_roof,
                         CREAM_FACADE, lerp_color(CREAM_FACADE, DUSTY_LAVENDER, 0.35),
                         TIN_ROOF, lean=2)
    draw_awning(draw, bx0 + lean + 10, by_roof + 90, bx1 - bx0 - 20, 28,
                SAGE_GREEN, lerp_color(SAGE_GREEN, DEEP_SAGE, 0.6))
    draw_sign_board(draw, bx0 + lean + 14, by_roof + 40, 140, 28,
                    ["FINCH'S BAKERY", "est. 1958"], SIGN_CREAM)
    draw_window(draw, bx0 + lean + 18, by_roof + 120, 140, 70,
                WINDOW_LIT, CREAM_FACADE, curtain=True)
    for floor in range(2):
        wy = by_roof + 15 + floor * 36
        for wx in [bx0 + lean + 20, bx0 + lean + 90]:
            draw_window(draw, wx, wy, 34, 28, WINDOW_LIT, CREAM_FACADE)
    draw.rectangle([bx0 + lean + 18, by_roof + 190, bx0 + lean + 78, by_roof + 204],
                   fill=SUNLIT_AMBER)
    draw.rectangle([bx0 + lean + 84, by_roof + 190, bx0 + lean + 158, by_roof + 204],
                   fill=SUNLIT_AMBER)
    rng = random.Random(88)
    for _ in range(16):
        px = rng.randint(bx0 + lean + 20, bx0 + lean + 155)
        py = by_roof + 192
        draw.ellipse([px - 3, py - 6, px + 3, py], fill=lerp_color(TERRACOTTA, SOFT_GOLD, 0.4))
    draw = ImageDraw.Draw(img)

    bx0_h, bx1_h = 205, 480
    by_roof_h = int(H * 0.20)
    lean_h = draw_building(draw, img, bx0_h, bx1_h, by_base, by_roof_h,
                           TERRACOTTA, RUST_SHADOW, SLATE_ROOF, lean=-3)
    rng = random.Random(3)
    for row in range(0, by_base - by_roof_h, 10):
        offset = (row // 10) % 2 * 9
        for col_x in range(bx0_h + lean_h + offset, bx1_h, 18):
            if rng.random() < 0.7:
                draw.rectangle([col_x, by_roof_h + row + 2,
                                 col_x + 7, by_roof_h + row + 7],
                                fill=lerp_color(TERRACOTTA, BRICK_DARK, 0.25))
    draw = ImageDraw.Draw(img)
    draw_awning(draw, bx0_h + lean_h + 8, by_roof_h + 110, bx1_h - bx0_h - 16, 26,
                lerp_color(SAGE_GREEN, TERRACOTTA, 0.3),
                lerp_color(DEEP_SAGE, RUST_SHADOW, 0.3))
    draw_sign_board(draw, bx0_h + lean_h + 12, by_roof_h + 60, 210, 30,
                    ["KOWALSKI HARDWARE", "PLUMBING - ELECTRIC - MISC"], SIGN_CREAM)
    draw_window(draw, bx0_h + lean_h + 20, by_roof_h + 138, 200, 80, WINDOW_LIT, CREAM_FACADE)
    draw.rectangle([bx0_h + lean_h + 22, by_roof_h + 140,
                    bx0_h + lean_h + 218, by_roof_h + 216],
                   fill=lerp_color(INTERIOR_WARM, WINDOW_DARK, 0.3))
    draw = ImageDraw.Draw(img)
    for floor in range(2):
        wy = by_roof_h + 14 + floor * 44
        for wx in [bx0_h + lean_h + 22, bx0_h + lean_h + 120, bx0_h + lean_h + 208]:
            draw_window(draw, wx, wy, 40, 32, WINDOW_LIT, CREAM_FACADE)
    draw.rectangle([bx0_h + lean_h + 240, by_roof_h + 135, bx0_h + lean_h + 260, by_base - 5],
                   fill=DEEP_COCOA)
    for tool_y in [by_roof_h + 150, by_roof_h + 175, by_roof_h + 200]:
        draw.line([(bx0_h + lean_h + 244, tool_y), (bx0_h + lean_h + 285, tool_y - 40)],
                  fill=DEEP_COCOA, width=2)

    bx0_s, bx1_s = 475, 545
    by_roof_s = int(H * 0.14)
    lean_s = draw_building(draw, img, bx0_s, bx1_s, by_base, by_roof_s,
                           CREAM_FACADE, lerp_color(CREAM_FACADE, DUSTY_LAVENDER, 0.4),
                           TERRA_ROOF, lean=3)
    for floor in range(3):
        wy = by_roof_s + 14 + floor * 42
        draw_window(draw, bx0_s + lean_s + 8, wy, 24, 28, WINDOW_DARK, CREAM_FACADE)

    bx0_po, bx1_po = 540, 750
    by_roof_po = int(H * 0.18)
    lean_po = draw_building(draw, img, bx0_po, bx1_po, by_base, by_roof_po,
                            lerp_color(TERRACOTTA, WARM_CREAM, 0.5),
                            lerp_color(DUSTY_LAVENDER, RUST_SHADOW, 0.2),
                            TIN_ROOF, lean=-2)
    for wx in [bx0_po + lean_po + 14, bx0_po + lean_po + 90, bx0_po + lean_po + 166]:
        draw_window(draw, wx, by_roof_po + 100, 50, 65, WINDOW_LIT, CREAM_FACADE)
    for wx in [bx0_po + lean_po + 20, bx0_po + lean_po + 100, bx0_po + lean_po + 174]:
        draw_window(draw, wx, by_roof_po + 20, 36, 52, WINDOW_LIT, CREAM_FACADE)
    draw.line([(bx0_po + lean_po + 100, by_roof_po - 40),
               (bx0_po + lean_po + 100, by_roof_po - 6)],
              fill=DEEP_COCOA, width=2)
    draw.polygon([(bx0_po + lean_po + 101, by_roof_po - 38),
                  (bx0_po + lean_po + 122, by_roof_po - 30),
                  (bx0_po + lean_po + 101, by_roof_po - 22)],
                 fill=TERRACOTTA)
    draw = ImageDraw.Draw(img)
    return draw


# ── RIGHT SIDE BUILDINGS ───────────────────────────────────────────────────────

def draw_right_buildings(img):
    draw = ImageDraw.Draw(img)
    by_base = H

    bx0_cs, bx1_cs = W - 260, W + 10
    by_roof_cs = int(H * 0.24)
    lean_cs = draw_building(draw, img, bx0_cs, bx1_cs, by_base, by_roof_cs,
                            lerp_color(TERRACOTTA, CREAM_FACADE, 0.6),
                            lerp_color(DUSTY_LAVENDER, RUST_SHADOW, 0.25),
                            SLATE_ROOF, lean=2)
    draw_awning(draw, bx0_cs + lean_cs + 6, by_roof_cs + 85, bx1_cs - bx0_cs - 14, 28,
                SAGE_GREEN, DEEP_SAGE)
    draw.polygon([(bx0_cs - 8, by_base - 5),
                  (bx0_cs + 44, by_base - 5),
                  (bx0_cs + 36, by_base - 55),
                  (bx0_cs, by_base - 55)],
                 fill=SIGN_CREAM)
    draw.rectangle([bx0_cs - 8, by_base - 56, bx0_cs + 44, by_base - 4],
                   outline=DEEP_COCOA, width=2)
    for ty in [by_base - 48, by_base - 36, by_base - 24]:
        draw.rectangle([bx0_cs + 2, ty, bx0_cs + 34, ty + 7], fill=DEEP_COCOA)
    draw_sign_board(draw, bx0_cs + lean_cs + 10, by_roof_cs + 44, 190, 24,
                    ["MILLBROOK GENERAL"], SIGN_CREAM)
    draw_window(draw, bx0_cs + lean_cs + 12, by_roof_cs + 113, 185, 78,
                WINDOW_LIT, CREAM_FACADE, curtain=True)
    draw.ellipse([bx0_cs + lean_cs + 140, by_roof_cs + 118,
                  bx0_cs + lean_cs + 165, by_roof_cs + 150],
                 fill=NEON_RED)
    for wx in [bx0_cs + lean_cs + 16, bx0_cs + lean_cs + 110]:
        draw_window(draw, wx, by_roof_cs + 18, 42, 50, WINDOW_LIT, CREAM_FACADE)
    draw = ImageDraw.Draw(img)

    bx0_d, bx1_d = W - 530, W - 255
    by_roof_d = int(H * 0.30)
    lean_d = draw_building(draw, img, bx0_d, bx1_d, by_base, by_roof_d,
                           CREAM_FACADE, DUSTY_LAVENDER,
                           TIN_ROOF, lean=-1)
    draw_window(draw, bx0_d + lean_d + 12, by_roof_d + 35, 220, 95,
                lerp_color(WINDOW_LIT, WINDOW_DARK, 0.35), CREAM_FACADE)
    for bth_x in [bx0_d + lean_d + 20, bx0_d + lean_d + 70, bx0_d + lean_d + 120]:
        draw.rectangle([bth_x, by_roof_d + 80, bth_x + 38, by_roof_d + 128],
                       fill=lerp_color(TERRACOTTA, DEEP_COCOA, 0.4))
    draw = ImageDraw.Draw(img)
    draw_sign_board(draw, bx0_d + lean_d + 14, by_roof_d + 8, 200, 22,
                    ["MILLBROOK DINER"], NEON_RED, text_col=WARM_CREAM)
    neon_x = bx0_d + lean_d + 14 + 100
    neon_y = by_roof_d + 8 + 11
    for r in range(18, 4, -3):
        alpha = max(0, 80 - r * 4)
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.ellipse([neon_x - r, neon_y - r//2, neon_x + r, neon_y + r//2],
                   fill=(255, 96, 80, alpha))
        img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"),
                  (0, 0))
    draw = ImageDraw.Draw(img)

    bx0_bk, bx1_bk = W - 740, W - 525
    by_roof_bk = int(H * 0.22)
    lean_bk = draw_building(draw, img, bx0_bk, bx1_bk, by_base, by_roof_bk,
                            DARK_SAGE_FACADE, lerp_color(DARK_SAGE_FACADE, DEEP_COCOA, 0.35),
                            SLATE_ROOF, lean=3)
    bay_x0 = bx0_bk + lean_bk + 20
    bay_y0 = by_roof_bk + 90
    draw.rectangle([bay_x0, bay_y0, bay_x0 + 90, by_roof_bk + 170], fill=WINDOW_LIT)
    draw.rectangle([bay_x0, bay_y0, bay_x0 + 90, by_roof_bk + 170],
                   outline=DEEP_COCOA, width=2)
    rng = random.Random(55)
    for _ in range(12):
        bx = rng.randint(bay_x0 + 2, bay_x0 + 82)
        by_b = rng.randint(bay_y0 + 30, by_roof_bk + 160)
        bw = rng.randint(6, 14)
        bh = rng.randint(12, 28)
        draw.rectangle([bx, by_b - bh, bx + bw, by_b],
                       fill=lerp_color(SUNLIT_AMBER, TERRACOTTA, rng.random()))
    draw = ImageDraw.Draw(img)
    for wx in [bx0_bk + lean_bk + 18, bx0_bk + lean_bk + 100]:
        draw_window(draw, wx, by_roof_bk + 18, 38, 44, WINDOW_DARK, DARK_SAGE_FACADE)

    bx0_ef, bx1_ef = W - 920, W - 735
    by_roof_ef = int(H * 0.25)
    lean_ef = draw_building(draw, img, bx0_ef, bx1_ef, by_base, by_roof_ef,
                            CREAM_FACADE, lerp_color(CREAM_FACADE, DUSTY_LAVENDER, 0.4),
                            TERRA_ROOF, lean=-2)
    draw.rectangle([bx0_ef + lean_ef + 14, by_roof_ef + 60,
                    bx0_ef + lean_ef + 140, by_roof_ef + 140],
                   fill=lerp_color(SIGN_CREAM, SUNLIT_AMBER, 0.3))
    draw.rectangle([bx0_ef + lean_ef + 14, by_roof_ef + 60,
                    bx0_ef + lean_ef + 140, by_roof_ef + 140],
                   outline=DEEP_COCOA, width=1)
    draw_sign_board(draw, bx0_ef + lean_ef + 30, by_roof_ef + 70, 80, 18,
                    ["FOR LEASE"], lerp_color(SIGN_CREAM, DUSTY_LAVENDER, 0.2))
    draw_window(draw, bx0_ef + lean_ef + 28, by_roof_ef + 16, 52, 36, WINDOW_DARK, CREAM_FACADE)
    draw = ImageDraw.Draw(img)
    return draw


# ── STREET TREES ──────────────────────────────────────────────────────────────

def draw_street_trees(img):
    draw = ImageDraw.Draw(img)
    rng = random.Random(21)
    left_trees = [
        (80,  int(H * 0.68)),
        (340, int(H * 0.63)),
        (520, int(H * 0.60)),
    ]
    right_trees = [
        (W - 100, int(H * 0.68)),
        (W - 340, int(H * 0.63)),
        (W - 520, int(H * 0.60)),
    ]
    for tx, ty in left_trees + right_trees:
        trunk_h = rng.randint(55, 90)
        trunk_w = max(6, int((ty - VP_Y) / (H - VP_Y) * 16))
        draw.rectangle([tx - trunk_w//2, ty - trunk_h,
                        tx + trunk_w//2, ty], fill=WOOD_BROWN)
        canopy_r = int((ty - VP_Y) / (H - VP_Y) * 70) + 20
        for _ in range(22):
            ox = rng.randint(-canopy_r, canopy_r)
            oy = rng.randint(-canopy_r, int(canopy_r * 0.4))
            r = rng.randint(canopy_r // 4, canopy_r // 2)
            leaf_col = rng.choice([LEAF_SUN, LEAF_MID, LEAF_SHADOW,
                                   lerp_color(LEAF_SUN, LEAF_MID, 0.5)])
            draw.ellipse([tx + ox - r, ty - trunk_h + oy - r,
                          tx + ox + r, ty - trunk_h + oy + r],
                         fill=leaf_col)
    draw = ImageDraw.Draw(img)
    return draw


# ── PARKED CARS ────────────────────────────────────────────────────────────────

def draw_parked_cars(img):
    draw = ImageDraw.Draw(img)
    cx, cy = 600, H - 30
    cw, ch = 110, 44
    draw.rectangle([cx, cy - ch, cx + cw, cy], fill=PARKED_CAR_2)
    draw.rectangle([cx + 18, cy - ch - 24, cx + cw - 18, cy - ch + 4], fill=lerp_color(PARKED_CAR_2, DEEP_COCOA, 0.4))
    draw.rectangle([cx + 22, cy - ch - 20, cx + 58, cy - ch + 2], fill=WINDOW_LIT)
    draw.rectangle([cx + 60, cy - ch - 20, cx + cw - 20, cy - ch + 2], fill=WINDOW_DARK)
    for wx in [cx + 16, cx + cw - 22]:
        draw.ellipse([wx - 8, cy - 14, wx + 8, cy + 2], fill=DEEP_COCOA)
    cx2 = W - 580
    cy2 = H - 28
    cw2, ch2 = 95, 38
    draw.rectangle([cx2, cy2 - ch2, cx2 + cw2, cy2], fill=PARKED_CAR_1)
    draw.rectangle([cx2 + 14, cy2 - ch2 - 20, cx2 + cw2 - 14, cy2 - ch2 + 4],
                   fill=lerp_color(PARKED_CAR_1, DEEP_COCOA, 0.45))
    draw.rectangle([cx2 + 18, cy2 - ch2 - 16, cx2 + 50, cy2 - ch2 + 2], fill=WINDOW_LIT)
    draw.rectangle([cx2 + 52, cy2 - ch2 - 16, cx2 + cw2 - 16, cy2 - ch2 + 2], fill=WINDOW_DARK)
    for wx in [cx2 + 14, cx2 + cw2 - 18]:
        draw.ellipse([wx - 7, cy2 - 12, wx + 7, cy2 + 1], fill=DEEP_COCOA)
    draw = ImageDraw.Draw(img)
    return draw


# ── CLOCK TOWER ────────────────────────────────────────────────────────────────

def draw_clock_tower(img):
    draw = ImageDraw.Draw(img)
    ctx = VP_X - 8
    cty_base = VP_Y + 80
    cty_top  = VP_Y - 110
    ctw = 50
    draw.rectangle([ctx - ctw//2, cty_top, ctx + ctw//2, cty_base], fill=CLOCK_STONE)
    draw.rectangle([ctx - ctw//2 - 4, cty_top - 8, ctx + ctw//2 + 4, cty_top], fill=CLOCK_STONE)
    clock_r = 16
    clock_cx = ctx
    clock_cy = cty_top + 26
    draw.ellipse([clock_cx - clock_r, clock_cy - clock_r,
                  clock_cx + clock_r, clock_cy + clock_r], fill=CLOCK_FACE_CLR)
    draw.ellipse([clock_cx - clock_r, clock_cy - clock_r,
                  clock_cx + clock_r, clock_cy + clock_r], outline=CLOCK_STONE, width=2)
    draw.line([(clock_cx, clock_cy), (clock_cx - 4, clock_cy - 10)],
              fill=DEEP_COCOA, width=2)
    draw.line([(clock_cx, clock_cy), (clock_cx + 6, clock_cy - 12)],
              fill=DEEP_COCOA, width=1)
    draw.polygon([(ctx, cty_top - 8), (ctx - 6, cty_top - 18), (ctx + 8, cty_top - 14)],
                 fill=DEEP_COCOA)
    draw.line([(ctx, cty_top - 8), (ctx, cty_top - 22)], fill=DEEP_COCOA, width=1)
    rng = random.Random(66)
    for p_ox, p_oy in [(-10, 0), (14, -3), (4, -28)]:
        draw.ellipse([clock_cx + p_ox - 3, clock_cy + p_oy - 3,
                      clock_cx + p_ox + 3, clock_cy + p_oy + 2],
                     fill=lerp_color(DEEP_COCOA, DUSTY_LAVENDER, 0.4))
    draw = ImageDraw.Draw(img)
    return draw


# ── POWER POLES & WIRES — FIX 1 ───────────────────────────────────────────────

def draw_power_infrastructure(img):
    """
    FIX 1: Power lines now perspective-correct with proper weights:
    - Main cable on each pole: 3px, converges to VP
    - Span wires (pole-to-pole along street): 1px
    - Slight catenary sag via parabolic curve (not straight)
    - Reduced overall darkness
    """
    draw = ImageDraw.Draw(img)
    rng = random.Random(99)

    poles_left  = [(60, H, 200), (240, H - 25, 175), (430, H - 50, 155),
                   (590, H - 70, 140), (690, H - 82, 130)]
    poles_right = [(W - 60, H, 200), (W - 230, H - 25, 175), (W - 420, H - 50, 155),
                   (W - 580, H - 70, 140), (W - 680, H - 82, 130)]

    all_poles = poles_left + poles_right

    def draw_pole(px, py, ph):
        # FIX 1: Pole width scales with perspective (further = thinner)
        dist_to_vp = abs(px - VP_X) / (W * 0.5)
        pw = max(2, int(ph / 50 * (0.5 + dist_to_vp * 0.5)))
        lean = rng.randint(-3, 3)
        draw.rectangle([px - pw//2 + lean, py - ph, px + pw//2 + lean, py], fill=POWER_POLE)
        arm_y = py - ph + int(ph * 0.15)
        arm_len = int(ph * 0.22)
        draw.rectangle([px - arm_len + lean, arm_y - 4, px + arm_len + lean, arm_y],
                       fill=POWER_POLE)
        for ins_x in [px - arm_len + lean + 4, px + lean, px + arm_len + lean - 4]:
            draw.ellipse([ins_x - 3, arm_y - 6, ins_x + 3, arm_y],
                         fill=lerp_color(WARM_CREAM, DUSTY_LAVENDER, 0.2))
        return px + lean, py - ph + int(ph * 0.15)

    pole_tops = {}
    for px, py, ph in all_poles:
        tx, ty = draw_pole(px, py, ph)
        pole_tops[(px, py)] = (tx, ty)

    # FIX 1: Main cables left-to-right cross-street — 3px with perspective sag
    wire_pairs = list(zip(poles_left, poles_right))
    for (lpx, lpy, lph), (rpx, rpy, rph) in wire_pairs:
        ltop = pole_tops[(lpx, lpy)]
        rtop = pole_tops[(rpx, rpy)]
        # Main cable: 3px at nearest, converges toward VP (thinner at distance)
        dist_near = max(lpx, W - rpx)
        dist_scale = max(0.3, 1.0 - (H - min(lpy, rpy)) / (H - VP_Y) * 0.6)
        main_w = max(1, int(3 * dist_scale))
        # Three wires at different heights
        for offset in [-4, 0, 5]:
            pts = []
            n_steps = 14
            for step in range(n_steps):
                t = step / (n_steps - 1)
                wx = int(lerp(ltop[0], rtop[0], t))
                wy_base = int(lerp(ltop[1], rtop[1], t))
                # Catenary sag: parabolic, more sag for closer (larger) spans
                sag_amount = int((1.0 - abs(2 * t - 1)) * 10 * dist_scale)
                wy = wy_base + sag_amount + offset
                pts.append((wx, wy))
            wire_w = main_w if offset == 0 else 1
            for i in range(len(pts) - 1):
                draw.line([pts[i], pts[i+1]], fill=POWER_LINE_CLR, width=wire_w)

    # FIX 1: Along-street wires — 1px span wires with catenary sag
    for side_poles in [poles_left, poles_right]:
        for i in range(len(side_poles) - 1):
            lpx, lpy, lph = side_poles[i]
            npx, npy, nph = side_poles[i + 1]
            ltop = pole_tops[(lpx, lpy)]
            ntop = pole_tops[(npx, npy)]
            for offset in [0, 5]:
                pts = []
                n_steps = 10
                for step in range(n_steps):
                    t = step / (n_steps - 1)
                    wx = int(lerp(ltop[0], ntop[0], t))
                    wy_base = int(lerp(ltop[1], ntop[1], t))
                    # Catenary sag for span wire — subtle
                    sag_amount = int((1.0 - abs(2 * t - 1)) * 5)
                    wy = wy_base + sag_amount + offset
                    pts.append((wx, wy))
                for j in range(len(pts) - 1):
                    draw.line([pts[j], pts[j+1]], fill=POWER_LINE_CLR, width=1)

    # Antennas on rooftops
    antenna_spots = [
        (50, int(H * 0.26)),    (130, int(H * 0.20)),
        (280, int(H * 0.18)),   (360, int(H * 0.16)),
        (500, int(H * 0.13)),   (620, int(H * 0.16)),
        (W - 180, int(H * 0.22)), (W - 300, int(H * 0.28)),
        (W - 400, int(H * 0.20)), (W - 580, int(H * 0.20)),
        (W - 660, int(H * 0.20)),
    ]
    for ax, ay in antenna_spots:
        atype = rng.randint(0, 3)
        draw.line([(ax, ay), (ax, ay - 28)], fill=ANTENNA_CLR, width=2)
        if atype == 0:
            draw.line([(ax, ay - 22), (ax - 14, ay - 40)], fill=ANTENNA_CLR, width=1)
            draw.line([(ax, ay - 22), (ax + 14, ay - 40)], fill=ANTENNA_CLR, width=1)
        elif atype == 1:
            draw.line([(ax - 10, ay - 20), (ax + 10, ay - 20)], fill=ANTENNA_CLR, width=1)
            draw.line([(ax - 6, ay - 28), (ax + 6, ay - 28)], fill=ANTENNA_CLR, width=1)
        elif atype == 2:
            draw.arc([ax - 8, ay - 36, ax + 8, ay - 24], 0, 180, fill=ANTENNA_CLR, width=2)
        else:
            for bar_y in [ay - 12, ay - 18, ay - 24, ay - 30]:
                bar_w = rng.randint(6, 16)
                draw.line([(ax - bar_w, bar_y), (ax + bar_w, bar_y)], fill=ANTENNA_CLR, width=1)

    draw = ImageDraw.Draw(img)
    return draw


# ── LIGHTING OVERLAYS ─────────────────────────────────────────────────────────

def draw_lighting(img):
    """Warm afternoon sun overlay from upper right, long cool cast shadows left."""
    sun_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sun_layer)
    for x in range(W // 2, W):
        t = (x - W // 2) / (W // 2)
        alpha = int(t * 26)
        sd.line([(x, 0), (x, H // 2)], fill=(232, 201, 90, alpha))
    base_rgba = img.convert("RGBA")
    img = Image.alpha_composite(base_rgba, sun_layer).convert("RGB")
    draw = ImageDraw.Draw(img)

    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = ImageDraw.Draw(shadow_layer)
    shadow_bands = [
        (int(W * 0.08), int(W * 0.03), 32, 28),
        (int(W * 0.28), int(W * 0.14), 28, 24),
        (int(W * 0.54), int(W * 0.40), 20, 20),
    ]
    for sx_top, sx_bot, sw, alpha in shadow_bands:
        pts = [
            (sx_top, int(H * 0.40)),
            (sx_top + sw, int(H * 0.40)),
            (sx_bot + sw, H),
            (sx_bot, H),
        ]
        sh.polygon(pts, fill=(*DUSTY_LAVENDER, alpha))
    base_rgba2 = img.convert("RGBA")
    img = Image.alpha_composite(base_rgba2, shadow_layer).convert("RGB")
    draw = ImageDraw.Draw(img)

    haze_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hz = ImageDraw.Draw(haze_layer)
    haze_cx = VP_X
    for r in range(220, 30, -10):
        alpha = max(0, int((220 - r) * 0.55))
        hz.ellipse([haze_cx - r, VP_Y - r // 2, haze_cx + r, VP_Y + r // 2],
                   fill=(*HAZE, alpha))
    base_rgba3 = img.convert("RGBA")
    img = Image.alpha_composite(base_rgba3, haze_layer).convert("RGB")
    draw = ImageDraw.Draw(img)

    return img, draw


# ── FOREGROUND DETAILS ────────────────────────────────────────────────────────

def draw_foreground_details(img):
    draw = ImageDraw.Draw(img)
    draw.rectangle([28, H - 80, 44, H], fill=lerp_color(POWER_POLE, DEEP_COCOA, 0.4))
    draw.line([(60, H - 15), (80, H - 30), (90, H - 12)], fill=DEEP_COCOA, width=2)
    draw.ellipse([78, H - 38, 86, H - 30], fill=SAGE_GREEN)
    rng = random.Random(66)
    for _ in range(14):
        lx = rng.randint(10, 200)
        ly = rng.randint(H - 40, H - 8)
        lr = rng.randint(3, 7)
        draw.ellipse([lx - lr, ly - lr//2, lx + lr, ly + lr//2],
                     fill=rng.choice([LEAF_SUN, LEAF_MID, LEAF_SHADOW]))
    for _ in range(10):
        lx = rng.randint(W - 200, W - 10)
        ly = rng.randint(H - 36, H - 6)
        lr = rng.randint(3, 6)
        draw.ellipse([lx - lr, ly - lr//2, lx + lr, ly + lr//2],
                     fill=rng.choice([LEAF_SUN, LEAF_MID]))
    draw = ImageDraw.Draw(img)
    return draw


# ── TOWN SQUARE TREES ──────────────────────────────────────────────────────────

def draw_square_trees(img):
    draw = ImageDraw.Draw(img)
    rng = random.Random(34)
    sq_trees = [
        (VP_X - 60, VP_Y + 55),
        (VP_X - 30, VP_Y + 45),
        (VP_X + 30, VP_Y + 45),
        (VP_X + 65, VP_Y + 55),
    ]
    for tx, ty in sq_trees:
        trunk_h = 30
        trunk_w = 5
        draw.rectangle([tx - trunk_w//2, ty - trunk_h, tx + trunk_w//2, ty], fill=WOOD_BROWN)
        for _ in range(10):
            ox = rng.randint(-22, 22)
            oy = rng.randint(-22, 6)
            r = rng.randint(10, 20)
            col = rng.choice([LEAF_SUN, LEAF_MID, SAGE_GREEN])
            draw.ellipse([tx + ox - r, ty - trunk_h + oy - r,
                          tx + ox + r, ty - trunk_h + oy + r], fill=col)
    ft_cx, ft_cy = VP_X - 6, VP_Y + 72
    ft_r = 18
    draw.ellipse([ft_cx - ft_r, ft_cy - ft_r//2, ft_cx + ft_r, ft_cy + ft_r//2],
                 fill=CLOCK_STONE)
    draw.ellipse([ft_cx - ft_r + 4, ft_cy - ft_r//2 + 3,
                  ft_cx + ft_r - 4, ft_cy + ft_r//2 - 3],
                 fill=SAGE_GREEN)
    for _ in range(12):
        wx = rng.randint(ft_cx - ft_r + 5, ft_cx + ft_r - 5)
        wy = rng.randint(ft_cy - 6, ft_cy + 4)
        draw.ellipse([wx - 2, wy - 3, wx + 2, wy + 1],
                     fill=rng.choice([SUNLIT_AMBER, TERRACOTTA, DUSTY_LAVENDER]))
    draw = ImageDraw.Draw(img)
    return draw


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    out_dir = "/home/wipkat/team/output/backgrounds/environments"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_ENV_millbrook_main_street.png")

    img = Image.new("RGB", (W, H), SKY_ZENITH)

    # 1. Sky
    draw = draw_sky(img)

    # 2. Road + Sidewalks (FIX 2: full asphalt surface + double-yellow + crosswalk)
    draw = draw_road_and_sidewalks(img)

    # 3. Right buildings
    draw = draw_right_buildings(img)

    # 4. Left buildings
    draw = draw_left_buildings(img)

    # 5. Clock tower + square
    draw = draw_clock_tower(img)
    draw = draw_square_trees(img)

    # 6. Street trees
    draw = draw_street_trees(img)

    # 7. Parked cars
    draw = draw_parked_cars(img)

    # 8. Power poles, wires, antennas (FIX 1: perspective-correct + catenary sag)
    draw = draw_power_infrastructure(img)

    # 9. Foreground details
    draw = draw_foreground_details(img)

    # 10. Lighting overlays
    img, draw = draw_lighting(img)

    draw = ImageDraw.Draw(img)
    img.save(out_path)
    print(f"Saved: {out_path}")
    print("Fix verification (Critique C9):")
    print("  [FIX 1] Power lines: 3px main cable + 1px spans + catenary sag + reduced darkness ✓")
    print("  [FIX 2] Road surface: full ROAD_ASPHALT plane + double-yellow + crosswalk stripes ✓")


if __name__ == "__main__":
    import argparse
    from LTG_TOOL_warmth_inject_hook import run_warmth_hook

    parser = argparse.ArgumentParser(description="LTG_TOOL_bg_millbrook_main_street — Millbrook Main Street")
    parser.add_argument(
        "--check-warmth",
        action="store_true",
        help="After generation run LTG_TOOL_warmth_inject if warm/cool QA fails; "
             "saves <name>_warminjected.png alongside the output.",
    )
    args = parser.parse_args()

    main()
    out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_millbrook_main_street.png"
    run_warmth_hook(out_path, enabled=args.check_warmth)
