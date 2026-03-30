# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_luma_cold_overlay_swatches.py
Luma & the Glitchkin — Cold Overlay Swatch Generator

Purpose: Generate a reference swatch PNG showing base color, Electric Cyan overlay,
         and alpha-composite result side-by-side for each cold overlay variant documented
         in luma_color_model.md (Cold/Cyan Overlay Variants section).

Formula: C_result = C_base * (1 - a) + C_overlay * a  (per channel, a as 0.0-1.0)
Overlay: Electric Cyan GL-01 = #00F0FF (R:0, G:240, B:255)

Output: output/characters/color_models/swatches/LTG_COLOR_luma_cold_overlay.png
Canvas: 1800 x 1500 px

Cycle 18 — Sam Kowalski, Color & Style Artist
Recalculated C18 — correct alpha-composite formula applied.
Rules: Open source only (PIL). After img.paste(), always refresh draw = ImageDraw.Draw(img).
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ── Constants ───────────────────────────────────────────────────────────────

ELEC_CYAN = (0, 240, 255)       # GL-01 — the overlay color for all swatches

# Canvas dimensions
W, H = 1800, 1500

# Layout
MARGIN_LEFT = 60
MARGIN_TOP = 100
SWATCH_W = 180
SWATCH_H = 80
SWATCH_GAP = 20
GROUP_GAP = 50
LABEL_H = 28
ROW_H = SWATCH_H + LABEL_H + 20

BG_COLOR = (18, 14, 22)          # Near-void dark background
TEXT_COLOR = (230, 220, 200)     # Warm cream text
HEADER_COLOR = (0, 240, 255)     # Electric Cyan for headers
PASS_COLOR = (57, 255, 20)       # Acid Green for PASS
FAIL_COLOR = (255, 45, 107)      # Hot Magenta for FAIL
THRESHOLD_COLOR = (255, 140, 0)  # Corrupted Amber for threshold row

# ── Alpha-composite formula ──────────────────────────────────────────────────

def blend(base, alpha):
    """Correct alpha-composite: C_result = C_base*(1-a) + C_overlay*a"""
    r = round(base[0] * (1 - alpha) + ELEC_CYAN[0] * alpha)
    g = round(base[1] * (1 - alpha) + ELEC_CYAN[1] * alpha)
    b = round(base[2] * (1 - alpha) + ELEC_CYAN[2] * alpha)
    return (r, g, b)

def is_cyan_dominant(rgb):
    r, g, b = rgb
    return g > r and b > r

def to_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(*rgb)

# ── Base colors ──────────────────────────────────────────────────────────────

SKIN_LAMP   = (200, 136, 90)    # #C8885A — CHAR-L-01 lamp-lit
SKIN_NEUT   = (196, 168, 130)   # #C4A882 — RW-10 neutral
HOODIE_BASE = (232, 114, 42)    # #E8722A — hoodie orange
HOODIE_SH   = (184, 85, 32)     # #B85520 — hoodie shadow

# Alpha levels for standard table entries (as fractions 0.0-1.0)
ALPHA_LEVELS = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35]

# Threshold alphas (min alpha for G>R AND B>R on each surface)
THRESHOLD_ALPHAS = {
    'skin_lamp': 0.31,
    'skin_neut': 0.21,
    'hoodie_base': 0.43,
    'hoodie_sh': 0.38,
}

# Groups: (label, base_color, base_name, alphas_to_show, threshold_alpha)
GROUPS = [
    (
        "Skin — Lamp-Lit Base (#C8885A, CHAR-L-01)",
        SKIN_LAMP,
        "#C8885A",
        ALPHA_LEVELS + [THRESHOLD_ALPHAS['skin_lamp']],
        THRESHOLD_ALPHAS['skin_lamp'],
    ),
    (
        "Skin — Neutral Base (#C4A882, RW-10)",
        SKIN_NEUT,
        "#C4A882",
        ALPHA_LEVELS + [THRESHOLD_ALPHAS['skin_neut']],
        THRESHOLD_ALPHAS['skin_neut'],
    ),
    (
        "Hoodie Orange Base (#E8722A)",
        HOODIE_BASE,
        "#E8722A",
        [0.10, 0.20, 0.30, 0.35, THRESHOLD_ALPHAS['hoodie_base'], 0.50],
        THRESHOLD_ALPHAS['hoodie_base'],
    ),
    (
        "Hoodie Shadow (#B85520)",
        HOODIE_SH,
        "#B85520",
        [0.10, 0.20, 0.30, THRESHOLD_ALPHAS['hoodie_sh'], 0.40],
        THRESHOLD_ALPHAS['hoodie_sh'],
    ),
]

# ── Drawing helpers ──────────────────────────────────────────────────────────

def draw_swatch_triple(draw, img, x, y, base, alpha, threshold_alpha, swatch_w, swatch_h):
    """Draw base | overlay | result swatches side by side. Returns x-end of the triple."""
    result = blend(base, alpha)
    is_threshold = (round(alpha * 100) == round(threshold_alpha * 100))
    is_dominant = is_cyan_dominant(result)

    sw = swatch_w
    gap = 4

    # Base swatch
    draw.rectangle([x, y, x + sw - 1, y + swatch_h - 1], fill=base)
    # Overlay (Electric Cyan with alpha shown as tinted rect)
    overlay_display = tuple(
        round(255 * (1 - alpha) + c * alpha) for c in (40, 40, 40)
    )
    # Show the cyan overlay color at full saturation with alpha indicated by label
    draw.rectangle([x + sw + gap, y, x + sw * 2 + gap - 1, y + swatch_h - 1], fill=ELEC_CYAN)
    # Result swatch
    draw.rectangle([x + sw * 2 + gap * 2, y, x + sw * 3 + gap * 2 - 1, y + swatch_h - 1], fill=result)

    # Threshold highlight border
    if is_threshold:
        border_c = THRESHOLD_COLOR
        for bx, by, bx2, by2 in [
            (x, y, x + sw * 3 + gap * 2 - 1, y + swatch_h - 1)
        ]:
            draw.rectangle([bx - 3, by - 3, bx2 + 3, by2 + 3], outline=border_c, width=3)

    return x + sw * 3 + gap * 2

def draw_label(draw, x, y, base, alpha, result, threshold_alpha, font, small_font):
    """Draw label row under a swatch triple."""
    pct = round(alpha * 100)
    is_threshold = (round(alpha * 100) == round(threshold_alpha * 100))
    is_dominant = is_cyan_dominant(result)
    dominant_str = "PASS" if is_dominant else "FAIL"
    dominant_color = PASS_COLOR if is_dominant else FAIL_COLOR
    if is_threshold:
        dominant_str = "THRESHOLD"
        dominant_color = THRESHOLD_COLOR

    hex_val = to_hex(result)
    r, g, b = result
    label = f"α={alpha:.2f} ({pct}%)  →  {hex_val} RGB({r},{g},{b})  [{dominant_str}]"
    draw.text((x, y), label, fill=dominant_color if is_threshold or is_dominant else TEXT_COLOR, font=small_font)

# ── Main ─────────────────────────────────────────────────────────────────────

def make_font(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", size)
    except Exception:
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)
        except Exception:
            return ImageFont.load_default()

def generate():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_large = make_font(22)
    font_mid   = make_font(16)
    font_small = make_font(13)

    # ── Title ──────────────────────────────────────────────────────────────
    draw.text((MARGIN_LEFT, 20), "LUMA — Cold / Cyan Overlay Swatches", fill=HEADER_COLOR, font=font_large)
    draw.text((MARGIN_LEFT, 50), "Electric Cyan GL-01 #00F0FF  ·  Recalculated C18  ·  Correct alpha-composite formula", fill=TEXT_COLOR, font=font_small)
    draw.text((MARGIN_LEFT, 70), "Formula: C_result = C_base × (1 − α) + C_overlay × α  (per channel)", fill=TEXT_COLOR, font=font_small)

    # Legend
    lx = W - 420
    draw.rectangle([lx, 20, lx + 18, 38], fill=PASS_COLOR)
    draw.text((lx + 24, 20), "PASS — G>R AND B>R (cyan-dominant)", fill=TEXT_COLOR, font=font_small)
    draw.rectangle([lx, 44, lx + 18, 62], fill=FAIL_COLOR)
    draw.text((lx + 24, 44), "FAIL — not cyan-dominant", fill=TEXT_COLOR, font=font_small)
    draw.rectangle([lx, 68, lx + 18, 86], fill=THRESHOLD_COLOR)
    draw.text((lx + 24, 68), "THRESHOLD — minimum α for dominance", fill=TEXT_COLOR, font=font_small)

    # Swatch column headers
    y = MARGIN_TOP
    draw.text((MARGIN_LEFT, y), "BASE", fill=TEXT_COLOR, font=font_small)
    draw.text((MARGIN_LEFT + SWATCH_W + 4, y), "OVERLAY", fill=TEXT_COLOR, font=font_small)
    draw.text((MARGIN_LEFT + SWATCH_W * 2 + 8, y), "RESULT", fill=TEXT_COLOR, font=font_small)

    y += 22

    for group_label, base, base_name, alphas, threshold_alpha in GROUPS:
        # Group header
        draw.text((MARGIN_LEFT, y), group_label, fill=HEADER_COLOR, font=font_mid)
        y += 26

        # Base swatch standalone label
        draw.rectangle([MARGIN_LEFT, y, MARGIN_LEFT + SWATCH_W - 1, y + 24], fill=base)
        draw.text((MARGIN_LEFT + SWATCH_W + 8, y + 4), f"Base {base_name}  RGB{base}", fill=TEXT_COLOR, font=font_small)
        y += 32

        # Swatch triples
        sorted_alphas = sorted(set(round(a, 2) for a in alphas))
        for alpha in sorted_alphas:
            result = blend(base, alpha)
            # Draw triple
            draw_swatch_triple(draw, img, MARGIN_LEFT, y, base, alpha, threshold_alpha, SWATCH_W, SWATCH_H)
            # IMPORTANT: refresh draw after any img.paste() — rule compliance
            draw = ImageDraw.Draw(img)
            # Draw label
            draw_label(draw, MARGIN_LEFT, y + SWATCH_H + 4, base, alpha, result, threshold_alpha, font_mid, font_small)
            y += SWATCH_H + LABEL_H + 14

        y += GROUP_GAP

    # Footer
    draw.text((MARGIN_LEFT, H - 30), "LTG_TOOL_luma_cold_overlay_swatches.py  ·  Sam Kowalski, Color & Style Artist  ·  Cycle 18  ·  Luma & the Glitchkin", fill=(100, 90, 80), font=font_small)

    # ── Save ──────────────────────────────────────────────────────────────
    out_path = "/home/wipkat/team/output/characters/color_models/swatches/LTG_COLOR_luma_cold_overlay.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    generate()
