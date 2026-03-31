#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_glitch_turnaround.py
Glitch — 4-View Character Turnaround
"Luma & the Glitchkin" — Cycle 24 / Maya Santos

Character rendering: uses canonical LTG_TOOL_char_glitch.draw_glitch().
4 views: FRONT, 3/4, SIDE, BACK — each rendered via the canonical module
with the appropriate facing parameter.

Canvas: 1600x700 (4 panels x 400w, single header bar)
Output: output/characters/main/turnarounds/LTG_CHAR_glitch_turnaround.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os
import sys

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

import numpy as np
from LTG_TOOL_char_glitch import draw_glitch, draw_glitch_to_pil
from LTG_TOOL_cairo_primitives import to_pil_rgba

# ── Palette ────────────────────────────────────────────────────────────────────
CORRUPT_AMB    = (255, 140,   0)
VOID_BLACK     = ( 10,  10,  20)
LINE           = VOID_BLACK
CANVAS_BG      = ( 16,  14,  24)
PANEL_BG       = ( 20,  16,  28)
HEADER_BG      = ( 12,  10,  20)
LABEL_COL      = CORRUPT_AMB
HU_LINE_COL    = ( 80,  50,  80)

CANVAS_W = 1600
CANVAS_H = 700
HEADER_H = 52
LABEL_H  = 32
VIEWS    = ["FRONT", "3/4", "SIDE", "BACK"]
N_VIEWS  = 4
PANEL_W  = CANVAS_W // N_VIEWS   # 400
PANEL_H  = CANVAS_H - HEADER_H - LABEL_H   # 616

SCALE    = 2  # internal 2x render, downsample to 1x at end


def render_view_from_canonical(view_idx, panel_w, panel_h):
    """Render a single Glitch view using the canonical char_glitch renderer.

    Returns a PIL RGBA image sized to panel_w x panel_h.
    """
    view = VIEWS[view_idx]

    # Map turnaround views to canonical facing parameter
    facing_map = {
        "FRONT": "front",
        "3/4":   "right",
        "SIDE":  "right",
        "BACK":  "front",  # back view uses front facing (rendered as back in canonical)
    }
    facing = facing_map.get(view, "front")

    # Render character at appropriate scale
    char_scale = 1.8 if SCALE == 2 else 1.0
    surface = draw_glitch(expression="neutral", scale=char_scale, facing=facing)
    char_pil = to_pil_rgba(surface)

    # Crop to bounding box
    bbox = char_pil.getbbox()
    if bbox:
        char_pil = char_pil.crop(bbox)

    # Scale to fit in panel (leave margin)
    max_h = int(panel_h * 0.65)
    max_w = int(panel_w * 0.60)
    if char_pil.height > 0 and char_pil.width > 0:
        scale_factor = min(max_h / char_pil.height, max_w / char_pil.width)
        new_w = max(1, int(char_pil.width * scale_factor))
        new_h = max(1, int(char_pil.height * scale_factor))
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)

    # Create panel image
    panel = Image.new("RGBA", (panel_w, panel_h), PANEL_BG + (255,))
    # Center character in panel
    cx = (panel_w - char_pil.width) // 2
    cy = int(panel_h * 0.50) - char_pil.height // 2
    panel.paste(char_pil, (cx, cy), char_pil)

    return panel


def build_turnaround():
    """Render 4-view turnaround at 2x, downsample to 1x."""
    W2 = CANVAS_W * SCALE
    H2 = CANVAS_H * SCALE
    PW2 = PANEL_W * SCALE
    PH2 = PANEL_H * SCALE
    HEADER_H2 = HEADER_H * SCALE
    LABEL_H2  = LABEL_H * SCALE

    img = Image.new("RGB", (W2, H2), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22 * SCALE)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10 * SCALE)
        font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 7 * SCALE)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_small = font_label

    # Header bar
    draw.rectangle([0, 0, W2, HEADER_H2], fill=HEADER_BG)
    title = "GLITCH — Character Turnaround v003  [char_glitch canonical]"
    try:
        tb = draw.textbbox((0, 0), title, font=font_title)
        tw = tb[2] - tb[0]; th = tb[3] - tb[1]
    except Exception:
        tw, th = len(title) * 14 * SCALE, 22 * SCALE
    draw.text(((W2 - tw) // 2, (HEADER_H2 - th) // 2),
              title, fill=CORRUPT_AMB, font=font_title)

    sub = "Antagonist  |  GL-07 Corrupt Amber  |  Cycle 24  |  4-View  |  Canonical char_glitch renderer"
    try:
        sb = draw.textbbox((0, 0), sub, font=font_small)
        sw = sb[2] - sb[0]
        draw.text(((W2 - sw) // 2, HEADER_H2 - 14 * SCALE),
                  sub, fill=(100, 60, 30), font=font_small)
    except Exception:
        pass

    # Render and paste each view panel
    for vi, view in enumerate(VIEWS):
        px = vi * PW2
        py = HEADER_H2

        # Render character view using canonical renderer
        panel_img = render_view_from_canonical(vi, PW2, PH2)
        # Convert to RGB for pasting
        panel_rgb = Image.new("RGB", panel_img.size, PANEL_BG)
        panel_rgb.paste(panel_img, mask=panel_img.split()[3] if panel_img.mode == "RGBA" else None)
        img.paste(panel_rgb, (px, py))

        # Panel border
        draw = ImageDraw.Draw(img)
        draw.rectangle([px, py, px + PW2, py + PH2 - 1],
                       outline=(40, 28, 50), width=1)

        # HU ruler line
        ru_x = px + PW2 - 18 * SCALE
        char_top_y = py + int(PH2 * 0.18)
        char_bot_y = py + int(PH2 * 0.82)
        draw.line([(ru_x, char_top_y), (ru_x, char_bot_y)],
                  fill=HU_LINE_COL, width=1)
        draw.line([(ru_x - 4 * SCALE, char_top_y),
                   (ru_x + 4 * SCALE, char_top_y)],
                  fill=HU_LINE_COL, width=1)
        draw.line([(ru_x - 4 * SCALE, char_bot_y),
                   (ru_x + 4 * SCALE, char_bot_y)],
                  fill=HU_LINE_COL, width=1)

        # View label in bottom bar
        label_y = py + PH2 + 6 * SCALE
        try:
            lb = draw.textbbox((0, 0), view, font=font_label)
            lw = lb[2] - lb[0]
        except Exception:
            lw = len(view) * 8 * SCALE
        draw.text((px + (PW2 - lw) // 2, label_y),
                  view, fill=LABEL_COL, font=font_label)

    # Bottom label bar background
    label_bar_y = HEADER_H2 + PH2
    draw.rectangle([0, label_bar_y, W2, H2], fill=HEADER_BG)
    # Re-draw view labels on top of bar
    for vi, view in enumerate(VIEWS):
        px = vi * PW2
        label_y = label_bar_y + 6 * SCALE
        try:
            lb = draw.textbbox((0, 0), view, font=font_label)
            lw = lb[2] - lb[0]
        except Exception:
            lw = len(view) * 8 * SCALE
        draw.text((px + (PW2 - lw) // 2, label_y),
                  view, fill=LABEL_COL, font=font_label)

    # Downsample
    img_out = img.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)
    return img_out


def main():
    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "characters", "main", "turnarounds"
    )
    os.makedirs(out_dir, exist_ok=True)

    turnaround = build_turnaround()
    out_path = os.path.join(out_dir, "LTG_CHAR_glitch_turnaround.png")
    turnaround.save(out_path)
    print(f"Saved: {out_path}")
    print(f"  Size: {turnaround.size[0]}x{turnaround.size[1]}px")
    print("  Views: FRONT, 3/4, SIDE, BACK")
    print("  v003: Migrated to canonical char_glitch renderer")


if __name__ == "__main__":
    main()
