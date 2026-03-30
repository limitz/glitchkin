# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_luma_face_curves.py
Luma Face Bezier Curve System — "Luma & the Glitchkin"
Author: Kai Nakamura / Cycle 40-41
Spec: output/production/luma_face_curve_spec.md v002 (Alex Chen, C41)
Supplement: output/production/luma_face_curve_spec_supplement_c40.md (Maya Santos, C40)

Replaces ad-hoc pixel-stroke face drawing with a mathematically-defined
bezier curve system. All expressions derive from named control-point transforms
on a neutral baseline.

Module API
----------
    from LTG_TOOL_luma_face_curves import draw_luma_face

    draw_luma_face(draw, fc=(300, 280), expression="RECKLESS")
    draw_luma_face(draw, fc=(300, 280), expression="THE NOTICING", overrides={"blush_alpha": 50})

CLI
---
    python LTG_TOOL_luma_face_curves.py
    → renders 1800×2000px reference sheet (3×3 grid, 9 expressions, 600×600px each) to
      output/characters/luma_face_curves_reference.png

Draw Order (spec §Draw Order)
-----------------------------
1. FACE_OVAL (fill + outline)
2. BLUSH_LEFT / BLUSH_RIGHT (fill, under-eye)
3. LEFT_EYE_OUTLINE + RIGHT_EYE_OUTLINE (fill white + outline)
4. LEFT_IRIS + RIGHT_IRIS (fill + outline)
5. LEFT_EYE pupils + highlights
6. RIGHT_EYE pupils + highlights
7. NOSE_BRIDGE
8. MOUTH
9. LEFT_BROW + RIGHT_BROW (drawn last — over eye overlap at outer corners)

Control-Point Transform Rules (spec §Control Point Transform Rules)
-------------------------------------------------------------------
1. Lid drop is top-only: le_lid_drop/re_lid_drop offsets P1 (top) downward. P3 fixed.
2. Brow corrections apply to P1 only (apex control point).
3. Iris always stays within eye outline bounding box.
4. Mouth is open cubic bezier stroke at 600px; simplify to line < 200px.
5. Blush drawn last. Alpha modulates by expression.
6. Smooth interpolation: linearly interpolate delta values across frames.

Changelog
---------
v1.1.0 (C41): CRITICAL eye-width correction per spec v002.
    LE_P0 = FC+(-94,-22), LE_P2 = FC+(+6,-22) (was -72/-16 — 56px → 100px canonical).
    RE_P0 = FC+(-6,-22), RE_P2 = FC+(94,-22) (was +16/+72).
    Reference sheet updated: 3×3 grid with all 9 expressions (6 canonical + 3 supplement).
    Output path: output/characters/luma_face_curves_reference.png.
v1.0.0 (C40): Initial implementation per luma_face_curve_spec.md v001.
    6 canonical expressions: RECKLESS, THE_NOTICING, THE_NOTICING_DOUBT,
    WORRIED, ALARMED, FRUSTRATED.
    3 supplement expressions: CONFIDENT, SOFT_SURPRISE, DETERMINED
    (Maya Santos luma_face_curve_spec_supplement_c40.md).
"""

__version__ = "1.1.0"

import os
import math
from copy import deepcopy
from PIL import Image, ImageDraw

# ── Palette (spec-compliant) ────────────────────────────────────────────────

SKIN_BASE       = (255, 225, 200)   # Luma warm skin — RW palette
OUTLINE_BLACK   = (20,  15,  10)    # Near-black line color (not pure black)
EYE_WHITE       = (250, 248, 242)   # Eye sclera
EYE_IRIS_COLOR  = (80,  60, 140)    # Iris — warm violet
EYE_PUPIL_BLACK = (10,  10,  20)    # Pupil
WHITE           = (255, 255, 255)
BLUSH_PINK      = (255, 175, 175)   # BLUSH fill color


# ── Bezier Utilities ─────────────────────────────────────────────────────────

def _quadratic_bezier_points(p0, p1, p2, n=64):
    """
    Sample n points along a quadratic bezier curve defined by three control points.
    Returns a list of (x, y) integer tuples.

    Parameters
    ----------
    p0 : tuple (x, y) — start point
    p1 : tuple (x, y) — control point (apex)
    p2 : tuple (x, y) — end point
    n  : int — number of sample points along curve (default 64)

    Returns
    -------
    list of (int, int) tuples
    """
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        x = u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0]
        y = u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]
        pts.append((int(round(x)), int(round(y))))
    return pts


def _cubic_bezier_points(p0, p1, p2, p3, n=64):
    """
    Sample n points along a cubic bezier curve defined by four control points.
    Returns a list of (x, y) integer tuples.

    Parameters
    ----------
    p0 : tuple (x, y) — start point
    p1 : tuple (x, y) — first control point
    p2 : tuple (x, y) — second control point
    p3 : tuple (x, y) — end point
    n  : int — number of sample points along curve (default 64)

    Returns
    -------
    list of (int, int) tuples
    """
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        x = (u**3 * p0[0]
             + 3 * u**2 * t * p1[0]
             + 3 * u * t**2 * p2[0]
             + t**3 * p3[0])
        y = (u**3 * p0[1]
             + 3 * u**2 * t * p1[1]
             + 3 * u * t**2 * p2[1]
             + t**3 * p3[1])
        pts.append((int(round(x)), int(round(y))))
    return pts


# ── Neutral Control Points (all offsets from FC) ────────────────────────────

def _build_neutral(fc):
    """
    Build the NEUTRAL_CONTROL_POINTS dict with all values as absolute pixel
    coordinates offset from fc (face center).

    Parameters
    ----------
    fc : tuple (x, y) — face center in canvas coordinates

    Returns
    -------
    dict — named control points
    """
    fx, fy = fc
    return {
        # Face oval
        "oval_rx": 115,
        "oval_ry": 130,
        "oval_tilt": 0,
        # Left brow (character's left = viewer's right)
        "LB_P0": (fx + (-75), fy + (-68)),
        "LB_P1": (fx + (-38), fy + (-88)),
        "LB_P2": (fx + (  0), fy + (-74)),
        # Right brow (character's right = viewer's left)
        "RB_P0": (fx + ( 75), fy + (-68)),
        "RB_P1": (fx + ( 38), fy + (-88)),
        "RB_P2": (fx + (  0), fy + (-74)),
        # Left eye (character's left = viewer's right)
        # v002: LE_P0=FC+(-94,-22), LE_P2=FC+(+6,-22) — 100px canonical eye width
        "LE_P0": (fx + (-94), fy + (-22)),
        "LE_P1": (fx + (-44), fy + (-44)),
        "LE_P2": (fx + (  6), fy + (-22)),
        "LE_P3": (fx + (-44), fy + ( -8)),
        "le_lid_drop": 0,
        # Right eye (character's right = viewer's left)
        # v002: RE_P0=FC+(-6,-22), RE_P2=FC+(94,-22) — 100px canonical eye width
        "RE_P0": (fx + ( -6), fy + (-22)),
        "RE_P1": (fx + ( 44), fy + (-44)),
        "RE_P2": (fx + ( 94), fy + (-22)),
        "RE_P3": (fx + ( 44), fy + ( -8)),
        "re_lid_drop": 6,   # canonical Luma right-eye: sleepy-curious lid drop
        # Left iris
        "LI_CENTER": (fx + (-44), fy + (-26)),
        "LI_R": 12,
        "LP_R": 5,
        # Right iris
        "RI_CENTER": (fx + ( 44), fy + (-26)),
        "RI_R": 12,
        "RP_R": 5,
        # Nose bridge
        "NB_TOP": (fx + (0), fy + (-10)),
        "NB_BOT": (fx + (0), fy + ( 10)),
        # Mouth
        "M_P0": (fx + (-38), fy + ( 42)),
        "M_P1": (fx + (-18), fy + ( 56)),
        "M_P2": (fx + ( 18), fy + ( 56)),
        "M_P3": (fx + ( 38), fy + ( 42)),
        # Blush
        "BLUSH_L_CENTER": (fx + (-65), fy + ( 20)),
        "BLUSH_R_CENTER": (fx + ( 65), fy + ( 20)),
        "blush_rx": 18,
        "blush_ry": 9,
        "blush_alpha": 0,
    }


# ── Expression Delta Dicts ──────────────────────────────────────────────────

EXPRESSION_DELTAS = {
    "RECKLESS": {
        "le_lid_drop": -4,
        "re_lid_drop":  2,
        "LB_P1_dy":    -6,
        "RB_P1_dy":    -4,
        "M_P1_dy":     +8,
        "M_P2_dy":     +8,
        "blush_alpha": 120,
    },
    "THE_NOTICING": {
        "le_lid_drop": +8,
        "re_lid_drop": +12,
        "LB_P1_dy":   +10,
        "RB_P1_dy":   +10,
        "LI_CENTER_dy": +4,
        "RI_CENTER_dy": +4,
        "M_P1_dy":     -4,
        "M_P2_dy":     -4,
        "blush_alpha":  0,
    },
    "THE_NOTICING_DOUBT": {
        # Inherits THE_NOTICING, then overrides:
        "le_lid_drop": +8,
        "re_lid_drop": +16,
        "LB_P1_dy":   +10,
        "RB_P1_dy":   +14,
        "LI_CENTER_dy": +4,
        "RI_CENTER_dy": +4,
        "M_P0_dy":     -6,
        "M_P1_dy":     -4,
        "M_P2_dy":     -4,
        "M_P3_dy":     -6,
        "blush_alpha":  0,
    },
    "WORRIED": {
        "RB_P1_dy":   +18,
        "LB_P1_dx":    -4,
        "RB_P1_dx":    +4,
        "le_lid_drop": +4,
        "re_lid_drop": +4,
        "M_P1_dy":    -10,
        "M_P2_dy":    -10,
        "blush_alpha":  0,
    },
    "ALARMED": {
        "le_lid_drop":  -12,
        "re_lid_drop":   -8,
        "LB_P1_dy":    -14,
        "RB_P1_dy":    -14,
        "oval_ry":      +6,
        "M_P1_dy":      +2,
        "M_P2_dy":      +2,
        "M_P0_dy":      +6,
        "M_P3_dy":      +6,
    },
    "FRUSTRATED": {
        "LB_P1_dy":   +8,
        "RB_P1_dy":   +8,
        "LI_CENTER_dy": +2,
        "RI_CENTER_dy": +2,
        "M_P1_dy":    -14,
        "M_P2_dy":    -14,
        "M_P0_dy":     -4,
        "M_P3_dy":     -4,
        "blush_alpha":  0,
    },
    # C40 supplement expressions (Maya Santos — luma_face_curve_spec_supplement_c40.md)
    "CONFIDENT": {
        "le_lid_drop":   -2,
        "re_lid_drop":   +4,
        "LB_P1_dy":      -8,
        "RB_P1_dy":      -6,
        "LI_CENTER_dy":  -2,
        "RI_CENTER_dy":  -2,
        "M_P1_dy":      +10,
        "M_P2_dy":      +10,
        "M_P0_dy":       +2,
        "M_P3_dy":       +2,
        "blush_alpha":   40,
    },
    "SOFT_SURPRISE": {
        "le_lid_drop":   -6,
        "re_lid_drop":   +2,
        "LB_P1_dy":      -8,
        "RB_P1_dy":      -8,
        "LI_CENTER_dy":   0,
        "RI_CENTER_dy":   0,
        "M_P1_dy":       -2,
        "M_P2_dy":       -2,
        "M_P0_dy":       +4,
        "M_P3_dy":       +4,
        "blush_alpha":    0,
    },
    "DETERMINED": {
        "LB_P1_dy":     +10,
        "RB_P1_dy":     +10,
        "LB_P1_dx":      +4,
        "RB_P1_dx":      -4,
        "le_lid_drop":   +6,
        "re_lid_drop":   +8,
        "LI_CENTER_dy":   0,
        "RI_CENTER_dy":   0,
        "LI_CENTER_dx":   0,
        "RI_CENTER_dx":   0,
        "M_P1_dy":       -8,
        "M_P2_dy":       -8,
        "M_P0_dy":       -2,
        "M_P3_dy":       -2,
        "blush_alpha":    0,
    },
}

# Canonical 6 expressions (original spec order)
CANONICAL_EXPRESSIONS = [
    "RECKLESS",
    "THE_NOTICING",
    "THE_NOTICING_DOUBT",
    "WORRIED",
    "ALARMED",
    "FRUSTRATED",
]

# C40 supplement expressions (Maya Santos)
SUPPLEMENT_EXPRESSIONS = [
    "CONFIDENT",
    "SOFT_SURPRISE",
    "DETERMINED",
]

# All 9 expressions for the 3×3 reference sheet (C41 spec requirement)
ALL_EXPRESSIONS = CANONICAL_EXPRESSIONS + SUPPLEMENT_EXPRESSIONS


def apply_deltas(neutral, delta_dict):
    """
    Merge a delta dict onto a copy of the neutral control points.

    Supported delta keys:
      - Any top-level key in neutral (replaces value directly)
      - "<POINT>_dy" — offset the y-component of a (x,y) tuple key by dy
      - "<POINT>_dx" — offset the x-component of a (x,y) tuple key by dx
      - "oval_ry" — adds to the oval_ry value (face elongation)
      - "le_lid_drop" / "re_lid_drop" — sets the lid drop scalar
      - "LB_P1_dy" / "RB_P1_dy" — offsets P1's y coordinate for brows
      - "LB_P1_dx" / "RB_P1_dx" — offsets P1's x coordinate for brows
      - "LI_CENTER_dy" / "RI_CENTER_dy" — iris center y offsets
      - "LI_CENTER_dx" / "RI_CENTER_dx" — iris center x offsets
      - "M_P0_dy" .. "M_P3_dy" — mouth control point y offsets
      - "blush_alpha" — sets blush alpha scalar (0-255)

    Parameters
    ----------
    neutral    : dict — neutral control points (from _build_neutral)
    delta_dict : dict — expression delta dict

    Returns
    -------
    dict — merged control points (deep copy; original unmodified)
    """
    cp = deepcopy(neutral)
    for key, val in delta_dict.items():
        if key == "blush_alpha":
            # blush_alpha is a SET operation (not accumulate) — spec writes absolute values
            cp["blush_alpha"] = val
        elif key in cp:
            # Top-level scalar keys: accumulate delta onto neutral base value
            # (le_lid_drop, re_lid_drop, oval_rx, oval_ry, LI_R, RI_R, etc.)
            if isinstance(cp[key], (int, float)):
                if isinstance(val, (int, float)):
                    cp[key] += val
            elif isinstance(cp[key], tuple):
                # Direct tuple replacement (rare — prefer _dx/_dy suffixes)
                cp[key] = val
        elif key.endswith("_dy"):
            # e.g. LB_P1_dy → offset y-component of LB_P1 tuple
            point_key = key[:-3]
            if point_key in cp and isinstance(cp[point_key], tuple):
                cp[point_key] = (cp[point_key][0], cp[point_key][1] + val)
        elif key.endswith("_dx"):
            # e.g. LB_P1_dx → offset x-component of LB_P1 tuple
            point_key = key[:-3]
            if point_key in cp and isinstance(cp[point_key], tuple):
                cp[point_key] = (cp[point_key][0] + val, cp[point_key][1])
        # Unknown keys are silently ignored (forward-compat with future spec additions)
    return cp


def _normalize_expression_name(expression):
    """
    Normalize expression string to canonical dict key form.
    Accepts: "THE NOTICING", "THE_NOTICING", "the noticing", "the_noticing" etc.
    Returns uppercase underscore form: "THE_NOTICING".
    """
    return expression.upper().replace(" ", "_")


def _get_eye_bbox(p0, p2, p1_top, p3_bot):
    """
    Return the bounding box (min_x, min_y, max_x, max_y) for an eye outline
    defined by four bezier points: P0 (left), P1 (top), P2 (right), P3 (bottom).
    Used for iris clamping.
    """
    all_x = [p0[0], p1_top[0], p2[0], p3_bot[0]]
    all_y = [p0[1], p1_top[1], p2[1], p3_bot[1]]
    return min(all_x), min(all_y), max(all_x), max(all_y)


def _clamp_iris(center, radius, bbox):
    """
    Clamp iris center so circle (center, radius) fits within bbox.
    Returns clamped (x, y).
    """
    min_x, min_y, max_x, max_y = bbox
    cx = max(min_x + radius, min(max_x - radius, center[0]))
    cy = max(min_y + radius, min(max_y - radius, center[1]))
    return (int(cx), int(cy))


# ── Draw Functions ──────────────────────────────────────────────────────────

def _draw_face_oval(draw, cp):
    """Draw face oval: fill with SKIN_BASE, outline OUTLINE_BLACK."""
    fx, fy = cp.get("_fc", (300, 280))
    rx = cp["oval_rx"]
    ry = cp["oval_ry"]
    draw.ellipse(
        [fx - rx, fy - ry, fx + rx, fy + ry],
        fill=SKIN_BASE,
        outline=OUTLINE_BLACK,
        width=3,
    )


def _draw_blush(draw, cp):
    """Draw blush ellipses under eyes with alpha-modulated fill."""
    alpha = cp.get("blush_alpha", 0)
    if alpha <= 0:
        return
    blush_col = (*BLUSH_PINK, alpha)
    lc = cp["BLUSH_L_CENTER"]
    rc = cp["BLUSH_R_CENTER"]
    rx = cp["blush_rx"]
    ry = cp["blush_ry"]
    # Use RGBA overlay to support alpha blush
    # Since draw may be on RGB canvas, approximate by blending at lower opacity
    # Create a temporary overlay for alpha blending
    canvas_w, canvas_h = draw._image.size
    overlay = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([lc[0] - rx, lc[1] - ry, lc[0] + rx, lc[1] + ry], fill=blush_col)
    od.ellipse([rc[0] - rx, rc[1] - ry, rc[0] + rx, rc[1] + ry], fill=blush_col)
    # Composite onto main image
    base = draw._image
    if base.mode != "RGBA":
        base_rgba = base.convert("RGBA")
        base_rgba.alpha_composite(overlay)
        base.paste(base_rgba.convert(base.mode))
    else:
        base.alpha_composite(overlay)


def _apply_lid_drop(p1, lid_drop):
    """
    Apply lid drop to the top control point of an eye bezier (P1).
    Positive lid_drop = lid descends from top (drowsy/THE NOTICING).
    Negative lid_drop = lid lifts (wide alarm).
    P3 (bottom) is NEVER changed (spec rule 1).
    """
    return (p1[0], p1[1] + lid_drop)


def _draw_eye(draw, p0, p1, p2, p3, lid_drop=0, fill=EYE_WHITE, outline_color=OUTLINE_BLACK,
              outline_w=3, n=64):
    """
    Draw a closed cubic bezier eye outline (top half + bottom half).
    The top arc uses P1 modified by lid_drop. The bottom arc uses P3 (fixed).
    Fill inside with EYE_WHITE.

    Construction: closed eye = top cubic (P0→P1→P2 as cubic control) + bottom cubic (P2→P3→P0).
    For a natural teardrop eye we use the four corner points as a closed bezier polygon.
    We approximate with two quadratic curves: P0→P1→P2 (top) and P2→P3→P0 (bottom).
    """
    # Apply lid drop to top control point
    p1_eff = _apply_lid_drop(p1, lid_drop)
    # Top half: P0 → P1_eff → P2 (quadratic)
    top_pts = _quadratic_bezier_points(p0, p1_eff, p2, n)
    # Bottom half: P2 → P3 → P0 (quadratic)
    bot_pts = _quadratic_bezier_points(p2, p3, p0, n)
    # Combine into closed polygon for fill
    all_pts = top_pts + bot_pts[1:]  # avoid duplicating P2
    if len(all_pts) >= 3:
        draw.polygon(all_pts, fill=fill)
        draw.line(top_pts, fill=outline_color, width=outline_w)
        draw.line(bot_pts, fill=outline_color, width=outline_w)


def _draw_iris(draw, center, r, pupil_r, cp_key=""):
    """Draw iris: fill EYE_IRIS_COLOR, outline 2px, pupil, highlight."""
    x, y = center
    draw.ellipse([x - r, y - r, x + r, y + r],
                 fill=EYE_IRIS_COLOR, outline=OUTLINE_BLACK, width=2)
    # Pupil
    draw.ellipse([x - pupil_r, y - pupil_r, x + pupil_r, y + pupil_r],
                 fill=EYE_PUPIL_BLACK)
    # Highlight (upper-left of iris)
    hl_x = x - max(2, r // 3)
    hl_y = y - max(2, r // 3)
    hl_r = max(1, r // 4)
    draw.ellipse([hl_x - hl_r, hl_y - hl_r, hl_x + hl_r, hl_y + hl_r], fill=WHITE)


def _draw_nose(draw, nb_top, nb_bot, canvas_size):
    """Draw minimal nose bridge line. Skipped at small canvas sizes (< 200px)."""
    if canvas_size < 200:
        return
    # Use OUTLINE_BLACK at ~60% alpha — approximate with lighter color
    nose_col = (int(OUTLINE_BLACK[0] * 0.6 + SKIN_BASE[0] * 0.4),
                int(OUTLINE_BLACK[1] * 0.6 + SKIN_BASE[1] * 0.4),
                int(OUTLINE_BLACK[2] * 0.6 + SKIN_BASE[2] * 0.4))
    draw.line([nb_top, nb_bot], fill=nose_col, width=2)


def _draw_mouth(draw, m_p0, m_p1, m_p2, m_p3, canvas_size=600, n=64):
    """
    Draw mouth as cubic bezier stroke (open, not filled).
    At canvas_size < 200px: simplify to a line between P0 and P3.
    Spec rule 4: mouth is open cubic bezier stroke at 600px.
    """
    if canvas_size < 200:
        draw.line([m_p0, m_p3], fill=OUTLINE_BLACK, width=3)
        return
    pts = _cubic_bezier_points(m_p0, m_p1, m_p2, m_p3, n)
    if len(pts) >= 2:
        draw.line(pts, fill=OUTLINE_BLACK, width=5)


def _draw_brow(draw, p0, p1, p2, n=64):
    """Draw brow as quadratic bezier stroke."""
    pts = _quadratic_bezier_points(p0, p1, p2, n)
    if len(pts) >= 2:
        draw.line(pts, fill=OUTLINE_BLACK, width=4)


# ── Public Module API ────────────────────────────────────────────────────────

def draw_luma_face(draw, fc=(300, 280), expression="RECKLESS", overrides=None):
    """
    Draw Luma's complete face in the specified expression at face center fc.

    This function draws directly onto an existing ImageDraw context.
    Call after drawing the hair cloud, body, and other layers if integrating
    into a full character render.

    Parameters
    ----------
    draw       : PIL.ImageDraw.Draw — draw context on which to render the face
    fc         : tuple (x, y) — face center position in canvas coordinates
    expression : str — expression name, case-insensitive. Accepts spaces or underscores.
                 Valid: RECKLESS, THE NOTICING, THE_NOTICING, THE NOTICING DOUBT,
                        THE_NOTICING_DOUBT, WORRIED, ALARMED, FRUSTRATED,
                        CONFIDENT, SOFT_SURPRISE, DETERMINED
    overrides  : dict or None — additional delta overrides applied AFTER the expression
                 delta (same format as expression delta dicts)

    Draw Order (per spec §Draw Order)
    -----------------------------------
    1. FACE_OVAL
    2. BLUSH
    3. EYE OUTLINES
    4. IRISES
    5-6. PUPILS + HIGHLIGHTS
    7. NOSE BRIDGE
    8. MOUTH
    9. BROWS (drawn last — over eye overlaps)
    """
    expr_key = _normalize_expression_name(expression)

    # Build neutral baseline
    neutral = _build_neutral(fc)
    neutral["_fc"] = fc

    # Get expression deltas
    delta = EXPRESSION_DELTAS.get(expr_key, {})

    # Apply deltas
    cp = apply_deltas(neutral, delta)
    cp["_fc"] = fc

    # Apply optional overrides
    if overrides:
        cp = apply_deltas(cp, overrides)
        cp["_fc"] = fc

    # --- 1. FACE OVAL ---
    _draw_face_oval(draw, cp)

    # --- 2. BLUSH ---
    _draw_blush(draw, cp)

    # --- 3. EYE OUTLINES ---
    le_lid = cp.get("le_lid_drop", 0)
    re_lid = cp.get("re_lid_drop", 6)

    _draw_eye(draw,
              cp["LE_P0"], cp["LE_P1"], cp["LE_P2"], cp["LE_P3"],
              lid_drop=le_lid)
    _draw_eye(draw,
              cp["RE_P0"], cp["RE_P1"], cp["RE_P2"], cp["RE_P3"],
              lid_drop=re_lid)

    # --- 4-6. IRISES, PUPILS, HIGHLIGHTS ---
    # Clamp iris centers to eye bounding boxes (spec rule 3)
    le_lid_eff = _apply_lid_drop(cp["LE_P1"], le_lid)
    le_bbox = _get_eye_bbox(cp["LE_P0"], cp["LE_P2"], le_lid_eff, cp["LE_P3"])
    li_center = _clamp_iris(cp["LI_CENTER"], cp["LI_R"], le_bbox)

    re_lid_eff = _apply_lid_drop(cp["RE_P1"], re_lid)
    re_bbox = _get_eye_bbox(cp["RE_P0"], cp["RE_P2"], re_lid_eff, cp["RE_P3"])
    ri_center = _clamp_iris(cp["RI_CENTER"], cp["RI_R"], re_bbox)

    _draw_iris(draw, li_center, cp["LI_R"], cp["LP_R"], "left")
    _draw_iris(draw, ri_center, cp["RI_R"], cp["RP_R"], "right")

    # --- 7. NOSE BRIDGE ---
    # Estimate canvas size from oval radius
    canvas_size_approx = cp["oval_rx"] * 2 + 40
    _draw_nose(draw, cp["NB_TOP"], cp["NB_BOT"], canvas_size_approx)

    # --- 8. MOUTH ---
    _draw_mouth(draw, cp["M_P0"], cp["M_P1"], cp["M_P2"], cp["M_P3"],
                canvas_size=canvas_size_approx)

    # --- 9. BROWS (last — over eye overlaps) ---
    _draw_brow(draw, cp["LB_P0"], cp["LB_P1"], cp["LB_P2"])
    _draw_brow(draw, cp["RB_P0"], cp["RB_P1"], cp["RB_P2"])


# ── CLI: Reference Sheet ─────────────────────────────────────────────────────

def _build_reference_sheet(output_path):
    """
    Generate a reference sheet showing all 9 expressions (6 canonical + 3 supplement)
    in a 3-column × 3-row grid.

    Per C41 spec requirement:
    - Each cell: 600×600px face canvas
    - Header strip: 44px per cell
    - Grid: 3 columns × 3 rows = 9 cells
    - Sheet size: 1800×(3×644) = 1800×1932px, thumbnailed to ≤1280px longest edge
    - Output: output/characters/luma_face_curves_reference.png
    """
    COLS = 3
    ROWS = 3
    CELL_W = 600
    CELL_H = 600
    HEADER_H = 44
    SHEET_W = COLS * CELL_W
    SHEET_H = ROWS * (CELL_H + HEADER_H)

    BG_COLOR = (240, 235, 228)
    HEADER_BG = (50, 40, 60)
    HEADER_SUPPLEMENT_BG = (40, 55, 70)  # slightly different tint for supplement expressions
    HEADER_TEXT_COL = (230, 215, 200)
    DIVIDER_COL = (180, 170, 160)

    sheet = Image.new("RGB", (SHEET_W, SHEET_H), BG_COLOR)
    sheet_draw = ImageDraw.Draw(sheet)

    # Font — fall back to default if no TTF available
    try:
        from PIL import ImageFont
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except Exception:
        try:
            from PIL import ImageFont
            font = ImageFont.load_default()
        except Exception:
            font = None

    for idx, expr_name in enumerate(ALL_EXPRESSIONS):
        col = idx % COLS
        row = idx // COLS

        cell_x = col * CELL_W
        cell_y = row * (CELL_H + HEADER_H)

        # Header strip — canonical vs supplement color distinction
        is_supplement = expr_name in SUPPLEMENT_EXPRESSIONS
        hdr_bg = HEADER_SUPPLEMENT_BG if is_supplement else HEADER_BG
        sheet_draw.rectangle(
            [cell_x, cell_y, cell_x + CELL_W - 1, cell_y + HEADER_H - 1],
            fill=hdr_bg,
        )
        display_name = expr_name.replace("_", " ")
        label = f"{display_name}  [supplement]" if is_supplement else display_name
        sheet_draw.text(
            (cell_x + 10, cell_y + 12),
            label,
            fill=HEADER_TEXT_COL,
            font=font,
        )

        # Cell background
        sheet_draw.rectangle(
            [cell_x, cell_y + HEADER_H, cell_x + CELL_W - 1, cell_y + HEADER_H + CELL_H - 1],
            fill=BG_COLOR,
        )

        # Grid dividers
        sheet_draw.rectangle(
            [cell_x, cell_y, cell_x + CELL_W - 1, cell_y + HEADER_H + CELL_H - 1],
            outline=DIVIDER_COL,
            width=1,
        )

        # Face center in cell — face at center of 600×600 cell area
        fc_x = cell_x + CELL_W // 2
        fc_y = cell_y + HEADER_H + CELL_H // 2

        # Draw face using module API
        draw_luma_face(sheet_draw, fc=(fc_x, fc_y), expression=expr_name)

    # Apply image size rule: ≤ 1280px in both dimensions
    sheet.thumbnail((1280, 1280), Image.LANCZOS)

    # Save — ensure output dir exists
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    sheet.save(output_path, "PNG")
    size_bytes = os.path.getsize(output_path)
    print(f"Saved: {output_path}")
    print(f"File size: {size_bytes:,} bytes ({size_bytes // 1024} KB)")
    print(f"Image size: {sheet.size[0]}×{sheet.size[1]}px")


if __name__ == "__main__":
    import os as _os
    _SCRIPT_DIR = _os.path.dirname(_os.path.abspath(__file__))
    # C41: output path is output/characters/luma_face_curves_reference.png
    # Script is in output/tools/ so go up one level to output/
    _OUTPUT = _os.path.join(
        _os.path.dirname(_SCRIPT_DIR),
        "characters", "luma_face_curves_reference.png"
    )
    print("LTG_TOOL_luma_face_curves.py — Luma Face Bezier Curve System")
    print(f"Version: {__version__}")
    print(f"Spec: luma_face_curve_spec.md v002 (C41 — 100px canonical eye width)")
    print(f"Generating 3x3 reference sheet (9 expressions: 6 canonical + 3 supplement)...")
    print(f"Output: {_OUTPUT}")
    _build_reference_sheet(_OUTPUT)
    print("\nExpressions rendered (3x3 grid):")
    print("  Row 1 — canonical:")
    for e in CANONICAL_EXPRESSIONS[:3]:
        print(f"    {e}")
    print("  Row 2 — canonical:")
    for e in CANONICAL_EXPRESSIONS[3:]:
        print(f"    {e}")
    print("  Row 3 — supplement (Maya Santos C40):")
    for e in SUPPLEMENT_EXPRESSIONS:
        print(f"    {e}")
    print("\nDone.")
