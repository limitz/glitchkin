#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_panel_a102.py
Storyboard Panel A1-02 — ARRIVAL — Luma enters kitchen — Cycle 18
Lee Tanaka, Storyboard Artist

Beat: Luma enters the kitchen. She spots the CRT TV in the adjacent room.
Something about the static catches her eye.

Shot: MEDIUM — Luma entering, TV BG
Camera: Eye-level, looking toward the kitchen/doorway corner.
        Luma FG-left entering through kitchen archway/hall.
        CRT TV visible in BG-right through doorway — glow on.

Luma expression: ALERT — she's stopped mid-step, head turning toward TV.
Body language: one foot in the air (mid-stride), head turned right (toward TV),
one hand raised slightly (reflexive — something caught her eye).

Arc: CURIOUS — first moment of noticing.
"""

from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_act1_panel_a102.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H

# ── Palette ─────────────────────────────────────────────────────────────────
WALL_WARM    = (240, 222, 188)
CEILING_WARM = (248, 238, 214)
FLOOR_LIGHT  = (212, 196, 162)
FLOOR_DARK   = (190, 174, 142)
WOOD_DARK    = (130,  85,  42)
WOOD_MED     = (168, 118,  62)
COUNTERTOP   = (200, 182, 148)
MORNING_GOLD = (255, 200,  80)
CURTAIN_WARM = (238, 198, 128)
LINE_DARK    = (100,  72,  40)
SHADOW_WARM  = (180, 152, 108)
DEEP_SHADOW  = (130,  98,  62)
CRT_CYAN     = (0, 220, 240)
CRT_CYAN_DIM = (0, 180, 200)

# Luma
LUMA_SKIN      = (242, 198, 152)   # warm skin
LUMA_HAIR      = (52,  32,  18)    # dark brown almost-black
LUMA_HOODIE    = (88, 158, 200)    # soft teal-blue jacket
LUMA_SHIRT     = (180, 220, 200)   # pale mint
LUMA_PANTS     = (88, 102, 130)    # dusty blue jeans
LUMA_SHOE      = (60,  48,  36)    # dark sneaker
LUMA_OUTLINE   = (52,  30,  10)
LUMA_EYE       = (62,  40,  18)

BG_CAPTION   = (22, 18, 14)
TEXT_CAP     = (235, 228, 210)
ANN_COL      = (200, 175, 120)
ANN_DIM      = (150, 135, 100)
CALLOUT_LUMA = (220, 200, 140)
SIGHT_LINE   = (0, 200, 220)


def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()


def add_glow(img, cx, cy, r_max, color_rgb, steps=6, max_alpha=50):
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_background(draw, img):
    """Kitchen interior BG — simplified, eye-level view toward doorway."""
    # Base wall
    draw.rectangle([0, 0, PW, DRAW_H], fill=WALL_WARM)

    # Ceiling
    draw.rectangle([0, 0, PW, int(DRAW_H * 0.24)], fill=CEILING_WARM)
    draw.line([(0, int(DRAW_H * 0.24)), (PW, int(DRAW_H * 0.24))], fill=SHADOW_WARM, width=2)

    # Morning sunlight from off-frame right (window in previous panel)
    add_glow(img, int(PW * 0.85), int(DRAW_H * 0.20), 180, MORNING_GOLD, steps=6, max_alpha=22)

    # Floor
    floor_y = int(DRAW_H * 0.73)
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=FLOOR_LIGHT)
    for c in range(12):
        for r in range(3):
            fx0 = int(c * PW / 12)
            fx1 = int((c + 1) * PW / 12)
            fy0 = int(floor_y + r * (DRAW_H - floor_y) / 3)
            fy1 = int(floor_y + (r + 1) * (DRAW_H - floor_y) / 3)
            if (r + c) % 2 == 0:
                draw.rectangle([fx0, fy0, fx1, fy1], fill=FLOOR_LIGHT)
            else:
                draw.rectangle([fx0, fy0, fx1, fy1], fill=FLOOR_DARK)
    draw.line([(0, floor_y), (PW, floor_y)], fill=SHADOW_WARM, width=2)

    # BG wall: right-side with doorway opening
    # Doorway BG-right — leads to adjacent room with CRT TV
    door_left  = int(PW * 0.62)
    door_right = int(PW * 0.82)
    door_top   = int(DRAW_H * 0.24)
    door_bot   = floor_y
    draw.rectangle([door_left, door_top, door_right, door_bot], fill=(38, 30, 20))
    # Doorframe
    draw.rectangle([door_left - 6, door_top - 2, door_left + 2, door_bot],
                   fill=WOOD_DARK, outline=LINE_DARK, width=1)
    draw.rectangle([door_right - 2, door_top - 2, door_right + 6, door_bot],
                   fill=WOOD_DARK, outline=LINE_DARK, width=1)
    draw.rectangle([door_left - 6, door_top - 4, door_right + 6, door_top + 2],
                   fill=WOOD_DARK, outline=LINE_DARK, width=1)

    # CRT TV through doorway — BG plane
    tv_x  = int(PW * 0.71)
    tv_y  = int(DRAW_H * 0.38)
    tv_w  = 48
    tv_h  = 38
    draw.rectangle([tv_x - tv_w // 2, tv_y, tv_x + tv_w // 2, tv_y + tv_h],
                   fill=(58, 50, 40), outline=(75, 65, 52), width=2)
    # Screen — static glow
    draw.rectangle([tv_x - tv_w // 2 + 5, tv_y + 5,
                    tv_x + tv_w // 2 - 5, tv_y + tv_h - 5],
                   fill=(95, 108, 98))
    add_glow(img, tv_x, tv_y + tv_h // 2, 52, CRT_CYAN, steps=5, max_alpha=40)

    # CRT glow bleeding through doorway into kitchen
    add_glow(img, door_left + 5, int(DRAW_H * 0.55), 75, CRT_CYAN_DIM, steps=4, max_alpha=20)

    # BG countertop (right of doorway)
    draw.rectangle([door_right + 5, int(DRAW_H * 0.56), PW, int(DRAW_H * 0.60)],
                   fill=COUNTERTOP, outline=LINE_DARK, width=1)
    draw.rectangle([door_right + 5, int(DRAW_H * 0.60), PW, floor_y],
                   fill=WOOD_DARK)

    # FG left — kitchen entry archway
    # Archway pillar (suggests she's just entered from hall)
    draw.rectangle([0, int(DRAW_H * 0.24), int(PW * 0.06), floor_y],
                   fill=SHADOW_WARM, outline=LINE_DARK, width=1)

    return draw


def draw_luma(draw, img):
    """
    Luma — MEDIUM shot — entering kitchen, MID-STRIDE, head turned right toward TV.
    Pose: one foot raised (left foot mid-step), torso angled slightly right,
    right arm raising (reflexive — attention caught), left arm neutral.
    Expression: ALERT — wide eyes directed right, mouth slightly open (surprise forming).
    Position: FG-left to center-left of frame.
    """
    rng = random.Random(102)

    # Body center
    luma_cx = int(PW * 0.28)
    luma_fy = int(DRAW_H * 0.82)    # feet level
    luma_h  = int(DRAW_H * 0.58)    # ~3.5 heads tall (medium shot — full body)

    head_r  = int(luma_h * 0.14)    # head radius
    body_cy = luma_fy - int(luma_h * 0.38)    # body center y
    body_w  = int(head_r * 2.2)
    body_h  = int(luma_h * 0.32)

    head_cy = body_cy - body_h // 2 - head_r - 2
    head_cx = luma_cx + 6   # slight rightward lean (attention caught right)

    # ── Hair (volume cloud — dark, gravity-defying) ──────────────────────────
    # Hair fills large area above/around head
    draw.ellipse([head_cx - head_r - 18, head_cy - head_r - 22,
                  head_cx + head_r + 14, head_cy + head_r + 4],
                 fill=LUMA_HAIR)
    # Hair ringlets / wisps
    for hx, hy, hr in [(head_cx - head_r - 10, head_cy - head_r - 12, 7),
                        (head_cx + head_r + 6, head_cy - head_r - 8, 6),
                        (head_cx - head_r + 4, head_cy - head_r - 20, 8)]:
        draw.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=LUMA_HAIR)

    # ── Hoodie/body ──────────────────────────────────────────────────────────
    # Torso — slightly angled right (attention caught)
    torso_pts = [(luma_cx - body_w // 2 - 2, body_cy - body_h // 2),
                 (luma_cx + body_w // 2 + 4, body_cy - body_h // 2),
                 (luma_cx + body_w // 2 + 8, body_cy + body_h // 2),
                 (luma_cx - body_w // 2 + 2, body_cy + body_h // 2)]
    draw.polygon(torso_pts, fill=LUMA_HOODIE, outline=LUMA_OUTLINE)

    # Hoodie hood/collar
    draw.ellipse([luma_cx - body_w // 2, body_cy - body_h // 2 - 5,
                  luma_cx + body_w // 2 + 4, body_cy - body_h // 2 + 14],
                 fill=LUMA_HOODIE, outline=LUMA_OUTLINE)

    # Jeans (lower body)
    waist_y = body_cy + body_h // 2
    hip_w   = body_w + 6
    leg_h   = int(luma_h * 0.30)

    # Left leg (standing — weight on right foot)
    draw.polygon([(luma_cx - 4, waist_y),
                  (luma_cx + hip_w // 2 - 2, waist_y),
                  (luma_cx + hip_w // 2 - 2 + 4, luma_fy),
                  (luma_cx + 4, luma_fy)],
                 fill=LUMA_PANTS, outline=LUMA_OUTLINE)

    # Right leg — raised (mid-stride LEFT foot is raised, RIGHT foot on ground)
    # Left foot in the air (left leg raised and bent forward — walking)
    draw.polygon([(luma_cx - hip_w // 2, waist_y),
                  (luma_cx - 4, waist_y),
                  (luma_cx + 4, waist_y + int(leg_h * 0.7)),
                  (luma_cx - hip_w // 2 + 4, waist_y + int(leg_h * 0.7))],
                 fill=LUMA_PANTS, outline=LUMA_OUTLINE)
    # Lower leg angled forward (raised foot)
    foot_raise_x = luma_cx - hip_w // 2 + 16
    foot_raise_y = waist_y + int(leg_h * 0.85)
    draw.polygon([(luma_cx + 2, waist_y + int(leg_h * 0.7)),
                  (luma_cx - hip_w // 2 + 4, waist_y + int(leg_h * 0.7)),
                  (foot_raise_x - 8, foot_raise_y),
                  (foot_raise_x + 6, foot_raise_y)],
                 fill=LUMA_PANTS, outline=LUMA_OUTLINE)
    # Raised shoe
    draw.ellipse([foot_raise_x - 12, foot_raise_y - 5,
                  foot_raise_x + 12, foot_raise_y + 8],
                 fill=LUMA_SHOE, outline=LUMA_OUTLINE)

    # Right shoe (grounded)
    draw.ellipse([luma_cx + hip_w // 2 - 10, luma_fy - 5,
                  luma_cx + hip_w // 2 + 14, luma_fy + 8],
                 fill=LUMA_SHOE, outline=LUMA_OUTLINE)

    # ── Arms ─────────────────────────────────────────────────────────────────
    shoulder_y = body_cy - body_h // 4

    # Left arm (viewer's left) — natural hang, slightly forward from stride
    left_elbow = (luma_cx - body_w // 2 - 14, shoulder_y + 28)
    left_hand  = (luma_cx - body_w // 2 - 8, shoulder_y + 54)
    draw.line([(luma_cx - body_w // 2, shoulder_y),
               left_elbow, left_hand], fill=LUMA_HOODIE, width=12)
    draw.ellipse([left_hand[0] - 7, left_hand[1] - 6,
                  left_hand[0] + 7, left_hand[1] + 6], fill=LUMA_SKIN, outline=LUMA_OUTLINE)

    # Right arm (viewer's right) — RAISED reflexively (attention caught)
    # Elbow bent, hand raised to chest height (not fully up — just reflexive alert)
    right_shoulder = (luma_cx + body_w // 2 + 2, shoulder_y)
    right_elbow    = (luma_cx + body_w // 2 + 18, shoulder_y + 10)
    right_hand     = (luma_cx + body_w // 2 + 8, shoulder_y - 10)
    draw.line([right_shoulder, right_elbow], fill=LUMA_HOODIE, width=12)
    draw.line([right_elbow, right_hand], fill=LUMA_HOODIE, width=10)
    draw.ellipse([right_hand[0] - 7, right_hand[1] - 6,
                  right_hand[0] + 7, right_hand[1] + 6], fill=LUMA_SKIN, outline=LUMA_OUTLINE)

    # ── Head (turned right — toward TV) ──────────────────────────────────────
    draw.ellipse([head_cx - head_r, head_cy - head_r,
                  head_cx + head_r, head_cy + head_r],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=2)

    # Eyes — wide, looking RIGHT (toward TV)
    # Both eyes shifted right (head turning)
    eye_y   = head_cy - head_r // 5
    eye_w   = int(head_r * 0.52)
    eye_h   = int(head_r * 0.34)
    for side, ex_off in enumerate([int(head_r * 0.25), int(head_r * 0.70)]):
        ex = head_cx + ex_off - head_r // 3  # offset eyes right
        # Sclera
        draw.ellipse([ex - eye_w // 2, eye_y - eye_h // 2,
                      ex + eye_w // 2, eye_y + eye_h // 2],
                     fill=(245, 242, 235), outline=LUMA_OUTLINE, width=1)
        # Iris (looking right — pupil offset right)
        iris_r = int(eye_h * 0.42)
        iris_x = ex + 3  # gaze direction: right
        draw.ellipse([iris_x - iris_r, eye_y - iris_r,
                      iris_x + iris_r, eye_y + iris_r],
                     fill=LUMA_EYE)
        # Pupil
        draw.ellipse([iris_x - iris_r + 2, eye_y - iris_r + 2,
                      iris_x + iris_r - 2, eye_y + iris_r - 2],
                     fill=(18, 12, 6))
        # Highlight
        draw.ellipse([iris_x + 1, eye_y - iris_r + 1,
                      iris_x + 5, eye_y - iris_r + 5], fill=(255, 255, 255))

    # Brows — raised (ALERT — attention caught)
    brow_y = eye_y - eye_h // 2 - 8
    for side, ex_off in enumerate([int(head_r * 0.25), int(head_r * 0.70)]):
        ex = head_cx + ex_off - head_r // 3
        draw.arc([ex - eye_w // 2, brow_y - 6, ex + eye_w // 2, brow_y + 4],
                 start=200, end=340, fill=LUMA_HAIR, width=2)

    # Mouth — slightly open (oh! moment)
    mouth_y = head_cy + head_r // 3
    draw.arc([head_cx - int(head_r * 0.30), mouth_y - 4,
              head_cx + int(head_r * 0.30), mouth_y + 10],
             start=10, end=170, fill=LUMA_OUTLINE, width=2)

    # Nose (minimal construction)
    draw.arc([head_cx - 6, head_cy + 2, head_cx + 6, head_cy + 14],
             start=240, end=300, fill=LUMA_OUTLINE, width=1)

    return draw


def draw_sight_line(draw, luma_head_cx, luma_head_cy, tv_cx, tv_cy):
    """Dotted cyan sight-line from Luma's eye to TV."""
    # Dotted line
    dx = tv_cx - luma_head_cx
    dy = tv_cy - luma_head_cy
    length = math.sqrt(dx * dx + dy * dy)
    steps = int(length / 10)
    for i in range(1, steps):
        frac = i / steps
        px = int(luma_head_cx + dx * frac)
        py = int(luma_head_cy + dy * frac)
        if i % 2 == 0:
            draw.rectangle([px - 2, py - 2, px + 2, py + 2], fill=SIGHT_LINE)


def make_panel():
    font_cap = load_font(12)
    font_ann = load_font(11)

    img  = Image.new('RGB', (PW, PH), WALL_WARM)
    draw = draw_background(ImageDraw.Draw(img), img)
    draw = ImageDraw.Draw(img)

    draw = draw_luma(draw, img)
    draw = ImageDraw.Draw(img)

    # Sight-line from Luma's gaze to TV
    luma_head_cx = int(PW * 0.28) + 6
    luma_head_cy = int(DRAW_H * 0.24)
    tv_cx = int(PW * 0.71)
    tv_cy = int(DRAW_H * 0.46)
    draw_sight_line(draw, luma_head_cx + int(0.10 * PW), luma_head_cy + int(0.10 * DRAW_H),
                    tv_cx, tv_cy)

    # Annotations
    font_ann = load_font(11)
    draw.text((10, 8), "A1-02  /  MEDIUM  /  eye-level  /  Luma entering, TV BG",
              font=font_ann, fill=ANN_COL)

    # Luma callout
    draw.text((int(PW * 0.06), int(DRAW_H * 0.14)), "LUMA",
              font=font_ann, fill=CALLOUT_LUMA)
    draw.text((int(PW * 0.06), int(DRAW_H * 0.14) + 10), "ALERT",
              font=font_ann, fill=(220, 200, 100))
    draw.text((int(PW * 0.06), int(DRAW_H * 0.14) + 20), "mid-stride → frozen",
              font=font_ann, fill=ANN_DIM)

    # TV callout
    draw.text((int(PW * 0.59), int(DRAW_H * 0.25)), "CRT TV",
              font=font_ann, fill=(0, 200, 220))
    draw.text((int(PW * 0.59), int(DRAW_H * 0.25) + 10), "static — something",
              font=font_ann, fill=(0, 175, 195))
    draw.text((int(PW * 0.59), int(DRAW_H * 0.25) + 20), "different in it",
              font=font_ann, fill=(0, 175, 195))

    # Gaze callout
    draw.text((int(PW * 0.36), int(DRAW_H * 0.28)), "→ gaze",
              font=font_ann, fill=SIGHT_LINE)

    # ARRIVAL label
    draw.rectangle([10, DRAW_H - 22, 90, DRAW_H - 5], fill=(50, 42, 30))
    draw.text((14, DRAW_H - 20), "ARRIVAL", font=font_ann, fill=(240, 220, 140))

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(18, 12, 8), width=2)
    draw.text((10, DRAW_H + 5), "A1-02  MEDIUM  eye-level  Luma entering kitchen — spots TV",
              font=font_cap, fill=(160, 155, 130))
    draw.text((10, DRAW_H + 20),
              "Luma enters kitchen. Mid-stride. Head turns right — CRT TV catches her eye.",
              font=font_cap, fill=(235, 228, 210))
    draw.text((10, DRAW_H + 36),
              "ARRIVAL beat. Expression: ALERT (not yet curious — instinctive freeze). Sight-line to TV.",
              font=font_ann, fill=(150, 140, 110))
    draw.text((PW - 240, DRAW_H + 46), "LTG_SB_act1_panel_a102_v001",
              font=font_ann, fill=(100, 95, 78))

    draw.rectangle([0, 0, PW - 1, PH - 1], outline=(18, 12, 8), width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("A1-02 panel generation complete (Cycle 18).")
