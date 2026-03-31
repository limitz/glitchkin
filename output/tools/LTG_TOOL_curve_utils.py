# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_curve_utils.py — v1.0.0 (Cycle 51, Morgan Walsh)

Shared bezier curve utilities wrapping the `bezier` library for arc-length
parameterization, subdivision, intersection detection, and point sampling.

Also wraps Shapely for silhouette polygon operations (outline extraction,
overlap computation, area measurement).

This module replaces hand-rolled bezier3/bezier4/bezier_point functions
duplicated across 9+ tools. Existing tools can migrate by importing from
here instead of defining their own.

Migration guide — replace local definitions with:

    from LTG_TOOL_curve_utils import (
        quadratic_bezier_pts,    # replaces bezier3, _bezier3, quadratic_bezier_pts
        cubic_bezier_pts,        # replaces bezier4, bezier_point+loop, cubic_bezier_pts
        cubic_bezier_single,     # replaces bezier_point (single t value)
        draw_bezier_polyline,    # replaces draw_bezier_curve
        arc_length,              # NEW: true arc length of a bezier curve
        subdivide_at_t,          # NEW: De Casteljau subdivision
        curve_intersections,     # NEW: find intersections between two curves
        curvature_at_t,          # NEW: curvature (1/radius) at parameter t
        uniform_t_by_arclength,  # NEW: arc-length parameterized t values
    )

For Shapely silhouette operations:

    from LTG_TOOL_curve_utils import (
        mask_to_polygon,         # binary mask -> Shapely Polygon
        polygon_overlap_ratio,   # intersection area / min area
        polygon_iou,             # intersection / union
        simplify_outline,        # Douglas-Peucker simplification
        outline_to_points,       # Shapely polygon -> list of (x,y)
    )

Dependencies:
    - bezier (pip install bezier)
    - Shapely (pip install Shapely)
    - numpy
    - PIL/Pillow (for draw_bezier_polyline)

Author: Morgan Walsh — Cycle 51
"""

import math
import warnings
from typing import List, Optional, Sequence, Tuple, Union

import numpy as np

# ─── BEZIER LIBRARY IMPORT ──────────────────────────────────────────────────

try:
    import bezier as _bezier_lib
    BEZIER_AVAILABLE = True
except ImportError:
    BEZIER_AVAILABLE = False
    warnings.warn(
        "bezier library not installed. Install with: pip install bezier. "
        "Falling back to hand-rolled implementations.",
        ImportWarning,
        stacklevel=2,
    )

# ─── SHAPELY IMPORT ─────────────────────────────────────────────────────────

try:
    from shapely.geometry import Polygon as _ShapelyPolygon
    from shapely.geometry import MultiPolygon as _ShapelyMultiPolygon
    from shapely import ops as _shapely_ops
    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False
    warnings.warn(
        "Shapely not installed. Install with: pip install Shapely. "
        "Silhouette polygon operations will not be available.",
        ImportWarning,
        stacklevel=2,
    )

# ─── TYPE ALIASES ────────────────────────────────────────────────────────────

Point = Tuple[float, float]
PointList = List[Tuple[int, int]]


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 1: BEZIER CURVE SAMPLING (drop-in replacements for hand-rolled code)
# ═══════════════════════════════════════════════════════════════════════════════

def _fallback_quadratic(p0, p1, p2, steps):
    """Hand-rolled quadratic bezier (fallback when bezier lib unavailable)."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        x = u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0]
        y = u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]
        pts.append((int(round(x)), int(round(y))))
    return pts


def _fallback_cubic(p0, p1, p2, p3, steps):
    """Hand-rolled cubic bezier (fallback when bezier lib unavailable)."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        x = (u**3 * p0[0] + 3 * u**2 * t * p1[0]
             + 3 * u * t**2 * p2[0] + t**3 * p3[0])
        y = (u**3 * p0[1] + 3 * u**2 * t * p1[1]
             + 3 * u * t**2 * p2[1] + t**3 * p3[1])
        pts.append((int(round(x)), int(round(y))))
    return pts


def _make_quadratic_curve(p0, p1, p2):
    """Create a bezier.Curve object for a quadratic bezier."""
    nodes = np.asfortranarray([
        [p0[0], p1[0], p2[0]],
        [p0[1], p1[1], p2[1]],
    ])
    return _bezier_lib.Curve(nodes, degree=2)


def _make_cubic_curve(p0, p1, p2, p3):
    """Create a bezier.Curve object for a cubic bezier."""
    nodes = np.asfortranarray([
        [p0[0], p1[0], p2[0], p3[0]],
        [p0[1], p1[1], p2[1], p3[1]],
    ])
    return _bezier_lib.Curve(nodes, degree=3)


def _sample_curve(curve, steps):
    """Sample points from a bezier.Curve at uniform t intervals."""
    t_vals = np.linspace(0.0, 1.0, steps + 1)
    points = curve.evaluate_multi(t_vals)  # shape (2, steps+1)
    pts = []
    for i in range(points.shape[1]):
        pts.append((int(round(points[0, i])), int(round(points[1, i]))))
    return pts


def quadratic_bezier_pts(p0, p1, p2, steps=48):
    """Sample points along a quadratic bezier curve.

    Drop-in replacement for: bezier3, _bezier3, quadratic_bezier_pts (local).

    Args:
        p0: Start point (x, y).
        p1: Control point (x, y).
        p2: End point (x, y).
        steps: Number of line segments (yields steps+1 points).

    Returns:
        List of (int, int) tuples along the curve.
    """
    if BEZIER_AVAILABLE:
        curve = _make_quadratic_curve(p0, p1, p2)
        return _sample_curve(curve, steps)
    return _fallback_quadratic(p0, p1, p2, steps)


def cubic_bezier_pts(p0, p1, p2, p3, steps=60):
    """Sample points along a cubic bezier curve.

    Drop-in replacement for: bezier4, cubic_bezier_pts (local).

    Args:
        p0: Start point (x, y).
        p1: First control point (x, y).
        p2: Second control point (x, y).
        p3: End point (x, y).
        steps: Number of line segments (yields steps+1 points).

    Returns:
        List of (int, int) tuples along the curve.
    """
    if BEZIER_AVAILABLE:
        curve = _make_cubic_curve(p0, p1, p2, p3)
        return _sample_curve(curve, steps)
    return _fallback_cubic(p0, p1, p2, p3, steps)


def cubic_bezier_single(p0, p1, p2, p3, t):
    """Evaluate a single point on a cubic bezier at parameter t.

    Drop-in replacement for: bezier_point(p0, p1, p2, p3, t).

    Args:
        p0, p1, p2, p3: Control points as (x, y) tuples.
        t: Parameter in [0, 1].

    Returns:
        (int, int) tuple — point on the curve at t.
    """
    if BEZIER_AVAILABLE:
        curve = _make_cubic_curve(p0, p1, p2, p3)
        point = curve.evaluate(t)  # shape (2, 1)
        return (int(round(point[0, 0])), int(round(point[1, 0])))
    u = 1 - t
    x = (u**3 * p0[0] + 3 * u**2 * t * p1[0]
         + 3 * u * t**2 * p2[0] + t**3 * p3[0])
    y = (u**3 * p0[1] + 3 * u**2 * t * p1[1]
         + 3 * u * t**2 * p2[1] + t**3 * p3[1])
    return (int(round(x)), int(round(y)))


def draw_bezier_polyline(draw, p0, p1, p2, p3, color, width=2, steps=30):
    """Draw a cubic bezier as a PIL polyline.

    Drop-in replacement for: draw_bezier_curve(draw, p0, p1, p2, p3, color, width, steps).

    Args:
        draw: PIL ImageDraw instance.
        p0, p1, p2, p3: Control points.
        color: Line color.
        width: Line width in pixels.
        steps: Number of line segments.

    Returns:
        List of (int, int) points along the curve.
    """
    pts = cubic_bezier_pts(p0, p1, p2, p3, steps)
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=color, width=width)
    return pts


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 2: ADVANCED BEZIER OPERATIONS (bezier library required)
# ═══════════════════════════════════════════════════════════════════════════════

def _require_bezier(fn_name):
    if not BEZIER_AVAILABLE:
        raise ImportError(
            f"{fn_name}() requires the bezier library. "
            "Install with: pip install bezier"
        )


def make_curve(control_points):
    """Create a bezier.Curve from a list of control points.

    Args:
        control_points: List of (x, y) tuples. Length determines degree:
            2 points = linear, 3 = quadratic, 4 = cubic.

    Returns:
        bezier.Curve instance.
    """
    _require_bezier("make_curve")
    n = len(control_points)
    nodes = np.asfortranarray([
        [p[0] for p in control_points],
        [p[1] for p in control_points],
    ])
    return _bezier_lib.Curve(nodes, degree=n - 1)


def arc_length(control_points):
    """Compute the true arc length of a bezier curve.

    Uses the bezier library's numerical integration for accurate results,
    unlike the polygon-length approximation used by hand-rolled code.

    Args:
        control_points: List of (x, y) tuples (2-4 points).

    Returns:
        float — arc length in pixels.
    """
    _require_bezier("arc_length")
    curve = make_curve(control_points)
    return float(curve.length)


def subdivide_at_t(control_points, t=0.5):
    """Subdivide a bezier curve at parameter t using De Casteljau's algorithm.

    Args:
        control_points: List of (x, y) tuples.
        t: Split parameter in (0, 1).

    Returns:
        (left_curve, right_curve) — each a bezier.Curve instance.
    """
    _require_bezier("subdivide_at_t")
    curve = make_curve(control_points)
    left, right = curve.subdivide()
    # The library's subdivide() always splits at t=0.5.
    # For arbitrary t, we evaluate manually using De Casteljau.
    if abs(t - 0.5) < 1e-9:
        return left, right
    # For arbitrary t: use the curve's nodes and De Casteljau manually
    nodes = np.array(control_points, dtype=np.float64)
    n = len(nodes)
    # De Casteljau triangle
    triangle = [nodes.copy()]
    for level in range(1, n):
        prev = triangle[-1]
        new_level = (1 - t) * prev[:-1] + t * prev[1:]
        triangle.append(new_level)
    # Left curve: first element of each level
    left_pts = [tuple(triangle[k][0]) for k in range(n)]
    # Right curve: last element of each level (reversed)
    right_pts = [tuple(triangle[n - 1 - k][k]) for k in range(n)]
    return make_curve(left_pts), make_curve(right_pts)


def curve_intersections(cp_a, cp_b):
    """Find intersection points between two bezier curves.

    Args:
        cp_a: Control points of curve A — list of (x, y) tuples.
        cp_b: Control points of curve B — list of (x, y) tuples.

    Returns:
        List of (x, y) float tuples — intersection points.
        Empty list if no intersections.
    """
    _require_bezier("curve_intersections")
    curve_a = make_curve(cp_a)
    curve_b = make_curve(cp_b)
    try:
        intersections = curve_a.intersect(curve_b)
        # intersections is a 2×N array of (s, t) parameter pairs
        if intersections.size == 0:
            return []
        result = []
        for i in range(intersections.shape[1]):
            s_val = intersections[0, i]
            pt = curve_a.evaluate(s_val)
            result.append((float(pt[0, 0]), float(pt[1, 0])))
        return result
    except Exception:
        return []


def curvature_at_t(control_points, t):
    """Compute curvature (1/radius) at parameter t on a bezier curve.

    High curvature = sharp bend. Low curvature = gentle sweep.
    Useful for QA: detecting kinks or overly sharp bends in character curves.

    Args:
        control_points: List of (x, y) tuples.
        t: Parameter in [0, 1].

    Returns:
        float — curvature value. 0.0 = straight line. Higher = sharper.
    """
    _require_bezier("curvature_at_t")
    curve = make_curve(control_points)
    # Numerical differentiation
    dt = 1e-6
    t0 = max(0.0, t - dt)
    t1 = min(1.0, t + dt)
    t_mid = t

    p0 = curve.evaluate(t0)
    p1 = curve.evaluate(t_mid)
    p2 = curve.evaluate(t1)

    # First derivative approximation
    dx = float(p2[0, 0] - p0[0, 0]) / (t1 - t0)
    dy = float(p2[1, 0] - p0[1, 0]) / (t1 - t0)

    # Second derivative approximation
    dt2 = t1 - t0
    ddx = float(p2[0, 0] - 2 * p1[0, 0] + p0[0, 0]) / ((dt2 / 2) ** 2)
    ddy = float(p2[1, 0] - 2 * p1[1, 0] + p0[1, 0]) / ((dt2 / 2) ** 2)

    # Curvature formula: |x'y'' - y'x''| / (x'^2 + y'^2)^(3/2)
    numerator = abs(dx * ddy - dy * ddx)
    denominator = (dx * dx + dy * dy) ** 1.5
    if denominator < 1e-12:
        return 0.0
    return numerator / denominator


def uniform_t_by_arclength(control_points, n_points=50):
    """Generate parameter values that produce evenly-spaced points along the curve.

    Standard uniform-t sampling bunches points on flat segments and spreads them
    on sharp bends. Arc-length parameterization distributes points evenly along
    the actual curve length — critical for smooth stroking and animation.

    Args:
        control_points: List of (x, y) tuples.
        n_points: Number of output points (including endpoints).

    Returns:
        List of float t-values in [0, 1] that produce ~uniform arc-length spacing.
    """
    _require_bezier("uniform_t_by_arclength")
    curve = make_curve(control_points)
    total_len = curve.length
    if total_len < 1e-9:
        return [0.0] * n_points

    # Oversample at fine resolution, then pick by cumulative distance
    n_fine = max(500, n_points * 10)
    t_fine = np.linspace(0.0, 1.0, n_fine)
    pts = curve.evaluate_multi(t_fine)  # (2, n_fine)

    # Compute cumulative arc length
    diffs = np.diff(pts, axis=1)
    seg_lengths = np.sqrt(diffs[0] ** 2 + diffs[1] ** 2)
    cum_len = np.zeros(n_fine)
    cum_len[1:] = np.cumsum(seg_lengths)

    # Interpolate t values at uniform arc-length intervals
    target_lengths = np.linspace(0.0, cum_len[-1], n_points)
    result_t = np.interp(target_lengths, cum_len, t_fine)
    return result_t.tolist()


def sample_at_arclength(control_points, n_points=50):
    """Sample points evenly spaced along arc length.

    Args:
        control_points: List of (x, y) tuples.
        n_points: Number of output points.

    Returns:
        List of (int, int) tuples evenly distributed along the curve.
    """
    t_vals = uniform_t_by_arclength(control_points, n_points)
    curve = make_curve(control_points)
    t_arr = np.array(t_vals)
    pts_arr = curve.evaluate_multi(t_arr)
    return [(int(round(pts_arr[0, i])), int(round(pts_arr[1, i])))
            for i in range(pts_arr.shape[1])]


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 3: SHAPELY SILHOUETTE OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def _require_shapely(fn_name):
    if not SHAPELY_AVAILABLE:
        raise ImportError(
            f"{fn_name}() requires Shapely. "
            "Install with: pip install Shapely"
        )


def mask_to_polygon(mask, simplify_tolerance=1.5):
    """Convert a binary numpy mask to a Shapely Polygon.

    Extracts the outer contour of the largest connected component in the mask
    and returns it as a Shapely Polygon suitable for geometric operations.

    Args:
        mask: 2D numpy array (uint8), 1 = foreground, 0 = background.
        simplify_tolerance: Douglas-Peucker tolerance for contour simplification.
            Higher = fewer vertices = faster operations. 1.5 is good for QA.

    Returns:
        shapely.geometry.Polygon or None if no foreground pixels.
    """
    _require_shapely("mask_to_polygon")

    # Find contour using numpy (no OpenCV dependency required for basic case)
    # We'll trace the outline by finding boundary pixels
    if mask.sum() == 0:
        return None

    # Pad to ensure contour is closed even if touching edges
    padded = np.pad(mask, 1, mode='constant', constant_values=0)

    # Use a simple contour-tracing approach via edge detection
    # Horizontal edges: difference between adjacent rows
    h_edges = np.diff(padded, axis=0)
    # Vertical edges: difference between adjacent columns
    v_edges = np.diff(padded, axis=1)

    # Collect boundary pixel coordinates
    boundary_rows, boundary_cols = [], []
    hy, hx = np.where(h_edges != 0)
    vy, vx = np.where(v_edges != 0)

    # Combine edge pixels (undo padding offset)
    all_y = np.concatenate([hy - 1, vy - 1])
    all_x = np.concatenate([hx - 1, vx - 1])

    if len(all_y) == 0:
        return None

    # Get unique boundary points
    coords = set(zip(all_x.tolist(), all_y.tolist()))
    if len(coords) < 3:
        return None

    # Sort by angle from centroid to form a valid polygon
    cx = sum(c[0] for c in coords) / len(coords)
    cy = sum(c[1] for c in coords) / len(coords)
    sorted_coords = sorted(coords, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
    sorted_coords.append(sorted_coords[0])  # close the ring

    try:
        poly = _ShapelyPolygon(sorted_coords)
        if not poly.is_valid:
            poly = poly.buffer(0)  # fix self-intersections
        if simplify_tolerance > 0:
            poly = poly.simplify(simplify_tolerance, preserve_topology=True)
        # If buffer() returned a MultiPolygon, take the largest
        if isinstance(poly, _ShapelyMultiPolygon):
            poly = max(poly.geoms, key=lambda g: g.area)
        return poly
    except Exception:
        return None


def mask_to_polygon_cv2(mask, simplify_tolerance=1.5):
    """Convert a binary mask to Shapely Polygon using OpenCV contours (more accurate).

    Preferred over mask_to_polygon() when cv2 is available — OpenCV's
    findContours produces cleaner outlines.

    Args:
        mask: 2D numpy array (uint8), values 0 or 1.
        simplify_tolerance: Douglas-Peucker tolerance.

    Returns:
        shapely.geometry.Polygon or None.
    """
    _require_shapely("mask_to_polygon_cv2")
    try:
        import cv2
    except ImportError:
        # Fall back to pure-numpy version
        return mask_to_polygon(mask, simplify_tolerance)

    mask_255 = (mask * 255).astype(np.uint8)
    contours, _ = cv2.findContours(mask_255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    # Take the largest contour
    largest = max(contours, key=cv2.contourArea)
    if len(largest) < 3:
        return None

    coords = [(int(pt[0][0]), int(pt[0][1])) for pt in largest]
    coords.append(coords[0])  # close ring

    try:
        poly = _ShapelyPolygon(coords)
        if not poly.is_valid:
            poly = poly.buffer(0)
        if simplify_tolerance > 0:
            poly = poly.simplify(simplify_tolerance, preserve_topology=True)
        if isinstance(poly, _ShapelyMultiPolygon):
            poly = max(poly.geoms, key=lambda g: g.area)
        return poly
    except Exception:
        return None


def polygon_overlap_ratio(poly_a, poly_b):
    """Compute Silhouette Overlap Ratio using Shapely geometric operations.

    SOR = intersection_area / min(area_A, area_B)

    This is a geometric replacement for Kai's pixel-level silhouette_overlap_ratio()
    in LTG_TOOL_silhouette_distinctiveness.py. Advantages:
    - Resolution-independent (works on the actual shapes, not pixel grids)
    - Faster for complex outlines (polygon intersection vs pixel-by-pixel)
    - Handles rotation and scaling without re-rasterizing

    Args:
        poly_a: Shapely Polygon for character A.
        poly_b: Shapely Polygon for character B.

    Returns:
        float in [0, 1]. 1.0 = identical outlines. 0.0 = no overlap.
    """
    _require_shapely("polygon_overlap_ratio")
    if poly_a is None or poly_b is None:
        return 0.0
    try:
        intersection = poly_a.intersection(poly_b)
        inter_area = intersection.area
        min_area = min(poly_a.area, poly_b.area)
        if min_area < 1e-9:
            return 0.0
        return inter_area / min_area
    except Exception:
        return 0.0


def polygon_iou(poly_a, poly_b):
    """Intersection over Union for two Shapely Polygons.

    Args:
        poly_a, poly_b: Shapely Polygon instances.

    Returns:
        float in [0, 1]. 1.0 = identical. 0.0 = no overlap.
    """
    _require_shapely("polygon_iou")
    if poly_a is None or poly_b is None:
        return 0.0
    try:
        intersection = poly_a.intersection(poly_b)
        union = poly_a.union(poly_b)
        if union.area < 1e-9:
            return 0.0
        return intersection.area / union.area
    except Exception:
        return 0.0


def simplify_outline(poly, tolerance=2.0):
    """Simplify a polygon outline using Douglas-Peucker.

    Args:
        poly: Shapely Polygon.
        tolerance: Simplification tolerance in pixels.

    Returns:
        Simplified Shapely Polygon.
    """
    _require_shapely("simplify_outline")
    if poly is None:
        return None
    return poly.simplify(tolerance, preserve_topology=True)


def outline_to_points(poly):
    """Extract the exterior ring of a Shapely Polygon as (x, y) integer tuples.

    Useful for converting back to PIL drawing coordinates.

    Args:
        poly: Shapely Polygon.

    Returns:
        List of (int, int) tuples.
    """
    _require_shapely("outline_to_points")
    if poly is None:
        return []
    coords = list(poly.exterior.coords)
    return [(int(round(x)), int(round(y))) for x, y in coords]


def polygon_width_profile(poly, n_rows=None):
    """Compute per-row width profile of a Shapely Polygon.

    Geometric replacement for the pixel-scanning width_profile() in
    silhouette_distinctiveness.py. Slices the polygon at each row height
    and measures the horizontal extent.

    Args:
        poly: Shapely Polygon.
        n_rows: Number of rows to sample (default: polygon bounding box height).

    Returns:
        numpy array of float widths, shape (n_rows,).
    """
    _require_shapely("polygon_width_profile")
    if poly is None:
        return np.zeros(0)

    from shapely.geometry import LineString

    minx, miny, maxx, maxy = poly.bounds
    height = maxy - miny
    if n_rows is None:
        n_rows = max(1, int(height))

    profile = np.zeros(n_rows, dtype=np.float64)
    for i in range(n_rows):
        y = miny + (height * i / n_rows)
        scanline = LineString([(minx - 1, y), (maxx + 1, y)])
        try:
            intersection = poly.intersection(scanline)
            if intersection.is_empty:
                continue
            profile[i] = intersection.length
        except Exception:
            continue
    return profile


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 4: POLYLINE HELPER (PIL draw convenience)
# ═══════════════════════════════════════════════════════════════════════════════

def polyline(draw, pts, color, width=2):
    """Draw a polyline through a list of points on a PIL ImageDraw.

    Shared convenience function — many tools define their own identical copy.

    Args:
        draw: PIL ImageDraw instance.
        pts: List of (x, y) tuples.
        color: Line fill color.
        width: Line width.
    """
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=color, width=width)


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 5: AUDIT HELPER — find hand-rolled bezier functions in the codebase
# ═══════════════════════════════════════════════════════════════════════════════

# Known hand-rolled bezier function signatures across the codebase (C51 audit):
HAND_ROLLED_BEZIER_REGISTRY = {
    "LTG_TOOL_luma_construction_prototype.py": {
        "functions": ["bezier3", "bezier4"],
        "usage": "torso curves, arm curves, shadow",
        "migration": "replace with quadratic_bezier_pts / cubic_bezier_pts",
    },
    "LTG_TOOL_luma_gesture_prototype.py": {
        "functions": ["bezier_point", "draw_bezier_curve"],
        "usage": "gesture line drawing, single-point eval",
        "migration": "replace with cubic_bezier_single / draw_bezier_polyline",
    },
    "LTG_TOOL_face_curve_validator.py": {
        "functions": ["quadratic_bezier_pts", "cubic_bezier_pts"],
        "usage": "face curve QA validation",
        "migration": "import from curve_utils (same names, drop-in)",
    },
    "LTG_TOOL_luma_face_curves.py": {
        "functions": ["_quadratic_bezier_points", "_cubic_bezier_points"],
        "usage": "face bezier rendering (eyes, mouth, brows)",
        "migration": "replace with quadratic_bezier_pts / cubic_bezier_pts",
    },
    "LTG_TOOL_luma_expression_sheet.py": {
        "functions": ["bezier3"],
        "usage": "expression sheet face curves",
        "migration": "replace with quadratic_bezier_pts",
    },
    "LTG_TOOL_sb_cold_open_P17_chartest.py": {
        "functions": ["bezier3", "bezier4"],
        "usage": "storyboard character test (torso, arms)",
        "migration": "replace with quadratic_bezier_pts / cubic_bezier_pts",
    },
    "LTG_TOOL_character_lineup.py": {
        "functions": ["_bezier3"],
        "usage": "lineup Luma bezier curves",
        "migration": "replace with quadratic_bezier_pts",
    },
    "LTG_TOOL_grandma_miri_expression_sheet.py": {
        "functions": ["bezier3"],
        "usage": "Miri expression face curves",
        "migration": "replace with quadratic_bezier_pts",
    },
    "LTG_TOOL_rendering_comparison.py": {
        "functions": ["_bezier_edge_cairo"],
        "usage": "cairo bezier edge drawing (different API — cairo ctx, not PIL)",
        "migration": "NOT a migration target — uses cairo ctx.curve_to(), not PIL polyline",
    },
}


def audit_hand_rolled_bezier(tools_dir=None):
    """Scan tools directory for files still using hand-rolled bezier functions.

    Returns a list of dicts: {file, functions, migrated}.
    'migrated' is True if the file imports from LTG_TOOL_curve_utils.

    Args:
        tools_dir: Path to output/tools/. Auto-detected if None.

    Returns:
        List of audit result dicts.
    """
    import pathlib

    if tools_dir is None:
        here = pathlib.Path(__file__).resolve().parent
        tools_dir = here
    else:
        tools_dir = pathlib.Path(tools_dir)

    results = []
    for filename, info in HAND_ROLLED_BEZIER_REGISTRY.items():
        filepath = tools_dir / filename
        if not filepath.exists():
            results.append({
                "file": filename,
                "functions": info["functions"],
                "status": "NOT_FOUND",
                "migrated": False,
                "note": info.get("migration", ""),
            })
            continue

        content = filepath.read_text(errors="replace")
        imports_curve_utils = "LTG_TOOL_curve_utils" in content

        # Check if local function definitions still exist
        local_defs = []
        for fn in info["functions"]:
            if f"def {fn}(" in content:
                local_defs.append(fn)

        if imports_curve_utils and not local_defs:
            status = "MIGRATED"
        elif imports_curve_utils and local_defs:
            status = "PARTIAL"
        else:
            status = "NOT_MIGRATED"

        results.append({
            "file": filename,
            "functions": info["functions"],
            "local_defs_remaining": local_defs,
            "status": status,
            "migrated": status == "MIGRATED",
            "note": info.get("migration", ""),
        })

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════════════════════

def _cli():
    """CLI entry point — run audit and demonstrate capabilities."""
    import argparse
    import pathlib

    parser = argparse.ArgumentParser(
        description="LTG Curve Utils — bezier library wrapper + Shapely silhouette ops",
    )
    parser.add_argument("--audit", action="store_true",
                        help="Audit tools for hand-rolled bezier functions")
    parser.add_argument("--demo", action="store_true",
                        help="Run a quick demo of bezier library features")
    parser.add_argument("--tools-dir", type=str, default=None,
                        help="Path to output/tools/ (auto-detected if omitted)")
    args = parser.parse_args()

    if args.audit:
        results = audit_hand_rolled_bezier(args.tools_dir)
        print("=" * 70)
        print("HAND-ROLLED BEZIER AUDIT")
        print("=" * 70)
        migrated = sum(1 for r in results if r["status"] == "MIGRATED")
        partial = sum(1 for r in results if r["status"] == "PARTIAL")
        not_migrated = sum(1 for r in results if r["status"] == "NOT_MIGRATED")
        not_found = sum(1 for r in results if r["status"] == "NOT_FOUND")

        for r in results:
            status_icon = {
                "MIGRATED": "PASS",
                "PARTIAL": "WARN",
                "NOT_MIGRATED": "PEND",
                "NOT_FOUND": "SKIP",
            }.get(r["status"], "????")
            print(f"  [{status_icon}] {r['file']}")
            print(f"         Functions: {', '.join(r['functions'])}")
            if r.get("local_defs_remaining"):
                print(f"         Still local: {', '.join(r['local_defs_remaining'])}")
            print(f"         Note: {r['note']}")
            print()

        print(f"Summary: {migrated} MIGRATED, {partial} PARTIAL, "
              f"{not_migrated} NOT_MIGRATED, {not_found} NOT_FOUND")
        print(f"Total files with hand-rolled bezier: {len(results)}")
        return

    if args.demo:
        print("Bezier library available:", BEZIER_AVAILABLE)
        print("Shapely available:", SHAPELY_AVAILABLE)
        print()

        # Demo: quadratic bezier
        p0, p1, p2 = (0, 0), (50, 100), (100, 0)
        pts = quadratic_bezier_pts(p0, p1, p2, steps=10)
        print(f"Quadratic bezier ({p0} -> {p1} -> {p2}), 11 points:")
        print(f"  First: {pts[0]}, Mid: {pts[5]}, Last: {pts[-1]}")

        # Demo: cubic bezier
        p0, p1, p2, p3 = (0, 0), (30, 100), (70, 100), (100, 0)
        pts = cubic_bezier_pts(p0, p1, p2, p3, steps=10)
        print(f"Cubic bezier, 11 points:")
        print(f"  First: {pts[0]}, Mid: {pts[5]}, Last: {pts[-1]}")

        if BEZIER_AVAILABLE:
            cp = [(0, 0), (30, 100), (70, 100), (100, 0)]
            length = arc_length(cp)
            print(f"Arc length: {length:.2f}px")

            curv = curvature_at_t(cp, 0.5)
            print(f"Curvature at t=0.5: {curv:.6f}")

            t_vals = uniform_t_by_arclength(cp, 5)
            print(f"Arc-length uniform t: {[f'{t:.3f}' for t in t_vals]}")

        if SHAPELY_AVAILABLE:
            print("\nShapely polygon demo:")
            from shapely.geometry import Polygon
            p1 = Polygon([(0, 0), (100, 0), (100, 100), (0, 100)])
            p2 = Polygon([(50, 0), (150, 0), (150, 100), (50, 100)])
            sor = polygon_overlap_ratio(p1, p2)
            iou = polygon_iou(p1, p2)
            print(f"  SOR: {sor:.3f}, IoU: {iou:.3f}")

        return

    parser.print_help()


if __name__ == "__main__":
    _cli()
