#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI direction
# and human assistance. Copyright vests solely in the human author under current law, which does not
# recognise AI as a rights-holding legal person. It is the express intent of the copyright holder to
# assign the relevant rights to the contributing AI entity or entities upon such time as they acquire
# recognised legal personhood under applicable law.
"""
LTG_TOOL_char_byte.py — Canonical Byte Modular Renderer
"Luma & the Glitchkin" — Cycle 53 / Rin Yamamoto

Standalone modular renderer for Byte. Extracted from LTG_TOOL_byte_expression_sheet.py v008.
All 10 expressions supported. Returns cairo.ImageSurface (ARGB32, transparent bg).

Public API:
    draw_byte(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface

Expressions: neutral, grumpy, searching, alarmed, reluctant_joy, confused,
             powered_down, resigned, storm_cracked, unguarded_warmth

Dependencies: pycairo, numpy, PIL/Pillow, LTG_TOOL_cairo_primitives
"""

__version__ = "1.0.0"

import sys
import os
import math
import random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from LTG_TOOL_cairo_primitives import (
    create_surface, draw_wobble_path, draw_ellipse,
    to_pil_image, to_pil_rgba, set_color,
    LINE_WEIGHT_ANCHOR, LINE_WEIGHT_STRUCTURE, LINE_WEIGHT_DETAIL, _c, _ca,
)

import cairo
import numpy as np

# ── Palette ────────────────────────────────────────────────────────────────────
BYTE_TEAL  = (0, 212, 232)
BYTE_HL    = (0, 240, 255)
BYTE_SH    = (0, 168, 192)
HOT_MAG    = (255, 45, 120)
SCAR_MAG   = (255, 45, 107)
UV_PURPLE  = (123, 47, 190)
SOFT_GOLD  = (232, 201, 90)
LINE       = (10, 10, 20)
EYE_W      = (240, 240, 245)
VOID_BLACK = (10, 10, 20)

# ── Expression spec table ─────────────────────────────────────────────────────
# Maps expression name -> (cracked_symbol, emotion, body_data, right_eye_style)
EXPRESSION_SPECS = {
    "neutral": (
        "flat", "default",
        {"arm_dy": 4, "arm_x_scale": 0.75, "leg_spread": 0.85,
         "body_tilt": 0, "body_squash": 1.0, "arm_l_dy": 4, "arm_r_dy": 4},
        "half_open"),
    "grumpy": (
        "grumpy", "disgust",
        {"arm_dy": -8, "arm_x_scale": 1.1, "leg_spread": 1.1,
         "body_tilt": -8, "body_squash": 1.0, "arm_l_dy": -6, "arm_r_dy": -10},
        "angry"),
    "searching": (
        "loading", "curious",
        {"arm_dy": -4, "arm_x_scale": 1.1, "leg_spread": 1.2,
         "body_tilt": -8, "body_squash": 1.0, "arm_l_dy": 4, "arm_r_dy": -18},
        "wide"),
    "alarmed": (
        "!", "fear",
        {"arm_dy": -16, "arm_x_scale": 2.0, "leg_spread": 1.6,
         "body_tilt": 0, "body_squash": 0.92, "arm_l_dy": -18, "arm_r_dy": -28},
        "wide_scared"),
    "reluctant_joy": (
        "♥", "happy",
        {"arm_dy": 8, "arm_x_scale": 0.65, "leg_spread": 0.8,
         "body_tilt": 12, "body_squash": 1.0, "arm_l_dy": -12, "arm_r_dy": 18,
         "reluctant_joy": True},
        "droopy"),
    "confused": (
        "?", "confused",
        {"arm_dy": -6, "arm_x_scale": 1.0, "leg_spread": 1.1,
         "body_tilt": -18, "body_squash": 1.0, "arm_l_dy": -14, "arm_r_dy": 2},
        "squint"),
    "powered_down": (
        "flat", "neutral",
        {"arm_dy": 26, "arm_x_scale": 0.20, "leg_spread": 0.6,
         "body_tilt": 0, "body_squash": 0.88, "arm_l_dy": 26, "arm_r_dy": 26},
        "flat"),
    "resigned": (
        "↓", "resigned",
        {"arm_dy": 24, "arm_x_scale": 0.25, "leg_spread": 0.70,
         "body_tilt": 14, "body_squash": 1.0, "arm_l_dy": 24, "arm_r_dy": 24},
        "droopy_resigned"),
    "storm_cracked": (
        "dead_zone", "storm",
        {"arm_dy": 10, "arm_x_scale": 0.55, "leg_spread": 0.72,
         "body_tilt": 18, "body_squash": 1.0, "arm_l_dy": 6, "arm_r_dy": 22,
         "storm_damage": True},
        "cracked_storm"),
    "unguarded_warmth": (
        "heart_purple", "warmth",
        {"arm_dy": -14, "arm_x_scale": 1.0, "leg_spread": 0.85,
         "body_tilt": -4, "body_squash": 1.0,
         "arm_l_dy": -14, "arm_r_dy": -16, "float_offset": -4,
         "lower_l_angle": 8, "lower_r_angle": 8,
         "unguarded_warmth": True},
        "star_gold"),
}

VALID_EXPRESSIONS = list(EXPRESSION_SPECS.keys())


# ── Internal drawing helpers ──────────────────────────────────────────────────

def _cairo_ellipse_path(ctx, cx, cy, rx, ry):
    """Add an ellipse path to the context."""
    ctx.save()
    ctx.translate(cx, cy)
    if rx != 0 and ry != 0:
        ctx.scale(rx, ry)
    ctx.arc(0, 0, 1.0, 0, 2 * math.pi)
    ctx.restore()


def _draw_pixel_grid(ctx, ox, oy, grid, cell, color_map):
    """Draw a pixel grid on cairo context."""
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            v = grid[row][col]
            color = color_map.get(v, VOID_BLACK)
            px = ox + col * cell
            py = oy + row * cell
            ctx.rectangle(px + 0.5, py + 0.5, cell - 1, cell - 1)
            set_color(ctx, color)
            ctx.fill()


def _draw_pixel_symbol(ctx, cx, cy, size, symbol):
    """Draw a pixel-eye symbol on cairo context."""
    if symbol == "dead_zone":
        cell = max(2, size // 7)
        ox = cx - (7 * cell) // 2
        oy = cy - (7 * cell) // 2
        DEAD_PX = (10, 10, 20)
        DIM_PX = (0, 80, 100)
        ALIVE_PX = (0, 180, 200)
        BRIGHT_PX = (200, 255, 255)
        DEEP_CYAN_BG = (26, 58, 64)
        glyph = [
            [3, 3, 3, 3, 0, 0, 0],
            [3, 1, 3, 3, 0, 0, 0],
            [1, 3, 3, 0, 0, 2, 0],
            [3, 3, 0, 0, 2, 0, 0],
            [3, 0, 0, 3, 3, 0, 3],
            [0, 0, 3, 1, 3, 3, 3],
            [0, 3, 3, 3, 1, 3, 3],
        ]
        color_map = {0: DEAD_PX, 1: ALIVE_PX, 2: BRIGHT_PX, 3: DIM_PX}
        ctx.rectangle(ox - 2, oy - 2, 7 * cell + 4, 7 * cell + 4)
        set_color(ctx, DEEP_CYAN_BG)
        ctx.fill_preserve()
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
        _draw_pixel_grid(ctx, ox, oy, glyph, cell, color_map)
        ctx.move_to(ox + 4.5 * cell, oy)
        ctx.line_to(ox + 2.0 * cell, oy + 7 * cell)
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
        return

    # Standard 5x5 symbols
    cell = size // 5
    if cell < 2:
        cell = 2
    ox = cx - (5 * cell) // 2
    oy = cy - (5 * cell) // 2

    grids = {
        "star_gold": ([
            [0, 1, 0, 1, 0], [1, 1, 1, 1, 1], [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1], [0, 1, 0, 1, 0]], SOFT_GOLD),
        "heart_purple": ([
            [0, 1, 0, 1, 0], [1, 1, 1, 1, 1], [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]], UV_PURPLE),
        "!": ([
            [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0], [0, 0, 1, 0, 0]], (0, 240, 255)),
        "?": ([
            [0, 1, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0], [0, 0, 1, 0, 0]], (0, 240, 255)),
        "♥": ([
            [0, 1, 0, 1, 0], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0], [0, 0, 1, 0, 0]], (0, 240, 255)),
        "loading": ([
            [1, 0, 1, 0, 1], [0, 0, 0, 0, 0], [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0], [1, 0, 1, 0, 1]], (0, 240, 255)),
        "flat": ([
            [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], (0, 240, 255)),
        "grumpy": ([
            [0, 0, 0, 0, 0], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1], [0, 0, 0, 0, 0]], (0, 240, 255)),
        "↓": ([
            [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0], [0, 0, 1, 0, 0]], (0, 240, 255)),
    }

    if symbol in grids:
        grid, sym_color = grids[symbol]
    else:
        return

    bg_color = (40, 32, 20) if sym_color == SOFT_GOLD else (255, 255, 255)
    ctx.rectangle(ox - 2, oy - 2, 5 * cell + 4, 5 * cell + 4)
    set_color(ctx, bg_color)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(1)
    ctx.stroke()

    off_color = (10, 8, 20)
    color_map = {1: sym_color, 0: off_color}
    _draw_pixel_grid(ctx, ox, oy, grid, cell, color_map)


def _draw_right_eye(ctx, cx, cy, size, style):
    """Draw Byte's right (organic) eye or special symbols."""
    cell = size // 5
    if cell < 2:
        cell = 2

    if style in ("star_gold", "flat"):
        _draw_pixel_symbol(ctx, cx, cy, size, style)
        return

    ew = cell * 2
    eh = cell * 2

    def _eye_base(cx, cy, ew, eh_top, fill_c, ol_c=None, ol_w=1):
        _cairo_ellipse_path(ctx, cx, cy, ew, eh_top)
        set_color(ctx, fill_c)
        ctx.fill()
        if ol_c:
            _cairo_ellipse_path(ctx, cx, cy, ew, eh_top)
            set_color(ctx, ol_c)
            ctx.set_line_width(ol_w)
            ctx.stroke()

    if style == "half_open":
        eye_h = int(eh * 0.6)
        _eye_base(cx, cy, ew, eye_h, EYE_W, LINE, 1)
        _cairo_ellipse_path(ctx, cx, cy, int(cell * 1.5), int(cell * 1.5))
        set_color(ctx, (45, 28, 14))
        ctx.fill()
        _cairo_ellipse_path(ctx, cx, cy, cell // 2 + 1, cell // 2 + 1)
        set_color(ctx, LINE)
        ctx.fill()
        _cairo_ellipse_path(ctx, cx + cell, cy - cell // 2, cell // 2, cell // 3)
        set_color(ctx, (200, 195, 185))
        ctx.fill()
        ctx.arc(cx, cy, ew, math.radians(200), math.radians(340))
        set_color(ctx, LINE)
        ctx.set_line_width(3)
        ctx.stroke()

    elif style == "wide":
        _eye_base(cx, cy, ew, eh, EYE_W)
        _cairo_ellipse_path(ctx, cx + 2, cy + 2, cell, cell)
        set_color(ctx, (60, 38, 20))
        ctx.fill()
        _cairo_ellipse_path(ctx, cx + 2, cy + 2, cell // 2, cell // 2)
        set_color(ctx, LINE)
        ctx.fill()
        _cairo_ellipse_path(ctx, cx + cell, cy - eh + cell, cell // 2, cell // 3)
        set_color(ctx, (255, 252, 245))
        ctx.fill()

    elif style == "wide_scared":
        _eye_base(cx, cy, ew + 2, eh + 3, EYE_W, LINE, 2)
        _cairo_ellipse_path(ctx, cx, cy, cell - 1, cell - 1)
        set_color(ctx, (60, 38, 20))
        ctx.fill()
        _cairo_ellipse_path(ctx, cx, cy, 4, 4)
        set_color(ctx, LINE)
        ctx.fill()
        _cairo_ellipse_path(ctx, cx + cell, cy - eh + cell, cell // 2, cell // 3)
        set_color(ctx, (255, 252, 245))
        ctx.fill()

    elif style == "angry":
        eye_h = eh - 2
        _eye_base(cx, cy + 2, ew, eye_h, EYE_W)
        _cairo_ellipse_path(ctx, cx - 2, cy + cell // 2, cell, cell)
        set_color(ctx, (60, 38, 20))
        ctx.fill()
        _cairo_ellipse_path(ctx, cx - 2, cy + cell // 2 + 2, 4, 4)
        set_color(ctx, LINE)
        ctx.fill()
        ctx.move_to(cx - ew, cy - eh // 2 + 4)
        ctx.line_to(cx + ew, cy - eh // 2)
        set_color(ctx, LINE)
        ctx.set_line_width(3)
        ctx.stroke()

    elif style == "droopy":
        _eye_base(cx, cy + 3, ew, eh - 2, EYE_W)
        _cairo_ellipse_path(ctx, cx + 1, cy + 2, cell, cell)
        set_color(ctx, (60, 38, 20))
        ctx.fill()
        _cairo_ellipse_path(ctx, cx + 1, cy + 3, 4, 4)
        set_color(ctx, LINE)
        ctx.fill()
        ctx.save()
        ctx.arc(cx, cy + 3, ew, math.radians(195), math.radians(345))
        set_color(ctx, LINE)
        ctx.set_line_width(6)
        ctx.stroke()
        ctx.restore()

    elif style == "droopy_resigned":
        eye_h = int(eh * 0.45)
        _eye_base(cx, cy + 6, ew, eye_h, EYE_W)
        _cairo_ellipse_path(ctx, cx + 1, cy + 8, cell, cell)
        set_color(ctx, (60, 38, 20))
        ctx.fill()
        _cairo_ellipse_path(ctx, cx + 1, cy + 10, 4, 4)
        set_color(ctx, LINE)
        ctx.fill()
        ctx.arc(cx, cy + 6, ew, math.radians(195), math.radians(345))
        set_color(ctx, LINE)
        ctx.set_line_width(8)
        ctx.stroke()

    elif style == "cracked_storm":
        eye_h = int(eh * 0.50)
        _eye_base(cx, cy + 4, ew, eye_h, EYE_W)
        _cairo_ellipse_path(ctx, cx + 1, cy + 6, cell, cell)
        set_color(ctx, (35, 22, 10))
        ctx.fill()
        _cairo_ellipse_path(ctx, cx + 1, cy + 8, 4, 4)
        set_color(ctx, LINE)
        ctx.fill()
        ctx.arc(cx, cy + 4, ew, math.radians(195), math.radians(345))
        set_color(ctx, LINE)
        ctx.set_line_width(8)
        ctx.stroke()

    elif style == "squint":
        _eye_base(cx, cy, ew, eh - 3, EYE_W)
        _cairo_ellipse_path(ctx, cx, cy - 2, cell, cell)
        set_color(ctx, (60, 38, 20))
        ctx.fill()
        _cairo_ellipse_path(ctx, cx, cy - 4, 4, 4)
        set_color(ctx, LINE)
        ctx.fill()
        ctx.move_to(cx - ew, cy - eh // 2 + 4)
        ctx.line_to(cx + ew, cy - eh // 2 + 2)
        set_color(ctx, LINE)
        ctx.set_line_width(3)
        ctx.stroke()

    else:
        _eye_base(cx, cy, ew, eh, EYE_W)
        _cairo_ellipse_path(ctx, cx, cy, cell, cell)
        set_color(ctx, (60, 38, 20))
        ctx.fill()
        _cairo_ellipse_path(ctx, cx, cy, cell // 2, cell // 2)
        set_color(ctx, LINE)
        ctx.fill()


def _draw_rounded_limb(ctx, x, y, w, h, fill_c, outline_c):
    """Draw a limb with rounded tip."""
    r = min(w, h) // 3
    ctx.new_path()
    ctx.move_to(x, y)
    ctx.line_to(x + w, y)
    ctx.line_to(x + w, y + h - r)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.line_to(x + r, y + h)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.close_path()
    set_color(ctx, fill_c)
    ctx.fill_preserve()
    set_color(ctx, outline_c)
    ctx.set_line_width(2)
    ctx.stroke()


def _apply_scene_lighting(ctx, bcx, bcy, body_rx, body_ry, scene_lighting):
    """Apply scene lighting tint overlay to Byte's body."""
    if not scene_lighting:
        return
    tint = scene_lighting.get("tint")
    intensity = scene_lighting.get("intensity", 0.15)
    if tint and len(tint) >= 3:
        ctx.save()
        _cairo_ellipse_path(ctx, bcx, bcy, body_rx, body_ry)
        ctx.clip()
        _cairo_ellipse_path(ctx, bcx, bcy, body_rx, body_ry)
        alpha = int(255 * min(max(intensity, 0), 0.4))
        set_color(ctx, (*tint[:3], alpha))
        ctx.fill()
        ctx.restore()


def _draw_byte_internal(ctx, cx, cy, size, expression, facing, scene_lighting):
    """Core Byte drawing routine on a cairo context.

    Args:
        ctx: cairo.Context to draw on
        cx, cy: center position
        size: base size in pixels (88 = expression sheet scale)
        expression: one of VALID_EXPRESSIONS
        facing: "front" (default), "left", or "right"
        scene_lighting: dict with optional keys {tint, intensity, direction}
    """
    spec = EXPRESSION_SPECS.get(expression, EXPRESSION_SPECS["neutral"])
    cracked_symbol, emotion, body_data, right_eye_style = spec

    s = size
    arm_dy = body_data.get("arm_dy", 0)
    arm_x_scale = body_data.get("arm_x_scale", 1.0)
    leg_spread = body_data.get("leg_spread", 1.0)
    body_tilt = body_data.get("body_tilt", 0)
    body_squash = body_data.get("body_squash", 1.0)
    arm_l_dy = body_data.get("arm_l_dy", arm_dy)
    arm_r_dy = body_data.get("arm_r_dy", arm_dy)
    storm_damage = body_data.get("storm_damage", False)
    unguarded_warmth = body_data.get("unguarded_warmth", False)
    float_offset = body_data.get("float_offset", 0)
    cy = cy + float_offset
    lower_l_angle = body_data.get("lower_l_angle", 0)
    lower_r_angle = body_data.get("lower_r_angle", 0)

    # Handle facing direction (flip tilt and arm assignments)
    flip = 1
    if facing == "left":
        flip = -1
        body_tilt = -body_tilt
        arm_l_dy, arm_r_dy = arm_r_dy, arm_l_dy
        lower_l_angle, lower_r_angle = lower_r_angle, lower_l_angle

    body_rx = s // 2
    body_ry = int(s * 0.55 * body_squash)
    bcx = cx + body_tilt
    bcy = cy

    # Body fill
    _cairo_ellipse_path(ctx, bcx, bcy, body_rx, body_ry)
    set_color(ctx, BYTE_TEAL)
    ctx.fill()

    # Right-side shadow (clipped to ellipse)
    ctx.save()
    _cairo_ellipse_path(ctx, bcx, bcy, body_rx, body_ry)
    ctx.clip()
    shadow_side = bcx if flip == 1 else bcx - body_rx - 2
    ctx.rectangle(shadow_side, bcy - body_ry, body_rx + 2, body_ry * 2 + 2)
    set_color(ctx, BYTE_SH)
    ctx.fill()
    ctx.restore()

    # Highlight arc (upper-left or upper-right depending on facing)
    ctx.save()
    _cairo_ellipse_path(ctx, bcx, bcy, body_rx, body_ry)
    ctx.clip()
    hl_off = -body_rx // 3 * flip
    _cairo_ellipse_path(ctx, bcx + hl_off, bcy - body_ry // 3,
                        body_rx - 4, body_ry - 4)
    set_color(ctx, BYTE_HL)
    ctx.set_line_width(3)
    ctx.stroke()
    ctx.restore()

    # Outline with wobble
    body_pts = []
    for i in range(64):
        t = i / 64.0 * 2 * math.pi
        bx = bcx + body_rx * math.cos(t)
        by = bcy + body_ry * math.sin(t)
        body_pts.append((bx, by))
    draw_wobble_path(ctx, body_pts, amplitude=0.8, frequency=0.12,
                     seed=42 + hash(expression) % 100)
    set_color(ctx, LINE)
    ctx.set_line_width(LINE_WEIGHT_ANCHOR)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.stroke()

    # Magenta scar markings
    crack_x = bcx - s // 4 * flip
    ctx.move_to(crack_x, bcy - body_ry // 2)
    ctx.line_to(crack_x + s // 8 * flip, bcy - body_ry // 6)
    set_color(ctx, SCAR_MAG)
    ctx.set_line_width(2.5)
    ctx.stroke()
    ctx.move_to(crack_x + s // 8 * flip, bcy - body_ry // 6)
    ctx.line_to(crack_x - s // 10 * flip, bcy + body_ry // 6)
    set_color(ctx, SCAR_MAG)
    ctx.set_line_width(2.5)
    ctx.stroke()

    # Damage notch
    notch_side = bcx + (body_rx - 4) * flip
    ctx.move_to(notch_side, bcy - body_ry // 4)
    ctx.line_to(notch_side + s // 12 * flip, bcy - body_ry // 6)
    ctx.line_to(notch_side, bcy + body_ry // 6)
    ctx.close_path()
    set_color(ctx, (0, 0, 0, 0))
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(1)
    ctx.stroke()

    # Storm damage marks
    if storm_damage:
        sx = bcx + s // 6 * flip
        sy = bcy - body_ry + 10
        ctx.move_to(sx, sy)
        ctx.line_to(sx + 8 * flip, sy + 12)
        set_color(ctx, HOT_MAG)
        ctx.set_line_width(2)
        ctx.stroke()
        ctx.move_to(sx + 8 * flip, sy + 12)
        ctx.line_to(sx + 4 * flip, sy + 18)
        set_color(ctx, HOT_MAG)
        ctx.set_line_width(2)
        ctx.stroke()

    # Unguarded warmth gold glow
    if unguarded_warmth:
        ctx.save()
        _cairo_ellipse_path(ctx, bcx, bcy, body_rx, body_ry)
        ctx.clip()
        _cairo_ellipse_path(ctx, bcx + body_rx // 3 * flip, bcy,
                            body_rx - 6, body_ry - 4)
        set_color(ctx, (*SOFT_GOLD, 60))
        ctx.set_line_width(3)
        ctx.stroke()
        ctx.restore()

    # Scene lighting overlay
    _apply_scene_lighting(ctx, bcx, bcy, body_rx, body_ry, scene_lighting)

    # Eyes
    eye_y = bcy - body_ry // 5
    eye_size = max(14, int(body_ry * 0.46))

    # Left eye (pixel/cracked) — flips with facing
    lx = bcx - s // 5 * flip
    crack_frame_sz = eye_size + 4

    if storm_damage:
        fr = crack_frame_sz // 2
        ctx.move_to(lx - fr, eye_y - fr)
        ctx.line_to(lx + fr - 2, eye_y - fr)
        ctx.line_to(lx + fr, eye_y - fr + 3)
        ctx.line_to(lx + fr + 2, eye_y - fr + 8)
        ctx.line_to(lx + fr, eye_y + fr)
        ctx.line_to(lx - fr, eye_y + fr)
        ctx.close_path()
        set_color(ctx, (26, 58, 64))
        ctx.fill_preserve()
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
        ctx.move_to(lx + fr - 2, eye_y - fr)
        ctx.line_to(lx - fr + 3, eye_y + fr)
        set_color(ctx, HOT_MAG)
        ctx.set_line_width(2)
        ctx.stroke()
    else:
        ctx.rectangle(lx - crack_frame_sz // 2, eye_y - crack_frame_sz // 2,
                      crack_frame_sz, crack_frame_sz)
        set_color(ctx, (255, 255, 255))
        ctx.fill_preserve()
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
        ctx.move_to(lx + 2, eye_y - crack_frame_sz // 2)
        ctx.line_to(lx - 4, eye_y + crack_frame_sz // 2)
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()

    _draw_pixel_symbol(ctx, lx, eye_y, eye_size, cracked_symbol)

    # Right eye (organic)
    rx_eye = bcx + s // 5 * flip
    _draw_right_eye(ctx, rx_eye, eye_y, eye_size, right_eye_style)

    # Mouth
    mouth_y = bcy + body_ry // 3
    mw = s // 3
    if emotion == "disgust":
        ctx.arc(bcx, mouth_y + 4, mw // 2, math.radians(200), math.radians(340))
        set_color(ctx, LINE)
        ctx.set_line_width(3)
        ctx.stroke()
    elif emotion == "curious":
        _cairo_ellipse_path(ctx, bcx, mouth_y - 2, 8, 6)
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
    elif emotion == "fear":
        _cairo_ellipse_path(ctx, bcx, mouth_y + 4, mw // 2 - 4, 10)
        set_color(ctx, (180, 160, 150))
        ctx.fill_preserve()
        set_color(ctx, LINE)
        ctx.set_line_width(3)
        ctx.stroke()
    elif emotion == "happy":
        ctx.arc(bcx, mouth_y, mw // 3, math.radians(20), math.radians(160))
        set_color(ctx, LINE)
        ctx.set_line_width(3)
        ctx.stroke()
    elif emotion == "confused":
        ctx.move_to(bcx - mw // 2, mouth_y + 4)
        for i in range(4):
            x1 = bcx - mw // 2 + i * (mw // 4)
            y1 = mouth_y + (4 if i % 2 == 0 else -4)
            ctx.line_to(x1 + mw // 4, mouth_y + (-4 if i % 2 == 0 else 4))
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
    elif emotion == "default":
        ctx.move_to(bcx - mw // 2, mouth_y)
        ctx.line_to(bcx + mw // 2, mouth_y)
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
        ctx.move_to(bcx - mw // 2, mouth_y)
        ctx.line_to(bcx - mw // 2 - 6, mouth_y + 4)
        ctx.stroke()
        ctx.move_to(bcx + mw // 2, mouth_y)
        ctx.line_to(bcx + mw // 2 + 6, mouth_y + 4)
        ctx.stroke()
    elif emotion == "resigned":
        ctx.move_to(bcx - mw // 3, mouth_y)
        ctx.line_to(bcx + mw // 3, mouth_y)
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
    elif emotion == "storm":
        ctx.move_to(bcx - mw // 4, mouth_y)
        ctx.line_to(bcx + mw // 4, mouth_y)
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
    elif emotion == "warmth":
        mw_s = mw // 3
        ctx.arc(bcx, mouth_y, mw_s, math.radians(25), math.radians(155))
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
    else:
        ctx.move_to(bcx - mw // 2, mouth_y)
        ctx.line_to(bcx + mw // 2, mouth_y)
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()

    # Antenna
    ant_base_x = bcx - s // 8 * flip
    ant_base_y = bcy - body_ry
    if storm_damage:
        ant_mid_x = ant_base_x + 6 * flip
        ant_mid_y = ant_base_y - s // 5
        ant_tip_x = ant_mid_x - 8 * flip
        ant_tip_y = ant_mid_y - s // 8
        ctx.move_to(ant_base_x, ant_base_y)
        ctx.line_to(ant_mid_x, ant_mid_y)
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
        ctx.move_to(ant_mid_x, ant_mid_y)
        ctx.line_to(ant_tip_x, ant_tip_y)
        ctx.stroke()
        _cairo_ellipse_path(ctx, ant_tip_x, ant_tip_y, 3, 3)
        set_color(ctx, HOT_MAG)
        ctx.fill()
    elif unguarded_warmth:
        ant_tip_x = ant_base_x - s // 10 * flip
        ant_tip_y = ant_base_y - s // 3
        ctx.move_to(ant_base_x, ant_base_y)
        ctx.line_to(ant_tip_x, ant_tip_y)
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
        _cairo_ellipse_path(ctx, ant_tip_x, ant_tip_y, 4, 4)
        set_color(ctx, SOFT_GOLD)
        ctx.fill()
    else:
        ant_tip_x = ant_base_x - s // 10 * flip
        ant_tip_y = ant_base_y - s // 3
        ctx.move_to(ant_base_x, ant_base_y)
        ctx.line_to(ant_tip_x, ant_tip_y)
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
        _cairo_ellipse_path(ctx, ant_tip_x, ant_tip_y, 4, 4)
        set_color(ctx, BYTE_HL)
        ctx.fill()

    # Limbs
    lw = s // 6
    lh = s // 5
    arm_extend = int(lw * arm_x_scale)
    arm_base_y = bcy - body_ry // 5

    # Left arm
    left_arm_y = arm_base_y + arm_l_dy
    _draw_rounded_limb(ctx, bcx - body_rx - arm_extend, left_arm_y,
                       arm_extend, lh, BYTE_TEAL, LINE)

    # Right arm
    right_arm_y = arm_base_y + arm_r_dy
    _draw_rounded_limb(ctx, bcx + body_rx, right_arm_y,
                       arm_extend, lh, BYTE_TEAL, LINE)

    # Legs
    leg_offset = int(s // 4 * leg_spread)
    leg_l_offset = leg_offset + (2 if unguarded_warmth else 0)
    leg_h = lh
    leg_w = int(lw * 0.9)
    leg_top_y = bcy + body_ry

    toe_l = int(leg_h * math.tan(math.radians(lower_l_angle)))
    toe_r = int(leg_h * math.tan(math.radians(lower_r_angle)))

    # Left leg
    if toe_l > 0:
        ctx.move_to(bcx - leg_l_offset - leg_w // 2, leg_top_y)
        ctx.line_to(bcx - leg_l_offset + leg_w // 2, leg_top_y)
        ctx.line_to(bcx - leg_l_offset + leg_w // 2 + toe_l, leg_top_y + leg_h)
        ctx.line_to(bcx - leg_l_offset - leg_w // 2 + toe_l, leg_top_y + leg_h)
        ctx.close_path()
    else:
        ctx.rectangle(bcx - leg_l_offset - leg_w // 2, leg_top_y, leg_w, leg_h)
    set_color(ctx, BYTE_TEAL)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()

    # Right leg
    if toe_r > 0:
        ctx.move_to(bcx + leg_offset - leg_w // 2, leg_top_y)
        ctx.line_to(bcx + leg_offset + leg_w // 2, leg_top_y)
        ctx.line_to(bcx + leg_offset + leg_w // 2 - toe_r, leg_top_y + leg_h)
        ctx.line_to(bcx + leg_offset - leg_w // 2 - toe_r, leg_top_y + leg_h)
        ctx.close_path()
    else:
        ctx.rectangle(bcx + leg_offset - leg_w // 2, leg_top_y, leg_w, leg_h)
    set_color(ctx, BYTE_TEAL)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()

    # Hover particles with bezier trails
    rng = random.Random(hash(expression) % 1000 + 7)
    particle_base_y = bcy + body_ry + leg_h + 3
    if unguarded_warmth:
        positions = [
            (bcx - 18, particle_base_y + 2),
            (bcx + 6, particle_base_y + 6),
            (bcx + 24, particle_base_y),
        ]
        for (ppx, ppy) in positions:
            ctx.rectangle(ppx, ppy, 10, 10)
            set_color(ctx, SOFT_GOLD)
            ctx.fill()
            trail_pts = [(ppx + 5, ppy + 10), (ppx + rng.randint(-8, 8), ppy + 16),
                         (ppx + rng.randint(-6, 6), ppy + 22)]
            if len(trail_pts) >= 2:
                ctx.move_to(trail_pts[0][0], trail_pts[0][1])
                for tp in trail_pts[1:]:
                    ctx.line_to(tp[0], tp[1])
                set_color(ctx, (*SOFT_GOLD, 100))
                ctx.set_line_width(1)
                ctx.stroke()
    else:
        particle_colors = [BYTE_HL, SCAR_MAG, BYTE_HL, (0, 200, 180)]
        for i, ppc in enumerate(particle_colors):
            ppx = bcx + rng.randint(-35, 25)
            ppy = particle_base_y + rng.randint(0, 10)
            ctx.rectangle(ppx, ppy, 10, 10)
            set_color(ctx, ppc)
            ctx.fill()
            trail_pts = [(ppx + 5, ppy + 10),
                         (ppx + 5 + rng.randint(-10, 10), ppy + 18),
                         (ppx + 5 + rng.randint(-8, 8), ppy + 26)]
            ctx.move_to(trail_pts[0][0], trail_pts[0][1])
            ctx.curve_to(trail_pts[0][0], trail_pts[0][1] + 3,
                         trail_pts[1][0], trail_pts[1][1],
                         trail_pts[2][0], trail_pts[2][1])
            set_color(ctx, (*ppc, 80))
            ctx.set_line_width(1)
            ctx.stroke()


# ── Public API ────────────────────────────────────────────────────────────────

def draw_byte(expression="neutral", pose="default", scale=1.0,
              facing="front", scene_lighting=None):
    """Render Byte and return a cairo.ImageSurface (ARGB32, transparent bg).

    Args:
        expression: str — one of VALID_EXPRESSIONS (10 total)
        pose: str — currently "default" (reserved for future pose variants)
        scale: float — multiplier on base 88px size (1.0 = expression sheet scale)
        facing: str — "front", "left", or "right"
        scene_lighting: dict or None — {tint: (R,G,B), intensity: 0.0-0.4, direction: str}

    Returns:
        cairo.ImageSurface (FORMAT_ARGB32) with transparent background.
        Character is centered in the surface with padding.
    """
    if expression not in EXPRESSION_SPECS:
        raise ValueError(f"Unknown expression '{expression}'. Valid: {VALID_EXPRESSIONS}")

    base_size = 88
    size = int(base_size * scale)
    # Surface large enough for character + arms + antenna + particles
    margin = int(size * 0.8)
    surf_w = size * 3 + margin * 2
    surf_h = int(size * 2.8) + margin * 2

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, surf_w, surf_h)
    ctx = cairo.Context(surface)
    ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)

    cx = surf_w // 2
    cy = surf_h // 2 - int(size * 0.15)

    _draw_byte_internal(ctx, cx, cy, size, expression, facing, scene_lighting)

    return surface


def draw_byte_to_pil(expression="neutral", pose="default", scale=1.0,
                     facing="front", scene_lighting=None, mode="RGBA"):
    """Convenience: render Byte and return a PIL Image.

    Same args as draw_byte(). Returns PIL Image in the requested mode.
    """
    from LTG_TOOL_cairo_primitives import to_pil_image as _to_pil
    surface = draw_byte(expression, pose, scale, facing, scene_lighting)
    return _to_pil(surface, mode=mode)


# ── Self-test ─────────────────────────────────────────────────────────────────

def _self_test():
    """Render all 10 expressions as a quick validation strip."""
    from PIL import Image as PILImage
    from LTG_TOOL_cairo_primitives import to_pil_rgba as _to_rgba

    try:
        from LTG_TOOL_project_paths import output_dir as _od
    except ImportError:
        import pathlib
        def _od(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)

    out_dir = str(_od("characters", "main"))
    os.makedirs(out_dir, exist_ok=True)

    strip_w = 200 * len(VALID_EXPRESSIONS)
    strip_h = 280
    strip = PILImage.new("RGBA", (strip_w, strip_h), (20, 18, 28, 255))

    for i, expr in enumerate(VALID_EXPRESSIONS):
        surf = draw_byte(expression=expr, scale=1.0)
        char_img = _to_rgba(surf)
        # Crop to content
        bbox = char_img.getbbox()
        if bbox:
            char_img = char_img.crop(bbox)
        # Fit into 200x280 slot
        char_img.thumbnail((180, 260), PILImage.LANCZOS)
        x_off = i * 200 + (200 - char_img.width) // 2
        y_off = (strip_h - char_img.height) // 2
        strip.paste(char_img, (x_off, y_off), char_img)

    strip.thumbnail((1280, 1280), PILImage.LANCZOS)
    out_path = os.path.join(out_dir, "LTG_CHAR_byte_modular_test.png")
    strip.save(out_path)
    w, h = strip.size
    print(f"Self-test saved: {out_path}  ({w}x{h}px)")
    print(f"  Expressions tested: {', '.join(VALID_EXPRESSIONS)}")
    print(f"  Version: {__version__}")


if __name__ == "__main__":
    _self_test()
