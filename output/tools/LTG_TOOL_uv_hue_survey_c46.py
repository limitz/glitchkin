# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_uv_hue_survey_c46.py
==============================
One-shot C46 analysis: survey purple-family hue distribution across all Glitch Layer
assets and reference images. Output informs UV_PURPLE hue-family range calibration
for LTG_TOOL_uv_purple_linter.py.

Author: Rin Yamamoto (Procedural Art Engineer) — Cycle 46
Version: 1.0.0
"""

from __future__ import annotations

import os
import sys
import json
from pathlib import Path

import numpy as np
import cv2
from PIL import Image

__version__ = "1.0.0"
__author__ = "Rin Yamamoto"

PROJECT_ROOT = Path("/home/wipkat/team")


def analyze_purple_hues(img_path: str) -> dict | None:
    """Analyze the hue distribution of purple-family pixels in an image."""
    img = Image.open(img_path).convert("RGB")
    pixels = np.array(img, dtype=np.uint8).reshape(-1, 3)

    # Convert to LAB
    bgr = pixels[:, ::-1].astype(np.uint8).reshape(1, -1, 3)
    lab_img = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    lab_raw = lab_img.reshape(-1, 3).astype(np.float32)
    lab = np.empty_like(lab_raw)
    lab[:, 0] = lab_raw[:, 0] * (100.0 / 255.0)
    lab[:, 1] = lab_raw[:, 1] - 128.0
    lab[:, 2] = lab_raw[:, 2] - 128.0

    # Compute hue and chroma
    hue = np.degrees(np.arctan2(lab[:, 2], lab[:, 1])) % 360.0
    chroma = np.sqrt(lab[:, 1] ** 2 + lab[:, 2] ** 2)

    # Filter: non-void (max channel >= 30), chromatic (C* >= 8)
    max_ch = np.max(pixels, axis=1)
    non_void = max_ch >= 30
    chromatic = chroma >= 8.0
    valid = non_void & chromatic

    if np.sum(valid) == 0:
        return None

    valid_hues = hue[valid]

    # Purple-family: broad range 220-340 (anything that could be purple/violet/magenta)
    purple_broad = (valid_hues >= 220.0) & (valid_hues <= 340.0)
    purple_hues = valid_hues[purple_broad]

    if len(purple_hues) == 0:
        return None

    # Also count how many fall in current range 255-325 vs proposed ranges
    in_current = ((purple_hues >= 255.0) & (purple_hues <= 325.0)).sum()
    in_250_330 = ((purple_hues >= 250.0) & (purple_hues <= 330.0)).sum()
    in_245_335 = ((purple_hues >= 245.0) & (purple_hues <= 335.0)).sum()
    in_260_300 = ((purple_hues >= 260.0) & (purple_hues <= 300.0)).sum()

    return {
        "total_chromatic": int(np.sum(valid)),
        "purple_count": int(len(purple_hues)),
        "purple_frac": float(len(purple_hues) / np.sum(valid)),
        "hue_min": float(np.min(purple_hues)),
        "hue_max": float(np.max(purple_hues)),
        "hue_mean": float(np.mean(purple_hues)),
        "hue_median": float(np.median(purple_hues)),
        "hue_std": float(np.std(purple_hues)),
        "hue_p1": float(np.percentile(purple_hues, 1)),
        "hue_p5": float(np.percentile(purple_hues, 5)),
        "hue_p10": float(np.percentile(purple_hues, 10)),
        "hue_p25": float(np.percentile(purple_hues, 25)),
        "hue_p75": float(np.percentile(purple_hues, 75)),
        "hue_p90": float(np.percentile(purple_hues, 90)),
        "hue_p95": float(np.percentile(purple_hues, 95)),
        "hue_p99": float(np.percentile(purple_hues, 99)),
        "in_260_300": int(in_260_300),
        "in_255_325": int(in_current),
        "in_250_330": int(in_250_330),
        "in_245_335": int(in_245_335),
        "coverage_260_300": float(in_260_300 / len(purple_hues)),
        "coverage_255_325": float(in_current / len(purple_hues)),
        "coverage_250_330": float(in_250_330 / len(purple_hues)),
        "coverage_245_335": float(in_245_335 / len(purple_hues)),
    }


def run_survey():
    """Run survey on all glitch-layer assets and reference images."""

    # Glitch layer assets
    glitch_assets = [
        "output/backgrounds/environments/LTG_ENV_glitch_storm_bg.png",
        "output/backgrounds/environments/LTG_ENV_glitchlayer_encounter.png",
        "output/backgrounds/environments/LTG_ENV_glitchlayer_frame.png",
        "output/backgrounds/environments/LTG_ENV_other_side_bg.png",
        "output/backgrounds/environments/bg_glitch_layer_encounter.png",
        "output/backgrounds/environments/glitch_layer_frame.png",
        "output/color/style_frames/LTG_COLOR_sf_covetous_glitch.png",
        "output/color/style_frames/LTG_COLOR_styleframe_glitch_storm.png",
        "output/color/style_frames/LTG_SF_covetous_glitch_v001.png",
        "output/color/color_keys/LTG_COLOR_colorkey_glitch_covetous.png",
        "output/color/color_keys/thumbnails/LTG_COLOR_colorkey_glitchlayer_entry.png",
        "output/color/color_keys/thumbnails/LTG_COLOR_colorkey_glitchstorm.png",
        "output/color/color_keys/thumbnails/LTG_COLOR_colorkey_nighttime_glitch.png",
        "output/storyboards/panels/LTG_SB_ep05_covetous.png",
    ]

    # Reference images
    ref_glitches = []
    ref_dir = PROJECT_ROOT / "reference" / "glitches"
    if ref_dir.exists():
        for f in sorted(ref_dir.iterdir()):
            if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
                ref_glitches.append(str(f))

    ref_pixelart = []
    ref_dir2 = PROJECT_ROOT / "reference" / "pixelart"
    if ref_dir2.exists():
        for f in sorted(ref_dir2.iterdir()):
            if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
                ref_pixelart.append(str(f))

    header = f"{'Asset':<60} {'Count':>8} {'Frac':>6} {'P5':>6} {'P10':>6} {'Med':>6} {'P90':>6} {'P95':>6} {'Min':>6} {'Max':>6} {'%260-300':>8} {'%255-325':>8} {'%250-330':>8}"
    sep = "-" * len(header)

    # Run analysis
    print("=" * 80)
    print("UV_PURPLE Hue-Family Range Survey — C46")
    print("=" * 80)
    print()

    all_data = {}

    for label, paths, is_ref in [
        ("GLITCH LAYER ASSETS", glitch_assets, False),
        ("REFERENCE: glitches/", ref_glitches, True),
        ("REFERENCE: pixelart/", ref_pixelart, True),
    ]:
        print(f"\n=== {label} ===")
        print(header)
        print(sep)

        for asset_path in paths:
            if not is_ref:
                full_path = str(PROJECT_ROOT / asset_path)
            else:
                full_path = asset_path
            basename = os.path.basename(full_path)

            if not os.path.exists(full_path):
                print(f"{basename:<60} FILE NOT FOUND")
                continue

            try:
                r = analyze_purple_hues(full_path)
            except Exception as e:
                print(f"{basename:<60} ERROR: {e}")
                continue

            if r is None:
                print(f"{basename:<60} NO PURPLE PIXELS")
                continue

            all_data[basename] = r
            print(
                f"{basename:<60} "
                f"{r['purple_count']:>8} {r['purple_frac']:>6.1%} "
                f"{r['hue_p5']:>6.1f} {r['hue_p10']:>6.1f} "
                f"{r['hue_median']:>6.1f} {r['hue_p90']:>6.1f} "
                f"{r['hue_p95']:>6.1f} {r['hue_min']:>6.1f} "
                f"{r['hue_max']:>6.1f} "
                f"{r['coverage_260_300']:>8.1%} "
                f"{r['coverage_255_325']:>8.1%} "
                f"{r['coverage_250_330']:>8.1%}"
            )

    # Aggregate analysis
    print("\n" + "=" * 80)
    print("AGGREGATE ANALYSIS")
    print("=" * 80)

    if all_data:
        # Collect all purple hues from LTG assets only
        ltg_results = {k: v for k, v in all_data.items() if k.startswith("LTG_")}
        if ltg_results:
            total_purple = sum(r["purple_count"] for r in ltg_results.values())
            avg_coverage_260_300 = np.mean([r["coverage_260_300"] for r in ltg_results.values()])
            avg_coverage_255_325 = np.mean([r["coverage_255_325"] for r in ltg_results.values()])
            avg_coverage_250_330 = np.mean([r["coverage_250_330"] for r in ltg_results.values()])
            avg_coverage_245_335 = np.mean([r["coverage_245_335"] for r in ltg_results.values()])

            global_p5 = np.mean([r["hue_p5"] for r in ltg_results.values()])
            global_p95 = np.mean([r["hue_p95"] for r in ltg_results.values()])
            global_min = min(r["hue_min"] for r in ltg_results.values())
            global_max = max(r["hue_max"] for r in ltg_results.values())

            print(f"\nLTG asset count with purple pixels: {len(ltg_results)}")
            print(f"Total purple-family pixels across LTG assets: {total_purple:,}")
            print(f"Global hue range: {global_min:.1f} - {global_max:.1f}")
            print(f"Average P5 hue: {global_p5:.1f}")
            print(f"Average P95 hue: {global_p95:.1f}")
            print()
            print("Range coverage (average across LTG assets):")
            print(f"  260-300 (old narrow):  {avg_coverage_260_300:.1%}")
            print(f"  255-325 (current):     {avg_coverage_255_325:.1%}")
            print(f"  250-330 (candidate A): {avg_coverage_250_330:.1%}")
            print(f"  245-335 (candidate B): {avg_coverage_245_335:.1%}")
            print()
            print("RECOMMENDATION:")
            if avg_coverage_255_325 >= 0.95:
                print("  Current range 255-325 captures >= 95% of purple pixels. No change needed.")
            elif avg_coverage_250_330 >= 0.95:
                print("  Widen to 250-330: captures >= 95% of purple pixels.")
            elif avg_coverage_245_335 >= 0.95:
                print("  Widen to 245-335: captures >= 95% of purple pixels.")
            else:
                print("  Further analysis needed - coverage below 95% at all tested ranges.")

    # Save JSON data
    out_path = str(PROJECT_ROOT / "output" / "production" / "uv_purple_hue_survey_c46.json")
    with open(out_path, "w") as f:
        json.dump(all_data, f, indent=2)
    print(f"\nDetailed data saved to: {out_path}")


if __name__ == "__main__":
    run_survey()
