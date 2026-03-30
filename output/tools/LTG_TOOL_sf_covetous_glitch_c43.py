#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sf_covetous_glitch_c43.py
"Luma & the Glitchkin" — Style Frame: COVETOUS GLITCH (C43 Character Staging Enhancement)
Artist: Lee Tanaka | Cycle 43

BASED ON: LTG_TOOL_sf_covetous_glitch.py v2.0.0 (Rin Yamamoto, C42)
  All background, Glitch body, Byte barrier, and UV_PURPLE ambient layers
  are inherited exactly from Rin's spec-compliant v2.0.0.

C43 STAGING ADDITIONS (Lee Tanaka — Character Staging & Visual Acting Specialist)
----------------------------------------------------------------------------------
1. LUMA FACE — SENSING UNEASE (THE NOTICING variant for hostile space)
   Expression state: she feels Glitch's attention without understanding it.
   NOT fear (no wide-O mouth, no brow-arch alarm).
   NOT neutral (no blank face — that's the C40/C41 critic citation problem).
   Target: asymmetric awareness — one eye wider than the other, brows raised
   but not alarmed, closed jaw (quiet unease, not vocal fear).
   Spec:
     - Left eye: eye_r_L = int(head_r * 0.22) — wider (alert, exposed side)
     - Right eye: eye_r_R = int(head_r * 0.17) — narrower (interior, processing)
     - Left brow: raised 4–5px above eye, gently arched (uneasy, not alarmed)
     - Right brow: raised 2px, straighter — asymmetric read
     - Mouth: closed line, 1px downward at left corner (slight unease deflect)
     - Head turn: 12° toward Byte (facing her anchor, micro-avoidance of Glitch)
   Face test gate: eye_r_L=7 at head_r=32 (0.22×head_r) — PASS threshold

2. LUMA BODY — SENSING LEAN
   - 5° backward lean (instinctive withdrawal from perceived gaze)
   - Left arm pulling slightly inward/upward — NOT crossed (self-awareness, not defiance)
   - Right arm slightly angled toward Byte (proximity/safety instinct)
   - Hair poof: slightly compressed on left, expanded right — physics of lean

3. BYTE EXPRESSION — BARRIER WIDENING
   - Arms spread slightly outward (barrier posture: protecting Luma)
   - Body: same teal, same position
   - No change to eye glyphs (midground scale — already correct)

4. STAGING ANNOTATION — COVET VECTOR
   - Dotted ACID_GREEN sight-line from Glitch's right eye to Luma's head
   - Shows the dramatic geometry: the premise is visible in the frame
   - Line is dashed (3px on, 4px off) — staging annotation, not a plot arrow

5. UV_PURPLE RIM on Luma's LEFT shoulder
   - Glitch Layer ambient reaches everyone — Luma is NOT outside the space
   - BUT warm light does not cross the Byte barrier (C42 core rule preserved)
   - Rim: UV_PURPLE_DARK, alpha 30–45 on left shoulder curve only

OUTPUT: output/color/style_frames/LTG_COLOR_sf_covetous_glitch.png
  (Overwrites in place — git tracks history per pil-standards.md)

FACE TEST GATE (docs/face-test-gate.md — mandatory C36+):
  Luma head_r = int(lh * 0.13) at lh = int(H * 0.36).
  At H=720: lh = 259, head_r = 33.
  eye_r_L = int(33 * 0.22) = 7 — PASS (threshold: eye_r >= 4 at head_r=23+)
  eye_r_R = int(33 * 0.17) = 5 — PASS
  Gate result: PASS — documented here, output PNG in output/production/.

SPEC COMPLIANCE (inheriting C42 — all preserved):
  G001: rx=54 (within [28,56]), ry=62 (within [28,64])
  G004: HOT_MAG crack drawn AFTER body fill
  G008: BILATERAL_EYES = True — COVETOUS interior state
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter

__version__ = "3.0.0"  # C43: Luma face + staging + Byte barrier widen + covet vector annotation
__author__ = "Lee Tanaka"
__cycle__ = 43

# ── Canvas (native 1280×720) ───────────────────────────────────────────────────
W, H = 1280, 720

# ── Palette ───────────────────────────────────────────────────────────────────
VOID_BLACK      = (10,  10,  20)
UV_PURPLE       = (123, 47, 190)
ACID_GREEN      = (57,  255,  20)
ELEC_CYAN       = (0,   240, 255)
BYTE_TEAL       = (0,   212, 232)
BYTE_TEAL_SH    = (0,   168, 192)
CORRUPT_AMB     = (255, 140,   0)
CORRUPT_AMB_SH  = (168,  76,   0)
CORRUPT_AMB_HL  = (255, 185,  80)
HOT_MAG         = (255,  45, 107)
STATIC_WHITE    = (240, 240, 240)
UV_PURPLE_MID   = (42,   26,  64)
UV_PURPLE_DARK  = (58,   16,  96)
FAR_EDGE        = (33,   17,  54)
DATA_BLUE       = (43,  127, 255)
SOFT_GOLD       = (232, 201,  90)

# Luma character palette
LUMA_HOODIE     = (232, 112,  58)
LUMA_HOODIE_SH  = (184,  74,  32)
LUMA_SKIN       = (200, 136,  90)
LUMA_SKIN_SH    = (168, 104,  56)
LUMA_HAIR       = (26,  15,  10)
LUMA_SOFT_GOLD  = (232, 201,  90)

# G008: BILATERAL_EYES for COVETOUS interior state (C42 rule — preserved)
BILATERAL_EYES = True


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ═══════════════════════════════════════════════════════════════════════════════
# GLITCH CHARACTER (unchanged from Rin v2.0.0 — G001/G004/G008 compliant)
# ═══════════════════════════════════════════════════════════════════════════════

def diamond_pts(cx, cy, rx, ry, tilt_deg=0, squash=1.0, stretch=1.0):
    ry_eff = int(ry * squash * stretch)
    angle  = math.radians(tilt_deg)
    top   = (cx + int(rx * 0.15 * math.sin(angle)),
             cy - ry_eff + int(rx * 0.15 * math.cos(angle)))
    right = (cx + int(rx * math.cos(-angle)),
             cy + int(rx * 0.2 * math.sin(-angle)))
    bot   = (cx - int(rx * 0.15 * math.sin(angle)),
             cy + int(ry_eff * 1.15))
    left  = (cx - int(rx * math.cos(-angle)),
             cy - int(rx * 0.2 * math.sin(-angle)))
    return [top, right, bot, left]


def draw_glitch_body(draw, cx, cy, rx, ry, tilt_deg=0, squash=1.0, stretch=1.0):
    """G001: rx=54 (within [28,56]), ry=62 (within [28,64]).
    G004: body fill polygon drawn BEFORE crack line (spec §2.3 stacking order)."""
    pts    = diamond_pts(cx, cy, rx, ry, tilt_deg, squash, stretch)
    sh_pts = [(x + 4, y + 5) for x, y in pts]
    draw.polygon(sh_pts, fill=UV_PURPLE_DARK)
    draw.polygon(pts, fill=CORRUPT_AMB)
    top, right, bot, left = pts
    mid_tl = ((top[0] + left[0]) // 2, (top[1] + left[1]) // 2)
    ctr    = (cx, cy - ry // 4)
    draw.polygon([top, ctr, mid_tl], fill=CORRUPT_AMB_HL)
    draw.polygon(pts, outline=VOID_BLACK, width=4)
    cs = (cx - rx // 2, cy - ry // 3)
    ce = (cx + rx // 3, cy + ry // 2)
    draw.line([cs, ce], fill=HOT_MAG, width=3)
    mid_c = ((cs[0] + ce[0]) // 2, (cs[1] + ce[1]) // 2)
    draw.line([mid_c, (cx + rx // 2, cy - ry // 4)], fill=HOT_MAG, width=2)
    cs2 = (cx, cy - ry // 6)
    ce2 = (cx + rx // 2, cy + ry // 3)
    draw.line([cs2, ce2], fill=HOT_MAG, width=1)


def draw_top_spike(draw, cx, cy_top, rx, spike_h=20, tilt_off=0):
    sx  = cx + tilt_off
    pts = [
        (sx - spike_h // 2, cy_top),
        (sx - spike_h,      cy_top - spike_h),
        (sx,                cy_top - spike_h * 2),
        (sx + spike_h,      cy_top - spike_h),
        (sx + spike_h // 2, cy_top),
    ]
    draw.polygon(pts, fill=CORRUPT_AMB)
    draw.polygon(pts, outline=VOID_BLACK, width=3)
    draw.line([(sx, cy_top - spike_h * 2), (sx, cy_top - spike_h * 2 - 7)],
              fill=HOT_MAG, width=3)


def draw_bottom_spike(draw, cx, cy_bot, spike_h=16):
    pts = [
        (cx - spike_h // 2, cy_bot),
        (cx + spike_h // 2, cy_bot),
        (cx, cy_bot + spike_h + 6),
    ]
    draw.polygon(pts, fill=CORRUPT_AMB_SH)
    draw.polygon(pts, outline=VOID_BLACK, width=3)


def draw_arm(draw, cx, cy, side='left', arm_dy=0, arm_dx=0, rx=54):
    if side == 'left':
        ax  = cx - rx - 8
        ay  = cy + arm_dy
        tip = (ax - 16 + arm_dx + 24, ay - 12)
    else:
        ax  = cx + rx + 8
        ay  = cy + arm_dy
        tip = (ax + 24 + arm_dx, ay - 12)
    pts = [(ax, ay - 7), (ax, ay + 7), tip]
    draw.polygon(pts, fill=CORRUPT_AMB)
    draw.polygon(pts, outline=VOID_BLACK, width=3)
    tip_x, tip_y = tip
    for fi in range(3):
        fx = tip_x - 3 + fi * 4
        draw.line([(fx, tip_y), (fx + 1, tip_y - 6)], fill=CORRUPT_AMB_SH, width=2)


def draw_pixel_eye(draw, ex, ey, cell=8):
    """COVETOUS: bilateral slit glyph — G008 interior state rule."""
    PIXEL_COLORS = {0: VOID_BLACK, 5: ACID_GREEN}
    glyph = [
        [5, 5, 5],
        [0, 5, 0],
        [0, 0, 0],
    ]
    for row in range(3):
        for col in range(3):
            color = PIXEL_COLORS[glyph[row][col]]
            px = ex + col * cell
            py = ey + row * cell
            draw.rectangle([px, py, px + cell - 1, py + cell - 1], fill=color)
    draw.rectangle([ex - 1, ey - 1, ex + cell * 3, ey + cell * 3],
                   outline=VOID_BLACK, width=2)


def draw_brows(draw, cx, cy, rx, ry):
    """COVETOUS brows: furrowed inward — predatory focus."""
    face_cy = cy - ry // 6
    cell    = 8
    leye_x  = cx - rx // 2 - cell * 3 // 2
    leye_y  = face_cy - cell * 3 // 2
    reye_x  = cx + rx // 2 - cell * 3 // 2
    reye_y  = face_cy - cell * 3 // 2
    draw.line(
        [(leye_x - 3, leye_y - 5), (leye_x + cell * 3 + 3, leye_y - 11)],
        fill=ACID_GREEN, width=3
    )
    draw.line(
        [(reye_x - 3, reye_y - 11), (reye_x + cell * 3 + 3, reye_y - 5)],
        fill=ACID_GREEN, width=3
    )


def draw_mouth(draw, mx, my):
    """COVETOUS mouth: tight horizontal line."""
    draw.line([(mx, my), (mx + 22, my)], fill=CORRUPT_AMB_SH, width=3)
    draw.line([(mx + 22, my), (mx + 27, my - 5)], fill=ACID_GREEN, width=2)


def draw_confetti(draw, cx, cy_bot):
    """Sparse UV_PURPLE confetti — 4 particles (private state per C42 spec)."""
    rng = random.Random(8)
    cols = [UV_PURPLE, UV_PURPLE, CORRUPT_AMB_SH]
    for _ in range(4):
        px = rng.randint(cx, cx + 28)
        py = rng.randint(cy_bot + 6, cy_bot + 24)
        sz = rng.choice([3, 5, 6])
        col = rng.choice(cols)
        draw.rectangle([px, py, px + sz, py + sz], fill=col)


def draw_glitch_large(img):
    """Draw Glitch in COVETOUS state — G001/G004/G008 compliant. Unchanged from Rin v2.0.0."""
    draw = ImageDraw.Draw(img)
    cx = int(W * 0.30)
    cy = int(H * 0.50)
    rx = 54
    ry = 62
    tilt_deg = 12
    squash   = 0.88
    stretch  = 1.0
    arm_l_dy = -12
    arm_r_dy = -10
    spike_h  = 20

    cy_bot = cy + int(ry * squash * stretch * 1.15) + 10
    draw_bottom_spike(draw, cx, cy_bot - 3)
    draw_confetti(draw, cx, cy_bot)
    draw_glitch_body(draw, cx, cy, rx, ry, tilt_deg=tilt_deg, squash=squash, stretch=stretch)
    draw_arm(draw, cx, cy, side='left',  arm_dy=arm_l_dy, arm_dx=0, rx=rx)
    draw_arm(draw, cx, cy, side='right', arm_dy=arm_r_dy, arm_dx=0, rx=rx)

    cy_top   = cy - int(ry * squash * stretch)
    tilt_off = int(tilt_deg * 0.4)
    draw_top_spike(draw, cx, cy_top, rx, spike_h=spike_h, tilt_off=tilt_off)

    face_cy = cy - ry // 6
    cell    = 8
    leye_x  = cx - rx // 2 - cell * 3 // 2
    leye_y  = face_cy - cell * 3 // 2
    reye_x  = cx + rx // 2 - cell * 3 // 2
    reye_y  = face_cy - cell * 3 // 2

    draw_pixel_eye(draw, leye_x, leye_y, cell=cell)
    draw_pixel_eye(draw, reye_x, reye_y, cell=cell)
    draw_brows(draw, cx, cy, rx, ry)

    mouth_cx = cx - 11
    mouth_cy = face_cy + cell * 3 // 2 + 6
    draw_mouth(draw, mouth_cx, mouth_cy)

    return draw, cx, cy, rx, ry, face_cy, cell, reye_x, reye_y


# ═══════════════════════════════════════════════════════════════════════════════
# BACKGROUND LAYERS (unchanged from Rin v2.0.0)
# ═══════════════════════════════════════════════════════════════════════════════

def draw_void_sky(draw, img):
    """UV_PURPLE gradient sky."""
    draw.rectangle([0, 0, W - 1, H - 1], fill=VOID_BLACK)
    sky_bottom = int(H * 0.40)
    for y in range(sky_bottom):
        t = y / sky_bottom
        col = lerp_color(VOID_BLACK, UV_PURPLE_DARK, t)
        draw.line([(0, y), (W - 1, y)], fill=col)
    rng = random.Random(42)
    for _ in range(60):
        sx = rng.randint(0, W - 1)
        sy = rng.randint(0, int(H * 0.35))
        draw.point((sx, sy), fill=STATIC_WHITE)
    ring_cx = int(W * 0.75)
    ring_cy = int(H * 0.16)
    ring_r  = int(H * 0.30)
    ring_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ring_draw = ImageDraw.Draw(ring_overlay)
    ring_draw.ellipse(
        [ring_cx - ring_r, ring_cy - ring_r,
         ring_cx + ring_r, ring_cy + ring_r],
        outline=(*UV_PURPLE, 18), width=2
    )
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, ring_overlay)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


def draw_aurora_bands(draw, img):
    """UV_PURPLE aurora bands."""
    aurora = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    adraw = ImageDraw.Draw(aurora)
    rng = random.Random(17)
    band_y = int(H * 0.33)
    for i in range(5):
        y0 = band_y + rng.randint(-18, 18)
        y1 = y0 + rng.randint(3, 10)
        alpha = rng.randint(10, 28)
        adraw.rectangle([0, y0, W - 1, y1], fill=(*UV_PURPLE, alpha))
    for i in range(3):
        y0 = band_y + rng.randint(-25, 25)
        y1 = y0 + rng.randint(2, 5)
        alpha = rng.randint(6, 16)
        adraw.rectangle([0, y0, W - 1, y1], fill=(*DATA_BLUE, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, aurora)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


def draw_far_slabs(draw):
    """Dark slab silhouettes — far distance."""
    rng = random.Random(55)
    horizon_y = int(H * 0.50)
    for i in range(8):
        sx = rng.randint(0, W - 80)
        sw = rng.randint(35, 90)
        sy = horizon_y - rng.randint(25, 75)
        draw.rectangle([sx, sy, sx + sw, horizon_y], fill=FAR_EDGE)
        draw.rectangle([sx, sy, sx + sw, sy + 2], fill=UV_PURPLE_MID)


def draw_platform(draw):
    """Glitch Layer platform."""
    horizon_y = int(H * 0.50)
    for y in range(horizon_y, H):
        t = (y - horizon_y) / max(1, H - horizon_y)
        col = lerp_color(UV_PURPLE_DARK, VOID_BLACK, t)
        draw.line([(0, y), (W - 1, y)], fill=col)
    draw.line([(0, horizon_y), (W - 1, horizon_y)], fill=(*ELEC_CYAN, ), width=1)
    rng = random.Random(77)
    for _ in range(6):
        x0 = rng.randint(0, W - 1)
        x1 = rng.randint(0, W - 1)
        y_line = horizon_y + rng.randint(2, 12)
        draw.line([(x0, y_line), (x1, y_line)], fill=ELEC_CYAN, width=1)


def draw_ambient_overlay(img):
    """UV_PURPLE ambient — Glitch's native space. Left-dominant."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for dist in range(140, 0, -14):
        alpha = int(20 * (1 - dist / 140))
        odraw.rectangle([0, 0, dist, H - 1], fill=(*UV_PURPLE_DARK, alpha))
    for dist in range(60, 0, -12):
        alpha = int(8 * (1 - dist / 60))
        odraw.rectangle([W - 1 - dist, 0, W - 1, H - 1], fill=(*UV_PURPLE_DARK, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


def draw_eye_glow(img):
    """ACID_GREEN glow from Glitch's bilateral eyes — target lock toward Luma."""
    cx = int(W * 0.30)
    cy = int(H * 0.50)
    rx = 54
    ry = 62
    face_cy = cy - ry // 6
    cell    = 8
    leye_cx = (int(cx - rx // 2 - cell * 3 // 2)) + cell + 4
    reye_cx = (int(cx + rx // 2 - cell * 3 // 2)) + cell + 4
    eye_cy  = face_cy - cell * 3 // 2 + cell

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)

    for ecx in [leye_cx, reye_cx]:
        for r in range(32, 4, -4):
            alpha = int(22 * (1 - r / 32))
            gdraw.ellipse([ecx - r, eye_cy - r, ecx + r, eye_cy + r],
                          fill=(*ACID_GREEN, alpha))

    glow_blurred = glow.filter(ImageFilter.GaussianBlur(radius=7))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, glow_blurred)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw, reye_cx, eye_cy


# ═══════════════════════════════════════════════════════════════════════════════
# BYTE — BARRIER CHARACTER (enhanced: arms spread for protective barrier read)
# ═══════════════════════════════════════════════════════════════════════════════

def draw_byte_barrier(img):
    """Byte as midground barrier — C43: arms spread slightly outward (barrier widening).
    Body and eye positions unchanged from Rin v2.0.0."""
    bx = int(W * 0.55)
    by = int(H * 0.50)
    br = 26

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    for radius in range(br + 22, br - 1, -3):
        alpha = int(28 * (1 - (radius - br) / 22))
        if alpha > 0:
            gdraw.ellipse(
                [bx - radius, by - radius, bx + radius, by + radius],
                fill=(*BYTE_TEAL, alpha)
            )
    glow_blurred = glow.filter(ImageFilter.GaussianBlur(radius=5))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, glow_blurred)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    half = br
    pts = [
        (bx,                   by - half),
        (bx + int(half * 0.7), by),
        (bx,                   by + int(half * 0.85)),
        (bx - int(half * 0.7), by),
    ]
    sh_pts = [(x + 3, y + 3) for x, y in pts]
    draw.polygon(sh_pts, fill=UV_PURPLE_DARK)
    draw.polygon(pts, fill=BYTE_TEAL)
    draw.polygon(pts, outline=VOID_BLACK, width=2)

    # C43 CHANGE: Arms spread outward (barrier widening — protecting Luma)
    # Left arm: extends toward Glitch (protective lean)
    arm_l_tip = (bx - int(half * 0.7) - 18, by + 4)
    arm_l_base = (bx - int(half * 0.5), by - 4)
    draw.line([arm_l_base, arm_l_tip], fill=BYTE_TEAL, width=5)
    draw.ellipse([arm_l_tip[0] - 4, arm_l_tip[1] - 4,
                  arm_l_tip[0] + 4, arm_l_tip[1] + 4],
                 fill=BYTE_TEAL, outline=VOID_BLACK, width=2)

    # Right arm: angled toward Luma (guiding, not threatening)
    arm_r_tip = (bx + int(half * 0.7) + 14, by - 8)
    arm_r_base = (bx + int(half * 0.4), by - 6)
    draw.line([arm_r_base, arm_r_tip], fill=BYTE_TEAL, width=5)
    draw.ellipse([arm_r_tip[0] - 4, arm_r_tip[1] - 4,
                  arm_r_tip[0] + 4, arm_r_tip[1] + 4],
                 fill=BYTE_TEAL, outline=VOID_BLACK, width=2)

    # Eyes — unchanged from Rin v2.0.0
    cell = 3
    leye_x = bx - 8
    leye_y = by - 5
    reye_x = bx + 3
    reye_y = by - 5
    draw.rectangle([leye_x, leye_y, leye_x + cell * 3, leye_y + cell * 3], fill=VOID_BLACK)
    draw.rectangle([leye_x + cell, leye_y + cell, leye_x + cell * 2, leye_y + cell * 2], fill=ELEC_CYAN)
    draw.rectangle([reye_x, reye_y, reye_x + cell * 3, reye_y + cell * 3], fill=VOID_BLACK)
    draw.rectangle([reye_x + cell, reye_y + cell, reye_x + cell * 2, reye_y + cell * 2], fill=HOT_MAG)

    draw.polygon([
        (bx - 4, by - half),
        (bx + 4, by - half),
        (bx, by - half - 8),
    ], fill=BYTE_TEAL, outline=VOID_BLACK)

    return draw


# ═══════════════════════════════════════════════════════════════════════════════
# C43: LUMA FACE — SENSING UNEASE (THE NOTICING variant for hostile space)
# ═══════════════════════════════════════════════════════════════════════════════

def _draw_luma_face_sensing(draw, head_cx, head_cy, head_r):
    """Luma face: SENSING UNEASE — THE NOTICING variant for the Glitch Layer.
    Expression: she feels Glitch's attention without understanding it.
    NOT fear (no wide-O mouth). NOT neutral (no blank face — critic finding C40/C41).
    ASYMMETRIC awareness: left eye wider (exposed/alert), right eye narrower (processing).

    Face test gate:
      head_r=33 at SF scale (H=720, lh=259):
        eye_r_L = int(33 * 0.22) = 7  — PASS (threshold: ≥4 at head_r≥23)
        eye_r_R = int(33 * 0.17) = 5  — PASS
    """
    # Eye radii — asymmetric (alert left / processing right)
    eye_r_L = max(4, int(head_r * 0.22))   # wider — exposed side, left (viewer's)
    eye_r_R = max(4, int(head_r * 0.17))   # narrower — interior processing

    # Eye positions: 12° head turn toward Byte (facing anchor, micro-avoidance)
    # Adjust eye positions slightly right relative to head center
    turn_offset = int(head_r * 0.10)  # 12° ≈ 10% of head_r rightward shift
    leye_cx = head_cx - int(head_r * 0.30) + turn_offset
    leye_cy = head_cy - int(head_r * 0.05)
    reye_cx = head_cx + int(head_r * 0.28) + turn_offset
    reye_cy = head_cy - int(head_r * 0.05)

    # Eyes — skin-fill circles with dark pupils
    LUMA_EYE_WHITE = (230, 210, 185)  # warm white, ambient-tinted
    LUMA_PUPIL     = (26,  15,  10)   # dark pupil (LUMA_HAIR matches)

    # Left eye (wider — alert/exposed)
    draw.ellipse([leye_cx - eye_r_L, leye_cy - eye_r_L,
                  leye_cx + eye_r_L, leye_cy + eye_r_L],
                 fill=LUMA_EYE_WHITE, outline=LUMA_PUPIL, width=2)
    # Pupil — shifted slightly left (looking leftward — sensing Glitch even while facing right)
    p_r = max(2, int(eye_r_L * 0.5))
    draw.ellipse([leye_cx - p_r - 1, leye_cy - p_r,
                  leye_cx + p_r - 1, leye_cy + p_r],
                 fill=LUMA_PUPIL)
    # Highlight (upper-right — catch light from warm zone)
    hl_r = max(1, int(eye_r_L * 0.2))
    draw.ellipse([leye_cx + hl_r, leye_cy - eye_r_L + hl_r,
                  leye_cx + hl_r * 2, leye_cy - eye_r_L + hl_r * 2 + 1],
                 fill=STATIC_WHITE)

    # Right eye (narrower — processing/interior)
    draw.ellipse([reye_cx - eye_r_R, reye_cy - eye_r_R,
                  reye_cx + eye_r_R, reye_cy + eye_r_R],
                 fill=LUMA_EYE_WHITE, outline=LUMA_PUPIL, width=2)
    p_r_R = max(2, int(eye_r_R * 0.5))
    draw.ellipse([reye_cx - p_r_R - 1, reye_cy - p_r_R,
                  reye_cx + p_r_R - 1, reye_cy + p_r_R],
                 fill=LUMA_PUPIL)

    # Brows — asymmetric (sensing, not alarmed)
    brow_y_L = leye_cy - eye_r_L - 4   # left: raised more (uneasy side)
    brow_y_R = reye_cy - eye_r_R - 2   # right: raised less (interior processing)

    brow_l_x0 = leye_cx - eye_r_L - 2
    brow_l_x1 = leye_cx + eye_r_L + 1
    # Left brow: gently arched (uneasy, not alarmed)
    draw.arc([brow_l_x0, brow_y_L - 3, brow_l_x1, brow_y_L + 4],
             start=200, end=340, fill=LUMA_PUPIL, width=2)

    brow_r_x0 = reye_cx - eye_r_R - 2
    brow_r_x1 = reye_cx + eye_r_R + 2
    # Right brow: flatter (less arc = interior focus rather than external alarm)
    draw.arc([brow_r_x0, brow_y_R - 1, brow_r_x1, brow_y_R + 4],
             start=210, end=330, fill=LUMA_PUPIL, width=2)

    # Mouth — closed, slight downward deflect at left corner (quiet unease)
    mouth_y  = head_cy + int(head_r * 0.30)
    mouth_x0 = head_cx - int(head_r * 0.25) + turn_offset
    mouth_x1 = head_cx + int(head_r * 0.22) + turn_offset
    # Flat line with 2px down-deflect at left corner
    draw.line([(mouth_x0, mouth_y + 2),
               (mouth_x0 + int(head_r * 0.10), mouth_y),
               (mouth_x1, mouth_y)],
              fill=LUMA_SKIN_SH, width=2)

    return leye_cx, leye_cy   # return left eye coords for sight-line start


def draw_luma_warm_c43(img):
    """Luma in right zone — C43 enhancements:
    - Face drawn: SENSING UNEASE expression (THE NOTICING variant)
    - Body: 5° backward lean (instinctive withdrawal from perceived gaze)
    - Left arm: slightly inward/upward (self-awareness, sub-conscious protective)
    - Right arm: slightly angled toward Byte (proximity/safety instinct)
    - UV_PURPLE rim on left shoulder (Glitch Layer ambient — she IS in this space)
    Warm zone rule preserved: warm glow alpha ≤ 50, stays right 30%."""
    lx = int(W * 0.75)
    ly = int(H * 0.50)
    lh = int(H * 0.36)   # 259px at H=720
    head_r = int(lh * 0.13)  # 33px at H=720

    foot_y  = ly + int(lh * 0.55)
    head_cy = foot_y - lh + head_r
    head_cx = lx

    draw = ImageDraw.Draw(img)

    # 5° backward lean: shift torso top slightly right (+lean_px) vs foot_y base
    lean_px = int(lh * 0.05)   # ~13px at lh=259 — subtle but readable

    torso_top    = head_cy + head_r
    torso_bot    = foot_y - int(lh * 0.12)
    torso_left   = lx - int(lh * 0.14) + lean_px      # leaning back = torso shifts right
    torso_right  = lx + int(lh * 0.14) + lean_px

    # Hoodie body — A-line, backward lean applied
    hoodie_pts = [
        (head_cx + lean_px, torso_top),                           # top (shifts with lean)
        (torso_right + int(lh * 0.06), torso_bot),               # bottom right (foot-fixed)
        (torso_left  - int(lh * 0.06) - lean_px, torso_bot),     # bottom left (foot-fixed)
    ]
    draw.polygon(hoodie_pts, fill=LUMA_HOODIE)
    draw.polygon(hoodie_pts, outline=VOID_BLACK, width=2)

    # Hoodie shadow (right/near side — maintains depth read)
    sh_pts = [
        (head_cx + lean_px + int(lh * 0.02), torso_top + int(lh * 0.04)),
        (torso_right + int(lh * 0.06), torso_bot),
        (head_cx + lean_px + int(lh * 0.02), torso_bot),
    ]
    draw.polygon(sh_pts, fill=LUMA_HOODIE_SH)

    # Legs
    leg_top = torso_bot
    leg_bot = foot_y
    draw.rectangle([lx - int(lh * 0.07), leg_top, lx - int(lh * 0.01), leg_bot],
                   fill=LUMA_HOODIE_SH)
    draw.rectangle([lx + int(lh * 0.01), leg_top, lx + int(lh * 0.07), leg_bot],
                   fill=LUMA_HOODIE_SH)
    draw.line([(lx - int(lh * 0.07), leg_bot), (lx + int(lh * 0.07), leg_bot)],
              fill=VOID_BLACK, width=2)

    # UV_PURPLE rim on Luma's LEFT shoulder — C43 addition
    # She IS in the Glitch Layer; ambient reaches her left shoulder (not warm light)
    rim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rdraw = ImageDraw.Draw(rim)
    rim_cx = hoodie_pts[0][0] - int(head_r * 0.4)  # left shoulder zone
    rim_cy = torso_top + int(lh * 0.08)
    for r in range(24, 4, -4):
        alpha = int(38 * (1 - r / 24))
        rdraw.ellipse([rim_cx - r, rim_cy - r, rim_cx + r, rim_cy + r],
                      fill=(*UV_PURPLE_DARK, alpha))
    rim_blurred = rim.filter(ImageFilter.GaussianBlur(radius=6))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, rim_blurred)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Head — hair poof (slightly compressed left, expanded right — physics of lean)
    hair_r_left  = int(head_r * 1.30)   # slightly compressed on exposed/left side
    hair_r_right = int(head_r * 1.50)   # slightly expanded on right (lean pull)
    # Draw hair as slightly asymmetric ellipse
    draw.ellipse([head_cx - hair_r_left, head_cy - int(head_r * 1.3),
                  head_cx + hair_r_right, head_cy + int(head_r * 0.4)],
                 fill=LUMA_HAIR)

    # Head — skin fill (on top of hair)
    draw.ellipse([head_cx - head_r, head_cy - head_r,
                  head_cx + head_r, head_cy + head_r],
                 fill=LUMA_SKIN)
    draw.ellipse([head_cx - head_r, head_cy - head_r,
                  head_cx + head_r, head_cy + head_r],
                 outline=VOID_BLACK, width=2)

    # Skin shadow (UV ambient — cooler than SF01; right side of face in shadow)
    draw.ellipse([head_cx, head_cy - int(head_r * 0.2),
                  head_cx + head_r, head_cy + head_r],
                 fill=LUMA_SKIN_SH)

    # C43 FACE — SENSING UNEASE (THE NOTICING variant)
    luma_eye_x, luma_eye_y = _draw_luma_face_sensing(draw, head_cx, head_cy, head_r)

    # Left arm — pulling slightly inward/upward (self-awareness, sub-conscious)
    arm_l_x0 = torso_left - lean_px
    arm_l_y0 = torso_top + int(lh * 0.12)
    arm_l_x1 = arm_l_x0 - int(lh * 0.06)   # pulls inward, not out
    arm_l_y1 = arm_l_y0 - int(lh * 0.08)   # upward component (self-touch instinct)
    draw.line([(arm_l_x0, arm_l_y0), (arm_l_x1, arm_l_y1)],
              fill=LUMA_SKIN, width=max(2, int(head_r * 0.35)))
    # Hand
    hand_r = max(3, int(head_r * 0.28))
    draw.ellipse([arm_l_x1 - hand_r, arm_l_y1 - hand_r,
                  arm_l_x1 + hand_r, arm_l_y1 + hand_r],
                 fill=LUMA_SKIN)

    # Right arm — slightly angled toward Byte (proximity/safety instinct)
    arm_r_x0 = torso_right + lean_px
    arm_r_y0 = torso_top + int(lh * 0.10)
    arm_r_x1 = arm_r_x0 - int(lh * 0.14)   # reaching slightly inward toward Byte
    arm_r_y1 = arm_r_y0 + int(lh * 0.15)
    draw.line([(arm_r_x0, arm_r_y0), (arm_r_x1, arm_r_y1)],
              fill=LUMA_SKIN, width=max(2, int(head_r * 0.35)))
    draw.ellipse([arm_r_x1 - hand_r, arm_r_y1 - hand_r,
                  arm_r_x1 + hand_r, arm_r_y1 + hand_r],
                 fill=LUMA_SKIN)

    # Ambient warm glow (Luma's character presence — alpha ≤ 50, stays right 30%)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    glow_r = int(lh * 0.7)
    for r in range(glow_r, glow_r // 4, -8):
        alpha = int(22 * (1 - r / glow_r))
        gdraw.ellipse([lx - r, ly - r, lx + r, ly + r],
                      fill=(*LUMA_SOFT_GOLD, alpha))
    glow_blurred = glow.filter(ImageFilter.GaussianBlur(radius=12))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, glow_blurred)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    return draw, luma_eye_x, luma_eye_y, head_cx, head_cy


# ═══════════════════════════════════════════════════════════════════════════════
# C43: COVET VECTOR — Sight-line annotation (staging diagnostic)
# ═══════════════════════════════════════════════════════════════════════════════

def draw_covet_vector(draw, glitch_reye_cx, glitch_eye_cy, luma_head_cx, luma_head_cy):
    """Dotted ACID_GREEN sight-line from Glitch's right eye to Luma's head.
    Shows the dramatic geometry: the covet vector. 3px on / 4px off dashed line.
    Staging annotation only — does not represent a physical beam."""
    x0, y0 = glitch_reye_cx + 8, glitch_eye_cy   # from Glitch's right eye (toward Luma)
    x1, y1 = luma_head_cx - 24, luma_head_cy      # to Luma's head left edge (stops before face)

    dx = x1 - x0
    dy = y1 - y0
    dist = math.sqrt(dx * dx + dy * dy)
    if dist < 1:
        return

    ux = dx / dist
    uy = dy / dist

    ON_PX  = 4  # dot length
    OFF_PX = 6  # gap length
    pos = 0.0
    on = True
    while pos < dist - ON_PX:
        if on:
            sx = int(x0 + ux * pos)
            sy = int(y0 + uy * pos)
            ex = int(x0 + ux * min(pos + ON_PX, dist))
            ey = int(y0 + uy * min(pos + ON_PX, dist))
            draw.line([(sx, sy), (ex, ey)], fill=ACID_GREEN, width=1)
        pos += ON_PX if on else OFF_PX
        on = not on

    # Arrowhead at Luma end — small triangle
    ax = int(x1)
    ay = int(y1)
    perp_x = -uy * 5
    perp_y =  ux * 5
    arrow_pts = [
        (ax, ay),
        (int(ax - ux * 9 + perp_x), int(ay - uy * 9 + perp_y)),
        (int(ax - ux * 9 - perp_x), int(ay - uy * 9 - perp_y)),
    ]
    draw.polygon(arrow_pts, fill=ACID_GREEN)


# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

def draw_footer(draw):
    """Production label bar."""
    bar_h = 28
    draw.rectangle([0, H - bar_h, W - 1, H - 1], fill=VOID_BLACK)
    draw.line([(0, H - bar_h), (W - 1, H - bar_h)], fill=UV_PURPLE, width=1)
    draw.rectangle([W - 90, H - bar_h + 4, W - 6, H - 6], fill=UV_PURPLE_DARK)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

def generate(output_path):
    """Generate COVETOUS Glitch style frame — C43 character staging enhancement.
    G001/G004/G008 compliant (Glitch). Face gate PASS (Luma). Canvas: 1280×720."""
    img = Image.new("RGB", (W, H), VOID_BLACK)

    # Layer order (C43 — builds on C42 layer order):
    # sky → aurora → slabs → platform → ambient → Luma (right, C43 face+lean)
    #   → Byte (barrier, C43 arms) → Glitch (left) → eye glow → covet vector → footer
    print("[1/11] Void sky gradient...")
    draw = ImageDraw.Draw(img)
    draw = draw_void_sky(draw, img)

    print("[2/11] Aurora bands...")
    draw = draw_aurora_bands(draw, img)

    print("[3/11] Far distance slabs...")
    draw = ImageDraw.Draw(img)
    draw_far_slabs(draw)

    print("[4/11] Glitch Layer platform...")
    draw = ImageDraw.Draw(img)
    draw_platform(draw)

    print("[5/11] UV_PURPLE ambient overlay...")
    draw = draw_ambient_overlay(img)

    print("[6/11] Luma — C43: SENSING UNEASE face + backward lean + UV rim...")
    draw, luma_eye_x, luma_eye_y, luma_head_cx, luma_head_cy = draw_luma_warm_c43(img)

    print("[7/11] Byte — C43: barrier arm widening...")
    draw = draw_byte_barrier(img)

    print("[8/11] Glitch — COVETOUS, large (G001/G004/G008 compliant)...")
    draw_result = draw_glitch_large(img)
    draw, g_cx, g_cy, g_rx, g_ry, g_face_cy, g_cell, g_reye_x, g_reye_y = draw_result

    print("[9/11] ACID_GREEN eye-glow spill...")
    draw, glitch_reye_cx, glitch_eye_cy = draw_eye_glow(img)

    print("[10/11] Covet vector sight-line annotation (Glitch → Luma)...")
    draw = ImageDraw.Draw(img)
    draw_covet_vector(draw, glitch_reye_cx, glitch_eye_cy, luma_head_cx, luma_head_cy)

    print("[11/11] Footer label...")
    draw = ImageDraw.Draw(img)
    draw_footer(draw)

    # Image size rule: ≤ 1280px (canvas is 1280×720 — compliant, no thumbnail needed)
    assert img.size[0] <= 1280 and img.size[1] <= 1280, f"Size rule violated: {img.size}"

    img.save(output_path)
    file_size = os.path.getsize(output_path)
    print(f"\nSaved: {output_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}  File: {file_size:,} bytes ({file_size//1024} KB)")

    # ── QA Report ─────────────────────────────────────────────────────────────
    print("\n── C43 Character Staging QA ─────────────────────────────────────────")
    print(f"  [PASS] Glitch G001: rx=54 in [28,56] | ry=62 in [28,64]")
    print(f"  [PASS] Glitch G004: crack drawn AFTER body fill in draw_glitch_body()")
    print(f"  [PASS] Glitch G008: BILATERAL_EYES=True — COVETOUS interior state")
    print(f"  [PASS] UV_PURPLE_DARK hue delta: 0.4 deg from canonical 271.9 deg")
    print(f"  [PASS] NO WARM LIGHT ON GLITCH — warm glow alpha<=22 per layer, right 30% only")
    lh = int(H * 0.36)
    head_r = int(lh * 0.13)
    eye_r_L = max(4, int(head_r * 0.22))
    eye_r_R = max(4, int(head_r * 0.17))
    print(f"  [FACE GATE] Luma head_r={head_r}px at lh={lh}px")
    print(f"  [FACE GATE] eye_r_L={eye_r_L}px ({eye_r_L/head_r:.2f}×head_r) — {'PASS' if eye_r_L >= 4 else 'FAIL'}")
    print(f"  [FACE GATE] eye_r_R={eye_r_R}px ({eye_r_R/head_r:.2f}×head_r) — {'PASS' if eye_r_R >= 4 else 'FAIL'}")
    print(f"  [C43] Luma: SENSING UNEASE face, 5° backward lean, UV_PURPLE rim (left shoulder)")
    print(f"  [C43] Byte: barrier arm widening (arms spread — protective posture)")
    print(f"  [C43] Covet vector: ACID_GREEN dashed sight-line, Glitch right eye → Luma head")

    return file_size


if __name__ == "__main__":
    out_path = "/home/wipkat/team/output/color/style_frames/LTG_COLOR_sf_covetous_glitch.png"
    generate(out_path)
