#!/usr/bin/env python3
"""
LTG_TOOL_glitch_expression_sheet.py
Glitch — Expression Sheet v003
"Luma & the Glitchkin" — Cycle 28 / Maya Santos

v003 UPDATE (C28 — Interior Desire): Responding to Nkechi Adeyemi critique C12:
  "Glitch has six performance states but no accessible interior desire.
   Not yet a character — still a design."

  Grid expanded: 3x2 (6 expressions) -> 3x3 (9 expressions).
  Canvas: 1200x900 unchanged. Panel height adjusted to fit 3 rows.

  Three new expressions added showing Glitch's INTERIOR DESIRE:

  7. YEARNING: Glitch utterly still. No tilt, no squash. Body at rest.
     Both eyes: UV_PURPLE dim glow (soft, not glyph). Arms hanging low.
     No confetti. Spike subdued (spike_h=6). Crack visible but quiet.
     Mouth: silence — no rendered mouth feature.
     BG: deep indigo-void, still, interior, private.
     Read: "watching Luma have something Glitch cannot name — and wanting it."

  8. COVETOUS: Glitch leaning toward subject (tilt=+12). Left eye ACID_GREEN
     narrow-slit target lock. Both eyes forward-fixed (not destabilized).
     Arms reaching forward. Mouth: tight horizontal line.
     Confetti: UV_PURPLE only, sparse (count=4).
     Read: "I could take that. I should take that."

  9. HOLLOW: Slightly deflated body (squash=0.88). Both eyes empty stare
     (VOID_BLACK with single STATIC_WHITE center pixel). Arms dangling.
     No confetti. No spike activity. Single dim mouth dot.
     BG: near-black cold blue.
     Read: "After the wanting, nothing came back. Just absence."

GLITCH SPEC (unchanged from v002):
  show_guides=False. 2x internal render LANCZOS to 1x.
  VOID_BLACK outline, CORRUPT_AMBER primary, HOT_MAG cracks, UV_PURPLE shadow.

Output: output/characters/main/LTG_CHAR_glitch_expression_sheet.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Palette ────────────────────────────────────────────────────────────────────
CORRUPT_AMB    = (255, 140,   0)
CORRUPT_AMB_SH = (168,  76,   0)
CORRUPT_AMB_HL = (255, 185,  80)
SOFT_GOLD      = (232, 201,  90)
HOT_MAG        = (255,  45, 107)
UV_PURPLE      = (123,  47, 190)
ACID_GREEN     = ( 57, 255,  20)
ELEC_CYAN      = (  0, 240, 255)
VOID_BLACK     = ( 10,  10,  20)
STATIC_WHITE   = (248, 246, 236)
CANVAS_BG      = ( 10,  10,  20)

BG_NEUTRAL     = ( 22,  18,  32)
BG_MISCHIEVOUS = ( 28,  12,  18)
BG_PANICKED    = ( 12,  12,  22)
BG_TRIUMPHANT  = ( 32,  22,   8)
BG_STUNNED     = ( 18,  10,  28)  # electric shock purple-void
BG_CALCULATING = ( 14,  20,  14)  # cold dark green — calculating ambience
BG_YEARNING    = ( 12,  10,  28)  # deep indigo-void — still interior
BG_COVETOUS    = ( 16,  12,  26)  # dark purple-teal — covetous ambience
BG_HOLLOW      = (  8,   8,  16)  # near-black cold blue — empty after wanting

HEADER_H  = 54
LABEL_H   = 36
PAD       = 18
COLS      = 3
ROWS      = 3
SCALE     = 2

CANVAS_W_1X = 1200
CANVAS_H_1X = 900

PANEL_W_1X = (CANVAS_W_1X - (COLS + 1) * PAD) // COLS
PANEL_H_1X = (CANVAS_H_1X - HEADER_H - ROWS * LABEL_H - (ROWS + 1) * PAD) // ROWS


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


def draw_glitch_body(draw, cx, cy, rx, ry, tilt_deg=0, squash=1.0, stretch=1.0,
                     crack_visible=True):
    pts    = diamond_pts(cx, cy, rx, ry, tilt_deg, squash, stretch)
    sh_pts = [(x + 3, y + 4) for x, y in pts]
    draw.polygon(sh_pts, fill=UV_PURPLE)
    draw.polygon(pts, fill=CORRUPT_AMB)
    top, right, bot, left = pts
    mid_tl = ((top[0] + left[0]) // 2, (top[1] + left[1]) // 2)
    ctr    = (cx, cy - ry // 4)
    draw.polygon([top, ctr, mid_tl], fill=CORRUPT_AMB_HL)
    draw.polygon(pts, outline=VOID_BLACK, width=3)
    if crack_visible:
        cs = (cx - rx // 2, cy - ry // 3)
        ce = (cx + rx // 3, cy + ry // 2)
        draw.line([cs, ce], fill=HOT_MAG, width=2)
        mid_c = ((cs[0] + ce[0]) // 2, (cs[1] + ce[1]) // 2)
        draw.line([mid_c, (cx + rx // 2, cy - ry // 4)], fill=HOT_MAG, width=1)


def draw_top_spike(draw, cx, cy_top, rx, spike_h=12, tilt_off=0):
    sx  = cx + tilt_off
    pts = [
        (sx - spike_h // 2, cy_top),
        (sx - spike_h,      cy_top - spike_h),
        (sx,                cy_top - spike_h * 2),
        (sx + spike_h,      cy_top - spike_h),
        (sx + spike_h // 2, cy_top),
    ]
    draw.polygon(pts, fill=CORRUPT_AMB)
    draw.polygon(pts, outline=VOID_BLACK, width=2)
    draw.line([(sx, cy_top - spike_h * 2), (sx, cy_top - spike_h * 2 - 4)],
              fill=HOT_MAG, width=2)


def draw_bottom_spike(draw, cx, cy_bot, spike_h=10):
    pts = [
        (cx - spike_h // 2, cy_bot),
        (cx + spike_h // 2, cy_bot),
        (cx, cy_bot + spike_h + 4),
    ]
    draw.polygon(pts, fill=CORRUPT_AMB_SH)
    draw.polygon(pts, outline=VOID_BLACK, width=2)


def draw_arm(draw, cx, cy, side='left', arm_dy=0, arm_dx=0, rx=34):
    if side == 'left':
        ax  = cx - rx - 6
        ay  = cy + arm_dy
        tip = (ax - 14 + arm_dx, ay - 8)
    else:
        ax  = cx + rx + 6
        ay  = cy + arm_dy
        tip = (ax + 14 + arm_dx, ay - 8)
    pts = [(ax, ay - 5), (ax, ay + 5), tip]
    draw.polygon(pts, fill=CORRUPT_AMB)
    draw.polygon(pts, outline=VOID_BLACK, width=2)


def draw_pixel_eye(draw, ex, ey, cell=5, expr='neutral', side='left'):
    PIXEL_COLORS = {
        0: VOID_BLACK,
        1: CORRUPT_AMB_SH,
        2: CORRUPT_AMB,
        3: SOFT_GOLD,
        4: HOT_MAG,
        5: ACID_GREEN,
        6: UV_PURPLE,
        7: STATIC_WHITE,
    }
    # Left eye (primary expression glyph)
    GLYPHS = {
        'neutral':     [[0, 2, 0], [2, 1, 2], [0, 2, 0]],
        'mischievous': [[5, 0, 5], [0, 5, 0], [5, 0, 5]],  # acid X
        'panicked':    [[4, 4, 4], [4, 0, 4], [4, 4, 4]],  # hot ring
        'triumphant':  [[3, 3, 3], [3, 3, 3], [3, 3, 3]],  # solid gold
        'stunned':     [[4, 4, 4], [4, 4, 4], [4, 4, 4]],  # full hot mag (overloaded)
        'calculating': [[5, 0, 5], [0, 5, 0], [5, 0, 5]],  # acid X (plotting)
        'yearning':    [[0, 6, 0], [6, 1, 6], [0, 6, 0]],  # UV_PURPLE soft glow ring
        'covetous':    [[5, 5, 5], [0, 5, 0], [0, 0, 0]],  # acid slit — target lock
        'hollow':      [[0, 0, 0], [0, 7, 0], [0, 0, 0]],  # single white center: empty stare
    }
    # Right eye (destabilized bleed of left)
    DESTAB = {
        'neutral':     [[1, 2, 0], [2, 0, 1], [0, 2, 1]],
        'mischievous': [[5, 0, 0], [0, 5, 5], [5, 0, 0]],
        'panicked':    [[4, 0, 4], [0, 4, 0], [4, 0, 4]],
        'triumphant':  [[3, 3, 1], [3, 3, 3], [1, 3, 3]],
        'stunned':     [[4, 0, 4], [4, 0, 0], [0, 4, 0]],  # incomplete alarm
        'calculating': [[1, 0, 1], [0, 1, 0], [1, 0, 0]],  # dim — power to left eye
        'yearning':    [[0, 6, 0], [6, 1, 6], [0, 6, 0]],  # same soft glow — both eyes
        'covetous':    [[5, 5, 5], [0, 5, 0], [0, 0, 0]],  # same slit — bilateral focus
        'hollow':      [[0, 0, 0], [0, 7, 0], [0, 0, 0]],  # same empty stare both eyes
    }
    glyph = DESTAB[expr] if side == 'right' else GLYPHS[expr]
    for row in range(3):
        for col in range(3):
            state = glyph[row][col]
            color = PIXEL_COLORS[state]
            px    = ex + col * cell
            py    = ey + row * cell
            draw.rectangle([px, py, px + cell - 1, py + cell - 1], fill=color)


def draw_mouth(draw, mx, my, expr='neutral', w=14):
    if expr == 'neutral':
        for i in range(3):
            draw.rectangle([mx + i * 4, my, mx + i * 4 + 2, my + 2],
                            fill=CORRUPT_AMB_SH)

    elif expr == 'mischievous':
        w2  = w + 6
        pts = [(mx, my), (mx + w2 // 2, my - 4), (mx + w2, my - 7)]
        draw.line(pts, fill=HOT_MAG, width=3)
        draw.rectangle([mx + w2 - 1, my - 9, mx + w2 + 3, my - 5], fill=ACID_GREEN)
        draw.rectangle([mx + w2 + 4, my - 8, mx + w2 + 6, my - 6], fill=ACID_GREEN)

    elif expr == 'panicked':
        draw.ellipse([mx - 2, my - 5, mx + w + 2, my + 6],
                     outline=HOT_MAG, width=3)
        draw.ellipse([mx + 1, my - 2, mx + w - 1, my + 3], fill=VOID_BLACK)

    elif expr == 'triumphant':
        pts = [(mx - 2, my + 4), (mx + w // 2, my - 9), (mx + w + 2, my + 4)]
        draw.line(pts, fill=SOFT_GOLD, width=3)
        for gx in [mx + 2, mx + w // 2 - 2, mx + w // 2 + 2, mx + w - 3]:
            draw.rectangle([gx, my - 12, gx + 2, my - 9], fill=STATIC_WHITE)

    elif expr == 'stunned':
        # Wide jagged open scream — bigger than PANICKED, irregular
        draw.ellipse([mx - 4, my - 7, mx + w + 4, my + 8],
                     outline=HOT_MAG, width=3)
        draw.ellipse([mx - 1, my - 4, mx + w + 1, my + 5], fill=VOID_BLACK)
        # Electric fringe at top of mouth
        for fx in [mx, mx + w // 3, mx + 2 * w // 3, mx + w]:
            draw.line([(fx, my - 7), (fx, my - 12)], fill=ELEC_CYAN, width=1)

    elif expr == 'calculating':
        # Tight 2-dot "processing" — minimal, controlled
        draw.rectangle([mx + 2, my, mx + 4, my + 2], fill=CORRUPT_AMB_SH)
        draw.rectangle([mx + 8, my, mx + 10, my + 2], fill=CORRUPT_AMB_SH)

    elif expr == 'yearning':
        # Silence — the wanting has no words. No mouth rendered.
        pass

    elif expr == 'covetous':
        # Tight horizontal line — barely containing desire
        draw.line([(mx, my), (mx + w, my)], fill=CORRUPT_AMB_SH, width=2)
        # Small corner uptick — the wanting leaks out at the edge
        draw.line([(mx + w, my), (mx + w + 3, my - 3)], fill=ACID_GREEN, width=1)

    elif expr == 'hollow':
        # Single dim dot — not even processing
        draw.rectangle([mx + w // 2 - 1, my, mx + w // 2 + 1, my + 2],
                       fill=CORRUPT_AMB_SH)


def draw_hover_confetti(draw, cx, cy_bot, expr='neutral', seed=7):
    import random
    rng = random.Random(seed)
    confetti_colors = {
        'neutral':     [HOT_MAG, UV_PURPLE, VOID_BLACK],
        'mischievous': [ACID_GREEN, HOT_MAG, ACID_GREEN],
        'panicked':    [HOT_MAG, HOT_MAG, ELEC_CYAN],
        'triumphant':  [CORRUPT_AMB, SOFT_GOLD, HOT_MAG],
        'stunned':     [ELEC_CYAN, HOT_MAG, ELEC_CYAN, HOT_MAG],   # electrified
        'calculating': [UV_PURPLE, VOID_BLACK, CORRUPT_AMB_SH],     # slow/sparse
        'yearning':    [],                                           # no confetti — stillness
        'covetous':    [UV_PURPLE, UV_PURPLE, CORRUPT_AMB_SH],      # sparse, forward drift
        'hollow':      [],                                           # no confetti — empty
    }
    cols   = confetti_colors.get(expr, [HOT_MAG, UV_PURPLE])
    count  = {'neutral': 8, 'mischievous': 14, 'panicked': 22,
               'triumphant': 18, 'stunned': 20, 'calculating': 5,
               'yearning': 0, 'covetous': 4, 'hollow': 0}.get(expr, 8)
    spread = {'neutral': 24, 'mischievous': 28, 'panicked': 38,
               'triumphant': 32, 'stunned': 42, 'calculating': 14,
               'yearning': 0, 'covetous': 18, 'hollow': 0}.get(expr, 24)
    for _ in range(count):
        if not cols:
            break
        px  = rng.randint(cx - spread, cx + spread)
        py_range = 22 if expr in ('panicked', 'stunned') else 16
        py  = rng.randint(cy_bot + 4, cy_bot + py_range)
        sz  = rng.choice([2, 3, 4])
        col = rng.choice(cols)
        draw.rectangle([px, py, px + sz, py + sz], fill=col)


def draw_expression(draw, panel_cx, panel_cy, panel_w, panel_h,
                    expr='neutral', show_guides=False):
    cx = panel_cx
    cy = panel_cy + panel_h // 10

    params = {
        'neutral':     dict(tilt=0,   squash=1.0,  stretch=1.0,
                            arm_l_dy=0,   arm_r_dy=0,   spike_h=10, crack=True),
        'mischievous': dict(tilt=20,  squash=0.90, stretch=1.0,
                            arm_l_dy=-6,  arm_r_dy=14,  spike_h=14, crack=True),
        'panicked':    dict(tilt=-14, squash=0.55, stretch=1.0,
                            arm_l_dy=18,  arm_r_dy=6,   spike_h=6,  crack=True),
        'triumphant':  dict(tilt=0,   squash=1.0,  stretch=1.35,
                            arm_l_dy=-20, arm_r_dy=-22, spike_h=22, crack=True),
        # STUNNED: hard recoil jolt, both arms flung symmetric upward/outward
        'stunned':     dict(tilt=-18, squash=0.65, stretch=1.0,
                            arm_l_dy=-10, arm_r_dy=-8,  spike_h=8,  crack=True),
        # CALCULATING: still body, one arm raised to "chin" level — planning pose
        'calculating': dict(tilt=0,   squash=1.0,  stretch=1.05,
                            arm_l_dy=-22, arm_r_dy=2,   spike_h=12, crack=True),
        # YEARNING: completely still — the interiority of wanting without acting
        'yearning':    dict(tilt=0,   squash=1.0,  stretch=1.0,
                            arm_l_dy=18, arm_r_dy=16,   spike_h=6,  crack=True),
        # COVETOUS: leaning toward subject, arms reaching, target-locked eyes
        'covetous':    dict(tilt=12,  squash=0.85, stretch=1.0,
                            arm_l_dy=-8, arm_r_dy=-6,   spike_h=12, crack=True),
        # HOLLOW: deflated after the wanting, nothing came back
        'hollow':      dict(tilt=0,   squash=0.88, stretch=0.95,
                            arm_l_dy=14, arm_r_dy=20,   spike_h=4,  crack=True),
    }
    p  = params.get(expr, params['neutral'])
    rx = 34  # horizontal half-extent (ry > rx: body taller than wide — spec §2.1)
    ry = 38  # vertical half-extent

    cy_bot = cy + int(ry * p['squash'] * p['stretch'] * 1.15) + 6
    draw_hover_confetti(draw, cx, cy_bot, expr=expr, seed=hash(expr) % 100 + 1)
    draw_bottom_spike(draw, cx, cy_bot - 2, spike_h=10)
    draw_glitch_body(draw, cx, cy, rx, ry,
                     tilt_deg=p['tilt'], squash=p['squash'],
                     stretch=p['stretch'], crack_visible=p['crack'])
    draw_arm(draw, cx, cy, side='left',  arm_dy=p['arm_l_dy'], rx=rx)
    draw_arm(draw, cx, cy, side='right', arm_dy=p['arm_r_dy'], rx=rx)

    cy_top   = cy - int(ry * p['squash'] * p['stretch'])
    tilt_off = int(p['tilt'] * 0.4)
    draw_top_spike(draw, cx, cy_top, rx, spike_h=p['spike_h'], tilt_off=tilt_off)

    face_cy = cy - ry // 6
    cell    = 5
    leye_x  = cx - rx // 2 - cell * 3 // 2
    leye_y  = face_cy - cell * 3 // 2
    draw_pixel_eye(draw, leye_x, leye_y, cell=cell, expr=expr, side='left')
    reye_x  = cx + rx // 2 - cell * 3 // 2
    reye_y  = face_cy - cell * 3 // 2
    draw_pixel_eye(draw, reye_x, reye_y, cell=cell, expr=expr, side='right')

    mouth_cx = cx - 7
    mouth_cy = face_cy + cell * 3 // 2 + 4
    draw_mouth(draw, mouth_cx, mouth_cy, expr=expr, w=14)

    # Brows
    if expr == 'panicked':
        draw.line([(leye_x - 4, leye_y - 3), (leye_x + 14, leye_y - 8)],
                  fill=HOT_MAG, width=3)
        draw.line([(reye_x - 2, reye_y - 8), (reye_x + 16, reye_y - 3)],
                  fill=HOT_MAG, width=3)
    elif expr == 'mischievous':
        draw.line([(leye_x, leye_y - 2), (leye_x + 14, leye_y - 2)],
                  fill=CORRUPT_AMB_SH, width=2)
        draw.line([(reye_x, reye_y - 7), (reye_x + 14, reye_y - 1)],
                  fill=ACID_GREEN, width=3)
    elif expr == 'triumphant':
        draw.line([(leye_x - 2, leye_y - 8), (leye_x + 16, leye_y - 2)],
                  fill=SOFT_GOLD, width=3)
        draw.line([(reye_x - 2, reye_y - 2), (reye_x + 16, reye_y - 8)],
                  fill=SOFT_GOLD, width=3)
    elif expr == 'stunned':
        # Both brows raised very high and wide — shocked symmetric jolt
        draw.line([(leye_x - 4, leye_y - 10), (leye_x + 14, leye_y - 5)],
                  fill=ELEC_CYAN, width=3)
        draw.line([(reye_x - 2, reye_y - 5), (reye_x + 16, reye_y - 10)],
                  fill=ELEC_CYAN, width=3)
    elif expr == 'calculating':
        # Left brow angled DOWN toward eye (plotting/scheming inward lean)
        # Right brow flat/low (power asymmetry — most energy in left eye)
        draw.line([(leye_x - 2, leye_y - 8), (leye_x + 14, leye_y - 2)],
                  fill=ACID_GREEN, width=3)
        draw.line([(reye_x, reye_y - 2), (reye_x + 14, reye_y - 2)],
                  fill=CORRUPT_AMB_SH, width=1)
    elif expr == 'yearning':
        # Brows slightly raised and inward — open, unguarded, aching
        draw.line([(leye_x - 2, leye_y - 6), (leye_x + 14, leye_y - 4)],
                  fill=UV_PURPLE, width=2)
        draw.line([(reye_x - 2, reye_y - 4), (reye_x + 14, reye_y - 6)],
                  fill=UV_PURPLE, width=2)
    elif expr == 'covetous':
        # Brows furrowed downward toward center — predatory focus
        draw.line([(leye_x - 2, leye_y - 3), (leye_x + 14, leye_y - 7)],
                  fill=ACID_GREEN, width=3)
        draw.line([(reye_x - 2, reye_y - 7), (reye_x + 14, reye_y - 3)],
                  fill=ACID_GREEN, width=3)
    elif expr == 'hollow':
        # Brows flat, barely visible — no energy left for expression
        draw.line([(leye_x, leye_y - 2), (leye_x + 14, leye_y - 2)],
                  fill=CORRUPT_AMB_SH, width=1)
        draw.line([(reye_x, reye_y - 2), (reye_x + 14, reye_y - 2)],
                  fill=CORRUPT_AMB_SH, width=1)
    else:
        # Neutral flat dim
        draw.line([(leye_x, leye_y - 3), (leye_x + 14, leye_y - 3)],
                  fill=CORRUPT_AMB_SH, width=1)
        draw.line([(reye_x, reye_y - 3), (reye_x + 14, reye_y - 3)],
                  fill=CORRUPT_AMB_SH, width=1)


def build_sheet(show_guides=False):
    W2        = CANVAS_W_1X * SCALE
    H2        = CANVAS_H_1X * SCALE
    PW2       = PANEL_W_1X  * SCALE
    PH2       = PANEL_H_1X  * SCALE
    PAD2      = PAD          * SCALE
    HEADER_H2 = HEADER_H    * SCALE
    LABEL_H2  = LABEL_H     * SCALE

    img  = Image.new("RGB", (W2, H2), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    EXPRESSIONS = [
        ("NEUTRAL",      BG_NEUTRAL),
        ("MISCHIEVOUS",  BG_MISCHIEVOUS),
        ("PANICKED",     BG_PANICKED),
        ("TRIUMPHANT",   BG_TRIUMPHANT),
        ("STUNNED",      BG_STUNNED),
        ("CALCULATING",  BG_CALCULATING),
        ("YEARNING",     BG_YEARNING),
        ("COVETOUS",     BG_COVETOUS),
        ("HOLLOW",       BG_HOLLOW),
    ]

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24 * SCALE)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10 * SCALE)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()

    draw.rectangle([0, 0, W2, HEADER_H2], fill=(18, 14, 26))
    title_text = "GLITCH — Expression Sheet v003  [Cycle 28 — 9 Expressions — Interior Desire Added]"
    try:
        tb = draw.textbbox((0, 0), title_text, font=font_title)
        tw = tb[2] - tb[0]
        th = tb[3] - tb[1]
    except Exception:
        tw, th = len(title_text) * 14 * SCALE, 24 * SCALE
    draw.text(((W2 - tw) // 2, (HEADER_H2 - th) // 2),
              title_text, fill=CORRUPT_AMB, font=font_title)

    sub_text = "ANTAGONIST  |  GL-07 CORRUPT AMBER  |  CYCLE 28  |  show_guides=False  |  1200x900  3x3"
    try:
        sb = draw.textbbox((0, 0), sub_text, font=font_label)
        sw = sb[2] - sb[0]
        draw.text(((W2 - sw) // 2, HEADER_H2 - 18 * SCALE),
                  sub_text, fill=(120, 80, 40), font=font_label)
    except Exception:
        pass

    for idx, (expr_name, bg_col) in enumerate(EXPRESSIONS):
        col = idx % COLS
        row = idx // COLS

        px  = PAD2 + col * (PW2 + PAD2)
        py  = HEADER_H2 + PAD2 + row * (PH2 + LABEL_H2 + PAD2)

        draw.rectangle([px, py, px + PW2, py + PH2], fill=bg_col)

        panel_cx = px + PW2 // 2
        panel_cy = py + PH2 // 2
        expr_key = expr_name.lower()

        draw_expression(draw, panel_cx, panel_cy, PW2, PH2,
                        expr=expr_key, show_guides=show_guides)

        # Refresh draw after each panel (img.paste() pattern)
        draw = ImageDraw.Draw(img)

        draw.rectangle([px, py, px + PW2, py + PH2],
                       outline=(40, 30, 50), width=1)

        label_y = py + PH2 + 4 * SCALE
        try:
            lb = draw.textbbox((0, 0), expr_name, font=font_label)
            lw = lb[2] - lb[0]
        except Exception:
            lw = len(expr_name) * 8 * SCALE
        draw.text((px + (PW2 - lw) // 2, label_y),
                  expr_name, fill=CORRUPT_AMB, font=font_label)

    img_out = img.resize((CANVAS_W_1X, CANVAS_H_1X), Image.LANCZOS)
    return img_out


def main():
    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "characters", "main"
    )
    os.makedirs(out_dir, exist_ok=True)

    sheet    = build_sheet(show_guides=False)
    out_path = os.path.join(out_dir, "LTG_CHAR_glitch_expression_sheet.png")
    sheet.save(out_path)
    print(f"Saved: {out_path}")
    print(f"  Size: {sheet.size[0]}x{sheet.size[1]}px")
    print("  Expressions: NEUTRAL, MISCHIEVOUS, PANICKED, TRIUMPHANT, STUNNED, CALCULATING,")
    print("               YEARNING, COVETOUS, HOLLOW")
    print("  Canvas: 1200x900 3x3 grid (expanded from 3x2)")
    print("  NEW — Interior desire states: YEARNING, COVETOUS, HOLLOW")
    print("  YEARNING: still body, UV_PURPLE eyes, no confetti, no mouth — interiority")
    print("  COVETOUS: leaning, acid-slit eyes, bilateral focus, sparse confetti")
    print("  HOLLOW: deflated, empty bilateral stare, no confetti — aftermath of wanting")
    print("  show_guides=False (pitch export)")


if __name__ == "__main__":
    main()
