#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_character_lineup.py
Character Lineup Generator — Luma & the Glitchkin
Cycle 44 / v009: Miri wooden hairpin rename (P0 cultural identity correction).

Cycle 44 changes (Maya Santos, C44):
  - draw_miri_lineup(): renamed chopstick_col → hairpin_col; accessory is now
    "wooden hairpins" per design correction. No geometry or color change.

Cycle 42 / v008: Two-tier ground plane staging (Lee Tanaka brief C42).

Cycle 42 changes (Maya Santos, Character Designer):
  - TWO-TIER GROUND PLANE: FG tier (Luma + Byte) at canvas_h×0.78;
    BG tier (Cosmo + Miri + Glitch) at canvas_h×0.70.
  - NEW CHARACTER ORDER (left → right): Cosmo | Miri | Luma | Byte | Glitch
    (Luma center-protagonist; Byte at her right on same FG tier;
    Cosmo bookends left; Miri flanks right of center; Glitch rightmost)
  - FG_SCALE = 1.03: Luma and Byte drawn at +3% height post-calculation.
    Proportion constants unchanged — uniform post-scale only.
  - SHADOW LINES: subtle 2px line at each tier (warm gray FG, cool gray BG).
  - CANVAS HEIGHT bumped to 560px body for BG/FG tier geometry.
  - Annotation bar notes FG/BG tier staging.
  - Addresses Daisuke C16 "inventory not cast" flag + C15 Luma power balance.
  - Closes lineup_staging_brief_c42.md spec (Lee Tanaka).

Cycle 33 changes (Alex Chen, Art Director):
  - BYTE_SH: (0, 144, 176) → (0, 168, 180) — canonical Deep Cyan GL-01a #00A8B4
  - MIRI_SLIPPER: (90, 122, 90) → (196, 144, 122) — warm apricot #C4907A

Cycle 29 changes (Maya Santos, Character Designer):
  - LUMA_HEADS: 3.5 → 3.2 (canonical proportion directive C28)
  - Eye width: int(s*28) → int(r*0.22) per canonical spec

Cycle 27 changes (Maya Santos, Character Designer):
  - Luma rebuilt to v006 canonical style (curl cloud hair, cheek nubs, bezier mouth).

Prior history:
  Cycle 24 (Maya Santos): Added Glitch.
  Cycle 14 (Alex Chen): Engineering dimension arrow for Byte float gap.
  Cycle 12 (Alex Chen): Ground-floor annotation.
  Cycle 10 (Alex Chen): Initial four-character lineup.

Output: /home/wipkat/team/output/characters/main/LTG_CHAR_character_lineup.png
Usage: python3 LTG_TOOL_character_lineup.py
"""
from PIL import Image, ImageDraw, ImageFont
import math

# ── Canvas ────────────────────────────────────────────────────────────────────
BG           = (250, 248, 244)
PANEL_BG     = (245, 241, 235)
LINE_COL     = (59, 40, 32)       # #3B2820 Deep Cocoa
LABEL_COL    = (50, 40, 35)
TICK_COL     = (160, 148, 138)
BASELINE_COL = (180, 165, 150)

# ── Height system ─────────────────────────────────────────────────────────────
LUMA_RENDER_H = 280
LUMA_HEADS    = 3.2   # v006 FIX: was 3.5, canonical is 3.2 (C28 directive)
HEAD_UNIT     = LUMA_RENDER_H / LUMA_HEADS   # ~87.5px

COSMO_HEADS   = 4.0
COSMO_H       = int(COSMO_HEADS * HEAD_UNIT)  # ~320px

MIRI_HEADS    = 3.2
MIRI_H        = int(MIRI_HEADS * HEAD_UNIT)   # ~256px

BYTE_H        = int(LUMA_RENDER_H * 0.58)     # ~162px

# Glitch: floating antagonist, slightly taller than Byte
GLITCH_H      = int(BYTE_H * 1.05)            # ~170px

# ── Layout ────────────────────────────────────────────────────────────────────
CHAR_SPACING  = 240     # tighter spacing to fit 5 characters
LEFT_MARGIN   = 100
N_CHARS       = 5
IMG_W         = LEFT_MARGIN * 2 + CHAR_SPACING * (N_CHARS - 1) + 180
TITLE_H       = 50
LABEL_AREA    = 90     # slightly taller for tier annotation
IMG_H         = 560    # bumped for two-tier geometry (was computed from HEADROOM)

# ── Two-tier ground planes (v008) ─────────────────────────────────────────────
# FG tier: Luma + Byte — visually closest to camera
# BG tier: Cosmo + Miri + Glitch — one step behind
FG_GROUND_Y  = int(IMG_H * 0.78)   # ~436 — FG chars stand here
BG_GROUND_Y  = int(IMG_H * 0.70)   # ~392 — BG chars stand here

# Legacy alias: BASELINE_Y used by existing height-marker + annotation helpers
# Points to FG tier (the reference tier for head-unit comparisons)
BASELINE_Y   = FG_GROUND_Y

# ── FG scale factor (post-calculation, proportion constants unchanged) ────────
FG_SCALE     = 1.03   # +3% height for FG characters (Luma + Byte)
BG_SCALE     = 1.00   # baseline for BG characters

# Scaled render heights (used for drawing and labels)
LUMA_RENDER_H_FG  = int(LUMA_RENDER_H * FG_SCALE)   # ~288px
BYTE_H_FG         = int(BYTE_H * FG_SCALE)           # ~167px
GLITCH_H_BG       = GLITCH_H                          # unscaled

# ── Character order: left → right ────────────────────────────────────────────
# Cosmo (left bookend) | Miri | Luma (center protagonist) | Byte | Glitch (right)
CHAR_ORDER    = ["cosmo", "miri", "luma", "byte", "glitch"]
CHAR_X        = {
    "cosmo":  LEFT_MARGIN + 60,
    "miri":   LEFT_MARGIN + 60 + CHAR_SPACING,
    "luma":   LEFT_MARGIN + 60 + CHAR_SPACING * 2,
    "byte":   LEFT_MARGIN + 60 + CHAR_SPACING * 3 - 20,
    "glitch": LEFT_MARGIN + 60 + CHAR_SPACING * 4,
}

# Ground Y per character (FG or BG tier)
CHAR_GROUND_Y = {
    "luma":   FG_GROUND_Y,
    "byte":   FG_GROUND_Y,
    "cosmo":  BG_GROUND_Y,
    "miri":   BG_GROUND_Y,
    "glitch": BG_GROUND_Y,
}

# Draw heights (FG chars use scaled height)
CHAR_HEIGHTS  = {
    "luma":   LUMA_RENDER_H_FG,
    "byte":   BYTE_H_FG,
    "cosmo":  COSMO_H,
    "miri":   MIRI_H,
    "glitch": GLITCH_H_BG,
}
CHAR_LABELS   = {
    "luma":   f"LUMA [FG]\n3.2 heads / {LUMA_RENDER_H}px (+3%)",
    "byte":   f"BYTE [FG]\n~Luma chest / {BYTE_H}px (+3%)",
    "cosmo":  f"COSMO [BG]\n4.0 heads / {COSMO_H}px",
    "miri":   f"MIRI [BG]\n3.2 heads / {MIRI_H}px",
    "glitch": f"GLITCH [BG]\n~Byte scale / {GLITCH_H}px",
}

# ── Colors ────────────────────────────────────────────────────────────────────
# Luma — canonical palette (matches expression sheet v006 and classroom pose)
LUMA_SKIN      = (200, 136, 90)    # matches v006 SKIN
LUMA_SKIN_SH   = (160, 104, 64)    # shadow
LUMA_HAIR      = (26, 15, 10)      # matches v006 HAIR
LUMA_HAIR_HL   = (61, 31, 15)      # hair highlight
LUMA_EYE_W     = (250, 240, 220)   # matches v006 EYE_W
LUMA_EYE_IRIS  = (200, 125, 62)    # matches v006 EYE_IRIS
LUMA_EYE_PUP   = (59, 40, 32)      # matches v006 EYE_PUP
LUMA_EYE_HL    = (240, 240, 240)
LUMA_HOODIE    = (232, 114, 42)
LUMA_PANTS     = (42, 40, 80)
LUMA_SHOE_UP   = (245, 232, 208)
LUMA_SHOE_SOLE = (199, 91, 57)
PX_CYAN        = (0, 240, 255)
PX_MAG         = (255, 45, 107)

# Byte
BYTE_TEAL     = (0, 212, 232)
BYTE_HL       = (0, 240, 255)
BYTE_SH       = (0, 168, 180)  # C33 FIX: was (0, 144, 176) wrong; canonical Deep Cyan GL-01a #00A8B4
SCAR_MAG      = (255, 45, 107)
BYTE_EYE_W   = (240, 240, 245)

# Cosmo
COSMO_SKIN     = (217, 192, 154)
COSMO_HAIR     = (26, 24, 36)
COSMO_JACKET   = (168, 155, 191)
COSMO_SHIRT_B  = (91, 141, 184)
COSMO_SHIRT_G  = (122, 158, 126)
COSMO_PANTS    = (140, 136, 128)
COSMO_FRAMES   = (92, 58, 32)
COSMO_LENS_BG  = (238, 244, 255)
COSMO_SHOE     = (92, 58, 32)
COSMO_NB       = (91, 141, 184)

# Miri
MIRI_SKIN      = (140, 84, 48)
MIRI_HAIR      = (216, 208, 200)
MIRI_CARDIGAN  = (184, 92, 56)
MIRI_PANTS     = (200, 174, 138)
MIRI_SLIPPER   = (196, 144, 122)  # C33 FIX: was (90, 122, 90) Deep Sage (cool green) violates warm palette guarantee; now #C4907A Dusty Warm Apricot per Sam C32 master_palette.md correction

# Glitch
GLITCH_AMB    = (255, 140,   0)   # CORRUPT_AMBER GL-07
GLITCH_AMB_SH = (168,  76,   0)   # CORRUPT_AMB_SHADOW
GLITCH_AMB_HL = (255, 185,  80)   # warm highlight
GLITCH_HOT    = (255,  45, 107)   # HOT_MAGENTA — crack/scar
GLITCH_UV     = (123,  47, 190)   # UV_PURPLE — shadow
GLITCH_GOLD   = (232, 201,  90)   # SOFT_GOLD — pixel eye glow
GLITCH_VB     = ( 10,  10,  20)   # VOID_BLACK — outline
GLITCH_ACID   = ( 57, 255,  20)   # ACID_GREEN — pixel alive state

NEG_SPACE = BG


# ── Geometry helpers (for Luma bezier curves) ─────────────────────────────────
def _bezier3(p0, p1, p2, steps=20):
    pts = []
    for i in range(steps + 1):
        t  = i / steps
        x  = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
        y  = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        pts.append((x, y))
    return pts


def _polyline(draw, pts, color, width=1):
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill=color, width=width)


# ══════════════════════════════════════════════════════════════════════════════
# LUMA — v006 canonical construction
# Scale: s = r / 100.0 where r = head radius at lineup scale (≈37px)
# Line weights at this small scale: head=2, structure=2, detail=1
# ══════════════════════════════════════════════════════════════════════════════

def draw_luma_lineup(draw, cx, base_y, h):
    """Luma full body at lineup height h, v007 canonical construction (3.2 heads).
    v006 changes from v005:
      - hu = h / 3.2 (was h / 3.5) — 3.2 heads canonical
      - eye width = int(r * 0.22) (was int(s*28) = r*0.28) — canonical h×0.22 spec
    Head: circle + chin fill + cheek nubs.
    Hair: 8 overlapping ellipses (curl cloud).
    Eyes: near-circular with iris, pupil, highlight, eyelid arc.
    Body: hoodie trapezoid, pants, sneakers (same as v004).
    """
    hu = h / 3.2            # v006 FIX: was h / 3.5 — 3.2 heads canonical
    r  = int(hu * 0.46)     # head radius ≈ 40px (slightly larger with 3.2 heads)
    s  = r / 100.0          # scale factor from classroom reference (head_r=100)
    hy = base_y - h         # top of character (top of hair)

    # Head center: head sits above neck, positioned slightly above hy
    # In v004, head started at hy (top of hair mass). We position head_cy so
    # that head top (cy - r) aligns around hy + hair-clearance.
    head_cy = hy + int(hu * 0.46) + int(r * 0.5)

    # ── HAIR — 8 overlapping ellipses (curl cloud, classroom style) ───────────
    # Ellipses offsets from classroom reference (head_r=100), scaled by s
    # Drawn behind head (before head ellipse)
    v_off = 0
    hair_ellipses = [
        (-int(s*155), -int(s*195)+v_off, int(s*145), int(s*40)),
        (-int(s*175), -int(s*170)+v_off, -int(s*80), -int(s*60)),
        (-int(s*165), -int(s*140)+v_off, -int(s*95), -int(s*30)),
        ( int(s*80),  -int(s*160)+v_off,  int(s*155), -int(s*60)),
        ( int(s*90),  -int(s*130)+v_off,  int(s*145), -int(s*40)),
        (-int(s*60),  -int(s*215)+v_off,  int(s*20),  -int(s*140)),
        (-int(s*20),  -int(s*225)+v_off,  int(s*70),  -int(s*145)),
        (-int(s*100), -int(s*200)+v_off, -int(s*30),  -int(s*130)),
    ]
    for (x1, y1, x2, y2) in hair_ellipses:
        draw.ellipse([cx + x1, head_cy + y1, cx + x2, head_cy + y2], fill=LUMA_HAIR)

    # Foreground strand arcs (detail weight=1 at this scale)
    draw.arc([cx - int(s*60), head_cy - int(s*195) + v_off,
              cx - int(s*10), head_cy - int(s*140)],
             start=30, end=200, fill=LUMA_HAIR, width=1)
    draw.arc([cx - int(s*20), head_cy - int(s*190) + v_off,
              cx + int(s*40), head_cy - int(s*130)],
             start=10, end=190, fill=LUMA_HAIR, width=1)

    # ── HEAD — circle + chin fill + cheek nubs (v006 classroom style) ─────────
    # Main head circle — HEAD OUTLINE: width=2 (scaled from width=4 at HR=104)
    draw.ellipse([cx - r, head_cy - r, cx + r, head_cy + r + int(r * 0.15)],
                 fill=LUMA_SKIN, outline=LINE_COL, width=2)

    # Lower chin fill (softens jaw)
    chin_rx = int(r * 0.95)
    draw.ellipse([cx - chin_rx, head_cy - int(r * 0.20),
                  cx + chin_rx, head_cy + r + int(r * 0.25)], fill=LUMA_SKIN)
    # Chin arc outline — STRUCTURE: width=1 (scaled from 3)
    draw.arc([cx - chin_rx, head_cy - int(r * 0.20),
              cx + chin_rx, head_cy + r + int(r * 0.25)],
             start=0, end=180, fill=LINE_COL, width=1)

    # Cheek nubs — classroom pose characteristic — STRUCTURE: width=1
    nub_w = int(r * 0.18)
    nub_h = int(r * 0.24)
    nub_y = head_cy - int(r * 0.12)
    draw.ellipse([cx - r - nub_w + int(r * 0.06), nub_y - nub_h // 2,
                  cx - r + nub_w + int(r * 0.06), nub_y + nub_h // 2],
                 fill=LUMA_SKIN, outline=LINE_COL, width=1)
    draw.ellipse([cx + r - nub_w - int(r * 0.06), nub_y - nub_h // 2,
                  cx + r + nub_w - int(r * 0.06), nub_y + nub_h // 2],
                 fill=LUMA_SKIN, outline=LINE_COL, width=1)

    # ── EYES — near-circular, eyelid arc (v006 classroom style) ───────────────
    eye_y = head_cy - int(s * 18)
    lex   = cx - int(s * 38)
    rex   = cx + int(s * 38)
    ew    = int(r * 0.22)    # v006 FIX: was int(s*28)=r*0.28, canonical spec h×0.22
    leh   = int(r * 0.27)   # eye height scaled to match narrower width
    reh   = int(r * 0.22)   # right eye slightly less open

    for (ex, eh) in [(lex, leh), (rex, reh)]:
        # Eye white oval — STRUCTURE: width=1
        draw.ellipse([ex - ew, eye_y - eh, ex + ew, eye_y + eh],
                     fill=LUMA_EYE_W, outline=LINE_COL, width=1)
        # Iris
        iris_r = int(ew * 0.54)
        iry    = max(2, min(iris_r, eh - 1))
        draw.chord([ex - iris_r, eye_y - iry, ex + iris_r, eye_y + iry],
                   start=15, end=345, fill=LUMA_EYE_IRIS)
        # Pupil
        pr = int(iris_r * 0.50)
        if pr >= 1:
            draw.ellipse([ex - pr, eye_y - pr, ex + pr, eye_y + pr],
                         fill=LUMA_EYE_PUP)
        # Highlight
        hl_s = max(1, int(pr * 0.38))
        hl_x = ex + int(iris_r * 0.42)
        hl_y = eye_y - int(iry * 0.48)
        draw.ellipse([hl_x - hl_s, hl_y - hl_s, hl_x + hl_s, hl_y + hl_s],
                     fill=LUMA_EYE_HL)
        # Eyelid arc — STRUCTURE: width=1
        draw.arc([ex - ew, eye_y - eh, ex + ew, eye_y + eh],
                 start=200, end=340, fill=LINE_COL, width=1)

    # Brows (simple line, structure weight=1)
    brow_y = eye_y - int(leh * 1.35)
    for (bx, sign) in [(lex, -1), (rex, 1)]:
        bx0 = bx + sign * int(s * 22)
        bx1 = bx - sign * int(s * 26)
        draw.line([(bx1, brow_y + int(s * 2)), (bx, brow_y - int(s * 6)),
                   (bx0, brow_y + int(s * 2))],
                  fill=LUMA_HAIR, width=1)

    # Nose — two small nostril dots + bridge arc (detail weight=1)
    draw.ellipse([cx - int(s*8), head_cy + int(s*8), cx - int(s*2), head_cy + int(s*14)],
                 fill=LUMA_SKIN_SH)
    draw.ellipse([cx + int(s*2), head_cy + int(s*8), cx + int(s*8), head_cy + int(s*14)],
                 fill=LUMA_SKIN_SH)

    # Mouth — neutral slight-smile bezier arc
    my = head_cy + int(s * 30)
    mw = int(s * 36)
    pts = _bezier3((cx - mw, my + int(s*4)), (cx, my - int(s*8)), (cx + mw, my + int(s*4)))
    _polyline(draw, pts, LINE_COL, width=1)

    # ── BODY — hoodie trapezoid (same as v004) ─────────────────────────────────
    # Neck connects head_cy bottom to body top
    neck_top = head_cy + r + int(r * 0.25)   # chin bottom

    sw  = int(hu * 0.38)
    hw2 = int(hu * 0.70)
    bt  = neck_top + int(hu * 0.08)   # body top (small neck gap)
    bh  = int(hu * 2.0)
    bb  = bt + bh
    draw.polygon([(cx - sw, bt), (cx + sw, bt), (cx + hw2, bb), (cx - hw2, bb)],
                 fill=LUMA_HOODIE, outline=LINE_COL, width=1)

    # Pocket / sleeve detail
    mid_frac = 0.55
    hem_mid  = cx + int(sw + (hw2 - sw) * mid_frac)
    py2 = bt + int(bh * 0.50)
    draw.rectangle([hem_mid, py2, hem_mid + int(hu*0.30), py2 + int(hu*0.42)],
                   fill=LUMA_HOODIE, outline=LINE_COL, width=1)

    # Pixel accent on hoodie chest
    pix_y = bt + int(bh * 0.20)
    draw.rectangle([cx - int(hu*0.14), pix_y, cx - int(hu*0.06), pix_y + int(hu*0.06)],
                   fill=PX_CYAN)
    draw.rectangle([cx - int(hu*0.04), pix_y, cx + int(hu*0.04), pix_y + int(hu*0.06)],
                   fill=PX_MAG)
    draw.rectangle([cx + int(hu*0.06), pix_y, cx + int(hu*0.14), pix_y + int(hu*0.06)],
                   fill=PX_CYAN)

    # ── LEGS ──────────────────────────────────────────────────────────────────
    lw = int(hu * 0.20)
    leg_h = int(hu * 0.55)
    draw.rectangle([cx - lw*2, bb, cx - 4, bb + leg_h],
                   fill=LUMA_PANTS, outline=LINE_COL, width=1)
    draw.rectangle([cx + 4, bb, cx + lw*2, bb + leg_h],
                   fill=LUMA_PANTS, outline=LINE_COL, width=1)

    # ── SHOES ─────────────────────────────────────────────────────────────────
    fw = int(hu * 0.52)
    fh = int(hu * 0.28)
    sole_h = int(fh * 0.35)
    draw.ellipse([cx - lw*2 - fw + int(fw*0.3), base_y - fh,
                  cx - lw*2 + int(fw*0.5), base_y],
                 fill=LUMA_SHOE_UP, outline=LINE_COL, width=1)
    draw.ellipse([cx + lw*2 - int(fw*0.5), base_y - fh,
                  cx + lw*2 + fw - int(fw*0.3), base_y],
                 fill=LUMA_SHOE_UP, outline=LINE_COL, width=1)
    draw.rectangle([cx - lw*2 - fw + int(fw*0.3), base_y - sole_h,
                    cx - lw*2 + int(fw*0.5), base_y], fill=LUMA_SHOE_SOLE)
    draw.rectangle([cx + lw*2 - int(fw*0.5), base_y - sole_h,
                    cx + lw*2 + fw - int(fw*0.3), base_y], fill=LUMA_SHOE_SOLE)


# ══════════════════════════════════════════════════════════════════════════════
# BYTE
# ══════════════════════════════════════════════════════════════════════════════

def draw_byte_lineup(draw, cx, base_y, h):
    s         = h
    float_gap = int(s * 0.18)
    body_rx   = s // 2
    body_ry   = int(s * 0.55)
    bcy       = base_y - float_gap - body_ry

    draw.ellipse([cx - body_rx, bcy - body_ry, cx + body_rx, bcy + body_ry],
                 fill=BYTE_TEAL, outline=LINE_COL, width=3)
    shadow_pts = [
        (cx,               bcy - body_ry),
        (cx + body_rx,     bcy - body_ry + 4),
        (cx + body_rx,     bcy + body_ry - 4),
        (cx,               bcy + body_ry),
        (cx + body_rx//2,  bcy + body_ry),
        (cx + body_rx,     bcy + body_ry//2),
        (cx + body_rx,     bcy),
    ]
    draw.polygon(shadow_pts, fill=BYTE_SH)
    draw.arc([cx - body_rx, bcy - body_ry, cx + body_rx, bcy + body_ry],
             start=200, end=310, fill=BYTE_HL, width=3)

    crack_x = cx - s//4
    draw.line([(crack_x, bcy - body_ry//2), (crack_x + s//8, bcy - body_ry//6)],
              fill=SCAR_MAG, width=2)
    draw.line([(crack_x + s//8, bcy - body_ry//6), (crack_x - s//10, bcy + body_ry//6)],
              fill=SCAR_MAG, width=2)

    eye_y  = bcy - body_ry // 5
    eye_sz = s // 4
    lx     = cx - s//5
    cell   = eye_sz // 5
    if cell < 1:
        cell = 1
    ox = lx - (5*cell)//2
    oy = eye_y - (5*cell)//2
    draw.rectangle([ox-2, oy-2, ox+5*cell+2, oy+5*cell+2],
                   fill=(255,255,255), outline=LINE_COL, width=1)
    for row in range(2):
        for col in range(2):
            px = lx + col * (cell*2 + 2) - cell*2
            py = eye_y + row * (cell*2 + 2)
            draw.rectangle([px, py, px + cell*2, py + cell*2], fill=(0, 240, 255))
    rx = cx + s//5
    er = s // 10
    draw.ellipse([rx - er, eye_y - er, rx + er, eye_y + er],
                 fill=BYTE_EYE_W, outline=LINE_COL, width=1)
    draw.ellipse([rx - er//2, eye_y - er//2, rx + er//2, eye_y + er//2],
                 fill=(60, 38, 20))

    lw = s // 6
    lh = s // 5
    arm_y = bcy - body_ry // 5
    draw.rectangle([cx - body_rx - lw, arm_y, cx - body_rx, arm_y + lh],
                   fill=BYTE_TEAL, outline=LINE_COL, width=2)
    draw.rectangle([cx + body_rx, arm_y, cx + body_rx + lw, arm_y + lh],
                   fill=BYTE_TEAL, outline=LINE_COL, width=2)

    leg_offset = s // 4
    leg_h = lh
    leg_w = int(lw * 0.9)
    draw.rectangle([cx - leg_offset - leg_w//2, bcy + body_ry,
                    cx - leg_offset + leg_w//2, bcy + body_ry + leg_h],
                   fill=BYTE_TEAL, outline=LINE_COL, width=2)
    draw.rectangle([cx + leg_offset - leg_w//2, bcy + body_ry,
                    cx + leg_offset + leg_w//2, bcy + body_ry + leg_h],
                   fill=BYTE_TEAL, outline=LINE_COL, width=2)

    particle_y = bcy + body_ry + leg_h + 4
    for (px, pc) in [(cx - int(s*0.28), BYTE_HL), (cx - int(s*0.08), SCAR_MAG),
                     (cx + int(s*0.08), BYTE_HL), (cx + int(s*0.24), (0, 200, 180))]:
        py = particle_y + (abs(px - cx) % 8)
        draw.rectangle([px, py, px + 10, py + 10], fill=pc)


# ══════════════════════════════════════════════════════════════════════════════
# COSMO
# ══════════════════════════════════════════════════════════════════════════════

def draw_cosmo_lineup(draw, cx, base_y, h):
    hu = h / 4.0
    hy = base_y - h

    hw = int(hu * 0.40)
    hh = int(hu * 0.95)
    draw.ellipse([cx - hw - 4, hy - int(hu*0.08), cx + hw + 4, hy + int(hu*0.12)],
                 fill=COSMO_HAIR)
    draw.ellipse([cx - hw - 2, hy - int(hu*0.22), cx - int(hw*0.2), hy + int(hu*0.05)],
                 fill=COSMO_HAIR)
    draw.rounded_rectangle([cx - hw, hy, cx + hw, hy + hh],
                            radius=6, fill=COSMO_SKIN, outline=LINE_COL, width=2)
    ey = hy + int(hh * 0.50)
    ew = int(hu * 0.12)
    draw.ellipse([cx - int(hu*0.30) - ew, ey - ew, cx - int(hu*0.30) + ew, ey + ew],
                 fill=COSMO_LENS_BG)
    draw.ellipse([cx + int(hu*0.30) - ew, ey - ew, cx + int(hu*0.30) + ew, ey + ew],
                 fill=COSMO_LENS_BG)
    ep = int(ew * 0.5)
    draw.ellipse([cx - int(hu*0.30) - ep, ey - ep, cx - int(hu*0.30) + ep, ey + ep],
                 fill=(61, 107, 69))
    draw.ellipse([cx + int(hu*0.30) - ep, ey - ep, cx + int(hu*0.30) + ep, ey + ep],
                 fill=(61, 107, 69))

    gr  = int(hu * 0.18)
    gy  = hy + int(hh * 0.48)
    rim = 3
    lcx = cx - int(hu * 0.30)
    rcx = cx + int(hu * 0.30)
    draw.ellipse([lcx - gr - rim, gy - gr - rim, lcx + gr + rim, gy + gr + rim],
                 fill=COSMO_FRAMES, outline=LINE_COL, width=1)
    draw.ellipse([rcx - gr - rim, gy - gr - rim, rcx + gr + rim, gy + gr + rim],
                 fill=COSMO_FRAMES, outline=LINE_COL, width=1)
    draw.ellipse([lcx - gr, gy - gr, lcx + gr, gy + gr], fill=COSMO_LENS_BG)
    draw.ellipse([rcx - gr, gy - gr, rcx + gr, gy + gr], fill=COSMO_LENS_BG)
    draw.rectangle([lcx + gr, gy - 2, rcx - gr, gy + 2], fill=COSMO_FRAMES)
    draw.arc([lcx - gr + 2, gy - gr + 2, lcx + gr - 2, gy - 2],
             start=200, end=340, fill=(240,240,240), width=2)
    draw.arc([rcx - gr + 2, gy - gr + 2, rcx + gr - 2, gy - 2],
             start=200, end=340, fill=(240,240,240), width=2)

    bw     = int(hu * 0.38)
    body_h = int(hu * 2.4)
    bt     = hy + hh
    bb     = bt + body_h
    draw.rectangle([cx - bw, bt, cx + bw, bb], fill=COSMO_SHIRT_B, outline=LINE_COL, width=2)
    stripe_h = int(hu * 0.15)
    sy = bt + int(body_h * 0.25)
    while sy + stripe_h < bb - int(body_h * 0.15):
        draw.rectangle([cx - bw + 2, sy, cx + bw - 2, sy + stripe_h], fill=COSMO_SHIRT_G)
        sy += stripe_h * 2
    jw = int(hu * 0.14)
    draw.rectangle([cx - bw, bt, cx - bw + jw, bb], fill=COSMO_JACKET, outline=LINE_COL, width=1)
    draw.rectangle([cx + bw - jw, bt, cx + bw, bb], fill=COSMO_JACKET, outline=LINE_COL, width=1)

    nw   = int(hu * 0.48)
    nh   = int(hu * 0.58)
    nb_y = bt + int(body_h * 0.28)
    draw.rectangle([cx - bw - nw + 10, nb_y, cx - bw + 10, nb_y + nh],
                   fill=COSMO_NB, outline=LINE_COL, width=1)

    lw    = int(hu * 0.18)
    leg_h = int(hu * 0.60)
    draw.rectangle([cx - bw + 4, bb, cx - lw, bb + leg_h],
                   fill=COSMO_PANTS, outline=LINE_COL, width=1)
    draw.rectangle([cx + lw, bb, cx + bw - 4, bb + leg_h],
                   fill=COSMO_PANTS, outline=LINE_COL, width=1)
    draw.line([(cx, bb + int(leg_h*0.3)), (cx, bb + leg_h)], fill=LINE_COL, width=1)

    fw = int(hu * 0.28)
    fh = int(hu * 0.18)
    draw.ellipse([cx - bw + 4 - int(fw*0.4), base_y - fh, cx - lw + int(fw*0.6), base_y],
                 fill=COSMO_SHOE, outline=LINE_COL, width=1)
    draw.ellipse([cx + lw - int(fw*0.3), base_y - fh, cx + bw - 4 + int(fw*0.4), base_y],
                 fill=COSMO_SHOE, outline=LINE_COL, width=1)
    draw.ellipse([cx - bw + 4 - int(fw*0.4), base_y - int(fh*0.35),
                  cx - lw + int(fw*0.6), base_y], fill=(184, 154, 120))
    draw.ellipse([cx + lw - int(fw*0.3), base_y - int(fh*0.35),
                  cx + bw - 4 + int(fw*0.4), base_y], fill=(184, 154, 120))


# ══════════════════════════════════════════════════════════════════════════════
# MIRI
# ══════════════════════════════════════════════════════════════════════════════

def draw_miri_lineup(draw, cx, base_y, h):
    hu = h / 3.2
    hy = base_y - h
    r  = int(hu * 0.46)

    bun_cx = cx + int(hu * 0.05)
    bun_cy = hy - int(hu * 0.32)
    bun_rx = int(hu * 0.38)
    bun_ry = int(hu * 0.46)
    draw.ellipse([bun_cx - bun_rx, bun_cy - bun_ry,
                  bun_cx + bun_rx, bun_cy + bun_ry],
                 fill=MIRI_HAIR, outline=LINE_COL, width=2)
    draw.arc([bun_cx - bun_rx + 4, bun_cy, bun_cx + bun_rx - 4, bun_cy + bun_ry],
             start=0, end=180, fill=(168, 152, 140), width=2)

    # WOODEN HAIRPINS — pair of dark-stained wooden hairpins piercing the bun (C44 rename from chopstick)
    hairpin_col = (92, 58, 32)  # wooden hairpins — dark warm wood brown
    draw.polygon([(bun_cx - int(hu*0.22), bun_cy - bun_ry - int(hu*0.55)),
                  (bun_cx - int(hu*0.14), bun_cy - bun_ry - int(hu*0.55)),
                  (bun_cx - int(hu*0.06), bun_cy + bun_ry - int(hu*0.12)),
                  (bun_cx - int(hu*0.13), bun_cy + bun_ry - int(hu*0.12))],
                 fill=hairpin_col, outline=LINE_COL, width=1)
    draw.polygon([(bun_cx + int(hu*0.14), bun_cy - bun_ry - int(hu*0.50)),
                  (bun_cx + int(hu*0.22), bun_cy - bun_ry - int(hu*0.50)),
                  (bun_cx + int(hu*0.13), bun_cy + bun_ry - int(hu*0.12)),
                  (bun_cx + int(hu*0.06), bun_cy + bun_ry - int(hu*0.12))],
                 fill=hairpin_col, outline=LINE_COL, width=1)

    draw.ellipse([cx - r, hy, cx + r, hy + int(hu)],
                 fill=MIRI_SKIN, outline=LINE_COL, width=2)
    ey = hy + int(hu * 0.44)
    ew = int(hu * 0.12)
    draw.ellipse([cx - int(hu*0.22) - ew, ey - ew, cx - int(hu*0.22) + ew, ey + ew],
                 fill=(250,240,220), outline=LINE_COL, width=1)
    draw.ellipse([cx + int(hu*0.10) - ew, ey - ew, cx + int(hu*0.10) + ew, ey + ew],
                 fill=(250,240,220), outline=LINE_COL, width=1)
    ep = int(ew * 0.55)
    draw.ellipse([cx - int(hu*0.22) - ep, ey - ep, cx - int(hu*0.22) + ep, ey + ep],
                 fill=(139, 94, 60))
    draw.ellipse([cx + int(hu*0.10) - ep, ey - ep, cx + int(hu*0.10) + ep, ey + ep],
                 fill=(139, 94, 60))
    draw.arc([cx - int(hu*0.22), ey + int(hu*0.20), cx + int(hu*0.22), ey + int(hu*0.44)],
             start=20, end=160, fill=LINE_COL, width=2)
    blush_r = int(hu * 0.14)
    draw.ellipse([cx - int(hu*0.40) - blush_r, ey + int(hu*0.08),
                  cx - int(hu*0.40) + blush_r, ey + int(hu*0.08) + blush_r*2],
                 fill=(212, 149, 107))
    draw.ellipse([cx + int(hu*0.28) - blush_r, ey + int(hu*0.08),
                  cx + int(hu*0.28) + blush_r, ey + int(hu*0.08) + blush_r*2],
                 fill=(212, 149, 107))
    draw.line([(cx - int(hu*0.36), ey - int(hu*0.26)), (cx - int(hu*0.10), ey - int(hu*0.22))],
              fill=(138, 122, 112), width=2)
    draw.line([(cx + int(hu*0.00), ey - int(hu*0.22)), (cx + int(hu*0.26), ey - int(hu*0.26))],
              fill=(138, 122, 112), width=2)

    shoulder_w = int(hu * 0.78)
    hip_w      = int(hu * 0.62)
    body_top_y = hy + int(hu * 0.88)
    body_h     = int(hu * 1.82)
    body_bot_y = body_top_y + body_h
    draw.polygon([(cx - shoulder_w, body_top_y), (cx + shoulder_w, body_top_y),
                  (cx + hip_w, body_bot_y), (cx - hip_w, body_bot_y)],
                 fill=MIRI_CARDIGAN, outline=LINE_COL, width=2)
    for i in range(3):
        ridge_y = body_top_y + int(body_h * (0.22 + i * 0.22))
        draw.line([(cx - int(shoulder_w * 0.6), ridge_y), (cx + int(shoulder_w * 0.6), ridge_y)],
                  fill=(212, 130, 90), width=2)
    btn_col = (232, 216, 184)
    bx = cx - int(hu*0.08)
    for i in range(4):
        by = body_top_y + int(body_h * (0.12 + i * 0.22))
        draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=btn_col, outline=LINE_COL, width=1)

    bag_x = cx + hip_w
    bag_y = body_top_y + int(body_h * 0.52)
    bag_w = int(hu * 0.32)
    bag_h = int(hu * 0.46)
    draw.rectangle([bag_x, bag_y, bag_x + bag_w, bag_y + bag_h],
                   fill=(140, 100, 60), outline=LINE_COL, width=1)

    iron_x   = bag_x + bag_w
    iron_y   = bag_y + bag_h - int(hu * 0.04)
    iron_len = int(hu * 0.50)
    iron_w   = int(hu * 0.07)
    draw.rectangle([iron_x, iron_y, iron_x + iron_len - int(iron_len*0.22), iron_y + iron_w + 2],
                   fill=(184, 92, 56), outline=LINE_COL, width=1)
    draw.polygon([(iron_x + iron_len - int(iron_len*0.22), iron_y),
                  (iron_x + iron_len - int(iron_len*0.22), iron_y + iron_w + 2),
                  (iron_x + iron_len, iron_y + (iron_w + 2)//2)],
                 fill=(200, 200, 200), outline=LINE_COL, width=1)

    lw    = int(hu * 0.22)
    leg_h = int(hu * 0.45)
    draw.rectangle([cx - hip_w + 6, body_bot_y, cx - lw, body_bot_y + leg_h],
                   fill=MIRI_PANTS, outline=LINE_COL, width=1)
    draw.rectangle([cx + lw, body_bot_y, cx + hip_w - 6, body_bot_y + leg_h],
                   fill=MIRI_PANTS, outline=LINE_COL, width=1)

    fw = int(hu * 0.30)
    fh = int(hu * 0.18)
    draw.rectangle([cx - hip_w + 4, base_y - fh, cx - lw + int(fw*0.4), base_y],
                   fill=MIRI_SLIPPER, outline=LINE_COL, width=1)
    draw.rectangle([cx + lw - int(fw*0.4), base_y - fh, cx + hip_w - 4, base_y],
                   fill=MIRI_SLIPPER, outline=LINE_COL, width=1)
    draw.rectangle([cx - hip_w + 4, base_y - fh,
                    cx - lw + int(fw*0.4), base_y - fh + int(fh*0.30)],
                   fill=(250, 240, 220))
    draw.rectangle([cx + lw - int(fw*0.4), base_y - fh,
                    cx + hip_w - 4, base_y - fh + int(fh*0.30)],
                   fill=(250, 240, 220))


# ══════════════════════════════════════════════════════════════════════════════
# GLITCH — floating antagonist Glitchkin (unchanged from v004)
# ══════════════════════════════════════════════════════════════════════════════

def draw_glitch_lineup(draw, cx, base_y, h):
    """Glitch at lineup height h, in canonical Corrupt Amber palette."""
    import math as _math

    float_gap = int(h * 0.18)
    rx = int(h * 0.38)
    ry = int(h * 0.44)
    bcy = base_y - float_gap - ry

    # Diamond / rhombus body (filled polygon)
    body_pts = [
        (cx,      bcy - ry),   # top spike
        (cx + rx, bcy),        # right
        (cx,      bcy + ry),   # bottom spike
        (cx - rx, bcy),        # left
    ]
    draw.polygon(body_pts, fill=GLITCH_AMB)

    # Shadow side (UV Purple — corrupted)
    shadow_pts = [
        (cx,      bcy),
        (cx + rx, bcy),
        (cx,      bcy + ry),
    ]
    draw.polygon(shadow_pts, fill=GLITCH_UV)

    # Outline
    draw.polygon(body_pts, outline=GLITCH_VB, width=3)

    # Crack / scar (Hot Magenta)
    crack_s = (cx - rx // 3, bcy - ry // 3)
    crack_m = (cx + rx // 6, bcy)
    crack_e = (cx - rx // 5, bcy + ry // 3)
    draw.line([crack_s, crack_m], fill=GLITCH_HOT, width=2)
    draw.line([crack_m, crack_e], fill=GLITCH_HOT, width=2)
    mid_c = ((crack_s[0] + crack_m[0])//2, (crack_s[1] + crack_m[1])//2)
    draw.line([mid_c, (cx + rx // 2, bcy - ry // 4)], fill=GLITCH_HOT, width=1)

    # Top spike
    tsp_h = int(h * 0.16)
    spike_pts = [
        (cx,                bcy - ry - tsp_h),
        (cx + int(rx*0.15), bcy - ry + int(tsp_h*0.3)),
        (cx - int(rx*0.15), bcy - ry + int(tsp_h*0.3)),
    ]
    draw.polygon(spike_pts, fill=GLITCH_AMB)
    draw.polygon(spike_pts, outline=GLITCH_VB, width=2)
    draw.arc([cx - int(rx*0.10), bcy - ry - tsp_h + 4,
              cx + int(rx*0.10), bcy - ry + int(tsp_h*0.2)],
             start=200, end=340, fill=GLITCH_AMB_HL, width=2)

    # Bottom spike
    bsp_h = int(h * 0.14)
    bsp_pts = [
        (cx - int(rx*0.12), bcy + ry - int(bsp_h*0.3)),
        (cx + int(rx*0.12), bcy + ry - int(bsp_h*0.3)),
        (cx,                bcy + ry + bsp_h),
    ]
    draw.polygon(bsp_pts, fill=GLITCH_AMB)
    draw.polygon(bsp_pts, outline=GLITCH_VB, width=2)

    # Pixel eyes (dual — one stable, one glitching)
    cell = max(3, int(h * 0.05))
    face_cy = bcy - int(ry * 0.15)

    PIXEL_COLS = {0: GLITCH_AMB_SH, 1: GLITCH_GOLD, 2: (0, 0, 0)}
    NEUTRAL_L = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    NEUTRAL_R = [[2, 1, 2], [1, 2, 1], [2, 1, 2]]

    leye_x = cx - rx // 2 - cell * 3 // 2
    leye_y = face_cy - cell * 3 // 2
    reye_x = cx + rx // 2 - cell * 3 // 2
    reye_y = face_cy - cell * 3 // 2

    for row in range(3):
        for col in range(3):
            state = NEUTRAL_L[row][col]
            px = leye_x + col * cell
            py = leye_y + row * cell
            draw.rectangle([px, py, px + cell - 1, py + cell - 1],
                            fill=PIXEL_COLS[state])
            state = NEUTRAL_R[row][col]
            px = reye_x + col * cell
            py = reye_y + row * cell
            draw.rectangle([px, py, px + cell - 1, py + cell - 1],
                            fill=PIXEL_COLS[state])

    # Flat neutral mouth
    mouth_cx = cx - 5
    mouth_cy = face_cy + cell * 3 // 2 + 3
    for i in range(3):
        draw.rectangle([mouth_cx + i * 4, mouth_cy,
                        mouth_cx + i * 4 + 2, mouth_cy + 2],
                       fill=GLITCH_AMB_SH)

    # Flat brow bars
    draw.line([(leye_x, leye_y - 3), (leye_x + cell * 3, leye_y - 3)],
              fill=GLITCH_AMB_SH, width=1)
    draw.line([(reye_x, reye_y - 3), (reye_x + cell * 3, reye_y - 3)],
              fill=GLITCH_AMB_SH, width=1)

    # Hover confetti
    import random as _random
    rng = _random.Random(42)
    confetti_y = bcy + ry + bsp_h + 5
    for _ in range(8):
        px  = rng.randint(cx - 20, cx + 20)
        py  = rng.randint(confetti_y, confetti_y + 14)
        col = rng.choice([GLITCH_HOT, GLITCH_UV, GLITCH_VB])
        draw.rectangle([px, py, px + 3, py + 3], fill=col)


# ══════════════════════════════════════════════════════════════════════════════
# HEIGHT COMPARISON MARKERS
# ══════════════════════════════════════════════════════════════════════════════

def draw_height_markers(draw, font_small):
    # Heights measured from each character's own ground tier
    luma_top   = FG_GROUND_Y - CHAR_HEIGHTS["luma"]
    cosmo_top  = BG_GROUND_Y - CHAR_HEIGHTS["cosmo"]
    luma_chest = FG_GROUND_Y - int(CHAR_HEIGHTS["luma"] * 0.62)
    miri_top   = BG_GROUND_Y - CHAR_HEIGHTS["miri"]

    lines = [
        (cosmo_top,  TICK_COL,           "Cosmo top [BG]"),
        (luma_top,   (180, 140, 80),      "Luma top [FG]"),
        (miri_top,   (140, 160, 120),     "Miri top [BG]"),
        (luma_chest, (80, 160, 200),      "Byte / Glitch height ref"),
    ]

    x_start = 30
    x_end   = IMG_W - 100

    for y, col, label in lines:
        x = x_start
        while x < x_end:
            draw.line([(x, y), (min(x + 8, x_end), y)], fill=col, width=1)
            x += 13
        draw.text((x_end + 4, y - 7), label, fill=col, font=font_small)


# ══════════════════════════════════════════════════════════════════════════════
# BYTE FLOAT-GAP DIMENSION ARROW (retained from v003/v004)
# ══════════════════════════════════════════════════════════════════════════════

def draw_byte_float_dimension(draw, font_small):
    GROUNDFLOOR_COL = (100, 168, 200)

    byte_cx   = CHAR_X["byte"]
    # Use unscaled BYTE_H for the float-gap engineering annotation
    # (the gap proportions are a characteristic of Byte's design, not the FG scale)
    s         = BYTE_H
    float_gap = int(s * 0.18)
    body_rx   = s // 2

    arrow_x = byte_cx + body_rx + 14
    top_y   = FG_GROUND_Y - float_gap
    bot_y   = FG_GROUND_Y

    if bot_y - top_y < 6:
        return

    draw.line([(arrow_x, top_y), (arrow_x, bot_y)], fill=GROUNDFLOOR_COL, width=2)

    tip_size = 5
    draw.polygon([(arrow_x, top_y),
                  (arrow_x - tip_size, top_y + tip_size * 2),
                  (arrow_x + tip_size, top_y + tip_size * 2)],
                 fill=GROUNDFLOOR_COL)
    draw.polygon([(arrow_x, bot_y),
                  (arrow_x - tip_size, bot_y - tip_size * 2),
                  (arrow_x + tip_size, bot_y - tip_size * 2)],
                 fill=GROUNDFLOOR_COL)

    serif_w = 7
    draw.line([(arrow_x - serif_w, top_y), (arrow_x + serif_w, top_y)],
              fill=GROUNDFLOOR_COL, width=2)
    draw.line([(arrow_x - serif_w, bot_y), (arrow_x + serif_w, bot_y)],
              fill=GROUNDFLOOR_COL, width=2)

    label   = "0.25 HU"
    label_x = arrow_x + serif_w + 4
    label_y = (top_y + bot_y) // 2 - 5
    draw.text((label_x, label_y), label, fill=GROUNDFLOOR_COL, font=font_small)

    gf_x0 = byte_cx - 70
    gf_x1 = byte_cx + 70
    gf_y  = FG_GROUND_Y
    x = gf_x0
    while x < gf_x1:
        draw.line([(x, gf_y), (min(x + 10, gf_x1), gf_y)],
                  fill=GROUNDFLOOR_COL, width=1)
        x += 14


# ══════════════════════════════════════════════════════════════════════════════
# MAIN GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

def generate_lineup(output_path):
    img  = Image.new('RGB', (IMG_W, IMG_H), BG)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
        font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except Exception:
        font_title = font_label = font_small = ImageFont.load_default()

    draw.rectangle([0, 0, IMG_W, IMG_H], fill=BG)

    title = ("LUMA & THE GLITCHKIN — Full Cast Lineup — C42 v008"
             " (two-tier staging: Luma+Byte FG / Cosmo+Miri+Glitch BG)")
    draw.text((20, 14), title, fill=LABEL_COL, font=font_title)
    draw.line([(0, TITLE_H - 4), (IMG_W, TITLE_H - 4)], fill=TICK_COL, width=1)

    # ── Two-tier shadow lines ──────────────────────────────────────────────────
    # BG tier shadow (cool gray) — drawn first so FG line sits on top
    FG_SHADOW_COL = (165, 148, 128)   # warm gray shadow for FG
    BG_SHADOW_COL = (148, 158, 170)   # cool gray shadow for BG
    draw.line([(40, BG_GROUND_Y), (IMG_W - 20, BG_GROUND_Y)],
              fill=BG_SHADOW_COL, width=2)
    # FG tier shadow (warm gray)
    draw.line([(40, FG_GROUND_Y), (IMG_W - 20, FG_GROUND_Y)],
              fill=FG_SHADOW_COL, width=2)

    # Tier labels
    draw.text((IMG_W - 95, BG_GROUND_Y + 5), "BG tier",
              fill=BG_SHADOW_COL, font=font_small)
    draw.text((IMG_W - 95, FG_GROUND_Y + 5), "FG tier",
              fill=FG_SHADOW_COL, font=font_small)

    draw_byte_float_dimension(draw, font_small)
    draw = ImageDraw.Draw(img)  # refresh after annotations

    draw_height_markers(draw, font_small)
    draw = ImageDraw.Draw(img)

    char_drawers = {
        "luma":   draw_luma_lineup,
        "byte":   draw_byte_lineup,
        "cosmo":  draw_cosmo_lineup,
        "miri":   draw_miri_lineup,
        "glitch": draw_glitch_lineup,
    }

    for char in CHAR_ORDER:
        cx       = CHAR_X[char]
        h        = CHAR_HEIGHTS[char]
        ground_y = CHAR_GROUND_Y[char]
        char_drawers[char](draw, cx, ground_y, h)
        draw = ImageDraw.Draw(img)  # refresh after each character

    # Character name labels below their respective ground lines
    for char in CHAR_ORDER:
        cx      = CHAR_X[char]
        ground_y = CHAR_GROUND_Y[char]
        lines   = CHAR_LABELS[char].split("\n")
        label_y = ground_y + 8
        for line in lines:
            lw = len(line) * 6
            draw.text((cx - lw // 2, label_y), line, fill=LABEL_COL, font=font_small)
            label_y += 13

    # Vertical height brackets — measured from each char's own ground tier
    for char in CHAR_ORDER:
        cx       = CHAR_X[char] - 44
        h        = CHAR_HEIGHTS[char]
        ground_y = CHAR_GROUND_Y[char]
        top_y    = ground_y - h
        if char in ("byte", "glitch"):
            s         = h
            float_gap = int(s * 0.18)
            body_ry   = int(s * 0.55)
            top_y     = ground_y - float_gap - body_ry * 2
        draw.line([(cx, top_y), (cx, ground_y)], fill=TICK_COL, width=1)
        draw.line([(cx - 4, top_y), (cx + 4, top_y)], fill=TICK_COL, width=1)
        draw.line([(cx - 4, ground_y), (cx + 4, ground_y)], fill=TICK_COL, width=1)
        draw.text((cx - 20, (top_y + ground_y)//2 - 5),
                  f"{h}px", fill=TICK_COL, font=font_small)

    # Staging annotation bar
    annotation = (
        f"Staging: FG tier (y={FG_GROUND_Y}) = Luma+Byte @+3% scale.  "
        f"BG tier (y={BG_GROUND_Y}) = Cosmo+Miri+Glitch @baseline scale.  "
        "Proportion constants unchanged — uniform post-scale only.  "
        "Closes Daisuke C16 P3 (inventory→cast) + C15 Luma power balance."
    )
    draw.text((20, IMG_H - 34), annotation, fill=(140, 120, 100), font=font_small)

    footer = (
        f"Full cast: Cosmo | Miri | LUMA | Byte | Glitch.  "
        f"Reference: 1 head unit = {HEAD_UNIT:.0f}px.  "
        "Colors per master_palette.md (canonical).  C42 v008."
    )
    draw.text((20, IMG_H - 18), footer, fill=TICK_COL, font=font_small)

    # IMAGE SIZE RULE: ≤ 1280px in both dimensions
    if img.size[0] > 1280 or img.size[1] > 1280:
        img.thumbnail((1280, 1280), Image.LANCZOS)

    img.save(output_path)
    print(f"Saved: {output_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}px")


def main():
    import os
    out_dir = "/home/wipkat/team/output/characters/main"
    os.makedirs(out_dir, exist_ok=True)
    generate_lineup(os.path.join(out_dir, "LTG_CHAR_character_lineup.png"))
    print("Character lineup v008 generation complete.")
    print("  C42 changes: two-tier ground plane (FG=Luma+Byte, BG=Cosmo+Miri+Glitch)")
    print(f"  FG_GROUND_Y={FG_GROUND_Y}, BG_GROUND_Y={BG_GROUND_Y}, FG_SCALE={FG_SCALE}")
    print(f"  Character order (L→R): cosmo | miri | luma | byte | glitch")
    print(f"  Luma: {LUMA_RENDER_H_FG}px drawn ({LUMA_RENDER_H}px base ×{FG_SCALE}), "
          f"{LUMA_HEADS} heads, head unit = {HEAD_UNIT:.1f}px")
    print(f"  Byte: {BYTE_H_FG}px drawn ({BYTE_H}px base ×{FG_SCALE})")


if __name__ == '__main__':
    main()
