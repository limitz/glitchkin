# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_warm_pixel_metric.py
==============================
Warm-Pixel-Percentage Metric for "Luma & the Glitchkin."

Replaces the hue-split metric (top-half vs bottom-half median hue) as the
primary warm/cool classification measure for Real World interior scenes.

Why: The hue-split metric fails for single-temperature-dominant interiors
because both halves share the same warm hue, producing separation near zero.
6 of 7 real interior reference photos failed the REAL_INTERIOR=12.0 threshold
in C46 calibration. Warm-pixel-percentage correctly classifies all 7.

Metric: percentage of chromatic pixels (saturation >= 5%) whose PIL HSV hue
falls in the warm range (0-42 or 213-255 on the 0-255 scale).

Thresholds (calibrated against reference photos + generated assets):
  REAL_INTERIOR: warm_pct >= 35%   (min reference: 42.0%, min generated: 42.5%)
  REAL_STORM:    warm_pct >= 5%    (SF02 Glitch Storm: 11.1%)
  GLITCH:        warm_pct < 15%    (Glitch environments: 0.9-10.6%)
  OTHER_SIDE:    warm_pct < 5%     (Other Side: 0.9-1.6%)

The threshold gap between REAL_INTERIOR floor (35%) and Glitch ceiling (11.1%)
is 24 percentage points -- robust against noise.

Author: Sam Kowalski (Color & Style Artist)
Created: Cycle 47 -- 2026-03-30
Version: 1.0.0

Usage:
  # Single image
  python3 LTG_TOOL_warm_pixel_metric.py path/to/image.png

  # Single image with world type
  python3 LTG_TOOL_warm_pixel_metric.py path/to/image.png --world REAL_INTERIOR

  # Batch directory
  python3 LTG_TOOL_warm_pixel_metric.py --batch output/backgrounds/environments/

  # Validation pass across all Real World environments
  python3 LTG_TOOL_warm_pixel_metric.py --validate-rw

  # Full report
  python3 LTG_TOOL_warm_pixel_metric.py --batch "reference/kitchen predawn" --batch "reference/living room night" --batch output/backgrounds/environments/ --report output/production/warm_pixel_metric_report.md

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

# PIL HSV hue ranges (0-255 scale)
# Warm: reds, oranges, yellows -- hue 0-42 and 213-255 (wraps around red)
# Cool: cyans, blues -- hue 85-170
WARM_HUE_LOW = 42
WARM_HUE_HIGH = 213
COOL_HUE_LOW = 85
COOL_HUE_HIGH = 170

# Minimum saturation to count as chromatic (matches render_qa)
MIN_SATURATION = 0.05

# Warm-pixel-percentage thresholds per world type
# Calibrated C47 against:
#   - 7 real interior reference photos (kitchen predawn + living room night)
#   - 8 generated REAL_INTERIOR environments + style frames
#   - 4 Glitch/Other Side environments + style frames
#
# REAL_INTERIOR: floor = 35% (min reference 42.0%, min generated 42.5%)
# REAL_STORM:    floor = 5%  (SF02 glitch storm = 11.1% warm)
# GLITCH:        ceiling = 15% (max observed 10.6%)
# OTHER_SIDE:    ceiling = 5%  (max observed 1.6%)
WARM_PCT_THRESHOLDS = {
    "REAL_INTERIOR": {"min": 35.0, "max": None,  "direction": "above"},
    "REAL_STORM":    {"min": 5.0,  "max": None,  "direction": "above"},
    "GLITCH":        {"min": None, "max": 15.0,  "direction": "below"},
    "OTHER_SIDE":    {"min": None, "max": 5.0,   "direction": "below"},
}

# Supported image extensions
SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
UNSUPPORTED_EXTS = {".avif"}

# World-type inference patterns (reuses logic from world_type_infer)
_WORLD_TYPE_KEYWORDS = {
    "OTHER_SIDE": ["other_side", "otherside", "sf03", "style_frame_03"],
    "GLITCH": ["glitch_layer", "glitchlayer", "glitch_encounter",
               "covetous_glitch", "glitch_showcase"],
    "REAL_STORM": ["glitch_storm", "storm_sf", "sf02", "style_frame_02",
                   "storm_bg"],
    # REAL_INTERIOR is default for Real World assets
}

# Real World environment filenames (for --validate-rw)
_RW_ENV_PATTERNS = [
    "grandma_living_room", "grandma_kitchen", "tech_den", "luma_study",
    "house_interior", "classroom", "school_hallway", "millbrook",
]


# ---------------------------------------------------------------------------
# Core metric
# ---------------------------------------------------------------------------

def measure_warm_pixel_percentage(img: Image.Image) -> Dict:
    """
    Measure warm, cool, and neutral pixel percentages.

    Returns dict with:
        warm_pct: float -- percentage of all pixels that are warm-chromatic
        cool_pct: float -- percentage of all pixels that are cool-chromatic
        neutral_pct: float -- percentage of neutral/achromatic pixels
        warm_count: int
        cool_count: int
        neutral_count: int
        total_pixels: int
        chromatic_warm_pct: float -- warm / (warm + cool) * 100
        warm_cool_ratio: float or "inf"
    """
    rgb = img.convert("RGB")
    arr = np.array(rgb, dtype=np.float32) / 255.0

    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    cmax = np.maximum(np.maximum(r, g), b)
    cmin = np.minimum(np.minimum(r, g), b)
    delta = cmax - cmin
    cmax_safe = np.where(cmax > 0, cmax, 1.0)
    sat = np.where(cmax > 0, delta / cmax_safe, 0.0)

    chromatic = sat >= MIN_SATURATION

    # Hue for chromatic pixels (0-6 scale -> 0-255 PIL scale)
    hue = np.zeros_like(delta)
    d_safe = np.where(delta > 0, delta, 1.0)

    r_mask = chromatic & (cmax == r)
    g_mask = chromatic & (~r_mask) & (cmax == g)
    b_mask = chromatic & (~r_mask) & (~g_mask) & (cmax == b)

    hue[r_mask] = ((g[r_mask] - b[r_mask]) / d_safe[r_mask]) % 6.0
    hue[g_mask] = ((b[g_mask] - r[g_mask]) / d_safe[g_mask]) + 2.0
    hue[b_mask] = ((r[b_mask] - g[b_mask]) / d_safe[b_mask]) + 4.0

    hue_pil = (hue / 6.0) * 255.0

    # Warm: hue 0-42 or 213-255
    warm_mask = chromatic & ((hue_pil <= WARM_HUE_LOW) | (hue_pil >= WARM_HUE_HIGH))
    # Cool: hue 85-170
    cool_mask = chromatic & (hue_pil >= COOL_HUE_LOW) & (hue_pil <= COOL_HUE_HIGH)
    # Neutral: everything else
    neutral_mask = ~warm_mask & ~cool_mask

    total = int(r.size)
    warm_count = int(np.sum(warm_mask))
    cool_count = int(np.sum(cool_mask))
    neutral_count = int(np.sum(neutral_mask))

    warm_pct = (warm_count / total) * 100.0 if total > 0 else 0.0
    cool_pct = (cool_count / total) * 100.0 if total > 0 else 0.0
    neutral_pct = (neutral_count / total) * 100.0 if total > 0 else 0.0

    # Chromatic warm percentage (warm / chromatic)
    chromatic_total = warm_count + cool_count
    chromatic_warm_pct = (warm_count / chromatic_total * 100.0) if chromatic_total > 0 else 0.0

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
        "chromatic_warm_pct": round(chromatic_warm_pct, 2),
        "warm_cool_ratio": round(ratio, 2) if ratio != float("inf") else "inf",
    }


# ---------------------------------------------------------------------------
# World-type inference
# ---------------------------------------------------------------------------

def infer_world_type(filename: str) -> str:
    """
    Infer world type from filename. Returns one of:
    REAL_INTERIOR, REAL_STORM, GLITCH, OTHER_SIDE.
    Default: REAL_INTERIOR.
    """
    fname_lower = filename.lower().replace("-", "_")
    for world_type, keywords in _WORLD_TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw in fname_lower:
                return world_type
    return "REAL_INTERIOR"


# ---------------------------------------------------------------------------
# Threshold evaluation
# ---------------------------------------------------------------------------

def evaluate_threshold(warm_pct: float, world_type: str) -> Dict:
    """
    Evaluate warm_pct against the threshold for the given world type.

    Returns dict with:
        world_type: str
        warm_pct: float
        threshold: dict (the threshold spec)
        passes: bool
        verdict: str
        explanation: str
    """
    threshold = WARM_PCT_THRESHOLDS.get(world_type)
    if threshold is None:
        return {
            "world_type": world_type,
            "warm_pct": warm_pct,
            "threshold": None,
            "passes": True,
            "verdict": "NO_THRESHOLD",
            "explanation": f"No warm-pixel threshold defined for world type '{world_type}'",
        }

    direction = threshold["direction"]
    if direction == "above":
        floor = threshold["min"]
        passes = warm_pct >= floor
        verdict = "PASS" if passes else "FAIL"
        explanation = f"warm_pct {warm_pct:.1f}% {'>=':} {floor}% minimum" if passes else f"warm_pct {warm_pct:.1f}% < {floor}% minimum"
    else:  # below
        ceiling = threshold["max"]
        passes = warm_pct <= ceiling
        verdict = "PASS" if passes else "FAIL"
        explanation = f"warm_pct {warm_pct:.1f}% <= {ceiling}% maximum" if passes else f"warm_pct {warm_pct:.1f}% > {ceiling}% maximum"

    return {
        "world_type": world_type,
        "warm_pct": warm_pct,
        "threshold": threshold,
        "passes": passes,
        "verdict": verdict,
        "explanation": explanation,
    }


# ---------------------------------------------------------------------------
# Single-image analysis
# ---------------------------------------------------------------------------

def analyze_image(img_path: str, world_type: Optional[str] = None) -> Optional[Dict]:
    """Full warm-pixel analysis for a single image."""
    path = Path(img_path)
    ext = path.suffix.lower()

    if ext in UNSUPPORTED_EXTS:
        return {
            "file": str(path),
            "filename": path.name,
            "status": "SKIPPED",
            "reason": f"Unsupported format: {ext}",
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
        img.load()
    except Exception as e:
        return {
            "file": str(path),
            "filename": path.name,
            "status": "ERROR",
            "reason": str(e),
        }

    pixels = measure_warm_pixel_percentage(img)

    wt = world_type if world_type else infer_world_type(path.name)
    threshold_eval = evaluate_threshold(pixels["warm_pct"], wt)

    return {
        "file": str(path),
        "filename": path.name,
        "size": "{}x{}".format(img.size[0], img.size[1]),
        "status": "OK",
        "pixels": pixels,
        "threshold_eval": threshold_eval,
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
    warm_pcts = [r["pixels"]["warm_pct"] for r in ok_results]
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

    if warm_pcts:
        summary["min_warm_pct"] = round(min(warm_pcts), 2)
        summary["max_warm_pct"] = round(max(warm_pcts), 2)
        summary["mean_warm_pct"] = round(sum(warm_pcts) / len(warm_pcts), 2)
        summary["median_warm_pct"] = round(float(np.median(warm_pcts)), 2)
    else:
        summary["min_warm_pct"] = None
        summary["max_warm_pct"] = None
        summary["mean_warm_pct"] = None
        summary["median_warm_pct"] = None

    return {
        "directory": str(dirpath),
        "results": results,
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# Validation pass: Real World environments
# ---------------------------------------------------------------------------

def validate_real_world(base_dir: str = "output/backgrounds/environments") -> Dict:
    """
    Run warm-pixel-percentage validation on all Real World environment PNGs.
    Returns structured results.
    """
    basepath = Path(base_dir)
    if not basepath.is_dir():
        return {"error": "Directory not found: {}".format(basepath)}

    results = []
    for entry in sorted(basepath.iterdir()):
        if not entry.is_file() or entry.suffix.lower() != ".png":
            continue
        # Skip layout subdirectory files
        if "layout" in entry.name.lower():
            continue

        # Determine if this is a Real World environment
        fname_lower = entry.name.lower()
        wt = infer_world_type(entry.name)

        result = analyze_image(str(entry), world_type=wt)
        if result is not None:
            results.append(result)

    # Also check style frames
    sf_dir = Path("output/color/style_frames")
    if sf_dir.is_dir():
        for entry in sorted(sf_dir.iterdir()):
            if not entry.is_file() or entry.suffix.lower() != ".png":
                continue
            wt = infer_world_type(entry.name)
            result = analyze_image(str(entry), world_type=wt)
            if result is not None:
                results.append(result)

    ok_results = [r for r in results if r.get("status") == "OK"]
    pass_count = sum(1 for r in ok_results if r["threshold_eval"]["passes"])
    fail_count = sum(1 for r in ok_results if not r["threshold_eval"]["passes"])

    return {
        "mode": "validate_rw",
        "results": results,
        "summary": {
            "total": len(ok_results),
            "pass": pass_count,
            "fail": fail_count,
        },
    }


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(batch_results: List[Dict], report_path: Optional[str] = None,
                    include_methodology: bool = True) -> str:
    """Generate a Markdown report from batch/validation results."""
    lines = []
    lines.append("# Warm-Pixel-Percentage Metric Report")
    lines.append("")
    lines.append("**Generated:** {}".format(datetime.now().strftime("%Y-%m-%d %H:%M")))
    lines.append("**Tool:** LTG_TOOL_warm_pixel_metric.py v1.0.0")
    lines.append("**Author:** Sam Kowalski (Color & Style Artist)")
    lines.append("**Cycle:** 47")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Global aggregation
    all_warm_pcts = []
    total_pass = 0
    total_fail = 0
    total_analyzed = 0

    for batch in batch_results:
        if "error" in batch:
            continue
        if "summary" in batch:
            s = batch["summary"]
            if "analyzed" in s:
                total_analyzed += s["analyzed"]
                total_pass += s.get("pass_count", s.get("pass", 0))
                total_fail += s.get("fail_count", s.get("fail", 0))
            elif "total" in s:
                total_analyzed += s["total"]
                total_pass += s.get("pass", 0)
                total_fail += s.get("fail", 0)
        for r in batch.get("results", []):
            if r.get("status") == "OK":
                all_warm_pcts.append(r["pixels"]["warm_pct"])

    lines.append("## Executive Summary")
    lines.append("")
    if all_warm_pcts:
        lines.append("- **Images analyzed:** {}".format(total_analyzed))
        lines.append("- **PASS:** {}".format(total_pass))
        lines.append("- **FAIL:** {}".format(total_fail))
        lines.append("- **Mean warm%:** {:.1f}%".format(sum(all_warm_pcts) / len(all_warm_pcts)))
        lines.append("- **Median warm%:** {:.1f}%".format(float(np.median(all_warm_pcts))))
        lines.append("- **Range:** {:.1f}% - {:.1f}%".format(min(all_warm_pcts), max(all_warm_pcts)))
    else:
        lines.append("No images analyzed.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Per-batch sections
    for batch in batch_results:
        if batch.get("mode") == "validate_rw":
            lines.append("## Real World Validation Pass")
        else:
            dirpath = batch.get("directory", "unknown")
            dirname = Path(dirpath).name
            lines.append("## Directory: `{}/`".format(dirname))
        lines.append("")

        if "error" in batch:
            lines.append("**Error:** {}".format(batch["error"]))
            lines.append("")
            continue

        # Per-image table
        lines.append("| File | Size | World | Warm% | Cool% | W:C | Verdict |")
        lines.append("|------|------|-------|-------|-------|-----|---------|")
        for r in batch.get("results", []):
            fname = r["filename"]
            if r.get("status") in ("SKIPPED", "ERROR"):
                reason = r.get("reason", "unknown")
                lines.append("| {} | -- | -- | -- | -- | -- | {}: {} |".format(
                    fname, r["status"], reason))
                continue
            pix = r["pixels"]
            te = r["threshold_eval"]
            size = r.get("size", "?")
            lines.append("| {} | {} | {} | {:.1f}% | {:.1f}% | {} | {} |".format(
                fname, size, te["world_type"],
                pix["warm_pct"], pix["cool_pct"],
                pix["warm_cool_ratio"], te["verdict"]))

        lines.append("")

    if include_methodology:
        lines.append("---")
        lines.append("")
        lines.append("## Methodology")
        lines.append("")
        lines.append("### Why warm-pixel-percentage replaces hue-split")
        lines.append("")
        lines.append("The prior metric (hue-split) measured the circular distance between the")
        lines.append("median PIL HSV hue of the top half and bottom half of the image. This fails")
        lines.append("for single-temperature-dominant interiors: when both halves are warm, the")
        lines.append("separation is near zero even though the scene is unambiguously warm-lit.")
        lines.append("")
        lines.append("C46 calibration showed 6/7 real interior reference photos fell below the")
        lines.append("REAL_INTERIOR=12.0 hue-split threshold (median separation: 2.30).")
        lines.append("")
        lines.append("Warm-pixel-percentage directly measures what we care about: how much of the")
        lines.append("image is warm-toned. It correctly classifies all reference photos and all")
        lines.append("generated assets with a 24-point gap between Real World and Glitch.")
        lines.append("")
        lines.append("### Threshold Calibration Data")
        lines.append("")
        lines.append("| Category | Asset | Warm% | Expected |")
        lines.append("|----------|-------|-------|----------|")
        lines.append("| Ref: Kitchen predawn | image-11854.jpg | 60.9% | REAL_INTERIOR PASS |")
        lines.append("| Ref: Kitchen predawn | image-13179.jpg | 84.1% | REAL_INTERIOR PASS |")
        lines.append("| Ref: Kitchen predawn | low-kitchen-ceiling-lights | 96.1% | REAL_INTERIOR PASS |")
        lines.append("| Ref: Living room | city-view-night | 48.2% | REAL_INTERIOR PASS |")
        lines.append("| Ref: Living room | dark-vintage-living-room | 42.0% | REAL_INTERIOR PASS |")
        lines.append("| Ref: Living room | gettyimages | 51.5% | REAL_INTERIOR PASS |")
        lines.append("| Ref: Living room | istockphoto | 85.8% | REAL_INTERIOR PASS |")
        lines.append("| Gen: REAL_INTERIOR | Grandma living room | 67.2% | REAL_INTERIOR PASS |")
        lines.append("| Gen: REAL_INTERIOR | Grandma kitchen | 67.9% | REAL_INTERIOR PASS |")
        lines.append("| Gen: REAL_INTERIOR | Tech den | 53.1% | REAL_INTERIOR PASS |")
        lines.append("| Gen: REAL_INTERIOR | Luma study | 53.3% | REAL_INTERIOR PASS |")
        lines.append("| Gen: REAL_INTERIOR | House interior (frame01) | 68.1% | REAL_INTERIOR PASS |")
        lines.append("| Gen: REAL_INTERIOR | SF01 discovery | 58.0% | REAL_INTERIOR PASS |")
        lines.append("| Gen: REAL_INTERIOR | School hallway | 42.5% | REAL_INTERIOR PASS |")
        lines.append("| Gen: REAL_INTERIOR | Classroom | 55.3% | REAL_INTERIOR PASS |")
        lines.append("| Gen: REAL_STORM | SF02 Glitch Storm | 11.1% | REAL_STORM PASS |")
        lines.append("| Gen: GLITCH | Glitch Storm BG | 10.6% | GLITCH PASS |")
        lines.append("| Gen: OTHER_SIDE | SF03 Other Side | 1.6% | OTHER_SIDE PASS |")
        lines.append("| Gen: OTHER_SIDE | Other Side BG | 0.9% | OTHER_SIDE PASS |")
        lines.append("")
        lines.append("### Thresholds")
        lines.append("")
        lines.append("| World Type | Direction | Threshold | Gap to nearest misclassification |")
        lines.append("|-----------|-----------|-----------|----------------------------------|")
        lines.append("| REAL_INTERIOR | warm_pct >= | 35% | 7pt (min RW is 42.0%) |")
        lines.append("| REAL_STORM | warm_pct >= | 5% | 6pt (SF02 is 11.1%) |")
        lines.append("| GLITCH | warm_pct <= | 15% | 4pt (max Glitch is 10.6%) |")
        lines.append("| OTHER_SIDE | warm_pct <= | 5% | 3pt (max Other Side is 1.6%) |")
        lines.append("")
        lines.append("### Recommendation")
        lines.append("")
        lines.append("**Use warm-pixel-percentage as the primary warm/cool check for REAL_INTERIOR.**")
        lines.append("The hue-split metric can be retained as a secondary signal for mixed-temperature")
        lines.append("scenes (e.g., SF02 contested storm) but should not gate REAL_INTERIOR classification.")
        lines.append("")

    report = "\n".join(lines)

    if report_path:
        rp = Path(report_path)
        rp.parent.mkdir(parents=True, exist_ok=True)
        with open(str(rp), "w") as f:
            f.write(report)

    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Warm-Pixel-Percentage Metric -- measures warm pixel coverage for scene classification."
    )
    parser.add_argument(
        "image", nargs="?", default=None,
        help="Single image path to analyze"
    )
    parser.add_argument(
        "--world", default=None,
        choices=["REAL_INTERIOR", "REAL_STORM", "GLITCH", "OTHER_SIDE"],
        help="Override world type (default: infer from filename)"
    )
    parser.add_argument(
        "--batch", action="append", default=[],
        help="Directory to batch-process (can be repeated)"
    )
    parser.add_argument(
        "--validate-rw", action="store_true",
        help="Run validation pass across all Real World environments and style frames"
    )
    parser.add_argument(
        "--report", default=None,
        help="Path to write Markdown report"
    )

    args = parser.parse_args()

    if not args.image and not args.batch and not args.validate_rw:
        parser.print_help()
        sys.exit(1)

    # Single image mode
    if args.image and not args.batch and not args.validate_rw:
        result = analyze_image(args.image, world_type=args.world)
        if result is None or result.get("status") in ("SKIPPED", "ERROR"):
            reason = result.get("reason", "unknown") if result else "unknown"
            print("Cannot analyze: {} ({})".format(args.image, reason))
            sys.exit(1)

        pix = result["pixels"]
        te = result["threshold_eval"]
        print("File: {} ({})".format(result["filename"], result["size"]))
        print("World type: {}".format(te["world_type"]))
        print("Warm-pixel percentage: {:.1f}%".format(pix["warm_pct"]))
        print("  Cool: {:.1f}%  Neutral: {:.1f}%".format(pix["cool_pct"], pix["neutral_pct"]))
        print("  Warm:Cool ratio: {}".format(pix["warm_cool_ratio"]))
        print("  Chromatic warm: {:.1f}%".format(pix["chromatic_warm_pct"]))
        print("Threshold evaluation: {}".format(te["verdict"]))
        print("  {}".format(te["explanation"]))
        sys.exit(0)

    # Collect batch results
    batch_results = []

    for d in args.batch:
        print("\nProcessing: {}".format(d))
        result = batch_analyze(d, world_type=args.world)
        batch_results.append(result)

        if "error" in result:
            print("  ERROR: {}".format(result["error"]))
            continue

        s = result["summary"]
        print("  Analyzed: {}, Skipped: {}".format(s["analyzed"], s["skipped"]))
        if s.get("mean_warm_pct") is not None:
            print("  Warm%: mean={:.1f}%, median={:.1f}%, range=[{:.1f}%, {:.1f}%]".format(
                s["mean_warm_pct"], s["median_warm_pct"],
                s["min_warm_pct"], s["max_warm_pct"]))
            print("  PASS: {}, FAIL: {}".format(s["pass_count"], s["fail_count"]))

    if args.validate_rw:
        print("\nRunning Real World validation pass...")
        rw_result = validate_real_world()
        batch_results.append(rw_result)

        if "error" in rw_result:
            print("  ERROR: {}".format(rw_result["error"]))
        else:
            s = rw_result["summary"]
            print("  Total: {}, PASS: {}, FAIL: {}".format(s["total"], s["pass"], s["fail"]))
            for r in rw_result.get("results", []):
                if r.get("status") == "OK":
                    pix = r["pixels"]
                    te = r["threshold_eval"]
                    mark = "PASS" if te["passes"] else "FAIL"
                    print("  {} {} warm={:.1f}% [{}]".format(
                        mark, r["filename"], pix["warm_pct"], te["world_type"]))

    # Add single image to results if in batch/validate mode
    if args.image:
        single = analyze_image(args.image, world_type=args.world)
        if single and single.get("status") == "OK":
            batch_results.append({
                "directory": str(Path(args.image).parent),
                "results": [single],
                "summary": {
                    "total_files": 1,
                    "analyzed": 1,
                    "skipped": 0,
                    "pass_count": 1 if single["threshold_eval"]["passes"] else 0,
                    "fail_count": 0 if single["threshold_eval"]["passes"] else 1,
                    "min_warm_pct": single["pixels"]["warm_pct"],
                    "max_warm_pct": single["pixels"]["warm_pct"],
                    "mean_warm_pct": single["pixels"]["warm_pct"],
                    "median_warm_pct": single["pixels"]["warm_pct"],
                },
            })

    # Report
    if args.report:
        report_text = generate_report(batch_results, report_path=args.report)
        print("\nReport written to: {}".format(args.report))
    elif batch_results:
        report_text = generate_report(batch_results)
        print("\n" + report_text)


if __name__ == "__main__":
    main()
