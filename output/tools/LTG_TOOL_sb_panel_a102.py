#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
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

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
from PIL import Image, ImageDraw, ImageFont
import math, random, os
import sys
from LTG_TOOL_char_luma import draw_luma as _draw_luma_canonical
from LTG_TOOL_cairo_primitives import to_pil_rgba
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PANELS_DIR = output_dir('storyboards', 'panels')
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

# (Luma colors handled by canonical char_luma renderer)

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

def draw_luma(draw, img):
    """Luma — canonical renderer."""
    scale = 0.4
    surface = _draw_luma_canonical(expression="CURIOUS", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = 180
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    luma_cx = int(PW * 0.35)
    luma_cy = int(DRAW_H * 0.65)
    _composite_char(img, char_pil, luma_cx, luma_cy)


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
