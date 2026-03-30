# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_sb_panel_a203.py
Storyboard Panel A2-03 — Full Restage: Cosmo SKEPTICAL (Cycle 16)
Lee Tanaka, Storyboard Artist

Carmen Reyes critique notes (Cycle 8):
  - C grade: camera never established, whiteboard empty rectangle
  - "If I can't feel the scene, you haven't drawn it."
  - Camera spec MUST be explicit: shot type, eyeline, POV or neutral
  - Whiteboard is the THIRD CHARACTER — must be visually populated
  - 3D spatial clarity: Cosmo / Luma / whiteboard relationships clear

Panel requirements (Cycle 16):
  - CAMERA: Cowboy shot (thighs up), eye-level, neutral observer
    Camera position: LEFT of frame, looking right across the room
    Cosmo: left-center frame, facing viewer slightly (3/4 view)
    Luma: background right (smaller due to depth), facing whiteboard
    Whiteboard: center-right, behind/beside Luma
  - WHITEBOARD: "Doomed plan" — arrows, circles, question marks, Byte symbol,
    "???" — visually dense, obviously too complicated to work
  - 3D SPATIAL: floor plane with perspective, characters at different depths,
    relative scale communicates foreground/background
  - COSMO SKEPTICAL: one brow raised, arms crossed, glasses ~9° tilted,
    deadpan mouth, 5-8° backward torso lean

Annotations:
  - Camera height (eye-level), eyeline, spatial description
  - Character distances and positions

Output:
  /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a203.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_act2_panel_a203.png")

os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 480, 270
CAPTION_H = 48
DRAW_H    = PH - CAPTION_H   # 222px

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

TECH_WALL    = (108, 84, 54)    # warm amber den wall
TECH_WALL_BG = (88, 68, 42)     # slightly darker bg wall
TECH_FLOOR   = (72, 54, 36)     # warm hardwood floor
CEILING_COL  = (80, 62, 38)


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


def draw_perspective_room(draw):
    """
    Two-point perspective room.
    VP1 far left (off-canvas left), VP2 right-center.
    Camera is eye-level at ~0.65 of DRAW_H.
    Floor recedes; back wall faces camera.
    This makes 3D geometry explicit and animatable.
    """
    horizon_y = int(DRAW_H * 0.60)    # eye-level camera height

    # Back wall (full room)
    draw.rectangle([0, 0, PW, horizon_y + 12], fill=TECH_WALL_BG)

    # Floor (perspective trapezoid)
    floor_pts = [(0, horizon_y + 12), (PW, horizon_y + 12),
                 (PW, DRAW_H), (0, DRAW_H)]
    draw.polygon(floor_pts, fill=TECH_FLOOR)

    # Horizon/floor line
    draw.line([0, horizon_y + 12, PW, horizon_y + 12], fill=(55, 40, 24), width=2)

    # Ceiling line (top band)
    draw.rectangle([0, 0, PW, 12], fill=CEILING_COL)

    # Floor perspective lines (vanishing point right — creates depth)
    vp_x, vp_y = PW + 80, horizon_y + 12
    for start_y in [DRAW_H, DRAW_H - 25, DRAW_H - 50]:
        draw.line([(0, start_y), (vp_x, vp_y)],
                  fill=(62, 46, 28), width=1)

    # Back wall: subtle vertical planking / panel lines
    for wx in range(50, PW, 70):
        draw.line([(wx, 0), (wx, horizon_y + 12)], fill=(98, 78, 50), width=1)

    # Baseboard
    draw.rectangle([0, horizon_y + 8, PW, horizon_y + 20],
                   fill=(62, 46, 28), outline=(50, 38, 22), width=1)

    return horizon_y


def draw_monitor_bg(draw, rng):
    """Cosmo's monitor wall (background left) — establishes tech den context."""
    mon_x, mon_y = 14, 18
    mon_w, mon_h = 68, 52
    draw.rectangle([mon_x, mon_y, mon_x + mon_w, mon_y + mon_h],
                   fill=(20, 18, 24), outline=(60, 55, 50), width=3)
    # Screen: tech den idle display
    draw.rectangle([mon_x + 5, mon_y + 5, mon_x + mon_w - 5, mon_y + mon_h - 5],
                   fill=(14, 24, 32))
    # Glitch contamination lines on screen
    for _ in range(3):
        sx = mon_x + rng.randint(6, mon_w - 6)
        sy = mon_y + rng.randint(6, mon_h - 10)
        draw.rectangle([sx, sy, sx + rng.randint(8, 20), sy + rng.randint(2, 5)],
                       fill=(0, rng.randint(80, 160), rng.randint(160, 220)))
    # Monitor stand
    draw.rectangle([mon_x + mon_w // 2 - 5, mon_y + mon_h,
                    mon_x + mon_w // 2 + 5, mon_y + mon_h + 8],
                   fill=(50, 45, 40))


def draw_whiteboard_third_character(draw, font_ann, wb_x, wb_y, wb_w, wb_h):
    """
    Whiteboard: the THIRD CHARACTER in the scene.
    Visually populated with the doomed plan — arrows, circles, "???",
    Byte symbol, step numbers that obviously can't work together.
    This IS the scene's thesis object.
    """
    # Board body (white)
    draw.rectangle([wb_x, wb_y, wb_x + wb_w, wb_y + wb_h],
                   fill=(248, 248, 244), outline=(70, 65, 60), width=4)

    # Frame highlight
    draw.rectangle([wb_x + 2, wb_y + 2, wb_x + wb_w - 2, wb_y + wb_h - 2],
                   outline=(200, 195, 185), width=1)

    # Board title
    draw.text((wb_x + 4, wb_y + 4), "THE PLAN v4.7", font=font_ann,
              fill=(180, 20, 20))
    draw.line([wb_x + 3, wb_y + 15, wb_x + wb_w - 3, wb_y + 15],
              fill=(140, 140, 140), width=1)

    # ── Doomed plan elements ─────────────────────────────────────────────────
    # Step 1 — with red arrow
    draw.text((wb_x + 5, wb_y + 18), "1.CARDBOARD TRAP", font=font_ann,
              fill=(200, 40, 40))
    draw.line([wb_x + 5, wb_y + 28, wb_x + wb_w - 8, wb_y + 28],
              fill=(200, 40, 40), width=1)
    # Arrow from step 1 to step 2
    draw.line([wb_x + wb_w // 2, wb_y + 28,
               wb_x + wb_w // 2, wb_y + 34],
              fill=(180, 40, 40), width=2)
    draw.polygon([(wb_x + wb_w // 2 - 4, wb_y + 32),
                  (wb_x + wb_w // 2 + 4, wb_y + 32),
                  (wb_x + wb_w // 2, wb_y + 36)],
                 fill=(180, 40, 40))

    # Step 2 — blue
    draw.text((wb_x + 5, wb_y + 37), "2.SIGNAL LURE(cans)", font=font_ann,
              fill=(40, 60, 180))
    # Connecting circle around step 2 (emphasis it's complicated)
    draw.ellipse([wb_x + 3, wb_y + 35, wb_x + wb_w - 5, wb_y + 50],
                 outline=(40, 60, 180), width=1)

    # Arrow from step 2 to step 3 (goes sideways — spatially weird)
    draw.line([wb_x + wb_w - 6, wb_y + 43,
               wb_x + wb_w - 2, wb_y + 55],
              fill=(100, 160, 80), width=2)
    draw.polygon([(wb_x + wb_w - 6, wb_y + 53),
                  (wb_x + wb_w - 2, wb_y + 55),
                  (wb_x + wb_w - 1, wb_y + 50)],
                 fill=(100, 160, 80))

    # Step 3 — green
    draw.text((wb_x + 5, wb_y + 52), "3.GLITCH FREQ APP", font=font_ann,
              fill=(40, 140, 60))

    # Byte symbol (pixel icon) — referenced in plan
    byte_icon_x = wb_x + wb_w - 24
    byte_icon_y = wb_y + 52
    draw.rectangle([byte_icon_x, byte_icon_y, byte_icon_x + 14, byte_icon_y + 12],
                   fill=(0, 180, 200), outline=(0, 100, 120), width=1)
    draw.rectangle([byte_icon_x + 3, byte_icon_y + 3,
                    byte_icon_x + 11, byte_icon_y + 9],
                   fill=(0, 80, 100))
    # "BYTE?" label
    draw.text((byte_icon_x - 4, byte_icon_y + 13), "BYTE?", font=font_ann,
              fill=(0, 120, 140))

    # Step 4 — purple with large ??? making the whole thing seem impossible
    draw.text((wb_x + 5, wb_y + 67), "4.CORRAL+CONTAIN", font=font_ann,
              fill=(120, 40, 160))
    # Large ??? over step 4 (obviously doubted)
    draw.text((wb_x + wb_w - 28, wb_y + 65), "???", font=font_ann,
              fill=(200, 60, 60))

    # Step 5 — circled with red and crossed arrows (obviously won't work)
    draw.text((wb_x + 5, wb_y + 79), "5.SUCCESS!", font=font_ann,
              fill=(180, 50, 50))
    # Cross-out X over "SUCCESS!" line
    draw.line([wb_x + 3, wb_y + 79, wb_x + wb_w // 2, wb_y + 90],
              fill=(220, 40, 40), width=2)
    draw.line([wb_x + wb_w // 2, wb_y + 79, wb_x + 3, wb_y + 90],
              fill=(220, 40, 40), width=2)

    # Arrows connecting everything in a loop (circular logic — doom signal)
    # Big circle arrow across the full board
    draw.arc([wb_x + 8, wb_y + 20, wb_x + wb_w - 8, wb_y + wb_h - 15],
             start=0, end=300, fill=(160, 140, 60), width=1)
    # Arrowhead at end of loop
    draw.polygon([(wb_x + 18, wb_y + 17),
                  (wb_x + 10, wb_y + 24),
                  (wb_x + 22, wb_y + 26)],
                 fill=(160, 140, 60))

    # Big "???" diagonal stamp across lower half (the overall verdict)
    draw.text((wb_x + wb_w // 4, wb_y + wb_h - 28), "??? WHY", font=font_ann,
              fill=(160, 160, 80))

    # Marker tray at bottom of board
    draw.rectangle([wb_x + 4, wb_y + wb_h - 6,
                    wb_x + wb_w - 4, wb_y + wb_h - 1],
                   fill=(190, 185, 175), outline=(100, 95, 88), width=1)
    # Marker caps (color dots)
    for i, col in enumerate([(200, 40, 40), (40, 60, 180), (40, 140, 60), (120, 40, 160)]):
        draw.rectangle([wb_x + 8 + i * 18, wb_y + wb_h - 5,
                        wb_x + 16 + i * 18, wb_y + wb_h - 1],
                       fill=col)


def draw_luma_background(draw, horizon_y):
    """Luma in background right — smaller scale, facing whiteboard."""
    # Luma at background depth: ~20% frame weight, right area
    luma_cx = 375
    # At background depth, Luma stands behind the horizon slightly
    luma_floor = horizon_y + 10    # she's at background depth
    l_head_r = 14    # smaller — background depth
    l_body_h = 40

    # Hair
    draw.ellipse([luma_cx - l_head_r - 6, luma_floor - l_body_h - l_head_r * 2 - 8,
                  luma_cx + l_head_r + 6, luma_floor - l_body_h - l_head_r + 2],
                 fill=LUMA_HAIR)
    # Head
    draw.ellipse([luma_cx - l_head_r, luma_floor - l_body_h - l_head_r * 2,
                  luma_cx + l_head_r, luma_floor - l_body_h],
                 fill=(190, 128, 82), outline=(38, 26, 12), width=1)
    # Body (torso — she's turned slightly toward whiteboard)
    draw.rounded_rectangle([luma_cx - 12, luma_floor - l_body_h,
                             luma_cx + 12, luma_floor],
                            radius=5,
                            fill=(145, 188, 165), outline=(38, 26, 12), width=1)
    # Arm raised toward whiteboard (pointing at plan)
    draw.line([luma_cx + 10, luma_floor - l_body_h + 10,
               luma_cx + 32, luma_floor - l_body_h - 8],
              fill=(178, 118, 74), width=5)
    # Small eyes (background scale)
    draw.ellipse([luma_cx - 5, luma_floor - l_body_h - l_head_r - 6,
                  luma_cx - 1, luma_floor - l_body_h - l_head_r - 2],
                 fill=(30, 20, 10))
    draw.ellipse([luma_cx + 1, luma_floor - l_body_h - l_head_r - 6,
                  luma_cx + 5, luma_floor - l_body_h - l_head_r - 2],
                 fill=(30, 20, 10))
    # Feet (small at this depth)
    draw.ellipse([luma_cx - 10, luma_floor - 4, luma_cx, luma_floor + 4],
                 fill=(40, 30, 20))
    draw.ellipse([luma_cx + 2, luma_floor - 4, luma_cx + 12, luma_floor + 4],
                 fill=(40, 30, 20))


def draw_cosmo_foreground(draw, font_ann, horizon_y):
    """
    Cosmo foreground left — SKEPTICAL.
    Cowboy shot (thighs up), large, close to camera.
    3/4 view — faces viewer slightly while still looking at whiteboard.
    Slight backward torso lean (5-8°) = skeptical lean away from the plan.
    """
    cosmo_cx = 155
    # Cosmo at foreground depth — larger scale
    # Cowboy shot: visible from mid-thigh up
    cowboy_top = horizon_y - 130    # head starts here
    cowboy_bot = DRAW_H + 15        # cut off at thighs (below frame)

    head_w = 60
    head_h = 70
    head_cy = cowboy_top + head_h // 2 + 8

    # Body lean: slight backward tilt (~6°) — cosmo_cx shifts right with height
    # Simulate lean: body base slightly left of center, head slightly more left
    lean_offset = 6    # pixels — head leans back (left) relative to feet
    head_actual_cx = cosmo_cx - lean_offset

    # ── Thighs / legs (barely visible — cowboy shot) ─────────────────────
    leg_w = 22
    thigh_top = DRAW_H - 10
    # Left thigh
    draw.rectangle([cosmo_cx - 24, thigh_top, cosmo_cx - 2, DRAW_H + 15],
                   fill=COSMO_PANTS, outline=COSMO_OUTLINE, width=1)
    # Right thigh
    draw.rectangle([cosmo_cx + 2, thigh_top, cosmo_cx + 24, DRAW_H + 15],
                   fill=COSMO_PANTS, outline=COSMO_OUTLINE, width=1)

    # ── Torso (cowboy shot shows full torso) ──────────────────────────────
    torso_w = 68
    torso_h = 90
    torso_top = head_cy + head_h // 2 + 4
    torso_bot = torso_top + torso_h
    # Lean: torso base at cosmo_cx, top shifted left (lean_offset)
    torso_cx_top = cosmo_cx - lean_offset // 2
    torso_cx_bot = cosmo_cx

    # Draw trapezoid-ish torso (slight lean)
    torso_pts = [
        (torso_cx_top - torso_w // 2, torso_top),
        (torso_cx_top + torso_w // 2, torso_top),
        (torso_cx_bot + torso_w // 2 + 2, torso_bot),
        (torso_cx_bot - torso_w // 2 - 2, torso_bot),
    ]
    draw.polygon(torso_pts, fill=COSMO_SHIRT)
    draw.polygon(torso_pts, outline=COSMO_OUTLINE, fill=None)

    # Collar V
    draw.line([torso_cx_top - 7, torso_top + 5, torso_cx_top, torso_top + 18],
              fill=COSMO_OUTLINE, width=2)
    draw.line([torso_cx_top + 7, torso_top + 5, torso_cx_top, torso_top + 18],
              fill=COSMO_OUTLINE, width=2)

    # Neck
    draw.rectangle([head_actual_cx - 9, head_cy + head_h // 2,
                    head_actual_cx + 9, torso_top + 2],
                   fill=COSMO_SKIN, outline=COSMO_OUTLINE, width=1)

    # ── CROSSED ARMS (skeptical posture) ──────────────────────────────────
    arm_y    = torso_top + 22
    arm_w    = int(torso_w * 0.55)

    # Right arm crossing over left (viewer's right to left)
    draw.line([torso_cx_top + torso_w // 2, arm_y,
               torso_cx_top - arm_w // 3, arm_y + 12],
              fill=COSMO_SHIRT, width=16)
    draw.line([torso_cx_top + torso_w // 2, arm_y,
               torso_cx_top - arm_w // 3, arm_y + 12],
              fill=COSMO_OUTLINE, width=1)

    # Left arm crossing over right (viewer's left to right)
    draw.line([torso_cx_top - torso_w // 2, arm_y + 10,
               torso_cx_top + arm_w // 3, arm_y + 22],
              fill=COSMO_SHIRT, width=16)
    draw.line([torso_cx_top - torso_w // 2, arm_y + 10,
               torso_cx_top + arm_w // 3, arm_y + 22],
              fill=COSMO_OUTLINE, width=1)

    # Cross-body fill (center of crossed arms)
    cross_w = int(torso_w * 0.85)
    cross_h = 28
    draw.rectangle([torso_cx_top - cross_w // 2, arm_y,
                    torso_cx_top + cross_w // 2, arm_y + cross_h],
                   fill=COSMO_SHIRT, outline=COSMO_OUTLINE, width=1)

    # ── Head ──────────────────────────────────────────────────────────────
    corner_r = int(head_w * 0.12)
    draw.rounded_rectangle([head_actual_cx - head_w // 2, head_cy - head_h // 2,
                             head_actual_cx + head_w // 2, head_cy + head_h // 2],
                            radius=corner_r,
                            fill=COSMO_SKIN, outline=COSMO_OUTLINE, width=2)

    # Hair
    hair_h = int(head_h * 0.16)
    draw.rounded_rectangle([head_actual_cx - head_w // 2 + 2, head_cy - head_h // 2 - hair_h + 4,
                             head_actual_cx + head_w // 2 - 2, head_cy - head_h // 2 + hair_h],
                            radius=int(head_w * 0.10),
                            fill=COSMO_HAIR, outline=COSMO_OUTLINE, width=1)

    # Cowlick
    cow_x = head_actual_cx - int(head_w * 0.08)
    cow_y = head_cy - head_h // 2 - hair_h - 2
    draw.ellipse([cow_x - 5, cow_y - 6, cow_x + 5, cow_y + 6],
                 fill=COSMO_HAIR, outline=COSMO_OUTLINE, width=1)

    # ── SKEPTICAL EXPRESSION ─────────────────────────────────────────────
    eye_y_base = head_cy - int(head_h * 0.05)
    lens_r     = int(head_w * 0.17)
    lens_sep   = int(head_w * 0.22)
    frame_w    = max(3, int(head_w * 0.06))

    # 9° tilt: right lens (viewer's right = his LEFT) higher — the skeptical brow
    tilt_offset = int(head_w * 0.09)

    l_lx = head_actual_cx - lens_sep      # viewer's left lens
    l_ly = eye_y_base + tilt_offset // 2  # lower (tilted down)

    r_lx = head_actual_cx + lens_sep      # viewer's right lens (his left — RAISED)
    r_ly = eye_y_base - tilt_offset // 2  # higher (tilted up)

    # Draw lenses
    for lx, ly in [(l_lx, l_ly), (r_lx, r_ly)]:
        draw.ellipse([lx - lens_r, ly - lens_r, lx + lens_r, ly + lens_r],
                     fill=COSMO_LENS, outline=COSMO_GLASS, width=frame_w)
        # Glare highlight
        draw.arc([lx - lens_r + 3, ly - lens_r + 3,
                  lx - 4,          ly - 2],
                 start=210, end=300, fill=STATIC_WHITE, width=max(1, frame_w // 2))

    # Nose bridge
    draw.line([l_lx + lens_r, l_ly, r_lx - lens_r, r_ly],
              fill=COSMO_GLASS, width=frame_w)

    # Eyes through lenses
    eye_r = int(lens_r * 0.56)
    for lx, ly in [(l_lx, l_ly), (r_lx, r_ly)]:
        draw.ellipse([lx - eye_r, ly - eye_r, lx + eye_r, ly + eye_r],
                     fill=(235, 215, 180))
        p_r = max(2, eye_r // 2)
        draw.ellipse([lx - p_r, ly - p_r, lx + p_r, ly + p_r], fill=(20, 15, 10))
        draw.rectangle([lx - p_r + 1, ly - p_r + 1,
                        lx - p_r + 3, ly - p_r + 3], fill=STATIC_WHITE)

    # ── SKEPTICAL BROWS ─────────────────────────────────────────────────
    brow_thick = max(2, int(head_w * 0.06))

    # His LEFT brow = viewer's RIGHT (r_lx): RAISED — skeptical
    brow_raise = int(head_h * 0.13)
    draw.arc([r_lx - lens_r, r_ly - lens_r - brow_raise - 4,
              r_lx + lens_r, r_ly - lens_r + 4 - brow_raise],
             start=200, end=340, fill=COSMO_HAIR, width=brow_thick)

    # His RIGHT brow = viewer's LEFT (l_lx): FLAT
    flat_brow_y = l_ly - lens_r - 6
    draw.line([l_lx - lens_r + 4, flat_brow_y,
               l_lx + lens_r - 4, flat_brow_y],
              fill=COSMO_HAIR, width=brow_thick)

    # ── DEADPAN MOUTH ────────────────────────────────────────────────────
    mouth_y   = head_cy + int(head_h * 0.22)
    mouth_w   = int(head_w * 0.30)
    draw.line([head_actual_cx - mouth_w // 2, mouth_y,
               head_actual_cx + mouth_w // 2, mouth_y],
              fill=COSMO_OUTLINE, width=max(2, int(head_w * 0.04)))
    # Slight downturn left corner
    draw.line([head_actual_cx - mouth_w // 2, mouth_y,
               head_actual_cx - mouth_w // 2 - 3, mouth_y + 4],
              fill=COSMO_OUTLINE, width=max(2, int(head_w * 0.03)))

    # Return head position for annotations
    return head_actual_cx, head_cy, head_w, head_h, r_lx, r_ly, lens_r


def generate():
    font     = load_font(13)
    font_b   = load_font(13, bold=True)
    font_cap = load_font(11)
    font_ann = load_font(9)

    img  = Image.new('RGB', (PW, PH), TECH_WALL)
    draw = ImageDraw.Draw(img)

    rng = random.Random(2203)

    # ── Draw room ───────────────────────────────────────────────────────────
    horizon_y = draw_perspective_room(draw)

    # ── Monitor background (left) ───────────────────────────────────────────
    draw_monitor_bg(draw, rng)

    # ── Whiteboard (center-right) — THIRD CHARACTER ─────────────────────────
    wb_x  = 280
    wb_y  = 16
    wb_w  = 175
    wb_h  = 108
    draw_whiteboard_third_character(draw, font_ann, wb_x, wb_y, wb_w, wb_h)

    # ── Luma (background right) ─────────────────────────────────────────────
    draw_luma_background(draw, horizon_y)

    # ── Cosmo foreground SKEPTICAL ───────────────────────────────────────────
    (head_cx, head_cy, head_w, head_h,
     r_lx, r_ly, lens_r) = draw_cosmo_foreground(draw, font_ann, horizon_y)

    # ── CAMERA / SPATIAL ANNOTATIONS ────────────────────────────────────────
    # Camera label (top-left)
    draw.text((4, 2), "CAMERA: COWBOY | EYE-LEVEL | NEUTRAL OBS", font=font_ann,
              fill=(220, 200, 120))
    draw.text((4, 11), "Cosmo FG left  |  Luma BG right  |  WB center-right",
              font=font_ann, fill=(180, 165, 100))

    # Eyeline horizontal guide
    draw.line([0, horizon_y, PW, horizon_y], fill=(100, 180, 100), width=1)
    # Label eyeline
    draw.text((PW - 62, horizon_y + 2), "EYELINE", font=font_ann, fill=(100, 180, 100))

    # Depth labels
    draw.text((4, DRAW_H - 32), "FG: Cosmo", font=font_ann, fill=(200, 190, 150))
    draw.text((320, DRAW_H - 32), "BG: Luma", font=font_ann, fill=(160, 150, 110))

    # Skeptical brow annotation
    draw.line([r_lx + lens_r + 6, r_ly - lens_r - 10,
               r_lx + lens_r + 14, r_ly - lens_r - 14],
              fill=(240, 200, 60), width=2)
    draw.text((r_lx + lens_r + 16, r_ly - lens_r - 20),
              "SKEPTICAL↑", font=font_ann, fill=(240, 200, 60))

    # Backward lean indicator
    draw.text((head_cx + head_w // 2 + 8, head_cy + 20),
              "~6° lean", font=font_ann, fill=(180, 210, 180))
    draw.text((head_cx + head_w // 2 + 8, head_cy + 29),
              "backward", font=font_ann, fill=(180, 210, 180))

    # Thought line from Cosmo to whiteboard
    wb_center_x = wb_x + wb_w // 2
    wb_center_y = wb_y + wb_h // 2
    for sx in range(head_cx + head_w // 2 + 4, wb_x - 4, 12):
        draw.rectangle([sx, head_cy - 5, sx + 6, head_cy - 3],
                       fill=(180, 180, 100))
    # Sight-line label
    draw.text((head_cx + head_w // 2 + 20, head_cy - 16),
              '"...not buying it."', font=font_cap, fill=(230, 220, 170))

    # ── Caption bar ──────────────────────────────────────────────────────────
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=BORDER_COL, width=2)
    draw.text((8, DRAW_H + 6), "A2-03  COWBOY  eye-level  neutral observer",
              font=font_cap, fill=(160, 160, 160))
    draw.text((8, DRAW_H + 20),
              "Cosmo SKEPTICAL — arms crossed, brow up, 6° lean. Whiteboard = doomed plan (3rd character).",
              font=font_cap, fill=TEXT_CAPTION)
    draw.text((8, DRAW_H + 34),
              "Cosmo FG-left / Luma BG-right / Whiteboard center-right  |  3D depth established",
              font=font_ann, fill=(150, 140, 110))

    # Border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COL, width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    generate()
    print("A2-03 v002 restage generation complete (Cycle 16).")
