#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_luma_construction_prototype.py
Luma Character Construction Prototype — v1.0.0
"Luma & the Glitchkin" — Cycle 50 / Maya Santos

PURPOSE: Side-by-side comparison of OLD (v014 geometric) vs NEW (organic curves) Luma
construction, using CURIOUS expression. This informs whether we rebuild all characters.

NEW CONSTRUCTION PRINCIPLES (derived from Hilda / Owl House / Kipo reference study):
  1. HEAD = 37% of total body height (was ~25%)
  2. EYES = 50% of face width, tall ovals (was ~22% of head height)
  3. ZERO straight lines on organic forms — dense polygon curves everywhere
  4. WEIGHT SHIFT in every pose: hip tilt, asymmetric shoulders, one foot planted
  5. TORSO = tapered organic shape (bean-like), not a rectangle
  6. LIMBS = tapered tubes with curve, not rectangles
  7. HANDS = rounded mittens with thumb bump, not plain ellipses
  8. SHOES = rounded organic shapes with visible curve, not sharp ellipses

Output: output/production/LTG_PROD_luma_construction_comparison.png (1280x720)
Left panel: OLD construction (simplified recreation of v014 method)
Right panel: NEW construction (organic curves prototype)

Author: Maya Santos
Date: 2026-03-30
Cycle: 50
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

from LTG_TOOL_curve_utils import quadratic_bezier_pts as _cu_quadratic, cubic_bezier_pts as _cu_cubic

# ── Palette (shared) ─────────────────────────────────────────────────────────
SKIN       = (200, 136, 90)
SKIN_SH    = (160, 104, 64)
SKIN_HL    = (223, 160, 112)
HAIR       = ( 26,  15, 10)
HAIR_HL    = ( 61,  31, 15)
EYE_W      = (250, 240, 220)
EYE_IRIS   = (200, 125, 62)
EYE_PUP    = ( 59,  40, 32)
EYE_HL     = (255, 255, 255)
BLUSH_C    = (232, 148, 100)
LINE       = ( 59,  40, 32)
HOODIE     = (150, 175, 200)   # CURIOUS cool blue-gray
HOODIE_SH  = (120, 145, 170)
HOODIE_HL  = (175, 198, 220)
PANTS      = ( 42,  40, 80)
PANTS_SH   = ( 26,  24, 48)
SHOE       = (245, 232, 208)
SHOE_SOLE  = (199,  91, 57)
LACES      = (  0, 240, 255)
PX_CYAN    = (  0, 240, 255)
PX_MAG     = (255,  45, 107)
CANVAS_BG  = (235, 224, 206)
PANEL_BG   = (230, 240, 235)   # CURIOUS soft warm mint

# ── Geometry helpers ─────────────────────────────────────────────────────────

def bezier3(p0, p1, p2, steps=48):
    """Delegates to curve_utils.quadratic_bezier_pts."""
    return _cu_quadratic(p0, p1, p2, steps=steps)


def bezier4(p0, p1, p2, p3, steps=60):
    """Delegates to curve_utils.cubic_bezier_pts."""
    return _cu_cubic(p0, p1, p2, p3, steps=steps)


def ellipse_points(cx, cy, rx, ry, steps=64, a0=0, a1=360):
    """Generate points along an elliptical arc."""
    pts = []
    for i in range(steps + 1):
        angle = math.radians(a0 + (a1 - a0) * i / steps)
        pts.append((cx + rx * math.cos(angle), cy + ry * math.sin(angle)))
    return pts


def polyline(draw, pts, color, width=2):
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill=color, width=width)


def smooth_polygon(draw, pts, fill=None, outline=None, width=1):
    """Draw a filled polygon from a list of points, then optional outline."""
    if fill:
        draw.polygon(pts, fill=fill)
    if outline:
        polyline(draw, pts + [pts[0]], outline, width)


def offset_curve(pts, dx, dy):
    """Shift all points by (dx, dy)."""
    return [(p[0] + dx, p[1] + dy) for p in pts]


def tube_polygon(centerline, w_start, w_end):
    """
    Build a filled polygon from a centerline with tapering width.
    Returns list of points tracing the left edge forward, then right edge backward.
    This creates a clean organic tube shape when drawn as a polygon.
    """
    n = len(centerline)
    if n < 2:
        return centerline
    left_edge = []
    right_edge = []
    for i in range(n):
        t = i / max(1, n - 1)
        w = w_start + (w_end - w_start) * t
        # Get perpendicular direction
        if i == 0:
            dx = centerline[1][0] - centerline[0][0]
            dy = centerline[1][1] - centerline[0][1]
        elif i == n - 1:
            dx = centerline[-1][0] - centerline[-2][0]
            dy = centerline[-1][1] - centerline[-2][1]
        else:
            dx = centerline[i+1][0] - centerline[i-1][0]
            dy = centerline[i+1][1] - centerline[i-1][1]
        length = math.sqrt(dx*dx + dy*dy) or 1.0
        # Perpendicular (rotated 90 degrees)
        nx = -dy / length
        ny = dx / length
        left_edge.append((centerline[i][0] + nx * w, centerline[i][1] + ny * w))
        right_edge.append((centerline[i][0] - nx * w, centerline[i][1] - ny * w))
    # Return left edge forward + right edge reversed = closed polygon
    return left_edge + right_edge[::-1]


# ══════════════════════════════════════════════════════════════════════════════
# OLD CONSTRUCTION (simplified recreation of v014 method)
# ══════════════════════════════════════════════════════════════════════════════

def draw_old_luma(img, ox, oy, panel_w, panel_h):
    """Recreate v014 Luma CURIOUS at small scale. Rectangle/ellipse construction."""
    draw = ImageDraw.Draw(img)

    # Scale factor for fitting into panel
    # Old Luma: head_r=52 at 1x, total ~8 head-radii tall
    # Character height ~ 416px at 1x. We fit into panel_h - 80 margin
    char_h = panel_h - 100
    s = char_h / 416.0

    cx = ox + panel_w // 2 - int(10 * s)  # slight offset for lean
    head_r = int(52 * s)
    hr = head_r

    # Head center Y: head at top
    head_cy = oy + 50 + head_r

    # ── Head: circle ──
    draw.ellipse([cx - hr, head_cy - hr, cx + hr, head_cy + hr + int(hr * 0.15)],
                 fill=SKIN, outline=LINE, width=max(2, int(3*s)))

    # ── Hair: overlapping dark ellipses (cloud) ──
    sc = hr / 100.0
    hair_els = [
        (-155, -195, 145, 40), (-175, -170, -80, -60), (-165, -140, -95, -30),
        (80, -160, 155, -60), (90, -130, 145, -40),
        (-60, -215, 20, -140), (-20, -225, 70, -145), (-100, -200, -30, -130),
    ]
    for (x1, y1, x2, y2) in hair_els:
        draw.ellipse([cx + int(x1*sc), head_cy + int(y1*sc),
                      cx + int(x2*sc), head_cy + int(y2*sc)], fill=HAIR)

    # ── Eyes: small, turnaround-aligned (ew = head_height * 0.22) ──
    ew = int(hr * 2 * 0.22)  # eye width
    eh = int(hr * 0.27)      # eye height
    eye_y = head_cy - int(18 * sc)
    for ex in [cx - int(38*sc), cx + int(38*sc)]:
        draw.ellipse([ex - ew//2, eye_y - eh, ex + ew//2, eye_y + eh],
                     fill=EYE_W, outline=LINE, width=max(1, int(2*s)))
        ir = int(ew * 0.30)
        draw.ellipse([ex - ir + int(4*s), eye_y - ir, ex + ir + int(4*s), eye_y + ir],
                     fill=EYE_IRIS)
        pr = int(ir * 0.50)
        draw.ellipse([ex - pr + int(4*s), eye_y - pr, ex + pr + int(4*s), eye_y + pr],
                     fill=EYE_PUP)

    # ── Nose: two dots ──
    draw.ellipse([cx - int(5*sc), head_cy + int(8*sc),
                  cx - int(2*sc), head_cy + int(14*sc)], fill=SKIN_SH)
    draw.ellipse([cx + int(2*sc), head_cy + int(8*sc),
                  cx + int(5*sc), head_cy + int(14*sc)], fill=SKIN_SH)

    # ── Mouth: gentle curve ──
    my = head_cy + int(30 * sc)
    mw = int(20 * sc)
    pts = bezier3((cx - mw, my), (cx, my - int(6*sc)), (cx + mw, my))
    polyline(draw, pts, LINE, width=max(1, int(2*s)))

    # ── Blush ──
    bw, bh = int(20*sc), int(10*sc)
    for bx_off in [-int(42*sc), int(42*sc)]:
        blush_x = cx + bx_off
        blush_y = head_cy + int(10*sc)
        blush_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        bd = ImageDraw.Draw(blush_img)
        bd.ellipse([blush_x - bw, blush_y - bh, blush_x + bw, blush_y + bh],
                   fill=(*BLUSH_C, 80))
        img = Image.alpha_composite(img, blush_img)
        draw = ImageDraw.Draw(img)

    # ── Neck: rectangle ──
    neck_y = head_cy + hr + int(hr * 0.10)
    neck_w = int(hr * 0.22)
    torso_top_y = neck_y + int(hr * 0.08)
    draw.rectangle([cx - neck_w, neck_y, cx + neck_w, torso_top_y + int(hr*0.05)],
                   fill=SKIN, outline=LINE, width=max(1, int(2*s)))

    # ── Torso: RECTANGLE with flat polygon ──
    torso_top_w = int(hr * 0.70)
    torso_bot_w = int(hr * 0.90)
    torso_h = int(hr * 2.10)
    torso_bot_y = torso_top_y + torso_h
    tilt = -int(hr * 0.22)  # CURIOUS lean

    torso_pts = [
        (cx + tilt - torso_top_w, torso_top_y),
        (cx + tilt + torso_top_w, torso_top_y),
        (cx + tilt//2 + torso_bot_w, torso_bot_y),
        (cx + tilt//2 - torso_bot_w, torso_bot_y),
    ]
    draw.polygon(torso_pts, fill=HOODIE, outline=LINE, width=max(1, int(2*s)))

    # Collar rectangle
    draw.rectangle([cx + tilt - torso_top_w + 4, torso_top_y,
                    cx + tilt + torso_top_w - 4, torso_top_y + int(hr * 0.18)],
                   fill=(250, 232, 200))

    # ── Arms: bezier tubes ──
    arm_w = int(hr * 0.28)
    # Left arm (raised for CURIOUS)
    ls_x = cx + tilt - torso_top_w + int(hr * 0.10)
    ls_y = torso_top_y + int(hr * 0.10)
    la_pts = bezier3((ls_x, ls_y),
                     (ls_x - int(hr*0.60) - int(hr*0.08), ls_y + int(hr*0.25)),
                     (ls_x - int(hr*1.20), ls_y - int(hr*0.20)))
    polyline(draw, la_pts, HOODIE, width=arm_w)
    polyline(draw, la_pts, LINE, width=max(1, int(2*s)))
    # hand
    hx, hy = la_pts[-1]
    hand_r = int(hr * 0.18)
    draw.ellipse([hx - hand_r, hy - hand_r, hx + hand_r, hy + hand_r],
                 fill=SKIN, outline=LINE, width=max(1, int(2*s)))

    # Right arm (hanging)
    rs_x = cx + tilt + torso_top_w - int(hr * 0.10)
    rs_y = torso_top_y + int(hr * 0.10)
    ra_pts = bezier3((rs_x, rs_y),
                     (rs_x + int(hr*0.10), rs_y + int(hr*0.50)),
                     (rs_x + int(hr*0.15), rs_y + int(hr*0.90)))
    polyline(draw, ra_pts, HOODIE, width=arm_w)
    polyline(draw, ra_pts, LINE, width=max(1, int(2*s)))
    hx, hy = ra_pts[-1]
    draw.ellipse([hx - hand_r, hy - hand_r, hx + hand_r, hy + hand_r],
                 fill=SKIN, outline=LINE, width=max(1, int(2*s)))

    # ── Legs: rectangles ──
    leg_w = int(hr * 0.38)
    pants_h = int(hr * 1.68)
    hip_cx = cx + tilt // 2
    for side, kdx, fdx in [(-1, -int(hr*0.20), -int(hr*0.20)),
                            (1, int(hr*0.10), int(hr*0.12))]:
        hip_x = hip_cx + side * int(hr * 0.42)
        knee_y = torso_bot_y + pants_h // 2
        foot_y = torso_bot_y + pants_h + int(hr * 0.30)
        # Upper leg: rectangle
        draw.rectangle([hip_x - leg_w//2, torso_bot_y,
                        hip_x + leg_w//2, knee_y],
                       fill=PANTS, outline=LINE, width=max(1, int(2*s)))
        # Lower leg: rectangle
        draw.rectangle([hip_x + kdx - leg_w//2, knee_y,
                        hip_x + fdx + leg_w//2, foot_y],
                       fill=PANTS, outline=LINE, width=max(1, int(2*s)))
        # Shoe
        shoe_w = int(hr * 0.40)
        shoe_h = int(hr * 0.22)
        draw.ellipse([hip_x + fdx - shoe_w, foot_y - int(hr*0.02),
                      hip_x + fdx + shoe_w, foot_y + shoe_h],
                     fill=SHOE, outline=LINE, width=max(1, int(2*s)))

    return img


# ══════════════════════════════════════════════════════════════════════════════
# NEW CONSTRUCTION (organic curves prototype)
# ══════════════════════════════════════════════════════════════════════════════

def draw_new_luma(img, ox, oy, panel_w, panel_h):
    """
    New Luma CURIOUS — organic curves construction.

    Key changes:
    - Head = 37% of body height (was ~25%)
    - Eyes = 50% of face width, tall ovals
    - All organic curves — tube_polygon for limbs, bezier outlines for torso
    - Weight on right leg, hip tilt, asymmetric shoulders
    - Bean-shaped torso, tapered limbs
    - Rounded mitten hands with thumb bump
    """
    draw = ImageDraw.Draw(img)

    # Character height to fit panel
    char_h = panel_h - 80
    total_h = char_h

    # NEW PROPORTIONS: head = 37% of total height
    head_h = int(total_h * 0.37)
    head_r = head_h // 2

    # Body height = remaining 63%
    body_h = total_h - head_h

    # Center with slight offset for weight shift
    cx = ox + panel_w // 2 + int(head_r * 0.05)
    head_cy = oy + 40 + head_r

    # Scale factor for detail sizing
    s = head_r / 100.0
    lw = max(3, int(3.5 * s))  # silhouette line weight
    lw2 = max(2, int(2.5 * s))  # interior line weight

    # ── WEIGHT SHIFT: hip tilt and asymmetric stance ──
    hip_tilt = int(5 * s)
    shoulder_tilt = -int(3 * s)

    # ══════════════════════════════════════════════════════════════════════
    # HEAD — Slightly wider than tall, organic shape with chin/cheek bumps
    # ══════════════════════════════════════════════════════════════════════
    head_rx = int(head_r * 1.06)
    head_ry = head_r

    # Build head outline with chin and cheek modulation
    final_head_pts = []
    for i in range(100):
        angle = math.radians(i * 360 / 100)
        r_base_x = head_rx
        r_base_y = head_ry
        # Chin: pull bottom-center down slightly, narrow slightly
        chin_f = max(0, math.cos(angle - math.pi / 2)) ** 2.5
        r_base_y += int(head_r * 0.10 * chin_f)
        r_base_x -= int(head_r * 0.04 * chin_f)
        # Cheek bumps at ~30 degrees below horizontal (both sides)
        for sign in [1, -1]:
            cheek_f = max(0, math.cos(angle - sign * 0.4)) ** 6
            r_base_x += int(head_r * 0.04 * cheek_f)
        px = cx + r_base_x * math.cos(angle)
        py = head_cy + r_base_y * math.sin(angle)
        final_head_pts.append((px, py))

    draw.polygon(final_head_pts, fill=SKIN)

    # ── HAIR: organic cloud — overlapping ellipses for BIG volume ──
    # Luma's signature: big, puffy cloud hair that extends well beyond head
    hair_blobs = [
        # Large base blobs for volume
        (0, -0.65, 0.70, 0.55),      # top center — BIG
        (-0.50, -0.50, 0.55, 0.50),  # left mass
        (0.50, -0.50, 0.55, 0.50),   # right mass
        # Upper extensions
        (-0.30, -0.95, 0.40, 0.35),  # upper left
        (0.30, -0.95, 0.40, 0.35),   # upper right
        (0, -1.10, 0.35, 0.30),      # very top
        # Side extensions (wider than head)
        (-0.85, -0.30, 0.35, 0.38),  # far left
        (0.85, -0.30, 0.35, 0.38),   # far right
        (-0.70, -0.60, 0.35, 0.32),  # left upper
        (0.70, -0.60, 0.35, 0.32),   # right upper
        # Fill gaps
        (-0.15, -0.45, 0.60, 0.42),  # center fill
        (0.15, -0.45, 0.60, 0.42),   # center fill
        (-0.50, -0.80, 0.32, 0.28),  # left gap
        (0.50, -0.80, 0.32, 0.28),   # right gap
        # Bumps on top for cloud effect
        (-0.45, -1.05, 0.25, 0.22),  # top bump L
        (0.45, -1.05, 0.25, 0.22),   # top bump R
        (0.15, -1.15, 0.22, 0.20),   # top bump C
    ]
    for (bx, by, brx, bry) in hair_blobs:
        hcx = cx + int(bx * head_rx)
        hcy = head_cy + int(by * head_ry)
        hrx = int(brx * head_rx)
        hry = int(bry * head_ry)
        draw.ellipse([hcx - hrx, hcy - hry, hcx + hrx, hcy + hry], fill=HAIR)

    # Hair highlight blobs (larger for visibility)
    for (bx, by, brx, bry) in [(-0.30, -0.85, 0.22, 0.13),
                                 (0.20, -0.72, 0.16, 0.10),
                                 (-0.55, -0.55, 0.14, 0.10)]:
        hcx = cx + int(bx * head_rx)
        hcy = head_cy + int(by * head_ry)
        hrx = int(brx * head_rx)
        hry = int(bry * head_ry)
        draw.ellipse([hcx - hrx, hcy - hry, hcx + hrx, hcy + hry], fill=HAIR_HL)

    # Redraw face area (skin over hair)
    face_cx = cx
    face_cy = head_cy + int(head_r * 0.10)
    face_rx = int(head_rx * 0.88)
    face_ry = int(head_ry * 0.70)
    face_pts = ellipse_points(face_cx, face_cy, face_rx, face_ry, steps=60)
    draw.polygon(face_pts, fill=SKIN)

    # Head outline
    polyline(draw, final_head_pts + [final_head_pts[0]], LINE, width=lw)

    # ══════════════════════════════════════════════════════════════════════
    # EYES — LARGE: each eye ~30% of head width, tall ovals
    # ══════════════════════════════════════════════════════════════════════
    eye_spacing = int(head_rx * 0.40)
    eye_y = head_cy + int(head_r * 0.05)
    eye_rx = int(head_rx * 0.28)
    eye_ry = int(head_ry * 0.32)

    for side in [-1, 1]:
        ex = cx + side * eye_spacing
        ey = eye_y + int(side * 3 * s * 0.06)  # tiny tilt

        # Eye white: slightly taller at bottom for appeal
        eye_pts = []
        for i in range(64):
            angle = math.radians(i * 360 / 64)
            rx_m = eye_rx * (1.0 + 0.03 * math.sin(angle))
            ry_m = eye_ry * (1.0 + 0.05 * math.sin(angle))
            eye_pts.append((ex + rx_m * math.cos(angle), ey + ry_m * math.sin(angle)))

        draw.polygon(eye_pts, fill=EYE_W)

        # Iris: large
        iris_r = int(eye_rx * 0.68)
        iris_ry = int(eye_ry * 0.62)
        gaze_dx = int(4 * s)   # CURIOUS: looking right
        gaze_dy = -int(2 * s)  # slightly up
        iris_cx = ex + gaze_dx
        iris_cy = ey + gaze_dy

        iris_pts = ellipse_points(iris_cx, iris_cy, iris_r, iris_ry, steps=40)
        draw.polygon(iris_pts, fill=EYE_IRIS)

        # Pupil
        pup_r = int(iris_r * 0.52)
        pup_ry = int(iris_ry * 0.52)
        draw.ellipse([iris_cx - pup_r, iris_cy - pup_ry,
                      iris_cx + pup_r, iris_cy + pup_ry], fill=EYE_PUP)

        # Highlight dots
        hl_r = max(int(pup_r * 0.42), 3)
        hl_x = iris_cx + int(iris_r * 0.32)
        hl_y = iris_cy - int(iris_ry * 0.32)
        draw.ellipse([hl_x - hl_r, hl_y - hl_r, hl_x + hl_r, hl_y + hl_r], fill=EYE_HL)
        hl2_r = max(int(hl_r * 0.45), 2)
        hl2_x = iris_cx - int(iris_r * 0.22)
        hl2_y = iris_cy + int(iris_ry * 0.18)
        draw.ellipse([hl2_x - hl2_r, hl2_y - hl2_r, hl2_x + hl2_r, hl2_y + hl2_r],
                     fill=(240, 240, 240))

        # Eye outline + upper lid (thick)
        polyline(draw, eye_pts + [eye_pts[0]], LINE, width=lw2)
        # Upper lid emphasis
        lid_pts = ellipse_points(ex, ey, eye_rx * 1.01, eye_ry * 0.97, steps=30, a0=195, a1=345)
        polyline(draw, lid_pts, LINE, width=lw)

        # Lower lash
        lower_pts = ellipse_points(ex, ey, eye_rx * 0.98, eye_ry * 1.01, steps=20, a0=15, a1=165)
        polyline(draw, lower_pts, LINE, width=lw2)

    # ── Brows ──
    for side, lift in [(-1, int(14*s)), (1, int(20*s))]:
        bx = cx + side * eye_spacing
        by = eye_y - eye_ry - int(6*s) - lift
        inner_x = bx + side * int(18*s)
        outer_x = bx - side * int(20*s)
        brow_pts = bezier3((outer_x, by + int(4*s)), (bx, by - int(4*s)),
                           (inner_x, by + int(2*s)), steps=24)
        polyline(draw, brow_pts, HAIR, width=lw)

    # ── Nose: minimal ──
    nose_y = head_cy + int(head_r * 0.28)
    nose_pts = bezier3((cx - int(4*s), nose_y), (cx, nose_y + int(3*s)),
                       (cx + int(3*s), nose_y - int(1*s)), steps=12)
    polyline(draw, nose_pts, SKIN_SH, width=lw2)

    # ── Mouth: CURIOUS — gentle smile ──
    mouth_y = head_cy + int(head_r * 0.44)
    mouth_w = int(head_rx * 0.30)
    mouth_pts = bezier3((cx - mouth_w, mouth_y + int(1*s)),
                        (cx, mouth_y - int(6*s)),
                        (cx + mouth_w, mouth_y - int(1*s)), steps=24)
    polyline(draw, mouth_pts, LINE, width=lw2)
    # Upturn at corners
    draw.line([(cx - mouth_w, mouth_y + int(1*s)),
               (cx - mouth_w - int(2*s), mouth_y - int(2*s))], fill=LINE, width=lw2)
    draw.line([(cx + mouth_w, mouth_y - int(1*s)),
               (cx + mouth_w + int(2*s), mouth_y - int(3*s))], fill=LINE, width=lw2)

    # ── Blush ──
    blush_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(blush_img)
    bw_s, bh_s = int(18*s), int(10*s)
    for boff in [-eye_spacing + int(3*s), eye_spacing - int(3*s)]:
        bd.ellipse([cx + boff - bw_s, head_cy + int(head_r*0.24) - bh_s,
                    cx + boff + bw_s, head_cy + int(head_r*0.24) + bh_s],
                   fill=(*BLUSH_C, 85))
    img = Image.alpha_composite(img, blush_img)
    draw = ImageDraw.Draw(img)

    # ══════════════════════════════════════════════════════════════════════
    # NECK — Short organic taper
    # ══════════════════════════════════════════════════════════════════════
    neck_top_y = head_cy + head_ry + int(head_r * 0.06)
    neck_bot_y = neck_top_y + int(head_r * 0.22)
    neck_wt = int(head_r * 0.25)
    neck_wb = int(head_r * 0.34)

    neck_l = bezier3((cx - neck_wt, neck_top_y), (cx - neck_wt - int(2*s), (neck_top_y+neck_bot_y)/2),
                     (cx - neck_wb, neck_bot_y), steps=12)
    neck_r = bezier3((cx + neck_wt, neck_top_y), (cx + neck_wt + int(2*s), (neck_top_y+neck_bot_y)/2),
                     (cx + neck_wb, neck_bot_y), steps=12)
    draw.polygon(neck_l + neck_r[::-1], fill=SKIN)

    # ══════════════════════════════════════════════════════════════════════
    # TORSO — Bean shape with organic S-curves, hip tilt, CURIOUS lean
    # ══════════════════════════════════════════════════════════════════════
    torso_top_y = neck_bot_y
    torso_h = int(body_h * 0.38)
    torso_bot_y = torso_top_y + torso_h
    lean_dx = -int(head_r * 0.12)  # CURIOUS lean left

    # Shoulder widths
    sh_w_l = int(head_r * 0.82)
    sh_w_r = int(head_r * 0.76)

    # Left side: shoulder down to left hip
    torso_l = bezier4(
        (cx + lean_dx - sh_w_l, torso_top_y + shoulder_tilt),
        (cx + lean_dx - sh_w_l - int(6*s), torso_top_y + torso_h * 0.35),
        (cx + lean_dx//2 - int(head_r*0.48), torso_bot_y - torso_h * 0.15),
        (cx + lean_dx//2 - int(head_r*0.52) + hip_tilt, torso_bot_y),
        steps=40
    )
    # Right side: right hip up to shoulder
    torso_r = bezier4(
        (cx + lean_dx//2 + int(head_r*0.52) - hip_tilt, torso_bot_y),
        (cx + lean_dx//2 + int(head_r*0.48), torso_bot_y - torso_h * 0.15),
        (cx + lean_dx + sh_w_r + int(6*s), torso_top_y + torso_h * 0.35),
        (cx + lean_dx + sh_w_r, torso_top_y - shoulder_tilt),
        steps=40
    )
    # Top edge (shoulders — gentle curve, not straight)
    torso_top = bezier3(
        (cx + lean_dx + sh_w_r, torso_top_y - shoulder_tilt),
        (cx + lean_dx, torso_top_y + int(4*s)),
        (cx + lean_dx - sh_w_l, torso_top_y + shoulder_tilt),
        steps=20
    )
    # Bottom edge (hip — gentle curve)
    torso_bot = bezier3(
        (cx + lean_dx//2 - int(head_r*0.52) + hip_tilt, torso_bot_y),
        (cx + lean_dx//2, torso_bot_y + int(4*s)),
        (cx + lean_dx//2 + int(head_r*0.52) - hip_tilt, torso_bot_y),
        steps=20
    )

    torso_poly = torso_l + torso_bot + torso_r + torso_top
    draw.polygon(torso_poly, fill=HOODIE)

    # Shadow on right side — simple vertical split through torso
    shadow_l = bezier4(
        (cx + lean_dx + int(head_r * 0.10), torso_top_y),
        (cx + lean_dx//2 + int(head_r * 0.15), torso_top_y + torso_h * 0.35),
        (cx + lean_dx//2 + int(head_r * 0.10), torso_bot_y - torso_h * 0.2),
        (cx + lean_dx//2 + int(head_r * 0.05), torso_bot_y),
        steps=24
    )
    shadow_poly = shadow_l + torso_bot[len(torso_bot)//2:] + torso_r + torso_top[:3]
    if len(shadow_poly) > 2:
        draw.polygon(shadow_poly, fill=HOODIE_SH)

    # Hoodie outline
    polyline(draw, torso_poly + [torso_poly[0]], LINE, width=lw)

    # Collar V-neck (curved)
    collar_pts = bezier3(
        (cx + lean_dx - int(head_r*0.30), torso_top_y + int(2*s)),
        (cx + lean_dx, torso_top_y + int(14*s)),
        (cx + lean_dx + int(head_r*0.30), torso_top_y + int(2*s)),
        steps=20
    )
    polyline(draw, collar_pts, (250, 232, 200), width=max(4, int(5*s)))
    polyline(draw, collar_pts, LINE, width=lw2)

    # Pixel accent
    import random
    rng = random.Random(42)
    px_cx = cx + lean_dx
    px_cy = torso_top_y + int(torso_h * 0.50)
    for _ in range(10):
        px_x = px_cx + rng.randint(-int(18*s), int(18*s))
        px_y = px_cy + rng.randint(-int(12*s), int(12*s))
        psz = max(2, rng.choice([int(2*s), int(3*s)]))
        pc = rng.choice([PX_CYAN, PX_MAG, (240, 240, 240)])
        draw.rectangle([px_x, px_y, px_x + psz, px_y + psz], fill=pc)

    # Hoodie hem (curved)
    hem_y = torso_bot_y - int(torso_h * 0.10)
    hem_pts = bezier3(
        (cx + lean_dx//2 - int(head_r*0.48), hem_y),
        (cx + lean_dx//2, hem_y + int(4*s)),
        (cx + lean_dx//2 + int(head_r*0.48), hem_y),
        steps=20
    )
    polyline(draw, hem_pts, HOODIE_SH, width=max(3, int(4*s)))

    # ══════════════════════════════════════════════════════════════════════
    # ARMS — using tube_polygon for clean filled shapes
    # ══════════════════════════════════════════════════════════════════════

    # Left arm: raised outward (CURIOUS — arm up and out, hand at head level)
    l_sh_x = cx + lean_dx - sh_w_l + int(10*s)
    l_sh_y = torso_top_y + int(8*s) + shoulder_tilt
    l_elbow_x = l_sh_x - int(40*s)
    l_elbow_y = l_sh_y + int(25*s)
    l_hand_x = l_elbow_x - int(15*s)
    l_hand_y = l_elbow_y - int(35*s)

    # Upper arm: goes out from shoulder to elbow
    upper_l = bezier4((l_sh_x, l_sh_y),
                       (l_sh_x - int(15*s), l_sh_y + int(5*s)),
                       (l_elbow_x + int(5*s), l_elbow_y - int(8*s)),
                       (l_elbow_x, l_elbow_y), steps=30)
    # Forearm: elbow up toward hand (raised gesture)
    fore_l = bezier4((l_elbow_x, l_elbow_y),
                      (l_elbow_x - int(5*s), l_elbow_y - int(12*s)),
                      (l_hand_x + int(5*s), l_hand_y + int(12*s)),
                      (l_hand_x, l_hand_y), steps=30)

    # Draw as filled tube polygons
    arm_tube = tube_polygon(upper_l, int(10*s), int(8*s))
    draw.polygon(arm_tube, fill=HOODIE)
    polyline(draw, arm_tube + [arm_tube[0]], LINE, width=lw2)

    fore_tube = tube_polygon(fore_l, int(8*s), int(7*s))
    draw.polygon(fore_tube, fill=HOODIE)
    polyline(draw, fore_tube + [fore_tube[0]], LINE, width=lw2)

    # Left hand: mitten
    hand_r_s = int(10*s)
    hand_pts = ellipse_points(l_hand_x, l_hand_y, hand_r_s, int(hand_r_s * 0.75), steps=24)
    draw.polygon(hand_pts, fill=SKIN)
    polyline(draw, hand_pts + [hand_pts[0]], LINE, width=lw2)
    # Thumb
    th_pts = ellipse_points(l_hand_x + int(7*s), l_hand_y + int(4*s),
                             int(4*s), int(3*s), steps=16)
    draw.polygon(th_pts, fill=SKIN)
    polyline(draw, th_pts + [th_pts[0]], LINE, width=max(1, int(1.5*s)))

    # Right arm: hanging relaxed with natural curve
    r_sh_x = cx + lean_dx + sh_w_r - int(10*s)
    r_sh_y = torso_top_y + int(8*s) - shoulder_tilt
    r_wrist_x = r_sh_x + int(12*s)
    r_wrist_y = torso_bot_y + int(12*s)
    r_hand_x = r_wrist_x + int(2*s)
    r_hand_y = r_wrist_y + int(10*s)

    # Sleeve portion (shoulder to wrist)
    arm_r = bezier4((r_sh_x, r_sh_y),
                     (r_sh_x + int(14*s), r_sh_y + int(25*s)),
                     (r_wrist_x + int(6*s), r_wrist_y - int(20*s)),
                     (r_wrist_x, r_wrist_y), steps=40)
    arm_r_tube = tube_polygon(arm_r, int(10*s), int(7*s))
    draw.polygon(arm_r_tube, fill=HOODIE)
    polyline(draw, arm_r_tube + [arm_r_tube[0]], LINE, width=lw2)

    # Right hand (below wrist)
    hand_pts_r = ellipse_points(r_hand_x, r_hand_y, hand_r_s, int(hand_r_s * 0.80), steps=24)
    draw.polygon(hand_pts_r, fill=SKIN)
    polyline(draw, hand_pts_r + [hand_pts_r[0]], LINE, width=lw2)

    # ══════════════════════════════════════════════════════════════════════
    # LEGS — tube_polygon for clean organic shapes
    # ══════════════════════════════════════════════════════════════════════
    leg_top_y = torso_bot_y
    leg_h = int(body_h * 0.50)
    foot_y = leg_top_y + leg_h

    hip_l_x = cx + lean_dx//2 - int(head_r * 0.28) + hip_tilt
    hip_r_x = cx + lean_dx//2 + int(head_r * 0.28) - hip_tilt

    # RIGHT LEG: weight-bearing, mostly straight
    r_knee_y = leg_top_y + leg_h * 0.48
    r_foot_x = hip_r_x + int(3*s)

    r_upper = bezier3((hip_r_x, leg_top_y),
                       (hip_r_x + int(4*s), (leg_top_y + r_knee_y)/2),
                       (hip_r_x + int(2*s), r_knee_y), steps=20)
    r_lower = bezier3((hip_r_x + int(2*s), r_knee_y),
                       (r_foot_x + int(2*s), (r_knee_y + foot_y)/2),
                       (r_foot_x, foot_y), steps=20)

    for pts, wt, wb in [(r_upper, int(12*s), int(10*s)),
                         (r_lower, int(10*s), int(8*s))]:
        tube = tube_polygon(pts, wt, wb)
        draw.polygon(tube, fill=PANTS)
        polyline(draw, tube + [tube[0]], LINE, width=lw2)

    # LEFT LEG: relaxed, angled out
    l_knee_y = leg_top_y + leg_h * 0.46
    l_foot_x = hip_l_x - int(10*s)

    l_upper = bezier3((hip_l_x, leg_top_y),
                       (hip_l_x - int(5*s), (leg_top_y + l_knee_y)/2),
                       (hip_l_x - int(6*s), l_knee_y), steps=20)
    l_lower = bezier3((hip_l_x - int(6*s), l_knee_y),
                       (l_foot_x - int(3*s), (l_knee_y + foot_y)/2),
                       (l_foot_x, foot_y + int(2*s)), steps=20)

    for pts, wt, wb in [(l_upper, int(12*s), int(10*s)),
                         (l_lower, int(10*s), int(8*s))]:
        tube = tube_polygon(pts, wt, wb)
        draw.polygon(tube, fill=PANTS)
        polyline(draw, tube + [tube[0]], LINE, width=lw2)

    # ══════════════════════════════════════════════════════════════════════
    # SHOES — Rounded, visible, with character
    # ══════════════════════════════════════════════════════════════════════
    shoe_w = int(18*s)
    shoe_h = int(10*s)

    for fx, fy, facing in [(r_foot_x, foot_y, 1), (l_foot_x, foot_y + int(2*s), -1)]:
        toe_x = fx + facing * int(8*s)
        # Sole
        sole_pts = ellipse_points(toe_x, fy + int(4*s), shoe_w + int(2*s),
                                   int(shoe_h * 0.45), steps=24)
        draw.polygon(sole_pts, fill=SHOE_SOLE)
        # Shoe body
        shoe_pts = ellipse_points(toe_x, fy, shoe_w, shoe_h, steps=32, a0=180, a1=360)
        shoe_bot = [(toe_x + shoe_w, fy), (toe_x - shoe_w, fy)]
        shoe_all = shoe_pts + shoe_bot
        draw.polygon(shoe_all, fill=SHOE)
        polyline(draw, shoe_all + [shoe_all[0]], LINE, width=lw2)
        # Laces
        for li in range(3):
            ly = fy - int(2*s) - li * int(3*s)
            draw.line([fx - int(5*s), ly, fx + int(5*s), ly], fill=LACES, width=max(1, int(s)))

    return img


# ══════════════════════════════════════════════════════════════════════════════
# MAIN — Side-by-side comparison
# ══════════════════════════════════════════════════════════════════════════════

def main():
    W, H = 1280, 720
    img = Image.new("RGBA", (W, H), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    # Title
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        font_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except OSError:
        font_title = ImageFont.load_default()
        font_label = font_title
        font_small = font_title

    title = "LUMA CONSTRUCTION COMPARISON — C50 | Old (v014 geometric) vs New (organic curves)"
    draw.text((20, 10), title, fill=LINE, font=font_title)

    # Divider
    mid_x = W // 2
    draw.line([(mid_x, 40), (mid_x, H - 10)], fill=LINE, width=2)

    # Panel backgrounds
    panel_top = 50
    panel_h = H - 60
    panel_w = mid_x - 30

    # Left panel: OLD
    draw.rectangle([15, panel_top, mid_x - 15, H - 10], fill=PANEL_BG)
    draw.text((20, panel_top + 5), "OLD: v014 Geometric Construction", fill=LINE, font=font_label)
    draw.text((20, panel_top + 25), "Rectangles + ellipses. Head ~25% of body. Small eyes.",
              fill=(120, 100, 80), font=font_small)

    # Right panel: NEW
    draw.rectangle([mid_x + 15, panel_top, W - 15, H - 10], fill=PANEL_BG)
    draw.text((mid_x + 20, panel_top + 5), "NEW: Organic Curves Prototype", fill=LINE, font=font_label)
    draw.text((mid_x + 20, panel_top + 25), "Dense polygons. Head ~37% of body. Large expressive eyes.",
              fill=(120, 100, 80), font=font_small)

    # Draw characters
    char_top = panel_top + 50
    char_h = panel_h - 60

    img = draw_old_luma(img, 15, char_top, panel_w, char_h)
    draw = ImageDraw.Draw(img)

    img = draw_new_luma(img, mid_x + 15, char_top, panel_w, char_h)
    draw = ImageDraw.Draw(img)

    # Annotation: proportion markers
    # Left panel: mark head proportion
    old_cx = 15 + panel_w // 2
    draw.text((20, H - 35), "Expression: CURIOUS | Head:Body ~1:3 (25%)",
              fill=(120, 100, 80), font=font_small)

    # Right panel
    draw.text((mid_x + 20, H - 35), "Expression: CURIOUS | Head:Body ~1:1.7 (37%) | Weight on R leg",
              fill=(120, 100, 80), font=font_small)

    # Save
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "production")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_PROD_luma_construction_comparison.png")

    # Enforce 1280px max
    final = img.convert("RGB")
    final.thumbnail((1280, 1280), Image.LANCZOS)
    final.save(out_path, "PNG")
    print(f"Saved: {out_path}")
    print(f"Size: {final.size[0]}x{final.size[1]}")

    return out_path


if __name__ == "__main__":
    main()
