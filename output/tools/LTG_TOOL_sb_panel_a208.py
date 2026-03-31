#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
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

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
from PIL import Image, ImageDraw, ImageFont
import math
import random
import os
import sys
from LTG_TOOL_char_miri import draw_miri
from LTG_TOOL_cairo_primitives import to_pil_rgba
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ACT2_PANELS_DIR = output_dir('storyboards', 'act2', 'panels')
PANELS_DIR = output_dir('storyboards', 'panels')
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

# Character palette constants removed — canonical renderer handles its own palette.

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

def draw_miri_face(draw, img):
    """Miri face CU — canonical renderer."""
    scale = 1.5
    surface = draw_miri(expression="WARM", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(DRAW_H * 0.80)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    miri_cx = int(PW * 0.48)
    miri_cy = int(DRAW_H * 0.50)
    _composite_char(img, char_pil, miri_cx, miri_cy)


def make_panel():
    font_cap = load_font(12)
    font_ann = load_font(11)

    img  = Image.new('RGB', (PW, PH), BG_DARK)
    draw = ImageDraw.Draw(img)

    draw_background(draw, img)
    draw = ImageDraw.Draw(img)

    draw_miri_face(draw, img)
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
