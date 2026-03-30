#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P25.py — Title Card Panel
Diego Vargas, Storyboard Artist — Cycle 49

P25 — TITLE CARD
"LUMA & THE GLITCHKIN" assembled pixel-by-pixel in Electric Cyan, then
glitch-flashes to Hot Magenta. Final frame of the cold open.

Beat: The title IS the punchline. After all the chaos, the show names itself.
Arc: PITCH BEAT (bright cyan 4px border — this is the hook-close).

Visual grammar:
  - Deep void background (VOID_BLACK) — no environment, just the title
  - Title text rendered in pixel font at large scale
  - "LUMA" in ELEC_CYAN (she is the real-world anchor)
  - "&" small, WARM_CREAM (connector)
  - "THE GLITCHKIN" in HOT_MAGENTA (they are the digital chaos)
  - Pixel confetti scatter (mixed cyan + magenta) — post-breach residue
  - Scanline overlay — CRT aesthetic carries into the title
  - Glitch-flash frame annotation: "FLASH: 2 FRAMES MAGENTA FULL-SCREEN"
  - Static pixel noise along edges (digital instability)

800x600px (528px draw area + 72px caption bar).
"""

import os
import sys
import random

from PIL import Image, ImageDraw, ImageFont

# Import pixel font
sys.path.insert(0, os.path.dirname(__file__))
try:
    from LTG_TOOL_pixel_font_v001 import draw_pixel_text
    _HAS_PIXEL_FONT = True
except ImportError:
    _HAS_PIXEL_FONT = False

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path

# ── Dimensions ─────────────────────────────────────────────────────────────
PW = 800
PH = 600
DRAW_H = 528
CAPTION_H = 72
BORDER_W = 4

# ── Palette ────────────────────────────────────────────────────────────────
VOID_BLACK = (10, 10, 20)
ELEC_CYAN = (0, 212, 232)
HOT_MAGENTA = (232, 0, 152)
WARM_CREAM = (250, 240, 220)
DEEP_SPACE = (6, 6, 14)
CAPTION_BG = (18, 16, 22)

# Caption text colors (3-tier standard)
TEXT_SHOT = (232, 224, 204)
TEXT_ARC = ELEC_CYAN  # PITCH BEAT = bright cyan
TEXT_DESC = (155, 148, 122)
TEXT_META = (88, 82, 66)

# Arc border color: PITCH BEAT = bright cyan
ARC_COLOR = ELEC_CYAN

# ── Font loading ───────────────────────────────────────────────────────────
def load_font(size):
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

FONT_SHOT = load_font(13)
FONT_ARC = load_font(11)
FONT_DESC = load_font(9)
FONT_META = load_font(8)
FONT_ANN = load_font(10)


def draw_scanlines(draw, w, h, spacing=3, alpha_base=25):
    """Draw horizontal CRT scanlines across the draw area."""
    for y in range(0, h, spacing):
        draw.line([(0, y), (w, y)], fill=(0, 0, 0, alpha_base), width=1)


def draw_static_noise(img, rng, density=0.008, margin=40):
    """Draw static pixel noise along the edges of the image."""
    w, h = img.size
    draw = ImageDraw.Draw(img)
    n_pixels = int(w * h * density)
    for _ in range(n_pixels):
        # Bias toward edges
        if rng.random() < 0.7:
            # Edge zone
            side = rng.randint(0, 3)
            if side == 0:  # top
                x, y = rng.randint(0, w - 1), rng.randint(0, margin)
            elif side == 1:  # bottom
                x, y = rng.randint(0, w - 1), rng.randint(h - margin, h - 1)
            elif side == 2:  # left
                x, y = rng.randint(0, margin), rng.randint(0, h - 1)
            else:  # right
                x, y = rng.randint(w - margin, w - 1), rng.randint(0, h - 1)
        else:
            x, y = rng.randint(0, w - 1), rng.randint(0, h - 1)

        if rng.random() < 0.5:
            c = (*ELEC_CYAN, rng.randint(30, 90))
        else:
            c = (*HOT_MAGENTA, rng.randint(30, 90))
        draw.point((x, y), fill=c[:3])
    return draw


def draw_confetti(draw, rng, w, h, count=35):
    """Draw mixed cyan+magenta pixel confetti scatter."""
    for _ in range(count):
        cx = rng.randint(20, w - 20)
        cy = rng.randint(20, h - 20)
        size = rng.randint(2, 5)
        if rng.random() < 0.55:
            color = ELEC_CYAN
        else:
            color = HOT_MAGENTA
        # Irregular polygon (4-7 sides per Cycle 11 standard)
        sides = rng.randint(4, 7)
        import math
        points = []
        for i in range(sides):
            angle = (2 * math.pi * i / sides) + rng.uniform(-0.3, 0.3)
            r = size * rng.uniform(0.6, 1.0)
            px = cx + int(r * math.cos(angle))
            py = cy + int(r * math.sin(angle))
            points.append((px, py))
        draw.polygon(points, fill=color)


def draw_phosphor_bands(draw, w, h, spacing=18):
    """Draw faint phosphor bands (CRT aesthetic)."""
    for y in range(0, h, spacing):
        # Faint green-blue tint band
        draw.rectangle([(0, y), (w, y + 1)], fill=(0, 30, 25))


def generate():
    rng = random.Random(2549)

    # ── Canvas ────────────────────────────────────────────────────────────
    img = Image.new('RGB', (PW, PH), VOID_BLACK)
    draw = ImageDraw.Draw(img)

    # ── Draw area background ──────────────────────────────────────────────
    # Void black with subtle radial gradient (lighter center)
    for y in range(DRAW_H):
        for x in range(PW):
            # Distance from center
            dx = (x - PW // 2) / (PW // 2)
            dy = (y - DRAW_H // 2) / (DRAW_H // 2)
            dist = min(1.0, (dx * dx + dy * dy) ** 0.5)
            # Subtle brightening toward center
            boost = int(8 * (1.0 - dist))
            r = min(255, VOID_BLACK[0] + boost)
            g = min(255, VOID_BLACK[1] + boost)
            b = min(255, VOID_BLACK[2] + boost + 2)
            img.putpixel((x, y), (r, g, b))

    draw = ImageDraw.Draw(img)

    # ── Phosphor bands (subtle CRT texture) ───────────────────────────────
    draw_phosphor_bands(draw, PW, DRAW_H, spacing=18)

    # ── Title text ────────────────────────────────────────────────────────
    if _HAS_PIXEL_FONT:
        # Use pixel font at large scale for authentic look
        # "LUMA" centered, large scale
        title_scale = 5
        amp_scale = 3
        sub_scale = 4

        # Calculate positions for centered layout
        # Each glyph is 5px wide * scale + 1px kerning * scale
        def text_width(text, scale):
            return len(text) * (5 * scale + scale) - scale  # no trailing kern

        luma_w = text_width("LUMA", title_scale)
        amp_w = text_width("&", amp_scale)
        the_w = text_width("THE", sub_scale)
        gk_w = text_width("GLITCHKIN", sub_scale)

        # Vertical layout
        center_y = DRAW_H // 2
        luma_y = center_y - 80
        amp_y = center_y - 20
        the_y = center_y + 30
        gk_y = center_y + 85

        # "LUMA" in ELEC_CYAN
        luma_x = (PW - luma_w) // 2
        draw_pixel_text(draw, luma_x, luma_y, "LUMA", ELEC_CYAN, scale=title_scale)

        # "&" in WARM_CREAM (smaller, connector)
        amp_x = (PW - amp_w) // 2
        draw_pixel_text(draw, amp_x, amp_y, "&", WARM_CREAM, scale=amp_scale)

        # "THE" in HOT_MAGENTA
        the_x = (PW - the_w) // 2
        draw_pixel_text(draw, the_x, the_y, "THE", HOT_MAGENTA, scale=sub_scale)

        # "GLITCHKIN" in HOT_MAGENTA
        gk_x = (PW - gk_w) // 2
        draw_pixel_text(draw, gk_x, gk_y, "GLITCHKIN", HOT_MAGENTA, scale=sub_scale)

    else:
        # Fallback: use system font for title
        big_font = load_font(48)
        med_font = load_font(28)
        sm_font = load_font(36)

        # "LUMA" in ELEC_CYAN
        draw.text((PW // 2, DRAW_H // 2 - 60), "LUMA", fill=ELEC_CYAN,
                   font=big_font, anchor="mm")
        # "&" in WARM_CREAM
        draw.text((PW // 2, DRAW_H // 2), "&", fill=WARM_CREAM,
                   font=med_font, anchor="mm")
        # "THE GLITCHKIN" in HOT_MAGENTA
        draw.text((PW // 2, DRAW_H // 2 + 50), "THE GLITCHKIN", fill=HOT_MAGENTA,
                   font=sm_font, anchor="mm")

    # ── Glow effect around title ──────────────────────────────────────────
    # Create a glow layer (soft bloom from text)
    glow = Image.new('RGB', (PW, DRAW_H), (0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    # Central glow ellipse (cyan dominant)
    from PIL import ImageFilter
    for radius, color, alpha in [
        (180, ELEC_CYAN, 18),
        (120, HOT_MAGENTA, 12),
        (80, ELEC_CYAN, 8),
    ]:
        cx, cy = PW // 2, DRAW_H // 2
        glow_draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            fill=tuple(int(c * alpha / 255) for c in color)
        )

    glow = glow.filter(ImageFilter.GaussianBlur(radius=30))

    # Additive composite (never darkens)
    import numpy as np
    img_arr = np.array(img).astype(np.int16)
    glow_arr = np.array(glow).astype(np.int16)
    # Only apply glow to draw area
    img_arr[:DRAW_H] = np.clip(img_arr[:DRAW_H] + glow_arr, 0, 255)
    img = Image.fromarray(img_arr.astype(np.uint8))
    draw = ImageDraw.Draw(img)

    # ── Pixel confetti (mixed cyan + magenta) ─────────────────────────────
    draw_confetti(draw, rng, PW, DRAW_H, count=35)

    # ── Static noise along edges ──────────────────────────────────────────
    draw = draw_static_noise(img, rng, density=0.006, margin=50)

    # ── Scanlines ─────────────────────────────────────────────────────────
    draw_scanlines(draw, PW, DRAW_H, spacing=3, alpha_base=18)

    # ── Glitch-flash annotation ───────────────────────────────────────────
    ann_y = DRAW_H - 28
    draw.text((PW // 2, ann_y), "FLASH: 2 FRAMES MAGENTA FULL-SCREEN",
              fill=HOT_MAGENTA, font=FONT_ANN, anchor="mm")

    # ── Pixel assembly annotation (top) ───────────────────────────────────
    draw.text((PW // 2, 16), "PIXEL-BY-PIXEL ASSEMBLY (12 FRAMES)",
              fill=ELEC_CYAN, font=FONT_ANN, anchor="mm")

    # ── Arc color border (PITCH BEAT = bright cyan, 4px) ──────────────────
    for i in range(BORDER_W):
        draw.rectangle([i, i, PW - 1 - i, PH - 1 - i], outline=ARC_COLOR)

    # ── Caption bar ───────────────────────────────────────────────────────
    cap_y = DRAW_H
    draw.rectangle([(BORDER_W, cap_y), (PW - BORDER_W - 1, PH - BORDER_W - 1)],
                    fill=CAPTION_BG)

    # Tier 1: Shot code (bold, top-left)
    draw.text((BORDER_W + 8, cap_y + 4), "P25 — TITLE CARD",
              fill=TEXT_SHOT, font=FONT_SHOT)

    # Tier 2: Arc label (top-right, arc color)
    draw.text((PW - BORDER_W - 8, cap_y + 4), "PITCH BEAT",
              fill=TEXT_ARC, font=FONT_ARC, anchor="ra")

    # Tier 3: Narrative description (second row)
    draw.text((BORDER_W + 8, cap_y + 22),
              "\"LUMA & THE GLITCHKIN\" pixel assembly. Cyan>Magenta flash. Cold open close.",
              fill=TEXT_DESC, font=FONT_DESC)

    # Metadata (bottom-right)
    draw.text((PW - BORDER_W - 8, cap_y + CAPTION_H - BORDER_W - 12),
              "800x600 | Diego Vargas C49",
              fill=TEXT_META, font=FONT_META, anchor="ra")

    # ── Save ──────────────────────────────────────────────────────────────
    out_dir = str(output_dir('storyboards', 'panels'))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_SB_cold_open_P25.png")
    img.save(out_path, "PNG")
    print(f"Saved: {out_path} ({img.size[0]}x{img.size[1]})")
    return out_path


if __name__ == "__main__":
    generate()
