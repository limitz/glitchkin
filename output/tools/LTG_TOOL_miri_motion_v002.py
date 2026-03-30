# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_miri_motion_v002.py
Ryo Hasegawa / Cycle 46
Motion Spec Sheet v002 — GRANDMA MIRI (Miriam Okonkwo-Santos)
Beat arc: Emotional Warmth Pacing

4 panels:
  B1: OBSERVING STILL   — hands in lap, held attention, zero secondary motion
  B2: RECOGNITION       — slight forward lean, hands loosen, micro head tilt
  B3: WARMTH BURST      — wide open-arm gesture, eyes crinkle, SUNLIT_AMBER glow halo
  B4: FOND SETTLE       — arms lower to lap/crossed, slight smile return, quiet

Distinct from v001 beat arc (which covers the base repertoire: Warm Attention /
Sharp Assessment / Proud Quiet Joy / Patient Correction). This arc captures the
B1/B4 stillness vs B3 warmth burst contrast — the core of Miri's appeal.
Palette: Real World only. SUNLIT_AMBER (212,146,58) used for B3 warmth glow —
no Glitch/GL colors.

Alex Chen C46 brief:
  "The contrast between B1/B4 stillness and B3 warmth burst is the core of her appeal.
   Use SUNLIT_AMBER as the dominant palette for warm bursts, Real World palette only."

Canvas: 1280x720 (<=1280 limit, native — no thumbnail)
Output: output/characters/motion/LTG_CHAR_miri_motion_v002.png
"""

from PIL import Image, ImageDraw
import os
import math
import json

# --- Load config ---
_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "sheet_geometry_config.json")

def _load_panel_top_miri(default=54):
    """Load panel_top_abs for miri family from sheet_geometry_config.json."""
    try:
        with open(_CONFIG_PATH) as f:
            cfg = json.load(f)
        geo = cfg.get("families", {}).get("miri_v002", {})
        if not geo:
            geo = cfg.get("families", {}).get("miri", {})
        return geo.get("panel_top_abs", default)
    except Exception:
        return default

_MIRI_PANEL_TOP = _load_panel_top_miri(default=54)

# --- CANONICAL COLORS (from grandma_miri.md) ---
SKIN            = (140,  84,  48)   # #8C5430 Deep Warm Brown
SKIN_SH         = (106,  58,  30)   # #6A3A1E Dark Sienna shadow
SKIN_HL         = (168, 106,  64)   # #A86A40 Warm Chestnut highlight
CHEEK_BLUSH     = (212, 149, 107)   # #D4956B Warm Blush (permanent)
HAIR_BASE       = (216, 208, 200)   # #D8D0C8 Silver White
HAIR_SH         = (168, 152, 140)   # #A8988C Warm Gray shadow
HAIR_HL         = (240, 236, 232)   # #F0ECE8 Bright Near-White highlight
CARDIGAN_BASE   = (184,  92,  56)   # #B85C38 Warm Terracotta Rust
CARDIGAN_SH     = (138,  60,  28)   # #8A3C1C Deep Rust
CARDIGAN_HL     = (212, 130,  90)   # #D4825A Dusty Apricot
CARDIGAN_BTN    = (232, 216, 184)   # #E8D8B8 Aged Bone buttons
PANTS           = (200, 174, 138)   # #C8AE8A Warm Linen Tan
PANTS_SH        = (160, 138, 106)   # #A08A6A Warm Medium Tan
SLIPPER_UP      = ( 90, 122,  90)   # #5A7A5A Deep Sage
SLIPPER_BOT     = ( 90,  56,  32)   # #5A3820 Warm Dark Brown sole
EYE_IRIS        = (139,  94,  60)   # #8B5E3C Deep Warm Amber
EYE_PUPIL       = ( 26,  15,  10)   # #1A0F0A Near-Black Espresso
EYE_WHITE       = (250, 240, 220)   # #FAF0DC Warm Cream
EYE_HL          = (240, 240, 240)   # Static White
BROW_COLOR      = (138, 122, 112)   # #8A7A70 Warm Gray brows
LINE_COLOR      = ( 59,  40,  32)   # #3B2820 Deep Cocoa (canonical show line)
ANNOTATION_BG   = (248, 244, 238)   # warm cream panel background
PANEL_BORDER    = (180, 165, 145)
LABEL_BG        = ( 50,  38,  28)
LABEL_TEXT      = (248, 244, 236)
MOTION_ARROW    = (220,  60,  20)   # orange — secondary motion (cardigan, hands)
BEAT_COLOR      = ( 80, 120, 200)   # blue — timing beats (matches Luma/Cosmo/Miri v001)
ACCENT_DASH     = (200, 190, 175)   # construction/guide lines
SUNLIT_AMBER    = (212, 146,  58)   # #D4923A warmth burst glow (Real World warm light)
SUNLIT_PALE     = (245, 220, 160)   # lighter amber for inner glow halo
CRINKLE_COLOR   = ( 80,  55,  40)   # eye crinkle lines on warmth burst

# --- CANVAS ---
W, H  = 1280, 720
COLS  = 4
PAD   = 14
_TITLE_H   = max(_MIRI_PANEL_TOP - PAD, 40)
PANEL_W    = (W - PAD * (COLS + 1)) // COLS
PANEL_H    = H - PAD * 2 - _TITLE_H


# ------------------------------------------------------------------ helpers

def panel_origin(col):
    """Top-left (x, y) of panel col (0-based)."""
    x = PAD + col * (PANEL_W + PAD)
    y = _MIRI_PANEL_TOP
    return x, y


def draw_arrow(draw, x0, y0, x1, y1, color=MOTION_ARROW, width=2, head=8):
    """Draw an arrow from (x0,y0) to (x1,y1) with arrowhead."""
    draw.line([(x0, y0), (x1, y1)], fill=color, width=width)
    angle = math.atan2(y1 - y0, x1 - x0)
    for da in (-0.4, 0.4):
        ax = x1 - head * math.cos(angle + da)
        ay = y1 - head * math.sin(angle + da)
        draw.line([(x1, y1), (int(ax), int(ay))], fill=color, width=width)


def label_box(draw, x, y, text, bg=LABEL_BG, fg=LABEL_TEXT, pad=4):
    """Small filled label rectangle."""
    bbox = draw.textbbox((0, 0), text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rectangle([x, y, x + tw + pad * 2, y + th + pad * 2], fill=bg)
    draw.text((x + pad, y + pad), text, fill=fg)
    return tw + pad * 2, th + pad * 2


# ------------------------------------------------------------------ cardigan knit lines

def draw_cardigan_knit(draw, cx, top_y, bot_y, half_w, head_r):
    """Draw cable-knit suggestion lines on cardigan body (3-4 vertical pairs)."""
    knit_spacing = max(12, int(head_r * 0.55))
    for offset in [-knit_spacing, 0, knit_spacing]:
        kx = cx + offset
        if kx - 3 > cx - half_w and kx + 3 < cx + half_w:
            for x_off in [-2, 2]:
                draw.line(
                    [(kx + x_off, top_y + 4), (kx + x_off, bot_y - 4)],
                    fill=CARDIGAN_SH, width=1
                )


# ------------------------------------------------------------------ character drawing

def draw_miri_figure(draw, ox, oy, head_r=22,
                     body_lean=0,
                     head_tilt=0,
                     arm_left_angle=-170,
                     arm_right_angle=-10,
                     weight_back=False,
                     arms_open=False,
                     hands_in_lap=False):
    """
    Draw Miri as a geometric construction figure.
    ox, oy = center-bottom of figure.
    Miri proportions: 3.2 heads tall.

    body_lean: degrees (negative = forward lean, positive = back)
    head_tilt: degrees (negative = tilt left/viewer-right, positive = right)
    weight_back: if True, body CG shifts back 3px
    arms_open: if True, both arms extended wide (WARMTH BURST gesture)
    hands_in_lap: if True, both arms angled toward lap/center (OBSERVING STILL)
    """
    hr  = head_r
    hw  = int(hr * 0.96)

    body_h  = int(hr * 1.22)
    body_w  = int(hr * 1.05)
    neck_h  = int(hr * 0.09)
    leg_h   = int(hr * 1.07)
    leg_w   = int(hr * 0.42)
    cardigan_hem_extra = int(hr * 0.58)

    foot_w  = int(hr * 0.72)
    foot_h  = int(hr * 0.24)

    lw = 3

    cg_back_offset = 4 if weight_back else 0
    lean_off = int(math.tan(math.radians(body_lean)) * body_h)

    # --- SLIPPERS ---
    fc = int(leg_w * 0.85)
    lf_cx = ox - fc + cg_back_offset
    rf_cx = ox + fc + cg_back_offset
    fy = oy
    draw.ellipse([lf_cx - foot_w // 2, fy - foot_h,
                  lf_cx + foot_w // 2, fy], fill=SLIPPER_BOT, outline=LINE_COLOR, width=lw)
    draw.ellipse([rf_cx - foot_w // 2, fy - foot_h,
                  rf_cx + foot_w // 2, fy], fill=SLIPPER_BOT, outline=LINE_COLOR, width=lw)
    draw.ellipse([lf_cx - foot_w // 2 + 2, fy - foot_h,
                  lf_cx + foot_w // 2 - 2, fy - 4], fill=SLIPPER_UP, outline=LINE_COLOR, width=lw)
    draw.ellipse([rf_cx - foot_w // 2 + 2, fy - foot_h,
                  rf_cx + foot_w // 2 - 2, fy - 4], fill=SLIPPER_UP, outline=LINE_COLOR, width=lw)

    # --- LEGS ---
    leg_top_y = oy - leg_h
    ll_cx = ox - fc // 2 + cg_back_offset
    rl_cx = ox + fc // 2 + cg_back_offset
    top_lw = int(leg_w * 1.05)
    for side, cx_leg in [(-1, ll_cx), (1, rl_cx)]:
        draw.polygon([
            cx_leg - top_lw // 2 + lean_off, leg_top_y,
            cx_leg + top_lw // 2 + lean_off, leg_top_y,
            cx_leg + leg_w // 2 + lean_off // 2, oy - foot_h + 2,
            cx_leg - leg_w // 2 + lean_off // 2, oy - foot_h + 2,
        ], fill=PANTS, outline=LINE_COLOR)
    for cx_leg in [ll_cx, rl_cx]:
        draw.line([(cx_leg + lean_off // 2, leg_top_y + 4),
                   (cx_leg + lean_off // 2, oy - foot_h - 4)],
                  fill=PANTS_SH, width=1)

    # --- TORSO ---
    body_bot_y = oy - leg_h + int(hr * 0.52)
    body_top_y = body_bot_y - body_h
    body_cx    = ox + lean_off + cg_back_offset

    cardigan_bot = body_bot_y + cardigan_hem_extra
    cardigan_w_bot = body_w + int(hr * 0.16)
    draw.polygon([
        body_cx - body_w,        body_top_y,
        body_cx + body_w,        body_top_y,
        body_cx + cardigan_w_bot, cardigan_bot,
        body_cx - cardigan_w_bot, cardigan_bot,
    ], fill=CARDIGAN_BASE, outline=LINE_COLOR)

    draw_cardigan_knit(draw, body_cx, body_top_y, cardigan_bot, body_w, head_r=hr)

    btn_r = max(3, int(hr * 0.13))
    btn_spacing = (cardigan_bot - body_top_y) // 5
    for i in range(1, 5):
        bx = body_cx
        by = body_top_y + i * btn_spacing
        draw.ellipse([bx - btn_r, by - btn_r, bx + btn_r, by + btn_r],
                     fill=CARDIGAN_BTN, outline=LINE_COLOR, width=1)

    v_w = int(body_w * 0.35)
    v_depth = int(body_h * 0.30)
    draw.polygon([
        body_cx, body_top_y + v_depth,
        body_cx - v_w, body_top_y + 2,
        body_cx + v_w, body_top_y + 2,
    ], fill=EYE_WHITE)

    for side in [-1, 1]:
        draw.line([(body_cx + side * (body_w - 4), body_top_y + 6),
                   (body_cx + side * (cardigan_w_bot - 4), cardigan_bot - 6)],
                  fill=CARDIGAN_SH, width=2)

    pkt_top = body_bot_y - int(hr * 0.30)
    pkt_bot = cardigan_bot - 8
    pkt_w   = int(body_w * 0.60)
    for side in [-1, 1]:
        pkt_cx = body_cx + side * int(body_w * 0.52)
        draw.rectangle([pkt_cx - pkt_w // 2, pkt_top,
                        pkt_cx + pkt_w // 2, pkt_bot],
                       outline=CARDIGAN_SH, width=2)

    # --- SHOULDER MARKERS ---
    shoulder_y = body_top_y + int(hr * 0.14)
    shoulder_r = 4
    for sx in [body_cx - body_w, body_cx + body_w]:
        draw.ellipse([sx - shoulder_r, shoulder_y - shoulder_r,
                      sx + shoulder_r, shoulder_y + shoulder_r],
                     fill=ACCENT_DASH, outline=LINE_COLOR, width=1)

    # --- ARMS ---
    arm_h  = int(hr * 1.45)
    arm_w  = int(hr * 0.30)

    if arms_open:
        # B3 WARMTH BURST: both arms spread wide, elevated, welcoming
        # Right arm (viewer's left): reaches left and up at ~-120°
        ang_r = math.radians(-118)
        ar_ex = body_cx - body_w + int(arm_h * math.cos(ang_r))
        ar_ey = shoulder_y + int(arm_h * math.sin(-ang_r))
        draw.polygon([
            body_cx - body_w - arm_w // 2, shoulder_y,
            body_cx - body_w + arm_w // 2, shoulder_y,
            ar_ex + arm_w // 2, ar_ey,
            ar_ex - arm_w // 2, ar_ey,
        ], fill=CARDIGAN_BASE, outline=LINE_COLOR)
        draw.ellipse([ar_ex - int(arm_w * 0.75), ar_ey,
                      ar_ex + int(arm_w * 0.75), ar_ey + int(hr * 0.32)],
                     fill=SKIN, outline=LINE_COLOR, width=2)

        # Left arm (viewer's right): reaches right and up at ~-60° (mirror)
        ang_l = math.radians(-62)
        al_ex = body_cx + body_w + int(arm_h * math.cos(ang_l))
        al_ey = shoulder_y + int(arm_h * math.sin(-ang_l))
        draw.polygon([
            body_cx + body_w - arm_w // 2, shoulder_y,
            body_cx + body_w + arm_w // 2, shoulder_y,
            al_ex + arm_w // 2, al_ey,
            al_ex - arm_w // 2, al_ey,
        ], fill=CARDIGAN_BASE, outline=LINE_COLOR)
        draw.ellipse([al_ex - int(arm_w * 0.75), al_ey,
                      al_ex + int(arm_w * 0.75), al_ey + int(hr * 0.32)],
                     fill=SKIN, outline=LINE_COLOR, width=2)

    elif hands_in_lap:
        # B1 OBSERVING STILL: both arms angled inward toward lap, hands near center
        # Right arm (viewer's left): angled inward-down toward lap
        ang_r = math.radians(-30)
        ar_ex = body_cx - body_w + int(arm_h * math.cos(ang_r))
        ar_ey = shoulder_y + int(arm_h * math.sin(-ang_r))
        draw.polygon([
            body_cx - body_w - arm_w // 2, shoulder_y,
            body_cx - body_w + arm_w // 2, shoulder_y,
            ar_ex + arm_w // 2, ar_ey,
            ar_ex - arm_w // 2, ar_ey,
        ], fill=CARDIGAN_BASE, outline=LINE_COLOR)
        draw.ellipse([ar_ex - int(arm_w * 0.75), ar_ey,
                      ar_ex + int(arm_w * 0.75), ar_ey + int(hr * 0.32)],
                     fill=SKIN, outline=LINE_COLOR, width=2)

        # Left arm (viewer's right): symmetric inward-down
        ang_l = math.radians(-150)
        al_ex = body_cx + body_w + int(arm_h * math.cos(ang_l))
        al_ey = shoulder_y + int(arm_h * math.sin(-ang_l))
        draw.polygon([
            body_cx + body_w - arm_w // 2, shoulder_y,
            body_cx + body_w + arm_w // 2, shoulder_y,
            al_ex + arm_w // 2, al_ey,
            al_ex - arm_w // 2, al_ey,
        ], fill=CARDIGAN_BASE, outline=LINE_COLOR)
        draw.ellipse([al_ex - int(arm_w * 0.75), al_ey,
                      al_ex + int(arm_w * 0.75), al_ey + int(hr * 0.32)],
                     fill=SKIN, outline=LINE_COLOR, width=2)

    else:
        # Default comfortable-ready arms (natural hang with slight elbow bend)
        ang_r = math.radians(arm_right_angle)
        ar_ex = body_cx - body_w + int(arm_h * math.cos(ang_r))
        ar_ey = shoulder_y + int(arm_h * math.sin(-ang_r))
        draw.polygon([
            body_cx - body_w - arm_w // 2, shoulder_y,
            body_cx - body_w + arm_w // 2, shoulder_y,
            ar_ex + arm_w // 2, ar_ey,
            ar_ex - arm_w // 2, ar_ey,
        ], fill=CARDIGAN_BASE, outline=LINE_COLOR)
        draw.ellipse([ar_ex - int(arm_w * 0.75), ar_ey,
                      ar_ex + int(arm_w * 0.75), ar_ey + int(hr * 0.32)],
                     fill=SKIN, outline=LINE_COLOR, width=2)

        ang_l = math.radians(arm_left_angle)
        al_ex = body_cx + body_w + int(arm_h * math.cos(ang_l))
        al_ey = shoulder_y + int(arm_h * math.sin(-ang_l))
        draw.polygon([
            body_cx + body_w - arm_w // 2, shoulder_y,
            body_cx + body_w + arm_w // 2, shoulder_y,
            al_ex + arm_w // 2, al_ey,
            al_ex - arm_w // 2, al_ey,
        ], fill=CARDIGAN_BASE, outline=LINE_COLOR)
        draw.ellipse([al_ex - int(arm_w * 0.75), al_ey,
                      al_ex + int(arm_w * 0.75), al_ey + int(hr * 0.32)],
                     fill=SKIN, outline=LINE_COLOR, width=2)

    # --- NECK ---
    neck_top  = body_top_y - neck_h
    neck_bot  = body_top_y
    neck_w    = int(hr * 0.20)
    neck_cx   = body_cx
    draw.rectangle([neck_cx - neck_w, neck_top,
                    neck_cx + neck_w, neck_bot],
                   fill=SKIN, outline=LINE_COLOR, width=lw)

    # --- HEAD ---
    head_lean_off = int(math.tan(math.radians(head_tilt)) * hr * 0.7)
    head_cx  = neck_cx + head_lean_off
    head_bot = neck_top
    head_top = head_bot - int(hr * 2.0)
    head_cy  = (head_top + head_bot) // 2
    draw.ellipse([head_cx - hw, head_top, head_cx + hw, head_bot],
                 fill=SKIN, outline=LINE_COLOR, width=lw)
    hl_r = max(4, int(hr * 0.22))
    draw.ellipse([head_cx - hl_r // 2, head_top + int(hr * 0.28),
                  head_cx + hl_r // 2, head_top + int(hr * 0.28) + hl_r // 2],
                 fill=SKIN_HL)

    # --- HAIR (silver bun) ---
    bun_cy  = head_top - int(hr * 0.18)
    bun_rx  = int(hr * 0.55)
    bun_ry  = int(hr * 0.32)
    draw.ellipse([head_cx - bun_rx, bun_cy - bun_ry,
                  head_cx + bun_rx, bun_cy + bun_ry + 4],
                 fill=HAIR_BASE, outline=LINE_COLOR, width=2)
    draw.ellipse([head_cx - int(bun_rx * 0.45), bun_cy - int(bun_ry * 0.70),
                  head_cx + int(bun_rx * 0.45), bun_cy],
                 fill=HAIR_HL)
    draw.arc([head_cx - bun_rx + 4, bun_cy,
              head_cx + bun_rx - 4, bun_cy + bun_ry + 2],
             start=0, end=180, fill=HAIR_SH, width=2)
    for side, wx_off, wy_off in [
        (-1, int(hw * 0.72), int(hr * 0.20)),
        ( 1, int(hw * 0.68), int(hr * 0.14)),
        (-1, int(hw * 0.80), int(hr * 0.42)),
    ]:
        wisp_x = head_cx + side * wx_off
        wisp_y = head_top + wy_off
        draw.arc([wisp_x - 5, wisp_y - 6, wisp_x + 5, wisp_y + 6],
                 start=180 if side == -1 else 0, end=350 if side == -1 else 170,
                 fill=HAIR_BASE, width=2)

    # --- FACE FEATURES ---
    face_cy = head_cy + int(hr * 0.06)

    # Cheek blush
    for side in [-1, 1]:
        blush_cx = head_cx + side * int(hw * 0.52)
        draw.ellipse([blush_cx - int(hr * 0.22), face_cy + int(hr * 0.02),
                      blush_cx + int(hr * 0.22), face_cy + int(hr * 0.26)],
                     fill=CHEEK_BLUSH)

    # Eyebrows
    brow_y   = face_cy - int(hr * 0.44)
    brow_sep = int(hw * 0.48)
    for side in [-1, 1]:
        bx = head_cx + side * brow_sep
        draw.line([bx - int(hw * 0.20), brow_y + 2,
                   bx + int(hw * 0.20) * (-side), brow_y - 2],
                  fill=BROW_COLOR, width=2)

    # Eyes
    eye_sep = int(hw * 0.46)
    eye_rx  = int(hr * 0.20)
    eye_ry  = int(hr * 0.15)
    for side in [-1, 1]:
        ex = head_cx + side * eye_sep
        ey = face_cy - int(hr * 0.10)
        draw.ellipse([ex - eye_rx, ey - eye_ry, ex + eye_rx, ey + eye_ry],
                     fill=EYE_WHITE, outline=LINE_COLOR, width=2)
        ir = int(eye_rx * 0.65)
        draw.ellipse([ex - ir, ey - min(ir, eye_ry - 1),
                      ex + ir, ey + min(ir, eye_ry - 1)], fill=EYE_IRIS)
        pr = int(ir * 0.52)
        draw.ellipse([ex - pr, ey - pr, ex + pr, ey + pr], fill=EYE_PUPIL)
        draw.ellipse([ex - int(ir * 0.30) - 2, ey - int(ir * 0.38) - 2,
                      ex - int(ir * 0.30) + 3, ey - int(ir * 0.38) + 3],
                     fill=EYE_HL)
        draw.arc([ex - eye_rx, ey - eye_ry, ex + eye_rx, ey + int(eye_ry * 0.4)],
                 start=200, end=340, fill=LINE_COLOR, width=3)
        # Crow's feet
        cw_x = ex + side * (eye_rx + 2)
        draw.arc([cw_x - 5, ey - 3, cw_x + 5, ey + 6],
                 start=0 if side == 1 else 180, end=90 if side == 1 else 270,
                 fill=LINE_COLOR, width=1)

    # Nose
    draw.arc([head_cx - int(hr * 0.10), face_cy + int(hr * 0.14),
              head_cx + int(hr * 0.10), face_cy + int(hr * 0.30)],
             start=130, end=310, fill=LINE_COLOR, width=3)

    # Mouth
    draw.arc([head_cx - int(hw * 0.30), face_cy + int(hr * 0.28),
              head_cx + int(hw * 0.30), face_cy + int(hr * 0.54)],
             start=10, end=170, fill=LINE_COLOR, width=3)

    # Smile lines
    for side in [-1, 1]:
        smx = head_cx + side * int(hw * 0.26)
        draw.arc([smx - 4, face_cy + int(hr * 0.25),
                  smx + 4, face_cy + int(hr * 0.56)],
                 start=200 if side == -1 else 340, end=320 if side == -1 else 100,
                 fill=LINE_COLOR, width=1)

    return (head_cx, head_cy, hr, body_cx, body_bot_y, body_w,
            body_top_y, shoulder_y, cardigan_bot, cardigan_w_bot,
            ll_cx, rl_cx)


# ------------------------------------------------------------------ PANEL DRAWING

def draw_panel_bg(draw, col, title, subtitle="", beat_label=""):
    px, py = panel_origin(col)
    draw.rectangle([px, py, px + PANEL_W, py + PANEL_H],
                   fill=ANNOTATION_BG, outline=PANEL_BORDER, width=1)
    draw.rectangle([px, py + PANEL_H - 30, px + PANEL_W, py + PANEL_H], fill=LABEL_BG)
    draw.text((px + 6, py + PANEL_H - 24), title, fill=LABEL_TEXT)
    if subtitle:
        draw.text((px + 6, py + PANEL_H - 13), subtitle, fill=(200, 190, 170))
    badge = beat_label or f"B{col + 1}"
    draw.rectangle([px + 3, py + 3, px + 36, py + 22], fill=BEAT_COLOR)
    draw.text((px + 6, py + 5), badge, fill=(240, 248, 255))


def draw_panel0_observing_still(img, draw):
    """Panel 0: OBSERVING STILL — hands in lap, minimal movement, held attention."""
    col = 0
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "OBSERVING STILL", "hands in lap — held attention", beat_label="B1")

    fig_x = px + PANEL_W // 2
    fig_y = py + PANEL_H - 48

    (hcx, hcy, hr, bcx, bby, bw, bty, shy,
     cdn_bot, cdn_w,
     ll_cx, rl_cx) = draw_miri_figure(
        draw, fig_x, fig_y, head_r=22,
        body_lean=0, head_tilt=0,
        weight_back=False,
        hands_in_lap=True)
    draw = ImageDraw.Draw(img)

    # Ground line
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)], fill=ACCENT_DASH, width=1)

    # Vertical centerline (absolute stillness — visual axis)
    draw.line([(bcx, bty - int(hr * 2.2)), (bcx, fig_y + 2)], fill=ACCENT_DASH, width=1)
    draw.text((bcx + 4, bty + int(hr * 0.3)), "CL — STILL", fill=ACCENT_DASH)

    # Zero secondary motion annotation
    label_box(draw, px + 8, py + PANEL_H - 90, "ZERO DRIFT",
              bg=(40, 30, 20), fg=(200, 190, 170))
    draw.text((px + 8, py + PANEL_H - 78), "no hover, no idle sway", fill=ACCENT_DASH)
    draw.text((px + 8, py + PANEL_H - 66), "cardigan: motionless", fill=ACCENT_DASH)

    # Attention direction annotation (she's watching something)
    draw_arrow(draw, hcx + hr + 2, hcy, hcx + hr + 22, hcy + 4,
               color=BEAT_COLOR, width=2, head=6)
    draw.text((hcx + hr + 24, hcy - 8), "watching —", fill=BEAT_COLOR)
    draw.text((hcx + hr + 24, hcy + 4), "held gaze", fill=BEAT_COLOR)

    # Hands in lap construction detail
    draw.text((px + 8, bby - 8), "hands resting", fill=ACCENT_DASH)
    draw.text((px + 8, bby + 4), "near lap", fill=ACCENT_DASH)

    # Timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y),      "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Hold: indefinite", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "No drift — truly still", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 37), "Blink rate: slow (calm)", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 49), "Breath: visible (slight", fill=ACCENT_DASH)
    draw.text((px + 8, timing_y + 61), "  shoulder rise, +0.5px)", fill=ACCENT_DASH)


def draw_panel1_recognition(img, draw):
    """Panel 1: RECOGNITION — slight forward lean, hands loosen, micro head tilt."""
    col = 1
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "RECOGNITION", "she sees what matters — lean begins", beat_label="B2")

    fig_x = px + PANEL_W // 2
    fig_y = py + PANEL_H - 48

    (hcx, hcy, hr, bcx, bby, bw, bty, shy,
     cdn_bot, cdn_w,
     ll_cx, rl_cx) = draw_miri_figure(
        draw, fig_x, fig_y, head_r=22,
        body_lean=-2, head_tilt=-3,      # subtle forward lean, head tilts slightly
        arm_right_angle=-22, arm_left_angle=-158,
        weight_back=False)
    draw = ImageDraw.Draw(img)

    # Ground line
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)], fill=ACCENT_DASH, width=1)

    # Forward lean annotation
    draw_arrow(draw, bcx - 4, bty + 10, bcx - 16, bty - 2,
               color=MOTION_ARROW, width=2, head=6)
    draw.text((px + 8, py + PANEL_H - 80), "-2° lean begins", fill=MOTION_ARROW)
    draw.text((px + 8, py + PANEL_H - 68), "beat 1.5 (head first)", fill=BEAT_COLOR)

    # Head tilt label
    draw_arrow(draw, hcx - hr - 2, hcy - int(hr * 0.5),
               hcx - hr - 18, hcy - int(hr * 0.7),
               color=BEAT_COLOR, width=2, head=6)
    draw.text((px + 8, hcy - int(hr * 0.85)), "-3° micro", fill=BEAT_COLOR)
    draw.text((px + 8, hcy - int(hr * 0.73)), "head tilt", fill=BEAT_COLOR)

    # Hands loosening annotation
    draw.text((bcx - bw + 4, bby + 2), "hands open", fill=MOTION_ARROW)
    draw.text((bcx - bw + 4, bby + 14), "from lap (beat 2)", fill=MOTION_ARROW)

    # Cardigan lag annotation — begins to move after lean
    draw_arrow(draw, bcx + cdn_w - 4, cdn_bot - 10,
               bcx + cdn_w + 12, cdn_bot + 8,
               color=MOTION_ARROW, width=2, head=6)
    draw.text((bcx + cdn_w + 14, cdn_bot - 4), "cardigan lag", fill=MOTION_ARROW)
    draw.text((bcx + cdn_w + 14, cdn_bot + 8), "+2.0 beats", fill=MOTION_ARROW)

    # Timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y),      "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Head tilt: beat 1 (leads)", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Body lean: beat 1.5", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 37), "Hands open: beat 2", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 49), "Cardigan: beat 3.5", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 61), "Eyes: widen slightly", fill=BEAT_COLOR)


def draw_panel2_warmth_burst(img, draw):
    """Panel 2: WARMTH BURST — wide open-arm gesture, eyes crinkle, SUNLIT_AMBER glow."""
    col = 2
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "WARMTH BURST", "open arms — SUNLIT_AMBER glow", beat_label="B3")

    fig_x = px + PANEL_W // 2
    fig_y = py + PANEL_H - 48

    # Draw SUNLIT_AMBER radial glow BEHIND figure (draw first so figure overlays it)
    # Glow centered on Miri's torso/chest — warmth emanates from her
    glow_cx = fig_x
    glow_cy = fig_y - 90    # approx torso center
    for radius, alpha_rgb in [
        (72, (245, 220, 160)),   # inner warm bright
        (105, (240, 200, 130)),  # mid amber
        (130, (232, 180, 105)),  # outer diffuse
    ]:
        draw.ellipse([glow_cx - radius, glow_cy - radius,
                      glow_cx + radius, glow_cy + radius],
                     fill=alpha_rgb, outline=None)
    # Re-draw panel background border on top of glow (keep panel clean outside glow)
    draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], fill=None, outline=PANEL_BORDER, width=1)

    (hcx, hcy, hr, bcx, bby, bw, bty, shy,
     cdn_bot, cdn_w,
     ll_cx, rl_cx) = draw_miri_figure(
        draw, fig_x, fig_y, head_r=22,
        body_lean=0, head_tilt=0,        # open and centered — she gives the space
        weight_back=False,
        arms_open=True)
    draw = ImageDraw.Draw(img)

    # Ground line
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)], fill=ACCENT_DASH, width=1)

    # Glow annotation
    label_box(draw, px + 8, py + 8, "SUNLIT_AMBER HALO",
              bg=(140, 80, 20), fg=(248, 230, 180))
    draw.text((px + 8, py + 30), "212,146,58 — Real World warm", fill=SUNLIT_AMBER)
    draw.text((px + 8, py + 42), "NO Glitch palette here", fill=ACCENT_DASH)

    # Eye crinkle annotation (eyes crinkle fully closed on B3 peak)
    draw.text((hcx + hr + 4, hcy - int(hr * 0.4)), "eyes crinkle", fill=CRINKLE_COLOR)
    draw.text((hcx + hr + 4, hcy - int(hr * 0.28)), "fully closed", fill=CRINKLE_COLOR)
    draw.text((hcx + hr + 4, hcy - int(hr * 0.16)), "at B3 peak", fill=CRINKLE_COLOR)
    # Draw crinkle lines on eyes (override default eye draw — eyes nearly shut)
    eye_sep = int(22 * 0.46)
    for side in [-1, 1]:
        ex = hcx + side * eye_sep
        ey = hcy - int(22 * 0.10)
        # Near-closed eye: just a curved slit
        draw.arc([ex - int(22 * 0.20), ey - 2, ex + int(22 * 0.20), ey + 4],
                 start=200, end=340, fill=LINE_COLOR, width=3)
        # Additional crinkle above
        draw.arc([ex - int(22 * 0.22), ey - int(22 * 0.12),
                  ex + int(22 * 0.22), ey + 2],
                 start=185, end=355, fill=CRINKLE_COLOR, width=1)

    # Open arms annotation
    draw_arrow(draw, bcx - bw - 8, shy,
               bcx - bw - 22, shy - 10,
               color=MOTION_ARROW, width=2, head=6)
    draw.text((px + 8, py + PANEL_H - 90), "arms open wide", fill=MOTION_ARROW)
    draw.text((px + 8, py + PANEL_H - 78), "elevated at shoulder level", fill=MOTION_ARROW)

    # Cardigan hem flutter annotation
    draw_arrow(draw, bcx, cdn_bot - 6, bcx - 10, cdn_bot + 10,
               color=MOTION_ARROW, width=2, head=5)
    draw.text((bcx - cdn_w + 4, cdn_bot + 12), "cardigan hem", fill=MOTION_ARROW)
    draw.text((bcx - cdn_w + 4, cdn_bot + 24), "flutter (lag +2.0b)", fill=MOTION_ARROW)

    # Timing block
    timing_y = py + 56
    draw.text((px + 8, timing_y),      "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Arms spread: beat 1", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Eyes crinkle: beat 1.5", fill=CRINKLE_COLOR)
    draw.text((px + 8, timing_y + 37), "Glow peak: beat 2", fill=(180, 120, 40))
    draw.text((px + 8, timing_y + 49), "Cardigan flutter: beat 3", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 61), "HOLD spread: 4-6 frames", fill=BEAT_COLOR)


def draw_panel3_fond_settle(img, draw):
    """Panel 3: FOND SETTLE — arms lower, slight smile, back to quiet."""
    col = 3
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "FOND SETTLE", "arms lower — back to quiet", beat_label="B4")

    fig_x = px + PANEL_W // 2
    fig_y = py + PANEL_H - 48

    (hcx, hcy, hr, bcx, bby, bw, bty, shy,
     cdn_bot, cdn_w,
     ll_cx, rl_cx) = draw_miri_figure(
        draw, fig_x, fig_y, head_r=22,
        body_lean=0, head_tilt=0,
        arm_right_angle=-32, arm_left_angle=-148,  # arms partially lowered toward crossed/lap
        weight_back=False)
    draw = ImageDraw.Draw(img)

    # Ground line
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)], fill=ACCENT_DASH, width=1)

    # Return to still annotation
    draw.line([(bcx, bty - int(hr * 2.2)), (bcx, fig_y + 2)], fill=ACCENT_DASH, width=1)
    draw.text((bcx + 4, bty + int(hr * 0.3)), "CL — settles", fill=ACCENT_DASH)

    # Ghosted open-arm position (where arms were at B3 — showing the return arc)
    ghost_arm_h = int(22 * 1.45)
    ghost_arm_w = int(22 * 0.30)
    ang_ghost_r = math.radians(-118)
    gr_ex = bcx - bw + int(ghost_arm_h * math.cos(ang_ghost_r))
    gr_ey = shy + int(ghost_arm_h * math.sin(-ang_ghost_r))
    for yy in range(0, ghost_arm_h, 6):
        frac = yy / ghost_arm_h
        gx = int(bcx - bw + frac * (gr_ex - (bcx - bw)))
        gy = int(shy + frac * (gr_ey - shy))
        draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=ACCENT_DASH, outline=None)
    draw.text((gr_ex - 40, gr_ey - 12), "B3 pos", fill=ACCENT_DASH)

    # Smile remaining annotation (slight smile persists — the warmth doesn't fully leave)
    draw.text((hcx + hr + 4, hcy + int(hr * 0.30)), "slight smile", fill=BEAT_COLOR)
    draw.text((hcx + hr + 4, hcy + int(hr * 0.42)), "remains —", fill=BEAT_COLOR)
    draw.text((hcx + hr + 4, hcy + int(hr * 0.54)), "warmth lingers", fill=BEAT_COLOR)

    # Cardigan settling annotation
    draw_arrow(draw, bcx + cdn_w - 4, cdn_bot - 8,
               bcx + cdn_w + 14, cdn_bot + 6,
               color=MOTION_ARROW, width=2, head=6)
    draw.text((bcx + cdn_w + 16, cdn_bot - 4), "cardigan", fill=MOTION_ARROW)
    draw.text((bcx + cdn_w + 16, cdn_bot + 8), "settles last", fill=MOTION_ARROW)
    draw.text((bcx + cdn_w + 16, cdn_bot + 20), "(+2.0b)", fill=MOTION_ARROW)

    # Blush sustain annotation (warmth blush stays at peak level through B4)
    draw.text((hcx - hr - 68, hcy + int(hr * 0.05)), "blush sustained", fill=CHEEK_BLUSH)
    draw.text((hcx - hr - 68, hcy + int(hr * 0.17)), "from B3 peak", fill=CHEEK_BLUSH)

    # Timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y),      "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Arms lower: 4 beats (slow)", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Eyes reopen: beat 1", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 37), "Smile: held +6 frames", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 49), "Blush fades: beat 8+", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 61), "Settle = mirror of B1", fill=ACCENT_DASH)


# ------------------------------------------------------------------ MAIN

def main():
    img = Image.new("RGB", (W, H), color=(242, 236, 226))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, W, PAD + 40], fill=LABEL_BG)
    draw.text((PAD, 8), "GRANDMA MIRI — Motion Spec Sheet v002  |  Emotional Warmth Pacing", fill=LABEL_TEXT)
    draw.text((PAD, 22), "RYO HASEGAWA  |  Luma & the Glitchkin  |  C46  |  Beat arc: STILL→RECOGNITION→WARMTH BURST→FOND SETTLE", fill=(180, 165, 140))

    # Legend strip
    legend_x = W - 310
    draw.rectangle([legend_x - 6, 6, legend_x + 302, PAD + 36], fill=(70, 55, 42))
    draw.text((legend_x,       8), "->  Secondary motion (cardigan)", fill=MOTION_ARROW)
    draw.text((legend_x,      20), "■  Timing beats", fill=BEAT_COLOR)
    draw.text((legend_x + 175,  8), "--  Construction/guide", fill=ACCENT_DASH)
    draw.text((legend_x + 175, 20), "●  SUNLIT_AMBER (warmth)", fill=SUNLIT_AMBER)

    draw_panel0_observing_still(img, draw)
    draw_panel1_recognition(img, draw)
    draw_panel2_warmth_burst(img, draw)
    draw_panel3_fond_settle(img, draw)

    # Save — native 1280x720, no thumbnail
    assert img.width <= 1280 and img.height <= 1280, "Canvas exceeds 1280px limit"

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "characters", "motion")
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_miri_motion_v002.png")
    img.save(out_path)
    print(f"Saved: {out_path} ({img.width}x{img.height}px)")


if __name__ == "__main__":
    main()
