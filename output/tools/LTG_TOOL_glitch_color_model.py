#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_CHAR_glitch_color_model_v001.py
Glitch — Color Model v001
"Luma & the Glitchkin" — Cycle 23 / Maya Santos

Color swatches + labeled palette document for Glitch.
Format: 800×500px — character color story document.
  Left half: character front silhouette in color (simplified)
  Right half: labeled swatches for each palette value

All palette values taken directly from canonical sources:
  GL-07 CORRUPT_AMBER = #FF8C00 (255,140,0)  — master_palette.md canonical
  HOT_MAG             = #FF2D6B (255,45,107)  — byte.md Section 9B
  UV_PURPLE           = #7B2FBE (123,47,190)  — master_palette.md GL-05
  VOID_BLACK          = #0A0A14 (10,10,20)    — canonical show line color
  ACID_GREEN          = #39FF14 (57,255,20)   — master_palette.md GL-03
  SOFT_GOLD           = #E8C95A (232,201,90)  — master_palette.md RW-02

Output: output/characters/color_models/LTG_COLOR_glitch_color_model.png

[Renamed from LTG_CHAR_glitch_color_model_v001.py to LTG_TOOL_glitch_color_model.py
 in Cycle 28 — generator files use LTG_TOOL_ prefix. Output PNG names are unchanged.]
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ── Canonical Palette ──────────────────────────────────────────────────────────
SWATCHES = [
    # (hex_display, rgb, label, role)
    ("#FF8C00", (255, 140,   0), "CORRUPT_AMBER — GL-07",   "Primary body fill"),
    ("#A84C00", (168,  76,   0), "CORRUPT_AMBER_SHADOW",     "Shadow/underside"),
    ("#FFB950", (255, 185,  80), "CORRUPT_AMBER_HIGHLIGHT",  "Body highlight facet"),
    ("#E8C95A", (232, 201,  90), "SOFT_GOLD — RW-02",        "Echo of warm origin"),
    ("#FF2D6B", (255,  45, 107), "HOT_MAGENTA — GL-04",      "Crack lines / danger"),
    ("#7B2FBE", (123,  47, 190), "UV_PURPLE — GL-05",        "Deep shadow / corruption"),
    ("#39FF14", ( 57, 255,  20), "ACID_GREEN — GL-03",       "Mischief eye state"),
    ("#0A0A14", ( 10,  10,  20), "VOID_BLACK — GL-01 LINE",  "Outline / dead pixels"),
    ("#F8F6EC", (248, 246, 236), "STATIC_WHITE — GL-06",     "Eye pixel highlight"),
    ("#00F0FF", (  0, 240, 255), "ELECTRIC_CYAN — GL-01",    "Pixel bleed / panic eye"),
]

CANVAS_W = 800
CANVAS_H = 500
CANVAS_BG = (16, 14, 24)
HEADER_H  = 52
LABEL_COL = (255, 140, 0)

# Character silhouette colors
CORRUPT_AMB    = (255, 140,   0)
CORRUPT_AMB_SH = (168,  76,   0)
CORRUPT_AMB_HL = (255, 185,  80)
HOT_MAG        = (255,  45, 107)
UV_PURPLE      = (123,  47, 190)
VOID_BLACK     = ( 10,  10,  20)
SOFT_GOLD      = (232, 201,  90)


def draw_character_silhouette(draw, cx, cy):
    """Simplified Glitch character front view for color model reference."""
    rx, ry = 50, 56  # ry > rx: body taller than wide — spec §2.1
    # Shadow
    sh_pts = [(cx+4, cy-ry), (cx+rx+4, cy+8), (cx+4, cy+int(ry*1.1)+4), (cx-rx+4, cy-8)]
    draw.polygon(sh_pts, fill=UV_PURPLE)
    # Body
    pts = [(cx, cy-ry), (cx+rx, cy+8), (cx, cy+int(ry*1.1)), (cx-rx, cy-8)]
    draw.polygon(pts, fill=CORRUPT_AMB)
    # Highlight facet
    draw.polygon([(cx, cy-ry), (cx+8, cy-ry//4), (cx-rx//2+4, cy-ry//2)],
                 fill=CORRUPT_AMB_HL)
    # Silhouette
    draw.polygon(pts, outline=VOID_BLACK, width=3)
    # Crack lines
    draw.line([(cx-rx//2, cy-ry//3), (cx+rx//3, cy+ry//2)], fill=HOT_MAG, width=2)
    draw.line([((cx-rx//2+cx+rx//3)//2, (cy-ry//3+cy+ry//2)//2),
               (cx+rx//2, cy-ry//4)], fill=HOT_MAG, width=1)
    # Top spike
    top_pts = [(cx-8,cy-ry),(cx-14,cy-ry-18),(cx,cy-ry-36),(cx+14,cy-ry-18),(cx+8,cy-ry)]
    draw.polygon(top_pts, fill=CORRUPT_AMB)
    draw.polygon(top_pts, outline=VOID_BLACK, width=2)
    draw.line([(cx, cy-ry-36), (cx, cy-ry-42)], fill=HOT_MAG, width=2)
    # Bottom spike
    cy_bot = cy + int(ry*1.1) + 4
    draw.polygon([(cx-8, cy_bot), (cx+8, cy_bot), (cx, cy_bot+14)],
                 fill=CORRUPT_AMB_SH)
    draw.polygon([(cx-8, cy_bot), (cx+8, cy_bot), (cx, cy_bot+14)],
                 outline=VOID_BLACK, width=2)
    # Arm spikes
    draw.polygon([(cx-rx-4, cy-4), (cx-rx-4, cy+4), (cx-rx-22, cy-8)],
                 fill=CORRUPT_AMB)
    draw.polygon([(cx-rx-4, cy-4), (cx-rx-4, cy+4), (cx-rx-22, cy-8)],
                 outline=VOID_BLACK, width=2)
    draw.polygon([(cx+rx+4, cy-4), (cx+rx+4, cy+4), (cx+rx+22, cy-8)],
                 fill=CORRUPT_AMB)
    draw.polygon([(cx+rx+4, cy-4), (cx+rx+4, cy+4), (cx+rx+22, cy-8)],
                 outline=VOID_BLACK, width=2)
    # Pixel eyes
    cell = 7
    face_cy = cy - ry // 6
    leye_x = cx - 30
    leye_y = face_cy - cell*3//2
    NEUTRAL = [[0, 2, 0], [2, 1, 2], [0, 2, 0]]
    PCOLS = {0: VOID_BLACK, 1: CORRUPT_AMB_SH, 2: CORRUPT_AMB, 3: SOFT_GOLD}
    for row in range(3):
        for col in range(3):
            c = PCOLS[NEUTRAL[row][col]]
            draw.rectangle([leye_x+col*cell, leye_y+row*cell,
                             leye_x+col*cell+cell-1, leye_y+row*cell+cell-1], fill=c)
    reye_x = cx + 8
    reye_y = face_cy - cell*3//2
    DESTAB = [[1, 2, 0], [2, 0, 1], [0, 2, 1]]
    for row in range(3):
        for col in range(3):
            c = PCOLS.get(DESTAB[row][col], VOID_BLACK)
            draw.rectangle([reye_x+col*cell, reye_y+row*cell,
                             reye_x+col*cell+cell-1, reye_y+row*cell+cell-1], fill=c)
    # Hover confetti
    import random
    rng = random.Random(42)
    for _ in range(8):
        px = rng.randint(cx-32, cx+32)
        py = rng.randint(cy_bot+4, cy_bot+20)
        sz = rng.choice([2, 3])
        col = rng.choice([HOT_MAG, UV_PURPLE, (10,10,20)])
        draw.rectangle([px, py, px+sz, py+sz], fill=col)


def build_color_model():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    try:
        font_h  = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font_sw = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)
        font_sm = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
    except Exception:
        font_h = ImageFont.load_default()
        font_sw = ImageFont.load_default()
        font_sm = ImageFont.load_default()

    # Header
    draw.rectangle([0, 0, CANVAS_W, HEADER_H], fill=(12, 10, 20))
    title = "GLITCH — Color Model v001  |  Cycle 23  |  GL-07 CORRUPT_AMBER PRIMARY"
    try:
        tb = draw.textbbox((0, 0), title, font=font_h)
        tw = tb[2] - tb[0]; th = tb[3] - tb[1]
    except Exception:
        tw, th = 400, 20
    draw.text(((CANVAS_W - tw) // 2, (HEADER_H - th) // 2),
              title, fill=LABEL_COL, font=font_h)

    # Character silhouette (left half)
    char_area_w = CANVAS_W // 2
    draw.rectangle([0, HEADER_H, char_area_w, CANVAS_H],
                   fill=(20, 16, 28))
    char_cx = char_area_w // 2
    char_cy = HEADER_H + (CANVAS_H - HEADER_H) // 2 + 10
    draw_character_silhouette(draw, char_cx, char_cy)

    # Character label
    char_label = "GLITCH  (NEUTRAL)"
    try:
        clb = draw.textbbox((0,0), char_label, font=font_sw)
        clw = clb[2] - clb[0]
        draw.text(((char_area_w - clw)//2, CANVAS_H - 24),
                  char_label, fill=(160, 100, 40), font=font_sw)
    except Exception:
        pass

    # Color swatches (right half)
    sw_x0  = char_area_w + 16
    sw_w   = 36
    sw_h   = 28
    sw_pad = 8
    sw_y0  = HEADER_H + 16
    label_x_off = sw_w + 10

    for i, (hexval, rgb, label, role) in enumerate(SWATCHES):
        sy = sw_y0 + i * (sw_h + sw_pad)
        # Swatch rectangle
        draw.rectangle([sw_x0, sy, sw_x0 + sw_w, sy + sw_h], fill=rgb)
        draw.rectangle([sw_x0, sy, sw_x0 + sw_w, sy + sw_h],
                       outline=(80, 60, 40), width=1)
        # Hex
        draw.text((sw_x0 + label_x_off, sy + 2), hexval,
                  fill=(200, 160, 80), font=font_sw)
        # Label
        draw.text((sw_x0 + label_x_off, sy + 13), label,
                  fill=(220, 220, 210), font=font_sw)
        # Role (small)
        draw.text((sw_x0 + label_x_off + 160, sy + 13), role,
                  fill=(120, 100, 80), font=font_sm)

    # Divider line between char and swatches
    draw.line([(char_area_w, HEADER_H), (char_area_w, CANVAS_H)],
              fill=(40, 30, 50), width=1)

    return img


def main():
    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "characters", "color_models"
    )
    os.makedirs(out_dir, exist_ok=True)

    model = build_color_model()
    out_path = os.path.join(out_dir, "LTG_COLOR_glitch_color_model.png")
    model.save(out_path)
    print(f"Saved: {out_path}")
    print(f"  Size: {model.size[0]}×{model.size[1]}px")
    print("  Swatches: 10 canonical colors documented")
    print("  Primary: GL-07 CORRUPT_AMBER #FF8C00")


if __name__ == "__main__":
    main()
