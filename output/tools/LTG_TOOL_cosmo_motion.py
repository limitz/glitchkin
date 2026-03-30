# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_cosmo_motion.py
Ryo Hasegawa / Cycle 42
Motion Spec Sheet — COSMO
4 panels: Idle/Observing | Startled | Analysis Lean | Reluctant Move

Cosmo motion vocabulary:
  - Upright, contained, deliberate. Rectangularity in everything.
  - Arms hang close to body; notebook under left arm is a secondary-mass anchor.
  - Startled: glasses tilt worsens, BOTH arms jut briefly, then snap back.
  - Analysis lean: forward tilt 6–8° only; head tilts right; notebook out or open.
  - Reluctant move: body rigid, leans 10–12°, arm NOT pumping — notebook clutched.
  - Notebook secondary motion: lags body on all sudden shifts (+1.5 beat behind).
  - Glasses: neutral 7° CCW; Startled peak: 13–15°; Recovery to 9° by beat 3.

Canvas: 1280x720 (≤1280 limit)
Output: output/characters/motion/LTG_CHAR_cosmo_motion.png
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

# --- Load config (mirrors pattern from luma/byte motion tools) ---
_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "sheet_geometry_config.json")

def _load_header_h_cosmo(default=54):
    """Load HEADER_H for cosmo family from sheet_geometry_config.json."""
    try:
        import json
        with open(_CONFIG_PATH) as f:
            cfg = json.load(f)
        geo = cfg.get("families", {}).get("cosmo", {})
        return geo.get("panel_top_abs", default)
    except Exception:
        return default

_COSMO_PANEL_TOP = _load_header_h_cosmo(default=54)

# --- CANONICAL COLORS (from cosmo.md / cosmo_color_model.md) ---
SKIN            = (217, 192, 154)   # #D9C09A Light Warm Olive
SKIN_SH         = (184, 154, 120)   # #B89A78 Warm Sand
HAIR            = ( 26,  24,  36)   # #1A1824 Blue-Black
GLASS_FRAME     = ( 92,  58,  32)   # #5C3A20 Warm Espresso Brown
GLASS_LENS      = (238, 244, 255)   # #EEF4FF Ghost Blue
GLASS_GLARE     = (240, 240, 240)   # #F0F0F0 Static White
IRIS            = ( 61, 107,  69)   # #3D6B45 Warm Forest Green
PUPIL           = ( 59,  40,  32)   # #3B2820 Deep Cocoa
EYE_W           = (250, 240, 220)   # #FAF0DC Warm Cream
EYE_HL          = (240, 240, 240)   # Static White
STRIPE_A        = ( 91, 141, 184)   # #5B8DB8 Cerulean Blue
STRIPE_B        = (122, 158, 126)   # #7A9E7E Sage Green
PANTS           = (140, 136, 128)   # #8C8880 Warm Mid-Gray
PANTS_SH        = (106, 100,  96)   # Mid-Dark Gray
SHOE            = ( 92,  58,  32)   # #5C3A20 Warm Espresso
NOTEBOOK        = ( 91, 141, 184)   # #5B8DB8 Cerulean Blue (matches shirt stripe)
NOTEBOOK_SH     = ( 61, 107, 138)   # #3D6B8A Deep Cerulean (spine in shadow)
LINE_COLOR      = ( 59,  40,  32)   # #3B2820 Deep Cocoa
ANNOTATION_BG   = (248, 244, 238)   # warm cream
PANEL_BORDER    = (180, 165, 145)
LABEL_BG        = ( 50,  38,  28)
LABEL_TEXT      = (248, 244, 236)
MOTION_ARROW    = (220,  60,  20)   # orange — secondary motion (notebook, glasses)
BEAT_COLOR      = ( 80, 120, 200)   # blue — timing beats
ACCENT_DASH     = (200, 190, 175)   # construction/guide lines

# --- CANVAS ---
W, H  = 1280, 720
COLS  = 4
PAD   = 14
_TITLE_H   = max(_COSMO_PANEL_TOP - PAD, 40)
PANEL_W    = (W - PAD * (COLS + 1)) // COLS
PANEL_H    = H - PAD * 2 - _TITLE_H


# ------------------------------------------------------------------ helpers

def panel_origin(col):
    """Top-left (x, y) of panel col (0-based)."""
    x = PAD + col * (PANEL_W + PAD)
    y = _COSMO_PANEL_TOP
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


# ------------------------------------------------------------------ character drawing

def draw_stripe_shirt(draw, cx, top_y, bot_y, half_w, stripe_h=None, head_r=22):
    """Horizontal cerulean/sage stripes clipped to shirt zone."""
    if stripe_h is None:
        stripe_h = max(5, int(head_r * 0.22))
    y = top_y
    ci = 0
    cols = [STRIPE_A, STRIPE_B]
    while y < bot_y:
        end_y = min(y + stripe_h, bot_y)
        draw.rectangle([cx - half_w, y, cx + half_w, end_y], fill=cols[ci % 2])
        ci += 1
        y = end_y


def draw_glasses_tilt(draw, gx, gy, head_r, tilt_deg=7):
    """
    Draw Cosmo's glasses at given center, tilted tilt_deg CCW.
    gx, gy = center of glasses span.
    """
    lens_rx = int(head_r * 0.38)
    lens_ry = int(head_r * 0.28)
    sep     = int(head_r * 0.76)
    rad     = math.radians(tilt_deg)

    for side in [-1, 1]:
        # lens center shifted by tilt
        lx = gx + side * sep // 2 + int(side * sep // 2 * math.sin(rad) * 0.2)
        ly = gy + side * (sep // 2) * math.sin(rad) * 0.35

        draw.ellipse([lx - lens_rx, ly - lens_ry,
                      lx + lens_rx, ly + lens_ry], fill=GLASS_LENS)
        draw.ellipse([lx - lens_rx, ly - lens_ry,
                      lx + lens_rx, ly + lens_ry],
                     outline=GLASS_FRAME, width=5)
        # glare crescent
        draw.arc([lx - lens_rx + 3, ly - lens_ry + 3,
                  lx + lens_rx - 3, ly + lens_ry - 3],
                 start=200, end=340, fill=GLASS_GLARE, width=3)
        # eye behind glass
        ir = int(lens_rx * 0.50)
        draw.ellipse([lx - ir, ly - min(ir, lens_ry - 2),
                      lx + ir, ly + min(ir, lens_ry - 2)], fill=IRIS)
        draw.ellipse([lx - int(ir * 0.55), ly - int(ir * 0.55),
                      lx + int(ir * 0.55), ly + int(ir * 0.55)], fill=PUPIL)
        # upper-right highlight (Cosmo DNA)
        draw.ellipse([lx + int(ir * 0.08), ly - int(lens_ry * 0.48),
                      lx + int(ir * 0.08) + 6, ly - int(lens_ry * 0.48) + 6],
                     fill=EYE_HL)

    # nose bridge
    bridge_x0 = gx - sep // 2 + lens_rx - 2
    bridge_x1 = gx + sep // 2 - lens_rx + 2
    draw.line([bridge_x0, gy, bridge_x1, gy], fill=GLASS_FRAME, width=4)

    # temple arms
    for side in [-1, 1]:
        lx = gx + side * sep // 2 + int(side * sep // 2 * math.sin(rad) * 0.2)
        draw.line([lx + side * lens_rx, gy,
                   lx + side * (lens_rx + int(head_r * 0.40)), gy - int(head_r * 0.08)],
                  fill=GLASS_FRAME, width=4)


def draw_cosmo_figure(draw, ox, oy, head_r=24,
                      body_tilt=0, head_tilt=0,
                      glasses_tilt=7,
                      arm_right_angle=-25,  # right arm (viewer's left) — notebook side
                      arm_left_angle=-155,  # left arm (viewer's right)
                      notebook_tucked=True,
                      notebook_out=False,
                      leg_spread=0):
    """
    Draw Cosmo as a geometric construction figure.
    ox, oy = center-bottom of figure.
    Cosmo is 4.0 heads tall.
    Notebook tucked under right arm (viewer's LEFT = Cosmo's LEFT = notebook side).
    NOTE: In frontal view, Cosmo's LEFT arm (which holds notebook) is on VIEWER'S RIGHT.
          But spec says notebook is tucked under left arm. We draw notebook on viewer's RIGHT.
    body_tilt: degrees (positive = tilt viewer's right)
    """
    s = 1.0
    hr  = head_r              # head radius (half-height)
    hw  = int(hr * 0.86)      # head half-width (rect: w = 0.86 h units)
    cr  = int(hr * 0.12)      # corner radius

    body_h  = int(hr * 2.4)   # slim torso (Cosmo: 1.2 heads)
    body_w  = int(hr * 0.74)  # narrow (torso_w = 0.95 × head_w → ≈ 0.82 hr)
    neck_h  = int(hr * 0.20)
    leg_h   = int(hr * 1.70)  # 4.0 heads total: 1.0 head + 0.1 neck + 1.2 torso + 0.8+0.9 legs
    leg_w   = int(hr * 0.40)
    foot_w  = int(hr * 0.72)
    foot_h  = int(hr * 0.28)

    lw = 3
    tilt_off = int(math.tan(math.radians(body_tilt)) * body_h)

    # --- FEET ---
    fc = int(leg_w * 0.8)
    lf_cx = ox - fc - leg_spread
    rf_cx = ox + fc + leg_spread
    fy     = oy
    # left foot (viewer's right → notebook side)
    draw.ellipse([lf_cx - foot_w // 2, fy - foot_h,
                  lf_cx + foot_w // 2, fy], fill=SHOE, outline=LINE_COLOR, width=lw)
    # right foot
    draw.ellipse([rf_cx - foot_w // 2, fy - foot_h,
                  rf_cx + foot_w // 2, fy], fill=SHOE, outline=LINE_COLOR, width=lw)

    # --- LEGS ---
    leg_top_y = oy - leg_h
    # left leg
    ll_cx = ox - fc - leg_spread // 2
    draw.rectangle([ll_cx - leg_w // 2 + tilt_off // 2, leg_top_y,
                    ll_cx + leg_w // 2 + tilt_off // 2, oy - foot_h],
                   fill=PANTS, outline=LINE_COLOR, width=lw)
    # right leg
    rl_cx = ox + fc + leg_spread // 2
    draw.rectangle([rl_cx - leg_w // 2 + tilt_off // 2, leg_top_y,
                    rl_cx + leg_w // 2 + tilt_off // 2, oy - foot_h],
                   fill=PANTS, outline=LINE_COLOR, width=lw)

    # --- TORSO (striped shirt) ---
    body_bot_y = oy - leg_h + int(hr * 0.5)
    body_top_y = body_bot_y - body_h
    body_cx    = ox + tilt_off
    draw_stripe_shirt(draw, body_cx, body_top_y, body_bot_y, body_w, head_r=hr)
    draw.rectangle([body_cx - body_w, body_top_y,
                    body_cx + body_w, body_bot_y],
                   outline=LINE_COLOR, width=lw)

    # Belt (thin dark strip)
    belt_y = body_bot_y - int(hr * 0.18)
    draw.rectangle([body_cx - body_w, belt_y,
                    body_cx + body_w, belt_y + int(hr * 0.10)],
                   fill=GLASS_FRAME, outline=LINE_COLOR, width=2)

    # --- SHOULDER MARKERS (geometry anchor) ---
    shoulder_y = body_top_y + int(hr * 0.18)
    shoulder_r = 4
    for sx in [body_cx - body_w, body_cx + body_w]:
        draw.ellipse([sx - shoulder_r, shoulder_y - shoulder_r,
                      sx + shoulder_r, shoulder_y + shoulder_r],
                     fill=ACCENT_DASH, outline=LINE_COLOR, width=1)

    # --- ARMS ---
    arm_h  = int(hr * 1.80)
    arm_w  = int(hr * 0.28)

    # Right arm (viewer's left)
    ang_r = math.radians(arm_right_angle)
    ar_ex = body_cx - body_w + int(arm_h * math.cos(ang_r))
    ar_ey = shoulder_y + int(arm_h * math.sin(-ang_r))  # flip y
    draw.rectangle([min(body_cx - body_w, ar_ex) - arm_w // 2,
                    shoulder_y,
                    max(body_cx - body_w, ar_ex) + arm_w // 2,
                    ar_ey + arm_w // 2],
                   fill=STRIPE_A, outline=LINE_COLOR, width=lw)

    # Left arm (viewer's right) — notebook arm
    ang_l = math.radians(arm_left_angle)
    al_ex = body_cx + body_w + int(arm_h * math.cos(ang_l))
    al_ey = shoulder_y + int(arm_h * math.sin(-ang_l))
    draw.rectangle([min(body_cx + body_w, al_ex) - arm_w // 2,
                    shoulder_y,
                    max(body_cx + body_w, al_ex) + arm_w // 2,
                    al_ey + arm_w // 2],
                   fill=STRIPE_A, outline=LINE_COLOR, width=lw)

    # --- NOTEBOOK ---
    nb_w  = int(hr * 0.36)   # notebook width
    nb_h  = int(hr * 0.56)   # notebook height (slim field notebook)
    if notebook_out:
        # Notebook extended forward (analysis mode — Cosmo consulting it)
        nb_cx = body_cx + body_w + arm_w + nb_w // 2 + 6
        nb_cy = body_bot_y - int(hr * 0.50)
    else:
        # Notebook tucked under left arm (viewer's right)
        nb_cx = body_cx + body_w + arm_w // 2 + nb_w // 2 + 4
        nb_cy = shoulder_y + arm_h // 2 + nb_h // 2
    nb_top  = nb_cy - nb_h // 2
    nb_bot  = nb_cy + nb_h // 2
    draw.rectangle([nb_cx - nb_w, nb_top, nb_cx, nb_bot],
                   fill=NOTEBOOK, outline=LINE_COLOR, width=2)
    # Spine (darker left edge)
    draw.rectangle([nb_cx - nb_w, nb_top, nb_cx - nb_w + 5, nb_bot],
                   fill=NOTEBOOK_SH)
    # Page edge (right side when open slightly)
    draw.line([nb_cx - 2, nb_top + 3, nb_cx - 2, nb_bot - 3],
              fill=EYE_W, width=2)

    # --- NECK ---
    neck_top  = body_top_y - neck_h
    neck_bot  = body_top_y
    neck_w    = int(hr * 0.22)
    neck_cx   = body_cx
    draw.rectangle([neck_cx - neck_w, neck_top,
                    neck_cx + neck_w, neck_bot],
                   fill=SKIN, outline=LINE_COLOR, width=lw)

    # --- HEAD (rectangular with rounded corners) ---
    # head_tilt: small head rotation relative to body
    head_cx = neck_cx + int(math.tan(math.radians(head_tilt)) * hr * 0.5)
    head_bot = neck_top
    head_top = head_bot - int(hr * 2.0)
    head_cy  = (head_top + head_bot) // 2
    corner_r = cr

    # Rounded-rect fill
    draw.rectangle([head_cx - hw + corner_r, head_top,
                    head_cx + hw - corner_r, head_bot], fill=SKIN)
    draw.rectangle([head_cx - hw, head_top + corner_r,
                    head_cx + hw, head_bot - corner_r], fill=SKIN)
    for (ox2, oy2) in [(head_cx - hw + corner_r, head_top + corner_r),
                       (head_cx + hw - corner_r, head_top + corner_r),
                       (head_cx - hw + corner_r, head_bot - corner_r),
                       (head_cx + hw - corner_r, head_bot - corner_r)]:
        draw.ellipse([ox2 - corner_r, oy2 - corner_r,
                      ox2 + corner_r, oy2 + corner_r], fill=SKIN)

    # Outline
    draw.line([head_cx - hw + corner_r, head_top,
               head_cx + hw - corner_r, head_top], fill=LINE_COLOR, width=lw)
    draw.line([head_cx - hw + corner_r, head_bot,
               head_cx + hw - corner_r, head_bot], fill=LINE_COLOR, width=lw)
    draw.line([head_cx - hw, head_top + corner_r,
               head_cx - hw, head_bot - corner_r], fill=LINE_COLOR, width=lw)
    draw.line([head_cx + hw, head_top + corner_r,
               head_cx + hw, head_bot - corner_r], fill=LINE_COLOR, width=lw)
    for (ox2, oy2, a0, a1) in [(head_cx - hw + corner_r, head_top + corner_r, 180, 270),
                                (head_cx + hw - corner_r, head_top + corner_r, 270, 360),
                                (head_cx - hw + corner_r, head_bot - corner_r, 90, 180),
                                (head_cx + hw - corner_r, head_bot - corner_r, 0, 90)]:
        draw.arc([ox2 - corner_r, oy2 - corner_r, ox2 + corner_r, oy2 + corner_r],
                 start=a0, end=a1, fill=LINE_COLOR, width=lw)

    # --- HAIR (minimal flat cap) ---
    hair_top_y = head_top - int(hr * 0.12)
    draw.rectangle([head_cx - hw + 3, hair_top_y,
                    head_cx + hw - 3, head_top + 4], fill=HAIR)
    # Cowlick (right side, viewer's left)
    draw.ellipse([head_cx + int(hw * 0.50), hair_top_y - int(hr * 0.06),
                  head_cx + int(hw * 0.92), hair_top_y + int(hr * 0.15)], fill=HAIR)

    # --- FACE FEATURES ---
    face_cy = head_cy + int(hr * 0.05)
    # Eyebrows (slightly arched, horizontal-ish — analytical)
    brow_y = face_cy - int(hr * 0.42)
    brow_sep = int(hw * 0.52)
    for side in [-1, 1]:
        bx = head_cx + side * brow_sep
        draw.line([bx - int(hw * 0.22), brow_y + (2 if side == 1 else 0),
                   bx + int(hw * 0.22), brow_y - 2],
                  fill=HAIR, width=3)

    # Nose (simple arc)
    draw.arc([head_cx - int(hr * 0.08), face_cy + int(hr * 0.12),
              head_cx + int(hr * 0.08), face_cy + int(hr * 0.28)],
             start=135, end=305, fill=LINE_COLOR, width=3)

    # Mouth (reserved — flat to slight uptick)
    draw.arc([head_cx - int(hw * 0.28), face_cy + int(hr * 0.28),
              head_cx + int(hw * 0.28), face_cy + int(hr * 0.52)],
             start=15, end=165, fill=LINE_COLOR, width=3)

    # Glasses (drawn OVER eyes)
    draw_glasses_tilt(draw, head_cx, face_cy - int(hr * 0.08), hr, tilt_deg=glasses_tilt)

    return (head_cx, head_cy, hr, body_cx, body_bot_y, body_w,
            body_top_y, shoulder_y, nb_cx, nb_cy, nb_h)


# ------------------------------------------------------------------ PANEL DRAWING

def draw_panel_bg(draw, col, title, subtitle="", beat_label=""):
    px, py = panel_origin(col)
    draw.rectangle([px, py, px + PANEL_W, py + PANEL_H],
                   fill=ANNOTATION_BG, outline=PANEL_BORDER, width=1)
    draw.rectangle([px, py + PANEL_H - 30, px + PANEL_W, py + PANEL_H], fill=LABEL_BG)
    draw.text((px + 6, py + PANEL_H - 24), title, fill=LABEL_TEXT)
    if subtitle:
        draw.text((px + 6, py + PANEL_H - 13), subtitle, fill=(200, 190, 170))
    # Beat badge: colored box top-left (required for lint check_beat_badges ≥15%)
    badge = beat_label or f"B{col + 1}"
    draw.rectangle([px + 3, py + 3, px + 36, py + 22], fill=BEAT_COLOR)
    draw.text((px + 6, py + 5), badge, fill=(240, 248, 255))


def draw_panel0_idle_observing(img, draw):
    """Panel 0: IDLE / OBSERVING — Cosmo neutral standing, notebook tucked, slight weight settle."""
    col = 0
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "IDLE / OBSERVING", "4-beat loop", beat_label="B1")

    fig_x = px + PANEL_W // 2 + 5   # slight right offset (notebook on viewer's right)
    fig_y = py + PANEL_H - 52

    (hcx, hcy, hr, bcx, bby, bw, bty, shy,
     nb_cx, nb_cy, nb_h) = draw_cosmo_figure(
        draw, fig_x, fig_y, head_r=24,
        body_tilt=1, head_tilt=3,
        glasses_tilt=7,
        arm_right_angle=-15, arm_left_angle=-165,
        notebook_tucked=True)
    draw = ImageDraw.Draw(img)

    # Ground line
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)], fill=ACCENT_DASH, width=1)
    draw.text((px + 14, fig_y + 3), "GROUND", fill=ACCENT_DASH)

    # Notebook annotation arrow (secondary motion lag)
    draw_arrow(draw, nb_cx - 5, nb_cy - nb_h // 2 - 4,
               nb_cx - 5, nb_cy - nb_h // 2 - 18,
               color=MOTION_ARROW, width=2, head=6)
    draw.text((nb_cx - 44, nb_cy - nb_h // 2 - 32), "notebook lag", fill=MOTION_ARROW)
    draw.text((nb_cx - 44, nb_cy - nb_h // 2 - 20), "+1.5 beats", fill=MOTION_ARROW)

    # Glasses tilt indicator
    draw.text((hcx + hr + 4, hcy - hr + 5), "7° CCW", fill=BEAT_COLOR)
    draw.text((hcx + hr + 4, hcy - hr + 17), "glasses tilt", fill=BEAT_COLOR)
    draw.text((hcx + hr + 4, hcy - hr + 29), "(neutral)", fill=BEAT_COLOR)

    # Upright construction line
    draw.line([(bcx, bty - hr * 2 - 12), (bcx, bby + 6)], fill=ACCENT_DASH, width=1)
    draw.text((bcx + 4, bty - hr), "CL", fill=ACCENT_DASH)

    # Timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y),      "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Weight shift:  beat 1", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Head settle:   beat 2", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 37), "Notebook lag:  beat 2.5", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 49), "Return:        beat 4 → loop", fill=BEAT_COLOR)


def draw_panel1_startled(img, draw):
    """Panel 1: STARTLED — glasses peak tilt, arms jut, notebook displaced."""
    col = 1
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "STARTLED", "beat 0 → peak beat 1 → snap back beat 2.5", beat_label="B2")

    fig_x = px + PANEL_W // 2 + 5
    fig_y = py + PANEL_H - 52

    # Peak startled pose: glasses tilt 14°, arms jutting out
    (hcx, hcy, hr, bcx, bby, bw, bty, shy,
     nb_cx, nb_cy, nb_h) = draw_cosmo_figure(
        draw, fig_x, fig_y, head_r=24,
        body_tilt=0, head_tilt=-4,   # slight head-back tilt
        glasses_tilt=14,              # glasses peak: +7° from neutral
        arm_right_angle=-40,          # right arm juts out
        arm_left_angle=-140,          # left arm juts out slightly
        notebook_tucked=True)
    draw = ImageDraw.Draw(img)

    # Ground line
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)], fill=ACCENT_DASH, width=1)

    # Glasses tilt annotation (peak state)
    label_box(draw, hcx - hr - 68, hcy - hr - 2, "14° PEAK",
              bg=(200, 80, 20), fg=(250, 244, 236))
    draw_arrow(draw, hcx - hr - 20, hcy - hr + 8, hcx - hr - 2, hcy - hr + 16,
               color=(200, 80, 20), width=2, head=6)

    # Glasses recovery arc (dashed annotation)
    draw.text((hcx + hr + 4, hcy - hr - 2), "recovery:", fill=BEAT_COLOR)
    draw.text((hcx + hr + 4, hcy - hr + 10), "14° → 9°", fill=BEAT_COLOR)
    draw.text((hcx + hr + 4, hcy - hr + 22), "by beat 3", fill=BEAT_COLOR)

    # Notebook jostled annotation
    draw_arrow(draw, nb_cx - 5, nb_cy, nb_cx + 12, nb_cy - 14,
               color=MOTION_ARROW, width=2, head=6)
    draw.text((nb_cx + 14, nb_cy - 22), "notebook", fill=MOTION_ARROW)
    draw.text((nb_cx + 14, nb_cy - 10), "jostled +1.5b", fill=MOTION_ARROW)

    # Arm-jut arrows
    draw_arrow(draw, bcx - bw - 8, shy + 10, bcx - bw - 26, shy + 24,
               color=MOTION_ARROW, width=2, head=6)

    # Timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y),      "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Glasses peak: beat 1", fill=(200, 80, 20))
    draw.text((px + 8, timing_y + 25), "Arms jut:     beat 1", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 37), "Notebook lag: beat 2.5", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 49), "Snap back:    beat 3", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 61), "Glasses norm: beat 4", fill=BEAT_COLOR)


def draw_panel2_analysis_lean(img, draw):
    """Panel 2: ANALYSIS LEAN — 6-8° forward tilt, head right, notebook extended."""
    col = 2
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "ANALYSIS LEAN", "2-beat approach, hold until answer", beat_label="B3")

    fig_x = px + PANEL_W // 2 + 5
    fig_y = py + PANEL_H - 52

    # Analysis pose: slight forward lean, head tilts right (toward subject of interest)
    (hcx, hcy, hr, bcx, bby, bw, bty, shy,
     nb_cx, nb_cy, nb_h) = draw_cosmo_figure(
        draw, fig_x, fig_y, head_r=24,
        body_tilt=-7, head_tilt=8,   # lean forward, head tips toward subject
        glasses_tilt=7,
        arm_right_angle=-12, arm_left_angle=-168,  # arms even closer — contained
        notebook_out=True)           # notebook extended (consulting it)
    draw = ImageDraw.Draw(img)

    # Ground line
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)], fill=ACCENT_DASH, width=1)

    # Body lean annotation
    draw_arrow(draw, bcx + 4, bty + 8, bcx - 16, bty - 6,
               color=MOTION_ARROW, width=2, head=6)
    draw.text((px + 8, py + PANEL_H - 80), "-7° torso lean", fill=MOTION_ARROW)
    draw.text((px + 8, py + PANEL_H - 68), "(controlled — NOT reckless)", fill=ACCENT_DASH)

    # Head tilt annotation
    draw_arrow(draw, hcx + hr, hcy - hr + 10, hcx + hr + 16, hcy + 2,
               color=BEAT_COLOR, width=2, head=6)
    draw.text((hcx + hr + 18, hcy - 8), "+8° head", fill=BEAT_COLOR)

    # Notebook-out annotation
    draw_arrow(draw, nb_cx - 2, nb_cy - nb_h // 2 - 5,
               nb_cx - 2, nb_cy - nb_h // 2 - 22,
               color=MOTION_ARROW, width=2, head=6)
    draw.text((nb_cx - 40, nb_cy - nb_h // 2 - 36), "notebook out", fill=MOTION_ARROW)
    draw.text((nb_cx - 40, nb_cy - nb_h // 2 - 24), "= ENGAGED", fill=MOTION_ARROW)

    # CG marker (stays over support polygon — contained lean)
    cg_x = bcx - 5
    cg_y = bty + (bby - bty) // 2
    draw.ellipse([cg_x - 5, cg_y - 5, cg_x + 5, cg_y + 5],
                 outline=BEAT_COLOR, width=2)
    draw.text((cg_x + 7, cg_y - 8), "CG", fill=BEAT_COLOR)

    # Timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y),      "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Lean init:    beat 1", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Head tilt:    beat 1.5", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 37), "Notebook out: beat 2", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 49), "HOLD:         until answer", fill=BEAT_COLOR)


def draw_panel3_reluctant_move(img, draw):
    """Panel 3: RELUCTANT MOVE — forward lean 10-12°, arms don't pump, notebook clutched."""
    col = 3
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "RELUCTANT MOVE", "beat 0: lean → beat 1: first step", beat_label="B4")

    fig_x = px + PANEL_W // 2 + 2
    fig_y = py + PANEL_H - 52

    # Reluctant run: notable forward lean but RIGID body (no loose secondary motion)
    # Arm does NOT pump — notebook arm stays clamped
    (hcx, hcy, hr, bcx, bby, bw, bty, shy,
     nb_cx, nb_cy, nb_h) = draw_cosmo_figure(
        draw, fig_x, fig_y, head_r=24,
        body_tilt=-12, head_tilt=-4,  # forward lean, head pulled slightly back (reluctant!)
        glasses_tilt=9,               # slight extra tilt from motion
        arm_right_angle=-10,          # arms barely move — NOT pumping
        arm_left_angle=-170,
        notebook_tucked=True,          # notebook CLUTCHED tight
        leg_spread=6)
    draw = ImageDraw.Draw(img)

    # Ground line
    draw.line([(px + 12, fig_y), (px + PANEL_W - 12, fig_y)], fill=ACCENT_DASH, width=1)

    # RIGID BODY marker — no secondary motion arrows on torso
    label_box(draw, px + 8, py + PANEL_H - 92, "RIGID TORSO",
              bg=(80, 60, 40), fg=(248, 230, 200))

    # Lean annotation
    draw_arrow(draw, bcx + 6, bty + 10, bcx - 22, bty - 8,
               color=MOTION_ARROW, width=2, head=7)
    draw.text((px + 8, py + PANEL_H - 110), "-12° lean (reluctant)", fill=MOTION_ARROW)

    # Head back-tilt (resisting the run)
    draw_arrow(draw, hcx - hr - 4, hcy - hr, hcx - hr - 18, hcy - hr - 8,
               color=BEAT_COLOR, width=2, head=6)
    draw.text((px + 8, py + PANEL_H - 132), "head trails -4° (resists)", fill=BEAT_COLOR)

    # Notebook clutched annotation
    draw_arrow(draw, nb_cx - 5, nb_cy, nb_cx - 18, nb_cy,
               color=MOTION_ARROW, width=2, head=6)
    draw.text((nb_cx - 80, nb_cy - 12), "CLUTCHED", fill=MOTION_ARROW)
    draw.text((nb_cx - 80, nb_cy), "notebook = stress", fill=MOTION_ARROW)

    # Contrast with Luma sprint reference
    draw.text((px + 8, py + PANEL_H - 155), "vs Luma sprint: arms pump;", fill=ACCENT_DASH)
    draw.text((px + 8, py + PANEL_H - 143), "Cosmo: arms LOCK", fill=ACCENT_DASH)

    # Timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y),      "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Lean: beat 1 (hard cut)", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "First step: beat 2", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 37), "NO arm pump — rigid", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 49), "Glasses: +2° per step", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 61), "Notebook lag: +1.5 beat", fill=MOTION_ARROW)


# ------------------------------------------------------------------ MAIN

def main():
    img = Image.new("RGB", (W, H), color=(238, 232, 222))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, W, PAD + 40], fill=LABEL_BG)
    draw.text((PAD, 8), "COSMO — Motion Spec Sheet v001", fill=LABEL_TEXT)
    draw.text((PAD, 22), "RYO HASEGAWA  |  Luma & the Glitchkin  |  C42", fill=(180, 165, 140))

    # Legend strip
    legend_x = W - 310
    draw.rectangle([legend_x - 6, 6, legend_x + 302, PAD + 36], fill=(70, 55, 42))
    draw.text((legend_x,       8), "->  Secondary motion (notebook, glasses)", fill=MOTION_ARROW)
    draw.text((legend_x,      20), "■  Timing beats", fill=BEAT_COLOR)
    draw.text((legend_x + 175, 8), "--  Construction/guide", fill=ACCENT_DASH)
    draw.text((legend_x + 175, 20), "o  CG / geometry anchor", fill=(200, 200, 200))

    draw_panel0_idle_observing(img, draw)
    draw_panel1_startled(img, draw)
    draw_panel2_analysis_lean(img, draw)
    draw_panel3_reluctant_move(img, draw)

    # enforce ≤1280px
    img.thumbnail((1280, 1280), Image.LANCZOS)

    out_dir = output_dir('characters', 'motion')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_cosmo_motion.png")
    img.save(out_path)
    print(f"Saved: {out_path} ({img.width}x{img.height}px)")


if __name__ == "__main__":
    main()
