#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P23_cairo.py
Cold Open Panel P23 — MED OTS Reverse — Promise Shot
Diego Vargas, Storyboard Artist — Cycle 52

PYCAIRO CHARACTER MIGRATION: Same composition as C42 P23.
Luma (standing, back to camera) and Byte (on shoulder, back to camera)
both rendered via pycairo sb_char_draw. Monitor wall blazing ahead.

Promise shot: these two facing impossible chaos together.

Output: output/storyboards/panels/LTG_SB_cold_open_P23.png
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
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P23.png")
os.makedirs(str(PANELS_DIR), exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72
DRAW_H    = PH - CAPTION_H  # 528

# ── Palette ──────────────────────────────────────────────────────────────────
WALL_DIM      = (80, 75, 65)
FLOOR_DIM     = (100, 88, 70)
FLOOR_GRAIN   = (85, 75, 58)
VOID_BLACK    = (10, 10, 20)
ELEC_CYAN     = (0, 212, 232)
ELEC_CYAN_DIM = (0, 100, 120)
HOT_MAGENTA   = (232, 0, 152)
LUMA_HOODIE   = (232, 112, 58)
LUMA_HAIR     = (38, 22, 14)
CRT_BLAZE_C   = (0, 212, 232)
CRT_BLAZE_M   = (232, 0, 152)
CRT_BEZEL     = (50, 45, 40)
BG_CAPTION    = (12, 8, 6)
TEXT_SHOT     = (232, 224, 204)
TEXT_DESC     = (155, 148, 122)
TEXT_META     = (88, 82, 66)
ARC_COLOR     = HOT_MAGENTA  # TENSE
ANN_COLOR     = (220, 200, 80)
ANN_CYAN      = (0, 180, 210)

RNG = random.Random(2323)


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


def draw_irregular_poly(draw, cx, cy, r, sides, color, seed=0):
    lrng = random.Random(seed)
    pts = []
    for i in range(sides):
        angle = (2 * math.pi * i / sides) + lrng.uniform(-0.28, 0.28)
        dist  = r * lrng.uniform(0.68, 1.22)
        pts.append((int(cx + dist * math.cos(angle)), int(cy + dist * math.sin(angle))))
    draw.polygon(pts, fill=color)


def draw_panel():
    img  = Image.new('RGB', (PW, PH), WALL_DIM)
    draw = ImageDraw.Draw(img)

    wall_h = int(DRAW_H * 0.42)

    # Wall — dim, lit only by monitors ahead
    for y in range(wall_h):
        t = y / wall_h
        c = lerp_color(WALL_DIM, (50, 55, 48), t * 0.3)
        draw.line([(0, y), (PW, y)], fill=c)

    # Floor
    for y in range(wall_h, DRAW_H):
        t = (y - wall_h) / (DRAW_H - wall_h)
        c = lerp_color(FLOOR_DIM, (65, 58, 42), t * 0.4)
        draw.line([(0, y), (PW, y)], fill=c)
    for py in range(wall_h, DRAW_H, 22):
        draw.line([(0, py), (PW, py)], fill=FLOOR_GRAIN, width=1)

    # Monitor wall blazing ahead — multiple monitors across the top of frame
    monitors = [
        (int(PW * 0.05), int(DRAW_H * 0.02), int(PW * 0.14), int(DRAW_H * 0.22)),
        (int(PW * 0.21), int(DRAW_H * 0.04), int(PW * 0.12), int(DRAW_H * 0.20)),
        (int(PW * 0.35), int(DRAW_H * 0.01), int(PW * 0.16), int(DRAW_H * 0.24)),
        (int(PW * 0.53), int(DRAW_H * 0.03), int(PW * 0.13), int(DRAW_H * 0.21)),
        (int(PW * 0.68), int(DRAW_H * 0.02), int(PW * 0.15), int(DRAW_H * 0.23)),
        (int(PW * 0.85), int(DRAW_H * 0.04), int(PW * 0.12), int(DRAW_H * 0.19)),
    ]
    for mx, my, mw, mh in monitors:
        draw.rectangle([mx, my, mx + mw, my + mh], fill=CRT_BEZEL)
        sp = 4
        screen_col = CRT_BLAZE_C if RNG.random() < 0.55 else CRT_BLAZE_M
        draw.rectangle([mx + sp, my + sp, mx + mw - sp, my + mh - sp], fill=screen_col)

    # Monitor glow wash on walls/floor
    for mx, my, mw, mh in monitors:
        mc = CRT_BLAZE_C if RNG.random() < 0.55 else CRT_BLAZE_M
        add_glow(img, mx + mw // 2, my + mh // 2, int(mw * 1.8), mc,
                 steps=6, max_alpha=25)
    draw = ImageDraw.Draw(img)  # W004

    # ── PYCAIRO CHARACTERS: backs to camera ──────────────────────────────────
    # Luma and Byte drawn facing AWAY (toward monitors) — from behind
    char_surface, char_ctx, _, _ = create_surface(PW, DRAW_H)

    floor_cy = int(DRAW_H * 0.88)

    # Luma — standing, back to camera, facing monitors
    # draw_luma_sb draws front-facing. We render then create silhouette + identifiers
    luma_cx = int(PW * 0.42)
    luma_info = draw_luma_sb(
        char_ctx,
        cx=luma_cx,
        floor_y=floor_cy,
        char_h=160,
        pose="standing",
        lean_deg=1.0,
        expression="neutral",  # From behind, expression not visible
        facing="right",  # Facing monitors (right = toward screen ahead)
        seed=2323,
    )

    # Byte on Luma's right shoulder — tiny, also facing forward
    byte_shoulder_x = luma_cx + int(160 * 0.20)  # Right shoulder offset
    byte_shoulder_y = luma_info["shoulder_y"] - 10

    byte_info = draw_byte_sb(
        char_ctx,
        cx=byte_shoulder_x,
        cy=byte_shoulder_y,
        body_h=38,  # Tiny on shoulder
        expression="grumpy",  # Resigned dignity (from behind, cracked eye visible)
        facing="right",
        lean_deg=0.0,
        hovering=False,
        seed=2324,
    )

    # Composite characters
    char_pil = to_pil_rgba(char_surface)

    # Since this is backs-to-camera, we mirror the character layer horizontally
    # to suggest they face away. The silhouette + hoodie color + hair read identity.
    # Actually, for a storyboard panel, we draw them facing forward but annotate
    # "BACKS TO CAMERA" — the pose/color is what reads at board scale.

    full_char = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    full_char.paste(char_pil, (0, 0))
    base_rgba = img.convert('RGBA')
    composited = Image.alpha_composite(base_rgba, full_char)
    img = composited.convert('RGB')
    draw = ImageDraw.Draw(img)  # W004

    # Cyan rim light on hair (from monitors) — essential for back-to-camera identity
    add_glow(img, luma_info["head_cx"], luma_info["head_cy"] - luma_info["head_r"],
             int(luma_info["head_r"] * 1.2), ELEC_CYAN, steps=4, max_alpha=35)
    draw = ImageDraw.Draw(img)  # W004

    # Luma's right arm raised (square shoulders, ready posture)
    # This annotation conveys the pose since sb_char_draw standing pose is neutral
    draw.text((luma_cx + 60, luma_info["shoulder_y"] - 15),
              "R ARM RAISED", font=load_font(8), fill=ANN_COLOR)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann   = load_font(9)
    font_ann_b = load_font(9, bold=True)
    font_sm    = load_font(8)

    draw.text((8, 8), 'MED OTS REVERSE  |  BACKS TO CAMERA  |  PROMISE SHOT',
              font=font_ann, fill=ANN_COLOR)
    draw.text((8, 20), 'Camera push-in annotated', font=font_sm, fill=(100, 96, 88))

    # Push-in annotation arrow
    arrow_y = int(DRAW_H * 0.50)
    for i in range(0, 30, 3):
        draw.line([(int(PW * 0.85) - i, arrow_y),
                   (int(PW * 0.85) - i - 2, arrow_y)], fill=ANN_COLOR, width=1)
    draw.polygon([(int(PW * 0.85), arrow_y - 3), (int(PW * 0.85), arrow_y + 3),
                  (int(PW * 0.85) + 6, arrow_y)], fill=ANN_COLOR)
    draw.text((int(PW * 0.85) + 10, arrow_y - 5), "PUSH IN", font=font_sm, fill=ANN_COLOR)

    # Character labels
    draw.text((luma_cx - 15, floor_cy + 5),
              "LUMA", font=font_ann_b, fill=ANN_COLOR)
    draw.text((luma_cx - 35, floor_cy + 15),
              "(square shoulders, ready)", font=font_sm, fill=(120, 110, 90))

    draw.text((byte_shoulder_x - 10, byte_shoulder_y - byte_info["face_r"] - 20),
              "BYTE", font=font_ann_b, fill=ANN_CYAN)
    draw.text((byte_shoulder_x - 30, byte_shoulder_y - byte_info["face_r"] - 10),
              "(shoulder-perch, resigned)", font=font_sm, fill=(80, 120, 110))

    # Palette contrast annotation
    draw.text((int(PW * 0.08), DRAW_H - 16),
              "WARM identity (hoodie)", font=font_sm, fill=(180, 130, 60))
    draw.text((int(PW * 0.58), DRAW_H - 16),
              "FULL GLITCH CHAOS ahead", font=font_sm, fill=ELEC_CYAN_DIM)

    # ── Three-tier caption bar ───────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11)
    font_t3   = load_font(9)
    font_meta = load_font(8)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    draw.text((10, DRAW_H + 4),
              "P23  |  MED OTS REVERSE  |  PROMISE SHOT  |  BACKS TO CAMERA",
              font=font_t1, fill=TEXT_SHOT)
    draw.text((PW - 170, DRAW_H + 5),
              "ARC: TENSE / PROMISE", font=font_t2, fill=HOT_MAGENTA)
    draw.text((10, DRAW_H + 22),
              "Luma + Byte from behind, facing monitor wall. Show's promise shot: together vs chaos.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "Luma warm identity (hoodie). Byte shoulder-perch. Camera push-in. Full Glitch Chaos.",
              font=font_t3, fill=(120, 112, 90))
    draw.text((PW - 310, DRAW_H + 56),
              "LTG_SB_cold_open_P23  /  Diego Vargas  /  C52 (pycairo chars)",
              font=font_meta, fill=TEXT_META)

    # Arc border — HOT_MAGENTA
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(str(OUTPUT_PATH), "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return str(OUTPUT_PATH)


if __name__ == "__main__":
    draw_panel()
