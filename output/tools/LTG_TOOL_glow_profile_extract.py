# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_glow_profile_extract.py
=================================
CRT Glow Profile Extraction Tool for "Luma & the Glitchkin."

Analyzes CRT reference photos to extract phosphor glow characteristics:
  1. Gaussian fit of phosphor glow radius (FWHM) — how far the glow extends
  2. Color temperature of glow spill — warm/cool shift of the scattered light
  3. Falloff curve parameters — shape of the radial intensity decay

These parameters feed into kitchen/living room generator glow calibration.

Algorithm:
  - Detect the CRT screen region (brightest connected component)
  - Sample radial luminance profiles from the screen edge outward
  - Fit a Gaussian + baseline model: I(r) = A * exp(-r^2 / (2*sigma^2)) + B
  - Extract FWHM = 2 * sqrt(2 * ln(2)) * sigma
  - Measure color temperature by sampling glow spill chromaticity (McCamy's formula)
  - Report falloff curve: sigma, amplitude, baseline, R-squared

Usage:
    python LTG_TOOL_glow_profile_extract.py reference/crt/
    python LTG_TOOL_glow_profile_extract.py reference/crt/image.jpg
    python LTG_TOOL_glow_profile_extract.py reference/crt/ --output report.json
    python LTG_TOOL_glow_profile_extract.py reference/crt/ --save-profiles output/production/

Module API:
    from LTG_TOOL_glow_profile_extract import (
        extract_glow_profile,
        batch_extract,
        GlowProfile,
    )

Author: Rin Yamamoto (Procedural Art Engineer) — Cycle 46
Version: 1.0.0
"""

from __future__ import annotations

import os
import sys
import json
import math
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
from PIL import Image

try:
    import cv2
    _CV2_AVAILABLE = True
except ImportError:
    cv2 = None  # type: ignore
    _CV2_AVAILABLE = False

__version__ = "1.0.0"
__author__ = "Rin Yamamoto"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# FWHM conversion factor: FWHM = 2 * sqrt(2 * ln(2)) * sigma
_FWHM_FACTOR = 2.0 * math.sqrt(2.0 * math.log(2.0))

# Minimum brightness percentile for CRT screen detection
_SCREEN_BRIGHT_PERCENTILE = 90

# Number of radial sample directions for profile averaging
_N_RADIAL_DIRECTIONS = 36  # every 10 degrees

# Maximum radial distance to sample (fraction of image diagonal)
_MAX_RADIAL_FRAC = 0.5

# Supported image extensions
_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff")


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class GlowProfile:
    """Extracted CRT glow profile parameters."""
    filename: str
    image_size: Tuple[int, int]  # (width, height)

    # Screen detection
    screen_center: Tuple[int, int]  # (cx, cy) pixel coords
    screen_bbox: Tuple[int, int, int, int]  # (x, y, w, h)
    screen_area_frac: float  # fraction of image area

    # Gaussian fit: I(r) = amplitude * exp(-r^2 / (2*sigma^2)) + baseline
    sigma_px: float  # Gaussian sigma in pixels
    sigma_frac: float  # sigma as fraction of image diagonal
    amplitude: float  # peak intensity above baseline (0-255 scale)
    baseline: float  # ambient light level (0-255 scale)
    fwhm_px: float  # full width at half maximum in pixels
    fwhm_frac: float  # FWHM as fraction of image diagonal
    r_squared: float  # goodness of fit (0-1)

    # Color temperature
    glow_color_temp_K: Optional[float]  # estimated color temperature in Kelvin
    glow_rgb_mean: Tuple[int, int, int]  # mean RGB of glow spill region
    screen_rgb_mean: Tuple[int, int, int]  # mean RGB of screen region

    # Falloff curve (sampled points for visualization)
    radial_distances_frac: List[float] = field(default_factory=list)
    radial_intensities: List[float] = field(default_factory=list)
    fitted_curve: List[float] = field(default_factory=list)

    # Metadata
    error: Optional[str] = None

    def to_dict(self) -> dict:
        """Serialize to dict, rounding floats for readability."""
        d = asdict(self)
        for key in ("sigma_px", "sigma_frac", "amplitude", "baseline",
                     "fwhm_px", "fwhm_frac", "r_squared", "screen_area_frac"):
            if d[key] is not None:
                d[key] = round(d[key], 4)
        if d["glow_color_temp_K"] is not None:
            d["glow_color_temp_K"] = round(d["glow_color_temp_K"], 0)
        d["radial_distances_frac"] = [round(x, 4) for x in d["radial_distances_frac"]]
        d["radial_intensities"] = [round(x, 2) for x in d["radial_intensities"]]
        d["fitted_curve"] = [round(x, 2) for x in d["fitted_curve"]]
        return d


# ---------------------------------------------------------------------------
# Screen detection
# ---------------------------------------------------------------------------

def _detect_screen_region(gray: np.ndarray) -> Tuple[Tuple[int, int], Tuple[int, int, int, int], np.ndarray]:
    """
    Detect the CRT screen as the brightest connected region.

    Parameters
    ----------
    gray : np.ndarray (H, W) uint8 — grayscale image

    Returns
    -------
    center : (cx, cy)
    bbox : (x, y, w, h)
    mask : (H, W) bool — True for screen pixels
    """
    h, w = gray.shape

    # Threshold at high percentile to find bright region
    threshold = np.percentile(gray, _SCREEN_BRIGHT_PERCENTILE)
    threshold = max(threshold, 128)  # ensure minimum brightness
    bright_mask = gray >= threshold

    if not np.any(bright_mask):
        # Fallback: use top 10% brightest pixels
        threshold = np.percentile(gray, 90)
        bright_mask = gray >= threshold

    if _CV2_AVAILABLE:
        # Use connected components to find the largest bright blob
        binary = bright_mask.astype(np.uint8) * 255
        # Morphological close to merge nearby bright regions
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        n_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary)

        if n_labels <= 1:
            # No bright regions found — use center of bright pixels
            ys, xs = np.where(bright_mask)
            cx, cy = int(np.mean(xs)), int(np.mean(ys))
            return (cx, cy), (0, 0, w, h), bright_mask

        # Find largest non-background component
        # stats columns: x, y, w, h, area
        areas = stats[1:, cv2.CC_STAT_AREA]  # skip background label 0
        largest_idx = np.argmax(areas) + 1  # offset for background
        cx = int(centroids[largest_idx][0])
        cy = int(centroids[largest_idx][1])
        bx = int(stats[largest_idx, cv2.CC_STAT_LEFT])
        by = int(stats[largest_idx, cv2.CC_STAT_TOP])
        bw = int(stats[largest_idx, cv2.CC_STAT_WIDTH])
        bh = int(stats[largest_idx, cv2.CC_STAT_HEIGHT])
        screen_mask = labels == largest_idx
        return (cx, cy), (bx, by, bw, bh), screen_mask
    else:
        # Numpy fallback: centroid of all bright pixels
        ys, xs = np.where(bright_mask)
        if len(xs) == 0:
            return (w // 2, h // 2), (0, 0, w, h), bright_mask
        cx, cy = int(np.mean(xs)), int(np.mean(ys))
        x_min, x_max = int(np.min(xs)), int(np.max(xs))
        y_min, y_max = int(np.min(ys)), int(np.max(ys))
        return (cx, cy), (x_min, y_min, x_max - x_min + 1, y_max - y_min + 1), bright_mask


# ---------------------------------------------------------------------------
# Radial profile sampling
# ---------------------------------------------------------------------------

def _sample_radial_profile(
    gray: np.ndarray,
    center: Tuple[int, int],
    screen_mask: np.ndarray,
    n_bins: int = 100,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Sample average radial luminance profile from screen edge outward.

    Samples along multiple radial directions and averages the profiles.

    Parameters
    ----------
    gray : (H, W) uint8 — grayscale image
    center : (cx, cy) — screen center
    screen_mask : (H, W) bool — screen region
    n_bins : int — number of radial distance bins

    Returns
    -------
    distances : (n_bins,) float — radial distance in pixels (bin centers)
    intensities : (n_bins,) float — average luminance per bin (0-255)
    """
    h, w = gray.shape
    cx, cy = center
    diag = math.sqrt(w * w + h * h)
    max_r = diag * _MAX_RADIAL_FRAC

    # Find approximate screen edge distance
    screen_ys, screen_xs = np.where(screen_mask)
    if len(screen_xs) == 0:
        screen_edge_r = 0.0
    else:
        screen_dists = np.sqrt((screen_xs - cx) ** 2 + (screen_ys - cy) ** 2)
        screen_edge_r = float(np.percentile(screen_dists, 90))

    # Sample from screen edge outward
    bin_edges = np.linspace(screen_edge_r, max_r, n_bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0

    # Precompute distance map from center
    yy, xx = np.mgrid[0:h, 0:w]
    dist_map = np.sqrt((xx - cx) ** 2.0 + (yy - cy) ** 2.0)

    # Exclude screen interior
    outside_screen = ~screen_mask

    # Bin the pixel luminances
    intensities = np.zeros(n_bins, dtype=np.float64)
    counts = np.zeros(n_bins, dtype=np.int64)

    for i in range(n_bins):
        in_bin = outside_screen & (dist_map >= bin_edges[i]) & (dist_map < bin_edges[i + 1])
        bin_count = np.sum(in_bin)
        if bin_count > 0:
            intensities[i] = np.mean(gray[in_bin].astype(np.float64))
            counts[i] = bin_count
        else:
            intensities[i] = np.nan

    # Interpolate NaN bins
    valid = ~np.isnan(intensities)
    if np.any(valid) and not np.all(valid):
        intensities[~valid] = np.interp(
            bin_centers[~valid], bin_centers[valid], intensities[valid]
        )

    return bin_centers, intensities


# ---------------------------------------------------------------------------
# Gaussian fitting
# ---------------------------------------------------------------------------

def _fit_gaussian_falloff(
    distances: np.ndarray,
    intensities: np.ndarray,
) -> Tuple[float, float, float, float]:
    """
    Fit a Gaussian + baseline model to the radial intensity profile.

    Model: I(r) = A * exp(-(r - r0)^2 / (2*sigma^2)) + B

    Uses least-squares (numpy-only, no scipy dependency).

    Parameters
    ----------
    distances : (N,) float — radial distances in pixels
    intensities : (N,) float — luminance values

    Returns
    -------
    sigma : float — Gaussian width (pixels)
    amplitude : float — peak intensity above baseline
    baseline : float — ambient intensity
    r_squared : float — coefficient of determination
    """
    # Normalize distances to start from 0 (edge of screen)
    r = distances - distances[0]
    y = intensities.copy()

    # Initial estimates
    baseline_est = float(np.min(y[-10:]))  # far-field baseline
    amplitude_est = float(y[0]) - baseline_est
    if amplitude_est <= 0:
        amplitude_est = 1.0

    # Find half-max point for sigma estimate
    half_max = baseline_est + amplitude_est / 2.0
    above_half = y >= half_max
    if np.any(above_half):
        half_max_idx = np.where(above_half)[0][-1]
        sigma_est = max(float(r[half_max_idx]) / _FWHM_FACTOR * 2.0, 1.0)
    else:
        sigma_est = float(r[-1]) / 4.0

    # Iterative refinement (simple grid search + gradient-free optimization)
    best_sigma = sigma_est
    best_amp = amplitude_est
    best_base = baseline_est
    best_r2 = -np.inf

    # Grid search around initial estimates
    for sigma_mult in [0.3, 0.5, 0.7, 1.0, 1.3, 1.6, 2.0, 2.5, 3.0]:
        sigma_try = sigma_est * sigma_mult
        if sigma_try <= 0:
            continue

        # Closed-form amplitude and baseline given sigma
        # Using linearized least squares: y = A * exp(-r^2/(2*s^2)) + B
        exp_term = np.exp(-r ** 2 / (2.0 * sigma_try ** 2))
        # Solve [A, B] = argmin sum(y - A*exp - B)^2
        # This is linear in A and B
        n = len(y)
        sum_e = np.sum(exp_term)
        sum_e2 = np.sum(exp_term ** 2)
        sum_y = np.sum(y)
        sum_ye = np.sum(y * exp_term)

        denom = n * sum_e2 - sum_e ** 2
        if abs(denom) < 1e-10:
            continue
        A = (n * sum_ye - sum_e * sum_y) / denom
        B = (sum_y * sum_e2 - sum_ye * sum_e) / denom

        if A < 0:
            A = 0.0

        fitted = A * exp_term + B
        ss_res = np.sum((y - fitted) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

        if r2 > best_r2:
            best_r2 = r2
            best_sigma = sigma_try
            best_amp = A
            best_base = B

    # Fine-tune sigma around best
    for delta_frac in np.linspace(-0.3, 0.3, 21):
        sigma_try = best_sigma * (1.0 + delta_frac)
        if sigma_try <= 0:
            continue
        exp_term = np.exp(-r ** 2 / (2.0 * sigma_try ** 2))
        n = len(y)
        sum_e = np.sum(exp_term)
        sum_e2 = np.sum(exp_term ** 2)
        sum_y = np.sum(y)
        sum_ye = np.sum(y * exp_term)
        denom = n * sum_e2 - sum_e ** 2
        if abs(denom) < 1e-10:
            continue
        A = (n * sum_ye - sum_e * sum_y) / denom
        B = (sum_y * sum_e2 - sum_ye * sum_e) / denom
        if A < 0:
            A = 0.0
        fitted = A * exp_term + B
        ss_res = np.sum((y - fitted) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
        if r2 > best_r2:
            best_r2 = r2
            best_sigma = sigma_try
            best_amp = A
            best_base = B

    return float(best_sigma), float(best_amp), float(best_base), float(best_r2)


# ---------------------------------------------------------------------------
# Color temperature estimation
# ---------------------------------------------------------------------------

def _estimate_color_temperature(rgb: np.ndarray) -> Optional[float]:
    """
    Estimate correlated color temperature from mean RGB using McCamy's formula.

    Parameters
    ----------
    rgb : (3,) float — mean R, G, B values (0-255)

    Returns
    -------
    float — estimated CCT in Kelvin, or None if computation fails
    """
    r, g, b = float(rgb[0]), float(rgb[1]), float(rgb[2])

    # Convert to CIE xyY chromaticity
    # sRGB to XYZ (simplified)
    def linearize(c):
        c = c / 255.0
        if c <= 0.04045:
            return c / 12.92
        return ((c + 0.055) / 1.055) ** 2.4

    r_lin = linearize(r)
    g_lin = linearize(g)
    b_lin = linearize(b)

    X = 0.4124564 * r_lin + 0.3575761 * g_lin + 0.1804375 * b_lin
    Y = 0.2126729 * r_lin + 0.7151522 * g_lin + 0.0721750 * b_lin
    Z = 0.0193339 * r_lin + 0.1191920 * g_lin + 0.9503041 * b_lin

    total = X + Y + Z
    if total < 1e-10:
        return None

    x = X / total
    y = Y / total

    if y < 1e-10:
        return None

    # McCamy's formula (approximation for CCT)
    n = (x - 0.3320) / (0.1858 - y)
    cct = 449.0 * n ** 3 + 3525.0 * n ** 2 + 6823.3 * n + 5520.33

    # Sanity check: typical CRT phosphors are 4000-9500K
    if cct < 1000 or cct > 25000:
        return None

    return cct


# ---------------------------------------------------------------------------
# Core extraction function
# ---------------------------------------------------------------------------

def extract_glow_profile(image_path: str) -> GlowProfile:
    """
    Extract CRT glow profile from a single reference image.

    Parameters
    ----------
    image_path : str
        Path to a CRT reference photo.

    Returns
    -------
    GlowProfile — extracted glow parameters
    """
    abs_path = os.path.abspath(image_path)
    basename = os.path.basename(abs_path)

    try:
        img = Image.open(abs_path).convert("RGB")
    except Exception as e:
        return GlowProfile(
            filename=basename, image_size=(0, 0),
            screen_center=(0, 0), screen_bbox=(0, 0, 0, 0), screen_area_frac=0.0,
            sigma_px=0.0, sigma_frac=0.0, amplitude=0.0, baseline=0.0,
            fwhm_px=0.0, fwhm_frac=0.0, r_squared=0.0,
            glow_color_temp_K=None, glow_rgb_mean=(0, 0, 0), screen_rgb_mean=(0, 0, 0),
            error=f"Cannot open image: {e}",
        )

    w, h = img.size
    rgb_arr = np.array(img, dtype=np.uint8)  # (H, W, 3)
    diag = math.sqrt(w * w + h * h)

    # Grayscale (luminance)
    gray = np.dot(rgb_arr[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)

    # Detect screen
    center, bbox, screen_mask = _detect_screen_region(gray)
    screen_area_frac = float(np.sum(screen_mask)) / (w * h) if w * h > 0 else 0.0

    # Screen mean color
    screen_pixels = rgb_arr[screen_mask]
    if len(screen_pixels) > 0:
        screen_rgb_mean = tuple(int(x) for x in np.mean(screen_pixels, axis=0))
    else:
        screen_rgb_mean = (0, 0, 0)

    # Sample radial profile
    distances, intensities = _sample_radial_profile(gray, center, screen_mask)

    if len(distances) == 0 or np.all(np.isnan(intensities)):
        return GlowProfile(
            filename=basename, image_size=(w, h),
            screen_center=center, screen_bbox=bbox, screen_area_frac=screen_area_frac,
            sigma_px=0.0, sigma_frac=0.0, amplitude=0.0, baseline=0.0,
            fwhm_px=0.0, fwhm_frac=0.0, r_squared=0.0,
            glow_color_temp_K=None, glow_rgb_mean=(0, 0, 0),
            screen_rgb_mean=screen_rgb_mean,
            error="Insufficient radial profile data",
        )

    # Fit Gaussian
    sigma, amplitude, baseline, r_squared = _fit_gaussian_falloff(distances, intensities)
    fwhm = sigma * _FWHM_FACTOR
    sigma_frac = sigma / diag if diag > 0 else 0.0
    fwhm_frac = fwhm / diag if diag > 0 else 0.0

    # Generate fitted curve
    r_from_edge = distances - distances[0]
    fitted_curve = amplitude * np.exp(-r_from_edge ** 2 / (2.0 * sigma ** 2)) + baseline

    # Glow spill color: sample annular region just outside screen
    screen_edge_r = distances[0]
    glow_inner = screen_edge_r
    glow_outer = screen_edge_r + sigma * 1.5  # within 1.5 sigma

    yy, xx = np.mgrid[0:h, 0:w]
    dist_map = np.sqrt((xx - center[0]) ** 2.0 + (yy - center[1]) ** 2.0)
    glow_ring = (~screen_mask) & (dist_map >= glow_inner) & (dist_map < glow_outer)

    glow_pixels = rgb_arr[glow_ring]
    if len(glow_pixels) > 0:
        glow_rgb_mean = tuple(int(x) for x in np.mean(glow_pixels, axis=0))
        glow_color_temp = _estimate_color_temperature(np.mean(glow_pixels, axis=0))
    else:
        glow_rgb_mean = (0, 0, 0)
        glow_color_temp = None

    return GlowProfile(
        filename=basename,
        image_size=(w, h),
        screen_center=center,
        screen_bbox=bbox,
        screen_area_frac=screen_area_frac,
        sigma_px=sigma,
        sigma_frac=sigma_frac,
        amplitude=amplitude,
        baseline=baseline,
        fwhm_px=fwhm,
        fwhm_frac=fwhm_frac,
        r_squared=r_squared,
        glow_color_temp_K=glow_color_temp,
        glow_rgb_mean=glow_rgb_mean,
        screen_rgb_mean=screen_rgb_mean,
        radial_distances_frac=[float(d / diag) for d in distances],
        radial_intensities=[float(x) for x in intensities],
        fitted_curve=[float(x) for x in fitted_curve],
    )


# ---------------------------------------------------------------------------
# Batch extraction
# ---------------------------------------------------------------------------

def batch_extract(
    directory_or_paths,
    extensions: Tuple[str, ...] = _IMAGE_EXTENSIONS,
) -> List[GlowProfile]:
    """
    Extract glow profiles from all images in a directory.

    Parameters
    ----------
    directory_or_paths : str | list[str]
        Directory path or explicit list of file paths.
    extensions : tuple[str, ...]
        File extensions to include.

    Returns
    -------
    list[GlowProfile] — one per valid image
    """
    if isinstance(directory_or_paths, str) and os.path.isdir(directory_or_paths):
        paths = sorted([
            os.path.join(directory_or_paths, f)
            for f in os.listdir(directory_or_paths)
            if os.path.splitext(f)[1].lower() in extensions
        ])
    else:
        paths = list(directory_or_paths)

    return [extract_glow_profile(p) for p in paths]


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def format_report(profiles: List[GlowProfile]) -> str:
    """Format a batch of glow profiles as a human-readable report."""
    lines = []
    lines.append("=" * 90)
    lines.append("CRT Glow Profile Extraction Report")
    lines.append("=" * 90)
    lines.append("")

    header = (
        f"{'Filename':<55} {'FWHM_px':>8} {'FWHM%':>6} "
        f"{'Amp':>5} {'Base':>5} {'R^2':>5} {'CCT_K':>7} {'GlowRGB':>15}"
    )
    lines.append(header)
    lines.append("-" * len(header))

    valid = []
    for p in profiles:
        if p.error:
            lines.append(f"{p.filename:<55} ERROR: {p.error}")
            continue
        lines.append(
            f"{p.filename:<55} {p.fwhm_px:>8.1f} {p.fwhm_frac * 100:>5.1f}% "
            f"{p.amplitude:>5.1f} {p.baseline:>5.1f} {p.r_squared:>5.3f} "
            f"{p.glow_color_temp_K or 0:>7.0f} "
            f"({p.glow_rgb_mean[0]:>3},{p.glow_rgb_mean[1]:>3},{p.glow_rgb_mean[2]:>3})"
        )
        valid.append(p)

    if valid:
        lines.append("")
        lines.append("-" * 60)
        lines.append("AGGREGATE STATISTICS")
        lines.append("-" * 60)

        fwhms = [p.fwhm_frac for p in valid if p.r_squared > 0.5]
        amps = [p.amplitude for p in valid if p.r_squared > 0.5]
        bases = [p.baseline for p in valid if p.r_squared > 0.5]
        ccts = [p.glow_color_temp_K for p in valid if p.glow_color_temp_K is not None and p.r_squared > 0.5]

        if fwhms:
            lines.append(f"  FWHM (% diag): mean={np.mean(fwhms) * 100:.1f}%, "
                         f"median={np.median(fwhms) * 100:.1f}%, "
                         f"range=[{np.min(fwhms) * 100:.1f}%, {np.max(fwhms) * 100:.1f}%]")
        if amps:
            lines.append(f"  Amplitude: mean={np.mean(amps):.1f}, "
                         f"median={np.median(amps):.1f}, "
                         f"range=[{np.min(amps):.1f}, {np.max(amps):.1f}]")
        if bases:
            lines.append(f"  Baseline: mean={np.mean(bases):.1f}, "
                         f"median={np.median(bases):.1f}, "
                         f"range=[{np.min(bases):.1f}, {np.max(bases):.1f}]")
        if ccts:
            lines.append(f"  Color Temp: mean={np.mean(ccts):.0f}K, "
                         f"median={np.median(ccts):.0f}K, "
                         f"range=[{np.min(ccts):.0f}K, {np.max(ccts):.0f}K]")

        lines.append("")
        lines.append("RECOMMENDED GLOW PARAMETERS (for generator calibration):")
        if fwhms:
            lines.append(f"  sigma_frac = {np.median(fwhms) / _FWHM_FACTOR:.4f}  "
                         f"(median sigma as fraction of canvas diagonal)")
            lines.append(f"  fwhm_frac  = {np.median(fwhms):.4f}  "
                         f"(median FWHM as fraction of canvas diagonal)")
        if amps:
            lines.append(f"  amplitude  = {np.median(amps):.1f}  "
                         f"(median peak glow intensity, 0-255)")
        if bases:
            lines.append(f"  baseline   = {np.median(bases):.1f}  "
                         f"(median ambient/spill floor, 0-255)")
        if ccts:
            lines.append(f"  color_temp = {np.median(ccts):.0f}K  "
                         f"(median glow CCT)")

        lines.append("")
        n_good = len(fwhms)
        n_total = len(profiles)
        n_err = len(profiles) - len(valid)
        n_low_fit = len(valid) - n_good
        lines.append(f"  Fit quality: {n_good} good (R^2 > 0.5), "
                     f"{n_low_fit} low-fit, {n_err} errors, {n_total} total")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="CRT Glow Profile Extraction Tool"
    )
    parser.add_argument(
        "path",
        help="Path to a CRT reference image or directory of images"
    )
    parser.add_argument(
        "--output", "-o",
        help="Path to save JSON output",
        default=None,
    )
    parser.add_argument(
        "--save-profiles",
        help="Directory to save individual profile JSONs",
        default=None,
    )

    args = parser.parse_args()

    if os.path.isdir(args.path):
        profiles = batch_extract(args.path)
    elif os.path.isfile(args.path):
        profiles = [extract_glow_profile(args.path)]
    else:
        print(f"ERROR: {args.path} is not a valid file or directory")
        sys.exit(1)

    # Print report
    print(format_report(profiles))

    # Save JSON
    if args.output:
        data = [p.to_dict() for p in profiles]
        with open(args.output, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\nJSON saved to: {args.output}")

    if args.save_profiles:
        os.makedirs(args.save_profiles, exist_ok=True)
        for p in profiles:
            out_path = os.path.join(
                args.save_profiles,
                os.path.splitext(p.filename)[0] + "_glow_profile.json"
            )
            with open(out_path, "w") as f:
                json.dump(p.to_dict(), f, indent=2)
        print(f"\nIndividual profiles saved to: {args.save_profiles}")


if __name__ == "__main__":
    main()
