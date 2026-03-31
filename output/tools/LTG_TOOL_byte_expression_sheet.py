#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_byte_expression_sheet.py
Byte Expression Sheet — v008 PYCAIRO REBUILD
"Luma & the Glitchkin" — Cycle 52 / Rin Yamamoto

v008 CHANGES (C52 — pycairo rebuild):
  Complete rebuild using pycairo for anti-aliased rendering.
  All body geometry now uses cairo bezier curves and native AA.
  Preserves all v007 expression specs exactly (10 expressions, 4x3 grid).
  Variable-width outlines via draw_tapered_stroke.
  Pixel confetti with bezier trails.
  Cracked eye with magenta pixel grid.

Output: output/characters/main/LTG_CHAR_byte_expression_sheet.png
"""

import sys
import os
import math
import random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from LTG_TOOL_cairo_primitives import (
    create_surface, draw_bezier_path, draw_tapered_stroke,
    draw_gradient_fill, draw_wobble_path, draw_smooth_polygon,
    draw_ellipse, to_pil_image, to_pil_rgba, set_color,
    stroke_path, fill_background, LINE_WEIGHT_ANCHOR,
    LINE_WEIGHT_STRUCTURE, LINE_WEIGHT_DETAIL, _c, _ca,
    flatten_path
)

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path

from PIL import Image, ImageDraw, ImageFont
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
BG         = (20, 18, 28)
VOID_BLACK = (10, 10, 20)

BG_NEUTRAL  = (28, 34, 42)
BG_GRUMPY   = (38, 20, 28)
BG_SEARCH   = (22, 30, 44)
BG_ALARM    = (18, 28, 44)
BG_RELJOY   = (22, 34, 32)
BG_CONFUSE  = (30, 24, 42)
BG_PWRDOWN  = (14, 12, 18)
BG_RESIGNED = (24, 26, 34)
BG_STORM    = (12, 10, 22)
BG_WARMTH   = (240, 224, 198)

# ── Layout ─────────────────────────────────────────────────────────────────────
PANEL_W = 240
PANEL_H = 320
COLS    = 3
ROWS    = 4
PAD     = 16
HEADER  = 50

# ── Expression definitions ─────────────────────────────────────────────────────
EXPRESSIONS = [
    ("NEUTRAL / DEFAULT", "flat", "default",
     {"arm_dy": 4, "arm_x_scale": 0.75, "leg_spread": 0.85,
      "body_tilt": 0, "body_squash": 1.0, "arm_l_dy": 4, "arm_r_dy": 4},
     "half_open", BG_NEUTRAL, "← was: ANY STATE", "→ next: SEARCHING / GRUMPY"),
    ("GRUMPY", "grumpy", "disgust",
     {"arm_dy": -8, "arm_x_scale": 1.1, "leg_spread": 1.1,
      "body_tilt": -8, "body_squash": 1.0, "arm_l_dy": -6, "arm_r_dy": -10},
     "angry", BG_GRUMPY, "← was: NEUTRAL", "→ next: REFUSING"),
    ("SEARCHING", "loading", "curious",
     {"arm_dy": -4, "arm_x_scale": 1.1, "leg_spread": 1.2,
      "body_tilt": -8, "body_squash": 1.0, "arm_l_dy": 4, "arm_r_dy": -18},
     "wide", BG_SEARCH, "← was: NEUTRAL", "→ next: ALARMED / FOUND"),
    ("ALARMED", "!", "fear",
     {"arm_dy": -16, "arm_x_scale": 2.0, "leg_spread": 1.6,
      "body_tilt": 0, "body_squash": 0.92, "arm_l_dy": -18, "arm_r_dy": -28},
     "wide_scared", BG_ALARM, "← was: SEARCHING", "→ next: FLEEING / FROZEN"),
    ("RELUCTANT JOY", "♥", "happy",
     {"arm_dy": 8, "arm_x_scale": 0.65, "leg_spread": 0.8,
      "body_tilt": 12, "body_squash": 1.0, "arm_l_dy": -12, "arm_r_dy": 18,
      "reluctant_joy": True},
     "droopy", BG_RELJOY, "← was: GRUMPY", "→ next: DENYING IT"),
    ("CONFUSED", "?", "confused",
     {"arm_dy": -6, "arm_x_scale": 1.0, "leg_spread": 1.1,
      "body_tilt": -18, "body_squash": 1.0, "arm_l_dy": -14, "arm_r_dy": 2},
     "squint", BG_CONFUSE, "← was: ANY STATE", "→ next: SEARCHING"),
    ("POWERED DOWN", "flat", "neutral",
     {"arm_dy": 26, "arm_x_scale": 0.20, "leg_spread": 0.6,
      "body_tilt": 0, "body_squash": 0.88, "arm_l_dy": 26, "arm_r_dy": 26},
     "flat", BG_PWRDOWN, "← was: ANY STATE", "→ next: BOOTING UP"),
    ("RESIGNED", "↓", "resigned",
     {"arm_dy": 24, "arm_x_scale": 0.25, "leg_spread": 0.70,
      "body_tilt": 14, "body_squash": 1.0, "arm_l_dy": 24, "arm_r_dy": 24},
     "droopy_resigned", BG_RESIGNED, "← was: NEUTRAL / GRUMPY", "→ next: COMPLYING"),
    ("STORM/CRACKED", "dead_zone", "storm",
     {"arm_dy": 10, "arm_x_scale": 0.55, "leg_spread": 0.72,
      "body_tilt": 18, "body_squash": 1.0, "arm_l_dy": 6, "arm_r_dy": 22,
      "storm_damage": True},
     "cracked_storm", BG_STORM, "← was: RESIGNED", "→ next: DAMAGE STATE"),
    ("UNGUARDED WARMTH", "heart_purple", "warmth",
     {"arm_dy": -14, "arm_x_scale": 1.0, "leg_spread": 0.85,
      "body_tilt": -4, "body_squash": 1.0,
      "arm_l_dy": -14, "arm_r_dy": -16, "float_offset": -4,
      "lower_l_angle": 8, "lower_r_angle": 8,
      "unguarded_warmth": True},
     "star_gold", BG_WARMTH, "← was: RELUCTANT JOY / ANY STATE",
     "→ He has stopped fighting it."),
]


# ── Cairo drawing helpers ──────────────────────────────────────────────────────

def cairo_ellipse_path(ctx, cx, cy, rx, ry):
    """Add an ellipse path to the context."""
    ctx.save()
    ctx.translate(cx, cy)
    if rx != 0 and ry != 0:
        ctx.scale(rx, ry)
    ctx.arc(0, 0, 1.0, 0, 2 * math.pi)
    ctx.restore()


def draw_pixel_grid_cairo(ctx, ox, oy, grid, cell, color_map):
    """Draw a pixel grid on cairo context."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    for row in range(rows):
        for col in range(cols):
            v = grid[row][col]
            color = color_map.get(v, VOID_BLACK)
            px = ox + col * cell
            py = oy + row * cell
            ctx.rectangle(px + 0.5, py + 0.5, cell - 1, cell - 1)
            set_color(ctx, color)
            ctx.fill()


def draw_pixel_symbol_cairo(ctx, cx, cy, size, symbol):
    """Draw a pixel-eye symbol on cairo context."""
    PIXEL_CYAN = (0, 240, 255)
    OFF = (20, 18, 28)

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
        # Background bezel
        ctx.rectangle(ox - 2, oy - 2, 7 * cell + 4, 7 * cell + 4)
        set_color(ctx, DEEP_CYAN_BG)
        ctx.fill_preserve()
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
        draw_pixel_grid_cairo(ctx, ox, oy, glyph, cell, color_map)
        # Crack line
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

    # Background bezel
    bg_color = (40, 32, 20) if sym_color == SOFT_GOLD else (255, 255, 255)
    ctx.rectangle(ox - 2, oy - 2, 5 * cell + 4, 5 * cell + 4)
    set_color(ctx, bg_color)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(1)
    ctx.stroke()

    off_color = (10, 8, 20)
    color_map = {1: sym_color, 0: off_color}
    draw_pixel_grid_cairo(ctx, ox, oy, grid, cell, color_map)


def draw_right_eye_cairo(ctx, cx, cy, size, style):
    """Draw Byte's right (organic) eye or special symbols."""
    cell = size // 5
    if cell < 2:
        cell = 2

    if style in ("star_gold", "flat"):
        draw_pixel_symbol_cairo(ctx, cx, cy, size, style)
        return

    ew = cell * 2
    eh = cell * 2

    def _eye_base(cx, cy, ew, eh_top, fill_c, ol_c=None, ol_w=1):
        cairo_ellipse_path(ctx, cx, cy, ew, eh_top)
        set_color(ctx, fill_c)
        ctx.fill()
        if ol_c:
            cairo_ellipse_path(ctx, cx, cy, ew, eh_top)
            set_color(ctx, ol_c)
            ctx.set_line_width(ol_w)
            ctx.stroke()

    if style == "half_open":
        eye_h = int(eh * 0.6)
        _eye_base(cx, cy, ew, eye_h, EYE_W, LINE, 1)
        cairo_ellipse_path(ctx, cx, cy, int(cell * 1.5), int(cell * 1.5))
        set_color(ctx, (45, 28, 14))
        ctx.fill()
        cairo_ellipse_path(ctx, cx, cy, cell // 2 + 1, cell // 2 + 1)
        set_color(ctx, LINE)
        ctx.fill()
        # Highlight
        cairo_ellipse_path(ctx, cx + cell, cy - cell // 2, cell // 2, cell // 3)
        set_color(ctx, (200, 195, 185))
        ctx.fill()
        # Heavy upper lid
        ctx.arc(cx, cy, ew, math.radians(200), math.radians(340))
        set_color(ctx, LINE)
        ctx.set_line_width(3)
        ctx.stroke()

    elif style == "wide":
        _eye_base(cx, cy, ew, eh, EYE_W)
        cairo_ellipse_path(ctx, cx + 2, cy + 2, cell, cell)
        set_color(ctx, (60, 38, 20))
        ctx.fill()
        cairo_ellipse_path(ctx, cx + 2, cy + 2, cell // 2, cell // 2)
        set_color(ctx, LINE)
        ctx.fill()
        cairo_ellipse_path(ctx, cx + cell, cy - eh + cell, cell // 2, cell // 3)
        set_color(ctx, (255, 252, 245))
        ctx.fill()

    elif style == "wide_scared":
        _eye_base(cx, cy, ew + 2, eh + 3, EYE_W, LINE, 2)
        cairo_ellipse_path(ctx, cx, cy, cell - 1, cell - 1)
        set_color(ctx, (60, 38, 20))
        ctx.fill()
        cairo_ellipse_path(ctx, cx, cy, 4, 4)
        set_color(ctx, LINE)
        ctx.fill()
        cairo_ellipse_path(ctx, cx + cell, cy - eh + cell, cell // 2, cell // 3)
        set_color(ctx, (255, 252, 245))
        ctx.fill()

    elif style == "angry":
        eye_h = eh - 2
        _eye_base(cx, cy + 2, ew, eye_h, EYE_W)
        cairo_ellipse_path(ctx, cx - 2, cy + cell // 2, cell, cell)
        set_color(ctx, (60, 38, 20))
        ctx.fill()
        cairo_ellipse_path(ctx, cx - 2, cy + cell // 2 + 2, 4, 4)
        set_color(ctx, LINE)
        ctx.fill()
        # Angry lid line
        ctx.move_to(cx - ew, cy - eh // 2 + 4)
        ctx.line_to(cx + ew, cy - eh // 2)
        set_color(ctx, LINE)
        ctx.set_line_width(3)
        ctx.stroke()

    elif style == "droopy":
        _eye_base(cx, cy + 3, ew, eh - 2, EYE_W)
        cairo_ellipse_path(ctx, cx + 1, cy + 2, cell, cell)
        set_color(ctx, (60, 38, 20))
        ctx.fill()
        cairo_ellipse_path(ctx, cx + 1, cy + 3, 4, 4)
        set_color(ctx, LINE)
        ctx.fill()
        # Droopy lid
        ctx.save()
        ctx.arc(cx, cy + 3, ew, math.radians(195), math.radians(345))
        set_color(ctx, LINE)
        ctx.set_line_width(6)
        ctx.stroke()
        ctx.restore()

    elif style == "droopy_resigned":
        eye_h = int(eh * 0.45)
        _eye_base(cx, cy + 6, ew, eye_h, EYE_W)
        cairo_ellipse_path(ctx, cx + 1, cy + 8, cell, cell)
        set_color(ctx, (60, 38, 20))
        ctx.fill()
        cairo_ellipse_path(ctx, cx + 1, cy + 10, 4, 4)
        set_color(ctx, LINE)
        ctx.fill()
        # Heavy droopy lid
        ctx.arc(cx, cy + 6, ew, math.radians(195), math.radians(345))
        set_color(ctx, LINE)
        ctx.set_line_width(8)
        ctx.stroke()

    elif style == "cracked_storm":
        eye_h = int(eh * 0.50)
        _eye_base(cx, cy + 4, ew, eye_h, EYE_W)
        cairo_ellipse_path(ctx, cx + 1, cy + 6, cell, cell)
        set_color(ctx, (35, 22, 10))
        ctx.fill()
        cairo_ellipse_path(ctx, cx + 1, cy + 8, 4, 4)
        set_color(ctx, LINE)
        ctx.fill()
        ctx.arc(cx, cy + 4, ew, math.radians(195), math.radians(345))
        set_color(ctx, LINE)
        ctx.set_line_width(8)
        ctx.stroke()

    elif style == "squint":
        _eye_base(cx, cy, ew, eh - 3, EYE_W)
        cairo_ellipse_path(ctx, cx, cy - 2, cell, cell)
        set_color(ctx, (60, 38, 20))
        ctx.fill()
        cairo_ellipse_path(ctx, cx, cy - 4, 4, 4)
        set_color(ctx, LINE)
        ctx.fill()
        # Squint line
        ctx.move_to(cx - ew, cy - eh // 2 + 4)
        ctx.line_to(cx + ew, cy - eh // 2 + 2)
        set_color(ctx, LINE)
        ctx.set_line_width(3)
        ctx.stroke()

    else:
        _eye_base(cx, cy, ew, eh, EYE_W)
        cairo_ellipse_path(ctx, cx, cy, cell, cell)
        set_color(ctx, (60, 38, 20))
        ctx.fill()
        cairo_ellipse_path(ctx, cx, cy, cell // 2, cell // 2)
        set_color(ctx, LINE)
        ctx.fill()


def draw_byte_cairo(ctx, cx, cy, size, name, cracked_symbol, emotion,
                    body_data, right_eye_style):
    """Draw Byte character using pycairo for smooth anti-aliased output."""
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

    body_rx = s // 2
    body_ry = int(s * 0.55 * body_squash)
    bcx = cx + body_tilt
    bcy = cy

    # Main oval body with wobble outline for organic feel
    # Body fill
    cairo_ellipse_path(ctx, bcx, bcy, body_rx, body_ry)
    set_color(ctx, BYTE_TEAL)
    ctx.fill()

    # Right-side shadow (clipped to ellipse)
    ctx.save()
    cairo_ellipse_path(ctx, bcx, bcy, body_rx, body_ry)
    ctx.clip()
    ctx.rectangle(bcx, bcy - body_ry, body_rx + 2, body_ry * 2 + 2)
    set_color(ctx, BYTE_SH)
    ctx.fill()
    ctx.restore()

    # Highlight arc (upper-left)
    ctx.save()
    cairo_ellipse_path(ctx, bcx, bcy, body_rx, body_ry)
    ctx.clip()
    cairo_ellipse_path(ctx, bcx - body_rx // 3, bcy - body_ry // 3,
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
    draw_wobble_path(ctx, body_pts, amplitude=0.8, frequency=0.12, seed=42 + hash(name) % 100)
    set_color(ctx, LINE)
    ctx.set_line_width(LINE_WEIGHT_ANCHOR)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.stroke()

    # Magenta scar markings
    crack_x = bcx - s // 4
    ctx.move_to(crack_x, bcy - body_ry // 2)
    ctx.line_to(crack_x + s // 8, bcy - body_ry // 6)
    set_color(ctx, SCAR_MAG)
    ctx.set_line_width(2.5)
    ctx.stroke()
    ctx.move_to(crack_x + s // 8, bcy - body_ry // 6)
    ctx.line_to(crack_x - s // 10, bcy + body_ry // 6)
    set_color(ctx, SCAR_MAG)
    ctx.set_line_width(2.5)
    ctx.stroke()

    # Damage notch (triangular chip on right side)
    ctx.move_to(bcx + body_rx - 4, bcy - body_ry // 4)
    ctx.line_to(bcx + body_rx + s // 12, bcy - body_ry // 6)
    ctx.line_to(bcx + body_rx - 4, bcy + body_ry // 6)
    ctx.close_path()
    set_color(ctx, BG)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(1)
    ctx.stroke()

    # Storm damage marks
    if storm_damage:
        sx = bcx + s // 6
        sy = bcy - body_ry + 10
        ctx.move_to(sx, sy)
        ctx.line_to(sx + 8, sy + 12)
        set_color(ctx, HOT_MAG)
        ctx.set_line_width(2)
        ctx.stroke()
        ctx.move_to(sx + 8, sy + 12)
        ctx.line_to(sx + 4, sy + 18)
        set_color(ctx, HOT_MAG)
        ctx.set_line_width(2)
        ctx.stroke()

    # Unguarded warmth gold glow
    if unguarded_warmth:
        ctx.save()
        cairo_ellipse_path(ctx, bcx, bcy, body_rx, body_ry)
        ctx.clip()
        cairo_ellipse_path(ctx, bcx + body_rx // 3, bcy, body_rx - 6, body_ry - 4)
        set_color(ctx, (*SOFT_GOLD, 60))
        ctx.set_line_width(3)
        ctx.stroke()
        ctx.restore()

    # Eyes
    eye_y = bcy - body_ry // 5
    eye_size = max(14, int(body_ry * 0.46))

    # Left eye (pixel/cracked)
    lx = bcx - s // 5
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

    draw_pixel_symbol_cairo(ctx, lx, eye_y, eye_size, cracked_symbol)

    # Right eye (organic)
    rx_eye = bcx + s // 5
    draw_right_eye_cairo(ctx, rx_eye, eye_y, eye_size, right_eye_style)

    # Mouth
    mouth_y = bcy + body_ry // 3
    mw = s // 3
    if emotion == "disgust":
        ctx.arc(bcx, mouth_y + 4, mw // 2, math.radians(200), math.radians(340))
        set_color(ctx, LINE)
        ctx.set_line_width(3)
        ctx.stroke()
    elif emotion == "curious":
        cairo_ellipse_path(ctx, bcx, mouth_y - 2, 8, 6)
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
    elif emotion == "fear":
        cairo_ellipse_path(ctx, bcx, mouth_y + 4, mw // 2 - 4, 10)
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
    ant_base_x = bcx - s // 8
    ant_base_y = bcy - body_ry
    if storm_damage:
        ant_mid_x = ant_base_x + 6
        ant_mid_y = ant_base_y - s // 5
        ant_tip_x = ant_mid_x - 8
        ant_tip_y = ant_mid_y - s // 8
        ctx.move_to(ant_base_x, ant_base_y)
        ctx.line_to(ant_mid_x, ant_mid_y)
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
        ctx.move_to(ant_mid_x, ant_mid_y)
        ctx.line_to(ant_tip_x, ant_tip_y)
        ctx.stroke()
        cairo_ellipse_path(ctx, ant_tip_x, ant_tip_y, 3, 3)
        set_color(ctx, HOT_MAG)
        ctx.fill()
    elif unguarded_warmth:
        ant_tip_x = ant_base_x - s // 10
        ant_tip_y = ant_base_y - s // 3
        ctx.move_to(ant_base_x, ant_base_y)
        ctx.line_to(ant_tip_x, ant_tip_y)
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
        cairo_ellipse_path(ctx, ant_tip_x, ant_tip_y, 4, 4)
        set_color(ctx, SOFT_GOLD)
        ctx.fill()
    else:
        ant_tip_x = ant_base_x - s // 10
        ant_tip_y = ant_base_y - s // 3
        ctx.move_to(ant_base_x, ant_base_y)
        ctx.line_to(ant_tip_x, ant_tip_y)
        set_color(ctx, LINE)
        ctx.set_line_width(2)
        ctx.stroke()
        cairo_ellipse_path(ctx, ant_tip_x, ant_tip_y, 4, 4)
        set_color(ctx, BYTE_HL)
        ctx.fill()

    # Limbs
    lw = s // 6
    lh = s // 5
    arm_extend = int(lw * arm_x_scale)
    arm_base_y = bcy - body_ry // 5

    # Left arm with rounded-tip shape
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
    rng = random.Random(hash(name) % 1000 + 7)
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
            # Bezier trail behind particle
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
            # Bezier trail
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


# ── Storm background ──────────────────────────────────────────────────────────

def draw_storm_bg_cairo(ctx, px, py, pw, ph):
    """Draw storm/circuit trace background texture."""
    trace_color = (0, 40, 50)
    uv_color = (40, 20, 60)
    for y_off in [40, 90, 140, 190, 240, 290]:
        yy = py + y_off
        for x_start in [px + 10, px + 80, px + 140]:
            seg_len = 30 + (x_start % 40)
            ctx.move_to(x_start, yy)
            ctx.line_to(x_start + seg_len, yy)
            set_color(ctx, trace_color)
            ctx.set_line_width(1)
            ctx.stroke()
    for i in range(3):
        x1 = px + i * 30
        y1 = py + 10
        x2 = px + pw
        y2 = py + ph // 2 + i * 20
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        set_color(ctx, uv_color)
        ctx.set_line_width(1)
        ctx.stroke()


def draw_warmth_bg_cairo(ctx, px, py, pw, ph):
    """Subtle warm glow gradient at bottom of warmth panel."""
    for i in range(8):
        alpha_ratio = (i + 1) / 8
        r = int(232 * alpha_ratio + 240 * (1 - alpha_ratio))
        g = int(201 * alpha_ratio + 224 * (1 - alpha_ratio))
        b = int(90 * alpha_ratio + 198 * (1 - alpha_ratio))
        yy = py + int(ph * (0.75 + i * 0.03))
        if yy < py + ph:
            ctx.rectangle(px, yy, pw, py + ph - yy)
            set_color(ctx, (r, g, b))
            ctx.fill()


# ── Sheet generator ─────────────────────────────────────────────────────────────

def generate_byte_expression_sheet(output_path):
    """Render 4x3 expression grid for Byte using pycairo. 10 expressions + 2 empty."""
    total_w = COLS * (PANEL_W + PAD) + PAD
    total_h = HEADER + ROWS * (PANEL_H + PAD) + PAD

    surface, ctx, _, _ = create_surface(total_w, total_h)
    fill_background(ctx, total_w, total_h, BG)

    # Title text
    ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(14)
    ctx.set_source_rgb(*_c(BYTE_HL))
    ctx.move_to(PAD, 30)
    ctx.show_text("BYTE — Expression Sheet v008 (pycairo rebuild C52)")

    for i, (name, symbol, emotion, body_data, right_eye_style, panel_bg,
            prev_st, next_st) in enumerate(EXPRESSIONS):
        col = i % COLS
        row = i // COLS
        ppx = PAD + col * (PANEL_W + PAD)
        ppy = HEADER + row * (PANEL_H + PAD)

        # Panel background
        ctx.rectangle(ppx, ppy, PANEL_W, PANEL_H)
        set_color(ctx, panel_bg)
        ctx.fill()

        # Special panel backgrounds
        if emotion == "storm":
            draw_storm_bg_cairo(ctx, ppx, ppy, PANEL_W, PANEL_H)
        if name == "UNGUARDED WARMTH":
            draw_warmth_bg_cairo(ctx, ppx, ppy, PANEL_W, PANEL_H)

        # Panel border
        ctx.rectangle(ppx, ppy, PANEL_W, PANEL_H)
        set_color(ctx, (40, 35, 55))
        ctx.set_line_width(1)
        ctx.stroke()

        # Draw Byte
        byte_size = 88
        bcx_panel = ppx + PANEL_W // 2
        bcy_panel = ppy + PANEL_H // 2 - 20
        draw_byte_cairo(ctx, bcx_panel, bcy_panel, byte_size,
                        name, symbol, emotion, body_data, right_eye_style)

        # Version tag
        if "STORM" in name:
            ctx.set_font_size(9)
            ctx.set_source_rgb(*_c(HOT_MAG))
            ctx.move_to(ppx + PANEL_W - 50, ppy + 14)
            ctx.show_text("[v003]")
        if "WARMTH" in name:
            ctx.set_font_size(9)
            ctx.set_source_rgb(*_c(SOFT_GOLD))
            ctx.move_to(ppx + PANEL_W - 62, ppy + 14)
            ctx.show_text("[NEW v005]")

        # Label bar
        bar_h = 58
        ctx.rectangle(ppx, ppy + PANEL_H - bar_h, PANEL_W, bar_h)
        set_color(ctx, (10, 8, 18))
        ctx.fill()

        label_color = SOFT_GOLD if "WARMTH" in name else BYTE_HL
        ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(12)
        ctx.set_source_rgb(*_c(label_color))
        ctx.move_to(ppx + 6, ppy + PANEL_H - bar_h + 16)
        ctx.show_text(name)

        ctx.set_font_size(9)
        ctx.set_source_rgb(*_c((120, 110, 140)))
        ctx.move_to(ppx + 6, ppy + PANEL_H - bar_h + 30)
        ctx.show_text(prev_st)
        ctx.move_to(ppx + 6, ppy + PANEL_H - bar_h + 44)
        ctx.show_text(next_st)

    # Convert to PIL and enforce size constraint
    img = to_pil_image(surface)
    img.thumbnail((1280, 1280), Image.LANCZOS)
    img.save(output_path)
    w, h = img.size
    print(f"Saved: {output_path}  ({w}x{h}px)")


if __name__ == '__main__':
    out_dir = str(output_dir('characters', 'main'))
    os.makedirs(out_dir, exist_ok=True)
    generate_byte_expression_sheet(
        os.path.join(out_dir, "LTG_CHAR_byte_expression_sheet.png")
    )
    print("v008 pycairo rebuild (Rin Yamamoto C52)")
    print("  Anti-aliased ellipses, wobble outlines, bezier confetti trails")
    print("  All 10 expressions preserved from v007")
