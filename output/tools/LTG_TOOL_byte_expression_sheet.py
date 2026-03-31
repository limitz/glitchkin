#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_byte_expression_sheet.py
Byte Expression Sheet — v009 Thin Wrapper
"Luma & the Glitchkin" — Cycle 54 / Maya Santos

v009 CHANGES (C54 — thin wrapper migration):
  All character drawing logic now lives in LTG_TOOL_char_byte.py (canonical renderer).
  This file handles ONLY sheet layout (4x3 grid), panel backgrounds, labels, and compositing.
  10 expressions, same output as v008.

Output: output/characters/main/LTG_CHAR_byte_expression_sheet.png
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

from LTG_TOOL_char_byte import (
    draw_byte, VALID_EXPRESSIONS, EXPRESSION_SPECS,
    BYTE_TEAL, BYTE_HL, BYTE_SH, HOT_MAG, SOFT_GOLD, LINE, VOID_BLACK,
)
from LTG_TOOL_cairo_primitives import (
    create_surface, set_color, fill_background,
    to_pil_image, to_pil_rgba, _c,
)

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path

from PIL import Image
import cairo

# ── Palette (sheet-level) ─────────────────────────────────────────────────────
BG         = (20, 18, 28)
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

# ── Expression metadata (sheet-specific: display names, backgrounds, labels) ──
EXPRESSIONS = [
    ("NEUTRAL / DEFAULT", "neutral", BG_NEUTRAL,
     "\u2190 was: ANY STATE", "\u2192 next: SEARCHING / GRUMPY"),
    ("GRUMPY", "grumpy", BG_GRUMPY,
     "\u2190 was: NEUTRAL", "\u2192 next: REFUSING"),
    ("SEARCHING", "searching", BG_SEARCH,
     "\u2190 was: NEUTRAL", "\u2192 next: ALARMED / FOUND"),
    ("ALARMED", "alarmed", BG_ALARM,
     "\u2190 was: SEARCHING", "\u2192 next: FLEEING / FROZEN"),
    ("RELUCTANT JOY", "reluctant_joy", BG_RELJOY,
     "\u2190 was: GRUMPY", "\u2192 next: DENYING IT"),
    ("CONFUSED", "confused", BG_CONFUSE,
     "\u2190 was: ANY STATE", "\u2192 next: SEARCHING"),
    ("POWERED DOWN", "powered_down", BG_PWRDOWN,
     "\u2190 was: ANY STATE", "\u2192 next: BOOTING UP"),
    ("RESIGNED", "resigned", BG_RESIGNED,
     "\u2190 was: NEUTRAL / GRUMPY", "\u2192 next: COMPLYING"),
    ("STORM/CRACKED", "storm_cracked", BG_STORM,
     "\u2190 was: RESIGNED", "\u2192 next: DAMAGE STATE"),
    ("UNGUARDED WARMTH", "unguarded_warmth", BG_WARMTH,
     "\u2190 was: RELUCTANT JOY / ANY STATE",
     "\u2192 He has stopped fighting it."),
]


def generate_byte_expression_sheet(output_path):
    """Render 4x3 expression grid for Byte using the canonical char_byte renderer."""
    total_w = COLS * (PANEL_W + PAD) + PAD
    total_h = HEADER + ROWS * (PANEL_H + PAD) + PAD

    surface, ctx, _, _ = create_surface(total_w, total_h)
    fill_background(ctx, total_w, total_h, BG)

    # Title text
    ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(14)
    ctx.set_source_rgb(*_c(BYTE_HL))
    ctx.move_to(PAD, 30)
    ctx.show_text("BYTE \u2014 Expression Sheet v009 (canonical char_byte C54)")

    for i, (display_name, expr_key, panel_bg, prev_st, next_st) in enumerate(EXPRESSIONS):
        col = i % COLS
        row = i // COLS
        ppx = PAD + col * (PANEL_W + PAD)
        ppy = HEADER + row * (PANEL_H + PAD)

        # Panel background
        ctx.rectangle(ppx, ppy, PANEL_W, PANEL_H)
        set_color(ctx, panel_bg)
        ctx.fill()

        # Panel border
        ctx.rectangle(ppx, ppy, PANEL_W, PANEL_H)
        set_color(ctx, (40, 35, 55))
        ctx.set_line_width(1)
        ctx.stroke()

        # Draw character via canonical renderer
        char_surface = draw_byte(expression=expr_key, scale=1.0)
        char_img = to_pil_rgba(char_surface)

        # Crop to content
        bbox = char_img.getbbox()
        if bbox:
            char_img = char_img.crop(bbox)

        # Fit into panel (leave room for label bar)
        bar_h = 58
        avail_w = PANEL_W - 8
        avail_h = PANEL_H - bar_h - 8
        char_img.thumbnail((avail_w, avail_h), Image.LANCZOS)

        # Center in panel area above label bar
        cx = ppx + (PANEL_W - char_img.width) // 2
        cy = ppy + (PANEL_H - bar_h - char_img.height) // 2
        # Need to composite: convert sheet surface to PIL, paste, convert back
        # Since we're on a cairo surface, we paste the character as a cairo source
        # Convert char PIL to cairo pattern
        char_rgb = char_img.convert("RGBA")
        char_data = char_rgb.tobytes("raw", "BGRa")
        char_cairo_surf = cairo.ImageSurface.create_for_data(
            bytearray(char_data), cairo.FORMAT_ARGB32,
            char_img.width, char_img.height
        )
        ctx.set_source_surface(char_cairo_surf, cx, cy)
        ctx.paint()

        # Version tag
        if "STORM" in display_name:
            ctx.set_font_size(9)
            ctx.set_source_rgb(*_c(HOT_MAG))
            ctx.move_to(ppx + PANEL_W - 50, ppy + 14)
            ctx.show_text("[v003]")
        if "WARMTH" in display_name:
            ctx.set_font_size(9)
            ctx.set_source_rgb(*_c(SOFT_GOLD))
            ctx.move_to(ppx + PANEL_W - 62, ppy + 14)
            ctx.show_text("[NEW v005]")

        # Label bar
        ctx.rectangle(ppx, ppy + PANEL_H - bar_h, PANEL_W, bar_h)
        set_color(ctx, (10, 8, 18))
        ctx.fill()

        label_color = SOFT_GOLD if "WARMTH" in display_name else BYTE_HL
        ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(12)
        ctx.set_source_rgb(*_c(label_color))
        ctx.move_to(ppx + 6, ppy + PANEL_H - bar_h + 16)
        ctx.show_text(display_name)

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
    print("v009 thin wrapper (Maya Santos C54)")
    print("  Character drawing via canonical char_byte renderer")
    print("  All 10 expressions preserved")
