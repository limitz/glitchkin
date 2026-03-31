#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_luma_turnaround.py
Luma — 4-View Character Turnaround v005
"Luma & the Glitchkin" — Cycle 54 / Rin Yamamoto

v005 UPDATE (C54 — Canonical renderer migration):
  Migrated from inline PIL drawing to canonical char_luma.py renderer.
  All 4 views (FRONT, LEFT, RIGHT, BACK) now call draw_luma() with
  appropriate facing values. BACK view uses shadow-fill overlay on
  the right-facing render to represent the rear view.

4 views: FRONT, RIGHT, LEFT, BACK
Canvas: 1280x560 (within 1280px limit)

Output: output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png
"""

import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from LTG_TOOL_char_luma import draw_luma, EXPRESSIONS
from LTG_TOOL_cairo_primitives import to_pil_rgba

from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# ── Layout ────────────────────────────────────────────────────────────────────
CANVAS_W = 1280
CANVAS_H = 560
VIEWS = ["FRONT", "RIGHT", "LEFT", "BACK"]
N_VIEWS = 4
VIEW_W = CANVAS_W // N_VIEWS
HEADER_H = 44
LABEL_H = 32
CHAR_AREA_H = CANVAS_H - HEADER_H - LABEL_H

# ── Colors ────────────────────────────────────────────────────────────────────
CANVAS_BG = (248, 244, 238)
PANEL_BG_A = (245, 240, 232)
PANEL_BG_B = (240, 236, 228)
LABEL_COL = (59, 40, 32)
SHADOW_COL = (210, 200, 185)

# Facing map: FRONT draws both eyes (right-facing is the primary view).
# BACK uses right-facing with a shadow overlay to indicate rear view.
FACING_MAP = {
    "FRONT": "right",
    "RIGHT": "right",
    "LEFT": "left",
    "BACK": "right",
}

DEFAULT_EXPRESSION = "CURIOUS"


def _render_char_view(facing, expression=DEFAULT_EXPRESSION, scale=1.0):
    """Render a single Luma view and return a cropped RGBA PIL Image."""
    surface = draw_luma(expression=expression, facing=facing, scale=scale)
    img = to_pil_rgba(surface)
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img


def _apply_back_treatment(img):
    """Apply shadow overlay to indicate BACK view — darkened, desaturated."""
    # Darken to shadow tone
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.65)
    # Slight desaturation
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.5)
    return img


def build_turnaround():
    """Build the 4-view Luma turnaround sheet."""
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), CANVAS_BG)
    draw = ImageDraw.Draw(canvas)

    # Panel backgrounds
    for v in range(N_VIEWS):
        x0 = v * VIEW_W
        x1 = (v + 1) * VIEW_W
        bg = PANEL_BG_A if v % 2 == 0 else PANEL_BG_B
        draw.rectangle([x0, HEADER_H, x1, CANVAS_H - LABEL_H], fill=bg)

    # Panel dividers
    for v in range(1, N_VIEWS):
        x = v * VIEW_W
        draw.line([(x, 0), (x, CANVAS_H)], fill=(150, 138, 120), width=1)

    # Render each view
    for v, view_name in enumerate(VIEWS):
        facing = FACING_MAP[view_name]
        char_img = _render_char_view(facing, scale=1.8)

        if view_name == "BACK":
            char_img = _apply_back_treatment(char_img)

        # Fit into panel
        max_h = CHAR_AREA_H - 20
        max_w = VIEW_W - 20
        char_img.thumbnail((max_w, max_h), Image.LANCZOS)

        # Center in panel
        panel_cx = v * VIEW_W + VIEW_W // 2
        x_off = panel_cx - char_img.width // 2
        y_off = HEADER_H + (CHAR_AREA_H - char_img.height) // 2
        canvas.paste(char_img, (x_off, y_off), char_img)

        # Ground shadow
        shadow_cy = y_off + char_img.height - 2
        draw = ImageDraw.Draw(canvas)
        draw.ellipse([panel_cx - 50, shadow_cy,
                      panel_cx + 50, shadow_cy + 8], fill=SHADOW_COL)

    # ── Header ────────────────────────────────────────────────────────────
    draw = ImageDraw.Draw(canvas)
    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
        font_sub = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = font_title
        font_sub = font_title

    title = "LUMA — Character Turnaround v005  |  Luma & the Glitchkin  |  Cycle 54 / Rin Yamamoto"
    sub = "v005: Canonical char_luma.py renderer  |  4 views  |  3.2 heads"
    draw.text((14, 5), title, fill=LABEL_COL, font=font_title)
    draw.text((14, 24), sub, fill=(120, 100, 80), font=font_sub)

    # ── View labels ───────────────────────────────────────────────────────
    for v, label in enumerate(VIEWS):
        lx = v * VIEW_W + VIEW_W // 2
        ly = CANVAS_H - LABEL_H + 6
        try:
            lb = draw.textbbox((0, 0), label, font=font_label)
            lw = lb[2] - lb[0]
            draw.text((lx - lw // 2, ly), label, fill=LABEL_COL, font=font_label)
        except Exception:
            draw.text((lx - 20, ly), label, fill=LABEL_COL)

    return canvas


def main():
    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "characters", "main", "turnarounds"
    )
    os.makedirs(out_dir, exist_ok=True)

    img = build_turnaround()
    img.thumbnail((1280, 1280), Image.LANCZOS)
    out_path = os.path.join(out_dir, "LTG_CHAR_luma_turnaround.png")
    img.save(out_path)
    print(f"Saved: {out_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}px")
    print("  v005: Canonical char_luma.py renderer — 4 views (FRONT, RIGHT, LEFT, BACK)")


if __name__ == "__main__":
    main()
