#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P24.py
Cold Open Panel P24 — WIDE/MED — CHAOS APEX: THE BREACH
Diego Vargas, Storyboard Artist — Cycle 42

Beat: THE HOOK FRAME. Every monitor has breached. Glitchkin pour out in a wave
      of pixel-glitch energy. The warm den is overwritten by digital invasion.
      Luma in the foreground — low-angle hero. Byte on her shoulder: resigned dignity.
      These two are the STILL POINT at the center of the storm.

Shot:   WIDE/MED — full scene, Luma FG, chaos surrounding
Camera: Low angle, Dutch tilt 12° LEFT. Maximum energy.
Palette: Full Glitch Chaos — warm palette gone. ELEC_CYAN/HOT_MAGENTA dominant.
         Only Luma herself retains warm color (identity / still point contrast).
Arc:    PITCH BEAT — this is the show's premise in one image.

Expression:
- Luma: chin up, eyes WIDE but jaw set — adrenaline overriding sense.
  The GRIN is starting to form. She is not scared; she is DELIGHTED.
- Byte: on her shoulder. RESIGNED DIGNITY. "I resent this. I am still here."

Image size rule: ≤ 1280px in both dimensions.
Output: output/storyboards/panels/LTG_SB_cold_open_P24.png
"""

from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P24.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H   # 540

# ── Palette ──────────────────────────────────────────────────────────────────
# Full Glitch Chaos — warm has been mostly overwritten
ELEC_CYAN    = (0, 212, 232)
ELEC_CYAN_DIM= (0, 140, 160)
ELEC_CYAN_HI = (80, 240, 252)
HOT_MAGENTA  = (232, 0, 152)
HOT_MAG_DIM  = (180, 0, 100)
UV_PURPLE    = (123, 47, 190)
VOID_BLACK   = (10, 10, 20)
DEEP_SPACE   = (18, 16, 32)
# Luma — warm identity preserved (still point contrast)
LUMA_HOODIE  = (232, 112, 58)   # canonical orange #E8703A
LUMA_SKIN    = (238, 192, 140)
LUMA_HAIR    = (52, 38, 24)
LUMA_HAIR_HI = (80, 56, 32)
LUMA_PANT    = (140, 112, 168)  # lavender shorts
# Byte
BYTE_TEAL    = (0, 212, 232)
BYTE_EYE_W   = (220, 230, 240)
CRACK_LINE   = (200, 30, 100)
# Room (remnant warm elements — mostly washed by glitch)
FLOOR_WARM   = (140, 110, 75)   # desaturated by chaos
WALL_REMNANT = (90, 70, 50)     # warm wall barely holding on
CRT_PLASTIC  = (60, 50, 40)     # monitors dark except screen glow
# Caption
BG_CAPTION   = (8, 6, 14)
TEXT_CAP     = (220, 215, 235)
ANN_COL      = (180, 155, 100)
ANN_DIM      = (130, 115, 90)
ARC_PITCH    = (0, 212, 232)    # PITCH BEAT arc

RNG = random.Random(2424)


def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()


def add_glow(img, cx, cy, r_max, color_rgb, steps=6, max_alpha=50):
    """Additive glow via alpha_composite — never darkens."""
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_irregular_poly(draw, cx, cy, r, sides, color, seed=0, outline=None):
    """Draw irregular polygon (Glitchkin pixel standard — no rectangles)."""
    rng = random.Random(seed)
    pts = []
    for i in range(sides):
        angle = (2 * math.pi * i / sides) + rng.uniform(-0.25, 0.25)
        dist  = r * rng.uniform(0.70, 1.20)
        pts.append((int(cx + dist * math.cos(angle)), int(cy + dist * math.sin(angle))))
    draw.polygon(pts, fill=color, outline=outline)


def draw_dutch_tilt_grid(draw, tilt_deg=12):
    """Draw faint tilted grid lines to establish Dutch tilt feel."""
    rad = math.radians(tilt_deg)
    cos_t = math.cos(rad)
    sin_t = math.sin(rad)
    # Faint diagonal horizon line (tilted floor/ceiling boundary)
    # Horizon at ~35% DRAW_H in normal coords — apply tilt
    hy = int(DRAW_H * 0.35)
    # Tilted line across full panel
    dx = int(DRAW_H * sin_t * 0.5)
    draw.line([(0, hy + dx), (PW, hy - dx)],
              fill=(40, 35, 55), width=2)


def draw_breach_monitors(draw, img):
    """
    Draw the wall of breached CRT monitors.
    Multiple screens open — pouring out glitch energy.
    Arranged across the back wall (blurred/BG read).
    """
    # Monitor positions: scattered across back wall
    # At Dutch tilt, wall reads at slight diagonal — annotations confirm this
    monitor_specs = [
        # (cx_frac, cy_frac, w_frac, h_frac, breach_intensity)
        (0.08,  0.14, 0.12, 0.16, 1.0),   # far left, high
        (0.22,  0.10, 0.14, 0.18, 0.9),   # left-center upper
        (0.42,  0.08, 0.16, 0.20, 1.0),   # center-left upper (main breach)
        (0.62,  0.12, 0.13, 0.17, 0.85),  # center-right
        (0.80,  0.08, 0.14, 0.19, 1.0),   # right upper
        (0.10,  0.32, 0.13, 0.16, 0.70),  # left mid
        (0.75,  0.30, 0.12, 0.15, 0.75),  # right mid
    ]

    for i, (cx_f, cy_f, w_f, h_f, intensity) in enumerate(monitor_specs):
        cx = int(cx_f * PW)
        cy = int(cy_f * DRAW_H)
        mw = int(w_f * PW)
        mh = int(h_f * DRAW_H)

        # Monitor body
        draw.rectangle([cx - mw // 2, cy - mh // 2, cx + mw // 2, cy + mh // 2],
                       fill=CRT_PLASTIC, outline=VOID_BLACK, width=2)

        # Screen area (inner — glowing with breach)
        sm = 6
        sx0 = cx - mw // 2 + sm
        sx1 = cx + mw // 2 - sm
        sy0 = cy - mh // 2 + sm
        sy1 = cy + mh // 2 - sm

        # Screen color — ELEC_CYAN at max breach
        breach_col = (int(ELEC_CYAN[0] * intensity), int(ELEC_CYAN[1] * intensity), int(ELEC_CYAN[2] * intensity))
        draw.rectangle([sx0, sy0, sx1, sy1], fill=breach_col)

        # Screen bulge annotation (concentric rings)
        scx = (sx0 + sx1) // 2
        scy = (sy0 + sy1) // 2
        screen_r = min(sx1 - sx0, sy1 - sy0) // 2
        for ring in range(1, 3):
            rr = screen_r * (1.0 + ring * 0.15)
            draw.ellipse([int(scx - rr), int(scy - rr * 0.75),
                          int(scx + rr), int(scy + rr * 0.75)],
                         outline=(*ELEC_CYAN_HI, 60 - ring * 15), width=1)

        # Glow from screen
        add_glow(img, scx, scy, int(screen_r * 1.8), ELEC_CYAN,
                 steps=4, max_alpha=int(40 * intensity))
        draw = ImageDraw.Draw(img)

        # Scan lines on screen
        for sl_y in range(sy0, sy1, 3):
            draw.line([(sx0, sl_y), (sx1, sl_y)], fill=(ELEC_CYAN_DIM), width=1)

    return draw


def draw_glitchkin_swarm(draw, img):
    """
    Draw Glitchkin pouring out — various shapes, sizes, angles.
    They read as a chaotic wave emanating from the monitors.
    At this scale, individual design detail is secondary to the WAVE read.
    """
    rng = random.Random(2424)

    # Glitchkin positions — scattered across upper 2/3 of panel
    # More dense near monitor wall, spreading outward
    glitchkin_positions = []
    for gi in range(28):
        gx = rng.randint(10, PW - 10)
        gy = rng.randint(10, int(DRAW_H * 0.72))
        g_scale = rng.uniform(0.6, 1.6)   # varies in size (depth illusion)
        glitchkin_positions.append((gx, gy, g_scale))

    # Sort by Y (back to front)
    glitchkin_positions.sort(key=lambda x: x[1])

    for gi, (gx, gy, g_scale) in enumerate(glitchkin_positions):
        body_r = int(12 * g_scale)
        sides = rng.randint(4, 7)
        # Color: mix of cyan, magenta, purple
        col_choice = rng.randint(0, 3)
        if col_choice == 0:
            col = ELEC_CYAN
        elif col_choice == 1:
            col = HOT_MAGENTA
        elif col_choice == 2:
            col = UV_PURPLE
        else:
            col = ELEC_CYAN_HI

        # Main body polygon
        draw_irregular_poly(draw, gx, gy, body_r, sides, col,
                            seed=gi * 37 + 100, outline=VOID_BLACK)

        # Eyes — tiny dots
        if body_r > 8:
            eye_sep = int(body_r * 0.35)
            eye_r = max(2, int(body_r * 0.15))
            draw.ellipse([gx - eye_sep - eye_r, gy - eye_r,
                          gx - eye_sep + eye_r, gy + eye_r],
                         fill=BYTE_EYE_W)
            draw.ellipse([gx + eye_sep - eye_r, gy - eye_r,
                          gx + eye_sep + eye_r, gy + eye_r],
                         fill=BYTE_EYE_W)

        # Pixel trail behind each Glitchkin (motion blur)
        trail_len = rng.randint(1, 3)
        for ti in range(trail_len):
            tx = gx + rng.randint(-20, 20) * (ti + 1) // 2
            ty = gy + rng.randint(-15, 5)
            trail_r = max(2, body_r - ti * 3)
            draw_irregular_poly(draw, tx, ty, trail_r, sides, col,
                                seed=gi * 53 + ti * 7 + 200)

    return draw


def draw_pixel_confetti_storm(draw):
    """Pixel confetti at storm density — fills air between characters and monitors."""
    rng = random.Random(999)
    for ci in range(220):
        cx = rng.randint(0, PW)
        cy = rng.randint(0, int(DRAW_H * 0.88))
        cs = rng.randint(2, 6)
        col_choice = rng.randint(0, 4)
        if col_choice == 0:
            col = ELEC_CYAN
        elif col_choice == 1:
            col = HOT_MAGENTA
        elif col_choice == 2:
            col = UV_PURPLE
        elif col_choice == 3:
            col = ELEC_CYAN_HI
        else:
            col = (220, 220, 240)   # white-ish

        # Use irregular poly instead of rectangle (Glitchkin pixel standard)
        draw_irregular_poly(draw, cx + cs // 2, cy + cs // 2,
                            cs, rng.randint(4, 6), col, seed=ci * 17 + 300)


def draw_luma(draw, img, luma_cx, luma_floor_y, body_h):
    """
    Draw Luma — low angle FG hero shot.
    Chin up, eyes wide but jaw set. Grin starting to form.
    Low angle = we look UP at her — heroic framing.
    She is the warm identity anchor in the glitch chaos.
    """
    # At low angle, she appears taller than Byte — proper scale.
    # body_h represents visible body from floor to head.

    leg_h    = int(body_h * 0.32)
    torso_h  = int(body_h * 0.38)
    head_r   = int(body_h * 0.14)
    head_cy  = luma_floor_y - body_h + head_r + int(body_h * 0.04)
    torso_y0 = head_cy + head_r
    torso_y1 = luma_floor_y - leg_h

    # ── LEGS ─────────────────────────────────────────────────────────────────
    leg_spread = int(body_h * 0.12)
    for side in [-1, 1]:
        leg_x = luma_cx + side * leg_spread
        foot_x = luma_cx + side * int(leg_spread * 1.15)
        draw.polygon([
            (leg_x - int(body_h * 0.045), torso_y1),
            (leg_x + int(body_h * 0.045), torso_y1),
            (foot_x + int(body_h * 0.05), luma_floor_y),
            (foot_x - int(body_h * 0.05), luma_floor_y),
        ], fill=LUMA_PANT, outline=VOID_BLACK)
        # Foot
        draw.rectangle([foot_x - int(body_h * 0.055), luma_floor_y,
                        foot_x + int(body_h * 0.055) + side * int(body_h * 0.04),
                        luma_floor_y + int(body_h * 0.04)],
                       fill=(60, 52, 44), outline=VOID_BLACK)

    # ── TORSO (hoodie — canonical orange) ────────────────────────────────────
    torso_hw_top = int(body_h * 0.17)   # slightly narrower at shoulder
    torso_hw_bot = int(body_h * 0.15)
    torso_pts = [
        (luma_cx - torso_hw_top, torso_y0 + int(torso_h * 0.05)),
        (luma_cx,                torso_y0),
        (luma_cx + torso_hw_top, torso_y0 + int(torso_h * 0.05)),
        (luma_cx + torso_hw_bot, torso_y1),
        (luma_cx - torso_hw_bot, torso_y1),
    ]
    draw.polygon(torso_pts, fill=LUMA_HOODIE, outline=VOID_BLACK)
    # Hoodie pocket (asymmetric bump left side)
    pocket_cx = luma_cx - int(torso_hw_top * 0.3)
    pocket_y  = torso_y0 + int(torso_h * 0.60)
    pocket_pts = [
        (pocket_cx - int(body_h * 0.05), pocket_y),
        (pocket_cx + int(body_h * 0.07), pocket_y),
        (pocket_cx + int(body_h * 0.06), pocket_y + int(body_h * 0.08)),
        (pocket_cx - int(body_h * 0.06), pocket_y + int(body_h * 0.09)),
    ]
    draw.polygon(pocket_pts, fill=(200, 90, 40), outline=VOID_BLACK)

    # ── ARMS ─────────────────────────────────────────────────────────────────
    arm_top_y = torso_y0 + int(torso_h * 0.10)
    arm_bot_y = torso_y0 + int(torso_h * 0.55)
    arm_len   = int(body_h * 0.24)

    # Right arm: raised/reaching up (ACTION pose — about to do something)
    ra_x0 = luma_cx + torso_hw_top
    ra_x1 = ra_x0 + arm_len
    ra_y0 = arm_top_y
    ra_y1 = arm_top_y - int(arm_len * 0.55)
    arm_w = int(body_h * 0.045)
    draw.polygon([
        (ra_x0,       ra_y0),
        (ra_x0 + arm_w, ra_y0 + arm_w),
        (ra_x1 + arm_w, ra_y1 + arm_w),
        (ra_x1,       ra_y1),
    ], fill=LUMA_HOODIE, outline=VOID_BLACK)
    # Right hand (raised, open)
    draw_irregular_poly(draw, ra_x1 + arm_w // 2, ra_y1,
                        int(body_h * 0.055), 5, LUMA_SKIN, seed=2401, outline=VOID_BLACK)

    # Left arm: at side, casual/grounded
    la_x0 = luma_cx - torso_hw_top
    la_x1 = la_x0 - int(arm_len * 0.8)
    la_y0 = arm_top_y
    la_y1 = arm_bot_y + int(body_h * 0.05)
    draw.polygon([
        (la_x0,         la_y0),
        (la_x0 - arm_w, la_y0 + arm_w),
        (la_x1 - arm_w, la_y1),
        (la_x1,         la_y1 - arm_w),
    ], fill=LUMA_HOODIE, outline=VOID_BLACK)

    # ── HEAD ─────────────────────────────────────────────────────────────────
    # At low angle: we see slightly undersell of chin — head tilted up
    draw_irregular_poly(draw, luma_cx, head_cy, head_r, 7,
                        LUMA_SKIN, seed=2402, outline=VOID_BLACK)

    # ── HAIR — chaotic cloud ─────────────────────────────────────────────────
    # Hair is BIG and chaotic — even more so with glitch energy nearby
    hair_r = int(head_r * 1.65)
    for hair_blob in range(7):
        brng = random.Random(hair_blob * 31 + 7)
        bx = luma_cx + brng.randint(-int(head_r * 0.9), int(head_r * 0.9))
        by = head_cy - int(head_r * 0.55) + brng.randint(-int(head_r * 0.5), int(head_r * 0.3))
        br = int(head_r * brng.uniform(0.7, 1.15))
        draw_irregular_poly(draw, bx, by, br, 5,
                            LUMA_HAIR if hair_blob % 3 != 2 else LUMA_HAIR_HI,
                            seed=hair_blob * 47 + 100, outline=None)

    # ── FACE — adrenaline delight expression ─────────────────────────────────
    eye_cy  = head_cy - int(head_r * 0.12)
    eye_sep = int(head_r * 0.38)
    eye_w   = int(head_r * 0.28)
    eye_h   = int(head_r * 0.36)   # WIDE open eyes — adrenaline

    for side in [-1, 1]:
        ex = luma_cx + side * eye_sep
        # Eye white (wide open ellipse)
        draw.ellipse([ex - eye_w, eye_cy - eye_h, ex + eye_w, eye_cy + eye_h],
                     fill=BYTE_EYE_W, outline=VOID_BLACK, width=2)
        # Iris (warm amber/brown)
        iris_r = int(eye_w * 0.55)
        draw.ellipse([ex - iris_r, eye_cy - iris_r, ex + iris_r, eye_cy + iris_r],
                     fill=(100, 70, 35), outline=VOID_BLACK, width=1)
        # Pupil
        pu_r = int(iris_r * 0.50)
        draw.ellipse([ex - pu_r, eye_cy - pu_r, ex + pu_r, eye_cy + pu_r],
                     fill=VOID_BLACK)
        # Cyan catch light (glitch world in her eyes)
        draw.ellipse([ex + iris_r // 4, eye_cy - iris_r // 2,
                      ex + iris_r // 4 + 4, eye_cy - iris_r // 2 + 4],
                     fill=ELEC_CYAN_HI)

    # Brows — raised but not alarmed — excited surprise
    brow_y = eye_cy - int(eye_h * 1.0)
    for side in [-1, 1]:
        bx_c = luma_cx + side * eye_sep
        draw.polygon([
            (bx_c - eye_w, brow_y + 4),
            (bx_c + side * int(eye_w * 0.3), brow_y - 4 - int(head_r * 0.06)),
            (bx_c + eye_w * side * -1, brow_y + 2),
            (bx_c + eye_w * side * -1, brow_y + 7),
            (bx_c - eye_w + 2, brow_y + 9),
        ], fill=LUMA_HAIR)

    # Mouth — the GRIN forming (wide, slight curl on both corners)
    mouth_cy = head_cy + int(head_r * 0.38)
    mouth_hw = int(head_r * 0.50)
    # Base line (open mouth, grin forming)
    draw.ellipse([luma_cx - mouth_hw, mouth_cy - int(head_r * 0.10),
                  luma_cx + mouth_hw, mouth_cy + int(head_r * 0.14)],
                 fill=VOID_BLACK, outline=LUMA_SKIN, width=1)
    # Corner upturns (the grin)
    for side in [-1, 1]:
        corner_x = luma_cx + side * mouth_hw
        draw.line([(corner_x, mouth_cy), (corner_x + side * 4, mouth_cy - 5)],
                  fill=VOID_BLACK, width=2)

    return draw


def draw_byte_on_shoulder(draw, img, byte_cx, byte_cy, body_h):
    """
    Draw Byte riding on Luma's shoulder — RESIGNED DIGNITY.
    Small relative to Luma's head. Present but not happy about it.
    """
    head_r = int(body_h * 0.20)
    torso_r = int(body_h * 0.26)

    # Byte body (inverted teardrop, compact)
    torso_pts = [
        (byte_cx - torso_r,     byte_cy + int(torso_r * 0.3)),
        (byte_cx,               byte_cy - int(torso_r * 0.4)),
        (byte_cx + torso_r,     byte_cy + int(torso_r * 0.3)),
        (byte_cx + int(torso_r * 0.5), byte_cy + torso_r),
        (byte_cx - int(torso_r * 0.5), byte_cy + torso_r),
    ]
    draw.polygon(torso_pts, fill=BYTE_TEAL, outline=VOID_BLACK)

    # Head
    draw_irregular_poly(draw, byte_cx, byte_cy - int(torso_r * 0.2),
                        head_r, 6, BYTE_TEAL, seed=2499, outline=VOID_BLACK)

    # Arms: slightly out (not hiding, not expressive — neutral resigned)
    arm_y = byte_cy + int(torso_r * 0.05)
    for side in [-1, 1]:
        draw.polygon([
            (byte_cx + side * torso_r, arm_y - 3),
            (byte_cx + side * (torso_r + int(body_h * 0.15)), arm_y - 1),
            (byte_cx + side * (torso_r + int(body_h * 0.14)), arm_y + 5),
            (byte_cx + side * torso_r, arm_y + 4),
        ], fill=BYTE_TEAL, outline=VOID_BLACK)

    # Eyes — RESIGNED expression
    eye_cy_b = byte_cy - int(torso_r * 0.15)
    eye_sep_b = int(head_r * 0.42)
    e_r = max(3, int(head_r * 0.32))

    # Normal eye (right) — HEAVY LID, downward inner corner (resigned not angry)
    ne_cx = byte_cx + eye_sep_b
    draw.ellipse([ne_cx - e_r, eye_cy_b - int(e_r * 0.75),
                  ne_cx + e_r, eye_cy_b + int(e_r * 0.75)],
                 fill=BYTE_EYE_W, outline=VOID_BLACK, width=1)
    heavy_lid = int(e_r * 0.42)   # heavy lid = resigned
    draw.ellipse([ne_cx - e_r, eye_cy_b - int(e_r * 0.75),
                  ne_cx + e_r, eye_cy_b - int(e_r * 0.75) + heavy_lid * 2],
                 fill=VOID_BLACK)
    draw.line([(ne_cx - e_r, eye_cy_b - int(e_r * 0.75) + heavy_lid),
               (ne_cx + e_r, eye_cy_b - int(e_r * 0.75) + heavy_lid)],
              fill=VOID_BLACK, width=2)
    # Iris
    ir = int(e_r * 0.45)
    draw.ellipse([ne_cx - ir, eye_cy_b - ir + heavy_lid // 2,
                  ne_cx + ir, eye_cy_b + ir - heavy_lid // 3],
                 fill=BYTE_TEAL, outline=VOID_BLACK, width=1)

    # Cracked eye (left)
    ce_cx = byte_cx - eye_sep_b
    draw.ellipse([ce_cx - e_r, eye_cy_b - int(e_r * 0.75),
                  ce_cx + e_r, eye_cy_b + int(e_r * 0.75)],
                 fill=VOID_BLACK, outline=ELEC_CYAN_DIM, width=1)
    draw.line([(ce_cx - e_r + 2, eye_cy_b - int(e_r * 0.6)),
               (ce_cx + e_r - 2, eye_cy_b + int(e_r * 0.6))],
              fill=CRACK_LINE, width=1)
    # Alive dot
    draw.ellipse([ce_cx - int(e_r * 0.35), eye_cy_b - int(e_r * 0.05),
                  ce_cx - int(e_r * 0.35) + 3, eye_cy_b - int(e_r * 0.05) + 3],
                 fill=ELEC_CYAN)

    # Mouth — flat "I resent this" line
    mouth_y_b = byte_cy + int(torso_r * 0.30)
    mouth_hw_b = int(head_r * 0.45)
    draw.line([(byte_cx - mouth_hw_b, mouth_y_b),
               (byte_cx + mouth_hw_b, mouth_y_b)],
              fill=VOID_BLACK, width=2)

    # ELEC_CYAN glow around Byte (he still radiates)
    add_glow(img, byte_cx, byte_cy, int(body_h * 0.60), ELEC_CYAN, steps=4, max_alpha=28)
    draw = ImageDraw.Draw(img)

    return draw


def apply_dutch_tilt(img, tilt_deg=12):
    """
    Apply Dutch tilt as a final rotation.
    Dutch tilt 12° left = rotate image 12° clockwise, then crop to original size.
    The Dutch tilt makes the camera feel tilted to the LEFT.
    """
    rad = math.radians(tilt_deg)
    # Expand bounding box so we don't lose corners
    rotated = img.rotate(-tilt_deg, expand=True, fillcolor=DEEP_SPACE)
    # Crop center to original size
    rw, rh = rotated.size
    left = (rw - PW) // 2
    top  = (rh - PH) // 2
    cropped = rotated.crop([left, top, left + PW, top + PH])
    return cropped


def draw_scene(img):
    draw = ImageDraw.Draw(img)

    # ── Background: CHAOS — warm den overwritten ──────────────────────────────
    # Full Glitch palette has taken over. Warm elements barely visible.
    # Room structure: blurred/abstracted in chaos — shapes read, detail lost.

    # Sky/ceiling — near-void, electric
    draw.rectangle([0, 0, PW, int(DRAW_H * 0.52)], fill=DEEP_SPACE)
    # Faint warm wall remnants at edges (barely holding on)
    draw.rectangle([0, 0, int(PW * 0.08), DRAW_H], fill=WALL_REMNANT)
    draw.rectangle([int(PW * 0.92), 0, PW, DRAW_H], fill=WALL_REMNANT)

    # Floor (warm but bleached by glitch energy)
    horizon_y = int(DRAW_H * 0.52)
    draw.rectangle([0, horizon_y, PW, DRAW_H], fill=FLOOR_WARM)
    # Floor desaturation from glitch overwrite — cyan tint spreading
    floor_cyan_overlay = Image.new('RGBA', (PW, DRAW_H - horizon_y), (0, 60, 80, 35))
    base = img.convert('RGBA')
    base.paste(floor_cyan_overlay, (0, horizon_y), floor_cyan_overlay)
    img.paste(base.convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Shelf/furniture silhouettes (barely legible in chaos)
    for shelf_x, shelf_y, shelf_w, shelf_h in [
        (0, int(DRAW_H * 0.20), int(PW * 0.14), int(DRAW_H * 0.28)),
        (int(PW * 0.86), int(DRAW_H * 0.18), int(PW * 0.14), int(DRAW_H * 0.26)),
    ]:
        draw.rectangle([shelf_x, shelf_y, shelf_x + shelf_w, shelf_y + shelf_h],
                       fill=(50, 38, 28))

    # Breach monitors on back wall
    draw = draw_breach_monitors(draw, img)

    # Overall ELEC_CYAN ambient flood from monitors
    add_glow(img, PW // 2, int(DRAW_H * 0.22), int(PW * 0.55), ELEC_CYAN,
             steps=5, max_alpha=25)
    draw = ImageDraw.Draw(img)

    # MAGENTA accent glow from shadows/corners (chaos accent)
    add_glow(img, int(PW * 0.05), int(DRAW_H * 0.40), 180, HOT_MAGENTA,
             steps=4, max_alpha=18)
    add_glow(img, int(PW * 0.95), int(DRAW_H * 0.40), 160, HOT_MAGENTA,
             steps=4, max_alpha=15)
    draw = ImageDraw.Draw(img)

    # ── Glitchkin swarm ───────────────────────────────────────────────────────
    draw = draw_glitchkin_swarm(draw, img)

    # ── Pixel confetti storm ──────────────────────────────────────────────────
    draw_pixel_confetti_storm(draw)
    draw = ImageDraw.Draw(img)

    # ── LUMA — foreground FG hero shot ────────────────────────────────────────
    # Low angle: she reads as FG dominance, floor pushes up behind her.
    # She is center-left (not dead center — gives Byte shoulder room).
    luma_cx      = int(PW * 0.44)
    luma_floor_y = int(DRAW_H * 0.95)   # feet at bottom of draw area
    luma_body_h  = int(DRAW_H * 0.68)   # tall — she fills the FG (low angle)

    draw = draw_luma(draw, img, luma_cx, luma_floor_y, luma_body_h)
    draw = ImageDraw.Draw(img)

    # ── BYTE — on Luma's shoulder ─────────────────────────────────────────────
    # Byte perched on her right shoulder (viewer's left relative to her body
    # = camera-right of Luma = to luma_cx + shoulder offset).
    # At low angle camera: shoulder is at about 35% body height from top.
    shoulder_y = luma_floor_y - int(luma_body_h * 0.68)
    shoulder_x = luma_cx + int(luma_body_h * 0.19)   # right shoulder in panel
    byte_body_h = int(luma_body_h * 0.12)  # Byte is tiny relative to Luma
    draw = draw_byte_on_shoulder(draw, img, shoulder_x, shoulder_y, byte_body_h)
    draw = ImageDraw.Draw(img)

    # ── Dutch tilt grid line (confirm tilt annotation) ────────────────────────
    draw_dutch_tilt_grid(draw, tilt_deg=12)

    # ── Panel annotations ─────────────────────────────────────────────────────
    font_ann   = load_font(11)
    font_ann_b = load_font(11, bold=True)

    draw.text((10, 8), "P24  /  WIDE/MED  /  Low angle  /  Dutch tilt 12° LEFT  /  STATIC",
              font=font_ann, fill=ANN_COL)
    draw.text((10, 20), "THE HOOK FRAME. Glitchkin pour from breached screens. CHAOS APEX.",
              font=font_ann, fill=(0, 200, 220))
    draw.text((10, 32), "Luma + Byte = STILL POINT. She grins. He resents. Show premise in one image.",
              font=font_ann, fill=ANN_DIM)

    # Character callouts
    draw.text((luma_cx - 50, luma_floor_y - luma_body_h - 18),
              "LUMA: adrenaline\noverrides sense",
              font=load_font(9), fill=(220, 160, 80))
    draw.text((shoulder_x + 10, shoulder_y - byte_body_h - 14),
              "BYTE: resigned\ndignity",
              font=load_font(9), fill=ELEC_CYAN_DIM)

    # Dutch tilt label
    draw.text((PW - 140, 10), "DUTCH TILT 12° L",
              font=load_font(10, bold=True), fill=HOT_MAGENTA)

    # Shot label
    draw.rectangle([10, DRAW_H - 24, 165, DRAW_H - 6], fill=(20, 10, 24))
    draw.text((14, DRAW_H - 22), "WIDE/MED / LOW ANGLE",
              font=font_ann_b, fill=(240, 220, 140))

    # Arc indicator
    draw.rectangle([PW - 180, DRAW_H - 24, PW - 10, DRAW_H - 6], fill=(0, 30, 40))
    draw.text((PW - 176, DRAW_H - 22), "ARC: PITCH BEAT",
              font=font_ann_b, fill=ARC_PITCH)

    return draw


def make_panel():
    font_cap  = load_font(12)
    font_ann  = load_font(11)
    font_sm   = load_font(10)

    img  = Image.new('RGB', (PW, PH), DEEP_SPACE)
    draw_scene(img)

    # Apply Dutch tilt to scene ONLY (draw area, not caption bar)
    # Crop scene draw area, tilt, paste back
    scene_crop = img.crop([0, 0, PW, DRAW_H])
    tilted_scene = scene_crop.rotate(-12, expand=False, fillcolor=DEEP_SPACE)
    img.paste(tilted_scene, (0, 0))
    draw = ImageDraw.Draw(img)

    # Caption bar (drawn AFTER tilt — stays flat)
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(8, 6, 14), width=2)
    draw.text((10, DRAW_H + 4),
              "P24  WIDE/MED  Low angle  Dutch 12° L  |  CHAOS APEX — THE HOOK FRAME",
              font=font_cap, fill=(160, 150, 175))
    draw.text((10, DRAW_H + 18),
              "Glitchkin pour from breached monitors. Luma + Byte at still center. Show premise.",
              font=font_cap, fill=TEXT_CAP)
    draw.text((10, DRAW_H + 33),
              "LUMA: \"Okay, Byte — how do we put them back?\"  BYTE: \"...I resent this.\"",
              font=font_ann, fill=(140, 130, 100))
    draw.text((PW - 230, DRAW_H + 46), "LTG_SB_cold_open_P24  /  Diego Vargas  /  C42",
              font=font_sm, fill=(100, 95, 108))

    # Arc border — bright cyan (PITCH BEAT)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_PITCH, width=4)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("P24 standalone panel generation complete.")
