#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_miri_turnaround.py
Grandma Miri — 4-View Character Turnaround
"Luma & the Glitchkin" — Cycle 20

4 views (FRONT, 3/4, SIDE, BACK) on a single 1600×800 canvas.
Full color rendering with 3-tier line weight:
  Silhouette: 3-4px output (drawn at 2x, scaled down)
  Interior structure: 2px output
  Detail (crow's feet, smile lines, knit): 1px output

Character: MIRI-A canonical — bun + crossed wooden hairpins + A-line cardigan + round glasses
Height: 3.2 heads (compact, rooted). Reference: ~1.25× Luma's perceived height at same scale.

Output: output/characters/main/turnarounds/LTG_CHAR_miri_turnaround.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Palette (from grandma_miri_color_model.md, canonical Cycle 17) ─────────────
SKIN_BASE   = (140, 84,  48)   # #8C5430 Deep Warm Brown
SKIN_SH     = (106, 58,  30)   # #6A3A1E Dark Sienna
SKIN_HL     = (168,106,  64)   # #A86A40 Warm Chestnut
BLUSH_PERM  = (212,149, 107)   # #D4956B permanent cheek blush (always present)
HAIR_BASE   = (216,208, 200)   # #D8D0C8 Silver White
HAIR_SH     = (168,152, 140)   # #A8988C Warm Gray
HAIR_HL     = (240,236, 232)   # #F0ECE8 Bright Near-White
EYE_IRIS    = (139, 94,  60)   # #8B5E3C Deep Warm Amber
EYE_PUP     = ( 26, 15,  10)   # #1A0F0A Near-Black Espresso
EYE_W       = (250,240, 220)   # #FAF0DC Warm Cream
EYE_HL      = (240,240, 240)   # #F0F0F0 Static White
BROW_COL    = (138,122, 112)   # #8A7A70 Warm Gray
GLASSES_COL = (138,122, 112)   # #8A7A70 Warm Gray (wire-frame, same as brows to recede)
CARDIGAN    = (184, 92,  56)   # #B85C38 Warm Terracotta Rust
CARDIGAN_SH = (138, 60,  28)   # #8A3C1C Deep Rust
CARDIGAN_HL = (212,130,  90)   # #D4825A Dusty Apricot
CARDIGAN_BTN= (232,216, 184)   # #E8D8B8 Aged Bone (buttons)
UNDERSHIRT  = (250,240, 220)   # #FAF0DC Warm Cream
PANTS       = (200,174, 138)   # #C8AE8A Warm Linen Tan
PANTS_SH    = (160,138, 106)   # #A08A6A Warm Medium Tan
PANTS_HL    = (222,201, 168)   # #DEC9A8 Light Linen
SLIPPER     = (196, 144, 122)  # C38 FIX: #C4907A Dusty Warm Apricot (was #5A7A5A Deep Sage — G>R violated Miri warm-palette guarantee; per master_palette.md CHAR-M-11 C32)
SLIPPER_LN  = (250,240, 220)   # #FAF0DC Warm Cream lining
SLIPPER_SOL = ( 90, 56,  32)   # #5A3820 Warm Dark Brown sole
HAIRPIN     = (180,120,  60)   # wooden hairpin — warm wood tone (C44: renamed from CHOPSTICK)
HAIRPIN_SH  = (120, 80,  30)   # wooden hairpin shadow side (C44: renamed from CHOPSTICK_SH)
LINE        = ( 59, 40,  32)   # #3B2820 Deep Cocoa — canonical silhouette line
CANVAS_BG   = (252,248, 242)   # warm off-white background
PANEL_BG    = (244,238, 228)   # very slightly tinted panel
LABEL_COL   = ( 59, 40,  32)   # Deep Cocoa for labels
HU_LINE_COL = (160,140, 120)   # muted tan for HU reference lines
SHADOW_COL  = (200,180, 155)   # cast ground shadow

# ── Layout ─────────────────────────────────────────────────────────────────────
CANVAS_W  = 1600
CANVAS_H  = 800
VIEWS     = ["FRONT", "3/4", "SIDE", "BACK"]
N_VIEWS   = 4
VIEW_W    = CANVAS_W // N_VIEWS   # 400 per view panel
VIEW_H    = CANVAS_H

# Within each panel:
PANEL_PAD = 30      # horizontal padding inside panel
HEADER_H  = 60      # top area for HU ruler / title
LABEL_H   = 48      # bottom area for view label
BODY_H    = VIEW_H - HEADER_H - LABEL_H  # 692 — character drawing area

# Render at 2× then scale down for sub-pixel AA quality
SCALE = 2

# Character height: Miri is 3.2 heads tall.
# We want her to comfortably fill BODY_H with some breathing room.
# Actual draw height ≈ BODY_H * 0.88 leaves ~12% margins.
CHAR_DRAW_H = int(BODY_H * 0.88)  # ≈ 609 at 1x (scaled up to 2x for render)
CHAR_TOP_MARGIN = int(BODY_H * 0.04)  # 4% top breathing room

def hu():
    """Head unit in 1x canvas pixels."""
    return CHAR_DRAW_H / 3.2

def hu_r():
    """Head unit in render-scale pixels (2x)."""
    return (CHAR_DRAW_H * SCALE) / 3.2

# ── Helper: draw rounded-corner rectangle ──────────────────────────────────────
def draw_rounded_rect(draw, x0, y0, x1, y1, radius, fill=None, outline=None, width=1):
    r = min(radius, (x1-x0)//2, (y1-y0)//2)
    if fill:
        draw.rectangle([x0+r, y0, x1-r, y1], fill=fill)
        draw.rectangle([x0, y0+r, x1, y1-r], fill=fill)
        draw.pieslice([x0, y0, x0+2*r, y0+2*r], 180, 270, fill=fill)
        draw.pieslice([x1-2*r, y0, x1, y0+2*r], 270, 360, fill=fill)
        draw.pieslice([x0, y1-2*r, x0+2*r, y1], 90, 180, fill=fill)
        draw.pieslice([x1-2*r, y1-2*r, x1, y1], 0, 90, fill=fill)
    if outline:
        draw.arc([x0, y0, x0+2*r, y0+2*r], 180, 270, fill=outline, width=width)
        draw.arc([x1-2*r, y0, x1, y0+2*r], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1-2*r, x0+2*r, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1-2*r, y1-2*r, x1, y1], 0, 90, fill=outline, width=width)
        draw.line([x0+r, y0, x1-r, y0], fill=outline, width=width)
        draw.line([x0+r, y1, x1-r, y1], fill=outline, width=width)
        draw.line([x0, y0+r, x0, y1-r], fill=outline, width=width)
        draw.line([x1, y0+r, x1, y1-r], fill=outline, width=width)


# ══════════════════════════════════════════════════════════════════════════════
# MIRI DRAWING FUNCTIONS — all coordinates in RENDER space (1x * SCALE)
# cx = horizontal center, base_y = ground line (feet bottom)
# ══════════════════════════════════════════════════════════════════════════════

def SL():
    """Silhouette line weight at render scale."""
    return max(3, int(3.5 * SCALE))

def IL():
    """Interior structure line weight at render scale."""
    return max(2, int(2 * SCALE))

def DL():
    """Detail line weight at render scale."""
    return max(1, int(1 * SCALE))


def draw_miri_front(draw, cx, base_y):
    """
    FRONT VIEW — full body, WARM/WELCOMING expression.
    Arms slightly open/extended in A-frame gesture.
    Bun visible over head silhouette.
    """
    H = int(hu() * SCALE)
    hr = int(H * 0.88 / 2 * 0.5)   # head radius (88% circular — slightly wider than tall)
    hw = int(hr * 1.05)              # head width radius (slightly wider)

    # --- Ground shadow (oval)
    sx, sy = cx, base_y + int(4*SCALE)
    draw.ellipse([sx - int(hw*1.8), sy - int(3*SCALE),
                  sx + int(hw*1.8), sy + int(8*SCALE)], fill=SHADOW_COL)

    # --- SLIPPERS (draw first — behind legs)
    slipper_w = int(hr * 1.3)
    slipper_h = int(hr * 0.55)
    sl_y = base_y - slipper_h
    sl_lx = cx - int(hr * 0.95)
    sl_rx = cx + int(hr * 0.22)

    # Left slipper
    draw.ellipse([sl_lx - slipper_w//2, sl_y,
                  sl_lx + slipper_w//2, base_y], fill=SLIPPER_SOL)
    draw.ellipse([sl_lx - slipper_w//2, sl_y,
                  sl_lx + slipper_w//2, base_y - slipper_h//4], fill=SLIPPER)
    # Right slipper
    draw.ellipse([sl_rx - slipper_w//2, sl_y,
                  sl_rx + slipper_w//2, base_y], fill=SLIPPER_SOL)
    draw.ellipse([sl_rx - slipper_w//2, sl_y,
                  sl_rx + slipper_w//2, base_y - slipper_h//4], fill=SLIPPER)
    # Slipper lining hint
    draw.arc([sl_lx - slipper_w//4, sl_y,
              sl_lx + slipper_w//4, sl_y + slipper_h//2], 200, 340, fill=SLIPPER_LN, width=DL())
    draw.arc([sl_rx - slipper_w//4, sl_y,
              sl_rx + slipper_w//4, sl_y + slipper_h//2], 200, 340, fill=SLIPPER_LN, width=DL())

    # --- LEGS
    leg_w   = int(hr * 0.55)
    leg_h   = int(H * 0.33)
    body_bot_y = base_y - slipper_h - leg_h + int(4*SCALE)

    # Left leg
    draw.rectangle([cx - int(hr*0.85), body_bot_y,
                    cx - int(hr*0.15), body_bot_y + leg_h], fill=PANTS)
    # Right leg
    draw.rectangle([cx + int(hr*0.10), body_bot_y,
                    cx + int(hr*0.82), body_bot_y + leg_h], fill=PANTS)
    # Pants shadow (inner)
    draw.line([cx - int(hr*0.16), body_bot_y, cx - int(hr*0.16), body_bot_y + leg_h],
              fill=PANTS_SH, width=DL())
    draw.line([cx + int(hr*0.11), body_bot_y, cx + int(hr*0.11), body_bot_y + leg_h],
              fill=PANTS_SH, width=DL())

    # --- CARDIGAN / TORSO
    torso_top_y = body_bot_y - int(H * 0.38)
    torso_w_top = int(hr * 1.45)    # shoulder width (1.1× head width per spec)
    torso_w_bot = int(hr * 1.55)    # cardigan slightly flares at hem (A-line)

    # Cardigan body fill (A-line silhouette)
    cardigan_pts = [
        (cx - torso_w_top, torso_top_y),
        (cx + torso_w_top, torso_top_y),
        (cx + torso_w_bot, body_bot_y),
        (cx - torso_w_bot, body_bot_y),
    ]
    draw.polygon(cardigan_pts, fill=CARDIGAN)

    # Cardigan highlight (left shoulder area)
    draw.polygon([
        (cx - torso_w_top, torso_top_y),
        (cx - torso_w_top + int(hr*0.5), torso_top_y),
        (cx - torso_w_top + int(hr*0.3), torso_top_y + int(H*0.06)),
        (cx - torso_w_top, torso_top_y + int(H*0.06)),
    ], fill=CARDIGAN_HL)

    # V-neck opening (undershirt visible)
    vneck_depth = int(H * 0.12)
    vneck_w     = int(hr * 0.55)
    neck_y      = torso_top_y + int(H * 0.04)
    draw.polygon([
        (cx, neck_y + vneck_depth),
        (cx - vneck_w//2, neck_y),
        (cx + vneck_w//2, neck_y),
    ], fill=UNDERSHIRT)

    # Cardigan pocket edges (two front pockets, lower half)
    pocket_top = torso_top_y + int(H * 0.22)
    pocket_bot = body_bot_y - int(H * 0.04)
    pocket_w   = int(hr * 0.60)
    # Left pocket
    draw_rounded_rect(draw,
        cx - int(hr*1.10), pocket_top,
        cx - int(hr*1.10) + pocket_w, pocket_bot,
        radius=int(4*SCALE), outline=CARDIGAN_SH, width=IL())
    # Right pocket
    draw_rounded_rect(draw,
        cx + int(hr*0.50), pocket_top,
        cx + int(hr*0.50) + pocket_w, pocket_bot,
        radius=int(4*SCALE), outline=CARDIGAN_SH, width=IL())

    # Cable-knit texture lines (3 vertical pairs per front panel, per spec)
    knit_y0 = torso_top_y + int(H * 0.08)
    knit_y1 = body_bot_y  - int(H * 0.03)
    for kx_off in [-int(hr*0.55), 0, int(hr*0.55)]:
        for dkx in [-int(2*SCALE), int(2*SCALE)]:
            draw.line([cx + kx_off + dkx, knit_y0,
                       cx + kx_off + dkx, knit_y1], fill=CARDIGAN_SH, width=DL())

    # Buttons (4 down center front)
    btn_r = int(4 * SCALE)
    for i in range(4):
        by = int(torso_top_y + vneck_depth + int(H * 0.04)
                 + i * (body_bot_y - torso_top_y - vneck_depth - int(H*0.08)) / 3.5)
        draw.ellipse([cx - btn_r, by - btn_r, cx + btn_r, by + btn_r],
                     fill=CARDIGAN_BTN, outline=CARDIGAN_SH, width=DL())

    # Cardigan silhouette outline
    draw.polygon(cardigan_pts, outline=LINE, width=SL())

    # --- ARMS (open/extended — WARM welcoming gesture)
    arm_len  = int(H * 0.30)
    arm_w    = int(hr * 0.42)
    # Upper arm top at shoulder; arms swing outward and slightly down
    arm_top_y = torso_top_y + int(H * 0.04)

    # Left arm
    al_x0 = cx - torso_w_top - int(arm_w * 0.3)
    al_y0 = arm_top_y
    al_x1 = cx - torso_w_top - int(hr * 0.85)
    al_y1 = arm_top_y + int(arm_len * 0.85)
    # Upper arm
    draw.polygon([
        (al_x0,             al_y0),
        (al_x0 + arm_w,     al_y0),
        (al_x1 + arm_w,     al_y1),
        (al_x1,             al_y1),
    ], fill=CARDIGAN)
    draw.polygon([
        (al_x0,             al_y0),
        (al_x0 + arm_w,     al_y0),
        (al_x1 + arm_w,     al_y1),
        (al_x1,             al_y1),
    ], outline=LINE, width=SL())

    # Left hand (mitten oval, skin)
    lh_cx = al_x1 + arm_w//2 - int(2*SCALE)
    lh_cy = al_y1 + int(hr * 0.30)
    lh_rw = int(hr * 0.38)
    lh_rh = int(hr * 0.45)
    draw.ellipse([lh_cx - lh_rw, lh_cy - lh_rh,
                  lh_cx + lh_rw, lh_cy + lh_rh], fill=SKIN_BASE, outline=LINE, width=IL())
    # Knuckle line
    draw.arc([lh_cx - lh_rw + int(2*SCALE), lh_cy - int(4*SCALE),
              lh_cx + lh_rw - int(2*SCALE), lh_cy + int(4*SCALE)],
             200, 340, fill=SKIN_SH, width=DL())

    # Right arm
    ar_x0 = cx + torso_w_top - arm_w + int(arm_w * 0.3)
    ar_y0 = arm_top_y
    ar_x1 = cx + torso_w_top + int(hr * 0.45)
    ar_y1 = arm_top_y + int(arm_len * 0.85)
    draw.polygon([
        (ar_x0,             ar_y0),
        (ar_x0 + arm_w,     ar_y0),
        (ar_x1 + arm_w,     ar_y1),
        (ar_x1,             ar_y1),
    ], fill=CARDIGAN)
    draw.polygon([
        (ar_x0,             ar_y0),
        (ar_x0 + arm_w,     ar_y0),
        (ar_x1 + arm_w,     ar_y1),
        (ar_x1,             ar_y1),
    ], outline=LINE, width=SL())

    # Right hand
    rh_cx = ar_x1 + arm_w//2
    rh_cy = ar_y1 + int(hr * 0.30)
    draw.ellipse([rh_cx - lh_rw, rh_cy - lh_rh,
                  rh_cx + lh_rw, rh_cy + lh_rh], fill=SKIN_BASE, outline=LINE, width=IL())
    draw.arc([rh_cx - lh_rw + int(2*SCALE), rh_cy - int(4*SCALE),
              rh_cx + lh_rw - int(2*SCALE), rh_cy + int(4*SCALE)],
             200, 340, fill=SKIN_SH, width=DL())

    # --- NECK
    neck_w  = int(hr * 0.45)
    neck_h  = int(H * 0.06)
    neck_top_y = torso_top_y - neck_h
    draw.rectangle([cx - neck_w, neck_top_y, cx + neck_w, torso_top_y + int(2*SCALE)],
                   fill=SKIN_BASE)

    # --- HEAD (88% circular — slightly wider than tall)
    head_top_y  = neck_top_y - int(hr * 1.95)
    head_cy     = neck_top_y - int(hr * 1.0)
    draw.ellipse([cx - hw, head_top_y, cx + hw, neck_top_y + int(4*SCALE)],
                 fill=SKIN_BASE, outline=LINE, width=SL())

    # Skin shadow (right side of face)
    draw.arc([cx, head_top_y + int(hr*0.3), cx + hw, neck_top_y],
             330, 90, fill=SKIN_SH, width=IL())

    # Highlight (forehead)
    hl_y = head_top_y + int(hr * 0.35)
    draw.ellipse([cx - int(hr*0.40), hl_y, cx + int(hr*0.10), hl_y + int(hr*0.45)],
                 fill=SKIN_HL)

    # --- EYES (front view — both eyes visible)
    eye_y   = head_cy - int(hr * 0.05)
    eye_rx  = int(hr * 0.30)
    eye_ry  = int(hr * 0.22)
    eye_l_cx = cx - int(hr * 0.52)
    eye_r_cx = cx + int(hr * 0.52)

    for ex in [eye_l_cx, eye_r_cx]:
        # Eye white
        draw.ellipse([ex - eye_rx, eye_y - eye_ry,
                      ex + eye_rx, eye_y + eye_ry], fill=EYE_W)
        # Iris
        iris_r = int(eye_ry * 0.78)
        draw.ellipse([ex - iris_r, eye_y - iris_r,
                      ex + iris_r, eye_y + iris_r], fill=EYE_IRIS)
        # Pupil
        pup_r = int(iris_r * 0.48)
        draw.ellipse([ex - pup_r, eye_y - pup_r,
                      ex + pup_r, eye_y + pup_r], fill=EYE_PUP)
        # Highlight (upper-left per spec)
        hl_r = int(iris_r * 0.30)
        draw.ellipse([ex - hl_r - int(2*SCALE), eye_y - hl_r - int(2*SCALE),
                      ex + int(1*SCALE),         eye_y + int(1*SCALE)], fill=EYE_HL)
        # Upper eyelid (slightly heavy arc)
        draw.arc([ex - eye_rx, eye_y - eye_ry,
                  ex + eye_rx, eye_y + eye_ry], 200, 340, fill=LINE, width=IL())

    # --- EYEBROWS (gentle arch, softer than Luma's)
    brow_y = eye_y - eye_ry - int(hr * 0.22)
    brow_w = int(hr * 0.40)
    brow_h = int(hr * 0.12)
    for bx in [eye_l_cx, eye_r_cx]:
        # Slight outward upward arch
        sign = 1 if bx == eye_r_cx else -1
        draw.arc([bx - brow_w//2, brow_y,
                  bx + brow_w//2, brow_y + brow_h*3],
                 210, 330, fill=BROW_COL, width=IL())

    # --- NOSE (soft button, most detailed in cast)
    nose_x = cx
    nose_y = head_cy + int(hr * 0.28)
    nose_r = int(hr * 0.16)
    draw.arc([nose_x - nose_r, nose_y - nose_r,
              nose_x + nose_r, nose_y + nose_r], 30, 150, fill=LINE, width=DL())
    # Nostril hints
    draw.arc([nose_x - nose_r - int(3*SCALE), nose_y,
              nose_x - int(2*SCALE), nose_y + int(5*SCALE)], 180, 360, fill=LINE, width=DL())
    draw.arc([nose_x + int(2*SCALE), nose_y,
              nose_x + nose_r + int(3*SCALE), nose_y + int(5*SCALE)], 180, 360, fill=LINE, width=DL())

    # --- MOUTH (WARM: gentle upward closed smile)
    mouth_y = head_cy + int(hr * 0.62)
    mouth_w = int(hr * 0.65)
    draw.arc([cx - mouth_w, mouth_y - int(hr * 0.20),
              cx + mouth_w, mouth_y + int(hr * 0.20)],
             10, 170, fill=LINE, width=IL())
    # Cheek press dimples
    draw.arc([cx - mouth_w - int(3*SCALE), mouth_y - int(4*SCALE),
              cx - mouth_w + int(6*SCALE), mouth_y + int(6*SCALE)], 260, 360, fill=LINE, width=DL())
    draw.arc([cx + mouth_w - int(6*SCALE), mouth_y - int(4*SCALE),
              cx + mouth_w + int(3*SCALE), mouth_y + int(6*SCALE)], 180, 280, fill=LINE, width=DL())

    # --- SMILE LINES (from nose to mouth corner — always present per spec, 40% weight)
    draw.arc([cx - int(hr*0.60), nose_y + int(hr*0.05),
              cx - int(hr*0.18), mouth_y], 120, 200, fill=SKIN_SH, width=DL())
    draw.arc([cx + int(hr*0.18), nose_y + int(hr*0.05),
              cx + int(hr*0.60), mouth_y], 340, 60, fill=SKIN_SH, width=DL())

    # --- CROW'S FEET (always present, DL weight)
    cft_y = eye_y
    # Left eye outer corner crow's feet
    cfw_l = eye_l_cx - eye_rx
    draw.arc([cfw_l - int(12*SCALE), cft_y - int(4*SCALE),
              cfw_l + int(2*SCALE),  cft_y + int(12*SCALE)], 300, 60, fill=SKIN_SH, width=DL())
    # Right eye outer corner crow's feet
    cfw_r = eye_r_cx + eye_rx
    draw.arc([cfw_r - int(2*SCALE),  cft_y - int(4*SCALE),
              cfw_r + int(12*SCALE), cft_y + int(12*SCALE)], 300, 60, fill=SKIN_SH, width=DL())

    # --- PERMANENT BLUSH (25% opacity overlay)
    blush_img = Image.new('RGBA', (int(hr * 1.2), int(hr * 0.7)), (0,0,0,0))
    blush_d   = ImageDraw.Draw(blush_img)
    blush_d.ellipse([0, 0, int(hr*1.2)-1, int(hr*0.7)-1], fill=(*BLUSH_PERM, 64))  # ~25%
    for bx_off in [-int(hr*0.70), int(hr*0.05)]:
        blush_paste_x = cx + bx_off - int(hr*0.60)
        blush_paste_y = eye_y + eye_ry - int(hr*0.10)
        # We'll draw directly — approximate with a low-alpha ellipse
    draw.ellipse([eye_l_cx - int(hr*0.55), eye_y + int(hr*0.05),
                  eye_l_cx + int(hr*0.55), eye_y + int(hr*0.55)], fill=(*BLUSH_PERM, 64))
    draw.ellipse([eye_r_cx - int(hr*0.55), eye_y + int(hr*0.05),
                  eye_r_cx + int(hr*0.55), eye_y + int(hr*0.55)], fill=(*BLUSH_PERM, 64))

    # --- GLASSES (round wire-frame, two round lenses + bridge + temples)
    gl_r    = int(eye_ry * 1.30)
    gl_col  = GLASSES_COL
    gl_w    = IL()
    # Left lens
    draw.ellipse([eye_l_cx - gl_r, eye_y - gl_r,
                  eye_l_cx + gl_r, eye_y + gl_r], outline=gl_col, width=gl_w)
    # Right lens
    draw.ellipse([eye_r_cx - gl_r, eye_y - gl_r,
                  eye_r_cx + gl_r, eye_y + gl_r], outline=gl_col, width=gl_w)
    # Bridge
    draw.line([eye_l_cx + gl_r, eye_y, eye_r_cx - gl_r, eye_y], fill=gl_col, width=gl_w)
    # Left temple (to ear/head edge)
    draw.line([eye_l_cx - gl_r, eye_y - gl_r//2,
               eye_l_cx - gl_r - int(hr*0.40), eye_y], fill=gl_col, width=gl_w)
    # Right temple
    draw.line([eye_r_cx + gl_r, eye_y - gl_r//2,
               eye_r_cx + gl_r + int(hr*0.40), eye_y], fill=gl_col, width=gl_w)

    # --- BUN (silver, sits on upper-back of head — visible over head in front view)
    bun_cx = cx + int(hr * 0.15)   # slightly right of center, rear placement
    bun_cy = head_top_y - int(hr * 0.45)
    bun_rx = int(hr * 0.70)
    bun_ry = int(hr * 0.55)
    draw.ellipse([bun_cx - bun_rx, bun_cy - bun_ry,
                  bun_cx + bun_rx, bun_cy + bun_ry], fill=HAIR_BASE, outline=LINE, width=IL())
    # Bun shadow (inner volume)
    draw.arc([bun_cx - int(bun_rx*0.60), bun_cy - int(bun_ry*0.50),
              bun_cx + int(bun_rx*0.60), bun_cy + int(bun_ry*0.60)],
             10, 180, fill=HAIR_SH, width=IL())
    # Bun highlight (crown)
    draw.arc([bun_cx - int(bun_rx*0.50), bun_cy - int(bun_ry*0.60),
              bun_cx + int(bun_rx*0.50), bun_cy - int(bun_ry*0.10)],
             200, 340, fill=HAIR_HL, width=DL())

    # Chopsticks (2 crossed sticks protruding from bun — front view shows as X)
    cs_cx = bun_cx
    cs_cy = bun_cy
    cs_len = int(hr * 1.10)
    cs_w   = int(3 * SCALE)
    # Chopstick 1 (top-left to bottom-right)
    draw.line([cs_cx - int(cs_len*0.45), cs_cy - int(cs_len*0.55),
               cs_cx + int(cs_len*0.45), cs_cy + int(cs_len*0.45)],
              fill=HAIRPIN, width=cs_w)
    # Chopstick 2 (top-right to bottom-left)
    draw.line([cs_cx + int(cs_len*0.45), cs_cy - int(cs_len*0.55),
               cs_cx - int(cs_len*0.45), cs_cy + int(cs_len*0.45)],
              fill=HAIRPIN, width=cs_w)
    # Chopstick shadow lines
    draw.line([cs_cx - int(cs_len*0.45) + int(SCALE), cs_cy - int(cs_len*0.55) + int(SCALE),
               cs_cx + int(cs_len*0.45) + int(SCALE), cs_cy + int(cs_len*0.45) + int(SCALE)],
              fill=HAIRPIN_SH, width=DL())

    # Front hair wisps (2-3 escaping strands at temples)
    wisp_y = head_top_y + int(hr * 0.60)
    for wx_off, wdx, wdy in [(-hw + int(hr*0.20), -int(hr*0.35), int(hr*0.40)),
                              ( hw - int(hr*0.25),  int(hr*0.35), int(hr*0.40))]:
        draw.line([cx + wx_off, wisp_y,
                   cx + wx_off + wdx, wisp_y + wdy],
                  fill=HAIR_BASE, width=IL())

    # --- SLIPPER outlines (draw on top)
    draw.ellipse([sl_lx - slipper_w//2, sl_y,
                  sl_lx + slipper_w//2, base_y], outline=LINE, width=SL())
    draw.ellipse([sl_rx - slipper_w//2, sl_y,
                  sl_rx + slipper_w//2, base_y], outline=LINE, width=SL())

    # Leg outlines
    draw.rectangle([cx - int(hr*0.85), body_bot_y,
                    cx - int(hr*0.15), body_bot_y + leg_h], outline=LINE, width=SL())
    draw.rectangle([cx + int(hr*0.10), body_bot_y,
                    cx + int(hr*0.82), body_bot_y + leg_h], outline=LINE, width=SL())

    # Neck outline
    draw.rectangle([cx - neck_w, neck_top_y, cx + neck_w, torso_top_y + int(2*SCALE)],
                   outline=LINE, width=SL())


def draw_miri_three_quarter(draw, cx, base_y):
    """
    3/4 VIEW — slight right rotation (character turns left, showing right cheek to viewer).
    Bun + wooden hairpin stack clearly visible from this angle.
    Glasses bridge visible.
    A-line cardigan silhouette reads.
    Near side (right of frame) is wider; far side compressed.
    """
    H   = int(hu() * SCALE)
    hr  = int(H * 0.88 / 2 * 0.5)
    hw  = int(hr * 1.05)

    # In 3/4 view the head appears slightly elliptical — near side wider
    head_w_near = int(hw * 1.05)
    head_w_far  = int(hw * 0.60)

    # --- Ground shadow
    draw.ellipse([cx - int(hw*1.7), base_y,
                  cx + int(hw*1.7), base_y + int(9*SCALE)], fill=SHADOW_COL)

    # --- SLIPPERS
    slipper_w = int(hr * 1.25)
    slipper_h = int(hr * 0.52)
    sl_y = base_y - slipper_h
    # Near (left) slipper: points slightly forward/left
    sl_lx = cx - int(hr * 0.50)
    sl_rx = cx + int(hr * 0.65)
    draw.ellipse([sl_lx - slipper_w//2, sl_y, sl_lx + slipper_w//2, base_y], fill=SLIPPER_SOL)
    draw.ellipse([sl_lx - slipper_w//2, sl_y, sl_lx + slipper_w//2, sl_y + slipper_h//2], fill=SLIPPER)
    draw.ellipse([sl_rx - int(slipper_w*0.42), sl_y+int(2*SCALE),
                  sl_rx + int(slipper_w*0.42), base_y], fill=SLIPPER_SOL)
    draw.ellipse([sl_rx - int(slipper_w*0.42), sl_y+int(2*SCALE),
                  sl_rx + int(slipper_w*0.42), sl_y + slipper_h//2 + int(2*SCALE)], fill=SLIPPER)

    # --- LEGS
    leg_h = int(H * 0.33)
    body_bot_y = base_y - slipper_h - leg_h + int(4*SCALE)
    # Near leg: wider
    draw.rectangle([cx - int(hr*0.65), body_bot_y, cx - int(hr*0.02), body_bot_y + leg_h], fill=PANTS)
    # Far leg: narrower, shifted right
    draw.rectangle([cx + int(hr*0.18), body_bot_y, cx + int(hr*0.72), body_bot_y + leg_h], fill=PANTS)
    draw.line([cx - int(hr*0.03), body_bot_y, cx - int(hr*0.03), body_bot_y + leg_h], fill=PANTS_SH, width=DL())

    # --- CARDIGAN (3/4: near side wider, far side compressed)
    torso_top_y  = body_bot_y - int(H * 0.38)
    tw_near      = int(hr * 1.40)
    tw_far       = int(hr * 0.90)
    cardigan_pts = [
        (cx - tw_near, torso_top_y),
        (cx + tw_far,  torso_top_y),
        (cx + int(tw_far * 1.10), body_bot_y),
        (cx - int(tw_near * 1.10), body_bot_y),
    ]
    draw.polygon(cardigan_pts, fill=CARDIGAN)
    # V-neck
    vneck_depth = int(H * 0.12)
    vneck_w     = int(hr * 0.50)
    neck_y = torso_top_y + int(H * 0.04)
    # Shift center of V-neck slightly toward near side
    vx = cx - int(hr * 0.15)
    draw.polygon([
        (vx, neck_y + vneck_depth),
        (vx - vneck_w//2, neck_y),
        (vx + int(vneck_w * 0.60), neck_y),
    ], fill=UNDERSHIRT)
    # Cable knit (fewer lines on far side, more prominent on near)
    knit_y0 = torso_top_y + int(H * 0.08)
    knit_y1 = body_bot_y  - int(H * 0.03)
    for kx_off in [-int(hr*0.55), int(hr*0.15)]:
        for dkx in [-int(2*SCALE), int(2*SCALE)]:
            draw.line([cx + kx_off + dkx, knit_y0,
                       cx + kx_off + dkx, knit_y1], fill=CARDIGAN_SH, width=DL())
    # Near pocket (only near side visible)
    pocket_top = torso_top_y + int(H * 0.22)
    pocket_bot = body_bot_y  - int(H * 0.04)
    pocket_w   = int(hr * 0.55)
    draw_rounded_rect(draw,
        cx - int(hr*1.05), pocket_top,
        cx - int(hr*1.05) + pocket_w, pocket_bot,
        radius=int(4*SCALE), outline=CARDIGAN_SH, width=IL())
    # Buttons (center-near)
    btn_r = int(4 * SCALE)
    for i in range(4):
        bby = int(torso_top_y + vneck_depth + int(H * 0.04)
                  + i * (body_bot_y - torso_top_y - vneck_depth - int(H*0.08)) / 3.5)
        draw.ellipse([vx - btn_r, bby - btn_r, vx + btn_r, bby + btn_r],
                     fill=CARDIGAN_BTN, outline=CARDIGAN_SH, width=DL())
    # Outline
    draw.polygon(cardigan_pts, outline=LINE, width=SL())

    # --- ARMS (3/4 view, near arm more visible)
    arm_len = int(H * 0.30)
    arm_w   = int(hr * 0.42)
    arm_top_y = torso_top_y + int(H * 0.04)

    # Near (left) arm — open gesture, swings out
    al_x0 = cx - tw_near - int(arm_w*0.2)
    al_y0 = arm_top_y
    al_x1 = cx - tw_near - int(hr * 0.80)
    al_y1 = arm_top_y + int(arm_len * 0.82)
    draw.polygon([(al_x0, al_y0), (al_x0 + arm_w, al_y0),
                  (al_x1 + arm_w, al_y1), (al_x1, al_y1)],
                 fill=CARDIGAN, outline=LINE, width=SL())
    lh_cx = al_x1 + arm_w//2
    lh_cy = al_y1 + int(hr * 0.28)
    lh_r  = int(hr * 0.38)
    draw.ellipse([lh_cx - lh_r, lh_cy - int(lh_r*1.15),
                  lh_cx + lh_r, lh_cy + int(lh_r*1.15)], fill=SKIN_BASE, outline=LINE, width=IL())

    # Far (right) arm — partially visible, foreshortened
    ar_x0 = cx + tw_far
    ar_y0 = arm_top_y
    ar_x1 = cx + tw_far + int(hr * 0.50)
    ar_y1 = arm_top_y + int(arm_len * 0.60)
    draw.polygon([(ar_x0, ar_y0), (ar_x0 + int(arm_w*0.60), ar_y0),
                  (ar_x1 + int(arm_w*0.60), ar_y1), (ar_x1, ar_y1)],
                 fill=CARDIGAN, outline=LINE, width=IL())

    # --- NECK
    neck_w   = int(hr * 0.42)
    neck_h   = int(H * 0.06)
    neck_top_y = torso_top_y - neck_h
    neck_cx = cx - int(hr * 0.18)  # slightly toward near side
    draw.rectangle([neck_cx - neck_w, neck_top_y, neck_cx + neck_w, torso_top_y + int(2*SCALE)],
                   fill=SKIN_BASE, outline=LINE, width=SL())

    # --- HEAD (3/4 — ellipse, near side wider)
    head_top_y = neck_top_y - int(hr * 1.95)
    head_cy    = neck_top_y - int(hr * 1.0)
    hcx = cx - int(hr * 0.18)
    draw.ellipse([hcx - head_w_near, head_top_y,
                  hcx + head_w_far,  neck_top_y + int(4*SCALE)],
                 fill=SKIN_BASE, outline=LINE, width=SL())
    # Side shadow (far cheek)
    draw.arc([hcx + int(head_w_far*0.40), head_top_y + int(hr*0.3),
              hcx + head_w_far, neck_top_y], 330, 100, fill=SKIN_SH, width=IL())

    # --- EYES (3/4: near eye fully visible, far eye partially visible / foreshortened)
    eye_y    = head_cy - int(hr * 0.05)
    eye_rx   = int(hr * 0.30)
    eye_ry   = int(hr * 0.22)
    eye_near = hcx - int(hr * 0.38)  # near eye, more visible
    eye_far  = hcx + int(hr * 0.22)  # far eye, smaller

    # Near eye (full)
    for ex, erx, ery in [(eye_near, eye_rx, eye_ry),
                          (eye_far,  int(eye_rx*0.65), eye_ry)]:
        draw.ellipse([ex - erx, eye_y - ery, ex + erx, eye_y + ery], fill=EYE_W)
        iris_r = int(ery * 0.78)
        draw.ellipse([ex - iris_r, eye_y - iris_r, ex + iris_r, eye_y + iris_r], fill=EYE_IRIS)
        pup_r = int(iris_r * 0.48)
        draw.ellipse([ex - pup_r, eye_y - pup_r, ex + pup_r, eye_y + pup_r], fill=EYE_PUP)
        hl_r = int(iris_r * 0.30)
        draw.ellipse([ex - hl_r - int(2*SCALE), eye_y - hl_r - int(2*SCALE),
                      ex + int(1*SCALE), eye_y + int(1*SCALE)], fill=EYE_HL)
        draw.arc([ex - erx, eye_y - ery, ex + erx, eye_y + ery], 200, 340, fill=LINE, width=IL())

    # EYEBROWS
    brow_y = eye_y - eye_ry - int(hr * 0.22)
    brow_w = int(hr * 0.38)
    for bx in [eye_near, eye_far]:
        draw.arc([bx - brow_w//2, brow_y, bx + brow_w//2, brow_y + int(hr*0.35)],
                 210, 330, fill=BROW_COL, width=IL())

    # NOSE (3/4 — bridge visible, soft button)
    nose_x = hcx - int(hr * 0.08)
    nose_y = head_cy + int(hr * 0.28)
    nose_r = int(hr * 0.16)
    draw.line([nose_x, head_cy, nose_x, nose_y + nose_r], fill=SKIN_SH, width=DL())
    draw.arc([nose_x - nose_r, nose_y - nose_r, nose_x + nose_r, nose_y + nose_r],
             30, 180, fill=LINE, width=DL())
    draw.arc([nose_x, nose_y, nose_x + nose_r + int(3*SCALE), nose_y + int(5*SCALE)],
             180, 360, fill=LINE, width=DL())

    # MOUTH (warm smile, 3/4)
    mouth_y = head_cy + int(hr * 0.62)
    mouth_w = int(hr * 0.60)
    draw.arc([hcx - mouth_w, mouth_y - int(hr*0.18), hcx + mouth_w, mouth_y + int(hr*0.18)],
             15, 165, fill=LINE, width=IL())

    # SMILE LINES
    draw.arc([hcx - int(hr*0.55), nose_y + int(hr*0.05), hcx - int(hr*0.18), mouth_y],
             120, 200, fill=SKIN_SH, width=DL())

    # CROW'S FEET
    draw.arc([eye_near - eye_rx - int(12*SCALE), eye_y - int(4*SCALE),
              eye_near - eye_rx + int(2*SCALE), eye_y + int(12*SCALE)], 290, 70, fill=SKIN_SH, width=DL())

    # CHEEK BLUSH
    draw.ellipse([eye_near - int(hr*0.55), eye_y + int(hr*0.05),
                  eye_near + int(hr*0.55), eye_y + int(hr*0.55)], fill=(*BLUSH_PERM, 64))
    draw.ellipse([eye_far - int(hr*0.40), eye_y + int(hr*0.05),
                  eye_far + int(hr*0.40), eye_y + int(hr*0.45)], fill=(*BLUSH_PERM, 48))

    # GLASSES (3/4: near lens full circle, far lens slightly oval, bridge visible)
    gl_r   = int(eye_ry * 1.30)
    gl_col = GLASSES_COL
    gl_w   = IL()
    draw.ellipse([eye_near - gl_r, eye_y - gl_r, eye_near + gl_r, eye_y + gl_r], outline=gl_col, width=gl_w)
    draw.ellipse([eye_far - int(gl_r*0.65), eye_y - gl_r,
                  eye_far + int(gl_r*0.65), eye_y + gl_r], outline=gl_col, width=gl_w)
    # Bridge
    draw.line([eye_near + gl_r, eye_y, eye_far - int(gl_r*0.65), eye_y], fill=gl_col, width=gl_w)
    # Near temple
    draw.line([eye_near - gl_r, eye_y - gl_r//2,
               eye_near - gl_r - int(hr*0.40), eye_y], fill=gl_col, width=gl_w)
    # Far temple (foreshortened, curves back)
    draw.line([eye_far + int(gl_r*0.65), eye_y - gl_r//2,
               eye_far + int(gl_r*0.65) + int(hr*0.28), eye_y], fill=gl_col, width=gl_w)

    # BUN (3/4 — bun+wooden hairpin stack clearly visible)
    bun_cx2 = hcx + int(hr * 0.45)   # bun further toward back from 3/4 angle
    bun_cy  = head_top_y - int(hr * 0.45)
    bun_rx  = int(hr * 0.68)
    bun_ry  = int(hr * 0.55)
    draw.ellipse([bun_cx2 - bun_rx, bun_cy - bun_ry,
                  bun_cx2 + bun_rx, bun_cy + bun_ry], fill=HAIR_BASE, outline=LINE, width=IL())
    draw.arc([bun_cx2 - int(bun_rx*0.55), bun_cy,
              bun_cx2 + int(bun_rx*0.55), bun_cy + bun_ry*2],
             10, 180, fill=HAIR_SH, width=IL())
    # Chopsticks in 3/4 — angled cross visible in profile
    cs_cx2 = bun_cx2
    cs_cy2 = bun_cy
    cs_len = int(hr * 1.05)
    draw.line([cs_cx2 - int(cs_len*0.40), cs_cy2 - int(cs_len*0.60),
               cs_cx2 + int(cs_len*0.40), cs_cy2 + int(cs_len*0.40)],
              fill=HAIRPIN, width=int(3*SCALE))
    draw.line([cs_cx2 + int(cs_len*0.40), cs_cy2 - int(cs_len*0.55),
               cs_cx2 - int(cs_len*0.35), cs_cy2 + int(cs_len*0.45)],
              fill=HAIRPIN, width=int(3*SCALE))
    # Front wisp
    wisp_y = head_top_y + int(hr * 0.65)
    draw.line([hcx - hw + int(hr*0.15), wisp_y,
               hcx - hw - int(hr*0.30), wisp_y + int(hr*0.45)], fill=HAIR_BASE, width=IL())

    # Slipper + leg outlines
    draw.ellipse([sl_lx - slipper_w//2, sl_y, sl_lx + slipper_w//2, base_y], outline=LINE, width=SL())
    draw.ellipse([sl_rx - int(slipper_w*0.42), sl_y+int(2*SCALE),
                  sl_rx + int(slipper_w*0.42), base_y], outline=LINE, width=SL())
    draw.rectangle([cx - int(hr*0.65), body_bot_y, cx - int(hr*0.02), body_bot_y + leg_h], outline=LINE, width=SL())
    draw.rectangle([cx + int(hr*0.18), body_bot_y, cx + int(hr*0.72), body_bot_y + leg_h], outline=LINE, width=SL())


def draw_miri_side(draw, cx, base_y):
    """
    SIDE VIEW — true profile (facing left).
    Bun clearly in silhouette behind head.
    Glasses as forward protrusion.
    Compact body shape.
    """
    H   = int(hu() * SCALE)
    hr  = int(H * 0.88 / 2 * 0.5)

    # In side view, head is a circle (88% — slightly oval, depth = hw, width = hr)
    head_d  = int(hr * 1.88)  # head depth (front to back, 88% of circle, ~= 2*hr)
    neck_w  = int(hr * 0.40)
    neck_h  = int(H * 0.06)

    # --- Ground shadow
    draw.ellipse([cx - int(hr*0.60), base_y,
                  cx + int(hr*0.60), base_y + int(8*SCALE)], fill=SHADOW_COL)

    # --- SLIPPER (side view — single slipper visible, pointing left/forward)
    slipper_len = int(hr * 1.55)
    slipper_h   = int(hr * 0.50)
    sl_y = base_y - slipper_h
    sl_cx = cx - int(hr * 0.08)
    draw.ellipse([sl_cx - slipper_len//2, sl_y, sl_cx + slipper_len//2, base_y], fill=SLIPPER_SOL)
    draw.ellipse([sl_cx - slipper_len//2, sl_y,
                  sl_cx + slipper_len//2, sl_y + slipper_h//2], fill=SLIPPER)
    draw.arc([sl_cx - slipper_len//4, sl_y,
              sl_cx + slipper_len//4, sl_y + slipper_h//2], 200, 340, fill=SLIPPER_LN, width=DL())

    # --- LEGS (side view — one leg in front, one slightly behind)
    leg_w   = int(hr * 0.55)
    leg_h   = int(H * 0.33)
    body_bot_y = base_y - slipper_h - leg_h + int(4*SCALE)
    # Front leg
    draw.rectangle([cx - leg_w//2 - int(4*SCALE), body_bot_y,
                    cx + leg_w//2 - int(4*SCALE), body_bot_y + leg_h], fill=PANTS)
    # Back leg (slightly offset, partially hidden)
    draw.rectangle([cx - leg_w//2 + int(6*SCALE), body_bot_y + int(8*SCALE),
                    cx + leg_w//2 + int(6*SCALE), body_bot_y + leg_h], fill=PANTS_SH)

    # --- CARDIGAN (side view — rectangle, slightly wider at hem, mid-thigh length)
    torso_top_y = body_bot_y - int(H * 0.38)
    side_torso_w = int(hr * 0.90)  # depth of torso in side view
    # Torso trapezoid (slightly wider at base for A-line hang)
    draw.polygon([
        (cx - int(side_torso_w*0.45), torso_top_y),
        (cx + int(side_torso_w*0.55), torso_top_y),
        (cx + int(side_torso_w*0.60), body_bot_y),
        (cx - int(side_torso_w*0.50), body_bot_y),
    ], fill=CARDIGAN)
    # Cable-knit hint (side view — vertical lines barely visible)
    draw.line([cx + int(side_torso_w*0.10), torso_top_y + int(H*0.10),
               cx + int(side_torso_w*0.10), body_bot_y - int(H*0.03)], fill=CARDIGAN_SH, width=DL())
    # Front edge of cardigan (visible open edge)
    draw.line([cx - int(side_torso_w*0.45), torso_top_y,
               cx - int(side_torso_w*0.50), body_bot_y], fill=CARDIGAN_SH, width=IL())
    # Cardigan outline
    draw.polygon([
        (cx - int(side_torso_w*0.45), torso_top_y),
        (cx + int(side_torso_w*0.55), torso_top_y),
        (cx + int(side_torso_w*0.60), body_bot_y),
        (cx - int(side_torso_w*0.50), body_bot_y),
    ], outline=LINE, width=SL())

    # --- ARM (side view — one arm visible, bent at side)
    arm_w   = int(hr * 0.42)
    arm_len = int(H * 0.28)
    arm_x0  = cx + int(side_torso_w * 0.50)
    arm_top_y = torso_top_y + int(H * 0.04)
    arm_x1  = arm_x0 + int(arm_w * 0.35)
    arm_y1  = arm_top_y + arm_len
    draw.polygon([
        (arm_x0, arm_top_y), (arm_x0 + arm_w, arm_top_y),
        (arm_x1 + arm_w, arm_y1), (arm_x1, arm_y1),
    ], fill=CARDIGAN, outline=LINE, width=SL())
    # Hand (side)
    hh_cx = arm_x1 + arm_w//2
    hh_cy = arm_y1 + int(hr * 0.28)
    draw.ellipse([hh_cx - int(hr*0.35), hh_cy - int(hr*0.42),
                  hh_cx + int(hr*0.35), hh_cy + int(hr*0.42)],
                 fill=SKIN_BASE, outline=LINE, width=IL())

    # --- NECK
    neck_top_y = torso_top_y - neck_h
    neck_cx    = cx + int(hr * 0.05)  # slight forward placement
    draw.rectangle([neck_cx - neck_w, neck_top_y, neck_cx + neck_w, torso_top_y + int(2*SCALE)],
                   fill=SKIN_BASE, outline=LINE, width=SL())

    # --- HEAD (side — near-circle, faces left/forward)
    head_top_y = neck_top_y - int(hr * 1.95)
    head_cy    = neck_top_y - int(hr * 1.0)
    hcx = neck_cx + int(hr * 0.05)  # head center slightly forward of neck
    # Head as slightly oval (wider than tall in silhouette) — facing left
    draw.ellipse([hcx - int(hr*0.95), head_top_y,
                  hcx + int(hr*0.95), neck_top_y + int(4*SCALE)], fill=SKIN_BASE, outline=LINE, width=SL())
    # Face shading (side plane)
    draw.arc([hcx - int(hr*0.20), head_top_y + int(hr*0.25),
              hcx + int(hr*0.95), neck_top_y], 300, 80, fill=SKIN_SH, width=IL())

    # --- EYE (side — single eye, profile, almond sliver)
    eye_x   = hcx - int(hr * 0.45)  # forward of center
    eye_y   = head_cy - int(hr * 0.05)
    ey_rw   = int(hr * 0.26)
    ey_rh   = int(hr * 0.18)
    draw.ellipse([eye_x - ey_rw, eye_y - ey_rh, eye_x + ey_rw, eye_y + ey_rh], fill=EYE_W)
    iris_r = int(ey_rh * 0.85)
    draw.ellipse([eye_x - iris_r, eye_y - iris_r, eye_x + iris_r, eye_y + iris_r], fill=EYE_IRIS)
    pup_r = int(iris_r * 0.48)
    draw.ellipse([eye_x - pup_r, eye_y - pup_r, eye_x + pup_r, eye_y + pup_r], fill=EYE_PUP)
    hl_r = int(iris_r * 0.30)
    draw.ellipse([eye_x - hl_r - int(2*SCALE), eye_y - hl_r - int(2*SCALE),
                  eye_x + int(1*SCALE), eye_y + int(1*SCALE)], fill=EYE_HL)
    draw.arc([eye_x - ey_rw, eye_y - ey_rh, eye_x + ey_rw, eye_y + ey_rh], 200, 340, fill=LINE, width=IL())

    # EYEBROW (side — single arch)
    brow_y = eye_y - ey_rh - int(hr * 0.22)
    draw.arc([eye_x - int(hr*0.25), brow_y, eye_x + int(hr*0.25), brow_y + int(hr*0.35)],
             210, 330, fill=BROW_COL, width=IL())

    # NOSE (side — profile button with bridge line)
    nose_x = hcx - int(hr * 0.80)  # protrudes forward from face
    nose_y = head_cy + int(hr * 0.28)
    nose_r = int(hr * 0.18)
    draw.line([hcx - int(hr*0.30), head_cy - int(hr*0.18), nose_x, nose_y], fill=SKIN_SH, width=DL())
    draw.arc([nose_x - nose_r, nose_y - nose_r, nose_x + nose_r, nose_y + nose_r],
             270, 90, fill=LINE, width=DL())
    # Nostril
    draw.arc([nose_x, nose_y, nose_x + nose_r + int(4*SCALE), nose_y + int(6*SCALE)],
             180, 360, fill=LINE, width=DL())

    # MOUTH (side — closed warm smile in profile)
    mouth_y = head_cy + int(hr * 0.62)
    mouth_x = hcx - int(hr * 0.62)  # forward
    draw.arc([mouth_x - int(hr*0.30), mouth_y - int(hr*0.15),
              mouth_x + int(hr*0.30), mouth_y + int(hr*0.15)],
             270, 90, fill=LINE, width=IL())

    # SMILE LINE (side view — single visible)
    draw.arc([mouth_x - int(hr*0.18), nose_y + int(hr*0.10),
              mouth_x + int(hr*0.18), mouth_y], 20, 130, fill=SKIN_SH, width=DL())

    # CROW'S FEET
    draw.arc([eye_x - ey_rw - int(12*SCALE), eye_y - int(4*SCALE),
              eye_x - ey_rw + int(2*SCALE), eye_y + int(12*SCALE)], 295, 65, fill=SKIN_SH, width=DL())

    # CHEEK BLUSH
    draw.ellipse([eye_x - int(hr*0.48), eye_y + int(hr*0.05),
                  eye_x + int(hr*0.48), eye_y + int(hr*0.52)], fill=(*BLUSH_PERM, 64))

    # GLASSES (side — forward protrusion: right lens as a circle, temple going back)
    gl_r   = int(ey_rh * 1.35)
    gl_col = GLASSES_COL
    draw.ellipse([eye_x - gl_r, eye_y - gl_r, eye_x + gl_r, eye_y + gl_r],
                 outline=gl_col, width=IL())
    # Bridge (tiny hint, going back toward face)
    draw.line([eye_x + gl_r, eye_y, eye_x + gl_r + int(hr*0.20), eye_y],
              fill=gl_col, width=IL())
    # Temple going backward
    draw.line([eye_x + gl_r + int(hr*0.20), eye_y - gl_r//2,
               eye_x + gl_r + int(hr*0.55), eye_y], fill=gl_col, width=IL())

    # BUN (side view — clearly in silhouette BEHIND head)
    bun_cx3 = hcx + int(hr * 0.68)  # bun behind/above head center
    bun_cy  = head_top_y - int(hr * 0.25)
    bun_rx  = int(hr * 0.65)
    bun_ry  = int(hr * 0.58)
    draw.ellipse([bun_cx3 - bun_rx, bun_cy - bun_ry,
                  bun_cx3 + bun_rx, bun_cy + bun_ry], fill=HAIR_BASE, outline=LINE, width=IL())
    draw.arc([bun_cx3 - int(bun_rx*0.50), bun_cy,
              bun_cx3 + int(bun_rx*0.50), bun_cy + int(bun_ry*2)],
             5, 175, fill=HAIR_SH, width=IL())
    draw.arc([bun_cx3 - int(bun_rx*0.45), bun_cy - int(bun_ry*0.60),
              bun_cx3 + int(bun_rx*0.45), bun_cy + int(bun_ry*0.05)],
             200, 340, fill=HAIR_HL, width=DL())

    # Chopstick tips visible in side profile (both sticks cross from same angle)
    cs_cxs = bun_cx3
    cs_cys = bun_cy
    # In side view: one stick appears as near-vertical, one as diagonal
    draw.line([cs_cxs - int(hr*0.20), cs_cys - int(hr*0.80),
               cs_cxs + int(hr*0.20), cs_cys + int(hr*0.50)],
              fill=HAIRPIN, width=int(3*SCALE))
    draw.line([cs_cxs - int(hr*0.55), cs_cys - int(hr*0.40),
               cs_cxs + int(hr*0.55), cs_cys + int(hr*0.20)],
              fill=HAIRPIN, width=int(3*SCALE))

    # Hair hairline at forehead (slight line)
    draw.arc([hcx - int(hr*0.90), head_top_y + int(hr*0.05),
              hcx + int(hr*0.10), head_top_y + int(hr*0.60)],
             240, 330, fill=HAIR_SH, width=DL())

    # Slipper outline + leg outlines
    draw.ellipse([sl_cx - slipper_len//2, sl_y, sl_cx + slipper_len//2, base_y],
                 outline=LINE, width=SL())
    draw.rectangle([cx - leg_w//2 - int(4*SCALE), body_bot_y,
                    cx + leg_w//2 - int(4*SCALE), body_bot_y + leg_h], outline=LINE, width=SL())


def draw_miri_back(draw, cx, base_y):
    """
    BACK VIEW — back of bun (show wooden hairpin pair crossed), cardigan back, overall silhouette.
    Face not visible.
    """
    H   = int(hu() * SCALE)
    hr  = int(H * 0.88 / 2 * 0.5)
    hw  = int(hr * 1.05)

    # --- Ground shadow
    draw.ellipse([cx - int(hw*1.8), base_y,
                  cx + int(hw*1.8), base_y + int(9*SCALE)], fill=SHADOW_COL)

    # --- SLIPPERS (back view — we see the heels)
    slipper_w = int(hr * 1.20)
    slipper_h = int(hr * 0.50)
    sl_y = base_y - slipper_h
    sl_lx = cx - int(hr * 0.88)
    sl_rx = cx + int(hr * 0.25)
    for slx in [sl_lx, sl_rx]:
        draw.ellipse([slx - slipper_w//2, sl_y + slipper_h//2,
                      slx + slipper_w//2, base_y], fill=SLIPPER_SOL)
        draw.ellipse([slx - slipper_w//2, sl_y,
                      slx + slipper_w//2, sl_y + slipper_h//2], fill=SLIPPER)
        draw.ellipse([slx - slipper_w//2, sl_y,
                      slx + slipper_w//2, base_y], outline=LINE, width=SL())

    # --- LEGS (back view)
    leg_h = int(H * 0.33)
    body_bot_y = base_y - slipper_h - leg_h + int(4*SCALE)
    draw.rectangle([cx - int(hr*0.85), body_bot_y, cx - int(hr*0.10), body_bot_y + leg_h], fill=PANTS)
    draw.rectangle([cx + int(hr*0.10), body_bot_y, cx + int(hr*0.85), body_bot_y + leg_h], fill=PANTS)
    draw.line([cx - int(hr*0.11), body_bot_y, cx - int(hr*0.11), body_bot_y + leg_h], fill=PANTS_SH, width=DL())
    draw.line([cx + int(hr*0.11), body_bot_y, cx + int(hr*0.11), body_bot_y + leg_h], fill=PANTS_SH, width=DL())

    # --- CARDIGAN BACK
    torso_top_y = body_bot_y - int(H * 0.38)
    torso_w_top = int(hr * 1.45)
    torso_w_bot = int(hr * 1.55)
    cardigan_pts = [
        (cx - torso_w_top, torso_top_y),
        (cx + torso_w_top, torso_top_y),
        (cx + torso_w_bot, body_bot_y),
        (cx - torso_w_bot, body_bot_y),
    ]
    draw.polygon(cardigan_pts, fill=CARDIGAN)
    # Highlight — left shoulder (back left = near viewer's left)
    draw.polygon([
        (cx + torso_w_top, torso_top_y),
        (cx + torso_w_top - int(hr*0.45), torso_top_y),
        (cx + torso_w_top - int(hr*0.28), torso_top_y + int(H*0.06)),
        (cx + torso_w_top, torso_top_y + int(H*0.06)),
    ], fill=CARDIGAN_HL)
    # Back cable knit
    knit_y0 = torso_top_y + int(H * 0.05)
    knit_y1 = body_bot_y  - int(H * 0.03)
    for kx_off in [-int(hr*0.50), 0, int(hr*0.50)]:
        for dkx in [-int(2*SCALE), int(2*SCALE)]:
            draw.line([cx + kx_off + dkx, knit_y0,
                       cx + kx_off + dkx, knit_y1], fill=CARDIGAN_SH, width=DL())
    # Center back seam
    draw.line([cx, torso_top_y + int(H*0.03), cx, body_bot_y], fill=CARDIGAN_SH, width=DL())
    # Outline
    draw.polygon(cardigan_pts, outline=LINE, width=SL())

    # --- ARMS (back view: both arms slightly extended as seen from behind)
    arm_len  = int(H * 0.28)
    arm_w    = int(hr * 0.42)
    arm_top_y = torso_top_y + int(H * 0.04)
    # Left arm (viewer's left = character's right)
    al_x0 = cx - torso_w_top - int(arm_w * 0.2)
    al_x1 = cx - torso_w_top - int(hr * 0.70)
    al_y1 = arm_top_y + arm_len
    draw.polygon([(al_x0, arm_top_y), (al_x0 + arm_w, arm_top_y),
                  (al_x1 + arm_w, al_y1), (al_x1, al_y1)],
                 fill=CARDIGAN, outline=LINE, width=SL())
    lh_cx = al_x1 + arm_w//2
    lh_cy = al_y1 + int(hr * 0.28)
    lh_r  = int(hr * 0.38)
    draw.ellipse([lh_cx - lh_r, lh_cy - int(lh_r*1.15),
                  lh_cx + lh_r, lh_cy + int(lh_r*1.15)], fill=SKIN_BASE, outline=LINE, width=IL())
    # Right arm
    ar_x0 = cx + torso_w_top
    ar_x1 = cx + torso_w_top + int(hr * 0.70)
    ar_y1 = arm_top_y + arm_len
    draw.polygon([(ar_x0, arm_top_y), (ar_x0 + arm_w, arm_top_y),
                  (ar_x1 + arm_w, ar_y1), (ar_x1, ar_y1)],
                 fill=CARDIGAN, outline=LINE, width=SL())
    rh_cx = ar_x1 + arm_w//2
    rh_cy = ar_y1 + int(hr * 0.28)
    draw.ellipse([rh_cx - lh_r, rh_cy - int(lh_r*1.15),
                  rh_cx + lh_r, rh_cy + int(lh_r*1.15)], fill=SKIN_BASE, outline=LINE, width=IL())

    # --- NECK (back — slight neck visible above cardigan)
    neck_w = int(hr * 0.40)
    neck_h = int(H * 0.06)
    neck_top_y = torso_top_y - neck_h
    draw.rectangle([cx - neck_w, neck_top_y, cx + neck_w, torso_top_y + int(2*SCALE)],
                   fill=SKIN_BASE, outline=LINE, width=SL())

    # --- HEAD (back view — back of head, no face features)
    head_top_y = neck_top_y - int(hr * 1.95)
    head_cy    = neck_top_y - int(hr * 1.0)
    draw.ellipse([cx - hw, head_top_y, cx + hw, neck_top_y + int(4*SCALE)],
                 fill=SKIN_BASE, outline=LINE, width=SL())
    # Back of head hair (forehead hairline starts lower back)
    draw.arc([cx - int(hw*0.85), head_top_y + int(hr*0.25),
              cx + int(hw*0.85), head_top_y + int(hr*1.10)],
             0, 180, fill=HAIR_SH, width=DL())

    # --- BUN (back view — most prominent view: full bun face + crossing wooden hairpins)
    bun_cx = cx
    bun_cy = head_top_y - int(hr * 0.30)
    bun_rx = int(hr * 0.72)
    bun_ry = int(hr * 0.58)
    draw.ellipse([bun_cx - bun_rx, bun_cy - bun_ry,
                  bun_cx + bun_rx, bun_cy + bun_ry], fill=HAIR_BASE, outline=LINE, width=SL())
    # Bun inner detail (shadow mass)
    draw.arc([bun_cx - int(bun_rx*0.55), bun_cy + int(bun_ry*0.15),
              bun_cx + int(bun_rx*0.55), bun_cy + int(bun_ry*2)],
             0, 180, fill=HAIR_SH, width=IL())
    # Swirl detail (clockwise spiral suggestion)
    draw.arc([bun_cx - int(bun_rx*0.42), bun_cy - int(bun_ry*0.42),
              bun_cx + int(bun_rx*0.42), bun_cy + int(bun_ry*0.42)],
             30, 220, fill=HAIR_SH, width=DL())
    # Highlight crown
    draw.arc([bun_cx - int(bun_rx*0.45), bun_cy - int(bun_ry*0.60),
              bun_cx + int(bun_rx*0.45), bun_cy - int(bun_ry*0.10)],
             200, 340, fill=HAIR_HL, width=DL())

    # WOODEN HAIRPINS — back view: X crossing clearly visible
    cs_cx = bun_cx
    cs_cy = bun_cy
    cs_len = int(hr * 1.15)
    # Stick 1 (\ direction)
    draw.line([cs_cx - int(cs_len*0.50), cs_cy - int(cs_len*0.60),
               cs_cx + int(cs_len*0.50), cs_cy + int(cs_len*0.50)],
              fill=HAIRPIN, width=int(3*SCALE))
    # Stick 2 (/ direction)
    draw.line([cs_cx + int(cs_len*0.50), cs_cy - int(cs_len*0.60),
               cs_cx - int(cs_len*0.50), cs_cy + int(cs_len*0.50)],
              fill=HAIRPIN, width=int(3*SCALE))
    # Stick shadows
    for sdx, sdy in [(int(SCALE), int(SCALE))]:
        draw.line([cs_cx - int(cs_len*0.50) + sdx, cs_cy - int(cs_len*0.60) + sdy,
                   cs_cx + int(cs_len*0.50) + sdx, cs_cy + int(cs_len*0.50) + sdy],
                  fill=HAIRPIN_SH, width=DL())

    # Escaping strands at neck/temples (back view)
    wisp_y = head_top_y + int(hr * 0.70)
    draw.line([cx - hw + int(hr*0.15), wisp_y,
               cx - hw - int(hr*0.30), wisp_y + int(hr*0.40)], fill=HAIR_BASE, width=IL())
    draw.line([cx + hw - int(hr*0.15), wisp_y,
               cx + hw + int(hr*0.30), wisp_y + int(hr*0.40)], fill=HAIR_BASE, width=IL())

    # Leg outlines
    draw.rectangle([cx - int(hr*0.85), body_bot_y, cx - int(hr*0.10), body_bot_y + leg_h], outline=LINE, width=SL())
    draw.rectangle([cx + int(hr*0.10), body_bot_y, cx + int(hr*0.85), body_bot_y + leg_h], outline=LINE, width=SL())


# ══════════════════════════════════════════════════════════════════════════════
# PANEL RENDERING
# ══════════════════════════════════════════════════════════════════════════════

def render_view_panel(view_index, view_name, draw_fn, canvas_img, font_label, font_small):
    """Render a single view panel into the canvas at the correct x offset."""
    panel_x = view_index * VIEW_W
    panel_y = 0

    # Panel background (draw directly on main canvas)
    draw = ImageDraw.Draw(canvas_img)
    # Panel background tint
    draw.rectangle([panel_x, panel_y, panel_x + VIEW_W - 1, VIEW_H - 1], fill=PANEL_BG)
    # Panel border (right edge separator, except last panel)
    if view_index < N_VIEWS - 1:
        draw.line([panel_x + VIEW_W - 1, HEADER_H, panel_x + VIEW_W - 1, VIEW_H - LABEL_H],
                  fill=(200, 185, 165), width=1)

    # ── Height Reference Line (HU ruler) ──────────────────────────────────────
    # Character base at 96% of BODY_H from top of body area (matches r_base_y at SCALE)
    char_base_y_1x = HEADER_H + int(BODY_H * 0.96)
    char_top_y_1x  = char_base_y_1x - CHAR_DRAW_H  # 3.2 HU body height
    # Bun extends ~0.25 HU above body top — cap ruler at bun top
    bun_top_y_1x   = char_top_y_1x - int(hu() * 0.30)

    ruler_x  = panel_x + VIEW_W - 55
    hu_px = hu()
    # Ruler spans body height (feet to top of head, not including bun)
    draw.line([ruler_x, char_top_y_1x, ruler_x, char_base_y_1x], fill=HU_LINE_COL, width=1)
    draw.line([ruler_x - 4, char_top_y_1x, ruler_x + 4, char_top_y_1x], fill=HU_LINE_COL, width=1)
    draw.line([ruler_x - 4, char_base_y_1x, ruler_x + 4, char_base_y_1x], fill=HU_LINE_COL, width=1)

    # HU tick marks (3.2 heads — mark each full HU from bottom)
    for i in range(1, 4):
        ty = int(char_base_y_1x - i * hu_px)
        draw.line([ruler_x - 3, ty, ruler_x + 3, ty], fill=HU_LINE_COL, width=1)

    # Use char_top_y_1x for vert_margin variable (kept for ruler label below)
    char_top_y = char_top_y_1x

    # Label ruler
    try:
        draw.text((ruler_x + 6, char_top_y_1x + 2), "3.2 HU", fill=HU_LINE_COL, font=font_small)
    except Exception:
        draw.text((ruler_x + 6, char_top_y_1x + 2), "3.2 HU", fill=HU_LINE_COL)

    # ── Render character at 2× scale then paste ────────────────────────────────
    render_w = VIEW_W * SCALE
    render_h = BODY_H * SCALE
    render_img = Image.new('RGBA', (render_w, render_h), (0, 0, 0, 0))
    render_draw = ImageDraw.Draw(render_img)

    # Character center and base in render space
    # Place base near bottom of render image, leaving ~3% bottom margin for shadow
    r_cx     = (VIEW_W // 2) * SCALE
    r_base_y = int(BODY_H * SCALE * 0.96)

    draw_fn(render_draw, r_cx, r_base_y)

    # Scale down to 1× with LANCZOS for AA
    render_small = render_img.resize((VIEW_W, BODY_H), Image.LANCZOS)
    # Composite onto canvas
    canvas_img.paste(render_small, (panel_x, HEADER_H), render_small)

    # (Label drawing deferred to main — drawn after bottom bar)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'characters', 'main', 'turnarounds')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'LTG_CHAR_miri_turnaround.png')

    # Create RGBA canvas for compositing
    canvas = Image.new('RGBA', (CANVAS_W, CANVAS_H), (*CANVAS_BG, 255))
    draw = ImageDraw.Draw(canvas)

    # ── Title header ────────────────────────────────────────────────────────────
    # Canvas-wide header bar
    draw.rectangle([0, 0, CANVAS_W, HEADER_H], fill=(38, 28, 20))

    # Load fonts
    try:
        font_title  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        font_label  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_small  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        font_sub    = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except Exception:
        font_title  = ImageFont.load_default()
        font_label  = font_title
        font_small  = font_title
        font_sub    = font_title

    # Title
    title_text = "GRANDMA MIRI — 4-View Character Turnaround"
    draw.text((30, 14), title_text, fill=(240, 230, 210), font=font_title)
    sub_text = "Luma & the Glitchkin  |  MIRI-A Canonical  |  Cycle 20  |  Maya Santos"
    draw.text((30, 38), sub_text, fill=(180, 160, 130), font=font_sub)

    # HU legend (right side of header)
    hu_legend = "HU = Head Unit  (3.2 HU total height)"
    try:
        bbox = font_sub.getbbox(hu_legend)
        lw = bbox[2] - bbox[0]
    except Exception:
        lw = len(hu_legend) * 8
    draw.text((CANVAS_W - lw - 30, 38), hu_legend, fill=(160, 145, 120), font=font_sub)

    # ── Render all 4 view panels ─────────────────────────────────────────────────
    view_fns = [draw_miri_front, draw_miri_three_quarter, draw_miri_side, draw_miri_back]
    for i, (vname, vfn) in enumerate(zip(VIEWS, view_fns)):
        render_view_panel(i, vname, vfn, canvas, font_label, font_small)

    # ── Bottom bar ───────────────────────────────────────────────────────────────
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, VIEW_H - LABEL_H, CANVAS_W, VIEW_H], fill=(38, 28, 20))
    # Label separator line above bottom bar
    draw.line([0, VIEW_H - LABEL_H, CANVAS_W, VIEW_H - LABEL_H], fill=(80, 60, 45), width=2)

    # ── View labels (drawn over bottom bar in light color) ──────────────────────
    for i, vname in enumerate(VIEWS):
        panel_x = i * VIEW_W
        label_y = VIEW_H - LABEL_H + 13
        try:
            bbox = font_label.getbbox(vname)
            tw = bbox[2] - bbox[0]
        except Exception:
            tw = len(vname) * 10
        draw.text((panel_x + (VIEW_W - tw) // 2, label_y),
                  vname, fill=(220, 200, 165), font=font_label)

    # Convert to RGB for PNG save
    out_img = canvas.convert('RGB')
    out_img.save(out_path, 'PNG')
    print(f"Saved: {out_path}")
    print(f"Size: {out_img.size}")


if __name__ == '__main__':
    main()
