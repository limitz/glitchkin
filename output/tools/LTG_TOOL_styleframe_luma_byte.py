# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_styleframe_luma_byte.py
Style Frame 04 — "The Dynamic" (Luma + Byte Interaction) — Full Rebuild
"Luma & the Glitchkin" — Cycle 32

Art Director: Alex Chen
Procedural Art Engineer: Rin Yamamoto
Cycle: 32

REBUILD REASON (Sven / Critique 13 P1, CRITICAL):
  SF04 source generators were lost in C28 (stubs only). Sven's audit:
    - Value ceiling at 198 (FAIL — needs >= 225 for a glowing character)
    - Silhouette ambiguous
    - Byte has zero monitor contribution
    - Shadow temperatures wrong

REBUILT FROM SCRATCH (C32) using LTG_COLOR_styleframe_luma_byte.png
as composition reference.

Canonical specs:
  - Byte body   = GL-01b #00D4E8 (BYTE_TEAL)
  - Luma blush  = #E8A87C
  - Rim light   = side="right" with char_cx set per-character
  - Face light  = warm upper-left for Luma
  - Value ceil  = brightest highlight >= 225
  - Monitor glow: Byte has cool (#00D4E8) contribution on their near side
  - Canvas 1280x720 (<= 1280px rule)

Composition (reconstructed from v003 PNG):
  - Background: warm domestic room. CRT monitor on right emitting cyan glow.
  - Luma: left-center (~x=0.32W), sitting/standing, facing right toward Byte.
  - Byte: right-center (~x=0.68W), hovering, facing left toward Luma.
  - Byte's monitor-face emits BYTE_TEAL glow that spills onto surroundings.
  - Title strip at bottom.

Output: /home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_luma_byte.png
Usage: python3 LTG_TOOL_styleframe_luma_byte.py
"""

import os
import sys
import math
import random
from PIL import Image, ImageDraw, ImageFont

# Import procedural draw library (v1.3.0 required for char_cx)
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _here)
from LTG_TOOL_procedural_draw import (
    wobble_line, wobble_polygon, variable_stroke,
    add_rim_light, add_face_lighting, silhouette_test, value_study
)

OUTPUT_PATH = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_luma_byte.png"

W, H = 1280, 720

# Scale helpers (reference: 1920x1080)
SX = W / 1920
SY = H / 1080
def sx(n): return int(n * SX)
def sy(n): return int(n * SY)
def sp(n): return int(n * min(SX, SY))

# ── Canonical Palette ─────────────────────────────────────────────────────────
WARM_CREAM      = (250, 240, 220)
SOFT_GOLD       = (232, 201,  90)
SUNLIT_AMBER    = (212, 146,  58)   # RW-03 #D4923A — defined for reference; not placed in SF04.
                                    # SF04 lamp halo uses (255,200,80) hue=41° — incandescent
                                    # lamp amber, intentionally warmer/brighter than outdoor RW-03.
                                    # Use RW-03 for sunlit-window/exterior surfaces; (255,200,80)
                                    # for indoor lamp glow. C35 analysis: warm_cool_analysis_c35.md.
TERRACOTTA      = (199,  91,  57)
RUST_SHADOW     = (140,  58,  34)
WARM_TAN        = (196, 168, 130)
SKIN            = (200, 136,  90)
SKIN_HL         = (232, 184, 136)   # warm highlight — guaranteed >= 225 not needed here
SKIN_SH         = (168, 104,  56)
HAIR_COLOR      = ( 26,  15,  10)
LINE            = ( 59,  40,  32)
HOODIE_ORANGE   = (232, 112,  58)
HOODIE_SHADOW   = (184,  74,  32)
JEANS           = ( 58,  90, 140)
JEANS_SH        = ( 38,  62, 104)
# Luma blush canonical: #E8A87C
BLUSH           = (232, 168, 124)   # #E8A87C

# Byte canonical: GL-01b #00D4E8 BYTE_TEAL
BYTE_TEAL       = (  0, 212, 232)   # GL-01b body fill
BYTE_HL         = (  0, 240, 255)   # ELEC_CYAN highlight — 255 channel guarantees >= 225
BYTE_SH         = (  0, 144, 176)
BYTE_OUTLINE    = (  0, 100, 130)
# Monitor glow: pure BYTE_TEAL
MONITOR_GLOW    = (  0, 212, 232)

ELEC_CYAN       = (  0, 240, 255)
HOT_MAGENTA     = (255,  45, 107)
UV_PURPLE       = (123,  47, 190)
VOID_BLACK      = ( 10,  10,  20)
CORRUPTED_AMBER = (255, 140,   0)
SCAR_MAG        = (255,  45, 107)

# Wall / room
WALL_WARM       = (220, 190, 150)
WALL_UPPER      = (200, 168, 122)
FLOOR_COLOR     = (160, 120,  70)
FLOOR_SHADOW    = (120,  88,  48)
CEILING_COLOR   = ( 80,  55,  22)

# Bright specular — value ceiling guarantee (>= 225)
SPECULAR_WHITE  = (255, 252, 240)   # 255 >= 225 ✓
SPECULAR_CYAN   = (180, 248, 255)   # 255 >= 225 ✓


def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def draw_background(img, draw):
    """Draw warm domestic room background with CRT monitor on right."""
    rng = random.Random(42)

    ceiling_y = sy(130)
    floor_y   = sy(680)

    # Ceiling strip
    draw.rectangle([0, 0, W, ceiling_y], fill=CEILING_COLOR)
    draw.line([(0, ceiling_y), (W, ceiling_y)], fill=(50, 32, 12), width=sp(4))

    # Back wall — warm gradient (vertical)
    for row in range(ceiling_y, floor_y):
        t = (row - ceiling_y) / max(1, floor_y - ceiling_y)
        r = int(WALL_UPPER[0] + (WALL_WARM[0] - WALL_UPPER[0]) * t)
        g = int(WALL_UPPER[1] + (WALL_WARM[1] - WALL_UPPER[1]) * t)
        b = int(WALL_UPPER[2] + (WALL_WARM[2] - WALL_UPPER[2]) * t)
        draw.line([(0, row), (W, row)], fill=(r, g, b))

    # Floor
    draw.rectangle([0, floor_y, W, H - 30], fill=FLOOR_COLOR)
    # Floor shadow at wall base
    for i in range(sp(20)):
        alpha_frac = 1.0 - i / sp(20)
        dark = int(40 * alpha_frac)
        r_ = max(0, FLOOR_COLOR[0] - dark)
        g_ = max(0, FLOOR_COLOR[1] - dark)
        b_ = max(0, FLOOR_COLOR[2] - dark)
        draw.line([(0, floor_y + i), (W, floor_y + i)], fill=(r_, g_, b_))

    # ── CRT monitor on right side ─────────────────────────────────────────────
    # Positioned at ~x=0.70W, centered vertically in upper half
    mon_cx = sx(1330)
    mon_cy = sy(440)
    mon_w  = sx(310)
    mon_h  = sy(220)
    mon_x0 = mon_cx - mon_w // 2
    mon_y0 = mon_cy - mon_h // 2
    mon_x1 = mon_cx + mon_w // 2
    mon_y1 = mon_cy + mon_h // 2
    frame_pad = sp(18)

    # Monitor housing (dark plastic)
    draw.rectangle([mon_x0 - frame_pad, mon_y0 - frame_pad,
                    mon_x1 + frame_pad, mon_y1 + frame_pad + sp(30)],
                   fill=(38, 34, 28))
    # Screen glow (BYTE_TEAL gradient — brightest center)
    for step in range(16, 0, -1):
        t = step / 16
        g_r = int(BYTE_TEAL[0] * t * 0.4)
        g_g = int(BYTE_TEAL[1] * t * 0.9)
        g_b = int(BYTE_TEAL[2] * t * 0.95)
        ex = int(mon_w // 2 * t)
        ey = int(mon_h // 2 * t)
        draw.ellipse([mon_cx - ex, mon_cy - ey, mon_cx + ex, mon_cy + ey],
                     fill=(g_r, g_g, g_b))
    # Screen rim
    draw.rectangle([mon_x0, mon_y0, mon_x1, mon_y1],
                   outline=(60, 50, 40), width=sp(3))
    # Screen specular dot (value ceiling guarantee — >= 225)
    spec_x = mon_cx - mon_w // 4
    spec_y = mon_cy - mon_h // 4
    draw.ellipse([spec_x - sp(6), spec_y - sp(4),
                  spec_x + sp(6), spec_y + sp(4)],
                 fill=SPECULAR_CYAN)

    # Monitor stand
    stand_x = mon_cx - sp(14)
    stand_bot = mon_y1 + frame_pad + sp(30)
    draw.rectangle([stand_x, stand_bot, stand_x + sp(28), stand_bot + sp(18)],
                   fill=(50, 44, 36))
    draw.rectangle([stand_x - sp(20), stand_bot + sp(18),
                    stand_x + sp(48), stand_bot + sp(28)],
                   fill=(44, 38, 30))

    # Monitor ambient glow radiating onto wall / floor (BYTE_TEAL spill)
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw  = ImageDraw.Draw(glow_layer)
    glow_steps = 12
    for gs in range(glow_steps, 0, -1):
        t = gs / glow_steps
        alpha = int(55 * t * t)
        gr  = int(BYTE_TEAL[0] * 0.1)
        gg  = int(BYTE_TEAL[1] * 0.85 * t)
        gb  = int(BYTE_TEAL[2] * 0.90 * t)
        ex  = int(mon_w * 0.9 * (1.0 + (1 - t) * 1.5))
        ey  = int(mon_h * 0.9 * (1.0 + (1 - t) * 1.5))
        glow_draw.ellipse([mon_cx - ex, mon_cy - ey, mon_cx + ex, mon_cy + ey],
                          fill=(gr, gg, gb, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # ── Lamp (upper left) — warm domestic source ──────────────────────────────
    lamp_x = sx(200)
    lamp_y = ceiling_y + sy(30)
    # Lamp shade
    shade_pts = [
        (lamp_x - sx(50), lamp_y + sy(40)),
        (lamp_x + sx(50), lamp_y + sy(40)),
        (lamp_x + sx(30), lamp_y),
        (lamp_x - sx(30), lamp_y),
    ]
    draw.polygon(shade_pts, fill=(220, 190, 110))
    draw.polygon(shade_pts, outline=(160, 130, 60), width=sp(2))
    # Lamp base
    draw.rectangle([lamp_x - sp(6), lamp_y + sy(40),
                    lamp_x + sp(6), lamp_y + sy(70)],
                   fill=(140, 110, 60))
    # Warm light halo from lamp
    lamp_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lamp_draw  = ImageDraw.Draw(lamp_layer)
    for ls in range(10, 0, -1):
        t = ls / 10
        alpha = int(40 * t * t)
        ex = int(sx(140) * (1.0 + (1 - t) * 2.0))
        ey = int(sy(100) * (1.0 + (1 - t) * 2.0))
        lamp_draw.ellipse([lamp_x - ex, lamp_y - ey, lamp_x + ex, lamp_y + ey],
                          fill=(255, 200, 80, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, lamp_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    return {
        "ceiling_y":  ceiling_y,
        "floor_y":    floor_y,
        "mon_cx":     mon_cx,
        "mon_cy":     mon_cy,
        "mon_x0":     mon_x0,
        "mon_y0":     mon_y0,
        "mon_x1":     mon_x1,
        "mon_y1":     mon_y1,
        "lamp_x":     lamp_x,
        "lamp_y":     lamp_y,
    }


def draw_luma(img, draw, bg_data):
    """Draw Luma: left-center, standing, facing right toward Byte."""
    rng = random.Random(100)

    luma_cx   = sx(420)
    floor_y   = bg_data["floor_y"]
    # Luma stands ~70% of canvas height above floor (head at ~y=0.30H)
    luma_base = floor_y
    head_r    = sp(64)

    def p(n): return int(n * min(SX, SY))

    # Body height: 3.2 heads. head + neck + torso + legs
    # We draw top-down: determine head position first
    total_body_h = int(head_r * 6.4)   # 3.2 heads * 2 (diameter per head)
    head_cy = luma_base - total_body_h + head_r
    head_cx = luma_cx + sp(12)  # slight lean toward Byte (rightward)

    # ── Legs ──────────────────────────────────────────────────────────────────
    leg_top   = luma_base - int(head_r * 2.5)
    leg_w     = sp(22)
    # Left leg
    draw.rectangle([luma_cx - leg_w - sp(4), leg_top,
                    luma_cx - sp(4),          luma_base],
                   fill=JEANS)
    draw.rectangle([luma_cx - leg_w - sp(4), leg_top,
                    luma_cx - sp(4),          leg_top + sp(8)],
                   fill=JEANS_SH)
    # Right leg
    draw.rectangle([luma_cx + sp(4),     leg_top,
                    luma_cx + leg_w + sp(4), luma_base],
                   fill=JEANS)
    draw.rectangle([luma_cx + sp(4),     leg_top,
                    luma_cx + leg_w + sp(4), leg_top + sp(8)],
                   fill=JEANS_SH)
    # Shoes
    draw.ellipse([luma_cx - leg_w - sp(10), luma_base - sp(6),
                  luma_cx - sp(4) + sp(10),  luma_base + sp(8)],
                 fill=LINE)
    draw.ellipse([luma_cx + sp(4) - sp(4),  luma_base - sp(6),
                  luma_cx + leg_w + sp(14),  luma_base + sp(8)],
                 fill=LINE)

    # ── Torso / Hoodie ────────────────────────────────────────────────────────
    torso_top = luma_base - int(head_r * 4.2)
    torso_bot = luma_base - int(head_r * 2.5)
    torso_hw  = sp(52)
    wobble_polygon(
        draw,
        [(luma_cx - torso_hw, torso_top), (luma_cx + torso_hw, torso_top),
         (luma_cx + torso_hw + sp(6), torso_bot), (luma_cx - torso_hw - sp(6), torso_bot)],
        color=HOODIE_SHADOW,
        width=sp(3),
        amplitude=sp(2),
        frequency=4,
        seed=200,
        fill=HOODIE_ORANGE,
    )
    draw = ImageDraw.Draw(img)

    # Hoodie pixel-pattern stripe (cyan/teal accent on chest)
    stripe_y = torso_top + int((torso_bot - torso_top) * 0.3)
    for px_i in range(0, torso_hw * 2, sp(6)):
        col = px_i % (sp(12))
        if col < sp(6):
            draw.rectangle([luma_cx - torso_hw + px_i, stripe_y,
                            luma_cx - torso_hw + px_i + sp(4), stripe_y + sp(4)],
                           fill=(0, 180, 210))

    # ── Left arm (reaching right toward Byte) ─────────────────────────────────
    arm_x0 = luma_cx + torso_hw
    arm_y0 = torso_top + int((torso_bot - torso_top) * 0.25)
    arm_x1 = arm_x0 + sp(70)
    arm_y1 = arm_y0 + sp(20)
    draw.rectangle([arm_x0, arm_y0, arm_x1, arm_y1 + sp(10)], fill=HOODIE_ORANGE)
    # Hand
    draw.ellipse([arm_x1 - sp(8), arm_y1 - sp(10),
                  arm_x1 + sp(14), arm_y1 + sp(14)],
                 fill=SKIN)

    # ── Right arm (down at side) ──────────────────────────────────────────────
    arm2_x0 = luma_cx - torso_hw - sp(6)
    arm2_y0 = torso_top + int((torso_bot - torso_top) * 0.2)
    arm2_x1 = arm2_x0 - sp(10)
    arm2_y1 = torso_bot + sp(10)
    draw.rectangle([arm2_x1, arm2_y0, arm2_x0, arm2_y1], fill=HOODIE_ORANGE)

    # ── Neck ──────────────────────────────────────────────────────────────────
    neck_w = sp(18)
    draw.rectangle([head_cx - neck_w, torso_top - sp(16),
                    head_cx + neck_w, torso_top + sp(6)],
                   fill=SKIN)

    # ── Head ──────────────────────────────────────────────────────────────────
    # Skin gradient
    for row in range(head_cy - head_r, head_cy + head_r):
        t_y = (row - head_cy) / max(1, head_r)
        rx_row = int(head_r * math.sqrt(max(0, 1 - t_y * t_y)))
        if rx_row < 1:
            continue
        for col in range(head_cx - rx_row, head_cx + rx_row + 1):
            t_x = (col - head_cx) / max(1, rx_row)
            w_f = 0.5 + 0.5 * t_x
            r_v = int(SKIN[0] * (1 - w_f) + SKIN_HL[0] * w_f)
            g_v = int(SKIN[1] * (1 - w_f) + SKIN_HL[1] * w_f)
            b_v = int(SKIN[2] * (1 - w_f) + SKIN_HL[2] * w_f)
            draw.point((col, row), fill=(r_v, g_v, b_v))

    # Head outline (wobble)
    num_pts = 20
    head_pts = []
    for i in range(num_pts):
        angle = (2 * math.pi * i / num_pts) - math.pi / 2
        hx = head_cx + head_r * math.cos(angle)
        hy = head_cy + head_r * math.sin(angle)
        head_pts.append((hx, hy))
    wobble_polygon(draw, head_pts, color=LINE, width=sp(3),
                   amplitude=sp(2), frequency=5, seed=101, fill=None)
    draw = ImageDraw.Draw(img)

    # Variable stroke arcs on head perimeter
    for arc_i in range(8):
        start_a = (2 * math.pi * arc_i / 8) - math.pi / 2
        end_a   = (2 * math.pi * (arc_i + 1) / 8) - math.pi / 2
        a_p1 = (head_cx + (head_r + sp(1)) * math.cos(start_a),
                head_cy + (head_r + sp(1)) * math.sin(start_a))
        a_p2 = (head_cx + (head_r + sp(1)) * math.cos(end_a),
                head_cy + (head_r + sp(1)) * math.sin(end_a))
        variable_stroke(img, a_p1, a_p2,
                        max_width=sp(5), min_width=sp(1),
                        color=LINE, seed=300 + arc_i)
    draw = ImageDraw.Draw(img)

    # Hair
    draw.chord([head_cx - head_r, head_cy - head_r + p(20),
                head_cx + head_r, head_cy + p(20)],
               start=190, end=350, fill=HAIR_COLOR)
    draw.arc([head_cx - head_r, head_cy - head_r + p(20),
              head_cx + head_r, head_cy + p(20)],
             start=190, end=350, fill=LINE, width=p(4))
    # Hair curls (puffs)
    for curl_i, (ca, cr_scale) in enumerate([
        (220, 0.28), (250, 0.24), (280, 0.26), (310, 0.22), (340, 0.24)
    ]):
        ca_rad = math.radians(ca)
        cx_ = head_cx + int(head_r * 0.85 * math.cos(ca_rad))
        cy_ = head_cy + int(head_r * 0.85 * math.sin(ca_rad))
        cr  = int(head_r * cr_scale)
        draw.ellipse([cx_ - cr, cy_ - cr, cx_ + cr, cy_ + cr], fill=HAIR_COLOR)
        draw.ellipse([cx_ - cr, cy_ - cr, cx_ + cr, cy_ + cr],
                     outline=LINE, width=p(3))

    # Eyes (canonical ew = int(head_r * 0.22))
    ew = int(head_r * 0.22)
    eye_y  = head_cy - int(head_r * 0.10)
    eye_lx = head_cx - int(head_r * 0.30)
    eye_rx = head_cx + int(head_r * 0.28)

    EYE_W_C  = (242, 240, 248)
    EYE_IRIS = ( 58,  32,  18)

    for ex_, ey_  in [(eye_lx, eye_y), (eye_rx, eye_y)]:
        draw.ellipse([ex_ - ew, ey_ - int(ew * 1.1),
                      ex_ + ew, ey_ + int(ew * 1.1)],
                     fill=EYE_W_C, outline=LINE, width=p(2))
        draw.ellipse([ex_ - int(ew * 0.55), ey_ - int(ew * 0.55),
                      ex_ + int(ew * 0.55), ey_ + int(ew * 0.55)],
                     fill=EYE_IRIS)
        # Eye specular — value ceiling guarantee (>= 225)
        draw.ellipse([ex_ - int(ew * 0.22), ey_ - int(ew * 0.40),
                      ex_ + int(ew * 0.22), ey_ - int(ew * 0.08)],
                     fill=SPECULAR_WHITE)

    # Blush (#E8A87C canonical)
    blush_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    blush_draw  = ImageDraw.Draw(blush_layer)
    blush_rx = int(head_r * 0.30)
    blush_ry = int(head_r * 0.14)
    blush_y  = eye_y + int(head_r * 0.22)
    blush_draw.ellipse([eye_lx - blush_rx, blush_y - blush_ry,
                        eye_lx + blush_rx, blush_y + blush_ry],
                       fill=(*BLUSH, 65))
    blush_draw.ellipse([eye_rx - blush_rx, blush_y - blush_ry,
                        eye_rx + blush_rx, blush_y + blush_ry],
                       fill=(*BLUSH, 65))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, blush_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Nose hint
    draw.ellipse([head_cx - p(4), head_cy + p(8),
                  head_cx + p(8), head_cy + p(16)],
                 fill=(168, 104, 68))

    # Brows (expressive — slight arch)
    wobble_line(draw,
                (eye_lx - ew, eye_y - int(ew * 1.5)),
                (eye_lx + ew, eye_y - int(ew * 1.1)),
                color=LINE, width=p(3), amplitude=p(2), frequency=3, seed=41)
    wobble_line(draw,
                (eye_rx - ew, eye_y - int(ew * 1.1)),
                (eye_rx + ew, eye_y - int(ew * 1.5)),
                color=LINE, width=p(3), amplitude=p(2), frequency=3, seed=51)

    # Smile (open, curious/delighted)
    mouth_cx = head_cx + p(4)
    mouth_y  = head_cy + int(head_r * 0.38)
    draw.arc([mouth_cx - int(head_r * 0.28), mouth_y - p(12),
              mouth_cx + int(head_r * 0.28), mouth_y + p(12)],
             start=10, end=170, fill=LINE, width=p(3))

    return head_cx, head_cy, head_r


def draw_byte(img, draw, bg_data):
    """Draw Byte: right-center, hovering, facing left toward Luma.
    Byte body = GL-01b #00D4E8 BYTE_TEAL.
    Monitor-face emits cool cyan glow onto near side.
    """
    rng = random.Random(200)

    byte_cx = sx(900)
    floor_y = bg_data["floor_y"]
    # Byte hovers above floor
    byte_cy = floor_y - sp(220)

    # Byte dimensions
    body_rx = sp(68)
    body_ry = sp(80)

    # ── Body fill — GL-01b BYTE_TEAL ──────────────────────────────────────────
    # Gradient body: darker at top, brighter BYTE_TEAL at front-face
    for row in range(byte_cy - body_ry, byte_cy + body_ry):
        t_y = (row - byte_cy) / max(1, body_ry)
        rx_row = int(body_rx * math.sqrt(max(0, 1 - t_y * t_y)))
        if rx_row < 1:
            continue
        for col in range(byte_cx - rx_row, byte_cx + rx_row + 1):
            # Horizontal gradient: left side darker (shadow), right brighter (lit by monitor)
            t_x = (col - byte_cx) / max(1, rx_row)
            # Monitor glow from left (Byte faces left toward Luma)
            # Near side = left face of Byte
            glow_t = max(0.0, -t_x)   # 1.0 at far left, 0.0 at right
            lit_t  = max(0.0,  t_x)   # 1.0 at far right, ambient shadow
            r_v = int(BYTE_TEAL[0] * 0.6 + BYTE_TEAL[0] * 0.4 * (1 - lit_t)
                      + 0 * glow_t)
            g_v = int(BYTE_TEAL[1] * 0.6 + BYTE_TEAL[1] * 0.4 * (1 - lit_t)
                      + int(BYTE_TEAL[1] * 0.4) * glow_t)
            b_v = int(BYTE_TEAL[2] * 0.6 + BYTE_TEAL[2] * 0.4 * (1 - lit_t)
                      + int(BYTE_TEAL[2] * 0.4) * glow_t)
            draw.point((col, row), fill=(r_v, g_v, b_v))

    # Outline
    wobble_polygon(
        draw,
        [(byte_cx + body_rx * math.cos(math.radians(a)),
          byte_cy + body_ry * math.sin(math.radians(a)))
         for a in range(0, 360, 18)],
        color=BYTE_OUTLINE,
        width=sp(3),
        amplitude=sp(2),
        frequency=5,
        seed=210,
        fill=None,
    )
    draw = ImageDraw.Draw(img)

    # ── Antenna ────────────────────────────────────────────────────────────────
    antenna_base_x = byte_cx + sp(10)
    antenna_base_y = byte_cy - body_ry
    antenna_tip_x  = antenna_base_x + sp(8)
    antenna_tip_y  = antenna_base_y - sp(44)
    wobble_line(draw,
                (antenna_base_x, antenna_base_y),
                (antenna_tip_x, antenna_tip_y),
                color=BYTE_OUTLINE, width=sp(3), amplitude=sp(2), frequency=3, seed=221)
    # Antenna ball
    draw.ellipse([antenna_tip_x - sp(8), antenna_tip_y - sp(8),
                  antenna_tip_x + sp(8), antenna_tip_y + sp(8)],
                 fill=ELEC_CYAN, outline=BYTE_OUTLINE, width=sp(2))
    # Antenna specular (>= 225)
    draw.ellipse([antenna_tip_x - sp(3), antenna_tip_y - sp(5),
                  antenna_tip_x + sp(3), antenna_tip_y - sp(1)],
                 fill=SPECULAR_WHITE)

    # ── Arms ───────────────────────────────────────────────────────────────────
    # Left arm (facing Luma — reaching out slightly)
    arm_lx0 = byte_cx - body_rx
    arm_ly0 = byte_cy + sp(10)
    arm_lx1 = arm_lx0 - sp(50)
    arm_ly1 = arm_ly0 + sp(12)
    draw.rectangle([arm_lx1, arm_ly0 - sp(10), arm_lx0, arm_ly1 + sp(10)],
                   fill=BYTE_TEAL)
    draw.rectangle([arm_lx1, arm_ly0 - sp(10), arm_lx0, arm_ly1 + sp(10)],
                   outline=BYTE_OUTLINE, width=sp(2))
    # Hand (left)
    draw.ellipse([arm_lx1 - sp(14), arm_ly1 - sp(14),
                  arm_lx1 + sp(6),  arm_ly1 + sp(6)],
                 fill=BYTE_TEAL, outline=BYTE_OUTLINE, width=sp(2))

    # Right arm (at side)
    arm_rx0 = byte_cx + body_rx
    arm_ry0 = byte_cy + sp(10)
    arm_rx1 = arm_rx0 + sp(36)
    arm_ry1 = arm_ry0 + sp(40)
    draw.rectangle([arm_rx0, arm_ry0 - sp(10), arm_rx1, arm_ry1],
                   fill=BYTE_TEAL)
    draw.rectangle([arm_rx0, arm_ry0 - sp(10), arm_rx1, arm_ry1],
                   outline=BYTE_OUTLINE, width=sp(2))

    # ── Face / Display screen ─────────────────────────────────────────────────
    face_rx = int(body_rx * 0.62)
    face_ry = int(body_ry * 0.58)
    face_x0 = byte_cx - face_rx
    face_y0 = byte_cy - face_ry
    face_x1 = byte_cx + face_rx
    face_y1 = byte_cy + face_ry

    # Screen backing (dark border)
    draw.rounded_rectangle([face_x0 - sp(4), face_y0 - sp(4),
                             face_x1 + sp(4), face_y1 + sp(4)],
                            radius=sp(8), fill=VOID_BLACK)
    # Screen glow (BYTE_TEAL monitor contribution — requirement)
    for gs in range(10, 0, -1):
        t = gs / 10
        g_r = int(BYTE_TEAL[0] * 0.15 * t)
        g_g = int(BYTE_TEAL[1] * 0.85 * t)
        g_b = int(BYTE_TEAL[2] * 0.90 * t)
        ex  = int(face_rx * t)
        ey  = int(face_ry * t)
        draw.ellipse([byte_cx - ex, byte_cy - ey, byte_cx + ex, byte_cy + ey],
                     fill=(g_r, g_g, g_b))

    # Eye pixel grid (5x5 system)
    # Left eye: standard open (Byte facing left)
    def draw_pixel_eye(ex_center, ey_center, pattern, color, bg_color=VOID_BLACK, cell=sp(8)):
        """Draw a 5x5 pixel grid eye from a pattern string (0=off,1=on,H=half)."""
        ox = ex_center - cell * 2
        oy = ey_center - cell * 2
        for row_i, row_str in enumerate(pattern):
            for col_i, ch in enumerate(row_str):
                px = ox + col_i * cell
                py = oy + row_i * cell
                if ch == '1':
                    draw.rectangle([px, py, px + cell - 1, py + cell - 1], fill=color)
                elif ch == 'H':
                    mid_c = tuple(int((a + b) / 2) for a, b in zip(color, bg_color))
                    draw.rectangle([px, py, px + cell - 1, py + cell - 1], fill=mid_c)

    # Open eye pattern (5 rows, 5 cols)
    eye_pattern_open = [
        "01110",
        "11111",
        "11111",
        "11111",
        "01110",
    ]
    eye_cy_ = byte_cy - int(body_ry * 0.12)
    eye_lx_ = byte_cx - int(body_rx * 0.36)
    eye_rx_ = byte_cx + int(body_rx * 0.30)
    draw_pixel_eye(eye_lx_, eye_cy_, eye_pattern_open, ELEC_CYAN)
    # Right eye: crescent (right eye is damaged — HOT_MAGENTA accent)
    eye_pattern_mag = [
        "00000",
        "01100",
        "11100",
        "01110",
        "00110",
    ]
    draw_pixel_eye(eye_rx_, eye_cy_, eye_pattern_mag, HOT_MAGENTA)

    # Screen specular dot (value ceiling >= 225)
    draw.ellipse([byte_cx - face_rx + sp(8), byte_cy - face_ry + sp(6),
                  byte_cx - face_rx + sp(16), byte_cy - face_ry + sp(12)],
                 fill=SPECULAR_CYAN)

    # ── Monitor contribution glow on Byte's near (left) side ────────────────
    # Byte faces left toward Luma; monitor glow spills onto Byte's right flank
    # "near side" = the side facing the monitor = right side of Byte body
    mon_glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    mon_glow_draw  = ImageDraw.Draw(mon_glow_layer)
    # Paint BYTE_TEAL glow on right side of Byte
    for gs in range(8, 0, -1):
        t = gs / 8
        alpha = int(50 * t * t)
        ex  = int(body_rx * 0.8 * (2.0 - t))
        ey  = int(body_ry * 0.5 * (2.0 - t))
        mon_glow_draw.ellipse([byte_cx, byte_cy - ey, byte_cx + ex, byte_cy + ey],
                              fill=(*BYTE_TEAL, alpha))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, mon_glow_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Hover shadow on floor
    shadow_y = floor_y + sp(6)
    shadow_rx = int(body_rx * 0.85)
    shadow_ry = sp(12)
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow_draw  = ImageDraw.Draw(shadow_layer)
    shadow_draw.ellipse([byte_cx - shadow_rx, shadow_y - shadow_ry,
                         byte_cx + shadow_rx, shadow_y + shadow_ry],
                        fill=(20, 20, 15, 80))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, shadow_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    return byte_cx, byte_cy


def generate():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    img  = Image.new("RGB", (W, H), WARM_CREAM)
    draw = ImageDraw.Draw(img)

    # STEP 1: Background (room + monitor + lamp)
    bg_data = draw_background(img, draw)
    draw = ImageDraw.Draw(img)

    # STEP 2: Luma
    luma_head_cx, luma_head_cy, luma_head_r = draw_luma(img, draw, bg_data)
    draw = ImageDraw.Draw(img)

    # STEP 3: Luma face lighting — warm upper-left lamp
    add_face_lighting(
        img,
        face_center=(luma_head_cx, luma_head_cy),
        face_radius=(luma_head_r, luma_head_r),
        light_dir=(-1.0, -1.0),           # upper-left lamp
        shadow_color=SKIN_SH,
        highlight_color=SKIN_HL,
        seed=500,
    )
    draw = ImageDraw.Draw(img)

    # STEP 4: Luma rim light — cool CRT/monitor teal from right
    # char_cx = luma_head_cx so mask is x > luma_head_cx (character-relative)
    add_rim_light(
        img,
        threshold=185,
        light_color=(0, 212, 232),          # BYTE_TEAL rim
        width=sp(3),
        side="right",
        char_cx=luma_head_cx,              # character-relative split
    )
    draw = ImageDraw.Draw(img)

    # STEP 5: Byte
    byte_cx, byte_cy = draw_byte(img, draw, bg_data)
    draw = ImageDraw.Draw(img)

    # STEP 6: Byte rim light — warm lamp glow from left (lamp is at left)
    # Byte's left side faces the warm lamp; right side faces the monitor wall
    add_rim_light(
        img,
        threshold=185,
        light_color=(255, 200,  80),        # warm amber lamp rim
        width=sp(2),
        side="left",
        char_cx=byte_cx,                   # character-relative split
    )
    draw = ImageDraw.Draw(img)

    # STEP 7: Interaction energy — small spark / connection between Luma's hand
    # and Byte's outstretched arm
    spark_x = int((luma_head_cx + sp(130) + byte_cx - sp(68)) / 2)
    spark_y = int(bg_data["floor_y"] - sp(180))
    spark_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    spark_draw  = ImageDraw.Draw(spark_layer)
    for gs in range(8, 0, -1):
        t = gs / 8
        alpha = int(120 * t * t)
        ex = int(sp(30) * (2.0 - t))
        ey = int(sp(20) * (2.0 - t))
        spark_draw.ellipse([spark_x - ex, spark_y - ey, spark_x + ex, spark_y + ey],
                           fill=(200, 248, 255, alpha))
    # Bright spark core (value ceiling >= 225)
    spark_draw.ellipse([spark_x - sp(6), spark_y - sp(4),
                        spark_x + sp(6), spark_y + sp(4)],
                       fill=(*SPECULAR_WHITE, 200))
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, spark_layer)
    img.paste(base_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # STEP 8: Top/bottom vignette
    vignette = Image.new("RGB", (W, H), (0, 0, 0))
    v_alpha  = Image.new("L", (W, H), 0)
    v_draw   = ImageDraw.Draw(v_alpha)
    for i in range(60):
        t = 1.0 - i / 60.0
        alpha_val = int(70 * t)
        v_draw.line([(0, i), (W, i)], fill=alpha_val)
        v_draw.line([(0, H - 1 - i), (W, H - 1 - i)], fill=alpha_val)
    img = Image.composite(vignette, img, v_alpha)
    draw = ImageDraw.Draw(img)

    # STEP 9: Title strip
    font_xs = load_font(11)
    draw.rectangle([0, H - 30, W, H], fill=(20, 12, 8))
    draw.text((10, H - 22),
              "LUMA & THE GLITCHKIN — Frame 04: The Dynamic  |  C32 — Full Rebuild v004",
              fill=(180, 150, 100), font=font_xs)

    # STEP 10: Image size rule (already 1280×720 — no resize needed)
    if img.width > 1280 or img.height > 1280:
        img.thumbnail((1280, 1280), Image.LANCZOS)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  ({img.width}x{img.height})")

    # Verify value ceiling
    import colorsys
    pixels = list(img.getdata())
    max_brightness = max(max(r, g, b) for r, g, b in pixels)
    print(f"Value ceiling (max channel): {max_brightness}  (need >= 225)")
    if max_brightness >= 225:
        print("  VALUE CEILING: PASS")
    else:
        print("  VALUE CEILING: FAIL")

    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
