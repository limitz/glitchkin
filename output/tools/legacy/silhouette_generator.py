# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
Character Silhouette Sheet Generator — Luma & the Glitchkin
Generates solid-black silhouettes of all characters at correct relative sizes.
Cycle 6 fixes:
  - Cosmo's glasses render as white negative-space cutouts
  - Luma's pocket bump protrudes OUTSIDE the hem boundary
  - Cosmo now has foot shapes
  - Miri has a distinctive shoulder bag hook
  - Second column of action poses added for all characters
"""
from PIL import Image, ImageDraw, ImageFont

BG = (255, 255, 255)
SILHOUETTE = (15, 10, 20)
NEG_SPACE  = (255, 255, 255)   # white "cutout" for glasses, etc.
OUTLINE_COL = (180, 170, 160)
TEXT_COL = (60, 50, 40)

# Luma is the reference: 3.5 heads at 280px tall
LUMA_H = 280
HEAD_UNIT = LUMA_H / 3.5


# ─────────────────────────────────────────────────────────────────
# NEUTRAL STANCES
# ─────────────────────────────────────────────────────────────────

def draw_luma(draw, cx, base_y):
    """Luma — neutral stance.
    Key hook: hoodie has a flared trapezoid hem (A-line shape).
    Oversized sneakers. Pocket bump protrudes OUTSIDE the hem edge.
    """
    h = LUMA_H
    hu = HEAD_UNIT
    # Head (round)
    r = int(hu * 0.46)
    hy = base_y - h
    draw.ellipse([cx - r, hy, cx + r, hy + int(hu)], fill=SILHOUETTE)
    # Big curly hair — wider blob on top
    draw.ellipse([cx - int(r*1.5), hy - int(r*0.6), cx + int(r*1.5), hy + int(r*0.8)], fill=SILHOUETTE)

    # Body — HOODIE: trapezoid A-line shape (narrow top, flared hem)
    shoulder_w = int(hu * 0.38)   # narrow shoulders
    hem_w      = int(hu * 0.70)   # wide flared hem
    body_top_y = hy + int(hu * 0.85)
    body_h     = int(hu * 2.0)
    body_bot_y = body_top_y + body_h

    body_pts = [
        (cx - shoulder_w, body_top_y),
        (cx + shoulder_w, body_top_y),
        (cx + hem_w,      body_bot_y),
        (cx - hem_w,      body_bot_y),
    ]
    draw.polygon(body_pts, fill=SILHOUETTE)

    # Pocket bump — protrudes OUTSIDE the hem edge (right side)
    # hem edge at mid-body y is approximately cx + hem_w * fraction
    mid_body_frac = 0.55
    hem_edge_at_mid = cx + int(shoulder_w + (hem_w - shoulder_w) * mid_body_frac)
    pocket_y = body_top_y + int(body_h * 0.50)
    pocket_w = int(hu * 0.30)   # wide enough to clearly protrude
    pocket_h = int(hu * 0.42)
    # Start at the hem edge so bump clearly exits the body silhouette
    draw.rectangle([hem_edge_at_mid, pocket_y,
                    hem_edge_at_mid + pocket_w, pocket_y + pocket_h],
                   fill=SILHOUETTE)

    # Legs
    lw = int(hu * 0.20)
    leg_h = int(hu * 0.55)
    leg_top_y = body_bot_y
    draw.rectangle([cx - lw*2, leg_top_y, cx - 4, leg_top_y + leg_h], fill=SILHOUETTE)
    draw.rectangle([cx + 4, leg_top_y, cx + lw*2, leg_top_y + leg_h], fill=SILHOUETTE)

    # Feet — OVERSIZED chunky sneakers
    fw = int(hu * 0.52)
    fh = int(hu * 0.28)
    draw.ellipse([cx - lw*2 - fw + int(fw*0.3), base_y - fh,
                  cx - lw*2 + int(fw*0.5),       base_y], fill=SILHOUETTE)
    draw.ellipse([cx + lw*2 - int(fw*0.5),        base_y - fh,
                  cx + lw*2 + fw - int(fw*0.3),   base_y], fill=SILHOUETTE)


def draw_cosmo(draw, cx, base_y):
    """Cosmo — neutral stance.
    Fixes: glasses as white negative-space cutouts; feet added.
    """
    hu = HEAD_UNIT
    h = int(4.0 * hu)
    hy = base_y - h
    # Head (rectangle, narrower)
    hw = int(hu * 0.4)
    hh = int(hu * 0.95)
    draw.rounded_rectangle([cx - hw, hy, cx + hw, hy + hh], radius=6, fill=SILHOUETTE)

    # Glasses — FILLED BLACK first (already part of silhouette), then
    # WHITE cutout inside so they register as negative space
    gr = int(hu * 0.18)
    gy = hy + int(hh * 0.45)
    lcx = cx - int(hu * 0.28)
    rcx = cx + int(hu * 0.28)
    # Outer rim (wider, in silhouette color)
    rim_extra = 3
    draw.ellipse([lcx - gr - rim_extra, gy - gr - rim_extra,
                  lcx + gr + rim_extra, gy + gr + rim_extra], fill=SILHOUETTE)
    draw.ellipse([rcx - gr - rim_extra, gy - gr - rim_extra,
                  rcx + gr + rim_extra, gy + gr + rim_extra], fill=SILHOUETTE)
    # Inner lens — white cutout (negative space = readable in silhouette)
    draw.ellipse([lcx - gr, gy - gr, lcx + gr, gy + gr], fill=NEG_SPACE)
    draw.ellipse([rcx - gr, gy - gr, rcx + gr, gy + gr], fill=NEG_SPACE)
    # Glasses bridge
    draw.rectangle([lcx + gr, gy - 3, rcx - gr, gy + 3], fill=SILHOUETTE)

    # Body (narrow rectangle)
    bw = int(hu * 0.38)
    body_h = int(hu * 2.4)
    draw.rectangle([cx - bw, hy + hh, cx + bw, hy + hh + body_h], fill=SILHOUETTE)
    # Notebook under left arm — extends left silhouette
    nw = int(hu * 0.5)
    nh = int(hu * 0.6)
    draw.rectangle([cx - bw - nw + 10, hy + hh + int(body_h*0.3),
                    cx - bw + 10, hy + hh + int(body_h*0.3) + nh], fill=SILHOUETTE)
    # Legs
    lw = int(hu * 0.18)
    leg_h = int(hu * 0.6)
    draw.rectangle([cx - bw + 4, hy + hh + body_h, cx - lw, hy + hh + body_h + leg_h], fill=SILHOUETTE)
    draw.rectangle([cx + lw, hy + hh + body_h, cx + bw - 4, hy + hh + body_h + leg_h], fill=SILHOUETTE)

    # FEET — minimal shoe shapes (previously missing)
    fw = int(hu * 0.28)
    fh = int(hu * 0.18)
    # Left foot pointing slightly left
    draw.ellipse([cx - bw + 4 - int(fw*0.4), base_y - fh,
                  cx - lw + int(fw*0.6),      base_y], fill=SILHOUETTE)
    # Right foot pointing slightly right
    draw.ellipse([cx + lw - int(fw*0.3),      base_y - fh,
                  cx + bw - 4 + int(fw*0.4),  base_y], fill=SILHOUETTE)


def draw_byte(draw, cx, base_y):
    """Byte — neutral stance, arm visible (not merged into body)."""
    hu = HEAD_UNIT
    s = int(LUMA_H * 0.20)
    hy = base_y - s
    c = int(s * 0.15)
    pts = [(cx - s//2 + c, hy), (cx + s//2 - c, hy),
           (cx + s//2, hy + c), (cx + s//2, hy + s - c),
           (cx + s//2 - c, hy + s), (cx - s//2 + c, hy + s),
           (cx - s//2, hy + s - c), (cx - s//2, hy + c)]
    draw.polygon(pts, fill=SILHOUETTE)
    # Stubby limbs — made slightly larger so they read in silhouette
    lw = int(s * 0.22)
    lh = int(s * 0.25)
    arm_y = hy + s//3
    draw.rectangle([cx - s//2 - lw, arm_y, cx - s//2, arm_y + lh], fill=SILHOUETTE)
    draw.rectangle([cx + s//2, arm_y, cx + s//2 + lw, arm_y + lh], fill=SILHOUETTE)
    # Legs
    leg_w = int(s * 0.18)
    leg_h = int(s * 0.20)
    draw.rectangle([cx - s//4 - leg_w//2, hy + s,
                    cx - s//4 + leg_w//2, hy + s + leg_h], fill=SILHOUETTE)
    draw.rectangle([cx + s//4 - leg_w//2, hy + s,
                    cx + s//4 + leg_w//2, hy + s + leg_h], fill=SILHOUETTE)


def draw_miri(draw, cx, base_y):
    """Miri — VARIANT A (neutral stance).
    Design hook: WIDE BUN WITH CHOPSTICK PAIR (tall stacked bun + two spikes).
    Wide cardigan silhouette: trapezoid, wider at shoulder than hip (inverted-flare).
    Prop: soldering iron held at side (small spike from right hand).
    Bag stays as secondary contour element.
    Communicates: grandmotherly warmth (wide cardigan) + maker/hacker (soldering iron, bun-chopsticks).
    """
    hu = HEAD_UNIT
    h = int(3.2 * hu)
    hy = base_y - h
    r = int(hu * 0.46)

    # HAIR: large domed bun sitting HIGH above head — this is the primary silhouette hook.
    # Bun is taller than it is wide — a distinctive vertical mass.
    bun_cx = cx + int(hu * 0.06)   # very slight right offset
    bun_cy = hy - int(hu * 0.32)
    bun_rx = int(hu * 0.38)
    bun_ry = int(hu * 0.46)        # taller bun — vertical emphasis
    draw.ellipse([bun_cx - bun_rx, bun_cy - bun_ry,
                  bun_cx + bun_rx, bun_cy + bun_ry], fill=SILHOUETTE)
    # CHOPSTICKS — two thin spikes piercing the bun at slight angles (V-pair)
    # Left chopstick: angled left and upward
    draw.polygon([(bun_cx - int(hu*0.22), bun_cy - bun_ry - int(hu*0.58)),
                  (bun_cx - int(hu*0.14), bun_cy - bun_ry - int(hu*0.58)),
                  (bun_cx - int(hu*0.06), bun_cy + bun_ry - int(hu*0.12)),
                  (bun_cx - int(hu*0.13), bun_cy + bun_ry - int(hu*0.12))],
                 fill=SILHOUETTE)
    # Right chopstick: angled right and upward
    draw.polygon([(bun_cx + int(hu*0.14), bun_cy - bun_ry - int(hu*0.52)),
                  (bun_cx + int(hu*0.22), bun_cy - bun_ry - int(hu*0.52)),
                  (bun_cx + int(hu*0.13), bun_cy + bun_ry - int(hu*0.12)),
                  (bun_cx + int(hu*0.06), bun_cy + bun_ry - int(hu*0.12))],
                 fill=SILHOUETTE)

    # Head (round, grandmotherly proportions)
    draw.ellipse([cx - r, hy, cx + r, hy + int(hu)], fill=SILHOUETTE)

    # CARDIGAN body — WIDE at shoulders, tapers slightly to hip (warmth silhouette).
    # Wider shoulders read as settled authority; the taper keeps shape interesting.
    shoulder_w = int(hu * 0.78)    # very wide cardigan shoulders
    hip_w      = int(hu * 0.62)    # narrow slightly at hip
    body_top_y = hy + int(hu * 0.88)
    body_h     = int(hu * 1.82)
    body_bot_y = body_top_y + body_h
    body_pts = [
        (cx - shoulder_w, body_top_y),
        (cx + shoulder_w, body_top_y),
        (cx + hip_w,      body_bot_y),
        (cx - hip_w,      body_bot_y),
    ]
    draw.polygon(body_pts, fill=SILHOUETTE)

    # SHOULDER BAG — protrudes from right hip (functional, not defining)
    bag_x = cx + hip_w
    bag_y = body_top_y + int(body_h * 0.52)
    bag_w = int(hu * 0.34)
    bag_h = int(hu * 0.48)
    draw.rectangle([bag_x, bag_y, bag_x + bag_w, bag_y + bag_h], fill=SILHOUETTE)
    # Strap tab at top of bag
    draw.rectangle([bag_x + int(bag_w*0.15), bag_y - int(hu*0.10),
                    bag_x + int(bag_w*0.65), bag_y], fill=SILHOUETTE)

    # SOLDERING IRON — held in right hand, slightly below bag.
    # Thin handle + pointed tip: small but unmistakable tech-tool silhouette hook.
    iron_base_x = bag_x + bag_w
    iron_base_y = bag_y + bag_h - int(hu * 0.04)
    iron_len    = int(hu * 0.52)
    iron_w      = int(hu * 0.07)
    # Handle (slightly thicker rectangle)
    draw.rectangle([iron_base_x, iron_base_y,
                    iron_base_x + iron_len - int(iron_len*0.22), iron_base_y + iron_w + 2],
                   fill=SILHOUETTE)
    # Tip (tapered triangle at end)
    draw.polygon([(iron_base_x + iron_len - int(iron_len*0.22), iron_base_y),
                  (iron_base_x + iron_len - int(iron_len*0.22), iron_base_y + iron_w + 2),
                  (iron_base_x + iron_len, iron_base_y + (iron_w + 2)//2)],
                 fill=SILHOUETTE)

    # Legs
    lw = int(hu * 0.22)
    leg_h = int(hu * 0.45)
    draw.rectangle([cx - hip_w + 6,  body_bot_y, cx - lw, body_bot_y + leg_h], fill=SILHOUETTE)
    draw.rectangle([cx + lw, body_bot_y, cx + hip_w - 6, body_bot_y + leg_h], fill=SILHOUETTE)
    # Simple block feet (sturdy, grounded)
    fw = int(hu * 0.30)
    fh = int(hu * 0.18)
    draw.rectangle([cx - hip_w + 4,  base_y - fh, cx - lw + int(fw*0.4), base_y], fill=SILHOUETTE)
    draw.rectangle([cx + lw - int(fw*0.4), base_y - fh, cx + hip_w - 4, base_y], fill=SILHOUETTE)


def draw_miri_v2(draw, cx, base_y):
    """Miri — VARIANT B (neutral stance).
    Design hook: LARGE ROUNDED CURLS — two big cloud puffs flanking head, lower and wider than Luma's.
    Wide tech-themed APRON over clothing: rectangle bib + strings, with a small circuit-board
    patch pocket (dotted grid) on the bib for the 'circuits' read.
    Bag stays on right hip. No soldering iron — apron replaces tool-holder function.
    Communicates: homey craft/cook warmth (apron) + tech obsession (circuit bib detail).
    """
    hu = HEAD_UNIT
    h = int(3.2 * hu)
    hy = base_y - h
    r = int(hu * 0.46)

    # HAIR: two big rounded curls flanking head (low puff style — NOT Luma's cloud-top).
    # Luma's hair is UP; Miri's is OUT — different silhouette axis.
    curl_r = int(hu * 0.42)
    curl_y = hy + int(hu * 0.22)   # at head height, not above
    # Left curl — large puff protruding far left
    draw.ellipse([cx - r - int(curl_r * 1.6), curl_y - curl_r,
                  cx - r + int(curl_r * 0.5), curl_y + curl_r], fill=SILHOUETTE)
    # Right curl — large puff protruding far right (slightly different size = natural)
    draw.ellipse([cx + r - int(curl_r * 0.5), curl_y - int(curl_r * 0.9),
                  cx + r + int(curl_r * 1.5), curl_y + int(curl_r * 0.9)], fill=SILHOUETTE)
    # Small connecting puff on top to close the silhouette
    draw.ellipse([cx - int(hu * 0.35), hy - int(hu * 0.12),
                  cx + int(hu * 0.35), hy + int(hu * 0.38)], fill=SILHOUETTE)

    # Head
    draw.ellipse([cx - r, hy, cx + r, hy + int(hu)], fill=SILHOUETTE)

    # Body — moderate rectangle (apron gives the width, not body itself)
    bw = int(hu * 0.55)
    body_h = int(hu * 1.82)
    body_top_y = hy + int(hu * 0.88)
    body_bot_y = body_top_y + body_h
    draw.rectangle([cx - bw, body_top_y, cx + bw, body_bot_y], fill=SILHOUETTE)

    # APRON BIB — wide rectangle over upper body, slightly wider than body.
    # This adds clear horizontal mass and breaks the plain-rectangle body read.
    apron_bw = int(hu * 0.46)
    apron_bib_top = body_top_y + int(body_h * 0.06)
    apron_bib_bot = body_top_y + int(body_h * 0.62)
    draw.rectangle([cx - apron_bw, apron_bib_top, cx + apron_bw, apron_bib_bot],
                   fill=SILHOUETTE)
    # Circuit-board pocket on bib — small square with NEG_SPACE grid inside
    # This creates a tiny readable negative-space detail (like Cosmo's glasses)
    pc_x = cx - int(hu * 0.18)
    pc_y = apron_bib_top + int(body_h * 0.14)
    pc_s = int(hu * 0.30)
    draw.rectangle([pc_x, pc_y, pc_x + pc_s, pc_y + pc_s], fill=NEG_SPACE)
    # 3x3 dot grid inside pocket (circuit trace negative-space)
    dot = max(2, int(pc_s * 0.12))
    for row in range(3):
        for col in range(3):
            dx = pc_x + int(pc_s * (0.2 + col * 0.3))
            dy = pc_y + int(pc_s * (0.2 + row * 0.3))
            draw.rectangle([dx, dy, dx + dot, dy + dot], fill=SILHOUETTE)

    # Apron strings — two small rectangles going up from bib top to shoulders
    str_w = int(hu * 0.08)
    draw.rectangle([cx - apron_bw - int(hu*0.05), apron_bib_top - int(hu*0.12),
                    cx - apron_bw - int(hu*0.05) + str_w, apron_bib_top], fill=SILHOUETTE)
    draw.rectangle([cx + apron_bw + int(hu*0.05) - str_w, apron_bib_top - int(hu*0.12),
                    cx + apron_bw + int(hu*0.05), apron_bib_top], fill=SILHOUETTE)

    # SHOULDER BAG — right hip
    bag_x = cx + bw
    bag_y = body_top_y + int(body_h * 0.52)
    bag_w = int(hu * 0.34)
    bag_h = int(hu * 0.48)
    draw.rectangle([bag_x, bag_y, bag_x + bag_w, bag_y + bag_h], fill=SILHOUETTE)
    draw.rectangle([bag_x + int(bag_w*0.15), bag_y - int(hu*0.10),
                    bag_x + int(bag_w*0.65), bag_y], fill=SILHOUETTE)

    # Legs
    lw = int(hu * 0.22)
    leg_h = int(hu * 0.45)
    draw.rectangle([cx - bw + 6, body_bot_y, cx - lw, body_bot_y + leg_h], fill=SILHOUETTE)
    draw.rectangle([cx + lw, body_bot_y, cx + bw - 6, body_bot_y + leg_h], fill=SILHOUETTE)
    fw = int(hu * 0.30)
    fh = int(hu * 0.18)
    draw.rectangle([cx - bw + 4, base_y - fh, cx - lw + int(fw*0.4), base_y], fill=SILHOUETTE)
    draw.rectangle([cx + lw - int(fw*0.4), base_y - fh, cx + bw - 4, base_y], fill=SILHOUETTE)


# ─────────────────────────────────────────────────────────────────
# ACTION POSES
# ─────────────────────────────────────────────────────────────────

def draw_luma_action(draw, cx, base_y):
    """Luma — mid-lean, one foot off ground, arms asymmetric, momentum pose."""
    h = LUMA_H
    hu = HEAD_UNIT
    r = int(hu * 0.46)

    # Head — shifted forward (lean) and slightly tilted
    head_off = int(hu * 0.20)   # lean forward
    hy = base_y - h + int(hu * 0.15)   # body pitched up slightly
    hx = cx + head_off
    draw.ellipse([hx - r, hy, hx + r, hy + int(hu)], fill=SILHOUETTE)
    draw.ellipse([hx - int(r*1.5), hy - int(r*0.6), hx + int(r*1.5), hy + int(r*0.8)], fill=SILHOUETTE)

    # Body — tilted forward trapezoid
    shoulder_w = int(hu * 0.38)
    hem_w      = int(hu * 0.70)
    body_top_y = hy + int(hu * 0.85)
    body_h     = int(hu * 2.0)
    body_bot_y = body_top_y + body_h

    # Lean: top of body shifted forward, bottom stays planted
    lean = int(hu * 0.25)
    body_pts = [
        (cx - shoulder_w + lean, body_top_y),
        (cx + shoulder_w + lean, body_top_y),
        (cx + hem_w,             body_bot_y),
        (cx - hem_w,             body_bot_y),
    ]
    draw.polygon(body_pts, fill=SILHOUETTE)

    # Pocket bump protruding outside hem
    mid_body_frac = 0.55
    hem_edge_at_mid = cx + int(shoulder_w + lean + (hem_w - shoulder_w - lean) * mid_body_frac)
    pocket_y = body_top_y + int(body_h * 0.50)
    pocket_w = int(hu * 0.30)
    pocket_h = int(hu * 0.42)
    draw.rectangle([hem_edge_at_mid, pocket_y,
                    hem_edge_at_mid + pocket_w, pocket_y + pocket_h], fill=SILHOUETTE)

    lw = int(hu * 0.20)
    leg_h = int(hu * 0.55)
    fw = int(hu * 0.52)
    fh = int(hu * 0.28)

    # Planted left leg — extended back
    draw.rectangle([cx - lw*2 - int(lean*0.3), body_bot_y,
                    cx - 4 - int(lean*0.3),   body_bot_y + leg_h], fill=SILHOUETTE)
    draw.ellipse([cx - lw*2 - int(lean*0.3) - fw + int(fw*0.3), base_y - fh,
                  cx - lw*2 - int(lean*0.3) + int(fw*0.5),       base_y], fill=SILHOUETTE)

    # Raised right leg — lifted forward (off ground)
    kick_up = int(hu * 0.45)
    draw.rectangle([cx + 4 + lean, body_bot_y,
                    cx + lw*2 + lean, body_bot_y + leg_h - kick_up], fill=SILHOUETTE)
    # Foot pointed forward/upward (diagonal)
    kick_pts = [
        (cx + lw*2 + lean,                 body_bot_y + leg_h - kick_up),
        (cx + lw*2 + lean + int(fw*0.7),   body_bot_y + leg_h - kick_up - int(fh*0.5)),
        (cx + lw*2 + lean + int(fw*0.7),   body_bot_y + leg_h - kick_up + fh - int(fh*0.5)),
    ]
    draw.polygon(kick_pts, fill=SILHOUETTE)

    # Right arm — raised and reaching forward
    arm_top_y = body_top_y + int(body_h*0.15)
    arm_h = int(hu * 0.55)
    draw.rectangle([cx + shoulder_w + lean, arm_top_y,
                    cx + shoulder_w + lean + int(hu*0.22), arm_top_y + arm_h], fill=SILHOUETTE)
    # Hand reaching out
    draw.ellipse([cx + shoulder_w + lean + int(hu*0.14), arm_top_y + arm_h - int(hu*0.12),
                  cx + shoulder_w + lean + int(hu*0.36), arm_top_y + arm_h + int(hu*0.12)],
                 fill=SILHOUETTE)

    # Left arm — swinging back for momentum
    draw.rectangle([cx - shoulder_w + lean - int(hu*0.22), arm_top_y + int(arm_h*0.3),
                    cx - shoulder_w + lean, arm_top_y + int(arm_h*0.3) + arm_h], fill=SILHOUETTE)


def draw_cosmo_action(draw, cx, base_y):
    """Cosmo — bent over notebook, one arm out, active-thinking pose."""
    hu = HEAD_UNIT
    h = int(4.0 * hu)

    # Body pitched forward at the waist
    lean = int(hu * 0.45)
    hy = base_y - h + int(hu * 0.30)   # slightly higher (bent)
    hx = cx + lean   # head shifts forward

    hw = int(hu * 0.4)
    hh = int(hu * 0.95)
    draw.rounded_rectangle([hx - hw, hy, hx + hw, hy + hh], radius=6, fill=SILHOUETTE)

    # Glasses on bent head — negative space cutouts
    gr = int(hu * 0.18)
    gy = hy + int(hh * 0.45)
    lcx_g = hx - int(hu * 0.28)
    rcx_g = hx + int(hu * 0.28)
    rim_extra = 3
    draw.ellipse([lcx_g - gr - rim_extra, gy - gr - rim_extra,
                  lcx_g + gr + rim_extra, gy + gr + rim_extra], fill=SILHOUETTE)
    draw.ellipse([rcx_g - gr - rim_extra, gy - gr - rim_extra,
                  rcx_g + gr + rim_extra, gy + gr + rim_extra], fill=SILHOUETTE)
    draw.ellipse([lcx_g - gr, gy - gr, lcx_g + gr, gy + gr], fill=NEG_SPACE)
    draw.ellipse([rcx_g - gr, gy - gr, rcx_g + gr, gy + gr], fill=NEG_SPACE)

    # Torso — pitched forward
    bw = int(hu * 0.38)
    body_h = int(hu * 2.0)
    # Torso as polygon (top at head, bottom shifted back)
    body_top_y = hy + hh
    body_bot_y = body_top_y + body_h
    torso_pts = [
        (hx - bw, body_top_y),
        (hx + bw, body_top_y),
        (cx + bw, body_bot_y),
        (cx - bw, body_bot_y),
    ]
    draw.polygon(torso_pts, fill=SILHOUETTE)

    # Notebook held in front (at mid-torso height)
    nw = int(hu * 0.55)
    nh = int(hu * 0.65)
    nb_x = hx - bw - nw + 8
    nb_y = body_top_y + int(body_h * 0.25)
    draw.rectangle([nb_x, nb_y, nb_x + nw, nb_y + nh], fill=SILHOUETTE)

    # Arm reaching out (right arm, extended to catch/point)
    arm_len = int(hu * 0.70)
    arm_top_y = body_top_y + int(body_h * 0.20)
    draw.rectangle([hx + bw, arm_top_y,
                    hx + bw + arm_len, arm_top_y + int(hu * 0.20)], fill=SILHOUETTE)
    draw.ellipse([hx + bw + arm_len - int(hu*0.1), arm_top_y - int(hu*0.12),
                  hx + bw + arm_len + int(hu*0.18), arm_top_y + int(hu*0.20) + int(hu*0.12)],
                 fill=SILHOUETTE)

    # Legs (standing upright below bent torso)
    lw = int(hu * 0.18)
    leg_h = int(hu * 0.6)
    draw.rectangle([cx - bw + 4, body_bot_y, cx - lw, body_bot_y + leg_h], fill=SILHOUETTE)
    draw.rectangle([cx + lw, body_bot_y, cx + bw - 4, body_bot_y + leg_h], fill=SILHOUETTE)

    # Feet
    fw = int(hu * 0.28)
    fh = int(hu * 0.18)
    draw.ellipse([cx - bw + 4 - int(fw*0.4), base_y - fh,
                  cx - lw + int(fw*0.6),      base_y], fill=SILHOUETTE)
    draw.ellipse([cx + lw - int(fw*0.3),      base_y - fh,
                  cx + bw - 4 + int(fw*0.4),  base_y], fill=SILHOUETTE)


def draw_byte_action(draw, cx, base_y):
    """Byte — MID-FLIGHT LEAP pose (Cycle 9 redesign per Dmitri feedback).
    Body at a diagonal (tilted ~25° from vertical), both arms extended at
    DIFFERENT angles (right arm forward-up, left arm back-down), one leg
    kicked back hard. The silhouette implies velocity, not indication.
    Rule: asymmetric arm angles + diagonal body + kicked leg = motion read.
    """
    hu = HEAD_UNIT
    s = int(LUMA_H * 0.20)
    c = int(s * 0.15)
    lw = int(s * 0.22)

    # ── Body: tilted diagonally (top-right, bottom-left) ──────────────────
    # Diagonal tilt: top of body shifts right (+tilt_x, -tilt_y),
    # bottom shifts left — creates a clear mid-air lean.
    tilt_x = int(s * 0.30)   # horizontal lean of top vs bottom
    tilt_y = int(s * 0.18)   # vertical compression (body foreshortened at angle)

    # Ground line raised: Byte is in the air (leap clears base_y by jump_h)
    jump_h = int(s * 0.45)
    hy = base_y - s - jump_h   # top of body (body fully off ground)

    # Body polygon: top-right / bottom-left diagonal
    pts = [
        (cx - s//2 + c + tilt_x,  hy),
        (cx + s//2 - c + tilt_x,  hy),
        (cx + s//2 + tilt_x,      hy + c),
        (cx + s//2,                hy + s - tilt_y - c),
        (cx + s//2 - c,            hy + s - tilt_y),
        (cx - s//2 + c,            hy + s - tilt_y),
        (cx - s//2,                hy + s - tilt_y - c),
        (cx - s//2 + tilt_x,      hy + c),
    ]
    draw.polygon(pts, fill=SILHOUETTE)

    # ── Arms: DIFFERENT ANGLES — velocity asymmetry ────────────────────────
    arm_root_y = hy + int((s - tilt_y) * 0.35)
    arm_h = int(s * 0.22)   # arm thickness

    # RIGHT ARM: thrusting FORWARD-UP (leading into the leap)
    # Extends upper-right at steep angle
    r_arm_len = int(s * 0.80)
    r_start_x = cx + s//2 + tilt_x
    r_start_y = arm_root_y
    r_ang_x = int(r_arm_len * 0.72)   # strong rightward thrust
    r_ang_y = -int(r_arm_len * 0.52)  # angled up
    draw.polygon([
        (r_start_x,              r_start_y - arm_h//2),
        (r_start_x + r_ang_x,    r_start_y + r_ang_y - arm_h//2),
        (r_start_x + r_ang_x,    r_start_y + r_ang_y + arm_h//2),
        (r_start_x,              r_start_y + arm_h//2),
    ], fill=SILHOUETTE)
    # Hand at right arm tip (small blob)
    draw.ellipse([r_start_x + r_ang_x - int(arm_h*0.6),
                  r_start_y + r_ang_y - int(arm_h*0.6),
                  r_start_x + r_ang_x + int(arm_h*0.4),
                  r_start_y + r_ang_y + int(arm_h*0.4)], fill=SILHOUETTE)

    # LEFT ARM: swinging BACK-DOWN (trailing the leap — momentum counterweight)
    # Extends lower-left at a shallow angle
    l_arm_len = int(s * 0.68)
    l_start_x = cx - s//2 + tilt_x
    l_start_y = arm_root_y + int(arm_h * 0.5)
    l_ang_x = -int(l_arm_len * 0.65)  # backward
    l_ang_y = int(l_arm_len * 0.38)   # angled DOWN (trailing)
    draw.polygon([
        (l_start_x,              l_start_y - arm_h//2),
        (l_start_x + l_ang_x,    l_start_y + l_ang_y - arm_h//2),
        (l_start_x + l_ang_x,    l_start_y + l_ang_y + arm_h//2),
        (l_start_x,              l_start_y + arm_h//2),
    ], fill=SILHOUETTE)

    # ── Legs: one KICKED BACK hard, one tucked forward ─────────────────────
    leg_w = int(s * 0.20)
    bot_y = hy + s - tilt_y   # bottom of body

    # Lead leg (right): tucked forward-up under body (crouch position in leap)
    tuck_x = int(s * 0.20)
    tuck_y = int(s * 0.28)
    draw.rectangle([cx + s//4 - leg_w//2,      bot_y,
                    cx + s//4 + tuck_x + leg_w, bot_y + tuck_y], fill=SILHOUETTE)

    # Trail leg (left): KICKED BACK and down hard — the power stroke
    # Long diagonal extending lower-left
    kick_len_x = int(s * 0.52)
    kick_len_y = int(s * 0.62)
    kick_pts = [
        (cx - s//4 - leg_w//2, bot_y),
        (cx - s//4 + leg_w//2, bot_y),
        (cx - s//4 + leg_w//2 - kick_len_x, bot_y + kick_len_y),
        (cx - s//4 - leg_w//2 - kick_len_x, bot_y + kick_len_y - int(leg_w*0.5)),
    ]
    draw.polygon(kick_pts, fill=SILHOUETTE)

    # ── Hover particles: scattered — not static, implies motion ───────────
    # Positioned below the leap trajectory (lower than neutral hover)
    particle_y = base_y - int(s * 0.08)
    psz = 10
    offsets = [(-int(s*0.45), 0), (-int(s*0.22), 8), (0, 3),
               (int(s*0.18), 0), (int(s*0.38), 6)]
    for ox, oy in offsets:
        draw.rectangle([cx + ox, particle_y + oy,
                        cx + ox + psz, particle_y + oy + psz], fill=SILHOUETTE)


def draw_miri_action(draw, cx, base_y):
    """Miri (Variant A) — action: leaning forward with soldering iron raised, examining something.
    Bun+chopsticks silhouette is visible even in leaning pose.
    """
    hu = HEAD_UNIT
    h = int(3.2 * hu)
    hy = base_y - h + int(hu * 0.12)  # slightly raised (lean)
    r  = int(hu * 0.46)

    # BUN + CHOPSTICKS (tilted forward slightly with head lean)
    lean = int(hu * 0.18)
    bun_cx = cx + int(hu * 0.06) + lean
    bun_cy = hy - int(hu * 0.30)
    bun_rx = int(hu * 0.38)
    bun_ry = int(hu * 0.44)
    draw.ellipse([bun_cx - bun_rx, bun_cy - bun_ry,
                  bun_cx + bun_rx, bun_cy + bun_ry], fill=SILHOUETTE)
    # Chopstick pair — angled forward with lean
    draw.polygon([(bun_cx - int(hu*0.20), bun_cy - bun_ry - int(hu*0.54)),
                  (bun_cx - int(hu*0.12), bun_cy - bun_ry - int(hu*0.54)),
                  (bun_cx - int(hu*0.04), bun_cy + bun_ry - int(hu*0.12)),
                  (bun_cx - int(hu*0.12), bun_cy + bun_ry - int(hu*0.12))],
                 fill=SILHOUETTE)
    draw.polygon([(bun_cx + int(hu*0.12), bun_cy - bun_ry - int(hu*0.48)),
                  (bun_cx + int(hu*0.20), bun_cy - bun_ry - int(hu*0.48)),
                  (bun_cx + int(hu*0.12), bun_cy + bun_ry - int(hu*0.12)),
                  (bun_cx + int(hu*0.05), bun_cy + bun_ry - int(hu*0.12))],
                 fill=SILHOUETTE)

    # Head — shifted forward (examining something)
    hx = cx + lean
    draw.ellipse([hx - r, hy, hx + r, hy + int(hu)], fill=SILHOUETTE)

    # Cardigan body — top shifted forward
    shoulder_w = int(hu * 0.78)
    hip_w      = int(hu * 0.62)
    body_top_y = hy + int(hu * 0.88)
    body_h     = int(hu * 1.82)
    body_bot_y = body_top_y + body_h
    body_pts = [
        (cx - shoulder_w + lean, body_top_y),
        (cx + shoulder_w + lean, body_top_y),
        (cx + hip_w,             body_bot_y),
        (cx - hip_w,             body_bot_y),
    ]
    draw.polygon(body_pts, fill=SILHOUETTE)

    # Bag on right hip
    bag_x = cx + hip_w
    bag_y = body_top_y + int(body_h * 0.52)
    bag_w = int(hu * 0.34)
    bag_h = int(hu * 0.48)
    draw.rectangle([bag_x, bag_y, bag_x + bag_w, bag_y + bag_h], fill=SILHOUETTE)

    # LEFT ARM — raised high, holding soldering iron aimed at something off-frame
    arm_w = int(hu * 0.22)
    arm_top_y = body_top_y + int(body_h * 0.08)
    # Upper arm raised
    draw.rectangle([cx - shoulder_w + lean - arm_w, arm_top_y - int(hu*0.30),
                    cx - shoulder_w + lean,          arm_top_y + int(hu*0.22)], fill=SILHOUETTE)
    # Forearm extends outward/upward at angle
    draw.rectangle([cx - shoulder_w + lean - arm_w - int(hu*0.42), arm_top_y - int(hu*0.52),
                    cx - shoulder_w + lean - arm_w,                 arm_top_y - int(hu*0.16)],
                   fill=SILHOUETTE)
    # Soldering iron in hand — extends further
    iron_tip_x = cx - shoulder_w + lean - arm_w - int(hu*0.42) - int(hu*0.48)
    iron_tip_y = arm_top_y - int(hu*0.52) - int(hu*0.06)
    iron_end_x = cx - shoulder_w + lean - arm_w - int(hu*0.42)
    iron_end_y = arm_top_y - int(hu*0.52) + int(hu*0.08)
    iron_w = int(hu * 0.08)
    draw.polygon([(iron_end_x, iron_end_y - iron_w//2),
                  (iron_end_x, iron_end_y + iron_w//2),
                  (iron_tip_x + int(hu*0.18), iron_tip_y + iron_w),
                  (iron_tip_x,                iron_tip_y)],
                 fill=SILHOUETTE)
    # Tip triangle
    draw.polygon([(iron_tip_x + int(hu*0.18), iron_tip_y),
                  (iron_tip_x + int(hu*0.18), iron_tip_y + iron_w),
                  (iron_tip_x,                iron_tip_y + iron_w//2)],
                 fill=SILHOUETTE)

    # RIGHT ARM — slightly out from body, holding steady
    draw.rectangle([cx + shoulder_w + lean, body_top_y + int(body_h * 0.12),
                    cx + shoulder_w + lean + arm_w, body_top_y + int(body_h * 0.58)],
                   fill=SILHOUETTE)
    # Hand blob
    draw.ellipse([cx + shoulder_w + lean + int(arm_w*0.1),
                  body_top_y + int(body_h * 0.56),
                  cx + shoulder_w + lean + arm_w + int(arm_w*0.5),
                  body_top_y + int(body_h * 0.68)], fill=SILHOUETTE)

    # Legs — both planted (grounded even while leaning)
    lw = int(hu * 0.22)
    leg_h = int(hu * 0.45)
    draw.rectangle([cx - hip_w + 4, body_bot_y, cx - lw, body_bot_y + leg_h], fill=SILHOUETTE)
    draw.rectangle([cx + lw, body_bot_y, cx + hip_w - 4, body_bot_y + leg_h], fill=SILHOUETTE)
    fw = int(hu * 0.30)
    fh = int(hu * 0.18)
    draw.rectangle([cx - hip_w + 2, base_y - fh, cx - lw + int(fw*0.4), base_y], fill=SILHOUETTE)
    draw.rectangle([cx + lw - int(fw*0.4), base_y - fh, cx + hip_w - 2, base_y], fill=SILHOUETTE)


def draw_miri_v2_action(draw, cx, base_y):
    """Miri (Variant B) — action: arms wide open (welcoming gesture), apron prominent.
    Big rounded curls read strongly even mid-gesture.
    """
    hu = HEAD_UNIT
    h = int(3.2 * hu)
    hy = base_y - h
    r  = int(hu * 0.46)

    # Big rounded curls — same as neutral but rendered on action pose
    curl_r = int(hu * 0.42)
    curl_y = hy + int(hu * 0.22)
    draw.ellipse([cx - r - int(curl_r * 1.6), curl_y - curl_r,
                  cx - r + int(curl_r * 0.5), curl_y + curl_r], fill=SILHOUETTE)
    draw.ellipse([cx + r - int(curl_r * 0.5), curl_y - int(curl_r * 0.9),
                  cx + r + int(curl_r * 1.5), curl_y + int(curl_r * 0.9)], fill=SILHOUETTE)
    draw.ellipse([cx - int(hu * 0.35), hy - int(hu * 0.12),
                  cx + int(hu * 0.35), hy + int(hu * 0.38)], fill=SILHOUETTE)

    # Head
    draw.ellipse([cx - r, hy, cx + r, hy + int(hu)], fill=SILHOUETTE)

    # Body + apron bib
    bw = int(hu * 0.55)
    body_h = int(hu * 1.82)
    body_top_y = hy + int(hu * 0.88)
    body_bot_y = body_top_y + body_h
    draw.rectangle([cx - bw, body_top_y, cx + bw, body_bot_y], fill=SILHOUETTE)
    apron_bw = int(hu * 0.46)
    apron_bib_top = body_top_y + int(body_h * 0.06)
    apron_bib_bot = body_top_y + int(body_h * 0.62)
    draw.rectangle([cx - apron_bw, apron_bib_top, cx + apron_bw, apron_bib_bot], fill=SILHOUETTE)
    # Circuit pocket (NEG_SPACE detail)
    pc_x = cx - int(hu * 0.18)
    pc_y = apron_bib_top + int(body_h * 0.14)
    pc_s = int(hu * 0.30)
    draw.rectangle([pc_x, pc_y, pc_x + pc_s, pc_y + pc_s], fill=NEG_SPACE)
    dot = max(2, int(pc_s * 0.12))
    for row in range(3):
        for col in range(3):
            dx = pc_x + int(pc_s * (0.2 + col * 0.3))
            dy = pc_y + int(pc_s * (0.2 + row * 0.3))
            draw.rectangle([dx, dy, dx + dot, dy + dot], fill=SILHOUETTE)

    # ARMS — wide open, both extended outward (welcoming/celebratory)
    arm_w = int(hu * 0.22)
    arm_h = int(hu * 0.50)
    arm_y = body_top_y + int(body_h * 0.14)
    # Left arm — angled up and out
    draw.polygon([(cx - bw, arm_y),
                  (cx - bw, arm_y + int(arm_h * 0.35)),
                  (cx - bw - arm_w * 3, arm_y - int(arm_h * 0.22)),
                  (cx - bw - arm_w * 3, arm_y - int(arm_h * 0.22) - arm_w)],
                 fill=SILHOUETTE)
    draw.ellipse([cx - bw - arm_w * 3 - int(arm_w * 0.8), arm_y - int(arm_h * 0.36),
                  cx - bw - arm_w * 3 + int(arm_w * 0.4), arm_y + int(arm_h * 0.02)],
                 fill=SILHOUETTE)
    # Right arm — angled up and out (symmetric open gesture)
    draw.polygon([(cx + bw, arm_y),
                  (cx + bw, arm_y + int(arm_h * 0.35)),
                  (cx + bw + arm_w * 3, arm_y - int(arm_h * 0.22)),
                  (cx + bw + arm_w * 3, arm_y - int(arm_h * 0.22) - arm_w)],
                 fill=SILHOUETTE)
    draw.ellipse([cx + bw + arm_w * 3 - int(arm_w * 0.4), arm_y - int(arm_h * 0.36),
                  cx + bw + arm_w * 3 + int(arm_w * 0.8), arm_y + int(arm_h * 0.02)],
                 fill=SILHOUETTE)

    # Bag on right hip
    bag_x = cx + bw
    bag_y = body_top_y + int(body_h * 0.62)
    bag_w = int(hu * 0.34)
    bag_h = int(hu * 0.38)
    draw.rectangle([bag_x, bag_y, bag_x + bag_w, bag_y + bag_h], fill=SILHOUETTE)

    # Legs — slight wide stance
    lw = int(hu * 0.22)
    leg_h = int(hu * 0.45)
    draw.rectangle([cx - bw + 4, body_bot_y, cx - lw - int(hu*0.04), body_bot_y + leg_h], fill=SILHOUETTE)
    draw.rectangle([cx + lw + int(hu*0.04), body_bot_y, cx + bw - 4, body_bot_y + leg_h], fill=SILHOUETTE)
    fw = int(hu * 0.30)
    fh = int(hu * 0.18)
    draw.rectangle([cx - bw + 2, base_y - fh, cx - lw + int(fw*0.4), base_y], fill=SILHOUETTE)
    draw.rectangle([cx + lw - int(fw*0.4), base_y - fh, cx + bw - 2, base_y], fill=SILHOUETTE)


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────

def generate(output_path):
    # Two rows: neutral (top) + action (bottom)
    # Characters: Luma, Cosmo, Byte, MIRI (canonical = MIRI-A, locked Cycle 9)
    # MIRI-B variant retired after Cycle 8 critic selection. MIRI-A is the only Miri.
    N_CHARS = 4
    COL_W   = 186
    W       = COL_W * N_CHARS + 80   # 80px total side margin (40 each side)

    # NEUTRAL_BASE is the ground line for neutral row.
    # Tallest character is Cosmo at 4.0 * HEAD_UNIT (~320px).
    # Miri chopsticks (MIRI-A) add ~HU*0.58 above bun — set headroom above clip threshold.
    NEUTRAL_BASE = 420
    # ACTION row: characters are roughly same height, allow same headroom.
    # Cycle 9: Byte action pose is a mid-flight leap — body raised jump_h above base.
    # jump_h = s*0.45 ≈ 25px. The arms go up (r_ang_y=-52px relative to arm root).
    # Net top of Byte action = base - s - jump_h - arm_up ≈ base - 56 - 25 - arm_up.
    # Keep 260px gap to accommodate full leap silhouette without clipping.
    ACTION_BASE  = NEUTRAL_BASE + 260   # 260px row gap for action variant arms + leap

    H2 = ACTION_BASE + 70   # 70px below action ground line for labels + title
    img2 = Image.new('RGB', (W, H2), BG)
    draw2 = ImageDraw.Draw(img2)

    try:
        font       = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
        font_col   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        font_note  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except:
        font = font_title = font_col = font_note = ImageFont.load_default()

    # MIRI-A is the canonical Miri (Cycle 9 lock: bun+chopsticks+cardigan+soldering-iron).
    # MIRI-B (curls+apron) is retired — no longer shown on silhouette sheet.
    col_labels    = ["LUMA", "COSMO", "BYTE", "MIRI"]
    neutral_drawers = [draw_luma, draw_cosmo, draw_byte, draw_miri]
    action_drawers  = [draw_luma_action, draw_cosmo_action, draw_byte_action, draw_miri_action]

    # Title at bottom so it doesn't interfere with characters
    draw2.text((16, H2 - 40),
               "LUMA & THE GLITCHKIN — Silhouette Sheet — Neutral + Action — Cycle 9",
               fill=(30, 20, 15), font=font_title)
    draw2.text((16, H2 - 24),
               "MIRI: bun+chopsticks+cardigan+soldering-iron (MIRI-A — CANONICAL, locked Cycle 9)  |  "
               "BYTE: mid-flight leap pose",
               fill=(80, 70, 60), font=font_note)

    # Row divider between neutral and action sections
    divider_y = NEUTRAL_BASE + 30
    draw2.line([(20, divider_y), (W - 20, divider_y)], fill=OUTLINE_COL, width=1)

    # Row labels
    draw2.text((4, 8), "NEUTRAL", fill=(120, 110, 100), font=font_col)
    draw2.text((4, NEUTRAL_BASE + 38), "ACTION", fill=(120, 110, 100), font=font_col)

    for i, (name, neutral_fn, action_fn) in enumerate(
            zip(col_labels, neutral_drawers, action_drawers)):
        col_cx = 80 + i * COL_W   # 80px left margin keeps Luma's wide curls on-canvas

        # Neutral
        neutral_fn(draw2, col_cx, NEUTRAL_BASE)
        draw2.line([(col_cx - 50, NEUTRAL_BASE), (col_cx + 50, NEUTRAL_BASE)],
                   fill=OUTLINE_COL, width=1)
        draw2.text((col_cx - 24, NEUTRAL_BASE + 8), name, fill=TEXT_COL, font=font)

        # Action
        action_fn(draw2, col_cx, ACTION_BASE)
        draw2.line([(col_cx - 50, ACTION_BASE), (col_cx + 50, ACTION_BASE)],
                   fill=OUTLINE_COL, width=1)
        draw2.text((col_cx - 28, ACTION_BASE + 8), f"{name}*", fill=TEXT_COL, font=font)

    img2.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == '__main__':
    import os
    os.makedirs("/home/wipkat/team/output/characters/main/silhouettes", exist_ok=True)
    generate("/home/wipkat/team/output/characters/main/silhouettes/character_silhouettes.png")
