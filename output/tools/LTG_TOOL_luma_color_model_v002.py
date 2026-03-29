#!/usr/bin/env python3
"""
LTG_TOOL_luma_color_model_v002.py
Luma — Color Model v002
"Luma & the Glitchkin" — Cycle 30 / Maya Santos

C30 CHANGES from v001:
  - Eye proportions corrected: eye_r_x = int(head_r * 0.22) (was 14 = head_r*0.30).
    Matches canonical spec from expression sheet v007 and turnaround v003 (ew = HR*0.22).
    At head_r=46: eye_r_x = 10px (was 14px — 30% narrower, matches cast proportion audit).
  - Eye height adjusted accordingly: eye_r_y = int(head_r * 0.16) (was 10, ~0.22).
    Left eye slightly taller than right, matches v007 asymmetric spec.
  - Header updated to reflect v002 and Cycle 30 origin.
  - Silhouette proportions: head_r=46, body built to imply 3.2-head ratio (schematic only).
  - Palette, swatches, canvas size UNCHANGED from v001.

Format:
  800×500px — character color story document.
  Left half: character front silhouette in color (simplified)
  Right half: labeled swatches for each palette value

Output: output/characters/color_models/LTG_COLOR_luma_color_model_v002.png
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# ── Canonical Palette ─────────────────────────────────────────────────────────
SWATCHES = [
    ("#E8703A", (232, 112, 58),  "HOODIE ORANGE — base fill",          "Hoodie main surface"),
    ("#B84A20", (184,  74, 32),  "HOODIE SHADOW",                      "Folds, under arms, below torso"),
    ("#F59050", (245, 144, 80),  "HOODIE HIGHLIGHT",                   "Shoulders, upper chest"),
    ("#C8885A", (200, 136, 90),  "SKIN — lamp-lit base",               "Warm caramel (Glitch Layer scenes)"),
    ("#C4A882", (196, 168, 130), "SKIN — neutral base RW-10",          "Outdoor / standard lighting"),
    ("#1A0F0A", ( 26,  15, 10),  "HAIR — near-black espresso",         "Main hair mass"),
    ("#2A2850", ( 42,  40, 80),  "PANTS — warm dark indigo",           "Trousers"),
    ("#F5E8D0", (245, 232, 208), "SHOE UPPER — cream canvas",          "Sneaker upper"),
    ("#C75B39", (199,  91, 57),  "SHOE SOLE — terracotta",             "Chunky sole / tongue accent"),
    ("#00F0FF", (  0, 240, 255), "HOODIE PIXEL CYAN — GL-01",          "~40% of pixel pattern"),
    ("#FF2D6B", (255,  45, 107), "HOODIE PIXEL MAGENTA — GL-04",       "~20% of pixel pattern"),
    ("#C87D3E", (200, 125, 62),  "EYE IRIS — warm amber",              "Both eyes"),
    ("#FAF0DC", (250, 240, 220), "EYE WHITE — warm cream",             "Show standard"),
    ("#3B2820", ( 59,  40, 32),  "LINE COLOR — deep cocoa",            "Full-weight silhouette"),
]

CANVAS_W = 800
CANVAS_H = 500
CANVAS_BG = (22, 14, 8)
HEADER_H  = 52
LABEL_COL = (232, 112, 58)   # hoodie orange for header accent

# Character silhouette colors
SKIN       = (200, 136, 90)
SKIN_SH    = (160, 104, 64)
HAIR       = ( 26,  15, 10)
HAIR_HL    = ( 61,  31, 15)
HOODIE     = (232, 112, 58)
HOODIE_SH  = (184,  74, 32)
PANTS      = ( 42,  40, 80)
SHOE       = (245, 232, 208)
SHOE_SOLE  = (199,  91, 57)
LACES      = (  0, 240, 255)
EYE_W      = (250, 240, 220)
EYE_IRIS   = (200, 125, 62)
EYE_PUP    = ( 59,  40, 32)
EYE_HL     = (240, 240, 240)
LINE       = ( 59,  40, 32)
PX_CYAN    = (  0, 240, 255)
PX_MAG     = (255,  45, 107)
PX_WHITE   = (240, 240, 240)


def draw_pixel_pattern(draw, x0, y0, pw, ph):
    """Draw a simplified pixel hoodie pattern on a region."""
    import random
    rng = random.Random(7)
    cols = [PX_CYAN, PX_MAG, PX_WHITE]
    weights = [4, 2, 2]
    for _ in range(18):
        px = rng.randint(x0 + 4, x0 + pw - 6)
        py = rng.randint(y0 + 4, y0 + ph - 6)
        sz = rng.choice([3, 4])
        c = rng.choices(cols, weights=weights)[0]
        draw.rectangle([px, py, px + sz, py + sz], fill=c)


def draw_character_silhouette(draw, img, cx, cy):
    """Simplified Luma front view for color model reference.

    v002 PROPORTIONS: eye_r_x = int(head_r * 0.22) per canonical v007 spec.
    Silhouette is schematic — implies 3.2-head proportions.
    """
    # Body proportions (scaled for 800×500 layout)
    head_r   = 46
    body_w   = 70
    body_h   = 90
    body_top = cy - 20
    body_bot = body_top + body_h

    # --- Legs (behind everything) ---
    leg_w = 22
    leg_h = 60
    # Left leg
    draw.rectangle([cx - leg_w - 4, body_bot - 10, cx - 4, body_bot + leg_h],
                   fill=PANTS)
    # Right leg
    draw.rectangle([cx + 4, body_bot - 10, cx + leg_w + 4, body_bot + leg_h],
                   fill=PANTS)
    # Pants outline
    draw.rectangle([cx - leg_w - 4, body_bot - 10, cx - 4, body_bot + leg_h],
                   outline=LINE, width=2)
    draw.rectangle([cx + 4, body_bot - 10, cx + leg_w + 4, body_bot + leg_h],
                   outline=LINE, width=2)

    # --- Shoes ---
    shoe_w = 28
    shoe_h = 14
    shoe_sole_h = 6
    for side in [-1, 1]:
        sx = cx + side * (leg_w // 2 + (4 if side < 0 else 4))
        sy = body_bot + leg_h

        if side < 0:
            sx = cx - 4 - leg_w // 2
        else:
            sx = cx + 4 + leg_w // 2

        # Sole
        draw.ellipse([sx - shoe_w + 2, sy + shoe_h - 4,
                      sx + shoe_w - 2, sy + shoe_h + shoe_sole_h],
                     fill=SHOE_SOLE)
        # Upper
        draw.ellipse([sx - shoe_w + 4, sy - 4,
                      sx + shoe_w - 4, sy + shoe_h],
                     fill=SHOE)
        draw.ellipse([sx - shoe_w + 4, sy - 4,
                      sx + shoe_w - 4, sy + shoe_h],
                     outline=LINE, width=2)
        # Laces (cyan)
        for i in range(3):
            ly = sy - 2 + i * 3
            draw.line([sx - shoe_w // 3, ly, sx + shoe_w // 3, ly],
                      fill=LACES, width=1)

    # --- Hoodie body (trapezoid / A-line) ---
    hoodie_pts = [
        (cx - body_w // 2 + 8, body_top),           # top-left
        (cx + body_w // 2 - 8, body_top),            # top-right
        (cx + body_w // 2 + 10, body_bot),           # bottom-right wider
        (cx - body_w // 2 - 10, body_bot),           # bottom-left wider
    ]
    draw.polygon(hoodie_pts, fill=HOODIE)

    # Hoodie shadow (right side fold)
    shadow_pts = [
        (cx + body_w // 2 - 8, body_top),
        (cx + body_w // 2 - 2, body_top + 20),
        (cx + body_w // 2 + 10, body_bot),
        (cx + body_w // 2 - 4, body_bot),
    ]
    draw.polygon(shadow_pts, fill=HOODIE_SH)

    draw.polygon(hoodie_pts, outline=LINE, width=2)

    # Hood rim (cream lining)
    hood_rim = (250, 232, 200)
    draw.rectangle([cx - body_w // 2 + 8, body_top,
                    cx + body_w // 2 - 8, body_top + 12],
                   fill=hood_rim)

    # Pixel pattern on hoodie chest
    draw_pixel_pattern(draw, cx - 22, body_top + 14, 44, 34)

    # Hoodie pocket bump
    draw.rectangle([cx - 22, body_bot - 22, cx + 22, body_bot],
                   fill=HOODIE_SH, outline=LINE, width=1)

    # --- Arms ---
    arm_w = 16
    arm_h = 55
    # Left arm (viewer's left, slightly down)
    draw.rectangle([cx - body_w // 2 - arm_w + 4, body_top + 8,
                    cx - body_w // 2 + 4, body_top + 8 + arm_h],
                   fill=HOODIE, outline=LINE, width=2)
    # Right arm (viewer's right)
    draw.rectangle([cx + body_w // 2 - 4, body_top + 8,
                    cx + body_w // 2 + arm_w - 4, body_top + 8 + arm_h],
                   fill=HOODIE, outline=LINE, width=2)
    # Mitten hands
    hand_r = 10
    # Left hand
    draw.ellipse([cx - body_w // 2 - arm_w // 2 - hand_r + 4,
                  body_top + 8 + arm_h - hand_r,
                  cx - body_w // 2 - arm_w // 2 + hand_r + 4,
                  body_top + 8 + arm_h + hand_r],
                 fill=SKIN, outline=LINE, width=2)
    # Right hand
    draw.ellipse([cx + body_w // 2 + arm_w // 2 - hand_r - 4,
                  body_top + 8 + arm_h - hand_r,
                  cx + body_w // 2 + arm_w // 2 + hand_r - 4,
                  body_top + 8 + arm_h + hand_r],
                 fill=SKIN, outline=LINE, width=2)

    # --- Head ---
    hx0 = cx - head_r
    hy0 = cy - head_r * 2 - 8
    hx1 = cx + head_r
    hy1 = cy - 8
    draw.ellipse([hx0, hy0, hx1, hy1], fill=SKIN)

    # Cheek nubs (canonical classroom-style Luma head)
    nub_r = int(head_r * 0.14)
    cheek_y = hy0 + int(head_r * 1.15)
    draw.ellipse([hx0 - nub_r + 2, cheek_y - nub_r,
                  hx0 + nub_r + 2, cheek_y + nub_r], fill=SKIN)
    draw.ellipse([hx1 - nub_r - 2, cheek_y - nub_r,
                  hx1 + nub_r - 2, cheek_y + nub_r], fill=SKIN)

    # --- Hair mass ---
    hair_top = hy0 - 10
    hair_bot = hy0 + int(head_r * 0.6)
    draw.ellipse([cx - head_r - 4, hair_top,
                  cx + head_r + 4, hair_bot + 4], fill=HAIR)
    # Hair highlight
    draw.arc([cx - head_r + 4, hair_top + 4,
              cx + head_r - 4, hair_top + int(head_r * 0.5)],
             start=200, end=340, fill=HAIR_HL, width=2)

    # Head outline over hair
    draw.ellipse([hx0, hy0, hx1, hy1], outline=LINE, width=3)

    # --- Face features ---
    face_cy = hy0 + int(head_r * 1.0)

    # Eyes — v002: canonical proportions ew = head_r * 0.22 (matches v007 spec)
    eye_r_x = int(head_r * 0.22)   # ~10px (was 14px in v001 = head_r*0.30)
    eye_r_y = int(head_r * 0.16)   # ~7px  (was 10px in v001 = head_r*0.22)
    for side in [-1, 1]:
        ex = cx + side * int(head_r * 0.38)
        ey = face_cy - int(head_r * 0.08)
        draw.ellipse([ex - eye_r_x, ey - eye_r_y,
                      ex + eye_r_x, ey + eye_r_y], fill=EYE_W)
        draw.ellipse([ex - int(eye_r_x * 0.7), ey - int(eye_r_y * 0.7),
                      ex + int(eye_r_x * 0.7), ey + int(eye_r_y * 0.7)],
                     fill=EYE_IRIS)
        pup_r = 3
        draw.ellipse([ex - pup_r, ey - pup_r, ex + pup_r, ey + pup_r],
                     fill=EYE_PUP)
        # Highlight (upper left)
        draw.ellipse([ex - 4, ey - eye_r_y + 1,
                      ex - 1, ey - eye_r_y + 4], fill=EYE_HL)
    # Nose
    draw.arc([cx - 5, face_cy + 5, cx + 5, face_cy + 14],
             start=0, end=180, fill=LINE, width=2)
    # Mouth (neutral slight smile)
    draw.arc([cx - 12, face_cy + 14, cx + 12, face_cy + 28],
             start=10, end=170, fill=LINE, width=2)
    # Brows
    for side in [-1, 1]:
        bx = cx + side * int(head_r * 0.38)
        by = face_cy - int(head_r * 0.32)
        draw.arc([bx - 10, by - 3, bx + 10, by + 5],
                 start=200 if side < 0 else 340,
                 end=340 if side < 0 else 200,
                 fill=HAIR, width=2)


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
        font_h  = ImageFont.load_default()
        font_sw = ImageFont.load_default()
        font_sm = ImageFont.load_default()

    # Header
    draw.rectangle([0, 0, CANVAS_W, HEADER_H], fill=(18, 10, 4))
    title = "LUMA — Color Model v002  |  Cycle 30  |  HOODIE ORANGE #E8703A PRIMARY"
    try:
        tb = draw.textbbox((0, 0), title, font=font_h)
        tw = tb[2] - tb[0]; th = tb[3] - tb[1]
    except Exception:
        tw, th = 400, 20
    draw.text(((CANVAS_W - tw) // 2, (HEADER_H - th) // 2),
              title, fill=LABEL_COL, font=font_h)

    # Character silhouette area (left half)
    char_area_w = CANVAS_W // 2
    draw.rectangle([0, HEADER_H, char_area_w, CANVAS_H], fill=(28, 18, 10))

    char_cx = char_area_w // 2
    char_cy = HEADER_H + (CANVAS_H - HEADER_H) // 2 + 20
    draw_character_silhouette(draw, img, char_cx, char_cy)
    draw = ImageDraw.Draw(img)  # refresh after any paste operations

    # Character label
    char_label = "LUMA  (NEUTRAL — 3.2 heads)"
    try:
        clb = draw.textbbox((0, 0), char_label, font=font_sw)
        clw = clb[2] - clb[0]
        draw.text(((char_area_w - clw) // 2, CANVAS_H - 24),
                  char_label, fill=(200, 130, 70), font=font_sw)
    except Exception:
        pass

    # Color swatches (right half)
    sw_x0      = char_area_w + 16
    sw_w       = 36
    sw_h       = 24
    sw_pad     = 5
    sw_y0      = HEADER_H + 10
    label_x_off = sw_w + 10

    for i, (hexval, rgb, label, role) in enumerate(SWATCHES):
        sy = sw_y0 + i * (sw_h + sw_pad)
        if sy + sw_h > CANVAS_H - 8:
            break
        draw.rectangle([sw_x0, sy, sw_x0 + sw_w, sy + sw_h], fill=rgb)
        draw.rectangle([sw_x0, sy, sw_x0 + sw_w, sy + sw_h],
                       outline=(60, 40, 20), width=1)
        draw.text((sw_x0 + label_x_off, sy + 2),
                  hexval, fill=(210, 175, 100), font=font_sw)
        draw.text((sw_x0 + label_x_off, sy + 12),
                  label, fill=(220, 215, 205), font=font_sw)
        draw.text((sw_x0 + label_x_off + 170, sy + 12),
                  role, fill=(120, 100, 80), font=font_sm)

    # Divider
    draw.line([(char_area_w, HEADER_H), (char_area_w, CANVAS_H)],
              fill=(50, 35, 20), width=1)

    return img


def main():
    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "characters", "color_models"
    )
    os.makedirs(out_dir, exist_ok=True)

    model = build_color_model()
    # Apply image size rule: ≤ 1280px
    model.thumbnail((1280, 1280), Image.LANCZOS)
    out_path = os.path.join(out_dir, "LTG_COLOR_luma_color_model_v002.png")
    model.save(out_path)
    print(f"Saved: {out_path}")
    print(f"  Size: {model.size[0]}x{model.size[1]}px")
    print("  Swatches: 14 canonical colors documented")
    print("  Primary: HOODIE ORANGE #E8703A")
    print("  Eye proportions: ew = head_r * 0.22 (matches v007 canonical spec)")
    print("  Head features: circle + cheek nubs (classroom-style)")


if __name__ == "__main__":
    main()
