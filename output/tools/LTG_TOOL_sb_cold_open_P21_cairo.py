#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P21_cairo.py
Cold Open Panel P21 — WIDE HIGH ANGLE — Re-Escalation
Diego Vargas, Storyboard Artist — Cycle 52

PYCAIRO CHARACTER MIGRATION: Same composition as C47 P21.
Luma (standing, rising) and Byte (standing, rigid) via pycairo sb_char_draw.
Dutch 5 CCW. 7 CRT monitors blazing. Cyan/magenta flood.

Output: output/storyboards/panels/LTG_SB_cold_open_P21.png
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
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P21.png")
os.makedirs(str(PANELS_DIR), exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72
DRAW_H    = PH - CAPTION_H  # 528

# ── Palette ──────────────────────────────────────────────────────────────────
WALL_WARM     = (190, 170, 138)
FLOOR_WARM    = (155, 128, 92)
FLOOR_GRAIN   = (130, 108, 76)
VOID_BLACK    = (10, 10, 20)
DEEP_SPACE    = (6, 4, 14)
ELEC_CYAN     = (0, 212, 232)
ELEC_CYAN_DIM = (0, 100, 120)
HOT_MAGENTA   = (232, 0, 152)
CRT_BLAZE_C   = (0, 212, 232)
CRT_BLAZE_M   = (232, 0, 152)
CRT_BEZEL     = (50, 45, 40)
CONFETTI_C    = (0, 212, 232)
CONFETTI_M    = (232, 0, 152)
BG_CAPTION    = (12, 8, 6)
TEXT_SHOT     = (232, 224, 204)
TEXT_DESC     = (155, 148, 122)
TEXT_META     = (88, 82, 66)
ARC_COLOR     = HOT_MAGENTA
ANN_COLOR     = (220, 200, 80)

RNG = random.Random(2121)


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
    # Build on oversized canvas for Dutch tilt crop
    extra = 40
    canvas_w = PW + extra * 2
    canvas_h = DRAW_H + extra * 2

    draw_img = Image.new('RGB', (canvas_w, canvas_h), WALL_WARM)
    draw = ImageDraw.Draw(draw_img)

    wall_h = int(canvas_h * 0.38)

    # Wall — warm, being overwhelmed by cyan/magenta flood
    for x in range(canvas_w):
        t = x / canvas_w
        c = lerp_color(WALL_WARM, (60, 100, 110), t * 0.45 + 0.20)
        draw.line([(x, 0), (x, wall_h)], fill=c)

    # Floor
    for x in range(canvas_w):
        t = x / canvas_w
        c = lerp_color(FLOOR_WARM, (80, 95, 90), t * 0.40 + 0.15)
        draw.line([(x, wall_h), (x, canvas_h)], fill=c)
    for py in range(wall_h, canvas_h, 24):
        draw.line([(0, py), (canvas_w, py)], fill=FLOOR_GRAIN, width=1)

    # 7 CRT monitors ALL BLAZING
    monitors = [
        (int(canvas_w * 0.08), int(canvas_h * 0.02), int(canvas_w * 0.12), int(canvas_h * 0.18)),
        (int(canvas_w * 0.22), int(canvas_h * 0.04), int(canvas_w * 0.10), int(canvas_h * 0.16)),
        (int(canvas_w * 0.35), int(canvas_h * 0.01), int(canvas_w * 0.14), int(canvas_h * 0.20)),
        (int(canvas_w * 0.52), int(canvas_h * 0.03), int(canvas_w * 0.11), int(canvas_h * 0.17)),
        (int(canvas_w * 0.65), int(canvas_h * 0.02), int(canvas_w * 0.13), int(canvas_h * 0.19)),
        (int(canvas_w * 0.80), int(canvas_h * 0.05), int(canvas_w * 0.10), int(canvas_h * 0.15)),
        (int(canvas_w * 0.92), int(canvas_h * 0.03), int(canvas_w * 0.08), int(canvas_h * 0.14)),
    ]
    for mx, my, mw, mh in monitors:
        draw.rectangle([mx, my, mx + mw, my + mh], fill=CRT_BEZEL)
        sp = 4
        # Blazing screen — alternating cyan/magenta
        screen_col = CRT_BLAZE_C if RNG.random() < 0.6 else CRT_BLAZE_M
        draw.rectangle([mx + sp, my + sp, mx + mw - sp, my + mh - sp], fill=screen_col)
        # Screen distortion rings
        rcx = mx + mw // 2
        rcy = my + mh // 2
        for ri in range(2):
            rr = int(mw * 0.3) + ri * 8
            draw.ellipse([rcx - rr, rcy - rr, rcx + rr, rcy + rr],
                         outline=(255, 255, 255, 80), width=1)

    # Cyan/magenta flood wash
    flood = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    fd = ImageDraw.Draw(flood)
    for mx, my, mw, mh in monitors:
        mc = CRT_BLAZE_C if RNG.random() < 0.6 else CRT_BLAZE_M
        gcx = mx + mw // 2
        gcy = my + mh // 2
        for gi in range(8, 0, -1):
            gr = int(mw * 1.5 * gi / 8)
            ga = int(30 * (1 - gi / 9))
            fd.ellipse([gcx - gr, gcy - gr, gcx + gr, gcy + gr], fill=(*mc, ga))
    draw_img.paste(Image.alpha_composite(draw_img.convert('RGBA'), flood).convert('RGB'))
    draw = ImageDraw.Draw(draw_img)

    # ── PYCAIRO CHARACTERS on oversized canvas ───────────────────────────────
    char_surface, char_ctx, _, _ = create_surface(canvas_w, canvas_h)

    floor_cy = wall_h + int((canvas_h - wall_h) * 0.82)

    # Luma camera-left — standing, rising from floor, ALARMED
    luma_cx = int(canvas_w * 0.30)
    luma_info = draw_luma_sb(
        char_ctx,
        cx=luma_cx,
        floor_y=floor_cy,
        char_h=110,  # Smaller (high angle makes characters small)
        pose="standing",
        lean_deg=4.0,  # Rising forward
        expression="alarmed",
        facing="right",
        seed=2121,
    )

    # Byte camera-right — standing rigid, facing monitors
    byte_cx = int(canvas_w * 0.70)
    byte_cy = luma_info["head_cy"] + 5  # Slightly lower (Byte is shorter)

    byte_info = draw_byte_sb(
        char_ctx,
        cx=byte_cx,
        cy=byte_cy,
        body_h=65,  # Smaller (high angle)
        expression="alarmed",
        facing="right",  # Facing monitors
        lean_deg=0.0,  # RIGID — arms pulled in
        hovering=False,
        seed=2122,
    )

    # Composite characters
    char_pil = to_pil_rgba(char_surface)
    full_char = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    full_char.paste(char_pil, (0, 0))
    base_rgba = draw_img.convert('RGBA')
    composited = Image.alpha_composite(base_rgba, full_char)
    draw_img = composited.convert('RGB')
    draw = ImageDraw.Draw(draw_img)

    # 30+ pixel confetti (full density return)
    for ci in range(35):
        cx_c = RNG.randint(extra, canvas_w - extra)
        cy_c = RNG.randint(extra, canvas_h - extra)
        r_c  = RNG.randint(1, 5)
        sides = RNG.randint(4, 7)
        col  = CONFETTI_C if RNG.randint(0, 2) != 0 else CONFETTI_M
        draw_irregular_poly(draw, cx_c, cy_c, r_c, sides, col, seed=ci * 31 + 2100)

    # ── Dutch tilt 5 CCW ─────────────────────────────────────────────────────
    tilted = draw_img.rotate(5, expand=False, fillcolor=DEEP_SPACE)
    # Crop to PW x DRAW_H from center
    cx_crop = canvas_w // 2
    cy_crop = canvas_h // 2
    left = cx_crop - PW // 2
    top  = cy_crop - DRAW_H // 2
    draw_area = tilted.crop((left, top, left + PW, top + DRAW_H))

    # ── Assemble final panel ─────────────────────────────────────────────────
    img = Image.new('RGB', (PW, PH), BG_CAPTION)
    img.paste(draw_area, (0, 0))
    draw = ImageDraw.Draw(img)

    # Annotations (on final panel, not tilted)
    font_ann   = load_font(9)
    font_ann_b = load_font(9, bold=True)
    font_sm    = load_font(8)

    draw.text((8, 8), 'WIDE HIGH ANGLE  |  DUTCH 5 CCW  |  RE-ESCALATION',
              font=font_ann, fill=ANN_COLOR)
    draw.text((8, 20), '7 CRT monitors ALL BLAZING', font=font_sm, fill=HOT_MAGENTA)

    # ── Three-tier caption bar ───────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11)
    font_t3   = load_font(9)
    font_meta = load_font(8)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    draw.text((10, DRAW_H + 4),
              "P21  |  WIDE HIGH ANGLE  |  DUTCH 5 CCW  |  RE-ESCALATION",
              font=font_t1, fill=TEXT_SHOT)
    draw.text((PW - 200, DRAW_H + 5),
              "ARC: TENSE / CRISIS", font=font_t2, fill=HOT_MAGENTA)
    draw.text((10, DRAW_H + 22),
              "All 7 monitors blazing. Glitchkin pressing against screens. Cyan/magenta flood.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "Byte RIGID (he knows). Luma RISING (alarmed but processing). 30+ confetti.",
              font=font_t3, fill=(120, 112, 90))
    draw.text((PW - 310, DRAW_H + 56),
              "LTG_SB_cold_open_P21  /  Diego Vargas  /  C52 (pycairo chars)",
              font=font_meta, fill=TEXT_META)

    # Arc border — HOT_MAGENTA
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(str(OUTPUT_PATH), "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return str(OUTPUT_PATH)


if __name__ == "__main__":
    draw_panel()
