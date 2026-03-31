#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_character_lineup.py
Character Lineup Generator — Luma & the Glitchkin
Cycle 53 / v013: Modular renderer migration (Alex Chen C53).

v013 changes (C53 — Alex Chen, Art Director):
  All 5 characters now rendered via canonical char_*.py modules.
  The lineup generator is now a pure composition tool — it imports
  draw_luma(), draw_byte(), draw_cosmo(), draw_miri(), draw_glitch()
  from their respective modules, renders each to a cairo surface,
  converts to PIL, resizes to lineup scale, and composites.
  No inline character drawing code remains.

  Layout geometry, two-tier staging, depth temperature, annotations
  all preserved from v012.

Prior history (compressed):
  v012 (C52): pycairo rebuild for Luma, Byte, Cosmo. Miri+Glitch PIL.
  v011 (C47): Cosmo visual hook (cowlick + bridge tape).
  v010 (C45): Two-tier depth bands (Option C, Lee Tanaka).
  v009 (C44): Miri wooden hairpin rename.
  v008 (C42): Two-tier ground plane staging (FG/BG tiers).
  v007 (C33): BYTE_SH / MIRI_SLIPPER color fixes.
  v006 (C29): Luma 3.2 heads, canonical eye width.
  v004-v001: Glitch added, dimension arrows, ground annotations, initial.

Output: /home/wipkat/team/output/characters/main/LTG_CHAR_character_lineup.png
Usage: python3 LTG_TOOL_character_lineup.py
"""
import sys
import os

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
from PIL import Image, ImageDraw, ImageFont
import math

# ── Modular character renderer imports ───────────────────────────────────────
from LTG_TOOL_cairo_primitives import to_pil_rgba
from LTG_TOOL_char_luma import draw_luma
from LTG_TOOL_char_byte import draw_byte
from LTG_TOOL_char_cosmo import draw_cosmo
from LTG_TOOL_char_miri import draw_miri
from LTG_TOOL_char_glitch import draw_glitch

# ── Canvas ────────────────────────────────────────────────────────────────────
BG           = (250, 248, 244)
PANEL_BG     = (245, 241, 235)
LINE_COL     = (59, 40, 32)       # #3B2820 Deep Cocoa
LABEL_COL    = (50, 40, 35)
TICK_COL     = (160, 148, 138)
BASELINE_COL = (180, 165, 150)

# ── Height system ─────────────────────────────────────────────────────────────
LUMA_RENDER_H = 280
LUMA_HEADS    = 3.2   # v006 FIX: was 3.5, canonical is 3.2 (C28 directive)
HEAD_UNIT     = LUMA_RENDER_H / LUMA_HEADS   # ~87.5px

COSMO_HEADS   = 4.0
COSMO_H       = int(COSMO_HEADS * HEAD_UNIT)  # ~320px

MIRI_HEADS    = 3.2
MIRI_H        = int(MIRI_HEADS * HEAD_UNIT)   # ~256px

BYTE_H        = int(LUMA_RENDER_H * 0.58)     # ~162px

# Glitch: floating antagonist, slightly taller than Byte
GLITCH_H      = int(BYTE_H * 1.05)            # ~170px

# ── Layout ────────────────────────────────────────────────────────────────────
CHAR_SPACING  = 240     # tighter spacing to fit 5 characters
LEFT_MARGIN   = 100
N_CHARS       = 5
IMG_W         = LEFT_MARGIN * 2 + CHAR_SPACING * (N_CHARS - 1) + 180
TITLE_H       = 50
LABEL_AREA    = 90     # slightly taller for tier annotation
IMG_H         = 560    # bumped for two-tier geometry (was computed from HEADROOM)

# ── Two-tier ground planes (v008) ─────────────────────────────────────────────
# FG tier: Luma + Byte — visually closest to camera
# BG tier: Cosmo + Miri + Glitch — one step behind
FG_GROUND_Y  = int(IMG_H * 0.78)   # ~436 — FG chars stand here
BG_GROUND_Y  = int(IMG_H * 0.70)   # ~392 — BG chars stand here

# Legacy alias: BASELINE_Y used by existing height-marker + annotation helpers
# Points to FG tier (the reference tier for head-unit comparisons)
BASELINE_Y   = FG_GROUND_Y

# ── FG scale factor (post-calculation, proportion constants unchanged) ────────
FG_SCALE     = 1.03   # +3% height for FG characters (Luma + Byte)
BG_SCALE     = 1.00   # baseline for BG characters

# Scaled render heights (used for drawing and labels)
LUMA_RENDER_H_FG  = int(LUMA_RENDER_H * FG_SCALE)   # ~288px
BYTE_H_FG         = int(BYTE_H * FG_SCALE)           # ~167px
GLITCH_H_BG       = GLITCH_H                          # unscaled

# ── Character order: left -> right ────────────────────────────────────────────
# Cosmo (left bookend) | Miri | Luma (center protagonist) | Byte | Glitch (right)
CHAR_ORDER    = ["cosmo", "miri", "luma", "byte", "glitch"]
CHAR_X        = {
    "cosmo":  LEFT_MARGIN + 60,
    "miri":   LEFT_MARGIN + 60 + CHAR_SPACING,
    "luma":   LEFT_MARGIN + 60 + CHAR_SPACING * 2,
    "byte":   LEFT_MARGIN + 60 + CHAR_SPACING * 3 - 20,
    "glitch": LEFT_MARGIN + 60 + CHAR_SPACING * 4,
}

# Ground Y per character (FG or BG tier)
CHAR_GROUND_Y = {
    "luma":   FG_GROUND_Y,
    "byte":   FG_GROUND_Y,
    "cosmo":  BG_GROUND_Y,
    "miri":   BG_GROUND_Y,
    "glitch": BG_GROUND_Y,
}

# Draw heights (FG chars use scaled height)
CHAR_HEIGHTS  = {
    "luma":   LUMA_RENDER_H_FG,
    "byte":   BYTE_H_FG,
    "cosmo":  COSMO_H,
    "miri":   MIRI_H,
    "glitch": GLITCH_H_BG,
}
CHAR_LABELS   = {
    "luma":   f"LUMA [FG]\n3.2 heads / {LUMA_RENDER_H}px (+3%)",
    "byte":   f"BYTE [FG]\n~Luma chest / {BYTE_H}px (+3%)",
    "cosmo":  f"COSMO [BG]\n4.0 heads / {COSMO_H}px",
    "miri":   f"MIRI [BG]\n3.2 heads / {MIRI_H}px",
    "glitch": f"GLITCH [BG]\n~Byte scale / {GLITCH_H}px",
}

# Default expressions for lineup (neutral/default standing pose)
CHAR_EXPRESSIONS = {
    "luma":   "CURIOUS",
    "byte":   "neutral",
    "cosmo":  "SKEPTICAL",
    "miri":   "WARM",
    "glitch": "neutral",
}


# ══════════════════════════════════════════════════════════════════════════════
# MODULAR CHARACTER RENDERING
# ══════════════════════════════════════════════════════════════════════════════

def _render_modular_character(char_name, target_h, cx, ground_y):
    """Render a character via its canonical char_*.py module.

    Calls draw_<char>(expression, scale=...) to produce a cairo surface,
    converts to PIL RGBA, trims transparent padding, resizes to target_h,
    and composites onto a full-canvas RGBA layer at the correct position.

    Returns:
        PIL RGBA image of the full lineup canvas size (IMG_W x IMG_H)
        with the character composited at the correct position.
    """
    expression = CHAR_EXPRESSIONS[char_name]
    draw_fns = {
        "luma":   draw_luma,
        "byte":   draw_byte,
        "cosmo":  draw_cosmo,
        "miri":   draw_miri,
        "glitch": draw_glitch,
    }
    draw_fn = draw_fns[char_name]

    # Render at scale=2.0 for enough resolution to downscale cleanly
    if char_name == "cosmo":
        # draw_cosmo returns (surface, geom_dict)
        surface, _geom = draw_fn(expression=expression, scale=2.0, facing="front")
    else:
        surface = draw_fn(expression=expression, scale=2.0, facing="front")

    char_img = to_pil_rgba(surface)

    # Trim transparent pixels to find actual character bounds
    bbox = char_img.getbbox()
    if bbox is None:
        return Image.new("RGBA", (IMG_W, IMG_H), (0, 0, 0, 0))

    trimmed = char_img.crop(bbox)
    orig_w, orig_h = trimmed.size

    # Resize to target lineup height, preserving aspect ratio
    scale_factor = target_h / orig_h
    new_w = max(1, int(orig_w * scale_factor))
    new_h = target_h
    resized = trimmed.resize((new_w, new_h), Image.LANCZOS)

    # Create full-canvas RGBA layer and paste character centered at (cx, ground_y)
    canvas = Image.new("RGBA", (IMG_W, IMG_H), (0, 0, 0, 0))
    paste_x = cx - new_w // 2
    paste_y = ground_y - new_h
    canvas.paste(resized, (paste_x, paste_y), resized)
    return canvas


# ══════════════════════════════════════════════════════════════════════════════
# HEIGHT COMPARISON MARKERS
# ══════════════════════════════════════════════════════════════════════════════

def draw_height_markers(draw, font_small):
    # Heights measured from each character's own ground tier
    luma_top   = FG_GROUND_Y - CHAR_HEIGHTS["luma"]
    cosmo_top  = BG_GROUND_Y - CHAR_HEIGHTS["cosmo"]
    luma_chest = FG_GROUND_Y - int(CHAR_HEIGHTS["luma"] * 0.62)
    miri_top   = BG_GROUND_Y - CHAR_HEIGHTS["miri"]

    lines = [
        (cosmo_top,  TICK_COL,           "Cosmo top [BG]"),
        (luma_top,   (180, 140, 80),      "Luma top [FG]"),
        (miri_top,   (140, 160, 120),     "Miri top [BG]"),
        (luma_chest, (80, 160, 200),      "Byte / Glitch height ref"),
    ]

    x_start = 30
    x_end   = IMG_W - 100

    for y, col, label in lines:
        x = x_start
        while x < x_end:
            draw.line([(x, y), (min(x + 8, x_end), y)], fill=col, width=1)
            x += 13
        draw.text((x_end + 4, y - 7), label, fill=col, font=font_small)


# ══════════════════════════════════════════════════════════════════════════════
# BYTE FLOAT-GAP DIMENSION ARROW (retained from v003/v004)
# ══════════════════════════════════════════════════════════════════════════════

def draw_byte_float_dimension(draw, font_small):
    GROUNDFLOOR_COL = (100, 168, 200)

    byte_cx   = CHAR_X["byte"]
    # Use unscaled BYTE_H for the float-gap engineering annotation
    # (the gap proportions are a characteristic of Byte's design, not the FG scale)
    s         = BYTE_H
    float_gap = int(s * 0.18)
    body_rx   = s // 2

    arrow_x = byte_cx + body_rx + 14
    top_y   = FG_GROUND_Y - float_gap
    bot_y   = FG_GROUND_Y

    if bot_y - top_y < 6:
        return

    draw.line([(arrow_x, top_y), (arrow_x, bot_y)], fill=GROUNDFLOOR_COL, width=2)

    tip_size = 5
    draw.polygon([(arrow_x, top_y),
                  (arrow_x - tip_size, top_y + tip_size * 2),
                  (arrow_x + tip_size, top_y + tip_size * 2)],
                 fill=GROUNDFLOOR_COL)
    draw.polygon([(arrow_x, bot_y),
                  (arrow_x - tip_size, bot_y - tip_size * 2),
                  (arrow_x + tip_size, bot_y - tip_size * 2)],
                 fill=GROUNDFLOOR_COL)

    serif_w = 7
    draw.line([(arrow_x - serif_w, top_y), (arrow_x + serif_w, top_y)],
              fill=GROUNDFLOOR_COL, width=2)
    draw.line([(arrow_x - serif_w, bot_y), (arrow_x + serif_w, bot_y)],
              fill=GROUNDFLOOR_COL, width=2)

    label   = "0.25 HU"
    label_x = arrow_x + serif_w + 4
    label_y = (top_y + bot_y) // 2 - 5
    draw.text((label_x, label_y), label, fill=GROUNDFLOOR_COL, font=font_small)

    gf_x0 = byte_cx - 70
    gf_x1 = byte_cx + 70
    gf_y  = FG_GROUND_Y
    x = gf_x0
    while x < gf_x1:
        draw.line([(x, gf_y), (min(x + 10, gf_x1), gf_y)],
                  fill=GROUNDFLOOR_COL, width=1)
        x += 14


# ══════════════════════════════════════════════════════════════════════════════
# MAIN GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

def generate_lineup(output_path):
    img  = Image.new('RGB', (IMG_W, IMG_H), BG)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
        font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except Exception:
        font_title = font_label = font_small = ImageFont.load_default()

    draw.rectangle([0, 0, IMG_W, IMG_H], fill=BG)

    title = ("LUMA & THE GLITCHKIN — Full Cast Lineup — C53 v013"
             " (modular char_*.py renderers | two-tier staging: FG/WARM + BG/COOL)")
    draw.text((20, 14), title, fill=LABEL_COL, font=font_title)
    draw.line([(0, TITLE_H - 4), (IMG_W, TITLE_H - 4)], fill=TICK_COL, width=1)

    # ── Two-tier gradient depth bands (v010 — Option C, Lee Tanaka C45) ─────────
    # Drawn BEFORE characters. Both bands <=10px tall — below all character geometry.
    # Warm/cool encoding: warm = FG/close, cool = BG/far. Reads at thumbnail scale.
    _BG_SHADOW_COL = (180, 195, 210)   # cool slate
    _BG_SHADOW_H   = 8                  # px
    _FG_SHADOW_COL = (220, 200, 160)   # warm amber
    _FG_SHADOW_H   = 10                 # px

    # BG tier drop-shadow (cool slate) — drawn first
    for row in range(_BG_SHADOW_H):
        alpha_frac = 1.0 - row / _BG_SHADOW_H    # fades to 0 downward
        r = int(_BG_SHADOW_COL[0] + (BG[0] - _BG_SHADOW_COL[0]) * (1 - alpha_frac))
        g = int(_BG_SHADOW_COL[1] + (BG[1] - _BG_SHADOW_COL[1]) * (1 - alpha_frac))
        b = int(_BG_SHADOW_COL[2] + (BG[2] - _BG_SHADOW_COL[2]) * (1 - alpha_frac))
        draw.line([(0, BG_GROUND_Y + row), (IMG_W, BG_GROUND_Y + row)],
                  fill=(r, g, b), width=1)

    # FG tier drop-shadow (warm amber)
    for row in range(_FG_SHADOW_H):
        alpha_frac = 1.0 - row / _FG_SHADOW_H
        r = int(_FG_SHADOW_COL[0] + (BG[0] - _FG_SHADOW_COL[0]) * (1 - alpha_frac))
        g = int(_FG_SHADOW_COL[1] + (BG[1] - _FG_SHADOW_COL[1]) * (1 - alpha_frac))
        b = int(_FG_SHADOW_COL[2] + (BG[2] - _FG_SHADOW_COL[2]) * (1 - alpha_frac))
        draw.line([(0, FG_GROUND_Y + row), (IMG_W, FG_GROUND_Y + row)],
                  fill=(r, g, b), width=1)

    # Tier labels (updated with warm/cool grammar)
    _tier_col_bg = (148, 165, 180)   # cool label color
    _tier_col_fg = (180, 150, 90)    # warm label color
    draw.text((IMG_W - 110, BG_GROUND_Y + 5), "BG tier (COOL)",
              fill=_tier_col_bg, font=font_small)
    draw.text((IMG_W - 110, FG_GROUND_Y + 5), "FG tier (WARM)",
              fill=_tier_col_fg, font=font_small)

    draw_byte_float_dimension(draw, font_small)
    draw = ImageDraw.Draw(img)  # refresh after annotations

    draw_height_markers(draw, font_small)
    draw = ImageDraw.Draw(img)

    # ── Characters — all rendered via modular char_*.py modules ───────────
    for char in CHAR_ORDER:
        cx       = CHAR_X[char]
        h        = CHAR_HEIGHTS[char]
        ground_y = CHAR_GROUND_Y[char]
        char_layer = _render_modular_character(char, h, cx, ground_y)
        img = Image.alpha_composite(img.convert("RGBA"), char_layer).convert("RGB")
        draw = ImageDraw.Draw(img)

    # Character name labels below their respective ground lines
    for char in CHAR_ORDER:
        cx      = CHAR_X[char]
        ground_y = CHAR_GROUND_Y[char]
        lines   = CHAR_LABELS[char].split("\n")
        label_y = ground_y + 8
        for line in lines:
            lw = len(line) * 6
            draw.text((cx - lw // 2, label_y), line, fill=LABEL_COL, font=font_small)
            label_y += 13

    # Vertical height brackets — measured from each char's own ground tier
    for char in CHAR_ORDER:
        cx       = CHAR_X[char] - 44
        h        = CHAR_HEIGHTS[char]
        ground_y = CHAR_GROUND_Y[char]
        top_y    = ground_y - h
        if char in ("byte", "glitch"):
            s         = h
            float_gap = int(s * 0.18)
            body_ry   = int(s * 0.55)
            top_y     = ground_y - float_gap - body_ry * 2
        draw.line([(cx, top_y), (cx, ground_y)], fill=TICK_COL, width=1)
        draw.line([(cx - 4, top_y), (cx + 4, top_y)], fill=TICK_COL, width=1)
        draw.line([(cx - 4, ground_y), (cx + 4, ground_y)], fill=TICK_COL, width=1)
        draw.text((cx - 20, (top_y + ground_y)//2 - 5),
                  f"{h}px", fill=TICK_COL, font=font_small)

    # Staging annotation bar
    annotation = (
        f"Staging: FG tier (y={FG_GROUND_Y}, WARM) = Luma+Byte @+3% scale.  "
        f"BG tier (y={BG_GROUND_Y}, COOL) = Cosmo+Miri+Glitch @baseline scale.  "
        "WARM = FG / COOL = BG.  "
        "Proportion constants unchanged — uniform post-scale only."
    )
    draw.text((20, IMG_H - 34), annotation, fill=(140, 120, 100), font=font_small)

    footer = (
        f"Full cast: Cosmo | Miri | LUMA | Byte | Glitch.  "
        f"Reference: 1 head unit = {HEAD_UNIT:.0f}px.  "
        "Colors per master_palette.md (canonical).  C53 v013 (modular char_*.py renderers)."
    )
    draw.text((20, IMG_H - 18), footer, fill=TICK_COL, font=font_small)

    # IMAGE SIZE RULE: <= 1280px in both dimensions
    if img.size[0] > 1280 or img.size[1] > 1280:
        img.thumbnail((1280, 1280), Image.LANCZOS)

    img.save(output_path)
    print(f"Saved: {output_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}px")


def main():
    import os
    out_dir = output_dir('characters', 'main')
    os.makedirs(out_dir, exist_ok=True)
    generate_lineup(os.path.join(out_dir, "LTG_CHAR_character_lineup.png"))
    print("Character lineup v013 generation complete.")
    print("  C53 changes: all 5 characters via modular char_*.py renderers")
    print(f"  FG_GROUND_Y={FG_GROUND_Y}, BG_GROUND_Y={BG_GROUND_Y}, FG_SCALE={FG_SCALE}")
    print(f"  Character order (L->R): cosmo | miri | luma | byte | glitch")
    print(f"  Luma: {LUMA_RENDER_H_FG}px drawn ({LUMA_RENDER_H}px base x{FG_SCALE}), "
          f"{LUMA_HEADS} heads, head unit = {HEAD_UNIT:.1f}px")
    print(f"  Byte: {BYTE_H_FG}px drawn ({BYTE_H}px base x{FG_SCALE})")


if __name__ == '__main__':
    main()
