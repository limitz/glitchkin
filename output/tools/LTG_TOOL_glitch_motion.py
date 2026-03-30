# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_glitch_motion.py
Ryo Hasegawa / Cycle 45
Motion Spec Sheet — GLITCH (Glitchkin antagonist)
4 panels: PREDATORY STILL | COVETOUS REACH | CORRUPTION SURGE | RETREAT

Beat arc per Alex Chen C44 brief:
  B1: PREDATORY STILL — absolute stillness (no idle hover, no confetti).
      Wrongness IS the absence of motion. Held state, indefinite duration.
  B2: COVETOUS REACH — desire-state. One arm-spike slowly extends toward subject.
      Very slow, smooth arc. Eyes bilateral acid-slit (interior state = real feeling).
      Minimal UV_PURPLE confetti only.
  B3: CORRUPTION SURGE — loss of composure. Body scale pulses ±15% (grow then shrink).
      Jittery, staccato. Crack line brightens (HOT_MAG arc). Spike_h increases.
      HOT_MAG+UV_PURPLE confetti max spread.
  B4: RETREAT — repelled/thwarted. Rapid body compression + backward displacement.
      Reads as coil-back, not defeat. Still dangerous. Eyes: panicked HOT ring.

Canonical Glitch body spec (from glitch.md — all generators must follow):
  - Body fill: CORRUPT_AMBER (255,140,0) — digital warm (NOT organic warm)
  - Shadow: UV_PURPLE (123,47,190) offset +3,+4
  - Highlight facet: CORRUPT_AMB_HL (255,185,80) — top-left triangle
  - Outline: VOID_BLACK (10,10,20) width=3
  - Crack: HOT_MAG (255,45,107) diagonal + fork — ALWAYS visible
  - rx=34, ry=38 base (scaled up here for motion doc clarity)
  - ry > rx (taller than wide — G002 spec)
  NOTE: Alex Chen C44 brief incorrectly states Glitch uses Void/Cyan/UV palette only.
  Glitch body IS CORRUPT_AMBER per glitch.md (Maya Santos C32, confirmed canonical spec).
  Discrepancy flagged in Alex inbox. Canonical spec followed here.

Canvas: 1280x720 (<=1280 limit)
Output: output/characters/motion/LTG_CHAR_glitch_motion.png
"""
from __future__ import annotations

import math
import os
import json
import random

from PIL import Image, ImageDraw

# --- Load config ---
_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "sheet_geometry_config.json")


def _load_header_h_glitch(default=56):
    """Load HEADER_H for glitch family from sheet_geometry_config.json."""
    try:
        with open(_CONFIG_PATH) as f:
            cfg = json.load(f)
        geo = cfg.get("families", {}).get("glitch", {})
        return geo.get("panel_top_abs", default)
    except Exception:
        return default


_GLITCH_PANEL_TOP = _load_header_h_glitch(default=56)

# --- CANONICAL COLORS (from glitch.md §2.2 — Maya Santos C32) ---
CORRUPT_AMB     = (255, 140,   0)   # #FF8C00 Main body fill
CORRUPT_AMB_SH  = (168,  76,   0)   # #A84C00 Shadow amber
CORRUPT_AMB_HL  = (255, 185,  80)   # #FFB950 Highlight facet
HOT_MAG         = (255,  45, 107)   # #FF2D6B crack + confetti
UV_PURPLE       = (123,  47, 190)   # #7B2FBE shadow + confetti
VOID_BLACK      = ( 10,  10,  20)   # #0A0A14 outline + panel background
SOFT_GOLD       = (232, 201,  90)   # #E8C95A Triumphant eye state
ACID_GREEN      = ( 57, 255,  20)   # #39FF14 Mischievous/Covetous eye state
ELEC_CYAN       = (  0, 240, 255)   # #00F0FF involuntary confetti leak only (PANICKED)

# Annotation colors — dark sheet
ANNOTATION_BG   = ( 22,  18,  32)   # dark near-void panel background
PANEL_BORDER    = ( 60,  50,  80)   # dim purple-grey border
LABEL_BG        = CORRUPT_AMB       # amber label on dark background
LABEL_TEXT      = VOID_BLACK        # void black text on amber
MOTION_ARROW    = CORRUPT_AMB       # amber — secondary motion arrows
BEAT_COLOR      = CORRUPT_AMB       # amber beats (matches character palette)
ACCENT_DASH     = ( 80,  60, 100)   # dim purple guide lines
ANNOT_TEXT      = (220, 200, 160)   # warm off-white annotations on dark bg

# --- CANVAS ---
W, H         = 1280, 720
COLS         = 4
PAD          = 14
HEADER_H     = 44
_TITLE_H     = max(_GLITCH_PANEL_TOP - PAD, 40)
PANEL_W      = (W - PAD * (COLS + 1)) // COLS
PANEL_H      = H - PAD * 2 - _GLITCH_PANEL_TOP

# Glitch body scale (larger than expression sheet rx=34 for motion doc clarity)
RX = 44
RY = 50


# ------------------------------------------------------------------ helpers

def panel_origin(col):
    """Top-left (x, y) of panel col (0-based)."""
    x = PAD + col * (PANEL_W + PAD)
    y = _GLITCH_PANEL_TOP
    return x, y


def draw_arrow(draw, x0, y0, x1, y1, color=None, width=2, head=8):
    color = color or MOTION_ARROW
    draw.line([(x0, y0), (x1, y1)], fill=color, width=width)
    angle = math.atan2(y1 - y0, x1 - x0)
    for da in (-0.4, 0.4):
        ax = x1 - head * math.cos(angle + da)
        ay = y1 - head * math.sin(angle + da)
        draw.line([(x1, y1), (int(ax), int(ay))], fill=color, width=width)


def label_box(draw, x, y, text, bg=None, fg=None, pad=4):
    bg = bg or LABEL_BG
    fg = fg or LABEL_TEXT
    bbox = draw.textbbox((0, 0), text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rectangle([x, y, x + tw + pad * 2, y + th + pad * 2], fill=bg)
    draw.text((x + pad, y + pad), text, fill=fg)
    return tw + pad * 2, th + pad * 2


def annot_text(draw, x, y, text, color=None):
    draw.text((x, y), text, fill=color or ANNOT_TEXT)


# ------------------------------------------------------------------ Glitch body

def diamond_pts(cx, cy, rx, ry, tilt_deg=0, squash=1.0, stretch=1.0):
    """Return (top, right, bot, left) of Glitch's diamond body."""
    ry_eff = int(ry * squash * stretch)
    tilt = math.radians(tilt_deg)
    top   = (cx + int(rx * 0.15 * math.sin(tilt)), cy - ry_eff + int(rx * 0.15 * math.cos(tilt)))
    right = (cx + int(rx * math.cos(-tilt)),        cy + int(rx * 0.2 * math.sin(-tilt)))
    bot   = (cx - int(rx * 0.15 * math.sin(tilt)),  cy + int(ry_eff * 1.15))
    left  = (cx - int(rx * math.cos(-tilt)),         cy - int(rx * 0.2 * math.sin(-tilt)))
    return top, right, bot, left


def draw_pixel_eye(draw, ex, ey, cell, glyph):
    """Draw a 3×3 pixel grid eye. Cell state map from glitch.md §6.1."""
    cell_colors = {
        0: VOID_BLACK, 1: CORRUPT_AMB_SH, 2: CORRUPT_AMB, 3: SOFT_GOLD,
        4: HOT_MAG, 5: ACID_GREEN, 6: UV_PURPLE, 7: (248, 246, 236),
    }
    for row in range(3):
        for col in range(3):
            color = cell_colors.get(glyph[row][col], VOID_BLACK)
            px = ex + col * cell
            py = ey + row * cell
            draw.rectangle([px, py, px + cell - 1, py + cell - 1], fill=color)


def destabilized_right_eye(left_glyph, seed=42):
    """Generate destabilized right eye (performance state — glitch.md §6.3)."""
    rng = random.Random(seed)
    right = []
    for row in left_glyph:
        new_row = []
        for state in row:
            if state == 3:
                new_row.append(rng.choice([1, 0]))
            elif state == 4:
                new_row.append(rng.choice([4, 0, 0]))
            elif state == 5:
                new_row.append(rng.choice([5, 0, 5]))
            else:
                new_row.append(state)
        right.append(new_row)
    return right


def draw_confetti(draw, cx, cy_spike_tip, colors, count, spread, seed=7):
    """Scatter pixel confetti below bottom spike tip."""
    rng = random.Random(seed)
    for _ in range(count):
        dx = rng.randint(-spread, spread)
        dy = rng.randint(0, int(spread * 0.8))
        px, py = cx + dx, cy_spike_tip + dy + 4
        sz = rng.choice([2, 3, 2])
        draw.rectangle([px, py, px + sz, py + sz], fill=rng.choice(colors))


def draw_glitch_figure(draw, cx, cy,
                       rx=RX, ry=RY,
                       tilt_deg=0,
                       squash=1.0,
                       stretch=1.0,
                       spike_h=10,
                       arm_l_dy=0,
                       arm_r_dy=0,
                       arm_l_extend=0,   # extra extension on left arm-spike tip
                       arm_r_extend=0,   # extra extension on right arm-spike tip
                       left_eye_glyph=None,
                       bilateral=False,
                       confetti_colors=None,
                       confetti_count=8,
                       confetti_spread=24,
                       confetti_seed=7,
                       crack_bright=False):  # B3: crack line brightened
    """
    Draw Glitch as a geometric construction figure.
    cx, cy = body center. Glitch hovers — no ground contact.
    Returns (top, right, bot, left, cy_top, cy_bot).
    """
    if left_eye_glyph is None:
        left_eye_glyph = [[0, 2, 0], [2, 1, 2], [0, 2, 0]]

    ry_eff = int(ry * squash * stretch)
    tilt_off = int(tilt_deg * 0.4)  # spike lean follows body

    top, right, bot, left = diamond_pts(cx, cy, rx, ry, tilt_deg, squash, stretch)
    cy_bot = bot[1]
    cy_top = top[1]
    spike_tip_y = cy_bot + spike_h + 4

    # 1. Confetti (below bottom spike — drawn first)
    if confetti_colors and confetti_count > 0:
        draw_confetti(draw, cx, spike_tip_y, confetti_colors, confetti_count,
                      confetti_spread, confetti_seed)

    # 2. Bottom spike (3-point downward triangle — hover point)
    bsp = [(cx - spike_h // 2, cy_bot), (cx + spike_h // 2, cy_bot),
           (cx, spike_tip_y)]
    draw.polygon(bsp, fill=CORRUPT_AMB_SH, outline=VOID_BLACK)

    # 3. Body shadow (UV_PURPLE, offset +3 right, +4 down)
    shadow_pts = [(p[0] + 3, p[1] + 4) for p in [top, right, bot, left]]
    draw.polygon(shadow_pts, fill=UV_PURPLE)

    # 4. Body fill (CORRUPT_AMBER — canonical)
    body_pts = [top, right, bot, left]
    draw.polygon(body_pts, fill=CORRUPT_AMB)

    # 5. Highlight facet (upper-left triangle)
    ctr_hl = (cx, cy - ry_eff // 4)
    mid_tl = ((top[0] + left[0]) // 2, (top[1] + left[1]) // 2)
    draw.polygon([top, ctr_hl, mid_tl], fill=CORRUPT_AMB_HL)

    # 6. Outline
    draw.polygon(body_pts, outline=VOID_BLACK, width=3)

    # 7. HOT_MAG crack + fork (ALWAYS visible — G004)
    crack_color = SOFT_GOLD if crack_bright else HOT_MAG  # brightened in B3 surge
    crack_w = 3 if crack_bright else 2
    cs = (cx - rx // 2, cy - ry_eff // 3)
    ce = (cx + rx // 3, cy + ry_eff // 2)
    draw.line([cs, ce], fill=crack_color, width=crack_w)
    mid_c = ((cs[0] + ce[0]) // 2, (cs[1] + ce[1]) // 2)
    fork = (cx + rx // 2, cy - ry_eff // 4)
    draw.line([mid_c, fork], fill=crack_color, width=max(1, crack_w - 1))

    # 8. Arm-spikes (geometric body extensions from left/right vertices)
    ax_l = left[0] - 6
    ay_l = left[1] + arm_l_dy
    tip_l = (ax_l - 14 - arm_l_extend + int(tilt_deg * 0.3), ay_l - 8)
    draw.polygon([(ax_l, ay_l - 5), (ax_l, ay_l + 5), tip_l],
                 fill=CORRUPT_AMB, outline=VOID_BLACK)

    ax_r = right[0] + 6
    ay_r = right[1] + arm_r_dy
    tip_r = (ax_r + 14 + arm_r_extend + int(tilt_deg * 0.3), ay_r - 8)
    draw.polygon([(ax_r, ay_r - 5), (ax_r, ay_r + 5), tip_r],
                 fill=CORRUPT_AMB, outline=VOID_BLACK)

    # 9. Face (pixel eyes — glitch.md §6.4)
    face_cy = cy - ry_eff // 6
    cell = 7   # larger than expression sheet for motion doc readability
    leye_x = cx - rx // 2 - cell * 3 // 2
    leye_y = face_cy - cell * 3 // 2
    reye_x = cx + rx // 2 - cell * 3 // 2
    reye_y = face_cy - cell * 3 // 2

    draw_pixel_eye(draw, leye_x, leye_y, cell, left_eye_glyph)
    right_glyph = left_eye_glyph if bilateral else destabilized_right_eye(left_eye_glyph)
    draw_pixel_eye(draw, reye_x, reye_y, cell, right_glyph)

    # 10. Top spike (5-point crown — leans with body tilt)
    sx = cx + tilt_off
    tsp = [
        (sx - spike_h // 2, cy_top),
        (sx - spike_h,       cy_top - spike_h),
        (sx,                  cy_top - spike_h * 2),   # tip
        (sx + spike_h,        cy_top - spike_h),
        (sx + spike_h // 2,   cy_top),
    ]
    draw.polygon(tsp, fill=CORRUPT_AMB, outline=VOID_BLACK)
    if spike_h >= 6:
        tip_x, tip_y = sx, cy_top - spike_h * 2
        draw.line([(tip_x, tip_y - 3), (tip_x, tip_y - 6)], fill=HOT_MAG, width=2)

    return top, right, bot, left, cy_top, cy_bot


# ------------------------------------------------------------------ beat badge + frame

def draw_beat_badge(draw, ox, oy, beat_num, label):
    """Amber beat badge in upper-left of panel, expression label below."""
    bx, by = ox + 6, oy + 6
    badge_text = f"B{beat_num}"
    bbox = draw.textbbox((0, 0), badge_text)
    bw = bbox[2] - bbox[0] + 12
    bh = bbox[3] - bbox[1] + 8
    draw.rectangle([bx, by, bx + bw, by + bh], fill=BEAT_COLOR)
    draw.text((bx + 6, by + 4), badge_text, fill=VOID_BLACK)
    draw.text((bx, by + bh + 4), label, fill=CORRUPT_AMB)


def draw_panel_frame(draw, ox, oy, pw, ph):
    draw.rectangle([ox, oy, ox + pw, oy + ph], outline=PANEL_BORDER, width=2)


# ===================================================================== panels

def draw_panel_b1(img, draw, col):
    """B1: PREDATORY STILL — absolute stillness. No hover, no confetti. Wrongness = absence of motion."""
    ox, oy = panel_origin(col)
    pw, ph = PANEL_W, PANEL_H
    cx = ox + pw // 2
    cy = oy + int(ph * 0.44)

    # Neutral eye glyph (calculating: perfectly still — control read)
    # CALCULATING eye = acid-X (same as mischievous per glitch.md §6.2)
    calculating_eye = [[5, 0, 5], [0, 5, 0], [5, 0, 5]]

    top, right, bot, left, cy_top, cy_bot = draw_glitch_figure(
        draw, cx, cy,
        tilt_deg=0,
        squash=1.0, stretch=1.0,
        spike_h=10,
        arm_l_dy=0, arm_r_dy=0,
        left_eye_glyph=calculating_eye,
        bilateral=False,   # performance — asymmetric eyes
        confetti_colors=None,
        confetti_count=0,
    )

    # NO HOVER INDICATOR — stillness is the annotation
    # Crossed-out oscillation symbol (explicit: NOT hovering)
    hx, hy = cx - 52, oy + 22
    draw.text((hx, hy), "NO HOVER", fill=HOT_MAG)
    draw.text((hx, hy + 14), "NO CONFETTI", fill=HOT_MAG)

    # Static lines = held / frozen (light construction marks)
    for i in range(3):
        draw.line([(cx - 50, cy - 10 + i * 10), (cx - 46, cy - 10 + i * 10)],
                  fill=ACCENT_DASH, width=1)
        draw.line([(cx + 46, cy - 10 + i * 10), (cx + 50, cy - 10 + i * 10)],
                  fill=ACCENT_DASH, width=1)

    # Spike still annotation
    annot_text(draw, cx + 8, cy_top - 12, "spike_h=10", color=CORRUPT_AMB)

    # Duration annotation
    annot_text(draw, ox + 6, oy + ph - 54, "tilt: 0\u00b0  squash: 1.0", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 40, "duration: HELD (indefinite)", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 26, "eyes: acid-X (CALCULATING)", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 12, "wrongness = absence of idle motion", color=CORRUPT_AMB)

    draw_beat_badge(draw, ox, oy, 1, "PREDATORY STILL")
    draw_panel_frame(draw, ox, oy, pw, ph)


def draw_panel_b2(img, draw, col):
    """B2: COVETOUS REACH — desire-state. Slow extension of right arm toward subject."""
    ox, oy = panel_origin(col)
    pw, ph = PANEL_W, PANEL_H
    cx = ox + pw // 2
    cy = oy + int(ph * 0.44)

    # Covetous eye: acid slit top row — target lock
    # Interior state: BILATERAL eyes (glitch.md §6.3 — G008)
    covetous_eye = [[5, 5, 5], [0, 5, 0], [0, 0, 0]]

    top, right, bot, left, cy_top, cy_bot = draw_glitch_figure(
        draw, cx, cy,
        tilt_deg=12,         # leans toward subject (covetous lean: +12° per glitch.md §5)
        squash=1.0, stretch=1.0,
        spike_h=12,          # covetous: 12 per glitch.md §3.1
        arm_l_dy=18,         # left arm low (hanging — yearning weight)
        arm_r_dy=-6,         # right arm slightly raised (reaching)
        arm_r_extend=14,     # RIGHT arm extends toward subject (+14px extension)
        left_eye_glyph=covetous_eye,
        bilateral=True,      # INTERIOR STATE — G008 bilateral (glitch.md §6.3)
        confetti_colors=[UV_PURPLE, UV_PURPLE, CORRUPT_AMB_SH],  # minimal UV only
        confetti_count=4,
        confetti_spread=18,
        confetti_seed=33,
    )

    # Slow arc arrow on extending right arm — smooth, long reach
    draw_arrow(draw, right[0] + 16, right[1] - 6,
               right[0] + 48, right[1] - 22,
               color=MOTION_ARROW, width=2, head=7)
    annot_text(draw, right[0] + 32, right[1] - 36, "SLOW extend", color=MOTION_ARROW)
    annot_text(draw, right[0] + 32, right[1] - 22, "toward subject", color=ANNOT_TEXT)

    # Bilateral eye callout (key character read)
    annot_text(draw, ox + 6, cy_top - 48, "BILATERAL eyes:", color=SOFT_GOLD)
    annot_text(draw, ox + 6, cy_top - 34, "acid-slit both sides", color=ACID_GREEN)
    annot_text(draw, ox + 6, cy_top - 20, "= REAL interior state", color=ANNOT_TEXT)

    # Speed annotation
    annot_text(draw, ox + 6, oy + ph - 54, "tilt: +12\u00b0 (toward subject)", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 40, "speed: very slow, smooth arc", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 26, "confetti: UV_PURPLE only (4px)", color=UV_PURPLE)
    annot_text(draw, ox + 6, oy + ph - 12, "right arm-spike: extended +14px toward subject", color=ANNOT_TEXT)

    draw_beat_badge(draw, ox, oy, 2, "COVETOUS REACH")
    draw_panel_frame(draw, ox, oy, pw, ph)


def draw_panel_b3(img, draw, col):
    """B3: CORRUPTION SURGE — body scale pulses ±15%, jittery. Crack brightens."""
    ox, oy = panel_origin(col)
    pw, ph = PANEL_W, PANEL_H
    cx = ox + pw // 2
    cy = oy + int(ph * 0.44)

    # Panicked eye: full HOT ring
    panicked_eye = [[4, 4, 4], [4, 0, 4], [4, 4, 4]]

    # B3: SURGE state — stretched body (showing +15% size pulse)
    top, right, bot, left, cy_top, cy_bot = draw_glitch_figure(
        draw, cx, cy,
        tilt_deg=0,
        squash=1.0, stretch=1.15,   # +15% body size at surge peak
        spike_h=16,                  # spike_h increases during surge
        arm_l_dy=-14, arm_r_dy=-16, # both arms flung out (panic)
        left_eye_glyph=panicked_eye,
        bilateral=False,   # panicked = performance (uncontrolled)
        confetti_colors=[HOT_MAG, UV_PURPLE],
        confetti_count=18,
        confetti_spread=36,
        confetti_seed=55,
        crack_bright=True,  # crack brightened during surge
    )

    # Ghost body at neutral scale (dashed outline — before surge)
    neutral_ry_eff = int(RY * 1.0)
    ghost_top_y = cy - neutral_ry_eff
    ghost_bot_y = cy + int(neutral_ry_eff * 1.15)
    draw.line([(cx, ghost_top_y), (cx, ghost_top_y - 20 * 2)], fill=ACCENT_DASH, width=1)
    annot_text(draw, cx + 6, ghost_top_y - 8, "neutral top (ghost)", color=ACCENT_DASH)

    # Scale pulse arrows (expand and compress — staccato)
    draw_arrow(draw, cx - RX - 30, cy, cx - RX - 50, cy,
               color=BEAT_COLOR, width=2, head=6)
    draw_arrow(draw, cx + RX + 30, cy, cx + RX + 50, cy,
               color=BEAT_COLOR, width=2, head=6)
    annot_text(draw, cx - RX - 78, cy + 6, "\u00b115%", color=CORRUPT_AMB)

    # Crack brightened callout
    annot_text(draw, ox + 6, cy_top - 24, "crack brightens:", color=SOFT_GOLD)
    annot_text(draw, ox + 6, cy_top - 10, "HOT_MAG \u2192 SOFT_GOLD arc", color=SOFT_GOLD)

    # Jitter annotation (not drawn — temporal, described in text)
    annot_text(draw, ox + 6, oy + ph - 54, "body: \u00b115% scale pulse, staccato fast", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 40, "spike_h=16 (elevated energy — loss of control)", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 26, "confetti: HOT_MAG+UV_PURPLE max (18px)", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 12, "jitter: body oscillation x+y ±4px per frame", color=CORRUPT_AMB)

    draw_beat_badge(draw, ox, oy, 3, "CORRUPTION SURGE")
    draw_panel_frame(draw, ox, oy, pw, ph)


def draw_panel_b4(img, draw, col):
    """B4: RETREAT — rapid compression + backward displacement. Coil-back, not defeat."""
    ox, oy = panel_origin(col)
    pw, ph = PANEL_W, PANEL_H
    cx = ox + pw // 2 + 20   # displaced right (retreating to viewer's right = away from subject)
    cy = oy + int(ph * 0.47)  # shifted down slightly for squash display

    # Stunned eye: full HOT_MAG — overloaded
    stunned_eye = [[4, 4, 4], [4, 4, 4], [4, 4, 4]]

    top, right, bot, left, cy_top, cy_bot = draw_glitch_figure(
        draw, cx, cy,
        tilt_deg=-20,   # hard recoil away from subject (stunned: -18° per glitch.md §5)
        squash=0.65,    # compressed on impact (between retreat 0.65 and panicked 0.55)
        stretch=1.0,
        spike_h=6,      # compressed under stress
        arm_l_dy=8, arm_r_dy=10,   # both slightly dropped (defensive, not fully dropped)
        left_eye_glyph=stunned_eye,
        bilateral=False,   # stunned = performance
        confetti_colors=[HOT_MAG, UV_PURPLE, CORRUPT_AMB_SH],
        confetti_count=14,
        confetti_spread=30,
        confetti_seed=77,
    )

    # Displacement direction arrow (backward = to the right in this composition)
    draw_arrow(draw, cx - 50, cy - 30, cx - 80, cy - 30,
               color=BEAT_COLOR, width=2, head=7)
    annot_text(draw, cx - 110, cy - 44, "backward", color=CORRUPT_AMB)
    annot_text(draw, cx - 114, cy - 30, "displacement", color=ANNOT_TEXT)

    # Squash annotation
    annot_text(draw, cx + 6, cy_top + 4, "squash=0.65", color=CORRUPT_AMB)

    # Danger callout — still dangerous
    annot_text(draw, ox + 6, oy + ph - 54, "tilt: -20\u00b0 (recoil away from subject)", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 40, "squash: 0.65 — compressed, not flattened", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 26, "speed: RAPID (1-2 frames to full compression)", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 12, "reads as COIL-BACK not defeat — still dangerous", color=CORRUPT_AMB)

    draw_beat_badge(draw, ox, oy, 4, "RETREAT")
    draw_panel_frame(draw, ox, oy, pw, ph)


# ===================================================================== main

def build_sheet():
    img = Image.new("RGB", (W, H), VOID_BLACK)
    draw = ImageDraw.Draw(img)

    # --- Header ---
    draw.rectangle([0, 0, W, _GLITCH_PANEL_TOP - 1], fill=(18, 12, 28))
    draw.text((PAD, 8), "GLITCH \u2014 Motion Spec Sheet", fill=CORRUPT_AMB)
    draw.text((PAD, 24),
              "Ryo Hasegawa / C45  |  Beat arc: PREDATORY STILL \u2192 COVETOUS REACH \u2192 CORRUPTION SURGE \u2192 RETREAT",
              fill=ANNOT_TEXT)
    draw.text((PAD, 38),
              "Amber arrows = secondary motion.  Amber badge = beat timing.  BILATERAL eyes = interior state (G008).  CORRUPT_AMBER body (glitch.md canonical).",
              fill=ACCENT_DASH)

    # --- Panel backgrounds ---
    for col in range(COLS):
        ox, oy = panel_origin(col)
        draw.rectangle([ox, oy, ox + PANEL_W, oy + PANEL_H], fill=(14, 10, 22))

    # --- Draw panels ---
    draw_panel_b1(img, draw, 0)
    draw_panel_b2(img, draw, 1)
    draw_panel_b3(img, draw, 2)
    draw_panel_b4(img, draw, 3)

    # --- Size guard ---
    img.thumbnail((1280, 1280))

    # --- Save ---
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "characters", "motion")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_glitch_motion.png")
    img.save(out_path)
    print(f"Saved: {out_path}  ({img.width}x{img.height})")
    return out_path


if __name__ == "__main__":
    build_sheet()
