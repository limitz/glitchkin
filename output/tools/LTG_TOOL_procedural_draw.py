# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_procedural_draw.py — Procedural Drawing Library
"Luma & the Glitchkin" — Procedural Art Engineering / Rin Yamamoto / Cycle 26

Provides hand-drawn stylization functions for PIL-based generators.
Adapted from artistry project techniques (Zeno Particelli AI artist):
  - Wobble paths: organic non-straight lines via sin-based perpendicular displacement
  - Variable stroke weight: taper from endpoints to midpoint using circle chain
  - Silhouette-first methodology: quality gate — always verify silhouette reads first
  - Rim lights: thin bright edge on character silhouettes
  - Value study / silhouette test: QA diagnostic tools
  - Volumetric face lighting: split-light with brow, nose-on-cheek, and chin shadows (C27)
  - Character bbox: auto-compute character center x from silhouette for rim-light use (C33)
  - Scene snapshot: crop a named region from a scene image and save as labelled diagnostic PNG (C34)

C39 Audit Notes:
  - get_char_bbox() confirmed present and correct (added C33, v1.4.0).
  - SF02 v008 audit: uses char_cx from geometry constants (NOT get_char_bbox on full frame) — CORRECT.
    Note: get_char_bbox() on a multi-character frame returns a bbox spanning all characters.
    Always pass per-character cx from geometry constants when the frame has multiple characters.
  - SF03 v005 audit: does NOT call add_rim_light() — no canvas-midpoint bug risk — CLEAN.
  - No latent head_cx bugs found in latest generator versions.

Library design:
  - All drawing functions accept seeded RNG for reproducibility
  - No cairocffi — 100% PIL/Pillow
  - Compatible with Kai Nakamura's LTG_TOOL_render_qa.py:
      silhouette_test(img, threshold=128) -> PIL.Image
      value_study(img) -> PIL.Image

Import:
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from LTG_TOOL_procedural_draw import (
        wobble_line, wobble_polygon, variable_stroke,
        add_rim_light, silhouette_test, value_study,
        get_char_bbox, scene_snapshot
    )

CLI demo:
    python output/tools/LTG_TOOL_procedural_draw.py

Dependencies: Python 3.8+, Pillow (PIL). No NumPy required.
"""

__version__ = "1.6.0"
__author__ = "Rin Yamamoto"
__cycle__ = 26  # library created; updated C27–C39

import math
import random
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _perpendicular_unit(dx: float, dy: float):
    """Return a unit vector perpendicular to (dx, dy)."""
    length = math.hypot(dx, dy)
    if length < 1e-9:
        return (0.0, 0.0)
    return (-dy / length, dx / length)


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def wobble_line(draw, p1, p2, color=(0, 0, 0), width=2,
                amplitude=2.0, frequency=8, seed=42):
    """Draw a slightly wobbly line between p1 and p2.

    Uses sin-based displacement perpendicular to the line direction to create
    an organic, hand-drawn feel. Draws as a series of short straight segments
    with slight perpendicular offset applied at each sample point.

    Args:
        draw      (ImageDraw.Draw): Active draw context.
        p1        (tuple): Start point (x, y).
        p2        (tuple): End point (x, y).
        color     (tuple): RGB or RGBA color for the line.
        width     (int)  : Line width in pixels.
        amplitude (float): Max perpendicular displacement in pixels.
        frequency (int)  : Number of wobble cycles along the full line length.
        seed      (int)  : Random seed for wobble phase offset.
    """
    rng = random.Random(seed)
    phase = rng.uniform(0, 2 * math.pi)

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    length = math.hypot(dx, dy)
    if length < 1e-9:
        return

    px, py = _perpendicular_unit(dx, dy)

    # Number of segments — at least 2 per wobble cycle, minimum 4 total
    num_segments = max(4, int(frequency * 4))
    steps = num_segments + 1

    pts = []
    for i in range(steps):
        t = i / num_segments
        # Position along the line
        x = p1[0] + t * dx
        y = p1[1] + t * dy
        # Perpendicular displacement: sin wave + small random jitter
        wobble = amplitude * math.sin(t * frequency * 2 * math.pi + phase)
        jitter = rng.uniform(-amplitude * 0.2, amplitude * 0.2)
        offset = wobble + jitter
        pts.append((x + px * offset, y + py * offset))

    # Draw as connected polyline segments
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=color, width=width)


def wobble_polygon(draw, points, color=(0, 0, 0), width=2,
                   amplitude=2.0, frequency=6, seed=42, fill=None):
    """Draw a closed polygon with wobbly outline.

    Applies wobble_line to each edge of the polygon in sequence.
    If fill is specified, the polygon interior is filled first (flat), then
    the wobble outline is drawn on top.

    Args:
        draw      (ImageDraw.Draw): Active draw context.
        points    (list)  : List of (x, y) vertex tuples.
        color     (tuple) : RGB or RGBA outline color.
        width     (int)   : Outline width in pixels.
        amplitude (float) : Max perpendicular wobble displacement.
        frequency (int)   : Wobble cycles per edge.
        seed      (int)   : Base random seed (incremented per edge for variety).
        fill      (tuple) : Optional RGB fill color for the polygon interior.
    """
    if len(points) < 2:
        return

    # Fill interior first if requested
    if fill is not None:
        draw.polygon(points, fill=fill)

    # Draw each edge with wobble, varying seed per edge
    n = len(points)
    for i in range(n):
        p1 = points[i]
        p2 = points[(i + 1) % n]
        edge_seed = seed + i * 137  # deterministic but varied per edge
        wobble_line(draw, p1, p2, color=color, width=width,
                    amplitude=amplitude, frequency=frequency, seed=edge_seed)


def variable_stroke(img, p1, p2, max_width=6, min_width=1,
                    color=(0, 0, 0), seed=42):
    """Draw a variable-width stroke between p1 and p2.

    Tapers from min_width at endpoints to max_width near the midpoint,
    simulating brush pressure variation. Implemented by drawing a chain of
    filled circles along the path at varying radii.

    IMPORTANT: This function modifies 'img' in place. After calling this,
    refresh your draw context: draw = ImageDraw.Draw(img)

    Args:
        img       (PIL.Image): The image to draw on (modified in place).
        p1        (tuple): Start point (x, y).
        p2        (tuple): End point (x, y).
        max_width (int)  : Maximum stroke width at the midpoint, in pixels.
        min_width (int)  : Minimum stroke width at endpoints, in pixels.
        color     (tuple): RGB color for the stroke.
        seed      (int)  : Random seed for slight width jitter.

    Returns:
        PIL.Image: The modified image (same object as img).
    """
    rng = random.Random(seed)
    draw = ImageDraw.Draw(img)

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    length = math.hypot(dx, dy)
    if length < 1e-9:
        return img

    # Enough steps for smooth result — at least 1 circle per pixel of length
    num_steps = max(8, int(length))

    for i in range(num_steps + 1):
        t = i / num_steps
        x = p1[0] + t * dx
        y = p1[1] + t * dy

        # Taper profile: parabolic — widest at midpoint, narrow at ends
        # Uses a smoothstep-style envelope: 4*t*(1-t) peaks at 1.0 when t=0.5
        envelope = 4.0 * t * (1.0 - t)  # range [0, 1]
        radius_f = min_width / 2.0 + (max_width / 2.0 - min_width / 2.0) * envelope
        # Add tiny random jitter for organic feel (±10% of current radius)
        jitter = rng.uniform(-0.1, 0.1) * radius_f
        radius = max(0.5, radius_f + jitter)

        r = int(round(radius))
        bbox = [int(x - r), int(y - r), int(x + r), int(y + r)]
        draw.ellipse(bbox, fill=color)

    return img


def add_rim_light(img, threshold=200, light_color=(255, 240, 200), width=3,
                  side="all", char_cx=None):
    """Add a rim light edge on the bright / character areas of the image.

    Finds the edges of bright regions (where pixel luminance > threshold) and
    paints a thin highlight along those edges. Simulates the 3/4-back lighting
    rim that separates characters from dark backgrounds.

    IMPORTANT: This function modifies 'img' in place. After calling this,
    refresh your draw context: draw = ImageDraw.Draw(img)

    Args:
        img         (PIL.Image): The image to modify (RGB mode recommended).
        threshold   (int)      : Luminance cutoff for 'bright' region detection (0–255).
        light_color (tuple)    : RGB color of the rim light highlight.
        width       (int)      : Rim light width in pixels (via edge dilation).
        side        (str)      : Spatial filter for rim light direction:
                                   "all"    — apply to all bright edges (backward compat default)
                                   "right"  — right side of character center only
                                   "left"   — left side of character center only
                                   "top"    — top half of canvas only   (y < height*0.5)
                                   "bottom" — bottom half of canvas only (y > height*0.5)
                                 This is a practical spatial approximation that correctly prevents
                                 the rim appearing on the wrong side without full normal-map analysis.
        char_cx     (int|None) : Character center x in pixels. When provided, "right"/"left"
                                 side masks are character-relative (x > char_cx or x < char_cx)
                                 rather than canvas-relative. This is essential for characters
                                 positioned left-of-center (e.g. Luma at ~x=0.35W in SF01) whose
                                 right torso/arm would otherwise be excluded by the 0.50W cutoff.
                                 Default None: falls back to canvas center (0.50W) for backwards
                                 compatibility.

    Returns:
        PIL.Image: The modified image (same object as img).
    """
    # Convert to grayscale for edge detection
    gray = img.convert("L")

    # Threshold to isolate bright regions
    bright_mask = gray.point(lambda p: 255 if p >= threshold else 0, mode="L")

    # Detect the edge of the bright region by comparing original with dilated version
    # Edge pixels = in dilated bright but not in original bright
    dilated = bright_mask.filter(ImageFilter.MaxFilter(size=width * 2 + 1))
    edge_mask = ImageChops.subtract(dilated, bright_mask)

    # Apply spatial mask to restrict rim to the specified side
    if side != "all":
        w, h = img.size
        spatial_mask = Image.new("L", (w, h), 0)
        if side == "right":
            # Use char_cx if provided; otherwise fall back to canvas center
            cx_split = char_cx if char_cx is not None else w // 2
            spatial_mask.paste(255, (cx_split, 0, w, h))
        elif side == "left":
            # Use char_cx if provided; otherwise fall back to canvas center
            cx_split = char_cx if char_cx is not None else w // 2
            spatial_mask.paste(255, (0, 0, cx_split, h))
        elif side == "top":
            # Only pixels in the top half
            spatial_mask.paste(255, (0, 0, w, h // 2))
        elif side == "bottom":
            # Only pixels in the bottom half
            spatial_mask.paste(255, (0, h // 2, w, h))
        # Multiply edge_mask by spatial_mask (keep only edge pixels in the specified region)
        edge_mask = ImageChops.multiply(edge_mask, spatial_mask)

    # Build rim layer: use edge_mask directly as alpha.
    # NOTE: do NOT use edge_mask.convert("RGBA") — converting L→RGBA sets alpha=255 everywhere,
    # which would flood the entire canvas with the rim color. Use edge_mask as-is for alpha.
    w_img, h_img = img.size
    rim_r = Image.new("L", (w_img, h_img), light_color[0])
    rim_g = Image.new("L", (w_img, h_img), light_color[1])
    rim_b = Image.new("L", (w_img, h_img), light_color[2])

    rim_layer = Image.merge("RGBA", (rim_r, rim_g, rim_b, edge_mask))

    # Composite rim layer over original
    base_rgba = img.convert("RGBA")
    composited = Image.alpha_composite(base_rgba, rim_layer)
    result = composited.convert(img.mode)

    # Write result into img in-place
    img.paste(result)
    return img


def silhouette_test(img, threshold=128):
    """Return a pure B&W silhouette of the image for squint-testing.

    Converts to grayscale and thresholds: pixels brighter than 'threshold'
    become white, others black. Use this to verify that the character or
    composition reads as a clear shape.

    Compatible with Kai Nakamura's LTG_TOOL_render_qa.py interface.

    Args:
        img       (PIL.Image): Input image (any mode; converted internally).
        threshold (int)      : Luminance cutoff (0–255). Default 128.

    Returns:
        PIL.Image: RGB image — pure black and white silhouette.
    """
    gray = img.convert("L")
    binary = gray.point(lambda p: 255 if p >= threshold else 0, mode="L")
    return binary.convert("RGB")


def get_char_bbox(img, threshold=128):
    """Return the bounding box and center of the character silhouette.

    Detects all pixels brighter than 'threshold' in grayscale and returns
    the axis-aligned bounding box of that bright region, plus its centre x/y.
    Designed to auto-compute char_cx for add_rim_light() without the caller
    needing to manually track the character's head centre through the draw loop.

    Usage pattern:
        add_rim_light(img, side="right", char_cx=get_char_bbox(img)[0])

    Args:
        img       (PIL.Image): Input image (any mode; converted internally).
        threshold (int)      : Luminance cutoff (0–255). Default 128.
                               Use a higher value (e.g. 180) to isolate only
                               the bright character against a dark background.

    Returns:
        tuple: (cx, cy, left, top, right, bottom) where:
            cx     (int)  : Horizontal centre of the bright-pixel bounding box.
            cy     (int)  : Vertical centre of the bright-pixel bounding box.
            left   (int)  : Leftmost bright column.
            top    (int)  : Topmost bright row.
            right  (int)  : Rightmost bright column.
            bottom (int)  : Bottommost bright row.

        Returns (w//2, h//2, 0, 0, w-1, h-1) — canvas centre — if no bright
        pixels are found, so the caller always gets a usable fallback.

    Notes:
        - Caller accesses char_cx as result[0], char_cy as result[1].
        - For characters against mid-tone backgrounds, raise threshold toward 180.
        - Modifies nothing — pure inspection, no side effects.
    """
    w, h = img.size
    gray = img.convert("L")

    # Collect all pixel positions above threshold
    pixels = gray.load()
    min_x, min_y = w, h
    max_x, max_y = -1, -1

    for y in range(h):
        for x in range(w):
            if pixels[x, y] >= threshold:
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y

    # Fallback: no bright pixels found — return canvas centre
    if max_x < 0:
        return (w // 2, h // 2, 0, 0, w - 1, h - 1)

    cx = (min_x + max_x) // 2
    cy = (min_y + max_y) // 2
    return (cx, cy, min_x, min_y, max_x, max_y)


def value_study(img):
    """Return a grayscale value study with stretched contrast.

    Converts the image to grayscale and performs histogram stretching so that
    the darkest pixel maps to 0 and the brightest maps to 255. Reveals the
    full range of values and makes dark-on-dark or light-on-light problems
    visible at a glance.

    Compatible with Kai Nakamura's LTG_TOOL_render_qa.py interface.

    Args:
        img (PIL.Image): Input image (any mode; converted internally).

    Returns:
        PIL.Image: RGB image — grayscale value study with stretched contrast.
    """
    gray = img.convert("L")
    pixels = list(gray.getdata())

    if not pixels:
        return gray.convert("RGB")

    min_val = min(pixels)
    max_val = max(pixels)

    if max_val == min_val:
        # Flat image — return mid-gray
        return gray.convert("RGB")

    scale = 255.0 / (max_val - min_val)
    stretched = gray.point(lambda p: int((p - min_val) * scale))
    return stretched.convert("RGB")


def scene_snapshot(img, region, label, out_dir):
    """Crop a named region from a scene image and save as a labelled diagnostic PNG.

    Purpose: lets any team member produce a targeted close-up crop for review
    without sending a full-resolution image to Claude. Crops are always saved at
    ≤1280×1280px (image-size rule), labelled with the region name, and grouped
    in a dedicated diagnostic directory.

    The label is drawn as a banner at the bottom of the crop (dark bar + white
    text) so the file is self-annotating when opened.

    Args:
        img     (PIL.Image) : The full scene image to crop from (not modified).
        region  (tuple)     : Crop box (left, top, right, bottom) in pixels.
                              Values are clamped to the image bounds automatically.
        label   (str)       : Short descriptive name, e.g. "luma_face_c34".
                              Used in the output filename and the annotation banner.
        out_dir (str)       : Directory path where the crop PNG is saved.
                              Directory is created if it does not exist.

    Returns:
        str: Absolute path of the saved PNG.

    Output filename format:
        <out_dir>/LTG_SNAP_<label>.png

    Usage example:
        from LTG_TOOL_procedural_draw import scene_snapshot
        snap_path = scene_snapshot(
            img,
            region=(300, 120, 680, 460),
            label="luma_face_sf02_v006",
            out_dir="output/production/snapshots"
        )
        # -> saves output/production/snapshots/LTG_SNAP_luma_face_sf02_v006.png

    Notes:
        - Output PNG is always ≤1280×1280px (thumbnail applied if crop exceeds limit).
        - The label banner height is approximately 5% of the crop height, min 18px.
        - The function never modifies the source image — a fresh copy is cropped.
        - If out_dir is a relative path it is treated relative to the current working
          directory at call time. Prefer absolute paths for pipeline scripts.
    """
    w, h = img.size
    left, top, right, bottom = region

    # Clamp crop box to image bounds
    left   = max(0, min(left,   w - 1))
    top    = max(0, min(top,    h - 1))
    right  = max(left + 1, min(right,  w))
    bottom = max(top  + 1, min(bottom, h))

    # Crop (copy — does not modify source)
    crop = img.crop((left, top, right, bottom))

    # Enforce ≤1280×1280px hard limit
    crop.thumbnail((1280, 1280), Image.LANCZOS)

    cw, ch = crop.size

    # --- Annotation banner ---
    banner_h = max(18, int(ch * 0.05))
    annotated = Image.new("RGB", (cw, ch + banner_h), (0, 0, 0))
    annotated.paste(crop, (0, 0))

    # Write label text in the banner
    draw = ImageDraw.Draw(annotated)
    # Simple small text — no external font needed; PIL default font
    text_x = 4
    text_y = ch + (banner_h - 10) // 2
    draw.text((text_x, text_y), label, fill=(255, 255, 255))

    # Clamp annotated image to ≤1280px (banner may push height over)
    annotated.thumbnail((1280, 1280), Image.LANCZOS)

    # Save
    os.makedirs(out_dir, exist_ok=True)
    # Sanitise label for filename: replace spaces/slashes with underscores
    safe_label = label.replace(" ", "_").replace("/", "_").replace("\\", "_")
    out_path = os.path.join(out_dir, f"LTG_SNAP_{safe_label}.png")
    annotated.save(out_path, "PNG")

    return os.path.abspath(out_path)


def add_face_lighting(img, face_center, face_radius, light_dir,
                      shadow_color, highlight_color, seed=42):
    """Apply volumetric split-light to a face area.

    Simulates three-point anatomical shadow casting on a cartoon face:
      1. Brow shadow — dark crescent on the brow ridge opposite the light
      2. Nose-on-cheek shadow — soft wedge cast from the nose onto the lit cheek
      3. Chin-on-neck shadow — gradient band along the lower jaw/neck boundary

    IMPORTANT: This function modifies 'img' in place. After calling this,
    refresh your draw context: draw = ImageDraw.Draw(img)

    Args:
        img             (PIL.Image): The image to modify (RGB mode).
        face_center     (tuple)    : (cx, cy) — centre of the face ellipse in pixels.
        face_radius     (tuple)    : (rx, ry) — horizontal/vertical radii of the face.
        light_dir       (tuple)    : (dx, dy) normalised — direction light comes FROM.
                                     e.g. (-1, -1) = upper-left source.
        shadow_color    (tuple)    : RGB of the shadow (typically warm-dark or cool-dark).
        highlight_color (tuple)    : RGB of the lit surface accent (warm or cool).
        seed            (int)      : Random seed — ensures reproducible wobble.

    Returns:
        PIL.Image: The modified image (same object as img).

    Technique notes (adapted from artistry/tools/render_engine.py Cairo approach):
      - Cairo used radial/linear gradient fills on path masks.
      - PIL equivalent: RGBA layer composited with alpha gradient baked per-pixel.
      - Anatomical positions derived from face_center + face_radius ratios:
          brow_y  ≈ face_center_y − 0.25 * ry
          nose_y  ≈ face_center_y + 0.10 * ry
          chin_y  ≈ face_center_y + 0.70 * ry
      - All shadow/highlight layers are soft-edged ellipses with feathering
        proportional to face_radius, ensuring they scale with the character.
      - Wobble paths (via wobble_line) give shadow edges organic imperfection.
    """
    rng = random.Random(seed)

    cx, cy = face_center
    rx, ry = face_radius

    # Normalise light direction
    ldx, ldy = light_dir
    llen = math.hypot(ldx, ldy)
    if llen < 1e-9:
        ldx, ldy = -1.0, -1.0
        llen = math.sqrt(2)
    ldx /= llen
    ldy /= llen

    # Shadow direction is opposite to light
    sdx, sdy = -ldx, -ldy

    w, h = img.size

    # Helper: clamp to image bounds
    def clamp_pt(x, y):
        return (max(0, min(w - 1, int(x))), max(0, min(h - 1, int(y))))

    # -----------------------------------------------------------------------
    # Layer 1 — Brow shadow
    # A soft dark ellipse on the brow ridge, shifted toward shadow side.
    # Anatomical position: upper third of face, displaced along shadow direction.
    # -----------------------------------------------------------------------
    brow_cx = cx + sdx * rx * 0.30
    brow_cy = cy - ry * 0.25 + sdy * ry * 0.10
    brow_rx = rx * 0.55
    brow_ry = ry * 0.18

    # Build a soft shadow layer (RGBA) for the brow
    brow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    brow_draw = ImageDraw.Draw(brow_layer)

    # Draw feathered ellipse by stacking concentric ellipses with decreasing alpha
    feather_steps = 8
    for step in range(feather_steps, 0, -1):
        t = step / feather_steps          # 1.0 at core, 1/feather_steps at edge
        alpha = int(90 * (t ** 1.5))     # non-linear falloff — stronger at core
        # Slight wobble per step for organic edge
        jitter_x = rng.uniform(-rx * 0.02, rx * 0.02)
        jitter_y = rng.uniform(-ry * 0.02, ry * 0.02)
        ex = brow_rx * (1.0 + (1 - t) * 0.4)
        ey = brow_ry * (1.0 + (1 - t) * 0.4)
        bbox = [
            int(brow_cx - ex + jitter_x), int(brow_cy - ey + jitter_y),
            int(brow_cx + ex + jitter_x), int(brow_cy + ey + jitter_y),
        ]
        brow_draw.ellipse(bbox, fill=(*shadow_color, alpha))

    # Composite brow shadow onto image
    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, brow_layer)
    img.paste(base_rgba.convert(img.mode))

    # -----------------------------------------------------------------------
    # Layer 2 — Nose-on-cheek shadow
    # A triangular/wedge soft shadow cast from the nose onto the lit cheek.
    # Positioned at mid-face, offset toward the shadow side (opposite light).
    # -----------------------------------------------------------------------
    nose_cx = cx + sdx * rx * 0.22
    nose_cy = cy + ry * 0.10
    nose_rx = rx * 0.28
    nose_ry = ry * 0.22

    nose_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    nose_draw = ImageDraw.Draw(nose_layer)

    feather_steps = 7
    for step in range(feather_steps, 0, -1):
        t = step / feather_steps
        alpha = int(75 * (t ** 1.8))
        jitter_x = rng.uniform(-rx * 0.015, rx * 0.015)
        jitter_y = rng.uniform(-ry * 0.015, ry * 0.015)
        ex = nose_rx * (1.0 + (1 - t) * 0.5)
        ey = nose_ry * (1.0 + (1 - t) * 0.5)
        bbox = [
            int(nose_cx - ex + jitter_x), int(nose_cy - ey + jitter_y),
            int(nose_cx + ex + jitter_x), int(nose_cy + ey + jitter_y),
        ]
        nose_draw.ellipse(bbox, fill=(*shadow_color, alpha))

    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, nose_layer)
    img.paste(base_rgba.convert(img.mode))

    # -----------------------------------------------------------------------
    # Layer 3 — Chin-on-neck shadow
    # A wide, low-contrast gradient band along the chin/jaw underside.
    # Anatomical position: lower face at chin_y ≈ cy + 0.70 * ry.
    # -----------------------------------------------------------------------
    chin_y = cy + ry * 0.70
    chin_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    chin_draw = ImageDraw.Draw(chin_layer)

    feather_steps = 6
    for step in range(feather_steps, 0, -1):
        t = step / feather_steps
        alpha = int(60 * (t ** 2.0))
        jitter_x = rng.uniform(-rx * 0.01, rx * 0.01)
        jitter_y = rng.uniform(-ry * 0.01, ry * 0.01)
        ex = rx * 0.65 * (1.0 + (1 - t) * 0.35)
        ey = ry * 0.12 * (1.0 + (1 - t) * 0.35)
        bbox = [
            int(cx - ex + jitter_x), int(chin_y - ey + jitter_y),
            int(cx + ex + jitter_x), int(chin_y + ey + jitter_y),
        ]
        chin_draw.ellipse(bbox, fill=(*shadow_color, alpha))

    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, chin_layer)
    img.paste(base_rgba.convert(img.mode))

    # -----------------------------------------------------------------------
    # Layer 4 — Highlight accent on lit side
    # A soft bright ellipse on the cheekbone/forehead on the lit side.
    # -----------------------------------------------------------------------
    hi_cx = cx + ldx * rx * 0.32
    hi_cy = cy - ry * 0.20 + ldy * ry * 0.05
    hi_rx = rx * 0.28
    hi_ry = ry * 0.22

    hi_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    hi_draw = ImageDraw.Draw(hi_layer)

    feather_steps = 7
    for step in range(feather_steps, 0, -1):
        t = step / feather_steps
        alpha = int(55 * (t ** 1.5))
        jitter_x = rng.uniform(-rx * 0.015, rx * 0.015)
        jitter_y = rng.uniform(-ry * 0.015, ry * 0.015)
        ex = hi_rx * (1.0 + (1 - t) * 0.4)
        ey = hi_ry * (1.0 + (1 - t) * 0.4)
        bbox = [
            int(hi_cx - ex + jitter_x), int(hi_cy - ey + jitter_y),
            int(hi_cx + ex + jitter_x), int(hi_cy + ey + jitter_y),
        ]
        hi_draw.ellipse(bbox, fill=(*highlight_color, alpha))

    base_rgba = img.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, hi_layer)
    img.paste(base_rgba.convert(img.mode))

    # -----------------------------------------------------------------------
    # Organic edge detail — wobble lines tracing brow / chin shadow boundaries
    # -----------------------------------------------------------------------
    draw = ImageDraw.Draw(img)

    # Brow shadow lower edge — dark organic line under brow ridge
    brow_edge_y = brow_cy + brow_ry * 0.6
    wobble_line(
        draw,
        (brow_cx - brow_rx * 0.9, brow_edge_y),
        (brow_cx + brow_rx * 0.9, brow_edge_y),
        color=(*shadow_color[:3],),
        width=1,
        amplitude=brow_ry * 0.35,
        frequency=4,
        seed=seed + 1,
    )

    # Chin shadow upper edge — subtle line along jaw underside
    chin_edge_y = chin_y - ry * 0.07
    chin_edge_alpha_color = tuple(
        int(c * 0.55) for c in shadow_color[:3]
    )
    wobble_line(
        draw,
        (cx - rx * 0.55, chin_edge_y),
        (cx + rx * 0.55, chin_edge_y),
        color=chin_edge_alpha_color,
        width=1,
        amplitude=ry * 0.04,
        frequency=3,
        seed=seed + 2,
    )

    return img


# ---------------------------------------------------------------------------
# Demo / test harness
# ---------------------------------------------------------------------------

def _build_test_image(out_path: str, size: int = 600):
    """Build a demonstration image exercising all six API functions.

    Layout (600×600):
      Top-left quadrant  : wobble_polygon oval silhouette (character blob)
      Top-right quadrant : variable_stroke line (tapered brush stroke)
      Bottom-left        : silhouette_test of the character blob
      Bottom-right       : value_study of the character blob
      Rim light          : applied to the top-left quadrant after drawing

    Args:
        out_path (str): Where to save the PNG.
        size     (int): Canvas size in pixels (square). Default 600.
    """
    q = size // 2  # quadrant size
    margin = 20

    # ------------------------------------------------------------------
    # 1. Build the full canvas
    # ------------------------------------------------------------------
    canvas = Image.new("RGB", (size, size), (245, 242, 235))
    draw = ImageDraw.Draw(canvas)

    # ------------------------------------------------------------------
    # 2. Top-left: wobble_polygon character-blob silhouette
    # ------------------------------------------------------------------
    # Build an oval-ish polygon approximating a cartoon character head blob
    cx, cy = q // 2, q // 2
    rx, ry = q // 2 - margin, q // 2 - margin - 10

    num_pts = 18
    blob_pts = []
    for i in range(num_pts):
        angle = (2 * math.pi * i / num_pts) - math.pi / 2
        # Slight squash-and-stretch: wider at ears, slightly pointed at crown
        r_mod = 1.0 + 0.08 * math.cos(2 * angle) + 0.05 * math.sin(3 * angle)
        bx = cx + rx * r_mod * math.cos(angle)
        by = cy + ry * r_mod * math.sin(angle)
        blob_pts.append((bx, by))

    # Draw filled blob first, then wobble outline
    wobble_polygon(draw, blob_pts,
                   color=(30, 20, 15), width=3,
                   amplitude=3.0, frequency=5, seed=7,
                   fill=(210, 185, 155))

    # Simple face features using wobble_line
    # Eyes
    eye_y = cy - ry * 0.15
    eye_lx = cx - rx * 0.28
    eye_rx = cx + rx * 0.28
    eye_r = rx * 0.12
    # Left eye
    eye_l_pts = [(eye_lx + eye_r * math.cos(a * math.pi / 4),
                  eye_y + eye_r * 0.6 * math.sin(a * math.pi / 4))
                 for a in range(9)]
    for j in range(len(eye_l_pts) - 1):
        wobble_line(draw, eye_l_pts[j], eye_l_pts[j + 1],
                    color=(30, 20, 15), width=2, amplitude=1.0, frequency=3, seed=11 + j)
    # Right eye (mirror)
    eye_r_pts = [(eye_rx + eye_r * math.cos(a * math.pi / 4),
                  eye_y + eye_r * 0.6 * math.sin(a * math.pi / 4))
                 for a in range(9)]
    for j in range(len(eye_r_pts) - 1):
        wobble_line(draw, eye_r_pts[j], eye_r_pts[j + 1],
                    color=(30, 20, 15), width=2, amplitude=1.0, frequency=3, seed=23 + j)

    # Nose shadow — short diagonal wobble line under nose bridge
    wobble_line(draw,
                (cx - rx * 0.07, cy + ry * 0.08),
                (cx + rx * 0.07, cy + ry * 0.18),
                color=(160, 120, 90), width=2, amplitude=1.5, frequency=3, seed=31)

    # Brow shadow — slightly curved line above each eye
    wobble_line(draw,
                (eye_lx - eye_r, eye_y - eye_r * 0.9),
                (eye_lx + eye_r, eye_y - eye_r * 0.7),
                color=(80, 55, 40), width=2, amplitude=1.0, frequency=4, seed=41)
    wobble_line(draw,
                (eye_rx - eye_r, eye_y - eye_r * 0.7),
                (eye_rx + eye_r, eye_y - eye_r * 0.9),
                color=(80, 55, 40), width=2, amplitude=1.0, frequency=4, seed=51)

    # Chin shadow — gentle curved line along jaw
    chin_y = cy + ry * 0.7
    wobble_line(draw,
                (cx - rx * 0.4, chin_y - 5),
                (cx + rx * 0.4, chin_y - 5),
                color=(160, 120, 90), width=2, amplitude=2.0, frequency=3, seed=61)

    # Rim light on the character blob
    # Extract the top-left quadrant, apply rim light, paste back
    tl_quad = canvas.crop((0, 0, q, q))
    add_rim_light(tl_quad, threshold=190, light_color=(255, 248, 210), width=2)
    canvas.paste(tl_quad, (0, 0))
    draw = ImageDraw.Draw(canvas)  # Refresh after paste

    # Quadrant label
    draw.rectangle([(0, q - 22), (q, q)], fill=(245, 242, 235))
    draw.text((margin // 2, q - 18), "wobble_polygon + rim_light", fill=(60, 60, 60))

    # ------------------------------------------------------------------
    # 3. Top-right: variable_stroke demonstration
    # ------------------------------------------------------------------
    # Background for this quadrant
    draw.rectangle([(q, 0), (size, q)], fill=(230, 225, 215))
    draw = ImageDraw.Draw(canvas)

    # Draw several variable_stroke lines showing taper variety
    strokes = [
        # (p1, p2, max_width, min_width, color, seed)
        ((q + margin, margin + 10), (size - margin, margin + 10), 8, 1, (30, 20, 15), 10),
        ((q + margin, margin + 40), (size - margin, margin + 40), 6, 1, (80, 55, 40), 20),
        ((q + margin, margin + 70), (size - margin, margin + 70), 4, 1, (120, 90, 65), 30),
        ((q + margin, margin + 100), (size - margin, margin + 100), 3, 1, (160, 120, 90), 40),
        # Diagonal stroke
        ((q + margin, margin + 140), (size - margin, q - margin - 40), 7, 1, (30, 20, 15), 50),
    ]
    for p1, p2, mw, nw, col, sd in strokes:
        variable_stroke(canvas, p1, p2, max_width=mw, min_width=nw, color=col, seed=sd)
    draw = ImageDraw.Draw(canvas)  # Refresh after variable_stroke

    draw.rectangle([(q, q - 22), (size, q)], fill=(230, 225, 215))
    draw.text((q + margin // 2, q - 18), "variable_stroke (taper)", fill=(60, 60, 60))

    # ------------------------------------------------------------------
    # 4. Bottom-left: silhouette_test of the character blob
    # ------------------------------------------------------------------
    tl_quad_fresh = canvas.crop((0, 0, q, q))
    sil = silhouette_test(tl_quad_fresh, threshold=128)
    # Resize to fit quadrant exactly (it already is q×q)
    canvas.paste(sil, (0, q))
    draw = ImageDraw.Draw(canvas)  # Refresh after paste

    draw.rectangle([(0, size - 22), (q, size)], fill=(255, 255, 255))
    draw.text((margin // 2, size - 18), "silhouette_test()", fill=(60, 60, 60))

    # ------------------------------------------------------------------
    # 5. Bottom-right: value_study of the character blob
    # ------------------------------------------------------------------
    vs = value_study(tl_quad_fresh)
    canvas.paste(vs, (q, q))
    draw = ImageDraw.Draw(canvas)  # Refresh after paste

    draw.rectangle([(q, size - 22), (size, size)], fill=(255, 255, 255))
    draw.text((q + margin // 2, size - 18), "value_study()", fill=(60, 60, 60))

    # ------------------------------------------------------------------
    # 6. Grid lines dividing quadrants
    # ------------------------------------------------------------------
    draw.line([(q, 0), (q, size)], fill=(100, 100, 100), width=1)
    draw.line([(0, q), (size, q)], fill=(100, 100, 100), width=1)

    # ------------------------------------------------------------------
    # 7. Save — enforce ≤ 640px for test images
    # ------------------------------------------------------------------
    if canvas.width > 640 or canvas.height > 640:
        canvas.thumbnail((640, 640), Image.LANCZOS)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    canvas.save(out_path, "PNG")
    print(f"Saved test image: {out_path}  ({canvas.width}×{canvas.height})")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Resolve output path relative to repo root regardless of CWD
    _here = os.path.dirname(os.path.abspath(__file__))
    _out = os.path.join(_here, "test_procedural_draw.png")

    print("LTG_TOOL_procedural_draw — Demo")
    print("=" * 50)
    print("Testing all eight API functions:")
    print("  1. wobble_line       — organic wobbly line")
    print("  2. wobble_polygon    — wobbly closed shape + fill")
    print("  3. variable_stroke   — tapered brush stroke")
    print("  4. add_rim_light     — bright edge on silhouette")
    print("  5. silhouette_test   — pure B&W shape read")
    print("  6. value_study       — contrast-stretched grayscale")
    print("  7. get_char_bbox     — auto-detect character bbox / char_cx")
    print("  8. scene_snapshot    — crop labelled region to diagnostic PNG")
    print()

    _build_test_image(_out, size=600)

    # Test scene_snapshot: crop the top-left quadrant from the test image and save
    _snap_out_dir = os.path.join(_here, "snapshots")
    test_img = Image.open(_out)
    snap_path = scene_snapshot(
        test_img,
        region=(0, 0, test_img.width // 2, test_img.height // 2),
        label="test_tl_quad_procedural_draw_v001",
        out_dir=_snap_out_dir,
    )
    print(f"Saved snapshot test: {snap_path}")
    print("Done.")
