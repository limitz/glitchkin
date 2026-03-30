#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_luma_turnaround.py
Luma — 4-View Character Turnaround v004
"Luma & the Glitchkin" — Cycle 32 / Rin Yamamoto

v004 UPDATE (C32 — Eye-Width Canonical Fix):
  Fixes Daisuke eye-width semantic mismatch (Critique 13 P1 / Alex C32 directive).
  Previous v003 used: ew = int(h * 0.22) where h = head-HEIGHT (one head unit * SCALE)
  This was wrong. Canonical spec (Alex Chen, C32): ew = int(head_r * 0.22)
    where head_r = head-RADIUS (h * 0.50).
  v003 ew was int(h * 0.22) = int(head_r * 2 * 0.22) = int(head_r * 0.44) — 2× too wide.

  Changes per view:
    FRONT:    ew = int(h * 0.22) → int(head_r * 0.22) where head_r = int(h * 0.50)
              = int(h * 0.11). eh adjusted proportionally: int(h * 0.15) → int(head_r * 0.15)
              = int(h * 0.075) — keeping ew/eh ratio unchanged.
    3/4:      Same fix applied to near eye. Far eye: ew_far = int(ew * 0.72) (unchanged ratio).
    SIDE:     ew = int(h * 0.16) → int(head_r * 0.16) = int(h * 0.08).
              eh = int(h * 0.13) → int(head_r * 0.13) = int(h * 0.065).

  All other proportions, line weights, hair, body — unchanged from v003.

v003 UPDATE (C28 — Line Weight Fix):
  All line weights corrected to v006 standard. All views updated. 3.2 heads canonical.

4 views: FRONT, 3/4, SIDE, BACK
Canvas: 1600×700px raw → thumbnail to 1280×560
2× render + LANCZOS for sub-pixel AA

Output: output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os
import random

# ── Palette ────────────────────────────────────────────────────────────────────
SKIN       = (200, 136, 90)
SKIN_SH    = (160, 104, 64)
SKIN_HL    = (223, 160, 112)
HAIR       = ( 26,  15, 10)
HAIR_SH    = ( 10,  10, 20)
HAIR_HL    = ( 61,  31, 15)
EYE_W      = (250, 240, 220)
EYE_IRIS   = (200, 125, 62)
EYE_PUP    = ( 59,  40, 32)
EYE_HL     = (240, 240, 240)
HOODIE     = (232, 112, 42)
HOODIE_SH  = (184,  74, 32)
HOODIE_HL  = (245, 144, 80)
HOOD_LINING = (250, 232, 200)
PANTS      = ( 42,  40, 80)
PANTS_SH   = ( 26,  24, 48)
SHOE       = (245, 232, 208)
SHOE_SOLE  = (199,  91, 57)
LACES      = (  0, 240, 255)
PX_CYAN    = (  0, 240, 255)
PX_MAG     = (255,  45, 107)
PX_WHITE   = (240, 240, 240)
LINE       = ( 59,  40, 32)
CANVAS_BG  = (248, 244, 238)
SHADOW_COL = (210, 200, 185)
LABEL_COL  = ( 59,  40, 32)

# ── Layout ────────────────────────────────────────────────────────────────────
CANVAS_W  = 1600
CANVAS_H  = 700
VIEWS     = ["FRONT", "3/4", "SIDE", "BACK"]
N_VIEWS   = 4
VIEW_W    = CANVAS_W // N_VIEWS
VIEW_H    = CANVAS_H
HEADER_H  = 52
LABEL_H   = 36
BODY_H    = VIEW_H - HEADER_H - LABEL_H   # 612px character area

SCALE = 2
CHAR_DRAW_H = int(BODY_H * 0.86)


def hu():
    """One head unit at 1×. Luma is ~3.2 heads tall."""
    return CHAR_DRAW_H / 3.2


def px_accent(draw, x0, y0, w, h_region, seed=7):
    """Simplified pixel accent on hoodie."""
    rng = random.Random(seed)
    for _ in range(10):
        px = rng.randint(x0 + 3, x0 + w - 4)
        py = rng.randint(y0 + 3, y0 + h_region - 4)
        sz = rng.choice([3, 4])
        c  = rng.choice([PX_CYAN, PX_MAG, PX_WHITE])
        draw.rectangle([px, py, px + sz, py + sz], fill=c)


# ── FRONT VIEW ────────────────────────────────────────────────────────────────

def render_front(draw, cx, base_y):
    S = SCALE
    h = int(hu() * S)
    top_y   = base_y - int(CHAR_DRAW_H * S)
    head_cy = top_y + h

    # --- HEAD (classroom-style: circle + cheek nubs, no jaw bump) ---
    head_r = int(h * 0.50)
    draw.ellipse([cx - head_r, head_cy - head_r,
                  cx + head_r, head_cy + head_r + int(h * 0.08)],
                 fill=SKIN)
    # Lower chin fill (classroom-style)
    chin_rx = int(h * 0.47)
    draw.ellipse([cx - chin_rx, head_cy - int(h * 0.10),
                  cx + chin_rx, head_cy + head_r + int(h * 0.12)], fill=SKIN)
    draw.arc([cx - chin_rx, head_cy - int(h * 0.10),
              cx + chin_rx, head_cy + head_r + int(h * 0.12)],
             start=0, end=180, fill=LINE, width=4)
    # Cheek nubs (classroom-style)
    nub_w = int(h * 0.09)
    nub_h = int(h * 0.12)
    nub_y = head_cy - int(h * 0.06)
    for side in [-1, 1]:
        draw.ellipse([cx + side * head_r - nub_w + side * int(h * 0.03),
                      nub_y - nub_h,
                      cx + side * head_r + nub_w + side * int(h * 0.03),
                      nub_y + nub_h],
                     fill=SKIN, outline=LINE, width=3)

    # Hair mass — 8 overlapping ellipses (classroom cloud method)
    # Scale factor: classroom head_r=100, turnaround FRONT head_r = h*0.50
    hs = h / 200.0   # h at 2x; classroom coord at 1x used head_r=100 → scale=h/200
    hair_top = head_cy - int(h * 0.95)   # top of hair cloud
    draw.ellipse([cx - int(hs*155), hair_top, cx + int(hs*145), head_cy - int(h*0.20)], fill=HAIR)
    draw.ellipse([cx - int(hs*175), hair_top + int(hs*25), cx - int(hs*80), head_cy - int(h*0.30)], fill=HAIR)
    draw.ellipse([cx - int(hs*165), hair_top + int(hs*55), cx - int(hs*95), head_cy - int(h*0.15)], fill=HAIR)
    draw.ellipse([cx + int(hs*80),  hair_top + int(hs*35), cx + int(hs*155), head_cy - int(h*0.30)], fill=HAIR)
    draw.ellipse([cx + int(hs*90),  hair_top + int(hs*65), cx + int(hs*145), head_cy - int(h*0.20)], fill=HAIR)
    draw.ellipse([cx - int(hs*60),  hair_top - int(hs*15), cx + int(hs*20),  head_cy - int(h*0.67)], fill=HAIR)
    draw.ellipse([cx - int(hs*20),  hair_top - int(hs*25), cx + int(hs*70),  head_cy - int(h*0.70)], fill=HAIR)
    draw.ellipse([cx - int(hs*100), hair_top,              cx - int(hs*30),  head_cy - int(h*0.63)], fill=HAIR)
    # Hair highlight
    draw.arc([cx - int(hs*60), hair_top - int(hs*10),
              cx + int(hs*60), hair_top + int(hs*45)],
             start=200, end=340, fill=HAIR_HL, width=3)
    # Head outline
    draw.ellipse([cx - head_r, head_cy - head_r,
                  cx + head_r, head_cy + head_r + int(h * 0.08)],
                 outline=LINE, width=4)

    # Face features
    eye_y  = head_cy + int(h * 0.04)
    sep    = int(h * 0.36)
    # C32 fix: ew = int(head_r * 0.22) — head_r is radius, not height
    # head_r = int(h * 0.50) so ew = int(int(h*0.50) * 0.22)
    ew, eh = int(head_r * 0.22), int(head_r * 0.15)
    for ex in [cx - sep, cx + sep]:
        draw.ellipse([ex - ew, eye_y - eh, ex + ew, eye_y + eh], fill=EYE_W)
        ir = int(ew * 0.68)
        draw.ellipse([ex - ir, eye_y - min(ir, eh - 2),
                      ex + ir, eye_y + min(ir, eh - 2)], fill=EYE_IRIS)
        draw.ellipse([ex - int(ir * 0.5), eye_y - int(ir * 0.5),
                      ex + int(ir * 0.5), eye_y + int(ir * 0.5)], fill=EYE_PUP)
        draw.ellipse([ex - int(ir * 0.28) - 3, eye_y - int(eh * 0.36),
                      ex - int(ir * 0.28) + 3, eye_y - int(eh * 0.36) + 5],
                     fill=EYE_HL)
        draw.arc([ex - ew, eye_y - eh, ex + ew, eye_y + eh],
                 start=200, end=340, fill=LINE, width=3)
        draw.ellipse([ex - ew, eye_y - eh, ex + ew, eye_y + eh],
                     outline=LINE, width=3)
    # Nose
    draw.arc([cx - int(h * 0.06), head_cy + int(h * 0.16),
              cx + int(h * 0.06), head_cy + int(h * 0.26)],
             start=135, end=305, fill=LINE, width=3)
    # Mouth (slight smile)
    draw.arc([cx - int(h * 0.20), head_cy + int(h * 0.28),
              cx + int(h * 0.20), head_cy + int(h * 0.45)],
             start=10, end=170, fill=LINE, width=3)
    # Brows
    brow_y = eye_y - int(eh * 1.44)
    for (bx, side) in [(cx - sep, -1), (cx + sep, 1)]:
        pts = [(bx + side * int(h * 0.20), brow_y),
               (bx, brow_y - int(h * 0.02)),
               (bx - side * int(h * 0.20), brow_y + int(h * 0.01))]
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=HAIR, width=2)

    # --- NECK ---
    neck_top = head_cy + head_r - int(h * 0.05)
    neck_bot = neck_top + int(h * 0.16)
    neck_w   = int(h * 0.12)
    draw.rectangle([cx - neck_w, neck_top, cx + neck_w, neck_bot], fill=SKIN)
    draw.rectangle([cx - neck_w, neck_top, cx + neck_w, neck_bot],
                   outline=LINE, width=3)

    # --- HOODIE BODY (A-line trapezoid) ---
    torso_top = neck_bot
    torso_bot = top_y + int(h * 2.50)
    top_w     = int(h * 0.40)
    bot_w     = int(h * 0.55)   # A-line: wider at hem
    torso_pts = [
        (cx - top_w, torso_top),
        (cx + top_w, torso_top),
        (cx + bot_w, torso_bot),
        (cx - bot_w, torso_bot),
    ]
    draw.polygon(torso_pts, fill=HOODIE)
    # Shadow flank
    draw.polygon([
        (cx + top_w - int(h * 0.08), torso_top),
        (cx + top_w, torso_top),
        (cx + bot_w, torso_bot),
        (cx + bot_w - int(h * 0.12), torso_bot),
    ], fill=HOODIE_SH)
    draw.polygon(torso_pts, outline=LINE, width=3)
    # Hood rim
    draw.rectangle([cx - top_w + 4, torso_top,
                    cx + top_w - 4, torso_top + int(h * 0.10)],
                   fill=HOOD_LINING)
    # Pixel accent
    px_accent(draw, cx - int(h * 0.16), torso_top + int(h * 0.12),
              int(h * 0.32), int(h * 0.24))
    # Pocket
    draw.rectangle([cx - int(h * 0.18), torso_bot - int(h * 0.14),
                    cx + int(h * 0.18), torso_bot],
                   fill=HOODIE_SH, outline=LINE, width=2)

    # --- ARMS ---
    arm_w  = int(h * 0.14)
    arm_h  = int(h * 0.50)
    # Left arm (slightly down)
    draw.rectangle([cx - top_w - arm_w + int(h * 0.02), torso_top + int(h * 0.04),
                    cx - top_w + int(h * 0.02), torso_top + int(h * 0.04) + arm_h],
                   fill=HOODIE, outline=LINE, width=3)
    # Right arm
    draw.rectangle([cx + top_w - int(h * 0.02), torso_top + int(h * 0.04),
                    cx + top_w + arm_w - int(h * 0.02), torso_top + int(h * 0.04) + arm_h],
                   fill=HOODIE, outline=LINE, width=3)
    hand_r = int(h * 0.11)
    for (hx, hy_off) in [(cx - top_w - arm_w // 2 + int(h * 0.02),
                           torso_top + int(h * 0.04) + arm_h),
                          (cx + top_w + arm_w // 2 - int(h * 0.02),
                           torso_top + int(h * 0.04) + arm_h)]:
        draw.ellipse([hx - hand_r, hy_off - hand_r * 2 // 3,
                      hx + hand_r, hy_off + hand_r * 2 // 3],
                     fill=SKIN, outline=LINE, width=3)

    # --- PANTS ---
    pants_top = torso_bot
    pants_bot = top_y + int(h * 3.05)
    leg_w     = int(h * 0.18)
    gap       = int(h * 0.02)
    for side in [-1, 1]:
        lx0 = cx + side * gap
        lx1 = cx + side * (gap + leg_w + int(h * 0.16))
        if side < 0:
            lx0, lx1 = lx1, lx0
        draw.rectangle([lx0, pants_top, lx1, pants_bot], fill=PANTS)
        draw.rectangle([lx0, pants_top, lx1, pants_bot], outline=LINE, width=3)

    # --- SHOES (oversized with chunky sole) ---
    shoe_y0 = pants_bot
    shoe_w  = int(h * 0.30)
    shoe_h  = int(h * 0.16)
    sole_h  = int(h * 0.10)
    for side in [-1, 1]:
        sx = cx + side * (gap + leg_w // 2 + int(h * 0.10))
        # Sole (chunky)
        draw.ellipse([sx - shoe_w + 2, shoe_y0 + shoe_h - sole_h // 2,
                      sx + shoe_w - 2, shoe_y0 + shoe_h + sole_h],
                     fill=SHOE_SOLE)
        # Upper
        draw.ellipse([sx - shoe_w + 4, shoe_y0 - int(h * 0.04),
                      sx + shoe_w - 4, shoe_y0 + shoe_h],
                     fill=SHOE)
        draw.ellipse([sx - shoe_w + 4, shoe_y0 - int(h * 0.04),
                      sx + shoe_w - 4, shoe_y0 + shoe_h],
                     outline=LINE, width=3)
        # Laces (Electric Cyan)
        for li in range(3):
            ly = shoe_y0 + li * 3
            draw.line([sx - int(shoe_w * 0.35), ly,
                       sx + int(shoe_w * 0.35), ly],
                      fill=LACES, width=1)

    # Ground shadow
    sh_y = shoe_y0 + shoe_h + sole_h
    draw.ellipse([cx - int(h * 0.70), sh_y,
                  cx + int(h * 0.70), sh_y + int(h * 0.08)], fill=SHADOW_COL)


# ── 3/4 VIEW ──────────────────────────────────────────────────────────────────

def render_three_quarter(draw, cx, base_y):
    S = SCALE
    h = int(hu() * S)
    top_y   = base_y - int(CHAR_DRAW_H * S)
    head_cy = top_y + h

    head_r = int(h * 0.48)   # slightly foreshortened
    # Near ear
    ear_r = int(h * 0.13)
    ear_y = head_cy + int(h * 0.12)
    draw.ellipse([cx - head_r - ear_r + 4, ear_y - ear_r,
                  cx - head_r + ear_r + 4, ear_y + ear_r],
                 fill=SKIN, outline=LINE, width=3)
    draw.ellipse([cx - head_r, head_cy - head_r,
                  cx + head_r, head_cy + head_r], fill=SKIN)

    # Hair
    hair_top = head_cy - int(h * 0.68)
    hair_mid = head_cy - int(h * 0.43)
    draw.ellipse([cx - int(h * 0.55), hair_top,
                  cx + int(h * 0.48), hair_mid + int(h * 0.12)], fill=HAIR)
    draw.ellipse([cx - int(h * 0.52), hair_top + int(h * 0.05),
                  cx - int(h * 0.05), hair_mid + int(h * 0.20)], fill=HAIR)
    draw.arc([cx - int(h * 0.24), hair_top + int(h * 0.05),
              cx + int(h * 0.24), hair_top + int(h * 0.18)],
             start=200, end=340, fill=HAIR_HL, width=3)
    draw.ellipse([cx - head_r, head_cy - head_r,
                  cx + head_r, head_cy + head_r], outline=LINE, width=4)

    # Eyes (3/4 — near eye slightly larger)
    eye_y  = head_cy + int(h * 0.04)
    # C32 fix: ew = int(head_r * 0.22) — head_r is radius, not height
    # head_r = int(h * 0.48) for 3/4 view (foreshortened)
    ew, eh = int(head_r * 0.22), int(head_r * 0.15)
    ew_far = int(ew * 0.72)
    for (ex, ew_i) in [(cx - int(h * 0.28), ew),
                        (cx + int(h * 0.20), ew_far)]:
        draw.ellipse([ex - ew_i, eye_y - eh, ex + ew_i, eye_y + eh], fill=EYE_W)
        ir = int(ew_i * 0.68)
        draw.ellipse([ex - int(ir * 0.7), eye_y - int(min(ir, eh - 2) * 0.7),
                      ex + int(ir * 0.7), eye_y + int(min(ir, eh - 2) * 0.7)],
                     fill=EYE_IRIS)
        draw.ellipse([ex - int(ir * 0.4), eye_y - int(ir * 0.4),
                      ex + int(ir * 0.4), eye_y + int(ir * 0.4)], fill=EYE_PUP)
        draw.ellipse([ex - int(ir * 0.3), eye_y - int(eh * 0.36),
                      ex - int(ir * 0.3) + 3, eye_y - int(eh * 0.36) + 4], fill=EYE_HL)
        draw.ellipse([ex - ew_i, eye_y - eh, ex + ew_i, eye_y + eh],
                     outline=LINE, width=3)
    draw.arc([cx - int(h * 0.06), head_cy + int(h * 0.16),
              cx + int(h * 0.07), head_cy + int(h * 0.26)],
             start=135, end=305, fill=LINE, width=3)
    draw.arc([cx - int(h * 0.15), head_cy + int(h * 0.28),
              cx + int(h * 0.20), head_cy + int(h * 0.45)],
             start=10, end=170, fill=LINE, width=3)

    # Neck
    neck_top = head_cy + head_r - int(h * 0.05)
    neck_bot = neck_top + int(h * 0.16)
    draw.rectangle([cx - int(h * 0.11), neck_top, cx + int(h * 0.11), neck_bot],
                   fill=SKIN, outline=LINE, width=3)

    # Torso (3/4 — shifted slightly)
    off     = int(h * 0.04)
    torso_top = neck_bot
    torso_bot = top_y + int(h * 2.50)
    top_w   = int(h * 0.38)
    bot_w   = int(h * 0.52)
    torso_pts = [
        (cx - off - top_w, torso_top),
        (cx - off + top_w, torso_top),
        (cx - off + bot_w, torso_bot),
        (cx - off - bot_w, torso_bot),
    ]
    draw.polygon(torso_pts, fill=HOODIE)
    draw.polygon([
        (cx - off + top_w - int(h * 0.08), torso_top),
        (cx - off + top_w, torso_top),
        (cx - off + bot_w, torso_bot),
        (cx - off + bot_w - int(h * 0.12), torso_bot),
    ], fill=HOODIE_SH)
    draw.polygon(torso_pts, outline=LINE, width=3)
    draw.rectangle([cx - off - top_w + 4, torso_top,
                    cx - off + top_w - 4, torso_top + int(h * 0.10)],
                   fill=HOOD_LINING)
    px_accent(draw, cx - off - int(h * 0.14), torso_top + int(h * 0.12),
              int(h * 0.28), int(h * 0.22), seed=14)

    # Arms
    arm_w = int(h * 0.13)
    arm_h = int(h * 0.50)
    draw.rectangle([cx - off - top_w - arm_w + int(h * 0.02), torso_top + int(h * 0.04),
                    cx - off - top_w + int(h * 0.02), torso_top + int(h * 0.04) + arm_h],
                   fill=HOODIE, outline=LINE, width=3)
    draw.rectangle([cx - off + top_w - int(h * 0.02), torso_top + int(h * 0.04),
                    cx - off + top_w + arm_w - int(h * 0.02),
                    torso_top + int(h * 0.04) + int(arm_h * 0.88)],
                   fill=HOODIE_SH, outline=LINE, width=3)
    hand_r = int(h * 0.11)
    draw.ellipse([cx - off - top_w - arm_w // 2 - hand_r + int(h * 0.02),
                  torso_top + int(h * 0.04) + arm_h - hand_r * 2 // 3,
                  cx - off - top_w - arm_w // 2 + hand_r + int(h * 0.02),
                  torso_top + int(h * 0.04) + arm_h + hand_r * 2 // 3],
                 fill=SKIN, outline=LINE, width=3)

    # Pants + shoes similar to front
    pants_top = torso_bot
    pants_bot = top_y + int(h * 3.05)
    gap = int(h * 0.02)
    for side in [-1, 1]:
        lx0 = cx - off + side * gap
        lx1 = cx - off + side * (gap + int(h * 0.34))
        if side < 0:
            lx0, lx1 = lx1, lx0
        draw.rectangle([lx0, pants_top, lx1, pants_bot], fill=PANTS)
        draw.rectangle([lx0, pants_top, lx1, pants_bot], outline=LINE, width=3)

    shoe_y0 = pants_bot
    shoe_w  = int(h * 0.28)
    shoe_h  = int(h * 0.16)
    sole_h  = int(h * 0.10)
    for side in [-1, 1]:
        sx = cx - off + side * int(h * 0.22)
        draw.ellipse([sx - shoe_w + 2, shoe_y0 + shoe_h - sole_h // 2,
                      sx + shoe_w - 2, shoe_y0 + shoe_h + sole_h], fill=SHOE_SOLE)
        draw.ellipse([sx - shoe_w + 4, shoe_y0 - int(h * 0.04),
                      sx + shoe_w - 4, shoe_y0 + shoe_h], fill=SHOE)
        draw.ellipse([sx - shoe_w + 4, shoe_y0 - int(h * 0.04),
                      sx + shoe_w - 4, shoe_y0 + shoe_h], outline=LINE, width=3)
        for li in range(3):
            draw.line([sx - int(shoe_w * 0.35), shoe_y0 + li * 3,
                       sx + int(shoe_w * 0.35), shoe_y0 + li * 3],
                      fill=LACES, width=1)
    sh_y = shoe_y0 + shoe_h + sole_h
    draw.ellipse([cx - off - int(h * 0.65), sh_y,
                  cx - off + int(h * 0.65), sh_y + int(h * 0.08)], fill=SHADOW_COL)


# ── SIDE VIEW ─────────────────────────────────────────────────────────────────

def render_side(draw, cx, base_y):
    """Side profile — Luma faces right."""
    S = SCALE
    h = int(hu() * S)
    top_y   = base_y - int(CHAR_DRAW_H * S)
    head_cy = top_y + h

    # Head profile
    head_front_x = cx + int(h * 0.48)
    head_back_x  = cx - int(h * 0.44)
    head_top_y   = head_cy - int(h * 0.52)
    head_bot_y   = head_cy + int(h * 0.52)

    # Ear (visible on side)
    ear_cx = cx - int(h * 0.04)
    ear_cy = head_cy + int(h * 0.12)
    ear_rx = int(h * 0.12)
    ear_ry = int(h * 0.16)
    draw.ellipse([ear_cx - ear_rx, ear_cy - ear_ry,
                  ear_cx + ear_rx, ear_cy + ear_ry], fill=SKIN)
    draw.ellipse([ear_cx - ear_rx, ear_cy - ear_ry,
                  ear_cx + ear_rx, ear_cy + ear_ry], outline=LINE, width=3)

    # Head shape (profile polygon)
    head_pts = [
        (cx, head_top_y - int(h * 0.04)),
        (head_front_x - int(h * 0.10), head_top_y),
        (head_front_x, head_cy - int(h * 0.20)),
        (head_front_x + int(h * 0.06), head_cy + int(h * 0.10)),
        (head_front_x - int(h * 0.04), head_cy + int(h * 0.32)),
        (head_front_x - int(h * 0.10), head_cy + int(h * 0.44)),
        (cx - int(h * 0.14), head_bot_y),
        (head_back_x + int(h * 0.04), head_cy + int(h * 0.28)),
        (head_back_x, head_cy),
        (head_back_x + int(h * 0.04), head_cy - int(h * 0.38)),
    ]
    draw.polygon(head_pts, fill=SKIN)
    draw.polygon(head_pts, outline=LINE, width=4)

    # Hair (profile — dark mass over back of skull)
    hair_pts = [
        (cx + int(h * 0.02), head_top_y - int(h * 0.10)),
        (head_front_x - int(h * 0.16), head_top_y + int(h * 0.04)),
        (head_front_x - int(h * 0.26), head_top_y + int(h * 0.16)),
        (cx - int(h * 0.06), head_top_y + int(h * 0.10)),
        (head_back_x - int(h * 0.02), head_cy - int(h * 0.20)),
        (head_back_x + int(h * 0.04), head_cy + int(h * 0.06)),
        (head_back_x + int(h * 0.08), head_cy + int(h * 0.22)),
    ]
    draw.polygon(hair_pts + [(cx + int(h * 0.02), head_top_y - int(h * 0.10))],
                 fill=HAIR)
    draw.arc([cx - int(h * 0.04), head_top_y - int(h * 0.04),
              cx + int(h * 0.08), head_top_y + int(h * 0.12)],
             start=260, end=60, fill=HAIR_HL, width=3)

    # Eye (single, profile)
    eye_cx = head_front_x - int(h * 0.14)
    eye_cy = head_cy - int(h * 0.10)
    # C32 fix: ew = int(head_r * 0.16) — head_r = int(h * 0.50)
    # Side head has no explicit head_r circle; use h*0.50 as reference radius
    _side_head_r = int(h * 0.50)
    ew, eh = int(_side_head_r * 0.16), int(_side_head_r * 0.13)
    draw.ellipse([eye_cx - ew, eye_cy - eh, eye_cx + ew, eye_cy + eh], fill=EYE_W)
    ir = int(ew * 0.68)
    draw.ellipse([eye_cx - int(ir * 0.7), eye_cy - int(eh * 0.7),
                  eye_cx + int(ir * 0.7), eye_cy + int(eh * 0.7)], fill=EYE_IRIS)
    draw.ellipse([eye_cx - int(ir * 0.4), eye_cy - int(ir * 0.4),
                  eye_cx + int(ir * 0.4), eye_cy + int(ir * 0.4)], fill=EYE_PUP)
    draw.ellipse([eye_cx - ir - 3, eye_cy - eh + 2,
                  eye_cx - ir + 2, eye_cy - eh + 6], fill=EYE_HL)
    draw.ellipse([eye_cx - ew, eye_cy - eh, eye_cx + ew, eye_cy + eh],
                 outline=LINE, width=3)
    # Brow (single)
    brow_y = eye_cy - eh - int(h * 0.08)
    draw.arc([eye_cx - int(h * 0.16), brow_y - int(h * 0.04),
              eye_cx + int(h * 0.12), brow_y + int(h * 0.04)],
             start=190, end=0, fill=HAIR, width=2)
    # Nose (profile)
    nose_x = head_front_x + int(h * 0.05)
    nose_y = head_cy + int(h * 0.10)
    draw.arc([nose_x - int(h * 0.12), nose_y - int(h * 0.10),
              nose_x + int(h * 0.04), nose_y + int(h * 0.14)],
             start=270, end=90, fill=SKIN_SH, width=3)
    # Mouth
    mouth_y = head_cy + int(h * 0.40)
    draw.line([head_front_x - int(h * 0.06), mouth_y,
               head_front_x + int(h * 0.08), mouth_y + int(h * 0.02)],
              fill=LINE, width=3)

    # Neck
    neck_top = head_bot_y - int(h * 0.32)
    neck_bot = neck_top + int(h * 0.30)
    draw.rectangle([cx - int(h * 0.14), neck_top,
                    cx + int(h * 0.14), neck_bot], fill=SKIN)
    draw.rectangle([cx - int(h * 0.14), neck_top,
                    cx + int(h * 0.14), neck_bot], outline=LINE, width=3)

    # Hoodie body (side view — depth visible)
    torso_top   = neck_bot
    torso_bot   = top_y + int(h * 2.50)
    torso_front = cx + int(h * 0.32)   # chest face
    torso_back  = cx - int(h * 0.26)   # back
    # Subtle pixel colors on front face
    for i in range(3):
        y0 = torso_top + i * int((torso_bot - torso_top) // 3)
        y1 = y0 + int((torso_bot - torso_top) // 3)
        col = HOODIE if i != 1 else HOODIE_SH
        draw.rectangle([torso_back, y0, torso_front, y1], fill=col)
    draw.line([torso_front, torso_top, torso_front, torso_bot], fill=LINE, width=3)
    draw.line([torso_back, torso_top, torso_back, torso_bot], fill=LINE, width=3)
    draw.line([torso_back, torso_top, torso_front, torso_top], fill=LINE, width=3)
    draw.line([torso_back, torso_bot, torso_front, torso_bot], fill=LINE, width=3)
    # Hood rim at neckline
    draw.rectangle([torso_back + 2, torso_top,
                    torso_front - 2, torso_top + int(h * 0.10)],
                   fill=HOOD_LINING)
    # Pocket (side — slightly raised bump at hem)
    draw.rectangle([torso_back + int(h * 0.04), torso_bot - int(h * 0.14),
                    torso_front - int(h * 0.04), torso_bot],
                   fill=HOODIE_SH, outline=LINE, width=2)

    # Near arm (front)
    arm_front = torso_front
    arm_top   = torso_top + int(h * 0.06)
    arm_bot   = arm_top + int(h * 0.52)
    arm_d     = int(h * 0.22)
    draw.rectangle([arm_front - arm_d, arm_top, arm_front, arm_bot],
                   fill=HOODIE, outline=LINE, width=3)
    hand_r = int(h * 0.11)
    draw.ellipse([arm_front - arm_d // 2 - hand_r, arm_bot - hand_r * 2 // 3,
                  arm_front - arm_d // 2 + hand_r, arm_bot + hand_r * 2 // 3],
                 fill=SKIN, outline=LINE, width=3)

    # Pants (side)
    pants_top  = torso_bot
    pants_bot  = top_y + int(h * 3.05)
    near_front = torso_front
    near_back  = cx - int(h * 0.10)
    far_back   = near_back - (near_front - near_back)
    draw.rectangle([near_back, pants_top, near_front, pants_bot], fill=PANTS)
    draw.line([(near_back + near_front) // 2, pants_top,
               (near_back + near_front) // 2, pants_bot],
              fill=PANTS_SH, width=2)
    draw.rectangle([near_back, pants_top, near_front, pants_bot],
                   outline=LINE, width=3)
    draw.rectangle([far_back, pants_top, near_back, pants_bot], fill=PANTS_SH)
    draw.line([far_back, pants_top, far_back, pants_bot], fill=LINE, width=3)

    # Shoes (side — oversized, profile length visible, chunky sole)
    shoe_y0  = pants_bot
    shoe_len = int(h * 0.62)
    shoe_h_s = int(h * 0.18)
    sole_h   = int(h * 0.12)
    shoe_x0  = cx - int(h * 0.18)
    shoe_x1  = shoe_x0 + shoe_len
    # Sole (chunky Terracotta)
    draw.rectangle([shoe_x0, shoe_y0 + shoe_h_s,
                    shoe_x1, shoe_y0 + shoe_h_s + sole_h], fill=SHOE_SOLE)
    draw.rectangle([shoe_x0, shoe_y0 + shoe_h_s,
                    shoe_x1, shoe_y0 + shoe_h_s + sole_h],
                   outline=LINE, width=3)
    # Upper (canvas, rounded toe)
    draw.rectangle([shoe_x0, shoe_y0 - int(h * 0.04),
                    shoe_x1 - int(h * 0.12), shoe_y0 + shoe_h_s], fill=SHOE)
    draw.ellipse([shoe_x1 - int(h * 0.24), shoe_y0 + int(h * 0.01),
                  shoe_x1, shoe_y0 + shoe_h_s], fill=SHOE)
    draw.polygon([
        (shoe_x0, shoe_y0 - int(h * 0.04)),
        (shoe_x1 - int(h * 0.12), shoe_y0 - int(h * 0.04)),
        (shoe_x1, shoe_y0 + int(h * 0.01)),
        (shoe_x1, shoe_y0 + shoe_h_s),
        (shoe_x0, shoe_y0 + shoe_h_s),
    ], outline=LINE, width=3)
    # Cyan laces
    for li in range(3):
        lx0 = shoe_x0 + int(shoe_len * 0.15)
        lx1 = shoe_x0 + int(shoe_len * 0.70)
        ly  = shoe_y0 + li * 4
        draw.line([lx0, ly, lx1, ly], fill=LACES, width=2)
    # Far shoe (heel only)
    far_shoe_x0 = shoe_x0 - int(h * 0.14)
    draw.rectangle([far_shoe_x0, shoe_y0 - int(h * 0.02),
                    shoe_x0 + int(h * 0.16), shoe_y0 + shoe_h_s + sole_h],
                   fill=SHOE_SOLE, outline=LINE, width=2)

    sh_y = shoe_y0 + shoe_h_s + sole_h
    draw.ellipse([cx - int(h * 0.70), sh_y,
                  cx + int(h * 0.70), sh_y + int(h * 0.08)], fill=SHADOW_COL)


# ── BACK VIEW ─────────────────────────────────────────────────────────────────

def render_back(draw, cx, base_y):
    S = SCALE
    h = int(hu() * S)
    top_y   = base_y - int(CHAR_DRAW_H * S)
    head_cy = top_y + h

    head_r = int(h * 0.50)
    ear_r  = int(h * 0.13)
    ear_y  = head_cy + int(h * 0.12)
    for side in [-1, 1]:
        draw.ellipse([cx + side * head_r - ear_r + side * (-4),
                      ear_y - ear_r,
                      cx + side * head_r + ear_r + side * (-4),
                      ear_y + ear_r], fill=SKIN, outline=LINE, width=3)
    draw.ellipse([cx - head_r, head_cy - head_r,
                  cx + head_r, head_cy + head_r], fill=SKIN)

    # Hair (back — full mass)
    hair_top = head_cy - int(h * 0.70)
    hair_mid = head_cy - int(h * 0.44)
    draw.ellipse([cx - int(h * 0.56), hair_top,
                  cx + int(h * 0.54), hair_mid + int(h * 0.12)], fill=HAIR)
    draw.ellipse([cx - int(h * 0.42), hair_top,
                  cx + int(h * 0.42), hair_mid + int(h * 0.10)], fill=HAIR)
    # Curls / texture at back
    draw.arc([cx - int(h * 0.28), hair_top + int(h * 0.06),
              cx + int(h * 0.28), hair_top + int(h * 0.20)],
             start=200, end=340, fill=HAIR_HL, width=3)
    draw.ellipse([cx - head_r, head_cy - head_r,
                  cx + head_r, head_cy + head_r], outline=LINE, width=4)

    # Neck
    neck_top = head_cy + head_r - int(h * 0.05)
    neck_bot = neck_top + int(h * 0.16)
    draw.rectangle([cx - int(h * 0.12), neck_top, cx + int(h * 0.12), neck_bot],
                   fill=SKIN, outline=LINE, width=3)

    # Hoodie back (hood visible — larger trapezoid)
    torso_top = neck_bot
    torso_bot = top_y + int(h * 2.50)
    top_w     = int(h * 0.42)
    bot_w     = int(h * 0.56)
    torso_pts = [
        (cx - top_w, torso_top),
        (cx + top_w, torso_top),
        (cx + bot_w, torso_bot),
        (cx - bot_w, torso_bot),
    ]
    draw.polygon(torso_pts, fill=HOODIE)
    draw.polygon(torso_pts, outline=LINE, width=3)
    # Hood (visible from back — rounded shape at neckline top)
    hood_pts = [
        (cx - top_w + int(h * 0.04), torso_top),
        (cx - int(h * 0.08), torso_top - int(h * 0.20)),
        (cx + int(h * 0.08), torso_top - int(h * 0.20)),
        (cx + top_w - int(h * 0.04), torso_top),
    ]
    draw.polygon(hood_pts, fill=HOODIE_SH)
    draw.polygon(hood_pts, outline=LINE, width=3)
    # Pocket (back — just hem seam)
    draw.line([cx - int(h * 0.18), torso_bot - int(h * 0.14),
               cx + int(h * 0.18), torso_bot - int(h * 0.14)],
              fill=HOODIE_SH, width=2)

    # Arms (back)
    arm_w = int(h * 0.14)
    arm_h = int(h * 0.50)
    for side in [-1, 1]:
        sx0 = cx + side * top_w + (int(h * 0.02) if side < 0 else -int(h * 0.02)) - (arm_w if side < 0 else 0)
        sx1 = sx0 + arm_w
        draw.rectangle([sx0, torso_top + int(h * 0.04),
                        sx1, torso_top + int(h * 0.04) + arm_h],
                       fill=HOODIE_SH, outline=LINE, width=3)
    hand_r = int(h * 0.11)
    for side in [-1, 1]:
        hx = cx + side * (top_w + arm_w // 2 - int(h * 0.02) - (arm_w if side < 0 else 0))
        hy = torso_top + int(h * 0.04) + arm_h
        draw.ellipse([hx - hand_r, hy - hand_r * 2 // 3,
                      hx + hand_r, hy + hand_r * 2 // 3],
                     fill=SKIN, outline=LINE, width=3)

    # Pants (back)
    pants_top = torso_bot
    pants_bot = top_y + int(h * 3.05)
    gap = int(h * 0.02)
    for side in [-1, 1]:
        lx0 = cx + side * gap
        lx1 = cx + side * (gap + int(h * 0.34))
        if side < 0:
            lx0, lx1 = lx1, lx0
        draw.rectangle([lx0, pants_top, lx1, pants_bot], fill=PANTS)
        draw.rectangle([lx0, pants_top, lx1, pants_bot], outline=LINE, width=3)

    # Shoes
    shoe_y0 = pants_bot
    shoe_w  = int(h * 0.28)
    shoe_h  = int(h * 0.16)
    sole_h  = int(h * 0.10)
    for side in [-1, 1]:
        sx = cx + side * int(h * 0.22)
        draw.ellipse([sx - shoe_w + 2, shoe_y0 + shoe_h - sole_h // 2,
                      sx + shoe_w - 2, shoe_y0 + shoe_h + sole_h], fill=SHOE_SOLE)
        draw.ellipse([sx - shoe_w + 4, shoe_y0 - int(h * 0.04),
                      sx + shoe_w - 4, shoe_y0 + shoe_h], fill=SHOE)
        draw.ellipse([sx - shoe_w + 4, shoe_y0 - int(h * 0.04),
                      sx + shoe_w - 4, shoe_y0 + shoe_h], outline=LINE, width=3)
    sh_y = shoe_y0 + shoe_h + sole_h
    draw.ellipse([cx - int(h * 0.65), sh_y,
                  cx + int(h * 0.65), sh_y + int(h * 0.08)], fill=SHADOW_COL)


# ── MAIN ASSEMBLY ─────────────────────────────────────────────────────────────

def build_turnaround():
    canvas_w2 = CANVAS_W * SCALE
    canvas_h2 = CANVAS_H * SCALE
    img2  = Image.new("RGB", (canvas_w2, canvas_h2), CANVAS_BG)
    draw2 = ImageDraw.Draw(img2)

    for v in range(N_VIEWS):
        x0 = v * VIEW_W * SCALE
        x1 = (v + 1) * VIEW_W * SCALE
        col = (245, 240, 232) if v % 2 == 0 else (240, 236, 228)
        draw2.rectangle([x0, 0, x1, canvas_h2], fill=col)

    render_fns = [render_front, render_three_quarter, render_side, render_back]
    for v, fn in enumerate(render_fns):
        panel_cx = v * VIEW_W * SCALE + VIEW_W * SCALE // 2
        base_y2  = (VIEW_H - LABEL_H) * SCALE - int(BODY_H * SCALE * 0.04)
        fn(draw2, panel_cx, base_y2)

    for v in range(1, N_VIEWS):
        x = v * VIEW_W * SCALE
        draw2.line([(x, 0), (x, canvas_h2)], fill=(180, 170, 155), width=2 * SCALE)

    img  = img2.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        font_sub   = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = font_title
        font_sub   = font_title

    title = "LUMA — Character Turnaround v004  |  Luma & the Glitchkin  |  Cycle 32 / Rin Yamamoto"
    sub   = "v004: Eye-width canonical fix — ew=int(head_r*0.22), head_r=radius | v003 line weights retained"
    draw.text((16, 6), title, fill=LABEL_COL, font=font_title)
    draw.text((16, 28), sub, fill=(120, 100, 80), font=font_sub)

    for v, label in enumerate(VIEWS):
        lx = v * VIEW_W + VIEW_W // 2
        ly = VIEW_H - LABEL_H + 6
        try:
            lb = draw.textbbox((0, 0), label, font=font_label)
            lw = lb[2] - lb[0]
            draw.text((lx - lw // 2, ly), label, fill=LABEL_COL, font=font_label)
        except Exception:
            draw.text((lx - 20, ly), label, fill=LABEL_COL)

    for v in range(1, N_VIEWS):
        x = v * VIEW_W
        draw.line([(x, 0), (x, CANVAS_H)], fill=(150, 138, 120), width=1)

    return img


def main():
    out_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "characters", "main", "turnarounds"
    )
    os.makedirs(out_dir, exist_ok=True)

    img = build_turnaround()
    # Image size rule: ≤ 1280px in both dimensions
    img.thumbnail((1280, 1280), Image.LANCZOS)
    out_path = os.path.join(out_dir, "LTG_CHAR_luma_turnaround.png")
    img.save(out_path)
    print(f"Saved: {out_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}px")
    print("  v004: Eye-width canonical fix — ew=int(head_r*0.22) radius-based | 3.2 heads | 4 views")


if __name__ == "__main__":
    main()
