# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_curve_draw.py — Bezier/Spline Curve Drawing Library for PIL

Provides organic curve-based drawing primitives for character construction.
All functions work with PIL ImageDraw surfaces and use numpy for bezier math.

Cycle 50/51: Initial build (Sam Kowalski).
  - draw_bezier_path: filled closed bezier path
  - draw_bezier_stroke: open bezier stroke
  - tapered_limb: tapered bezier limb segment
  - curved_torso: torso with curved sides
  - gesture_spine: gesture line (S/C curve) generator
  - draw_hair_volume: asymmetric hair mass shape
  - draw_eyelid_shape: expression-driven eyelid curves
  - hand_shape: mitten-style hand silhouettes

Dependencies: Pillow, NumPy
Render scale: works at 2x (2560x1440) for AA — caller downscales to 1280x720.
"""
from __future__ import annotations

import math
from typing import List, Tuple, Optional, Union

import numpy as np
from PIL import Image, ImageDraw


# ---------------------------------------------------------------------------
# Core bezier math
# ---------------------------------------------------------------------------

def _cubic_bezier_point(
    t: float,
    p0: Tuple[float, float],
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    p3: Tuple[float, float],
) -> Tuple[float, float]:
    """Evaluate a single cubic bezier at parameter t in [0,1]."""
    u = 1.0 - t
    x = u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0]
    y = u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1]
    return (x, y)


def _cubic_bezier_points(
    p0: Tuple[float, float],
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    p3: Tuple[float, float],
    num_points: int = 50,
) -> List[Tuple[float, float]]:
    """Sample a cubic bezier segment into a polyline of num_points points."""
    return [
        _cubic_bezier_point(t / (num_points - 1), p0, p1, p2, p3)
        for t in range(num_points)
    ]


def _quadratic_bezier_point(
    t: float,
    p0: Tuple[float, float],
    p1: Tuple[float, float],
    p2: Tuple[float, float],
) -> Tuple[float, float]:
    """Evaluate a quadratic bezier at parameter t in [0,1]."""
    u = 1.0 - t
    x = u**2 * p0[0] + 2 * u * t * p1[0] + t**2 * p2[0]
    y = u**2 * p0[1] + 2 * u * t * p1[1] + t**2 * p2[1]
    return (x, y)


def _quadratic_bezier_points(
    p0: Tuple[float, float],
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    num_points: int = 50,
) -> List[Tuple[float, float]]:
    """Sample a quadratic bezier segment into a polyline."""
    return [
        _quadratic_bezier_point(t / (num_points - 1), p0, p1, p2)
        for t in range(num_points)
    ]


def _multi_segment_bezier(
    anchors: List[Tuple[float, float]],
    controls: List[Tuple[Tuple[float, float], Tuple[float, float]]],
    points_per_segment: int = 50,
) -> List[Tuple[float, float]]:
    """Build a polyline from multiple cubic bezier segments.

    anchors: N+1 anchor points for N segments.
    controls: N pairs of (ctrl_out, ctrl_in) per segment.
        segment i: anchors[i] -> controls[i][0] -> controls[i][1] -> anchors[i+1]
    """
    all_pts: List[Tuple[float, float]] = []
    for i in range(len(controls)):
        seg = _cubic_bezier_points(
            anchors[i], controls[i][0], controls[i][1], anchors[i + 1],
            num_points=points_per_segment,
        )
        if i > 0:
            seg = seg[1:]  # avoid duplicate at junction
        all_pts.extend(seg)
    return all_pts


# ---------------------------------------------------------------------------
# Auto-smooth: derive control points from anchor-only paths
# ---------------------------------------------------------------------------

def _auto_controls(
    anchors: List[Tuple[float, float]],
    tension: float = 0.33,
    closed: bool = False,
) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """Derive smooth cubic bezier control points from anchor points.

    Uses Catmull-Rom style tangent estimation: the tangent at anchor[i] is
    proportional to the vector from anchor[i-1] to anchor[i+1].

    tension: 0.0 = straight lines, 0.5 = maximum smoothing. Default 0.33.
    closed: if True, wraps around (first anchor connects to last).

    Returns list of (ctrl_out, ctrl_in) pairs for each segment.
    """
    n = len(anchors)
    if n < 2:
        return []

    tangents: List[Tuple[float, float]] = []
    for i in range(n):
        if closed:
            prev = anchors[(i - 1) % n]
            nxt = anchors[(i + 1) % n]
        else:
            prev = anchors[max(0, i - 1)]
            nxt = anchors[min(n - 1, i + 1)]
        tangents.append(((nxt[0] - prev[0]) * tension, (nxt[1] - prev[1]) * tension))

    segments = n if closed else n - 1
    controls: List[Tuple[Tuple[float, float], Tuple[float, float]]] = []
    for i in range(segments):
        j = (i + 1) % n
        ctrl_out = (anchors[i][0] + tangents[i][0], anchors[i][1] + tangents[i][1])
        ctrl_in = (anchors[j][0] - tangents[j][0], anchors[j][1] - tangents[j][1])
        controls.append((ctrl_out, ctrl_in))

    return controls


def smooth_path(
    anchors: List[Tuple[float, float]],
    tension: float = 0.33,
    closed: bool = False,
    points_per_segment: int = 50,
) -> List[Tuple[float, float]]:
    """Convert anchor points to a smooth polyline using auto-derived controls.

    This is the simplest API: give it anchor points, get smooth curves.
    """
    controls = _auto_controls(anchors, tension=tension, closed=closed)
    if closed:
        # For closed paths, wrap anchors so _multi_segment_bezier can iterate
        ext_anchors = list(anchors) + [anchors[0]]
    else:
        ext_anchors = list(anchors)
    return _multi_segment_bezier(ext_anchors, controls, points_per_segment)


# ---------------------------------------------------------------------------
# Public drawing API
# ---------------------------------------------------------------------------

def draw_bezier_path(
    draw: ImageDraw.ImageDraw,
    anchors: List[Tuple[float, float]],
    controls: Optional[List[Tuple[Tuple[float, float], Tuple[float, float]]]] = None,
    fill: Optional[Union[Tuple[int, ...], str]] = None,
    outline: Optional[Union[Tuple[int, ...], str]] = None,
    width: int = 1,
    tension: float = 0.33,
    points_per_segment: int = 50,
) -> None:
    """Draw a filled closed bezier path on a PIL ImageDraw surface.

    anchors: list of (x, y) anchor points defining the shape.
    controls: optional list of (ctrl_out, ctrl_in) per segment. If None,
              auto-derived from anchors using Catmull-Rom tangents.
    fill: fill color.
    outline: outline color.
    width: outline width in pixels.
    tension: smoothing tension (only used when controls is None).
    points_per_segment: density of sampled points per bezier segment.
    """
    if controls is not None:
        ext_anchors = list(anchors) + [anchors[0]]
        pts = _multi_segment_bezier(ext_anchors, controls, points_per_segment)
    else:
        pts = smooth_path(anchors, tension=tension, closed=True,
                          points_per_segment=points_per_segment)

    int_pts = [(int(round(x)), int(round(y))) for x, y in pts]

    if fill is not None:
        draw.polygon(int_pts, fill=fill)
    if outline is not None:
        # Draw outline as a closed polyline for width > 1 support
        for i in range(len(int_pts)):
            j = (i + 1) % len(int_pts)
            draw.line([int_pts[i], int_pts[j]], fill=outline, width=width)


def draw_bezier_stroke(
    draw: ImageDraw.ImageDraw,
    anchors: List[Tuple[float, float]],
    controls: Optional[List[Tuple[Tuple[float, float], Tuple[float, float]]]] = None,
    color: Optional[Union[Tuple[int, ...], str]] = None,
    width: int = 2,
    tension: float = 0.33,
    points_per_segment: int = 50,
) -> None:
    """Draw an open bezier stroke (for outlines, wrinkle lines, etc.).

    anchors: list of (x, y) anchor points.
    controls: optional explicit control points. If None, auto-derived.
    color: stroke color.
    width: stroke width in pixels.
    """
    if controls is not None:
        pts = _multi_segment_bezier(anchors, controls, points_per_segment)
    else:
        pts = smooth_path(anchors, tension=tension, closed=False,
                          points_per_segment=points_per_segment)

    int_pts = [(int(round(x)), int(round(y))) for x, y in pts]

    if color is not None:
        for i in range(len(int_pts) - 1):
            draw.line([int_pts[i], int_pts[i + 1]], fill=color, width=width)


def tapered_limb(
    draw: ImageDraw.ImageDraw,
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    w1: float,
    w2: float,
    fill: Optional[Union[Tuple[int, ...], str]] = None,
    outline: Optional[Union[Tuple[int, ...], str]] = None,
    width: int = 1,
    bend: float = 0.0,
    bend_direction: float = 0.0,
    points_per_segment: int = 50,
) -> None:
    """Draw a limb segment as a tapered bezier shape.

    p1: wide end (joint near torso). (x, y)
    p2: narrow end (hand/foot). (x, y)
    w1: width at p1 (full width, not half).
    w2: width at p2.
    fill: fill color.
    outline: outline color.
    width: outline width.
    bend: amount of curvature (0.0 = straight, positive = outward bend).
           Value is fraction of limb length used as control point offset.
    bend_direction: angle in radians for bend direction offset.
                    0.0 = perpendicular to limb axis (default outward).
    """
    # Limb axis
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    length = math.sqrt(dx * dx + dy * dy)
    if length < 1e-6:
        return

    # Unit vectors along and perpendicular to limb
    ax = dx / length
    ay = dy / length
    # Perpendicular (to the right of the axis direction)
    px = -ay
    py = ax

    # Apply bend_direction rotation to perpendicular
    if bend_direction != 0.0:
        cos_bd = math.cos(bend_direction)
        sin_bd = math.sin(bend_direction)
        px2 = px * cos_bd - py * sin_bd
        py2 = px * sin_bd + py * cos_bd
        px, py = px2, py2

    # Build the outline as two curved edges + end caps
    hw1 = w1 / 2.0
    hw2 = w2 / 2.0

    # The four corners of the limb shape
    # Left side (top to bottom)
    tl = (p1[0] + px * hw1, p1[1] + py * hw1)
    bl = (p2[0] + px * hw2, p2[1] + py * hw2)
    # Right side
    tr = (p1[0] - px * hw1, p1[1] - py * hw1)
    br = (p2[0] - px * hw2, p2[1] - py * hw2)

    # Midpoint for bend control
    mid_x = (p1[0] + p2[0]) / 2.0
    mid_y = (p1[1] + p2[1]) / 2.0
    bend_offset_x = px * bend * length
    bend_offset_y = py * bend * length

    # Build left edge as quadratic bezier (tl -> mid+offset -> bl)
    left_mid = (mid_x + px * hw1 * 0.7 + bend_offset_x,
                mid_y + py * hw1 * 0.7 + bend_offset_y)
    left_pts = _quadratic_bezier_points(tl, left_mid, bl, points_per_segment)

    # Build right edge as quadratic bezier (br -> mid-offset -> tr)
    right_mid = (mid_x - px * hw2 * 0.7 - bend_offset_x * 0.5,
                 mid_y - py * hw2 * 0.7 - bend_offset_y * 0.5)
    right_pts = _quadratic_bezier_points(br, right_mid, tr, points_per_segment)

    # Combine into closed polygon: left edge down, right edge up
    all_pts = left_pts + right_pts
    int_pts = [(int(round(x)), int(round(y))) for x, y in all_pts]

    if fill is not None:
        draw.polygon(int_pts, fill=fill)
    if outline is not None:
        for i in range(len(int_pts)):
            j = (i + 1) % len(int_pts)
            draw.line([int_pts[i], int_pts[j]], fill=outline, width=width)


def curved_torso(
    draw: ImageDraw.ImageDraw,
    shoulder_l: Tuple[float, float],
    shoulder_r: Tuple[float, float],
    waist_l: Tuple[float, float],
    waist_r: Tuple[float, float],
    fill: Optional[Union[Tuple[int, ...], str]] = None,
    outline: Optional[Union[Tuple[int, ...], str]] = None,
    width: int = 1,
    shoulder_curve: float = 0.15,
    side_curve: float = 0.12,
    waist_curve: float = 0.08,
    points_per_segment: int = 50,
) -> None:
    """Draw a torso shape defined by shoulder and waist points, with curved sides.

    shoulder_l, shoulder_r: left and right shoulder points (x, y).
    waist_l, waist_r: left and right waist/hip points (x, y).
    fill: fill color.
    outline: outline color.
    width: outline width.
    shoulder_curve: upward bow of shoulder line (fraction of shoulder width).
    side_curve: outward bow of side lines (fraction of torso height).
    waist_curve: downward bow of waist line (fraction of waist width).
    """
    # Shoulder width and torso height for scaling curves
    sw = abs(shoulder_r[0] - shoulder_l[0])
    th = abs(waist_l[1] - shoulder_l[1])
    ww = abs(waist_r[0] - waist_l[0])

    # Top edge: shoulders — slight upward bow (convex)
    shoulder_mid = (
        (shoulder_l[0] + shoulder_r[0]) / 2.0,
        min(shoulder_l[1], shoulder_r[1]) - sw * shoulder_curve,
    )
    top_pts = _quadratic_bezier_points(shoulder_l, shoulder_mid, shoulder_r,
                                       points_per_segment)

    # Right side: shoulder_r to waist_r — slight outward bow
    right_mid = (
        max(shoulder_r[0], waist_r[0]) + th * side_curve,
        (shoulder_r[1] + waist_r[1]) / 2.0,
    )
    right_pts = _quadratic_bezier_points(shoulder_r, right_mid, waist_r,
                                         points_per_segment)

    # Bottom edge: waist — slight downward bow (for hip)
    waist_mid = (
        (waist_l[0] + waist_r[0]) / 2.0,
        max(waist_l[1], waist_r[1]) + ww * waist_curve,
    )
    bottom_pts = _quadratic_bezier_points(waist_r, waist_mid, waist_l,
                                          points_per_segment)

    # Left side: waist_l to shoulder_l — slight outward bow
    left_mid = (
        min(shoulder_l[0], waist_l[0]) - th * side_curve,
        (shoulder_l[1] + waist_l[1]) / 2.0,
    )
    left_pts = _quadratic_bezier_points(waist_l, left_mid, shoulder_l,
                                        points_per_segment)

    # Combine all edges (skip duplicates at junctions)
    all_pts = top_pts + right_pts[1:] + bottom_pts[1:] + left_pts[1:]
    int_pts = [(int(round(x)), int(round(y))) for x, y in all_pts]

    if fill is not None:
        draw.polygon(int_pts, fill=fill)
    if outline is not None:
        for i in range(len(int_pts)):
            j = (i + 1) % len(int_pts)
            draw.line([int_pts[i], int_pts[j]], fill=outline, width=width)


def gesture_spine(
    head_pos: Tuple[float, float],
    foot_pos: Tuple[float, float],
    curve_amount: float = 0.05,
    curve_direction: str = "right",
    curve_type: str = "s",
    num_points: int = 20,
) -> List[Tuple[float, float]]:
    """Generate a gesture line (S-curve or C-curve) for body construction.

    head_pos: top of the spine (x, y).
    foot_pos: base of the spine / weight-bearing foot (x, y).
    curve_amount: magnitude of curvature as fraction of spine length.
                  0.0 = straight, 0.05 = subtle, 0.15 = strong.
    curve_direction: "left" or "right" — primary curve direction.
    curve_type: "s" for S-curve, "c" for C-curve. S-curves have a reversal
                at the midpoint; C-curves bow consistently.
    num_points: number of sample points along the spine.

    Returns: list of (x, y) points along the gesture spine. The body is
             constructed around this spine (shoulder width at ~25%, hip at ~60%).
    """
    dx = foot_pos[0] - head_pos[0]
    dy = foot_pos[1] - head_pos[1]
    length = math.sqrt(dx * dx + dy * dy)
    if length < 1e-6:
        return [head_pos]

    # Perpendicular direction
    ax = dx / length
    ay = dy / length
    px = -ay
    py = ax

    sign = -1.0 if curve_direction == "left" else 1.0
    offset = curve_amount * length

    if curve_type == "s":
        # S-curve: upper body curves one way, lower body curves the other
        # Control points at 33% and 66% of spine
        ctrl1 = (
            head_pos[0] + dx * 0.33 + px * offset * sign,
            head_pos[1] + dy * 0.33 + py * offset * sign,
        )
        ctrl2 = (
            head_pos[0] + dx * 0.66 - px * offset * sign * 0.7,
            head_pos[1] + dy * 0.66 - py * offset * sign * 0.7,
        )
    else:
        # C-curve: consistent bow in one direction
        ctrl1 = (
            head_pos[0] + dx * 0.33 + px * offset * sign,
            head_pos[1] + dy * 0.33 + py * offset * sign,
        )
        ctrl2 = (
            head_pos[0] + dx * 0.66 + px * offset * sign * 0.8,
            head_pos[1] + dy * 0.66 + py * offset * sign * 0.8,
        )

    points = _cubic_bezier_points(head_pos, ctrl1, ctrl2, foot_pos,
                                  num_points=num_points)
    return points


def spine_point_at(
    spine: List[Tuple[float, float]],
    fraction: float,
) -> Tuple[float, float]:
    """Get the (x, y) position at a fraction (0.0=head, 1.0=foot) along a spine."""
    if not spine:
        return (0.0, 0.0)
    idx = fraction * (len(spine) - 1)
    i = int(idx)
    t = idx - i
    if i >= len(spine) - 1:
        return spine[-1]
    return (
        spine[i][0] + t * (spine[i + 1][0] - spine[i][0]),
        spine[i][1] + t * (spine[i + 1][1] - spine[i][1]),
    )


def spine_tangent_at(
    spine: List[Tuple[float, float]],
    fraction: float,
) -> Tuple[float, float]:
    """Get the tangent direction (unit vector) at a fraction along a spine."""
    if len(spine) < 2:
        return (0.0, 1.0)
    idx = fraction * (len(spine) - 1)
    i = max(0, min(int(idx), len(spine) - 2))
    dx = spine[i + 1][0] - spine[i][0]
    dy = spine[i + 1][1] - spine[i][1]
    mag = math.sqrt(dx * dx + dy * dy)
    if mag < 1e-6:
        return (0.0, 1.0)
    return (dx / mag, dy / mag)


def spine_perpendicular_at(
    spine: List[Tuple[float, float]],
    fraction: float,
) -> Tuple[float, float]:
    """Get the perpendicular direction (unit vector) at a fraction along a spine."""
    tx, ty = spine_tangent_at(spine, fraction)
    return (-ty, tx)


# ---------------------------------------------------------------------------
# Higher-level character construction helpers
# ---------------------------------------------------------------------------

def draw_hair_volume(
    draw: ImageDraw.ImageDraw,
    head_center: Tuple[float, float],
    head_radius: float,
    fill: Optional[Union[Tuple[int, ...], str]] = None,
    outline: Optional[Union[Tuple[int, ...], str]] = None,
    width: int = 1,
    asymmetry: float = 0.15,
    volume_top: float = 0.3,
    volume_side: float = 0.2,
    side_bias: str = "right",
    points_per_segment: int = 50,
) -> None:
    """Draw an asymmetric hair mass that overlaps the head boundary.

    head_center: (x, y) center of head circle.
    head_radius: radius of the head.
    fill: hair fill color.
    outline: outline color.
    width: outline width.
    asymmetry: how much more volume on the bias side (fraction of head_radius).
    volume_top: extra height above head (fraction of head_radius).
    volume_side: extra width to the sides (fraction of head_radius).
    side_bias: "left" or "right" — which side gets more volume.
    """
    cx, cy = head_center
    r = head_radius
    sign = 1.0 if side_bias == "right" else -1.0

    # Hair anchors: start from left ear level, go up and over, down to right ear
    # Asymmetric: bias side gets more volume
    anchors = [
        (cx - r - r * volume_side, cy + r * 0.1),                    # left ear
        (cx - r * 0.7, cy - r - r * volume_top * 0.7),               # left crown
        (cx + sign * r * asymmetry, cy - r - r * volume_top),        # peak (biased)
        (cx + r * 0.7, cy - r - r * volume_top * 0.6),               # right crown
        (cx + r + r * volume_side + r * asymmetry * sign, cy + r * 0.1),  # right ear
        (cx + r * 0.3, cy + r * 0.4),                                # right nape
        (cx - r * 0.3, cy + r * 0.4),                                # left nape
    ]

    draw_bezier_path(draw, anchors, fill=fill, outline=outline, width=width,
                     tension=0.35, points_per_segment=points_per_segment)


def draw_eyelid_shape(
    draw: ImageDraw.ImageDraw,
    eye_center: Tuple[float, float],
    eye_width: float,
    eye_height: float,
    expression: str = "neutral",
    fill_white: Optional[Union[Tuple[int, ...], str]] = (255, 255, 255),
    fill_iris: Optional[Union[Tuple[int, ...], str]] = None,
    fill_pupil: Optional[Union[Tuple[int, ...], str]] = (20, 20, 20),
    fill_highlight: Optional[Union[Tuple[int, ...], str]] = (255, 255, 255),
    outline_color: Optional[Union[Tuple[int, ...], str]] = None,
    outline_width: int = 2,
    iris_ratio: float = 0.65,
    pupil_ratio: float = 0.35,
    points_per_segment: int = 50,
) -> None:
    """Draw an expression-driven eye with distinct upper/lower lid curves.

    eye_center: (x, y) center of the eye.
    eye_width: total horizontal extent of the eye opening.
    eye_height: total vertical extent of the eye opening (varies by expression).
    expression: one of "neutral", "happy", "sad", "angry", "surprised", "worried".
    fill_white: sclera color.
    fill_iris: iris color.
    fill_pupil: pupil color.
    fill_highlight: highlight/catchlight color.
    outline_color: lid outline color.
    outline_width: lid outline width.
    iris_ratio: iris diameter as fraction of eye_height.
    pupil_ratio: pupil diameter as fraction of iris diameter.
    """
    cx, cy = eye_center
    hw = eye_width / 2.0
    hh = eye_height / 2.0

    # Define upper and lower lid curves per expression
    # Each lid is 5 anchor points: left corner, left-mid, top/bottom, right-mid, right corner
    if expression == "happy":
        # Squinting — lower lid pushes up, upper lid slightly lowered
        upper = [
            (cx - hw, cy), (cx - hw * 0.5, cy - hh * 0.6),
            (cx, cy - hh * 0.5),
            (cx + hw * 0.5, cy - hh * 0.6), (cx + hw, cy),
        ]
        lower = [
            (cx - hw, cy), (cx - hw * 0.5, cy + hh * 0.2),
            (cx, cy + hh * 0.15),
            (cx + hw * 0.5, cy + hh * 0.2), (cx + hw, cy),
        ]
    elif expression == "sad":
        # Outer corners of upper lid droop
        upper = [
            (cx - hw, cy - hh * 0.1), (cx - hw * 0.5, cy - hh * 0.9),
            (cx, cy - hh),
            (cx + hw * 0.5, cy - hh * 0.7), (cx + hw, cy + hh * 0.15),
        ]
        lower = [
            (cx - hw, cy - hh * 0.1), (cx - hw * 0.5, cy + hh * 0.5),
            (cx, cy + hh * 0.6),
            (cx + hw * 0.5, cy + hh * 0.5), (cx + hw, cy + hh * 0.15),
        ]
    elif expression == "angry":
        # Upper lid drops in V toward nose, lower lid tenses
        upper = [
            (cx - hw, cy - hh * 0.3), (cx - hw * 0.5, cy - hh * 0.8),
            (cx, cy - hh * 0.6),
            (cx + hw * 0.5, cy - hh * 0.4), (cx + hw, cy + hh * 0.1),
        ]
        lower = [
            (cx - hw, cy - hh * 0.3), (cx - hw * 0.5, cy + hh * 0.3),
            (cx, cy + hh * 0.4),
            (cx + hw * 0.5, cy + hh * 0.35), (cx + hw, cy + hh * 0.1),
        ]
    elif expression == "surprised":
        # Upper lid rises above iris, lower lid drops, full iris visible
        upper = [
            (cx - hw, cy), (cx - hw * 0.5, cy - hh * 1.1),
            (cx, cy - hh * 1.2),
            (cx + hw * 0.5, cy - hh * 1.1), (cx + hw, cy),
        ]
        lower = [
            (cx - hw, cy), (cx - hw * 0.5, cy + hh * 0.8),
            (cx, cy + hh * 0.9),
            (cx + hw * 0.5, cy + hh * 0.8), (cx + hw, cy),
        ]
    elif expression == "worried":
        # Similar to sad but with more tension — brows would add to this
        upper = [
            (cx - hw, cy + hh * 0.1), (cx - hw * 0.5, cy - hh * 0.7),
            (cx, cy - hh * 0.85),
            (cx + hw * 0.5, cy - hh * 0.65), (cx + hw, cy + hh * 0.1),
        ]
        lower = [
            (cx - hw, cy + hh * 0.1), (cx - hw * 0.5, cy + hh * 0.5),
            (cx, cy + hh * 0.55),
            (cx + hw * 0.5, cy + hh * 0.5), (cx + hw, cy + hh * 0.1),
        ]
    else:  # neutral
        upper = [
            (cx - hw, cy), (cx - hw * 0.5, cy - hh * 0.85),
            (cx, cy - hh),
            (cx + hw * 0.5, cy - hh * 0.85), (cx + hw, cy),
        ]
        lower = [
            (cx - hw, cy), (cx - hw * 0.5, cy + hh * 0.6),
            (cx, cy + hh * 0.7),
            (cx + hw * 0.5, cy + hh * 0.6), (cx + hw, cy),
        ]

    # Build eye shape from upper + lower lid curves
    upper_pts = smooth_path(upper, tension=0.35, closed=False,
                            points_per_segment=points_per_segment)
    lower_pts = smooth_path(lower, tension=0.35, closed=False,
                            points_per_segment=points_per_segment)

    # Combine into closed eye shape (upper forward, lower reversed)
    eye_shape = upper_pts + list(reversed(lower_pts))
    int_eye = [(int(round(x)), int(round(y))) for x, y in eye_shape]

    # Draw sclera
    if fill_white is not None:
        draw.polygon(int_eye, fill=fill_white)

    # Draw iris (large circle — 65-75% of eye opening height)
    iris_r = eye_height * iris_ratio / 2.0
    if fill_iris is not None:
        iris_bbox = [
            int(cx - iris_r), int(cy - iris_r),
            int(cx + iris_r), int(cy + iris_r),
        ]
        draw.ellipse(iris_bbox, fill=fill_iris)

    # Draw pupil
    pupil_r = iris_r * pupil_ratio
    if fill_pupil is not None:
        pupil_bbox = [
            int(cx - pupil_r), int(cy - pupil_r),
            int(cx + pupil_r), int(cy + pupil_r),
        ]
        draw.ellipse(pupil_bbox, fill=fill_pupil)

    # Draw highlight / catchlight
    if fill_highlight is not None:
        hl_r = max(2, int(iris_r * 0.25))
        hl_cx = int(cx - iris_r * 0.25)
        hl_cy = int(cy - iris_r * 0.3)
        draw.ellipse([hl_cx - hl_r, hl_cy - hl_r, hl_cx + hl_r, hl_cy + hl_r],
                     fill=fill_highlight)

    # Draw lid outlines
    if outline_color is not None:
        for i in range(len(upper_pts) - 1):
            p0 = (int(round(upper_pts[i][0])), int(round(upper_pts[i][1])))
            p1 = (int(round(upper_pts[i+1][0])), int(round(upper_pts[i+1][1])))
            draw.line([p0, p1], fill=outline_color, width=outline_width)
        for i in range(len(lower_pts) - 1):
            p0 = (int(round(lower_pts[i][0])), int(round(lower_pts[i][1])))
            p1 = (int(round(lower_pts[i+1][0])), int(round(lower_pts[i+1][1])))
            draw.line([p0, p1], fill=outline_color, width=outline_width)


def hand_shape(
    draw: ImageDraw.ImageDraw,
    wrist_pos: Tuple[float, float],
    hand_size: float,
    pose: str = "rest",
    angle: float = 0.0,
    fill: Optional[Union[Tuple[int, ...], str]] = None,
    outline: Optional[Union[Tuple[int, ...], str]] = None,
    width: int = 1,
    points_per_segment: int = 30,
) -> None:
    """Draw a mitten-style hand silhouette.

    wrist_pos: (x, y) attachment point at the wrist.
    hand_size: overall scale of the hand (diameter of palm region).
    pose: "rest", "fist", "open", "point".
    angle: rotation in radians (0 = pointing down).
    fill: fill color.
    outline: outline color.
    width: outline width.
    """
    s = hand_size / 2.0

    # Define hand shapes in local coords (wrist at origin, pointing down)
    if pose == "fist":
        local = [
            (-s * 0.7, 0), (-s * 0.8, s * 0.4), (-s * 0.7, s * 0.9),
            (-s * 0.3, s * 1.1), (s * 0.3, s * 1.1),
            (s * 0.7, s * 0.9), (s * 0.8, s * 0.4), (s * 0.7, 0),
        ]
    elif pose == "open":
        local = [
            (-s * 0.6, 0), (-s * 0.9, s * 0.5), (-s * 1.0, s * 1.2),
            (-s * 0.5, s * 1.5), (0, s * 1.6),
            (s * 0.5, s * 1.5), (s * 1.0, s * 1.2),
            (s * 0.9, s * 0.5), (s * 0.6, 0),
        ]
    elif pose == "point":
        # Index finger extended, others curled
        local = [
            (-s * 0.6, 0), (-s * 0.7, s * 0.4), (-s * 0.5, s * 0.9),
            (-s * 0.15, s * 0.9), (-s * 0.1, s * 1.6),  # index tip
            (s * 0.1, s * 1.6), (s * 0.15, s * 0.9),
            (s * 0.5, s * 0.9), (s * 0.7, s * 0.4), (s * 0.6, 0),
        ]
    else:  # rest
        local = [
            (-s * 0.6, 0), (-s * 0.7, s * 0.5), (-s * 0.6, s * 1.0),
            (-s * 0.3, s * 1.3), (0, s * 1.35),
            (s * 0.3, s * 1.3), (s * 0.6, s * 1.0),
            (s * 0.7, s * 0.5), (s * 0.6, 0),
        ]

    # Rotate and translate to world coords
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    anchors = []
    for lx, ly in local:
        rx = lx * cos_a - ly * sin_a + wrist_pos[0]
        ry = lx * sin_a + ly * cos_a + wrist_pos[1]
        anchors.append((rx, ry))

    draw_bezier_path(draw, anchors, fill=fill, outline=outline, width=width,
                     tension=0.35, points_per_segment=points_per_segment)


# ---------------------------------------------------------------------------
# Utility: construct body from gesture spine
# ---------------------------------------------------------------------------

def body_from_spine(
    spine: List[Tuple[float, float]],
    head_radius: float,
    shoulder_width: float,
    waist_width: float,
    hip_width: float,
) -> dict:
    """Derive key body construction points from a gesture spine.

    Returns a dict with positions for: head_center, shoulder_l, shoulder_r,
    waist_l, waist_r, hip_l, hip_r, plus the spine itself.

    Landmark fractions (from character_quality_spec_c50.md):
      head center: 0.0 (top of spine)
      neck: ~0.12
      shoulders: ~0.20
      waist: ~0.50
      hips: ~0.60
      feet: 1.0
    """
    head_center = spine_point_at(spine, 0.0)
    neck = spine_point_at(spine, 0.12)

    sh_pt = spine_point_at(spine, 0.20)
    sh_perp = spine_perpendicular_at(spine, 0.20)
    shoulder_l = (sh_pt[0] + sh_perp[0] * shoulder_width / 2,
                  sh_pt[1] + sh_perp[1] * shoulder_width / 2)
    shoulder_r = (sh_pt[0] - sh_perp[0] * shoulder_width / 2,
                  sh_pt[1] - sh_perp[1] * shoulder_width / 2)

    wa_pt = spine_point_at(spine, 0.50)
    wa_perp = spine_perpendicular_at(spine, 0.50)
    waist_l = (wa_pt[0] + wa_perp[0] * waist_width / 2,
               wa_pt[1] + wa_perp[1] * waist_width / 2)
    waist_r = (wa_pt[0] - wa_perp[0] * waist_width / 2,
               wa_pt[1] - wa_perp[1] * waist_width / 2)

    hi_pt = spine_point_at(spine, 0.60)
    hi_perp = spine_perpendicular_at(spine, 0.60)
    hip_l = (hi_pt[0] + hi_perp[0] * hip_width / 2,
             hi_pt[1] + hi_perp[1] * hip_width / 2)
    hip_r = (hi_pt[0] - hi_perp[0] * hip_width / 2,
             hi_pt[1] - hi_perp[1] * hip_width / 2)

    return {
        "head_center": head_center,
        "neck": neck,
        "shoulder_l": shoulder_l,
        "shoulder_r": shoulder_r,
        "waist_l": waist_l,
        "waist_r": waist_r,
        "hip_l": hip_l,
        "hip_r": hip_r,
        "spine": spine,
    }


# ---------------------------------------------------------------------------
# Visual test — generates sample shapes to verify the library
# ---------------------------------------------------------------------------

def _generate_test_image(output_path: str) -> None:
    """Generate a visual test sheet showing all curve drawing primitives."""
    W, H = 1280, 720
    img = Image.new("RGBA", (W, H), (30, 28, 35, 255))
    draw = ImageDraw.Draw(img)

    # Color palette for test shapes (from LTG master palette)
    HOODIE_ORANGE = (232, 112, 58)
    BYTE_TEAL = (0, 212, 232)
    UV_PURPLE = (123, 47, 190)
    SOFT_GOLD = (232, 201, 90)
    HOT_MAGENTA = (255, 0, 128)
    WARM_CREAM = (250, 240, 220)
    DEEP_SHADOW = (42, 26, 16)
    SKIN_TONE = (200, 136, 90)
    HAIR_DARK = (60, 40, 30)

    # --- Section 1: Bezier paths (top left) ---
    # Organic blob shape
    draw_bezier_path(
        draw,
        anchors=[(80, 60), (160, 40), (220, 80), (200, 150), (120, 160), (60, 120)],
        fill=HOODIE_ORANGE,
        outline=DEEP_SHADOW,
        width=3,
        tension=0.4,
    )
    draw = ImageDraw.Draw(img)  # refresh after potential paste

    # Bezier stroke (open curve)
    draw_bezier_stroke(
        draw,
        anchors=[(260, 60), (300, 120), (350, 80), (400, 140), (440, 100)],
        color=BYTE_TEAL,
        width=4,
        tension=0.4,
    )

    # --- Section 2: Tapered limbs (top center) ---
    # Arm — straight
    tapered_limb(draw, p1=(500, 60), p2=(500, 180), w1=30, w2=16,
                 fill=SKIN_TONE, outline=DEEP_SHADOW, width=2)
    # Arm — bent
    tapered_limb(draw, p1=(560, 60), p2=(600, 180), w1=28, w2=14,
                 fill=SKIN_TONE, outline=DEEP_SHADOW, width=2,
                 bend=0.15)
    # Leg — tapered with bend
    tapered_limb(draw, p1=(660, 60), p2=(640, 200), w1=36, w2=18,
                 fill=(100, 80, 140), outline=DEEP_SHADOW, width=2,
                 bend=-0.1)

    # --- Section 3: Curved torso (top right) ---
    curved_torso(
        draw,
        shoulder_l=(750, 50), shoulder_r=(870, 55),
        waist_l=(770, 180), waist_r=(850, 185),
        fill=HOODIE_ORANGE,
        outline=DEEP_SHADOW,
        width=3,
        shoulder_curve=0.15,
        side_curve=0.12,
    )

    # --- Section 4: Gesture spines (middle left) ---
    # S-curve
    spine_s = gesture_spine((80, 260), (80, 460), curve_amount=0.08,
                            curve_direction="right", curve_type="s")
    for i in range(len(spine_s) - 1):
        p0 = (int(spine_s[i][0]), int(spine_s[i][1]))
        p1 = (int(spine_s[i+1][0]), int(spine_s[i+1][1]))
        draw.line([p0, p1], fill=HOT_MAGENTA, width=3)

    # C-curve
    spine_c = gesture_spine((160, 260), (160, 460), curve_amount=0.10,
                            curve_direction="left", curve_type="c")
    for i in range(len(spine_c) - 1):
        p0 = (int(spine_c[i][0]), int(spine_c[i][1]))
        p1 = (int(spine_c[i+1][0]), int(spine_c[i+1][1]))
        draw.line([p0, p1], fill=SOFT_GOLD, width=3)

    # Strong S
    spine_strong = gesture_spine((240, 260), (240, 460), curve_amount=0.15,
                                 curve_direction="right", curve_type="s")
    for i in range(len(spine_strong) - 1):
        p0 = (int(spine_strong[i][0]), int(spine_strong[i][1]))
        p1 = (int(spine_strong[i+1][0]), int(spine_strong[i+1][1]))
        draw.line([p0, p1], fill=UV_PURPLE, width=3)

    # --- Section 5: Eyes (middle center) ---
    expressions = ["neutral", "happy", "sad", "angry", "surprised", "worried"]
    for idx, expr in enumerate(expressions):
        ex = 400 + idx * 80
        ey = 320
        draw_eyelid_shape(
            draw,
            eye_center=(ex, ey),
            eye_width=50,
            eye_height=35,
            expression=expr,
            fill_iris=(100, 70, 50),
            outline_color=DEEP_SHADOW,
            outline_width=2,
        )
        draw = ImageDraw.Draw(img)  # refresh

    # --- Section 6: Hand shapes (middle right) ---
    poses = ["rest", "fist", "open", "point"]
    for idx, pose in enumerate(poses):
        hx = 950 + (idx % 2) * 80
        hy = 280 + (idx // 2) * 100
        hand_shape(draw, wrist_pos=(hx, hy), hand_size=40, pose=pose,
                   fill=SKIN_TONE, outline=DEEP_SHADOW, width=2)

    # --- Section 7: Hair volume (bottom left) ---
    # Draw head circle first, then hair overlapping
    draw.ellipse([60, 510, 160, 610], fill=SKIN_TONE, outline=DEEP_SHADOW, width=2)
    draw = ImageDraw.Draw(img)
    draw_hair_volume(
        draw,
        head_center=(110, 560),
        head_radius=50,
        fill=HAIR_DARK,
        outline=DEEP_SHADOW,
        width=2,
        asymmetry=0.2,
        volume_top=0.35,
        side_bias="right",
    )
    draw = ImageDraw.Draw(img)

    # --- Section 8: Full body from spine (bottom center/right) ---
    spine = gesture_spine((500, 500), (500, 700), curve_amount=0.06,
                          curve_direction="right", curve_type="s")
    body = body_from_spine(spine, head_radius=30, shoulder_width=80,
                           waist_width=55, hip_width=65)

    # Draw spine line
    for i in range(len(spine) - 1):
        p0 = (int(spine[i][0]), int(spine[i][1]))
        p1 = (int(spine[i+1][0]), int(spine[i+1][1]))
        draw.line([p0, p1], fill=HOT_MAGENTA, width=2)

    # Draw torso
    curved_torso(
        draw,
        shoulder_l=body["shoulder_l"], shoulder_r=body["shoulder_r"],
        waist_l=body["waist_l"], waist_r=body["waist_r"],
        fill=HOODIE_ORANGE, outline=DEEP_SHADOW, width=2,
    )
    draw = ImageDraw.Draw(img)

    # Draw head
    hc = body["head_center"]
    draw.ellipse([int(hc[0]-30), int(hc[1]-30), int(hc[0]+30), int(hc[1]+30)],
                 fill=SKIN_TONE, outline=DEEP_SHADOW, width=2)
    draw = ImageDraw.Draw(img)

    # Draw hair
    draw_hair_volume(draw, head_center=hc, head_radius=30, fill=HAIR_DARK,
                     outline=DEEP_SHADOW, width=2, asymmetry=0.15,
                     volume_top=0.3, side_bias="right")
    draw = ImageDraw.Draw(img)

    # Draw arms (tapered limbs from shoulders)
    tapered_limb(draw, p1=body["shoulder_l"], p2=(body["shoulder_l"][0]-20, body["waist_l"][1]+10),
                 w1=20, w2=12, fill=SKIN_TONE, outline=DEEP_SHADOW, width=2, bend=0.08)
    tapered_limb(draw, p1=body["shoulder_r"], p2=(body["shoulder_r"][0]+15, body["waist_r"][1]+15),
                 w1=20, w2=12, fill=SKIN_TONE, outline=DEEP_SHADOW, width=2, bend=-0.05)

    # Draw legs from hips
    tapered_limb(draw, p1=body["hip_l"], p2=(body["hip_l"][0]-5, 700),
                 w1=24, w2=14, fill=(100, 80, 140), outline=DEEP_SHADOW, width=2)
    tapered_limb(draw, p1=body["hip_r"], p2=(body["hip_r"][0]+5, 700),
                 w1=24, w2=14, fill=(100, 80, 140), outline=DEEP_SHADOW, width=2)

    # Draw eyes on head
    draw_eyelid_shape(draw, eye_center=(hc[0]-10, hc[1]-5), eye_width=16, eye_height=12,
                      expression="neutral", fill_iris=(100, 70, 50),
                      outline_color=DEEP_SHADOW, outline_width=1)
    draw = ImageDraw.Draw(img)
    draw_eyelid_shape(draw, eye_center=(hc[0]+10, hc[1]-5), eye_width=16, eye_height=12,
                      expression="neutral", fill_iris=(100, 70, 50),
                      outline_color=DEEP_SHADOW, outline_width=1)
    draw = ImageDraw.Draw(img)

    # Draw hands
    hand_shape(draw, wrist_pos=(body["shoulder_l"][0]-20, body["waist_l"][1]+10),
               hand_size=16, pose="rest", fill=SKIN_TONE, outline=DEEP_SHADOW, width=1)
    hand_shape(draw, wrist_pos=(body["shoulder_r"][0]+15, body["waist_r"][1]+15),
               hand_size=16, pose="rest", fill=SKIN_TONE, outline=DEEP_SHADOW, width=1)

    # --- Labels ---
    # Simple text labels (no custom font needed)
    labels = [
        ((80, 20), "Bezier Paths"),
        ((260, 20), "Bezier Stroke"),
        ((500, 20), "Tapered Limbs"),
        ((750, 20), "Curved Torso"),
        ((60, 240), "Gesture Spines"),
        ((400, 240), "Eye Expressions"),
        ((930, 240), "Hand Poses"),
        ((40, 490), "Hair Volume"),
        ((420, 480), "Full Body (from spine)"),
    ]
    for pos, text in labels:
        draw.text(pos, text, fill=WARM_CREAM)

    # Expression labels under eyes
    for idx, expr in enumerate(expressions):
        ex = 400 + idx * 80
        draw.text((ex - 20, 350), expr[:4], fill=WARM_CREAM)

    # Save — native 1280x720, no thumbnail()
    img.save(output_path, "PNG")
    print(f"Test image saved: {output_path} ({W}x{H})")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import os
    import sys

    # Determine output path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    output_dir = os.path.join(project_root, "output", "production")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "curve_library_test_c50.png")
    _generate_test_image(output_path)
