# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_colorkey_glitchstorm_gen.py
Color Key Generator — Style Frame 02 "Glitch Storm" (Scene Type: Nighttime Glitch Attack)
"Luma & the Glitchkin"

Author: Sam Kowalski, Color & Style Artist
Date: 2026-03-29
Cycle 12

Purpose:
  Generates a 640×360 color key thumbnail for the Glitch Storm scenario (Style Frame 02).
  This fills the gap identified in Priority 3: no rendered color key existed for SF02.
  The color key is based on the full color spec in style_frame_02_glitch_storm.md and
  cross-references Color Key 02 (Nighttime Glitch Attack) from scene_color_keys.md.

  The SF02 color key differs from the general Key 02 thumbnail in the following ways:
  - The crack is the primary compositional center (upper-right descending to lower-middle)
  - Dutch angle (4°) applied to the full composition
  - Character zone (lower third) shows Luma + Cosmo running, with Byte on left shoulder
  - Townspeople silhouettes in mid-ground building facades
  - Glitch confetti (storm-origin only): Cyan, Static White, Hot Magenta, UV Purple
    NO Acid Green in storm confetti — per master palette Forbidden #8
  - Three-tier street lighting: Cyan from crack (right), Magenta fill (ambient),
    Warm Gold from building windows (left)

Output: /home/wipkat/team/output/color/color_keys/thumbnails/
        LTG_COLOR_colorkey_glitchstorm.png
        (Also generates LTG-compliant copy of the existing key thumbnails for compliance)

Usage: python3 LTG_TOOL_colorkey_glitchstorm_gen.py
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/home/wipkat/team/output/color/color_keys/thumbnails"
W, H = 640, 360  # 16:9 thumbnail

# ── Palette constants (all inline tuples named) ──────────────────────────────
# Real World
WARM_CREAM      = (250, 240, 220)   # RW-01
SOFT_GOLD       = (232, 201,  90)   # RW-02
TERRACOTTA      = (199,  91,  57)   # RW-04
DEEP_COCOA      = ( 59,  40,  32)   # RW-11
WARM_TAN        = (196, 168, 130)   # RW-10
NIGHT_SKY_DEEP  = ( 26,  20,  40)   # RW-NS

# Glitch
ELEC_CYAN       = (  0, 240, 255)   # GL-01
HOT_MAGENTA     = (255,  45, 107)   # GL-02
ACID_GREEN      = ( 57, 255,  20)   # GL-03 — NOT in storm confetti; included for reference only
UV_PURPLE       = (123,  47, 190)   # GL-04
STATIC_WHITE    = (240, 240, 240)   # GL-05
DATA_BLUE       = ( 43, 127, 255)   # GL-06
CORRUPTED_AMBER = (255, 140,   0)   # GL-07
VOID_BLACK      = ( 10,  10,  20)   # GL-08

# Derived / scene-specific (from style_frame_02_glitch_storm.md)
CYAN_WASH_ROAD  = ( 42,  90, 106)   # ENV-02 — Asphalt under Cyan key
WARM_ROAD       = ( 74,  58,  42)   # ENV-03 — Asphalt under warm spill
DARK_ASPHALT    = ( 42,  42,  56)   # ENV-01 — Night asphalt base
NIGHT_SIDEWALK  = ( 58,  56,  72)   # ENV-04 — Nighttime sidewalk
DEEP_WARM_BLDG  = ( 90,  56,  32)   # ENV-07 — Building shadow side (deep warm)
ROOFLINE        = ( 26,  24,  32)   # ENV-08 — Near-void rooflines
CYAN_CAST_SHAD  = ( 10,  42,  58)   # ENV-05 — Cast shadows under Cyan key
VOID_SKY_CORE   = ( 10,  10,  20)   # Sky void core (= VOID_BLACK, named alias)
STORM_GROUND    = ( 26,  20,  40)   # Desaturated deep for townspeople silhouettes
# ENV-06 CORRECTED (Cycle 13, Jordan Reed — Naomi CRITICAL):
# Old value RGB(154,140,138): G=140 < R=154, B=138 < R=154 — reads WARM GREY, not cyan-lit.
# Fix: start from unlit terracotta ~(180,120,90), apply cyan key (R-30, G+52, B+72).
# G=172 > R=150 [PASS], B=162 > R=150 [PASS], G+B=334 > R+R=300 [PASS].
TERRACOTTA_CYAN_LIT = (150, 172, 162)  # ENV-06 — terracotta wall under ELEC_CYAN key

# Character colors (storm-lit, from SF02 spec)
LUMA_HOODIE_STM = (200, 105,  90)   # DRW-07 — Storm-Modified Hoodie Orange
# Cycle 13 saturation fix (Sam Kowalski — Naomi C12-3):
# Prior value RGB(192,122,112) had lower saturation than background building walls — violates
# character-over-background saturation rule (style_guide.md). New value RGB(200,105,90),
# HSL≈(9°,50%,57%), hex #C8695A. See LTG_TOOL_style_frame_02_glitch_storm.py for
# full derivation. master_palette.md DRW-07 entry updated to #C8695A.
LUMA_SKIN_STM   = (106, 180, 174)   # DRW-08 — Storm-Modified Skin (Cyan key)
COSMO_JACKET_S  = (128, 192, 204)   # DRW-09 — Storm-Modified Jacket (Cosmo)
LUMA_HAIR_STM   = ( 59,  40,  32)   # base hair, with RIM_MAGENTA on motion edges
RIM_MAGENTA     = (106,  42,  58)   # DRW-17 — Magenta-Influenced Hair (Storm)
HOODIE_SHADOW   = ( 58,  26,  20)   # DRW-03 shadow (3A1A14) — deep hoodie shadow
BYTE_AMBER_OUTLINE = (255, 140,  0) # GL-07 — Corrupted Amber outline for Byte
BYTE_VOID       = ( 10,  10,  20)   # Byte body fill = Void Black (VOID_BLACK alias)
BYTE_CRACKED_EYE = (255,  45, 107) # GL-02 Hot Magenta — cracked eye
BYTE_CYAN_EYE   = (  0, 240, 255)  # GL-01 Electric Cyan — cyan eye


def load_font(size=13, bold=False):
    paths = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
         else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def lbl(draw, x, y, text, font, fg=(255, 255, 255), bg=None):
    if bg:
        bb = draw.textbbox((x, y), text, font=font)
        draw.rectangle([bb[0]-2, bb[1]-1, bb[2]+2, bb[3]+1], fill=bg)
    draw.text((x, y), text, fill=fg, font=font)


def palette_strip(draw, swatches, x, y, sw=36, sh=26, gap=4):
    """Draw a row of labeled color swatches with contrast-aware labels."""
    font = load_font(9)
    for i, (col, name) in enumerate(swatches):
        sx = x + i * (sw + gap)
        draw.rectangle([sx, y, sx + sw, y + sh], fill=col)
        draw.rectangle([sx, y, sx + sw, y + sh], outline=(80, 70, 60), width=1)
        r, g, b = col
        lum = 0.299 * r / 255 + 0.587 * g / 255 + 0.114 * b / 255
        tc = (10, 10, 10) if lum > 0.45 else (240, 235, 220)
        draw.text((sx + 2, y + 14), name[:5], fill=tc, font=font)


def apply_dutch_angle(img, degrees=4.0):
    """Apply a clockwise Dutch angle tilt to the image.
    The image is rotated, then center-cropped back to original dimensions.
    This creates the subtle compositional tilt without letterboxing.
    """
    # Expand to avoid clipping corners during rotation
    expanded = Image.new("RGB", (int(W * 1.2), int(H * 1.2)), VOID_BLACK)
    offset_x = (expanded.width - W) // 2
    offset_y = (expanded.height - H) // 2
    expanded.paste(img, (offset_x, offset_y))
    rotated = expanded.rotate(-degrees, expand=False)  # negative = clockwise
    # Center crop back to W×H
    cx = (rotated.width - W) // 2
    cy = (rotated.height - H) // 2
    return rotated.crop((cx, cy, cx + W, cy + H))


def generate_sf02_glitch_storm_colorkey():
    """
    Generate the Style Frame 02 — Glitch Storm color key thumbnail.

    Composition (before dutch angle):
    - Sky (upper 60%): Dark night + UV Purple glitch masses + main crack (upper-right to lower-center)
    - Mid-ground (25-60%): Millbrook rooftops + building facades
    - Street (lower 25%): Dark asphalt with competing light pools
    - Characters zone (lower 20%): Luma + Cosmo running (simplified silhouette blocks)

    Color narrative:
    - Sky = totally lost to glitch (Void Black, UV Purple, Hot Magenta, Cyan)
    - Buildings = contested (terracotta partially neutralized by Cyan)
    - Street = contested (Cyan pool vs. warm window spill)
    - Characters = most saturated, most alive, fighting both worlds simultaneously
    """
    random.seed(202612)  # deterministic for reproducible output

    img = Image.new("RGB", (W, H), NIGHT_SKY_DEEP)
    draw = ImageDraw.Draw(img)

    # ── SKY LAYER (upper 60% of frame) ──────────────────────────────────────
    # Base night sky
    draw.rectangle([0, 0, W, int(H * 0.60)], fill=NIGHT_SKY_DEEP)

    # UV Purple glitch storm masses — angular, blocky (corrupted cloud forms)
    # Left mass
    draw.rectangle([0, 0, int(W * 0.45), int(H * 0.22)], fill=UV_PURPLE)
    draw.rectangle([int(W * 0.05), int(H * 0.08), int(W * 0.38), int(H * 0.30)],
                   fill=UV_PURPLE)
    # Right mass (storm front from upper-right)
    draw.rectangle([int(W * 0.55), 0, W, int(H * 0.35)], fill=UV_PURPLE)
    draw.rectangle([int(W * 0.70), 0, W, int(H * 0.50)], fill=UV_PURPLE)

    # Void Black cores within UV masses (deepest storm zones)
    draw.rectangle([int(W * 0.10), int(H * 0.04), int(W * 0.32), int(H * 0.16)],
                   fill=VOID_SKY_CORE)
    draw.rectangle([int(W * 0.72), int(H * 0.02), int(W * 0.92), int(H * 0.18)],
                   fill=VOID_SKY_CORE)

    # ── MAIN CRACK — descends from upper-right to lower-center ──────────────
    # Per SF02 spec: "from upper-right corner down through the right vertical third"
    # The crack has orthogonal segments (digital damage, not organic lightning)
    crack_segs = [
        (int(W * 0.82), 0),
        (int(W * 0.80), int(H * 0.12)),
        (int(W * 0.75), int(H * 0.18)),   # orthogonal step
        (int(W * 0.75), int(H * 0.28)),
        (int(W * 0.68), int(H * 0.32)),   # 45-degree break
        (int(W * 0.62), int(H * 0.42)),
        (int(W * 0.58), int(H * 0.55)),   # reaching toward mid-frame
    ]

    # Hot Magenta burning edge (outermost glow — 2px accent per spec)
    draw.line(crack_segs, fill=HOT_MAGENTA, width=12)
    # Electric Cyan core
    draw.line(crack_segs, fill=ELEC_CYAN, width=8)
    # Static White overexposed center
    draw.line(crack_segs, fill=STATIC_WHITE, width=3)

    # Cyan flood wash on right side of frame (crack illuminates right side)
    cyan_wash = Image.new("RGB", (int(W * 0.45), H), ELEC_CYAN)
    # Blend by drawing a semi-transparent rectangle — simulated via alpha composite
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.rectangle([int(W * 0.55), 0, W, int(H * 0.65)],
                      fill=(0, 240, 255, 40))  # Cyan wash, alpha 40/255
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Redraw crack on top of wash
    draw.line(crack_segs, fill=HOT_MAGENTA, width=8)
    draw.line(crack_segs, fill=ELEC_CYAN, width=5)
    draw.line(crack_segs, fill=STATIC_WHITE, width=2)

    # Sub-crack branches (Data Blue at tips — narrowing away from main)
    sub_cracks = [
        [(int(W * 0.75), int(H * 0.28)), (int(W * 0.84), int(H * 0.36))],
        [(int(W * 0.68), int(H * 0.32)), (int(W * 0.78), int(H * 0.40))],
    ]
    for sc in sub_cracks:
        draw.line(sc, fill=DATA_BLUE, width=2)

    # ── STORM PIXEL CONFETTI — source-origin physics ─────────────────────────
    # Storm confetti = Cyan, Static White, Hot Magenta, UV Purple ONLY
    # NO ACID GREEN — per master palette Forbidden #8 and SF02 spec
    STORM_CONFETTI_COLORS = [ELEC_CYAN, STATIC_WHITE, HOT_MAGENTA, UV_PURPLE]
    # Near crack: large (8–12px), dense
    for _ in range(25):
        px = random.randint(int(W * 0.45), W)
        py = random.randint(0, int(H * 0.50))
        ps = random.choice([6, 8, 10])  # large near source
        pc = random.choice(STORM_CONFETTI_COLORS)
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)
    # Far from crack: small (2–4px), sparse — falling to street level
    for _ in range(15):
        px = random.randint(0, W)
        py = random.randint(int(H * 0.50), int(H * 0.80))
        ps = random.choice([2, 3])  # small, traveled far from source
        pc = random.choice(STORM_CONFETTI_COLORS)
        draw.rectangle([px, py, px + ps, py + ps], fill=pc)

    # ── BUILDINGS (mid-ground, 30-65% height) ────────────────────────────────
    # Millbrook rooftop silhouettes — nighttime, partially Cyan-lit (right-facing walls)
    buildings = [
        # (x_left, y_top, x_right, y_bottom) — varied heights for skyline
        (0,            int(H * 0.30), int(W * 0.14), int(H * 0.65)),
        (int(W * 0.12), int(H * 0.25), int(W * 0.27), int(H * 0.65)),
        (int(W * 0.25), int(H * 0.32), int(W * 0.40), int(H * 0.65)),
        (int(W * 0.38), int(H * 0.27), int(W * 0.54), int(H * 0.65)),
        (int(W * 0.52), int(H * 0.23), int(W * 0.68), int(H * 0.65)),
        (int(W * 0.66), int(H * 0.28), int(W * 0.82), int(H * 0.65)),
        (int(W * 0.80), int(H * 0.22), W,              int(H * 0.65)),
    ]
    for bx0, by0, bx1, by1 in buildings:
        # Shadow (left) faces — deep warm
        draw.rectangle([bx0, by0, bx1, by1], fill=DEEP_WARM_BLDG)
        # Right-facing walls (Cyan-lit) — terracotta neutralized by Cyan key
        # Simplified: right 40% of building face is Cyan-contaminated
        cx_split = bx0 + int((bx1 - bx0) * 0.60)
        draw.rectangle([cx_split, by0, bx1, by1], fill=TERRACOTTA_CYAN_LIT)  # ENV-06 (Cycle 13 fix)
        # Roofline (near-void)
        draw.rectangle([bx0, by0, bx1, by0 + 3], fill=ROOFLINE)
        # Warm windows (last vestige of safety — interior lit)
        win_spacing = max(12, (bx1 - bx0) // 3)
        for wx in range(bx0 + 6, bx1 - 10, win_spacing):
            wy = by0 + random.randint(8, int((by1 - by0) * 0.5))
            draw.rectangle([wx, wy, wx + 8, wy + 7], fill=WARM_CREAM)
        # Townspeople silhouette at a few windows (darker shape inside the light)
        tw_wx = bx0 + int((bx1 - bx0) * 0.30)
        tw_wy = by0 + int((by1 - by0) * 0.40)
        draw.rectangle([tw_wx, tw_wy, tw_wx + 5, tw_wy + 6], fill=STORM_GROUND)

    # ── STREET (lower 35%, contested zone) ────────────────────────────────────
    street_y = int(H * 0.65)

    # Base dark asphalt
    draw.rectangle([0, street_y, W, H], fill=DARK_ASPHALT)

    # Cyan light pool (right side — from the crack above)
    ov2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov2_draw = ImageDraw.Draw(ov2)
    ov2_draw.rectangle([int(W * 0.42), street_y, W, H],
                       fill=(42, 90, 106, 180))  # ENV-02, alpha 180
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, ov2)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Warm window spill (left side — building light on sidewalk)
    ov3 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov3_draw = ImageDraw.Draw(ov3)
    ov3_draw.rectangle([0, street_y + int(H * 0.04), int(W * 0.35), H],
                       fill=(74, 58, 42, 40))  # ENV-03, alpha 40
    # Cycle 13 alpha alignment (Sam Kowalski — Naomi C12-2):
    # Prior value: alpha=150 (~59%). SF02 background script (LTG_TOOL_style_frame_02_glitch_storm.py)
    # uses alpha=40 (~16%) for the same warm window spill scene value.
    # CANONICAL: alpha=40 (~16%). Rationale: this is a background building window spill on
    # a stormy night — a subtle warm glow, not a dominant light source. 59% was too strong
    # and would overpower the dominant cyan key from the crack. 16% reads as the correct
    # "last light in a dark building" quality. Updated this script to match the SF02 bg value.
    # Document: master_palette.md Section 1C ENV-03 note, warm spill canonical alpha = 40/255.
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, ov3)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Sidewalk edge
    draw.rectangle([0, street_y, W, street_y + 5], fill=NIGHT_SIDEWALK)

    # ── CHARACTERS (lower 20%, foreground) ────────────────────────────────────
    # Simplified silhouette blocks showing color breakdown
    # Luma — left third-line, small against frame height
    char_y_base = int(H * 0.78)
    char_h = int(H * 0.20)  # characters occupy ~20% of frame height
    char_w = int(W * 0.06)

    luma_x = int(W * 0.28)
    # Luma body — hoodie (storm-modified orange)
    draw.rectangle([luma_x, char_y_base, luma_x + char_w, char_y_base + char_h],
                   fill=LUMA_HOODIE_STM)
    # Skin tone on face zone (top of figure)
    draw.rectangle([luma_x + 2, char_y_base - int(char_h * 0.20),
                    luma_x + char_w - 2, char_y_base + 4],
                   fill=LUMA_SKIN_STM)
    # Hair (motion arc) with magenta rim
    draw.rectangle([luma_x - 4, char_y_base - int(char_h * 0.18),
                    luma_x + 4, char_y_base],
                   fill=RIM_MAGENTA)
    # Cast shadow — very dark Cyan-cast
    draw.ellipse([luma_x - 2, char_y_base + char_h,
                  luma_x + char_w + 2, char_y_base + char_h + 5],
                 fill=CYAN_CAST_SHAD)

    # Byte on Luma's LEFT shoulder — tiny, amber outline
    byte_x = luma_x - 5
    byte_y = char_y_base + int(char_h * 0.10)
    byte_sz = 7  # very small in wide shot
    draw.rectangle([byte_x - 1, byte_y - 1, byte_x + byte_sz + 1, byte_y + byte_sz + 1],
                   fill=BYTE_AMBER_OUTLINE)  # amber outline (2px)
    draw.rectangle([byte_x, byte_y, byte_x + byte_sz, byte_y + byte_sz],
                   fill=BYTE_VOID)
    # Byte's cracked eye facing right (toward crack/danger)
    draw.point((byte_x + byte_sz, byte_y + 2), fill=BYTE_CRACKED_EYE)

    # Cosmo — one stride behind Luma, slightly right
    cosmo_x = int(W * 0.35)
    # Cosmo jacket (storm-modified lavender)
    draw.rectangle([cosmo_x, char_y_base + 3, cosmo_x + char_w,
                    char_y_base + char_h],
                   fill=COSMO_JACKET_S)
    # Cosmo skin
    draw.rectangle([cosmo_x + 2, char_y_base - int(char_h * 0.18),
                    cosmo_x + char_w - 2, char_y_base + 7],
                   fill=LUMA_SKIN_STM)  # same storm skin modification
    # Cosmo cast shadow
    draw.ellipse([cosmo_x - 2, char_y_base + char_h + 2,
                  cosmo_x + char_w + 2, char_y_base + char_h + 7],
                 fill=CYAN_CAST_SHAD)

    # ── SHATTERED STOREFRONT (right foreground, partial) ──────────────────────
    store_x = int(W * 0.72)
    draw.rectangle([store_x, int(H * 0.58), store_x + int(W * 0.08), H],
                   fill=(50, 42, 50))  # dark storefront
    # Broken glass — Static White + Cyan reflection
    draw.polygon([(store_x + 4, int(H * 0.60)),
                  (store_x + 18, int(H * 0.63)),
                  (store_x + 10, int(H * 0.70)),
                  (store_x + 2, int(H * 0.68))],
                 fill=STATIC_WHITE)
    draw.line([(store_x + 4, int(H * 0.60)),
               (store_x + 14, int(H * 0.75))],
              fill=ELEC_CYAN, width=1)  # glitch crack spreading

    # ── PALETTE STRIP ─────────────────────────────────────────────────────────
    swatches = [
        (NIGHT_SKY_DEEP,   "Night"),
        (UV_PURPLE,        "UVPur"),
        (ELEC_CYAN,        "Cyan"),
        (HOT_MAGENTA,      "Mag*"),   # * = accent edge, not full zone
        (VOID_BLACK,       "Void"),
        (SOFT_GOLD,        "Gold*"),  # * = building window accent only
        (WARM_CREAM,       "Cream*"), # * = window glow micro-accent (5%)
        (STATIC_WHITE,     "Wht*"),   # * = specular/confetti accent
        (CORRUPTED_AMBER,  "Amb*"),   # * = Byte outline exception only
    ]
    palette_strip(draw, swatches, 8, H - 38)

    # ── LABELS ────────────────────────────────────────────────────────────────
    lbl(draw, 8, 8,
        "SF02 Color Key — Glitch Storm  [Cycle 12]",
        load_font(14, bold=True), fg=STATIC_WHITE, bg=VOID_BLACK)
    lbl(draw, 8, 26,
        "Storm confetti: Cyan/White/Magenta/UVPurple only. NO Acid Green. Byte: Amber outline.",
        load_font(9), fg=STATIC_WHITE, bg=(10, 10, 20, 200))
    lbl(draw, 8, 38,
        "Sky = glitch-total. Buildings = contested. Street = warm-vs-cold. Characters = alive.",
        load_font(9), fg=(200, 180, 240), bg=VOID_BLACK)

    # ── OUTPUT ────────────────────────────────────────────────────────────────
    # Apply 4° clockwise Dutch angle per SF02 spec
    img = apply_dutch_angle(img, degrees=4.0)

    out_path = os.path.join(OUTPUT_DIR, "LTG_COLOR_colorkey_glitchstorm.png")
    img.save(out_path)
    print(f"Saved: {out_path}")
    return out_path


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    result = generate_sf02_glitch_storm_colorkey()
    print(f"Done. Output: {result}")
