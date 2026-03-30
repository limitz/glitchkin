# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_CHAR_luma_motion.py
Ryo Hasegawa / Cycle 38
Motion Spec Sheet — LUMA (v002)

FIXES from C37/C38 critique:
1. P1 CG SUPPORT POLYGON: body lean/tilt clamped so CG never leaves foot support polygon.
   CG is constrained within ±(foot_half_span) of feet midpoint.
2. P1 ARM/SHOULDER MASS: shoulder geometry circle added as origin point for all arm movement.
3. P1 HAIR ANNOTATION VS CODE: Panel 1 annotation corrected to match code (hair_trail_angle=-12
   = pre-lean IS active; was incorrectly labeled "NOT yet trailing").

Output: output/characters/motion/LTG_CHAR_luma_motion.png
Canvas: 1280x720 (≤1280 limit)
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
from PIL import Image, ImageDraw
import os
import math

# --- CANONICAL COLORS (from master_palette.md) ---
HOODIE_ORANGE    = (230, 100,  35)   # RW-01 Luma Hoodie Orange
SKIN_MID         = (210, 155, 110)   # RW-03 Mid Skin
HAIR_DARK        = ( 26,  15,  10)   # Near-Black Espresso
DEEP_COCOA       = ( 59,  40,  32)   # line work
WARM_AMBER_IRIS  = (200, 125,  62)   # eye iris
PANTS_SAGE       = (130, 145, 115)   # trousers
SHOE_DARK        = ( 60,  45,  35)
PIXEL_CYAN       = (  0, 212, 232)   # hoodie pixel pattern accent
ANNOTATION_BG    = (248, 244, 236)   # panel background warm cream
PANEL_BORDER     = (180, 165, 145)
LABEL_BG         = ( 50,  38,  28)
LABEL_TEXT       = (248, 244, 236)
LINE_COLOR       = DEEP_COCOA
MOTION_ARROW     = (220,  60,  20)   # bright orange arrows for secondary motion
BEAT_COLOR       = ( 80, 120, 200)   # blue for beat counts / timing
ACCENT_DASH      = (200, 190, 175)   # construction guide lines
SHOULDER_COL     = (190, 135,  90)   # shoulder geometry indicator
CG_COLOR         = (220, 40, 40)     # CG marker color (red)

# --- CANVAS ---
W, H = 1280, 720
COLS, ROWS = 4, 1
PAD = 14
PANEL_W = (W - PAD * (COLS + 1)) // COLS
PANEL_H = H - PAD * 2 - 40  # 40px for top title bar


# ------------------------------------------------------------------ helpers

def panel_origin(col):
    """Top-left (x, y) of panel col (0-based)."""
    x = PAD + col * (PANEL_W + PAD)
    y = PAD + 40
    return x, y


def draw_arrow(draw, x0, y0, x1, y1, color=MOTION_ARROW, width=2, head=8):
    """Draw an arrow from (x0,y0) to (x1,y1) with arrowhead."""
    draw.line([(x0, y0), (x1, y1)], fill=color, width=width)
    angle = math.atan2(y1 - y0, x1 - x0)
    for da in (-0.4, 0.4):
        ax = x1 - head * math.cos(angle + da)
        ay = y1 - head * math.sin(angle + da)
        draw.line([(x1, y1), (int(ax), int(ay))], fill=color, width=width)


def draw_curved_arrow(draw, cx, cy, start_angle, end_angle, radius, color, width=2, head=7):
    """Curved secondary-motion arc with arrowhead at end."""
    pts = []
    steps = 20
    for i in range(steps + 1):
        t = start_angle + (end_angle - start_angle) * i / steps
        x = cx + radius * math.cos(t)
        y = cy + radius * math.sin(t)
        pts.append((int(x), int(y)))
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=color, width=width)
    # arrowhead at last point
    tx = pts[-1][0] - pts[-2][0]
    ty = pts[-1][1] - pts[-2][1]
    angle = math.atan2(ty, tx)
    x1, y1 = pts[-1]
    for da in (-0.4, 0.4):
        ax = x1 - head * math.cos(angle + da)
        ay = y1 - head * math.sin(angle + da)
        draw.line([(x1, y1), (int(ax), int(ay))], fill=color, width=width)


def label_box(draw, x, y, text, bg=LABEL_BG, fg=LABEL_TEXT, font=None, pad=4):
    """Small filled label rectangle."""
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
    else:
        bbox = draw.textbbox((0, 0), text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rectangle([x, y, x + tw + pad * 2, y + th + pad * 2], fill=bg)
    draw.text((x + pad, y + pad), text, fill=fg, font=font)
    return tw + pad * 2, th + pad * 2


def annotation_line(draw, x, y, text, color=BEAT_COLOR, font=None):
    draw.text((x, y), text, fill=color, font=font)


def draw_cg_marker(draw, cx, cy, r=5, color=CG_COLOR):
    """Draw a small cross+circle CG (center of gravity) indicator."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=2)
    draw.line([(cx - r - 3, cy), (cx + r + 3, cy)], fill=color, width=2)
    draw.line([(cx, cy - r - 3), (cx, cy + r + 3)], fill=color, width=2)


# ------------------------------------------------------------------ character drawing

def draw_luma_figure(draw, ox, oy, scale=1.0,
                     body_tilt=0, head_tilt=0,
                     hair_lift=0, hair_trail_angle=0,
                     hoodie_flare=0, lean_forward=0,
                     arm_left_angle=-30, arm_right_angle=-150,
                     leg_left_spread=0, leg_right_spread=0,
                     show_hoodie_settle=False,
                     show_cg=False):
    """
    Draws Luma as a simplified geometric construction figure.
    ox, oy = center-bottom of figure
    scale = overall scale factor
    body_tilt = degrees (positive = tilt right)
    head_tilt = degrees (positive = tilt right)
    hair_lift = px additional hair height
    hair_trail_angle = degrees CCW (positive = lean back as in sprint)
    hoodie_flare = px of hoodie hem flare (secondary motion)
    lean_forward = px of forward lean — CLAMPED to keep CG within support polygon
    show_cg = if True, draw CG marker + support polygon

    FIX v002: lean_forward is applied as a VISUAL shift of the body top only.
    The body_cx (CG anchor) is kept within the support polygon defined by the feet.
    Support polygon = ±foot_half_span from ox.
    Actual CG shift from lean = lean_forward * 0.5 (partial forward lean of mass).
    Total CG offset from tilt+lean is clamped to ±(foot_span * 0.4).
    """
    s = scale
    # proportions: 3.2 heads total
    head_r = int(22 * s)
    body_h = int(head_r * 2.1)
    body_w = int(head_r * 2.0)
    leg_h  = int(head_r * 1.1)
    leg_w  = int(head_r * 0.55)
    foot_w = int(head_r * 0.8)
    foot_h = int(head_r * 0.35)

    lw = max(2, int(2 * s))  # line weight

    # --- SUPPORT POLYGON ---
    fc = int(leg_w * 0.7)  # foot center offset from ox
    foot_half_span = fc + foot_w // 2  # half-width of support polygon

    # --- CG / LEAN CONSTRAINT (P1 FIX) ---
    # Raw tilt offset at body top
    tilt_offset = int(math.tan(math.radians(body_tilt)) * (leg_h + body_h * 0.5))
    # The CG shift is a combination of tilt and lean_forward.
    # We model CG as approximately at body mid-height.
    # lean_forward shifts the whole body relative to feet; tilt shifts the top.
    # CG offset = lean_forward (lateral shift of upper body) + tilt contribution
    raw_cg_offset = lean_forward + int(math.tan(math.radians(body_tilt)) * leg_h)
    # Clamp CG offset to within 40% of foot half-span
    max_cg_shift = int(foot_half_span * 0.40)
    cg_offset = max(-max_cg_shift, min(max_cg_shift, raw_cg_offset))

    # body_cx is the CG position (constrained)
    body_cx = ox + cg_offset

    # Visual tilt offset for body top (body top leans further than CG)
    body_top_visual_offset = int(math.tan(math.radians(body_tilt)) * body_h * 0.5)

    # Leg tops follow the CG base
    leg_tilt_offset = int(math.tan(math.radians(body_tilt)) * leg_h)

    # --- FEET ---
    lf_cx = ox - fc + leg_left_spread
    lf_cy = oy
    draw.ellipse([lf_cx - foot_w // 2, lf_cy - foot_h,
                  lf_cx + foot_w // 2, lf_cy],
                 fill=SHOE_DARK, outline=LINE_COLOR, width=lw)
    rf_cx = ox + fc + leg_right_spread
    rf_cy = oy
    draw.ellipse([rf_cx - foot_w // 2, rf_cy - foot_h,
                  rf_cx + foot_w // 2, rf_cy],
                 fill=SHOE_DARK, outline=LINE_COLOR, width=lw)

    # --- LEGS ---
    # left leg
    ll_top_x = ox - fc + leg_left_spread // 2 + leg_tilt_offset
    ll_top_y = oy - leg_h
    draw.rectangle([ll_top_x - leg_w // 2, ll_top_y,
                    ll_top_x + leg_w // 2, oy - foot_h],
                   fill=PANTS_SAGE, outline=LINE_COLOR, width=lw)
    # right leg
    rl_top_x = ox + fc + leg_right_spread // 2 + leg_tilt_offset
    rl_top_y = oy - leg_h
    draw.rectangle([rl_top_x - leg_w // 2, rl_top_y,
                    rl_top_x + leg_w // 2, oy - foot_h],
                   fill=PANTS_SAGE, outline=LINE_COLOR, width=lw)

    # --- BODY (hoodie) ---
    body_bottom_y = oy - leg_h + int(head_r * 0.3)
    body_top_y = body_bottom_y - body_h
    # Body top has visual lean from tilt + lean_forward, but constrained at CG
    body_top_cx = body_cx + body_top_visual_offset
    hw = body_w // 2 + hoodie_flare
    # A-line hoodie shape (trapezoid-ish)
    body_pts = [
        (body_top_cx - int(body_w * 0.45), body_top_y),
        (body_top_cx + int(body_w * 0.45), body_top_y),
        (body_cx + hw, body_bottom_y),
        (body_cx - hw, body_bottom_y),
    ]
    draw.polygon(body_pts, fill=HOODIE_ORANGE, outline=LINE_COLOR)
    draw.line([(body_pts[0][0], body_top_y),
               (body_pts[1][0], body_top_y)],
              fill=LINE_COLOR, width=lw)

    # pixel pattern hint on hoodie chest (3 tiny squares)
    for i, col in enumerate([PIXEL_CYAN, PIXEL_CYAN, (230, 80, 160)]):
        px_ = body_top_cx - 6 + i * 5
        py_ = body_top_y + int(body_h * 0.4)
        draw.rectangle([px_, py_, px_ + 3, py_ + 3], fill=col)

    # hoodie pocket bump
    draw.arc([body_cx - int(body_w * 0.25), body_bottom_y - int(head_r * 0.4),
              body_cx + int(body_w * 0.25), body_bottom_y + 4],
             start=200, end=340, fill=LINE_COLOR, width=lw - 1)

    # --- SHOULDERS (P1 FIX: shoulder geometry as arm origin) ---
    shoulder_y = body_top_y + int(body_h * 0.18)
    shoulder_r = int(head_r * 0.22)  # shoulder mass radius
    left_shoulder_cx  = body_top_cx - int(body_w * 0.42)
    right_shoulder_cx = body_top_cx + int(body_w * 0.42)

    # Draw shoulder circles as mass indicators
    draw.ellipse([left_shoulder_cx - shoulder_r, shoulder_y - shoulder_r,
                  left_shoulder_cx + shoulder_r, shoulder_y + shoulder_r],
                 fill=SHOULDER_COL, outline=LINE_COLOR, width=lw - 1)
    draw.ellipse([right_shoulder_cx - shoulder_r, shoulder_y - shoulder_r,
                  right_shoulder_cx + shoulder_r, shoulder_y + shoulder_r],
                 fill=SHOULDER_COL, outline=LINE_COLOR, width=lw - 1)

    # --- ARMS (originate from shoulder center) ---
    arm_l = int(head_r * 1.35)
    arm_w = int(head_r * 0.35)

    # left arm — origin is left shoulder center
    la_angle = math.radians(arm_left_angle)
    la_ex = left_shoulder_cx + int(arm_l * math.cos(la_angle))
    la_ey = shoulder_y + int(arm_l * math.sin(la_angle))
    draw.line([(left_shoulder_cx, shoulder_y),
               (la_ex, la_ey)], fill=HOODIE_ORANGE, width=int(arm_w * 1.2))
    draw.line([(left_shoulder_cx, shoulder_y),
               (la_ex, la_ey)], fill=LINE_COLOR, width=lw)
    draw.ellipse([la_ex - arm_w // 2, la_ey - arm_w // 2,
                  la_ex + arm_w // 2, la_ey + arm_w // 2],
                 fill=SKIN_MID, outline=LINE_COLOR, width=lw - 1)

    # right arm — origin is right shoulder center
    ra_angle = math.radians(arm_right_angle)
    ra_ex = right_shoulder_cx + int(arm_l * math.cos(ra_angle))
    ra_ey = shoulder_y + int(arm_l * math.sin(ra_angle))
    draw.line([(right_shoulder_cx, shoulder_y),
               (ra_ex, ra_ey)], fill=HOODIE_ORANGE, width=int(arm_w * 1.2))
    draw.line([(right_shoulder_cx, shoulder_y),
               (ra_ex, ra_ey)], fill=LINE_COLOR, width=lw)
    draw.ellipse([ra_ex - arm_w // 2, ra_ey - arm_w // 2,
                  ra_ex + arm_w // 2, ra_ey + arm_w // 2],
                 fill=SKIN_MID, outline=LINE_COLOR, width=lw - 1)

    # --- HEAD ---
    neck_h = int(head_r * 0.12)
    head_cx = body_top_cx + int(math.tan(math.radians(head_tilt + body_tilt * 0.5)) * head_r)
    head_cy = body_top_y - neck_h - head_r

    # neck
    draw.rectangle([head_cx - int(head_r * 0.35), body_top_y - neck_h,
                    head_cx + int(head_r * 0.35), body_top_y],
                   fill=SKIN_MID, outline=LINE_COLOR, width=lw - 1)

    # head circle
    draw.ellipse([head_cx - head_r, head_cy - int(head_r * 0.97),
                  head_cx + head_r, head_cy + int(head_r * 0.97)],
                 fill=SKIN_MID, outline=LINE_COLOR, width=lw)

    # eyes
    ew = int(head_r * 0.22)
    eh = int(ew * 1.1)
    eye_y = head_cy
    for ex_offset in [-int(head_r * 0.35), int(head_r * 0.35)]:
        ex = head_cx + ex_offset
        draw.rounded_rectangle([ex - ew, eye_y - eh, ex + ew, eye_y + eh],
                                radius=int(ew * 0.45),
                                fill=(250, 240, 220), outline=DEEP_COCOA, width=lw - 1)
        # iris
        draw.ellipse([ex - int(ew * 0.6), eye_y - int(ew * 0.6),
                      ex + int(ew * 0.6), eye_y + int(ew * 0.6)],
                     fill=WARM_AMBER_IRIS)
        draw.ellipse([ex - int(ew * 0.3), eye_y - int(ew * 0.3),
                      ex + int(ew * 0.3), eye_y + int(ew * 0.3)],
                     fill=DEEP_COCOA)
        # highlight
        draw.ellipse([ex - int(ew * 0.2), eye_y - int(ew * 0.4),
                      ex + int(ew * 0.05), eye_y - int(ew * 0.1)],
                     fill=(240, 240, 240))

    # brows
    brow_y = eye_y - eh - int(head_r * 0.18)
    brow_w = int(head_r * 0.30)
    brow_thick = max(2, int(2.5 * s))
    for bx_off in [-int(head_r * 0.35), int(head_r * 0.35)]:
        bx = head_cx + bx_off
        draw.line([(bx - brow_w, brow_y + 2),
                   (bx, brow_y),
                   (bx + brow_w, brow_y + 2)],
                  fill=DEEP_COCOA, width=brow_thick)

    # nose
    draw.arc([head_cx - int(head_r * 0.08), head_cy + int(head_r * 0.06),
              head_cx + int(head_r * 0.08), head_cy + int(head_r * 0.22)],
             start=0, end=180, fill=LINE_COLOR, width=max(1, lw - 1))

    # mouth (slight smile)
    m_y = head_cy + int(head_r * 0.45)
    draw.arc([head_cx - int(head_r * 0.22), m_y - int(head_r * 0.1),
              head_cx + int(head_r * 0.22), m_y + int(head_r * 0.14)],
             start=20, end=160, fill=LINE_COLOR, width=lw - 1)

    # --- HAIR ---
    hair_mass_h = int(head_r * 0.95) + hair_lift
    hair_dx = int(math.tan(math.radians(hair_trail_angle)) * hair_mass_h * 0.7)
    hair_cx = head_cx + hair_dx
    hair_top = head_cy - head_r - hair_mass_h + int(head_r * 0.1)
    hair_left = hair_cx - int(head_r * 1.25)
    hair_right = hair_cx + int(head_r * 1.15)
    # main mass ellipse
    draw.ellipse([hair_left, hair_top,
                  hair_right, head_cy - int(head_r * 0.3)],
                 fill=HAIR_DARK, outline=LINE_COLOR, width=lw)
    # 5 curl indicators
    import random
    rng = random.Random(42)
    for i in range(5):
        cx_c = hair_cx + rng.randint(-int(head_r * 0.7), int(head_r * 0.6))
        cy_c = head_cy - head_r - rng.randint(int(head_r * 0.2), int(head_r * 0.8))
        cr = rng.randint(int(head_r * 0.15), int(head_r * 0.30))
        draw.arc([cx_c - cr, cy_c - cr, cx_c + cr, cy_c + cr],
                 start=rng.randint(0, 120), end=rng.randint(200, 340),
                 fill=(60, 30, 15), width=max(1, lw - 1))

    # hoodie settle indicator (dashed arc at hem if show_hoodie_settle)
    if show_hoodie_settle:
        for i in range(0, 16, 2):
            a_start = 190 + i * 10
            a_end = a_start + 9
            draw.arc([body_cx - hw - 4, body_bottom_y - 6,
                      body_cx + hw + 4, body_bottom_y + 16],
                     start=a_start, end=a_end,
                     fill=MOTION_ARROW, width=2)

    # --- CG MARKER + SUPPORT POLYGON (optional, for documentation panels) ---
    cg_y = body_bottom_y - int(body_h * 0.45)  # approximate CG height
    if show_cg:
        # Support polygon line at ground level
        draw.line([(ox - foot_half_span, oy + 4), (ox + foot_half_span, oy + 4)],
                  fill=CG_COLOR, width=1)
        draw.text((ox - foot_half_span - 2, oy + 6), "|", fill=CG_COLOR)
        draw.text((ox + foot_half_span - 2, oy + 6), "|", fill=CG_COLOR)
        # Vertical CG plumb line
        draw.line([(body_cx, cg_y), (body_cx, oy + 4)],
                  fill=CG_COLOR, width=1)
        # CG dot
        draw_cg_marker(draw, body_cx, cg_y)

    return head_cx, head_cy, head_r, body_cx, body_bottom_y, hw, body_top_y, shoulder_y, body_top_cx


# ------------------------------------------------------------------ PANEL DRAWING

def draw_panel_bg(draw, col, title, subtitle=""):
    px, py = panel_origin(col)
    draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], fill=ANNOTATION_BG, outline=PANEL_BORDER, width=1)
    # title strip at bottom
    draw.rectangle([px, py + PANEL_H - 30, px + PANEL_W, py + PANEL_H], fill=LABEL_BG)
    draw.text((px + 6, py + PANEL_H - 24), title, fill=LABEL_TEXT)
    if subtitle:
        draw.text((px + 6, py + PANEL_H - 13), subtitle, fill=(200, 190, 170))


def draw_panel0_idle(img, draw):
    """Panel 0: Idle / Curious — subtle weight shift, hoodie settle, head tilt."""
    col = 0
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "IDLE / CURIOUS", "beat: 1-2-3-4 loop")

    fig_x = px + PANEL_W // 2
    fig_y = py + PANEL_H - 50

    hcx, hcy, hr, bcx, bby, hw, bty, shy, btopcx = draw_luma_figure(
        draw, fig_x, fig_y, scale=1.05,
        body_tilt=4, head_tilt=8,
        arm_left_angle=-20, arm_right_angle=-160,
        show_hoodie_settle=True,
        show_cg=True
    )

    # weight shift ground contact line
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)],
              fill=ACCENT_DASH, width=1)
    draw.text((px + 14, fig_y + 3), "GROUND", fill=ACCENT_DASH)

    # head tilt annotation
    draw_arrow(draw, hcx + hr + 4, hcy - hr, hcx + hr + 20, hcy + 4,
               color=BEAT_COLOR, width=2)
    draw.text((hcx + hr + 22, hcy - 12), "+8° head tilt", fill=BEAT_COLOR)

    # weight shift arrow (body)
    draw_arrow(draw, bcx - 5, bby + 4, bcx + 16, bby + 4,
               color=MOTION_ARROW, width=2)
    draw.text((bcx + 18, bby - 2), "weight R", fill=MOTION_ARROW)

    # hoodie settle annotation
    draw.text((px + 8, py + PANEL_H - 70), "hoodie hem:", fill=MOTION_ARROW)
    draw.text((px + 8, py + PANEL_H - 58), "+2 beat lag", fill=MOTION_ARROW)

    # shoulder annotation (v002: new)
    draw.text((px + 8, py + PANEL_H - 95), "● shoulder mass origin", fill=SHOULDER_COL)

    # CG annotation
    draw.text((px + 8, py + PANEL_H - 108), "+ CG within polygon", fill=CG_COLOR)

    # timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y), "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Body shift: beat 1", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Head tilt: beat 1.5", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 37), "Hoodie settle: beat 3", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 49), "Return: beat 4 → loop", fill=BEAT_COLOR)


def draw_panel1_sprint_anticipation(img, draw):
    """Panel 1: Sprint Anticipation — weight forward, hair pre-lean ACTIVE at -12°.

    v002 FIX: Annotation corrected. hair_trail_angle=-12 IS active (hair already
    pre-leaning forward at -12°). Previous annotation said 'NOT yet trailing' which
    contradicted the code. Correct reading: this is anticipation pre-lean, NOT the
    full sprint trail (-30°+). Hair begins leaning with body on beat 1.
    """
    col = 1
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "SPRINT ANTICIPATION", "beat: 0-1 (2-frame hold)")

    fig_x = px + PANEL_W // 2 - 10
    fig_y = py + PANEL_H - 50

    hcx, hcy, hr, bcx, bby, hw, bty, shy, btopcx = draw_luma_figure(
        draw, fig_x, fig_y, scale=1.05,
        body_tilt=-10, head_tilt=-8,
        hair_lift=4, hair_trail_angle=-12,
        lean_forward=-12,
        arm_left_angle=-45, arm_right_angle=-135,
        leg_left_spread=-8, leg_right_spread=8,
        show_cg=True
    )

    # ground line
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)],
              fill=ACCENT_DASH, width=1)

    # body lean annotation
    draw_arrow(draw, btopcx, bty + 10, btopcx - 20, bty - 5, color=MOTION_ARROW, width=2)
    draw.text((px + 8, py + PANEL_H - 115), "-10° torso lean", fill=MOTION_ARROW)

    # hair pre-lean annotation — v002: CORRECTED (was "NOT yet trailing")
    draw_arrow(draw, hcx - hr, hcy - hr, hcx - hr - 20, hcy - hr - 8,
               color=MOTION_ARROW, width=2)
    draw.text((px + 8, py + PANEL_H - 100), "hair: -12° pre-lean", fill=MOTION_ARROW)
    draw.text((px + 8, py + PANEL_H - 88), "(anticipation lean: ACTIVE)", fill=MOTION_ARROW)
    draw.text((px + 8, py + PANEL_H - 76), "full trail @ sprint peak", fill=ACCENT_DASH)

    # wide stance indicator
    draw.text((px + 8, py + PANEL_H - 64), "wide stance (1.15×)", fill=BEAT_COLOR)

    # CG constraint note
    draw.text((px + 8, py + PANEL_H - 52), "+ CG within polygon", fill=CG_COLOR)

    # timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y), "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Beat 0: neutral", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Beat 1: ANTICIPATION", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 37), "  — torso dips fwd", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 49), "  — arms back (load)", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 61), "  — hair pre-lean -12°", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 73), "Beat 2: LAUNCH", fill=(220, 60, 20))

    # action line
    draw.line([(btopcx + 20, bty + 15), (btopcx + 50, py + PANEL_H - 60)],
              fill=(180, 120, 80), width=1)
    draw.text((btopcx + 22, bty + 20), "action", fill=(180, 120, 80))
    draw.text((btopcx + 22, bty + 30), "line →", fill=(180, 120, 80))


def draw_panel2_discovery(img, draw):
    """Panel 2: Discovery reaction — full-body recoil + lean-in (2 beats shown)."""
    col = 2
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "DISCOVERY REACTION", "beat A: recoil | beat B: lean-in")

    # Beat A — RECOIL (left half of panel)
    fa_x = px + PANEL_W // 4
    fig_y = py + PANEL_H - 50

    hcx_a, hcy_a, hr, bcx_a, bby, hw, bty, shy, btopcx_a = draw_luma_figure(
        draw, fa_x, fig_y, scale=0.88,
        body_tilt=8, head_tilt=12,
        hair_lift=8,
        arm_left_angle=-60, arm_right_angle=-120,
        lean_forward=6
    )
    # beat A label
    draw.rectangle([fa_x - 18, py + 8, fa_x + 30, py + 20], fill=LABEL_BG)
    draw.text((fa_x - 16, py + 10), "BEAT A", fill=LABEL_TEXT)

    # Beat B — LEAN IN (right half of panel)
    fb_x = px + 3 * PANEL_W // 4
    hcx_b, hcy_b, hr2, bcx_b, bby2, hw2, bty2, shy2, btopcx_b = draw_luma_figure(
        draw, fb_x, fig_y, scale=0.88,
        body_tilt=-6, head_tilt=-15,
        hair_lift=6,
        arm_left_angle=-20, arm_right_angle=-170,
        lean_forward=-8
    )
    # beat B label
    draw.rectangle([fb_x - 18, py + 8, fb_x + 30, py + 20], fill=(30, 80, 140))
    draw.text((fb_x - 16, py + 10), "BEAT B", fill=LABEL_TEXT)

    # transition arrow between the two
    mid_x = px + PANEL_W // 2
    draw_arrow(draw, mid_x - 12, py + PANEL_H // 2 - 10,
               mid_x + 12, py + PANEL_H // 2 - 10,
               color=MOTION_ARROW, width=3, head=10)

    # divider line
    draw.line([(mid_x, py + 30), (mid_x, py + PANEL_H - 35)],
              fill=ACCENT_DASH, width=1)

    # annotations
    draw.text((px + 6, py + PANEL_H - 105), "A: whole body jerks back", fill=MOTION_ARROW)
    draw.text((px + 6, py + PANEL_H - 93), "   (1-frame overshoots)", fill=MOTION_ARROW)
    draw.text((px + 6, py + PANEL_H - 78), "B: forward lean + wide eyes", fill=BEAT_COLOR)
    draw.text((px + 6, py + PANEL_H - 66), "   hair lags 0.5 beat behind B", fill=MOTION_ARROW)

    # ground line
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)],
              fill=ACCENT_DASH, width=1)


def draw_panel3_landing(img, draw):
    """Panel 3: Landing / Stop — follow-through on hoodie + hair."""
    col = 3
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "LANDING / STOP", "secondary: hoodie + hair lag")

    fig_x = px + PANEL_W // 2
    fig_y = py + PANEL_H - 50

    hcx, hcy, hr, bcx, bby, hw, bty, shy, btopcx = draw_luma_figure(
        draw, fig_x, fig_y, scale=1.05,
        body_tilt=3, head_tilt=2,
        hair_lift=0, hair_trail_angle=18,  # hair still travelling forward
        hoodie_flare=8,  # hoodie still swinging wide
        arm_left_angle=-35, arm_right_angle=-145,
        show_hoodie_settle=False
    )

    # Ground contact
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)],
              fill=ACCENT_DASH, width=1)

    # hair follow-through annotation
    draw_arrow(draw, hcx + hr, hcy - int(hr * 0.8), hcx + hr + 22, hcy - int(hr * 0.5),
               color=MOTION_ARROW, width=2)
    draw.text((hcx + hr + 24, hcy - int(hr * 0.9)), "hair: +18°", fill=MOTION_ARROW)
    draw.text((hcx + hr + 24, hcy - int(hr * 0.9) + 11), "still fwd", fill=MOTION_ARROW)

    # hoodie flare annotation
    draw_curved_arrow(draw,
                      bcx + hw - 4, bby - 6,
                      math.radians(90), math.radians(140),
                      int(hr * 0.6),
                      color=MOTION_ARROW, width=2)
    draw.text((px + 8, py + PANEL_H - 105), "hoodie hem: +8px", fill=MOTION_ARROW)
    draw.text((px + 8, py + PANEL_H - 93), "swings past body stop", fill=MOTION_ARROW)

    # timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y), "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Beat 1: body STOPS", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Beat 1.5: hoodie peaks", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 37), "  at +8px flare", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 49), "Beat 2: hair peaks fwd", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 61), "Beat 3: hoodie settles", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 73), "Beat 4: hair settles", fill=BEAT_COLOR)

    # secondary motion key
    draw.text((px + 8, py + PANEL_H - 66), "KEY: body leads, hoodie", fill=ACCENT_DASH)
    draw.text((px + 8, py + PANEL_H - 55), "+0.5b, hair +1.0b behind", fill=MOTION_ARROW)


# ------------------------------------------------------------------ MAIN

def main():
    img = Image.new("RGB", (W, H), color=(235, 228, 215))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, W, PAD + 40], fill=LABEL_BG)
    draw.text((PAD, 8), "LUMA — Motion Spec Sheet v002", fill=LABEL_TEXT)
    draw.text((PAD, 22), "RYO HASEGAWA  |  Luma & the Glitchkin  |  C38  |  FIXES: CG polygon, shoulder mass, hair annotation", fill=(180, 165, 140))
    # legend strip
    legend_x = W - 320
    draw.rectangle([legend_x - 6, 6, legend_x + 312, PAD + 36], fill=(70, 55, 42))
    draw.text((legend_x, 8), "→  Secondary motion", fill=MOTION_ARROW)
    draw.text((legend_x, 20), "■  Timing beats", fill=BEAT_COLOR)
    draw.text((legend_x + 130, 8), "●  Shoulder origin (v002)", fill=SHOULDER_COL)
    draw.text((legend_x + 130, 20), "+  CG marker / support poly", fill=CG_COLOR)

    draw_panel0_idle(img, draw)
    draw_panel1_sprint_anticipation(img, draw)
    draw_panel2_discovery(img, draw)
    draw_panel3_landing(img, draw)

    # enforce ≤1280px
    img.thumbnail((1280, 1280), Image.LANCZOS)

    out_dir = output_dir('characters', 'motion')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_luma_motion.png")
    img.save(out_path)
    print(f"Saved: {out_path} ({img.width}×{img.height}px)")


if __name__ == "__main__":
    main()
