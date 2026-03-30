# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
Character Turnaround Generator — Luma & Byte
Cycle 9: Creates 4-view turnaround strips (front, 3/4, side, back) at consistent
200px character height. Each view is drawn as a simplified but faithful silhouette
showing the key design elements from each angle.

Output:
  luma_turnaround.png  — 4-view strip
  byte_turnaround.png  — 4-view strip
"""
from PIL import Image, ImageDraw, ImageFont
import math

# ── Colors ─────────────────────────────────────────────────────────────────────
BG           = (252, 250, 246)
SILHOUETTE   = (15, 10, 20)
NEG_SPACE    = (252, 250, 246)   # matches BG — glass cutouts etc.
LINE_COL     = (60, 50, 40)
LABEL_COL    = (50, 40, 35)
TICK_COL     = (180, 165, 155)
PANEL_BG     = (245, 241, 235)   # slightly tinted panel background

# ── Layout constants ────────────────────────────────────────────────────────────
CHAR_H   = 200          # canonical character height in pixels
VIEW_W   = 180          # width per view panel
PADDING  = 20           # panel interior padding
LABEL_H  = 36           # height reserved below each panel for view label
TITLE_H  = 30           # height reserved above the strip for the character name
STRIP_W  = VIEW_W * 4   # total strip width
STRIP_H  = TITLE_H + CHAR_H + 60 + LABEL_H + 20  # +60 headroom above char, +20 bottom

VIEWS = ["FRONT", "3/4", "SIDE", "BACK"]


# ══════════════════════════════════════════════════════════════════════════════
# LUMA TURNAROUND VIEWS
# ══════════════════════════════════════════════════════════════════════════════

def _luma_head_unit():
    """Luma is 3.5 heads tall at CHAR_H=200px."""
    return CHAR_H / 3.5


def draw_luma_front(draw, cx, base_y):
    """Luma — front view. Canonical forward-facing design.
    Key hooks: cloud hair top, A-line trapezoid hoodie, pocket bump, oversized sneakers.
    """
    hu = _luma_head_unit()
    h  = CHAR_H
    r  = int(hu * 0.46)
    hy = base_y - h

    # Hair cloud mass
    draw.ellipse([cx - int(r*1.5), hy - int(r*0.6), cx + int(r*1.5), hy + int(r*0.8)],
                 fill=SILHOUETTE)
    # Head
    draw.ellipse([cx - r, hy, cx + r, hy + int(hu)], fill=SILHOUETTE)

    # Body — A-line trapezoid hoodie
    sw = int(hu * 0.38)
    hw2 = int(hu * 0.70)
    body_top_y = hy + int(hu * 0.85)
    body_h     = int(hu * 2.0)
    body_bot_y = body_top_y + body_h
    draw.polygon([(cx - sw, body_top_y), (cx + sw, body_top_y),
                  (cx + hw2, body_bot_y), (cx - hw2, body_bot_y)], fill=SILHOUETTE)

    # Pocket bump — protrudes right side outside hem
    mid_frac = 0.55
    hem_mid = cx + int(sw + (hw2 - sw) * mid_frac)
    pocket_y = body_top_y + int(body_h * 0.50)
    draw.rectangle([hem_mid, pocket_y,
                    hem_mid + int(hu * 0.30), pocket_y + int(hu * 0.42)],
                   fill=SILHOUETTE)

    # Legs
    lw = int(hu * 0.20)
    leg_h = int(hu * 0.55)
    draw.rectangle([cx - lw*2, body_bot_y, cx - 4, body_bot_y + leg_h], fill=SILHOUETTE)
    draw.rectangle([cx + 4, body_bot_y, cx + lw*2, body_bot_y + leg_h], fill=SILHOUETTE)

    # Oversized sneakers
    fw = int(hu * 0.52)
    fh = int(hu * 0.28)
    draw.ellipse([cx - lw*2 - fw + int(fw*0.3), base_y - fh,
                  cx - lw*2 + int(fw*0.5),       base_y], fill=SILHOUETTE)
    draw.ellipse([cx + lw*2 - int(fw*0.5),        base_y - fh,
                  cx + lw*2 + fw - int(fw*0.3),   base_y], fill=SILHOUETTE)


def draw_luma_three_quarter(draw, cx, base_y):
    """Luma — 3/4 view (approx 45° rotation to left).
    Shows depth in hair volume, hoodie slightly compressed on far side,
    pocket bump visible on near side, one sneaker foreshortened.
    The near shoulder is wider than the far shoulder.
    """
    hu = _luma_head_unit()
    h  = CHAR_H
    r  = int(hu * 0.46)
    hy = base_y - h

    # Hair cloud — slightly asymmetric (near side wider)
    draw.ellipse([cx - int(r*1.7), hy - int(r*0.6), cx + int(r*1.1), hy + int(r*0.8)],
                 fill=SILHOUETTE)
    # Add depth blob on near side
    draw.ellipse([cx - int(r*1.8), hy - int(r*0.3), cx - int(r*0.8), hy + int(r*0.6)],
                 fill=SILHOUETTE)
    # Head (slightly oval in 3/4)
    draw.ellipse([cx - int(r*0.92), hy, cx + int(r*0.78), hy + int(hu)], fill=SILHOUETTE)

    # Body — trapezoid compressed on far side (3/4 foreshortening)
    near_sw = int(hu * 0.44)   # near shoulder wider
    far_sw  = int(hu * 0.22)   # far shoulder foreshortened
    near_hw = int(hu * 0.78)   # near hem (full flare)
    far_hw  = int(hu * 0.38)   # far hem compressed
    body_top_y = hy + int(hu * 0.85)
    body_h     = int(hu * 2.0)
    body_bot_y = body_top_y + body_h
    # Near side left, far side right
    draw.polygon([(cx - near_sw, body_top_y), (cx + far_sw, body_top_y),
                  (cx + far_hw,  body_bot_y), (cx - near_hw, body_bot_y)],
                 fill=SILHOUETTE)

    # Pocket bump on near (left) side
    pocket_y = body_top_y + int(body_h * 0.50)
    draw.rectangle([cx - near_hw - int(hu * 0.28), pocket_y,
                    cx - near_hw, pocket_y + int(hu * 0.42)], fill=SILHOUETTE)

    # Near arm (left) visible at side
    arm_y = body_top_y + int(body_h * 0.12)
    draw.rectangle([cx - near_sw - int(hu * 0.22), arm_y,
                    cx - near_sw, arm_y + int(hu * 0.55)], fill=SILHOUETTE)

    # Legs — near leg fully visible, far leg partially occluded
    lw = int(hu * 0.20)
    leg_h = int(hu * 0.55)
    draw.rectangle([cx - lw*2, body_bot_y, cx - 4, body_bot_y + leg_h], fill=SILHOUETTE)
    draw.rectangle([cx + 4, body_bot_y, cx + lw + 4, body_bot_y + leg_h], fill=SILHOUETTE)

    # Sneakers — near foot full, far foot partially hidden
    fw = int(hu * 0.52)
    fh = int(hu * 0.28)
    draw.ellipse([cx - lw*2 - fw + int(fw*0.3), base_y - fh,
                  cx - lw*2 + int(fw*0.5),       base_y], fill=SILHOUETTE)
    # Far shoe — foreshortened oval
    draw.ellipse([cx + 4, base_y - fh, cx + lw + 4 + int(fw*0.55), base_y], fill=SILHOUETTE)


def draw_luma_side(draw, cx, base_y):
    """Luma — side (profile) view.
    Hair mass extends behind head. A-line hoodie reads as a wedge.
    Pocket bump visible protruding from front hem.
    One sneaker fully visible in profile.
    """
    hu = _luma_head_unit()
    h  = CHAR_H
    r  = int(hu * 0.46)
    hy = base_y - h

    # Hair cloud — extends behind head in profile
    draw.ellipse([cx - int(r*0.6), hy - int(r*0.7), cx + int(r*1.3), hy + int(r*0.9)],
                 fill=SILHOUETTE)
    draw.ellipse([cx, hy - int(r*0.5), cx + int(r*1.2), hy - int(r*0.0)], fill=SILHOUETTE)

    # Head — oval in profile (slightly deeper front-to-back)
    draw.ellipse([cx - int(r*0.55), hy, cx + int(r*0.78), hy + int(hu)], fill=SILHOUETTE)

    # Body — side view: narrow vertical rectangle (width = depth ~0.6 hu)
    body_depth = int(hu * 0.60)   # front-to-back depth
    body_top_y = hy + int(hu * 0.85)
    body_h     = int(hu * 2.0)
    body_bot_y = body_top_y + body_h
    # Front edge of body slightly forward, back edge behind center
    front_x = cx - int(body_depth * 0.65)
    back_x  = cx + int(body_depth * 0.35)
    # Taper: shoulder narrower, hem slightly wider (A-line in profile)
    draw.polygon([(front_x - int(hu*0.06), body_top_y), (back_x, body_top_y),
                  (back_x, body_bot_y), (front_x - int(hu*0.16), body_bot_y)],
                 fill=SILHOUETTE)

    # Pocket bump — protrudes from front hem
    pocket_y = body_top_y + int(body_h * 0.50)
    draw.rectangle([front_x - int(hu*0.16) - int(hu*0.28), pocket_y,
                    front_x - int(hu*0.16), pocket_y + int(hu*0.42)], fill=SILHOUETTE)

    # Single leg in profile
    lw = int(hu * 0.20)
    leg_h = int(hu * 0.55)
    # Slightly forward position
    leg_cx = cx - int(hu * 0.10)
    draw.rectangle([leg_cx - lw, body_bot_y, leg_cx + lw, body_bot_y + leg_h], fill=SILHOUETTE)

    # Sneaker in profile — elongated oval
    # Cycle 11 fix: normalized to 0.52 to match front/back view proportions (was 0.65)
    fw = int(hu * 0.52)
    fh = int(hu * 0.28)
    draw.ellipse([leg_cx - fw + int(fw*0.3), base_y - fh,
                  leg_cx + int(fw*0.4),       base_y], fill=SILHOUETTE)


def draw_luma_back(draw, cx, base_y):
    """Luma — back view.
    Back of hair cloud (same mass). Back of hoodie — no pocket, plain trapezoid.
    Back of sneakers. Hoodie has a small tag/loop detail at center neck.
    """
    hu = _luma_head_unit()
    h  = CHAR_H
    r  = int(hu * 0.46)
    hy = base_y - h

    # Hair cloud — same from back, slightly different shape (back of curls)
    draw.ellipse([cx - int(r*1.5), hy - int(r*0.6), cx + int(r*1.5), hy + int(r*0.8)],
                 fill=SILHOUETTE)
    draw.ellipse([cx - int(r*1.3), hy - int(r*0.4), cx - int(r*0.5), hy + int(r*0.3)],
                 fill=SILHOUETTE)
    draw.ellipse([cx + int(r*0.5), hy - int(r*0.4), cx + int(r*1.3), hy + int(r*0.3)],
                 fill=SILHOUETTE)

    # Head (back of head — same circle)
    draw.ellipse([cx - r, hy, cx + r, hy + int(hu)], fill=SILHOUETTE)

    # Hoodie — A-line from back (plain, no pocket)
    sw = int(hu * 0.38)
    hw2 = int(hu * 0.70)
    body_top_y = hy + int(hu * 0.85)
    body_h     = int(hu * 2.0)
    body_bot_y = body_top_y + body_h
    draw.polygon([(cx - sw, body_top_y), (cx + sw, body_top_y),
                  (cx + hw2, body_bot_y), (cx - hw2, body_bot_y)], fill=SILHOUETTE)

    # Hoodie tag loop at center-back neckline (small detail)
    tag_y = body_top_y - int(hu * 0.08)
    draw.rectangle([cx - int(hu*0.06), tag_y, cx + int(hu*0.06), body_top_y], fill=SILHOUETTE)

    # Legs (same from back)
    lw = int(hu * 0.20)
    leg_h = int(hu * 0.55)
    draw.rectangle([cx - lw*2, body_bot_y, cx - 4, body_bot_y + leg_h], fill=SILHOUETTE)
    draw.rectangle([cx + 4, body_bot_y, cx + lw*2, body_bot_y + leg_h], fill=SILHOUETTE)

    # Back of sneakers — heel-forward view
    fw = int(hu * 0.52)
    fh = int(hu * 0.28)
    draw.ellipse([cx - lw*2 - fw + int(fw*0.3), base_y - fh,
                  cx - lw*2 + int(fw*0.5),       base_y], fill=SILHOUETTE)
    draw.ellipse([cx + lw*2 - int(fw*0.5),        base_y - fh,
                  cx + lw*2 + fw - int(fw*0.3),   base_y], fill=SILHOUETTE)


# ══════════════════════════════════════════════════════════════════════════════
# BYTE TURNAROUND VIEWS
# ══════════════════════════════════════════════════════════════════════════════

def _byte_size():
    """Byte at CHAR_H=200px — body is an OVAL (ellipse). body_rx = s//2, body_ry = s*0.55.
    CANONICAL: oval matches byte_expressions_generator.py. Chamfered-box is RETIRED.
    """
    return int(CHAR_H * 0.55)


def draw_byte_front(draw, cx, base_y):
    """Byte — front view. OVAL body (ellipse), pixel eyes, stubby limbs, hover gap.
    Body shape matches byte_expressions_generator.py canonical design.
    """
    s  = _byte_size()
    float_gap = int(s * 0.18)
    # Oval proportions: rx = s//2, ry = s*0.55 (slightly taller than wide)
    body_rx = s // 2
    body_ry = int(s * 0.55)
    # Center of oval: base_y - float_gap - body_ry (bottom of oval at base_y - float_gap)
    bcy = base_y - float_gap - body_ry
    hy = bcy - body_ry   # top of oval (for eye/limb reference)

    # OVAL body
    draw.ellipse([cx - body_rx, bcy - body_ry,
                  cx + body_rx, bcy + body_ry], fill=SILHOUETTE)

    # Pixel eyes — positioned relative to oval center
    eye_y = bcy - body_ry // 5
    eye_sz = max(4, int(s * 0.10))
    # Left eye — pixel squares (2x2 arrangement)
    lx = cx - int(s * 0.22)
    for row in range(2):
        for col in range(2):
            px = lx + col * (eye_sz + 2) - eye_sz
            py = eye_y + row * (eye_sz + 2)
            draw.rectangle([px, py, px + eye_sz, py + eye_sz], fill=NEG_SPACE)
    # Right eye — organic circle (asymmetric personality element)
    rx = cx + int(s * 0.15)
    er = int(s * 0.10)
    draw.ellipse([rx - er, eye_y, rx + er, eye_y + er*2], fill=NEG_SPACE)

    # Small mouth — horizontal pixel bar in lower oval
    mouth_y = bcy + body_ry // 3
    draw.rectangle([cx - int(s*0.18), mouth_y, cx + int(s*0.18), mouth_y + max(2, int(s*0.05))],
                   fill=NEG_SPACE)

    # Stubby arm limbs — attach at oval edge (body_rx wide, midway up body)
    lw = int(s * 0.22)
    lh = int(s * 0.25)
    arm_y = bcy - body_ry // 5
    draw.rectangle([cx - body_rx - lw, arm_y, cx - body_rx, arm_y + lh], fill=SILHOUETTE)
    draw.rectangle([cx + body_rx, arm_y, cx + body_rx + lw, arm_y + lh], fill=SILHOUETTE)

    # Stubby leg limbs — attach at bottom of oval
    leg_w = int(s * 0.18)
    leg_h = int(s * 0.20)
    leg_offset = s // 4
    draw.rectangle([cx - leg_offset - leg_w//2, bcy + body_ry,
                    cx - leg_offset + leg_w//2, bcy + body_ry + leg_h],
                   fill=SILHOUETTE)
    draw.rectangle([cx + leg_offset - leg_w//2, bcy + body_ry,
                    cx + leg_offset + leg_w//2, bcy + body_ry + leg_h],
                   fill=SILHOUETTE)

    # Hover particles — 10x10 pixel confetti below feet
    particle_y = bcy + body_ry + leg_h + 4
    psz = 10
    for i, px in enumerate([cx - int(s*0.30), cx - int(s*0.08),
                             cx + int(s*0.08), cx + int(s*0.25)]):
        py = particle_y + (i % 2) * 6
        draw.rectangle([px, py, px + psz, py + psz], fill=SILHOUETTE)


def draw_byte_three_quarter(draw, cx, base_y):
    """Byte — 3/4 view. Oval with slight horizontal compression to suggest depth.
    Front face features (eyes) visible on the near side. Near side wider/fuller,
    far side compressed. Depth shown via slight parallelogram shadow on far side.
    """
    s  = _byte_size()
    float_gap = int(s * 0.18)
    body_rx = s // 2
    body_ry = int(s * 0.55)
    # Shift the oval center slightly left — near face centered on cx, far side recedes right
    face_off = int(s * 0.12)
    fx = cx - face_off   # near face center
    bcy = base_y - float_gap - body_ry

    # OVAL body (front face, near side)
    draw.ellipse([fx - body_rx, bcy - body_ry,
                  fx + body_rx, bcy + body_ry], fill=SILHOUETTE)

    # Depth shadow — parallelogram on far (right) side of oval to suggest 3D volume
    depth = int(s * 0.28)
    SIDE_FILL = (40, 35, 45)
    side_pts = [
        (fx + body_rx,          bcy - body_ry + int(body_ry*0.3)),
        (fx + body_rx + depth,  bcy - body_ry + int(body_ry*0.3) - int(depth*0.4)),
        (fx + body_rx + depth,  bcy + body_ry - int(body_ry*0.3) - int(depth*0.4)),
        (fx + body_rx,          bcy + body_ry - int(body_ry*0.3)),
    ]
    draw.polygon(side_pts, fill=SIDE_FILL)

    # Top rim — small ellipse arc showing upper curve receding
    TOP_FILL = (30, 26, 35)
    top_pts = [
        (fx - body_rx + int(body_rx*0.3), bcy - body_ry),
        (fx + body_rx,                    bcy - body_ry + int(body_ry*0.3)),
        (fx + body_rx + depth,            bcy - body_ry + int(body_ry*0.3) - int(depth*0.4)),
        (fx - body_rx + int(body_rx*0.3) + int(depth*0.2), bcy - body_ry - int(depth*0.3)),
    ]
    draw.polygon(top_pts, fill=TOP_FILL)

    # Pixel eyes on near face
    eye_y = bcy - body_ry // 5
    eye_sz = max(4, int(s * 0.10))
    lx = fx - int(s * 0.22)
    for row in range(2):
        for col in range(2):
            px = lx + col * (eye_sz + 2) - eye_sz
            py = eye_y + row * (eye_sz + 2)
            draw.rectangle([px, py, px + eye_sz, py + eye_sz], fill=NEG_SPACE)
    rx = fx + int(s * 0.15)
    er = int(s * 0.10)
    draw.ellipse([rx - er, eye_y, rx + er, eye_y + er*2], fill=NEG_SPACE)

    # Arms — near (left) arm full, far (right) arm on depth face
    lw = int(s * 0.22)
    lh = int(s * 0.25)
    arm_y = bcy - body_ry // 5
    draw.rectangle([fx - body_rx - lw, arm_y, fx - body_rx, arm_y + lh], fill=SILHOUETTE)
    draw.rectangle([fx + body_rx + depth - int(lw*0.2), arm_y - int(lh*0.2),
                    fx + body_rx + depth + int(lw*0.6), arm_y + lh - int(lh*0.2)],
                   fill=SILHOUETTE)

    # Legs
    leg_w = int(s * 0.18)
    leg_h = int(s * 0.20)
    leg_offset = s // 4
    draw.rectangle([fx - leg_offset - leg_w//2, bcy + body_ry,
                    fx - leg_offset + leg_w//2, bcy + body_ry + leg_h],
                   fill=SILHOUETTE)
    draw.rectangle([fx + leg_offset - leg_w//2 + int(depth*0.12), bcy + body_ry,
                    fx + leg_offset + leg_w//2 + int(depth*0.12), bcy + body_ry + leg_h],
                   fill=SILHOUETTE)

    # Hover particles
    particle_y = bcy + body_ry + leg_h + 4
    psz = 10
    for i, px in enumerate([fx - int(s*0.25), fx, fx + int(s*0.18), fx + int(s*0.35)]):
        py = particle_y + (i % 2) * 6
        draw.rectangle([px, py, px + psz, py + psz], fill=SILHOUETTE)


def draw_byte_side(draw, cx, base_y):
    """Byte — side (profile) view.
    Narrow ellipse — oval compressed to show side depth. Single eye hint (rim visible).
    One arm forward, legs visible.
    """
    s  = _byte_size()
    float_gap = int(s * 0.18)
    # In profile: body is narrow — depth is ~0.62 of s, height same
    body_rx_side = int(s * 0.31)   # narrow profile width (depth of oval)
    body_ry = int(s * 0.55)
    bcy = base_y - float_gap - body_ry

    # Narrow OVAL for side profile
    draw.ellipse([cx - body_rx_side, bcy - body_ry,
                  cx + body_rx_side, bcy + body_ry], fill=SILHOUETTE)

    # Side profile: face is turned away — show single eye rim as hint on near edge
    eye_rim_x = cx - body_rx_side + int(body_rx_side * 0.3)
    eye_rim_y = bcy - body_ry // 5
    er = int(s * 0.07)
    draw.ellipse([eye_rim_x - er, eye_rim_y, eye_rim_x + er, eye_rim_y + er*2],
                 fill=NEG_SPACE)

    # One visible arm (front arm — forward in profile)
    lw = int(s * 0.22)
    lh = int(s * 0.25)
    arm_y = bcy - body_ry // 5
    draw.rectangle([cx + body_rx_side, arm_y, cx + body_rx_side + lw, arm_y + lh],
                   fill=SILHOUETTE)

    # Legs
    leg_w = int(s * 0.18)
    leg_h = int(s * 0.20)
    leg_offset = s // 4
    draw.rectangle([cx - leg_offset - leg_w//2, bcy + body_ry,
                    cx - leg_offset + leg_w//2, bcy + body_ry + leg_h],
                   fill=SILHOUETTE)
    draw.rectangle([cx + leg_offset - leg_w//2, bcy + body_ry,
                    cx + leg_offset + leg_w//2, bcy + body_ry + leg_h],
                   fill=SILHOUETTE)

    # Hover particles
    particle_y = bcy + body_ry + leg_h + 4
    psz = 10
    for i, px in enumerate([cx - int(s*0.22), cx - int(s*0.05),
                             cx + int(s*0.05), cx + int(s*0.22)]):
        py = particle_y + (i % 2) * 6
        draw.rectangle([px, py, px + psz, py + psz], fill=SILHOUETTE)


def draw_byte_back(draw, cx, base_y):
    """Byte — back view.
    Plain OVAL back — no eyes visible.
    Back of arms/legs. Hover particles below feet.
    Center-back data-port: vertical NEG_SPACE slot — key character detail.
    """
    s  = _byte_size()
    float_gap = int(s * 0.18)
    body_rx = s // 2
    body_ry = int(s * 0.55)
    bcy = base_y - float_gap - body_ry

    # OVAL body back (same proportions as front)
    draw.ellipse([cx - body_rx, bcy - body_ry,
                  cx + body_rx, bcy + body_ry], fill=SILHOUETTE)

    # Center-back data port — vertical NEG_SPACE slot (character hook from behind)
    port_w = max(3, int(s * 0.07))
    port_h = int(s * 0.22)
    port_y = bcy - body_ry // 5
    draw.rectangle([cx - port_w//2, port_y, cx + port_w//2, port_y + port_h],
                   fill=NEG_SPACE)

    # Arms (same as front — symmetric)
    lw = int(s * 0.22)
    lh = int(s * 0.25)
    arm_y = bcy - body_ry // 5
    draw.rectangle([cx - body_rx - lw, arm_y, cx - body_rx, arm_y + lh], fill=SILHOUETTE)
    draw.rectangle([cx + body_rx, arm_y, cx + body_rx + lw, arm_y + lh], fill=SILHOUETTE)

    # Legs
    leg_w = int(s * 0.18)
    leg_h = int(s * 0.20)
    leg_offset = s // 4
    draw.rectangle([cx - leg_offset - leg_w//2, bcy + body_ry,
                    cx - leg_offset + leg_w//2, bcy + body_ry + leg_h],
                   fill=SILHOUETTE)
    draw.rectangle([cx + leg_offset - leg_w//2, bcy + body_ry,
                    cx + leg_offset + leg_w//2, bcy + body_ry + leg_h],
                   fill=SILHOUETTE)

    # Hover particles
    particle_y = bcy + body_ry + leg_h + 4
    psz = 10
    for i, px in enumerate([cx - int(s*0.30), cx - int(s*0.08),
                             cx + int(s*0.08), cx + int(s*0.25)]):
        py = particle_y + (i % 2) * 6
        draw.rectangle([px, py, px + psz, py + psz], fill=SILHOUETTE)


# ══════════════════════════════════════════════════════════════════════════════
# COSMO TURNAROUND VIEWS
# Cosmo: tall, lanky, 4.0 heads tall. Defining feature: thick plastic glasses
# (negative-space lens cutouts). Notebook always under left arm.
# Striped shirt, slim chinos, low-profile shoes.
# ══════════════════════════════════════════════════════════════════════════════

def _cosmo_head_unit():
    """Cosmo is 4.0 heads tall at CHAR_H=200px."""
    return CHAR_H / 4.0


def _draw_cosmo_glasses(draw, cx, gy, gr, is_front=True, is_back=False, is_side=False,
                        front_x=None):
    """Draw Cosmo's glasses as the defining silhouette element.
    Thick plastic frames with NEG_SPACE lens cutouts.
    gr: lens radius. gy: vertical center of glasses.
    is_front: both lenses visible (front view).
    is_back: no lenses visible (back view).
    is_side: single lens in profile, projecting forward from front_x.
    Otherwise: 3/4 view (near lens full, far lens compressed).

    Cycle 12: is_side parameter added so draw_cosmo_side() calls this helper
    instead of inline code, matching the consistency guarantee of front/3-quarter/back views.
    """
    if is_back:
        return  # back view: glasses not visible

    if is_side:
        # Side/profile view: one circular lens as a protrusion ahead of the face silhouette.
        # front_x is the front edge of the head in profile — lens sits slightly ahead of it.
        if front_x is None:
            front_x = cx - int(gr * 0.4)  # fallback estimate
        rim = 3
        lens_cx = front_x - int(gr * 0.4)  # ahead of front face edge
        # Outer rim
        draw.ellipse([lens_cx - gr - rim, gy - gr - rim, lens_cx + gr + rim, gy + gr + rim],
                     fill=SILHOUETTE)
        # Inner lens cutout
        draw.ellipse([lens_cx - gr, gy - gr, lens_cx + gr, gy + gr], fill=NEG_SPACE)
        # Ear arm: extends from lens rim to the back of the head
        # back_x is estimated as front_x + head_depth (≈ 2.5 × gr from front_x)
        back_x = front_x + int(gr * 3.0)
        draw.rectangle([lens_cx + gr, gy - 2, back_x + int(gr * 0.33), gy + 2],
                       fill=SILHOUETTE)
        return

    if is_front:
        lcx = cx - int(gr * 1.55)
        rcx = cx + int(gr * 1.55)
        rim = 3
        # Outer rims
        draw.ellipse([lcx - gr - rim, gy - gr - rim, lcx + gr + rim, gy + gr + rim],
                     fill=SILHOUETTE)
        draw.ellipse([rcx - gr - rim, gy - gr - rim, rcx + gr + rim, gy + gr + rim],
                     fill=SILHOUETTE)
        # Inner lens cutouts
        draw.ellipse([lcx - gr, gy - gr, lcx + gr, gy + gr], fill=NEG_SPACE)
        draw.ellipse([rcx - gr, gy - gr, rcx + gr, gy + gr], fill=NEG_SPACE)
        # Bridge
        draw.rectangle([lcx + gr, gy - 2, rcx - gr, gy + 2], fill=SILHOUETTE)
    else:
        # 3/4: near lens (left) full, far lens (right) slightly compressed + offset
        near_cx = cx - int(gr * 1.1)
        far_cx  = cx + int(gr * 0.8)
        far_rx  = int(gr * 0.72)   # compressed in 3/4
        rim = 3
        draw.ellipse([near_cx - gr - rim, gy - gr - rim, near_cx + gr + rim, gy + gr + rim],
                     fill=SILHOUETTE)
        draw.ellipse([far_cx - far_rx - rim, gy - gr - rim + 2,
                      far_cx + far_rx + rim, gy + gr + rim - 2], fill=SILHOUETTE)
        draw.ellipse([near_cx - gr, gy - gr, near_cx + gr, gy + gr], fill=NEG_SPACE)
        draw.ellipse([far_cx - far_rx, gy - gr + 2, far_cx + far_rx, gy + gr - 2], fill=NEG_SPACE)
        draw.rectangle([near_cx + gr, gy - 2, far_cx - far_rx, gy + 2], fill=SILHOUETTE)


def draw_cosmo_front(draw, cx, base_y):
    """Cosmo — front view. Tall, lanky. Glasses front-on: both lenses as NEG_SPACE.
    Notebook tucked under left arm — flat rectangle side-view.
    """
    hu = _cosmo_head_unit()
    h  = CHAR_H
    hy = base_y - h

    # Head (slightly narrower rectangle, rounded)
    hw = int(hu * 0.40)
    hh = int(hu * 0.95)
    draw.rounded_rectangle([cx - hw, hy, cx + hw, hy + hh], radius=6, fill=SILHOUETTE)

    # Glasses — front view, both lenses
    gr = int(hu * 0.18)
    gy = hy + int(hh * 0.48)
    _draw_cosmo_glasses(draw, cx, gy, gr, is_front=True)

    # Hair — short, slight cowlick on left side
    draw.ellipse([cx - hw - 4, hy - int(hu*0.08), cx + hw + 4, hy + int(hu*0.12)],
                 fill=SILHOUETTE)
    draw.ellipse([cx - hw - 2, hy - int(hu*0.22), cx - int(hw*0.2), hy + int(hu*0.05)],
                 fill=SILHOUETTE)

    # Body — narrow rectangle (slim build)
    bw = int(hu * 0.38)
    body_h = int(hu * 2.4)
    body_top_y = hy + hh
    body_bot_y = body_top_y + body_h
    draw.rectangle([cx - bw, body_top_y, cx + bw, body_bot_y], fill=SILHOUETTE)

    # Notebook — under left arm, flat rectangle protruding left
    nw = int(hu * 0.48)
    nh = int(hu * 0.58)
    nb_y = body_top_y + int(body_h * 0.28)
    draw.rectangle([cx - bw - nw + 10, nb_y, cx - bw + 10, nb_y + nh], fill=SILHOUETTE)

    # Legs — slim
    lw = int(hu * 0.18)
    leg_h = int(hu * 0.60)
    draw.rectangle([cx - bw + 4, body_bot_y, cx - lw, body_bot_y + leg_h], fill=SILHOUETTE)
    draw.rectangle([cx + lw, body_bot_y, cx + bw - 4, body_bot_y + leg_h], fill=SILHOUETTE)

    # Shoes — low profile
    fw = int(hu * 0.28)
    fh = int(hu * 0.18)
    draw.ellipse([cx - bw + 4 - int(fw*0.4), base_y - fh, cx - lw + int(fw*0.6), base_y],
                 fill=SILHOUETTE)
    draw.ellipse([cx + lw - int(fw*0.3), base_y - fh, cx + bw - 4 + int(fw*0.4), base_y],
                 fill=SILHOUETTE)


def draw_cosmo_three_quarter(draw, cx, base_y):
    """Cosmo — 3/4 view. Glasses partially visible (near lens full, far compressed).
    Near side wider, far side compressed. Notebook at near side.
    """
    hu = _cosmo_head_unit()
    h  = CHAR_H
    hy = base_y - h

    hw = int(hu * 0.40)
    hh = int(hu * 0.95)
    # Slightly asymmetric head in 3/4
    draw.rounded_rectangle([cx - int(hw*1.0), hy, cx + int(hw*0.82), hy + hh],
                            radius=6, fill=SILHOUETTE)

    # Glasses — 3/4, near lens + compressed far lens
    gr = int(hu * 0.18)
    gy = hy + int(hh * 0.48)
    _draw_cosmo_glasses(draw, cx - int(hu*0.08), gy, gr, is_front=False)

    # Hair
    draw.ellipse([cx - int(hw*1.1), hy - int(hu*0.08), cx + int(hw*0.9), hy + int(hu*0.12)],
                 fill=SILHOUETTE)

    # Body — near side wider, far side compressed
    near_bw = int(hu * 0.44)
    far_bw  = int(hu * 0.22)
    body_h  = int(hu * 2.4)
    body_top_y = hy + hh
    body_bot_y = body_top_y + body_h
    draw.polygon([(cx - near_bw, body_top_y), (cx + far_bw, body_top_y),
                  (cx + far_bw, body_bot_y), (cx - near_bw, body_bot_y)],
                 fill=SILHOUETTE)

    # Notebook — near side arm (protruding from left edge)
    nw = int(hu * 0.48)
    nh = int(hu * 0.58)
    nb_y = body_top_y + int(body_h * 0.28)
    draw.rectangle([cx - near_bw - nw + 8, nb_y, cx - near_bw + 8, nb_y + nh], fill=SILHOUETTE)

    # Legs (3/4 near + far; ensure far leg has positive width)
    lw = int(hu * 0.18)
    leg_h = int(hu * 0.60)
    draw.rectangle([cx - near_bw + 4, body_bot_y, cx - lw, body_bot_y + leg_h], fill=SILHOUETTE)
    far_leg_x1 = cx + lw
    far_leg_x2 = cx + max(far_bw - 4, lw + 8)   # guard against inversion
    draw.rectangle([far_leg_x1, body_bot_y, far_leg_x2, body_bot_y + leg_h], fill=SILHOUETTE)

    # Shoes
    fw = int(hu * 0.28)
    fh = int(hu * 0.18)
    draw.ellipse([cx - near_bw + 4 - int(fw*0.4), base_y - fh, cx - lw + int(fw*0.6), base_y],
                 fill=SILHOUETTE)
    far_shoe_x2 = cx + max(far_bw - 4, lw + 8) + int(fw*0.3)
    draw.ellipse([cx + lw - int(fw*0.3), base_y - fh, far_shoe_x2, base_y],
                 fill=SILHOUETTE)


def draw_cosmo_side(draw, cx, base_y):
    """Cosmo — side (profile) view. Glasses show as a single lens in profile — one round
    protrusion from the face silhouette, establishing the glasses from every angle.
    Notebook visible as thin edge protruding behind body.
    """
    hu = _cosmo_head_unit()
    h  = CHAR_H
    hy = base_y - h

    hw = int(hu * 0.40)
    hh = int(hu * 0.95)
    # Slight chin projection for profile
    head_depth = int(hu * 0.62)
    front_x = cx - int(head_depth * 0.60)
    back_x  = cx + int(head_depth * 0.40)
    draw.rounded_rectangle([front_x, hy, back_x, hy + hh], radius=6, fill=SILHOUETTE)

    # Glasses — in side profile: one lens as circular protrusion beyond front face.
    # Cycle 12: refactored to call _draw_cosmo_glasses(is_side=True) for consistency
    # with front, 3/4, and back views. Inline code removed.
    gr = int(hu * 0.18)
    gy = hy + int(hh * 0.48)
    _draw_cosmo_glasses(draw, cx=front_x, gy=gy, gr=gr,
                        is_front=False, is_back=False, is_side=True,
                        front_x=front_x)

    # Hair — extends slightly behind head
    draw.ellipse([front_x - 2, hy - int(hu*0.08), back_x + int(hu*0.14), hy + int(hu*0.12)],
                 fill=SILHOUETTE)

    # Body — narrow in profile
    body_depth = int(hu * 0.56)
    body_h     = int(hu * 2.4)
    body_top_y = hy + hh
    body_bot_y = body_top_y + body_h
    b_front = cx - int(body_depth * 0.62)
    b_back  = cx + int(body_depth * 0.38)
    draw.rectangle([b_front, body_top_y, b_back, body_bot_y], fill=SILHOUETTE)

    # Notebook — thin edge visible sticking out back of body in profile
    draw.rectangle([b_back, body_top_y + int(body_h*0.28),
                    b_back + int(hu*0.10), body_top_y + int(body_h*0.28) + int(hu*0.58)],
                   fill=SILHOUETTE)

    # Leg
    lw = int(hu * 0.18)
    leg_h = int(hu * 0.60)
    leg_cx = cx - int(hu * 0.10)
    draw.rectangle([leg_cx - lw, body_bot_y, leg_cx + lw, body_bot_y + leg_h], fill=SILHOUETTE)

    # Shoe
    fw = int(hu * 0.40)
    fh = int(hu * 0.18)
    draw.ellipse([leg_cx - fw + int(fw*0.2), base_y - fh, leg_cx + int(fw*0.5), base_y],
                 fill=SILHOUETTE)


def draw_cosmo_back(draw, cx, base_y):
    """Cosmo — back view. No glasses visible. Back of head, plain body, notebook
    spine visible peeking left. Back of shoes.
    """
    hu = _cosmo_head_unit()
    h  = CHAR_H
    hy = base_y - h

    hw = int(hu * 0.40)
    hh = int(hu * 0.95)
    draw.rounded_rectangle([cx - hw, hy, cx + hw, hy + hh], radius=6, fill=SILHOUETTE)

    # Hair from back — cowlick silhouette visible on left
    draw.ellipse([cx - hw - 4, hy - int(hu*0.08), cx + hw + 4, hy + int(hu*0.12)],
                 fill=SILHOUETTE)
    draw.ellipse([cx - hw - 2, hy - int(hu*0.22), cx - int(hw*0.2), hy + int(hu*0.05)],
                 fill=SILHOUETTE)

    # Body
    bw = int(hu * 0.38)
    body_h = int(hu * 2.4)
    body_top_y = hy + hh
    body_bot_y = body_top_y + body_h
    draw.rectangle([cx - bw, body_top_y, cx + bw, body_bot_y], fill=SILHOUETTE)

    # Notebook spine peeking left from behind body
    nb_y = body_top_y + int(body_h * 0.28)
    draw.rectangle([cx - bw - int(hu*0.10), nb_y, cx - bw, nb_y + int(hu*0.58)], fill=SILHOUETTE)

    # Pants center crease — vertical line on back
    crease_top = body_bot_y - int(body_h * 0.60)
    draw.line([(cx, crease_top), (cx, body_bot_y)], fill=BG, width=2)

    # Legs
    lw = int(hu * 0.18)
    leg_h = int(hu * 0.60)
    draw.rectangle([cx - bw + 4, body_bot_y, cx - lw, body_bot_y + leg_h], fill=SILHOUETTE)
    draw.rectangle([cx + lw, body_bot_y, cx + bw - 4, body_bot_y + leg_h], fill=SILHOUETTE)

    # Shoes — heel forward from back
    fw = int(hu * 0.28)
    fh = int(hu * 0.18)
    draw.ellipse([cx - bw + 4 - int(fw*0.2), base_y - fh, cx - lw + int(fw*0.6), base_y],
                 fill=SILHOUETTE)
    draw.ellipse([cx + lw - int(fw*0.3), base_y - fh, cx + bw - 4 + int(fw*0.2), base_y],
                 fill=SILHOUETTE)


# ══════════════════════════════════════════════════════════════════════════════
# MIRI TURNAROUND VIEWS
# Miri (MIRI-A — CANONICAL): 3.2 heads tall, sturdy and warm.
# Defining elements: tall oval bun + V-pair chopsticks, wide inverted-flare cardigan,
# soldering iron held at side. Silver hair. Terracotta rust cardigan.
# ══════════════════════════════════════════════════════════════════════════════

def _miri_head_unit():
    """Miri is 3.2 heads tall at CHAR_H=200px."""
    return CHAR_H / 3.2


def draw_miri_front(draw, cx, base_y):
    """Miri — front view. Bun + chopsticks prominent above head.
    Wide cardigan (inverted-flare trapezoid). Soldering iron on right side.
    """
    hu = _miri_head_unit()
    h  = CHAR_H
    hy = base_y - h

    r = int(hu * 0.46)

    # BUN — large oval mass sitting above head (primary silhouette hook)
    bun_cx = cx + int(hu * 0.05)
    bun_cy = hy - int(hu * 0.32)
    bun_rx = int(hu * 0.38)
    bun_ry = int(hu * 0.46)
    draw.ellipse([bun_cx - bun_rx, bun_cy - bun_ry,
                  bun_cx + bun_rx, bun_cy + bun_ry], fill=SILHOUETTE)

    # CHOPSTICKS — V-pair spikes piercing bun
    draw.polygon([(bun_cx - int(hu*0.22), bun_cy - bun_ry - int(hu*0.55)),
                  (bun_cx - int(hu*0.14), bun_cy - bun_ry - int(hu*0.55)),
                  (bun_cx - int(hu*0.06), bun_cy + bun_ry - int(hu*0.12)),
                  (bun_cx - int(hu*0.13), bun_cy + bun_ry - int(hu*0.12))],
                 fill=SILHOUETTE)
    draw.polygon([(bun_cx + int(hu*0.14), bun_cy - bun_ry - int(hu*0.50)),
                  (bun_cx + int(hu*0.22), bun_cy - bun_ry - int(hu*0.50)),
                  (bun_cx + int(hu*0.13), bun_cy + bun_ry - int(hu*0.12)),
                  (bun_cx + int(hu*0.06), bun_cy + bun_ry - int(hu*0.12))],
                 fill=SILHOUETTE)

    # Head (round)
    draw.ellipse([cx - r, hy, cx + r, hy + int(hu)], fill=SILHOUETTE)

    # CARDIGAN — wide inverted-flare (wide shoulders, narrower hip)
    shoulder_w = int(hu * 0.78)
    hip_w      = int(hu * 0.62)
    body_top_y = hy + int(hu * 0.88)
    body_h     = int(hu * 1.82)
    body_bot_y = body_top_y + body_h
    draw.polygon([(cx - shoulder_w, body_top_y), (cx + shoulder_w, body_top_y),
                  (cx + hip_w, body_bot_y), (cx - hip_w, body_bot_y)],
                 fill=SILHOUETTE)

    # Bag — protrudes right hip
    bag_x = cx + hip_w
    bag_y = body_top_y + int(body_h * 0.52)
    bag_w = int(hu * 0.32)
    bag_h = int(hu * 0.46)
    draw.rectangle([bag_x, bag_y, bag_x + bag_w, bag_y + bag_h], fill=SILHOUETTE)

    # SOLDERING IRON — right hand, extends right
    iron_x = bag_x + bag_w
    iron_y = bag_y + bag_h - int(hu * 0.04)
    iron_len = int(hu * 0.50)
    iron_w   = int(hu * 0.07)
    draw.rectangle([iron_x, iron_y, iron_x + iron_len - int(iron_len*0.22), iron_y + iron_w + 2],
                   fill=SILHOUETTE)
    draw.polygon([(iron_x + iron_len - int(iron_len*0.22), iron_y),
                  (iron_x + iron_len - int(iron_len*0.22), iron_y + iron_w + 2),
                  (iron_x + iron_len, iron_y + (iron_w + 2)//2)],
                 fill=SILHOUETTE)

    # Legs
    lw = int(hu * 0.22)
    leg_h = int(hu * 0.45)
    draw.rectangle([cx - hip_w + 6, body_bot_y, cx - lw, body_bot_y + leg_h], fill=SILHOUETTE)
    draw.rectangle([cx + lw, body_bot_y, cx + hip_w - 6, body_bot_y + leg_h], fill=SILHOUETTE)

    # Feet — sturdy block feet
    fw = int(hu * 0.30)
    fh = int(hu * 0.18)
    draw.rectangle([cx - hip_w + 4, base_y - fh, cx - lw + int(fw*0.4), base_y], fill=SILHOUETTE)
    draw.rectangle([cx + lw - int(fw*0.4), base_y - fh, cx + hip_w - 4, base_y], fill=SILHOUETTE)


def draw_miri_three_quarter(draw, cx, base_y):
    """Miri — 3/4 view. Bun + chopstick pair visible (near side fuller).
    Cardigan near shoulder wider. Soldering iron + bag visible at near side.
    """
    hu = _miri_head_unit()
    h  = CHAR_H
    hy = base_y - h
    r = int(hu * 0.46)

    # BUN — near side slightly wider in 3/4
    bun_cx = cx - int(hu * 0.08)
    bun_cy = hy - int(hu * 0.32)
    bun_rx_near = int(hu * 0.42)
    bun_rx_far  = int(hu * 0.30)
    bun_ry = int(hu * 0.46)
    draw.ellipse([bun_cx - bun_rx_near, bun_cy - bun_ry,
                  bun_cx + bun_rx_far, bun_cy + bun_ry], fill=SILHOUETTE)
    # Near-side depth blob
    draw.ellipse([bun_cx - bun_rx_near - int(hu*0.06), bun_cy - int(bun_ry*0.5),
                  bun_cx - int(bun_rx_near*0.4), bun_cy + int(bun_ry*0.4)], fill=SILHOUETTE)

    # CHOPSTICKS — V-pair visible, near chopstick fully shown
    draw.polygon([(bun_cx - int(hu*0.20), bun_cy - bun_ry - int(hu*0.55)),
                  (bun_cx - int(hu*0.12), bun_cy - bun_ry - int(hu*0.55)),
                  (bun_cx - int(hu*0.05), bun_cy + bun_ry - int(hu*0.12)),
                  (bun_cx - int(hu*0.12), bun_cy + bun_ry - int(hu*0.12))],
                 fill=SILHOUETTE)
    draw.polygon([(bun_cx + int(hu*0.10), bun_cy - bun_ry - int(hu*0.45)),
                  (bun_cx + int(hu*0.18), bun_cy - bun_ry - int(hu*0.45)),
                  (bun_cx + int(hu*0.11), bun_cy + bun_ry - int(hu*0.12)),
                  (bun_cx + int(hu*0.04), bun_cy + bun_ry - int(hu*0.12))],
                 fill=SILHOUETTE)

    # Head (slightly oval in 3/4)
    draw.ellipse([cx - int(r*0.95), hy, cx + int(r*0.78), hy + int(hu)], fill=SILHOUETTE)

    # Body — near shoulder wider, far compressed
    near_sw = int(hu * 0.84)
    far_sw  = int(hu * 0.42)
    near_hw = int(hu * 0.68)
    far_hw  = int(hu * 0.34)
    body_top_y = hy + int(hu * 0.88)
    body_h     = int(hu * 1.82)
    body_bot_y = body_top_y + body_h
    draw.polygon([(cx - near_sw, body_top_y), (cx + far_sw, body_top_y),
                  (cx + far_hw, body_bot_y), (cx - near_hw, body_bot_y)],
                 fill=SILHOUETTE)

    # Bag + soldering iron on near side
    bag_x = cx + far_hw
    bag_y = body_top_y + int(body_h * 0.52)
    draw.rectangle([bag_x, bag_y, bag_x + int(hu*0.28), bag_y + int(hu*0.42)], fill=SILHOUETTE)
    iron_x = bag_x + int(hu*0.28)
    draw.rectangle([iron_x, bag_y + int(hu*0.38), iron_x + int(hu*0.40), bag_y + int(hu*0.46)],
                   fill=SILHOUETTE)

    # Near arm visible
    arm_y = body_top_y + int(body_h * 0.10)
    draw.rectangle([cx - near_sw - int(hu*0.20), arm_y,
                    cx - near_sw, arm_y + int(hu*0.55)], fill=SILHOUETTE)

    # Legs
    lw = int(hu * 0.22)
    leg_h = int(hu * 0.45)
    draw.rectangle([cx - near_hw + 6, body_bot_y, cx - lw, body_bot_y + leg_h], fill=SILHOUETTE)
    draw.rectangle([cx + lw, body_bot_y, cx + far_hw - 6, body_bot_y + leg_h], fill=SILHOUETTE)

    # Feet
    fw = int(hu * 0.30)
    fh = int(hu * 0.18)
    draw.rectangle([cx - near_hw + 4, base_y - fh, cx - lw + int(fw*0.4), base_y], fill=SILHOUETTE)
    draw.rectangle([cx + lw - int(fw*0.4), base_y - fh, cx + far_hw - 4, base_y], fill=SILHOUETTE)


def draw_miri_side(draw, cx, base_y):
    """Miri — side (profile) view. Bun reads as tall oval behind/above head.
    One chopstick visible in profile. Cardigan reads as a wide wedge.
    Soldering iron extends forward from right hand.
    """
    hu = _miri_head_unit()
    h  = CHAR_H
    hy = base_y - h
    r = int(hu * 0.46)

    # BUN — side profile: oval extending above and slightly behind head
    bun_cx = cx + int(hu * 0.10)
    bun_cy = hy - int(hu * 0.32)
    bun_rx = int(hu * 0.20)   # narrow in profile
    bun_ry = int(hu * 0.46)
    draw.ellipse([bun_cx - bun_rx, bun_cy - bun_ry,
                  bun_cx + bun_rx, bun_cy + bun_ry], fill=SILHOUETTE)

    # One chopstick visible in profile (near one, pointing upward at angle)
    draw.polygon([(bun_cx - int(hu*0.08), bun_cy - bun_ry - int(hu*0.52)),
                  (bun_cx - int(hu*0.02), bun_cy - bun_ry - int(hu*0.52)),
                  (bun_cx + int(hu*0.04), bun_cy + bun_ry - int(hu*0.10)),
                  (bun_cx - int(hu*0.02), bun_cy + bun_ry - int(hu*0.10))],
                 fill=SILHOUETTE)

    # Head — in profile
    head_depth = int(hu * 0.62)
    front_x = cx - int(head_depth * 0.60)
    back_x  = cx + int(head_depth * 0.40)
    draw.ellipse([front_x, hy, back_x, hy + int(hu)], fill=SILHOUETTE)

    # Body — side view of cardigan: wide wedge (depth of wide shoulders)
    body_depth_top = int(hu * 0.88)
    body_depth_bot = int(hu * 0.70)
    body_top_y = hy + int(hu * 0.88)
    body_h     = int(hu * 1.82)
    body_bot_y = body_top_y + body_h
    front_top = cx - int(body_depth_top * 0.55)
    back_top  = cx + int(body_depth_top * 0.45)
    front_bot = cx - int(body_depth_bot * 0.55)
    back_bot  = cx + int(body_depth_bot * 0.45)
    draw.polygon([(front_top, body_top_y), (back_top, body_top_y),
                  (back_bot, body_bot_y), (front_bot, body_bot_y)],
                 fill=SILHOUETTE)

    # Soldering iron extends forward from front edge (right hand, near side)
    iron_y = body_top_y + int(body_h * 0.62)
    iron_len = int(hu * 0.50)
    iron_w   = int(hu * 0.07)
    draw.rectangle([front_bot - iron_len, iron_y,
                    front_bot, iron_y + iron_w + 2], fill=SILHOUETTE)
    draw.polygon([(front_bot - iron_len, iron_y),
                  (front_bot - iron_len, iron_y + iron_w + 2),
                  (front_bot - iron_len - int(hu*0.08), iron_y + (iron_w+2)//2)],
                 fill=SILHOUETTE)

    # Leg (single in profile, slightly forward)
    lw = int(hu * 0.22)
    leg_h = int(hu * 0.45)
    leg_cx = cx - int(hu * 0.08)
    draw.rectangle([leg_cx - lw, body_bot_y, leg_cx + lw, body_bot_y + leg_h], fill=SILHOUETTE)

    # Foot in profile — block slipper
    fw = int(hu * 0.42)
    fh = int(hu * 0.18)
    draw.rectangle([leg_cx - fw + int(fw*0.2), base_y - fh, leg_cx + int(fw*0.3), base_y],
                   fill=SILHOUETTE)


def draw_miri_back(draw, cx, base_y):
    """Miri — back view. Bun + chopstick pair from behind — distinctive silhouette hook.
    Plain cardigan back. No bag (on right side, hidden). No soldering iron.
    """
    hu = _miri_head_unit()
    h  = CHAR_H
    hy = base_y - h
    r = int(hu * 0.46)

    # BUN from back — same oval profile, chopsticks V-pair visible above bun
    bun_cx = cx + int(hu * 0.05)
    bun_cy = hy - int(hu * 0.32)
    bun_rx = int(hu * 0.38)
    bun_ry = int(hu * 0.46)
    draw.ellipse([bun_cx - bun_rx, bun_cy - bun_ry,
                  bun_cx + bun_rx, bun_cy + bun_ry], fill=SILHOUETTE)

    # Chopsticks V-pair from behind (same geometry — symmetry means they look the same)
    draw.polygon([(bun_cx - int(hu*0.22), bun_cy - bun_ry - int(hu*0.55)),
                  (bun_cx - int(hu*0.14), bun_cy - bun_ry - int(hu*0.55)),
                  (bun_cx - int(hu*0.06), bun_cy + bun_ry - int(hu*0.12)),
                  (bun_cx - int(hu*0.13), bun_cy + bun_ry - int(hu*0.12))],
                 fill=SILHOUETTE)
    draw.polygon([(bun_cx + int(hu*0.14), bun_cy - bun_ry - int(hu*0.50)),
                  (bun_cx + int(hu*0.22), bun_cy - bun_ry - int(hu*0.50)),
                  (bun_cx + int(hu*0.13), bun_cy + bun_ry - int(hu*0.12)),
                  (bun_cx + int(hu*0.06), bun_cy + bun_ry - int(hu*0.12))],
                 fill=SILHOUETTE)

    # Head (back of head)
    draw.ellipse([cx - r, hy, cx + r, hy + int(hu)], fill=SILHOUETTE)

    # Cardigan back — plain inverted-flare trapezoid
    shoulder_w = int(hu * 0.78)
    hip_w      = int(hu * 0.62)
    body_top_y = hy + int(hu * 0.88)
    body_h     = int(hu * 1.82)
    body_bot_y = body_top_y + body_h
    draw.polygon([(cx - shoulder_w, body_top_y), (cx + shoulder_w, body_top_y),
                  (cx + hip_w, body_bot_y), (cx - hip_w, body_bot_y)],
                 fill=SILHOUETTE)

    # Legs
    lw = int(hu * 0.22)
    leg_h = int(hu * 0.45)
    draw.rectangle([cx - hip_w + 6, body_bot_y, cx - lw, body_bot_y + leg_h], fill=SILHOUETTE)
    draw.rectangle([cx + lw, body_bot_y, cx + hip_w - 6, body_bot_y + leg_h], fill=SILHOUETTE)

    # Feet (back of slippers)
    fw = int(hu * 0.30)
    fh = int(hu * 0.18)
    draw.rectangle([cx - hip_w + 4, base_y - fh, cx - lw + int(fw*0.4), base_y], fill=SILHOUETTE)
    draw.rectangle([cx + lw - int(fw*0.4), base_y - fh, cx + hip_w - 4, base_y], fill=SILHOUETTE)


# ══════════════════════════════════════════════════════════════════════════════
# STRIP GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

LUMA_VIEW_DRAWERS = [
    draw_luma_front,
    draw_luma_three_quarter,
    draw_luma_side,
    draw_luma_back,
]

BYTE_VIEW_DRAWERS = [
    draw_byte_front,
    draw_byte_three_quarter,
    draw_byte_side,
    draw_byte_back,
]

COSMO_VIEW_DRAWERS = [
    draw_cosmo_front,
    draw_cosmo_three_quarter,
    draw_cosmo_side,
    draw_cosmo_back,
]

MIRI_VIEW_DRAWERS = [
    draw_miri_front,
    draw_miri_three_quarter,
    draw_miri_side,
    draw_miri_back,
]


def generate_turnaround(char_name, view_drawers, output_path):
    """Generate a 4-view turnaround strip for a character.

    Layout: [FRONT | 3/4 | SIDE | BACK] — labeled below each panel.
    Character name as title above the strip.
    Scale bar at bottom (100px = 1 head unit for Luma; 1 body unit for Byte).
    """
    img = Image.new('RGB', (STRIP_W, STRIP_H), BG)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
        font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except Exception:
        font_title = font_label = font_small = ImageFont.load_default()

    # Title bar
    title_text = f"{char_name.upper()} — CHARACTER TURNAROUND — Cycle 10"
    draw.text((16, 8), title_text, fill=LABEL_COL, font=font_title)
    draw.line([(0, TITLE_H - 4), (STRIP_W, TITLE_H - 4)], fill=TICK_COL, width=1)

    # Ground line Y (consistent across all panels)
    ground_y = TITLE_H + 60 + CHAR_H   # 60px headroom above character top

    for i, (view_name, view_fn) in enumerate(zip(VIEWS, view_drawers)):
        panel_x = i * VIEW_W
        panel_end = panel_x + VIEW_W
        cx = panel_x + VIEW_W // 2

        # Panel background
        draw.rectangle([panel_x + 4, TITLE_H, panel_end - 4, STRIP_H - 4], fill=PANEL_BG)

        # Ground tick marks
        draw.line([(panel_x + 20, ground_y), (panel_end - 20, ground_y)],
                  fill=TICK_COL, width=1)

        # Draw character view
        view_fn(draw, cx, ground_y)

        # Height annotation line on first panel
        if i == 0:
            # Compute approx top of character for height line
            top_y = TITLE_H + 8
            draw.line([(panel_x + 8, top_y), (panel_x + 8, ground_y)],
                      fill=TICK_COL, width=1)
            draw.line([(panel_x + 5, top_y), (panel_x + 11, top_y)],
                      fill=TICK_COL, width=1)
            draw.line([(panel_x + 5, ground_y), (panel_x + 11, ground_y)],
                      fill=TICK_COL, width=1)
            draw.text((panel_x + 14, (top_y + ground_y)//2 - 5),
                      f"{CHAR_H}px", fill=TICK_COL, font=font_small)

        # Panel separator line
        if i > 0:
            draw.line([(panel_x + 4, TITLE_H), (panel_x + 4, STRIP_H - 4)],
                      fill=TICK_COL, width=1)

        # View label below ground line
        label_x = cx - len(view_name) * 4
        draw.text((label_x, ground_y + 10), view_name, fill=LABEL_COL, font=font_label)

    # Footer note
    draw.text((16, STRIP_H - 18),
              f"All views at consistent {CHAR_H}px character height. "
              "Hover particles indicate floating clearance for Byte.",
              fill=TICK_COL, font=font_small)

    img.save(output_path)
    print(f"Saved: {output_path}")


def main():
    import os
    out_dir = "/home/wipkat/team/output/characters/main/turnarounds"
    os.makedirs(out_dir, exist_ok=True)

    generate_turnaround(
        "Luma",
        LUMA_VIEW_DRAWERS,
        os.path.join(out_dir, "luma_turnaround.png")
    )
    generate_turnaround(
        "Byte",
        BYTE_VIEW_DRAWERS,
        os.path.join(out_dir, "byte_turnaround.png")
    )
    # Cycle 12: new versioned file — glasses refactored to use _draw_cosmo_glasses(is_side=True)
    generate_turnaround(
        "Cosmo",
        COSMO_VIEW_DRAWERS,
        os.path.join(out_dir, "LTG_CHAR_cosmo_turnaround_v002.png")
    )
    generate_turnaround(
        "Miri",
        MIRI_VIEW_DRAWERS,
        os.path.join(out_dir, "miri_turnaround.png")
    )
    print("Turnaround generation complete — all 4 characters.")


if __name__ == '__main__':
    main()
