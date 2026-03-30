#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
Act 2 Panels — Cycle 15 — "Luma & the Glitchkin"
Lee Tanaka, Storyboard Artist

Generates 3 Act 2 storyboard panels:

  A2-03 — Cosmo SKEPTICAL expression (wide/medium shot — wrong plan beat)
  A2-04 — Investigation montage (2x2 vignette grid — Luma searches the house)
  A2-07 — BLOCKED placeholder (awaiting Byte expression sheet v002 RESIGNED + cracked-eye glyph)

Plus an updated Act 2 contact sheet (v002) with all 7 Act 2 panels.

Key design principles (MEMORY.md):
  - Body language tells the story before the face
  - Glow effects ADD light (alpha_composite), never darkness
  - Pixel confetti = ADD light scatter (Glitch Layer visual signature)
  - Contact sheet is the first read — arc must be readable in thumbnail
  - Naming: LTG_[CATEGORY]_[descriptor]_v[###].[ext]
  - Dutch tilt = Image.rotate() on entire canvas
  - Byte's expression: four components (eye aperture, cracked-eye pixel state, mouth shape, body lean)
  - Cosmo glasses: always tilted 7° neutral, 9° skeptical
  - Cosmo skeptical: one brow up (his left, viewer's right), flat deadpan mouth

Outputs (480x270px each):
  /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a203.png
  /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a204.png
  /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a207.png  (placeholder)
  /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_a2_02.png       (copy)
  /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_a2_03.png
  /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_a2_04.png
  /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_a2_07.png
  /home/wipkat/team/output/storyboards/act2/LTG_SB_act2_contact_sheet.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random
import os
import shutil

PANELS_DIR     = "/home/wipkat/team/output/storyboards/panels"
ACT2_PANELS    = "/home/wipkat/team/output/storyboards/act2/panels"
SHEETS_DIR     = "/home/wipkat/team/output/storyboards"
ACT2_SHEETS    = "/home/wipkat/team/output/storyboards/act2"
PW, PH         = 480, 270
CAPTION_H      = 48
DRAW_H         = PH - CAPTION_H   # 222px scene area
BORDER         = 2

os.makedirs(PANELS_DIR,  exist_ok=True)
os.makedirs(ACT2_PANELS, exist_ok=True)
os.makedirs(SHEETS_DIR,  exist_ok=True)
os.makedirs(ACT2_SHEETS, exist_ok=True)

# ── Palette ──────────────────────────────────────────────────────────────────
BG_CAPTION    = (25, 20, 18)
TEXT_CAPTION  = (235, 228, 210)
TEXT_ANN      = (20, 15, 12)
BORDER_COL    = (20, 15, 12)

LUMA_SKIN     = (200, 136, 90)
LUMA_HAIR     = (22, 14, 8)
LUMA_PJ       = (160, 200, 180)
LUMA_OUTLINE  = (42, 28, 14)

COSMO_SKIN    = (168, 118, 72)
COSMO_HAIR    = (14, 10, 6)
COSMO_SHIRT   = (80, 100, 170)
COSMO_PANTS   = (40, 55, 100)
COSMO_OUTLINE = (30, 20, 10)
COSMO_GLASS   = (92, 58, 32)   # Warm Espresso Brown #5C3A20
COSMO_LENS    = (238, 244, 255)

BYTE_BODY     = (0, 212, 232)
BYTE_MID      = (0, 160, 175)
BYTE_DARK     = (0, 105, 115)
BYTE_OUTLINE  = (10, 10, 20)
BYTE_SCAR     = (255, 45, 107)
BYTE_EYE_W   = (232, 248, 255)
BYTE_EYE_CYN  = (0, 240, 255)
BYTE_EYE_PUP  = (10, 10, 20)
BYTE_BEZEL    = (26, 58, 64)

GLYPH_DEAD    = (10, 10, 24)
GLYPH_DIM     = (0, 80, 100)
GLYPH_MID     = (0, 168, 180)
GLYPH_CRACK   = (255, 45, 107)
GLYPH_BRIGHT  = (200, 255, 255)
GLYPH_OVER    = (10, 10, 20)

GLITCH_CYAN   = (0, 240, 255)
GLITCH_MAG    = (255, 0, 200)
GLITCH_ACID   = (180, 255, 40)
GLITCH_PURPLE = (123, 47, 190)
GLITCH_WHITE  = (240, 240, 240)

WARM_AMBER    = (55, 38, 24)
WARM_WALL     = (110, 85, 55)
WARM_FLOOR    = (72, 54, 36)
TECH_DEN_WALL = (120, 95, 62)
TECH_DEN_FLR  = (78, 58, 38)

STATIC_WHITE  = (240, 240, 240)
BLOCKED_ORANGE= (220, 120, 20)
BLOCKED_BG    = (30, 22, 16)
BLOCKED_RED   = (200, 40, 40)


def load_fonts():
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    bold_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    def try_font(ps, size):
        for p in ps:
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
        return ImageFont.load_default()
    return (
        try_font(paths, 13),
        try_font(bold_paths, 13),
        try_font(paths, 11),
        try_font(paths, 9),
    )


def make_panel(filepath, shot_label, caption_text, draw_fn, bg_color=(30, 24, 20)):
    """Create a 480×270 storyboard panel."""
    img  = Image.new('RGB', (PW, PH), bg_color)
    draw = ImageDraw.Draw(img)
    font, font_bold, font_cap, font_ann = load_fonts()

    draw.rectangle([0, 0, PW, DRAW_H], fill=bg_color)
    draw_fn(img, draw, font, font_bold, font_cap, font_ann)

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=BORDER_COL, width=BORDER)
    draw.text((8, DRAW_H + 6), shot_label, font=font_cap, fill=(160, 160, 160))

    # Caption wrap
    words = caption_text.split()
    lines, current = [], ""
    for w in words:
        test = (current + " " + w).strip()
        if len(test) <= 62:
            current = test
        else:
            lines.append(current)
            current = w
    if current:
        lines.append(current)
    for i, line in enumerate(lines[:2]):
        draw.text((8, DRAW_H + 20 + i * 14), line, font=font_cap, fill=TEXT_CAPTION)

    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COL, width=BORDER)
    img.save(filepath)
    print(f"  Saved: {os.path.basename(filepath)}")
    return img


def add_glow(img, cx, cy, r_max, color_rgb, steps=6, max_alpha=60):
    """Add concentric glow rings — ADD light via alpha_composite. Never darkens."""
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def pixel_confetti(draw, cx, cy, spread_x, spread_y, rng, n=10, colors=None):
    """Scatter pixel confetti (Glitch Layer intrusion marker)."""
    if colors is None:
        colors = [GLITCH_CYAN, GLITCH_MAG, GLITCH_ACID, GLITCH_PURPLE, GLITCH_WHITE]
    for _ in range(n):
        px  = cx + rng.randint(-spread_x, spread_x)
        py  = cy + rng.randint(-spread_y, spread_y)
        sz  = rng.randint(2, 5)
        col = rng.choice(colors)
        draw.rectangle([px, py, px + sz, py + sz], fill=col)


def draw_cosmo_skeptical(draw, cx, cy, head_w, head_h, full_body=True):
    """
    Draw Cosmo with SKEPTICAL expression:
      - One brow UP (his left = viewer's right), other brow flat
      - Flat deadpan mouth
      - Glasses tilted 9° (more than neutral 7°)
      - Arms crossed (skeptical body language)
    head_w, head_h: dimensions of the rounded-rectangle head
    """
    # ── Body ────────────────────────────────────────────────────────────────
    torso_w = int(head_w * 0.86)
    torso_h = int(head_h * 1.2)
    neck_h  = int(head_h * 0.08)

    head_top  = cy - head_h // 2
    head_bot  = cy + head_h // 2
    neck_top  = head_bot
    neck_bot  = neck_top + neck_h
    torso_top = neck_bot
    torso_bot = torso_top + torso_h

    if full_body:
        # Upper legs
        leg_w  = int(head_w * 0.22)
        leg_h  = int(head_h * 0.8)
        lleg_x = cx - torso_w // 2
        rleg_x = cx + torso_w // 2 - leg_w
        draw.rectangle([lleg_x, torso_bot, lleg_x + leg_w, torso_bot + leg_h],
                       fill=COSMO_PANTS, outline=COSMO_OUTLINE, width=1)
        draw.rectangle([rleg_x, torso_bot, rleg_x + leg_w, torso_bot + leg_h],
                       fill=COSMO_PANTS, outline=COSMO_OUTLINE, width=1)

        # Feet
        foot_h = int(head_h * 0.12)
        foot_w = int(head_w * 0.28)
        draw.ellipse([lleg_x - 3, torso_bot + leg_h - 2,
                      lleg_x + foot_w, torso_bot + leg_h + foot_h],
                     fill=(40, 35, 30), outline=COSMO_OUTLINE, width=1)
        draw.ellipse([rleg_x - 3, torso_bot + leg_h - 2,
                      rleg_x + foot_w, torso_bot + leg_h + foot_h],
                     fill=(40, 35, 30), outline=COSMO_OUTLINE, width=1)

    # Torso
    draw.rounded_rectangle([cx - torso_w // 2, torso_top, cx + torso_w // 2, torso_bot],
                            radius=int(torso_w * 0.12),
                            fill=COSMO_SHIRT, outline=COSMO_OUTLINE, width=2)

    # Collar detail
    draw.line([cx - 6, torso_top + 4, cx, torso_top + 14], fill=COSMO_OUTLINE, width=2)
    draw.line([cx + 6, torso_top + 4, cx, torso_top + 14], fill=COSMO_OUTLINE, width=2)

    # ── CROSSED ARMS (skeptical posture) ──────────────────────────────────
    arm_y   = torso_top + torso_h // 3
    arm_len = int(head_w * 0.55)
    arm_w   = max(4, int(head_w * 0.12))

    # Right arm crossing left (viewer's right to left)
    draw.line([cx + torso_w // 2, arm_y,
               cx - arm_len // 3, arm_y + 10],
              fill=COSMO_SHIRT, width=arm_w)
    draw.line([cx + torso_w // 2, arm_y,
               cx - arm_len // 3, arm_y + 10],
              fill=COSMO_OUTLINE, width=1)

    # Left arm crossing right (viewer's left to right)
    draw.line([cx - torso_w // 2, arm_y + 8,
               cx + arm_len // 3, arm_y + 18],
              fill=COSMO_SHIRT, width=arm_w)
    draw.line([cx - torso_w // 2, arm_y + 8,
               cx + arm_len // 3, arm_y + 18],
              fill=COSMO_OUTLINE, width=1)

    # Arm overlap block (center cross)
    arm_cross_w = int(head_w * 0.60)
    arm_cross_h = int(head_h * 0.18)
    draw.rectangle([cx - arm_cross_w // 2, arm_y,
                    cx + arm_cross_w // 2, arm_y + arm_cross_h],
                   fill=COSMO_SHIRT, outline=COSMO_OUTLINE, width=1)

    # Neck
    draw.rectangle([cx - int(head_w * 0.14), neck_top,
                    cx + int(head_w * 0.14), neck_bot],
                   fill=COSMO_SKIN, outline=COSMO_OUTLINE, width=1)

    # ── Head ────────────────────────────────────────────────────────────────
    corner_r = int(head_w * 0.12)
    draw.rounded_rectangle([cx - head_w // 2, head_top,
                             cx + head_w // 2, head_bot],
                            radius=corner_r,
                            fill=COSMO_SKIN, outline=COSMO_OUTLINE, width=2)

    # Hair (flat on top, very short)
    hair_h = int(head_h * 0.15)
    draw.rounded_rectangle([cx - head_w // 2 + 2, head_top - hair_h + 4,
                             cx + head_w // 2 - 2, head_top + hair_h],
                            radius=int(head_w * 0.10),
                            fill=COSMO_HAIR, outline=COSMO_OUTLINE, width=1)

    # Cowlick (top center, slight lean left)
    cow_x = cx - int(head_w * 0.10)
    cow_y = head_top - hair_h - 2
    draw.ellipse([cow_x - 4, cow_y - 5, cow_x + 4, cow_y + 5],
                 fill=COSMO_HAIR, outline=COSMO_OUTLINE, width=1)

    # ── SKEPTICAL EXPRESSION ────────────────────────────────────────────────
    # Glasses at 9° (more than neutral 7°)
    # We'll draw glasses slightly tilted by offsetting L vs R eye heights
    eye_y_base = cy - int(head_h * 0.05)
    lens_r     = int(head_w * 0.16)   # each lens radius (0.32 × head_w / 2)
    lens_sep   = int(head_w * 0.20)   # separation between lens centers
    frame_w    = max(3, int(head_w * 0.06))

    # 9° tilt: left lens (viewer) lower, right lens higher
    tilt_offset = int(head_w * 0.08)  # ~9° approximated by vertical offset

    # LEFT lens center (viewer's left = character's right)
    l_lx = cx - lens_sep
    l_ly = eye_y_base + tilt_offset // 2

    # RIGHT lens center (viewer's right = character's left)
    r_lx = cx + lens_sep
    r_ly = eye_y_base - tilt_offset // 2

    # Draw lenses (glass tint + frame)
    for lx, ly in [(l_lx, l_ly), (r_lx, r_ly)]:
        draw.ellipse([lx - lens_r, ly - lens_r, lx + lens_r, ly + lens_r],
                     fill=COSMO_LENS, outline=COSMO_GLASS, width=frame_w)
        # Glare highlight
        draw.arc([lx - lens_r + 3, ly - lens_r + 3,
                  lx - 4,         ly - 2],
                 start=210, end=300, fill=STATIC_WHITE, width=max(1, frame_w // 2))

    # Nose bridge
    draw.line([l_lx + lens_r, l_ly, r_lx - lens_r, r_ly],
              fill=COSMO_GLASS, width=frame_w)

    # ── EYES through lenses ──────────────────────────────────────────────────
    eye_r = int(lens_r * 0.55)
    for lx, ly in [(l_lx, l_ly), (r_lx, r_ly)]:
        draw.ellipse([lx - eye_r, ly - eye_r, lx + eye_r, ly + eye_r],
                     fill=(235, 215, 180))
        # Pupil
        p_r = max(2, eye_r // 2)
        draw.ellipse([lx - p_r, ly - p_r, lx + p_r, ly + p_r], fill=(20, 15, 10))
        # Highlight
        draw.rectangle([lx - p_r + 1, ly - p_r + 1,
                        lx - p_r + 3, ly - p_r + 3], fill=STATIC_WHITE)

    # ── SKEPTICAL BROWS ──────────────────────────────────────────────────────
    brow_thick = max(2, int(head_w * 0.06))

    # His LEFT brow = viewer's RIGHT (r_lx): RAISED high — the skeptical brow
    brow_raise = int(head_h * 0.12)  # significantly raised
    draw.arc([r_lx - lens_r, r_ly - lens_r - brow_raise - 4,
              r_lx + lens_r, r_ly - lens_r + 4 - brow_raise],
             start=200, end=340, fill=COSMO_HAIR, width=brow_thick)

    # His RIGHT brow = viewer's LEFT (l_lx): FLAT (skeptical asymmetry)
    flat_brow_y = l_ly - lens_r - 6
    draw.line([l_lx - lens_r + 4, flat_brow_y,
               l_lx + lens_r - 4, flat_brow_y],
              fill=COSMO_HAIR, width=brow_thick)

    # ── FLAT DEADPAN MOUTH ────────────────────────────────────────────────────
    mouth_y = cy + int(head_h * 0.22)
    mouth_w = int(head_w * 0.30)
    draw.line([cx - mouth_w // 2, mouth_y,
               cx + mouth_w // 2, mouth_y],
              fill=COSMO_OUTLINE, width=max(2, int(head_w * 0.04)))

    # Slight skeptical downturn at left corner
    draw.line([cx - mouth_w // 2, mouth_y,
               cx - mouth_w // 2 - 2, mouth_y + 3],
              fill=COSMO_OUTLINE, width=max(2, int(head_w * 0.03)))


# ═══════════════════════════════════════════════════════════════════════════════
#  PANEL A2-03 — Cosmo SKEPTICAL (wide/medium — wrong plan beat)
# ═══════════════════════════════════════════════════════════════════════════════

def draw_a203(img, draw, font, font_bold, font_cap, font_ann):
    """
    A2-03: Cosmo doesn't believe what he's hearing.
    Wide shot: Cosmo center-left, full body, arms crossed, skeptical expression.
    Cosmo's whiteboard (elaborate, color-coded plan) is visible background-right.
    Luma is partial background-right (partial frame).
    Tech den / warm amber environment.
    """
    rng = random.Random(2203)

    # ── Background: tech den (warm amber, daytime) ──────────────────────────
    draw.rectangle([0, 0, PW, DRAW_H], fill=TECH_DEN_WALL)

    # Floor
    floor_y = int(DRAW_H * 0.72)
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=TECH_DEN_FLR)
    draw.line([0, floor_y, PW, floor_y], fill=(55, 40, 24), width=2)

    # Ceiling
    draw.rectangle([0, 0, PW, 10], fill=(88, 68, 42))

    # ── Whiteboard (background right) — elaborate color-coded plan ──────────
    wb_x, wb_y = 290, 18
    wb_w, wb_h = 160, 110
    draw.rectangle([wb_x, wb_y, wb_x + wb_w, wb_y + wb_h],
                   fill=(245, 245, 240), outline=(80, 80, 80), width=3)

    # Board header
    draw.text((wb_x + 6, wb_y + 5), "THE PLAN v1.0", font=font_ann, fill=(40, 40, 40))
    draw.line([wb_x + 4, wb_y + 16, wb_x + wb_w - 4, wb_y + 16],
              fill=(80, 80, 80), width=1)

    # Color-coded plan steps (tiny, clearly elaborate)
    plan_items = [
        ((200, 60, 60),  "1. CARDBOARD TRAP"),
        ((60, 120, 200), "2. SIGNAL LURE (cans)"),
        ((60, 160, 80),  "3. GLITCH FREQ APP"),
        ((180, 80, 180), "4. CORRAL + CONTAIN"),
        ((200, 150, 40), "5. REPORT TO ALEX"),
    ]
    for i, (col, txt) in enumerate(plan_items):
        ty = wb_y + 22 + i * 16
        draw.rectangle([wb_x + 6, ty + 2, wb_x + 12, ty + 8], fill=col)
        draw.text((wb_x + 16, ty), txt, font=font_ann, fill=(30, 30, 30))

    # Whiteboard marker tray
    draw.rectangle([wb_x + 4, wb_y + wb_h - 6, wb_x + wb_w - 4, wb_y + wb_h - 1],
                   fill=(200, 195, 185), outline=(100, 100, 90), width=1)

    # Arrows connecting plan steps (visual busyness)
    for i in range(3):
        ay = wb_y + 28 + i * 16
        ax = wb_x + wb_w - 12
        draw.line([ax, ay, ax + 8, ay + 8], fill=(150, 150, 150), width=1)

    # ── Monitor wall (background left) — subtle glitch artifacts ────────────
    mon_x, mon_y = 18, 22
    mon_w, mon_h = 80, 60
    draw.rectangle([mon_x, mon_y, mon_x + mon_w, mon_y + mon_h],
                   fill=(20, 18, 24), outline=(60, 55, 50), width=3)
    # Screen glow — cyan contamination (glitch artifacts)
    for _ in range(4):
        mx = mon_x + rng.randint(4, mon_w - 4)
        my = mon_y + rng.randint(4, mon_h - 4)
        draw.rectangle([mx, my, mx + rng.randint(6, 18), my + rng.randint(3, 8)],
                       fill=(0, rng.randint(100, 200), rng.randint(180, 255)))
    # Pixel confetti near monitor
    pixel_confetti(draw, mon_x + mon_w // 2, mon_y + mon_h // 2,
                   30, 30, rng, n=8)

    # ── LUMA — background right (partial, blurred-impression) ───────────────
    # Luma at ~25% frame weight, right side, showing her enthusiasm
    luma_cx = 400
    luma_cy = floor_y - 50
    l_head_r = 18
    # Hair
    draw.ellipse([luma_cx - l_head_r - 8, luma_cy - l_head_r - 14,
                  luma_cx + l_head_r + 8, luma_cy - l_head_r + 6],
                 fill=(30, 20, 10))
    # Head
    draw.ellipse([luma_cx - l_head_r, luma_cy - l_head_r,
                  luma_cx + l_head_r, luma_cy + l_head_r],
                 fill=(190, 128, 82), outline=(40, 26, 12), width=1)
    # Enthusiastic arm raised (Luma gesturing toward whiteboard)
    draw.line([luma_cx - 12, luma_cy + 12, luma_cx - 35, luma_cy - 22],
              fill=(170, 100, 60), width=6)
    # Torso (partial)
    draw.rectangle([luma_cx - 16, luma_cy + 12, luma_cx + 16, luma_cy + 55],
                   fill=(155, 195, 175), outline=(38, 26, 12), width=1)

    # ── COSMO — center, full body, large, SKEPTICAL ──────────────────────────
    cosmo_cx = 195
    cosmo_cy = floor_y - 85

    # Head size: ~48px wide × 56px tall (readable at medium-wide scale)
    c_head_w = 52
    c_head_h = 60

    draw_cosmo_skeptical(draw, cosmo_cx, cosmo_cy, c_head_w, c_head_h, full_body=True)

    # Annotation: skeptical brow arrow + label
    draw.line([cosmo_cx + c_head_w // 2 + 14, cosmo_cy - c_head_h // 4,
               cosmo_cx + c_head_w // 2 + 4,  cosmo_cy - c_head_h // 4 + 2],
              fill=(220, 180, 40), width=2)
    draw.text((cosmo_cx + c_head_w // 2 + 16, cosmo_cy - c_head_h // 4 - 6),
              "SKEPTICAL brow", font=font_ann, fill=(220, 180, 40))

    # Annotation: crossed arms
    draw.text((cosmo_cx - c_head_w - 48, cosmo_cy + c_head_h // 4),
              "arms crossed", font=font_ann, fill=(180, 220, 180))

    # Annotation: glasses tilt 9°
    draw.text((cosmo_cx - c_head_w + 2, cosmo_cy - c_head_h // 2 - 20),
              "glasses ~9°", font=font_ann, fill=(200, 180, 150))

    # Sight-line: dotted from Cosmo toward whiteboard (he's ignoring it)
    for sx in range(cosmo_cx + c_head_w // 2 + 6, wb_x - 6, 12):
        draw.rectangle([sx, cosmo_cy - 8, sx + 6, cosmo_cy - 6],
                       fill=(180, 180, 100))

    # "NOT BUYING IT" annotation (thought space above Cosmo)
    draw.text((cosmo_cx - 36, cosmo_cy - c_head_h // 2 - 38),
              '"...not buying it."', font=font_cap, fill=(220, 220, 180))


# ═══════════════════════════════════════════════════════════════════════════════
#  PANEL A2-04 — Investigation montage (2×2 vignette grid)
# ═══════════════════════════════════════════════════════════════════════════════

def draw_a204(img, draw, font, font_bold, font_cap, font_ann):
    """
    A2-04: Montage panel — 2×2 grid of vignettes showing Luma investigating.
    Vignettes:
      TL — Luma searching the TV (kneeling, looking behind)
      TR — Luma looking under furniture (on hands and knees)
      BL — Luma examining the desk (leaning in, magnifying glass implied)
      BR — Luma finding a clue (holding up a small glowing object, excited)
    Light and energetic composition. Each vignette has a thin border and micro-caption.
    """
    rng = random.Random(2204)

    # ── Grid layout ─────────────────────────────────────────────────────────
    grid_margin = 6
    gutter      = 5
    cell_w = (PW - grid_margin * 2 - gutter) // 2
    cell_h = (DRAW_H - grid_margin * 2 - gutter) // 2

    # Cell positions (top-left corners)
    cells = {
        'TL': (grid_margin,           grid_margin),
        'TR': (grid_margin + cell_w + gutter, grid_margin),
        'BL': (grid_margin,           grid_margin + cell_h + gutter),
        'BR': (grid_margin + cell_w + gutter, grid_margin + cell_h + gutter),
    }

    # Draw overall background
    draw.rectangle([0, 0, PW, DRAW_H], fill=(35, 28, 20))

    # ── Draw cell backgrounds and borders ────────────────────────────────────
    cell_bgs = {
        'TL': (52, 38, 24),    # warm amber — near the TV
        'TR': (40, 32, 20),    # darker — under furniture shadow
        'BL': (48, 38, 28),    # desk area — amber
        'BR': (30, 24, 36),    # discovery — slightly cooler/purple (glitch contact)
    }
    for key, (cx, cy) in cells.items():
        draw.rectangle([cx, cy, cx + cell_w, cy + cell_h],
                       fill=cell_bgs[key], outline=(15, 12, 8), width=2)

    # ── Vignette labels ──────────────────────────────────────────────────────
    vignette_labels = {
        'TL': "search: TV",
        'TR': "search: under",
        'BL': "examine: desk",
        'BR': "CLUE FOUND",
    }

    # ── TL: Luma behind TV (searching) ───────────────────────────────────────
    cx_tl, cy_tl = cells['TL']
    # TV silhouette (old CRT style)
    tv_x = cx_tl + cell_w // 2 - 28
    tv_y = cy_tl + cell_h // 2 - 24
    draw.rectangle([tv_x, tv_y, tv_x + 52, tv_y + 42],
                   fill=(35, 30, 25), outline=(70, 65, 58), width=3)
    draw.rectangle([tv_x + 5, tv_y + 5, tv_x + 45, tv_y + 32],
                   fill=(15, 30, 40))
    # Screen slight cyan (glitch contamination)
    draw.rectangle([tv_x + 8, tv_y + 8, tv_x + 28, tv_y + 20],
                   fill=(0, 80, 100))
    # TV legs
    draw.line([tv_x + 12, tv_y + 42, tv_x + 12, tv_y + 50], fill=(60, 55, 45), width=4)
    draw.line([tv_x + 40, tv_y + 42, tv_x + 40, tv_y + 50], fill=(60, 55, 45), width=4)

    # Luma — peeking around left side of TV (head + hand visible)
    l_cx = tv_x - 10
    l_cy = cy_tl + cell_h // 2
    # Hair
    draw.ellipse([l_cx - 14, l_cy - 18, l_cx + 6, l_cy - 2],
                 fill=LUMA_HAIR)
    # Head
    draw.ellipse([l_cx - 10, l_cy - 14, l_cx + 8, l_cy + 4],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=1)
    # Wide curious eyes (two dots)
    draw.ellipse([l_cx - 5, l_cy - 8, l_cx - 1, l_cy - 4], fill=(30, 20, 10))
    draw.ellipse([l_cx + 1, l_cy - 8, l_cx + 5, l_cy - 4], fill=(30, 20, 10))
    # Hand gripping TV edge
    draw.ellipse([tv_x - 6, l_cy - 4, tv_x + 2, l_cy + 4],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=1)
    # Pixel confetti near TV screen
    pixel_confetti(draw, tv_x + 26, tv_y + 16, 18, 14, rng, n=6)

    # Label
    draw.text((cx_tl + 4, cy_tl + cell_h - 14), vignette_labels['TL'],
              font=font_ann, fill=(200, 190, 150))

    # ── TR: Luma under furniture ──────────────────────────────────────────────
    cx_tr, cy_tr = cells['TR']
    # Floor line
    floor_tr = cy_tr + cell_h * 2 // 3
    draw.rectangle([cx_tr, floor_tr, cx_tr + cell_w, cy_tr + cell_h],
                   fill=(55, 42, 28))
    draw.line([cx_tr, floor_tr, cx_tr + cell_w, floor_tr], fill=(40, 30, 18), width=2)

    # Couch leg (L) and coffee table leg (R)
    for leg_x in [cx_tr + 8, cx_tr + cell_w - 18]:
        draw.rectangle([leg_x, cy_tr + cell_h // 3, leg_x + 10, floor_tr + 2],
                       fill=(90, 70, 50), outline=(55, 42, 28), width=1)

    # Luma on hands and knees under furniture (side view)
    l_cx = cx_tr + cell_w // 2
    l_cy = floor_tr - 16
    # Body horizontal
    draw.ellipse([l_cx - 22, l_cy - 8, l_cx + 16, l_cy + 8],
                 fill=LUMA_PJ, outline=LUMA_OUTLINE, width=1)
    # Head (looking forward/down)
    draw.ellipse([l_cx + 8, l_cy - 16, l_cx + 30, l_cy + 2],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=1)
    # Hair
    draw.ellipse([l_cx + 8, l_cy - 26, l_cx + 28, l_cy - 12],
                 fill=LUMA_HAIR)
    # Eye dot
    draw.ellipse([l_cx + 20, l_cy - 11, l_cx + 24, l_cy - 7],
                 fill=(30, 20, 10))
    # Arms (reaching under)
    draw.line([l_cx + 22, l_cy - 4, l_cx + 42, l_cy + 8],
              fill=LUMA_SKIN, width=5)
    # Legs sticking out behind
    draw.line([l_cx - 18, l_cy + 4, l_cx - 36, l_cy + 18],
              fill=LUMA_PJ, width=5)
    draw.line([l_cx - 12, l_cy + 6, l_cx - 30, l_cy + 22],
              fill=LUMA_PJ, width=5)

    # Dust motes/darkness lines
    for _ in range(6):
        dx = cx_tr + rng.randint(8, cell_w - 8)
        dy = cy_tr + rng.randint(4, cell_h // 3)
        draw.line([dx, dy, dx + rng.randint(6, 18), dy], fill=(45, 35, 22), width=1)

    draw.text((cx_tr + 4, cy_tr + cell_h - 14), vignette_labels['TR'],
              font=font_ann, fill=(190, 180, 140))

    # ── BL: Luma at the desk, leaning in, examining ───────────────────────────
    cx_bl, cy_bl = cells['BL']
    floor_bl = cy_bl + cell_h * 2 // 3
    draw.rectangle([cx_bl, floor_bl, cx_bl + cell_w, cy_bl + cell_h],
                   fill=(60, 48, 32))
    draw.line([cx_bl, floor_bl, cx_bl + cell_w, floor_bl],
              fill=(45, 35, 22), width=2)

    # Desk surface
    desk_top = floor_bl - 30
    draw.rectangle([cx_bl + 4, desk_top, cx_bl + cell_w - 4, floor_bl],
                   fill=(100, 78, 50), outline=(70, 55, 35), width=1)

    # Items on desk: notebook, screwdriver, old connector
    draw.rectangle([cx_bl + 10, desk_top - 2, cx_bl + 30, desk_top + 3],
                   fill=(200, 180, 140))   # notebook
    draw.line([cx_bl + 35, desk_top - 8, cx_bl + 42, desk_top + 3],
              fill=(150, 140, 130), width=3)  # screwdriver

    # Luma leaning in (upper body visible, MCU-ish from waist up)
    l_cx = cx_bl + cell_w // 2 - 6
    l_cy = desk_top - 40
    # Torso (leaning forward)
    draw.rounded_rectangle([l_cx - 16, l_cy, l_cx + 16, l_cy + 30],
                            radius=6, fill=LUMA_PJ, outline=LUMA_OUTLINE, width=1)
    # Head (tilted forward / down)
    draw.ellipse([l_cx - 13, l_cy - 26, l_cx + 13, l_cy + 2],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=1)
    draw.ellipse([l_cx - 15, l_cy - 36, l_cx + 15, l_cy - 14],
                 fill=LUMA_HAIR)
    # Concentration expression — furrowed brow, narrowed eyes
    draw.arc([l_cx - 8, l_cy - 20, l_cx - 2, l_cy - 14],
             start=200, end=340, fill=LUMA_OUTLINE, width=2)   # left brow furrowed
    draw.arc([l_cx + 2, l_cy - 20, l_cx + 8, l_cy - 14],
             start=200, end=340, fill=LUMA_OUTLINE, width=2)   # right brow furrowed
    draw.ellipse([l_cx - 7, l_cy - 12, l_cx - 3, l_cy - 8],
                 fill=(30, 20, 10))   # left eye
    draw.ellipse([l_cx + 3, l_cy - 12, l_cx + 7, l_cy - 8],
                 fill=(30, 20, 10))   # right eye

    # Arm reaching toward desk
    draw.line([l_cx + 12, l_cy + 16, l_cx + 28, desk_top - 2],
              fill=LUMA_SKIN, width=6)
    # Hand blob
    draw.ellipse([l_cx + 24, desk_top - 8, l_cx + 34, desk_top + 2],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=1)

    # Implied magnifying glass (circle near hand)
    mg_cx = l_cx + 36
    mg_cy = desk_top - 4
    draw.ellipse([mg_cx - 8, mg_cy - 8, mg_cx + 8, mg_cy + 8],
                 outline=(170, 160, 140), width=2)
    draw.line([mg_cx + 5, mg_cy + 5, mg_cx + 12, mg_cy + 12],
              fill=(140, 130, 110), width=2)

    draw.text((cx_bl + 4, cy_bl + cell_h - 14), vignette_labels['BL'],
              font=font_ann, fill=(200, 190, 150))

    # ── BR: Luma FOUND A CLUE — excited, holding glowing object ──────────────
    cx_br, cy_br = cells['BR']
    # Background: slightly cooler/purple = glitch contact
    # (already set in cell_bgs['BR'])

    # Luma center, upper body, arm raised, triumphant
    l_cx = cx_br + cell_w // 2
    l_cy = cy_br + cell_h // 2 + 5
    # Body (excited, slight lean back from discovery)
    draw.rounded_rectangle([l_cx - 16, l_cy, l_cx + 16, l_cy + 28],
                            radius=6, fill=LUMA_PJ, outline=LUMA_OUTLINE, width=1)
    # Head
    draw.ellipse([l_cx - 14, l_cy - 28, l_cx + 14, l_cy + 2],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=1)
    # Big hair
    draw.ellipse([l_cx - 18, l_cy - 42, l_cx + 18, l_cy - 18],
                 fill=LUMA_HAIR)
    # Big excited eyes
    draw.ellipse([l_cx - 8, l_cy - 20, l_cx - 2, l_cy - 13],
                 fill=(235, 215, 180))
    draw.ellipse([l_cx + 2, l_cy - 20, l_cx + 8, l_cy - 13],
                 fill=(235, 215, 180))
    draw.ellipse([l_cx - 6, l_cy - 19, l_cx - 3, l_cy - 15],
                 fill=(30, 20, 10))
    draw.ellipse([l_cx + 3, l_cy - 19, l_cx + 6, l_cy - 15],
                 fill=(30, 20, 10))
    # Highlight dots
    draw.rectangle([l_cx - 6, l_cy - 19, l_cx - 5, l_cy - 18], fill=STATIC_WHITE)
    draw.rectangle([l_cx + 3, l_cy - 19, l_cx + 4, l_cy - 18], fill=STATIC_WHITE)
    # Open mouth (surprised excitement)
    draw.ellipse([l_cx - 5, l_cy - 10, l_cx + 5, l_cy - 4],
                 fill=(20, 14, 10))

    # Raised arm holding glowing object
    draw.line([l_cx + 12, l_cy + 4, l_cx + 28, l_cy - 28],
              fill=LUMA_SKIN, width=7)
    # Glowing clue object (small chip/pixel cluster)
    clue_cx = l_cx + 30
    clue_cy = l_cy - 34
    draw.rectangle([clue_cx - 6, clue_cy - 6, clue_cx + 6, clue_cy + 6],
                   fill=GLITCH_CYAN, outline=(0, 180, 200), width=2)
    draw.rectangle([clue_cx - 3, clue_cy - 3, clue_cx + 3, clue_cy + 3],
                   fill=GLYPH_BRIGHT)
    # Glow radiating from clue (manual rings — ADD light)
    add_glow(img, clue_cx + cx_br - (PW // 2 - cell_w // 2 - gutter // 2),
             clue_cy + cy_br - (DRAW_H // 2 - cell_h // 2 - gutter // 2),
             22, (0, 220, 240), steps=5, max_alpha=55)

    # Pixel confetti scatter (glitch contact from clue)
    pixel_confetti(draw, clue_cx + cx_br - (PW // 2 - cell_w // 2),
                   clue_cy + cy_br - (DRAW_H // 2 - cell_h // 2),
                   28, 28, rng, n=10)

    # "AHA!" annotation
    draw.text((l_cx - 12, l_cy - 50), "AHA!", font=font_bold, fill=(0, 230, 255))

    draw.text((cx_br + 4, cy_br + cell_h - 14), vignette_labels['BR'],
              font=font_ann, fill=(160, 240, 220))

    # ── Grid divider lines (subtle) ──────────────────────────────────────────
    mid_x = grid_margin + cell_w + gutter // 2
    mid_y = grid_margin + cell_h + gutter // 2
    draw.line([mid_x, grid_margin, mid_x, DRAW_H - grid_margin],
              fill=(20, 16, 12), width=gutter)
    draw.line([grid_margin, mid_y, PW - grid_margin, mid_y],
              fill=(20, 16, 12), width=gutter)

    # ── Overall montage label ─────────────────────────────────────────────────
    # (drawn last so it's on top)
    draw.text((PW // 2 - 45, 3), "MONTAGE — INVESTIGATION", font=font_ann, fill=(180, 170, 130))


# ═══════════════════════════════════════════════════════════════════════════════
#  PANEL A2-07 — BLOCKED PLACEHOLDER
# ═══════════════════════════════════════════════════════════════════════════════

def draw_a207_blocked(img, draw, font, font_bold, font_cap, font_ann):
    """
    A2-07: BLOCKED — awaiting Byte expression sheet v002 RESIGNED + cracked-eye glyph.
    Placeholder panel communicates the block state clearly.
    """
    # Background: dark with red hazard pattern
    draw.rectangle([0, 0, PW, DRAW_H], fill=BLOCKED_BG)

    # Hazard diagonal stripes
    stripe_w = 22
    for i in range(-DRAW_H // stripe_w, PW // stripe_w + 2):
        x0 = i * stripe_w * 2
        pts = [(x0, 0), (x0 + DRAW_H, DRAW_H),
               (x0 + DRAW_H + stripe_w, DRAW_H), (x0 + stripe_w, 0)]
        draw.polygon(pts, fill=(42, 24, 14))

    # Central block box
    bx, by, bw, bh = 60, 28, 360, 148
    draw.rectangle([bx, by, bx + bw, by + bh],
                   fill=(22, 16, 12), outline=BLOCKED_RED, width=3)

    # Block label
    draw.text((bx + bw // 2 - 60, by + 10), "PRODUCTION BLOCK",
              font=font_bold, fill=BLOCKED_RED)
    draw.line([bx + 10, by + 28, bx + bw - 10, by + 28],
              fill=BLOCKED_RED, width=1)

    # Shot description
    draw.text((bx + 12, by + 36), "A2-07: Byte Partial Confession ECU",
              font=font_cap, fill=(200, 190, 170))
    draw.text((bx + 12, by + 52), "Extreme close-up — Byte's face",
              font=font_ann, fill=(170, 160, 140))
    draw.text((bx + 12, by + 64), "Cracked eye PROMINENT",
              font=font_ann, fill=(170, 160, 140))
    draw.text((bx + 12, by + 76), "RESIGNED expression (not in sheet v001)",
              font=font_ann, fill=(170, 160, 140))

    draw.line([bx + 10, by + 88, bx + bw - 10, by + 88],
              fill=(80, 60, 50), width=1)

    # Block reason
    draw.text((bx + 12, by + 96), "BLOCKED ON:",
              font=font_bold, fill=BLOCKED_ORANGE)
    draw.text((bx + 12, by + 110),
              "  LTG_CHAR_byte_expression_sheet.png",
              font=font_ann, fill=(220, 160, 80))
    draw.text((bx + 12, by + 122),
              "  RESIGNED expression required",
              font=font_ann, fill=(200, 150, 60))
    draw.text((bx + 12, by + 134),
              "  cracked-eye glyph RESIGNED state needed",
              font=font_ann, fill=(200, 150, 60))

    # Byte silhouette (ghosted — can't draw yet)
    ghost_cx = bx + bw // 2
    ghost_cy = by + bh + 22
    # Ghost oval body
    draw.ellipse([ghost_cx - 35, ghost_cy - 30, ghost_cx + 35, ghost_cy + 30],
                 outline=(60, 55, 52), width=2)
    # Ghost eye slots (blocked)
    draw.rectangle([ghost_cx - 22, ghost_cy - 8, ghost_cx - 8, ghost_cy + 2],
                   outline=(70, 60, 55), width=1)
    draw.rectangle([ghost_cx + 8,  ghost_cy - 8, ghost_cx + 22, ghost_cy + 2],
                   outline=(70, 60, 55), width=1)
    # X over eyes
    draw.line([ghost_cx - 22, ghost_cy - 8, ghost_cx - 8, ghost_cy + 2],
              fill=(100, 50, 50), width=1)
    draw.line([ghost_cx - 8,  ghost_cy - 8, ghost_cx - 22, ghost_cy + 2],
              fill=(100, 50, 50), width=1)
    draw.line([ghost_cx + 8,  ghost_cy - 8, ghost_cx + 22, ghost_cy + 2],
              fill=(100, 50, 50), width=1)
    draw.line([ghost_cx + 22, ghost_cy - 8, ghost_cx + 8,  ghost_cy + 2],
              fill=(100, 50, 50), width=1)
    # "?" label
    draw.text((ghost_cx - 6, ghost_cy - 14), "?", font=font_bold, fill=(80, 70, 60))

    # Staging note
    draw.text((bx + 12, by + bh + 8),
              "staging approx — awaiting byte_expression_sheet_v002 RESIGNED",
              font=font_ann, fill=(130, 120, 100))


# ═══════════════════════════════════════════════════════════════════════════════
#  CONTACT SHEET v002 — All Act 2 panels in sequence
# ═══════════════════════════════════════════════════════════════════════════════

def build_act2_contact_sheet_v002():
    """
    Build Act 2 contact sheet v002 — shows all Act 2 panels in sequence.
    Order: A1-04, A2-02, A2-03, A2-04, A2-05b, A2-06, A2-07
    Layout: horizontal strip (7 thumbnails, 2 rows × 4 + 3 arrangement or single row scaled)
    Output: /home/wipkat/team/output/storyboards/act2/LTG_SB_act2_contact_sheet.png
    """
    # Panels in sequence
    panel_files = [
        (PANELS_DIR + "/LTG_SB_act2_panel_a104.png",  "A1-04\nnear-miss"),
        (PANELS_DIR + "/LTG_SB_act2_panel_a202.png",  "A2-02\nByte MCU"),
        (PANELS_DIR + "/LTG_SB_act2_panel_a203.png",  "A2-03\nCosmo skeptic"),
        (PANELS_DIR + "/LTG_SB_act2_panel_a204.png",  "A2-04\nmontage"),
        (PANELS_DIR + "/LTG_SB_act2_panel_a205b.png", "A2-05b\nCosmo app"),
        (PANELS_DIR + "/LTG_SB_act2_panel_a206.png",  "A2-06\napp fail"),
        (PANELS_DIR + "/LTG_SB_act2_panel_a207.png",  "A2-07\nBLOCKED"),
    ]

    # Contact sheet: 2 rows, row1=4 panels, row2=3 panels
    # Thumbnail: 160×90 each (1/3 of original)
    thumb_w, thumb_h = 160, 90
    margin           = 10
    gutter           = 6
    label_h          = 22
    row1_count       = 4
    row2_count       = 3

    sheet_w = margin * 2 + thumb_w * row1_count + gutter * (row1_count - 1)
    sheet_h = (margin * 3
               + (thumb_h + label_h) * 2
               + gutter * 2
               + 30)  # header space

    sheet = Image.new('RGB', (sheet_w, sheet_h), (18, 14, 10))
    sd    = ImageDraw.Draw(sheet)
    font, font_bold, font_cap, font_ann = load_fonts()

    # Header
    sd.text((margin, 6), "ACT 2 CONTACT SHEET — Luma & the Glitchkin",
            font=font_cap, fill=(200, 190, 160))
    sd.text((sheet_w - 160, 6), "v002 — Cycle 15",
            font=font_ann, fill=(150, 140, 110))
    sd.line([margin, 22, sheet_w - margin, 22], fill=(50, 44, 36), width=1)

    # Arc labels (emotional temperature)
    arc_labels = ["NEAR-MISS", "VULNERABLE", "SKEPTICAL", "INVESTIGATING",
                  "DETERMINED", "FAILURE", "BLOCKED"]

    for idx, ((fpath, label), arc_lbl) in enumerate(zip(panel_files, arc_labels)):
        row = 0 if idx < row1_count else 1
        col = idx if row == 0 else idx - row1_count

        x = margin + col * (thumb_w + gutter)
        y = 28 + margin + row * (thumb_h + label_h + gutter + margin)

        # Load and resize panel
        try:
            pimg = Image.open(fpath).resize((thumb_w, thumb_h), Image.LANCZOS)
        except Exception:
            # Placeholder if file missing
            pimg = Image.new('RGB', (thumb_w, thumb_h), (40, 30, 22))
            pd   = ImageDraw.Draw(pimg)
            pd.text((8, 36), "PENDING", font=font_cap, fill=(150, 130, 100))

        sheet.paste(pimg, (x, y))

        # Border
        sd.rectangle([x - 1, y - 1, x + thumb_w, y + thumb_h],
                     outline=(50, 44, 36), width=1)

        # Label
        beat_id = label.split('\n')[0]
        beat_desc = label.split('\n')[1] if '\n' in label else ''
        sd.text((x + 2, y + thumb_h + 3), beat_id,
                font=font_ann, fill=(180, 170, 140))
        sd.text((x + 2, y + thumb_h + 12), beat_desc,
                font=font_ann, fill=(140, 130, 100))

        # Arc annotation
        arc_color = (220, 80, 40) if arc_lbl == "BLOCKED" else (120, 180, 140)
        sd.text((x + 2, y - 12), arc_lbl, font=font_ann, fill=arc_color)

    # Sequence connector arrows between rows
    for i in range(row1_count - 1):
        ax = margin + i * (thumb_w + gutter) + thumb_w + gutter // 2
        ay = 28 + margin + thumb_h // 2
        sd.line([ax - 3, ay, ax + 3, ay], fill=(80, 100, 80), width=2)
        # Arrow head
        sd.polygon([(ax + 3, ay - 3), (ax + 3, ay + 3), (ax + 7, ay)],
                   fill=(80, 100, 80))

    # Row 2 connector arrows
    for i in range(row2_count - 1):
        ax = margin + i * (thumb_w + gutter) + thumb_w + gutter // 2
        ay = 28 + margin * 2 + thumb_h + label_h + gutter + thumb_h // 2
        sd.line([ax - 3, ay, ax + 3, ay], fill=(80, 100, 80), width=2)
        sd.polygon([(ax + 3, ay - 3), (ax + 3, ay + 3), (ax + 7, ay)],
                   fill=(80, 100, 80))

    out_path = ACT2_SHEETS + "/LTG_SB_act2_contact_sheet.png"
    sheet.save(out_path)
    print(f"  Saved: LTG_SB_act2_contact_sheet.png")
    return sheet


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=== Act 2 Panels — Cycle 15 ===")
    print()

    # ── A2-03: Cosmo SKEPTICAL ───────────────────────────────────────────────
    print("Generating A2-03: Cosmo Skeptical...")
    path_a203 = PANELS_DIR + "/LTG_SB_act2_panel_a203.png"
    make_panel(
        path_a203,
        "A2-03 | MED-WIDE | COSMO SKEPTICAL",
        "Cosmo doesn't believe it. Arms crossed, one brow raised (SKEPTICAL). Glasses ~9°. staging approx — awaiting Byte expression sheet v002 RESIGNED",
        draw_a203,
        bg_color=(52, 38, 24),
    )

    # ── A2-04: Investigation montage ────────────────────────────────────────
    print("Generating A2-04: Investigation Montage...")
    path_a204 = PANELS_DIR + "/LTG_SB_act2_panel_a204.png"
    make_panel(
        path_a204,
        "A2-04 | MONTAGE 2×2 | LUMA INVESTIGATES",
        "Montage: TV search / under furniture / desk examination / clue found. Light and energetic.",
        draw_a204,
        bg_color=(35, 28, 20),
    )

    # ── A2-07: BLOCKED placeholder ──────────────────────────────────────────
    print("Generating A2-07: BLOCKED placeholder...")
    path_a207 = PANELS_DIR + "/LTG_SB_act2_panel_a207.png"
    make_panel(
        path_a207,
        "A2-07 | ECU | BLOCKED — awaiting byte_expression_sheet_v002",
        "BLOCKED: awaiting Byte expression sheet v002 RESIGNED + cracked-eye glyph design",
        draw_a207_blocked,
        bg_color=BLOCKED_BG,
    )

    # ── Copy files to act2/panels/ (canonical LTG naming) ───────────────────
    print()
    print("Copying to act2/panels/ with LTG naming...")

    # Also copy existing panels A2-02, A2-05b, A2-06 for the contact sheet
    copies = [
        (PANELS_DIR + "/LTG_SB_act2_panel_a202.png",
         ACT2_PANELS + "/LTG_SB_a2_02.png"),
        (path_a203, ACT2_PANELS + "/LTG_SB_a2_03.png"),
        (path_a204, ACT2_PANELS + "/LTG_SB_a2_04.png"),
        (PANELS_DIR + "/LTG_SB_act2_panel_a205b.png",
         ACT2_PANELS + "/LTG_SB_a2_05b.png"),
        (PANELS_DIR + "/LTG_SB_act2_panel_a206.png",
         ACT2_PANELS + "/LTG_SB_a2_06.png"),
        (path_a207, ACT2_PANELS + "/LTG_SB_a2_07.png"),
    ]

    for src, dst in copies:
        try:
            shutil.copy2(src, dst)
            print(f"  Copied: {os.path.basename(src)} -> {os.path.basename(dst)}")
        except Exception as e:
            print(f"  WARN: could not copy {os.path.basename(src)}: {e}")

    # ── Contact sheet v002 ───────────────────────────────────────────────────
    print()
    print("Building Act 2 contact sheet v002...")
    build_act2_contact_sheet_v002()

    print()
    print("=== Cycle 15 complete ===")
    print("  A2-03: Cosmo SKEPTICAL — DONE")
    print("  A2-04: Investigation montage — DONE")
    print("  A2-07: BLOCKED placeholder — DONE")
    print("  Contact sheet v002 — DONE")
    print()
    print("  STILL BLOCKED: A2-07 real panel")
    print("  DEPENDENCY: LTG_CHAR_byte_expression_sheet.png (RESIGNED)")
