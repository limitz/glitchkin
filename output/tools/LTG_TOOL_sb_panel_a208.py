#!/usr/bin/env python3
"""
LTG_TOOL_sb_panel_a208.py
Storyboard Panel A2-08 — Grandma Miri Returns — Rebuilt per Critique Cycle 9
Lee Tanaka, Storyboard Artist

REBUILD NOTES (v002 vs v001):
v001 used ECU low-angle (power declaration reading).
v002 corrects to OPTION A — Luma POV:
  Camera: level eye / slightly upward (from Luma's eye height)
  We're looking from approximately Luma's eye height INTO Miri's face.
  Miri fills the upper 2/3 of frame.
  INTIMATE, CLOSE, PERSONAL — not larger-than-life.
  This is the moment of connection, not confrontation.

Camera: MEDIUM CU / eye-level (Luma's height) / slightly upward
  → Miri's face fills upper 2/3 of frame
  → We share Luma's POV — the audience IS Luma in this shot
  → Warm kitchen light from behind Miri (doorway backlight)
  → CRT glow on Miri's face (amber-green catch light, left cheek)
  → Miri is framed by the doorway — warm amber surround

Expression: SURPRISED → KNOWING
  Wide eyes, soft brows (wonder not alarm), one corner of mouth rising.
  Age lines = earned warmth.

Output:
  /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_act2_panel_a208.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

ACT2_PANELS_DIR = "/home/wipkat/team/output/storyboards/act2/panels"
PANELS_DIR      = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH     = os.path.join(ACT2_PANELS_DIR, "LTG_SB_act2_panel_a208.png")

os.makedirs(ACT2_PANELS_DIR, exist_ok=True)
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H   # 540px scene area

# ── Palette ──────────────────────────────────────────────────────────────────
BG_CAPTION   = (22, 18, 14)
TEXT_CAPTION = (235, 228, 210)
BORDER_COL   = (18, 12, 8)

# Grandma Miri
MIRI_SKIN       = (215, 165, 120)
MIRI_SKIN_LIGHT = (232, 185, 140)
MIRI_HAIR       = (195, 185, 175)
MIRI_HAIR_DARK  = (150, 142, 135)
MIRI_SWEATER    = (160, 100, 60)
MIRI_OUTLINE    = (80, 48, 24)

# CRT glow (amber-green)
CRT_AMBER    = (230, 180, 80)
CRT_GREEN    = (80, 200, 120)
CRT_MIX      = (180, 200, 100)
CRT_WARM     = (240, 195, 90)

# Doorway / kitchen warm light (Miri's backlight)
KITCHEN_WARM = (240, 195, 120)  # warm amber from behind Miri
KITCHEN_DIM  = (180, 140, 80)

# Background
BG_DARK      = (22, 16, 12)    # dark hallway
BG_DOORWAY   = (80, 62, 38)    # warm doorway surround
BG_WALL      = (38, 30, 22)

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
    Background: doorway surround — warm kitchen light from BEHIND Miri.
    Creates a backlight halo / rim light on her hair and shoulders.
    Dark hallway around doorway.
    CRT glow from off-frame lower-left (room below camera POV).
    """
    # Dark hallway base
    draw.rectangle([0, 0, PW, DRAW_H], fill=BG_DARK)

    # Doorway shape — arched warm rectangle in upper center
    # Miri stands IN the doorway — warm light frames her from behind
    door_left  = int(PW * 0.12)
    door_right = int(PW * 0.88)
    door_top   = 0
    door_bot   = int(DRAW_H * 0.75)

    # Doorway warm fill (kitchen behind her)
    draw.rectangle([door_left, door_top, door_right, door_bot], fill=BG_DOORWAY)

    # Kitchen glow from doorway center (bright warm backlight)
    door_cx = PW // 2
    add_glow(img, door_cx, door_bot // 2, 280, KITCHEN_WARM, steps=8, max_alpha=55)
    add_glow(img, door_cx, door_bot // 3, 200, KITCHEN_WARM, steps=6, max_alpha=40)

    # Doorway frame (dark edges, vertical)
    frame_w = 20
    draw.rectangle([door_left - frame_w, door_top, door_left, door_bot],
                   fill=(28, 22, 14))
    draw.rectangle([door_right, door_top, door_right + frame_w, door_bot],
                   fill=(28, 22, 14))

    # Floor below doorway
    draw.rectangle([0, door_bot, PW, DRAW_H], fill=BG_DARK)

    # CRT glow from off-frame lower-left (the TV in the room behind camera)
    add_glow(img, -20, DRAW_H - 30, 300, CRT_MIX, steps=7, max_alpha=35)
    add_glow(img, 0, DRAW_H, 220, CRT_AMBER, steps=5, max_alpha=28)


def draw_miri_face(draw, img):
    """
    Grandma Miri — MEDIUM CU from Luma's POV (eye height, slightly upward).
    Face fills upper 2/3 of frame.
    INTIMATE framing — not larger-than-life, but personal and close.
    Miri is centered, face at top 2/3 of DRAW_H.

    Expression: SURPRISED → KNOWING
    """
    face_cx = PW // 2
    # Slightly upward tilt: face center at ~35% from top of draw area
    face_cy = int(DRAW_H * 0.35)

    head_w  = 310   # wide MCU — intimate, personal
    head_h  = 280

    # ── Shoulders (bottom of frame — body below face in POV shot) ────────────
    shoulder_w = 420
    shoulder_y = face_cy + head_h // 2 - 20
    # Sweater torso (partially visible at bottom)
    draw.ellipse([face_cx - shoulder_w // 2, shoulder_y,
                  face_cx + shoulder_w // 2, shoulder_y + 150],
                 fill=MIRI_SWEATER, outline=(100, 60, 35), width=2)
    # Neck
    neck_w = 80
    draw.rectangle([face_cx - neck_w // 2, shoulder_y - 30,
                    face_cx + neck_w // 2, shoulder_y + 30],
                   fill=MIRI_SKIN, outline=MIRI_OUTLINE, width=1)

    # ── Hair — framing face, kitchen backlight rim ────────────────────────────
    # Hair above face
    draw.ellipse([face_cx - head_w // 2 - 15, face_cy - head_h // 2 - 35,
                  face_cx + head_w // 2 + 15, face_cy - head_h // 2 + 45],
                 fill=MIRI_HAIR)
    draw.ellipse([face_cx - head_w // 2 + 8, face_cy - head_h // 2 - 30,
                  face_cx + head_w // 2 - 8, face_cy - head_h // 2 + 35],
                 fill=MIRI_HAIR_DARK)

    # Rim light on hair from kitchen behind (warm amber highlight)
    glow_layer = Image.new('RGBA', (PW, DRAW_H), (0, 0, 0, 0))
    gl = ImageDraw.Draw(glow_layer)
    # Top of hair lit from behind
    for r in [80, 55, 35]:
        alpha = max(12, 45 - r // 2)
        gl.ellipse([face_cx - r, face_cy - head_h // 2 - 30 - r,
                    face_cx + r, face_cy - head_h // 2 - 30 + r],
                   fill=(*KITCHEN_WARM, alpha))
    # Left side rim
    left_rim_cx = face_cx - head_w // 2 - 5
    left_rim_cy = face_cy
    for r in [50, 35]:
        alpha = max(10, 30 - r // 2)
        gl.ellipse([left_rim_cx - r, left_rim_cy - r,
                    left_rim_cx + r, left_rim_cy + r],
                   fill=(*KITCHEN_WARM, alpha))
    # Right side rim
    right_rim_cx = face_cx + head_w // 2 + 5
    right_rim_cy = face_cy
    for r in [50, 35]:
        alpha = max(10, 30 - r // 2)
        gl.ellipse([right_rim_cx - r, right_rim_cy - r,
                    right_rim_cx + r, right_rim_cy + r],
                   fill=(*KITCHEN_WARM, alpha))

    # CRT catch light on LEFT cheek (amber-green from off-frame lower-left)
    cheek_cx = face_cx - head_w // 4
    cheek_cy = face_cy + 25
    for r in [90, 65, 42]:
        alpha = max(8, 30 - r // 3)
        gl.ellipse([cheek_cx - r, cheek_cy - r,
                    cheek_cx + r, cheek_cy + r],
                   fill=(*CRT_AMBER, alpha))
    # Green component on left brow
    brow_gx = face_cx - head_w // 3
    brow_gy = face_cy - head_h // 5
    for r in [60, 40]:
        alpha = max(6, 20 - r // 4)
        gl.ellipse([brow_gx - r, brow_gy - r,
                    brow_gx + r, brow_gy + r],
                   fill=(*CRT_GREEN, alpha))

    base  = img.convert('RGBA')
    panel = base.crop((0, 0, PW, DRAW_H))
    merged = Image.alpha_composite(panel.convert('RGBA'), glow_layer)
    img.paste(merged.convert('RGB'), (0, 0))
    draw = ImageDraw.Draw(img)

    # Hair side volume
    draw.ellipse([face_cx - head_w // 2 - 18, face_cy - head_h // 4,
                  face_cx - head_w // 2 + 32, face_cy + head_h // 4],
                 fill=MIRI_HAIR)
    draw.ellipse([face_cx + head_w // 2 - 32, face_cy - head_h // 4,
                  face_cx + head_w // 2 + 18, face_cy + head_h // 4],
                 fill=MIRI_HAIR)

    # ── Main face ────────────────────────────────────────────────────────────
    draw.ellipse([face_cx - head_w // 2, face_cy - head_h // 2,
                  face_cx + head_w // 2, face_cy + head_h // 2],
                 fill=MIRI_SKIN, outline=MIRI_OUTLINE, width=2)

    # ── Facial detail lines (age = earned warmth) ─────────────────────────────
    # Laugh lines at cheek corners
    for offset_y in [0, 5]:
        draw.arc([face_cx - head_w // 4 - 10, face_cy + 22 + offset_y,
                  face_cx - head_w // 4 + 18, face_cy + 52 + offset_y],
                 start=220, end=320, fill=MIRI_OUTLINE, width=1)
    for offset_y in [0, 5]:
        draw.arc([face_cx + head_w // 4 - 18, face_cy + 22 + offset_y,
                  face_cx + head_w // 4 + 10, face_cy + 52 + offset_y],
                 start=220, end=320, fill=MIRI_OUTLINE, width=1)
    # Forehead lines (2, subtle)
    for ly in [face_cy - head_h // 3 + 5, face_cy - head_h // 3 + 15]:
        draw.arc([face_cx - head_w // 3, ly, face_cx + head_w // 3, ly + 10],
                 start=200, end=340, fill=(170, 120, 80), width=1)

    # ── EYES — SURPRISED / KNOWING ──────────────────────────────────────────
    eye_y    = face_cy - 18
    eye_sep  = 72
    eye_w    = 56
    eye_h    = 44

    for side, ex_off in enumerate([-eye_sep, eye_sep]):
        ex = face_cx + ex_off

        # Sclera — wide open
        draw.ellipse([ex - eye_w // 2, eye_y - eye_h // 2,
                      ex + eye_w // 2, eye_y + eye_h // 2],
                     fill=STATIC_WHITE, outline=MIRI_OUTLINE, width=2)
        # Iris
        draw.ellipse([ex - 15, eye_y - 15, ex + 15, eye_y + 15],
                     fill=(110, 75, 42))
        # Pupil
        draw.ellipse([ex - 9, eye_y - 9, ex + 9, eye_y + 9],
                     fill=(20, 12, 8))
        # CRT catch-light (amber — left eye has more since facing screen)
        goff = 6 if side == 0 else 4
        draw.ellipse([ex - 9 + goff, eye_y - 9 + 3,
                      ex - 9 + goff + 5, eye_y - 9 + 8],
                     fill=CRT_AMBER)
        draw.rectangle([ex + 7, eye_y - 8, ex + 10, eye_y - 5],
                       fill=CRT_GREEN)
        # Lower eyelid crinkle (recognition warmth)
        draw.arc([ex - eye_w // 2 + 6, eye_y + eye_h // 4,
                  ex + eye_w // 2 - 6, eye_y + eye_h // 2 + 7],
                 start=10, end=170, fill=MIRI_OUTLINE, width=1)

    # ── BROWS — raised soft arc (wonder, not alarm) ───────────────────────────
    brow_y = eye_y - eye_h // 2 - 12
    for side, ex_off in enumerate([-eye_sep, eye_sep]):
        ex = face_cx + ex_off
        draw.arc([ex - eye_w // 2, brow_y - 10,
                  ex + eye_w // 2, brow_y + 12],
                 start=200, end=340, fill=MIRI_HAIR_DARK, width=3)
        for hx in range(ex - eye_w // 2 + 5, ex + eye_w // 2 - 5, 7):
            angle_y = brow_y - int(10 * math.sin(
                math.pi * (hx - (ex - eye_w // 2)) / eye_w))
            draw.line([hx, angle_y + 2, hx + 3, angle_y - 2],
                      fill=MIRI_HAIR_DARK, width=1)

    # ── NOSE (MCU — visible) ─────────────────────────────────────────────────
    nose_tip_y = eye_y + 52
    draw.line([face_cx - 4, eye_y + 16, face_cx - 7, nose_tip_y - 5],
              fill=(170, 115, 75), width=2)
    draw.arc([face_cx - 22, nose_tip_y - 12, face_cx - 2, nose_tip_y + 5],
             start=30, end=200, fill=MIRI_OUTLINE, width=2)
    draw.arc([face_cx + 2, nose_tip_y - 12, face_cx + 22, nose_tip_y + 5],
             start=340, end=150, fill=MIRI_OUTLINE, width=2)
    draw.ellipse([face_cx - 8, nose_tip_y - 6, face_cx + 8, nose_tip_y + 6],
                 fill=MIRI_SKIN_LIGHT)

    # ── MOUTH — SURPRISED → KNOWING ──────────────────────────────────────────
    mouth_y   = face_cy + 72
    mouth_half = 44

    # Slightly open (surprise — lips parted)
    draw.arc([face_cx - mouth_half, mouth_y - 8,
              face_cx + mouth_half, mouth_y + 12],
             start=5, end=175, fill=MIRI_OUTLINE, width=3)

    # Right corner lifting (recognition — her left, viewer's right)
    draw.arc([face_cx + mouth_half - 22, mouth_y - 16,
              face_cx + mouth_half + 10, mouth_y + 4],
             start=260, end=360, fill=MIRI_OUTLINE, width=2)

    # Upper lip
    draw.arc([face_cx - mouth_half + 8, mouth_y - 14,
              face_cx + mouth_half - 8, mouth_y],
             start=200, end=340, fill=(160, 105, 70), width=2)
    # Lower lip
    draw.arc([face_cx - mouth_half + 12, mouth_y - 2,
              face_cx + mouth_half - 12, mouth_y + 18],
             start=0, end=180, fill=(185, 120, 85), width=2)

    # Nasolabial folds
    draw.arc([face_cx - 42, nose_tip_y,
              face_cx - 14, mouth_y + 5],
             start=240, end=330, fill=(170, 115, 78), width=1)
    draw.arc([face_cx + 14, nose_tip_y,
              face_cx + 42, mouth_y + 5],
             start=210, end=300, fill=(170, 115, 78), width=1)

    return draw


def draw_annotations(draw, font_ann):
    """Annotations: shot type, camera, expression callouts."""
    draw.text((8, 8),
              "A2-08  /  MCU  /  eye-level (Luma POV)  /  slightly upward",
              font=font_ann, fill=ANN_COL)
    draw.text((8, 20),
              "Miri in doorway — warm kitchen light from behind — INTIMATE",
              font=font_ann, fill=ANN_DIM)

    # Miri expression callout
    draw.text((PW - 265, int(DRAW_H * 0.12)), "GRANDMA MIRI",
              font=font_ann, fill=CALLOUT_MIRI)
    draw.text((PW - 265, int(DRAW_H * 0.12) + 12), "SURPRISED → KNOWING",
              font=font_ann, fill=(200, 220, 160))
    draw.text((PW - 265, int(DRAW_H * 0.12) + 24), "not fear — recognition",
              font=font_ann, fill=(160, 185, 130))

    # Eye callout
    draw.text((8, int(DRAW_H * 0.30)), "eyes: wide / wonder",
              font=font_ann, fill=(200, 200, 160))
    draw.text((8, int(DRAW_H * 0.30) + 12), "no fear lines",
              font=font_ann, fill=(160, 160, 125))

    # Kitchen light callout
    draw.text((PW - 250, int(DRAW_H * 0.72)), "kitchen warm light — backlight",
              font=font_ann, fill=(220, 185, 100))
    draw.text((PW - 250, int(DRAW_H * 0.72) + 12), "rim on hair + shoulders",
              font=font_ann, fill=(190, 160, 90))

    # CRT glow callout
    draw.text((8, DRAW_H - 32), "CRT glow — off-frame lower-left",
              font=font_ann, fill=(190, 185, 100))
    draw.text((8, DRAW_H - 20), "amber catch on left cheek + brow",
              font=font_ann, fill=(170, 190, 90))

    # POV label
    draw.text((PW - 220, 8), "LUMA POV — eye height",
              font=font_ann, fill=ANN_DIM)
    draw.text((PW - 220, 18), "intimate / personal",
              font=font_ann, fill=ANN_DIM)


def make_panel():
    font_cap = load_font(12)
    font_ann = load_font(11)

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
    draw.text((10, DRAW_H + 6), "A2-08  MCU  eye-level (Luma POV)  Luma's height looking up",
              font=font_cap, fill=(160, 155, 130))
    draw.text((10, DRAW_H + 22),
              "Grandma Miri — SURPRISED → KNOWING. Not fear. Recognition. Kitchen backlight. CRT glow left cheek.",
              font=font_cap, fill=TEXT_CAPTION)
    draw.text((10, DRAW_H + 38),
              "OPTION A: Luma POV — intimate, personal. Miri fills upper 2/3. She belongs here. She knows.",
              font=font_ann, fill=(150, 140, 110))
    draw.text((PW - 260, DRAW_H + 46), "LTG_SB_act2_panel_a208_v002  |  Cycle 19",
              font=font_ann, fill=(100, 95, 78))

    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COL, width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")

    panels_path = os.path.join(PANELS_DIR, "LTG_SB_act2_panel_a208.png")
    img.save(panels_path, "PNG")
    print(f"Also saved: {panels_path}")

    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("A2-08 v002 panel generation complete (Cycle 19).")
