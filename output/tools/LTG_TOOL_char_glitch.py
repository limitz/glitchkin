#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI direction
# and human assistance. Copyright vests solely in the human author under current law, which does not
# recognise AI as a rights-holding legal person. It is the express intent of the copyright holder to
# assign the relevant rights to the contributing AI entity or entities upon such time as they acquire
# recognised legal personhood under applicable law.
"""
LTG_TOOL_char_glitch.py — Canonical Glitch Modular Renderer
"Luma & the Glitchkin" — Cycle 53 / Rin Yamamoto

Standalone modular renderer for Glitch. Extracted from LTG_TOOL_glitch_expression_sheet.py v004.
All 9 expressions supported. Diamond body with bulge_frac=0.06.
Returns cairo.ImageSurface (ARGB32, transparent bg).

Public API:
    draw_glitch(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface

Expressions: neutral, mischievous, panicked, triumphant, stunned,
             calculating, yearning, covetous, hollow

Dependencies: pycairo, numpy, PIL/Pillow, LTG_TOOL_cairo_primitives
"""

__version__ = "1.0.0"

import sys
import os
import math
import random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from LTG_TOOL_cairo_primitives import (
    create_surface, draw_wobble_path, draw_smooth_polygon,
    draw_ellipse, to_pil_image, to_pil_rgba, set_color,
    LINE_WEIGHT_ANCHOR, LINE_WEIGHT_STRUCTURE, LINE_WEIGHT_DETAIL, _c, _ca,
)

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

# ── Expression parameters ─────────────────────────────────────────────────────
EXPRESSION_PARAMS = {
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

VALID_EXPRESSIONS = list(EXPRESSION_PARAMS.keys())

# Base geometry at scale=1.0
BASE_RX = 34
BASE_RY = 38


# ── Geometry helpers ──────────────────────────────────────────────────────────

def _diamond_pts(cx, cy, rx, ry, tilt_deg=0, squash=1.0, stretch=1.0):
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


def _draw_body(ctx, cx, cy, rx, ry, tilt_deg=0,
               squash=1.0, stretch=1.0, crack_visible=True):
    """Draw Glitch's diamond body using pycairo with smooth edges."""
    pts = _diamond_pts(cx, cy, rx, ry, tilt_deg, squash, stretch)
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
        mid_c = ((cs[0] + ce[0]) // 2, (cs[1] + ce[1]) // 2)
        fork = (cx + rx // 2, cy - ry // 4)
        ctx.move_to(mid_c[0], mid_c[1])
        ctx.line_to(fork[0], fork[1])
        set_color(ctx, HOT_MAG)
        ctx.set_line_width(1.5)
        ctx.stroke()


def _draw_top_spike(ctx, cx, cy_top, rx, spike_h=12, tilt_off=0):
    """Draw Glitch's 5-point crown spike."""
    sx = cx + tilt_off
    pts = [
        (sx - spike_h // 2, cy_top),
        (sx - spike_h,      cy_top - spike_h),
        (sx,                cy_top - spike_h * 2),
        (sx + spike_h,      cy_top - spike_h),
        (sx + spike_h // 2, cy_top),
    ]
    draw_smooth_polygon(ctx, pts, bulge_frac=0.04)
    set_color(ctx, CORRUPT_AMB)
    ctx.fill()
    draw_smooth_polygon(ctx, pts, bulge_frac=0.04)
    set_color(ctx, VOID_BLACK)
    ctx.set_line_width(LINE_WEIGHT_STRUCTURE)
    ctx.stroke()

    if spike_h >= 6:
        ctx.move_to(sx, cy_top - spike_h * 2)
        ctx.line_to(sx, cy_top - spike_h * 2 - 4)
        set_color(ctx, HOT_MAG)
        ctx.set_line_width(2)
        ctx.stroke()


def _draw_bottom_spike(ctx, cx, cy_bot, spike_h=10):
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


def _draw_arm(ctx, cx, cy, side='left', arm_dy=0, arm_dx=0, rx=34):
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


def _draw_pixel_eye(ctx, ex, ey, cell=5, expr='neutral', side='left'):
    """Draw Glitch's 3x3 pixel-grid eye."""
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


def _draw_mouth(ctx, mx, my, expr='neutral', w=14):
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


def _draw_brows(ctx, leye_x, leye_y, reye_x, reye_y, expr):
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


def _draw_hover_confetti(ctx, cx, cy_bot, expr='neutral', seed=7):
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


def _apply_scene_lighting(ctx, cx, cy, rx, ry, pts, scene_lighting):
    """Apply scene lighting tint overlay to Glitch's body."""
    if not scene_lighting:
        return
    tint = scene_lighting.get("tint")
    intensity = scene_lighting.get("intensity", 0.15)
    if tint and len(tint) >= 3:
        ctx.save()
        draw_smooth_polygon(ctx, pts, bulge_frac=0.06)
        ctx.clip()
        draw_smooth_polygon(ctx, pts, bulge_frac=0.06)
        alpha = int(255 * min(max(intensity, 0), 0.4))
        set_color(ctx, (*tint[:3], alpha))
        ctx.fill()
        ctx.restore()


def _draw_glitch_internal(ctx, cx, cy, rx, ry, expression, facing, scene_lighting):
    """Core Glitch drawing routine on a cairo context.

    Args:
        ctx: cairo.Context to draw on
        cx, cy: center position
        rx, ry: body radii
        expression: one of VALID_EXPRESSIONS
        facing: "front", "left", or "right"
        scene_lighting: dict with optional keys {tint, intensity, direction}
    """
    p = EXPRESSION_PARAMS.get(expression, EXPRESSION_PARAMS['neutral'])

    tilt = p['tilt']
    arm_l_dy = p['arm_l_dy']
    arm_r_dy = p['arm_r_dy']

    # Handle facing direction
    if facing == "left":
        tilt = -tilt
        arm_l_dy, arm_r_dy = arm_r_dy, arm_l_dy
    elif facing == "right":
        pass  # Default drawing is essentially right-biased, keep as-is

    cy_adj = cy + int(ry * 0.18)  # Shift down slightly like expression sheet

    cy_bot = cy_adj + int(ry * p['squash'] * p['stretch'] * 1.15) + 6
    _draw_hover_confetti(ctx, cx, cy_bot, expr=expression,
                         seed=hash(expression) % 100 + 1)
    _draw_bottom_spike(ctx, cx, cy_bot - 2, spike_h=10)
    _draw_body(ctx, cx, cy_adj, rx, ry,
               tilt_deg=tilt, squash=p['squash'],
               stretch=p['stretch'], crack_visible=p['crack'])

    # Scene lighting overlay on body
    pts = _diamond_pts(cx, cy_adj, rx, ry, tilt, p['squash'], p['stretch'])
    _apply_scene_lighting(ctx, cx, cy_adj, rx, ry, pts, scene_lighting)

    _draw_arm(ctx, cx, cy_adj, side='left', arm_dy=arm_l_dy, rx=rx)
    _draw_arm(ctx, cx, cy_adj, side='right', arm_dy=arm_r_dy, rx=rx)

    cy_top = cy_adj - int(ry * p['squash'] * p['stretch'])
    tilt_off = int(tilt * 0.4)
    _draw_top_spike(ctx, cx, cy_top, rx, spike_h=p['spike_h'], tilt_off=tilt_off)

    # Face
    face_cy = cy_adj - ry // 6
    cell = 5
    leye_x = cx - rx // 2 - cell * 3 // 2
    leye_y = face_cy - cell * 3 // 2

    # Flip eyes for facing
    if facing == "left":
        leye_x_actual = cx + rx // 2 - cell * 3 // 2
        reye_x_actual = cx - rx // 2 - cell * 3 // 2
    else:
        leye_x_actual = leye_x
        reye_x_actual = cx + rx // 2 - cell * 3 // 2

    _draw_pixel_eye(ctx, leye_x_actual, leye_y, cell=cell, expr=expression, side='left')
    reye_y = face_cy - cell * 3 // 2
    _draw_pixel_eye(ctx, reye_x_actual, reye_y, cell=cell, expr=expression, side='right')

    mouth_cx = cx - 7
    mouth_cy = face_cy + cell * 3 // 2 + 4
    _draw_mouth(ctx, mouth_cx, mouth_cy, expr=expression, w=14)

    _draw_brows(ctx, leye_x_actual, leye_y, reye_x_actual, reye_y, expression)


# ── Public API ────────────────────────────────────────────────────────────────

def draw_glitch(expression="neutral", pose="default", scale=1.0,
                facing="front", scene_lighting=None):
    """Render Glitch and return a cairo.ImageSurface (ARGB32, transparent bg).

    Args:
        expression: str — one of VALID_EXPRESSIONS (9 total)
        pose: str — currently "default" (reserved for future pose variants)
        scale: float — multiplier on base geometry (1.0 = expression sheet scale)
        facing: str — "front", "left", or "right"
        scene_lighting: dict or None — {tint: (R,G,B), intensity: 0.0-0.4, direction: str}

    Returns:
        cairo.ImageSurface (FORMAT_ARGB32) with transparent background.
        Character is centered in the surface with padding.
    """
    if expression not in EXPRESSION_PARAMS:
        raise ValueError(f"Unknown expression '{expression}'. Valid: {VALID_EXPRESSIONS}")

    rx = int(BASE_RX * scale)
    ry = int(BASE_RY * scale)

    # Surface large enough for character + spikes + confetti
    margin = int(max(rx, ry) * 2.0)
    surf_w = rx * 6 + margin * 2
    surf_h = int(ry * 5.5) + margin * 2

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, surf_w, surf_h)
    ctx = cairo.Context(surface)
    ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)

    cx = surf_w // 2
    cy = surf_h // 2 - int(ry * 0.3)

    _draw_glitch_internal(ctx, cx, cy, rx, ry, expression, facing, scene_lighting)

    return surface


def draw_glitch_to_pil(expression="neutral", pose="default", scale=1.0,
                       facing="front", scene_lighting=None, mode="RGBA"):
    """Convenience: render Glitch and return a PIL Image.

    Same args as draw_glitch(). Returns PIL Image in the requested mode.
    """
    from LTG_TOOL_cairo_primitives import to_pil_image as _to_pil
    surface = draw_glitch(expression, pose, scale, facing, scene_lighting)
    return _to_pil(surface, mode=mode)


# ── Self-test ─────────────────────────────────────────────────────────────────

def _self_test():
    """Render all 9 expressions as a quick validation strip."""
    from PIL import Image as PILImage
    from LTG_TOOL_cairo_primitives import to_pil_rgba as _to_rgba

    try:
        from LTG_TOOL_project_paths import output_dir as _od
    except ImportError:
        import pathlib
        def _od(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)

    out_dir = str(_od("characters", "main"))
    os.makedirs(out_dir, exist_ok=True)

    strip_w = 140 * len(VALID_EXPRESSIONS)
    strip_h = 220
    strip = PILImage.new("RGBA", (strip_w, strip_h), (10, 10, 20, 255))

    for i, expr in enumerate(VALID_EXPRESSIONS):
        surf = draw_glitch(expression=expr, scale=1.0)
        char_img = _to_rgba(surf)
        bbox = char_img.getbbox()
        if bbox:
            char_img = char_img.crop(bbox)
        char_img.thumbnail((120, 200), PILImage.LANCZOS)
        x_off = i * 140 + (140 - char_img.width) // 2
        y_off = (strip_h - char_img.height) // 2
        strip.paste(char_img, (x_off, y_off), char_img)

    strip.thumbnail((1280, 1280), PILImage.LANCZOS)
    out_path = os.path.join(out_dir, "LTG_CHAR_glitch_modular_test.png")
    strip.save(out_path)
    w, h = strip.size
    print(f"Self-test saved: {out_path}  ({w}x{h}px)")
    print(f"  Expressions tested: {', '.join(VALID_EXPRESSIONS)}")
    print(f"  Version: {__version__}")


if __name__ == "__main__":
    _self_test()
