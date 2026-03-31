#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_scanline_pitch_extract.py
===================================
CRT Scanline Pitch & Inter-line Darkness Extraction Tool for "Luma & the Glitchkin."

Analyzes CRT reference photos to extract:
  1. Scanline pitch — pixel distance between line centers (the repeating period)
  2. Inter-line darkness ratio — dark gap as fraction of pitch (how much black between lines)
  3. Peak luminance profile — brightness distribution across the scanline cycle

These parameters feed into CRT overlay passes used by kitchen, living room, and
Glitch Layer generators. Currently scanline pitch is hardcoded (spacing=4); this tool
provides reference-driven calibration.

Complements LTG_TOOL_glow_profile_extract.py (C46) — together they cover the full
CRT rendering stack: glow falloff + scanline structure.

Algorithm:
  - Convert image to grayscale
  - Extract vertical luminance profile (column average or single-column sample)
  - Detect repeating scanline pattern via autocorrelation of the luminance signal
  - The first significant autocorrelation peak after lag=0 gives the pitch
  - Measure inter-line darkness as the ratio of trough-width to pitch
  - Report statistics across multiple column samples for robustness

Usage:
    python LTG_TOOL_scanline_pitch_extract.py reference/crt/image.jpg
    python LTG_TOOL_scanline_pitch_extract.py reference/crt/
    python LTG_TOOL_scanline_pitch_extract.py reference/crt/ --output report.json
    python LTG_TOOL_scanline_pitch_extract.py reference/crt/ --save-profiles output/production/

Module API:
    from LTG_TOOL_scanline_pitch_extract import (
        extract_scanline_profile,
        batch_extract,
        ScanlineProfile,
    )

Author: Rin Yamamoto (Procedural Art Engineer) — Cycle 47
Version: 1.0.0
"""

from __future__ import annotations

import os
import sys
import json
import math
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import List, Optional, Tuple

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from PIL import Image

__version__ = "1.0.0"
__author__ = "Rin Yamamoto"
__cycle__ = 47

# ── Supported image extensions ──────────────────────────────────────────────
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".avif"}


@dataclass
class ScanlineProfile:
    """Extracted scanline characteristics from a single CRT reference image."""
    file: str
    pitch_px: float                 # scanline pitch in pixels (distance between centers)
    darkness_ratio: float           # inter-line dark gap as fraction of pitch (0..1)
    peak_luminance: float           # mean peak luminance (0..255)
    trough_luminance: float         # mean trough luminance (0..255)
    contrast_ratio: float           # peak / max(trough, 1)
    confidence: float               # autocorrelation peak strength (0..1, higher=cleaner)
    num_samples: int                # number of column samples used
    pitch_std: float                # standard deviation of pitch across samples
    image_width: int = 0
    image_height: int = 0
    error: str = ""


def _grayscale_array(img: Image.Image) -> list:
    """Convert PIL image to grayscale and return as 2D list of luminance values.
    Uses pure Python when NumPy is unavailable."""
    gray = img.convert("L")
    w, h = gray.size
    pixels = list(gray.getdata())
    return [pixels[y * w:(y + 1) * w] for y in range(h)]


def _column_profile(gray_2d: list, col: int) -> list:
    """Extract vertical luminance profile at a given column index."""
    return [gray_2d[y][col] for y in range(len(gray_2d))]


def _mean_column_profile(gray_2d: list, col_start: int, col_end: int) -> list:
    """Average vertical luminance profile over a range of columns."""
    h = len(gray_2d)
    profile = []
    width = col_end - col_start
    for y in range(h):
        total = sum(gray_2d[y][c] for c in range(col_start, col_end))
        profile.append(total / max(width, 1))
    return profile


def _autocorrelation(signal: list, max_lag: int) -> list:
    """Compute normalized autocorrelation of a 1D signal.
    Returns list of autocorrelation values for lags 0..max_lag."""
    n = len(signal)
    mean = sum(signal) / n
    centered = [s - mean for s in signal]
    var = sum(c * c for c in centered)
    if var < 1e-10:
        return [0.0] * (max_lag + 1)

    result = []
    for lag in range(max_lag + 1):
        corr = 0.0
        for i in range(n - lag):
            corr += centered[i] * centered[i + lag]
        result.append(corr / var)
    return result


def _find_first_peak(autocorr: list, min_lag: int = 2) -> Tuple[int, float]:
    """Find the first significant peak in autocorrelation after min_lag.
    Returns (lag, peak_value). If no peak found, returns (0, 0.0)."""
    n = len(autocorr)
    if n < min_lag + 2:
        return (0, 0.0)

    # Find first local maximum after min_lag
    for i in range(min_lag + 1, n - 1):
        if autocorr[i] > autocorr[i - 1] and autocorr[i] > autocorr[i + 1]:
            if autocorr[i] > 0.05:  # minimum significance threshold
                return (i, autocorr[i])

    return (0, 0.0)


def _measure_darkness_ratio(profile: list, pitch: int) -> Tuple[float, float, float]:
    """Measure inter-line darkness ratio given a scanline pitch.

    Returns (darkness_ratio, peak_lum, trough_lum).
    darkness_ratio = fraction of the pitch cycle that is 'dark' (below midpoint).
    """
    n = len(profile)
    if pitch < 2 or n < pitch * 2:
        return (0.0, 0.0, 0.0)

    # Collect per-cycle statistics
    peaks = []
    troughs = []
    dark_counts = []

    num_cycles = (n - pitch) // pitch
    for c in range(min(num_cycles, 50)):  # cap at 50 cycles for speed
        start = c * pitch
        end = start + pitch
        if end > n:
            break
        cycle = profile[start:end]
        p = max(cycle)
        t = min(cycle)
        peaks.append(p)
        troughs.append(t)
        mid = (p + t) / 2
        dark = sum(1 for v in cycle if v < mid)
        dark_counts.append(dark / pitch)

    if not peaks:
        return (0.0, 0.0, 0.0)

    avg_peak = sum(peaks) / len(peaks)
    avg_trough = sum(troughs) / len(troughs)
    avg_dark_ratio = sum(dark_counts) / len(dark_counts)

    return (avg_dark_ratio, avg_peak, avg_trough)


def extract_scanline_profile(image_path: str, num_column_samples: int = 10) -> ScanlineProfile:
    """Extract scanline pitch and darkness ratio from a single CRT reference image.

    Args:
        image_path: Path to the reference image.
        num_column_samples: Number of column positions to sample for robustness.

    Returns:
        ScanlineProfile with extracted parameters.
    """
    path = Path(image_path)
    try:
        img = Image.open(path)
    except Exception as e:
        return ScanlineProfile(
            file=str(path.name), pitch_px=0.0, darkness_ratio=0.0,
            peak_luminance=0.0, trough_luminance=0.0, contrast_ratio=0.0,
            confidence=0.0, num_samples=0, pitch_std=0.0, error=str(e)
        )

    w, h = img.size
    gray_2d = _grayscale_array(img)

    # Sample columns evenly across the center 60% of the image
    # (avoid edges where CRT curvature distortion is worst)
    col_start = int(w * 0.2)
    col_end = int(w * 0.8)
    step = max(1, (col_end - col_start) // max(num_column_samples, 1))
    sample_cols = list(range(col_start, col_end, step))[:num_column_samples]

    if not sample_cols:
        sample_cols = [w // 2]

    pitches = []
    confidences = []
    darkness_ratios = []
    peak_lums = []
    trough_lums = []

    max_lag = min(h // 2, 100)  # search up to 100px or half image height

    for col in sample_cols:
        # Average over a small band for noise reduction (5px wide)
        band_start = max(0, col - 2)
        band_end = min(w, col + 3)
        profile = _mean_column_profile(gray_2d, band_start, band_end)

        autocorr = _autocorrelation(profile, max_lag)
        lag, peak_val = _find_first_peak(autocorr, min_lag=2)

        if lag > 0 and peak_val > 0.05:
            pitches.append(lag)
            confidences.append(peak_val)

            dr, pl, tl = _measure_darkness_ratio(profile, lag)
            darkness_ratios.append(dr)
            peak_lums.append(pl)
            trough_lums.append(tl)

    if not pitches:
        return ScanlineProfile(
            file=str(path.name), pitch_px=0.0, darkness_ratio=0.0,
            peak_luminance=0.0, trough_luminance=0.0, contrast_ratio=0.0,
            confidence=0.0, num_samples=len(sample_cols), pitch_std=0.0,
            image_width=w, image_height=h,
            error="No scanline pattern detected (autocorrelation found no periodic signal)"
        )

    # Compute statistics
    mean_pitch = sum(pitches) / len(pitches)
    mean_conf = sum(confidences) / len(confidences)
    mean_dark = sum(darkness_ratios) / len(darkness_ratios) if darkness_ratios else 0.0
    mean_peak = sum(peak_lums) / len(peak_lums) if peak_lums else 0.0
    mean_trough = sum(trough_lums) / len(trough_lums) if trough_lums else 0.0
    contrast = mean_peak / max(mean_trough, 1.0)

    # Pitch standard deviation
    if len(pitches) > 1:
        var = sum((p - mean_pitch) ** 2 for p in pitches) / (len(pitches) - 1)
        pitch_std = math.sqrt(var)
    else:
        pitch_std = 0.0

    return ScanlineProfile(
        file=str(path.name),
        pitch_px=round(mean_pitch, 2),
        darkness_ratio=round(mean_dark, 4),
        peak_luminance=round(mean_peak, 1),
        trough_luminance=round(mean_trough, 1),
        contrast_ratio=round(contrast, 2),
        confidence=round(mean_conf, 4),
        num_samples=len(pitches),
        pitch_std=round(pitch_std, 2),
        image_width=w,
        image_height=h,
    )


def batch_extract(directory: str, num_column_samples: int = 10) -> List[ScanlineProfile]:
    """Extract scanline profiles from all images in a directory.

    Args:
        directory: Path to directory containing CRT reference images.
        num_column_samples: Number of column positions to sample per image.

    Returns:
        List of ScanlineProfile results.
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        print(f"[ERROR] Not a directory: {directory}")
        return []

    files = sorted([
        f for f in dir_path.iterdir()
        if f.suffix.lower() in IMAGE_EXTS and f.is_file()
    ])

    if not files:
        print(f"[WARN] No image files found in {directory}")
        return []

    results = []
    for i, fpath in enumerate(files, 1):
        print(f"  [{i}/{len(files)}] {fpath.name}...", end="", flush=True)
        profile = extract_scanline_profile(str(fpath), num_column_samples)
        status = "OK" if profile.pitch_px > 0 else "NO PATTERN"
        if profile.error:
            status = f"ERR: {profile.error[:40]}"
        print(f"  pitch={profile.pitch_px:.1f}px  dark={profile.darkness_ratio:.3f}  "
              f"conf={profile.confidence:.3f}  [{status}]")
        results.append(profile)

    return results


def summarize_batch(profiles: List[ScanlineProfile]) -> dict:
    """Compute summary statistics from a batch of scanline profiles.
    Filters to profiles with confidence > 0.1 for reliable results."""
    good = [p for p in profiles if p.pitch_px > 0 and p.confidence > 0.1]
    if not good:
        return {"count": 0, "good_count": 0, "note": "No reliable scanline patterns detected"}

    pitches = [p.pitch_px for p in good]
    dark_ratios = [p.darkness_ratio for p in good]
    contrasts = [p.contrast_ratio for p in good]
    confs = [p.confidence for p in good]

    def _stats(vals):
        n = len(vals)
        mean = sum(vals) / n
        if n > 1:
            var = sum((v - mean) ** 2 for v in vals) / (n - 1)
            std = math.sqrt(var)
        else:
            std = 0.0
        return {
            "mean": round(mean, 3),
            "std": round(std, 3),
            "min": round(min(vals), 3),
            "max": round(max(vals), 3),
            "count": n,
        }

    return {
        "count": len(profiles),
        "good_count": len(good),
        "pitch_px": _stats(pitches),
        "darkness_ratio": _stats(dark_ratios),
        "contrast_ratio": _stats(contrasts),
        "confidence": _stats(confs),
        "recommended_spacing": round(sum(pitches) / len(pitches)),
        "recommended_darkness": round(sum(dark_ratios) / len(dark_ratios), 3),
    }


def print_report(profiles: List[ScanlineProfile]):
    """Print a formatted report of batch extraction results."""
    print("\n" + "=" * 80)
    print("CRT SCANLINE PITCH EXTRACTION REPORT")
    print("=" * 80)

    print(f"\n{'File':<55} {'Pitch':>6} {'Dark':>6} {'Conf':>6} {'Contrast':>8} {'Note'}")
    print("-" * 95)

    for p in profiles:
        note = ""
        if p.error:
            note = p.error[:25]
        elif p.confidence < 0.1:
            note = "low confidence"
        elif p.pitch_std > p.pitch_px * 0.3 and p.pitch_px > 0:
            note = "high variance"
        print(f"{p.file:<55} {p.pitch_px:>6.1f} {p.darkness_ratio:>6.3f} "
              f"{p.confidence:>6.3f} {p.contrast_ratio:>8.2f}  {note}")

    summary = summarize_batch(profiles)
    print("\n" + "-" * 95)
    print(f"Total images: {summary['count']}  |  "
          f"Good fits: {summary.get('good_count', 0)}")

    if summary.get("good_count", 0) > 0:
        ps = summary["pitch_px"]
        ds = summary["darkness_ratio"]
        print(f"\nRecommended scanline_overlay() params (from {ps['count']} good fits):")
        print(f"  spacing = {summary['recommended_spacing']}  "
              f"(mean={ps['mean']:.1f} ± {ps['std']:.1f}, range [{ps['min']:.1f}, {ps['max']:.1f}])")
        print(f"  darkness_ratio = {summary['recommended_darkness']:.3f}  "
              f"(mean={ds['mean']:.3f} ± {ds['std']:.3f})")
        cs = summary["contrast_ratio"]
        print(f"  contrast_ratio = {cs['mean']:.2f}  "
              f"(mean={cs['mean']:.2f} ± {cs['std']:.2f})")
    else:
        print("\nNo reliable scanline patterns detected in this batch.")


def main():
    """CLI entry point."""
    import argparse
    parser = argparse.ArgumentParser(
        description="CRT Scanline Pitch Extraction Tool — Luma & the Glitchkin"
    )
    parser.add_argument("path", help="Image file or directory of CRT reference images")
    parser.add_argument("--output", "-o", help="Save results as JSON to this path")
    parser.add_argument("--samples", type=int, default=10,
                        help="Number of column samples per image (default: 10)")
    parser.add_argument("--save-profiles", help="Directory to save detailed JSON profiles")
    args = parser.parse_args()

    target = Path(args.path)

    if target.is_file():
        print(f"Extracting scanline profile from: {target.name}")
        profile = extract_scanline_profile(str(target), args.samples)
        print_report([profile])
        profiles = [profile]
    elif target.is_dir():
        print(f"Batch extracting from: {target}")
        profiles = batch_extract(str(target), args.samples)
        print_report(profiles)
    else:
        print(f"[ERROR] Path not found: {args.path}")
        sys.exit(1)

    # Save JSON output if requested
    if args.output:
        out_data = {
            "tool": "LTG_TOOL_scanline_pitch_extract",
            "version": __version__,
            "cycle": __cycle__,
            "profiles": [asdict(p) for p in profiles],
            "summary": summarize_batch(profiles),
        }
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(out_data, f, indent=2)
        print(f"\nJSON saved: {out_path}")

    if args.save_profiles:
        prof_dir = Path(args.save_profiles)
        prof_dir.mkdir(parents=True, exist_ok=True)
        out_data = {
            "tool": "LTG_TOOL_scanline_pitch_extract",
            "version": __version__,
            "cycle": __cycle__,
            "profiles": [asdict(p) for p in profiles],
            "summary": summarize_batch(profiles),
        }
        out_path = prof_dir / "scanline_pitch_profiles_c47.json"
        with open(out_path, "w") as f:
            json.dump(out_data, f, indent=2)
        print(f"\nProfiles saved: {out_path}")


if __name__ == "__main__":
    main()
