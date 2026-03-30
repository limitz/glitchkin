#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_luma_expression_sheet.py
Luma Expression Sheet — v013  TIER-1 SILHOUETTE BODY POSTURES
"Luma & the Glitchkin" — Cycle 41 / Maya Santos

v013 CHANGES (C41 — Alex Chen C41 directive: luma_silhouette_strategy.md Option 3 Hybrid):
  Tier-1 expression body posture upgrades. Goal: blur any Tier-1 panel to illegibility —
  the outline must distinguish from all other Tier-1 expressions.

  1. RECKLESS (replaces DELIGHTED) — Luma's signature expression added to sheet.
     Body: wide stance, arms slightly spread outward (tips extend beyond torso width).
     Lee Tanaka C41 brief: pupils at leading edge of iris (forward/lateral intent).
     Head: level or very slight upward tilt (0–+3°). Full blush, excited hair.
     Face: draw_luma_face("RECKLESS") via face curves system.

  2. ALARMED (replaces SURPRISED) — recoil / threat-response.
     Body: arms raised toward face — draw_alarmed_arms() (energy inward/upward).
     Lee Tanaka C41 brief: slight backward lean, pupils centered/back-edge.
     Small downward pupil drift for Byte-encounter P12 context.
     Face: draw_luma_face("ALARMED") via face curves system.

  3. FRUSTRATED — crossed arms already correct (draw_crossed_arms unchanged).
     No body change needed. Already Tier-1 compliant.

  4. THE NOTICING — gaze direction fix (Lee Tanaka C41 brief — CRITICAL).
     Pupils must aim toward frame-RIGHT (screen-right territory, where the noticed
     subject lives in P06/SF01). LI/RI_CENTER_dx +6px rightward shift via overrides.
     Everything else unchanged (forward lean, noticing hand, brow asymmetry).

  Tier-2 pairs (face-only — no body changes per strategy):
     THE NOTICING / THE NOTICING — DOUBT (same attending body, doubt is internal).
     WORRIED (stillness under worry IS the silhouette signal).

v012 CHANGES preserved (Alex Chen, Cycle 42):
  Face drawing for THE NOTICING, THE NOTICING — DOUBT, WORRIED, FRUSTRATED, DETERMINED
  routes through draw_luma_face() from LTG_TOOL_luma_face_curves.py v1.1.0.
  RECKLESS and ALARMED now also route through face curves (added in v013 mapping).

v011 NOTES (preserved for history):
  v011 GOAL: Fix THE NOTICING right eye lid geometry.
  Takeshi Murakami (C38 critique): the right eye uses a wince (symmetric
  bottom-lid-rises approach). It must be a SQUINT — top lid drops ~20-25%,
  bottom lid stays neutral.

  Root cause: v010 used r_open=0.65 which scales the eye ellipse symmetrically —
  both the top and bottom of the eye contract equally. This is a wince/sleepy-lid,
  not a focusing squint. A focusing squint (squinting AT something) pulls the
  UPPER lid down while the lower lid stays anchored.

  v011 FIX: `squint_top_r` parameter in draw_eyes_full().
  When True for the right eye:
    - Draw the full eye ellipse at r_open=1.0 (full natural height)
    - Compute a "lid drop" of 20-25% of reh_base from the TOP
    - Overdraw the top portion of the eye opening with a BG-colored rectangle
      (simulates the upper lid covering the top of the eye)
    - Draw the upper lash line as a thick arc across where the lid sits
  Result: bottom of eye stays at full height, top closes down from above —
  the physical mechanics of focusing on a distant/specific thing.

  All other v010 improvements preserved:
  - r_open fix now moot (squint_top_r replaces it)
  - brow asymmetry: brow_l_dy=-HR*0.22, brow_r_dy=-HR*0.04 (unchanged)
  - pure lateral gaze (gaze_dy=0.0) (unchanged)
  - noticing_hand_v010 gesture (unchanged)
  - BG deeper blue-grey (195,210,228) (unchanged)
  - hoodie deeper slate (105,128,162) (unchanged)
  - subtle blush=30 (unchanged)
  - body_tilt +HR*0.03 tiny lean (unchanged)
  - center slot position (unchanged)

Silhouette: same known WARN (Luma human chars — documented limitation).

v010 ORIGINAL NOTES (for history):
v010 GOAL: Improve THE NOTICING's emotional read.

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

Output: output/characters/main/LTG_CHAR_luma_expressions.png

Author: Maya Santos
Date: 2026-03-29
Cycle: 38
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os
import sys

# ── Face Curves Integration ───────────────────────────────────────────────────
# Import canonical bezier face system (v1.1.0 — 100px canonical eye width)
# Path: output/tools/LTG_TOOL_luma_face_curves.py (same directory)
_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
try:
    from LTG_TOOL_luma_face_curves import draw_luma_face as _draw_luma_face_curves
    _FACE_CURVES_AVAILABLE = True
except ImportError:
    _FACE_CURVES_AVAILABLE = False

# Expression name mapping: expression sheet name → face curves expression name
# Only expressions present in EXPRESSION_DELTAS in luma_face_curves are listed.
_FACE_CURVES_EXPR_MAP = {
    "THE NOTICING":         "THE_NOTICING",
    "THE NOTICING — DOUBT": "THE_NOTICING_DOUBT",
    "WORRIED":              "WORRIED",
    "FRUSTRATED":           "FRUSTRATED",
    "DETERMINED":           "DETERMINED",
    "ALARMED":              "ALARMED",
    "RECKLESS":             "RECKLESS",
}
# Note: CURIOUS retains v011 hand-coded face drawing (no matching face curves expression).

# Per-expression overrides applied on top of the face curves expression delta.
# Use to fine-tune iris shift, blush, or any scalar that differs at expression-sheet
# scale from the spec default.
# v013: THE NOTICING — gaze correction per Lee Tanaka C41 sight-line brief.
#   Pupils MUST aim toward frame-right (screen-right territory, where the noticed
#   subject lives in P06/SF01). LI_CENTER_dx/RI_CENTER_dx shift iris rightward.
#   +6px at 2x render scale → visible pupil shift toward right of panel.
_FACE_CURVES_OVERRIDES = {
    "THE NOTICING":         {"LI_CENTER_dx": +6, "RI_CENTER_dx": +6},
    "THE NOTICING — DOUBT": {"LI_CENTER_dx": +6, "RI_CENTER_dx": +6},  # same attending gaze
}

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
    "THE NOTICING": (105, 128, 162),   # v010: deeper slate blue
    "THE NOTICING — DOUBT": (112, 124, 152),  # v011: same cool family, muted uncertainty
    "CURIOUS":      (150, 175, 200),   # cool blue-gray
    "DETERMINED":   (155,  85, 45),    # warm amber-red
    "RECKLESS":     (232, 112, 42),    # full orange — Luma's signature energy (v013: replaces DELIGHTED)
    "ALARMED":      (200,  90, 38),    # deeper burnt orange — stress-warm (v013: replaces SURPRISED)
    "WORRIED":      ( 80, 100, 140),   # muted indigo
    "FRUSTRATED":   (135,  75, 65),    # muted terracotta
}

# v010: THE NOTICING BG is deeper blue-grey for more emotional charge
BG = {
    "THE NOTICING": (195, 210, 228),   # v010: deeper blue-grey
    "THE NOTICING — DOUBT": (186, 198, 218),  # v011: same family, cooler/darker uncertainty
    "CURIOUS":      (230, 240, 235),   # soft warm mint
    "DETERMINED":   (238, 228, 210),   # warm parchment
    "RECKLESS":     (248, 236, 210),   # warm golden cream — signature excitement (v013)
    "ALARMED":      (242, 230, 218),   # warm pale — adrenaline moment (v013)
    "WORRIED":      (225, 230, 242),   # pale blue-gray
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


def draw_eyes_full(draw, cx, cy, params, bg_color=None):
    """Classroom-style eyes with turnaround-aligned eye width.

    v011 addition: squint_top_r parameter.
    When params["squint_top_r"] is True, the right eye is drawn with the UPPER
    lid dropping ~22% (not a symmetric shrink — that's a wince). The lower lid
    stays at its natural position. This is the physical mechanic of a focusing
    squint — upper lid drops, lower stays, creating the "locking onto something"
    directional look.

    Algorithm for squint_top_r:
      1. Draw the full right eye ellipse at r_open=1.0 (natural open height)
      2. Compute lid_drop = int(reh_base * 0.22) — the top lid descent
      3. Overdraw the top lid_drop pixels of the eye with a BG-colored rect
         (masks out the top of the eye, simulating the lid covering from above)
      4. Draw a thick horizontal lid line at the new top of visible eye opening
      This is then capped with the standard lower-lash arc.
    """
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

    squint_top_r = p.get("squint_top_r", False)

    if p.get("half_lid"):
        leh = max(4, int(leh_base * 0.50))
        reh = max(4, int(reh_base * 0.50))
    else:
        leh = max(4, int(leh_base * l_open))
        # For squint_top_r: right eye stays at FULL natural height (reh_base)
        # — the lid drop is applied as an overdraw, not a geometry change.
        reh = reh_base if squint_top_r else max(4, int(reh_base * r_open))

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

        # v011: squint_top_r — right eye only: upper lid drop (not a wince)
        if is_right and squint_top_r:
            # Drop amount: 22% of the natural eye half-height
            lid_drop = int(reh_base * 0.22)
            # The visible top of the eye opening is now eye_y - reh_base + lid_drop
            new_top_y = eye_y - reh_base + lid_drop
            # Overdraw the upper portion (above new_top_y) with the panel BG color
            # to simulate the lid covering it from above
            mask_color = bg_color if bg_color is not None else (235, 224, 206)
            # Overdraw from the full ellipse top to new_top_y
            draw.rectangle([ex - ew - 1, eye_y - reh_base - 3,
                             ex + ew + 1, new_top_y], fill=mask_color)
            # Draw the lid as a strong horizontal line (the lid edge)
            draw.line([(ex - ew + 2, new_top_y), (ex + ew - 2, new_top_y)],
                      fill=LINE, width=4)
            # Draw a slight bowing of the lid (it's not perfectly flat — curves
            # slightly upward in the center, like a real upper lid)
            lid_bow = int(reh_base * 0.06)  # very slight bow
            for bow_x in range(-ew + 3, ew - 3, 2):
                # Parabolic bow: 0 at edges, lid_bow at center
                bow_y = int(lid_bow * (1 - (bow_x / ew) ** 2))
                draw.point((ex + bow_x, new_top_y - bow_y), fill=LINE)
            # Also clean up the border of the eye above new_top_y
            # Redraw a partial top arc in mask_color to ensure clean cutoff
            draw.arc([ex - ew, eye_y - reh_base, ex + ew, eye_y + reh_base],
                     start=220, end=320, fill=mask_color, width=5)
            # Redraw the outer border line of the lid
            draw.line([(ex - ew + 2, new_top_y), (ex + ew - 2, new_top_y)],
                      fill=LINE, width=3)

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
    elif style == "doubt_corner":
        # v011: THE NOTICING DOUBT VARIANT — Lee Tanaka brief.
        # Mouth nearly closed. RIGHT corner (Luma's right = viewer's left) pulled DOWN
        # slightly. The body's resistance to a conclusion it hasn't granted permission.
        # Lower lip slightly forward (present, not pouted).
        # NOT a frown: one corner deflects ~3px down, other stays near-neutral.
        # Left corner (viewer's left = Luma's right): tiny upturn (she almost wants it to be true)
        # Right corner (viewer's right = Luma's left): 3px down (the doubt side)
        left_y  = my + int(s * 2)    # nearly neutral left corner
        right_y = my + int(s * 8)    # doubt corner — 3px lower in design space
        # Mouth line goes left-to-right with slight asymmetric droop on right
        pts = bezier3((lx + int(s*6), left_y), (cx - int(s*4), my + int(s*4)),
                      (rx - int(s*8), right_y))
        polyline(draw, pts, LINE, width=3)
        # Lower lip — slightly forward/present (a small filled ellipse just below center)
        draw.ellipse([cx - int(s*10), my + int(s*6), cx + int(s*4), my + int(s*13)],
                     fill=LINE)


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


def draw_worried_wide_arms(draw, cx, neck_cx, torso_top_y, hoodie_col):
    """
    WORRIED v011: Arms angled OUT from body — wide anxious spread.

    v009/v010 used draw_self_hug_arms which wraps arms INWARD across chest.
    Problem: at RPD measurement scale the "arms wrapping toward center" profile
    is too similar to FRUSTRATED's crossed arms (both create centerward arm mass).

    v011 REDESIGN: Arms extend OUT and slightly DOWN from shoulders — a wide
    anxious "I don't know what to do" spread. Creates:
      - Strong horizontal extension LEFT AND RIGHT of body silhouette
      - Hands hanging at hip level, away from center (not clasped)
      - "Helpless" open-palms-out posture: arms angle outward 45° from body

    Silhouette result: wide mass OUTSIDE torso on BOTH SIDES.
    vs FRUSTRATED: tight cross INSIDE torso.
    RPD arms zone: opposite profiles (mass at edges vs mass at center).
    """
    arm_w = int(HR * 0.28)
    torso_top_w = int(HR * 0.70)

    # Left arm: from left shoulder, angles out-left and slightly down
    l_shoulder_x = neck_cx - torso_top_w + int(HR * 0.10)
    l_shoulder_y = torso_top_y + int(HR * 0.15)
    l_elbow_x = neck_cx - torso_top_w - int(HR * 0.50)   # extends well LEFT of torso
    l_elbow_y = l_shoulder_y + int(HR * 0.40)
    l_hand_x = neck_cx - torso_top_w - int(HR * 0.85)    # hand far left
    l_hand_y = l_shoulder_y + int(HR * 0.75)
    pts_l = bezier3((l_shoulder_x, l_shoulder_y), (l_elbow_x, l_elbow_y),
                    (l_hand_x, l_hand_y))
    polyline(draw, pts_l, hoodie_col, width=arm_w * 2)
    polyline(draw, pts_l, LINE, width=3)
    hand_r = int(HR * 0.22)
    draw.ellipse([l_hand_x - hand_r, l_hand_y - int(hand_r * 0.7),
                  l_hand_x + hand_r, l_hand_y + int(hand_r * 0.7)],
                 fill=SKIN, outline=LINE, width=3)

    # Right arm: from right shoulder, angles out-right and slightly down
    r_shoulder_x = neck_cx + torso_top_w - int(HR * 0.10)
    r_shoulder_y = torso_top_y + int(HR * 0.15)
    r_elbow_x = neck_cx + torso_top_w + int(HR * 0.50)   # extends well RIGHT of torso
    r_elbow_y = r_shoulder_y + int(HR * 0.40)
    r_hand_x = neck_cx + torso_top_w + int(HR * 0.85)    # hand far right
    r_hand_y = r_shoulder_y + int(HR * 0.75)
    pts_r = bezier3((r_shoulder_x, r_shoulder_y), (r_elbow_x, r_elbow_y),
                    (r_hand_x, r_hand_y))
    polyline(draw, pts_r, hoodie_col, width=arm_w * 2)
    polyline(draw, pts_r, LINE, width=3)
    draw.ellipse([r_hand_x - hand_r, r_hand_y - int(hand_r * 0.7),
                  r_hand_x + hand_r, r_hand_y + int(hand_r * 0.7)],
                 fill=SKIN, outline=LINE, width=3)


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


def draw_alarmed_arms(draw, cx, neck_cx, torso_top_y, hoodie_col):
    """
    ALARMED v013: Arms raised — energy inward/upward, recoil geometry.

    Alex Chen C41 directive: at least one arm raised or hands-to-face.
    Lee Tanaka C41 brief: body orientation = arms up / hands to face, energy inward/upward.

    Design: Both arms raise toward face level — a bilateral recoil. Left arm raises
    higher (hand near chin, guarding), right arm also raised but slightly lower and
    out (spreading to assess the threat). This creates a strong distinct silhouette
    from FRUSTRATED (arms crossed, horizontal) and THE NOTICING (one arm at side).

    The raised-hands configuration reads as "ALARMED" even when the face is blurred:
    mass at upper body, away from torso sides, reaching toward head.
    """
    arm_w = int(HR * 0.28)
    torso_top_w = int(HR * 0.70)
    hand_r = int(HR * 0.22)

    # Left arm: raises sharply up toward chin/cheek area — guard position
    l_shoulder_x = neck_cx - torso_top_w + int(HR * 0.10)
    l_shoulder_y = torso_top_y + int(HR * 0.15)
    l_elbow_x = neck_cx - int(HR * 0.35)
    l_elbow_y = l_shoulder_y - int(HR * 0.25)
    l_hand_x  = neck_cx - int(HR * 0.55)
    l_hand_y  = l_shoulder_y - int(HR * 0.55)   # hands raised to chin level
    pts_l = bezier3((l_shoulder_x, l_shoulder_y), (l_elbow_x, l_elbow_y),
                    (l_hand_x, l_hand_y))
    polyline(draw, pts_l, hoodie_col, width=arm_w * 2)
    polyline(draw, pts_l, LINE, width=3)
    draw.ellipse([l_hand_x - hand_r, l_hand_y - int(hand_r * 0.7),
                  l_hand_x + hand_r, l_hand_y + int(hand_r * 0.7)],
                 fill=SKIN, outline=LINE, width=3)

    # Right arm: raised outward and up — defensive spreading, assessing space
    r_shoulder_x = neck_cx + torso_top_w - int(HR * 0.10)
    r_shoulder_y = torso_top_y + int(HR * 0.15)
    r_elbow_x = neck_cx + int(HR * 0.60)
    r_elbow_y = r_shoulder_y - int(HR * 0.10)
    r_hand_x  = neck_cx + int(HR * 0.72)
    r_hand_y  = r_shoulder_y - int(HR * 0.40)   # raised but lower than left
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
    v013: ALARMED also gets custom arm drawing (raised arms).
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
        # v011: REVERTED to draw_self_hug_arms (from v009).
        # draw_worried_wide_arms was tried but caused regression on CURIOUS↔WORRIED pair
        # (85.8%→87.5%) while only improving WORRIED↔FRUSTRATED by 2%.
        # Root cause: ~373px panel width creates shared torso column projection that
        # overwhelms arm extension differences. This is the documented C33-C37 tool
        # limitation for standing human characters. The visual design of self-hug
        # is the correct storytelling choice for WORRIED — retain it.
        draw_self_hug_arms(draw, cx, neck_cx, torso_top_y, hoodie_col)
    elif expr_name == "ALARMED":
        # v013: raised arms toward face — energy inward/upward (Tier-1 body posture)
        draw_alarmed_arms(draw, cx, neck_cx, torso_top_y, hoodie_col)
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
            # v011: LEFT eye fully open (1.0). RIGHT eye = SQUINT (top lid drops
            # ~22%). This is a focusing squint, not a wince. The bottom lid stays
            # neutral — only the UPPER lid drops. squint_top_r=True triggers the
            # new upper-lid-drop rendering in draw_eyes_full() v011.
            # v010 used r_open=0.65 (symmetric shrink = wince). That is FIXED here.
            "l_open": 1.0, "r_open": 1.0,   # r_open=1.0 because squint_top_r handles it
            "squint_top_r": True,             # v011: top-lid-drop squint on right eye
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
        # v011 (Alex Chen power-balance): chin-forward thrust +HR*0.02 (instinct to get closer)
        "cy_offset": -int(HR * 0.04),
        "cx_offset": int(HR * 0.02),   # v011: chin-forward — instinct to get closer to the thing
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
    # DETERMINED — v011 update (Alex Chen power-balance direction)
    # Forward hip lean: weight on front foot, about to start running.
    # body_tilt 0→-HR*0.08 (lean forward from hips), left leg slightly forward.
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
            # v011: -HR*0.08 forward lean (was 0). Body tips from hips — she's about to run.
            "body_tilt": -int(HR * 0.08),
            # Arms slightly forward from body (pulled in during a forward lean, not hanging)
            "arm_l": (-int(HR * 0.22), int(HR * 0.88),
                      -int(HR * 0.55), int(HR * 0.22)),
            "arm_r": (int(HR * 0.22), int(HR * 0.88),
                      int(HR * 0.55), int(HR * 0.22)),
            # Weight on left foot (slightly forward), right foot planted behind
            "leg_l": (-int(HR * 0.22), -int(HR * 0.12)),  # left leg forward
            "leg_r": (int(HR * 0.18), int(HR * 0.08)),    # right leg plants
            "feet_off_ground": False,
        },
    },
    # ─────────────────────────────────────────────────────────────────────────
    # ALARMED — v013 NEW (Tier-1 silhouette expression, Alex Chen C41 directive)
    # Replaces SURPRISED. Body: at least one arm raised / hands-to-face.
    # Energy inward/upward. Slight backward tilt (recoil geometry).
    # Face: via draw_luma_face("ALARMED") — wide eyes, brows shoot up, jaw drop.
    # Lee Tanaka sight-line brief: pupils centered or back-edge; slight downward
    # shift (~5px at expression sheet scale) for Byte-encounter context (Byte is
    # much shorter than Luma — P12 context).
    # draw_alarmed_arms() handles the body silhouette requirement.
    # ─────────────────────────────────────────────────────────────────────────
    "ALARMED": {
        "hair": "excited",  # hair puffs up in alarm
        "blush": 0,         # adrenaline drains blush
        "eyes": {           # fallback only — draw_luma_face() handles ALARMED face
            "l_open": 1.0, "r_open": 1.0,
            "brow_l_dy": -int(HR * 0.32), "brow_r_dy": -int(HR * 0.32),
            "gaze_dx": 0, "gaze_dy": 0.15,  # slightly down (Byte scale)
            "pupils_wide": True,
            "brow_furrow_l": False, "brow_furrow_r": False,
        },
        "mouth": "open_oval",  # fallback
        "cy_offset": -int(HR * 0.06),  # head back slightly (recoil)
        "pose": {
            # Slight backward tilt — 2-5° back per Lee Tanaka brief
            "body_tilt": int(HR * 0.12),  # lean back
            "arm_l": None,  # ALARMED arms handled by draw_alarmed_arms()
            "arm_r": None,
            # Wide stance — body braced
            "leg_l": (-int(HR * 0.18), int(HR * 0.05)),
            "leg_r": ( int(HR * 0.18), -int(HR * 0.05)),
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
    # RECKLESS — v013 NEW (Tier-1 silhouette expression — Luma's signature state)
    # Replaces DELIGHTED. Matches luma.md §9 "RECKLESS EXCITEMENT" description.
    # Alex Chen C41 directive: wide stance, arms slightly out — energy-outward.
    # Lee Tanaka C41 brief: pupils at leading edge of iris (forward/lateral intent,
    # not panic). Head level to +3° up. Arm tips > torso width on each side.
    # Face: via draw_luma_face("RECKLESS") — big grin, both eyes wide, brows high.
    # ─────────────────────────────────────────────────────────────────────────
    "RECKLESS": {
        "hair": "excited",  # hair puffs up with energy
        "blush": 140,       # full blush — RECKLESS EXCITEMENT spec says outer cheek full
        "eyes": {           # fallback only — draw_luma_face() handles RECKLESS face
            "l_open": 1.0, "r_open": 1.0,
            "brow_l_dy": -int(HR * 0.28), "brow_r_dy": -int(HR * 0.28),
            "gaze_dx": -0.3, "gaze_dy": -0.1,  # forward/slightly up — leading edge
            "pupils_wide": True,
            "brow_furrow_l": False, "brow_furrow_r": False,
        },
        "mouth": "smile_big",  # fallback
        "cy_offset": -int(HR * 0.08),  # head slightly up — confidence lift
        "pose": {
            # Very slight forward lean (energy forward, not backward)
            "body_tilt": -int(HR * 0.06),
            # Arms slightly out from body — energy-outward silhouette.
            # Lee brief: arm tips must extend beyond torso width by at least 10%.
            # torso_top_w = HR*0.70 → tips need to reach HR*0.70 + HR*0.10 = HR*0.80 from cx.
            # Using arm spec: shoulder at -(HR*0.60), arm end extends to -(HR*0.85) from cx.
            # This gives ~HR*0.85 extension = well beyond torso_top_w of HR*0.70.
            "arm_l": (-int(HR * 0.80), int(HR * 0.55), -int(HR * 0.12), int(HR * 0.15)),
            "arm_r": ( int(HR * 0.80), int(HR * 0.55),  int(HR * 0.12), int(HR * 0.15)),
            # Wide stance — energy outward in legs too
            "leg_l": (-int(HR * 0.22), -int(HR * 0.08)),
            "leg_r": ( int(HR * 0.22),  int(HR * 0.08)),
            "feet_off_ground": False,
        },
    },
    # ─────────────────────────────────────────────────────────────────────────
    # THE NOTICING — DOUBT VARIANT (v011 — Lee Tanaka C38 brief)
    # Taraji Coleman C15 note: "she doubts herself hardest in the exact moment
    # she is most correct." Same scene, different conviction level.
    # TWO EYES DISAGREE: left = certain (locked on), right = hedging (is this real?).
    # Upper right lid drops 3-4px vs left (not a squint, just a slight guard).
    # Left brow high (wonder). Right brow lower with inward kink (corrugator — "but...").
    # Mouth: nearly closed, right corner deflects slightly down (body resistance).
    # Body leans BACK 2-3° (buying time). Chin-touch preserved.
    # ─────────────────────────────────────────────────────────────────────────
    "THE NOTICING — DOUBT": {
        "hair": "default",
        "blush": 30,   # same as THE NOTICING — uncertainty also flushes
        "eyes": {
            # LEFT eye: locked on (fully open, certain). Same as THE NOTICING.
            "l_open": 1.0,
            # RIGHT eye: slightly guarded — NOT a full squint (that's THE NOTICING).
            # Just 3-4px of top-lid lowering = a fractional squint_top_r.
            # We reuse squint_top_r but with a gentler drop (controlled via r_open).
            # r_open=0.88 = natural open with a hint of lid closing (not a wince).
            # The asymmetry vs l_open=1.0 reads as "one eye believes, one hesitates."
            "r_open": 0.88,
            # LEFT brow: same high arc as THE NOTICING (wonder)
            "brow_l_dy": -int(HR * 0.22),
            # RIGHT brow: lower by ~8-10px vs left, with inward kink at inner corner
            "brow_r_dy": -int(HR * 0.06),  # lower than left (not mirrored)
            "brow_furrow_r": True,          # subtle inward corrugator kink on right
            "brow_furrow_l": False,
            # Gaze: same lateral tracking (she's still looking at the thing)
            "gaze_dx": -0.5, "gaze_dy": 0.0,
        },
        "mouth": "doubt_corner",   # v011: right corner slightly down, lower lip present
        # Head SLIGHTLY higher + backward — buying time
        "cy_offset": -int(HR * 0.02),   # slightly less raised than THE NOTICING
        "cx_offset": 0,   # no chin-forward — doubt pulls back
        "pose": {
            # v011 (Lee Tanaka brief): lean BACK 2-3°. Body buys itself a half-second.
            "body_tilt": -int(HR * 0.03),  # slight backward tilt (vs +HR*0.03 in THE NOTICING)
            # Non-chin arm: one arm slightly self-soothing — one arm crosses below chest,
            # cradling the other elbow. Not fully crossed — just contained.
            # Left arm: slightly crossed in front of body (cradling right elbow)
            "arm_l": (int(HR * 0.12), int(HR * 0.70), int(HR * 0.30), int(HR * 0.20)),
            "arm_r": None,   # right arm handled by draw_noticing_hand_v010()
            "leg_l": (-int(HR * 0.15), -int(HR * 0.10)),  # weight on left
            "leg_r": ( int(HR * 0.22),  int(HR * 0.18)),  # right planted
            "feet_off_ground": False,
        },
        "noticing_hand_v010": True,   # chin-touch preserved per brief
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

def render_character(expr, panel_w, panel_h, panel_bg=None):
    """Render full-body character panel at 2x scale, return 1x via LANCZOS.

    v013: RECKLESS and ALARMED added to face curves map; body postures updated.
    Per-expression overrides passed to draw_luma_face() for iris shift adjustments
    (e.g. THE NOTICING rightward gaze correction).

    v012: Face drawing routes through draw_luma_face() from
    LTG_TOOL_luma_face_curves v1.1.0 for all expressions that have a matching
    face curves expression. The canonical bezier system replaces the old
    draw_eyes_full() / draw_nose() / draw_mouth() calls for those expressions.

    Fallback: CURIOUS retains v011 hand-coded face drawing (no face curves expression).

    v011: panel_bg passed through to draw_eyes_full() for legacy squint_top_r
    overdraw (only used by fallback CURIOUS path now).
    """
    rw   = panel_w * RENDER_SCALE
    rh   = panel_h * RENDER_SCALE

    img  = Image.new("RGBA", (rw, rh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    spec      = EXPR_SPECS[expr]
    cy_off    = spec.get("cy_offset", 0)
    hoodie_c  = HOODIE_MAP[expr]

    cx_off    = spec.get("cx_offset", 0)    # v011: chin-forward thrust (horizontal head shift)
    head_cx = rw // 2 + cx_off
    head_cy = int(rh * 0.18) + cy_off

    # Draw body first (behind head)
    draw_body_pose(draw, rw // 2, head_cy, hoodie_c, spec.get("pose", {}),
                   expr_name=expr)

    # THE NOTICING v010: use improved hand gesture
    if spec.get("noticing_hand_v010"):
        draw_noticing_hand_v010(draw, rw // 2, head_cy, hoodie_c)

    draw = ImageDraw.Draw(img)

    # Determine face curves expression name (if available)
    curves_expr = _FACE_CURVES_EXPR_MAP.get(expr, None)
    use_curves  = _FACE_CURVES_AVAILABLE and curves_expr is not None

    if use_curves:
        # v012: canonical bezier face system path.
        # Hair first (behind face), then draw_luma_face() for all facial geometry.
        # draw_head() is NOT called — draw_luma_face() provides the face oval.
        # draw_ears() is also skipped — ear/cheek nubs were part of draw_head().
        draw_hair(draw, head_cx, head_cy, variant=spec["hair"])
        draw = ImageDraw.Draw(img)
        # draw_luma_face() handles: face oval, blush, eye outlines, irises,
        # pupils, highlights, nose bridge, mouth, brows — per spec v002.
        # v013: pass per-expression overrides (e.g. iris shift for THE NOTICING gaze).
        face_overrides = _FACE_CURVES_OVERRIDES.get(expr, None)
        _draw_luma_face_curves(draw, fc=(head_cx, head_cy), expression=curves_expr,
                               overrides=face_overrides)
    else:
        # Fallback: v011 hand-coded face drawing (CURIOUS only in v013)
        draw_head(draw, head_cx, head_cy)
        draw_ears(draw, head_cx, head_cy)
        draw_hair(draw, head_cx, head_cy, variant=spec["hair"])
        draw_blush(draw, head_cx, head_cy, alpha=spec["blush"])
        # v011: pass panel_bg for squint_top_r lid overdraw
        draw_eyes_full(draw, head_cx, head_cy, spec["eyes"], bg_color=panel_bg)
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
    "CURIOUS",                  # slot 0
    "DETERMINED",               # slot 1
    "ALARMED",                  # slot 2 — v013: replaces SURPRISED (Tier-1 body posture)
    "WORRIED",                  # slot 3
    "THE NOTICING",             # slot 4 — CENTER (v010 change — was slot 0 in v009)
    "RECKLESS",                 # slot 5 — v013: replaces DELIGHTED (Tier-1 body posture; Luma signature)
    "FRUSTRATED",               # slot 6
    "THE NOTICING — DOUBT",     # slot 7 — v011 addition (Lee Tanaka C38 brief)
    # slot 8 left blank
]


def build_sheet(show_guides=False):
    """Build full 1200×900 expression sheet (v013 — Tier-1 silhouette body postures)."""
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

    title = "LUMA — Expression Sheet v013  |  Luma & the Glitchkin"
    sub   = ("Designer: Maya Santos  |  Cycle 41  |  "
             "3.2 heads  |  ew = canonical 100px (face_curve_spec v002)  |  "
             "v013: Tier-1 silhouette body postures — RECKLESS/ALARMED added; THE NOTICING gaze fix")
    draw.text((PAD, 8),  title, fill=(59, 40, 32), font=font_title)
    draw.text((PAD, 34), sub,   fill=(110, 88, 68), font=font_sub)

    for idx, expr in enumerate(EXPRESSIONS):
        col = idx % COLS
        row = idx // COLS
        px  = PAD + col * (PANEL_W + PAD)
        py  = HEADER + PAD + row * (PANEL_H + LABEL_H + PAD)

        bg  = BG[expr]
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], fill=bg)

        # THE NOTICING and its DOUBT VARIANT get a heavier border
        is_noticing = (expr == "THE NOTICING")
        is_doubt    = (expr == "THE NOTICING — DOUBT")
        border_w = 3 if (is_noticing or is_doubt) else 2
        if is_noticing:
            border_c = (60, 90, 140)   # deep blue
        elif is_doubt:
            border_c = (72, 68, 110)   # muted violet (same cool family, more uncertain)
        else:
            border_c = LINE
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H],
                       outline=border_c, width=border_w)

        # v011: pass panel bg color so squint_top_r overdraw matches panel background
        char_img = render_character(expr, PANEL_W - PAD * 2, PANEL_H - PAD, panel_bg=bg)
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
        if is_noticing:
            label_col = (60, 90, 140)
        elif is_doubt:
            label_col = (72, 68, 110)
        else:
            label_col = LINE
        draw.text((tx, ty), label_text, fill=label_col, font=font_label)

        if is_noticing:
            tag = "★ anchor expression"
            try:
                tbbox = draw.textbbox((0, 0), tag, font=font_anchor)
                ttw   = tbbox[2] - tbbox[0]
            except Exception:
                ttw   = 80
            tx2 = px + (PANEL_W - ttw) // 2
            ty2 = label_y + th + 4
            draw.text((tx2, ty2), tag, fill=(60, 90, 140), font=font_anchor)

    # Slot 8 remains blank canvas (slot 7 = THE NOTICING — DOUBT, v011 addition)

    return sheet


def main():
    out_dir  = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "characters", "main")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_luma_expressions.png")
    sheet    = build_sheet(show_guides=False)
    # IMAGE SIZE RULE: <= 1280px in both dimensions
    sheet.thumbnail((1280, 1280), Image.LANCZOS)
    sheet.save(out_path)
    print(f"Saved: {os.path.abspath(out_path)}")
    print(f"Canvas: {sheet.size[0]}x{sheet.size[1]}")
    curves_status = "ACTIVE" if _FACE_CURVES_AVAILABLE else "NOT FOUND — using v011 fallback for all expressions"
    print(f"v013: face curves integration (LTG_TOOL_luma_face_curves v1.1.0): {curves_status}")
    if _FACE_CURVES_AVAILABLE:
        print("  Expressions using draw_luma_face():")
        for sheet_name, curves_name in _FACE_CURVES_EXPR_MAP.items():
            print(f"    {sheet_name!r} -> {curves_name!r}")
        print("  Expressions using v011 fallback (no face curves expression):")
        for expr in EXPRESSIONS:
            if expr not in _FACE_CURVES_EXPR_MAP:
                print(f"    {expr!r}")
    print("v013 Tier-1 silhouette body postures (Alex Chen C41 directive):")
    print("  - RECKLESS: added (replaces DELIGHTED) — wide stance, arms slightly out, energy-outward")
    print("  - ALARMED: added (replaces SURPRISED) — arms raised toward face, recoil geometry")
    print("  - FRUSTRATED: crossed arms unchanged (already correct)")
    print("  - THE NOTICING: gaze fix — pupils now rightward (+LI/RI_CENTER_dx +6)")
    print("    per Lee Tanaka C41 brief: subject at screen-right in P06/SF01 context")
    print("  - Eye geometry: 100px canonical width per luma_face_curve_spec.md v002 (v012)")


if __name__ == "__main__":
    main()
