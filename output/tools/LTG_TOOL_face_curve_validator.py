# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_face_curve_validator.py
Luma Face Curve Spec Validator
"Luma & the Glitchkin" — Cycle 41 / Maya Santos

PURPOSE:
  Renders bezier spec expressions from the luma_face_curve_spec.md control point
  dicts and reports geometry metrics:
    - Eye width (P0→P2 distance, horizontal)
    - Lid-top-drop delta (from neutral P1 y)
    - Mouth y-position (average of corners)
    - Brow apex y (P1 y value relative to FC)

  Flags deviations from neutral control points by more than allowed tolerances.
  Helps catch control-point errors before Kai's bezier renderer implementation.

USAGE:
  python3 LTG_TOOL_face_curve_validator.py
          [--expression EXPR_NAME]
          [--all]
          [--output-sheet PATH]
          [--report PATH]
          [--tolerance-eye 5]
          [--tolerance-brow 5]
          [--tolerance-mouth 5]

  --expression EXPR_NAME   Validate a single expression by name (e.g. RECKLESS)
  --all                    Validate all expressions in the spec (default)
  --output-sheet PATH      Output contact sheet PNG (default: output/production/
                           LTG_TOOL_face_curve_validator_sheet.png)
  --report PATH            Write text report to file
  --tolerance-eye N        Allowed deviation in eye width from canonical 100px
                           before WARN (default: 5px)
  --tolerance-brow N       Allowed deviation in brow apex y from neutral before
                           WARN in extra-credit check (default: 5px)
  --tolerance-mouth N      Allowed mouth y deviation from expected neutral read
                           (default: 5px)

OUTPUT:
  - Contact sheet PNG ≤ 1280x1280px showing all validated expressions
  - Each panel shows the rendered face + metric annotations
  - Text report to stdout (and optionally to file)
  - Exit code: 0=PASS, 1=WARN, 2=FAIL

Author: Maya Santos, Character Designer
Cycle: 41
Date: 2026-03-30
"""

import argparse
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

# ── Hard limit ────────────────────────────────────────────────────────────────
MAX_DIM = 1280

# ── Output dir ────────────────────────────────────────────────────────────────
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "production")
DEFAULT_SHEET = os.path.join(OUT_DIR, "LTG_TOOL_face_curve_validator_sheet.png")

# ── Face coordinate system ────────────────────────────────────────────────────
# Canvas 600×600, origin FC = (300, 280)
CANVAS_W   = 600
CANVAS_H   = 600
FC         = (300, 280)

# ── Neutral baseline control points ──────────────────────────────────────────
# All points expressed as FC + (dx, dy)

def fc(dx, dy):
    return (FC[0] + dx, FC[1] + dy)

NEUTRAL = {
    # Face oval
    "oval_rx": 115,
    "oval_ry": 130,

    # Left brow (character's left = viewer's right)
    "LB_P0": fc(-75, -68),
    "LB_P1": fc(-38, -88),
    "LB_P2": fc(  0, -74),

    # Right brow (character's right = viewer's left)
    "RB_P0": fc( 75, -68),
    "RB_P1": fc( 38, -88),
    "RB_P2": fc(  0, -74),

    # Left eye outline (closed cubic bezier)
    # Eye width = P0 to P2 horizontal distance = canonical 100px
    "LE_P0": fc(-94, -22),   # outer corner
    "LE_P1": fc(-44, -44),   # top center
    "LE_P2": fc(  6, -22),   # inner corner
    "LE_P3": fc(-44,  -8),   # bottom center

    # Right eye outline
    "RE_P0": fc( -6, -22),   # inner corner
    "RE_P1": fc( 44, -44),   # top center
    "RE_P2": fc( 94, -22),   # outer corner
    "RE_P3": fc( 44,  -8),   # bottom center

    # Irises
    "LI_CENTER": fc(-44, -26),
    "LI_R": 12,
    "RI_CENTER": fc( 44, -26),
    "RI_R": 12,

    # Mouth (cubic bezier)
    "M_P0": fc(-38,  42),
    "M_P1": fc(-18,  56),
    "M_P2": fc( 18,  56),
    "M_P3": fc( 38,  42),

    # Blush
    "BLUSH_L_CENTER": fc(-65,  20),
    "BLUSH_R_CENTER": fc( 65,  20),
    "blush_rx": 18,
    "blush_ry":  9,
    "blush_alpha": 80,

    # Lid drop defaults
    "le_lid_drop": 0,
    "re_lid_drop": 6,   # canonical right-eye has +6 lid drop at neutral
}

EYE_WIDTH_CANON = 100   # LE_P0 to LE_P2 horizontal distance


# ── Expression delta table (from spec + supplement) ──────────────────────────

EXPRESSION_DELTAS = {
    "NEUTRAL": {},

    "RECKLESS": {
        "le_lid_drop": -4,
        "re_lid_drop":  2,
        "LB_P1_dy":    -6,
        "RB_P1_dy":    -4,
        "M_P1_dy":    +8,
        "M_P2_dy":    +8,
        "blush_alpha": 120,
    },

    "THE_NOTICING": {
        "le_lid_drop":  +8,
        "re_lid_drop": +12,
        "LB_P1_dy":   +10,
        "RB_P1_dy":   +10,
        "LI_CENTER_dy": +4,
        "RI_CENTER_dy": +4,
        "M_P1_dy":    -4,
        "M_P2_dy":    -4,
        "blush_alpha":  0,
    },

    "THE_NOTICING_DOUBT": {
        # Inherits THE_NOTICING
        "le_lid_drop":  +8,
        "re_lid_drop": +16,
        "LB_P1_dy":   +10,
        "RB_P1_dy":   +14,
        "LI_CENTER_dy": +4,
        "RI_CENTER_dy": +4,
        "M_P1_dy":    -4,
        "M_P2_dy":    -4,
        "M_P0_dy":    -6,
        "M_P3_dy":    -6,
        "blush_alpha":  0,
    },

    "WORRIED": {
        "RB_P1_dy":   +18,
        "LB_P1_dx":    -4,
        "RB_P1_dx":    +4,
        "le_lid_drop": +4,
        "re_lid_drop": +4,
        "M_P1_dy":   -10,
        "M_P2_dy":   -10,
        "blush_alpha":  0,
    },

    "ALARMED": {
        "le_lid_drop": -12,
        "re_lid_drop":  -8,
        "LB_P1_dy":   -14,
        "RB_P1_dy":   -14,
        "oval_ry":     +6,
        "M_P1_dy":    +2,
        "M_P2_dy":    +2,
        "M_P0_dy":    +6,
        "M_P3_dy":    +6,
    },

    "FRUSTRATED": {
        "LB_P1_dy":   +8,
        "RB_P1_dy":   +8,
        "LI_CENTER_dy": +2,
        "RI_CENTER_dy": +2,
        "M_P1_dy":   -14,
        "M_P2_dy":   -14,
        "M_P0_dy":    -4,
        "M_P3_dy":    -4,
        "blush_alpha":  0,
    },

    # C40 supplement
    "CONFIDENT": {
        "le_lid_drop":  -2,
        "re_lid_drop":  +4,
        "LB_P1_dy":    -8,
        "RB_P1_dy":    -6,
        "LI_CENTER_dy": -2,
        "RI_CENTER_dy": -2,
        "M_P1_dy":    +10,
        "M_P2_dy":    +10,
        "M_P0_dy":    +2,
        "M_P3_dy":    +2,
        "blush_alpha":  40,
    },

    "SOFT_SURPRISE": {
        "le_lid_drop":  -6,
        "re_lid_drop":  +2,
        "LB_P1_dy":    -8,
        "RB_P1_dy":    -8,
        "LI_CENTER_dy":  0,
        "RI_CENTER_dy":  0,
        "M_P1_dy":     -2,
        "M_P2_dy":     -2,
        "M_P0_dy":    +4,
        "M_P3_dy":    +4,
        "blush_alpha":  0,
    },

    "DETERMINED": {
        "LB_P1_dy":    +10,
        "RB_P1_dy":    +10,
        "LB_P1_dx":    +4,
        "RB_P1_dx":    -4,
        "le_lid_drop":  +6,
        "re_lid_drop":  +8,
        "LI_CENTER_dy":  0,
        "RI_CENTER_dy":  0,
        "LI_CENTER_dx":  0,
        "RI_CENTER_dx":  0,
        "M_P1_dy":     -8,
        "M_P2_dy":     -8,
        "M_P0_dy":     -2,
        "M_P3_dy":     -2,
        "blush_alpha":  0,
    },
}

# ── Tolerance thresholds ──────────────────────────────────────────────────────
DEFAULT_TOL_EYE   = 5    # px deviation from 100px canonical eye width
DEFAULT_TOL_BROW  = 5    # px deviation brow apex from expected range
DEFAULT_TOL_MOUTH = 5    # px deviation mouth y from expected range


# ── Control point resolver ────────────────────────────────────────────────────

def resolve_points(deltas):
    """Apply expression deltas to neutral baseline; return resolved point dict."""
    pts = dict(NEUTRAL)

    # Scalar updates
    for key in ("oval_rx", "oval_ry", "blush_alpha", "le_lid_drop", "re_lid_drop"):
        if key in deltas:
            pts[key] = pts[key] + deltas[key]

    # Named point offsets (dx/dy suffixes on point names)
    point_names = [
        "LB_P0", "LB_P1", "LB_P2",
        "RB_P0", "RB_P1", "RB_P2",
        "LE_P0", "LE_P1", "LE_P2", "LE_P3",
        "RE_P0", "RE_P1", "RE_P2", "RE_P3",
        "M_P0",  "M_P1",  "M_P2",  "M_P3",
        "LI_CENTER", "RI_CENTER",
    ]
    for pname in point_names:
        x, y = pts[pname]
        dx_key = pname + "_dx"
        dy_key = pname + "_dy"
        if dx_key in deltas:
            x += deltas[dx_key]
        if dy_key in deltas:
            y += deltas[dy_key]
        pts[pname] = (x, y)

    return pts


# ── Bezier helpers ────────────────────────────────────────────────────────────

def quadratic_bezier_pts(p0, p1, p2, steps=40):
    """Sample N points along a quadratic bezier curve."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
        y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        pts.append((x, y))
    return pts


def cubic_bezier_pts(p0, p1, p2, p3, steps=60):
    """Sample N points along a cubic bezier curve."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = ((1-t)**3 * p0[0] + 3*(1-t)**2*t * p1[0]
             + 3*(1-t)*t**2 * p2[0] + t**3 * p3[0])
        y = ((1-t)**3 * p0[1] + 3*(1-t)**2*t * p1[1]
             + 3*(1-t)*t**2 * p2[1] + t**3 * p3[1])
        pts.append((x, y))
    return pts


def polyline(draw, pts, color, width=2):
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill=color, width=width)


# ── Geometry metric extractor ─────────────────────────────────────────────────

def extract_metrics(pts_dict):
    """
    Compute geometry metrics from resolved control point dict.

    Returns dict:
      eye_width_L   — horizontal distance LE_P0 → LE_P2
      eye_width_R   — horizontal distance RE_P0 → RE_P2
      le_lid_top_y  — LE_P1.y (top of left eye curve)
      re_lid_top_y  — RE_P1.y (top of right eye curve, with lid drop)
      le_lid_drop   — delta from neutral LE_P1.y
      re_lid_drop   — delta from neutral RE_P1.y
      lb_apex_y     — LB_P1.y (left brow apex)
      rb_apex_y     — RB_P1.y (right brow apex)
      mouth_corner_y — average of M_P0.y and M_P3.y (mouth corner height)
      mouth_ctrl_y   — average of M_P1.y and M_P2.y (controls → smile/frown)
    """
    le_p0 = pts_dict["LE_P0"]
    le_p1 = pts_dict["LE_P1"]
    le_p2 = pts_dict["LE_P2"]
    re_p0 = pts_dict["RE_P0"]
    re_p1 = pts_dict["RE_P1"]
    re_p2 = pts_dict["RE_P2"]

    # Lid drop is a separate scalar in pts_dict (applied to P1.y at render time)
    le_lid = pts_dict["le_lid_drop"]
    re_lid = pts_dict["re_lid_drop"]

    return {
        "eye_width_L":        abs(le_p2[0] - le_p0[0]),
        "eye_width_R":        abs(re_p2[0] - re_p0[0]),
        "le_lid_top_y":       le_p1[1],
        "re_lid_top_y":       re_p1[1],
        "le_lid_drop":        le_lid,
        "re_lid_drop":        re_lid,
        "le_lid_drop_delta":  le_lid - NEUTRAL["le_lid_drop"],
        "re_lid_drop_delta":  re_lid - NEUTRAL["re_lid_drop"],
        "lb_apex_y":          pts_dict["LB_P1"][1],
        "rb_apex_y":          pts_dict["RB_P1"][1],
        "lb_apex_rel":        pts_dict["LB_P1"][1] - FC[1],
        "rb_apex_rel":        pts_dict["RB_P1"][1] - FC[1],
        "mouth_corner_y":     (pts_dict["M_P0"][1] + pts_dict["M_P3"][1]) / 2,
        "mouth_ctrl_y":       (pts_dict["M_P1"][1] + pts_dict["M_P2"][1]) / 2,
    }


# ── Tolerance checker ─────────────────────────────────────────────────────────

def check_tolerances(metrics, tol_eye=DEFAULT_TOL_EYE,
                     tol_brow=DEFAULT_TOL_BROW,
                     tol_mouth=DEFAULT_TOL_MOUTH,
                     expression_name=""):
    """
    Check metrics against expected values and return list of issues.

    Returns:
      issues — list of dicts: {level: PASS|WARN|FAIL, metric, value, expected, message}
    """
    issues = []
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"

    # Eye width check (canonical 100px, left eye)
    ew_l = metrics["eye_width_L"]
    ew_r = metrics["eye_width_R"]

    for side, ew in [("LEFT", ew_l), ("RIGHT", ew_r)]:
        dev = abs(ew - EYE_WIDTH_CANON)
        if dev == 0:
            lvl = PASS
        elif dev <= tol_eye:
            lvl = PASS
        elif dev <= tol_eye * 3:
            lvl = WARN
        else:
            lvl = FAIL
        issues.append({
            "level": lvl,
            "metric": f"eye_width_{side}",
            "value": round(ew, 1),
            "expected": EYE_WIDTH_CANON,
            "message": f"{side} eye width {ew:.1f}px (canonical {EYE_WIDTH_CANON}px, delta {dev:.1f}px)",
        })

    # Right-eye lid drop asymmetry check
    # At neutral: re_lid_drop = +6 (canonical signature)
    # At expression: should be >= 0 unless ALARMED (intentional wide open)
    # Flag if re_lid_drop drops below -4 in non-ALARMED expressions
    re_drop = metrics["re_lid_drop"]
    if expression_name not in ("ALARMED",) and re_drop < -4:
        issues.append({
            "level": WARN,
            "metric": "re_lid_drop_asymmetry",
            "value": re_drop,
            "expected": ">= 0 (canonical right-eye signature)",
            "message": (f"Right-eye lid drop {re_drop}px — canonical signature may be lost. "
                        "Re-lid should not go fully wide open except in ALARMED."),
        })
    else:
        issues.append({
            "level": PASS,
            "metric": "re_lid_drop_asymmetry",
            "value": re_drop,
            "expected": ">= 0",
            "message": f"Right-eye lid drop {re_drop}px — signature preserved.",
        })

    # Brow range check
    # LB_P1 relative y (FC-relative): neutral = -88. Reasonable range [-110, -60]
    lb_rel = metrics["lb_apex_rel"]
    rb_rel = metrics["rb_apex_rel"]
    for side, br in [("LB", lb_rel), ("RB", rb_rel)]:
        if -110 <= br <= -60:
            lvl = PASS
        elif -120 <= br <= -50:
            lvl = WARN
        else:
            lvl = FAIL
        issues.append({
            "level": lvl,
            "metric": f"{side}_apex_rel_y",
            "value": br,
            "expected": "range [-110, -60] from FC",
            "message": f"{side} brow apex at FC+{br}px (neutral -88, range [-110,-60])",
        })

    # Mouth corner range check
    # Neutral M_P0/M_P3 y = FC_y + 42 = 322. Range: FC+(+20) to FC+(+65)
    mc_y = metrics["mouth_corner_y"]
    mc_rel = mc_y - FC[1]
    if 20 <= mc_rel <= 65:
        lvl = PASS
    elif 10 <= mc_rel <= 75:
        lvl = WARN
    else:
        lvl = FAIL
    issues.append({
        "level": lvl,
        "metric": "mouth_corner_y_rel",
        "value": round(mc_rel, 1),
        "expected": "range [+20, +65] from FC",
        "message": f"Mouth corners at FC+{mc_rel:.1f}px (neutral +42, range [+20,+65])",
    })

    return issues


# ── Face renderer ─────────────────────────────────────────────────────────────

# Color palette (luma face spec)
SKIN_BASE     = (200, 136,  90)
SKIN_SH       = (160, 104,  64)
OUTLINE_BLACK = ( 59,  40,  32)
EYE_WHITE     = (250, 240, 220)
EYE_IRIS      = (200, 125,  62)
EYE_PUPIL     = ( 59,  40,  32)
EYE_HL        = (240, 240, 240)
BROW_COL      = ( 59,  40,  32)
MOUTH_COL     = ( 59,  40,  32)
BLUSH_PINK    = (232, 148, 100)
PANEL_BG      = (235, 225, 210)

# Annotation colors
ANN_PASS      = ( 40, 180,  60)
ANN_WARN      = (210, 140,  30)
ANN_FAIL      = (210,  50,  50)
ANN_TEXT      = ( 59,  40,  32)
ANN_METRIC    = ( 80, 120, 180)
ANN_GUIDE     = (180, 160, 140, 60)


def render_face(pts_dict, metrics, issues, canvas_scale=0.5):
    """
    Render the face from resolved control points at canvas_scale × 600px.
    Annotates with metric readings and issue flags.
    Returns PIL Image.
    """
    W = int(CANVAS_W * canvas_scale)
    H = int(CANVAS_H * canvas_scale)
    s = canvas_scale

    img  = Image.new("RGB", (W, H), PANEL_BG)
    draw = ImageDraw.Draw(img)

    def sc(pt):
        """Scale a point to the render canvas."""
        return (int(pt[0] * s), int(pt[1] * s))

    def si(v):
        """Scale an integer value."""
        return max(1, int(v * s))

    # ── Face oval ──────────────────────────────────────────────────────────────
    fc_x, fc_y = int(FC[0] * s), int(FC[1] * s)
    orx = si(pts_dict["oval_rx"])
    ory = si(pts_dict["oval_ry"])
    draw.ellipse([fc_x - orx, fc_y - ory, fc_x + orx, fc_y + ory],
                 fill=SKIN_BASE, outline=OUTLINE_BLACK, width=si(3))

    # ── Blush ──────────────────────────────────────────────────────────────────
    ba = min(255, max(0, pts_dict["blush_alpha"]))
    if ba > 0:
        brx = si(pts_dict["blush_rx"])
        bry = si(pts_dict["blush_ry"])
        blush_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        bd = ImageDraw.Draw(blush_img)
        for bc in ("BLUSH_L_CENTER", "BLUSH_R_CENTER"):
            bx, by = sc(pts_dict[bc])
            bd.ellipse([bx - brx, by - bry, bx + brx, by + bry],
                       fill=(BLUSH_PINK[0], BLUSH_PINK[1], BLUSH_PINK[2], ba))
        img = Image.alpha_composite(img.convert("RGBA"), blush_img).convert("RGB")
        draw = ImageDraw.Draw(img)

    # ── Eye outlines ──────────────────────────────────────────────────────────
    def draw_eye(p0_key, p1_key, p2_key, p3_key, lid_drop):
        p0 = sc(pts_dict[p0_key])
        p1_raw = pts_dict[p1_key]
        p1 = sc((p1_raw[0], p1_raw[1] + lid_drop))
        p2 = sc(pts_dict[p2_key])
        p3 = sc(pts_dict[p3_key])

        # Draw top arc (P0 → P1 → P2) as quadratic bezier
        top_pts = quadratic_bezier_pts(p0, p1, p2, steps=30)
        # Draw bottom arc (P0 → P3 → P2) as quadratic bezier
        bot_pts = quadratic_bezier_pts(p0, p3, p2, steps=30)

        # Fill: sample a polygon from top+bottom arcs
        poly = [(int(x), int(y)) for x, y in (top_pts + list(reversed(bot_pts)))]
        if len(poly) >= 3:
            draw.polygon(poly, fill=EYE_WHITE)
        polyline(draw, top_pts, OUTLINE_BLACK, si(3))
        polyline(draw, bot_pts, OUTLINE_BLACK, si(2))

    draw_eye("LE_P0", "LE_P1", "LE_P2", "LE_P3", pts_dict["le_lid_drop"])
    draw_eye("RE_P0", "RE_P1", "RE_P2", "RE_P3", pts_dict["re_lid_drop"])

    # ── Irises + pupils + highlights ──────────────────────────────────────────
    for center_key, r_key in (("LI_CENTER", "LI_R"), ("RI_CENTER", "RI_R")):
        cx_i, cy_i = sc(pts_dict[center_key])
        r_i = si(pts_dict[r_key])
        draw.ellipse([cx_i - r_i, cy_i - r_i, cx_i + r_i, cy_i + r_i],
                     fill=EYE_IRIS, outline=OUTLINE_BLACK, width=si(2))
        rp = max(1, si(5))
        draw.ellipse([cx_i - rp, cy_i - rp, cx_i + rp, cy_i + rp], fill=EYE_PUPIL)
        rh = max(1, si(3))
        draw.ellipse([cx_i - rh - si(4), cy_i - rh - si(4),
                      cx_i - si(4) + rh, cy_i - si(4) + rh],
                     fill=EYE_HL)

    # ── Nose bridge ───────────────────────────────────────────────────────────
    nb_top = sc(fc( 0, -10))
    nb_bot = sc(fc( 0,  10))
    draw.line([nb_top, nb_bot], fill=OUTLINE_BLACK, width=si(2))

    # ── Mouth ─────────────────────────────────────────────────────────────────
    mp0 = sc(pts_dict["M_P0"])
    mp1 = sc(pts_dict["M_P1"])
    mp2 = sc(pts_dict["M_P2"])
    mp3 = sc(pts_dict["M_P3"])
    mouth_pts = cubic_bezier_pts(mp0, mp1, mp2, mp3, steps=40)
    polyline(draw, mouth_pts, MOUTH_COL, si(5))

    # ── Brows ─────────────────────────────────────────────────────────────────
    for p0_key, p1_key, p2_key in (
        ("LB_P0", "LB_P1", "LB_P2"),
        ("RB_P0", "RB_P1", "RB_P2"),
    ):
        brow_pts = quadratic_bezier_pts(
            sc(pts_dict[p0_key]),
            sc(pts_dict[p1_key]),
            sc(pts_dict[p2_key]),
            steps=30,
        )
        polyline(draw, brow_pts, BROW_COL, si(4))

    # ── FC crosshair (faint guide) ─────────────────────────────────────────────
    guide_col = (160, 140, 120)
    draw.line([(fc_x - si(8), fc_y), (fc_x + si(8), fc_y)], fill=guide_col, width=1)
    draw.line([(fc_x, fc_y - si(8)), (fc_x, fc_y + si(8))], fill=guide_col, width=1)

    return img


# ── Annotation panel renderer ─────────────────────────────────────────────────

def render_annotation_panel(metrics, issues, font_small):
    """Render a small metrics/issues panel. Returns PIL Image (panel-width × 200px)."""
    W = 300
    H = 200
    img  = Image.new("RGB", (W, H), (240, 235, 228))
    draw = ImageDraw.Draw(img)

    y = 4
    lh = 16

    # Summary line
    worst = "PASS"
    for iss in issues:
        if iss["level"] == "FAIL":
            worst = "FAIL"
            break
        if iss["level"] == "WARN":
            worst = "WARN"

    col_map = {"PASS": ANN_PASS, "WARN": ANN_WARN, "FAIL": ANN_FAIL}
    draw.rectangle([0, 0, W, lh + 4], fill=col_map[worst])
    draw.text((4, 2), f"GATE: {worst}", fill=(255, 255, 255), font=font_small)
    y += lh + 6

    # Key metrics
    lines = [
        f"Eye W L/R: {metrics['eye_width_L']:.0f} / {metrics['eye_width_R']:.0f}px (canon={EYE_WIDTH_CANON})",
        f"LE lid drop: {metrics['le_lid_drop']:+.0f}px  RE: {metrics['re_lid_drop']:+.0f}px",
        f"LB apex: FC{metrics['lb_apex_rel']:+.0f}  RB: FC{metrics['rb_apex_rel']:+.0f}px",
        f"Mouth corners: FC+{metrics['mouth_corner_y'] - FC[1]:.0f}px  ctrl: FC+{metrics['mouth_ctrl_y'] - FC[1]:.0f}px",
    ]
    for line in lines:
        draw.text((4, y), line, fill=ANN_METRIC, font=font_small)
        y += lh

    # Issues
    y += 2
    for iss in issues:
        if iss["level"] == "PASS":
            continue
        col = col_map.get(iss["level"], ANN_TEXT)
        msg = f"[{iss['level']}] {iss['metric']}: {iss['message']}"
        # Truncate to fit
        if len(msg) > 50:
            msg = msg[:47] + "..."
        draw.text((4, y), msg, fill=col, font=font_small)
        y += lh
        if y > H - lh:
            break

    return img


# ── Contact sheet builder ─────────────────────────────────────────────────────

COLS_SHEET = 3
FACE_SCALE = 0.40   # Each face panel: 600 * 0.40 = 240px wide
ANN_H      = 200    # Annotation panel height
TITLE_H    = 50
PAD_SHEET  = 12


def build_contact_sheet(expressions_to_validate, tol_eye, tol_brow, tol_mouth,
                        font_title, font_label, font_small):
    """
    Build a contact sheet with one panel per expression.
    Returns PIL Image (≤ 1280px in both dims).
    """
    face_w = int(CANVAS_W * FACE_SCALE)
    face_h = int(CANVAS_H * FACE_SCALE)
    ann_w  = 300
    ann_h  = ANN_H

    cell_w = face_w + ann_w + PAD_SHEET
    cell_h = face_h + 30 + PAD_SHEET  # 30px for label

    n      = len(expressions_to_validate)
    cols   = min(COLS_SHEET, n)
    rows   = math.ceil(n / cols)

    sheet_w = cols * (cell_w + PAD_SHEET) + PAD_SHEET
    sheet_h = rows * (cell_h + PAD_SHEET) + PAD_SHEET + TITLE_H

    # Enforce ≤ 1280 limit
    scale = 1.0
    if sheet_w > MAX_DIM or sheet_h > MAX_DIM:
        scale = min(MAX_DIM / sheet_w, MAX_DIM / sheet_h)

    sheet = Image.new("RGB", (sheet_w, sheet_h), (50, 42, 36))
    draw  = ImageDraw.Draw(sheet)

    # Title
    draw.text((PAD_SHEET, 12),
              "LTG Face Curve Validator — Expression Contact Sheet",
              fill=(220, 200, 180), font=font_title)
    draw.text((PAD_SHEET, 32),
              f"Canvas 600×600  |  FC=({FC[0]},{FC[1]})  |  Eye canon={EYE_WIDTH_CANON}px  |  tol_eye=±{tol_eye}px",
              fill=(150, 132, 114), font=font_small)

    all_results = []

    for idx, expr_name in enumerate(expressions_to_validate):
        row = idx // cols
        col = idx % cols

        x0 = PAD_SHEET + col * (cell_w + PAD_SHEET)
        y0 = TITLE_H + PAD_SHEET + row * (cell_h + PAD_SHEET)

        deltas  = EXPRESSION_DELTAS.get(expr_name, {})
        pts     = resolve_points(deltas)
        metrics = extract_metrics(pts)
        issues  = check_tolerances(metrics, tol_eye, tol_brow, tol_mouth, expr_name)

        all_results.append({
            "expression": expr_name,
            "metrics":    metrics,
            "issues":     issues,
        })

        # Determine worst result for this expression
        worst = "PASS"
        for iss in issues:
            if iss["level"] == "FAIL":
                worst = "FAIL"
                break
            if iss["level"] == "WARN":
                worst = "WARN"

        # Cell background
        cell_col = {
            "PASS": (35, 55, 38),
            "WARN": (60, 48, 20),
            "FAIL": (60, 24, 24),
        }.get(worst, (35, 35, 40))
        draw.rectangle([x0, y0, x0 + cell_w, y0 + cell_h], fill=cell_col)

        # Render face
        face_img = render_face(pts, metrics, issues, canvas_scale=FACE_SCALE)
        sheet.paste(face_img, (x0, y0))
        draw = ImageDraw.Draw(sheet)

        # Annotation panel (to the right of face)
        ann_img = render_annotation_panel(metrics, issues, font_small)
        ann_img_resized = ann_img.resize((ann_w, min(face_h, ann_h)), Image.LANCZOS)
        sheet.paste(ann_img_resized, (x0 + face_w + 2, y0))
        draw = ImageDraw.Draw(sheet)

        # Label
        label_col = {"PASS": (100, 210, 100), "WARN": (220, 180, 60), "FAIL": (220, 80, 80)}.get(worst, (200, 200, 200))
        draw.text((x0, y0 + face_h + 4),
                  f"{expr_name}  [{worst}]",
                  fill=label_col, font=font_label)

    # Apply global scale if needed
    if scale < 1.0:
        new_w = int(sheet_w * scale)
        new_h = int(sheet_h * scale)
        sheet = sheet.resize((new_w, new_h), Image.LANCZOS)

    return sheet, all_results


# ── Text report formatter ─────────────────────────────────────────────────────

def format_report(all_results, tol_eye, tol_brow, tol_mouth):
    lines = [
        "=" * 72,
        "LTG_TOOL_face_curve_validator — Expression Geometry Report",
        f"Eye canon={EYE_WIDTH_CANON}px  tol_eye=±{tol_eye}  tol_brow=±{tol_brow}  tol_mouth=±{tol_mouth}",
        f"FC=({FC[0]},{FC[1]})  Canvas 600×600",
        "=" * 72,
        "",
    ]

    overall_worst = "PASS"
    for res in all_results:
        expr = res["expression"]
        m    = res["metrics"]
        iss  = res["issues"]

        worst_expr = "PASS"
        for i in iss:
            if i["level"] == "FAIL":
                worst_expr = "FAIL"
                break
            if i["level"] == "WARN":
                worst_expr = "WARN"

        if worst_expr == "FAIL" and overall_worst != "FAIL":
            overall_worst = "FAIL"
        elif worst_expr == "WARN" and overall_worst == "PASS":
            overall_worst = "WARN"

        lines.append(f"── {expr}  [{worst_expr}]")
        lines.append(f"   Eye width   L={m['eye_width_L']:.1f}px  R={m['eye_width_R']:.1f}px  (canon={EYE_WIDTH_CANON}px)")
        lines.append(f"   Lid drop    LE={m['le_lid_drop']:+.0f}px  RE={m['re_lid_drop']:+.0f}px")
        lines.append(f"   Brow apex   LB=FC{m['lb_apex_rel']:+.0f}px  RB=FC{m['rb_apex_rel']:+.0f}px  (neutral -88px)")
        lines.append(f"   Mouth       corners=FC+{m['mouth_corner_y'] - FC[1]:.0f}px  ctrl=FC+{m['mouth_ctrl_y'] - FC[1]:.0f}px")
        for i in iss:
            if i["level"] != "PASS":
                lines.append(f"   [{i['level']}] {i['metric']}: {i['message']}")
        lines.append("")

    lines.append("=" * 72)
    lines.append(f"OVERALL: {overall_worst}")
    lines.append("=" * 72)
    return "\n".join(lines), overall_worst


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Luma Face Curve Spec Validator — geometry check + contact sheet",
    )
    parser.add_argument("--expression", "-e",
                        help="Validate a single expression by name")
    parser.add_argument("--all", "-a", action="store_true",
                        help="Validate all expressions (default when no --expression given)")
    parser.add_argument("--output-sheet", default=DEFAULT_SHEET,
                        help=f"Output PNG path (default: {DEFAULT_SHEET})")
    parser.add_argument("--report", help="Save text report to file")
    parser.add_argument("--tolerance-eye",   type=int, default=DEFAULT_TOL_EYE)
    parser.add_argument("--tolerance-brow",  type=int, default=DEFAULT_TOL_BROW)
    parser.add_argument("--tolerance-mouth", type=int, default=DEFAULT_TOL_MOUTH)
    args = parser.parse_args()

    if args.expression:
        expr_name = args.expression.upper().replace(" ", "_")
        if expr_name not in EXPRESSION_DELTAS:
            print(f"ERROR: Unknown expression '{expr_name}'")
            print(f"Available: {', '.join(EXPRESSION_DELTAS.keys())}")
            sys.exit(2)
        expressions = [expr_name]
    else:
        expressions = list(EXPRESSION_DELTAS.keys())

    # Fonts
    try:
        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_label = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
        font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = font_title
        font_small = font_title

    # Build sheet
    sheet, all_results = build_contact_sheet(
        expressions,
        args.tolerance_eye,
        args.tolerance_brow,
        args.tolerance_mouth,
        font_title, font_label, font_small,
    )

    # Enforce ≤ 1280px hard limit
    sheet.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)

    # Save sheet
    os.makedirs(os.path.dirname(args.output_sheet), exist_ok=True)
    sheet.save(args.output_sheet)
    print(f"Sheet saved: {args.output_sheet}  ({sheet.width}×{sheet.height}px)")

    # Text report
    report_text, overall = format_report(
        all_results, args.tolerance_eye, args.tolerance_brow, args.tolerance_mouth)
    print(report_text)

    if args.report:
        with open(args.report, "w") as f:
            f.write(report_text)
        print(f"Report saved: {args.report}")

    # Exit code
    if overall == "FAIL":
        sys.exit(2)
    elif overall == "WARN":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
