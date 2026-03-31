#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_panel_a201.py
Storyboard Panel A2-01 — Tech Den Wide (Act 2 Opener) — Cycle 17
Lee Tanaka, Storyboard Artist

Beat: Act 2 opens in Cosmo's tech den. Wide establishing shot.
Cosmo at desk (BG, back/3-4 to camera, focused on monitor).
Luma in doorway (FG left edge, leaning in, DETERMINED).
Contrast: Cosmo's ordered world vs Luma's chaotic plan.

Camera: WIDE / slightly high-angle / neutral observer
  - 3/4 angle, slightly high — full room visible
  - Two-point perspective: room corner visible, floor plane recedes
  - Cosmo at back desk (BG, 3/4 turn), Luma FG-left doorway

Expression callouts:
  - Cosmo: FOCUSED (lean forward, screen glow on face)
  - Luma: DETERMINED (leaning in, chin up, confident stance)

Output:
  /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_act2_panel_a201.png
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
from LTG_TOOL_char_cosmo import draw_cosmo
from LTG_TOOL_char_luma import draw_luma as _draw_luma_canonical
from LTG_TOOL_cairo_primitives import to_pil_rgba
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ACT2_PANELS_DIR = output_dir('storyboards', 'act2', 'panels')
PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH     = os.path.join(ACT2_PANELS_DIR, "LTG_SB_act2_panel_a201.png")

os.makedirs(ACT2_PANELS_DIR, exist_ok=True)
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H   # 540px scene area

# ── Palette ──────────────────────────────────────────────────────────────────
BG_CAPTION   = (22, 18, 14)
TEXT_CAPTION = (235, 228, 210)
BORDER_COL   = (18, 12, 8)

# Room colors
WALL_BACK    = (105, 85, 58)     # warm amber back wall
WALL_SIDE    = (88, 70, 46)      # slightly darker side wall
FLOOR_COL    = (70, 52, 34)      # warm wood floor
CEILING_COL  = (80, 65, 42)      # ceiling

# Desk / equipment
DESK_COL     = (55, 44, 30)
DESK_SHADOW  = (42, 33, 22)
MONITOR_BEZ  = (30, 28, 30)
MONITOR_SCR  = (20, 100, 140)    # teal screen glow
MONITOR_GLOW = (0, 160, 200)
EQUIP_COL    = (50, 50, 60)

# (Cosmo colors handled by canonical char_cosmo renderer)
# (Luma colors handled by canonical char_luma renderer)

# Doorway
DOOR_FRAME   = (60, 48, 32)
DOOR_OPEN    = (180, 160, 130)   # warm hallway light spilling in

STATIC_WHITE = (240, 240, 240)
ANN_COL      = (220, 200, 130)
ANN_DIM      = (160, 145, 95)
CALLOUT_COL  = (100, 200, 180)


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


def draw_room(draw, img):
    """
    Two-point perspective: Tech Den interior.
    Slightly high-angle camera (horizon at 45% of DRAW_H).
    Wide shot — full room visible.
    VPs: VP-L off-canvas far left, VP-R off-canvas far right.
    """
    horizon_y = int(DRAW_H * 0.42)    # slightly high angle = horizon lower than center
    room_corner_x = int(PW * 0.52)    # room corner (wall edge) visible in center-right

    # Back-left wall (faces camera, lighter)
    back_wall_pts = [
        (0, 0),                         # top-left canvas
        (room_corner_x, 0),             # top of corner
        (room_corner_x, horizon_y + 20), # corner horizon
        (0, horizon_y + 80),            # left horizon
    ]
    draw.polygon(back_wall_pts, fill=WALL_BACK)

    # Back-right wall (angled away, darker)
    back_wall_r = [
        (room_corner_x, 0),
        (PW, 0),
        (PW, horizon_y + 60),
        (room_corner_x, horizon_y + 20),
    ]
    draw.polygon(back_wall_r, fill=WALL_SIDE)

    # Ceiling (top strip)
    draw.polygon([(0, 0), (PW, 0), (PW, int(DRAW_H * 0.08)), (0, int(DRAW_H * 0.08))],
                 fill=CEILING_COL)

    # Floor plane (recedes from camera)
    floor_pts = [
        (0, horizon_y + 80),
        (room_corner_x, horizon_y + 20),
        (PW, horizon_y + 60),
        (PW, DRAW_H),
        (0, DRAW_H),
    ]
    draw.polygon(floor_pts, fill=FLOOR_COL)

    # Room corner vertical line
    draw.line([room_corner_x, 0, room_corner_x, horizon_y + 20], fill=DOOR_FRAME, width=2)

    # Wall base (baseboard)
    draw.line([0, horizon_y + 78, room_corner_x, horizon_y + 18],
              fill=DESK_SHADOW, width=2)
    draw.line([room_corner_x, horizon_y + 18, PW, horizon_y + 58],
              fill=DESK_SHADOW, width=2)

    # Back wall equipment shelves (sketchy horizontal lines)
    rng = random.Random(201)
    for shelf_y_frac in [0.18, 0.28, 0.38]:
        sy = int(DRAW_H * shelf_y_frac)
        draw.line([int(PW * 0.12), sy, int(PW * 0.46), sy],
                  fill=DESK_SHADOW, width=2)
        # Shelf items (boxes, equipment)
        for bx in range(int(PW * 0.13), int(PW * 0.44), rng.randint(22, 38)):
            bh = rng.randint(12, 20)
            bw = rng.randint(14, 24)
            draw.rectangle([bx, sy - bh, bx + bw, sy], fill=EQUIP_COL, outline=DESK_SHADOW)

    return horizon_y


def draw_desk_and_monitor(draw, img):
    """
    Cosmo's desk — back right of room, with monitor glow.
    BG position: desk at ~55-80% x, ~50-90% y of DRAW_H.
    """
    # Desk (perspective-shortened since BG)
    desk_x1 = int(PW * 0.52)
    desk_x2 = int(PW * 0.88)
    desk_y_top = int(DRAW_H * 0.52)
    desk_y_bot = int(DRAW_H * 0.60)

    # Desk surface
    draw.polygon([
        (desk_x1, desk_y_top),
        (desk_x2, desk_y_top - 8),
        (desk_x2, desk_y_bot - 8),
        (desk_x1, desk_y_bot),
    ], fill=DESK_COL, outline=DESK_SHADOW)

    # Desk front face
    draw.polygon([
        (desk_x1, desk_y_bot),
        (desk_x2, desk_y_bot - 8),
        (desk_x2, DRAW_H - 30),
        (desk_x1, DRAW_H - 20),
    ], fill=DESK_SHADOW)

    # Monitor — on the desk
    mon_cx  = int(PW * 0.70)
    mon_cy  = int(DRAW_H * 0.38)
    mon_w   = 110
    mon_h   = 78

    # Monitor bezel
    draw.rectangle([mon_cx - mon_w // 2, mon_cy - mon_h // 2,
                    mon_cx + mon_w // 2, mon_cy + mon_h // 2],
                   fill=MONITOR_BEZ, outline=(18, 16, 18), width=3)
    # Screen (inset)
    scr_m = 8
    draw.rectangle([mon_cx - mon_w // 2 + scr_m, mon_cy - mon_h // 2 + scr_m,
                    mon_cx + mon_w // 2 - scr_m, mon_cy + mon_h // 2 - scr_m],
                   fill=MONITOR_SCR)

    # Screen content: code lines / data grid (FOCUSED state)
    rng = random.Random(2201)
    scr_left  = mon_cx - mon_w // 2 + scr_m + 3
    scr_top   = mon_cy - mon_h // 2 + scr_m + 3
    scr_right = mon_cx + mon_w // 2 - scr_m - 3
    scr_bot   = mon_cy + mon_h // 2 - scr_m - 3
    for line_y in range(scr_top + 4, scr_bot - 4, 8):
        lw = rng.randint(int((scr_right - scr_left) * 0.3),
                         int((scr_right - scr_left) * 0.9))
        lc = (rng.randint(80, 140), rng.randint(200, 255), rng.randint(180, 240))
        draw.line([scr_left + 2, line_y, scr_left + lw, line_y], fill=lc, width=1)

    # Monitor stand
    draw.rectangle([mon_cx - 8, mon_cy + mon_h // 2,
                    mon_cx + 8, desk_y_top],
                   fill=MONITOR_BEZ)
    draw.rectangle([mon_cx - 22, desk_y_top,
                    mon_cx + 22, desk_y_top + 5],
                   fill=MONITOR_BEZ)

    # Monitor glow (screen light spilling forward)
    add_glow(img, mon_cx, mon_cy, 55, (0, 160, 200), steps=5, max_alpha=30)

    return mon_cx, mon_cy, desk_y_top






def draw_annotations(draw, luma_cx, luma_lean, luma_head_cy,
                      cosmo_cx, cosmo_body_top, font_ann):
    """Shot type, character position, and expression callouts."""
    # Shot type
    draw.text((10, 8), "WIDE  /  slightly high-angle  /  neutral observer",
              font=font_ann, fill=ANN_COL)

    # Luma expression callout
    label_x = luma_cx + luma_lean + 42
    label_y = luma_head_cy - 20
    draw.line([luma_cx + luma_lean + 34, luma_head_cy - 8,
               label_x, label_y],
              fill=CALLOUT_COL, width=1)
    draw.text((label_x + 2, label_y - 5), "LUMA — DETERMINED", font=font_ann,
              fill=CALLOUT_COL)
    draw.text((label_x + 2, label_y + 5), "leaning into room", font=font_ann,
              fill=(140, 200, 170))

    # Cosmo expression callout
    cos_label_x = cosmo_cx + 80
    cos_label_y = cosmo_body_top - 10
    draw.line([cosmo_cx + 26, cosmo_body_top + 8,
               cos_label_x, cos_label_y],
              fill=(200, 220, 130), width=1)
    draw.text((cos_label_x + 2, cos_label_y - 5), "COSMO — FOCUSED",
              font=font_ann, fill=(200, 220, 130))
    draw.text((cos_label_x + 2, cos_label_y + 5), "back to camera",
              font=font_ann, fill=(150, 170, 95))

    # Depth labels
    draw.text((10, DRAW_H - 20), "FG: Luma", font=font_ann, fill=(220, 170, 100))
    draw.text((int(PW * 0.55), DRAW_H - 20), "BG: Cosmo + desk",
              font=font_ann, fill=(160, 150, 110))

    # Camera position callout
    draw.text((PW - 200, 8), "high-angle cam", font=font_ann, fill=ANN_DIM)
    draw.text((PW - 200, 18), "3/4 room view", font=font_ann, fill=ANN_DIM)



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

def draw_cosmo_bg(draw, img, mon_cx, desk_y_top):
    """Cosmo at desk — canonical renderer."""
    scale = 0.8
    surface, _geom = draw_cosmo(expression="SKEPTICAL", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    cosmo_cy = desk_y_top - 10
    if char_pil.height > 0:
        target_h = int(desk_y_top * 0.6)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
        cosmo_cy = desk_y_top - char_pil.height // 2 - 10
    _composite_char(img, char_pil, mon_cx, cosmo_cy)
    return mon_cx, cosmo_cy - char_pil.height // 2


def draw_doorway_and_luma(draw, img):
    """Luma in doorway — canonical renderer. Returns (draw, luma_cx, luma_lean, luma_head_cy)."""
    # Draw doorway frame
    door_cx = int(PW * 0.18)
    door_top = int(DRAW_H * 0.15)
    door_bottom = int(DRAW_H * 0.88)
    door_w = 80
    draw.rectangle([door_cx - door_w//2, door_top,
                    door_cx + door_w//2, door_bottom],
                   fill=(250, 240, 220), outline=(120, 100, 70), width=2)
    # Luma in doorway
    scale = 0.35
    surface = _draw_luma_canonical(expression="CURIOUS", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    luma_cy = door_bottom - 5
    if char_pil.height > 0:
        target_h = int((door_bottom - door_top) * 0.7)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
        luma_cy = door_bottom - char_pil.height // 2 - 5
    _composite_char(img, char_pil, door_cx, luma_cy)
    # Return values for annotation positioning
    luma_cx = door_cx
    luma_lean = 10  # slight lean into room
    luma_head_cy = luma_cy - char_pil.height // 2 + 10
    return draw, luma_cx, luma_lean, luma_head_cy


def make_panel():
    font      = load_font(14)
    font_bold = load_font(14, bold=True)
    font_cap  = load_font(12)
    font_ann  = load_font(11)

    img  = Image.new('RGB', (PW, PH), (105, 85, 58))
    draw = ImageDraw.Draw(img)

    # Draw scene
    horizon_y = draw_room(draw, img)
    draw = ImageDraw.Draw(img)

    mon_cx, mon_cy, desk_y_top = draw_desk_and_monitor(draw, img)
    draw = ImageDraw.Draw(img)

    cosmo_cx, cosmo_body_top = draw_cosmo_bg(draw, img, mon_cx, desk_y_top)
    draw = ImageDraw.Draw(img)

    draw, luma_cx, luma_lean, luma_head_cy = draw_doorway_and_luma(draw, img)
    draw = ImageDraw.Draw(img)

    draw_annotations(draw, luma_cx, luma_lean, luma_head_cy,
                     cosmo_cx, cosmo_body_top, font_ann)

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=BORDER_COL, width=2)
    draw.text((10, DRAW_H + 6), "A2-01  WIDE  slightly high-angle  neutral observer",
              font=font_cap, fill=(160, 155, 130))
    draw.text((10, DRAW_H + 22),
              "Tech Den establishing shot — Cosmo (BG, FOCUSED at monitor) / Luma (FG doorway, DETERMINED)",
              font=font_cap, fill=TEXT_CAPTION)
    draw.text((10, DRAW_H + 38),
              "Act 2 opener | full room visible | 3/4 angle | Cosmo's ordered world vs Luma's plan | monitor glow on Cosmo",
              font=font_ann, fill=(150, 140, 110))
    draw.text((PW - 200, DRAW_H + 46), "LTG_SB_act2_panel_a201_v001",
              font=font_ann, fill=(100, 95, 78))

    # Border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COL, width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")

    # Also save to main panels dir
    panels_path = os.path.join(PANELS_DIR, "LTG_SB_act2_panel_a201.png")
    img.save(panels_path, "PNG")
    print(f"Also saved: {panels_path}")

    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("A2-01 panel generation complete (Cycle 17).")
