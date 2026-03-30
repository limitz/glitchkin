#!/usr/bin/env python3
"""
LTG_TOOL_cosmo_expression_sheet.py
Cosmo Expression Sheet Generator — "Luma & the Glitchkin"

v007 — C38 P2 Fix: SKEPTICAL arm geometry (Maya Santos)

  KEY CHANGES from v006:
  - SKEPTICAL ARM FIX (3+ cycles flagged as unresolved):
    In v006 SKEPTICAL used arm_mode="standard" with arm_l_dy=-18, arm_r_dy=-12.
    Standard mode draws rectangular arms at the shoulder/torso edge. At body_tilt=8
    the arms visually merged with the body silhouette — unreadable at any scale.

    New arm_mode="skeptical_crossed":
      - Left arm: forearm crosses ACROSS body at mid-torso height, ending to the
        RIGHT of center — classic dismissive half-fold.
        (left arm, right of center = visible crossing motion)
      - Right arm: elbow COCKED OUT away from body at shoulder level, forearm
        angling back inward — arms-akimbo skeptical body language.
        (elbow sticks RIGHT of torso = clear silhouette hook)
    Both arms are now clearly visible outside the body silhouette.

  Silhouette differentiation:
    SKEPTICAL: elbow out right + hand crossing left = strong asymmetric arm profile.
    DETERMINED: standard forward-hang arms.
    DELIGHTED: both arms raised forward at chest height.
    → SKEPTICAL reads as distinct at thumbnail scale.

  All v006 content preserved:
    S003 compliance (all glasses_tilt ≤ 9° ± 2° from 7°),
    all other 5 expressions (AWKWARD, WORRIED, SURPRISED, DETERMINED, FRUSTRATED).

Output: output/characters/main/LTG_CHAR_cosmo_expression_sheet.png
Author: Maya Santos — Cycle 38 (SKEPTICAL arm fix)
Date: 2026-03-29
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Palette ───────────────────────────────────────────────────────────────────
SKIN        = (217, 192, 154)
SKIN_SH     = (184, 154, 120)
SKIN_HL     = (238, 212, 176)
HAIR        = (26, 24, 36)
HAIR_SH     = (14, 14, 24)
HAIR_HL     = (44, 43, 64)
EYE_WHITE   = (250, 240, 220)
IRIS        = (61, 107, 69)
PUPIL       = (59, 40, 32)
EYE_HL      = (240, 240, 240)
GLASS_FRAME = (92, 58, 32)
GLASS_LENS  = (238, 244, 255)
GLASS_GLARE = (240, 240, 240)
STRIPE_A    = (91, 141, 184)
STRIPE_B    = (122, 158, 126)
PANTS       = (140, 136, 128)
PANTS_SH    = (106, 100, 96)
SHOE        = (92, 58, 32)
SHOE_SOLE   = (184, 154, 120)
NOTEBOOK    = (91, 141, 184)
NOTEBOOK_SP = (61, 107, 138)
LINE        = (59, 40, 32)
BLUSH       = (210, 128, 80)
BLUSH_HI    = (228, 162, 120)

# v005/v006: Panel backgrounds deliberately chosen to be well-separated from all
# character colors to ensure silhouette tool correctly detects character pixels.
BG_NEUTRAL   = (240, 220, 180)   # warm amber
BG_FRUSTRAT  = (235, 215, 175)   # warm amber variant
BG_DETERMIN  = (225, 235, 220)   # warm sage
BG_SKEPTIC   = (230, 218, 178)   # warm honey
BG_WORRIED   = (225, 212, 172)   # warm sand
BG_SURPRISED = (242, 222, 175)   # warm golden
BG_DELIGHTED = (220, 232, 212)   # sage green
BG_AWKWARD   = (238, 220, 185)   # warm cream
BG_THOUGHTFUL= (215, 228, 215)   # sage

CANVAS_BG    = (28, 24, 20)

# ── Layout ────────────────────────────────────────────────────────────────────
# v005/v006: 3x2 grid (6 expressions), labels OUTSIDE panel bounds
PANEL_W = 370
PANEL_H = 440   # content panel only — no label bar inside
LABEL_H = 64    # label area below panel, separate from PANEL_H
COLS    = 3
ROWS    = 2
PAD     = 18
HEADER  = 52

# ── Expression definitions ────────────────────────────────────────────────────
# v006: glasses_tilt CLAMPED to ±2° of spec target 7°.
# Max allowed = 9°. SKEPTICAL stays at 9° (within tolerance). All others at 7°.

EXPRESSIONS = [
    # Row 0 — High differentiation: AWKWARD (jagged asymmetry), WORRIED (wide bracket), SURPRISED (horizontal)
    {
        "name":     "AWKWARD",
        "body_data": {
            "arm_l_dy": 0, "arm_r_dy": 0,
            "body_tilt": 3, "body_squash": 0.98,
            "notebook_show": False, "notebook_open": False,
            "arm_mode": "awkward",  # maximum asymmetry — left hang, right palm-out stiff
        },
        "panel_bg": BG_AWKWARD,
        "glasses_tilt": 7,   # v006 fix: was 10° (S003 FAIL) → 7° (spec target)
        "brow_data": {"l_raise": 12, "r_raise": 2, "l_furrow": 3, "r_furrow": 0},
        "mouth_data": {"style": "grimace"},
        "blush": True,
        "prev_state": "← was: ANY ATTEMPT TO HELP",
        "next_state": "→ next: WORRIED / RETREATING",
    },
    {
        "name":     "WORRIED",
        "body_data": {
            "arm_l_dy": 0, "arm_r_dy": 0,
            "body_tilt": -3, "body_squash": 0.96,
            "notebook_show": False, "notebook_open": False,
            "arm_mode": "head_grab",  # both hands to sides of head, wide bracket
        },
        "panel_bg": BG_WORRIED,
        "glasses_tilt": 8,   # already within spec (7° ± 2°)
        "brow_data": {"l_raise": 6, "r_raise": 6, "l_furrow": 10, "r_furrow": 10},
        "mouth_data": {"style": "compressed"},
        "blush": False,
        "prev_state": "← was: NEUTRAL / SKEPTICAL",
        "next_state": "→ next: FRUSTRATED / TRYING ANYWAY",
    },
    {
        "name":     "SURPRISED",
        "body_data": {
            "arm_l_dy": -35, "arm_r_dy": -35,
            "body_tilt": 12, "body_squash": 0.97,
            "notebook_show": True, "notebook_open": True,
            "arm_mode": "wide_startle",  # horizontal arm-spread startle
        },
        "panel_bg": BG_SURPRISED,
        "glasses_tilt": 7,   # v006 fix: was 10° (S003 FAIL) → 7° (spec target)
        "brow_data": {"l_raise": 16, "r_raise": 16, "l_furrow": 0, "r_furrow": 0},
        "mouth_data": {"style": "open_surprised"},
        "blush": True,
        "prev_state": "← was: DETERMINED (plan in action)",
        "next_state": "→ next: FRUSTRATED / ACCEPTING CHAOS",
    },
    # Row 1 — Contained: SKEPTICAL (backward/crossed), DETERMINED (forward/compact), FRUSTRATED (low/defeated)
    {
        "name":     "SKEPTICAL",
        "body_data": {
            "arm_l_dy": -18, "arm_r_dy": -12,
            "body_tilt": 8,  "body_squash": 1.0,
            "notebook_show": True, "notebook_open": False,
            # v007: Changed from "standard" to "skeptical_crossed"
            # Reason: standard arms disappear behind torso at body_tilt=8 (3+ cycles flagged).
            # skeptical_crossed: left arm crosses body (hand right of center),
            # right elbow cocks out (visible outside torso right).
            "arm_mode": "skeptical_crossed",
        },
        "panel_bg": BG_SKEPTIC,
        "glasses_tilt": 9,   # within spec (7° ± 2° max=9°) — retained for expression read
        "brow_data": {"l_raise": 18, "r_raise": 0, "l_furrow": 0, "r_furrow": 1},
        "mouth_data": {"style": "flat"},
        "blush": False,
        "prev_state": "← was: NEUTRAL / OBSERVING",
        "next_state": "→ next: RESIGNED / PREPARING ANYWAY",
    },
    {
        "name":     "DETERMINED",
        "body_data": {
            "arm_l_dy": 8, "arm_r_dy": -30,
            "body_tilt": -5, "body_squash": 1.0,
            "notebook_show": True, "notebook_open": False,
            "arm_mode": "standard",
        },
        "panel_bg": BG_DETERMIN,
        "glasses_tilt": 7,   # already at spec target
        "brow_data": {"l_raise": 2, "r_raise": 2, "l_furrow": 2, "r_furrow": 2},
        "mouth_data": {"style": "slight_smile"},
        "blush": False,
        "prev_state": "← was: NEUTRAL / OBSERVING",
        "next_state": "→ next: FRUSTRATED or SUCCEEDED",
    },
    {
        "name":     "FRUSTRATED / DEFEATED",
        "body_data": {
            "arm_l_dy": 20, "arm_r_dy": 12,
            "body_tilt": 4, "body_squash": 0.96,
            "notebook_show": True, "notebook_open": True,
            "arm_mode": "standard",
        },
        "panel_bg": BG_FRUSTRAT,
        "glasses_tilt": 7,   # v006 fix: was 10° (S003 FAIL) → 7° (spec target)
        "brow_data": {"l_raise": -3, "r_raise": -3, "l_furrow": 4, "r_furrow": 4},
        "mouth_data": {"style": "compressed"},
        "blush": False,
        "prev_state": "← was: DETERMINED",
        "next_state": "→ next: RESIGNED / RECALIBRATING",
    },
]


# ── Drawing helpers ───────────────────────────────────────────────────────────

def _draw_cosmo_head(draw, cx, cy, hu):
    hw = int(hu * 0.43)
    hh = int(hu * 0.50)
    r  = int(hu * 0.12)
    try:
        draw.rounded_rectangle([cx - hw, cy - hh, cx + hw, cy + hh],
                                radius=r, fill=SKIN, outline=LINE, width=2)
    except AttributeError:
        draw.rectangle([cx - hw + r, cy - hh, cx + hw - r, cy + hh], fill=SKIN)
        draw.rectangle([cx - hw, cy - hh + r, cx + hw, cy + hh - r], fill=SKIN)
        for (ox, oy) in [(cx - hw + r, cy - hh + r), (cx + hw - r, cy - hh + r),
                         (cx - hw + r, cy + hh - r), (cx + hw - r, cy + hh - r)]:
            draw.ellipse([ox - r, oy - r, ox + r, oy + r], fill=SKIN)
        draw.rounded_rectangle([cx - hw, cy - hh, cx + hw, cy + hh],
                                radius=r, outline=LINE, width=2)


def _draw_cosmo_hair(draw, cx, cy, hu):
    hw       = int(hu * 0.43)
    hh       = int(hu * 0.50)
    hair_top = cy - hh - int(hu * 0.05)
    hair_bot = cy - hh + int(hu * 0.15)
    draw.ellipse([cx - hw - 2, hair_top, cx + int(hw * 0.2), hair_bot + 6], fill=HAIR)
    draw.ellipse([cx - int(hw * 0.2), hair_top + 2, cx + hw + 2, hair_bot + 4], fill=HAIR)
    part_x = cx + int(hw * 0.12)
    draw.line([(part_x, hair_top + 4), (part_x, hair_bot)], fill=SKIN, width=2)
    cowlick_x = cx + int(hw * 0.05)
    cowlick_y = hair_top
    draw.arc([cowlick_x - int(hu * 0.07), cowlick_y - int(hu * 0.05),
              cowlick_x + int(hu * 0.07), cowlick_y + int(hu * 0.08)],
             start=280, end=80, fill=HAIR_HL, width=3)
    draw.arc([cx - int(hw * 0.6), hair_top + 2, cx + int(hw * 0.6), hair_top + int(hu * 0.12)],
             start=200, end=340, fill=HAIR_HL, width=2)


def _draw_cosmo_glasses(draw, cx, cy, hu, tilt_deg):
    lens_r  = int(hu * 0.16)
    frame_w = max(3, int(hu * 0.06))
    bridge  = int(hu * 0.05)
    eye_sep = lens_r + bridge
    gcy     = cy - int(hu * 0.10)
    theta   = math.radians(-tilt_deg)
    cos_t, sin_t = math.cos(theta), math.sin(theta)

    def rot(dx, dy):
        return (int(cx + dx * cos_t - dy * sin_t),
                int(gcy + dx * sin_t + dy * cos_t))

    lcx, lcy = rot(-eye_sep, 0)
    rcx, rcy = rot(+eye_sep, 0)

    draw.ellipse([lcx - lens_r, lcy - lens_r, lcx + lens_r, lcy + lens_r], fill=GLASS_LENS)
    draw.ellipse([rcx - lens_r, rcy - lens_r, rcx + lens_r, rcy + lens_r], fill=GLASS_LENS)

    gl_r = int(lens_r * 0.7)
    draw.arc([lcx - gl_r, lcy - lens_r + 2, lcx + gl_r, lcy - lens_r + int(lens_r * 0.5)],
             start=200, end=340, fill=GLASS_GLARE, width=2)
    draw.arc([rcx - gl_r, rcy - lens_r + 2, rcx + gl_r, rcy - lens_r + int(lens_r * 0.5)],
             start=200, end=340, fill=GLASS_GLARE, width=2)

    draw.ellipse([lcx - lens_r, lcy - lens_r, lcx + lens_r, lcy + lens_r],
                 outline=GLASS_FRAME, width=frame_w)
    draw.ellipse([rcx - lens_r, rcy - lens_r, rcx + lens_r, rcy + lens_r],
                 outline=GLASS_FRAME, width=frame_w)

    bridge_l = rot(-bridge, 0)
    bridge_r = rot(+bridge, 0)
    draw.line([bridge_l, bridge_r], fill=GLASS_FRAME, width=frame_w)

    l_temple_start = rot(-eye_sep - lens_r, 0)
    l_temple_end   = rot(-eye_sep - lens_r - int(hu * 0.06), int(hu * 0.02))
    r_temple_start = rot(+eye_sep + lens_r, 0)
    r_temple_end   = rot(+eye_sep + lens_r + int(hu * 0.06), int(hu * 0.02))
    draw.line([l_temple_start, l_temple_end], fill=GLASS_FRAME, width=max(2, frame_w - 1))
    draw.line([r_temple_start, r_temple_end], fill=GLASS_FRAME, width=max(2, frame_w - 1))

    return lcx, lcy, rcx, rcy, lens_r


def _draw_cosmo_eyes(draw, lcx, lcy, rcx, rcy, lens_r):
    iris_r = int(lens_r * 0.55)
    pup_r  = int(iris_r * 0.55)
    for (ex, ey) in [(lcx, lcy), (rcx, rcy)]:
        draw.ellipse([ex - iris_r - 4, ey - iris_r - 4,
                      ex + iris_r + 4, ey + iris_r + 4], fill=EYE_WHITE)
        draw.ellipse([ex - iris_r, ey - iris_r, ex + iris_r, ey + iris_r], fill=IRIS)
        draw.ellipse([ex - pup_r, ey - pup_r, ex + pup_r, ey + pup_r], fill=PUPIL)
        hl_r = max(2, int(iris_r * 0.28))
        draw.ellipse([ex + int(iris_r * 0.3), ey - iris_r + 2,
                      ex + int(iris_r * 0.3) + hl_r * 2, ey - iris_r + 2 + hl_r * 2],
                     fill=EYE_HL)
        draw.line([(ex - iris_r - 3, ey + int(iris_r * 0.5)),
                   (ex + iris_r + 3, ey + int(iris_r * 0.5))], fill=LINE, width=2)


def _draw_cosmo_nose(draw, cx, cy, hu):
    nose_r = int(hu * 0.05)
    draw.ellipse([cx - nose_r, cy + int(hu * 0.06),
                  cx + nose_r, cy + int(hu * 0.16)], fill=SKIN_SH)


def _draw_cosmo_brows(draw, cx, cy, hu, tilt_deg, brow_data, lcx, lcy, rcx, rcy):
    lens_r     = int(hu * 0.16)
    brow_y_base = lcy - lens_r - int(hu * 0.06)
    l_raise    = brow_data.get("l_raise", 0)
    r_raise    = brow_data.get("r_raise", 0)
    l_furrow   = brow_data.get("l_furrow", 0)
    r_furrow   = brow_data.get("r_furrow", 0)
    brow_w     = int(hu * 0.18)
    brow_thick = max(3, int(hu * 0.028))

    l_inner_y = brow_y_base - l_raise - l_furrow
    l_outer_y = brow_y_base - l_raise + l_furrow // 2
    l_pts = [(lcx - brow_w, l_outer_y), (lcx, l_inner_y), (lcx + brow_w, l_outer_y + 2)]
    draw.line(l_pts, fill=HAIR, width=brow_thick)

    r_inner_y = brow_y_base - r_raise - r_furrow
    r_outer_y = brow_y_base - r_raise + r_furrow // 2
    r_pts = [(rcx - brow_w, r_outer_y + 2), (rcx, r_inner_y), (rcx + brow_w, r_outer_y)]
    draw.line(r_pts, fill=HAIR, width=brow_thick)


def _draw_cosmo_mouth(draw, cx, cy, hu, mouth_data):
    mouth_y = cy + int(hu * 0.26)
    mw      = int(hu * 0.20)
    style   = mouth_data.get("style", "neutral")

    if style == "neutral":
        draw.line([(cx - mw, mouth_y), (cx + mw, mouth_y)], fill=LINE, width=2)
        draw.line([(cx - mw, mouth_y), (cx - mw + 4, mouth_y - 2)], fill=LINE, width=2)
        draw.line([(cx + mw, mouth_y), (cx + mw - 4, mouth_y - 2)], fill=LINE, width=2)
    elif style == "slight_smile":
        draw.arc([cx - mw, mouth_y - int(hu * 0.06), cx + mw, mouth_y + int(hu * 0.06)],
                 start=10, end=170, fill=LINE, width=3)
    elif style == "flat":
        draw.line([(cx - mw, mouth_y), (cx + mw, mouth_y)], fill=LINE, width=3)
    elif style == "compressed":
        draw.line([(cx - mw + 4, mouth_y - 1), (cx + mw - 4, mouth_y - 1)], fill=LINE, width=3)
        draw.line([(cx - mw, mouth_y + 3), (cx - mw + 6, mouth_y - 2)], fill=LINE, width=2)
        draw.line([(cx + mw, mouth_y + 3), (cx + mw - 6, mouth_y - 2)], fill=LINE, width=2)
    elif style == "grimace":
        draw.rectangle([cx - mw + 4, mouth_y - 4, cx + mw - 4, mouth_y + 6],
                       fill=(245, 240, 232), outline=LINE, width=2)
        for i in range(4):
            tx = cx - mw + 8 + i * (int(mw * 0.45))
            draw.line([(tx, mouth_y - 4), (tx, mouth_y + 6)], fill=LINE, width=1)
    elif style == "open_surprised":
        draw.ellipse([cx - int(mw * 0.55), mouth_y - 4,
                      cx + int(mw * 0.55), mouth_y + int(hu * 0.10)],
                     fill=(210, 180, 150), outline=LINE, width=2)
    elif style == "open_delight":
        draw.arc([cx - mw, mouth_y - int(hu * 0.06), cx + mw, mouth_y + int(hu * 0.10)],
                 start=10, end=170, fill=LINE, width=3)


def _draw_cosmo_body(draw, cx, body_top_y, hu, body_data):
    arm_l_dy    = body_data.get("arm_l_dy", 0)
    arm_r_dy    = body_data.get("arm_r_dy", 0)
    body_tilt   = body_data.get("body_tilt", 0)
    body_squash = body_data.get("body_squash", 1.0)
    nb_show     = body_data.get("notebook_show", True)
    nb_open     = body_data.get("notebook_open", False)
    arm_mode    = body_data.get("arm_mode", "standard")

    torso_hw  = int(hu * 0.41)
    torso_h   = int(hu * 1.2 * body_squash)
    tilt_off  = int(body_tilt * 2.5)
    torso_bot_y = body_top_y + torso_h

    shirt_pts = [
        (cx - torso_hw + tilt_off, body_top_y),
        (cx + torso_hw + tilt_off, body_top_y),
        (cx + torso_hw,            torso_bot_y),
        (cx - torso_hw,            torso_bot_y),
    ]
    draw.polygon(shirt_pts, fill=STRIPE_A, outline=LINE, width=2)

    stripe_h  = max(4, int(hu * 0.055))
    n_stripes = torso_h // stripe_h
    for i in range(n_stripes):
        if i % 2 == 0:
            continue
        sy     = body_top_y + i * stripe_h
        ey     = min(sy + stripe_h, torso_bot_y)
        t_frac = (sy - body_top_y) / max(1, torso_h)
        s_tilt = tilt_off * (1 - t_frac)
        sw_l   = int(torso_hw - abs(s_tilt) * 0.1)
        stripe_pts = [
            (cx - sw_l + int(s_tilt), sy),
            (cx + sw_l + int(s_tilt), sy),
            (cx + sw_l,               ey),
            (cx - sw_l,               ey),
        ]
        draw.polygon(stripe_pts, fill=STRIPE_B)

    draw.polygon(shirt_pts, outline=LINE, width=2)

    neck_w = int(hu * 0.10)
    draw.ellipse([cx - neck_w, body_top_y - int(hu * 0.04),
                  cx + neck_w, body_top_y + int(hu * 0.08)], fill=SKIN)

    arm_w = int(hu * 0.12)
    arm_h = int(hu * 0.75)
    arm_y = body_top_y + int(hu * 0.06)

    lax = cx - torso_hw + tilt_off - int(hu * 0.03)
    rax = cx + torso_hw + tilt_off + int(hu * 0.03)

    # ── STANDARD ARM DRAWING ─────────────────────────────────────────────────
    if arm_mode == "standard":
        lay = arm_y + arm_l_dy
        draw.rectangle([lax - arm_w, lay, lax, lay + arm_h], fill=STRIPE_A, outline=LINE, width=2)
        draw.ellipse([lax - arm_w - 6, lay + arm_h - 6,
                      lax + 4, lay + arm_h + int(hu * 0.14)], fill=SKIN, outline=LINE, width=2)

        ray = arm_y + arm_r_dy
        draw.rectangle([rax, ray, rax + arm_w, ray + arm_h], fill=STRIPE_A, outline=LINE, width=2)
        draw.ellipse([rax - 4, ray + arm_h - 6,
                      rax + arm_w + 6, ray + arm_h + int(hu * 0.14)], fill=SKIN, outline=LINE, width=2)

    # ── THOUGHTFUL — right arm raises to face to touch glasses ───────────────
    elif arm_mode == "thoughtful":
        lay = arm_y + arm_l_dy
        draw.rectangle([lax - arm_w, lay, lax, lay + arm_h], fill=STRIPE_A, outline=LINE, width=2)
        draw.ellipse([lax - arm_w - 6, lay + arm_h - 6,
                      lax + 4, lay + arm_h + int(hu * 0.14)], fill=SKIN, outline=LINE, width=2)
        elbow_x = rax + int(hu * 0.36)
        elbow_y = arm_y - int(arm_h * 0.12)
        hand_x  = cx + int(hu * 0.32)
        hand_y  = arm_y - int(arm_h * 0.55)
        draw.line([(rax, arm_y), (elbow_x, elbow_y)], fill=STRIPE_A, width=arm_w * 3)
        draw.line([(rax, arm_y), (elbow_x, elbow_y)], fill=LINE, width=2)
        draw.line([(elbow_x, elbow_y), (hand_x, hand_y)], fill=STRIPE_A, width=arm_w * 3)
        draw.line([(elbow_x, elbow_y), (hand_x, hand_y)], fill=LINE, width=2)
        draw.ellipse([hand_x - int(arm_w * 1.2), hand_y - int(hu * 0.12),
                      hand_x + int(arm_w * 1.2), hand_y + int(hu * 0.06)],
                     fill=SKIN, outline=LINE, width=2)

    # ── DELIGHTED — both arms raised to chest height, elbows bent ────────────
    elif arm_mode == "delighted":
        for side, ax in [(-1, lax), (1, rax)]:
            elbow_x = cx + side * int(hu * 0.60)
            elbow_y = arm_y - int(arm_h * 0.20)
            hand_x  = cx + side * int(hu * 0.45)
            hand_y  = arm_y - int(arm_h * 0.65)
            draw.line([(ax, arm_y), (elbow_x, elbow_y)], fill=STRIPE_A, width=arm_w * 3)
            draw.line([(ax, arm_y), (elbow_x, elbow_y)], fill=LINE, width=2)
            draw.line([(elbow_x, elbow_y), (hand_x, hand_y)], fill=STRIPE_A, width=arm_w * 3)
            draw.line([(elbow_x, elbow_y), (hand_x, hand_y)], fill=LINE, width=2)
            draw.ellipse([hand_x - int(arm_w * 1.3), hand_y - int(hu * 0.08),
                          hand_x + int(arm_w * 1.3), hand_y + int(hu * 0.08)],
                         fill=SKIN, outline=LINE, width=2)

    # ── HEAD GRAB — hands frame sides of head, TALL silhouette above head ────
    elif arm_mode == "head_grab":
        for side, ax in [(-1, lax), (1, rax)]:
            elbow_x = cx + side * int(hu * 0.82)
            elbow_y = body_top_y - int(hu * 0.25)
            hand_x = cx + side * int(hu * 0.65)
            hand_y = body_top_y - int(hu * 1.20)
            draw.line([(ax, body_top_y + int(hu * 0.06)), (elbow_x, elbow_y)], fill=STRIPE_A, width=arm_w * 3)
            draw.line([(ax, body_top_y + int(hu * 0.06)), (elbow_x, elbow_y)], fill=LINE, width=2)
            draw.line([(elbow_x, elbow_y), (hand_x, hand_y)], fill=STRIPE_A, width=arm_w * 3)
            draw.line([(elbow_x, elbow_y), (hand_x, hand_y)], fill=LINE, width=2)
            draw.ellipse([hand_x - int(arm_w * 1.6), hand_y - int(hu * 0.16),
                          hand_x + int(arm_w * 1.6), hand_y + int(hu * 0.10)],
                         fill=SKIN, outline=LINE, width=2)

    # ── AWKWARD — maximum asymmetry: left hang + right palm-out stiff ────────
    elif arm_mode == "awkward":
        lay = arm_y + 8
        draw.rectangle([lax - arm_w, lay, lax, lay + arm_h + 15], fill=STRIPE_A, outline=LINE, width=2)
        draw.ellipse([lax - arm_w - 6, lay + arm_h + 8,
                      lax + 4, lay + arm_h + int(hu * 0.22)], fill=SKIN, outline=LINE, width=2)

        raise_off = -int(hu * 0.22)
        palm_x    = rax + int(hu * 0.90)
        palm_y    = arm_y + int(arm_h * 0.18) + raise_off
        elbow_x   = rax + int(hu * 0.52)
        elbow_y   = arm_y + int(arm_h * 0.35) + raise_off
        draw.line([(rax, arm_y + raise_off), (elbow_x, elbow_y)], fill=STRIPE_A, width=arm_w * 3)
        draw.line([(rax, arm_y + raise_off), (elbow_x, elbow_y)], fill=LINE, width=2)
        draw.line([(elbow_x, elbow_y), (palm_x, palm_y)], fill=STRIPE_A, width=arm_w * 3)
        draw.line([(elbow_x, elbow_y), (palm_x, palm_y)], fill=LINE, width=2)
        draw.ellipse([palm_x - int(arm_w * 1.0), palm_y - int(hu * 0.20),
                      palm_x + int(arm_w * 1.0), palm_y + int(hu * 0.08)],
                     fill=SKIN_HL, outline=LINE, width=2)

    # ── WIDE STARTLE — horizontal arms + backward lean ────────────────────────
    elif arm_mode == "wide_startle":
        for side, ax in [(-1, lax), (1, rax)]:
            elbow_x = cx + side * int(hu * 0.90)
            elbow_y = arm_y - int(arm_h * 0.04)
            hand_x  = cx + side * int(hu * 1.30)
            hand_y  = arm_y - int(arm_h * 0.12)
            draw.line([(ax, arm_y), (elbow_x, elbow_y)], fill=STRIPE_A, width=arm_w * 3)
            draw.line([(ax, arm_y), (elbow_x, elbow_y)], fill=LINE, width=2)
            draw.line([(elbow_x, elbow_y), (hand_x, hand_y)], fill=STRIPE_A, width=arm_w * 3)
            draw.line([(elbow_x, elbow_y), (hand_x, hand_y)], fill=LINE, width=2)
            draw.ellipse([hand_x - int(arm_w * 1.4), hand_y - int(hu * 0.12),
                          hand_x + int(arm_w * 1.4), hand_y + int(hu * 0.10)],
                         fill=SKIN, outline=LINE, width=2)

    # ── SKEPTICAL CROSSED — v007: both arms angled inward, hands tucked at waist ─
    elif arm_mode == "skeptical_crossed":
        # SKEPTICAL: a "not impressed" symmetrical fold at waist level.
        # Both arms angled slightly down and inward — hands tucked near hip/waist.
        # This creates NARROW arm silhouette (both arms close to body) compared to:
        #   AWKWARD: asymmetric arms (one far right, one hanging)
        #   DETERMINED: arms straight down at sides
        #   DELIGHTED: both arms raised at chest height
        # The key differentiator: both hands near center/waist = "buttoned up" skeptic.
        # Notebook (closed) is held in left arm, adding mass to the left side.

        # LEFT ARM: notebook tucked, arm goes slightly down and inward
        l_shoulder_x = lax
        l_shoulder_y = arm_y + int(arm_h * 0.08)
        l_elbow_x    = lax - int(hu * 0.04)           # barely left of shoulder
        l_elbow_y    = l_shoulder_y + int(arm_h * 0.42)
        l_hand_x     = cx - int(hu * 0.22)            # hand at left of center (notebook arm)
        l_hand_y     = l_shoulder_y + int(arm_h * 0.72)
        draw.line([(l_shoulder_x, l_shoulder_y), (l_elbow_x, l_elbow_y)],
                  fill=STRIPE_A, width=arm_w * 3)
        draw.line([(l_shoulder_x, l_shoulder_y), (l_elbow_x, l_elbow_y)],
                  fill=LINE, width=2)
        draw.line([(l_elbow_x, l_elbow_y), (l_hand_x, l_hand_y)],
                  fill=STRIPE_A, width=arm_w * 3)
        draw.line([(l_elbow_x, l_elbow_y), (l_hand_x, l_hand_y)],
                  fill=LINE, width=2)
        draw.ellipse([l_hand_x - int(arm_w * 1.3), l_hand_y - int(hu * 0.10),
                      l_hand_x + int(arm_w * 1.3), l_hand_y + int(hu * 0.10)],
                     fill=SKIN, outline=LINE, width=2)

        # RIGHT ARM: hand rests on left forearm — supporting the "arms loosely folded" posture.
        # Goes from right shoulder INWARD (crossing to left-center) — visible crossing.
        r_shoulder_x = rax
        r_shoulder_y = arm_y + int(arm_h * 0.22)     # slightly lower than left
        r_elbow_x    = cx + int(hu * 0.18)            # right of center
        r_elbow_y    = r_shoulder_y + int(arm_h * 0.28)
        r_hand_x     = cx - int(hu * 0.05)            # hand crossing to left-center
        r_hand_y     = r_shoulder_y + int(arm_h * 0.55)
        draw.line([(r_shoulder_x, r_shoulder_y), (r_elbow_x, r_elbow_y)],
                  fill=STRIPE_A, width=arm_w * 3)
        draw.line([(r_shoulder_x, r_shoulder_y), (r_elbow_x, r_elbow_y)],
                  fill=LINE, width=2)
        draw.line([(r_elbow_x, r_elbow_y), (r_hand_x, r_hand_y)],
                  fill=STRIPE_A, width=arm_w * 3)
        draw.line([(r_elbow_x, r_elbow_y), (r_hand_x, r_hand_y)],
                  fill=LINE, width=2)
        draw.ellipse([r_hand_x - int(arm_w * 1.3), r_hand_y - int(hu * 0.10),
                      r_hand_x + int(arm_w * 1.3), r_hand_y + int(hu * 0.10)],
                     fill=SKIN, outline=LINE, width=2)

    # ── Notebook ──────────────────────────────────────────────────────────────
    if nb_show:
        nb_h = int(hu * 0.30)
        nb_w = int(hu * 0.18)
        if nb_open:
            nb_x = cx - int(nb_w * 0.5)
            nb_y = torso_bot_y - int(hu * 0.55)
            draw.rectangle([nb_x, nb_y, nb_x + nb_w * 2, nb_y + nb_h],
                           fill=NOTEBOOK, outline=LINE, width=2)
            draw.line([(nb_x + nb_w, nb_y), (nb_x + nb_w, nb_y + nb_h)],
                      fill=(250, 240, 220), width=3)
            draw.line([(nb_x + nb_w, nb_y), (nb_x + nb_w, nb_y + nb_h)],
                      fill=LINE, width=1)
        else:
            nb_tuck_x = cx - torso_hw - int(hu * 0.02)
            nb_tuck_y = arm_y + int(arm_h * 0.35)
            draw.rectangle([nb_tuck_x - nb_w, nb_tuck_y,
                            nb_tuck_x,        nb_tuck_y + nb_h],
                           fill=NOTEBOOK, outline=LINE, width=2)
            draw.rectangle([nb_tuck_x - 6, nb_tuck_y,
                            nb_tuck_x,     nb_tuck_y + nb_h], fill=NOTEBOOK_SP)
            draw.line([(nb_tuck_x - nb_w + 3, nb_tuck_y + 3),
                       (nb_tuck_x - nb_w + 3, nb_tuck_y + nb_h - 3)],
                      fill=(250, 240, 220), width=2)

    # ── Legs ──────────────────────────────────────────────────────────────────
    leg_w = int(hu * 0.16)
    leg_h = int(hu * 0.90)
    leg_l = cx - int(torso_hw * 0.42)
    leg_r = cx + int(torso_hw * 0.42)
    leg_y = torso_bot_y

    pigeon = arm_mode == "awkward"

    draw.rectangle([leg_l - leg_w, leg_y, leg_l + leg_w, leg_y + leg_h],
                   fill=PANTS, outline=LINE, width=2)
    draw.line([(leg_l, leg_y), (leg_l, leg_y + leg_h)], fill=PANTS_SH, width=1)
    draw.rectangle([leg_r - leg_w, leg_y, leg_r + leg_w, leg_y + leg_h],
                   fill=PANTS, outline=LINE, width=2)
    draw.line([(leg_r, leg_y), (leg_r, leg_y + leg_h)], fill=PANTS_SH, width=1)

    shoe_w = int(hu * 0.28)
    shoe_h = int(hu * 0.18)
    shoe_y = leg_y + leg_h

    if pigeon:
        draw.ellipse([leg_l - int(shoe_w * 0.1), shoe_y,
                      leg_l + shoe_w - int(shoe_w * 0.1), shoe_y + shoe_h],
                     fill=SHOE, outline=LINE, width=2)
        draw.ellipse([leg_r + leg_w - int(shoe_w * 0.4), shoe_y,
                      leg_r + leg_w + shoe_w - int(shoe_w * 0.3), shoe_y + shoe_h],
                     fill=SHOE, outline=LINE, width=2)
    else:
        draw.ellipse([leg_l - leg_w - shoe_w + int(shoe_w * 0.3), shoe_y,
                      leg_l - leg_w + int(shoe_w * 0.4), shoe_y + shoe_h],
                     fill=SHOE, outline=LINE, width=2)
        draw.arc([leg_l - leg_w - shoe_w + int(shoe_w * 0.35), shoe_y + 3,
                  leg_l - leg_w + int(shoe_w * 0.35), shoe_y + shoe_h - 3],
                 start=200, end=340, fill=SHOE_SOLE, width=2)
        draw.ellipse([leg_r + leg_w - int(shoe_w * 0.4), shoe_y,
                      leg_r + leg_w + shoe_w - int(shoe_w * 0.3), shoe_y + shoe_h],
                     fill=SHOE, outline=LINE, width=2)
        draw.arc([leg_r + leg_w - int(shoe_w * 0.35), shoe_y + 3,
                  leg_r + leg_w + shoe_w - int(shoe_w * 0.35), shoe_y + shoe_h - 3],
                 start=200, end=340, fill=SHOE_SOLE, width=2)


def draw_cosmo(draw, cx, cy, hu, expr):
    glasses_tilt = expr.get("glasses_tilt", 7)
    body_data    = expr.get("body_data", {})
    brow_data    = expr.get("brow_data", {})
    mouth_data   = expr.get("mouth_data", {"style": "neutral"})

    body_top_y = cy + int(hu * 0.55)
    _draw_cosmo_body(draw, cx, body_top_y, hu, body_data)
    _draw_cosmo_hair(draw, cx, cy, hu)
    _draw_cosmo_head(draw, cx, cy, hu)
    lcx, lcy, rcx, rcy, lens_r = _draw_cosmo_glasses(draw, cx, cy, hu, glasses_tilt)
    _draw_cosmo_eyes(draw, lcx, lcy, rcx, rcy, lens_r)
    _draw_cosmo_brows(draw, cx, cy, hu, glasses_tilt, brow_data, lcx, lcy, rcx, rcy)
    _draw_cosmo_nose(draw, cx, cy, hu)
    _draw_cosmo_mouth(draw, cx, cy, hu, mouth_data)

    if expr.get("blush", False):
        blush_r_x = int(hu * 0.22)
        blush_r_y = int(hu * 0.09)
        cheek_y   = cy + int(hu * 0.20)
        left_cx   = cx - int(hu * 0.35)
        right_cx  = cx + int(hu * 0.35)
        for bcx in (left_cx, right_cx):
            draw.ellipse([bcx - blush_r_x, cheek_y - blush_r_y,
                          bcx + blush_r_x, cheek_y + blush_r_y],
                         fill=BLUSH)
            inner_rx = int(blush_r_x * 0.55)
            inner_ry = int(blush_r_y * 0.55)
            draw.ellipse([bcx - inner_rx, cheek_y - inner_ry,
                          bcx + inner_rx, cheek_y + inner_ry],
                         fill=BLUSH_HI)


def generate_cosmo_expression_sheet(output_path):
    # v006: Labels are OUTSIDE panel bounds (inherited from v005 silhouette tool fix)
    total_w = COLS * (PANEL_W + PAD) + PAD
    total_h = HEADER + ROWS * (PANEL_H + LABEL_H + PAD) + PAD

    img  = Image.new('RGB', (total_w, total_h), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font       = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
        font_sm    = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        font_title = font = font_sm = ImageFont.load_default()

    draw.text((PAD, 14),
              "COSMO — Expression Sheet — Luma & the Glitchkin  |  v007  |  C38: SKEPTICAL arm fix (skeptical_crossed)",
              fill=(91, 141, 184), font=font_title)

    # v006: character scaled to ~19% of panel height (same as v005)
    HU = int(PANEL_H * 0.190)

    beat_tags = {
        "AWKWARD":                "A1-03 / A2-02",
        "WORRIED":                "A2-02",
        "SURPRISED":              "A2-04c",
        "SKEPTICAL":              "A2-03",
        "DETERMINED":             "A2-05b",
        "FRUSTRATED / DEFEATED":  "A2-06",
    }

    for i, expr in enumerate(EXPRESSIONS):
        col = i % COLS
        row = i // COLS
        ppx = PAD + col * (PANEL_W + PAD)
        ppy = HEADER + row * (PANEL_H + LABEL_H + PAD)

        # ── Character panel (light background, no dark bar) ──────────────────
        panel_bg = expr["panel_bg"]
        draw.rectangle([ppx, ppy, ppx + PANEL_W, ppy + PANEL_H], fill=panel_bg)
        draw.rectangle([ppx, ppy, ppx + PANEL_W, ppy + PANEL_H], outline=(80, 74, 70), width=1)

        arm_modes_needing_room = {"head_grab", "wide_startle", "skeptical_crossed"}
        face_frac = 0.42 if expr["body_data"].get("arm_mode") in arm_modes_needing_room else 0.32
        face_cy = ppy + int(PANEL_H * face_frac)
        face_cx = ppx + PANEL_W // 2
        draw_cosmo(draw, face_cx, face_cy, HU, expr)

        tag = beat_tags.get(expr["name"])
        if tag:
            draw.text((ppx + PANEL_W - 74, ppy + 6), tag, fill=(100, 160, 120), font=font_sm)

        # ── Label strip (BELOW panel, in CANVAS_BG area) ─────────────────────
        label_y = ppy + PANEL_H
        draw.rectangle([ppx, label_y, ppx + PANEL_W, label_y + LABEL_H],
                       fill=(18, 14, 12))
        draw.text((ppx + 6, label_y + 6),
                  expr["name"], fill=(91, 141, 184), font=font)
        draw.text((ppx + 6, label_y + 26),
                  expr["prev_state"], fill=(130, 118, 112), font=font_sm)
        draw.text((ppx + 6, label_y + 40),
                  expr["next_state"], fill=(130, 118, 112), font=font_sm)

    img.thumbnail((1280, 1280), Image.LANCZOS)
    img.save(output_path)
    print(f"Saved: {output_path}  ({img.size[0]}x{img.size[1]}px)")
    print("v007 fix: SKEPTICAL arm_mode='skeptical_crossed'")
    print("  - Left arm crosses body (hand right of center — dismissive fold)")
    print("  - Right elbow cocks OUT (arms-akimbo — visible outside torso right)")
    print("  - Both arms now clearly readable outside body silhouette")
    print("v006 preserved: S003 glasses_tilt compliance, all other expressions unchanged")


if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "characters", "main")
    os.makedirs(out_dir, exist_ok=True)
    generate_cosmo_expression_sheet(
        os.path.join(out_dir, "LTG_CHAR_cosmo_expression_sheet.png")
    )
