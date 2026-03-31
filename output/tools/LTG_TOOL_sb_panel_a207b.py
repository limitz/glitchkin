#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_panel_a207b.py
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

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
from PIL import Image, ImageDraw, ImageFont
import random
import os
import sys
from LTG_TOOL_char_miri import draw_miri
from LTG_TOOL_cairo_primitives import to_pil_rgba
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ACT2_PANELS_DIR = output_dir('storyboards', 'act2', 'panels')
PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH     = os.path.join(ACT2_PANELS_DIR, "LTG_SB_act2_panel_a207b.png")

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





def _char_to_pil(surface):
    """Convert a cairo.ImageSurface from canonical char module to cropped PIL RGBA."""
    from LTG_TOOL_cairo_primitives import to_pil_rgba
    pil_img = to_pil_rgba(surface)
    bbox = pil_img.getbbox()
    if bbox:
        pil_img = pil_img.crop(bbox)
    return pil_img


def _composite_char(base_img, char_pil, cx, cy):
    """Composite a character PIL RGBA image onto base_img centered at (cx, cy)."""
    x = cx - char_pil.width // 2
    y = cy - char_pil.height // 2
    overlay = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    overlay.paste(char_pil, (x, y), char_pil)
    base_rgba = base_img.convert('RGBA')
    result = Image.alpha_composite(base_rgba, overlay)
    base_img.paste(result.convert('RGB'))

def draw_miri_silhouette(draw, img):
    """Miri silhouette in hallway — canonical renderer."""
    scale = 0.5
    surface = draw_miri(expression="KNOWING", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = 200
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    # Darken to silhouette
    r, g, b, a = char_pil.split()
    silhouette = Image.merge('RGBA', (
        r.point(lambda x: int(x * 0.15)),
        g.point(lambda x: int(x * 0.15)),
        b.point(lambda x: int(x * 0.15)),
        a
    ))
    miri_cx = int(PW * 0.50)
    miri_cy = int(DRAW_H * 0.55)
    _composite_char(img, silhouette, miri_cx, miri_cy)


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
    draw_miri_silhouette(draw, img)
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

    panels_path = os.path.join(PANELS_DIR, "LTG_SB_act2_panel_a207b.png")
    img.save(panels_path, "PNG")
    print(f"Also saved: {panels_path}")

    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("A2-07b panel generation complete (Cycle 19).")
