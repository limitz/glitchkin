#!/usr/bin/env python3
"""
LTG_COLOR_byte_color_model_v001.py
Byte — Color Model v001
"Luma & the Glitchkin" — Cycle 25 / Maya Santos

Format matches LTG_COLOR_glitch_color_model_v001.py:
  800×500px — character color story document.
  Left half: character front silhouette in color (simplified)
  Right half: labeled swatches for each palette value

CRITICAL: Byte body = GL-01b (#00D4E8 BYTE_TEAL) — NOT #00F0FF Electric Cyan.
Highlight/pixel displays = #00F0FF. Body fill = #00D4E8.

All palette values from canonical source: byte_color_model.md

Output: output/characters/color_models/LTG_COLOR_byte_color_model_v001.png
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# ── Canonical Palette ─────────────────────────────────────────────────────────
SWATCHES = [
    ("#00D4E8", (  0, 212, 232), "BYTE_TEAL — GL-01b body fill",       "Body core + limbs"),
    ("#00A8B5", (  0, 168, 181), "DEEP_CYAN — shadow",                 "Underside of body + limbs"),
    ("#00F0FF", (  0, 240, 255), "ELECTRIC_CYAN — GL-01 highlight",    "Top face / pixel displays"),
    ("#0A0A14", ( 10,  10,  20), "VOID_BLACK — GL-01 LINE",            "Outline / interior void"),
    ("#1A3A40", ( 26,  58,  64), "EYE BEZEL — deep cyan-gray",         "Eye frame border"),
    ("#FF2D6B", (255,  45, 107), "HOT_MAGENTA — GL-04 scar",           "Glitch scar / crack line"),
    ("#C4235A", (196,  35,  90), "SCAR_SCATTER — 70% mag equiv.",      "Secondary scar patches"),
    ("#E8F8FF", (232, 248, 255), "EYE WHITE — blue-tinted",            "Normal eye white (digital)"),
    ("#7B2FBE", (123,  47, 190), "UV_PURPLE — GL-05 pixel symbol",     "Heart symbol (accidental affection)"),
    ("#39FF14", ( 57, 255,  20), "ACID_GREEN — GL-03 pixel symbol",    "Warning triangle (alarmed)"),
    ("#E8C95A", (232, 201,  90), "SOFT_GOLD — RW-02 pixel symbol",     "Star symbol (pleased/smug)"),
    ("#FF2D6B", (255,  45, 107), "HOT_MAG — pixel exclamation",        "Angry / irritated state"),
    ("#007878", (  0, 120, 120), "DARK_CYAN — pixel down-arrow",       "Sad / glum state"),
    ("#AAAAAA", (170, 170, 170), "STATIC_GRAY — pixel flat line",      "Content / neutral resting"),
]

CANVAS_W  = 800
CANVAS_H  = 500
CANVAS_BG = (8, 10, 18)
HEADER_H  = 52
LABEL_COL = (0, 212, 232)   # Byte Teal for header accent

# Character silhouette colors
BODY       = (  0, 212, 232)   # BYTE_TEAL — body fill
BODY_SH    = (  0, 168, 181)   # shadow
BODY_HL    = (  0, 240, 255)   # highlight (Electric Cyan)
VOID_BK    = ( 10,  10,  20)
EYE_BZ     = ( 26,  58,  64)
SCAR_MAG   = (255,  45, 107)
UV_PUR     = (123,  47, 190)
ACID_GR    = ( 57, 255,  20)
EYE_W_DIG  = (232, 248, 255)   # blue-tinted white


def draw_pixel_eye_3x3(draw, ex, ey, cell, grid, col_map):
    for row in range(3):
        for col in range(3):
            c = col_map[grid[row][col]]
            draw.rectangle([ex + col*cell, ey + row*cell,
                             ex + col*cell + cell - 1, ey + row*cell + cell - 1],
                            fill=c)


def draw_character_silhouette(draw, cx, cy):
    """Simplified Byte front view for color model reference."""
    # Byte is an asymmetric oval body with limbs + spike + cracked eye
    body_rx = 44
    body_ry = 52
    body_top = cy - body_ry
    body_bot = cy + body_ry

    # Shadow ellipse (offset down-right)
    draw.ellipse([cx - body_rx + 5, cy - body_ry + 6,
                  cx + body_rx + 5, cy + body_ry + 6], fill=BODY_SH)

    # Body fill
    draw.ellipse([cx - body_rx, cy - body_ry, cx + body_rx, cy + body_ry],
                 fill=BODY)

    # Top highlight facet
    draw.ellipse([cx - body_rx + 8, cy - body_ry,
                  cx + body_rx - 8, cy - body_ry + int(body_ry * 0.4)],
                 fill=BODY_HL)

    # Body outline
    draw.ellipse([cx - body_rx, cy - body_ry, cx + body_rx, cy + body_ry],
                 outline=VOID_BK, width=3)

    # Notches (interior void — upper right corner)
    notch1 = [cx + body_rx - 22, cy - body_ry + 4,
               cx + body_rx - 2,  cy - body_ry + 22]
    notch2 = [cx + body_rx - 12, cy - body_ry + 18,
               cx + body_rx + 2,  cy - body_ry + 36]
    draw.chord(notch1, start=0, end=360, fill=VOID_BK)
    draw.chord(notch2, start=0, end=360, fill=VOID_BK)

    # Top spike (offset toward right/damaged side)
    spike_x = cx + int(body_rx * 0.2)
    spike_top = body_top - 28
    spike_pts = [
        (spike_x - 7, body_top - 4),
        (spike_x - 4, spike_top),
        (spike_x + 4, spike_top),
        (spike_x + 7, body_top - 4),
    ]
    draw.polygon(spike_pts, fill=BODY)
    draw.polygon(spike_pts, outline=VOID_BK, width=2)

    # Glitch scar (diagonal across front — upper-right to lower-left)
    draw.line([(cx + body_rx - 12, cy - body_ry + 10),
               (cx - body_rx + 8, cy + body_ry - 12)],
              fill=SCAR_MAG, width=3)
    # Secondary scatter
    draw.rectangle([cx + 8, cy - 22, cx + 14, cy - 18], fill=(196, 35, 90))
    draw.rectangle([cx - 4, cy + 8,  cx + 2,  cy + 12],  fill=(196, 35, 90))

    # Limbs (four rounded rectangles)
    limb_w = 14
    limb_h = 38
    # Top-left
    draw.rounded_rectangle([cx - body_rx - limb_w + 4, cy - limb_h // 2 - 10,
                             cx - body_rx + 4, cy + limb_h // 2 - 10],
                            radius=5, fill=BODY, outline=VOID_BK, width=2)
    # Bottom-left
    draw.rounded_rectangle([cx - body_rx - limb_w + 4, cy + body_ry - 8,
                             cx - body_rx + 4, cy + body_ry + limb_h - 8],
                            radius=5, fill=BODY, outline=VOID_BK, width=2)
    # Top-right
    draw.rounded_rectangle([cx + body_rx - 4, cy - limb_h // 2 - 10,
                             cx + body_rx + limb_w - 4, cy + limb_h // 2 - 10],
                            radius=5, fill=BODY, outline=VOID_BK, width=2)
    # Bottom-right
    draw.rounded_rectangle([cx + body_rx - 4, cy + body_ry - 8,
                             cx + body_rx + limb_w - 4, cy + body_ry + limb_h - 8],
                            radius=5, fill=BODY, outline=VOID_BK, width=2)

    # Hover confetti (below body)
    import random
    rng = random.Random(42)
    conf_cols = [SCAR_MAG, UV_PUR, BODY_HL]
    for _ in range(10):
        px = rng.randint(cx - 30, cx + 30)
        py = rng.randint(cy + body_ry + 6, cy + body_ry + 20)
        sz = rng.choice([2, 3])
        c  = rng.choice(conf_cols)
        draw.rectangle([px, py, px + sz, py + sz], fill=c)

    # Eyes (3x3 pixel grid)
    cell = 8
    # Left eye (normal — 3x3 active display)
    NEUTRAL_L = [[0, 2, 0], [2, 1, 2], [0, 2, 0]]
    PCOLS = {0: VOID_BK, 1: EYE_BZ, 2: BODY_HL}
    leye_x = cx - 32
    leye_y = cy - cell * 3 // 2
    # Eye bezel background
    draw.rectangle([leye_x - 3, leye_y - 3,
                    leye_x + cell * 3 + 2, leye_y + cell * 3 + 2],
                   fill=EYE_BZ)
    draw_pixel_eye_3x3(draw, leye_x, leye_y, cell, NEUTRAL_L, PCOLS)

    # Right eye (cracked — destabilized pixel display)
    DESTAB = [[1, 2, 0], [2, 0, 1], [0, 2, 1]]
    reye_x = cx + 8
    reye_y = cy - cell * 3 // 2
    # Cracked eye bezel (irregular)
    draw.rectangle([reye_x - 3, reye_y - 3,
                    reye_x + cell * 3 + 2, reye_y + cell * 3 + 2],
                   fill=EYE_BZ)
    draw_pixel_eye_3x3(draw, reye_x, reye_y, cell, DESTAB, PCOLS)
    # Crack overlay (void black line)
    draw.line([(reye_x + cell * 3 - 4, reye_y),
               (reye_x + 2, reye_y + cell * 3 - 2)],
              fill=VOID_BK, width=2)
    # Hot Mag crack on body exterior (scar continues through eye bezel edge)
    draw.line([(reye_x + cell * 3 + 2, reye_y + 2),
               (reye_x - 3, reye_y + cell - 1)],
              fill=SCAR_MAG, width=1)


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
    draw.rectangle([0, 0, CANVAS_W, HEADER_H], fill=(4, 8, 16))
    title = "BYTE — Color Model v001  |  Cycle 25  |  GL-01b BYTE_TEAL #00D4E8 BODY"
    try:
        tb = draw.textbbox((0, 0), title, font=font_h)
        tw = tb[2] - tb[0]; th = tb[3] - tb[1]
    except Exception:
        tw, th = 400, 20
    draw.text(((CANVAS_W - tw) // 2, (HEADER_H - th) // 2),
              title, fill=LABEL_COL, font=font_h)

    # Character silhouette (left half)
    char_area_w = CANVAS_W // 2
    draw.rectangle([0, HEADER_H, char_area_w, CANVAS_H], fill=(10, 14, 22))
    char_cx = char_area_w // 2
    char_cy = HEADER_H + (CANVAS_H - HEADER_H) // 2 + 10
    draw_character_silhouette(draw, char_cx, char_cy)
    draw = ImageDraw.Draw(img)  # refresh after any paste

    # Character label
    char_label = "BYTE  (NEUTRAL)"
    try:
        clb = draw.textbbox((0, 0), char_label, font=font_sw)
        clw = clb[2] - clb[0]
        draw.text(((char_area_w - clw) // 2, CANVAS_H - 24),
                  char_label, fill=(0, 180, 200), font=font_sw)
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
                       outline=(30, 50, 60), width=1)
        draw.text((sw_x0 + label_x_off, sy + 2),
                  hexval, fill=(120, 220, 240), font=font_sw)
        draw.text((sw_x0 + label_x_off, sy + 12),
                  label, fill=(220, 225, 230), font=font_sw)
        draw.text((sw_x0 + label_x_off + 190, sy + 12),
                  role, fill=(100, 120, 130), font=font_sm)

    # Divider
    draw.line([(char_area_w, HEADER_H), (char_area_w, CANVAS_H)],
              fill=(20, 40, 50), width=1)

    return img


def main():
    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "characters", "color_models"
    )
    os.makedirs(out_dir, exist_ok=True)

    model = build_color_model()
    out_path = os.path.join(out_dir, "LTG_COLOR_byte_color_model_v001.png")
    model.save(out_path)
    print(f"Saved: {out_path}")
    print(f"  Size: {model.size[0]}x{model.size[1]}px")
    print("  Swatches: 14 canonical colors documented")
    print("  CRITICAL: Body fill = #00D4E8 BYTE_TEAL (GL-01b) — NOT #00F0FF")


if __name__ == "__main__":
    main()
