#!/usr/bin/env python3
"""
LTG_COLOR_styleframe_luma_byte_v001.py
Style Frame 04 — "The Dynamic" — Luma + Byte Interaction
"Luma & the Glitchkin" — Cycle 25

Art Director: Alex Chen
Date: 2026-03-29
Cycle: 25

Design brief:
  This frame exists to answer the single biggest critique gap from C11:
  "No asset shows Luma and Byte in the same frame at readable scale
   with their emotional dynamic legible."

  Scene: Luma and Byte are in her bedroom at dusk. Byte sits on her
  right shoulder. Luma is leaning slightly forward — CURIOUS expression,
  looking at something off-screen right (the TV / a glitch signal).
  Byte is looking the OPPOSITE direction — up at Luma's face — with a
  WORRIED/skeptical expression. He clearly disapproves of whatever she's
  about to do. She clearly hasn't noticed his protest.

  This is the show's core dynamic in one frame:
    - Luma: warm, forward-leaning, reckless optimism
    - Byte: cool, guarded, secretly watching out for her
  They share space. They do not yet share attention. The comedy and
  tenderness both live in that gap.

  Lighting: Warm window light from the left (RW-03 Sunlit Amber).
  Cool monitor/Glitch Layer ambient from right (GL-01b Elec Cyan).
  Byte subtly glows with his own inner cyan — he is his own light source.

Format: 1920x1080 (matches SF01–03)
Output: output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v001.png
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v001.png"
W, H = 1920, 1080

# ── Master Palette ────────────────────────────────────────────────────────────
WARM_CREAM      = (250, 240, 220)
SOFT_GOLD       = (232, 201,  90)
SUNLIT_AMBER    = (212, 146,  58)
TERRACOTTA      = (199,  91,  57)
RUST_SHADOW     = (140,  58,  34)
SAGE_GREEN      = (122, 158, 126)
DUSTY_LAVENDER  = (168, 155, 191)
SHADOW_PLUM     = ( 92,  74, 114)
WARM_TAN        = (196, 168, 130)
SKIN_SHADOW     = (140,  90,  56)
DEEP_COCOA      = ( 59,  40,  32)
OCHRE_BRICK     = (184, 148,  74)
ELEC_CYAN       = (  0, 240, 255)
BYTE_TEAL       = (  0, 212, 232)
DEEP_CYAN       = (  0, 168, 180)
HOT_MAGENTA     = (255,  45, 107)
UV_PURPLE       = (123,  47, 190)
VOID_BLACK      = ( 10,  10,  20)
STATIC_WHITE    = (240, 240, 240)

# Character colors — Luma
SKIN            = (200, 136,  90)
SKIN_HL         = (223, 160, 112)
SKIN_SH         = (160, 104,  64)
HAIR            = ( 26,  15,  10)
HAIR_HL         = ( 61,  31,  15)
EYE_W           = (250, 240, 220)
EYE_IRIS        = (200, 125,  62)
EYE_PUP         = ( 59,  40,  32)
HOODIE_ORANGE   = (232, 112,  58)
HOODIE_SH       = (184,  74,  32)
HOODIE_AMBIENT  = (179,  98,  80)
JEANS           = ( 58,  90, 140)
JEANS_SH        = ( 38,  62, 104)

# Character colors — Byte
BYTE_FILL       = (  0, 190, 210)
BYTE_SH         = (  0, 110, 140)
BYTE_HL         = (  0, 240, 255)
BYTE_DARK_SH    = (  0,  60,  90)
SCAR_MAG        = (255,  45, 107)
PIXEL_EYE       = (  0, 240, 255)

LINE            = ( 59,  40,  32)


def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def draw_glow_ellipse(draw, cx, cy, rx, ry, color_rgb, steps=12):
    """Draw a soft radial glow using concentric ellipses."""
    for i in range(steps, 0, -1):
        t = i / steps
        alpha_val = int(50 * (1 - t))
        er = max(1, int(rx * t))
        ery = max(1, int(ry * t))
        # Blend toward void black
        r_v = int(VOID_BLACK[0] + (color_rgb[0] - VOID_BLACK[0]) * (1 - t))
        g_v = int(VOID_BLACK[1] + (color_rgb[1] - VOID_BLACK[1]) * (1 - t))
        b_v = int(VOID_BLACK[2] + (color_rgb[2] - VOID_BLACK[2]) * (1 - t))
        draw.ellipse([cx - er, cy - ery, cx + er, cy + ery],
                     fill=(r_v, g_v, b_v))


def draw_background(draw, img):
    """Draw the bedroom background with dual warm/cool lighting."""
    rng = random.Random(77)

    # Sky / window light zone — upper left warm
    for y in range(H):
        t = y / H
        # Base: warm amber gradient from top to bottom
        base_r = int(SUNLIT_AMBER[0] * 0.32 + 10)
        base_g = int(SUNLIT_AMBER[1] * 0.22 + 8)
        base_b = int(SUNLIT_AMBER[2] * 0.14 + 5)
        # Darken as we go down
        r_v = max(8, int(base_r * (1.0 - t * 0.6)))
        g_v = max(6, int(base_g * (1.0 - t * 0.6)))
        b_v = max(4, int(base_b * (1.0 - t * 0.5)))
        draw.line([(0, y), (W, y)], fill=(r_v, g_v, b_v))

    # Warm wall — upper portion
    wall_color = (168, 118, 60)
    for y in range(0, int(H * 0.55)):
        t = y / (H * 0.55)
        r_v = int(wall_color[0] * (1.0 - t * 0.25))
        g_v = int(wall_color[1] * (1.0 - t * 0.3))
        b_v = int(wall_color[2] * (1.0 - t * 0.35))
        draw.line([(0, y), (W, y)], fill=(r_v, g_v, b_v))

    # Floor — wooden planks
    floor_y = int(H * 0.72)
    floor_color = (120, 75, 30)
    draw.rectangle([0, floor_y, W, H], fill=floor_color)
    for y in range(floor_y, H, 32):
        draw.line([(0, y), (W, y)], fill=RUST_SHADOW, width=1)
    for y in range(floor_y + 4, H, 64):
        draw.line([(0, y), (W, y)], fill=(95, 56, 22), width=1)

    # Baseboard
    draw.rectangle([0, floor_y - 16, W, floor_y], fill=(90, 55, 20))
    draw.line([(0, floor_y - 16), (W, floor_y - 16)], fill=DEEP_COCOA, width=2)

    # Window — left side, large, golden afternoon light
    win_x0, win_y0 = 80, 55
    win_x1, win_y1 = 380, 520
    # Window frame (wooden — warm brown)
    frame_color = (160, 100, 40)
    draw.rectangle([win_x0 - 24, win_y0 - 14, win_x1 + 24, win_y1 + 14],
                   fill=frame_color)
    # Window pane — bright golden light
    draw.rectangle([win_x0, win_y0, win_x1, win_y1], fill=SOFT_GOLD)
    # Light gradient inside window (brighter center)
    for step in range(12, 0, -1):
        t = step / 12.0
        wc_x = (win_x0 + win_x1) // 2
        wc_y = (win_y0 + win_y1) // 2
        er = int((win_x1 - win_x0) * 0.5 * t)
        ery = int((win_y1 - win_y0) * 0.5 * t)
        r_v = int(SOFT_GOLD[0] + (250 - SOFT_GOLD[0]) * (1 - t))
        g_v = int(SOFT_GOLD[1] + (240 - SOFT_GOLD[1]) * (1 - t))
        b_v = int(SOFT_GOLD[2] + (180 - SOFT_GOLD[2]) * (1 - t))
        draw.ellipse([wc_x - er, wc_y - ery, wc_x + er, wc_y + ery],
                     fill=(r_v, g_v, b_v))
    # Window frame crossbars
    draw.line([(win_x0, (win_y0 + win_y1) // 2), (win_x1, (win_y0 + win_y1) // 2)],
              fill=frame_color, width=10)
    draw.line([((win_x0 + win_x1) // 2, win_y0), ((win_x0 + win_x1) // 2, win_y1)],
              fill=frame_color, width=10)
    draw.rectangle([win_x0, win_y0, win_x1, win_y1], outline=DEEP_COCOA, width=4)

    # Window light shaft on floor (warm trapezoid)
    shaft_pts = [
        (win_x0 + 20, win_y1),
        (win_x1 - 20, win_y1),
        (win_x1 + 80, floor_y),
        (win_x0 - 40, floor_y),
    ]
    shaft_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shaft_draw = ImageDraw.Draw(shaft_layer)
    shaft_draw.polygon(shaft_pts, fill=(*SUNLIT_AMBER, 55))
    base_rgba = img.convert("RGBA")
    img.paste(Image.alpha_composite(base_rgba, shaft_layer).convert("RGB"))

    # Desk — right side, partial
    desk_x = int(W * 0.74)
    desk_y = int(H * 0.56)
    desk_w = int(W * 0.26)
    desk_h = int(H * 0.08)
    desk_color = (145, 90, 35)
    draw.rectangle([desk_x, desk_y, desk_x + desk_w, desk_y + desk_h],
                   fill=desk_color)
    draw.rectangle([desk_x, desk_y - 6, desk_x + desk_w, desk_y],
                   fill=(165, 110, 50))
    draw.line([(desk_x, desk_y), (desk_x + desk_w, desk_y)], fill=DEEP_COCOA, width=2)

    # Small CRT monitor on desk — source of cyan light from right
    crt_x = int(W * 0.78)
    crt_y = int(H * 0.32)
    crt_w = int(W * 0.18)
    crt_h = int(H * 0.22)
    # CRT body
    draw.rectangle([crt_x - 14, crt_y - 14, crt_x + crt_w + 14, crt_y + crt_h + 26],
                   fill=(40, 34, 52), outline=(28, 22, 40), width=3)
    draw.rectangle([crt_x + crt_w // 3, crt_y + crt_h + 22,
                    crt_x + crt_w * 2 // 3, crt_y + crt_h + 44],
                   fill=(32, 26, 42))
    # CRT screen — electric cyan glow
    scr_pad = 18
    scr_x0 = crt_x + scr_pad
    scr_y0 = crt_y + scr_pad
    scr_x1 = crt_x + crt_w - scr_pad
    scr_y1 = crt_y + crt_h - scr_pad
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1], fill=ELEC_CYAN)
    # Scanlines
    for sy in range(scr_y0 + 3, scr_y1, 5):
        draw.line([(scr_x0, sy), (scr_x1, sy)], fill=DEEP_CYAN, width=1)
    # Static/noise on screen
    scr_rng = random.Random(12)
    for _ in range(18):
        px_x = scr_x0 + scr_rng.randint(4, scr_x1 - scr_x0 - 4)
        px_y = scr_y0 + scr_rng.randint(4, scr_y1 - scr_y0 - 4)
        ps = scr_rng.choice([2, 3, 4])
        pc = scr_rng.choice([(0, 80, 100), (0, 140, 160), STATIC_WHITE])
        draw.rectangle([px_x, px_y, px_x + ps, px_y + ps], fill=pc)
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1], outline=DEEP_CYAN, width=3)

    # Cyan light spill from monitor onto wall and desk
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    # Wall glow behind monitor
    for step in range(16, 0, -1):
        t = step / 16.0
        er = int(crt_w * 1.8 * t)
        ery = int(crt_h * 1.6 * t)
        alpha = int(28 * (1 - t))
        glow_draw.ellipse([(crt_x + crt_w // 2) - er, (crt_y + crt_h // 2) - ery,
                           (crt_x + crt_w // 2) + er, (crt_y + crt_h // 2) + ery],
                          fill=(*ELEC_CYAN, alpha))
    base_rgba = img.convert("RGBA")
    img.paste(Image.alpha_composite(base_rgba, glow_layer).convert("RGB"))

    # Pixel confetti — Glitch Layer energy leaking
    confetti_rng = random.Random(55)
    confetti_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    confetti_draw = ImageDraw.Draw(confetti_layer)
    for _ in range(35):
        px = confetti_rng.randint(int(W * 0.5), W - 40)
        py = confetti_rng.randint(int(H * 0.15), int(H * 0.80))
        ps = confetti_rng.choice([2, 3, 4, 5, 6])
        pc = confetti_rng.choice([ELEC_CYAN, BYTE_TEAL, HOT_MAGENTA, STATIC_WHITE,
                                  (0, 200, 220), UV_PURPLE])
        alpha = confetti_rng.randint(80, 180)
        confetti_draw.rectangle([px, py, px + ps, py + ps], fill=(*pc, alpha))
    base_rgba = img.convert("RGBA")
    img.paste(Image.alpha_composite(base_rgba, confetti_layer).convert("RGB"))

    draw2 = ImageDraw.Draw(img)
    return draw2


def draw_luma(draw, img, cx, cy):
    """
    Draw Luma at mid-shot scale — head and upper body clearly visible.
    Luma is leaning slightly forward (CURIOUS expression — looking right).
    cx, cy = center of her torso mass.
    Her proportions: 3.5 heads. At this scale, head ~220px tall.

    She is positioned slightly left of center, facing toward screen-right.
    """
    rng = random.Random(11)

    # Scale: head height = 220px
    HU = 220  # one head unit

    # Body proportions
    head_r = int(HU * 0.50)          # head radius ~110px
    torso_h = int(HU * 1.0)          # torso height ~220px
    torso_w = int(HU * 0.58)         # torso width

    # Torso center — Luma's body leaning slightly forward
    lean_offset = 22  # pixels rightward lean (forward lean toward screen-right)
    torso_cx = cx + lean_offset
    torso_cy = cy

    # Head sits above torso, minimal neck
    neck_gap = int(HU * 0.05)
    head_cx = torso_cx - 8   # head slightly to left of torso center (3/4 view)
    head_cy = torso_cy - torso_h // 2 - neck_gap - head_r

    # Determine screen-right-facing: Luma looks right, so face details are
    # shifted slightly right on the head

    # ── Jeans / lower body ────────────────────────────────────────────────
    leg_w = int(HU * 0.28)
    leg_h = int(HU * 0.80)
    leg_y0 = torso_cy + torso_h // 2
    # Left leg (viewer's left)
    draw.rounded_rectangle(
        [torso_cx - torso_w // 2 + 4, leg_y0,
         torso_cx - torso_w // 2 + 4 + leg_w, leg_y0 + leg_h],
        radius=18, fill=JEANS, outline=LINE, width=3)
    # Right leg (viewer's right)
    draw.rounded_rectangle(
        [torso_cx + torso_w // 2 - 4 - leg_w, leg_y0,
         torso_cx + torso_w // 2 - 4, leg_y0 + leg_h],
        radius=18, fill=JEANS, outline=LINE, width=3)
    # Jeans shadow on inner legs
    draw.rounded_rectangle(
        [torso_cx - torso_w // 2 + 4, leg_y0,
         torso_cx - torso_w // 2 + 4 + leg_w - 6, leg_y0 + leg_h],
        radius=18, fill=JEANS_SH, outline=None)
    draw.rounded_rectangle(
        [torso_cx + torso_w // 2 - 4 - leg_w + 6, leg_y0,
         torso_cx + torso_w // 2 - 4, leg_y0 + leg_h],
        radius=18, fill=JEANS_SH, outline=None)

    # ── Hoodie — torso ────────────────────────────────────────────────────
    draw.rounded_rectangle(
        [torso_cx - torso_w // 2, torso_cy - torso_h // 2,
         torso_cx + torso_w // 2, torso_cy + torso_h // 2],
        radius=28, fill=HOODIE_ORANGE, outline=LINE, width=4)
    # Shadow (right/back side — cool ambient from monitor)
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.rounded_rectangle(
        [torso_cx + torso_w // 4, torso_cy - torso_h // 2,
         torso_cx + torso_w // 2, torso_cy + torso_h // 2],
        radius=28, fill=(*HOODIE_AMBIENT, 140))
    base_rgba = img.convert("RGBA")
    img.paste(Image.alpha_composite(base_rgba, shadow_layer).convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Pixel pattern on hoodie (3x3 grid of small squares — Luma's signature)
    pixel_size = 8
    pixel_gap = 14
    px_grid_x = torso_cx - 18
    px_grid_y = torso_cy - 30
    for row in range(3):
        for col in range(3):
            px_x = px_grid_x + col * (pixel_size + pixel_gap)
            px_y = px_grid_y + row * (pixel_size + pixel_gap)
            # Alternate: most gold, one cyan (Glitch Layer contamination)
            if (row == 1 and col == 1):
                pc = ELEC_CYAN
            else:
                pc = SOFT_GOLD
            draw.rectangle([px_x, px_y, px_x + pixel_size, px_y + pixel_size], fill=pc)

    # Hoodie kangaroo pocket
    pocket_y = torso_cy + int(torso_h * 0.2)
    draw.rounded_rectangle(
        [torso_cx - torso_w // 2 + 12, pocket_y,
         torso_cx + torso_w // 2 - 12, torso_cy + torso_h // 2 - 10],
        radius=12, fill=HOODIE_SH, outline=LINE, width=2)

    # ── Arms ──────────────────────────────────────────────────────────────
    arm_w = int(HU * 0.22)
    arm_h = int(HU * 0.85)

    # Left arm (viewer's left) — relaxed, slightly out from body
    la_x = torso_cx - torso_w // 2 - arm_w // 2 + 6
    la_y = torso_cy - torso_h // 2 + int(HU * 0.12)
    draw.rounded_rectangle(
        [la_x - arm_w // 2, la_y,
         la_x + arm_w // 2, la_y + arm_h],
        radius=16, fill=HOODIE_ORANGE, outline=LINE, width=3)

    # Right arm (viewer's right) — forward lean arm, slightly forward
    ra_x = torso_cx + torso_w // 2 + arm_w // 2 - 6
    ra_y = torso_cy - torso_h // 2 + int(HU * 0.08)
    draw.rounded_rectangle(
        [ra_x - arm_w // 2, ra_y,
         ra_x + arm_w // 2, ra_y + arm_h],
        radius=16, fill=HOODIE_ORANGE, outline=LINE, width=3)

    # ── Skin — neck ───────────────────────────────────────────────────────
    draw.ellipse(
        [head_cx - int(HU * 0.12), head_cy + head_r - 8,
         head_cx + int(HU * 0.12), head_cy + head_r + int(HU * 0.08)],
        fill=SKIN)

    # ── Head — base circle ───────────────────────────────────────────────
    draw.ellipse(
        [head_cx - head_r, head_cy - head_r,
         head_cx + head_r, head_cy + head_r],
        fill=SKIN, outline=LINE, width=4)
    # Cheek highlight (warm side — left/window side)
    draw.ellipse(
        [head_cx - head_r + 10, head_cy - int(head_r * 0.1),
         head_cx - head_r + 10 + int(head_r * 0.55),
         head_cy - int(head_r * 0.1) + int(head_r * 0.38)],
        fill=SKIN_HL)
    # Shadow side (right — cool monitor ambient)
    shadow_head_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(shadow_head_layer)
    sh_draw.ellipse(
        [head_cx, head_cy - head_r,
         head_cx + head_r, head_cy + head_r],
        fill=(*SKIN_SH, 120))
    base_rgba = img.convert("RGBA")
    img.paste(Image.alpha_composite(base_rgba, shadow_head_layer).convert("RGB"))
    draw = ImageDraw.Draw(img)
    # Redraw head outline over shadow
    draw.ellipse(
        [head_cx - head_r, head_cy - head_r,
         head_cx + head_r, head_cy + head_r],
        outline=LINE, width=4)

    # ── Blush ─────────────────────────────────────────────────────────────
    # CURIOUS expression — excited, forward-leaning, so blush is active
    blush_r = int(head_r * 0.22)
    blush_y = head_cy + int(head_r * 0.15)
    # Left cheek
    blush_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bl_draw = ImageDraw.Draw(blush_layer)
    bl_draw.ellipse(
        [head_cx - int(head_r * 0.68) - blush_r, blush_y - blush_r // 2,
         head_cx - int(head_r * 0.68) + blush_r * 2, blush_y + blush_r],
        fill=(220, 80, 50, 55))
    # Right cheek
    bl_draw.ellipse(
        [head_cx + int(head_r * 0.32) - blush_r, blush_y - blush_r // 2,
         head_cx + int(head_r * 0.32) + blush_r * 2, blush_y + blush_r],
        fill=(208, 72, 48, 55))
    base_rgba = img.convert("RGBA")
    img.paste(Image.alpha_composite(base_rgba, blush_layer).convert("RGB"))
    draw = ImageDraw.Draw(img)

    # ── Face features — CURIOUS expression (looking right) ───────────────
    # Face is 3/4 turned right. Features shifted right of center.
    face_shift = int(head_r * 0.10)  # features shift right

    # Eyes
    eye_y = head_cy + int(head_r * 0.05)
    eye_w = int(head_r * 0.36)
    eye_h = int(head_r * 0.32)
    # Curious expression: one brow raised (right), eyes wide, slight forward lean look
    # Left eye — slightly more open (curious)
    le_cx = head_cx - int(head_r * 0.28) + face_shift
    draw.rounded_rectangle(
        [le_cx - eye_w // 2, eye_y - eye_h // 2,
         le_cx + eye_w // 2, eye_y + eye_h // 2],
        radius=8, fill=EYE_W, outline=LINE, width=2)
    draw.ellipse(
        [le_cx - int(eye_w * 0.32), eye_y - int(eye_h * 0.35),
         le_cx + int(eye_w * 0.32), eye_y + int(eye_h * 0.35)],
        fill=EYE_IRIS)
    draw.ellipse(
        [le_cx - int(eye_w * 0.18), eye_y - int(eye_h * 0.22),
         le_cx + int(eye_w * 0.18), eye_y + int(eye_h * 0.22)],
        fill=EYE_PUP)
    draw.ellipse(
        [le_cx - int(eye_w * 0.14), eye_y - int(eye_h * 0.28),
         le_cx - int(eye_w * 0.06), eye_y - int(eye_h * 0.12)],
        fill=STATIC_WHITE)  # highlight

    # Right eye — slightly squinted (curious look into distance)
    re_cx = head_cx + int(head_r * 0.28) + face_shift
    re_h_open = int(eye_h * 0.85)  # slightly more squinted
    draw.rounded_rectangle(
        [re_cx - eye_w // 2, eye_y - re_h_open // 2,
         re_cx + eye_w // 2, eye_y + re_h_open // 2],
        radius=8, fill=EYE_W, outline=LINE, width=2)
    draw.ellipse(
        [re_cx - int(eye_w * 0.32), eye_y - int(re_h_open * 0.35),
         re_cx + int(eye_w * 0.32), eye_y + int(re_h_open * 0.35)],
        fill=EYE_IRIS)
    draw.ellipse(
        [re_cx - int(eye_w * 0.18), eye_y - int(re_h_open * 0.22),
         re_cx + int(eye_w * 0.18), eye_y + int(re_h_open * 0.22)],
        fill=EYE_PUP)
    draw.ellipse(
        [re_cx - int(eye_w * 0.14), eye_y - int(re_h_open * 0.28),
         re_cx - int(eye_w * 0.06), eye_y - int(re_h_open * 0.12)],
        fill=STATIC_WHITE)

    # Eyebrows — CURIOUS: left brow slightly raised + kinked, right brow higher still
    brow_y_l = eye_y - eye_h // 2 - int(head_r * 0.16)
    brow_y_r = eye_y - re_h_open // 2 - int(head_r * 0.22)  # raised (curious)
    brow_w = int(head_r * 0.38)
    brow_thickness = 6
    # Left brow — slight inward kink
    draw.line(
        [(le_cx - brow_w // 2, brow_y_l + 4),
         (le_cx, brow_y_l),
         (le_cx + brow_w // 2, brow_y_l + 2)],
        fill=LINE, width=brow_thickness)
    # Right brow — raised arch (more curious)
    draw.line(
        [(re_cx - brow_w // 2, brow_y_r + 6),
         (re_cx, brow_y_r),
         (re_cx + brow_w // 2, brow_y_r + 4)],
        fill=LINE, width=brow_thickness)

    # Nose — minimal apostrophe
    nose_x = head_cx + face_shift + int(head_r * 0.06)
    nose_y = head_cy + int(head_r * 0.28)
    draw.arc(
        [nose_x - 10, nose_y - 8, nose_x + 6, nose_y + 8],
        start=180, end=340, fill=LINE, width=3)

    # Mouth — CURIOUS: slightly open, one corner lifted (about to say something)
    mouth_y = head_cy + int(head_r * 0.50)
    mouth_w = int(head_r * 0.50)
    mouth_x = head_cx + face_shift - mouth_w // 2 + 4
    # Main curve — slight smile, open
    draw.arc(
        [mouth_x, mouth_y - 10, mouth_x + mouth_w, mouth_y + 20],
        start=10, end=170, fill=LINE, width=4)
    # Slight opening — tiny dark interior suggestion
    draw.ellipse(
        [mouth_x + mouth_w // 4, mouth_y - 2,
         mouth_x + mouth_w * 3 // 4, mouth_y + 12],
        fill=DEEP_COCOA)

    # ── Hair ──────────────────────────────────────────────────────────────
    # Massive dark curl cloud. Slightly more volume on left (viewer's left).
    # CURIOUS state: hair slightly excited — lifted, flyaways active.
    hair_cx = head_cx - 6
    hair_cy = head_cy - head_r + 8

    # Main hair mass — irregular cloud shape
    hair_mass_points = [
        (hair_cx - int(head_r * 1.10), hair_cy + int(head_r * 0.30)),   # left ear
        (hair_cx - int(head_r * 1.18), hair_cy - int(head_r * 0.15)),   # left mid
        (hair_cx - int(head_r * 0.90), hair_cy - int(head_r * 0.65)),   # upper left
        (hair_cx - int(head_r * 0.42), hair_cy - int(head_r * 1.05)),   # upper center-left
        (hair_cx + int(head_r * 0.08), hair_cy - int(head_r * 1.22)),   # crown center
        (hair_cx + int(head_r * 0.55), hair_cy - int(head_r * 1.08)),   # upper center-right
        (hair_cx + int(head_r * 0.92), hair_cy - int(head_r * 0.60)),   # upper right
        (hair_cx + int(head_r * 1.05), hair_cy + int(head_r * 0.05)),   # right
        (hair_cx + int(head_r * 0.85), hair_cy + int(head_r * 0.40)),   # lower right
        (hair_cx - int(head_r * 0.80), hair_cy + int(head_r * 0.55)),   # lower left
    ]
    draw.polygon(hair_mass_points, fill=HAIR, outline=LINE)

    # Hair highlight on crown
    draw.polygon([
        (hair_cx - int(head_r * 0.22), hair_cy - int(head_r * 1.18)),
        (hair_cx + int(head_r * 0.18), hair_cy - int(head_r * 1.22)),
        (hair_cx + int(head_r * 0.40), hair_cy - int(head_r * 0.90)),
        (hair_cx + int(head_r * 0.08), hair_cy - int(head_r * 0.88)),
        (hair_cx - int(head_r * 0.12), hair_cy - int(head_r * 0.90)),
    ], fill=HAIR_HL)

    # 5 locked curl indicators (internal structure lines)
    curls = [
        # (start_x, start_y, radius, start_angle, end_angle)
        (hair_cx - int(head_r * 0.70), hair_cy - int(head_r * 0.42), 28, 0, 280),
        (hair_cx - int(head_r * 0.30), hair_cy - int(head_r * 0.78), 24, 20, 310),
        (hair_cx + int(head_r * 0.15), hair_cy - int(head_r * 0.95), 22, 30, 300),
        (hair_cx + int(head_r * 0.55), hair_cy - int(head_r * 0.72), 26, 10, 290),
        (hair_cx - int(head_r * 0.90), hair_cy - int(head_r * 0.10), 20, 40, 320),
    ]
    for cx_c, cy_c, r_c, a0, a1 in curls:
        draw.arc(
            [cx_c - r_c, cy_c - r_c, cx_c + r_c, cy_c + r_c],
            start=a0, end=a1, fill=HAIR_HL, width=3)

    # Flyaway hairs — 4 wispy curves (CURIOUS state: slightly more flyaways)
    flyaway_rng = random.Random(77)
    for _ in range(4):
        fx = hair_cx + flyaway_rng.randint(-int(head_r * 0.8), int(head_r * 0.8))
        fy = hair_cy - int(head_r * 0.85) - flyaway_rng.randint(0, 20)
        fly_len = flyaway_rng.randint(18, 34)
        fly_dx = flyaway_rng.randint(-12, 12)
        draw.line([(fx, fy), (fx + fly_dx, fy - fly_len)], fill=HAIR_HL, width=2)

    # One escapee ringlet near right ear
    ring_cx = head_cx + int(head_r * 0.82)
    ring_cy = head_cy + int(head_r * 0.20)
    draw.arc([ring_cx - 14, ring_cy - 16, ring_cx + 14, ring_cy + 16],
             start=60, end=310, fill=HAIR, width=4)

    return draw, head_cx, head_cy, head_r, torso_cx, torso_cy


def draw_byte(draw, img, shoulder_cx, shoulder_cy):
    """
    Draw Byte perched on Luma's right shoulder, looking UP at her face.
    His expression: WORRIED / skeptical — he disapproves of what she's
    about to do. One eye slightly narrowed, pixel mouth frown.
    He's small — about 80px body oval width at this scale.
    """
    # Byte's body dimensions
    bw = 80   # body oval width
    bh = 68   # body oval height (wider than tall)
    bcx = shoulder_cx
    bcy = shoulder_cy - bh // 2 - 8  # sitting on shoulder with slight float

    # Byte glow — he is his own light source (subtle cyan aura)
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    for step in range(10, 0, -1):
        t = step / 10.0
        er = int(bw * 0.8 * t)
        ery = int(bh * 0.8 * t)
        alpha = int(38 * (1 - t))
        glow_draw.ellipse([bcx - er, bcy - ery, bcx + er, bcy + ery],
                          fill=(*BYTE_TEAL, alpha))
    base_rgba = img.convert("RGBA")
    img.paste(Image.alpha_composite(base_rgba, glow_layer).convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Pixel confetti beneath Byte (floating mechanism)
    confetti_rng = random.Random(33)
    for _ in range(12):
        px_x = bcx + confetti_rng.randint(-bw // 2, bw // 2)
        px_y = bcy + bh // 2 + confetti_rng.randint(2, 22)
        ps = confetti_rng.choice([2, 3, 4])
        pc = confetti_rng.choice([ELEC_CYAN, HOT_MAGENTA, BYTE_TEAL])
        alpha = confetti_rng.randint(80, 160)
        conf_l = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        conf_d = ImageDraw.Draw(conf_l)
        conf_d.rectangle([px_x, px_y, px_x + ps, px_y + ps], fill=(*pc, alpha))
        base_rgba = img.convert("RGBA")
        img.paste(Image.alpha_composite(base_rgba, conf_l).convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Byte's body oval — main fill (shadow side right, lit side left by window)
    draw.ellipse(
        [bcx - bw // 2, bcy - bh // 2, bcx + bw // 2, bcy + bh // 2],
        fill=BYTE_FILL, outline=LINE, width=3)
    # Shadow (right side — deeper)
    shadow_b_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sb_draw = ImageDraw.Draw(shadow_b_layer)
    sb_draw.ellipse(
        [bcx, bcy - bh // 2, bcx + bw // 2, bcy + bh // 2],
        fill=(*BYTE_SH, 180))
    base_rgba = img.convert("RGBA")
    img.paste(Image.alpha_composite(base_rgba, shadow_b_layer).convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Highlight (left side — window light)
    hl_b_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hb_draw = ImageDraw.Draw(hl_b_layer)
    hb_draw.ellipse(
        [bcx - bw // 2, bcy - bh // 2, bcx - bw // 8, bcy],
        fill=(*BYTE_HL, 90))
    base_rgba = img.convert("RGBA")
    img.paste(Image.alpha_composite(base_rgba, hl_b_layer).convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Glitch scar — Hot Magenta diagonal crack on right side
    scar_x1 = bcx + int(bw * 0.15)
    scar_y1 = bcy - int(bh * 0.30)
    scar_x2 = bcx + int(bw * 0.38)
    scar_y2 = bcy + int(bh * 0.32)
    draw.line([(scar_x1, scar_y1), (scar_x2, scar_y2)], fill=SCAR_MAG, width=3)
    # Crack branch
    draw.line([(scar_x1 + 8, scar_y1 + 16), (scar_x1 + 20, scar_y1 + 8)],
              fill=SCAR_MAG, width=2)

    # Byte is looking UP at Luma — so face tilted upward
    # Face occupies ~70% of oval. Eyes shifted upward.
    face_tilt_up = int(bh * 0.12)  # features shift up (looking up)

    # Pixel eyes — WORRIED expression
    # Left eye: small pixel square, slightly narrowed (worried)
    eye_size = 10
    eye_gap = int(bw * 0.22)
    eye_y = bcy - face_tilt_up - eye_size // 2

    # Byte looks up at Luma — both eyes tracking upward, slight left-turn
    # (he's on right shoulder looking left-and-up toward her face)
    eye_track_x = -int(bw * 0.05)  # slight left shift (eyes tracking toward her)
    eye_track_y = -int(bh * 0.08)   # upward shift

    le_x = bcx - eye_gap + eye_track_x
    re_x = bcx + eye_gap - eye_size + eye_track_x
    e_y = eye_y + eye_track_y

    # Left pixel eye — slightly narrowed (worried squint)
    draw.rectangle([le_x - eye_size // 2, e_y,
                    le_x + eye_size // 2, e_y + eye_size - 2],
                   fill=PIXEL_EYE)
    # Right pixel eye — normal height
    draw.rectangle([re_x - eye_size // 2, e_y - 1,
                    re_x + eye_size // 2, e_y + eye_size],
                   fill=PIXEL_EYE)

    # Eye glow (eyes are their own light source)
    for eye_cx, eye_cy in [(le_x, e_y + eye_size // 2), (re_x, e_y + eye_size // 2)]:
        eye_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        eg_draw = ImageDraw.Draw(eye_glow)
        eg_draw.ellipse([eye_cx - 8, eye_cy - 8, eye_cx + 8, eye_cy + 8],
                        fill=(*PIXEL_EYE, 55))
        base_rgba = img.convert("RGBA")
        img.paste(Image.alpha_composite(base_rgba, eye_glow).convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Pixel mouth — WORRIED: flat line, slight downward curve at corners
    mouth_x = bcx + eye_track_x - 10
    mouth_y = bcy + int(bh * 0.18) + eye_track_y // 2
    mouth_w = 20
    # Three pixel blocks: center flat, corners lower
    draw.rectangle([mouth_x, mouth_y, mouth_x + 6, mouth_y + 4], fill=LINE)
    draw.rectangle([mouth_x + 7, mouth_y, mouth_x + 13, mouth_y + 4], fill=LINE)
    draw.rectangle([mouth_x + 14, mouth_y, mouth_x + 20, mouth_y + 4], fill=LINE)
    # Corner droop pixels
    draw.rectangle([mouth_x - 3, mouth_y + 3, mouth_x, mouth_y + 7], fill=LINE)
    draw.rectangle([mouth_x + 20, mouth_y + 3, mouth_x + 23, mouth_y + 7], fill=LINE)

    # Stubby limbs — two lower (feet), two upper (arms)
    limb_color = BYTE_FILL
    limb_w = 12
    limb_h = 22

    # Lower limbs — hanging down (floating)
    ll_x = bcx - int(bw * 0.22)
    rl_x = bcx + int(bw * 0.22)
    limb_bot_y = bcy + bh // 2

    draw.rounded_rectangle(
        [ll_x - limb_w // 2, limb_bot_y,
         ll_x + limb_w // 2, limb_bot_y + limb_h],
        radius=6, fill=limb_color, outline=LINE, width=2)
    draw.rounded_rectangle(
        [rl_x - limb_w // 2, limb_bot_y,
         rl_x + limb_w // 2, limb_bot_y + limb_h],
        radius=6, fill=limb_color, outline=LINE, width=2)

    # Upper limbs — arms. WORRIED expression: one arm slightly raised (gesturing up)
    # Left arm: raised slightly (tiny gesture toward Luma — "are you LISTENING?")
    la_x = bcx - int(bw * 0.42)
    draw.rounded_rectangle(
        [la_x - limb_w // 2, bcy - int(bh * 0.28) - 10,
         la_x + limb_w // 2, bcy - int(bh * 0.28) + limb_h],
        radius=6, fill=limb_color, outline=LINE, width=2)

    # Right arm: hanging naturally
    ra_x = bcx + int(bw * 0.42)
    draw.rounded_rectangle(
        [ra_x - limb_w // 2, bcy + int(bh * 0.05),
         ra_x + limb_w // 2, bcy + int(bh * 0.05) + limb_h],
        radius=6, fill=limb_color, outline=LINE, width=2)

    # Redraw body outline on top of everything
    draw.ellipse(
        [bcx - bw // 2, bcy - bh // 2, bcx + bw // 2, bcy + bh // 2],
        outline=LINE, width=3)

    return draw


def draw_warm_rim_light(img, luma_cx, luma_cy, luma_hr):
    """Add warm amber rim light on Luma's left side (window-side)."""
    rim_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rim_draw = ImageDraw.Draw(rim_layer)
    # Rim ellipse on left side of luma
    rx = int(luma_hr * 1.15)
    ry = int(luma_hr * 1.8)
    for step in range(8, 0, -1):
        t = step / 8.0
        er = max(1, int(rx * 0.15 * t))
        ery = max(1, int(ry * 0.12 * t))
        alpha = int(45 * (1 - t))
        cx_r = luma_cx - rx + er
        rim_draw.ellipse([cx_r - er, luma_cy - ery, cx_r + er, luma_cy + ery],
                         fill=(*SUNLIT_AMBER, alpha))
    base_rgba = img.convert("RGBA")
    img.paste(Image.alpha_composite(base_rgba, rim_layer).convert("RGB"))


def draw_labels(draw):
    """Draw slate label — AD reference / pitch asset."""
    try:
        font = load_font(size=18, bold=False)
        font_bold = load_font(size=22, bold=True)
    except Exception:
        font = font_bold = ImageFont.load_default()

    # Bottom-left corner slate
    label_x = 32
    label_y = H - 60
    draw.rectangle([label_x - 4, label_y - 4, label_x + 560, label_y + 52],
                   fill=(12, 10, 18, 200) if hasattr(draw, '_mode') else (12, 10, 18))
    draw.text((label_x, label_y),
              "SF04 — LUMA + BYTE: THE DYNAMIC", fill=SOFT_GOLD, font=font_bold)
    draw.text((label_x, label_y + 26),
              "Cycle 25 | Art Director: Alex Chen | v001",
              fill=(160, 150, 130), font=font)


def generate():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    img = Image.new("RGB", (W, H), (80, 52, 22))
    draw = ImageDraw.Draw(img)

    # Step 1: Background
    draw = draw_background(draw, img)
    draw = ImageDraw.Draw(img)

    # Step 2: Draw Luma — centered slightly left of frame center
    # Luma is our primary character — she occupies roughly left-center of frame
    # Her torso center sits at ~40% width, ~60% height
    luma_cx = int(W * 0.40)
    luma_cy = int(H * 0.60)

    draw, head_cx, head_cy, head_r, torso_cx, torso_cy = draw_luma(draw, img, luma_cx, luma_cy)

    # Step 3: Add warm rim light on Luma (window side)
    draw_warm_rim_light(img, head_cx, head_cy, head_r)
    draw = ImageDraw.Draw(img)

    # Step 4: Draw Byte on Luma's right shoulder
    # Right shoulder position: torso_cx + torso_w//2, just above torso mid
    # From Luma's draw: torso_w = HU * 0.58 = 220 * 0.58 ≈ 128
    HU = 220
    torso_w = int(HU * 0.58)
    shoulder_x = torso_cx + torso_w // 2 - 10
    shoulder_y = torso_cy - int(HU * 0.45)
    draw = draw_byte(draw, img, shoulder_x, shoulder_y)
    draw = ImageDraw.Draw(img)

    # Step 5: Vignette — darken corners to focus attention on characters
    vig_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vig_draw = ImageDraw.Draw(vig_layer)
    for step in range(18, 0, -1):
        t = step / 18.0
        er = int(W * 0.62 * t)
        ery = int(H * 0.62 * t)
        alpha = int(80 * (1 - t))
        vig_draw.ellipse([W // 2 - er, H // 2 - ery, W // 2 + er, H // 2 + ery],
                         fill=(0, 0, 0, alpha))
    # Vignette is inverse of this — we want corners dark, center clear
    # So we invert: make a dark RGBA and punch a clear ellipse
    vig_dark = Image.new("RGBA", (W, H), (0, 0, 0, 90))
    vig_punch_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vp_draw = ImageDraw.Draw(vig_punch_layer)
    for step in range(14, 0, -1):
        t = step / 14.0
        er = int(W * 0.46 * t)
        ery = int(H * 0.50 * t)
        alpha = int(90 * t)
        vp_draw.ellipse([W // 2 - er, H // 2 - ery, W // 2 + er, H // 2 + ery],
                        fill=(0, 0, 0, alpha))
    base_rgba = img.convert("RGBA")
    with_vignette = Image.alpha_composite(base_rgba, vig_dark)
    # Re-add central brightness by lightening center
    img.paste(with_vignette.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Step 6: Labels
    draw_labels(draw)

    # Save
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
