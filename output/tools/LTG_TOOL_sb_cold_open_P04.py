#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P04.py
Cold Open Panel P04 — WIDE INTERIOR — Glitch Bleeds Into Warm Room
Diego Vargas, Storyboard Artist — Cycle 53

Beat: Full tech den revealed. Glitch bleeds into warm room. MCU push-in,
cyan intrusion has directional source point from CRT screen edge toward Luma.
Camera: MCU push-in — Luma mid-chest up, CRT in BG right.

Luma drawn via pycairo (draw_luma_sb standing pose, leaning forward).
Environment is PIL. Glitch pixel trail from screen to Luma.

Output: output/storyboards/panels/LTG_SB_cold_open_P04.png
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
    draw_ellipse, stroke_path, draw_smooth_polygon,
)
from LTG_TOOL_sb_char_draw import draw_luma_sb

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P04.png")
os.makedirs(str(PANELS_DIR), exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72
DRAW_H    = PH - CAPTION_H  # 528

# ── Palette ──────────────────────────────────────────────────────────────────
WARM_CREAM   = (250, 240, 220)
WALL_WARM    = (228, 214, 188)
FLOOR_LIGHT  = (195, 172, 132)
LUMA_HOODIE  = (232, 112, 58)
LUMA_SKIN    = (218, 172, 128)
LUMA_HAIR    = (38, 22, 14)
SUNLIT_AMB   = (212, 146, 58)
ELEC_CYAN    = (0, 212, 232)
ELEC_CYAN_DIM = (0, 140, 160)
HOT_MAGENTA  = (232, 0, 152)
VOID_BLACK   = (10, 10, 20)
CRT_DARK     = (52, 44, 34)
CRT_SCREEN   = (20, 30, 28)
LINE_DARK    = (42, 32, 22)
BG_CAPTION   = (12, 8, 6)
TEXT_SHOT    = (232, 224, 204)
TEXT_ARC     = HOT_MAGENTA  # TENSE arc
TEXT_DESC    = (155, 148, 122)
TEXT_META    = (88, 82, 66)
ARC_COLOR    = HOT_MAGENTA  # TENSE — magenta border
ANN_COLOR    = (180, 158, 108)
ANN_CYAN     = (0, 180, 210)

RNG = random.Random(404)


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


def add_glow(img, cx, cy, r_max, color_rgb, steps=6, max_alpha=50):
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_irregular_poly(draw, cx, cy, r, sides, color, seed=0, outline=None):
    lrng = random.Random(seed)
    pts = []
    for i in range(sides):
        angle = (2 * math.pi * i / sides) + lrng.uniform(-0.3, 0.3)
        dist  = r * lrng.uniform(0.65, 1.0)
        pts.append((cx + dist * math.cos(angle), cy + dist * math.sin(angle)))
    draw.polygon(pts, fill=color, outline=outline)


def draw_arrow(draw, x0, y0, x1, y1, color, width=1):
    draw.line([(x0, y0), (x1, y1)], fill=color, width=width)
    angle = math.atan2(y1 - y0, x1 - x0)
    arr_len = 8
    for da in [2.6, -2.6]:
        ax = x1 - arr_len * math.cos(angle + da)
        ay = y1 - arr_len * math.sin(angle + da)
        draw.line([(x1, y1), (int(ax), int(ay))], fill=color, width=width)


def draw_panel():
    img  = Image.new('RGB', (PW, PH), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # ── Environment ─────────────────────────────────────────────────────────
    floor_y = int(DRAW_H * 0.72)
    draw.rectangle([0, 0, PW, floor_y], fill=WALL_WARM)
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=FLOOR_LIGHT)

    # Warm ambient from left
    add_glow(img, 0, int(DRAW_H * 0.3), 160, SUNLIT_AMB, steps=5, max_alpha=22)
    draw = ImageDraw.Draw(img)  # W004

    # CRT TV (right side, partially in-frame — source of intrusion)
    tv_rx = int(PW * 0.72)
    tv_ty = int(DRAW_H * 0.24)
    tv_w  = int(PW * 0.30)
    tv_h  = int(DRAW_H * 0.42)
    draw.rectangle([tv_rx, tv_ty, tv_rx + tv_w, tv_ty + tv_h],
                   fill=CRT_DARK, outline=(72, 60, 46), width=2)
    draw.rectangle([tv_rx + 6, tv_ty + 6, tv_rx + tv_w - 6, tv_ty + tv_h - 6],
                   fill=CRT_SCREEN)

    # CRT glow — bright, intrusive
    add_glow(img, tv_rx + tv_w // 2, tv_ty + tv_h // 2, 130, ELEC_CYAN,
             steps=8, max_alpha=55)
    draw = ImageDraw.Draw(img)  # W004

    # Cyan glow bleeding rightward into room
    add_glow(img, tv_rx, tv_ty + tv_h // 2, 200, ELEC_CYAN, steps=7, max_alpha=35)
    draw = ImageDraw.Draw(img)  # W004

    # SOURCE PIXELS escaping screen edge (irregular polygons)
    src_rng = random.Random(44)
    for py_off in range(tv_ty + 8, tv_ty + tv_h - 8, 7):
        col = ELEC_CYAN if py_off % 14 < 7 else HOT_MAGENTA
        pr = src_rng.randint(3, 6)
        sides = src_rng.randint(4, 6)
        draw_irregular_poly(draw, tv_rx - 2, py_off, pr, sides, col, seed=py_off * 3)

    # DIRECTIONAL VECTOR: pixel trail from screen toward Luma's face
    luma_face_x = int(PW * 0.38)
    luma_face_y = int(DRAW_H * 0.22)
    src_x = tv_rx
    src_y = tv_ty + tv_h // 2
    trail_rng = random.Random(55)
    vec_steps = 12
    for step in range(vec_steps):
        t = step / (vec_steps - 1)
        trail_px = int(src_x + (luma_face_x - src_x) * t)
        trail_py = int(src_y + (luma_face_y - src_y) * t)
        trail_col = ELEC_CYAN if step % 2 == 0 else HOT_MAGENTA
        trail_r = max(2, int(6 * (1 - t * 0.5)))
        trail_sides = trail_rng.randint(4, 7)
        draw_irregular_poly(draw, trail_px, trail_py, trail_r, trail_sides,
                            trail_col, seed=step * 37 + 55)

    # Direction arrow annotation
    draw_arrow(draw, tv_rx, src_y, luma_face_x + 20, luma_face_y + 20,
               color=ELEC_CYAN_DIM, width=1)

    # ── PYCAIRO CHARACTER: Luma standing, leaning toward CRT ────────────────
    luma_cx    = int(PW * 0.35)
    luma_floor = int(DRAW_H * 0.88)
    luma_ch    = int(DRAW_H * 0.60)  # MCU — larger character

    char_surface, char_ctx, _, _ = create_surface(PW, DRAW_H)

    luma_info = draw_luma_sb(
        char_ctx,
        cx=luma_cx,
        floor_y=luma_floor,
        char_h=luma_ch,
        pose="standing",
        lean_deg=5.0,
        expression="assessing",
        facing="right",
        seed=404,
    )

    # Composite cairo onto PIL
    char_pil = to_pil_rgba(char_surface)
    full_char = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    full_char.paste(char_pil, (0, 0))
    base_rgba = img.convert('RGBA')
    composited = Image.alpha_composite(base_rgba, full_char)
    img = composited.convert('RGB')
    draw = ImageDraw.Draw(img)  # W004

    # Cyan light on Luma's right side (from CRT)
    add_glow(img, luma_info["head_cx"] + int(luma_ch * 0.15), luma_info["head_cy"],
             int(luma_ch * 0.25), ELEC_CYAN, steps=4, max_alpha=30)
    draw = ImageDraw.Draw(img)  # W004

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann = load_font(9)
    font_sm  = load_font(8)

    draw.text((8, 8), "MCU — PUSH-IN TOWARD SCREEN", font=font_ann, fill=ANN_COLOR)
    draw.text((8, 20), "Cyan bleeds in — SOURCE: screen edge -> Luma",
              font=font_sm, fill=ANN_CYAN)

    draw.text((tv_rx + 4, tv_ty - 14), "SOURCE POINT",
              font=font_sm, fill=ELEC_CYAN)
    draw.text((luma_face_x - 40, luma_face_y - 16), "INTRUSION TARGET",
              font=font_sm, fill=ELEC_CYAN_DIM)

    # ── Three-tier caption bar ───────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11)
    font_t3   = load_font(9)
    font_meta = load_font(8)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    draw.text((10, DRAW_H + 4),
              "P04  |  MCU  |  PUSH-IN  |  GLITCH BLEEDS IN",
              font=font_t1, fill=TEXT_SHOT)
    draw.text((PW - 180, DRAW_H + 5),
              "ARC: TENSE", font=font_t2, fill=TEXT_ARC)
    draw.text((10, DRAW_H + 22),
              "Full tech den revealed. Cyan intrusion has directional source point from CRT edge.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "Pixel trail: screen -> Luma's face. Warm room invaded. Push-in camera.",
              font=font_t3, fill=(120, 112, 90))
    draw.text((PW - 310, DRAW_H + 56),
              "LTG_SB_cold_open_P04  /  Diego Vargas  /  C53 (pycairo chars)",
              font=font_meta, fill=TEXT_META)

    # Arc border — magenta (TENSE)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(str(OUTPUT_PATH), "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return str(OUTPUT_PATH)


if __name__ == "__main__":
    draw_panel()
