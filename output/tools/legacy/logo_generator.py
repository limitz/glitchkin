#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
Logo Generator — "Luma & the Glitchkin"
Show logo / title card for the animated series.

Art Director: Alex Chen
Date: 2026-03-29
Cycle 10

Design brief:
  - "Luma" in warm amber/orange — the Real World, warmth, home
  - "&" in neutral warm white — the bridge
  - "the Glitchkin" in electric cyan with pixel corruption effect — the digital, the glitch world
  - A glitch decoration element (pixel noise / scan-line distortion)
  - Typography: bold, slightly warped/glitchy treatment using Pillow

Color palette (from master_palette.md):
  SUNLIT_AMBER    = (212, 146,  58)   # RW-03
  SOFT_GOLD       = (232, 201,  90)   # RW-02
  ELEC_CYAN       = (  0, 240, 255)   # GL-01
  DEEP_CYAN       = (  0, 168, 180)   # GL-02
  VOID_BLACK      = ( 10,  10,  20)   # GL-06
  HOT_MAGENTA     = (255,  45, 107)   # GL-03 — glitch accent
  STATIC_WHITE    = (240, 240, 240)   # GL-08
  WARM_CREAM      = (250, 240, 220)   # RW-01

Output: /home/wipkat/team/output/production/show_logo.png

Usage: python3 logo_generator.py
"""

import os
import random
import math
from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH = "/home/wipkat/team/output/production/show_logo.png"
W, H = 1200, 480

# ── Master Palette Colors ──────────────────────────────────────────────────────
SUNLIT_AMBER    = (212, 146,  58)   # RW-03 — "Luma" text
SOFT_GOLD       = (232, 201,  90)   # RW-02 — "Luma" highlight / glow
WARM_ORANGE     = (240, 128,  40)   # Slightly deeper orange — "Luma" shadow layer
ELEC_CYAN       = (  0, 240, 255)   # GL-01 — "the Glitchkin" text
DEEP_CYAN       = (  0, 168, 180)   # GL-02 — "the Glitchkin" shadow
HOT_MAGENTA     = (255,  45, 107)   # GL-03 — glitch corruption pixels
VOID_BLACK      = ( 10,  10,  20)   # GL-06 — background
STATIC_WHITE    = (240, 240, 240)   # GL-08 — "&" symbol
WARM_CREAM      = (250, 240, 220)   # RW-01 — "&" secondary tone
UV_PURPLE       = (123,  47, 190)   # GL-04 — glitch decoration
BYTE_TEAL       = (  0, 212, 232)   # GL-01b — "the Glitchkin" mid-tone


def load_font(size=64, bold=False):
    """Load a font, falling back to default if unavailable."""
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def draw_glitch_warp(draw, text, font, base_x, base_y, color, color2, rng, warp_strength=3):
    """
    Draw text with a glitchy/warped treatment:
    - Primary text at base position
    - A shadow/offset layer for depth
    - Horizontal slice shifts (glitch displacement)
    - Pixel noise along the text edge
    """
    # Get text bounding box to measure it
    bbox = font.getbbox(text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Draw shadow (1 color darker/deeper) slightly offset — depth layer
    for sx, sy in [(2, 2), (3, 3)]:
        draw.text((base_x + sx, base_y + sy), text, fill=color2, font=font)

    # Draw main text
    draw.text((base_x, base_y), text, fill=color, font=font)

    # Pixel corruption: small colored squares scattered near the text bounds
    for _ in range(22):
        px = base_x + rng.randint(-8, text_w + 8)
        py = base_y + rng.randint(-4, text_h + 4)
        ps = rng.choice([2, 3, 4, 5])
        pc = rng.choice([HOT_MAGENTA, ELEC_CYAN, UV_PURPLE, STATIC_WHITE])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)


def draw_glitch_cyan_text(draw, text, font, base_x, base_y, rng):
    """
    Draw "the Glitchkin" in electric cyan with pixel corruption effect:
    - Horizontal slice displacement (glitch lines)
    - Chromatic aberration (cyan offset + magenta offset)
    - Pixel scatter along text boundary
    """
    # Shadow layer
    draw.text((base_x + 3, base_y + 3), text, fill=DEEP_CYAN, font=font)

    # Chromatic aberration — magenta ghost offset left/up
    draw.text((base_x - 2, base_y - 2), text, fill=(*HOT_MAGENTA, 80), font=font)

    # Cyan ghost offset right/down
    draw.text((base_x + 2, base_y + 2), text, fill=(*BYTE_TEAL, 120), font=font)

    # Primary cyan text
    draw.text((base_x, base_y), text, fill=ELEC_CYAN, font=font)

    # Glitch horizontal slice displacement — take 4 random rows and shift them slightly
    bbox = font.getbbox(text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Pixel corruption scatter
    for _ in range(40):
        px = base_x + rng.randint(-12, text_w + 12)
        py = base_y + rng.randint(-6, text_h + 6)
        ps = rng.choice([2, 3, 4, 6])
        pc = rng.choice([ELEC_CYAN, HOT_MAGENTA, STATIC_WHITE, UV_PURPLE, (0, 200, 220)])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)


def draw_decoration_element(draw, img, rng):
    """
    Draw a pixel/glitch decoration element below the title text.
    A scan-line bar with pixel noise — suggests a CRT screen or data stream.
    """
    bar_y = int(H * 0.82)
    bar_h = 6
    bar_x0 = int(W * 0.06)
    bar_x1 = int(W * 0.94)

    # Scan-line bar — deep cyan base
    draw.rectangle([bar_x0, bar_y, bar_x1, bar_y + bar_h], fill=DEEP_CYAN)

    # Pixel noise along the scan-line
    for i in range(0, bar_x1 - bar_x0, 8):
        noise_h = rng.randint(1, 14)
        nc = rng.choice([ELEC_CYAN, HOT_MAGENTA, STATIC_WHITE, UV_PURPLE, DEEP_CYAN])
        draw.rectangle([bar_x0 + i, bar_y - noise_h,
                        bar_x0 + i + rng.randint(3, 7), bar_y], fill=nc)

    # A second thinner bar above
    bar2_y = bar_y - 18
    draw.rectangle([bar_x0 + 60, bar2_y, bar_x1 - 60, bar2_y + 2], fill=BYTE_TEAL)
    for i in range(0, bar_x1 - bar_x0 - 120, 12):
        if rng.random() > 0.6:
            draw.rectangle([bar_x0 + 60 + i, bar2_y - rng.randint(1, 6),
                            bar_x0 + 60 + i + rng.randint(2, 5), bar2_y], fill=HOT_MAGENTA)

    # Glitch block elements — small rectangles to either side of the title
    for _ in range(12):
        bx = rng.randint(int(W * 0.02), int(W * 0.08))
        by = rng.randint(int(H * 0.15), int(H * 0.75))
        bw = rng.randint(4, 18)
        bh = rng.randint(2, 8)
        bc = rng.choice([ELEC_CYAN, DEEP_CYAN, HOT_MAGENTA, UV_PURPLE])
        draw.rectangle([bx, by, bx + bw, by + bh], fill=bc)

    for _ in range(12):
        bx = rng.randint(int(W * 0.92), int(W * 0.98))
        by = rng.randint(int(H * 0.15), int(H * 0.75))
        bw = rng.randint(4, 18)
        bh = rng.randint(2, 8)
        bc = rng.choice([ELEC_CYAN, DEEP_CYAN, HOT_MAGENTA, UV_PURPLE])
        draw.rectangle([bx, by, bx + bw, by + bh], fill=bc)


def draw_background(draw, img):
    """
    Dark background with subtle warm-to-cold gradient and scan-line texture.
    Reads as a CRT/digital environment.
    """
    # Near-void dark background — GL-06 Void Black base
    for y in range(H):
        # Subtle vertical gradient: slightly warmer at bottom-left, cooler at top-right
        t = y / H
        r_v = int(VOID_BLACK[0] + 4 * t)
        g_v = int(VOID_BLACK[1] + 2 * t)
        b_v = int(VOID_BLACK[2] + 8 * t)
        draw.line([(0, y), (W, y)], fill=(r_v, g_v, b_v))

    # Very faint scan-lines at low alpha — CRT reference
    scan_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    scan_draw = ImageDraw.Draw(scan_layer)
    for y in range(0, H, 4):
        scan_draw.line([(0, y), (W, y)], fill=(0, 0, 0, 30))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, scan_layer)
    img.paste(base_rgba.convert("RGB"))

    # Warm amber glow — lower left (the Luma / Real World zone)
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    for step in range(12, 0, -1):
        t = step / 12
        rx = int(W * 0.30 * t)
        ry = int(H * 0.40 * t)
        alpha = int(35 * (1 - t))
        glow_draw.ellipse([int(W * 0.05) - rx, int(H * 0.85) - ry,
                           int(W * 0.05) + rx, int(H * 0.85) + ry],
                          fill=(*SOFT_GOLD, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow_layer)
    img.paste(base_rgba.convert("RGB"))

    # Cyan glow — upper right (the Glitchkin / digital zone)
    glow_layer2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw2 = ImageDraw.Draw(glow_layer2)
    for step in range(12, 0, -1):
        t = step / 12
        rx = int(W * 0.32 * t)
        ry = int(H * 0.42 * t)
        alpha = int(30 * (1 - t))
        glow_draw2.ellipse([int(W * 0.92) - rx, int(H * 0.18) - ry,
                            int(W * 0.92) + rx, int(H * 0.18) + ry],
                           fill=(*ELEC_CYAN, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow_layer2)
    img.paste(base_rgba.convert("RGB"))


def draw_luma_amber_glow(draw, img, text_x, text_y, text_w, text_h):
    """
    Add warm amber glow halo behind the 'Luma' text.
    Simulates the warmth/lamp light quality of her character.
    """
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    cx = text_x + text_w // 2
    cy = text_y + text_h // 2
    for step in range(14, 0, -1):
        t = step / 14
        rx = int((text_w // 2 + 30) * t)
        ry = int((text_h // 2 + 20) * t)
        alpha = int(50 * (1 - t))
        glow_draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                          fill=(*SOFT_GOLD, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow_layer)
    img.paste(base_rgba.convert("RGB"))


def draw_glitchkin_cyan_glow(draw, img, text_x, text_y, text_w, text_h):
    """
    Add electric cyan glow halo behind 'the Glitchkin' text.
    Simulates the monitor wall / digital world quality.
    """
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    cx = text_x + text_w // 2
    cy = text_y + text_h // 2
    for step in range(14, 0, -1):
        t = step / 14
        rx = int((text_w // 2 + 24) * t)
        ry = int((text_h // 2 + 18) * t)
        alpha = int(40 * (1 - t))
        glow_draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                          fill=(*ELEC_CYAN, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow_layer)
    img.paste(base_rgba.convert("RGB"))


def generate():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    img = Image.new("RGB", (W, H), VOID_BLACK)
    draw = ImageDraw.Draw(img)

    rng = random.Random(42)  # Fixed seed for reproducibility

    # ── STEP 1: Background ─────────────────────────────────────────────────
    draw_background(draw, img)
    draw = ImageDraw.Draw(img)  # Refresh after background compositing

    # ── STEP 2: Load fonts ─────────────────────────────────────────────────
    font_luma = load_font(size=148, bold=True)       # "Luma" — large, dominant
    font_amp  = load_font(size=80,  bold=False)      # "&" — smaller, neutral
    font_the  = load_font(size=46,  bold=False)      # "the" — small, above Glitchkin
    font_glitch = load_font(size=96, bold=True)      # "Glitchkin" — large, bold cyan

    # ── STEP 3: Measure text for layout ────────────────────────────────────
    luma_bbox    = font_luma.getbbox("Luma")
    luma_w       = luma_bbox[2] - luma_bbox[0]
    luma_h       = luma_bbox[3] - luma_bbox[1]

    amp_bbox     = font_amp.getbbox("&")
    amp_w        = amp_bbox[2] - amp_bbox[0]
    amp_h        = amp_bbox[3] - amp_bbox[1]

    the_bbox     = font_the.getbbox("the")
    the_w        = the_bbox[2] - the_bbox[0]

    glitch_bbox  = font_glitch.getbbox("Glitchkin")
    glitch_w     = glitch_bbox[2] - glitch_bbox[0]
    glitch_h     = glitch_bbox[3] - glitch_bbox[1]

    # Layout: "Luma" top-left area, "&" center, "the Glitchkin" right/below
    # Horizontal layout on a wide canvas:
    #   [  Luma  ]  [&]  [ the\nGlitchkin ]
    margin = int(W * 0.06)
    baseline_y = int(H * 0.18)   # top of text block

    luma_x = margin
    luma_y = baseline_y

    amp_x = luma_x + luma_w + int(W * 0.04)
    amp_y = baseline_y + (luma_h - amp_h) // 2 + 10  # vertically centered with Luma

    glitch_section_x = amp_x + amp_w + int(W * 0.04)
    the_x = glitch_section_x
    the_y = baseline_y + 8
    glitch_x = glitch_section_x
    glitch_y = the_y + int(H * 0.09)

    # ── STEP 4: Luma amber glow behind "Luma" text ─────────────────────────
    draw_luma_amber_glow(draw, img, luma_x, luma_y, luma_w, luma_h)
    draw = ImageDraw.Draw(img)

    # ── STEP 5: Draw "Luma" — warm amber/orange, bold, slight warp ─────────
    draw_glitch_warp(draw, "Luma", font_luma,
                     luma_x, luma_y,
                     color=SUNLIT_AMBER,
                     color2=WARM_ORANGE,
                     rng=rng,
                     warp_strength=3)

    # Soft Gold highlight on top edge of "Luma" letters — warmth/lamp effect
    draw.text((luma_x - 1, luma_y - 1), "Luma", fill=SOFT_GOLD, font=font_luma)
    draw.text((luma_x, luma_y), "Luma", fill=SUNLIT_AMBER, font=font_luma)

    # ── STEP 6: Draw "&" — neutral warm white ─────────────────────────────
    draw.text((amp_x + 2, amp_y + 2), "&", fill=(60, 50, 40), font=font_amp)   # shadow
    draw.text((amp_x, amp_y), "&", fill=WARM_CREAM, font=font_amp)

    # ── STEP 7: Glitchkin cyan glow behind "the Glitchkin" ─────────────────
    draw_glitchkin_cyan_glow(draw, img, glitch_x, the_y, glitch_w + the_w, glitch_h + 60)
    draw = ImageDraw.Draw(img)

    # ── STEP 8: Draw "the" — small, Electric Cyan, above "Glitchkin" ───────
    draw.text((the_x + 2, the_y + 2), "the", fill=DEEP_CYAN, font=font_the)
    draw.text((the_x, the_y), "the", fill=ELEC_CYAN, font=font_the)

    # ── STEP 9: Draw "Glitchkin" — electric cyan, pixel corruption effect ──
    draw_glitch_cyan_text(draw, "Glitchkin", font_glitch, glitch_x, glitch_y, rng)

    # ── STEP 10: Decoration element — pixel/glitch bar ─────────────────────
    draw_decoration_element(draw, img, rng)
    draw = ImageDraw.Draw(img)

    # ── STEP 11: Tagline — REMOVED (Victoria Ashford / Fiona O'Sullivan Cycle 11) ──
    # "A cartoon series by the Dream Team" does not belong on a show title card.
    # Logo shows show title only. Tagline was placeholder text, removed before pitch use.

    # ── STEP 12: Pixel border elements — corner accents ────────────────────
    # Small pixel square in each corner — glitch frame accent
    corner_size = 8
    corner_gap = 14
    corner_colors = [SOFT_GOLD, ELEC_CYAN, HOT_MAGENTA, BYTE_TEAL]
    corners = [
        (corner_gap, corner_gap),
        (W - corner_gap - corner_size, corner_gap),
        (corner_gap, H - corner_gap - corner_size),
        (W - corner_gap - corner_size, H - corner_gap - corner_size),
    ]
    for (cx, cy), cc in zip(corners, corner_colors):
        draw.rectangle([cx, cy, cx + corner_size, cy + corner_size], fill=cc)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
