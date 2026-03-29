#!/usr/bin/env python3
"""
LTG_TOOL_luma_classroom_pose_v001.py
Luma Classroom Pose Generator — "Luma & the Glitchkin"

Cycle 14: Sitting-in-class pose for storyboard beat A1-04.
Beat description: Luma seated at desk, slight slouch, pen tapping desk,
head tilting toward blackboard. Near-miss moment — she's ALMOST connecting
the binary lesson to Byte.

Pose spec:
  - Body: seated (torso upright-ish, slight slouch)
  - Left arm: elbow on desk, hand supports chin lightly (distracted lean)
  - Right arm: extended forward, pen tip touching desk surface (tapping)
  - Head: slight rightward tilt (toward blackboard) — tilt_deg = 8°
  - Expression: AT-REST CURIOSITY — the near-miss expression
    (pupils shifted right toward blackboard, slight collar tilt, asymmetric mouth corner)

Output: LTG_CHAR_luma_classroom_pose_v001.png
Format: Single pose sheet — character on left, annotation panel on right.
Canvas: 900×560px

Character-over-background saturation rule: all character colors must
exceed BG saturation.
"""
from PIL import Image, ImageDraw, ImageFont
import math

# ── Palette — matches luma_expression_sheet canonical colors ─────────────────
SKIN        = (200, 136, 90)
SKIN_SH     = (168, 104, 56)
SKIN_HL     = (232, 184, 136)
HAIR        = (26, 15, 10)
EYE_W       = (255, 252, 245)
EYE_PUP     = (20, 12, 8)
EYE_IRIS    = (60, 38, 20)
LINE        = (59, 40, 32)
BLUSH       = (220, 100, 60, 120)
HOODIE_C    = (120, 155, 130)   # muted sage — At-Rest Curiosity hoodie
PANTS       = (60, 50, 80)      # dark indigo pants
SNEAKER     = (220, 220, 220)   # white sneakers

# Environment colors
DESK_TOP    = (180, 155, 120)   # warm wood desk surface
DESK_FRONT  = (148, 124, 90)    # desk front face
DESK_SHADOW = (120, 100, 70)    # under-desk shadow
PEN_BODY    = (200, 60, 80)     # red pen (pop of color)
PEN_TIP     = (40, 34, 28)      # dark pen tip

# Background — low saturation, warm classroom
BG_WARM     = (238, 228, 210)   # warm parchment (classroom wall)
BG_PANEL    = (248, 244, 236)   # annotation panel

CANVAS_BG   = (238, 228, 210)

# ── Canvas ────────────────────────────────────────────────────────────────────
CANVAS_W = 900
CANVAS_H = 560
CHAR_AREA_W = 520   # left portion for character
ANNO_AREA_X = 540   # annotation panel starts here


def _draw_luma_hair_seated(draw, cx, cy):
    """Cloud-top hair mass for seated Luma — same as expression sheet."""
    draw.ellipse([cx-155, cy-195, cx+145, cy+40],  fill=HAIR)
    draw.ellipse([cx-175, cy-170, cx-80,  cy-60],   fill=HAIR)
    draw.ellipse([cx-165, cy-140, cx-95,  cy-30],   fill=HAIR)
    draw.ellipse([cx+80,  cy-160, cx+155, cy-60],   fill=HAIR)
    draw.ellipse([cx+90,  cy-130, cx+145, cy-40],   fill=HAIR)
    draw.ellipse([cx-60,  cy-215, cx+20,  cy-140],  fill=HAIR)
    draw.ellipse([cx-20,  cy-225, cx+70,  cy-145],  fill=HAIR)
    draw.ellipse([cx-100, cy-200, cx-30,  cy-130],  fill=HAIR)


def _draw_luma_head(draw, cx, cy):
    """Luma's head — standard ellipse + cheek nubs. Same as expression sheet."""
    head_r = 100
    draw.ellipse([cx-head_r, cy-head_r, cx+head_r, cy+head_r+15],
                 fill=SKIN, outline=LINE, width=3)
    draw.ellipse([cx-95, cy-20, cx+95, cy+head_r+25], fill=SKIN)
    draw.arc([cx-95, cy-20, cx+95, cy+head_r+25], start=0, end=180, fill=LINE, width=3)
    draw.ellipse([cx-head_r-12, cy-20, cx-head_r+14, cy+20],
                 fill=SKIN, outline=LINE, width=2)
    draw.ellipse([cx+head_r-14, cy-20, cx+head_r+12, cy+20],
                 fill=SKIN, outline=LINE, width=2)


def _draw_hair_overlay(draw, cx, cy):
    """Foreground hair strands — same as expression sheet."""
    draw.arc([cx-60, cy-195, cx-10, cy-140], start=30,  end=200, fill=HAIR, width=8)
    draw.arc([cx-20, cy-190, cx+40, cy-130], start=10,  end=190, fill=HAIR, width=7)


def _draw_nose(draw, cx, cy):
    """Luma's nose."""
    draw.ellipse([cx-8, cy+8,  cx-2, cy+14], fill=SKIN_SH)
    draw.ellipse([cx+2, cy+8,  cx+8, cy+14], fill=SKIN_SH)
    draw.arc([cx-6, cy-10, cx+6, cy+12], start=200, end=340, fill=SKIN_SH, width=2)


def _draw_at_rest_curiosity_face(draw, cx, cy):
    """AT-REST CURIOSITY expression — three differentiators per Cycle 13 spec.

    From MEMORY.md Cycle 13 Lessons:
    1. Asymmetric mouth corner: right endpoint raised ~3px (one side rises)
    2. Slight collar tilt: rotate_deg=3 (body orienting toward object of interest)
    3. Left pupil offset: shifted to lex-3 (5px right of neutral lex-8 position)
       so gaze direction reads as curiosity / near-miss at panel scale

    For classroom pose: gaze shifts RIGHTWARD toward blackboard (pupils shift screen-right).
    Head tilt 8° rightward further reinforces the near-miss direction.
    """
    lex, ley = cx - 38, cy - 18
    rex, rey = cx + 38, cy - 18
    ew = 28

    # AT-REST CURIOSITY: eyes — leh=28 (lead left eye slightly more open), reh=22
    leh, reh = 28, 22

    # Left eye (lead eye — slightly more open per Cycle 13)
    draw.ellipse([lex-ew, ley-leh, lex+ew, ley+leh], fill=EYE_W, outline=LINE, width=2)
    iris_r = 15
    draw.chord([lex-iris_r, ley-iris_r+2, lex+iris_r, ley+iris_r+2],
               start=15, end=345, fill=EYE_IRIS)
    # Pupil shifted RIGHT (toward blackboard) — lex-3 = 5px right of neutral lex-8
    lex_pup = lex - 3
    draw.ellipse([lex_pup-9, ley-7, lex_pup+9, ley+9], fill=EYE_PUP)
    draw.ellipse([lex_pup+6, ley-9, lex_pup+13, ley-2], fill=(255, 252, 245))
    draw.arc([lex-ew, ley-leh, lex+ew, ley+leh], start=200, end=340, fill=LINE, width=4)

    # Right eye (slightly less open — reh=22)
    draw.ellipse([rex-ew, rey-reh, rex+ew, rey+reh], fill=EYE_W, outline=LINE, width=2)
    draw.chord([rex-iris_r, rey-iris_r+2, rex+iris_r, rey+iris_r+2],
               start=15, end=345, fill=EYE_IRIS)
    # Right pupil also shifted right (same direction as left — they track together)
    rex_pup = rex - 3
    draw.ellipse([rex_pup-9, rey-7, rex_pup+9, rey+9], fill=EYE_PUP)
    draw.ellipse([rex_pup+6, rey-9, rex_pup+13, rey-2], fill=(255, 252, 245))
    draw.arc([rex-ew, rey-reh, rex+ew, rey+reh], start=200, end=340, fill=LINE, width=4)

    # Brows — softly raised (curiosity, not worry) — nearly horizontal with slight arch
    l_brow = [(lex-26, ley-32), (lex+0, ley-38), (lex+22, ley-30)]
    draw.line(l_brow, fill=HAIR, width=5)
    r_brow = [(rex-22, rey-30), (rex+0, rey-38), (rex+26, rey-32)]
    draw.line(r_brow, fill=HAIR, width=5)

    _draw_nose(draw, cx, cy)

    # Mouth — asymmetric corner (right endpoint raised ~3px per Cycle 13)
    # "One side rises" is the differentiator from Neutral
    mouth_cx = cx
    mouth_l  = mouth_cx - 36
    mouth_r  = mouth_cx + 36
    mouth_y  = cy + 30
    # Draw via polyline with tilt: right side rises 3px
    n_pts = 20
    mouth_pts = []
    for i in range(n_pts + 1):
        t = i / n_pts
        # Arc base (gentle upward arc from neutral)
        angle = math.pi + t * math.pi   # 180° to 360° = bottom of ellipse
        arc_x = int(mouth_cx + 36 * math.cos(math.pi - t * math.pi))
        arc_y = int(mouth_y + 12 * math.sin(math.pi - t * math.pi) - 8)
        # Asymmetric tilt: right side rises 3px (tilt_x ratio 0=left, 1=right)
        tilt_amount = 3 * t
        arc_y -= int(tilt_amount)
        mouth_pts.append((arc_x, arc_y))
    if len(mouth_pts) > 1:
        draw.line(mouth_pts, fill=LINE, width=3)

    # Blush — curiosity warmth (subtle)
    draw.ellipse([cx-100+8, cy+5, cx-100+58, cy+35], fill=BLUSH + (80,) if len(BLUSH) == 3 else (220, 100, 60))
    draw.ellipse([cx+100-58, cy+5, cx+100-8, cy+35], fill=(220, 100, 60))


def _draw_collar_tilted(draw, cx, cy, rotate_deg=3):
    """Collar with slight tilt — rotate_deg=3 for AT-REST CURIOSITY per Cycle 13."""
    head_r = 100
    collar_cx = cx
    collar_cy = cy + head_r + 45
    rx, ry = 90, 35
    theta = math.radians(rotate_deg)
    cos_t, sin_t = math.cos(theta), math.sin(theta)

    def rot(x, y):
        return (int(collar_cx + x * cos_t - y * sin_t),
                int(collar_cy + x * sin_t + y * cos_t))

    N = 48
    full_pts = [rot(int(rx * math.cos(2 * math.pi * i / N)),
                    int(ry * math.sin(2 * math.pi * i / N))) for i in range(N)]
    draw.polygon(full_pts, fill=HOODIE_C)
    arc_pts = [rot(int(rx * math.cos(math.radians(a))),
                   int(ry * math.sin(math.radians(a)))) for a in range(180, 361, 5)]
    draw.line(arc_pts, fill=LINE, width=3)
    # Hoodie channel dots (cyan — consistent with expression sheet)
    for i in range(5):
        local_x = -35 + i * 17
        local_y = 8
        sq = [rot(local_x - 5, local_y - 4), rot(local_x + 5, local_y - 4),
              rot(local_x + 5, local_y + 4), rot(local_x - 5, local_y + 4)]
        draw.polygon(sq, fill=(0, 240, 255))


def draw_luma_seated(draw, cx, cy):
    """Draw full seated Luma pose.

    Pose:
    - Torso: seated, slight slouch forward (body_tilt=4)
    - Left arm: elbow on desk, forearm up, hand near chin (distracted lean)
    - Right arm: extended forward onto desk, pen in hand (tapping)
    - Legs: bent at 90°, only upper legs visible (below desk)
    - Head: 8° rightward tilt (toward blackboard — near-miss beat)

    cy is the face center. Desk surface at cy + ~290px.
    """
    head_r = 100

    # ── Desk environment (drawn first — behind character) ───────────────────
    desk_y   = cy + 295    # desk surface y
    desk_x1  = cx - 260
    desk_x2  = cx + 280
    desk_h   = 28

    # Desk shadow (cast downward)
    draw.rectangle([desk_x1 + 6, desk_y + desk_h,
                    desk_x2 + 6, desk_y + desk_h + 12],
                   fill=DESK_SHADOW)
    # Desk top surface
    draw.rectangle([desk_x1, desk_y, desk_x2, desk_y + desk_h],
                   fill=DESK_TOP, outline=LINE, width=2)
    # Desk front face
    draw.rectangle([desk_x1, desk_y + desk_h,
                    desk_x2, desk_y + desk_h + 40],
                   fill=DESK_FRONT, outline=LINE, width=2)
    # Wood grain lines (subtle)
    for gi in range(3):
        gy = desk_y + 8 + gi * 8
        draw.line([(desk_x1 + 20, gy), (desk_x2 - 20, gy)],
                  fill=DESK_SHADOW, width=1)

    # ── Luma body (torso + arms in seated position) ──────────────────────────
    hu = 140   # body height unit (same as expression sheet _draw_body)

    # Seated torso: shortened visible torso (hips at desk level)
    # Slight slouch: torso leaning forward slightly
    body_tilt = 4
    tilt_off  = int(body_tilt * 0.5)
    shoulder_w = int(hu * 0.52)
    # Visible torso only from shoulder to desk level
    torso_top_y = cy + head_r + 40
    torso_bot_y = desk_y + 2   # torso appears to sit behind desk

    hoodie_pts = [
        (cx - shoulder_w + tilt_off, torso_top_y),
        (cx + shoulder_w + tilt_off, torso_top_y),
        (cx + int(hu * 0.58),        torso_bot_y),
        (cx - int(hu * 0.58),        torso_bot_y),
    ]
    draw.polygon(hoodie_pts, fill=HOODIE_C, outline=LINE, width=3)

    # Hoodie seam arc
    seam_y = torso_top_y + int(hu * 0.22)
    draw.arc([cx - int(hu * 0.25), seam_y,
              cx + int(hu * 0.25), seam_y + int(hu * 0.18)],
             start=10, end=170, fill=LINE, width=2)

    # Pocket bump (left side — character-right, viewer-left)
    pocket_x = cx - int(hu * 0.50)
    pocket_y = torso_top_y + int(hu * 0.35)
    draw.ellipse([pocket_x, pocket_y,
                  pocket_x + int(hu * 0.22), pocket_y + int(hu * 0.26)],
                 fill=HOODIE_C, outline=LINE, width=2)

    arm_w = int(hu * 0.13)
    arm_y = torso_top_y + int(hu * 0.08)

    # ── Right arm (viewer's right = Luma's left) — pen tapping arm ───────────
    # Arm extends forward onto desk. Forearm resting on desk surface.
    # Right arm: dy = -15 (raised slightly — forward reaching, not draped)
    r_shoulder_x = cx + shoulder_w + tilt_off + int(hu * 0.05)
    r_arm_top_y  = arm_y - 15
    # Arm goes from shoulder down to desk level, angled forward
    r_arm_pts = [
        (r_shoulder_x,         r_arm_top_y),
        (r_shoulder_x + arm_w, r_arm_top_y),
        (cx + int(hu * 0.30),  desk_y - 4),
        (cx + int(hu * 0.12),  desk_y - 4),
    ]
    draw.polygon(r_arm_pts, fill=HOODIE_C, outline=LINE, width=2)

    # Hand (resting on desk)
    hand_cx = cx + int(hu * 0.20)
    hand_cy = desk_y
    draw.ellipse([hand_cx - 14, hand_cy - 10,
                  hand_cx + 18, hand_cy + 12],
                 fill=SKIN, outline=LINE, width=2)

    # Pen in right hand — body angled on desk, tip touching surface
    pen_x1 = hand_cx + 6
    pen_y1 = hand_cy - 8
    pen_x2 = pen_x1 + 40
    pen_y2 = pen_y1 + 6
    draw.line([(pen_x1, pen_y1), (pen_x2, pen_y2)], fill=PEN_BODY, width=5)
    # Pen tip
    draw.line([(pen_x2, pen_y2), (pen_x2 + 6, desk_y - 2)], fill=PEN_TIP, width=3)
    # Pen clip detail
    draw.line([(pen_x1 + 4, pen_y1 - 2), (pen_x1 + 10, pen_y2 + 4)],
              fill=(240, 240, 240), width=1)

    # ── Left arm (viewer's left = Luma's right) — elbow-on-desk lean ─────────
    # Elbow planted on desk, forearm raises, hand near chin.
    l_shoulder_x = cx - shoulder_w + tilt_off - int(hu * 0.05)
    l_arm_top_y  = arm_y

    # Upper arm (shoulder to elbow at desk)
    l_elbow_x = cx - int(hu * 0.25)
    l_elbow_y = desk_y - 2
    l_upper_pts = [
        (l_shoulder_x,          l_arm_top_y),
        (l_shoulder_x - arm_w,  l_arm_top_y + 10),
        (l_elbow_x - arm_w,     l_elbow_y),
        (l_elbow_x,             l_elbow_y),
    ]
    draw.polygon(l_upper_pts, fill=HOODIE_C, outline=LINE, width=2)

    # Forearm (elbow up to hand near chin) — raised, supports the lean
    l_hand_cx = cx - int(hu * 0.15)
    l_hand_cy = cy + head_r + 55   # near chin level
    l_fore_pts = [
        (l_elbow_x - arm_w, l_elbow_y),
        (l_elbow_x,         l_elbow_y),
        (l_hand_cx + 8,     l_hand_cy - 8),
        (l_hand_cx - 10,    l_hand_cy - 8),
    ]
    draw.polygon(l_fore_pts, fill=HOODIE_C, outline=LINE, width=2)
    # Left hand (cupped near chin — distracted lean support)
    draw.ellipse([l_hand_cx - 16, l_hand_cy - 14,
                  l_hand_cx + 14, l_hand_cy + 10],
                 fill=SKIN, outline=LINE, width=2)

    # ── Upper legs (only tops visible above desk) ────────────────────────────
    leg_w  = int(hu * 0.18)
    leg_l  = cx - int(hu * 0.35)
    leg_r  = cx + int(hu * 0.25)

    # Very slight hint of legs behind/below desk front
    draw.rectangle([leg_l - leg_w, desk_y + desk_h,
                    leg_l + leg_w, desk_y + desk_h + 30],
                   fill=PANTS, outline=LINE, width=1)
    draw.rectangle([leg_r - leg_w, desk_y + desk_h,
                    leg_r + leg_w, desk_y + desk_h + 30],
                   fill=PANTS, outline=LINE, width=1)

    # ── Head (drawn last — on top) ────────────────────────────────────────────
    # Head tilt 8° toward blackboard (rightward)
    # We simulate by drawing at slightly offset position (tilt approximation)
    head_tilt_x = 8   # px shift rightward at top of head = near-miss lean
    _draw_luma_hair_seated(draw, cx + head_tilt_x // 2, cy)
    _draw_luma_head(draw, cx, cy)
    _draw_at_rest_curiosity_face(draw, cx, cy)
    _draw_hair_overlay(draw, cx + head_tilt_x // 2, cy)
    _draw_collar_tilted(draw, cx, cy, rotate_deg=3)


def draw_annotation_panel(draw, x, y, w, h, font, font_sm):
    """Right-side annotation panel with pose callouts."""
    # Panel background
    draw.rectangle([x, y, x + w, y + h], fill=BG_PANEL, outline=(180, 168, 150), width=2)

    title_color  = (80, 56, 32)
    label_color  = (59, 40, 32)
    detail_color = (110, 90, 68)
    beat_color   = (60, 100, 80)

    annotations = [
        ("BEAT", "A1-04 — NEAR-MISS MICRO-BEAT",    beat_color,  True),
        ("",     "",                                  label_color, False),
        ("EXPR", "AT-REST CURIOSITY",                label_color, True),
        ("",     "eyes shift right (blackboard)",     detail_color, False),
        ("",     "asymm. mouth corner (right rises)", detail_color, False),
        ("",     "collar tilt 3° (orienting)",        detail_color, False),
        ("",     "",                                  label_color, False),
        ("POSE", "DISTRACTED LEAN",                  label_color, True),
        ("",     "left elbow on desk",                detail_color, False),
        ("",     "right hand tapping pen",            detail_color, False),
        ("",     "head tilt 8° right",                detail_color, False),
        ("",     "",                                  label_color, False),
        ("NOTE", "Byte is NOT shown here —",         label_color, True),
        ("",     "he is in the desk tray pocket",    detail_color, False),
        ("",     "(asleep in eraser bits)",           detail_color, False),
        ("",     "",                                  label_color, False),
        ("RULE", "Character > BG saturation",        (120, 100, 60), False),
        ("",     "Hoodie sage #789e82 — HOLDS",      detail_color, False),
    ]

    line_h = 22
    cur_y  = y + 18
    cur_x  = x + 14

    draw.text((cur_x, cur_y - 2),
              "LUMA — Classroom Pose  v001",
              fill=title_color, font=font)
    cur_y += 28
    draw.line([(cur_x, cur_y), (x + w - 14, cur_y)], fill=(180, 168, 150), width=1)
    cur_y += 10

    for (prefix, text, color, bold) in annotations:
        if not text:
            cur_y += 8
            continue
        if prefix:
            draw.text((cur_x, cur_y),
                      f"{prefix}: ", fill=(100, 140, 110), font=font_sm)
            draw.text((cur_x + 42, cur_y), text, fill=color, font=font_sm)
        else:
            draw.text((cur_x + 42, cur_y), text, fill=color, font=font_sm)
        cur_y += line_h
        if cur_y > y + h - 20:
            break

    # Storyboard reference footer
    draw.line([(cur_x, y + h - 30), (x + w - 14, y + h - 30)],
              fill=(180, 168, 150), width=1)
    draw.text((cur_x, y + h - 24),
              "Cycle 14 — Maya Santos",
              fill=detail_color, font=font_sm)


def generate_luma_classroom_pose(output_path):
    """Render seated classroom pose sheet for Luma."""
    img  = Image.new('RGB', (CANVAS_W, CANVAS_H), CANVAS_BG)
    draw = ImageDraw.Draw(img, 'RGBA')

    try:
        font       = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        font_sm    = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except Exception:
        font = font_sm = font_title = ImageFont.load_default()

    # Sheet title
    draw.text((20, 12),
              "LUMA — Classroom Pose  |  Beat A1-04: Near-Miss  |  Cycle 14",
              fill=(80, 56, 32), font=font_title)

    # Character area background (slightly warmer)
    draw.rectangle([0, 40, CHAR_AREA_W, CANVAS_H], fill=(235, 224, 206))

    # Draw Luma seated — face center at (260, 200)
    char_cx = 270
    char_cy = 200
    draw_luma_seated(draw, char_cx, char_cy)

    # Annotation panel
    draw_annotation_panel(draw, ANNO_AREA_X, 40,
                          CANVAS_W - ANNO_AREA_X - 10,
                          CANVAS_H - 50,
                          font, font_sm)

    # Divider line between char area and annotation
    draw.line([(CHAR_AREA_W, 40), (CHAR_AREA_W, CANVAS_H)],
              fill=(180, 168, 150), width=2)

    img_rgb = img.convert('RGB')
    img_rgb.save(output_path)
    print(f"Saved: {output_path}  ({CANVAS_W}×{CANVAS_H}px)")


if __name__ == '__main__':
    import os
    out_dir = "/home/wipkat/team/output/characters/main"
    os.makedirs(out_dir, exist_ok=True)
    generate_luma_classroom_pose(
        os.path.join(out_dir, "LTG_CHAR_luma_classroom_pose_v001.png")
    )
