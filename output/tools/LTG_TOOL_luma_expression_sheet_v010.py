#!/usr/bin/env python3
"""
LTG_TOOL_luma_expression_sheet_v010.py
Luma Expression Sheet — v010  THE NOTICING REWORK
"Luma & the Glitchkin" — Cycle 37 / Maya Santos

v010 GOAL: Improve THE NOTICING's emotional read.
  Critics score it 52-58/100 consistently. The pose geometry (chin-touch, asymmetric
  eyes, zero tilt) is correct but the expression "doesn't land." Root cause diagnosis:

  PROBLEM 1 — Eye asymmetry too subtle at panel scale.
    v009 used l_open=1.0, r_open=0.85. At 373px panel width, after LANCZOS
    downsampling, the 15% height difference is ~2px and reads as nearly identical eyes.
    Fix: l_open=1.0, r_open=0.65. The right eye narrows to 65% — reads as a squint-
    lean toward the noticed thing. The asymmetry now survives thumbnail scale.

  PROBLEM 2 — Head dead-neutral zero tilt reads as "daydreaming," not "noticing."
    Zero tilt means Luma is equally open to all directions. The noticed thing has
    a direction — she must fractionally tilt toward it (right). A 3-4px head tilt
    right (tilt_offset in body_tilt) creates the physical micro-lean of someone
    whose attention has been arrested by something specific.
    Fix: body_tilt = +int(HR * 0.03) (small right lean) + cy_offset = -int(HR * 0.04)
    (head fractionally higher — the physical lift of alert recognition).

  PROBLEM 3 — Panel BG is too pale/passive.
    v009 used (218, 226, 235) — pale blue-grey. At small size this reads as
    "blank" and gives no emotional charge to the expression. THE NOTICING is an
    interior moment — it needs a slightly deeper, cooler, more charged field.
    Fix: BG = (195, 210, 228) — deeper blue-grey. Still cool/interior but has
    presence. Makes the panel read as distinct from CURIOUS/DETERMINED (warm panels).

  PROBLEM 4 — Noticing hand doesn't read as "stopped in tracks."
    v009: hand at cx + HR*0.95, plain ellipse at chin level. Reads as casual
    thinking-pose. THE NOTICING is a freeze-frame — the kid is arrested by something.
    Fix: draw_noticing_hand_v010() — finger-to-lower-lip gesture. Index finger
    extended slightly upward (specificity of contact), thumb tucked. The arm path
    is more deliberate — comes UP from below rather than sideways. Creates a
    vertical forearm line which is visually distinct from horizontal arms in other
    expressions.

  PROBLEM 5 — Left eye gaze direction doesn't feel "tracking something."
    v009: gaze_dx=-0.4, gaze_dy=0.15 (looking slightly left and slightly down).
    The down-component reads as "distracted," not "locking onto something."
    Fix: gaze_dx=-0.5, gaze_dy=0.0. Pure lateral tracking left — the noticed
    thing is to Luma's left, at eye level. The 0 vertical component snaps the
    gaze to feel directed and intentional.

  PROBLEM 6 — Hoodie color too cool/passive for THE NOTICING.
    v009: (130, 148, 172) — muted blue-grey that blends into the cool BG.
    Fix: (105, 128, 162) — slightly deeper/richer slate blue. Creates clear
    figure/ground separation against the deeper BG while remaining interior/cool.

  PROBLEM 7 — Left brow asymmetry not strong enough.
    v009: brow_l_dy=-int(HR*0.14), brow_r_dy=-int(HR*0.06).
    The difference (0.08×HR ≈ 8px at 2x) is too small at downsampled scale.
    Fix: brow_l_dy=-int(HR*0.22), brow_r_dy=-int(HR*0.04).
    Left brow lifts significantly more — the "one eyebrow way up" of someone
    clocking something unexpected. This is the strongest readable brow signal.

ALL OTHER EXPRESSIONS: unchanged from v009. All v009 silhouette work preserved.

EYE-WIDTH: ew = int(HEAD_HEIGHT_2X × 0.22) = 45px at 2x (unchanged).

LAYOUT: 3×3 grid, 9 slots. 7 filled, 2 blank. THE NOTICING moves from slot 0
  (top-left) to slot 4 (CENTER) to give it visual primacy in the grid.
  This makes it the anchoring focal point instead of being read first-and-fast
  in corner position. Center position = the expression the eye returns to.

Output: output/characters/main/LTG_CHAR_luma_expressions_v010.png

Author: Maya Santos
Date: 2026-03-30
Cycle: 37
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
# v010: THE NOTICING hoodie is deeper/richer slate blue for better figure/ground separation
HOODIE_MAP = {
    "THE NOTICING": (105, 128, 162),   # v010: deeper slate blue (was 130,148,172 in v009)
    "CURIOUS":      (150, 175, 200),   # cool blue-gray
    "DETERMINED":   (155,  85, 45),    # warm amber-red
    "SURPRISED":    (232, 112, 42),    # full orange
    "WORRIED":      ( 80, 100, 140),   # muted indigo
    "DELIGHTED":    (232, 112, 42),    # full orange
    "FRUSTRATED":   (135,  75, 65),    # muted terracotta
}

# v010: THE NOTICING BG is deeper blue-grey for more emotional charge
BG = {
    "THE NOTICING": (195, 210, 228),   # v010: deeper blue-grey (was 218,226,235 in v009)
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

# EYE-WIDTH: head_height × 0.22 (turnaround-aligned, unchanged from v008/v009)
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
        # v009: Barely-parted, mid-breath of recognition
        pts = bezier3((lx + int(s*8), my + int(s*2)), (cx, my - int(s*4)),
                      (rx - int(s*8), my + int(s*2)))
        polyline(draw, pts, LINE, width=3)
        draw.ellipse([cx - int(s*6), my + int(s*3), cx + int(s*6), my + int(s*10)],
                     fill=(210, 65, 48))
    elif style == "noticing_v010":
        # v010: Tighter, slightly open — breath caught, not just thinking.
        # Lower corners pulled fractionally down (asymmetric — left side pulled
        # more than right, because the noticed thing is on the left).
        pts = bezier3((lx + int(s*10), my + int(s*6)), (cx - int(s*6), my - int(s*2)),
                      (rx - int(s*14), my + int(s*2)))
        polyline(draw, pts, LINE, width=3)
        # Tiny breath-parted opening — dark interior dot, not full open
        draw.ellipse([cx - int(s*5) - int(s*8), my + int(s*4),
                      cx + int(s*3) - int(s*8), my + int(s*10)],
                     fill=(190, 60, 42))
    elif style == "tight_frown":
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


def draw_noticing_hand_v010(draw, cx, head_cy, hoodie_col):
    """
    v010: Improved 'stopped in tracks' hand gesture for THE NOTICING.

    v009: hand at cx+HR*0.95, generic ellipse at chin level.
          Reads as casual thinking.

    v010: Finger-to-lower-lip gesture. The arm comes UP from below (from the
          torso right side), creating a VERTICAL forearm line. The hand arrives
          at the lower lip with the index finger slightly extended upward.
          This is the specific physical freeze of someone just noticing something —
          not a cognitive gesture (chin-stroke) but a caught-in-the-moment gesture
          (hand to mouth/lip, breath-stopped).

          Silhouette hook: the arm path is a strong diagonal from lower-right torso
          to upper-right face, ending in a near-vertical forearm. At thumbnail scale
          this reads as a clear diagonal arm line that no other expression has.
    """
    s = HR / 100.0

    # Shoulder/torso origin — right side of torso, at upper torso height
    torso_r_x  = cx + int(HR * 0.82)
    torso_r_y  = head_cy + int(HR * 1.55)

    # Elbow — mid-path, slightly right and above torso shoulder
    elbow_x    = cx + int(HR * 1.10)
    elbow_y    = head_cy + int(HR * 0.85)

    # Hand arrival — at lower lip (cx right side, at lip level)
    hand_cx    = cx + int(HR * 0.72)
    hand_cy    = head_cy + int(HR * 0.48)   # lower lip level

    arm_w      = int(HR * 0.28)

    # Draw arm as bezier: shoulder → elbow → hand
    pts = bezier3((torso_r_x, torso_r_y), (elbow_x, elbow_y),
                  (hand_cx, hand_cy + int(HR * 0.14)))
    polyline(draw, pts, hoodie_col, width=arm_w * 2)
    polyline(draw, pts, LINE, width=3)

    # Hand — compact oval at lower-lip (slightly smaller than v009 for precision)
    hand_r = int(HR * 0.20)
    draw.ellipse([hand_cx - hand_r, hand_cy - int(hand_r * 0.55),
                  hand_cx + hand_r, hand_cy + int(hand_r * 0.55)],
                 fill=SKIN, outline=LINE, width=3)

    # Index finger extended upward — a thin line from hand top, slight diagonal
    # This specificity is what makes the gesture readable as "stopped cold"
    finger_base_x = hand_cx - int(s * 4)
    finger_base_y = hand_cy - int(hand_r * 0.55)
    finger_tip_x  = hand_cx - int(s * 7)
    finger_tip_y  = hand_cy - int(hand_r * 0.55) - int(HR * 0.20)
    draw.line([(finger_base_x, finger_base_y), (finger_tip_x, finger_tip_y)],
              fill=SKIN, width=int(s * 7))
    draw.line([(finger_base_x, finger_base_y), (finger_tip_x, finger_tip_y)],
              fill=LINE, width=2)
    # Fingertip
    draw.ellipse([finger_tip_x - int(s*5), finger_tip_y - int(s*6),
                  finger_tip_x + int(s*5), finger_tip_y + int(s*4)],
                 fill=SKIN, outline=LINE, width=2)


def draw_crossed_arms(draw, cx, neck_cx, torso_top_y, hoodie_col):
    """FRUSTRATED: Arms crossed tight across body (unchanged from v009)."""
    arm_w = int(HR * 0.28)
    torso_top_w = int(HR * 0.70)

    l_shoulder_x = neck_cx - torso_top_w + int(HR * 0.10)
    l_shoulder_y = torso_top_y + int(HR * 0.20)
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
    """WORRIED: Self-hug arms (unchanged from v009)."""
    arm_w = int(HR * 0.28)
    torso_top_w = int(HR * 0.70)
    chest_y = torso_top_y + int(HR * 0.28)

    l_shoulder_x = neck_cx - torso_top_w + int(HR * 0.10)
    l_shoulder_y = torso_top_y + int(HR * 0.10)
    l_elbow_x = l_shoulder_x - int(HR * 0.08)
    l_elbow_y = l_shoulder_y + int(HR * 0.15)
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

    r_shoulder_x = neck_cx + torso_top_w - int(HR * 0.10)
    r_shoulder_y = torso_top_y + int(HR * 0.10)
    r_elbow_x = r_shoulder_x + int(HR * 0.08)
    r_elbow_y = r_shoulder_y + int(HR * 0.15)
    r_hand_x = neck_cx - int(HR * 0.38)
    r_hand_y = chest_y + int(HR * 0.08)
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
    v009/v010: FRUSTRATED and WORRIED get custom arm drawing.
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
    if expr_name == "FRUSTRATED":
        draw_crossed_arms(draw, cx, neck_cx, torso_top_y, hoodie_col)
    elif expr_name == "WORRIED":
        draw_self_hug_arms(draw, cx, neck_cx, torso_top_y, hoodie_col)
    else:
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
    # THE NOTICING — v010 REWORK (all 7 improvements applied)
    # ─────────────────────────────────────────────────────────────────────────
    "THE NOTICING": {
        "hair": "default",
        "blush": 30,    # v010: subtle blush — recognition has warmth. Was 0.
        "eyes": {
            # v010: STRONGER asymmetry. Left = fully open (1.0). Right = 0.65 squint.
            # At thumbnail scale the 35% height difference now survives downsampling.
            "l_open": 1.0, "r_open": 0.65,
            # v010: Left brow lifts dramatically more — "one eyebrow way up" of noticing.
            "brow_l_dy": -int(HR * 0.22), "brow_r_dy": -int(HR * 0.04),
            # v010: Pure lateral gaze left (gaze_dy=0, not 0.15).
            # The noticed thing is at eye level — directed, intentional, not wandering.
            "gaze_dx": -0.5, "gaze_dy": 0.0,
            "brow_furrow_l": False, "brow_furrow_r": False,
        },
        "mouth": "noticing_v010",   # v010: tighter, asymmetric breath-catch
        # v010: head fractionally up (recognition = physical lift of alertness)
        # Also very slight lean toward noticed thing via body_tilt (+right)
        "cy_offset": -int(HR * 0.04),
        "pose": {
            # v010: tiny right lean — Luma is arrested by something to her right
            "body_tilt": int(HR * 0.03),
            # Left arm: hanging at side (same as v009 — unchanged)
            "arm_l": (-int(HR * 0.08), int(HR * 0.96), -int(HR * 0.04), int(HR * 0.10)),
            "arm_r": None,   # right arm handled by draw_noticing_hand_v010()
            "leg_l": (-int(HR * 0.30), -int(HR * 0.22)),
            "leg_r": ( int(HR * 0.30),  int(HR * 0.22)),
            "feet_off_ground": False,
        },
        "noticing_hand_v010": True,   # v010: use improved hand gesture
    },
    # ─────────────────────────────────────────────────────────────────────────
    # CURIOUS — unchanged from v009
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
            "arm_l": (-int(HR * 1.20), -int(HR * 0.20), -int(HR * 0.08), -int(HR * 0.50)),
            "arm_r": (int(HR * 0.15), int(HR * 0.90), int(HR * 0.05), int(HR * 0.05)),
            "leg_l": (-int(HR * 0.20), -int(HR * 0.20)),
            "leg_r": (int(HR * 0.10), int(HR * 0.12)),
            "feet_off_ground": False,
        },
    },
    # ─────────────────────────────────────────────────────────────────────────
    # DETERMINED — unchanged from v009
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
            "arm_l": (-int(HR * 0.18), int(HR * 0.92),
                      -int(HR * 0.62), int(HR * 0.30)),
            "arm_r": (int(HR * 0.18), int(HR * 0.92),
                      int(HR * 0.62), int(HR * 0.30)),
            "leg_l": (-int(HR * 0.15), 0),
            "leg_r": (int(HR * 0.15), 0),
            "feet_off_ground": False,
        },
    },
    # ─────────────────────────────────────────────────────────────────────────
    # SURPRISED — unchanged from v009
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
            "arm_l": (-int(HR * 1.50), -int(HR * 0.55), -int(HR * 0.08), -int(HR * 0.60)),
            "arm_r": ( int(HR * 1.50), -int(HR * 0.55),  int(HR * 0.08), -int(HR * 0.60)),
            "leg_l": (-int(HR * 0.05), int(HR * 0.10)),
            "leg_r": (int(HR * 0.20), -int(HR * 0.05)),
            "feet_off_ground": False,
        },
    },
    # ─────────────────────────────────────────────────────────────────────────
    # WORRIED — unchanged from v009
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
            "arm_l": None,
            "arm_r": None,
            "leg_l": (int(HR * 0.08), 0),
            "leg_r": (-int(HR * 0.08), 0),
            "feet_off_ground": False,
        },
    },
    # ─────────────────────────────────────────────────────────────────────────
    # DELIGHTED — unchanged from v009
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
            "arm_l": (-int(HR * 1.00), -int(HR * 1.50), -int(HR * 0.10), -int(HR * 0.40)),
            "arm_r": ( int(HR * 1.00), -int(HR * 1.50),  int(HR * 0.10), -int(HR * 0.40)),
            "leg_l": (-int(HR * 0.10), -int(HR * 0.05), int(HR * 0.35)),
            "leg_r": (int(HR * 0.15), int(HR * 0.05), int(HR * 0.20)),
            "feet_off_ground": True,
        },
    },
    # ─────────────────────────────────────────────────────────────────────────
    # FRUSTRATED — unchanged from v009
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

    # THE NOTICING v010: use improved hand gesture
    if spec.get("noticing_hand_v010"):
        draw_noticing_hand_v010(draw, head_cx, head_cy, hoodie_c)

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
# v010: THE NOTICING moves to CENTER slot (slot 4) for visual primacy.
# Previously slot 0 (top-left) — corner position gets scanned and dismissed fast.
# Center position = focal anchor the eye returns to repeatedly.
# Slot layout: 3×3 grid
#   slot 0  slot 1  slot 2
#   slot 3  slot 4  slot 5
#   slot 6  slot 7  slot 8 (blank)
EXPRESSIONS = [
    "CURIOUS",        # slot 0
    "DETERMINED",     # slot 1
    "SURPRISED",      # slot 2
    "WORRIED",        # slot 3
    "THE NOTICING",   # slot 4 — CENTER (v010 change — was slot 0 in v009)
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

    title = "LUMA — Expression Sheet v010  |  Luma & the Glitchkin"
    sub   = ("Designer: Maya Santos  |  Cycle 37  |  "
             "3.2 heads  |  ew = head_height\u00d70.22  |  "
             "v010: THE NOTICING rework (eye asymmetry + hand gesture + center position)")
    draw.text((PAD, 8),  title, fill=(59, 40, 32), font=font_title)
    draw.text((PAD, 34), sub,   fill=(110, 88, 68), font=font_sub)

    for idx, expr in enumerate(EXPRESSIONS):
        col = idx % COLS
        row = idx // COLS
        px  = PAD + col * (PANEL_W + PAD)
        py  = HEADER + PAD + row * (PANEL_H + LABEL_H + PAD)

        bg  = BG[expr]
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], fill=bg)

        # THE NOTICING gets a heavier, more prominent border
        border_w = 3 if expr == "THE NOTICING" else 2
        border_c = (60, 90, 140) if expr == "THE NOTICING" else LINE  # deeper blue in v010
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
        label_col = (60, 90, 140) if expr == "THE NOTICING" else LINE
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
            draw.text((tx2, ty2), tag, fill=(60, 90, 140), font=font_anchor)

    # Slots 7 and 8 remain blank canvas

    return sheet


def main():
    out_dir  = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "characters", "main")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_luma_expressions_v010.png")
    sheet    = build_sheet(show_guides=False)
    # IMAGE SIZE RULE: <= 1280px in both dimensions
    sheet.thumbnail((1280, 1280), Image.LANCZOS)
    sheet.save(out_path)
    print(f"Saved: {os.path.abspath(out_path)}")
    print(f"Canvas: {sheet.size[0]}x{sheet.size[1]}")
    print("v010: THE NOTICING improvements:")
    print("  - r_open 0.85->0.65 (stronger eye asymmetry)")
    print("  - brow_l_dy -0.14HR->-0.22HR (more dramatic left brow lift)")
    print("  - gaze_dy 0.15->0.0 (pure lateral tracking, not wandering downward)")
    print("  - noticing_hand_v010: finger-to-lower-lip gesture (vertical forearm)")
    print("  - BG: (218,226,235)->(195,210,228) deeper blue-grey")
    print("  - hoodie: (130,148,172)->(105,128,162) deeper slate")
    print("  - subtle blush added (alpha=30)")
    print("  - body_tilt +HR*0.03 (tiny lean toward noticed thing)")
    print("  - POSITION: slot 0 (top-left)->slot 4 (CENTER) for visual primacy")


if __name__ == "__main__":
    main()
