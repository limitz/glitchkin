#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
Character Proportion Diagram Generator — Luma & the Glitchkin
Draws head-unit proportion diagrams for characters side by side.
"""
from PIL import Image, ImageDraw, ImageFont

HEAD_UNIT = 80  # pixels per head unit
CHAR_WIDTH = 120
PADDING = 40
LABEL_H = 30
BOTTOM_PAD = 60
BG = (245, 242, 235)
OUTLINE = (30, 20, 15)
FILL = (200, 195, 185)

CHARACTERS = [
    {"name": "LUMA", "heads": 3.5, "color": (232, 114, 42),   "shape": "round"},
    {"name": "COSMO", "heads": 4.0, "color": (74, 120, 180),  "shape": "rect"},
    {"name": "BYTE",  "heads": 0.7, "color": (0, 240, 255),   "shape": "cube", "note": "~20% Luma height"},
    {"name": "MIRI",  "heads": 3.2, "color": (184, 92, 56),   "shape": "round"},
]

def draw_character(draw, x, char, max_heads, fonts):
    font, font_sm, font_title = fonts
    max_h = max_heads * HEAD_UNIT
    char_h = char["heads"] * HEAD_UNIT
    y_offset = LABEL_H + PADDING + int(max_h - char_h)

    cx = x + CHAR_WIDTH // 2
    head_r = int(HEAD_UNIT * 0.45)

    if char["shape"] == "round":
        # Round head
        draw.ellipse([cx - head_r, y_offset, cx + head_r, y_offset + HEAD_UNIT], fill=char["color"], outline=OUTLINE, width=2)
        # Body
        body_h = int((char["heads"] - 1.0) * HEAD_UNIT)
        bw = int(CHAR_WIDTH * 0.55)
        draw.rectangle([cx - bw//2, y_offset + HEAD_UNIT, cx + bw//2, y_offset + char_h], fill=char["color"], outline=OUTLINE, width=2)
    elif char["shape"] == "rect":
        # Rectangle head
        hw = int(HEAD_UNIT * 0.42)
        draw.rounded_rectangle([cx - hw, y_offset, cx + hw, y_offset + HEAD_UNIT], radius=8, fill=char["color"], outline=OUTLINE, width=2)
        body_h = int((char["heads"] - 1.0) * HEAD_UNIT)
        bw = int(CHAR_WIDTH * 0.45)
        draw.rectangle([cx - bw//2, y_offset + HEAD_UNIT, cx + bw//2, y_offset + char_h], fill=char["color"], outline=OUTLINE, width=2)
    elif char["shape"] == "cube":
        # Chamfered cube
        s = int(HEAD_UNIT * 0.6)
        draw.rectangle([cx - s//2, y_offset, cx + s//2, y_offset + s], fill=char["color"], outline=OUTLINE, width=2)
        # Stubby limbs
        draw.rectangle([cx - s//2 - 10, y_offset + s//4, cx - s//2, y_offset + s//4 + 12], fill=char["color"], outline=OUTLINE, width=1)
        draw.rectangle([cx + s//2, y_offset + s//4, cx + s//2 + 10, y_offset + s//4 + 12], fill=char["color"], outline=OUTLINE, width=1)

    # Head unit ruler on right
    ry = y_offset
    rx = x + CHAR_WIDTH - 8
    for i in range(int(char["heads"]) + 1):
        ty = ry + i * HEAD_UNIT
        if ty <= y_offset + char_h + 2:
            draw.line([(rx, ty), (rx + 6, ty)], fill=OUTLINE, width=1)

    # Name label below
    bottom_y = LABEL_H + PADDING + int(max_h) + 12
    draw.text((x + CHAR_WIDTH//2 - 30, bottom_y), char["name"], fill=OUTLINE, font=font)
    draw.text((x + CHAR_WIDTH//2 - 30, bottom_y + 18), f"{char['heads']} heads", fill=(100, 90, 80), font=font_sm)
    if "note" in char:
        draw.text((x + CHAR_WIDTH//2 - 45, bottom_y + 34), char["note"], fill=(140, 120, 100), font=font_sm)

def generate(output_path):
    max_heads = max(c["heads"] for c in CHARACTERS)
    n = len(CHARACTERS)
    w = n * (CHAR_WIDTH + PADDING) + PADDING
    h = LABEL_H + PADDING + int(max_heads * HEAD_UNIT) + BOTTOM_PAD + 60

    img = Image.new('RGB', (w, h), BG)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except:
        font = font_sm = font_title = ImageFont.load_default()

    draw.text((PADDING, 8), "LUMA & THE GLITCHKIN — Character Proportions", fill=OUTLINE, font=font_title)

    for i, char in enumerate(CHARACTERS):
        x = PADDING + i * (CHAR_WIDTH + PADDING)
        draw_character(draw, x, char, max_heads, (font, font_sm, font_title))

    # Ground line
    ground_y = LABEL_H + PADDING + int(max_heads * HEAD_UNIT)
    draw.line([(PADDING//2, ground_y), (w - PADDING//2, ground_y)], fill=(150, 140, 130), width=1)

    img.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == '__main__':
    generate("/home/wipkat/team/output/characters/main/proportion_diagram.png")
