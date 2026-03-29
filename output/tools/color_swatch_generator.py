#!/usr/bin/env python3
"""
Color Swatch Generator — Luma & the Glitchkin
Usage: python3 color_swatch_generator.py "Title" output.png hex1,label1 hex2,label2 ...
Also importable as a module: generate_swatches(title, swatches, output_path)
"""
import sys
from PIL import Image, ImageDraw, ImageFont

SWATCH_W = 200
SWATCH_H = 80
COLS = 4
PADDING = 20
HEADER_H = 60
FONT_SIZE_LABEL = 14
FONT_SIZE_HEX = 12
BG_COLOR = (245, 242, 235)
TEXT_DARK = (30, 20, 15)
TEXT_LIGHT = (240, 235, 220)

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def luminance(rgb):
    r, g, b = [x/255.0 for x in rgb]
    return 0.299*r + 0.587*g + 0.114*b

def generate_swatches(title, swatches, output_path):
    rows = (len(swatches) + COLS - 1) // COLS
    w = COLS * SWATCH_W + (COLS + 1) * PADDING
    h = HEADER_H + rows * SWATCH_H + (rows + 1) * PADDING + PADDING

    img = Image.new('RGB', (w, h), BG_COLOR)
    draw = ImageDraw.Draw(img)

    try:
        font_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", FONT_SIZE_LABEL)
        font_hex = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONT_SIZE_HEX)
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    except:
        font_label = ImageFont.load_default()
        font_hex = font_label
        font_title = font_label

    draw.text((PADDING, PADDING), title, fill=TEXT_DARK, font=font_title)

    for i, (hex_color, label) in enumerate(swatches):
        col = i % COLS
        row = i // COLS
        x = PADDING + col * (SWATCH_W + PADDING)
        y = HEADER_H + PADDING + row * (SWATCH_H + PADDING)

        rgb = hex_to_rgb(hex_color)
        draw.rectangle([x, y, x + SWATCH_W, y + SWATCH_H], fill=rgb)
        draw.rectangle([x, y, x + SWATCH_W, y + SWATCH_H], outline=(180, 170, 160), width=1)

        text_color = TEXT_LIGHT if luminance(rgb) < 0.45 else TEXT_DARK
        draw.text((x + 6, y + 8), label[:24], fill=text_color, font=font_label)
        draw.text((x + 6, y + 28), hex_color.upper(), fill=text_color, font=font_hex)

    img.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: color_swatch_generator.py 'Title' output.png hex1,label1 ...")
        sys.exit(1)
    title = sys.argv[1]
    output = sys.argv[2]
    swatches = []
    for arg in sys.argv[3:]:
        parts = arg.split(',', 1)
        swatches.append((parts[0], parts[1] if len(parts) > 1 else parts[0]))
    generate_swatches(title, swatches, output)
