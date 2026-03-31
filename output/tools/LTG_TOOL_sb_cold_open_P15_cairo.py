#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P15_cairo.py
Cold Open Panel P15 — MED — Luma Hits Floor / Glitch Forced Hair Circle
Diego Vargas, Storyboard Artist — Cycle 52

PYCAIRO CHARACTER MIGRATION: Luma rendered via sb_char_draw on the floor.
Floor-level camera. Glitch forces hair into perfect circle (8 frames max).
Daze stars + confetti from Byte off-panel right.

Output: output/storyboards/panels/LTG_SB_cold_open_P15.png
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
from LTG_TOOL_sb_char_draw import draw_luma_sb

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P15.png")
os.makedirs(str(PANELS_DIR), exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72
DRAW_H    = PH - CAPTION_H  # 528

# ── Palette ──────────────────────────────────────────────────────────────────
WALL_DIM      = (165, 148, 118)
FLOOR_WARM    = (155, 128, 92)
FLOOR_PLANK   = (135, 112, 78)
ELEC_CYAN     = (0, 212, 232)
ELEC_CYAN_DIM = (0, 100, 120)
HOT_MAGENTA   = (232, 0, 152)
VOID_BLACK    = (10, 10, 20)
LUMA_HOODIE   = (232, 112, 58)
LUMA_HAIR     = (38, 22, 14)
HAIR_HL       = (61, 31, 15)
DAZE_YELLOW   = (255, 220, 80)
CONFETTI_C    = (0, 212, 232)
CONFETTI_M    = (232, 0, 152)
BG_CAPTION    = (12, 8, 6)
TEXT_SHOT     = (232, 224, 204)
TEXT_DESC     = (155, 148, 122)
TEXT_META     = (88, 82, 66)
ARC_COLOR     = HOT_MAGENTA  # TENSE / COMEDY
ANN_COLOR     = (220, 200, 80)

RNG = random.Random(1515)


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


def draw_irregular_poly(draw, cx, cy, r, sides, color, seed=0):
    lrng = random.Random(seed)
    pts = []
    for i in range(sides):
        angle = (2 * math.pi * i / sides) + lrng.uniform(-0.28, 0.28)
        dist  = r * lrng.uniform(0.68, 1.22)
        pts.append((int(cx + dist * math.cos(angle)), int(cy + dist * math.sin(angle))))
    draw.polygon(pts, fill=color)


def draw_panel():
    img  = Image.new('RGB', (PW, PH), FLOOR_WARM)
    draw = ImageDraw.Draw(img)

    # Floor-level camera: wall is thin strip at top, floor fills frame
    wall_strip_h = int(DRAW_H * 0.18)
    draw.rectangle([0, 0, PW, wall_strip_h], fill=WALL_DIM)

    # Floor planks
    for py in range(wall_strip_h, DRAW_H, 18):
        draw.line([(0, py), (PW, py)], fill=FLOOR_PLANK, width=1)

    # ── PYCAIRO CHARACTER: Luma sprawled on floor ────────────────────────────
    # Using standing pose rotated/adapted for floor — she's sprawled
    # Luma drawn standing then her visual position placed as if fallen
    char_surface, char_ctx, _, _ = create_surface(PW, DRAW_H)

    # Draw Luma standing (we'll position her to appear as on floor from side view)
    luma_cx = int(PW * 0.38)
    luma_floor_y = int(DRAW_H * 0.82)  # Ground level

    luma_info = draw_luma_sb(
        char_ctx,
        cx=luma_cx,
        floor_y=luma_floor_y,
        char_h=130,
        pose="sitting",  # Cross-legged = collapsed on floor
        lean_deg=-5.0,   # Leaning back (dazed)
        expression="alarmed",
        facing="right",
        seed=1515,
    )

    # Composite Luma
    char_pil = to_pil_rgba(char_surface)
    full_char = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    full_char.paste(char_pil, (0, 0))
    base_rgba = img.convert('RGBA')
    composited = Image.alpha_composite(base_rgba, full_char)
    img = composited.convert('RGB')
    draw = ImageDraw.Draw(img)  # W004

    # ── Glitch forced hair PERFECT CIRCLE ────────────────────────────────────
    head_cx = luma_info["head_cx"]
    head_cy = luma_info["head_cy"]
    head_r  = luma_info["head_r"]
    circle_r = int(head_r * 1.55)

    # ELEC_CYAN circle outline (forced symmetry)
    draw.ellipse([head_cx - circle_r, head_cy - circle_r,
                  head_cx + circle_r, head_cy + circle_r],
                 outline=ELEC_CYAN, width=2)

    # Radial lines inside (symmetry enforcement visual)
    for ra in range(0, 360, 30):
        angle = math.radians(ra)
        rx1 = head_cx + int((circle_r * 0.4) * math.cos(angle))
        ry1 = head_cy + int((circle_r * 0.4) * math.sin(angle))
        rx2 = head_cx + int((circle_r * 0.85) * math.cos(angle))
        ry2 = head_cy + int((circle_r * 0.85) * math.sin(angle))
        draw.line([(rx1, ry1), (rx2, ry2)], fill=ELEC_CYAN_DIM, width=1)

    # Pixel artifacts on circle rim
    for pa in range(0, 360, 25):
        angle = math.radians(pa + RNG.randint(-5, 5))
        px = head_cx + int(circle_r * math.cos(angle))
        py = head_cy + int(circle_r * math.sin(angle))
        sides = RNG.randint(4, 6)
        draw_irregular_poly(draw, px, py, RNG.randint(2, 4), sides, ELEC_CYAN, seed=pa * 3)

    # ── Daze stars ───────────────────────────────────────────────────────────
    star_r_orbit = circle_r + 15
    for si in range(6):
        angle = math.radians(si * 60 + 15)
        sx = head_cx + int(star_r_orbit * math.cos(angle))
        sy = head_cy + int(star_r_orbit * math.sin(angle))
        color = DAZE_YELLOW if si % 2 == 0 else ELEC_CYAN
        star_size = 4
        # 4-point star
        draw.polygon([(sx, sy - star_size), (sx + 2, sy - 1),
                       (sx + star_size, sy), (sx + 2, sy + 1),
                       (sx, sy + star_size), (sx - 2, sy + 1),
                       (sx - star_size, sy), (sx - 2, sy - 1)], fill=color)

    # ── Confetti drifting from Byte off-panel right ──────────────────────────
    for ci in range(18):
        cx_c = PW - RNG.randint(0, int(PW * 0.35))
        cy_c = RNG.randint(int(DRAW_H * 0.15), int(DRAW_H * 0.85))
        r_c  = RNG.randint(1, 4)
        sides = RNG.randint(4, 7)
        col  = CONFETTI_C if RNG.randint(0, 2) != 0 else CONFETTI_M
        draw_irregular_poly(draw, cx_c, cy_c, r_c, sides, col, seed=ci * 23 + 1500)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann   = load_font(9)
    font_ann_b = load_font(9, bold=True)
    font_sm    = load_font(8)

    draw.text((8, 8), 'MED  |  FLOOR-LEVEL  |  FLAT HORIZON  |  GLITCH FORCED SYMMETRY',
              font=font_ann, fill=ANN_COLOR)

    draw.text((head_cx + circle_r + 8, head_cy - 20),
              "GLITCH FORCED", font=font_ann_b, fill=ELEC_CYAN)
    draw.text((head_cx + circle_r + 8, head_cy - 8),
              "PERFECT CIRCLE", font=font_ann_b, fill=ELEC_CYAN)
    draw.text((head_cx + circle_r + 8, head_cy + 4),
              "8 FRAMES MAX", font=font_sm, fill=ELEC_CYAN_DIM)
    draw.text((head_cx + circle_r + 8, head_cy + 14),
              "then chaos reasserts", font=font_sm, fill=(100, 96, 88))

    # ── Three-tier caption bar ───────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11)
    font_t3   = load_font(9)
    font_meta = load_font(8)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    draw.text((10, DRAW_H + 4),
              "P15  |  MED  |  FLOOR-LEVEL  |  LUMA SPRAWLED  |  FORCED CIRCLE",
              font=font_t1, fill=TEXT_SHOT)
    draw.text((PW - 200, DRAW_H + 5),
              "ARC: TENSE / COMEDY", font=font_t2, fill=HOT_MAGENTA)
    draw.text((10, DRAW_H + 22),
              "Luma hits floor. Glitch forces hair into perfect circle (8 frames max). Daze stars.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "Then natural chaos reasserts. Confetti drifts from Byte off-panel right.",
              font=font_t3, fill=(120, 112, 90))
    draw.text((PW - 310, DRAW_H + 56),
              "LTG_SB_cold_open_P15  /  Diego Vargas  /  C52 (pycairo chars)",
              font=font_meta, fill=TEXT_META)

    # Arc border — HOT_MAGENTA
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(str(OUTPUT_PATH), "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return str(OUTPUT_PATH)


if __name__ == "__main__":
    draw_panel()
