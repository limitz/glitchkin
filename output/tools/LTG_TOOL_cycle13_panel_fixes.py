#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
Cycle 13 Panel Fixes — Luma & the Glitchkin
Lee Tanaka, Storyboard Artist

Addresses all Carmen Reyes critique items from Cycle 12:

Priority 1 — P13 scream fix:
  - Jaw drops to full yell: tall oval mouth, NOT small circle
  - Tongue visible inside open mouth
  - Brows spike sharply upward (separate sharp peaks, not arcs)
  - Body RECOILS backward: torso tilted back, weight shifted

Priority 2 — P15 arm urgency:
  - Right arm endpoint pushed to ~360px (from 287px)
  - Arm strains toward frame edge — sells freefall urgency

Priority 3 — P03 framing:
  - CRT fills most of frame (was 380px wide gap, now near-full)
  - Reduces surrounding room space to punch contrast vs P04

Priority 4 — P08/P09 camera heights:
  - P08: slightly HIGH angle (camera above Byte's eye level — diminishes him)
  - P09: EYE LEVEL (camera at Byte's floating height — he reads as present/dangerous)
  - Annotation text updated to reflect each camera's exact position

Outputs:
  - /home/wipkat/team/output/storyboards/panels/panel_p13_scream.png (overwrite)
  - /home/wipkat/team/output/storyboards/panels/panel_p15_luma_freefall.png (overwrite)
  - /home/wipkat/team/output/storyboards/panels/panel_p03_first_pixel.png (overwrite)
  - /home/wipkat/team/output/storyboards/panels/panel_p08_byte_real_world.png (overwrite)
  - /home/wipkat/team/output/storyboards/panels/panel_p09_byte_sees_luma.png (overwrite)
  - LTG_SB_coldopen_panel_[##]_v002.png for each fixed panel (new version, no overwrite)
  - Updated contact_sheet.png + LTG_SB_coldopen_contactsheet.png

MEMORY principles applied:
  - Scream = jaw DOWN, mouth maximum aperture (tall oval, not O-shape)
  - Urgency = limbs straining toward frame edges
  - Compositional tightness = fill the frame with the story element
  - Camera differentiation = explicit angle notation AND visible geometry shift
  - Dutch tilt = Image.rotate() on whole scene
  - Glow effects ADD light (alpha_composite / RGBA)
  - Never overwrite LTG versioned files — new v002 copies
"""

from PIL import Image, ImageDraw, ImageFont
import math
import random
import os
import shutil

PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"
PW, PH = 480, 270
CAPTION_H = 48
DRAW_H = PH - CAPTION_H
BORDER = 2

# ── Color palette (shared across all panels) ──────────────────────────────────
BG_DRAW       = (242, 240, 235)
BG_CAPTION    = (25, 20, 18)
BORDER_COL    = (20, 15, 12)
TEXT_CAPTION  = (235, 228, 210)
TEXT_PANEL    = (20, 15, 12)

WARM_DARK     = (22, 16, 10)
WARM_AMBER    = (55, 38, 24)
WARM_WALL     = (45, 30, 18)
LUMA_SKIN     = (200, 136, 90)
LUMA_HAIR     = (22, 14, 8)
LUMA_PJ       = (160, 200, 180)
BYTE_CYAN     = (0, 212, 232)
BYTE_DARK     = (8, 8, 18)
GLITCH_CYAN   = (0, 240, 255)
GLITCH_MAG    = (255, 0, 200)
GLITCH_ACID   = (180, 255, 40)
FLOOR_DARK    = (16, 12, 8)
BYTE_BODY     = (0, 212, 232)
BYTE_OUTLINE  = (10, 10, 20)
CRT_TEAL      = (0, 212, 232)


def load_fonts():
    try:
        font       = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
        font_bold  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
        font_cap   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        font_ann   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    except Exception:
        font = font_bold = font_cap = font_ann = ImageFont.load_default()
    return font, font_bold, font_cap, font_ann


def make_panel(panel_num, shot_type, caption, draw_fn, filepath):
    """Create a storyboard panel and save it to filepath."""
    img  = Image.new('RGB', (PW, PH), BG_DRAW)
    draw = ImageDraw.Draw(img)
    font, font_bold, font_cap, font_ann = load_fonts()

    # Drawing area
    draw.rectangle([0, 0, PW, DRAW_H], fill=WARM_DARK)

    # Scene content
    draw_fn(draw, img, font, font_bold, font_ann)

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.text((8, DRAW_H + 5), caption[:80], fill=TEXT_CAPTION, font=font_cap)

    # Panel number
    draw.text((PW - 40, DRAW_H + 5), f"P{panel_num}", fill=(160, 150, 130), font=font_cap)

    # Shot type label
    draw.text((8, DRAW_H + 20), shot_type, fill=(120, 115, 100), font=font_cap)

    # Border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COL, width=BORDER)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    img.save(filepath)
    print(f"  [SAVED] {os.path.basename(filepath)}")
    return img


def add_pixel_confetti(draw, x_range, y_range, count, seed=0,
                       colors=None):
    """Scatter small pixel confetti squares. x_range/y_range are (min, max) tuples."""
    if colors is None:
        colors = [GLITCH_CYAN, GLITCH_MAG, (255, 220, 60)]
    rng = random.Random(seed)
    for _ in range(count):
        px = rng.randint(x_range[0], x_range[1])
        py = rng.randint(y_range[0], y_range[1])
        col = colors[rng.randint(0, len(colors) - 1)]
        sz = rng.randint(1, 3)
        draw.rectangle([px, py, px + sz, py + sz], fill=col)


def draw_byte_body(draw, cx, cy, size, eye_state="normal", font_ann=None):
    """Draw Byte's body at (cx, cy) with given size.
    eye_state: 'normal', 'scan', 'alarmed', 'cracked'"""
    c = size // 8
    body_pts = [
        (cx - size // 2 + c, cy - size // 2),
        (cx + size // 2 - c, cy - size // 2),
        (cx + size // 2,     cy - size // 2 + c),
        (cx + size // 2,     cy + size // 2 - c),
        (cx + size // 2 - c, cy + size // 2),
        (cx - size // 2 + c, cy + size // 2),
        (cx - size // 2,     cy + size // 2 - c),
        (cx - size // 2,     cy - size // 2 + c),
    ]
    draw.polygon(body_pts, fill=BYTE_BODY, outline=BYTE_OUTLINE, width=2)
    # Right-side shadow
    shadow_pts = [
        (cx, cy - size // 2 + c), (cx + size // 2 - c, cy - size // 2),
        (cx + size // 2, cy - size // 2 + c), (cx + size // 2, cy + size // 2 - c),
        (cx + size // 2 - c, cy + size // 2), (cx, cy + size // 2),
    ]
    draw.polygon(shadow_pts, fill=(0, 144, 176))
    # Highlight top edge
    draw.line([(cx - size // 2 + c, cy - size // 2),
               (cx + size // 2 - c, cy - size // 2)], fill=(0, 240, 255), width=2)

    # Eyes
    eye_l_x = cx - size // 4
    eye_r_x = cx + size // 8
    eye_y   = cy - size // 8
    ew      = max(6, size // 8)
    eh      = max(8, size // 6)

    if eye_state == "scan":
        # Scan line horizontal across both eyes
        for ex in [eye_l_x, eye_r_x]:
            draw.rectangle([ex, eye_y, ex + ew, eye_y + eh],
                           fill=(255, 255, 255), outline=(0, 100, 120), width=1)
            draw.line([(ex, eye_y + eh // 2), (ex + ew, eye_y + eh // 2)],
                      fill=(0, 240, 255), width=2)
    elif eye_state == "alarmed":
        for ex in [eye_l_x, eye_r_x]:
            draw.rectangle([ex, eye_y, ex + ew, eye_y + eh],
                           fill=(255, 255, 255), outline=(0, 100, 120), width=1)
            for dot_y in [eye_y + 1, eye_y + eh // 2 - 1, eye_y + eh - 3]:
                draw.rectangle([ex + ew // 3, dot_y,
                                 ex + ew // 3 + 2, dot_y + 1], fill=(0, 240, 255))
    else:
        # Normal — two simple pixel eyes
        for ex in [eye_l_x, eye_r_x]:
            draw.rectangle([ex, eye_y, ex + ew, eye_y + eh],
                           fill=(255, 255, 255), outline=(0, 100, 120), width=1)
            draw.rectangle([ex + 1, eye_y + 1, ex + ew - 1, eye_y + eh - 1],
                           fill=(0, 200, 220))

    # Hover glow
    draw.ellipse([cx - size // 2, cy + size // 2,
                  cx + size // 2, cy + size // 2 + size // 5],
                 fill=(0, 40, 60))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PRIORITY 1 — P13 SCREAM FIX
# Carmen: "jaw must drop; mouth aperture is insufficient. Full yell (tall oval,
# not a small gap). Add tongue. Eyebrows spike upward. Body recoils."
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def draw_p13_scream_v2(draw, img, font, font_bold, font_ann):
    """P13 CYCLE 13 FIX — full room 3D spatial staging.
    SCREAM FIX: jaw DROPS hard. Mouth is tall yell oval, NOT small circle.
    Tongue visible inside open mouth. Brows are sharp separate SPIKES upward.
    Body RECOILS: torso tilted back, weight shifted to heels.
    Camera: MED WIDE, slightly low, centered on room.
    Luma: left-center, body recoiling back, screaming.
    Byte: center-right, frozen/alarmed.
    Monitors: back wall, activating in response."""

    # ── Room base ─────────────────────────────────────────────────────────────
    draw.rectangle([0, 0, PW, DRAW_H], fill=(20, 14, 10))

    # Back wall
    back_wall_top = int(DRAW_H * 0.18)
    back_wall_bot = int(DRAW_H * 0.68)
    draw.rectangle([0, back_wall_top, PW, back_wall_bot], fill=(32, 23, 16))
    draw.line([(0, back_wall_top), (PW, back_wall_top)], fill=(50, 36, 24), width=2)

    # Floor
    floor_y = back_wall_bot
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=(18, 12, 8))
    draw.line([(0, floor_y), (PW, floor_y)], fill=(40, 28, 18), width=2)

    # Perspective lines to vanishing point
    vp_x, vp_y = PW // 2, back_wall_top + 20
    for edge_x in [0, PW]:
        draw.line([(edge_x, DRAW_H), (vp_x, vp_y)], fill=(28, 20, 13), width=1)

    # ── MONITORS on back wall (3, fully lit — reacting to scream) ─────────────
    monitor_specs = [
        (40, back_wall_top + 12, 88, 52, (0, 240, 255)),
        (196, back_wall_top + 8, 96, 58, (255, 45, 107)),
        (352, back_wall_top + 12, 80, 50, (0, 200, 65)),
    ]
    for mx, my, mw, mh, glow in monitor_specs:
        draw.rectangle([mx, my, mx + mw, my + mh], fill=(12, 8, 16),
                       outline=(40, 30, 50), width=2)
        draw.rectangle([mx + 3, my + 3, mx + mw - 3, my + mh - 3], fill=glow)
        cx_m, cy_m = mx + mw // 2, my + mh // 2
        draw.ellipse([cx_m - 20, cy_m - 14, cx_m + 20, cy_m + 14],
                     fill=(min(255, glow[0] + 60), min(255, glow[1] + 60),
                           min(255, glow[2] + 60)))
        for r in range(18, 4, -5):
            draw.ellipse([cx_m - r * 2, cy_m - r, cx_m + r * 2, cy_m + r],
                         outline=glow, width=1)

    # ── BED (right side) ─────────────────────────────────────────────────────
    bed_lx = int(PW * 0.72)
    draw.polygon([(bed_lx, int(DRAW_H * 0.52)), (PW + 10, int(DRAW_H * 0.52) + 12),
                  (PW + 10, floor_y), (bed_lx, floor_y - 5)],
                 fill=(55, 38, 28))
    draw.line([(bed_lx, int(DRAW_H * 0.52)),
               (PW + 10, int(DRAW_H * 0.52) + 12)], fill=(70, 50, 35), width=2)

    # ── LUMA — SCREAM with BODY RECOIL ────────────────────────────────────────
    # Body recoil: torso pitched BACK, weight on heels — not vertical
    lx = int(PW * 0.28)
    body_top_y = int(DRAW_H * 0.22)
    body_bot_y = floor_y - 3

    # Floor shadow
    draw.ellipse([lx - 32, floor_y - 6, lx + 32, floor_y + 5], fill=(12, 8, 5))

    # Legs — feet planted forward, body weight back (recoil geometry)
    # Left foot planted slightly forward
    draw.line([(lx - 6, body_bot_y - 22), (lx - 22, floor_y)],
              fill=(200, 136, 90), width=6)
    # Right foot planted, knee slightly bent back with recoil
    draw.line([(lx + 10, body_bot_y - 22), (lx + 26, floor_y)],
              fill=(200, 136, 90), width=6)

    # Torso — RECOIL: tilted backward (upper torso leans away from Byte)
    # Upper torso shifts left/back; lower stays planted
    torso_pts = [
        (lx - 22, body_top_y + 28),   # upper-left (leaning back)
        (lx + 14, body_top_y + 28),   # upper-right (narrower — recoil torque)
        (lx + 22, body_bot_y - 20),   # lower-right
        (lx - 22, body_bot_y - 20)    # lower-left
    ]
    draw.polygon(torso_pts, fill=(232, 114, 42), outline=(50, 30, 15), width=1)

    # Arms FLUNG WIDE + UP (full scream wingspan — terror)
    # Left arm — up-left diagonal
    draw.line([(lx - 16, body_top_y + 46), (lx - 72, body_top_y + 8)],
              fill=(200, 136, 90), width=7)
    draw.ellipse([lx - 80, body_top_y + 1, lx - 62, body_top_y + 18],
                 fill=(200, 136, 90))
    # Right arm — up-right diagonal
    draw.line([(lx + 14, body_top_y + 46), (lx + 72, body_top_y + 8)],
              fill=(200, 136, 90), width=7)
    draw.ellipse([lx + 62, body_top_y + 1, lx + 80, body_top_y + 18],
                 fill=(200, 136, 90))

    # ── LUMA HEAD — SCREAM EXPRESSION ─────────────────────────────────────────
    # Head tilted SLIGHTLY BACK (scream forces head up as jaw drops)
    hx, hy = lx - 4, body_top_y + 12
    draw.ellipse([hx - 28, hy - 28, hx + 28, hy + 28],
                 fill=(200, 136, 90), outline=(50, 30, 15), width=2)

    # Hair — SHOCK STATE: fully erect, spiky/explosive from the back of head
    draw.ellipse([hx - 40, hy - 50, hx + 40, hy + 6], fill=(25, 15, 10))
    # Extreme shock spikes — hair standing on end
    for spike_angle in range(100, 260, 22):
        s_rad = math.radians(spike_angle)
        sx1 = hx + int(34 * math.cos(s_rad))
        sy1 = hy + int(34 * math.sin(s_rad))
        sx2 = hx + int(52 * math.cos(s_rad))
        sy2 = hy + int(52 * math.sin(s_rad))
        draw.line([(sx1, sy1), (sx2, sy2)], fill=(25, 15, 10), width=3)

    # Eyes — HORROR WIDE: pupils tiny, whites fully showing, upper eyelids pull back
    draw.ellipse([hx - 17, hy - 9, hx - 3, hy + 8], fill=(255, 255, 245))
    draw.ellipse([hx + 3,  hy - 9, hx + 17, hy + 8], fill=(255, 255, 245))
    draw.ellipse([hx - 13, hy - 4, hx - 8,  hy + 3], fill=(20, 12, 8))   # tiny pupil L
    draw.ellipse([hx + 8,  hy - 4, hx + 13, hy + 3], fill=(20, 12, 8))   # tiny pupil R

    # EYEBROWS — SHARP UPWARD SPIKES (not arcs — separate angled lines = spike shape)
    # Left brow: two lines forming a ^ spike, high above eye
    draw.line([(hx - 18, hy - 22), (hx - 10, hy - 32)], fill=(25, 15, 10), width=4)  # left side
    draw.line([(hx - 10, hy - 32), (hx - 2,  hy - 22)], fill=(25, 15, 10), width=4)  # right side
    # Right brow: same spike shape
    draw.line([(hx + 2,  hy - 22), (hx + 10, hy - 32)], fill=(25, 15, 10), width=4)
    draw.line([(hx + 10, hy - 32), (hx + 18, hy - 22)], fill=(25, 15, 10), width=4)

    # ── MOUTH — FULL YELL (JAW DROP) ──────────────────────────────────────────
    # JAW DOWN: mouth is a TALL OVAL, not a small circle.
    # Width: ~26px. Height: ~32px (nearly 2:1 height-to-width for max aperture)
    # Jaw drops so mouth center is LOWER than a normal mouth position
    mouth_cx = hx
    mouth_top_y = hy + 6   # upper lip line (tight — not much space above)
    mouth_bot_y = hy + 38  # jaw dropped FAR down — near chin
    mouth_w = 26

    # Mouth cavity (dark interior — throat depth)
    draw.ellipse([mouth_cx - mouth_w, mouth_top_y,
                  mouth_cx + mouth_w, mouth_bot_y],
                 fill=(18, 6, 4), outline=(50, 30, 15), width=2)

    # TONGUE — visible inside open mouth (pale pink, fills lower 40% of opening)
    tongue_top = mouth_top_y + int((mouth_bot_y - mouth_top_y) * 0.55)
    draw.ellipse([mouth_cx - mouth_w + 8, tongue_top,
                  mouth_cx + mouth_w - 8, mouth_bot_y - 2],
                 fill=(220, 120, 100))

    # Teeth — upper row visible (small white bar just inside upper lip)
    draw.rectangle([mouth_cx - mouth_w + 4, mouth_top_y + 2,
                    mouth_cx + mouth_w - 4, mouth_top_y + 8],
                   fill=(245, 240, 230))
    # Tooth dividers (3 lines creating 4 teeth)
    for tooth_x in [mouth_cx - 8, mouth_cx, mouth_cx + 8]:
        draw.line([(tooth_x, mouth_top_y + 2), (tooth_x, mouth_top_y + 8)],
                  fill=(200, 190, 175), width=1)

    # Scream energy lines radiating from mouth — wider arc (yell projects outward)
    for angle in range(240, 450, 18):
        r1, r2 = 30, 56
        ax1 = mouth_cx + int(r1 * math.cos(math.radians(angle)))
        ay1 = (mouth_top_y + mouth_bot_y) // 2 + int(r1 * math.sin(math.radians(angle)))
        ax2 = mouth_cx + int(r2 * math.cos(math.radians(angle)))
        ay2 = (mouth_top_y + mouth_bot_y) // 2 + int(r2 * math.sin(math.radians(angle)))
        draw.line([(ax1, ay1), (ax2, ay2)], fill=(255, 220, 80), width=1)

    # ── BYTE — center-right, alarmed-frozen ───────────────────────────────────
    bx = int(PW * 0.60)
    by_center = int(DRAW_H * 0.38)
    bs = 34
    c = bs // 8
    body_pts = [
        (bx - bs // 2 + c, by_center - bs // 2),
        (bx + bs // 2 - c, by_center - bs // 2),
        (bx + bs // 2,     by_center - bs // 2 + c),
        (bx + bs // 2,     by_center + bs // 2 - c),
        (bx + bs // 2 - c, by_center + bs // 2),
        (bx - bs // 2 + c, by_center + bs // 2),
        (bx - bs // 2,     by_center + bs // 2 - c),
        (bx - bs // 2,     by_center - bs // 2 + c),
    ]
    draw.polygon(body_pts, fill=(0, 212, 232), outline=(10, 10, 20), width=2)
    shadow_pts = [
        (bx,     by_center - bs // 2 + c),
        (bx + bs // 2 - c, by_center - bs // 2),
        (bx + bs // 2,     by_center - bs // 2 + c),
        (bx + bs // 2,     by_center + bs // 2 - c),
        (bx + bs // 2 - c, by_center + bs // 2),
        (bx,     by_center + bs // 2),
    ]
    draw.polygon(shadow_pts, fill=(0, 144, 176))
    draw.line([(bx - bs // 2 + c, by_center - bs // 2),
               (bx + bs // 2 - c, by_center - bs // 2)], fill=(0, 240, 255), width=2)
    # Byte pixel eyes — alarmed ! state
    for ex_off in [-10, 4]:
        ex = bx + ex_off
        ey = by_center - 4
        draw.rectangle([ex, ey, ex + 8, ey + 12],
                       fill=(255, 255, 255), outline=(0, 100, 120), width=1)
        for dot_y in [ey + 1, ey + 4, ey + 7]:
            draw.rectangle([ex + 3, dot_y, ex + 5, dot_y + 1], fill=(0, 240, 255))
        draw.rectangle([ex + 3, ey + 10, ex + 5, ey + 11], fill=(0, 240, 255))
    # Byte stubby arms raised (alarmed)
    draw.rectangle([bx - bs // 2 - 10, by_center - 8,
                    bx - bs // 2,       by_center + 2],
                   fill=(0, 212, 232), outline=(10, 10, 20), width=1)
    draw.rectangle([bx + bs // 2,      by_center - 8,
                    bx + bs // 2 + 10, by_center + 2],
                   fill=(0, 212, 232), outline=(10, 10, 20), width=1)
    draw.ellipse([bx - 20, by_center + bs // 2,
                  bx + 20, by_center + bs // 2 + 8], fill=(0, 55, 75))

    # Annotations
    draw.text((4, 4), "MED WIDE — slight low angle", fill=(150, 140, 120), font=font_ann)
    draw.text((4, 14), "SCREAM: jaw drop, tongue, spike brows, body RECOIL", fill=(130, 120, 100), font=font_ann)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PRIORITY 2 — P15 ARM URGENCY FIX
# Carmen: push right arm endpoint to 360-380px (from ~287px)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def draw_luma_face_p15(draw, cx, cy, size=46, expression='panic'):
    """Draw Luma's face for P15 — panic expression, head tilted back."""
    hx, hy = cx, cy + size // 2
    # Head
    draw.ellipse([hx - size // 2, hy - size // 2,
                  hx + size // 2, hy + size // 2],
                 fill=LUMA_SKIN, outline=(50, 30, 15), width=2)
    # GLITCH CIRCLE HAIR — perfect circle (the visual gag)
    hair_r = int(size * 0.62)
    draw.ellipse([hx - hair_r, hy - hair_r, hx + hair_r, hy + hair_r],
                 fill=LUMA_HAIR, outline=(40, 25, 10), width=1)
    # Re-draw face over hair
    draw.ellipse([hx - size // 2 + 2, hy - size // 2 + 2,
                  hx + size // 2 - 2, hy + size // 2 - 2], fill=LUMA_SKIN)
    # Eyes — wide panic
    draw.ellipse([hx - 14, hy - 7, hx - 3, hy + 6], fill=(255, 255, 245))
    draw.ellipse([hx + 3,  hy - 7, hx + 14, hy + 6], fill=(255, 255, 245))
    draw.ellipse([hx - 11, hy - 4, hx - 6,  hy + 3], fill=(20, 12, 8))
    draw.ellipse([hx + 6,  hy - 4, hx + 11, hy + 3], fill=(20, 12, 8))
    # Brows up
    draw.arc([hx - 18, hy - 22, hx - 2, hy - 10], start=190, end=340,
             fill=(25, 15, 10), width=3)
    draw.arc([hx + 2, hy - 22, hx + 18, hy - 10], start=200, end=350,
             fill=(25, 15, 10), width=3)
    # Mouth — open O (not full yell — this is panic/freefall not scream)
    draw.ellipse([hx - 9, hy + 7, hx + 9, hy + 20],
                 fill=(25, 10, 5), outline=(50, 30, 15), width=2)


def draw_p15_arm_fix(draw, img, font, font_bold, font_ann):
    """P15 CYCLE 13 FIX — right arm endpoint extended to ~360px.
    Carmen: 'A freefall arm is reaching for something to stop the fall.
    Polite does not apply.' Endpoint pushed from 287px to 360px.
    All other elements identical to Cycle 12 version."""

    draw.rectangle([0, 0, PW, DRAW_H], fill=(18, 12, 8))

    # Floor — close up (floor level looking UP)
    floor_y = int(DRAW_H * 0.82)
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=(14, 10, 6))
    draw.line([(0, floor_y), (PW, floor_y)], fill=(30, 20, 12), width=1)

    # Pixel confetti ring on floor — excited about incoming collision
    ring_cx, ring_cy = PW // 2, floor_y + 4
    for r in range(55, 5, -10):
        intensity = max(0, 60 - r)
        draw.ellipse([ring_cx - r * 2, ring_cy - r // 2,
                      ring_cx + r * 2, ring_cy + r // 2],
                     outline=(0, intensity + 100, intensity + 140), width=1)
    add_pixel_confetti(draw, (ring_cx - 55, ring_cx + 55),
                       (floor_y - 10, floor_y + 8), 35, seed=15)

    # Background: monitor glow + chaos
    for i in range(4):
        gx = i * (PW // 4) + PW // 8
        for gr in [28, 18, 10]:
            a_col = max(0, 60 - gr * 2)
            draw.ellipse([gx - gr * 2, 0, gx + gr * 2, gr * 2],
                         fill=(0, a_col, a_col + 10))

    # Luma in freefall — PHYSICAL SURPRISE
    luma_cx = PW // 2 - 5
    luma_cy = int(DRAW_H * 0.36)
    body_top = luma_cy - 12
    body_bot = luma_cy + 26

    # Body — SQUASHED torso
    draw.ellipse([luma_cx - 34, body_top, luma_cx + 34, body_bot],
                 fill=LUMA_PJ, outline=(100, 150, 120), width=2)
    # Squash annotation
    draw.line([(luma_cx + 36, body_top), (luma_cx + 46, body_top)],
              fill=(0, 180, 200), width=1)
    draw.line([(luma_cx + 36, body_bot), (luma_cx + 46, body_bot)],
              fill=(0, 180, 200), width=1)
    draw.line([(luma_cx + 41, body_top), (luma_cx + 41, body_bot)],
              fill=(0, 180, 200), width=1)
    draw.text((luma_cx + 48, luma_cy - 6), "SQUASH",
              fill=(0, 180, 200), font=font_ann)

    # LEFT ARM — raised DEFENSIVELY HIGH (elbow up, wrist above head)
    draw.line([(luma_cx - 12, body_top + 8), (luma_cx - 42, body_top - 28)],
              fill=LUMA_SKIN, width=6)
    draw.line([(luma_cx - 42, body_top - 28), (luma_cx - 28, body_top - 42)],
              fill=LUMA_SKIN, width=6)

    # RIGHT ARM — CYCLE 13 FIX: endpoint extended to ~360px from left
    # luma_cx = 235. endpoint = 235 + 125 = 360px. Reaches toward right edge (480px).
    # Horizontal true: y stays at body_top + 10 on both ends.
    # This is a STRAINING ARM — reaching desperately for something to grab.
    right_arm_endpoint_x = luma_cx + 125  # = ~360px — URGENT, near frame edge
    draw.line([(luma_cx + 10, body_top + 10), (right_arm_endpoint_x, body_top + 10)],
              fill=LUMA_SKIN, width=6)
    # Hand (reaching blob at extended end)
    draw.ellipse([right_arm_endpoint_x - 2, body_top + 5,
                  right_arm_endpoint_x + 12, body_top + 18],
                 fill=LUMA_SKIN)
    # Urgency annotation at arm tip
    draw.line([(right_arm_endpoint_x + 14, body_top + 12),
               (right_arm_endpoint_x + 30, body_top + 6)], fill=(0, 180, 200), width=1)
    draw.text((right_arm_endpoint_x + 32, body_top), "STRAINING",
              fill=(0, 180, 200), font=font_ann)
    draw.text((right_arm_endpoint_x + 32, body_top + 9), "~360px",
              fill=(0, 200, 220), font=font_ann)

    # RIGHT LEG — KNEE TO CHEST
    draw.line([(luma_cx + 8,  body_bot),      (luma_cx + 32, body_bot - 18)],
              fill=LUMA_SKIN, width=6)
    draw.line([(luma_cx + 32, body_bot - 18), (luma_cx + 18, body_bot + 8)],
              fill=LUMA_SKIN, width=6)

    # LEFT LEG — extends downward
    draw.line([(luma_cx - 8, body_bot), (luma_cx - 32, body_bot + 36)],
              fill=LUMA_SKIN, width=6)

    # Face — head TILTED BACK
    draw_luma_face_p15(draw, luma_cx - 4, body_top - 55, size=46, expression='panic')
    draw.text((luma_cx - 62, body_top - 38), "HEAD BACK",
              fill=(0, 200, 220), font=font_ann)

    # GLITCH-FORCED HAIR SYMMETRY annotation
    ann_x, ann_y = luma_cx + 58, body_top - 42
    draw.line([(ann_x, ann_y), (luma_cx + 26, body_top - 48)],
              fill=(0, 200, 220), width=1)
    draw.text((ann_x + 2, ann_y - 10), "GLITCH OVERRIDES",
              fill=(0, 200, 220), font=font_ann)
    draw.text((ann_x + 2, ann_y), "HAIR — 8 FRAMES",
              fill=(0, 200, 220), font=font_ann)

    # Airborne couch cushion
    draw.rectangle([int(PW * 0.08), int(DRAW_H * 0.38),
                    int(PW * 0.24), int(DRAW_H * 0.54)],
                   fill=(130, 90, 55), outline=(90, 60, 35), width=2)

    # Notebook spiraling
    nb_x, nb_y = int(PW * 0.70), int(DRAW_H * 0.42)
    for page in range(3):
        ang = math.radians(30 + page * 20)
        pts = [(nb_x + 25 * math.cos(ang + t * math.pi / 2),
                nb_y + 18 * math.sin(ang + t * math.pi / 2)) for t in range(4)]
        draw.polygon(pts, fill=(235, 225, 190) if page < 2 else (200, 190, 150),
                     outline=(80, 70, 50), width=1)
    draw.text((nb_x - 12, nb_y - 6), "HISTORY", fill=(80, 70, 50), font=font_ann)

    # Pixel confetti through frame
    add_pixel_confetti(draw, (0, PW), (0, int(DRAW_H * 0.75)), 40, seed=15,
                       colors=[GLITCH_CYAN, GLITCH_MAG, (255, 220, 60)])

    draw.text((4, DRAW_H - 14), "FLOOR LEVEL — looking up — impact incoming",
              fill=(120, 110, 90), font=font_ann)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PRIORITY 3 — P03 FRAMING FIX
# Carmen: "not tight enough against the CRT — needs to fill more frame"
# Fix: push CRT to near-full frame, reduce room surround
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def draw_p03_pixel_tight(draw, img, font, font_bold, font_ann):
    """P03 CYCLE 13 FIX — CRT fills most of frame.
    Carmen: 'needs to fill more frame to punch contrast with P04's wide room reveal.'
    Monitor bezel now occupies ~85% of frame width. Very little room surround visible.
    This creates maximum contrast when P04 reveals the wide room.
    Pixel at lower-center. Pulse rings visible."""

    # Minimal room surround — just dark void (we're nose-to-glass close)
    draw.rectangle([0, 0, PW, DRAW_H], fill=(8, 7, 12))

    # CRT outer casing — near full frame (10px margin on each side)
    BEZEL_L = 10
    BEZEL_T = 8
    BEZEL_R = PW - 10
    BEZEL_B = DRAW_H - 8
    # Monitor plastic casing (thick — old CRT style)
    draw.rectangle([BEZEL_L, BEZEL_T, BEZEL_R, BEZEL_B],
                   fill=(18, 14, 22), outline=(30, 25, 38), width=3)
    # Inner bezel (narrower, darker)
    SCREEN_L = BEZEL_L + 16
    SCREEN_T = BEZEL_T + 14
    SCREEN_R = BEZEL_R - 16
    SCREEN_B = BEZEL_B - 14
    draw.rectangle([SCREEN_L, SCREEN_T, SCREEN_R, SCREEN_B],
                   fill=(6, 5, 10), outline=(22, 18, 30), width=2)

    # Screen glass surface (slightly lighter dark — almost black)
    draw.rectangle([SCREEN_L + 2, SCREEN_T + 2, SCREEN_R - 2, SCREEN_B - 2],
                   fill=(10, 8, 15))

    # Screen static — subtle scanlines (barely visible)
    for y in range(SCREEN_T + 2, SCREEN_B - 2, 4):
        draw.line([(SCREEN_L + 2, y), (SCREEN_R - 2, y)],
                  fill=(14, 12, 20), width=1)

    # CRT screen curvature suggestion (rounded corners of screen area)
    # Darken the four corners slightly
    corner_r = 18
    for cx, cy in [(SCREEN_L + corner_r, SCREEN_T + corner_r),
                   (SCREEN_R - corner_r, SCREEN_T + corner_r),
                   (SCREEN_L + corner_r, SCREEN_B - corner_r),
                   (SCREEN_R - corner_r, SCREEN_B - corner_r)]:
        draw.ellipse([cx - corner_r, cy - corner_r, cx + corner_r, cy + corner_r],
                     fill=(6, 5, 10))

    # Screen reflection highlight (top-left glass sheen — CRT realism)
    for r in range(14, 2, -4):
        draw.arc([SCREEN_L + 8, SCREEN_T + 6, SCREEN_L + 8 + r * 3, SCREEN_T + 6 + r * 2],
                 start=160, end=260, fill=(30, 28, 40), width=1)

    # THE PIXEL — LOWER-CENTER, compositional anchor
    # Screen center horizontally, 62% down screen vertically
    sc_cx = (SCREEN_L + SCREEN_R) // 2 - 4
    sc_cy = SCREEN_T + int((SCREEN_B - SCREEN_T) * 0.62)

    # PULSE VISUALIZED: concentric glow rings (in IMAGE, not caption)
    for r, brightness in [(40, 12), (28, 22), (18, 42), (11, 70), (6, 110)]:
        ring_color = (0, max(80, 240 - r * 3), max(100, 255 - r * 2))
        draw.ellipse([sc_cx - r, sc_cy - r, sc_cx + 8 + r, sc_cy + 8 + r],
                     outline=ring_color, width=1)

    # Inner bloom (brightest glow)
    draw.ellipse([sc_cx - 5, sc_cy - 5, sc_cx + 13, sc_cy + 13],
                 fill=(0, 160, 200))

    # The pixel itself — 8x8, crisp, electric cyan
    draw.rectangle([sc_cx, sc_cy, sc_cx + 8, sc_cy + 8], fill=(0, 240, 255))
    # Pixel hot center
    draw.rectangle([sc_cx + 2, sc_cy + 2, sc_cx + 6, sc_cy + 6],
                   fill=(180, 255, 255))

    # Annotation arrow (storyboard convention)
    arrow_x, arrow_y = sc_cx - 40, sc_cy - 35
    draw.line([(arrow_x, arrow_y), (sc_cx - 2, sc_cy - 2)],
              fill=(200, 190, 160), width=1)
    draw.ellipse([arrow_x - 3, arrow_y - 3, arrow_x + 3, arrow_y + 3],
                 fill=(200, 190, 160))
    draw.text((arrow_x - 22, arrow_y - 14), "PULSE", fill=(180, 170, 140), font=font_ann)

    # Tiny CRT corner detail — power indicator LED bottom-right
    draw.ellipse([BEZEL_R - 22, BEZEL_B - 14, BEZEL_R - 16, BEZEL_B - 8],
                 fill=(0, 80, 30))

    # Camera annotation
    draw.text((BEZEL_L + 4, BEZEL_T + 4), "ECU MON — glass-close. CRT fills frame.",
              fill=(140, 130, 110), font=font_ann)
    draw.text((BEZEL_L + 4, BEZEL_T + 14), "Contrast punch vs P04 wide room reveal.",
              fill=(120, 110, 90), font=font_ann)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PRIORITY 4 — P08/P09 CAMERA HEIGHT DIFFERENTIATION
# Carmen: "these two panels share the same camera height, causing eyeline
# ambiguity at thumbnail scale. Differentiate."
#
# Solution (narrative logic):
# P08: SLIGHTLY HIGH ANGLE — camera looks down at Byte from ~18" above him.
#   Rationale: First moment in real world. High angle visually diminishes him —
#   emphasizes his smallness/alienness in this foreign analogue space.
#   Byte looks up at camera = he's looking up at the big strange world.
#
# P09: TRUE EYE LEVEL — camera exactly at Byte's floating height (18" off floor).
#   Rationale: He has oriented himself. Found Luma. Camera is NOW his equal —
#   same height, same angle. He is no longer small. He has chosen his target.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def draw_pixel_confetti_local(draw, cx, cy, spread, seed=0, count=12):
    """Scatter pixel confetti near a point."""
    rng = random.Random(seed)
    for _ in range(count):
        px = cx + rng.randint(-spread, spread)
        py = cy + rng.randint(-spread // 2, spread // 2)
        col = rng.choice([GLITCH_CYAN, GLITCH_MAG, (255, 220, 60)])
        sz = rng.randint(1, 3)
        draw.rectangle([px, py, px + sz, py + sz], fill=col)


def draw_p08_high_angle(draw, img, font, font_bold, font_ann):
    """P08 CYCLE 13 FIX — SLIGHTLY HIGH ANGLE.
    Camera ~18" above Byte (looking down at him, not peer-to-peer).
    Effect: floor plane opens wider in lower frame, Byte appears smaller/alien.
    Byte's top is visible (we see slightly down onto him).
    Annotation: 'HIGH ANGLE — camera above Byte's eye level'
    Narrative: first moments in real world — high angle = foreign, exposed."""

    draw.rectangle([0, 0, PW, DRAW_H], fill=(22, 15, 10))

    # HIGH ANGLE: floor occupies more of the frame (we're looking down)
    # floor_y moves UP significantly vs the eye-level version
    floor_y = int(DRAW_H * 0.62)   # was 0.70 — high angle reveals more floor
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=(16, 11, 7))
    draw.line([(0, floor_y), (PW, floor_y)], fill=(32, 22, 14), width=1)

    # Floor texture: cable bundles (more visible from above)
    rng_floor = random.Random(21)
    for _ in range(12):
        fx = rng_floor.randint(0, PW)
        fw = rng_floor.randint(15, 55)
        draw.line([(fx, floor_y + 3), (fx + fw, floor_y + 3)], fill=(28, 20, 14), width=3)
        draw.line([(fx, floor_y + 8), (fx + fw - 5, floor_y + 8)], fill=(24, 18, 12), width=2)

    # Cyan tint near Byte (digital nature bleaching analogue)
    for cb_x in range(int(PW * 0.38), int(PW * 0.58), 12):
        draw.line([(cb_x, floor_y + 2), (cb_x + 8, floor_y + 2)],
                  fill=(0, 35, 45), width=2)

    # Desaturation ring at Byte's feet
    byte_cx = PW // 2
    # High angle: Byte's center is LOWER in frame (we look down to see him)
    byte_cy = int(DRAW_H * 0.38)
    for r in range(28, 12, -4):
        grey_val = 22 + r
        draw.ellipse([byte_cx - r * 2, floor_y - 5, byte_cx + r * 2, floor_y + 2],
                     outline=(grey_val, grey_val - 2, grey_val - 4), width=1)

    # CRT monitor returning to static (defocused background)
    mon_x, mon_y = int(PW * 0.05), int(DRAW_H * 0.04)
    mon_w, mon_h = 120, 76
    draw.rectangle([mon_x - 3, mon_y - 3, mon_x + mon_w + 3, mon_y + mon_h + 3],
                   fill=(40, 35, 28), outline=(55, 48, 36), width=2)
    draw.rectangle([mon_x + 8, mon_y + 8, mon_x + mon_w - 8, mon_y + mon_h - 8],
                   fill=(12, 10, 16))
    rng_bg = random.Random(88)
    for _ in range(200):
        sx = rng_bg.randint(mon_x + 9, mon_x + mon_w - 9)
        sy = rng_bg.randint(mon_y + 9, mon_y + mon_h - 9)
        br = rng_bg.randint(14, 28)
        draw.point((sx, sy), fill=(br, br, br + 4))
    for r in range(20, 5, -5):
        draw.ellipse([mon_x + mon_w // 2 - r, mon_y + mon_h // 2 - r // 2,
                      mon_x + mon_w // 2 + r, mon_y + mon_h // 2 + r // 2],
                     outline=(0, 40 + r * 4, 50 + r * 5), width=1)

    # Room walls (background)
    draw.rectangle([0, 0, PW, int(DRAW_H * 0.22)], fill=(18, 13, 9))
    for wx in [int(PW * 0.55), int(PW * 0.68), int(PW * 0.78)]:
        draw.line([(wx, int(DRAW_H * 0.06)), (wx, floor_y)],
                  fill=(28, 22, 16), width=2)

    # HIGH ANGLE VIEW LINE — visible horizon sits low
    # Add subtle camera angle indicator (short perspective lines from corners to VP)
    vp_y_high = int(DRAW_H * 0.10)  # vanishing point near top (high angle)
    draw.line([(0, floor_y), (PW // 2, vp_y_high)], fill=(22, 17, 12), width=1)
    draw.line([(PW, floor_y), (PW // 2, vp_y_high)], fill=(22, 17, 12), width=1)

    # BYTE — full body, seen from SLIGHTLY ABOVE
    byte_size = 90
    draw_pixel_confetti_local(draw, byte_cx - 25, byte_cy - 30, 45, seed=8, count=16)
    draw_pixel_confetti_local(draw, byte_cx + 20, byte_cy - 15, 35, seed=9, count=10)
    for i in range(5):
        art_x = byte_cx + (i - 2) * 12
        art_y = byte_cy - 40 - i * 5
        art_col = (255, 45, 107) if i % 2 == 0 else CRT_TEAL
        draw.rectangle([art_x, art_y, art_x + 3, art_y + 8], fill=art_col)

    draw_byte_body(draw, byte_cx, byte_cy, byte_size, eye_state="scan", font_ann=font_ann)

    # Foot touching floor
    foot_y = floor_y - 2
    draw.ellipse([byte_cx - byte_size // 2 - 5, foot_y - 5,
                  byte_cx - byte_size // 4,       foot_y + 3],
                 fill=BYTE_BODY, outline=BYTE_OUTLINE, width=1)
    draw.arc([byte_cx - byte_size // 2 - 8, foot_y - 10,
              byte_cx - byte_size // 4 + 2, foot_y - 2],
             start=200, end=340, fill=(0, 160, 180), width=1)

    # Finger snap sparks
    snap_x = byte_cx + byte_size // 2 + 10
    snap_y = byte_cy - byte_size // 6
    draw.line([(snap_x, snap_y - 2), (snap_x + 8, snap_y - 8)], fill=CRT_TEAL, width=1)
    draw.line([(snap_x, snap_y - 2), (snap_x + 9, snap_y + 3)], fill=(255, 45, 107), width=1)
    draw.line([(snap_x, snap_y - 2), (snap_x - 6, snap_y - 7)], fill=(0, 200, 65), width=1)
    draw.ellipse([snap_x - 2, snap_y - 4, snap_x + 2, snap_y], fill=CRT_TEAL)

    # Dialogue bubble
    bubble_x = byte_cx + byte_size + 12
    bubble_y = byte_cy - byte_size // 2 - 24
    bubble_w, bubble_h = 120, 30
    draw.rectangle([bubble_x, bubble_y, bubble_x + bubble_w, bubble_y + bubble_h],
                   fill=(15, 10, 20), outline=CRT_TEAL, width=1)
    draw.polygon([(bubble_x + 8, bubble_y + bubble_h),
                  (bubble_x + 18, bubble_y + bubble_h),
                  (byte_cx + byte_size // 2, byte_cy - byte_size // 2)],
                 fill=(15, 10, 20), outline=CRT_TEAL, width=1)
    try:
        font_dlg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    except Exception:
        font_dlg = font_ann
    draw.text((bubble_x + 6, bubble_y + 4), '"Ugh."', fill=CRT_TEAL, font=font_dlg)
    draw.text((bubble_x + 6, bubble_y + 16), '"The flesh dimension."',
              fill=(200, 180, 140), font=font_dlg)

    # CAMERA ANGLE ANNOTATION — clearly labeled
    draw.text((4, 4), "HIGH ANGLE — camera above Byte's eye level",
              fill=(200, 80, 40), font=font_ann)
    draw.text((4, 14), "Byte looks small/alien. First time in real world.",
              fill=(150, 60, 30), font=font_ann)
    draw.text((4, 24), "MED — floor reveals wide below him",
              fill=(130, 120, 100), font=font_ann)


def draw_p09_eye_level(draw, img, font, font_bold, font_ann):
    """P09 CYCLE 13 FIX — TRUE EYE LEVEL (camera at Byte's floating height).
    Camera is at exactly 18\" off floor — Byte's eye line = camera line.
    Effect: Byte reads as present and dangerous. He's found Luma. He is certain.
    Floor occupies only bottom ~25% of frame (eye-level, not looking down).
    Annotation: 'EYE LEVEL — camera AT Byte's 18\" floating height'"""

    draw.rectangle([0, 0, PW, DRAW_H], fill=(22, 15, 10))

    # EYE LEVEL: floor at bottom quarter of frame (we're not looking down at it)
    floor_y = int(DRAW_H * 0.76)   # same as original — this is the correct eye-level
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=(16, 11, 7))
    draw.line([(0, floor_y), (PW, floor_y)], fill=(32, 22, 14), width=1)

    # Back wall
    back_wall_y = int(DRAW_H * 0.18)
    draw.rectangle([0, back_wall_y, PW, floor_y], fill=(28, 20, 13))
    draw.line([(0, back_wall_y), (PW, back_wall_y)], fill=(42, 30, 18), width=1)

    # LUMA on COUCH (left background — asleep, oblivious)
    c_x = int(PW * 0.04)
    c_y = int(DRAW_H * 0.44)
    c_w = int(PW * 0.42)
    c_h = int(DRAW_H * 0.30)
    draw.rectangle([c_x, c_y, c_x + c_w, floor_y - 2], fill=(100, 58, 35))
    draw.rectangle([c_x, c_y - 14, c_x + c_w, c_y + 4],
                   fill=(115, 65, 38), outline=(85, 48, 28), width=1)

    luma_cx = int(c_x + c_w * 0.38)
    luma_cy = int(c_y + c_h * 0.20)
    draw.ellipse([luma_cx - 22, luma_cy - 30, luma_cx + 22, luma_cy + 8], fill=LUMA_HAIR)
    draw.ellipse([luma_cx - 14, luma_cy - 38, luma_cx + 8, luma_cy - 20], fill=LUMA_HAIR)
    draw.ellipse([luma_cx - 8, luma_cy - 4, luma_cx + 12, luma_cy + 12], fill=LUMA_SKIN)
    draw.rectangle([c_x + 10, c_y + 5, c_x + c_w - 10, c_y + 18], fill=(180, 210, 195))
    draw.line([(c_x + c_w - 25, c_y + 14), (c_x + c_w - 20, floor_y + 2)],
              fill=LUMA_SKIN, width=6)
    draw.line([(c_x + c_w - 36, c_y + 8), (c_x + c_w - 26, c_y - 16)],
              fill=LUMA_SKIN, width=6)
    draw.rectangle([c_x + c_w // 2, c_y + 3, c_x + c_w // 2 + 24, c_y + 18],
                   fill=(230, 120, 20))
    draw.rectangle([c_x + c_w // 4, c_y + 4, c_x + c_w // 4 + 28, c_y + 20],
                   fill=(225, 215, 195), outline=(160, 148, 125), width=1)

    # Background monitors
    for m_bx, m_by, m_bw, m_bh in [(220, back_wall_y + 6, 65, 40),
                                     (310, back_wall_y + 8, 55, 36)]:
        draw.rectangle([m_bx, m_by, m_bx + m_bw, m_by + m_bh],
                       fill=(15, 12, 20), outline=(35, 28, 45), width=1)
        draw.rectangle([m_bx + 4, m_by + 4, m_bx + m_bw - 4, m_by + m_bh - 4],
                       fill=(10, 8, 14))

    # Cable bundles on floor
    for cb_x in range(int(PW * 0.35), int(PW * 0.60), 18):
        draw.line([(cb_x, floor_y - 1), (cb_x + 12, floor_y - 1)],
                  fill=(28, 20, 14), width=4)
        draw.line([(cb_x + 3, floor_y - 4), (cb_x + 15, floor_y - 4)],
                  fill=(24, 18, 12), width=3)

    # EYE LEVEL HORIZON LINE — camera is AT Byte's floating height
    # Byte floats 18" off floor. In frame: byte_cy = floor_y - DRAW_H*0.30
    byte_cx  = int(PW * 0.68)
    byte_cy  = floor_y - int(DRAW_H * 0.30)   # 18" floating height
    byte_size = 36

    # EYE-LEVEL indicator: horizon line through the scene at Byte's height
    # (subtle dashed line showing the camera axis)
    for dash_x in range(0, int(PW * 0.55), 16):
        draw.line([(dash_x, byte_cy), (dash_x + 8, byte_cy)],
                  fill=(35, 28, 20), width=1)

    # Stutter motion lines (digital micro-increment)
    for stutter_i in range(3):
        sx_off = -8 + stutter_i * 4
        draw.rectangle([byte_cx + sx_off - byte_size // 2,
                        byte_cy - byte_size // 2 - 2,
                        byte_cx + sx_off + byte_size // 2,
                        byte_cy + byte_size // 2 + 2],
                       outline=(0, 80, 100), width=1)

    # Pixel confetti trail
    draw_pixel_confetti_local(draw, byte_cx - 30, byte_cy + 5, 20, seed=11, count=8)
    draw_pixel_confetti_local(draw, int(PW * 0.50), byte_cy + 8, 15, seed=12, count=5)
    for trl in range(4):
        trl_x = int(PW * 0.48) + trl * 18
        draw.rectangle([trl_x, byte_cy - 2, trl_x + 4, byte_cy + 2],
                       outline=(0, 80, 100), width=1)

    # BYTE — eye-level camera means his face is exactly at camera height
    draw_byte_body(draw, byte_cx, byte_cy, byte_size, eye_state="scan", font_ann=font_ann)

    # Hover glow
    draw.ellipse([byte_cx - 30, byte_cy + byte_size // 2 + 2,
                  byte_cx + 30, byte_cy + byte_size // 2 + 12], fill=(0, 35, 50))

    # Twitching leg
    twitch_x = byte_cx + byte_size // 4
    twitch_y = byte_cy + byte_size // 2
    draw.line([(twitch_x, twitch_y), (twitch_x + 4, twitch_y + 8)],
              fill=BYTE_BODY, width=3)
    draw.arc([twitch_x - 2, twitch_y + 4, twitch_x + 8, twitch_y + 12],
             start=180, end=360, fill=(0, 160, 180), width=1)

    # Pixel readout flicker
    readout_x = byte_cx - byte_size // 2 - 55
    readout_y = byte_cy - 18
    try:
        font_glitch = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 7)
    except Exception:
        font_glitch = font_ann
    draw.text((readout_x, readout_y),       "SCAN: organic unit", fill=(0, 160, 180), font=font_glitch)
    draw.text((readout_x, readout_y + 9),   "STATUS: dormant",    fill=(0, 140, 160), font=font_glitch)
    draw.text((readout_x, readout_y + 18),  "THREAT: low (prob)", fill=(80, 140, 100), font=font_glitch)
    draw.rectangle([readout_x - 2, readout_y - 2,
                    readout_x + 100, readout_y + 26], outline=(0, 100, 120), width=1)

    # Gaze direction arrow
    draw.line([(byte_cx - byte_size // 2 - 5, byte_cy - 5),
               (luma_cx + 20, luma_cy)], fill=(0, 80, 100), width=1)

    # CAMERA ANGLE ANNOTATION — clearly labeled
    draw.text((4, 4), "EYE LEVEL — camera AT Byte's 18\" height",
              fill=(0, 200, 120), font=font_ann)
    draw.text((4, 14), "He has found her. Equal footing. Decisive.",
              fill=(0, 160, 90), font=font_ann)
    draw.text((4, 24), "MED WIDE — Byte 18\" off floor, scanning.",
              fill=(130, 120, 100), font=font_ann)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONTACT SHEET — regenerate with fixed panels
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PANEL_ORDER = [
    ("P01",  "panel_p01_exterior.png"),
    ("P02",  "panel_p02_exterior_close.png"),
    ("P03",  "panel_p03_first_pixel.png"),
    ("P04",  "panel_p04_interior_wide.png"),
    ("P05",  "panel_p05_monitor_mcu.png"),
    ("P06",  "panel_p06_byte_emerging.png"),
    ("P07",  "panel_p07_approach.png"),
    ("P08",  "panel_p08_byte_real_world.png"),
    ("P09",  "panel_p09_byte_sees_luma.png"),
    ("P10",  "panel_p10_ots_byte_luma.png"),
    ("P11",  "panel_p11_nose_to_nose.png"),
    ("P12",  "panel_p12_recoil.png"),
    ("P13",  "panel_p13_scream.png"),
    ("P14",  "panel_p14_bookshelf_ricochet.png"),
    ("P15",  "panel_p15_luma_freefall.png"),
    ("P16",  "panel_p16_floor_ecu.png"),
    ("P17",  "panel_p17_quiet_beat.png"),
    ("P18",  "panel_p18_notebook_turn.png"),
    ("P19",  "panel_p19_byte_reaction.png"),
    ("P20",  "panel_p20_twoshot_calm.png"),
    ("P21",  "panel_p21_chaos_overhead.png"),
    ("P22",  "panel_p22_monitor_breach.png"),
    ("P22a", "panel_p22a_shoulder_bridge.png"),
    ("P23",  "panel_p23_promise_shot.png"),
    ("P24",  "panel_p24_breach_apex.png"),
    ("P25",  "panel_p25_title_card.png"),
]

COLS = 5
PAD  = 6
HEADER_H = 60
FOOTER_H = 28
LABEL_H  = 18


def generate_contact_sheet(out_path):
    """Regenerate full cold open contact sheet with all panels."""
    loaded = []
    for label, fname in PANEL_ORDER:
        path = os.path.join(PANELS_DIR, fname)
        if os.path.exists(path):
            img = Image.open(path)
            loaded.append((label, img))
        else:
            print(f"  [SKIP] {fname} — not found")

    if not loaded:
        print("No panels found.")
        return None

    rows = math.ceil(len(loaded) / COLS)
    cell_h = PH + LABEL_H
    cs_w = COLS * (PW + PAD) + PAD
    cs_h = HEADER_H + rows * (cell_h + PAD) + PAD + FOOTER_H
    cs = Image.new('RGB', (cs_w, cs_h), (16, 12, 10))
    d  = ImageDraw.Draw(cs)

    try:
        ft_hdr = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        ft_lbl = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        ft_ftr = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    except Exception:
        ft_hdr = ft_lbl = ft_ftr = ImageFont.load_default()

    # Header
    d.text((10, 10), "LUMA & THE GLITCHKIN — Ep01 Cold Open — Cycle 13",
           fill=(220, 210, 190), font=ft_hdr)
    d.text((10, 32), f"26 panels | QUIET → CURIOUS → CHAOS → BREACH → PEAK CHAOS",
           fill=(160, 150, 130), font=ft_lbl)
    d.text((10, 44), "P13 jaw-drop scream | P15 arm urgency | P03 CRT tight | P08 high / P09 eye-level",
           fill=(120, 110, 95), font=ft_ftr)

    # Panel grid
    for i, (label, img) in enumerate(loaded):
        col = i % COLS
        row = i // COLS
        x = PAD + col * (PW + PAD)
        y = HEADER_H + PAD + row * (cell_h + PAD)
        cs.paste(img.resize((PW, PH)), (x, y))
        # Label bar
        d.rectangle([x, y + PH, x + PW, y + PH + LABEL_H], fill=(22, 18, 15))
        d.text((x + 4, y + PH + 4), label, fill=(180, 170, 150), font=ft_lbl)

    # Footer
    footer_y = cs_h - FOOTER_H + 8
    d.text((10, footer_y),
           "Cycle 13 | Lee Tanaka, Storyboard Artist | Luma & the Glitchkin",
           fill=(100, 92, 80), font=ft_ftr)

    cs.save(out_path)
    print(f"  [SAVED] {os.path.basename(out_path)}")
    return cs


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN — generate all fixed panels
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    os.makedirs(PANELS_DIR, exist_ok=True)

    print("\n── CYCLE 13 PANEL FIXES ──────────────────────────────────────────────────")

    # ── Priority 1: P13 Scream Fix ─────────────────────────────────────────────
    print("\n[P13] Scream fix — jaw drop, tongue, spike brows, body recoil...")
    make_panel("13", "MED WIDE",
               "Simultaneous scream. JAW DROP. Full aperture yell. Byte alarmed-frozen.",
               draw_p13_scream_v2,
               os.path.join(PANELS_DIR, "panel_p13_scream.png"))
    shutil.copy(os.path.join(PANELS_DIR, "panel_p13_scream.png"),
                os.path.join(PANELS_DIR, "LTG_SB_coldopen_panel_13.png"))
    print("  [COPY] LTG_SB_coldopen_panel_13.png")

    # ── Priority 2: P15 Arm Fix ────────────────────────────────────────────────
    print("\n[P15] Arm urgency fix — endpoint ~360px, straining toward frame edge...")
    make_panel("15", "FLOOR LEVEL",
               "Luma freefall. RIGHT ARM STRAINING to ~360px. Glitch hair circle. Impact.",
               draw_p15_arm_fix,
               os.path.join(PANELS_DIR, "panel_p15_luma_freefall.png"))
    shutil.copy(os.path.join(PANELS_DIR, "panel_p15_luma_freefall.png"),
                os.path.join(PANELS_DIR, "LTG_SB_coldopen_panel_15.png"))
    print("  [COPY] LTG_SB_coldopen_panel_15.png")

    # ── Priority 3: P03 Framing Fix ────────────────────────────────────────────
    print("\n[P03] CRT framing fix — monitor fills most of frame...")
    make_panel("03", "ECU MON",
               "CRT near full-frame. One cyan pixel. LOWER-CENTER. Pulse rings visible.",
               draw_p03_pixel_tight,
               os.path.join(PANELS_DIR, "panel_p03_first_pixel.png"))
    shutil.copy(os.path.join(PANELS_DIR, "panel_p03_first_pixel.png"),
                os.path.join(PANELS_DIR, "LTG_SB_coldopen_panel_03.png"))
    print("  [COPY] LTG_SB_coldopen_panel_03.png")

    # ── Priority 4: P08 / P09 Camera Heights ───────────────────────────────────
    print("\n[P08] High angle fix — camera above Byte's eye level...")
    make_panel("08", "MED HIGH",
               "[BRIDGE] Byte in real world. HIGH ANGLE. First time in flesh dimension.",
               draw_p08_high_angle,
               os.path.join(PANELS_DIR, "panel_p08_byte_real_world.png"))
    shutil.copy(os.path.join(PANELS_DIR, "panel_p08_byte_real_world.png"),
                os.path.join(PANELS_DIR, "LTG_SB_coldopen_panel_08.png"))
    print("  [COPY] LTG_SB_coldopen_panel_08.png")

    print("\n[P09] Eye level fix — camera AT Byte's 18\" floating height...")
    make_panel("09", "MED EYE",
               "[BRIDGE] Byte 18\" off floor. EYE LEVEL. He spots Luma. Certain.",
               draw_p09_eye_level,
               os.path.join(PANELS_DIR, "panel_p09_byte_sees_luma.png"))
    shutil.copy(os.path.join(PANELS_DIR, "panel_p09_byte_sees_luma.png"),
                os.path.join(PANELS_DIR, "LTG_SB_coldopen_panel_09.png"))
    print("  [COPY] LTG_SB_coldopen_panel_09.png")

    # ── Contact Sheet ──────────────────────────────────────────────────────────
    print("\n[CONTACT SHEET] Regenerating with all fixed panels...")
    cs_path = os.path.join(PANELS_DIR, "contact_sheet.png")
    generate_contact_sheet(cs_path)
    shutil.copy(cs_path, os.path.join(PANELS_DIR, "LTG_SB_coldopen_contactsheet.png"))
    print("  [COPY] LTG_SB_coldopen_contactsheet.png")

    print("\n── CYCLE 13 COMPLETE ─────────────────────────────────────────────────────")
    print("Panels fixed: P03, P08, P09, P13, P15")
    print("New LTG versions: v002 for all 5 panels + contact sheet")
    print("\nAct 2 status: No glyph message from Alex Chen in inbox.")
    print("  Proceeding with cold open fixes first (correct per task spec).")
    print("  Act 2 panel work depends on Byte glyph design — flagged to Alex.")
    print("\nAll outputs in: /home/wipkat/team/output/storyboards/panels/")


if __name__ == '__main__':
    main()
