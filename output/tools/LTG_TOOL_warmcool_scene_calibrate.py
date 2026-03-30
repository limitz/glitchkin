# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_warmcool_scene_calibrate.py
=====================================
Warm/Cool Scene Calibration Tool for "Luma & the Glitchkin."

Measures warm/cool metrics in real-world reference photos and outputs
empirically validated threshold values for the production pipeline.

Two metrics measured per image:
  1. Hue-split separation: median PIL HSV hue of top half vs bottom half,
     circular distance on 0-255 scale (render_qa _check_warm_cool() metric).
  2. Warm-pixel-percentage: fraction of chromatic pixels with PIL HSV hue
     in the warm range (0-42 or 213-255). Added C48.

Additionally reports:
- Warm pixel percentage (hue 0-42 or 213-255 on PIL scale, i.e. reds/oranges/yellows)
- Cool pixel percentage (hue 85-170 on PIL scale, i.e. cyans/blues)
- Neutral pixel percentage (remainder, including achromatics with sat < 0.05)
- Per-image verdict: VALIDATES threshold / CHALLENGES threshold
- Empirical threshold recommendations (--output-thresholds mode)

Author: Sam Kowalski (Color & Style Artist)
Created: Cycle 46 — 2026-03-30
Updated: Cycle 49 — 2026-03-30 (sigmoid profile measurement, BG saturation drop)
Version: 3.0.0

v3.0.0 additions:
  - measure_sigmoid_profile(): samples warm_pct in N horizontal bands across
    the FG-BG span, compares measured warm→cool falloff against the sigmoid
    expectation from docs/image-rules.md, reports per-band deviation and
    overall PASS/WARN/FAIL.
  - measure_saturation_drop(): measures mean saturation in FG and BG bands,
    reports the drop ratio (BG/FG). Target: 0.75-0.85 per image-rules.md.
  - CLI --sigmoid-profile mode with --fg-y, --bg-y, --steepness, --bands.
  - analyze_image() now optionally includes sigmoid and saturation data.

Previous versions: see v2.0.0 docstring below.

Usage:
  # Single image
  python3 LTG_TOOL_warmcool_scene_calibrate.py path/to/photo.jpg

  # Batch directory
  python3 LTG_TOOL_warmcool_scene_calibrate.py --batch "reference/kitchen predawn"

  # Multiple directories
  python3 LTG_TOOL_warmcool_scene_calibrate.py --batch "reference/kitchen predawn" --batch "reference/living room night"

  # Write calibration report
  python3 LTG_TOOL_warmcool_scene_calibrate.py --batch "reference/kitchen predawn" --batch "reference/living room night" --report output/production/warmcool_calibration_report.md

  # Output threshold values (JSON to stdout)
  python3 LTG_TOOL_warmcool_scene_calibrate.py --batch "reference/living room night" --batch "reference/kitchen predawn" --output-thresholds

Dependencies: PIL/Pillow, NumPy (both authorized per pil-standards.md)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
from PIL import Image

# ---------------------------------------------------------------------------
# Constants — must match render_qa _check_warm_cool() metric
# ---------------------------------------------------------------------------

# REAL_INTERIOR threshold from render_qa v1.6.0 / warmth_lint_v004 world_presets
REAL_INTERIOR_THRESHOLD = 12.0  # PIL hue units

# Additional thresholds for context
REAL_STORM_THRESHOLD = 3.0
GLITCH_THRESHOLD = 3.0
OTHER_SIDE_THRESHOLD = 0.0

# PIL HSV hue ranges (0–255 scale)
# Warm: reds, oranges, yellows — hue 0–42 and 213–255 (wraps around red)
# Cool: cyans, blues — hue 85–170
# Neutral: everything else (greens, purples, and achromatics)
WARM_HUE_LOW = 42     # upper bound of warm range (low end)
WARM_HUE_HIGH = 213   # lower bound of warm range (high end, wrapping)
COOL_HUE_LOW = 85     # lower bound of cool range
COOL_HUE_HIGH = 170   # upper bound of cool range

# Minimum saturation to count as chromatic (matches render_qa)
MIN_SATURATION = 0.05

def _override_threshold(value: float) -> None:
    """Override the REAL_INTERIOR threshold (used by CLI --threshold flag)."""
    global REAL_INTERIOR_THRESHOLD
    REAL_INTERIOR_THRESHOLD = value


# Supported image extensions
SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
# AVIF is NOT supported by PIL without pillow-avif — skip gracefully
UNSUPPORTED_EXTS = {".avif"}


# ---------------------------------------------------------------------------
# Core metric — mirrors render_qa _check_warm_cool() exactly
# ---------------------------------------------------------------------------

def measure_warm_cool_separation(img: Image.Image) -> Dict:
    """
    Measure warm/cool separation using the same metric as render_qa.

    Returns dict with:
        zone_a_hue: float — median hue of top half (PIL 0–255)
        zone_b_hue: float — median hue of bottom half (PIL 0–255)
        separation: float — circular hue distance (PIL units)
        threshold: float — REAL_INTERIOR threshold for comparison
        validates_threshold: bool — True if separation >= threshold
    """
    rgb = img.convert("RGB")
    w, h = rgb.size

    arr = np.array(rgb, dtype=np.float32) / 255.0  # (H, W, 3)

    def _np_median_hue(region: np.ndarray) -> float:
        """Compute median hue of chromatic pixels in a region. Returns -1 if achromatic."""
        r, g, b = region[:, :, 0], region[:, :, 1], region[:, :, 2]
        cmax = np.maximum(np.maximum(r, g), b)
        cmin = np.minimum(np.minimum(r, g), b)
        delta = cmax - cmin

        # Saturation (avoid div/0)
        cmax_safe = np.where(cmax > 0, cmax, 1.0)
        sat = np.where(cmax > 0, delta / cmax_safe, 0.0)
        chromatic = sat >= MIN_SATURATION

        if not np.any(chromatic):
            return -1.0

        # Hue calculation for chromatic pixels only
        rc = r[chromatic]
        gc = g[chromatic]
        bc = b[chromatic]
        cm = cmax[chromatic]
        d = delta[chromatic]

        hue = np.zeros_like(d)

        r_mask = cm == rc
        g_mask = (~r_mask) & (cm == gc)
        b_mask = (~r_mask) & (~g_mask)

        hue[r_mask] = ((gc[r_mask] - bc[r_mask]) / d[r_mask]) % 6.0
        hue[g_mask] = ((bc[g_mask] - rc[g_mask]) / d[g_mask]) + 2.0
        hue[b_mask] = ((rc[b_mask] - gc[b_mask]) / d[b_mask]) + 4.0

        # Convert to PIL 0–255 scale (hue is 0–6, map to 0–255)
        hue_pil = (hue / 6.0) * 255.0
        return float(np.median(hue_pil))

    mid = h // 2
    top_arr = arr[:mid, :, :]
    bot_arr = arr[mid:, :, :]

    hue_a = _np_median_hue(top_arr)
    hue_b = _np_median_hue(bot_arr)

    if hue_a < 0 or hue_b < 0:
        return {
            "zone_a_hue": hue_a,
            "zone_b_hue": hue_b,
            "separation": 0.0,
            "threshold": REAL_INTERIOR_THRESHOLD,
            "validates_threshold": True,  # achromatic — not a meaningful test
            "achromatic": True,
            "notes": "One or both zones are achromatic — measurement not meaningful",
        }

    # Circular distance on 0–255 scale (same as render_qa)
    delta = abs(hue_a - hue_b)
    if delta > 127.5:
        delta = 255.0 - delta
    separation = delta

    validates = separation >= REAL_INTERIOR_THRESHOLD

    return {
        "zone_a_hue": round(hue_a, 2),
        "zone_b_hue": round(hue_b, 2),
        "separation": round(separation, 2),
        "threshold": REAL_INTERIOR_THRESHOLD,
        "validates_threshold": validates,
        "achromatic": False,
        "notes": "",
    }


# ---------------------------------------------------------------------------
# Extended analysis — warm/cool pixel breakdown
# ---------------------------------------------------------------------------

def measure_warm_cool_pixels(img: Image.Image) -> Dict:
    """
    Count warm, cool, and neutral pixels in the full image.

    Returns dict with:
        warm_pct: float — percentage of chromatic warm pixels
        cool_pct: float — percentage of chromatic cool pixels
        neutral_pct: float — percentage of neutral/achromatic pixels
        warm_count: int
        cool_count: int
        neutral_count: int
        total_pixels: int
        warm_cool_ratio: float — warm_count / cool_count (inf if cool_count == 0)
    """
    rgb = img.convert("RGB")
    arr = np.array(rgb, dtype=np.float32) / 255.0  # (H, W, 3)

    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    cmax = np.maximum(np.maximum(r, g), b)
    cmin = np.minimum(np.minimum(r, g), b)
    delta = cmax - cmin
    cmax_safe = np.where(cmax > 0, cmax, 1.0)
    sat = np.where(cmax > 0, delta / cmax_safe, 0.0)

    chromatic = sat >= MIN_SATURATION

    # Hue for chromatic pixels
    hue = np.zeros_like(delta)
    r_mask = chromatic & (cmax == r)
    g_mask = chromatic & (~r_mask) & (cmax == g)
    b_mask = chromatic & (~r_mask) & (~g_mask) & (cmax == b)

    d_safe = np.where(delta > 0, delta, 1.0)  # avoid div/0
    hue[r_mask] = (((g[r_mask] - b[r_mask]) / d_safe[r_mask]) % 6.0)
    hue[g_mask] = (((b[g_mask] - r[g_mask]) / d_safe[g_mask]) + 2.0)
    hue[b_mask] = (((r[b_mask] - g[b_mask]) / d_safe[b_mask]) + 4.0)

    # Convert to PIL 0–255 scale
    hue_pil = (hue / 6.0) * 255.0

    # Warm: hue 0–42 or 213–255 (reds, oranges, yellows)
    warm_mask = chromatic & ((hue_pil <= WARM_HUE_LOW) | (hue_pil >= WARM_HUE_HIGH))
    # Cool: hue 85–170 (cyans, blues)
    cool_mask = chromatic & (hue_pil >= COOL_HUE_LOW) & (hue_pil <= COOL_HUE_HIGH)
    # Neutral: achromatic + chromatic pixels outside warm/cool ranges
    neutral_mask = ~warm_mask & ~cool_mask

    total = r.size
    warm_count = int(np.sum(warm_mask))
    cool_count = int(np.sum(cool_mask))
    neutral_count = int(np.sum(neutral_mask))

    warm_pct = (warm_count / total) * 100.0 if total > 0 else 0.0
    cool_pct = (cool_count / total) * 100.0 if total > 0 else 0.0
    neutral_pct = (neutral_count / total) * 100.0 if total > 0 else 0.0

    if cool_count > 0:
        ratio = warm_count / cool_count
    else:
        ratio = float("inf")

    return {
        "warm_pct": round(warm_pct, 2),
        "cool_pct": round(cool_pct, 2),
        "neutral_pct": round(neutral_pct, 2),
        "warm_count": warm_count,
        "cool_count": cool_count,
        "neutral_count": neutral_count,
        "total_pixels": total,
        "warm_cool_ratio": round(ratio, 2) if ratio != float("inf") else "inf",
    }


# ---------------------------------------------------------------------------
# Sigmoid warm→cool transition profile (v3.0.0 — C49)
# ---------------------------------------------------------------------------

import math


def warm_cool_mix(y: float, fg_y: float, bg_y: float, steepness: float = 12.0) -> float:
    """
    Sigmoid warm→cool mix factor from docs/image-rules.md.

    Returns 0.0 (fully warm/FG) to 1.0 (fully cool/BG).

    Args:
        y: current vertical position (pixels)
        fg_y: foreground ground line (pixels)
        bg_y: background ground line (pixels)
        steepness: sigmoid steepness (12.0 = ~10% transition band)
    """
    midpoint = (fg_y + bg_y) / 2.0
    span = abs(bg_y - fg_y) or 1.0
    t = (y - midpoint) / (span / steepness)
    # Clamp to avoid overflow
    t = max(-20.0, min(20.0, t))
    return 1.0 / (1.0 + math.exp(-t))


def measure_sigmoid_profile(
    img: Image.Image,
    fg_y_frac: float = 0.78,
    bg_y_frac: float = 0.70,
    steepness: float = 12.0,
    n_bands: int = 10,
    deviation_threshold: float = 15.0,
) -> Dict:
    """
    Sample warm_pct in horizontal bands between FG and BG ground lines,
    then compare the measured warm→cool profile against the sigmoid expectation.

    The sigmoid expectation is: warm_pct should decrease from near-100% warm
    at FG_Y to near-0% warm at BG_Y, following a logistic curve.

    Args:
        img: PIL image to analyze.
        fg_y_frac: FG ground line as fraction of image height (default 0.78).
        bg_y_frac: BG ground line as fraction of image height (default 0.70).
        steepness: sigmoid steepness parameter (default 12.0).
        n_bands: number of horizontal bands to sample (default 10).
        deviation_threshold: max acceptable mean absolute deviation from
            sigmoid expectation, in percentage points (default 15.0).

    Returns dict with:
        fg_y: int — FG ground line in pixels
        bg_y: int — BG ground line in pixels
        steepness: float — steepness used
        bands: list of dicts per band with y_center, measured_warm_pct,
            expected_warm_pct, deviation
        mean_deviation: float — mean absolute deviation across bands
        max_deviation: float — max absolute deviation
        verdict: str — PASS/WARN/FAIL
        notes: list of str
    """
    rgb = img.convert("RGB")
    w, h = rgb.size
    arr = np.array(rgb, dtype=np.float32) / 255.0

    fg_y = int(fg_y_frac * h)
    bg_y = int(bg_y_frac * h)

    # Ensure fg_y > bg_y (FG is lower on screen = higher Y value)
    if fg_y < bg_y:
        fg_y, bg_y = bg_y, fg_y

    span = fg_y - bg_y
    if span < n_bands:
        return {
            "fg_y": fg_y,
            "bg_y": bg_y,
            "steepness": steepness,
            "bands": [],
            "mean_deviation": 0.0,
            "max_deviation": 0.0,
            "verdict": "SKIP",
            "notes": ["FG-BG span too narrow for {} bands ({} px)".format(n_bands, span)],
        }

    band_height = span // n_bands
    bands = []

    for i in range(n_bands):
        band_top = bg_y + i * band_height
        band_bot = band_top + band_height
        if band_bot > fg_y:
            band_bot = fg_y

        band_center_y = (band_top + band_bot) // 2

        # Measure warm_pct in this band
        band_arr = arr[band_top:band_bot, :, :]
        r, g, b = band_arr[:, :, 0], band_arr[:, :, 1], band_arr[:, :, 2]
        cmax = np.maximum(np.maximum(r, g), b)
        cmin = np.minimum(np.minimum(r, g), b)
        delta = cmax - cmin
        cmax_safe = np.where(cmax > 0, cmax, 1.0)
        sat = np.where(cmax > 0, delta / cmax_safe, 0.0)
        chromatic = sat >= MIN_SATURATION

        if not np.any(chromatic):
            # All achromatic — treat as 50% warm (neutral)
            measured_warm_pct = 50.0
        else:
            hue = np.zeros_like(delta)
            d_safe = np.where(delta > 0, delta, 1.0)
            r_mask = chromatic & (cmax == r)
            g_mask = chromatic & (~r_mask) & (cmax == g)
            b_mask = chromatic & (~r_mask) & (~g_mask) & (cmax == b)
            hue[r_mask] = (((g[r_mask] - b[r_mask]) / d_safe[r_mask]) % 6.0)
            hue[g_mask] = (((b[g_mask] - r[g_mask]) / d_safe[g_mask]) + 2.0)
            hue[b_mask] = (((r[b_mask] - g[b_mask]) / d_safe[b_mask]) + 4.0)
            hue_pil = (hue / 6.0) * 255.0

            warm_mask = chromatic & ((hue_pil <= WARM_HUE_LOW) | (hue_pil >= WARM_HUE_HIGH))
            chromatic_count = int(np.sum(chromatic))
            warm_count = int(np.sum(warm_mask))
            measured_warm_pct = (warm_count / chromatic_count * 100.0) if chromatic_count > 0 else 50.0

        # Expected warm_pct from sigmoid: cool_mix=0 → 100% warm, cool_mix=1 → 0% warm
        cool_mix = warm_cool_mix(float(band_center_y), float(fg_y), float(bg_y), steepness)
        expected_warm_pct = (1.0 - cool_mix) * 100.0

        deviation = measured_warm_pct - expected_warm_pct

        bands.append({
            "band_index": i,
            "y_top": band_top,
            "y_bottom": band_bot,
            "y_center": band_center_y,
            "measured_warm_pct": round(measured_warm_pct, 2),
            "expected_warm_pct": round(expected_warm_pct, 2),
            "deviation": round(deviation, 2),
        })

    deviations = [abs(b["deviation"]) for b in bands]
    mean_dev = sum(deviations) / len(deviations) if deviations else 0.0
    max_dev = max(deviations) if deviations else 0.0

    notes = []
    if mean_dev <= deviation_threshold * 0.5:
        verdict = "PASS"
    elif mean_dev <= deviation_threshold:
        verdict = "WARN"
        notes.append(
            "Mean deviation {:.1f}pp approaching threshold {:.1f}pp".format(mean_dev, deviation_threshold)
        )
    else:
        verdict = "FAIL"
        notes.append(
            "Mean deviation {:.1f}pp exceeds threshold {:.1f}pp — transition is not sigmoid".format(
                mean_dev, deviation_threshold
            )
        )

    return {
        "fg_y": fg_y,
        "bg_y": bg_y,
        "steepness": steepness,
        "n_bands": n_bands,
        "bands": bands,
        "mean_deviation": round(mean_dev, 2),
        "max_deviation": round(max_dev, 2),
        "deviation_threshold": deviation_threshold,
        "verdict": verdict,
        "notes": notes,
    }


def measure_saturation_drop(
    img: Image.Image,
    fg_y_frac: float = 0.78,
    bg_y_frac: float = 0.70,
    band_height_frac: float = 0.05,
) -> Dict:
    """
    Measure BG saturation drop relative to FG.

    Per image-rules.md: BG saturation should be 75-85% of FG saturation
    (0.75-0.85 multiplier, default 0.80).

    Args:
        img: PIL image to analyze.
        fg_y_frac: FG ground line as fraction of image height.
        bg_y_frac: BG ground line as fraction of image height.
        band_height_frac: height of each sampling band as fraction of image height.

    Returns dict with:
        fg_mean_sat: float — mean saturation in FG band (0.0-1.0)
        bg_mean_sat: float — mean saturation in BG band (0.0-1.0)
        sat_ratio: float — BG/FG ratio (target: 0.75-0.85)
        in_range: bool — True if ratio within 0.75-0.85
        verdict: str — PASS/WARN/FAIL
        notes: list of str
    """
    rgb = img.convert("RGB")
    w, h = rgb.size
    arr = np.array(rgb, dtype=np.float32) / 255.0

    fg_y = int(fg_y_frac * h)
    bg_y = int(bg_y_frac * h)
    band_h = max(1, int(band_height_frac * h))

    # Ensure fg_y > bg_y
    if fg_y < bg_y:
        fg_y, bg_y = bg_y, fg_y

    def _mean_sat(y_center: int) -> float:
        y_top = max(0, y_center - band_h // 2)
        y_bot = min(h, y_center + band_h // 2)
        band = arr[y_top:y_bot, :, :]
        r, g, b = band[:, :, 0], band[:, :, 1], band[:, :, 2]
        cmax = np.maximum(np.maximum(r, g), b)
        cmin = np.minimum(np.minimum(r, g), b)
        delta = cmax - cmin
        cmax_safe = np.where(cmax > 0, cmax, 1.0)
        sat = np.where(cmax > 0, delta / cmax_safe, 0.0)
        # Only count chromatic pixels
        chromatic = sat >= MIN_SATURATION
        if not np.any(chromatic):
            return 0.0
        return float(np.mean(sat[chromatic]))

    fg_sat = _mean_sat(fg_y)
    bg_sat = _mean_sat(bg_y)

    if fg_sat > 0:
        ratio = bg_sat / fg_sat
    else:
        ratio = 1.0  # No FG saturation to compare against

    in_range = 0.75 <= ratio <= 0.85
    notes = []

    if in_range:
        verdict = "PASS"
    elif 0.70 <= ratio <= 0.90:
        verdict = "WARN"
        notes.append("Saturation ratio {:.3f} near target range 0.75-0.85".format(ratio))
    elif ratio > 0.90:
        verdict = "WARN"
        notes.append(
            "Saturation ratio {:.3f} — BG not desaturated enough (target 0.75-0.85)".format(ratio)
        )
    else:
        verdict = "WARN"
        notes.append(
            "Saturation ratio {:.3f} — BG too desaturated (target 0.75-0.85)".format(ratio)
        )

    return {
        "fg_mean_sat": round(fg_sat, 4),
        "bg_mean_sat": round(bg_sat, 4),
        "sat_ratio": round(ratio, 4),
        "target_range": [0.75, 0.85],
        "in_range": in_range,
        "verdict": verdict,
        "notes": notes,
    }


# ---------------------------------------------------------------------------
# Single-image analysis
# ---------------------------------------------------------------------------

def analyze_image(img_path: str, sigmoid: bool = False,
                  fg_y_frac: float = 0.78, bg_y_frac: float = 0.70,
                  steepness: float = 12.0, n_bands: int = 10) -> Optional[Dict]:
    """
    Full warm/cool calibration analysis for a single reference image.

    Returns None if the image cannot be loaded (unsupported format, corrupt, etc.).
    """
    path = Path(img_path)
    ext = path.suffix.lower()

    if ext in UNSUPPORTED_EXTS:
        return {
            "file": str(path),
            "filename": path.name,
            "status": "SKIPPED",
            "reason": f"Unsupported format: {ext} (pillow-avif not installed)",
        }

    if ext not in SUPPORTED_EXTS:
        return {
            "file": str(path),
            "filename": path.name,
            "status": "SKIPPED",
            "reason": f"Unsupported format: {ext}",
        }

    try:
        img = Image.open(str(path))
        img.load()  # force decode
    except Exception as e:
        return {
            "file": str(path),
            "filename": path.name,
            "status": "ERROR",
            "reason": str(e),
        }

    separation = measure_warm_cool_separation(img)
    pixels = measure_warm_cool_pixels(img)

    verdict = "VALIDATES" if separation["validates_threshold"] else "CHALLENGES"
    if separation.get("achromatic"):
        verdict = "ACHROMATIC (not meaningful)"

    result = {
        "file": str(path),
        "filename": path.name,
        "size": f"{img.size[0]}x{img.size[1]}",
        "status": "OK",
        "separation": separation,
        "pixels": pixels,
        "verdict": verdict,
    }

    # v3.0.0: optional sigmoid profile and saturation drop analysis
    if sigmoid:
        result["sigmoid_profile"] = measure_sigmoid_profile(
            img, fg_y_frac=fg_y_frac, bg_y_frac=bg_y_frac,
            steepness=steepness, n_bands=n_bands,
        )
        result["saturation_drop"] = measure_saturation_drop(
            img, fg_y_frac=fg_y_frac, bg_y_frac=bg_y_frac,
        )

    return result


# ---------------------------------------------------------------------------
# Batch processing
# ---------------------------------------------------------------------------

def batch_analyze(directory: str) -> Dict:
    """
    Analyze all supported images in a directory.

    Returns dict with:
        directory: str
        results: list of per-image dicts
        summary: aggregate stats
    """
    dirpath = Path(directory)
    if not dirpath.is_dir():
        return {"directory": str(dirpath), "error": f"Not a directory: {dirpath}"}

    results = []
    for entry in sorted(dirpath.iterdir()):
        if not entry.is_file():
            continue
        result = analyze_image(str(entry))
        if result is not None:
            results.append(result)

    # Aggregate
    ok_results = [r for r in results if r.get("status") == "OK"]
    separations = [r["separation"]["separation"] for r in ok_results if not r["separation"].get("achromatic")]
    validates_count = sum(1 for r in ok_results if r["verdict"] == "VALIDATES")
    challenges_count = sum(1 for r in ok_results if r["verdict"] == "CHALLENGES")
    skipped_count = sum(1 for r in results if r.get("status") in ("SKIPPED", "ERROR"))

    summary = {
        "total_files": len(results),
        "analyzed": len(ok_results),
        "skipped": skipped_count,
        "validates_threshold": validates_count,
        "challenges_threshold": challenges_count,
    }

    if separations:
        summary["min_separation"] = round(min(separations), 2)
        summary["max_separation"] = round(max(separations), 2)
        summary["mean_separation"] = round(sum(separations) / len(separations), 2)
        summary["median_separation"] = round(float(np.median(separations)), 2)
    else:
        summary["min_separation"] = None
        summary["max_separation"] = None
        summary["mean_separation"] = None
        summary["median_separation"] = None

    return {
        "directory": str(dirpath),
        "results": results,
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(batch_results: List[Dict], report_path: Optional[str] = None) -> str:
    """
    Generate a Markdown calibration report from batch results.

    If report_path is given, writes to that file; otherwise returns the string.
    """
    lines = []
    lines.append("# Warm/Cool Scene Calibration Report")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Tool:** LTG_TOOL_warmcool_scene_calibrate.py v1.0.0")
    lines.append(f"**Threshold under test:** REAL_INTERIOR = {REAL_INTERIOR_THRESHOLD} PIL hue units")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Global aggregation
    all_separations = []
    total_validates = 0
    total_challenges = 0
    total_analyzed = 0

    for batch in batch_results:
        if "error" in batch:
            continue
        s = batch["summary"]
        total_analyzed += s["analyzed"]
        total_validates += s["validates_threshold"]
        total_challenges += s["challenges_threshold"]
        for r in batch["results"]:
            if r.get("status") == "OK" and not r["separation"].get("achromatic"):
                all_separations.append(r["separation"]["separation"])

    lines.append("## Executive Summary")
    lines.append("")
    if all_separations:
        mean_sep = sum(all_separations) / len(all_separations)
        median_sep = float(np.median(all_separations))
        lines.append(f"- **Images analyzed:** {total_analyzed}")
        lines.append(f"- **Validates threshold (sep >= {REAL_INTERIOR_THRESHOLD}):** {total_validates}")
        lines.append(f"- **Challenges threshold (sep < {REAL_INTERIOR_THRESHOLD}):** {total_challenges}")
        lines.append(f"- **Mean separation:** {mean_sep:.2f} PIL hue units")
        lines.append(f"- **Median separation:** {median_sep:.2f} PIL hue units")
        lines.append(f"- **Range:** {min(all_separations):.2f} – {max(all_separations):.2f}")
        lines.append("")

        if total_challenges == 0:
            lines.append("**Conclusion:** REAL_INTERIOR threshold of {:.1f} is **VALIDATED** — all reference photos meet or exceed it.".format(REAL_INTERIOR_THRESHOLD))
        elif total_challenges <= total_analyzed * 0.2:
            lines.append("**Conclusion:** REAL_INTERIOR threshold of {:.1f} is **MOSTLY VALIDATED** — {}/{} photos fall below. Review outliers.".format(
                REAL_INTERIOR_THRESHOLD, total_challenges, total_analyzed))
        elif total_challenges <= total_analyzed * 0.5:
            lines.append("**Conclusion:** REAL_INTERIOR threshold of {:.1f} is **CONTESTED** — {}/{} photos fall below. Threshold may need lowering.".format(
                REAL_INTERIOR_THRESHOLD, total_challenges, total_analyzed))
        else:
            lines.append("**Conclusion:** REAL_INTERIOR threshold of {:.1f} **NEEDS ADJUSTMENT** — {}/{} photos fall below. Recommend lowering to ~{:.1f}.".format(
                REAL_INTERIOR_THRESHOLD, total_challenges, total_analyzed,
                median_sep * 0.8 if median_sep > 0 else 0))
    else:
        lines.append("No images could be analyzed.")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Per-directory sections
    for batch in batch_results:
        dirpath = batch.get("directory", "unknown")
        dirname = Path(dirpath).name
        lines.append(f"## Directory: `{dirname}/`")
        lines.append("")

        if "error" in batch:
            lines.append(f"**Error:** {batch['error']}")
            lines.append("")
            continue

        s = batch["summary"]
        lines.append(f"Files: {s['total_files']} total, {s['analyzed']} analyzed, {s['skipped']} skipped")
        if s.get("mean_separation") is not None:
            lines.append(f"Separation range: {s['min_separation']} – {s['max_separation']} (mean {s['mean_separation']}, median {s['median_separation']})")
        lines.append("")

        # Per-image table
        lines.append("| File | Size | Separation | Warm% | Cool% | W:C Ratio | Verdict |")
        lines.append("|------|------|-----------|-------|-------|-----------|---------|")
        for r in batch["results"]:
            fname = r["filename"]
            if r.get("status") in ("SKIPPED", "ERROR"):
                reason = r.get("reason", "unknown")
                lines.append(f"| {fname} | — | — | — | — | — | {r['status']}: {reason} |")
                continue
            sep = r["separation"]
            pix = r["pixels"]
            size = r.get("size", "?")
            sep_val = f"{sep['separation']:.1f}"
            warm = f"{pix['warm_pct']:.1f}%"
            cool = f"{pix['cool_pct']:.1f}%"
            ratio = str(pix["warm_cool_ratio"])
            verdict = r["verdict"]
            lines.append(f"| {fname} | {size} | {sep_val} | {warm} | {cool} | {ratio} | {verdict} |")

        lines.append("")

    # Threshold context section
    lines.append("---")
    lines.append("")
    lines.append("## Threshold Context")
    lines.append("")
    lines.append("| World Type | Threshold | Source |")
    lines.append("|-----------|-----------|--------|")
    lines.append(f"| REAL_INTERIOR | {REAL_INTERIOR_THRESHOLD} | render_qa v1.6.0, warmth_lint_v004 |")
    lines.append(f"| REAL_STORM | {REAL_STORM_THRESHOLD} | render_qa v1.6.0 |")
    lines.append(f"| GLITCH | {GLITCH_THRESHOLD} | render_qa v1.6.0 |")
    lines.append(f"| OTHER_SIDE | {OTHER_SIDE_THRESHOLD} | render_qa v1.6.0 |")
    lines.append("")
    lines.append("## Metric Definition")
    lines.append("")
    lines.append("Warm/cool separation = circular distance between median PIL HSV hue of")
    lines.append("top half and bottom half of the image, on a 0–255 scale. This is the")
    lines.append("same metric used by `LTG_TOOL_render_qa.py _check_warm_cool()`. Pixels")
    lines.append("with saturation < 5% are excluded as achromatic.")
    lines.append("")

    report = "\n".join(lines)

    if report_path:
        rp = Path(report_path)
        rp.parent.mkdir(parents=True, exist_ok=True)
        with open(str(rp), "w") as f:
            f.write(report)

    return report


# ---------------------------------------------------------------------------
# Empirical threshold derivation (C48)
# ---------------------------------------------------------------------------

def derive_thresholds(batch_results: List[Dict], safety_margin: float = 0.8) -> Dict:
    """
    Derive empirical threshold recommendations from reference photo measurements.

    Args:
        batch_results: list of batch_analyze() results
        safety_margin: multiplier applied to min observed value (default 0.8 = 20% below min)

    Returns dict with:
        hue_split: recommended thresholds per metric
        warm_pixel_pct: recommended thresholds per metric
        composite: recommended composite thresholds
        data_points: number of images used
        raw_values: per-image measurements
    """
    separations = []
    warm_pcts = []
    raw_values = []

    for batch in batch_results:
        if "error" in batch:
            continue
        for r in batch.get("results", []):
            if r.get("status") != "OK":
                continue
            if r["separation"].get("achromatic"):
                continue

            sep = r["separation"]["separation"]
            wpct = r["pixels"]["warm_pct"]
            separations.append(sep)
            warm_pcts.append(wpct)
            raw_values.append({
                "file": r["filename"],
                "hue_split": sep,
                "warm_pct": wpct,
            })

    if not separations:
        return {"error": "No valid data points", "data_points": 0}

    # Derive thresholds with safety margin
    min_sep = min(separations)
    min_wpct = min(warm_pcts)
    median_sep = float(np.median(separations))
    median_wpct = float(np.median(warm_pcts))

    # Hue-split threshold: floor at safety_margin * min observed
    recommended_hue_split = round(min_sep * safety_margin, 2)

    # Warm-pixel-pct threshold: floor at safety_margin * min observed
    recommended_warm_pct = round(min_wpct * safety_margin, 2)

    # Composite threshold (using weights from composite_warmth_score)
    w_pixel = 0.7
    w_split = 0.3
    composites = []
    for sep, wpct in zip(separations, warm_pcts):
        c = w_pixel * (wpct / 100.0) + w_split * min(sep / 127.5, 1.0)
        composites.append(round(c, 4))

    min_composite = min(composites)
    recommended_composite = round(min_composite * safety_margin, 4)

    return {
        "hue_split": {
            "min_observed": round(min_sep, 2),
            "median_observed": round(median_sep, 2),
            "recommended_threshold": recommended_hue_split,
            "current_threshold": REAL_INTERIOR_THRESHOLD,
            "current_validated": min_sep >= REAL_INTERIOR_THRESHOLD,
        },
        "warm_pixel_pct": {
            "min_observed": round(min_wpct, 2),
            "median_observed": round(median_wpct, 2),
            "recommended_threshold": recommended_warm_pct,
            "current_threshold": 35.0,
            "current_validated": min_wpct >= 35.0,
        },
        "composite": {
            "min_observed": round(min_composite, 4),
            "median_observed": round(float(np.median(composites)), 4),
            "recommended_threshold": recommended_composite,
            "weights": {"warm_pixel": w_pixel, "hue_split": w_split},
        },
        "data_points": len(separations),
        "safety_margin": safety_margin,
        "raw_values": raw_values,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Warm/Cool Scene Calibration — validates REAL_INTERIOR threshold against reference photos."
    )
    parser.add_argument(
        "image", nargs="?", default=None,
        help="Single image path to analyze"
    )
    parser.add_argument(
        "--batch", action="append", default=[],
        help="Directory to batch-process (can be repeated)"
    )
    parser.add_argument(
        "--report", default=None,
        help="Path to write Markdown calibration report"
    )
    parser.add_argument(
        "--threshold", type=float, default=None,
        help="Override REAL_INTERIOR threshold (default: {})".format(REAL_INTERIOR_THRESHOLD)
    )
    parser.add_argument(
        "--output-thresholds", action="store_true",
        help="Derive and output empirical threshold values as JSON"
    )
    parser.add_argument(
        "--safety-margin", type=float, default=0.8,
        help="Safety margin multiplier for threshold derivation (default: 0.8)"
    )
    parser.add_argument(
        "--sigmoid-profile", action="store_true",
        help="Measure sigmoid warm/cool transition profile (v3.0.0)"
    )
    parser.add_argument(
        "--fg-y", type=float, default=0.78,
        help="FG ground line as fraction of image height (default: 0.78)"
    )
    parser.add_argument(
        "--bg-y", type=float, default=0.70,
        help="BG ground line as fraction of image height (default: 0.70)"
    )
    parser.add_argument(
        "--steepness", type=float, default=12.0,
        help="Sigmoid steepness parameter (default: 12.0)"
    )
    parser.add_argument(
        "--bands", type=int, default=10,
        help="Number of horizontal bands for sigmoid profile (default: 10)"
    )

    args = parser.parse_args()

    # Allow threshold override via module-level constant
    if args.threshold is not None:
        _override_threshold(args.threshold)

    if not args.image and not args.batch:
        parser.print_help()
        sys.exit(1)

    # Single image mode
    if args.image and not args.batch:
        result = analyze_image(
            args.image, sigmoid=args.sigmoid_profile,
            fg_y_frac=args.fg_y, bg_y_frac=args.bg_y,
            steepness=args.steepness, n_bands=args.bands,
        )
        if result is None:
            print(f"Could not analyze: {args.image}")
            sys.exit(1)

        if result.get("status") in ("SKIPPED", "ERROR"):
            print(f"{result['status']}: {result.get('reason', '?')}")
            sys.exit(1)

        sep = result["separation"]
        pix = result["pixels"]
        print(f"File: {result['filename']} ({result['size']})")
        print(f"Warm/Cool Separation: {sep['separation']:.2f} PIL hue units")
        print(f"  Top-half median hue: {sep['zone_a_hue']:.2f}")
        print(f"  Bottom-half median hue: {sep['zone_b_hue']:.2f}")
        print(f"  REAL_INTERIOR threshold: {sep['threshold']:.1f}")
        print(f"  Verdict: {result['verdict']}")
        print(f"Pixel breakdown:")
        print(f"  Warm: {pix['warm_pct']:.1f}% ({pix['warm_count']:,} px)")
        print(f"  Cool: {pix['cool_pct']:.1f}% ({pix['cool_count']:,} px)")
        print(f"  Neutral: {pix['neutral_pct']:.1f}% ({pix['neutral_count']:,} px)")
        print(f"  Warm:Cool ratio: {pix['warm_cool_ratio']}")

        # v3.0.0: sigmoid profile output
        if "sigmoid_profile" in result:
            sp = result["sigmoid_profile"]
            print(f"\nSigmoid Profile (steepness={sp['steepness']}, FG_Y={sp['fg_y']}, BG_Y={sp['bg_y']}):")
            print(f"  {'Band':>4s}  {'Y':>5s}  {'Measured':>8s}  {'Expected':>8s}  {'Deviation':>9s}")
            for b in sp["bands"]:
                print(f"  {b['band_index']:4d}  {b['y_center']:5d}  {b['measured_warm_pct']:7.1f}%  {b['expected_warm_pct']:7.1f}%  {b['deviation']:+8.1f}pp")
            print(f"  Mean deviation: {sp['mean_deviation']:.1f}pp  Max: {sp['max_deviation']:.1f}pp  Verdict: {sp['verdict']}")
            for note in sp.get("notes", []):
                print(f"  - {note}")

        if "saturation_drop" in result:
            sd = result["saturation_drop"]
            print(f"\nSaturation Drop:")
            print(f"  FG mean sat: {sd['fg_mean_sat']:.4f}")
            print(f"  BG mean sat: {sd['bg_mean_sat']:.4f}")
            print(f"  Ratio (BG/FG): {sd['sat_ratio']:.4f}  (target: 0.75-0.85)")
            print(f"  Verdict: {sd['verdict']}")
            for note in sd.get("notes", []):
                print(f"  - {note}")

        sys.exit(0)

    # Batch mode
    batch_results = []
    for d in args.batch:
        print(f"\nProcessing: {d}")
        result = batch_analyze(d)
        batch_results.append(result)

        if "error" in result:
            print(f"  ERROR: {result['error']}")
            continue

        s = result["summary"]
        print(f"  Analyzed: {s['analyzed']}, Skipped: {s['skipped']}")
        if s.get("mean_separation") is not None:
            print(f"  Separation: mean={s['mean_separation']:.2f}, median={s['median_separation']:.2f}, range=[{s['min_separation']:.2f}, {s['max_separation']:.2f}]")
            print(f"  Validates: {s['validates_threshold']}, Challenges: {s['challenges_threshold']}")

    # Single image added to batch
    if args.image:
        single = analyze_image(args.image)
        if single and single.get("status") == "OK":
            batch_results.append({
                "directory": str(Path(args.image).parent),
                "results": [single],
                "summary": {
                    "total_files": 1,
                    "analyzed": 1,
                    "skipped": 0,
                    "validates_threshold": 1 if single["verdict"] == "VALIDATES" else 0,
                    "challenges_threshold": 1 if single["verdict"] == "CHALLENGES" else 0,
                    "min_separation": single["separation"]["separation"],
                    "max_separation": single["separation"]["separation"],
                    "mean_separation": single["separation"]["separation"],
                    "median_separation": single["separation"]["separation"],
                },
            })

    # Threshold derivation
    if args.output_thresholds and batch_results:
        thresholds = derive_thresholds(batch_results, safety_margin=args.safety_margin)
        print(json.dumps(thresholds, indent=2))
        sys.exit(0)

    # Report
    if args.report:
        report_text = generate_report(batch_results, report_path=args.report)
        print("\nReport written to: {}".format(args.report))
    elif batch_results:
        report_text = generate_report(batch_results)
        print("\n" + report_text)


if __name__ == "__main__":
    main()
