# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
Luma Expression Sheet Generator — "Luma & the Glitchkin"
Cycle 11: 6-expression 3x2 grid, full-body character panels with annotated
prev/next state context, matching Byte expression sheet structure.

Expressions:
  1. Reckless Excitement   — signature grin (from luma_face_generator.py)
  2. Worried/Determined    — inner brow kink, tense
  3. Mischievous Plotting  — tilted smirk
  4. Settling/Wonder       — wide eyes, soft open mouth (from chaos generator P17)
  5. Recognition           — asymmetric brow raise, concentration (from chaos P18)
  6. Warmth                — happiness-narrowed eyes, cheek crinkle (from chaos P20)

Panel design mirrors byte_expressions_generator.py:
  - 3 cols × 2 rows, PANEL_W × PANEL_H per cell
  - Dark label bar at bottom: name, prev_state, next_state
  - Distinct panel background color per expression
  - Full body (hoodie + legs + sneakers) drawn beneath face
"""
from PIL import Image, ImageDraw, ImageFont
import math

# ── Palette — matches luma_face_generator.py ─────────────────────────────────
SKIN       = (200, 136, 90)
SKIN_SH    = (168, 104, 56)
SKIN_HL    = (232, 184, 136)
HAIR       = (26, 15, 10)
EYE_W      = (255, 252, 245)
EYE_PUP    = (20, 12, 8)
EYE_IRIS   = (60, 38, 20)
BLUSH      = (220, 100, 60, 140)
LINE       = (59, 40, 32)

HOODIE_O   = (232, 114, 42)    # orange — Excitement
HOODIE_W   = (52,  38,  24)    # dark — Worried
HOODIE_M   = (180, 60, 120)    # magenta-purple — Mischief
HOODIE_S   = (88, 130, 175)    # steel blue — Settling/Wonder
HOODIE_R   = (60,  95, 145)    # deep blue — Recognition
HOODIE_WA  = (198, 140,  70)   # warm gold — Warmth

# Panel backgrounds — each must be immediately distinct at pitch/print distance
BG_EXCITE  = (240, 200, 150)   # warm amber (canonical Cycle 9)
BG_WORRY   = (195, 212, 228)   # cool blue-grey
BG_MISCH   = (220, 205, 242)   # warm lavender
BG_SETTLE  = (180, 215, 205)   # soft teal-mint
BG_RECOG   = (165, 185, 220)   # medium periwinkle
BG_WARMTH  = (250, 215, 170)   # soft warm peach

CANVAS_BG  = (30, 22, 16)

# ── Layout ────────────────────────────────────────────────────────────────────
PANEL_W = 280
PANEL_H = 390
COLS    = 3
ROWS    = 2
PAD     = 18
HEADER  = 52


# ── Hair helpers (from luma_face_generator.py) ────────────────────────────────
def _draw_hair_mass(draw, cx, cy):
    draw.ellipse([cx-155, cy-195, cx+145, cy+40],  fill=HAIR)
    draw.ellipse([cx-175, cy-170, cx-80,  cy-60],   fill=HAIR)
    draw.ellipse([cx-165, cy-140, cx-95,  cy-30],   fill=HAIR)
    draw.ellipse([cx+80,  cy-160, cx+155, cy-60],   fill=HAIR)
    draw.ellipse([cx+90,  cy-130, cx+145, cy-40],   fill=HAIR)
    draw.ellipse([cx-60,  cy-215, cx+20,  cy-140],  fill=HAIR)
    draw.ellipse([cx-20,  cy-225, cx+70,  cy-145],  fill=HAIR)
    draw.ellipse([cx-100, cy-200, cx-30,  cy-130],  fill=HAIR)


def _draw_head(draw, cx, cy):
    head_r = 100
    draw.ellipse([cx-head_r, cy-head_r, cx+head_r, cy+head_r+15],
                 fill=SKIN, outline=LINE, width=3)
    draw.ellipse([cx-95, cy-20, cx+95, cy+head_r+25], fill=SKIN)
    draw.arc([cx-95, cy-20, cx+95, cy+head_r+25], start=0, end=180, fill=LINE, width=3)
    draw.ellipse([cx-head_r-12, cy-20, cx-head_r+14, cy+20],
                 fill=SKIN, outline=LINE, width=2)
    draw.ellipse([cx+head_r-14, cy-20, cx+head_r+12, cy+20],
                 fill=SKIN, outline=LINE, width=2)


def _draw_nose(draw, cx, cy):
    draw.ellipse([cx-8, cy+8,  cx-2, cy+14], fill=SKIN_SH)
    draw.ellipse([cx+2, cy+8,  cx+8, cy+14], fill=SKIN_SH)
    draw.arc([cx-6, cy-10, cx+6, cy+12], start=200, end=340, fill=SKIN_SH, width=2)


def _draw_hair_overlay(draw, cx, cy):
    draw.arc([cx-60, cy-195, cx-10, cy-140], start=30,  end=200, fill=HAIR, width=8)
    draw.arc([cx-20, cy-190, cx+40, cy-130], start=10,  end=190, fill=HAIR, width=7)


def _draw_collar(draw, cx, cy, head_r, color=HOODIE_O, rotate_deg=0):
    """Rotated collar ellipse — matches luma_face_generator.py logic exactly."""
    collar_cx = cx
    collar_cy = cy + head_r + 45
    rx, ry = 90, 35
    theta = math.radians(rotate_deg)
    cos_t, sin_t = math.cos(theta), math.sin(theta)

    def rot(x, y):
        return (int(collar_cx + x*cos_t - y*sin_t),
                int(collar_cy + x*sin_t + y*cos_t))

    N = 48
    full_pts = [rot(int(rx*math.cos(2*math.pi*i/N)),
                    int(ry*math.sin(2*math.pi*i/N))) for i in range(N)]
    draw.polygon(full_pts, fill=color)
    arc_pts = [rot(int(rx*math.cos(math.radians(a))),
                   int(ry*math.sin(math.radians(a)))) for a in range(180, 361, 5)]
    draw.line(arc_pts, fill=LINE, width=3)
    for i in range(5):
        local_x = -35 + i*17
        local_y = 8
        sq = [rot(local_x-5, local_y-4), rot(local_x+5, local_y-4),
              rot(local_x+5, local_y+4), rot(local_x-5, local_y+4)]
        draw.polygon(sq, fill=(0, 240, 255))


def _draw_body(draw, cx, body_top_y, hoodie_color, arm_l_dy=0, arm_r_dy=0,
               body_tilt=0, body_squash=1.0):
    """Draw Luma's A-line hoodie body, arms, legs, and sneakers.

    A-line trapezoid: narrow at shoulders, wider at hem — canonical Cycle 5 silhouette fix.
    Sneaker width: hu*0.52 (Cycle 11 canonical, matches front-view proportion).
    """
    hu = 140   # body height unit (scales all body proportions)

    # Hoodie trapezoid (A-line) — top narrow, bottom wide
    shoulder_w = int(hu * 0.52)
    hem_w      = int(hu * 0.70)
    hem_y      = body_top_y + int(hu * 0.85)
    tilt_off   = int(body_tilt * 0.5)   # lean offset (small, not full tilt)

    hoodie_pts = [
        (cx - shoulder_w + tilt_off, body_top_y),
        (cx + shoulder_w + tilt_off, body_top_y),
        (cx + hem_w,                 hem_y),
        (cx - hem_w,                 hem_y),
    ]
    draw.polygon(hoodie_pts, fill=hoodie_color, outline=LINE, width=3)

    # Pocket bump — left side (asymmetric silhouette hook, Cycle 5)
    pocket_x  = cx - hem_w + int(hu * 0.06)
    pocket_y  = body_top_y + int(hu * 0.42)
    pocket_w  = int(hu * 0.22)
    pocket_h  = int(hu * 0.28)
    draw.ellipse([pocket_x, pocket_y,
                  pocket_x + pocket_w, pocket_y + pocket_h],
                 fill=hoodie_color, outline=LINE, width=2)

    # Center pocket seam line
    seam_y = body_top_y + int(hu * 0.38)
    draw.arc([cx - int(hu*0.25), seam_y,
              cx + int(hu*0.25), seam_y + int(hu*0.18)],
             start=10, end=170, fill=LINE, width=2)

    # Arms (rectangles hanging from shoulder level)
    lw    = int(hu * 0.13)
    lh    = int(hu * 0.45)
    arm_y = body_top_y + int(hu * 0.10)

    # Left arm
    lax1 = cx - shoulder_w + tilt_off - int(hu * 0.05)
    lay1 = arm_y + arm_l_dy
    draw.rectangle([lax1 - lw, lay1, lax1, lay1 + lh],
                   fill=hoodie_color, outline=LINE, width=2)
    # Left hand blob
    draw.ellipse([lax1 - lw - 8, lay1 + lh - 4,
                  lax1 + 4,      lay1 + lh + 20],
                 fill=SKIN, outline=LINE, width=2)

    # Right arm
    rax1 = cx + shoulder_w + tilt_off + int(hu * 0.05)
    ray1 = arm_y + arm_r_dy
    draw.rectangle([rax1, ray1, rax1 + lw, ray1 + lh],
                   fill=hoodie_color, outline=LINE, width=2)
    # Right hand blob
    draw.ellipse([rax1 - 4,      ray1 + lh - 4,
                  rax1 + lw + 8, ray1 + lh + 20],
                 fill=SKIN, outline=LINE, width=2)

    # Legs — two rectangles below hem
    leg_w  = int(hu * 0.18)
    leg_h  = int(hu * 0.45)
    leg_l  = cx - int(hem_w * 0.38)
    leg_r  = cx + int(hem_w * 0.38)
    leg_y  = hem_y

    draw.rectangle([leg_l - leg_w, leg_y, leg_l + leg_w, leg_y + leg_h],
                   fill=(60, 50, 80), outline=LINE, width=2)
    draw.rectangle([leg_r - leg_w, leg_y, leg_r + leg_w, leg_y + leg_h],
                   fill=(60, 50, 80), outline=LINE, width=2)

    # Oversized sneakers — fw=0.52*hu (canonical, Cycle 11 normalized)
    fw    = int(hu * 0.52)
    fh    = int(hu * 0.28)
    sn_y  = leg_y + leg_h
    base_y = sn_y + fh

    # Left sneaker
    draw.ellipse([leg_l - leg_w - fw + int(fw*0.3), sn_y,
                  leg_l - leg_w + int(fw*0.5),      base_y],
                 fill=(220, 220, 220), outline=LINE, width=2)
    # Sneaker toe cap detail
    draw.arc([leg_l - leg_w - fw + int(fw*0.3) + 4, sn_y + 4,
              leg_l - leg_w + int(fw*0.5) - 4,      base_y - 4],
             start=200, end=340, fill=(180, 180, 180), width=2)

    # Right sneaker
    draw.ellipse([leg_r + leg_w - int(fw*0.5),      sn_y,
                  leg_r + leg_w + fw - int(fw*0.3), base_y],
                 fill=(220, 220, 220), outline=LINE, width=2)
    draw.arc([leg_r + leg_w - int(fw*0.5) + 4, sn_y + 4,
              leg_r + leg_w + fw - int(fw*0.3) - 4, base_y - 4],
             start=200, end=340, fill=(180, 180, 180), width=2)


# ── Expression face draw functions ────────────────────────────────────────────

def draw_reckless_excitement(draw, cx, cy):
    """Signature grin — broken symmetry, from luma_face_generator.py."""
    head_r = 100
    _draw_hair_mass(draw, cx, cy)
    _draw_head(draw, cx, cy)

    lex, ley = cx-38, cy-18
    rex, rey = cx+38, cy-18
    ew = 28
    leh, reh = 30, 26

    draw.ellipse([lex-ew, ley-leh, lex+ew, ley+leh], fill=EYE_W, outline=LINE, width=2)
    iris_r = 15
    draw.chord([lex-iris_r, ley-iris_r+2, lex+iris_r, ley+iris_r+2], start=15, end=345, fill=EYE_IRIS)
    draw.ellipse([lex-9, ley-7, lex+9, ley+9], fill=EYE_PUP)
    draw.ellipse([lex+6, ley-9, lex+13, ley-2], fill=(255,252,245))
    draw.arc([lex-ew, ley-leh, lex+ew, ley+leh], start=200, end=340, fill=LINE, width=4)

    draw.ellipse([rex-ew, rey-reh, rex+ew, rey+reh], fill=EYE_W, outline=LINE, width=2)
    draw.chord([rex-iris_r, rey-iris_r+2, rex+iris_r, rey+iris_r+2], start=15, end=345, fill=EYE_IRIS)
    ps = 5
    draw.ellipse([rex-9+ps, rey-7, rex+9+ps, rey+9], fill=EYE_PUP)
    draw.ellipse([rex+6+ps, rey-9, rex+13+ps, rey-2], fill=(255,252,245))
    draw.arc([rex-ew, rey-reh, rex+ew, rey+reh], start=200, end=340, fill=LINE, width=4)
    draw.ellipse([lex-9+ps, ley-7, lex+9+ps, ley+9], fill=EYE_PUP)

    l_brow = [(lex-30, ley-42), (lex-5, ley-52), (lex+22, ley-39)]
    draw.line(l_brow, fill=HAIR, width=5)
    r_brow = [(rex-22, rey-34), (rex-5, rey-40), (rex+28, rey-32)]
    draw.line(r_brow, fill=HAIR, width=5)

    _draw_nose(draw, cx, cy)
    m_off = -6
    draw.arc([cx-45+m_off, cy+18, cx+45+m_off, cy+70], start=5, end=175, fill=LINE, width=4)
    draw.arc([cx-44+m_off, cy+20, cx+44+m_off, cy+50], start=5, end=175, fill=LINE, width=3)
    draw.chord([cx-42+m_off, cy+22, cx+42+m_off, cy+65], start=7, end=173, fill=(250,246,238))
    draw.arc([cx-42+m_off, cy+22, cx+42+m_off, cy+65], start=7, end=173, fill=LINE, width=2)
    draw.arc([cx-20+m_off, cy+62, cx+26+m_off, cy+76], start=5, end=175, fill=SKIN_SH, width=2)
    draw.arc([cx-50, cy+25, cx-30, cy+45], start=320, end=60, fill=SKIN_SH, width=2)
    draw.ellipse([cx-head_r+8,  cy+5, cx-head_r+58, cy+38], fill=(220, 80, 50, 110))
    draw.ellipse([cx+head_r-58, cy+5, cx+head_r-8,  cy+38], fill=(220, 80, 50, 90))

    _draw_hair_overlay(draw, cx, cy)
    _draw_collar(draw, cx, cy, head_r, color=HOODIE_O, rotate_deg=8)


def draw_worried_determined(draw, cx, cy):
    """Inner brow kink, tense. From luma_face_generator.py."""
    head_r = 100
    _draw_hair_mass(draw, cx, cy)
    _draw_head(draw, cx, cy)

    lex, ley = cx-38, cy-20
    rex, rey = cx+38, cy-20
    ew, eh = 28, 22

    draw.ellipse([lex-ew, ley-eh, lex+ew, ley+eh], fill=EYE_W, outline=LINE, width=2)
    draw.ellipse([lex-13, ley-13, lex+13, ley+13], fill=EYE_IRIS)
    draw.ellipse([lex-8, ley-8, lex+8, ley+8], fill=EYE_PUP)
    draw.ellipse([lex+3, ley-8, lex+9, ley-2], fill=(255,252,245))
    draw.arc([lex-ew, ley-eh, lex+ew, ley+eh], start=195, end=345, fill=LINE, width=5)

    draw.ellipse([rex-ew, rey-eh, rex+ew, rey+eh], fill=EYE_W, outline=LINE, width=2)
    draw.ellipse([rex-13, rey-13, rex+13, rey+13], fill=EYE_IRIS)
    draw.ellipse([rex-8, rey-8, rex+8, rey+8], fill=EYE_PUP)
    draw.ellipse([rex+3, rey-8, rex+9, rey-2], fill=(255,252,245))
    draw.arc([rex-ew, rey-eh, rex+ew, rey+eh], start=195, end=345, fill=LINE, width=5)

    # Worried/determined brow pair — 8px outer height differential + corrugator kink
    l_brow = [(lex-28, ley-38), (lex+5, ley-26), (lex+20, ley-20), (lex+26, ley-28)]
    draw.line(l_brow, fill=HAIR, width=6)
    r_brow = [(rex+28, rey-30), (rex-5, rey-24), (rex-20, rey-20), (rex-26, rey-28)]
    draw.line(r_brow, fill=HAIR, width=6)

    _draw_nose(draw, cx, cy)
    draw.line([(cx-32, cy+38), (cx+32, cy+38)], fill=LINE, width=3)
    draw.line([(cx-32, cy+38), (cx-38, cy+44)], fill=LINE, width=3)
    draw.line([(cx+32, cy+38), (cx+38, cy+44)], fill=LINE, width=3)
    draw.ellipse([cx-head_r+12, cy+10, cx-head_r+52, cy+36], fill=(200,80,50,55))
    draw.ellipse([cx+head_r-52, cy+10, cx+head_r-12, cy+36], fill=(200,80,50,55))

    _draw_hair_overlay(draw, cx, cy)
    _draw_collar(draw, cx, cy, head_r, color=HOODIE_W, rotate_deg=2)


def draw_mischievous_plotting(draw, cx, cy):
    """Tilted smirk, sky-high brow. From luma_face_generator.py."""
    head_r = 100
    _draw_hair_mass(draw, cx, cy)
    _draw_head(draw, cx, cy)

    lex, ley = cx-38, cy-18
    rex, rey = cx+38, cy-18
    ew = 28

    leh_top = 14
    draw.ellipse([lex-ew, ley-leh_top, lex+ew, ley+leh_top+6], fill=EYE_W, outline=LINE, width=2)
    draw.ellipse([lex-13, ley-12, lex+13, ley+12], fill=EYE_IRIS)
    draw.ellipse([lex-8, ley-8, lex+8, ley+8], fill=EYE_PUP)
    draw.ellipse([lex+3, ley-7, lex+9, ley-1], fill=(255,252,245))
    draw.arc([lex-ew, ley-leh_top, lex+ew, ley+leh_top+6], start=195, end=345, fill=LINE, width=6)

    reh = 28
    draw.ellipse([rex-ew, rey-reh, rex+ew, rey+reh], fill=EYE_W, outline=LINE, width=2)
    draw.ellipse([rex-13, rey-13, rex+13, rey+13], fill=EYE_IRIS)
    draw.ellipse([rex-8, rey-8, rex+8, rey+8], fill=EYE_PUP)
    draw.ellipse([rex+3, rey-10, rex+9, rey-3], fill=(255,252,245))
    draw.arc([rex-ew, rey-reh, rex+ew, rey+reh], start=200, end=340, fill=LINE, width=4)

    l_brow = [(lex-30, ley-46), (lex-5, ley-58), (lex+24, ley-44)]
    draw.line(l_brow, fill=HAIR, width=5)
    r_brow = [(rex-24, rey-22), (rex+5, rey-30), (rex+28, rey-38)]
    draw.line(r_brow, fill=HAIR, width=5)

    _draw_nose(draw, cx, cy)

    r_corner = (cx+55, cy+38)
    l_corner = (cx-38, cy+30)
    draw.line([r_corner, (cx-2, cy+38)], fill=LINE, width=3)
    smirk_pts = [(cx-2, cy+38), (cx-18, cy+32), l_corner]
    draw.line(smirk_pts, fill=LINE, width=3)
    teeth_pts = [l_corner, (cx-18,cy+30),(cx+10,cy+30),(cx+55,cy+38),
                 (cx+40,cy+46),(cx+0,cy+48),(cx-28,cy+44)]
    draw.polygon(teeth_pts, fill=(250,246,238))
    draw.line([r_corner, (cx-2, cy+38)], fill=LINE, width=3)
    draw.line(smirk_pts, fill=LINE, width=3)
    draw.ellipse([cx-head_r+8, cy+5, cx-head_r+58, cy+35], fill=(200,70,130,90))

    _draw_hair_overlay(draw, cx, cy)
    _draw_collar(draw, cx, cy, head_r, color=HOODIE_M, rotate_deg=-5)


def draw_settling_wonder(draw, cx, cy):
    """P17 — After excitement high, settling into wonder looking at Byte.
    Wide eyes, brows raised (not alarmed), soft open mouth. From chaos generator."""
    head_r = 100
    _draw_hair_mass(draw, cx, cy)
    _draw_head(draw, cx, cy)

    lex, ley = cx-38, cy-18
    rex, rey = cx+38, cy-18
    ew, eh = 28, 30   # wide/round eyes — genuine wonder

    for (ex, ey) in [(lex, ley), (rex, rey)]:
        draw.ellipse([ex-ew, ey-eh, ex+ew, ey+eh], fill=EYE_W, outline=LINE, width=2)
        draw.ellipse([ex-14, ey-14, ex+14, ey+14], fill=EYE_IRIS)
        # Pupils slightly dilated — wonder
        draw.ellipse([ex-9, ey-9, ex+9, ey+9], fill=EYE_PUP)
        draw.ellipse([ex+4, ey-11, ex+11, ey-4], fill=(255,252,245))
        draw.arc([ex-ew, ey-eh, ex+ew, ey+eh], start=200, end=340, fill=LINE, width=3)

    # Brows raised gently — open curiosity, not alarm, not furrowed
    draw.arc([lex-26, ley-52, lex+26, ley-28], start=200, end=340, fill=HAIR, width=5)
    draw.arc([rex-26, rey-50, rex+26, rey-26], start=200, end=340, fill=HAIR, width=5)

    _draw_nose(draw, cx, cy)

    # Mouth: softly open, wondering — gentle arc with small oval gap (not a scream)
    mouth_y = cy + 30
    draw.arc([cx-28, mouth_y, cx+28, mouth_y+24], start=20, end=160, fill=LINE, width=2)
    draw.ellipse([cx-14, mouth_y+4, cx+14, mouth_y+20], fill=(50,30,15))

    # Soft blush — wonder + delight
    draw.ellipse([cx-head_r+8,  cy+8, cx-head_r+52, cy+36], fill=(220,90,50,80))
    draw.ellipse([cx+head_r-52, cy+8, cx+head_r-8,  cy+36], fill=(220,90,50,70))

    _draw_hair_overlay(draw, cx, cy)
    _draw_collar(draw, cx, cy, head_r, color=HOODIE_S, rotate_deg=0)


def draw_recognition(draw, cx, cy):
    """P18 — Cognitive connection: asymmetric brow raise, concentrated narrowed eyes.
    ONE brow lifted (the aha brow), other brow level/slight furrow.
    Eyes narrowed in concentration — not wide, not closed."""
    head_r = 100
    _draw_hair_mass(draw, cx, cy)
    _draw_head(draw, cx, cy)

    lex, ley = cx-38, cy-18
    rex, rey = cx+38, cy-18
    ew = 28

    # Left eye — more open (the raised-brow side)
    leh = 26
    draw.ellipse([lex-ew, ley-leh, lex+ew, ley+leh], fill=EYE_W, outline=LINE, width=2)
    draw.ellipse([lex-12, ley-12, lex+12, ley+12], fill=EYE_IRIS)
    draw.ellipse([lex-7, ley-7, lex+7, ley+7], fill=EYE_PUP)
    draw.ellipse([lex+3, ley-9, lex+10, ley-3], fill=(255,252,245))
    draw.arc([lex-ew, ley-leh, lex+ew, ley+leh], start=200, end=340, fill=LINE, width=3)

    # Right eye — slightly squinted in concentration
    reh = 20
    draw.ellipse([rex-ew, rey-reh, rex+ew, rey+reh], fill=EYE_W, outline=LINE, width=2)
    draw.ellipse([rex-11, rey-11, rex+11, rey+11], fill=EYE_IRIS)
    draw.ellipse([rex-6,  rey-6,  rex+6,  rey+6],  fill=EYE_PUP)
    draw.ellipse([rex+3,  rey-8,  rex+10, rey-2],  fill=(255,252,245))
    draw.arc([rex-ew, rey-reh, rex+ew, rey+reh], start=200, end=340, fill=LINE, width=5)

    # Brows — ONE brow raised sky-high (aha), one level/slightly down (concentration)
    # Left brow: SKY HIGH — the recognition brow
    l_brow = [(lex-28, ley-52), (lex-2, ley-60), (lex+24, ley-48)]
    draw.line(l_brow, fill=HAIR, width=6)
    # Right brow: level/slightly inward (the thinking brow)
    r_brow = [(rex-24, rey-28), (rex+2, rey-32), (rex+26, rey-28)]
    draw.line(r_brow, fill=HAIR, width=5)

    _draw_nose(draw, cx, cy)

    # Mouth: slight open — "wait, is that—" moment, not closed, not full open
    draw.arc([cx-24, cy+28, cx+24, cy+44], start=15, end=165, fill=LINE, width=2)
    # Small gap — cognitive pause
    draw.ellipse([cx-8, cy+32, cx+8, cy+44], fill=(50,30,15))

    _draw_hair_overlay(draw, cx, cy)
    _draw_collar(draw, cx, cy, head_r, color=HOODIE_R, rotate_deg=3)


def draw_warmth(draw, cx, cy):
    """P20 — Choosing connection deliberately. Soft smile, happiness-narrowed eyes,
    cheek crinkle, brows gently raised. From chaos generator."""
    head_r = 100
    _draw_hair_mass(draw, cx, cy)
    _draw_head(draw, cx, cy)

    lex, ley = cx-38, cy-18
    rex, rey = cx+38, cy-18
    ew = 28

    # Eyes slightly narrowed — warmth squint (happiness closes eyes a little)
    for (ex, ey) in [(lex, ley), (rex, rey)]:
        eh = 20
        draw.ellipse([ex-ew, ey-eh, ex+ew, ey+eh], fill=EYE_W, outline=LINE, width=2)
        draw.ellipse([ex-12, ey-12, ex+12, ey+12], fill=EYE_IRIS)
        draw.ellipse([ex-7, ey-7, ex+7, ey+7], fill=EYE_PUP)
        draw.ellipse([ex+3, ey-8, ex+10, ey-2], fill=(255,252,245))
        # Heavier upper lid — warmth + slight squint
        draw.arc([ex-ew, ey-eh, ex+ew, ey+eh], start=195, end=345, fill=LINE, width=5)

    # Brows gently raised — peaceful presence, not alarmed, not tense
    draw.arc([lex-26, ley-46, lex+26, ley-26], start=200, end=340, fill=HAIR, width=5)
    draw.arc([rex-26, rey-44, rex+26, rey-24], start=200, end=340, fill=HAIR, width=5)

    _draw_nose(draw, cx, cy)

    # Soft genuine smile — NOT the grin. Gentle arc, no teeth, corners lifted.
    draw.arc([cx-34, cy+28, cx+34, cy+56], start=15, end=165, fill=LINE, width=3)

    # Cheek crinkle lines — warmth squint detail (Cycle 10: from chaos P20)
    draw.line([(cx-head_r+28, cy+10), (cx-head_r+18, cy+24)], fill=SKIN_SH, width=2)
    draw.line([(cx-head_r+34, cy+8),  (cx-head_r+24, cy+20)], fill=SKIN_SH, width=2)
    draw.line([(cx+head_r-28, cy+10), (cx+head_r-18, cy+24)], fill=SKIN_SH, width=2)
    draw.line([(cx+head_r-34, cy+8),  (cx+head_r-24, cy+20)], fill=SKIN_SH, width=2)

    # Warm blush — genuine happiness
    draw.ellipse([cx-head_r+8,  cy+5, cx-head_r+55, cy+35], fill=(230, 100, 60, 100))
    draw.ellipse([cx+head_r-55, cy+5, cx+head_r-8,  cy+35], fill=(230, 100, 60, 90))

    _draw_hair_overlay(draw, cx, cy)
    _draw_collar(draw, cx, cy, head_r, color=HOODIE_WA, rotate_deg=1)


# ── Expression table ──────────────────────────────────────────────────────────
#   (name, draw_fn, bg_color, hoodie_color, arm_l_dy, arm_r_dy, body_tilt, body_squash,
#    prev_state, next_state)
EXPRESSIONS = [
    (
        "RECKLESS EXCITEMENT",
        draw_reckless_excitement,
        BG_EXCITE, HOODIE_O,
        0, -8, 6, 1.0,
        "← was: ANY STATE",
        "→ next: CHARGING IN"
    ),
    (
        "WORRIED / DETERMINED",
        draw_worried_determined,
        BG_WORRY, HOODIE_W,
        0, 0, 0, 1.0,
        "← was: CALM",
        "→ next: TAKING ACTION"
    ),
    (
        "MISCHIEVOUS PLOTTING",
        draw_mischievous_plotting,
        BG_MISCH, HOODIE_M,
        -4, -10, -4, 1.0,
        "← was: BORED",
        "→ next: EXECUTING PLAN"
    ),
    (
        "SETTLING / WONDER",
        draw_settling_wonder,
        BG_SETTLE, HOODIE_S,
        8, 8, 0, 1.0,
        "← was: EXCITEMENT",
        "→ next: CURIOSITY"
    ),
    (
        "RECOGNITION",
        draw_recognition,
        BG_RECOG, HOODIE_R,
        -6, 2, -5, 1.0,
        "← was: CONFUSION",
        "→ next: CONNECTING"
    ),
    (
        "WARMTH",
        draw_warmth,
        BG_WARMTH, HOODIE_WA,
        10, 6, 2, 1.0,
        "← was: RECOGNITION",
        "→ next: CONNECTION"
    ),
]


def generate_luma_expression_sheet(output_path):
    """Render a 3×2 expression grid for Luma, matching Byte sheet structure."""

    total_w = COLS * (PANEL_W + PAD) + PAD
    total_h = HEADER + ROWS * (PANEL_H + PAD) + PAD

    img  = Image.new('RGBA', (total_w, total_h), (*CANVAS_BG, 255))
    draw = ImageDraw.Draw(img, 'RGBA')

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font       = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        font_sm    = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        font_title = font = font_sm = ImageFont.load_default()

    draw.text((PAD, 14), "LUMA — Expression Sheet — Luma & the Glitchkin",
              fill=(235, 200, 140), font=font_title)

    for i, (name, draw_fn, bg_col, hoodie_col,
            arm_l_dy, arm_r_dy, body_tilt, body_squash,
            prev_st, next_st) in enumerate(EXPRESSIONS):

        col = i % COLS
        row = i // COLS
        px  = PAD + col * (PANEL_W + PAD)
        py  = HEADER + row * (PANEL_H + PAD)

        # Panel background
        draw.rectangle([px, py, px+PANEL_W, py+PANEL_H],
                       fill=(*bg_col, 255), outline=(160, 150, 140, 255), width=2)

        # Face is rendered at a reduced scale in the upper 2/3 of the panel
        # Scale factor: face was designed for 400px wide; panel is 280px → scale ~0.58
        # We use a separate face canvas and paste it in
        FACE_SCALE = 0.55
        face_cw = int(400 * FACE_SCALE)
        face_ch = int(440 * FACE_SCALE)

        face_img  = Image.new('RGBA', (face_cw, face_ch), (*bg_col, 0))
        face_draw = ImageDraw.Draw(face_img, 'RGBA')

        # Draw at full scale on a larger intermediate canvas, then resize
        FULL_W, FULL_H = 400, 440
        full_face = Image.new('RGBA', (FULL_W, FULL_H), (*bg_col, 0))
        fd = ImageDraw.Draw(full_face, 'RGBA')
        draw_fn(fd, FULL_W//2, FULL_H//2 + 20)
        full_face_resized = full_face.resize((face_cw, face_ch), Image.LANCZOS)

        # Paste face into panel — center horizontally, top portion of panel
        face_x = px + (PANEL_W - face_cw) // 2
        face_y = py + 6
        img.alpha_composite(full_face_resized, (face_x, face_y))

        # Body below face — draw directly on main canvas
        body_top = face_y + face_ch - 20   # slight overlap so collar connects
        body_cx  = px + PANEL_W // 2
        _draw_body(draw, body_cx, body_top, hoodie_col,
                   arm_l_dy=arm_l_dy, arm_r_dy=arm_r_dy,
                   body_tilt=body_tilt, body_squash=body_squash)

        # Label bar at bottom of panel
        bar_h = 62
        bar_y = py + PANEL_H - bar_h
        draw.rectangle([px, bar_y, px+PANEL_W, py+PANEL_H], fill=(18, 12, 8, 230))
        draw.text((px+8, bar_y+4),  name,    fill=(235, 200, 140), font=font)
        draw.text((px+8, bar_y+22), prev_st, fill=(150, 130, 100), font=font_sm)
        draw.text((px+8, bar_y+36), next_st, fill=(150, 130, 100), font=font_sm)

    img = img.convert('RGB')
    img.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == '__main__':
    import os
    out_dir = "/home/wipkat/team/output/characters/main"
    os.makedirs(out_dir, exist_ok=True)
    generate_luma_expression_sheet(
        os.path.join(out_dir, "luma_expression_sheet.png")
    )
