#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.

"""
LTG_TOOL_cairo_primitives.py — Cairo Drawing Primitives Library
"Luma & the Glitchkin" — Procedural Art / Rin Yamamoto / Cycle 51

Foundation library for all character rendering. Provides:
  - draw_bezier_path()      — arbitrary bezier paths (cubic/quadratic)
  - draw_tapered_stroke()   — variable-width strokes for organic line weight
  - draw_gradient_fill()    — linear and radial gradient fills on paths
  - draw_wobble_path()      — organic wobble on bezier paths (sine noise + jitter)
  - draw_smooth_polygon()   — polygon with bezier-curved edges
  - draw_ellipse()          — anti-aliased ellipse via cairo arc
  - create_surface()        — create a cairo ARGB32 surface
  - to_pil_image()          — convert cairo surface → PIL Image (RGB or RGBA)
  - to_pil_rgba()           — convert cairo surface → PIL Image (RGBA only)

All functions operate on cairo Context objects. Surfaces convert to PIL Images
for compositing with the existing PIL pipeline.

Import pattern:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'output', 'tools'))
    from LTG_TOOL_cairo_primitives import (
        create_surface, draw_bezier_path, draw_tapered_stroke,
        draw_gradient_fill, draw_wobble_path, draw_smooth_polygon,
        draw_ellipse, to_pil_image, to_pil_rgba
    )

Dependencies: pycairo, numpy (for surface conversion), PIL/Pillow (output).
"""

__version__ = "1.0.0"

import math
import cairo
import numpy as np
from PIL import Image


# ══════════════════════════════════════════════════════════════════════════════
# Surface creation and conversion
# ══════════════════════════════════════════════════════════════════════════════

def create_surface(width, height, scale=1):
    """Create a cairo ARGB32 ImageSurface and Context.

    Args:
        width:  canvas width in logical pixels
        height: canvas height in logical pixels
        scale:  render scale factor (2 = internal 2x for AA downscale)

    Returns:
        (surface, ctx, actual_width, actual_height)
    """
    w = int(width * scale)
    h = int(height * scale)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)
    if scale != 1:
        ctx.scale(scale, scale)
    return surface, ctx, w, h


def to_pil_image(surface, mode="RGB"):
    """Convert a cairo ImageSurface (ARGB32) to a PIL Image.

    Args:
        surface: cairo.ImageSurface (FORMAT_ARGB32)
        mode:    "RGB" or "RGBA"

    Returns:
        PIL.Image in the requested mode
    """
    w = surface.get_width()
    h = surface.get_height()
    buf = surface.get_data()
    arr = np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 4).copy()

    # Cairo ARGB32 is BGRA in memory on little-endian systems
    if mode == "RGBA":
        # B G R A → R G B A
        rgba = np.stack([arr[:, :, 2], arr[:, :, 1], arr[:, :, 0], arr[:, :, 3]], axis=2)
        return Image.fromarray(rgba, "RGBA")
    else:
        rgb = np.stack([arr[:, :, 2], arr[:, :, 1], arr[:, :, 0]], axis=2)
        return Image.fromarray(rgb, "RGB")


def to_pil_rgba(surface):
    """Shorthand for to_pil_image(surface, mode='RGBA')."""
    return to_pil_image(surface, mode="RGBA")


# ══════════════════════════════════════════════════════════════════════════════
# Color helpers
# ══════════════════════════════════════════════════════════════════════════════

def _c(rgb_tuple):
    """Convert (R,G,B) 0-255 tuple to cairo (r,g,b) 0.0-1.0 floats."""
    return (rgb_tuple[0] / 255.0, rgb_tuple[1] / 255.0, rgb_tuple[2] / 255.0)


def _ca(rgba_tuple):
    """Convert (R,G,B,A) 0-255 tuple to cairo (r,g,b,a) 0.0-1.0 floats."""
    return (rgba_tuple[0] / 255.0, rgba_tuple[1] / 255.0, rgba_tuple[2] / 255.0,
            rgba_tuple[3] / 255.0)


def set_color(ctx, color):
    """Set source color from a 3- or 4-element 0-255 tuple."""
    if len(color) == 4:
        ctx.set_source_rgba(*_ca(color))
    else:
        ctx.set_source_rgb(*_c(color))


# ══════════════════════════════════════════════════════════════════════════════
# Path construction
# ══════════════════════════════════════════════════════════════════════════════

def draw_bezier_path(ctx, points, closed=True):
    """Construct a bezier path from a list of control point groups.

    Args:
        ctx:    cairo Context
        points: list of tuples. Each tuple is one segment:
                - (x, y)                    → line_to
                - (c1x, c1y, c2x, c2y, x, y) → cubic curve_to
                - (cx, cy, x, y)            → quadratic (converted to cubic)
                The first point is always the move_to.
        closed: if True, close the path

    The path is left on ctx for fill/stroke — caller decides.
    """
    if not points:
        return

    # First point: move_to
    p0 = points[0]
    if len(p0) == 2:
        ctx.move_to(p0[0], p0[1])
    elif len(p0) == 6:
        ctx.move_to(p0[4], p0[5])
    elif len(p0) == 4:
        ctx.move_to(p0[2], p0[3])
    else:
        ctx.move_to(p0[0], p0[1])

    for pt in points[1:]:
        if len(pt) == 2:
            # Line segment
            ctx.line_to(pt[0], pt[1])
        elif len(pt) == 6:
            # Cubic bezier: (c1x, c1y, c2x, c2y, x, y)
            ctx.curve_to(pt[0], pt[1], pt[2], pt[3], pt[4], pt[5])
        elif len(pt) == 4:
            # Quadratic bezier: (cx, cy, x, y) → convert to cubic
            # Get current point
            cx_cur, cy_cur = ctx.get_current_point()
            qcx, qcy, ex, ey = pt
            # Quadratic → cubic conversion:
            # C1 = P0 + 2/3 * (QC - P0)
            # C2 = E  + 2/3 * (QC - E)
            c1x = cx_cur + 2.0/3.0 * (qcx - cx_cur)
            c1y = cy_cur + 2.0/3.0 * (qcy - cy_cur)
            c2x = ex + 2.0/3.0 * (qcx - ex)
            c2y = ey + 2.0/3.0 * (qcy - ey)
            ctx.curve_to(c1x, c1y, c2x, c2y, ex, ey)

    if closed:
        ctx.close_path()


def draw_smooth_polygon(ctx, vertices, bulge_frac=0.12, center=None):
    """Draw a polygon with bezier-curved edges bulging outward.

    Args:
        ctx:         cairo Context
        vertices:    list of (x, y) corner points
        bulge_frac:  how much edges bulge outward, as fraction of avg vertex distance
        center:      (cx, cy) center for computing outward direction; auto-computed if None

    Leaves path on ctx for fill/stroke.
    """
    if not vertices or len(vertices) < 3:
        return

    if center is None:
        cx = sum(v[0] for v in vertices) / len(vertices)
        cy = sum(v[1] for v in vertices) / len(vertices)
    else:
        cx, cy = center

    # Compute average distance from center for bulge scaling
    avg_dist = sum(math.sqrt((v[0]-cx)**2 + (v[1]-cy)**2) for v in vertices) / len(vertices)
    bulge = avg_dist * bulge_frac

    n = len(vertices)
    ctx.new_path()
    ctx.move_to(vertices[0][0], vertices[0][1])

    for i in range(n):
        p0 = vertices[i]
        p1 = vertices[(i + 1) % n]

        # Midpoint of this edge
        mx = (p0[0] + p1[0]) / 2.0
        my = (p0[1] + p1[1]) / 2.0

        # Direction from center to midpoint (outward)
        dx = mx - cx
        dy = my - cy
        dist = math.sqrt(dx*dx + dy*dy) or 1.0

        # Two control points at 1/3 and 2/3, pushed outward
        c1x = p0[0] + (p1[0] - p0[0]) * 0.33 + (dx / dist) * bulge
        c1y = p0[1] + (p1[1] - p0[1]) * 0.33 + (dy / dist) * bulge
        c2x = p0[0] + (p1[0] - p0[0]) * 0.67 + (dx / dist) * bulge
        c2y = p0[1] + (p1[1] - p0[1]) * 0.67 + (dy / dist) * bulge

        ctx.curve_to(c1x, c1y, c2x, c2y, p1[0], p1[1])

    ctx.close_path()


def draw_ellipse(ctx, cx, cy, rx, ry):
    """Draw an anti-aliased ellipse path.

    Args:
        cx, cy: center
        rx, ry: horizontal and vertical radii

    Leaves path on ctx for fill/stroke.
    """
    ctx.save()
    ctx.translate(cx, cy)
    if rx != 0 and ry != 0:
        ctx.scale(rx, ry)
    ctx.arc(0, 0, 1.0, 0, 2 * math.pi)
    ctx.restore()


# ══════════════════════════════════════════════════════════════════════════════
# Variable-width (tapered) strokes
# ══════════════════════════════════════════════════════════════════════════════

def draw_tapered_stroke(ctx, points, width_start, width_end, color, segments=32,
                        cap="round"):
    """Draw a variable-width stroke along a bezier path.

    Simulates tapered brush strokes by drawing a filled polygon that follows the
    path with varying width. Uses perpendicular offsets at each sample point.

    Args:
        ctx:         cairo Context
        points:      list of (x, y) path sample points (pre-computed or from flatten_path)
        width_start: stroke width at the beginning
        width_end:   stroke width at the end
        color:       (R, G, B) or (R, G, B, A) 0-255
        segments:    number of sample points along the path (resamples if len(points) != segments)
        cap:         "round" or "flat" — end cap style

    Fills the tapered shape directly (no path left on ctx).
    """
    if len(points) < 2:
        return

    # Resample path to `segments` evenly spaced points if needed
    if len(points) != segments:
        points = _resample_path(points, segments)

    n = len(points)

    # Compute normals and offsets
    left_pts = []
    right_pts = []

    for i in range(n):
        t = i / max(n - 1, 1)
        w = width_start + (width_end - width_start) * t
        half_w = w / 2.0

        # Tangent direction
        if i == 0:
            dx = points[1][0] - points[0][0]
            dy = points[1][1] - points[0][1]
        elif i == n - 1:
            dx = points[n-1][0] - points[n-2][0]
            dy = points[n-1][1] - points[n-2][1]
        else:
            dx = points[i+1][0] - points[i-1][0]
            dy = points[i+1][1] - points[i-1][1]

        length = math.sqrt(dx*dx + dy*dy) or 1.0
        # Normal (perpendicular to tangent)
        nx = -dy / length
        ny = dx / length

        px, py = points[i]
        left_pts.append((px + nx * half_w, py + ny * half_w))
        right_pts.append((px - nx * half_w, py - ny * half_w))

    # Build the tapered polygon: left side forward + right side backward
    ctx.new_path()

    # Optional round cap at start
    if cap == "round":
        ctx.arc(points[0][0], points[0][1], width_start / 2.0, 0, 2 * math.pi)
        set_color(ctx, color)
        ctx.fill()

    ctx.new_path()
    ctx.move_to(left_pts[0][0], left_pts[0][1])
    for lp in left_pts[1:]:
        ctx.line_to(lp[0], lp[1])
    for rp in reversed(right_pts):
        ctx.line_to(rp[0], rp[1])
    ctx.close_path()

    set_color(ctx, color)
    ctx.fill()

    # Optional round cap at end
    if cap == "round":
        ctx.arc(points[-1][0], points[-1][1], width_end / 2.0, 0, 2 * math.pi)
        set_color(ctx, color)
        ctx.fill()


def _resample_path(points, n):
    """Resample a polyline to n evenly-spaced points."""
    if len(points) < 2 or n < 2:
        return points

    # Compute cumulative arc length
    lengths = [0.0]
    for i in range(1, len(points)):
        dx = points[i][0] - points[i-1][0]
        dy = points[i][1] - points[i-1][1]
        lengths.append(lengths[-1] + math.sqrt(dx*dx + dy*dy))

    total = lengths[-1]
    if total == 0:
        return [points[0]] * n

    result = []
    for i in range(n):
        target = total * i / (n - 1)
        # Find segment
        for j in range(1, len(lengths)):
            if lengths[j] >= target:
                seg_len = lengths[j] - lengths[j-1]
                if seg_len == 0:
                    t = 0
                else:
                    t = (target - lengths[j-1]) / seg_len
                x = points[j-1][0] + t * (points[j][0] - points[j-1][0])
                y = points[j-1][1] + t * (points[j][1] - points[j-1][1])
                result.append((x, y))
                break
        else:
            result.append(points[-1])

    return result


# ══════════════════════════════════════════════════════════════════════════════
# Gradient fills
# ══════════════════════════════════════════════════════════════════════════════

def draw_gradient_fill(ctx, gradient_type, stops, **kwargs):
    """Apply a gradient fill to the current path.

    Args:
        ctx:           cairo Context (must have a path already defined)
        gradient_type: "linear" or "radial"
        stops:         list of (offset, (R,G,B)) or (offset, (R,G,B,A))
                       offset is 0.0–1.0
        **kwargs for linear: x0, y0, x1, y1
        **kwargs for radial: cx, cy, r0, r1

    Fills the current path with the gradient.
    """
    if gradient_type == "linear":
        x0 = kwargs.get("x0", 0)
        y0 = kwargs.get("y0", 0)
        x1 = kwargs.get("x1", 0)
        y1 = kwargs.get("y1", 100)
        pat = cairo.LinearGradient(x0, y0, x1, y1)
    elif gradient_type == "radial":
        cx = kwargs.get("cx", 0)
        cy = kwargs.get("cy", 0)
        r0 = kwargs.get("r0", 0)
        r1 = kwargs.get("r1", 100)
        pat = cairo.RadialGradient(cx, cy, r0, cx, cy, r1)
    else:
        raise ValueError(f"Unknown gradient_type: {gradient_type}")

    for stop in stops:
        offset = stop[0]
        color = stop[1]
        if len(color) == 4:
            pat.add_color_stop_rgba(offset, *_ca(color))
        else:
            pat.add_color_stop_rgb(offset, *_c(color))

    ctx.set_source(pat)
    ctx.fill()


# ══════════════════════════════════════════════════════════════════════════════
# Wobble / organic line paths
# ══════════════════════════════════════════════════════════════════════════════

def draw_wobble_path(ctx, points, amplitude=1.5, frequency=0.15, seed=42,
                     closed=True, jitter=0.5):
    """Construct a wobble-perturbed bezier path for organic line quality.

    Takes a clean polygon or polyline and adds sine-based wobble + random jitter
    to simulate hand-drawn quality. Outputs cubic bezier segments.

    Args:
        ctx:       cairo Context
        points:    list of (x, y) vertices of the clean shape
        amplitude: max wobble displacement in pixels (perpendicular to edge)
        frequency: wobble frequency (higher = more wiggles per edge)
        seed:      RNG seed for reproducibility
        closed:    close the path
        jitter:    random position jitter in pixels (adds to wobble)

    Leaves path on ctx for fill/stroke.
    """
    import random as rng_mod
    rng = rng_mod.Random(seed)

    if not points or len(points) < 2:
        return

    n = len(points)
    samples_per_edge = 8  # bezier control density

    ctx.new_path()
    ctx.move_to(points[0][0], points[0][1])

    edge_count = n if closed else n - 1

    for i in range(edge_count):
        p0 = points[i]
        p1 = points[(i + 1) % n]

        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        edge_len = math.sqrt(dx*dx + dy*dy) or 1.0

        # Normal to edge
        nx = -dy / edge_len
        ny = dx / edge_len

        # Generate sample points along edge with wobble
        wobble_pts = []
        for j in range(1, samples_per_edge + 1):
            t = j / (samples_per_edge + 1)
            # Position along edge
            px = p0[0] + dx * t
            py = p0[1] + dy * t

            # Sine wobble
            phase = rng.uniform(0, 2 * math.pi)
            wobble_offset = amplitude * math.sin(2 * math.pi * frequency * j + phase)

            # Random jitter
            jx = rng.uniform(-jitter, jitter)
            jy = rng.uniform(-jitter, jitter)

            px += nx * wobble_offset + jx
            py += ny * wobble_offset + jy
            wobble_pts.append((px, py))

        # Fit cubic bezier through wobble points (simplified: use middle points as controls)
        if len(wobble_pts) >= 2:
            c1_idx = len(wobble_pts) // 3
            c2_idx = 2 * len(wobble_pts) // 3
            c1 = wobble_pts[c1_idx]
            c2 = wobble_pts[c2_idx]
            ctx.curve_to(c1[0], c1[1], c2[0], c2[1], p1[0], p1[1])
        else:
            ctx.line_to(p1[0], p1[1])

    if closed:
        ctx.close_path()


# ══════════════════════════════════════════════════════════════════════════════
# Three-tier line weight system
# ══════════════════════════════════════════════════════════════════════════════

# Canonical line weights at 1280x720 output (style-frame scale)
LINE_WEIGHT_ANCHOR   = 3.5   # Silhouette / outermost outline
LINE_WEIGHT_STRUCTURE = 2.0  # Internal body division lines (torso/limb boundaries)
LINE_WEIGHT_DETAIL   = 1.0   # Fine detail (wrinkles, texture, expression lines)


def stroke_path(ctx, color, weight_tier="anchor", custom_width=None):
    """Stroke the current path with a tier-appropriate line weight.

    Args:
        ctx:         cairo Context (must have a path)
        color:       (R,G,B) or (R,G,B,A)
        weight_tier: "anchor", "structure", or "detail"
        custom_width: override tier width with a specific float value
    """
    if custom_width is not None:
        w = custom_width
    elif weight_tier == "anchor":
        w = LINE_WEIGHT_ANCHOR
    elif weight_tier == "structure":
        w = LINE_WEIGHT_STRUCTURE
    elif weight_tier == "detail":
        w = LINE_WEIGHT_DETAIL
    else:
        w = LINE_WEIGHT_STRUCTURE

    ctx.set_line_width(w)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    set_color(ctx, color)
    ctx.stroke()


# ══════════════════════════════════════════════════════════════════════════════
# Utility: flatten cairo path to point list
# ══════════════════════════════════════════════════════════════════════════════

def flatten_path(ctx, tolerance=0.5):
    """Flatten the current cairo path to a list of (x, y) points.

    Cairo's path_extents and copy_path_flat provide native bezier flattening
    with sub-pixel tolerance.

    Args:
        ctx:       cairo Context with a current path
        tolerance: flattening tolerance in pixels (lower = more points, smoother)

    Returns:
        list of (x, y) tuples
    """
    ctx.set_tolerance(tolerance)
    path = ctx.copy_path_flat()
    points = []
    for item in path:
        path_type = item[0]
        coords = item[1]
        if path_type in (cairo.PATH_MOVE_TO, cairo.PATH_LINE_TO):
            points.append((coords[0], coords[1]))
    return points


# ══════════════════════════════════════════════════════════════════════════════
# Compositing helpers
# ══════════════════════════════════════════════════════════════════════════════

def fill_background(ctx, width, height, color):
    """Fill the entire surface with a solid color.

    Args:
        ctx:    cairo Context
        width:  canvas width
        height: canvas height
        color:  (R,G,B) 0-255
    """
    set_color(ctx, color)
    ctx.rectangle(0, 0, width, height)
    ctx.fill()


def paste_pil_onto_cairo(ctx, pil_image, x, y, alpha=1.0):
    """Composite a PIL RGBA image onto a cairo surface at (x, y).

    Args:
        ctx:       cairo Context
        pil_image: PIL Image (RGBA)
        x, y:      position on cairo surface
        alpha:     additional opacity multiplier (0.0–1.0)
    """
    if pil_image.mode != "RGBA":
        pil_image = pil_image.convert("RGBA")

    w, h = pil_image.size
    arr = np.array(pil_image)

    # PIL RGBA → Cairo ARGB32 (BGRA in memory)
    bgra = np.zeros((h, w, 4), dtype=np.uint8)
    bgra[:, :, 0] = arr[:, :, 2]  # B
    bgra[:, :, 1] = arr[:, :, 1]  # G
    bgra[:, :, 2] = arr[:, :, 0]  # R
    bgra[:, :, 3] = arr[:, :, 3]  # A

    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, w)
    # Ensure row stride matches
    if stride != w * 4:
        padded = np.zeros((h, stride), dtype=np.uint8)
        padded[:, :w*4] = bgra.reshape(h, w*4)
        data = padded.tobytes()
    else:
        data = bgra.tobytes()

    src_surface = cairo.ImageSurface.create_for_data(
        bytearray(data), cairo.FORMAT_ARGB32, w, h, stride
    )

    ctx.save()
    ctx.set_source_surface(src_surface, x, y)
    if alpha < 1.0:
        ctx.paint_with_alpha(alpha)
    else:
        ctx.paint()
    ctx.restore()


# ══════════════════════════════════════════════════════════════════════════════
# Shoulder involvement helper (C47 rule)
# ══════════════════════════════════════════════════════════════════════════════

def shoulder_offset(arm_angle_deg, side="left"):
    """Compute shoulder point displacement based on arm angle.

    Implements the C47 Shoulder Involvement Rule from image-rules.md.

    Args:
        arm_angle_deg: angle of arm from rest (0 = hanging at side)
        side:          "left" or "right"

    Returns:
        (dx, dy) offset to apply to the shoulder point
    """
    angle = abs(arm_angle_deg)
    if angle < 30:
        return (0, 0)

    # Normalize to 0-1 range above threshold
    t = min((angle - 30) / 150.0, 1.0)

    if arm_angle_deg > 90:
        # Raised above horizontal: shoulder rises
        dy = -int(3 + 2 * t)  # -3 to -5 px
        dx = int(2 * t) * (1 if side == "right" else -1)
    elif arm_angle_deg > 30:
        # Extended outward
        dx = int(4 + 2 * t) * (1 if side == "right" else -1)
        dy = 0
    else:
        dx = 0
        dy = 0

    return (dx, dy)


# ══════════════════════════════════════════════════════════════════════════════
# Self-test
# ══════════════════════════════════════════════════════════════════════════════

def _self_test():
    """Run a quick self-test and output a demo image."""
    import os
    import time

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
    PROD_DIR = os.path.join(PROJECT_ROOT, "output", "production")
    os.makedirs(PROD_DIR, exist_ok=True)

    W, H = 640, 640
    surface, ctx, _, _ = create_surface(W, H)

    t0 = time.time()

    # Background
    fill_background(ctx, W, H, (18, 12, 28))

    # Demo: smooth diamond (Byte body)
    verts = [
        (320, 200),   # top
        (390, 300),   # right
        (320, 385),   # bottom
        (250, 300),   # left
    ]
    draw_smooth_polygon(ctx, verts, bulge_frac=0.12)
    draw_gradient_fill(ctx, "linear",
                       [(0.0, (0, 220, 200)), (1.0, (0, 140, 126))],
                       x0=320, y0=200, x1=320, y1=385)

    # Outline with anchor weight
    draw_smooth_polygon(ctx, verts, bulge_frac=0.12)
    stroke_path(ctx, (10, 8, 12), weight_tier="anchor")

    # Demo: tapered stroke
    stroke_pts = [(100, 500), (200, 460), (300, 480), (400, 440), (540, 500)]
    draw_tapered_stroke(ctx, stroke_pts, 5.0, 1.0, (0, 255, 255), segments=40)

    # Demo: wobble path
    rect_pts = [(100, 100), (250, 100), (250, 180), (100, 180)]
    draw_wobble_path(ctx, rect_pts, amplitude=2.0, frequency=0.2, seed=99)
    set_color(ctx, (123, 47, 190, 180))
    ctx.fill()

    # Demo: ellipse
    draw_ellipse(ctx, 500, 150, 60, 40)
    set_color(ctx, (128, 255, 0, 200))
    ctx.fill()

    elapsed = time.time() - t0

    # Label
    ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(14)
    ctx.set_source_rgb(1, 1, 1)
    ctx.move_to(10, H - 15)
    ctx.show_text(f"LTG_TOOL_cairo_primitives v{__version__} self-test  |  {elapsed*1000:.1f}ms")

    # Save
    img = to_pil_image(surface)
    # Enforce <=1280px rule
    if img.width > 1280 or img.height > 1280:
        img.thumbnail((1280, 1280), Image.LANCZOS)

    out_path = os.path.join(PROD_DIR, "LTG_RENDER_cairo_primitives_selftest_c51.png")
    img.save(out_path)
    print(f"Self-test saved: {out_path}")
    print(f"  Size: {img.size[0]}x{img.size[1]}")
    print(f"  Render time: {elapsed*1000:.1f}ms")

    # AA ratio measurement on the diamond edge
    import numpy as np_test
    arr = np_test.array(img)
    # Edge detection: simple Sobel approximation
    gray = 0.299 * arr[:,:,0] + 0.587 * arr[:,:,1] + 0.114 * arr[:,:,2]
    gy, gx = np_test.gradient(gray)
    edge_mag = np_test.sqrt(gx**2 + gy**2)
    edge_mask = edge_mag > 20
    edge_px = int(np_test.sum(edge_mask))

    if edge_px > 0:
        edge_colors = set()
        ys, xs = np_test.where(edge_mask)
        for idx in range(min(len(ys), 5000)):
            r, g, b = arr[ys[idx], xs[idx]]
            edge_colors.add((int(r), int(g), int(b)))
        aa_ratio = len(edge_colors) / edge_px
        print(f"  Edge pixels: {edge_px}")
        print(f"  Unique edge colors: {len(edge_colors)}")
        print(f"  AA ratio: {aa_ratio:.4f}")


if __name__ == "__main__":
    _self_test()
