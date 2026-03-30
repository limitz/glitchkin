#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_depth_temp_lint.py
===========================
Depth Temperature Grammar Linter for "Luma & the Glitchkin."

Validates the Depth Temperature Rule (codified C45, docs/image-rules.md):
    Warm color = foreground. Cool color = background.

In any multi-character or multi-tier composition, the warm/cool split is the
primary depth cue. This tool measures average color temperature per depth tier
and reports PASS/WARN/FAIL.

Tier detection:
    - Default tier positions derived from LTG_TOOL_character_lineup.py v008
      geometry: FG_GROUND_Y = 78% of image height, BG_GROUND_Y = 70%.
    - Each tier is sampled as a horizontal band: a strip of pixels centered
      on the ground-plane Y coordinate (configurable band height).
    - Custom tier positions can be supplied via CLI or API for non-lineup
      compositions (style frames, multi-character scene panels).

Temperature measurement:
    - Per-pixel warmth score: R_channel - B_channel (positive = warm, neg = cool).
    - Near-black pixels (R+G+B < 60) are excluded (background void / outlines).
    - Near-white pixels (R+G+B > 700) are excluded (highlight blow-out).
    - Per-tier average warmth reported as a signed float.
    - Separation = FG_warmth - BG_warmth. Positive = correct depth grammar.

Scoring:
    PASS  — FG warmer than BG by >= threshold (default 12.0 for REAL_INTERIOR)
    WARN  — FG warmer than BG but separation < threshold
    FAIL  — FG cooler than or equal to BG (inverted depth grammar)
    SKIP  — Glitch Layer scene (exempt per rule), or image not on disk

The REAL_INTERIOR threshold of 12.0 matches world_type_infer.py v1.2.0.

Usage (CLI):
    python LTG_TOOL_depth_temp_lint.py path/to/image.png
    python LTG_TOOL_depth_temp_lint.py --fg-y 0.78 --bg-y 0.70 path/to/image.png
    python LTG_TOOL_depth_temp_lint.py --band 40 --threshold 8.0 path/to/image.png
    python LTG_TOOL_depth_temp_lint.py --self-test
    python LTG_TOOL_depth_temp_lint.py --batch dir_or_file [dir_or_file ...]

Usage (module API — for precritique_qa integration):
    from LTG_TOOL_depth_temp_lint import lint_depth_temperature
    result = lint_depth_temperature("path/to/image.png")
    # result = {"overall": "PASS"|"WARN"|"FAIL"|"SKIP",
    #           "fg_warmth": float, "bg_warmth": float,
    #           "separation": float, "threshold": float,
    #           "fg_pixels": int, "bg_pixels": int,
    #           "message": str, "path": str}

    from LTG_TOOL_depth_temp_lint import run_depth_temp_check
    batch_result = run_depth_temp_check(["img1.png", "img2.png"])
    # batch_result = {"overall": "PASS"|..., "pass": int, "warn": int,
    #                 "fail": int, "skip": int, "per_file": [...]}

Author: Lee Tanaka (Character Staging & Visual Acting Specialist)
Created: Cycle 46 — 2026-03-30
Version: 1.1.0

Version history:
    1.1.0 (C48) — Per-asset band override config support.
                   load_band_overrides() reads depth_temp_band_overrides.json.
                   lint_depth_temperature() accepts overrides dict.
                   run_depth_temp_check() accepts overrides dict, applies per-basename.
                   SF04/SF05 false positives resolve to PASS with correct band positions.
    1.0.0 (C46) — Initial release.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import numpy as np
    _NP_AVAILABLE = True
except ImportError:
    np = None  # type: ignore
    _NP_AVAILABLE = False

from PIL import Image

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent.parent

if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

# ---------------------------------------------------------------------------
# World-type inference (for threshold + GL exemption)
# ---------------------------------------------------------------------------
_world_type_mod = None


def _load_world_type_infer():
    """Lazily import LTG_TOOL_world_type_infer. Returns module or None."""
    global _world_type_mod
    if _world_type_mod is not None:
        return _world_type_mod
    try:
        import importlib.util as ilu
        spec = ilu.spec_from_file_location(
            "LTG_TOOL_world_type_infer",
            str(TOOLS_DIR / "LTG_TOOL_world_type_infer.py"),
        )
        mod = ilu.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _world_type_mod = mod
        return mod
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Default constants (from LTG_TOOL_character_lineup.py v008)
# ---------------------------------------------------------------------------

# Tier Y positions as fractions of image height
DEFAULT_FG_Y_FRAC = 0.78   # FG ground plane
DEFAULT_BG_Y_FRAC = 0.70   # BG ground plane

# Band height in pixels (half above, half below the ground Y)
DEFAULT_BAND_H = 50

# Default warm/cool separation threshold (REAL_INTERIOR)
DEFAULT_THRESHOLD = 12.0

# Pixel exclusion bounds (sum of RGB channels)
DARK_CUTOFF = 60    # R+G+B < 60 = near-black, skip
BRIGHT_CUTOFF = 700  # R+G+B > 700 = near-white, skip

# Glitch Layer world types — exempt from this rule
EXEMPT_WORLD_TYPES = {"GLITCH", "OTHER_SIDE"}

__version__ = "1.1.0"
__author__ = "Lee Tanaka"

# Per-asset band override config path
BAND_OVERRIDES_JSON = TOOLS_DIR / "depth_temp_band_overrides.json"


# ---------------------------------------------------------------------------
# Band override config loader
# ---------------------------------------------------------------------------

_band_overrides_cache = None


def load_band_overrides(
    config_path: Optional[str] = None,
) -> Dict[str, Dict]:
    """
    Load per-asset band position overrides from JSON config.

    The config file maps PNG basenames to override dicts with keys:
        fg_y_frac, bg_y_frac, band_h (optional), threshold (optional).

    Args:
        config_path: Path to JSON file. None = use default
                     (depth_temp_band_overrides.json in tools dir).

    Returns:
        Dict mapping basename -> override dict. Empty dict if file absent.
    """
    global _band_overrides_cache
    if config_path is None and _band_overrides_cache is not None:
        return _band_overrides_cache

    p = Path(config_path) if config_path else BAND_OVERRIDES_JSON
    if not p.is_file():
        if config_path is None:
            _band_overrides_cache = {}
        return {}

    try:
        with open(str(p), "r", encoding="utf-8") as f:
            data = json.load(f)
        overrides = data.get("overrides", {})
        result = {}
        for basename, entry in overrides.items():
            result[basename] = {
                k: v for k, v in entry.items()
                if k in ("fg_y_frac", "bg_y_frac", "band_h", "threshold", "label")
            }
        if config_path is None:
            _band_overrides_cache = result
        return result
    except Exception:
        if config_path is None:
            _band_overrides_cache = {}
        return {}


# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------

def _measure_strip_warmth(
    pixels: "np.ndarray",
) -> Tuple[float, int]:
    """
    Measure average warmth of a pixel strip.

    Args:
        pixels: numpy array of shape (N, 3) or (H, W, 3), dtype uint8/int.

    Returns:
        (avg_warmth, valid_pixel_count) where avg_warmth = mean(R - B)
        over non-excluded pixels. If no valid pixels, returns (0.0, 0).
    """
    if pixels.ndim == 3:
        pixels = pixels.reshape(-1, 3)

    pixels = pixels.astype(np.int32)
    R = pixels[:, 0]
    G = pixels[:, 1]
    B = pixels[:, 2]
    chan_sum = R + G + B

    # Exclude near-black and near-white
    mask = (chan_sum >= DARK_CUTOFF) & (chan_sum <= BRIGHT_CUTOFF)
    valid_count = int(mask.sum())
    if valid_count == 0:
        return 0.0, 0

    warmth_values = R[mask] - B[mask]
    avg_warmth = float(warmth_values.mean())
    return avg_warmth, valid_count


def _measure_strip_warmth_pil(
    img: Image.Image,
    y_start: int,
    y_end: int,
) -> Tuple[float, int]:
    """
    Pure-PIL fallback for measuring warmth of a horizontal strip.

    Args:
        img: PIL Image in RGB mode.
        y_start, y_end: row range [y_start, y_end).

    Returns:
        (avg_warmth, valid_pixel_count).
    """
    w = img.width
    total_warmth = 0.0
    count = 0
    for y in range(max(0, y_start), min(img.height, y_end)):
        for x in range(w):
            r, g, b = img.getpixel((x, y))[:3]
            s = r + g + b
            if s < DARK_CUTOFF or s > BRIGHT_CUTOFF:
                continue
            total_warmth += (r - b)
            count += 1
    if count == 0:
        return 0.0, 0
    return total_warmth / count, count


def _extract_strip(
    img: Image.Image,
    y_center: int,
    band_h: int,
) -> Tuple[int, int]:
    """Compute clamped y_start, y_end for a strip centered at y_center."""
    half = band_h // 2
    y_start = max(0, y_center - half)
    y_end = min(img.height, y_center + half)
    return y_start, y_end


# ---------------------------------------------------------------------------
# Public API: single-image lint
# ---------------------------------------------------------------------------

def lint_depth_temperature(
    image_path: str,
    fg_y_frac: float = DEFAULT_FG_Y_FRAC,
    bg_y_frac: float = DEFAULT_BG_Y_FRAC,
    band_h: int = DEFAULT_BAND_H,
    threshold: Optional[float] = None,
    world_type_override: Optional[str] = None,
    overrides: Optional[Dict[str, Dict]] = None,
) -> Dict:
    """
    Lint a single image for Depth Temperature Rule compliance.

    Args:
        image_path: Path to the PNG/JPG to analyse.
        fg_y_frac: Foreground ground-plane Y as fraction of image height (0.0-1.0).
        bg_y_frac: Background ground-plane Y as fraction of image height (0.0-1.0).
        band_h: Height of the sampling band in pixels.
        threshold: Warm/cool separation threshold. None = auto from world_type_infer.
        world_type_override: Force a world type (e.g. "GLITCH" to force SKIP).
        overrides: Per-asset band override dict (basename -> {fg_y_frac, bg_y_frac, ...}).
                   If None, loads from depth_temp_band_overrides.json automatically.
                   Pass an empty dict {} to disable override loading.

    Returns:
        Dict with keys: overall, fg_warmth, bg_warmth, separation, threshold,
                        fg_pixels, bg_pixels, message, path, world_type.
    """
    path_str = str(image_path)
    basename = os.path.basename(path_str)

    # Apply per-asset band overrides (from JSON config or caller)
    if overrides is None:
        overrides = load_band_overrides()
    asset_override = overrides.get(basename, {})
    if asset_override:
        fg_y_frac = asset_override.get("fg_y_frac", fg_y_frac)
        bg_y_frac = asset_override.get("bg_y_frac", bg_y_frac)
        band_h = asset_override.get("band_h", band_h)
        if threshold is None and "threshold" in asset_override:
            threshold = asset_override["threshold"]

    # Check file exists
    if not os.path.isfile(path_str):
        return {
            "overall": "SKIP",
            "fg_warmth": 0.0,
            "bg_warmth": 0.0,
            "separation": 0.0,
            "threshold": 0.0,
            "fg_pixels": 0,
            "bg_pixels": 0,
            "message": f"File not found: {basename}",
            "path": path_str,
            "world_type": None,
        }

    # Determine world type and threshold
    wt_mod = _load_world_type_infer()
    if world_type_override:
        world_type = world_type_override.upper()
    elif wt_mod:
        world_type = wt_mod.infer_world_type(basename)
    else:
        world_type = None

    # Exempt Glitch Layer scenes
    if world_type in EXEMPT_WORLD_TYPES:
        return {
            "overall": "SKIP",
            "fg_warmth": 0.0,
            "bg_warmth": 0.0,
            "separation": 0.0,
            "threshold": 0.0,
            "fg_pixels": 0,
            "bg_pixels": 0,
            "message": f"SKIP: {world_type} scene exempt from Depth Temperature Rule",
            "path": path_str,
            "world_type": world_type,
        }

    # Resolve threshold
    if threshold is not None:
        thr = threshold
    elif wt_mod:
        thr = wt_mod.get_warm_cool_threshold(world_type)
    else:
        thr = DEFAULT_THRESHOLD

    # Load image
    try:
        img = Image.open(path_str).convert("RGB")
    except Exception as e:
        return {
            "overall": "FAIL",
            "fg_warmth": 0.0,
            "bg_warmth": 0.0,
            "separation": 0.0,
            "threshold": thr,
            "fg_pixels": 0,
            "bg_pixels": 0,
            "message": f"Cannot open image: {e}",
            "path": path_str,
            "world_type": world_type,
        }

    h = img.height

    # Compute tier Y positions
    fg_y = int(h * fg_y_frac)
    bg_y = int(h * bg_y_frac)

    # Extract strips
    fg_start, fg_end = _extract_strip(img, fg_y, band_h)
    bg_start, bg_end = _extract_strip(img, bg_y, band_h)

    # Measure warmth
    if _NP_AVAILABLE:
        arr = np.array(img)
        fg_strip = arr[fg_start:fg_end, :, :]
        bg_strip = arr[bg_start:bg_end, :, :]
        fg_warmth, fg_px = _measure_strip_warmth(fg_strip)
        bg_warmth, bg_px = _measure_strip_warmth(bg_strip)
    else:
        fg_warmth, fg_px = _measure_strip_warmth_pil(img, fg_start, fg_end)
        bg_warmth, bg_px = _measure_strip_warmth_pil(img, bg_start, bg_end)

    separation = fg_warmth - bg_warmth

    # Determine grade
    min_pixels = 50  # need at least this many valid pixels per tier
    if fg_px < min_pixels or bg_px < min_pixels:
        overall = "WARN"
        msg = (
            f"Insufficient valid pixels (FG={fg_px}, BG={bg_px}; min={min_pixels}). "
            f"FG warmth={fg_warmth:.1f}, BG warmth={bg_warmth:.1f}, sep={separation:.1f}"
        )
    elif separation >= thr:
        overall = "PASS"
        msg = (
            f"PASS: FG warmth={fg_warmth:.1f}, BG warmth={bg_warmth:.1f}, "
            f"separation={separation:.1f} >= threshold {thr:.1f}"
        )
    elif separation > 0:
        overall = "WARN"
        msg = (
            f"WARN: FG warmer than BG but separation insufficient. "
            f"FG={fg_warmth:.1f}, BG={bg_warmth:.1f}, sep={separation:.1f} < {thr:.1f}"
        )
    else:
        overall = "FAIL"
        msg = (
            f"FAIL: Depth temperature INVERTED. FG={fg_warmth:.1f}, BG={bg_warmth:.1f}, "
            f"sep={separation:.1f}. Expected warm FG / cool BG."
        )

    return {
        "overall": overall,
        "fg_warmth": round(fg_warmth, 2),
        "bg_warmth": round(bg_warmth, 2),
        "separation": round(separation, 2),
        "threshold": thr,
        "fg_pixels": fg_px,
        "bg_pixels": bg_px,
        "message": msg,
        "path": path_str,
        "world_type": world_type,
        "fg_y_frac": fg_y_frac,
        "bg_y_frac": bg_y_frac,
        "band_override": bool(asset_override),
    }


# ---------------------------------------------------------------------------
# Public API: batch check (for precritique_qa integration)
# ---------------------------------------------------------------------------

def run_depth_temp_check(
    image_paths: List[str],
    fg_y_frac: float = DEFAULT_FG_Y_FRAC,
    bg_y_frac: float = DEFAULT_BG_Y_FRAC,
    band_h: int = DEFAULT_BAND_H,
    threshold: Optional[float] = None,
    overrides: Optional[Dict[str, Dict]] = None,
) -> Dict:
    """
    Run depth temperature lint on a list of image paths.

    Args:
        image_paths: List of paths to lint.
        fg_y_frac: Default FG Y fraction (overridden per-asset if in overrides).
        bg_y_frac: Default BG Y fraction (overridden per-asset if in overrides).
        band_h: Default band height (overridden per-asset if in overrides).
        threshold: Default threshold (overridden per-asset if in overrides).
        overrides: Per-asset band override dict. None = load from JSON config.

    Returns a dict matching precritique_qa section conventions:
        {
            "overall":  "PASS" | "WARN" | "FAIL",
            "pass":     int,
            "warn":     int,
            "fail":     int,
            "skip":     int,
            "per_file": [result_dict, ...],
        }
    """
    # Load overrides once for the batch
    if overrides is None:
        overrides = load_band_overrides()

    pass_count = 0
    warn_count = 0
    fail_count = 0
    skip_count = 0
    per_file = []

    for p in image_paths:
        res = lint_depth_temperature(
            p,
            fg_y_frac=fg_y_frac,
            bg_y_frac=bg_y_frac,
            band_h=band_h,
            threshold=threshold,
            overrides=overrides,
        )
        per_file.append(res)
        grade = res["overall"]
        if grade == "PASS":
            pass_count += 1
        elif grade == "WARN":
            warn_count += 1
        elif grade == "FAIL":
            fail_count += 1
        else:
            skip_count += 1

    if fail_count > 0:
        overall = "FAIL"
    elif warn_count > 0:
        overall = "WARN"
    elif pass_count > 0:
        overall = "PASS"
    else:
        overall = "PASS"  # all skipped = no failures

    return {
        "overall": overall,
        "pass": pass_count,
        "warn": warn_count,
        "fail": fail_count,
        "skip": skip_count,
        "per_file": per_file,
    }


# ---------------------------------------------------------------------------
# Self-test: synthetic image generation
# ---------------------------------------------------------------------------

def _self_test() -> bool:
    """
    Generate synthetic test images and verify all three outcomes
    (PASS, WARN, FAIL) are correctly detected.

    Returns True if all tests pass.
    """
    from PIL import ImageDraw

    print("[self-test] Generating synthetic depth temperature test images...")
    test_dir = REPO_ROOT / "output" / "production"
    test_dir.mkdir(parents=True, exist_ok=True)

    W, H = 400, 300
    fg_y = int(H * DEFAULT_FG_Y_FRAC)  # ~234
    bg_y = int(H * DEFAULT_BG_Y_FRAC)  # ~210
    band_half = DEFAULT_BAND_H // 2

    all_pass = True

    # --- Test 1: PASS (warm FG, cool BG, big separation) ---
    img = Image.new("RGB", (W, H), (180, 190, 210))  # cool base
    draw = ImageDraw.Draw(img)
    # FG band: warm amber
    draw.rectangle(
        [0, fg_y - band_half, W, fg_y + band_half],
        fill=(220, 190, 140),
    )
    # BG band: cool slate
    draw.rectangle(
        [0, bg_y - band_half, W, bg_y + band_half],
        fill=(160, 175, 200),
    )
    pass_path = str(test_dir / "LTG_SNAP_depth_temp_test_PASS.png")
    img.save(pass_path)

    res = lint_depth_temperature(pass_path, threshold=12.0)
    status = "OK" if res["overall"] == "PASS" else "FAIL"
    if res["overall"] != "PASS":
        all_pass = False
    print(f"  Test PASS image: {res['overall']} (expected PASS) [{status}]")
    print(f"    FG={res['fg_warmth']:.1f}, BG={res['bg_warmth']:.1f}, sep={res['separation']:.1f}")

    # --- Test 2: WARN (FG slightly warmer, under threshold) ---
    img2 = Image.new("RGB", (W, H), (180, 185, 195))
    draw2 = ImageDraw.Draw(img2)
    # FG band: slightly warm
    draw2.rectangle(
        [0, fg_y - band_half, W, fg_y + band_half],
        fill=(195, 185, 180),
    )
    # BG band: slightly cool
    draw2.rectangle(
        [0, bg_y - band_half, W, bg_y + band_half],
        fill=(180, 185, 190),
    )
    warn_path = str(test_dir / "LTG_SNAP_depth_temp_test_WARN.png")
    img2.save(warn_path)

    res2 = lint_depth_temperature(warn_path, threshold=12.0)
    status2 = "OK" if res2["overall"] == "WARN" else "FAIL"
    if res2["overall"] != "WARN":
        all_pass = False
    print(f"  Test WARN image: {res2['overall']} (expected WARN) [{status2}]")
    print(f"    FG={res2['fg_warmth']:.1f}, BG={res2['bg_warmth']:.1f}, sep={res2['separation']:.1f}")

    # --- Test 3: FAIL (inverted — cool FG, warm BG) ---
    img3 = Image.new("RGB", (W, H), (185, 185, 185))
    draw3 = ImageDraw.Draw(img3)
    # FG band: cool
    draw3.rectangle(
        [0, fg_y - band_half, W, fg_y + band_half],
        fill=(160, 175, 210),
    )
    # BG band: warm
    draw3.rectangle(
        [0, bg_y - band_half, W, bg_y + band_half],
        fill=(220, 190, 140),
    )
    fail_path = str(test_dir / "LTG_SNAP_depth_temp_test_FAIL.png")
    img3.save(fail_path)

    res3 = lint_depth_temperature(fail_path, threshold=12.0)
    status3 = "OK" if res3["overall"] == "FAIL" else "FAIL"
    if res3["overall"] != "FAIL":
        all_pass = False
    print(f"  Test FAIL image: {res3['overall']} (expected FAIL) [{status3}]")
    print(f"    FG={res3['fg_warmth']:.1f}, BG={res3['bg_warmth']:.1f}, sep={res3['separation']:.1f}")

    # --- Test 4: SKIP (Glitch Layer exempt) ---
    skip_path = str(test_dir / "LTG_SNAP_depth_temp_test_SKIP.png")
    img.save(skip_path)  # reuse PASS image
    res4 = lint_depth_temperature(skip_path, world_type_override="GLITCH")
    status4 = "OK" if res4["overall"] == "SKIP" else "FAIL"
    if res4["overall"] != "SKIP":
        all_pass = False
    print(f"  Test SKIP (GL exempt): {res4['overall']} (expected SKIP) [{status4}]")

    # --- Test 5: batch API ---
    batch_res = run_depth_temp_check([pass_path, warn_path, fail_path])
    batch_ok = (
        batch_res["overall"] == "FAIL"
        and batch_res["pass"] == 1
        and batch_res["warn"] == 1
        and batch_res["fail"] == 1
    )
    status5 = "OK" if batch_ok else "FAIL"
    if not batch_ok:
        all_pass = False
    print(f"  Test batch API: overall={batch_res['overall']} p={batch_res['pass']} "
          f"w={batch_res['warn']} f={batch_res['fail']} [{status5}]")

    if all_pass:
        print("\n[self-test] ALL TESTS PASSED")
    else:
        print("\n[self-test] SOME TESTS FAILED")
    return all_pass


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Depth Temperature Grammar Linter — warm=FG, cool=BG rule check.",
    )
    p.add_argument(
        "images",
        nargs="*",
        help="Image file(s) or directory to lint.",
    )
    p.add_argument(
        "--fg-y",
        type=float,
        default=DEFAULT_FG_Y_FRAC,
        help=f"FG ground-plane Y as fraction of height (default: {DEFAULT_FG_Y_FRAC})",
    )
    p.add_argument(
        "--bg-y",
        type=float,
        default=DEFAULT_BG_Y_FRAC,
        help=f"BG ground-plane Y as fraction of height (default: {DEFAULT_BG_Y_FRAC})",
    )
    p.add_argument(
        "--band",
        type=int,
        default=DEFAULT_BAND_H,
        help=f"Band height in pixels (default: {DEFAULT_BAND_H})",
    )
    p.add_argument(
        "--threshold",
        type=float,
        default=None,
        help=f"Warm/cool separation threshold (default: auto from world type, fallback {DEFAULT_THRESHOLD})",
    )
    p.add_argument(
        "--world-type",
        type=str,
        default=None,
        help="Force a world type (REAL, REAL_INTERIOR, REAL_STORM, GLITCH, OTHER_SIDE).",
    )
    p.add_argument(
        "--self-test",
        action="store_true",
        help="Run built-in self-test with synthetic images.",
    )
    p.add_argument(
        "--batch",
        action="store_true",
        help="Treat arguments as directories — lint all PNGs inside.",
    )
    return p


def main():
    parser = _build_parser()
    args = parser.parse_args()

    if args.self_test:
        ok = _self_test()
        return 0 if ok else 2

    if not args.images:
        parser.print_help()
        return 1

    # Gather files
    paths = []
    for item in args.images:
        p = Path(item)
        if p.is_dir() or args.batch:
            if p.is_dir():
                paths.extend(sorted(str(f) for f in p.glob("*.png")))
            else:
                paths.append(str(p))
        else:
            paths.append(str(p))

    if not paths:
        print("No PNG files found.")
        return 1

    # Run lint
    results = run_depth_temp_check(
        paths,
        fg_y_frac=args.fg_y,
        bg_y_frac=args.bg_y,
        band_h=args.band,
        threshold=args.threshold,
    )

    # Print results
    print(f"\nDepth Temperature Lint — {len(paths)} file(s)")
    print("=" * 60)
    for res in results["per_file"]:
        grade = res["overall"]
        bn = os.path.basename(res["path"])
        if grade == "SKIP":
            print(f"  [{grade}] {bn}: {res['message']}")
        else:
            print(f"  [{grade}] {bn}: FG={res['fg_warmth']:.1f} BG={res['bg_warmth']:.1f} "
                  f"sep={res['separation']:.1f} (thr={res['threshold']:.1f})")
    print("=" * 60)
    print(f"OVERALL: {results['overall']}  "
          f"(PASS={results['pass']} WARN={results['warn']} "
          f"FAIL={results['fail']} SKIP={results['skip']})")

    if results["overall"] == "PASS":
        return 0
    elif results["overall"] == "WARN":
        return 1
    else:
        return 2


if __name__ == "__main__":
    sys.exit(main())
