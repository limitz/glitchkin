#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_panel_a104_kitchen.py
Storyboard Panel A1-04 (kitchen cold open) — FIRST CONTACT — Byte appears — Cycle 18
Lee Tanaka, Storyboard Artist

NOTE: A1-04 (classroom near-miss) already exists as LTG_SB_act2_panel_a104.png.
This is the KITCHEN cold open A1-04 — a DIFFERENT beat:
Byte appears on the TV screen. First face-to-face contact.

Beat: Byte appears on the screen. Luma: SURPRISED. Byte: default glow, slightly
indignant at being stared at.

Shot: TWO-SHOT — Luma MCU (left) + TV screen Byte (right)
Camera: Eye-level (child height). Very similar to A1-03 setup but now Byte is
clearly visible on screen — full character reveal on screen.

Luma expression: SURPRISED (wide eyes, jaw slightly dropped, leaning back slightly
from pure reflex — she was leaning in a moment ago, now she recoils an inch).

Byte (on screen): default glow (cyan/teal), slightly indignant expression —
arms crossed if body visible, one eye slightly narrowed (unamused at being stared at),
small body on the screen (he's at 2/3 body reveal in the lower screen area).

Arc: SURPRISED — first contact. "Wait — that looked back at me."
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
from PIL import Image, ImageDraw, ImageFont
import math, random, os
import sys
from LTG_TOOL_char_byte import draw_byte
from LTG_TOOL_char_luma import draw_luma as _draw_luma_canonical
from LTG_TOOL_cairo_primitives import to_pil_rgba
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_act1_panel_a104.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H

# ── Palette ─────────────────────────────────────────────────────────────────
BG_DARK      = (28, 22, 16)
FLOOR_DARK   = (36, 28, 20)
LINE_DARK    = (100, 72, 40)

# (Luma colors handled by canonical char_luma renderer)

# TV
TV_BODY      = (55, 48, 38)
TV_TRIM      = (72, 62, 50)
CRT_SCREEN   = (90, 105, 92)
CRT_STATIC1  = (130, 140, 128)
CRT_CYAN     = (0, 240, 255)
CRT_GLOW     = (0, 210, 230)

# (Byte colors handled by canonical char_byte renderer)

BG_CAPTION = (22, 18, 14)
TEXT_CAP   = (235, 228, 210)
ANN_COL    = (200, 175, 120)
ANN_DIM    = (150, 135, 100)
CALLOUT_L  = (220, 200, 140)
CALLOUT_B  = (0, 220, 240)


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







def _char_to_pil(surface):
    """Convert a cairo.ImageSurface from canonical char module to cropped PIL RGBA."""
    from LTG_TOOL_cairo_primitives import to_pil_rgba
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

def draw_tv_with_byte(draw, img, rng):
    """TV with Byte on screen — canonical Byte renderer."""
    # Draw TV frame first
    tv_cx, tv_cy = int(PW * 0.72), int(DRAW_H * 0.38)
    tv_w, tv_h = 140, 110
    draw.rectangle([tv_cx - tv_w//2, tv_cy - tv_h//2,
                    tv_cx + tv_w//2, tv_cy + tv_h//2],
                   fill=(40, 35, 28), outline=(80, 70, 55), width=3)
    # Screen area
    scr_x0 = tv_cx - tv_w//2 + 8
    scr_y0 = tv_cy - tv_h//2 + 8
    scr_x1 = tv_cx + tv_w//2 - 8
    scr_y1 = tv_cy + tv_h//2 - 8
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1], fill=(10, 10, 20))
    # Byte inside screen
    scale = 0.6
    surface = draw_byte(expression="grumpy", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = scr_y1 - scr_y0 - 10
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    _composite_char(img, char_pil, (scr_x0 + scr_x1) // 2, (scr_y0 + scr_y1) // 2)


def draw_luma_surprised(draw, img):
    """Luma surprised — canonical renderer."""
    scale = 0.5
    surface = _draw_luma_canonical(expression="SURPRISED", scale=scale, facing="left")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = 200
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    luma_cx = int(PW * 0.30)
    luma_cy = int(DRAW_H * 0.62)
    _composite_char(img, char_pil, luma_cx, luma_cy)


def make_panel():
    font_cap = load_font(12)
    font_ann = load_font(11)
    rng      = random.Random(104)

    img  = Image.new('RGB', (PW, PH), BG_DARK)
    draw = ImageDraw.Draw(img)

    # BG: dark room
    draw.rectangle([0, 0, PW, DRAW_H], fill=BG_DARK)
    draw.rectangle([0, int(DRAW_H * 0.78), PW, DRAW_H], fill=FLOOR_DARK)
    draw.line([(0, int(DRAW_H * 0.78)), (PW, int(DRAW_H * 0.78))],
              fill=(46, 36, 26), width=2)

    # CRT TV with Byte (BG-right)
    draw = draw_tv_with_byte(draw, img, rng)
    draw = ImageDraw.Draw(img)

    # Luma surprised (FG-left)
    draw = draw_luma_surprised(draw, img)
    draw = ImageDraw.Draw(img)

    # Annotations
    draw.text((10, 8), "A1-04  /  TWO-SHOT  /  eye-level  /  Luma MCU + TV screen Byte",
              font=font_ann, fill=ANN_COL)
    draw.text((10, 20), "FIRST CONTACT — Byte appears. Luma: SURPRISED. Byte: INDIGNANT.",
              font=font_ann, fill=ANN_DIM)

    # Luma callout
    draw.text((14, int(DRAW_H * 0.06)), "LUMA",
              font=font_ann, fill=CALLOUT_L)
    draw.text((14, int(DRAW_H * 0.06) + 10), "SURPRISED",
              font=font_ann, fill=(220, 200, 100))
    draw.text((14, int(DRAW_H * 0.06) + 20), "jaw dropped / eyes MAX",
              font=font_ann, fill=ANN_DIM)

    # Byte callout
    draw.text((int(PW * 0.50), int(DRAW_H * 0.06)), "BYTE",
              font=font_ann, fill=CALLOUT_B)
    draw.text((int(PW * 0.50), int(DRAW_H * 0.06) + 10), "INDIGNANT",
              font=font_ann, fill=(0, 200, 220))
    draw.text((int(PW * 0.50), int(DRAW_H * 0.06) + 20), "arms crossed / squint",
              font=font_ann, fill=(0, 170, 190))

    # "it looked at me" beat note
    draw.text((int(PW * 0.28), int(DRAW_H * 0.82)), '"it looked at me"',
              font=font_ann, fill=(200, 180, 120))

    # FIRST CONTACT label
    draw.rectangle([10, DRAW_H - 22, 130, DRAW_H - 5], fill=(18, 14, 10))
    draw.text((14, DRAW_H - 20), "FIRST CONTACT", font=font_ann, fill=(0, 240, 255))

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(18, 12, 8), width=2)
    draw.text((10, DRAW_H + 5), "A1-04  TWO-SHOT  eye-level  Luma + Byte (on screen)",
              font=font_cap, fill=(160, 155, 130))
    draw.text((10, DRAW_H + 20),
              "Byte appears on CRT screen. Luma: SURPRISED. Byte: default glow, INDIGNANT.",
              font=font_cap, fill=(235, 228, 210))
    draw.text((10, DRAW_H + 36),
              "FIRST CONTACT beat. The Glitchkin see back. Cold open hook. CRT pixel confetti.",
              font=font_ann, fill=(150, 140, 110))
    draw.text((PW - 240, DRAW_H + 46), "LTG_SB_act1_panel_a104_v001",
              font=font_ann, fill=(100, 95, 78))

    draw.rectangle([0, 0, PW - 1, PH - 1], outline=(18, 12, 8), width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("A1-04 (kitchen) panel generation complete (Cycle 18).")
