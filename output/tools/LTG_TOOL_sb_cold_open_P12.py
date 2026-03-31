#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P12.py
Cold Open Panel P12 — CU TWO-SHOT — Luma and Byte Nose-to-Nose
Diego Vargas, Storyboard Artist — Cycle 53

Beat: Luma and Byte nose-to-nose. Equal presence, center-weighted.
Breathing negative space between them. CRT visible camera-right BG.
P12 staging spec: Equal presence ~30% width each, ~40% gap.
Byte at Luma's exact head_cy (eye-level descent).

Both characters drawn via pycairo: Luma via draw_luma_sb (standing),
Byte via draw_byte_sb (hovering at Luma eye level).

Output: output/storyboards/panels/LTG_SB_cold_open_P12.png
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
from LTG_TOOL_sb_char_draw import draw_luma_sb, draw_byte_sb

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P12.png")
os.makedirs(str(PANELS_DIR), exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72
DRAW_H    = PH - CAPTION_H  # 528

# ── Palette ──────────────────────────────────────────────────────────────────
WARM_CREAM   = (250, 240, 220)
WALL_WARM    = (228, 214, 188)
FLOOR_LIGHT  = (195, 172, 132)
SUNLIT_AMB   = (212, 146, 58)
LUMA_HOODIE  = (232, 112, 58)
LUMA_SKIN    = (218, 172, 128)
LUMA_HAIR    = (38, 22, 14)
ELEC_CYAN    = (0, 212, 232)
ELEC_CYAN_DIM = (0, 140, 160)
ELEC_CYAN_HI = (90, 248, 255)
HOT_MAGENTA  = (232, 0, 152)
VOID_BLACK   = (10, 10, 20)
CRT_DARK     = (52, 44, 34)
CRT_PHOSPHOR = (140, 158, 130)
CRT_STATIC_D = (118, 132, 112)
DESAT_RING   = (168, 172, 168)
LINE_DARK    = (42, 32, 22)
BG_CAPTION   = (12, 8, 6)
TEXT_SHOT    = (232, 224, 204)
TEXT_ARC     = ELEC_CYAN
TEXT_DESC    = (155, 148, 122)
TEXT_META    = (88, 82, 66)
ARC_COLOR    = ELEC_CYAN  # CURIOUS / PRE-DISCOVERY
ANN_COLOR    = (180, 158, 108)

RNG = random.Random(1212)


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

    # ── Environment: warm room BG with CRT camera-right ─────────────────────
    floor_y = int(DRAW_H * 0.72)
    draw.rectangle([0, 0, PW, floor_y], fill=WALL_WARM)
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=FLOOR_LIGHT)

    # Warm ambient from left
    add_glow(img, int(PW * 0.15), int(DRAW_H * 0.30), 150, SUNLIT_AMB,
             steps=5, max_alpha=20)
    draw = ImageDraw.Draw(img)  # W004

    # CRT visible camera-right BG
    tv_x = int(PW * 0.78)
    tv_y = int(DRAW_H * 0.28)
    tv_w, tv_h = 60, 48
    draw.rectangle([tv_x, tv_y, tv_x + tv_w, tv_y + tv_h],
                   fill=CRT_DARK, outline=(72, 60, 46), width=2)
    draw.rectangle([tv_x + 5, tv_y + 5, tv_x + tv_w - 5, tv_y + tv_h - 5],
                   fill=CRT_PHOSPHOR)
    for sl_y in range(tv_y + 5, tv_y + tv_h - 5, 3):
        draw.line([(tv_x + 5, sl_y), (tv_x + tv_w - 5, sl_y)],
                  fill=CRT_STATIC_D, width=1)
    add_glow(img, tv_x + tv_w // 2, tv_y + tv_h // 2, 55, ELEC_CYAN,
             steps=4, max_alpha=30)
    draw = ImageDraw.Draw(img)  # W004

    # Cyan ambient on right side of room from CRT
    add_glow(img, int(PW * 0.82), int(DRAW_H * 0.45), 120, ELEC_CYAN,
             steps=5, max_alpha=20)
    draw = ImageDraw.Draw(img)  # W004

    # ── PYCAIRO CHARACTERS ──────────────────────────────────────────────────
    # Luma: camera-left (~28% of frame center)
    # Byte: camera-right (~72% of frame center)
    # Equal presence, ~40% breathing gap between them

    luma_cx    = int(PW * 0.28)
    luma_floor = int(DRAW_H * 0.85)
    luma_ch    = int(DRAW_H * 0.55)

    char_surface, char_ctx, _, _ = create_surface(PW, DRAW_H)

    # Draw Luma standing, facing right (toward Byte)
    luma_info = draw_luma_sb(
        char_ctx,
        cx=luma_cx,
        floor_y=luma_floor,
        char_h=luma_ch,
        pose="standing",
        lean_deg=2.0,
        expression="assessing",
        facing="right",
        seed=1212,
    )

    # Byte at Luma's exact eye level (P12 spec: Byte at Luma's head_cy)
    byte_cx = int(PW * 0.68)
    byte_cy = luma_info["head_cy"]  # same vertical center as Luma's head
    byte_bh = int(DRAW_H * 0.28)

    byte_info = draw_byte_sb(
        char_ctx,
        cx=byte_cx,
        cy=byte_cy,
        body_h=byte_bh,
        expression="still",
        facing="left",
        lean_deg=2.0,
        hovering=True,
        seed=1213,
    )

    # Composite cairo onto PIL
    char_pil = to_pil_rgba(char_surface)
    full_char = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    full_char.paste(char_pil, (0, 0))
    base_rgba = img.convert('RGBA')
    composited = Image.alpha_composite(base_rgba, full_char)
    img = composited.convert('RGB')
    draw = ImageDraw.Draw(img)  # W004

    # Byte glow (subtle)
    add_glow(img, byte_cx, byte_cy, int(byte_bh * 0.5), ELEC_CYAN,
             steps=5, max_alpha=28)
    draw = ImageDraw.Draw(img)  # W004

    # Warm glow on Luma from ambient
    add_glow(img, luma_cx - 15, luma_info["head_cy"], 40, SUNLIT_AMB,
             steps=3, max_alpha=16)
    draw = ImageDraw.Draw(img)  # W004

    # Desat ring on floor below Byte
    ring_cx = byte_cx
    ring_y  = int(DRAW_H * 0.82)
    rw = int(byte_bh * 0.45)
    rh = int(rw * 0.25)
    for ro in range(3):
        draw.ellipse([ring_cx - rw - ro * 3, ring_y - rh - ro,
                      ring_cx + rw + ro * 3, ring_y + rh + ro],
                     outline=DESAT_RING, width=1)

    # ── Breathing space annotation ──────────────────────────────────────────
    font_sm = load_font(8)
    font_ann = load_font(9)

    # Nose-to-nose gap annotation
    gap_left  = luma_info["head_cx"] + luma_info["head_r"]
    gap_right = byte_cx - int(byte_bh * 0.20)
    gap_mid_x = (gap_left + gap_right) // 2
    gap_mid_y = luma_info["head_cy"]

    # Bracket lines for breathing space
    draw.line([(gap_left + 4, gap_mid_y - 15), (gap_left + 4, gap_mid_y + 15)],
              fill=(120, 110, 85), width=1)
    draw.line([(gap_right - 4, gap_mid_y - 15), (gap_right - 4, gap_mid_y + 15)],
              fill=(120, 110, 85), width=1)
    draw.line([(gap_left + 4, gap_mid_y), (gap_right - 4, gap_mid_y)],
              fill=(120, 110, 85), width=1)
    draw.text((gap_mid_x - 20, gap_mid_y - 22),
              "BREATHING\nSPACE", font=font_sm, fill=(140, 128, 95))

    # Sight-line between them
    luma_eye_x = luma_info["head_cx"] + int(luma_info["head_r"] * 0.5)
    luma_eye_y = luma_info["head_cy"]
    byte_face_x = byte_info.get("face_cx", byte_cx - int(byte_bh * 0.15))
    byte_face_y = byte_info.get("face_cy", byte_cy)
    dx = byte_face_x - luma_eye_x
    dy = byte_face_y - luma_eye_y
    dist = math.sqrt(dx**2 + dy**2)
    n_dashes = max(2, int(dist / 10))
    for di in range(n_dashes):
        t0 = di / n_dashes
        t1 = (di + 0.45) / n_dashes
        sx0 = int(luma_eye_x + dx * t0)
        sy0 = int(luma_eye_y + dy * t0)
        sx1 = int(luma_eye_x + dx * t1)
        sy1 = int(luma_eye_y + dy * t1)
        draw.line([(sx0, sy0), (sx1, sy1)], fill=ELEC_CYAN_DIM, width=1)

    # Equal presence labels
    draw.text((luma_cx - 20, DRAW_H - 16), "~30% LUMA",
              font=font_sm, fill=(180, 130, 60))
    draw.text((byte_cx - 20, DRAW_H - 16), "~30% BYTE",
              font=font_sm, fill=ELEC_CYAN_DIM)

    # Camera note
    draw.text((8, 8), "CU TWO-SHOT  |  CENTER-WEIGHTED  |  EQUAL PRESENCE",
              font=font_ann, fill=ANN_COLOR)
    draw.text((8, 20), "Nose-to-nose. Neither cropped or edge-hugging.",
              font=font_sm, fill=(150, 130, 95))

    # Pixel confetti (light, atmospheric)
    for ci in range(8):
        cpx = RNG.randint(int(PW * 0.35), int(PW * 0.65))
        cpy = RNG.randint(int(DRAW_H * 0.15), int(DRAW_H * 0.70))
        cr  = RNG.randint(2, 4)
        cs  = RNG.randint(4, 6)
        cc  = ELEC_CYAN if RNG.random() < 0.7 else HOT_MAGENTA
        draw_irregular_poly(draw, cpx, cpy, cr, cs, cc, seed=ci * 23 + 121)

    # ── Three-tier caption bar ───────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11)
    font_t3   = load_font(9)
    font_meta = load_font(8)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    draw.text((10, DRAW_H + 4),
              "P12  |  CU  |  TWO-SHOT  |  NOSE-TO-NOSE",
              font=font_t1, fill=TEXT_SHOT)
    draw.text((PW - 240, DRAW_H + 5),
              "ARC: CURIOUS / PRE-DISCOVERY", font=font_t2, fill=TEXT_ARC)
    draw.text((10, DRAW_H + 22),
              "Luma and Byte nose-to-nose. Equal presence, center-weighted. Breathing space.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "CRT visible camera-right BG. Byte at Luma's eye level. Neither cropped.",
              font=font_t3, fill=(120, 112, 90))
    draw.text((PW - 310, DRAW_H + 56),
              "LTG_SB_cold_open_P12  /  Diego Vargas  /  C53 (pycairo chars)",
              font=font_meta, fill=TEXT_META)

    # Arc border — cyan
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(str(OUTPUT_PATH), "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return str(OUTPUT_PATH)


if __name__ == "__main__":
    draw_panel()
