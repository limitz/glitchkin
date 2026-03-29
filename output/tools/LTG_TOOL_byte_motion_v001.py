"""
LTG_TOOL_byte_motion_v001.py
Ryo Hasegawa / Cycle 37 — renamed to LTG_TOOL_ prefix Cycle 38 (Kai Nakamura)
Motion Spec Sheet — BYTE
3 panels: Float/Hover | Surprise (squash+stretch) | Approach (tilt+glow)
Output: output/characters/motion/LTG_CHAR_byte_motion_v001.png
Canvas: 1280x720 (≤1280 limit)

NOTE: This is the canonical LTG_TOOL_ version.
      LTG_CHAR_byte_motion_v001.py is a forwarding stub pointing here.
"""

from PIL import Image, ImageDraw, ImageFilter
import os
import math
import random

# --- CANONICAL COLORS ---
BYTE_TEAL        = (  0, 212, 232)   # GL-01b — canonical body fill
BYTE_OUTLINE     = ( 30,  50,  55)   # dark teal-black outline
ELEC_CYAN        = (  0, 240, 255)   # glow / highlights
VOID_BLACK       = ( 10,  10,  20)   # deep void
HOT_MAGENTA      = (255,  45, 107)   # crack / right eye
CORRUPT_AMBER    = (200, 122,  32)   # outline/storm variant accent
UV_PURPLE        = (123,  47, 190)   # shadow/confetti
SOFT_GOLD        = (232, 201,  90)   # left eye (normal) — warm data
ANNOTATION_BG    = (230, 240, 245)   # cool-tinted panel background
PANEL_BORDER     = (140, 175, 185)
LABEL_BG         = ( 15,  30,  40)
LABEL_TEXT       = (230, 245, 248)
LINE_COLOR       = BYTE_OUTLINE
MOTION_ARROW     = (255,  45, 107)   # hot magenta for arrows
BEAT_COLOR       = (  0, 190, 215)   # cyan for beat text
ACCENT_DASH      = (150, 175, 185)
GLOW_CYAN        = (  0, 232, 248)

# --- CANVAS ---
W, H = 1280, 720
COLS, ROWS = 3, 1
PAD = 16
PANEL_W = (W - PAD * (COLS + 1)) // COLS
PANEL_H = H - PAD * 2 - 40


# ------------------------------------------------------------------ helpers

def panel_origin(col):
    x = PAD + col * (PANEL_W + PAD)
    y = PAD + 40
    return x, y


def draw_arrow(draw, x0, y0, x1, y1, color=MOTION_ARROW, width=2, head=8):
    draw.line([(x0, y0), (x1, y1)], fill=color, width=width)
    angle = math.atan2(y1 - y0, x1 - x0)
    for da in (-0.42, 0.42):
        ax = x1 - head * math.cos(angle + da)
        ay = y1 - head * math.sin(angle + da)
        draw.line([(x1, y1), (int(ax), int(ay))], fill=color, width=width)


def draw_glow_circle(img, cx, cy, radius, color, alpha_max=80):
    """Add a soft radial glow (blurred layer) onto img."""
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    r, g, b = color
    for step in range(3):
        r_step = radius - step * (radius // 4)
        a_step = alpha_max - step * (alpha_max // 3)
        if r_step > 0:
            gd.ellipse([cx - r_step, cy - r_step, cx + r_step, cy + r_step],
                       fill=(r, g, b, a_step))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=radius // 3))
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, glow)
    return img_rgba.convert("RGB")


def draw_pixel_confetti(draw, cx, cy, count=8, spread=22, color=BYTE_TEAL, seed=7):
    """Draw small pixel squares as hover mechanism / confetti."""
    rng = random.Random(seed)
    for _ in range(count):
        px = cx + rng.randint(-spread, spread)
        py = cy + rng.randint(-spread // 2, spread // 2)
        sz = rng.randint(2, 4)
        alpha_col = tuple(min(255, c + rng.randint(-30, 30)) for c in color)
        draw.rectangle([px, py, px + sz, py + sz], fill=alpha_col)


def draw_byte_body(img_or_draw, draw_obj, cx, cy, bw, bh,
                   tilt_deg=0, squash_x=1.0, squash_y=1.0,
                   glow_radius=0, glow_alpha=0, phase=0):
    """
    Draw Byte's oval body with limbs, face, and optional glow.
    cx, cy = center of oval
    bw, bh = half-axes (body width, height)
    tilt_deg = body tilt in degrees (positive = lean right/toward target)
    squash_x/y = squash-stretch multipliers on axes
    glow_radius = if > 0, adds a glow ring
    phase = 0 = normal / 1 = alarmed / 2 = approach-lean
    Returns: (cx, cy) for annotation use
    """
    is_img = hasattr(img_or_draw, 'convert')
    draw = draw_obj
    s = bw / 30  # scale factor

    actual_bw = int(bw * squash_x)
    actual_bh = int(bh * squash_y)

    # tilt offset for leaning (shifts top of oval)
    tilt_rad = math.radians(tilt_deg)
    tx = int(math.sin(tilt_rad) * actual_bh)

    # --- GLOW ---
    if glow_radius > 0 and is_img:
        img_or_draw = draw_glow_circle(img_or_draw, cx + tx // 2, cy,
                                       glow_radius, ELEC_CYAN, glow_alpha)
        draw = ImageDraw.Draw(img_or_draw)

    lw = max(2, int(2.2 * s))

    # --- BODY OVAL ---
    # approximate tilt with a shifted bounding box
    draw.ellipse([cx - actual_bw + tx, cy - actual_bh,
                  cx + actual_bw + tx, cy + actual_bh],
                 fill=BYTE_TEAL, outline=LINE_COLOR, width=lw)

    # HOT_MAGENTA crack scar (right side / viewer left)
    crack_x = cx - int(actual_bw * 0.55) + tx
    crack_y = cy - int(actual_bh * 0.3)
    draw.line([(crack_x, crack_y),
               (crack_x + int(6 * s), crack_y + int(8 * s)),
               (crack_x + int(3 * s), crack_y + int(14 * s))],
              fill=HOT_MAGENTA, width=max(1, lw - 1))

    # --- LIMBS ---
    limb_len = int(22 * s)
    limb_w = int(7 * s)
    tip_r = int(4 * s)
    arm_configs = [
        # (base_dx, base_dy, end_dx, end_dy) - relative to cx, cy
        (-int(actual_bw * 0.65) + tx, -int(actual_bh * 0.25), -int(actual_bw * 1.0) + tx, -int(actual_bh * 0.55)),  # left arm
        ( int(actual_bw * 0.65) + tx, -int(actual_bh * 0.25),  int(actual_bw * 1.0) + tx, -int(actual_bh * 0.55)),  # right arm
    ]
    if phase == 1:  # alarmed — arms wide+up
        arm_configs = [
            (-int(actual_bw * 0.65) + tx, -int(actual_bh * 0.15),
             -int(actual_bw * 1.3) + tx, -int(actual_bh * 0.75)),
            ( int(actual_bw * 0.65) + tx, -int(actual_bh * 0.15),
              int(actual_bw * 1.3) + tx, -int(actual_bh * 0.75)),
        ]
    elif phase == 2:  # approach — arms slightly forward
        arm_configs = [
            (-int(actual_bw * 0.6) + tx, -int(actual_bh * 0.2),
             -int(actual_bw * 0.85) + tx, -int(actual_bh * 0.1)),
            ( int(actual_bw * 0.6) + tx, -int(actual_bh * 0.2),
              int(actual_bw * 0.85) + tx, -int(actual_bh * 0.1)),
        ]

    for (bx, by, ex, ey) in arm_configs:
        draw.line([(cx + bx, cy + by), (cx + ex, cy + ey)],
                  fill=BYTE_TEAL, width=limb_w)
        draw.line([(cx + bx, cy + by), (cx + ex, cy + ey)],
                  fill=LINE_COLOR, width=lw)
        draw.ellipse([cx + ex - tip_r, cy + ey - tip_r,
                      cx + ex + tip_r, cy + ey + tip_r],
                     fill=BYTE_TEAL, outline=LINE_COLOR, width=lw - 1)

    # legs
    leg_configs = [
        (-int(actual_bw * 0.35) + tx, int(actual_bh * 0.6),
         -int(actual_bw * 0.45) + tx, int(actual_bh * 0.6) + limb_len),
        ( int(actual_bw * 0.35) + tx, int(actual_bh * 0.6),
          int(actual_bw * 0.45) + tx, int(actual_bh * 0.6) + limb_len),
    ]
    if phase == 1:  # alarmed — legs wide
        leg_configs = [
            (-int(actual_bw * 0.4) + tx, int(actual_bh * 0.6),
             -int(actual_bw * 0.65) + tx, int(actual_bh * 0.6) + limb_len),
            ( int(actual_bw * 0.4) + tx, int(actual_bh * 0.6),
              int(actual_bw * 0.65) + tx, int(actual_bh * 0.6) + limb_len),
        ]
    for (bx, by, ex, ey) in leg_configs:
        draw.line([(cx + bx, cy + by), (cx + ex, cy + ey)],
                  fill=BYTE_TEAL, width=limb_w)
        draw.line([(cx + bx, cy + by), (cx + ex, cy + ey)],
                  fill=LINE_COLOR, width=lw)
        draw.ellipse([cx + ex - tip_r, cy + ey - tip_r,
                      cx + ex + tip_r, cy + ey + tip_r],
                     fill=BYTE_TEAL, outline=LINE_COLOR, width=lw - 1)

    # pixel confetti below legs
    bottom_y = cy + int(actual_bh * 0.6) + limb_len + tip_r
    draw_pixel_confetti(draw, cx + tx // 2, bottom_y + 10, count=10, spread=actual_bw, seed=42 + phase)

    # floating gap marker
    draw.line([(cx - int(actual_bw * 0.3) + tx, bottom_y + 12),
               (cx + int(actual_bw * 0.3) + tx, bottom_y + 12)],
              fill=BEAT_COLOR, width=1)

    # --- FACE ---
    # Eyes: 5×5 pixel grid per spec
    eye_gap = int(actual_bw * 0.42)
    eye_y = cy - int(actual_bh * 0.1)
    pixel_sz = max(2, int(4 * s))

    if phase == 0:  # normal — left: soft_gold cross/dot, right: clean dot
        # Left eye (warm/organic)
        for ey_off in range(3):
            for ex_off in range(3):
                if (ey_off == 1 or ex_off == 1):
                    col = SOFT_GOLD
                else:
                    col = (20, 40, 45)
                draw.rectangle([cx - eye_gap + tx + ex_off * pixel_sz,
                                 eye_y + ey_off * pixel_sz,
                                 cx - eye_gap + tx + ex_off * pixel_sz + pixel_sz - 1,
                                 eye_y + ey_off * pixel_sz + pixel_sz - 1],
                                fill=col)
        # Right eye (cracked — per glyph spec)
        for ey_off in range(3):
            for ex_off in range(3):
                if ey_off == 0 and ex_off == 2:
                    col = HOT_MAGENTA  # crack pixel
                elif ey_off == 2 and ex_off == 0:
                    col = (20, 40, 45)  # dead zone
                else:
                    col = ELEC_CYAN
                draw.rectangle([cx + eye_gap + tx + ex_off * pixel_sz - pixel_sz,
                                 eye_y + ey_off * pixel_sz,
                                 cx + eye_gap + tx + ex_off * pixel_sz,
                                 eye_y + ey_off * pixel_sz + pixel_sz - 1],
                                fill=col)

    elif phase == 1:  # alarmed — warning triangle pixels
        # left eye: exclamation
        draw.rectangle([cx - eye_gap + tx + pixel_sz,
                         eye_y,
                         cx - eye_gap + tx + pixel_sz * 2 - 1,
                         eye_y + pixel_sz * 2 - 1], fill=SOFT_GOLD)
        draw.rectangle([cx - eye_gap + tx + pixel_sz,
                         eye_y + pixel_sz * 2 + 1,
                         cx - eye_gap + tx + pixel_sz * 2 - 1,
                         eye_y + pixel_sz * 3 - 1], fill=SOFT_GOLD)
        # right eye: triangle/alarm
        for pt in [(0, 2), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]:
            draw.rectangle([cx + eye_gap + tx + pt[0] * pixel_sz - pixel_sz * 2,
                             eye_y + pt[1] * pixel_sz,
                             cx + eye_gap + tx + pt[0] * pixel_sz - pixel_sz * 2 + pixel_sz - 1,
                             eye_y + pt[1] * pixel_sz + pixel_sz - 1],
                            fill=HOT_MAGENTA)

    elif phase == 2:  # approach — slightly intensified
        # left eye: bright warm dot cluster
        for ey_off in range(3):
            for ex_off in range(3):
                if ey_off == 1 and ex_off == 1:
                    col = (255, 230, 120)  # bright gold
                elif abs(ey_off - 1) + abs(ex_off - 1) <= 1:
                    col = SOFT_GOLD
                else:
                    col = (20, 40, 45)
                draw.rectangle([cx - eye_gap + tx + ex_off * pixel_sz,
                                 eye_y + ey_off * pixel_sz,
                                 cx - eye_gap + tx + ex_off * pixel_sz + pixel_sz - 1,
                                 eye_y + ey_off * pixel_sz + pixel_sz - 1],
                                fill=col)
        # right eye: brighter cyan
        for ey_off in range(3):
            for ex_off in range(3):
                if ey_off == 0 and ex_off == 2:
                    col = HOT_MAGENTA
                else:
                    col = (0, 255, 255) if (ey_off == 1 and ex_off == 1) else ELEC_CYAN
                draw.rectangle([cx + eye_gap + tx + ex_off * pixel_sz - pixel_sz,
                                 eye_y + ey_off * pixel_sz,
                                 cx + eye_gap + tx + ex_off * pixel_sz,
                                 eye_y + ey_off * pixel_sz + pixel_sz - 1],
                                fill=col)

    # mouth (grumpy line, slight variation by phase)
    mouth_y = cy + int(actual_bh * 0.35)
    mouth_w = int(actual_bw * 0.5)
    mouth_arc_start = 190 if phase == 0 else (165 if phase == 2 else 185)
    mouth_arc_end   = 350 if phase == 0 else (375 if phase == 2 else 355)
    draw.arc([cx - mouth_w + tx, mouth_y - int(actual_bh * 0.12),
              cx + mouth_w + tx, mouth_y + int(actual_bh * 0.12)],
             start=mouth_arc_start, end=mouth_arc_end,
             fill=LINE_COLOR, width=lw - 1)

    # antenna (small stub on top)
    ant_bx = cx + int(actual_bw * 0.2) + tx
    ant_by = cy - actual_bh
    ant_tip_x = ant_bx + int(4 * s)
    ant_tip_y = ant_by - int(12 * s)
    draw.line([(ant_bx, ant_by), (ant_tip_x, ant_tip_y)],
              fill=LINE_COLOR, width=lw - 1)
    draw.ellipse([ant_tip_x - int(3 * s), ant_tip_y - int(3 * s),
                  ant_tip_x + int(3 * s), ant_tip_y + int(3 * s)],
                 fill=SOFT_GOLD, outline=LINE_COLOR, width=max(1, lw - 1))

    return cx, cy, is_img and img_or_draw, draw


# ------------------------------------------------------------------ PANELS

def draw_panel_bg(draw, col, title, subtitle=""):
    px, py = panel_origin(col)
    draw.rectangle([px, py, px + PANEL_W, py + PANEL_H], fill=ANNOTATION_BG, outline=PANEL_BORDER, width=1)
    draw.rectangle([px, py + PANEL_H - 30, px + PANEL_W, py + PANEL_H], fill=LABEL_BG)
    draw.text((px + 6, py + PANEL_H - 24), title, fill=LABEL_TEXT)
    if subtitle:
        draw.text((px + 6, py + PANEL_H - 13), subtitle, fill=(150, 195, 210))


def draw_panel0_float(img, draw):
    """Panel 0: Float/Hover — up-down oscillation, pixel artifacts at extremes."""
    col = 0
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "FLOAT / HOVER", "0.5Hz oscillation, ±6px")

    # Draw 3 ghost positions showing oscillation arc
    center_x = px + PANEL_W // 2
    base_y = py + PANEL_H - 100
    bw, bh = 32, 28

    positions = [
        (center_x - 60, base_y - 0,   0.35,  "MID"),    # center neutral (ghost)
        (center_x,      base_y - 6,   1.0,   "TOP"),    # top of arc (full opacity)
        (center_x + 60, base_y + 6,   0.35,  "BOT"),    # bottom of arc (ghost)
    ]

    for i, (fx, fy, opacity, label) in enumerate(positions):
        # Ghost effect via lighter body color
        body_col = tuple(int(c * opacity + 230 * (1 - opacity)) for c in BYTE_TEAL)
        outline_col = tuple(int(c * opacity + 200 * (1 - opacity)) for c in LINE_COLOR)

        # simplified draw for ghosts
        draw.ellipse([fx - bw, fy - bh, fx + bw, fy + bh],
                     fill=body_col, outline=outline_col, width=2)

        # pixel artifacts at extremes (top and bottom)
        if label in ("TOP", "BOT"):
            artifact_col = ELEC_CYAN if label == "TOP" else UV_PURPLE
            seed = 10 if label == "TOP" else 20
            draw_pixel_confetti(draw, fx, fy + bh + 12, count=6,
                                spread=bw, color=artifact_col, seed=seed)
            draw.text((fx - 18, fy + bh + 30), f"pixel artifact\nat {label}", fill=artifact_col)

        # position label
        draw.text((fx - 10, fy - bh - 14), label, fill=BEAT_COLOR)

    # oscillation arc line
    pts_arc = []
    for i in range(25):
        t = i / 24
        arc_x = (positions[0][0] * (1 - t) + positions[2][0] * t)
        arc_y = positions[1][1] + (positions[2][1] - positions[1][1]) * math.sin(t * math.pi)
        pts_arc.append((int(arc_x), int(arc_y - bh - 20)))
    for i in range(len(pts_arc) - 1):
        draw.line([pts_arc[i], pts_arc[i + 1]], fill=ACCENT_DASH, width=1)

    # vertical oscillation arrows on primary figure (middle)
    fx, fy = positions[1][0], positions[1][1]
    draw_arrow(draw, fx + bw + 10, fy, fx + bw + 10, fy - 18, color=MOTION_ARROW)
    draw_arrow(draw, fx + bw + 22, fy, fx + bw + 22, fy + 18, color=MOTION_ARROW)
    draw.text((fx + bw + 28, fy - 8), "±6px", fill=MOTION_ARROW)

    # timing annotations
    timing_y = py + 8
    draw.text((px + 8, timing_y), "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "0.5Hz cycle (2 sec/loop)", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Up arc: 1.0 sec", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 37), "Down arc: 1.0 sec", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 49), "Pixel artifacts: top+bot", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 61), "extremes only (±6px)", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 73), "Ease in/out (no linear)", fill=ACCENT_DASH)

    # floating gap note
    draw.text((px + 8, py + PANEL_H - 66), "FLOAT GAP: 0.25 body-units", fill=ACCENT_DASH)
    draw.text((px + 8, py + PANEL_H - 55), "above any surface", fill=ACCENT_DASH)


def draw_panel1_surprise(img, draw):
    """Panel 1: Surprise — rapid expand (squash/stretch), then contract."""
    col = 1
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "SURPRISE", "squash 3f → stretch 2f → settle")

    center_x = px + PANEL_W // 2
    base_y = py + PANEL_H - 100

    # Show 4 states: neutral → squash → stretch → settle
    states = [
        # (x, y_center, bw, bh, squash_x, squash_y, label, phase, offset_y)
        (px + 40,            base_y - 10, 28, 26, 1.0, 1.0, "NEUTRAL",  0, 0),
        (center_x - 40,      base_y + 8,  38, 18, 1.35, 0.7, "SQUASH\n(3f)", 1, 8),
        (center_x + 40,      base_y - 20, 20, 38, 0.7,  1.45,"STRETCH\n(2f)", 0, -20),
        (px + PANEL_W - 45,  base_y - 4,  28, 26, 1.0, 1.0, "SETTLE",  0, 0),
    ]

    for (sx, sy, bw, bh, sq_x, sq_y, label, ph, yo) in states:
        actual_bw = int(bw * sq_x)
        actual_bh = int(bh * sq_y)
        draw.ellipse([sx - actual_bw, sy - actual_bh, sx + actual_bw, sy + actual_bh],
                     fill=BYTE_TEAL, outline=LINE_COLOR, width=2)
        # minimal face for readability
        draw_pixel_confetti(draw, sx, sy + actual_bh + 8, count=5, spread=actual_bw, seed=100)
        label_y = sy + actual_bh + 22
        for i, ln in enumerate(label.split("\n")):
            draw.text((sx - 22, label_y + i * 11), ln, fill=BEAT_COLOR)

    # transition arrows
    arrow_y = base_y - 5
    for i in range(len(states) - 1):
        x0 = states[i][0] + states[i][2] + 4
        x1 = states[i + 1][0] - states[i + 1][2] - 4
        draw_arrow(draw, x0, arrow_y, x1, arrow_y, color=MOTION_ARROW, width=2)

    # squash/stretch labels
    sq_x_state = states[1]
    draw_arrow(draw, sq_x_state[0], sq_x_state[1] - sq_x_state[3],
               sq_x_state[0], sq_x_state[1] - sq_x_state[3] - 16,
               color=ACCENT_DASH)
    draw.text((sq_x_state[0] + 6, sq_x_state[1] - sq_x_state[3] - 15),
              "−30% H", fill=ACCENT_DASH)
    draw_arrow(draw, sq_x_state[0] + sq_x_state[2] + 2, sq_x_state[1],
               sq_x_state[0] + sq_x_state[2] + 18, sq_x_state[1],
               color=ACCENT_DASH)
    draw.text((sq_x_state[0] + sq_x_state[2] + 20, sq_x_state[1] - 6),
              "+35% W", fill=ACCENT_DASH)

    st_x_state = states[2]
    draw_arrow(draw, st_x_state[0], st_x_state[1] - st_x_state[3] - 2,
               st_x_state[0], st_x_state[1] - st_x_state[3] - 18,
               color=MOTION_ARROW)
    draw.text((st_x_state[0] + 4, st_x_state[1] - st_x_state[3] - 18),
              "+45% H", fill=MOTION_ARROW)

    # timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y), "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Beat 0: neutral", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Beat 1 (3 frames): SQUASH", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 37), "  W+35%, H−30%", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 49), "Beat 1+3f (2 frames): STRETCH", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 61), "  H+45%, W−30%", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 73), "Beat 2+: settle to neutral", fill=ACCENT_DASH)
    draw.text((px + 8, timing_y + 85), "  (elastic ease out)", fill=ACCENT_DASH)

    # note: limbs trail during stretch
    draw.text((px + 8, py + PANEL_H - 55), "LIMBS lag 1 frame behind body", fill=MOTION_ARROW)
    draw.text((px + 8, py + PANEL_H - 44), "during squash & stretch", fill=MOTION_ARROW)


def draw_panel2_approach(img, draw):
    """Panel 2: Approach — tilt toward + glow intensification."""
    col = 2
    px, py = panel_origin(col)
    draw_panel_bg(draw, col, "APPROACH", "lean in + glow intensifies")

    # Show 3 states: neutral → start lean → full approach (glow peak)
    center_x = px + PANEL_W // 2
    base_y = py + PANEL_H - 110

    # State 1: neutral (far)
    s1_x = px + 55
    s1_y = base_y
    draw.ellipse([s1_x - 22, s1_y - 20, s1_x + 22, s1_y + 20],
                 fill=BYTE_TEAL, outline=LINE_COLOR, width=2)
    draw.text((s1_x - 18, s1_y + 24), "NEUTRAL", fill=BEAT_COLOR)
    draw.text((s1_x - 18, s1_y + 35), "tilt: 0°", fill=ACCENT_DASH)

    # State 2: beginning lean (toward right — toward Luma)
    s2_x = center_x
    s2_y = base_y
    bw2, bh2 = 26, 23
    tilt2 = -12
    tx2 = int(math.sin(math.radians(tilt2)) * bh2)
    draw.ellipse([s2_x - bw2 + tx2, s2_y - bh2,
                  s2_x + bw2 + tx2, s2_y + bh2],
                 fill=BYTE_TEAL, outline=LINE_COLOR, width=2)
    # glow layer (subtle)
    draw.ellipse([s2_x - bw2 - 6 + tx2, s2_y - bh2 - 6,
                  s2_x + bw2 + 6 + tx2, s2_y + bh2 + 6],
                 outline=ELEC_CYAN, width=1)
    draw.text((s2_x - 18, s2_y + 28), "LEAN", fill=BEAT_COLOR)
    draw.text((s2_x - 18, s2_y + 39), "tilt: −12°", fill=MOTION_ARROW)
    draw_arrow(draw, s2_x - bw2 + tx2 - 10, s2_y - 5,
               s2_x + bw2 + tx2 + 10, s2_y - 5, color=MOTION_ARROW)

    # State 3: full approach (big tilt + glow)
    s3_x = px + PANEL_W - 65
    s3_y = base_y - 8  # slightly higher (leaning forward lifts)
    bw3, bh3 = 30, 27
    tilt3 = -22
    tx3 = int(math.sin(math.radians(tilt3)) * bh3)
    # multi-ring glow
    for ring_r, ring_alpha in [(50, 30), (35, 50), (22, 70)]:
        draw.ellipse([s3_x - ring_r + tx3, s3_y - ring_r,
                      s3_x + ring_r + tx3, s3_y + ring_r],
                     outline=(*ELEC_CYAN, ring_alpha), width=1)
    draw.ellipse([s3_x - bw3 + tx3, s3_y - bh3,
                  s3_x + bw3 + tx3, s3_y + bh3],
                 fill=BYTE_TEAL, outline=LINE_COLOR, width=2)
    # bright eye glow dots
    for ex_off, col in [(-int(bw3 * 0.42), SOFT_GOLD), (int(bw3 * 0.42), ELEC_CYAN)]:
        draw.ellipse([s3_x + ex_off + tx3 - 4, s3_y - 3,
                      s3_x + ex_off + tx3 + 4, s3_y + 5],
                     fill=col)
    draw.text((s3_x - 22, s3_y + 32), "APPROACH", fill=MOTION_ARROW)
    draw.text((s3_x - 22, s3_y + 43), "tilt: −22°", fill=MOTION_ARROW)
    draw.text((s3_x - 22, s3_y + 54), "glow: PEAK", fill=ELEC_CYAN)

    # glow intensity progression bar
    bar_y = py + PANEL_H - 85
    draw.text((px + 8, bar_y), "GLOW INTENSITY:", fill=BEAT_COLOR)
    glow_states = [(s1_x, 0, "(none)"), (s2_x, 0.4, "40%"), (s3_x, 1.0, "100%")]
    for gx, level, label in glow_states:
        bar_w = int(50 * level)
        draw.rectangle([gx - 25, bar_y + 12, gx + 25, bar_y + 20],
                       fill=(30, 50, 60), outline=ACCENT_DASH, width=1)
        if bar_w > 0:
            glow_col = tuple(int(c * level) for c in ELEC_CYAN)
            draw.rectangle([gx - 25, bar_y + 12, gx - 25 + bar_w, bar_y + 20],
                           fill=glow_col)
        draw.text((gx - 14, bar_y + 22), label, fill=BEAT_COLOR)

    # timing block
    timing_y = py + 8
    draw.text((px + 8, timing_y), "TIMING", fill=LABEL_BG)
    draw.text((px + 8, timing_y + 13), "Beat 0: neutral (0° tilt, 0% glow)", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 25), "Beat 1: lean begins (−12°)", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 37), "  glow: 40% intensity", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 49), "Beat 2: full approach (−22°)", fill=BEAT_COLOR)
    draw.text((px + 8, timing_y + 61), "  glow: 100% (ELEC_CYAN halo)", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 73), "  pixel confetti multiplies ×2", fill=MOTION_ARROW)
    draw.text((px + 8, timing_y + 85), "  eye brightness peaks", fill=ACCENT_DASH)

    # tilt direction arrow (target side)
    draw_arrow(draw, s1_x + 30, base_y - 40, s3_x - 30, base_y - 40,
               color=ACCENT_DASH, width=1, head=6)
    draw.text((center_x - 24, base_y - 56), "target direction →", fill=ACCENT_DASH)

    draw.text((px + 8, py + PANEL_H - 44), "Glow halo: ELEC_CYAN, 3-ring falloff", fill=ELEC_CYAN)


# ------------------------------------------------------------------ MAIN

def main():
    img = Image.new("RGB", (W, H), color=(18, 28, 35))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, W, PAD + 40], fill=LABEL_BG)
    draw.text((PAD, 8), "BYTE — Motion Spec Sheet v001", fill=LABEL_TEXT)
    draw.text((PAD, 22), "RYO HASEGAWA  |  Luma & the Glitchkin  |  C37", fill=(120, 165, 180))
    # legend strip
    legend_x = W - 280
    draw.rectangle([legend_x - 6, 6, legend_x + 270, PAD + 36], fill=(20, 40, 55))
    draw.text((legend_x, 8), "→  Secondary motion", fill=MOTION_ARROW)
    draw.text((legend_x, 20), "■  Timing beats", fill=BEAT_COLOR)
    draw.text((legend_x + 140, 8), "—  Ground/construction", fill=ACCENT_DASH)
    draw.text((legend_x + 140, 20), "~  Glow intensity", fill=ELEC_CYAN)

    draw_panel0_float(img, draw)
    draw_panel1_surprise(img, draw)
    draw_panel2_approach(img, draw)

    # enforce ≤1280px
    img.thumbnail((1280, 1280), Image.LANCZOS)

    out_dir = "/home/wipkat/team/output/characters/motion"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_byte_motion_v001.png")
    img.save(out_path)
    print(f"Saved: {out_path} ({img.width}×{img.height}px)")


if __name__ == "__main__":
    main()
