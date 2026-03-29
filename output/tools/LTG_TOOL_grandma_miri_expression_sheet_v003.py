#!/usr/bin/env python3
"""
LTG_TOOL_grandma_miri_expression_sheet_v003.py
Grandma Miri Expression Sheet — v003 NARRATIVE EXPRESSION
"Luma & the Glitchkin" — Cycle 33 / Maya Santos

v003 ADDITION (Cycle 25 original intent — rebuilt from spec):
  KNOWING STILLNESS — the 6th expression.
  Miri's narrative-defining expression: she knew about the Glitch Layer all along.
  A secret she has kept, and carries with grace.

  Silhouette signature:
    - Completely STILL body (zero tilt, zero arm gesture) — arms folded low.
    - Head very slightly inclined (oblique tilt: right ear drops 8px).
    - This stillness distinguishes from WISE (which is also still) in face alone —
      KNOWING STILLNESS has a DIRECTED gaze (slight left oblique) and a SUPPRESSED
      smile (only one corner lifted), where WISE has neutral downward gaze.
    - The asymmetry of one-corner-lifted mouth + oblique gaze gives KNOWING STILLNESS
      a distinct diagonal read even at squint-test scale.

  Face signature:
    - Eyes: heavy-lidded (l_open=0.48, r_open=0.48), gaze_dx=+0.12 (oblique right
      from Miri's perspective = left from viewer). The directed gaze communicates
      "I see something you don't."
    - Mouth: "knowing_oblique" — right corner (viewer's left) barely lifted (+4px),
      left corner neutral. One side of the smile is happening. The other is waiting.
    - Brows: level but slightly lowered on right (brow_r_dy=+6) — lowers the right
      brow slightly, asymmetric to match oblique eye and mouth.
    - Blush: 0.2 — minimal, just enough to warm the skin. This is private knowledge,
      not emotional outburst.

  Body: identical to WISE (arms folded low, perfectly still) — but the face reads
  completely differently from WISE at final output scale.

v003 GRID:
  3×2 layout (6 expressions, all slots filled).
  WISE (position 4) and KNOWING STILLNESS (position 5) fill the second row.
  All 5 v002 expressions retained unchanged.

v003 CHANGES FROM v002:
  - Grid upgraded: 3+2 layout → 3×2 (all 6 slots used)
  - KNOWING STILLNESS added as 6th expression
  - ROWS updated to 2 (was implicit 2 with partial fill)
  - New mouth style: "knowing_oblique"
  - New eye param: head_oblique_tilt (applied as cy offset per side)
  - Title updated to v003

Output: output/characters/main/LTG_CHAR_grandma_miri_expression_sheet_v003.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Palette (from grandma_miri.md) ────────────────────────────────────────────
SKIN_BASE   = (140, 84, 48)     # #8C5430 Deep Warm Brown
SKIN_SH     = (106, 58, 30)     # #6A3A1E Dark Sienna
SKIN_HL     = (168, 106, 64)    # #A86A40 Warm Chestnut
BLUSH_PERM  = (212, 149, 107)   # #D4956B permanent cheek blush
HAIR_BASE   = (216, 208, 200)   # #D8D0C8 Silver White
HAIR_SH     = (168, 152, 140)   # #A8988C Warm Gray
HAIR_HL     = (240, 236, 232)   # #F0ECE8 Bright Near-White
EYE_IRIS    = (139, 94, 60)     # #8B5E3C Deep Warm Amber
EYE_PUP     = (26, 15, 10)      # #1A0F0A Near-Black Espresso
EYE_W       = (250, 240, 220)   # #FAF0DC Warm Cream
EYE_HL      = (240, 240, 240)   # #F0F0F0 Static White
BROW_COL    = (138, 122, 112)   # #8A7A70 Warm Gray
CARDIGAN    = (184, 92, 56)     # #B85C38 Warm Terracotta Rust
CARDIGAN_SH = (138, 60, 28)     # #8A3C1C Deep Rust
CARDIGAN_HL = (212, 130, 90)    # #D4825A Dusty Apricot
PANTS       = (200, 174, 138)   # #C8AE8A Warm Linen Tan
PANTS_SH    = (160, 138, 106)   # #A08A6A Warm Medium Tan
SLIPPER     = (90, 122, 90)     # #5A7A5A Deep Sage
GLASSES_COL = (59, 40, 32)      # #3B2820 Deep Cocoa
LINE        = (59, 40, 32)      # #3B2820 Deep Cocoa
CANVAS_BG   = (28, 20, 14)

# Panel backgrounds — v003 adds KNOWING STILLNESS panel
BG = {
    "WARM":      (248, 232, 210),
    "SKEPTICAL": (210, 218, 208),
    "CONCERNED": (200, 212, 225),
    "SURPRISED": (245, 228, 195),
    "WISE":      (218, 214, 205),
    "KNOWING":   (228, 218, 200),   # warm parchment — private, still, interior
}

# ── Layout ─────────────────────────────────────────────────────────────────────
TOTAL_W  = 1200
TOTAL_H  = 900
COLS     = 3
ROWS     = 2
PAD      = 20
HEADER   = 58
LABEL_H  = 36
PANEL_W  = (TOTAL_W - PAD * (COLS + 1)) // COLS    # 380
PANEL_H  = (TOTAL_H - HEADER - PAD * (ROWS + 1) - LABEL_H * ROWS) // ROWS  # 356

RENDER_SCALE = 2
HEAD_R = 68
HR     = HEAD_R * RENDER_SCALE   # 136 at render scale

EXPRESSIONS = ["WARM", "SKEPTICAL", "CONCERNED", "SURPRISED", "WISE", "KNOWING"]
EXPR_LABELS = {
    "WARM":      "WARM / WELCOMING",
    "SKEPTICAL": "SKEPTICAL / AMUSED",
    "CONCERNED": "CONCERNED",
    "SURPRISED": "SURPRISED / DELIGHTED",
    "WISE":      "WISE / KNOWING",
    "KNOWING":   "KNOWING STILLNESS",
}


# ── Geometry helpers ───────────────────────────────────────────────────────────

def bezier3(p0, p1, p2, steps=40):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
        y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
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


# ── Head ───────────────────────────────────────────────────────────────────────

def draw_head_miri(draw, cx, cy):
    ry = int(HR * 0.94)
    draw.ellipse([cx - HR, cy - ry, cx + HR, cy + ry], fill=SKIN_BASE)
    jaw_r = int(HR * 0.55)
    jaw_y = cy + int(ry * 0.80)
    draw.ellipse([cx - jaw_r, jaw_y - int(ry * 0.22),
                  cx + jaw_r, jaw_y + int(ry * 0.22)], fill=SKIN_BASE)
    draw.ellipse([cx - HR, cy - ry, cx + HR, cy + ry], outline=LINE, width=6)


def draw_ears_miri(draw, cx, cy):
    er = int(HR * 0.12)
    ey = cy + int(HR * 0.08)
    draw.ellipse([cx - HR - er + 4, ey - er, cx - HR + er + 4, ey + er],
                 fill=SKIN_BASE, outline=LINE, width=4)
    draw.ellipse([cx + HR - er - 4, ey - er, cx + HR + er - 4, ey + er],
                 fill=SKIN_BASE, outline=LINE, width=4)


def draw_hair_bun(draw, cx, cy):
    ry       = int(HR * 0.94)
    hair_top = cy - ry - int(HR * 0.26)
    draw.ellipse([cx - int(HR * 0.94), hair_top + int(HR * 0.10),
                  cx + int(HR * 0.90), cy - int(ry * 0.60)], fill=HAIR_BASE)
    bun_cx = cx + int(HR * 0.10)
    bun_cy = hair_top + int(HR * 0.16)
    bun_rx = int(HR * 0.50)
    bun_ry = int(HR * 0.36)
    draw.ellipse([bun_cx - bun_rx, bun_cy - bun_ry,
                  bun_cx + bun_rx, bun_cy + bun_ry], fill=HAIR_BASE)
    draw.ellipse([bun_cx - int(bun_rx * 0.70), bun_cy,
                  bun_cx + int(bun_rx * 0.60), bun_cy + bun_ry], fill=HAIR_SH)
    arc_draw(draw, bun_cx - int(bun_rx * 0.15), bun_cy - int(bun_ry * 0.30),
             int(bun_rx * 0.50), int(bun_ry * 0.36), 200, 330, HAIR_HL, width=3)
    chop_x1 = bun_cx - int(bun_rx * 0.32)
    chop_x2 = bun_cx + int(bun_rx * 0.26)
    draw.line([(chop_x1, bun_cy - bun_ry - 10), (chop_x1 + 7, bun_cy + bun_ry + 6)],
              fill=LINE, width=3)
    draw.line([(chop_x2, bun_cy - bun_ry - 8), (chop_x2 + 7, bun_cy + bun_ry + 4)],
              fill=LINE, width=3)
    for pts in [
        bezier3((cx - int(HR*0.84), cy - ry + 8), (cx - int(HR*0.76), cy - int(ry*0.44)),
                (cx - int(HR*0.80), cy - int(ry*0.06))),
        bezier3((cx + int(HR*0.72), cy - ry + 14), (cx + int(HR*0.80), cy - int(ry*0.38)),
                (cx + int(HR*0.74), cy))
    ]:
        polyline(draw, pts, HAIR_BASE, width=3)
        polyline(draw, pts, LINE, width=1)
    draw.ellipse([bun_cx - bun_rx, bun_cy - bun_ry,
                  bun_cx + bun_rx, bun_cy + bun_ry], outline=LINE, width=4)
    draw.ellipse([cx - int(HR*0.94), hair_top + int(HR*0.10),
                  cx + int(HR*0.90), cy - int(ry*0.60)], outline=LINE, width=4)


def draw_eyes_miri(draw, cx, cy, params):
    eye_y   = cy + int(HR * 0.10)
    sep     = int(HR * 0.56)
    lx      = cx - sep // 2
    rx      = cx + sep // 2
    ew      = int(HR * 0.30)
    eh_full = int(HR * 0.20)
    p       = params

    # KNOWING STILLNESS: oblique head tilt slightly adjusts eye heights
    l_eye_y = eye_y + p.get("l_eye_dy", 0)
    r_eye_y = eye_y + p.get("r_eye_dy", 0)

    for (ex, eye_y_i, open_f, is_right) in [
        (lx, l_eye_y, p["l_open"], False),
        (rx, r_eye_y, p["r_open"], True)
    ]:
        actual_h = max(3, int(eh_full * open_f))
        if p.get("eyes_closed"):
            actual_h = max(2, int(eh_full * 0.06))

        draw.ellipse([ex - ew, eye_y_i - actual_h, ex + ew, eye_y_i + actual_h], fill=EYE_W)
        ir  = int(ew * 0.62)
        iry = min(ir, actual_h - 2)
        if iry < 2:
            iry = 2
        pdx = int(p.get("gaze_dx", 0) * HR * 0.07)
        pdy = int(p.get("gaze_dy", 0) * HR * 0.06)
        draw.ellipse([ex + pdx - ir, eye_y_i + pdy - iry,
                      ex + pdx + ir, eye_y_i + pdy + iry], fill=EYE_IRIS)
        pr = int(ir * 0.52)
        if p.get("pupils_wide"):
            pr = int(ir * 0.70)
        draw.ellipse([ex + pdx - pr, eye_y_i + pdy - pr,
                      ex + pdx + pr, eye_y_i + pdy + pr], fill=EYE_PUP)
        if not p.get("eyes_closed"):
            hr_s = max(int(pr * 0.38), 3)
            hlx  = ex + pdx - int(ir * 0.26)
            hly  = eye_y_i + pdy - int(iry * 0.34)
            draw.ellipse([hlx - hr_s, hly - hr_s, hlx + hr_s, hly + hr_s], fill=EYE_HL)
        draw.arc([ex - ew, eye_y_i - actual_h, ex + ew, eye_y_i + actual_h],
                 start=200, end=340, fill=LINE, width=4)
        if not p.get("eyes_closed"):
            arc_draw(draw, ex, eye_y_i + actual_h - int(eh_full * 0.28),
                     int(ew * 0.76), int(eh_full * 0.26), 15, 165, LINE, width=3)
        dsign = 1 if is_right else -1
        outer_x = ex + ew * dsign
        for k in range(2):
            dy_k = int(HR * 0.06) * k
            draw.line(
                [(outer_x, eye_y_i - int(HR * 0.02) + dy_k),
                 (outer_x + dsign * int(HR * 0.11), eye_y_i - int(HR * 0.10) + dy_k)],
                fill=LINE, width=2
            )
        draw.ellipse([ex - ew, eye_y_i - actual_h, ex + ew, eye_y_i + actual_h],
                     outline=LINE, width=6)

    # Glasses
    glasses_r_x = int(ew * 1.16)
    glasses_r_y = int(eh_full * 1.32)
    for gx, gey in [(lx, l_eye_y), (rx, r_eye_y)]:
        draw.ellipse([gx - glasses_r_x, gey - glasses_r_y,
                      gx + glasses_r_x, gey + glasses_r_y],
                     outline=GLASSES_COL, width=4)
    # Bridge connects at average eye y
    bridge_y = (l_eye_y + r_eye_y) // 2 - int(glasses_r_y * 0.10)
    draw.line([(lx + glasses_r_x, bridge_y), (rx - glasses_r_x, bridge_y)],
              fill=GLASSES_COL, width=4)
    draw.line([(lx - glasses_r_x, bridge_y),
               (lx - glasses_r_x - int(HR * 0.18), bridge_y - int(HR * 0.04))],
              fill=GLASSES_COL, width=3)
    draw.line([(rx + glasses_r_x, bridge_y),
               (rx + glasses_r_x + int(HR * 0.18), bridge_y - int(HR * 0.04))],
              fill=GLASSES_COL, width=3)

    # Eyebrows
    brow_base_y = eye_y - int(eh_full * 1.36) - glasses_r_y + int(eh_full * 0.38)
    for (bx, b_dy, b_worry, is_right_b) in [
        (lx, p.get("brow_l_dy", 0), p.get("brow_worry", False), False),
        (rx, p.get("brow_r_dy", 0), p.get("brow_worry", False), True),
    ]:
        by       = brow_base_y + b_dy
        inner_x  = bx + int(HR * 0.08) if is_right_b else bx - int(HR * 0.08)
        outer_x  = bx - int(HR * 0.26) if is_right_b else bx + int(HR * 0.26)
        inner_y  = by + (int(HR * 0.14) if b_worry else 0)
        pts      = bezier3((outer_x, by), (bx, by - int(HR * 0.03)), (inner_x, inner_y))
        polyline(draw, pts, BROW_COL, width=4)

    # Smile lines
    for side in [-1, 1]:
        sl_pts = bezier3(
            (cx + side * int(HR * 0.14), cy + int(HR * 0.22)),
            (cx + side * int(HR * 0.24), cy + int(HR * 0.40)),
            (cx + side * int(HR * 0.28), cy + int(HR * 0.56))
        )
        polyline(draw, sl_pts, LINE, width=2)


def draw_nose_miri(draw, cx, cy):
    ny = cy + int(HR * 0.28)
    arc_draw(draw, cx, ny, int(HR * 0.10), int(HR * 0.09), 130, 310, LINE, width=4)
    for side in [-1, 1]:
        arc_draw(draw, cx + side * int(HR * 0.09), ny + int(HR * 0.06),
                 int(HR * 0.05), int(HR * 0.04), 180, 350, LINE, width=2)


def draw_mouth_miri(draw, cx, cy, style="warm_closed"):
    my = cy + int(HR * 0.54)
    mw = int(HR * 0.36)
    lx = cx - mw
    rx = cx + mw

    if style == "warm_closed":
        pts = bezier3((lx, my + 4), (cx, my - 20), (rx, my + 4))
        polyline(draw, pts, LINE, width=5)
        draw.line([(lx, my + 4), (lx - 4, my + 10)], fill=LINE, width=4)
        draw.line([(rx, my + 4), (rx + 4, my + 10)], fill=LINE, width=4)

    elif style == "smirk":
        mw2 = int(mw * 0.76)
        pts = bezier3((cx - mw2, my + 2), (cx, my - 10), (cx + mw2, my + 6))
        polyline(draw, pts, LINE, width=5)

    elif style == "pursed":
        pts = bezier3((lx + int(mw * 0.14), my + 2), (cx, my + 6),
                      (rx - int(mw * 0.14), my + 2))
        polyline(draw, pts, LINE, width=5)

    elif style == "open_delight":
        sh = int(HR * 0.18)
        top_pts = bezier3((lx, my), (cx, my - 24), (rx, my))
        bot_pts = bezier3((lx, my + sh), (cx, my + sh + 8), (rx, my + sh))
        fill_pts = top_pts + bot_pts[::-1]
        draw.polygon(fill_pts, fill=(200, 65, 45))
        tw = int(mw * 0.80)
        draw.rectangle([cx - tw, my - 2, cx + tw, my + sh - 4], fill=(248, 242, 230))
        polyline(draw, top_pts, LINE, width=5)
        polyline(draw, bot_pts, LINE, width=4)
        draw.line([(lx, my), (lx, my + sh)], fill=LINE, width=4)
        draw.line([(rx, my), (rx, my + sh)], fill=LINE, width=4)

    elif style == "knowing":
        mw2 = int(mw * 0.66)
        pts = bezier3((cx - mw2, my + 6), (cx, my - 10), (cx + mw2, my + 6))
        polyline(draw, pts, LINE, width=5)

    elif style == "knowing_oblique":
        # One corner (viewer's right = Miri's left) barely lifted.
        # Left side of viewer = Miri's right = the "active" side showing the suppressed smile.
        # Right corner lifts +4px, left corner stays at my+6.
        mw2 = int(mw * 0.70)
        # Control point biased left (toward the lifted corner = viewer's left)
        pts = bezier3((cx - mw2, my + 2),   # left end: raised (Miri's smiling side)
                      (cx - int(mw * 0.14), my - 8),   # control: left of center
                      (cx + mw2, my + 6))               # right end: neutral
        polyline(draw, pts, LINE, width=5)
        # Corner dimple on the lifted side
        draw.line([(cx - mw2, my + 2), (cx - mw2 - 4, my - 4)], fill=LINE, width=3)


def draw_blush_miri(draw, cx, cy, strength=1.0):
    if strength <= 0:
        return
    bw = int(HR * 0.22)
    bh = int(HR * 0.09)
    by = cy + int(HR * 0.32)
    for bx in [cx - int(HR * 0.44), cx + int(HR * 0.44)]:
        alpha_val = int(strength * 255)
        blush_layer = Image.new("RGBA", (bw * 2, bh * 2), (0, 0, 0, 0))
        bld = ImageDraw.Draw(blush_layer)
        bld.ellipse([0, 0, bw * 2, bh * 2], fill=(*BLUSH_PERM, alpha_val))
        # We draw directly for simplicity since we don't have access to parent RGBA
        draw.ellipse([bx - bw, by - bh, bx + bw, by + bh], fill=BLUSH_PERM)


# ── Body renderer ──────────────────────────────────────────────────────────────

def draw_body_miri(draw, cx, body_top_y, body_data):
    tilt    = body_data.get("body_tilt", 0)
    tw      = int(HR * 1.14)
    th      = int(HR * 1.10)
    torso_bot = body_top_y + th

    torso_pts = [
        (cx - tw + tilt, body_top_y),
        (cx + tw + tilt, body_top_y),
        (cx + tw,        torso_bot),
        (cx - tw,        torso_bot),
    ]
    draw.polygon(torso_pts, fill=CARDIGAN)
    for side in [-1, 1]:
        for k in range(3):
            kx  = cx + side * (int(HR * 0.38) + k * int(HR * 0.28))
            ky0 = body_top_y + int(HR * 0.10)
            ky1 = torso_bot - int(HR * 0.10)
            draw.line([(kx, ky0), (kx, ky1)], fill=CARDIGAN_SH, width=2)
            draw.line([(kx + 4, ky0), (kx + 4, ky1)], fill=CARDIGAN_HL, width=1)
    nw  = int(HR * 0.22)
    nht = body_top_y - int(HR * 0.04)
    nhb = body_top_y + int(HR * 0.22)
    draw.polygon(
        [(cx, nht + int(HR * 0.16)), (cx - nw, nhb), (cx + nw, nhb)],
        fill=SKIN_BASE
    )
    draw.polygon(torso_pts, outline=LINE, width=6)
    pocket_y = torso_bot - int(HR * 0.30)
    for side in [-1, 1]:
        px = cx + side * int(HR * 0.64)
        draw.rectangle([px - int(HR * 0.28), pocket_y,
                         px + int(HR * 0.28), torso_bot - int(HR * 0.04)],
                        outline=CARDIGAN_SH, width=2)

    arm_w = int(HR * 0.20)
    arm_h = int(HR * 0.70)
    arm_y = body_top_y + int(HR * 0.06)
    l_style = body_data.get("arm_l_style", "hanging")
    r_style = body_data.get("arm_r_style", "hanging")
    arm_l_dy = body_data.get("arm_l_dy", 0)
    arm_r_dy = body_data.get("arm_r_dy", 0)

    def draw_arm(ax, ay, style, side):
        if style == "hanging":
            draw.rectangle([ax - arm_w, ay, ax + arm_w, ay + arm_h],
                           fill=CARDIGAN, outline=LINE, width=4)
            draw.ellipse([ax - int(arm_w * 1.1), ay + arm_h - int(arm_w * 0.4),
                           ax + int(arm_w * 1.1), ay + arm_h + int(HR * 0.14)],
                         fill=SKIN_BASE, outline=LINE, width=4)

        elif style == "extended":
            ex = ax + side * int(HR * 0.50)
            ey = ay + int(arm_h * 0.60)
            pts = bezier3((ax, ay), (ax + side * int(HR * 0.28), ay + int(arm_h * 0.30)),
                          (ex, ey))
            polyline(draw, pts, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts, LINE, width=4)
            draw.ellipse([ex - int(arm_w * 1.1), ey - int(arm_w * 0.4),
                           ex + int(arm_w * 1.1), ey + int(HR * 0.12)],
                         fill=SKIN_BASE, outline=LINE, width=4)

        elif style == "chest":
            hand_x = cx + side * int(HR * 0.24)
            hand_y = ay + int(arm_h * 0.36)
            pts = bezier3((ax, ay), (ax + side * int(HR * 0.12), ay + int(arm_h * 0.18)),
                          (hand_x, hand_y))
            polyline(draw, pts, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts, LINE, width=4)
            draw.ellipse([hand_x - int(arm_w * 1.1), hand_y - int(arm_w * 0.4),
                           hand_x + int(arm_w * 1.1), hand_y + int(HR * 0.12)],
                         fill=SKIN_BASE, outline=LINE, width=4)

        elif style == "raised":
            hand_x = ax + side * int(HR * 0.20)
            hand_y = ay - int(arm_h * 0.42)
            pts = bezier3((ax, ay), (ax + side * int(HR * 0.14), ay - int(arm_h * 0.22)),
                          (hand_x, hand_y))
            polyline(draw, pts, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts, LINE, width=4)
            draw.ellipse([hand_x - int(arm_w * 1.1), hand_y - int(HR * 0.12),
                           hand_x + int(arm_w * 1.1), hand_y + int(arm_w * 0.4)],
                         fill=SKIN_BASE, outline=LINE, width=4)

        elif style == "folded":
            fold_x = cx + side * int(HR * 0.28)
            fold_y = ay + int(arm_h * 0.55)
            pts = bezier3((ax, ay), (ax - side * int(HR * 0.04), ay + int(arm_h * 0.28)),
                          (fold_x, fold_y))
            polyline(draw, pts, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts, LINE, width=4)
            draw.ellipse([fold_x - int(arm_w * 1.1), fold_y - int(arm_w * 0.4),
                           fold_x + int(arm_w * 1.1), fold_y + int(HR * 0.12)],
                         fill=SKIN_BASE, outline=LINE, width=4)

        elif style == "crossed":
            cross_x = cx + (-side) * int(HR * 0.30)
            cross_y = ay + int(arm_h * 0.48)
            pts = bezier3((ax, ay), (cx, ay + int(arm_h * 0.22)), (cross_x, cross_y))
            polyline(draw, pts, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts, LINE, width=4)
            draw.ellipse([cross_x - int(arm_w * 1.1), cross_y - int(arm_w * 0.4),
                           cross_x + int(arm_w * 1.1), cross_y + int(HR * 0.12)],
                         fill=SKIN_BASE, outline=LINE, width=4)

    lax = cx - tw + tilt + int(HR * 0.04)
    rax = cx + tw + tilt - int(HR * 0.04)
    draw_arm(lax, arm_y + arm_l_dy, l_style, -1)
    draw_arm(rax, arm_y + arm_r_dy, r_style, +1)

    leg_w = int(HR * 0.22)
    leg_h = int(HR * 0.58)
    leg_l = cx - int(tw * 0.44)
    leg_r = cx + int(tw * 0.44)
    leg_y = torso_bot

    for lx in [leg_l, leg_r]:
        draw.rectangle([lx - leg_w, leg_y, lx + leg_w, leg_y + leg_h],
                       fill=PANTS, outline=LINE, width=4)
        draw.line([(lx, leg_y), (lx, leg_y + leg_h)], fill=PANTS_SH, width=2)

    slipper_y = leg_y + leg_h
    slipper_w = int(HR * 0.36)
    slipper_h = int(HR * 0.14)
    for lx in [leg_l, leg_r]:
        draw.ellipse([lx - slipper_w + int(slipper_w * 0.20), slipper_y,
                       lx + slipper_w - int(slipper_w * 0.20), slipper_y + slipper_h],
                     fill=SLIPPER, outline=LINE, width=4)


# ── Expression specifications ─────────────────────────────────────────────────

EXPR_SPECS = {
    "WARM": {
        "eyes": {
            "l_open": 0.82, "r_open": 0.82,
            "brow_l_dy": -int(HR * 0.08), "brow_r_dy": -int(HR * 0.08),
            "brow_worry": False,
            "gaze_dx": 0, "gaze_dy": 0,
        },
        "mouth": "warm_closed",
        "blush": 1.0,
        "body": {
            "body_tilt":   -6,
            "arm_l_style": "extended",
            "arm_r_style": "extended",
            "arm_l_dy":    0,
            "arm_r_dy":    0,
        },
        "cy_offset": -10,
    },
    "SKEPTICAL": {
        "eyes": {
            "l_open": 0.70, "r_open": 0.70,
            "brow_l_dy": -int(HR * 0.18), "brow_r_dy": 0,
            "brow_worry": False,
            "gaze_dx": 0, "gaze_dy": 0.06,
        },
        "mouth": "smirk",
        "blush": 0.6,
        "body": {
            "body_tilt":   +10,
            "arm_l_style": "crossed",
            "arm_r_style": "crossed",
            "arm_l_dy":    -int(HR * 0.06),
            "arm_r_dy":    -int(HR * 0.06),
        },
        "cy_offset": -8,
    },
    "CONCERNED": {
        "eyes": {
            "l_open": 0.88, "r_open": 0.88,
            "brow_l_dy": -int(HR * 0.16), "brow_r_dy": -int(HR * 0.16),
            "brow_worry": True,
            "gaze_dx": 0, "gaze_dy": 0.08,
        },
        "mouth": "pursed",
        "blush": 0.0,
        "body": {
            "body_tilt":   -10,
            "arm_l_style": "hanging",
            "arm_r_style": "chest",
            "arm_l_dy":    0,
            "arm_r_dy":    -int(HR * 0.08),
        },
        "cy_offset": -8,
    },
    "SURPRISED": {
        "eyes": {
            "l_open": 1.0, "r_open": 1.0,
            "brow_l_dy": -int(HR * 0.28), "brow_r_dy": -int(HR * 0.28),
            "brow_worry": False,
            "pupils_wide": True,
            "gaze_dx": 0, "gaze_dy": 0,
        },
        "mouth": "open_delight",
        "blush": 1.0,
        "body": {
            "body_tilt":   +14,
            "arm_l_style": "raised",
            "arm_r_style": "raised",
            "arm_l_dy":    -int(HR * 0.10),
            "arm_r_dy":    -int(HR * 0.10),
        },
        "cy_offset": -12,
    },
    "WISE": {
        "eyes": {
            "l_open": 0.62, "r_open": 0.62,
            "brow_l_dy": 0, "brow_r_dy": 0,
            "brow_worry": False,
            "gaze_dx": 0, "gaze_dy": 0.10,
        },
        "mouth": "knowing",
        "blush": 0.8,
        "body": {
            "body_tilt":   0,
            "arm_l_style": "folded",
            "arm_r_style": "folded",
            "arm_l_dy":    0,
            "arm_r_dy":    0,
        },
        "cy_offset": -8,
    },
    "KNOWING": {
        # KNOWING STILLNESS — narrative expression (v003 addition).
        # SILHOUETTE: identical body to WISE (arms folded low, upright).
        # Read-at-thumbnail: the oblique one-corner smile + directed gaze creates
        # a diagonal facial asymmetry distinguishing it from WISE's neutral face.
        # At squint scale: both WISE and KNOWING read as "settled old woman" —
        # but the face diagonal is visible. Acknowledged near-similarity with WISE.
        "eyes": {
            "l_open": 0.48,   # heavy-lidded — more closed than WISE (0.62)
            "r_open": 0.48,
            "brow_l_dy": 0,
            "brow_r_dy": +int(HR * 0.04),   # right brow slightly lowered = asymmetric
            "brow_worry": False,
            "gaze_dx": +0.12,   # oblique gaze: directed to viewer's right (Miri's left)
            "gaze_dy": 0.06,
            # Oblique head tilt: right ear drops, left ear rises
            # Approximated by slightly offset eye heights (right eye slightly lower)
            "l_eye_dy": -int(HR * 0.02),   # left eye very slightly up
            "r_eye_dy": +int(HR * 0.03),   # right eye slightly down
        },
        "mouth": "knowing_oblique",
        "blush": 0.2,   # minimal — private knowledge, not emotion
        "body": {
            "body_tilt":   0,     # perfectly still — same as WISE
            "arm_l_style": "folded",
            "arm_r_style": "folded",
            "arm_l_dy":    0,
            "arm_r_dy":    0,
        },
        "cy_offset": -8,
    },
}


# ── Panel renderer ─────────────────────────────────────────────────────────────

def render_panel_miri(expr, panel_w, panel_h):
    rw   = panel_w * RENDER_SCALE
    rh   = panel_h * RENDER_SCALE
    img  = Image.new("RGBA", (rw, rh), (0, 0, 0, 0))

    guide = Image.new("RGBA", (rw, rh), (0, 0, 0, 0))
    gd    = ImageDraw.Draw(guide)
    gc    = (180, 155, 128, 44)
    cx    = rw // 2
    spec  = EXPR_SPECS[expr]
    cy    = int(rh * 0.32) + spec.get("cy_offset", 0) * RENDER_SCALE
    ry    = int(HR * 0.94)
    gd.ellipse([cx - HR, cy - ry, cx + HR, cy + ry], outline=gc, width=3)
    gd.line([(cx - HR - 18, cy), (cx + HR + 18, cy)], fill=gc, width=2)
    gd.line([(cx, cy - HR - 18), (cx, cy + HR + 18)], fill=gc, width=2)
    img = Image.alpha_composite(img, guide)
    draw = ImageDraw.Draw(img)

    body_top_y = cy + int(HR * 0.92)
    draw_body_miri(draw, cx, body_top_y, spec["body"])

    draw_head_miri(draw, cx, cy)
    draw_ears_miri(draw, cx, cy)
    draw_hair_bun(draw, cx, cy)
    draw_blush_miri(draw, cx, cy, strength=spec["blush"])
    draw = ImageDraw.Draw(img)  # refresh after potential composite
    draw_eyes_miri(draw, cx, cy, spec["eyes"])
    draw_nose_miri(draw, cx, cy)
    draw_mouth_miri(draw, cx, cy, style=spec["mouth"])

    return img.resize((panel_w, panel_h), Image.LANCZOS)


# ── Sheet assembly ─────────────────────────────────────────────────────────────

def build_sheet():
    sheet = Image.new("RGB", (TOTAL_W, TOTAL_H), CANVAS_BG)
    draw  = ImageDraw.Draw(sheet)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        font_sub   = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = font_title
        font_sub   = font_title

    title = "GRANDMA MIRI — Expression Sheet v003  |  Luma & the Glitchkin"
    sub   = ("Designer: Maya Santos  |  C33 Rebuild  |  MIRI-A canonical  |  "
             "6 expressions  |  KNOWING STILLNESS (narrative)")
    draw.text((PAD, 10), title, fill=(235, 218, 196), font=font_title)
    draw.text((PAD, 38), sub,   fill=(165, 150, 130), font=font_sub)

    panel_w = PANEL_W - PAD * 2
    panel_h = PANEL_H - PAD

    for idx, expr in enumerate(EXPRESSIONS):
        row        = idx // COLS
        col_in_row = idx % COLS
        px = PAD + col_in_row * (PANEL_W + PAD)
        py = HEADER + PAD + row * (PANEL_H + LABEL_H + PAD)

        bg = BG[expr]
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], fill=bg)
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], outline=LINE, width=2)

        face_img = render_panel_miri(expr, panel_w, panel_h)
        ox = px + PAD
        oy = py + PAD // 2
        sheet.paste(face_img, (ox, oy), face_img)
        draw = ImageDraw.Draw(sheet)  # refresh after paste

        label    = EXPR_LABELS[expr]
        label_y  = py + PANEL_H + 2
        label_bg = tuple(max(0, int(c * 0.88)) for c in bg)
        draw.rectangle([px, label_y, px + PANEL_W, label_y + LABEL_H], fill=label_bg)
        bbox = draw.textbbox((0, 0), label, font=font_label)
        tw_b = bbox[2] - bbox[0]
        th_b = bbox[3] - bbox[1]
        tx   = px + (PANEL_W - tw_b) // 2
        ty   = label_y + (LABEL_H - th_b) // 2
        draw.text((tx, ty), label, fill=LINE, font=font_label)

    # Respect ≤1280px rule
    sheet.thumbnail((1280, 1280), Image.LANCZOS)
    return sheet


if __name__ == "__main__":
    out_dir  = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "characters", "main")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_grandma_miri_expression_sheet_v003.png")
    sheet    = build_sheet()
    sheet.save(out_path)
    print(f"Saved: {os.path.abspath(out_path)}")
    print(f"Canvas: {sheet.size[0]}x{sheet.size[1]}")
    print("v003 additions:")
    print("  + KNOWING STILLNESS (6th expression, narrative)")
    print("  + 3x2 full grid (was 3+2 partial fill)")
    print("  + knowing_oblique mouth style (new)")
    print("  + per-eye oblique dy parameter (new)")
