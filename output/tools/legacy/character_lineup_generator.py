# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
Character Lineup Generator — Luma & the Glitchkin
Cycle 10: Generates a SINGLE IMAGE showing all 4 main characters standing together
at their CORRECT relative heights on a shared baseline.

Height relationships (production bible):
  - Luma: 3.5 heads tall (young protagonist, compact) — reference character
  - Byte: roughly Luma's chest height (floating companion)
  - Cosmo: taller than Luma (adult proportions, 4.0 heads)
  - Miri: shorter than Cosmo, warm and sturdy (3.2 heads)

Colors from master_palette.md (canonical hex values):
  - Luma: orange hoodie #E8722A, dark indigo pants #2A2850, cream shoes #F5E8D0
  - Byte: teal body #00D4E8 with magenta scar #FF2D6B
  - Cosmo: lavender cardigan/jacket #A89BBF, striped shirt (cerulean #5B8DB8 + sage #7A9E7E), chinos #8C8880
  - Miri: terracotta rust cardigan #B85C38, linen pants #C8AE8A, sage slippers #5A7A5A, silver hair #D8D0C8

Output: /home/wipkat/team/output/characters/main/character_lineup.png
"""
from PIL import Image, ImageDraw, ImageFont
import math

# ── Canvas ────────────────────────────────────────────────────────────────────
BG          = (250, 248, 244)
PANEL_BG    = (245, 241, 235)
LINE_COL    = (59, 40, 32)      # #3B2820 Deep Cocoa — show-wide line color
LABEL_COL   = (50, 40, 35)
TICK_COL    = (160, 148, 138)
BASELINE_COL = (180, 165, 150)

# ── Height system ─────────────────────────────────────────────────────────────
# Luma is the reference. At 3.5 heads, she sets the scale.
# We render Luma at 280px (same as silhouette sheet reference).
# All other characters scale proportionally.
LUMA_RENDER_H = 280          # Luma's rendered height in pixels
LUMA_HEADS    = 3.5
HEAD_UNIT     = LUMA_RENDER_H / LUMA_HEADS   # one head unit in pixels (~80px)

COSMO_HEADS   = 4.0
COSMO_H       = int(COSMO_HEADS * HEAD_UNIT)   # ~320px

MIRI_HEADS    = 3.2
MIRI_H        = int(MIRI_HEADS * HEAD_UNIT)    # ~256px

# Byte height: roughly Luma's chest height.
# Chest is about 2 heads down from top, so ~2/3.5 of Luma's height = ~160px.
BYTE_H        = int(LUMA_RENDER_H * 0.58)      # ~162px

# ── Layout ────────────────────────────────────────────────────────────────────
CHAR_SPACING  = 260     # horizontal spacing between character centers
LEFT_MARGIN   = 120
N_CHARS       = 4
IMG_W         = LEFT_MARGIN * 2 + CHAR_SPACING * (N_CHARS - 1) + 160
TITLE_H       = 50
HEADROOM      = int(COSMO_H * 1.15)   # space above baseline for tallest char + labels
LABEL_AREA    = 80
IMG_H         = TITLE_H + HEADROOM + LABEL_AREA

# Baseline Y
BASELINE_Y    = TITLE_H + HEADROOM

# Character order: Luma, Byte (floating near Luma), Cosmo, Miri
# Byte is placed next to Luma to show their height relationship clearly.
CHAR_ORDER    = ["luma", "byte", "cosmo", "miri"]
CHAR_X        = {
    "luma":  LEFT_MARGIN + 60,
    "byte":  LEFT_MARGIN + 60 + CHAR_SPACING - 40,
    "cosmo": LEFT_MARGIN + 60 + CHAR_SPACING * 2 - 20,
    "miri":  LEFT_MARGIN + 60 + CHAR_SPACING * 3,
}
CHAR_HEIGHTS  = {
    "luma":  LUMA_RENDER_H,
    "byte":  BYTE_H,
    "cosmo": COSMO_H,
    "miri":  MIRI_H,
}
CHAR_LABELS   = {
    "luma":  f"LUMA\n3.5 heads / {LUMA_RENDER_H}px",
    "byte":  f"BYTE\n~Luma chest height / {BYTE_H}px",
    "cosmo": f"COSMO\n4.0 heads / {COSMO_H}px",
    "miri":  f"MIRI\n3.2 heads / {MIRI_H}px",
}

# ── Colors ────────────────────────────────────────────────────────────────────
# Luma
LUMA_SKIN      = (196, 168, 130)   # #C4A882 warm tan (neutral light)
LUMA_HAIR      = (26, 15, 10)      # #1A0F0A near-black espresso
LUMA_HOODIE    = (232, 114, 42)    # #E8722A warm orange
LUMA_PANTS     = (42, 40, 80)      # #2A2850 dark indigo
LUMA_SHOE_UP   = (245, 232, 208)   # #F5E8D0 cream canvas
LUMA_SHOE_SOLE = (199, 91, 57)     # #C75B39 terracotta sole
LUMA_EYE_W    = (250, 240, 220)    # #FAF0DC warm cream

# Byte
BYTE_TEAL     = (0, 212, 232)      # #00D4E8
BYTE_HL       = (0, 240, 255)      # #00F0FF
BYTE_SH       = (0, 144, 176)      # #0090B0
SCAR_MAG      = (255, 45, 107)     # #FF2D6B
BYTE_EYE_W   = (240, 240, 245)

# Cosmo
COSMO_SKIN     = (217, 192, 154)   # #D9C09A light warm olive
COSMO_HAIR     = (26, 24, 36)      # #1A1824 blue-black
COSMO_JACKET   = (168, 155, 191)   # #A89BBF dusty lavender
COSMO_SHIRT_B  = (91, 141, 184)    # #5B8DB8 cerulean stripe
COSMO_SHIRT_G  = (122, 158, 126)   # #7A9E7E sage stripe
COSMO_PANTS    = (140, 136, 128)   # #8C8880 warm mid-gray chinos
COSMO_FRAMES   = (92, 58, 32)      # #5C3A20 warm espresso glasses
COSMO_LENS_BG  = (238, 244, 255)   # #EEF4FF ghost blue lens tint
COSMO_SHOE     = (92, 58, 32)      # #5C3A20 espresso leather
COSMO_NB       = (91, 141, 184)    # #5B8DB8 cerulean notebook

# Miri
MIRI_SKIN      = (140, 84, 48)     # #8C5430 deep warm brown
MIRI_HAIR      = (216, 208, 200)   # #D8D0C8 warm silver
MIRI_CARDIGAN  = (184, 92, 56)     # #B85C38 terracotta rust
MIRI_PANTS     = (200, 174, 138)   # #C8AE8A warm linen tan
MIRI_SLIPPER   = (90, 122, 90)     # #5A7A5A deep sage

NEG_SPACE = BG


# ══════════════════════════════════════════════════════════════════════════════
# LUMA — colored lineup pose
# ══════════════════════════════════════════════════════════════════════════════

def draw_luma_lineup(draw, cx, base_y, h):
    """Luma at lineup height h, in color. Front facing."""
    hu = h / 3.5
    r  = int(hu * 0.46)
    hy = base_y - h

    # Hair
    draw.ellipse([cx - int(r*1.5), hy - int(r*0.6), cx + int(r*1.5), hy + int(r*0.8)],
                 fill=LUMA_HAIR, outline=LINE_COL, width=2)
    # Head
    draw.ellipse([cx - r, hy, cx + r, hy + int(hu)],
                 fill=LUMA_SKIN, outline=LINE_COL, width=2)
    # Eyes
    ey = hy + int(hu * 0.42)
    ew = int(hu * 0.14)
    draw.ellipse([cx - int(hu*0.22) - ew, ey - ew, cx - int(hu*0.22) + ew, ey + ew],
                 fill=LUMA_EYE_W, outline=LINE_COL, width=1)
    draw.ellipse([cx + int(hu*0.10) - ew, ey - ew, cx + int(hu*0.10) + ew, ey + ew],
                 fill=LUMA_EYE_W, outline=LINE_COL, width=1)
    # Mouth
    draw.arc([cx - int(hu*0.18), ey + int(hu*0.18), cx + int(hu*0.18), ey + int(hu*0.38)],
             start=20, end=160, fill=LINE_COL, width=2)

    # Hoodie body (A-line)
    sw  = int(hu * 0.38)
    hw2 = int(hu * 0.70)
    bt  = hy + int(hu * 0.85)
    bh  = int(hu * 2.0)
    bb  = bt + bh
    draw.polygon([(cx - sw, bt), (cx + sw, bt), (cx + hw2, bb), (cx - hw2, bb)],
                 fill=LUMA_HOODIE, outline=LINE_COL, width=2)
    # Pocket bump
    mid_frac = 0.55
    hem_mid  = cx + int(sw + (hw2 - sw) * mid_frac)
    py2 = bt + int(bh * 0.50)
    draw.rectangle([hem_mid, py2, hem_mid + int(hu*0.30), py2 + int(hu*0.42)],
                   fill=LUMA_HOODIE, outline=LINE_COL, width=1)
    # Hoodie pixel accents (3 small squares on chest)
    pix_y = bt + int(bh * 0.20)
    draw.rectangle([cx - int(hu*0.14), pix_y, cx - int(hu*0.06), pix_y + int(hu*0.06)],
                   fill=(0, 240, 255))
    draw.rectangle([cx - int(hu*0.04), pix_y, cx + int(hu*0.04), pix_y + int(hu*0.06)],
                   fill=(255, 45, 107))
    draw.rectangle([cx + int(hu*0.06), pix_y, cx + int(hu*0.14), pix_y + int(hu*0.06)],
                   fill=(0, 240, 255))

    # Pants (legs)
    lw = int(hu * 0.20)
    leg_h = int(hu * 0.55)
    draw.rectangle([cx - lw*2, bb, cx - 4, bb + leg_h], fill=LUMA_PANTS, outline=LINE_COL, width=1)
    draw.rectangle([cx + 4, bb, cx + lw*2, bb + leg_h], fill=LUMA_PANTS, outline=LINE_COL, width=1)

    # Shoes — cream upper, terracotta sole
    fw = int(hu * 0.52)
    fh = int(hu * 0.28)
    sole_h = int(fh * 0.35)
    draw.ellipse([cx - lw*2 - fw + int(fw*0.3), base_y - fh,
                  cx - lw*2 + int(fw*0.5),       base_y],
                 fill=LUMA_SHOE_UP, outline=LINE_COL, width=1)
    draw.ellipse([cx + lw*2 - int(fw*0.5),        base_y - fh,
                  cx + lw*2 + fw - int(fw*0.3),   base_y],
                 fill=LUMA_SHOE_UP, outline=LINE_COL, width=1)
    # Sole stripe
    draw.rectangle([cx - lw*2 - fw + int(fw*0.3), base_y - sole_h,
                    cx - lw*2 + int(fw*0.5), base_y],
                   fill=LUMA_SHOE_SOLE)
    draw.rectangle([cx + lw*2 - int(fw*0.5), base_y - sole_h,
                    cx + lw*2 + fw - int(fw*0.3), base_y],
                   fill=LUMA_SHOE_SOLE)


# ══════════════════════════════════════════════════════════════════════════════
# BYTE — colored lineup pose (floating, so base_y offset by float gap)
# ══════════════════════════════════════════════════════════════════════════════

def draw_byte_lineup(draw, cx, base_y, h):
    """Byte at lineup height h, in color. Oval body, floating."""
    s = h
    float_gap = int(s * 0.18)
    body_rx = s // 2
    body_ry = int(s * 0.55)
    bcy = base_y - float_gap - body_ry

    # Main oval body
    draw.ellipse([cx - body_rx, bcy - body_ry, cx + body_rx, bcy + body_ry],
                 fill=BYTE_TEAL, outline=LINE_COL, width=3)
    # Shadow right side
    shadow_pts = [
        (cx,               bcy - body_ry),
        (cx + body_rx,     bcy - body_ry + 4),
        (cx + body_rx,     bcy + body_ry - 4),
        (cx,               bcy + body_ry),
        (cx + body_rx//2,  bcy + body_ry),
        (cx + body_rx,     bcy + body_ry//2),
        (cx + body_rx,     bcy),
    ]
    draw.polygon(shadow_pts, fill=BYTE_SH)
    # Highlight arc
    draw.arc([cx - body_rx, bcy - body_ry, cx + body_rx, bcy + body_ry],
             start=200, end=310, fill=BYTE_HL, width=3)

    # Magenta scar
    crack_x = cx - s//4
    draw.line([(crack_x, bcy - body_ry//2), (crack_x + s//8, bcy - body_ry//6)],
              fill=SCAR_MAG, width=2)
    draw.line([(crack_x + s//8, bcy - body_ry//6), (crack_x - s//10, bcy + body_ry//6)],
              fill=SCAR_MAG, width=2)

    # Eyes
    eye_y  = bcy - body_ry // 5
    eye_sz = s // 4
    lx = cx - s//5
    cell = eye_sz // 5
    if cell < 1:
        cell = 1
    ox = lx - (5*cell)//2
    oy = eye_y - (5*cell)//2
    draw.rectangle([ox-2, oy-2, ox+5*cell+2, oy+5*cell+2],
                   fill=(255,255,255), outline=LINE_COL, width=1)
    # Normal pixel grid (2x2 squares)
    for row in range(2):
        for col in range(2):
            px = lx + col * (cell*2 + 2) - cell*2
            py = eye_y + row * (cell*2 + 2)
            draw.rectangle([px, py, px + cell*2, py + cell*2], fill=(0, 240, 255))
    # Right organic eye
    rx = cx + s//5
    er = s // 10
    draw.ellipse([rx - er, eye_y - er, rx + er, eye_y + er],
                 fill=BYTE_EYE_W, outline=LINE_COL, width=1)
    draw.ellipse([rx - er//2, eye_y - er//2, rx + er//2, eye_y + er//2],
                 fill=(60, 38, 20))

    # Arms
    lw = s // 6
    lh = s // 5
    arm_y = bcy - body_ry // 5
    draw.rectangle([cx - body_rx - lw, arm_y, cx - body_rx, arm_y + lh],
                   fill=BYTE_TEAL, outline=LINE_COL, width=2)
    draw.rectangle([cx + body_rx, arm_y, cx + body_rx + lw, arm_y + lh],
                   fill=BYTE_TEAL, outline=LINE_COL, width=2)

    # Legs
    leg_offset = s // 4
    leg_h = lh
    leg_w = int(lw * 0.9)
    draw.rectangle([cx - leg_offset - leg_w//2, bcy + body_ry,
                    cx - leg_offset + leg_w//2, bcy + body_ry + leg_h],
                   fill=BYTE_TEAL, outline=LINE_COL, width=2)
    draw.rectangle([cx + leg_offset - leg_w//2, bcy + body_ry,
                    cx + leg_offset + leg_w//2, bcy + body_ry + leg_h],
                   fill=BYTE_TEAL, outline=LINE_COL, width=2)

    # Hover particles — 10x10px
    particle_y = bcy + body_ry + leg_h + 4
    for (px, pc) in [(cx - int(s*0.28), BYTE_HL), (cx - int(s*0.08), SCAR_MAG),
                     (cx + int(s*0.08), BYTE_HL), (cx + int(s*0.24), (0, 200, 180))]:
        py = particle_y + (abs(px - cx) % 8)
        draw.rectangle([px, py, px + 10, py + 10], fill=pc)


# ══════════════════════════════════════════════════════════════════════════════
# COSMO — colored lineup pose
# ══════════════════════════════════════════════════════════════════════════════

def draw_cosmo_lineup(draw, cx, base_y, h):
    """Cosmo at lineup height h, in color. Front facing. Glasses always present."""
    hu = h / 4.0
    hy = base_y - h

    # Hair
    hw = int(hu * 0.40)
    hh = int(hu * 0.95)
    draw.ellipse([cx - hw - 4, hy - int(hu*0.08), cx + hw + 4, hy + int(hu*0.12)],
                 fill=COSMO_HAIR)
    draw.ellipse([cx - hw - 2, hy - int(hu*0.22), cx - int(hw*0.2), hy + int(hu*0.05)],
                 fill=COSMO_HAIR)
    # Head
    draw.rounded_rectangle([cx - hw, hy, cx + hw, hy + hh],
                            radius=6, fill=COSMO_SKIN, outline=LINE_COL, width=2)
    # Eyes (inside glasses)
    ey = hy + int(hh * 0.50)
    ew = int(hu * 0.12)
    draw.ellipse([cx - int(hu*0.30) - ew, ey - ew, cx - int(hu*0.30) + ew, ey + ew],
                 fill=COSMO_LENS_BG)
    draw.ellipse([cx + int(hu*0.30) - ew, ey - ew, cx + int(hu*0.30) + ew, ey + ew],
                 fill=COSMO_LENS_BG)
    # Pupils (green iris)
    ep = int(ew * 0.5)
    draw.ellipse([cx - int(hu*0.30) - ep, ey - ep, cx - int(hu*0.30) + ep, ey + ep],
                 fill=(61, 107, 69))
    draw.ellipse([cx + int(hu*0.30) - ep, ey - ep, cx + int(hu*0.30) + ep, ey + ep],
                 fill=(61, 107, 69))

    # Glasses frames (thick plastic, negative-space cutout)
    gr = int(hu * 0.18)
    gy = hy + int(hh * 0.48)
    rim = 3
    lcx = cx - int(hu * 0.30)
    rcx = cx + int(hu * 0.30)
    # Outer rim (espresso brown)
    draw.ellipse([lcx - gr - rim, gy - gr - rim, lcx + gr + rim, gy + gr + rim],
                 fill=COSMO_FRAMES, outline=LINE_COL, width=1)
    draw.ellipse([rcx - gr - rim, gy - gr - rim, rcx + gr + rim, gy + gr + rim],
                 fill=COSMO_FRAMES, outline=LINE_COL, width=1)
    # Inner lens tint
    draw.ellipse([lcx - gr, gy - gr, lcx + gr, gy + gr], fill=COSMO_LENS_BG)
    draw.ellipse([rcx - gr, gy - gr, rcx + gr, gy + gr], fill=COSMO_LENS_BG)
    # Bridge
    draw.rectangle([lcx + gr, gy - 2, rcx - gr, gy + 2], fill=COSMO_FRAMES)
    # Lens glare (white crescent)
    draw.arc([lcx - gr + 2, gy - gr + 2, lcx + gr - 2, gy - 2],
             start=200, end=340, fill=(240,240,240), width=2)
    draw.arc([rcx - gr + 2, gy - gr + 2, rcx + gr - 2, gy - 2],
             start=200, end=340, fill=(240,240,240), width=2)

    # Body — jacket over striped shirt
    bw = int(hu * 0.38)
    body_h = int(hu * 2.4)
    bt = hy + hh
    bb = bt + body_h
    # Shirt (striped — simplified as two colored bands)
    draw.rectangle([cx - bw, bt, cx + bw, bb], fill=COSMO_SHIRT_B, outline=LINE_COL, width=2)
    # Horizontal sage stripes
    stripe_h = int(hu * 0.15)
    sy = bt + int(body_h * 0.25)
    while sy + stripe_h < bb - int(body_h * 0.15):
        draw.rectangle([cx - bw + 2, sy, cx + bw - 2, sy + stripe_h], fill=COSMO_SHIRT_G)
        sy += stripe_h * 2
    # Jacket open over shirt (lavender, open front — two side panels)
    jw = int(hu * 0.14)
    draw.rectangle([cx - bw, bt, cx - bw + jw, bb], fill=COSMO_JACKET, outline=LINE_COL, width=1)
    draw.rectangle([cx + bw - jw, bt, cx + bw, bb], fill=COSMO_JACKET, outline=LINE_COL, width=1)

    # Notebook under left arm
    nw = int(hu * 0.48)
    nh = int(hu * 0.58)
    nb_y = bt + int(body_h * 0.28)
    draw.rectangle([cx - bw - nw + 10, nb_y, cx - bw + 10, nb_y + nh],
                   fill=COSMO_NB, outline=LINE_COL, width=1)

    # Pants
    lw = int(hu * 0.18)
    leg_h = int(hu * 0.60)
    draw.rectangle([cx - bw + 4, bb, cx - lw, bb + leg_h],
                   fill=COSMO_PANTS, outline=LINE_COL, width=1)
    draw.rectangle([cx + lw, bb, cx + bw - 4, bb + leg_h],
                   fill=COSMO_PANTS, outline=LINE_COL, width=1)
    # Center crease
    draw.line([(cx, bb + int(leg_h*0.3)), (cx, bb + leg_h)], fill=LINE_COL, width=1)

    # Shoes
    fw = int(hu * 0.28)
    fh = int(hu * 0.18)
    draw.ellipse([cx - bw + 4 - int(fw*0.4), base_y - fh, cx - lw + int(fw*0.6), base_y],
                 fill=COSMO_SHOE, outline=LINE_COL, width=1)
    draw.ellipse([cx + lw - int(fw*0.3), base_y - fh, cx + bw - 4 + int(fw*0.4), base_y],
                 fill=COSMO_SHOE, outline=LINE_COL, width=1)
    # Tan sole
    draw.ellipse([cx - bw + 4 - int(fw*0.4), base_y - int(fh*0.35),
                  cx - lw + int(fw*0.6), base_y], fill=(184, 154, 120))
    draw.ellipse([cx + lw - int(fw*0.3), base_y - int(fh*0.35),
                  cx + bw - 4 + int(fw*0.4), base_y], fill=(184, 154, 120))


# ══════════════════════════════════════════════════════════════════════════════
# MIRI — colored lineup pose (MIRI-A canonical)
# ══════════════════════════════════════════════════════════════════════════════

def draw_miri_lineup(draw, cx, base_y, h):
    """Miri (MIRI-A canonical) at lineup height h, in color.
    Bun + chopsticks, terracotta rust cardigan, soldering iron.
    """
    hu = h / 3.2
    hy = base_y - h
    r  = int(hu * 0.46)

    # BUN (silver hair)
    bun_cx = cx + int(hu * 0.05)
    bun_cy = hy - int(hu * 0.32)
    bun_rx = int(hu * 0.38)
    bun_ry = int(hu * 0.46)
    draw.ellipse([bun_cx - bun_rx, bun_cy - bun_ry,
                  bun_cx + bun_rx, bun_cy + bun_ry],
                 fill=MIRI_HAIR, outline=LINE_COL, width=2)
    # Shadow inside bun
    draw.arc([bun_cx - bun_rx + 4, bun_cy, bun_cx + bun_rx - 4, bun_cy + bun_ry],
             start=0, end=180, fill=(168, 152, 140), width=2)

    # CHOPSTICKS (warm espresso color)
    chopstick_col = (92, 58, 32)
    draw.polygon([(bun_cx - int(hu*0.22), bun_cy - bun_ry - int(hu*0.55)),
                  (bun_cx - int(hu*0.14), bun_cy - bun_ry - int(hu*0.55)),
                  (bun_cx - int(hu*0.06), bun_cy + bun_ry - int(hu*0.12)),
                  (bun_cx - int(hu*0.13), bun_cy + bun_ry - int(hu*0.12))],
                 fill=chopstick_col, outline=LINE_COL, width=1)
    draw.polygon([(bun_cx + int(hu*0.14), bun_cy - bun_ry - int(hu*0.50)),
                  (bun_cx + int(hu*0.22), bun_cy - bun_ry - int(hu*0.50)),
                  (bun_cx + int(hu*0.13), bun_cy + bun_ry - int(hu*0.12)),
                  (bun_cx + int(hu*0.06), bun_cy + bun_ry - int(hu*0.12))],
                 fill=chopstick_col, outline=LINE_COL, width=1)

    # Head
    draw.ellipse([cx - r, hy, cx + r, hy + int(hu)],
                 fill=MIRI_SKIN, outline=LINE_COL, width=2)
    # Eyes
    ey = hy + int(hu * 0.44)
    ew = int(hu * 0.12)
    draw.ellipse([cx - int(hu*0.22) - ew, ey - ew, cx - int(hu*0.22) + ew, ey + ew],
                 fill=(250,240,220), outline=LINE_COL, width=1)
    draw.ellipse([cx + int(hu*0.10) - ew, ey - ew, cx + int(hu*0.10) + ew, ey + ew],
                 fill=(250,240,220), outline=LINE_COL, width=1)
    # Iris (deep warm amber)
    ep = int(ew * 0.55)
    draw.ellipse([cx - int(hu*0.22) - ep, ey - ep, cx - int(hu*0.22) + ep, ey + ep],
                 fill=(139, 94, 60))
    draw.ellipse([cx + int(hu*0.10) - ep, ey - ep, cx + int(hu*0.10) + ep, ey + ep],
                 fill=(139, 94, 60))
    # Smile (warm grandmotherly expression)
    draw.arc([cx - int(hu*0.22), ey + int(hu*0.20), cx + int(hu*0.22), ey + int(hu*0.44)],
             start=20, end=160, fill=LINE_COL, width=2)
    # Permanent cheek blush
    blush_r = int(hu * 0.14)
    draw.ellipse([cx - int(hu*0.40) - blush_r, ey + int(hu*0.08),
                  cx - int(hu*0.40) + blush_r, ey + int(hu*0.08) + blush_r*2],
                 fill=(212, 149, 107))
    draw.ellipse([cx + int(hu*0.28) - blush_r, ey + int(hu*0.08),
                  cx + int(hu*0.28) + blush_r, ey + int(hu*0.08) + blush_r*2],
                 fill=(212, 149, 107))
    # Eyebrows (gray, soft)
    draw.line([(cx - int(hu*0.36), ey - int(hu*0.26)), (cx - int(hu*0.10), ey - int(hu*0.22))],
              fill=(138, 122, 112), width=2)
    draw.line([(cx + int(hu*0.00), ey - int(hu*0.22)), (cx + int(hu*0.26), ey - int(hu*0.26))],
              fill=(138, 122, 112), width=2)

    # CARDIGAN — inverted-flare (wide shoulder, slightly narrower hip)
    shoulder_w = int(hu * 0.78)
    hip_w      = int(hu * 0.62)
    body_top_y = hy + int(hu * 0.88)
    body_h     = int(hu * 1.82)
    body_bot_y = body_top_y + body_h
    draw.polygon([(cx - shoulder_w, body_top_y), (cx + shoulder_w, body_top_y),
                  (cx + hip_w, body_bot_y), (cx - hip_w, body_bot_y)],
                 fill=MIRI_CARDIGAN, outline=LINE_COL, width=2)
    # Cable-knit highlight ridges (simplified horizontal arcs)
    for i in range(3):
        ridge_y = body_top_y + int(body_h * (0.22 + i * 0.22))
        draw.line([(cx - int(shoulder_w * 0.6), ridge_y), (cx + int(shoulder_w * 0.6), ridge_y)],
                  fill=(212, 130, 90), width=2)
    # Cardigan buttons
    btn_col = (232, 216, 184)
    bx = cx - int(hu*0.08)
    for i in range(4):
        by = body_top_y + int(body_h * (0.12 + i * 0.22))
        draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=btn_col, outline=LINE_COL, width=1)

    # Bag on right hip
    bag_x = cx + hip_w
    bag_y = body_top_y + int(body_h * 0.52)
    bag_w = int(hu * 0.32)
    bag_h = int(hu * 0.46)
    draw.rectangle([bag_x, bag_y, bag_x + bag_w, bag_y + bag_h],
                   fill=(140, 100, 60), outline=LINE_COL, width=1)

    # SOLDERING IRON — right hand, terracotta handle
    iron_x = bag_x + bag_w
    iron_y = bag_y + bag_h - int(hu * 0.04)
    iron_len = int(hu * 0.50)
    iron_w   = int(hu * 0.07)
    draw.rectangle([iron_x, iron_y, iron_x + iron_len - int(iron_len*0.22), iron_y + iron_w + 2],
                   fill=(184, 92, 56), outline=LINE_COL, width=1)
    draw.polygon([(iron_x + iron_len - int(iron_len*0.22), iron_y),
                  (iron_x + iron_len - int(iron_len*0.22), iron_y + iron_w + 2),
                  (iron_x + iron_len, iron_y + (iron_w + 2)//2)],
                 fill=(200, 200, 200), outline=LINE_COL, width=1)

    # Pants (linen tan)
    lw = int(hu * 0.22)
    leg_h = int(hu * 0.45)
    draw.rectangle([cx - hip_w + 6, body_bot_y, cx - lw, body_bot_y + leg_h],
                   fill=MIRI_PANTS, outline=LINE_COL, width=1)
    draw.rectangle([cx + lw, body_bot_y, cx + hip_w - 6, body_bot_y + leg_h],
                   fill=MIRI_PANTS, outline=LINE_COL, width=1)

    # House slippers (deep sage)
    fw = int(hu * 0.30)
    fh = int(hu * 0.18)
    draw.rectangle([cx - hip_w + 4, base_y - fh, cx - lw + int(fw*0.4), base_y],
                   fill=MIRI_SLIPPER, outline=LINE_COL, width=1)
    draw.rectangle([cx + lw - int(fw*0.4), base_y - fh, cx + hip_w - 4, base_y],
                   fill=MIRI_SLIPPER, outline=LINE_COL, width=1)
    # Slipper cream lining
    draw.rectangle([cx - hip_w + 4, base_y - fh,
                    cx - lw + int(fw*0.4), base_y - fh + int(fh*0.30)],
                   fill=(250, 240, 220))
    draw.rectangle([cx + lw - int(fw*0.4), base_y - fh,
                    cx + hip_w - 4, base_y - fh + int(fh*0.30)],
                   fill=(250, 240, 220))


# ══════════════════════════════════════════════════════════════════════════════
# HEIGHT COMPARISON MARKERS
# ══════════════════════════════════════════════════════════════════════════════

def draw_height_markers(draw, font_small):
    """Draw horizontal dashed height reference lines connecting characters."""
    # Luma's top
    luma_top  = BASELINE_Y - CHAR_HEIGHTS["luma"]
    # Cosmo's top (tallest)
    cosmo_top = BASELINE_Y - CHAR_HEIGHTS["cosmo"]
    # Luma chest (Byte's height reference)
    luma_chest = BASELINE_Y - int(CHAR_HEIGHTS["luma"] * 0.62)
    # Miri's top
    miri_top  = BASELINE_Y - CHAR_HEIGHTS["miri"]

    lines = [
        (cosmo_top,  TICK_COL, "Cosmo top"),
        (luma_top,   (180, 140, 80), "Luma top"),
        (miri_top,   (140, 160, 120), "Miri top"),
        (luma_chest, (80, 160, 200), "Byte height / Luma chest"),
    ]

    x_start = 30
    x_end   = IMG_W - 30

    for y, col, label in lines:
        # Dashed line
        x = x_start
        dash = 8
        gap  = 5
        while x < x_end:
            draw.line([(x, y), (min(x + dash, x_end), y)], fill=col, width=1)
            x += dash + gap
        # Label at right edge
        draw.text((x_end + 4, y - 7), label, fill=col, font=font_small)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

def generate_lineup(output_path):
    img = Image.new('RGB', (IMG_W, IMG_H), BG)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
        font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except Exception:
        font_title = font_label = font_small = ImageFont.load_default()

    # Background panel
    draw.rectangle([0, 0, IMG_W, IMG_H], fill=BG)

    # Title
    title = "LUMA & THE GLITCHKIN — Character Height Lineup — Cycle 12"
    draw.text((20, 14), title, fill=LABEL_COL, font=font_title)
    draw.line([(0, TITLE_H - 4), (IMG_W, TITLE_H - 4)], fill=TICK_COL, width=1)

    # Baseline
    draw.line([(40, BASELINE_Y), (IMG_W - 20, BASELINE_Y)], fill=BASELINE_COL, width=2)

    # ── Cycle 12: Ground-floor annotation under Byte (Dmitri Volkov P1 — 3rd notice) ──
    # Byte floats above BASELINE_Y. A dashed ground-floor line at BASELINE_Y under Byte
    # + a labeled arrow makes the float-height explicit. Annotation is local to Byte's column.
    byte_cx   = CHAR_X["byte"]
    gf_x0     = byte_cx - 70
    gf_x1     = byte_cx + 70
    gf_y      = BASELINE_Y
    # Dashed ground-floor line (slightly thicker, distinct color from the shared baseline)
    # (100, 168, 200): one-off annotation color — cool blue-gray; distinct from BASELINE_COL
    # to read as a call-out, not as the shared height system line.
    GROUNDFLOOR_COL = (100, 168, 200)
    x = gf_x0
    while x < gf_x1:
        draw.line([(x, gf_y), (min(x + 10, gf_x1), gf_y)],
                  fill=GROUNDFLOOR_COL, width=2)
        x += 10 + 4
    # Label: "ground floor." with downward tick arrow
    label = "ground floor."
    lw_px = len(label) * 6
    label_x = byte_cx - lw_px // 2
    label_y = gf_y + 6
    draw.text((label_x, label_y), label, fill=GROUNDFLOOR_COL, font=font_small)
    # Small downward-pointing arrow above the label, on the line itself
    arrow_x = byte_cx
    draw.line([(arrow_x, gf_y - 1), (arrow_x, gf_y - 12)], fill=GROUNDFLOOR_COL, width=1)
    draw.polygon([(arrow_x - 4, gf_y - 12), (arrow_x + 4, gf_y - 12), (arrow_x, gf_y - 4)],
                 fill=GROUNDFLOOR_COL)

    # Height reference markers
    draw_height_markers(draw, font_small)

    # Draw all 4 characters
    char_drawers = {
        "luma":  draw_luma_lineup,
        "byte":  draw_byte_lineup,
        "cosmo": draw_cosmo_lineup,
        "miri":  draw_miri_lineup,
    }
    for char in CHAR_ORDER:
        cx = CHAR_X[char]
        h  = CHAR_HEIGHTS[char]
        char_drawers[char](draw, cx, BASELINE_Y, h)

    # Character name labels below baseline
    for char in CHAR_ORDER:
        cx   = CHAR_X[char]
        h    = CHAR_HEIGHTS[char]
        lines = CHAR_LABELS[char].split("\n")
        label_y = BASELINE_Y + 12
        for line in lines:
            lw = len(line) * 6
            draw.text((cx - lw // 2, label_y), line, fill=LABEL_COL, font=font_small)
            label_y += 14

    # Vertical height brackets for each character
    for char in CHAR_ORDER:
        cx = CHAR_X[char] - 40
        h  = CHAR_HEIGHTS[char]
        top_y = BASELINE_Y - h
        # For Byte use floating top
        if char == "byte":
            s = h
            float_gap = int(s * 0.18)
            body_ry   = int(s * 0.55)
            top_y = BASELINE_Y - float_gap - body_ry * 2
        draw.line([(cx, top_y), (cx, BASELINE_Y)], fill=TICK_COL, width=1)
        draw.line([(cx - 4, top_y), (cx + 4, top_y)], fill=TICK_COL, width=1)
        draw.line([(cx - 4, BASELINE_Y), (cx + 4, BASELINE_Y)], fill=TICK_COL, width=1)
        draw.text((cx - 20, (top_y + BASELINE_Y)//2 - 5), f"{h}px", fill=TICK_COL, font=font_small)

    # Footer
    footer = (
        "Heights shown at correct relative scale. "
        f"Reference: 1 head unit = {HEAD_UNIT:.0f}px. "
        "Colors per master_palette.md (canonical). Cycle 12 — ground floor annotation added."
    )
    draw.text((20, IMG_H - 18), footer, fill=TICK_COL, font=font_small)

    img.save(output_path)
    print(f"Saved: {output_path}")


def main():
    import os
    out_dir = "/home/wipkat/team/output/characters/main"
    os.makedirs(out_dir, exist_ok=True)
    # Cycle 12: new versioned output — never overwrite existing assets
    generate_lineup(os.path.join(out_dir, "LTG_CHAR_lineup_v002.png"))
    print("Character lineup generation complete.")


if __name__ == '__main__':
    main()
