#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P10_cairo.py
Cold Open Panel P10 — OTS / Byte POV — Luma Sleeping
Diego Vargas, Storyboard Artist — Cycle 52

PYCAIRO CHARACTER MIGRATION: Same composition as C44 P10. Byte's OTS silhouette
rendered via pycairo (draw_byte_sb) for organic body shape, then darkened to
VOID_BLACK silhouette with ELEC_CYAN rim. Luma remains PIL (sleeping/rear view
not in sb_char_draw).

Output: output/storyboards/panels/LTG_SB_cold_open_P10.png
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
from LTG_TOOL_sb_char_draw import draw_byte_sb

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P10.png")
os.makedirs(str(PANELS_DIR), exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72
DRAW_H    = PH - CAPTION_H  # 528

# ── Palette ──────────────────────────────────────────────────────────────────
WARM_CREAM   = (250, 240, 220)
WARM_AMB     = (212, 146, 58)
LUMA_SKIN    = (218, 172, 128)
LUMA_SKIN_SH = (185, 138, 92)
LUMA_HAIR    = (38, 22, 14)
LUMA_HOODIE  = (232, 112, 58)
COUCH_TOP    = (168, 122, 82)
COUCH_SHADOW = (128, 88, 56)
PILLOW_WARM  = (210, 180, 140)
WALL_WARM    = (228, 214, 188)
MONITOR_GREY = (140, 155, 138)
MONITOR_SCAN = (118, 132, 112)
MONITOR_PLST = (155, 148, 122)
VOID_BLACK   = (10, 10, 20)
ELEC_CYAN    = (0, 212, 232)
ELEC_CYAN_DIM= (0, 140, 160)
ELEC_CYAN_HI = (90, 248, 255)
HOT_MAGENTA  = (232, 0, 152)
BYTE_BODY    = (12, 28, 38)
BG_CAPTION   = (12, 8, 6)
TEXT_SHOT    = (232, 224, 204)
TEXT_ARC     = ELEC_CYAN
TEXT_DESC    = (155, 148, 122)
TEXT_META    = (88, 82, 66)
ARC_COLOR    = ELEC_CYAN
ANN_LINE     = (80, 200, 120)

RNG = random.Random(1010)


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

    # Background wall
    draw.rectangle([0, 0, PW, DRAW_H], fill=WALL_WARM)

    # Background monitors
    for mx, my, mw, mh in [(460, 20, 180, 140), (655, 30, 160, 130), (630, 175, 140, 110)]:
        draw.rectangle([mx, my, mx + mw, my + mh], fill=MONITOR_PLST)
        draw.rectangle([mx + 8, my + 8, mx + mw - 8, my + mh - 8], fill=MONITOR_GREY)
        for sy in range(my + 8, my + mh - 8, 4):
            draw.line([(mx + 8, sy), (mx + mw - 8, sy)], fill=MONITOR_SCAN, width=1)

    # Couch back
    couch_top_y = int(DRAW_H * 0.62)
    draw.rectangle([0, couch_top_y, PW, DRAW_H], fill=COUCH_TOP)
    draw.rectangle([0, couch_top_y, PW, couch_top_y + 12], fill=COUCH_SHADOW)

    # Pillow
    pillow_x1 = int(PW * 0.30)
    pillow_y0 = int(DRAW_H * 0.48)
    draw.rectangle([0, pillow_y0, pillow_x1, couch_top_y + 6], fill=PILLOW_WARM)
    draw.rectangle([0, pillow_y0, pillow_x1, pillow_y0 + 4], fill=COUCH_SHADOW)

    # ── Luma sleeping (PIL — rear view, not in sb_char_draw) ─────────────────
    head_cx = int(PW * 0.42)
    head_cy = int(DRAW_H * 0.42)
    head_r  = int(DRAW_H * 0.16)

    # Hair cloud from behind
    hair_w = int(head_r * 1.6)
    hair_h = int(head_r * 1.3)
    draw.ellipse([head_cx - hair_w, head_cy - hair_h,
                  head_cx + int(hair_w * 0.8), head_cy + int(hair_h * 0.5)],
                 fill=LUMA_HAIR)

    # Hoodie shoulders
    shoulder_y = head_cy + head_r
    draw.rectangle([head_cx - int(head_r * 1.8), shoulder_y,
                    head_cx + int(head_r * 1.0), shoulder_y + int(head_r * 0.9)],
                   fill=LUMA_HOODIE)

    # Cheek visible
    cheek_cx = head_cx + int(head_r * 0.25)
    cheek_cy = head_cy + int(head_r * 0.12)
    cheek_r  = int(head_r * 0.55)
    draw.ellipse([cheek_cx - cheek_r, cheek_cy - cheek_r,
                  cheek_cx + cheek_r, cheek_cy + cheek_r], fill=LUMA_SKIN)
    draw.ellipse([cheek_cx - int(cheek_r * 0.6), cheek_cy + int(cheek_r * 0.5),
                  cheek_cx + int(cheek_r * 0.6), cheek_cy + int(cheek_r * 1.2)],
                 fill=LUMA_SKIN)

    # Closed eye hint
    eye_x = cheek_cx - int(cheek_r * 0.2)
    eye_y = cheek_cy - int(cheek_r * 0.12)
    eye_w = int(cheek_r * 0.55)
    draw.arc([eye_x - eye_w // 2, eye_y - 4, eye_x + eye_w // 2, eye_y + 4],
             start=200, end=340, fill=LUMA_SKIN_SH, width=2)

    # Cyan glow on cheek
    add_glow(img, cheek_cx + int(cheek_r * 0.4), cheek_cy,
             int(head_r * 0.8), ELEC_CYAN, steps=8, max_alpha=38)
    draw = ImageDraw.Draw(img)  # W004

    # ── PYCAIRO: Byte OTS silhouette ─────────────────────────────────────────
    # Render Byte via pycairo for organic shape, then darken to silhouette
    byte_cx_pos = int(PW * 0.80)
    byte_cy_pos = int(DRAW_H * 0.58)
    byte_bh     = int(DRAW_H * 0.36)

    char_surface, char_ctx, _, _ = create_surface(PW, DRAW_H)

    byte_info = draw_byte_sb(
        char_ctx,
        cx=byte_cx_pos,
        cy=byte_cy_pos,
        body_h=byte_bh,
        expression="spotted",
        facing="left",
        lean_deg=1.5,
        hovering=True,
        seed=1010,
    )

    # Convert to PIL, then darken to silhouette
    char_pil = to_pil_rgba(char_surface)

    # Create silhouette: where alpha > 0, replace RGB with BYTE_BODY
    char_arr = np.array(char_pil)
    mask = char_arr[:, :, 3] > 30
    char_arr[mask, 0] = BYTE_BODY[0]
    char_arr[mask, 1] = BYTE_BODY[1]
    char_arr[mask, 2] = BYTE_BODY[2]
    silhouette = Image.fromarray(char_arr, 'RGBA')

    full_char = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    full_char.paste(silhouette, (0, 0))
    base_rgba = img.convert('RGBA')
    composited = Image.alpha_composite(base_rgba, full_char)
    img = composited.convert('RGB')
    draw = ImageDraw.Draw(img)  # W004

    # Cyan rim light on left edge of Byte silhouette
    rim_layer = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rim_layer)
    rim_cx = byte_cx_pos - int(byte_bh * 0.25)
    for ri in range(6, 0, -1):
        r_rim = int(byte_bh * 0.08 * ri / 6)
        a_rim = int(55 * (1 - ri / 7))
        rd.ellipse([rim_cx - r_rim, byte_cy_pos - int(byte_bh * 0.5) - r_rim,
                    rim_cx + r_rim, byte_cy_pos + int(byte_bh * 0.3) + r_rim],
                   fill=(*ELEC_CYAN, a_rim))
    img.paste(Image.alpha_composite(img.convert('RGBA'), rim_layer).convert('RGB'))
    draw = ImageDraw.Draw(img)  # W004

    # Pixel clusters on back
    for pi in range(5):
        px = byte_cx_pos + RNG.randint(-int(byte_bh * 0.2), int(byte_bh * 0.15))
        py = byte_cy_pos - RNG.randint(int(byte_bh * 0.05), int(byte_bh * 0.3))
        pr = RNG.randint(3, 6)
        sides = RNG.randint(4, 6)
        c = ELEC_CYAN if RNG.random() < 0.7 else ELEC_CYAN_HI
        draw_irregular_poly(draw, px, py, pr, sides, c, seed=pi * 7 + 31)

    # Byte ambient glow
    add_glow(img, byte_cx_pos, byte_cy_pos, int(byte_bh * 0.6), ELEC_CYAN,
             steps=10, max_alpha=28)
    draw = ImageDraw.Draw(img)  # W004

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann = load_font(9)
    font_sm  = load_font(8)

    # Sight-line
    byte_eye_x = byte_cx_pos - int(byte_bh * 0.18)
    byte_eye_y = byte_cy_pos - int(byte_bh * 0.32)
    luma_temple_x = head_cx - int(head_r * 0.35)
    luma_temple_y = head_cy - int(head_r * 0.2)

    total_dx = luma_temple_x - byte_eye_x
    total_dy = luma_temple_y - byte_eye_y
    total_dist = math.sqrt(total_dx**2 + total_dy**2)
    steps_sl = max(1, int(total_dist / 10))
    for si in range(steps_sl):
        t0 = si / steps_sl
        t1 = (si + 0.4) / steps_sl
        sx0 = int(byte_eye_x + total_dx * t0)
        sy0 = int(byte_eye_y + total_dy * t0)
        sx1 = int(byte_eye_x + total_dx * t1)
        sy1 = int(byte_eye_y + total_dy * t1)
        draw.line([(sx0, sy0), (sx1, sy1)], fill=ANN_LINE, width=1)

    draw.text((byte_eye_x - 80, byte_eye_y - 18),
              "BYTE POV", font=font_ann, fill=ELEC_CYAN_DIM)
    draw.text((byte_eye_x - 80, byte_eye_y - 8),
              "she doesn't know", font=font_sm, fill=(90, 110, 100))

    draw.text((10, 8), "HIGH-REAR CAMERA", font=font_ann, fill=(95, 88, 72))
    draw.text((10, 20), "OTS / near-POV / elevated-behind", font=font_sm, fill=(75, 68, 55))

    draw.text((cheek_cx + int(cheek_r * 0.5) + 6, cheek_cy - 6),
              "CYAN GLOW\nher cheek", font=font_sm, fill=ELEC_CYAN_DIM)

    # ── Three-tier caption bar ───────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11)
    font_t3   = load_font(9)
    font_meta = load_font(8)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    draw.text((10, DRAW_H + 4),
              "P10  |  OTS  |  HIGH-REAR  |  BYTE POV",
              font=font_t1, fill=TEXT_SHOT)
    draw.text((PW - 230, DRAW_H + 5),
              "ARC: TENSE / PRE-DISCOVERY", font=font_t2, fill=TEXT_ARC)
    draw.text((10, DRAW_H + 22),
              "Byte FG silhouette (cool). Luma BG warm, asleep, unaware. Cyan glow on cheek.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "Dotted sight-line: Byte's eye pos -> Luma's temple. BG monitors: grey-green static.",
              font=font_t3, fill=(120, 112, 90))
    draw.text((PW - 310, DRAW_H + 56),
              "LTG_SB_cold_open_P10  /  Diego Vargas  /  C52 (pycairo chars)",
              font=font_meta, fill=TEXT_META)

    # Arc border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(str(OUTPUT_PATH), "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return str(OUTPUT_PATH)


if __name__ == "__main__":
    draw_panel()
