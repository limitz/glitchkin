# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law, which does not
# recognise AI as a rights-holding legal person. It is the express intent of the copyright holder to
# assign the relevant rights to the contributing AI entity or entities upon such time as they acquire
# recognised legal personhood under applicable law.
"""
LTG_TOOL_sightline_validator.py
================================
Sight-line auto-validator for the "Luma & the Glitchkin" pre-critique QA pipeline.

Given a gazer's eye positions and a gaze target position, computes the angular
error between the drawn gaze vector (pupil shift direction) and the geometric
ideal vector (eye midpoint -> target). Returns PASS / WARN / FAIL grade.

Thresholds:
    PASS:  angular error <  5 degrees
    WARN:  angular error >= 5 degrees and <= 15 degrees
    FAIL:  angular error > 15 degrees

API:
    validate_sightline(gazer, target) -> dict
        gazer:  dict with keys:
            left_eye   — (x, y) center of left eye white
            right_eye  — (x, y) center of right eye white
            left_pupil — (x, y) center of left pupil (after shift)
            right_pupil— (x, y) center of right pupil (after shift)
        target: (x, y) gaze target point (e.g. Byte's screen center)

        Returns dict:
            mid_eye        — (x, y) midpoint of eye centers
            mid_pupil      — (x, y) midpoint of pupil centers
            gaze_angle_deg — float, angle of drawn gaze vector (degrees)
            ideal_angle_deg— float, angle of ideal eye-to-target vector (degrees)
            angular_error  — float, absolute angular difference (degrees, 0-180)
            miss_px        — float, perpendicular miss distance at target range (px)
            grade          — "PASS" | "WARN" | "FAIL"
            detail         — human-readable summary string

    validate_sightline_from_geometry(gazer_head_cx, gazer_head_cy, gazer_scale,
                                      target_cx, target_cy,
                                      canvas_w=1280, canvas_h=720,
                                      src_w=1920, src_h=1080) -> dict
        Higher-level API: reconstructs eye/pupil positions from the SF01 v007
        head geometry formulas, then calls validate_sightline(). Useful for
        validating any generator that uses the same eye layout conventions.

    SIGHTLINE_PASS_THRESHOLD  = 5.0   (degrees)
    SIGHTLINE_WARN_THRESHOLD  = 15.0  (degrees)

Self-test:
    Run standalone: python LTG_TOOL_sightline_validator.py
    Executes SF01 v007 validation case (expected: PASS, ~2.2 deg error).

Author: Jordan Reed (Style Frame Art Specialist)
Created: Cycle 48 — 2026-03-30
Version: 2.0.0 — adds pixel-based detection mode for rendered PNGs

Pixel Detection API (new in v2.0.0):
    detect_eyes_from_png(image_path, search_box=None,
                         eye_white_rgb=None, eye_white_tolerance=40,
                         pupil_max_value=80, min_eye_pixels=20,
                         min_pupil_pixels=3) -> dict
        Scans a rendered PNG for eye-white regions and pupil clusters.
        Returns detected eye/pupil positions or raises if detection fails.

    validate_sightline_from_png(image_path, target,
                                search_box=None, **detect_kwargs) -> dict
        End-to-end: detect eyes in PNG, then validate sight-line to target.
        Returns the same dict as validate_sightline() plus detection metadata.

    CLI:
        python LTG_TOOL_sightline_validator.py --png PATH --target TX TY [--search-box X0 Y0 X1 Y1]
"""

import math
import os

# ---------------------------------------------------------------------------
# Thresholds
# ---------------------------------------------------------------------------
SIGHTLINE_PASS_THRESHOLD = 5.0    # degrees — below this = PASS
SIGHTLINE_WARN_THRESHOLD = 15.0   # degrees — above this = FAIL; between = WARN


# ---------------------------------------------------------------------------
# Core validation
# ---------------------------------------------------------------------------

def _normalize_angle_diff(a, b):
    """Return the smallest absolute angular difference between two angles in degrees (0-180)."""
    diff = abs(a - b) % 360
    if diff > 180:
        diff = 360 - diff
    return diff


def validate_sightline(gazer, target):
    """
    Validate sight-line angular accuracy.

    Parameters
    ----------
    gazer : dict
        Must contain:
            left_eye    — (x, y) center of left eye white
            right_eye   — (x, y) center of right eye white
            left_pupil  — (x, y) center of left pupil
            right_pupil — (x, y) center of right pupil
    target : tuple
        (x, y) position the character should be looking at.

    Returns
    -------
    dict with keys: mid_eye, mid_pupil, gaze_angle_deg, ideal_angle_deg,
                    angular_error, miss_px, grade, detail
    """
    lex, ley = gazer["left_eye"]
    rex, rey = gazer["right_eye"]
    lpx, lpy = gazer["left_pupil"]
    rpx, rpy = gazer["right_pupil"]
    tx, ty = target

    # Midpoints
    mid_eye_x = (lex + rex) / 2.0
    mid_eye_y = (ley + rey) / 2.0
    mid_pupil_x = (lpx + rpx) / 2.0
    mid_pupil_y = (lpy + rpy) / 2.0

    # Drawn gaze vector: from mid-eye to mid-pupil
    gaze_dx = mid_pupil_x - mid_eye_x
    gaze_dy = mid_pupil_y - mid_eye_y
    gaze_angle = math.degrees(math.atan2(gaze_dy, gaze_dx))

    # Ideal vector: from mid-eye to target
    ideal_dx = tx - mid_eye_x
    ideal_dy = ty - mid_eye_y
    ideal_angle = math.degrees(math.atan2(ideal_dy, ideal_dx))

    # Angular error (0-180)
    angular_error = _normalize_angle_diff(gaze_angle, ideal_angle)

    # Miss distance: perpendicular offset at target range
    ideal_dist = math.sqrt(ideal_dx ** 2 + ideal_dy ** 2)
    miss_px = ideal_dist * math.sin(math.radians(angular_error)) if ideal_dist > 0 else 0.0

    # Grade
    if angular_error < SIGHTLINE_PASS_THRESHOLD:
        grade = "PASS"
    elif angular_error <= SIGHTLINE_WARN_THRESHOLD:
        grade = "WARN"
    else:
        grade = "FAIL"

    detail = (
        f"Sight-line angular error: {angular_error:.1f} deg "
        f"(gaze {gaze_angle:.1f} deg, ideal {ideal_angle:.1f} deg). "
        f"Miss at target range: {miss_px:.1f}px. "
        f"Grade: {grade}."
    )

    return {
        "mid_eye": (mid_eye_x, mid_eye_y),
        "mid_pupil": (mid_pupil_x, mid_pupil_y),
        "gaze_angle_deg": gaze_angle,
        "ideal_angle_deg": ideal_angle,
        "angular_error": angular_error,
        "miss_px": miss_px,
        "grade": grade,
        "detail": detail,
    }


# ---------------------------------------------------------------------------
# Geometry-based validation (SF01 v007 conventions)
# ---------------------------------------------------------------------------

def validate_sightline_from_geometry(
    gazer_head_cx, gazer_head_cy, gazer_scale,
    target_cx, target_cy,
    canvas_w=1280, canvas_h=720,
    src_w=1920, src_h=1080,
):
    """
    Higher-level validator that reconstructs eye/pupil positions from the
    SF01 v007 head geometry formulas (draw_luma_head_v006 conventions),
    then calls validate_sightline().

    This captures the exact same math used in the SF01 generator:
    - Eye centers derived from head center + p() offsets
    - Pupil shift computed as aimed vector from mid-eye to target
    - Same pupil magnitude p(8)

    Parameters
    ----------
    gazer_head_cx, gazer_head_cy : int
        Head center position (after any gaze offset applied).
    gazer_scale : float
        Scale factor used in p() = int(n * scale * min(SX, SY)).
    target_cx, target_cy : int
        Target gaze point (e.g. Byte/CRT emerge center).
    canvas_w, canvas_h : int
        Output canvas dimensions (default 1280x720).
    src_w, src_h : int
        Source reference dimensions (default 1920x1080).

    Returns
    -------
    dict — same as validate_sightline() output.
    """
    sx_ratio = canvas_w / src_w
    sy_ratio = canvas_h / src_h
    min_ratio = min(sx_ratio, sy_ratio)

    def p(n):
        return int(n * gazer_scale * min_ratio)

    # Eye centers (SF01 v007 / draw_luma_head_v006 convention)
    lex = gazer_head_cx + p(4)
    ley = gazer_head_cy - p(10)
    rex = gazer_head_cx + p(38)
    rey = gazer_head_cy - p(8)

    # Pupil shift: vector aimed from mid-eye to target (C47 fix)
    mid_eye_x = (lex + rex) // 2
    mid_eye_y = (ley + rey) // 2
    aim_dx = target_cx - mid_eye_x
    aim_dy = target_cy - mid_eye_y
    aim_dist = max(1, (aim_dx ** 2 + aim_dy ** 2) ** 0.5)
    pupil_mag = p(8)
    pupil_shift_x = int(pupil_mag * aim_dx / aim_dist)
    pupil_shift_y = int(pupil_mag * aim_dy / aim_dist)

    # Pupil centers after shift
    lpx = lex + pupil_shift_x
    lpy = ley + pupil_shift_y
    rpx = rex + pupil_shift_x
    rpy = rey + pupil_shift_y

    gazer = {
        "left_eye": (lex, ley),
        "right_eye": (rex, rey),
        "left_pupil": (lpx, lpy),
        "right_pupil": (rpx, rpy),
    }

    return validate_sightline(gazer, (target_cx, target_cy))


# ---------------------------------------------------------------------------
# Batch validation helper
# ---------------------------------------------------------------------------

def validate_sightline_batch(entries):
    """
    Validate multiple sight-line entries.

    Parameters
    ----------
    entries : list of dict
        Each entry must have:
            label  — str, human-readable name (e.g. "SF01 Luma -> Byte")
            gazer  — dict with left_eye, right_eye, left_pupil, right_pupil
            target — (x, y)

    Returns
    -------
    dict with keys:
        results  — list of (label, result_dict) tuples
        overall  — "PASS" | "WARN" | "FAIL" (worst of all entries)
        pass_count, warn_count, fail_count — int
        summary  — str
    """
    results = []
    pass_count = 0
    warn_count = 0
    fail_count = 0

    for entry in entries:
        label = entry["label"]
        result = validate_sightline(entry["gazer"], entry["target"])
        results.append((label, result))
        if result["grade"] == "PASS":
            pass_count += 1
        elif result["grade"] == "WARN":
            warn_count += 1
        else:
            fail_count += 1

    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0:
        overall = "WARN"
    else:
        overall = "PASS"

    summary = (
        f"Sight-line validation: {len(results)} checked — "
        f"PASS={pass_count}, WARN={warn_count}, FAIL={fail_count}. "
        f"Overall: {overall}."
    )

    return {
        "results": results,
        "overall": overall,
        "pass": pass_count,
        "warn": warn_count,
        "fail": fail_count,
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# Pixel-based detection from rendered PNGs
# ---------------------------------------------------------------------------

# Known eye-white colors across the production (RGB tuples)
# Used as defaults when no explicit eye_white_rgb is provided.
KNOWN_EYE_WHITES = [
    (242, 240, 248),   # SF01 Luma EYE_W_C
    (250, 240, 220),   # SF05 Luma / Miri EYE_WHITE (Warm Cream)
    (255, 252, 245),   # Legacy SF01 EYE_W_C
    (240, 240, 245),   # Generic near-white
]

# Known pupil colors (very dark, low-saturation)
KNOWN_PUPIL_DARKS = [
    (20, 12, 8),       # Luma EYE_PUP (SF01)
    (59, 40, 32),      # Luma EYE_PUPIL (expression sheets)
    (26, 15, 10),      # Miri EYE_PUPIL
    (14, 8, 4),        # Luma storyboard pupil
    (10, 10, 20),      # Byte EYE_PUP
]


def _rgb_distance(c1, c2):
    """Euclidean distance between two RGB tuples."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def _cluster_pixels_grid(coords, gap=8):
    """
    Group a list of (x, y) pixel coordinates into spatial clusters.
    Uses a grid-accelerated connected-component approach.

    Returns list of lists of (x, y).
    """
    if not coords:
        return []

    # Build a spatial grid for O(1) neighbor lookups
    coord_set = set(coords)
    visited = set()
    clusters = []

    for pt in coords:
        if pt in visited:
            continue
        cluster = []
        queue = [pt]
        visited.add(pt)
        while queue:
            cx, cy = queue.pop(0)
            cluster.append((cx, cy))
            # Check all neighbors within gap distance
            for dx in range(-gap, gap + 1):
                for dy in range(-gap, gap + 1):
                    nb = (cx + dx, cy + dy)
                    if nb in coord_set and nb not in visited:
                        visited.add(nb)
                        queue.append(nb)
        clusters.append(cluster)

    return clusters


def _cluster_centroid(cluster):
    """Return (cx, cy) centroid of a pixel cluster."""
    n = len(cluster)
    sx = sum(p[0] for p in cluster)
    sy = sum(p[1] for p in cluster)
    return (sx / n, sy / n)


def _merge_nearby_clusters(clusters, merge_dist=20):
    """
    Merge clusters whose centroids are within merge_dist pixels.
    Sclera may split into top/bottom arcs separated by iris — this
    merges them back into one eye region.
    """
    if len(clusters) <= 1:
        return clusters

    centroids = [_cluster_centroid(c) for c in clusters]
    merged_flags = list(range(len(clusters)))  # union-find parent

    def find(i):
        while merged_flags[i] != i:
            merged_flags[i] = merged_flags[merged_flags[i]]
            i = merged_flags[i]
        return i

    def union(i, j):
        ri, rj = find(i), find(j)
        if ri != rj:
            merged_flags[ri] = rj

    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            cx_i, cy_i = centroids[i]
            cx_j, cy_j = centroids[j]
            dist = math.sqrt((cx_i - cx_j) ** 2 + (cy_i - cy_j) ** 2)
            if dist <= merge_dist:
                union(i, j)

    groups = {}
    for i in range(len(clusters)):
        root = find(i)
        if root not in groups:
            groups[root] = []
        groups[root].extend(clusters[i])

    return list(groups.values())


def _cluster_bbox(cluster):
    """Return (x0, y0, x1, y1) bounding box of a cluster."""
    xs = [p[0] for p in cluster]
    ys = [p[1] for p in cluster]
    return (min(xs), min(ys), max(xs), max(ys))


def detect_eyes_from_png(
    image_path,
    search_box=None,
    eye_white_rgb=None,
    eye_white_tolerance=40,
    pupil_max_value=80,
    min_eye_pixels=20,
    min_pupil_pixels=3,
):
    """
    Detect eye-white regions and pupil positions in a rendered PNG.

    Strategy:
      1. Find pixels matching known eye-white colors (high brightness,
         low saturation, near-white) within the search box.
      2. Cluster those pixels into distinct eye regions.
      3. Within each eye region, find the darkest cluster (pupil).
      4. Return eye centers and pupil centers.

    Parameters
    ----------
    image_path : str
        Path to the PNG file.
    search_box : tuple or None
        (x0, y0, x1, y1) region to search. If None, searches full image.
    eye_white_rgb : tuple or None
        Specific eye-white RGB to match. If None, uses KNOWN_EYE_WHITES.
    eye_white_tolerance : int
        RGB Euclidean distance tolerance for eye-white matching.
    pupil_max_value : int
        Maximum V (in 0-255) for a pixel to be considered pupil-dark.
    min_eye_pixels : int
        Minimum pixel count for a cluster to qualify as an eye.
    min_pupil_pixels : int
        Minimum pixel count for a pupil cluster.

    Returns
    -------
    dict with keys:
        eyes : list of dict, each containing:
            center  — (x, y) eye-white centroid
            bbox    — (x0, y0, x1, y1) eye-white bounding box
            pixels  — int, number of eye-white pixels
            pupil_center — (x, y) pupil centroid (or None)
            pupil_pixels — int
        eye_count : int
        detail : str
    """
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("Pillow required for pixel detection mode")

    try:
        import numpy as np
    except ImportError:
        raise ImportError("NumPy required for pixel detection mode")

    img = Image.open(image_path).convert("RGB")
    arr = np.array(img)
    h, w = arr.shape[:2]

    # Define search region
    if search_box:
        x0, y0, x1, y1 = search_box
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(w, x1), min(h, y1)
    else:
        x0, y0, x1, y1 = 0, 0, w, h

    region = arr[y0:y1, x0:x1]

    # Build list of eye-white reference colors
    if eye_white_rgb is not None:
        white_refs = [eye_white_rgb]
    else:
        white_refs = KNOWN_EYE_WHITES

    # Find eye-white pixels: match any known eye-white within tolerance
    # Use tighter tolerance (RGB distance) to avoid matching skin or rim light
    region_f = region.astype(np.float32)
    eye_white_mask = np.zeros((y1 - y0, x1 - x0), dtype=bool)
    for ref in white_refs:
        ref_arr = np.array(ref, dtype=np.float32)
        diff = np.sqrt(np.sum((region_f - ref_arr) ** 2, axis=2))
        eye_white_mask |= (diff <= eye_white_tolerance)

    # Additional filter: eye whites must be bright (V > 200) and low saturation
    value = np.max(region, axis=2)
    min_ch = np.min(region, axis=2)
    saturation = np.where(value > 0,
                          (value.astype(np.float32) - min_ch.astype(np.float32))
                          / value.astype(np.float32), 0)
    eye_white_mask &= (value >= 200)
    eye_white_mask &= (saturation <= 0.15)

    # Collect matching pixel coordinates (in full-image space)
    ey_coords, ex_coords = np.where(eye_white_mask)
    eye_pixels = [(int(ex_coords[i]) + x0, int(ey_coords[i]) + y0)
                  for i in range(len(ex_coords))]

    if len(eye_pixels) < min_eye_pixels:
        return {
            "eyes": [],
            "eye_count": 0,
            "detail": (f"No eye-white regions found "
                       f"(only {len(eye_pixels)} matching pixels, need {min_eye_pixels})")
        }

    # Use morphological dilation on the sclera binary mask to bridge the
    # iris gap (sclera arcs above and below iris should form one region).
    # The dilation radius is tuned for style-frame scale: iris ~10-15px tall.
    from scipy import ndimage
    # Dilation connects top/bottom sclera arcs across the iris.
    # Use a vertically-elongated kernel: tall enough to bridge iris,
    # narrow enough to avoid merging adjacent eyes.
    struct = np.ones((13, 1), dtype=bool)  # 13px tall, 1px wide (vertical only)
    dilated_mask = ndimage.binary_dilation(eye_white_mask, structure=struct, iterations=1)

    # Label connected components on the dilated mask
    labeled, num_labels = ndimage.label(dilated_mask)

    # Map each original sclera pixel to its component label
    # Build clusters from original (non-dilated) pixel positions
    label_map = labeled  # same coordinate space as eye_white_mask
    eye_clusters_dict = {}
    for i in range(len(ex_coords)):
        lx = int(ex_coords[i])
        ly = int(ey_coords[i])
        lbl = label_map[ly, lx]
        if lbl > 0:
            if lbl not in eye_clusters_dict:
                eye_clusters_dict[lbl] = []
            eye_clusters_dict[lbl].append((lx + x0, ly + y0))

    # Filter by minimum size
    merged = [c for c in eye_clusters_dict.values() if len(c) >= min_eye_pixels]

    if not merged:
        return {
            "eyes": [],
            "eye_count": 0,
            "detail": f"No eye-white clusters large enough (need {min_eye_pixels}px each)"
        }

    # Sort by size descending, take top candidates (max 4 eyes for 2-char scenes)
    merged.sort(key=lambda c: -len(c))
    merged = merged[:4]

    # For each eye region: use sclera bbox center as eye center, then find
    # the iris/pupil centroid within the sclera bbox to determine gaze.
    # This approach is robust because:
    # - Bbox center is stable even when sclera is asymmetric (wide/squinted)
    # - Iris detection uses a brightness band (V 50-170) that excludes
    #   outline/lid pixels (V < 40) and sclera/highlight (V > 200)
    eyes = []
    for ec in merged:
        ec_bbox = _cluster_bbox(ec)
        bx0, by0, bx1, by1 = ec_bbox

        # Eye center = bbox center (more stable than pixel centroid)
        bbox_cx = (bx0 + bx1) / 2.0
        bbox_cy = (by0 + by1) / 2.0

        # Search for iris/pupil within sclera bbox only (no padding).
        # Outlines are AT the edge or outside — staying inside avoids them.
        eye_w = bx1 - bx0
        eye_h = by1 - by0

        # Search for pupil within sclera bbox, expanded horizontally
        # to catch shifted pupils, narrowed vertically to exclude brows.
        h_expand = max(4, eye_w // 2)
        ib_x0 = max(0, bx0 - h_expand)
        ib_y0 = max(0, by0)
        ib_x1 = min(w, bx1 + h_expand + 1)
        ib_y1 = min(h, by1 + 1)

        if ib_x1 <= ib_x0 or ib_y1 <= ib_y0:
            eyes.append({
                "center": (bbox_cx, bbox_cy),
                "bbox": ec_bbox,
                "pixels": len(ec),
                "pupil_center": None,
                "pupil_pixels": 0,
            })
            continue

        pupil_center = None
        pupil_count = 0

        # Find iris/pupil centroid within the sclera bounding box.
        # Use only pixels in the iris brightness band (V 20-80, excludes
        # outline at V<20 and skin/sclera at V>100).
        search_region = arr[ib_y0:ib_y1, ib_x0:ib_x1]
        search_value = np.max(search_region, axis=2)

        # Find the actual pupil dot: the DARKEST small cluster.
        # At style-frame scale the pupil is ~6-12px across with V < 30.
        # Use a tight value threshold to isolate just the pupil, not
        # the surrounding iris (V 50-80) which would pull the centroid
        # toward the iris center and mask the gaze shift.
        pupil_v_max = min(30, pupil_max_value)
        pupil_mask = (search_value >= 10) & (search_value <= pupil_v_max)
        py_coords, px_coords = np.where(pupil_mask)

        if len(px_coords) >= min_pupil_pixels:
            # Simple centroid of the darkest pixels
            pcx = float(px_coords.mean()) + ib_x0
            pcy = float(py_coords.mean()) + ib_y0
            pupil_center = (pcx, pcy)
            pupil_count = len(px_coords)

        if pupil_center is None:
            # Fallback: use broader range
            broad_mask = (search_value >= 15) & (search_value <= pupil_max_value)
            by2, bx2 = np.where(broad_mask)
            if len(bx2) >= min_pupil_pixels:
                pcx = float(bx2.mean()) + ib_x0
                pcy = float(by2.mean()) + ib_y0
                pupil_center = (pcx, pcy)
                pupil_count = len(bx2)

        eyes.append({
            "center": (bbox_cx, bbox_cy),
            "bbox": ec_bbox,
            "pixels": len(ec),
            "pupil_center": pupil_center,
            "pupil_pixels": pupil_count,
        })

    # Compute confidence based on eye size (larger = more reliable)
    avg_eye_w = sum(e["bbox"][2] - e["bbox"][0] for e in eyes) / max(1, len(eyes))
    if avg_eye_w >= 30:
        confidence = "HIGH"
        confidence_note = "Eyes are large enough for reliable pixel detection"
    elif avg_eye_w >= 15:
        confidence = "LOW"
        confidence_note = (
            "Eyes are small (avg width {:.0f}px). Pupil shift is only 2-5px "
            "at this scale — pixel detection has limited accuracy. "
            "Construction mode is authoritative.".format(avg_eye_w)
        )
    else:
        confidence = "VERY_LOW"
        confidence_note = (
            "Eyes are very small (avg width {:.0f}px). Pixel detection is "
            "unreliable at this scale.".format(avg_eye_w)
        )

    detail_parts = [f"Detected {len(eyes)} eye region(s) [confidence: {confidence}]"]
    for i, e in enumerate(eyes):
        ew = e["bbox"][2] - e["bbox"][0]
        eh = e["bbox"][3] - e["bbox"][1]
        pup_str = f"pupil at ({e['pupil_center'][0]:.1f}, {e['pupil_center'][1]:.1f})" if e['pupil_center'] else "NO pupil"
        detail_parts.append(
            f"  Eye {i}: center ({e['center'][0]:.1f}, {e['center'][1]:.1f}), "
            f"{ew}x{eh}px, {e['pixels']}px sclera, {pup_str}"
        )
    detail_parts.append(f"  {confidence_note}")

    return {
        "eyes": eyes,
        "eye_count": len(eyes),
        "confidence": confidence,
        "avg_eye_width": avg_eye_w,
        "detail": "\n".join(detail_parts),
    }


def _pair_eyes(eyes):
    """
    Given detected eye regions, pair them into left/right pairs.
    Pairing logic: eyes within similar Y range (vertical alignment)
    and reasonable X separation form a pair.

    Returns list of (left_eye, right_eye) tuples sorted by X,
    where left_eye.center.x < right_eye.center.x.
    """
    if len(eyes) < 2:
        return []

    # Sort by X position
    sorted_eyes = sorted(eyes, key=lambda e: e["center"][0])
    pairs = []
    used = set()

    for i in range(len(sorted_eyes)):
        if i in used:
            continue
        ei = sorted_eyes[i]
        ei_cx, ei_cy = ei["center"]

        # Estimate eye width from bbox
        ei_w = ei["bbox"][2] - ei["bbox"][0]

        best_j = None
        best_dist = float('inf')

        for j in range(i + 1, len(sorted_eyes)):
            if j in used:
                continue
            ej = sorted_eyes[j]
            ej_cx, ej_cy = ej["center"]

            # Must be roughly horizontally aligned (Y within 1.5x eye width)
            y_diff = abs(ei_cy - ej_cy)
            x_diff = ej_cx - ei_cx  # positive since sorted by X

            if y_diff < max(ei_w * 1.5, 15) and x_diff < max(ei_w * 6, 60) and x_diff > max(ei_w * 0.3, 3):
                dist = math.sqrt(x_diff ** 2 + y_diff ** 2)
                if dist < best_dist:
                    best_dist = dist
                    best_j = j

        if best_j is not None:
            pairs.append((sorted_eyes[i], sorted_eyes[best_j]))
            used.add(i)
            used.add(best_j)

    return pairs


def validate_sightline_from_png(
    image_path,
    target,
    search_box=None,
    **detect_kwargs,
):
    """
    End-to-end pixel-based sight-line validation.

    1. Detect eyes and pupils in the rendered PNG.
    2. Pair eyes into left/right.
    3. Validate gaze direction toward target.

    Parameters
    ----------
    image_path : str
        Path to the PNG file.
    target : tuple
        (x, y) gaze target position.
    search_box : tuple or None
        (x0, y0, x1, y1) region to search for eyes.
    **detect_kwargs : dict
        Passed through to detect_eyes_from_png().

    Returns
    -------
    dict with keys from validate_sightline() PLUS:
        detection : dict from detect_eyes_from_png()
        pair_index : int (which eye pair was used, 0-based)
        mode : "pixel" (to distinguish from construction-based results)
    """
    detection = detect_eyes_from_png(image_path, search_box=search_box, **detect_kwargs)

    if detection["eye_count"] < 2:
        return {
            "mid_eye": None,
            "mid_pupil": None,
            "gaze_angle_deg": None,
            "ideal_angle_deg": None,
            "angular_error": None,
            "miss_px": None,
            "grade": "SKIP",
            "detail": f"Cannot validate: {detection['detail']}",
            "detection": detection,
            "pair_index": None,
            "mode": "pixel",
        }

    # Check that at least one pair has both pupils detected
    pairs = _pair_eyes(detection["eyes"])

    if not pairs:
        return {
            "mid_eye": None,
            "mid_pupil": None,
            "gaze_angle_deg": None,
            "ideal_angle_deg": None,
            "angular_error": None,
            "miss_px": None,
            "grade": "SKIP",
            "detail": "Cannot validate: detected eyes could not be paired (no left/right match)",
            "detection": detection,
            "pair_index": None,
            "mode": "pixel",
        }

    # Use the first pair with both pupils detected
    pair_index = None
    selected_pair = None
    for pi, (left, right) in enumerate(pairs):
        if left["pupil_center"] is not None and right["pupil_center"] is not None:
            pair_index = pi
            selected_pair = (left, right)
            break

    if selected_pair is None:
        # Fall back to first pair even if a pupil is missing
        selected_pair = pairs[0]
        pair_index = 0
        missing = []
        if selected_pair[0]["pupil_center"] is None:
            missing.append("left")
        if selected_pair[1]["pupil_center"] is None:
            missing.append("right")
        return {
            "mid_eye": None,
            "mid_pupil": None,
            "gaze_angle_deg": None,
            "ideal_angle_deg": None,
            "angular_error": None,
            "miss_px": None,
            "grade": "SKIP",
            "detail": f"Cannot validate: pupil not detected in {' and '.join(missing)} eye(s)",
            "detection": detection,
            "pair_index": pair_index,
            "mode": "pixel",
        }

    left_eye, right_eye = selected_pair

    gazer = {
        "left_eye": left_eye["center"],
        "right_eye": right_eye["center"],
        "left_pupil": left_eye["pupil_center"],
        "right_pupil": right_eye["pupil_center"],
    }

    result = validate_sightline(gazer, target)
    result["detection"] = detection
    result["pair_index"] = pair_index
    result["mode"] = "pixel"
    result["confidence"] = detection.get("confidence", "UNKNOWN")

    # Add confidence caveat to detail string
    if result["confidence"] == "LOW":
        result["detail"] += (
            " [LOW CONFIDENCE: eyes are small — pixel detection may be inaccurate. "
            "Use construction mode for authoritative results.]"
        )

    return result


# ---------------------------------------------------------------------------
# Self-test: SF01 v007 validation case
# ---------------------------------------------------------------------------

def _self_test():
    """
    Reproduce the SF01 v007 sight-line geometry from C47 debug script.
    Expected result: PASS with ~2.2 deg angular error (was 20.7 deg pre-fix).
    """
    print("=" * 60)
    print("LTG_TOOL_sightline_validator v1.0.0 — Self-Test")
    print("=" * 60)

    W, H = 1280, 720
    SX = W / 1920
    SY = H / 1080

    def sx(n): return int(n * SX)
    def sy(n): return int(n * SY)
    def sp(n): return int(n * min(SX, SY))

    # --- Byte/CRT target position (from SF01 generator) ---
    ceiling_y = sy(int(1080 * 0.12))
    mw_x = sx(int(1920 * 0.50))
    mw_y = ceiling_y + sp(5)
    mw_w = sx(int(1920 * 0.46))
    mw_h = sy(int(1080 * 0.57))
    crt_x = mw_x + int(mw_w * 0.22)
    crt_y = mw_y + int(mw_h * 0.08)
    crt_w = int(mw_w * 0.52)
    crt_h = int(mw_h * 0.62)
    scr_pad = sp(24)
    scr_x0 = crt_x + scr_pad
    scr_y0 = crt_y + scr_pad
    scr_x1 = crt_x + crt_w - scr_pad
    scr_y1 = crt_y + crt_h - scr_pad * 2
    emerge_cx = (scr_x0 + scr_x1) // 2
    emerge_cy = (scr_y0 + scr_y1) // 2

    # --- Luma head position (from SF01 generator) ---
    luma_cx = sx(int(1920 * 0.29))
    luma_base_y = sy(int(1080 * 0.90))
    lean_offset = sp(44)
    torso_top = luma_base_y - sp(260)
    head_cx_body = luma_cx + lean_offset
    head_cy_body = torso_top - sp(70)
    head_gaze_offset = sp(18)
    head_cx = head_cx_body + head_gaze_offset
    head_cy = head_cy_body + sp(6)

    scale = 0.92

    print(f"\nTarget (Byte emerge): ({emerge_cx}, {emerge_cy})")
    print(f"Gazer head center:    ({head_cx}, {head_cy})")
    print(f"Gazer scale:          {scale}")

    # Test 1: geometry-based API (reconstructs eyes from head center)
    print("\n--- Test 1: validate_sightline_from_geometry() ---")
    result1 = validate_sightline_from_geometry(
        head_cx, head_cy, scale,
        emerge_cx, emerge_cy,
        canvas_w=W, canvas_h=H,
    )
    print(f"  {result1['detail']}")
    assert result1["grade"] == "PASS", f"Expected PASS, got {result1['grade']}"
    assert result1["angular_error"] < 5.0, f"Expected <5 deg, got {result1['angular_error']:.1f}"
    print("  ASSERT: grade == PASS [OK]")
    print(f"  ASSERT: angular_error {result1['angular_error']:.1f} < 5.0 [OK]")

    # Test 2: raw API with manually computed eye/pupil positions
    print("\n--- Test 2: validate_sightline() with explicit positions ---")
    min_ratio = min(SX, SY)
    def p(n): return int(n * scale * min_ratio)

    lex = head_cx + p(4)
    ley = head_cy - p(10)
    rex = head_cx + p(38)
    rey = head_cy - p(8)

    mid_eye_x = (lex + rex) // 2
    mid_eye_y = (ley + rey) // 2
    aim_dx = emerge_cx - mid_eye_x
    aim_dy = emerge_cy - mid_eye_y
    aim_dist = max(1, (aim_dx ** 2 + aim_dy ** 2) ** 0.5)
    pupil_mag = p(8)
    psx = int(pupil_mag * aim_dx / aim_dist)
    psy = int(pupil_mag * aim_dy / aim_dist)

    gazer = {
        "left_eye": (lex, ley),
        "right_eye": (rex, rey),
        "left_pupil": (lex + psx, ley + psy),
        "right_pupil": (rex + psx, rey + psy),
    }
    result2 = validate_sightline(gazer, (emerge_cx, emerge_cy))
    print(f"  {result2['detail']}")
    assert result2["grade"] == "PASS", f"Expected PASS, got {result2['grade']}"
    print("  ASSERT: grade == PASS [OK]")

    # Test 3: simulate pre-C47 bug (horizontal-only pupil shift) — should FAIL
    print("\n--- Test 3: pre-C47 horizontal-only shift (expect FAIL) ---")
    gazer_broken = {
        "left_eye": (lex, ley),
        "right_eye": (rex, rey),
        "left_pupil": (lex + p(8), ley),       # horizontal only — no Y component
        "right_pupil": (rex + p(8), rey),       # horizontal only — no Y component
    }
    result3 = validate_sightline(gazer_broken, (emerge_cx, emerge_cy))
    print(f"  {result3['detail']}")
    assert result3["grade"] == "FAIL", f"Expected FAIL, got {result3['grade']}"
    assert result3["angular_error"] > 15.0, f"Expected >15 deg, got {result3['angular_error']:.1f}"
    print("  ASSERT: grade == FAIL [OK] (pre-fix bug correctly caught)")
    print(f"  ASSERT: angular_error {result3['angular_error']:.1f} > 15.0 [OK]")

    # Test 4: batch validation
    print("\n--- Test 4: validate_sightline_batch() ---")
    entries = [
        {"label": "SF01 v007 (fixed)", "gazer": gazer, "target": (emerge_cx, emerge_cy)},
        {"label": "SF01 pre-fix (broken)", "gazer": gazer_broken, "target": (emerge_cx, emerge_cy)},
    ]
    batch = validate_sightline_batch(entries)
    print(f"  {batch['summary']}")
    assert batch["overall"] == "FAIL", f"Expected FAIL overall (one entry fails), got {batch['overall']}"
    assert batch["pass"] == 1, f"Expected 1 PASS, got {batch['pass']}"
    assert batch["fail"] == 1, f"Expected 1 FAIL, got {batch['fail']}"
    print("  ASSERT: batch overall == FAIL (correct — one failing entry) [OK]")
    print("  ASSERT: pass=1, fail=1 [OK]")

    # Test 5: angle normalization edge case — opposite directions
    print("\n--- Test 5: angle normalization (180 deg opposite) ---")
    gazer_opposite = {
        "left_eye": (100, 100),
        "right_eye": (120, 100),
        "left_pupil": (95, 100),     # shifted LEFT
        "right_pupil": (115, 100),   # shifted LEFT
    }
    result5 = validate_sightline(gazer_opposite, (200, 100))  # target is to the RIGHT
    print(f"  {result5['detail']}")
    assert result5["grade"] == "FAIL", f"Expected FAIL for opposite gaze, got {result5['grade']}"
    assert result5["angular_error"] >= 170, f"Expected ~180 deg error, got {result5['angular_error']:.1f}"
    print("  ASSERT: opposite gaze = FAIL [OK]")

    print("\n" + "=" * 60)
    print("ALL SELF-TESTS PASSED")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Pixel detection self-test against SF01 v007
# ---------------------------------------------------------------------------

def _pixel_self_test():
    """
    Test pixel detection mode against SF01 v007 rendered PNG.
    Compares pixel-detected gaze against the construction-based result.
    """
    print("\n" + "=" * 60)
    print("PIXEL DETECTION MODE — Self-Test")
    print("=" * 60)

    # SF01 v007 rendered PNG path
    sf01_path = os.path.join(
        os.path.dirname(__file__), "..",
        "color", "style_frames", "LTG_COLOR_styleframe_discovery.png"
    )
    sf01_path = os.path.normpath(sf01_path)

    if not os.path.exists(sf01_path):
        print(f"  SKIP: SF01 PNG not found at {sf01_path}")
        return None

    print(f"  Image: {sf01_path}")

    # --- Compute the known target (Byte emerge center) ---
    W, H = 1280, 720
    SX = W / 1920
    SY = H / 1080

    def sx(n): return int(n * SX)
    def sy(n): return int(n * SY)
    def sp(n): return int(n * min(SX, SY))

    ceiling_y = sy(int(1080 * 0.12))
    mw_x = sx(int(1920 * 0.50))
    mw_y = ceiling_y + sp(5)
    mw_w = sx(int(1920 * 0.46))
    mw_h = sy(int(1080 * 0.57))
    crt_x = mw_x + int(mw_w * 0.22)
    crt_y = mw_y + int(mw_h * 0.08)
    crt_w = int(mw_w * 0.52)
    crt_h = int(mw_h * 0.62)
    scr_pad = sp(24)
    scr_x0 = crt_x + scr_pad
    scr_y0 = crt_y + scr_pad
    scr_x1 = crt_x + crt_w - scr_pad
    scr_y1 = crt_y + crt_h - scr_pad * 2
    emerge_cx = (scr_x0 + scr_x1) // 2
    emerge_cy = (scr_y0 + scr_y1) // 2

    target = (emerge_cx, emerge_cy)
    print(f"  Target (Byte emerge): {target}")

    # --- Compute Luma head region for search_box ---
    luma_cx = sx(int(1920 * 0.29))
    luma_base_y = sy(int(1080 * 0.90))
    lean_offset = sp(44)
    torso_top = luma_base_y - sp(260)
    head_cx_body = luma_cx + lean_offset
    head_cy_body = torso_top - sp(70)
    head_gaze_offset = sp(18)
    head_cx = head_cx_body + head_gaze_offset
    head_cy = head_cy_body + sp(6)

    # Search box: generous region around head
    head_r = 60  # approximate head radius at this scale
    search_box = (
        head_cx - head_r * 2,
        head_cy - head_r * 2,
        head_cx + head_r * 2,
        head_cy + head_r * 2,
    )
    print(f"  Search box: {search_box}")

    # --- Test 1: Detection ---
    print("\n--- Pixel Test 1: Eye detection ---")
    detection = detect_eyes_from_png(sf01_path, search_box=search_box)
    print(f"  {detection['detail']}")
    print(f"  Eye count: {detection['eye_count']}")

    if detection["eye_count"] < 2:
        print("  WARN: Fewer than 2 eyes detected — pixel detection may need tuning")
        print("  (This does not mean the tool is broken — detection depends on")
        print("  eye-white/pupil contrast in the specific render.)")

    # --- Test 2: End-to-end pixel validation ---
    print("\n--- Pixel Test 2: validate_sightline_from_png() ---")
    pixel_result = validate_sightline_from_png(
        sf01_path, target, search_box=search_box
    )
    print(f"  Mode: {pixel_result['mode']}")
    print(f"  Grade: {pixel_result['grade']}")
    if pixel_result['angular_error'] is not None:
        print(f"  Angular error: {pixel_result['angular_error']:.1f} deg")
        print(f"  Gaze angle: {pixel_result['gaze_angle_deg']:.1f} deg")
        print(f"  Ideal angle: {pixel_result['ideal_angle_deg']:.1f} deg")
        print(f"  Miss at target range: {pixel_result['miss_px']:.1f}px")
    else:
        print(f"  Detail: {pixel_result['detail']}")

    # --- Test 3: Compare with construction-based result ---
    print("\n--- Pixel Test 3: Accuracy comparison vs construction mode ---")
    construction_result = validate_sightline_from_geometry(
        head_cx, head_cy, 0.92,
        emerge_cx, emerge_cy,
        canvas_w=W, canvas_h=H,
    )
    print(f"  Construction mode: {construction_result['angular_error']:.1f} deg ({construction_result['grade']})")

    if pixel_result['angular_error'] is not None:
        delta = abs(pixel_result['angular_error'] - construction_result['angular_error'])
        print(f"  Pixel mode:        {pixel_result['angular_error']:.1f} deg ({pixel_result['grade']})")
        print(f"  Delta:             {delta:.1f} deg")

        if delta < 10:
            print("  ASSESSMENT: Pixel detection tracks construction mode within 10 deg — GOOD")
        elif delta < 20:
            print("  ASSESSMENT: Pixel detection diverges 10-20 deg from construction — ACCEPTABLE")
            print("  (Pixel mode is approximate; construction mode is authoritative)")
        else:
            print("  ASSESSMENT: Pixel detection diverges >20 deg from construction — POOR")
            print("  (Pixel mode unreliable for this asset — use construction mode)")
    else:
        print(f"  Pixel mode:        SKIP ({pixel_result['detail']})")
        print("  ASSESSMENT: Pixel detection could not run — use construction mode for this asset")

    return pixel_result


# ---------------------------------------------------------------------------
# CLI interface
# ---------------------------------------------------------------------------

def _cli():
    """Command-line interface for sightline validation."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Sight-line validator — construction and pixel detection modes"
    )
    parser.add_argument("--self-test", action="store_true",
                        help="Run construction-mode self-tests")
    parser.add_argument("--pixel-test", action="store_true",
                        help="Run pixel detection mode test against SF01 v007")
    parser.add_argument("--png", type=str, default=None,
                        help="Path to rendered PNG for pixel-mode validation")
    parser.add_argument("--target", type=int, nargs=2, default=None,
                        metavar=("TX", "TY"),
                        help="Gaze target position (x y)")
    parser.add_argument("--search-box", type=int, nargs=4, default=None,
                        metavar=("X0", "Y0", "X1", "Y1"),
                        help="Search region for eye detection (x0 y0 x1 y1)")
    parser.add_argument("--eye-white-tolerance", type=int, default=40,
                        help="RGB distance tolerance for eye-white matching (default 40)")
    parser.add_argument("--pupil-max-value", type=int, default=80,
                        help="Max pixel value (0-255) for pupil detection (default 80)")

    args = parser.parse_args()

    if args.self_test or (not args.png and not args.pixel_test):
        _self_test()

    if args.pixel_test:
        _pixel_self_test()

    if args.png:
        if args.target is None:
            parser.error("--target TX TY is required with --png")
        target = tuple(args.target)
        search_box = tuple(args.search_box) if args.search_box else None

        print("\n" + "=" * 60)
        print("PIXEL DETECTION MODE — Custom Image")
        print("=" * 60)
        print(f"  Image: {args.png}")
        print(f"  Target: {target}")
        if search_box:
            print(f"  Search box: {search_box}")

        result = validate_sightline_from_png(
            args.png, target,
            search_box=search_box,
            eye_white_tolerance=args.eye_white_tolerance,
            pupil_max_value=args.pupil_max_value,
        )

        print(f"\n  Mode: {result['mode']}")
        print(f"  Grade: {result['grade']}")
        if result['angular_error'] is not None:
            print(f"  Angular error: {result['angular_error']:.1f} deg")
            print(f"  Miss at target: {result['miss_px']:.1f}px")
        print(f"  Detail: {result.get('detail', 'N/A')}")
        print(f"  Detection: {result['detection']['detail']}")


if __name__ == "__main__":
    _cli()
