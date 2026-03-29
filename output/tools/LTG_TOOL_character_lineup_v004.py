#!/usr/bin/env python3
"""
LTG_TOOL_character_lineup_v004.py
Character Lineup Generator — Luma & the Glitchkin
Cycle 24: Added GLITCH (5th character) to the lineup.

Cycle 24 changes (Maya Santos, Character Designer):
  - Added Glitch (antagonist Glitchkin) to the lineup. Placed at far right.
  - Glitch hovers — similar to Byte. Scale: same floating entity class as Byte
    but slightly taller diamond body (glitch_h ≈ BYTE_H * 1.05).
  - Glitch rendered in canonical colors: CORRUPT_AMBER body, HOT_MAG crack,
    UV_PURPLE shadow, VOID_BLACK outline. Diamond/rhombus form with pixel eyes.
  - N_CHARS updated 4→5. IMG_W expanded to accommodate 5 characters.
  - CHAR_ORDER: luma, byte, cosmo, miri, glitch.
  - Height marker updated: Glitch hover-top line added.
  - Footer updated to Cycle 24.
  - Output: LTG_CHAR_lineup_v004.png (never overwrites v003).

Cycle 14 changes (Alex Chen, Art Director):
  - Proper engineering dimension arrow for Byte float gap (Dmitri Volkov P1).
  - Title updated to "Cycle 14". Output: LTG_CHAR_lineup_v003.png.

Prior history:
  Cycle 12 (Alex Chen): Ground-floor annotation. Output: LTG_CHAR_lineup_v002.png.
  Cycle 10 (Alex Chen): Initial four-character lineup. Output: LTG_CHAR_lineup_v001.png.

Output: /home/wipkat/team/output/characters/main/LTG_CHAR_lineup_v004.png
Usage: python3 LTG_TOOL_character_lineup_v004.py
"""
from PIL import Image, ImageDraw, ImageFont
import math

# ── Canvas ────────────────────────────────────────────────────────────────────
BG           = (250, 248, 244)
PANEL_BG     = (245, 241, 235)
LINE_COL     = (59, 40, 32)       # #3B2820 Deep Cocoa
LABEL_COL    = (50, 40, 35)
TICK_COL     = (160, 148, 138)
BASELINE_COL = (180, 165, 150)

# ── Height system ─────────────────────────────────────────────────────────────
LUMA_RENDER_H = 280
LUMA_HEADS    = 3.5
HEAD_UNIT     = LUMA_RENDER_H / LUMA_HEADS   # ~80px

COSMO_HEADS   = 4.0
COSMO_H       = int(COSMO_HEADS * HEAD_UNIT)  # ~320px

MIRI_HEADS    = 3.2
MIRI_H        = int(MIRI_HEADS * HEAD_UNIT)   # ~256px

BYTE_H        = int(LUMA_RENDER_H * 0.58)     # ~162px

# Glitch: floating antagonist, slightly taller than Byte
# Diamond body ≈ Byte body height + top/bottom spikes. Comparable floating entity.
GLITCH_H      = int(BYTE_H * 1.05)            # ~170px

# ── Layout ────────────────────────────────────────────────────────────────────
CHAR_SPACING  = 240     # tighter spacing to fit 5 characters
LEFT_MARGIN   = 100
N_CHARS       = 5
IMG_W         = LEFT_MARGIN * 2 + CHAR_SPACING * (N_CHARS - 1) + 180
TITLE_H       = 50
HEADROOM      = int(COSMO_H * 1.15)
LABEL_AREA    = 80
IMG_H         = TITLE_H + HEADROOM + LABEL_AREA

BASELINE_Y    = TITLE_H + HEADROOM

CHAR_ORDER    = ["luma", "byte", "cosmo", "miri", "glitch"]
CHAR_X        = {
    "luma":   LEFT_MARGIN + 60,
    "byte":   LEFT_MARGIN + 60 + CHAR_SPACING - 40,
    "cosmo":  LEFT_MARGIN + 60 + CHAR_SPACING * 2 - 20,
    "miri":   LEFT_MARGIN + 60 + CHAR_SPACING * 3,
    "glitch": LEFT_MARGIN + 60 + CHAR_SPACING * 4 + 10,
}
CHAR_HEIGHTS  = {
    "luma":   LUMA_RENDER_H,
    "byte":   BYTE_H,
    "cosmo":  COSMO_H,
    "miri":   MIRI_H,
    "glitch": GLITCH_H,
}
CHAR_LABELS   = {
    "luma":   f"LUMA\n3.5 heads / {LUMA_RENDER_H}px",
    "byte":   f"BYTE\n~Luma chest / {BYTE_H}px",
    "cosmo":  f"COSMO\n4.0 heads / {COSMO_H}px",
    "miri":   f"MIRI\n3.2 heads / {MIRI_H}px",
    "glitch": f"GLITCH\n~Byte scale / {GLITCH_H}px",
}

# ── Colors ────────────────────────────────────────────────────────────────────
# Luma
LUMA_SKIN      = (196, 168, 130)
LUMA_HAIR      = (26, 15, 10)
LUMA_HOODIE    = (232, 114, 42)
LUMA_PANTS     = (42, 40, 80)
LUMA_SHOE_UP   = (245, 232, 208)
LUMA_SHOE_SOLE = (199, 91, 57)
LUMA_EYE_W    = (250, 240, 220)

# Byte
BYTE_TEAL     = (0, 212, 232)
BYTE_HL       = (0, 240, 255)
BYTE_SH       = (0, 144, 176)
SCAR_MAG      = (255, 45, 107)
BYTE_EYE_W   = (240, 240, 245)

# Cosmo
COSMO_SKIN     = (217, 192, 154)
COSMO_HAIR     = (26, 24, 36)
COSMO_JACKET   = (168, 155, 191)
COSMO_SHIRT_B  = (91, 141, 184)
COSMO_SHIRT_G  = (122, 158, 126)
COSMO_PANTS    = (140, 136, 128)
COSMO_FRAMES   = (92, 58, 32)
COSMO_LENS_BG  = (238, 244, 255)
COSMO_SHOE     = (92, 58, 32)
COSMO_NB       = (91, 141, 184)

# Miri
MIRI_SKIN      = (140, 84, 48)
MIRI_HAIR      = (216, 208, 200)
MIRI_CARDIGAN  = (184, 92, 56)
MIRI_PANTS     = (200, 174, 138)
MIRI_SLIPPER   = (90, 122, 90)

# Glitch
GLITCH_AMB    = (255, 140,   0)   # CORRUPT_AMBER GL-07
GLITCH_AMB_SH = (168,  76,   0)   # CORRUPT_AMB_SHADOW
GLITCH_AMB_HL = (255, 185,  80)   # warm highlight
GLITCH_HOT    = (255,  45, 107)   # HOT_MAGENTA — crack/scar
GLITCH_UV     = (123,  47, 190)   # UV_PURPLE — shadow
GLITCH_GOLD   = (232, 201,  90)   # SOFT_GOLD — pixel eye glow
GLITCH_VB     = ( 10,  10,  20)   # VOID_BLACK — outline
GLITCH_ACID   = ( 57, 255,  20)   # ACID_GREEN — pixel alive state

NEG_SPACE = BG


# ══════════════════════════════════════════════════════════════════════════════
# LUMA
# ══════════════════════════════════════════════════════════════════════════════

def draw_luma_lineup(draw, cx, base_y, h):
    hu = h / 3.5
    r  = int(hu * 0.46)
    hy = base_y - h

    draw.ellipse([cx - int(r*1.5), hy - int(r*0.6), cx + int(r*1.5), hy + int(r*0.8)],
                 fill=LUMA_HAIR, outline=LINE_COL, width=2)
    draw.ellipse([cx - r, hy, cx + r, hy + int(hu)],
                 fill=LUMA_SKIN, outline=LINE_COL, width=2)
    ey = hy + int(hu * 0.42)
    ew = int(hu * 0.14)
    draw.ellipse([cx - int(hu*0.22) - ew, ey - ew, cx - int(hu*0.22) + ew, ey + ew],
                 fill=LUMA_EYE_W, outline=LINE_COL, width=1)
    draw.ellipse([cx + int(hu*0.10) - ew, ey - ew, cx + int(hu*0.10) + ew, ey + ew],
                 fill=LUMA_EYE_W, outline=LINE_COL, width=1)
    draw.arc([cx - int(hu*0.18), ey + int(hu*0.18), cx + int(hu*0.18), ey + int(hu*0.38)],
             start=20, end=160, fill=LINE_COL, width=2)

    sw  = int(hu * 0.38)
    hw2 = int(hu * 0.70)
    bt  = hy + int(hu * 0.85)
    bh  = int(hu * 2.0)
    bb  = bt + bh
    draw.polygon([(cx - sw, bt), (cx + sw, bt), (cx + hw2, bb), (cx - hw2, bb)],
                 fill=LUMA_HOODIE, outline=LINE_COL, width=2)
    mid_frac = 0.55
    hem_mid  = cx + int(sw + (hw2 - sw) * mid_frac)
    py2 = bt + int(bh * 0.50)
    draw.rectangle([hem_mid, py2, hem_mid + int(hu*0.30), py2 + int(hu*0.42)],
                   fill=LUMA_HOODIE, outline=LINE_COL, width=1)
    pix_y = bt + int(bh * 0.20)
    draw.rectangle([cx - int(hu*0.14), pix_y, cx - int(hu*0.06), pix_y + int(hu*0.06)],
                   fill=(0, 240, 255))
    draw.rectangle([cx - int(hu*0.04), pix_y, cx + int(hu*0.04), pix_y + int(hu*0.06)],
                   fill=(255, 45, 107))
    draw.rectangle([cx + int(hu*0.06), pix_y, cx + int(hu*0.14), pix_y + int(hu*0.06)],
                   fill=(0, 240, 255))

    lw = int(hu * 0.20)
    leg_h = int(hu * 0.55)
    draw.rectangle([cx - lw*2, bb, cx - 4, bb + leg_h], fill=LUMA_PANTS, outline=LINE_COL, width=1)
    draw.rectangle([cx + 4, bb, cx + lw*2, bb + leg_h], fill=LUMA_PANTS, outline=LINE_COL, width=1)

    fw = int(hu * 0.52)
    fh = int(hu * 0.28)
    sole_h = int(fh * 0.35)
    draw.ellipse([cx - lw*2 - fw + int(fw*0.3), base_y - fh,
                  cx - lw*2 + int(fw*0.5), base_y],
                 fill=LUMA_SHOE_UP, outline=LINE_COL, width=1)
    draw.ellipse([cx + lw*2 - int(fw*0.5), base_y - fh,
                  cx + lw*2 + fw - int(fw*0.3), base_y],
                 fill=LUMA_SHOE_UP, outline=LINE_COL, width=1)
    draw.rectangle([cx - lw*2 - fw + int(fw*0.3), base_y - sole_h,
                    cx - lw*2 + int(fw*0.5), base_y], fill=LUMA_SHOE_SOLE)
    draw.rectangle([cx + lw*2 - int(fw*0.5), base_y - sole_h,
                    cx + lw*2 + fw - int(fw*0.3), base_y], fill=LUMA_SHOE_SOLE)


# ══════════════════════════════════════════════════════════════════════════════
# BYTE
# ══════════════════════════════════════════════════════════════════════════════

def draw_byte_lineup(draw, cx, base_y, h):
    s         = h
    float_gap = int(s * 0.18)
    body_rx   = s // 2
    body_ry   = int(s * 0.55)
    bcy       = base_y - float_gap - body_ry

    draw.ellipse([cx - body_rx, bcy - body_ry, cx + body_rx, bcy + body_ry],
                 fill=BYTE_TEAL, outline=LINE_COL, width=3)
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
    draw.arc([cx - body_rx, bcy - body_ry, cx + body_rx, bcy + body_ry],
             start=200, end=310, fill=BYTE_HL, width=3)

    crack_x = cx - s//4
    draw.line([(crack_x, bcy - body_ry//2), (crack_x + s//8, bcy - body_ry//6)],
              fill=SCAR_MAG, width=2)
    draw.line([(crack_x + s//8, bcy - body_ry//6), (crack_x - s//10, bcy + body_ry//6)],
              fill=SCAR_MAG, width=2)

    eye_y  = bcy - body_ry // 5
    eye_sz = s // 4
    lx     = cx - s//5
    cell   = eye_sz // 5
    if cell < 1:
        cell = 1
    ox = lx - (5*cell)//2
    oy = eye_y - (5*cell)//2
    draw.rectangle([ox-2, oy-2, ox+5*cell+2, oy+5*cell+2],
                   fill=(255,255,255), outline=LINE_COL, width=1)
    for row in range(2):
        for col in range(2):
            px = lx + col * (cell*2 + 2) - cell*2
            py = eye_y + row * (cell*2 + 2)
            draw.rectangle([px, py, px + cell*2, py + cell*2], fill=(0, 240, 255))
    rx = cx + s//5
    er = s // 10
    draw.ellipse([rx - er, eye_y - er, rx + er, eye_y + er],
                 fill=BYTE_EYE_W, outline=LINE_COL, width=1)
    draw.ellipse([rx - er//2, eye_y - er//2, rx + er//2, eye_y + er//2],
                 fill=(60, 38, 20))

    lw = s // 6
    lh = s // 5
    arm_y = bcy - body_ry // 5
    draw.rectangle([cx - body_rx - lw, arm_y, cx - body_rx, arm_y + lh],
                   fill=BYTE_TEAL, outline=LINE_COL, width=2)
    draw.rectangle([cx + body_rx, arm_y, cx + body_rx + lw, arm_y + lh],
                   fill=BYTE_TEAL, outline=LINE_COL, width=2)

    leg_offset = s // 4
    leg_h = lh
    leg_w = int(lw * 0.9)
    draw.rectangle([cx - leg_offset - leg_w//2, bcy + body_ry,
                    cx - leg_offset + leg_w//2, bcy + body_ry + leg_h],
                   fill=BYTE_TEAL, outline=LINE_COL, width=2)
    draw.rectangle([cx + leg_offset - leg_w//2, bcy + body_ry,
                    cx + leg_offset + leg_w//2, bcy + body_ry + leg_h],
                   fill=BYTE_TEAL, outline=LINE_COL, width=2)

    particle_y = bcy + body_ry + leg_h + 4
    for (px, pc) in [(cx - int(s*0.28), BYTE_HL), (cx - int(s*0.08), SCAR_MAG),
                     (cx + int(s*0.08), BYTE_HL), (cx + int(s*0.24), (0, 200, 180))]:
        py = particle_y + (abs(px - cx) % 8)
        draw.rectangle([px, py, px + 10, py + 10], fill=pc)


# ══════════════════════════════════════════════════════════════════════════════
# COSMO
# ══════════════════════════════════════════════════════════════════════════════

def draw_cosmo_lineup(draw, cx, base_y, h):
    hu = h / 4.0
    hy = base_y - h

    hw = int(hu * 0.40)
    hh = int(hu * 0.95)
    draw.ellipse([cx - hw - 4, hy - int(hu*0.08), cx + hw + 4, hy + int(hu*0.12)],
                 fill=COSMO_HAIR)
    draw.ellipse([cx - hw - 2, hy - int(hu*0.22), cx - int(hw*0.2), hy + int(hu*0.05)],
                 fill=COSMO_HAIR)
    draw.rounded_rectangle([cx - hw, hy, cx + hw, hy + hh],
                            radius=6, fill=COSMO_SKIN, outline=LINE_COL, width=2)
    ey = hy + int(hh * 0.50)
    ew = int(hu * 0.12)
    draw.ellipse([cx - int(hu*0.30) - ew, ey - ew, cx - int(hu*0.30) + ew, ey + ew],
                 fill=COSMO_LENS_BG)
    draw.ellipse([cx + int(hu*0.30) - ew, ey - ew, cx + int(hu*0.30) + ew, ey + ew],
                 fill=COSMO_LENS_BG)
    ep = int(ew * 0.5)
    draw.ellipse([cx - int(hu*0.30) - ep, ey - ep, cx - int(hu*0.30) + ep, ey + ep],
                 fill=(61, 107, 69))
    draw.ellipse([cx + int(hu*0.30) - ep, ey - ep, cx + int(hu*0.30) + ep, ey + ep],
                 fill=(61, 107, 69))

    gr  = int(hu * 0.18)
    gy  = hy + int(hh * 0.48)
    rim = 3
    lcx = cx - int(hu * 0.30)
    rcx = cx + int(hu * 0.30)
    draw.ellipse([lcx - gr - rim, gy - gr - rim, lcx + gr + rim, gy + gr + rim],
                 fill=COSMO_FRAMES, outline=LINE_COL, width=1)
    draw.ellipse([rcx - gr - rim, gy - gr - rim, rcx + gr + rim, gy + gr + rim],
                 fill=COSMO_FRAMES, outline=LINE_COL, width=1)
    draw.ellipse([lcx - gr, gy - gr, lcx + gr, gy + gr], fill=COSMO_LENS_BG)
    draw.ellipse([rcx - gr, gy - gr, rcx + gr, gy + gr], fill=COSMO_LENS_BG)
    draw.rectangle([lcx + gr, gy - 2, rcx - gr, gy + 2], fill=COSMO_FRAMES)
    draw.arc([lcx - gr + 2, gy - gr + 2, lcx + gr - 2, gy - 2],
             start=200, end=340, fill=(240,240,240), width=2)
    draw.arc([rcx - gr + 2, gy - gr + 2, rcx + gr - 2, gy - 2],
             start=200, end=340, fill=(240,240,240), width=2)

    bw     = int(hu * 0.38)
    body_h = int(hu * 2.4)
    bt     = hy + hh
    bb     = bt + body_h
    draw.rectangle([cx - bw, bt, cx + bw, bb], fill=COSMO_SHIRT_B, outline=LINE_COL, width=2)
    stripe_h = int(hu * 0.15)
    sy = bt + int(body_h * 0.25)
    while sy + stripe_h < bb - int(body_h * 0.15):
        draw.rectangle([cx - bw + 2, sy, cx + bw - 2, sy + stripe_h], fill=COSMO_SHIRT_G)
        sy += stripe_h * 2
    jw = int(hu * 0.14)
    draw.rectangle([cx - bw, bt, cx - bw + jw, bb], fill=COSMO_JACKET, outline=LINE_COL, width=1)
    draw.rectangle([cx + bw - jw, bt, cx + bw, bb], fill=COSMO_JACKET, outline=LINE_COL, width=1)

    nw   = int(hu * 0.48)
    nh   = int(hu * 0.58)
    nb_y = bt + int(body_h * 0.28)
    draw.rectangle([cx - bw - nw + 10, nb_y, cx - bw + 10, nb_y + nh],
                   fill=COSMO_NB, outline=LINE_COL, width=1)

    lw    = int(hu * 0.18)
    leg_h = int(hu * 0.60)
    draw.rectangle([cx - bw + 4, bb, cx - lw, bb + leg_h],
                   fill=COSMO_PANTS, outline=LINE_COL, width=1)
    draw.rectangle([cx + lw, bb, cx + bw - 4, bb + leg_h],
                   fill=COSMO_PANTS, outline=LINE_COL, width=1)
    draw.line([(cx, bb + int(leg_h*0.3)), (cx, bb + leg_h)], fill=LINE_COL, width=1)

    fw = int(hu * 0.28)
    fh = int(hu * 0.18)
    draw.ellipse([cx - bw + 4 - int(fw*0.4), base_y - fh, cx - lw + int(fw*0.6), base_y],
                 fill=COSMO_SHOE, outline=LINE_COL, width=1)
    draw.ellipse([cx + lw - int(fw*0.3), base_y - fh, cx + bw - 4 + int(fw*0.4), base_y],
                 fill=COSMO_SHOE, outline=LINE_COL, width=1)
    draw.ellipse([cx - bw + 4 - int(fw*0.4), base_y - int(fh*0.35),
                  cx - lw + int(fw*0.6), base_y], fill=(184, 154, 120))
    draw.ellipse([cx + lw - int(fw*0.3), base_y - int(fh*0.35),
                  cx + bw - 4 + int(fw*0.4), base_y], fill=(184, 154, 120))


# ══════════════════════════════════════════════════════════════════════════════
# MIRI
# ══════════════════════════════════════════════════════════════════════════════

def draw_miri_lineup(draw, cx, base_y, h):
    hu = h / 3.2
    hy = base_y - h
    r  = int(hu * 0.46)

    bun_cx = cx + int(hu * 0.05)
    bun_cy = hy - int(hu * 0.32)
    bun_rx = int(hu * 0.38)
    bun_ry = int(hu * 0.46)
    draw.ellipse([bun_cx - bun_rx, bun_cy - bun_ry,
                  bun_cx + bun_rx, bun_cy + bun_ry],
                 fill=MIRI_HAIR, outline=LINE_COL, width=2)
    draw.arc([bun_cx - bun_rx + 4, bun_cy, bun_cx + bun_rx - 4, bun_cy + bun_ry],
             start=0, end=180, fill=(168, 152, 140), width=2)

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

    draw.ellipse([cx - r, hy, cx + r, hy + int(hu)],
                 fill=MIRI_SKIN, outline=LINE_COL, width=2)
    ey = hy + int(hu * 0.44)
    ew = int(hu * 0.12)
    draw.ellipse([cx - int(hu*0.22) - ew, ey - ew, cx - int(hu*0.22) + ew, ey + ew],
                 fill=(250,240,220), outline=LINE_COL, width=1)
    draw.ellipse([cx + int(hu*0.10) - ew, ey - ew, cx + int(hu*0.10) + ew, ey + ew],
                 fill=(250,240,220), outline=LINE_COL, width=1)
    ep = int(ew * 0.55)
    draw.ellipse([cx - int(hu*0.22) - ep, ey - ep, cx - int(hu*0.22) + ep, ey + ep],
                 fill=(139, 94, 60))
    draw.ellipse([cx + int(hu*0.10) - ep, ey - ep, cx + int(hu*0.10) + ep, ey + ep],
                 fill=(139, 94, 60))
    draw.arc([cx - int(hu*0.22), ey + int(hu*0.20), cx + int(hu*0.22), ey + int(hu*0.44)],
             start=20, end=160, fill=LINE_COL, width=2)
    blush_r = int(hu * 0.14)
    draw.ellipse([cx - int(hu*0.40) - blush_r, ey + int(hu*0.08),
                  cx - int(hu*0.40) + blush_r, ey + int(hu*0.08) + blush_r*2],
                 fill=(212, 149, 107))
    draw.ellipse([cx + int(hu*0.28) - blush_r, ey + int(hu*0.08),
                  cx + int(hu*0.28) + blush_r, ey + int(hu*0.08) + blush_r*2],
                 fill=(212, 149, 107))
    draw.line([(cx - int(hu*0.36), ey - int(hu*0.26)), (cx - int(hu*0.10), ey - int(hu*0.22))],
              fill=(138, 122, 112), width=2)
    draw.line([(cx + int(hu*0.00), ey - int(hu*0.22)), (cx + int(hu*0.26), ey - int(hu*0.26))],
              fill=(138, 122, 112), width=2)

    shoulder_w = int(hu * 0.78)
    hip_w      = int(hu * 0.62)
    body_top_y = hy + int(hu * 0.88)
    body_h     = int(hu * 1.82)
    body_bot_y = body_top_y + body_h
    draw.polygon([(cx - shoulder_w, body_top_y), (cx + shoulder_w, body_top_y),
                  (cx + hip_w, body_bot_y), (cx - hip_w, body_bot_y)],
                 fill=MIRI_CARDIGAN, outline=LINE_COL, width=2)
    for i in range(3):
        ridge_y = body_top_y + int(body_h * (0.22 + i * 0.22))
        draw.line([(cx - int(shoulder_w * 0.6), ridge_y), (cx + int(shoulder_w * 0.6), ridge_y)],
                  fill=(212, 130, 90), width=2)
    btn_col = (232, 216, 184)
    bx = cx - int(hu*0.08)
    for i in range(4):
        by = body_top_y + int(body_h * (0.12 + i * 0.22))
        draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=btn_col, outline=LINE_COL, width=1)

    bag_x = cx + hip_w
    bag_y = body_top_y + int(body_h * 0.52)
    bag_w = int(hu * 0.32)
    bag_h = int(hu * 0.46)
    draw.rectangle([bag_x, bag_y, bag_x + bag_w, bag_y + bag_h],
                   fill=(140, 100, 60), outline=LINE_COL, width=1)

    iron_x   = bag_x + bag_w
    iron_y   = bag_y + bag_h - int(hu * 0.04)
    iron_len = int(hu * 0.50)
    iron_w   = int(hu * 0.07)
    draw.rectangle([iron_x, iron_y, iron_x + iron_len - int(iron_len*0.22), iron_y + iron_w + 2],
                   fill=(184, 92, 56), outline=LINE_COL, width=1)
    draw.polygon([(iron_x + iron_len - int(iron_len*0.22), iron_y),
                  (iron_x + iron_len - int(iron_len*0.22), iron_y + iron_w + 2),
                  (iron_x + iron_len, iron_y + (iron_w + 2)//2)],
                 fill=(200, 200, 200), outline=LINE_COL, width=1)

    lw    = int(hu * 0.22)
    leg_h = int(hu * 0.45)
    draw.rectangle([cx - hip_w + 6, body_bot_y, cx - lw, body_bot_y + leg_h],
                   fill=MIRI_PANTS, outline=LINE_COL, width=1)
    draw.rectangle([cx + lw, body_bot_y, cx + hip_w - 6, body_bot_y + leg_h],
                   fill=MIRI_PANTS, outline=LINE_COL, width=1)

    fw = int(hu * 0.30)
    fh = int(hu * 0.18)
    draw.rectangle([cx - hip_w + 4, base_y - fh, cx - lw + int(fw*0.4), base_y],
                   fill=MIRI_SLIPPER, outline=LINE_COL, width=1)
    draw.rectangle([cx + lw - int(fw*0.4), base_y - fh, cx + hip_w - 4, base_y],
                   fill=MIRI_SLIPPER, outline=LINE_COL, width=1)
    draw.rectangle([cx - hip_w + 4, base_y - fh,
                    cx - lw + int(fw*0.4), base_y - fh + int(fh*0.30)],
                   fill=(250, 240, 220))
    draw.rectangle([cx + lw - int(fw*0.4), base_y - fh,
                    cx + hip_w - 4, base_y - fh + int(fh*0.30)],
                   fill=(250, 240, 220))


# ══════════════════════════════════════════════════════════════════════════════
# GLITCH — floating antagonist Glitchkin
# Diamond/rhombus body, CORRUPT_AMBER, HOT_MAG cracks, dual pixel eyes.
# Floats above baseline (similar to Byte), confetti particles below.
# ══════════════════════════════════════════════════════════════════════════════

def draw_glitch_lineup(draw, cx, base_y, h):
    """Glitch at lineup height h, in canonical Corrupt Amber palette.
    Neutral/idle stance for lineup context.
    Float gap = 18% of h (same ratio as Byte).
    """
    import math as _math

    float_gap = int(h * 0.18)
    # Diamond body: rx = half-width, ry = half-height
    rx = int(h * 0.38)
    ry = int(h * 0.32)
    # Body center Y: base_y - float_gap - ry (center of diamond)
    bcy = base_y - float_gap - ry

    # ── Shadow layer (UV Purple) ──────────────────────────────────────────────
    def dpts(tilt=0, sq=1.0, st=1.0, ox=0, oy=0):
        ry_e = int(ry * sq * st)
        a    = _math.radians(tilt)
        top  = (cx + ox + int(rx*0.15*_math.sin(a)), bcy + oy - ry_e)
        rpt  = (cx + ox + int(rx*_math.cos(-a)),     bcy + oy + int(rx*0.2*_math.sin(-a)))
        bot  = (cx + ox - int(rx*0.15*_math.sin(a)), bcy + oy + int(ry_e*1.15))
        lpt  = (cx + ox - int(rx*_math.cos(-a)),     bcy + oy - int(rx*0.2*_math.sin(-a)))
        return [top, rpt, bot, lpt]

    sh_pts = dpts(ox=3, oy=4)
    draw.polygon(sh_pts, fill=GLITCH_UV)

    # ── Main body (Corrupt Amber) ─────────────────────────────────────────────
    body_pts = dpts()
    draw.polygon(body_pts, fill=GLITCH_AMB)

    # Highlight facet (top-left)
    top, rpt, bot, lpt = body_pts
    mid_tl = ((top[0] + lpt[0]) // 2, (top[1] + lpt[1]) // 2)
    ctr    = (cx, bcy - ry // 4)
    draw.polygon([top, ctr, mid_tl], fill=GLITCH_AMB_HL)

    # Silhouette outline
    draw.polygon(body_pts, outline=GLITCH_VB, width=3)

    # HOT_MAG crack (interior structure)
    crack_s = (cx - rx // 2, bcy - ry // 3)
    crack_e = (cx + rx // 3, bcy + ry // 2)
    draw.line([crack_s, crack_e], fill=GLITCH_HOT, width=2)
    mid_c   = ((crack_s[0] + crack_e[0]) // 2, (crack_s[1] + crack_e[1]) // 2)
    draw.line([mid_c, (cx + rx // 2, bcy - ry // 4)], fill=GLITCH_HOT, width=1)

    # ── Top spike ─────────────────────────────────────────────────────────────
    cy_top   = bcy - ry
    spike_h  = max(8, h // 16)
    sx       = cx
    spike_pts = [
        (sx - spike_h // 2, cy_top),
        (sx - spike_h,      cy_top - spike_h),
        (sx,                cy_top - spike_h * 2),
        (sx + spike_h,      cy_top - spike_h),
        (sx + spike_h // 2, cy_top),
    ]
    draw.polygon(spike_pts, fill=GLITCH_AMB)
    draw.polygon(spike_pts, outline=GLITCH_VB, width=2)
    draw.line([(sx, cy_top - spike_h * 2), (sx, cy_top - spike_h * 2 - 4)],
              fill=GLITCH_HOT, width=2)

    # ── Bottom spike ──────────────────────────────────────────────────────────
    cy_bot   = bcy + int(ry * 1.15)
    bsp_h    = max(6, h // 18)
    bsp_pts  = [
        (cx - bsp_h // 2, cy_bot),
        (cx + bsp_h // 2, cy_bot),
        (cx, cy_bot + bsp_h + 3),
    ]
    draw.polygon(bsp_pts, fill=GLITCH_AMB_SH)
    draw.polygon(bsp_pts, outline=GLITCH_VB, width=2)

    # ── Arms (spike stubs) ────────────────────────────────────────────────────
    arm_y  = bcy
    tip_sz = max(10, h // 14)
    # Left arm
    lax = cx - rx - 4
    draw.polygon([(lax, arm_y - 4), (lax, arm_y + 4), (lax - tip_sz, arm_y - 6)],
                 fill=GLITCH_AMB)
    draw.polygon([(lax, arm_y - 4), (lax, arm_y + 4), (lax - tip_sz, arm_y - 6)],
                 outline=GLITCH_VB, width=2)
    # Right arm
    rax = cx + rx + 4
    draw.polygon([(rax, arm_y - 4), (rax, arm_y + 4), (rax + tip_sz, arm_y - 6)],
                 fill=GLITCH_AMB)
    draw.polygon([(rax, arm_y - 4), (rax, arm_y + 4), (rax + tip_sz, arm_y - 6)],
                 outline=GLITCH_VB, width=2)

    # ── Pixel eyes (3×3 each, neutral glyph) ─────────────────────────────────
    # Neutral left glyph: cross/diamond — watchful
    NEUTRAL_L = [[0, 2, 0],
                 [2, 1, 2],
                 [0, 2, 0]]
    # Neutral right glyph: destabilized
    NEUTRAL_R = [[1, 2, 0],
                 [2, 0, 1],
                 [0, 2, 1]]
    PIXEL_COLS = {
        0: GLITCH_VB,
        1: GLITCH_AMB_SH,
        2: GLITCH_AMB,
        3: GLITCH_GOLD,
        4: GLITCH_HOT,
        5: GLITCH_ACID,
    }
    cell     = max(3, h // 46)
    face_cy  = bcy - ry // 6
    leye_x   = cx - rx // 2 - cell * 3 // 2
    leye_y   = face_cy - cell * 3 // 2
    reye_x   = cx + rx // 2 - cell * 3 // 2
    reye_y   = face_cy - cell * 3 // 2

    for row in range(3):
        for col in range(3):
            # Left eye
            state = NEUTRAL_L[row][col]
            px    = leye_x + col * cell
            py    = leye_y + row * cell
            draw.rectangle([px, py, px + cell - 1, py + cell - 1],
                            fill=PIXEL_COLS[state])
            # Right eye (destabilized)
            state = NEUTRAL_R[row][col]
            px    = reye_x + col * cell
            py    = reye_y + row * cell
            draw.rectangle([px, py, px + cell - 1, py + cell - 1],
                            fill=PIXEL_COLS[state])

    # Flat neutral mouth (3 dim amber dots)
    mouth_cx = cx - 5
    mouth_cy = face_cy + cell * 3 // 2 + 3
    for i in range(3):
        draw.rectangle([mouth_cx + i * 4, mouth_cy,
                        mouth_cx + i * 4 + 2, mouth_cy + 2],
                       fill=GLITCH_AMB_SH)

    # Flat brow bars (neutral)
    draw.line([(leye_x, leye_y - 3), (leye_x + cell * 3, leye_y - 3)],
              fill=GLITCH_AMB_SH, width=1)
    draw.line([(reye_x, reye_y - 3), (reye_x + cell * 3, reye_y - 3)],
              fill=GLITCH_AMB_SH, width=1)

    # ── Hover confetti (Hot Mag / UV Purple — corrupted) ─────────────────────
    import random as _random
    rng = _random.Random(42)
    confetti_y = cy_bot + bsp_h + 5
    for _ in range(8):
        px  = rng.randint(cx - 20, cx + 20)
        py  = rng.randint(confetti_y, confetti_y + 14)
        col = rng.choice([GLITCH_HOT, GLITCH_UV, GLITCH_VB])
        draw.rectangle([px, py, px + 3, py + 3], fill=col)


# ══════════════════════════════════════════════════════════════════════════════
# HEIGHT COMPARISON MARKERS
# ══════════════════════════════════════════════════════════════════════════════

def draw_height_markers(draw, font_small):
    luma_top   = BASELINE_Y - CHAR_HEIGHTS["luma"]
    cosmo_top  = BASELINE_Y - CHAR_HEIGHTS["cosmo"]
    luma_chest = BASELINE_Y - int(CHAR_HEIGHTS["luma"] * 0.62)
    miri_top   = BASELINE_Y - CHAR_HEIGHTS["miri"]

    lines = [
        (cosmo_top,  TICK_COL,           "Cosmo top"),
        (luma_top,   (180, 140, 80),      "Luma top"),
        (miri_top,   (140, 160, 120),     "Miri top"),
        (luma_chest, (80, 160, 200),      "Byte / Glitch height ref"),
    ]

    x_start = 30
    x_end   = IMG_W - 100

    for y, col, label in lines:
        x = x_start
        while x < x_end:
            draw.line([(x, y), (min(x + 8, x_end), y)], fill=col, width=1)
            x += 13
        draw.text((x_end + 4, y - 7), label, fill=col, font=font_small)


# ══════════════════════════════════════════════════════════════════════════════
# BYTE FLOAT-GAP DIMENSION ARROW (retained from v003)
# ══════════════════════════════════════════════════════════════════════════════

def draw_byte_float_dimension(draw, font_small):
    GROUNDFLOOR_COL = (100, 168, 200)

    byte_cx   = CHAR_X["byte"]
    s         = BYTE_H
    float_gap = int(s * 0.18)
    body_rx   = s // 2

    arrow_x = byte_cx + body_rx + 10
    top_y   = BASELINE_Y - float_gap
    bot_y   = BASELINE_Y

    if bot_y - top_y < 6:
        return

    draw.line([(arrow_x, top_y), (arrow_x, bot_y)], fill=GROUNDFLOOR_COL, width=2)

    tip_size = 5
    draw.polygon([(arrow_x, top_y),
                  (arrow_x - tip_size, top_y + tip_size * 2),
                  (arrow_x + tip_size, top_y + tip_size * 2)],
                 fill=GROUNDFLOOR_COL)
    draw.polygon([(arrow_x, bot_y),
                  (arrow_x - tip_size, bot_y - tip_size * 2),
                  (arrow_x + tip_size, bot_y - tip_size * 2)],
                 fill=GROUNDFLOOR_COL)

    serif_w = 7
    draw.line([(arrow_x - serif_w, top_y), (arrow_x + serif_w, top_y)],
              fill=GROUNDFLOOR_COL, width=2)
    draw.line([(arrow_x - serif_w, bot_y), (arrow_x + serif_w, bot_y)],
              fill=GROUNDFLOOR_COL, width=2)

    label   = "0.25 HU"
    label_x = arrow_x + serif_w + 4
    label_y = (top_y + bot_y) // 2 - 5
    draw.text((label_x, label_y), label, fill=GROUNDFLOOR_COL, font=font_small)

    gf_x0 = byte_cx - 70
    gf_x1 = byte_cx + 70
    gf_y  = BASELINE_Y
    x = gf_x0
    while x < gf_x1:
        draw.line([(x, gf_y), (min(x + 10, gf_x1), gf_y)],
                  fill=GROUNDFLOOR_COL, width=1)
        x += 14


# ══════════════════════════════════════════════════════════════════════════════
# MAIN GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

def generate_lineup(output_path):
    img  = Image.new('RGB', (IMG_W, IMG_H), BG)
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

    draw.rectangle([0, 0, IMG_W, IMG_H], fill=BG)

    title = "LUMA & THE GLITCHKIN — Full Cast Height Lineup — Cycle 24"
    draw.text((20, 14), title, fill=LABEL_COL, font=font_title)
    draw.line([(0, TITLE_H - 4), (IMG_W, TITLE_H - 4)], fill=TICK_COL, width=1)

    draw.line([(40, BASELINE_Y), (IMG_W - 20, BASELINE_Y)], fill=BASELINE_COL, width=2)

    draw_byte_float_dimension(draw, font_small)
    draw = ImageDraw.Draw(img)  # refresh after annotations

    draw_height_markers(draw, font_small)
    draw = ImageDraw.Draw(img)

    char_drawers = {
        "luma":   draw_luma_lineup,
        "byte":   draw_byte_lineup,
        "cosmo":  draw_cosmo_lineup,
        "miri":   draw_miri_lineup,
        "glitch": draw_glitch_lineup,
    }

    for char in CHAR_ORDER:
        cx = CHAR_X[char]
        h  = CHAR_HEIGHTS[char]
        char_drawers[char](draw, cx, BASELINE_Y, h)
        draw = ImageDraw.Draw(img)  # refresh after each character

    # Character name labels below baseline
    for char in CHAR_ORDER:
        cx    = CHAR_X[char]
        lines = CHAR_LABELS[char].split("\n")
        label_y = BASELINE_Y + 12
        for line in lines:
            lw = len(line) * 6
            draw.text((cx - lw // 2, label_y), line, fill=LABEL_COL, font=font_small)
            label_y += 14

    # Vertical height brackets for each character
    for char in CHAR_ORDER:
        cx    = CHAR_X[char] - 40
        h     = CHAR_HEIGHTS[char]
        top_y = BASELINE_Y - h
        if char in ("byte", "glitch"):
            s         = h
            float_gap = int(s * 0.18)
            body_ry   = int(s * 0.55)
            top_y     = BASELINE_Y - float_gap - body_ry * 2
        draw.line([(cx, top_y), (cx, BASELINE_Y)], fill=TICK_COL, width=1)
        draw.line([(cx - 4, top_y), (cx + 4, top_y)], fill=TICK_COL, width=1)
        draw.line([(cx - 4, BASELINE_Y), (cx + 4, BASELINE_Y)], fill=TICK_COL, width=1)
        draw.text((cx - 20, (top_y + BASELINE_Y)//2 - 5), f"{h}px", fill=TICK_COL, font=font_small)

    footer = (
        f"Full cast: Luma, Byte, Cosmo, Miri, Glitch. "
        f"Reference: 1 head unit = {HEAD_UNIT:.0f}px. "
        "Colors per master_palette.md (canonical). Cycle 24 — Glitch integrated."
    )
    draw.text((20, IMG_H - 18), footer, fill=TICK_COL, font=font_small)

    img.save(output_path)
    print(f"Saved: {output_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}px")


def main():
    import os
    out_dir = "/home/wipkat/team/output/characters/main"
    os.makedirs(out_dir, exist_ok=True)
    generate_lineup(os.path.join(out_dir, "LTG_CHAR_lineup_v004.png"))
    print("Character lineup v004 generation complete.")
    print("  Cast: Luma, Byte, Cosmo, Miri, Glitch (5 characters)")


if __name__ == '__main__':
    main()
