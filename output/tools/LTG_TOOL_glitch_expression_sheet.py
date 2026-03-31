#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_glitch_expression_sheet.py
Glitch — Expression Sheet v005 Thin Wrapper
"Luma & the Glitchkin" — Cycle 54 / Maya Santos

v005 CHANGES (C54 — thin wrapper migration):
  All character drawing logic now lives in LTG_TOOL_char_glitch.py (canonical renderer).
  This file handles ONLY sheet layout (3x3 grid at 2x, downscaled), panel backgrounds,
  and expression labels. 9 expressions preserved.
  Interior desire states: YEARNING, COVETOUS, HOLLOW retained.

Output: output/characters/main/LTG_CHAR_glitch_expression_sheet.png
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

from LTG_TOOL_char_glitch import (
    draw_glitch, VALID_EXPRESSIONS,
    CORRUPT_AMB, CORRUPT_AMB_SH, CORRUPT_AMB_HL,
    SOFT_GOLD, HOT_MAG, UV_PURPLE, VOID_BLACK, STATIC_WHITE,
)
from LTG_TOOL_cairo_primitives import (
    create_surface, set_color, fill_background,
    to_pil_image, to_pil_rgba, _c,
)

try:
    from LTG_TOOL_project_paths import output_dir
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)

from PIL import Image
import cairo

# ── Palette (sheet-level) ─────────────────────────────────────────────────────
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

# ── Layout ────────────────────────────────────────────────────────────────────
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

# ── Expression metadata ───────────────────────────────────────────────────────
SHEET_EXPRESSIONS = [
    ("NEUTRAL",      "neutral",      BG_NEUTRAL),
    ("MISCHIEVOUS",  "mischievous",  BG_MISCHIEVOUS),
    ("PANICKED",     "panicked",     BG_PANICKED),
    ("TRIUMPHANT",   "triumphant",   BG_TRIUMPHANT),
    ("STUNNED",      "stunned",      BG_STUNNED),
    ("CALCULATING",  "calculating",  BG_CALCULATING),
    ("YEARNING",     "yearning",     BG_YEARNING),
    ("COVETOUS",     "covetous",     BG_COVETOUS),
    ("HOLLOW",       "hollow",       BG_HOLLOW),
]


def build_sheet():
    """Build the 3x3 Glitch expression sheet using canonical renderer at 2x then downscale."""
    W2 = CANVAS_W_1X * SCALE
    H2 = CANVAS_H_1X * SCALE
    PW2 = PANEL_W_1X * SCALE
    PH2 = PANEL_H_1X * SCALE
    PAD2 = PAD * SCALE
    HEADER_H2 = HEADER_H * SCALE
    LABEL_H2 = LABEL_H * SCALE

    surface, ctx, _, _ = create_surface(W2, H2)
    fill_background(ctx, W2, H2, CANVAS_BG)

    # Title header
    ctx.rectangle(0, 0, W2, HEADER_H2)
    set_color(ctx, (18, 14, 26))
    ctx.fill()

    ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(24 * SCALE)
    title_text = "GLITCH \u2014 Expression Sheet v005  [C54 canonical char_glitch \u2014 9 Expressions]"
    ext = ctx.text_extents(title_text)
    ctx.move_to((W2 - ext.width) / 2, (HEADER_H2 + ext.height) / 2 - 10 * SCALE)
    ctx.set_source_rgb(*_c(CORRUPT_AMB))
    ctx.show_text(title_text)

    ctx.set_font_size(10 * SCALE)
    sub_text = "ANTAGONIST  |  GL-07 CORRUPT AMBER  |  CYCLE 54 canonical renderer  |  1200x900  3x3"
    ext2 = ctx.text_extents(sub_text)
    ctx.move_to((W2 - ext2.width) / 2, HEADER_H2 - 8 * SCALE)
    ctx.set_source_rgb(*_c((120, 80, 40)))
    ctx.show_text(sub_text)

    for idx, (display_name, expr_key, bg_col) in enumerate(SHEET_EXPRESSIONS):
        col = idx % COLS
        row = idx // COLS

        px = PAD2 + col * (PW2 + PAD2)
        py = HEADER_H2 + PAD2 + row * (PH2 + LABEL_H2 + PAD2)

        # Panel background
        ctx.rectangle(px, py, PW2, PH2)
        set_color(ctx, bg_col)
        ctx.fill()

        # Draw character via canonical renderer
        char_surface = draw_glitch(expression=expr_key, scale=SCALE)
        char_img = to_pil_rgba(char_surface)

        # Crop to content
        bbox = char_img.getbbox()
        if bbox:
            char_img = char_img.crop(bbox)

        # Fit into panel
        avail_w = PW2 - 8
        avail_h = PH2 - 8
        char_img.thumbnail((avail_w, avail_h), Image.LANCZOS)

        # Center in panel
        cx = int(px + (PW2 - char_img.width) / 2)
        cy = int(py + (PH2 - char_img.height) / 2)

        # Composite character onto cairo surface
        char_rgba = char_img.convert("RGBA")
        char_data = char_rgba.tobytes("raw", "BGRa")
        char_cairo_surf = cairo.ImageSurface.create_for_data(
            bytearray(char_data), cairo.FORMAT_ARGB32,
            char_img.width, char_img.height
        )
        ctx.set_source_surface(char_cairo_surf, cx, cy)
        ctx.paint()

        # Panel border
        ctx.rectangle(px, py, PW2, PH2)
        set_color(ctx, (40, 30, 50))
        ctx.set_line_width(1)
        ctx.stroke()

        # Label
        label_y = py + PH2 + 4 * SCALE
        ctx.set_font_size(10 * SCALE)
        ext = ctx.text_extents(display_name)
        ctx.move_to(px + (PW2 - ext.width) / 2, label_y + ext.height)
        ctx.set_source_rgb(*_c(CORRUPT_AMB))
        ctx.show_text(display_name)

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
    print("  Expressions: " + ", ".join(name for name, _, _ in SHEET_EXPRESSIONS))
    print("  v005 thin wrapper (Maya Santos C54)")
    print("  Character drawing via canonical char_glitch renderer")
    print("  Interior desire states preserved: YEARNING, COVETOUS, HOLLOW")


if __name__ == "__main__":
    main()
