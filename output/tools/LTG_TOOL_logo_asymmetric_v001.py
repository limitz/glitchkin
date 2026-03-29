#!/usr/bin/env python3
"""
Logo Generator — "Luma & the Glitchkin" — ASYMMETRIC LAYOUT
Alternative logo composition exploring left-anchored dominance.

Art Director: Alex Chen
Date: 2026-03-30
Cycle: 12

Design brief (Victoria Ashford C11 A+ P2):
  Current layout: balanced horizontal spread [Luma] [&] [the Glitchkin]
  Asymmetric layout:
    - "Luma" larger and left-anchored (dominant visual weight, ~40% of canvas width)
    - "& the" small connector — mid-canvas bridge
    - "Glitchkin" smaller + stacked (name broken into two lines), right side
    - Glitch treatment (chromatic aberration, pixel scatter, horizontal slices) acts as
      VISUAL COUNTERWEIGHT on the right — even though "Glitchkin" is physically smaller,
      its digital energy fills the right zone with motion and weight
    - Result: warm heaviness on the left (Luma = presence, solidity) vs
              cold fragmentation on the right (Glitchkin = energy, instability)
      The two halves balance through contrast, not symmetry.

  The asymmetry also suggests the narrative dynamic: Luma grounds the world;
  the Glitchkin fills it with chaos.

Color palette (from master_palette.md):
  SUNLIT_AMBER    = (212, 146,  58)   # RW-03 — "Luma" text
  SOFT_GOLD       = (232, 201,  90)   # RW-02 — warm highlight
  ELEC_CYAN       = (  0, 240, 255)   # GL-01 — "the Glitchkin" text
  DEEP_CYAN       = (  0, 168, 180)   # GL-02 — shadow
  VOID_BLACK      = ( 10,  10,  20)   # GL-06 — background
  HOT_MAGENTA     = (255,  45, 107)   # GL-03 — glitch accent
  STATIC_WHITE    = (240, 240, 240)   # GL-08
  WARM_CREAM      = (250, 240, 220)   # RW-01

Output: /home/wipkat/team/output/production/LTG_BRAND_logo_asymmetric_v001.png
"""

import os
import random
import math
from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH = "/home/wipkat/team/output/production/LTG_BRAND_logo_asymmetric_v001.png"
W, H = 1200, 480

# ── Master Palette Colors ──────────────────────────────────────────────────────
SUNLIT_AMBER    = (212, 146,  58)
SOFT_GOLD       = (232, 201,  90)
WARM_ORANGE     = (240, 128,  40)
ELEC_CYAN       = (  0, 240, 255)
DEEP_CYAN       = (  0, 168, 180)
HOT_MAGENTA     = (255,  45, 107)
VOID_BLACK      = ( 10,  10,  20)
STATIC_WHITE    = (240, 240, 240)
WARM_CREAM      = (250, 240, 220)
UV_PURPLE       = (123,  47, 190)
BYTE_TEAL       = (  0, 212, 232)


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
    """Draw text with warm glitchy treatment — shadow offset + pixel noise."""
    bbox = font.getbbox(text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    # Shadow layers
    for sx, sy in [(2, 2), (3, 3)]:
        draw.text((base_x + sx, base_y + sy), text, fill=color2, font=font)
    # Main text
    draw.text((base_x, base_y), text, fill=color, font=font)
    # Pixel corruption — warm zone
    for _ in range(22):
        px = base_x + rng.randint(-8, text_w + 8)
        py = base_y + rng.randint(-4, text_h + 4)
        ps = rng.choice([2, 3, 4, 5])
        pc = rng.choice([SOFT_GOLD, WARM_ORANGE, WARM_CREAM, HOT_MAGENTA])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)


def draw_glitch_cyan_text(draw, text, font, base_x, base_y, rng, scatter_count=40):
    """Draw "Glitchkin" text with heavy glitch treatment — this is the visual counterweight."""
    bbox = font.getbbox(text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Heavy chromatic aberration — more pronounced than the symmetric version
    # because this is the visual counterweight: the glitch energy must read as BIG
    for sx, sy, col, a in [
        (4, 4, DEEP_CYAN, None),            # deep shadow
        (-3, -3, (*HOT_MAGENTA, 100), None), # magenta ghost upper-left
        (3, 3, (*BYTE_TEAL, 130), None),     # cyan ghost lower-right
        (-1, 1, (*UV_PURPLE, 70), None),     # purple ghost diagonal
    ]:
        c = col if isinstance(col, tuple) and len(col) == 3 else None
        ca = col if isinstance(col, tuple) and len(col) == 4 else None
        if c:
            draw.text((base_x + sx, base_y + sy), text, fill=c, font=font)
        else:
            draw.text((base_x + sx, base_y + sy), text, fill=ca, font=font)

    # Primary text
    draw.text((base_x, base_y), text, fill=ELEC_CYAN, font=font)

    # Horizontal slice displacement — glitch lines cut through the text
    # Take 6 random horizontal bands and shift them right slightly
    slice_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    slice_draw  = ImageDraw.Draw(slice_layer)
    for _ in range(6):
        slice_y  = base_y + rng.randint(4, text_h - 8)
        slice_h  = rng.randint(3, 8)
        shift_x  = rng.choice([-6, -4, 5, 7, 10])
        # Cut out a horizontal slice and render a shifted ghost in magenta
        slice_draw.rectangle([base_x + shift_x, slice_y,
                               base_x + text_w + shift_x, slice_y + slice_h],
                              fill=(*HOT_MAGENTA, 60))

    # Heavy pixel scatter — RIGHT side of logo, fills the right zone with visual energy
    # Scatter count is higher than symmetric version — asymmetric counterweight
    for _ in range(scatter_count):
        px = base_x + rng.randint(-20, text_w + 40)
        py = base_y + rng.randint(-14, text_h + 20)
        ps = rng.choice([2, 3, 4, 6, 8])   # larger max size — more visual weight
        pc = rng.choice([ELEC_CYAN, HOT_MAGENTA, STATIC_WHITE, UV_PURPLE,
                         BYTE_TEAL, (0, 200, 220)])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)

    return slice_layer


def draw_background(draw, img):
    """
    Dark background with asymmetric warm-left / cold-right zone structure.
    More pronounced division than the symmetric layout — matches the asymmetric text.
    """
    # Near-void dark background gradient
    for y in range(H):
        t = y / H
        r_v = int(VOID_BLACK[0] + 4 * t)
        g_v = int(VOID_BLACK[1] + 2 * t)
        b_v = int(VOID_BLACK[2] + 8 * t)
        draw.line([(0, y), (W, y)], fill=(r_v, g_v, b_v))

    # Faint scan-lines — CRT reference
    scan_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    scan_draw  = ImageDraw.Draw(scan_layer)
    for y in range(0, H, 4):
        scan_draw.line([(0, y), (W, y)], fill=(0, 0, 0, 28))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, scan_layer)
    img.paste(base_rgba.convert("RGB"))

    # LARGE warm amber glow — left half (Luma zone, more dominant than symmetric layout)
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw  = ImageDraw.Draw(glow_layer)
    for step in range(16, 0, -1):
        t = step / 16
        rx = int(W * 0.38 * t)   # bigger than symmetric (W*0.30)
        ry = int(H * 0.55 * t)
        alpha = int(42 * (1 - t))
        glow_draw.ellipse([int(W * 0.03) - rx, int(H * 0.80) - ry,
                           int(W * 0.03) + rx, int(H * 0.80) + ry],
                          fill=(*SOFT_GOLD, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow_layer)
    img.paste(base_rgba.convert("RGB"))

    # Secondary warm halo behind Luma text area (upper-left)
    glow_layer2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw2  = ImageDraw.Draw(glow_layer2)
    for step in range(10, 0, -1):
        t = step / 10
        rx = int(W * 0.26 * t)
        ry = int(H * 0.38 * t)
        alpha = int(28 * (1 - t))
        glow_draw2.ellipse([int(W * 0.18) - rx, int(H * 0.35) - ry,
                            int(W * 0.18) + rx, int(H * 0.35) + ry],
                           fill=(*SUNLIT_AMBER, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow_layer2)
    img.paste(base_rgba.convert("RGB"))

    # CONCENTRATED cyan glow — right quarter (Glitchkin zone)
    # Narrower X-spread but taller to fill the stacked text column
    glow_layer3 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw3  = ImageDraw.Draw(glow_layer3)
    for step in range(14, 0, -1):
        t = step / 14
        rx = int(W * 0.22 * t)   # narrower — right-anchored
        ry = int(H * 0.54 * t)   # taller — compensates for the stacked text
        alpha = int(36 * (1 - t))
        glow_draw3.ellipse([int(W * 0.88) - rx, int(H * 0.50) - ry,
                            int(W * 0.88) + rx, int(H * 0.50) + ry],
                           fill=(*ELEC_CYAN, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow_layer3)
    img.paste(base_rgba.convert("RGB"))

    # Vertical divider mark at the boundary (~50% width) — subtle geometric beat
    # A single 1px line in DEEP_CYAN at very low alpha — just readable enough
    divider_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    divider_draw  = ImageDraw.Draw(divider_layer)
    divider_x = int(W * 0.50)
    divider_draw.line([(divider_x, int(H * 0.10)), (divider_x, int(H * 0.90))],
                      fill=(*DEEP_CYAN, 25), width=1)
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, divider_layer)
    img.paste(base_rgba.convert("RGB"))


def draw_luma_amber_glow(img, text_x, text_y, text_w, text_h):
    """Warm amber glow halo behind 'Luma' — larger for the asymmetric dominant version."""
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw  = ImageDraw.Draw(glow_layer)
    cx = text_x + text_w // 2
    cy = text_y + text_h // 2
    for step in range(16, 0, -1):
        t = step / 16
        rx = int((text_w // 2 + 50) * t)   # bigger halo than symmetric (+50 vs +30)
        ry = int((text_h // 2 + 36) * t)
        alpha = int(55 * (1 - t))           # slightly stronger
        glow_draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                          fill=(*SOFT_GOLD, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow_layer)
    img.paste(base_rgba.convert("RGB"))


def draw_glitchkin_cyan_glow(img, text_x, text_y, text_w, text_h):
    """Concentrated cyan glow behind 'Glitchkin' stack — taller/narrower as counterweight."""
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw  = ImageDraw.Draw(glow_layer)
    cx = text_x + text_w // 2
    cy = text_y + text_h // 2
    for step in range(16, 0, -1):
        t = step / 16
        rx = int((text_w // 2 + 32) * t)
        ry = int((text_h // 2 + 44) * t)   # taller than wide — stacked text geometry
        alpha = int(48 * (1 - t))
        glow_draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                          fill=(*ELEC_CYAN, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow_layer)
    img.paste(base_rgba.convert("RGB"))


def generate():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    img  = Image.new("RGB", (W, H), VOID_BLACK)
    draw = ImageDraw.Draw(img)
    rng  = random.Random(42)   # fixed seed for reproducibility

    # ── STEP 1: Background ─────────────────────────────────────────────────
    draw_background(draw, img)
    draw = ImageDraw.Draw(img)

    # ── STEP 2: Load fonts ─────────────────────────────────────────────────
    # Asymmetric layout: "Luma" MUCH larger — 180px vs 148px in symmetric
    # "the" and "Glitchkin" smaller and stacked vertically on the right
    font_luma    = load_font(size=180, bold=True)   # dominant left anchor
    font_amp     = load_font(size=56,  bold=False)  # smaller bridge
    font_the     = load_font(size=38,  bold=False)  # small label above Glitchkin stack
    font_glitch  = load_font(size=72,  bold=True)   # Glitchkin — smaller than Luma

    # ── STEP 3: Measure text ───────────────────────────────────────────────
    luma_bbox   = font_luma.getbbox("Luma")
    luma_w      = luma_bbox[2] - luma_bbox[0]
    luma_h      = luma_bbox[3] - luma_bbox[1]

    amp_bbox    = font_amp.getbbox("&")
    amp_w       = amp_bbox[2] - amp_bbox[0]
    amp_h       = amp_bbox[3] - amp_bbox[1]

    the_bbox    = font_the.getbbox("the")
    the_w       = the_bbox[2] - the_bbox[0]
    the_h       = the_bbox[3] - the_bbox[1]

    glitch_bbox = font_glitch.getbbox("Glitchkin")
    glitch_w    = glitch_bbox[2] - glitch_bbox[0]
    glitch_h    = glitch_bbox[3] - glitch_bbox[1]

    # ── STEP 4: Layout ─────────────────────────────────────────────────────
    # "Luma" — left-anchored, vertically centered
    margin    = int(W * 0.05)
    luma_x    = margin
    luma_y    = (H - luma_h) // 2 - int(H * 0.04)  # slightly above center

    # "&" — small connector, placed at mid-right of "Luma", vertically mid
    amp_x  = luma_x + luma_w + int(W * 0.025)
    amp_y  = luma_y + luma_h - amp_h - int(H * 0.06)  # baseline-aligned with Luma bottom

    # "the" — small text above "Glitchkin", right-side stack
    # Stack x-position: after the "&", roughly right 35% of canvas
    stack_x   = amp_x + amp_w + int(W * 0.028)
    the_x     = stack_x
    # Align "the" to start the stack — top-of-stack is at luma top
    the_y     = luma_y + int(luma_h * 0.08)

    # "Glitchkin" — below "the", same left edge
    glitch_x  = stack_x
    glitch_y  = the_y + the_h + int(H * 0.04)

    # ── STEP 5: Glow layers behind text ───────────────────────────────────
    draw_luma_amber_glow(img, luma_x, luma_y, luma_w, luma_h)
    draw = ImageDraw.Draw(img)

    # Glow behind full "the Glitchkin" stack
    stack_total_h = (glitch_y + glitch_h) - the_y
    stack_total_w = max(the_w, glitch_w)
    draw_glitchkin_cyan_glow(img, glitch_x, the_y, stack_total_w, stack_total_h)
    draw = ImageDraw.Draw(img)

    # ── STEP 6: Draw "Luma" — dominant, warm amber, slight warp ───────────
    draw_glitch_warp(draw, "Luma", font_luma,
                     luma_x, luma_y,
                     color=SUNLIT_AMBER,
                     color2=WARM_ORANGE,
                     rng=rng,
                     warp_strength=3)
    # Soft gold highlight pass
    draw.text((luma_x - 1, luma_y - 1), "Luma", fill=SOFT_GOLD, font=font_luma)
    draw.text((luma_x, luma_y), "Luma", fill=SUNLIT_AMBER, font=font_luma)

    # ── STEP 7: Draw "&" — small neutral bridge ────────────────────────────
    draw.text((amp_x + 2, amp_y + 2), "&", fill=(60, 50, 40), font=font_amp)
    draw.text((amp_x, amp_y), "&", fill=WARM_CREAM, font=font_amp)

    # ── STEP 8: Draw "the" — small, above Glitchkin stack ─────────────────
    draw.text((the_x + 2, the_y + 2), "the", fill=DEEP_CYAN, font=font_the)
    draw.text((the_x, the_y), "the", fill=ELEC_CYAN, font=font_the)

    # ── STEP 9: Draw "Glitchkin" — electric cyan, heavy glitch treatment ──
    # Scatter count raised to 60 for the asymmetric version — more visual weight
    slice_layer = draw_glitch_cyan_text(draw, "Glitchkin", font_glitch,
                                         glitch_x, glitch_y, rng,
                                         scatter_count=60)
    # Apply the horizontal glitch slice layer
    base_rgba = img.convert("RGBA")
    img_with_slices = Image.alpha_composite(base_rgba, slice_layer)
    img.paste(img_with_slices.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # ── STEP 10: Pixel border accents ─────────────────────────────────────
    # Asymmetric: warm corner accents on LEFT two corners, cold on RIGHT two
    corner_size = 8
    corner_gap  = 14
    corners_warm = [
        (corner_gap, corner_gap),
        (corner_gap, H - corner_gap - corner_size),
    ]
    corners_cold = [
        (W - corner_gap - corner_size, corner_gap),
        (W - corner_gap - corner_size, H - corner_gap - corner_size),
    ]
    for cx, cy in corners_warm:
        draw.rectangle([cx, cy, cx + corner_size, cy + corner_size], fill=SOFT_GOLD)
    for cx, cy in corners_cold:
        draw.rectangle([cx, cy, cx + corner_size, cy + corner_size], fill=ELEC_CYAN)

    # ── STEP 11: Decoration element — scan-line bar below text ────────────
    bar_y  = int(H * 0.84)
    bar_h  = 5
    bar_x0 = int(W * 0.05)
    bar_x1 = int(W * 0.95)
    # Bi-color bar: warm on left half, cold on right half
    mid_bar = (bar_x0 + bar_x1) // 2
    draw.rectangle([bar_x0, bar_y, mid_bar, bar_y + bar_h], fill=SUNLIT_AMBER)
    draw.rectangle([mid_bar, bar_y, bar_x1, bar_y + bar_h], fill=DEEP_CYAN)
    # Pixel noise on bar
    for i in range(0, bar_x1 - bar_x0, 8):
        noise_h = rng.randint(1, 12)
        side_x  = bar_x0 + i
        if side_x < mid_bar:
            nc = rng.choice([SOFT_GOLD, SUNLIT_AMBER, WARM_CREAM, HOT_MAGENTA])
        else:
            nc = rng.choice([ELEC_CYAN, BYTE_TEAL, STATIC_WHITE, HOT_MAGENTA])
        draw.rectangle([side_x, bar_y - noise_h,
                        side_x + rng.randint(3, 7), bar_y], fill=nc)

    # ── STEP 12: Layout descriptor text (small, bottom) ──────────────────
    try:
        font_desc = load_font(size=13, bold=False)
    except Exception:
        font_desc = ImageFont.load_default()
    draw.text((margin, H - 22),
              "ASYMMETRIC LAYOUT — Cycle 12 — for comparison with symmetric v001",
              fill=(120, 110, 100),
              font=font_desc)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
