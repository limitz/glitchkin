"""
LTG_TOOL_luma_motion_v001.py
Ryo Hasegawa / Cycle 37 — renamed to LTG_TOOL_ prefix Cycle 38 (Kai Nakamura)
Motion Spec Sheet — LUMA
4 panels: Idle/Curious | Sprint Anticipation | Discovery Reaction (2-beat) | Landing/Stop
Output: output/characters/motion/LTG_CHAR_luma_motion_v001.png
Canvas: 1280x720 (≤1280 limit)

NOTE: This is the canonical LTG_TOOL_ version.
      LTG_CHAR_luma_motion_v001.py is a forwarding stub pointing here.
"""

from PIL import Image, ImageDraw, ImageFont
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


# ------------------------------------------------------------------ character drawing

def draw_luma_figure(draw, ox, oy, scale=1.0,
                     body_tilt=0, head_tilt=0,
                     hair_lift=0, hair_trail_angle=0,
                     hoodie_flare=0, lean_forward=0,
                     arm_left_angle=-30, arm_right_angle=-150,
                     leg_left_spread=0, leg_right_spread=0,
                     show_hoodie_settle=False):
    """
    Draws Luma as a simplified geometric construction figure.
    ox, oy = center-bottom of figure
    scale = overall scale factor
    body_tilt = degrees (positive = tilt right)
    head_tilt = degrees (positive = tilt right)
    hair_lift = px additional hair height
    hair_trail_angle = degrees CCW (positive = lean back as in sprint)
    hoodie_flare = px of hoodie hem flare (secondary motion)
    lean_forward = px of forward lean at top of body
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

    # --- FEET ---
    fc = int(leg_w * 0.7)  # foot center offset
    # left foot
    lf_cx = ox - fc + leg_left_spread
    lf_cy = oy
    draw.ellipse([lf_cx - foot_w // 2, lf_cy - foot_h,
                  lf_cx + foot_w // 2, lf_cy],
                 fill=SHOE_DARK, outline=LINE_COLOR, width=lw)
    # right foot
    rf_cx = ox + fc + leg_right_spread
    rf_cy = oy
    draw.ellipse([rf_cx - foot_w // 2, rf_cy - foot_h,
                  rf_cx + foot_w // 2, rf_cy],
                 fill=SHOE_DARK, outline=LINE_COLOR, width=lw)

    # --- LEGS ---
    tilt_offset = int(math.tan(math.radians(body_tilt)) * leg_h)
    # left leg
    ll_top_x = ox - fc + leg_left_spread // 2 + tilt_offset
    ll_top_y = oy - leg_h
    draw.rectangle([ll_top_x - leg_w // 2, ll_top_y,
                    ll_top_x + leg_w // 2, oy - foot_h],
                   fill=PANTS_SAGE, outline=LINE_COLOR, width=lw)
    # right leg
    rl_top_x = ox + fc + leg_right_spread // 2 + tilt_offset
    rl_top_y = oy - leg_h
    draw.rectangle([rl_top_x - leg_w // 2, rl_top_y,
                    rl_top_x + leg_w // 2, oy - foot_h],
                   fill=PANTS_SAGE, outline=LINE_COLOR, width=lw)

    # --- BODY (hoodie) ---
    body_bottom_y = oy - leg_h + int(head_r * 0.3)
    body_top_y = body_bottom_y - body_h
    body_cx = ox + lean_forward + tilt_offset
    hw = body_w // 2 + hoodie_flare
    # A-line hoodie shape (trapezoid-ish)
    body_pts = [
        (body_cx - int(body_w * 0.45), body_top_y),
        (body_cx + int(body_w * 0.45), body_top_y),
        (body_cx + hw, body_bottom_y),
        (body_cx - hw, body_bottom_y),
    ]
    draw.polygon(body_pts, fill=HOODIE_ORANGE, outline=LINE_COLOR)
    draw.line([(body_cx - int(body_w * 0.45), body_top_y),
               (body_cx + int(body_w * 0.45), body_top_y)],
              fill=LINE_COLOR, width=lw)
    for pt in [(body_cx - hw, body_bottom_y), (body_cx + hw, body_bottom_y)]:
        draw.line([body_pts[2], body_pts[3]], fill=LINE_COLOR, width=lw)

    # pixel pattern hint on hoodie chest (3 tiny squares)
    for i, col in enumerate([PIXEL_CYAN, PIXEL_CYAN, (230, 80, 160)]):
        px = body_cx - 6 + i * 5
        py = body_top_y + int(body_h * 0.4)
        draw.rectangle([px, py, px + 3, py + 3], fill=col)

    # hoodie pocket bump
    draw.arc([body_cx - int(body_w * 0.25), body_bottom_y - int(head_r * 0.4),
              body_cx + int(body_w * 0.25), body_bottom_y + 4],
             start=200, end=340, fill=LINE_COLOR, width=lw - 1)

    # --- ARMS ---
    arm_l = int(head_r * 1.35)
    arm_w = int(head_r * 0.35)
    shoulder_y = body_top_y + int(body_h * 0.18)
    # left arm
    la_angle = math.radians(arm_left_angle)
    la_ex = body_cx - int(body_w * 0.40) + int(arm_l * math.cos(la_angle))
    la_ey = shoulder_y + int(arm_l * math.sin(la_angle))
    draw.line([(body_cx - int(body_w * 0.40), shoulder_y),
               (la_ex, la_ey)], fill=HOODIE_ORANGE, width=int(arm_w * 1.2))
    draw.line([(body_cx - int(body_w * 0.40), shoulder_y),
               (la_ex, la_ey)], fill=LINE_COLOR, width=lw)
    draw.ellipse([la_ex - arm_w // 2, la_ey - arm_w // 2,
                  la_ex + arm_w // 2, la_ey + arm_w // 2],
                 fill=SKIN_MID, outline=LINE_COLOR, width=lw - 1)
    # right arm
    ra_angle = math.radians(arm_right_angle)
    ra_ex = body_cx + int(body_w * 0.40) + int(arm_l * math.cos(ra_angle))
    ra_ey = shoulder_y + int(arm_l * math.sin(ra_angle))
    draw.line([(body_cx + int(body_w * 0.40), shoulder_y),
               (ra_ex, ra_ey)], fill=HOODIE_ORANGE, width=int(arm_w * 1.2))
    draw.line([(body_cx + int(body_w * 0.40), shoulder_y),
               (ra_ex, ra_ey)], fill=LINE_COLOR, width=lw)
    draw.ellipse([ra_ex - arm_w // 2, ra_ey - arm_w // 2,
                  ra_ex + arm_w // 2, ra_ey + arm_w // 2],
                 fill=SKIN_MID, outline=LINE_COLOR, width=lw - 1)

    # --- HEAD ---
    neck_h = int(head_r * 0.12)
    head_cx = body_cx + int(math.tan(math.radians(head_tilt + body_tilt * 0.5)) * head_r)
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
    # trail angle shifts hair mass
    hair_dx = int(math.tan(math.radians(hair_trail_angle)) * hair_mass_h * 0.7)
    hair_cx = head_cx + hair_dx
    # hair shape: roughly ellipse-ish with bumps
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
        # draw dashed curved line below hoodie hem to show delayed follow-through
        for i in range(0, 16, 2):
            a_start = 190 + i * 10
            a_end = a_start + 9
            draw.arc([body_cx - hw - 4, body_bottom_y - 6,
                      body_cx + hw + 4, body_bottom_y + 16],
                     start=a_start, end=a_end,
                     fill=MOTION_ARROW, width=2)

    return head_cx, head_cy, head_r, body_cx, body_bottom_y, hw, body_top_y, shoulder_y


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

    hcx, hcy, hr, bcx, bby, hw, bty, shy = draw_luma_figure(
        draw, fig_x, fig_y, scale=1.05,
        body_tilt=4, head_tilt=8,
        arm_left_angle=-20, arm_right_angle=-160,
        show_hoodie_settle=True
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

    # timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y), "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Body shift: beat 1", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Head tilt: beat 1.5", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 37), "Hoodie settle: beat 3", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 49), "Return: beat 4 → loop", fill=BEAT_COLOR)


def draw_panel1_sprint_anticipation(img, draw):
    """Panel 1: Sprint Anticipation — weight forward, hair pre-trail."""
    col = 1
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "SPRINT ANTICIPATION", "beat: 0-1 (2-frame hold)")

    fig_x = px + PANEL_W // 2 - 10
    fig_y = py + PANEL_H - 50

    hcx, hcy, hr, bcx, bby, hw, bty, shy = draw_luma_figure(
        draw, fig_x, fig_y, scale=1.05,
        body_tilt=-10, head_tilt=-8,
        hair_lift=4, hair_trail_angle=-12,
        lean_forward=-12,
        arm_left_angle=-45, arm_right_angle=-135,
        leg_left_spread=-8, leg_right_spread=8
    )

    # ground line
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)],
              fill=ACCENT_DASH, width=1)

    # body lean annotation
    draw_arrow(draw, bcx, bty + 10, bcx - 20, bty - 5, color=MOTION_ARROW, width=2)
    draw.text((px + 8, py + PANEL_H - 105), "-10° torso lean", fill=MOTION_ARROW)

    # hair pre-trail annotation
    draw_arrow(draw, hcx - hr, hcy - hr, hcx - hr - 20, hcy - hr - 8,
               color=MOTION_ARROW, width=2)
    draw.text((px + 8, py + PANEL_H - 90), "hair: -12° pre-lean", fill=MOTION_ARROW)
    draw.text((px + 8, py + PANEL_H - 78), "(NOT yet trailing)", fill=ACCENT_DASH)

    # wide stance indicator
    draw.text((px + 8, py + PANEL_H - 66), "wide stance (1.15×)", fill=BEAT_COLOR)

    # timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y), "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Beat 0: neutral", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Beat 1: ANTICIPATION", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 37), "  — torso dips fwd", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 49), "  — arms back (load)", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 61), "  — hair barely moves", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 73), "Beat 2: LAUNCH", fill=(220, 60, 20))

    # action line
    draw.line([(bcx + 20, bty + 15), (bcx + 50, py + PANEL_H - 60)],
              fill=(180, 120, 80), width=1)
    draw.text((bcx + 22, bty + 20), "action", fill=(180, 120, 80))
    draw.text((bcx + 22, bty + 30), "line →", fill=(180, 120, 80))


def draw_panel2_discovery(img, draw):
    """Panel 2: Discovery reaction — full-body recoil + lean-in (2 beats shown)."""
    col = 2
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "DISCOVERY REACTION", "beat A: recoil | beat B: lean-in")

    # Beat A — RECOIL (left half of panel)
    fa_x = px + PANEL_W // 4
    fig_y = py + PANEL_H - 50

    hcx_a, hcy_a, hr, bcx_a, bby, hw, bty, shy = draw_luma_figure(
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
    hcx_b, hcy_b, hr2, bcx_b, bby2, hw2, bty2, shy2 = draw_luma_figure(
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

    hcx, hcy, hr, bcx, bby, hw, bty, shy = draw_luma_figure(
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
    draw.text((PAD, 8), "LUMA — Motion Spec Sheet v001", fill=LABEL_TEXT)
    draw.text((PAD, 22), "RYO HASEGAWA  |  Luma & the Glitchkin  |  C37", fill=(180, 165, 140))
    # legend strip
    legend_x = W - 280
    draw.rectangle([legend_x - 6, 6, legend_x + 270, PAD + 36], fill=(70, 55, 42))
    draw.text((legend_x, 8), "→  Secondary motion", fill=MOTION_ARROW)
    draw.text((legend_x, 20), "■  Timing beats", fill=BEAT_COLOR)
    draw.text((legend_x + 140, 8), "—  Ground/construction", fill=ACCENT_DASH)
    draw.text((legend_x + 140, 20), "○  Settled position", fill=ANNOTATION_BG)

    draw_panel0_idle(img, draw)
    draw_panel1_sprint_anticipation(img, draw)
    draw_panel2_discovery(img, draw)
    draw_panel3_landing(img, draw)

    # enforce ≤1280px
    img.thumbnail((1280, 1280), Image.LANCZOS)

    out_dir = "/home/wipkat/team/output/characters/motion"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_luma_motion_v001.png")
    img.save(out_path)
    print(f"Saved: {out_path} ({img.width}×{img.height}px)")


if __name__ == "__main__":
    main()
