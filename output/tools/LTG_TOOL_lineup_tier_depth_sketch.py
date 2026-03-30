#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_lineup_tier_depth_sketch.py
Lineup Tier Depth Indicator Band — Options Sketch
Cycle 45 / Lee Tanaka — Character Staging & Visual Acting Specialist

Generates a 3-panel comparison sketch (≤1280×720) showing three depth indicator
band approaches for the character lineup two-tier ground plane (v008).

Panel layout: side by side, left to right:
  A) Thin horizontal rule between tiers (minimal, clear, clean)
  B) Per-tier ground shadow gradient (atmospheric, suggestive)
  C) RECOMMENDATION: Dual-warmth shadow bands (warm FG + cool BG)

The "characters" are simplified silhouettes sufficient to read tier position.
Output: output/production/lineup_tier_depth_sketch.png
Usage: python3 LTG_TOOL_lineup_tier_depth_sketch.py
"""
from PIL import Image, ImageDraw, ImageFont
import math

# ── Canvas ────────────────────────────────────────────────────────────────────
PANEL_W   = 400
PANEL_H   = 480
MARGIN    = 8
N_PANELS  = 3
IMG_W     = PANEL_W * N_PANELS + MARGIN * (N_PANELS + 1)
TITLE_H   = 50
IMG_H     = PANEL_H + TITLE_H + MARGIN * 2

BG_COL       = (245, 241, 235)   # lineup BG
TITLE_COL    = (40, 30, 25)
PANEL_BG     = (250, 248, 244)
BORDER_COL   = (200, 190, 180)

# ── Tier geometry (mirrors LTG_TOOL_character_lineup.py v008) ─────────────────
FG_GROUND_Y = int(PANEL_H * 0.78)   # ~374
BG_GROUND_Y = int(PANEL_H * 0.70)   # ~336
LABEL_Y     = PANEL_H - 60          # label area starts here

# ── Character silhouette palette ──────────────────────────────────────────────
FG_CHAR_COL  = (70, 50, 40)    # FG chars: Luma + Byte (darker = closer)
BG_CHAR_COL  = (140, 128, 118) # BG chars: Cosmo + Miri + Glitch (lighter = farther)
SHADOW_WARM  = (220, 200, 160) # warm amber for FG tier shadow
SHADOW_COOL  = (180, 195, 210) # cool slate for BG tier shadow
RULE_COL     = (160, 148, 138) # neutral mid-tone rule line

# ── Font ──────────────────────────────────────────────────────────────────────
try:
    font_title  = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 18)
    font_label  = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 13)
    font_small  = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 11)
    font_tag    = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 12)
except OSError:
    font_title  = ImageFont.load_default()
    font_label  = font_title
    font_small  = font_title
    font_tag    = font_title


def _draw_stub_char(draw, cx, ground_y, h, col, *, label=None, font=None):
    """Draw a simple oval silhouette stub (head + body rectangle)."""
    head_r = max(int(h * 0.22), 8)
    head_cy = ground_y - h + head_r
    # head
    draw.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=col)
    # body
    body_top = head_cy + head_r
    body_w   = max(int(head_r * 1.4), 10)
    body_bot = ground_y
    draw.rectangle([cx - body_w, body_top, cx + body_w, body_bot], fill=col)
    # label
    if label and font:
        draw.text((cx, ground_y + 4), label, fill=(80, 60, 50), font=font, anchor="mt")


def draw_panel_base(draw, ox, oy, title_str, font_lbl):
    """Draw panel background, title, and tier ground lines."""
    # panel bg
    draw.rectangle([ox, oy, ox + PANEL_W - 1, oy + PANEL_H - 1], fill=PANEL_BG, outline=BORDER_COL)
    # title band
    draw.rectangle([ox, oy, ox + PANEL_W - 1, oy + 26], fill=(235, 228, 218))
    draw.text((ox + PANEL_W // 2, oy + 13), title_str, fill=TITLE_COL, font=font_lbl, anchor="mm")
    # BG ground subtle dashed
    for x in range(ox + 8, ox + PANEL_W - 8, 8):
        draw.line([(x, oy + BG_GROUND_Y), (x + 4, oy + BG_GROUND_Y)], fill=(200, 188, 175), width=1)


def draw_stub_cast(draw, ox, oy, fg_col, bg_col, font_sm):
    """Draw 5 stub silhouettes at FG/BG tier positions."""
    # BG chars: cosmo, miri, glitch
    bg_positions = [
        (ox + int(PANEL_W * 0.18), oy + BG_GROUND_Y, int(PANEL_H * 0.56), "C"),
        (ox + int(PANEL_W * 0.40), oy + BG_GROUND_Y, int(PANEL_H * 0.44), "M"),
        (ox + int(PANEL_W * 0.82), oy + BG_GROUND_Y, int(PANEL_H * 0.32), "G"),
    ]
    for cx, gy, h, lbl in bg_positions:
        _draw_stub_char(draw, cx, gy, h, bg_col, label=lbl, font=font_sm)

    # FG chars: luma, byte
    fg_positions = [
        (ox + int(PANEL_W * 0.55), oy + FG_GROUND_Y, int(PANEL_H * 0.50), "L"),
        (ox + int(PANEL_W * 0.68), oy + FG_GROUND_Y, int(PANEL_H * 0.29), "B"),
    ]
    for cx, gy, h, lbl in fg_positions:
        _draw_stub_char(draw, cx, gy, h, fg_col, label=lbl, font=font_sm)


def draw_tier_labels(draw, ox, oy, font_sm):
    """Draw FG / BG tier annotation text on the panel."""
    draw.text((ox + PANEL_W - 10, oy + BG_GROUND_Y - 6), "BG", fill=(130, 118, 108), font=font_sm, anchor="rb")
    draw.text((ox + PANEL_W - 10, oy + FG_GROUND_Y - 6), "FG", fill=(90, 70, 55), font=font_sm, anchor="rb")


# ──────────────────────────────────────────────────────────────────────────────
# OPTION A: Thin horizontal rule between FG and BG ground levels
# ──────────────────────────────────────────────────────────────────────────────
def draw_option_a(draw, ox, oy, fonts):
    """Option A: A single thin horizontal rule separating the two tier ground lines."""
    font_lbl, font_sm, font_tag = fonts
    # midpoint between BG_GROUND_Y and FG_GROUND_Y
    mid_y = (BG_GROUND_Y + FG_GROUND_Y) // 2
    draw_panel_base(draw, ox, oy, "A — Thin Rule", font_lbl)
    draw_stub_cast(draw, ox, oy, FG_CHAR_COL, BG_CHAR_COL, font_sm)

    # rule: 1px across full width, mid-tone warm gray
    draw.line([(ox + 6, oy + mid_y), (ox + PANEL_W - 7, oy + mid_y)], fill=RULE_COL, width=1)

    draw_tier_labels(draw, ox, oy, font_sm)
    # annotation
    draw.text((ox + 6, oy + mid_y - 12), "1px rule", fill=RULE_COL, font=font_small, anchor="lt")
    # verdict
    draw.rectangle([ox + 6, oy + PANEL_H - 36, ox + PANEL_W - 6, oy + PANEL_H - 6], fill=(240, 236, 228))
    draw.text((ox + PANEL_W // 2, oy + PANEL_H - 21), "Too subtle — tier delta=44px already close", fill=(120, 100, 80), font=font_small, anchor="mm")


# ──────────────────────────────────────────────────────────────────────────────
# OPTION B: Atmospheric haze band between the tiers (low alpha fog strip)
# ──────────────────────────────────────────────────────────────────────────────
def draw_option_b(draw, ox, oy, fonts):
    """Option B: Low-alpha haze band between the two tier levels (≤20% alpha as specified)."""
    font_lbl, font_sm, font_tag = fonts
    draw_panel_base(draw, ox, oy, "B — Haze Band", font_lbl)

    # Draw haze band: strip from BG_GROUND_Y - 6 to FG_GROUND_Y + 6
    haze_top = oy + BG_GROUND_Y - 4
    haze_bot = oy + FG_GROUND_Y + 4
    haze_h   = haze_bot - haze_top

    # Render haze as an overlay image pasted onto the panel
    haze = Image.new("RGBA", (PANEL_W - 12, haze_h), (0, 0, 0, 0))
    haze_d = ImageDraw.Draw(haze)
    # gradient: peak alpha at centre, falls to 0 at edges (simulate soft edge)
    for row in range(haze_h):
        t = row / max(haze_h - 1, 1)
        # tent function: 0 → 1 → 0 across the strip
        alpha = int(50 * (1.0 - abs(t - 0.5) * 2))   # max alpha ~50 (≈20% at 255)
        haze_d.rectangle([0, row, PANEL_W - 13, row], fill=(200, 210, 220, alpha))

    # paste haze (needs RGBA composite)
    panel_crop_img = Image.new("RGBA", (PANEL_W, PANEL_H), (250, 248, 244, 255))
    panel_crop_img.alpha_composite(haze, dest=(6, BG_GROUND_Y - 4))
    draw_stub_img = panel_crop_img.convert("RGB")

    # We need access to the outer image — instead draw directly using alpha approx
    # (pure PIL ImageDraw has no alpha fill for rect, so use ellipse trick)
    # Approximate: draw several low-contrast rectangles
    for row in range(haze_h):
        y_abs = haze_top + row
        t = row / max(haze_h - 1, 1)
        alpha_frac = 1.0 - abs(t - 0.5) * 2   # 0→1→0
        intensity  = int(200 + 30 * alpha_frac)  # barely visible — near BG color
        col_h = (intensity, intensity + 5, intensity + 10)
        draw.line([(ox + 6, y_abs), (ox + PANEL_W - 7, y_abs)], fill=col_h, width=1)

    draw_stub_cast(draw, ox, oy, FG_CHAR_COL, BG_CHAR_COL, font_sm)
    draw_tier_labels(draw, ox, oy, font_sm)
    draw.text((ox + 6, oy + BG_GROUND_Y - 16), "haze band (≤20%α)", fill=(130, 140, 150), font=font_small, anchor="lt")
    # verdict
    draw.rectangle([ox + 6, oy + PANEL_H - 36, ox + PANEL_W - 6, oy + PANEL_H - 6], fill=(240, 236, 228))
    draw.text((ox + PANEL_W // 2, oy + PANEL_H - 21), "Haze reads well in color; too subtle in B&W", fill=(120, 100, 80), font=font_small, anchor="mm")


# ──────────────────────────────────────────────────────────────────────────────
# OPTION C (RECOMMENDED): Dual-warmth drop-shadow bands per tier
# Warm shadow under FG tier, cool shadow under BG tier
# ──────────────────────────────────────────────────────────────────────────────
def draw_option_c(draw, ox, oy, fonts):
    """Option C (RECOMMENDED): Per-tier drop-shadow bands using warm/cool tonal contrast."""
    font_lbl, font_sm, font_tag = fonts
    draw_panel_base(draw, ox, oy, "C — RECOMMENDED", font_lbl)

    # BG tier shadow: cool slate, 8px tall beneath BG_GROUND_Y
    shadow_h = 8
    for row in range(shadow_h):
        y_abs = oy + BG_GROUND_Y + row
        alpha_frac = 1.0 - (row / shadow_h)   # fades downward
        r = int(180 + (250 - 180) * (1 - alpha_frac))
        g = int(195 + (248 - 195) * (1 - alpha_frac))
        b = int(210 + (244 - 210) * (1 - alpha_frac))
        draw.line([(ox + 6, y_abs), (ox + PANEL_W - 7, y_abs)], fill=(r, g, b), width=1)

    # FG tier shadow: warm amber, 10px tall beneath FG_GROUND_Y
    shadow_h_fg = 10
    for row in range(shadow_h_fg):
        y_abs = oy + FG_GROUND_Y + row
        alpha_frac = 1.0 - (row / shadow_h_fg)
        r = int(220 + (250 - 220) * (1 - alpha_frac))
        g = int(200 + (248 - 200) * (1 - alpha_frac))
        b = int(160 + (244 - 160) * (1 - alpha_frac))
        draw.line([(ox + 6, y_abs), (ox + PANEL_W - 7, y_abs)], fill=(r, g, b), width=1)

    draw_stub_cast(draw, ox, oy, FG_CHAR_COL, BG_CHAR_COL, font_sm)
    draw_tier_labels(draw, ox, oy, font_sm)

    # annotation arrows
    draw.text((ox + 6, oy + BG_GROUND_Y + 2),  "cool shadow (BG)", fill=(100, 115, 135), font=font_small, anchor="lt")
    draw.text((ox + 6, oy + FG_GROUND_Y + 2),  "warm shadow (FG)", fill=(140, 100, 60),  font=font_small, anchor="lt")

    # "RECOMMENDED" banner
    draw.rectangle([ox + 6, oy + PANEL_H - 36, ox + PANEL_W - 6, oy + PANEL_H - 6], fill=(200, 220, 180))
    draw.text((ox + PANEL_W // 2, oy + PANEL_H - 21), "Warm/cool reads in B&W + color; aligns with palette grammar", fill=(50, 80, 40), font=font_small, anchor="mm")


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    img  = Image.new("RGB", (IMG_W, IMG_H), BG_COL)
    draw = ImageDraw.Draw(img)

    # title bar
    draw.rectangle([0, 0, IMG_W - 1, TITLE_H - 1], fill=(230, 224, 214))
    draw.text((IMG_W // 2, TITLE_H // 2),
              "Lineup Tier Depth Indicator — 3-Option Sketch (C45, Lee Tanaka)",
              fill=TITLE_COL, font=font_title, anchor="mm")

    fonts = (font_label, font_small, font_tag)

    for i, draw_fn in enumerate([draw_option_a, draw_option_b, draw_option_c]):
        ox = MARGIN + i * (PANEL_W + MARGIN)
        oy = TITLE_H + MARGIN
        draw_fn(draw, ox, oy, fonts)
        # refresh draw context after each panel (pil-standards.md)
        draw = ImageDraw.Draw(img)

    # enforce image size rule (≤1280px)
    img.thumbnail((1280, 1280))

    out_path = "output/production/lineup_tier_depth_sketch.png"
    img.save(out_path)
    print(f"Saved: {out_path}  ({img.width}×{img.height}px)")


if __name__ == "__main__":
    main()
