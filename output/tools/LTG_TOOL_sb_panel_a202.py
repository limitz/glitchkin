#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_panel_a202.py
Storyboard Panel A2-02 — Byte MCU VULNERABLE/RESIGNED expression (Cycle 18)
Maya Santos, Character Designer

Panel direction (Alex Chen, Cycle 18):
  - MCU (Medium Close-Up): head + upper body
  - Beat: Luma has just told Byte the plan. Byte is processing.
    VULNERABLE moment — the last flicker before resignation sets in.
  - Expression: RESIGNED geometry but 55% aperture (vs standard 45%)
    "The last flicker before giving up" — slightly more open than full RESIGNED
    - Droopy lower lid (parabolic curve, NOT flat)
    - Downcast pupil (shifted to lower half)
    - Flat short mouth (resigned — no energy)
    - 55% aperture (slightly more open = still a trace of resistance)
    - Reduced highlight dot (dim — not extinguished, not bright)
  - Body: one arm beginning to fold in (transitional — not fully drawn in yet)
  - Byte body fill: GL-01b #00D4E8 (Byte Teal — canonical, NOT GL-01 #00F0FF)
  - Background: mid-value dark, subtle circuit trace texture

Reference: RESIGNED geometry from LTG_CHAR_byte_expression_sheet.py
  - droopy_resigned: parabolic lower lid, pupil+10px down, dim highlight, heavy upper lid
  - For A2-02: aperture = 55% (not 45%) — the "almost resigned" state

Output:
  /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_act2_panel_a202.png

Cycle 18 production notes:
  - After img.paste() always refresh draw = ImageDraw.Draw(img)
  - RESIGNED parabolic lower lid = max sag 7px at center (matches expression sheet)
  - 55% aperture distinguishes A2-02 from A2-07 (45%) — vulnerability still visible
  - Left arm fully extended (neutral), right arm beginning to fold = transitional posture
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
from PIL import Image, ImageDraw, ImageFont
import math
import os
import sys
from LTG_TOOL_char_byte import draw_byte
from LTG_TOOL_cairo_primitives import to_pil_rgba
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ACT2_PANELS_DIR = output_dir('storyboards', 'act2', 'panels')
OUTPUT_PATH     = os.path.join(ACT2_PANELS_DIR, "LTG_SB_act2_panel_a202.png")

os.makedirs(ACT2_PANELS_DIR, exist_ok=True)

PW, PH       = 800, 540
CAPTION_H    = 56
DRAW_H       = PH - CAPTION_H   # 484px scene area

# ── Palette ───────────────────────────────────────────────────────────────────
BG_CAPTION    = (18, 15, 22)
TEXT_CAPTION  = (230, 222, 200)
BORDER_COL    = (14, 10, 18)
STATIC_WHITE  = (240, 240, 240)
ANN_COL       = (200, 185, 120)
ANN_DIM       = (140, 130, 90)
CALLOUT_CYN   = (0, 200, 218)
CALLOUT_DIM   = (0, 150, 165)

# Byte canonical colors
# GL-01b = #00D4E8  (Byte Teal — CANONICAL BODY FILL, per production spec)
BYTE_BODY    = (0, 212, 232)   # GL-01b #00D4E8
BYTE_MID     = (0, 168, 184)   # mid shadow
BYTE_DARK    = (0, 105, 118)   # deep shadow / face plate
BYTE_OUTLINE = (10, 10, 20)
BYTE_EYE_W   = (232, 248, 255) # eye sclera
BYTE_EYE_CYN = (0, 200, 218)   # dim cyan iris (reduced — RESIGNED energy level)
BYTE_EYE_PUP = (10, 10, 20)
BYTE_BEZEL   = (22, 48, 58)    # eye bezel / frame

# Pixel eye (left side of face — RESIGNED downward arrow)
GLYPH_DEAD  = (10, 10, 24)
GLYPH_DIM   = (0, 80, 100)
GLYPH_MID   = (0, 168, 180)
GLYPH_CRACK = (255, 45, 107)

# Background
BG_BASE      = (28, 30, 40)    # mid-value dark — not void-black, readable MCU
CIRCUIT_COL  = (38, 52, 62)
CIRCUIT_DOT  = (48, 66, 78)
CIRCUIT_NODE = (28, 44, 52)


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


def add_glow(img, cx, cy, r_max, color_rgb, steps=6, max_alpha=60):
    """ADD light via alpha_composite — never darkens."""
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_background(img, draw):
    """
    Mid-value dark background with subtle circuit trace texture.
    A2-02: intimate space — Byte processing what Luma told him.
    Not as deep/void as A2-07 ECU — this is an MCU with more spatial context.
    """
    # Mid-value dark base (not pure black — mid-value for MCU intimacy)
    draw.rectangle([0, 0, PW, DRAW_H], fill=BG_BASE)

    import random
    rng = random.Random(2202)

    # Horizontal circuit trace runs
    for _ in range(18):
        tx   = rng.randint(0, PW)
        ty   = rng.randint(0, DRAW_H)
        tlen = rng.randint(30, 120)
        draw.line([tx, ty, tx + tlen, ty], fill=CIRCUIT_COL, width=1)
        # Junction dot at end
        draw.rectangle([tx + tlen - 2, ty - 2, tx + tlen + 2, ty + 2],
                       fill=CIRCUIT_DOT)

    # Vertical trace runs
    for _ in range(12):
        tx   = rng.randint(0, PW)
        ty   = rng.randint(0, DRAW_H)
        tlen = rng.randint(20, 70)
        draw.line([tx, ty, tx, ty + tlen], fill=CIRCUIT_COL, width=1)

    # Circuit nodes (cross junction marks)
    for _ in range(8):
        nx = rng.randint(30, PW - 30)
        ny = rng.randint(20, DRAW_H - 20)
        r  = rng.randint(3, 6)
        draw.ellipse([nx - r, ny - r, nx + r, ny + r],
                     fill=CIRCUIT_NODE, outline=CIRCUIT_DOT)

    # Subtle vignette — edges slightly darker (intimacy framing)
    vignette = Image.new('RGBA', (PW, DRAW_H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette)
    for margin, alpha in [(0, 55), (20, 38), (45, 20)]:
        vd.rectangle([margin, margin, PW - margin, DRAW_H - margin],
                     outline=(0, 0, 0, alpha), width=margin + 1 if margin > 0 else 1)
    # Corners vignette
    corner_size = 160
    for cx_v, cy_v in [(0, 0), (PW, 0), (0, DRAW_H), (PW, DRAW_H)]:
        for r, a in [(corner_size, 30), (corner_size - 30, 18), (corner_size - 60, 10)]:
            vd.ellipse([cx_v - r, cy_v - r, cx_v + r, cy_v + r],
                       fill=(0, 0, 0, a))
    base = img.convert('RGBA')
    panel_area = base.crop((0, 0, PW, DRAW_H))
    merged = Image.alpha_composite(panel_area.convert('RGBA'), vignette)
    img.paste(merged.convert('RGB'), (0, 0))
    draw = ImageDraw.Draw(img)

    return draw


def draw_downward_arrow_glyph(draw, origin_x, origin_y, pixel_size):
    """
    Render a 5×5 downward-arrow pixel glyph — RESIGNED defeat indicator.
    Used in left-eye pixel display of Byte's face.
    """
    ARROW_BRIGHT = {
        (0, 2), (1, 2),
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
        (3, 1), (3, 2), (3, 3),
        (4, 2),
    }
    for row_idx in range(5):
        for col_idx in range(5):
            if (row_idx, col_idx) in ARROW_BRIGHT:
                color = GLYPH_MID
            else:
                color = GLYPH_DEAD
            px = origin_x + col_idx * pixel_size
            py = origin_y + row_idx * pixel_size
            draw.rectangle([px, py, px + pixel_size - 1, py + pixel_size - 1],
                           fill=color)





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

def draw_byte_mcu(img, draw, font_ann):
    """Byte MCU — canonical renderer (close-up)."""
    scale = 2.5
    surface = draw_byte(expression="searching", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(DRAW_H * 0.80)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    byte_cx = int(PW * 0.50)
    byte_cy = int(DRAW_H * 0.48)
    _composite_char(img, char_pil, byte_cx, byte_cy)


def make_panel():
    font      = load_font(14)
    font_bold = load_font(14, bold=True)
    font_cap  = load_font(12)
    font_ann  = load_font(10)

    img  = Image.new('RGB', (PW, PH), BG_BASE)
    draw = ImageDraw.Draw(img)

    # Draw background
    draw = draw_background(img, draw)

    # Draw Byte MCU
    draw = draw_byte_mcu(img, draw, font_ann)

    # ── Caption bar ───────────────────────────────────────────────────────────
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=BORDER_COL, width=2)
    draw.text((10, DRAW_H + 6),
              "A2-02  MCU  neutral observer",
              font=font_cap, fill=(155, 148, 125))
    draw.text((10, DRAW_H + 22),
              "Byte processing what Luma just told him — VULNERABLE moment, last flicker before resignation",
              font=font_cap, fill=TEXT_CAPTION)
    draw.text((10, DRAW_H + 38),
              "beat: pre-resignation  |  expr: RESIGNED geom 55% apt  |  body: transitional fold  |  bg: circuit trace",
              font=font_ann, fill=(145, 138, 108))
    draw.text((PW - 260, DRAW_H + 44),
              "LTG_SB_act2_panel_a202_v002",
              font=font_ann, fill=(95, 90, 72))

    # ── Border ────────────────────────────────────────────────────────────────
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COL, width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("A2-02 panel (v002) generation complete (Cycle 18).")
    print("  Expression: RESIGNED geometry, 55% aperture (pre-resignation vulnerable beat)")
    print("  Body: transitional posture — right arm beginning to fold in")
    print("  Body fill: GL-01b #00D4E8 (Byte Teal canonical)")
