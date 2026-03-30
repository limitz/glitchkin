#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_character_face_test.py
Character Face Legibility Test — Sprint/Wide-Shot Scale

Renders a character head at sprint/wide-shot scale (head_r = 20–25px range) and
draws candidate facial expressions — varying eye sizes, brow angles, mouth shapes —
as a contact sheet of 6–8 variants. Output ≤ 600×400px reference PNG.

Purpose:
  Prevent "invisible at sprint scale" expression problems before they enter full
  SF generator iteration cycles. Run this before modifying face geometry in any
  SF generator to confirm the expression reads at the target render scale.

Usage:
  python3 LTG_TOOL_character_face_test.py [options]

  --char       CHARACTER   Character to test: luma (default), cosmo, miri, byte
  --head-r     INT         Head radius in pixels (default: 23 — Luma SF02 sprint scale)
  --variants   INT         Number of variants to generate: 6 or 8 (default: 6)
  --output     PATH        Output PNG path (default: ./LTG_TOOL_face_test_<char>_r<R>.png)
  --scale      INT         Zoom multiplier for display panels (default: 3 — each panel
                           shows head at head_r * scale for visibility, but the raw
                           head_r is used for the face geometry to test actual legibility)

Output:
  PNG contact sheet ≤ 600×400px (hard limit enforced).
  Each variant panel shows:
  - Character head at specified head_r (test scale — what SF will render)
  - Character head at head_r * scale (zoomed — to inspect geometry)
  - Variant label + expression description

Byte character notes:
  Byte's body IS the oval (no separate head). Eyes are 5×5 pixel grid system.
  Left eye (viewer's left) = normal DEEP_CYAN grid.
  Right eye (viewer's right) = cracked HOT_MAGENTA crack line, dead-zone upper-right.
  No nose, no brows. Pixel mouth optional per expression.
  Face gate checks: eye_count==2, left/right differentiation, pixel_grid_proportions.

Author: Lee Tanaka — Character Staging & Visual Acting Specialist
Cycle: 35 (C34 ideabox idea, actioned C35)
Byte profile: Kai Nakamura — Technical Art Engineer
Byte profile cycle: C45 (2026-03-30)
Date: 2026-03-29
"""

import os
import sys
import argparse
import math
from PIL import Image, ImageDraw, ImageFont

# ── Output rule: hard limit ≤ 1280px in both dimensions ──────────────────────
MAX_DIM = 1280

# ── Palette ───────────────────────────────────────────────────────────────────
# Shared colors
VOID_BLACK      = (10, 10, 20)
STATIC_WHITE    = (240, 240, 240)
DEEP_COCOA      = (59, 40, 32)
PANEL_BG        = (28, 28, 36)
PANEL_BORDER    = (60, 60, 80)
LABEL_COLOR     = (200, 200, 200)
HEADER_COLOR    = (0, 220, 240)
PASS_COLOR      = (60, 200, 80)
WARN_COLOR      = (220, 160, 40)
FAIL_COLOR      = (220, 60, 60)

# Luma colors (SF02 storm variant)
LUMA_SKIN_STORM    = (106, 180, 174)
LUMA_HOODIE_STORM  = (200, 105, 90)
LUMA_HAIR          = (59, 40, 32)
LUMA_HAIR_MAGENTA  = (106, 42, 58)
LUMA_CORRUPT_AMB   = (255, 140, 0)

# Cosmo colors (standard)
COSMO_SKIN         = (224, 180, 140)
COSMO_JACKET       = (160, 150, 175)
COSMO_HAIR         = (40, 30, 20)
COSMO_GLASSES      = (50, 50, 60)

# Miri colors (standard)
MIRI_SKIN          = (220, 175, 145)
MIRI_HAIR          = (140, 130, 125)   # silver-grey
MIRI_CARDIGAN      = (175, 135, 105)

# Byte colors (canonical spec GL-01b + GL-02)
BYTE_TEAL          = (0, 212, 232)     # #00D4E8 GL-01b — body fill (always)
BYTE_HIGHLIGHT     = (0, 240, 255)     # #00F0FF GL-01  — highlight/circuit accent
BYTE_SHADOW        = (0, 168, 192)     # #00A8C0 GL-01a — deep-cyan shadow
BYTE_HOT_MAG       = (255, 45, 107)   # #FF2D6B GL-02  — cracked eye crack line
BYTE_VOID          = (10, 10, 20)     # #0A0A14 — outline + dead-zone fill
BYTE_EYE_NORMAL    = (0, 240, 255)    # #00F0FF DEEP_CYAN — left (normal) eye pixels
BYTE_EYE_DEAD      = (10, 10, 20)     # dead-zone pixels in cracked right eye


# ── Expression Variant Definitions ───────────────────────────────────────────
# Each variant is a dict of drawing parameters.
# All parameters are defined as fractions of head_r for scale independence.

# Variant parameter schema:
#   label:        str — short name shown in panel
#   description:  str — one line description
#   eye_r_L:      float — left eye radius as fraction of head_r
#   eye_r_R:      float — right eye radius as fraction of head_r
#   brow_L_angle: float — left brow angle in degrees (+ = outer end up, - = inner end pulled down)
#   brow_R_angle: float — right brow angle in degrees
#   mouth_h:      float — mouth oval height as fraction of head_r (0 = line, >0 = open)
#   mouth_w:      float — mouth oval width as fraction of head_r
#   gaze_offset:  tuple (dx_frac, dy_frac) — pupil offset as fraction of eye_r
#   eye_y_frac:   float — eye Y center as fraction of head_r from center (-1=top, +1=bottom)
#   skin_color:   tuple — override skin fill (None = character default)
#   readability:  str — PASS/WARN/FAIL at sprint scale

LUMA_VARIANTS = [
    {
        "label": "NEUTRAL",
        "description": "No face drawn (baseline — current v006 state)",
        "eye_r_L": 0.0, "eye_r_R": 0.0,
        "brow_L_angle": 0.0, "brow_R_angle": 0.0,
        "mouth_h": 0.0, "mouth_w": 0.0,
        "gaze_offset": (0.0, 0.0), "eye_y_frac": -0.15,
        "readability": "FAIL",
    },
    {
        "label": "FOCUSED DET.",
        "description": "Asymmetric eyes, brow inward-L, set jaw (brief spec)",
        "eye_r_L": 0.174, "eye_r_R": 0.130,   # 4px / 3px at r=23
        "brow_L_angle": -10.0, "brow_R_angle": 0.0,
        "mouth_h": 0.065, "mouth_w": 0.174,    # 1.5px tall at r=23 — compressed
        "gaze_offset": (0.25, 0.30), "eye_y_frac": -0.15,
        "readability": "PASS",
    },
    {
        "label": "FEAR",
        "description": "Both eyes wide, brows up, open O mouth",
        "eye_r_L": 0.217, "eye_r_R": 0.217,   # 5px both — symmetric wide
        "brow_L_angle": 12.0, "brow_R_angle": 12.0,
        "mouth_h": 0.217, "mouth_w": 0.217,    # open O
        "gaze_offset": (0.0, -0.10), "eye_y_frac": -0.20,
        "readability": "WARN",
    },
    {
        "label": "DETERMINED+",
        "description": "Eyes fwd-down, both brows pulled in (symmetric)",
        "eye_r_L": 0.174, "eye_r_R": 0.174,
        "brow_L_angle": -8.0, "brow_R_angle": -8.0,
        "mouth_h": 0.065, "mouth_w": 0.174,
        "gaze_offset": (0.20, 0.25), "eye_y_frac": -0.15,
        "readability": "PASS",
    },
    {
        "label": "TOO SMALL",
        "description": "Eyes at 2px — too small, faces disappear",
        "eye_r_L": 0.087, "eye_r_R": 0.087,   # 2px at r=23
        "brow_L_angle": -5.0, "brow_R_angle": 0.0,
        "mouth_h": 0.043, "mouth_w": 0.130,
        "gaze_offset": (0.0, 0.20), "eye_y_frac": -0.15,
        "readability": "FAIL",
    },
    {
        "label": "EYES ONLY",
        "description": "Eyes + brows, no mouth — minimal viable face",
        "eye_r_L": 0.174, "eye_r_R": 0.130,
        "brow_L_angle": -10.0, "brow_R_angle": 0.0,
        "mouth_h": 0.0, "mouth_w": 0.0,
        "gaze_offset": (0.25, 0.30), "eye_y_frac": -0.15,
        "readability": "PASS",
    },
]

COSMO_VARIANTS = [
    {
        "label": "NEUTRAL",
        "description": "No face drawn (baseline)",
        "eye_r_L": 0.0, "eye_r_R": 0.0,
        "brow_L_angle": 0.0, "brow_R_angle": 0.0,
        "mouth_h": 0.0, "mouth_w": 0.0,
        "gaze_offset": (0.0, 0.0), "eye_y_frac": -0.15,
        "readability": "FAIL",
    },
    {
        "label": "PANIC RUN",
        "description": "Eyes wide, brows up, open mouth (fear/panic)",
        "eye_r_L": 0.200, "eye_r_R": 0.200,
        "brow_L_angle": 12.0, "brow_R_angle": 12.0,
        "mouth_h": 0.200, "mouth_w": 0.200,
        "gaze_offset": (0.0, -0.10), "eye_y_frac": -0.20,
        "readability": "WARN",
    },
    {
        "label": "SKEPTICAL",
        "description": "One brow raised, other flat, deadpan mouth",
        "eye_r_L": 0.130, "eye_r_R": 0.174,
        "brow_L_angle": 0.0, "brow_R_angle": 15.0,
        "mouth_h": 0.043, "mouth_w": 0.150,
        "gaze_offset": (0.10, 0.0), "eye_y_frac": -0.15,
        "readability": "PASS",
    },
    {
        "label": "WORRIED",
        "description": "Brows together-up, brow bridge crease, slight frown",
        "eye_r_L": 0.174, "eye_r_R": 0.174,
        "brow_L_angle": 8.0, "brow_R_angle": -8.0,
        "mouth_h": 0.065, "mouth_w": 0.174,
        "gaze_offset": (0.0, 0.20), "eye_y_frac": -0.18,
        "readability": "PASS",
    },
    {
        "label": "TOO SMALL",
        "description": "Eyes at 2px — too small at sprint scale",
        "eye_r_L": 0.087, "eye_r_R": 0.087,
        "brow_L_angle": 0.0, "brow_R_angle": 12.0,
        "mouth_h": 0.043, "mouth_w": 0.130,
        "gaze_offset": (0.0, 0.0), "eye_y_frac": -0.15,
        "readability": "FAIL",
    },
    {
        "label": "CURIOUS",
        "description": "Head tilted slightly, asymmetric eye size, open query",
        "eye_r_L": 0.174, "eye_r_R": 0.130,
        "brow_L_angle": 5.0, "brow_R_angle": 0.0,
        "mouth_h": 0.087, "mouth_w": 0.174,
        "gaze_offset": (-0.10, -0.10), "eye_y_frac": -0.15,
        "readability": "PASS",
    },
]

MIRI_VARIANTS = [
    {
        "label": "NEUTRAL",
        "description": "No face drawn (baseline)",
        "eye_r_L": 0.0, "eye_r_R": 0.0,
        "brow_L_angle": 0.0, "brow_R_angle": 0.0,
        "mouth_h": 0.0, "mouth_w": 0.0,
        "gaze_offset": (0.0, 0.0), "eye_y_frac": -0.15,
        "readability": "FAIL",
    },
    {
        "label": "KNOWING STILL.",
        "description": "Eyes neutral-soft, oblique mouth corner (signature)",
        "eye_r_L": 0.148, "eye_r_R": 0.148,
        "brow_L_angle": 2.0, "brow_R_angle": 2.0,
        "mouth_h": 0.043, "mouth_w": 0.200,
        "gaze_offset": (0.0, 0.10), "eye_y_frac": -0.12,
        "readability": "WARN",    # subtle, may not survive sprint scale
    },
    {
        "label": "SURPRISED",
        "description": "Wide eyes, raised brows, hand-to-cheek signal",
        "eye_r_L": 0.217, "eye_r_R": 0.217,
        "brow_L_angle": 10.0, "brow_R_angle": 10.0,
        "mouth_h": 0.130, "mouth_w": 0.174,
        "gaze_offset": (0.0, -0.15), "eye_y_frac": -0.22,
        "readability": "PASS",
    },
    {
        "label": "WELCOMING",
        "description": "Warm squint, soft upward mouth curve",
        "eye_r_L": 0.148, "eye_r_R": 0.148,
        "brow_L_angle": 4.0, "brow_R_angle": 4.0,
        "mouth_h": 0.065, "mouth_w": 0.217,
        "gaze_offset": (0.0, 0.05), "eye_y_frac": -0.10,
        "readability": "WARN",
    },
    {
        "label": "RECOGNITION",
        "description": "Asymmetric brow, one eye squint, pursed mouth",
        "eye_r_L": 0.130, "eye_r_R": 0.174,
        "brow_L_angle": -3.0, "brow_R_angle": 12.0,
        "mouth_h": 0.043, "mouth_w": 0.174,
        "gaze_offset": (0.10, 0.10), "eye_y_frac": -0.15,
        "readability": "PASS",
    },
    {
        "label": "TOO SMALL",
        "description": "Eyes at 2px — fails at sprint scale",
        "eye_r_L": 0.087, "eye_r_R": 0.087,
        "brow_L_angle": 2.0, "brow_R_angle": 2.0,
        "mouth_h": 0.043, "mouth_w": 0.174,
        "gaze_offset": (0.0, 0.0), "eye_y_frac": -0.12,
        "readability": "FAIL",
    },
]

# ── Byte Variant Definitions ──────────────────────────────────────────────────
# Byte uses the 5×5 pixel grid eye system.  Variant parameters differ from
# organic characters — no brows, no nose, optional pixel mouth.
#
# Byte-specific schema keys:
#   label:           str — short name shown in panel
#   description:     str — one line description
#   left_eye_style:  str — "normal" (DEEP_CYAN pixels) | "off" (blank)
#   right_eye_style: str — "cracked" (HOT_MAG crack, dead upper-right) |
#                          "searching" (scan-line mid row) | "off"
#   mouth_style:     str — "none" | "flat" (pixel row) | "frown" | "uptick"
#   eye_size_px:     int — pixel cell size (each cell = 1 pixel at sprint scale;
#                          2 or 3 for zoom reference)
#   eye_y_frac:      float — eye Y center as fraction of head_r from oval center
#   readability:     str — PASS/WARN/FAIL at sprint scale
#   gate_eye_count:  int — expected visible eyes (0, 1, or 2)
#   gate_differentiated: bool — True if L/R should be visually distinct

BYTE_VARIANTS = [
    {
        "label": "NEUTRAL",
        "description": "Both eyes present, no mouth — default idle state",
        "left_eye_style": "normal",
        "right_eye_style": "cracked",
        "mouth_style": "none",
        "eye_size_px": 1,
        "eye_y_frac": -0.10,
        "readability": "PASS",
        "gate_eye_count": 2,
        "gate_differentiated": True,
    },
    {
        "label": "GRUMPY",
        "description": "Normal left eye flat, cracked right eye heavy lid, flat mouth",
        "left_eye_style": "normal",
        "right_eye_style": "cracked",
        "mouth_style": "flat",
        "eye_size_px": 1,
        "eye_y_frac": -0.10,
        "readability": "PASS",
        "gate_eye_count": 2,
        "gate_differentiated": True,
    },
    {
        "label": "ALARMED",
        "description": "Both eyes wide open (full 5×5), no mouth — pure alarm",
        "left_eye_style": "normal",
        "right_eye_style": "cracked",
        "mouth_style": "none",
        "eye_size_px": 1,
        "eye_y_frac": -0.15,
        "readability": "PASS",
        "gate_eye_count": 2,
        "gate_differentiated": True,
    },
    {
        "label": "SEARCHING",
        "description": "Normal left, right eye scan-line, flat mouth",
        "left_eye_style": "normal",
        "right_eye_style": "searching",
        "mouth_style": "flat",
        "eye_size_px": 1,
        "eye_y_frac": -0.10,
        "readability": "WARN",   # scan-line subtlety may not survive sprint scale
        "gate_eye_count": 2,
        "gate_differentiated": True,
    },
    {
        "label": "POWERED DOWN",
        "description": "Both eyes off (dark) — no active pixels visible",
        "left_eye_style": "off",
        "right_eye_style": "off",
        "mouth_style": "none",
        "eye_size_px": 1,
        "eye_y_frac": -0.10,
        "readability": "WARN",   # eyes dark — state may be unclear at sprint
        "gate_eye_count": 0,
        "gate_differentiated": False,
    },
    {
        "label": "PIXEL ONLY",
        "description": "1px single dot eyes — too small, fails at sprint scale",
        "left_eye_style": "normal",
        "right_eye_style": "cracked",
        "mouth_style": "none",
        "eye_size_px": 0,        # 0 = draw as 1px dot (too small test)
        "eye_y_frac": -0.10,
        "readability": "FAIL",
        "gate_eye_count": 2,
        "gate_differentiated": False,  # 1px dots cannot show L/R differentiation
    },
]

VARIANT_REGISTRY = {
    "luma":  LUMA_VARIANTS,
    "cosmo": COSMO_VARIANTS,
    "miri":  MIRI_VARIANTS,
    "byte":  BYTE_VARIANTS,
}

CHAR_SKIN = {
    "luma":  LUMA_SKIN_STORM,
    "cosmo": COSMO_SKIN,
    "miri":  MIRI_SKIN,
    "byte":  BYTE_TEAL,        # Byte body fill IS the "skin"
}
CHAR_BODY = {
    "luma":  LUMA_HOODIE_STORM,
    "cosmo": COSMO_JACKET,
    "miri":  MIRI_CARDIGAN,
    "byte":  BYTE_SHADOW,      # lower-limb stub color
}
CHAR_HAIR = {
    "luma":  LUMA_HAIR,
    "cosmo": COSMO_HAIR,
    "miri":  MIRI_HAIR,
    "byte":  BYTE_VOID,        # outline color (no hair)
}


# ── Drawing functions ─────────────────────────────────────────────────────────

def draw_head_base(draw, cx, cy, head_r, skin_color, hair_color, char_name):
    """Draw the head ellipse + basic hair for the character.

    For Byte: draws the oval body (Byte's body IS the oval — wider-than-tall)
    with a VOID_BLACK outline. No hair.
    """
    if char_name == "byte":
        # Byte body is wider-than-tall oval.  Use 1.15× width, 0.90× height.
        bx = int(head_r * 1.15)
        by = int(head_r * 0.90)
        draw.ellipse([cx - bx, cy - by, cx + bx, cy + by],
                     fill=skin_color, outline=BYTE_VOID, width=max(1, int(head_r * 0.08)))
        # Subtle highlight arc (upper-right)
        draw.arc([cx - bx + 2, cy - by + 2, cx + bx - 2, cy + by - 2],
                 start=310, end=30, fill=BYTE_HIGHLIGHT, width=max(1, int(head_r * 0.06)))
        return

    draw.ellipse([cx - head_r, cy - head_r, cx + head_r, cy + head_r],
                 fill=skin_color)
    if char_name == "luma":
        # Hair arc — dark upper portion
        draw.arc([cx - head_r, cy - head_r, cx + head_r, cy + head_r],
                 start=190, end=360, fill=hair_color, width=max(1, int(head_r * 0.5)))
    elif char_name == "cosmo":
        # Simple hair top cap
        draw.chord([cx - head_r, cy - head_r, cx + head_r, cy - int(head_r * 0.3)],
                   start=180, end=360, fill=hair_color)
    elif char_name == "miri":
        # Silver-grey hair arc
        draw.arc([cx - head_r, cy - head_r, cx + head_r, cy + head_r],
                 start=195, end=345, fill=hair_color, width=max(1, int(head_r * 0.45)))


def draw_body_stub(draw, cx, head_r, skin_color, body_color, char_name):
    """Draw minimal body stub below head for context."""
    torso_top = cx  # reused as cy in caller — pass torso top separately
    # We just draw a small rectangle below the head to give body context
    pass  # body stub handled at panel level where we have full coords


def brow_line(draw, cx, brow_y, side, angle_deg, head_r, hair_color):
    """Draw a single brow line with given angle."""
    brow_half_w = max(3, int(head_r * 0.38))
    eye_x_offset = int(head_r * 0.38)

    if side == "L":
        center_x = cx - eye_x_offset
    else:
        center_x = cx + eye_x_offset

    angle_rad = math.radians(angle_deg)
    # outer end = away from nose, inner end = toward nose
    outer_dx = -brow_half_w if side == "L" else brow_half_w
    inner_dx = brow_half_w if side == "L" else -brow_half_w

    # Apply angle: raise outer end, lower inner end (for normal arched brow)
    # Negative angle = inner end pulled DOWN (frown/determination)
    outer_dy = -int(brow_half_w * math.tan(angle_rad))
    inner_dy = int(brow_half_w * math.tan(angle_rad))

    draw.line([
        (center_x + outer_dx, brow_y + outer_dy),
        (center_x + inner_dx, brow_y + inner_dy),
    ], fill=hair_color, width=1)


def draw_face(draw, cx, head_cy, head_r, variant, hair_color):
    """Draw eyes, brows, and mouth from variant parameters."""
    v = variant
    eye_r_L = max(0, round(v["eye_r_L"] * head_r))
    eye_r_R = max(0, round(v["eye_r_R"] * head_r))

    if eye_r_L == 0 and eye_r_R == 0:
        # No face — baseline variant
        return

    SCLERA = (240, 240, 240)
    PUPIL  = (10, 10, 20)
    MOUTH  = (90, 40, 40)

    eye_y_offset = v["eye_y_frac"] * head_r
    eye_y = int(head_cy + eye_y_offset)
    eye_x_L = cx - int(head_r * 0.38)
    eye_x_R = cx + int(head_r * 0.38)

    gaze_dx = v["gaze_offset"][0]
    gaze_dy = v["gaze_offset"][1]

    # Left eye
    if eye_r_L > 0:
        draw.ellipse([eye_x_L - eye_r_L, eye_y - eye_r_L,
                      eye_x_L + eye_r_L, eye_y + eye_r_L],
                     fill=SCLERA)
        pupil_r = max(1, eye_r_L - 1)
        px = int(eye_x_L + gaze_dx * eye_r_L)
        py = int(eye_y + gaze_dy * eye_r_L)
        draw.ellipse([px - pupil_r, py - pupil_r, px + pupil_r, py + pupil_r],
                     fill=PUPIL)

    # Right eye
    if eye_r_R > 0:
        draw.ellipse([eye_x_R - eye_r_R, eye_y - eye_r_R,
                      eye_x_R + eye_r_R, eye_y + eye_r_R],
                     fill=SCLERA)
        pupil_r = max(1, eye_r_R - 1)
        px = int(eye_x_R + gaze_dx * eye_r_R)
        py = int(eye_y + gaze_dy * eye_r_R)
        draw.ellipse([px - pupil_r, py - pupil_r, px + pupil_r, py + pupil_r],
                     fill=PUPIL)

    # Brows
    brow_y = int(head_cy - head_r * 0.48)
    if v["brow_L_angle"] != 0.0 or eye_r_L > 0:
        brow_line(draw, cx, brow_y, "L", v["brow_L_angle"], head_r, hair_color)
    if v["brow_R_angle"] != 0.0 or eye_r_R > 0:
        brow_line(draw, cx, brow_y, "R", v["brow_R_angle"], head_r, hair_color)

    # Mouth
    mouth_h = max(0, round(v["mouth_h"] * head_r))
    mouth_w = max(0, round(v["mouth_w"] * head_r))
    mouth_y = int(head_cy + head_r * 0.38)

    if mouth_h == 0 and mouth_w > 0:
        # Compressed line
        draw.line([(cx - mouth_w, mouth_y), (cx + mouth_w, mouth_y)],
                  fill=MOUTH, width=1)
    elif mouth_h > 0 and mouth_w > 0:
        draw.ellipse([cx - mouth_w, mouth_y - mouth_h,
                      cx + mouth_w, mouth_y + mouth_h],
                     fill=MOUTH)


def draw_byte_pixel_eye(draw, ox, oy, cell, style):
    """Draw a 5×5 pixel-grid Byte eye at origin (ox, oy) with given cell size.

    Args:
        draw  : ImageDraw.Draw instance
        ox    : left edge x of the 5×5 grid
        oy    : top edge y of the 5×5 grid
        cell  : pixel cell size in px (1 = sprint scale, 2–3 = zoomed)
        style : "normal"   — DEEP_CYAN filled 5×5 with outline (left eye)
                "cracked"  — HOT_MAG diagonal crack, dead-zone upper-right (right eye)
                "searching" — scan-line (lit middle row only)
                "off"      — dark/void pixels (powered down)
    """
    c = max(1, cell)
    grid = 5

    if style == "normal":
        # Full 5×5 DEEP_CYAN grid — canonical left eye
        for row in range(grid):
            for col in range(grid):
                draw.rectangle(
                    [ox + col * c, oy + row * c,
                     ox + col * c + c - 1, oy + row * c + c - 1],
                    fill=BYTE_EYE_NORMAL)

    elif style == "cracked":
        # Right eye: cracked eye glyph per Alex Chen C13 spec.
        # Dead zone: upper-right quadrant (rows 0-1, cols 3-4).
        # HOT_MAGENTA crack: diagonal from (0,4) top-right corner to (4,0) bottom-left.
        # Alive zone: lower-left pixels in BYTE_EYE_NORMAL.
        dead_zone = {(r, c) for r in range(2) for c in range(3, 5)}
        # crack pixels: rough diagonal
        crack_pixels = {(0, 4), (1, 3), (1, 4), (2, 2), (2, 3), (3, 1), (3, 2), (4, 0), (4, 1)}
        for row in range(grid):
            for col in range(grid):
                if (row, col) in crack_pixels:
                    fill = BYTE_HOT_MAG
                elif (row, col) in dead_zone:
                    fill = BYTE_EYE_DEAD
                else:
                    fill = BYTE_EYE_NORMAL
                draw.rectangle(
                    [ox + col * c, oy + row * c,
                     ox + col * c + c - 1, oy + row * c + c - 1],
                    fill=fill)

    elif style == "searching":
        # Scan-line: only middle row lit (row 2), rest dark
        for row in range(grid):
            for col in range(grid):
                fill = BYTE_EYE_NORMAL if row == 2 else BYTE_EYE_DEAD
                draw.rectangle(
                    [ox + col * c, oy + row * c,
                     ox + col * c + c - 1, oy + row * c + c - 1],
                    fill=fill)

    elif style == "off":
        # Powered down: all dark
        for row in range(grid):
            for col in range(grid):
                draw.rectangle(
                    [ox + col * c, oy + row * c,
                     ox + col * c + c - 1, oy + row * c + c - 1],
                    fill=BYTE_EYE_DEAD)


def draw_byte_pixel_mouth(draw, cx, mouth_y, cell, style):
    """Draw an optional pixel mouth for Byte expressions.

    Args:
        draw     : ImageDraw.Draw
        cx       : horizontal center x
        mouth_y  : y coordinate of mouth row
        cell     : pixel cell size
        style    : "flat" | "frown" | "uptick" | "none"
    """
    c = max(1, cell)
    if style == "none":
        return
    mouth_w_cells = 5  # 5-pixel wide

    if style == "flat":
        # Single horizontal row of 5 pixels
        x0 = cx - (mouth_w_cells * c) // 2
        for col in range(mouth_w_cells):
            draw.rectangle(
                [x0 + col * c, mouth_y,
                 x0 + col * c + c - 1, mouth_y + c - 1],
                fill=BYTE_VOID)

    elif style == "frown":
        # V-shape: outer cells 1px lower than center
        x0 = cx - (mouth_w_cells * c) // 2
        offsets = [c, 0, 0, 0, c]  # outer cells drop down
        for col in range(mouth_w_cells):
            draw.rectangle(
                [x0 + col * c, mouth_y + offsets[col],
                 x0 + col * c + c - 1, mouth_y + offsets[col] + c - 1],
                fill=BYTE_VOID)

    elif style == "uptick":
        # Inverted V: outer cells 1px higher
        x0 = cx - (mouth_w_cells * c) // 2
        offsets = [-c, 0, 0, 0, -c]
        for col in range(mouth_w_cells):
            draw.rectangle(
                [x0 + col * c, mouth_y + offsets[col],
                 x0 + col * c + c - 1, mouth_y + offsets[col] + c - 1],
                fill=BYTE_VOID)


def draw_byte_face(draw, cx, body_cy, body_rx, body_ry, variant, cell_size):
    """Draw Byte's pixel-grid face onto the body oval.

    Eyes are placed in the upper half of the oval.
    No nose, no brows. Optional pixel mouth below eye line.

    Args:
        draw      : ImageDraw.Draw
        cx        : horizontal center of the oval body
        body_cy   : vertical center of the oval body
        body_rx   : horizontal radius of the oval body
        body_ry   : vertical radius of the oval body
        variant   : Byte variant dict
        cell_size : pixel cell size (1 at sprint scale)
    """
    v = variant
    c = max(1, cell_size)
    eye_grid = 5 * c   # total width/height of 5×5 eye grid at this cell size
    eye_y_frac = v["eye_y_frac"]

    # Eye centres: offset from oval centre
    eye_center_y = int(body_cy + eye_y_frac * body_ry)
    eye_sep = int(body_rx * 0.42)  # horizontal separation from center

    # Left eye origin (top-left of grid)
    lex_orig = cx - eye_sep - eye_grid // 2
    ley_orig = eye_center_y - eye_grid // 2

    # Right eye origin (top-left of grid)
    rex_orig = cx + eye_sep - eye_grid // 2
    rey_orig = eye_center_y - eye_grid // 2

    left_style  = v["left_eye_style"]
    right_style = v["right_eye_style"]

    if v["eye_size_px"] == 0:
        # "too small" test — draw as single pixels
        if left_style != "off":
            draw.point((cx - eye_sep, eye_center_y), fill=BYTE_EYE_NORMAL)
        if right_style != "off":
            draw.point((cx + eye_sep, eye_center_y), fill=BYTE_HOT_MAG)
    else:
        draw_byte_pixel_eye(draw, lex_orig, ley_orig, c, left_style)
        draw_byte_pixel_eye(draw, rex_orig, rey_orig, c, right_style)

    # Optional pixel mouth — below oval centre
    mouth_y = int(body_cy + body_ry * 0.35)
    draw_byte_pixel_mouth(draw, cx, mouth_y, c, v["mouth_style"])


def check_byte_face_gate(variant):
    """Run face gate checks for a Byte variant.

    Checks:
      FG-B01  eye_count: expected gate_eye_count visible eyes present
      FG-B02  differentiation: left/right eyes are visually distinct (gate_differentiated)
      FG-B03  pixel_grid_proportions: eye_size_px >= 1 (spec minimum)

    Returns:
        dict with keys: eye_count (PASS/FAIL), differentiation (PASS/FAIL/SKIP),
                        pixel_grid (PASS/FAIL), overall (PASS/WARN/FAIL)
    """
    v = variant
    results = {}

    # FG-B01 eye count
    visible = 0
    if v["left_eye_style"] != "off":
        visible += 1
    if v["right_eye_style"] != "off":
        visible += 1
    expected = v["gate_eye_count"]
    results["eye_count"] = "PASS" if visible == expected else "FAIL"

    # FG-B02 differentiation
    if not v["gate_differentiated"]:
        results["differentiation"] = "SKIP"
    else:
        diff = (v["left_eye_style"] != v["right_eye_style"])
        results["differentiation"] = "PASS" if diff else "FAIL"

    # FG-B03 pixel grid proportions
    results["pixel_grid"] = "PASS" if v["eye_size_px"] >= 1 else "FAIL"

    # Overall
    checks = [r for r in results.values() if r != "SKIP"]
    if "FAIL" in checks:
        results["overall"] = "FAIL"
    elif v["readability"] == "WARN":
        results["overall"] = "WARN"
    else:
        results["overall"] = "PASS"

    return results


def render_panel(char_name, head_r, variant, scale, panel_w, panel_h):
    """Render a single variant panel. Returns a PIL Image.

    For Byte: head_r is used as the oval body's Y-radius (wider-than-tall oval).
    Byte's face is drawn with pixel-grid eyes; no torso stub (Byte body IS the oval).
    """
    skin  = CHAR_SKIN[char_name]
    body  = CHAR_BODY[char_name]
    hair  = CHAR_HAIR[char_name]

    panel = Image.new("RGB", (panel_w, panel_h), PANEL_BG)
    draw  = ImageDraw.Draw(panel)

    # ── Left sub-panel: ACTUAL sprint scale (head_r as specified) ───────────
    left_w = panel_w // 2 - 4
    actual_cx = left_w // 2
    actual_cy = panel_h // 2 - 8

    if char_name == "byte":
        # Byte: oval body only (no separate torso stub)
        body_rx = int(head_r * 1.15)
        body_ry = int(head_r * 0.90)
        draw_head_base(draw, actual_cx, actual_cy, head_r, skin, hair, char_name)
        # Draw lower-limb nubs below oval
        limb_y = actual_cy + body_ry + 1
        limb_w = max(2, int(head_r * 0.18))
        limb_h = max(3, int(head_r * 0.35))
        for lx in [actual_cx - int(head_r * 0.35), actual_cx + int(head_r * 0.35)]:
            draw.ellipse([lx - limb_w, limb_y, lx + limb_w, limb_y + limb_h],
                         fill=body)
        draw_byte_face(draw, actual_cx, actual_cy, body_rx, body_ry, variant, 1)
    else:
        # Body stub (minimal)
        torso_w = max(4, int(head_r * 1.4))
        torso_h = max(6, int(head_r * 2.3))
        torso_top = actual_cy + head_r + 1
        draw.ellipse([actual_cx - torso_w // 2, torso_top,
                      actual_cx + torso_w // 2, torso_top + torso_h],
                     fill=body)
        draw_head_base(draw, actual_cx, actual_cy, head_r, skin, hair, char_name)
        draw_face(draw, actual_cx, actual_cy, head_r, variant, hair)

    # Label: "R=23px"
    label_small = f"r={head_r}px"
    draw.text((2, panel_h - 16), label_small, fill=(120, 120, 140))

    # Divider line
    draw.line([(left_w + 2, 4), (left_w + 2, panel_h - 4)],
              fill=PANEL_BORDER, width=1)

    # ── Right sub-panel: ZOOMED (head_r * scale) ────────────────────────────
    zoom_r = head_r * scale
    right_cx = left_w + 8 + (panel_w - left_w - 8) // 2
    right_cy = actual_cy

    if char_name == "byte":
        body_rx_z = int(zoom_r * 1.15)
        body_ry_z = int(zoom_r * 0.90)
        draw_head_base(draw, right_cx, right_cy, zoom_r, skin, hair, char_name)
        limb_y_z = right_cy + body_ry_z + 1
        limb_w_z = max(2, int(zoom_r * 0.18))
        limb_h_z = max(3, int(zoom_r * 0.35))
        for lx in [right_cx - int(zoom_r * 0.35), right_cx + int(zoom_r * 0.35)]:
            draw.ellipse([lx - limb_w_z, limb_y_z, lx + limb_w_z, limb_y_z + limb_h_z],
                         fill=body)
        draw_byte_face(draw, right_cx, right_cy, body_rx_z, body_ry_z, variant, scale)
    else:
        torso_w_z = max(4, int(zoom_r * 1.4))
        torso_h_z = max(6, int(zoom_r * 2.3))
        torso_top_z = right_cy + zoom_r + 1
        draw.ellipse([right_cx - torso_w_z // 2, torso_top_z,
                      right_cx + torso_w_z // 2, torso_top_z + torso_h_z],
                     fill=body)
        draw_head_base(draw, right_cx, right_cy, zoom_r, skin, hair, char_name)
        draw_face(draw, right_cx, right_cy, zoom_r, variant, hair)

    label_zoom = f"r={zoom_r}px ({scale}×)"
    draw.text((left_w + 4, panel_h - 16), label_zoom, fill=(120, 120, 140))

    return panel


def readability_color(r):
    if r == "PASS":
        return PASS_COLOR
    elif r == "WARN":
        return WARN_COLOR
    return FAIL_COLOR


def build_contact_sheet(char_name, head_r, variants, scale, out_path):
    """Build and save the contact sheet PNG."""
    n = len(variants)
    cols = 2
    rows = math.ceil(n / cols)

    # Compute panel size to fit within MAX_DIM (600×400 target)
    sheet_w = min(600, MAX_DIM)
    sheet_h = min(400, MAX_DIM)

    header_h = 32
    label_h  = 26
    usable_h = sheet_h - header_h

    panel_w = sheet_w // cols - 4
    panel_h = usable_h // rows - label_h - 4

    # Clamp panel dims
    panel_w = max(80, min(panel_w, 260))
    panel_h = max(60, min(panel_h, 180))

    actual_sheet_w = cols * (panel_w + 4) + 4
    actual_sheet_h = header_h + rows * (panel_h + label_h + 4) + 4

    # Apply hard limit
    actual_sheet_w = min(actual_sheet_w, MAX_DIM)
    actual_sheet_h = min(actual_sheet_h, MAX_DIM)

    sheet = Image.new("RGB", (actual_sheet_w, actual_sheet_h), (18, 18, 26))
    sd = ImageDraw.Draw(sheet)

    # Header
    header_text = f"LTG FACE TEST  |  char={char_name}  head_r={head_r}px  zoom={scale}x  |  cycle 35"
    sd.text((4, 8), header_text, fill=HEADER_COLOR)

    y_cursor = header_h + 2

    for idx, variant in enumerate(variants):
        col = idx % cols
        row = idx // cols

        px = 4 + col * (panel_w + 4)
        py = y_cursor + row * (panel_h + label_h + 4)

        # Render panel
        p = render_panel(char_name, head_r, variant, scale, panel_w, panel_h)
        sheet.paste(p, (px, py))

        # Panel border
        r_color = readability_color(variant["readability"])
        sd.rectangle([px - 1, py - 1, px + panel_w + 1, py + panel_h + 1],
                     outline=r_color, width=1)

        # Label area below panel
        label_y = py + panel_h + 2
        label_text = f"{variant['label']}  [{variant['readability']}]"
        desc_text  = variant["description"][:38]  # truncate if long

        sd.text((px, label_y), label_text, fill=r_color)
        sd.text((px, label_y + 13), desc_text, fill=(160, 160, 160))

    # Enforce max dimension
    sheet.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)
    sheet.save(out_path)
    print(f"[face_test] Saved: {out_path}  ({sheet.width}×{sheet.height}px)")
    return out_path


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="LTG Character Face Legibility Test — sprint/wide-shot scale."
    )
    parser.add_argument("--char",     default="luma",
                        choices=["luma", "cosmo", "miri", "byte"],
                        help="Character to test (default: luma)")
    parser.add_argument("--head-r",   type=int, default=23,
                        help="Head radius in pixels (default: 23 — SF02 sprint scale)")
    parser.add_argument("--variants", type=int, default=6,
                        choices=[4, 6, 8],
                        help="Number of variants (default: 6)")
    parser.add_argument("--scale",    type=int, default=3,
                        help="Zoom multiplier for right sub-panel (default: 3)")
    parser.add_argument("--output",   default=None,
                        help="Output PNG path (default: auto-named)")
    args = parser.parse_args()

    char_name = args.char
    head_r    = max(10, min(60, args.head_r))
    n_variants = args.variants
    scale     = max(1, min(6, args.scale))

    all_variants = VARIANT_REGISTRY.get(char_name, LUMA_VARIANTS)
    variants = all_variants[:n_variants]

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           os.pardir, "production")
    os.makedirs(out_dir, exist_ok=True)

    if args.output:
        out_path = args.output
    else:
        out_path = os.path.join(out_dir,
                                f"LTG_TOOL_face_test_{char_name}_r{head_r}_v001.png")

    out_path = os.path.abspath(out_path)
    build_contact_sheet(char_name, head_r, variants, scale, out_path)

    # Print summary
    print("\n── Face Readability Summary ─────────────────────────────────")
    for v in variants:
        r = v["readability"]
        color_tag = {"PASS": "OK", "WARN": "!!", "FAIL": "XX"}[r]
        print(f"  [{color_tag}] {v['label']:<18s}  {v['readability']}  — {v['description']}")
    print()

    if char_name == "byte":
        print("── Byte Face Gate Checks (FG-B01 / FG-B02 / FG-B03) ────────")
        overall_fail = False
        overall_warn = False
        for v in variants:
            gate = check_byte_face_gate(v)
            o = gate["overall"]
            if o == "FAIL":
                overall_fail = True
            elif o == "WARN":
                overall_warn = True
            ec_tag = {"PASS": "OK", "FAIL": "XX"}.get(gate["eye_count"], "OK")
            df_tag = {"PASS": "OK", "FAIL": "XX", "SKIP": "--"}.get(gate["differentiation"], "--")
            pg_tag = {"PASS": "OK", "FAIL": "XX"}.get(gate["pixel_grid"], "OK")
            overall_tag = {"PASS": "OK", "WARN": "!!", "FAIL": "XX"}[o]
            print(f"  [{overall_tag}] {v['label']:<18s}  "
                  f"eye_count=[{ec_tag}]  diff=[{df_tag}]  px_grid=[{pg_tag}]")
        print()
        if overall_fail:
            print("GATE RESULT: FAIL — fix face geometry before submitting.")
        elif overall_warn:
            print("GATE RESULT: WARN — include this output in completion report.")
        else:
            print("GATE RESULT: PASS")
        print()
        print("Byte spec notes:")
        print("  FG-B01  eye_count: visible eyes match expected gate_eye_count")
        print("  FG-B02  differentiation: left (normal) != right (cracked)")
        print("  FG-B03  pixel_grid: eye_size_px >= 1 (5×5 grid must be rendered)")
        print(f"  Sprint scale: at head_r={head_r}px, eye grid = 5×5 px.")
        print(f"                eye_size_px=0 (1-dot) is FAIL at sprint scale.")
    else:
        print(f"Scale note: At head_r={head_r}px, eye_r=4px (0.17×head_r) is minimum readable.")
        print(f"           eye_r ≤ 2px (0.09×head_r) is FAIL at sprint scale.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
