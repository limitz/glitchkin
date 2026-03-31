#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
test_face_lighting.py — Test harness for add_face_lighting()
Generates: output/tools/test_face_lighting.png  (≤ 640px)

Layout:
  Left panel  — face with light coming from upper-left  (warm highlight, cool-dark shadow)
  Right panel — same face with light from upper-right   (swapped sides)

Run:
    python output/tools/test_face_lighting.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw
from LTG_TOOL_procedural_draw import (
    wobble_polygon, add_face_lighting, add_rim_light, silhouette_test
)

# ---------------------------------------------------------------------------
# Canonical palette (LTG)
# ---------------------------------------------------------------------------
SKIN_BASE    = (210, 185, 155)
OUTLINE      = (30,  20,  15)
SHADOW_WARM  = (100, 60,  40)   # warm-dark shadow (real-world style)
SHADOW_COOL  = (60,  70, 110)   # cool-dark shadow (Glitch-world style)
HIGHLIGHT_W  = (255, 248, 210)  # warm highlight
HIGHLIGHT_C  = (180, 240, 255)  # cool / UV highlight
BG           = (240, 236, 228)

PANEL_SIZE   = 300              # each panel; total canvas = 600×300


def _draw_face_panel(canvas, offset_x, light_dir, shadow_color, highlight_color, seed_base):
    """Draw one face panel into the canvas at offset_x."""
    q = PANEL_SIZE
    margin = 20

    # Background
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([(offset_x, 0), (offset_x + q, q)], fill=BG)

    # Face blob — approximate cartoon head shape
    cx = offset_x + q // 2
    cy = q // 2 - 10
    rx = q // 2 - margin - 15
    ry = q // 2 - margin - 5

    num_pts = 20
    blob_pts = []
    for i in range(num_pts):
        angle = (2 * math.pi * i / num_pts) - math.pi / 2
        r_mod = 1.0 + 0.07 * math.cos(2 * angle) + 0.04 * math.sin(3 * angle)
        bx = cx + rx * r_mod * math.cos(angle)
        by = cy + ry * r_mod * math.sin(angle)
        blob_pts.append((bx, by))

    draw = ImageDraw.Draw(canvas)
    wobble_polygon(draw, blob_pts,
                   color=OUTLINE, width=2,
                   amplitude=2.5, frequency=5, seed=seed_base,
                   fill=SKIN_BASE)

    # Ears (simple circles, slightly behind head)
    ear_y = cy - ry * 0.05
    draw.ellipse([
        cx - rx - 12, int(ear_y - ry * 0.22),
        cx - rx + 4,  int(ear_y + ry * 0.22),
    ], fill=SKIN_BASE, outline=OUTLINE, width=1)
    draw.ellipse([
        cx + rx - 4,  int(ear_y - ry * 0.22),
        cx + rx + 12, int(ear_y + ry * 0.22),
    ], fill=SKIN_BASE, outline=OUTLINE, width=1)

    # Eyes
    eye_y  = cy - ry * 0.18
    eye_lx = cx - rx * 0.30
    eye_rx = cx + rx * 0.30
    eye_r  = int(rx * 0.11)
    draw.ellipse([int(eye_lx - eye_r), int(eye_y - eye_r * 0.8),
                  int(eye_lx + eye_r), int(eye_y + eye_r * 0.8)],
                 fill=(30, 20, 15))
    draw.ellipse([int(eye_rx - eye_r), int(eye_y - eye_r * 0.8),
                  int(eye_rx + eye_r), int(eye_y + eye_r * 0.8)],
                 fill=(30, 20, 15))
    # Eye-shine dots
    draw.ellipse([int(eye_lx + 1), int(eye_y - eye_r * 0.4),
                  int(eye_lx + 4), int(eye_y)], fill=(255, 255, 255))
    draw.ellipse([int(eye_rx + 1), int(eye_y - eye_r * 0.4),
                  int(eye_rx + 4), int(eye_y)], fill=(255, 255, 255))

    # Nose — small curve
    draw.line([
        (cx - 5, cy + int(ry * 0.12)),
        (cx,     cy + int(ry * 0.20)),
        (cx + 5, cy + int(ry * 0.12)),
    ], fill=(160, 120, 90), width=1)

    # Mouth — gentle curve
    mouth_pts = [
        (cx + int(rx * 0.25 * math.cos(a * math.pi / 6)),
         cy + int(ry * 0.42 + ry * 0.06 * math.sin(a * math.pi / 6)))
        for a in range(7)
    ]
    for j in range(len(mouth_pts) - 1):
        draw.line([mouth_pts[j], mouth_pts[j + 1]], fill=(100, 60, 50), width=2)

    # --- Apply volumetric face lighting ---
    add_face_lighting(
        canvas,
        face_center=(cx, cy),
        face_radius=(rx, ry),
        light_dir=light_dir,
        shadow_color=shadow_color,
        highlight_color=highlight_color,
        seed=seed_base + 100,
    )

    # Rim light pass
    region = canvas.crop((offset_x, 0, offset_x + q, q))
    add_rim_light(region, threshold=185, light_color=highlight_color, width=2)
    canvas.paste(region, (offset_x, 0))
    draw = ImageDraw.Draw(canvas)  # refresh after paste

    # Panel label
    label = f"light: ({light_dir[0]:+.0f},{light_dir[1]:+.0f})"
    draw.rectangle([(offset_x, q - 20), (offset_x + q, q)], fill=BG)
    draw.text((offset_x + 6, q - 17), label, fill=(60, 60, 60))

    # Divider line between panels
    if offset_x > 0:
        draw.line([(offset_x, 0), (offset_x, q)], fill=(130, 130, 130), width=1)


def build_test_image(out_path):
    """Build the two-panel face-lighting test image."""
    canvas_w = PANEL_SIZE * 2
    canvas_h = PANEL_SIZE
    canvas = Image.new("RGB", (canvas_w, canvas_h), BG)

    # Panel 1 — upper-left light, warm shadow
    _draw_face_panel(canvas,
                     offset_x=0,
                     light_dir=(-0.7, -0.7),
                     shadow_color=SHADOW_WARM,
                     highlight_color=HIGHLIGHT_W,
                     seed_base=7)

    # Panel 2 — upper-right light, cool shadow (Glitch-world aesthetic)
    _draw_face_panel(canvas,
                     offset_x=PANEL_SIZE,
                     light_dir=(0.7, -0.7),
                     shadow_color=SHADOW_COOL,
                     highlight_color=HIGHLIGHT_C,
                     seed_base=13)

    # Title bar at top
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([(0, 0), (canvas_w, 18)], fill=(30, 20, 15))
    draw.text((8, 2), "add_face_lighting() — brow / nose-cheek / chin shadows", fill=(240, 230, 200))

    # Enforce ≤ 640px
    if canvas.width > 640 or canvas.height > 640:
        canvas.thumbnail((640, 640), Image.LANCZOS)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    canvas.save(out_path, "PNG")
    print(f"Saved: {out_path}  ({canvas.width}x{canvas.height})")


if __name__ == "__main__":
    _here = os.path.dirname(os.path.abspath(__file__))
    _out = os.path.join(_here, "test_face_lighting.png")
    build_test_image(_out)
    print("Done.")
