#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sb_ep05_covetous.py
Episode 5 — COVETOUS Beat: Three-Character Triangulation Storyboard Panel
Diego Vargas, Storyboard Artist — Cycle 43

Beat: Glitch's first appearance in the series (Episode 5).
      Three-character triangulation: Glitch (COVETOUS, left) — Byte (barrier, midground center)
      — Luma (subject of desire, right zone, warm character palette).

      Glitch wants what it cannot take: Luma's ability to move freely between worlds.
      The image is the gap between Glitch and Luma. Byte stands in it.

Shot:   Low angle (approximately Glitch's center height — Glitch reads larger, imposing)
Setting: Glitch Layer — familiar location where Glitch is already present.
         UV Purple void, digital platform depth system.

Character positions:
  LEFT / CENTER-LEFT: Glitch — COVETOUS state. tilt_deg=+12 (lean toward Luma).
                       Bilateral acid-slit eyes [[5,5,5],[0,5,0],[0,0,0]].
                       Arms slightly raised (arm_l_dy=-8, arm_r_dy=-6).
                       spike_h=12. Corrupt Amber body. UV Purple shadow +3px/+4px.
  MIDGROUND CENTER:   Byte — protective barrier posture. Teal body. Smaller than Glitch.
                       Arms extended slightly (barrier lean between characters).
  RIGHT ZONE:         Luma — LUMA_HOODIE orange. Warm skin. Background-scale.
                       She is what Glitch covets: the bridge between worlds.

Color arc (left to right): Glitch amber-in-void → Byte teal-transition → Luma warm orange
Warm zone rule: Luma's warm colors must stay right 30%. Glitch NOT warmed by Luma.

Arc: no arc defined for EP5 — this is a STYLE FRAME / KEY BEAT storyboard panel.
     Border: UV_PURPLE (the Glitch Layer signature).

Image size rule: ≤ 1280px in both dimensions.
Output: output/storyboards/panels/LTG_SB_ep05_covetous.png
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
from PIL import Image, ImageDraw, ImageFont
import math, random, os

PANELS_DIR = output_dir('storyboards', 'panels')
OUTPUT_PATH = os.path.join(PANELS_DIR, "LTG_SB_ep05_covetous.png")
os.makedirs(PANELS_DIR, exist_ok=True)

PW, PH    = 800, 600
CAPTION_H = 60
DRAW_H    = PH - CAPTION_H   # 540

# ── Palette ──────────────────────────────────────────────────────────────────
# Glitch Layer background
VOID_BLACK      = (10, 10, 20)
UV_PURPLE       = (123, 47, 190)
UV_PURPLE_DIM   = (74, 28, 114)
UV_PURPLE_ATMO  = (46, 17, 80)
PLATFORM_LINE   = (0, 240, 255)      # GL-01 Electric Cyan — thin platform lines only
PLATFORM_MID    = (0, 130, 160)      # desaturated for mid-distance depth
# Glitch character
CORRUPT_AMBER   = (255, 140, 0)      # GL-07
CORRUPT_AMB_HL  = (255, 185, 80)     # highlight facet
CORRUPT_AMB_SH  = (168, 92, 0)       # shadow / bottom spike
HOT_MAG         = (255, 45, 107)     # GL-02 crack line
ACID_GREEN      = (57, 255, 20)      # GL-03 — COVETOUS eye color
# Byte character
BYTE_TEAL       = (0, 212, 232)
BYTE_TEAL_DIM   = (0, 160, 180)      # under UV ambient
ELEC_CYAN       = (0, 212, 232)
ELEC_CYAN_HI    = (90, 248, 255)
BYTE_EYE_W      = (228, 240, 248)
CRACK_LINE      = (200, 30, 100)
# Luma character (right warm zone)
LUMA_HOODIE     = (232, 112, 58)     # CANONICAL ORANGE per master_palette.md
LUMA_SKIN       = (218, 172, 128)    # under UV ambient — cooler than SF01, retains R>G>B warmth
LUMA_HAIR       = (38, 22, 14)
SOFT_GOLD       = (232, 201, 90)     # RW-02 warm ambient radiate from Luma (alpha max 50)
# Caption / annotation
BG_CAPTION      = (10, 6, 18)
TEXT_CAP        = (230, 220, 210)
ANN_COL         = (180, 155, 210)    # purple-tinted annotation
ANN_DIM         = (120, 108, 148)
BORDER_COLOR    = UV_PURPLE          # Glitch Layer frame

RNG = random.Random(555)


def load_font(size=14, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()


def add_glow(img, cx, cy, r_max, color_rgb, steps=6, max_alpha=50):
    for i in range(steps, 0, -1):
        r     = int(r_max * (i / steps))
        alpha = int(max_alpha * (1 - (i / steps) * 0.6))
        glow  = Image.new('RGBA', img.size, (0, 0, 0, 0))
        gd    = ImageDraw.Draw(glow)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color_rgb, alpha))
        base  = img.convert('RGBA')
        img.paste(Image.alpha_composite(base, glow).convert('RGB'))


def draw_irregular_poly(draw, cx, cy, r, sides, color, seed=0, outline=None, outline_w=1):
    """4–7 sided irregular polygon — Cycle 11 standard."""
    rng = random.Random(seed)
    pts = []
    for i in range(sides):
        angle = (2 * math.pi * i / sides) + rng.uniform(-0.28, 0.28)
        dist  = r * rng.uniform(0.68, 1.22)
        pts.append((int(cx + dist * math.cos(angle)), int(cy + dist * math.sin(angle))))
    draw.polygon(pts, fill=color, outline=outline)


def diamond_pts(cx, cy, rx, ry, tilt_deg=0):
    """Glitch diamond body vertices (per glitch.md §2.1)."""
    a = math.radians(tilt_deg)
    # Follows glitch.md spec exactly
    top   = (cx + int(rx * 0.15 * math.sin(a)),  cy - ry + int(rx * 0.15 * math.cos(a)))
    right = (cx + int(rx * math.cos(-a)),          cy + int(rx * 0.2 * math.sin(-a)))
    bot   = (cx - int(rx * 0.15 * math.sin(a)),   cy + int(ry * 1.15))
    left  = (cx - int(rx * math.cos(-a)),          cy - int(rx * 0.2 * math.sin(-a)))
    return top, right, bot, left


def draw_glitch(draw, cx, cy, rx=34, ry=38, tilt_deg=12,
                spike_h=12, arm_l_dy=-8, arm_r_dy=-6,
                scale=1.0):
    """
    Draw Glitch in COVETOUS state.
    tilt_deg=+12 (lean toward Luma / camera-right).
    Bilateral acid-slit eyes: [[5,5,5],[0,5,0],[0,0,0]]
    Arms slightly raised toward Luma.
    """
    # Scale all measurements
    rx = int(rx * scale)
    ry = int(ry * scale)
    spike_h = int(spike_h * scale)

    top, right, bot, left = diamond_pts(cx, cy, rx, ry, tilt_deg)

    # ── Shadow offset (+3px right, +4px down per spec) ────────────────────────
    sh_pts = [(p[0] + 3, p[1] + 4) for p in [top, right, bot, left]]
    draw.polygon(sh_pts, fill=UV_PURPLE_DIM)

    # ── Body fill ─────────────────────────────────────────────────────────────
    draw.polygon([top, right, bot, left], fill=CORRUPT_AMBER, outline=VOID_BLACK)

    # ── Highlight facet (upper-left triangle) ─────────────────────────────────
    ctr    = (cx, cy - ry // 4)
    mid_tl = ((top[0] + left[0]) // 2, (top[1] + left[1]) // 2)
    draw.polygon([top, ctr, mid_tl], fill=CORRUPT_AMB_HL)

    # ── Outline (reapply over highlight) ──────────────────────────────────────
    draw.polygon([top, right, bot, left], fill=None, outline=VOID_BLACK)

    # ── HOT_MAG crack (diagonal upper-left to lower-right) ───────────────────
    cs = (cx - rx // 2, cy - ry // 3)
    ce = (cx + rx // 3, cy + ry // 2)
    draw.line([cs, ce], fill=HOT_MAG, width=max(1, int(2 * scale)))
    mid_c = ((cs[0] + ce[0]) // 2, (cs[1] + ce[1]) // 2)
    fork  = (cx + rx // 2, cy - ry // 4)
    draw.line([mid_c, fork], fill=HOT_MAG, width=1)

    # ── Top spike (crown, 5-point) ────────────────────────────────────────────
    a       = math.radians(tilt_deg)
    tilt_off = int(a * rx * 0.4)
    sy       = top[1]
    sx       = cx + tilt_off
    spike_pts = [
        (sx - spike_h // 2, sy),
        (sx - spike_h,       sy - spike_h),
        (sx,                 sy - spike_h * 2),    # tip
        (sx + spike_h,       sy - spike_h),
        (sx + spike_h // 2,  sy),
    ]
    draw.polygon(spike_pts, fill=CORRUPT_AMBER, outline=VOID_BLACK)
    # HOT_MAG spark at tip
    tip = spike_pts[2]
    draw.line([tip, (tip[0], tip[1] - int(spike_h * 0.4))], fill=HOT_MAG, width=2)

    # ── Bottom spike (hover point) ─────────────────────────────────────────────
    by = bot[1]
    bot_spike_pts = [
        (cx - spike_h // 2, by),
        (cx + spike_h // 2, by),
        (cx,                by + spike_h + 4),
    ]
    draw.polygon(bot_spike_pts, fill=CORRUPT_AMB_SH, outline=VOID_BLACK)

    # ── Arm-spikes ─────────────────────────────────────────────────────────────
    # Left arm-spike (from left vertex)
    arm_spike_h = max(4, int(10 * scale))
    for (vertex, arm_dy, arm_dir) in [(left, arm_l_dy, -1), (right, arm_r_dy, 1)]:
        vx, vy = vertex
        # arm_dy < 0 = raised (reaching forward/toward subject)
        scaled_dy = int(arm_dy * scale)
        arm_tip_y = vy + scaled_dy
        arm_tip_x = vx + arm_dir * arm_spike_h
        arm_pts = [
            (vx,                    vy - arm_spike_h // 3),
            (vx,                    vy + arm_spike_h // 3),
            (arm_tip_x,             arm_tip_y),
        ]
        draw.polygon(arm_pts, fill=CORRUPT_AMBER, outline=VOID_BLACK)

    # ── COVETOUS eyes (bilateral acid slit: [[5,5,5],[0,5,0],[0,0,0]]) ─────────
    # cell_size proportional to rx
    cell = max(3, int(4 * scale))
    face_cy = cy - int(ry * 0.15)   # eye row slightly above center

    for eye_side, ex in [(-1, cx - rx // 2), (1, cx + rx // 2)]:
        leye_x = ex - cell * 3 // 2
        leye_y = face_cy - cell * 3 // 2
        # COVETOUS glyph: [[5,5,5],[0,5,0],[0,0,0]]
        # Row 0 (top): all lit. Row 1 (mid): center only. Row 2 (bot): all dark.
        glyph = [
            [1, 1, 1],   # top row: all acid green
            [0, 1, 0],   # mid row: center only
            [0, 0, 0],   # bot row: all dark
        ]
        for row_i, row in enumerate(glyph):
            for col_i, val in enumerate(row):
                px = leye_x + col_i * cell
                py = leye_y + row_i * cell
                fill = ACID_GREEN if val else VOID_BLACK
                draw.rectangle([px, py, px + cell - 1, py + cell - 1], fill=fill)

    return top, bot, left, right


def draw_byte_barrier(draw, cx, cy, body_h, scale=0.75):
    """
    Byte in barrier posture: positioned between Glitch and Luma.
    Arms extended slightly (barrier lean). Scale < Glitch (Byte reads smaller).
    """
    bh = int(body_h * scale)
    torso_h  = int(bh * 0.62)
    head_r   = int(bh * 0.22)
    leg_h    = int(bh * 0.25)

    torso_top_y = cy - int(bh * 0.50)
    torso_bot_y = torso_top_y + torso_h
    torso_hw_t  = int(bh * 0.29)
    torso_hw_b  = int(bh * 0.12)

    # Body (inverted teardrop)
    torso_pts = [
        (cx - torso_hw_t, torso_top_y + int(torso_h * 0.18)),
        (cx,              torso_top_y),
        (cx + torso_hw_t, torso_top_y + int(torso_h * 0.18)),
        (cx + torso_hw_b + 3, torso_bot_y - 4),
        (cx - torso_hw_b - 3, torso_bot_y - 4),
    ]
    draw.polygon(torso_pts, fill=BYTE_TEAL, outline=VOID_BLACK)

    # Inner core
    ihw = int(torso_hw_t * 0.52)
    inner_pts = [
        (cx - ihw, torso_top_y + int(torso_h * 0.28)),
        (cx,       torso_top_y + int(torso_h * 0.10)),
        (cx + ihw, torso_top_y + int(torso_h * 0.28)),
        (cx + ihw - 3, torso_bot_y - 8),
        (cx - ihw + 3, torso_bot_y - 8),
    ]
    draw.polygon(inner_pts, fill=VOID_BLACK)

    # Head
    head_cy = torso_top_y + int(head_r * 0.58)
    draw_irregular_poly(draw, cx, head_cy, head_r, 6, BYTE_TEAL, seed=5501, outline=VOID_BLACK)

    # Arms — EXTENDED (barrier posture — arms out at body level)
    arm_top_y = torso_top_y + int(torso_h * 0.20)
    arm_bot_y = torso_top_y + int(torso_h * 0.55)
    arm_len   = int(bh * 0.26)    # slightly extended for barrier read
    arm_w     = int(bh * 0.075)

    for side in [-1, 1]:
        ax0    = cx + side * torso_hw_t
        ax2    = ax0 + side * arm_len
        amid_y = arm_top_y + int((arm_bot_y - arm_top_y) * 0.5)
        arm_pts = [
            (ax0,                   arm_top_y),
            (ax2 + side * 2,        amid_y - arm_w),
            (ax2 + side * 4,        amid_y + arm_w),
            (ax0,                   arm_bot_y),
        ]
        draw.polygon(arm_pts, fill=BYTE_TEAL, outline=VOID_BLACK)
        hand_r = int(bh * 0.062)
        draw_irregular_poly(draw, ax2 + side * 4, amid_y, hand_r, 5,
                            ELEC_CYAN_HI, seed=5502 + side * 3, outline=VOID_BLACK)

    # Legs
    leg_top_y = torso_bot_y - 4
    leg_w     = int(bh * 0.09)
    for side in [-1, 1]:
        lx = cx + side * torso_hw_b // 2
        fx = lx + side * int(bh * 0.04)
        leg_pts = [
            (lx - leg_w // 2, leg_top_y),
            (lx + leg_w // 2, leg_top_y),
            (fx + leg_w // 2 + side * 2, leg_top_y + leg_h),
            (fx - leg_w // 2 + side * 2, leg_top_y + leg_h),
        ]
        draw.polygon(leg_pts, fill=BYTE_TEAL, outline=VOID_BLACK)

    # Eyes — organic (left, faces toward Glitch) + cracked (right, faces outward)
    eye_cy  = head_cy - int(head_r * 0.12)
    eye_sep = int(head_r * 0.45)
    e_r     = int(head_r * 0.30)

    # Left (organic) eye faces Glitch (camera-left) — iris slightly left
    le_cx = cx - eye_sep
    draw.ellipse([le_cx - e_r, eye_cy - e_r, le_cx + e_r, eye_cy + e_r],
                 fill=BYTE_EYE_W, outline=VOID_BLACK, width=1)
    iris_r = int(e_r * 0.50)
    iris_ox = -int(iris_r * 0.30)    # shifted toward Glitch
    draw.ellipse([le_cx - iris_r + iris_ox, eye_cy - iris_r,
                  le_cx + iris_r + iris_ox, eye_cy + iris_r],
                 fill=ELEC_CYAN, outline=VOID_BLACK, width=1)

    # Right (cracked) eye faces outward
    re_cx = cx + eye_sep
    draw.ellipse([re_cx - e_r, eye_cy - e_r, re_cx + e_r, eye_cy + e_r],
                 fill=VOID_BLACK, outline=ELEC_CYAN_HI, width=1)
    draw.line([(re_cx - e_r + 2, eye_cy - int(e_r * 0.65)),
               (re_cx + e_r - 2, eye_cy + int(e_r * 0.65))],
              fill=CRACK_LINE, width=1)
    draw.ellipse([re_cx - 3, eye_cy - 3, re_cx + 3, eye_cy + 3],
                 fill=ELEC_CYAN)

    # Mouth — flat, protective (barrier posture = determined neutrality)
    mouth_y  = head_cy + int(head_r * 0.42)
    mouth_hw = int(head_r * 0.44)
    draw.line([(cx - mouth_hw, mouth_y), (cx + mouth_hw, mouth_y)],
              fill=VOID_BLACK, width=2)

    return head_cy, head_r


def draw_luma_right(draw, cx, cy, scale=0.65):
    """
    Luma in right zone — warm palette. Background-scale (smaller than Byte).
    Slightly behind Byte's depth plane.
    """
    bh    = int(DRAW_H * 0.35 * scale)
    head_r = int(bh * 0.22)

    # Head
    draw.ellipse([cx - head_r, cy - head_r, cx + head_r, cy + head_r],
                 fill=LUMA_SKIN, outline=(100, 68, 48))

    # Hair cloud
    hair_r = int(head_r * 1.42)
    for seed_h in [201, 211, 221, 231, 241, 251]:
        draw_irregular_poly(draw, cx, cy, hair_r, 7, LUMA_HAIR, seed=seed_h)
    draw.ellipse([cx - head_r + 3, cy - head_r + 3,
                  cx + head_r - 3, cy + head_r - 3], fill=LUMA_SKIN)

    # Eyes (slightly apprehensive — sensing something is wrong, but asleep or unaware)
    eye_cy_l = cy
    eye_sep_l = int(head_r * 0.38)
    e_r_l     = int(head_r * 0.22)
    for side in [-1, 1]:
        ex = cx + side * eye_sep_l
        draw.ellipse([ex - e_r_l, eye_cy_l - e_r_l,
                      ex + e_r_l, eye_cy_l + e_r_l],
                     fill=(60, 38, 28))
        # Iris
        draw.ellipse([ex - int(e_r_l * 0.58), eye_cy_l - int(e_r_l * 0.58),
                      ex + int(e_r_l * 0.58), eye_cy_l + int(e_r_l * 0.58)],
                     fill=(80, 48, 30))

    # Hoodie body (orange — this is the warm zone that Glitch covets)
    torso_top = cy + head_r
    torso_bot = torso_top + int(bh * 0.52)
    torso_hw  = int(head_r * 1.24)
    draw.rectangle([cx - torso_hw, torso_top, cx + torso_hw, torso_bot],
                   fill=LUMA_HOODIE, outline=(160, 68, 28))

    # Hoodie pocket (canonical pocket bump asymmetry)
    pock_x = cx - int(torso_hw * 0.18)
    pock_y = torso_top + int((torso_bot - torso_top) * 0.55)
    pock_w = int(torso_hw * 0.85)
    pock_h = int((torso_bot - torso_top) * 0.40)
    draw.rectangle([pock_x, pock_y, pock_x + pock_w, pock_y + pock_h],
                   fill=(200, 88, 40), outline=(160, 68, 28))

    # Legs (standing)
    leg_top = torso_bot
    leg_h   = int(bh * 0.22)
    leg_w   = int(head_r * 0.50)
    for side in [-1, 1]:
        lx = cx + side * int(torso_hw * 0.40)
        draw.rectangle([lx - leg_w, leg_top, lx + leg_w, leg_top + leg_h],
                       fill=(60, 52, 80), outline=(38, 30, 54))   # dark pants (UV ambient)

    return cx, cy


def draw_platform_lines(draw, n_lines=4, seed=88):
    """Canonical Glitch Layer platform depth system — thin cyan lines only."""
    rng = random.Random(seed)
    platform_y_levels = [
        int(DRAW_H * 0.68), int(DRAW_H * 0.76), int(DRAW_H * 0.84), int(DRAW_H * 0.90)
    ]
    for py in platform_y_levels:
        # Platform line: perspective-narrowed toward vanishing point
        x_l = rng.randint(0, int(PW * 0.08))
        x_r = rng.randint(int(PW * 0.88), PW)
        draw.line([(x_l, py), (x_r, py)], fill=PLATFORM_LINE, width=1)
        # Mid-ground depth markers (dimmer lines between platforms)
        for px_off in [int(PW * 0.15), int(PW * 0.38), int(PW * 0.60), int(PW * 0.82)]:
            y_off = rng.randint(-3, 3)
            draw.line([(px_off, py + y_off), (px_off, py + y_off + int(DRAW_H * 0.07))],
                      fill=PLATFORM_MID, width=1)


def draw_scene(img):
    draw = ImageDraw.Draw(img)

    # ── Background — Glitch Layer void ───────────────────────────────────────
    # Far void: VOID_BLACK base
    draw.rectangle([0, 0, PW, DRAW_H], fill=VOID_BLACK)

    # UV atmospheric haze (left 75% — Glitch's zone)
    uv_layer = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    uvd = ImageDraw.Draw(uv_layer)
    for bx in range(0, int(PW * 0.78)):
        t = 1.0 - (bx / (PW * 0.78))
        a = max(0, int(85 * t * t))
        uvd.line([(bx, 0), (bx, DRAW_H)], fill=(*UV_PURPLE, a))
    img.paste(Image.alpha_composite(img.convert('RGBA'), uv_layer).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Atmospheric mid-void band (depth separation)
    draw.rectangle([0, int(DRAW_H * 0.38), PW, int(DRAW_H * 0.55)],
                   fill=UV_PURPLE_ATMO)
    # Soften this band's edges
    add_glow(img, PW // 2, int(DRAW_H * 0.46), int(PW * 0.55), UV_PURPLE_ATMO,
             steps=3, max_alpha=18)
    draw = ImageDraw.Draw(img)

    # Platform ground void (lower 30%)
    draw.rectangle([0, int(DRAW_H * 0.72), PW, DRAW_H], fill=UV_PURPLE_DIM)

    # Platform lines
    draw_platform_lines(draw)

    # ── Right zone: Luma's warm character warmth radiates (alpha max 50) ───────
    # Soft gold radial glow from Luma's position — NOT a light source on Glitch
    luma_cx = int(PW * 0.80)
    luma_cy = int(DRAW_H * 0.40)
    warm_glow_layer = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    wgd = ImageDraw.Draw(warm_glow_layer)
    # Radial from Luma — falls to 0 over 120px
    for r in range(120, 0, -10):
        a = max(0, int(50 * (1 - r / 120)))
        wgd.ellipse([luma_cx - r, luma_cy - r, luma_cx + r, luma_cy + r],
                    fill=(*SOFT_GOLD, a))
    img.paste(Image.alpha_composite(img.convert('RGBA'), warm_glow_layer).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # ── Draw characters (back to front: Luma, Byte, Glitch) ──────────────────

    # LUMA (right zone — background scale, slightly behind Byte)
    draw_luma_right(draw, luma_cx, luma_cy, scale=0.62)

    # BYTE (midground barrier — between Glitch and Luma)
    byte_cx = int(PW * 0.53)
    byte_cy = int(DRAW_H * 0.44)
    byte_bh = int(DRAW_H * 0.30)
    draw_byte_barrier(draw, byte_cx, byte_cy, byte_bh, scale=0.78)

    # UV Purple shadow on Byte (canonical Glitch Layer ambient)
    byte_shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    bsd = ImageDraw.Draw(byte_shadow)
    bsd.ellipse([byte_cx - int(byte_bh * 0.25) + 4, byte_cy - int(byte_bh * 0.35) + 5,
                 byte_cx + int(byte_bh * 0.25) + 4, byte_cy + int(byte_bh * 0.35) + 5],
                fill=(*UV_PURPLE_DIM, 50))
    img.paste(Image.alpha_composite(img.convert('RGBA'), byte_shadow).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # GLITCH (left/center-left — foreground, dominant) — COVETOUS state
    glitch_cx = int(PW * 0.26)
    glitch_cy = int(DRAW_H * 0.42)
    glitch_rx = 44
    glitch_ry = 50

    draw_glitch(draw, glitch_cx, glitch_cy, rx=glitch_rx, ry=glitch_ry,
                tilt_deg=12, spike_h=12, arm_l_dy=-8, arm_r_dy=-6, scale=1.0)

    # COVETOUS confetti — UV Purple + dark amber only, minimal (count=4 per spec)
    for ci, (conf_col, conf_seed) in enumerate([
        (UV_PURPLE_DIM, 5501), ((168, 92, 0), 5502),
        (UV_PURPLE, 5503), (UV_PURPLE_DIM, 5504),
    ]):
        ang = math.radians(ci * 90 + 35)
        px  = glitch_cx + int(18 * math.cos(ang))
        py  = glitch_cy + int(18 * math.sin(ang))
        draw_irregular_poly(draw, px, py, 3, 5, conf_col, seed=5500 + ci)

    # Glitch ambient glow (UV Purple ambient — NOT warm light)
    add_glow(img, glitch_cx, glitch_cy, int(glitch_rx * 1.8),
             UV_PURPLE, steps=5, max_alpha=28)
    draw = ImageDraw.Draw(img)

    # ── Barrier line annotation ───────────────────────────────────────────────
    barrier_x = byte_cx
    draw.line([(barrier_x, int(DRAW_H * 0.18)), (barrier_x, int(DRAW_H * 0.88))],
              fill=(*BYTE_TEAL, ), width=1)
    # Actually draw as dashed
    dash_y = int(DRAW_H * 0.18)
    while dash_y < int(DRAW_H * 0.88):
        draw.line([(barrier_x, dash_y), (barrier_x, min(dash_y + 8, int(DRAW_H * 0.88)))],
                  fill=BYTE_TEAL_DIM, width=1)
        dash_y += 15
    draw.text((barrier_x + 4, int(DRAW_H * 0.20)), "barrier",
              font=load_font(8), fill=BYTE_TEAL_DIM)

    # ── Color arc annotation (left to right) ─────────────────────────────────
    arc_y = DRAW_H - 38
    arc_labels = [
        (int(PW * 0.18), "Glitch\namber/void"),
        (int(PW * 0.52), "Byte\nteal"),
        (int(PW * 0.80), "Luma\nwarm orange"),
    ]
    for ax, alabel in arc_labels:
        draw.text((ax - 18, arc_y), alabel, font=load_font(8), fill=ANN_DIM)

    # ── Panel annotations ─────────────────────────────────────────────────────
    font_ann   = load_font(11)
    font_ann_b = load_font(11, bold=True)

    draw.text((10, 8),
              "EP05  /  COVETOUS BEAT  /  low angle  /  Glitch Layer",
              font=font_ann, fill=ANN_COL)
    draw.text((10, 20),
              "Glitch (COVETOUS): bilateral acid-slit eyes. +12° lean. Arms slightly raised. Amber-in-void.",
              font=font_ann, fill=ANN_DIM)
    draw.text((10, 32),
              "Byte (barrier): between Glitch and Luma. Arms extended. Smaller than Glitch.",
              font=font_ann, fill=ANN_DIM)

    # Glitch label
    draw.text((glitch_cx - 20, int(DRAW_H * 0.12)), "GLITCH\nCOVETOUS",
              font=font_ann_b, fill=CORRUPT_AMBER)
    # Byte label
    draw.text((byte_cx + 5, int(DRAW_H * 0.18)), "BYTE\nbarrier",
              font=font_ann_b, fill=ELEC_CYAN)
    # Luma label
    draw.text((luma_cx - 10, int(DRAW_H * 0.16)), "LUMA\nwarm zone",
              font=font_ann_b, fill=LUMA_HOODIE)

    # Shot label
    draw.rectangle([10, DRAW_H - 24, 100, DRAW_H - 6], fill=(18, 8, 30))
    draw.text((14, DRAW_H - 22), "LOW ANGLE / STATIC",
              font=font_ann_b, fill=(200, 180, 235))

    # Rule reminder
    draw.rectangle([PW - 220, DRAW_H - 24, PW - 10, DRAW_H - 6], fill=(24, 8, 36))
    draw.text((PW - 216, DRAW_H - 22), "Glitch NOT lit by Luma (void only)",
              font=load_font(10), fill=UV_PURPLE)

    return draw


def make_panel():
    font_cap = load_font(12)
    font_ann = load_font(11)
    font_sm  = load_font(10)

    img = Image.new('RGB', (PW, PH), VOID_BLACK)
    draw_scene(img)

    # Caption bar
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, DRAW_H, PW, PH], fill=BG_CAPTION)
    draw.line([0, DRAW_H, PW, DRAW_H], fill=(6, 4, 12), width=2)
    draw.text((10, DRAW_H + 4),
              "EP05  COVETOUS BEAT  low angle  |  Three-character triangulation: Glitch / Byte / Luma",
              font=font_cap, fill=(155, 148, 185))
    draw.text((10, DRAW_H + 18),
              "Glitch: COVETOUS (bilateral acid-slit eyes, +12° lean, amber-in-void). "
              "Byte: barrier midground. Luma: warm right zone.",
              font=font_cap, fill=TEXT_CAP)
    draw.text((10, DRAW_H + 33),
              "Color arc: Glitch amber/void → Byte teal → Luma warm orange. "
              "Glitch NOT warmed by Luma. The gap IS the image.",
              font=font_ann, fill=(140, 130, 168))
    draw.text((PW - 240, DRAW_H + 46),
              "LTG_SB_ep05_covetous  /  Diego Vargas  /  C43",
              font=font_sm, fill=(95, 88, 118))

    # Border: UV_PURPLE (Glitch Layer frame)
    draw.rectangle([0, 0, PW - 1, PH - 1], outline=BORDER_COLOR, width=4)

    img.thumbnail((1280, 1280))
    img.save(OUTPUT_PATH, "PNG")
    print(f"Saved: {OUTPUT_PATH}  {img.size}")
    return OUTPUT_PATH


if __name__ == "__main__":
    make_panel()
    print("EP05 COVETOUS panel generation complete.")
