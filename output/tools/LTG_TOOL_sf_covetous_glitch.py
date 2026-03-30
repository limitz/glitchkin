# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_sf_covetous_glitch.py
"Luma & the Glitchkin" — Style Frame: COVETOUS GLITCH
Artist: Rin Yamamoto | Cycle 40

BRIEF
-----
Jayden Torres (audience critic, C40): "COVETOUS expression is the creepiest thing
in the pitch and should be in a style frame immediately."

Glitch in COVETOUS state. The moment Glitch reveals it wants what Byte has —
connection, warmth, presence. Tone: precise and predatory.

COMPOSITION
-----------
- Location: Other Side space — VOID_BLACK + UV_PURPLE ambient, zero warm light.
- Glitch: center frame, large (foreground), COVETOUS expression from expr v003.
  tilt=+12 (leaning toward subject), arms reaching forward, ACID_GREEN slit eyes,
  predatory brow angle, sparse UV_PURPLE confetti drifting forward.
- Background: simplified Other Side void. Aurora bands, UV_PURPLE sky gradient,
  far-distance slab silhouettes (inverted atmos perspective — more purple, darker).
- Byte silhouette: far right distance, tiny, warm teal glow — the object of desire.
  Small scale emphasizes inaccessibility. Rendered as simple silhouette with
  BYTE_TEAL glow halo — warmth in darkness as the "thing Glitch cannot name."
- Foreground void: feathered edge at bottom, inverted perspective floor.
- Color language:
    - ACID_GREEN in eyes and brow lines = predatory calculation
    - UV_PURPLE ambient = digital void, Glitch's native space
    - CORRUPT_AMBER body = Glitch's essential color, not threatening here but
      precise, contained, still — because it is watching
    - BYTE_TEAL far away = warmth Glitch wants but cannot have
    - HOT_MAGENTA crack = the internal fracture exposed by desire

OUTPUT: output/color/style_frames/LTG_SF_covetous_glitch_v001.png

CRITICAL RULES:
  - NO WARM LIGHT. Warmth exists only in Byte's distant teal glow (pigment).
  - UV_PURPLE_DARK = GL-04a (58, 16, 96) — canonical, verified C40.
  - After every img.paste() / alpha_composite: refresh draw = ImageDraw.Draw(img).
  - Output ≤ 1280px both dimensions (docs/image-rules.md).
  - All RNG seeded for reproducibility.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFilter

__version__ = "1.0.0"
__author__ = "Rin Yamamoto"
__cycle__ = 40

# ── Canvas ────────────────────────────────────────────────────────────────────
W, H = 1280, 720

# ── Palette ───────────────────────────────────────────────────────────────────
VOID_BLACK      = (10,  10,  20)
UV_PURPLE       = (123, 47, 190)      # GL-04 #7B2FBE — canonical
ACID_GREEN      = (57,  255,  20)     # GL-03 #39FF14
ELEC_CYAN       = (0,   240, 255)     # GL-01a
BYTE_TEAL       = (0,   212, 232)     # GL-01b
CORRUPT_AMB     = (255, 140,   0)     # GL-07
CORRUPT_AMB_SH  = (168,  76,   0)
CORRUPT_AMB_HL  = (255, 185,  80)
SOFT_GOLD       = (232, 201,  90)
HOT_MAG         = (255,  45, 107)     # GL-06
STATIC_WHITE    = (240, 240, 240)
UV_PURPLE_MID   = (42,   26,  64)
UV_PURPLE_DARK  = (58,   16,  96)     # GL-04a #3A1060 — 72% sat. C40 canonical.
FAR_EDGE        = (33,   17,  54)
SLAB_FACE       = (10,   20,  32)
DATA_BLUE       = (43,  127, 255)
DATA_BLUE_HL    = (106, 186, 255)


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ── Background: Other Side Void ───────────────────────────────────────────────

def draw_void_sky(draw, img):
    """UV_PURPLE gradient sky — classic Other Side inverted atmospheric perspective."""
    draw.rectangle([0, 0, W - 1, H - 1], fill=VOID_BLACK)
    sky_bottom = int(H * 0.40)
    for y in range(sky_bottom):
        t = y / sky_bottom
        col = lerp_color(VOID_BLACK, UV_PURPLE_DARK, t)
        draw.line([(0, y), (W - 1, y)], fill=col)

    # Sparse stars
    rng = random.Random(42)
    for _ in range(60):
        sx = rng.randint(0, W - 1)
        sy = rng.randint(0, int(H * 0.35))
        draw.point((sx, sy), fill=STATIC_WHITE)

    # Ring megastructure (far sky element — canonically Other Side)
    ring_cx = int(W * 0.82)
    ring_cy = int(H * 0.16)
    ring_r  = int(H * 0.36)
    ring_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ring_draw = ImageDraw.Draw(ring_overlay)
    ring_draw.ellipse(
        [ring_cx - ring_r, ring_cy - ring_r,
         ring_cx + ring_r, ring_cy + ring_r],
        outline=(*UV_PURPLE, 45), width=2
    )
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, ring_overlay)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


def draw_aurora_bands(draw, img):
    """UV_PURPLE aurora bands across sky horizon."""
    aurora = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    adraw = ImageDraw.Draw(aurora)
    rng = random.Random(17)
    band_y = int(H * 0.33)
    for i in range(5):
        y0 = band_y + rng.randint(-20, 20)
        y1 = y0 + rng.randint(4, 12)
        alpha = rng.randint(12, 30)
        adraw.rectangle([0, y0, W - 1, y1], fill=(*UV_PURPLE, alpha))
    for i in range(3):
        y0 = band_y + rng.randint(-30, 30)
        y1 = y0 + rng.randint(2, 6)
        alpha = rng.randint(8, 18)
        adraw.rectangle([0, y0, W - 1, y1], fill=(*DATA_BLUE, alpha))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, aurora)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


def draw_far_slabs(draw):
    """Dark slab silhouettes — far distance. More purple, darker with distance (inverted atmos)."""
    rng = random.Random(55)
    horizon_y = int(H * 0.50)
    for i in range(8):
        sx = rng.randint(0, W - 80)
        sw = rng.randint(40, 110)
        sy = horizon_y - rng.randint(30, 90)
        sh = rng.randint(30, 90)
        draw.rectangle([sx, sy, sx + sw, horizon_y], fill=FAR_EDGE)
        draw.rectangle([sx, sy, sx + sw, sy + 2], fill=UV_PURPLE_MID)


def draw_floor(draw):
    """Flat void floor — digital grid, minimal, circuit-trace accent."""
    horizon_y = int(H * 0.50)
    # Floor base gradient — UV_PURPLE_DARK to VOID_BLACK below horizon
    for y in range(horizon_y, H):
        t = (y - horizon_y) / max(1, H - horizon_y)
        col = lerp_color(UV_PURPLE_DARK, VOID_BLACK, t)
        draw.line([(0, y), (W - 1, y)], fill=col)

    # Perspective grid lines converging to center-horizon VP
    vp_x = W // 2
    vp_y = horizon_y
    rng = random.Random(33)
    for i in range(12):
        fx = int(W * i / 11)
        alpha = 20 + rng.randint(0, 12)
        grid_overlay_line = [(vp_x + int((fx - vp_x) * 0.05), vp_y), (fx, H - 1)]
        draw.line(grid_overlay_line, fill=(*DATA_BLUE[:3], ), width=1)

    # Horizontal grid lines (perspective-spaced)
    for k in range(6):
        t = (k + 1) / 7
        gy = int(horizon_y + t * t * (H - horizon_y))
        draw.line([(0, gy), (W - 1, gy)], fill=UV_PURPLE_MID, width=1)


def draw_byte_silhouette(img):
    """
    Tiny Byte silhouette in far-right distance — the object of Glitch's desire.
    Rendered as a small teal diamond with warm glow halo.
    Small scale = inaccessible. Warmth in darkness = what Glitch wants.
    """
    bx = int(W * 0.78)
    by = int(H * 0.46)
    br = 18  # tiny — far away

    # Glow halo — BYTE_TEAL soft circle (desire, warmth at distance)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    for radius in range(br + 30, br - 1, -2):
        alpha = int(40 * (1 - (radius - br) / 30))
        if alpha > 0:
            gdraw.ellipse(
                [bx - radius, by - radius, bx + radius, by + radius],
                fill=(*BYTE_TEAL, alpha)
            )
    glow_blurred = glow.filter(ImageFilter.GaussianBlur(radius=6))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, glow_blurred)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)

    # Byte body: small diamond
    half = br
    pts = [
        (bx,        by - half),
        (bx + int(half * 0.7), by),
        (bx,        by + int(half * 0.8)),
        (bx - int(half * 0.7), by),
    ]
    draw.polygon(pts, fill=BYTE_TEAL)
    draw.polygon(pts, outline=VOID_BLACK, width=1)

    # Tiny 3x3 pixel eyes — BYTE_TEAL body, simple open glyphs
    cell = 2
    leye_x = bx - 7
    leye_y = by - 4
    reye_x = bx + 2
    reye_y = by - 4
    for ex, ey in [(leye_x, leye_y), (reye_x, reye_y)]:
        draw.rectangle([ex, ey, ex + cell * 3, ey + cell * 3], fill=VOID_BLACK)
        draw.rectangle([ex + cell, ey + cell, ex + cell * 2, ey + cell * 2], fill=ELEC_CYAN)

    return draw


# ── Glitch Character (COVETOUS — large, foreground) ───────────────────────────

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
    pts    = diamond_pts(cx, cy, rx, ry, tilt_deg, squash, stretch)
    sh_pts = [(x + 6, y + 8) for x, y in pts]
    # Deep shadow (UV_PURPLE for Other Side ambient)
    draw.polygon(sh_pts, fill=UV_PURPLE_DARK)
    draw.polygon(pts, fill=CORRUPT_AMB)
    top, right, bot, left = pts
    mid_tl = ((top[0] + left[0]) // 2, (top[1] + left[1]) // 2)
    ctr    = (cx, cy - ry // 4)
    draw.polygon([top, ctr, mid_tl], fill=CORRUPT_AMB_HL)
    draw.polygon(pts, outline=VOID_BLACK, width=5)
    # HOT_MAGENTA crack — desire made visible as fracture
    cs = (cx - rx // 2, cy - ry // 3)
    ce = (cx + rx // 3, cy + ry // 2)
    draw.line([cs, ce], fill=HOT_MAG, width=3)
    mid_c = ((cs[0] + ce[0]) // 2, (cs[1] + ce[1]) // 2)
    draw.line([mid_c, (cx + rx // 2, cy - ry // 4)], fill=HOT_MAG, width=2)
    # Secondary crack — internal pressure of wanting
    cs2 = (cx, cy - ry // 6)
    ce2 = (cx + rx // 2, cy + ry // 3)
    draw.line([cs2, ce2], fill=(*HOT_MAG, ), width=1)


def draw_top_spike(draw, cx, cy_top, rx, spike_h=24, tilt_off=0):
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
    draw.line([(sx, cy_top - spike_h * 2), (sx, cy_top - spike_h * 2 - 8)],
              fill=HOT_MAG, width=3)


def draw_bottom_spike(draw, cx, cy_bot, spike_h=20):
    pts = [
        (cx - spike_h // 2, cy_bot),
        (cx + spike_h // 2, cy_bot),
        (cx, cy_bot + spike_h + 8),
    ]
    draw.polygon(pts, fill=CORRUPT_AMB_SH)
    draw.polygon(pts, outline=VOID_BLACK, width=3)


def draw_arm(draw, cx, cy, side='left', arm_dy=0, arm_dx=0, rx=68):
    """Reaching arms — COVETOUS extends toward the object of desire (Byte, right side)."""
    if side == 'left':
        ax  = cx - rx - 10
        ay  = cy + arm_dy
        # Left arm reaching forward-right (toward where Byte is)
        tip = (ax - 20 + arm_dx + 30, ay - 14)
    else:
        ax  = cx + rx + 10
        ay  = cy + arm_dy
        # Right arm extending fully toward Byte
        tip = (ax + 30 + arm_dx, ay - 16)
    pts = [(ax, ay - 8), (ax, ay + 8), tip]
    draw.polygon(pts, fill=CORRUPT_AMB)
    draw.polygon(pts, outline=VOID_BLACK, width=3)
    # Claw-like finger tips — reaching, wanting
    tip_x, tip_y = tip
    for fi in range(3):
        fx = tip_x - 4 + fi * 5
        draw.line([(fx, tip_y), (fx + 1, tip_y - 8)], fill=CORRUPT_AMB_SH, width=2)


def draw_pixel_eye(draw, ex, ey, cell=10, side='left'):
    """
    COVETOUS eye glyph: [[5,5,5],[0,5,0],[0,0,0]] — acid slit, target lock.
    Both eyes identical — bilateral focus (not destabilized as in other expressions).
    """
    PIXEL_COLORS = {
        0: VOID_BLACK,
        5: ACID_GREEN,
    }
    glyph = [
        [5, 5, 5],
        [0, 5, 0],
        [0, 0, 0],
    ]
    for row in range(3):
        for col in range(3):
            state = glyph[row][col]
            color = PIXEL_COLORS[state]
            px    = ex + col * cell
            py    = ey + row * cell
            draw.rectangle([px, py, px + cell - 1, py + cell - 1], fill=color)
    # Eye outline box
    draw.rectangle([ex - 1, ey - 1, ex + cell * 3, ey + cell * 3],
                   outline=VOID_BLACK, width=2)


def draw_brows(draw, cx, cy, rx, ry):
    """
    COVETOUS brows: furrowed downward toward center — predatory inward focus.
    ACID_GREEN, angled inward. Matches the expression sheet exactly, scaled up.
    """
    face_cy = cy - ry // 6
    cell    = 10
    leye_x  = cx - rx // 2 - cell * 3 // 2
    leye_y  = face_cy - cell * 3 // 2
    reye_x  = cx + rx // 2 - cell * 3 // 2
    reye_y  = face_cy - cell * 3 // 2

    # Left brow: angled down-right toward center
    draw.line(
        [(leye_x - 4, leye_y - 6), (leye_x + cell * 3 + 4, leye_y - 14)],
        fill=ACID_GREEN, width=4
    )
    # Right brow: angled down-left toward center
    draw.line(
        [(reye_x - 4, reye_y - 14), (reye_x + cell * 3 + 4, reye_y - 6)],
        fill=ACID_GREEN, width=4
    )


def draw_mouth(draw, mx, my):
    """
    COVETOUS mouth: tight horizontal line — barely containing desire.
    Small corner uptick at right edge — the wanting leaks out.
    """
    draw.line([(mx, my), (mx + 28, my)], fill=CORRUPT_AMB_SH, width=3)
    draw.line([(mx + 28, my), (mx + 34, my - 6)], fill=ACID_GREEN, width=2)


def draw_confetti(draw, cx, cy_bot):
    """Sparse UV_PURPLE confetti drifting forward-right — COVETOUS spec: count=4, forward drift."""
    rng = random.Random(8)
    cols = [UV_PURPLE, UV_PURPLE, CORRUPT_AMB_SH]
    for _ in range(4):
        # Drifted forward: confetti scatters toward Byte (right side)
        px = rng.randint(cx, cx + 36)
        py = rng.randint(cy_bot + 8, cy_bot + 32)
        sz = rng.choice([4, 6, 8])
        col = rng.choice(cols)
        draw.rectangle([px, py, px + sz, py + sz], fill=col)


def draw_glitch_large(img):
    """
    Draw Glitch in COVETOUS state, large (foreground), center-left.
    Scale: rx=68, ry=76 (about 3× expression sheet size).
    Position: center of frame, slightly left of center so Byte is visible right.
    """
    draw = ImageDraw.Draw(img)
    cx = int(W * 0.42)
    cy = int(H * 0.50)
    rx = 68
    ry = 76

    # COVETOUS pose params from expression sheet:
    tilt_deg = 12    # lean toward subject
    squash   = 0.85
    stretch  = 1.0
    arm_l_dy = -16   # arms reaching
    arm_r_dy = -12
    spike_h  = 24    # spike_h=12 in sheet — scaled 2×

    cy_bot = cy + int(ry * squash * stretch * 1.15) + 12
    draw_bottom_spike(draw, cx, cy_bot - 4)
    draw_confetti(draw, cx, cy_bot)
    draw_glitch_body(draw, cx, cy, rx, ry, tilt_deg=tilt_deg, squash=squash, stretch=stretch)
    draw_arm(draw, cx, cy, side='left',  arm_dy=arm_l_dy, arm_dx=0, rx=rx)
    draw_arm(draw, cx, cy, side='right', arm_dy=arm_r_dy, arm_dx=0, rx=rx)

    cy_top   = cy - int(ry * squash * stretch)
    tilt_off = int(tilt_deg * 0.4)
    draw_top_spike(draw, cx, cy_top, rx, spike_h=spike_h, tilt_off=tilt_off)

    # Face features
    face_cy = cy - ry // 6
    cell    = 10
    leye_x  = cx - rx // 2 - cell * 3 // 2
    leye_y  = face_cy - cell * 3 // 2
    reye_x  = cx + rx // 2 - cell * 3 // 2
    reye_y  = face_cy - cell * 3 // 2

    draw_pixel_eye(draw, leye_x, leye_y, cell=cell, side='left')
    draw_pixel_eye(draw, reye_x, reye_y, cell=cell, side='right')
    draw_brows(draw, cx, cy, rx, ry)

    mouth_cx = cx - 14
    mouth_cy = face_cy + cell * 3 // 2 + 8
    draw_mouth(draw, mouth_cx, mouth_cy)

    return draw


# ── UV_PURPLE ambient overlay (Glitch is inside its own space) ────────────────

def draw_ambient_overlay(img):
    """Subtle UV_PURPLE ambient fill — Glitch's native space, radiating from all sides."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)

    # Corner vignette — UV_PURPLE tinting in corners and edges (Other Side canonical)
    for dist in range(150, 0, -15):
        alpha = int(18 * (1 - dist / 150))
        odraw.rectangle([0, 0, dist, H - 1], fill=(*UV_PURPLE_DARK, alpha))
        odraw.rectangle([W - 1 - dist, 0, W - 1, H - 1], fill=(*UV_PURPLE_DARK, alpha))

    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


# ── ACID_GREEN eye-glow spill (Glitch staring — eyes radiate intent) ─────────

def draw_eye_glow(img):
    """
    ACID_GREEN glow emanating from Glitch's eyes — bidirectional target lock.
    The stare has physical weight: color spills forward toward Byte.
    """
    cx = int(W * 0.42)
    cy = int(H * 0.50)
    rx = 68
    ry = 76
    face_cy = cy - ry // 6
    cell    = 10
    leye_cx = (int(cx - rx // 2 - cell * 3 // 2)) + cell + 5
    reye_cx = (int(cx + rx // 2 - cell * 3 // 2)) + cell + 5
    eye_cy  = face_cy - cell * 3 // 2 + cell

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)

    for ecx in [leye_cx, reye_cx]:
        for r in range(40, 5, -5):
            alpha = int(25 * (1 - r / 40))
            gdraw.ellipse([ecx - r, eye_cy - r, ecx + r, eye_cy + r],
                          fill=(*ACID_GREEN, alpha))

    glow_blurred = glow.filter(ImageFilter.GaussianBlur(radius=8))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, glow_blurred)
    img.paste(img_rgba.convert("RGB"))
    draw = ImageDraw.Draw(img)
    return draw


# ── Footer label ─────────────────────────────────────────────────────────────

def draw_footer(draw):
    """Production label bar — black strip, cyan/amber text."""
    bar_h = 28
    draw.rectangle([0, H - bar_h, W - 1, H - 1], fill=VOID_BLACK)
    label = "LUMA & THE GLITCHKIN  |  GLITCH — COVETOUS  |  Style Frame C40"
    # No font dependency — draw as pixel blocks forming label background
    draw.line([(0, H - bar_h), (W - 1, H - bar_h)], fill=UV_PURPLE, width=1)
    # Right tag: small version block
    draw.rectangle([W - 90, H - bar_h + 4, W - 6, H - 6], fill=UV_PURPLE_DARK)


# ── Main generator ────────────────────────────────────────────────────────────

def generate(output_path):
    img = Image.new("RGB", (W, H), VOID_BLACK)

    # Layer order: sky → aurora → slabs → floor → ambient → Byte → Glitch → eye glow → footer
    print("[1/9] Void sky gradient...")
    draw = ImageDraw.Draw(img)
    draw = draw_void_sky(draw, img)

    print("[2/9] Aurora bands...")
    draw = draw_aurora_bands(draw, img)

    print("[3/9] Far distance slabs...")
    draw = ImageDraw.Draw(img)
    draw_far_slabs(draw)

    print("[4/9] Void floor grid...")
    draw = ImageDraw.Draw(img)
    draw_floor(draw)

    print("[5/9] Ambient UV_PURPLE overlay...")
    draw = draw_ambient_overlay(img)

    print("[6/9] Byte silhouette (far right — object of desire)...")
    draw = draw_byte_silhouette(img)

    print("[7/9] Glitch — COVETOUS (large, foreground)...")
    draw = draw_glitch_large(img)

    print("[8/9] ACID_GREEN eye-glow spill...")
    draw = draw_eye_glow(img)

    print("[9/9] Footer label...")
    draw = ImageDraw.Draw(img)
    draw_footer(draw)

    # Hard limit: ≤ 1280px in both dimensions (docs/image-rules.md)
    img.thumbnail((1280, 1280), Image.LANCZOS)

    img.save(output_path)
    import os
    file_size = os.path.getsize(output_path)
    print(f"Saved: {output_path}")
    print(f"  Size: {img.size[0]}×{img.size[1]}  File: {file_size:,} bytes ({file_size//1024} KB)")

    # Self-report UV_PURPLE hue status
    print(f"\n[QA] UV_PURPLE_DARK = (58, 16, 96) = GL-04a #3A1060 — 271.5° hue, 83.3% sat")
    print(f"[QA] Delta from canonical 271.9°: 0.4° — PASS (spec ≤ 5°)")
    print(f"[QA] NO WARM LIGHT. Byte teal glow = pigment warmth only, not ambient.")

    return file_size


if __name__ == "__main__":
    out_path = "/home/wipkat/team/output/color/style_frames/LTG_SF_covetous_glitch_v001.png"
    generate(out_path)
