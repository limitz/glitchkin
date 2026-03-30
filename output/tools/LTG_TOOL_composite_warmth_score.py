# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_composite_warmth_score.py
====================================
Composite Warmth Score for "Luma & the Glitchkin."

Combines two independent metrics into a single per-asset warmth score:
  1. Warm-pixel-percentage (from LTG_TOOL_warm_pixel_metric.py)
  2. Hue-split separation (from LTG_TOOL_warmcool_scene_calibrate.py)

Why: Each metric captures a different aspect of warmth. Warm-pixel-percentage
measures how much of the frame is warm-hued. Hue-split measures how spatially
separated warm and cool zones are (top vs bottom half). A composite score
gives a unified Real World warmth assessment — high composite = warm interior,
low composite = cold/alien environment.

Formula:
  composite = (w_pixel * norm_warm_pct) + (w_split * norm_hue_split)

Where:
  - norm_warm_pct = warm_pct / 100 (0.0 to 1.0)
  - norm_hue_split = min(hue_split / 127.5, 1.0) (0.0 to 1.0, capped at max)
  - w_pixel = 0.7 (warm-pixel-percentage carries more signal for single-temp scenes)
  - w_split = 0.3 (hue-split adds value for mixed-temp scenes like SF02)
  - Weights sum to 1.0. Score range: 0.0 to 1.0.

Weight rationale: Warm-pixel-percentage correctly classifies all 31 tested assets
(C47 validation) while hue-split fails for single-temperature-dominant scenes
(FP-006). Warm-pixel-percentage gets 70% weight. Hue-split retains 30% weight
because it captures spatial temperature variation that warm-pixel-percentage
misses (e.g., SF02 contested warm/cool lower third).

Thresholds (derived from C47 warm_pixel_metric calibration + C46 calibrate data):
  REAL_INTERIOR: composite >= 0.25
  REAL_STORM:    composite >= 0.04
  GLITCH:        composite <= 0.12
  OTHER_SIDE:    composite <= 0.04

Author: Sam Kowalski (Color & Style Artist)
Created: Cycle 48 — 2026-03-30
Version: 1.0.0

Usage:
  # Single image
  python3 LTG_TOOL_composite_warmth_score.py path/to/image.png

  # Single image with world type override
  python3 LTG_TOOL_composite_warmth_score.py path/to/image.png --world REAL_INTERIOR

  # Batch directory
  python3 LTG_TOOL_composite_warmth_score.py --batch output/backgrounds/environments/

  # Batch multiple directories
  python3 LTG_TOOL_composite_warmth_score.py --batch "reference/living room night" --batch "reference/kitchen predawn"

  # Generate report
  python3 LTG_TOOL_composite_warmth_score.py --batch output/backgrounds/environments/ --report output/production/composite_warmth_report_c48.md

Dependencies: PIL/Pillow, NumPy (both authorized per pil-standards.md)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
from PIL import Image

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# PIL HSV hue ranges (0-255 scale) — must match warm_pixel_metric and calibrate
WARM_HUE_LOW = 42
WARM_HUE_HIGH = 213
COOL_HUE_LOW = 85
COOL_HUE_HIGH = 170

# Minimum saturation to count as chromatic
MIN_SATURATION = 0.05

# Composite weights (sum to 1.0)
W_PIXEL = 0.7   # warm-pixel-percentage weight
W_SPLIT = 0.3   # hue-split separation weight

# Max hue-split for normalization (PIL 0-255 circular, max distance = 127.5)
MAX_HUE_SPLIT = 127.5

# Composite thresholds per world type
COMPOSITE_THRESHOLDS = {
    "REAL_INTERIOR": {"min": 0.25, "max": None,  "direction": "above"},
    "REAL_STORM":    {"min": 0.04, "max": None,  "direction": "above"},
    "GLITCH":        {"min": None, "max": 0.12,  "direction": "below"},
    "OTHER_SIDE":    {"min": None, "max": 0.04,  "direction": "below"},
}

# Supported image extensions
SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
UNSUPPORTED_EXTS = {".avif"}

# World-type inference keywords (from warm_pixel_metric)
_WORLD_TYPE_KEYWORDS = {
    "OTHER_SIDE": ["other_side", "otherside", "sf03", "style_frame_03"],
    "GLITCH": ["glitch_layer", "glitchlayer", "glitch_encounter",
               "covetous_glitch", "glitch_showcase"],
    "REAL_STORM": ["glitch_storm", "storm_sf", "sf02", "style_frame_02",
                   "storm_bg"],
}


# ---------------------------------------------------------------------------
# Core metric: warm-pixel-percentage (reused from warm_pixel_metric)
# ---------------------------------------------------------------------------

def _compute_hue_and_masks(arr: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute PIL-scale hue array and warm/cool/chromatic masks from a float32 RGB array.

    Args:
        arr: (H, W, 3) float32 array, values 0.0-1.0

    Returns:
        (hue_pil, warm_mask, cool_mask, chromatic_mask) — all (H, W) arrays.
    """
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    cmax = np.maximum(np.maximum(r, g), b)
    cmin = np.minimum(np.minimum(r, g), b)
    delta = cmax - cmin
    cmax_safe = np.where(cmax > 0, cmax, 1.0)
    sat = np.where(cmax > 0, delta / cmax_safe, 0.0)

    chromatic = sat >= MIN_SATURATION

    # Hue on 0-6 scale for chromatic pixels
    hue = np.zeros_like(delta)
    d_safe = np.where(delta > 0, delta, 1.0)

    r_mask = chromatic & (cmax == r)
    g_mask = chromatic & (~r_mask) & (cmax == g)
    b_mask = chromatic & (~r_mask) & (~g_mask) & (cmax == b)

    hue[r_mask] = ((g[r_mask] - b[r_mask]) / d_safe[r_mask]) % 6.0
    hue[g_mask] = ((b[g_mask] - r[g_mask]) / d_safe[g_mask]) + 2.0
    hue[b_mask] = ((r[b_mask] - g[b_mask]) / d_safe[b_mask]) + 4.0

    hue_pil = (hue / 6.0) * 255.0

    warm_mask = chromatic & ((hue_pil <= WARM_HUE_LOW) | (hue_pil >= WARM_HUE_HIGH))
    cool_mask = chromatic & (hue_pil >= COOL_HUE_LOW) & (hue_pil <= COOL_HUE_HIGH)

    return hue_pil, warm_mask, cool_mask, chromatic


def measure_warm_pixel_percentage(img: Image.Image) -> Dict:
    """
    Measure warm, cool, and neutral pixel percentages.

    Returns dict with: warm_pct, cool_pct, neutral_pct, warm_count, cool_count,
    neutral_count, total_pixels, chromatic_warm_pct, warm_cool_ratio.
    """
    rgb = img.convert("RGB")
    arr = np.array(rgb, dtype=np.float32) / 255.0

    hue_pil, warm_mask, cool_mask, chromatic = _compute_hue_and_masks(arr)

    neutral_mask = ~warm_mask & ~cool_mask

    total = int(arr[:, :, 0].size)
    warm_count = int(np.sum(warm_mask))
    cool_count = int(np.sum(cool_mask))
    neutral_count = int(np.sum(neutral_mask))

    warm_pct = (warm_count / total) * 100.0 if total > 0 else 0.0
    cool_pct = (cool_count / total) * 100.0 if total > 0 else 0.0
    neutral_pct = (neutral_count / total) * 100.0 if total > 0 else 0.0

    chromatic_total = warm_count + cool_count
    chromatic_warm_pct = (warm_count / chromatic_total * 100.0) if chromatic_total > 0 else 0.0

    ratio = (warm_count / cool_count) if cool_count > 0 else float("inf")

    return {
        "warm_pct": round(warm_pct, 2),
        "cool_pct": round(cool_pct, 2),
        "neutral_pct": round(neutral_pct, 2),
        "warm_count": warm_count,
        "cool_count": cool_count,
        "neutral_count": neutral_count,
        "total_pixels": total,
        "chromatic_warm_pct": round(chromatic_warm_pct, 2),
        "warm_cool_ratio": round(ratio, 2) if ratio != float("inf") else "inf",
    }


# ---------------------------------------------------------------------------
# Core metric: hue-split separation (reused from warmcool_scene_calibrate)
# ---------------------------------------------------------------------------

def measure_hue_split(img: Image.Image) -> Dict:
    """
    Measure warm/cool hue separation between top and bottom halves.

    Returns dict with: zone_a_hue, zone_b_hue, separation, achromatic.
    """
    rgb = img.convert("RGB")
    w, h = rgb.size
    arr = np.array(rgb, dtype=np.float32) / 255.0

    def _median_hue(region: np.ndarray) -> float:
        """Median PIL hue of chromatic pixels. Returns -1 if achromatic."""
        hue_pil, warm_mask, cool_mask, chromatic = _compute_hue_and_masks(region)
        if not np.any(chromatic):
            return -1.0
        return float(np.median(hue_pil[chromatic]))

    mid = h // 2
    hue_a = _median_hue(arr[:mid, :, :])
    hue_b = _median_hue(arr[mid:, :, :])

    if hue_a < 0 or hue_b < 0:
        return {
            "zone_a_hue": hue_a,
            "zone_b_hue": hue_b,
            "separation": 0.0,
            "achromatic": True,
        }

    delta = abs(hue_a - hue_b)
    if delta > 127.5:
        delta = 255.0 - delta

    return {
        "zone_a_hue": round(hue_a, 2),
        "zone_b_hue": round(hue_b, 2),
        "separation": round(delta, 2),
        "achromatic": False,
    }


# ---------------------------------------------------------------------------
# Composite score
# ---------------------------------------------------------------------------

def compute_composite_warmth(warm_pct: float, hue_split: float,
                             w_pixel: float = W_PIXEL,
                             w_split: float = W_SPLIT) -> float:
    """
    Compute composite warmth score from warm-pixel-percentage and hue-split.

    Args:
        warm_pct: warm pixel percentage (0-100)
        hue_split: hue separation in PIL units (0-127.5)
        w_pixel: weight for warm-pixel-percentage (default 0.7)
        w_split: weight for hue-split (default 0.3)

    Returns:
        Composite score 0.0 to 1.0.
    """
    norm_warm = warm_pct / 100.0
    norm_split = min(hue_split / MAX_HUE_SPLIT, 1.0)
    return round(w_pixel * norm_warm + w_split * norm_split, 4)


def evaluate_composite(composite: float, world_type: str) -> Dict:
    """
    Evaluate composite score against threshold for the given world type.

    Returns dict with: world_type, composite, threshold, passes, verdict, explanation.
    """
    threshold = COMPOSITE_THRESHOLDS.get(world_type)
    if threshold is None:
        return {
            "world_type": world_type,
            "composite": composite,
            "threshold": None,
            "passes": True,
            "verdict": "NO_THRESHOLD",
            "explanation": "No composite threshold defined for world type '{}'".format(world_type),
        }

    direction = threshold["direction"]
    if direction == "above":
        floor = threshold["min"]
        passes = composite >= floor
        verdict = "PASS" if passes else "FAIL"
        if passes:
            explanation = "composite {:.4f} >= {:.2f} minimum".format(composite, floor)
        else:
            explanation = "composite {:.4f} < {:.2f} minimum".format(composite, floor)
    else:
        ceiling = threshold["max"]
        passes = composite <= ceiling
        verdict = "PASS" if passes else "FAIL"
        if passes:
            explanation = "composite {:.4f} <= {:.2f} maximum".format(composite, ceiling)
        else:
            explanation = "composite {:.4f} > {:.2f} maximum".format(composite, ceiling)

    return {
        "world_type": world_type,
        "composite": composite,
        "threshold": threshold,
        "passes": passes,
        "verdict": verdict,
        "explanation": explanation,
    }


# ---------------------------------------------------------------------------
# World-type inference
# ---------------------------------------------------------------------------

def infer_world_type(filename: str) -> str:
    """Infer world type from filename. Default: REAL_INTERIOR."""
    fname_lower = filename.lower().replace("-", "_")
    for world_type, keywords in _WORLD_TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw in fname_lower:
                return world_type
    return "REAL_INTERIOR"


# ---------------------------------------------------------------------------
# Single-image analysis
# ---------------------------------------------------------------------------

def analyze_image(img_path: str, world_type: Optional[str] = None) -> Optional[Dict]:
    """Full composite warmth analysis for a single image."""
    path = Path(img_path)
    ext = path.suffix.lower()

    if ext in UNSUPPORTED_EXTS:
        return {
            "file": str(path),
            "filename": path.name,
            "status": "SKIPPED",
            "reason": "Unsupported format: {} (pillow-avif not installed)".format(ext),
        }

    if ext not in SUPPORTED_EXTS:
        return {
            "file": str(path),
            "filename": path.name,
            "status": "SKIPPED",
            "reason": "Unsupported format: {}".format(ext),
        }

    try:
        img = Image.open(str(path))
        img.load()
    except Exception as e:
        return {
            "file": str(path),
            "filename": path.name,
            "status": "ERROR",
            "reason": str(e),
        }

    pixels = measure_warm_pixel_percentage(img)
    split = measure_hue_split(img)
    composite = compute_composite_warmth(pixels["warm_pct"], split["separation"])

    wt = world_type if world_type else infer_world_type(path.name)
    threshold_eval = evaluate_composite(composite, wt)

    return {
        "file": str(path),
        "filename": path.name,
        "size": "{}x{}".format(img.size[0], img.size[1]),
        "status": "OK",
        "warm_pct": pixels["warm_pct"],
        "cool_pct": pixels["cool_pct"],
        "hue_split": split["separation"],
        "composite": composite,
        "threshold_eval": threshold_eval,
        "detail": {
            "pixels": pixels,
            "split": split,
        },
    }


# ---------------------------------------------------------------------------
# Batch processing
# ---------------------------------------------------------------------------

def batch_analyze(directory: str, world_type: Optional[str] = None) -> Dict:
    """Analyze all supported images in a directory."""
    dirpath = Path(directory)
    if not dirpath.is_dir():
        return {"directory": str(dirpath), "error": "Not a directory: {}".format(dirpath)}

    results = []
    for entry in sorted(dirpath.iterdir()):
        if not entry.is_file():
            continue
        result = analyze_image(str(entry), world_type=world_type)
        if result is not None:
            results.append(result)

    ok_results = [r for r in results if r.get("status") == "OK"]
    composites = [r["composite"] for r in ok_results]
    pass_count = sum(1 for r in ok_results if r["threshold_eval"]["passes"])
    fail_count = sum(1 for r in ok_results if not r["threshold_eval"]["passes"])
    skipped_count = sum(1 for r in results if r.get("status") in ("SKIPPED", "ERROR"))

    summary = {
        "total_files": len(results),
        "analyzed": len(ok_results),
        "skipped": skipped_count,
        "pass_count": pass_count,
        "fail_count": fail_count,
    }

    if composites:
        summary["min_composite"] = round(min(composites), 4)
        summary["max_composite"] = round(max(composites), 4)
        summary["mean_composite"] = round(sum(composites) / len(composites), 4)
        summary["median_composite"] = round(float(np.median(composites)), 4)
    else:
        summary["min_composite"] = None
        summary["max_composite"] = None
        summary["mean_composite"] = None
        summary["median_composite"] = None

    return {
        "directory": str(dirpath),
        "results": results,
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(batch_results: List[Dict], report_path: Optional[str] = None) -> str:
    """Generate a Markdown report from batch results."""
    lines = []
    lines.append("# Composite Warmth Score Report")
    lines.append("")
    lines.append("**Generated:** {}".format(datetime.now().strftime("%Y-%m-%d %H:%M")))
    lines.append("**Tool:** LTG_TOOL_composite_warmth_score.py v1.0.0")
    lines.append("**Author:** Sam Kowalski (Color & Style Artist)")
    lines.append("**Cycle:** 48")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## Methodology")
    lines.append("")
    lines.append("Composite warmth score combines two metrics:")
    lines.append("")
    lines.append("1. **Warm-pixel-percentage** (weight {:.0%}): fraction of chromatic pixels".format(W_PIXEL))
    lines.append("   with PIL HSV hue in the warm range (0-42 or 213-255).")
    lines.append("2. **Hue-split separation** (weight {:.0%}): circular hue distance between".format(W_SPLIT))
    lines.append("   median hue of top-half and bottom-half of the image.")
    lines.append("")
    lines.append("Formula: `composite = {:.1f} * (warm_pct / 100) + {:.1f} * min(hue_split / 127.5, 1.0)`".format(W_PIXEL, W_SPLIT))
    lines.append("")
    lines.append("| World Type | Threshold | Direction |")
    lines.append("|---|---|---|")
    for wt, spec in COMPOSITE_THRESHOLDS.items():
        if spec["direction"] == "above":
            lines.append("| {} | >= {:.2f} | Above |".format(wt, spec["min"]))
        else:
            lines.append("| {} | <= {:.2f} | Below |".format(wt, spec["max"]))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Global aggregation
    all_composites = []
    total_pass = 0
    total_fail = 0
    total_analyzed = 0

    for batch in batch_results:
        if "error" in batch:
            continue
        s = batch.get("summary", {})
        total_analyzed += s.get("analyzed", 0)
        total_pass += s.get("pass_count", 0)
        total_fail += s.get("fail_count", 0)
        for r in batch.get("results", []):
            if r.get("status") == "OK":
                all_composites.append(r["composite"])

    lines.append("## Summary")
    lines.append("")
    lines.append("- **Images analyzed:** {}".format(total_analyzed))
    lines.append("- **PASS:** {}".format(total_pass))
    lines.append("- **FAIL:** {}".format(total_fail))
    if all_composites:
        lines.append("- **Composite range:** {:.4f} -- {:.4f}".format(min(all_composites), max(all_composites)))
        lines.append("- **Composite median:** {:.4f}".format(float(np.median(all_composites))))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Per-directory results
    for batch in batch_results:
        if "error" in batch:
            lines.append("## {} (ERROR)".format(batch.get("directory", "unknown")))
            lines.append("")
            lines.append(batch["error"])
            lines.append("")
            continue

        lines.append("## {}".format(batch.get("directory", "unknown")))
        lines.append("")
        lines.append("| File | Size | Warm% | Cool% | Hue-Split | Composite | World | Verdict |")
        lines.append("|---|---|---|---|---|---|---|---|")

        for r in batch.get("results", []):
            if r.get("status") == "SKIPPED":
                lines.append("| {} | -- | -- | -- | -- | -- | -- | SKIPPED ({}) |".format(
                    r["filename"], r.get("reason", "")))
                continue
            if r.get("status") == "ERROR":
                lines.append("| {} | -- | -- | -- | -- | -- | -- | ERROR ({}) |".format(
                    r["filename"], r.get("reason", "")))
                continue

            te = r["threshold_eval"]
            lines.append("| {} | {} | {:.1f}% | {:.1f}% | {:.1f} | {:.4f} | {} | {} |".format(
                r["filename"],
                r["size"],
                r["warm_pct"],
                r["cool_pct"],
                r["hue_split"],
                r["composite"],
                te["world_type"],
                te["verdict"],
            ))

        lines.append("")

    report_text = "\n".join(lines) + "\n"

    if report_path:
        rpath = Path(report_path)
        rpath.parent.mkdir(parents=True, exist_ok=True)
        with open(str(rpath), "w") as f:
            f.write(report_text)
        print("Report written to: {}".format(report_path))

    return report_text


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Composite warmth score: warm-pixel-pct + hue-split")
    parser.add_argument("image", nargs="?", help="Path to a single image")
    parser.add_argument("--world", type=str, default=None,
                        help="World type override (REAL_INTERIOR, REAL_STORM, GLITCH, OTHER_SIDE)")
    parser.add_argument("--batch", type=str, action="append", default=[],
                        help="Directory to batch-analyze (repeatable)")
    parser.add_argument("--report", type=str, default=None,
                        help="Path to write Markdown report")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON instead of human-readable text")

    args = parser.parse_args()

    if args.image and not args.batch:
        # Single image mode
        result = analyze_image(args.image, world_type=args.world)
        if result is None:
            print("ERROR: Could not analyze image")
            sys.exit(1)

        if args.json:
            # Convert inf to string for JSON serialization
            def _sanitize(obj: object) -> object:
                if isinstance(obj, float) and obj == float("inf"):
                    return "inf"
                if isinstance(obj, dict):
                    return {k: _sanitize(v) for k, v in obj.items()}
                if isinstance(obj, list):
                    return [_sanitize(v) for v in obj]
                return obj

            print(json.dumps(_sanitize(result), indent=2))
        else:
            if result["status"] == "SKIPPED":
                print("{}: SKIPPED -- {}".format(result["filename"], result.get("reason", "")))
            elif result["status"] == "ERROR":
                print("{}: ERROR -- {}".format(result["filename"], result.get("reason", "")))
            else:
                te = result["threshold_eval"]
                print("{} ({})".format(result["filename"], result["size"]))
                print("  Warm pixels: {:.1f}%  Cool pixels: {:.1f}%".format(
                    result["warm_pct"], result["cool_pct"]))
                print("  Hue-split:   {:.1f}".format(result["hue_split"]))
                print("  Composite:   {:.4f}".format(result["composite"]))
                print("  World type:  {}".format(te["world_type"]))
                print("  Verdict:     {}".format(te["verdict"]))
                print("  {}".format(te["explanation"]))

        sys.exit(0)

    batch_results = []
    for d in args.batch:
        print("Analyzing: {} ...".format(d))
        batch = batch_analyze(d, world_type=args.world)
        batch_results.append(batch)

        if "error" in batch:
            print("  ERROR: {}".format(batch["error"]))
            continue

        s = batch["summary"]
        print("  Analyzed: {} | PASS: {} | FAIL: {} | Skipped: {}".format(
            s["analyzed"], s["pass_count"], s["fail_count"], s["skipped"]))
        if s["median_composite"] is not None:
            print("  Composite range: {:.4f} -- {:.4f} (median {:.4f})".format(
                s["min_composite"], s["max_composite"], s["median_composite"]))

    if args.report and batch_results:
        generate_report(batch_results, report_path=args.report)

    if args.json and batch_results:
        def _sanitize(obj: object) -> object:
            if isinstance(obj, float) and obj == float("inf"):
                return "inf"
            if isinstance(obj, dict):
                return {k: _sanitize(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [_sanitize(v) for v in obj]
            return obj
        print(json.dumps(_sanitize(batch_results), indent=2))


if __name__ == "__main__":
    main()
