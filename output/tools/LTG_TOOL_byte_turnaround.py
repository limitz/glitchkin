#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_byte_turnaround.py
Byte — 4-View Color Turnaround v002 (pycairo)
"Luma & the Glitchkin" — Cycle 54 / Rin Yamamoto

v002 UPDATE (C54 — Canonical renderer migration):
  Migrated from inline pycairo drawing to canonical char_byte.py renderer.
  All 4 views (FRONT, RIGHT, LEFT, BACK) call draw_byte() with
  appropriate facing values. BACK view uses shadow-fill overlay
  (shadow color as primary fill, per BACK view convention).

Features preserved:
  - BYTE_TEAL body fill with highlights
  - Cracked eye with magenta pixel grid
  - Antenna with cyan tip
  - Pixel confetti hover particles

Output: output/characters/main/turnarounds/LTG_CHAR_byte_turnaround.png
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from LTG_TOOL_char_byte import draw_byte, VALID_EXPRESSIONS
from LTG_TOOL_cairo_primitives import to_pil_rgba

try:
    from LTG_TOOL_project_paths import output_dir
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)

from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# ── Layout ────────────────────────────────────────────────────────────────────
CANVAS_W = 800
CANVAS_H = 360
VIEWS = ["FRONT", "RIGHT", "LEFT", "BACK"]
N_VIEWS = 4
VIEW_W = CANVAS_W // N_VIEWS
TITLE_H = 36
LABEL_H = 32
CHAR_AREA_H = CANVAS_H - TITLE_H - LABEL_H

# ── Colors ────────────────────────────────────────────────────────────────────
BG = (252, 250, 246)
BYTE_TEAL = (0, 212, 232)
LINE_COL = (50, 40, 35)

FACING_MAP = {
    "FRONT": "front",
    "RIGHT": "right",
    "LEFT": "left",
    "BACK": "front",
}

DEFAULT_EXPRESSION = "neutral"


def _render_char_view(facing, expression=DEFAULT_EXPRESSION, scale=1.0):
    """Render a single Byte view and return a cropped RGBA PIL Image."""
    surface = draw_byte(expression=expression, facing=facing, scale=scale)
    img = to_pil_rgba(surface)
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img


def _apply_back_treatment(img):
    """Apply shadow overlay to indicate BACK view — darkened, desaturated."""
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.60)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.45)
    return img


def build_turnaround():
    """Build the 4-view Byte turnaround strip."""
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), BG)
    draw = ImageDraw.Draw(canvas)

    # Title
    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = font_title

    draw.text((12, 8), "BYTE — Color Turnaround  |  v002 canonical  |  C54  |  Rin Yamamoto",
              fill=BYTE_TEAL, font=font_title)

    # Ground line
    ground_y = TITLE_H + CHAR_AREA_H - 10
    draw.line([(0, ground_y), (CANVAS_W, ground_y)], fill=(200, 190, 180), width=1)

    # Panel borders
    for v in range(1, N_VIEWS):
        x = v * VIEW_W
        draw.line([(x, TITLE_H), (x, CANVAS_H - LABEL_H)],
                  fill=(230, 225, 218), width=1)

    # Render each view
    for v, view_name in enumerate(VIEWS):
        facing = FACING_MAP[view_name]
        char_img = _render_char_view(facing, scale=2.0)

        if view_name == "BACK":
            char_img = _apply_back_treatment(char_img)

        max_h = CHAR_AREA_H - 20
        max_w = VIEW_W - 16
        char_img.thumbnail((max_w, max_h), Image.LANCZOS)

        panel_cx = v * VIEW_W + VIEW_W // 2
        x_off = panel_cx - char_img.width // 2
        y_off = ground_y - char_img.height
        canvas.paste(char_img, (x_off, y_off), char_img)

        # View label
        draw = ImageDraw.Draw(canvas)
        try:
            lb = draw.textbbox((0, 0), view_name, font=font_label)
            lw = lb[2] - lb[0]
        except Exception:
            lw = len(view_name) * 7
        draw.text((panel_cx - lw // 2, CANVAS_H - LABEL_H + 8),
                  view_name, fill=LINE_COL, font=font_label)

    img = canvas
    img.thumbnail((1280, 1280), Image.LANCZOS)
    return img


def main():
    out_dir = str(output_dir('characters', 'main', 'turnarounds'))
    os.makedirs(out_dir, exist_ok=True)

    img = build_turnaround()
    out_path = os.path.join(out_dir, "LTG_CHAR_byte_turnaround.png")
    img.save(out_path)
    w, h = img.size
    print(f"Saved: {out_path}  ({w}x{h}px)")

    main_dir = str(output_dir('characters', 'main'))
    main_path = os.path.join(main_dir, "LTG_CHAR_byte_turnaround.png")
    img.save(main_path)
    print(f"Also saved: {main_path}")


if __name__ == "__main__":
    main()
