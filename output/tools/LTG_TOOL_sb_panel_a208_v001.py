#!/usr/bin/env python3
"""
LTG_TOOL_sb_panel_a208_v001.py
Storyboard Panel A2-08 — Grandma Miri Returns — Cycle 17
Lee Tanaka, Storyboard Artist

Beat: Emotional climax of Act 2. Grandma Miri enters to find Luma and
the Glitchkin. Her reaction is the emotional pivot: she isn't afraid.
She *recognizes* them.

Expression: SURPRISED → KNOWING
  Not fear — gentle wonder + recognition.
  CRT glow catches on her face (warm amber-green).
  She belongs here.

Camera: ECU / low angle (looking up slightly at Miri)
  Low angle = camera slightly below her eyeline = she feels momentarily
  larger than life. Her face fills the upper 2/3 of the frame.
  CRT glow from off-frame lower-left (the TV in the room below her gaze).

Expression callouts:
  - Eyes: wide — initial surprise, but no fear (brows high but not scrunched)
  - One corner of mouth beginning to lift = recognition surfacing
  - Cheek crinkles = warmth, not alarm
  - CRT warm glow: amber-green catch light on face

Output:
  /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_act2_panel_a208_v001.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

ACT2_PANELS_DIR = "/home/wipkat/team/output/storyboards/act2/panels"
PANELS_DIR      = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH     = os.path.join(ACT2_PANELS_DIR, "LTG_SB_act2_panel_a208_v001.png")

os.makedirs(ACT2_PANELS_DIR, exist_ok=True)
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H   # 540px scene area

# ── Palette ──────────────────────────────────────────────────────────────────
BG_CAPTION   = (22, 18, 14)
TEXT_CAPTION = (235, 228, 210)
BORDER_COL   = (18, 12, 8)

# Grandma Miri (warm older woman — softer skin tones)
MIRI_SKIN       = (215, 165, 120)   # warm medium skin
MIRI_SKIN_LIGHT = (232, 185, 140)   # cheek highlight
MIRI_HAIR       = (195, 185, 175)   # grey-silver hair
MIRI_HAIR_DARK  = (150, 142, 135)
MIRI_SWEATER    = (160, 100, 60)    # warm terracotta/rust sweater
MIRI_OUTLINE    = (80, 48, 24)

# CRT glow colors (amber-green — the signature glow of this show)
CRT_AMBER    = (230, 180, 80)
CRT_GREEN    = (80, 200, 120)
CRT_MIX      = (180, 200, 100)     # amber-green blend
CRT_WARM     = (240, 195, 90)

# Background (dim room, doorway glow)
BG_DARK      = (28, 22, 18)        # dark room bg
BG_DOORWAY   = (65, 55, 40)        # warm hallway behind her
BG_WALL      = (42, 34, 25)        # dark room wall

STATIC_WHITE = (240, 240, 240)
ANN_COL      = (220, 200, 130)
ANN_DIM      = (160, 145, 95)
CALLOUT_MIRI = (200, 220, 160)


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


def draw_background(draw, img):
    """
    Background: dark room (night/dim) with CRT glow from below-left.
    Doorway light behind Miri creates rim light on hair.
    ECU — background is mostly dark with glow gradients.
    Low angle camera: looking slightly up at Miri.
    """
    # Base dark room
    draw.rectangle([0, 0, PW, DRAW_H], fill=BG_DARK)

    # Subtle wall texture (very dark)
    rng = random.Random(2208)
    for _ in range(8):
        rx = rng.randint(0, PW)
        ry = rng.randint(0, DRAW_H)
        rw = rng.randint(40, 120)
        rh = rng.randint(2, 5)
        draw.rectangle([rx, ry, rx + rw, ry + rh], fill=(32, 26, 20))

    # Doorway rim light behind Miri (warm amber from hallway)
    # Creates a backlight halo — she enters from hallway light
    add_glow(img, PW // 2, DRAW_H // 2 + 50, 240, (190, 150, 80), steps=6, max_alpha=30)

    # CRT glow source: OFF-FRAME LOWER-LEFT
    # This is the CRT TV glow catching on Miri's face
    # Strong amber-green from lower left corner
    add_glow(img, -30, DRAW_H - 40, 340, (180, 200, 80), steps=7, max_alpha=42)
    add_glow(img, 0, DRAW_H, 280, (230, 180, 60), steps=6, max_alpha=35)

    # Secondary green pulse (Glitchkin presence)
    add_glow(img, 60, DRAW_H - 20, 200, (60, 220, 120), steps=5, max_alpha=22)


def draw_miri_face(draw, img):
    """
    Grandma Miri — ECU on face.
    Low angle: camera slightly below eyeline — her face fills upper 2/3 of frame.
    Face is large, centered slightly above center.

    SURPRISED → KNOWING expression:
    - Eyes: wide, not scrunched — wonder, not alarm
    - Brows: raised high (surprise), but soft curve (not pinched/angry)
    - One corner of mouth lifting = recognition emerging
    - Cheek crinkles = warmth, earned by years
    - CRT glow catches on cheek and brow (amber-green)
    """
    # Face positioning — ECU, fills frame
    face_cx = PW // 2
    face_cy = int(DRAW_H * 0.42)   # slightly above center (low angle = face up)

    head_w  = 340   # wide ECU — face near full frame width
    head_h  = 300

    # ── Neck and shoulder (low-angle ECU — partial bottom of frame) ─────
    # Just shoulders/neck base visible at bottom
    neck_w = 90
    neck_h = 60
    neck_y = face_cy + head_h // 2 - 10
    draw.rectangle([face_cx - neck_w // 2, neck_y,
                    face_cx + neck_w // 2, neck_y + neck_h + 20],
                   fill=MIRI_SKIN, outline=MIRI_OUTLINE, width=1)

    # Sweater collar (just top visible)
    draw.ellipse([face_cx - neck_w - 30, neck_y + 30,
                  face_cx + neck_w + 30, neck_y + neck_h + 50],
                 fill=MIRI_SWEATER, outline=(100, 60, 35), width=2)

    # ── Main face oval ───────────────────────────────────────────────────
    draw.ellipse([face_cx - head_w // 2, face_cy - head_h // 2,
                  face_cx + head_w // 2, face_cy + head_h // 2],
                 fill=MIRI_SKIN, outline=MIRI_OUTLINE, width=2)

    # Cheek highlight (CRT glow catching left cheek = CRT light from lower-left)
    glow_layer = Image.new('RGBA', (PW, DRAW_H), (0, 0, 0, 0))
    gl = ImageDraw.Draw(glow_layer)
    # Left cheek catch light (amber-green from CRT)
    for r in [80, 60, 42]:
        alpha = max(8, 32 - r // 3)
        gl.ellipse([face_cx - head_w // 2 + 30 - r,
                    face_cy + 20 - r,
                    face_cx - head_w // 2 + 30 + r,
                    face_cy + 20 + r],
                   fill=(*CRT_AMBER, alpha))
    # Brow/forehead catch
    for r in [70, 50]:
        alpha = max(6, 22 - r // 4)
        gl.ellipse([face_cx - head_w // 3 - r, face_cy - head_h // 4 - r,
                    face_cx - head_w // 3 + r, face_cy - head_h // 4 + r],
                   fill=(*CRT_GREEN, alpha))
    base = img.convert('RGBA')
    panel_area = base.crop((0, 0, PW, DRAW_H))
    merged = Image.alpha_composite(panel_area.convert('RGBA'), glow_layer)
    img.paste(merged.convert('RGB'), (0, 0))
    draw = ImageDraw.Draw(img)

    # ── Hair — grey/silver, slightly messy (just woke up or mid-activity) ─
    # Hair framing face — bun-ish at top, wisps
    hair_pts_left = [
        (face_cx - head_w // 2 - 10, face_cy - 20),
        (face_cx - head_w // 2 + 20, face_cy - head_h // 2 - 8),
        (face_cx - head_w // 4, face_cy - head_h // 2 - 18),
        (face_cx, face_cy - head_h // 2 - 22),
    ]
    hair_pts_right = [
        (face_cx, face_cy - head_h // 2 - 22),
        (face_cx + head_w // 4, face_cy - head_h // 2 - 16),
        (face_cx + head_w // 2 - 18, face_cy - head_h // 2 - 6),
        (face_cx + head_w // 2 + 8, face_cy - 15),
    ]
    # Draw hair volume above face
    draw.ellipse([face_cx - head_w // 2 - 10, face_cy - head_h // 2 - 30,
                  face_cx + head_w // 2 + 10, face_cy - head_h // 2 + 40],
                 fill=MIRI_HAIR)
    draw.ellipse([face_cx - head_w // 2 + 5, face_cy - head_h // 2 - 28,
                  face_cx + head_w // 2 - 5, face_cy - head_h // 2 + 30],
                 fill=MIRI_HAIR_DARK)

    # Hair sides (frame the face — ECU shows hair at both sides)
    # Left side hair
    draw.ellipse([face_cx - head_w // 2 - 12, face_cy - head_h // 4,
                  face_cx - head_w // 2 + 30, face_cy + head_h // 4],
                 fill=MIRI_HAIR)
    # Right side
    draw.ellipse([face_cx + head_w // 2 - 30, face_cy - head_h // 4,
                  face_cx + head_w // 2 + 12, face_cy + head_h // 4],
                 fill=MIRI_HAIR)

    # ── Facial feature detail lines (age — earned warmth) ─────────────────
    # Laugh/smile lines at cheek corners
    # Left side (her right, CRT-lit side)
    for offset_y in [0, 5]:
        draw.arc([face_cx - head_w // 4 - 8, face_cy + 20 + offset_y,
                  face_cx - head_w // 4 + 18, face_cy + 50 + offset_y],
                 start=220, end=320, fill=MIRI_OUTLINE, width=1)
    # Right side
    for offset_y in [0, 5]:
        draw.arc([face_cx + head_w // 4 - 18, face_cy + 20 + offset_y,
                  face_cx + head_w // 4 + 8, face_cy + 50 + offset_y],
                 start=220, end=320, fill=MIRI_OUTLINE, width=1)

    # Forehead lines (just two, subtle — not exaggerated)
    for ly in [face_cy - head_h // 3 + 5, face_cy - head_h // 3 + 14]:
        draw.arc([face_cx - head_w // 3, ly, face_cx + head_w // 3, ly + 10],
                 start=200, end=340, fill=(170, 120, 80), width=1)

    # ── EYES — SURPRISED/KNOWING ─────────────────────────────────────────
    # Wide, not scrunched. Full aperture. No fear lines at corners.
    eye_y    = face_cy - 20
    eye_sep  = 75   # distance from center to eye center
    eye_w    = 58
    eye_h    = 46

    for side, ex_off in enumerate([-eye_sep, eye_sep]):
        ex = face_cx + ex_off

        # Sclera (wide open — surprised state)
        draw.ellipse([ex - eye_w // 2, eye_y - eye_h // 2,
                      ex + eye_w // 2, eye_y + eye_h // 2],
                     fill=STATIC_WHITE, outline=MIRI_OUTLINE, width=2)

        # Iris (warm brown — grandmotherly)
        iris_r = 16
        draw.ellipse([ex - iris_r, eye_y - iris_r, ex + iris_r, eye_y + iris_r],
                     fill=(110, 75, 42))

        # Pupil (dilated slightly — dim room + surprise)
        pup_r = 10
        draw.ellipse([ex - pup_r, eye_y - pup_r, ex + pup_r, eye_y + pup_r],
                     fill=(20, 12, 8))

        # CRT glow catch-light in pupil (amber from lower-left)
        # Left eye gets more glow (facing the CRT source)
        glow_offset = 6 if side == 0 else 4
        draw.ellipse([ex - pup_r + glow_offset, eye_y - pup_r + 3,
                      ex - pup_r + glow_offset + 5, eye_y - pup_r + 8],
                     fill=CRT_AMBER)
        # Secondary green highlight
        draw.rectangle([ex + pup_r - 5, eye_y - pup_r + 2,
                        ex + pup_r - 2, eye_y - pup_r + 5],
                       fill=CRT_GREEN)

        # Lower eyelid crinkle (cheek-smile crinkle beginning = recognition)
        draw.arc([ex - eye_w // 2 + 5, eye_y + eye_h // 4,
                  ex + eye_w // 2 - 5, eye_y + eye_h // 2 + 6],
                 start=10, end=170, fill=MIRI_OUTLINE, width=1)

    # ── BROWS — HIGH, SOFT ARC (surprised but not alarmed) ───────────────
    brow_y = eye_y - eye_h // 2 - 14
    for side, ex_off in enumerate([-eye_sep, eye_sep]):
        ex = face_cx + ex_off
        # Soft arc — raised high, but rounded (wonder vs fear = arc not spike)
        draw.arc([ex - eye_w // 2, brow_y - 10,
                  ex + eye_w // 2, brow_y + 14],
                 start=200, end=340, fill=MIRI_HAIR_DARK, width=3)
        # Brow hair texture (ECU = visible hair strokes)
        for hx in range(ex - eye_w // 2 + 5, ex + eye_w // 2 - 5, 7):
            angle_y = brow_y - int(10 * math.sin(math.pi * (hx - (ex - eye_w // 2)) / eye_w))
            draw.line([hx, angle_y + 2, hx + 3, angle_y - 2],
                      fill=MIRI_HAIR_DARK, width=1)

    # ── NOSE (ECU — subtle construction lines, not full detail) ──────────
    nose_x = face_cx
    nose_tip_y = eye_y + 50
    # Bridge shadow
    draw.line([face_cx - 5, eye_y + 15, face_cx - 8, nose_tip_y - 5],
              fill=(170, 115, 75), width=2)
    # Nostril flare (slight — CRT shadow on left)
    draw.arc([nose_x - 22, nose_tip_y - 12, nose_x - 2, nose_tip_y + 4],
             start=30, end=200, fill=MIRI_OUTLINE, width=2)
    draw.arc([nose_x + 2, nose_tip_y - 12, nose_x + 22, nose_tip_y + 4],
             start=340, end=150, fill=MIRI_OUTLINE, width=2)
    # Tip
    draw.ellipse([nose_x - 8, nose_tip_y - 6, nose_x + 8, nose_tip_y + 6],
                 fill=MIRI_SKIN_LIGHT)

    # ── MOUTH — SURPRISED → KNOWING beginning ────────────────────────────
    # One corner beginning to lift (right corner = recognition surfacing)
    mouth_y   = face_cy + 68
    mouth_half = 48

    # Base mouth line (slight open — surprise, lips parted)
    draw.arc([face_cx - mouth_half, mouth_y - 8,
              face_cx + mouth_half, mouth_y + 12],
             start=5, end=175, fill=MIRI_OUTLINE, width=3)

    # Right corner lift (her left, viewer's right — recognition)
    # Slight upward curve at one corner = the "knowing" beginning to surface
    draw.arc([face_cx + mouth_half - 20, mouth_y - 16,
              face_cx + mouth_half + 10, mouth_y + 4],
             start=260, end=360, fill=MIRI_OUTLINE, width=2)

    # Upper lip line (ECU — visible)
    draw.arc([face_cx - mouth_half + 8, mouth_y - 16,
              face_cx + mouth_half - 8, mouth_y],
             start=200, end=340, fill=(160, 105, 70), width=2)

    # Lips (ECU means visible color)
    # Lower lip
    draw.arc([face_cx - mouth_half + 12, mouth_y - 2,
              face_cx + mouth_half - 12, mouth_y + 18],
             start=0, end=180, fill=(185, 120, 85), width=2)

    # ── Nasolabial fold (smile lines from nose to mouth) ─────────────────
    # Very light — earned, not exaggerated
    draw.arc([face_cx - 40, nose_tip_y,
              face_cx - 12, mouth_y + 5],
             start=240, end=330, fill=(170, 115, 78), width=1)
    draw.arc([face_cx + 12, nose_tip_y,
              face_cx + 40, mouth_y + 5],
             start=210, end=300, fill=(170, 115, 78), width=1)

    return draw


def draw_annotations(draw, font_ann):
    """Shot type, expression, and CRT glow callouts."""
    # Shot type
    draw.text((10, 8), "ECU  /  low angle (looking slightly up)  /  neutral",
              font=font_ann, fill=ANN_COL)

    # Grandma Miri expression callout — right side
    draw.text((PW - 260, int(DRAW_H * 0.18)), "GRANDMA MIRI",
              font=font_ann, fill=CALLOUT_MIRI)
    draw.text((PW - 260, int(DRAW_H * 0.18) + 10), "SURPRISED → KNOWING",
              font=font_ann, fill=(200, 220, 160))
    draw.text((PW - 260, int(DRAW_H * 0.18) + 20), "not fear — recognition",
              font=font_ann, fill=(160, 185, 130))

    # Eye callout — left side
    draw.text((10, int(DRAW_H * 0.26)), "eyes: wide / wonder",
              font=font_ann, fill=(200, 200, 160))
    draw.text((10, int(DRAW_H * 0.26) + 10), "no fear lines",
              font=font_ann, fill=(160, 160, 125))

    # CRT glow callout (lower left)
    draw.text((10, DRAW_H - 32), "CRT glow — off-frame lower-left",
              font=font_ann, fill=(200, 195, 110))
    draw.text((10, DRAW_H - 20), "amber-green catch on cheek + brow",
              font=font_ann, fill=(180, 200, 100))

    # Mouth callout
    draw.text((PW - 230, int(DRAW_H * 0.72)), "mouth: one corner rising",
              font=font_ann, fill=(210, 170, 110))
    draw.text((PW - 230, int(DRAW_H * 0.72) + 10), "= KNOWING beginning",
              font=font_ann, fill=(190, 160, 100))

    # Low angle note
    draw.text((PW - 190, 8), "low angle = larger than life",
              font=font_ann, fill=ANN_DIM)
    draw.text((PW - 190, 18), "she belongs here",
              font=font_ann, fill=ANN_DIM)


def make_panel():
    font      = load_font(14)
    font_bold = load_font(14, bold=True)
    font_cap  = load_font(12)
    font_ann  = load_font(11)

    img  = Image.new('RGB', (PW, PH), BG_DARK)
    draw = ImageDraw.Draw(img)

    draw_background(draw, img)
    draw = ImageDraw.Draw(img)

    draw = draw_miri_face(draw, img)
    draw = ImageDraw.Draw(img)

    draw_annotations(draw, font_ann)

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=BORDER_COL, width=2)
    draw.text((10, DRAW_H + 6), "A2-08  ECU  low angle  neutral",
              font=font_cap, fill=(160, 155, 130))
    draw.text((10, DRAW_H + 22),
              "Grandma Miri — SURPRISED → KNOWING — not fear, recognition. CRT amber-green glow on face.",
              font=font_cap, fill=TEXT_CAPTION)
    draw.text((10, DRAW_H + 38),
              "Act 2 emotional climax | Miri recognizes the Glitchkin | she belongs here | low angle = larger than life",
              font=font_ann, fill=(150, 140, 110))
    draw.text((PW - 200, DRAW_H + 46), "LTG_SB_act2_panel_a208_v001",
              font=font_ann, fill=(100, 95, 78))

    # Border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COL, width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")

    panels_path = os.path.join(PANELS_DIR, "LTG_SB_act2_panel_a208_v001.png")
    img.save(panels_path, "PNG")
    print(f"Also saved: {panels_path}")

    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("A2-08 panel generation complete (Cycle 17).")
