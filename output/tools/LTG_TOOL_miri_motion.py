# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_miri_motion.py
Ryo Hasegawa / Cycle 44
Motion Spec Sheet — GRANDMA MIRI (Miriam Okonkwo-Santos)
4 panels: Warm Attention | Sharp Assessment | Proud Quiet Joy | Patient Correction

Miri motion vocabulary:
  - STILL CENTER: she is the grounded anchor; all her states begin from upright stability.
  - Cardigan secondary motion: heavy cable-knit fabric lags +2.0 beats behind any body shift.
  - Arms default to "comfortable ready" — slight elbow bend, hands often near pockets.
  - Head moves first on emotional cues; body follows (opposite of Luma, who leads with body).
  - No reckless energy. Every lean is deliberate and small (max 6° in any direction).
  - Hands are the most expressive body part after face; two-finger gesture = precision mode.
  - Hair bun: minimal secondary motion — soft but contained. No Luma-style trail.
  - Sharp Assessment: one eyebrow raised, slight chin-down, evaluating lean (3-4° forward).
  - Proud Quiet Joy: weight BACK (she yields space to Luma's energy), shoulders drop 1px.
  - Patient Correction: two-finger raised hand, deliberate — she gestures ONCE.

Canvas: 1280x720 (<=1280 limit)
Output: output/characters/motion/LTG_CHAR_miri_motion.png
"""

from PIL import Image, ImageDraw
import os
import math
import json

# --- Load config (mirrors pattern from luma/byte/cosmo motion tools) ---
_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "sheet_geometry_config.json")

def _load_header_h_miri(default=54):
    """Load HEADER_H for miri family from sheet_geometry_config.json."""
    try:
        with open(_CONFIG_PATH) as f:
            cfg = json.load(f)
        geo = cfg.get("families", {}).get("miri", {})
        return geo.get("panel_top_abs", default)
    except Exception:
        return default

_MIRI_PANEL_TOP = _load_header_h_miri(default=54)

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
BEAT_COLOR      = ( 80, 120, 200)   # blue — timing beats (matches Luma/Cosmo convention)
ACCENT_DASH     = (200, 190, 175)   # construction/guide lines

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
                     arm_left_angle=-170,   # left arm (viewer's right)
                     arm_right_angle=-10,   # right arm (viewer's left)
                     weight_back=False,
                     hand_raised=False):
    """
    Draw Miri as a geometric construction figure.
    ox, oy = center-bottom of figure.
    Miri proportions: 3.2 heads tall (shorter than everyone else).
    Head = compressed circle (88% circular).
    Torso = wide weathered rectangle (1.2x head width).
    Cardigan extends to mid-thigh.

    body_lean: degrees (negative = forward lean, positive = back)
    head_tilt: degrees (negative = tilt left/viewer-right, positive = right)
    weight_back: if True, body CG shifts back 3px (Proud Quiet Joy)
    hand_raised: if True, draw right arm raised with two-finger gesture
    """
    hr  = head_r
    # Head: slightly compressed circle — hw slightly narrower than hr
    hw  = int(hr * 0.96)      # head half-width (88% circular → slightly wider than tall)

    # Miri is 3.2 heads total
    body_h  = int(hr * 1.22)  # torso (slightly wider/shorter than Cosmo)
    body_w  = int(hr * 1.05)  # wide — 1.1x head width shoulders → body_w ~ 1.05hr
    neck_h  = int(hr * 0.09)  # short neck (shorter than Cosmo)
    # Legs: upper 0.55hr + lower 0.52hr = 1.07hr (short and solid)
    leg_h   = int(hr * 1.07)
    leg_w   = int(hr * 0.42)
    # Cardigan extends below torso to mid-thigh
    cardigan_hem_extra = int(hr * 0.58)  # cardigan falls past body_bot to mid-thigh

    foot_w  = int(hr * 0.72)
    foot_h  = int(hr * 0.24)

    lw = 3

    # CG offset for weight_back
    cg_back_offset = 4 if weight_back else 0

    lean_off = int(math.tan(math.radians(body_lean)) * body_h)

    # --- SLIPPERS ---
    fc = int(leg_w * 0.85)  # foot center offset from body center
    lf_cx = ox - fc + cg_back_offset
    rf_cx = ox + fc + cg_back_offset
    fy = oy
    # Sole (bottom)
    draw.ellipse([lf_cx - foot_w // 2, fy - foot_h,
                  lf_cx + foot_w // 2, fy], fill=SLIPPER_BOT, outline=LINE_COLOR, width=lw)
    draw.ellipse([rf_cx - foot_w // 2, fy - foot_h,
                  rf_cx + foot_w // 2, fy], fill=SLIPPER_BOT, outline=LINE_COLOR, width=lw)
    # Upper (sage green) over sole
    draw.ellipse([lf_cx - foot_w // 2 + 2, fy - foot_h,
                  lf_cx + foot_w // 2 - 2, fy - 4], fill=SLIPPER_UP, outline=LINE_COLOR, width=lw)
    draw.ellipse([rf_cx - foot_w // 2 + 2, fy - foot_h,
                  rf_cx + foot_w // 2 - 2, fy - 4], fill=SLIPPER_UP, outline=LINE_COLOR, width=lw)

    # --- LEGS (short, slightly tapered) ---
    leg_top_y = oy - leg_h
    ll_cx = ox - fc // 2 + cg_back_offset
    rl_cx = ox + fc // 2 + cg_back_offset
    # Slight taper toward ankle: top width > bottom width
    top_lw = int(leg_w * 1.05)
    for side, cx_leg in [(-1, ll_cx), (1, rl_cx)]:
        draw.polygon([
            cx_leg - top_lw // 2 + lean_off, leg_top_y,
            cx_leg + top_lw // 2 + lean_off, leg_top_y,
            cx_leg + leg_w // 2 + lean_off // 2, oy - foot_h + 2,
            cx_leg - leg_w // 2 + lean_off // 2, oy - foot_h + 2,
        ], fill=PANTS, outline=LINE_COLOR)
    # Pants shadow (fold line center)
    for cx_leg in [ll_cx, rl_cx]:
        draw.line([(cx_leg + lean_off // 2, leg_top_y + 4),
                   (cx_leg + lean_off // 2, oy - foot_h - 4)],
                  fill=PANTS_SH, width=1)

    # --- TORSO (wide rectangle — Miri's planted foundation) ---
    body_bot_y = oy - leg_h + int(hr * 0.52)
    body_top_y = body_bot_y - body_h
    body_cx    = ox + lean_off + cg_back_offset

    # Cardigan hem (A-shape: falls to mid-thigh, slightly wider than torso)
    cardigan_bot = body_bot_y + cardigan_hem_extra
    cardigan_w_bot = body_w + int(hr * 0.16)  # slight A-shape flare at hem
    draw.polygon([
        body_cx - body_w,        body_top_y,
        body_cx + body_w,        body_top_y,
        body_cx + cardigan_w_bot, cardigan_bot,
        body_cx - cardigan_w_bot, cardigan_bot,
    ], fill=CARDIGAN_BASE, outline=LINE_COLOR)

    # Cable-knit lines on cardigan
    draw_cardigan_knit(draw, body_cx, body_top_y, cardigan_bot, body_w, head_r=hr)

    # Cardigan button row (4 buttons down center)
    btn_r = max(3, int(hr * 0.13))
    btn_spacing = (cardigan_bot - body_top_y) // 5
    for i in range(1, 5):
        bx = body_cx
        by = body_top_y + i * btn_spacing
        draw.ellipse([bx - btn_r, by - btn_r, bx + btn_r, by + btn_r],
                     fill=CARDIGAN_BTN, outline=LINE_COLOR, width=1)

    # Cardigan V-neck opening (shows undershirt cream)
    v_w = int(body_w * 0.35)
    v_depth = int(body_h * 0.30)
    draw.polygon([
        body_cx, body_top_y + v_depth,
        body_cx - v_w, body_top_y + 2,
        body_cx + v_w, body_top_y + 2,
    ], fill=EYE_WHITE)

    # Shadow fold lines on cardigan sides
    for side in [-1, 1]:
        draw.line([(body_cx + side * (body_w - 4), body_top_y + 6),
                   (body_cx + side * (cardigan_w_bot - 4), cardigan_bot - 6)],
                  fill=CARDIGAN_SH, width=2)

    # Pockets (two front pockets, lower half)
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

    if hand_raised:
        # Right arm (viewer's left) raised — two-finger precision gesture
        # Arm up at ~-70° (raised toward speaker level)
        ang_r = math.radians(-68)
        ar_ex = body_cx - body_w + int(arm_h * math.cos(ang_r))
        ar_ey = shoulder_y + int(arm_h * math.sin(-ang_r))
        draw.polygon([
            body_cx - body_w - arm_w // 2, shoulder_y,
            body_cx - body_w + arm_w // 2, shoulder_y,
            ar_ex + arm_w // 2, ar_ey,
            ar_ex - arm_w // 2, ar_ey,
        ], fill=CARDIGAN_BASE, outline=LINE_COLOR)
        # Hand: two fingers pointing up
        finger_base = (ar_ex, ar_ey)
        finger_len  = int(hr * 0.30)
        finger_w    = int(hr * 0.10)
        # Index finger
        draw.rectangle([finger_base[0] - finger_w,    finger_base[1] - finger_len,
                        finger_base[0],               finger_base[1]],
                       fill=SKIN, outline=LINE_COLOR, width=2)
        # Middle finger
        draw.rectangle([finger_base[0] + 2,            finger_base[1] - finger_len,
                        finger_base[0] + finger_w + 2, finger_base[1]],
                       fill=SKIN, outline=LINE_COLOR, width=2)
        # Remaining fingers (closed fist implied — smaller)
        draw.rectangle([finger_base[0] - finger_w - 2, finger_base[1] - int(finger_len * 0.55),
                        finger_base[0] + finger_w + 4, finger_base[1]],
                       fill=SKIN, outline=LINE_COLOR, width=1)
    else:
        # Right arm (viewer's left) — natural comfortable bend
        ang_r = math.radians(arm_right_angle)
        ar_ex = body_cx - body_w + int(arm_h * math.cos(ang_r))
        ar_ey = shoulder_y + int(arm_h * math.sin(-ang_r))
        draw.polygon([
            body_cx - body_w - arm_w // 2, shoulder_y,
            body_cx - body_w + arm_w // 2, shoulder_y,
            ar_ex + arm_w // 2, ar_ey,
            ar_ex - arm_w // 2, ar_ey,
        ], fill=CARDIGAN_BASE, outline=LINE_COLOR)
        # Hand (simple oval — working hands)
        draw.ellipse([ar_ex - int(arm_w * 0.75), ar_ey,
                      ar_ex + int(arm_w * 0.75), ar_ey + int(hr * 0.32)],
                     fill=SKIN, outline=LINE_COLOR, width=2)

    # Left arm (viewer's right) — comfortable default
    ang_l = math.radians(arm_left_angle)
    al_ex = body_cx + body_w + int(arm_h * math.cos(ang_l))
    al_ey = shoulder_y + int(arm_h * math.sin(-ang_l))
    draw.polygon([
        body_cx + body_w - arm_w // 2, shoulder_y,
        body_cx + body_w + arm_w // 2, shoulder_y,
        al_ex + arm_w // 2, al_ey,
        al_ex - arm_w // 2, al_ey,
    ], fill=CARDIGAN_BASE, outline=LINE_COLOR)
    # Left hand
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

    # --- HEAD (compressed circle — "88% circular") ---
    head_lean_off = int(math.tan(math.radians(head_tilt)) * hr * 0.7)
    head_cx  = neck_cx + head_lean_off
    head_bot = neck_top
    head_top = head_bot - int(hr * 2.0)    # diameter = 2*hr
    head_cy  = (head_top + head_bot) // 2
    # Compressed: rx slightly wider than ry for that "settled" circle feel
    draw.ellipse([head_cx - hw, head_top, head_cx + hw, head_bot],
                 fill=SKIN, outline=LINE_COLOR, width=lw)
    # Highlight on forehead
    hl_r = max(4, int(hr * 0.22))
    draw.ellipse([head_cx - hl_r // 2, head_top + int(hr * 0.28),
                  head_cx + hl_r // 2, head_top + int(hr * 0.28) + hl_r // 2],
                 fill=SKIN_HL)

    # --- HAIR (silver bun — adds 0.25hr height above skull) ---
    bun_cy  = head_top - int(hr * 0.18)
    bun_rx  = int(hr * 0.55)
    bun_ry  = int(hr * 0.32)
    draw.ellipse([head_cx - bun_rx, bun_cy - bun_ry,
                  head_cx + bun_rx, bun_cy + bun_ry + 4],
                 fill=HAIR_BASE, outline=LINE_COLOR, width=2)
    # Bun highlight (crown)
    draw.ellipse([head_cx - int(bun_rx * 0.45), bun_cy - int(bun_ry * 0.70),
                  head_cx + int(bun_rx * 0.45), bun_cy],
                 fill=HAIR_HL)
    # Bun shadow (lower half)
    draw.arc([head_cx - bun_rx + 4, bun_cy,
              head_cx + bun_rx - 4, bun_cy + bun_ry + 2],
             start=0, end=180, fill=HAIR_SH, width=2)
    # Escaping wisps (2-3 at temples — Miri's hair always escapes a little)
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

    # Permanent cheek blush (always present)
    for side in [-1, 1]:
        blush_cx = head_cx + side * int(hw * 0.52)
        draw.ellipse([blush_cx - int(hr * 0.22), face_cy + int(hr * 0.02),
                      blush_cx + int(hr * 0.22), face_cy + int(hr * 0.26)],
                     fill=CHEEK_BLUSH)

    # Eyebrows (softer and narrower than Luma's — natural slight arch)
    brow_y   = face_cy - int(hr * 0.44)
    brow_sep = int(hw * 0.48)
    for side in [-1, 1]:
        bx = head_cx + side * brow_sep
        # Natural arch — outer end slightly higher
        draw.line([bx - int(hw * 0.20), brow_y + 2,
                   bx + int(hw * 0.20) * (-side), brow_y - 2],
                  fill=BROW_COLOR, width=2)

    # Eyes (rounded almonds — horizontal, steady)
    eye_sep = int(hw * 0.46)
    eye_rx  = int(hr * 0.20)   # slightly wider than Luma (steady gaze)
    eye_ry  = int(hr * 0.15)   # more horizontal
    for side in [-1, 1]:
        ex = head_cx + side * eye_sep
        ey = face_cy - int(hr * 0.10)
        # White
        draw.ellipse([ex - eye_rx, ey - eye_ry, ex + eye_rx, ey + eye_ry],
                     fill=EYE_WHITE, outline=LINE_COLOR, width=2)
        # Iris (deep warm amber)
        ir = int(eye_rx * 0.65)
        draw.ellipse([ex - ir, ey - min(ir, eye_ry - 1),
                      ex + ir, ey + min(ir, eye_ry - 1)], fill=EYE_IRIS)
        # Pupil
        pr = int(ir * 0.52)
        draw.ellipse([ex - pr, ey - pr, ex + pr, ey + pr], fill=EYE_PUPIL)
        # Highlight — upper-left (same as Luma: visual DNA marker)
        draw.ellipse([ex - int(ir * 0.30) - 2, ey - int(ir * 0.38) - 2,
                      ex - int(ir * 0.30) + 3, ey - int(ir * 0.38) + 3],
                     fill=EYE_HL)
        # Upper eyelid — slight heaviness (calm, not tired)
        draw.arc([ex - eye_rx, ey - eye_ry, ex + eye_rx, ey + int(eye_ry * 0.4)],
                 start=200, end=340, fill=LINE_COLOR, width=3)
        # Crow's feet (always present — laugh lines)
        cw_x = ex + side * (eye_rx + 2)
        draw.arc([cw_x - 5, ey - 3, cw_x + 5, ey + 6],
                 start=0 if side == 1 else 180, end=90 if side == 1 else 270,
                 fill=LINE_COLOR, width=1)

    # Nose (more defined than Luma — button with bridge suggestion)
    draw.arc([head_cx - int(hr * 0.10), face_cy + int(hr * 0.14),
              head_cx + int(hr * 0.10), face_cy + int(hr * 0.30)],
             start=130, end=310, fill=LINE_COLOR, width=3)

    # Mouth (default: gentle closed upward curve — always almost smiling)
    draw.arc([head_cx - int(hw * 0.30), face_cy + int(hr * 0.28),
              head_cx + int(hw * 0.30), face_cy + int(hr * 0.54)],
             start=10, end=170, fill=LINE_COLOR, width=3)

    # Smile lines (faint — always present, record of every smile)
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
    # Beat badge: colored box top-left (required for lint check_beat_badges)
    badge = beat_label or f"B{col + 1}"
    draw.rectangle([px + 3, py + 3, px + 36, py + 22], fill=BEAT_COLOR)
    draw.text((px + 6, py + 5), badge, fill=(240, 248, 255))


def draw_panel0_warm_attention(img, draw):
    """Panel 0: WARM ATTENTION — Miri's default. Upright, present, slight forward emotional lean."""
    col = 0
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "WARM ATTENTION", "Miri default — still center", beat_label="B1")

    fig_x = px + PANEL_W // 2
    fig_y = py + PANEL_H - 48

    (hcx, hcy, hr, bcx, bby, bw, bty, shy,
     cdn_bot, cdn_w,
     ll_cx, rl_cx) = draw_miri_figure(
        draw, fig_x, fig_y, head_r=22,
        body_lean=0, head_tilt=2,       # very slight forward incline of head
        arm_right_angle=-22, arm_left_angle=-158,
        weight_back=False)
    draw = ImageDraw.Draw(img)

    # Ground line
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)], fill=ACCENT_DASH, width=1)
    draw.text((px + 14, fig_y + 3), "GROUND", fill=ACCENT_DASH)

    # Upright construction line (she stays vertical — this is deliberate)
    draw.line([(bcx, bty - hr * 2 - 14), (bcx, fig_y + 2)], fill=ACCENT_DASH, width=1)
    draw.text((bcx + 4, bty), "CL — VERTICAL", fill=ACCENT_DASH)

    # Cardigan secondary motion annotation
    draw_arrow(draw, bcx + cdn_w - 6, cdn_bot - 12,
               bcx + cdn_w + 14, cdn_bot + 8,
               color=MOTION_ARROW, width=2, head=6)
    draw.text((bcx + cdn_w + 16, cdn_bot - 2), "cardigan", fill=MOTION_ARROW)
    draw.text((bcx + cdn_w + 16, cdn_bot + 10), "+2.0 beats", fill=MOTION_ARROW)
    draw.text((bcx + cdn_w + 16, cdn_bot + 22), "behind body", fill=MOTION_ARROW)

    # Head-first annotation (she leads with emotional presence before body moves)
    draw_arrow(draw, hcx - hr - 4, hcy - hr + 10,
               hcx - hr - 22, hcy - hr + 24,
               color=BEAT_COLOR, width=2, head=6)
    draw.text((px + 6, hcy - hr + 30), "+2° head", fill=BEAT_COLOR)
    draw.text((px + 6, hcy - hr + 42), "precedes body", fill=BEAT_COLOR)

    # Timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y),      "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Head: beat 1 (leads)", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Weight settle: beat 2", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 37), "Cardigan hem: beat 3", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 49), "4-beat idle loop", fill=BEAT_COLOR)


def draw_panel1_sharp_assessment(img, draw):
    """Panel 1: SHARP ASSESSMENT — 'The Engineer Look'. Chin down, one brow raised, 3-4° forward."""
    col = 1
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "SHARP ASSESSMENT", "chin down, one brow up — she sees it", beat_label="B2")

    fig_x = px + PANEL_W // 2
    fig_y = py + PANEL_H - 48

    (hcx, hcy, hr, bcx, bby, bw, bty, shy,
     cdn_bot, cdn_w,
     ll_cx, rl_cx) = draw_miri_figure(
        draw, fig_x, fig_y, head_r=22,
        body_lean=-3, head_tilt=-5,    # slight chin-down forward evaluating lean
        arm_right_angle=-22, arm_left_angle=-158,
        weight_back=False)
    draw = ImageDraw.Draw(img)

    # Ground line
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)], fill=ACCENT_DASH, width=1)

    # Single raised brow annotation (left brow = viewer's right, patient not skeptical)
    label_box(draw, hcx - hr - 62, hcy - hr - 6, "1 BROW UP",
              bg=(60, 90, 160), fg=(240, 248, 255))
    draw_arrow(draw, hcx - hr - 12, hcy - hr + 8, hcx - hr - 2, hcy - hr + 18,
               color=BEAT_COLOR, width=2, head=6)

    # Eyes-narrowed label (65% aperture)
    draw.text((hcx + hr + 4, hcy - hr + 4), "eyes 65%", fill=BEAT_COLOR)
    draw.text((hcx + hr + 4, hcy - hr + 16), "aperture", fill=BEAT_COLOR)
    draw.text((hcx + hr + 4, hcy - hr + 28), "(evaluating)", fill=BEAT_COLOR)

    # Forward lean annotation
    draw_arrow(draw, bcx + 4, bty + 8, bcx - 12, bty - 4,
               color=MOTION_ARROW, width=2, head=6)
    draw.text((px + 8, py + PANEL_H - 76), "-3° forward lean", fill=MOTION_ARROW)
    draw.text((px + 8, py + PANEL_H - 64), "(controlled — she IS)", fill=ACCENT_DASH)

    # Mouth neutral annotation (smile paused — computation mode)
    draw.text((hcx - hr - 62, hcy + int(hr * 0.40)), "mouth: paused", fill=ACCENT_DASH)
    draw.text((hcx - hr - 62, hcy + int(hr * 0.52)), "not a frown", fill=ACCENT_DASH)

    # Timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y),      "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Chin drops: beat 1", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Brow raises: beat 1.5", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 37), "Lean: beat 2 (not before)", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 49), "HOLD until she speaks", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 61), "No cardigan swing (still)", fill=ACCENT_DASH)


def draw_panel2_proud_quiet_joy(img, draw):
    """Panel 2: PROUD QUIET JOY — weight back, blush suppressed (Pride Override), full closed smile."""
    col = 2
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "PROUD QUIET JOY", "weight back — yields space to Luma", beat_label="B3")

    fig_x = px + PANEL_W // 2
    fig_y = py + PANEL_H - 48

    (hcx, hcy, hr, bcx, bby, bw, bty, shy,
     cdn_bot, cdn_w,
     ll_cx, rl_cx) = draw_miri_figure(
        draw, fig_x, fig_y, head_r=22,
        body_lean=2, head_tilt=0,      # slight weight-back (body eases backward)
        arm_right_angle=-22, arm_left_angle=-158,
        weight_back=True)
    draw = ImageDraw.Draw(img)

    # Ground line
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)], fill=ACCENT_DASH, width=1)

    # Pride Override annotation
    label_box(draw, px + 8, py + PANEL_H - 90, "PRIDE OVERRIDE",
              bg=(100, 60, 20), fg=(248, 230, 200))
    draw.text((px + 8, py + PANEL_H - 78), "blush fades: 25% -> 7.5%", fill=MOTION_ARROW)
    draw.text((px + 8, py + PANEL_H - 66), "when Luma excited", fill=MOTION_ARROW)

    # Weight-back annotation
    draw_arrow(draw, bcx - 4, bty + 8, bcx + 14, bty - 4,
               color=BEAT_COLOR, width=2, head=6)
    draw.text((hcx + hr + 4, bty + 4), "+2° back", fill=BEAT_COLOR)
    draw.text((hcx + hr + 4, bty + 16), "yields space", fill=BEAT_COLOR)

    # Shoulders drop annotation (1px — subtle)
    draw_arrow(draw, bcx - bw - 2, shy, bcx - bw - 2, shy + 6,
               color=MOTION_ARROW, width=2, head=5)
    draw.text((px + 8, shy - 14), "shoulders", fill=MOTION_ARROW)
    draw.text((px + 8, shy - 2), "drop 1px", fill=MOTION_ARROW)

    # Ghosted position (neutral — dashed construction)
    ghost_cx = bcx - 4   # ghost center slightly forward
    for yy in range(bty, bby, 8):
        draw.line([(ghost_cx - bw, yy), (ghost_cx - bw, yy + 4)], fill=ACCENT_DASH, width=1)
        draw.line([(ghost_cx + bw, yy), (ghost_cx + bw, yy + 4)], fill=ACCENT_DASH, width=1)
    draw.text((ghost_cx + bw + 4, bty + (bby - bty) // 2), "neutral pos", fill=ACCENT_DASH)

    # Timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y),      "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Weight eases back: 3 beats", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Shoulder drop: beat 2", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 37), "Pride Override: same frame", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 49), "  as Luma excited blush", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 61), "Returns: +8 frames after", fill=BEAT_COLOR)


def draw_panel3_patient_correction(img, draw):
    """Panel 3: PATIENT CORRECTION — two-finger raised hand, slight forward, one deliberate gesture."""
    col = 3
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "PATIENT CORRECTION", "two fingers — once; she will not repeat it", beat_label="B4")

    fig_x = px + PANEL_W // 2 + 4
    fig_y = py + PANEL_H - 48

    (hcx, hcy, hr, bcx, bby, bw, bty, shy,
     cdn_bot, cdn_w,
     ll_cx, rl_cx) = draw_miri_figure(
        draw, fig_x, fig_y, head_r=22,
        body_lean=-2, head_tilt=3,     # slight forward (bringing herself to the conversation)
        arm_right_angle=-22, arm_left_angle=-158,
        weight_back=False,
        hand_raised=True)
    draw = ImageDraw.Draw(img)

    # Ground line
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)], fill=ACCENT_DASH, width=1)

    # Two-finger label (engineering precision gesture)
    label_box(draw, px + 8, py + PANEL_H - 92, "PRECISION HAND",
              bg=(40, 70, 130), fg=(240, 248, 255))
    draw.text((px + 8, py + PANEL_H - 80), "index + middle only", fill=BEAT_COLOR)
    draw.text((px + 8, py + PANEL_H - 68), "engineering habit", fill=BEAT_COLOR)
    draw.text((px + 8, py + PANEL_H - 56), "ONCE — not repeated", fill=(220, 60, 20))

    # Head forward annotation
    draw_arrow(draw, hcx + hr + 2, hcy, hcx + hr + 18, hcy + 8,
               color=BEAT_COLOR, width=2, head=6)
    draw.text((hcx + hr + 20, hcy - 6), "+3° head", fill=BEAT_COLOR)
    draw.text((hcx + hr + 20, hcy + 6), "forward", fill=BEAT_COLOR)

    # Cardigan swing on arm raise
    draw_arrow(draw, bcx - cdn_w + 8, cdn_bot - 8,
               bcx - cdn_w - 12, cdn_bot + 10,
               color=MOTION_ARROW, width=2, head=6)
    draw.text((px + 8, cdn_bot + 12), "cardigan swings", fill=MOTION_ARROW)
    draw.text((px + 8, cdn_bot + 24), "+2.0 beats behind", fill=MOTION_ARROW)

    # Eyes: steady contact (she makes eye contact during correction)
    draw.text((hcx + hr + 20, hcy + 20), "eyes: direct", fill=BEAT_COLOR)
    draw.text((hcx + hr + 20, hcy + 32), "contact hold", fill=BEAT_COLOR)

    # Timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y),      "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Head forward: beat 1", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Arm raises: beat 1.5", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 37), "Hand: beat 2 (precise, still)", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 49), "Cardigan swing: beat 3.5", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 61), "Arm down: beat 5 (slow)", fill=BEAT_COLOR)


# ------------------------------------------------------------------ MAIN

def main():
    img = Image.new("RGB", (W, H), color=(238, 232, 222))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, W, PAD + 40], fill=LABEL_BG)
    draw.text((PAD, 8), "GRANDMA MIRI — Motion Spec Sheet v001", fill=LABEL_TEXT)
    draw.text((PAD, 22), "RYO HASEGAWA  |  Luma & the Glitchkin  |  C44", fill=(180, 165, 140))

    # Legend strip
    legend_x = W - 310
    draw.rectangle([legend_x - 6, 6, legend_x + 302, PAD + 36], fill=(70, 55, 42))
    draw.text((legend_x,       8), "->  Secondary motion (cardigan, hands)", fill=MOTION_ARROW)
    draw.text((legend_x,      20), "■  Timing beats", fill=BEAT_COLOR)
    draw.text((legend_x + 175, 8), "--  Construction/guide", fill=ACCENT_DASH)
    draw.text((legend_x + 175, 20), "o  CG / geometry", fill=(200, 200, 200))

    draw_panel0_warm_attention(img, draw)
    draw_panel1_sharp_assessment(img, draw)
    draw_panel2_proud_quiet_joy(img, draw)
    draw_panel3_patient_correction(img, draw)

    # enforce <=1280px
    img.thumbnail((1280, 1280), Image.LANCZOS)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "characters", "motion")
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_miri_motion.png")
    img.save(out_path)
    print(f"Saved: {out_path} ({img.width}x{img.height}px)")


if __name__ == "__main__":
    main()
