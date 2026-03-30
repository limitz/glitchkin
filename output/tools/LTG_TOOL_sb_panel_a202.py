# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_sb_panel_a202.py
Storyboard Panel A2-02 — Byte MCU VULNERABLE/RESIGNED expression (Cycle 18)
Maya Santos, Character Designer

Panel direction (Alex Chen, Cycle 18):
  - MCU (Medium Close-Up): head + upper body
  - Beat: Luma has just told Byte the plan. Byte is processing.
    VULNERABLE moment — the last flicker before resignation sets in.
  - Expression: RESIGNED geometry but 55% aperture (vs standard 45%)
    "The last flicker before giving up" — slightly more open than full RESIGNED
    - Droopy lower lid (parabolic curve, NOT flat)
    - Downcast pupil (shifted to lower half)
    - Flat short mouth (resigned — no energy)
    - 55% aperture (slightly more open = still a trace of resistance)
    - Reduced highlight dot (dim — not extinguished, not bright)
  - Body: one arm beginning to fold in (transitional — not fully drawn in yet)
  - Byte body fill: GL-01b #00D4E8 (Byte Teal — canonical, NOT GL-01 #00F0FF)
  - Background: mid-value dark, subtle circuit trace texture

Reference: RESIGNED geometry from LTG_CHAR_byte_expression_sheet.py
  - droopy_resigned: parabolic lower lid, pupil+10px down, dim highlight, heavy upper lid
  - For A2-02: aperture = 55% (not 45%) — the "almost resigned" state

Output:
  /home/wipkat/team/output/storyboards/act2/panels/LTG_SB_act2_panel_a202.png

Cycle 18 production notes:
  - After img.paste() always refresh draw = ImageDraw.Draw(img)
  - RESIGNED parabolic lower lid = max sag 7px at center (matches expression sheet)
  - 55% aperture distinguishes A2-02 from A2-07 (45%) — vulnerability still visible
  - Left arm fully extended (neutral), right arm beginning to fold = transitional posture
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

ACT2_PANELS_DIR = "/home/wipkat/team/output/storyboards/act2/panels"
OUTPUT_PATH     = os.path.join(ACT2_PANELS_DIR, "LTG_SB_act2_panel_a202.png")

os.makedirs(ACT2_PANELS_DIR, exist_ok=True)

PW, PH       = 800, 540
CAPTION_H    = 56
DRAW_H       = PH - CAPTION_H   # 484px scene area

# ── Palette ───────────────────────────────────────────────────────────────────
BG_CAPTION    = (18, 15, 22)
TEXT_CAPTION  = (230, 222, 200)
BORDER_COL    = (14, 10, 18)
STATIC_WHITE  = (240, 240, 240)
ANN_COL       = (200, 185, 120)
ANN_DIM       = (140, 130, 90)
CALLOUT_CYN   = (0, 200, 218)
CALLOUT_DIM   = (0, 150, 165)

# Byte canonical colors
# GL-01b = #00D4E8  (Byte Teal — CANONICAL BODY FILL, per production spec)
BYTE_BODY    = (0, 212, 232)   # GL-01b #00D4E8
BYTE_MID     = (0, 168, 184)   # mid shadow
BYTE_DARK    = (0, 105, 118)   # deep shadow / face plate
BYTE_OUTLINE = (10, 10, 20)
BYTE_EYE_W   = (232, 248, 255) # eye sclera
BYTE_EYE_CYN = (0, 200, 218)   # dim cyan iris (reduced — RESIGNED energy level)
BYTE_EYE_PUP = (10, 10, 20)
BYTE_BEZEL   = (22, 48, 58)    # eye bezel / frame

# Pixel eye (left side of face — RESIGNED downward arrow)
GLYPH_DEAD  = (10, 10, 24)
GLYPH_DIM   = (0, 80, 100)
GLYPH_MID   = (0, 168, 180)
GLYPH_CRACK = (255, 45, 107)

# Background
BG_BASE      = (28, 30, 40)    # mid-value dark — not void-black, readable MCU
CIRCUIT_COL  = (38, 52, 62)
CIRCUIT_DOT  = (48, 66, 78)
CIRCUIT_NODE = (28, 44, 52)


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


def draw_background(img, draw):
    """
    Mid-value dark background with subtle circuit trace texture.
    A2-02: intimate space — Byte processing what Luma told him.
    Not as deep/void as A2-07 ECU — this is an MCU with more spatial context.
    """
    # Mid-value dark base (not pure black — mid-value for MCU intimacy)
    draw.rectangle([0, 0, PW, DRAW_H], fill=BG_BASE)

    import random
    rng = random.Random(2202)

    # Horizontal circuit trace runs
    for _ in range(18):
        tx   = rng.randint(0, PW)
        ty   = rng.randint(0, DRAW_H)
        tlen = rng.randint(30, 120)
        draw.line([tx, ty, tx + tlen, ty], fill=CIRCUIT_COL, width=1)
        # Junction dot at end
        draw.rectangle([tx + tlen - 2, ty - 2, tx + tlen + 2, ty + 2],
                       fill=CIRCUIT_DOT)

    # Vertical trace runs
    for _ in range(12):
        tx   = rng.randint(0, PW)
        ty   = rng.randint(0, DRAW_H)
        tlen = rng.randint(20, 70)
        draw.line([tx, ty, tx, ty + tlen], fill=CIRCUIT_COL, width=1)

    # Circuit nodes (cross junction marks)
    for _ in range(8):
        nx = rng.randint(30, PW - 30)
        ny = rng.randint(20, DRAW_H - 20)
        r  = rng.randint(3, 6)
        draw.ellipse([nx - r, ny - r, nx + r, ny + r],
                     fill=CIRCUIT_NODE, outline=CIRCUIT_DOT)

    # Subtle vignette — edges slightly darker (intimacy framing)
    vignette = Image.new('RGBA', (PW, DRAW_H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette)
    for margin, alpha in [(0, 55), (20, 38), (45, 20)]:
        vd.rectangle([margin, margin, PW - margin, DRAW_H - margin],
                     outline=(0, 0, 0, alpha), width=margin + 1 if margin > 0 else 1)
    # Corners vignette
    corner_size = 160
    for cx_v, cy_v in [(0, 0), (PW, 0), (0, DRAW_H), (PW, DRAW_H)]:
        for r, a in [(corner_size, 30), (corner_size - 30, 18), (corner_size - 60, 10)]:
            vd.ellipse([cx_v - r, cy_v - r, cx_v + r, cy_v + r],
                       fill=(0, 0, 0, a))
    base = img.convert('RGBA')
    panel_area = base.crop((0, 0, PW, DRAW_H))
    merged = Image.alpha_composite(panel_area.convert('RGBA'), vignette)
    img.paste(merged.convert('RGB'), (0, 0))
    draw = ImageDraw.Draw(img)

    return draw


def draw_downward_arrow_glyph(draw, origin_x, origin_y, pixel_size):
    """
    Render a 5×5 downward-arrow pixel glyph — RESIGNED defeat indicator.
    Used in left-eye pixel display of Byte's face.
    """
    ARROW_BRIGHT = {
        (0, 2), (1, 2),
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
        (3, 1), (3, 2), (3, 3),
        (4, 2),
    }
    for row_idx in range(5):
        for col_idx in range(5):
            if (row_idx, col_idx) in ARROW_BRIGHT:
                color = GLYPH_MID
            else:
                color = GLYPH_DEAD
            px = origin_x + col_idx * pixel_size
            py = origin_y + row_idx * pixel_size
            draw.rectangle([px, py, px + pixel_size - 1, py + pixel_size - 1],
                           fill=color)


def draw_byte_mcu(img, draw, font_ann):
    """
    Byte MCU — head + upper body, centered in frame.
    Beat: VULNERABLE (RESIGNED geometry, 55% aperture)
    Body: one arm beginning to fold in (transitional posture)
    Byte body fill: GL-01b #00D4E8
    """
    # MCU framing: head+upper body, Byte centered, body fills ~70% of frame height
    body_cx = PW // 2
    body_cy = int(DRAW_H * 0.62)   # body center — head+body fills upper 80% of frame

    # ── Body (OVAL — canonical Byte shape) ────────────────────────────────────
    body_rx = 165   # half-width
    body_ry = 185   # half-height (slightly squashed oval = Byte's shape)

    # Slight backward lean (+4 body tilt — processing/beginning to pull back)
    # Achieved by offsetting body slightly right of center
    lean_offset = 6
    bx = body_cx + lean_offset

    # Body shadow/shading (darker back oval for depth)
    draw.ellipse([bx - body_rx + 8, body_cy - body_ry + 8,
                  bx + body_rx - 8, body_cy + body_ry - 8],
                 fill=BYTE_MID)
    # Body fill — GL-01b #00D4E8 (Byte Teal canonical)
    draw.ellipse([bx - body_rx, body_cy - body_ry,
                  bx + body_rx, body_cy + body_ry],
                 fill=BYTE_BODY, outline=BYTE_OUTLINE, width=4)

    # Body highlight zone (inner lighter ellipse — 3D read)
    draw.ellipse([bx - body_rx + 18, body_cy - body_ry + 18,
                  bx + body_rx - 55, body_cy + body_ry - 80],
                 fill=(0, 225, 245))   # slightly brighter inner zone

    # ── Arms — TRANSITIONAL POSTURE ────────────────────────────────────────────
    # Left arm (viewer left): still extended downward — not yet folding in
    # Right arm (viewer right): beginning to fold — elbow pulling toward body
    arm_w = 38
    arm_h = 85

    # Left arm — extended normally (not yet folding)
    alx = bx - body_rx - 6
    aly = body_cy + 28
    draw.ellipse([alx, aly, alx + arm_w, aly + arm_h],
                 fill=BYTE_BODY, outline=BYTE_OUTLINE, width=3)
    # Left arm shadow edge
    draw.arc([alx, aly, alx + arm_w, aly + arm_h],
             start=0, end=180, fill=BYTE_MID, width=6)

    # Right arm — beginning to fold in (pulled ~40% toward body vs neutral)
    # In neutral, arm_x_scale=1.0 puts arm at body edge.
    # RESIGNED (full) uses arm_x_scale=0.50 — arm very close.
    # A2-02 transitional: arm ~0.75 of way to body — clearly moving inward
    arx = bx + body_rx - 26   # pulled significantly inward (vs edge at bx+body_rx)
    ary = body_cy + 36
    # Arm is foreshortened (folding in — slight perspective)
    arm_fold_w = arm_w - 6    # slightly narrower = depth foreshortening
    arm_fold_h = arm_h - 18   # shorter = beginning to compact
    draw.ellipse([arx, ary, arx + arm_fold_w, ary + arm_fold_h],
                 fill=BYTE_BODY, outline=BYTE_OUTLINE, width=3)
    # Right arm shadow — fold shadow on inner edge
    draw.arc([arx, ary, arx + arm_fold_w, ary + arm_fold_h],
             start=180, end=360, fill=BYTE_MID, width=6)

    # ── Hover particles (Cycle 10 spec: 10×10px, canonical) ───────────────────
    # Reduced energy in RESIGNED state — fewer / dimmer particles
    import random
    rng = random.Random(202)
    for _ in range(3):
        px = bx + rng.randint(-body_rx - 14, body_rx + 14)
        py = body_cy + rng.randint(-body_ry - 10, -body_ry + 10)
        # 10×10px canonical hover particle
        draw.rectangle([px, py, px + 10, py + 10],
                       fill=(0, 168, 184), outline=(0, 140, 155), width=1)

    # ── Face Plate ─────────────────────────────────────────────────────────────
    # Face plate: inset panel on Byte's face (front-facing oval section)
    face_cy   = body_cy - int(body_ry * 0.22)   # face in upper portion of body
    fp_w      = 210
    fp_h      = 152
    fp_x      = bx - fp_w // 2
    fp_y      = face_cy - fp_h // 2

    draw.rounded_rectangle([fp_x, fp_y, fp_x + fp_w, fp_y + fp_h],
                           radius=24, fill=BYTE_DARK,
                           outline=BYTE_OUTLINE, width=3)

    # ── LEFT EYE: Pixel display — RESIGNED downward arrow glyph ────────────────
    # Left eye is the pixel-LED display eye (Byte's left = viewer's left)
    left_eye_w = 72
    left_eye_h = 50
    lex = fp_x + 20
    ley = fp_y + fp_h // 2 - left_eye_h // 2 - 6

    # Eye bezel
    draw.rectangle([lex, ley, lex + left_eye_w, ley + left_eye_h],
                   fill=BYTE_BEZEL, outline=BYTE_OUTLINE, width=3)

    # Dark interior
    draw.rectangle([lex + 4, ley + 4, lex + left_eye_w - 4, ley + left_eye_h - 4],
                   fill=GLYPH_DEAD)

    # Downward arrow pixel glyph — RESIGNED state
    arrow_ps    = 5   # pixel size
    arrow_gw    = 5 * arrow_ps
    arrow_gh    = 5 * arrow_ps
    arrow_ox    = lex + (left_eye_w - arrow_gw) // 2
    arrow_oy    = ley + (left_eye_h - arrow_gh) // 2
    draw_downward_arrow_glyph(draw, arrow_ox, arrow_oy, arrow_ps)

    # Subtle glow from pixel eye (very dim — low energy for RESIGNED)
    add_glow(img, lex + left_eye_w // 2, ley + left_eye_h // 2,
             20, (0, 168, 180), steps=4, max_alpha=18)
    draw = ImageDraw.Draw(img)

    # ── RIGHT EYE: Organic eye — RESIGNED 55% aperture ─────────────────────────
    # Right eye = Byte's organic eye (right side of face = viewer's right)
    # A2-02 spec: 55% aperture (more open than RESIGNED standard 45%)
    # = "last flicker before giving up" — one tick more open than full RESIGNED
    right_eye_w = 82
    right_eye_h = 58
    rex = fp_x + fp_w - 20 - right_eye_w
    rey = fp_y + fp_h // 2 - right_eye_h // 2 - 6

    # Eye frame bezel
    draw.rectangle([rex, rey, rex + right_eye_w, rey + right_eye_h],
                   fill=BYTE_BEZEL, outline=BYTE_OUTLINE, width=3)

    # Eye sclera (white interior)
    inner_m = 5
    ew_inner_x1 = rex + inner_m
    ew_inner_y1 = rey + inner_m
    ew_inner_x2 = rex + right_eye_w - inner_m
    ew_inner_y2 = rey + right_eye_h - inner_m

    # RESIGNED geometry — 55% aperture version:
    # aperture_h = height of visible eye area = 55% of total eye height
    # (Standard RESIGNED = 45%, Standard NEUTRAL = 60%)
    total_eye_h = right_eye_h - inner_m * 2
    aperture_h  = int(total_eye_h * 0.55)   # 55% — A2-02 spec

    # Eye white area (inside bezel, offset down slightly = weight of defeat)
    eye_center_x = rex + right_eye_w // 2
    eye_center_y = rey + right_eye_h // 2 + 4  # slight downward offset

    ew = right_eye_w // 2 - inner_m   # half-width of eye
    eh = right_eye_h // 2 - inner_m   # half-height of eye

    # Draw eye white (will be partially covered by droopy lid below)
    eye_h_55 = int(eh * 0.55)
    draw.ellipse([eye_center_x - ew, eye_center_y - eye_h_55 + 5,
                  eye_center_x + ew, eye_center_y + eye_h_55 + 5],
                 fill=BYTE_EYE_W)

    # Iris — shifted DOWN (downcast gaze — defeat/avoidance)
    # Strongly downward: lower portion of sclera
    cell = ew // 3   # relative unit
    iris_cx = eye_center_x
    iris_cy = eye_center_y + 7   # strongly downcast (+7px from center)
    iris_r  = cell + 4
    draw.ellipse([iris_cx - iris_r, iris_cy - iris_r,
                  iris_cx + iris_r, iris_cy + iris_r],
                 fill=(55, 35, 16))   # dark brown iris

    # Pupil (same downcast direction)
    pup_r = iris_r - 5
    draw.ellipse([iris_cx - pup_r, iris_cy - pup_r,
                  iris_cx + pup_r, iris_cy + pup_r],
                 fill=BYTE_EYE_PUP)

    # REDUCED highlight dot — dim, not extinguished (55% = still a flicker)
    # Smaller than neutral highlight, positioned lower-right (match downcast iris)
    draw.ellipse([iris_cx + 2, iris_cy - pup_r + 2,
                  iris_cx + 6, iris_cy - pup_r + 6],
                 fill=(180, 175, 165))   # dim grey-white (not full bright)

    # HEAVY UPPER LID — pressing down (heavier than neutral, at 55% aperture)
    # Arc across top of sclera
    draw.arc([eye_center_x - ew, eye_center_y - eye_h_55 + 5,
              eye_center_x + ew, eye_center_y + eye_h_55 + 5],
             start=195, end=345, fill=BYTE_OUTLINE, width=8)
    # Lid cover rectangle (fills top portion down to 55% mark)
    lid_cover_h = int(total_eye_h * (1.0 - 0.55))   # top portion = 45% covered
    draw.rectangle([rex + inner_m, rey + inner_m,
                    rex + right_eye_w - inner_m,
                    rey + inner_m + lid_cover_h],
                   fill=BYTE_BEZEL)
    # Lid edge line (weight of the heavy lid)
    draw.line([rex + inner_m, rey + inner_m + lid_cover_h,
               rex + right_eye_w - inner_m, rey + inner_m + lid_cover_h],
              fill=BYTE_OUTLINE, width=3)

    # PARABOLIC DROOPING LOWER LID — key geometry (from expression sheet v002)
    # Parabolic sag: max droop at center. This is what distinguishes RESIGNED from NEUTRAL.
    # (NEUTRAL has flat arc — RESIGNED has concave-downward parabolic curve)
    droop_pts = []
    for i in range(13):
        t = i / 12.0   # 0..1 left to right
        dx = int(-ew + t * 2 * ew)
        # Parabolic sag formula — max 7px at center (matches expression sheet)
        sag = int(7 * 4 * t * (1 - t))
        dy  = int(eye_h_55 + 5 + sag)
        droop_pts.append((eye_center_x + dx, eye_center_y + dy))
    if len(droop_pts) > 1:
        draw.line(droop_pts, fill=BYTE_OUTLINE, width=3)

    # No smile crinkle (distinct from RELUCTANT JOY)

    # ── RESIGNED MOUTH — flat short line ─────────────────────────────────────
    # Flat line: no energy to frown, no energy to smile. Flatness IS the expression.
    mouth_y    = fp_y + int(fp_h * 0.80)
    mouth_cx   = bx
    mouth_half = 22    # shorter than neutral (reduced energy)
    draw.line([mouth_cx - mouth_half, mouth_y,
               mouth_cx + mouth_half, mouth_y],
              fill=BYTE_OUTLINE, width=3)
    # Subtle corner tuck (not a downturn — pure flat resignation)
    draw.line([mouth_cx - mouth_half, mouth_y,
               mouth_cx - mouth_half + 4, mouth_y + 1],
              fill=BYTE_OUTLINE, width=2)
    draw.line([mouth_cx + mouth_half, mouth_y,
               mouth_cx + mouth_half - 4, mouth_y + 1],
              fill=BYTE_OUTLINE, width=2)

    # ── Cyan glow corona (Byte's digital nature — dim, muted = RESIGNED) ─────
    add_glow(img, bx, face_cy, 110, (0, 180, 200), steps=5, max_alpha=14)
    draw = ImageDraw.Draw(img)

    # ── Annotations ──────────────────────────────────────────────────────────
    # Shot type
    draw.text((8, 6), "MCU  —  Byte", font=font_ann, fill=ANN_COL)
    draw.text((8, 18), "head + upper body", font=font_ann, fill=ANN_DIM)

    # Expression annotation (right side)
    ann_rx = PW - 160
    draw.text((ann_rx, 6), "RESIGNED (55% apt)", font=font_ann, fill=CALLOUT_CYN)
    draw.text((ann_rx, 18), "VULNERABLE beat", font=font_ann, fill=(180, 160, 90))
    draw.text((ann_rx, 30), "pre-resignation", font=font_ann, fill=(150, 135, 75))

    # Droopy lid callout
    droop_ann_x = rex - 110
    droop_ann_y = rey + inner_m + lid_cover_h - 4
    draw.line([rex + inner_m - 2, droop_ann_y,
               droop_ann_x + 85, droop_ann_y + 2],
              fill=CALLOUT_CYN, width=1)
    draw.text((droop_ann_x, droop_ann_y - 10), "droopy lower lid", font=font_ann,
              fill=CALLOUT_CYN)
    draw.text((droop_ann_x, droop_ann_y + 2), "parabolic sag", font=font_ann,
              fill=CALLOUT_DIM)

    # Aperture callout
    draw.text((droop_ann_x, droop_ann_y + 14), "55% apt (not 45%)", font=font_ann,
              fill=(180, 165, 80))

    # Folding arm callout
    arm_ann_y = ary + arm_fold_h // 2
    draw.text((arx + arm_fold_w + 8, arm_ann_y), "arm folding in", font=font_ann,
              fill=(160, 145, 85))
    draw.text((arx + arm_fold_w + 8, arm_ann_y + 12), "transitional", font=font_ann,
              fill=(130, 118, 68))

    # Downcast pupil callout (brief)
    draw.text((rex + right_eye_w + 8, rey + right_eye_h // 2),
              "downcast pupil", font=font_ann, fill=CALLOUT_DIM)

    return draw


def make_panel():
    font      = load_font(14)
    font_bold = load_font(14, bold=True)
    font_cap  = load_font(12)
    font_ann  = load_font(10)

    img  = Image.new('RGB', (PW, PH), BG_BASE)
    draw = ImageDraw.Draw(img)

    # Draw background
    draw = draw_background(img, draw)

    # Draw Byte MCU
    draw = draw_byte_mcu(img, draw, font_ann)

    # ── Caption bar ───────────────────────────────────────────────────────────
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=BORDER_COL, width=2)
    draw.text((10, DRAW_H + 6),
              "A2-02  MCU  neutral observer",
              font=font_cap, fill=(155, 148, 125))
    draw.text((10, DRAW_H + 22),
              "Byte processing what Luma just told him — VULNERABLE moment, last flicker before resignation",
              font=font_cap, fill=TEXT_CAPTION)
    draw.text((10, DRAW_H + 38),
              "beat: pre-resignation  |  expr: RESIGNED geom 55% apt  |  body: transitional fold  |  bg: circuit trace",
              font=font_ann, fill=(145, 138, 108))
    draw.text((PW - 260, DRAW_H + 44),
              "LTG_SB_act2_panel_a202_v002",
              font=font_ann, fill=(95, 90, 72))

    # ── Border ────────────────────────────────────────────────────────────────
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COL, width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("A2-02 panel (v002) generation complete (Cycle 18).")
    print("  Expression: RESIGNED geometry, 55% aperture (pre-resignation vulnerable beat)")
    print("  Body: transitional posture — right arm beginning to fold in")
    print("  Body fill: GL-01b #00D4E8 (Byte Teal canonical)")
