#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_scale_reference_sheet.py — Character-Environment Scale Reference
"Luma & the Glitchkin" — Environment Art / Hana Okonkwo / Cycle 50

Generates a reference sheet showing character heights relative to environment
landmarks (door frames, countertops, desks, chairs, lockers). This ensures
characters are the correct scale when composited into environments.

Character proportions from character_lineup.md:
  Cosmo:  ~4.3 Luma-heads tall (5'1")
  Luma:   ~3.5 Luma-heads tall (~4'8", 10yr old)
  Miri:   ~3.2 Luma-heads tall (5'0")
  Byte:   ~0.5 Luma-heads (6 inches, digital)

Environment landmarks (extracted from generators):
  Kitchen:   floor at ~82% canvas, counter at ~58%, upper cabinets at ~38%
  Hallway:   floor at ~85%, locker top at ~32%, ceiling at ~15%
  Classroom: floor at ~82%, desk top at ~65%, chalkboard at ~30%
  Study:     floor at ~80%, couch seat at ~62%, desk at ~55%

Output: output/production/LTG_SCALE_reference_sheet.png
"""

__version__ = "1.0.0"

import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

W, H = 1280, 720
BG_COLOR = (245, 240, 232)
GRID_COLOR = (200, 195, 185)
TEXT_COLOR = (80, 65, 50)
LABEL_COLOR = (120, 100, 80)

# Character colors (from palette)
LUMA_COLOR = (230, 140, 60)     # hoodie orange
COSMO_COLOR = (168, 155, 191)   # cardigan lavender
MIRI_COLOR = (195, 120, 65)     # cardigan warm
BYTE_COLOR = (100, 220, 220)    # electric cyan

# Character heights in "Luma heads" (from character_lineup.md)
LUMA_HEADS = 3.5
COSMO_HEADS = 4.3
MIRI_HEADS = 3.2
BYTE_HEADS = 0.5

# Environment Y coordinates (from generators, 1280x720 canvas)
# These are the key landmark Y positions characters interact with.
ENVIRONMENTS = {
    "Kitchen": {
        "floor_y": int(H * 0.82),       # 590
        "counter_y": int(H * 0.58),      # 418
        "upper_cab_y": int(H * 0.38),    # 274
        "door_top_y": int(H * 0.28),     # 202 (approx)
        "landmarks": [
            ("Floor", int(H * 0.82)),
            ("Countertop", int(H * 0.58)),
            ("Upper Cabinets", int(H * 0.38)),
            ("Door Frame Top", int(H * 0.28)),
        ]
    },
    "Hallway": {
        "floor_y": int(H * 0.85),       # 612
        "landmarks": [
            ("Floor", int(H * 0.85)),
            ("Locker Top", int(H * 0.32)),
            ("Door Frame Top", int(H * 0.26)),
            ("Ceiling", int(H * 0.15)),
        ]
    },
    "Classroom": {
        "floor_y": int(H * 0.82),       # 590
        "landmarks": [
            ("Floor", int(H * 0.82)),
            ("Desk Top", int(H * 0.65)),
            ("Chair Seat", int(H * 0.70)),
            ("Chalkboard Bottom", int(H * 0.42)),
            ("Chalkboard Top", int(H * 0.30)),
        ]
    },
    "Study": {
        "floor_y": int(H * 0.80),       # 576
        "landmarks": [
            ("Floor", int(H * 0.80)),
            ("Couch Seat", int(H * 0.62)),
            ("Desk Surface", int(H * 0.55)),
            ("Shelf", int(H * 0.35)),
        ]
    },
}

# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def draw_character_silhouette(draw, cx, base_y, head_units, head_px,
                              color, label, label_side="right"):
    """Draw a simplified character silhouette at the correct scale.

    This is intentionally simplified — a head circle + body rectangle.
    The point is scale reference, not character design.
    """
    total_h = int(head_units * head_px)
    top_y = base_y - total_h

    # Head
    head_r = head_px // 2
    head_cy = top_y + head_r
    draw.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
                 fill=color, outline=(60, 50, 40), width=1)

    # Body (torso + legs as simplified rectangle)
    body_top = head_cy + head_r
    body_w = max(4, int(head_px * 0.9))
    if body_top < base_y:
        draw.rectangle([cx - body_w // 2, body_top, cx + body_w // 2, base_y],
                       fill=color, outline=(60, 50, 40), width=1)

    # Height line
    draw.line([(cx - 15, top_y), (cx + 15, top_y)], fill=(60, 50, 40), width=1)
    draw.line([(cx - 15, base_y), (cx + 15, base_y)], fill=(60, 50, 40), width=1)
    draw.line([(cx, top_y), (cx, base_y)], fill=(60, 50, 40, 80), width=1)

    # Label
    label_x = cx + 18 if label_side == "right" else cx - 18
    anchor = "la" if label_side == "right" else "ra"
    try:
        draw.text((label_x, top_y + 5), label, fill=TEXT_COLOR, anchor=anchor)
    except TypeError:
        # Fallback for PIL versions without anchor parameter
        draw.text((label_x, top_y + 5), label, fill=TEXT_COLOR)

    # Height annotation
    h_text = f"{head_units:.1f} heads"
    mid_y = (top_y + base_y) // 2
    try:
        draw.text((label_x, mid_y), h_text, fill=LABEL_COLOR, anchor=anchor)
    except TypeError:
        draw.text((label_x, mid_y), h_text, fill=LABEL_COLOR)

    return total_h


def draw_landmark_line(draw, y, x1, x2, label, side="left"):
    """Draw a horizontal landmark reference line with label."""
    draw.line([(x1, y), (x2, y)], fill=GRID_COLOR, width=1)
    # Dashes
    dash_len = 6
    gap_len = 4
    x = x1
    while x < x2:
        draw.line([(x, y), (min(x + dash_len, x2), y)], fill=GRID_COLOR, width=1)
        x += dash_len + gap_len

    label_x = x1 - 5 if side == "left" else x2 + 5
    anchor = "ra" if side == "left" else "la"
    try:
        draw.text((label_x, y - 6), label, fill=LABEL_COLOR, anchor=anchor)
    except TypeError:
        draw.text((label_x, y - 6), label, fill=LABEL_COLOR)


def generate_scale_sheet():
    """Generate the full scale reference sheet."""
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Title
    try:
        draw.text((W // 2, 15), "CHARACTER-ENVIRONMENT SCALE REFERENCE",
                  fill=TEXT_COLOR, anchor="ma")
        draw.text((W // 2, 32), "Luma & the Glitchkin — C50",
                  fill=LABEL_COLOR, anchor="ma")
    except TypeError:
        draw.text((W // 2 - 180, 15), "CHARACTER-ENVIRONMENT SCALE REFERENCE",
                  fill=TEXT_COLOR)
        draw.text((W // 2 - 100, 32), "Luma & the Glitchkin — C50",
                  fill=LABEL_COLOR)

    # Divide canvas into 4 environment panels
    panel_w = W // 4
    margin_top = 55
    margin_bot = 20

    env_names = ["Kitchen", "Hallway", "Classroom", "Study"]

    for i, env_name in enumerate(env_names):
        env = ENVIRONMENTS[env_name]
        px = i * panel_w
        panel_cx = px + panel_w // 2

        # Panel border
        draw.rectangle([px + 2, margin_top, px + panel_w - 2, H - margin_bot],
                       outline=GRID_COLOR, width=1)

        # Environment label
        try:
            draw.text((panel_cx, margin_top + 8), env_name,
                      fill=TEXT_COLOR, anchor="ma")
        except TypeError:
            draw.text((panel_cx - 25, margin_top + 8), env_name, fill=TEXT_COLOR)

        # Draw landmark lines
        for lm_name, lm_y in env["landmarks"]:
            draw_landmark_line(draw, lm_y, px + 5, px + panel_w - 5,
                               lm_name, side="left")

        floor_y = env["floor_y"]

        # Calculate head_px so characters fit in the panel
        # Use Cosmo (tallest) as reference — he should be ~65% of panel height
        panel_height = H - margin_bot - margin_top - 30
        cosmo_target_h = int(panel_height * 0.55)
        head_px = int(cosmo_target_h / COSMO_HEADS)

        # Place characters left to right: Miri, Luma, Cosmo, Byte
        char_positions = [
            (panel_cx - panel_w * 0.28, MIRI_HEADS, MIRI_COLOR, "Miri", "left"),
            (panel_cx - panel_w * 0.05, LUMA_HEADS, LUMA_COLOR, "Luma", "left"),
            (panel_cx + panel_w * 0.18, COSMO_HEADS, COSMO_COLOR, "Cosmo", "right"),
            (panel_cx + panel_w * 0.35, BYTE_HEADS, BYTE_COLOR, "Byte", "right"),
        ]

        for cx_offset, heads, color, name, side in char_positions:
            cx = int(cx_offset)
            draw_character_silhouette(draw, cx, floor_y, heads, head_px,
                                     color, name, label_side=side)

    # Add scale bar at bottom
    draw.line([(20, H - 12), (W - 20, H - 12)], fill=GRID_COLOR, width=1)
    scale_text = f"1 Luma-head = {head_px}px at this scale"
    try:
        draw.text((W // 2, H - 10), scale_text, fill=LABEL_COLOR, anchor="ma")
    except TypeError:
        draw.text((W // 2 - 80, H - 14), scale_text, fill=LABEL_COLOR)

    return img


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    img = generate_scale_sheet()

    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from LTG_TOOL_project_paths import output_dir, ensure_dir
        out_path = output_dir("production", "LTG_SCALE_reference_sheet.png")
        ensure_dir(out_path.parent)
    except ImportError:
        out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "production", "LTG_SCALE_reference_sheet.png")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

    img.save(str(out_path))
    print(f"Scale reference sheet saved: {out_path}")
    print(f"Size: {img.size[0]}x{img.size[1]}")
