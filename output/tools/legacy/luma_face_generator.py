# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
Luma Face Generator — "Luma & the Glitchkin"
Cycle 6: multi-expression sheet (3 expressions), broken symmetry for reckless_excitement,
removed curl artifact outlines, added worried_determined and mischievous_plotting expressions.
"""
from PIL import Image, ImageDraw, ImageFont
import math

FACE_W, FACE_H = 400, 440

SKIN      = (200, 136, 90)
SKIN_SH   = (168, 104, 56)
SKIN_HL   = (232, 184, 136)
HAIR      = (26, 15, 10)
EYE_W     = (255, 252, 245)
EYE_PUP   = (20, 12, 8)
EYE_IRIS  = (60, 38, 20)
BLUSH     = (220, 100, 60, 140)
LINE      = (59, 40, 32)
HOODIE_O  = (232, 114, 42)
HOODIE_W  = (52, 38, 24)     # worried/determined hoodie (darker)
HOODIE_M  = (180, 60, 120)   # mischievous hoodie tint
# Panel backgrounds — must be distinguishable at pitch/print scale.
# Excitement: committed warm amber mid-tone (240,200,150) — Cycle 9 push from off-white.
#   Previous (248,238,220) read as off-white at distance; new value reads clearly warm.
# Worry: genuinely cool desaturated blue-grey (much cooler than before).
# Mischief: bold warm deep lavender (committed purple, not "light neutral").
BG        = (240, 200, 150)   # warm amber mid-tone (Cycle 9: pushed from off-white to committed warm amber — reads clearly at distance)
BG_WORRY  = (195, 212, 228)   # cool desaturated blue-grey
BG_MISCH  = (220, 205, 242)   # warm deep lavender


def _draw_hair_mass(draw, cx, cy):
    """Luma's hair cloud — no artifact curl outlines."""
    draw.ellipse([cx-155, cy-195, cx+145, cy+40], fill=HAIR)
    draw.ellipse([cx-175, cy-170, cx-80,  cy-60],  fill=HAIR)
    draw.ellipse([cx-165, cy-140, cx-95,  cy-30],  fill=HAIR)
    draw.ellipse([cx+80,  cy-160, cx+155, cy-60],  fill=HAIR)
    draw.ellipse([cx+90,  cy-130, cx+145, cy-40],  fill=HAIR)
    draw.ellipse([cx-60,  cy-215, cx+20,  cy-140], fill=HAIR)
    draw.ellipse([cx-20,  cy-225, cx+70,  cy-145], fill=HAIR)
    draw.ellipse([cx-100, cy-200, cx-30,  cy-130], fill=HAIR)
    # NOTE: removed the faint circular outline loops that read as artifacts


def _draw_head(draw, cx, cy):
    head_r = 100
    draw.ellipse([cx-head_r, cy-head_r, cx+head_r, cy+head_r+15],
                 fill=SKIN, outline=LINE, width=3)
    draw.ellipse([cx-95, cy-20, cx+95, cy+head_r+25], fill=SKIN)
    draw.arc([cx-95, cy-20, cx+95, cy+head_r+25], start=0, end=180, fill=LINE, width=3)
    # Ears
    draw.ellipse([cx-head_r-12, cy-20, cx-head_r+14, cy+20],
                 fill=SKIN, outline=LINE, width=2)
    draw.ellipse([cx+head_r-14, cy-20, cx+head_r+12, cy+20],
                 fill=SKIN, outline=LINE, width=2)


def _draw_nose(draw, cx, cy):
    draw.ellipse([cx-8, cy+8, cx-2, cy+14], fill=SKIN_SH)
    draw.ellipse([cx+2, cy+8, cx+8, cy+14], fill=SKIN_SH)
    draw.arc([cx-6, cy-10, cx+6, cy+12], start=200, end=340, fill=SKIN_SH, width=2)


def _draw_hair_overlay(draw, cx, cy):
    """Stray curls over forehead."""
    draw.arc([cx-60, cy-195, cx-10, cy-140], start=30,  end=200, fill=HAIR, width=8)
    draw.arc([cx-20, cy-190, cx+40, cy-130], start=10,  end=190, fill=HAIR, width=7)


def _draw_collar(draw, cx, cy, head_r, color=None, offset_x=0, rotate_deg=0):
    """Draw Luma's hoodie collar.

    Cycle 8 fix (Marcus mandate): collar is drawn as a ROTATED arc, not an x-offset ellipse.
    rotate_deg: positive = tilt right (reckless excitement, head leans toward monitor).
    Rotation is implemented by transforming the collar's polygon/arc control points
    using a 2D rotation matrix — no temporary image needed, works with any draw context.
    offset_x is kept for backward compatibility but rotate_deg is the primary control.

    The collar arc is modelled as an ellipse rotated about its own centre:
      - Ellipse semi-axes: rx=90, ry=35, centred at (cx, cy+head_r+45)
      - We draw the collar fill as a filled polygon (rotated ellipse approximated by N pts)
        then overdraw the lower arc as a polyline of the same rotated points.
    """
    col = color if color else HOODIE_O
    collar_cx = cx + offset_x
    collar_cy = cy + head_r + 45
    rx = 90
    ry = 35
    theta = math.radians(rotate_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    def rot(x, y):
        """Rotate point (x,y) relative to collar_cx/cy by rotate_deg."""
        return (
            int(collar_cx + x * cos_t - y * sin_t),
            int(collar_cy + x * sin_t + y * cos_t),
        )

    # Build full ellipse outline (N=48 points) for fill polygon
    N = 48
    full_pts = [rot(int(rx * math.cos(2*math.pi*i/N)),
                    int(ry * math.sin(2*math.pi*i/N))) for i in range(N)]
    draw.polygon(full_pts, fill=col)

    # Lower arc (180→360 degrees = bottom half) as polyline for outline
    arc_pts = [rot(int(rx * math.cos(math.radians(a))),
                   int(ry * math.sin(math.radians(a)))) for a in range(180, 361, 5)]
    draw.line(arc_pts, fill=LINE, width=3)

    # Pixel circuit detail squares on collar — placed along collar centre line
    for i in range(5):
        # Local position: evenly spaced across collar, slightly below centre
        local_x = -35 + i * 17
        local_y = 8
        px_c, py_c = rot(local_x, local_y)
        # Draw a small rotated square as a polygon
        half = 5
        sq = [rot(local_x - half, local_y - 4),
              rot(local_x + half, local_y - 4),
              rot(local_x + half, local_y + 4),
              rot(local_x - half, local_y + 4)]
        draw.polygon(sq, fill=(0, 240, 255))


def draw_reckless_excitement(draw, cx, cy):
    """
    RECKLESS EXCITEMENT — broken symmetry.
    Left brow higher + kinked. Mouth arc shifted left.
    Pupils shifted screen-right (looking at exciting thing).
    Left eye slightly more open. Bottom lip suggestion.
    Collar slightly off-center (implied head tilt).
    Chord iris partially cut by upper eyelid (engagement).
    """
    head_r = 100

    _draw_hair_mass(draw, cx, cy)
    _draw_head(draw, cx, cy)

    # Eyes — asymmetric
    lex, ley = cx-38, cy-18   # left eye center
    rex, rey = cx+38, cy-18   # right eye center
    ew = 28
    leh = 30   # left eye more open (+ 4px)
    reh = 26   # right eye normal

    # Left eye (more open)
    draw.ellipse([lex-ew, ley-leh, lex+ew, ley+leh], fill=EYE_W, outline=LINE, width=2)
    # Iris — squashed ellipse, top cut off by chord (simulates raised eyelid engagement)
    iris_r = 15
    draw.chord([lex-iris_r, ley-iris_r+2, lex+iris_r, ley+iris_r+2],
               start=15, end=345, fill=EYE_IRIS)
    draw.ellipse([lex-9, ley-7, lex+9, ley+9], fill=EYE_PUP)
    # Highlight — shifted right to imply looking at something off-right
    draw.ellipse([lex+6, ley-9, lex+13, ley-2], fill=(255, 252, 245))
    draw.arc([lex-ew, ley-leh, lex+ew, ley+leh], start=200, end=340, fill=LINE, width=4)

    # Right eye (normal open)
    draw.ellipse([rex-ew, rey-reh, rex+ew, rey+reh], fill=EYE_W, outline=LINE, width=2)
    draw.chord([rex-iris_r, rey-iris_r+2, rex+iris_r, rey+iris_r+2],
               start=15, end=345, fill=EYE_IRIS)
    # Pupils shifted screen-right — looking at something exciting
    pupil_shift = 5
    draw.ellipse([rex-9+pupil_shift, rey-7, rex+9+pupil_shift, rey+9], fill=EYE_PUP)
    draw.ellipse([rex+6+pupil_shift, rey-9, rex+13+pupil_shift, rey-2], fill=(255, 252, 245))
    draw.arc([rex-ew, rey-reh, rex+ew, rey+reh], start=200, end=340, fill=LINE, width=4)

    # Left pupil also shifted right
    draw.ellipse([lex-9+pupil_shift, ley-7, lex+9+pupil_shift, ley+9], fill=EYE_PUP)

    # Brows — ASYMMETRIC
    # Left brow: HIGHER and kinked (outer corner angled down = reckless "I know something")
    l_brow_pts = [(lex - 30, ley-42), (lex - 5, ley-52), (lex + 22, ley-39)]
    draw.line(l_brow_pts, fill=HAIR, width=5)
    # Right brow: lower, clean arch (contrast)
    r_brow_pts = [(rex - 22, rey-34), (rex - 5, rey-40), (rex + 28, rey-32)]
    draw.line(r_brow_pts, fill=HAIR, width=5)

    _draw_nose(draw, cx, cy)

    # Mouth — grin arc shifted LEFT of center, one corner higher
    # Left corner pulled up = reckless dominant side
    m_off = -6   # shift left
    draw.arc([cx-45+m_off, cy+18, cx+45+m_off, cy+70],
             start=5, end=175, fill=LINE, width=4)
    # Top lip
    draw.arc([cx-44+m_off, cy+20, cx+44+m_off, cy+50],
             start=5, end=175, fill=LINE, width=3)
    # Teeth chord fill
    draw.chord([cx-42+m_off, cy+22, cx+42+m_off, cy+65],
               start=7, end=173, fill=(250, 246, 238))
    draw.arc([cx-42+m_off, cy+22, cx+42+m_off, cy+65],
             start=7, end=173, fill=LINE, width=2)
    # Bottom lip suggestion — slightly dips below chord
    draw.arc([cx-20+m_off, cy+62, cx+26+m_off, cy+76],
             start=5, end=175, fill=SKIN_SH, width=2)
    # Dimple left (more pronounced)
    draw.arc([cx-50, cy+25, cx-30, cy+45], start=320, end=60, fill=SKIN_SH, width=2)

    # Blush — high intensity, outer cheeks
    draw.ellipse([cx-head_r+8, cy+5,   cx-head_r+58, cy+38], fill=(220, 80, 50, 110))
    draw.ellipse([cx+head_r-58, cy+5,  cx+head_r-8,  cy+38], fill=(220, 80, 50, 90))

    _draw_hair_overlay(draw, cx, cy)
    # Collar ROTATED right — head leaning toward monitor (Cycle 8: rotation not x-offset)
    _draw_collar(draw, cx, cy, head_r, rotate_deg=8)


def draw_worried_determined(draw, cx, cy):
    """
    WORRIED/DETERMINED — brows furrowed and close together in a V,
    tight straight mouth with slight jaw set, narrowed eyes.
    """
    head_r = 100

    _draw_hair_mass(draw, cx, cy)
    _draw_head(draw, cx, cy)

    lex, ley = cx-38, cy-20
    rex, rey = cx+38, cy-20
    ew = 28
    eh = 22   # narrowed eyes (worried tightness)

    # Left eye — slightly narrowed
    draw.ellipse([lex-ew, ley-eh, lex+ew, ley+eh], fill=EYE_W, outline=LINE, width=2)
    draw.ellipse([lex-13, ley-13, lex+13, ley+13], fill=EYE_IRIS)
    draw.ellipse([lex-8, ley-8, lex+8, ley+8], fill=EYE_PUP)
    draw.ellipse([lex+3, ley-8, lex+9, ley-2], fill=(255, 252, 245))
    # Heavy upper lid to show tension
    draw.arc([lex-ew, ley-eh, lex+ew, ley+eh], start=195, end=345, fill=LINE, width=5)

    # Right eye — similarly narrowed
    draw.ellipse([rex-ew, rey-eh, rex+ew, rey+eh], fill=EYE_W, outline=LINE, width=2)
    draw.ellipse([rex-13, rey-13, rex+13, rey+13], fill=EYE_IRIS)
    draw.ellipse([rex-8, rey-8, rex+8, rey+8], fill=EYE_PUP)
    draw.ellipse([rex+3, rey-8, rex+9, rey-2], fill=(255, 252, 245))
    draw.arc([rex-ew, rey-eh, rex+ew, rey+eh], start=195, end=345, fill=LINE, width=5)

    # Brows — WORRIED/DETERMINED combination.
    # Outer two-thirds angle DOWN toward nose bridge (determined V-shape).
    # Inner tip (medial corner, closest to nose) kinks UPWARD — the corrugator kink
    # that distinguishes "I'm worried" from pure determined aggression.
    #
    # Cycle 8 fix (Marcus + Dmitri mandates):
    # Left brow outer corner is 8-10px HIGHER than right brow outer corner.
    # This height differential creates the visual "dueling impulses" read at pitch scale.
    # Previous: both outer corners at ley-30 / rey-30 (identical height, too subtle).
    # Now: left outer = ley-38, right outer = ley-30 → 8px differential visible at distance.
    # Corrugator kink increased to match: inner tip kicks up 8px (was 4px).
    #
    # Left brow: outer corner HIGH (worried/raised), angles down, inner tip kicks up 8px
    l_brow_pts = [(lex - 28, ley-38), (lex + 5, ley-26), (lex + 20, ley-20), (lex + 26, ley-28)]
    draw.line(l_brow_pts, fill=HAIR, width=6)
    # Right brow: outer corner LOWER (determined/set), angles down, inner tip kicks up 8px
    r_brow_pts = [(rex + 28, rey-30), (rex - 5, rey-24), (rex - 20, rey-20), (rex - 26, rey-28)]
    draw.line(r_brow_pts, fill=HAIR, width=6)

    _draw_nose(draw, cx, cy)

    # Mouth — tight, straight, slightly downturned at corners (set jaw)
    draw.line([(cx-32, cy+38), (cx+32, cy+38)], fill=LINE, width=3)
    # Corners pulled down slightly
    draw.line([(cx-32, cy+38), (cx-38, cy+44)], fill=LINE, width=3)
    draw.line([(cx+32, cy+38), (cx+38, cy+44)], fill=LINE, width=3)

    # Minimal blush (tension, not happiness)
    draw.ellipse([cx-head_r+12, cy+10, cx-head_r+52, cy+36], fill=(200, 80, 50, 55))
    draw.ellipse([cx+head_r-52, cy+10, cx+head_r-12, cy+36], fill=(200, 80, 50, 55))

    _draw_hair_overlay(draw, cx, cy)
    # Worried — collar nearly upright (slight lean, tense)
    _draw_collar(draw, cx, cy, head_r, color=HOODIE_W, rotate_deg=2)


def draw_mischievous_plotting(draw, cx, cy):
    """
    MISCHIEVOUS PLOTTING — one brow raised sky-high (scheming arc),
    other brow down and inward. Half-lidded eyes. Slight smirk pulling one corner only.
    """
    head_r = 100

    _draw_hair_mass(draw, cx, cy)
    _draw_head(draw, cx, cy)

    lex, ley = cx-38, cy-18
    rex, rey = cx+38, cy-18
    ew = 28

    # Left eye — half-lidded (scheming)
    leh_top = 14   # compressed from top
    draw.ellipse([lex-ew, ley-leh_top, lex+ew, ley+leh_top+6], fill=EYE_W, outline=LINE, width=2)
    draw.ellipse([lex-13, ley-12, lex+13, ley+12], fill=EYE_IRIS)
    draw.ellipse([lex-8, ley-8, lex+8, ley+8], fill=EYE_PUP)
    draw.ellipse([lex+3, ley-7, lex+9, ley-1], fill=(255, 252, 245))
    # Heavy droopy upper lid — the scheming look
    draw.arc([lex-ew, ley-leh_top, lex+ew, ley+leh_top+6],
             start=195, end=345, fill=LINE, width=6)

    # Right eye — wide open (contrast = theatrical suspense)
    reh = 28
    draw.ellipse([rex-ew, rey-reh, rex+ew, rey+reh], fill=EYE_W, outline=LINE, width=2)
    draw.ellipse([rex-13, rey-13, rex+13, rey+13], fill=EYE_IRIS)
    draw.ellipse([rex-8, rey-8, rex+8, rey+8], fill=EYE_PUP)
    draw.ellipse([rex+3, rey-10, rex+9, rey-3], fill=(255, 252, 245))
    draw.arc([rex-ew, rey-reh, rex+ew, rey+reh], start=200, end=340, fill=LINE, width=4)

    # Brows — EXTREME asymmetry
    # Left brow: SKY HIGH arch (scheming/plotting)
    l_brow_pts = [(lex - 30, ley-46), (lex - 5, ley-58), (lex + 24, ley-44)]
    draw.line(l_brow_pts, fill=HAIR, width=5)
    # Right brow: down and inward (the other half of scheming)
    r_brow_pts = [(rex - 24, rey-22), (rex + 5, rey-30), (rex + 28, rey-38)]
    draw.line(r_brow_pts, fill=HAIR, width=5)

    _draw_nose(draw, cx, cy)

    # Mouth — asymmetric smirk, only LEFT corner pulls up.
    # Right corner anchored at (cx+55, cy+38) — proper cheek anchor, not mid-face.
    # Left corner hooks up to (cx-38, cy+30).
    # Teeth fill sits symmetrically under the smirk arc.
    r_corner = (cx + 55, cy + 38)   # right: flat, anchored at cheek
    l_corner = (cx - 38, cy + 30)   # left: raised, conspiratorial hook
    mid_top  = (cx + 8,  cy + 30)   # mid-point of smirk top (slightly left-biased)
    # Outline: right flat segment then curved left hook
    draw.line([r_corner, (cx - 2, cy + 38)], fill=LINE, width=3)          # flat right half
    smirk_pts = [(cx - 2, cy + 38), (cx - 18, cy + 32), l_corner]
    draw.line(smirk_pts, fill=LINE, width=3)
    # Teeth — symmetric fill under the smirk arc from l_corner to r_corner
    # Use a filled polygon rather than a chord to avoid arc-angle crescent artifacts
    teeth_pts = [
        l_corner,
        (cx - 18, cy + 30),   # left inner curve
        (cx + 10, cy + 30),   # right inner curve
        (cx + 55, cy + 38),   # right corner
        (cx + 40, cy + 46),   # right bottom
        (cx + 0,  cy + 48),   # bottom centre
        (cx - 28, cy + 44),   # left bottom
    ]
    draw.polygon(teeth_pts, fill=(250, 246, 238))
    # Re-draw smirk outline over fill so it stays crisp
    draw.line([r_corner, (cx - 2, cy + 38)], fill=LINE, width=3)
    draw.line(smirk_pts, fill=LINE, width=3)

    # Blush — one-sided (the plotting side)
    draw.ellipse([cx-head_r+8, cy+5, cx-head_r+58, cy+35], fill=(200, 70, 130, 90))

    _draw_hair_overlay(draw, cx, cy)
    # Mischievous — collar rotated left (conspiratorial lean away from viewer)
    _draw_collar(draw, cx, cy, head_r, color=HOODIE_M, rotate_deg=-5)


EXPRESSIONS_MAP = {
    "reckless_excitement":  (draw_reckless_excitement,  "Reckless Excitement",  BG),
    "worried_determined":   (draw_worried_determined,   "Worried / Determined", BG_WORRY),
    "mischievous_plotting": (draw_mischievous_plotting, "Mischievous Plotting", BG_MISCH),
}


def draw_luma_face(output_path, expression="reckless_excitement"):
    """Draw a single Luma face at 600x600."""
    img = Image.new('RGBA', (600, 600), (*BG, 255))
    draw = ImageDraw.Draw(img, 'RGBA')

    try:
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font_sm = ImageFont.load_default()

    cx, cy = 300, 320

    fn, label, _ = EXPRESSIONS_MAP.get(expression,
                    (draw_reckless_excitement, expression.replace('_', ' ').title(), BG))
    fn(draw, cx, cy)

    draw.rectangle([0, 564, 600, 600], fill=(20, 15, 12))
    draw.text((10, 572), f"LUMA — {label} — Luma & the Glitchkin",
              fill=(235, 228, 210), font=font_sm)

    img = img.convert('RGB')
    img.save(output_path)
    print(f"Saved: {output_path}")


def draw_luma_expressions_sheet(output_path):
    """
    Generate a 3-panel horizontal expression sheet.
    Each panel is FACE_W x FACE_H.
    """
    PAD = 20
    LABEL_H = 48
    N = len(EXPRESSIONS_MAP)
    total_w = N * FACE_W + (N + 1) * PAD
    total_h = FACE_H + 2 * PAD + LABEL_H + 40  # +40 for title

    img = Image.new('RGBA', (total_w, total_h), (*BG, 255))
    draw = ImageDraw.Draw(img, 'RGBA')

    try:
        font       = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        font_sm    = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except:
        font = font_sm = font_title = ImageFont.load_default()

    draw.text((PAD, 8), "LUMA — Expression Sheet — Luma & the Glitchkin",
              fill=(40, 25, 15), font=font_title)

    for i, (key, (fn, label, bg_col)) in enumerate(EXPRESSIONS_MAP.items()):
        px = PAD + i * (FACE_W + PAD)
        py = 40

        # Panel background
        draw.rectangle([px, py, px + FACE_W, py + FACE_H],
                       fill=(*bg_col, 255), outline=(180, 170, 160, 255), width=1)

        # Face drawn centered within panel
        face_cx = px + FACE_W // 2
        face_cy = py + FACE_H // 2 + 20
        fn(draw, face_cx, face_cy)

        # Label bar at bottom of panel
        draw.rectangle([px, py + FACE_H - LABEL_H, px + FACE_W, py + FACE_H],
                       fill=(20, 15, 12, 220))
        draw.text((px + 8, py + FACE_H - LABEL_H + 8),
                  label.upper(), fill=(235, 228, 210), font=font_sm)

    img = img.convert('RGB')
    img.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == '__main__':
    # Generate individual face (backward compatible)
    draw_luma_face(
        "/home/wipkat/team/output/characters/main/luma_face_closeup.png",
        "reckless_excitement"
    )
    # Generate multi-expression sheet
    draw_luma_expressions_sheet(
        "/home/wipkat/team/output/characters/main/luma_expressions.png"
    )
