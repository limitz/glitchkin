#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P20_cairo.py
Cold Open Panel P20 — MED WIDE — Names Exchanged / First Quiet
Diego Vargas, Storyboard Artist — Cycle 52

PYCAIRO CHARACTER MIGRATION: Same composition as C47 P20.
Both Luma (sitting, notebook) and Byte (hovering, wary) rendered via sb_char_draw.
Negative space ~25% (closer than P17's 40%).

Output: output/storyboards/panels/LTG_SB_cold_open_P20.png
"""

import math
import os
import sys
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path

from PIL import Image, ImageDraw, ImageFont
import numpy as np

from LTG_TOOL_cairo_primitives import (
    create_surface, to_pil_rgba, set_color, fill_background,
    draw_ellipse, stroke_path, draw_smooth_polygon, draw_tapered_stroke,
)
from LTG_TOOL_sb_char_draw import draw_luma_sb, draw_byte_sb

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P20.png")
os.makedirs(str(PANELS_DIR), exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72
DRAW_H    = PH - CAPTION_H  # 528

# ── Palette ──────────────────────────────────────────────────────────────────
WARM_CREAM    = (250, 240, 220)
SUNLIT_AMB    = (212, 146, 58)
WALL_WARM     = (190, 170, 138)
FLOOR_WARM    = (155, 128, 92)
FLOOR_GRAIN   = (130, 108, 76)
VOID_BLACK    = (10, 10, 20)
ELEC_CYAN     = (0, 212, 232)
ELEC_CYAN_DIM = (0, 100, 120)
HOT_MAGENTA   = (232, 0, 152)
CRT_BG        = (32, 42, 32)
CRT_STATIC    = (56, 70, 56)
CRT_BEZEL     = (50, 45, 40)
BOOKSHELF     = (110, 82, 52)
BOOK_COLORS   = [(140, 52, 38), (48, 88, 120), (168, 128, 42), (68, 108, 68)]
BG_CAPTION    = (12, 8, 6)
TEXT_SHOT     = (232, 224, 204)
TEXT_DESC     = (155, 148, 122)
TEXT_META     = (88, 82, 66)
ARC_COLOR     = ELEC_CYAN
ANN_COLOR     = (220, 200, 80)
ANN_CYAN      = (0, 180, 210)
ANN_DIM       = (80, 90, 100)

RNG = random.Random(2020)


def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def add_glow(img, cx, cy, r_max, color_rgb, steps=6, max_alpha=50):
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_panel():
    img  = Image.new('RGB', (PW, PH), WALL_WARM)
    draw = ImageDraw.Draw(img)

    wall_h = int(DRAW_H * 0.38)
    floor_y = wall_h

    # Wall gradient warm left to cool right
    for x in range(PW):
        t = x / PW
        c = lerp_color(WALL_WARM, (140, 155, 155), t * 0.45)
        draw.line([(x, 0), (x, wall_h)], fill=c)

    # Floor
    for x in range(PW):
        t = x / PW
        c = lerp_color(FLOOR_WARM, (125, 132, 128), t * 0.35)
        draw.line([(x, floor_y), (x, DRAW_H)], fill=c)
    for py in range(floor_y, DRAW_H, 24):
        draw.line([(0, py), (PW, py)], fill=FLOOR_GRAIN, width=1)

    # Bookshelf BG left
    shelf_x, shelf_y = 10, int(DRAW_H * 0.02)
    shelf_w, shelf_h = int(PW * 0.18), int(DRAW_H * 0.34)
    draw.rectangle([shelf_x, shelf_y, shelf_x + shelf_w, shelf_y + shelf_h], fill=BOOKSHELF)
    for si in range(3):
        sy = shelf_y + int(shelf_h * (si + 1) / 4)
        draw.line([(shelf_x, sy), (shelf_x + shelf_w, sy)], fill=(90, 65, 40), width=2)
        for bi in range(4):
            bx = shelf_x + 8 + bi * int(shelf_w / 5)
            bw = RNG.randint(10, 16)
            bh = int(shelf_h / 4) - 8
            bc = BOOK_COLORS[RNG.randint(0, 3)]
            draw.rectangle([bx, sy - bh, bx + bw, sy - 2], fill=bc)

    # CRT monitors BG right
    for mx, my, mw, mh in [
        (int(PW * 0.72), int(DRAW_H * 0.04), int(PW * 0.14), int(DRAW_H * 0.22)),
        (int(PW * 0.88), int(DRAW_H * 0.08), int(PW * 0.10), int(DRAW_H * 0.18)),
    ]:
        draw.rectangle([mx, my, mx + mw, my + mh], fill=CRT_BEZEL)
        sp = 5
        draw.rectangle([mx + sp, my + sp, mx + mw - sp, my + mh - sp], fill=CRT_BG)
        for sy in range(my + sp + 1, my + mh - sp, 3):
            draw.line([(mx + sp, sy), (mx + mw - sp, sy)], fill=CRT_STATIC, width=1)

    # Warm lamp glow left
    add_glow(img, -20, int(DRAW_H * 0.20), int(PW * 0.40),
             SUNLIT_AMB, steps=8, max_alpha=16)
    draw = ImageDraw.Draw(img)  # W004

    # ── PYCAIRO CHARACTERS ───────────────────────────────────────────────────
    char_surface, char_ctx, _, _ = create_surface(PW, DRAW_H)

    luma_floor_y = floor_y + int((DRAW_H - floor_y) * 0.82)

    # Luma sitting camera-left (notebook in lap — prop continuity from P18)
    luma_cx = int(PW * 0.28)
    luma_info = draw_luma_sb(
        char_ctx,
        cx=luma_cx,
        floor_y=luma_floor_y,
        char_h=140,
        pose="sitting",
        lean_deg=2.0,
        expression="neutral",
        facing="right",
        seed=2020,
    )

    # Byte hovering camera-right at Luma's eye level (concession)
    byte_cx = int(PW * 0.72)
    byte_cy = luma_info["head_cy"]  # Eye-level

    byte_info = draw_byte_sb(
        char_ctx,
        cx=byte_cx,
        cy=byte_cy,
        body_h=75,
        expression="grumpy",  # WARY ACCEPTANCE
        facing="left",
        lean_deg=1.0,
        hovering=True,
        seed=2021,
    )

    # Composite
    char_pil = to_pil_rgba(char_surface)
    full_char = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    full_char.paste(char_pil, (0, 0))
    base_rgba = img.convert('RGBA')
    composited = Image.alpha_composite(base_rgba, full_char)
    img = composited.convert('RGB')
    draw = ImageDraw.Draw(img)  # W004

    # Cyan glow from Byte
    add_glow(img, byte_cx, byte_cy, 90, ELEC_CYAN, steps=6, max_alpha=22)
    draw = ImageDraw.Draw(img)  # W004

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann   = load_font(9)
    font_ann_b = load_font(9, bold=True)
    font_sm    = load_font(8)

    draw.text((8, 8), 'MED WIDE  |  TWO-SHOT  |  NAMES EXCHANGED  |  FIRST QUIET',
              font=font_ann, fill=ANN_COLOR)

    # Negative space (~25% — closer than P17's 40%)
    gap_x = (luma_cx + byte_cx) // 2
    gap_y = int(DRAW_H * 0.75)
    draw.text((gap_x - 28, gap_y), "~25% GAP", font=font_sm, fill=(100, 96, 88))
    draw.text((gap_x - 30, gap_y + 10), "(closer than P17)", font=font_sm, fill=(80, 76, 70))

    # Character labels
    draw.text((luma_cx - 20, luma_info["head_cy"] - luma_info["head_r"] - 30),
              "LUMA", font=font_ann_b, fill=ANN_COLOR)
    draw.text((luma_cx - 25, luma_info["head_cy"] - luma_info["head_r"] - 20),
              "(notebook in lap)", font=font_sm, fill=(120, 110, 90))

    draw.text((byte_cx - 10, byte_info["face_cy"] - byte_info["face_r"] - 30),
              "BYTE", font=font_ann_b, fill=ANN_CYAN)
    draw.text((byte_cx - 35, byte_info["face_cy"] - byte_info["face_r"] - 20),
              "(wary acceptance)", font=font_sm, fill=ANN_DIM)

    # Depth temperature
    draw.text((int(PW * 0.08), DRAW_H - 16),
              "WARM (Luma zone)", font=font_sm, fill=(180, 130, 60))
    draw.text((int(PW * 0.68), DRAW_H - 16),
              "COOL (Byte zone)", font=font_sm, fill=ELEC_CYAN_DIM)

    # ── Three-tier caption bar ───────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11)
    font_t3   = load_font(9)
    font_meta = load_font(8)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    draw.text((10, DRAW_H + 4),
              "P20  |  MED WIDE  |  TWO-SHOT  |  NAMES EXCHANGED",
              font=font_t1, fill=TEXT_SHOT)
    draw.text((PW - 260, DRAW_H + 5),
              "ARC: CURIOUS / FIRST ENCOUNTER", font=font_t2, fill=ELEC_CYAN)
    draw.text((10, DRAW_H + 22),
              "First quiet after naming. Luma sitting, notebook in lap. Byte hovering at her level.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "Negative space ~25% (CLOSER than P17). Wary acceptance. New normal forming.",
              font=font_t3, fill=(120, 112, 90))
    draw.text((PW - 310, DRAW_H + 56),
              "LTG_SB_cold_open_P20  /  Diego Vargas  /  C52 (pycairo chars)",
              font=font_meta, fill=TEXT_META)

    # Arc border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(str(OUTPUT_PATH), "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return str(OUTPUT_PATH)


if __name__ == "__main__":
    draw_panel()
