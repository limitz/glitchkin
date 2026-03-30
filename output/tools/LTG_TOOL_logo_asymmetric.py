#!/usr/bin/env python3
"""
LTG_TOOL_logo_asymmetric.py
Logo Generator — "Luma & the Glitchkin" — ASYMMETRIC LAYOUT v002

Art Director: Alex Chen
Date: 2026-03-30
Cycle: 13

Cycle 13 changes (Victoria Ashford A- → A grade):
  - "&" connector: warm-to-cold gradient treatment (left half warm orange/amber,
    right half electric cyan). The "&" is now the hinge between two worlds,
    not neutral punctuation.
  - "the/Glitchkin" inter-line gap: reduced by ~30% (was int(H * 0.04), now int(H * 0.028))
    "the" and "Glitchkin" now read as one vertical unit, not two elements sitting near each other.

Prior design:
  - "Luma" larger and left-anchored (~40% canvas width, dominant visual weight)
  - "&" small connector — mid-canvas bridge
  - "Glitchkin" smaller + stacked (name broken into two lines), right side
  - Background glow zones and bi-color scan bar

Output: /home/wipkat/team/output/production/LTG_BRAND_logo_asymmetric.png
"""

import os
import random
import math
from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH = "/home/wipkat/team/output/production/LTG_BRAND_logo_asymmetric.png"
W, H = 1200, 480

# Master Palette Colors
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
    bbox = font.getbbox(text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    for sx, sy in [(2, 2), (3, 3)]:
        draw.text((base_x + sx, base_y + sy), text, fill=color2, font=font)
    draw.text((base_x, base_y), text, fill=color, font=font)
    for _ in range(22):
        px = base_x + rng.randint(-8, text_w + 8)
        py = base_y + rng.randint(-4, text_h + 4)
        ps = rng.choice([2, 3, 4, 5])
        pc = rng.choice([SOFT_GOLD, WARM_ORANGE, WARM_CREAM, HOT_MAGENTA])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)


def draw_amp_gradient(img, font_amp, amp_x, amp_y, amp_w, amp_h):
    """
    Cycle 13: Draw '&' with warm-to-cold gradient treatment.
    Left half of glyph: warm SUNLIT_AMBER / WARM_ORANGE
    Right half of glyph: ELEC_CYAN / BYTE_TEAL
    The '&' is the hinge — it belongs to both worlds simultaneously.

    Technique: render glyph on a temp RGBA layer, then apply color gradient per column.
    """
    # Render glyph on temp white-background surface for alpha extraction
    temp_size = (amp_w + 40, amp_h + 40)
    glyph_img  = Image.new("RGBA", temp_size, (0, 0, 0, 0))
    glyph_draw = ImageDraw.Draw(glyph_img)
    # Shadow
    glyph_draw.text((4, 4), "&", fill=(60, 50, 40, 255), font=font_amp)
    # Main body - will be replaced by gradient
    glyph_draw.text((2, 2), "&", fill=(255, 255, 255, 255), font=font_amp)
    glyph_draw.text((0, 0), "&", fill=(255, 255, 255, 255), font=font_amp)

    # Build gradient overlay for the glyph area
    # Per-column: blend from SUNLIT_AMBER (left) to ELEC_CYAN (right)
    grad_layer = Image.new("RGBA", temp_size, (0, 0, 0, 0))
    for col in range(temp_size[0]):
        t = col / max(1, temp_size[0] - 1)
        # warm: SUNLIT_AMBER → WARM_ORANGE at 50%; cold: BYTE_TEAL → ELEC_CYAN at 100%
        if t < 0.5:
            tt = t / 0.5
            r_v = int(SUNLIT_AMBER[0] * (1 - tt) + WARM_ORANGE[0] * tt)
            g_v = int(SUNLIT_AMBER[1] * (1 - tt) + WARM_ORANGE[1] * tt)
            b_v = int(SUNLIT_AMBER[2] * (1 - tt) + WARM_ORANGE[2] * tt)
        else:
            tt = (t - 0.5) / 0.5
            r_v = int(BYTE_TEAL[0] * (1 - tt) + ELEC_CYAN[0] * tt)
            g_v = int(BYTE_TEAL[1] * (1 - tt) + ELEC_CYAN[1] * tt)
            b_v = int(BYTE_TEAL[2] * (1 - tt) + ELEC_CYAN[2] * tt)
        for row in range(temp_size[1]):
            # Apply gradient color where glyph mask is opaque
            px_data = glyph_img.getpixel((col, row))
            if px_data[3] > 128:
                grad_layer.putpixel((col, row), (r_v, g_v, b_v, px_data[3]))

    # Composite gradient glyph onto main image
    base_rgba = img.convert("RGBA")
    # Paste at (amp_x, amp_y)
    region = base_rgba.crop((amp_x, amp_y, amp_x + temp_size[0], amp_y + temp_size[1]))
    region_w = region.size[0]
    region_h = region.size[1]
    if grad_layer.size[0] > region_w or grad_layer.size[1] > region_h:
        grad_layer = grad_layer.crop((0, 0, region_w, region_h))
    merged = Image.alpha_composite(region.convert("RGBA"), grad_layer)
    base_rgba.paste(merged.convert("RGBA"), (amp_x, amp_y))
    img.paste(base_rgba.convert("RGB"))

    return img


def draw_glitch_cyan_text(draw, text, font, base_x, base_y, rng, scatter_count=40):
    bbox = font.getbbox(text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    for sx, sy, col, a in [
        (4, 4, DEEP_CYAN, None),
        (-3, -3, (*HOT_MAGENTA, 100), None),
        (3, 3, (*BYTE_TEAL, 130), None),
        (-1, 1, (*UV_PURPLE, 70), None),
    ]:
        c = col if isinstance(col, tuple) and len(col) == 3 else None
        ca = col if isinstance(col, tuple) and len(col) == 4 else None
        if c:
            draw.text((base_x + sx, base_y + sy), text, fill=c, font=font)
        else:
            draw.text((base_x + sx, base_y + sy), text, fill=ca, font=font)

    draw.text((base_x, base_y), text, fill=ELEC_CYAN, font=font)

    slice_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    slice_draw  = ImageDraw.Draw(slice_layer)
    for _ in range(6):
        slice_y  = base_y + rng.randint(4, text_h - 8)
        slice_h  = rng.randint(3, 8)
        shift_x  = rng.choice([-6, -4, 5, 7, 10])
        slice_draw.rectangle([base_x + shift_x, slice_y,
                               base_x + text_w + shift_x, slice_y + slice_h],
                              fill=(*HOT_MAGENTA, 60))

    for _ in range(scatter_count):
        px = base_x + rng.randint(-20, text_w + 40)
        py = base_y + rng.randint(-14, text_h + 20)
        ps = rng.choice([2, 3, 4, 6, 8])
        pc = rng.choice([ELEC_CYAN, HOT_MAGENTA, STATIC_WHITE, UV_PURPLE,
                         BYTE_TEAL, (0, 200, 220)])
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)

    return slice_layer


def draw_background(draw, img):
    for y in range(H):
        t = y / H
        r_v = int(VOID_BLACK[0] + 4 * t)
        g_v = int(VOID_BLACK[1] + 2 * t)
        b_v = int(VOID_BLACK[2] + 8 * t)
        draw.line([(0, y), (W, y)], fill=(r_v, g_v, b_v))

    scan_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    scan_draw  = ImageDraw.Draw(scan_layer)
    for y in range(0, H, 4):
        scan_draw.line([(0, y), (W, y)], fill=(0, 0, 0, 28))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, scan_layer)
    img.paste(base_rgba.convert("RGB"))

    # Warm amber glow — left half
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw  = ImageDraw.Draw(glow_layer)
    for step in range(16, 0, -1):
        t = step / 16
        rx = int(W * 0.38 * t)
        ry = int(H * 0.55 * t)
        alpha = int(42 * (1 - t))
        glow_draw.ellipse([int(W * 0.03) - rx, int(H * 0.80) - ry,
                           int(W * 0.03) + rx, int(H * 0.80) + ry],
                          fill=(*SOFT_GOLD, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow_layer)
    img.paste(base_rgba.convert("RGB"))

    # Secondary warm halo behind Luma text
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

    # Cyan glow — right quarter
    glow_layer3 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw3  = ImageDraw.Draw(glow_layer3)
    for step in range(14, 0, -1):
        t = step / 14
        rx = int(W * 0.22 * t)
        ry = int(H * 0.54 * t)
        alpha = int(36 * (1 - t))
        glow_draw3.ellipse([int(W * 0.88) - rx, int(H * 0.50) - ry,
                            int(W * 0.88) + rx, int(H * 0.50) + ry],
                           fill=(*ELEC_CYAN, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow_layer3)
    img.paste(base_rgba.convert("RGB"))

    # Vertical divider
    divider_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    divider_draw  = ImageDraw.Draw(divider_layer)
    divider_x = int(W * 0.50)
    divider_draw.line([(divider_x, int(H * 0.10)), (divider_x, int(H * 0.90))],
                      fill=(*DEEP_CYAN, 25), width=1)
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, divider_layer)
    img.paste(base_rgba.convert("RGB"))


def draw_luma_amber_glow(img, text_x, text_y, text_w, text_h):
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw  = ImageDraw.Draw(glow_layer)
    cx = text_x + text_w // 2
    cy = text_y + text_h // 2
    for step in range(16, 0, -1):
        t = step / 16
        rx = int((text_w // 2 + 50) * t)
        ry = int((text_h // 2 + 36) * t)
        alpha = int(55 * (1 - t))
        glow_draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                          fill=(*SOFT_GOLD, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow_layer)
    img.paste(base_rgba.convert("RGB"))


def draw_glitchkin_cyan_glow(img, text_x, text_y, text_w, text_h):
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw  = ImageDraw.Draw(glow_layer)
    cx = text_x + text_w // 2
    cy = text_y + text_h // 2
    for step in range(16, 0, -1):
        t = step / 16
        rx = int((text_w // 2 + 32) * t)
        ry = int((text_h // 2 + 44) * t)
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
    rng  = random.Random(42)

    # STEP 1: Background
    draw_background(draw, img)
    draw = ImageDraw.Draw(img)

    # STEP 2: Load fonts
    font_luma    = load_font(size=180, bold=True)
    font_amp     = load_font(size=56,  bold=False)
    font_the     = load_font(size=38,  bold=False)
    font_glitch  = load_font(size=72,  bold=True)

    # STEP 3: Measure text
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

    # STEP 4: Layout
    margin    = int(W * 0.05)
    luma_x    = margin
    luma_y    = (H - luma_h) // 2 - int(H * 0.04)

    amp_x  = luma_x + luma_w + int(W * 0.025)
    amp_y  = luma_y + luma_h - amp_h - int(H * 0.06)

    stack_x   = amp_x + amp_w + int(W * 0.028)
    the_x     = stack_x
    the_y     = luma_y + int(luma_h * 0.08)

    # Cycle 13 fix: reduce inter-line gap by ~30%
    # Was: int(H * 0.04) = ~19px. Now: int(H * 0.028) = ~13px.
    # "the" and "Glitchkin" now read as one vertical lockup.
    glitch_x  = stack_x
    glitch_y  = the_y + the_h + int(H * 0.028)  # was int(H * 0.04)

    # STEP 5: Glow layers behind text
    draw_luma_amber_glow(img, luma_x, luma_y, luma_w, luma_h)
    draw = ImageDraw.Draw(img)

    stack_total_h = (glitch_y + glitch_h) - the_y
    stack_total_w = max(the_w, glitch_w)
    draw_glitchkin_cyan_glow(img, glitch_x, the_y, stack_total_w, stack_total_h)
    draw = ImageDraw.Draw(img)

    # STEP 6: Draw "Luma" — dominant, warm amber
    draw_glitch_warp(draw, "Luma", font_luma,
                     luma_x, luma_y,
                     color=SUNLIT_AMBER,
                     color2=WARM_ORANGE,
                     rng=rng, warp_strength=3)
    draw.text((luma_x - 1, luma_y - 1), "Luma", fill=SOFT_GOLD, font=font_luma)
    draw.text((luma_x, luma_y), "Luma", fill=SUNLIT_AMBER, font=font_luma)

    # STEP 7: Draw "&" — Cycle 13: warm-to-cold gradient treatment
    # The "&" is the show's premise in one character — two worlds, one hinge.
    # Shadow pass first (RGB base)
    draw.text((amp_x + 2, amp_y + 2), "&", fill=(30, 20, 15), font=font_amp)
    # Gradient "& " applied as RGBA layer
    img = draw_amp_gradient(img, font_amp, amp_x, amp_y, amp_w, amp_h)
    draw = ImageDraw.Draw(img)

    # STEP 8: Draw "the" — small, above Glitchkin stack
    draw.text((the_x + 2, the_y + 2), "the", fill=DEEP_CYAN, font=font_the)
    draw.text((the_x, the_y), "the", fill=ELEC_CYAN, font=font_the)

    # STEP 9: Draw "Glitchkin" — electric cyan, heavy glitch treatment
    slice_layer = draw_glitch_cyan_text(draw, "Glitchkin", font_glitch,
                                         glitch_x, glitch_y, rng, scatter_count=60)
    base_rgba = img.convert("RGBA")
    img_with_slices = Image.alpha_composite(base_rgba, slice_layer)
    img.paste(img_with_slices.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # STEP 10: Pixel border accents — warm corners left, cold corners right
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

    # STEP 11: Bi-color scan bar below text
    bar_y  = int(H * 0.84)
    bar_h  = 5
    bar_x0 = int(W * 0.05)
    bar_x1 = int(W * 0.95)
    mid_bar = (bar_x0 + bar_x1) // 2
    draw.rectangle([bar_x0, bar_y, mid_bar, bar_y + bar_h], fill=SUNLIT_AMBER)
    draw.rectangle([mid_bar, bar_y, bar_x1, bar_y + bar_h], fill=DEEP_CYAN)
    for i in range(0, bar_x1 - bar_x0, 8):
        noise_h = rng.randint(1, 12)
        side_x  = bar_x0 + i
        if side_x < mid_bar:
            nc = rng.choice([SOFT_GOLD, SUNLIT_AMBER, WARM_CREAM, HOT_MAGENTA])
        else:
            nc = rng.choice([ELEC_CYAN, BYTE_TEAL, STATIC_WHITE, HOT_MAGENTA])
        draw.rectangle([side_x, bar_y - noise_h,
                        side_x + rng.randint(3, 7), bar_y], fill=nc)

    # STEP 12: Layout descriptor
    try:
        font_desc = load_font(size=13, bold=False)
    except Exception:
        font_desc = ImageFont.load_default()
    draw.text((margin, H - 22),
              "ASYMMETRIC LAYOUT v002 — Cycle 13 — & gradient + tighter the/Glitchkin gap",
              fill=(120, 110, 100), font=font_desc)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
