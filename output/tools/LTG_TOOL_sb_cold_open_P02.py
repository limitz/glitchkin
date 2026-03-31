#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P02.py
Cold Open Panel P02 — WIDE ESTABLISHING — Luma Enters Grandma's Tech Den
Diego Vargas, Storyboard Artist — Cycle 53

Beat: Character intro via sleeping position, snacks, notebook. Luma enters
Grandma's warm cluttered tech den. Wide shot, slightly high angle, two-point
perspective. Warm dominant palette with subtle CRT glow from background.

Luma drawn via pycairo (draw_luma_sb standing pose, entering from left).
Environment is PIL.

Output: output/storyboards/panels/LTG_SB_cold_open_P02.png
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
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P02.png")
os.makedirs(str(PANELS_DIR), exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72
DRAW_H    = PH - CAPTION_H  # 528

# ── Palette ──────────────────────────────────────────────────────────────────
WARM_CREAM   = (250, 240, 220)
WALL_WARM    = (228, 214, 188)
WALL_UPPER   = (245, 232, 205)
FLOOR_LIGHT  = (195, 172, 132)
FLOOR_DARK   = (178, 155, 118)
WOOD_DARK    = (95, 68, 42)
WOOD_MED     = (138, 105, 68)
LUMA_HOODIE  = (232, 112, 58)
LUMA_SKIN    = (218, 172, 128)
LUMA_HAIR    = (38, 22, 14)
SUNLIT_AMB   = (212, 146, 58)
ELEC_CYAN    = (0, 212, 232)
ELEC_CYAN_DIM = (0, 140, 160)
CRT_PHOSPHOR = (140, 158, 130)
CRT_STATIC_D = (118, 132, 112)
CRT_DARK     = (62, 58, 48)
VOID_BLACK   = (10, 10, 20)
LINE_DARK    = (42, 32, 22)
BG_CAPTION   = (12, 8, 6)
TEXT_SHOT    = (232, 224, 204)
TEXT_ARC     = SUNLIT_AMB
TEXT_DESC    = (155, 148, 122)
TEXT_META    = (88, 82, 66)
ARC_COLOR    = SUNLIT_AMB   # QUIET / CURIOUS — warm amber
ANN_COLOR    = (180, 158, 108)
COUCH_WARM   = (158, 112, 72)
COUCH_SHADOW = (120, 82, 50)
PILLOW_WARM  = (200, 170, 130)

RNG = random.Random(202)


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


def draw_panel():
    img  = Image.new('RGB', (PW, PH), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # ── Environment: Grandma's tech den ─────────────────────────────────────
    horizon_y = int(DRAW_H * 0.38)
    floor_y   = int(DRAW_H * 0.68)

    # Ceiling
    draw.rectangle([0, 0, PW, int(DRAW_H * 0.18)], fill=WALL_UPPER)

    # Wall
    draw.rectangle([0, int(DRAW_H * 0.18), PW, floor_y], fill=WALL_WARM)

    # Floor with checkerboard
    for col in range(8):
        for row in range(4):
            fy0 = int(floor_y + row / 4 * (DRAW_H - floor_y))
            fy1 = int(floor_y + (row + 1) / 4 * (DRAW_H - floor_y))
            fx0 = col * PW // 8
            fx1 = (col + 1) * PW // 8
            fill = FLOOR_LIGHT if (row + col) % 2 == 0 else FLOOR_DARK
            draw.rectangle([fx0, fy0, fx1, fy1], fill=fill)

    # Window (warm light from left)
    win_x, win_y = int(PW * 0.06), int(DRAW_H * 0.20)
    win_w, win_h = int(PW * 0.14), int(DRAW_H * 0.28)
    draw.rectangle([win_x, win_y, win_x + win_w, win_y + win_h],
                   fill=(255, 225, 145), outline=LINE_DARK, width=2)
    draw.line([win_x + win_w // 2, win_y, win_x + win_w // 2, win_y + win_h],
              fill=LINE_DARK, width=1)
    draw.line([win_x, win_y + win_h // 2, win_x + win_w, win_y + win_h // 2],
              fill=LINE_DARK, width=1)
    add_glow(img, win_x + win_w // 2, floor_y, 100, SUNLIT_AMB, steps=4, max_alpha=25)
    draw = ImageDraw.Draw(img)  # W004

    # Bookshelf (right BG)
    shelf_x = int(PW * 0.62)
    shelf_w = int(PW * 0.32)
    for s in range(4):
        sy = int(DRAW_H * 0.20) + s * int(DRAW_H * 0.11)
        draw.rectangle([shelf_x, sy, shelf_x + shelf_w, sy + int(DRAW_H * 0.09)],
                       fill=WOOD_DARK, outline=LINE_DARK, width=1)
        for b in range(10):
            bx = shelf_x + 4 + b * int(shelf_w / 11)
            bc = RNG.choice([(180, 80, 60), (80, 100, 150), (100, 140, 80),
                              (160, 140, 60), (100, 80, 120), (140, 60, 90)])
            bw = RNG.randint(8, 14)
            draw.rectangle([bx, sy + 2, bx + bw, sy + int(DRAW_H * 0.08)],
                           fill=bc, outline=LINE_DARK, width=1)

    # Couch (center-right, where Luma will eventually sleep)
    couch_x = int(PW * 0.42)
    couch_y = int(DRAW_H * 0.52)
    couch_w = int(PW * 0.32)
    couch_h = int(DRAW_H * 0.18)
    draw.rectangle([couch_x, couch_y, couch_x + couch_w, couch_y + couch_h],
                   fill=COUCH_WARM, outline=COUCH_SHADOW, width=2)
    draw.rectangle([couch_x, couch_y, couch_x + couch_w, couch_y + 8],
                   fill=COUCH_SHADOW)
    # Pillow on couch
    draw.rectangle([couch_x + 8, couch_y + 4, couch_x + int(couch_w * 0.3), couch_y + couch_h - 6],
                   fill=PILLOW_WARM, outline=COUCH_SHADOW, width=1)

    # Coffee table in front of couch
    ct_x = couch_x + int(couch_w * 0.15)
    ct_y = int(DRAW_H * 0.72)
    ct_w = int(couch_w * 0.6)
    draw.rectangle([ct_x, ct_y, ct_x + ct_w, ct_y + int(DRAW_H * 0.05)],
                   fill=WOOD_MED, outline=LINE_DARK, width=1)
    # Snacks on table
    for sx in range(3):
        snack_x = ct_x + 8 + sx * int(ct_w / 4)
        snack_c = RNG.choice([(220, 180, 60), (200, 80, 60), (100, 160, 80)])
        draw.rectangle([snack_x, ct_y - 6, snack_x + 12, ct_y], fill=snack_c)
    # Notebook on table
    nb_x = ct_x + ct_w - 30
    draw.rectangle([nb_x, ct_y - 8, nb_x + 22, ct_y], fill=(240, 235, 220),
                   outline=LINE_DARK, width=1)
    draw.line([nb_x + 11, ct_y - 8, nb_x + 11, ct_y], fill=(180, 60, 60), width=1)

    # CRT TV on shelf (right BG — story trigger, subtle)
    tv_x, tv_y = int(PW * 0.72), int(DRAW_H * 0.42)
    tv_w, tv_h = 55, 42
    draw.rectangle([tv_x, tv_y, tv_x + tv_w, tv_y + tv_h],
                   fill=CRT_DARK, outline=(80, 68, 52), width=2)
    draw.rectangle([tv_x + 5, tv_y + 5, tv_x + tv_w - 5, tv_y + tv_h - 5],
                   fill=CRT_PHOSPHOR)
    # Scanlines
    for sl_y in range(tv_y + 5, tv_y + tv_h - 5, 3):
        draw.line([(tv_x + 5, sl_y), (tv_x + tv_w - 5, sl_y)],
                  fill=CRT_STATIC_D, width=1)
    # Subtle CRT glow
    add_glow(img, tv_x + tv_w // 2, tv_y + tv_h // 2 + 15, 40, ELEC_CYAN,
             steps=3, max_alpha=15)
    draw = ImageDraw.Draw(img)  # W004

    # Doorway (left) — Luma enters from here
    door_x = int(PW * 0.18)
    door_w = int(PW * 0.10)
    door_y_top = int(DRAW_H * 0.12)
    draw.rectangle([door_x, door_y_top, door_x + door_w, floor_y],
                   fill=(180, 155, 110), outline=LINE_DARK, width=2)

    # ── PYCAIRO CHARACTER: Luma standing, entering from doorway ─────────────
    luma_cx   = int(PW * 0.28)
    luma_floor = int(DRAW_H * 0.68)
    luma_ch   = int(DRAW_H * 0.38)  # wide shot — smaller character

    char_surface, char_ctx, _, _ = create_surface(PW, DRAW_H)

    luma_info = draw_luma_sb(
        char_ctx,
        cx=luma_cx,
        floor_y=luma_floor,
        char_h=luma_ch,
        pose="standing",
        lean_deg=2.0,
        expression="neutral",
        facing="right",
        seed=202,
    )

    # Composite cairo onto PIL
    char_pil = to_pil_rgba(char_surface)
    full_char = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    full_char.paste(char_pil, (0, 0))
    base_rgba = img.convert('RGBA')
    composited = Image.alpha_composite(base_rgba, full_char)
    img = composited.convert('RGB')
    draw = ImageDraw.Draw(img)  # W004

    # Warm glow on Luma from window
    add_glow(img, luma_cx - 20, luma_info["head_cy"], 50, SUNLIT_AMB,
             steps=4, max_alpha=20)
    draw = ImageDraw.Draw(img)  # W004

    # Sight-line: Luma looking toward couch/CRT area
    font_sm = load_font(8)
    luma_eye_x = luma_info["head_cx"] + int(luma_ch * 0.05)
    luma_eye_y = luma_info["head_cy"]
    target_x = int(PW * 0.58)
    target_y = int(DRAW_H * 0.48)
    dx = target_x - luma_eye_x
    dy = target_y - luma_eye_y
    dist = math.sqrt(dx**2 + dy**2)
    n_dashes = max(2, int(dist / 12))
    for di in range(n_dashes):
        t0 = di / n_dashes
        t1 = (di + 0.45) / n_dashes
        sx0 = int(luma_eye_x + dx * t0)
        sy0 = int(luma_eye_y + dy * t0)
        sx1 = int(luma_eye_x + dx * t1)
        sy1 = int(luma_eye_y + dy * t1)
        draw.line([(sx0, sy0), (sx1, sy1)], fill=ANN_COLOR, width=1)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann = load_font(9)
    draw.text((8, 8), "WIDE — HIGH ANGLE — 2-PT PERSPECTIVE", font=font_ann, fill=ANN_COLOR)
    draw.text((8, 20), "Luma enters from doorway L. Couch/snacks/notebook establish.",
              font=font_sm, fill=(150, 130, 95))

    draw.text((tv_x + tv_w + 4, tv_y), "CRT", font=font_sm, fill=ELEC_CYAN_DIM)
    draw.text((couch_x + couch_w + 4, couch_y + 4), "couch", font=font_sm, fill=ANN_COLOR)
    draw.text((ct_x + ct_w + 4, ct_y - 4), "snacks + notebook", font=font_sm, fill=ANN_COLOR)

    # ── Three-tier caption bar ───────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11)
    font_t3   = load_font(9)
    font_meta = load_font(8)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    draw.text((10, DRAW_H + 4),
              "P02  |  WIDE  |  HIGH ANGLE  |  LUMA ENTERS",
              font=font_t1, fill=TEXT_SHOT)
    draw.text((PW - 220, DRAW_H + 5),
              "ARC: QUIET / CURIOUS", font=font_t2, fill=TEXT_ARC)
    draw.text((10, DRAW_H + 22),
              "Luma enters Grandma's tech den. Snacks, notebook, couch visible. CRT in BG shelf.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "High angle wide — character intro via environment. Warm dominant, subtle CRT glow.",
              font=font_t3, fill=(120, 112, 90))
    draw.text((PW - 310, DRAW_H + 56),
              "LTG_SB_cold_open_P02  /  Diego Vargas  /  C53 (pycairo chars)",
              font=font_meta, fill=TEXT_META)

    # Arc border — warm amber (QUIET arc)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(str(OUTPUT_PATH), "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return str(OUTPUT_PATH)


if __name__ == "__main__":
    draw_panel()
