#!/usr/bin/env python3
"""
LTG_COLOR_cosmo_color_model_v001.py
Cosmo — Color Model v001
"Luma & the Glitchkin" — Cycle 25 / Maya Santos

Format matches LTG_COLOR_glitch_color_model_v001.py:
  800×500px — character color story document.
  Left half: character front silhouette in color (simplified)
  Right half: labeled swatches for each palette value

All palette values from canonical source: cosmo_color_model.md

Output: output/characters/color_models/LTG_COLOR_cosmo_color_model_v001.png

[Renamed from LTG_COLOR_cosmo_color_model_v001.py to LTG_TOOL_cosmo_color_model_v001.py
 in Cycle 28 — generator files use LTG_TOOL_ prefix. Output PNG names are unchanged.]
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# ── Canonical Palette ─────────────────────────────────────────────────────────
SWATCHES = [
    ("#D9C09A", (217, 192, 154), "SKIN — light warm olive",            "Face, hands"),
    ("#B89A78", (184, 154, 120), "SKIN_SHADOW",                        "Under chin, inner arm, nose"),
    ("#EED4B0", (238, 212, 176), "SKIN_HIGHLIGHT",                     "Forehead, nose bridge, cheekbone"),
    ("#1A1824", ( 26,  24,  36), "HAIR — blue-black",                  "Main hair mass (faint blue cast)"),
    ("#5C3A20", ( 92,  58,  32), "GLASS FRAME — warm espresso",        "Thick plastic frames (0.06x head w)"),
    ("#EEF4FF", (238, 244, 255), "GLASS LENS — ghost blue",            "Barely-perceptible tint"),
    ("#5B8DB8", ( 91, 141, 184), "STRIPE BLUE / NOTEBOOK — cerulean",  "Blue stripes + notebook cover"),
    ("#7A9E7E", (122, 158, 126), "STRIPE GREEN — sage",                "Green stripes on shirt"),
    ("#8C8880", (140, 136, 128), "PANTS — warm mid-gray",              "Slim-fit chinos"),
    ("#3D6B45", ( 61, 107,  69), "EYE IRIS — warm forest green",       "Muted, intellectual"),
    ("#FAF0DC", (250, 240, 220), "EYE WHITE — warm cream",             "Show standard"),
    ("#A89BBF", (168, 155, 191), "CARDIGAN — dusty lavender",          "Optional layer (school / cold scenes)"),
    ("#F0F0F0", (240, 240, 240), "GLASS GLARE — static white",         "Crescent at lens upper edge"),
    ("#3B2820", ( 59,  40,  32), "LINE COLOR — deep cocoa",            "Silhouette + 60% internal"),
]

CANVAS_W  = 800
CANVAS_H  = 500
CANVAS_BG = (16, 14, 10)
HEADER_H  = 52
LABEL_COL = (91, 141, 184)   # cerulean for header accent

# Character silhouette colors
SKIN       = (217, 192, 154)
SKIN_SH    = (184, 154, 120)
SKIN_HL    = (238, 212, 176)
HAIR       = ( 26,  24,  36)
HAIR_HL    = ( 44,  43,  64)
EYE_W      = (250, 240, 220)
IRIS       = ( 61, 107,  69)
PUPIL      = ( 59,  40,  32)
EYE_HL     = (240, 240, 240)
GLASS_FR   = ( 92,  58,  32)
GLASS_LN   = (238, 244, 255)
GLASS_GL   = (240, 240, 240)
STRIPE_A   = ( 91, 141, 184)
STRIPE_B   = (122, 158, 126)
PANTS      = (140, 136, 128)
PANTS_SH   = (106, 100,  96)
SHOE       = ( 92,  58,  32)
SHOE_SOLE  = (184, 154, 120)
NOTEBOOK   = ( 91, 141, 184)
NOTEBK_SP  = ( 61, 107, 138)
LINE       = ( 59,  40,  32)


def draw_character_silhouette(draw, cx, cy):
    """Simplified Cosmo front view for color model reference."""
    head_r_x = 34
    head_r_y = 40
    body_w   = 58
    body_h   = 80
    body_top = cy - 22
    body_bot = body_top + body_h

    # --- Legs ---
    leg_w = 18
    leg_h = 56
    draw.rectangle([cx - leg_w - 2, body_bot - 8, cx - 2, body_bot + leg_h],
                   fill=PANTS)
    draw.rectangle([cx + 2, body_bot - 8, cx + leg_w + 2, body_bot + leg_h],
                   fill=PANTS)
    # Center crease line (mandatory)
    draw.line([cx - leg_w // 2 - 1, body_bot - 8,
               cx - leg_w // 2 - 1, body_bot + leg_h],
              fill=PANTS_SH, width=1)
    draw.line([cx + leg_w // 2 + 1, body_bot - 8,
               cx + leg_w // 2 + 1, body_bot + leg_h],
              fill=PANTS_SH, width=1)
    draw.rectangle([cx - leg_w - 2, body_bot - 8, cx - 2, body_bot + leg_h],
                   outline=LINE, width=2)
    draw.rectangle([cx + 2, body_bot - 8, cx + leg_w + 2, body_bot + leg_h],
                   outline=LINE, width=2)

    # --- Shoes (low-profile) ---
    shoe_w = 20
    shoe_h = 10
    for side in [-1, 1]:
        sx = cx + side * (leg_w // 2 + (2 if side < 0 else 2))
        sy = body_bot + leg_h

        if side < 0:
            sx = cx - 2 - leg_w // 2
        else:
            sx = cx + 2 + leg_w // 2

        draw.ellipse([sx - shoe_w + 2, sy + shoe_h - 3,
                      sx + shoe_w - 2, sy + shoe_h + 6],
                     fill=SHOE_SOLE)
        draw.ellipse([sx - shoe_w + 4, sy - 2,
                      sx + shoe_w - 4, sy + shoe_h],
                     fill=SHOE)
        draw.ellipse([sx - shoe_w + 4, sy - 2,
                      sx + shoe_w - 4, sy + shoe_h],
                     outline=LINE, width=2)

    # --- Shirt body (striped) ---
    # Horizontal stripes
    for i in range(int(body_h / 9)):
        sy = body_top + i * 9
        sh = min(4, body_bot - sy)
        col = STRIPE_A if i % 2 == 0 else STRIPE_B
        # Trapezoid-ish: shirt is tucked in, no A-line
        draw.rectangle([cx - body_w // 2, sy, cx + body_w // 2, sy + sh], fill=col)

    # Shirt outline
    draw.rectangle([cx - body_w // 2, body_top, cx + body_w // 2, body_bot],
                   outline=LINE, width=2)

    # Belt (thin, espresso)
    belt_y = body_bot - 10
    draw.rectangle([cx - body_w // 2 + 2, belt_y,
                    cx + body_w // 2 - 2, belt_y + 5],
                   fill=GLASS_FR)
    # Belt buckle
    draw.rectangle([cx - 5, belt_y - 1, cx + 5, belt_y + 6],
                   fill=GLASS_FR, outline=LINE, width=1)

    # --- Notebook (under left arm — mandatory) ---
    nb_x0 = cx - body_w // 2 - 22
    nb_y0 = cy + 4
    nb_x1 = nb_x0 + 16
    nb_y1 = nb_y0 + 44
    draw.rectangle([nb_x0, nb_y0, nb_x1, nb_y1], fill=NOTEBOOK)
    draw.line([nb_x0 + 3, nb_y0, nb_x0 + 3, nb_y1], fill=NOTEBK_SP, width=3)
    draw.rectangle([nb_x0, nb_y0, nb_x1, nb_y1], outline=LINE, width=2)

    # --- Arms ---
    arm_w = 14
    arm_h = 50
    # Left arm (holds notebook)
    draw.rectangle([cx - body_w // 2 - arm_w + 2, body_top + 6,
                    cx - body_w // 2 + 2, body_top + 6 + arm_h],
                   fill=STRIPE_A, outline=LINE, width=2)
    # Right arm
    draw.rectangle([cx + body_w // 2 - 2, body_top + 6,
                    cx + body_w // 2 + arm_w - 2, body_top + 6 + arm_h],
                   fill=STRIPE_B, outline=LINE, width=2)
    # Hands
    hand_r = 9
    for side in [-1, 1]:
        hx = cx + side * (body_w // 2 + arm_w // 2 - (2 if side < 0 else 2))
        hy = body_top + 6 + arm_h
        draw.ellipse([hx - hand_r, hy - hand_r, hx + hand_r, hy + hand_r],
                     fill=SKIN, outline=LINE, width=2)

    # --- Head ---
    hx0 = cx - head_r_x
    hy0 = cy - head_r_y * 2 - 6
    hx1 = cx + head_r_x
    hy1 = cy - 6
    draw.ellipse([hx0, hy0, hx1, hy1], fill=SKIN)

    # --- Hair (side part, cowlick) ---
    hair_top = hy0 - 8
    hair_bot = hy0 + int(head_r_y * 0.55)
    draw.ellipse([cx - head_r_x - 3, hair_top,
                  cx + int(head_r_x * 0.25), hair_bot + 4], fill=HAIR)
    draw.ellipse([cx - int(head_r_x * 0.25), hair_top + 2,
                  cx + head_r_x + 3, hair_bot + 2], fill=HAIR)
    # Part
    draw.line([cx + int(head_r_x * 0.15), hair_top + 4,
               cx + int(head_r_x * 0.15), hair_bot],
              fill=SKIN, width=2)

    # Head outline
    draw.ellipse([hx0, hy0, hx1, hy1], outline=LINE, width=3)

    # --- Glasses (always tilted 7°, always present) ---
    face_cy = hy0 + int(head_r_y * 0.92)
    gcy     = face_cy - int(head_r_y * 0.10)
    lens_r  = 15
    frame_w = 4
    bridge  = lens_r
    theta   = math.radians(-7)
    cos_t   = math.cos(theta)
    sin_t   = math.sin(theta)

    def rot(dx, dy):
        return (int(cx + dx * cos_t - dy * sin_t),
                int(gcy + dx * sin_t + dy * cos_t))

    lcx_g, lcy_g = rot(-bridge - lens_r, 0)
    rcx_g, rcy_g = rot(+bridge + lens_r, 0)

    for (ex, ey) in [(lcx_g, lcy_g), (rcx_g, rcy_g)]:
        draw.ellipse([ex - lens_r, ey - lens_r, ex + lens_r, ey + lens_r],
                     fill=GLASS_LN)
        # Glare crescent
        draw.arc([ex - int(lens_r * 0.7), ey - lens_r + 2,
                  ex + int(lens_r * 0.7), ey - lens_r + int(lens_r * 0.5)],
                 start=200, end=340, fill=GLASS_GL, width=2)
        draw.ellipse([ex - lens_r, ey - lens_r, ex + lens_r, ey + lens_r],
                     outline=GLASS_FR, width=frame_w)

    # Bridge
    bl = rot(-bridge, 0)
    br = rot(+bridge, 0)
    draw.line([bl, br], fill=GLASS_FR, width=frame_w)

    # Eyes (inside glasses)
    for (ex, ey) in [(lcx_g, lcy_g), (rcx_g, rcy_g)]:
        iris_r = int(lens_r * 0.55)
        pup_r  = int(iris_r * 0.55)
        draw.ellipse([ex - iris_r, ey - iris_r, ex + iris_r, ey + iris_r],
                     fill=EYE_W)
        draw.ellipse([ex - int(iris_r * 0.7), ey - int(iris_r * 0.7),
                      ex + int(iris_r * 0.7), ey + int(iris_r * 0.7)],
                     fill=IRIS)
        draw.ellipse([ex - pup_r, ey - pup_r, ex + pup_r, ey + pup_r],
                     fill=PUPIL)
        # Highlight (upper-right — intentional Cosmo DNA)
        draw.ellipse([ex + int(iris_r * 0.3), ey - iris_r + 2,
                      ex + int(iris_r * 0.3) + 4, ey - iris_r + 6],
                     fill=EYE_HL)

    # Nose
    nose_cx = cx + 1
    draw.arc([nose_cx - 5, face_cy + 4, nose_cx + 5, face_cy + 14],
             start=0, end=180, fill=SKIN_SH, width=2)

    # Mouth
    draw.arc([cx - 10, face_cy + 14, cx + 10, face_cy + 26],
             start=10, end=170, fill=LINE, width=2)

    # Brows
    for side in [-1, 1]:
        bx = cx + side * int(head_r_x * 0.55)
        by = gcy - lens_r - 7
        draw.arc([bx - 12, by - 3, bx + 12, by + 5],
                 start=200 if side < 0 else 340,
                 end=340 if side < 0 else 200,
                 fill=HAIR, width=2)


def build_color_model():
    img  = Image.new("RGB", (CANVAS_W, CANVAS_H), CANVAS_BG)
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
    draw.rectangle([0, 0, CANVAS_W, HEADER_H], fill=(10, 8, 6))
    title = "COSMO — Color Model v001  |  Cycle 25  |  CERULEAN #5B8DB8 / SAGE #7A9E7E"
    try:
        tb = draw.textbbox((0, 0), title, font=font_h)
        tw = tb[2] - tb[0]; th = tb[3] - tb[1]
    except Exception:
        tw, th = 400, 20
    draw.text(((CANVAS_W - tw) // 2, (HEADER_H - th) // 2),
              title, fill=LABEL_COL, font=font_h)

    # Character silhouette (left half)
    char_area_w = CANVAS_W // 2
    draw.rectangle([0, HEADER_H, char_area_w, CANVAS_H], fill=(20, 18, 14))
    char_cx = char_area_w // 2
    char_cy = HEADER_H + (CANVAS_H - HEADER_H) // 2 + 18
    draw_character_silhouette(draw, char_cx, char_cy)
    draw = ImageDraw.Draw(img)  # refresh after any paste

    # Character label
    char_label = "COSMO  (NEUTRAL)"
    try:
        clb = draw.textbbox((0, 0), char_label, font=font_sw)
        clw = clb[2] - clb[0]
        draw.text(((char_area_w - clw) // 2, CANVAS_H - 24),
                  char_label, fill=(100, 140, 160), font=font_sw)
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
                       outline=(40, 35, 25), width=1)
        draw.text((sw_x0 + label_x_off, sy + 2),
                  hexval, fill=(150, 180, 190), font=font_sw)
        draw.text((sw_x0 + label_x_off, sy + 12),
                  label, fill=(220, 215, 205), font=font_sw)
        draw.text((sw_x0 + label_x_off + 180, sy + 12),
                  role, fill=(100, 110, 100), font=font_sm)

    # Divider
    draw.line([(char_area_w, HEADER_H), (char_area_w, CANVAS_H)],
              fill=(40, 35, 25), width=1)

    return img


def main():
    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "characters", "color_models"
    )
    os.makedirs(out_dir, exist_ok=True)

    model = build_color_model()
    out_path = os.path.join(out_dir, "LTG_COLOR_cosmo_color_model_v001.png")
    model.save(out_path)
    print(f"Saved: {out_path}")
    print(f"  Size: {model.size[0]}x{model.size[1]}px")
    print("  Swatches: 14 canonical colors documented")
    print("  Primary: CERULEAN #5B8DB8 / SAGE #7A9E7E stripes")


if __name__ == "__main__":
    main()
