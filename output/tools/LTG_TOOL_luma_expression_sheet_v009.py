#!/usr/bin/env python3
"""
LTG_TOOL_luma_expression_sheet_v009.py
Luma Expression Sheet — v009  ARM SILHOUETTE DIFFERENTIATION
"Luma & the Glitchkin" — Cycle 34 / Maya Santos

v009 GOAL: Maximize arm/shoulder silhouette differentiation across all 7 expressions.
    - Driven by LTG_TOOL_expression_silhouette_v002.py --mode arms baseline (C34)
    - Prior v008 arms-mode baseline: FAIL (worst pair SURPRISED↔FRUSTRATED 97.9%)

ARMS-MODE PROBLEM PAIRS (v008 baseline):
    Panel 3 SURPRISED ↔ Panel 6 FRUSTRATED — 97.9% (FAIL) — both have arms near body
    Panel 0 THE NOTICING ↔ Panel 6 FRUSTRATED — 93.1% (FAIL)
    Panel 2 DETERMINED ↔ Panel 5 DELIGHTED — 90.2% (FAIL)
    Panel 1 CURIOUS ↔ Panel 4 WORRIED — 88.3% (FAIL)

FIXES (v009):
  SURPRISED:    Arms FULLY outstretched wide + raised — true Y-shape silhouette.
                arm_l: far LEFT and HIGH (-HR*1.40, -HR*0.55). arm_r: far RIGHT and HIGH.
                Distinct from all others at thumbnail.

  FRUSTRATED:   TIGHT CROSSED-ARM pose — arms cross the body horizontally.
                arm_l reaches across to RIGHT SIDE of torso (positive dx from left shoulder).
                arm_r reaches across to LEFT SIDE of torso (negative dx from right shoulder).
                Creates a horizontal bar across the mid-body unique to this expression.
                CANONICAL character design note: Luma crossing her arms = "I'm not having it."

  DETERMINED:   FISTS AT HIPS with ELBOWS FLARING — arms bow out at elbow.
                Lower arms fold back toward hips, elbows push outward.
                Creates a wide-hip "hands on hips" silhouette read.

  WORRIED:      ARMS HUGGING SELF — arms wrap over chest.
                Both arms cross body AT CHEST LEVEL (higher than v008).
                Creates a "self-hug" shape: arms crossed high on chest.

  DELIGHTED:    ARMS RAISED HIGH IN V — both arms above shoulder, V-spread.
                Clearly distinct from all others: only expression with hands above head.
                Retains jump (feet off ground).

  CURIOUS:      ONE ARM FORWARD REACHING — reaches out toward subject of curiosity.
                Left arm extends directly FORWARD (as in reaching/pointing gesture).
                Right arm stays at side or slight bend.
                Lean is more pronounced.

  THE NOTICING: UNCHANGED — already has the distinctive one-hand-to-chin silhouette.

EYE-WIDTH: ew = int(HEAD_HEIGHT_2X × 0.22) = 45px at 2x (unchanged from v008).

LAYOUT: 3×3 grid, 9 slots. 7 filled, 2 blank. Slot 0 = THE NOTICING.

Output: output/characters/main/LTG_CHAR_luma_expressions_v009.png

Author: Maya Santos
Date: 2026-03-29
Cycle: 34
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
CANVAS_BG  = (235, 224, 206)   # warm parchment

# Hoodie color tint per expression
HOODIE_MAP = {
    "THE NOTICING": (130, 148, 172),   # muted blue-grey — still, interior
    "CURIOUS":      (150, 175, 200),   # cool blue-gray
    "DETERMINED":   (155,  85, 45),    # warm amber-red
    "SURPRISED":    (232, 112, 42),    # full orange
    "WORRIED":      ( 80, 100, 140),   # muted indigo
    "DELIGHTED":    (232, 112, 42),    # full orange
    "FRUSTRATED":   (135,  75, 65),    # muted terracotta
}

BG = {
    "THE NOTICING": (218, 226, 235),   # pale blue-grey
    "CURIOUS":      (230, 240, 235),   # soft warm mint
    "DETERMINED":   (238, 228, 210),   # warm parchment
    "SURPRISED":    (245, 234, 210),   # warm cream
    "WORRIED":      (225, 230, 242),   # pale blue-gray
    "DELIGHTED":    (250, 238, 215),   # warm golden cream
    "FRUSTRATED":   (235, 220, 220),   # pale rose
}

# ── Layout ────────────────────────────────────────────────────────────────────
COLS      = 3
ROWS      = 3
PAD       = 20
HEADER    = 58
LABEL_H   = 32
TOTAL_W   = 1200
TOTAL_H   = 900
PANEL_W   = (TOTAL_W - PAD * (COLS + 1)) // COLS   # ~373px
PANEL_H   = (TOTAL_H - HEADER - PAD * (ROWS + 1) - LABEL_H * ROWS) // ROWS  # ~235px

RENDER_SCALE = 2

# Character proportions in render space (2x)
HEAD_R   = 52   # head radius at 1x
HR       = HEAD_R * RENDER_SCALE   # 104 at 2x

# v008/v009 EYE-WIDTH: head_height × 0.22 (turnaround-aligned)
HEAD_HEIGHT_2X = 2 * HR   # 208px
EW_CANON = int(HEAD_HEIGHT_2X * 0.22)  # 45px at 2x


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
    draw.ellipse([cx - HR, cy - HR, cx + HR, cy + HR + int(HR * 0.15)],
                 fill=SKIN, outline=LINE, width=4)
    chin_rx = int(HR * 0.95)
    draw.ellipse([cx - chin_rx, cy - int(HR * 0.20),
                  cx + chin_rx, cy + HR + int(HR * 0.25)], fill=SKIN)
    draw.arc([cx - chin_rx, cy - int(HR * 0.20),
              cx + chin_rx, cy + HR + int(HR * 0.25)],
             start=0, end=180, fill=LINE, width=3)
    nub_w = int(HR * 0.18)
    nub_h = int(HR * 0.24)
    nub_y = cy - int(HR * 0.12)
    draw.ellipse([cx - HR - nub_w + int(HR * 0.06), nub_y - nub_h // 2,
                  cx - HR + nub_w + int(HR * 0.06), nub_y + nub_h // 2],
                 fill=SKIN, outline=LINE, width=3)
    draw.ellipse([cx + HR - nub_w - int(HR * 0.06), nub_y - nub_h // 2,
                  cx + HR + nub_w - int(HR * 0.06), nub_y + nub_h // 2],
                 fill=SKIN, outline=LINE, width=3)


def draw_ears(draw, cx, cy):
    pass   # cheek nubs in draw_head() serve as ear/cheek indicators


def draw_hair(draw, cx, cy, variant="default"):
    """Classroom-style cloud hair: 8 overlapping ellipses."""
    s = HR / 100.0

    if variant == "excited":
        v_off  = -int(s * 15)
        spread = int(s * 10)
    elif variant == "drooped":
        v_off  = int(s * 8)
        spread = -int(s * 5)
    elif variant == "tight":
        v_off  = int(s * 4)
        spread = -int(s * 8)
    else:
        v_off  = 0
        spread = 0

    hair_ellipses = [
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

    draw.arc([cx - int(s*60), cy - int(s*195) + v_off,
              cx - int(s*10), cy - int(s*140)],
             start=30, end=200, fill=HAIR, width=3)
    draw.arc([cx - int(s*20), cy - int(s*190) + v_off,
              cx + int(s*40), cy - int(s*130)],
             start=10, end=190, fill=HAIR, width=3)


def draw_eyes_full(draw, cx, cy, params):
    """Classroom-style eyes with turnaround-aligned eye width."""
    s      = HR / 100.0
    eye_y  = cy - int(s * 18)
    lex    = cx - int(s * 38)
    rex    = cx + int(s * 38)

    ew     = EW_CANON   # 45px at 2x

    p = params

    leh_base = int(HR * 0.27)
    reh_base = int(HR * 0.22)
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
        draw.ellipse([ex - ew, eye_y - eh, ex + ew, eye_y + eh], fill=EYE_W,
                     outline=LINE, width=3)
        iris_r = int(ew * 0.60)
        iry    = min(iris_r, eh - 2)
        if iry < 2:
            iry = 2
        draw.chord([ex + pdx - iris_r, eye_y + pdy - iry,
                    ex + pdx + iris_r, eye_y + pdy + iry],
                   start=15, end=345, fill=EYE_IRIS)
        pr = int(iris_r * 0.64) if p.get("pupils_wide") else int(iris_r * 0.50)
        pup_x = ex + pdx
        draw.ellipse([pup_x - pr, eye_y + pdy - pr,
                      pup_x + pr, eye_y + pdy + pr], fill=EYE_PUP)
        hl_x = pup_x + int(iris_r * 0.42)
        hl_y = eye_y + pdy - int(iry * 0.48)
        hl_s = max(int(pr * 0.38), 3)
        draw.ellipse([hl_x - hl_s, hl_y - hl_s, hl_x + hl_s, hl_y + hl_s],
                     fill=EYE_HL)
        draw.arc([ex - ew, eye_y - eh, ex + ew, eye_y + eh],
                 start=200, end=340, fill=LINE, width=3)
        if p.get("crinkle"):
            dsign   = 1 if is_right else -1
            outer_x = ex + ew * dsign
            for k in range(3):
                dy_k = int(s * 4) * k
                draw.line([(outer_x, eye_y + dy_k),
                           (outer_x + dsign * int(s * 11),
                            eye_y + dy_k - int(s * 7))],
                          fill=LINE, width=2)

    # Brows
    brow_base_y = eye_y - int(leh_base * 1.42)
    for (bx, b_dy, b_furrow) in [
        (lex, p.get("brow_l_dy", 0), p.get("brow_furrow_l", False)),
        (rex, p.get("brow_r_dy", 0), p.get("brow_furrow_r", False)),
    ]:
        by         = brow_base_y + b_dy
        is_right_b = (bx == rex)
        inner_x = bx + int(s * 22) if is_right_b else bx - int(s * 22)
        outer_x = bx - int(s * 26) if is_right_b else bx + int(s * 26)
        inner_y = by + (int(s * 8) if b_furrow else int(s * 2))
        outer_y = by + (0 if b_furrow else int(s * 2))
        brow_pts = [(outer_x, outer_y), (bx, by - int(s * 6)), (inner_x, inner_y)]
        draw.line(brow_pts, fill=HAIR, width=3)


def draw_nose(draw, cx, cy):
    """Classroom-style nose: two small nostril dots + bridge arc."""
    s = HR / 100.0
    draw.ellipse([cx - int(s*8), cy + int(s*8),  cx - int(s*2), cy + int(s*14)],
                 fill=SKIN_SH)
    draw.ellipse([cx + int(s*2), cy + int(s*8),  cx + int(s*8), cy + int(s*14)],
                 fill=SKIN_SH)
    draw.arc([cx - int(s*6), cy - int(s*10), cx + int(s*6), cy + int(s*12)],
             start=200, end=340, fill=SKIN_SH, width=2)


def draw_mouth(draw, cx, cy, style="neutral"):
    """Classroom-style mouth. All mouth polylines width=3."""
    s  = HR / 100.0
    my = cy + int(s * 30)
    mw = int(s * 36)
    lx, rx = cx - mw, cx + mw

    if style == "neutral":
        pts = bezier3((lx, my + int(s*4)), (cx, my - int(s*8)), (rx, my + int(s*4)))
        polyline(draw, pts, LINE, width=3)
    elif style == "smile_closed":
        pts = bezier3((lx, my + int(s*4)), (cx, my - int(s*20)), (rx, my + int(s*4)))
        polyline(draw, pts, LINE, width=3)
        draw.line([(lx, my + int(s*4)), (lx - int(s*5), my + int(s*14))],
                  fill=LINE, width=3)
        draw.line([(rx, my + int(s*4)), (rx + int(s*5), my + int(s*14))],
                  fill=LINE, width=3)
    elif style == "smile_big":
        sh    = int(s * 22)
        top_p = bezier3((lx, my), (cx, my - int(s*28)), (rx, my))
        bot_p = bezier3((lx, my + sh), (cx, my + sh + int(s*10)), (rx, my + sh))
        fill_pts = top_p + bot_p[::-1]
        draw.polygon(fill_pts, fill=(210, 70, 50))
        tw_m = int(mw * 0.82)
        draw.rectangle([cx - tw_m, my - 2, cx + tw_m, my + sh - 4],
                       fill=(248, 242, 230))
        polyline(draw, top_p, LINE, width=3)
        polyline(draw, bot_p, LINE, width=3)
        draw.line([(lx, my), (lx, my + sh)], fill=LINE, width=3)
        draw.line([(rx, my), (rx, my + sh)], fill=LINE, width=3)
    elif style == "open_oval":
        ow = int(mw * 0.54)
        oh = int(s * 28)
        draw.ellipse([cx - ow, my - int(oh * 0.38), cx + ow, my + int(oh * 0.62)],
                     fill=(210, 65, 48))
        draw.ellipse([cx - ow, my - int(oh * 0.38), cx + ow, my + int(oh * 0.62)],
                     outline=LINE, width=3)
    elif style == "pressed_flat":
        pts = bezier3((lx, my + int(s*4)), (cx, my + int(s*8)), (rx, my + int(s*4)))
        polyline(draw, pts, LINE, width=3)
    elif style == "corners_down":
        pts = bezier3((lx, my - int(s*12)), (cx, my + int(s*16)), (rx, my - int(s*12)))
        polyline(draw, pts, LINE, width=3)
    elif style == "frown_slight":
        pts = bezier3((lx, my - int(s*6)), (cx, my + int(s*14)), (rx, my - int(s*6)))
        polyline(draw, pts, LINE, width=3)
    elif style == "noticing":
        # Barely-parted, mid-breath of recognition
        pts = bezier3((lx + int(s*8), my + int(s*2)), (cx, my - int(s*4)),
                      (rx - int(s*8), my + int(s*2)))
        polyline(draw, pts, LINE, width=3)
        draw.ellipse([cx - int(s*6), my + int(s*3), cx + int(s*6), my + int(s*10)],
                     fill=(210, 65, 48))
    elif style == "tight_frown":
        # FRUSTRATED new mouth: compressed corners, tighter line
        pts = bezier3((lx + int(s*10), my - int(s*4)), (cx, my + int(s*18)),
                      (rx - int(s*10), my - int(s*4)))
        polyline(draw, pts, LINE, width=3)


def draw_blush(draw, cx, cy, alpha=0):
    """Classroom-style blush: ovals beside face at cheek level."""
    if alpha <= 0:
        return
    s  = HR / 100.0
    bw = int(s * 28)
    bh = int(s * 14)
    by = cy + int(s * 20)
    for bx in [cx - int(s * 80), cx + int(s * 80)]:
        draw.ellipse([bx - bw, by - bh, bx + bw, by + bh], fill=BLUSH_C)


def draw_noticing_hand(draw, cx, head_cy, hoodie_col):
    """Draw the 'thinking hand' gesture for THE NOTICING.
    Right hand raised to chin level — lightly touching cheek.
    """
    s = HR / 100.0
    hand_cx = cx + int(HR * 0.95)
    hand_cy = head_cy + int(HR * 0.60)
    hand_r  = int(HR * 0.22)
    draw.ellipse([hand_cx - hand_r, hand_cy - int(hand_r * 0.70),
                  hand_cx + hand_r, hand_cy + int(hand_r * 0.70)],
                 fill=SKIN, outline=LINE, width=3)
    arm_end_x  = cx + int(HR * 0.80)
    arm_end_y  = hand_cy + int(HR * 0.20)
    torso_x    = cx + int(HR * 0.85)
    torso_y    = head_cy + int(HR * 1.50)
    arm_w      = int(HR * 0.28)
    pts = bezier3((torso_x, torso_y), (arm_end_x, arm_end_y),
                  (hand_cx - 4, hand_cy + 4))
    polyline(draw, pts, hoodie_col, width=arm_w * 2)
    polyline(draw, pts, LINE, width=3)


def draw_crossed_arms(draw, cx, neck_cx, torso_top_y, hoodie_col):
    """
    FRUSTRATED: Arms crossed tight across body.
    Left arm: from left shoulder crosses to RIGHT side of torso.
    Right arm: from right shoulder crosses to LEFT side, slightly lower.
    Creates a horizontal crossing-bar silhouette unique to FRUSTRATED.
    """
    arm_w = int(HR * 0.28)
    torso_top_w = int(HR * 0.70)

    # Left arm: shoulder is left side of torso, hand crosses to right
    l_shoulder_x = neck_cx - torso_top_w + int(HR * 0.10)
    l_shoulder_y = torso_top_y + int(HR * 0.20)
    # Hand lands on right side of mid-torso, slightly lower
    l_hand_x = neck_cx + int(HR * 0.55)
    l_hand_y = l_shoulder_y + int(HR * 0.60)
    l_mid_x  = neck_cx - int(HR * 0.05)
    l_mid_y  = l_shoulder_y + int(HR * 0.20)
    pts_l = bezier3((l_shoulder_x, l_shoulder_y), (l_mid_x, l_mid_y),
                    (l_hand_x, l_hand_y))
    polyline(draw, pts_l, hoodie_col, width=arm_w * 2)
    polyline(draw, pts_l, LINE, width=3)
    hand_r = int(HR * 0.22)
    draw.ellipse([l_hand_x - hand_r, l_hand_y - int(hand_r * 0.7),
                  l_hand_x + hand_r, l_hand_y + int(hand_r * 0.7)],
                 fill=SKIN, outline=LINE, width=3)

    # Right arm: shoulder is right side of torso, hand crosses to left — slightly lower
    r_shoulder_x = neck_cx + torso_top_w - int(HR * 0.10)
    r_shoulder_y = torso_top_y + int(HR * 0.30)
    r_hand_x = neck_cx - int(HR * 0.55)
    r_hand_y = r_shoulder_y + int(HR * 0.50)
    r_mid_x  = neck_cx + int(HR * 0.05)
    r_mid_y  = r_shoulder_y + int(HR * 0.15)
    pts_r = bezier3((r_shoulder_x, r_shoulder_y), (r_mid_x, r_mid_y),
                    (r_hand_x, r_hand_y))
    polyline(draw, pts_r, hoodie_col, width=arm_w * 2)
    polyline(draw, pts_r, LINE, width=3)
    draw.ellipse([r_hand_x - hand_r, r_hand_y - int(hand_r * 0.7),
                  r_hand_x + hand_r, r_hand_y + int(hand_r * 0.7)],
                 fill=SKIN, outline=LINE, width=3)


def draw_self_hug_arms(draw, cx, neck_cx, torso_top_y, hoodie_col):
    """
    WORRIED: Self-hug arms — both arms cross high on chest (higher than v008).
    Creates a compact self-hug silhouette at chest level.
    Difference from FRUSTRATED: both arms at chest height (not mid-torso),
    elbows stay wider before crossing, hands almost meet at center.
    """
    arm_w = int(HR * 0.28)
    torso_top_w = int(HR * 0.70)
    chest_y = torso_top_y + int(HR * 0.28)   # high on chest

    # Left arm: wraps UP and across at chest height
    l_shoulder_x = neck_cx - torso_top_w + int(HR * 0.10)
    l_shoulder_y = torso_top_y + int(HR * 0.10)
    # Elbow flares left and slightly up before wrapping in
    l_elbow_x = l_shoulder_x - int(HR * 0.08)
    l_elbow_y = l_shoulder_y + int(HR * 0.15)
    # Hand wraps to right side of chest
    l_hand_x = neck_cx + int(HR * 0.38)
    l_hand_y = chest_y + int(HR * 0.20)
    pts_l = bezier3((l_shoulder_x, l_shoulder_y), (l_elbow_x, l_elbow_y),
                    (l_hand_x, l_hand_y))
    polyline(draw, pts_l, hoodie_col, width=arm_w * 2)
    polyline(draw, pts_l, LINE, width=3)
    hand_r = int(HR * 0.22)
    draw.ellipse([l_hand_x - hand_r, l_hand_y - int(hand_r * 0.7),
                  l_hand_x + hand_r, l_hand_y + int(hand_r * 0.7)],
                 fill=SKIN, outline=LINE, width=3)

    # Right arm: wraps UP and across, slightly behind left arm
    r_shoulder_x = neck_cx + torso_top_w - int(HR * 0.10)
    r_shoulder_y = torso_top_y + int(HR * 0.10)
    r_elbow_x = r_shoulder_x + int(HR * 0.08)
    r_elbow_y = r_shoulder_y + int(HR * 0.15)
    r_hand_x = neck_cx - int(HR * 0.38)
    r_hand_y = chest_y + int(HR * 0.08)   # slightly higher (behind left arm)
    pts_r = bezier3((r_shoulder_x, r_shoulder_y), (r_elbow_x, r_elbow_y),
                    (r_hand_x, r_hand_y))
    polyline(draw, pts_r, hoodie_col, width=arm_w * 2)
    polyline(draw, pts_r, LINE, width=3)
    draw.ellipse([r_hand_x - hand_r, r_hand_y - int(hand_r * 0.7),
                  r_hand_x + hand_r, r_hand_y + int(hand_r * 0.7)],
                 fill=SKIN, outline=LINE, width=3)


def draw_body_pose(draw, cx, head_cy, hoodie_col, pose, expr_name=""):
    """
    Draw full body: torso, arms, legs, shoes.
    v009: FRUSTRATED and WORRIED get custom arm drawing for better silhouette.
    """
    tilt = pose.get("body_tilt", 0)

    neck_y  = head_cy + HR + int(HR * 0.10)
    neck_cx = cx + tilt

    torso_top_w = int(HR * 0.70)
    torso_bot_w = int(HR * 0.90)
    torso_h     = int(HR * 2.10)
    torso_top_y = neck_y + int(HR * 0.08)
    torso_bot_y = torso_top_y + torso_h

    hip_cx = neck_cx + tilt // 2

    torso_pts = [
        (neck_cx - torso_top_w, torso_top_y),
        (neck_cx + torso_top_w, torso_top_y),
        (hip_cx  + torso_bot_w, torso_bot_y),
        (hip_cx  - torso_bot_w, torso_bot_y),
    ]
    draw.polygon(torso_pts, fill=hoodie_col)
    shadow_pts = [
        (neck_cx + torso_top_w - int(HR * 0.15), torso_top_y),
        (neck_cx + torso_top_w, torso_top_y),
        (hip_cx  + torso_bot_w, torso_bot_y),
        (hip_cx  + torso_bot_w - int(HR * 0.20), torso_bot_y),
    ]
    draw.polygon(shadow_pts, fill=HOODIE_SH)
    draw.polygon(torso_pts, outline=LINE, width=3)

    draw.rectangle([neck_cx - torso_top_w + 4, torso_top_y,
                    neck_cx + torso_top_w - 4, torso_top_y + int(HR * 0.18)],
                   fill=(250, 232, 200))

    px_x0 = neck_cx - int(HR * 0.28)
    px_y0 = torso_top_y + int(HR * 0.22)
    draw_hoodie_pixel_accent(draw, px_x0, px_y0,
                             int(HR * 0.56), int(HR * 0.44), hoodie_col)

    draw.rectangle([hip_cx - int(HR * 0.32), torso_bot_y - int(HR * 0.28),
                    hip_cx + int(HR * 0.32), torso_bot_y],
                   fill=HOODIE_SH, outline=LINE, width=2)

    draw.rectangle([neck_cx - int(HR * 0.22), neck_y,
                    neck_cx + int(HR * 0.22), torso_top_y + int(HR * 0.05)],
                   fill=SKIN)
    draw.rectangle([neck_cx - int(HR * 0.22), neck_y,
                    neck_cx + int(HR * 0.22), torso_top_y + int(HR * 0.05)],
                   outline=LINE, width=3)

    # === ARMS ===
    # Special custom arm drawing for FRUSTRATED and WORRIED (v009 silhouette fix)
    if expr_name == "FRUSTRATED":
        draw_crossed_arms(draw, cx, neck_cx, torso_top_y, hoodie_col)
    elif expr_name == "WORRIED":
        draw_self_hug_arms(draw, cx, neck_cx, torso_top_y, hoodie_col)
    else:
        # Standard arm drawing from pose spec
        arm_specs = [
            ("arm_l", pose.get("arm_l"), neck_cx - torso_top_w + int(HR * 0.10), torso_top_y + int(HR * 0.10)),
            ("arm_r", pose.get("arm_r"), neck_cx + torso_top_w - int(HR * 0.10), torso_top_y + int(HR * 0.10)),
        ]
        arm_w = int(HR * 0.28)
        for (key, arm_data, shoulder_x, shoulder_y) in arm_specs:
            if arm_data is None:
                continue
            end_x = shoulder_x + arm_data[0]
            end_y = shoulder_y + arm_data[1]
            mid_x = (shoulder_x + end_x) // 2 + arm_data[2] if len(arm_data) > 2 else (shoulder_x + end_x) // 2
            mid_y = (shoulder_y + end_y) // 2 + arm_data[3] if len(arm_data) > 3 else (shoulder_y + end_y) // 2
            pts   = bezier3((shoulder_x, shoulder_y), (mid_x, mid_y), (end_x, end_y))
            polyline(draw, pts, hoodie_col, width=arm_w * 2)
            polyline(draw, pts, LINE, width=3)
            hand_r = int(HR * 0.22)
            draw.ellipse([end_x - hand_r, end_y - hand_r * 2 // 3,
                          end_x + hand_r, end_y + hand_r * 2 // 3],
                         fill=SKIN, outline=LINE, width=3)

    # === LEGS ===
    pants_h = int(HR * 1.68)
    leg_w   = int(HR * 0.38)
    leg_l_spec = pose.get("leg_l", (0, 0))
    leg_r_spec = pose.get("leg_r", (0, 0))

    feet_off = pose.get("feet_off_ground", False)
    ground_y = torso_bot_y + pants_h + int(HR * 0.30)

    for side in [-1, 1]:
        hip_x   = hip_cx + side * int(HR * 0.42)
        spec    = leg_l_spec if side < 0 else leg_r_spec
        knee_dx = spec[0]
        foot_dx = spec[1]
        foot_lift = spec[2] if len(spec) > 2 else 0

        knee_x = hip_x + knee_dx
        knee_y = torso_bot_y + pants_h // 2
        foot_x = hip_x + foot_dx
        foot_y = ground_y - foot_lift

        draw.rectangle([hip_x  - leg_w // 2, torso_bot_y - int(HR * 0.08),
                         hip_x  + leg_w // 2, knee_y],
                        fill=PANTS)
        draw.rectangle([hip_x  - leg_w // 2, torso_bot_y - int(HR * 0.08),
                         hip_x  + leg_w // 2, knee_y],
                        outline=LINE, width=3)
        pts = bezier3(
            (hip_x, knee_y),
            ((knee_x + foot_x) // 2, (knee_y + foot_y) // 2),
            (foot_x, foot_y)
        )
        polyline(draw, pts, PANTS, width=leg_w * 2)
        polyline(draw, pts, LINE, width=3)

        shoe_w = int(HR * 0.50)
        shoe_h = int(HR * 0.28)
        draw.ellipse([foot_x - shoe_w + 2, foot_y + shoe_h - int(HR * 0.06),
                      foot_x + shoe_w - 2, foot_y + shoe_h + int(HR * 0.14)],
                     fill=SHOE_SOLE)
        draw.ellipse([foot_x - shoe_w + 4, foot_y - int(HR * 0.04),
                      foot_x + shoe_w - 4, foot_y + shoe_h],
                     fill=SHOE)
        draw.ellipse([foot_x - shoe_w + 4, foot_y - int(HR * 0.04),
                      foot_x + shoe_w - 4, foot_y + shoe_h],
                     outline=LINE, width=3)
        for li in range(3):
            ly = foot_y + li * 3
            draw.line([foot_x - int(shoe_w * 0.35), ly,
                       foot_x + int(shoe_w * 0.35), ly],
                      fill=LACES, width=1)


# ── Expression specs ──────────────────────────────────────────────────────────

EXPR_SPECS = {
    # ─────────────────────────────────────────────────────────────────────────
    # THE NOTICING — UNCHANGED (distinctive one-hand-to-chin already passes)
    # ─────────────────────────────────────────────────────────────────────────
    "THE NOTICING": {
        "hair": "default",
        "blush": 0,
        "eyes": {
            "l_open": 1.0, "r_open": 0.85,
            "brow_l_dy": -int(HR * 0.14), "brow_r_dy": -int(HR * 0.06),
            "gaze_dx": -0.4, "gaze_dy": 0.15,
            "brow_furrow_l": False, "brow_furrow_r": False,
        },
        "mouth": "noticing",
        "cy_offset": 0,
        "pose": {
            "body_tilt": 0,
            "arm_l": (-int(HR * 0.08), int(HR * 0.96), -int(HR * 0.04), int(HR * 0.10)),
            "arm_r": None,
            "leg_l": (-int(HR * 0.30), -int(HR * 0.22)),
            "leg_r": ( int(HR * 0.30),  int(HR * 0.22)),
            "feet_off_ground": False,
        },
        "noticing_hand": True,
    },
    # ─────────────────────────────────────────────────────────────────────────
    # CURIOUS — ONE ARM FORWARD REACHING (v009 silhouette fix)
    # Left arm reaches outward/forward; right arm relaxed back.
    # Lean more pronounced. Distinct from WORRIED's self-hug.
    # ─────────────────────────────────────────────────────────────────────────
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
        "cy_offset": int(HR * 0.08),
        "pose": {
            "body_tilt": -int(HR * 0.22),
            # Left arm: reaches FORWARD (far left and slightly up — reaching gesture)
            "arm_l": (-int(HR * 1.20), -int(HR * 0.20), -int(HR * 0.08), -int(HR * 0.50)),
            # Right arm: relaxed back/down at side
            "arm_r": (int(HR * 0.15), int(HR * 0.90), int(HR * 0.05), int(HR * 0.05)),
            "leg_l": (-int(HR * 0.20), -int(HR * 0.20)),
            "leg_r": (int(HR * 0.10), int(HR * 0.12)),
            "feet_off_ground": False,
        },
    },
    # ─────────────────────────────────────────────────────────────────────────
    # DETERMINED — FISTS AT HIPS WITH FLARING ELBOWS (v009 silhouette fix)
    # Arms bow outward at elbow before coming down to hips.
    # Creates distinctive wide-elbow hip silhouette.
    # ─────────────────────────────────────────────────────────────────────────
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
            "body_tilt": 0,
            # Fists at hips: arm goes OUTWARD first (elbow flare) then back to hips
            # arm_data: (end_dx, end_dy, mid_dx, mid_dy) from shoulder
            # Left arm: goes far left (elbow) then comes back to left hip
            "arm_l": (-int(HR * 0.18), int(HR * 0.92),
                      -int(HR * 0.62), int(HR * 0.30)),  # elbow flares left
            # Right arm: goes far right (elbow) then comes back to right hip
            "arm_r": (int(HR * 0.18), int(HR * 0.92),
                      int(HR * 0.62), int(HR * 0.30)),   # elbow flares right
            "leg_l": (-int(HR * 0.15), 0),
            "leg_r": (int(HR * 0.15), 0),
            "feet_off_ground": False,
        },
    },
    # ─────────────────────────────────────────────────────────────────────────
    # SURPRISED — ARMS FULLY WIDE AND HIGH (v009 silhouette fix)
    # True Y-shape: both arms extend far out AND UP.
    # Hands above shoulder level. Extremely distinct wide silhouette.
    # ─────────────────────────────────────────────────────────────────────────
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
        "cy_offset": -int(HR * 0.06),
        "pose": {
            "body_tilt": int(HR * 0.15),
            # Arms WIDE and HIGH: end far out and well ABOVE shoulder level
            # end_dy negative = arm ends ABOVE shoulder (Y-shape)
            "arm_l": (-int(HR * 1.50), -int(HR * 0.55), -int(HR * 0.08), -int(HR * 0.60)),
            "arm_r": ( int(HR * 1.50), -int(HR * 0.55),  int(HR * 0.08), -int(HR * 0.60)),
            "leg_l": (-int(HR * 0.05), int(HR * 0.10)),
            "leg_r": (int(HR * 0.20), -int(HR * 0.05)),
            "feet_off_ground": False,
        },
    },
    # ─────────────────────────────────────────────────────────────────────────
    # WORRIED — SELF-HUG ARMS (v009 silhouette fix, custom draw)
    # Arms cross HIGH on chest (self-hug). Defined by draw_self_hug_arms().
    # "arm_l"/"arm_r" not used — custom draw handles the pose.
    # ─────────────────────────────────────────────────────────────────────────
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
        "cy_offset": int(HR * 0.04),
        "pose": {
            "body_tilt": int(HR * 0.05),
            # Not used — draw_self_hug_arms() handles this expression
            "arm_l": None,
            "arm_r": None,
            "leg_l": (int(HR * 0.08), 0),
            "leg_r": (-int(HR * 0.08), 0),
            "feet_off_ground": False,
        },
    },
    # ─────────────────────────────────────────────────────────────────────────
    # DELIGHTED — ARMS RAISED HIGH IN V (v009 silhouette fix)
    # Both arms sweep up to V-shape — highest position of any expression.
    # Only expression with hands clearly above head level at thumbnail.
    # ─────────────────────────────────────────────────────────────────────────
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
        "cy_offset": -int(HR * 0.10),
        "pose": {
            "body_tilt": -int(HR * 0.12),
            # Arms HIGH in V: end FAR OUT and FAR UP — above the head
            # end_dy strongly negative = hands above head level
            "arm_l": (-int(HR * 1.00), -int(HR * 1.50), -int(HR * 0.10), -int(HR * 0.40)),
            "arm_r": ( int(HR * 1.00), -int(HR * 1.50),  int(HR * 0.10), -int(HR * 0.40)),
            "leg_l": (-int(HR * 0.10), -int(HR * 0.05), int(HR * 0.35)),
            "leg_r": (int(HR * 0.15), int(HR * 0.05), int(HR * 0.20)),
            "feet_off_ground": True,
        },
    },
    # ─────────────────────────────────────────────────────────────────────────
    # FRUSTRATED — TIGHT CROSSED ARMS (v009 silhouette fix, custom draw)
    # Arms cross MID-TORSO horizontally. Defined by draw_crossed_arms().
    # Distinct from WORRIED (chest-level self-hug) in crossing height + read.
    # "arm_l"/"arm_r" not used — custom draw handles the pose.
    # ─────────────────────────────────────────────────────────────────────────
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
        "mouth": "tight_frown",
        "cy_offset": int(HR * 0.06),
        "pose": {
            "body_tilt": int(HR * 0.10),
            # Not used — draw_crossed_arms() handles this expression
            "arm_l": None,
            "arm_r": None,
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

    head_cx = rw // 2
    head_cy = int(rh * 0.18) + cy_off

    # Draw body first (behind head)
    draw_body_pose(draw, head_cx, head_cy, hoodie_c, spec.get("pose", {}),
                   expr_name=expr)

    # THE NOTICING special: bent-arm-to-chin hand gesture
    if spec.get("noticing_hand"):
        draw_noticing_hand(draw, head_cx, head_cy, hoodie_c)

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
# 7 expressions in 3×3 grid. Slots 7 and 8 intentionally blank.
EXPRESSIONS = [
    "THE NOTICING",   # slot 0 — anchor (top-left)
    "CURIOUS",        # slot 1
    "DETERMINED",     # slot 2
    "SURPRISED",      # slot 3
    "WORRIED",        # slot 4
    "DELIGHTED",      # slot 5
    "FRUSTRATED",     # slot 6
    # slots 7 and 8 left blank
]


def build_sheet(show_guides=False):
    """Build full 1200×900 expression sheet."""
    sheet = Image.new("RGB", (TOTAL_W, TOTAL_H), CANVAS_BG)
    draw  = ImageDraw.Draw(sheet)

    try:
        font_title  = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        font_label  = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
        font_sub    = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        font_anchor = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
    except Exception:
        font_title  = ImageFont.load_default()
        font_label  = font_title
        font_sub    = font_title
        font_anchor = font_title

    title = "LUMA — Expression Sheet v009  |  Luma & the Glitchkin"
    sub   = ("Designer: Maya Santos  |  Cycle 34  |  "
             "3.2 heads  |  ew = head_height\u00d70.22  |  "
             "v009: ARM SILHOUETTE DIFFERENTIATION (--mode arms fix)")
    draw.text((PAD, 8),  title, fill=(59, 40, 32), font=font_title)
    draw.text((PAD, 34), sub,   fill=(110, 88, 68), font=font_sub)

    for idx, expr in enumerate(EXPRESSIONS):
        col = idx % COLS
        row = idx // COLS
        px  = PAD + col * (PANEL_W + PAD)
        py  = HEADER + PAD + row * (PANEL_H + LABEL_H + PAD)

        bg  = BG[expr]
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], fill=bg)

        border_w = 3 if expr == "THE NOTICING" else 2
        border_c = (80, 100, 140) if expr == "THE NOTICING" else LINE
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H],
                       outline=border_c, width=border_w)

        char_img = render_character(expr, PANEL_W - PAD * 2, PANEL_H - PAD)
        ox = px + PAD
        oy = py + PAD // 2
        sheet.paste(char_img, (ox, oy), char_img)

        draw = ImageDraw.Draw(sheet)

        label_y  = py + PANEL_H + 2
        label_bg = tuple(max(0, int(c * 0.88)) for c in bg)
        draw.rectangle([px, label_y, px + PANEL_W, label_y + LABEL_H], fill=label_bg)

        label_text = expr
        try:
            bbox = draw.textbbox((0, 0), label_text, font=font_label)
            tw   = bbox[2] - bbox[0]
            th   = bbox[3] - bbox[1]
        except Exception:
            tw, th = 100, 14
        tx = px + (PANEL_W - tw) // 2
        ty = label_y + (LABEL_H - th) // 2
        label_col = (80, 100, 140) if expr == "THE NOTICING" else LINE
        draw.text((tx, ty), label_text, fill=label_col, font=font_label)

        if expr == "THE NOTICING":
            tag = "★ anchor expression"
            try:
                tbbox = draw.textbbox((0, 0), tag, font=font_anchor)
                ttw   = tbbox[2] - tbbox[0]
            except Exception:
                ttw   = 80
            tx2 = px + (PANEL_W - ttw) // 2
            ty2 = label_y + th + 4
            draw.text((tx2, ty2), tag, fill=(80, 100, 140), font=font_anchor)

    # Slots 7 and 8 remain blank canvas

    return sheet


def main():
    out_dir  = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "characters", "main")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_luma_expressions_v009.png")
    sheet    = build_sheet(show_guides=False)
    # IMAGE SIZE RULE: ≤ 1280px in both dimensions
    sheet.thumbnail((1280, 1280), Image.LANCZOS)
    sheet.save(out_path)
    print(f"Saved: {os.path.abspath(out_path)}")
    print(f"Canvas: {sheet.size[0]}x{sheet.size[1]}")


if __name__ == "__main__":
    main()
