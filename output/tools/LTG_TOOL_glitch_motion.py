# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_glitch_motion.py
Ryo Hasegawa / Cycle 45
Motion Spec Sheet — GLITCH (Glitchkin antagonist)
4 panels: PREDATORY STILL | COVETOUS REACH | CORRUPTION SURGE | RETREAT

Beat arc per Alex Chen C44 brief:
  B1: PREDATORY STILL — absolute stillness (no idle hover, no confetti).
      Wrongness IS the absence of motion. Held state, indefinite duration.
  B2: COVETOUS REACH — desire-state. One arm-spike slowly extends toward subject.
      Very slow, smooth arc. Eyes bilateral acid-slit (interior state = real feeling).
      Minimal UV_PURPLE confetti only.
  B3: CORRUPTION SURGE — loss of composure. Body scale pulses ±15% (grow then shrink).
      Jittery, staccato. Crack line brightens (HOT_MAG arc). Spike_h increases.
      HOT_MAG+UV_PURPLE confetti max spread.
  B4: RETREAT — repelled/thwarted. Rapid body compression + backward displacement.
      Reads as coil-back, not defeat. Still dangerous. Eyes: panicked HOT ring.

Canonical Glitch body spec (from glitch.md — all generators must follow):
  - Body fill: CORRUPT_AMBER (255,140,0) — digital warm (NOT organic warm)
  - Shadow: UV_PURPLE (123,47,190) offset +3,+4
  - Highlight facet: CORRUPT_AMB_HL (255,185,80) — top-left triangle
  - Outline: VOID_BLACK (10,10,20) width=3
  - Crack: HOT_MAG (255,45,107) diagonal + fork — ALWAYS visible
  - rx=34, ry=38 base (scaled up here for motion doc clarity)
  - ry > rx (taller than wide — G002 spec)
  NOTE: Alex Chen C44 brief incorrectly states Glitch uses Void/Cyan/UV palette only.
  Glitch body IS CORRUPT_AMBER per glitch.md (Maya Santos C32, confirmed canonical spec).
  Discrepancy flagged in Alex inbox. Canonical spec followed here.

Canvas: 1280x720 (<=1280 limit)
Output: output/characters/motion/LTG_CHAR_glitch_motion.png
"""
from __future__ import annotations

import math
import os
import sys
import json
import random

from PIL import Image, ImageDraw

# --- Path setup ---
_TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOL_DIR not in sys.path:
    sys.path.insert(0, _TOOL_DIR)

# --- Canonical character renderer ---
from LTG_TOOL_char_glitch import draw_glitch
from LTG_TOOL_cairo_primitives import to_pil_rgba

# --- Load config ---
_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "sheet_geometry_config.json")


def _load_header_h_glitch(default=56):
    """Load HEADER_H for glitch family from sheet_geometry_config.json."""
    try:
        with open(_CONFIG_PATH) as f:
            cfg = json.load(f)
        geo = cfg.get("families", {}).get("glitch", {})
        return geo.get("panel_top_abs", default)
    except Exception:
        return default


_GLITCH_PANEL_TOP = _load_header_h_glitch(default=56)

# --- CANONICAL COLORS (from glitch.md §2.2 — Maya Santos C32) ---
CORRUPT_AMB     = (255, 140,   0)   # #FF8C00 Main body fill
CORRUPT_AMB_SH  = (168,  76,   0)   # #A84C00 Shadow amber
CORRUPT_AMB_HL  = (255, 185,  80)   # #FFB950 Highlight facet
HOT_MAG         = (255,  45, 107)   # #FF2D6B crack + confetti
UV_PURPLE       = (123,  47, 190)   # #7B2FBE shadow + confetti
VOID_BLACK      = ( 10,  10,  20)   # #0A0A14 outline + panel background
SOFT_GOLD       = (232, 201,  90)   # #E8C95A Triumphant eye state
ACID_GREEN      = ( 57, 255,  20)   # #39FF14 Mischievous/Covetous eye state
ELEC_CYAN       = (  0, 240, 255)   # #00F0FF involuntary confetti leak only (PANICKED)

# Annotation colors — dark sheet
ANNOTATION_BG   = ( 22,  18,  32)   # dark near-void panel background
PANEL_BORDER    = ( 60,  50,  80)   # dim purple-grey border
LABEL_BG        = CORRUPT_AMB       # amber label on dark background
LABEL_TEXT      = VOID_BLACK        # void black text on amber
MOTION_ARROW    = CORRUPT_AMB       # amber — secondary motion arrows
BEAT_COLOR      = CORRUPT_AMB       # amber beats (matches character palette)
ACCENT_DASH     = ( 80,  60, 100)   # dim purple guide lines
ANNOT_TEXT      = (220, 200, 160)   # warm off-white annotations on dark bg

# --- CANVAS ---
W, H         = 1280, 720
COLS         = 4
PAD          = 14
HEADER_H     = 44
_TITLE_H     = max(_GLITCH_PANEL_TOP - PAD, 40)
PANEL_W      = (W - PAD * (COLS + 1)) // COLS
PANEL_H      = H - PAD * 2 - _GLITCH_PANEL_TOP

# Glitch body scale (larger than expression sheet rx=34 for motion doc clarity)
RX = 44
RY = 50


# ------------------------------------------------------------------ helpers

def panel_origin(col):
    """Top-left (x, y) of panel col (0-based)."""
    x = PAD + col * (PANEL_W + PAD)
    y = _GLITCH_PANEL_TOP
    return x, y


def draw_arrow(draw, x0, y0, x1, y1, color=None, width=2, head=8):
    color = color or MOTION_ARROW
    draw.line([(x0, y0), (x1, y1)], fill=color, width=width)
    angle = math.atan2(y1 - y0, x1 - x0)
    for da in (-0.4, 0.4):
        ax = x1 - head * math.cos(angle + da)
        ay = y1 - head * math.sin(angle + da)
        draw.line([(x1, y1), (int(ax), int(ay))], fill=color, width=width)


def label_box(draw, x, y, text, bg=None, fg=None, pad=4):
    bg = bg or LABEL_BG
    fg = fg or LABEL_TEXT
    bbox = draw.textbbox((0, 0), text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rectangle([x, y, x + tw + pad * 2, y + th + pad * 2], fill=bg)
    draw.text((x + pad, y + pad), text, fill=fg)
    return tw + pad * 2, th + pad * 2


def annot_text(draw, x, y, text, color=None):
    draw.text((x, y), text, fill=color or ANNOT_TEXT)


# ------------------------------------------------------------------ Glitch body
# Canonical renderer: draw_glitch() from LTG_TOOL_char_glitch.py

# Expression mapping for motion beats:
#   B1 PREDATORY STILL -> calculating
#   B2 COVETOUS REACH  -> covetous
#   B3 CORRUPTION SURGE -> panicked
#   B4 RETREAT          -> stunned

def render_glitch_to_panel(expression, scale=1.3):
    """Render Glitch via canonical renderer, return cropped PIL RGBA image.

    Args:
        expression: one of the canonical expressions (calculating, covetous, panicked, stunned, etc.)
        scale: size multiplier for the canonical renderer

    Returns:
        PIL RGBA image, tightly cropped to character bounds.
    """
    surface = draw_glitch(expression=expression, scale=scale)
    char_img = to_pil_rgba(surface)
    bbox = char_img.getbbox()
    if bbox:
        char_img = char_img.crop(bbox)
    return char_img


def paste_glitch_in_panel(img, draw, cx, cy, expression, scale=1.3, target_h=None):
    """Render Glitch and paste centered at (cx, cy) on the motion sheet.

    Args:
        img: PIL Image (motion sheet)
        draw: ImageDraw for img
        cx, cy: center position on the sheet
        expression: canonical expression string
        scale: renderer scale
        target_h: optional target height to resize to

    Returns:
        (img, draw, char_bbox) where char_bbox is (left, top, right, bottom)
        of the pasted character on the sheet.
    """
    char_img = render_glitch_to_panel(expression, scale=scale)
    if target_h and char_img.height > 0:
        ratio = target_h / char_img.height
        new_w = max(1, int(char_img.width * ratio))
        char_img = char_img.resize((new_w, target_h), Image.LANCZOS)

    paste_x = cx - char_img.width // 2
    paste_y = cy - char_img.height // 2

    # Convert to RGBA for alpha composite
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    img.paste(char_img, (paste_x, paste_y), char_img)
    if img.mode == "RGBA":
        img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    char_bbox = (paste_x, paste_y,
                 paste_x + char_img.width, paste_y + char_img.height)
    return img, draw, char_bbox


# ------------------------------------------------------------------ beat badge + frame

def draw_beat_badge(draw, ox, oy, beat_num, label):
    """Amber beat badge in upper-left of panel, expression label below."""
    bx, by = ox + 6, oy + 6
    badge_text = f"B{beat_num}"
    bbox = draw.textbbox((0, 0), badge_text)
    bw = bbox[2] - bbox[0] + 12
    bh = bbox[3] - bbox[1] + 8
    draw.rectangle([bx, by, bx + bw, by + bh], fill=BEAT_COLOR)
    draw.text((bx + 6, by + 4), badge_text, fill=VOID_BLACK)
    draw.text((bx, by + bh + 4), label, fill=CORRUPT_AMB)


def draw_panel_frame(draw, ox, oy, pw, ph):
    draw.rectangle([ox, oy, ox + pw, oy + ph], outline=PANEL_BORDER, width=2)


# ===================================================================== panels

def draw_panel_b1(img, draw, col):
    """B1: PREDATORY STILL — absolute stillness. No hover, no confetti. Wrongness = absence of motion."""
    ox, oy = panel_origin(col)
    pw, ph = PANEL_W, PANEL_H
    cx = ox + pw // 2
    cy = oy + int(ph * 0.44)

    # Canonical renderer: calculating expression = acid-X eyes, neutral body
    target_h = int(ph * 0.55)
    img, draw, cbbox = paste_glitch_in_panel(
        img, draw, cx, cy, expression="calculating",
        scale=1.3, target_h=target_h)
    cy_top = cbbox[1]

    # NO HOVER INDICATOR — stillness is the annotation
    hx, hy = cx - 52, oy + 22
    draw.text((hx, hy), "NO HOVER", fill=HOT_MAG)
    draw.text((hx, hy + 14), "NO CONFETTI", fill=HOT_MAG)

    # Static lines = held / frozen (light construction marks)
    for i in range(3):
        draw.line([(cx - 50, cy - 10 + i * 10), (cx - 46, cy - 10 + i * 10)],
                  fill=ACCENT_DASH, width=1)
        draw.line([(cx + 46, cy - 10 + i * 10), (cx + 50, cy - 10 + i * 10)],
                  fill=ACCENT_DASH, width=1)

    # Spike still annotation
    annot_text(draw, cx + 8, cy_top - 12, "spike_h=10", color=CORRUPT_AMB)

    # Duration annotation
    annot_text(draw, ox + 6, oy + ph - 54, "tilt: 0\u00b0  squash: 1.0", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 40, "duration: HELD (indefinite)", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 26, "eyes: acid-X (CALCULATING)", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 12, "wrongness = absence of idle motion", color=CORRUPT_AMB)

    draw_beat_badge(draw, ox, oy, 1, "PREDATORY STILL")
    draw_panel_frame(draw, ox, oy, pw, ph)


def draw_panel_b2(img, draw, col):
    """B2: COVETOUS REACH — desire-state. Slow extension of right arm toward subject."""
    ox, oy = panel_origin(col)
    pw, ph = PANEL_W, PANEL_H
    cx = ox + pw // 2
    cy = oy + int(ph * 0.44)

    # Canonical renderer: covetous expression — bilateral eyes, tilt lean
    target_h = int(ph * 0.55)
    img, draw, cbbox = paste_glitch_in_panel(
        img, draw, cx, cy, expression="covetous",
        scale=1.3, target_h=target_h)
    cy_top = cbbox[1]
    right_x = cbbox[2]
    right_y = cy

    # Slow arc arrow on extending right arm — smooth, long reach
    draw_arrow(draw, right_x - 10, right_y - 6,
               right_x + 20, right_y - 22,
               color=MOTION_ARROW, width=2, head=7)
    annot_text(draw, right_x + 4, right_y - 36, "SLOW extend", color=MOTION_ARROW)
    annot_text(draw, right_x + 4, right_y - 22, "toward subject", color=ANNOT_TEXT)

    # Bilateral eye callout (key character read)
    annot_text(draw, ox + 6, cy_top - 48, "BILATERAL eyes:", color=SOFT_GOLD)
    annot_text(draw, ox + 6, cy_top - 34, "acid-slit both sides", color=ACID_GREEN)
    annot_text(draw, ox + 6, cy_top - 20, "= REAL interior state", color=ANNOT_TEXT)

    # Speed annotation
    annot_text(draw, ox + 6, oy + ph - 54, "tilt: +12\u00b0 (toward subject)", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 40, "speed: very slow, smooth arc", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 26, "confetti: UV_PURPLE only (4px)", color=UV_PURPLE)
    annot_text(draw, ox + 6, oy + ph - 12, "right arm-spike: extended +14px toward subject", color=ANNOT_TEXT)

    draw_beat_badge(draw, ox, oy, 2, "COVETOUS REACH")
    draw_panel_frame(draw, ox, oy, pw, ph)


def draw_panel_b3(img, draw, col):
    """B3: CORRUPTION SURGE — body scale pulses +15%, jittery. Crack brightens."""
    ox, oy = panel_origin(col)
    pw, ph = PANEL_W, PANEL_H
    cx = ox + pw // 2
    cy = oy + int(ph * 0.44)

    # Canonical renderer: panicked expression — HOT ring eyes, stretched body
    target_h = int(ph * 0.62)  # +15% surge = slightly larger
    img, draw, cbbox = paste_glitch_in_panel(
        img, draw, cx, cy, expression="panicked",
        scale=1.5, target_h=target_h)
    cy_top = cbbox[1]

    # Ghost body at neutral scale annotation
    ghost_top_y = cy - int(RY * 1.0)
    draw.line([(cx, ghost_top_y), (cx, ghost_top_y - 40)], fill=ACCENT_DASH, width=1)
    annot_text(draw, cx + 6, ghost_top_y - 8, "neutral top (ghost)", color=ACCENT_DASH)

    # Scale pulse arrows (expand and compress — staccato)
    draw_arrow(draw, cx - RX - 30, cy, cx - RX - 50, cy,
               color=BEAT_COLOR, width=2, head=6)
    draw_arrow(draw, cx + RX + 30, cy, cx + RX + 50, cy,
               color=BEAT_COLOR, width=2, head=6)
    annot_text(draw, cx - RX - 78, cy + 6, "\u00b115%", color=CORRUPT_AMB)

    # Crack brightened callout
    annot_text(draw, ox + 6, cy_top - 24, "crack brightens:", color=SOFT_GOLD)
    annot_text(draw, ox + 6, cy_top - 10, "HOT_MAG \u2192 SOFT_GOLD arc", color=SOFT_GOLD)

    # Jitter annotation (not drawn — temporal, described in text)
    annot_text(draw, ox + 6, oy + ph - 54, "body: \u00b115% scale pulse, staccato fast", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 40, "spike_h=16 (elevated energy — loss of control)", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 26, "confetti: HOT_MAG+UV_PURPLE max (18px)", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 12, "jitter: body oscillation x+y \u00b14px per frame", color=CORRUPT_AMB)

    draw_beat_badge(draw, ox, oy, 3, "CORRUPTION SURGE")
    draw_panel_frame(draw, ox, oy, pw, ph)


def draw_panel_b4(img, draw, col):
    """B4: RETREAT — rapid compression + backward displacement. Coil-back, not defeat."""
    ox, oy = panel_origin(col)
    pw, ph = PANEL_W, PANEL_H
    cx = ox + pw // 2 + 20   # displaced right (retreating to viewer's right = away from subject)
    cy = oy + int(ph * 0.47)  # shifted down slightly for squash display

    # Canonical renderer: stunned expression — compressed, recoil
    target_h = int(ph * 0.48)  # squashed = shorter
    img, draw, cbbox = paste_glitch_in_panel(
        img, draw, cx, cy, expression="stunned",
        scale=1.3, target_h=target_h)
    cy_top = cbbox[1]

    # Displacement direction arrow (backward = to the right in this composition)
    draw_arrow(draw, cx - 50, cy - 30, cx - 80, cy - 30,
               color=BEAT_COLOR, width=2, head=7)
    annot_text(draw, cx - 110, cy - 44, "backward", color=CORRUPT_AMB)
    annot_text(draw, cx - 114, cy - 30, "displacement", color=ANNOT_TEXT)

    # Squash annotation
    annot_text(draw, cx + 6, cy_top + 4, "squash=0.65", color=CORRUPT_AMB)

    # Danger callout — still dangerous
    annot_text(draw, ox + 6, oy + ph - 54, "tilt: -20\u00b0 (recoil away from subject)", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 40, "squash: 0.65 — compressed, not flattened", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 26, "speed: RAPID (1-2 frames to full compression)", color=ANNOT_TEXT)
    annot_text(draw, ox + 6, oy + ph - 12, "reads as COIL-BACK not defeat — still dangerous", color=CORRUPT_AMB)

    draw_beat_badge(draw, ox, oy, 4, "RETREAT")
    draw_panel_frame(draw, ox, oy, pw, ph)


# ===================================================================== main

def build_sheet():
    img = Image.new("RGB", (W, H), VOID_BLACK)
    draw = ImageDraw.Draw(img)

    # --- Header ---
    draw.rectangle([0, 0, W, _GLITCH_PANEL_TOP - 1], fill=(18, 12, 28))
    draw.text((PAD, 8), "GLITCH \u2014 Motion Spec Sheet", fill=CORRUPT_AMB)
    draw.text((PAD, 24),
              "Ryo Hasegawa / C45  |  Beat arc: PREDATORY STILL \u2192 COVETOUS REACH \u2192 CORRUPTION SURGE \u2192 RETREAT",
              fill=ANNOT_TEXT)
    draw.text((PAD, 38),
              "Amber arrows = secondary motion.  Amber badge = beat timing.  BILATERAL eyes = interior state (G008).  CORRUPT_AMBER body (glitch.md canonical).",
              fill=ACCENT_DASH)

    # --- Panel backgrounds ---
    for col in range(COLS):
        ox, oy = panel_origin(col)
        draw.rectangle([ox, oy, ox + PANEL_W, oy + PANEL_H], fill=(14, 10, 22))

    # --- Draw panels ---
    draw_panel_b1(img, draw, 0)
    draw_panel_b2(img, draw, 1)
    draw_panel_b3(img, draw, 2)
    draw_panel_b4(img, draw, 3)

    # --- Size guard ---
    img.thumbnail((1280, 1280))

    # --- Save ---
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "characters", "motion")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "LTG_CHAR_glitch_motion.png")
    img.save(out_path)
    print(f"Saved: {out_path}  ({img.width}x{img.height})")
    return out_path


if __name__ == "__main__":
    build_sheet()
