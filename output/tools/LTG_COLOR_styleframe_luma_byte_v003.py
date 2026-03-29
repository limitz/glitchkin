#!/usr/bin/env python3
"""
LTG_COLOR_styleframe_luma_byte_v003.py
Style Frame 04 — "The Dynamic" — Luma + Byte Interaction  (PROCEDURAL QUALITY)
"Luma & the Glitchkin" — Cycle 28

Art Director: Alex Chen
Procedural Art Engineer: Rin Yamamoto
Cycle: 28

Design brief (same as v001/v002):
  Scene: Luma and Byte are in her bedroom at dusk. Byte sits on her
  right shoulder. Luma is leaning slightly forward — CURIOUS expression,
  looking at something off-screen right (the TV / a glitch signal).
  Byte is looking the OPPOSITE direction — up at Luma's face — with a
  WORRIED/skeptical expression.

  Lighting: Warm window light from the left (RW-03 Sunlit Amber).
  Cool monitor/Glitch Layer ambient from right (GL-01b Byte Teal).

C28 fixes applied (from Critique 12 — Sven Halvorsen):
  1. Blush color corrected: RGB (232, 168, 124) alpha 65 — warm peach
     (was orange-red (220, 80, 50))
  2. Byte body fill corrected: (0, 212, 232) = GL-01b BYTE_TEAL canonical
     (was (0, 190, 210))
  3. add_rim_light() now uses side="right" — cyan rim only on monitor-facing
     right side of Luma (was direction-agnostic, incorrectly lit the left side)

Format: 1280x720 (≤ 1280px rule — scaled from 1920x1080 composition)
Output: output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v003.png
"""

import os
import sys
import math
import random
from PIL import Image, ImageDraw, ImageFont

# Import procedural draw library
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
from LTG_TOOL_procedural_draw_v001 import (
    wobble_line, wobble_polygon, variable_stroke,
    add_rim_light, add_face_lighting
)

OUTPUT_PATH = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v003.png"

# Working at 1280x720 — fits ≤ 1280px rule directly, no thumbnail needed
W, H = 1280, 720

# Scale factor vs original 1920x1080 composition
SX = W / 1920
SY = H / 1080


def sx(v): return int(v * SX)
def sy(v): return int(v * SY)


# ── Master Palette ────────────────────────────────────────────────────────────
WARM_CREAM      = (250, 240, 220)
SOFT_GOLD       = (232, 201,  90)
SUNLIT_AMBER    = (212, 146,  58)   # RW-03 — warm light basis
TERRACOTTA      = (199,  91,  57)
RUST_SHADOW     = (140,  58,  34)
SAGE_GREEN      = (122, 158, 126)
DUSTY_LAVENDER  = (168, 155, 191)
SHADOW_PLUM     = ( 92,  74, 114)
WARM_TAN        = (196, 168, 130)
SKIN_SHADOW     = (140,  90,  56)
DEEP_COCOA      = ( 59,  40,  32)
OCHRE_BRICK     = (184, 148,  74)
ELEC_CYAN       = (  0, 240, 255)   # GL-01a
BYTE_TEAL       = (  0, 212, 232)   # GL-01b — Byte body fill / cool rim (CANONICAL)
DEEP_CYAN       = (  0, 168, 180)
HOT_MAGENTA     = (255,  45, 107)   # GL-06
UV_PURPLE       = (123,  47, 190)   # GL-04
VOID_BLACK      = ( 10,  10,  20)
STATIC_WHITE    = (240, 240, 240)

# Character colors — Luma (CHAR-L palette)
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

# Character colors — Byte (C28: BYTE_FILL corrected to canonical GL-01b)
BYTE_FILL       = (  0, 212, 232)   # C28 FIX: was (0, 190, 210), now canonical BYTE_TEAL
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


def draw_background(draw, img):
    """Draw bedroom background with dual warm/cool lighting + procedural edges."""

    # Sky gradient — warm amber from top
    for y in range(H):
        t = y / H
        base_r = int(SUNLIT_AMBER[0] * 0.32 + 10)
        base_g = int(SUNLIT_AMBER[1] * 0.22 + 8)
        base_b = int(SUNLIT_AMBER[2] * 0.14 + 5)
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
    for y in range(floor_y, H, sy(32)):
        draw.line([(0, y), (W, y)], fill=RUST_SHADOW, width=1)
    for y in range(floor_y + sy(4), H, sy(64)):
        draw.line([(0, y), (W, y)], fill=(95, 56, 22), width=1)

    # Baseboard — procedural wobble line
    baseboard_y = floor_y - sy(16)
    draw.rectangle([0, baseboard_y, W, floor_y], fill=(90, 55, 20))
    # Wobble the top edge of baseboard for organic feel
    wobble_line(draw,
                (0, baseboard_y), (W, baseboard_y),
                color=DEEP_COCOA, width=2,
                amplitude=2.0, frequency=12, seed=101)

    # Window — left side (scaled)
    win_x0, win_y0 = sx(80), sy(55)
    win_x1, win_y1 = sx(380), sy(520)
    frame_color = (160, 100, 40)
    draw.rectangle([win_x0 - sx(24), win_y0 - sy(14),
                    win_x1 + sx(24), win_y1 + sy(14)],
                   fill=frame_color)
    draw.rectangle([win_x0, win_y0, win_x1, win_y1], fill=SOFT_GOLD)

    # Light gradient inside window
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

    # Window crossbars
    draw.line([(win_x0, (win_y0 + win_y1) // 2), (win_x1, (win_y0 + win_y1) // 2)],
              fill=frame_color, width=sx(10))
    draw.line([((win_x0 + win_x1) // 2, win_y0), ((win_x0 + win_x1) // 2, win_y1)],
              fill=frame_color, width=sx(10))

    # Window frame outer edge — procedural wobble for hand-drawn feel
    frame_pts = [
        (win_x0 - sx(24), win_y0 - sy(14)),
        (win_x1 + sx(24), win_y0 - sy(14)),
        (win_x1 + sx(24), win_y1 + sy(14)),
        (win_x0 - sx(24), win_y1 + sy(14)),
    ]
    wobble_polygon(draw, frame_pts, color=DEEP_COCOA, width=3,
                   amplitude=2.0, frequency=5, seed=201)

    draw.rectangle([win_x0, win_y0, win_x1, win_y1], outline=DEEP_COCOA, width=3)

    # Window light shaft
    shaft_pts = [
        (win_x0 + sx(20), win_y1),
        (win_x1 - sx(20), win_y1),
        (win_x1 + sx(80), floor_y),
        (win_x0 - sx(40), floor_y),
    ]
    shaft_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shaft_draw = ImageDraw.Draw(shaft_layer)
    shaft_draw.polygon(shaft_pts, fill=(*SUNLIT_AMBER, 55))
    base_rgba = img.convert("RGBA")
    img.paste(Image.alpha_composite(base_rgba, shaft_layer).convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Desk — right side partial
    desk_x = int(W * 0.74)
    desk_y = int(H * 0.56)
    desk_w = int(W * 0.26)
    desk_h = int(H * 0.08)
    desk_color = (145, 90, 35)
    draw.rectangle([desk_x, desk_y, desk_x + desk_w, desk_y + desk_h],
                   fill=desk_color)
    draw.rectangle([desk_x, desk_y - sy(6), desk_x + desk_w, desk_y],
                   fill=(165, 110, 50))
    # Procedural wobble on desk top edge
    wobble_line(draw,
                (desk_x, desk_y), (desk_x + desk_w, desk_y),
                color=DEEP_COCOA, width=2,
                amplitude=1.5, frequency=8, seed=301)

    # CRT monitor on desk
    crt_x = int(W * 0.78)
    crt_y = int(H * 0.32)
    crt_w = int(W * 0.18)
    crt_h = int(H * 0.22)
    draw.rectangle([crt_x - sx(14), crt_y - sy(14),
                    crt_x + crt_w + sx(14), crt_y + crt_h + sy(26)],
                   fill=(40, 34, 52), outline=(28, 22, 40), width=3)
    draw.rectangle([crt_x + crt_w // 3, crt_y + crt_h + sy(22),
                    crt_x + crt_w * 2 // 3, crt_y + crt_h + sy(44)],
                   fill=(32, 26, 42))

    # CRT screen
    scr_pad = sx(18)
    scr_x0 = crt_x + scr_pad
    scr_y0 = crt_y + scr_pad
    scr_x1 = crt_x + crt_w - scr_pad
    scr_y1 = crt_y + crt_h - scr_pad
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1], fill=ELEC_CYAN)
    for sy_scan in range(scr_y0 + 3, scr_y1, 5):
        draw.line([(scr_x0, sy_scan), (scr_x1, sy_scan)], fill=DEEP_CYAN, width=1)
    scr_rng = random.Random(12)
    for _ in range(18):
        px_x = scr_x0 + scr_rng.randint(4, max(5, scr_x1 - scr_x0 - 4))
        px_y = scr_y0 + scr_rng.randint(4, max(5, scr_y1 - scr_y0 - 4))
        ps = scr_rng.choice([2, 3, 4])
        pc = scr_rng.choice([(0, 80, 100), (0, 140, 160), STATIC_WHITE])
        draw.rectangle([px_x, px_y, px_x + ps, px_y + ps], fill=pc)
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1], outline=DEEP_CYAN, width=3)

    # Cyan light spill from monitor
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
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

    # Pixel confetti — Glitch Layer energy
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
    Draw Luma at mid-shot scale with procedural quality outlines.
    cx, cy = center of torso mass (scaled coordinates).
    Returns draw, head_cx, head_cy, head_r, torso_cx, torso_cy
    """

    # Scale: head height = 220px at 1920x1080 → 147px at 1280x720
    HU = sy(220)

    # Body proportions
    head_r = int(HU * 0.50)
    torso_h = int(HU * 1.0)
    torso_w = int(HU * 0.58)

    lean_offset = sx(22)
    torso_cx = cx + lean_offset
    torso_cy = cy

    neck_gap = int(HU * 0.05)
    head_cx = torso_cx - sx(8)
    head_cy = torso_cy - torso_h // 2 - neck_gap - head_r

    face_shift = int(head_r * 0.10)

    # ── Jeans / lower body ───────────────────────────────────────────────────
    leg_w = int(HU * 0.28)
    leg_h = int(HU * 0.80)
    leg_y0 = torso_cy + torso_h // 2

    draw.rounded_rectangle(
        [torso_cx - torso_w // 2 + 4, leg_y0,
         torso_cx - torso_w // 2 + 4 + leg_w, leg_y0 + leg_h],
        radius=sy(18), fill=JEANS, outline=LINE, width=3)
    draw.rounded_rectangle(
        [torso_cx + torso_w // 2 - 4 - leg_w, leg_y0,
         torso_cx + torso_w // 2 - 4, leg_y0 + leg_h],
        radius=sy(18), fill=JEANS, outline=LINE, width=3)
    draw.rounded_rectangle(
        [torso_cx - torso_w // 2 + 4, leg_y0,
         torso_cx - torso_w // 2 + 4 + leg_w - 6, leg_y0 + leg_h],
        radius=sy(18), fill=JEANS_SH, outline=None)
    draw.rounded_rectangle(
        [torso_cx + torso_w // 2 - 4 - leg_w + 6, leg_y0,
         torso_cx + torso_w // 2 - 4, leg_y0 + leg_h],
        radius=sy(18), fill=JEANS_SH, outline=None)

    # ── Hoodie torso — fill first, then procedural outline ───────────────────
    torso_pts = [
        (torso_cx - torso_w // 2, torso_cy - torso_h // 2),
        (torso_cx + torso_w // 2, torso_cy - torso_h // 2),
        (torso_cx + torso_w // 2, torso_cy + torso_h // 2),
        (torso_cx - torso_w // 2, torso_cy + torso_h // 2),
    ]
    draw.rounded_rectangle(
        [torso_cx - torso_w // 2, torso_cy - torso_h // 2,
         torso_cx + torso_w // 2, torso_cy + torso_h // 2],
        radius=sy(28), fill=HOODIE_ORANGE)

    # Procedural wobble outline on hoodie torso
    wobble_polygon(draw, torso_pts, color=LINE, width=3,
                   amplitude=2.5, frequency=4, seed=401)

    # Shadow (right/back side)
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.rounded_rectangle(
        [torso_cx + torso_w // 4, torso_cy - torso_h // 2,
         torso_cx + torso_w // 2, torso_cy + torso_h // 2],
        radius=sy(28), fill=(*HOODIE_AMBIENT, 140))
    base_rgba = img.convert("RGBA")
    img.paste(Image.alpha_composite(base_rgba, shadow_layer).convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Pixel grid on hoodie
    pixel_size = sx(8)
    pixel_gap = sx(14)
    px_grid_x = torso_cx - sx(18)
    px_grid_y = torso_cy - sy(30)
    for row in range(3):
        for col in range(3):
            px_x = px_grid_x + col * (pixel_size + pixel_gap)
            px_y = px_grid_y + row * (pixel_size + pixel_gap)
            pc = ELEC_CYAN if (row == 1 and col == 1) else SOFT_GOLD
            draw.rectangle([px_x, px_y, px_x + pixel_size, px_y + pixel_size], fill=pc)

    # Kangaroo pocket
    pocket_y = torso_cy + int(torso_h * 0.2)
    draw.rounded_rectangle(
        [torso_cx - torso_w // 2 + sx(12), pocket_y,
         torso_cx + torso_w // 2 - sx(12), torso_cy + torso_h // 2 - sy(10)],
        radius=sy(12), fill=HOODIE_SH, outline=LINE, width=2)

    # ── Arms ─────────────────────────────────────────────────────────────────
    arm_w = int(HU * 0.22)
    arm_h = int(HU * 0.85)

    la_x = torso_cx - torso_w // 2 - arm_w // 2 + sx(6)
    la_y = torso_cy - torso_h // 2 + int(HU * 0.12)
    draw.rounded_rectangle(
        [la_x - arm_w // 2, la_y,
         la_x + arm_w // 2, la_y + arm_h],
        radius=sy(16), fill=HOODIE_ORANGE, outline=LINE, width=3)

    ra_x = torso_cx + torso_w // 2 + arm_w // 2 - sx(6)
    ra_y = torso_cy - torso_h // 2 + int(HU * 0.08)
    draw.rounded_rectangle(
        [ra_x - arm_w // 2, ra_y,
         ra_x + arm_w // 2, ra_y + arm_h],
        radius=sy(16), fill=HOODIE_ORANGE, outline=LINE, width=3)

    # Arm outline wobble on left arm (main visible arm)
    arm_pts = [
        (la_x - arm_w // 2, la_y),
        (la_x + arm_w // 2, la_y),
        (la_x + arm_w // 2, la_y + arm_h),
        (la_x - arm_w // 2, la_y + arm_h),
    ]
    wobble_polygon(draw, arm_pts, color=LINE, width=2,
                   amplitude=1.5, frequency=5, seed=411)

    # ── Neck ─────────────────────────────────────────────────────────────────
    draw.ellipse(
        [head_cx - int(HU * 0.12), head_cy + head_r - sy(8),
         head_cx + int(HU * 0.12), head_cy + head_r + int(HU * 0.08)],
        fill=SKIN)

    # ── Head — filled circle ─────────────────────────────────────────────────
    draw.ellipse(
        [head_cx - head_r, head_cy - head_r,
         head_cx + head_r, head_cy + head_r],
        fill=SKIN)
    # Cheek highlight
    draw.ellipse(
        [head_cx - head_r + sx(10), head_cy - int(head_r * 0.1),
         head_cx - head_r + sx(10) + int(head_r * 0.55),
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

    # ── variable_stroke on head perimeter — primary character outline ────────
    # Draw 8 arcs around the head perimeter using variable_stroke
    num_arcs = 8
    for i in range(num_arcs):
        a0 = (2 * math.pi * i / num_arcs) - math.pi / 2
        a1 = (2 * math.pi * (i + 1) / num_arcs) - math.pi / 2
        p1 = (head_cx + head_r * math.cos(a0), head_cy + head_r * math.sin(a0))
        p2 = (head_cx + head_r * math.cos(a1), head_cy + head_r * math.sin(a1))
        variable_stroke(img, p1, p2, max_width=4, min_width=1, color=LINE, seed=500 + i)
    draw = ImageDraw.Draw(img)

    # ── Blush — C28 FIX: warm peach RGB (232, 168, 124) alpha 65 ─────────────
    # (was orange-red (220, 80, 50) alpha 55 — physically incorrect)
    BLUSH_COLOR = (232, 168, 124)
    BLUSH_ALPHA = 65
    blush_r = int(head_r * 0.22)
    blush_y = head_cy + int(head_r * 0.15)
    blush_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bl_draw = ImageDraw.Draw(blush_layer)
    bl_draw.ellipse(
        [head_cx - int(head_r * 0.68) - blush_r, blush_y - blush_r // 2,
         head_cx - int(head_r * 0.68) + blush_r * 2, blush_y + blush_r],
        fill=(*BLUSH_COLOR, BLUSH_ALPHA))
    bl_draw.ellipse(
        [head_cx + int(head_r * 0.32) - blush_r, blush_y - blush_r // 2,
         head_cx + int(head_r * 0.32) + blush_r * 2, blush_y + blush_r],
        fill=(*BLUSH_COLOR, BLUSH_ALPHA))
    base_rgba = img.convert("RGBA")
    img.paste(Image.alpha_composite(base_rgba, blush_layer).convert("RGB"))
    draw = ImageDraw.Draw(img)

    # ── Face features — CURIOUS expression ───────────────────────────────────
    eye_y = head_cy + int(head_r * 0.05)
    eye_w = int(head_r * 0.36)
    eye_h = int(head_r * 0.32)

    # Left eye
    le_cx = head_cx - int(head_r * 0.28) + face_shift
    draw.rounded_rectangle(
        [le_cx - eye_w // 2, eye_y - eye_h // 2,
         le_cx + eye_w // 2, eye_y + eye_h // 2],
        radius=sy(8), fill=EYE_W, outline=LINE, width=2)
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
        fill=STATIC_WHITE)

    # Right eye
    re_cx = head_cx + int(head_r * 0.28) + face_shift
    re_h_open = int(eye_h * 0.85)
    draw.rounded_rectangle(
        [re_cx - eye_w // 2, eye_y - re_h_open // 2,
         re_cx + eye_w // 2, eye_y + re_h_open // 2],
        radius=sy(8), fill=EYE_W, outline=LINE, width=2)
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

    # Eyebrows — CURIOUS: raised arches with wobble_line for organic feel
    brow_y_l = eye_y - eye_h // 2 - int(head_r * 0.16)
    brow_y_r = eye_y - re_h_open // 2 - int(head_r * 0.22)
    brow_w = int(head_r * 0.38)

    wobble_line(draw,
                (le_cx - brow_w // 2, brow_y_l + 4),
                (le_cx + brow_w // 2, brow_y_l + 2),
                color=LINE, width=5, amplitude=1.5, frequency=3, seed=601)
    wobble_line(draw,
                (re_cx - brow_w // 2, brow_y_r + 6),
                (re_cx + brow_w // 2, brow_y_r + 4),
                color=LINE, width=5, amplitude=1.5, frequency=3, seed=611)

    # Nose
    nose_x = head_cx + face_shift + int(head_r * 0.06)
    nose_y = head_cy + int(head_r * 0.28)
    draw.arc(
        [nose_x - sx(10), nose_y - sy(8), nose_x + sx(6), nose_y + sy(8)],
        start=180, end=340, fill=LINE, width=3)

    # Mouth — CURIOUS (open, one corner lifted)
    mouth_y = head_cy + int(head_r * 0.50)
    mouth_w = int(head_r * 0.50)
    mouth_x = head_cx + face_shift - mouth_w // 2 + 4
    draw.arc(
        [mouth_x, mouth_y - sy(10), mouth_x + mouth_w, mouth_y + sy(20)],
        start=10, end=170, fill=LINE, width=4)
    draw.ellipse(
        [mouth_x + mouth_w // 4, mouth_y - 2,
         mouth_x + mouth_w * 3 // 4, mouth_y + sy(12)],
        fill=DEEP_COCOA)

    # ── Hair — procedural wobble polygon silhouette ───────────────────────────
    hair_cx = head_cx - sx(6)
    hair_cy = head_cy - head_r + sy(8)

    hair_mass_points = [
        (hair_cx - int(head_r * 1.10), hair_cy + int(head_r * 0.30)),
        (hair_cx - int(head_r * 1.18), hair_cy - int(head_r * 0.15)),
        (hair_cx - int(head_r * 0.90), hair_cy - int(head_r * 0.65)),
        (hair_cx - int(head_r * 0.42), hair_cy - int(head_r * 1.05)),
        (hair_cx + int(head_r * 0.08), hair_cy - int(head_r * 1.22)),
        (hair_cx + int(head_r * 0.55), hair_cy - int(head_r * 1.08)),
        (hair_cx + int(head_r * 0.92), hair_cy - int(head_r * 0.60)),
        (hair_cx + int(head_r * 1.05), hair_cy + int(head_r * 0.05)),
        (hair_cx + int(head_r * 0.85), hair_cy + int(head_r * 0.40)),
        (hair_cx - int(head_r * 0.80), hair_cy + int(head_r * 0.55)),
    ]

    # Wobble polygon: fill first (flat), then procedural outline
    wobble_polygon(draw, hair_mass_points,
                   color=LINE, width=3,
                   amplitude=3.5, frequency=4, seed=701,
                   fill=HAIR)

    # Hair highlight crown
    draw.polygon([
        (hair_cx - int(head_r * 0.22), hair_cy - int(head_r * 1.18)),
        (hair_cx + int(head_r * 0.18), hair_cy - int(head_r * 1.22)),
        (hair_cx + int(head_r * 0.40), hair_cy - int(head_r * 0.90)),
        (hair_cx + int(head_r * 0.08), hair_cy - int(head_r * 0.88)),
        (hair_cx - int(head_r * 0.12), hair_cy - int(head_r * 0.90)),
    ], fill=HAIR_HL)

    # Curl arcs
    curls = [
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

    # Flyaways
    flyaway_rng = random.Random(77)
    for _ in range(4):
        fx = hair_cx + flyaway_rng.randint(-int(head_r * 0.8), int(head_r * 0.8))
        fy = hair_cy - int(head_r * 0.85) - flyaway_rng.randint(0, 20)
        fly_len = flyaway_rng.randint(18, 34)
        fly_dx = flyaway_rng.randint(-12, 12)
        draw.line([(fx, fy), (fx + fly_dx, fy - fly_len)], fill=HAIR_HL, width=2)

    # Ringlet near right ear
    ring_cx = head_cx + int(head_r * 0.82)
    ring_cy = head_cy + int(head_r * 0.20)
    draw.arc([ring_cx - sx(14), ring_cy - sy(16), ring_cx + sx(14), ring_cy + sy(16)],
             start=60, end=310, fill=HAIR, width=4)

    return draw, head_cx, head_cy, head_r, torso_cx, torso_cy


def draw_byte(draw, img, shoulder_cx, shoulder_cy):
    """
    Draw Byte on Luma's right shoulder with procedural quality outlines.
    C28: BYTE_FILL corrected to canonical GL-01b (0, 212, 232).
    """
    bw = sx(80)
    bh = sy(68)
    bcx = shoulder_cx
    bcy = shoulder_cy - bh // 2 - sy(8)

    # Byte glow — own light source (GL-01b BYTE_TEAL — NOT ELEC_CYAN)
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

    # Pixel confetti beneath Byte
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

    # Byte body fill — C28 FIX: canonical GL-01b (0, 212, 232)
    draw.ellipse(
        [bcx - bw // 2, bcy - bh // 2, bcx + bw // 2, bcy + bh // 2],
        fill=BYTE_FILL)

    # Shadow right side
    shadow_b_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sb_draw = ImageDraw.Draw(shadow_b_layer)
    sb_draw.ellipse(
        [bcx, bcy - bh // 2, bcx + bw // 2, bcy + bh // 2],
        fill=(*BYTE_SH, 180))
    base_rgba = img.convert("RGBA")
    img.paste(Image.alpha_composite(base_rgba, shadow_b_layer).convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Highlight left side (window)
    hl_b_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hb_draw = ImageDraw.Draw(hl_b_layer)
    hb_draw.ellipse(
        [bcx - bw // 2, bcy - bh // 2, bcx - bw // 8, bcy],
        fill=(*BYTE_HL, 90))
    base_rgba = img.convert("RGBA")
    img.paste(Image.alpha_composite(base_rgba, hl_b_layer).convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Glitch scar — Hot Magenta
    scar_x1 = bcx + int(bw * 0.15)
    scar_y1 = bcy - int(bh * 0.30)
    scar_x2 = bcx + int(bw * 0.38)
    scar_y2 = bcy + int(bh * 0.32)
    draw.line([(scar_x1, scar_y1), (scar_x2, scar_y2)], fill=SCAR_MAG, width=3)
    draw.line([(scar_x1 + sx(8), scar_y1 + sy(16)), (scar_x1 + sx(20), scar_y1 + sy(8))],
              fill=SCAR_MAG, width=2)

    # variable_stroke on Byte body perimeter
    num_arcs = 8
    for i in range(num_arcs):
        a0 = (2 * math.pi * i / num_arcs) - math.pi / 2
        a1 = (2 * math.pi * (i + 1) / num_arcs) - math.pi / 2
        # Scale for oval
        p1 = (bcx + (bw // 2) * math.cos(a0), bcy + (bh // 2) * math.sin(a0))
        p2 = (bcx + (bw // 2) * math.cos(a1), bcy + (bh // 2) * math.sin(a1))
        variable_stroke(img, p1, p2, max_width=3, min_width=1, color=LINE, seed=800 + i)
    draw = ImageDraw.Draw(img)

    # Face features — WORRIED, looking up
    face_tilt_up = int(bh * 0.12)
    eye_size = max(5, sx(10))
    eye_gap = int(bw * 0.22)
    eye_y = bcy - face_tilt_up - eye_size // 2

    eye_track_x = -int(bw * 0.05)
    eye_track_y = -int(bh * 0.08)

    le_x = bcx - eye_gap + eye_track_x
    re_x = bcx + eye_gap - eye_size + eye_track_x
    e_y = eye_y + eye_track_y

    draw.rectangle([le_x - eye_size // 2, e_y,
                    le_x + eye_size // 2, e_y + eye_size - 2],
                   fill=PIXEL_EYE)
    draw.rectangle([re_x - eye_size // 2, e_y - 1,
                    re_x + eye_size // 2, e_y + eye_size],
                   fill=PIXEL_EYE)

    # Eye glow
    for eye_cx_g, eye_cy_g in [(le_x, e_y + eye_size // 2), (re_x, e_y + eye_size // 2)]:
        eye_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        eg_draw = ImageDraw.Draw(eye_glow)
        eg_draw.ellipse([eye_cx_g - sy(8), eye_cy_g - sy(8),
                         eye_cx_g + sy(8), eye_cy_g + sy(8)],
                        fill=(*PIXEL_EYE, 55))
        base_rgba = img.convert("RGBA")
        img.paste(Image.alpha_composite(base_rgba, eye_glow).convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Pixel mouth — WORRIED frown
    mouth_x = bcx + eye_track_x - sx(10)
    mouth_y = bcy + int(bh * 0.18) + eye_track_y // 2
    mouth_w = sx(20)
    draw.rectangle([mouth_x, mouth_y, mouth_x + sx(6), mouth_y + sy(4)], fill=LINE)
    draw.rectangle([mouth_x + sx(7), mouth_y, mouth_x + sx(13), mouth_y + sy(4)], fill=LINE)
    draw.rectangle([mouth_x + sx(14), mouth_y, mouth_x + sx(20), mouth_y + sy(4)], fill=LINE)
    draw.rectangle([mouth_x - sx(3), mouth_y + sy(3), mouth_x, mouth_y + sy(7)], fill=LINE)
    draw.rectangle([mouth_x + sx(20), mouth_y + sy(3), mouth_x + sx(23), mouth_y + sy(7)], fill=LINE)

    # Stubby limbs
    limb_color = BYTE_FILL
    limb_w = max(4, sx(12))
    limb_h = sy(22)

    ll_x = bcx - int(bw * 0.22)
    rl_x = bcx + int(bw * 0.22)
    limb_bot_y = bcy + bh // 2

    draw.rounded_rectangle(
        [ll_x - limb_w // 2, limb_bot_y,
         ll_x + limb_w // 2, limb_bot_y + limb_h],
        radius=sy(6), fill=limb_color, outline=LINE, width=2)
    draw.rounded_rectangle(
        [rl_x - limb_w // 2, limb_bot_y,
         rl_x + limb_w // 2, limb_bot_y + limb_h],
        radius=sy(6), fill=limb_color, outline=LINE, width=2)

    # Left arm raised (gesture)
    la_x = bcx - int(bw * 0.42)
    draw.rounded_rectangle(
        [la_x - limb_w // 2, bcy - int(bh * 0.28) - sy(10),
         la_x + limb_w // 2, bcy - int(bh * 0.28) + limb_h],
        radius=sy(6), fill=limb_color, outline=LINE, width=2)

    # Right arm natural
    ra_x = bcx + int(bw * 0.42)
    draw.rounded_rectangle(
        [ra_x - limb_w // 2, bcy + int(bh * 0.05),
         ra_x + limb_w // 2, bcy + int(bh * 0.05) + limb_h],
        radius=sy(6), fill=limb_color, outline=LINE, width=2)

    # Redraw body outline (on top)
    draw.ellipse(
        [bcx - bw // 2, bcy - bh // 2, bcx + bw // 2, bcy + bh // 2],
        outline=LINE, width=2)

    return draw


def draw_labels(draw):
    """Draw slate label."""
    try:
        font = load_font(size=14, bold=False)
        font_bold = load_font(size=16, bold=True)
    except Exception:
        font = font_bold = ImageFont.load_default()

    label_x = 22
    label_y = H - 50
    draw.rectangle([label_x - 4, label_y - 4, label_x + 480, label_y + 42],
                   fill=(12, 10, 18))
    draw.text((label_x, label_y),
              "SF04 — LUMA + BYTE: THE DYNAMIC", fill=SOFT_GOLD, font=font_bold)
    draw.text((label_x, label_y + 20),
              "Cycle 28 | Procedural Quality v003 | Rin Yamamoto | C28 fixes applied",
              fill=(160, 150, 130), font=font)


def generate():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    img = Image.new("RGB", (W, H), (80, 52, 22))
    draw = ImageDraw.Draw(img)

    # Step 1: Background with procedural edges
    draw = draw_background(draw, img)
    draw = ImageDraw.Draw(img)

    # Step 2: Draw Luma
    luma_cx = int(W * 0.40)
    luma_cy = int(H * 0.60)
    draw, head_cx, head_cy, head_r, torso_cx, torso_cy = draw_luma(draw, img, luma_cx, luma_cy)
    draw = ImageDraw.Draw(img)

    # Step 3: add_face_lighting on Luma — warm light from upper-left (window)
    # light_dir (-1, -1) = upper-left source (window side)
    luma_face_center = (head_cx, head_cy)
    luma_face_radius = (head_r, head_r)
    add_face_lighting(
        img,
        face_center=luma_face_center,
        face_radius=luma_face_radius,
        light_dir=(-1, -1),                      # upper-left = window
        shadow_color=SKIN_SH,                    # warm-dark shadow
        highlight_color=SKIN_HL,                 # warm highlight
        seed=901
    )
    draw = ImageDraw.Draw(img)

    # Step 4: add_rim_light on Luma — C28 FIX: side="right" (monitor-facing side only)
    # Previously direction-agnostic — this fix prevents cyan rim on the warm left side
    add_rim_light(img, threshold=170, light_color=BYTE_TEAL, width=3, side="right")
    draw = ImageDraw.Draw(img)

    # Step 5: Draw Byte on Luma's right shoulder
    HU = sy(220)
    torso_w = int(HU * 0.58)
    shoulder_x = torso_cx + torso_w // 2 - sx(10)
    shoulder_y = torso_cy - int(HU * 0.45)
    draw = draw_byte(draw, img, shoulder_x, shoulder_y)
    draw = ImageDraw.Draw(img)

    # Step 6: Vignette
    vig_dark = Image.new("RGBA", (W, H), (0, 0, 0, 90))
    base_rgba = img.convert("RGBA")
    with_vignette = Image.alpha_composite(base_rgba, vig_dark)
    img.paste(with_vignette.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Step 7: Labels
    draw_labels(draw)

    # Image size rule: ≤ 1280px — already 1280×720, apply thumbnail as safety
    img.thumbnail((1280, 1280), Image.LANCZOS)

    # Save
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  ({img.width}x{img.height})")
    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
