#!/usr/bin/env python3
"""
LTG_TOOL_sb_panel_a207.py
Storyboard Panel A2-07 — Byte ECU RESIGNED expression (Cycle 16)
Lee Tanaka, Storyboard Artist

Panel direction (Carmen Reyes):
  - ECU (Extreme Close-Up) on Byte's cracked eye, RESIGNED expression
  - Frame tight enough that the pixel glyph fills ~30% of frame width
  - One character, one emotion — no spatial ambiguity
  - Most important beat in Act 2: moment Byte chooses to trust Luma
  - Background: deep void dark with subtle circuit traces (intimate, quiet)

RESIGNED expression (from Alex Chen, expression sheet v002):
  - Left eye (pixel display): Downward arrow ↓ pixel glyph — defeat indicator
  - Right eye (organic): droopy_resigned — heavy upper lid (50% aperture),
    pupil shifted downward (defeat/avoidance gaze). No suppressed smile.
  - Arms: close to body (arm_x_scale=0.50) — drawn-in avoidance posture
  - Body lean: slightly backward (+8°) — pulling away from disclosure
  - Mouth: short flat line (shorter than neutral) — no energy
  - Cracked eye glyph: DEAD=#0A0A18, DIM=#005064, MID=#00A8B4,
    CRACK=Hot Magenta #FF2D6B, BRIGHT=#C8FFFF

Cracked eye usage notes (from glyph tool):
  - Cracked eye is the RIGHT eye of Byte's face (faces toward danger)
  - Crack runs upper-right to lower-left across eye bezel
  - Dead zone is upper-right
  - Glyph fills 60% of cracked-eye interior

Output:
  /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a207.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_act2_panel_a207.png")

os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH       = 480, 270
CAPTION_H    = 48
DRAW_H       = PH - CAPTION_H   # 222px scene area

# ── Palette ──────────────────────────────────────────────────────────────────
BG_CAPTION   = (25, 20, 18)
TEXT_CAPTION = (235, 228, 210)
BORDER_COL   = (20, 15, 12)
STATIC_WHITE = (240, 240, 240)

# Byte colors
BYTE_BODY    = (0, 212, 232)
BYTE_MID     = (0, 160, 175)
BYTE_DARK    = (0, 105, 115)
BYTE_OUTLINE = (10, 10, 20)
BYTE_SCAR    = (255, 45, 107)
BYTE_EYE_W   = (232, 248, 255)
BYTE_EYE_CYN = (0, 240, 255)
BYTE_EYE_PUP = (10, 10, 20)
BYTE_BEZEL   = (26, 58, 64)

# Dead-pixel glyph colors (from glyph tool / byte.md Section 9B)
GLYPH_DEAD   = (10, 10, 24)
GLYPH_DIM    = (0, 80, 100)
GLYPH_MID    = (0, 168, 180)
GLYPH_CRACK  = (255, 45, 107)    # Hot Magenta
GLYPH_BRIGHT = (200, 255, 255)
GLYPH_OVER   = (10, 10, 20)      # Void Black crack overlay

# Background circuit trace colors
CIRCUIT_COL  = (22, 38, 44)
CIRCUIT_DOT  = (30, 55, 62)

ELEC_CYAN    = (0, 240, 255)


# ── 7×7 Dead-Pixel Glyph Definition (matches LTG_CHAR_byte_cracked_eye_glyph_v001) ──
GLYPH_7x7 = [
    [1, 1, 1, 1, 3, 0, 0],
    [1, 2, 1, 3, 0, 0, 0],
    [2, 1, 3, 0, 0, 4, 0],
    [1, 3, 0, 0, 4, 0, 0],
    [3, 0, 0, 1, 1, 0, 1],
    [0, 0, 1, 2, 1, 1, 1],
    [0, 3, 1, 1, 2, 1, 1],
]
PIXEL_COLORS = {
    0: GLYPH_DEAD,
    1: GLYPH_DIM,
    2: GLYPH_MID,
    3: GLYPH_CRACK,
    4: GLYPH_BRIGHT,
}


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


def render_cracked_eye_glyph(draw, origin_x, origin_y, pixel_size):
    """Render the 7×7 cracked-eye glyph at given position and scale."""
    for row_idx, row in enumerate(GLYPH_7x7):
        for col_idx, state in enumerate(row):
            color = PIXEL_COLORS[state]
            px = origin_x + col_idx * pixel_size
            py = origin_y + row_idx * pixel_size
            draw.rectangle([px, py, px + pixel_size - 1, py + pixel_size - 1], fill=color)
    # Outer grid border
    gw = 7 * pixel_size
    gh = 7 * pixel_size
    draw.rectangle([origin_x - 1, origin_y - 1,
                    origin_x + gw, origin_y + gh],
                   outline=(40, 60, 70), width=1)


def draw_downward_arrow_glyph(draw, origin_x, origin_y, pixel_size):
    """
    Render a downward-arrow pixel glyph for RESIGNED left eye display.
    5×5 pixel grid showing ↓ arrow — defeat indicator.
    """
    # Downward arrow pattern (5×5 pixels)
    ARROW_5x5 = [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
    ]
    ARROW_COLORS = {0: GLYPH_DIM, 1: GLYPH_MID}
    # Bright active pixels for the arrow shaft
    ARROW_BRIGHT = {
        (0, 2), (1, 2),          # shaft
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),  # cross-bar
        (3, 1), (3, 2), (3, 3),  # V-top
        (4, 2),                  # V-tip
    }
    for row_idx, row in enumerate(ARROW_5x5):
        for col_idx, state in enumerate(row):
            if (row_idx, col_idx) in ARROW_BRIGHT:
                color = GLYPH_MID
            else:
                color = GLYPH_DEAD
            px = origin_x + col_idx * pixel_size
            py = origin_y + row_idx * pixel_size
            draw.rectangle([px, py, px + pixel_size - 1, py + pixel_size - 1], fill=color)


def draw_a207_panel(img, draw, font, font_bold, font_cap, font_ann):
    """
    A2-07: ECU on Byte — RESIGNED expression.
    Byte's face fills the frame. Cracked eye is the focal center.
    Background: deep void with circuit traces.
    This is the most important beat in Act 2: Byte chooses to trust Luma.
    """
    # ── Background: void + circuit traces ──────────────────────────────────
    # Deep void base — not pure black, has depth
    draw.rectangle([0, 0, PW, DRAW_H], fill=(8, 10, 18))

    # Subtle circuit traces (horizontal + vertical runs)
    import random
    rng = random.Random(2207)

    # Horizontal trace runs
    for _ in range(12):
        tx = rng.randint(0, PW)
        ty = rng.randint(0, DRAW_H)
        tlen = rng.randint(20, 80)
        draw.line([tx, ty, tx + tlen, ty], fill=CIRCUIT_COL, width=1)
        # Junction dot
        draw.rectangle([tx + tlen - 2, ty - 2, tx + tlen + 2, ty + 2],
                       fill=CIRCUIT_DOT)
    # Vertical trace runs
    for _ in range(8):
        tx = rng.randint(0, PW)
        ty = rng.randint(0, DRAW_H)
        tlen = rng.randint(15, 50)
        draw.line([tx, ty, tx, ty + tlen], fill=CIRCUIT_COL, width=1)

    # Faint corner vignette glow (warm magenta — emotional undertone)
    # Use subtle dark red at corners
    corner_glow = Image.new('RGBA', (PW, DRAW_H), (0, 0, 0, 0))
    cg = ImageDraw.Draw(corner_glow)
    for r in [120, 90, 60]:
        alpha = 12
        cg.ellipse([-r, -r, r, r], fill=(60, 0, 30, alpha))
        cg.ellipse([PW - r, -r, PW + r, r], fill=(60, 0, 30, alpha))
    base = img.convert('RGBA')
    panel_area = base.crop((0, 0, PW, DRAW_H))
    merged = Image.alpha_composite(panel_area.convert('RGBA'), corner_glow)
    img.paste(merged.convert('RGB'), (0, 0))
    draw = ImageDraw.Draw(img)

    # ── Byte ECU — face fills the frame ────────────────────────────────────
    # ECU: face centered, fills ~80% of frame height
    # Body partially visible at bottom (drawn-in arms for RESIGNED posture)
    face_cx  = PW // 2
    face_cy  = DRAW_H // 2 - 10    # slightly above center — face dominates

    # Body oval (LARGE — ECU means we see mostly face, top of body)
    body_w   = 260
    body_h   = 210
    draw.ellipse([face_cx - body_w // 2, face_cy - body_h // 2,
                  face_cx + body_w // 2, face_cy + body_h // 2],
                 fill=BYTE_MID, outline=BYTE_OUTLINE, width=3)
    # Body highlight (inner lighter zone)
    draw.ellipse([face_cx - body_w // 2 + 10, face_cy - body_h // 2 + 10,
                  face_cx + body_w // 2 - 10, face_cy + body_h // 2 - 10],
                 fill=BYTE_BODY, outline=None)

    # RESIGNED body lean: slight backward (right side of body pulled back slightly)
    # Achieved by the body being cropped at the bottom of the frame

    # ── RESIGNED arms: drawn in close to body ──────────────────────────────
    # Arms barely visible, tight against the body sides (avoidance posture)
    arm_w = 22
    arm_h = 55
    # Left arm (viewer left) — barely visible, very close to body
    arm_lx = face_cx - body_w // 2 + 8
    arm_ly = face_cy + 40
    draw.ellipse([arm_lx, arm_ly, arm_lx + arm_w, arm_ly + arm_h],
                 fill=BYTE_MID, outline=BYTE_OUTLINE, width=2)
    # Right arm (viewer right) — same, drawn in
    arm_rx = face_cx + body_w // 2 - arm_w - 8
    arm_ry = face_cy + 40
    draw.ellipse([arm_rx, arm_ry, arm_rx + arm_w, arm_ry + arm_h],
                 fill=BYTE_MID, outline=BYTE_OUTLINE, width=2)

    # ── Face plate area ─────────────────────────────────────────────────────
    # ECU: face region is the top 60% of the body oval
    # Face plate: darker inset on front face
    fp_w = 180
    fp_h = 130
    fp_x = face_cx - fp_w // 2
    fp_y = face_cy - fp_h // 2 - 18
    draw.rounded_rectangle([fp_x, fp_y, fp_x + fp_w, fp_y + fp_h],
                           radius=20, fill=BYTE_DARK, outline=BYTE_OUTLINE, width=2)

    # ── CRACKED EYE (RIGHT eye of Byte = viewer's right, facing toward danger) ─
    # ECU: cracked eye fills ~30% of frame width = ~144px
    # Cracked eye is the DOMINANT element
    cracked_eye_w  = 90     # eye frame width
    cracked_eye_h  = 64     # eye frame height
    # Position: right side of face plate (viewer's right)
    ce_x = face_cx + 18
    ce_y = fp_y + fp_h // 2 - cracked_eye_h // 2 - 4

    # Eye bezel (deep frame)
    draw.rectangle([ce_x, ce_y, ce_x + cracked_eye_w, ce_y + cracked_eye_h],
                   fill=BYTE_BEZEL, outline=BYTE_OUTLINE, width=3)

    # Physical crack line across bezel: upper-right to lower-left
    crack_start = (ce_x + int(cracked_eye_w * 0.70), ce_y + 2)
    crack_end   = (ce_x + int(cracked_eye_w * 0.18), ce_y + cracked_eye_h - 2)
    draw.line([crack_start, crack_end], fill=GLYPH_OVER, width=3)
    # Crack hair-line (magenta glow at crack edge)
    draw.line([crack_start, crack_end], fill=GLYPH_CRACK, width=1)

    # Glyph inside cracked eye — fills 60% of interior
    glyph_area_w = int(cracked_eye_w * 0.55)
    glyph_area_h = int(cracked_eye_h * 0.80)
    pixel_size   = max(2, min(glyph_area_w // 7, glyph_area_h // 7))
    glyph_w      = 7 * pixel_size
    glyph_h      = 7 * pixel_size
    g_origin_x   = ce_x + (glyph_area_w - glyph_w) // 2 + 4
    g_origin_y   = ce_y + (cracked_eye_h - glyph_h) // 2

    # Clip glyph to left side of crack
    glyph_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glyph_layer)
    for row_idx, row in enumerate(GLYPH_7x7):
        for col_idx, state in enumerate(row):
            color = PIXEL_COLORS[state]
            px = g_origin_x + col_idx * pixel_size
            py = g_origin_y + row_idx * pixel_size
            # Only render on the cracked (left of fracture) side
            local_x = px - ce_x
            if local_x < int(cracked_eye_w * 0.60):
                gd.rectangle([px, py, px + pixel_size - 1, py + pixel_size - 1],
                              fill=(*color, 230))
    base_rgba = img.convert('RGBA')
    img.paste(Image.alpha_composite(base_rgba, glyph_layer).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Bezel chip at upper-right (physical damage detail)
    chip_x = ce_x + cracked_eye_w - 12
    chip_y = ce_y
    draw.polygon([(chip_x, chip_y), (chip_x + 12, chip_y),
                  (chip_x + 12, chip_y + 8)],
                 fill=BYTE_OUTLINE)

    # Hot magenta glow from crack
    add_glow(img, ce_x + int(cracked_eye_w * 0.45), ce_y + cracked_eye_h // 2,
             28, (255, 45, 107), steps=5, max_alpha=35)

    draw = ImageDraw.Draw(img)

    # ── NORMAL EYE (LEFT eye of Byte = viewer's left) — RESIGNED state ──────
    # Droopy-lid: heavy upper lid at ~50% aperture, pupil shifted down
    ne_w  = 72
    ne_h  = 50
    ne_x  = face_cx - 18 - ne_w    # left side of face plate
    ne_y  = fp_y + fp_h // 2 - ne_h // 2 - 4

    # Eye frame
    draw.rectangle([ne_x, ne_y, ne_x + ne_w, ne_y + ne_h],
                   fill=BYTE_BEZEL, outline=BYTE_OUTLINE, width=3)

    # Eye interior (white sclera)
    inner_m = 5
    draw.ellipse([ne_x + inner_m, ne_y + inner_m,
                  ne_x + ne_w - inner_m, ne_y + ne_h - inner_m],
                 fill=BYTE_EYE_W)

    # Iris (electric cyan)
    iris_cx = ne_x + ne_w // 2
    iris_cy = ne_y + ne_h // 2 + 4    # RESIGNED: pupil slightly down
    iris_r  = 14
    draw.ellipse([iris_cx - iris_r, iris_cy - iris_r,
                  iris_cx + iris_r, iris_cy + iris_r],
                 fill=BYTE_EYE_CYN)
    # Pupil
    pup_r = 7
    draw.ellipse([iris_cx - pup_r, iris_cy - pup_r,
                  iris_cx + pup_r, iris_cy + pup_r],
                 fill=BYTE_EYE_PUP)
    # Highlight
    draw.rectangle([iris_cx + 3, iris_cy - pup_r + 2,
                    iris_cx + 6, iris_cy - pup_r + 5],
                   fill=STATIC_WHITE)

    # DROOPY LID — heavy upper lid covering ~50% of eye aperture
    # Draw a filled rectangle over the top half of the eye interior
    lid_cover_h = int((ne_h - inner_m * 2) * 0.50)
    draw.rectangle([ne_x + inner_m, ne_y + inner_m,
                    ne_x + ne_w - inner_m, ne_y + inner_m + lid_cover_h],
                   fill=BYTE_BEZEL)
    # Lid edge line (heavier — the "weight" of the lid)
    draw.line([ne_x + inner_m, ne_y + inner_m + lid_cover_h,
               ne_x + ne_w - inner_m, ne_y + inner_m + lid_cover_h],
              fill=BYTE_OUTLINE, width=3)
    # Eyelid crease (defines the heaviness)
    draw.line([ne_x + inner_m + 2, ne_y + inner_m + lid_cover_h - 3,
               ne_x + ne_w - inner_m - 2, ne_y + inner_m + lid_cover_h - 3],
              fill=(18, 42, 48), width=1)

    # Downward arrow glyph INSIDE the normal left eye (RESIGNED indicator)
    # Small pixel glyph centered in visible eye area (below droopy lid)
    visible_eye_top  = ne_y + inner_m + lid_cover_h + 2
    visible_eye_h    = ne_h - inner_m * 2 - lid_cover_h
    arrow_pixel_size = 3
    arrow_origin_x   = ne_x + ne_w // 2 - (5 * arrow_pixel_size) // 2
    arrow_origin_y   = visible_eye_top + (visible_eye_h - 5 * arrow_pixel_size) // 2
    draw_downward_arrow_glyph(draw, arrow_origin_x, arrow_origin_y, arrow_pixel_size)

    # ── RESIGNED MOUTH ──────────────────────────────────────────────────────
    # Short flat line — no energy to frown, no energy to smile
    mouth_y    = fp_y + fp_h * 3 // 4
    mouth_cx   = face_cx
    mouth_half = 20    # shorter than neutral
    draw.line([mouth_cx - mouth_half, mouth_y,
               mouth_cx + mouth_half, mouth_y],
              fill=BYTE_OUTLINE, width=3)
    # Subtle mouth corners pulled slightly inward (not a downturn — pure flat)
    draw.line([mouth_cx - mouth_half, mouth_y,
               mouth_cx - mouth_half + 4, mouth_y + 1],
              fill=BYTE_OUTLINE, width=2)
    draw.line([mouth_cx + mouth_half, mouth_y,
               mouth_cx + mouth_half - 4, mouth_y + 1],
              fill=BYTE_OUTLINE, width=2)

    # ── Cyan glow corona (Byte's digital nature — subtle, quiet) ─────────────
    add_glow(img, face_cx, face_cy - 10, 120, (0, 200, 220), steps=5, max_alpha=18)
    draw = ImageDraw.Draw(img)

    # ── Annotations ─────────────────────────────────────────────────────────
    # Shot type annotation
    draw.text((6, 4), "ECU — Byte face", font=font_ann, fill=(180, 170, 130))
    # Beat annotation
    draw.text((6, 14), "RESIGNED: Byte chooses trust", font=font_ann, fill=(200, 180, 100))

    # Cracked eye callout arrow
    ann_x = ce_x + cracked_eye_w + 8
    ann_y = ce_y + cracked_eye_h // 2 - 6
    draw.line([ann_x, ann_y, ann_x + 6, ann_y],
              fill=(220, 80, 100), width=2)
    draw.text((ann_x + 8, ann_y - 5), "CRACKED EYE", font=font_ann, fill=(220, 80, 100))
    draw.text((ann_x + 8, ann_y + 5), "glyph ~30% frame", font=font_ann, fill=(180, 70, 80))

    # Droopy lid annotation
    draw.text((ne_x - 68, ne_y + 4), "droopy lid", font=font_ann, fill=(0, 200, 220))
    draw.text((ne_x - 68, ne_y + 14), "50% aperture", font=font_ann, fill=(0, 160, 180))
    draw.line([ne_x - 4, ne_y + inner_m + lid_cover_h,
               ne_x - 12, ne_y + 14 + 5],
              fill=(0, 180, 200), width=1)

    # Resigned posture annotation
    draw.text((6, DRAW_H - 22), "arms drawn in — avoidance posture", font=font_ann,
              fill=(160, 150, 110))


def make_panel():
    font      = load_font(13)
    font_bold = load_font(13, bold=True)
    font_cap  = load_font(11)
    font_ann  = load_font(9)

    img  = Image.new('RGB', (PW, PH), (8, 10, 18))
    draw = ImageDraw.Draw(img)

    draw_a207_panel(img, draw, font, font_bold, font_cap, font_ann)

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=BORDER_COL, width=2)
    draw.text((8, DRAW_H + 6), "A2-07  ECU  neutral observer",
              font=font_cap, fill=(160, 160, 160))
    draw.text((8, DRAW_H + 20),
              "Byte's cracked eye — RESIGNED. Most important beat Act 2. Byte chooses to trust Luma.",
              font=font_cap, fill=TEXT_CAPTION)
    draw.text((8, DRAW_H + 34),
              "beat: partial confession / trust threshold  |  bg: void+circuit traces  |  ECU cracked eye fills frame",
              font=font_ann, fill=(150, 140, 110))

    # Border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COL, width=2)

    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("A2-07 panel generation complete (Cycle 16).")
