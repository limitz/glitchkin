# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_miri_motion_v002.py
Ryo Hasegawa / Cycle 47
Motion Spec Sheet v003 — GRANDMA MIRI (Miriam Okonkwo-Santos)
Beat arc: Emotional Warmth Pacing

COMPLETE REWORK (Takeshi C46 critique: 44/100 — weakest sheet, "poses labeled not performed").

Key changes from v002:
  - Figure scale: head_r 22→32 (45% larger, fills panel properly)
  - Weight distribution: asymmetric in EVERY panel (one foot bears more)
  - Shoulder-hip counterpose: visible rotation, hip shift, NOT just lean angle
  - Hands PERFORM: each panel has specific, purposeful hand positions
  - Spine participation: visible curve change across the arc
  - Fond Settle is EARNED — distinct from Observing Still

4 panels:
  B1: OBSERVING STILL   — weight right foot, left hand curled on armrest,
                           right hand loosely on lap. Contained but alert.
  B2: RECOGNITION       — weight shifts forward, hands lift from surfaces,
                           breath-catch visible in shoulder rise, spine engages
  B3: WARMTH BURST      — spine arches forward, arms open from SHOULDER rotation,
                           weight forward on balls of feet, SUNLIT_AMBER glow
  B4: FOND SETTLE       — weight settles back to right foot but NOT identical to B1,
                           arms cross loosely, head tilt remains, smile earned

Canvas: 1280x720 (<=1280 limit, native)
Output: output/characters/motion/LTG_CHAR_miri_motion_v002.png
"""

from PIL import Image, ImageDraw
import os
import math
import json

# --- Load config ---
_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "sheet_geometry_config.json")

def _load_panel_top_miri(default=54):
    """Load panel_top_abs for miri_v002 family from sheet_geometry_config.json."""
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
CG_MARKER       = (180,  60,  60)   # center-of-gravity marker color
WEIGHT_COLOR    = (100, 160,  80)   # weight distribution annotation

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


def draw_cg_marker(draw, cx, cy, label="CG", color=CG_MARKER):
    """Draw a center-of-gravity cross marker with label."""
    s = 5
    draw.line([(cx - s, cy), (cx + s, cy)], fill=color, width=2)
    draw.line([(cx, cy - s), (cx, cy + s)], fill=color, width=2)
    draw.text((cx + s + 2, cy - 5), label, fill=color)


def draw_weight_bar(draw, x, y, w, left_pct, color=WEIGHT_COLOR):
    """Draw a weight distribution bar. left_pct is 0.0-1.0 weight on left foot."""
    h = 6
    draw.rectangle([x, y, x + w, y + h], outline=color, width=1)
    split_x = x + int(w * left_pct)
    # Left side filled heavier
    if left_pct > 0.01:
        draw.rectangle([x + 1, y + 1, split_x, y + h - 1], fill=color)
    draw.text((x, y + h + 2), f"L:{int(left_pct*100)}%", fill=color)
    draw.text((x + w - 30, y + h + 2), f"R:{int((1-left_pct)*100)}%", fill=color)


# ------------------------------------------------------------------ cardigan knit lines

def draw_cardigan_knit(draw, cx, top_y, bot_y, half_w, head_r):
    """Draw cable-knit suggestion lines on cardigan body (3-4 vertical pairs)."""
    knit_spacing = max(14, int(head_r * 0.50))
    for offset in [-knit_spacing, 0, knit_spacing]:
        kx = cx + offset
        if kx - 3 > cx - half_w and kx + 3 < cx + half_w:
            for x_off in [-2, 2]:
                draw.line(
                    [(kx + x_off, top_y + 4), (kx + x_off, bot_y - 4)],
                    fill=CARDIGAN_SH, width=1
                )


# ------------------------------------------------------------------ character drawing

def draw_miri_figure(draw, ox, oy, head_r=32,
                     body_lean=0,
                     head_tilt=0,
                     hip_shift=0,
                     shoulder_drop_side=0,
                     left_foot_weight=0.5,
                     arm_left_mode="default",
                     arm_right_mode="default",
                     arm_left_angle=-170,
                     arm_right_angle=-10,
                     spine_curve=0,
                     eyes_crinkle=False,
                     smile_amount=0.5):
    """
    Draw Miri as a geometric construction figure — v003: PERFORMING POSES.

    ox, oy = center-bottom of figure.
    Miri proportions: 3.2 heads tall. head_r=32 (v003 — was 22 in v002).

    Key v003 changes:
      - hip_shift: px lateral shift of hip (positive = viewer right)
      - shoulder_drop_side: -1=left shoulder drops, +1=right drops, 0=level
      - left_foot_weight: 0.0-1.0 — weight on left foot (0.5=even, 0.7=left heavy)
      - arm modes: "default", "armrest", "lap_curl", "open_wide", "crossed", "lifting"
      - spine_curve: degrees of mid-spine convex forward curve (engagement signal)
      - eyes_crinkle: True = full crinkle closed (B3 warmth peak)
      - smile_amount: 0.0-1.0 mouth arc scale
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

    lean_off = int(math.tan(math.radians(body_lean)) * body_h)

    # --- FEET with weight distribution ---
    fc = int(leg_w * 0.85)
    # Weight foot plants firmly; light foot slightly lifted or angled
    lf_cx = ox - fc + hip_shift
    rf_cx = ox + fc + hip_shift
    fy = oy

    # Weighted foot is slightly wider/more grounded; light foot narrower
    l_weight = left_foot_weight
    r_weight = 1.0 - left_foot_weight
    lf_scale = 0.85 + 0.3 * l_weight  # 0.85 to 1.15
    rf_scale = 0.85 + 0.3 * r_weight
    lf_lift = int((1.0 - l_weight) * 4)  # light foot lifts 0-4px
    rf_lift = int((1.0 - r_weight) * 4)

    # Left foot
    lfw = int(foot_w * lf_scale)
    lf_top = fy - foot_h + lf_lift
    lf_bot = max(lf_top + 2, fy - lf_lift)
    draw.ellipse([lf_cx - lfw // 2, lf_top,
                  lf_cx + lfw // 2, lf_bot], fill=SLIPPER_BOT, outline=LINE_COLOR, width=lw)
    lf_up_top = lf_top
    lf_up_bot = max(lf_up_top + 2, lf_bot - 4)
    draw.ellipse([lf_cx - lfw // 2 + 2, lf_up_top,
                  lf_cx + lfw // 2 - 2, lf_up_bot], fill=SLIPPER_UP, outline=LINE_COLOR, width=lw)

    # Right foot
    rfw = int(foot_w * rf_scale)
    rf_top = fy - foot_h + rf_lift
    rf_bot = max(rf_top + 2, fy - rf_lift)
    draw.ellipse([rf_cx - rfw // 2, rf_top,
                  rf_cx + rfw // 2, rf_bot], fill=SLIPPER_BOT, outline=LINE_COLOR, width=lw)
    rf_up_top = rf_top
    rf_up_bot = max(rf_up_top + 2, rf_bot - 4)
    draw.ellipse([rf_cx - rfw // 2 + 2, rf_up_top,
                  rf_cx + rfw // 2 - 2, rf_up_bot], fill=SLIPPER_UP, outline=LINE_COLOR, width=lw)

    # --- LEGS with weight asymmetry ---
    leg_top_y = oy - leg_h
    ll_cx = ox - fc // 2 + hip_shift
    rl_cx = ox + fc // 2 + hip_shift
    top_lw = int(leg_w * 1.05)

    # Weighted leg is straighter; light leg has slight bend
    for side, cx_leg, w_frac in [(-1, ll_cx, l_weight), (1, rl_cx, r_weight)]:
        knee_offset = int((1.0 - w_frac) * 6 * side)  # light leg bends outward
        draw.polygon([
            cx_leg - top_lw // 2 + lean_off, leg_top_y,
            cx_leg + top_lw // 2 + lean_off, leg_top_y,
            cx_leg + leg_w // 2 + lean_off // 2 + knee_offset, oy - foot_h + 2,
            cx_leg - leg_w // 2 + lean_off // 2 + knee_offset, oy - foot_h + 2,
        ], fill=PANTS, outline=LINE_COLOR)
        # Leg center crease
        draw.line([(cx_leg + lean_off // 2, leg_top_y + 4),
                   (cx_leg + lean_off // 2 + knee_offset, oy - foot_h - 4)],
                  fill=PANTS_SH, width=1)

    # --- HIP REGION (visible weight shift) ---
    hip_y = leg_top_y + int(hr * 0.15)
    hip_tilt = int(hip_shift * 0.3)  # hip tilts with weight shift

    # --- TORSO with spine curve ---
    body_bot_y = oy - leg_h + int(hr * 0.52)
    body_top_y = body_bot_y - body_h
    body_cx    = ox + lean_off + hip_shift

    # Spine curve: mid-torso shifts forward/back
    spine_px = int(math.sin(math.radians(spine_curve)) * hr * 0.3)

    # Shoulder drop: one shoulder lower than the other
    sh_drop_px = int(abs(shoulder_drop_side) * hr * 0.12)
    left_sh_y_offset = sh_drop_px if shoulder_drop_side < 0 else 0
    right_sh_y_offset = sh_drop_px if shoulder_drop_side > 0 else 0

    cardigan_bot = body_bot_y + cardigan_hem_extra
    cardigan_w_bot = body_w + int(hr * 0.16)

    # Draw torso with slight spine curve at midpoint
    mid_y = (body_top_y + cardigan_bot) // 2
    # Upper torso
    draw.polygon([
        body_cx - body_w,        body_top_y,
        body_cx + body_w,        body_top_y,
        body_cx + body_w + int(hr * 0.06) + spine_px,  mid_y,
        body_cx - body_w + int(hr * 0.06) + spine_px,  mid_y,
    ], fill=CARDIGAN_BASE, outline=LINE_COLOR)
    # Lower torso/cardigan
    draw.polygon([
        body_cx - body_w + int(hr * 0.06) + spine_px,  mid_y,
        body_cx + body_w + int(hr * 0.06) + spine_px,  mid_y,
        body_cx + cardigan_w_bot, cardigan_bot,
        body_cx - cardigan_w_bot, cardigan_bot,
    ], fill=CARDIGAN_BASE, outline=LINE_COLOR)

    draw_cardigan_knit(draw, body_cx + spine_px // 2, body_top_y, cardigan_bot, body_w, head_r=hr)

    # Buttons
    btn_r = max(3, int(hr * 0.12))
    btn_spacing = (cardigan_bot - body_top_y) // 5
    for i in range(1, 5):
        bx = body_cx + int(spine_px * (i / 5))
        by = body_top_y + i * btn_spacing
        draw.ellipse([bx - btn_r, by - btn_r, bx + btn_r, by + btn_r],
                     fill=CARDIGAN_BTN, outline=LINE_COLOR, width=1)

    # V-neck
    v_w = int(body_w * 0.35)
    v_depth = int(body_h * 0.30)
    draw.polygon([
        body_cx, body_top_y + v_depth,
        body_cx - v_w, body_top_y + 2,
        body_cx + v_w, body_top_y + 2,
    ], fill=EYE_WHITE)

    # Cardigan side seams
    for side in [-1, 1]:
        draw.line([(body_cx + side * (body_w - 4), body_top_y + 6),
                   (body_cx + side * (cardigan_w_bot - 4), cardigan_bot - 6)],
                  fill=CARDIGAN_SH, width=2)

    # Pockets
    pkt_top = body_bot_y - int(hr * 0.25)
    pkt_bot = cardigan_bot - 8
    pkt_w   = int(body_w * 0.55)
    for side in [-1, 1]:
        pkt_cx = body_cx + side * int(body_w * 0.52) + spine_px // 2
        draw.rectangle([pkt_cx - pkt_w // 2, pkt_top,
                        pkt_cx + pkt_w // 2, pkt_bot],
                       outline=CARDIGAN_SH, width=2)

    # --- SHOULDER MARKERS with drop ---
    shoulder_y_base = body_top_y + int(hr * 0.14)
    l_shoulder_x = body_cx - body_w
    r_shoulder_x = body_cx + body_w
    l_shoulder_y = shoulder_y_base + left_sh_y_offset
    r_shoulder_y = shoulder_y_base + right_sh_y_offset
    shoulder_r = 5
    for sx, sy in [(l_shoulder_x, l_shoulder_y), (r_shoulder_x, r_shoulder_y)]:
        draw.ellipse([sx - shoulder_r, sy - shoulder_r,
                      sx + shoulder_r, sy + shoulder_r],
                     fill=ACCENT_DASH, outline=LINE_COLOR, width=1)

    # --- ARMS based on mode ---
    arm_h  = int(hr * 1.40)
    arm_w  = int(hr * 0.30)
    hand_r = int(hr * 0.22)

    def _draw_arm(start_x, start_y, angle_rad, fill_col=CARDIGAN_BASE):
        """Draw a single arm from shoulder to hand."""
        end_x = start_x + int(arm_h * math.cos(angle_rad))
        end_y = start_y - int(arm_h * math.sin(angle_rad))
        # Elbow at midpoint with slight bend
        mid_x = (start_x + end_x) // 2
        mid_y = (start_y + end_y) // 2
        # Upper arm
        draw.polygon([
            start_x - arm_w // 2, start_y,
            start_x + arm_w // 2, start_y,
            mid_x + arm_w // 3, mid_y,
            mid_x - arm_w // 3, mid_y,
        ], fill=fill_col, outline=LINE_COLOR)
        # Forearm
        draw.polygon([
            mid_x - arm_w // 3, mid_y,
            mid_x + arm_w // 3, mid_y,
            end_x + arm_w // 4, end_y,
            end_x - arm_w // 4, end_y,
        ], fill=fill_col, outline=LINE_COLOR)
        # Hand
        draw.ellipse([end_x - hand_r, end_y - hand_r // 2,
                      end_x + hand_r, end_y + hand_r],
                     fill=SKIN, outline=LINE_COLOR, width=2)
        return end_x, end_y

    def _draw_arm_crossed(start_x, start_y, side, body_cx_ref):
        """Arm crossed: forearm wraps across body."""
        # Upper arm goes down and slightly in
        mid_x = start_x + side * int(arm_h * 0.15)
        mid_y = start_y + int(arm_h * 0.45)
        draw.polygon([
            start_x - arm_w // 2, start_y,
            start_x + arm_w // 2, start_y,
            mid_x + arm_w // 3, mid_y,
            mid_x - arm_w // 3, mid_y,
        ], fill=CARDIGAN_BASE, outline=LINE_COLOR)
        # Forearm crosses to opposite side
        end_x = body_cx_ref - side * int(body_w * 0.60)
        end_y = mid_y + int(arm_h * 0.10)
        draw.polygon([
            mid_x - arm_w // 3, mid_y,
            mid_x + arm_w // 3, mid_y,
            end_x + arm_w // 4, end_y,
            end_x - arm_w // 4, end_y,
        ], fill=CARDIGAN_BASE, outline=LINE_COLOR)
        draw.ellipse([end_x - hand_r, end_y - hand_r // 2,
                      end_x + hand_r, end_y + hand_r],
                     fill=SKIN, outline=LINE_COLOR, width=2)
        return end_x, end_y

    def _draw_arm_lifting(start_x, start_y, side):
        """Arm lifting from surface — hands rising, fingers loosening."""
        # Arm going slightly up and out — mid-gesture of leaving armrest
        mid_x = start_x + side * int(arm_h * 0.25)
        mid_y = start_y + int(arm_h * 0.30)
        draw.polygon([
            start_x - arm_w // 2, start_y,
            start_x + arm_w // 2, start_y,
            mid_x + arm_w // 3, mid_y,
            mid_x - arm_w // 3, mid_y,
        ], fill=CARDIGAN_BASE, outline=LINE_COLOR)
        # Forearm rises slightly — hand hovering above where it was
        end_x = mid_x + side * int(arm_h * 0.12)
        end_y = mid_y - int(arm_h * 0.08)
        draw.polygon([
            mid_x - arm_w // 3, mid_y,
            mid_x + arm_w // 3, mid_y,
            end_x + arm_w // 4, end_y,
            end_x - arm_w // 4, end_y,
        ], fill=CARDIGAN_BASE, outline=LINE_COLOR)
        # Hand with fingers spread (loosening)
        draw.ellipse([end_x - hand_r, end_y - hand_r,
                      end_x + hand_r, end_y + hand_r // 2],
                     fill=SKIN, outline=LINE_COLOR, width=2)
        # Finger lines radiating (loosening gesture)
        for ang_off in [-0.3, 0.0, 0.3]:
            fx = end_x + int(hand_r * 1.2 * math.cos(ang_off + (0 if side > 0 else math.pi)))
            fy = end_y - int(hand_r * 0.6 * math.sin(ang_off + 0.5))
            draw.line([(end_x, end_y - 2), (fx, fy)], fill=SKIN_HL, width=1)
        return end_x, end_y

    # Right arm (viewer's left side — start_x = l_shoulder_x)
    r_hand_x, r_hand_y = 0, 0
    l_hand_x, l_hand_y = 0, 0

    if arm_right_mode == "armrest":
        # Arm resting on armrest — hand curled, arm bent at elbow, forearm on surface
        ang = math.radians(arm_right_angle)
        r_hand_x, r_hand_y = _draw_arm(l_shoulder_x, l_shoulder_y, ang)
        # Curled fingers on armrest
        for i in range(3):
            cx_f = r_hand_x - 2 + i * 4
            draw.arc([cx_f - 3, r_hand_y - 2, cx_f + 3, r_hand_y + 5],
                     start=180, end=360, fill=SKIN_SH, width=1)
    elif arm_right_mode == "lifting":
        r_hand_x, r_hand_y = _draw_arm_lifting(l_shoulder_x, l_shoulder_y, -1)
    elif arm_right_mode == "open_wide":
        ang = math.radians(-120)
        r_hand_x, r_hand_y = _draw_arm(l_shoulder_x, l_shoulder_y, ang)
    elif arm_right_mode == "crossed":
        r_hand_x, r_hand_y = _draw_arm_crossed(l_shoulder_x, l_shoulder_y, -1, body_cx)
    else:
        ang = math.radians(arm_right_angle)
        r_hand_x, r_hand_y = _draw_arm(l_shoulder_x, l_shoulder_y, ang)

    # Left arm (viewer's right side — start_x = r_shoulder_x)
    if arm_left_mode == "lap_curl":
        # Hand loosely on lap — forearm angled inward/down
        ang = math.radians(arm_left_angle)
        l_hand_x, l_hand_y = _draw_arm(r_shoulder_x, r_shoulder_y, ang)
    elif arm_left_mode == "lifting":
        l_hand_x, l_hand_y = _draw_arm_lifting(r_shoulder_x, r_shoulder_y, 1)
    elif arm_left_mode == "open_wide":
        ang = math.radians(-60)
        l_hand_x, l_hand_y = _draw_arm(r_shoulder_x, r_shoulder_y, ang)
    elif arm_left_mode == "crossed":
        l_hand_x, l_hand_y = _draw_arm_crossed(r_shoulder_x, r_shoulder_y, 1, body_cx)
    else:
        ang = math.radians(arm_left_angle)
        l_hand_x, l_hand_y = _draw_arm(r_shoulder_x, r_shoulder_y, ang)

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
    # Forehead highlight
    hl_r = max(5, int(hr * 0.20))
    draw.ellipse([head_cx - hl_r // 2, head_top + int(hr * 0.26),
                  head_cx + hl_r // 2, head_top + int(hr * 0.26) + hl_r // 2],
                 fill=SKIN_HL)

    # --- HAIR (silver bun) ---
    bun_cy  = head_top - int(hr * 0.16)
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
    # Wisps
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
        draw.ellipse([blush_cx - int(hr * 0.20), face_cy + int(hr * 0.02),
                      blush_cx + int(hr * 0.20), face_cy + int(hr * 0.24)],
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

    if eyes_crinkle:
        # Full crinkle: eyes nearly shut, crinkle lines above and below
        for side in [-1, 1]:
            ex = head_cx + side * eye_sep
            ey = face_cy - int(hr * 0.10)
            draw.arc([ex - eye_rx, ey - 2, ex + eye_rx, ey + 4],
                     start=200, end=340, fill=LINE_COLOR, width=3)
            # Crinkle above
            draw.arc([ex - int(eye_rx * 1.1), ey - int(hr * 0.12),
                      ex + int(eye_rx * 1.1), ey + 2],
                     start=185, end=355, fill=CRINKLE_COLOR, width=1)
            # Crinkle below
            draw.arc([ex - int(eye_rx * 0.8), ey + 1,
                      ex + int(eye_rx * 0.8), ey + int(hr * 0.08)],
                     start=10, end=170, fill=CRINKLE_COLOR, width=1)
            # Extra crow's feet
            cw_x = ex + side * (eye_rx + 3)
            for dy in [-3, 0, 3]:
                draw.line([(cw_x, ey + dy), (cw_x + side * 5, ey + dy - 2)],
                          fill=CRINKLE_COLOR, width=1)
    else:
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
            # Upper eyelid (heavier than Luma's — aged, calm)
            draw.arc([ex - eye_rx, ey - eye_ry, ex + eye_rx, ey + int(eye_ry * 0.4)],
                     start=200, end=340, fill=LINE_COLOR, width=3)
            # Crow's feet (always present)
            cw_x = ex + side * (eye_rx + 2)
            draw.arc([cw_x - 5, ey - 3, cw_x + 5, ey + 6],
                     start=0 if side == 1 else 180, end=90 if side == 1 else 270,
                     fill=LINE_COLOR, width=1)

    # Nose
    draw.arc([head_cx - int(hr * 0.10), face_cy + int(hr * 0.14),
              head_cx + int(hr * 0.10), face_cy + int(hr * 0.30)],
             start=130, end=310, fill=LINE_COLOR, width=3)

    # Mouth with variable smile
    mouth_top = face_cy + int(hr * 0.28)
    mouth_bot = mouth_top + int(hr * 0.26 * smile_amount)
    mouth_hw = int(hw * 0.30 * (0.8 + 0.4 * smile_amount))
    draw.arc([head_cx - mouth_hw, mouth_top,
              head_cx + mouth_hw, mouth_bot],
             start=10, end=170, fill=LINE_COLOR, width=3)

    # Smile lines (always present, deepen with smile_amount)
    sl_w = max(1, int(2 * smile_amount + 0.5))
    for side in [-1, 1]:
        smx = head_cx + side * int(hw * 0.26)
        draw.arc([smx - 4, face_cy + int(hr * 0.25),
                  smx + 4, face_cy + int(hr * 0.56)],
                 start=200 if side == -1 else 340, end=320 if side == -1 else 100,
                 fill=LINE_COLOR, width=sl_w)

    return {
        "head_cx": head_cx, "head_cy": head_cy, "head_top": head_top, "hr": hr,
        "body_cx": body_cx, "body_bot_y": body_bot_y, "body_w": body_w,
        "body_top_y": body_top_y,
        "l_shoulder_x": l_shoulder_x, "l_shoulder_y": l_shoulder_y,
        "r_shoulder_x": r_shoulder_x, "r_shoulder_y": r_shoulder_y,
        "cardigan_bot": cardigan_bot, "cardigan_w_bot": cardigan_w_bot,
        "ll_cx": ll_cx, "rl_cx": rl_cx,
        "lf_cx": lf_cx, "rf_cx": rf_cx, "fy": fy,
        "r_hand_x": r_hand_x, "r_hand_y": r_hand_y,
        "l_hand_x": l_hand_x, "l_hand_y": l_hand_y,
    }


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
    """Panel 0: OBSERVING STILL — weight on RIGHT foot, left hand curled on armrest,
    right hand loosely on lap. Contained but present. Not default — HELD stillness."""
    col = 0
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "OBSERVING STILL",
                  "weight R, armrest curl, held attention", beat_label="B1")

    fig_x = px + PANEL_W // 2
    fig_y = py + PANEL_H - 40

    fig = draw_miri_figure(
        draw, fig_x, fig_y, head_r=32,
        body_lean=0, head_tilt=-2,   # very slight head tilt — she's watching
        hip_shift=4,                 # weight shifted right
        shoulder_drop_side=-1,       # left shoulder drops slightly (relaxed side)
        left_foot_weight=0.30,       # 30% left, 70% right — RIGHT is planted
        arm_right_mode="armrest",    # right arm (viewer left): curled on armrest
        arm_right_angle=-40,
        arm_left_mode="lap_curl",    # left arm (viewer right): loosely in lap
        arm_left_angle=-145,
        spine_curve=0,               # erect — stillness is effort
        smile_amount=0.3)            # neutral-warm resting face
    draw = ImageDraw.Draw(img)

    # Ground line
    draw.line([(px + 10, fig_y), (px + PANEL_W - 10, fig_y)], fill=ACCENT_DASH, width=1)

    # CG marker — offset right (matches weight)
    cg_x = fig["body_cx"] + 3
    cg_y = (fig["body_top_y"] + fig["body_bot_y"]) // 2
    draw_cg_marker(draw, cg_x, cg_y, "CG (R)")

    # Weight distribution bar
    draw_weight_bar(draw, px + 8, fig_y + 4, 80, 0.30)

    # Shoulder drop annotation
    draw_arrow(draw, fig["l_shoulder_x"] - 2, fig["l_shoulder_y"],
               fig["l_shoulder_x"] - 16, fig["l_shoulder_y"] + 8,
               color=BEAT_COLOR, width=1, head=5)
    draw.text((px + 8, fig["l_shoulder_y"] - 4), "L drop", fill=BEAT_COLOR)

    # "HELD" stillness annotation — this is not relaxation, it is attention
    label_box(draw, px + PANEL_W - 88, py + 6, "HELD STILL",
              bg=(40, 30, 20), fg=(200, 190, 170))
    draw.text((px + PANEL_W - 88, py + 26), "NOT default —", fill=ACCENT_DASH)
    draw.text((px + PANEL_W - 88, py + 38), "effort of stillness", fill=ACCENT_DASH)

    # Gaze direction
    hx, hy = fig["head_cx"], fig["head_cy"]
    hr = fig["hr"]
    draw_arrow(draw, hx + hr + 2, hy, hx + hr + 18, hy + 3,
               color=BEAT_COLOR, width=2, head=5)
    draw.text((hx + hr + 20, hy - 6), "watching", fill=BEAT_COLOR)

    # Armrest hand detail annotation
    draw.text((px + 6, fig["r_hand_y"] - 12), "fingers curled", fill=MOTION_ARROW)
    draw.text((px + 6, fig["r_hand_y"] + 2), "on armrest", fill=MOTION_ARROW)

    # Timing
    draw.text((px + 8, py + 56), "Hold: indefinite", fill=BEAT_COLOR)
    draw.text((px + 8, py + 68), "Blink: slow (calm)", fill=BEAT_COLOR)
    draw.text((px + 8, py + 80), "Breath: shoulder +0.5px", fill=MOTION_ARROW)
    draw.text((px + 8, py + 92), "Cardigan: motionless", fill=ACCENT_DASH)


def draw_panel1_recognition(img, draw):
    """Panel 1: RECOGNITION — weight shifts forward, breath catch visible in shoulder rise,
    hands LIFT from surfaces, spine begins to engage. The body CHANGES."""
    col = 1
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "RECOGNITION",
                  "weight fwd, hands lift, breath catch", beat_label="B2")

    fig_x = px + PANEL_W // 2
    fig_y = py + PANEL_H - 40

    fig = draw_miri_figure(
        draw, fig_x, fig_y, head_r=32,
        body_lean=-3,                # forward lean begins — she's moving toward
        head_tilt=-4,                # head tilt deepens — she sees it
        hip_shift=2,                 # weight shifting forward from right
        shoulder_drop_side=0,        # shoulders RISE (breath catch) — both up
        left_foot_weight=0.45,       # weight equalizing — about to shift forward
        arm_right_mode="lifting",    # right hand lifting OFF armrest
        arm_left_mode="lifting",     # left hand lifting FROM lap
        spine_curve=6,               # spine begins forward engagement curve
        smile_amount=0.35)           # mouth hasn't changed yet — recognition is in body first
    draw = ImageDraw.Draw(img)

    # Ground line
    draw.line([(px + 10, fig_y), (px + PANEL_W - 10, fig_y)], fill=ACCENT_DASH, width=1)

    # CG marker — shifted forward
    cg_x = fig["body_cx"] - 2
    cg_y = (fig["body_top_y"] + fig["body_bot_y"]) // 2
    draw_cg_marker(draw, cg_x, cg_y, "CG (fwd)")

    # Weight distribution
    draw_weight_bar(draw, px + 8, fig_y + 4, 80, 0.45)

    # Forward lean annotation
    draw_arrow(draw, fig["body_cx"] - 4, fig["body_top_y"] + 10,
               fig["body_cx"] - 18, fig["body_top_y"] - 4,
               color=MOTION_ARROW, width=2, head=6)
    draw.text((px + 6, py + PANEL_H - 92), "-3\u00b0 lean begins", fill=MOTION_ARROW)
    draw.text((px + 6, py + PANEL_H - 80), "beat 1.5 (head first)", fill=BEAT_COLOR)

    # Head tilt deepens
    hx, hy = fig["head_cx"], fig["head_cy"]
    hr = fig["hr"]
    draw_arrow(draw, hx - hr - 2, hy - int(hr * 0.5),
               hx - hr - 16, hy - int(hr * 0.65),
               color=BEAT_COLOR, width=2, head=5)
    draw.text((px + 6, hy - int(hr * 0.75)), "-4\u00b0 head", fill=BEAT_COLOR)

    # Breath catch annotation — shoulders rise
    draw.text((px + PANEL_W - 84, py + 6), "BREATH CATCH", fill=MOTION_ARROW)
    draw.text((px + PANEL_W - 84, py + 18), "shoulders rise", fill=MOTION_ARROW)
    draw.text((px + PANEL_W - 84, py + 30), "+3px simultaneous", fill=MOTION_ARROW)

    # Hands lifting annotation
    draw.text((px + 6, fig["r_hand_y"] - 18), "hands LIFT", fill=MOTION_ARROW)
    draw.text((px + 6, fig["r_hand_y"] - 6), "fingers loosen", fill=MOTION_ARROW)

    # Spine engagement annotation
    spine_y = (fig["body_top_y"] + fig["body_bot_y"]) // 2
    draw.text((fig["body_cx"] + fig["body_w"] + 4, spine_y - 4),
              "spine 6\u00b0", fill=ACCENT_DASH)
    draw.text((fig["body_cx"] + fig["body_w"] + 4, spine_y + 8),
              "engages", fill=ACCENT_DASH)

    # Cardigan lag
    draw_arrow(draw, fig["body_cx"] + fig["cardigan_w_bot"] - 4,
               fig["cardigan_bot"] - 8,
               fig["body_cx"] + fig["cardigan_w_bot"] + 10,
               fig["cardigan_bot"] + 6,
               color=MOTION_ARROW, width=2, head=5)
    draw.text((fig["body_cx"] + fig["cardigan_w_bot"] + 12,
               fig["cardigan_bot"] - 6), "lag +2.0b", fill=MOTION_ARROW)

    # Timing
    draw.text((px + 8, py + 44), "Head tilt: beat 1", fill=BEAT_COLOR)
    draw.text((px + 8, py + 56), "Body lean: beat 1.5", fill=BEAT_COLOR)
    draw.text((px + 8, py + 68), "Hands lift: beat 2", fill=MOTION_ARROW)
    draw.text((px + 8, py + 80), "Cardigan: beat 3.5", fill=MOTION_ARROW)
    draw.text((px + 8, py + 92), "Eyes widen: beat 1", fill=BEAT_COLOR)


def draw_panel2_warmth_burst(img, draw):
    """Panel 2: WARMTH BURST — full body, spine arches forward, arms open from SHOULDER
    rotation, weight on balls of feet, SUNLIT_AMBER glow. SPINE PARTICIPATES."""
    col = 2
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "WARMTH BURST",
                  "spine forward, arms from shoulders, glow", beat_label="B3")

    fig_x = px + PANEL_W // 2
    fig_y = py + PANEL_H - 40

    # SUNLIT_AMBER radial glow BEHIND figure — warmth radiates outward
    glow_cx = fig_x
    glow_cy = fig_y - 110  # chest level for larger figure
    for radius, color in [
        (95, SUNLIT_PALE),
        (130, (240, 200, 130)),
        (160, (232, 180, 105)),
    ]:
        draw.ellipse([glow_cx - radius, glow_cy - radius,
                      glow_cx + radius, glow_cy + radius],
                     fill=color, outline=None)
    # Re-draw panel border on top of glow
    draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], fill=None, outline=PANEL_BORDER, width=1)

    fig = draw_miri_figure(
        draw, fig_x, fig_y, head_r=32,
        body_lean=-2,                # slight forward lean — spine is the main story
        head_tilt=0,                 # head centered — she gives openly
        hip_shift=0,                 # weight centered and forward
        shoulder_drop_side=0,        # both shoulders BACK and DOWN (chest opens)
        left_foot_weight=0.50,       # even weight — balls of both feet
        arm_right_mode="open_wide",  # arms open WIDE from shoulder rotation
        arm_left_mode="open_wide",
        spine_curve=14,              # STRONG forward spine curve — chest opens
        eyes_crinkle=True,           # eyes crinkle fully closed at peak
        smile_amount=1.0)            # full smile
    draw = ImageDraw.Draw(img)

    # Ground line
    draw.line([(px + 10, fig_y), (px + PANEL_W - 10, fig_y)], fill=ACCENT_DASH, width=1)

    # CG marker — forward
    cg_x = fig["body_cx"] - 4
    cg_y = (fig["body_top_y"] + fig["body_bot_y"]) // 2
    draw_cg_marker(draw, cg_x, cg_y, "CG fwd")

    # Glow annotation
    label_box(draw, px + 6, py + 6, "SUNLIT_AMBER",
              bg=(140, 80, 20), fg=(248, 230, 180))
    draw.text((px + 6, py + 28), "212,146,58", fill=SUNLIT_AMBER)
    draw.text((px + 6, py + 40), "Real World ONLY", fill=ACCENT_DASH)

    # Spine annotation — THE key change
    spine_y = (fig["body_top_y"] + fig["body_bot_y"]) // 2
    draw_arrow(draw, fig["body_cx"] + fig["body_w"] + 6, spine_y,
               fig["body_cx"] + fig["body_w"] + 20, spine_y - 8,
               color=MOTION_ARROW, width=2, head=6)
    draw.text((fig["body_cx"] + fig["body_w"] + 8, spine_y - 20),
              "spine 14\u00b0 fwd", fill=MOTION_ARROW)
    draw.text((fig["body_cx"] + fig["body_w"] + 8, spine_y - 8),
              "CHEST OPENS", fill=MOTION_ARROW)

    # Shoulder rotation annotation
    draw.text((px + 6, fig["l_shoulder_y"] - 12), "shoulders ROTATE", fill=MOTION_ARROW)
    draw.text((px + 6, fig["l_shoulder_y"]), "back + down", fill=MOTION_ARROW)
    draw.text((px + 6, fig["l_shoulder_y"] + 12), "arms follow", fill=MOTION_ARROW)

    # Eye crinkle annotation
    hx, hy = fig["head_cx"], fig["head_cy"]
    hr = fig["hr"]
    draw.text((hx + hr + 4, hy - int(hr * 0.35)), "eyes crinkle", fill=CRINKLE_COLOR)
    draw.text((hx + hr + 4, hy - int(hr * 0.23)), "fully closed", fill=CRINKLE_COLOR)
    draw.text((hx + hr + 4, hy - int(hr * 0.11)), "at PEAK", fill=CRINKLE_COLOR)

    # Cardigan hem flutter
    draw_arrow(draw, fig["body_cx"], fig["cardigan_bot"] - 4,
               fig["body_cx"] - 8, fig["cardigan_bot"] + 10,
               color=MOTION_ARROW, width=2, head=5)

    # Timing
    ty = py + 54
    draw.text((px + 8, ty), "Arms spread: beat 1", fill=BEAT_COLOR)
    draw.text((px + 8, ty + 12), "Eyes crinkle: beat 1.5", fill=CRINKLE_COLOR)
    draw.text((px + 8, ty + 24), "Glow peak: beat 2", fill=(180, 120, 40))
    draw.text((px + 8, ty + 36), "Cardigan: beat 3", fill=MOTION_ARROW)
    draw.text((px + 8, ty + 48), "HOLD: 4-6 frames", fill=BEAT_COLOR)


def draw_panel3_fond_settle(img, draw):
    """Panel 3: FOND SETTLE — NOT a return to B1. Arms cross loosely (different from B1
    armrest+lap). Head tilt lingers. Smile earned. Weight settles back but stance is wider.
    This is a person who just GAVE something and is landing from it."""
    col = 3
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "FOND SETTLE",
                  "earned rest, NOT B1 — arms crossed, smile stays", beat_label="B4")

    fig_x = px + PANEL_W // 2
    fig_y = py + PANEL_H - 40

    fig = draw_miri_figure(
        draw, fig_x, fig_y, head_r=32,
        body_lean=1,                 # slight BACK lean — settling from forward
        head_tilt=-2,                # head tilt LINGERS from B2 — warmth remains
        hip_shift=3,                 # weight settles right again but not as far as B1
        shoulder_drop_side=1,        # RIGHT shoulder drops (opposite from B1)
        left_foot_weight=0.35,       # similar to B1 but not identical
        arm_right_mode="crossed",    # arms loosely crossed — different from B1 armrest
        arm_left_mode="crossed",
        spine_curve=-2,              # slight back curve — settling
        smile_amount=0.7)            # smile EARNED — bigger than B1's 0.3
    draw = ImageDraw.Draw(img)

    # Ground line
    draw.line([(px + 10, fig_y), (px + PANEL_W - 10, fig_y)], fill=ACCENT_DASH, width=1)

    # CG marker — back from B3
    cg_x = fig["body_cx"] + 2
    cg_y = (fig["body_top_y"] + fig["body_bot_y"]) // 2
    draw_cg_marker(draw, cg_x, cg_y, "CG (back)")

    # Weight distribution
    draw_weight_bar(draw, px + 8, fig_y + 4, 80, 0.35)

    # Ghosted B3 open-arm position (where arms were — the arc they traveled)
    ghost_color = (200, 190, 175, 128)  # translucent accent
    ghost_arm_h = int(32 * 1.40)
    for side, ang_deg in [(-1, -120), (1, -60)]:
        ang = math.radians(ang_deg)
        sh_x = fig["l_shoulder_x"] if side == -1 else fig["r_shoulder_x"]
        sh_y = fig["l_shoulder_y"] if side == -1 else fig["r_shoulder_y"]
        end_x = sh_x + int(ghost_arm_h * math.cos(ang))
        end_y = sh_y - int(ghost_arm_h * math.sin(ang))
        for t in range(0, ghost_arm_h, 8):
            frac = t / ghost_arm_h
            gx = int(sh_x + frac * (end_x - sh_x))
            gy = int(sh_y + frac * (end_y - sh_y))
            draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=ACCENT_DASH)
    draw.text((px + PANEL_W - 58, fig["l_shoulder_y"] - 18), "B3 pos", fill=ACCENT_DASH)

    # "NOT B1" annotation — key distinction
    label_box(draw, px + PANEL_W - 64, py + 6, "NOT B1",
              bg=(120, 40, 30), fg=(248, 230, 200))
    draw.text((px + PANEL_W - 88, py + 28), "arms: crossed", fill=ACCENT_DASH)
    draw.text((px + PANEL_W - 88, py + 40), "  (B1 = armrest+lap)", fill=ACCENT_DASH)
    draw.text((px + PANEL_W - 88, py + 52), "smile: 0.7", fill=ACCENT_DASH)
    draw.text((px + PANEL_W - 88, py + 64), "  (B1 = 0.3)", fill=ACCENT_DASH)
    draw.text((px + PANEL_W - 88, py + 76), "shoulder: R drops", fill=ACCENT_DASH)
    draw.text((px + PANEL_W - 88, py + 88), "  (B1 = L drops)", fill=ACCENT_DASH)

    # Smile lingering annotation
    hx, hy = fig["head_cx"], fig["head_cy"]
    hr = fig["hr"]
    draw.text((hx + hr + 4, hy + int(hr * 0.25)), "smile EARNED", fill=BEAT_COLOR)
    draw.text((hx + hr + 4, hy + int(hr * 0.37)), "bigger than B1", fill=BEAT_COLOR)

    # Blush sustain
    draw.text((hx - hr - 68, hy + int(hr * 0.05)), "blush sustained", fill=CHEEK_BLUSH)
    draw.text((hx - hr - 68, hy + int(hr * 0.17)), "from B3 peak", fill=CHEEK_BLUSH)

    # Cardigan settling
    draw_arrow(draw, fig["body_cx"] + fig["cardigan_w_bot"] - 4,
               fig["cardigan_bot"] - 6,
               fig["body_cx"] + fig["cardigan_w_bot"] + 10,
               fig["cardigan_bot"] + 4,
               color=MOTION_ARROW, width=2, head=5)
    draw.text((fig["body_cx"] + fig["cardigan_w_bot"] + 12,
               fig["cardigan_bot"] - 8), "settles", fill=MOTION_ARROW)
    draw.text((fig["body_cx"] + fig["cardigan_w_bot"] + 12,
               fig["cardigan_bot"] + 4), "last +2.0b", fill=MOTION_ARROW)

    # Timing
    draw.text((px + 8, py + 100), "Arms lower: 4 beats", fill=BEAT_COLOR)
    draw.text((px + 8, py + 112), "Eyes reopen: beat 1", fill=BEAT_COLOR)
    draw.text((px + 8, py + 124), "Smile: held +6 fr", fill=MOTION_ARROW)
    draw.text((px + 8, py + 136), "Blush fades: beat 8+", fill=MOTION_ARROW)
    draw.text((px + 8, py + 148), "Settle != B1", fill=ACCENT_DASH)


# ------------------------------------------------------------------ MAIN

def main():
    img = Image.new("RGB", (W, H), color=(242, 236, 226))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, W, PAD + 40], fill=LABEL_BG)
    draw.text((PAD, 8),
              "GRANDMA MIRI \u2014 Motion Spec Sheet v003  |  Emotional Warmth Pacing",
              fill=LABEL_TEXT)
    draw.text((PAD, 22),
              "RYO HASEGAWA  |  Luma & the Glitchkin  |  C47  |  "
              "STILL\u2192RECOGNITION\u2192WARMTH BURST\u2192FOND SETTLE",
              fill=(180, 165, 140))

    # Legend strip
    legend_x = W - 340
    draw.rectangle([legend_x - 6, 6, legend_x + 332, PAD + 36], fill=(70, 55, 42))
    draw.text((legend_x,       8), "->  Secondary motion", fill=MOTION_ARROW)
    draw.text((legend_x,      20), "X   CG marker", fill=CG_MARKER)
    draw.text((legend_x + 130,  8), "[]  Weight bar", fill=WEIGHT_COLOR)
    draw.text((legend_x + 130, 20), "--  Construction", fill=ACCENT_DASH)
    draw.text((legend_x + 250,  8), "B#  Timing", fill=BEAT_COLOR)
    draw.text((legend_x + 250, 20), "o   SUNLIT_AMBER", fill=SUNLIT_AMBER)

    draw_panel0_observing_still(img, draw)
    draw_panel1_recognition(img, draw)
    draw_panel2_warmth_burst(img, draw)
    draw_panel3_fond_settle(img, draw)

    # Save — native 1280x720
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
