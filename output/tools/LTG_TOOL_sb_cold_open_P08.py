#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_cold_open_P08.py
Cold Open Panel P08 — MED — Byte Full Character Reveal
Diego Vargas, Storyboard Artist — Cycle 41

Beat: Byte is OUT. Standing in the real world for the first time.
      "The flesh dimension." — said with the tone of someone who expected
      it to smell, and it does. Full body reveal: compact, angular,
      tiny (head barely above cable bundles). Pixel confetti still drifting.
      Thin desaturation ring at his feet (digital nature bleaching the analogue floor).
      Camera at HIS eye level (~6" off floor).

Shot:   MED — full character (Byte)
Camera: Eye level (very low to floor — Byte's scale ~6"). Static.
        Camera at HIS scale validates him as a character at tiny size.
Palette: Byte = ELEC_CYAN + VOID_BLACK. Real World floor/room = warm amber/cream.
         CRT screen in BG returning to normal static (defocused).
Arc:    TENSE — transition beat (he's out, Luma still asleep, what now?)

Expression: disgust cycling → assessment → reluctant acknowledgment.
Body: compact inverted-teardrop, stubby arms/legs. Trailing pixel artifacts.
Size: TINY relative to room — head barely above cable bundles (6" tall).
Desaturation ring: at his feet, warm floor color slightly bleached/grey.

Image size rule: ≤ 1280px in both dimensions.
Output: output/storyboards/panels/LTG_SB_cold_open_P08.png
"""

from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_cold_open_P08.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H   # 540

# ── Palette ──────────────────────────────────────────────────────────────────
# Real World — warm
WARM_CREAM   = (250, 240, 220)
WARM_AMB     = (212, 146, 58)
FLOOR_WARM   = (195, 168, 126)
FLOOR_SHADOW = (165, 140, 102)
WALL_WARM    = (228, 214, 188)
WALL_SHADOW  = (196, 180, 152)
CABLE_DARK   = (55, 45, 32)
CABLE_MED    = (72, 60, 44)
WOOD_DARK    = (120, 80, 40)
SHELF_DARK   = (80, 60, 38)
LINE_DARK    = (70, 54, 36)
CRT_PLASTIC  = (185, 172, 138)
STATIC_GREY  = (148, 138, 128)
STATIC_DIM   = (125, 116, 108)
# Glitch World
ELEC_CYAN    = (0, 212, 232)
ELEC_CYAN_DIM= (0, 150, 170)
ELEC_CYAN_HI = (80, 240, 252)
HOT_MAGENTA  = (232, 0, 152)
VOID_BLACK   = (10, 10, 20)
BYTE_TEAL    = (0, 212, 232)
BYTE_EYE_W   = (220, 230, 240)
CRACK_LINE   = (200, 30, 100)
# Desaturation ring (floor bleached at Byte's feet)
DESAT_RING   = (175, 168, 160)     # washed-out warm floor — less saturation
CONFETTI_C   = (0, 212, 232)
CONFETTI_M   = (232, 0, 152)
PIXEL_SPARK  = (80, 240, 252)
# Caption
BG_CAPTION   = (14, 10, 8)
TEXT_CAP     = (235, 228, 210)
ANN_COL      = (200, 175, 120)
ANN_DIM      = (150, 135, 100)
ARC_TENSE    = (232, 0, 152)       # TENSE arc — hot magenta

RNG = random.Random(808)


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
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_irregular_poly(draw, cx, cy, r, sides, color, seed=0, outline=None):
    rng = random.Random(seed)
    pts = []
    for i in range(sides):
        angle = (2 * math.pi * i / sides) + rng.uniform(-0.25, 0.25)
        dist  = r * rng.uniform(0.70, 1.20)
        pts.append((int(cx + dist * math.cos(angle)), int(cy + dist * math.sin(angle))))
    draw.polygon(pts, fill=color, outline=outline)


def draw_byte_full_body(img, draw, byte_cx, byte_floor_y, body_h):
    """
    Draw Byte's full body standing in the real world.
    byte_cx: horizontal center of Byte
    byte_floor_y: y-coordinate of the floor (Byte stands on this)
    body_h: height of Byte's full body in pixels
    """
    # Byte is TINY — body_h should be small (real world scale = ~6 inches)
    # Full body = head + torso (inverted teardrop) + stubby legs

    torso_h  = int(body_h * 0.65)
    leg_h    = int(body_h * 0.28)
    head_r   = int(body_h * 0.22)   # head is roughly top sphere of the teardrop

    torso_top_y = byte_floor_y - body_h
    torso_bot_y = byte_floor_y - leg_h
    torso_cx    = byte_cx

    # ── BODY (inverted teardrop — wide at top, tapers toward legs) ───────────
    # 5-sided irregular polygon for torso
    torso_half_w_top = int(body_h * 0.32)
    torso_half_w_bot = int(body_h * 0.14)

    torso_pts = [
        (torso_cx - torso_half_w_top,     torso_top_y + int(torso_h * 0.18)),   # upper-left
        (torso_cx,                        torso_top_y),                           # top center
        (torso_cx + torso_half_w_top,     torso_top_y + int(torso_h * 0.18)),   # upper-right
        (torso_cx + torso_half_w_bot + 4, torso_bot_y - 4),                      # lower-right
        (torso_cx - torso_half_w_bot - 4, torso_bot_y - 4),                      # lower-left
    ]
    draw.polygon(torso_pts, fill=BYTE_TEAL, outline=VOID_BLACK)

    # Inner body detail (darker core for depth)
    inner_half_w = int(torso_half_w_top * 0.55)
    inner_pts = [
        (torso_cx - inner_half_w,  torso_top_y + int(torso_h * 0.28)),
        (torso_cx,                 torso_top_y + int(torso_h * 0.10)),
        (torso_cx + inner_half_w,  torso_top_y + int(torso_h * 0.28)),
        (torso_cx + inner_half_w - 4, torso_bot_y - 8),
        (torso_cx - inner_half_w + 4, torso_bot_y - 8),
    ]
    draw.polygon(inner_pts, fill=VOID_BLACK)

    # ── HEAD (merged with torso top — big round top of teardrop) ─────────────
    # Head protrudes from top of torso
    head_cy = torso_top_y + int(head_r * 0.6)
    # 6-sided irregular polygon for head
    draw_irregular_poly(draw, torso_cx, head_cy, head_r, 6,
                        BYTE_TEAL, seed=8801, outline=VOID_BLACK)

    # ── ARMS (short stubby — angled slightly outward) ─────────────────────────
    arm_top_y = torso_top_y + int(torso_h * 0.22)
    arm_bot_y = torso_top_y + int(torso_h * 0.55)
    arm_w     = int(body_h * 0.08)
    arm_len   = int(body_h * 0.22)

    for side in [-1, 1]:
        arm_x0  = torso_cx + side * torso_half_w_top
        arm_cx2 = arm_x0 + side * arm_len
        arm_mid_y = (arm_top_y + arm_bot_y) // 2
        # Arm as 4-point polygon
        arm_pts = [
            (arm_x0,          arm_top_y),
            (arm_cx2 + side * 2, arm_mid_y - arm_w),
            (arm_cx2 + side * 4, arm_mid_y + arm_w),
            (arm_x0,          arm_bot_y),
        ]
        draw.polygon(arm_pts, fill=BYTE_TEAL, outline=VOID_BLACK)

        # Hand (small irregular polygon)
        hand_cx = arm_cx2 + side * 4
        hand_cy = arm_mid_y
        hand_r  = int(body_h * 0.068)
        draw_irregular_poly(draw, hand_cx, hand_cy, hand_r, 5,
                            ELEC_CYAN_HI, seed=8802 + side * 3, outline=VOID_BLACK)

    # ── LEGS (short stubby, slightly spread) ─────────────────────────────────
    leg_top_y = torso_bot_y - 4
    leg_w     = int(body_h * 0.095)

    for side in [-1, 1]:
        leg_x    = torso_cx + side * torso_half_w_bot // 2
        foot_x   = leg_x + side * int(body_h * 0.05)
        leg_pts  = [
            (leg_x - leg_w // 2, leg_top_y),
            (leg_x + leg_w // 2, leg_top_y),
            (foot_x + leg_w // 2 + side * 2, byte_floor_y),
            (foot_x - leg_w // 2 + side * 2, byte_floor_y),
        ]
        draw.polygon(leg_pts, fill=BYTE_TEAL, outline=VOID_BLACK)

        # Foot (wider — pixel foot shape, angular)
        foot_y = byte_floor_y - 3
        foot_pts = [
            (foot_x - int(body_h * 0.06), foot_y),
            (foot_x + side * int(body_h * 0.14) + int(body_h * 0.06), foot_y),
            (foot_x + side * int(body_h * 0.14), foot_y + int(body_h * 0.06)),
            (foot_x - int(body_h * 0.04), foot_y + int(body_h * 0.06)),
        ]
        draw.polygon(foot_pts, fill=ELEC_CYAN_HI, outline=VOID_BLACK)

    # ── EYES ─────────────────────────────────────────────────────────────────
    # At this scale, eyes are small but still read clearly
    eye_cy = head_cy - int(head_r * 0.15)
    eye_sep = int(head_r * 0.46)
    e_r     = int(head_r * 0.30)

    # Normal eye (right)
    ne_cx = torso_cx + eye_sep
    ne_cy = eye_cy
    draw.ellipse([ne_cx - e_r, ne_cy - int(e_r * 0.75),
                  ne_cx + e_r, ne_cy + int(e_r * 0.75)],
                 fill=BYTE_EYE_W, outline=VOID_BLACK, width=1)
    # Squint lid
    lid = int(e_r * 0.28)
    draw.line([(ne_cx - e_r, ne_cy - int(e_r * 0.75) + lid),
               (ne_cx + e_r, ne_cy - int(e_r * 0.75) + lid)],
              fill=VOID_BLACK, width=2)
    draw.ellipse([ne_cx - e_r, ne_cy - int(e_r * 0.75),
                  ne_cx + e_r, ne_cy - int(e_r * 0.75) + lid * 2],
                 fill=VOID_BLACK)
    # Iris — LEVEL-FORWARD gaze (Lee Tanaka: contempt beat = level-forward or slight upward)
    # Slight upward offset: iris centered at slightly above the eye midpoint.
    # NOT downward (shame/resignation) — Byte is contemptuous, not defeated.
    iris_r = int(e_r * 0.50)
    gaze_up = int(e_r * 0.10)   # subtle upward push — superiority/contempt gaze
    draw.ellipse([ne_cx - iris_r, ne_cy - iris_r + lid // 2 - gaze_up,
                  ne_cx + iris_r, ne_cy + iris_r - gaze_up],
                 fill=BYTE_TEAL, outline=VOID_BLACK, width=1)

    # Cracked eye (left)
    ce_cx = torso_cx - eye_sep
    ce_cy = eye_cy
    draw.ellipse([ce_cx - e_r, ce_cy - int(e_r * 0.75),
                  ce_cx + e_r, ce_cy + int(e_r * 0.75)],
                 fill=VOID_BLACK, outline=ELEC_CYAN_DIM, width=1)
    # Main crack line
    draw.line([(ce_cx - e_r + 2, ce_cy - int(e_r * 0.65)),
               (ce_cx + e_r - 2, ce_cy + int(e_r * 0.65))],
              fill=CRACK_LINE, width=1)
    # Alive eye dot — shifted upward to match level-forward/contempt gaze direction
    # Sits at left-center rather than lower-left, consistent with outward-level aim
    draw.ellipse([ce_cx - int(e_r * 0.38) - 2, ce_cy - int(e_r * 0.06),
                  ce_cx - int(e_r * 0.38) + 4, ce_cy - int(e_r * 0.06) + 4],
                 fill=ELEC_CYAN)

    # ── EXPRESSION — grudging assessment ─────────────────────────────────────
    # Mouth: narrow flat line — slightly downturned at corners (reluctant)
    mouth_y = head_cy + int(head_r * 0.40)
    mouth_hw = int(head_r * 0.50)
    draw.line([(torso_cx - mouth_hw, mouth_y),
               (torso_cx + mouth_hw, mouth_y)],
              fill=VOID_BLACK, width=2)
    # Slightly downturned corners
    draw.line([(torso_cx - mouth_hw, mouth_y),
               (torso_cx - mouth_hw - 3, mouth_y + 3)],
              fill=VOID_BLACK, width=2)
    draw.line([(torso_cx + mouth_hw, mouth_y),
               (torso_cx + mouth_hw + 3, mouth_y + 3)],
              fill=VOID_BLACK, width=2)

    # ── PIXEL TRAILS / CONFETTI still drifting from emergence ────────────────
    # Faint magenta + cyan pixel sparks floating upward and outward
    for spark_seed in range(20):
        srng = random.Random(spark_seed * 131 + 7)
        # Drift pattern: sparks fall upward + spread left/right (post-emergence)
        dx = srng.randint(-int(body_h * 1.8), int(body_h * 1.8))
        dy = -srng.randint(int(body_h * 0.2), int(body_h * 2.2))   # upward
        sx = torso_cx + dx
        sy = torso_top_y + dy
        if sy > 0 and sx > 0 and sx < PW:
            spark_size = srng.randint(2, 5)
            col = CONFETTI_C if srng.randint(0, 2) != 0 else CONFETTI_M
            alpha_fade = max(0, 255 - abs(dy) // 2)
            draw.rectangle([sx, sy, sx + spark_size, sy + spark_size], fill=col)

    # Trailing pixel artifacts from emergence — elongated streaks downward from Byte
    for trail_i in range(5):
        trng = random.Random(trail_i * 43 + 200)
        tx = torso_cx + trng.randint(-20, 20)
        ty_start = torso_top_y - trng.randint(5, 25)
        ty_end   = ty_start + trng.randint(8, 20)
        col = ELEC_CYAN_DIM if trng.randint(0, 1) == 0 else CRACK_LINE
        draw.line([(tx, ty_start), (tx, ty_end)], fill=col, width=1)


def draw_desaturation_ring(draw, byte_cx, byte_floor_y, radius):
    """Thin ring of desaturated floor around Byte's feet — digital bleaching effect."""
    # Ellipse on floor plane
    rw = radius
    rh = int(radius * 0.35)   # floor perspective foreshortening
    ring_y = byte_floor_y
    for r_offset in range(3):
        rw2 = rw + r_offset * 4
        rh2 = rh + r_offset * 1
        draw.ellipse([byte_cx - rw2, ring_y - rh2,
                      byte_cx + rw2, ring_y + rh2],
                     outline=DESAT_RING, width=1)


def draw_scene(img):
    draw = ImageDraw.Draw(img)

    # ── Background: Grandma's tech den floor level ────────────────────────────
    # Camera is 6" off the floor — Byte's eye level.
    # We see: floor dominant in lower frame, wall/shelving BG.
    # The camera is at THE FLOOR — horizon is very low.

    # Horizon line is very low (camera at floor level)
    horizon_y = int(DRAW_H * 0.38)   # low horizon, floor dominant

    # Wall (warm background)
    draw.rectangle([0, 0, PW, horizon_y], fill=WALL_WARM)
    # Shelving/equipment silhouettes on back wall (BG — blurred)
    for shelf_x, shelf_y, shelf_w, shelf_h in [
        (10, int(DRAW_H * 0.05), int(PW * 0.22), int(DRAW_H * 0.28)),
        (int(PW * 0.58), int(DRAW_H * 0.03), int(PW * 0.20), int(DRAW_H * 0.22)),
        (int(PW * 0.82), int(DRAW_H * 0.06), int(PW * 0.16), int(DRAW_H * 0.24)),
    ]:
        draw.rectangle([shelf_x, shelf_y, shelf_x + shelf_w, shelf_y + shelf_h],
                       fill=WALL_SHADOW)
    # Warm ambient glow (den lamp)
    add_glow(img, int(PW * 0.85), int(DRAW_H * 0.08), 160, WARM_AMB, steps=4, max_alpha=18)
    draw = ImageDraw.Draw(img)

    # CRT monitor BG (the one Byte just came through — returning to static)
    # Defocused — just a shape in BG left of center
    crt_bx = int(PW * 0.32)
    crt_by = int(DRAW_H * 0.03)
    crt_bw = int(PW * 0.20)
    crt_bh = int(DRAW_H * 0.22)
    draw.rectangle([crt_bx, crt_by, crt_bx + crt_bw, crt_by + crt_bh],
                   fill=CRT_PLASTIC, outline=LINE_DARK, width=2)
    # Screen: returning to normal static
    scr_margin = 12
    draw.rectangle([crt_bx + scr_margin, crt_by + scr_margin,
                    crt_bx + crt_bw - scr_margin, crt_by + crt_bh - scr_margin],
                   fill=STATIC_GREY)
    # Scan lines on screen
    for sl_y in range(crt_by + scr_margin, crt_by + crt_bh - scr_margin, 4):
        draw.line([(crt_bx + scr_margin, sl_y), (crt_bx + crt_bw - scr_margin, sl_y)],
                  fill=STATIC_DIM, width=1)
    # Faint residual glow (not fully settled)
    add_glow(img, crt_bx + crt_bw // 2, crt_by + crt_bh // 2,
             50, ELEC_CYAN, steps=4, max_alpha=20)
    draw = ImageDraw.Draw(img)
    # Annotation: CRT returning to static
    draw.text((crt_bx + 2, crt_by + crt_bh + 2), "CRT: returning\nto static",
              font=load_font(9), fill=ELEC_CYAN_DIM)

    # Wall-to-floor boundary
    draw.line([(0, horizon_y), (PW, horizon_y)], fill=FLOOR_SHADOW, width=2)

    # Floor (warm, seen from near-floor camera — takes up majority of lower frame)
    draw.rectangle([0, horizon_y, PW, DRAW_H], fill=FLOOR_WARM)
    # Floor perspective lines (very shallow at this camera height)
    vp_x = int(PW * 0.50)
    vp_y = horizon_y
    for line_i, frac in enumerate([0.08, 0.22, 0.38, 0.55, 0.68, 0.82, 0.94]):
        fx = int(frac * PW)
        draw.line([(vp_x, vp_y), (fx, DRAW_H)], fill=FLOOR_SHADOW, width=1)

    # ── Cable bundles on floor (Byte's clearing) ─────────────────────────────
    # Byte stands in a CLEARING between cable bundles — his head is barely
    # above them. Cables run across the floor in bundles.

    # Cable bundle left of Byte
    for ci in range(4):
        cx_offset = 0 + ci * 3
        draw.line([(0, int(DRAW_H * 0.58) + ci * 5),
                   (int(PW * 0.30), int(DRAW_H * 0.82) + ci * 3)],
                  fill=CABLE_DARK if ci % 2 == 0 else CABLE_MED, width=5 - ci)

    # Cable bundle right of Byte
    for ci in range(4):
        cx_offset = ci * 3
        draw.line([(PW, int(DRAW_H * 0.62) + ci * 4),
                   (int(PW * 0.68), int(DRAW_H * 0.80) + ci * 3)],
                  fill=CABLE_DARK if ci % 2 == 0 else CABLE_MED, width=5 - ci)

    # Cable bundle coiling in FG (near-camera, thick — low angle exaggerates these)
    draw.arc([int(PW * 0.03), int(DRAW_H * 0.82),
              int(PW * 0.28), DRAW_H + 30],
             start=160, end=340, fill=CABLE_DARK, width=8)
    draw.arc([int(PW * 0.68), int(DRAW_H * 0.84),
              int(PW * 0.96), DRAW_H + 40],
             start=200, end=360, fill=CABLE_DARK, width=7)

    # ── Byte's position — center of clearing ─────────────────────────────────
    byte_cx      = int(PW * 0.52)
    byte_floor_y = int(DRAW_H * 0.78)      # where Byte stands on the floor
    body_h       = int(DRAW_H * 0.28)      # Byte's full height in panel pixels
                                            # = ~75px at DRAW_H=540 — reads TINY

    # Desaturation ring at Byte's feet (digital bleaching)
    draw_desaturation_ring(draw, byte_cx, byte_floor_y, int(body_h * 0.55))

    # ELEC_CYAN ambient glow (Byte himself radiates)
    add_glow(img, byte_cx, byte_floor_y - body_h // 2, body_h // 2,
             ELEC_CYAN, steps=5, max_alpha=35)
    draw = ImageDraw.Draw(img)

    # Draw Byte
    draw_byte_full_body(img, draw, byte_cx, byte_floor_y, body_h)
    draw = ImageDraw.Draw(img)

    # ── Size annotation arrow — Byte is TINY ─────────────────────────────────
    # Double-headed arrow showing Byte's height alongside him
    ann_x = byte_cx + int(body_h * 0.85)
    ann_top = byte_floor_y - body_h
    ann_bot = byte_floor_y
    draw.line([(ann_x, ann_top), (ann_x, ann_bot)],
              fill=ELEC_CYAN_DIM, width=1)
    draw.polygon([(ann_x - 4, ann_top + 8), (ann_x + 4, ann_top + 8),
                  (ann_x, ann_top)], fill=ELEC_CYAN_DIM)
    draw.polygon([(ann_x - 4, ann_bot - 8), (ann_x + 4, ann_bot - 8),
                  (ann_x, ann_bot)], fill=ELEC_CYAN_DIM)
    draw.text((ann_x + 5, (ann_top + ann_bot) // 2 - 6),
              "~6\"", font=load_font(10), fill=ELEC_CYAN_DIM)

    # ── Panel annotations ─────────────────────────────────────────────────────
    font_ann   = load_font(11)
    font_ann_b = load_font(11, bold=True)

    draw.text((10, 8), "P08  /  MED  /  eye level (~6\" off floor — Byte's scale)  /  STATIC",
              font=font_ann, fill=ANN_COL)
    draw.text((10, 20), "Byte: full body reveal — standing in real world — TINY (head barely above cables)",
              font=font_ann, fill=ANN_DIM)
    draw.text((10, 32), "Gaze: level-forward (contempt/superiority). NOT downward. Desat ring at feet.",
              font=font_ann, fill=ANN_DIM)

    # Dialogue notation at Byte
    dial_y = byte_floor_y - body_h - 28
    dial_x = byte_cx - int(body_h * 0.4)
    draw.text((dial_x, dial_y), "\"Ugh.\"",
              font=font_ann_b, fill=WARM_CREAM)
    draw.text((dial_x - 15, dial_y + 13), "\"The flesh dimension.\"",
              font=load_font(10), fill=(200, 190, 170))

    # Shot label
    draw.rectangle([10, DRAW_H - 24, 92, DRAW_H - 6], fill=(40, 20, 10))
    draw.text((14, DRAW_H - 22), "MED / STATIC",
              font=font_ann_b, fill=(240, 220, 140))

    # Arc indicator
    draw.rectangle([PW - 120, DRAW_H - 24, PW - 10, DRAW_H - 6], fill=(40, 0, 20))
    draw.text((PW - 116, DRAW_H - 22), "ARC: TENSE",
              font=font_ann_b, fill=ARC_TENSE)

    return draw


def make_panel():
    font_cap  = load_font(12)
    font_ann  = load_font(11)
    font_sm   = load_font(10)

    img  = Image.new('RGB', (PW, PH), WALL_WARM)
    draw_scene(img)
    draw = ImageDraw.Draw(img)

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(10, 8, 6), width=2)
    draw.text((10, DRAW_H + 4),
              "P08  MED  eye-level (Byte's ~6\" scale)  |  Byte full reveal — flesh dimension",
              font=font_cap, fill=(160, 155, 130))
    draw.text((10, DRAW_H + 18),
              "Byte standing in clearing between cable bundles. TINY. Confetti drifting. Desat ring at feet.",
              font=font_cap, fill=TEXT_CAP)
    draw.text((10, DRAW_H + 33),
              "\"Ugh. The flesh dimension.\" — Expression: disgust cycling through assessment to reluctant OK.",
              font=font_ann, fill=(150, 140, 110))
    draw.text((PW - 230, DRAW_H + 46), "LTG_SB_cold_open_P08  /  Diego Vargas  /  C42",
              font=font_sm, fill=(100, 95, 78))

    # Arc border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=ARC_TENSE, width=3)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("P08 standalone panel generation complete.")
