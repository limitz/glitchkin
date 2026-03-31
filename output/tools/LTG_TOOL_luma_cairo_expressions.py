#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_luma_cairo_expressions.py — Luma Full Expression Sheet v3.0.0
"Luma & the Glitchkin" — Cycle 54 / Maya Santos

PURPOSE:
  Thin wrapper around LTG_TOOL_char_luma.py (the canonical Luma renderer).
  Generates a 3x2 expression sheet by calling draw_luma() for each expression,
  converting to PIL, and pasting onto a grid with labels and color enhancements.

  All character drawing logic lives in LTG_TOOL_char_luma.py.
  This file handles ONLY sheet layout, labels, and color enhancement compositing.

EXPRESSIONS (all 6):
  CURIOUS, DETERMINED, SURPRISED, WORRIED, DELIGHTED, FRUSTRATED

OUTPUT:
  output/characters/main/LTG_CHAR_luma_expression_sheet.png (1280x720)
  output/production/LTG_PROD_luma_cairo_expressions.png (1280x720) [copy]

Dependencies: pycairo, Pillow, LTG_TOOL_char_luma
"""

__version__ = "3.0.0"
__author__ = "Maya Santos"
__cycle__ = 54

import os
import sys

import cairo
from PIL import Image

# Add tools dir to path for imports
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS_DIR)

from LTG_TOOL_char_luma import (
    draw_luma, draw_luma_on_context, cairo_surface_to_pil,
    EXPRESSIONS, HOODIE_COLORS, LINE_COL, GESTURE_SPECS,
)

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir
except ImportError:
    import pathlib
    def output_dir(*parts):
        return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path):
        path.mkdir(parents=True, exist_ok=True)
        return path

try:
    from LTG_TOOL_character_color_enhance import (
        apply_scene_tint, apply_skin_warmth, apply_form_shadow
    )
    HAS_COLOR_ENHANCE = True
except ImportError:
    HAS_COLOR_ENHANCE = False

# ── Sheet Layout Constants ──────────────────────────────────────────────────
RENDER_W = 2560
RENDER_H = 1440
OUTPUT_W = 1280
OUTPUT_H = 720
CANVAS_BG = (235/255, 224/255, 206/255)

# PIL palette for color enhance integration
HOODIE_PIL    = (232, 112, 58)
HOODIE_SH_PIL = (184, 74, 32)


def _set_color(ctx, color, alpha=1.0):
    """Set cairo source color. Accepts 3-tuple (rgb) or 4-tuple (rgba)."""
    if len(color) == 4:
        ctx.set_source_rgba(*color[:3], color[3] * alpha)
    else:
        ctx.set_source_rgba(*color, alpha)


# ── Main Render ──────────────────────────────────────────────────────────────

def render_expression_sheet():
    """Render all 6 Luma expressions in a 3x2 grid using the canonical renderer."""

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, RENDER_W, RENDER_H)
    ctx = cairo.Context(surface)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)

    # Background
    _set_color(ctx, CANVAS_BG)
    ctx.rectangle(0, 0, RENDER_W, RENDER_H)
    ctx.fill()

    # 3x2 grid layout
    cols = 3
    rows = 2
    margin = 30
    top_margin = 50  # room for title
    panel_w = (RENDER_W - (cols + 1) * margin) // cols
    panel_h = (RENDER_H - top_margin - (rows + 1) * margin) // rows

    expressions = list(EXPRESSIONS)
    panel_colors = [
        (230/255, 240/255, 235/255),   # warm mint
        (240/255, 232/255, 218/255),   # warm cream
        (240/255, 225/255, 230/255),   # warm rose
        (225/255, 230/255, 240/255),   # cool lavender
        (245/255, 238/255, 220/255),   # warm gold
        (238/255, 225/255, 225/255),   # muted coral
    ]

    char_data = []

    for idx, expr in enumerate(expressions):
        col = idx % cols
        row = idx // cols
        px = margin + col * (panel_w + margin)
        py = top_margin + margin + row * (panel_h + margin)

        # Panel background
        ctx.rectangle(px, py, panel_w, panel_h)
        _set_color(ctx, panel_colors[idx])
        ctx.fill_preserve()
        _set_color(ctx, LINE_COL, 0.15)
        ctx.set_line_width(2)
        ctx.stroke()

        # Ground plane
        ground_y = py + panel_h - 45

        # Ground line
        ctx.new_path()
        ctx.move_to(px + 15, ground_y)
        ctx.line_to(px + panel_w - 15, ground_y)
        _set_color(ctx, LINE_COL, 0.2)
        ctx.set_line_width(2)
        ctx.stroke()

        # Drop shadow band (warm)
        ctx.rectangle(px + 15, ground_y, panel_w - 30, 10)
        _set_color(ctx, (0.85, 0.78, 0.65, 0.3))
        ctx.fill()

        # Character — drawn via canonical renderer directly on context
        char_h = panel_h - 100  # leave room for label and ground
        char_cx = px + panel_w / 2
        info = draw_luma_on_context(ctx, char_cx, ground_y, char_h, expr)
        char_data.append((expr, info))

        # Label
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(22)
        _set_color(ctx, LINE_COL)
        text_ext = ctx.text_extents(expr)
        ctx.move_to(px + panel_w / 2 - text_ext.width / 2,
                    py + panel_h - 12)
        ctx.show_text(expr)

        # Sub-label
        ctx.set_font_size(11)
        _set_color(ctx, LINE_COL, 0.5)
        sub = f"37% head | gesture line | cairo v{__version__}"
        sub_ext = ctx.text_extents(sub)
        ctx.move_to(px + panel_w / 2 - sub_ext.width / 2, py + 18)
        ctx.show_text(sub)

    # Title bar
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(18)
    _set_color(ctx, LINE_COL, 0.6)
    title = "LUMA \u2014 Full Expression Sheet C54 / Maya Santos / pycairo (canonical)"
    title_ext = ctx.text_extents(title)
    ctx.move_to(RENDER_W / 2 - title_ext.width / 2, 32)
    ctx.show_text(title)

    # Convert to PIL for color enhancement and final output
    pil_img = cairo_surface_to_pil(surface)

    # Apply Sam's color enhancements if available
    if HAS_COLOR_ENHANCE:
        pil_rgb = pil_img.convert("RGB")

        for expr, info in char_data:
            char_left = int(info["head_cx"] - info["head_rx"] * 2)
            char_top = int(info["head_cy"] - info["head_r"] * 1.5)
            char_right = int(info["head_cx"] + info["head_rx"] * 2)
            char_bottom = int(info["ground_y"])
            char_bbox = (char_left, char_top, char_right, char_bottom)

            pil_rgb = apply_scene_tint(pil_rgb, char_bbox,
                                        key_light_color=(212, 146, 58), alpha=18)

            face_center = (int(info["head_cx"]), int(info["head_cy"]))
            face_radius = (int(info["head_rx"]), int(info["head_ry"]))
            pil_rgb = apply_skin_warmth(pil_rgb, face_center, face_radius)

            torso_left = int(info["torso_cx"] - info["head_r"] * 0.8)
            torso_top = int(info["torso_cy"] - info["char_h"] * 0.19)
            torso_right = int(info["torso_cx"] + info["head_r"] * 0.8)
            torso_bottom = int(info["torso_cy"] + info["char_h"] * 0.19)
            pil_rgb = apply_form_shadow(pil_rgb,
                                         (torso_left, torso_top, torso_right, torso_bottom),
                                         HOODIE_PIL, HOODIE_SH_PIL,
                                         shadow_shape="torso_diagonal")

        pil_img = pil_rgb.convert("RGBA")

    # Downscale to output resolution with LANCZOS
    pil_out = pil_img.convert("RGB").resize((OUTPUT_W, OUTPUT_H), Image.LANCZOS)

    # Save to BOTH locations (production + main character sheet)
    prod_path = str(output_dir("production", "LTG_PROD_luma_cairo_expressions.png"))
    ensure_dir(output_dir("production"))
    pil_out.save(prod_path)

    main_path = str(output_dir("characters", "main", "LTG_CHAR_luma_expression_sheet.png"))
    ensure_dir(output_dir("characters", "main"))
    pil_out.save(main_path)

    print(f"Saved: {prod_path}")
    print(f"Saved: {main_path}")
    print(f"  Size: {pil_out.size[0]}x{pil_out.size[1]}")
    print(f"  Expressions: {', '.join(expressions)}")
    print(f"  Engine: pycairo {cairo.version} (canonical char_luma)")
    print(f"  Color enhance: {'applied' if HAS_COLOR_ENHANCE else 'skipped (import failed)'}")

    return main_path, char_data


if __name__ == "__main__":
    out_path, char_data = render_expression_sheet()
    print(f"\nDone. Output at: {out_path}")
