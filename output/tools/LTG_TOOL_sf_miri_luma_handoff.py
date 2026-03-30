#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_sf_miri_luma_handoff.py
Style Frame — "The Hand-Off" (SF_MIRI_LUMA_HANDOFF / SF06 candidate)
"Luma & the Glitchkin" — Cycle 49 / Maya Santos

Cycle 49 changes (Maya Santos, C49):
  - MIRI ELDER POSTURE: Forward lean (3-5 degrees) via head/torso offset.
    Head shifts +3px rightward (toward CRT), torso 60% of that, feet stay.
    Rounded shoulders: shoulder rest drops 3px, inward 2px.
    Stacks with existing C48 shoulder involvement.
  - Per Alex Chen C49 brief (Miri posture update P1).

Cycle 48 changes (Maya Santos, C48):
  - SHOULDER INVOLVEMENT: Both Miri and Luma torsos now use polyline shoulder
    points with deltoid bumps that respond to arm position.
    Miri: right shoulder shifts outward +5px (forward pull for hand-off gesture).
    Luma: left shoulder slight rise -3px (curious lean), right shoulder outward
    +5px (forward/outward arm).
    Per image-rules.md Shoulder Involvement Rule (codified C47).
    Per-character clothing reads: Miri = cardigan crease, Luma = hoodie bunch.

Cycle 44 / Maya Santos (original)

Concept: "The Hand-Off"
Miri and Luma together in the living room, at the CRT. Miri's hand is on
the TV. Luma's posture is attentive curiosity — she's being shown something,
not just standing near it. The CRT is between them in composition. Warm,
intergenerational, specific. This is the origin point of the show.

Setting: Grandma Miri's living room (the cold-open setting — CRT is here).
Palette: Real World only. No Glitch Layer colors.
Canvas: 1280×720px

Character relative scale (from lineup):
  Miri:  3.2 heads tall. HEAD_UNIT = 52px in style frame scale.
  Luma:  3.5 heads tall. HEAD_UNIT = 52px in style frame scale.
  (Lineup uses 87.5px HU. Style frame uses ~60% — characters read at
   ~2/3 lineup scale against background depth.)

Composition:
  - CRT center-left (x ~490–680)
  - Miri stands LEFT of CRT, facing slight 3/4 right. Hand toward TV.
  - Luma stands RIGHT of CRT, facing slight 3/4 left. Attentive lean.
  - Both characters at same ground line (foreground, not on BG wall plane)
  - Warm/cool split: Miri in warm zone (left lamp), Luma in cool zone (CRT glow)

Face test gate: Luma face drawn via draw_luma_face_handoff() at sprint scale.
  Miri face drawn via draw_miri_face_handoff(). No automated gate for Miri.

Output: output/color/style_frames/LTG_COLOR_sf_miri_luma_handoff.png
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path
import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter

random.seed(44)

W, H = 1280, 720

# ── Real World Palette ─────────────────────────────────────────────────────────
# Room palette (from living room env tool)
WARM_CREAM       = (250, 240, 220)
AGED_CREAM       = (238, 226, 198)
WALL_BASE        = (236, 220, 192)
WALL_SHADOW      = (188, 168, 136)
CEILING_WARM     = (244, 234, 210)
FLOOR_OAK_LIGHT  = (198, 162, 110)
FLOOR_OAK_MED   = (172, 138,  86)
FLOOR_OAK_DARK  = (140, 108,  64)
FLOOR_RUG_RED   = (158,  68,  42)
FLOOR_RUG_EDGE  = (128,  48,  28)
LINE_DARK        = ( 59,  40,  32)
NEAR_BLACK_WARM  = ( 28,  18,  10)
SHADOW_DEEP      = ( 44,  28,  16)
SUNLIT_AMBER     = (255, 200, 100)
CRT_PLASTIC      = (108,  90,  68)
CRT_PLASTIC_DARK = ( 72,  58,  40)
CRT_SCREEN_GLOW  = ( 30,  90, 108)
CRT_SCREEN_DARK  = ( 12,  52,  68)
CRT_STAND_WOOD   = ( 90,  64,  32)
CRT_COOL_SPILL   = (  0, 128, 148)
LAMP_WARM        = (255, 200, 120)
WOOD_LIGHT       = (210, 178, 130)
WOOD_MED         = (160, 128,  80)

# Miri palette
MIRI_SKIN        = (140,  84,  48)
MIRI_SKIN_SH     = (106,  58,  30)
MIRI_HAIR        = (216, 208, 200)
MIRI_HAIR_SH     = (168, 152, 136)
MIRI_CARDIGAN    = (184,  92,  56)
MIRI_CARD_SH     = (138,  60,  28)
MIRI_PANTS       = (200, 174, 138)
MIRI_SLIPPER     = ( 90, 122,  90)
MIRI_EYE_IRIS    = (139,  94,  60)
MIRI_HAIRPIN     = ( 92,  58,  32)
MIRI_BLUSH       = (212, 149, 107)

# Luma palette
LUMA_SKIN        = (200, 136,  90)
LUMA_SKIN_SH     = (164, 100,  60)
LUMA_HAIR        = ( 44,  28,  18)
LUMA_HOODIE      = (232, 114,  42)
LUMA_HOODIE_SH   = (180,  76,  20)
LUMA_JEANS       = ( 72,  96, 138)
LUMA_JEANS_SH    = ( 52,  72, 110)
LUMA_SHOES       = ( 52,  36,  24)
LUMA_EYE_IRIS    = (200, 125,  62)

SPEC_WHITE       = (248, 248, 240)


# ── Utility ────────────────────────────────────────────────────────────────────

def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def alpha_overlay_rect(img, x1, y1, x2, y2, color, alpha):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([x1, y1, x2, y2], fill=(*color, alpha))
    out = Image.alpha_composite(img.convert("RGBA"), layer)
    return out.convert("RGB")


def arc_pts(cx, cy, rx, ry, a0, a1, steps=40):
    pts = []
    for i in range(steps + 1):
        t = a0 + (a1 - a0) * i / steps
        r = math.radians(t)
        pts.append((int(cx + rx * math.cos(r)), int(cy + ry * math.sin(r))))
    return pts


def polyline(draw, pts, color, width=2):
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill=color, width=width)


# ── Background: Living Room Simplified ────────────────────────────────────────

def draw_background(img):
    """
    Simplified living room for style frame — key elements only.
    Perspective: mild 3/4, vp slightly right of center, elevated.
    Back wall center, floor in foreground, warm/cool split.
    """
    draw = ImageDraw.Draw(img)

    # Vanishing point
    vp_x = int(W * 0.52)
    vp_y = int(H * 0.38)

    # Back wall bounding box
    bw_left  = int(W * 0.04)
    bw_top   = int(H * 0.08)
    bw_right = int(W * 0.96)
    bw_bot   = int(H * 0.62)

    # Ceiling
    draw.rectangle([0, 0, W, bw_top], fill=CEILING_WARM)

    # Back wall fill
    draw.rectangle([bw_left, bw_top, bw_right, bw_bot], fill=WALL_BASE)

    # Left side wall (receding, warm shadow)
    draw.polygon([0, bw_top, bw_left, bw_top, bw_left, bw_bot, 0, H],
                 fill=WALL_SHADOW)

    # Right side wall
    draw.polygon([bw_right, bw_top, W, bw_top, W, H, bw_right, bw_bot],
                 fill=lerp_color(WALL_BASE, WALL_SHADOW, 0.4))

    # Baseboard on back wall
    draw.rectangle([bw_left, bw_bot - 8, bw_right, bw_bot], fill=AGED_CREAM)
    draw.line([(bw_left, bw_bot - 8), (bw_right, bw_bot - 8)], fill=LINE_DARK, width=1)

    # Floor
    for y in range(bw_bot, H + 4, 8):
        t = (y - bw_bot) / max(1, H - bw_bot)
        col = lerp_color(FLOOR_OAK_MED, FLOOR_OAK_DARK, t * 0.5)
        draw.line([(0, y), (W, y)], fill=col)

    # Floor planks (perspective lines from vp)
    for px in range(0, W + 80, 80):
        draw.line([(vp_x, bw_bot), (px, H)], fill=FLOOR_OAK_DARK, width=1)

    # Area rug (warm red, foreground center)
    rug_pts = [
        (int(W * 0.10), H),
        (int(W * 0.90), H),
        (int(W * 0.80), int(H * 0.76)),
        (int(W * 0.20), int(H * 0.76)),
    ]
    draw.polygon(rug_pts, fill=FLOOR_RUG_RED)
    draw.polygon(rug_pts, outline=FLOOR_RUG_EDGE, width=3)

    # Rug inner border (decorative)
    inner = [
        (int(W * 0.15), H - 6),
        (int(W * 0.85), H - 6),
        (int(W * 0.77), int(H * 0.78)),
        (int(W * 0.23), int(H * 0.78)),
    ]
    draw.polygon(inner, outline=lerp_color(FLOOR_RUG_RED, AGED_CREAM, 0.35), width=2)

    # Warm wallpaper texture hint
    for y in range(bw_top + 4, bw_bot - 8, 18):
        if (y // 18) % 3 == 0:
            draw.line([(bw_left, y), (bw_right, y)],
                      fill=(*AGED_CREAM, ), width=1)

    # Family photos suggestion — upper back wall, L and R of CRT
    for px, pw in [(int(W * 0.18), 42), (int(W * 0.30), 30), (int(W * 0.76), 36)]:
        py = int(H * 0.14)
        ph = int(pw * 0.75)
        draw.rectangle([px, py, px + pw, py + ph], fill=AGED_CREAM, outline=LINE_DARK, width=1)
        draw.rectangle([px + 3, py + 3, px + pw - 3, py + ph - 3],
                       fill=lerp_color(WALL_SHADOW, AGED_CREAM, 0.5))

    draw = ImageDraw.Draw(img)
    return draw, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot


# ── CRT Television ─────────────────────────────────────────────────────────────

def draw_crt_tv(img):
    """
    CRT — center composition. Screen ON. Warm plastic body.
    Smaller than living room env (style frame characters in FG).
    CRT sits on stand center-left of room.
    Returns screen bounds and TV body bounds.
    """
    draw = ImageDraw.Draw(img)

    # Stand
    stand_x1 = int(W * 0.36)
    stand_x2 = int(W * 0.64)
    stand_y1 = int(H * 0.57)
    stand_y2 = int(H * 0.63)

    draw.rectangle([stand_x1, stand_y1, stand_x2, stand_y2], fill=CRT_STAND_WOOD)
    draw.line([(stand_x1, stand_y1), (stand_x2, stand_y1)], fill=WOOD_LIGHT, width=2)
    draw.rectangle([stand_x1, stand_y1, stand_x2, stand_y2], outline=LINE_DARK, width=1)

    # TV body
    tv_x1 = stand_x1 + 10
    tv_x2 = stand_x2 - 10
    tv_y1 = int(H * 0.30)
    tv_y2 = stand_y1 + 8

    tv_w = tv_x2 - tv_x1
    tv_h = tv_y2 - tv_y1

    draw.rectangle([tv_x1, tv_y1, tv_x2, tv_y2], fill=CRT_PLASTIC)
    draw.rectangle([tv_x1, tv_y1, tv_x2, tv_y2], outline=LINE_DARK, width=2)

    # Plastic top highlight
    draw.line([(tv_x1 + 4, tv_y1 + 2), (tv_x2 - 4, tv_y1 + 2)],
              fill=lerp_color(CRT_PLASTIC, WARM_CREAM, 0.35), width=1)

    # Shadow bottom half
    draw.rectangle([tv_x1, tv_y1 + tv_h // 2, tv_x2, tv_y2], fill=CRT_PLASTIC_DARK)

    # Screen bezel
    bm_x = max(6, tv_w // 10)
    bm_y = max(5, tv_h // 10)
    bezel_x1 = tv_x1 + bm_x
    bezel_x2 = tv_x2 - bm_x
    bezel_y1 = tv_y1 + bm_y
    bezel_y2 = tv_y2 - int(tv_h * 0.28)

    draw.rectangle([bezel_x1, bezel_y1, bezel_x2, bezel_y2], fill=NEAR_BLACK_WARM)
    draw.rectangle([bezel_x1, bezel_y1, bezel_x2, bezel_y2], outline=LINE_DARK, width=1)

    # Screen
    scr_x1 = bezel_x1 + 4
    scr_x2 = bezel_x2 - 4
    scr_y1 = bezel_y1 + 3
    scr_y2 = bezel_y2 - 3
    scr_w = scr_x2 - scr_x1
    scr_h = scr_y2 - scr_y1

    # Screen gradient
    for y in range(scr_y1, scr_y2):
        t = (y - scr_y1) / max(1, scr_h)
        col = lerp_color((55, 130, 155), (18, 62, 80), t * 0.6)
        draw.line([(scr_x1, y), (scr_x2, y)], fill=col)

    # Scanlines
    for y in range(scr_y1, scr_y2, 3):
        draw.line([(scr_x1 + 1, y), (scr_x2 - 1, y)], fill=(8, 38, 52), width=1)

    # Screen glare
    gl_x1 = scr_x1 + int(scr_w * 0.06)
    gl_x2 = scr_x1 + int(scr_w * 0.22)
    gl_y1 = scr_y1 + int(scr_h * 0.06)
    gl_y2 = scr_y1 + int(scr_h * 0.18)
    draw.rectangle([gl_x1, gl_y1, gl_x2, gl_y2],
                   fill=lerp_color(CRT_SCREEN_GLOW, (200, 230, 238), 0.65))

    # Speaker grille
    gr_y1 = bezel_y2 + 3
    gr_y2 = tv_y2 - 8
    gr_x1 = tv_x1 + int(tv_w * 0.07)
    gr_x2 = tv_x1 + int(tv_w * 0.44)
    draw.rectangle([gr_x1, gr_y1, gr_x2, gr_y2], fill=CRT_PLASTIC_DARK)
    for gi in range(5):
        gx = gr_x1 + 3 + gi * 5
        if gx < gr_x2 - 3:
            draw.line([(gx, gr_y1 + 2), (gx, gr_y2 - 2)],
                      fill=lerp_color(CRT_PLASTIC_DARK, CRT_PLASTIC, 0.45), width=1)

    # Knobs
    kx_base = tv_x2 - int(tv_w * 0.20)
    ky_base = bezel_y2 + int((tv_y2 - bezel_y2) * 0.5)
    for ki in range(2):
        kx = kx_base + ki * 14
        draw.ellipse([kx - 5, ky_base - 5, kx + 5, ky_base + 5], fill=LINE_DARK)
        draw.ellipse([kx - 3, ky_base - 3, kx + 3, ky_base + 3], fill=WOOD_MED)

    # Antenna (rabbit ears)
    ant_cx = (tv_x1 + tv_x2) // 2
    ant_y  = tv_y1 - 2
    draw.line([(ant_cx - 4, ant_y), (ant_cx - 22, ant_y - 38)], fill=LINE_DARK, width=2)
    draw.line([(ant_cx + 4, ant_y), (ant_cx + 20, ant_y - 34)], fill=LINE_DARK, width=2)

    draw = ImageDraw.Draw(img)
    return scr_x1, scr_y1, scr_x2, scr_y2, tv_x1, tv_y1, tv_x2, tv_y2


def draw_crt_glow(img, scr_x1, scr_y1, scr_x2, scr_y2):
    """Cool CRT ambient spill — rightward and downward."""
    scr_cx = (scr_x1 + scr_x2) // 2
    scr_cy = (scr_y1 + scr_y2) // 2

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)

    for r in range(280, 20, -8):
        t = 1.0 - (r - 20) / 260.0
        alpha = int(t ** 2.0 * 48)
        gd.ellipse(
            [scr_cx - r, scr_cy - r // 2,
             scr_cx + r, scr_cy + r // 2],
            fill=(*CRT_COOL_SPILL, alpha)
        )

    out = Image.alpha_composite(img.convert("RGBA"), glow)
    return out.convert("RGB")


# ── Shoulder Involvement (C48 — codified C47 image-rules.md) ─────────────────
# When an arm moves past ~30 degrees from rest, the shoulder line must change.
# Per-character clothing reads: Miri = cardigan shoulder crease; Luma = hoodie
# fabric bunch. Implemented as torso polyline with deltoid bump vertices.

def _sf_shoulder_dy(arm_dy, arm_dx, mode="standard"):
    """Calculate shoulder displacement for style-frame characters.

    arm_dy: vertical displacement of arm endpoint from shoulder (negative = raised)
    arm_dx: horizontal displacement from shoulder (positive = extended outward)
    mode: "extended" for forward/outward reach, "neutral" for relaxed
    Returns (dy, dx_shift): dy is vertical shift (negative = up), dx is outward shift.
    """
    dy = 0
    dx = 0
    if mode == "extended":
        # Shoulder point shifts outward 4-6px and drops 1-2px for forward extension
        dy = -2
        dx = 5
    elif arm_dy < -10:
        # Raised arm: shoulder rises proportional to raise
        dy = max(-6, int(arm_dy * 0.20))
    return dy, dx


# ── Character Drawing ──────────────────────────────────────────────────────────
# Characters at style-frame scale.
# Head radius: HR = 42px (Miri), 46px (Luma) — readable faces at 1280×720.
# Ground line: GROUND_Y = int(H * 0.90)
# C48: Shoulder involvement applied per image-rules.md (Shoulder Involvement Rule).

GROUND_Y = int(H * 0.90)


# ─ Miri ───────────────────────────────────────────────────────────────────────

MIRI_HR = 42   # head radius
MIRI_HU = int(MIRI_HR * 2 * (1 / 1.0))  # HU = 2×HR (1 head = 2*radius)

def draw_miri_character(img, draw, cx, ground_y):
    """
    Grandma Miri — MIRI-A canonical. Standing, facing 3/4 right.
    Right hand extended forward/toward CRT (the "hand-off" gesture).
    Expression: WARM ATTENTION — soft smile, slightly forward lean.
    Height: 3.2 heads (MIRI_HU × 3.2).
    C49: Elder posture — forward lean + rounded shoulders.
    """
    HR = MIRI_HR
    HU = int(HR * 2)  # one head unit = 2 × head radius

    total_h = int(HU * 3.2)
    head_cy = ground_y - total_h + HR
    head_cx = cx

    # C49: ELDER POSTURE — forward lean (3-5 degrees from vertical).
    # Head shifts rightward (toward CRT/Luma) relative to feet.
    # Torso shifts proportionally less. Feet stay at cx.
    elder_lean_dx = int(HU * 0.04)   # ~3px at SF scale
    elder_sh_drop = 3                 # 3px shoulder drop (rounded shoulders)
    elder_sh_inward = 2               # 2px inward shift
    head_cx = cx + elder_lean_dx
    torso_cx = cx + int(elder_lean_dx * 0.6)

    # ── Body (weathered torso with shoulder involvement) ────────────────────
    torso_top_y  = head_cy + HR + int(HU * 0.08)   # neck gap
    torso_bot_y  = head_cy + HR + int(HU * 1.13)   # torso bottom
    torso_w_half = int(HU * 0.52)

    # C48: Shoulder displacement — Miri's right arm is extended toward CRT.
    # Left arm neutral: no displacement. Right arm forward: shoulder shifts out.
    l_sh_dy, l_sh_dx = _sf_shoulder_dy(0, 0, mode="neutral")
    r_sh_dy, r_sh_dx = _sf_shoulder_dy(0, int(HU * 0.62), mode="extended")
    sh_bump_w = int(HU * 0.07)  # deltoid bump width

    # C49: Apply elder shoulder drop + inward shift
    l_sh_dy += elder_sh_drop
    r_sh_dy += elder_sh_drop

    # Cardigan body fill — polyline torso with shoulder bumps
    torso_pts = [
        (torso_cx - torso_w_half - sh_bump_w + elder_sh_inward, torso_top_y),   # outer left shoulder (inward)
        (torso_cx - torso_w_half + l_sh_dx + elder_sh_inward, torso_top_y + l_sh_dy),  # left deltoid (dropped + inward)
        (torso_cx - int(torso_w_half * 0.3), torso_top_y),                       # inner left shoulder
        (torso_cx + int(torso_w_half * 0.3), torso_top_y),                       # inner right shoulder
        (torso_cx + torso_w_half + r_sh_dx - elder_sh_inward, torso_top_y + r_sh_dy),  # right deltoid (dropped + inward)
        (torso_cx + torso_w_half + sh_bump_w + r_sh_dx - elder_sh_inward, torso_top_y),  # outer right (inward)
        (cx + torso_w_half, torso_bot_y),                                         # bottom right (feet at cx)
        (cx - torso_w_half, torso_bot_y),                                         # bottom left (feet at cx)
    ]
    draw.polygon(torso_pts, fill=MIRI_CARDIGAN, outline=LINE_DARK, width=2)

    # Cardigan shadow (right side — warm light from left)
    shadow_x = torso_cx + int(torso_w_half * 0.35)
    draw.rectangle([shadow_x, torso_top_y + 4,
                    torso_cx + torso_w_half - 2, torso_bot_y],
                   fill=MIRI_CARD_SH)

    # Cardigan V-neck
    draw.line([(torso_cx - int(torso_w_half * 0.2), torso_top_y),
               (torso_cx, torso_top_y + int(HU * 0.18))],
              fill=LINE_DARK, width=2)
    draw.line([(torso_cx + int(torso_w_half * 0.2), torso_top_y),
               (torso_cx, torso_top_y + int(HU * 0.18))],
              fill=LINE_DARK, width=2)

    # Cable-knit texture suggestion
    for ky in range(torso_top_y + 12, torso_bot_y - 4, 10):
        draw.line([(torso_cx - torso_w_half + 6, ky), (torso_cx - torso_w_half + 6, ky + 5)],
                  fill=lerp_color(MIRI_CARDIGAN, MIRI_CARD_SH, 0.3), width=1)
        draw.line([(torso_cx - torso_w_half + 14, ky), (torso_cx - torso_w_half + 14, ky + 5)],
                  fill=lerp_color(MIRI_CARDIGAN, MIRI_CARD_SH, 0.3), width=1)

    # ── Left arm (neutral — slightly bent, toward body) ───────────────────────
    la_shoulder = (torso_cx - torso_w_half, torso_top_y + int(HU * 0.10))
    la_elbow    = (torso_cx - torso_w_half - int(HU * 0.18), torso_top_y + int(HU * 0.45))
    la_hand     = (torso_cx - torso_w_half - int(HU * 0.08), torso_top_y + int(HU * 0.80))
    polyline(draw, [la_shoulder, la_elbow, la_hand], MIRI_CARDIGAN, width=10)
    polyline(draw, [la_shoulder, la_elbow, la_hand], LINE_DARK, width=2)

    # ── Right arm extended TOWARD CRT (the hand-off gesture) ─────────────────
    # Arm reaches rightward and slightly forward
    ra_shoulder = (torso_cx + torso_w_half, torso_top_y + int(HU * 0.10))
    ra_elbow    = (torso_cx + torso_w_half + int(HU * 0.35), torso_top_y + int(HU * 0.28))
    ra_hand     = (torso_cx + torso_w_half + int(HU * 0.62), torso_top_y + int(HU * 0.44))
    polyline(draw, [ra_shoulder, ra_elbow, ra_hand], MIRI_CARDIGAN, width=10)
    polyline(draw, [ra_shoulder, ra_elbow, ra_hand], LINE_DARK, width=2)

    # Hand (mitten-style oval)
    draw.ellipse([ra_hand[0] - 9, ra_hand[1] - 8,
                  ra_hand[0] + 12, ra_hand[1] + 7],
                 fill=MIRI_SKIN, outline=LINE_DARK, width=2)
    # Knuckle line (Miri's working hands)
    draw.line([(ra_hand[0] - 3, ra_hand[1] + 1),
               (ra_hand[0] + 9, ra_hand[1] + 1)],
              fill=MIRI_SKIN_SH, width=1)

    # ── Legs ──────────────────────────────────────────────────────────────────
    leg_top_y = torso_bot_y
    leg_bot_y = ground_y
    leg_half_w = int(HU * 0.16)

    # Left leg
    draw.rectangle([cx - leg_half_w * 2 - 4, leg_top_y,
                    cx - 3, leg_bot_y],
                   fill=MIRI_PANTS, outline=LINE_DARK, width=1)
    # Right leg
    draw.rectangle([cx + 3, leg_top_y,
                    cx + leg_half_w * 2 + 4, leg_bot_y],
                   fill=MIRI_PANTS, outline=LINE_DARK, width=1)

    # Slippers
    slipper_w = int(HU * 0.28)
    slipper_h = int(HU * 0.10)
    for sx in [cx - leg_half_w * 2 + int(HU * 0.04),
               cx + 3]:
        draw.ellipse([sx - 2, ground_y - slipper_h,
                      sx + slipper_w, ground_y + 3],
                     fill=MIRI_SLIPPER, outline=LINE_DARK, width=1)

    # ── Head ──────────────────────────────────────────────────────────────────
    # Slightly offset right for 3/4 pose
    face_cx = head_cx + int(HR * 0.06)
    face_cy = head_cy

    # Neck — connects head (at head_cx) to torso (at torso_cx)
    neck_cx = (head_cx + torso_cx) // 2
    draw.rectangle([neck_cx - int(HR * 0.18), head_cy + int(HR * 0.80),
                    neck_cx + int(HR * 0.18), head_cy + HR + int(HU * 0.10)],
                   fill=MIRI_SKIN)

    # Head circle
    draw.ellipse([face_cx - HR, face_cy - int(HR * 0.94),
                  face_cx + HR, face_cy + int(HR * 0.94)],
                 fill=MIRI_SKIN, outline=LINE_DARK, width=2)

    # Chin shadow
    draw.ellipse([face_cx - int(HR * 0.9), face_cy + int(HR * 0.4),
                  face_cx + int(HR * 0.7), face_cy + int(HR * 0.94)],
                 fill=MIRI_SKIN_SH)

    # ── Ears ──────────────────────────────────────────────────────────────────
    ear_y = face_cy + int(HR * 0.06)
    er = int(HR * 0.12)
    draw.ellipse([face_cx - HR - er, ear_y - er, face_cx - HR + 2, ear_y + er],
                 fill=MIRI_SKIN, outline=LINE_DARK, width=1)
    draw.ellipse([face_cx + HR - 2, ear_y - er, face_cx + HR + er, ear_y + er],
                 fill=MIRI_SKIN, outline=LINE_DARK, width=1)

    # ── Hair bun ──────────────────────────────────────────────────────────────
    bun_cx = face_cx + int(HR * 0.08)
    bun_cy = face_cy - int(HR * 0.88)
    bun_rx = int(HR * 0.52)
    bun_ry = int(HR * 0.50)

    # Base hair (covers top of head)
    draw.ellipse([face_cx - HR, face_cy - int(HR * 0.94),
                  face_cx + HR, face_cy - int(HR * 0.30)],
                 fill=MIRI_HAIR)
    draw.line([(face_cx - HR, face_cy - int(HR * 0.62)),
               (face_cx + HR, face_cy - int(HR * 0.62))],
              fill=MIRI_HAIR, width=2)

    # Bun
    draw.ellipse([bun_cx - bun_rx, bun_cy - bun_ry,
                  bun_cx + bun_rx, bun_cy + bun_ry],
                 fill=MIRI_HAIR, outline=LINE_DARK, width=1)

    # Bun highlight
    draw.arc([bun_cx - bun_rx + 3, bun_cy - bun_ry + 3,
              bun_cx + int(bun_rx * 0.5), bun_cy + int(bun_ry * 0.35)],
             start=200, end=330,
             fill=lerp_color(MIRI_HAIR, WARM_CREAM, 0.5), width=1)

    # Bun shadow underside
    draw.arc([bun_cx - bun_rx + 2, bun_cy + 2,
              bun_cx + bun_rx - 2, bun_cy + bun_ry],
             start=0, end=180, fill=MIRI_HAIR_SH, width=2)

    # ── Wooden hairpins ───────────────────────────────────────────────────────
    hairpin_x1 = bun_cx - int(bun_rx * 0.32)
    hairpin_x2 = bun_cx + int(bun_rx * 0.24)
    draw.line([(hairpin_x1, bun_cy - bun_ry - int(HR * 0.18)),
               (hairpin_x1 + 5, bun_cy + bun_ry + int(HR * 0.08))],
              fill=MIRI_HAIRPIN, width=3)
    draw.line([(hairpin_x2, bun_cy - bun_ry - int(HR * 0.14)),
               (hairpin_x2 + 5, bun_cy + bun_ry + int(HR * 0.06))],
              fill=MIRI_HAIRPIN, width=3)

    # Escaping strands
    for dx, dy_end in [(-int(HR * 0.82), int(HR * 0.18)), (-int(HR * 0.68), int(HR * 0.32))]:
        draw.line([(face_cx + dx, face_cy - int(HR * 0.60)),
                   (face_cx + dx - 6, face_cy + dy_end)],
                  fill=MIRI_HAIR, width=1)

    # ── Face features ─────────────────────────────────────────────────────────
    # Eyebrows (warm gray, gentle arch)
    brow_y = face_cy - int(HR * 0.40)
    ew     = int(HR * 0.28)
    brow_col = (138, 122, 112)
    # Left brow
    polyline(draw, [
        (face_cx - ew - 2, brow_y + 2),
        (face_cx - ew // 2, brow_y - 2),
        (face_cx + 2, brow_y)
    ], brow_col, width=2)
    # Right brow
    polyline(draw, [
        (face_cx + 4, brow_y),
        (face_cx + ew // 2, brow_y - 3),
        (face_cx + ew + 2, brow_y + 2)
    ], brow_col, width=2)

    # Eyes (rounded almond, WARM ATTENTION — 80% aperture)
    eye_y  = face_cy + int(HR * 0.10)
    eye_rx = int(HR * 0.19)
    eye_ry = int(HR * 0.12)
    # Left eye
    lex = face_cx - int(HR * 0.32)
    draw.ellipse([lex - eye_rx, eye_y - eye_ry, lex + eye_rx, eye_y + eye_ry],
                 fill=(248, 240, 220), outline=LINE_DARK, width=1)
    draw.ellipse([lex - int(eye_rx * 0.55), eye_y - int(eye_ry * 0.55),
                  lex + int(eye_rx * 0.55), eye_y + int(eye_ry * 0.55)],
                 fill=MIRI_EYE_IRIS)
    draw.ellipse([lex - int(eye_rx * 0.28), eye_y - int(eye_ry * 0.28),
                  lex + int(eye_rx * 0.28), eye_y + int(eye_ry * 0.28)],
                 fill=LINE_DARK)
    draw.ellipse([lex - int(eye_rx * 0.45), eye_y - int(eye_ry * 0.38),
                  lex - int(eye_rx * 0.25), eye_y - int(eye_ry * 0.12)],
                 fill=SPEC_WHITE)

    # Right eye (slightly narrower in 3/4 — attentive)
    rex = face_cx + int(HR * 0.24)
    r_rx = int(eye_rx * 0.88)
    draw.ellipse([rex - r_rx, eye_y - eye_ry, rex + r_rx, eye_y + eye_ry],
                 fill=(248, 240, 220), outline=LINE_DARK, width=1)
    draw.ellipse([rex - int(r_rx * 0.55), eye_y - int(eye_ry * 0.55),
                  rex + int(r_rx * 0.55), eye_y + int(eye_ry * 0.55)],
                 fill=MIRI_EYE_IRIS)
    draw.ellipse([rex - int(r_rx * 0.28), eye_y - int(eye_ry * 0.28),
                  rex + int(r_rx * 0.28), eye_y + int(eye_ry * 0.28)],
                 fill=LINE_DARK)
    draw.ellipse([rex - int(r_rx * 0.44), eye_y - int(eye_ry * 0.36),
                  rex - int(r_rx * 0.22), eye_y - int(eye_ry * 0.10)],
                 fill=SPEC_WHITE)

    # Crow's feet (right eye outer corner)
    cfe_x = rex + r_rx
    cfe_y = eye_y
    crow_col = lerp_color(MIRI_SKIN, LINE_DARK, 0.35)
    draw.line([(cfe_x, cfe_y - 1), (cfe_x + 4, cfe_y - 4)], fill=crow_col, width=1)
    draw.line([(cfe_x, cfe_y + 1), (cfe_x + 4, cfe_y + 3)], fill=crow_col, width=1)
    # Left eye outer corner
    cfl_x = lex - eye_rx
    draw.line([(cfl_x, cfe_y - 1), (cfl_x - 4, cfe_y - 4)], fill=crow_col, width=1)
    draw.line([(cfl_x, cfe_y + 1), (cfl_x - 4, cfe_y + 3)], fill=crow_col, width=1)

    # Nose
    ny = face_cy + int(HR * 0.30)
    draw.arc([face_cx - int(HR * 0.12), ny, face_cx + int(HR * 0.14), ny + int(HR * 0.10)],
             start=190, end=350, fill=MIRI_SKIN_SH, width=1)

    # Mouth (WARM ATTENTION — gentle closed smile)
    my = face_cy + int(HR * 0.54)
    mw = int(HR * 0.32)
    polyline(draw, [
        (face_cx - mw, my + 2),
        (face_cx - mw // 2, my),
        (face_cx + mw // 2, my),
        (face_cx + mw, my + 2),
    ], LINE_DARK, width=2)

    # Permanent blush (direct fill — simplified, no alpha composite needed at this scale)
    for (bx, by) in [(face_cx - int(HR * 0.42), eye_y + int(HR * 0.14)),
                     (face_cx + int(HR * 0.30), eye_y + int(HR * 0.14))]:
        br = int(HR * 0.24)
        blush_col = lerp_color(MIRI_SKIN, MIRI_BLUSH, 0.55)
        draw.ellipse([bx - br, by - int(br * 0.6), bx + br, by + int(br * 0.6)],
                     fill=blush_col)

    # ── Shadow at feet ────────────────────────────────────────────────────────
    draw.ellipse([cx - int(HU * 0.55), ground_y - 4,
                  cx + int(HU * 0.55), ground_y + 10],
                 fill=lerp_color(FLOOR_OAK_DARK, NEAR_BLACK_WARM, 0.55))
    draw = ImageDraw.Draw(img)

    return img, draw


# ─ Luma ───────────────────────────────────────────────────────────────────────

LUMA_HR = 46   # head radius
LUMA_HU = int(LUMA_HR * 2)


def draw_luma_character(img, draw, cx, ground_y):
    """
    Luma — ATTENTIVE CURIOSITY. Standing, 3/4 left (facing Miri and CRT).
    Slight forward lean: she is being shown something and she is very interested.
    Expression: FOCUSED DETERMINATION / attentive (eyes wide, eyebrows neutral-raised).
    Height: 3.5 heads.
    """
    HR = LUMA_HR
    HU = LUMA_HU

    total_h = int(HU * 3.5)
    head_cy = ground_y - total_h + HR
    head_cx = cx

    # Forward lean: shift upper body left (toward Miri+CRT)
    lean_dx = -int(HU * 0.06)

    # ── Body (hoodie with shoulder involvement) ─────────────────────────────────
    torso_cx     = cx + lean_dx
    torso_top_y  = head_cy + HR + int(HU * 0.08)
    torso_bot_y  = head_cy + HR + int(HU * 1.10)
    torso_w_half = int(HU * 0.44)

    # C48: Shoulder displacement — Luma's left arm slightly raised (curious lean),
    # right arm forward/outward toward CRT direction.
    # Left arm dy: elbow at 0.40 HU below shoulder -> moderate raise
    l_arm_dy = int(HU * 0.40) - int(HU * 0.08)  # elbow y relative to shoulder
    l_sh_dy, l_sh_dx = _sf_shoulder_dy(-abs(int(HU * 0.12)), 0, mode="standard")
    # Right arm: forward/outward
    r_sh_dy, r_sh_dx = _sf_shoulder_dy(0, int(HU * 0.10), mode="extended")
    sh_bump_w = int(HU * 0.06)  # hoodie fabric bunch width

    # Hoodie torso — polyline with shoulder bumps
    torso_pts = [
        (torso_cx - torso_w_half - sh_bump_w, torso_top_y),              # outer left shoulder
        (torso_cx - torso_w_half + l_sh_dx, torso_top_y + l_sh_dy),     # left deltoid peak (slight raise)
        (torso_cx - int(torso_w_half * 0.3), torso_top_y),               # inner left shoulder
        (torso_cx + int(torso_w_half * 0.3), torso_top_y),               # inner right shoulder
        (torso_cx + torso_w_half + r_sh_dx, torso_top_y + r_sh_dy),     # right deltoid peak
        (torso_cx + torso_w_half + sh_bump_w + r_sh_dx, torso_top_y),   # outer right shoulder
        (torso_cx + torso_w_half, torso_bot_y),                           # bottom right
        (torso_cx - torso_w_half, torso_bot_y),                           # bottom left
    ]
    draw.polygon(torso_pts, fill=LUMA_HOODIE, outline=LINE_DARK, width=2)

    # Shadow (right side — CRT cool light from right, warm from left)
    shadow_x = torso_cx - int(torso_w_half * 0.30)
    draw.rectangle([torso_cx - torso_w_half + 2, torso_top_y + 4,
                    shadow_x, torso_bot_y],
                   fill=LUMA_HOODIE_SH)

    # Hoodie kangaroo pocket
    pock_y1 = torso_bot_y - int(HU * 0.30)
    pock_y2 = torso_bot_y - int(HU * 0.04)
    pock_x1 = torso_cx - int(torso_w_half * 0.55)
    pock_x2 = torso_cx + int(torso_w_half * 0.55)
    draw.rectangle([pock_x1, pock_y1, pock_x2, pock_y2],
                   fill=LUMA_HOODIE_SH, outline=LINE_DARK, width=1)
    draw.line([(torso_cx, pock_y1), (torso_cx, pock_y2)],
              fill=LINE_DARK, width=1)

    # ── Left arm (raised slightly — curious lean forward, one arm up) ─────────
    la_shoulder = (torso_cx - torso_w_half, torso_top_y + int(HU * 0.08))
    la_elbow    = (torso_cx - torso_w_half - int(HU * 0.28), torso_top_y + int(HU * 0.40))
    la_hand     = (torso_cx - torso_w_half - int(HU * 0.14), torso_top_y + int(HU * 0.72))
    polyline(draw, [la_shoulder, la_elbow, la_hand], LUMA_HOODIE, width=11)
    polyline(draw, [la_shoulder, la_elbow, la_hand], LINE_DARK, width=2)
    # Hand
    draw.ellipse([la_hand[0] - 10, la_hand[1] - 9,
                  la_hand[0] + 8, la_hand[1] + 8],
                 fill=LUMA_SKIN, outline=LINE_DARK, width=2)

    # ── Right arm (forward/outward — open, curious, toward CRT direction) ─────
    ra_shoulder = (torso_cx + torso_w_half, torso_top_y + int(HU * 0.08))
    ra_elbow    = (torso_cx + torso_w_half + int(HU * 0.10), torso_top_y + int(HU * 0.38))
    ra_hand     = (torso_cx + torso_w_half - int(HU * 0.04), torso_top_y + int(HU * 0.72))
    polyline(draw, [ra_shoulder, ra_elbow, ra_hand], LUMA_HOODIE, width=11)
    polyline(draw, [ra_shoulder, ra_elbow, ra_hand], LINE_DARK, width=2)
    draw.ellipse([ra_hand[0] - 9, ra_hand[1] - 9,
                  ra_hand[0] + 9, ra_hand[1] + 8],
                 fill=LUMA_SKIN, outline=LINE_DARK, width=2)

    # ── Legs (column-wide, jeans) ─────────────────────────────────────────────
    leg_top_y = torso_bot_y
    leg_bot_y = ground_y
    leg_hw    = int(HU * 0.15)

    # Slight lean: shift legs right of torso center
    leg_cx = cx + int(lean_dx * 0.3)
    draw.rectangle([leg_cx - leg_hw * 2 - 3, leg_top_y,
                    leg_cx - 2, leg_bot_y],
                   fill=LUMA_JEANS, outline=LINE_DARK, width=1)
    draw.rectangle([leg_cx + 2, leg_top_y,
                    leg_cx + leg_hw * 2 + 3, leg_bot_y],
                   fill=LUMA_JEANS, outline=LINE_DARK, width=1)
    # Jeans shadow
    draw.rectangle([leg_cx - leg_hw * 2 - 3, leg_top_y,
                    leg_cx - leg_hw, leg_bot_y],
                   fill=LUMA_JEANS_SH)

    # Shoes
    shoe_w = int(HU * 0.26)
    shoe_h = int(HU * 0.11)
    for sx in [leg_cx - leg_hw * 2 + int(HU * 0.02),
               leg_cx + 2]:
        draw.ellipse([sx - 2, ground_y - shoe_h,
                      sx + shoe_w, ground_y + 4],
                     fill=LUMA_SHOES, outline=LINE_DARK, width=1)

    # ── Head ──────────────────────────────────────────────────────────────────
    face_cx = head_cx + lean_dx - int(HR * 0.04)
    face_cy = head_cy

    # Neck
    draw.rectangle([face_cx - int(HR * 0.18), face_cy + int(HR * 0.80),
                    face_cx + int(HR * 0.18), face_cy + HR + int(HU * 0.10)],
                   fill=LUMA_SKIN)

    # Head circle (95% circular)
    draw.ellipse([face_cx - HR, face_cy - HR,
                  face_cx + HR, face_cy + HR],
                 fill=LUMA_SKIN, outline=LINE_DARK, width=2)

    # Chin shadow (slight)
    draw.ellipse([face_cx - int(HR * 0.88), face_cy + int(HR * 0.5),
                  face_cx + int(HR * 0.80), face_cy + HR],
                 fill=LUMA_SKIN_SH)

    # ── Hair (dark brown cloud, 5 curls) ──────────────────────────────────────
    hair_top_y = face_cy - int(HR * 1.18)
    # Main hair mass
    draw.ellipse([face_cx - int(HR * 1.02), hair_top_y,
                  face_cx + int(HR * 1.02), face_cy - int(HR * 0.32)],
                 fill=LUMA_HAIR)

    # Curl bumps (5 curls radiating top and sides)
    curl_specs = [
        (face_cx - int(HR * 0.72), face_cy - int(HR * 1.14), int(HR * 0.24)),
        (face_cx - int(HR * 0.22), face_cy - int(HR * 1.22), int(HR * 0.26)),
        (face_cx + int(HR * 0.30), face_cy - int(HR * 1.18), int(HR * 0.22)),
        (face_cx + int(HR * 0.78), face_cy - int(HR * 0.96), int(HR * 0.20)),
        (face_cx - int(HR * 0.95), face_cy - int(HR * 0.72), int(HR * 0.18)),
    ]
    for (ccx, ccy, cr) in curl_specs:
        draw.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=LUMA_HAIR)

    # Hair outline
    draw.arc([face_cx - int(HR * 1.02), hair_top_y,
              face_cx + int(HR * 1.02), face_cy - int(HR * 0.32)],
             start=180, end=360, fill=LINE_DARK, width=1)

    # ── Face features ─────────────────────────────────────────────────────────
    # Eyebrows (thick graphic brows — raised/neutral, curious)
    brow_y = face_cy - int(HR * 0.44)
    bw     = int(HR * 0.30)
    # Left brow (further from 3/4 center — slightly narrower)
    draw.rectangle([face_cx - bw - 2, brow_y - 3,
                    face_cx - 4, brow_y],
                   fill=LUMA_HAIR)
    # Right brow
    draw.rectangle([face_cx + 6, brow_y - 3,
                    face_cx + bw + 2, brow_y],
                   fill=LUMA_HAIR)

    # Eyes (ATTENTIVE — both open, slight left-facing gaze)
    eye_y  = face_cy - int(HR * 0.10)
    eye_rx = int(HR * 0.20)
    eye_ry = int(HR * 0.16)

    # Left eye
    lex = face_cx - int(HR * 0.34)
    draw.ellipse([lex - eye_rx, eye_y - eye_ry, lex + eye_rx, eye_y + eye_ry],
                 fill=(250, 242, 222), outline=LINE_DARK, width=2)
    draw.ellipse([lex - int(eye_rx * 0.58), eye_y - int(eye_ry * 0.58),
                  lex + int(eye_rx * 0.58), eye_y + int(eye_ry * 0.58)],
                 fill=LUMA_EYE_IRIS)
    draw.ellipse([lex - int(eye_rx * 0.30), eye_y - int(eye_ry * 0.30),
                  lex + int(eye_rx * 0.30), eye_y + int(eye_ry * 0.30)],
                 fill=LINE_DARK)
    draw.ellipse([lex - int(eye_rx * 0.48), eye_y - int(eye_ry * 0.42),
                  lex - int(eye_rx * 0.24), eye_y - int(eye_ry * 0.12)],
                 fill=SPEC_WHITE)

    # Right eye (slightly smaller — 3/4 perspective)
    rex = face_cx + int(HR * 0.26)
    r_rx = int(eye_rx * 0.86)
    draw.ellipse([rex - r_rx, eye_y - eye_ry, rex + r_rx, eye_y + eye_ry],
                 fill=(250, 242, 222), outline=LINE_DARK, width=2)
    draw.ellipse([rex - int(r_rx * 0.55), eye_y - int(eye_ry * 0.55),
                  rex + int(r_rx * 0.55), eye_y + int(eye_ry * 0.55)],
                 fill=LUMA_EYE_IRIS)
    draw.ellipse([rex - int(r_rx * 0.28), eye_y - int(eye_ry * 0.28),
                  rex + int(r_rx * 0.28), eye_y + int(eye_ry * 0.28)],
                 fill=LINE_DARK)
    draw.ellipse([rex - int(r_rx * 0.44), eye_y - int(eye_ry * 0.40),
                  rex - int(r_rx * 0.20), eye_y - int(eye_ry * 0.12)],
                 fill=SPEC_WHITE)

    # Right eye — canonical upper lid drop (+6px per spec)
    draw.line([(rex - r_rx, eye_y - eye_ry + 6), (rex + r_rx, eye_y - eye_ry + 6)],
              fill=LINE_DARK, width=1)

    # Nose (apostrophe)
    ny = face_cy + int(HR * 0.22)
    draw.arc([face_cx, ny - 2, face_cx + int(HR * 0.12), ny + int(HR * 0.08)],
             start=180, end=360, fill=LUMA_SKIN_SH, width=1)

    # Mouth (slight open smile — attentive curiosity, 'oh?' expression)
    my = face_cy + int(HR * 0.44)
    mw = int(HR * 0.30)
    polyline(draw, [
        (face_cx - mw, my + 4),
        (face_cx - mw // 2, my),
        (face_cx + mw // 2, my),
        (face_cx + mw, my + 4),
    ], LINE_DARK, width=2)
    # Slight open — lower lip hint
    draw.arc([face_cx - int(mw * 0.6), my,
              face_cx + int(mw * 0.6), my + int(HR * 0.14)],
             start=0, end=180, fill=LUMA_SKIN_SH, width=1)

    # ── Shadow at feet ────────────────────────────────────────────────────────
    draw.ellipse([cx - int(HU * 0.52), ground_y - 4,
                  cx + int(HU * 0.52), ground_y + 10],
                 fill=lerp_color(FLOOR_OAK_DARK, NEAR_BLACK_WARM, 0.55))
    draw = ImageDraw.Draw(img)

    return img, draw


# ── Lighting Passes ────────────────────────────────────────────────────────────

def draw_warm_lamp_glow(img):
    """Warm key light from left — Miri's side."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    lamp_cx = int(W * 0.12)
    lamp_cy = int(H * 0.25)
    for r in range(360, 20, -8):
        t = 1.0 - (r - 20) / 340.0
        alpha = int(t ** 2.0 * 40)
        ld.ellipse([lamp_cx - r, lamp_cy - r // 2,
                    lamp_cx + r, lamp_cy + r // 2],
                   fill=(*LAMP_WARM, alpha))
    out = Image.alpha_composite(img.convert("RGBA"), layer)
    return out.convert("RGB")


def draw_deep_shadow_pass(img):
    """Push corners and edges toward value floor ≤30."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    # Top left corner
    for x in range(0, int(W * 0.14)):
        t = max(0.0, 1.0 - x / (W * 0.14))
        ld.line([(x, 0), (x, int(H * 0.25))],
                fill=(*NEAR_BLACK_WARM, int(t ** 1.5 * 200)))
    # Top right corner
    for x in range(int(W * 0.86), W):
        t = max(0.0, (x - W * 0.86) / max(1, W * 0.14))
        ld.line([(x, 0), (x, int(H * 0.20))],
                fill=(*NEAR_BLACK_WARM, int(t ** 1.5 * 200)))
    # Floor depth vignette
    for y in range(int(H * 0.88), H):
        t = max(0.0, (y - H * 0.88) / max(1, H * 0.12))
        ld.line([(0, y), (W, y)],
                fill=(*NEAR_BLACK_WARM, int(t * 80)))
    out = Image.alpha_composite(img.convert("RGBA"), layer)
    return out.convert("RGB")


# ── Caption / Label ────────────────────────────────────────────────────────────

def draw_caption(img):
    """Minimal style frame label: title + scene ID bottom-left."""
    draw = ImageDraw.Draw(img)
    try:
        from PIL import ImageFont
        font = ImageFont.load_default()
    except Exception:
        font = None

    label = "SF06 — THE HAND-OFF  |  Miri + Luma + CRT  |  REAL WORLD  |  C48 Maya Santos"
    draw.rectangle([0, H - 22, W, H], fill=NEAR_BLACK_WARM)
    draw.text((8, H - 18), label, fill=AGED_CREAM, font=font)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    random.seed(44)

    out_dir = output_dir('color', 'style_frames')
    out_path = os.path.join(out_dir, "LTG_COLOR_sf_miri_luma_handoff.png")
    os.makedirs(out_dir, exist_ok=True)

    img = Image.new("RGB", (W, H), WALL_BASE)

    # Layer 1: Background room
    draw, vp_x, vp_y, bw_left, bw_top, bw_right, bw_bot = draw_background(img)

    # Layer 2: CRT — the central compositional object
    crt_result = draw_crt_tv(img)
    scr_x1, scr_y1, scr_x2, scr_y2, tv_x1, tv_y1, tv_x2, tv_y2 = crt_result
    draw = ImageDraw.Draw(img)

    # Layer 3: CRT cool glow (sets warm/cool right-side tone before characters)
    img = draw_crt_glow(img, scr_x1, scr_y1, scr_x2, scr_y2)
    draw = ImageDraw.Draw(img)

    # Layer 4: Warm lamp glow (Miri's left side)
    img = draw_warm_lamp_glow(img)
    draw = ImageDraw.Draw(img)

    # Layer 5: Miri — LEFT of CRT, facing right, hand extended toward TV
    # CRT center is at ~(int(W*0.50), ). Miri stands at x≈350.
    miri_cx = int(W * 0.285)
    img, draw = draw_miri_character(img, draw, miri_cx, GROUND_Y)
    draw = ImageDraw.Draw(img)

    # Layer 6: Luma — RIGHT of CRT, facing left/3/4, attentive lean
    # Luma is taller — stands at x≈800.
    luma_cx = int(W * 0.72)
    img, draw = draw_luma_character(img, draw, luma_cx, GROUND_Y)
    draw = ImageDraw.Draw(img)

    # Layer 7: Dual temperature overlay (warm left / cool right)
    img = alpha_overlay_rect(img, 0, 0, W // 2, H, SUNLIT_AMBER, 28)
    img = alpha_overlay_rect(img, W // 2, 0, W, H, CRT_COOL_SPILL, 32)
    draw = ImageDraw.Draw(img)

    # Layer 8: Deep shadow pass (value floor ≤30)
    img = draw_deep_shadow_pass(img)
    draw = ImageDraw.Draw(img)

    # Layer 9: Caption
    draw_caption(img)

    # Size rule compliance
    img.thumbnail((1280, 1280), Image.LANCZOS)
    img.save(out_path)
    print(f"[Maya C48] Saved: {out_path}  ({img.width}×{img.height}px)")
    print("  Composition: Miri (L) + CRT (C) + Luma (R) — The Hand-Off")
    print("  Palette: Real World only. No GL colors.")
    print("  C48: Shoulder involvement applied — Miri R shoulder forward pull, Luma L rise + R outward.")
    print("  Face test note: Luma face at sprint scale — visual inspection.")
    print("    Miri face at sprint scale — visual inspection (no automated gate for Miri).")


if __name__ == "__main__":
    main()
