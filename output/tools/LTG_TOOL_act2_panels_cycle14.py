# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
Act 2 Panels — Cycle 14 — "Luma & the Glitchkin"
Lee Tanaka, Storyboard Artist

Generates 4 Act 2 storyboard panels (all newly unblocked):

  A1-04 — Near-miss micro-beat (classroom)
  A2-02 — Byte MCU vulnerability (uses cracked-eye glyph — NOW UNBLOCKED)
  A2-05b — Cosmo using Glitch Frequency app
  A2-06 — App failure INSERT (phone screen close-up)

Plus an Act 2 contact sheet.

Key design principles applied (from MEMORY.md):
  - Glow effects ADD light (alpha_composite), never darkness
  - Face placement carries emotional info: centered=neutral, lower-center=effort/urgency
  - Byte's expression: four components (eye aperture, cracked-eye pixel state, mouth shape, body lean)
  - A still frame must make the motion before/after feel present
  - Dutch tilt = Image.rotate() on entire canvas
  - Pixel confetti = ADD light scatter (Glitch Layer visual signature)
  - Byte 7x7 dead-pixel glyph: DEAD=#0A0A18, DIM=#005064, MID=#00A8B4,
    CRACK=Hot Magenta #FF2D6B, BRIGHT=#C8FFFF, crack overlay=Void Black #0A0A14
  - Naming: LTG_[CATEGORY]_[descriptor]_v[###].[ext]

Outputs (480x270px each):
  /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a104.png
  /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a202.png
  /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a205b.png
  /home/wipkat/team/output/storyboards/panels/LTG_SB_act2_panel_a206.png
  /home/wipkat/team/output/storyboards/LTG_SB_act2_contactsheet.png
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

PANELS_DIR  = "/home/wipkat/team/output/storyboards/panels"
SHEETS_DIR  = "/home/wipkat/team/output/storyboards"
PW, PH      = 480, 270
CAPTION_H   = 48
DRAW_H      = PH - CAPTION_H  # 222px for scene area
BORDER      = 2

os.makedirs(PANELS_DIR, exist_ok=True)
os.makedirs(SHEETS_DIR, exist_ok=True)

# ── Shared palette ────────────────────────────────────────────────────────────
BG_CAPTION     = (25, 20, 18)
TEXT_CAPTION   = (235, 228, 210)
TEXT_ANN       = (20, 15, 12)
BORDER_COL     = (20, 15, 12)

# Luma
LUMA_SKIN      = (200, 136, 90)
LUMA_HAIR      = (22, 14, 8)
LUMA_PJ        = (160, 200, 180)
LUMA_OUTLINE   = (42, 28, 14)

# Byte
BYTE_BODY      = (0, 212, 232)
BYTE_MID       = (0, 160, 175)
BYTE_DARK      = (0, 105, 115)
BYTE_OUTLINE   = (10, 10, 20)
BYTE_SCAR      = (255, 45, 107)        # Hot Magenta
BYTE_SCAR_DIM  = (196, 35, 90)
BYTE_EYE_W     = (232, 248, 255)
BYTE_EYE_CYN   = (0, 240, 255)
BYTE_EYE_PUP   = (10, 10, 20)
BYTE_BEZEL     = (26, 58, 64)

# Dead-pixel glyph colors (Section 9B)
GLYPH_DEAD     = (10, 10, 24)          # ~#0A0A18
GLYPH_DIM      = (0, 80, 100)          # #005064
GLYPH_MID      = (0, 168, 180)         # #00A8B4
GLYPH_CRACK    = (255, 45, 107)        # Hot Magenta #FF2D6B (crack line)
GLYPH_BRIGHT   = (200, 255, 255)       # #C8FFFF
GLYPH_OVER     = (10, 10, 20)          # Void Black crack overlay

# Glitch palette
GLITCH_CYAN    = (0, 240, 255)
GLITCH_MAG     = (255, 0, 200)
GLITCH_ACID    = (180, 255, 40)
GLITCH_PURPLE  = (123, 47, 190)
GLITCH_WHITE   = (240, 240, 240)

# Cosmo
COSMO_SKIN     = (168, 118, 72)
COSMO_HAIR     = (14, 10, 6)
COSMO_SHIRT    = (80, 100, 170)
COSMO_OUTLINE  = (30, 20, 10)

# Environment
WARM_AMBER     = (55, 38, 24)
WARM_WALL      = (110, 85, 55)
WARM_FLOOR     = (72, 54, 36)
COOL_SCHOOL    = (170, 160, 195)       # dusty lavender
SCHOOL_SAGE    = (120, 150, 130)       # sage green
SCHOOL_FLOOR   = (140, 130, 110)
BOARD_GREEN    = (48, 80, 58)
BOARD_TEXT     = (220, 235, 215)
DESK_TAN       = (180, 155, 110)
STREET_TERRA   = (190, 130, 90)        # terracotta exterior
STREET_CREAM   = (235, 220, 190)
STREET_ASPHALT = (80, 75, 70)
PHONE_DARK     = (20, 18, 24)
PHONE_SILVER   = (180, 180, 195)
APP_BG         = (10, 12, 30)
APP_CYAN       = (0, 230, 255)
APP_GREEN      = (40, 255, 120)
APP_GRID       = (0, 60, 80)
STATIC_WHITE   = (240, 240, 240)
STATIC_DARK    = (10, 8, 14)


def load_fonts():
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    bold_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    def try_font(paths, size):
        for p in paths:
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
        return ImageFont.load_default()
    return (
        try_font(paths, 13),
        try_font(bold_paths, 13),
        try_font(paths, 11),
        try_font(paths, 9),
    )


def make_panel(filepath, shot_label, caption_text, draw_fn, bg_color=(30, 24, 20)):
    """Create a 480x270 storyboard panel."""
    img  = Image.new('RGB', (PW, PH), bg_color)
    draw = ImageDraw.Draw(img)
    font, font_bold, font_cap, font_ann = load_fonts()

    # Scene draw area
    draw.rectangle([0, 0, PW, DRAW_H], fill=bg_color)

    # Run scene drawing function
    draw_fn(img, draw, font, font_bold, font_cap, font_ann)

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=BORDER_COL, width=BORDER)

    # Shot label (left)
    draw.text((8, DRAW_H + 6), shot_label, font=font_cap, fill=(160, 160, 160))

    # Caption text (wrap at 55 chars, two lines max)
    words = caption_text.split()
    lines = []
    current = ""
    for w in words:
        test = (current + " " + w).strip()
        if len(test) <= 60:
            current = test
        else:
            lines.append(current)
            current = w
    if current:
        lines.append(current)

    for i, line in enumerate(lines[:2]):
        draw.text((8, DRAW_H + 20 + i * 14), line, font=font_cap, fill=TEXT_CAPTION)

    # Panel border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COL, width=BORDER)

    img.save(filepath)
    print(f"  Saved: {os.path.basename(filepath)}")
    return img


def add_glow(img, cx, cy, r_max, color_rgb, steps=6, max_alpha=60):
    """Add concentric glow rings (ADD light via alpha_composite). Never darkens."""
    for i in range(steps, 0, -1):
        r = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow_layer)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r],
                   fill=(*color_rgb, alpha))
        img_rgba = img.convert('RGBA')
        img_rgba = Image.alpha_composite(img_rgba, glow_layer)
        img.paste(img_rgba.convert('RGB'))


def pixel_confetti(draw, cx, cy, spread_x, spread_y, rng, n=10, colors=None):
    """Scatter pixel confetti squares (Glitch Layer intrusion marker)."""
    if colors is None:
        colors = [GLITCH_CYAN, GLITCH_MAG, GLITCH_ACID, GLITCH_PURPLE, GLITCH_WHITE]
    for _ in range(n):
        px = cx + rng.randint(-spread_x, spread_x)
        py = cy + rng.randint(-spread_y, spread_y)
        sz = rng.randint(2, 5)
        col = rng.choice(colors)
        draw.rectangle([px, py, px + sz, py + sz], fill=col)


def draw_byte_cracked_eye_glyph(draw, ex, ey, ew, eh):
    """
    Draw Byte's canonical cracked-eye dead-pixel glyph (7x7 grid, Section 9B).
    ex, ey = top-left corner of eye bezel
    ew, eh = eye bezel width and height
    """
    # Eye bezel background
    draw.rectangle([ex, ey, ex + ew, ey + eh], fill=BYTE_BEZEL)

    # 7x7 grid fits into interior with 2px margin
    margin = max(2, ew // 10)
    gx = ex + margin
    gy = ey + margin
    gw = ew - margin * 2
    gh = eh - margin * 2
    pw_g = gw / 7.0
    ph_g = gh / 7.0

    # Pixel state grid from Section 9B
    # D=DEAD, d=DIM, M=MID, B=BRIGHT, C=CRACK
    grid = [
        ['d', 'd', 'd', 'd', 'C', 'D', 'D'],  # row 0
        ['d', 'M', 'd', 'C', 'D', 'D', 'D'],  # row 1
        ['M', 'd', 'C', 'D', 'D', 'B', 'D'],  # row 2
        ['d', 'C', 'D', 'D', 'B', 'D', 'D'],  # row 3
        ['C', 'D', 'D', 'd', 'd', 'D', 'd'],  # row 4
        ['D', 'D', 'd', 'M', 'd', 'd', 'd'],  # row 5
        ['D', 'C', 'd', 'd', 'M', 'd', 'd'],  # row 6
    ]
    state_map = {
        'D': GLYPH_DEAD,
        'd': GLYPH_DIM,
        'M': GLYPH_MID,
        'B': GLYPH_BRIGHT,
        'C': GLYPH_CRACK,
    }
    for row_i, row in enumerate(grid):
        for col_i, state in enumerate(row):
            px0 = int(gx + col_i * pw_g)
            py0 = int(gy + row_i * ph_g)
            px1 = int(gx + (col_i + 1) * pw_g) - 1
            py1 = int(gy + (row_i + 1) * ph_g) - 1
            draw.rectangle([px0, py0, px1, py1], fill=state_map[state])

    # Crack overlay: diagonal void black line from upper-right to lower-left (over everything)
    draw.line([ex + ew - margin, ey + margin, ex + margin, ey + eh - margin],
              fill=GLYPH_OVER, width=max(1, ew // 18))

    # Chipped corner: upper-right corner of bezel removed (triangular gap)
    chip = max(3, ew // 7)
    draw.polygon([
        (ex + ew - chip, ey),
        (ex + ew, ey),
        (ex + ew, ey + chip),
    ], fill=BYTE_BEZEL)


def draw_byte_normal_eye(draw, ex, ey, ew, eh, expression_dot=True):
    """Draw Byte's normal (left) eye."""
    # Eye bezel
    draw.rectangle([ex, ey, ex + ew, ey + eh], fill=BYTE_BEZEL)
    # Eye white (slightly inset)
    m = max(1, ew // 8)
    draw.rectangle([ex + m, ey + m, ex + ew - m, ey + eh - m], fill=BYTE_EYE_W)
    # Iris
    icx = ex + ew // 2
    icy = ey + eh // 2
    ir = max(3, ew // 3)
    draw.ellipse([icx - ir, icy - ir, icx + ir, icy + ir], fill=BYTE_EYE_CYN)
    # Pupil
    pr = max(2, ir // 2)
    draw.ellipse([icx - pr, icy - pr, icx + pr, icy + pr], fill=BYTE_EYE_PUP)
    # Highlight
    draw.rectangle([icx - ir + 1, icy - ir + 1, icx - ir + 3, icy - ir + 3],
                   fill=STATIC_WHITE)


def draw_byte_oval(img, draw, cx, cy, bw, bh, expression='resigned', lean='slight_forward'):
    """
    Draw Byte's oval body at (cx, cy) center with given dimensions.
    expression: 'resigned', 'vulnerable', 'alarmed', 'grumpy'
    lean: 'slight_forward', 'backward', 'neutral'
    Returns the image (modified in place via PIL operations).
    """
    # Lean offset
    lean_dx = {'slight_forward': 4, 'backward': -8, 'neutral': 0}.get(lean, 0)
    lean_dy = {'slight_forward': 2, 'backward': -4, 'neutral': 0}.get(lean, 0)

    # Body oval (main tone)
    bx = cx - bw // 2 + lean_dx
    by = cy - bh // 2 + lean_dy
    draw.ellipse([bx, by, bx + bw, by + bh], fill=BYTE_BODY, outline=BYTE_OUTLINE, width=2)

    # Shadow underside
    shadow_bh = bh // 3
    draw.ellipse([bx, by + bh - shadow_bh, bx + bw, by + bh],
                 fill=BYTE_DARK, outline=BYTE_OUTLINE, width=1)

    # Highlight top arc
    hl_bw = bw * 2 // 3
    hl_bh = bh // 4
    hl_bx = bx + (bw - hl_bw) // 2
    draw.ellipse([hl_bx, by + 2, hl_bx + hl_bw, by + hl_bh + 2],
                 fill=(80, 230, 245))

    # Hot Magenta scar: diagonal from upper-right to lower-left
    scar_x1 = bx + bw * 3 // 4
    scar_y1 = by + bh // 6
    scar_x2 = bx + bw // 4
    scar_y2 = by + bh * 5 // 6
    draw.line([scar_x1, scar_y1, scar_x2, scar_y2], fill=BYTE_SCAR, width=max(2, bw // 20))
    # Secondary scar scatter
    sx = bx + bw // 2
    sy = by + bh // 2
    for offx, offy, sw, sh in [(6, -4, 4, 3), (-5, 5, 3, 2), (8, 8, 5, 2)]:
        draw.rectangle([sx + offx, sy + offy, sx + offx + sw, sy + offy + sh],
                       fill=BYTE_SCAR_DIM)

    # Eyes: left=normal (viewer right), right=cracked (viewer left)
    face_cx = cx + lean_dx
    face_cy = cy + lean_dy

    ew = max(12, bw // 5)
    eh = max(9, bh // 5)
    eye_sep = bw // 4

    # Normal eye (viewer's RIGHT = character's left)
    nex = face_cx + eye_sep // 2 - ew // 2
    ney = face_cy - eh // 2 - 2
    draw_byte_normal_eye(draw, nex, ney, ew, eh)

    # Cracked eye (viewer's LEFT = character's right)
    cex = face_cx - eye_sep // 2 - ew // 2
    cey = face_cy - eh // 2 - 2

    # Apply glyph if eye is large enough (20px+ width threshold from spec)
    if ew >= 14:
        draw_byte_cracked_eye_glyph(draw, cex, cey, ew, eh)
    else:
        # Simplified two-tone at small scale
        draw.rectangle([cex, cey, cex + ew, cey + eh], fill=GLYPH_DEAD)
        draw.line([cex + ew, cey, cex, cey + eh], fill=GLYPH_CRACK, width=1)

    # Mouth shape per expression
    mx = face_cx - bw // 10
    my = face_cy + bh // 5
    mw = bw // 5

    if expression == 'resigned':
        # Flat resigned line, slightly downturned at ends
        draw.line([mx, my, mx + mw, my], fill=BYTE_OUTLINE, width=2)
        draw.line([mx, my, mx + 2, my + 2], fill=BYTE_OUTLINE, width=2)
        draw.line([mx + mw, my, mx + mw - 2, my + 2], fill=BYTE_OUTLINE, width=2)
    elif expression == 'vulnerable':
        # Slight open mouth — suggests he's about to say something honest
        draw.ellipse([mx, my - 2, mx + mw, my + mw // 2], fill=(10, 10, 20))
    elif expression == 'alarmed':
        # Wide open, small oval
        draw.ellipse([mx - 2, my - 3, mx + mw + 2, my + mw // 2 + 3],
                     fill=(10, 10, 20), outline=BYTE_OUTLINE, width=1)
    else:  # grumpy
        # Downturned ends
        draw.arc([mx - 2, my - 6, mx + mw + 2, my + 4], start=200, end=340,
                 fill=BYTE_OUTLINE, width=2)

    # Limbs per expression / lean
    limb_len = max(10, bw // 4)

    if expression == 'resigned':
        # Grumpy neutral: arms flat against sides
        # Left arm
        draw.line([bx + lean_dx - 2, by + bh // 2 + lean_dy,
                   bx + lean_dx - limb_len, by + bh // 2 + 4 + lean_dy],
                  fill=BYTE_OUTLINE, width=max(3, bw // 12))
        # Right arm
        draw.line([bx + bw + lean_dx + 2, by + bh // 2 + lean_dy,
                   bx + bw + lean_dx + limb_len, by + bh // 2 + 4 + lean_dy],
                  fill=BYTE_OUTLINE, width=max(3, bw // 12))
    elif expression == 'vulnerable':
        # Arms slightly inward, body language uncertain
        draw.line([bx + lean_dx - 2, by + bh // 2 + lean_dy,
                   bx + lean_dx - limb_len + 5, by + bh // 2 + 10 + lean_dy],
                  fill=BYTE_OUTLINE, width=max(3, bw // 12))
        draw.line([bx + bw + lean_dx + 2, by + bh // 2 + lean_dy,
                   bx + bw + lean_dx + limb_len - 5, by + bh // 2 + 10 + lean_dy],
                  fill=BYTE_OUTLINE, width=max(3, bw // 12))

    # Lower limbs (legs)
    draw.line([face_cx - bw // 5 + lean_dx, by + bh + lean_dy,
               face_cx - bw // 4 + lean_dx, by + bh + limb_len + lean_dy],
              fill=BYTE_OUTLINE, width=max(3, bw // 12))
    draw.line([face_cx + bw // 5 + lean_dx, by + bh + lean_dy,
               face_cx + bw // 4 + lean_dx, by + bh + limb_len + lean_dy],
              fill=BYTE_OUTLINE, width=max(3, bw // 12))

    # Floating pixel confetti below legs
    rng = random.Random(cx + cy)  # deterministic per position
    for _ in range(8):
        px = face_cx + lean_dx + rng.randint(-bw // 2, bw // 2)
        py = by + bh + limb_len + rng.randint(2, 8)
        sz = rng.randint(2, 4)
        col = rng.choice([GLITCH_CYAN, GLITCH_MAG, GLITCH_ACID, GLITCH_WHITE])
        draw.rectangle([px, py, px + sz, py + sz], fill=col)


# ═══════════════════════════════════════════════════════════════════════════════
#  PANEL A1-04 — Near-miss micro-beat (classroom)
# ═══════════════════════════════════════════════════════════════════════════════

def draw_a104(img, draw, font, font_bold, font_cap, font_ann):
    """
    A1-04: Science class. Luma in foreground, teacher at binary lesson board (background),
    Byte napping in eraser bits on Luma's desk tray (right foreground).
    Triangle of sight lines tells the story: Luma eyes up → board → gaze snaps to Byte.
    Near-miss — she almost connects.
    """
    rng = random.Random(1404)

    # ── Background: classroom (dusty lavender + sage green) ──────────────────
    # Wall
    draw.rectangle([0, 0, PW, DRAW_H], fill=COOL_SCHOOL)

    # Floor
    floor_y = DRAW_H - 50
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=SCHOOL_FLOOR)
    draw.line([0, floor_y, PW, floor_y], fill=(110, 100, 90), width=2)

    # Ceiling strip
    draw.rectangle([0, 0, PW, 12], fill=(150, 145, 175))

    # Desks in back rows (simple perspective perspective — smaller, higher up)
    for col in range(4):
        dx = 40 + col * 95
        dy = 90
        dw, dh = 70, 18
        draw.rectangle([dx, dy, dx + dw, dy + dh], fill=DESK_TAN,
                       outline=(140, 120, 95), width=1)
        # Student silhouettes (simple circles for heads)
        hcx = dx + dw // 2
        hcy = dy - 14
        draw.ellipse([hcx - 8, hcy - 8, hcx + 8, hcy + 8],
                     fill=(165, 115, 70), outline=(30, 20, 10), width=1)

    # ── Blackboard (upper center-right, clearly readable) ──────────────────
    brd_x, brd_y, brd_w, brd_h = 180, 12, 240, 68
    draw.rectangle([brd_x, brd_y, brd_x + brd_w, brd_y + brd_h],
                   fill=BOARD_GREEN, outline=(32, 56, 40), width=3)

    # Board header text
    draw.text((brd_x + 8, brd_y + 6), "BINARY SYSTEMS", font=font_cap, fill=BOARD_TEXT)
    draw.text((brd_x + 8, brd_y + 22), "HOW COMPUTERS STORE DATA", font=font_ann, fill=BOARD_TEXT)

    # Binary lesson: rows of 1s and 0s
    binary_row = "  0 1 1 0  0 1 0 1  1 0 1 1"
    draw.text((brd_x + 8, brd_y + 38), binary_row, font=font_ann, fill=(200, 225, 200))
    draw.text((brd_x + 8, brd_y + 52), "  1 0 0 1  1 1 0 0  0 1 0 0", font=font_ann, fill=(200, 225, 200))

    # Chalk dust smudge at board base
    for i in range(6):
        cx_d = brd_x + 10 + i * 35
        draw.ellipse([cx_d, brd_y + brd_h - 4, cx_d + 25, brd_y + brd_h + 2],
                     fill=(200, 215, 205))

    # ── Teacher (Ms. Okafor) silhouette at the board ──────────────────────
    tcx = brd_x + 20
    tcy = brd_y + brd_h + 2
    # Body: dark warm figure
    T_SKIN = (160, 100, 55)
    T_DRESS = (40, 50, 70)
    draw.ellipse([tcx - 12, tcy, tcx + 12, tcy + 20], fill=T_SKIN, outline=(20, 12, 6), width=1)  # head
    draw.ellipse([tcx - 16, tcy + 18, tcx + 16, tcy + 50], fill=T_DRESS, outline=(20, 12, 6), width=1)  # body
    # Arm reaching to board
    draw.line([tcx + 14, tcy + 28, brd_x + 38, brd_y + 55], fill=T_SKIN, width=4)

    # Subtle projector flicker (overhead projector pixel artifact — no one notices except Luma)
    proj_cx = 240
    proj_cy = 8
    proj_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    proj_d = ImageDraw.Draw(proj_layer)
    proj_d.ellipse([proj_cx - 15, proj_cy - 4, proj_cx + 15, proj_cy + 12],
                   fill=(*GLITCH_CYAN, 25))
    img_rgba = img.convert('RGBA')
    img_rgba = Image.alpha_composite(img_rgba, proj_layer)
    img.paste(img_rgba.convert('RGB'))
    draw = ImageDraw.Draw(img)  # refresh draw handle

    # 2 tiny pixel confetti on projector (very subtle)
    for _ in range(2):
        px = proj_cx + rng.randint(-20, 20)
        py = proj_cy + rng.randint(-3, 10)
        draw.rectangle([px, py, px + 2, py + 2], fill=GLITCH_CYAN)

    # ── Luma (foreground, left of center — lower placement = effort/discovery) ─
    # Luma is in the back row, but compositionally she dominates the foreground
    luma_cx = 140
    luma_cy = DRAW_H - 80

    # Desk surface (Luma's desk, foreground, large)
    desk_x = 30
    desk_y = luma_cy + 25
    desk_w = 200
    desk_h = 22
    draw.rectangle([desk_x, desk_y, desk_x + desk_w, desk_y + desk_h],
                   fill=DESK_TAN, outline=(140, 120, 95), width=2)

    # Desk leg (perspective)
    draw.line([desk_x + 20, desk_y + desk_h, desk_x + 10, DRAW_H],
              fill=(130, 110, 85), width=3)

    # Notebook on desk (Luma's project — margin drawings visible)
    nb_x = desk_x + 25
    nb_y = desk_y - 18
    draw.rectangle([nb_x, nb_y, nb_x + 90, nb_y + 18], fill=(240, 237, 225),
                   outline=(60, 50, 40), width=1)
    # Glitchkin doodles in notebook margin
    for i in range(3):
        mx_d = nb_x + 5 + i * 26
        my_d = nb_y + 4
        draw.polygon([(mx_d, my_d + 8), (mx_d + 8, my_d), (mx_d + 16, my_d + 8),
                      (mx_d + 12, my_d + 14), (mx_d + 4, my_d + 14)],
                     outline=LUMA_HAIR, fill=None)

    # Eraser tray with eraser bits (right side of desk) — Byte naps here
    tray_x = desk_x + desk_w - 55
    tray_y = desk_y - 8
    draw.rectangle([tray_x, tray_y, tray_x + 48, tray_y + 8],
                   fill=(200, 195, 185), outline=(160, 155, 145), width=1)
    # Eraser bits/crumbs
    for i in range(6):
        ex_b = tray_x + 3 + i * 7
        ey_b = tray_y + 1 + rng.randint(0, 3)
        draw.ellipse([ex_b, ey_b, ex_b + 5, ey_b + 3], fill=(215, 210, 200))

    # Byte napping on eraser tray (small, charming) — uses full glyph since ~30px wide
    byte_cx_desk = tray_x + 24
    byte_cy_desk = tray_y - 14
    byte_bw = 28
    byte_bh = 22
    # Body
    draw.ellipse([byte_cx_desk - byte_bw // 2, byte_cy_desk - byte_bh // 2,
                  byte_cx_desk + byte_bw // 2, byte_cy_desk + byte_bh // 2],
                 fill=BYTE_BODY, outline=BYTE_OUTLINE, width=2)
    # Scar
    draw.line([byte_cx_desk + 6, byte_cy_desk - 8, byte_cx_desk - 6, byte_cy_desk + 8],
              fill=BYTE_SCAR, width=2)
    # Eyes: closed for napping (simple arcs)
    ne_cx = byte_cx_desk + 5
    ce_cx = byte_cx_desk - 5
    eye_y = byte_cy_desk - 2
    draw.arc([ne_cx - 5, eye_y - 3, ne_cx + 5, eye_y + 3], start=0, end=180,
             fill=BYTE_OUTLINE, width=2)
    draw.arc([ce_cx - 5, eye_y - 3, ce_cx + 5, eye_y + 3], start=0, end=180,
             fill=BYTE_OUTLINE, width=2)
    # Small ZZZ for napping
    draw.text((byte_cx_desk + 10, byte_cy_desk - 18), "z", font=font_ann,
              fill=(140, 180, 200))
    draw.text((byte_cx_desk + 15, byte_cy_desk - 24), "Z", font=font_ann,
              fill=(140, 180, 200))

    # Luma body (seated, upper body visible above desk)
    # Head — positioned to show gaze direction (looking UP toward board)
    head_cx = luma_cx
    head_cy = luma_cy - 15
    head_r = 26

    # Head tilt: looking upward (face center raised, eyes shifted up)
    draw.ellipse([head_cx - head_r, head_cy - head_r - 5,
                  head_cx + head_r, head_cy + head_r - 5],
                 fill=LUMA_SKIN, outline=LUMA_OUTLINE, width=2)

    # Hair
    draw.ellipse([head_cx - head_r - 3, head_cy - head_r - 8,
                  head_cx + head_r + 3, head_cy + 4],
                 fill=LUMA_HAIR, outline=LUMA_OUTLINE, width=2)

    # Eyes — shifted UPWARD (she's looking toward the board)
    eye_base_y = head_cy - 14  # elevated (looking up)
    # Right eye (viewer left)
    draw.ellipse([head_cx - 16, eye_base_y - 5, head_cx - 4, eye_base_y + 5],
                 fill=(255, 255, 255), outline=LUMA_OUTLINE, width=1)
    draw.ellipse([head_cx - 14, eye_base_y - 3, head_cx - 6, eye_base_y + 3],
                 fill=(50, 35, 20))
    # Left eye (viewer right)
    draw.ellipse([head_cx + 4, eye_base_y - 5, head_cx + 16, eye_base_y + 5],
                 fill=(255, 255, 255), outline=LUMA_OUTLINE, width=1)
    draw.ellipse([head_cx + 6, eye_base_y - 3, head_cx + 14, eye_base_y + 3],
                 fill=(50, 35, 20))
    # Pupils (looking slightly up and to the right toward board)
    draw.ellipse([head_cx - 11, eye_base_y - 4, head_cx - 7, eye_base_y],
                 fill=(20, 10, 5))
    draw.ellipse([head_cx + 9, eye_base_y - 4, head_cx + 13, eye_base_y],
                 fill=(20, 10, 5))

    # Slight wide-eye expression (almost making connection): wider eye highlights
    draw.rectangle([head_cx - 13, eye_base_y - 3, head_cx - 11, eye_base_y - 1],
                   fill=(255, 255, 255))
    draw.rectangle([head_cx + 11, eye_base_y - 3, head_cx + 13, eye_base_y - 1],
                   fill=(255, 255, 255))

    # Mouth: slightly open (concentration / almost-connection)
    draw.arc([head_cx - 8, head_cy - 3, head_cx + 8, head_cy + 5],
             start=0, end=180, fill=LUMA_OUTLINE, width=2)

    # Body / hoodie
    draw.ellipse([head_cx - 22, head_cy + 16, head_cx + 22, head_cy + 50],
                 fill=LUMA_PJ, outline=LUMA_OUTLINE, width=2)

    # ── SIGHT LINE INDICATORS (compositional storytelling) ──────────────────
    # Luma's eyeline up to board (dashed cyan line — subtle)
    board_target_x = brd_x + 80
    board_target_y = brd_y + 35
    eye_start_x = head_cx + 10
    eye_start_y = head_cy - 14

    # Draw as dotted line
    dx_line = board_target_x - eye_start_x
    dy_line = board_target_y - eye_start_y
    length = math.sqrt(dx_line**2 + dy_line**2)
    if length > 0:
        ux, uy = dx_line / length, dy_line / length
        t = 0
        while t < length - 10:
            x1 = int(eye_start_x + ux * t)
            y1 = int(eye_start_y + uy * t)
            x2 = int(eye_start_x + ux * min(t + 6, length))
            y2 = int(eye_start_y + uy * min(t + 6, length))
            # Use a faint glow layer for the dotted line
            sightline_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
            sld = ImageDraw.Draw(sightline_layer)
            sld.line([x1, y1, x2, y2], fill=(*GLITCH_CYAN, 55), width=1)
            img_rgba = img.convert('RGBA')
            img_rgba = Image.alpha_composite(img_rgba, sightline_layer)
            img.paste(img_rgba.convert('RGB'))
            draw = ImageDraw.Draw(img)
            t += 12

    # Small annotation: "ALMOST..."
    draw.text((head_cx - 5, eye_base_y - 18), "almost...",
              font=font_ann, fill=(100, 80, 60))

    # ── Annotation arrows ──────────────────────────────────────────────────
    # Board label
    draw.text((brd_x + 5, brd_y + brd_h + 8), "BINARY LESSON", font=font_ann, fill=(80, 110, 90))
    # Byte label
    draw.text((tray_x + 2, tray_y - 28), "Byte (napping)", font=font_ann, fill=(0, 180, 200))
    # Luma label
    draw.text((luma_cx - head_r - 25, luma_cy - 40), "Luma", font=font_ann, fill=(140, 90, 50))


# ═══════════════════════════════════════════════════════════════════════════════
#  PANEL A2-02 — Byte MCU vulnerability
# ═══════════════════════════════════════════════════════════════════════════════

def draw_a202(img, draw, font, font_bold, font_cap, font_ann):
    """
    A2-02: Byte MCU. His face fills most of the frame.
    Cracked eye IS the emotional center. Expression: resigned/vulnerable.
    Luma visible in background-right at ~20% weight (blurred).
    Warm background tint — Byte in real world, uncomfortable.
    Cracked eye uses full dead-pixel glyph (eye rendered large enough for 7x7 grid).
    """
    rng = random.Random(2202)

    # ── Background: warm living room / tech den (Byte in real world = uncomfortable) ─
    # Warm amber gradient — real world colour palette
    for y in range(DRAW_H):
        t = y / DRAW_H
        r = int(110 * (1 - t) + 55 * t)
        g = int(85 * (1 - t) + 38 * t)
        b = int(55 * (1 - t) + 24 * t)
        draw.line([0, y, PW, y], fill=(r, g, b))

    # Soft floor line
    floor_y = DRAW_H - 40
    draw.line([0, floor_y, PW, floor_y], fill=(45, 30, 18), width=1)

    # ── Luma in background (right, ~20% weight, intentionally blurred/soft) ─
    # Render at low saturation and reduced contrast — she's background
    luma_bg_cx = 380
    luma_bg_cy = DRAW_H // 2 + 20
    luma_bg_r = 28

    # Background head — muted, de-saturated
    bg_skin = (190, 150, 120)  # desaturated toward warm neutral
    draw.ellipse([luma_bg_cx - luma_bg_r, luma_bg_cy - luma_bg_r - 5,
                  luma_bg_cx + luma_bg_r, luma_bg_cy + luma_bg_r - 5],
                 fill=bg_skin, outline=(130, 100, 75), width=1)
    draw.ellipse([luma_bg_cx - luma_bg_r - 3, luma_bg_cy - luma_bg_r - 9,
                  luma_bg_cx + luma_bg_r + 3, luma_bg_cy + 4],
                 fill=(60, 45, 30), outline=(50, 35, 22), width=1)
    # Luma body (crouching, leaning forward = intense listening)
    draw.ellipse([luma_bg_cx - 20, luma_bg_cy + 18, luma_bg_cx + 20, luma_bg_cy + 50],
                 fill=(145, 185, 165), outline=(100, 130, 115), width=1)
    # Eyes — forward focus (looking at Byte)
    for ex_off in [-10, 5]:
        draw.ellipse([luma_bg_cx + ex_off, luma_bg_cy - 8,
                      luma_bg_cx + ex_off + 8, luma_bg_cy - 2],
                     fill=(230, 230, 230), outline=(100, 80, 60), width=1)
        draw.ellipse([luma_bg_cx + ex_off + 2, luma_bg_cy - 7,
                      luma_bg_cx + ex_off + 6, luma_bg_cy - 3],
                     fill=(40, 28, 15))

    # Cosmo: barely visible blur in very back
    cosmo_bg_cx = 440
    cosmo_bg_cy = DRAW_H // 2 + 10
    draw.ellipse([cosmo_bg_cx - 18, cosmo_bg_cy - 18, cosmo_bg_cx + 18, cosmo_bg_cy + 18],
                 fill=(155, 105, 65), outline=(100, 75, 50), width=1)

    # ── Coffee table surface (Byte is ON the table) ──────────────────────
    table_y = DRAW_H - 55
    table_x = 80
    table_w = 250
    table_h = 14
    draw.rectangle([table_x, table_y, table_x + table_w, table_y + table_h],
                   fill=(90, 68, 44), outline=(60, 44, 28), width=2)

    # ── BYTE — large MCU (fills 55% of frame width) ──────────────────────
    # Per spec: cracked eye at ~30% of frame width = 144px
    # Byte centered slightly left of center
    byte_cx = 200
    byte_cy = DRAW_H // 2 + 10
    byte_bw = 150   # wide — he fills the frame in MCU
    byte_bh = 120

    # ── Body ──────────────────────────────────────────────────────────────
    bx = byte_cx - byte_bw // 2
    by = byte_cy - byte_bh // 2

    # Main body oval
    draw.ellipse([bx, by, bx + byte_bw, by + byte_bh],
                 fill=BYTE_BODY, outline=BYTE_OUTLINE, width=3)

    # Underside shadow
    draw.ellipse([bx, by + byte_bh - byte_bh // 3,
                  bx + byte_bw, by + byte_bh],
                 fill=BYTE_DARK)

    # Highlight
    hl_w = byte_bw * 2 // 3
    draw.ellipse([bx + (byte_bw - hl_w) // 2, by + 4,
                  bx + (byte_bw - hl_w) // 2 + hl_w, by + byte_bh // 5],
                 fill=(80, 230, 245))

    # Hot Magenta scar — prominent at MCU scale
    sx1 = bx + byte_bw * 3 // 4
    sy1 = by + byte_bh // 8
    sx2 = bx + byte_bw // 5
    sy2 = by + byte_bh * 7 // 8
    draw.line([sx1, sy1, sx2, sy2], fill=BYTE_SCAR, width=5)
    # Scar scatter
    for offx, offy, sw, sh in [(12, -8, 8, 5), (-10, 12, 6, 4), (18, 18, 10, 4)]:
        draw.rectangle([byte_cx + offx, byte_cy + offy,
                        byte_cx + offx + sw, byte_cy + offy + sh],
                       fill=BYTE_SCAR_DIM)

    # Glow corona around Byte (he's in the real world — digital presence is uneasy)
    add_glow(img, byte_cx, byte_cy, 90, GLITCH_CYAN, steps=5, max_alpha=35)
    draw = ImageDraw.Draw(img)

    # ── EYES — at MCU scale: cracked eye is ~40px wide, well above the 20px threshold ─
    # Eye dimensions at this scale
    ew_mcu = 42
    eh_mcu = 32
    eye_sep_mcu = byte_bw // 3

    face_cx = byte_cx
    face_cy = byte_cy - 5

    # Normal eye (viewer's RIGHT)
    nex = face_cx + eye_sep_mcu // 2 - ew_mcu // 2
    ney = face_cy - eh_mcu // 2 - 4

    # Cracked eye (viewer's LEFT) — THIS IS THE EMOTIONAL CENTER OF THE PANEL
    cex = face_cx - eye_sep_mcu // 2 - ew_mcu // 2
    cey = face_cy - eh_mcu // 2 - 4

    # Normal eye
    draw_byte_normal_eye(draw, nex, ney, ew_mcu, eh_mcu)

    # Cracked eye — full 7x7 dead-pixel glyph (per Section 9B)
    draw_byte_cracked_eye_glyph(draw, cex, cey, ew_mcu, eh_mcu)

    # Extra glow on cracked eye (it flickers / costs him to display)
    add_glow(img, cex + ew_mcu // 2, cey + eh_mcu // 2, 30, GLYPH_CRACK[:3], steps=4, max_alpha=45)
    draw = ImageDraw.Draw(img)

    # ── Mouth: VULNERABLE — slightly open, bottom lip drawn down ──────────
    mx = face_cx - 14
    my = face_cy + byte_bh // 5 - 5
    mw = 28
    # Slightly open oval
    draw.ellipse([mx, my - 4, mx + mw, my + mw // 2 + 2],
                 fill=(10, 10, 20), outline=BYTE_OUTLINE, width=2)

    # ── Arms: inward / uncertain body language ────────────────────────────
    limb_w = max(6, byte_bw // 18)
    # Left arm (inward)
    draw.line([bx - 2, by + byte_bh // 2,
               bx - byte_bw // 5, by + byte_bh * 2 // 3],
              fill=BYTE_OUTLINE, width=limb_w)
    # Right arm (inward)
    draw.line([bx + byte_bw + 2, by + byte_bh // 2,
               bx + byte_bw + byte_bw // 5, by + byte_bh * 2 // 3],
              fill=BYTE_OUTLINE, width=limb_w)

    # Lower limbs
    draw.line([face_cx - byte_bw // 5, by + byte_bh,
               face_cx - byte_bw // 4, by + byte_bh + 30],
              fill=BYTE_OUTLINE, width=limb_w)
    draw.line([face_cx + byte_bw // 5, by + byte_bh,
               face_cx + byte_bw // 4, by + byte_bh + 30],
              fill=BYTE_OUTLINE, width=limb_w)

    # Pixel confetti beneath Byte (floating)
    pixel_confetti(draw, byte_cx, by + byte_bh + 35, 50, 12, rng, n=12)

    # ── Warm discomfort glow around feet / table surface ──────────────────
    add_glow(img, byte_cx, table_y, 60, (200, 100, 40), steps=4, max_alpha=30)
    draw = ImageDraw.Draw(img)

    # Desaturation ring at feet (digital/analogue boundary indicator)
    ring_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring_layer)
    rd.ellipse([byte_cx - 70, table_y - 10, byte_cx + 70, table_y + 14],
               fill=(220, 210, 200, 30))
    img_rgba = img.convert('RGBA')
    img_rgba = Image.alpha_composite(img_rgba, ring_layer)
    img.paste(img_rgba.convert('RGB'))
    draw = ImageDraw.Draw(img)

    # ── Annotation labels ────────────────────────────────────────────────
    draw.text((cex + 2, cey - 14), "CRACKED EYE", font=font_ann, fill=GLYPH_CRACK)
    draw.text((cex + 2, cey - 5), "dead-pixel state", font=font_ann, fill=(180, 100, 130))
    draw.text((luma_bg_cx - 25, luma_bg_cy - 40), "Luma ~20% weight", font=font_ann,
              fill=(160, 130, 100))
    draw.text((byte_cx - 30, by - 18), "BYTE MCU", font=font_ann, fill=BYTE_SCAR)
    draw.text((byte_cx - 45, by - 8), "expression: resigned / vulnerable", font=font_ann,
              fill=(140, 180, 200))


# ═══════════════════════════════════════════════════════════════════════════════
#  PANEL A2-05b — Cosmo using Glitch Frequency app
# ═══════════════════════════════════════════════════════════════════════════════

def draw_a205b(img, draw, font, font_bold, font_cap, font_ann):
    """
    A2-05b: Cosmo MCU on Millbrook street.
    Phone with Glitch Frequency app running — screen clearly visible.
    Confident pose, determined face. Flickering streetlight behind him.
    Terracotta + cream exterior palette.
    """
    rng = random.Random(2205)

    # ── Exterior background: Millbrook street ────────────────────────────
    # Sky: pale cream / late afternoon
    sky_top = (235, 225, 205)
    sky_bot = (210, 195, 175)
    for y in range(DRAW_H):
        t = y / DRAW_H
        r = int(sky_top[0] * (1 - t) + sky_bot[0] * t)
        g = int(sky_top[1] * (1 - t) + sky_bot[1] * t)
        b = int(sky_top[2] * (1 - t) + sky_bot[2] * t)
        draw.line([0, y, PW, y], fill=(r, g, b))

    # Street (terracotta sidewalk)
    street_y = DRAW_H - 55
    draw.rectangle([0, street_y, PW, DRAW_H], fill=STREET_TERRA)
    # Sidewalk cracks
    draw.line([0, street_y + 18, PW, street_y + 18], fill=(160, 110, 75), width=1)
    draw.line([120, street_y, 115, DRAW_H], fill=(160, 110, 75), width=1)
    draw.line([300, street_y, 305, DRAW_H], fill=(160, 110, 75), width=1)

    # Buildings in background (terracotta + cream blocks)
    for bx_b, bw_b, bh_b, bc in [
        (0, 80, 90, (185, 140, 105)),
        (85, 120, 110, (200, 165, 130)),
        (210, 90, 85, (175, 130, 95)),
        (305, 100, 100, (190, 155, 120)),
        (410, 75, 80, (180, 145, 108)),
    ]:
        bby = street_y - bh_b
        draw.rectangle([bx_b, bby, bx_b + bw_b, street_y],
                       fill=bc, outline=(140, 100, 70), width=1)
        # Windows
        for wx in range(2):
            for wy in range(2):
                wxx = bx_b + 15 + wx * 35
                wyy = bby + 15 + wy * 30
                if wxx + 18 < bx_b + bw_b and wyy + 20 < street_y:
                    draw.rectangle([wxx, wyy, wxx + 18, wyy + 20],
                                   fill=(210, 195, 160), outline=(130, 100, 70), width=1)

    # ── Streetlight (background, flickering — Glitch Layer signature) ─────
    pole_x = 360
    pole_y = street_y
    draw.line([pole_x, pole_y, pole_x, street_y - 80], fill=(90, 85, 80), width=5)
    # Lamp head
    draw.rectangle([pole_x - 18, street_y - 90, pole_x + 18, street_y - 78],
                   fill=(100, 95, 90), outline=(70, 65, 60), width=2)

    # Flickering light (Glitch Layer pattern — cyan)
    lamp_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(lamp_layer)
    # Main light pool
    ld.ellipse([pole_x - 40, street_y - 95, pole_x + 40, street_y - 65],
               fill=(*GLITCH_CYAN, 55))
    # Flicker artifact on lamp
    ld.rectangle([pole_x - 8, street_y - 88, pole_x + 8, street_y - 80],
                 fill=(*GLITCH_CYAN, 120))
    img_rgba = img.convert('RGBA')
    img_rgba = Image.alpha_composite(img_rgba, lamp_layer)
    img.paste(img_rgba.convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Pixel confetti near streetlight (active Glitch Layer intrusion)
    pixel_confetti(draw, pole_x, street_y - 85, 30, 20, rng, n=8)
    # Small glitch annotation
    draw.text((pole_x - 28, street_y - 110), "GLITCH SIGNAL", font=font_ann,
              fill=GLITCH_CYAN)

    # ── COSMO (center, confident pose) ───────────────────────────────────
    cosmo_cx = 190
    cosmo_cy = DRAW_H // 2 + 5

    # Body
    body_top = cosmo_cy + 20
    draw.ellipse([cosmo_cx - 30, body_top, cosmo_cx + 30, body_top + 70],
                 fill=COSMO_SHIRT, outline=COSMO_OUTLINE, width=2)

    # Head
    draw.ellipse([cosmo_cx - 26, cosmo_cy - 28, cosmo_cx + 26, cosmo_cy + 22],
                 fill=COSMO_SKIN, outline=COSMO_OUTLINE, width=2)
    # Hair (Cosmo: dark, neat, rectangular language)
    draw.rectangle([cosmo_cx - 26, cosmo_cy - 28, cosmo_cx + 26, cosmo_cy - 14],
                   fill=COSMO_HAIR, outline=COSMO_OUTLINE, width=1)

    # Glasses (large rectangular frames — character detail)
    for ex_off, eye_cx_g in [(-14, cosmo_cx - 10), (6, cosmo_cx + 10)]:
        draw.rectangle([cosmo_cx + ex_off - 14, cosmo_cy - 12,
                        cosmo_cx + ex_off + 14, cosmo_cy + 4],
                       outline=COSMO_OUTLINE, width=3)
        # Lens
        draw.rectangle([cosmo_cx + ex_off - 12, cosmo_cy - 10,
                        cosmo_cx + ex_off + 12, cosmo_cy + 2],
                       fill=(210, 215, 230))
        # Eye behind lens (determined look)
        draw.ellipse([eye_cx_g - 5, cosmo_cy - 8, eye_cx_g + 5, cosmo_cy],
                     fill=(40, 28, 15))

    # Mouth: confident set — slight compression, ready
    draw.arc([cosmo_cx - 10, cosmo_cy + 6, cosmo_cx + 10, cosmo_cy + 16],
             start=20, end=160, fill=COSMO_OUTLINE, width=2)

    # Left arm holding phone (raised, confident grip)
    arm_ex = cosmo_cx - 24
    arm_ey = body_top + 15
    phone_cx = cosmo_cx - 60
    phone_cy = cosmo_cy + 5
    # Arm
    draw.line([arm_ex, arm_ey, phone_cx + 25, phone_cy + 55],
              fill=COSMO_SKIN, width=10)

    # ── PHONE (left foreground, app screen prominent) ─────────────────────
    ph_x = phone_cx - 30
    ph_y = phone_cy - 55
    ph_w = 68
    ph_h = 118

    # Phone body
    draw.rounded_rectangle([ph_x, ph_y, ph_x + ph_w, ph_y + ph_h],
                            radius=8, fill=PHONE_DARK, outline=PHONE_SILVER, width=3)

    # Screen (inset)
    sc_x = ph_x + 5
    sc_y = ph_y + 8
    sc_w = ph_w - 10
    sc_h = ph_h - 20

    # App background
    draw.rectangle([sc_x, sc_y, sc_x + sc_w, sc_y + sc_h], fill=APP_BG)

    # App grid overlay (pixel grid)
    for grid_x in range(sc_x, sc_x + sc_w, 8):
        draw.line([grid_x, sc_y, grid_x, sc_y + sc_h], fill=(*APP_GRID, ), width=1)
    for grid_y in range(sc_y, sc_y + sc_h, 8):
        draw.line([sc_x, grid_y, sc_x + sc_w, grid_y], fill=APP_GRID, width=1)

    # App header: "GLITCH FREQ" label
    draw.text((sc_x + 2, sc_y + 2), "GLITCH FREQ", font=font_ann, fill=APP_CYAN)

    # Waveform visualization (frequency readout — active)
    wf_base_y = sc_y + 35
    wf_pts = []
    wf_rng = random.Random(42)
    for i in range(12):
        wx = sc_x + 3 + i * (sc_w - 6) // 11
        wy = wf_base_y - wf_rng.randint(4, 22)
        wf_pts.append((wx, wy))
        wf_pts_bottom = [(wx, wf_base_y)]
        draw.line([(wx, wy), (wx, wf_base_y)], fill=APP_GREEN, width=2)

    # Waveform connecting line
    if len(wf_pts) > 1:
        draw.line(wf_pts, fill=APP_CYAN, width=1)

    # Numeric frequency readout
    draw.text((sc_x + 2, wf_base_y + 8), "FREQ: 7.34 GHz", font=font_ann, fill=APP_GREEN)
    draw.text((sc_x + 2, wf_base_y + 18), "SIGNAL: ACTIVE", font=font_ann, fill=APP_CYAN)
    draw.text((sc_x + 2, wf_base_y + 28), ">>> SCANNING...", font=font_ann, fill=APP_GREEN)

    # Screen glow (phone illuminating Cosmo's face)
    add_glow(img, ph_x + ph_w // 2, ph_y + ph_h // 2, 55, APP_CYAN[:3], steps=5, max_alpha=40)
    draw = ImageDraw.Draw(img)

    # Annotations
    draw.text((ph_x - 5, ph_y - 16), "GLITCH FREQ APP", font=font_ann, fill=APP_CYAN)
    draw.text((ph_x - 5, ph_y - 7), "active / scanning", font=font_ann, fill=APP_GREEN)
    draw.text((cosmo_cx + 28, cosmo_cy - 30), "Cosmo: confident", font=font_ann,
              fill=(100, 80, 60))
    draw.text((cosmo_cx + 28, cosmo_cy - 21), "pre-failure pose", font=font_ann,
              fill=(120, 95, 70))


# ═══════════════════════════════════════════════════════════════════════════════
#  PANEL A2-06 — App failure INSERT
# ═══════════════════════════════════════════════════════════════════════════════

def draw_a206(img, draw, font, font_bold, font_cap, font_ann):
    """
    A2-06: INSERT — phone screen close-up. App crashes. Static/glitch fills screen.
    No Cosmo visible. Pure screen insert. Should feel like a punch cut.
    480x270 filled almost entirely with the phone screen.
    """
    rng = random.Random(2206)

    # ── FULL FRAME PHONE SCREEN (fills the frame — INSERT framing) ────────
    # Black field first
    draw.rectangle([0, 0, PW, DRAW_H], fill=(5, 5, 8))

    # Phone bezel (thin, visible at edges)
    bezel_margin = 20
    draw.rectangle([0, 0, PW, DRAW_H], fill=PHONE_DARK)
    draw.rectangle([0, 0, PW, 5], fill=PHONE_SILVER)   # top bar
    draw.rectangle([0, DRAW_H - 5, PW, DRAW_H], fill=PHONE_SILVER)  # bottom bar

    # Screen area (nearly full frame)
    sc_x = bezel_margin
    sc_y = bezel_margin
    sc_w = PW - bezel_margin * 2
    sc_h = DRAW_H - bezel_margin * 2

    # ── STATIC / GLITCH fills screen ──────────────────────────────────────
    # Base: dark crashed app color (not full black — it's a crash, not off)
    draw.rectangle([sc_x, sc_y, sc_x + sc_w, sc_y + sc_h], fill=(15, 12, 20))

    # Horizontal scan line corruption (punch cut visual)
    # Mix of static white flickers and horizontal glitch bars
    for _ in range(35):
        bar_y = rng.randint(sc_y, sc_y + sc_h - 4)
        bar_h_s = rng.randint(1, 8)
        bar_alpha = rng.randint(60, 200)
        bar_color = rng.choice([
            STATIC_WHITE, GLITCH_CYAN, GLITCH_MAG, GLITCH_ACID,
            (255, 255, 255), (200, 200, 200), (50, 50, 60)
        ])
        # Horizontal bar — full width
        bar_x_start = sc_x + rng.randint(0, sc_w // 3)
        bar_x_end = sc_x + sc_w - rng.randint(0, sc_w // 4)
        static_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(static_layer)
        sd.rectangle([bar_x_start, bar_y, bar_x_end, bar_y + bar_h_s],
                     fill=(*bar_color, bar_alpha))
        img_rgba = img.convert('RGBA')
        img_rgba = Image.alpha_composite(img_rgba, static_layer)
        img.paste(img_rgba.convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Vertical displacement artifacts (screen tearing)
    for _ in range(12):
        tv_x = rng.randint(sc_x, sc_x + sc_w - 40)
        tv_y = rng.randint(sc_y, sc_y + sc_h)
        tv_w_s = rng.randint(20, 80)
        tv_h_s = rng.randint(2, 12)
        tv_shift = rng.randint(-15, 15)
        # Torn / displaced block — random pixel noise block
        for row in range(tv_h_s):
            for col in range(tv_w_s):
                px = tv_x + col
                py = tv_y + row + tv_shift
                if sc_x <= px <= sc_x + sc_w and sc_y <= py <= sc_y + sc_h:
                    c = rng.choice([(0, 240, 255), (255, 0, 200), (255, 255, 255),
                                    (30, 30, 40), (180, 255, 40)])
                    draw.point((px, py), fill=c)

    # ── Crashed app remnants (ghosted UI under static) ────────────────────
    # Faint waveform ghost — the app that was running
    ghost_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(ghost_layer)
    ghost_wf = []
    gf_rng = random.Random(42)  # same seed = same waveform, now corrupted
    for i in range(12):
        wx = sc_x + 3 + i * (sc_w - 6) // 11
        wy = sc_y + 55 - gf_rng.randint(4, 22) + rng.randint(-8, 8)  # corrupted shift
        ghost_wf.append((wx, wy))
    if len(ghost_wf) > 1:
        gd.line(ghost_wf, fill=(0, 200, 230, 50), width=2)
    img_rgba = img.convert('RGBA')
    img_rgba = Image.alpha_composite(img_rgba, ghost_layer)
    img.paste(img_rgba.convert('RGB'))
    draw = ImageDraw.Draw(img)

    # ── ERROR TEXT (crashed app) ───────────────────────────────────────────
    # Center of screen: error state
    err_cx = PW // 2
    err_cy = DRAW_H // 2

    # Error symbol — big X made of glitch elements
    x_size = 30
    draw.line([err_cx - x_size, err_cy - x_size, err_cx + x_size, err_cy + x_size],
              fill=GLITCH_MAG, width=5)
    draw.line([err_cx + x_size, err_cy - x_size, err_cx - x_size, err_cy + x_size],
              fill=GLITCH_MAG, width=5)

    # Error text
    draw.text((err_cx - 60, err_cy + x_size + 8), "APP TERMINATED", font=font_cap,
              fill=STATIC_WHITE)
    draw.text((err_cx - 55, err_cy + x_size + 22), "SIGNAL LOST: ERR 0xFF", font=font_ann,
              fill=GLITCH_CYAN)
    draw.text((err_cx - 40, err_cy + x_size + 33), ">>> GLITCH LAYER REJECTED", font=font_ann,
              fill=GLITCH_MAG)

    # ── Pixel confetti erupting from crash (app death = Glitch Layer response) ─
    pixel_confetti(draw, err_cx, err_cy, 100, 70, rng, n=20,
                   colors=[GLITCH_CYAN, GLITCH_MAG, GLITCH_ACID, STATIC_WHITE])

    # ── Screen crack FX at impact point (upper-left corner — feels like a punch) ─
    crack_cx = sc_x + sc_w // 4
    crack_cy = sc_y + sc_h // 4
    # Radiating crack lines
    for angle_deg in [0, 45, 90, 135, 180, 225, 270, 315]:
        angle_rad = math.radians(angle_deg)
        length_c = rng.randint(18, 40)
        ex_c = int(crack_cx + math.cos(angle_rad) * length_c)
        ey_c = int(crack_cy + math.sin(angle_rad) * length_c)
        draw.line([crack_cx, crack_cy, ex_c, ey_c], fill=STATIC_WHITE, width=1)
    # Center dot
    draw.ellipse([crack_cx - 3, crack_cy - 3, crack_cx + 3, crack_cy + 3],
                 fill=STATIC_WHITE)

    # Vignette border (adds to "screen edge" feel)
    for edge_w in range(8, 0, -2):
        alpha = int(130 * (1 - edge_w / 8))
        v_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        vd = ImageDraw.Draw(v_layer)
        vd.rectangle([sc_x + edge_w, sc_y + edge_w,
                      sc_x + sc_w - edge_w, sc_y + sc_h - edge_w],
                     outline=(0, 0, 0, alpha), width=2)
        img_rgba = img.convert('RGBA')
        img_rgba = Image.alpha_composite(img_rgba, v_layer)
        img.paste(img_rgba.convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Panel label
    draw.text((sc_x + 4, sc_y + 4), "INSERT: phone screen", font=font_ann,
              fill=(100, 100, 120))
    draw.text((sc_x + 4, sc_y + 14), "Cosmo NOT visible", font=font_ann,
              fill=(80, 80, 100))


# ═══════════════════════════════════════════════════════════════════════════════
#  CONTACT SHEET
# ═══════════════════════════════════════════════════════════════════════════════

def make_contact_sheet(panel_imgs, output_path):
    """
    2x2 contact sheet for 4 Act 2 panels (480x270 each).
    Sheet: 2 cols x 2 rows + header bar.
    """
    cols, rows = 2, 2
    thumb_w, thumb_h = 480, 270
    margin = 12
    header_h = 52
    label_h = 28

    sheet_w = cols * thumb_w + (cols + 1) * margin
    sheet_h = header_h + rows * (thumb_h + label_h) + (rows + 1) * margin

    sheet = Image.new('RGB', (sheet_w, sheet_h), (18, 14, 12))
    sd = ImageDraw.Draw(sheet)

    try:
        hfont = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        lfont = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        hfont = lfont = ImageFont.load_default()

    # Header bar
    sd.rectangle([0, 0, sheet_w, header_h], fill=(28, 22, 18))
    sd.text((margin, 10), "Luma & the Glitchkin — Act 2 Panels", font=hfont,
            fill=(235, 228, 210))
    sd.text((margin, 32), "Cycle 14  |  Lee Tanaka, Storyboard Artist  |  4 panels",
            font=lfont, fill=(160, 150, 130))
    sd.line([0, header_h, sheet_w, header_h], fill=(60, 50, 40), width=2)

    labels = [
        "A1-04 — Near-miss: Binary Lesson",
        "A2-02 — Byte MCU: Cracked-Eye Vulnerability",
        "A2-05b — Cosmo: Glitch Freq App",
        "A2-06 — INSERT: App Crash / Static",
    ]

    for idx, (panel_img, label) in enumerate(zip(panel_imgs, labels)):
        col = idx % cols
        row = idx // cols
        x = margin + col * (thumb_w + margin)
        y = header_h + margin + row * (thumb_h + label_h + margin)

        # Paste panel thumbnail
        sheet.paste(panel_img.resize((thumb_w, thumb_h), Image.LANCZOS), (x, y))

        # White border
        sd.rectangle([x - 1, y - 1, x + thumb_w + 1, y + thumb_h + 1],
                     outline=(80, 70, 60), width=1)

        # Label below
        sd.rectangle([x, y + thumb_h, x + thumb_w, y + thumb_h + label_h],
                     fill=(28, 22, 18))
        sd.text((x + 6, y + thumb_h + 6), f"{idx + 1}. {label}", font=lfont,
                fill=(200, 190, 170))

    sheet.save(output_path)
    print(f"  Saved contact sheet: {os.path.basename(output_path)}")
    return sheet


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Cycle 14 — Act 2 Panel Generation")
    print("=" * 50)

    panels = []

    # A1-04 — Near-miss micro-beat
    print("\n[1/4] A1-04 — Near-miss (classroom binary lesson)...")
    p1 = make_panel(
        filepath=os.path.join(PANELS_DIR, "LTG_SB_act2_panel_a104.png"),
        shot_label="A1-04  |  WIDE — Classroom  |  Pressure / near-miss",
        caption_text="Luma's gaze drifts to board — BINARY SYSTEMS — almost connects. "
                     "Byte naps in eraser bits. Near-miss before the payoff.",
        draw_fn=draw_a104,
        bg_color=(170, 160, 195),
    )
    panels.append(p1)

    # A2-02 — Byte MCU vulnerability
    print("\n[2/4] A2-02 — Byte MCU vulnerability (cracked-eye glyph)...")
    p2 = make_panel(
        filepath=os.path.join(PANELS_DIR, "LTG_SB_act2_panel_a202.png"),
        shot_label="A2-02  |  MCU — Byte face  |  Strained negotiation / vulnerability",
        caption_text="Byte MCU: cracked eye at frame center — dead-pixel glyph fully rendered. "
                     "Resigned expression. Luma ~20% bg. Emotional anchor beat.",
        draw_fn=draw_a202,
        bg_color=(55, 38, 24),
    )
    panels.append(p2)

    # A2-05b — Cosmo app setup
    print("\n[3/4] A2-05b — Cosmo Glitch Frequency app...")
    p3 = make_panel(
        filepath=os.path.join(PANELS_DIR, "LTG_SB_act2_panel_a205b.png"),
        shot_label="A2-05b  |  MCU — Cosmo street  |  Determined / pre-failure",
        caption_text="Cosmo on street, phone out, Glitch Freq app scanning. "
                     "Confident. Streetlight glitches behind him. Setup for A2-06 crash.",
        draw_fn=draw_a205b,
        bg_color=(210, 195, 175),
    )
    panels.append(p3)

    # A2-06 — App failure INSERT
    print("\n[4/4] A2-06 — App failure INSERT (phone screen crash)...")
    p4 = make_panel(
        filepath=os.path.join(PANELS_DIR, "LTG_SB_act2_panel_a206.png"),
        shot_label="A2-06  |  INSERT — Phone screen  |  Failure punch cut",
        caption_text="Phone screen INSERT: app crashes, static/glitch fills frame. "
                     "No Cosmo — pure screen. Punch cut. Glitch Layer rejected the signal.",
        draw_fn=draw_a206,
        bg_color=(5, 5, 8),
    )
    panels.append(p4)

    # Contact sheet
    print("\n[5/5] Act 2 contact sheet...")
    make_contact_sheet(
        panel_imgs=panels,
        output_path=os.path.join(SHEETS_DIR, "LTG_SB_act2_contactsheet.png"),
    )

    print("\n" + "=" * 50)
    print("Cycle 14 complete. All Act 2 panels generated.")
    print(f"  Panels dir: {PANELS_DIR}")
    print(f"  Sheet dir:  {SHEETS_DIR}")
    print("\nFiles written:")
    for name in [
        "LTG_SB_act2_panel_a104.png",
        "LTG_SB_act2_panel_a202.png",
        "LTG_SB_act2_panel_a205b.png",
        "LTG_SB_act2_panel_a206.png",
    ]:
        print(f"  {PANELS_DIR}/{name}")
    print(f"  {SHEETS_DIR}/LTG_SB_act2_contactsheet.png")
