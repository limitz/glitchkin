#!/usr/bin/env python3
"""
LTG_CHAR_grandma_miri_expression_sheet_v003.py
Grandma Miri Expression Sheet v003 — NARRATIVE EXPRESSION ADDITION
"Luma & the Glitchkin" — Cycle 25 / Maya Santos

v003 CHANGE: Critique 11 (Valentina) — Miri's five expressions show emotions but not
her character SECRET: she quietly knew about the Glitch Layer all along.
"At minimum one expression on the sheet should hint at this — a weighted glance,
a suppressed smile, a knowing stillness."

CHANGE FROM v002:
  - WISE/KNOWING slot replaced with two expressions: WISE kept + new KNOWING STILLNESS
  - Layout upgraded from 5-panel 3+2 to 6-panel 3×2 grid (1200×900, consistent standard)
  - New KNOWING STILLNESS expression:
    * Body: completely still, arms settled, upright — "I've been waiting for this"
    * Eyes: WEIGHTED GLANCE — gaze directed oblique/down, heavy-lidded, sees more than she shows
    * Mouth: SUPPRESSED SMILE — one corner very slightly lifted, restrained
    * Blush: very low (0.2) — warmth contained, not broadcasting
    * This is Miri's NARRATIVE EXPRESSION — she knew all along

show_guides=False for pitch export.

Output: output/characters/main/LTG_CHAR_grandma_miri_expression_sheet_v003.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Palette (canonical grandma_miri_color_model.md) ───────────────────────────
SKIN_BASE   = (140, 84, 48)
SKIN_SH     = (106, 58, 30)
SKIN_HL     = (168, 106, 64)
BLUSH_PERM  = (212, 149, 107)
HAIR_BASE   = (216, 208, 200)
HAIR_SH     = (168, 152, 140)
HAIR_HL     = (240, 236, 232)
EYE_IRIS    = (139, 94, 60)
EYE_PUP     = ( 26, 15, 10)
EYE_W       = (250, 240, 220)
EYE_HL      = (240, 240, 240)
BROW_COL    = (138, 122, 112)
CARDIGAN    = (184, 92, 56)
CARDIGAN_SH = (138, 60, 28)
CARDIGAN_HL = (212, 130, 90)
PANTS       = (200, 174, 138)
PANTS_SH    = (160, 138, 106)
SLIPPER     = ( 90, 122, 90)
GLASSES_COL = ( 59,  40, 32)
LINE        = ( 59,  40, 32)
CANVAS_BG   = ( 28,  20, 14)

BG = {
    "WARM":      (248, 232, 210),
    "SKEPTICAL": (210, 218, 208),
    "CONCERNED": (200, 212, 225),
    "SURPRISED": (245, 228, 195),
    "WISE":      (218, 214, 205),
    "KNOWING":   (215, 218, 212),   # slightly cooler than WISE — restrained, composed
}

# ── Layout (3×2, 6 panels, 1200×900) ──────────────────────────────────────────
TOTAL_W  = 1200
TOTAL_H  = 900
COLS     = 3
ROWS     = 2
PAD      = 20
HEADER   = 58
LABEL_H  = 36
PANEL_W  = (TOTAL_W - PAD * (COLS + 1)) // COLS
PANEL_H  = (TOTAL_H - HEADER - PAD * (ROWS + 1) - LABEL_H * ROWS) // ROWS

RENDER_SCALE = 2
HEAD_R = 68
HR     = HEAD_R * RENDER_SCALE

EXPRESSIONS = ["WARM", "SKEPTICAL", "CONCERNED", "SURPRISED", "WISE", "KNOWING"]
EXPR_LABELS = {
    "WARM":      "WARM / WELCOMING",
    "SKEPTICAL": "SKEPTICAL / AMUSED",
    "CONCERNED": "CONCERNED",
    "SURPRISED": "SURPRISED / DELIGHTED",
    "WISE":      "WISE / KNOWING",
    "KNOWING":   "KNOWING STILLNESS  ★ NARRATIVE",
}


# ── Geometry helpers ──────────────────────────────────────────────────────────

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


# ── Head ─────────────────────────────────────────────────────────────────────

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
    draw.ellipse([bun_cx - bun_rx, bun_cy - bun_ry,
                  bun_cx + bun_rx, bun_cy + bun_ry], outline=LINE, width=4)
    for pts in [
        bezier3((cx - int(HR*0.84), cy - ry + 8), (cx - int(HR*0.76), cy - int(ry*0.44)),
                (cx - int(HR*0.80), cy - int(ry*0.06))),
        bezier3((cx + int(HR*0.72), cy - ry + 14), (cx + int(HR*0.80), cy - int(ry*0.38)),
                (cx + int(HR*0.74), cy))
    ]:
        polyline(draw, pts, HAIR_BASE, width=3)
        polyline(draw, pts, LINE, width=1)
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

    for (ex, open_f, is_right) in [(lx, p["l_open"], False), (rx, p["r_open"], True)]:
        actual_h = max(3, int(eh_full * open_f))
        if p.get("eyes_closed"):
            actual_h = max(2, int(eh_full * 0.06))

        draw.ellipse([ex - ew, eye_y - actual_h, ex + ew, eye_y + actual_h], fill=EYE_W)
        ir  = int(ew * 0.62)
        iry = min(ir, actual_h - 2)
        if iry < 2:
            iry = 2
        pdx = int(p.get("gaze_dx", 0) * HR * 0.07)
        pdy = int(p.get("gaze_dy", 0) * HR * 0.06)
        draw.ellipse([ex + pdx - ir, eye_y + pdy - iry,
                      ex + pdx + ir, eye_y + pdy + iry], fill=EYE_IRIS)
        pr = int(ir * 0.52)
        if p.get("pupils_wide"):
            pr = int(ir * 0.70)
        draw.ellipse([ex + pdx - pr, eye_y + pdy - pr,
                      ex + pdx + pr, eye_y + pdy + pr], fill=EYE_PUP)
        if not p.get("eyes_closed"):
            hr_s = max(int(pr * 0.38), 3)
            hlx  = ex + pdx - int(ir * 0.26)
            hly  = eye_y + pdy - int(iry * 0.34)
            draw.ellipse([hlx - hr_s, hly - hr_s, hlx + hr_s, hly + hr_s], fill=EYE_HL)
        draw.arc([ex - ew, eye_y - actual_h, ex + ew, eye_y + actual_h],
                 start=200, end=340, fill=LINE, width=4)
        if not p.get("eyes_closed"):
            arc_draw(draw, ex, eye_y + actual_h - int(eh_full * 0.28),
                     int(ew * 0.76), int(eh_full * 0.26), 15, 165, LINE, width=3)
        # Crow's feet — always present
        dsign   = 1 if is_right else -1
        outer_x = ex + ew * dsign
        for k in range(2):
            dy_k = int(HR * 0.06) * k
            draw.line(
                [(outer_x, eye_y - int(HR * 0.02) + dy_k),
                 (outer_x + dsign * int(HR * 0.11), eye_y - int(HR * 0.10) + dy_k)],
                fill=LINE, width=2
            )
        draw.ellipse([ex - ew, eye_y - actual_h, ex + ew, eye_y + actual_h],
                     outline=LINE, width=6)

    # KNOWING STILLNESS: weighted glance — heavy upper lid overlay
    if p.get("heavy_lid_overlay"):
        for ex in [lx, rx]:
            actual_h_v = max(3, int(eh_full * p["l_open"]))
            # Draw heavy upper lid (darker fill crescent at top of eye = heavy-lidded)
            lid_h = int(actual_h_v * 0.46)
            draw.rectangle([ex - ew + 2, eye_y - actual_h_v,
                             ex + ew - 2, eye_y - actual_h_v + lid_h],
                            fill=SKIN_BASE)
            # Re-draw upper lid arc over it
            draw.arc([ex - ew, eye_y - actual_h_v, ex + ew, eye_y + actual_h_v],
                     start=200, end=340, fill=LINE, width=5)

    # Glasses
    glasses_r_x = int(ew * 1.16)
    glasses_r_y = int(eh_full * 1.32)
    for gx in [lx, rx]:
        draw.ellipse([gx - glasses_r_x, eye_y - glasses_r_y,
                      gx + glasses_r_x, eye_y + glasses_r_y],
                     outline=GLASSES_COL, width=4)
    bridge_y = eye_y - int(glasses_r_y * 0.10)
    draw.line([(lx + glasses_r_x, bridge_y), (rx - glasses_r_x, bridge_y)],
              fill=GLASSES_COL, width=4)
    draw.line([(lx - glasses_r_x, bridge_y),
               (lx - glasses_r_x - int(HR * 0.18), bridge_y - int(HR * 0.04))],
              fill=GLASSES_COL, width=3)
    draw.line([(rx + glasses_r_x, bridge_y),
               (rx + glasses_r_x + int(HR * 0.18), bridge_y - int(HR * 0.04))],
              fill=GLASSES_COL, width=3)

    # Brows
    brow_base_y = eye_y - int(eh_full * 1.36) - glasses_r_y + int(eh_full * 0.38)
    for (bx, b_dy, b_worry, is_right_b) in [
        (lx, p.get("brow_l_dy", 0), p.get("brow_worry", False), False),
        (rx, p.get("brow_r_dy", 0), p.get("brow_worry", False), True),
    ]:
        by      = brow_base_y + b_dy
        inner_x = bx + int(HR * 0.08) if is_right_b else bx - int(HR * 0.08)
        outer_x = bx - int(HR * 0.26) if is_right_b else bx + int(HR * 0.26)
        inner_y = by + (int(HR * 0.14) if b_worry else 0)
        pts     = bezier3((outer_x, by), (bx, by - int(HR * 0.03)), (inner_x, inner_y))
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
        sh      = int(HR * 0.18)
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

    elif style == "suppressed_smile":
        # NARRATIVE EXPRESSION: suppressed smile — one corner barely lifted
        # The key: almost neutral but the VIEWER knows she knows.
        # Very slight asymmetric rise at viewer's right (her left) corner only.
        mw2 = int(mw * 0.72)
        # Left side flat (her right = viewer's left)
        # Right side (her left = viewer's right) slightly lifted
        pts = bezier3(
            (cx - mw2, my + 4),          # left corner flat
            (cx + int(mw * 0.10), my - 6),   # slight curve center-right
            (cx + mw2, my - 4),           # right corner just barely up
        )
        polyline(draw, pts, LINE, width=5)
        # Right corner pull (dimple hint)
        draw.line([(cx + mw2, my - 4), (cx + mw2 + 4, my + 4)],
                  fill=LINE, width=3)


def draw_blush_miri(draw, cx, cy, strength=1.0):
    if strength <= 0:
        return
    bw = int(HR * 0.22)
    bh = int(HR * 0.09)
    by = cy + int(HR * 0.32)
    for bx in [cx - int(HR * 0.44), cx + int(HR * 0.44)]:
        draw.ellipse([bx - bw, by - bh, bx + bw, by + bh], fill=BLUSH_PERM)


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

    arm_w    = int(HR * 0.20)
    arm_h    = int(HR * 0.70)
    arm_y    = body_top_y + int(HR * 0.06)
    l_style  = body_data.get("arm_l_style", "hanging")
    r_style  = body_data.get("arm_r_style", "hanging")
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
            ex  = ax + side * int(HR * 0.50)
            ey  = ay + int(arm_h * 0.60)
            pts = bezier3((ax, ay), (ax + side * int(HR * 0.28), ay + int(arm_h * 0.30)), (ex, ey))
            polyline(draw, pts, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts, LINE, width=4)
            draw.ellipse([ex - int(arm_w * 1.1), ey - int(arm_w * 0.4),
                           ex + int(arm_w * 1.1), ey + int(HR * 0.12)],
                         fill=SKIN_BASE, outline=LINE, width=4)
        elif style == "chest":
            hand_x = cx + side * int(HR * 0.24)
            hand_y = ay + int(arm_h * 0.36)
            pts    = bezier3((ax, ay), (ax + side * int(HR * 0.12), ay + int(arm_h * 0.18)),
                              (hand_x, hand_y))
            polyline(draw, pts, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts, LINE, width=4)
            draw.ellipse([hand_x - int(arm_w * 1.1), hand_y - int(arm_w * 0.4),
                           hand_x + int(arm_w * 1.1), hand_y + int(HR * 0.12)],
                         fill=SKIN_BASE, outline=LINE, width=4)
        elif style == "raised":
            hand_x = ax + side * int(HR * 0.20)
            hand_y = ay - int(arm_h * 0.42)
            pts    = bezier3((ax, ay), (ax + side * int(HR * 0.14), ay - int(arm_h * 0.22)),
                              (hand_x, hand_y))
            polyline(draw, pts, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts, LINE, width=4)
            draw.ellipse([hand_x - int(arm_w * 1.1), hand_y - int(HR * 0.12),
                           hand_x + int(arm_w * 1.1), hand_y + int(arm_w * 0.4)],
                         fill=SKIN_BASE, outline=LINE, width=4)
        elif style == "folded":
            fold_x = cx + side * int(HR * 0.28)
            fold_y = ay + int(arm_h * 0.55)
            pts    = bezier3((ax, ay), (ax - side * int(HR * 0.04), ay + int(arm_h * 0.28)),
                              (fold_x, fold_y))
            polyline(draw, pts, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts, LINE, width=4)
            draw.ellipse([fold_x - int(arm_w * 1.1), fold_y - int(arm_w * 0.4),
                           fold_x + int(arm_w * 1.1), fold_y + int(HR * 0.12)],
                         fill=SKIN_BASE, outline=LINE, width=4)
        elif style == "crossed":
            cross_x = cx + (-side) * int(HR * 0.30)
            cross_y = ay + int(arm_h * 0.48)
            pts     = bezier3((ax, ay), (cx, ay + int(arm_h * 0.22)), (cross_x, cross_y))
            polyline(draw, pts, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts, LINE, width=4)
            draw.ellipse([cross_x - int(arm_w * 1.1), cross_y - int(arm_w * 0.4),
                           cross_x + int(arm_w * 1.1), cross_y + int(HR * 0.12)],
                         fill=SKIN_BASE, outline=LINE, width=4)
        elif style == "settled":
            # NARRATIVE EXPRESSION arm style:
            # Both arms resting low and slightly in front — VERY STILL.
            # "I've been sitting here waiting for this moment."
            rest_x = cx + side * int(HR * 0.44)
            rest_y = ay + int(arm_h * 0.70)
            pts    = bezier3((ax, ay), (ax + side * int(HR * 0.06), ay + int(arm_h * 0.36)),
                              (rest_x, rest_y))
            polyline(draw, pts, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts, LINE, width=4)
            draw.ellipse([rest_x - int(arm_w * 1.1), rest_y - int(arm_w * 0.4),
                           rest_x + int(arm_w * 1.1), rest_y + int(HR * 0.12)],
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

    for lx_ in [leg_l, leg_r]:
        draw.rectangle([lx_ - leg_w, leg_y, lx_ + leg_w, leg_y + leg_h],
                       fill=PANTS, outline=LINE, width=4)
        draw.line([(lx_, leg_y), (lx_, leg_y + leg_h)], fill=PANTS_SH, width=2)

    slipper_y = leg_y + leg_h
    slipper_w = int(HR * 0.36)
    slipper_h = int(HR * 0.14)
    for lx_ in [leg_l, leg_r]:
        draw.ellipse([lx_ - slipper_w + int(slipper_w * 0.20), slipper_y,
                       lx_ + slipper_w - int(slipper_w * 0.20), slipper_y + slipper_h],
                     fill=SLIPPER, outline=LINE, width=4)


# ── Expression specifications ─────────────────────────────────────────────────

EXPR_SPECS = {
    "WARM": {
        "eyes": {
            "l_open": 0.82, "r_open": 0.82,
            "brow_l_dy": -int(HR * 0.08), "brow_r_dy": -int(HR * 0.08),
            "brow_worry": False, "gaze_dx": 0, "gaze_dy": 0,
        },
        "mouth": "warm_closed", "blush": 1.0,
        "body": {"body_tilt": -6, "arm_l_style": "extended", "arm_r_style": "extended",
                 "arm_l_dy": 0, "arm_r_dy": 0},
        "cy_offset": -10,
    },
    "SKEPTICAL": {
        "eyes": {
            "l_open": 0.70, "r_open": 0.70,
            "brow_l_dy": -int(HR * 0.18), "brow_r_dy": 0,
            "brow_worry": False, "gaze_dx": 0, "gaze_dy": 0.06,
        },
        "mouth": "smirk", "blush": 0.6,
        "body": {"body_tilt": +10, "arm_l_style": "crossed", "arm_r_style": "crossed",
                 "arm_l_dy": -int(HR * 0.06), "arm_r_dy": -int(HR * 0.06)},
        "cy_offset": -8,
    },
    "CONCERNED": {
        "eyes": {
            "l_open": 0.88, "r_open": 0.88,
            "brow_l_dy": -int(HR * 0.16), "brow_r_dy": -int(HR * 0.16),
            "brow_worry": True, "gaze_dx": 0, "gaze_dy": 0.08,
        },
        "mouth": "pursed", "blush": 0.0,
        "body": {"body_tilt": -10, "arm_l_style": "hanging", "arm_r_style": "chest",
                 "arm_l_dy": 0, "arm_r_dy": -int(HR * 0.08)},
        "cy_offset": -8,
    },
    "SURPRISED": {
        "eyes": {
            "l_open": 1.0, "r_open": 1.0,
            "brow_l_dy": -int(HR * 0.28), "brow_r_dy": -int(HR * 0.28),
            "brow_worry": False, "pupils_wide": True, "gaze_dx": 0, "gaze_dy": 0,
        },
        "mouth": "open_delight", "blush": 1.0,
        "body": {"body_tilt": +14, "arm_l_style": "raised", "arm_r_style": "raised",
                 "arm_l_dy": -int(HR * 0.10), "arm_r_dy": -int(HR * 0.10)},
        "cy_offset": -12,
    },
    "WISE": {
        "eyes": {
            "l_open": 0.62, "r_open": 0.62,
            "brow_l_dy": 0, "brow_r_dy": 0,
            "brow_worry": False, "gaze_dx": 0, "gaze_dy": 0.10,
        },
        "mouth": "knowing", "blush": 0.8,
        "body": {"body_tilt": 0, "arm_l_style": "folded", "arm_r_style": "folded",
                 "arm_l_dy": 0, "arm_r_dy": 0},
        "cy_offset": -8,
    },
    # ── NARRATIVE EXPRESSION: KNOWING STILLNESS ──────────────────────────────────
    # "She knew about the Glitch Layer all along."
    # Body:  completely still — arms settled low (not folded, not raised — just THERE)
    # Eyes:  WEIGHTED GLANCE — heavy upper lid, gaze oblique-down-right, seeing through time
    # Mouth: SUPPRESSED SMILE — barely one corner lifted, holding it in
    # Blush: very low (0.2) — warmth is INWARD, not broadcasting outward
    # Brows: very slightly lowered and level — relaxed authority, not effort
    # This is Miri looking at Luma and thinking: "I've been waiting for you to figure this out."
    "KNOWING": {
        "eyes": {
            "l_open": 0.50, "r_open": 0.50,   # heavy-lidded — sees more than she shows
            "brow_l_dy": int(HR * 0.04), "brow_r_dy": int(HR * 0.04),  # brows slightly lowered
            "brow_worry": False,
            "gaze_dx": 0.6, "gaze_dy": 0.30,   # oblique downward glance — weighted
            "heavy_lid_overlay": True,           # extra heavy lid effect
        },
        "mouth": "suppressed_smile", "blush": 0.2,   # barely any blush
        "body": {
            "body_tilt":   0,      # perfectly still — no lean, no movement
            "arm_l_style": "settled",   # arms at rest, low, unhurried
            "arm_r_style": "settled",
            "arm_l_dy":    int(HR * 0.06),
            "arm_r_dy":    int(HR * 0.06),
        },
        "cy_offset": -8,
    },
}


# ── Panel renderer ─────────────────────────────────────────────────────────────

def render_panel_miri(expr, panel_w, panel_h):
    rw   = panel_w * RENDER_SCALE
    rh   = panel_h * RENDER_SCALE
    img  = Image.new("RGBA", (rw, rh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx   = rw // 2
    spec = EXPR_SPECS[expr]
    cy   = int(rh * 0.32) + spec.get("cy_offset", 0) * RENDER_SCALE

    body_top_y = cy + int(HR * 0.92)
    draw_body_miri(draw, cx, body_top_y, spec["body"])
    draw = ImageDraw.Draw(img)   # refresh after paste

    draw_head_miri(draw, cx, cy)
    draw_ears_miri(draw, cx, cy)
    draw_hair_bun(draw, cx, cy)
    draw_blush_miri(draw, cx, cy, strength=spec["blush"])
    draw_eyes_miri(draw, cx, cy, spec["eyes"])
    draw_nose_miri(draw, cx, cy)
    draw_mouth_miri(draw, cx, cy, style=spec["mouth"])

    return img.resize((panel_w, panel_h), Image.LANCZOS)


# ── Sheet assembly ─────────────────────────────────────────────────────────────

def build_sheet(show_guides=False):
    sheet = Image.new("RGB", (TOTAL_W, TOTAL_H), CANVAS_BG)
    draw  = ImageDraw.Draw(sheet)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
        font_sub   = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = font_title
        font_sub   = font_title

    title = "GRANDMA MIRI — Expression Sheet v003  |  Luma & the Glitchkin"
    sub   = ("Designer: Maya Santos  |  Cycle 25  |  KNOWING STILLNESS added  |  "
             "★ NARRATIVE EXPRESSION: she knew about the Glitch Layer all along")
    draw.text((PAD, 10), title, fill=(235, 218, 196), font=font_title)
    draw.text((PAD, 36), sub,   fill=(165, 150, 130), font=font_sub)

    panel_w = PANEL_W - PAD * 2
    panel_h = PANEL_H - PAD

    for idx, expr in enumerate(EXPRESSIONS):
        col = idx % COLS
        row = idx // COLS
        px  = PAD + col * (PANEL_W + PAD)
        py  = HEADER + PAD + row * (PANEL_H + LABEL_H + PAD)

        bg  = BG[expr]
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], fill=bg)
        draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], outline=LINE, width=2)

        # Highlight the NARRATIVE expression panel with a subtle accent border
        if expr == "KNOWING":
            draw.rectangle([px, py, px + PANEL_W, py + PANEL_H],
                           outline=(100, 110, 95), width=4)

        face_img = render_panel_miri(expr, panel_w, panel_h)
        ox = px + PAD
        oy = py + PAD // 2
        sheet.paste(face_img, (ox, oy), face_img)

        # CRITICAL: refresh draw after paste
        draw = ImageDraw.Draw(sheet)

        label    = EXPR_LABELS[expr]
        label_y  = py + PANEL_H + 2
        label_bg = tuple(max(0, int(c * 0.88)) for c in bg)
        draw.rectangle([px, label_y, px + PANEL_W, label_y + LABEL_H], fill=label_bg)
        try:
            bbox = draw.textbbox((0, 0), label, font=font_label)
            tw   = bbox[2] - bbox[0]
            th   = bbox[3] - bbox[1]
        except Exception:
            tw, th = 100, 14
        tx = px + (PANEL_W - tw) // 2
        ty = label_y + (LABEL_H - th) // 2
        draw.text((tx, ty), label, fill=LINE, font=font_label)

    return sheet


if __name__ == "__main__":
    out_dir  = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "characters", "main")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_grandma_miri_expression_sheet_v003.png")
    sheet    = build_sheet(show_guides=False)
    sheet.save(out_path)
    print(f"Saved: {os.path.abspath(out_path)}")
    print(f"Canvas: {sheet.size[0]}x{sheet.size[1]}")
    print("v003 NARRATIVE EXPRESSION added: KNOWING STILLNESS")
    print("  - Eyes: heavy-lidded oblique downward glance")
    print("  - Mouth: suppressed smile (one corner barely lifted)")
    print("  - Body: completely still — arms settled low")
    print("  - Blush: 0.2 (warmth contained inward)")
    print("  - Message: 'I've been waiting for you to figure this out.'")
