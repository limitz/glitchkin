#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_grandma_miri_expression_sheet.py
Grandma Miri Expression Sheet — v006 Wooden Hairpin Rename (P0 C44)
"Luma & the Glitchkin" — Cycle 44 / Maya Santos

v006 CHANGES (C44 — Alex Chen P0 — cultural identity correction):
  - Renamed draw_hair_bun() vars: chop_x1/chop_x2 → hairpin_x1/hairpin_x2.
    Accessory is now "wooden hairpins" per design correction (replaces chopstick pair).
    No drawing logic change — geometry, color (92, 58, 32), and silhouette unchanged.

v005 CHANGES (C41 — Daisuke Kobayashi C16 P3 — M001 spec lint WARN fix):
  - Added `MIRI_HEAD_RATIO = 3.2` as an explicit canonical constant.
    Closes M001 WARN (ratio inferred → ratio explicit). No visual change.

v004 CHANGES (Lee Tanaka C34 Pose Brief):

  WARM/WELCOMING — REDESIGNED for maximum silhouette range:
    - Both arms: wide-open embrace — elbows bent, forearms up, hands at
      chest/shoulder height, palms facing out.
    - New arm style: "wide_open" — significantly wider than any other pose.
    - Body: slight forward lean (toward whoever she is welcoming).
    - Silhouette read: wide-top V or U shape from arms. The widest silhouette
      on the sheet. Cannot be confused with CONCERNED or NOSTALGIC.

  NOSTALGIC/WISTFUL — NEW GESTURE:
    - One hand flat to chest (palm on sternum — "this hits me in the heart").
    - Other arm at side, slightly in front of body.
    - Head: slightly tilted down, gaze_dy=0.12 (wistful downward look).
    - New arm styles: arm_l_style="chest_flat", arm_r_style="hanging".
    - Silhouette: compact — arms near body. Distinct from WELCOMING (wide).

  CONCERNED — CLASPED HANDS:
    - Both hands clasped at chest level (prayer/worry hands).
    - Both arms come inward to center, hands meeting at chest.
    - New arm style: "clasped_center" applied to both arms.
    - Body: slight forward lean, head forward and down.
    - Silhouette: compact top (no wide arm spread), forward tilt.
      Distinct from WELCOMING (wide) and NOSTALGIC (one side flat).

  SURPRISED/DELIGHTED — HAND TO CHEEK:
    - One hand to cheek (grandmother "oh my goodness" gesture).
    - Hand-to-cheek creates arm-up-to-face asymmetric silhouette element.
    - Body: small pull-back (body_tilt = +18, mild recoil).
    - Other arm: slightly raised or at chest.
    - New arm style: arm_r_style="hand_to_cheek" — raises right arm to face.
    - Silhouette: asymmetric — one arm raised to face level. Distinct from
      all symmetric poses.

  WISE/KNOWING — SMALL POSE HOOK ADDED:
    - Arms loosely crossed (not tight worried, but relaxed-knowing elder
      confidence). Existing "crossed" style already available.
    - Slight weight to one side (body_tilt=+5, comfortable authority lean).
    - Silhouette: relaxed crossed arms at mid-torso. Different from CONCERNED
      (clasped at chest) and WELCOMING (wide open).

  KNOWING STILLNESS — ONE ASYMMETRIC ELEMENT ADDED:
    - Index finger pointing down at side (subtle "I know more" gesture).
    - arm_r_style="index_point_down" — right arm with pointing hand.
    - Head: fractionally turned (head_oblique retained from v003).
    - Silhouette: still very close to WISE — but has one asymmetric element.
      This is intentional and accepted.

  Silhouette pair targets (v004):
    WELCOMING: widest shape on sheet (arms-out V)
    NOSTALGIC: compact/asymmetric (one hand to chest)
    CONCERNED: compact/symmetric (hands clasped center)
    SURPRISED: asymmetric raise (one arm to face)
    WISE: relaxed crossed arms + lean
    KNOWING: near-identical to WISE + one subtle pointing gesture

Output: output/characters/main/LTG_CHAR_grandma_miri_expression_sheet.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Palette (from grandma_miri.md) ────────────────────────────────────────────
SKIN_BASE   = (140, 84, 48)
SKIN_SH     = (106, 58, 30)
SKIN_HL     = (168, 106, 64)
BLUSH_PERM  = (212, 149, 107)
HAIR_BASE   = (216, 208, 200)
HAIR_SH     = (168, 152, 140)
HAIR_HL     = (240, 236, 232)
EYE_IRIS    = (139, 94, 60)
EYE_PUP     = (26, 15, 10)
EYE_W       = (250, 240, 220)
EYE_HL      = (240, 240, 240)
BROW_COL    = (138, 122, 112)
CARDIGAN    = (184, 92, 56)
CARDIGAN_SH = (138, 60, 28)
CARDIGAN_HL = (212, 130, 90)
PANTS       = (200, 174, 138)
PANTS_SH    = (160, 138, 106)
SLIPPER     = (196, 144, 122)   # C38 FIX: #C4907A Dusty Warm Apricot (was (90,122,90) #5A7A5A Deep Sage — G>R violated Miri warm-palette guarantee; per master_palette.md CHAR-M-11 C32)
GLASSES_COL = (59, 40, 32)
LINE        = (59, 40, 32)
CANVAS_BG   = (28, 20, 14)

BG = {
    "WARM":      (248, 232, 210),
    "SKEPTICAL": (210, 218, 208),
    "CONCERNED": (200, 212, 225),
    "SURPRISED": (245, 228, 195),
    "WISE":      (218, 214, 205),
    "KNOWING":   (228, 218, 200),
}

# ── Layout ─────────────────────────────────────────────────────────────────────
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

# ── Canonical proportion constant (M001 — closes spec lint WARN) ───────────────
# Grandma Miri's canonical head-to-body ratio: total character height = 3.2 × head height.
# This matches the lineup tool (MIRI_HEADS = 3.2) and the character spec.
MIRI_HEAD_RATIO = 3.2

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
    hairpin_x1 = bun_cx - int(bun_rx * 0.32)
    hairpin_x2 = bun_cx + int(bun_rx * 0.26)
    draw.line([(hairpin_x1, bun_cy - bun_ry - 10), (hairpin_x1 + 7, bun_cy + bun_ry + 6)],
              fill=LINE, width=3)
    draw.line([(hairpin_x2, bun_cy - bun_ry - 8), (hairpin_x2 + 7, bun_cy + bun_ry + 4)],
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

    glasses_r_x = int(ew * 1.16)
    glasses_r_y = int(eh_full * 1.32)
    for gx, gey in [(lx, l_eye_y), (rx, r_eye_y)]:
        draw.ellipse([gx - glasses_r_x, gey - glasses_r_y,
                      gx + glasses_r_x, gey + glasses_r_y],
                     outline=GLASSES_COL, width=4)
    bridge_y = (l_eye_y + r_eye_y) // 2 - int(glasses_r_y * 0.10)
    draw.line([(lx + glasses_r_x, bridge_y), (rx - glasses_r_x, bridge_y)],
              fill=GLASSES_COL, width=4)
    draw.line([(lx - glasses_r_x, bridge_y),
               (lx - glasses_r_x - int(HR * 0.18), bridge_y - int(HR * 0.04))],
              fill=GLASSES_COL, width=3)
    draw.line([(rx + glasses_r_x, bridge_y),
               (rx + glasses_r_x + int(HR * 0.18), bridge_y - int(HR * 0.04))],
              fill=GLASSES_COL, width=3)

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
        mw2 = int(mw * 0.70)
        pts = bezier3((cx - mw2, my + 2),
                      (cx - int(mw * 0.14), my - 8),
                      (cx + mw2, my + 6))
        polyline(draw, pts, LINE, width=5)
        draw.line([(cx - mw2, my + 2), (cx - mw2 - 4, my - 4)], fill=LINE, width=3)


def draw_blush_miri(draw, cx, cy, strength=1.0):
    if strength <= 0:
        return
    bw = int(HR * 0.22)
    bh = int(HR * 0.09)
    by = cy + int(HR * 0.32)
    for bx in [cx - int(HR * 0.44), cx + int(HR * 0.44)]:
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

    lax = cx - tw + tilt + int(HR * 0.04)
    rax = cx + tw + tilt - int(HR * 0.04)

    def draw_arm(ax, ay, style, side):
        """Draw a Miri arm with the given style."""
        if style == "hanging":
            draw.rectangle([ax - arm_w, ay, ax + arm_w, ay + arm_h],
                           fill=CARDIGAN, outline=LINE, width=4)
            draw.ellipse([ax - int(arm_w * 1.1), ay + arm_h - int(arm_w * 0.4),
                           ax + int(arm_w * 1.1), ay + arm_h + int(HR * 0.14)],
                         fill=SKIN_BASE, outline=LINE, width=4)

        elif style == "extended":
            # v003 "extended" — arms somewhat open
            ex = ax + side * int(HR * 0.50)
            ey = ay + int(arm_h * 0.60)
            pts = bezier3((ax, ay), (ax + side * int(HR * 0.28), ay + int(arm_h * 0.30)),
                          (ex, ey))
            polyline(draw, pts, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts, LINE, width=4)
            draw.ellipse([ex - int(arm_w * 1.1), ey - int(arm_w * 0.4),
                           ex + int(arm_w * 1.1), ey + int(HR * 0.12)],
                         fill=SKIN_BASE, outline=LINE, width=4)

        elif style == "wide_open":
            # v004 WELCOMING — wide-open embrace. Arms go wide out and up.
            # Elbow out to side at shoulder height, forearm angled up with palms facing out.
            elbow_x = cx + side * int(HR * 1.20)
            elbow_y = ay + int(arm_h * 0.08)
            hand_x  = cx + side * int(HR * 1.00)
            hand_y  = ay - int(arm_h * 0.30)
            pts_upper = bezier3((ax, ay), (ax + side * int(HR * 0.60), ay - int(arm_h * 0.04)),
                                (elbow_x, elbow_y))
            polyline(draw, pts_upper, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts_upper, LINE, width=4)
            pts_lower = bezier3((elbow_x, elbow_y),
                                (elbow_x + side * int(HR * 0.02), elbow_y - int(arm_h * 0.18)),
                                (hand_x, hand_y))
            polyline(draw, pts_lower, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts_lower, LINE, width=4)
            # Palm facing out — slightly flattened oval
            draw.ellipse([hand_x - int(arm_w * 0.8), hand_y - int(HR * 0.16),
                           hand_x + int(arm_w * 0.8), hand_y + int(HR * 0.04)],
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

        elif style == "chest_flat":
            # v004 NOSTALGIC — palm flat on sternum (heart gesture)
            # Arm comes inward and up, hand flat on chest center
            hand_x = cx + side * int(HR * 0.12)   # close to center
            hand_y = ay + int(arm_h * 0.24)
            pts = bezier3((ax, ay),
                          (ax + side * int(HR * 0.08), ay + int(arm_h * 0.12)),
                          (hand_x, hand_y))
            polyline(draw, pts, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts, LINE, width=4)
            # Flat hand on chest — wider oval, suggesting palm
            draw.ellipse([hand_x - int(arm_w * 1.4), hand_y - int(HR * 0.08),
                           hand_x + int(arm_w * 1.4), hand_y + int(HR * 0.12)],
                         fill=SKIN_BASE, outline=LINE, width=4)

        elif style == "clasped_center":
            # v004 CONCERNED — both hands clasped at chest (prayer hands)
            # Arms come to center, hands meet at mid-chest
            hand_x = cx + side * int(HR * 0.06)
            hand_y = ay + int(arm_h * 0.38)
            pts = bezier3((ax, ay),
                          (ax + side * int(HR * 0.04), ay + int(arm_h * 0.18)),
                          (hand_x, hand_y))
            polyline(draw, pts, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts, LINE, width=4)
            # Clasped hand — overlapping circles to suggest prayer hands
            draw.ellipse([hand_x - int(arm_w * 1.0), hand_y - int(HR * 0.06),
                           hand_x + int(arm_w * 1.0), hand_y + int(HR * 0.10)],
                         fill=SKIN_BASE, outline=LINE, width=3)

        elif style == "raised":
            # v003 "raised" — arm goes up (for SURPRISED/DELIGHTED)
            hand_x = ax + side * int(HR * 0.20)
            hand_y = ay - int(arm_h * 0.42)
            pts = bezier3((ax, ay), (ax + side * int(HR * 0.14), ay - int(arm_h * 0.22)),
                          (hand_x, hand_y))
            polyline(draw, pts, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts, LINE, width=4)
            draw.ellipse([hand_x - int(arm_w * 1.1), hand_y - int(HR * 0.12),
                           hand_x + int(arm_w * 1.1), hand_y + int(arm_w * 0.4)],
                         fill=SKIN_BASE, outline=LINE, width=4)

        elif style == "hand_to_cheek":
            # v004 SURPRISED/DELIGHTED — hand raised to cheek (grandmother "oh my" gesture)
            # The arm must reach face level (above torso top)
            cheek_x = cx + side * int(HR * 0.55)
            cheek_y = ay - int(arm_h * 0.75)  # at face/cheek level
            elbow_x = cx + side * int(HR * 0.70)
            elbow_y = ay - int(arm_h * 0.28)
            pts_up = bezier3((ax, ay),
                             (ax + side * int(HR * 0.40), ay - int(arm_h * 0.12)),
                             (elbow_x, elbow_y))
            polyline(draw, pts_up, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts_up, LINE, width=4)
            pts_cheek = bezier3((elbow_x, elbow_y),
                                (cx + side * int(HR * 0.62), elbow_y - int(arm_h * 0.24)),
                                (cheek_x, cheek_y))
            polyline(draw, pts_cheek, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts_cheek, LINE, width=4)
            # Hand at cheek
            draw.ellipse([cheek_x - int(arm_w * 1.1), cheek_y - int(HR * 0.14),
                           cheek_x + int(arm_w * 1.1), cheek_y + int(HR * 0.04)],
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

        elif style == "index_point_down":
            # v004 KNOWING STILLNESS — index finger pointing down at side
            # Arm slightly forward from body, hand lower, one finger extended downward
            hand_x = ax + side * int(HR * 0.08)
            hand_y = ay + int(arm_h * 0.72)
            pts = bezier3((ax, ay),
                          (ax + side * int(HR * 0.04), ay + int(arm_h * 0.36)),
                          (hand_x, hand_y))
            polyline(draw, pts, CARDIGAN, width=arm_w * 2)
            polyline(draw, pts, LINE, width=4)
            # Hand shape
            draw.ellipse([hand_x - int(arm_w * 1.0), hand_y - int(HR * 0.04),
                           hand_x + int(arm_w * 1.0), hand_y + int(HR * 0.12)],
                         fill=SKIN_BASE, outline=LINE, width=3)
            # Pointing finger (extends slightly below hand)
            draw.line([(hand_x, hand_y + int(HR * 0.10)),
                       (hand_x + side * int(HR * 0.04), hand_y + int(HR * 0.22))],
                      fill=SKIN_BASE, width=int(arm_w * 0.6))
            draw.line([(hand_x, hand_y + int(HR * 0.10)),
                       (hand_x + side * int(HR * 0.04), hand_y + int(HR * 0.22))],
                      fill=LINE, width=2)

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
        # v004: wide-open embrace — significantly wider silhouette
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
            "arm_l_style": "wide_open",   # v004: was "extended" — now genuinely wide
            "arm_r_style": "wide_open",
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
        # v004: both hands clasped at chest level (prayer/worry hands)
        "eyes": {
            "l_open": 0.88, "r_open": 0.88,
            "brow_l_dy": -int(HR * 0.16), "brow_r_dy": -int(HR * 0.16),
            "brow_worry": True,
            "gaze_dx": 0, "gaze_dy": 0.10,  # slightly more downward focus
        },
        "mouth": "pursed",
        "blush": 0.0,
        "body": {
            "body_tilt":   -12,   # forward lean toward person she is concerned about
            "arm_l_style": "clasped_center",
            "arm_r_style": "clasped_center",
            "arm_l_dy":    -int(HR * 0.04),
            "arm_r_dy":    -int(HR * 0.04),
        },
        "cy_offset": -10,
    },
    "SURPRISED": {
        # v004: one hand to cheek — asymmetric signature gesture
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
            "body_tilt":   +18,   # small pull-back recoil
            "arm_l_style": "raised",   # left arm slightly raised / at chest
            "arm_r_style": "hand_to_cheek",   # RIGHT hand to cheek — asymmetric hook
            "arm_l_dy":    -int(HR * 0.10),
            "arm_r_dy":    -int(HR * 0.10),
        },
        "cy_offset": -12,
    },
    "WISE": {
        # v004: arms loosely crossed + slight lean — elder confidence
        "eyes": {
            "l_open": 0.62, "r_open": 0.62,
            "brow_l_dy": 0, "brow_r_dy": 0,
            "brow_worry": False,
            "gaze_dx": 0, "gaze_dy": 0.10,
        },
        "mouth": "knowing",
        "blush": 0.8,
        "body": {
            "body_tilt":   +5,   # v004: slight weight-shift lean (comfortable authority)
            "arm_l_style": "crossed",
            "arm_r_style": "crossed",
            "arm_l_dy":    0,
            "arm_r_dy":    0,
        },
        "cy_offset": -8,
    },
    "KNOWING": {
        # v004: right arm gets index_point_down gesture + slight oblique head turn retained
        "eyes": {
            "l_open": 0.48,
            "r_open": 0.48,
            "brow_l_dy": 0,
            "brow_r_dy": +int(HR * 0.04),
            "brow_worry": False,
            "gaze_dx": +0.12,
            "gaze_dy": 0.06,
            "l_eye_dy": -int(HR * 0.02),
            "r_eye_dy": +int(HR * 0.03),
        },
        "mouth": "knowing_oblique",
        "blush": 0.2,
        "body": {
            "body_tilt":   0,
            "arm_l_style": "folded",         # left arm folded (same as v003)
            "arm_r_style": "index_point_down",  # v004: right arm with subtle pointing gesture
            "arm_l_dy":    0,
            "arm_r_dy":    +int(HR * 0.04),   # right arm slightly lower
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
    draw = ImageDraw.Draw(img)
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

    title = "GRANDMA MIRI — Expression Sheet v005  |  Luma & the Glitchkin"
    sub   = ("Designer: Maya Santos  |  C41 M001 Fix  |  "
             f"6 expressions  |  HEAD_RATIO={MIRI_HEAD_RATIO}  |  WELCOMING redesign + hand-to-cheek")
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
        draw = ImageDraw.Draw(sheet)

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

    sheet.thumbnail((1280, 1280), Image.LANCZOS)
    return sheet


if __name__ == "__main__":
    out_dir  = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "characters", "main")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_grandma_miri_expression_sheet.png")
    sheet    = build_sheet()
    sheet.save(out_path)
    print(f"Saved: {os.path.abspath(out_path)}")
    print(f"Canvas: {sheet.size[0]}x{sheet.size[1]}")
    print("v004 additions:")
    print("  + WELCOMING: wide_open arms (max silhouette range)")
    print("  + NOSTALGIC: chest_flat palm gesture")
    print("  + CONCERNED: clasped_center prayer hands")
    print("  + SURPRISED: hand_to_cheek asymmetric hook")
    print("  + WISE: slight body lean (body_tilt=+5)")
    print("  + KNOWING STILLNESS: index_point_down subtle gesture")
