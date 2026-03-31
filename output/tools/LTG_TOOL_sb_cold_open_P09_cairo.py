#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P09_cairo.py
Cold Open Panel P09 — MED WIDE — Byte Floating / Spots Luma / SPOTTED
Diego Vargas, Storyboard Artist — Cycle 52

PYCAIRO CHARACTER MIGRATION: Same composition, environment, and staging as C43 P09
but Byte drawn with shared pycairo character module (LTG_TOOL_sb_char_draw.py).
Luma remains asleep (background-scale PIL) — sb_char_draw doesn't have a sleeping pose.
Byte gets the full pycairo upgrade with organic bezier curves.

Output: output/storyboards/panels/LTG_SB_cold_open_P09.png
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
from LTG_TOOL_char_byte import draw_byte
from LTG_TOOL_char_luma import draw_luma

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P09.png")
os.makedirs(str(PANELS_DIR), exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72
DRAW_H    = PH - CAPTION_H  # 528

# ── Palette ──────────────────────────────────────────────────────────────────
WARM_CREAM   = (250, 240, 220)
WARM_AMB     = (212, 146, 58)
SUNLIT_AMB   = (212, 146, 58)
LUMA_HOODIE  = (232, 112, 58)
LUMA_SKIN    = (218, 172, 128)
LUMA_HAIR    = (38, 22, 14)
COUCH_WARM   = (158, 112, 72)
COUCH_SHADOW = (120, 82, 50)
COUCH_PILLOW = (200, 170, 130)
WALL_WARM    = (228, 214, 188)
WALL_COOL    = (195, 206, 218)
FLOOR_WARM   = (188, 162, 120)
FLOOR_COOL   = (155, 168, 172)
CRT_PHOSPHOR = (140, 158, 130)
CRT_STATIC_D = (118, 132, 112)
CRT_DARK     = (62, 58, 48)
ELEC_CYAN    = (0, 212, 232)
ELEC_CYAN_DIM= (0, 140, 160)
ELEC_CYAN_FD = (0, 60, 80)
HOT_MAGENTA  = (232, 0, 152)
VOID_BLACK   = (10, 10, 20)
BYTE_TEAL    = (0, 212, 232)
DESAT_RING   = (168, 172, 168)
CONFETTI_C   = (0, 212, 232)
CONFETTI_M   = (232, 0, 152)
BG_CAPTION   = (12, 8, 6)
TEXT_SHOT    = (232, 224, 204)
TEXT_DESC    = (155, 148, 122)
TEXT_META    = (88, 82, 66)
ARC_COLOR    = ELEC_CYAN
ANN_COLOR    = (180, 158, 108)
ANN_DIM      = (130, 118, 88)
ANN_CYAN     = (0, 180, 210)

RNG = random.Random(909)


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
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_irregular_poly(draw, cx, cy, r, sides, color, seed=0, outline=None):
    rng = random.Random(seed)
    pts = []
    for i in range(sides):
        angle = (2 * math.pi * i / sides) + rng.uniform(-0.28, 0.28)
        dist  = r * rng.uniform(0.68, 1.22)
        pts.append((int(cx + dist * math.cos(angle)), int(cy + dist * math.sin(angle))))
    draw.polygon(pts, fill=color, outline=outline)


def draw_confetti_gravity(draw, byte_cx, byte_feet_y, count, rng_seed):
    rng = random.Random(rng_seed)
    for i in range(count):
        dx   = rng.randint(-int(PW * 0.20), int(PW * 0.20))
        dy   = rng.randint(0, int(DRAW_H * 0.25))
        px   = byte_cx + dx
        py   = byte_feet_y + dy
        if 0 < px < PW and 0 < py < DRAW_H:
            r     = rng.randint(1, 4)
            sides = rng.randint(4, 7)
            col   = CONFETTI_C if rng.randint(0, 2) != 0 else CONFETTI_M
            draw_irregular_poly(draw, px, py, r, sides, col, seed=i * 37 + rng_seed)


def draw_confetti_trail(draw, from_x, from_y, to_x, to_y, count, rng_seed):
    rng = random.Random(rng_seed)
    for i in range(count):
        t   = rng.uniform(0, 1)
        px  = int(from_x + t * (to_x - from_x)) + rng.randint(-20, 20)
        py  = int(from_y + t * (to_y - from_y)) + rng.randint(-15, 15)
        if 0 < px < PW and 0 < py < DRAW_H:
            r     = rng.randint(1, 3)
            sides = rng.randint(4, 6)
            col   = CONFETTI_C if rng.randint(0, 3) != 0 else CONFETTI_M
            draw_irregular_poly(draw, px, py, r, sides, col, seed=i * 53 + rng_seed)


def _char_to_pil(surface):
    """Convert a cairo.ImageSurface from canonical char module to cropped PIL RGBA."""
    pil_img = to_pil_rgba(surface)
    bbox = pil_img.getbbox()
    if bbox:
        pil_img = pil_img.crop(bbox)
    return pil_img


def _composite_char(base_img, char_pil, cx, cy):
    """Composite a character PIL RGBA image onto base_img centered at (cx, cy)."""
    x = cx - char_pil.width // 2
    y = cy - char_pil.height // 2
    overlay = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    overlay.paste(char_pil, (x, y), char_pil)
    base_rgba = base_img.convert('RGBA')
    result = Image.alpha_composite(base_rgba, overlay)
    base_img.paste(result.convert('RGB'))


def draw_luma_asleep(img, draw, luma_head_cx, luma_head_cy):
    """Luma asleep on couch — canonical renderer (WORRIED as sleeping stand-in).

    Draws couch/pillow environment, then composites canonical Luma rotated slightly
    to suggest sleeping posture.
    """
    scale = 0.70
    body_h_luma = int(DRAW_H * 0.28 * scale)
    head_r_l    = int(body_h_luma * 0.22)

    # Couch behind Luma (draw first)
    couch_x = luma_head_cx - int(head_r_l * 1.25) - int(head_r_l * 0.6)
    couch_y = luma_head_cy + int(head_r_l * 0.8)
    couch_w = int(head_r_l * 2.5 * 2.4)
    couch_h = int(body_h_luma * 0.75)
    draw.rectangle([couch_x, couch_y, couch_x + couch_w, couch_y + couch_h],
                   fill=COUCH_WARM, outline=COUCH_SHADOW)

    # Pillow under head
    pillow_pts = [
        (luma_head_cx - int(head_r_l * 1.5),  luma_head_cy - int(head_r_l * 0.60)),
        (luma_head_cx + int(head_r_l * 1.5),  luma_head_cy - int(head_r_l * 0.60)),
        (luma_head_cx + int(head_r_l * 1.3),  luma_head_cy + int(head_r_l * 0.65)),
        (luma_head_cx - int(head_r_l * 1.3),  luma_head_cy + int(head_r_l * 0.65)),
    ]
    draw.polygon(pillow_pts, fill=COUCH_PILLOW, outline=COUCH_SHADOW)

    # Canonical Luma renderer — WORRIED as sleeping stand-in
    surface = draw_luma(expression="WORRIED", scale=0.3, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        char_pil = char_pil.resize(
            (int(char_pil.width * 0.6), int(char_pil.height * 0.6)), Image.LANCZOS)
    # Rotate slightly for sleeping posture
    char_pil = char_pil.rotate(15, expand=True, fillcolor=(0, 0, 0, 0))
    _composite_char(img, char_pil, luma_head_cx, luma_head_cy)


def draw_background_monitors(draw):
    for bm_x, bm_y, bm_w, bm_h in [
        (int(PW * 0.50), int(DRAW_H * 0.04), int(PW * 0.14), int(DRAW_H * 0.22)),
        (int(PW * 0.68), int(DRAW_H * 0.08), int(PW * 0.12), int(DRAW_H * 0.18)),
        (int(PW * 0.82), int(DRAW_H * 0.05), int(PW * 0.10), int(DRAW_H * 0.20)),
    ]:
        draw.rectangle([bm_x, bm_y, bm_x + bm_w, bm_y + bm_h],
                       fill=CRT_DARK, outline=(50, 46, 38))
        sm = 5
        draw.rectangle([bm_x + sm, bm_y + sm, bm_x + bm_w - sm, bm_y + bm_h - sm],
                       fill=CRT_PHOSPHOR)
        for sl in range(bm_y + sm + 1, bm_y + bm_h - sm, 3):
            draw.line([(bm_x + sm, sl), (bm_x + bm_w - sm, sl)],
                      fill=CRT_STATIC_D, width=1)


def draw_panel():
    img  = Image.new('RGB', (PW, PH), WALL_WARM)
    draw = ImageDraw.Draw(img)

    horizon_y = int(DRAW_H * 0.38)

    # Wall — warm left, cool right
    for x in range(PW):
        t = x / PW
        c = lerp_color(WALL_WARM, WALL_COOL, t * 0.55)
        draw.line([(x, 0), (x, horizon_y)], fill=c)

    # Floor
    draw.rectangle([0, horizon_y, PW, DRAW_H], fill=FLOOR_WARM)
    vp_x = int(PW * 0.48)
    for frac in [0.07, 0.20, 0.36, 0.52, 0.67, 0.80, 0.93]:
        fx = int(frac * PW)
        draw.line([(vp_x, horizon_y), (fx, DRAW_H)], fill=FLOOR_COOL, width=1)

    # BG monitors
    draw_background_monitors(draw)

    # Warm lamp glow
    add_glow(img, int(PW * 0.10), int(DRAW_H * 0.06), 120, WARM_AMB, steps=4, max_alpha=22)
    draw = ImageDraw.Draw(img)  # W004

    # Luma asleep (PIL — background scale)
    luma_head_x = int(PW * 0.18)
    luma_head_y = int(DRAW_H * 0.38)
    draw_luma_asleep(img, draw, luma_head_x, luma_head_y)
    draw = ImageDraw.Draw(img)  # W004

    add_glow(img, luma_head_x, luma_head_y, 65, WARM_AMB, steps=4, max_alpha=16)
    draw = ImageDraw.Draw(img)  # W004

    # ── PYCAIRO CHARACTER: Byte floating ─────────────────────────────────────
    byte_cx   = int(PW * 0.65)
    byte_cy   = int(DRAW_H * 0.40)
    byte_bh   = int(DRAW_H * 0.30)
    floor_y   = int(DRAW_H * 0.78)

    # Canonical Byte renderer — "searching" is closest to "spotted"
    byte_scale = byte_bh / 88.0
    byte_surface = draw_byte(expression="searching", scale=byte_scale, facing="left")
    byte_pil = _char_to_pil(byte_surface)
    if byte_pil.height > 0:
        aspect = byte_pil.width / byte_pil.height
        new_h = byte_bh
        new_w = int(new_h * aspect)
        byte_pil = byte_pil.resize((new_w, new_h), Image.LANCZOS)
    _composite_char(img, byte_pil, byte_cx, byte_cy)
    draw = ImageDraw.Draw(img)  # W004

    # Compute face position for sight-line annotation
    byte_head_r = int(byte_bh * 0.20)
    byte_face_cx = byte_cx - int(byte_head_r * 0.6)
    byte_face_cy = byte_cy - byte_bh // 2 + byte_head_r

    # Byte glow
    add_glow(img, byte_cx, byte_cy, int(byte_bh * 0.55), ELEC_CYAN, steps=6, max_alpha=35)
    draw = ImageDraw.Draw(img)  # W004

    # Gravity ghost confetti
    feet_y = byte_cy + byte_bh // 2
    draw_confetti_gravity(draw, byte_cx, feet_y, count=35, rng_seed=991)

    # Confetti trail
    emerge_x = int(PW * 0.52)
    emerge_y = int(DRAW_H * 0.60)
    draw_confetti_trail(draw, emerge_x, emerge_y, byte_cx, byte_cy,
                        count=20, rng_seed=992)

    # Desaturation ring on floor below Byte
    ring_cx = byte_cx
    ring_y  = floor_y
    rw      = int(byte_bh * 0.50)
    rh      = int(rw * 0.28)
    for ro in range(3):
        draw.ellipse([ring_cx - rw - ro * 4, ring_y - rh - ro,
                      ring_cx + rw + ro * 4, ring_y + rh + ro],
                     outline=DESAT_RING, width=1)

    # Sight-line annotation
    sight_x1 = byte_face_cx
    sight_y1 = byte_face_cy
    sight_x2, sight_y2 = luma_head_x, luma_head_y
    dist     = math.sqrt((sight_x2 - sight_x1) ** 2 + (sight_y2 - sight_y1) ** 2)
    n_dashes = max(2, int(dist / 14))
    for di in range(n_dashes):
        t0 = di / n_dashes
        t1 = (di + 0.55) / n_dashes
        x0_d = int(sight_x1 + t0 * (sight_x2 - sight_x1))
        y0_d = int(sight_y1 + t0 * (sight_y2 - sight_y1))
        x1_d = int(sight_x1 + t1 * (sight_x2 - sight_x1))
        y1_d = int(sight_y1 + t1 * (sight_y2 - sight_y1))
        draw.line([(x0_d, y0_d), (x1_d, y1_d)], fill=ELEC_CYAN_DIM, width=1)

    mid_x = (sight_x1 + sight_x2) // 2
    mid_y = (sight_y1 + sight_y2) // 2 - 10
    font_sm = load_font(8)
    draw.text((mid_x, mid_y), "sight-line", font=font_sm, fill=ELEC_CYAN_DIM)

    # Float gap annotation
    ann_x = byte_cx + int(byte_bh * 0.55)
    draw.line([(ann_x, feet_y), (ann_x, floor_y)], fill=ELEC_CYAN_DIM, width=1)
    draw.polygon([(ann_x - 3, feet_y + 7), (ann_x + 3, feet_y + 7), (ann_x, feet_y)],
                 fill=ELEC_CYAN_DIM)
    draw.polygon([(ann_x - 3, floor_y - 7), (ann_x + 3, floor_y - 7), (ann_x, floor_y)],
                 fill=ELEC_CYAN_DIM)
    draw.text((ann_x + 4, (feet_y + floor_y) // 2 - 5),
              "18\"\nfloat", font=font_sm, fill=ELEC_CYAN_DIM)

    # Annotations
    font_ann   = load_font(9)
    font_ann_b = load_font(9, bold=True)
    draw.text((8, 8), 'MED WIDE  |  4-5FT  |  FLAT HORIZON  |  BYTE SPOTTED',
              font=font_ann, fill=ANN_COLOR)

    draw.text((8, DRAW_H - 16),
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
              "P09  |  MED WIDE  |  4-5FT  |  BYTE SPOTTED  |  LUMA ASLEEP",
              font=font_t1, fill=TEXT_SHOT)
    draw.text((PW - 260, DRAW_H + 5),
              "ARC: CURIOUS / FIRST ENCOUNTER", font=font_t2, fill=ELEC_CYAN)
    draw.text((10, DRAW_H + 22),
              "Byte floating 18\" off floor. Spots Luma asleep on couch. Iris shifted LEFT.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "Gravity ghost: confetti drifts DOWN. BG monitors: normal static. Warm/cool gradient.",
              font=font_t3, fill=(120, 112, 90))
    draw.text((PW - 310, DRAW_H + 56),
              "LTG_SB_cold_open_P09  /  Diego Vargas  /  C52 (pycairo chars)",
              font=font_meta, fill=TEXT_META)

    # Arc border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(str(OUTPUT_PATH), "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return str(OUTPUT_PATH)


if __name__ == "__main__":
    draw_panel()
