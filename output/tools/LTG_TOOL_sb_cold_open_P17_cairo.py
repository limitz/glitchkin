#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P17_cairo.py
Cold Open Panel P17 — MED — Beat of Stillness / The Chip Falls
Diego Vargas, Storyboard Artist — Cycle 51

PYCAIRO CHARACTER REBUILD: Same composition, environment, and staging as C46 P17
but Luma and Byte are now drawn with the shared pycairo character module
(LTG_TOOL_sb_char_draw.py) for organic bezier curves, tapered strokes,
anti-aliased rendering, and gesture line construction.

Background and annotations remain PIL-based. Characters rendered on a separate
cairo surface and composited in.

Output: output/storyboards/panels/LTG_SB_cold_open_P17.png
"""

import math
import os
import sys
import random

# Ensure sibling tool imports work
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
from LTG_TOOL_sb_char_draw import draw_luma_sb, draw_byte_sb, draw_chip

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P17.png")
os.makedirs(str(PANELS_DIR), exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72
DRAW_H    = PH - CAPTION_H   # 528

# ── Palette ──────────────────────────────────────────────────────────────────
WARM_CREAM    = (250, 240, 220)
SUNLIT_AMB    = (212, 146, 58)
SUNLIT_DIM    = (180, 120, 50)
VOID_BLACK    = (10, 10, 20)
ELEC_CYAN     = (0, 212, 232)
ELEC_CYAN_DIM = (0, 100, 120)
ELEC_CYAN_FD  = (0, 60, 80)
HOT_MAGENTA   = (232, 0, 152)
LUMA_HOODIE   = (232, 112, 58)
LUMA_SKIN     = (218, 172, 128)
FLOOR_WARM    = (155, 128, 92)
FLOOR_GRAIN   = (130, 108, 76)
WALL_WARM     = (190, 170, 138)
CRT_BG        = (32, 42, 32)
CRT_STATIC    = (56, 70, 56)
CRT_BEZEL     = (50, 45, 40)
BYTE_TEAL     = (0, 212, 232)
DEEP_SPACE    = (6, 4, 14)
DESAT_RING    = (200, 195, 190)

# Caption
BG_CAPTION    = (12, 8, 6)
TEXT_SHOT     = (232, 224, 204)
TEXT_DESC     = (155, 148, 122)
TEXT_META     = (88, 82, 66)
ARC_COLOR     = ELEC_CYAN
ANN_COLOR     = (220, 200, 80)
ANN_CYAN      = (0, 180, 210)
ANN_DIM       = (80, 90, 100)

RNG = random.Random(1717)


def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def add_glow(img, cx, cy, r_max, color_rgb, steps=6, max_alpha=50):
    """Additive alpha composite glow — never darkens."""
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_irregular_poly(draw, cx, cy, r, sides, color, rng, fill=True):
    pts = []
    for i in range(sides):
        angle = (2 * math.pi * i / sides) + rng.uniform(-0.2, 0.2)
        rr    = r * rng.uniform(0.72, 1.0)
        pts.append((int(cx + rr * math.cos(angle)),
                    int(cy + rr * math.sin(angle))))
    if fill:
        draw.polygon(pts, fill=color)
    else:
        draw.polygon(pts, outline=color)


def draw_panel():
    img  = Image.new('RGB', (PW, PH), WALL_WARM)
    draw = ImageDraw.Draw(img)

    # ── Background: den room — restoring to calm ─────────────────────────────
    wall_h = int(DRAW_H * 0.38)
    floor_y = wall_h

    # Wall — warm left (Luma zone), cool right (Byte zone)
    for x in range(PW):
        t = x / PW
        c = lerp_color(WALL_WARM, (130, 148, 148), t * 0.55)
        draw.line([(x, 0), (x, wall_h)], fill=c)

    # Floor — warm left, cool tint right
    for x in range(PW):
        t = x / PW
        c = lerp_color(FLOOR_WARM, (130, 135, 128), t * 0.35)
        draw.line([(x, floor_y), (x, DRAW_H)], fill=c)

    # Floor planks
    for py in range(floor_y, DRAW_H, 24):
        draw.line([(0, py), (PW, py)], fill=FLOOR_GRAIN, width=1)

    # ── CRT Monitors BG — right zone, behind Byte ───────────────────────────
    mon_specs = [
        (int(PW * 0.60), int(DRAW_H * 0.05), int(PW * 0.24), int(DRAW_H * 0.26)),
        (int(PW * 0.86), int(DRAW_H * 0.08), int(PW * 0.12), int(DRAW_H * 0.22)),
    ]
    for mx, my, mw, mh in mon_specs:
        draw.rectangle([mx, my, mx + mw, my + mh], fill=CRT_BEZEL)
        screen_pad = 6
        draw.rectangle([mx + screen_pad, my + screen_pad,
                         mx + mw - screen_pad, my + mh - screen_pad],
                        fill=CRT_BG)
        for _ in range(60):
            sx = RNG.randint(mx + screen_pad + 2, mx + mw - screen_pad - 2)
            sy = RNG.randint(my + screen_pad + 2, my + mh - screen_pad - 2)
            draw.point((sx, sy), fill=CRT_STATIC)

    # Warm lamp glow from camera-left
    add_glow(img, -20, int(DRAW_H * 0.20), int(PW * 0.55),
             SUNLIT_AMB, steps=10, max_alpha=18)
    draw = ImageDraw.Draw(img)  # W004 refresh

    # ── PYCAIRO CHARACTER RENDERING ──────────────────────────────────────────
    # Create a cairo surface for characters only (RGBA for compositing)
    char_surface, char_ctx, _, _ = create_surface(PW, DRAW_H)

    # Luma position (same as original P17)
    luma_floor_y = floor_y + int((DRAW_H - floor_y) * 0.82)
    luma_cx = int(PW * 0.24)

    # Draw Luma sitting cross-legged using sb_char_draw module
    luma_info = draw_luma_sb(
        char_ctx,
        cx=luma_cx,
        floor_y=luma_floor_y,
        char_h=140,
        pose="sitting",
        lean_deg=3.0,
        expression="assessing",
        facing="right",
        seed=1717,
    )

    # Byte position (same as original P17)
    byte_cx = int(PW * 0.76)
    byte_cy = int(DRAW_H * 0.52)

    # Draw Byte hovering using sb_char_draw module
    byte_info = draw_byte_sb(
        char_ctx,
        cx=byte_cx,
        cy=byte_cy,
        body_h=75,
        expression="still",
        facing="left",
        lean_deg=2.0,
        hovering=True,
        seed=1718,
    )

    # Draw falling pixel chip between them
    chip_x = int(PW * 0.50)
    chip_y = int(DRAW_H * 0.55)
    draw_chip(char_ctx, chip_x, chip_y, size=7, trail_len=40, trail_step=6)

    # Convert cairo character layer to PIL RGBA and composite onto BG
    char_pil = to_pil_rgba(char_surface)
    # char_pil is PW x DRAW_H; img is PW x PH — paste onto full canvas
    full_char = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    full_char.paste(char_pil, (0, 0))
    base_rgba = img.convert('RGBA')
    composited = Image.alpha_composite(base_rgba, full_char)
    img = composited.convert('RGB')
    draw = ImageDraw.Draw(img)  # W004 refresh

    # ── Ghost trails (fading pixel wisps from Byte's ricochet) ───────────────
    for t_step in range(4):
        t    = t_step / 5.0
        ghost_x = int(byte_cx + (1 - t) * 80 * math.cos(math.radians(130)))
        ghost_y = int(byte_cy + (1 - t) * 60 * math.sin(math.radians(130)))
        ghost_r = int(18 * (1 - t * 0.7))
        ghost_a = int(35 * (1 - t))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([ghost_x - ghost_r, ghost_y - ghost_r,
                    ghost_x + ghost_r, ghost_y + ghost_r],
                   fill=(*ELEC_CYAN_FD, ghost_a))
        img.paste(Image.alpha_composite(img.convert('RGBA'), glow).convert('RGB'))
    draw = ImageDraw.Draw(img)  # W004 refresh

    # ── Desaturation ring on floor under Byte ────────────────────────────────
    desat_floor_y = floor_y + int((DRAW_H - floor_y) * 0.88)
    draw.ellipse([byte_cx - 38, desat_floor_y - 10,
                  byte_cx + 38, desat_floor_y + 10],
                 outline=DESAT_RING, width=2)

    # Cyan glow from Byte
    add_glow(img, byte_cx, byte_cy, 120, ELEC_CYAN, steps=8, max_alpha=22)
    draw = ImageDraw.Draw(img)  # W004 refresh

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann   = load_font(9,  bold=False)
    font_ann_b = load_font(9,  bold=True)
    font_sm    = load_font(8,  bold=False)

    # Camera note
    draw.text((8, 8), 'MED  |  4-5FT  |  FLAT HORIZON  |  BEAT OF STILLNESS',
              font=font_ann, fill=ANN_COLOR)

    # Chip annotation
    draw.text((chip_x + 7 + 6, chip_y - 6), '"soft tick"',
              font=font_ann_b, fill=ANN_CYAN)
    draw.text((chip_x + 7 + 6, chip_y + 6), "only thing moving",
              font=font_sm, fill=ANN_DIM)

    # Luma annotation
    head_cy = luma_info["head_cy"]
    head_r = luma_info["head_r"]
    draw.text((luma_cx - 35, head_cy - head_r - 32),
              "ASSESSING", font=font_ann_b, fill=ANN_COLOR)
    draw.text((luma_cx - 30, head_cy - head_r - 22),
              "(fear gone, processing)", font=font_sm, fill=(130, 120, 100))

    # Byte annotation
    draw.text((byte_cx + 40, byte_info["face_cy"] - 10),
              "STILL", font=font_ann_b, fill=ANN_CYAN)
    draw.text((byte_cx + 40, byte_info["face_cy"] + 2),
              "(mirror of Luma's beat)", font=font_sm, fill=ANN_DIM)

    # Pixel trail note
    draw.text((int(PW * 0.58), int(DRAW_H * 0.15)),
              "trail fading", font=font_sm, fill=ELEC_CYAN_DIM)
    draw.text((int(PW * 0.58), int(DRAW_H * 0.15) + 10),
              "(last wisps)", font=font_sm, fill=ELEC_CYAN_DIM)

    # Desat ring annotation
    draw.text((byte_cx + 42, desat_floor_y - 5),
              "desat ring", font=font_sm, fill=(160, 155, 150))

    # Depth temp annotation
    draw.text((int(PW * 0.08), DRAW_H - 16),
              "WARM (Luma zone)", font=font_sm, fill=(180, 130, 60))
    draw.text((int(PW * 0.68), DRAW_H - 16),
              "COOL (Byte zone)", font=font_sm, fill=ELEC_CYAN_DIM)

    # Negative space annotation
    gap_label_x = int(PW * 0.42)
    gap_label_y = int(DRAW_H * 0.75)
    draw.text((gap_label_x - 24, gap_label_y), "NEGATIVE SPACE",
              font=font_sm, fill=(100, 96, 88))
    draw.text((gap_label_x - 16, gap_label_y + 10), "(their distance)",
              font=font_sm, fill=(80, 76, 70))

    # ── Three-tier caption bar ───────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11, bold=False)
    font_t3   = load_font(9,  bold=False)
    font_meta = load_font(8,  bold=False)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    # Tier 1 — Shot code
    draw.text((10, DRAW_H + 4),
              "P17  |  MED  |  4-5FT  |  BEAT OF STILLNESS  |  CHIP FALLS",
              font=font_t1, fill=TEXT_SHOT)

    # Tier 2 — Arc label
    draw.text((PW - 260, DRAW_H + 5),
              "ARC: CURIOUS / FIRST ENCOUNTER", font=font_t2, fill=ELEC_CYAN)

    # Tier 3 — Narrative
    draw.text((10, DRAW_H + 22),
              "Luma sitting cross-legged. Byte hovering across room. Trails fading. Everything stops.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "One pixel chip falls between them. \"Soft tick.\" This cracks the standoff.",
              font=font_t3, fill=(120, 112, 90))

    # Metadata
    draw.text((PW - 310, DRAW_H + 56),
              "LTG_SB_cold_open_P17  /  Diego Vargas  /  C51 (pycairo chars)",
              font=font_meta, fill=TEXT_META)

    # Arc border — ELEC_CYAN
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(str(OUTPUT_PATH), "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return str(OUTPUT_PATH)


if __name__ == "__main__":
    draw_panel()
    print("P17 pycairo character rebuild complete (C51).")
    print("Beat: Beat of stillness. Luma + Byte drawn with LTG_TOOL_sb_char_draw.")
    print("Background/annotations remain PIL. Characters are organic bezier curves.")
