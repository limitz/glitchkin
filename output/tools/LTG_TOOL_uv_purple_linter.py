# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_uv_purple_linter.py
=================================
UV_PURPLE Dominance Linter for "Luma & the Glitchkin."

Verifies that UV_PURPLE (#7B2FBE) and ELEC_CYAN (#00F0FF) collectively dominate
the non-black pixel area in Glitch Layer images. This enforces the core world-rule:

    Glitch Layer = UV_PURPLE + ELEC_CYAN dominant, zero warm light.
    Real World   = warm palette dominant.

The linter also flags warm-hue contamination (LAB hue 30°–80°) in Glitch Layer images.

Checks (Glitch Layer images only):
  A. UV_PURPLE + ELEC_CYAN Dominance
       Pixels within LAB ΔE ≤ 15 of UV_PURPLE (#7B2FBE) or ELEC_CYAN (#00F0FF)
       as a fraction of non-black pixels (VOID_BLACK: per-channel value < 20).
       PASS  ≥ 20%
       WARN  10–19%
       FAIL  < 10%
  B. Warm-Hue Contamination
       Pixels with LAB hue angle h° in [30°, 80°] as a fraction of ALL pixels.
       PASS  < 5%
       WARN  ≥ 5%  (WARN only — warm contamination does not FAIL on its own)

Images inferred as non-GLITCH world type are skipped (informational note only).
Override world type with --world-type glitch.

Usage:
    python LTG_TOOL_uv_purple_linter.py path/to/image.png
    python LTG_TOOL_uv_purple_linter.py path/to/image.png --world-type glitch
    python LTG_TOOL_uv_purple_linter.py --batch output/color/style_frames/
    python LTG_TOOL_uv_purple_linter.py --batch output/color/style_frames/ --world-type glitch

Module API:
    from LTG_TOOL_uv_purple_linter import lint_uv_purple_dominance, batch_lint

Author: Rin Yamamoto (Procedural Art Engineer) — Cycle 44
Version: 1.0.0

Changelog:
  1.0.0 (Cycle 44): Initial implementation. Requested by Alex Chen C44 brief.
                    Check A: UV_PURPLE + ELEC_CYAN pixel fraction (LAB ΔE ≤ 15).
                    Check B: Warm-hue contamination (LAB h° 30°–80°).
                    Module API + CLI (single file + batch).
                    Integrates with LTG_TOOL_world_type_infer.py.
                    Fallback: numpy-only path when cv2 unavailable.
"""

from __future__ import annotations

import os
import sys
import math
import glob
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Optional dependencies
# ---------------------------------------------------------------------------

try:
    from PIL import Image
    _PIL_AVAILABLE = True
except ImportError:
    _PIL_AVAILABLE = False

try:
    import numpy as np
    _NP_AVAILABLE = True
except ImportError:
    np = None  # type: ignore
    _NP_AVAILABLE = False

try:
    import cv2
    _CV2_AVAILABLE = True
except ImportError:
    cv2 = None  # type: ignore
    _CV2_AVAILABLE = False

__version__ = "1.0.0"
__author__  = "Rin Yamamoto"

# ---------------------------------------------------------------------------
# Canonical palette references
# ---------------------------------------------------------------------------

UV_PURPLE_RGB  = (123, 47, 190)   # GL-04  #7B2FBE
ELEC_CYAN_RGB  = (0, 240, 255)    # GL-01a #00F0FF

# VOID_BLACK threshold: pixels with max(R,G,B) < this are treated as void/black.
# Uses max-channel (HSV Value) so very dark near-black pixels (e.g. (13,10,25))
# are correctly excluded even when one channel slightly exceeds the per-channel floor.
VOID_BLACK_THRESHOLD = 30

# LAB ΔE threshold for colour matching
LAB_DE_THRESHOLD = 15.0

# Dominance thresholds (fraction of non-black pixels)
DOMINANCE_PASS_FRAC  = 0.20   # ≥ 20%
DOMINANCE_WARN_FRAC  = 0.10   # ≥ 10%, < 20%
# < 10% → FAIL

# Warm-hue contamination threshold (fraction of ALL pixels)
WARM_FRAC_WARN = 0.05   # ≥ 5% → WARN

# Warm hue range in LAB (LCH hue angle, degrees)
WARM_HUE_MIN = 30.0
WARM_HUE_MAX = 80.0

# Minimum LAB chroma (C* = sqrt(a*² + b*²)) required for a pixel's hue angle to be
# considered reliable. Near-neutral dark pixels have near-zero chroma; their hue
# angles are numerically unstable and should not contribute to the warm-hue check.
WARM_HUE_MIN_CHROMA = 8.0

# ---------------------------------------------------------------------------
# Colour conversion helpers
# ---------------------------------------------------------------------------

def _rgb_to_lab_numpy(rgb_array: "np.ndarray") -> "np.ndarray":
    """
    Convert an (N, 3) uint8 RGB array to an (N, 3) float32 LAB array.

    Uses cv2 if available (accurate, uses D65 illuminant).
    Falls back to a pure-numpy sRGB→XYZ→LAB approximation otherwise.

    Parameters
    ----------
    rgb_array : np.ndarray of shape (N, 3), dtype uint8
        Each row is (R, G, B) in 0–255.

    Returns
    -------
    np.ndarray of shape (N, 3), dtype float32
        Each row is (L*, a*, b*) in OpenCV LAB scale
        (L: 0–100 in cv2 convention, a/b: ±127).
    """
    if _CV2_AVAILABLE:
        # cv2 expects BGR uint8 image; reshape to (1, N, 3) for batch conversion
        bgr = rgb_array[:, ::-1].astype(np.uint8)  # RGB → BGR
        bgr_img = bgr.reshape(1, -1, 3)
        lab_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2LAB)
        lab_raw = lab_img.reshape(-1, 3).astype(np.float32)
        # cv2 LAB is 8-bit scaled: L in [0,255]→[0,100]; a,b in [0,255]→[-128,127].
        # Convert to standard CIELAB scale so ΔE, chroma, and hue calculations are correct.
        lab_standard = np.empty_like(lab_raw)
        lab_standard[:, 0] = lab_raw[:, 0] * (100.0 / 255.0)   # L: 0-255 → 0-100
        lab_standard[:, 1] = lab_raw[:, 1] - 128.0              # a: 0-255 → -128 to 127
        lab_standard[:, 2] = lab_raw[:, 2] - 128.0              # b: 0-255 → -128 to 127
        return lab_standard
    else:
        # Pure numpy sRGB → XYZ D65 → CIELAB
        # Linearise sRGB
        rgb_f = rgb_array.astype(np.float32) / 255.0
        mask = rgb_f > 0.04045
        rgb_lin = np.where(mask, ((rgb_f + 0.055) / 1.055) ** 2.4, rgb_f / 12.92)

        # XYZ (D65 illuminant, sRGB matrix)
        M = np.array([
            [0.4124564, 0.3575761, 0.1804375],
            [0.2126729, 0.7151522, 0.0721750],
            [0.0193339, 0.1191920, 0.9503041],
        ], dtype=np.float32)
        xyz = rgb_lin @ M.T   # (N, 3)

        # Normalise by D65 white point
        xyz /= np.array([0.95047, 1.00000, 1.08883], dtype=np.float32)

        # f(t) function
        delta = 6.0 / 29.0
        f = np.where(xyz > delta ** 3,
                     np.cbrt(xyz),
                     xyz / (3 * delta ** 2) + 4.0 / 29.0)

        L_star = 116.0 * f[:, 1] - 16.0          # 0–100
        a_star = 500.0 * (f[:, 0] - f[:, 1])      # ±127
        b_star = 200.0 * (f[:, 1] - f[:, 2])      # ±127

        return np.stack([L_star, a_star, b_star], axis=1).astype(np.float32)


def _lab_de76(lab_a: "np.ndarray", lab_b_ref: "np.ndarray") -> "np.ndarray":
    """
    Compute CIE76 ΔE between each row of lab_a and a single reference lab_b_ref.

    Parameters
    ----------
    lab_a     : (N, 3) float32
    lab_b_ref : (3,) float32

    Returns
    -------
    (N,) float32 — ΔE per pixel
    """
    diff = lab_a - lab_b_ref[np.newaxis, :]
    return np.sqrt(np.sum(diff ** 2, axis=1))


def _lab_hue_angle(lab_array: "np.ndarray") -> "np.ndarray":
    """
    Compute the LCH hue angle h° (0–360) for each LAB pixel.

    h° = atan2(b*, a*) converted to degrees, then shifted to [0, 360).

    Parameters
    ----------
    lab_array : (N, 3) float32 — columns L, a, b

    Returns
    -------
    (N,) float32 — hue angle in degrees [0, 360)
    """
    a_star = lab_array[:, 1]
    b_star = lab_array[:, 2]
    h = np.degrees(np.arctan2(b_star, a_star))
    h = h % 360.0
    return h.astype(np.float32)


# ---------------------------------------------------------------------------
# Reference LAB values
# ---------------------------------------------------------------------------

def _precompute_ref_lab() -> Tuple["np.ndarray", "np.ndarray"]:
    """Return LAB reference values for UV_PURPLE and ELEC_CYAN."""
    refs = np.array([UV_PURPLE_RGB, ELEC_CYAN_RGB], dtype=np.uint8)
    lab_refs = _rgb_to_lab_numpy(refs)   # (2, 3)
    return lab_refs[0], lab_refs[1]      # UV_PURPLE_LAB, ELEC_CYAN_LAB


# ---------------------------------------------------------------------------
# Core lint function
# ---------------------------------------------------------------------------

def lint_uv_purple_dominance(
    image_path: str,
    world_type_override: Optional[str] = None,
) -> Dict:
    """
    Run the UV_PURPLE dominance lint on a single image.

    Parameters
    ----------
    image_path : str
        Path to a PNG (or any PIL-readable) image.
    world_type_override : str | None
        If provided ("glitch", "GLITCH", "other_side", etc.), overrides the
        world-type inferred from the filename.
        Pass "glitch" to force Glitch Layer checks on any image.
        Pass "skip" to force non-GLITCH (skip lint).

    Returns
    -------
    dict with keys:
        path          : str — absolute path
        basename      : str — filename
        world_type    : str | None — inferred or overridden world type
        skipped       : bool — True if image is not Glitch Layer world type
        skip_reason   : str | None
        checks        : list of check result dicts (when not skipped)
        overall       : "PASS" | "WARN" | "FAIL" | "SKIP"
        error         : str | None — if exception during lint
    """
    abs_path = os.path.abspath(image_path)
    basename = os.path.basename(abs_path)

    result: Dict = {
        "path":       abs_path,
        "basename":   basename,
        "world_type": None,
        "skipped":    False,
        "skip_reason": None,
        "checks":     [],
        "overall":    "SKIP",
        "error":      None,
    }

    # Determine world type
    if world_type_override is not None:
        override_norm = world_type_override.upper()
        if override_norm in ("GLITCH", "GLITCH_LAYER"):
            result["world_type"] = "GLITCH"
        elif override_norm in ("OTHER_SIDE", "OTHERSIDE"):
            result["world_type"] = "OTHER_SIDE"
        elif override_norm == "SKIP":
            result["world_type"] = "SKIP"
        else:
            result["world_type"] = override_norm
    else:
        try:
            # Try to import world_type_infer
            _tools_dir = Path(__file__).resolve().parent
            if str(_tools_dir) not in sys.path:
                sys.path.insert(0, str(_tools_dir))
            from LTG_TOOL_world_type_infer import infer_world_type
            result["world_type"] = infer_world_type(abs_path)
        except ImportError:
            result["world_type"] = None

    # Only run checks on Glitch Layer images
    wt = result["world_type"]
    if wt not in ("GLITCH",):
        result["skipped"] = True
        if wt is None:
            result["skip_reason"] = "World type unknown — not a recognised Glitch Layer asset"
        elif wt == "OTHER_SIDE":
            result["skip_reason"] = "OTHER_SIDE world — UV_PURPLE rules differ; dominance lint skipped"
        else:
            result["skip_reason"] = f"World type {wt!r} — not a Glitch Layer asset"
        result["overall"] = "SKIP"
        return result

    # Dependency check
    if not _PIL_AVAILABLE:
        result["error"] = "PIL/Pillow not available — cannot load image"
        result["overall"] = "FAIL"
        return result
    if not _NP_AVAILABLE:
        result["error"] = "NumPy not available — cannot run pixel analysis"
        result["overall"] = "FAIL"
        return result

    # Load image
    try:
        img = Image.open(abs_path).convert("RGB")
    except Exception as exc:
        result["error"] = f"Cannot open image: {exc}"
        result["overall"] = "FAIL"
        return result

    # Flatten to (N, 3) uint8 array
    pixels_rgb = np.array(img, dtype=np.uint8).reshape(-1, 3)
    total_pixels = len(pixels_rgb)

    if total_pixels == 0:
        result["error"] = "Image has zero pixels"
        result["overall"] = "FAIL"
        return result

    # Convert to LAB
    pixels_lab = _rgb_to_lab_numpy(pixels_rgb)

    # Precompute reference LAB values
    uv_purple_lab, elec_cyan_lab = _precompute_ref_lab()

    # ------------------------------------------------------------------
    # Check A: UV_PURPLE + ELEC_CYAN Dominance
    # ------------------------------------------------------------------

    # Identify void/black pixels: max(R,G,B) < VOID_BLACK_THRESHOLD.
    # Using max-channel (HSV Value) captures dark near-neutral pixels like (13,10,25)
    # whose dominant channel may slightly exceed a per-channel floor.
    is_void = np.max(pixels_rgb, axis=1) < VOID_BLACK_THRESHOLD   # (N,) bool
    non_black_mask = ~is_void
    non_black_count = int(np.sum(non_black_mask))

    if non_black_count == 0:
        check_a = {
            "check":   "A",
            "name":    "UV_PURPLE + ELEC_CYAN Dominance",
            "verdict": "WARN",
            "msg":     "All pixels are void/black — no non-black pixels to measure dominance.",
            "uv_purple_frac":   0.0,
            "elec_cyan_frac":   0.0,
            "combined_frac":    0.0,
            "non_black_pixels": 0,
        }
    else:
        # Compute ΔE for UV_PURPLE and ELEC_CYAN on all pixels
        de_uv    = _lab_de76(pixels_lab, uv_purple_lab)
        de_cyan  = _lab_de76(pixels_lab, elec_cyan_lab)

        # Pixels matching either reference (within threshold)
        match_uv   = de_uv   <= LAB_DE_THRESHOLD    # (N,) bool
        match_cyan = de_cyan <= LAB_DE_THRESHOLD

        # Combined match (union)
        match_combined = match_uv | match_cyan

        # Count only among non-black pixels
        non_black_match_uv   = int(np.sum(match_uv   & non_black_mask))
        non_black_match_cyan = int(np.sum(match_cyan & non_black_mask))
        non_black_match_both = int(np.sum(match_combined & non_black_mask))

        uv_frac       = non_black_match_uv   / non_black_count
        cyan_frac     = non_black_match_cyan / non_black_count
        combined_frac = non_black_match_both / non_black_count

        if combined_frac >= DOMINANCE_PASS_FRAC:
            verdict_a = "PASS"
            msg_a = (
                f"Combined UV_PURPLE+ELEC_CYAN = {combined_frac:.1%} of non-black pixels "
                f"(UV_PURPLE={uv_frac:.1%}, ELEC_CYAN={cyan_frac:.1%}). ≥ 20% — PASS."
            )
        elif combined_frac >= DOMINANCE_WARN_FRAC:
            verdict_a = "WARN"
            msg_a = (
                f"Combined UV_PURPLE+ELEC_CYAN = {combined_frac:.1%} of non-black pixels "
                f"(UV_PURPLE={uv_frac:.1%}, ELEC_CYAN={cyan_frac:.1%}). 10–19% — WARN. "
                f"Glitch Layer scenes should have stronger UV_PURPLE/ELEC_CYAN presence."
            )
        else:
            verdict_a = "FAIL"
            msg_a = (
                f"Combined UV_PURPLE+ELEC_CYAN = {combined_frac:.1%} of non-black pixels "
                f"(UV_PURPLE={uv_frac:.1%}, ELEC_CYAN={cyan_frac:.1%}). < 10% — FAIL. "
                f"Structural violation: Glitch Layer must be UV_PURPLE+ELEC_CYAN dominant."
            )

        check_a = {
            "check":             "A",
            "name":              "UV_PURPLE + ELEC_CYAN Dominance",
            "verdict":           verdict_a,
            "msg":               msg_a,
            "uv_purple_frac":    round(uv_frac, 4),
            "elec_cyan_frac":    round(cyan_frac, 4),
            "combined_frac":     round(combined_frac, 4),
            "non_black_pixels":  non_black_count,
            "total_pixels":      total_pixels,
        }

    result["checks"].append(check_a)

    # ------------------------------------------------------------------
    # Check B: Warm-Hue Contamination
    # ------------------------------------------------------------------

    hue_angles = _lab_hue_angle(pixels_lab)   # (N,) float32, degrees [0, 360)

    # Compute LAB chroma for each pixel: C* = sqrt(a*² + b*²)
    chroma = np.sqrt(pixels_lab[:, 1] ** 2 + pixels_lab[:, 2] ** 2)

    # Warm hue: 30°–80° in LAB hue, but only for pixels with sufficient chroma.
    # Near-neutral dark pixels have near-zero chroma and numerically unstable hue
    # angles that must not be counted as warm-hue contamination.
    chromatic_mask = chroma >= WARM_HUE_MIN_CHROMA
    warm_mask = (
        chromatic_mask
        & (hue_angles >= WARM_HUE_MIN)
        & (hue_angles <= WARM_HUE_MAX)
    )
    warm_count = int(np.sum(warm_mask))
    warm_frac  = warm_count / total_pixels

    if warm_frac >= WARM_FRAC_WARN:
        verdict_b = "WARN"
        msg_b = (
            f"Warm-hue pixels (LAB h° {WARM_HUE_MIN:.0f}°–{WARM_HUE_MAX:.0f}°, "
            f"chroma C* ≥ {WARM_HUE_MIN_CHROMA:.0f}) = "
            f"{warm_frac:.1%} of total pixels ({warm_count}/{total_pixels}). "
            f"≥ 5% — WARN. Glitch Layer images should have near-zero warm light."
        )
    else:
        verdict_b = "PASS"
        msg_b = (
            f"Warm-hue pixels (LAB h° {WARM_HUE_MIN:.0f}°–{WARM_HUE_MAX:.0f}°, "
            f"chroma C* ≥ {WARM_HUE_MIN_CHROMA:.0f}) = "
            f"{warm_frac:.1%} of total pixels ({warm_count}/{total_pixels}). "
            f"< 5% — PASS."
        )

    check_b = {
        "check":       "B",
        "name":        "Warm-Hue Contamination",
        "verdict":     verdict_b,
        "msg":         msg_b,
        "warm_frac":   round(warm_frac, 4),
        "warm_pixels": warm_count,
        "total_pixels": total_pixels,
    }
    result["checks"].append(check_b)

    # ------------------------------------------------------------------
    # Overall verdict
    # ------------------------------------------------------------------
    verdicts = [c["verdict"] for c in result["checks"]]
    if "FAIL" in verdicts:
        result["overall"] = "FAIL"
    elif "WARN" in verdicts:
        result["overall"] = "WARN"
    else:
        result["overall"] = "PASS"

    return result


# ---------------------------------------------------------------------------
# Batch lint
# ---------------------------------------------------------------------------

def batch_lint(
    directory_or_paths,
    world_type_override: Optional[str] = None,
    extensions: Tuple[str, ...] = (".png",),
) -> Dict:
    """
    Run UV_PURPLE dominance lint on all PNG files in a directory.

    Parameters
    ----------
    directory_or_paths : str | list[str]
        Directory path or explicit list of file paths.
    world_type_override : str | None
        Passed through to lint_uv_purple_dominance() for every file.
    extensions : tuple[str, ...]
        File extensions to include. Default: (".png",)

    Returns
    -------
    dict with keys:
        directory    : str | None
        results      : list of per-file result dicts
        summary      : dict — overall counts and verdict
    """
    if isinstance(directory_or_paths, str) and os.path.isdir(directory_or_paths):
        directory = directory_or_paths
        paths = sorted([
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if os.path.splitext(f)[1].lower() in extensions
        ])
    else:
        directory = None
        paths = list(directory_or_paths)

    results = []
    counts: Dict[str, int] = {"PASS": 0, "WARN": 0, "FAIL": 0, "SKIP": 0}

    for p in paths:
        r = lint_uv_purple_dominance(p, world_type_override=world_type_override)
        results.append(r)
        overall = r.get("overall", "SKIP")
        counts[overall] = counts.get(overall, 0) + 1

    # Worst grade (ignoring SKIPs)
    if counts.get("FAIL", 0) > 0:
        batch_overall = "FAIL"
    elif counts.get("WARN", 0) > 0:
        batch_overall = "WARN"
    elif counts.get("PASS", 0) > 0:
        batch_overall = "PASS"
    else:
        batch_overall = "SKIP"

    return {
        "directory": directory,
        "results":   results,
        "summary": {
            "overall": batch_overall,
            "pass":    counts.get("PASS", 0),
            "warn":    counts.get("WARN", 0),
            "fail":    counts.get("FAIL", 0),
            "skip":    counts.get("SKIP", 0),
            "total":   len(results),
        },
    }


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

_VERDICT_BADGES = {
    "PASS": "[PASS]",
    "WARN": "[WARN]",
    "FAIL": "[FAIL]",
    "SKIP": "[SKIP]",
}


def format_result(result: Dict, verbose: bool = True) -> str:
    """Format a single file lint result as a human-readable string."""
    lines = []
    badge = _VERDICT_BADGES.get(result["overall"], result["overall"])
    lines.append(f"{badge}  {result['basename']}")
    if result.get("world_type"):
        lines.append(f"       world_type : {result['world_type']}")
    if result.get("skipped"):
        lines.append(f"       SKIP — {result.get('skip_reason', '')}")
        return "\n".join(lines)
    if result.get("error"):
        lines.append(f"       ERROR — {result['error']}")
        return "\n".join(lines)
    for check in result.get("checks", []):
        cv = _VERDICT_BADGES.get(check["verdict"], check["verdict"])
        lines.append(f"       Check {check['check']} ({check['name']}): {cv}")
        if verbose:
            lines.append(f"         {check['msg']}")
    return "\n".join(lines)


def format_batch_report(batch: Dict) -> str:
    """Format a batch lint report as a human-readable string."""
    lines = []
    summary = batch["summary"]
    src = batch.get("directory") or "explicit paths"
    lines.append(f"UV_PURPLE Dominance Linter — Batch Report")
    lines.append(f"Source: {src}")
    lines.append(
        f"Overall: {summary['overall']}  "
        f"PASS={summary['pass']}  WARN={summary['warn']}  "
        f"FAIL={summary['fail']}  SKIP={summary['skip']}  "
        f"(total {summary['total']} files)"
    )
    lines.append("")
    for r in batch["results"]:
        lines.append(format_result(r, verbose=True))
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Precritique QA module API
# ---------------------------------------------------------------------------
# These functions are called by LTG_TOOL_precritique_qa.py Section 11.

def run_glitch_layer_dominance_check(glitch_png_paths: List[str]) -> Dict:
    """
    Section 11 runner: UV_PURPLE dominance check on a specific list of Glitch Layer PNGs.

    World type override = "GLITCH" is applied to all paths (they are pre-selected Glitch Layer).

    Parameters
    ----------
    glitch_png_paths : list[str]
        Absolute paths to Glitch Layer rendered PNGs.

    Returns
    -------
    dict with keys:
        overall     : "PASS" | "WARN" | "FAIL"
        pass        : int
        warn        : int
        fail        : int
        skip        : int
        per_file    : list of per-file result dicts
    """
    results = []
    counts: Dict[str, int] = {"PASS": 0, "WARN": 0, "FAIL": 0, "SKIP": 0}

    for p in glitch_png_paths:
        r = lint_uv_purple_dominance(str(p), world_type_override="GLITCH")
        results.append(r)
        overall = r.get("overall", "SKIP")
        counts[overall] = counts.get(overall, 0) + 1

    if counts.get("FAIL", 0) > 0:
        overall = "FAIL"
    elif counts.get("WARN", 0) > 0:
        overall = "WARN"
    elif counts.get("PASS", 0) > 0:
        overall = "PASS"
    else:
        overall = "SKIP"

    return {
        "overall":  overall,
        "pass":     counts.get("PASS", 0),
        "warn":     counts.get("WARN", 0),
        "fail":     counts.get("FAIL", 0),
        "skip":     counts.get("SKIP", 0),
        "per_file": results,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli(argv: List[str]) -> int:
    """CLI entry point."""
    if not argv:
        print(f"LTG_TOOL_uv_purple_linter  v{__version__}")
        print("Usage:")
        print("  python LTG_TOOL_uv_purple_linter.py <image.png> [--world-type glitch]")
        print("  python LTG_TOOL_uv_purple_linter.py --batch <directory/> [--world-type glitch]")
        return 0

    world_type_override: Optional[str] = None
    if "--world-type" in argv:
        idx = argv.index("--world-type")
        if idx + 1 < len(argv):
            world_type_override = argv[idx + 1]
            argv = argv[:idx] + argv[idx + 2:]
        else:
            print("ERROR: --world-type requires an argument (e.g. glitch)", file=sys.stderr)
            return 2

    # --batch mode
    if "--batch" in argv:
        idx = argv.index("--batch")
        if idx + 1 >= len(argv):
            print("ERROR: --batch requires a directory argument", file=sys.stderr)
            return 2
        directory = argv[idx + 1]
        if not os.path.isdir(directory):
            print(f"ERROR: Not a directory: {directory}", file=sys.stderr)
            return 2
        batch = batch_lint(directory, world_type_override=world_type_override)
        print(format_batch_report(batch))
        summary = batch["summary"]
        if summary["overall"] == "FAIL":
            return 2
        elif summary["overall"] == "WARN":
            return 1
        return 0

    # Single file mode
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print("ERROR: No image path provided.", file=sys.stderr)
        return 2

    exit_code = 0
    for p in paths:
        if not os.path.isfile(p):
            print(f"ERROR: File not found: {p}", file=sys.stderr)
            exit_code = 2
            continue
        result = lint_uv_purple_dominance(p, world_type_override=world_type_override)
        print(format_result(result, verbose=True))
        print()
        if result["overall"] == "FAIL":
            exit_code = max(exit_code, 2)
        elif result["overall"] == "WARN":
            exit_code = max(exit_code, 1)

    return exit_code


if __name__ == "__main__":
    sys.exit(_cli(sys.argv[1:]))
