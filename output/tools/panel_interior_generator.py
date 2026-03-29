#!/usr/bin/env python3
"""
Panel Interior Generator — Luma & the Glitchkin
Cycle 6: Renders P02, P04, P05, P06, P08, P09, P10

Color system:
  - Warm amber/terracotta: Luma's house palette
  - CRT teal (#00F0FF / 0,240,255): Byte / glitch intruder
  - Void Black: (8, 6, 14)
  - Corrupted Amber outline on Byte: (255, 140, 0)

MEMORY.md lessons applied:
  - Pulse must be VISIBLE in image (concentric glow rings)
  - Lower-center is the compositional anchor for mystery elements
  - Bridge panels establish spatial geometry (3D contracts)
  - Contact sheet is the first test — arc must read in thumbnail
  - Distinctive house/character details go IN the image
  - Bridging panels are not optional — position changes must be shown
  - A storyboard panel cannot outsource storytelling to caption text
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os
import random

PW, PH = 480, 270
CAPTION_H = 48
DRAW_H = PH - CAPTION_H
BORDER = 2
BG_DRAW = (242, 240, 235)
BG_CAPTION = (25, 20, 18)
BORDER_COL = (20, 15, 12)
TEXT_CAPTION = (235, 228, 210)

# Palette constants
WARM_AMBER   = (42, 28, 14)          # room shadow
TERRACOTTA   = (180, 90, 45)         # wall surface
LUMA_SKIN    = (200, 136, 90)        # Luma skin tone
LUMA_HAIR    = (25, 15, 10)          # dark hair
CRT_TEAL     = (0, 240, 255)         # Byte / glitch
BYTE_BODY    = (0, 212, 232)         # Byte body fill
BYTE_OUTLINE = (255, 140, 0)         # Corrupted Amber outline
MONITOR_DARK = (12, 10, 18)          # inactive monitor screen
MONITOR_BEZEL = (55, 48, 65)         # monitor plastic casing
SCAN_LINE    = (14, 12, 20)          # CRT scanline color

OUT_DIR = "/home/wipkat/team/output/storyboards/panels"


def load_fonts():
    try:
        font       = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
        font_bold  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
        font_cap   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        font_ann   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    except Exception:
        fb = ImageFont.load_default()
        font = font_bold = font_cap = font_ann = fb
    return font, font_bold, font_cap, font_ann


def make_panel(panel_num, shot_type, caption, draw_fn, filename):
    img = Image.new('RGB', (PW, PH), BG_DRAW)
    draw = ImageDraw.Draw(img)
    font, font_bold, font_cap, font_ann = load_fonts()

    draw.rectangle([0, 0, PW, DRAW_H], fill=BG_DRAW)
    draw_fn(draw, font, font_bold, font_ann)

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.text((8, DRAW_H + 6), caption[:72], fill=TEXT_CAPTION, font=font_cap)

    # Border
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COL, width=BORDER)

    # Panel number badge
    draw.rectangle([0, 0, 40, 20], fill=(20, 15, 12))
    draw.text((4, 3), f"P{panel_num:02d}", fill=(235, 228, 210), font=font_bold)

    # Shot type badge
    sw = 90
    draw.rectangle([PW - sw, 0, PW, 20], fill=(20, 15, 12))
    draw.text((PW - sw + 4, 3), shot_type, fill=(235, 228, 210), font=font_bold)

    path = os.path.join(OUT_DIR, filename)
    img.save(path)
    print(f"Saved: {path}")
    return img


def draw_byte_body(draw, cx, cy, size, eye_state="processing", font_ann=None):
    """Reusable Byte character renderer.
    eye_state: 'processing' | 'scan' | 'alarmed' | 'curious'
    Uses Corrupted Amber outline per production bible."""
    bs = size
    c  = max(1, bs // 8)

    # Hover glow below body
    draw.ellipse([cx - bs, cy + bs // 2, cx + bs, cy + bs // 2 + bs // 4],
                 fill=(0, 50, 70))

    # Body polygon (chamfered rectangle — Byte's signature shape)
    body_pts = [
        (cx - bs // 2 + c, cy - bs // 2),
        (cx + bs // 2 - c, cy - bs // 2),
        (cx + bs // 2,     cy - bs // 2 + c),
        (cx + bs // 2,     cy + bs // 2 - c),
        (cx + bs // 2 - c, cy + bs // 2),
        (cx - bs // 2 + c, cy + bs // 2),
        (cx - bs // 2,     cy + bs // 2 - c),
        (cx - bs // 2,     cy - bs // 2 + c),
    ]
    draw.polygon(body_pts, fill=BYTE_BODY, outline=BYTE_OUTLINE, width=2)

    # Highlight strip on top edge
    draw.line(
        [(cx - bs // 2 + c, cy - bs // 2), (cx + bs // 2 - c, cy - bs // 2)],
        fill=CRT_TEAL, width=2
    )

    # Shadow on right side
    shadow_pts = [
        (cx,               cy - bs // 2 + c),
        (cx + bs // 2 - c, cy - bs // 2),
        (cx + bs // 2,     cy - bs // 2 + c),
        (cx + bs // 2,     cy + bs // 2 - c),
        (cx + bs // 2 - c, cy + bs // 2),
        (cx,               cy + bs // 2),
    ]
    draw.polygon(shadow_pts, fill=(0, 144, 176))

    # Eyes
    ew, eh = max(6, bs // 4), max(8, bs // 3)
    # Normal eye (right side of Byte = viewer's left in OTS, but generally left in direct shots)
    normal_ex = cx - bs // 4 - ew // 2
    cracked_ex = cx + bs // 8
    ey = cy - eh // 3

    # Normal eye (round, slightly squinted)
    draw.rectangle([normal_ex, ey, normal_ex + ew, ey + eh], fill=(255, 255, 255), outline=(10, 10, 20), width=1)
    draw.ellipse([normal_ex + 1, ey + 1, normal_ex + ew - 1, ey + eh - 1], outline=(0, 0, 0), width=1)

    # Cracked eye (pixel display)
    draw.rectangle([cracked_ex, ey, cracked_ex + ew, ey + eh], fill=(255, 255, 255), outline=(10, 10, 20), width=1)
    # Crack lines (diagonal across eye)
    draw.line([(cracked_ex, ey), (cracked_ex + ew, ey + eh)], fill=(0, 180, 200), width=1)
    draw.line([(cracked_ex + ew // 2, ey), (cracked_ex, ey + eh // 2)], fill=(0, 160, 180), width=1)

    # Pixel display in cracked eye based on state
    if eye_state == "processing":
        # Three rotating dots (processing symbol)
        dots = [(cracked_ex + 1, ey + 2), (cracked_ex + ew // 2, ey + eh - 3), (cracked_ex + ew - 2, ey + 2)]
        for dx, dy in dots:
            draw.rectangle([dx, dy, dx + 1, dy + 1], fill=CRT_TEAL)
    elif eye_state == "scan":
        # Horizontal scan line
        scan_y = ey + eh // 2
        draw.line([(cracked_ex, scan_y), (cracked_ex + ew, scan_y)], fill=CRT_TEAL, width=1)
    elif eye_state == "alarmed":
        # ! symbol
        for dy in [ey + 1, ey + 3, ey + 5]:
            draw.rectangle([cracked_ex + ew // 2 - 1, dy, cracked_ex + ew // 2 + 1, dy + 1], fill=CRT_TEAL)
        draw.rectangle([cracked_ex + ew // 2 - 1, ey + eh - 3, cracked_ex + ew // 2 + 1, ey + eh - 2], fill=CRT_TEAL)
    elif eye_state == "curious":
        # ? symbol approximation: arc + dot
        draw.arc([cracked_ex + 1, ey + 1, cracked_ex + ew - 1, ey + eh // 2 + 2],
                 start=0, end=270, fill=CRT_TEAL, width=1)
        draw.rectangle([cracked_ex + ew // 2 - 1, ey + eh - 3, cracked_ex + ew // 2 + 1, ey + eh - 2], fill=CRT_TEAL)

    # Stubby limbs
    arm_y = cy
    leg_y = cy + bs // 2
    arm_len = max(4, bs // 3)
    draw.rectangle([cx - bs // 2 - arm_len, arm_y - 2, cx - bs // 2, arm_y + 2], fill=BYTE_BODY, outline=BYTE_OUTLINE, width=1)
    draw.rectangle([cx + bs // 2,           arm_y - 2, cx + bs // 2 + arm_len, arm_y + 2], fill=BYTE_BODY, outline=BYTE_OUTLINE, width=1)
    draw.rectangle([cx - bs // 4 - 2, leg_y, cx - bs // 4 + 2, leg_y + arm_len], fill=BYTE_BODY, outline=BYTE_OUTLINE, width=1)
    draw.rectangle([cx + bs // 4 - 2, leg_y, cx + bs // 4 + 2, leg_y + arm_len], fill=BYTE_BODY, outline=BYTE_OUTLINE, width=1)


def draw_pixel_confetti(draw, cx, cy, radius, seed=0, count=12):
    """Scatter pixel confetti around a point — Byte's digital trail."""
    rng = random.Random(seed)
    for _ in range(count):
        angle  = rng.uniform(0, math.tau)
        dist   = rng.uniform(4, radius)
        px = cx + int(dist * math.cos(angle))
        py = cy + int(dist * math.sin(angle))
        color  = rng.choice([CRT_TEAL, (255, 45, 107), (0, 200, 65), (255, 220, 80)])
        size   = rng.randint(1, 3)
        draw.rectangle([px, py, px + size, py + size], fill=color)


def draw_crt_monitor(draw, mx, my, mw, mh, pixel_count=0, label=None, font_ann=None):
    """Draw a CRT monitor with optional active pixels on screen."""
    # Monitor body (deep bezel, yellowed plastic)
    draw.rectangle([mx, my, mx + mw, my + mh], fill=(62, 55, 42), outline=MONITOR_BEZEL, width=3)
    # Inner bezel shadow
    draw.rectangle([mx + 4, my + 4, mx + mw - 4, my + mh - 4], fill=(30, 25, 38), outline=(20, 18, 28), width=1)
    # Screen area
    screen_x1, screen_y1 = mx + 7, my + 7
    screen_x2, screen_y2 = mx + mw - 7, my + mh - 7
    draw.rectangle([screen_x1, screen_y1, screen_x2, screen_y2], fill=MONITOR_DARK)

    # Scanlines (analog CRT texture)
    for sy in range(screen_y1, screen_y2, 3):
        draw.line([(screen_x1, sy), (screen_x2, sy)], fill=SCAN_LINE, width=1)

    # Stickers (character detail)
    sticker_x = mx + mw - 14
    sticker_y = my + mh - 12
    draw.rectangle([sticker_x, sticker_y, sticker_x + 10, sticker_y + 6], fill=(200, 180, 60))
    draw.rectangle([sticker_x + 12, sticker_y - 1, sticker_x + 22, sticker_y + 5], fill=(100, 180, 255))

    # Active pixels (if any)
    if pixel_count > 0:
        rng = random.Random(pixel_count * 7 + mx)
        sw = screen_x2 - screen_x1
        sh = screen_y2 - screen_y1
        for i in range(pixel_count):
            # Cluster them in lower-center area (Cycle 4 lesson: lower-center is anchor)
            cluster_x = screen_x1 + sw // 2 + rng.randint(-sw // 4, sw // 4)
            cluster_y = screen_y1 + int(sh * 0.62) + rng.randint(-8, 8)
            draw.rectangle([cluster_x, cluster_y, cluster_x + 2, cluster_y + 2], fill=CRT_TEAL)
            # Micro glow
            if i < 3:
                draw.ellipse([cluster_x - 2, cluster_y - 2, cluster_x + 4, cluster_y + 4],
                             outline=(0, 120, 140), width=1)

    # Label
    if label and font_ann:
        draw.text((mx + 2, my + mh + 2), label, fill=(120, 110, 90), font=font_ann)


# ── P02: Exterior Close ───────────────────────────────────────────────────────

def draw_p02_exterior_close(draw, font, font_bold, font_ann):
    """P02: Eye-level exterior. House fills 2/3 frame. Living room window glowing.
    Warm terracotta walls, sage shutters, MIRI mailbox, circuit-board doormat.
    The warm/cool teal fight at curtain edges is the KEY IMAGE."""

    # Night sky (narrower slice now — we're closer)
    draw.rectangle([0, 0, PW, DRAW_H], fill=(18, 20, 32))

    # Ground / street
    ground_y = int(DRAW_H * 0.78)
    draw.rectangle([0, ground_y, PW, DRAW_H], fill=(20, 18, 14))
    # Street texture
    for x in range(0, PW, 40):
        draw.line([(x, ground_y + 4), (x + 20, ground_y + 4)], fill=(28, 24, 18), width=1)

    # House body (2/3 frame width, centered slightly left)
    hx, hy = 60, int(DRAW_H * 0.08)
    hw, hh = int(PW * 0.75), int(DRAW_H * 0.72)

    # House walls (warm terracotta)
    draw.rectangle([hx, hy + int(hh * 0.28), hx + hw, ground_y], fill=(160, 88, 52))
    # Wall texture / horizontal planks
    for row_y in range(hy + int(hh * 0.28), ground_y, 8):
        draw.line([(hx, row_y), (hx + hw, row_y)], fill=(148, 80, 46), width=1)

    # Roof (slightly peaked, dark)
    roof_peak_y = hy
    roof_base_y = hy + int(hh * 0.28)
    draw.polygon([
        (hx - 8, roof_base_y),
        (hx + hw + 8, roof_base_y),
        (hx + hw // 2, roof_peak_y),
    ], fill=(28, 20, 14))
    # Roof tile lines
    for i in range(1, 5):
        tx = hx + hw // 2 + (i * hw // 8)
        draw.line([(hx + hw // 2, roof_peak_y), (tx, roof_base_y)], fill=(20, 14, 10), width=1)
        tx2 = hx + hw // 2 - (i * hw // 8)
        draw.line([(hx + hw // 2, roof_peak_y), (tx2, roof_base_y)], fill=(20, 14, 10), width=1)

    # ANTENNA CLUSTER on rooftop (house distinctive detail — in image, not just bible)
    ax = hx + hw // 2
    ry = roof_peak_y
    # Main tall antenna
    draw.line([(ax, ry), (ax, ry - 32)], fill=(35, 28, 22), width=2)
    draw.line([(ax - 14, ry - 22), (ax + 14, ry - 22)], fill=(35, 28, 22), width=2)
    # Shorter side antenna
    draw.line([(ax + 18, ry - 2), (ax + 18, ry - 18)], fill=(35, 28, 22), width=2)
    draw.line([(ax + 10, ry - 14), (ax + 26, ry - 14)], fill=(35, 28, 22), width=2)
    # Tiny antenna light
    draw.ellipse([ax - 2, ry - 36, ax + 2, ry - 32], fill=(255, 50, 80))

    # Power lines (thin, threading in from edges)
    draw.line([(0, int(DRAW_H * 0.18)), (ax + 18, ry - 2)], fill=(40, 33, 26), width=1)
    draw.line([(PW, int(DRAW_H * 0.22)), (ax + 18, ry - 2)], fill=(40, 33, 26), width=1)

    # Sage green shutters
    shutter_col = (72, 100, 68)
    for sx, sy, sw_s, sh_s in [
        (hx + 8, hy + int(hh * 0.32), 18, 38),        # upper left shutter
        (hx + 42, hy + int(hh * 0.32), 18, 38),       # upper right shutter
        (hx + hw - 60, hy + int(hh * 0.32), 18, 38),  # upper right window shutters
        (hx + hw - 26, hy + int(hh * 0.32), 18, 38),
    ]:
        draw.rectangle([sx, sy, sx + sw_s, sy + sh_s], fill=shutter_col, outline=(55, 78, 52), width=1)
        # Shutter slats
        for sl in range(sy + 5, sy + sh_s, 6):
            draw.line([(sx + 2, sl), (sx + sw_s - 2, sl)], fill=(60, 86, 58), width=1)

    # Upper floor windows (bedroom — DARK)
    for wx in [hx + hw // 4 - 20, hx + hw * 3 // 4 - 20]:
        draw.rectangle([wx, hy + int(hh * 0.32), wx + 44, hy + int(hh * 0.58)],
                       fill=(15, 14, 22), outline=(100, 85, 65), width=2)
        # Window frame
        draw.line([(wx + 22, hy + int(hh * 0.32)), (wx + 22, hy + int(hh * 0.58))],
                  fill=(90, 75, 58), width=1)

    # ── KEY: LIVING ROOM WINDOW (lower-left) — GLOWING ──────────────────────
    # This is the story-critical element — warm amber curtains + teal fight at edges
    lw_x = hx + 20
    lw_y = hy + int(hh * 0.54)
    lw_w, lw_h = 80, 55

    # Curtain fill (warm amber, glowing from monitor light within)
    draw.rectangle([lw_x, lw_y, lw_x + lw_w, lw_y + lw_h], fill=(180, 130, 55))
    # Curtain folds
    for fold_x in range(lw_x + 10, lw_x + lw_w, 14):
        draw.line([(fold_x, lw_y), (fold_x, lw_y + lw_h)], fill=(160, 110, 40), width=2)
    # AMBER ↔ TEAL FIGHT at curtain edges (warm/cool struggle)
    for i in range(8):
        alpha = 1.0 - (i / 8)
        r_mix = int(200 * alpha)
        g_mix = int(200 * alpha + 180 * (1 - alpha))
        b_mix = int(60 * alpha + 220 * (1 - alpha))
        draw.rectangle([lw_x - i, lw_y, lw_x - i + 2, lw_y + lw_h],
                       fill=(max(0, r_mix - 80), g_mix // 3, b_mix // 2))
        draw.rectangle([lw_x + lw_w + i - 2, lw_y, lw_x + lw_w + i, lw_y + lw_h],
                       fill=(max(0, r_mix - 80), g_mix // 3, b_mix // 2))
    # Window frame
    draw.rectangle([lw_x - 2, lw_y - 2, lw_x + lw_w + 2, lw_y + lw_h + 2],
                   outline=(110, 88, 60), width=2)
    # Window cross bar
    draw.line([(lw_x + lw_w // 2, lw_y), (lw_x + lw_w // 2, lw_y + lw_h)], fill=(100, 80, 55), width=2)
    draw.line([(lw_x, lw_y + lw_h // 2), (lw_x + lw_w, lw_y + lw_h // 2)], fill=(100, 80, 55), width=2)

    # Glow spill on the ground below window
    for r in range(20, 5, -5):
        gx_c = lw_x + lw_w // 2
        gy_c = ground_y
        draw.ellipse([gx_c - r * 2, gy_c - r // 2, gx_c + r * 2, gy_c + r // 2],
                     outline=(60, 100, 80), width=1)

    # Climbing vines on left wall edge
    vine_x = hx + 5
    for vy in range(ground_y, hy + int(hh * 0.4), -15):
        draw.ellipse([vine_x + random.Random(vy).randint(-4, 8),
                      vy - 6,
                      vine_x + random.Random(vy).randint(4, 14),
                      vy + 2],
                     outline=(60, 88, 48), width=1)
    draw.line([(vine_x + 6, ground_y), (vine_x + 4, hy + int(hh * 0.5))], fill=(50, 75, 40), width=2)

    # MIRI MAILBOX
    mb_x = hx + hw + 15
    mb_y = ground_y - 28
    draw.rectangle([mb_x, mb_y, mb_x + 34, mb_y + 18], fill=(140, 80, 40), outline=(100, 60, 28), width=1)
    draw.ellipse([mb_x, mb_y, mb_x + 34, mb_y + 12], fill=(140, 80, 40))  # rounded top
    # Post
    draw.line([(mb_x + 17, mb_y + 18), (mb_x + 17, ground_y)], fill=(90, 65, 40), width=3)
    # MIRI text
    try:
        font_mb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 8)
    except Exception:
        font_mb = font_ann
    draw.text((mb_x + 4, mb_y + 4), "MIRI", fill=(220, 200, 140), font=font_mb)

    # Circuit-board doormat (pause-frame joke — in image per MEMORY lesson)
    dm_x = hx + hw // 2 - 25
    dm_y = ground_y - 8
    draw.rectangle([dm_x, dm_y, dm_x + 50, dm_y + 8], fill=(30, 50, 30), outline=(50, 80, 50), width=1)
    # Circuit traces on mat
    for tx in range(dm_x + 5, dm_x + 45, 8):
        draw.line([(tx, dm_y + 2), (tx + 4, dm_y + 2)], fill=(0, 180, 80), width=1)
        draw.ellipse([tx + 3, dm_y + 1, tx + 5, dm_y + 3], fill=(0, 200, 100))

    # Porch: old boots, potted fern
    # Boots
    draw.ellipse([hx + hw // 2 - 40, ground_y - 18, hx + hw // 2 - 22, ground_y - 4],
                 fill=(45, 32, 20), outline=(30, 20, 12), width=1)
    draw.ellipse([hx + hw // 2 - 25, ground_y - 20, hx + hw // 2 - 8, ground_y - 5],
                 fill=(45, 32, 20), outline=(30, 20, 12), width=1)
    # Fern pot
    pot_x = hx + hw + 5
    draw.rectangle([pot_x, ground_y - 22, pot_x + 16, ground_y - 6],
                   fill=(130, 80, 50), outline=(100, 60, 35), width=1)
    # Fern fronds
    for angle_deg in range(-80, 80, 25):
        angle_r = math.radians(angle_deg - 90)
        ex = pot_x + 8 + int(22 * math.cos(angle_r))
        ey = ground_y - 22 + int(22 * math.sin(angle_r))
        draw.line([(pot_x + 8, ground_y - 22), (ex, ey)], fill=(55, 100, 45), width=2)

    # Annotation
    draw.text((4, 4), "EYE LEVEL — street", fill=(150, 140, 120), font=font_ann)
    draw.text((4, 14), "WARM/COOL fight at curtain", fill=(130, 120, 100), font=font_ann)


# ── P04: Interior Wide ────────────────────────────────────────────────────────

def draw_p04_interior_wide(draw, font, font_bold, font_ann):
    """P04: WIDE interior — the tech den revealed. Luma asleep on couch.
    Slightly high angle (15° down), 3-quarter view from doorway corner.
    Warm amber/sage shadows, stacked CRT monitors, organized chaos.
    CRITICAL: Luma's sleeping position communicates character BEFORE dialogue."""

    # Room base — warm dark amber
    draw.rectangle([0, 0, PW, DRAW_H], fill=(22, 16, 10))

    # ── Room geometry: TWO-POINT PERSPECTIVE — three-quarter view from doorway corner ─
    # FIX: was one-point. Script specifies corner view with back wall + side wall both visible.
    # Camera is in the doorway corner, looking diagonally INTO the room.
    # VP1 = far left (back wall recedes left)  VP2 = far right (side wall recedes right)
    # Room corner (vertical edge) sits at about x=35% of frame — the dominant visual anchor.
    floor_y = int(DRAW_H * 0.74)
    corner_x = int(PW * 0.35)    # vertical room corner line (where back wall meets side wall)
    ceiling_y = int(DRAW_H * 0.14)  # ceiling height at corner
    # Vanishing points (both off-screen for natural FOV)
    vp1_x, vp1_y = -80, int(DRAW_H * 0.22)    # left VP (back wall)
    vp2_x, vp2_y = PW + 100, int(DRAW_H * 0.22)  # right VP (side wall)

    # BACK WALL (recedes to left VP — right portion of scene)
    # Bounded by: corner_x (left edge), right frame edge (right), ceiling/floor perspective lines
    back_wall_ceil_right = ceiling_y + int((PW - corner_x) * (vp2_y - ceiling_y) / (vp2_x - corner_x))
    back_wall_floor_right = floor_y + int((PW - corner_x) * (vp2_y - floor_y) / (vp2_x - corner_x))
    back_wall_pts = [
        (corner_x, ceiling_y),
        (PW,       max(0, back_wall_ceil_right)),
        (PW,       min(DRAW_H, back_wall_floor_right)),
        (corner_x, floor_y),
    ]
    draw.polygon(back_wall_pts, fill=(32, 24, 16))

    # SIDE WALL (recedes to right VP — left portion of scene, from doorway)
    # Bounded by: left frame edge, corner_x (right edge), ceiling/floor perspective lines
    side_wall_ceil_left = ceiling_y + int((0 - corner_x) * (vp1_y - ceiling_y) / (vp1_x - corner_x))
    side_wall_floor_left = floor_y + int((0 - corner_x) * (vp1_y - floor_y) / (vp1_x - corner_x))
    side_wall_pts = [
        (0,        max(0, side_wall_ceil_left)),
        (corner_x, ceiling_y),
        (corner_x, floor_y),
        (0,        min(DRAW_H, side_wall_floor_left)),
    ]
    draw.polygon(side_wall_pts, fill=(26, 19, 11))  # slightly darker — side wall in shadow

    # Room corner (vertical) — crisp line where the two walls meet
    draw.line([(corner_x, ceiling_y), (corner_x, floor_y)], fill=(55, 40, 24), width=2)

    # Ceiling plane
    ceil_pts = [
        (0,        max(0, side_wall_ceil_left)),
        (corner_x, ceiling_y),
        (PW,       max(0, back_wall_ceil_right)),
        (PW, 0),
        (0, 0),
    ]
    draw.polygon(ceil_pts, fill=(20, 14, 9))

    # Floor plane
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=(18, 13, 8))
    draw.line([(0, floor_y), (PW, floor_y)], fill=(38, 28, 16), width=1)

    # Perspective floor lines radiating from the corner toward both VPs
    draw.line([(corner_x, floor_y), (vp1_x, vp1_y)], fill=(28, 20, 12), width=1)
    draw.line([(corner_x, floor_y), (vp2_x, vp2_y)], fill=(28, 20, 12), width=1)
    # Additional floor grid lines
    for frac in [0.2, 0.5, 0.8]:
        fx_left = int(corner_x * (1 - frac))
        fy_left = int(floor_y + (DRAW_H - floor_y) * frac * 0.4)
        draw.line([(fx_left, fy_left), (vp2_x, vp2_y)], fill=(24, 17, 10), width=1)
        fx_right = int(corner_x + (PW - corner_x) * frac)
        fy_right = int(floor_y + (DRAW_H - floor_y) * frac * 0.4)
        draw.line([(fx_right, fy_right), (vp1_x, vp1_y)], fill=(24, 17, 10), width=1)

    # back_wall_y alias — used by downstream code to position monitors/shelves
    back_wall_y = ceiling_y

    # ── STACKED CRT MONITORS on back wall / shelves ────────────────────────
    # These are the environmental character of the room
    # Monitor shelf (back wall center-right)
    shelf_specs = [
        (200, back_wall_y + 5,  75, 48, 0),    # main CRT — THE one with the pixel
        (285, back_wall_y + 8,  65, 42, 0),    # side monitor
        (200, back_wall_y + 60, 70, 44, 2),    # lower shelf monitor (2 pixels)
        (130, back_wall_y + 12, 60, 38, 0),    # left stack monitor
    ]
    for mx, my, mw, mh, npx in shelf_specs:
        draw_crt_monitor(draw, mx, my, mw, mh, pixel_count=npx, font_ann=font_ann)

    # ── THE KEY CRT (P03's monitor) with TWO cyan pixels ──────────────────
    # Upper-left background — per script: "two pixels now, barely noticeable"
    # This is the plant for the re-watch
    kx, ky = 205, back_wall_y + 8
    kw, kh = 72, 45
    # Two pixels (lower-center area of screen — compositional anchor)
    screen_cx = kx + 7 + (kw - 14) // 2
    screen_bottom = ky + 7 + (kh - 14)
    draw.rectangle([screen_cx - 4, screen_bottom - 8, screen_cx - 2, screen_bottom - 6], fill=CRT_TEAL)
    draw.rectangle([screen_cx,     screen_bottom - 8, screen_cx + 2, screen_bottom - 6], fill=CRT_TEAL)
    # Micro glow rings around the pixels (pulse VISIBLE per MEMORY lesson)
    for r in (6, 10):
        draw.ellipse([screen_cx - r, screen_bottom - 8 - r, screen_cx + r, screen_bottom - 6 + r],
                     outline=(0, 120, 140), width=1)

    # Shelves
    for shelf_y in [back_wall_y + 55, back_wall_y + 105]:
        draw.line([(120, shelf_y), (380, shelf_y)], fill=(55, 42, 28), width=3)

    # ZIP drives, circuit boards as art on the wall
    for i, cx_art in enumerate([142, 165, 386, 408]):
        col = (40 + i * 8, 35 + i * 5, 50 + i * 10)
        draw.rectangle([cx_art, back_wall_y + 20, cx_art + 16, back_wall_y + 36], fill=col, outline=(60, 55, 70), width=1)

    # ── CABLES (bundled like hanging vines) ───────────────────────────────
    for cx_cable, cy_top in [(250, back_wall_y + 50), (310, back_wall_y + 55), (180, back_wall_y + 48)]:
        for i in range(3):
            wave_x = cx_cable + i * 3
            draw.line([(wave_x, cy_top), (wave_x + 4, floor_y - 10)], fill=(30, 25, 20), width=1)
    # Cable bundles on floor (cyan-lit as glitch creeps)
    for cb_x in range(120, 380, 25):
        draw.line([(cb_x, floor_y - 2), (cb_x + 15, floor_y - 2)], fill=(28, 22, 16), width=3)
    # Thin cyan tint on cables nearest the monitor (early glitch invasion)
    for cb_x in range(195, 295, 15):
        draw.line([(cb_x, floor_y - 2), (cb_x + 10, floor_y - 2)], fill=(0, 45, 55), width=2)

    # ── LUMA ON COUCH (CHARACTER INTRODUCTION) ────────────────────────────
    # Couch: center-frame, worn, warm terracotta fabric
    couch_x  = int(PW * 0.22)
    couch_y  = int(DRAW_H * 0.44)
    couch_w  = int(PW * 0.54)
    couch_h  = int(DRAW_H * 0.30)
    floor_pos = floor_y - 2

    # Couch body
    draw.rectangle([couch_x, couch_y, couch_x + couch_w, floor_pos], fill=(120, 68, 40))
    draw.rectangle([couch_x, couch_y, couch_x + couch_w, couch_y + 8], fill=(140, 80, 48))  # seat edge
    # Couch back (higher)
    draw.rectangle([couch_x, couch_y - 18, couch_x + couch_w, couch_y + 4], fill=(130, 72, 42), outline=(100, 56, 30), width=1)
    # Couch legs
    for lx_leg in [couch_x + 8, couch_x + couch_w - 16]:
        draw.rectangle([lx_leg, floor_pos - 4, lx_leg + 8, floor_pos + 6], fill=(80, 50, 28))

    # LUMA — chaotic sleeping position (per script: body gave up mid-activity)
    # She's sideways, face buried in backrest, one leg off the couch, one leg thrown over the back
    luma_cx = int(couch_x + couch_w * 0.40)  # slightly left of center

    # BODY: sideways diagonal — torso laid across couch, PJ top visible
    # PJ top (mint/pale with pixel-grid pattern)
    pj_color = (180, 210, 195)  # pale mint
    # Torso (diagonal, sprawled — body going left-right across the couch seat)
    torso_pts = [
        (couch_x + 18, couch_y + 6),         # left hip
        (couch_x + couch_w - 30, couch_y + 10),  # right hip
        (couch_x + couch_w - 25, couch_y + 22), # right shoulder
        (couch_x + 22, couch_y + 20),         # left shoulder
    ]
    draw.polygon(torso_pts, fill=pj_color, outline=(140, 170, 152), width=1)
    # Pixel grid pattern on PJ (tiny squares)
    for px_g in range(couch_x + 25, couch_x + couch_w - 32, 8):
        for py_g in range(couch_y + 8, couch_y + 20, 8):
            draw.rectangle([px_g, py_g, px_g + 3, py_g + 3], outline=(140, 170, 152), width=1)

    # HEAD: face buried into couch backrest — only back-of-head visible, with chaotic HAIR
    head_cx = couch_x + 20   # left armrest end (head resting here)
    head_cy = couch_y - 2
    # Hair cloud (POOFY, gravity-defying — key character marker)
    draw.ellipse([head_cx - 28, head_cy - 38, head_cx + 28, head_cy + 10], fill=LUMA_HAIR)
    # Extra poof bits
    draw.ellipse([head_cx - 20, head_cy - 48, head_cx + 8, head_cy - 28], fill=LUMA_HAIR)
    draw.ellipse([head_cx + 2, head_cy - 45, head_cx + 28, head_cy - 25], fill=LUMA_HAIR)
    # One escaped ringlet visible at edge
    draw.arc([head_cx + 18, head_cy - 28, head_cx + 34, head_cy - 12], start=160, end=340, fill=LUMA_HAIR, width=3)
    # Back of neck / skin peeking from hair
    draw.ellipse([head_cx - 10, head_cy - 5, head_cx + 10, head_cy + 12], fill=LUMA_SKIN)

    # LEFT LEG: dangling off couch onto floor
    draw.line([(couch_x + couch_w - 40, couch_y + 18), (couch_x + couch_w - 35, floor_pos + 5)],
              fill=LUMA_SKIN, width=8)
    # Foot flat on floor
    draw.ellipse([couch_x + couch_w - 44, floor_pos, couch_x + couch_w - 22, floor_pos + 10],
                 fill=LUMA_SKIN, outline=(170, 108, 65), width=1)

    # RIGHT LEG: thrown over back of couch (dangling behind)
    draw.line([(couch_x + couch_w - 55, couch_y + 10),
               (couch_x + couch_w - 44, couch_y - 22)],
              fill=LUMA_SKIN, width=8)
    # Foot dangling behind couch back
    draw.ellipse([couch_x + couch_w - 55, couch_y - 32,
                  couch_x + couch_w - 35, couch_y - 18],
                 fill=LUMA_SKIN, outline=(170, 108, 65), width=1)

    # ARM: flung across top cushion
    draw.line([(luma_cx, couch_y + 12), (couch_x + couch_w - 10, couch_y - 4)],
              fill=LUMA_SKIN, width=6)

    # ── PROPS: Characterization through objects ────────────────────────────
    # NEON CRUNCH bag (electric orange, "EXTREME FLAVOR" — chosen for color)
    bag_x = int(couch_x + couch_w * 0.52)
    bag_y = couch_y + 4
    draw.rectangle([bag_x, bag_y, bag_x + 32, bag_y + 22], fill=(230, 120, 20), outline=(200, 90, 10), width=1)
    draw.rectangle([bag_x + 2, bag_y + 2, bag_x + 30, bag_y + 10], fill=(255, 160, 30))  # logo area
    # Cheese puffs on couch seat (in Luma's hair and scattered)
    for px_puff, py_puff in [(head_cx - 5, couch_y - 8), (head_cx + 6, couch_y - 4),
                               (bag_x - 10, couch_y + 12), (bag_x + 38, couch_y + 6)]:
        draw.ellipse([px_puff, py_puff, px_puff + 5, py_puff + 3], fill=(240, 160, 50))
    # One puff visibly in hair
    draw.ellipse([head_cx + 8, head_cy - 20, head_cx + 14, head_cy - 16], fill=(240, 160, 50))

    # NOTEBOOK on lap (tilted but balanced — remarkable feat)
    nb_x = int(couch_x + couch_w * 0.28)
    nb_y = couch_y + 4
    # Notebook body (slightly tilted)
    nb_pts = [(nb_x, nb_y + 4), (nb_x + 38, nb_y), (nb_x + 40, nb_y + 24), (nb_x + 2, nb_y + 28)]
    draw.polygon(nb_pts, fill=(230, 220, 200), outline=(160, 150, 130), width=1)
    # Lines of text (chaotic — Luma's writing style)
    for line_y in range(nb_y + 6, nb_y + 22, 4):
        draw.line([(nb_x + 4, line_y + 2), (nb_x + 34, line_y + 1)], fill=(140, 130, 110), width=1)
    # Project title visible: "HISTORY OF THE INTERNET"
    try:
        font_nb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 5)
    except Exception:
        font_nb = font_ann
    draw.text((nb_x + 3, nb_y + 2), "HISTORY OF THE INTERNET", fill=(80, 70, 55), font=font_nb)
    # Margin doodles (tiny pixel character sketch)
    draw.rectangle([nb_x + 28, nb_y + 12, nb_x + 32, nb_y + 22], outline=(100, 90, 75), width=1)
    draw.rectangle([nb_x + 30, nb_y + 10, nb_x + 34, nb_y + 12], fill=(100, 90, 75))  # head
    # Mid-word trailing off — last line shorter
    draw.line([(nb_x + 4, nb_y + 24), (nb_x + 18, nb_y + 23)], fill=(120, 110, 90), width=1)

    # FIZZ-BOMB energy drink cans on end table
    table_x = couch_x + couch_w + 8
    table_y = couch_y + 2
    draw.rectangle([table_x, table_y, table_x + 20, floor_pos - 2], fill=(55, 40, 28))
    # Three crushed/empty cans
    for ci, can_y_offset in enumerate([0, -14, -26]):
        can_y = floor_pos - 18 + can_y_offset
        draw.rectangle([table_x + 3, can_y, table_x + 17, can_y + 12],
                       fill=(220 - ci * 20, 80 + ci * 20, 40), outline=(180, 60, 30), width=1)

    # ── Knitted blanket folded over recliner (background detail) ──────────
    rec_x = int(PW * 0.72)
    rec_y = int(DRAW_H * 0.36)
    draw.rectangle([rec_x, rec_y, rec_x + 48, floor_pos - 2], fill=(68, 48, 32))
    draw.rectangle([rec_x, rec_y - 8, rec_x + 48, rec_y + 6], fill=(80, 56, 36))  # headrest
    # Knitted blanket
    draw.rectangle([rec_x + 2, rec_y + 2, rec_x + 46, rec_y + 24], fill=(140, 100, 65))
    # Knit texture
    for kx_t in range(rec_x + 4, rec_x + 44, 6):
        draw.arc([kx_t, rec_y + 4, kx_t + 4, rec_y + 10], start=0, end=180, fill=(120, 85, 55), width=1)
        draw.arc([kx_t, rec_y + 8, kx_t + 4, rec_y + 14], start=180, end=360, fill=(120, 85, 55), width=1)

    # ── Technical manuals bookshelf ────────────────────────────────────────
    shelf_x = int(PW * 0.74)
    shelf_bk_y = back_wall_y + 15
    draw.line([(shelf_x, shelf_bk_y + 30), (PW - 5, shelf_bk_y + 30)], fill=(55, 42, 28), width=3)
    # Books
    book_colors = [(160, 60, 30), (55, 90, 140), (40, 110, 60), (180, 140, 40), (120, 40, 120)]
    bk_x = shelf_x + 2
    for bc in book_colors:
        bk_w = random.Random(bk_x).randint(10, 16)
        draw.rectangle([bk_x, shelf_bk_y + 4, bk_x + bk_w, shelf_bk_y + 30],
                       fill=bc, outline=(bc[0]//2, bc[1]//2, bc[2]//2), width=1)
        bk_x += bk_w + 1

    # Annotations
    draw.text((4, 4), "WIDE INTERIOR — 15° down", fill=(150, 140, 120), font=font_ann)
    draw.text((4, 14), "LUMA: collapsed mid-activity", fill=(130, 120, 100), font=font_ann)


# ── P05: MCU Monitor Screen (inside the shelf) ────────────────────────────────

def draw_p05_monitor_mcu(draw, font, font_bold, font_ann):
    """P05: MCU from INSIDE the shelf looking out. Low angle, slightly up.
    Monitor screen fills upper 2/3. 8-12 cyan pixels clustered, pulsing.
    Luma's sleeping form visible as warm blur in background (left, above monitor).
    WE ARE ON THE MONITOR'S SIDE NOW. The threat has geography."""

    # Shelf environment — very close, dark
    draw.rectangle([0, 0, PW, DRAW_H], fill=(10, 8, 14))

    # ── Monitor bottom edge (housing cuts across lower frame) ─────────────
    # We're looking UP at the monitor from below-and-in-front on the shelf
    monitor_bottom = int(DRAW_H * 0.70)
    monitor_left   = 30
    monitor_right  = PW - 30

    # Plastic housing bottom (yellowed, chunky)
    draw.rectangle([monitor_left, monitor_bottom, monitor_right, DRAW_H],
                   fill=(65, 58, 44), outline=(50, 44, 32), width=2)
    # Vent slots on bottom of monitor housing
    for vx in range(monitor_left + 20, monitor_right - 20, 14):
        draw.rectangle([vx, monitor_bottom + 6, vx + 8, monitor_bottom + 10],
                       fill=(45, 38, 28))
    # Stickers on housing bottom
    draw.rectangle([monitor_right - 40, monitor_bottom + 4, monitor_right - 24, monitor_bottom + 14],
                   fill=(180, 160, 50))
    draw.rectangle([monitor_right - 20, monitor_bottom + 5, monitor_right - 8, monitor_bottom + 13],
                   fill=(80, 120, 200))

    # ── Screen (upper 2/3 of frame) ────────────────────────────────────────
    screen_top = 5
    screen_bot = monitor_bottom - 4
    screen_lft = monitor_left + 8
    screen_rgt = monitor_right - 8

    # Screen fill — static dark
    draw.rectangle([screen_lft, screen_top, screen_rgt, screen_bot], fill=(10, 8, 16))

    # Analog static texture (NOT digital noise — film grain feel)
    rng_static = random.Random(99)
    for _ in range(800):
        sx = rng_static.randint(screen_lft, screen_rgt)
        sy = rng_static.randint(screen_top, screen_bot)
        brightness = rng_static.randint(15, 40)
        draw.point((sx, sy), fill=(brightness, brightness - 2, brightness + 5))

    # Phosphor scanlines (analog CRT — horizontal lines, warm-greenish cast)
    for sy in range(screen_top, screen_bot, 3):
        draw.line([(screen_lft, sy), (screen_rgt, sy)], fill=(12, 10, 18), width=1)

    # CRT screen edge glow (phosphor bloom)
    for r in range(5, 1, -1):
        draw.rectangle([screen_lft - r, screen_top - r, screen_rgt + r, screen_bot + r],
                       outline=(0, 25 + r * 8, 30 + r * 10), width=1)

    # ── THE PIXEL CLUSTER: 8-12 pixels, lower-center, organized HEARTBEAT ─
    # Lower-center = compositional anchor (MEMORY lesson: where the eye rests)
    screen_w = screen_rgt - screen_lft
    screen_h = screen_bot - screen_top
    cluster_cx = screen_lft + int(screen_w * 0.52)  # slightly right of center
    cluster_cy = screen_top + int(screen_h * 0.64)  # lower-center anchor

    # Outer pulse rings FIRST (visible pulse — MEMORY lesson)
    for r, opacity in [(42, 15), (30, 28), (20, 50), (12, 85)]:
        ring_col = (0, max(60, 220 - r * 3), max(80, 240 - r * 2))
        draw.ellipse([cluster_cx - r, cluster_cy - r, cluster_cx + r + 4, cluster_cy + r + 4],
                     outline=ring_col, width=1)

    # 10 cyan pixels in irregular heartbeat cluster
    pixel_positions = [
        (0, 0), (3, 2), (-2, 3), (5, -1), (-3, -2),
        (2, 5), (-4, 4), (6, 3), (1, -4), (4, 1)
    ]
    for pdx, pdy in pixel_positions:
        px_x = cluster_cx + pdx * 3
        px_y = cluster_cy + pdy * 3
        draw.rectangle([px_x, px_y, px_x + 2, px_y + 2], fill=CRT_TEAL)
        # Hot center
        draw.rectangle([px_x, px_y, px_x + 1, px_y + 1], fill=(180, 255, 255))

    # ── FOREGROUND SHELF SURFACE (we're on the shelf) ─────────────────────
    shelf_surface_y = int(DRAW_H * 0.82)
    draw.rectangle([0, shelf_surface_y, PW, DRAW_H], fill=(20, 16, 12))

    # Shelf detritus at camera level (cable coil, floppy disk sleeve)
    # Cable coil (left foreground)
    draw.ellipse([20, shelf_surface_y - 5, 65, shelf_surface_y + 15],
                 outline=(32, 26, 20), width=3)
    draw.ellipse([28, shelf_surface_y - 1, 57, shelf_surface_y + 11],
                 outline=(28, 22, 16), width=2)
    # Floppy disk sleeve (right foreground, partially in frame)
    draw.rectangle([PW - 50, shelf_surface_y - 2, PW - 5, shelf_surface_y + 16],
                   fill=(48, 42, 58), outline=(38, 32, 48), width=1)
    draw.line([(PW - 48, shelf_surface_y + 6), (PW - 7, shelf_surface_y + 6)],
              fill=(60, 52, 72), width=1)

    # ── LUMA in background (warm blurry shape — we have crossed to monitor side) ─
    # She is above and to the LEFT of the monitor, soft-focus
    # Draw as a warm amber blur (suggestion of form only)
    luma_blur_x = 20
    luma_blur_y = int(DRAW_H * 0.28)
    for r in range(35, 5, -8):
        alpha_r = 255 - r * 5
        warm_col = (max(0, 80 - r * 2), max(0, 50 - r * 2), max(0, 15 - r))
        draw.ellipse([luma_blur_x - r, luma_blur_y - r * 2,
                      luma_blur_x + r * 2, luma_blur_y + r],
                     fill=warm_col)
    # Hair blur (dark blob above the warm shape)
    draw.ellipse([luma_blur_x - 15, luma_blur_y - 30,
                  luma_blur_x + 25, luma_blur_y - 5],
                 fill=(18, 12, 8))

    # Annotations
    draw.text((4, 4), "MCU — inside shelf, low angle UP", fill=(150, 140, 120), font=font_ann)
    draw.text((4, 14), "WE ARE ON THE MONITOR'S SIDE", fill=(0, 140, 160), font=font_ann)
    draw.text((cluster_cx - 18, cluster_cy - 50), "PIXEL\nCLUSTER", fill=(0, 180, 200), font=font_ann)
    # Arrow to cluster
    draw.line([(cluster_cx - 5, cluster_cy - 32), (cluster_cx, cluster_cy - 14)],
              fill=(0, 160, 180), width=1)


# ── P06: CU Monitor Screen — Byte emerging ────────────────────────────────────

def draw_p06_byte_emerging(draw, font, font_bold, font_ann):
    """P06: Screen FILLS the frame. Byte's face pressing against the glass from inside.
    FIRST APPEARANCE OF BYTE. Expression: DISGUSTED/CURIOUS (not menacing).
    Pixel confetti beginning to bleed from bulge point.
    CRT scan lines over entire frame — we are looking AT the screen."""

    # Screen fill (all the way to frame edges — screen IS the frame)
    draw.rectangle([0, 0, PW, DRAW_H], fill=(8, 6, 14))

    # ── Analog static field (background of screen) ────────────────────────
    rng = random.Random(13)
    for _ in range(1200):
        sx = rng.randint(0, PW)
        sy = rng.randint(0, DRAW_H)
        br = rng.randint(12, 35)
        draw.point((sx, sy), fill=(br, br - 1, br + 3))

    # Phosphor scanlines (dense — we're very close to the screen)
    for sy in range(0, DRAW_H, 2):
        draw.line([(0, sy), (PW, sy)], fill=(6, 5, 10), width=1)

    # ── BYTE'S FACE pressed against glass from inside ─────────────────────
    # Face is pressed flat — like a kid against a bakery window
    # His face fills about 1/3 of the screen at this scale
    # FIX: Move face off-center — lower-center per compositional principles.
    # Lower-center = anchor, weight, discovery. Off-center = pressing effort.
    face_cx = int(PW * 0.50)   # horizontal: centered-left (slightly left of center)
    face_cy = int(DRAW_H * 0.58)  # FIX: was 0.46 (center) — now lower-center, reads as pressing UP
    face_size = 80  # larger — this is his BIG reveal shot

    # Distortion field around face (pressing against the membrane)
    for r in range(80, 15, -15):
        distortion_col = (0, max(20, 60 - r // 2), max(25, 80 - r // 2))
        draw.ellipse([face_cx - r, face_cy - r * 3 // 4,
                      face_cx + r, face_cy + r * 3 // 4],
                     outline=distortion_col, width=1)

    # ── BYTE FACE CONSTRUCTION (pressed flat, facing viewer) ──────────────
    # Body/face is a flattened chamfered rectangle (pressed against glass = slightly distorted)
    half = face_size // 2
    c_ch = max(4, face_size // 8)

    face_pts = [
        (face_cx - half + c_ch, face_cy - half),
        (face_cx + half - c_ch, face_cy - half),
        (face_cx + half,        face_cy - half + c_ch),
        (face_cx + half,        face_cy + half - c_ch),
        (face_cx + half - c_ch, face_cy + half),
        (face_cx - half + c_ch, face_cy + half),
        (face_cx - half,        face_cy + half - c_ch),
        (face_cx - half,        face_cy - half + c_ch),
    ]
    # Main body — electric cyan with slight squish (pressed against glass)
    draw.polygon(face_pts, fill=(0, 200, 218), outline=(0, 240, 255), width=3)

    # Glass-pressed highlight (brighter on the surface touching glass)
    draw.line([(face_cx - half + c_ch, face_cy - half), (face_cx + half - c_ch, face_cy - half)],
              fill=(180, 255, 255), width=3)
    draw.line([(face_cx - half, face_cy - half + c_ch), (face_cx - half, face_cy + half - c_ch)],
              fill=(120, 240, 255), width=2)

    # Corrupted Amber outline (production bible: Byte's outline color)
    draw.polygon(face_pts, outline=BYTE_OUTLINE, width=1)

    # ── EYES (EXPRESSION: DISGUSTED/CURIOUS — not menacing) ───────────────
    eye_y = face_cy - face_size // 6

    # NORMAL EYE (viewer's RIGHT) — 70% aperture, assessment squint
    ne_x = face_cx + face_size // 8
    ne_w, ne_h = 18, 16
    # Eyelid at 70% (upper lid cuts across top 30%)
    draw.ellipse([ne_x - ne_w // 2, eye_y - ne_h // 2, ne_x + ne_w // 2, eye_y + ne_h // 2],
                 fill=(240, 240, 230))
    # 70% aperture — upper lid mask
    draw.rectangle([ne_x - ne_w // 2, eye_y - ne_h // 2, ne_x + ne_w // 2, eye_y - ne_h // 4],
                   fill=(0, 200, 218))  # lid cut (same color as face = squinted)
    # Pupil (assessing, not wide — this is "examining something unpleasant")
    draw.ellipse([ne_x - 4, eye_y - 3, ne_x + 4, eye_y + 5], fill=(10, 10, 20))
    draw.ellipse([ne_x - 2, eye_y - 1, ne_x + 2, eye_y + 3], fill=(30, 200, 220))  # catch light

    # CRACKED EYE (viewer's LEFT) — SEARCHING/PROCESSING symbol
    ce_x = face_cx - face_size // 8
    ce_w, ce_h = 18, 16
    draw.ellipse([ce_x - ce_w // 2, eye_y - ce_h // 2, ce_x + ce_w // 2, eye_y + ce_h // 2],
                 fill=(240, 240, 230))
    # Crack lines across the iris
    draw.line([(ce_x - ce_w // 2, eye_y - ce_h // 2), (ce_x + ce_w // 2, eye_y + ce_h // 2)],
              fill=(0, 160, 180), width=1)
    draw.line([(ce_x, eye_y - ce_h // 2), (ce_x - ce_w // 3, eye_y)],
              fill=(0, 140, 160), width=1)
    # PROCESSING symbol: three rotating dots (Cyan/Magenta alternating per script)
    dot_colors = [CRT_TEAL, (255, 45, 107), CRT_TEAL]
    dot_positions = [
        (ce_x - 3, eye_y - 4),
        (ce_x + 3, eye_y - 2),
        (ce_x - 1, eye_y + 3),
    ]
    for (dx, dy), dc in zip(dot_positions, dot_colors):
        draw.rectangle([dx, dy, dx + 2, dy + 2], fill=dc)

    # ── MOUTH: "ugh" shape — disgusted, NOT threatening ────────────────────
    # Flat grimace, corners pressed OUT not back
    # "Someone who opened the fridge and found something old"
    mouth_y = face_cy + face_size // 4
    mouth_w = face_size // 2
    # Flat horizontal grimace (not a snarl, not a roar)
    draw.line([(face_cx - mouth_w // 2, mouth_y), (face_cx + mouth_w // 2, mouth_y)],
              fill=(5, 5, 15), width=3)
    # Corners pressed OUT (slight outward flare, not curl)
    draw.line([(face_cx - mouth_w // 2 - 4, mouth_y - 2),
               (face_cx - mouth_w // 2, mouth_y)], fill=(5, 5, 15), width=2)
    draw.line([(face_cx + mouth_w // 2, mouth_y),
               (face_cx + mouth_w // 2 + 4, mouth_y - 2)], fill=(5, 5, 15), width=2)
    # Pixel teeth (HORIZONTAL, visible but mouth is FLAT not wide)
    # Small row of white squares at the grimace line
    for tx in range(face_cx - mouth_w // 2 + 4, face_cx + mouth_w // 2 - 4, 7):
        draw.rectangle([tx, mouth_y - 2, tx + 5, mouth_y + 1], fill=(220, 225, 220))
    # Tiny open mouth gap (open a sliver — "ugh" not silent)
    draw.rectangle([face_cx - mouth_w // 3, mouth_y, face_cx + mouth_w // 3, mouth_y + 4],
                   fill=(5, 5, 15))

    # ── HANDS pressing on glass (flat against screen surface) ─────────────
    # Left hand pressing (viewer's left)
    hnd_y = face_cy + face_size // 6
    draw.polygon([
        (face_cx - half + 5, hnd_y - 8),
        (face_cx - half + 20, hnd_y - 8),
        (face_cx - half + 22, hnd_y + 4),
        (face_cx - half + 3,  hnd_y + 4),
    ], fill=(0, 180, 200), outline=BYTE_OUTLINE, width=1)
    # Finger lines on hand
    for fi in range(face_cx - half + 8, face_cx - half + 20, 4):
        draw.line([(fi, hnd_y - 8), (fi, hnd_y + 4)], fill=(0, 150, 170), width=1)

    # Right hand
    draw.polygon([
        (face_cx + half - 20, hnd_y - 8),
        (face_cx + half - 5,  hnd_y - 8),
        (face_cx + half - 3,  hnd_y + 4),
        (face_cx + half - 22, hnd_y + 4),
    ], fill=(0, 180, 200), outline=BYTE_OUTLINE, width=1)
    for fi in range(face_cx + half - 17, face_cx + half - 6, 4):
        draw.line([(fi, hnd_y - 8), (fi, hnd_y + 4)], fill=(0, 150, 170), width=1)

    # ── SCREEN BULGE where face is pressing ───────────────────────────────
    # FIX: Increase bulge ring contrast — must be visible against dark screen background.
    # Use brighter cyan-tinted outlines with wider strokes so rings read clearly.
    for r in range(65, 20, -9):
        # Brightness ramps UP toward center — inner rings are hottest
        bulge_b = max(40, 120 - r)
        bulge_g = max(60, 160 - r)
        bulge_col = (bulge_b // 4, bulge_g, bulge_b + 20)  # cyan-tinted bright ring
        ring_w = 2 if r < 40 else 1
        draw.ellipse([face_cx - r, face_cy - r * 3 // 4,
                      face_cx + r, face_cy + r * 3 // 4],
                     outline=bulge_col, width=ring_w)

    # ── PIXEL CONFETTI starting to bleed from bulge point ─────────────────
    # First escape of pixels into the room — "feels like it's escaping"
    draw_pixel_confetti(draw, face_cx + half - 10, face_cy, 30, seed=6, count=8)
    draw_pixel_confetti(draw, face_cx, face_cy - half + 5, 25, seed=7, count=6)

    # Annotations
    draw.text((4, 4), "CU SCREEN — straight-on", fill=(150, 140, 120), font=font_ann)
    draw.text((4, 14), "BYTE: DISGUSTED/CURIOUS. NOT menacing.", fill=(200, 160, 40), font=font_ann)


# ── P08: Byte in the real world — Full reveal ─────────────────────────────────

def draw_p08_byte_real_world(draw, font, font_bold, font_ann):
    """P08: MED — Byte full body, in the real world for first time.
    Camera at HIS eye level (6 inches off floor). Pixel confetti drifting.
    Byte: floor-level. He looks down, up, down. Profound distaste.
    CRT monitor returning to normal static behind him (defocused).
    BRIDGE: establishes Byte's physical presence and scale in room."""

    # Room: warm dark floor-level view
    draw.rectangle([0, 0, PW, DRAW_H], fill=(22, 15, 10))

    # ── Floor plane (very close — camera AT floor level) ──────────────────
    floor_y = int(DRAW_H * 0.70)
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=(16, 11, 7))
    draw.line([(0, floor_y), (PW, floor_y)], fill=(32, 22, 14), width=1)

    # Floor texture: cable bundles at floor level
    rng_floor = random.Random(21)
    for _ in range(8):
        fx = rng_floor.randint(0, PW)
        fw = rng_floor.randint(15, 45)
        draw.line([(fx, floor_y + 3), (fx + fw, floor_y + 3)], fill=(28, 20, 14), width=3)
        draw.line([(fx, floor_y + 7), (fx + fw - 5, floor_y + 7)], fill=(24, 18, 12), width=2)

    # Thin cyan tint on nearest cables (Byte's digital nature bleaching the analogue)
    for cb_x in range(int(PW * 0.38), int(PW * 0.58), 12):
        draw.line([(cb_x, floor_y + 2), (cb_x + 8, floor_y + 2)], fill=(0, 35, 45), width=2)

    # ── DESATURATION RING at Byte's feet (digital nature bleaching analogue) ──
    byte_cx = PW // 2
    byte_cy = int(DRAW_H * 0.42)  # his center (hovering just above floor)

    # Thin desaturation ring (analogue world reacting)
    for r in range(28, 12, -4):
        grey_val = 22 + r
        draw.ellipse([byte_cx - r * 2, floor_y - 5, byte_cx + r * 2, floor_y + 2],
                     outline=(grey_val, grey_val - 2, grey_val - 4), width=1)

    # ── BACKGROUND: CRT monitor returning to static (defocused) ───────────
    # Monitor looms in background, slightly off-left, screen returning to normal
    mon_x, mon_y = int(PW * 0.05), int(DRAW_H * 0.06)
    mon_w, mon_h = 120, 80
    # Defocused monitor (soft blur approximated by slightly larger, muted edges)
    draw.rectangle([mon_x - 3, mon_y - 3, mon_x + mon_w + 3, mon_y + mon_h + 3],
                   fill=(40, 35, 28), outline=(55, 48, 36), width=2)
    draw.rectangle([mon_x + 8, mon_y + 8, mon_x + mon_w - 8, mon_y + mon_h - 8],
                   fill=(12, 10, 16))
    # Screen returning to static (rng texture, muted — not the sharp pixel anymore)
    rng_bg = random.Random(88)
    for _ in range(200):
        sx = rng_bg.randint(mon_x + 9, mon_x + mon_w - 9)
        sy = rng_bg.randint(mon_y + 9, mon_y + mon_h - 9)
        br = rng_bg.randint(14, 28)
        draw.point((sx, sy), fill=(br, br, br + 4))
    # Screen ripple (disturbed water — surface returning to flat after Byte's exit)
    for r in range(20, 5, -5):
        draw.ellipse([mon_x + mon_w // 2 - r, mon_y + mon_h // 2 - r // 2,
                      mon_x + mon_w // 2 + r, mon_y + mon_h // 2 + r // 2],
                     outline=(0, 40 + r * 4, 50 + r * 5), width=1)

    # Room walls/environment (background — warm dark)
    draw.rectangle([0, 0, PW, int(DRAW_H * 0.25)], fill=(18, 13, 9))  # ceiling suggestion
    # Cable bundles on wall
    for wx in [int(PW * 0.55), int(PW * 0.68), int(PW * 0.78)]:
        draw.line([(wx, int(DRAW_H * 0.08)), (wx, floor_y)], fill=(28, 22, 16), width=2)

    # ── BYTE — full body, floor level, profound distaste ──────────────────
    byte_size = 90  # FIX: was 42 — too small for a character introduction shot. 80-100px minimum.

    # Confetti still drifting from emergence (pixel snow)
    draw_pixel_confetti(draw, byte_cx - 25, byte_cy - 30, 45, seed=8, count=16)
    draw_pixel_confetti(draw, byte_cx + 20, byte_cy - 15, 35, seed=9, count=10)

    # Magenta/cyan trailing artifacts (floating upward from emergence)
    for i in range(5):
        art_x = byte_cx + (i - 2) * 12
        art_y = byte_cy - 40 - i * 5
        art_col = (255, 45, 107) if i % 2 == 0 else CRT_TEAL
        draw.rectangle([art_x, art_y, art_x + 3, art_y + 8], fill=art_col)

    # BYTE'S BODY with eye state: "assessment" (scan line — taking in the room)
    draw_byte_body(draw, byte_cx, byte_cy, byte_size, eye_state="scan", font_ann=font_ann)

    # Foot touching floor gesture (per script: touches floor, recoils, touches again)
    # Left foot touching down tentatively
    foot_y = floor_y - 2
    draw.ellipse([byte_cx - byte_size // 2 - 5, foot_y - 5,
                  byte_cx - byte_size // 4, foot_y + 3],
                 fill=BYTE_BODY, outline=BYTE_OUTLINE, width=1)
    # Small "recoil" motion line from foot
    draw.arc([byte_cx - byte_size // 2 - 8, foot_y - 10,
              byte_cx - byte_size // 4 + 2, foot_y - 2],
             start=200, end=340, fill=(0, 160, 180), width=1)

    # ── FINGER SNAP SPARKS (per script: snaps fingers, confirms something) ─
    snap_x = byte_cx + byte_size // 2 + 10
    snap_y = byte_cy - byte_size // 6
    draw.line([(snap_x, snap_y - 2), (snap_x + 8, snap_y - 8)], fill=CRT_TEAL, width=1)
    draw.line([(snap_x, snap_y - 2), (snap_x + 9, snap_y + 3)], fill=(255, 45, 107), width=1)
    draw.line([(snap_x, snap_y - 2), (snap_x - 6, snap_y - 7)], fill=(0, 200, 65), width=1)
    draw.ellipse([snap_x - 2, snap_y - 4, snap_x + 2, snap_y], fill=CRT_TEAL)

    # ── DIALOGUE BUBBLE (Byte's first words) ──────────────────────────────
    bubble_x = byte_cx + byte_size + 12
    bubble_y = byte_cy - byte_size // 2 - 24
    bubble_w, bubble_h = 120, 30
    draw.rectangle([bubble_x, bubble_y, bubble_x + bubble_w, bubble_y + bubble_h],
                   fill=(15, 10, 20), outline=CRT_TEAL, width=1)
    # Tail
    draw.polygon([
        (bubble_x + 8, bubble_y + bubble_h),
        (bubble_x + 18, bubble_y + bubble_h),
        (byte_cx + byte_size // 2, byte_cy - byte_size // 2),
    ], fill=(15, 10, 20), outline=CRT_TEAL, width=1)
    try:
        font_dlg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    except Exception:
        font_dlg = font_ann
    draw.text((bubble_x + 6, bubble_y + 4), '"Ugh."', fill=CRT_TEAL, font=font_dlg)
    draw.text((bubble_x + 6, bubble_y + 16), '"The flesh dimension."', fill=(200, 180, 140), font=font_dlg)

    # Annotations
    draw.text((4, 4), "MED — floor level (Byte's scale)", fill=(150, 140, 120), font=font_ann)
    draw.text((4, 14), "FIRST TIME IN REAL WORLD. Profound distaste.", fill=(130, 120, 100), font=font_ann)


# ── P09: Byte floats up, sees Luma ────────────────────────────────────────────

def draw_p09_byte_sees_luma(draw, font, font_bold, font_ann):
    """P09: MED WIDE — Byte floating 18" off ground, center-right.
    Luma visible on couch in background-left (still asleep, oblivious).
    Byte has spotted her. His cracked eye SCANS. Pixel readout flickers.
    He begins drifting toward her — digital micro-increment movement.
    BRIDGE: establishes their relative positions in room space."""

    # Room: warm dark den
    draw.rectangle([0, 0, PW, DRAW_H], fill=(22, 15, 10))

    # ── Room 3D geometry (spatial contract for P10 and P11) ───────────────
    # Floor
    floor_y = int(DRAW_H * 0.76)
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=(16, 11, 7))
    draw.line([(0, floor_y), (PW, floor_y)], fill=(32, 22, 14), width=1)

    # Back wall
    back_wall_y = int(DRAW_H * 0.18)
    draw.rectangle([0, back_wall_y, PW, floor_y], fill=(28, 20, 13))
    draw.line([(0, back_wall_y), (PW, back_wall_y)], fill=(42, 30, 18), width=1)

    # ── LUMA on COUCH (left background — still asleep, oblivious) ─────────
    # Couch in background-left
    c_x = int(PW * 0.04)
    c_y = int(DRAW_H * 0.44)
    c_w = int(PW * 0.42)
    c_h = int(DRAW_H * 0.30)

    # Couch body (terracotta)
    draw.rectangle([c_x, c_y, c_x + c_w, floor_y - 2], fill=(100, 58, 35))
    draw.rectangle([c_x, c_y - 14, c_x + c_w, c_y + 4], fill=(115, 65, 38), outline=(85, 48, 28), width=1)

    # LUMA — sleeping (warm blurry, slightly smaller — she's in the background)
    luma_cx = int(c_x + c_w * 0.38)
    luma_cy = int(c_y + c_h * 0.20)

    # Hair cloud (iconic — even from here it reads)
    draw.ellipse([luma_cx - 22, luma_cy - 30, luma_cx + 22, luma_cy + 8], fill=LUMA_HAIR)
    draw.ellipse([luma_cx - 14, luma_cy - 38, luma_cx + 8, luma_cy - 20], fill=LUMA_HAIR)
    # Back of head / warm skin
    draw.ellipse([luma_cx - 8, luma_cy - 4, luma_cx + 12, luma_cy + 12], fill=LUMA_SKIN)

    # Sideways body (PJ mint tone)
    draw.rectangle([c_x + 10, c_y + 5, c_x + c_w - 10, c_y + 18], fill=(180, 210, 195))

    # Dangling leg off couch
    draw.line([(c_x + c_w - 25, c_y + 14), (c_x + c_w - 20, floor_y + 2)],
              fill=LUMA_SKIN, width=6)

    # Thrown-over-back leg
    draw.line([(c_x + c_w - 36, c_y + 8), (c_x + c_w - 26, c_y - 16)],
              fill=LUMA_SKIN, width=6)

    # NEON CRUNCH bag (visible even in background — orange blob)
    draw.rectangle([c_x + c_w // 2, c_y + 3, c_x + c_w // 2 + 24, c_y + 18],
                   fill=(230, 120, 20))

    # Notebook on lap
    draw.rectangle([c_x + c_w // 4, c_y + 4, c_x + c_w // 4 + 28, c_y + 20],
                   fill=(225, 215, 195), outline=(160, 148, 125), width=1)

    # Monitor back wall (background texture)
    for m_bx, m_by, m_bw, m_bh in [(220, back_wall_y + 6, 65, 40), (310, back_wall_y + 8, 55, 36)]:
        draw.rectangle([m_bx, m_by, m_bx + m_bw, m_by + m_bh], fill=(15, 12, 20), outline=(35, 28, 45), width=1)
        draw.rectangle([m_bx + 4, m_by + 4, m_bx + m_bw - 4, m_by + m_bh - 4], fill=(10, 8, 14))

    # ── CABLE BUNDLES on floor (between Byte and Luma) ────────────────────
    # These are the obstacles Byte is floating over
    for cb_x in range(int(PW * 0.35), int(PW * 0.60), 18):
        draw.line([(cb_x, floor_y - 1), (cb_x + 12, floor_y - 1)], fill=(28, 20, 14), width=4)
        draw.line([(cb_x + 3, floor_y - 4), (cb_x + 15, floor_y - 4)], fill=(24, 18, 12), width=3)

    # ── BYTE — center-right, floating 18" off ground ──────────────────────
    # Camera is at Byte's elevation (18" from floor)
    byte_cx = int(PW * 0.68)
    # 18" off floor in frame space: floor_y is at bottom, so 18" = ~1/3 of DRAW_H above floor
    byte_cy = floor_y - int(DRAW_H * 0.30)
    byte_size = 36

    # His floating is digital: micro-increment, slight hover vibration
    # Show as small motion lines (horizontal, short) — digital stutter
    for stutter_i in range(3):
        sx_off = -8 + stutter_i * 4
        draw.rectangle([byte_cx + sx_off - byte_size // 2,
                        byte_cy - byte_size // 2 - 2,
                        byte_cx + sx_off + byte_size // 2,
                        byte_cy + byte_size // 2 + 2],
                       outline=(0, 80, 100), width=1)

    # Pixel confetti trail (left behind as he floated from the monitor)
    draw_pixel_confetti(draw, byte_cx - 30, byte_cy + 5, 20, seed=11, count=8)
    draw_pixel_confetti(draw, int(PW * 0.50), byte_cy + 8, 15, seed=12, count=5)
    # Trail direction: left → right (from monitor toward Luma)
    for trl in range(4):
        trl_x = int(PW * 0.48) + trl * 18
        draw.rectangle([trl_x, byte_cy - 2, trl_x + 4, byte_cy + 2], outline=(0, 80, 100), width=1)

    # BYTE (eye state: scan — he has found Luma and is actively scanning her)
    draw_byte_body(draw, byte_cx, byte_cy, byte_size, eye_state="scan", font_ann=font_ann)

    # Hover glow below him (larger at this height — more dramatic)
    draw.ellipse([byte_cx - 30, byte_cy + byte_size // 2 + 2,
                  byte_cx + 30, byte_cy + byte_size // 2 + 12],
                 fill=(0, 35, 50))

    # One twitching leg (per script: "one leg is twitching — trying to look controlled")
    twitch_x = byte_cx + byte_size // 4
    twitch_y = byte_cy + byte_size // 2
    draw.line([(twitch_x, twitch_y), (twitch_x + 4, twitch_y + 8)],
              fill=BYTE_BODY, width=3)
    draw.arc([twitch_x - 2, twitch_y + 4, twitch_x + 8, twitch_y + 12],
             start=180, end=360, fill=(0, 160, 180), width=1)

    # ── PIXEL READOUT flicker near Byte's vision ──────────────────────────
    # Per script: "two or three lines of glitch text that flash and disappear"
    readout_x = byte_cx - byte_size // 2 - 55
    readout_y = byte_cy - 18
    try:
        font_glitch = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 7)
    except Exception:
        font_glitch = font_ann
    draw.text((readout_x, readout_y),      "SCAN: organic unit", fill=(0, 160, 180), font=font_glitch)
    draw.text((readout_x, readout_y + 9),  "STATUS: dormant",    fill=(0, 140, 160), font=font_glitch)
    draw.text((readout_x, readout_y + 18), "THREAT: low (prob)", fill=(80, 140, 100), font=font_glitch)
    # Bracket the readout (HUD style)
    draw.rectangle([readout_x - 2, readout_y - 2, readout_x + 100, readout_y + 26],
                   outline=(0, 100, 120), width=1)

    # Gaze direction arrow (from Byte to Luma — compositional guide)
    draw.line([(byte_cx - byte_size // 2 - 5, byte_cy - 5),
               (luma_cx + 20, luma_cy)], fill=(0, 80, 100), width=1)

    # Annotations
    draw.text((4, 4), "MED WIDE — Byte 18\" off floor", fill=(150, 140, 120), font=font_ann)
    draw.text((4, 14), "Byte spots Luma. Digital scan. Drift begins.", fill=(130, 120, 100), font=font_ann)


# ── P10: OTS — Byte looking at Luma's sleeping face ──────────────────────────

def draw_p10_ots_byte_luma(draw, font, font_bold, font_ann):
    """P10: OTS (Over The Shoulder) — Byte's POV looking at Luma's sleeping face.
    Camera: 18" from floor, horizontal eyeline. Looking from monitor-wall toward couch.
    Byte: dark angular silhouette, lower-left quadrant (20% of frame width).
    Luma's sleeping face: center-right, in focus, warm and close.
    THEMATIC CORE: angular cold silhouette framing warm rounded face.
    Cyan glow from Byte lights Luma's cheek — FIRST CONTACT of digital and real."""

    # Room ambient — warm dark
    draw.rectangle([0, 0, PW, DRAW_H], fill=(30, 22, 14))

    # ── BACKGROUND (soft focus — warm amber den, blurry back wall) ────────
    # Couch back (behind Luma's head — in soft focus)
    couch_back_y = int(DRAW_H * 0.38)
    couch_back_w = int(PW * 0.72)
    draw.rectangle([int(PW * 0.18), couch_back_y, PW, int(DRAW_H * 0.62)],
                   fill=(88, 52, 32))
    # Worn fabric detail (slightly stained terracotta — per script)
    for stn_x in range(int(PW * 0.30), PW - 10, 22):
        rng_stn = random.Random(stn_x)
        if rng_stn.random() > 0.5:
            draw.ellipse([stn_x, couch_back_y + 4, stn_x + 8, couch_back_y + 10],
                         fill=(80, 46, 28))

    # Extreme soft focus monitor glow on back wall (very distant, blurry warm amber)
    for r in range(50, 10, -12):
        draw.ellipse([PW - 80 - r * 2, couch_back_y - r, PW - 40 + r * 2, couch_back_y + r * 2],
                     outline=(55, 42, 22), width=2)

    # ── LUMA'S SLEEPING FACE — center-right, IN FOCUS ─────────────────────
    # She is ~ 8-5 inches from Byte. Face slightly smooshed against cushion.
    face_cx = int(PW * 0.62)
    face_cy = int(DRAW_H * 0.44)

    # Face base (warm skin, slightly smooshed — one cheek against couch)
    # Face is slightly squashed on the cushion side (right side slightly flattened)
    draw.ellipse([face_cx - 42, face_cy - 36, face_cx + 36, face_cy + 38], fill=LUMA_SKIN)
    draw.ellipse([face_cx - 42, face_cy - 36, face_cx + 36, face_cy + 38],
                 outline=(170, 108, 65), width=1)

    # Hair (dark mass, fills frame above and around her head)
    # Upper frame periphery — massive cloud of hair
    draw.ellipse([face_cx - 68, face_cy - 60, face_cx + 50, face_cy + 12], fill=LUMA_HAIR)
    draw.ellipse([face_cx - 55, face_cy - 75, face_cx + 40, face_cy - 35], fill=LUMA_HAIR)
    # Hair also fills right frame edge
    draw.ellipse([face_cx + 20, face_cy - 50, face_cx + 55, face_cy + 20], fill=LUMA_HAIR)

    # CLOSED EYELIDS (fully relaxed — deep sleep, per script: no tension lines)
    # Luma looking slightly sideways (face turned into cushion)
    l_eye_x = face_cx - 14
    r_eye_x = face_cx + 8
    eye_y    = face_cy - 6
    # Eyelashes (simple graphic arcs, thick and bold per script)
    draw.arc([l_eye_x - 14, eye_y - 6, l_eye_x + 4, eye_y + 4], start=200, end=340, fill=(25, 15, 10), width=4)
    draw.arc([r_eye_x - 10, eye_y - 6, r_eye_x + 8, eye_y + 4], start=200, end=340, fill=(25, 15, 10), width=4)
    # Eyebrow (FULLY RELAXED — no tension — she is in last moment of genuine rest)
    draw.arc([l_eye_x - 18, eye_y - 18, l_eye_x + 4, eye_y - 6], start=200, end=340, fill=(25, 15, 10), width=3)
    draw.arc([r_eye_x - 12, eye_y - 18, r_eye_x + 8, eye_y - 6], start=200, end=340, fill=(25, 15, 10), width=3)

    # Slightly open mouth (one corner resting on cushion — smooshed)
    mouth_cx = face_cx - 2
    mouth_y  = face_cy + 18
    draw.arc([mouth_cx - 10, mouth_y - 4, mouth_cx + 8, mouth_y + 6],
             start=10, end=170, fill=(155, 90, 55), width=2)
    # Smoosh effect — right side of mouth slightly flattened
    draw.line([(mouth_cx + 6, mouth_y + 1), (mouth_cx + 12, mouth_y)],
              fill=(160, 95, 60), width=1)

    # NEON CRUNCH orange chip crumb on her left cheek (per script — Byte is staring at it)
    chip_x = face_cx - 24
    chip_y = face_cy + 8
    draw.ellipse([chip_x, chip_y, chip_x + 6, chip_y + 4], fill=(240, 160, 50))

    # ── CYAN GLOW from Byte touching Luma's cheek ─────────────────────────
    # FIRST MOMENT the Digital World literally touches the Real World character
    # Left cheek closest to Byte — the cyan glow falls here.
    # FIX: Use bright semi-transparent cyan (SCREEN/Add logic) — glow adds light, not darkness.
    # PIL has no blending modes, so we draw LIGHT-COLORED semi-transparent ellipses
    # over the skin using a composite approach: draw glow image, then paste with alpha.
    glow_x = face_cx - 32
    glow_y = face_cy + 2
    # Build glow as a separate RGBA layer (full panel size) and composite over skin
    base_img = draw._image  # the PIL Image object
    glow_layer = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    # Outer rings: bright cyan, very low opacity — they ADD light to cheek
    for r, alpha in [(42, 35), (32, 55), (22, 80), (14, 110), (8, 140)]:
        bright_cyan = (80, 255, 255, alpha)
        glow_draw.ellipse([glow_x - r, glow_y - r, glow_x + r, glow_y + r],
                          fill=bright_cyan)
    # Hot center spot
    glow_draw.ellipse([glow_x - 5, glow_y - 5, glow_x + 5, glow_y + 5],
                      fill=(200, 255, 255, 180))
    # Composite: convert existing base to RGBA, alpha_composite, paste back as RGB
    base_rgba = base_img.convert('RGBA')
    base_rgba = Image.alpha_composite(base_rgba, glow_layer)
    # Paste result back onto the base image in-place
    base_img.paste(base_rgba.convert('RGB'), (0, 0))
    # Pixel confetti between them (digital snowfall — per script)
    draw_pixel_confetti(draw, face_cx - 55, face_cy - 10, 30, seed=14, count=10)

    # ── BYTE SILHOUETTE — lower-left quadrant (dark, angular, foreground) ─
    # Per spec: Byte's back-of-head + left upper body, lower-left quadrant
    # ~20% of frame width = 96px at 480px canvas. Must read as a solid OTS anchor.
    sil_cx = int(PW * 0.15)
    sil_cy = int(DRAW_H * 0.60)  # slightly below center-left (he's at 18" level, couch is 24-30")
    sil_size = 96  # FIX: was 44px — too small to anchor the OTS. Now ~20% of frame width.

    # Silhouette: dark cool-palette shape (he reads as INTRUDER shape vs warm rounded face)
    sil_half = sil_size // 2
    sil_c = max(3, sil_size // 8)

    sil_pts = [
        (sil_cx - sil_half + sil_c, sil_cy - sil_half),
        (sil_cx + sil_half - sil_c, sil_cy - sil_half),
        (sil_cx + sil_half,         sil_cy - sil_half + sil_c),
        (sil_cx + sil_half,         sil_cy + sil_half - sil_c),
        (sil_cx + sil_half - sil_c, sil_cy + sil_half),
        (sil_cx - sil_half + sil_c, sil_cy + sil_half),
        (sil_cx - sil_half,         sil_cy + sil_half - sil_c),
        (sil_cx - sil_half,         sil_cy - sil_half + sil_c),
    ]
    # Silhouette fill — very dark, slight cool tint (he's the cool-palette intruder)
    draw.polygon(sil_pts, fill=(8, 18, 22), outline=(0, 60, 80), width=2)

    # Slight cyan edge-lighting on Byte's outline (his own emission)
    # Right edge closest to Luma: stronger glow
    draw.line([(sil_cx + sil_half - sil_c, sil_cy - sil_half),
               (sil_cx + sil_half, sil_cy - sil_half + sil_c)],
              fill=(0, 100, 130), width=2)
    draw.line([(sil_cx + sil_half, sil_cy - sil_half + sil_c),
               (sil_cx + sil_half, sil_cy + sil_half - sil_c)],
              fill=(0, 120, 150), width=2)
    draw.line([(sil_cx + sil_half, sil_cy + sil_half - sil_c),
               (sil_cx + sil_half - sil_c, sil_cy + sil_half)],
              fill=(0, 100, 130), width=2)

    # Triangular spike at top of his head (Byte's signature detail)
    spike_tip_y = sil_cy - sil_half - 14
    draw.polygon([
        (sil_cx - 6, sil_cy - sil_half),
        (sil_cx + 6, sil_cy - sil_half),
        (sil_cx, spike_tip_y),
    ], fill=(6, 15, 20), outline=(0, 60, 80), width=1)

    # Left upper limb stub (per spec: left shoulder is OTS anchor)
    draw.rectangle([sil_cx - sil_half - 12, sil_cy - 4,
                    sil_cx - sil_half, sil_cy + 3],
                   fill=(8, 18, 22), outline=(0, 50, 70), width=1)

    # Body leaning slightly FORWARD (tilted toward Luma — curious, not threatening)
    # The silhouette subtly tilts clockwise

    # ── CRACKED EYE PIXEL: SEARCHING/PROCESSING symbol visible ──────────
    # Even in silhouette, the cracked eye's display is visible as cyan pixels
    eye_sil_x = sil_cx + sil_half // 4
    eye_sil_y = sil_cy - sil_half // 4
    # Processing dots glowing through the silhouette
    for di, (dx, dy) in enumerate([(-3, -2), (0, 2), (3, -1)]):
        dot_col = CRT_TEAL if di != 1 else (255, 45, 107)
        draw.rectangle([eye_sil_x + dx, eye_sil_y + dy,
                        eye_sil_x + dx + 2, eye_sil_y + dy + 2],
                       fill=dot_col)

    # ── Pixel confetti between them (digital snowfall) ─────────────────────
    # Already drawn above, adding a few more closer to Byte
    draw_pixel_confetti(draw, (sil_cx + face_cx) // 2 - 10, (sil_cy + face_cy) // 2,
                        18, seed=15, count=6)

    # Annotations
    draw.text((4, 4), "OTS — Byte's shoulder, 18\" level", fill=(150, 140, 120), font=font_ann)
    draw.text((4, 14), "CYAN LIGHT: Digital touches Real. Tender.", fill=(0, 140, 160), font=font_ann)


# ── Main generation ────────────────────────────────────────────────────────────

def generate_all():
    os.makedirs(OUT_DIR, exist_ok=True)

    panels = [
        (2,  "WIDE EXT",  "Eye-level exterior. MIRI mailbox. Warm/cool teal fight at curtain edges.",
         draw_p02_exterior_close,  "panel_p02_exterior_close.png"),
        (4,  "WIDE INT",  "Tech den. Luma asleep on couch — body gave up mid-activity. 2px now.",
         draw_p04_interior_wide,   "panel_p04_interior_wide.png"),
        (5,  "MCU MON",   "Inside the shelf. 8-12 cyan pixels clustered. We are on monitor's side.",
         draw_p05_monitor_mcu,     "panel_p05_monitor_mcu.png"),
        (6,  "CU SCREEN", "FIRST BYTE. Disgusted/curious face pressed on glass. Pixel confetti bleeding.",
         draw_p06_byte_emerging,   "panel_p06_byte_emerging.png"),
        (8,  "MED LOW",   "[BRIDGE] Byte in real world. Floor level. Profound distaste. Flesh dimension.",
         draw_p08_byte_real_world, "panel_p08_byte_real_world.png"),
        (9,  "MED WIDE",  "[BRIDGE] Byte floats 18\". Spots Luma. Digital scan. Begins drift toward her.",
         draw_p09_byte_sees_luma,  "panel_p09_byte_sees_luma.png"),
        (10, "OTS",       "[BRIDGE] Byte's shoulder. Luma asleep close. Cyan light on cheek. Intimate.",
         draw_p10_ots_byte_luma,   "panel_p10_ots_byte_luma.png"),
    ]

    images = {}
    for num, shot, caption, draw_fn, filename in panels:
        img = make_panel(num, shot, caption, draw_fn, filename)
        images[num] = img

    print(f"\nAll {len(panels)} interior/escalation panels generated.")
    return images


if __name__ == '__main__':
    generate_all()
