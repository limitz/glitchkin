#!/usr/bin/env python3
"""
LTG_TOOL_sb_panel_a207b_v001.py
Storyboard Panel A2-07b — BRIDGING SHOT — Miri hears something
Lee Tanaka, Storyboard Artist

NEW PANEL — Cycle 19
Bridges A2-07 (Byte RESIGNED, glitch void) to A2-08 (Miri face, kitchen).
Two ECUs in different spaces needed a connection.

Beat: The kitchen door viewed from hallway/partial kitchen angle.
Miri's silhouette appears in doorway — she's heard something, stopped mid-motion.
She holds a tea towel (mid-chore, stopped).
Warm kitchen light behind her silhouette — amber glow frames her shape.
Her posture: head cocked, listening. Not alarmed — curious, knowing.
Caption: "Something is different tonight."

Camera: MEDIUM / eye-level / hallway POV
  → We are in the hallway looking toward the kitchen doorway
  → Miri's silhouette fills the doorway — backlit, dramatic
  → Warm amber kitchen light bleeds around her edges
  → We cannot see her face — only the silhouette and posture
  → Her head tilt says everything: she knows. She's listening.

Shot type: MEDIUM / eye-level / hallway POV
"""

from PIL import Image, ImageDraw, ImageFont
import random
import os

ACT2_PANELS_DIR = "/home/wipkat/team/output/storyboards/act2/panels"
PANELS_DIR      = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH     = os.path.join(ACT2_PANELS_DIR, "LTG_SB_act2_panel_a207b_v001.png")

os.makedirs(ACT2_PANELS_DIR, exist_ok=True)
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H   # 540px scene area

# ── Palette ──────────────────────────────────────────────────────────────────
BG_CAPTION   = (18, 14, 10)
TEXT_CAPTION = (235, 228, 210)
BORDER_COL   = (12, 8, 4)

# Hallway (very dark, nighttime)
HALLWAY_BG   = (18, 14, 10)
HALLWAY_WALL = (28, 22, 14)
HALLWAY_FLOOR= (24, 18, 12)

# Doorway (lit warm from kitchen behind)
DOORWAY_FILL = (220, 160, 80)   # bright warm amber
DOORWAY_MID  = (180, 130, 55)
KITCHEN_GLOW = (240, 195, 100)
KITCHEN_HOT  = (255, 210, 120)

# Door frame
FRAME_DARK   = (40, 30, 18)
FRAME_LIT    = (80, 60, 35)

# Miri silhouette (pure dark — backlit)
MIRI_SILHOUETTE = (25, 18, 12)
MIRI_RIM_EDGE   = (120, 88, 42)   # thin warm rim on silhouette edges

# Annotations
ANN_COL      = (200, 180, 120)
ANN_DIM      = (150, 135, 95)
CALLOUT_COL  = (220, 200, 140)


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
    """ADD light via alpha_composite."""
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_hallway_perspective(draw, img):
    """
    Hallway in single-point perspective toward doorway.
    Camera: eye-level, looking from hallway toward kitchen door.
    Vanishing point at center of doorway opening.
    """
    vp_x = PW // 2
    vp_y = int(DRAW_H * 0.42)   # vanishing point = doorway center

    # ── Hallway walls (single-point perspective) ──────────────────────────────
    # Left wall: upper-left corner → VP; lower-left corner → VP
    # Left wall face
    draw.polygon([
        (0, 0),
        (int(PW * 0.25), vp_y - int(DRAW_H * 0.20)),   # left wall top VP
        (int(PW * 0.25), vp_y + int(DRAW_H * 0.20)),   # left wall bot VP
        (0, DRAW_H),
    ], fill=HALLWAY_WALL, outline=HALLWAY_WALL)

    # Right wall face
    draw.polygon([
        (PW, 0),
        (int(PW * 0.75), vp_y - int(DRAW_H * 0.20)),
        (int(PW * 0.75), vp_y + int(DRAW_H * 0.20)),
        (PW, DRAW_H),
    ], fill=HALLWAY_WALL, outline=HALLWAY_WALL)

    # Ceiling (top)
    draw.polygon([
        (0, 0),
        (int(PW * 0.25), vp_y - int(DRAW_H * 0.20)),
        (int(PW * 0.75), vp_y - int(DRAW_H * 0.20)),
        (PW, 0),
    ], fill=(22, 16, 10), outline=(22, 16, 10))

    # Floor
    draw.polygon([
        (0, DRAW_H),
        (int(PW * 0.25), vp_y + int(DRAW_H * 0.20)),
        (int(PW * 0.75), vp_y + int(DRAW_H * 0.20)),
        (PW, DRAW_H),
    ], fill=HALLWAY_FLOOR, outline=HALLWAY_FLOOR)

    # ── Doorway opening (bright warm light from kitchen) ──────────────────────
    door_left  = int(PW * 0.28)
    door_right = int(PW * 0.72)
    door_top   = int(DRAW_H * 0.04)
    door_bot   = int(DRAW_H * 0.82)

    # Kitchen warm light fill (gradient via layered glow)
    draw.rectangle([door_left, door_top, door_right, door_bot],
                   fill=DOORWAY_FILL)

    # Bright hot center (overhead kitchen light)
    add_glow(img, vp_x, int(DRAW_H * 0.20), 200, KITCHEN_HOT, steps=8, max_alpha=70)
    add_glow(img, vp_x, int(DRAW_H * 0.30), 280, KITCHEN_GLOW, steps=8, max_alpha=55)

    # Kitchen interior suggestion (counter line, window hint)
    counter_y = int(DRAW_H * 0.58)
    draw.rectangle([door_left + 5, counter_y, door_right - 5, counter_y + 8],
                   fill=(190, 145, 72))
    # Window hint in BG
    win_left = int(PW * 0.40)
    win_right = int(PW * 0.60)
    win_top = int(DRAW_H * 0.15)
    win_bot = int(DRAW_H * 0.38)
    draw.rectangle([win_left, win_top, win_right, win_bot],
                   fill=(200, 180, 140), outline=(150, 115, 58), width=2)
    # Window cross
    draw.line([win_left, (win_top + win_bot) // 2,
               win_right, (win_top + win_bot) // 2],
              fill=(150, 115, 58), width=2)
    draw.line([(win_left + win_right) // 2, win_top,
               (win_left + win_right) // 2, win_bot],
              fill=(150, 115, 58), width=2)

    # ── Door frame ──────────────────────────────────────────────────────────
    frame_t = 14   # thickness
    # Top jamb
    draw.rectangle([door_left - frame_t, door_top - frame_t,
                    door_right + frame_t, door_top],
                   fill=FRAME_DARK, outline=FRAME_LIT, width=1)
    # Left jamb
    draw.rectangle([door_left - frame_t, door_top - frame_t,
                    door_left, door_bot],
                   fill=FRAME_DARK, outline=FRAME_LIT, width=1)
    # Right jamb
    draw.rectangle([door_right, door_top - frame_t,
                    door_right + frame_t, door_bot],
                   fill=FRAME_DARK, outline=FRAME_LIT, width=1)

    # Kitchen glow SPILL onto hallway walls (bleeds past doorway edges)
    add_glow(img, door_left, int(DRAW_H * 0.45), 120, DOORWAY_MID, steps=5, max_alpha=38)
    add_glow(img, door_right, int(DRAW_H * 0.45), 120, DOORWAY_MID, steps=5, max_alpha=38)
    add_glow(img, vp_x, door_bot, 150, DOORWAY_MID, steps=5, max_alpha=30)


def draw_miri_silhouette(draw, img):
    """
    Miri's silhouette in doorway — backlit.
    Standing center-doorway, MEDIUM shot (full or 3/4 body).
    Head COCKED (tilted right ~15°) — listening posture.
    Holding tea towel in one hand (arms slightly away from body).
    Pure dark silhouette — warm rim light traces her edges.
    """
    # Miri's body center in doorway
    sil_cx   = PW // 2
    sil_bot  = int(DRAW_H * 0.82)    # feet at bottom of doorway
    sil_h    = 260                    # full body height (MEDIUM shot)
    sil_top  = sil_bot - sil_h

    # Body proportions (older woman, sturdy build)
    head_r     = 30    # head radius
    neck_h     = 18
    torso_w    = 60
    torso_h    = 100
    hip_w      = 68
    leg_w      = 28
    leg_h      = 95

    # HEAD — cocked right (~15 degrees = head center shifted)
    head_cx = sil_cx + 12   # head leans right
    head_cy = sil_top + head_r

    # Draw silhouette from top to bottom
    # Head (slightly offset right = listening tilt)
    draw.ellipse([head_cx - head_r, head_cy - head_r,
                  head_cx + head_r, head_cy + head_r],
                 fill=MIRI_SILHOUETTE)

    # Hair volume (bun suggestion on top-left of head)
    draw.ellipse([head_cx - head_r - 8, head_cy - head_r - 10,
                  head_cx + head_r - 5, head_cy - head_r + 12],
                 fill=MIRI_SILHOUETTE)

    # Neck
    neck_top = head_cy + head_r - 5
    neck_bot = neck_top + neck_h
    draw.rectangle([sil_cx - 12, neck_top, sil_cx + 12, neck_bot],
                   fill=MIRI_SILHOUETTE)

    # Torso (upper body — slightly hunched forward, listening)
    torso_top = neck_bot - 5
    torso_bot = torso_top + torso_h
    draw.ellipse([sil_cx - torso_w // 2, torso_top,
                  sil_cx + torso_w // 2, torso_bot],
                 fill=MIRI_SILHOUETTE)

    # ── LEFT ARM — holding tea towel (drooping from hand) ─────────────────────
    # Left arm: extends slightly outward and down, towel hangs
    la_shoulder_x = sil_cx - torso_w // 2 + 8
    la_shoulder_y = torso_top + 20
    la_elbow_x    = la_shoulder_x - 22
    la_elbow_y    = la_shoulder_y + 45
    la_hand_x     = la_elbow_x - 10
    la_hand_y     = la_elbow_y + 35

    draw.line([la_shoulder_x, la_shoulder_y,
               la_elbow_x, la_elbow_y,
               la_hand_x, la_hand_y],
              fill=MIRI_SILHOUETTE, width=14)
    # Tea towel hanging from hand (rectangle slightly bent)
    towel_top_x  = la_hand_x - 6
    towel_top_y  = la_hand_y
    draw.polygon([
        (towel_top_x, towel_top_y),
        (towel_top_x + 22, towel_top_y),
        (towel_top_x + 20, towel_top_y + 50),
        (towel_top_x - 4, towel_top_y + 50),
    ], fill=MIRI_SILHOUETTE)

    # ── RIGHT ARM — raised slightly (stopped mid-motion) ──────────────────────
    ra_shoulder_x = sil_cx + torso_w // 2 - 8
    ra_shoulder_y = torso_top + 20
    ra_elbow_x    = ra_shoulder_x + 18
    ra_elbow_y    = ra_shoulder_y + 30
    ra_hand_x     = ra_elbow_x + 5
    ra_hand_y     = ra_elbow_y - 12

    draw.line([ra_shoulder_x, ra_shoulder_y,
               ra_elbow_x, ra_elbow_y,
               ra_hand_x, ra_hand_y],
              fill=MIRI_SILHOUETTE, width=14)
    # Hand blob
    draw.ellipse([ra_hand_x - 9, ra_hand_y - 9,
                  ra_hand_x + 9, ra_hand_y + 9],
                 fill=MIRI_SILHOUETTE)

    # ── Hips / skirt ──────────────────────────────────────────────────────────
    hip_top = torso_bot - 20
    hip_bot = hip_top + 50
    draw.ellipse([sil_cx - hip_w // 2, hip_top,
                  sil_cx + hip_w // 2, hip_bot],
                 fill=MIRI_SILHOUETTE)

    # ── Legs ──────────────────────────────────────────────────────────────────
    leg_top = hip_bot - 18
    # Left leg
    ll_cx = sil_cx - leg_w // 2 - 4
    draw.rectangle([ll_cx - leg_w // 2, leg_top,
                    ll_cx + leg_w // 2, sil_bot],
                   fill=MIRI_SILHOUETTE)
    # Right leg
    rl_cx = sil_cx + leg_w // 2 + 4
    draw.rectangle([rl_cx - leg_w // 2, leg_top,
                    rl_cx + leg_w // 2, sil_bot],
                   fill=MIRI_SILHOUETTE)

    # ── Rim light (warm amber edge — kitchen light wrapping around silhouette) ─
    # Thin bright edges on silhouette outline (ADD glow near edges)
    add_glow(img, head_cx - head_r, head_cy, 22, KITCHEN_GLOW, steps=3, max_alpha=45)
    add_glow(img, head_cx + head_r, head_cy, 22, KITCHEN_GLOW, steps=3, max_alpha=45)
    add_glow(img, sil_cx - torso_w // 2, torso_top + torso_h // 2,
             20, KITCHEN_GLOW, steps=3, max_alpha=40)
    add_glow(img, sil_cx + torso_w // 2, torso_top + torso_h // 2,
             20, KITCHEN_GLOW, steps=3, max_alpha=40)
    add_glow(img, la_hand_x, la_hand_y, 18, KITCHEN_GLOW, steps=3, max_alpha=35)

    return draw


def make_panel():
    font_cap = load_font(12)
    font_ann = load_font(11)
    font_b   = load_font(12, bold=True)

    img  = Image.new('RGB', (PW, PH), HALLWAY_BG)
    draw = ImageDraw.Draw(img)

    # Draw hallway perspective + doorway
    draw_hallway_perspective(draw, img)
    draw = ImageDraw.Draw(img)

    # Draw Miri silhouette in doorway
    draw = draw_miri_silhouette(draw, img)
    draw = ImageDraw.Draw(img)

    # ── Annotations ──────────────────────────────────────────────────────────
    draw.text((8, 8),
              "A2-07b  /  MEDIUM  /  eye-level  /  hallway POV",
              font=font_ann, fill=ANN_COL)
    draw.text((8, 20),
              "Bridging shot: A2-07 (Byte resigned) → A2-08 (Miri face)",
              font=font_ann, fill=ANN_DIM)

    # Miri posture callout
    draw.text((PW - 255, int(DRAW_H * 0.08)), "GRANDMA MIRI",
              font=font_ann, fill=(200, 220, 160))
    draw.text((PW - 255, int(DRAW_H * 0.08) + 12), "SILHOUETTE — backlit",
              font=font_ann, fill=(180, 200, 140))
    draw.text((PW - 255, int(DRAW_H * 0.08) + 24), "head cocked — LISTENING",
              font=font_ann, fill=ANN_DIM)
    draw.text((PW - 255, int(DRAW_H * 0.08) + 36), "tea towel in hand",
              font=font_ann, fill=ANN_DIM)
    draw.text((PW - 255, int(DRAW_H * 0.08) + 48), "stopped mid-motion",
              font=font_ann, fill=ANN_DIM)

    # Kitchen light callout
    draw.text((8, int(DRAW_H * 0.12)), "WARM KITCHEN LIGHT",
              font=font_ann, fill=(220, 185, 100))
    draw.text((8, int(DRAW_H * 0.12) + 12), "amber glow — frames her shape",
              font=font_ann, fill=(190, 160, 85))

    # Posture note
    draw.text((8, DRAW_H - 44), "posture: curious, not alarmed",
              font=font_ann, fill=ANN_DIM)
    draw.text((8, DRAW_H - 32), "she HAS heard things before",
              font=font_ann, fill=ANN_DIM)
    draw.text((8, DRAW_H - 20), "knowing stillness in the pause",
              font=font_ann, fill=ANN_DIM)

    # Bridge label
    draw.rectangle([8, DRAW_H - 58, 120, DRAW_H - 46], fill=(18, 14, 8))
    draw.text((12, DRAW_H - 56), "BRIDGE A2-07 → A2-08",
              font=font_ann, fill=(200, 180, 100))

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=BORDER_COL, width=2)
    draw.text((10, DRAW_H + 6),
              "A2-07b  MEDIUM  eye-level  hallway POV  |  new bridging shot",
              font=font_cap, fill=(160, 155, 130))
    draw.text((10, DRAW_H + 22),
              "Something is different tonight.  Miri hears something — stops mid-motion.  Head cocked, listening.",
              font=font_cap, fill=TEXT_CAPTION)
    draw.text((10, DRAW_H + 38),
              "Warm kitchen amber frames silhouette. Bridges RESIGNED (A2-07) → RECOGNITION (A2-08). Knowing stillness.",
              font=font_ann, fill=(150, 140, 110))
    draw.text((PW - 260, DRAW_H + 46), "LTG_SB_act2_panel_a207b_v001  |  Cycle 19",
              font=font_ann, fill=(100, 95, 78))

    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COL, width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")

    panels_path = os.path.join(PANELS_DIR, "LTG_SB_act2_panel_a207b_v001.png")
    img.save(panels_path, "PNG")
    print(f"Also saved: {panels_path}")

    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("A2-07b panel generation complete (Cycle 19).")
