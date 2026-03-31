#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_byte_turnaround.py
Byte — 4-View Color Turnaround (pycairo)
"Luma & the Glitchkin" — Cycle 52 / Rin Yamamoto

Replaces the legacy black silhouette turnaround with a full-color
pycairo render. Four views: FRONT, 3/4, SIDE, BACK.

Features:
  - BYTE_TEAL (#00D4E8) body fill with BYTE_SH shadow and BYTE_HL highlights
  - Cracked eye with magenta pixel grid (FRONT, 3/4)
  - Hot Magenta scar markings
  - Damage notch on right side
  - Antenna with cyan tip
  - Pixel confetti hover particles
  - Anti-aliased wobble outlines via cairo

Output: output/characters/main/turnarounds/LTG_CHAR_byte_turnaround.png
"""

import sys
import os
import math
import random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from LTG_TOOL_cairo_primitives import (
    create_surface, draw_wobble_path, draw_ellipse,
    set_color, stroke_path, fill_background, to_pil_image,
    LINE_WEIGHT_ANCHOR, LINE_WEIGHT_STRUCTURE, LINE_WEIGHT_DETAIL, _c
)

try:
    from LTG_TOOL_project_paths import output_dir
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)

from PIL import Image
import cairo
import numpy as np


# ── Palette ────────────────────────────────────────────────────────────────────
BYTE_TEAL  = (0, 212, 232)
BYTE_HL    = (0, 240, 255)
BYTE_SH    = (0, 168, 192)
BYTE_DARK  = (0, 120, 140)
HOT_MAG    = (255, 45, 120)
SCAR_MAG   = (255, 45, 107)
LINE       = (10, 10, 20)
EYE_W      = (240, 240, 245)
VOID_BLACK = (10, 10, 20)
BG         = (252, 250, 246)

# ── Layout ─────────────────────────────────────────────────────────────────────
CHAR_H   = 180
VIEW_W   = 200
VIEWS    = ["FRONT", "3/4", "SIDE", "BACK"]
PAD      = 20
LABEL_H  = 36
TITLE_H  = 40
STRIP_W  = VIEW_W * 4
STRIP_H  = TITLE_H + CHAR_H + 80 + LABEL_H


def cairo_ellipse_path(ctx, cx, cy, rx, ry):
    ctx.save()
    ctx.translate(cx, cy)
    if rx != 0 and ry != 0:
        ctx.scale(rx, ry)
    ctx.arc(0, 0, 1.0, 0, 2 * math.pi)
    ctx.restore()


def ellipse_points(cx, cy, rx, ry, n=48):
    """Generate n points along an ellipse."""
    pts = []
    for i in range(n):
        t = i / n * 2 * math.pi
        pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    return pts


def draw_byte_front(ctx, cx, base_y):
    """Byte — FRONT view with full color, cracked eye, scar, confetti."""
    body_rx = 40
    body_ry = 30
    bcy = base_y - 80

    # Hover confetti
    rng = random.Random(42)
    for _ in range(6):
        px = cx + rng.randint(-25, 25)
        py = base_y - rng.randint(2, 18)
        sz = rng.choice([4, 5, 6])
        col = rng.choice([BYTE_HL, SCAR_MAG, (0, 200, 180)])
        ctx.rectangle(px, py, sz, sz)
        set_color(ctx, col)
        ctx.fill()

    # Body oval
    pts = ellipse_points(cx, bcy, body_rx, body_ry)
    draw_wobble_path(ctx, pts, amplitude=0.6, frequency=0.1, seed=100)
    set_color(ctx, BYTE_TEAL)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(LINE_WEIGHT_ANCHOR)
    ctx.stroke()

    # Shadow on right half
    ctx.save()
    cairo_ellipse_path(ctx, cx, bcy, body_rx, body_ry)
    ctx.clip()
    ctx.rectangle(cx, bcy - body_ry, body_rx + 2, body_ry * 2 + 2)
    set_color(ctx, BYTE_SH)
    ctx.fill()
    ctx.restore()

    # Highlight arc upper-left
    ctx.save()
    cairo_ellipse_path(ctx, cx, bcy, body_rx, body_ry)
    ctx.clip()
    cairo_ellipse_path(ctx, cx - body_rx // 3, bcy - body_ry // 3,
                       body_rx - 6, body_ry - 6)
    set_color(ctx, BYTE_HL)
    ctx.set_line_width(2)
    ctx.stroke()
    ctx.restore()

    # Re-draw outline
    cairo_ellipse_path(ctx, cx, bcy, body_rx, body_ry)
    set_color(ctx, LINE)
    ctx.set_line_width(LINE_WEIGHT_ANCHOR)
    ctx.stroke()

    # Scar markings
    crack_x = cx - 14
    ctx.move_to(crack_x, bcy - 12)
    ctx.line_to(crack_x + 8, bcy - 4)
    set_color(ctx, SCAR_MAG)
    ctx.set_line_width(2.5)
    ctx.stroke()
    ctx.move_to(crack_x + 8, bcy - 4)
    ctx.line_to(crack_x - 4, bcy + 6)
    ctx.stroke()

    # Damage notch right side
    ctx.move_to(cx + body_rx - 3, bcy - body_ry // 4)
    ctx.line_to(cx + body_rx + 6, bcy - body_ry // 6)
    ctx.line_to(cx + body_rx - 3, bcy + body_ry // 6)
    ctx.close_path()
    set_color(ctx, BG)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(1)
    ctx.stroke()

    # Left eye (cracked/pixel)
    lx = cx - 14
    ey = bcy - 4
    cell = 3
    # Bezel
    ctx.rectangle(lx - 8, ey - 8, 16, 16)
    set_color(ctx, (26, 58, 64))
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(1.5)
    ctx.stroke()
    # Flat line symbol
    for c in range(5):
        ctx.rectangle(lx - 6 + c * 3, ey - 1, 2, 2)
        set_color(ctx, (0, 240, 255))
        ctx.fill()
    # Crack line
    ctx.move_to(lx + 6, ey - 8)
    ctx.line_to(lx - 4, ey + 8)
    set_color(ctx, LINE)
    ctx.set_line_width(1.5)
    ctx.stroke()

    # Right eye (organic)
    rx_eye = cx + 14
    cairo_ellipse_path(ctx, rx_eye, ey, 8, 7)
    set_color(ctx, EYE_W)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(1)
    ctx.stroke()
    cairo_ellipse_path(ctx, rx_eye, ey, 5, 5)
    set_color(ctx, (45, 28, 14))
    ctx.fill()
    cairo_ellipse_path(ctx, rx_eye, ey, 2, 2)
    set_color(ctx, LINE)
    ctx.fill()
    cairo_ellipse_path(ctx, rx_eye + 3, ey - 3, 2, 1.5)
    set_color(ctx, (200, 195, 185))
    ctx.fill()

    # Mouth
    ctx.move_to(cx - 10, bcy + 10)
    ctx.line_to(cx + 10, bcy + 10)
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()
    # Downturn
    ctx.move_to(cx - 10, bcy + 10)
    ctx.line_to(cx - 14, bcy + 13)
    ctx.stroke()
    ctx.move_to(cx + 10, bcy + 10)
    ctx.line_to(cx + 14, bcy + 13)
    ctx.stroke()

    # Antenna
    ant_bx = cx - 8
    ant_by = bcy - body_ry
    ant_tx = ant_bx - 6
    ant_ty = ant_by - 24
    ctx.move_to(ant_bx, ant_by)
    ctx.line_to(ant_tx, ant_ty)
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()
    cairo_ellipse_path(ctx, ant_tx, ant_ty, 4, 4)
    set_color(ctx, BYTE_HL)
    ctx.fill()

    # Arms
    arm_w = 14
    arm_h = 16
    # Left arm
    ctx.rectangle(cx - body_rx - arm_w, bcy - 4, arm_w, arm_h)
    set_color(ctx, BYTE_TEAL)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()
    # Right arm
    ctx.rectangle(cx + body_rx, bcy - 4, arm_w, arm_h)
    set_color(ctx, BYTE_TEAL)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()

    # Legs
    leg_w = 10
    leg_h = 18
    ctx.rectangle(cx - 12 - leg_w // 2, bcy + body_ry, leg_w, leg_h)
    set_color(ctx, BYTE_TEAL)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()
    ctx.rectangle(cx + 12 - leg_w // 2, bcy + body_ry, leg_w, leg_h)
    set_color(ctx, BYTE_TEAL)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()


def draw_byte_three_quarter(ctx, cx, base_y):
    """Byte — 3/4 view. Near side wider, far side compressed."""
    body_rx = 40
    body_ry = 30
    bcy = base_y - 80

    # Confetti
    rng = random.Random(55)
    for _ in range(5):
        px = cx + rng.randint(-20, 20)
        py = base_y - rng.randint(2, 16)
        sz = rng.choice([4, 5])
        col = rng.choice([BYTE_HL, SCAR_MAG])
        ctx.rectangle(px, py, sz, sz)
        set_color(ctx, col)
        ctx.fill()

    # Body — slightly asymmetric (wider on near side)
    rx_near = body_rx
    rx_far = int(body_rx * 0.65)
    # Draw as offset ellipse
    ctx.save()
    ctx.translate(cx - 4, bcy)
    ctx.scale(1.0, 1.0)
    cairo_ellipse_path(ctx, 0, 0, (rx_near + rx_far) // 2, body_ry)
    set_color(ctx, BYTE_TEAL)
    ctx.fill()
    ctx.restore()

    # Shadow on far side
    ctx.save()
    cairo_ellipse_path(ctx, cx - 4, bcy, (rx_near + rx_far) // 2, body_ry)
    ctx.clip()
    ctx.rectangle(cx - 4 - rx_far, bcy - body_ry, rx_far, body_ry * 2)
    set_color(ctx, BYTE_SH)
    ctx.fill()
    ctx.restore()

    # Outline
    cairo_ellipse_path(ctx, cx - 4, bcy, (rx_near + rx_far) // 2, body_ry)
    set_color(ctx, LINE)
    ctx.set_line_width(LINE_WEIGHT_ANCHOR)
    ctx.stroke()

    # Scar
    ctx.move_to(cx - 18, bcy - 10)
    ctx.line_to(cx - 12, bcy)
    set_color(ctx, SCAR_MAG)
    ctx.set_line_width(2)
    ctx.stroke()

    # Eyes (only near eye visible fully)
    ey = bcy - 4
    rx_eye = cx + 8
    cairo_ellipse_path(ctx, rx_eye, ey, 7, 6)
    set_color(ctx, EYE_W)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(1)
    ctx.stroke()
    cairo_ellipse_path(ctx, rx_eye, ey, 4, 4)
    set_color(ctx, (45, 28, 14))
    ctx.fill()
    cairo_ellipse_path(ctx, rx_eye, ey, 1.5, 1.5)
    set_color(ctx, LINE)
    ctx.fill()

    # Far eye (partially obscured — just show bezel edge)
    lx = cx - 16
    ctx.rectangle(lx - 5, ey - 6, 10, 12)
    set_color(ctx, (26, 58, 64))
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(1)
    ctx.stroke()
    ctx.move_to(lx + 3, ey - 6)
    ctx.line_to(lx - 2, ey + 6)
    set_color(ctx, LINE)
    ctx.set_line_width(1)
    ctx.stroke()

    # Mouth
    ctx.move_to(cx - 6, bcy + 10)
    ctx.line_to(cx + 12, bcy + 9)
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()

    # Antenna
    ant_bx = cx - 6
    ant_by = bcy - body_ry
    ant_tx = ant_bx - 8
    ant_ty = ant_by - 22
    ctx.move_to(ant_bx, ant_by)
    ctx.line_to(ant_tx, ant_ty)
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()
    cairo_ellipse_path(ctx, ant_tx, ant_ty, 4, 4)
    set_color(ctx, BYTE_HL)
    ctx.fill()

    # Near arm
    ctx.rectangle(cx + (rx_near + rx_far) // 2 - 4, bcy - 3, 12, 14)
    set_color(ctx, BYTE_TEAL)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()

    # Legs
    leg_w = 10
    leg_h = 16
    ctx.rectangle(cx - 4 - leg_w // 2, bcy + body_ry, leg_w, leg_h)
    set_color(ctx, BYTE_TEAL)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()
    ctx.rectangle(cx + 10 - leg_w // 2, bcy + body_ry, leg_w, leg_h)
    set_color(ctx, BYTE_TEAL)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()


def draw_byte_side(ctx, cx, base_y):
    """Byte — SIDE view. Foreshortened oval, profile antenna."""
    body_rx = 22  # foreshortened
    body_ry = 30
    bcy = base_y - 80

    # Confetti
    rng = random.Random(77)
    for _ in range(4):
        px = cx + rng.randint(-15, 15)
        py = base_y - rng.randint(2, 14)
        sz = rng.choice([4, 5])
        ctx.rectangle(px, py, sz, sz)
        set_color(ctx, rng.choice([BYTE_HL, (0, 200, 180)]))
        ctx.fill()

    # Body
    cairo_ellipse_path(ctx, cx, bcy, body_rx, body_ry)
    set_color(ctx, BYTE_TEAL)
    ctx.fill()

    # Shadow on back half
    ctx.save()
    cairo_ellipse_path(ctx, cx, bcy, body_rx, body_ry)
    ctx.clip()
    ctx.rectangle(cx - body_rx, bcy - body_ry, body_rx, body_ry * 2)
    set_color(ctx, BYTE_SH)
    ctx.fill()
    ctx.restore()

    # Outline
    cairo_ellipse_path(ctx, cx, bcy, body_rx, body_ry)
    set_color(ctx, LINE)
    ctx.set_line_width(LINE_WEIGHT_ANCHOR)
    ctx.stroke()

    # Scar (partial — side view shows continuation)
    ctx.move_to(cx - 4, bcy - 8)
    ctx.line_to(cx + 2, bcy + 4)
    set_color(ctx, SCAR_MAG)
    ctx.set_line_width(2)
    ctx.stroke()

    # Eye — profile view, single eye visible (right/organic)
    ey = bcy - 3
    cairo_ellipse_path(ctx, cx + 8, ey, 5, 6)
    set_color(ctx, EYE_W)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(1)
    ctx.stroke()
    cairo_ellipse_path(ctx, cx + 9, ey, 3, 3)
    set_color(ctx, (45, 28, 14))
    ctx.fill()
    cairo_ellipse_path(ctx, cx + 9, ey, 1.5, 1.5)
    set_color(ctx, LINE)
    ctx.fill()

    # Mouth (side = short line)
    ctx.move_to(cx + 10, bcy + 10)
    ctx.line_to(cx + 18, bcy + 9)
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()

    # Antenna (side view — points forward)
    ant_bx = cx
    ant_by = bcy - body_ry
    ant_tx = cx + 16
    ant_ty = ant_by - 18
    ctx.move_to(ant_bx, ant_by)
    ctx.line_to(ant_tx, ant_ty)
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()
    cairo_ellipse_path(ctx, ant_tx, ant_ty, 3, 3)
    set_color(ctx, BYTE_HL)
    ctx.fill()

    # Single leg visible
    leg_w = 10
    leg_h = 16
    ctx.rectangle(cx - leg_w // 2, bcy + body_ry, leg_w, leg_h)
    set_color(ctx, BYTE_TEAL)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()


def draw_byte_back(ctx, cx, base_y):
    """Byte — BACK view. Full oval, no face, back scar marks visible."""
    body_rx = 40
    body_ry = 30
    bcy = base_y - 80

    # Confetti
    rng = random.Random(33)
    for _ in range(5):
        px = cx + rng.randint(-20, 20)
        py = base_y - rng.randint(2, 14)
        sz = rng.choice([4, 5])
        ctx.rectangle(px, py, sz, sz)
        set_color(ctx, rng.choice([BYTE_HL, (0, 200, 180)]))
        ctx.fill()

    # Body
    pts = ellipse_points(cx, bcy, body_rx, body_ry)
    draw_wobble_path(ctx, pts, amplitude=0.6, frequency=0.1, seed=200)
    set_color(ctx, BYTE_SH)  # Back is shadowed
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(LINE_WEIGHT_ANCHOR)
    ctx.stroke()

    # Highlight on left edge (light comes from upper-left)
    ctx.save()
    cairo_ellipse_path(ctx, cx, bcy, body_rx, body_ry)
    ctx.clip()
    ctx.rectangle(cx - body_rx, bcy - body_ry, body_rx // 2, body_ry * 2)
    set_color(ctx, BYTE_TEAL)
    ctx.fill()
    ctx.restore()

    # Re-draw outline
    cairo_ellipse_path(ctx, cx, bcy, body_rx, body_ry)
    set_color(ctx, LINE)
    ctx.set_line_width(LINE_WEIGHT_ANCHOR)
    ctx.stroke()

    # Back scar marks (continuation of front scar, from behind)
    ctx.move_to(cx + 12, bcy - 14)
    ctx.line_to(cx + 4, bcy + 8)
    set_color(ctx, SCAR_MAG)
    ctx.set_line_width(2)
    ctx.stroke()
    # Secondary scatter marks
    for (sx, sy) in [(cx + 8, bcy - 6), (cx + 14, bcy + 2)]:
        ctx.rectangle(sx, sy, 3, 3)
        set_color(ctx, (196, 35, 90))  # SCAR_MAG 70%
        ctx.fill()

    # Damage notch (visible from back too)
    ctx.move_to(cx + body_rx - 3, bcy - body_ry // 4)
    ctx.line_to(cx + body_rx + 5, bcy - body_ry // 6)
    ctx.line_to(cx + body_rx - 3, bcy + body_ry // 6)
    ctx.close_path()
    set_color(ctx, BG)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(1)
    ctx.stroke()

    # Antenna (from behind)
    ant_bx = cx - 8
    ant_by = bcy - body_ry
    ant_tx = ant_bx - 4
    ant_ty = ant_by - 22
    ctx.move_to(ant_bx, ant_by)
    ctx.line_to(ant_tx, ant_ty)
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()
    cairo_ellipse_path(ctx, ant_tx, ant_ty, 4, 4)
    set_color(ctx, BYTE_HL)
    ctx.fill()

    # Arms (from behind)
    arm_w = 14
    arm_h = 16
    ctx.rectangle(cx - body_rx - arm_w, bcy - 4, arm_w, arm_h)
    set_color(ctx, BYTE_SH)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()
    ctx.rectangle(cx + body_rx, bcy - 4, arm_w, arm_h)
    set_color(ctx, BYTE_SH)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()

    # Legs
    leg_w = 10
    leg_h = 18
    ctx.rectangle(cx - 12 - leg_w // 2, bcy + body_ry, leg_w, leg_h)
    set_color(ctx, BYTE_SH)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()
    ctx.rectangle(cx + 12 - leg_w // 2, bcy + body_ry, leg_w, leg_h)
    set_color(ctx, BYTE_SH)
    ctx.fill_preserve()
    set_color(ctx, LINE)
    ctx.set_line_width(2)
    ctx.stroke()


def build_turnaround():
    """Build the 4-view Byte turnaround strip."""
    surface, ctx, _, _ = create_surface(STRIP_W, STRIP_H)
    fill_background(ctx, STRIP_W, STRIP_H, BG)

    # Title
    ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(14)
    ctx.set_source_rgb(*_c(BYTE_TEAL))
    ctx.move_to(PAD, 26)
    ctx.show_text("BYTE — Color Turnaround  |  v001 pycairo  |  C52  |  Rin Yamamoto")

    # Ground line
    ground_y = TITLE_H + CHAR_H + 50
    ctx.move_to(0, ground_y)
    ctx.line_to(STRIP_W, ground_y)
    set_color(ctx, (200, 190, 180))
    ctx.set_line_width(1)
    ctx.stroke()

    draw_funcs = [draw_byte_front, draw_byte_three_quarter,
                  draw_byte_side, draw_byte_back]

    for i, (view_name, draw_fn) in enumerate(zip(VIEWS, draw_funcs)):
        panel_x = i * VIEW_W
        panel_cx = panel_x + VIEW_W // 2

        # Panel border
        ctx.rectangle(panel_x, TITLE_H, VIEW_W, STRIP_H - TITLE_H - LABEL_H)
        set_color(ctx, (230, 225, 218))
        ctx.set_line_width(0.5)
        ctx.stroke()

        draw_fn(ctx, panel_cx, ground_y)

        # View label
        ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(11)
        ext = ctx.text_extents(view_name)
        lx = panel_cx - ext.width / 2
        ctx.move_to(lx, STRIP_H - 10)
        ctx.set_source_rgb(*_c((50, 40, 35)))
        ctx.show_text(view_name)

    img = to_pil_image(surface)
    img.thumbnail((1280, 1280), Image.LANCZOS)
    return img


def main():
    out_dir = str(output_dir('characters', 'main', 'turnarounds'))
    os.makedirs(out_dir, exist_ok=True)

    img = build_turnaround()
    out_path = os.path.join(out_dir, "LTG_CHAR_byte_turnaround.png")
    img.save(out_path)
    w, h = img.size
    print(f"Saved: {out_path}  ({w}x{h}px)")

    # Also save to main directory (overwrite legacy)
    main_dir = str(output_dir('characters', 'main'))
    main_path = os.path.join(main_dir, "LTG_CHAR_byte_turnaround.png")
    img.save(main_path)
    print(f"Also saved: {main_path}")


if __name__ == "__main__":
    main()
