#!/usr/bin/env python3
"""
LTG_TOOL_sb_panel_a201_v001.py
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
  /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_act2_panel_a201_v001.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

ACT2_PANELS_DIR = "/home/wipkat/team/output/storyboards/act2/panels"
PANELS_DIR      = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH     = os.path.join(ACT2_PANELS_DIR, "LTG_SB_act2_panel_a201_v001.png")

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

# Cosmo colors (background — slightly muted)
COSMO_SKIN   = (160, 112, 68)
COSMO_HAIR   = (14, 10, 6)
COSMO_SHIRT  = (70, 90, 160)
COSMO_PANTS  = (38, 52, 95)
COSMO_OUTLINE= (28, 18, 8)

# Luma colors (FG — brighter, warmer)
LUMA_SKIN    = (210, 142, 96)
LUMA_HAIR    = (22, 14, 8)
LUMA_JACKET  = (190, 80, 50)     # warm red jacket — stands out in doorway
LUMA_PANTS   = (60, 80, 120)
LUMA_OUTLINE = (42, 28, 14)

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


def draw_cosmo_bg(draw, img, mon_cx, desk_y_top):
    """
    Cosmo at desk — BG, back/3-4 to camera.
    Back of head visible, leaning forward toward monitor.
    Screen glow catching on face profile.
    FOCUSED state.
    """
    cx = int(PW * 0.62)
    seat_y = int(DRAW_H * 0.72)

    # BG scale — slightly smaller (depth reading)
    scale = 0.72

    head_r = int(22 * scale)
    body_w = int(50 * scale)
    body_h = int(70 * scale)

    # Body (3/4 back view — torso slightly angled toward monitor)
    body_cx = cx
    body_top = seat_y - body_h - head_r * 2 + 5

    draw.ellipse([body_cx - body_w // 2, body_top,
                  body_cx + body_w // 2, body_top + body_h],
                 fill=COSMO_SHIRT, outline=COSMO_OUTLINE, width=2)

    # Legs / seated lower body
    draw.ellipse([body_cx - body_w // 2 + 4, body_top + body_h - 10,
                  body_cx + body_w // 2 - 4, body_top + body_h + 20],
                 fill=COSMO_PANTS, outline=COSMO_OUTLINE, width=1)

    # Chair (simple back)
    chair_back_x = body_cx + body_w // 2 - 4
    draw.line([chair_back_x, body_top + 10, chair_back_x, seat_y + 10],
              fill=DESK_SHADOW, width=4)
    draw.line([chair_back_x - 20, body_top + 10, chair_back_x + 5, body_top + 10],
              fill=DESK_SHADOW, width=3)

    # Arms reaching forward toward keyboard/monitor (FOCUSED lean)
    # Left arm
    draw.line([body_cx - 18, body_top + 20,
               body_cx - 10, desk_y_top - 2],
              fill=COSMO_SKIN, width=int(9 * scale))
    # Right arm
    draw.line([body_cx + 18, body_top + 20,
               body_cx + 25, desk_y_top - 2],
              fill=COSMO_SKIN, width=int(9 * scale))

    # Head (back of head + slight profile glimpse — 3/4 away)
    head_cx = body_cx + int(5 * scale)
    head_cy = body_top - head_r + 2

    draw.ellipse([head_cx - head_r, head_cy - head_r,
                  head_cx + head_r, head_cy + head_r],
                 fill=COSMO_SKIN, outline=COSMO_OUTLINE, width=2)

    # Hair (back of head)
    draw.ellipse([head_cx - head_r, head_cy - head_r - 2,
                  head_cx + head_r, head_cy + 4],
                 fill=COSMO_HAIR)

    # Monitor glow on face/neck profile (side catch light)
    add_glow(img, head_cx - head_r + 2, head_cy, head_r + 8,
             (0, 160, 200), steps=4, max_alpha=40)

    return cx, body_top


def draw_doorway_and_luma(draw, img):
    """
    Doorway FG-left. Luma leaning in, DETERMINED.
    FG = larger scale, brighter color, partial crop at bottom.
    Warm hallway light from behind her.
    """
    # Doorway frame (left edge of frame)
    door_x1 = 0
    door_x2 = int(PW * 0.22)
    door_top = 0
    door_bot = DRAW_H

    # Hallway warm light behind door (warm amber)
    hall_layer = Image.new('RGBA', (PW, DRAW_H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hall_layer)
    # Warm light spilling from hallway
    for r in [140, 110, 80, 55]:
        alpha = max(6, 20 - r // 12)
        hd.ellipse([door_x1 - r, door_top + door_bot // 2 - r,
                    door_x1 + r, door_top + door_bot // 2 + r],
                   fill=(220, 175, 100, alpha))
    base = img.convert('RGBA')
    panel_area = base.crop((0, 0, PW, DRAW_H))
    merged = Image.alpha_composite(panel_area.convert('RGBA'), hall_layer)
    img.paste(merged.convert('RGB'), (0, 0))
    draw = ImageDraw.Draw(img)

    # Door frame (left edge + top)
    draw.rectangle([door_x2 - 8, door_top, door_x2, door_bot],
                   fill=DOOR_FRAME, outline=(40, 30, 20))
    draw.line([door_x2, door_top, door_x2, door_bot],
              fill=(30, 22, 14), width=3)

    # ── Luma — FG left, in doorway ─────────────────────────────────────────
    # FG = full size, partially cropped at bottom (doorway establishes depth)
    luma_cx = int(PW * 0.14)
    luma_base = int(DRAW_H * 1.05)   # body extends below frame = FG depth read

    head_r  = 36
    body_w  = 72
    body_h  = 110

    head_cy = luma_base - body_h - head_r - 4

    # Body (leaning in — torso angled slightly right into room)
    body_top = head_cy + head_r + 2
    lean_offset = 8   # lean into room
    draw.ellipse([luma_cx - body_w // 2 + lean_offset, body_top,
                  luma_cx + body_w // 2 + lean_offset, body_top + body_h],
                 fill=LUMA_JACKET, outline=LUMA_OUTLINE, width=2)

    # Arm (reaching into room or hand on doorframe — DETERMINED lean)
    # Right arm extended forward into room
    draw.line([luma_cx + body_w // 2 + lean_offset, body_top + 18,
               luma_cx + body_w // 2 + lean_offset + 45, body_top + 28],
              fill=LUMA_SKIN, width=10)
    # Hand blob
    draw.ellipse([luma_cx + body_w // 2 + lean_offset + 38, body_top + 22,
                  luma_cx + body_w // 2 + lean_offset + 54, body_top + 36],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=1)

    # Left arm on doorframe
    draw.line([luma_cx - body_w // 2 + lean_offset, body_top + 18,
               door_x2 - 4, body_top + 28],
              fill=LUMA_SKIN, width=10)

    # Head
    draw.ellipse([luma_cx - head_r + lean_offset, head_cy - head_r,
                  luma_cx + head_r + lean_offset, head_cy + head_r],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=2)

    # Hair
    draw.ellipse([luma_cx - head_r + lean_offset, head_cy - head_r - 2,
                  luma_cx + head_r + lean_offset, head_cy + 8],
                 fill=LUMA_HAIR)

    # DETERMINED expression: eyes forward, chin slightly down, brows set
    eye_y = head_cy - 4
    # Eyes — both open, forward-facing gaze toward Cosmo
    for ex_off in [-12, 12]:
        ex = luma_cx + lean_offset + ex_off
        draw.ellipse([ex - 7, eye_y - 5, ex + 7, eye_y + 5],
                     fill=STATIC_WHITE)
        draw.ellipse([ex - 4, eye_y - 3, ex + 4, eye_y + 3],
                     fill=(40, 60, 80))    # dark iris — looking toward Cosmo

    # Brows (set — determined, not raised/fearful — firm horizontal with slight inward angle)
    draw.line([luma_cx + lean_offset - 16, eye_y - 9,
               luma_cx + lean_offset - 4, eye_y - 8],
              fill=LUMA_HAIR, width=2)
    draw.line([luma_cx + lean_offset + 4, eye_y - 8,
               luma_cx + lean_offset + 16, eye_y - 9],
              fill=LUMA_HAIR, width=2)

    # Mouth (firm small smile — confidence)
    draw.arc([luma_cx + lean_offset - 8, head_cy + 5,
              luma_cx + lean_offset + 8, head_cy + 15],
             start=10, end=170, fill=LUMA_OUTLINE, width=2)

    # Door frame casting shadow over part of Luma (depth feel)
    shadow = Image.new('RGBA', (PW, DRAW_H), (0, 0, 0, 0))
    shdw = ImageDraw.Draw(shadow)
    shdw.rectangle([door_x2, 0, door_x2 + 12, DRAW_H], fill=(0, 0, 0, 40))
    base = img.convert('RGBA')
    panel_area = base.crop((0, 0, PW, DRAW_H))
    merged = Image.alpha_composite(panel_area.convert('RGBA'), shadow)
    img.paste(merged.convert('RGB'), (0, 0))
    draw = ImageDraw.Draw(img)

    return draw, luma_cx, lean_offset, head_cy


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
    panels_path = os.path.join(PANELS_DIR, "LTG_SB_act2_panel_a201_v001.png")
    img.save(panels_path, "PNG")
    print(f"Also saved: {panels_path}")

    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("A2-01 panel generation complete (Cycle 17).")
