# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_luma_gesture_prototype.py
Ryo Hasegawa / Cycle 50

Gesture-first vs rectangle-first construction comparison for Luma SURPRISED.
Demonstrates why gesture line must come BEFORE body shapes.

Output: output/characters/motion/LTG_CHAR_luma_gesture_prototype.png
Canvas: 1280x720 (within limit)

Left panel:  OLD approach — rectangle body, symmetric legs, arms bolted on
Right panel: NEW approach — gesture line drawn first, body built around it
"""

import os
import sys
import math

from PIL import Image, ImageDraw, ImageFont
from LTG_TOOL_curve_utils import cubic_bezier_single as _cu_single, draw_bezier_polyline as _cu_draw_bezier

# --- path setup ---
_TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_TOOL_DIR, "..", ".."))
_OUTPUT_DIR = os.path.join(_PROJECT_ROOT, "output", "characters", "motion")
os.makedirs(_OUTPUT_DIR, exist_ok=True)

# --- COLORS ---
HOODIE_ORANGE    = (230, 100,  35)
SKIN_MID         = (210, 155, 110)
HAIR_DARK        = ( 26,  15,  10)
DEEP_COCOA       = ( 59,  40,  32)
PANTS_SAGE       = (130, 145, 115)
SHOE_DARK        = ( 60,  45,  35)
LINE_COLOR       = DEEP_COCOA
ANNOTATION_BG    = (248, 244, 236)
PANEL_BORDER     = (180, 165, 145)
LABEL_BG         = ( 50,  38,  28)
LABEL_TEXT        = (248, 244, 236)
GESTURE_RED      = (220,  50,  40)
GESTURE_BLUE     = ( 60, 120, 200)
GHOST_GRAY       = (180, 175, 165)
ANCHOR_GREEN     = ( 60, 180,  80)
BEAT_COLOR       = ( 80, 120, 200)
MOTION_ARROW     = (220,  60,  20)
WARM_AMBER_IRIS  = (200, 125,  62)

# --- CANVAS ---
W, H = 1280, 720
PAD = 14
TITLE_H = 44
PANEL_W = (W - PAD * 3) // 2
PANEL_H = H - PAD * 2 - TITLE_H


def bezier_point(p0, p1, p2, p3, t):
    """Delegates to curve_utils.cubic_bezier_single (int-cast for compat)."""
    pt = _cu_single(p0, p1, p2, p3, t)
    return (int(pt[0]), int(pt[1]))


def draw_bezier_curve(draw, p0, p1, p2, p3, color, width=2, steps=30):
    """Delegates to curve_utils.draw_bezier_polyline."""
    return _cu_draw_bezier(draw, p0, p1, p2, p3, color, width=width, steps=steps)


def draw_anchor(draw, x, y, r=4, color=ANCHOR_GREEN):
    """Draw a filled anchor point circle."""
    draw.ellipse([x - r, y - r, x + r, y + r], fill=color, outline=LINE_COLOR, width=1)


def label_box(draw, x, y, text, bg=LABEL_BG, fg=LABEL_TEXT, font=None, pad_h=4, pad_v=3):
    """Small filled label rectangle."""
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
    else:
        bbox = draw.textbbox((0, 0), text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rectangle([x, y, x + tw + pad_h * 2, y + th + pad_v * 2], fill=bg)
    draw.text((x + pad_h, y + pad_v), text, fill=fg, font=font)
    return tw + pad_h * 2, th + pad_v * 2


def draw_arrow(draw, x0, y0, x1, y1, color=MOTION_ARROW, width=2, head=8):
    """Arrow with head."""
    draw.line([(x0, y0), (x1, y1)], fill=color, width=width)
    angle = math.atan2(y1 - y0, x1 - x0)
    for da in (-0.4, 0.4):
        ax = x1 - head * math.cos(angle + da)
        ay = y1 - head * math.sin(angle + da)
        draw.line([(x1, y1), (int(ax), int(ay))], fill=color, width=width)


# ----------------------------------------------------------------
# OLD APPROACH: Rectangle-first Luma SURPRISED
# ----------------------------------------------------------------
def draw_old_surprised(draw, ox, oy, scale=1.0):
    """Current rectangle-first construction. Same body as every other expression."""
    s = scale
    head_r = int(22 * s)
    body_h = int(head_r * 2.1)
    body_w = int(head_r * 2.0)
    leg_h = int(head_r * 1.1)
    leg_w = int(head_r * 0.55)
    foot_w = int(head_r * 0.8)
    foot_h = int(head_r * 0.35)
    lw = max(2, int(2 * s))

    # Symmetric feet at same Y
    fc = int(leg_w * 0.7)
    for side in [-1, 1]:
        fx = ox + side * fc
        draw.ellipse([fx - foot_w//2, oy - foot_h, fx + foot_w//2, oy],
                     fill=SHOE_DARK, outline=LINE_COLOR, width=lw)

    # Symmetric legs — identical columns
    for side in [-1, 1]:
        lx = ox + side * fc
        draw.rectangle([lx - leg_w//2, oy - leg_h, lx + leg_w//2, oy - foot_h],
                       fill=PANTS_SAGE, outline=LINE_COLOR, width=lw)

    # Centered body rectangle
    body_bottom = oy - leg_h + int(head_r * 0.3)
    body_top = body_bottom - body_h
    body_cx = ox
    hw = body_w // 2
    body_pts = [
        (body_cx - int(body_w * 0.45), body_top),
        (body_cx + int(body_w * 0.45), body_top),
        (body_cx + hw, body_bottom),
        (body_cx - hw, body_bottom),
    ]
    draw.polygon(body_pts, fill=HOODIE_ORANGE, outline=LINE_COLOR)

    # Centered head
    neck_h = int(head_r * 0.12)
    head_cx = body_cx
    head_cy = body_top - neck_h - head_r
    draw.rectangle([head_cx - int(head_r * 0.35), body_top - neck_h,
                    head_cx + int(head_r * 0.35), body_top],
                   fill=SKIN_MID, outline=LINE_COLOR, width=lw - 1)
    draw.ellipse([head_cx - head_r, head_cy - int(head_r * 0.97),
                  head_cx + head_r, head_cy + int(head_r * 0.97)],
                 fill=SKIN_MID, outline=LINE_COLOR, width=lw)

    # Eyes
    ew = int(head_r * 0.22)
    eh = int(ew * 1.1)
    for ex_off in [-int(head_r * 0.35), int(head_r * 0.35)]:
        ex = head_cx + ex_off
        draw.rounded_rectangle([ex - ew, head_cy - eh, ex + ew, head_cy + eh],
                               radius=int(ew * 0.45),
                               fill=(250, 240, 220), outline=DEEP_COCOA, width=lw - 1)
        draw.ellipse([ex - int(ew * 0.6), head_cy - int(ew * 0.6),
                      ex + int(ew * 0.6), head_cy + int(ew * 0.6)],
                     fill=WARM_AMBER_IRIS)
        draw.ellipse([ex - int(ew * 0.3), head_cy - int(ew * 0.3),
                      ex + int(ew * 0.3), head_cy + int(ew * 0.3)],
                     fill=DEEP_COCOA)

    # Symmetric arms spread wide
    arm_l = int(head_r * 1.35)
    arm_w = int(head_r * 0.35)
    shoulder_y = body_top + int(body_h * 0.18)
    for side, angle_deg in [(-1, -30), (1, -150)]:
        sx = body_cx + side * int(body_w * 0.40)
        angle = math.radians(angle_deg)
        ex = sx + int(arm_l * math.cos(angle))
        ey = shoulder_y + int(arm_l * math.sin(angle))
        draw.line([(sx, shoulder_y), (ex, ey)], fill=HOODIE_ORANGE, width=int(arm_w * 1.2))
        draw.line([(sx, shoulder_y), (ex, ey)], fill=LINE_COLOR, width=lw)
        draw.ellipse([ex - arm_w//2, ey - arm_w//2, ex + arm_w//2, ey + arm_w//2],
                     fill=SKIN_MID, outline=LINE_COLOR, width=lw - 1)

    # Hair
    hair_top = head_cy - head_r - int(head_r * 0.85)
    draw.ellipse([head_cx - int(head_r * 1.25), hair_top,
                  head_cx + int(head_r * 1.15), head_cy - int(head_r * 0.3)],
                 fill=HAIR_DARK, outline=LINE_COLOR, width=lw)

    # Draw the gesture line OVER the figure to show it's straight
    # Head top to feet center
    draw.line([(head_cx, hair_top - 8), (ox, oy + 4)],
              fill=GESTURE_RED, width=3)

    return head_cx, head_cy


# ----------------------------------------------------------------
# NEW APPROACH: Gesture-line-first Luma SURPRISED
# ----------------------------------------------------------------
def draw_new_surprised(draw, ox, oy, scale=1.0):
    """
    Gesture-first construction.
    1. Draw gesture line (backward C-curve)
    2. Place anchors ON the line
    3. Build body AROUND the anchors
    """
    s = scale
    head_r = int(26 * s)  # slightly larger for better read
    lw = max(2, int(2 * s))
    body_h_total = int(head_r * 4.2)  # full body from head top to feet

    # --- STEP 1: Define gesture line as cubic bezier ---
    # Backward C-curve: head snaps back, body recoils, weight on back foot
    # The curve goes from HEAD (top) to WEIGHT FOOT (bottom)
    # Head is behind and above, back foot is behind at ground
    head_anchor = (ox - int(18 * s), oy - body_h_total + int(10 * s))
    # Control point 1: upper body leans back
    cp1 = (ox - int(25 * s), oy - int(body_h_total * 0.65))
    # Control point 2: hip pushes forward slightly
    cp2 = (ox + int(8 * s), oy - int(body_h_total * 0.25))
    # Weight foot: back, on the ground
    foot_anchor = (ox - int(10 * s), oy)

    # Draw the gesture line in red
    gesture_pts = draw_bezier_curve(draw, head_anchor, cp1, cp2, foot_anchor,
                                     color=GESTURE_RED, width=3, steps=40)

    # --- STEP 2: Place body anchors along the gesture line ---
    # Sample positions along the bezier
    def sample(t):
        return bezier_point(head_anchor, cp1, cp2, foot_anchor, t)

    head_pos = sample(0.0)        # top of gesture
    neck_pos = sample(0.08)       # neck base
    shoulder_pos = sample(0.15)   # shoulder center
    waist_pos = sample(0.42)      # waist
    hip_pos = sample(0.52)        # hip center
    knee_pos = sample(0.75)       # approximate knee
    ankle_pos = sample(0.92)      # ankle
    foot_pos = sample(1.0)        # weight foot

    # Free foot: forward and lifted
    free_foot_pos = (ox + int(14 * s), oy - int(6 * s))

    # Mark anchor points
    for pt, label in [(head_pos, "H"), (shoulder_pos, "S"), (hip_pos, "Hip"),
                      (foot_pos, "WF"), (free_foot_pos, "FF")]:
        draw_anchor(draw, pt[0], pt[1], r=4)

    # --- STEP 3: Build body around anchors ---

    # Shoulders: derive from shoulder_pos with TILT (protective hunch, one higher)
    shoulder_tilt = int(6 * s)  # left shoulder higher (defensive side)
    l_shoulder = (shoulder_pos[0] - int(head_r * 0.7), shoulder_pos[1] - shoulder_tilt)
    r_shoulder = (shoulder_pos[0] + int(head_r * 0.7), shoulder_pos[1] + int(shoulder_tilt * 0.3))

    # Hips: derive from hip_pos with TILT (toward back leg)
    hip_tilt = int(4 * s)
    l_hip = (hip_pos[0] - int(head_r * 0.5), hip_pos[1] - hip_tilt)
    r_hip = (hip_pos[0] + int(head_r * 0.5), hip_pos[1] + int(hip_tilt * 0.5))

    # --- FEET ---
    foot_w = int(head_r * 0.7)
    foot_h = int(head_r * 0.3)
    # Weight foot: planted flat
    draw.ellipse([foot_pos[0] - foot_w//2, foot_pos[1] - foot_h,
                  foot_pos[0] + foot_w//2, foot_pos[1]],
                 fill=SHOE_DARK, outline=LINE_COLOR, width=lw)
    # Free foot: lifted, on toe
    draw.ellipse([free_foot_pos[0] - int(foot_w * 0.4), free_foot_pos[1] - int(foot_h * 0.7),
                  free_foot_pos[0] + int(foot_w * 0.4), free_foot_pos[1]],
                 fill=SHOE_DARK, outline=LINE_COLOR, width=lw)

    # --- LEGS (asymmetric) ---
    leg_w = int(head_r * 0.45)
    # Weight leg: from hip to foot, thicker (load-bearing), STRAIGHTER
    # Upper leg
    wl_knee = (int((l_hip[0] + foot_pos[0]) * 0.5) - int(3 * s),
               int((l_hip[1] + foot_pos[1]) * 0.55))
    draw.line([l_hip, wl_knee], fill=PANTS_SAGE, width=int(leg_w * 1.3))
    draw.line([l_hip, wl_knee], fill=LINE_COLOR, width=lw)
    # Lower leg
    draw.line([wl_knee, (foot_pos[0], foot_pos[1] - foot_h)], fill=PANTS_SAGE, width=int(leg_w * 1.1))
    draw.line([wl_knee, (foot_pos[0], foot_pos[1] - foot_h)], fill=LINE_COLOR, width=lw)

    # Free leg: from hip to free foot, thinner, BENT at knee
    fl_knee = (int((r_hip[0] + free_foot_pos[0]) * 0.5) + int(5 * s),
               int((r_hip[1] + free_foot_pos[1]) * 0.5) - int(8 * s))
    draw.line([r_hip, fl_knee], fill=PANTS_SAGE, width=int(leg_w * 1.1))
    draw.line([r_hip, fl_knee], fill=LINE_COLOR, width=lw)
    draw.line([fl_knee, (free_foot_pos[0], free_foot_pos[1] - int(foot_h * 0.5))],
              fill=PANTS_SAGE, width=int(leg_w * 0.9))
    draw.line([fl_knee, (free_foot_pos[0], free_foot_pos[1] - int(foot_h * 0.5))],
              fill=LINE_COLOR, width=lw)

    # --- TORSO (built between shoulder and hip anchors, following gesture line) ---
    # Trapezoid between shoulders and hips, TILTED to match gesture
    torso_pts = [l_shoulder, r_shoulder, r_hip, l_hip]
    draw.polygon(torso_pts, fill=HOODIE_ORANGE, outline=LINE_COLOR)

    # Hoodie pixel pattern
    torso_cx = (l_shoulder[0] + r_shoulder[0]) // 2
    torso_cy = (l_shoulder[1] + l_hip[1]) // 2
    for i, col in enumerate([(0, 212, 232), (0, 212, 232), (230, 80, 160)]):
        px = torso_cx - 6 + i * 5
        py = torso_cy - int(5 * s)
        draw.rectangle([px, py, px + 3, py + 3], fill=col)

    # --- ARMS (asymmetric: one up-shield, one flung-back) ---
    arm_w_px = int(head_r * 0.30)
    # Left arm: UP near face (shield/defensive)
    l_elbow = (l_shoulder[0] - int(12 * s), l_shoulder[1] - int(20 * s))
    l_hand = (l_shoulder[0] + int(5 * s), l_shoulder[1] - int(38 * s))
    # Upper arm
    draw.line([l_shoulder, l_elbow], fill=HOODIE_ORANGE, width=int(arm_w_px * 1.3))
    draw.line([l_shoulder, l_elbow], fill=LINE_COLOR, width=lw)
    # Forearm
    draw.line([l_elbow, l_hand], fill=HOODIE_ORANGE, width=int(arm_w_px * 1.1))
    draw.line([l_elbow, l_hand], fill=LINE_COLOR, width=lw)
    # Hand (open, palm out)
    draw.ellipse([l_hand[0] - int(arm_w_px * 0.7), l_hand[1] - int(arm_w_px * 0.7),
                  l_hand[0] + int(arm_w_px * 0.7), l_hand[1] + int(arm_w_px * 0.7)],
                 fill=SKIN_MID, outline=LINE_COLOR, width=lw - 1)

    # Right arm: FLUNG back and down (counterbalance)
    r_elbow = (r_shoulder[0] + int(22 * s), r_shoulder[1] + int(10 * s))
    r_hand = (r_shoulder[0] + int(38 * s), r_shoulder[1] + int(22 * s))
    draw.line([r_shoulder, r_elbow], fill=HOODIE_ORANGE, width=int(arm_w_px * 1.3))
    draw.line([r_shoulder, r_elbow], fill=LINE_COLOR, width=lw)
    draw.line([r_elbow, r_hand], fill=HOODIE_ORANGE, width=int(arm_w_px * 1.1))
    draw.line([r_elbow, r_hand], fill=LINE_COLOR, width=lw)
    draw.ellipse([r_hand[0] - int(arm_w_px * 0.6), r_hand[1] - int(arm_w_px * 0.6),
                  r_hand[0] + int(arm_w_px * 0.6), r_hand[1] + int(arm_w_px * 0.6)],
                 fill=SKIN_MID, outline=LINE_COLOR, width=lw - 1)

    # --- HEAD (positioned on gesture line, tilted back) ---
    head_cx = head_pos[0]
    head_cy = head_pos[1]
    # Neck connecting to shoulder center
    draw.line([neck_pos, shoulder_pos], fill=SKIN_MID, width=int(head_r * 0.5))
    draw.line([neck_pos, shoulder_pos], fill=LINE_COLOR, width=lw)

    # Head ellipse (slightly tilted back)
    draw.ellipse([head_cx - head_r, head_cy - int(head_r * 0.97),
                  head_cx + head_r, head_cy + int(head_r * 0.97)],
                 fill=SKIN_MID, outline=LINE_COLOR, width=lw)

    # Eyes — wide open (surprise)
    ew = int(head_r * 0.24)
    eh = int(ew * 1.3)  # wider for surprise
    eye_y = head_cy - int(head_r * 0.05)
    for ex_off in [-int(head_r * 0.33), int(head_r * 0.33)]:
        ex = head_cx + ex_off
        draw.rounded_rectangle([ex - ew, eye_y - eh, ex + ew, eye_y + eh],
                               radius=int(ew * 0.3),
                               fill=(250, 240, 220), outline=DEEP_COCOA, width=lw - 1)
        draw.ellipse([ex - int(ew * 0.55), eye_y - int(ew * 0.55),
                      ex + int(ew * 0.55), eye_y + int(ew * 0.55)],
                     fill=WARM_AMBER_IRIS)
        draw.ellipse([ex - int(ew * 0.25), eye_y - int(ew * 0.25),
                      ex + int(ew * 0.25), eye_y + int(ew * 0.25)],
                     fill=DEEP_COCOA)
        draw.ellipse([ex - int(ew * 0.15), eye_y - int(ew * 0.35),
                      ex + int(ew * 0.05), eye_y - int(ew * 0.1)],
                     fill=(240, 240, 240))

    # Brows — raised (surprise)
    brow_y = eye_y - eh - int(head_r * 0.22)
    brow_w = int(head_r * 0.28)
    brow_thick = max(2, int(2.5 * s))
    for bx_off in [-int(head_r * 0.33), int(head_r * 0.33)]:
        bx = head_cx + bx_off
        draw.arc([bx - brow_w, brow_y - int(head_r * 0.06),
                  bx + brow_w, brow_y + int(head_r * 0.12)],
                 start=200, end=340, fill=DEEP_COCOA, width=brow_thick)

    # Mouth — open O (surprise)
    m_y = head_cy + int(head_r * 0.35)
    m_r = int(head_r * 0.16)
    draw.ellipse([head_cx - m_r, m_y - int(m_r * 0.8),
                  head_cx + m_r, m_y + int(m_r * 0.8)],
                 fill=(180, 80, 60), outline=LINE_COLOR, width=lw - 1)

    # Hair — trailing behind (secondary motion)
    hair_dx = int(8 * s)  # hair trails behind the recoil direction
    hair_top = head_cy - head_r - int(head_r * 0.8)
    draw.ellipse([head_cx - int(head_r * 1.2) + hair_dx, hair_top,
                  head_cx + int(head_r * 1.1) + hair_dx, head_cy - int(head_r * 0.3)],
                 fill=HAIR_DARK, outline=LINE_COLOR, width=lw)

    return head_cx, head_cy


# ----------------------------------------------------------------
# MAIN — Assemble comparison sheet
# ----------------------------------------------------------------
def main():
    img = Image.new("RGB", (W, H), ANNOTATION_BG)
    draw = ImageDraw.Draw(img)

    # --- Title bar ---
    draw.rectangle([0, 0, W, TITLE_H], fill=LABEL_BG)
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except OSError:
        title_font = ImageFont.load_default()
        label_font = title_font
        small_font = title_font

    draw.text((PAD, 8), "GESTURE LINE COMPARISON — LUMA SURPRISED", fill=LABEL_TEXT, font=title_font)
    draw.text((PAD, 26),
              "Ryo Hasegawa | Luma & the Glitchkin | C50  |  LEFT: rectangle-first (current)  |  RIGHT: gesture-line-first (new)",
              fill=(180, 170, 155), font=small_font)

    # Legend
    legend_x = W - 400
    draw.rectangle([legend_x, 6, legend_x + 8, 14], fill=GESTURE_RED)
    draw.text((legend_x + 12, 6), "Gesture line (line of action)", fill=(200, 190, 170), font=small_font)
    draw.ellipse([legend_x, 22, legend_x + 8, 30], fill=ANCHOR_GREEN)
    draw.text((legend_x + 12, 20), "Body anchor points", fill=(200, 190, 170), font=small_font)
    draw.rectangle([legend_x + 200, 6, legend_x + 208, 14], fill=MOTION_ARROW)
    draw.text((legend_x + 212, 6), "Secondary motion", fill=(200, 190, 170), font=small_font)

    # --- Panel backgrounds ---
    left_x = PAD
    right_x = PAD * 2 + PANEL_W
    panel_y = TITLE_H + PAD

    for px in [left_x, right_x]:
        draw.rectangle([px, panel_y, px + PANEL_W, panel_y + PANEL_H],
                       outline=PANEL_BORDER, width=2)

    # --- LEFT: Rectangle-first (OLD) ---
    fig_cx_old = left_x + PANEL_W // 2
    fig_oy_old = panel_y + PANEL_H - 40

    draw_old_surprised(draw, fig_cx_old, fig_oy_old, scale=1.8)

    # Annotations for old approach
    label_box(draw, left_x + 8, panel_y + 8, "OLD: Rectangle-First", font=label_font)
    # Problem callouts
    problems = [
        (left_x + 12, panel_y + 40, "Straight vertical gesture line"),
        (left_x + 12, panel_y + 56, "Symmetric legs (identical columns)"),
        (left_x + 12, panel_y + 72, "Head centered over body center"),
        (left_x + 12, panel_y + 88, "Arms symmetric (mirror positions)"),
        (left_x + 12, panel_y + 104, "No weight distribution"),
        (left_x + 12, panel_y + 120, "No hip tilt or shoulder counter"),
        (left_x + 12, panel_y + 136, "Body shape identical to all other expressions"),
    ]
    for x, y, text in problems:
        draw.text((x, y), "X  " + text, fill=(180, 60, 40), font=small_font)

    # Verdict
    draw.rectangle([left_x + 8, panel_y + PANEL_H - 50, left_x + PANEL_W - 8, panel_y + PANEL_H - 8],
                   fill=(180, 60, 40))
    draw.text((left_x + 16, panel_y + PANEL_H - 46),
              "GESTURE TEST: FAIL — Body reads as STANDING, not SURPRISED",
              fill=(255, 255, 255), font=label_font)
    draw.text((left_x + 16, panel_y + PANEL_H - 28),
              "Cover face: emotion = NONE. This is a mannequin with arms repositioned.",
              fill=(255, 220, 200), font=small_font)

    # Refresh draw context after all panel work
    draw = ImageDraw.Draw(img)

    # --- RIGHT: Gesture-first (NEW) ---
    fig_cx_new = right_x + PANEL_W // 2 - int(10 * 1)
    fig_oy_new = panel_y + PANEL_H - 40

    draw_new_surprised(draw, fig_cx_new, fig_oy_new, scale=1.8)

    # Annotations for new approach
    label_box(draw, right_x + 8, panel_y + 8, "NEW: Gesture-Line-First", bg=(40, 100, 60), font=label_font)
    improvements = [
        (right_x + 12, panel_y + 40, "Backward C-curve gesture line (recoil)"),
        (right_x + 12, panel_y + 56, "Weight 70/30 on back foot (off-balance)"),
        (right_x + 12, panel_y + 72, "Head snapped back behind shoulders"),
        (right_x + 12, panel_y + 88, "Arms asymmetric: shield UP + flung BACK"),
        (right_x + 12, panel_y + 104, "Hip tilt toward weight-bearing leg"),
        (right_x + 12, panel_y + 120, "Shoulder counter-tilt (one raised, one dropped)"),
        (right_x + 12, panel_y + 136, "Free foot lifted (lost contact with ground)"),
        (right_x + 12, panel_y + 152, "Two-segment arms with elbow bend"),
        (right_x + 12, panel_y + 168, "Hair trails BEHIND recoil (secondary motion)"),
    ]
    for x, y, text in improvements:
        draw.text((x, y), "+  " + text, fill=(40, 130, 60), font=small_font)

    # Verdict
    draw.rectangle([right_x + 8, panel_y + PANEL_H - 50, right_x + PANEL_W - 8, panel_y + PANEL_H - 8],
                   fill=(40, 100, 60))
    draw.text((right_x + 16, panel_y + PANEL_H - 46),
              "GESTURE TEST: PASS — Body reads as STARTLED without seeing face",
              fill=(255, 255, 255), font=label_font)
    draw.text((right_x + 16, panel_y + PANEL_H - 28),
              "Cover face: emotion = RECOIL/SURPRISE. 9 anchor points vs 3.",
              fill=(200, 240, 200), font=small_font)

    # --- Save ---
    out_path = os.path.join(_OUTPUT_DIR, "LTG_CHAR_luma_gesture_prototype.png")
    img = img.resize((W, H), Image.LANCZOS)  # ensure size
    img.save(out_path, "PNG")
    print(f"Saved: {out_path}")
    print(f"Size: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
