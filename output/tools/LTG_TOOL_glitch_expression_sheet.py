#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_glitch_expression_sheet.py
Glitch — Expression Sheet v004 PYCAIRO REBUILD
"Luma & the Glitchkin" — Cycle 52 / Rin Yamamoto

v004 CHANGES (C52 — pycairo rebuild):
  Complete rebuild using pycairo for anti-aliased rendering.
  Diamond body, spikes, arm-spikes, and pixel eyes all rendered via cairo bezier paths.
  Hard-faceted geometry benefits from cairo's precise bezier curves.
  Preserves all v003 expression specs exactly (9 expressions, 3x3 grid).
  Interior desire states: YEARNING, COVETOUS, HOLLOW retained.

Output: output/characters/main/LTG_CHAR_glitch_expression_sheet.png
"""

import sys
import os
import math
import random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from LTG_TOOL_cairo_primitives import (
    create_surface, draw_bezier_path, draw_wobble_path,
    draw_smooth_polygon, draw_ellipse, set_color,
    stroke_path, fill_background, to_pil_image,
    LINE_WEIGHT_ANCHOR, LINE_WEIGHT_STRUCTURE, LINE_WEIGHT_DETAIL, _c
)

try:
    from LTG_TOOL_project_paths import output_dir
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)

from PIL import Image
import cairo
import numpy as np


# ── Palette ────────────────────────────────────────────────────────────────────
CORRUPT_AMB    = (255, 140,   0)
CORRUPT_AMB_SH = (168,  76,   0)
CORRUPT_AMB_HL = (255, 185,  80)
SOFT_GOLD      = (232, 201,  90)
HOT_MAG        = (255,  45, 107)
UV_PURPLE      = (123,  47, 190)
ACID_GREEN     = ( 57, 255,  20)
ELEC_CYAN      = (  0, 240, 255)
VOID_BLACK     = ( 10,  10,  20)
STATIC_WHITE   = (248, 246, 236)
CANVAS_BG      = ( 10,  10,  20)

BG_NEUTRAL     = ( 22,  18,  32)
BG_MISCHIEVOUS = ( 28,  12,  18)
BG_PANICKED    = ( 12,  12,  22)
BG_TRIUMPHANT  = ( 32,  22,   8)
BG_STUNNED     = ( 18,  10,  28)
BG_CALCULATING = ( 14,  20,  14)
BG_YEARNING    = ( 12,  10,  28)
BG_COVETOUS    = ( 16,  12,  26)
BG_HOLLOW      = (  8,   8,  16)

HEADER_H  = 54
LABEL_H   = 36
PAD       = 18
COLS      = 3
ROWS      = 3
SCALE     = 2

CANVAS_W_1X = 1200
CANVAS_H_1X = 900

PANEL_W_1X = (CANVAS_W_1X - (COLS + 1) * PAD) // COLS
PANEL_H_1X = (CANVAS_H_1X - HEADER_H - ROWS * LABEL_H - (ROWS + 1) * PAD) // ROWS


# ── Geometry helpers ────────────────────────────────────────────────────────────

def diamond_pts(cx, cy, rx, ry, tilt_deg=0, squash=1.0, stretch=1.0):
    """Compute 4-point diamond vertices."""
    ry_eff = int(ry * squash * stretch)
    angle = math.radians(tilt_deg)
    top   = (cx + int(rx * 0.15 * math.sin(angle)),
             cy - ry_eff + int(rx * 0.15 * math.cos(angle)))
    right = (cx + int(rx * math.cos(-angle)),
             cy + int(rx * 0.2 * math.sin(-angle)))
    bot   = (cx - int(rx * 0.15 * math.sin(angle)),
             cy + int(ry_eff * 1.15))
    left  = (cx - int(rx * math.cos(-angle)),
             cy - int(rx * 0.2 * math.sin(-angle)))
    return [top, right, bot, left]


def draw_glitch_body_cairo(ctx, cx, cy, rx, ry, tilt_deg=0,
                            squash=1.0, stretch=1.0, crack_visible=True):
    """Draw Glitch's diamond body using pycairo with smooth edges."""
    pts = diamond_pts(cx, cy, rx, ry, tilt_deg, squash, stretch)
    top, right, bot, left = pts
    sh_pts = [(x + 3, y + 4) for x, y in pts]

    # UV_PURPLE shadow
    draw_smooth_polygon(ctx, sh_pts, bulge_frac=0.06)
    set_color(ctx, UV_PURPLE)
    ctx.fill()

    # Main body fill
    draw_smooth_polygon(ctx, pts, bulge_frac=0.06)
    set_color(ctx, CORRUPT_AMB)
    ctx.fill()

    # Highlight facet (top-left triangle)
    mid_tl = ((top[0] + left[0]) // 2, (top[1] + left[1]) // 2)
    ctr = (cx, cy - ry // 4)
    ctx.move_to(top[0], top[1])
    ctx.line_to(ctr[0], ctr[1])
    ctx.line_to(mid_tl[0], mid_tl[1])
    ctx.close_path()
    set_color(ctx, CORRUPT_AMB_HL)
    ctx.fill()

    # Outline with slight wobble for organic feel
    draw_wobble_path(ctx, pts, amplitude=0.4, frequency=0.08, seed=42)
    set_color(ctx, VOID_BLACK)
    ctx.set_line_width(LINE_WEIGHT_ANCHOR)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.stroke()

    # HOT_MAG crack
    if crack_visible:
        cs = (cx - rx // 2, cy - ry // 3)
        ce = (cx + rx // 3, cy + ry // 2)
        ctx.move_to(cs[0], cs[1])
        ctx.line_to(ce[0], ce[1])
        set_color(ctx, HOT_MAG)
        ctx.set_line_width(2)
        ctx.stroke()
        # Fork branch
        mid_c = ((cs[0] + ce[0]) // 2, (cs[1] + ce[1]) // 2)
        fork = (cx + rx // 2, cy - ry // 4)
        ctx.move_to(mid_c[0], mid_c[1])
        ctx.line_to(fork[0], fork[1])
        set_color(ctx, HOT_MAG)
        ctx.set_line_width(1.5)
        ctx.stroke()


def draw_top_spike_cairo(ctx, cx, cy_top, rx, spike_h=12, tilt_off=0):
    """Draw Glitch's 5-point crown spike using cairo bezier paths."""
    sx = cx + tilt_off
    pts = [
        (sx - spike_h // 2, cy_top),
        (sx - spike_h,      cy_top - spike_h),
        (sx,                cy_top - spike_h * 2),
        (sx + spike_h,      cy_top - spike_h),
        (sx + spike_h // 2, cy_top),
    ]
    # Use smooth polygon for slightly organic crown
    draw_smooth_polygon(ctx, pts, bulge_frac=0.04)
    set_color(ctx, CORRUPT_AMB)
    ctx.fill()
    draw_smooth_polygon(ctx, pts, bulge_frac=0.04)
    set_color(ctx, VOID_BLACK)
    ctx.set_line_width(LINE_WEIGHT_STRUCTURE)
    ctx.stroke()

    # HOT_MAG spark at crown tip
    if spike_h >= 6:
        ctx.move_to(sx, cy_top - spike_h * 2)
        ctx.line_to(sx, cy_top - spike_h * 2 - 4)
        set_color(ctx, HOT_MAG)
        ctx.set_line_width(2)
        ctx.stroke()


def draw_bottom_spike_cairo(ctx, cx, cy_bot, spike_h=10):
    """Draw Glitch's downward hover spike."""
    pts = [
        (cx - spike_h // 2, cy_bot),
        (cx + spike_h // 2, cy_bot),
        (cx, cy_bot + spike_h + 4),
    ]
    ctx.move_to(pts[0][0], pts[0][1])
    for p in pts[1:]:
        ctx.line_to(p[0], p[1])
    ctx.close_path()
    set_color(ctx, CORRUPT_AMB_SH)
    ctx.fill_preserve()
    set_color(ctx, VOID_BLACK)
    ctx.set_line_width(LINE_WEIGHT_STRUCTURE)
    ctx.stroke()


def draw_arm_cairo(ctx, cx, cy, side='left', arm_dy=0, arm_dx=0, rx=34):
    """Draw Glitch's triangular arm-spike."""
    if side == 'left':
        ax = cx - rx - 6
        ay = cy + arm_dy
        tip = (ax - 14 + arm_dx, ay - 8)
    else:
        ax = cx + rx + 6
        ay = cy + arm_dy
        tip = (ax + 14 + arm_dx, ay - 8)
    pts = [(ax, ay - 5), (ax, ay + 5), tip]
    ctx.move_to(pts[0][0], pts[0][1])
    for p in pts[1:]:
        ctx.line_to(p[0], p[1])
    ctx.close_path()
    set_color(ctx, CORRUPT_AMB)
    ctx.fill_preserve()
    set_color(ctx, VOID_BLACK)
    ctx.set_line_width(LINE_WEIGHT_STRUCTURE)
    ctx.stroke()


def draw_pixel_eye_cairo(ctx, ex, ey, cell=5, expr='neutral', side='left'):
    """Draw Glitch's 3x3 pixel-grid eye on cairo context."""
    PIXEL_COLORS = {
        0: VOID_BLACK,
        1: CORRUPT_AMB_SH,
        2: CORRUPT_AMB,
        3: SOFT_GOLD,
        4: HOT_MAG,
        5: ACID_GREEN,
        6: UV_PURPLE,
        7: STATIC_WHITE,
    }
    GLYPHS = {
        'neutral':     [[0, 2, 0], [2, 1, 2], [0, 2, 0]],
        'mischievous': [[5, 0, 5], [0, 5, 0], [5, 0, 5]],
        'panicked':    [[4, 4, 4], [4, 0, 4], [4, 4, 4]],
        'triumphant':  [[3, 3, 3], [3, 3, 3], [3, 3, 3]],
        'stunned':     [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
        'calculating': [[5, 0, 5], [0, 5, 0], [5, 0, 5]],
        'yearning':    [[0, 6, 0], [6, 1, 6], [0, 6, 0]],
        'covetous':    [[5, 5, 5], [0, 5, 0], [0, 0, 0]],
        'hollow':      [[0, 0, 0], [0, 7, 0], [0, 0, 0]],
    }
    DESTAB = {
        'neutral':     [[1, 2, 0], [2, 0, 1], [0, 2, 1]],
        'mischievous': [[5, 0, 0], [0, 5, 5], [5, 0, 0]],
        'panicked':    [[4, 0, 4], [0, 4, 0], [4, 0, 4]],
        'triumphant':  [[3, 3, 1], [3, 3, 3], [1, 3, 3]],
        'stunned':     [[4, 0, 4], [4, 0, 0], [0, 4, 0]],
        'calculating': [[1, 0, 1], [0, 1, 0], [1, 0, 0]],
        'yearning':    [[0, 6, 0], [6, 1, 6], [0, 6, 0]],
        'covetous':    [[5, 5, 5], [0, 5, 0], [0, 0, 0]],
        'hollow':      [[0, 0, 0], [0, 7, 0], [0, 0, 0]],
    }
    glyph = DESTAB[expr] if side == 'right' else GLYPHS[expr]
    for row in range(3):
        for col in range(3):
            state = glyph[row][col]
            color = PIXEL_COLORS[state]
            px = ex + col * cell
            py = ey + row * cell
            ctx.rectangle(px, py, cell - 1, cell - 1)
            set_color(ctx, color)
            ctx.fill()


def draw_mouth_cairo(ctx, mx, my, expr='neutral', w=14):
    """Draw Glitch's mouth for each expression."""
    if expr == 'neutral':
        for i in range(3):
            ctx.rectangle(mx + i * 4, my, 2, 2)
            set_color(ctx, CORRUPT_AMB_SH)
            ctx.fill()
    elif expr == 'mischievous':
        w2 = w + 6
        ctx.move_to(mx, my)
        ctx.curve_to(mx + w2 // 3, my - 2, mx + 2 * w2 // 3, my - 5, mx + w2, my - 7)
        set_color(ctx, HOT_MAG)
        ctx.set_line_width(3)
        ctx.stroke()
        ctx.rectangle(mx + w2 - 1, my - 9, 4, 4)
        set_color(ctx, ACID_GREEN)
        ctx.fill()
    elif expr == 'panicked':
        draw_ellipse(ctx, mx + w // 2, my, w // 2 + 2, 6)
        set_color(ctx, VOID_BLACK)
        ctx.fill_preserve()
        set_color(ctx, HOT_MAG)
        ctx.set_line_width(3)
        ctx.stroke()
    elif expr == 'triumphant':
        ctx.move_to(mx - 2, my + 4)
        ctx.line_to(mx + w // 2, my - 9)
        ctx.line_to(mx + w + 2, my + 4)
        set_color(ctx, SOFT_GOLD)
        ctx.set_line_width(3)
        ctx.stroke()
        for gx in [mx + 2, mx + w // 2 - 2, mx + w // 2 + 2, mx + w - 3]:
            ctx.rectangle(gx, my - 12, 2, 3)
            set_color(ctx, STATIC_WHITE)
            ctx.fill()
    elif expr == 'stunned':
        draw_ellipse(ctx, mx + w // 2, my, w // 2 + 4, 8)
        set_color(ctx, VOID_BLACK)
        ctx.fill_preserve()
        set_color(ctx, HOT_MAG)
        ctx.set_line_width(3)
        ctx.stroke()
        for fx in [mx, mx + w // 3, mx + 2 * w // 3, mx + w]:
            ctx.move_to(fx, my - 7)
            ctx.line_to(fx, my - 12)
            set_color(ctx, ELEC_CYAN)
            ctx.set_line_width(1)
            ctx.stroke()
    elif expr == 'calculating':
        ctx.rectangle(mx + 2, my, 2, 2)
        set_color(ctx, CORRUPT_AMB_SH)
        ctx.fill()
        ctx.rectangle(mx + 8, my, 2, 2)
        set_color(ctx, CORRUPT_AMB_SH)
        ctx.fill()
    elif expr == 'yearning':
        pass  # No mouth — silence
    elif expr == 'covetous':
        ctx.move_to(mx, my)
        ctx.line_to(mx + w, my)
        set_color(ctx, CORRUPT_AMB_SH)
        ctx.set_line_width(2)
        ctx.stroke()
        ctx.move_to(mx + w, my)
        ctx.line_to(mx + w + 3, my - 3)
        set_color(ctx, ACID_GREEN)
        ctx.set_line_width(1)
        ctx.stroke()
    elif expr == 'hollow':
        ctx.rectangle(mx + w // 2 - 1, my, 2, 2)
        set_color(ctx, CORRUPT_AMB_SH)
        ctx.fill()


def draw_hover_confetti_cairo(ctx, cx, cy_bot, expr='neutral', seed=7):
    """Draw Glitch's hover confetti beneath bottom spike."""
    rng = random.Random(seed)
    confetti_colors = {
        'neutral':     [HOT_MAG, UV_PURPLE, VOID_BLACK],
        'mischievous': [ACID_GREEN, HOT_MAG, ACID_GREEN],
        'panicked':    [HOT_MAG, HOT_MAG, ELEC_CYAN],
        'triumphant':  [CORRUPT_AMB, SOFT_GOLD, HOT_MAG],
        'stunned':     [ELEC_CYAN, HOT_MAG, ELEC_CYAN, HOT_MAG],
        'calculating': [UV_PURPLE, VOID_BLACK, CORRUPT_AMB_SH],
        'yearning':    [],
        'covetous':    [UV_PURPLE, UV_PURPLE, CORRUPT_AMB_SH],
        'hollow':      [],
    }
    cols = confetti_colors.get(expr, [HOT_MAG, UV_PURPLE])
    count = {'neutral': 8, 'mischievous': 14, 'panicked': 22,
             'triumphant': 18, 'stunned': 20, 'calculating': 5,
             'yearning': 0, 'covetous': 4, 'hollow': 0}.get(expr, 8)
    spread = {'neutral': 24, 'mischievous': 28, 'panicked': 38,
              'triumphant': 32, 'stunned': 42, 'calculating': 14,
              'yearning': 0, 'covetous': 18, 'hollow': 0}.get(expr, 24)
    for _ in range(count):
        if not cols:
            break
        px = rng.randint(cx - spread, cx + spread)
        py_range = 22 if expr in ('panicked', 'stunned') else 16
        py = rng.randint(cy_bot + 4, cy_bot + py_range)
        sz = rng.choice([2, 3, 4])
        col = rng.choice(cols)
        ctx.rectangle(px, py, sz, sz)
        set_color(ctx, col)
        ctx.fill()


def draw_brows_cairo(ctx, leye_x, leye_y, reye_x, reye_y, expr):
    """Draw expression-specific brows."""
    brow_specs = {
        'panicked':    [(leye_x - 4, leye_y - 3, leye_x + 14, leye_y - 8, HOT_MAG, 3),
                        (reye_x - 2, reye_y - 8, reye_x + 16, reye_y - 3, HOT_MAG, 3)],
        'mischievous': [(leye_x, leye_y - 2, leye_x + 14, leye_y - 2, CORRUPT_AMB_SH, 2),
                        (reye_x, reye_y - 7, reye_x + 14, reye_y - 1, ACID_GREEN, 3)],
        'triumphant':  [(leye_x - 2, leye_y - 8, leye_x + 16, leye_y - 2, SOFT_GOLD, 3),
                        (reye_x - 2, reye_y - 2, reye_x + 16, reye_y - 8, SOFT_GOLD, 3)],
        'stunned':     [(leye_x - 4, leye_y - 10, leye_x + 14, leye_y - 5, ELEC_CYAN, 3),
                        (reye_x - 2, reye_y - 5, reye_x + 16, reye_y - 10, ELEC_CYAN, 3)],
        'calculating': [(leye_x - 2, leye_y - 8, leye_x + 14, leye_y - 2, ACID_GREEN, 3),
                        (reye_x, reye_y - 2, reye_x + 14, reye_y - 2, CORRUPT_AMB_SH, 1)],
        'yearning':    [(leye_x - 2, leye_y - 6, leye_x + 14, leye_y - 4, UV_PURPLE, 2),
                        (reye_x - 2, reye_y - 4, reye_x + 14, reye_y - 6, UV_PURPLE, 2)],
        'covetous':    [(leye_x - 2, leye_y - 3, leye_x + 14, leye_y - 7, ACID_GREEN, 3),
                        (reye_x - 2, reye_y - 7, reye_x + 14, reye_y - 3, ACID_GREEN, 3)],
        'hollow':      [(leye_x, leye_y - 2, leye_x + 14, leye_y - 2, CORRUPT_AMB_SH, 1),
                        (reye_x, reye_y - 2, reye_x + 14, reye_y - 2, CORRUPT_AMB_SH, 1)],
        'neutral':     [(leye_x, leye_y - 3, leye_x + 14, leye_y - 3, CORRUPT_AMB_SH, 1),
                        (reye_x, reye_y - 3, reye_x + 14, reye_y - 3, CORRUPT_AMB_SH, 1)],
    }
    brows = brow_specs.get(expr, [])
    for (x1, y1, x2, y2, color, width) in brows:
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        set_color(ctx, color)
        ctx.set_line_width(width)
        ctx.stroke()


def draw_expression_cairo(ctx, panel_cx, panel_cy, panel_w, panel_h, expr='neutral'):
    """Draw a single Glitch expression panel on cairo context."""
    cx = panel_cx
    cy = panel_cy + panel_h // 10

    params = {
        'neutral':     dict(tilt=0,   squash=1.0,  stretch=1.0,
                            arm_l_dy=0,   arm_r_dy=0,   spike_h=10, crack=True),
        'mischievous': dict(tilt=20,  squash=0.90, stretch=1.0,
                            arm_l_dy=-6,  arm_r_dy=14,  spike_h=14, crack=True),
        'panicked':    dict(tilt=-14, squash=0.55, stretch=1.0,
                            arm_l_dy=18,  arm_r_dy=6,   spike_h=6,  crack=True),
        'triumphant':  dict(tilt=0,   squash=1.0,  stretch=1.35,
                            arm_l_dy=-20, arm_r_dy=-22, spike_h=22, crack=True),
        'stunned':     dict(tilt=-18, squash=0.65, stretch=1.0,
                            arm_l_dy=-10, arm_r_dy=-8,  spike_h=8,  crack=True),
        'calculating': dict(tilt=0,   squash=1.0,  stretch=1.05,
                            arm_l_dy=-22, arm_r_dy=2,   spike_h=12, crack=True),
        'yearning':    dict(tilt=0,   squash=1.0,  stretch=1.0,
                            arm_l_dy=18, arm_r_dy=16,   spike_h=6,  crack=True),
        'covetous':    dict(tilt=12,  squash=0.85, stretch=1.0,
                            arm_l_dy=-8, arm_r_dy=-6,   spike_h=12, crack=True),
        'hollow':      dict(tilt=0,   squash=0.88, stretch=0.95,
                            arm_l_dy=14, arm_r_dy=20,   spike_h=4,  crack=True),
    }
    p = params.get(expr, params['neutral'])
    rx = 34
    ry = 38

    cy_bot = cy + int(ry * p['squash'] * p['stretch'] * 1.15) + 6
    draw_hover_confetti_cairo(ctx, cx, cy_bot, expr=expr, seed=hash(expr) % 100 + 1)
    draw_bottom_spike_cairo(ctx, cx, cy_bot - 2, spike_h=10)
    draw_glitch_body_cairo(ctx, cx, cy, rx, ry,
                           tilt_deg=p['tilt'], squash=p['squash'],
                           stretch=p['stretch'], crack_visible=p['crack'])
    draw_arm_cairo(ctx, cx, cy, side='left', arm_dy=p['arm_l_dy'], rx=rx)
    draw_arm_cairo(ctx, cx, cy, side='right', arm_dy=p['arm_r_dy'], rx=rx)

    cy_top = cy - int(ry * p['squash'] * p['stretch'])
    tilt_off = int(p['tilt'] * 0.4)
    draw_top_spike_cairo(ctx, cx, cy_top, rx, spike_h=p['spike_h'], tilt_off=tilt_off)

    # Face
    face_cy = cy - ry // 6
    cell = 5
    leye_x = cx - rx // 2 - cell * 3 // 2
    leye_y = face_cy - cell * 3 // 2
    draw_pixel_eye_cairo(ctx, leye_x, leye_y, cell=cell, expr=expr, side='left')
    reye_x = cx + rx // 2 - cell * 3 // 2
    reye_y = face_cy - cell * 3 // 2
    draw_pixel_eye_cairo(ctx, reye_x, reye_y, cell=cell, expr=expr, side='right')

    mouth_cx = cx - 7
    mouth_cy = face_cy + cell * 3 // 2 + 4
    draw_mouth_cairo(ctx, mouth_cx, mouth_cy, expr=expr, w=14)

    draw_brows_cairo(ctx, leye_x, leye_y, reye_x, reye_y, expr)


def build_sheet():
    """Build the 3x3 Glitch expression sheet using pycairo at 2x then downscale."""
    W2 = CANVAS_W_1X * SCALE
    H2 = CANVAS_H_1X * SCALE
    PW2 = PANEL_W_1X * SCALE
    PH2 = PANEL_H_1X * SCALE
    PAD2 = PAD * SCALE
    HEADER_H2 = HEADER_H * SCALE
    LABEL_H2 = LABEL_H * SCALE

    surface, ctx, _, _ = create_surface(W2, H2)
    fill_background(ctx, W2, H2, CANVAS_BG)

    EXPRESSIONS = [
        ("NEUTRAL",      BG_NEUTRAL),
        ("MISCHIEVOUS",  BG_MISCHIEVOUS),
        ("PANICKED",     BG_PANICKED),
        ("TRIUMPHANT",   BG_TRIUMPHANT),
        ("STUNNED",      BG_STUNNED),
        ("CALCULATING",  BG_CALCULATING),
        ("YEARNING",     BG_YEARNING),
        ("COVETOUS",     BG_COVETOUS),
        ("HOLLOW",       BG_HOLLOW),
    ]

    # Title header
    ctx.rectangle(0, 0, W2, HEADER_H2)
    set_color(ctx, (18, 14, 26))
    ctx.fill()

    ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(24 * SCALE)
    title_text = "GLITCH — Expression Sheet v004  [C52 pycairo — 9 Expressions]"
    ext = ctx.text_extents(title_text)
    ctx.move_to((W2 - ext.width) / 2, (HEADER_H2 + ext.height) / 2 - 10 * SCALE)
    ctx.set_source_rgb(*_c(CORRUPT_AMB))
    ctx.show_text(title_text)

    ctx.set_font_size(10 * SCALE)
    sub_text = "ANTAGONIST  |  GL-07 CORRUPT AMBER  |  CYCLE 52 pycairo rebuild  |  1200x900  3x3"
    ext2 = ctx.text_extents(sub_text)
    ctx.move_to((W2 - ext2.width) / 2, HEADER_H2 - 8 * SCALE)
    ctx.set_source_rgb(*_c((120, 80, 40)))
    ctx.show_text(sub_text)

    for idx, (expr_name, bg_col) in enumerate(EXPRESSIONS):
        col = idx % COLS
        row = idx // COLS

        px = PAD2 + col * (PW2 + PAD2)
        py = HEADER_H2 + PAD2 + row * (PH2 + LABEL_H2 + PAD2)

        # Panel background
        ctx.rectangle(px, py, PW2, PH2)
        set_color(ctx, bg_col)
        ctx.fill()

        panel_cx = px + PW2 // 2
        panel_cy = py + PH2 // 2
        expr_key = expr_name.lower()

        draw_expression_cairo(ctx, panel_cx, panel_cy, PW2, PH2, expr=expr_key)

        # Panel border
        ctx.rectangle(px, py, PW2, PH2)
        set_color(ctx, (40, 30, 50))
        ctx.set_line_width(1)
        ctx.stroke()

        # Label
        label_y = py + PH2 + 4 * SCALE
        ctx.set_font_size(10 * SCALE)
        ext = ctx.text_extents(expr_name)
        ctx.move_to(px + (PW2 - ext.width) / 2, label_y + ext.height)
        ctx.set_source_rgb(*_c(CORRUPT_AMB))
        ctx.show_text(expr_name)

    # Convert to PIL, downscale with LANCZOS
    img = to_pil_image(surface)
    img_out = img.resize((CANVAS_W_1X, CANVAS_H_1X), Image.LANCZOS)
    return img_out


def main():
    out_dir = str(output_dir('characters', 'main'))
    os.makedirs(out_dir, exist_ok=True)

    sheet = build_sheet()
    out_path = os.path.join(out_dir, "LTG_CHAR_glitch_expression_sheet.png")
    sheet.save(out_path)
    w, h = sheet.size
    print(f"Saved: {out_path}  ({w}x{h}px)")
    print("  Expressions: NEUTRAL, MISCHIEVOUS, PANICKED, TRIUMPHANT, STUNNED, CALCULATING,")
    print("               YEARNING, COVETOUS, HOLLOW")
    print("  v004 pycairo rebuild (Rin Yamamoto C52)")
    print("  Anti-aliased diamond body, smooth crown spike, bezier crack lines")
    print("  Interior desire states preserved: YEARNING, COVETOUS, HOLLOW")


if __name__ == "__main__":
    main()
