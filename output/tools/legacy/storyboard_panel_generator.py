# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
Storyboard Panel Generator — Luma & the Glitchkin
Creates 480x270px storyboard panels with caption bars.
Cycle 5 update: P03 fixed (pulse visible), P07/P12 bridging panels added,
P13 fully redrawn with 3D spatial staging.
"""
from PIL import Image, ImageDraw, ImageFont
import math

PW, PH = 480, 270
CAPTION_H = 48
DRAW_H = PH - CAPTION_H
BORDER = 2
BG_DRAW = (242, 240, 235)
BG_CAPTION = (25, 20, 18)
BORDER_COL = (20, 15, 12)
TEXT_CAPTION = (235, 228, 210)
TEXT_PANEL = (20, 15, 12)

def make_panel(panel_num, shot_type, caption, draw_fn, output_path):
    img = Image.new('RGB', (PW, PH), BG_DRAW)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
        font_caption = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except:
        font = font_bold = font_caption = ImageFont.load_default()

    # Drawing area background
    draw.rectangle([0, 0, PW, DRAW_H], fill=BG_DRAW)

    # Draw the scene content
    draw_fn(draw, font, font_bold)

    # Caption bar
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.text((8, DRAW_H + 6), caption[:72], fill=TEXT_CAPTION, font=font_caption)

    # Border
    draw.rectangle([0, 0, PW-1, PH-1], outline=BORDER_COL, width=BORDER)

    # Panel number (top left)
    draw.rectangle([0, 0, 40, 20], fill=(20,15,12))
    draw.text((4, 3), f"P{panel_num}", fill=(235,228,210), font=font_bold)

    # Shot type (top right)
    sw = 80
    draw.rectangle([PW-sw, 0, PW, 20], fill=(20,15,12))
    draw.text((PW-sw+4, 3), shot_type, fill=(235,228,210), font=font_bold)

    img.save(output_path)
    print(f"Saved: {output_path}")
    return img

# ── Panel drawing functions ───────────────────────────────────────────────────

def draw_p01_exterior(draw, font, font_bold):
    # Night sky
    draw.rectangle([0, 0, PW, DRAW_H], fill=(18, 22, 35))
    # Stars (small dots)
    import random; random.seed(42)
    for _ in range(40):
        sx, sy = random.randint(10, PW-10), random.randint(5, int(DRAW_H*0.55))
        draw.ellipse([sx-1, sy-1, sx+1, sy+1], fill=(220, 215, 200))
    # Ground
    draw.rectangle([0, int(DRAW_H*0.72), PW, DRAW_H], fill=(25, 20, 15))
    # House silhouette
    hx, hy = 160, int(DRAW_H*0.38)
    hw, hh = 160, int(DRAW_H*0.35)
    draw.rectangle([hx, hy+int(hh*0.35), hx+hw, hy+hh], fill=(15, 12, 10))
    # Roof (triangle)
    draw.polygon([(hx-10, hy+int(hh*0.35)), (hx+hw+10, hy+int(hh*0.35)), (hx+hw//2, hy)], fill=(10, 8, 7))
    # Glowing window
    draw.rectangle([hx+hw//2-18, hy+int(hh*0.45), hx+hw//2+18, hy+int(hh*0.72)], fill=(0, 200, 220))
    draw.rectangle([hx+hw//2-16, hy+int(hh*0.47), hx+hw//2+16, hy+int(hh*0.70)], fill=(0, 240, 255))
    # Glow halo around window
    for r in range(12, 3, -3):
        gx, gy = hx+hw//2, hy+int(hh*0.585)
        draw.ellipse([gx-r*2, gy-r, gx+r*2, gy+r], outline=(0, 240, 200), width=1)
    # LUMA'S HOUSE DISTINCTIVE DETAIL: antenna cluster on roof
    ax = hx + hw//2
    roof_peak = hy
    # Main antenna
    draw.line([(ax, roof_peak), (ax, roof_peak-28)], fill=(30,25,20), width=2)
    draw.line([(ax-12, roof_peak-20), (ax+12, roof_peak-20)], fill=(30,25,20), width=2)
    # Side antenna
    draw.line([(ax+15, roof_peak-4), (ax+15, roof_peak-20)], fill=(30,25,20), width=2)
    draw.line([(ax+8, roof_peak-16), (ax+22, roof_peak-16)], fill=(30,25,20), width=2)
    # Tiny blinking light on antenna
    draw.ellipse([ax-2, roof_peak-31, ax+2, roof_peak-27], fill=(255, 45, 107))
    # Power lines (thin, not severing composition)
    draw.line([(0, int(DRAW_H*0.30)), (60, int(DRAW_H*0.28))], fill=(40,35,28), width=1)
    draw.line([(370, int(DRAW_H*0.32)), (PW, int(DRAW_H*0.30))], fill=(40,35,28), width=1)
    draw.line([(60, int(DRAW_H*0.28)), (ax+15, roof_peak-4)], fill=(40,35,28), width=1)

def draw_p03_pixel(draw, font, font_bold):
    """P03 FIX: pixel moved to lower-center (compositional anchor, not exit).
    Pulse is now VISIBLE — concentric glow rings show the pulse in the image."""
    # Monitor environment — dark void
    draw.rectangle([0, 0, PW, DRAW_H], fill=(12, 11, 18))
    # Monitor bezel
    draw.rectangle([50, 15, PW-50, DRAW_H-15], fill=(6, 5, 10))
    draw.rectangle([52, 17, PW-52, DRAW_H-17], outline=(30,25,40), width=1)
    # Monitor screen (slightly lighter dark)
    draw.rectangle([54, 18, PW-54, DRAW_H-18], fill=(10, 8, 15))
    # Static suggestion (subtle scanlines)
    for y in range(18, DRAW_H-18, 4):
        draw.line([(54, y), (PW-54, y)], fill=(14, 12, 20), width=1)

    # THE pixel — LOWER-CENTER, compositional anchor (eye rests here, not exits)
    px = PW // 2 - 4         # horizontally centered
    py = int(DRAW_H * 0.62)  # lower-center: eye gravity pulls down

    # PULSE VISUALIZED: concentric glow rings (not in caption, in IMAGE)
    # Outer pulse rings — larger, dimmer
    for r, alpha in [(32, 18), (22, 35), (14, 60), (8, 100)]:
        ring_color = (0, max(80, 240 - r*3), max(100, 255 - r*2))
        draw.ellipse([px-r, py-r, px+r+8, py+r+8], outline=ring_color, width=1)
    # Inner bloom
    draw.ellipse([px-4, py-4, px+12, py+12], fill=(0, 180, 200))
    # The pixel itself — 8×8, crisp, electric cyan
    draw.rectangle([px, py, px+8, py+8], fill=(0, 240, 255))
    # Pixel hot center
    draw.rectangle([px+2, py+2, px+6, py+6], fill=(180, 255, 255))

    # Annotation arrow pointing at pixel (storyboard convention)
    arrow_x, arrow_y = px - 30, py - 28
    draw.line([(arrow_x, arrow_y), (px-2, py-2)], fill=(200, 190, 160), width=1)
    draw.ellipse([arrow_x-3, arrow_y-3, arrow_x+3, arrow_y+3], fill=(200,190,160))
    try:
        font_ann = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    except:
        font_ann = font
    draw.text((arrow_x - 24, arrow_y - 14), "PULSE", fill=(180,170,140), font=font_ann)

def draw_p07_approach(draw, font, font_bold):
    """BRIDGE PANEL P07: Byte drifting across floor toward sleeping Luma.
    Low angle, establishes room scale and Byte's ground-level approach."""
    # Room: warm dark bedroom, monitor glow from off-left
    draw.rectangle([0, 0, PW, DRAW_H], fill=(28, 20, 14))
    # Floor plane (perspective line) — establishes 3D space
    floor_y = int(DRAW_H * 0.72)
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=(20, 15, 10))
    draw.line([(0, floor_y), (PW, floor_y)], fill=(40, 30, 20), width=1)
    # Monitor glow from left wall (off-screen source)
    for i in range(6):
        lx = i * 18
        intensity = max(0, 60 - i*10)
        draw.line([(lx, 0), (lx, DRAW_H)], fill=(0, intensity, intensity+20), width=12)

    # Luma asleep (right side) — seen from low angle across room
    # Just her feet/lower body on bed, suggesting the bed off-right
    bed_x = int(PW * 0.68)
    bed_y = int(DRAW_H * 0.48)
    # Bed edge (foreshortened)
    draw.rectangle([bed_x, bed_y, PW, floor_y-2], fill=(55, 38, 28))
    draw.line([(bed_x, bed_y), (PW, bed_y)], fill=(70,50,35), width=2)
    # Luma's feet/legs visible hanging off bed edge
    draw.ellipse([bed_x+10, bed_y+5, bed_x+40, bed_y+22], fill=(200,136,90))  # foot
    draw.ellipse([bed_x+50, bed_y+8, bed_x+78, bed_y+24], fill=(200,136,90))  # foot
    # Blanket suggestion
    draw.arc([bed_x+5, bed_y-8, bed_x+90, bed_y+20], start=0, end=180, fill=(85,58,42), width=3)

    # BYTE — small, floating low, approaching from left
    bx = int(PW * 0.28)
    by = int(floor_y * 0.72)  # floating just above floor level
    bs = 24
    # Hover glow below Byte
    draw.ellipse([bx-20, by+bs//2+2, bx+20, by+bs//2+10], fill=(0, 60, 80))
    # Byte body
    c = bs//8
    body_pts = [
        (bx-bs//2+c, by-bs//2), (bx+bs//2-c, by-bs//2),
        (bx+bs//2, by-bs//2+c), (bx+bs//2, by+bs//2-c),
        (bx+bs//2-c, by+bs//2), (bx-bs//2+c, by+bs//2),
        (bx-bs//2, by+bs//2-c), (bx-bs//2, by-bs//2+c),
    ]
    draw.polygon(body_pts, fill=(0, 212, 232), outline=(10,10,20), width=2)
    # Pixel eye (loading symbol - curious/searching)
    draw.rectangle([bx-7, by-4, bx+2, by+5], fill=(255,255,255), outline=(10,10,20), width=1)
    for dot_x, dot_y in [(bx-6, by-3), (bx-3, by+2), (bx, by-3)]:
        draw.rectangle([dot_x, dot_y, dot_x+1, dot_y+1], fill=(0,240,255))
    # Motion trail (Byte moving right)
    for t in range(1, 4):
        tx = bx - t * 14
        draw.rectangle([tx-bs//3, by-bs//3, tx+bs//3, by+bs//3],
                       outline=(0, 212-t*25, 232-t*25), width=1)

    # Camera angle annotation
    try:
        font_ann = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    except:
        font_ann = font
    draw.text((4, 4), "LOW ANGLE — floor level", fill=(150,140,120), font=font_ann)

def draw_p11_nose_to_nose(draw, font, font_bold):
    draw.rectangle([0, 0, PW, DRAW_H], fill=(40, 28, 18))
    # Soft monitor glow background
    for r in range(60, 10, -10):
        draw.ellipse([PW//2-r*3, DRAW_H//2-r*2, PW//2+r*3, DRAW_H//2+r*2],
                     outline=(0, 120, 140), width=1)

    # Luma head (left, round, large)
    lx, ly = PW//2 - 35, DRAW_H//2 - 30
    draw.ellipse([lx-38, ly-38, lx+38, ly+38], fill=(200, 136, 90))
    draw.ellipse([lx-38, ly-38, lx+38, ly+38], outline=(50,30,15), width=2)
    # Hair blob
    draw.ellipse([lx-52, ly-60, lx+52, ly+10], fill=(25, 15, 10))
    # Eyes (wide open)
    draw.ellipse([lx-18, ly-8, lx-4, ly+8], fill=(255,255,255))
    draw.ellipse([lx+4, ly-8, lx+18, ly+8], fill=(255,255,255))
    draw.ellipse([lx-14, ly-5, lx-7, ly+5], fill=(20,12,8))
    draw.ellipse([lx+7, ly-5, lx+14, ly+5], fill=(20,12,8))
    # "OH NO" MICRO-EXPRESSION: raised inner brows (eyebrow raise)
    draw.arc([lx-22, ly-32, lx-2, ly-18], start=200, end=340, fill=(25,15,10), width=4)
    draw.arc([lx+2, ly-32, lx+22, ly-18], start=200, end=340, fill=(25,15,10), width=4)
    # Inner brow crease (the "oh no" forehead line)
    draw.arc([lx-10, ly-38, lx+10, ly-26], start=200, end=340, fill=(168,104,56), width=2)

    # Byte (right, small geometric)
    bx, by = PW//2 + 35, DRAW_H//2 - 10
    bs = 28
    draw.rectangle([bx-bs//2, by-bs//2, bx+bs//2, by+bs//2], fill=(0,212,232))
    draw.rectangle([bx-bs//2, by-bs//2, bx+bs//2, by+bs//2], outline=(0,150,180), width=2)
    # Byte pixel eye (! symbol — alarmed)
    draw.rectangle([bx-10, by-6, bx-2, by+6], fill=(255,255,255), outline=(0,100,120), width=1)
    for dot_y in [by-5, by-2, by+1]:
        draw.rectangle([bx-7, dot_y, bx-5, dot_y+1], fill=(0,240,255))
    draw.rectangle([bx-7, by+3, bx-5, by+5], fill=(0,240,255))

    # Gap / breath between them
    draw.line([(PW//2-2, DRAW_H//2-40), (PW//2-2, DRAW_H//2+40)], fill=(200,180,120), width=1)

def draw_p12_recoil(draw, font, font_bold):
    """BRIDGE PANEL P12: Initial recoil — the moment BEFORE the full scream.
    Establishes room geometry for P13. Luma rearing back, Byte frozen.
    Camera: MED. Room visible. Bed behind Luma. Monitors on back wall."""
    # Room — warm amber-dark bedroom
    draw.rectangle([0, 0, PW, DRAW_H], fill=(25, 18, 12))

    # BACK WALL (establishes room depth)
    back_wall_y = int(DRAW_H * 0.25)
    draw.rectangle([0, back_wall_y, PW, int(DRAW_H * 0.72)], fill=(30, 22, 15))
    draw.line([(0, back_wall_y), (PW, back_wall_y)], fill=(45,32,20), width=1)

    # MONITORS ON BACK WALL (3 monitors, dark/inactive, establishing their location)
    for i, (mx, mw, mh) in enumerate([(55,90,55), (195,100,60), (330,85,52)]):
        my = back_wall_y + 8
        draw.rectangle([mx, my, mx+mw, my+mh], fill=(15,12,20), outline=(35,28,45), width=2)
        draw.rectangle([mx+3, my+3, mx+mw-3, my+mh-3], fill=(10,8,15))
        # Slight flicker — monitors starting to react
        flicker = (0, 30+i*15, 40+i*15)
        draw.rectangle([mx+4, my+4, mx+mw-4, my+mh-4], fill=flicker)

    # FLOOR
    floor_y = int(DRAW_H * 0.72)
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=(18, 13, 8))
    draw.line([(0, floor_y), (PW, floor_y)], fill=(38,28,18), width=1)

    # BED (behind/right of Luma — she's just stood up from it)
    bed_right = int(PW * 0.82)
    draw.rectangle([bed_right-80, int(DRAW_H*0.55), bed_right, floor_y], fill=(55,38,28))
    draw.rectangle([bed_right-80, int(DRAW_H*0.50), bed_right, int(DRAW_H*0.57)], fill=(70,50,35))  # headboard

    # LUMA — left of center, mid-recoil: torso jerking back, arms rising
    lx = int(PW * 0.38)
    # Floor shadow
    draw.ellipse([lx-30, floor_y-6, lx+30, floor_y+4], fill=(12,8,5))
    # Body (facing right, recoiling left-back)
    body_top = int(DRAW_H * 0.28)
    body_bot = floor_y - 2
    # Torso leaning back
    draw.polygon([(lx-16, body_top+30), (lx+12, body_top+30),
                  (lx+18, body_bot-30), (lx-22, body_bot-30)], fill=(232,114,42))
    # Head (tilted back in recoil)
    hx, hy = lx+4, body_top+8
    draw.ellipse([hx-24, hy-24, hx+24, hy+24], fill=(200,136,90), outline=(50,30,15), width=2)
    # Hair
    draw.ellipse([hx-36, hy-40, hx+36, hy+8], fill=(25,15,10))
    # Eyes (going wide — whites showing)
    draw.ellipse([hx-14, hy-6, hx-2, hy+8], fill=(255,255,245))
    draw.ellipse([hx+2, hy-6, hx+14, hy+8], fill=(255,255,245))
    draw.ellipse([hx-11, hy-3, hx-5, hy+5], fill=(20,12,8))
    draw.ellipse([hx+5, hy-3, hx+11, hy+5], fill=(20,12,8))
    # Mouth starting to open
    draw.arc([hx-10, hy+8, hx+10, hy+20], start=20, end=160, fill=(30,15,8), width=3)
    # Arms rising (surprise gesture)
    draw.line([(lx-8, body_top+50), (lx-42, body_top+25)], fill=(200,136,90), width=5)
    draw.line([(lx+8, body_top+50), (lx+38, body_top+22)], fill=(200,136,90), width=5)
    # Legs
    draw.line([(lx-6, body_bot-30), (lx-14, floor_y)], fill=(200,136,90), width=5)
    draw.line([(lx+6, body_bot-30), (lx+16, floor_y)], fill=(200,136,90), width=5)

    # BYTE — center-right, frozen in place (the cause)
    bx = int(PW * 0.62)
    by = int(DRAW_H * 0.42)
    bs = 30
    c = bs // 8
    body_pts = [
        (bx-bs//2+c, by-bs//2), (bx+bs//2-c, by-bs//2),
        (bx+bs//2, by-bs//2+c), (bx+bs//2, by+bs//2-c),
        (bx+bs//2-c, by+bs//2), (bx-bs//2+c, by+bs//2),
        (bx-bs//2, by+bs//2-c), (bx-bs//2, by-bs//2+c),
    ]
    draw.polygon(body_pts, fill=(0,212,232), outline=(10,10,20), width=2)
    # Byte pixel eye (! alarmed)
    draw.rectangle([bx-8, by-4, bx-1, by+7], fill=(255,255,255), outline=(0,100,120), width=1)
    for dy in [-3, 0, 3]:
        draw.rectangle([bx-6, by+dy, bx-3, by+dy+1], fill=(0,240,255))
    draw.rectangle([bx-6, by+5, bx-3, by+7], fill=(0,240,255))
    # Hover glow
    draw.ellipse([bx-18, by+bs//2, bx+18, by+bs//2+8], fill=(0,55,75))

    # Spatial arrow annotation
    try:
        font_ann = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    except:
        font_ann = font
    draw.text((4, 4), "MED — pre-scream recoil", fill=(150,140,120), font=font_ann)

def draw_p13_scream(draw, font, font_bold):
    """P13 REDRAW — full 3D spatial staging.
    Camera: MED WIDE, slightly low, centered on room.
    Room geometry visible: floor, back wall, monitors on wall.
    Luma: left, arms flung wide, screaming.
    Byte: center-right, frozen/alarmed, at Luma's eye level.
    Monitors: back wall, activating in response to the sound."""

    # ── Room base ─────────────────────────────────────────────────────────────
    # Sky/ceiling (dark)
    draw.rectangle([0, 0, PW, DRAW_H], fill=(20, 14, 10))

    # Back wall (perspective — wider at top, establishes depth)
    back_wall_top = int(DRAW_H * 0.18)
    back_wall_bot = int(DRAW_H * 0.68)
    draw.rectangle([0, back_wall_top, PW, back_wall_bot], fill=(32, 23, 16))
    draw.line([(0, back_wall_top), (PW, back_wall_top)], fill=(50, 36, 24), width=2)

    # Floor (in perspective)
    floor_y = back_wall_bot
    draw.rectangle([0, floor_y, PW, DRAW_H], fill=(18, 12, 8))
    draw.line([(0, floor_y), (PW, floor_y)], fill=(40, 28, 18), width=2)

    # Perspective lines to vanishing point (center, back wall)
    vp_x, vp_y = PW // 2, back_wall_top + 20
    for edge_x in [0, PW]:
        draw.line([(edge_x, DRAW_H), (vp_x, vp_y)], fill=(28, 20, 13), width=1)

    # ── MONITORS on back wall (3, lit up — responding to scream) ─────────────
    monitor_specs = [
        (40, back_wall_top + 12, 88, 52, (0, 240, 255)),     # left — cyan
        (196, back_wall_top + 8, 96, 58, (255, 45, 107)),    # center — magenta
        (352, back_wall_top + 12, 80, 50, (0, 200, 65)),     # right — acid green
    ]
    for mx, my, mw, mh, glow in monitor_specs:
        # Monitor casing
        draw.rectangle([mx, my, mx+mw, my+mh], fill=(12, 8, 16), outline=(40,30,50), width=2)
        # Screen glow (reacting to scream — fully lit)
        draw.rectangle([mx+3, my+3, mx+mw-3, my+mh-3], fill=glow)
        # Screen center fill (lighter)
        cx_m, cy_m = mx + mw//2, my + mh//2
        draw.ellipse([cx_m-20, cy_m-14, cx_m+20, cy_m+14], fill=(min(255,glow[0]+60), min(255,glow[1]+60), min(255,glow[2]+60)))
        # Screen glow spill onto wall
        for r in range(18, 4, -5):
            draw.ellipse([cx_m-r*2, cy_m-r, cx_m+r*2, cy_m+r], outline=glow, width=1)

    # ── BED (right side, angled in perspective) ───────────────────────────────
    bed_lx = int(PW * 0.72)
    bed_rx = PW + 10
    bed_ty = int(DRAW_H * 0.52)
    bed_by = floor_y
    draw.polygon([(bed_lx, bed_ty), (bed_rx, bed_ty+12),
                  (bed_rx, bed_by), (bed_lx, bed_by-5)], fill=(55, 38, 28))
    draw.line([(bed_lx, bed_ty), (bed_rx, bed_ty+12)], fill=(70,50,35), width=2)

    # ── LUMA — left of center, full-body scream ───────────────────────────────
    lx = int(PW * 0.28)
    body_top_y = int(DRAW_H * 0.22)
    body_bot_y = floor_y - 3

    # Floor shadow
    draw.ellipse([lx-32, floor_y-6, lx+32, floor_y+5], fill=(12, 8, 5))

    # Legs (feet planted, weight forward)
    draw.line([(lx-8, body_bot_y-20), (lx-18, floor_y)], fill=(200,136,90), width=6)
    draw.line([(lx+8, body_bot_y-20), (lx+20, floor_y)], fill=(200,136,90), width=6)

    # Torso (hoodie — orange-amber)
    torso_pts = [
        (lx-18, body_top_y+30), (lx+18, body_top_y+30),
        (lx+22, body_bot_y-20), (lx-22, body_bot_y-20)
    ]
    draw.polygon(torso_pts, fill=(232, 114, 42), outline=(50,30,15), width=1)

    # Arms FLUNG WIDE (full wingspan of terror)
    # Left arm — up-left diagonal
    draw.line([(lx-14, body_top_y+48), (lx-68, body_top_y+12)], fill=(200,136,90), width=7)
    draw.ellipse([lx-76, body_top_y+5, lx-58, body_top_y+22], fill=(200,136,90))  # hand
    # Right arm — up-right diagonal
    draw.line([(lx+14, body_top_y+48), (lx+68, body_top_y+12)], fill=(200,136,90), width=7)
    draw.ellipse([lx+58, body_top_y+5, lx+76, body_top_y+22], fill=(200,136,90))  # hand

    # Head
    hx, hy = lx, body_top_y + 14
    draw.ellipse([hx-26, hy-26, hx+26, hy+26], fill=(200,136,90), outline=(50,30,15), width=2)
    # Hair (big unruly cloud, flyaway from shock)
    draw.ellipse([hx-38, hy-44, hx+38, hy+8], fill=(25, 15, 10))
    # Flyaway shock curls
    draw.arc([hx-45, hy-48, hx-22, hy-28], start=140, end=320, fill=(25,15,10), width=5)
    draw.arc([hx+22, hy-48, hx+45, hy-28], start=220, end=40, fill=(25,15,10), width=5)
    # Eyes (horror — pupils tiny, whites showing)
    draw.ellipse([hx-16, hy-7, hx-3, hy+8], fill=(255,255,245))
    draw.ellipse([hx+3, hy-7, hx+16, hy+8], fill=(255,255,245))
    draw.ellipse([hx-12, hy-3, hx-7, hy+4], fill=(20,12,8))  # tiny pupils
    draw.ellipse([hx+7, hy-3, hx+12, hy+4], fill=(20,12,8))
    # Eyebrows — shot up in terror
    draw.arc([hx-20, hy-24, hx-2, hy-12], start=190, end=340, fill=(25,15,10), width=4)
    draw.arc([hx+2, hy-24, hx+20, hy-12], start=200, end=350, fill=(25,15,10), width=4)
    # Mouth — wide open scream (O shape)
    draw.ellipse([hx-12, hy+8, hx+12, hy+22], fill=(25, 10, 5), outline=(50,30,15), width=2)

    # Scream energy lines radiating from mouth
    for angle in range(250, 430, 20):
        r1, r2 = 16, 38
        ax1 = hx + int(r1 * math.cos(math.radians(angle)))
        ay1 = hy + 15 + int(r1 * math.sin(math.radians(angle)))
        ax2 = hx + int(r2 * math.cos(math.radians(angle)))
        ay2 = hy + 15 + int(r2 * math.sin(math.radians(angle)))
        draw.line([(ax1, ay1), (ax2, ay2)], fill=(255, 220, 80), width=1)

    # ── BYTE — center-right, alarmed-frozen ───────────────────────────────────
    bx = int(PW * 0.60)
    by_center = int(DRAW_H * 0.38)
    bs = 34
    c = bs // 8
    body_pts = [
        (bx-bs//2+c, by_center-bs//2), (bx+bs//2-c, by_center-bs//2),
        (bx+bs//2, by_center-bs//2+c), (bx+bs//2, by_center+bs//2-c),
        (bx+bs//2-c, by_center+bs//2), (bx-bs//2+c, by_center+bs//2),
        (bx-bs//2, by_center+bs//2-c), (bx-bs//2, by_center-bs//2+c),
    ]
    draw.polygon(body_pts, fill=(0, 212, 232), outline=(10,10,20), width=2)
    # Shadow right side
    shadow_pts = [
        (bx, by_center-bs//2+c), (bx+bs//2-c, by_center-bs//2),
        (bx+bs//2, by_center-bs//2+c), (bx+bs//2, by_center+bs//2-c),
        (bx+bs//2-c, by_center+bs//2), (bx, by_center+bs//2),
    ]
    draw.polygon(shadow_pts, fill=(0, 144, 176))
    # Highlight
    draw.line([(bx-bs//2+c, by_center-bs//2), (bx+bs//2-c, by_center-bs//2)], fill=(0,240,255), width=2)

    # Byte pixel eyes — both showing ! (alarmed)
    for ex_off in [-10, 4]:
        ex = bx + ex_off
        ey = by_center - 4
        draw.rectangle([ex, ey, ex+8, ey+12], fill=(255,255,255), outline=(0,100,120), width=1)
        for dot_y in [ey+1, ey+4, ey+7]:
            draw.rectangle([ex+3, dot_y, ex+5, dot_y+1], fill=(0,240,255))
        draw.rectangle([ex+3, ey+10, ex+5, ey+11], fill=(0,240,255))

    # Stubby arms raised (alarmed pose)
    draw.rectangle([bx-bs//2-10, by_center-8, bx-bs//2, by_center+2], fill=(0,212,232), outline=(10,10,20), width=1)
    draw.rectangle([bx+bs//2, by_center-8, bx+bs//2+10, by_center+2], fill=(0,212,232), outline=(10,10,20), width=1)

    # Hover glow
    draw.ellipse([bx-20, by_center+bs//2, bx+20, by_center+bs//2+8], fill=(0, 55, 75))

    # ── Spatial annotation ────────────────────────────────────────────────────
    try:
        font_ann = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
    except:
        font_ann = font
    draw.text((4, 4), "MED WIDE — slight low angle", fill=(150,140,120), font=font_ann)
    draw.text((4, 14), "CAM: center, 3/4 low", fill=(130,120,100), font=font_ann)

def draw_p25_title(draw, font, font_bold):
    draw.rectangle([0, 0, PW, DRAW_H], fill=(8, 6, 14))
    # Glitch scan lines
    for y in range(0, DRAW_H, 6):
        if y % 18 == 0:
            draw.line([(0, y), (PW, y)], fill=(20, 15, 30), width=2)

    # Glitch offset rectangles (corruption artifacts)
    import random; random.seed(7)
    for _ in range(6):
        gx = random.randint(20, PW-20)
        gy = random.randint(20, DRAW_H-20)
        gw = random.randint(30, 120)
        gh = random.randint(3, 12)
        gc = random.choice([(0,240,255),(255,45,107),(0,200,65)])
        for i in range(gh):
            draw.line([(gx, gy+i), (gx+gw, gy+i)], fill=gc, width=1)

    try:
        font_title_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except:
        font_title_big = font_bold
        font_sub = font

    # Cyan offset shadow
    draw.text((PW//2 - 142, DRAW_H//2 - 38), "LUMA &", fill=(0, 180, 200), font=font_title_big)
    draw.text((PW//2 - 152, DRAW_H//2 - 4), "THE GLITCHKIN", fill=(255, 30, 90), font=font_title_big)
    # Main text
    draw.text((PW//2 - 140, DRAW_H//2 - 40), "LUMA &", fill=(0, 240, 255), font=font_title_big)
    draw.text((PW//2 - 150, DRAW_H//2 - 6), "THE GLITCHKIN", fill=(255, 255, 255), font=font_title_big)

    draw.text((PW//2 - 60, DRAW_H//2 + 34), "[ SMASH CUT ]", fill=(100, 90, 120), font=font_sub)

    # P25 ANNOTATION: title construction method
    draw.text((8, DRAW_H - 18), "TITLE CONSTRUCTS glitch-by-glitch (not hard cut)", fill=(120,110,90), font=font_sub)

def generate_all():
    import os
    out = "/home/wipkat/team/output/storyboards/panels"
    os.makedirs(out, exist_ok=True)

    panels = [
        ("01",  "EWS",      "Millbrook. Night. One window glows. Antenna cluster on roof.",
         draw_p01_exterior,   "panel_p01_exterior.png"),
        ("03",  "ECU MON",  "One pixel. Cyan. Wrong. LOWER-CENTER. It pulses — glow rings show it.",
         draw_p03_pixel,      "panel_p03_first_pixel.png"),
        ("07",  "MED-LOW",  "[BRIDGE] Byte drifts across bedroom floor toward sleeping Luma.",
         draw_p07_approach,   "panel_p07_approach.png"),
        ("11",  "CU",       "Eyes snap open. Nose to nose. BEAT. Luma: 'oh no' brow raise.",
         draw_p11_nose_to_nose, "panel_p11_nose_to_nose.png"),
        ("12",  "MED",      "[BRIDGE] Initial recoil. Room geometry established. Monitors dark.",
         draw_p12_recoil,     "panel_p12_recoil.png"),
        ("13",  "MED WIDE", "Simultaneous scream. 3D room. Monitors activate. Arms flung wide.",
         draw_p13_scream,     "panel_p13_scream.png"),
        ("25",  "TITLE",    "SMASH CUT. Glitch construction, letter-by-letter. LUMA & THE GLITCHKIN.",
         draw_p25_title,      "panel_p25_title_card.png"),
    ]

    images = []
    for num, shot, caption, draw_fn, filename in panels:
        img = make_panel(num, shot, caption, draw_fn, os.path.join(out, filename))
        images.append(img)

    # Contact sheet — 2 rows of panels
    cols = 4
    rows = 2
    pad = 4
    cs_w = cols * (PW + pad) + pad
    cs_h = 50 + rows * (PH + pad) + pad
    cs = Image.new('RGB', (cs_w, cs_h), (20, 15, 12))
    d = ImageDraw.Draw(cs)
    try:
        ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except:
        ft = ImageFont.load_default()
    d.text((10, 10), "LUMA & THE GLITCHKIN — Ep01 Cold Open — Cycle 5 Revision", fill=(220,210,190), font=ft)
    for i, img in enumerate(images):
        col = i % cols
        row = i // cols
        x = pad + col * (PW + pad)
        y = 50 + pad + row * (PH + pad)
        cs.paste(img, (x, y))
    cs.save(os.path.join(out, "contact_sheet.png"))
    print(f"Saved: {os.path.join(out, 'contact_sheet.png')}")

if __name__ == '__main__':
    generate_all()
