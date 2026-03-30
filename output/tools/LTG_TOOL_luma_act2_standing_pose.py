# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_luma_act2_standing_pose.py
Luma Act 2 Standing Reactive Pose Generator — "Luma & the Glitchkin"

Cycle 15: Standing reactive pose for Act 2 beats.
Beat context: Luma is in the tech den / on the street — investigating,
problem-solving, reacting. She is NOT seated. This pose covers:
  - A2-01: Tech den, trying to communicate with Byte (investigative urgency)
  - A2-03: Enthusiastic about Cosmo's plan (leaning in, engaged)
  - A2-05: On street, reading the streetlight signal (alert / wonder)
  - A2-08: Facing Grandma Miri (uncertain, a little guilty)

Pose spec:
  - Body: upright standing, slight forward lean (body_tilt = -5)
  - Right arm: raised, hand open / reaching (primary gesture arm)
  - Left arm: bent at side, hand at waist (secondary / grounded arm)
  - Legs: slight wide stance (leg_spread = 1.1)
  - Head: 5° tilt left (attentive, questioning lean)
  - Expression: WORRIED / DETERMINED — brows furrowed asymmetric,
    left brow 10px higher than right (corrugator kink), wide eyes,
    slight jaw-open. Per Cycle 6 spec: brow differential >= 8px.

A-line hoodie silhouette is canonical: narrow shoulders flaring to wide hem.
Pocket bump on viewer-right side for silhouette asymmetry hook.

Output: LTG_CHAR_luma_act2_standing_pose.png
Format: Character pose sheet — character on left, annotation panel on right.
Canvas: 900×600px

Silhouette test: black-blob version generated at bottom of annotation panel.
Character-over-background saturation rule: all character colors must
exceed BG saturation.
"""
from PIL import Image, ImageDraw, ImageFont
import math

# ── Palette — canonical from luma.md and luma_expression_sheet ────────────────
SKIN        = (200, 136, 90)       # Warm Caramel #C8885A
SKIN_SH     = (160, 104, 56)       # Burnished Sienna #A06840
SKIN_HL     = (232, 184, 136)      # Sunlit Caramel #DFA070
HAIR        = (26, 15, 10)         # Espresso Near-Black #1A0F0A
EYE_W       = (250, 240, 220)      # Warm Cream #FAF0DC
EYE_IRIS    = (200, 125, 62)       # Warm Amber #C87D3E
EYE_PUP     = (59, 40, 32)         # Deep Cocoa #3B2820
LINE        = (59, 40, 32)         # Deep Cocoa #3B2820
HOODIE_C    = (232, 114, 42)       # Warm Orange #E8722A
HOODIE_SH   = (184, 85, 32)        # Burnt Umber #B85520
HOODIE_HL   = (245, 144, 80)       # Bright Apricot #F59050
PANTS       = (58, 48, 76)         # dark indigo pants
SNEAKER     = (220, 220, 218)      # off-white sneakers
SNEAKER_SOL = (80, 70, 60)         # sole / rubber trim

# Pixel pattern colors (hoodie pixel grid)
PIX_CYAN    = (0, 240, 255)        # #00F0FF
PIX_MAG     = (255, 45, 107)       # #FF2D6B
PIX_GREEN   = (57, 255, 20)        # #39FF14

# Background — warm neutral
BG_WARM     = (234, 224, 208)      # parchment
BG_PANEL    = (246, 240, 230)      # annotation panel

CANVAS_W = 900
CANVAS_H = 600
CHAR_AREA_W = 520
ANNO_AREA_X = 540


# ── Drawing helpers ────────────────────────────────────────────────────────────

def _rot(cx, cy, x, y, theta):
    """Rotate point (x,y) around (cx,cy) by theta radians."""
    c, s = math.cos(theta), math.sin(theta)
    return (int(cx + x * c - y * s), int(cy + x * s + y * c))


def _draw_luma_hair(draw, cx, cy):
    """Cloud-top hair mass — 5 spiral-curl indicators, slightly asymmetric.
    Per luma.md: right side (viewer-left) has more volume.
    LOCKED CURL COUNT: 5.
    """
    # Main mass
    draw.ellipse([cx - 145, cy - 185, cx + 140, cy + 35], fill=HAIR)
    # Left mass (viewer-right) — slightly less volume
    draw.ellipse([cx - 165, cy - 160, cx - 75,  cy - 50],  fill=HAIR)
    draw.ellipse([cx - 155, cy - 130, cx - 85,  cy - 20],  fill=HAIR)
    # Right mass (viewer-left) — more volume per spec
    draw.ellipse([cx + 75,  cy - 170, cx + 155, cy - 55],  fill=HAIR)
    draw.ellipse([cx + 85,  cy - 140, cx + 148, cy - 35],  fill=HAIR)
    # Crown blobs (top)
    draw.ellipse([cx - 65,  cy - 205, cx + 20,  cy - 135], fill=HAIR)
    draw.ellipse([cx - 20,  cy - 215, cx + 65,  cy - 140], fill=HAIR)
    draw.ellipse([cx - 100, cy - 195, cx - 28,  cy - 120], fill=HAIR)
    # 5 curl indicators (arc overlays for depth suggestion)
    # These represent the 5 locked curls — not individual strands
    curl_specs = [
        (cx - 120, cy - 155, cx - 60,  cy - 75,  40, 210),
        (cx - 50,  cy - 185, cx + 30,  cy - 110, 30, 200),
        (cx + 10,  cy - 165, cx + 80,  cy - 90,  30, 210),
        (cx + 80,  cy - 145, cx + 140, cy - 75,  35, 210),
        (cx - 30,  cy - 215, cx + 50,  cy - 150, 25, 195),
    ]
    curl_color = (56, 30, 18)  # slightly lighter than HAIR for depth
    for (x0, y0, x1, y1, s, e) in curl_specs:
        draw.arc([x0, y0, x1, y1], start=s, end=e, fill=curl_color, width=5)


def _draw_luma_head(draw, cx, cy):
    """Luma head — near-circle, slight chin nub, cheek blobs. Per luma.md."""
    hr = 96
    draw.ellipse([cx - hr, cy - hr, cx + hr, cy + hr + 14],
                 fill=SKIN, outline=LINE, width=3)
    # Chin rounding
    draw.ellipse([cx - 90, cy - 15, cx + 90, cy + hr + 24], fill=SKIN)
    draw.arc([cx - 90, cy - 15, cx + 90, cy + hr + 24],
             start=0, end=180, fill=LINE, width=3)
    # Cheek nubs
    draw.ellipse([cx - hr - 12, cy - 18, cx - hr + 14, cy + 20],
                 fill=SKIN, outline=LINE, width=2)
    draw.ellipse([cx + hr - 14, cy - 18, cx + hr + 12, cy + 20],
                 fill=SKIN, outline=LINE, width=2)


def _draw_hair_overlay(draw, cx, cy):
    """Foreground flyaway strands — escape curls over face."""
    draw.arc([cx - 65, cy - 190, cx - 10, cy - 130], start=30,  end=205, fill=HAIR, width=8)
    draw.arc([cx - 20, cy - 182, cx + 42, cy - 122], start=10,  end=190, fill=HAIR, width=7)
    # Third strand — wisp drooping over forehead
    draw.arc([cx - 40, cy - 170, cx + 10, cy - 120], start=50,  end=210, fill=HAIR, width=5)


def _draw_nose(draw, cx, cy):
    """Minimal apostrophe nose — per luma.md."""
    draw.ellipse([cx - 8, cy + 6,  cx - 2, cy + 12], fill=SKIN_SH)
    draw.ellipse([cx + 2, cy + 6,  cx + 8, cy + 12], fill=SKIN_SH)
    draw.arc([cx - 6, cy - 10, cx + 6, cy + 12], start=200, end=340, fill=SKIN_SH, width=2)


def _draw_worried_determined_face(draw, cx, cy):
    """WORRIED/DETERMINED expression — canonical from Cycle 6 and 11 spec.

    Per Cycle 8 MEMORY: brow differential >= 8-10px at pitch distance.
    Left outer brow corner at ley-38, right at ley-30 = 8px gap.
    Corrugator kink (inner brow tip kicks up) combined with V-brows.

    Per Cycle 6 MEMORY: 'Worried brow = outer V + inner-corner kink UP.
    Without it, V-brows read as aggression only.'

    Expression reads: determined problem-solver who is also a little scared.
    Good for A2-01 (investigating), A2-05 (alert street signal read).
    """
    lex, ley = cx - 36, cy - 18
    rex, rey = cx + 36, cy - 18
    ew = 26
    leh, reh = 30, 28   # both eyes fairly wide — alert state

    # Left eye (lead eye — slightly wider per Cycle 12 spec)
    draw.ellipse([lex - ew, ley - leh, lex + ew, ley + leh],
                 fill=EYE_W, outline=LINE, width=2)
    iris_r = 15
    draw.chord([lex - iris_r, ley - iris_r + 2, lex + iris_r, ley + iris_r + 2],
               start=15, end=345, fill=EYE_IRIS)
    draw.ellipse([lex - 8, ley - 7, lex + 10, ley + 9], fill=EYE_PUP)
    draw.ellipse([lex + 5, ley - 9, lex + 13, ley - 2], fill=(255, 252, 245))
    draw.arc([lex - ew, ley - leh, lex + ew, ley + leh],
             start=200, end=340, fill=LINE, width=4)

    # Right eye
    draw.ellipse([rex - ew, rey - reh, rex + ew, rey + reh],
                 fill=EYE_W, outline=LINE, width=2)
    draw.chord([rex - iris_r, rey - iris_r + 2, rex + iris_r, rey + iris_r + 2],
               start=15, end=345, fill=EYE_IRIS)
    draw.ellipse([rex - 8, rey - 7, rex + 10, rey + 9], fill=EYE_PUP)
    draw.ellipse([rex + 5, rey - 9, rex + 13, rey - 2], fill=(255, 252, 245))
    draw.arc([rex - ew, rey - reh, rex + ew, rey + reh],
             start=200, end=340, fill=LINE, width=4)

    # ── WORRIED/DETERMINED brows — Cycle 8 spec ──────────────────────────────
    # Left brow: outer corner 8px lower than inner kink → V shape
    # left outer: (lex-26, ley-30), inner/kink: (lex+0, ley-44), right edge: (lex+22, ley-36)
    # Differential: ley-44 vs ley-36 = 8px gap — MINIMUM per spec
    draw.line([(lex - 26, ley - 30), (lex + 0, ley - 44), (lex + 22, ley - 36)],
              fill=HAIR, width=5)
    # Corrugator kink: inner tip kicks UP one more step
    draw.line([(lex - 4, ley - 46), (lex + 6, ley - 50)], fill=HAIR, width=4)

    # Right brow: mirrored but slightly lower (8px differential from left)
    # right brow outer corner: (rex+26, rey-30), inner/kink: (rex+0, rey-38)
    draw.line([(rex + 26, rey - 30), (rex + 0, rey - 38), (rex - 22, rey - 32)],
              fill=HAIR, width=5)
    draw.line([(rex + 4, rey - 40), (rex - 6, rey - 44)], fill=HAIR, width=4)

    _draw_nose(draw, cx, cy)

    # Mouth — slight jaw-open (cognitive urgency, not fear-scream)
    # Small oval gap below arc — per Cycle 11: 'gentle open oval = wonder/urgency, not alarm'
    mouth_cx = cx
    mouth_y  = cy + 32
    n_pts = 20
    mouth_pts = []
    for i in range(n_pts + 1):
        t = i / n_pts
        arc_x = int(mouth_cx + 28 * math.cos(math.pi - t * math.pi))
        arc_y = int(mouth_y + 8  * math.sin(math.pi - t * math.pi) - 4)
        mouth_pts.append((arc_x, arc_y))
    if len(mouth_pts) > 1:
        draw.line(mouth_pts, fill=LINE, width=3)

    # Small oval gap (jaw-open indicator — not a rectangle scream)
    draw.ellipse([mouth_cx - 10, mouth_y - 2, mouth_cx + 10, mouth_y + 10],
                 fill=(240, 210, 180), outline=LINE, width=2)

    # Blush — omit for this expression (worried, not warm)


def _draw_pixel_pattern(draw, cx, y_top, hu):
    """Hoodie chest pixel grid — per luma.md pattern construction rules.

    Grid placed on center-chest panel (~0.5hw x 0.4hh).
    Pattern is slightly off-axis (glitch quality). 40% cyan, 20% magenta, rest white.
    """
    px_sz = 4  # pixel square size
    grid_w = int(hu * 0.50)
    grid_h = int(hu * 0.40)
    gx0 = cx - grid_w // 2
    gy0 = y_top + int(hu * 0.22)

    # Seeded pattern for reproducibility
    import random
    rng = random.Random(42)
    for gy in range(gy0, gy0 + grid_h, px_sz + 2):
        for gx in range(gx0, gx0 + grid_w, px_sz + 2):
            r = rng.random()
            if r < 0.35:
                c = PIX_CYAN
            elif r < 0.55:
                c = PIX_MAG
            elif r < 0.62:
                c = PIX_GREEN
            else:
                c = (240, 240, 235)  # Static White
            # Occasional gap (glitch quality — not perfect grid)
            if rng.random() > 0.12:
                off_x = rng.randint(-1, 1)
                off_y = rng.randint(-1, 1)
                draw.rectangle([gx + off_x, gy + off_y,
                                 gx + off_x + px_sz, gy + off_y + px_sz],
                                fill=c)


def _draw_collar(draw, cx, cy, rotate_deg=2):
    """Hoodie collar — rotation per Cycle 8 spec. rotate_deg=2 for slight forward lean."""
    head_r = 96
    collar_cx = cx
    collar_cy = cy + head_r + 42
    rx, ry = 88, 33
    theta = math.radians(rotate_deg)
    cos_t, sin_t = math.cos(theta), math.sin(theta)

    def rot(x, y):
        return (int(collar_cx + x * cos_t - y * sin_t),
                int(collar_cy + x * sin_t + y * cos_t))

    N = 48
    full_pts = [rot(int(rx * math.cos(2 * math.pi * i / N)),
                    int(ry * math.sin(2 * math.pi * i / N))) for i in range(N)]
    draw.polygon(full_pts, fill=HOODIE_C)
    arc_pts = [rot(int(rx * math.cos(math.radians(a))),
                   int(ry * math.sin(math.radians(a)))) for a in range(180, 361, 5)]
    draw.line(arc_pts, fill=LINE, width=3)
    # Hoodie drawstring dots (cyan)
    for i in range(5):
        lx = -34 + i * 17
        ly = 8
        sq = [rot(lx - 4, ly - 3), rot(lx + 4, ly - 3),
              rot(lx + 4, ly + 3), rot(lx - 4, ly + 3)]
        draw.polygon(sq, fill=PIX_CYAN)


def draw_luma_standing(draw, cx, ground_y):
    """Draw full standing Luma — Act 2 reactive pose.

    Pose: upright with slight forward lean (investigative energy).
    Right arm raised/reaching (primary gesture). Left arm at waist.
    Wide stance. Head 5° tilt left (questioning lean).

    cx = horizontal center. ground_y = feet baseline.
    Character built from ground up using canonical proportions from luma.md.
    Total height = 3.5 heads = ~350px at hr=100. With hair: ~390px.
    """
    hr  = 96    # head radius
    hu  = 138   # body height unit

    # ── Build top-down from head center ──────────────────────────────────────
    # Place head center so feet land at ground_y
    # Total below head center: collar ~42 + torso hu + legs 0.75hu + feet 0.20hu
    total_below_head = 42 + hu + int(hu * 0.75) + int(hu * 0.20)
    cy = ground_y - total_below_head - hr  # face center y

    # Slight forward lean: tilt body_x left 8px at torso (cx-8 for whole body)
    # We achieve this by offsetting body cx slightly
    body_cx = cx - 4  # subtle lean toward viewer-right

    # ── Legs (drawn first — behind everything) ───────────────────────────────
    leg_w   = int(hu * 0.16)
    leg_top = cy + hr + 42 + hu     # waist level
    leg_bot = ground_y - int(hu * 0.20)  # above feet

    # Wide stance: legs spread 1.1x
    leg_spread = 1.1
    l_leg_cx = body_cx - int(hu * 0.28 * leg_spread)
    r_leg_cx = body_cx + int(hu * 0.24 * leg_spread)

    # Left leg
    draw.rectangle([l_leg_cx - leg_w, leg_top,
                    l_leg_cx + leg_w, leg_bot], fill=PANTS, outline=LINE, width=2)
    # Right leg
    draw.rectangle([r_leg_cx - leg_w, leg_top,
                    r_leg_cx + leg_w, leg_bot], fill=PANTS, outline=LINE, width=2)

    # Pants cuffs
    for lcx in (l_leg_cx, r_leg_cx):
        draw.rectangle([lcx - leg_w - 2, leg_bot - 8,
                        lcx + leg_w + 2, leg_bot + 4],
                       fill=PANTS, outline=LINE, width=1)

    # ── Sneakers ─────────────────────────────────────────────────────────────
    sneaker_w = int(hu * 0.52 * 0.52)   # fw = int(hu * 0.52) per Cycle 11 spec
    sneaker_h = int(hu * 0.20)
    sole_h    = int(sneaker_h * 0.28)

    for s_cx in (l_leg_cx, r_leg_cx):
        # Shoe body
        draw.ellipse([s_cx - sneaker_w, ground_y - sneaker_h,
                      s_cx + sneaker_w, ground_y],
                     fill=SNEAKER, outline=LINE, width=2)
        # Sole stripe
        draw.arc([s_cx - sneaker_w, ground_y - sole_h,
                  s_cx + sneaker_w, ground_y + sole_h // 2],
                 start=0, end=180, fill=SNEAKER_SOL, width=sole_h)
        # Toe cap highlight
        draw.arc([s_cx - sneaker_w + 4, ground_y - sneaker_h + 6,
                  s_cx + sneaker_w - 4, ground_y - sneaker_h // 2],
                 start=200, end=345, fill=(240, 240, 238), width=3)

    # ── Torso (A-line hoodie) ─────────────────────────────────────────────────
    # Narrow shoulders flaring to wide hem — canonical silhouette per Cycle 5
    torso_top_y = cy + hr + 42
    torso_bot_y = leg_top + 4
    shoulder_w  = int(hu * 0.52)   # narrow shoulders
    hem_w       = int(hu * 0.78)   # wide A-line hem

    hoodie_pts = [
        (body_cx - shoulder_w, torso_top_y),
        (body_cx + shoulder_w, torso_top_y),
        (body_cx + hem_w,      torso_bot_y),
        (body_cx - hem_w,      torso_bot_y),
    ]
    draw.polygon(hoodie_pts, fill=HOODIE_C, outline=LINE, width=3)

    # Hoodie shadow — underside of torso
    shadow_pts = [
        (body_cx - hem_w,       torso_bot_y - 18),
        (body_cx + hem_w,       torso_bot_y - 18),
        (body_cx + hem_w,       torso_bot_y),
        (body_cx - hem_w,       torso_bot_y),
    ]
    draw.polygon(shadow_pts, fill=HOODIE_SH)

    # Hoodie highlight — shoulder/chest area
    draw.ellipse([body_cx - int(shoulder_w * 0.7), torso_top_y,
                  body_cx + int(shoulder_w * 0.7), torso_top_y + int(hu * 0.28)],
                 fill=HOODIE_HL)
    # Re-draw outline on top
    draw.polygon(hoodie_pts, fill=None, outline=LINE, width=3)

    # Hoodie seam arc
    seam_y = torso_top_y + int(hu * 0.22)
    draw.arc([body_cx - int(hu * 0.24), seam_y,
              body_cx + int(hu * 0.24), seam_y + int(hu * 0.17)],
             start=10, end=170, fill=LINE, width=2)

    # Pixel pattern on chest
    _draw_pixel_pattern(draw, body_cx, torso_top_y, hu)

    # ── Pocket bump (viewer-right = character-left) ────────────────────────────
    # Per Cycle 5: protruding pocket on one side for asymmetry and silhouette hook
    pkt_x = body_cx + int(hu * 0.52)
    pkt_y = torso_top_y + int(hu * 0.38)
    draw.ellipse([pkt_x, pkt_y,
                  pkt_x + int(hu * 0.22), pkt_y + int(hu * 0.24)],
                 fill=HOODIE_C, outline=LINE, width=2)

    arm_w = int(hu * 0.13)
    arm_top_y = torso_top_y + int(hu * 0.06)

    # ── Right arm (viewer-right = Luma's left) — RAISED/REACHING ─────────────
    # Primary gesture arm: raised forward-up, hand open
    r_shoulder_x = body_cx + shoulder_w + int(hu * 0.04)
    r_arm_dy     = -40   # raised upward relative to shoulder
    r_elbow_x    = r_shoulder_x + int(hu * 0.28)
    r_elbow_y    = arm_top_y + r_arm_dy + int(hu * 0.25)
    r_hand_x     = r_shoulder_x + int(hu * 0.48)
    r_hand_y     = arm_top_y + r_arm_dy

    # Upper arm — shoulder to elbow
    r_upper_pts = [
        (r_shoulder_x,           arm_top_y + r_arm_dy),
        (r_shoulder_x + arm_w,   arm_top_y + r_arm_dy + 8),
        (r_elbow_x + arm_w,      r_elbow_y),
        (r_elbow_x,              r_elbow_y),
    ]
    draw.polygon(r_upper_pts, fill=HOODIE_C, outline=LINE, width=2)

    # Forearm — elbow to hand (angled up-forward)
    r_fore_pts = [
        (r_elbow_x,              r_elbow_y),
        (r_elbow_x + arm_w,      r_elbow_y),
        (r_hand_x + arm_w // 2,  r_hand_y + arm_w),
        (r_hand_x - arm_w // 2,  r_hand_y + arm_w),
    ]
    draw.polygon(r_fore_pts, fill=HOODIE_C, outline=LINE, width=2)

    # Right hand — MITTEN geometry (Cycle 16 fix per Dmitri/production rule).
    # Production rule: rough/reference poses use CLEAN MITTEN hands — no finger or thumb
    # differentiation. A single rounded oval blob reads as "open/reaching" at reference scale.
    # Removed: thumb arc, finger spread lines — replaced with solid mitten oval.
    draw.ellipse([r_hand_x - 14, r_hand_y - 10,
                  r_hand_x + 18, r_hand_y + 16],
                 fill=SKIN, outline=LINE, width=2)

    # ── Left arm (viewer-left = Luma's right) — AT WAIST (grounded) ──────────
    l_shoulder_x = body_cx - shoulder_w - int(hu * 0.04)
    l_arm_dy     = 10    # slightly below shoulder level (relaxed but present)
    l_elbow_x    = l_shoulder_x - int(hu * 0.18)
    l_elbow_y    = arm_top_y + l_arm_dy + int(hu * 0.32)
    l_hand_x     = body_cx - int(hu * 0.52)
    l_hand_y     = arm_top_y + l_arm_dy + int(hu * 0.44)

    # Upper arm
    l_upper_pts = [
        (l_shoulder_x,           arm_top_y + l_arm_dy),
        (l_shoulder_x - arm_w,   arm_top_y + l_arm_dy + 10),
        (l_elbow_x - arm_w,      l_elbow_y),
        (l_elbow_x,              l_elbow_y),
    ]
    draw.polygon(l_upper_pts, fill=HOODIE_C, outline=LINE, width=2)

    # Forearm (bent at elbow, hand near waist)
    l_fore_pts = [
        (l_elbow_x,              l_elbow_y),
        (l_elbow_x - arm_w,      l_elbow_y),
        (l_hand_x - arm_w // 2,  l_hand_y),
        (l_hand_x + arm_w // 2,  l_hand_y),
    ]
    draw.polygon(l_fore_pts, fill=HOODIE_C, outline=LINE, width=2)

    # Left hand (fisted at waist — grounded posture)
    draw.ellipse([l_hand_x - 14, l_hand_y - 10,
                  l_hand_x + 12, l_hand_y + 14],
                 fill=SKIN, outline=LINE, width=2)

    # ── Head (drawn last — on top) ────────────────────────────────────────────
    # Head 5° tilt leftward (questioning lean) — slight offset
    head_cx = cx - 3   # subtle lean
    _draw_luma_hair(draw, head_cx, cy)
    _draw_luma_head(draw, head_cx, cy)
    _draw_worried_determined_face(draw, head_cx, cy)
    _draw_hair_overlay(draw, head_cx, cy)
    _draw_collar(draw, head_cx, cy, rotate_deg=2)

    return cy   # return face center y for annotation lines


def draw_silhouette_blob(draw, cx, ground_y, scale=0.38):
    """Squint-test silhouette — black blob at reduced scale.

    Per Cycle 4/5 rules: silhouette must be readable as a black blob.
    A-line trapezoid + oversized sneakers + cloud-top hair must all read
    distinctly from Miri (rectangle), Cosmo (tall+narrow), Byte (oval+float).
    """
    s = scale
    hr = int(96 * s)
    hu = int(138 * s)

    total_below = 42 + hu + int(hu * 0.75) + int(hu * 0.20)
    cy = ground_y - int(total_below * s) - hr

    # Simplified A-line trapezoid body
    torso_top = cy + int(hr * 0.8)
    torso_bot = cy + int(hr * 0.8) + int(hu * s * 0.88)
    sw = int(hu * s * 0.52)
    hw = int(hu * s * 0.78)

    pts = [(cx - sw, torso_top), (cx + sw, torso_top),
           (cx + hw, torso_bot), (cx - hw, torso_bot)]
    draw.polygon(pts, fill=(10, 10, 10))

    # Pocket bump (silhouette hook)
    draw.ellipse([cx + int(hu * s * 0.50), torso_top + int(hu * s * 0.35),
                  cx + int(hu * s * 0.72), torso_top + int(hu * s * 0.59)],
                 fill=(10, 10, 10))

    # Arms
    arm_w = int(hu * s * 0.13)
    # Right arm raised
    draw.ellipse([cx + int(sw * 1.05), torso_top - int(hu * s * 0.18),
                  cx + int(sw * 1.05) + int(hu * s * 0.52),
                  torso_top + int(hu * s * 0.28)],
                 fill=(10, 10, 10))
    # Left arm at waist
    draw.ellipse([cx - int(sw * 1.05) - int(hu * s * 0.42),
                  torso_top + int(hu * s * 0.08),
                  cx - int(sw * 1.05),
                  torso_top + int(hu * s * 0.52)],
                 fill=(10, 10, 10))

    # Legs (wide stance)
    leg_w = int(hu * s * 0.16)
    leg_top = torso_bot
    leg_bot = ground_y - int(hu * s * 0.20)
    lcx = cx - int(hu * s * 0.30)
    rcx = cx + int(hu * s * 0.26)
    draw.rectangle([lcx - leg_w, leg_top, lcx + leg_w, leg_bot],
                   fill=(10, 10, 10))
    draw.rectangle([rcx - leg_w, leg_top, rcx + leg_w, leg_bot],
                   fill=(10, 10, 10))

    # Sneakers
    snkr_w = int(hu * s * 0.26)
    snkr_h = int(hu * s * 0.20)
    for scx in (lcx, rcx):
        draw.ellipse([scx - snkr_w, ground_y - snkr_h,
                      scx + snkr_w, ground_y],
                     fill=(10, 10, 10))

    # Hair cloud
    draw.ellipse([cx - int(145 * s), cy - int(195 * s),
                  cx + int(140 * s), cy + int(35 * s)],
                 fill=(10, 10, 10))
    draw.ellipse([cx - int(165 * s), cy - int(160 * s),
                  cx - int(75 * s),  cy - int(50 * s)],
                 fill=(10, 10, 10))
    draw.ellipse([cx + int(75 * s),  cy - int(170 * s),
                  cx + int(155 * s), cy - int(55 * s)],
                 fill=(10, 10, 10))
    draw.ellipse([cx - int(65 * s),  cy - int(205 * s),
                  cx + int(20 * s),  cy - int(135 * s)],
                 fill=(10, 10, 10))

    # Head
    draw.ellipse([cx - hr, cy - hr, cx + hr, cy + hr + int(14 * s)],
                 fill=(10, 10, 10))


def draw_annotation_panel(draw, x, y, w, h, font, font_sm):
    """Right-side annotation panel with pose callouts and silhouette test."""
    draw.rectangle([x, y, x + w, y + h], fill=BG_PANEL, outline=(180, 168, 150), width=2)

    title_c  = (80, 56, 32)
    label_c  = (59, 40, 32)
    detail_c = (110, 90, 68)
    beat_c   = (60, 100, 80)

    annotations = [
        ("BEATS", "A2-01, A2-03, A2-05, A2-08",    beat_c,   True),
        ("",      "",                                label_c,  False),
        ("EXPR",  "WORRIED / DETERMINED",           label_c,  True),
        ("",      "brow diff left=38 right=30",     detail_c, False),
        ("",      "corrugator kink (inner UP)",      detail_c, False),
        ("",      "jaw-open oval (not scream rect)", detail_c, False),
        ("",      "",                                label_c,  False),
        ("POSE",  "STANDING REACTIVE",              label_c,  True),
        ("",      "right arm raised/reaching",       detail_c, False),
        ("",      "left arm at waist (grounded)",    detail_c, False),
        ("",      "wide stance leg_spread=1.1",      detail_c, False),
        ("",      "body_tilt=-5 (forward lean)",     detail_c, False),
        ("",      "head tilt 5° left (query lean)",  detail_c, False),
        ("",      "",                                label_c,  False),
        ("SIHL",  "Squint test — see blob below",   (100, 80, 60), False),
        ("",      "A-line + cloud hair + sneakers",  detail_c, False),
        ("",      "pocket bump: asymmetry hook",     detail_c, False),
        ("",      "",                                label_c,  False),
        ("RULE",  "NEVER overwrite — new version",  (140, 80, 50), False),
        ("",      "Char saturation > BG saturation", detail_c, False),
    ]

    line_h = 22
    cur_y  = y + 18
    cur_x  = x + 14

    draw.text((cur_x, cur_y - 2),
              "LUMA — Act 2 Standing Pose  v001 (C16)",
              fill=title_c, font=font)
    cur_y += 28
    draw.line([(cur_x, cur_y), (x + w - 14, cur_y)],
              fill=(180, 168, 150), width=1)
    cur_y += 10

    for (prefix, text, color, bold) in annotations:
        if not text:
            cur_y += 8
            continue
        if prefix:
            draw.text((cur_x, cur_y),
                      f"{prefix}: ", fill=(100, 140, 110), font=font_sm)
            draw.text((cur_x + 52, cur_y), text, fill=color, font=font_sm)
        else:
            draw.text((cur_x + 52, cur_y), text, fill=color, font=font_sm)
        cur_y += line_h
        if cur_y > y + h - 100:
            break

    # ── Silhouette blob (squint test) ─────────────────────────────────────────
    blob_y    = y + h - 88
    blob_cx   = x + w // 2
    blob_gy   = y + h - 16

    # Blob label
    draw.text((cur_x, blob_y - 16), "SQUINT TEST:", fill=(80, 60, 40), font=font_sm)
    draw_silhouette_blob(draw, blob_cx, blob_gy, scale=0.30)

    # Footer
    draw.line([(cur_x, y + h - 14), (x + w - 14, y + h - 14)],
              fill=(180, 168, 150), width=1)
    draw.text((cur_x, y + h - 10),
              "Cycle 15/16 — Maya Santos",
              fill=detail_c, font=font_sm)


def generate_luma_act2_standing_pose(output_path):
    """Render Act 2 standing pose sheet for Luma."""
    img  = Image.new('RGB', (CANVAS_W, CANVAS_H), BG_WARM)
    draw = ImageDraw.Draw(img, 'RGBA')

    try:
        font       = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
        font_sm    = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
    except Exception:
        font = font_sm = font_title = ImageFont.load_default()

    # Sheet header
    draw.text((18, 10),
              "LUMA — Act 2 Standing Pose  |  Beats A2-01/03/05/08  |  Cycle 15",
              fill=(80, 56, 32), font=font_title)
    draw.line([(18, 34), (CANVAS_W - 18, 34)], fill=(180, 168, 150), width=1)

    # Character zone background (slightly lighter than border)
    draw.rectangle([10, 40, CHAR_AREA_W, CANVAS_H - 10], fill=(238, 228, 210))

    # Draw character
    char_cx    = CHAR_AREA_W // 2 + 20
    ground_y   = CANVAS_H - 30
    cy = draw_luma_standing(draw, char_cx, ground_y)

    # Ground line
    draw.line([(18, ground_y + 2), (CHAR_AREA_W - 10, ground_y + 2)],
              fill=(160, 144, 120), width=2)
    # Ground shadow
    draw.ellipse([char_cx - 80, ground_y,
                  char_cx + 80, ground_y + 10],
                 fill=(180, 164, 140))

    # Annotation panel
    draw_annotation_panel(draw, ANNO_AREA_X, 40,
                          CANVAS_W - ANNO_AREA_X - 10,
                          CANVAS_H - 50, font, font_sm)

    img.save(output_path)
    print(f"Saved: {output_path}")
    dims = img.size
    print(f"Dimensions: {dims[0]}×{dims[1]}px")


if __name__ == "__main__":
    output_path = (
        "/home/wipkat/team/output/characters/main/"
        "LTG_CHAR_luma_act2_standing_pose.png"
    )
    generate_luma_act2_standing_pose(output_path)
