#!/usr/bin/env python3
"""
LTG_TOOL_character_face_test_v001.py
Character Face Legibility Test — Sprint/Wide-Shot Scale

Renders a character head at sprint/wide-shot scale (head_r = 20–25px range) and
draws candidate facial expressions — varying eye sizes, brow angles, mouth shapes —
as a contact sheet of 6–8 variants. Output ≤ 600×400px reference PNG.

Purpose:
  Prevent "invisible at sprint scale" expression problems before they enter full
  SF generator iteration cycles. Run this before modifying face geometry in any
  SF generator to confirm the expression reads at the target render scale.

Usage:
  python3 LTG_TOOL_character_face_test_v001.py [options]

  --char       CHARACTER   Character to test: luma (default), cosmo, miri
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

Author: Lee Tanaka — Character Staging & Visual Acting Specialist
Cycle: 35 (C34 ideabox idea, actioned C35)
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

VARIANT_REGISTRY = {
    "luma":  LUMA_VARIANTS,
    "cosmo": COSMO_VARIANTS,
    "miri":  MIRI_VARIANTS,
}

CHAR_SKIN = {
    "luma":  LUMA_SKIN_STORM,
    "cosmo": COSMO_SKIN,
    "miri":  MIRI_SKIN,
}
CHAR_BODY = {
    "luma":  LUMA_HOODIE_STORM,
    "cosmo": COSMO_JACKET,
    "miri":  MIRI_CARDIGAN,
}
CHAR_HAIR = {
    "luma":  LUMA_HAIR,
    "cosmo": COSMO_HAIR,
    "miri":  MIRI_HAIR,
}


# ── Drawing functions ─────────────────────────────────────────────────────────

def draw_head_base(draw, cx, cy, head_r, skin_color, hair_color, char_name):
    """Draw the head ellipse + basic hair for the character."""
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


def render_panel(char_name, head_r, variant, scale, panel_w, panel_h):
    """Render a single variant panel. Returns a PIL Image."""
    skin  = CHAR_SKIN[char_name]
    body  = CHAR_BODY[char_name]
    hair  = CHAR_HAIR[char_name]

    panel = Image.new("RGB", (panel_w, panel_h), PANEL_BG)
    draw  = ImageDraw.Draw(panel)

    # ── Left sub-panel: ACTUAL sprint scale (head_r as specified) ───────────
    left_w = panel_w // 2 - 4
    actual_cx = left_w // 2
    actual_cy = panel_h // 2 - 8

    # Body stub (minimal)
    torso_w = max(4, int(head_r * 1.4))
    torso_h = max(6, int(head_r * 2.3))
    torso_top = actual_cy + head_r + 1
    draw.ellipse([actual_cx - torso_w // 2, torso_top,
                  actual_cx + torso_w // 2, torso_top + torso_h],
                 fill=body)

    # Head
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
                        choices=["luma", "cosmo", "miri"],
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
    print(f"Scale note: At head_r={head_r}px, eye_r=4px (0.17×head_r) is minimum readable.")
    print(f"           eye_r ≤ 2px (0.09×head_r) is FAIL at sprint scale.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
