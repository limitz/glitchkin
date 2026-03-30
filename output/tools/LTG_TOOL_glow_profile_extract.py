# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_glow_profile_extract.py
=================================
CRT Glow Profile Extraction Tool for "Luma & the Glitchkin."

Analyzes CRT reference photos to extract phosphor glow characteristics:
  1. Anisotropic Gaussian fit — separate σ_x (horizontal) and σ_y (vertical) falloff
  2. Isotropic Gaussian fit — radial average (backward compatible with v1.0.0)
  3. Color temperature of glow spill — warm/cool shift of the scattered light
  4. Falloff curve parameters — shape of the radial intensity decay
  5. Cross-validation against C46 calibration (sigma_frac=0.1165, FWHM 27.4%)

These parameters feed into kitchen/living room generator glow calibration and
scanline-aware CRT rendering (anisotropic glow follows CRT phosphor geometry).

Algorithm:
  - Detect the CRT screen region (brightest connected component)
  - Isotropic path: sample radial luminance profiles from screen edge outward,
    fit Gaussian + baseline: I(r) = A * exp(-r^2 / (2*sigma^2)) + B
  - Anisotropic path: sample horizontal and vertical luminance strips through
    screen center, fit separate Gaussians:
      I_x(x) = A_x * exp(-x^2 / (2*sigma_x^2)) + B_x  (horizontal)
      I_y(y) = A_y * exp(-y^2 / (2*sigma_y^2)) + B_y  (vertical)
  - Extract FWHM = 2 * sqrt(2 * ln(2)) * sigma for each axis
  - Measure color temperature by sampling glow spill chromaticity (McCamy's formula)
  - Cross-validate: compare isotropic sigma_frac against C46 reference (0.1165)

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

Author: Rin Yamamoto (Procedural Art Engineer) — Cycle 46, upgraded Cycle 48
Version: 2.0.0 (C48 — anisotropic σ_x/σ_y Gaussian, cross-validation vs C46)
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

__version__ = "2.0.0"
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
_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".avif")

# C46 calibration reference values (from crt_glow_profiles_c46.json aggregate)
_C46_REF_SIGMA_FRAC = 0.1165
_C46_REF_FWHM_FRAC = 0.2744

# Width of horizontal/vertical strip for anisotropic sampling (pixels each side of center)
_ANISO_STRIP_HALF_WIDTH = 10


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

    # Isotropic Gaussian fit: I(r) = amplitude * exp(-r^2 / (2*sigma^2)) + baseline
    sigma_px: float  # Gaussian sigma in pixels (isotropic)
    sigma_frac: float  # sigma as fraction of image diagonal
    amplitude: float  # peak intensity above baseline (0-255 scale)
    baseline: float  # ambient light level (0-255 scale)
    fwhm_px: float  # full width at half maximum in pixels
    fwhm_frac: float  # FWHM as fraction of image diagonal
    r_squared: float  # goodness of fit (0-1)

    # Anisotropic Gaussian fit: separate horizontal (x) and vertical (y) axes
    sigma_x_px: float = 0.0  # horizontal sigma in pixels
    sigma_y_px: float = 0.0  # vertical sigma in pixels
    sigma_x_frac: float = 0.0  # horizontal sigma as fraction of image width
    sigma_y_frac: float = 0.0  # vertical sigma as fraction of image height
    fwhm_x_px: float = 0.0
    fwhm_y_px: float = 0.0
    fwhm_x_frac: float = 0.0  # FWHM_x as fraction of image width
    fwhm_y_frac: float = 0.0  # FWHM_y as fraction of image height
    amplitude_x: float = 0.0
    amplitude_y: float = 0.0
    baseline_x: float = 0.0
    baseline_y: float = 0.0
    r_squared_x: float = 0.0
    r_squared_y: float = 0.0
    anisotropy_ratio: float = 1.0  # sigma_x / sigma_y (>1 = wider horizontal glow)

    # Cross-validation against C46 calibration
    c46_sigma_frac_ref: float = _C46_REF_SIGMA_FRAC
    c46_sigma_frac_delta: float = 0.0  # this_sigma_frac - C46_ref
    c46_sigma_frac_delta_pct: float = 0.0  # percentage deviation from C46

    # Color temperature
    glow_color_temp_K: Optional[float] = None  # estimated color temperature in Kelvin
    glow_rgb_mean: Tuple[int, int, int] = (0, 0, 0)  # mean RGB of glow spill region
    screen_rgb_mean: Tuple[int, int, int] = (0, 0, 0)  # mean RGB of screen region

    # Falloff curve (sampled points for visualization)
    radial_distances_frac: List[float] = field(default_factory=list)
    radial_intensities: List[float] = field(default_factory=list)
    fitted_curve: List[float] = field(default_factory=list)

    # Metadata
    error: Optional[str] = None

    def to_dict(self) -> dict:
        """Serialize to dict, rounding floats for readability."""
        d = asdict(self)
        round_4 = (
            "sigma_px", "sigma_frac", "amplitude", "baseline",
            "fwhm_px", "fwhm_frac", "r_squared", "screen_area_frac",
            "sigma_x_px", "sigma_y_px", "sigma_x_frac", "sigma_y_frac",
            "fwhm_x_px", "fwhm_y_px", "fwhm_x_frac", "fwhm_y_frac",
            "amplitude_x", "amplitude_y", "baseline_x", "baseline_y",
            "r_squared_x", "r_squared_y", "anisotropy_ratio",
            "c46_sigma_frac_ref", "c46_sigma_frac_delta", "c46_sigma_frac_delta_pct",
        )
        for key in round_4:
            if d.get(key) is not None:
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
# Radial profile sampling (isotropic)
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
# Axis-aligned strip sampling (anisotropic)
# ---------------------------------------------------------------------------

def _sample_axis_profile(
    gray: np.ndarray,
    center: Tuple[int, int],
    screen_mask: np.ndarray,
    axis: str,
    half_width: int = _ANISO_STRIP_HALF_WIDTH,
    n_bins: int = 80,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Sample luminance along a horizontal or vertical strip through screen center,
    outside the screen region, for anisotropic Gaussian fitting.

    Parameters
    ----------
    gray : (H, W) uint8
    center : (cx, cy)
    screen_mask : (H, W) bool
    axis : 'x' (horizontal) or 'y' (vertical)
    half_width : int — strip half-width in pixels for averaging
    n_bins : int — number of distance bins from screen edge outward

    Returns
    -------
    distances : (N,) float — distance from screen edge in pixels
    intensities : (N,) float — average luminance
    """
    h, w = gray.shape
    cx, cy = center

    if axis == "x":
        # Horizontal strip: rows [cy - hw : cy + hw], all columns
        y_lo = max(0, cy - half_width)
        y_hi = min(h, cy + half_width + 1)
        strip = gray[y_lo:y_hi, :]  # (strip_h, W)
        strip_mask = screen_mask[y_lo:y_hi, :]
        # Average across strip height
        strip_lum = np.mean(strip.astype(np.float64), axis=0)  # (W,)
        strip_screen = np.any(strip_mask, axis=0)  # (W,) — True if any screen pixel in column
        positions = np.arange(w, dtype=np.float64)
        edge_positions = positions[strip_screen]
        if len(edge_positions) == 0:
            return np.array([]), np.array([])
        # Screen extent on this axis
        screen_lo = float(edge_positions[0])
        screen_hi = float(edge_positions[-1])
        screen_center_ax = (screen_lo + screen_hi) / 2.0
        screen_half = (screen_hi - screen_lo) / 2.0
        # Sample outward from both sides, measure distance from screen edge
        # Left side: positions < screen_lo, distance = screen_lo - position
        left_mask = (positions < screen_lo) & (~strip_screen)
        left_dists = screen_lo - positions[left_mask]
        left_lum = strip_lum[left_mask]
        # Right side: positions > screen_hi, distance = position - screen_hi
        right_mask = (positions > screen_hi) & (~strip_screen)
        right_dists = positions[right_mask] - screen_hi
        right_lum = strip_lum[right_mask]
    else:
        # Vertical strip: columns [cx - hw : cx + hw], all rows
        x_lo = max(0, cx - half_width)
        x_hi = min(w, cx + half_width + 1)
        strip = gray[:, x_lo:x_hi]
        strip_mask = screen_mask[:, x_lo:x_hi]
        strip_lum = np.mean(strip.astype(np.float64), axis=1)  # (H,)
        strip_screen = np.any(strip_mask, axis=1)
        positions = np.arange(h, dtype=np.float64)
        edge_positions = positions[strip_screen]
        if len(edge_positions) == 0:
            return np.array([]), np.array([])
        screen_lo = float(edge_positions[0])
        screen_hi = float(edge_positions[-1])
        # Top side
        top_mask = (positions < screen_lo) & (~strip_screen)
        top_dists = screen_lo - positions[top_mask]
        top_lum = strip_lum[top_mask]
        # Bottom side
        bot_mask = (positions > screen_hi) & (~strip_screen)
        bot_dists = positions[bot_mask] - screen_hi
        bot_lum = strip_lum[bot_mask]
        left_dists, left_lum = top_dists, top_lum
        right_dists, right_lum = bot_dists, bot_lum

    # Combine both sides
    all_dists = np.concatenate([left_dists, right_dists])
    all_lum = np.concatenate([left_lum, right_lum])

    if len(all_dists) == 0:
        return np.array([]), np.array([])

    # Bin into distance bins
    max_dist = float(np.max(all_dists))
    if max_dist <= 0:
        return np.array([]), np.array([])
    bin_edges = np.linspace(0, max_dist, n_bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
    intensities = np.full(n_bins, np.nan, dtype=np.float64)

    for i in range(n_bins):
        in_bin = (all_dists >= bin_edges[i]) & (all_dists < bin_edges[i + 1])
        if np.any(in_bin):
            intensities[i] = np.mean(all_lum[in_bin])

    # Interpolate NaN
    valid = ~np.isnan(intensities)
    if np.any(valid) and not np.all(valid):
        intensities[~valid] = np.interp(
            bin_centers[~valid], bin_centers[valid], intensities[valid]
        )
    elif not np.any(valid):
        return np.array([]), np.array([])

    return bin_centers, intensities


# ---------------------------------------------------------------------------
# Gaussian fitting (shared for isotropic and anisotropic)
# ---------------------------------------------------------------------------

def _fit_gaussian_falloff(
    distances: np.ndarray,
    intensities: np.ndarray,
) -> Tuple[float, float, float, float]:
    """
    Fit a Gaussian + baseline model to an intensity profile.

    Model: I(d) = A * exp(-d^2 / (2*sigma^2)) + B

    Uses linearized least-squares grid search (no scipy).

    Parameters
    ----------
    distances : (N,) float — distances from edge (pixels)
    intensities : (N,) float — luminance values

    Returns
    -------
    sigma : float — Gaussian width (pixels)
    amplitude : float — peak intensity above baseline
    baseline : float — ambient intensity
    r_squared : float — coefficient of determination
    """
    if len(distances) < 3 or len(intensities) < 3:
        return 0.0, 0.0, 0.0, 0.0

    # Normalize distances to start from 0
    r = distances - distances[0]
    y = intensities.copy()

    # Remove any remaining NaN
    valid = ~np.isnan(y)
    if np.sum(valid) < 3:
        return 0.0, 0.0, 0.0, 0.0
    r = r[valid]
    y = y[valid]

    # Initial estimates
    baseline_est = float(np.min(y[-max(1, len(y) // 10):]))  # far-field baseline
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

    # Grid search around initial estimates
    best_sigma = sigma_est
    best_amp = amplitude_est
    best_base = baseline_est
    best_r2 = -np.inf

    for sigma_mult in [0.3, 0.5, 0.7, 1.0, 1.3, 1.6, 2.0, 2.5, 3.0]:
        sigma_try = sigma_est * sigma_mult
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

    Produces both isotropic (radial) and anisotropic (sigma_x, sigma_y) fits,
    plus cross-validation against C46 calibration parameters.

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

    # --- Isotropic radial profile ---
    distances, intensities = _sample_radial_profile(gray, center, screen_mask)

    if len(distances) == 0 or np.all(np.isnan(intensities)):
        return GlowProfile(
            filename=basename, image_size=(w, h),
            screen_center=center, screen_bbox=bbox, screen_area_frac=screen_area_frac,
            sigma_px=0.0, sigma_frac=0.0, amplitude=0.0, baseline=0.0,
            fwhm_px=0.0, fwhm_frac=0.0, r_squared=0.0,
            screen_rgb_mean=screen_rgb_mean,
            error="Insufficient radial profile data",
        )

    sigma, amplitude, baseline, r_squared = _fit_gaussian_falloff(distances, intensities)
    fwhm = sigma * _FWHM_FACTOR
    sigma_frac = sigma / diag if diag > 0 else 0.0
    fwhm_frac = fwhm / diag if diag > 0 else 0.0

    # Generate fitted curve for visualization
    r_from_edge = distances - distances[0]
    fitted_curve = amplitude * np.exp(-r_from_edge ** 2 / (2.0 * sigma ** 2)) + baseline

    # --- Anisotropic axis profiles ---
    # Horizontal (x-axis)
    dist_x, lum_x = _sample_axis_profile(gray, center, screen_mask, axis="x")
    if len(dist_x) >= 3:
        sigma_x, amp_x, base_x, r2_x = _fit_gaussian_falloff(dist_x, lum_x)
    else:
        sigma_x, amp_x, base_x, r2_x = 0.0, 0.0, 0.0, 0.0

    # Vertical (y-axis)
    dist_y, lum_y = _sample_axis_profile(gray, center, screen_mask, axis="y")
    if len(dist_y) >= 3:
        sigma_y, amp_y, base_y, r2_y = _fit_gaussian_falloff(dist_y, lum_y)
    else:
        sigma_y, amp_y, base_y, r2_y = 0.0, 0.0, 0.0, 0.0

    # Anisotropy ratio
    anisotropy_ratio = (sigma_x / sigma_y) if sigma_y > 0 else 1.0

    # Axis-relative fractions (sigma_x / width, sigma_y / height)
    sigma_x_frac = sigma_x / w if w > 0 else 0.0
    sigma_y_frac = sigma_y / h if h > 0 else 0.0
    fwhm_x_px = sigma_x * _FWHM_FACTOR
    fwhm_y_px = sigma_y * _FWHM_FACTOR
    fwhm_x_frac = fwhm_x_px / w if w > 0 else 0.0
    fwhm_y_frac = fwhm_y_px / h if h > 0 else 0.0

    # --- Cross-validation against C46 ---
    c46_delta = sigma_frac - _C46_REF_SIGMA_FRAC
    c46_delta_pct = (c46_delta / _C46_REF_SIGMA_FRAC * 100.0) if _C46_REF_SIGMA_FRAC > 0 else 0.0

    # --- Glow spill color ---
    screen_edge_r = distances[0]
    glow_inner = screen_edge_r
    glow_sigma = sigma if sigma > 0 else 1.0
    glow_outer = screen_edge_r + glow_sigma * 1.5

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
        # Isotropic
        sigma_px=sigma,
        sigma_frac=sigma_frac,
        amplitude=amplitude,
        baseline=baseline,
        fwhm_px=fwhm,
        fwhm_frac=fwhm_frac,
        r_squared=r_squared,
        # Anisotropic
        sigma_x_px=sigma_x,
        sigma_y_px=sigma_y,
        sigma_x_frac=sigma_x_frac,
        sigma_y_frac=sigma_y_frac,
        fwhm_x_px=fwhm_x_px,
        fwhm_y_px=fwhm_y_px,
        fwhm_x_frac=fwhm_x_frac,
        fwhm_y_frac=fwhm_y_frac,
        amplitude_x=amp_x,
        amplitude_y=amp_y,
        baseline_x=base_x,
        baseline_y=base_y,
        r_squared_x=r2_x,
        r_squared_y=r2_y,
        anisotropy_ratio=anisotropy_ratio,
        # C46 cross-validation
        c46_sigma_frac_ref=_C46_REF_SIGMA_FRAC,
        c46_sigma_frac_delta=c46_delta,
        c46_sigma_frac_delta_pct=c46_delta_pct,
        # Color
        glow_color_temp_K=glow_color_temp,
        glow_rgb_mean=glow_rgb_mean,
        screen_rgb_mean=screen_rgb_mean,
        # Curves
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
    lines.append("=" * 120)
    lines.append("CRT Glow Profile Extraction Report  (v2.0.0 — anisotropic)")
    lines.append("=" * 120)
    lines.append("")

    # Isotropic table
    lines.append("--- ISOTROPIC (radial average) ---")
    header = (
        f"{'Filename':<55} {'FWHM_px':>8} {'FWHM%':>6} "
        f"{'Amp':>5} {'Base':>5} {'R^2':>5} {'CCT_K':>7} {'GlowRGB':>15} "
        f"{'C46_d%':>7}"
    )
    lines.append(header)
    lines.append("-" * len(header))

    valid = []
    for p in profiles:
        if p.error:
            lines.append(f"{p.filename:<55} ERROR: {p.error}")
            continue
        c46_tag = f"{p.c46_sigma_frac_delta_pct:>+6.1f}%" if p.r_squared > 0.3 else "   N/A"
        lines.append(
            f"{p.filename:<55} {p.fwhm_px:>8.1f} {p.fwhm_frac * 100:>5.1f}% "
            f"{p.amplitude:>5.1f} {p.baseline:>5.1f} {p.r_squared:>5.3f} "
            f"{p.glow_color_temp_K or 0:>7.0f} "
            f"({p.glow_rgb_mean[0]:>3},{p.glow_rgb_mean[1]:>3},{p.glow_rgb_mean[2]:>3}) "
            f"{c46_tag}"
        )
        valid.append(p)

    # Anisotropic table
    lines.append("")
    lines.append("--- ANISOTROPIC (σ_x horizontal / σ_y vertical) ---")
    aheader = (
        f"{'Filename':<55} {'σ_x':>7} {'σ_y':>7} "
        f"{'FWHM_x%':>8} {'FWHM_y%':>8} {'R²_x':>5} {'R²_y':>5} {'σ_x/σ_y':>8}"
    )
    lines.append(aheader)
    lines.append("-" * len(aheader))

    for p in valid:
        lines.append(
            f"{p.filename:<55} {p.sigma_x_px:>7.1f} {p.sigma_y_px:>7.1f} "
            f"{p.fwhm_x_frac * 100:>7.1f}% {p.fwhm_y_frac * 100:>7.1f}% "
            f"{p.r_squared_x:>5.3f} {p.r_squared_y:>5.3f} "
            f"{p.anisotropy_ratio:>8.3f}"
        )

    # Aggregate statistics
    if valid:
        lines.append("")
        lines.append("-" * 80)
        lines.append("AGGREGATE STATISTICS (R^2 > 0.5 filter for isotropic)")
        lines.append("-" * 80)

        good_iso = [p for p in valid if p.r_squared > 0.5]
        fwhms = [p.fwhm_frac for p in good_iso]
        amps = [p.amplitude for p in good_iso]
        bases = [p.baseline for p in good_iso]
        ccts = [p.glow_color_temp_K for p in good_iso if p.glow_color_temp_K is not None]

        if fwhms:
            lines.append(f"  Isotropic FWHM (% diag): mean={np.mean(fwhms) * 100:.1f}%, "
                         f"median={np.median(fwhms) * 100:.1f}%, "
                         f"range=[{np.min(fwhms) * 100:.1f}%, {np.max(fwhms) * 100:.1f}%]")
        if amps:
            lines.append(f"  Amplitude: mean={np.mean(amps):.1f}, "
                         f"median={np.median(amps):.1f}")
        if bases:
            lines.append(f"  Baseline: mean={np.mean(bases):.1f}, "
                         f"median={np.median(bases):.1f}")
        if ccts:
            lines.append(f"  Color Temp: mean={np.mean(ccts):.0f}K, "
                         f"median={np.median(ccts):.0f}K")

        # Anisotropic aggregate (R^2 > 0.5 on BOTH axes)
        good_aniso = [p for p in valid if p.r_squared_x > 0.5 and p.r_squared_y > 0.5]
        if good_aniso:
            sx = [p.sigma_x_frac for p in good_aniso]
            sy = [p.sigma_y_frac for p in good_aniso]
            ratios = [p.anisotropy_ratio for p in good_aniso]
            lines.append("")
            lines.append(f"  Anisotropic ({len(good_aniso)} good fits, R^2_x > 0.5 AND R^2_y > 0.5):")
            lines.append(f"    σ_x/W: mean={np.mean(sx):.4f}, median={np.median(sx):.4f}")
            lines.append(f"    σ_y/H: mean={np.mean(sy):.4f}, median={np.median(sy):.4f}")
            lines.append(f"    σ_x/σ_y ratio: mean={np.mean(ratios):.3f}, "
                         f"median={np.median(ratios):.3f}, "
                         f"range=[{np.min(ratios):.3f}, {np.max(ratios):.3f}]")

        # Cross-validation summary
        lines.append("")
        lines.append("CROSS-VALIDATION vs C46 (sigma_frac ref = 0.1165, FWHM ref = 27.4%)")
        if good_iso:
            sigma_fracs = [p.sigma_frac for p in good_iso]
            lines.append(f"  This run sigma_frac: mean={np.mean(sigma_fracs):.4f}, "
                         f"median={np.median(sigma_fracs):.4f}")
            mean_delta_pct = (np.mean(sigma_fracs) - _C46_REF_SIGMA_FRAC) / _C46_REF_SIGMA_FRAC * 100
            lines.append(f"  Mean deviation from C46: {mean_delta_pct:+.1f}%")
            if abs(mean_delta_pct) < 15:
                lines.append("  VERDICT: CONSISTENT with C46 calibration (within 15%)")
            elif abs(mean_delta_pct) < 30:
                lines.append("  VERDICT: MODERATE deviation from C46 (15-30%) — review reference set")
            else:
                lines.append("  VERDICT: LARGE deviation from C46 (>30%) — different reference population?")
        else:
            lines.append("  No good isotropic fits to compare")

        # Recommended parameters
        lines.append("")
        lines.append("RECOMMENDED GLOW PARAMETERS (for generator calibration):")
        if fwhms:
            lines.append(f"  sigma_frac = {np.median(fwhms) / _FWHM_FACTOR:.4f}  "
                         f"(median sigma as fraction of canvas diagonal)")
            lines.append(f"  fwhm_frac  = {np.median(fwhms):.4f}  "
                         f"(median FWHM as fraction of canvas diagonal)")
        if good_aniso:
            lines.append(f"  sigma_x_frac = {np.median(sx):.4f}  "
                         f"(median horizontal sigma / image width)")
            lines.append(f"  sigma_y_frac = {np.median(sy):.4f}  "
                         f"(median vertical sigma / image height)")
            lines.append(f"  anisotropy   = {np.median(ratios):.3f}  "
                         f"(median σ_x/σ_y ratio)")
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
        n_good = len(good_iso)
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
        description="CRT Glow Profile Extraction Tool (v2.0.0 — anisotropic)"
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
