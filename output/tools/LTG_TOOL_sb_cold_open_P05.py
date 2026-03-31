#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P05.py
Cold Open Panel P05 — MCU MONITOR — Camera Inside Shelf Looking Out
Diego Vargas, Storyboard Artist — Cycle 53

Beat: Camera inside shelf looking out. Pixel cluster growing (8-12 cyan pixels).
Luma's blurred warm form visible in BG through gap. Shelf frame creates a
natural vignette. This is purely environment + pixel VFX — no character
drawing needed (Luma is a blurred warm shape in background).

Output: output/storyboards/panels/LTG_SB_cold_open_P05.png
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

from PIL import Image, ImageDraw, ImageFont, ImageFilter

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P05.png")
os.makedirs(str(PANELS_DIR), exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 72
DRAW_H    = PH - CAPTION_H  # 528

# ── Palette ──────────────────────────────────────────────────────────────────
WARM_CREAM   = (250, 240, 220)
WALL_WARM    = (228, 214, 188)
SHELF_DARK   = (55, 38, 22)
SHELF_INNER  = (42, 30, 18)
SHELF_EDGE   = (75, 55, 35)
LUMA_HOODIE  = (232, 112, 58)
LUMA_SKIN    = (218, 172, 128)
SUNLIT_AMB   = (212, 146, 58)
ELEC_CYAN    = (0, 212, 232)
ELEC_CYAN_DIM = (0, 140, 160)
ELEC_CYAN_HI = (90, 248, 255)
HOT_MAGENTA  = (232, 0, 152)
VOID_BLACK   = (10, 10, 20)
CRT_PHOSPHOR = (40, 55, 48)
BG_CAPTION   = (12, 8, 6)
TEXT_SHOT    = (232, 224, 204)
TEXT_ARC     = ELEC_CYAN
TEXT_DESC    = (155, 148, 122)
TEXT_META    = (88, 82, 66)
ARC_COLOR    = ELEC_CYAN  # CURIOUS / DISCOVERY
ANN_COLOR    = (180, 158, 108)

RNG = random.Random(505)


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
    img  = Image.new('RGB', (PW, PH), SHELF_INNER)
    draw = ImageDraw.Draw(img)

    # ── View through shelf gap ──────────────────────────────────────────────
    # The camera is INSIDE the shelf looking out through a gap.
    # Central opening shows the warm room beyond.

    # Opening dimensions (the gap looking out)
    open_x0 = int(PW * 0.18)
    open_y0 = int(DRAW_H * 0.12)
    open_x1 = int(PW * 0.82)
    open_y1 = int(DRAW_H * 0.88)

    # Room visible through gap — warm tones
    draw.rectangle([open_x0, open_y0, open_x1, open_y1], fill=WALL_WARM)

    # Floor visible through gap
    room_floor = int(DRAW_H * 0.62)
    draw.rectangle([open_x0, room_floor, open_x1, open_y1], fill=(195, 172, 132))

    # Warm ambient in room beyond
    add_glow(img, int(PW * 0.35), int(DRAW_H * 0.40), 140, SUNLIT_AMB,
             steps=5, max_alpha=25)
    draw = ImageDraw.Draw(img)  # W004

    # Luma's blurred warm form in BG (soft, out of focus)
    # Draw Luma as a blurred warm silhouette
    luma_layer = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    ld = ImageDraw.Draw(luma_layer)
    luma_cx = int(PW * 0.42)
    luma_top = int(DRAW_H * 0.28)
    luma_bot = int(DRAW_H * 0.72)
    # Hoodie body shape
    ld.polygon([
        (luma_cx - 28, luma_bot),
        (luma_cx - 22, int(DRAW_H * 0.42)),
        (luma_cx + 22, int(DRAW_H * 0.40)),
        (luma_cx + 28, luma_bot),
    ], fill=(*LUMA_HOODIE, 160))
    # Head
    head_cy = int(DRAW_H * 0.32)
    ld.ellipse([luma_cx - 18, head_cy - 18, luma_cx + 18, head_cy + 18],
               fill=(*LUMA_SKIN, 160))
    # Hair
    ld.ellipse([luma_cx - 22, head_cy - 26, luma_cx + 20, head_cy + 4],
               fill=(*((38, 22, 14)), 160))

    # Blur the Luma layer for out-of-focus effect
    luma_layer = luma_layer.filter(ImageFilter.GaussianBlur(radius=6))

    # Composite blurred Luma onto img
    base_rgba = img.convert('RGBA')
    composited = Image.alpha_composite(base_rgba, luma_layer)
    img = composited.convert('RGB')
    draw = ImageDraw.Draw(img)  # W004

    # ── Shelf frame (dark wood borders) ─────────────────────────────────────
    # Top shelf
    draw.rectangle([0, 0, PW, open_y0], fill=SHELF_DARK)
    draw.rectangle([0, open_y0 - 6, PW, open_y0], fill=SHELF_EDGE)
    # Bottom shelf
    draw.rectangle([0, open_y1, PW, DRAW_H], fill=SHELF_DARK)
    draw.rectangle([0, open_y1, PW, open_y1 + 6], fill=SHELF_EDGE)
    # Left shelf wall
    draw.rectangle([0, 0, open_x0, DRAW_H], fill=SHELF_DARK)
    draw.rectangle([open_x0 - 6, open_y0, open_x0, open_y1], fill=SHELF_EDGE)
    # Right shelf wall
    draw.rectangle([open_x1, 0, PW, DRAW_H], fill=SHELF_DARK)
    draw.rectangle([open_x1, open_y0, open_x1 + 6, open_y1], fill=SHELF_EDGE)

    # Objects on shelf (foreground, partially silhouetted)
    # Book spines on left
    for bi in range(3):
        bx = open_x0 - 45 + bi * 16
        by = int(DRAW_H * 0.50)
        bh = RNG.randint(60, 90)
        bc = RNG.choice([(80, 40, 30), (40, 50, 70), (50, 60, 40)])
        draw.rectangle([bx, by - bh, bx + 12, by], fill=bc)

    # Small object on right (silhouette of rubber duck or figurine)
    duck_x = open_x1 + 12
    duck_y = open_y1 - 30
    draw.ellipse([duck_x, duck_y, duck_x + 20, duck_y + 18],
                 fill=(60, 55, 35))

    # ── Pixel cluster (8-12 cyan pixels) growing on shelf surface ───────────
    # These are the first signs of the glitch world reaching into reality
    cluster_cx = int(PW * 0.55)
    cluster_cy = int(DRAW_H * 0.78)  # on the bottom shelf surface

    pixel_count = 10
    prng = random.Random(5050)
    for pi in range(pixel_count):
        # Cluster in a rough circular pattern
        angle = prng.uniform(0, 2 * math.pi)
        dist  = prng.uniform(0, 22)
        px = cluster_cx + int(dist * math.cos(angle))
        py = cluster_cy + int(dist * math.sin(angle) * 0.6)  # compressed vertically
        pr = prng.randint(3, 7)
        sides = prng.randint(4, 7)
        # Mostly cyan, some brighter
        if prng.random() < 0.7:
            col = ELEC_CYAN
        elif prng.random() < 0.5:
            col = ELEC_CYAN_HI
        else:
            col = HOT_MAGENTA
        draw_irregular_poly(draw, px, py, pr, sides, col, seed=pi * 17 + 505)

    # Pixel cluster glow
    add_glow(img, cluster_cx, cluster_cy, 35, ELEC_CYAN, steps=5, max_alpha=45)
    draw = ImageDraw.Draw(img)  # W004

    # A few stray pixels drifting upward from cluster
    for si in range(4):
        sx = cluster_cx + prng.randint(-30, 30)
        sy = cluster_cy - prng.randint(20, 60)
        sr = prng.randint(2, 4)
        ss = prng.randint(4, 6)
        draw_irregular_poly(draw, sx, sy, sr, ss, ELEC_CYAN_DIM, seed=si * 13 + 707)

    # ── Annotations ──────────────────────────────────────────────────────────
    font_ann = load_font(9)
    font_sm  = load_font(8)

    draw.text((open_x0 + 4, open_y0 + 4),
              "CAMERA INSIDE SHELF — LOOKING OUT", font=font_ann, fill=ANN_COLOR)
    draw.text((open_x0 + 4, open_y0 + 16),
              "Luma's warm blurred form in BG", font=font_sm, fill=(180, 140, 80))

    # Pixel cluster label
    draw.text((cluster_cx + 28, cluster_cy - 8),
              "8-12 CYAN PIXELS\ngrowing", font=font_sm, fill=ELEC_CYAN)

    # ── Three-tier caption bar ───────────────────────────────────────────────
    font_t1   = load_font(13, bold=True)
    font_t2   = load_font(11)
    font_t3   = load_font(9)
    font_meta = load_font(8)

    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 4), width=2)

    draw.text((10, DRAW_H + 4),
              "P05  |  MCU  |  INSIDE SHELF  |  PIXEL CLUSTER",
              font=font_t1, fill=TEXT_SHOT)
    draw.text((PW - 240, DRAW_H + 5),
              "ARC: CURIOUS / DISCOVERY", font=font_t2, fill=TEXT_ARC)
    draw.text((10, DRAW_H + 22),
              "Camera inside shelf looking out. 8-12 cyan pixels clustering. Luma blurred in BG.",
              font=font_t3, fill=TEXT_DESC)
    draw.text((10, DRAW_H + 35),
              "Shelf frame = natural vignette. Pixel cluster on shelf surface, stray pixels drift.",
              font=font_t3, fill=(120, 112, 90))
    draw.text((PW - 310, DRAW_H + 56),
              "LTG_SB_cold_open_P05  /  Diego Vargas  /  C53 (PIL env)",
              font=font_meta, fill=TEXT_META)

    # Arc border — cyan (CURIOUS)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(str(OUTPUT_PATH), "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return str(OUTPUT_PATH)


if __name__ == "__main__":
    draw_panel()
