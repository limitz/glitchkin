#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P13_cairo.py
Cold Open Panel P13 — MIRROR COMPOSITION — Commitment / Threshold Beat
Diego Vargas, Storyboard Artist — Cycle 52

PYCAIRO CHARACTER MIGRATION: Same composition as C47 P13.
Both Luma and Byte rendered via pycairo sb_char_draw module.
Luma: standing pose (3/4 toward Byte), Byte: full-frontal with forward lean.
Mirror eye grammar preserved via annotations.

Output: output/storyboards/panels/LTG_SB_cold_open_P13.png
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
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P13.png")
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
LUMA_HOODIE   = (232, 112, 58)
CRT_BG        = (32, 42, 32)
CRT_STATIC    = (56, 70, 56)
CRT_BEZEL     = (50, 45, 40)
ARC_COMMIT    = (60, 200, 140)
BG_CAPTION    = (12, 8, 6)
TEXT_SHOT     = (232, 224, 204)
TEXT_DESC     = (155, 148, 122)
TEXT_META     = (88, 82, 66)
ANN_COLOR     = (220, 200, 80)
ANN_CYAN      = (0, 180, 210)
ANN_MAGENTA   = (200, 60, 130)
ANN_DIM       = (80, 90, 100)

RNG = random.Random(1313)


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

    # Wall — warm left (Luma), cool right (Byte)
    for x in range(PW):
        t = x / PW
        c = lerp_color(WALL_WARM, (140, 155, 155), t * 0.50)
        draw.line([(x, 0), (x, wall_h)], fill=c)

    # Floor
    for x in range(PW):
        t = x / PW
        c = lerp_color(FLOOR_WARM, (120, 130, 125), t * 0.40)
        draw.line([(x, floor_y), (x, DRAW_H)], fill=c)
    for py in range(floor_y, DRAW_H, 24):
        draw.line([(0, py), (PW, py)], fill=FLOOR_GRAIN, width=1)

    # CRT monitor visible camera-right BG
    mon_x, mon_y, mon_w, mon_h = int(PW * 0.78), int(DRAW_H * 0.06), int(PW * 0.18), int(DRAW_H * 0.24)
    draw.rectangle([mon_x, mon_y, mon_x + mon_w, mon_y + mon_h], fill=CRT_BEZEL)
    sp = 6
    draw.rectangle([mon_x + sp, mon_y + sp, mon_x + mon_w - sp, mon_y + mon_h - sp], fill=CRT_BG)
    for _ in range(50):
        sx = RNG.randint(mon_x + sp + 2, mon_x + mon_w - sp - 2)
        sy = RNG.randint(mon_y + sp + 2, mon_y + mon_h - sp - 2)
        draw.point((sx, sy), fill=CRT_STATIC)

    # Warm lamp glow from camera-left
    add_glow(img, -20, int(DRAW_H * 0.20), int(PW * 0.45),
             SUNLIT_AMB, steps=8, max_alpha=18)
    draw = ImageDraw.Draw(img)  # W004

    # ── PYCAIRO CHARACTERS ───────────────────────────────────────────────────
    char_surface, char_ctx, _, _ = create_surface(PW, DRAW_H)

    luma_floor_y = floor_y + int((DRAW_H - floor_y) * 0.82)
    luma_cx = int(PW * 0.28)

    # Luma — standing, facing right toward Byte
    luma_info = draw_luma_sb(
        char_ctx,
        cx=luma_cx,
        floor_y=luma_floor_y,
        char_h=150,
        pose="standing",
        lean_deg=2.0,
        expression="neutral",
        facing="right",
        seed=1313,
    )

    # Byte — camera-right, full-frontal, slight forward lean toward Luma
    byte_cx = int(PW * 0.72)
    byte_cy = luma_info["head_cy"]  # Eye-level with Luma

    byte_info = draw_byte_sb(
        char_ctx,
        cx=byte_cx,
        cy=byte_cy,
        body_h=80,
        expression="still",  # Quiet commitment, not grumpy
        facing="left",
        lean_deg=3.5,  # -3-4 degree forward lean
        hovering=True,
        seed=1314,
    )

    # Composite cairo characters onto PIL background
    char_pil = to_pil_rgba(char_surface)
    full_char = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    full_char.paste(char_pil, (0, 0))
    base_rgba = img.convert('RGBA')
    composited = Image.alpha_composite(base_rgba, full_char)
    img = composited.convert('RGB')
    draw = ImageDraw.Draw(img)  # W004

    # Directional ELEC_CYAN glow from Byte toward Luma
    # Brighter on Luma's side (left side of Byte)
    glow_cx = byte_cx - int(PW * 0.08)
    add_glow(img, glow_cx, byte_cy, 120, ELEC_CYAN, steps=8, max_alpha=28)
    # Dimmer on Byte's far side
    add_glow(img, byte_cx + int(PW * 0.05), byte_cy, 60, ELEC_CYAN, steps=4, max_alpha=12)
    draw = ImageDraw.Draw(img)  # W004

    # ── Mirror gaze annotations ──────────────────────────────────────────────
    font_ann   = load_font(9)
    font_ann_b = load_font(9, bold=True)
    font_sm    = load_font(8)

    # Eye-level guideline
    eye_y = luma_info["head_cy"]
    for dx in range(0, PW, 8):
        draw.line([(dx, eye_y), (dx + 4, eye_y)], fill=(100, 96, 88), width=1)
    draw.text((int(PW * 0.44), eye_y - 14), "EYE-LEVEL", font=font_sm, fill=(100, 96, 88))

    # Mirror gaze arrows — cyan (trust) pointing inward
    # Luma's open eye -> center
    luma_eye_x = luma_info["head_cx"] + int(luma_info["head_r"] * 0.3)
    arrow_len = 40
    for i in range(0, arrow_len, 3):
        alpha_t = 1.0 - i / arrow_len
        draw.line([(luma_eye_x + i, eye_y - 20),
                   (luma_eye_x + i + 2, eye_y - 20)],
                  fill=ANN_CYAN, width=1)
    draw.text((luma_eye_x + 2, eye_y - 32), "TRUST ->", font=font_sm, fill=ANN_CYAN)

    # Byte's organic eye -> center
    byte_eye_x = byte_info["face_cx"] - int(byte_info["face_r"] * 0.3)
    for i in range(0, arrow_len, 3):
        draw.line([(byte_eye_x - i, eye_y - 20),
                   (byte_eye_x - i - 2, eye_y - 20)],
                  fill=ANN_CYAN, width=1)
    draw.text((byte_eye_x - 48, eye_y - 32), "<- TRUST", font=font_sm, fill=ANN_CYAN)

    # Magenta arrows — damage/doubt pointing outward
    draw.text((luma_cx - 55, eye_y + 10), "<- DOUBT", font=font_sm, fill=ANN_MAGENTA)
    draw.text((byte_cx + 20, eye_y + 10), "CRACK ->", font=font_sm, fill=ANN_MAGENTA)

    # Camera note
    draw.text((8, 8), 'MED TWO-SHOT  |  FLAT HORIZON  |  MIRROR COMPOSITION',
              font=font_ann, fill=ANN_COLOR)

    # Negative space annotation
    gap_x = (luma_cx + byte_cx) // 2
    gap_y = int(DRAW_H * 0.75)
    draw.text((gap_x - 30, gap_y), "NEGATIVE SPACE", font=font_sm, fill=(100, 96, 88))
    draw.text((gap_x - 22, gap_y + 10), "(threshold gap)", font=font_sm, fill=(80, 76, 70))

    # Character labels
    draw.text((luma_cx - 15, luma_info["head_cy"] - luma_info["head_r"] - 30),
              "LUMA", font=font_ann_b, fill=ANN_COLOR)
    draw.text((luma_cx - 30, luma_info["head_cy"] - luma_info["head_r"] - 20),
              "(receiving, not yet committed)", font=font_sm, fill=(120, 110, 90))

    draw.text((byte_cx - 10, byte_info["face_cy"] - byte_info["face_r"] - 30),
              "BYTE", font=font_ann_b, fill=ANN_CYAN)
    draw.text((byte_cx - 40, byte_info["face_cy"] - byte_info["face_r"] - 20),
              "(quiet warmth — threshold)", font=font_sm, fill=ANN_DIM)

    # ── Three-tier caption bar ───────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11)
    font_t3   = load_font(9)
    font_meta = load_font(8)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    draw.text((10, DRAW_H + 4),
              "P13  |  MED TWO-SHOT  |  MIRROR COMPOSITION  |  THRESHOLD",
              font=font_t1, fill=TEXT_SHOT)
    draw.text((PW - 240, DRAW_H + 5),
              "ARC: COMMITMENT / THRESHOLD", font=font_t2, fill=ARC_COMMIT)
    draw.text((10, DRAW_H + 22),
              "Luma camera-left, Byte camera-right. Open eyes face center (trust); damaged eyes face out.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "Directional ELEC_CYAN glow (brighter toward Luma). Barely-there warmth arc mouth. Threshold.",
              font=font_t3, fill=(120, 112, 90))
    draw.text((PW - 310, DRAW_H + 56),
              "LTG_SB_cold_open_P13  /  Diego Vargas  /  C52 (pycairo chars)",
              font=font_meta, fill=TEXT_META)

    # Arc border — ARC_COMMIT
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COMMIT, width=4)

    img.thumbnail((1280, 1280))
    img.save(str(OUTPUT_PATH), "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return str(OUTPUT_PATH)


if __name__ == "__main__":
    draw_panel()
