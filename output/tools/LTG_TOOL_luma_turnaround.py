#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_luma_turnaround.py
Luma — 5-View Character Turnaround v006
"Luma & the Glitchkin" — Cycle 54 / Maya Santos

v006 UPDATE (C54 — True multi-view turnaround):
  Uses char_luma.py v1.1.0 pose_mode parameter for genuine multi-view rendering.
  All 5 views are now visually distinct — no darkened copies or mirror flips.
  - FRONT: Full frontal, both eyes visible, symmetric near-symmetric body
  - 3/4:   3/4 angle, near eye dominant, far eye foreshortened
  - SIDE:  Side-facing view (canonical right-facing)
  - SIDE-L: Mirror of side (left-facing)
  - BACK:  Rear view, hair from behind, no face, hoodie back, feet visible

  Body connectivity fixes applied in char_luma.py v1.1.0:
  - Legs now overlap into torso bottom (no gap at junction)
  - Hip bridge shape unifies torso/leg boundary
  - Arms drawn as unified silhouettes (single outline per arm)

5 views: FRONT, 3/4, SIDE, SIDE-L, BACK
Canvas: 1280x560 (within 1280px limit)

Output: output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png
"""

import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from LTG_TOOL_char_luma import draw_luma, EXPRESSIONS, cairo_surface_to_pil

from PIL import Image, ImageDraw, ImageFont

# ── Layout ────────────────────────────────────────────────────────────────────
CANVAS_W = 1280
CANVAS_H = 560
# 5 views
VIEWS = ["FRONT", "3/4", "SIDE", "SIDE-L", "BACK"]
N_VIEWS = 5
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

# View spec: (pose_mode, facing) — all visually distinct
VIEW_SPEC = {
    "FRONT":  ("front",         "right"),
    "3/4":    ("threequarter",  "right"),
    "SIDE":   ("side",          "right"),
    "SIDE-L": ("side",          "left"),
    "BACK":   ("back",          "right"),
}

DEFAULT_EXPRESSION = "CURIOUS"


def _render_char_view(view_name, expression=DEFAULT_EXPRESSION, scale=1.0):
    """Render a single Luma view using the appropriate pose_mode and return a cropped RGBA PIL Image."""
    pose_mode, facing = VIEW_SPEC[view_name]
    surface = draw_luma(expression=expression, facing=facing, scale=scale, pose_mode=pose_mode)
    img = cairo_surface_to_pil(surface)
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img


def build_turnaround():
    """Build the 5-view Luma turnaround sheet."""
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
        char_img = _render_char_view(view_name, scale=1.6)

        # Fit into panel
        max_h = CHAR_AREA_H - 20
        max_w = VIEW_W - 16
        char_img.thumbnail((max_w, max_h), Image.LANCZOS)

        # Center in panel
        panel_cx = v * VIEW_W + VIEW_W // 2
        x_off = panel_cx - char_img.width // 2
        y_off = HEADER_H + (CHAR_AREA_H - char_img.height) // 2
        canvas.paste(char_img, (x_off, y_off), char_img)

        # Ground shadow
        shadow_cy = y_off + char_img.height - 2
        draw = ImageDraw.Draw(canvas)
        draw.ellipse([panel_cx - 42, shadow_cy,
                      panel_cx + 42, shadow_cy + 7], fill=SHADOW_COL)

    # ── Header ────────────────────────────────────────────────────────────
    draw = ImageDraw.Draw(canvas)
    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
        font_sub = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = font_title
        font_sub = font_title

    title = "LUMA — Character Turnaround v006  |  Luma & the Glitchkin  |  Cycle 54 / Maya Santos"
    sub = "v006: True multi-view (front/3q/side/back) via pose_mode — body connectivity fixes — 3.2 heads"
    draw.text((14, 5), title, fill=LABEL_COL, font=font_title)
    draw.text((14, 26), sub, fill=(120, 100, 80), font=font_sub)

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
    print("  v006: 5 views (FRONT, 3/4, SIDE, SIDE-L, BACK) — all visually distinct")


if __name__ == "__main__":
    main()
