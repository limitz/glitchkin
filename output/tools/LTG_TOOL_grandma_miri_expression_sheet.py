#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_grandma_miri_expression_sheet.py
Grandma Miri Expression Sheet — v009 Thin Wrapper
"Luma & the Glitchkin" — Cycle 54 / Maya Santos

v009 CHANGES (C54 — thin wrapper migration):
  All character drawing logic now lives in LTG_TOOL_char_miri.py (canonical renderer).
  This file handles ONLY sheet layout (3x2 grid), panel backgrounds, labels.
  6 expressions preserved from v008. Elder posture, rounded shoulders, and all
  gesture specs are encoded in the canonical module.

Output: output/characters/main/LTG_CHAR_grandma_miri_expression_sheet.png
"""
from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# ── Tool imports ─────────────────────────────────────────────────────────────
_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

from LTG_TOOL_char_miri import (
    draw_miri, cairo_surface_to_pil, EXPRESSIONS,
)

# ── Palette (sheet-level) ────────────────────────────────────────────────────
LINE        = (59, 40, 32)
CANVAS_BG   = (28, 20, 14)

BG = {
    "WARM":      (248, 232, 210),
    "SKEPTICAL": (210, 218, 208),
    "CONCERNED": (200, 212, 225),
    "SURPRISED": (245, 228, 195),
    "WISE":      (218, 214, 205),
    "KNOWING":   (228, 218, 200),
}

# ── Layout ─────────────────────────────────────────────────────────────────────
TOTAL_W  = 1200
TOTAL_H  = 900
COLS     = 3
ROWS     = 2
PAD      = 20
HEADER   = 58
LABEL_H  = 36
PANEL_W  = (TOTAL_W - PAD * (COLS + 1)) // COLS
PANEL_H  = (TOTAL_H - HEADER - PAD * (ROWS + 1) - LABEL_H * ROWS) // ROWS

MIRI_HEAD_RATIO = 3.2

EXPR_LABELS = {
    "WARM":      "WARM / WELCOMING",
    "SKEPTICAL": "SKEPTICAL / AMUSED",
    "CONCERNED": "CONCERNED",
    "SURPRISED": "SURPRISED / DELIGHTED",
    "WISE":      "WISE / KNOWING",
    "KNOWING":   "KNOWING STILLNESS",
}


def render_panel_miri(expr, panel_w, panel_h):
    """Render a single Miri expression panel using the canonical renderer."""
    # Draw character via canonical module
    surface = draw_miri(expression=expr, scale=1.0)
    char_img = cairo_surface_to_pil(surface)

    # Crop to content
    bbox = char_img.getbbox()
    if bbox:
        char_img = char_img.crop(bbox)

    # Create panel image
    panel = Image.new("RGBA", (panel_w, panel_h), (0, 0, 0, 0))

    # Fit character into panel
    avail_w = panel_w - 10
    avail_h = panel_h - 10
    char_img.thumbnail((avail_w, avail_h), Image.LANCZOS)

    # Center in panel
    cx = (panel_w - char_img.width) // 2
    cy = (panel_h - char_img.height) // 2
    panel.paste(char_img, (cx, cy), char_img)

    return panel


def build_sheet():
    """Build the Grandma Miri expression sheet (3x2 grid)."""
    sheet = Image.new("RGB", (TOTAL_W, TOTAL_H), CANVAS_BG)
    draw  = ImageDraw.Draw(sheet)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        font_sub   = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = font_title
        font_sub   = font_title

    title = "GRANDMA MIRI \u2014 Expression Sheet v009  |  Luma & the Glitchkin"
    sub   = ("Designer: Maya Santos  |  C54 Canonical char_miri  |  "
             f"6 expressions  |  HEAD_RATIO={MIRI_HEAD_RATIO}")
    draw.text((PAD, 10), title, fill=(235, 218, 196), font=font_title)
    draw.text((PAD, 38), sub,   fill=(165, 150, 130), font=font_sub)

    panel_w = PANEL_W - PAD * 2
    panel_h = PANEL_H - PAD

    for idx, expr in enumerate(EXPRESSIONS):
        row        = idx // COLS
        col_in_row = idx % COLS
        px = PAD + col_in_row * (PANEL_W + PAD)
        py = HEADER + PAD + row * (PANEL_H + LABEL_H + PAD)

        bg = BG[expr]
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], fill=bg)
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], outline=LINE, width=2)

        face_img = render_panel_miri(expr, panel_w, panel_h)
        ox = px + PAD
        oy = py + PAD // 2
        sheet.paste(face_img, (ox, oy), face_img)
        draw = ImageDraw.Draw(sheet)

        label    = EXPR_LABELS[expr]
        label_y  = py + PANEL_H + 2
        label_bg = tuple(max(0, int(c * 0.88)) for c in bg)
        draw.rectangle([px, label_y, px + PANEL_W, label_y + LABEL_H], fill=label_bg)
        bbox = draw.textbbox((0, 0), label, font=font_label)
        tw_b = bbox[2] - bbox[0]
        th_b = bbox[3] - bbox[1]
        tx   = px + (PANEL_W - tw_b) // 2
        ty   = label_y + (LABEL_H - th_b) // 2
        draw.text((tx, ty), label, fill=LINE, font=font_label)

    sheet.thumbnail((1280, 1280), Image.LANCZOS)
    return sheet


if __name__ == "__main__":
    out_dir  = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "characters", "main")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_grandma_miri_expression_sheet.png")
    sheet    = build_sheet()
    sheet.save(out_path)
    print(f"Saved: {os.path.abspath(out_path)}")
    print(f"Canvas: {sheet.size[0]}x{sheet.size[1]}")
    print("v009 thin wrapper (Maya Santos C54)")
    print("  Character drawing via canonical char_miri renderer")
    print("  6 expressions: WARM, SKEPTICAL, CONCERNED, SURPRISED, WISE, KNOWING")
