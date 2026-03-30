# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_grandma_miri_color_model.py
Generates: output/characters/color_models/LTG_COLOR_grandma_miri_color_model.png

Author: Sam Kowalski, Color & Style Artist
Cycle: 17
Date: 2026-03-29

PURPOSE:
    Produces a production-ready color swatch sheet for Grandma Miri.
    All values sourced from grandma_miri_color_model.md and master_palette.md.
    Each swatch is labeled with: color name, hex code, RGB values.
    Swatches are grouped by zone (face/skin, hair, clothing, accessories).

CYCLE 17 CHANGES:
    - Initial creation. New character color model swatch sheet.

IMPORTANT NOTES:
    - After every img.paste() call, refresh: draw = ImageDraw.Draw(img)
    - Grandma Miri uses WARM/DOMESTIC lighting only. NO Glitch palette.
    - Line color: Deep Cocoa #3B2820 (RW-11) — show-wide standard.
    - Skin base: #8C5430 (darker than Luma's #C8885A — same amber family, lower value).
    - Hair: warm silver (#D8D0C8), NOT cool blue-gray silver.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ---------------------------------------------------------------------------
# OUTPUT PATH
# ---------------------------------------------------------------------------
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "characters", "color_models")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "LTG_COLOR_grandma_miri_color_model.png")

# ---------------------------------------------------------------------------
# PALETTE CONSTANTS — all sourced from master_palette.md and grandma_miri_color_model.md
# ---------------------------------------------------------------------------

# Show-wide line color (RW-11)
DEEP_COCOA = (59, 40, 32)           # #3B2820

# Show-wide background for swatch sheets
WARM_CREAM = (250, 240, 220)        # #FAF0DC — RW-01

# --- SKIN ZONE ---
SKIN_BASE = (140, 84, 48)           # #8C5430  Deep Warm Brown
SKIN_SHADOW = (106, 58, 30)         # #6A3A1E  Dark Sienna
SKIN_HIGHLIGHT = (168, 106, 64)     # #A86A40  Warm Chestnut
CHEEK_BLUSH = (212, 149, 107)       # #D4956B  Permanent Blush (25% opacity feel)

# --- EYES ---
EYE_WHITE = (250, 240, 220)         # #FAF0DC  Warm Cream (RW-01)
EYE_IRIS = (139, 94, 60)            # #8B5E3C  Deep Warm Amber
EYE_PUPIL = (26, 15, 10)            # #1A0F0A  Near-Black Espresso (= DRW-18 hair base)
EYE_HIGHLIGHT = (240, 240, 240)     # #F0F0F0  Static White
EYEBROW_GRAY = (138, 122, 112)      # #8A7A70  Warm Gray

# --- HAIR ---
HAIR_BASE = (216, 208, 200)         # #D8D0C8  Silver White (warm silver)
HAIR_SHADOW = (168, 152, 140)       # #A8988C  Warm Gray shadow
HAIR_HIGHLIGHT = (240, 236, 232)    # #F0ECE8  Bright Near-White (warm)

# --- CARDIGAN (sweater) ---
CARDIGAN_BASE = (184, 92, 56)       # #B85C38  Warm Terracotta Rust
CARDIGAN_SHADOW = (138, 60, 28)     # #8A3C1C  Deep Rust
CARDIGAN_HIGHLIGHT = (212, 130, 90) # #D4825A  Dusty Apricot
CARDIGAN_BUTTONS = (232, 216, 184)  # #E8D8B8  Aged Bone

# --- GLASSES ---
# Glasses frames: not specified in color model but standard for this character type.
# Using Warm Gray (eyebrow color) as thin wire frame — same value family, visually quiet.
GLASSES_FRAME = (138, 122, 112)     # #8A7A70  Warm Gray (matches eyebrows — spec note)

# --- PANTS ---
PANTS_BASE = (200, 174, 138)        # #C8AE8A  Warm Linen Tan
PANTS_SHADOW = (160, 138, 106)      # #A08A6A  Warm Medium Tan
PANTS_HIGHLIGHT = (222, 201, 168)   # #DEC9A8  Light Linen

# --- SLIPPERS ---
SLIPPER_UPPER = (196, 144, 122)     # C38 FIX: #C4907A  Dusty Warm Apricot (was #5A7A5A Deep Sage — G>R violated Miri warm-palette guarantee; per master_palette.md CHAR-M-11 C32)
SLIPPER_LINING = (250, 240, 220)    # #FAF0DC  Warm Cream
SLIPPER_SOLE = (90, 56, 32)         # #5A3820  Warm Dark Brown

# ---------------------------------------------------------------------------
# SWATCH DATA
# Each entry: (label, hex_str, rgb_tuple, group_label)
# ---------------------------------------------------------------------------

SWATCHES = [
    # GROUP: SKIN & FACE
    ("Skin Base",        "#8C5430", SKIN_BASE,        "SKIN & FACE"),
    ("Skin Shadow",      "#6A3A1E", SKIN_SHADOW,      "SKIN & FACE"),
    ("Skin Highlight",   "#A86A40", SKIN_HIGHLIGHT,   "SKIN & FACE"),
    ("Cheek Blush",      "#D4956B", CHEEK_BLUSH,      "SKIN & FACE"),

    # GROUP: EYES
    ("Eye White",        "#FAF0DC", EYE_WHITE,        "EYES"),
    ("Eye Iris",         "#8B5E3C", EYE_IRIS,         "EYES"),
    ("Eye Pupil",        "#1A0F0A", EYE_PUPIL,        "EYES"),
    ("Eye Highlight",    "#F0F0F0", EYE_HIGHLIGHT,    "EYES"),
    ("Eyebrow Gray",     "#8A7A70", EYEBROW_GRAY,     "EYES"),

    # GROUP: HAIR
    ("Hair Base",        "#D8D0C8", HAIR_BASE,        "HAIR"),
    ("Hair Shadow",      "#A8988C", HAIR_SHADOW,      "HAIR"),
    ("Hair Highlight",   "#F0ECE8", HAIR_HIGHLIGHT,   "HAIR"),

    # GROUP: CARDIGAN (sweater)
    ("Cardigan Base",    "#B85C38", CARDIGAN_BASE,    "CARDIGAN"),
    ("Cardigan Shadow",  "#8A3C1C", CARDIGAN_SHADOW,  "CARDIGAN"),
    ("Cardigan Hi",      "#D4825A", CARDIGAN_HIGHLIGHT,"CARDIGAN"),
    ("Cardi Buttons",    "#E8D8B8", CARDIGAN_BUTTONS, "CARDIGAN"),

    # GROUP: GLASSES
    ("Glasses Frame",    "#8A7A70", GLASSES_FRAME,    "GLASSES"),

    # GROUP: PANTS
    ("Pants Base",       "#C8AE8A", PANTS_BASE,       "PANTS"),
    ("Pants Shadow",     "#A08A6A", PANTS_SHADOW,     "PANTS"),
    ("Pants Highlight",  "#DEC9A8", PANTS_HIGHLIGHT,  "PANTS"),

    # GROUP: SLIPPERS
    ("Slipper Upper",    "#C4907A", SLIPPER_UPPER,    "SLIPPERS"),
    ("Slipper Lining",   "#FAF0DC", SLIPPER_LINING,   "SLIPPERS"),
    ("Slipper Sole",     "#5A3820", SLIPPER_SOLE,     "SLIPPERS"),

    # GROUP: LINE
    ("Line Color",       "#3B2820", DEEP_COCOA,       "LINE"),
]

# ---------------------------------------------------------------------------
# LAYOUT CONSTANTS
# ---------------------------------------------------------------------------
CANVAS_W = 1200
CANVAS_BG = (245, 235, 215)     # Slightly warmer than pure Warm Cream for contrast

SWATCH_W = 160
SWATCH_H = 90
LABEL_H = 52                    # height below swatch for text
CELL_W = SWATCH_W + 24          # horizontal spacing between swatches
CELL_H = SWATCH_H + LABEL_H + 20

SWATCHES_PER_ROW = 6

MARGIN_LEFT = 40
MARGIN_TOP = 130                # room for title + subtitle
GROUP_HEADER_H = 36

TITLE_COLOR = DEEP_COCOA
SUBTITLE_COLOR = (100, 80, 60)  # warm medium brown
GROUP_COLOR = (130, 90, 60)     # warm brown for group headers
TEXT_COLOR = DEEP_COCOA
HEX_COLOR = (80, 60, 40)
RGB_COLOR = (110, 85, 60)

BORDER_COLOR = DEEP_COCOA
BORDER_WIDTH = 2

# ---------------------------------------------------------------------------
# FONT — use default PIL bitmap font (no external dependency)
# ---------------------------------------------------------------------------
def get_font(size=14):
    """Return default PIL font — no external font files required."""
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except OSError:
        pass
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", size)
    except OSError:
        pass
    return ImageFont.load_default()


def get_bold_font(size=14):
    """Return bold PIL font — fallback to default."""
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except OSError:
        pass
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", size)
    except OSError:
        pass
    return ImageFont.load_default()


# ---------------------------------------------------------------------------
# HELPER: group swatches
# ---------------------------------------------------------------------------
def group_swatches(swatches):
    """Return list of (group_name, [swatch_entries]) in order of first appearance."""
    groups = {}
    order = []
    for entry in swatches:
        label, hex_str, rgb, group = entry
        if group not in groups:
            groups[group] = []
            order.append(group)
        groups[group].append((label, hex_str, rgb))
    return [(g, groups[g]) for g in order]


# ---------------------------------------------------------------------------
# HELPER: luminance for text contrast
# ---------------------------------------------------------------------------
def luminance(rgb):
    """Approximate perceptual luminance 0..1."""
    r, g, b = [x / 255.0 for x in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def text_color_for_bg(rgb):
    """Return black or white text color based on background luminance."""
    if luminance(rgb) > 0.45:
        return (40, 25, 15)     # dark warm near-black
    else:
        return (245, 235, 215)  # light warm cream


# ---------------------------------------------------------------------------
# MAIN DRAW FUNCTION
# ---------------------------------------------------------------------------
def draw_swatch_sheet():
    grouped = group_swatches(SWATCHES)

    # --- Calculate total canvas height ---
    total_h = MARGIN_TOP
    for group_name, entries in grouped:
        total_h += GROUP_HEADER_H + 8
        rows = (len(entries) + SWATCHES_PER_ROW - 1) // SWATCHES_PER_ROW
        total_h += rows * CELL_H + 16
    total_h += 80   # footer

    img = Image.new("RGB", (CANVAS_W, total_h), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    font_title = get_bold_font(28)
    font_subtitle = get_font(16)
    font_group = get_bold_font(15)
    font_label = get_bold_font(12)
    font_hex = get_font(11)
    font_rgb = get_font(10)

    # --- Title ---
    draw.text((MARGIN_LEFT, 30), "GRANDMA MIRI — Color Model Swatch Sheet", font=font_title, fill=TITLE_COLOR)
    draw.text((MARGIN_LEFT, 66), "Luma & the Glitchkin  |  Cycle 17  |  Sam Kowalski, Color & Style Artist", font=font_subtitle, fill=SUBTITLE_COLOR)
    draw.text((MARGIN_LEFT, 90), "All values: warm/domestic light only. NO Glitch palette. Line: #3B2820 Deep Cocoa.", font=font_hex, fill=SUBTITLE_COLOR)

    # --- Horizontal rule under title ---
    draw.line([(MARGIN_LEFT, 115), (CANVAS_W - MARGIN_LEFT, 115)], fill=DEEP_COCOA, width=2)

    y = MARGIN_TOP

    for group_name, entries in grouped:
        # --- Group header ---
        draw.text((MARGIN_LEFT, y), f"— {group_name} —", font=font_group, fill=GROUP_COLOR)
        y += GROUP_HEADER_H

        # --- Swatches in this group ---
        for idx, (label, hex_str, rgb) in enumerate(entries):
            col = idx % SWATCHES_PER_ROW
            row = idx // SWATCHES_PER_ROW

            x = MARGIN_LEFT + col * CELL_W
            sy = y + row * CELL_H

            # Swatch rectangle fill
            swatch_rect = [x, sy, x + SWATCH_W, sy + SWATCH_H]
            draw.rectangle(swatch_rect, fill=rgb)
            # Border
            draw.rectangle(swatch_rect, outline=BORDER_COLOR, width=BORDER_WIDTH)

            # Text below swatch
            text_y = sy + SWATCH_H + 6
            tc = TEXT_COLOR

            draw.text((x, text_y), label, font=font_label, fill=tc)
            draw.text((x, text_y + 16), hex_str, font=font_hex, fill=HEX_COLOR)
            draw.text((x, text_y + 29), f"RGB {rgb[0]},{rgb[1]},{rgb[2]}", font=font_rgb, fill=RGB_COLOR)

        rows_in_group = (len(entries) + SWATCHES_PER_ROW - 1) // SWATCHES_PER_ROW
        y += rows_in_group * CELL_H + 16

    # --- Footer ---
    draw.line([(MARGIN_LEFT, y), (CANVAS_W - MARGIN_LEFT, y)], fill=DEEP_COCOA, width=1)
    draw.text((MARGIN_LEFT, y + 8), "Source: grandma_miri_color_model.md v1.0 + master_palette.md v2.0 | LTG_COLOR_grandma_miri_color_model.png", font=font_rgb, fill=SUBTITLE_COLOR)

    return img


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    img = draw_swatch_sheet()
    img.save(OUTPUT_FILE)
    print(f"Saved: {OUTPUT_FILE}")
    print(f"Size: {img.size[0]} x {img.size[1]} px")
