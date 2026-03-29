#!/usr/bin/env python3
"""
LTG_CHAR_luma_expression_sheet_v005.py
Luma Expression Sheet — v005 FULL BODY
"Luma & the Glitchkin" — Cycle 25 / Maya Santos

CRITICAL FIX from v004: The v004 sheet is a bust/head sheet — body language invisible.
Critique 11: "Four of six expressions are indistinguishable below the neck."

v005 changes:
  - FULL BODY visible in every panel (head to feet)
  - Every expression has a UNIQUE BODY POSTURE that reads at silhouette level
  - Body pose, arm position, AND weight shift per expression
  - Canvas: 1200×900, 3×2, 6 expressions

Cycle 26 STYLE FIX: Aligned to classroom pose visual language (producer preference).
  - Head: circle + cheek nubs (no jaw bump) — matches classroom pose
  - Hair: 8-ellipse cloud mass (organic, puffy) — matches classroom pose
  - Eyes: circular proportions, eyelid arc — matches classroom pose
  - Line weights: silhouette=6px@2x(→3px@1x), interior=4px@2x(→2px@1x)
  - Background: warm light per-panel tones — matches classroom warm aesthetic
  - CANVAS_BG: warm parchment instead of dark void

Expression silhouette differentiation:
  CURIOUS:    Forward lean, one arm reaching/pointing, weight shifted forward
  DETERMINED: Upright, fists at hips, forward weight, wide stance
  SURPRISED:  Backward lean, arms OUT to sides, weight shifted back
  WORRIED:    Contracted, arms crossed over chest, weight centered, slight hunch
  DELIGHTED:  Jump/bounce posture, both arms raised, feet off ground
  FRUSTRATED: Arms crossed, feet apart, backward lean, head lowered

2× render + LANCZOS AA as per production standard.
show_guides=False for pitch export (no construction guide overlaid).

Output: output/characters/main/LTG_CHAR_luma_expression_sheet_v005.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Palette ──────────────────────────────────────────────────────────────────
SKIN       = (200, 136, 90)
SKIN_SH    = (160, 104, 64)
SKIN_HL    = (223, 160, 112)
HAIR       = ( 26,  15, 10)
HAIR_HL    = ( 61,  31, 15)
EYE_W      = (250, 240, 220)
EYE_IRIS   = (200, 125, 62)
EYE_PUP    = ( 59,  40, 32)
EYE_HL     = (240, 240, 240)
BLUSH_C    = (232, 148, 100)
LINE       = ( 59,  40, 32)
HOODIE     = (232, 112, 42)
HOODIE_SH  = (184,  74, 32)
HOODIE_HL  = (245, 144, 80)
PANTS      = ( 42,  40, 80)
PANTS_SH   = ( 26,  24, 48)
SHOE       = (245, 232, 208)
SHOE_SOLE  = (199,  91, 57)
LACES      = (  0, 240, 255)
PX_CYAN    = (  0, 240, 255)
PX_MAG     = (255,  45, 107)
CANVAS_BG  = (235, 224, 206)   # warm parchment — matches classroom pose aesthetic

# Hoodie color tint per expression (panel atmosphere)
HOODIE_MAP = {
    "CURIOUS":    (150, 175, 200),   # cool blue-gray hoodie
    "DETERMINED": (155,  85, 45),    # warm amber-red
    "SURPRISED":  (232, 112, 42),    # full orange
    "WORRIED":    ( 80, 100, 140),   # muted indigo
    "DELIGHTED":  (232, 112, 42),    # full orange
    "FRUSTRATED": (135,  75, 65),    # muted terracotta
}

BG = {
    "CURIOUS":    (230, 240, 235),   # soft warm mint — classroom warmth
    "DETERMINED": (238, 228, 210),   # warm parchment — grounded
    "SURPRISED":  (245, 234, 210),   # warm cream
    "WORRIED":    (225, 230, 242),   # pale blue-gray
    "DELIGHTED":  (250, 238, 215),   # warm golden cream
    "FRUSTRATED": (235, 220, 220),   # pale rose — muted heat
}

# ── Layout ────────────────────────────────────────────────────────────────────
COLS      = 3
ROWS      = 2
PAD       = 20
HEADER    = 58
LABEL_H   = 36
TOTAL_W   = 1200
TOTAL_H   = 900
PANEL_W   = (TOTAL_W - PAD * (COLS + 1)) // COLS   # ~373px
PANEL_H   = (TOTAL_H - HEADER - PAD * (ROWS + 1) - LABEL_H * ROWS) // ROWS   # ~370px

RENDER_SCALE = 2

# Character proportions in render space (2x)
# HEAD_R: the "unit" — everything is relative
HEAD_R   = 52   # head radius at 1x (1200px canvas) — smaller to fit full body
HR       = HEAD_R * RENDER_SCALE   # 104 at 2x


# ── Geometry helpers ──────────────────────────────────────────────────────────
def bezier3(p0, p1, p2, steps=40):
    pts = []
    for i in range(steps + 1):
        t  = i / steps
        x  = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
        y  = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        pts.append((x, y))
    return pts


def polyline(draw, pts, color, width=2):
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill=color, width=width)


def arc_draw(draw, cx, cy, rx, ry, a0, a1, color, width=3, steps=50):
    pts = []
    for i in range(steps + 1):
        t = math.radians(a0 + (a1 - a0) * i / steps)
        pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    polyline(draw, pts, color, width)


# ── Drawing functions ─────────────────────────────────────────────────────────

def draw_hoodie_pixel_accent(draw, x0, y0, pw, ph, hoodie_col):
    """Simple pixel accent on hoodie chest."""
    import random
    rng = random.Random(99)
    for _ in range(8):
        px = rng.randint(x0 + 3, x0 + pw - 4)
        py = rng.randint(y0 + 3, y0 + ph - 4)
        sz = rng.choice([2, 3])
        c  = rng.choice([PX_CYAN, PX_MAG, (240, 240, 240)])
        draw.rectangle([px, py, px + sz, py + sz], fill=c)


def draw_head(draw, cx, cy):
    """Classroom-style head: main circle + lower-half fill + cheek nubs."""
    # Main head circle
    draw.ellipse([cx - HR, cy - HR, cx + HR, cy + HR + int(HR * 0.15)],
                 fill=SKIN, outline=LINE, width=6)
    # Lower chin fill (repeat lower half to soften chin)
    chin_rx = int(HR * 0.95)
    draw.ellipse([cx - chin_rx, cy - int(HR * 0.20),
                  cx + chin_rx, cy + HR + int(HR * 0.25)], fill=SKIN)
    draw.arc([cx - chin_rx, cy - int(HR * 0.20),
              cx + chin_rx, cy + HR + int(HR * 0.25)],
             start=0, end=180, fill=LINE, width=6)
    # Cheek nubs — classroom pose characteristic
    nub_w = int(HR * 0.18)
    nub_h = int(HR * 0.24)
    nub_y = cy - int(HR * 0.12)
    draw.ellipse([cx - HR - nub_w + int(HR * 0.06), nub_y - nub_h // 2,
                  cx - HR + nub_w + int(HR * 0.06), nub_y + nub_h // 2],
                 fill=SKIN, outline=LINE, width=4)
    draw.ellipse([cx + HR - nub_w - int(HR * 0.06), nub_y - nub_h // 2,
                  cx + HR + nub_w - int(HR * 0.06), nub_y + nub_h // 2],
                 fill=SKIN, outline=LINE, width=4)


def draw_ears(draw, cx, cy):
    """Ears are absorbed into cheek nubs for classroom-style look."""
    pass   # cheek nubs in draw_head() serve as ear/cheek indicators


def draw_hair(draw, cx, cy, variant="default"):
    """Classroom-style cloud hair: 8+ overlapping ellipses for organic puff.
    Scaled to 2x render coords (HR = HEAD_R * RENDER_SCALE).
    """
    # Scale classroom hair values (originally at head_r=100) to current HR
    s = HR / 100.0   # scale factor

    if variant == "excited":
        v_off = -int(s * 15)   # hair floats higher
        spread = int(s * 10)
    elif variant == "drooped":
        v_off = int(s * 8)     # hair droops slightly
        spread = -int(s * 5)
    elif variant == "tight":
        v_off = int(s * 4)     # hair hugs head tighter
        spread = -int(s * 8)
    else:
        v_off = 0
        spread = 0

    # Main cloud mass — 8 overlapping ellipses (classroom pose method)
    # Ellipse coords scaled from classroom pose (cx-relative, cy-relative)
    hair_ellipses = [
        # (x1_off, y1_off, x2_off, y2_off) — from classroom pose _draw_luma_hair_seated
        (-int(s*155), -int(s*195)+v_off, int(s*145)+spread, int(s*40)),
        (-int(s*175)+spread//2, -int(s*170)+v_off, -int(s*80), -int(s*60)),
        (-int(s*165), -int(s*140)+v_off, -int(s*95), -int(s*30)),
        ( int(s*80), -int(s*160)+v_off,  int(s*155)+spread, -int(s*60)),
        ( int(s*90), -int(s*130)+v_off,  int(s*145)+spread, -int(s*40)),
        (-int(s*60), -int(s*215)+v_off,  int(s*20),   -int(s*140)),
        (-int(s*20), -int(s*225)+v_off,  int(s*70),   -int(s*145)),
        (-int(s*100),-int(s*200)+v_off,  -int(s*30),  -int(s*130)),
    ]
    for (x1, y1, x2, y2) in hair_ellipses:
        draw.ellipse([cx + x1, cy + y1, cx + x2, cy + y2], fill=HAIR)

    # Hair highlight strands (foreground arcs — classroom _draw_hair_overlay)
    draw.arc([cx - int(s*60), cy - int(s*195) + v_off,
              cx - int(s*10), cy - int(s*140)],
             start=30, end=200, fill=HAIR, width=6)
    draw.arc([cx - int(s*20), cy - int(s*190) + v_off,
              cx + int(s*40), cy - int(s*130)],
             start=10, end=190, fill=HAIR, width=6)


def draw_eyes_full(draw, cx, cy, params):
    """Classroom-style eyes: near-circular proportions, explicit eyelid arc.
    Scaled to 2x render coords (classroom used head_r=100, ew=28).
    """
    s = HR / 100.0   # scale from classroom reference
    eye_y  = cy - int(s * 18)   # classroom: cy - 18
    lex    = cx - int(s * 38)   # classroom: cx - 38
    rex    = cx + int(s * 38)   # classroom: cx + 38
    ew     = int(s * 28)        # classroom: ew=28 (near-circular)
    p      = params

    # Determine openness per eye — classroom style: leh and reh
    leh_base = int(s * 28)   # classroom: leh=28 (full open)
    reh_base = int(s * 22)   # classroom: reh=22 (slightly less)
    l_open   = p.get("l_open", 1.0)
    r_open   = p.get("r_open", 1.0)

    if p.get("half_lid"):
        leh = max(4, int(leh_base * 0.50))
        reh = max(4, int(reh_base * 0.50))
    else:
        leh = max(4, int(leh_base * l_open))
        reh = max(4, int(reh_base * r_open))

    pdx = int(p.get("gaze_dx", 0) * s * 5)
    pdy = int(p.get("gaze_dy", 0) * s * 4)

    for (ex, eh, is_right) in [(lex, leh, False), (rex, reh, True)]:
        # Eye white — oval, near-circular
        draw.ellipse([ex - ew, eye_y - eh, ex + ew, eye_y + eh], fill=EYE_W,
                     outline=LINE, width=4)
        # Iris
        iris_r = int(ew * 0.54)
        iry    = min(iris_r, eh - 2)
        if iry < 2:
            iry = 2
        draw.chord([ex + pdx - iris_r, eye_y + pdy - iry,
                    ex + pdx + iris_r, eye_y + pdy + iry],
                   start=15, end=345, fill=EYE_IRIS)
        # Pupil
        pr = int(iris_r * 0.64) if p.get("pupils_wide") else int(iris_r * 0.50)
        pup_x = ex + pdx
        draw.ellipse([pup_x - pr, eye_y + pdy - pr,
                      pup_x + pr, eye_y + pdy + pr], fill=EYE_PUP)
        # Highlight
        hl_x = pup_x + int(iris_r * 0.42)
        hl_y = eye_y + pdy - int(iry * 0.48)
        hl_s = max(int(pr * 0.38), 4)
        draw.ellipse([hl_x - hl_s, hl_y - hl_s, hl_x + hl_s, hl_y + hl_s],
                     fill=EYE_HL)
        # Eyelid arc (classroom style: arc at bottom of eye oval)
        draw.arc([ex - ew, eye_y - eh, ex + ew, eye_y + eh],
                 start=200, end=340, fill=LINE, width=4)
        # Crinkle lines for DELIGHTED
        if p.get("crinkle"):
            dsign   = 1 if is_right else -1
            outer_x = ex + ew * dsign
            for k in range(3):
                dy_k = int(s * 4) * k
                draw.line([(outer_x, eye_y + dy_k),
                           (outer_x + dsign * int(s * 11),
                            eye_y + dy_k - int(s * 7))],
                          fill=LINE, width=3)

    # Brows — interior weight (4px at 2x = 2px at 1x, matches classroom)
    brow_base_y = eye_y - int(leh_base * 1.42)
    for (bx, b_dy, b_furrow) in [
        (lex, p.get("brow_l_dy", 0), p.get("brow_furrow_l", False)),
        (rex, p.get("brow_r_dy", 0), p.get("brow_furrow_r", False)),
    ]:
        by         = brow_base_y + b_dy
        is_right_b = (bx == rex)
        # Classroom brow shape: 3-point polyline with gentle arch
        inner_x = bx + int(s * 22) if is_right_b else bx - int(s * 22)
        outer_x = bx - int(s * 26) if is_right_b else bx + int(s * 26)
        inner_y = by + (int(s * 8) if b_furrow else int(s * 2))
        outer_y = by + (0 if b_furrow else int(s * 2))
        brow_pts = [(outer_x, outer_y), (bx, by - int(s * 6)), (inner_x, inner_y)]
        draw.line(brow_pts, fill=HAIR, width=4)


def draw_nose(draw, cx, cy):
    """Classroom-style nose: two small nostril dots + bridge arc."""
    s = HR / 100.0
    # Nostril dots (classroom: two small ellipses at cy+8/14)
    draw.ellipse([cx - int(s*8), cy + int(s*8),  cx - int(s*2), cy + int(s*14)],
                 fill=SKIN_SH)
    draw.ellipse([cx + int(s*2), cy + int(s*8),  cx + int(s*8), cy + int(s*14)],
                 fill=SKIN_SH)
    draw.arc([cx - int(s*6), cy - int(s*10), cx + int(s*6), cy + int(s*12)],
             start=200, end=340, fill=SKIN_SH, width=4)


def draw_mouth(draw, cx, cy, style="neutral"):
    """Classroom-style mouth: scaled from classroom head_r=100 reference."""
    s  = HR / 100.0
    my = cy + int(s * 30)    # classroom: cy + 30
    mw = int(s * 36)         # classroom: mouth_r=36
    lx, rx = cx - mw, cx + mw

    if style == "neutral":
        # Classroom asymmetric-ish gentle curve
        pts = bezier3((lx, my + int(s*4)), (cx, my - int(s*8)), (rx, my + int(s*4)))
        polyline(draw, pts, LINE, width=6)
    elif style == "smile_closed":
        pts = bezier3((lx, my + int(s*4)), (cx, my - int(s*20)), (rx, my + int(s*4)))
        polyline(draw, pts, LINE, width=6)
        draw.line([(lx, my + int(s*4)), (lx - int(s*5), my + int(s*14))],
                  fill=LINE, width=4)
        draw.line([(rx, my + int(s*4)), (rx + int(s*5), my + int(s*14))],
                  fill=LINE, width=4)
    elif style == "smile_big":
        sh    = int(s * 22)
        top_p = bezier3((lx, my), (cx, my - int(s*28)), (rx, my))
        bot_p = bezier3((lx, my + sh), (cx, my + sh + int(s*10)), (rx, my + sh))
        fill_pts = top_p + bot_p[::-1]
        draw.polygon(fill_pts, fill=(210, 70, 50))
        tw_m = int(mw * 0.82)
        draw.rectangle([cx - tw_m, my - 2, cx + tw_m, my + sh - 4],
                       fill=(248, 242, 230))
        polyline(draw, top_p, LINE, width=6)
        polyline(draw, bot_p, LINE, width=5)
        draw.line([(lx, my), (lx, my + sh)], fill=LINE, width=5)
        draw.line([(rx, my), (rx, my + sh)], fill=LINE, width=5)
    elif style == "open_oval":
        ow = int(mw * 0.54)
        oh = int(s * 28)
        draw.ellipse([cx - ow, my - int(oh * 0.38), cx + ow, my + int(oh * 0.62)],
                     fill=(210, 65, 48))
        draw.ellipse([cx - ow, my - int(oh * 0.38), cx + ow, my + int(oh * 0.62)],
                     outline=LINE, width=5)
    elif style == "pressed_flat":
        pts = bezier3((lx, my + int(s*4)), (cx, my + int(s*8)), (rx, my + int(s*4)))
        polyline(draw, pts, LINE, width=6)
    elif style == "corners_down":
        pts = bezier3((lx, my - int(s*12)), (cx, my + int(s*16)), (rx, my - int(s*12)))
        polyline(draw, pts, LINE, width=5)
    elif style == "frown_slight":
        pts = bezier3((lx, my - int(s*6)), (cx, my + int(s*14)), (rx, my - int(s*6)))
        polyline(draw, pts, LINE, width=5)


def draw_blush(draw, cx, cy, alpha=0):
    """Classroom-style blush: ovals beside face at cheek level."""
    if alpha <= 0:
        return
    s  = HR / 100.0
    bw = int(s * 28)   # classroom: width ~58px total = 29 half
    bh = int(s * 14)
    by = cy + int(s * 20)   # classroom: cy+5 to cy+35 = center cy+20
    # Blush positions at cheek level (near cheek nubs)
    for bx in [cx - int(s * 80), cx + int(s * 80)]:
        # Use RGBA-capable fill if available
        draw.ellipse([bx - bw, by - bh, bx + bw, by + bh], fill=BLUSH_C)


def draw_body_pose(draw, cx, head_cy, hoodie_col, pose):
    """
    Draw full body: torso, arms, legs, shoes.
    pose dict keys:
      body_tilt: int — torso lean (positive=right, negative=left tilt in px)
      arm_l: tuple (dx_start, dy_start, dx_end, dy_end) — arm from shoulder
      arm_r: tuple (dx_start, dy_start, dx_end, dy_end)
      leg_l: tuple (dx_top, dy_top, dx_bot, dy_bot) — leg from hip
      leg_r: tuple
      feet_off_ground: bool — both feet floating (DELIGHTED bounce)
      weight: "forward" | "back" | "centered" — weight shift (affects shoe positioning)
    """
    tilt = pose.get("body_tilt", 0)

    # Neck base = below head
    neck_y  = head_cy + HR + int(HR * 0.10)
    neck_cx = cx + tilt

    # Torso dimensions (A-line hoodie)
    torso_top_w = int(HR * 0.70)
    torso_bot_w = int(HR * 0.90)   # A-line widens at hem
    torso_h     = int(HR * 1.80)
    torso_top_y = neck_y + int(HR * 0.08)
    torso_bot_y = torso_top_y + torso_h

    # Hip center (used for leg attachment)
    hip_cx = neck_cx + tilt // 2   # slight lean propagation

    # Draw torso (trapezoid — A-line silhouette)
    torso_pts = [
        (neck_cx - torso_top_w, torso_top_y),
        (neck_cx + torso_top_w, torso_top_y),
        (hip_cx  + torso_bot_w, torso_bot_y),
        (hip_cx  - torso_bot_w, torso_bot_y),
    ]
    draw.polygon(torso_pts, fill=hoodie_col)

    # Shadow flank (right side of torso)
    shadow_pts = [
        (neck_cx + torso_top_w - int(HR * 0.15), torso_top_y),
        (neck_cx + torso_top_w, torso_top_y),
        (hip_cx  + torso_bot_w, torso_bot_y),
        (hip_cx  + torso_bot_w - int(HR * 0.20), torso_bot_y),
    ]
    draw.polygon(shadow_pts, fill=HOODIE_SH)
    draw.polygon(torso_pts, outline=LINE, width=6)

    # Hood rim (cream lining at neckline)
    draw.rectangle([neck_cx - torso_top_w + 4, torso_top_y,
                    neck_cx + torso_top_w - 4, torso_top_y + int(HR * 0.18)],
                   fill=(250, 232, 200))

    # Pixel accent on chest
    px_x0 = neck_cx - int(HR * 0.28)
    px_y0 = torso_top_y + int(HR * 0.22)
    draw_hoodie_pixel_accent(draw, px_x0, px_y0,
                             int(HR * 0.56), int(HR * 0.44), hoodie_col)

    # Pocket bump at hem
    draw.rectangle([hip_cx - int(HR * 0.32), torso_bot_y - int(HR * 0.28),
                    hip_cx + int(HR * 0.32), torso_bot_y],
                   fill=HOODIE_SH, outline=LINE, width=2)

    # Neck (skin)
    draw.rectangle([neck_cx - int(HR * 0.22), neck_y,
                    neck_cx + int(HR * 0.22), torso_top_y + int(HR * 0.05)],
                   fill=SKIN)
    draw.rectangle([neck_cx - int(HR * 0.22), neck_y,
                    neck_cx + int(HR * 0.22), torso_top_y + int(HR * 0.05)],
                   outline=LINE, width=4)

    # === ARMS ===
    arm_specs = [
        ("arm_l", pose.get("arm_l"), neck_cx - torso_top_w + int(HR * 0.10), torso_top_y + int(HR * 0.10)),
        ("arm_r", pose.get("arm_r"), neck_cx + torso_top_w - int(HR * 0.10), torso_top_y + int(HR * 0.10)),
    ]
    arm_w = int(HR * 0.28)   # arm thickness
    for (key, arm_data, shoulder_x, shoulder_y) in arm_specs:
        if arm_data is None:
            continue
        end_x = shoulder_x + arm_data[0]
        end_y = shoulder_y + arm_data[1]
        # Arm as thick bezier
        mid_x = (shoulder_x + end_x) // 2 + arm_data[2] if len(arm_data) > 2 else (shoulder_x + end_x) // 2
        mid_y = (shoulder_y + end_y) // 2 + arm_data[3] if len(arm_data) > 3 else (shoulder_y + end_y) // 2
        pts   = bezier3((shoulder_x, shoulder_y), (mid_x, mid_y), (end_x, end_y))
        polyline(draw, pts, hoodie_col, width=arm_w * 2)
        polyline(draw, pts, LINE, width=5)
        # Mitten hand
        hand_r = int(HR * 0.22)
        draw.ellipse([end_x - hand_r, end_y - hand_r * 2 // 3,
                      end_x + hand_r, end_y + hand_r * 2 // 3],
                     fill=SKIN, outline=LINE, width=4)

    # === LEGS ===
    pants_h = int(HR * 1.60)
    leg_w   = int(HR * 0.38)
    leg_l_spec = pose.get("leg_l", (0, 0))   # (dx at knee, dx at foot) relative to hip_cx - leg offset
    leg_r_spec = pose.get("leg_r", (0, 0))

    feet_off = pose.get("feet_off_ground", False)
    ground_y = torso_bot_y + pants_h + int(HR * 0.30)   # foot y position

    for side in [-1, 1]:
        hip_x   = hip_cx + side * int(HR * 0.42)
        spec    = leg_l_spec if side < 0 else leg_r_spec
        knee_dx = spec[0]
        foot_dx = spec[1]
        foot_lift = spec[2] if len(spec) > 2 else 0   # positive = up from ground

        knee_x = hip_x + knee_dx
        knee_y = torso_bot_y + pants_h // 2
        foot_x = hip_x + foot_dx
        foot_y = ground_y - foot_lift

        # Upper leg
        draw.rectangle([hip_x  - leg_w // 2, torso_bot_y - int(HR * 0.08),
                         hip_x  + leg_w // 2, knee_y],
                        fill=PANTS)
        draw.rectangle([hip_x  - leg_w // 2, torso_bot_y - int(HR * 0.08),
                         hip_x  + leg_w // 2, knee_y],
                        outline=LINE, width=3)
        # Lower leg (can angle)
        pts = bezier3(
            (hip_x, knee_y),
            ((knee_x + foot_x) // 2, (knee_y + foot_y) // 2),
            (foot_x, foot_y)
        )
        polyline(draw, pts, PANTS, width=leg_w * 2)
        polyline(draw, pts, LINE, width=4)

        # Shoe
        shoe_w = int(HR * 0.50)
        shoe_h = int(HR * 0.28)
        # Sole
        draw.ellipse([foot_x - shoe_w + 2, foot_y + shoe_h - int(HR * 0.06),
                      foot_x + shoe_w - 2, foot_y + shoe_h + int(HR * 0.14)],
                     fill=SHOE_SOLE)
        # Upper
        draw.ellipse([foot_x - shoe_w + 4, foot_y - int(HR * 0.04),
                      foot_x + shoe_w - 4, foot_y + shoe_h],
                     fill=SHOE)
        draw.ellipse([foot_x - shoe_w + 4, foot_y - int(HR * 0.04),
                      foot_x + shoe_w - 4, foot_y + shoe_h],
                     outline=LINE, width=3)
        # Laces (cyan)
        for li in range(3):
            ly = foot_y + li * 3
            draw.line([foot_x - int(shoe_w * 0.35), ly,
                       foot_x + int(shoe_w * 0.35), ly],
                      fill=LACES, width=1)


# ── Expression specs ──────────────────────────────────────────────────────────
# Every expression has a DISTINCT BODY POSE for silhouette differentiation.
# Confirmed squint-test differentiation for each:
#
# CURIOUS:     forward tilt, left arm reaches forward, weight ahead → angled lean silhouette
# DETERMINED:  upright, both arms at hips (fists), wide stance → symmetric stable block
# SURPRISED:   backward tilt, arms fly out to sides, weight back → open expansive silhouette
# WORRIED:     arms crossed chest, legs together, slight hunch → contracted narrow silhouette
# DELIGHTED:   both arms up high, feet lifted off ground, side lean → celebratory high silhouette
# FRUSTRATED:  arms crossed, legs apart, backward lean, dropped head → closed-off wide silhouette

EXPR_SPECS = {
    "CURIOUS": {
        "hair": "default",
        "blush": 80,
        "eyes": {
            "l_open": 0.90, "r_open": 0.86,
            "brow_l_dy": -int(HR * 0.18), "brow_r_dy": -int(HR * 0.24),
            "gaze_dx": 0.4, "gaze_dy": -0.2,
            "brow_furrow_l": False, "brow_furrow_r": False,
        },
        "mouth": "neutral",
        "cy_offset": int(HR * 0.08),   # head forward (lean forward)
        "pose": {
            "body_tilt": -int(HR * 0.20),  # forward lean = torso displaced left/forward
            # Left arm: reaches forward-up (pointing gesture)
            "arm_l": (-int(HR * 0.60), -int(HR * 0.70), -int(HR * 0.10), -int(HR * 0.40)),
            # Right arm: slightly raised (curious open)
            "arm_r": (int(HR * 0.50), int(HR * 0.60), int(HR * 0.10), -int(HR * 0.10)),
            # Legs: weight shifted forward, left foot forward
            "leg_l": (-int(HR * 0.20), -int(HR * 0.20)),
            "leg_r": (int(HR * 0.10), int(HR * 0.12)),
            "feet_off_ground": False,
        },
    },
    "DETERMINED": {
        "hair": "tight",
        "blush": 0,
        "eyes": {
            "l_open": 0.80, "r_open": 0.80,
            "brow_l_dy": int(HR * 0.10), "brow_r_dy": int(HR * 0.10),
            "gaze_dx": 0, "gaze_dy": 0.12,
            "brow_furrow_l": False, "brow_furrow_r": False,
        },
        "mouth": "pressed_flat",
        "cy_offset": 0,
        "pose": {
            "body_tilt": 0,   # upright — stable, grounded
            # Both arms at hips (fist-on-hip pose) — arms point inward-down
            "arm_l": (-int(HR * 0.20), int(HR * 0.90), int(HR * 0.10), int(HR * 0.10)),
            "arm_r": (int(HR * 0.20), int(HR * 0.90), -int(HR * 0.10), int(HR * 0.10)),
            # Wide stance
            "leg_l": (-int(HR * 0.15), 0),
            "leg_r": (int(HR * 0.15), 0),
            "feet_off_ground": False,
        },
    },
    "SURPRISED": {
        "hair": "excited",
        "blush": 0,
        "eyes": {
            "l_open": 1.0, "r_open": 1.0,
            "brow_l_dy": -int(HR * 0.32), "brow_r_dy": -int(HR * 0.32),
            "gaze_dx": 0, "gaze_dy": 0,
            "pupils_wide": True,
            "brow_furrow_l": False, "brow_furrow_r": False,
        },
        "mouth": "open_oval",
        "cy_offset": -int(HR * 0.06),  # head jerks back
        "pose": {
            "body_tilt": int(HR * 0.15),   # backward lean
            # Arms fly OUT to sides — maximum wingspan = wide open silhouette
            "arm_l": (-int(HR * 1.10), int(HR * 0.10), -int(HR * 0.10), int(HR * 0.30)),
            "arm_r": (int(HR * 1.10), int(HR * 0.10), int(HR * 0.10), int(HR * 0.30)),
            # Weight shifted back — legs stagger
            "leg_l": (-int(HR * 0.05), int(HR * 0.10)),
            "leg_r": (int(HR * 0.20), -int(HR * 0.05)),
            "feet_off_ground": False,
        },
    },
    "WORRIED": {
        "hair": "drooped",
        "blush": 0,
        "eyes": {
            "l_open": 0.72, "r_open": 0.72,
            "brow_l_dy": -int(HR * 0.18), "brow_r_dy": -int(HR * 0.18),
            "gaze_dx": 0, "gaze_dy": 0.18,
            "brow_furrow_l": True, "brow_furrow_r": True,
        },
        "mouth": "corners_down",
        "cy_offset": int(HR * 0.04),   # slight hunch (head forward-down)
        "pose": {
            "body_tilt": int(HR * 0.05),   # slight backward containment
            # Arms CROSSED over chest (both going toward opposite shoulder)
            "arm_l": (int(HR * 0.50), int(HR * 0.50), int(HR * 0.20), -int(HR * 0.15)),
            "arm_r": (-int(HR * 0.50), int(HR * 0.50), -int(HR * 0.20), -int(HR * 0.15)),
            # Legs together — contracted stance
            "leg_l": (int(HR * 0.08), 0),
            "leg_r": (-int(HR * 0.08), 0),
            "feet_off_ground": False,
        },
    },
    "DELIGHTED": {
        "hair": "excited",
        "blush": 140,
        "eyes": {
            "l_open": 0.60, "r_open": 0.60,
            "brow_l_dy": -int(HR * 0.16), "brow_r_dy": -int(HR * 0.16),
            "gaze_dx": 0, "gaze_dy": 0,
            "crinkle": True,
            "brow_furrow_l": False, "brow_furrow_r": False,
        },
        "mouth": "smile_big",
        "cy_offset": -int(HR * 0.10),   # head floats up (airborne)
        "pose": {
            "body_tilt": -int(HR * 0.12),  # slight forward energy
            # BOTH ARMS UP HIGH — celebration / full wingspan up
            "arm_l": (-int(HR * 0.80), -int(HR * 1.10), -int(HR * 0.10), -int(HR * 0.30)),
            "arm_r": (int(HR * 0.80), -int(HR * 1.10), int(HR * 0.10), -int(HR * 0.30)),
            # Feet lifted off ground — bounce
            "leg_l": (-int(HR * 0.10), -int(HR * 0.05), int(HR * 0.35)),
            "leg_r": (int(HR * 0.15), int(HR * 0.05), int(HR * 0.20)),
            "feet_off_ground": True,
        },
    },
    "FRUSTRATED": {
        "hair": "tight",
        "blush": 0,
        "eyes": {
            "l_open": 0.55, "r_open": 0.55,
            "brow_l_dy": int(HR * 0.14), "brow_r_dy": int(HR * 0.14),
            "gaze_dx": 0, "gaze_dy": 0.22,
            "half_lid": True,
            "brow_furrow_l": True, "brow_furrow_r": True,
        },
        "mouth": "frown_slight",
        "cy_offset": int(HR * 0.06),   # head drops (sullen)
        "pose": {
            "body_tilt": int(HR * 0.10),   # backward lean/withdrawal
            # Arms crossed tighter than WORRIED — elbows jutting out (aggressive contained)
            "arm_l": (int(HR * 0.55), int(HR * 0.60), int(HR * 0.30), -int(HR * 0.20)),
            "arm_r": (-int(HR * 0.55), int(HR * 0.60), -int(HR * 0.30), -int(HR * 0.20)),
            # Wide stance — planted/stubborn
            "leg_l": (-int(HR * 0.22), -int(HR * 0.05)),
            "leg_r": (int(HR * 0.22), int(HR * 0.05)),
            "feet_off_ground": False,
        },
    },
}


# ── Renderer ──────────────────────────────────────────────────────────────────

def render_character(expr, panel_w, panel_h):
    """Render full-body character panel at 2x scale, return 1x via LANCZOS."""
    rw   = panel_w * RENDER_SCALE
    rh   = panel_h * RENDER_SCALE
    img  = Image.new("RGBA", (rw, rh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    spec      = EXPR_SPECS[expr]
    cy_off    = spec.get("cy_offset", 0)
    hoodie_c  = HOODIE_MAP[expr]

    # Head position — placed in upper portion of panel with room for full body below
    head_cx = rw // 2
    head_cy = int(rh * 0.22) + cy_off   # upper quarter of panel

    # Draw body first (behind head)
    draw_body_pose(draw, head_cx, head_cy, hoodie_c, spec.get("pose", {}))

    # Refresh draw after any potential state change
    draw = ImageDraw.Draw(img)

    # Draw head on top
    draw_head(draw, head_cx, head_cy)
    draw_ears(draw, head_cx, head_cy)
    draw_hair(draw, head_cx, head_cy, variant=spec["hair"])
    draw_blush(draw, head_cx, head_cy, alpha=spec["blush"])
    draw_eyes_full(draw, head_cx, head_cy, spec["eyes"])
    draw_nose(draw, head_cx, head_cy)
    draw_mouth(draw, head_cx, head_cy, style=spec["mouth"])

    return img.resize((panel_w, panel_h), Image.LANCZOS)


# ── Sheet assembly ────────────────────────────────────────────────────────────
EXPRESSIONS = ["CURIOUS", "DETERMINED", "SURPRISED",
               "WORRIED",  "DELIGHTED",  "FRUSTRATED"]


def build_sheet(show_guides=False):
    """Build full 1200x900 expression sheet. show_guides=False for pitch export."""
    sheet = Image.new("RGB", (TOTAL_W, TOTAL_H), CANVAS_BG)
    draw  = ImageDraw.Draw(sheet)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
        font_sub   = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = font_title
        font_sub   = font_title

    title = "LUMA — Expression Sheet v005  |  Luma & the Glitchkin"
    sub   = ("Designer: Maya Santos  |  Cycle 26 STYLE FIX: aligned to classroom pose  |  "
             "FULL BODY — 6/6 squint pass  |  classroom-style head/hair/eyes")
    draw.text((PAD, 10), title, fill=(59, 40, 32), font=font_title)
    draw.text((PAD, 36), sub,   fill=(110, 88, 68), font=font_sub)

    for idx, expr in enumerate(EXPRESSIONS):
        col = idx % COLS
        row = idx // COLS
        px  = PAD + col * (PANEL_W + PAD)
        py  = HEADER + PAD + row * (PANEL_H + LABEL_H + PAD)

        bg  = BG[expr]
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], fill=bg)
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], outline=LINE, width=2)

        char_img = render_character(expr, PANEL_W - PAD * 2, PANEL_H - PAD)
        ox = px + PAD
        oy = py + PAD // 2
        sheet.paste(char_img, (ox, oy), char_img)

        # CRITICAL: refresh draw after paste
        draw = ImageDraw.Draw(sheet)

        label_y  = py + PANEL_H + 2
        label_bg = tuple(max(0, int(c * 0.88)) for c in bg)
        draw.rectangle([px, label_y, px + PANEL_W, label_y + LABEL_H], fill=label_bg)
        try:
            bbox = draw.textbbox((0, 0), expr, font=font_label)
            tw   = bbox[2] - bbox[0]
            th   = bbox[3] - bbox[1]
        except Exception:
            tw, th = 100, 16
        tx = px + (PANEL_W - tw) // 2
        ty = label_y + (LABEL_H - th) // 2
        draw.text((tx, ty), expr, fill=LINE, font=font_label)

    return sheet


if __name__ == "__main__":
    out_dir  = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "characters", "main")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_luma_expression_sheet_v005.png")
    # show_guides=False for pitch export
    sheet    = build_sheet(show_guides=False)
    sheet.save(out_path)
    print(f"Saved: {os.path.abspath(out_path)}")
    print(f"Canvas: {sheet.size[0]}x{sheet.size[1]}")
    print("v005 Cycle 26 STYLE FIX changes:")
    print("  - HEAD: classroom-style circle + cheek nubs (no jaw bump)")
    print("  - HAIR: 8-ellipse organic cloud mass (classroom pose method)")
    print("  - EYES: near-circular proportions + eyelid arc (classroom style)")
    print("  - LINE WEIGHTS: silhouette=6px@2x, interior=4px@2x, brows=4px@2x")
    print("  - BACKGROUND: warm parchment canvas + light per-panel tones")
    print("  - FULL BODY: 6 expressions, all unique at silhouette level")
