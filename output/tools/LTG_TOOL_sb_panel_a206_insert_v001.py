#!/usr/bin/env python3
"""
LTG_TOOL_sb_panel_a206_insert_v001.py
Storyboard Panel A2-06 MED — Cosmo + Luma Two-Shot Establishing Shot (Cycle 16)
Lee Tanaka, Storyboard Artist

Context:
  The INSERT (phone screen failure) already exists at:
  LTG_SB_act2_panel_a206_v001.png — phone screen static crash (works at B+)

  This MED shot is MISSING. Without it, the INSERT's emotional impact is reduced.
  The INSERT's failure must be emotionally meaningful — this establishes WHAT is
  being looked at and WHO cares about it.

Panel requirements:
  - MED two-shot: Cosmo and Luma together, BEFORE the phone failure
  - Establishes spatial relationship — who is where, what they're looking at
  - Their expressions: expectant / hopeful BEFORE the failure
  - They are BOTH looking at the phone (Cosmo holding it, Luma beside him)
  - Camera: medium shot, eye-level, neutral observer (outside / street context
    since Cosmo is using the Glitch Frequency app outside)
  - Environment: exterior / street context (night-adjacent, city warmth)

Beat context:
  A2-05b: Cosmo on street, confident with the GLITCH FREQ app open
  A2-06 MED [THIS]: Cosmo + Luma two-shot, both expectant, looking at phone
  A2-06 INSERT: Phone screen crashes — APP TERMINATED (existing panel)

Output:
  /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a206_med_v001.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_act2_panel_a206_med_v001.png")

os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 480, 270
CAPTION_H = 48
DRAW_H    = PH - CAPTION_H

# ── Palette ──────────────────────────────────────────────────────────────────
BG_CAPTION   = (25, 20, 18)
TEXT_CAPTION = (235, 228, 210)
BORDER_COL   = (20, 15, 12)
STATIC_WHITE = (240, 240, 240)

LUMA_SKIN    = (200, 136, 90)
LUMA_HAIR    = (22, 14, 8)
LUMA_PJ      = (160, 200, 180)
LUMA_OUTLINE = (42, 28, 14)

COSMO_SKIN   = (168, 118, 72)
COSMO_HAIR   = (14, 10, 6)
COSMO_SHIRT  = (80, 100, 170)
COSMO_PANTS  = (40, 55, 100)
COSMO_OUTLINE= (30, 20, 10)
COSMO_GLASS  = (92, 58, 32)
COSMO_LENS   = (238, 244, 255)

# Exterior night-adjacent environment
SKY_TOP      = (18, 14, 28)
SKY_HORIZON  = (40, 30, 50)
STREET_COL   = (52, 46, 40)
SIDEWALK_COL = (68, 62, 55)
BUILDING_COL = (35, 30, 44)
WARM_LAMP    = (220, 160, 80)
GLITCH_CYAN  = (0, 240, 255)


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


def draw_exterior_bg(draw, rng):
    """Night-adjacent exterior — street, sky gradient, building silhouettes."""
    # Sky gradient (top to horizon)
    horizon_y = int(DRAW_H * 0.52)
    for y in range(horizon_y):
        t = y / horizon_y
        r = int(SKY_TOP[0] + (SKY_HORIZON[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_HORIZON[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_HORIZON[2] - SKY_TOP[2]) * t)
        draw.line([(0, y), (PW, y)], fill=(r, g, b))

    # Sidewalk
    draw.rectangle([0, horizon_y, PW, DRAW_H], fill=SIDEWALK_COL)
    draw.line([0, horizon_y, PW, horizon_y], fill=(42, 38, 32), width=2)

    # Building silhouettes (background)
    for bx, bw, bh in [(0, 80, 80), (70, 60, 65), (200, 90, 72),
                        (350, 100, 88), (420, 60, 60)]:
        draw.rectangle([bx, horizon_y - bh, bx + bw, horizon_y],
                       fill=BUILDING_COL)
        # Windows (lit warm — city life)
        for wy in range(horizon_y - bh + 8, horizon_y - 6, 12):
            for wx in range(bx + 6, bx + bw - 6, 10):
                if rng.random() > 0.4:
                    draw.rectangle([wx, wy, wx + 5, wy + 5],
                                   fill=(rng.randint(180, 220),
                                         rng.randint(120, 160),
                                         rng.randint(40, 80)))

    # Streetlamp (right background)
    lamp_x, lamp_y = PW - 55, int(DRAW_H * 0.25)
    draw.line([lamp_x, lamp_y, lamp_x, horizon_y], fill=(80, 72, 60), width=4)
    draw.ellipse([lamp_x - 8, lamp_y - 10, lamp_x + 8, lamp_y + 4],
                 fill=WARM_LAMP)

    return horizon_y


def draw_phone_in_hand(draw, img, cx, cy, phone_w=36, phone_h=60):
    """
    Phone held at chest/waist level — screen facing up/toward characters.
    Shows the GLITCH FREQ app running (not yet crashed).
    This links visually to A2-05b.
    """
    # Phone frame
    draw.rounded_rectangle([cx - phone_w // 2, cy - phone_h // 2,
                             cx + phone_w // 2, cy + phone_h // 2],
                            radius=4,
                            fill=(18, 16, 22), outline=(70, 65, 60), width=3)
    # Screen (ACTIVE — app running, pre-crash)
    screen_m = 4
    screen_x1 = cx - phone_w // 2 + screen_m
    screen_y1 = cy - phone_h // 2 + screen_m
    screen_x2 = cx + phone_w // 2 - screen_m
    screen_y2 = cy + phone_h // 2 - screen_m - 6
    draw.rectangle([screen_x1, screen_y1, screen_x2, screen_y2],
                   fill=(8, 14, 24))

    # GLITCH FREQ app running — waveform (seed 42 matches A2-05b)
    import random
    rng2 = random.Random(42)
    wave_mid_y = (screen_y1 + screen_y2) // 2
    wave_w     = screen_x2 - screen_x1 - 4
    prev_pt    = None
    for x in range(screen_x1 + 2, screen_x2 - 2, 2):
        phase = (x - screen_x1) / wave_w * 2 * math.pi * 2
        amp   = 6 + rng2.randint(-2, 2)
        pt    = (x, int(wave_mid_y + math.sin(phase) * amp))
        if prev_pt:
            draw.line([prev_pt, pt], fill=GLITCH_CYAN, width=1)
        prev_pt = pt

    # Freq readout (tiny text lines)
    draw.text((screen_x1 + 2, screen_y1 + 2), "GHz", font=ImageFont.load_default(),
              fill=(0, 160, 200))

    # Phone glow (screen light washing onto hands)
    add_glow(img, cx, cy, 22, (0, 200, 240), steps=4, max_alpha=30)

    # Home bar at bottom of phone
    draw.line([cx - 6, screen_y2 + 3, cx + 6, screen_y2 + 3],
              fill=(60, 58, 55), width=2)


def draw_cosmo_med(draw, img, cx, cy, font_ann, horizon_y):
    """Cosmo in MED shot — EXPECTANT/HOPEFUL expression, holding phone."""
    head_w = 44
    head_h = 52
    head_cy = cy - 30

    # Body
    torso_w = 52
    torso_h = 65
    torso_top = head_cy + head_h // 2 + 3
    torso_bot = torso_top + torso_h
    draw.rounded_rectangle([cx - torso_w // 2, torso_top,
                             cx + torso_w // 2, torso_bot],
                            radius=6,
                            fill=COSMO_SHIRT, outline=COSMO_OUTLINE, width=2)

    # Collar
    draw.line([cx - 5, torso_top + 4, cx, torso_top + 12], fill=COSMO_OUTLINE, width=2)
    draw.line([cx + 5, torso_top + 4, cx, torso_top + 12], fill=COSMO_OUTLINE, width=2)

    # Neck
    draw.rectangle([cx - 7, head_cy + head_h // 2, cx + 7, torso_top + 2],
                   fill=COSMO_SKIN, outline=COSMO_OUTLINE, width=1)

    # Arms — both angled slightly down/inward toward phone
    arm_top = torso_top + 8
    # Left arm (holding side of phone)
    draw.line([cx - torso_w // 2, arm_top, cx - 14, torso_top + 42],
              fill=COSMO_SHIRT, width=12)
    draw.line([cx - torso_w // 2, arm_top, cx - 14, torso_top + 42],
              fill=COSMO_OUTLINE, width=1)
    # Right arm (holding other side)
    draw.line([cx + torso_w // 2, arm_top, cx + 14, torso_top + 42],
              fill=COSMO_SHIRT, width=12)
    draw.line([cx + torso_w // 2, arm_top, cx + 14, torso_top + 42],
              fill=COSMO_OUTLINE, width=1)

    # Hands holding phone
    draw.ellipse([cx - 20, torso_top + 38, cx - 10, torso_top + 50],
                 fill=COSMO_SKIN, outline=COSMO_OUTLINE, width=1)
    draw.ellipse([cx + 10, torso_top + 38, cx + 20, torso_top + 50],
                 fill=COSMO_SKIN, outline=COSMO_OUTLINE, width=1)

    # Phone (between hands)
    phone_cy = torso_top + 50
    draw_phone_in_hand(draw, img, cx, phone_cy + 10, phone_w=30, phone_h=48)

    # Head
    corner_r = int(head_w * 0.12)
    draw.rounded_rectangle([cx - head_w // 2, head_cy - head_h // 2,
                             cx + head_w // 2, head_cy + head_h // 2],
                            radius=corner_r,
                            fill=COSMO_SKIN, outline=COSMO_OUTLINE, width=2)

    # Hair
    hair_h = int(head_h * 0.16)
    draw.rounded_rectangle([cx - head_w // 2 + 2, head_cy - head_h // 2 - hair_h + 3,
                             cx + head_w // 2 - 2, head_cy - head_h // 2 + hair_h],
                            radius=int(head_w * 0.10),
                            fill=COSMO_HAIR, outline=COSMO_OUTLINE, width=1)

    # Glasses
    lens_r   = int(head_w * 0.17)
    lens_sep = int(head_w * 0.22)
    frame_w  = max(2, int(head_w * 0.06))
    eye_y    = head_cy - int(head_h * 0.05)

    l_lx = cx - lens_sep
    r_lx = cx + lens_sep

    for lx in [l_lx, r_lx]:
        draw.ellipse([lx - lens_r, eye_y - lens_r, lx + lens_r, eye_y + lens_r],
                     fill=COSMO_LENS, outline=COSMO_GLASS, width=frame_w)
    draw.line([l_lx + lens_r, eye_y, r_lx - lens_r, eye_y],
              fill=COSMO_GLASS, width=frame_w)

    # EXPECTANT eyes: wide, looking down at phone
    eye_r = int(lens_r * 0.55)
    for lx in [l_lx, r_lx]:
        draw.ellipse([lx - eye_r, eye_y - eye_r, lx + eye_r, eye_y + eye_r],
                     fill=(235, 215, 180))
        p_r = max(2, eye_r // 2)
        # Pupils looking DOWN toward phone
        draw.ellipse([lx - p_r, eye_y, lx + p_r, eye_y + p_r * 2],
                     fill=(20, 15, 10))
        draw.rectangle([lx - p_r + 1, eye_y + 1,
                        lx - p_r + 3, eye_y + 3], fill=STATIC_WHITE)

    # HOPEFUL brows: both slightly raised (expectant)
    brow_thick = max(2, int(head_w * 0.05))
    for lx, ly in [(l_lx, eye_y), (r_lx, eye_y)]:
        draw.arc([lx - lens_r, ly - lens_r - 10,
                  lx + lens_r, ly - lens_r + 4],
                 start=200, end=340, fill=COSMO_HAIR, width=brow_thick)

    # Mouth: small hopeful upturn (slight smile — expectant)
    mouth_y = head_cy + int(head_h * 0.22)
    mouth_w = int(head_w * 0.25)
    draw.arc([cx - mouth_w // 2, mouth_y - 4,
              cx + mouth_w // 2, mouth_y + 4],
             start=0, end=180, fill=COSMO_OUTLINE, width=max(2, int(head_w * 0.04)))

    return head_cy, head_h


def draw_luma_med(draw, cx, cy, font_ann):
    """Luma in MED shot — beside Cosmo, EXPECTANT/HOPEFUL, leaning in to see phone."""
    head_w = 40
    head_h = 48
    head_cy = cy - 25

    # Body
    torso_w = 48
    torso_h = 60
    torso_top = head_cy + head_h // 2 + 3
    torso_bot = torso_top + torso_h
    draw.rounded_rectangle([cx - torso_w // 2, torso_top,
                             cx + torso_w // 2, torso_bot],
                            radius=5,
                            fill=LUMA_PJ, outline=LUMA_OUTLINE, width=2)

    # Neck
    draw.rectangle([cx - 6, head_cy + head_h // 2, cx + 6, torso_top + 2],
                   fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=1)

    # Arm LEANING TOWARD phone (toward Cosmo, left arm reaches)
    draw.line([cx - torso_w // 2, torso_top + 12, cx - 30, torso_top + 50],
              fill=LUMA_SKIN, width=10)
    draw.line([cx - torso_w // 2, torso_top + 12, cx - 30, torso_top + 50],
              fill=LUMA_OUTLINE, width=1)
    # Hand reaching
    draw.ellipse([cx - 40, torso_top + 46, cx - 24, torso_top + 58],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=1)

    # Right arm (relaxed at side)
    draw.line([cx + torso_w // 2, torso_top + 12, cx + torso_w // 2 + 8, torso_top + 45],
              fill=LUMA_SKIN, width=10)
    draw.line([cx + torso_w // 2, torso_top + 12, cx + torso_w // 2 + 8, torso_top + 45],
              fill=LUMA_OUTLINE, width=1)

    # Hair
    draw.ellipse([cx - head_w // 2 - 8, head_cy - head_h // 2 - 14,
                  cx + head_w // 2 + 8, head_cy - head_h // 2 + 6],
                 fill=LUMA_HAIR)
    # Head
    draw.ellipse([cx - head_w // 2, head_cy - head_h // 2,
                  cx + head_w // 2, head_cy + head_h // 2],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=2)

    # EXPECTANT eyes: wide, slightly tilted (excited to see result)
    eye_sep = int(head_w * 0.25)
    eye_r   = 7
    for sign, ex in [(-1, cx - eye_sep), (1, cx + eye_sep)]:
        ey = head_cy - 6
        # Eye white
        draw.ellipse([ex - eye_r, ey - eye_r, ex + eye_r, ey + eye_r],
                     fill=(240, 220, 190))
        # Iris (warm brown — Luma)
        draw.ellipse([ex - eye_r + 2, ey - eye_r + 2, ex + eye_r - 2, ey + eye_r - 2],
                     fill=(120, 70, 30))
        # Pupil — looking sideways/down toward phone (down + toward Cosmo = left)
        pu_off_x = -2 if sign < 0 else -3
        pu_off_y = 2
        draw.ellipse([ex + pu_off_x - 3, ey + pu_off_y - 3,
                      ex + pu_off_x + 3, ey + pu_off_y + 3],
                     fill=(20, 15, 10))
        # Highlight
        draw.rectangle([ex + pu_off_x - 2, ey + pu_off_y - 2,
                        ex + pu_off_x, ey + pu_off_y], fill=STATIC_WHITE)

    # HOPEFUL brows: slightly raised inward (excited/hopeful)
    for ex in [cx - eye_sep, cx + eye_sep]:
        ey = head_cy - 6
        draw.arc([ex - eye_r - 2, ey - eye_r - 9,
                  ex + eye_r + 2, ey - eye_r + 1],
                 start=200, end=340, fill=(50, 32, 14), width=2)

    # Mouth: open hopeful smile (small teeth visible)
    mouth_y = head_cy + int(head_h * 0.25)
    mouth_w = int(head_w * 0.35)
    draw.arc([cx - mouth_w // 2, mouth_y - 5,
              cx + mouth_w // 2, mouth_y + 5],
             start=0, end=180, fill=LUMA_OUTLINE, width=2)
    # Teeth suggestion
    draw.rectangle([cx - mouth_w // 2 + 3, mouth_y - 3,
                    cx + mouth_w // 2 - 3, mouth_y + 1],
                   fill=(240, 235, 225))


def generate():
    font     = load_font(13)
    font_b   = load_font(13, bold=True)
    font_cap = load_font(11)
    font_ann = load_font(9)

    img  = Image.new('RGB', (PW, PH), SKY_TOP)
    draw = ImageDraw.Draw(img)

    rng = random.Random(2206)

    # ── Background: exterior night ──────────────────────────────────────────
    horizon_y = draw_exterior_bg(draw, rng)

    # ── Characters ──────────────────────────────────────────────────────────
    # Cosmo: left-center, holding phone
    cosmo_cx = 190
    cosmo_cy = horizon_y + 55

    # Luma: right of Cosmo, leaning in
    luma_cx  = 300
    luma_cy  = horizon_y + 55

    draw_luma_med(draw, luma_cx, luma_cy, font_ann)
    cosmo_head_cy, cosmo_head_h = draw_cosmo_med(draw, img, cosmo_cx, cosmo_cy,
                                                  font_ann, horizon_y)
    draw = ImageDraw.Draw(img)

    # ── Phone screen glow on their faces ────────────────────────────────────
    phone_cy = cosmo_cy - 30 + 52 + 65 + 60  # approximate phone position
    add_glow(img, cosmo_cx, cosmo_cy + 30, 55, (0, 200, 240), steps=4, max_alpha=22)
    add_glow(img, luma_cx - 15, luma_cy + 20, 40, (0, 200, 240), steps=4, max_alpha=15)
    draw = ImageDraw.Draw(img)

    # ── ANNOTATIONS ─────────────────────────────────────────────────────────
    # Camera spec
    draw.text((4, 2), "CAMERA: MED TWO-SHOT | EYE-LEVEL | NEUTRAL OBS", font=font_ann,
              fill=(200, 190, 130))
    draw.text((4, 11), "Cosmo left / Luma right — both looking at phone", font=font_ann,
              fill=(160, 150, 100))

    # Character labels
    draw.text((cosmo_cx - 22, cosmo_head_cy - cosmo_head_h // 2 - 18),
              "COSMO", font=font_ann, fill=(200, 190, 160))
    draw.text((luma_cx - 16, luma_cy - 80),
              "LUMA", font=font_ann, fill=(200, 190, 160))

    # Expectant expression label
    draw.text((cosmo_cx - 28, cosmo_head_cy + cosmo_head_h // 2 + 4),
              "HOPEFUL/EXPECTANT", font=font_ann, fill=(220, 200, 80))

    # INSERT leads label
    draw.text((4, DRAW_H - 22), "→ leads to A2-06 INSERT (phone screen crash)",
              font=font_ann, fill=(180, 140, 100))

    # ── Caption bar ──────────────────────────────────────────────────────────
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=BORDER_COL, width=2)
    draw.text((8, DRAW_H + 6), "A2-06 MED  two-shot  eye-level  neutral observer",
              font=font_cap, fill=(160, 160, 160))
    draw.text((8, DRAW_H + 20),
              "Cosmo + Luma — expectant/hopeful, looking at phone (BEFORE crash).",
              font=font_cap, fill=TEXT_CAPTION)
    draw.text((8, DRAW_H + 34),
              "Establishes spatial relationship and stakes — makes INSERT failure emotionally meaningful.",
              font=font_ann, fill=(150, 140, 110))

    # Border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COL, width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
    print("A2-06 MED establishing shot generation complete (Cycle 16).")
