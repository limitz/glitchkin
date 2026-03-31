#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_luma_canonical_test.py — Luma Canonical Expression Test Sheet v1.0.0
"Luma & the Glitchkin" — Cycle 61 / Maya Santos

PURPOSE:
  7-expression test sheet using draw_luma() with pose_mode="front".
  Reflects current canonical renderer state (v1.4.0+).
  Layout: 4 top row + 3 bottom row (7 total), with expression labels.

OUTPUT:
  output/characters/main/LTG_CHAR_luma_canonical_test.png (1280px max)

Dependencies: pycairo, Pillow, LTG_TOOL_char_luma
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from PIL import Image, ImageDraw, ImageFont
from LTG_TOOL_char_luma import draw_luma, cairo_surface_to_pil, EXPRESSIONS

__version__ = "1.0.0"
__author__ = "Maya Santos"
__cycle__ = 61

# ── Layout ────────────────────────────────────────────────────────────────────
PANEL_W = 280
PANEL_H = 380
LABEL_H = 28
COLS_ROW1 = 4
COLS_ROW2 = 3
PADDING = 8
SHEET_W = COLS_ROW1 * PANEL_W + (COLS_ROW1 + 1) * PADDING
SHEET_H = 2 * (PANEL_H + LABEL_H) + 3 * PADDING + 48  # +48 for title
BG_COLOR = (240, 236, 228)
LABEL_BG = (60, 48, 36)
LABEL_FG = (240, 230, 210)
TITLE_COL = (59, 40, 32)


def generate_sheet():
    sheet = Image.new("RGB", (SHEET_W, SHEET_H), BG_COLOR)
    draw = ImageDraw.Draw(sheet)

    # Title
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()

    draw.text((PADDING, 10), "LUMA — Canonical Expression Test (Front View) v1.4.0",
              fill=TITLE_COL, font=font_title)

    for idx, expr in enumerate(EXPRESSIONS):
        row = 0 if idx < COLS_ROW1 else 1
        col = idx if idx < COLS_ROW1 else idx - COLS_ROW1

        # Center the bottom row
        if row == 1:
            row2_total_w = COLS_ROW2 * PANEL_W + (COLS_ROW2 - 1) * PADDING
            x_offset = (SHEET_W - row2_total_w) // 2
            px = x_offset + col * (PANEL_W + PADDING)
        else:
            px = PADDING + col * (PANEL_W + PADDING)

        py = 48 + PADDING + row * (PANEL_H + LABEL_H + PADDING)

        # Render character
        surf = draw_luma(expression=expr, pose_mode="front", scale=1.0)
        char_img = cairo_surface_to_pil(surf)

        # Scale to fit panel, maintain aspect ratio
        char_img.thumbnail((PANEL_W, PANEL_H - 10), Image.LANCZOS)

        # Paste centered in panel
        paste_x = px + (PANEL_W - char_img.width) // 2
        paste_y = py + (PANEL_H - char_img.height) // 2 - 5

        # White panel background
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], fill=(252, 248, 240), outline=(180, 160, 130), width=1)

        if char_img.mode == "RGBA":
            sheet.paste(char_img, (paste_x, paste_y), char_img)
        else:
            sheet.paste(char_img, (paste_x, paste_y))

        # Label
        label_y = py + PANEL_H
        draw.rectangle([px, label_y, px + PANEL_W, label_y + LABEL_H], fill=LABEL_BG)
        # Center label text
        try:
            bbox = font_label.getbbox(expr)
            text_w = bbox[2] - bbox[0]
        except Exception:
            text_w = len(expr) * 7
        lx = px + (PANEL_W - text_w) // 2
        draw.text((lx, label_y + 6), expr, fill=LABEL_FG, font=font_label)

    # Apply size rule: <= 1280px
    sheet.thumbnail((1280, 1280), Image.LANCZOS)
    return sheet


if __name__ == "__main__":
    out_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "characters", "main", "LTG_CHAR_luma_canonical_test.png"
    )
    sheet = generate_sheet()
    sheet.save(out_path)
    print(f"Saved: {out_path}")
    print(f"  Size: {sheet.width}x{sheet.height}px")
    print(f"  {len(EXPRESSIONS)} expressions — front view — v1.4.0 renderer")
