#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_vanishing_point_lint.py
Vanishing Point Linter — "Luma & the Glitchkin"
Author: Kai Nakamura / Cycle 40
Spec: ideabox/actioned/20260330_kai_nakamura_vanishing_point_spec.md (C39)
      Producer brief: members/kai_nakamura/inbox/20260330_cycle40_brief.md

Uses Sobel edge detection (numpy + cv2) to estimate the dominant vanishing-point
direction in environment backgrounds and style frames. Flags frames where the VP
estimate falls outside the expected range for the scene type.

Algorithm
---------
1. Load image → grayscale numpy array
2. Compute Sobel gradient in X and Y:
       Gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
       Gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
3. Encode as complex number per pixel: Z = Gx + j·Gy
   → angle = arctan2(Gy, Gx) (edge perpendicular direction)
   → magnitude = sqrt(Gx² + Gy²)
4. Build weighted angle histogram (72 bins × 5°) weighted by magnitude.
5. Find dominant angle θ = histogram peak.
6. The dominant edge direction is θ. Lines perpendicular to θ (at θ ± 90°) are
   the perspective lines. Their convergence point is the VP direction.
7. The VP azimuth (horizontal position in frame) is estimated from the dominant
   near-horizontal edge cluster. If lines converge strongly to left or right of
   center, the VP is off-center.
8. Apply per-scene rules:
   - Real World (ENV/SF01/SF02): VP expected in middle 30% of frame width.
     Flag WARN if VP estimate is outside [-0.15W … +0.15W] from center.
   - Glitch Layer (SF03 and Glitch Layer environments): VP may be extreme.
     WARN only if NO dominant VP is detected (flat/parallel-line scene).
   - auto: infer from filename.

Checks
------
VP001  Dominant edge convergence detected (any file)
       FAIL if image has no detectable edge structure (< threshold magnitude)
VP002  Real-World VP in frame (Real World environments and SF01/SF02)
       WARN if VP estimate is outside center 30% of frame width
VP003  Glitch Layer VP extreme (SF03, glitch environments)
       INFO — extreme VP is expected; no fail unless VP completely absent

Scene Classification (from filename)
--------------------------------------
  "real_world" / "Real World" / "rw_" → REAL_WORLD
  "glitch_layer" / "other_side" / "SF03" → GLITCH_LAYER
  "classroom" / "kitchen" / "hallway" / "main_street" / "tech_den" → REAL_WORLD
  "SF01" / "SF02" → REAL_WORLD
  default → REAL_WORLD (conservative)

Usage
-----
    python LTG_TOOL_vanishing_point_lint.py image.png
    python LTG_TOOL_vanishing_point_lint.py output/color/style_frames/
    python LTG_TOOL_vanishing_point_lint.py --save-report PATH output/

API
---
    from LTG_TOOL_vanishing_point_lint import lint_file, lint_directory, format_report

    result = lint_file("LTG_ENV_classroom_bg.png")
    # result: dict with keys: file, scene_type, grade, issues, vp_azimuth_pct,
    #                         dominant_angle_deg, magnitude_mean, skipped_reason

    results = lint_directory("/path/to/output/")
    print(format_report(results))

Changelog
---------
v1.0.0 (C40): Initial implementation per C39 ideabox spec + C40 Producer brief.
    Sobel X+Y → complex angle+magnitude encoding.
    Dominant edge direction histogram → VP estimate.
    Real World VP expected in middle 30% of frame.
    Glitch Layer: extreme VP allowed.
    CLI + module API.
    Dependencies: numpy + cv2. Falls back gracefully when cv2 is absent.

Dependencies
------------
    numpy — required
    cv2 (OpenCV) — required for Sobel. Falls back to numpy convolution if absent.
    Pillow — for image loading
"""

__version__ = "1.0.0"

import os
import sys
import math
import glob as _glob

try:
    import numpy as np
    _NP_AVAILABLE = True
except ImportError:
    np = None
    _NP_AVAILABLE = False

try:
    import cv2
    _CV2_AVAILABLE = True
except ImportError:
    cv2 = None
    _CV2_AVAILABLE = False

from PIL import Image


# ── Scene classification ──────────────────────────────────────────────────────

SCENE_REAL_WORLD = "REAL_WORLD"
SCENE_GLITCH_LAYER = "GLITCH_LAYER"
SCENE_UNKNOWN = "UNKNOWN"

_GLITCH_KEYWORDS = [
    "glitch_layer", "glitchlayer", "other_side", "otherside",
    "sf03", "styleframe_otherside", "styleframe03",
]
_REAL_WORLD_KEYWORDS = [
    "classroom", "kitchen", "hallway", "main_street", "mainstreet",
    "tech_den", "techden", "millbrook", "grandma",
    "sf01", "sf02", "styleframe_discovery", "styleframe_glitch_storm",
    "styleframe01", "styleframe02",
    "real_world", "rw_",
]


def classify_scene(filepath):
    """
    Classify scene type from filename.

    Returns SCENE_REAL_WORLD, SCENE_GLITCH_LAYER, or SCENE_UNKNOWN.
    Defaults to REAL_WORLD (conservative) for unknown files.
    """
    name = os.path.basename(filepath).lower()
    for kw in _GLITCH_KEYWORDS:
        if kw in name:
            return SCENE_GLITCH_LAYER
    for kw in _REAL_WORLD_KEYWORDS:
        if kw in name:
            return SCENE_REAL_WORLD
    return SCENE_REAL_WORLD  # conservative default


# ── Sobel / edge computation ─────────────────────────────────────────────────

def _sobel_numpy_fallback(gray_f32):
    """
    Sobel-like convolution using numpy when cv2 is unavailable.
    Returns (Gx, Gy) float64 arrays.
    """
    from numpy.lib.stride_tricks import as_strided
    import numpy as np

    # Simple 3×3 Sobel kernels
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
    Ky = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float64)

    h, w = gray_f32.shape
    Gx = np.zeros_like(gray_f32, dtype=np.float64)
    Gy = np.zeros_like(gray_f32, dtype=np.float64)

    # Pad
    padded = np.pad(gray_f32, 1, mode='edge')
    for kr in range(3):
        for kc in range(3):
            Gx += Kx[kr, kc] * padded[kr:kr + h, kc:kc + w]
            Gy += Ky[kr, kc] * padded[kr:kr + h, kc:kc + w]
    return Gx, Gy


def compute_sobel(image_path):
    """
    Load image, convert to grayscale, compute Sobel gradients.

    Returns
    -------
    dict with keys:
        Gx, Gy        — gradient arrays (float64)
        angle_deg     — per-pixel edge angle in degrees (arctan2, 0–360)
        magnitude     — per-pixel edge magnitude
        width, height — image dimensions
    Returns None if image cannot be loaded or dependencies missing.
    """
    if not _NP_AVAILABLE:
        return None

    try:
        img = Image.open(image_path).convert("L")
        # Downscale for speed (Sobel on 1280px is fine; avoid 1920px cost)
        img.thumbnail((640, 640), Image.LANCZOS)
        gray_np = np.array(img, dtype=np.float32)
    except Exception:
        return None

    h, w = gray_np.shape

    if _CV2_AVAILABLE:
        # OpenCV Sobel (ksize=5 for better angular resolution)
        Gx = cv2.Sobel(gray_np, cv2.CV_64F, 1, 0, ksize=5)
        Gy = cv2.Sobel(gray_np, cv2.CV_64F, 0, 1, ksize=5)
    else:
        Gx, Gy = _sobel_numpy_fallback(gray_np.astype(np.float64))

    magnitude = np.sqrt(Gx ** 2 + Gy ** 2)
    angle_rad = np.arctan2(Gy, Gx)
    angle_deg = np.degrees(angle_rad) % 360.0  # map to [0, 360)

    return {
        "Gx": Gx,
        "Gy": Gy,
        "angle_deg": angle_deg,
        "magnitude": magnitude,
        "width": w,
        "height": h,
    }


# ── Angle histogram and VP estimation ────────────────────────────────────────

N_BINS = 72
BIN_DEG = 360.0 / N_BINS   # 5° per bin


def build_angle_histogram(sobel_data, mag_threshold_pct=0.10):
    """
    Build a magnitude-weighted angle histogram from Sobel data.

    Pixels with magnitude below (mag_threshold_pct × max_mag) are excluded —
    they are noise, not actual edges.

    Returns
    -------
    dict:
        histogram   — numpy array of N_BINS floats (weighted counts)
        peak_bin    — index of dominant bin
        peak_angle  — dominant edge angle in degrees
        mag_mean    — mean magnitude across all pixels
        strong_pct  — fraction of pixels above threshold
    """
    angle_deg = sobel_data["angle_deg"]
    magnitude = sobel_data["magnitude"]

    max_mag = magnitude.max()
    threshold = max_mag * mag_threshold_pct

    strong_mask = magnitude > threshold
    strong_angles = angle_deg[strong_mask]
    strong_magnitudes = magnitude[strong_mask]

    # Build histogram
    histogram = np.zeros(N_BINS, dtype=np.float64)
    if len(strong_angles) > 0:
        bin_indices = (strong_angles / BIN_DEG).astype(int) % N_BINS
        for bi, mag in zip(bin_indices.flat, strong_magnitudes.flat):
            histogram[bi] += mag

    peak_bin = int(np.argmax(histogram))
    peak_angle = peak_bin * BIN_DEG + BIN_DEG / 2.0   # center of dominant bin

    return {
        "histogram": histogram,
        "peak_bin": peak_bin,
        "peak_angle": peak_angle,
        "mag_mean": float(magnitude.mean()),
        "strong_pct": float(strong_mask.mean()),
    }


def estimate_vp_azimuth(sobel_data, hist_data):
    """
    Estimate the vanishing point azimuth (horizontal position relative to frame center)
    from the dominant near-horizontal edge cluster.

    Perspective lines in a scene converge at the VP. For a standard 16:9 frame
    with a VP on the horizon, most perspective lines are near-horizontal (0–30°).
    The horizontal component of their angles biases toward the VP direction.

    Method: For edges with angle within ±30° of horizontal (0° or 180°),
    sum their Gx magnitudes. If Gx > 0 dominates → lines lean right → VP is to the right.
    If Gx < 0 dominates → lines lean left → VP is to the left.

    Returns azimuth as fraction of frame half-width: -1.0 = far left, +1.0 = far right,
    0.0 = center.
    """
    angle_deg = sobel_data["angle_deg"]
    Gx = sobel_data["Gx"]
    magnitude = sobel_data["magnitude"]
    w = sobel_data["width"]

    max_mag = magnitude.max()
    if max_mag == 0:
        return 0.0

    threshold = max_mag * 0.10

    # Near-horizontal edges: angle within 30° of 0° or 180°
    angle_mod = angle_deg % 180.0   # fold 180–360 onto 0–180
    near_horiz = ((angle_mod < 30) | (angle_mod > 150)) & (magnitude > threshold)

    if near_horiz.sum() == 0:
        return 0.0

    # Weighted mean of Gx for near-horizontal edges
    gx_near = Gx[near_horiz]
    mag_near = magnitude[near_horiz]
    weighted_gx = np.sum(gx_near * mag_near) / np.sum(mag_near)

    # Normalise by frame half-width worth of Sobel response
    # At image width w, max meaningful Gx ≈ 255 (full contrast edge)
    # We normalise so ±255 → ±1.0 and clamp
    azimuth = float(np.clip(weighted_gx / 255.0, -1.0, 1.0))
    return azimuth


# ── Lint logic ────────────────────────────────────────────────────────────────

# Real World VP tolerance: center 30% of frame = ±0.15 half-widths
REAL_WORLD_VP_TOLERANCE = 0.15

# Minimum strong-edge fraction: if < this, VP001 FAIL (no detectable edge structure)
MIN_STRONG_PCT = 0.02

# Minimum mean magnitude for VP001 (very dark/flat images)
MIN_MAG_MEAN = 1.0


def lint_file(filepath, scene_type=None):
    """
    Lint a single image file for vanishing point compliance.

    Parameters
    ----------
    filepath   : str — path to PNG image file
    scene_type : str or None — "REAL_WORLD", "GLITCH_LAYER", or None (auto-classify)

    Returns
    -------
    dict:
        file            — str: filepath
        scene_type      — str: classified scene type
        grade           — str: "PASS" / "WARN" / "FAIL" / "SKIP"
        issues          — list of str: issue descriptions
        vp_azimuth_pct  — float or None: VP azimuth as fraction of half-width
        dominant_angle_deg — float or None: dominant edge angle in degrees
        magnitude_mean  — float or None: mean gradient magnitude
        strong_pct      — float or None: fraction of strong-edge pixels
        skipped_reason  — str or None: reason if SKIP
    """
    result = {
        "file": filepath,
        "scene_type": scene_type,
        "grade": "SKIP",
        "issues": [],
        "vp_azimuth_pct": None,
        "dominant_angle_deg": None,
        "magnitude_mean": None,
        "strong_pct": None,
        "skipped_reason": None,
    }

    if not os.path.isfile(filepath):
        result["skipped_reason"] = "File not found"
        return result

    ext = os.path.splitext(filepath)[1].lower()
    if ext not in (".png", ".jpg", ".jpeg"):
        result["skipped_reason"] = "Not an image file"
        return result

    if not _NP_AVAILABLE:
        result["skipped_reason"] = "numpy not available"
        return result

    # Auto-classify scene type
    if scene_type is None:
        scene_type = classify_scene(filepath)
    result["scene_type"] = scene_type

    # Compute Sobel
    sobel_data = compute_sobel(filepath)
    if sobel_data is None:
        result["skipped_reason"] = "Could not load or process image"
        return result

    # Build angle histogram
    hist_data = build_angle_histogram(sobel_data)
    result["dominant_angle_deg"] = round(hist_data["peak_angle"], 1)
    result["magnitude_mean"] = round(hist_data["mag_mean"], 2)
    result["strong_pct"] = round(hist_data["strong_pct"], 4)

    # Estimate VP azimuth
    vp_azimuth = estimate_vp_azimuth(sobel_data, hist_data)
    result["vp_azimuth_pct"] = round(vp_azimuth, 3)

    issues = []

    # VP001 — Dominant edge structure detected
    if hist_data["strong_pct"] < MIN_STRONG_PCT or hist_data["mag_mean"] < MIN_MAG_MEAN:
        issues.append(
            f"VP001: FAIL — Insufficient edge structure detected "
            f"(strong_pct={hist_data['strong_pct']:.3f}, mag_mean={hist_data['mag_mean']:.1f}). "
            f"Image may be flat/solid-color or very low contrast."
        )

    # VP002 — Real World VP in frame center
    if scene_type == SCENE_REAL_WORLD:
        if abs(vp_azimuth) > REAL_WORLD_VP_TOLERANCE:
            direction = "right" if vp_azimuth > 0 else "left"
            issues.append(
                f"VP002: WARN — Real World scene VP estimate is off-center "
                f"(azimuth={vp_azimuth:+.3f}, tolerance=±{REAL_WORLD_VP_TOLERANCE:.2f}). "
                f"Perspective lines appear to converge toward {direction} of frame. "
                f"Expected VP within center 30% of frame width."
            )

    # VP003 — Glitch Layer VP info
    if scene_type == SCENE_GLITCH_LAYER:
        if hist_data["strong_pct"] >= MIN_STRONG_PCT:
            issues.append(
                f"VP003: INFO — Glitch Layer scene; extreme VP acceptable "
                f"(azimuth={vp_azimuth:+.3f}, dominant_angle={hist_data['peak_angle']:.1f}°). "
                f"No constraint violation — documenting for critic reference."
            )

    result["issues"] = issues

    # Compute grade
    has_fail = any(i.startswith("VP001: FAIL") for i in issues)
    has_warn = any("WARN" in i for i in issues)
    if has_fail:
        result["grade"] = "FAIL"
    elif has_warn:
        result["grade"] = "WARN"
    else:
        result["grade"] = "PASS"

    return result


def lint_directory(directory, pattern="*.png", scene_type=None):
    """
    Lint all PNG images in a directory.

    Parameters
    ----------
    directory  : str — path to directory
    pattern    : str — glob pattern (default "*.png")
    scene_type : str or None — override scene type for all files

    Returns
    -------
    list of result dicts (from lint_file)
    """
    results = []
    search_path = os.path.join(directory, pattern)
    files = sorted(_glob.glob(search_path))
    for f in files:
        results.append(lint_file(f, scene_type=scene_type))
    return results


# ── Formatting ────────────────────────────────────────────────────────────────

def format_report(results, include_pass=True, include_info=True):
    """
    Format lint results as a human-readable Markdown report.

    Parameters
    ----------
    results      : list of result dicts from lint_file / lint_directory
    include_pass : bool — include PASS files in output (default True)
    include_info : bool — include INFO issues in output (default True)

    Returns
    -------
    str — Markdown-formatted report
    """
    if not results:
        return "# Vanishing Point Lint Report\n\nNo results.\n"

    total = len(results)
    pass_count = sum(1 for r in results if r["grade"] == "PASS")
    warn_count = sum(1 for r in results if r["grade"] == "WARN")
    fail_count = sum(1 for r in results if r["grade"] == "FAIL")
    skip_count = sum(1 for r in results if r["grade"] == "SKIP")

    lines = [
        "# Vanishing Point Lint Report",
        f"**Tool:** LTG_TOOL_vanishing_point_lint.py v{__version__}",
        "",
        "## Summary",
        f"| Grade | Count |",
        f"|---|---|",
        f"| PASS  | {pass_count} |",
        f"| WARN  | {warn_count} |",
        f"| FAIL  | {fail_count} |",
        f"| SKIP  | {skip_count} |",
        f"| **Total** | **{total}** |",
        "",
        "## Results",
        "",
    ]

    for r in results:
        grade = r["grade"]
        if grade == "PASS" and not include_pass:
            continue
        if grade == "SKIP":
            lines.append(f"### SKIP — `{os.path.basename(r['file'])}`")
            lines.append(f"  Reason: {r.get('skipped_reason', 'unknown')}")
            lines.append("")
            continue

        lines.append(f"### {grade} — `{os.path.basename(r['file'])}`")
        lines.append(f"  Scene type: {r.get('scene_type', '?')}")
        if r.get("vp_azimuth_pct") is not None:
            lines.append(f"  VP azimuth: {r['vp_azimuth_pct']:+.3f}  (±{REAL_WORLD_VP_TOLERANCE:.2f} = center 30%)")
        if r.get("dominant_angle_deg") is not None:
            lines.append(f"  Dominant edge angle: {r['dominant_angle_deg']:.1f}°")
        if r.get("magnitude_mean") is not None:
            lines.append(f"  Magnitude mean: {r['magnitude_mean']:.2f}  |  Strong px: {r.get('strong_pct', 0):.1%}")
        for issue in r.get("issues", []):
            if not include_info and issue.startswith("VP003"):
                continue
            lines.append(f"  - {issue}")
        lines.append("")

    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

def _cli():
    import argparse
    parser = argparse.ArgumentParser(
        description="LTG_TOOL_vanishing_point_lint.py — VP perspective linter"
    )
    parser.add_argument("targets", nargs="*",
                        help="PNG file(s) or directory to lint")
    parser.add_argument("--scene-type", choices=["REAL_WORLD", "GLITCH_LAYER"],
                        help="Override scene type classification")
    parser.add_argument("--save-report", metavar="PATH",
                        help="Save Markdown report to this path")
    parser.add_argument("--no-pass", action="store_true",
                        help="Omit PASS results from report")
    parser.add_argument("--no-info", action="store_true",
                        help="Omit VP003 INFO lines from report")
    args = parser.parse_args()

    if not _NP_AVAILABLE:
        print("ERROR: numpy is required but not available. Install numpy to use this tool.")
        sys.exit(2)

    if not args.targets:
        # Default: scan style frames directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        default_dir = os.path.join(os.path.dirname(script_dir), "color", "style_frames")
        args.targets = [default_dir]

    results = []
    for target in args.targets:
        if os.path.isdir(target):
            results.extend(lint_directory(target, scene_type=args.scene_type))
        elif os.path.isfile(target):
            results.append(lint_file(target, scene_type=args.scene_type))
        else:
            print(f"WARNING: target not found: {target}")

    report = format_report(results,
                           include_pass=not args.no_pass,
                           include_info=not args.no_info)
    print(report)

    if args.save_report:
        os.makedirs(os.path.dirname(os.path.abspath(args.save_report)), exist_ok=True)
        with open(args.save_report, "w", encoding="utf-8") as fh:
            fh.write(report)
        print(f"Report saved to: {args.save_report}")

    fail_count = sum(1 for r in results if r["grade"] == "FAIL")
    warn_count = sum(1 for r in results if r["grade"] == "WARN")
    if fail_count > 0:
        sys.exit(2)
    elif warn_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    _cli()
