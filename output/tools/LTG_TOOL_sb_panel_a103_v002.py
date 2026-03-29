#!/usr/bin/env python3
"""
LTG_TOOL_sb_panel_a103_v002.py
Storyboard Panel A1-03 — DISCOVERY — Rebuilt per Critique Cycle 9
Lee Tanaka, Storyboard Artist

REBUILD NOTES (v002 vs v001):
- Camera: MCU / slightly low angle (child perspective, upward toward screen)
- Luma's face fills at LEAST 50% of frame width — this is the DISCOVERY MCU
- CRT screen is OFF-FRAME lower-left — its amber-green glow lights Luma's face
  asymmetrically: LEFT CHEEK lit warm-green (screen-side)
- Pixel shapes on screen: If showing screen edge (corner visible), blocky
  pixel forms at 40×40px minimum. Per brief: show Luma's wide eyes + lighting
  tells the discovery. One small corner of screen visible lower-left, but
  the FACE is the primary subject.
- Expression: CURIOUS → SURPRISED (transitional). One eye wider than the other.
  Mouth slightly open.
- Caption: "Discovery — she SEES them."

Shot: MCU / slightly low angle / child-perspective looking upward
Camera: screen is off-frame lower-left; glow visible ON Luma's face
Arc: DISCOVERY — first real contact. This is the moment the audience commits.
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_act1_panel_a103_v002.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H  # 540px scene area

# ── Palette ─────────────────────────────────────────────────────────────────
BG_DARK      = (24, 18, 12)     # very dark room — night / pre-dawn
BG_WALL      = (34, 26, 18)
FLOOR_DARK   = (28, 22, 14)

# Luma
LUMA_SKIN        = (242, 198, 152)
LUMA_SKIN_DARK   = (200, 155, 110)  # shadow side of face
LUMA_HAIR        = (52, 32, 18)
LUMA_HOODIE      = (72, 140, 185)
LUMA_OUTLINE     = (42, 22, 8)
LUMA_EYE_WHITE   = (245, 242, 235)
LUMA_EYE_IRIS    = (62, 40, 18)
LUMA_EYE_PUPIL   = (14, 8, 4)

# CRT glow (amber-green — the CRT screen off-frame lower-left)
CRT_AMBER_GREEN  = (160, 220, 90)   # amber-green screen glow
CRT_AMBER        = (230, 175, 60)   # warm amber component
CRT_GREEN        = (60, 210, 100)   # cool green component
SCREEN_GLOW_RGB  = (140, 210, 80)   # composite glow hitting face

# Screen corner (just visible, lower-left)
TV_BODY          = (48, 40, 30)
TV_BEZEL         = (60, 52, 40)
CRT_SCREEN_BASE  = (85, 100, 80)    # dark static base
CRT_STATIC_LIGHT = (120, 138, 110)
CRT_STATIC_DARK  = (55, 68, 50)

# Glitchkin pixel shapes (readable, 40×40 minimum)
PIXEL_CYAN       = (0, 240, 255)
PIXEL_BRIGHT     = (200, 255, 255)
PIXEL_MID        = (0, 185, 210)

# UI
BG_CAPTION  = (16, 12, 8)
TEXT_CAP    = (235, 228, 210)
ANN_COL     = (200, 175, 120)
ANN_DIM     = (150, 135, 100)
CALLOUT_L   = (220, 200, 140)
CALLOUT_TV  = (0, 200, 220)


def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def add_glow(img, cx, cy, r_max, color_rgb, steps=6, max_alpha=60):
    """ADD light via alpha_composite — never darkens."""
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_crt_corner(draw, img, rng):
    """
    Screen corner — lower-left of frame, partially visible.
    Just enough to anchor the glow source. Blocky Glitchkin pixel shapes visible.
    Two distinct Glitchkin pixel shapes at 40×40px minimum.
    """
    # Screen corner: positioned lower-left, partially cropped at frame edge
    corner_x = -30    # extends off left edge
    corner_y = int(DRAW_H * 0.55)
    screen_w  = 220
    screen_h  = 160

    # TV body behind screen
    draw.rectangle([corner_x, corner_y - 18,
                    corner_x + screen_w + 25, corner_y + screen_h + 22],
                   fill=TV_BODY, outline=TV_BEZEL, width=3)

    # Screen area
    sx = corner_x + 14
    sy = corner_y
    sw = screen_w
    sh = screen_h

    # Screen background — CRT glow (bright, active)
    draw.rectangle([sx, sy, sx + sw, sy + sh], fill=(70, 90, 65))

    # CRT static texture
    for _ in range(180):
        px = rng.randint(sx, sx + sw - 1)
        py = rng.randint(sy, sy + sh - 1)
        lum = rng.randint(40, 140)
        draw.rectangle([px, py, px + 1, py + 1], fill=(lum // 2, lum, lum // 3))

    # Scan lines
    for scan_y in range(sy, sy + sh, 5):
        draw.line([sx, scan_y, sx + sw, scan_y], fill=(50, 65, 44), width=1)

    # ── GLITCHKIN PIXEL SHAPES — READABLE (40×40px minimum) ─────────────────
    # Shape 1: upper-right area of visible screen — irregular blocky form
    # Glitchkin A — 48×44px bounding box
    ga_x = sx + sw - 80   # right side of screen
    ga_y = sy + 18

    # Multi-block pixel character — irregular polygon via blocks
    # Body blocks (assembled from rectangles = pixel art character)
    ga_blocks = [
        # Head area
        (ga_x + 12, ga_y,      ga_x + 36, ga_y + 10),   # head top
        (ga_x + 8,  ga_y + 10, ga_x + 40, ga_y + 22),   # head wide
        (ga_x + 10, ga_y + 22, ga_x + 38, ga_y + 32),   # shoulders
        # Body
        (ga_x + 14, ga_y + 32, ga_x + 34, ga_y + 44),   # torso
        # Arm extensions
        (ga_x + 2,  ga_y + 24, ga_x + 14, ga_y + 34),   # left arm
        (ga_x + 34, ga_y + 24, ga_x + 46, ga_y + 34),   # right arm
        # Leg extensions
        (ga_x + 12, ga_y + 44, ga_x + 22, ga_y + 56),   # left leg
        (ga_x + 26, ga_y + 44, ga_x + 36, ga_y + 56),   # right leg
    ]
    for bx0, by0, bx1, by1 in ga_blocks:
        draw.rectangle([bx0, by0, bx1, by1], fill=PIXEL_CYAN)
    # Bright core pixels
    for bx0, by0, bx1, by1 in ga_blocks[1:3]:
        draw.rectangle([bx0 + 2, by0 + 2, bx1 - 2, by1 - 2], fill=PIXEL_BRIGHT)
    # Bounding box annotation line
    draw.rectangle([ga_x, ga_y, ga_x + 48, ga_y + 58], outline=(0, 180, 200), width=1)

    # Shape 2: lower-left of screen — different shape, smaller
    gb_x = sx + 20
    gb_y = sy + sh - 70

    gb_blocks = [
        (gb_x + 10, gb_y,      gb_x + 30, gb_y + 12),   # head
        (gb_x + 6,  gb_y + 12, gb_x + 34, gb_y + 24),   # upper body
        (gb_x + 8,  gb_y + 24, gb_x + 30, gb_y + 40),   # lower body
        # short stubby legs
        (gb_x + 8,  gb_y + 40, gb_x + 18, gb_y + 50),
        (gb_x + 22, gb_y + 40, gb_x + 30, gb_y + 50),
    ]
    for bx0, by0, bx1, by1 in gb_blocks:
        draw.rectangle([bx0, by0, bx1, by1], fill=PIXEL_MID)
    draw.rectangle([gb_x + 6, gb_y + 12, gb_x + 34, gb_y + 24],
                   fill=PIXEL_CYAN)
    draw.rectangle([gb_x, gb_y, gb_x + 40, gb_y + 52], outline=(0, 180, 200), width=1)

    # Glow from screen (strong — this is the light source)
    screen_cx = sx + sw // 2
    screen_cy = sy + sh // 2
    add_glow(img, screen_cx, screen_cy, 180, CRT_AMBER_GREEN, steps=8, max_alpha=55)
    add_glow(img, screen_cx, screen_cy, 120, CRT_GREEN, steps=5, max_alpha=35)

    # Pixel shape glow
    add_glow(img, ga_x + 24, ga_y + 28, 35, PIXEL_CYAN, steps=4, max_alpha=60)
    add_glow(img, gb_x + 20, gb_y + 25, 28, PIXEL_CYAN, steps=3, max_alpha=45)

    return draw


def draw_luma_mcu(draw, img):
    """
    Luma — MCU / slightly low angle (camera is at child-height, looking upward).
    Face fills at least 50% of frame width (400px at 800px wide).
    Camera is BELOW Luma's eyeline — low angle = we look UP at her face.
    CRT screen is OFF-FRAME lower-left — glow hits LEFT CHEEK (warm-green asymmetric).
    Expression: CURIOUS → SURPRISED (transitional)
      - One eye wider than the other (left eye wider — screen-side)
      - Mouth slightly open
    """
    # MCU: face is the dominant element — fills the RIGHT 60% of the frame
    # Left side has screen corner and glow; right side is Luma's face close-up
    face_cx = int(PW * 0.60)     # center of face — shifted right
    face_cy = int(DRAW_H * 0.38) # upper portion (slightly below top) — low angle

    head_w = 290   # wide MCU — face fills > 50% of 800px frame
    head_h = 260

    # ── Background behind face ────────────────────────────────────────────────
    # Wall — very dark, with CRT glow spilling from lower-left
    draw.rectangle([0, 0, PW, DRAW_H], fill=BG_DARK)
    # Floor line (low angle camera shows floor, slight upward perspective)
    floor_y = int(DRAW_H * 0.80)
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=FLOOR_DARK)
    draw.line([0, floor_y, PW, floor_y], fill=(38, 30, 20), width=2)

    # CRT glow from lower-left corner (dominant light source)
    add_glow(img, 0, DRAW_H, 500, CRT_AMBER_GREEN, steps=9, max_alpha=48)
    add_glow(img, 0, DRAW_H, 320, CRT_AMBER, steps=6, max_alpha=38)
    add_glow(img, 60, DRAW_H - 30, 250, CRT_GREEN, steps=5, max_alpha=28)
    draw = ImageDraw.Draw(img)

    # ── Neck + body (cropped MCU — lower body below frame) ───────────────────
    neck_cx = face_cx
    neck_top = face_cy + head_h // 2 - 15
    neck_w   = 80
    draw.rectangle([neck_cx - neck_w // 2, neck_top,
                    neck_cx + neck_w // 2, DRAW_H + 40],
                   fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=1)

    # Hoodie shoulders/body (cropped at bottom of frame — true MCU)
    shoulder_w = head_w + 60
    draw.ellipse([neck_cx - shoulder_w // 2, neck_top + 20,
                  neck_cx + shoulder_w // 2, neck_top + 140],
                 fill=LUMA_HOODIE, outline=LUMA_OUTLINE, width=2)
    # Collar / hoodie body fills frame bottom
    draw.rectangle([neck_cx - shoulder_w // 2, neck_top + 50,
                    neck_cx + shoulder_w // 2, DRAW_H + 20],
                   fill=LUMA_HOODIE, outline=LUMA_OUTLINE, width=2)

    # ── Hair ─────────────────────────────────────────────────────────────────
    # Hair crown (above face) — low angle = we see top of head
    draw.ellipse([face_cx - head_w // 2 - 22, face_cy - head_h // 2 - 30,
                  face_cx + head_w // 2 + 22, face_cy + head_h // 2 - 60],
                 fill=LUMA_HAIR)
    # Hair volume at sides
    draw.ellipse([face_cx - head_w // 2 - 28, face_cy - head_h // 4,
                  face_cx - head_w // 2 + 20, face_cy + head_h // 4],
                 fill=LUMA_HAIR)
    draw.ellipse([face_cx + head_w // 2 - 20, face_cy - head_h // 4,
                  face_cx + head_w // 2 + 28, face_cy + head_h // 4],
                 fill=LUMA_HAIR)
    # Side hair strands
    for dy in range(-60, 80, 18):
        draw.ellipse([face_cx - head_w // 2 - 18, face_cy + dy,
                      face_cx - head_w // 2 + 8, face_cy + dy + 14],
                     fill=LUMA_HAIR)

    # ── Face ─────────────────────────────────────────────────────────────────
    # Shadow side (right side — away from CRT glow)
    draw.ellipse([face_cx - head_w // 2, face_cy - head_h // 2,
                  face_cx + head_w // 2, face_cy + head_h // 2],
                 fill=LUMA_SKIN_DARK, outline=LUMA_OUTLINE, width=2)
    # Lit side (LEFT side — facing screen glow) with warm-green tint
    draw.ellipse([face_cx - head_w // 2, face_cy - head_h // 2,
                  face_cx + 15, face_cy + head_h // 2],
                 fill=LUMA_SKIN)

    # ── CRT glow on LEFT CHEEK (screen side) — asymmetric lighting ───────────
    glow_layer = Image.new('RGBA', (PW, DRAW_H), (0, 0, 0, 0))
    gl = ImageDraw.Draw(glow_layer)

    # Warm-green catch light on LEFT cheek (toward screen lower-left)
    cheek_cx = face_cx - head_w // 4    # left cheek center
    cheek_cy = face_cy + 30
    for r in [110, 80, 55, 35]:
        alpha = max(10, 42 - r // 3)
        gl.ellipse([cheek_cx - r, cheek_cy - r,
                    cheek_cx + r, cheek_cy + r],
                   fill=(*CRT_AMBER_GREEN, alpha))
    # Amber component on left brow
    brow_glow_cx = face_cx - head_w // 3
    brow_glow_cy = face_cy - head_h // 5
    for r in [70, 48]:
        alpha = max(8, 28 - r // 4)
        gl.ellipse([brow_glow_cx - r, brow_glow_cy - r,
                    brow_glow_cx + r, brow_glow_cy + r],
                   fill=(*CRT_AMBER, alpha))

    base       = img.convert('RGBA')
    panel_crop = base.crop((0, 0, PW, DRAW_H))
    merged     = Image.alpha_composite(panel_crop.convert('RGBA'), glow_layer)
    img.paste(merged.convert('RGB'), (0, 0))
    draw = ImageDraw.Draw(img)

    # ── Eyes — transitional CURIOUS → SURPRISED ──────────────────────────────
    # Left eye (CRT-facing side): WIDER — the surprising side
    # Right eye: slightly less wide — asymmetric = transitional state
    eye_y     = face_cy - head_h // 8
    left_ex   = face_cx - int(head_w * 0.22)
    right_ex  = face_cx + int(head_w * 0.22)

    # LEFT EYE — wider (screen side, sees the Glitchkin first)
    lew  = 70   # eye width
    leh  = 55   # eye height (taller = more surprised)
    draw.ellipse([left_ex - lew // 2, eye_y - leh // 2,
                  left_ex + lew // 2, eye_y + leh // 2],
                 fill=LUMA_EYE_WHITE, outline=LUMA_OUTLINE, width=2)
    draw.ellipse([left_ex - 18, eye_y - 18, left_ex + 18, eye_y + 18],
                 fill=LUMA_EYE_IRIS)
    draw.ellipse([left_ex - 11, eye_y - 11, left_ex + 11, eye_y + 11],
                 fill=LUMA_EYE_PUPIL)
    # CRT catch-light in left eye (amber-green from screen)
    draw.ellipse([left_ex - 8, eye_y - 8, left_ex - 2, eye_y - 2],
                 fill=(160, 240, 80))
    # Specular highlight
    draw.ellipse([left_ex + 4, eye_y - 7, left_ex + 8, eye_y - 3],
                 fill=(255, 255, 240))

    # RIGHT EYE — slightly less open (curious, not yet fully surprised)
    rew  = 60
    reh  = 44
    draw.ellipse([right_ex - rew // 2, eye_y - reh // 2,
                  right_ex + rew // 2, eye_y + reh // 2],
                 fill=LUMA_EYE_WHITE, outline=LUMA_OUTLINE, width=2)
    draw.ellipse([right_ex - 14, eye_y - 14, right_ex + 14, eye_y + 14],
                 fill=LUMA_EYE_IRIS)
    draw.ellipse([right_ex - 9, eye_y - 9, right_ex + 9, eye_y + 9],
                 fill=LUMA_EYE_PUPIL)
    # Specular highlight
    draw.ellipse([right_ex + 3, eye_y - 6, right_ex + 7, eye_y - 2],
                 fill=(255, 255, 240))

    # ── Brows — raised (both), left higher than right ─────────────────────────
    brow_y = eye_y - leh // 2 - 14
    # Left brow — higher arc (more surprised)
    draw.arc([left_ex - lew // 2, brow_y - 14,
              left_ex + lew // 2, brow_y + 8],
             start=200, end=340, fill=LUMA_HAIR, width=3)
    # Right brow — slightly lower (still raised but less)
    draw.arc([right_ex - rew // 2, brow_y - 8,
              right_ex + rew // 2, brow_y + 8],
             start=200, end=340, fill=LUMA_HAIR, width=3)

    # ── Nose (frontal MCU — straight-on) ─────────────────────────────────────
    nose_tip_y = face_cy + 22
    nose_cx    = face_cx - 8   # slight 3/4 turn toward screen
    draw.line([nose_cx + 10, eye_y + 28, nose_cx + 8, nose_tip_y - 6],
              fill=(170, 120, 75), width=2)
    draw.arc([nose_cx - 12, nose_tip_y - 10,
              nose_cx + 6, nose_tip_y + 4],
             start=30, end=200, fill=LUMA_OUTLINE, width=2)
    draw.arc([nose_cx + 6, nose_tip_y - 10,
              nose_cx + 24, nose_tip_y + 4],
             start=340, end=150, fill=LUMA_OUTLINE, width=2)

    # ── Mouth — slightly open (surprise beginning) ────────────────────────────
    mouth_y   = face_cy + head_h // 4 + 5
    mouth_w   = 55
    # Lower lip opening — O-shape, small
    draw.arc([nose_cx - mouth_w // 2, mouth_y - 6,
              nose_cx + mouth_w // 2, mouth_y + 18],
             start=0, end=180, fill=LUMA_OUTLINE, width=3)
    # Upper lip
    draw.arc([nose_cx - mouth_w // 2 + 8, mouth_y - 14,
              nose_cx + mouth_w // 2 - 8, mouth_y + 2],
             start=200, end=340, fill=(165, 110, 75), width=2)
    # Inner dark (mouth open)
    draw.ellipse([nose_cx - 10, mouth_y - 2,
                  nose_cx + 10, mouth_y + 12],
                 fill=(38, 22, 14))

    return draw


def make_panel():
    font_cap = load_font(12)
    font_ann = load_font(11)
    font_b   = load_font(12, bold=True)
    rng      = random.Random(103)

    img  = Image.new('RGB', (PW, PH), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Draw Luma MCU first (she fills the frame — background is drawn inside)
    draw = draw_luma_mcu(draw, img)
    draw = ImageDraw.Draw(img)

    # Draw CRT screen corner (lower-left, partially off-frame)
    draw = draw_crt_corner(draw, img, rng)
    draw = ImageDraw.Draw(img)

    # ── Annotations ──────────────────────────────────────────────────────────
    draw.text((8, 8),
              "A1-03  /  MCU  /  low angle (child POV, upward)  /  Luma face dominant",
              font=font_ann, fill=ANN_COL)
    draw.text((8, 20),
              "Discovery — she SEES them  |  CRT off-frame lower-left",
              font=font_ann, fill=ANN_DIM)

    # Expression callout (right side — unobstructed area)
    cx_label = int(PW * 0.70)
    draw.text((cx_label, int(DRAW_H * 0.06)), "LUMA — MCU",
              font=font_ann, fill=CALLOUT_L)
    draw.text((cx_label, int(DRAW_H * 0.06) + 12), "CURIOUS → SURPRISED",
              font=font_ann, fill=(220, 200, 100))
    draw.text((cx_label, int(DRAW_H * 0.06) + 24), "left eye WIDER",
              font=font_ann, fill=ANN_DIM)
    draw.text((cx_label, int(DRAW_H * 0.06) + 36), "mouth slightly open",
              font=font_ann, fill=ANN_DIM)

    # CRT glow callout
    draw.text((10, int(DRAW_H * 0.72)), "CRT GLOW — off-frame lower-left",
              font=font_ann, fill=(160, 220, 80))
    draw.text((10, int(DRAW_H * 0.72) + 12), "amber-green hits LEFT cheek",
              font=font_ann, fill=(120, 190, 70))
    draw.text((10, int(DRAW_H * 0.72) + 24), "asymmetric warm-green lighting",
              font=font_ann, fill=ANN_DIM)

    # Pixel shape callout
    draw.text((10, int(DRAW_H * 0.50)), "GLITCHKIN",
              font=font_ann, fill=CALLOUT_TV)
    draw.text((10, int(DRAW_H * 0.50) + 12), "pixel shapes visible",
              font=font_ann, fill=(0, 200, 220))
    draw.text((10, int(DRAW_H * 0.50) + 24), "40×40px+ blocks",
              font=font_ann, fill=(0, 180, 200))

    # Eye asymmetry annotation
    draw.text((int(PW * 0.38), int(DRAW_H * 0.50)), "← wider",
              font=font_ann, fill=(220, 200, 120))
    draw.text((int(PW * 0.62), int(DRAW_H * 0.50)), "narrower",
              font=font_ann, fill=(160, 150, 100))

    # Low angle annotation arrow
    draw.text((int(PW * 0.70), DRAW_H - 32), "low angle = camera BELOW eyeline",
              font=font_ann, fill=ANN_DIM)
    draw.text((int(PW * 0.70), DRAW_H - 20), "audience looks UP at Luma",
              font=font_ann, fill=ANN_DIM)

    # DISCOVERY label badge
    draw.rectangle([8, DRAW_H - 22, 112, DRAW_H - 5], fill=(18, 14, 8))
    draw.text((12, DRAW_H - 20), "DISCOVERY", font=font_b, fill=(0, 240, 255))

    # ── Caption bar ──────────────────────────────────────────────────────────
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(14, 10, 6), width=2)
    draw.text((10, DRAW_H + 5),
              "A1-03  MCU / low angle  —  Luma's face fills 50%+ of frame  —  CRT screen off-frame lower-left",
              font=font_cap, fill=(160, 155, 130))
    draw.text((10, DRAW_H + 20),
              "Discovery — she SEES them.  Left cheek lit warm-green (CRT glow).  Left eye wider.  Mouth open.",
              font=font_cap, fill=TEXT_CAP)
    draw.text((10, DRAW_H + 36),
              "CURIOUS → SURPRISED transitional.  Glitchkin pixel shapes 40×40px in screen corner lower-left.",
              font=font_ann, fill=(150, 140, 110))
    draw.text((PW - 260, DRAW_H + 46), "LTG_SB_act1_panel_a103_v002  |  Cycle 19",
              font=font_ann, fill=(100, 95, 78))

    draw.rectangle([0, 0, PW - 1, PH - 1], outline=(14, 10, 6), width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("A1-03 v002 panel generation complete (Cycle 19).")
