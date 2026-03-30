#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_visual_blank_test.py
Visual Blank Test Checklist — Storyboard Panel QA Tool
Diego Vargas, Storyboard Artist — Cycle 48

PURPOSE:
Every storyboard panel should communicate its beat WITHOUT text. If the beat lives only
in the captions/annotations, the panel has failed as a board. This tool:

1. Takes any storyboard panel PNG
2. Renders a text-stripped version (caption bar removed, annotation regions masked)
3. Runs a checklist of visual readability metrics
4. Outputs PASS / WARN / FAIL per check, with an overall verdict

CHECKS:
  C1 — SILHOUETTE CONTRAST: Are distinct character shapes visible against the background?
        Measures foreground-background luminance delta. FAIL if delta < 15.
  C2 — MULTI-ZONE COMPOSITION: Does the frame have distinct spatial zones (not a flat fill)?
        Splits into quadrants and checks variance. FAIL if all quadrants are within 8 luma.
  C3 — FOCAL POINT: Is there a clear region of highest visual energy (contrast, saturation)?
        Finds the peak-energy 10% area. WARN if energy is too evenly distributed.
  C4 — CHARACTER PRESENCE: Are there character-scale regions in the expected zones?
        Uses edge density in the central band. FAIL if no high-edge-density cluster found.
  C5 — DEPTH CUES: Is there warm/cool temperature separation (depth temperature rule)?
        Measures warm vs cool pixel ratio in upper vs lower halves. WARN if flat.
  C6 — ARC COLOR BORDER: Is the arc-color border present and intact?
        Checks outer 4px band for saturated non-neutral color. WARN if missing.

USAGE:
  python LTG_TOOL_visual_blank_test.py --panel P22
  python LTG_TOOL_visual_blank_test.py --file output/storyboards/panels/LTG_SB_cold_open_P22.png
  python LTG_TOOL_visual_blank_test.py --all         # test all panels in panels/
  python LTG_TOOL_visual_blank_test.py --panel P22 --save   # save text-stripped PNG

OUTPUT:
  Prints checklist results per panel. If --save, writes <panel>_blank_test.png to
  output/production/blank_tests/
"""

try:
    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402
except ImportError:
    import pathlib
    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path

import argparse
import os
import sys
import glob as glob_mod

try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False

from PIL import Image, ImageDraw, ImageFilter

PANELS_DIR = str(output_dir('storyboards', 'panels'))
BLANK_TEST_DIR = str(output_dir('production', 'blank_tests'))
CAPTION_H = 72  # standard caption bar height


def strip_text(img):
    """Remove caption bar and mask annotation-colored text regions in the draw area.

    Returns the draw area only (caption bar cropped), with annotation-colored pixels
    replaced by local neighborhood average.
    """
    w, h = img.size
    draw_h = h - CAPTION_H
    # Crop to draw area only (remove caption bar)
    draw_area = img.crop([0, 0, w, draw_h]).copy()

    if not _HAS_NUMPY:
        return draw_area

    arr = np.array(draw_area)

    # Annotation colors to mask (approximate — match within tolerance)
    ann_colors = [
        (220, 200, 80),   # ANN_COLOR (yellow annotations)
        (80, 90, 100),    # ANN_DIM (dim gray annotations)
        (0, 180, 210),    # ANN_CYAN
        (255, 220, 180),  # crack/highlight annotations
        (232, 224, 204),  # TEXT_SHOT color that might bleed into draw area
        (155, 148, 122),  # TEXT_DESC
    ]

    mask = np.zeros(arr.shape[:2], dtype=bool)
    tolerance = 35

    for ac in ann_colors:
        diff = np.sqrt(np.sum((arr.astype(float) - np.array(ac, dtype=float)) ** 2, axis=2))
        mask |= (diff < tolerance)

    # Replace masked pixels with local mean (5px box blur)
    if mask.any():
        blurred = np.array(draw_area.filter(ImageFilter.BoxBlur(5)))
        arr[mask] = blurred[mask]

    result = Image.fromarray(arr)
    return result


def to_luma(img):
    """Convert PIL image to numpy luminance array (0-255)."""
    if not _HAS_NUMPY:
        return None
    arr = np.array(img.convert('RGB')).astype(float)
    luma = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    return luma


def check_silhouette_contrast(img):
    """C1: Foreground-background luminance delta.

    Uses two methods: (A) center-vs-edges mean delta, (B) overall luma standard
    deviation in the central region. Either passing is sufficient — method B catches
    ECU/prop panels where the entire frame is one zone but internal contrast is strong.
    """
    luma = to_luma(img)
    if luma is None:
        return "SKIP", "numpy not available"
    h, w = luma.shape
    # Method A: center vs edges
    center_band = luma[int(h * 0.2):int(h * 0.8), int(w * 0.2):int(w * 0.8)]
    outer_top = luma[:int(h * 0.15), :]
    outer_bot = luma[int(h * 0.85):, :]
    fg_mean = np.mean(center_band)
    bg_mean = np.mean(np.concatenate([outer_top.flatten(), outer_bot.flatten()]))
    delta_a = abs(fg_mean - bg_mean)

    # Method B: internal contrast (std dev of center region)
    center_std = np.std(center_band)

    if delta_a >= 15 or center_std >= 20:
        detail = f"FG/BG delta={delta_a:.1f}, center std={center_std:.1f}"
        if delta_a < 15:
            detail += " (ECU/prop panel — internal contrast carries)"
        return "PASS", detail
    elif delta_a >= 10 or center_std >= 14:
        return "WARN", f"FG/BG delta={delta_a:.1f}, center std={center_std:.1f} (marginal)"
    return "FAIL", f"FG/BG delta={delta_a:.1f}, center std={center_std:.1f} (need delta>15 or std>20)"


def check_multi_zone(img):
    """C2: Quadrant variance — are there distinct spatial zones?"""
    luma = to_luma(img)
    if luma is None:
        return "SKIP", "numpy not available"
    h, w = luma.shape
    quads = [
        luma[:h // 2, :w // 2],
        luma[:h // 2, w // 2:],
        luma[h // 2:, :w // 2],
        luma[h // 2:, w // 2:],
    ]
    means = [np.mean(q) for q in quads]
    spread = max(means) - min(means)
    if spread < 8:
        return "FAIL", f"Quadrant spread = {spread:.1f} (flat — need >8)"
    elif spread < 16:
        return "WARN", f"Quadrant spread = {spread:.1f} (low variance — >16 ideal)"
    return "PASS", f"Quadrant spread = {spread:.1f}"


def check_focal_point(img):
    """C3: Is there a clear region of highest visual energy?"""
    if not _HAS_NUMPY:
        return "SKIP", "numpy not available"
    arr = np.array(img.convert('RGB')).astype(float)
    h, w = arr.shape[:2]
    # Energy = local contrast (Laplacian approximation via difference of means)
    luma = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    # Compute local energy via block std dev (8x8 blocks)
    block = 8
    energy_map = np.zeros((h // block, w // block))
    for by in range(energy_map.shape[0]):
        for bx in range(energy_map.shape[1]):
            patch = luma[by * block:(by + 1) * block, bx * block:(bx + 1) * block]
            energy_map[by, bx] = np.std(patch)

    total_energy = np.sum(energy_map)
    if total_energy < 1:
        return "FAIL", "No visual energy detected"

    # Top 10% energy blocks
    threshold = np.percentile(energy_map, 90)
    hot_blocks = energy_map >= threshold
    hot_count = np.sum(hot_blocks)
    total_blocks = energy_map.size

    # If hot blocks are >40% of total, energy is too spread
    hot_ratio = hot_count / total_blocks
    if hot_ratio > 0.40:
        return "WARN", f"Energy spread across {hot_ratio:.0%} of frame (diffuse — may lack focal point)"
    return "PASS", f"Focal energy concentrated in {hot_ratio:.0%} of frame"


def check_character_presence(img):
    """C4: Edge density — are characters/forms present?

    Checks both the central band AND the upper-center region (for MCU panels
    where the face is in the upper portion and body fills below). The higher
    of the two scores is used.
    """
    if not _HAS_NUMPY:
        return "SKIP", "numpy not available"
    luma = to_luma(img)
    h, w = luma.shape

    def edge_density_of(region):
        dy = np.abs(np.diff(region, axis=0))
        dx = np.abs(np.diff(region, axis=1))
        return (np.mean(dy) + np.mean(dx)) / 2

    # Central horizontal band (standard)
    band1 = luma[int(h * 0.15):int(h * 0.85), int(w * 0.1):int(w * 0.9)]
    ed1 = edge_density_of(band1)

    # Upper-center region (for MCU face panels)
    band2 = luma[int(h * 0.05):int(h * 0.55), int(w * 0.15):int(w * 0.85)]
    ed2 = edge_density_of(band2)

    edge_density = max(ed1, ed2)
    source = "central" if ed1 >= ed2 else "upper"

    if edge_density < 1.5:
        return "FAIL", f"Edge density = {edge_density:.1f} ({source}) (no character-scale forms — need >1.5)"
    elif edge_density < 4:
        return "WARN", f"Edge density = {edge_density:.1f} ({source}) (low — MCU/costume panels may be OK if silhouette reads)"
    elif edge_density < 8:
        return "PASS", f"Edge density = {edge_density:.1f} ({source}) (adequate)"
    return "PASS", f"Edge density = {edge_density:.1f} ({source})"


def check_depth_cues(img):
    """C5: Warm/cool temperature separation between upper and lower halves."""
    if not _HAS_NUMPY:
        return "SKIP", "numpy not available"
    arr = np.array(img.convert('RGB')).astype(float)
    h, w = arr.shape[:2]
    # Warmth metric: R channel weight minus B channel weight
    warmth = arr[:, :, 0] - arr[:, :, 2]  # positive = warm, negative = cool
    upper = np.mean(warmth[:h // 2, :])
    lower = np.mean(warmth[h // 2:, :])
    delta = abs(upper - lower)
    if delta < 5:
        return "WARN", f"Warm/cool split = {delta:.1f} (flat depth — >5 needed for depth cue)"
    return "PASS", f"Warm/cool split = {delta:.1f} (upper={upper:.1f}, lower={lower:.1f})"


def check_arc_border(img_full):
    """C6: Is the arc-color border present? Checks the original full image (with border)."""
    if not _HAS_NUMPY:
        return "SKIP", "numpy not available"
    arr = np.array(img_full.convert('RGB')).astype(float)
    h, w = arr.shape[:2]
    # Sample outer 4px band
    top = arr[:4, :, :]
    bot = arr[h - 4:, :, :]
    left = arr[:, :4, :]
    right = arr[:, w - 4:, :]
    border = np.concatenate([top.reshape(-1, 3), bot.reshape(-1, 3),
                             left.reshape(-1, 3), right.reshape(-1, 3)], axis=0)
    # Check for saturated non-neutral color
    saturation = np.max(border, axis=1) - np.min(border, axis=1)
    high_sat = np.mean(saturation > 60)
    if high_sat < 0.3:
        return "WARN", f"Border saturation = {high_sat:.0%} pixels saturated (arc border may be missing)"
    return "PASS", f"Border saturation = {high_sat:.0%} pixels saturated — arc border present"


def run_blank_test(panel_path, save=False):
    """Run the full blank test checklist on a single panel."""
    if not os.path.exists(panel_path):
        print(f"  ERROR: File not found: {panel_path}")
        return None

    img_full = Image.open(panel_path).convert('RGB')
    stripped = strip_text(img_full)

    results = {}
    checks = [
        ("C1_SILHOUETTE", check_silhouette_contrast),
        ("C2_MULTI_ZONE", check_multi_zone),
        ("C3_FOCAL_POINT", check_focal_point),
        ("C4_CHAR_PRESENCE", check_character_presence),
        ("C5_DEPTH_CUES", check_depth_cues),
    ]

    for name, fn in checks:
        verdict, detail = fn(stripped)
        results[name] = (verdict, detail)

    # C6 uses full image (border is outside draw area)
    v6, d6 = check_arc_border(img_full)
    results["C6_ARC_BORDER"] = (v6, d6)

    # Overall verdict
    verdicts = [r[0] for r in results.values()]
    if "FAIL" in verdicts:
        overall = "FAIL"
    elif "WARN" in verdicts:
        overall = "WARN"
    elif "SKIP" in verdicts and all(v in ("PASS", "SKIP") for v in verdicts):
        overall = "PASS (some checks skipped)"
    else:
        overall = "PASS"

    # Print results
    basename = os.path.basename(panel_path)
    print(f"\n{'=' * 70}")
    print(f"BLANK TEST: {basename}")
    print(f"{'=' * 70}")
    for name, (verdict, detail) in results.items():
        marker = {"PASS": "OK ", "WARN": "?? ", "FAIL": "XX ", "SKIP": "-- "}
        print(f"  [{marker.get(verdict, '   ')}{verdict:4s}] {name}: {detail}")
    print(f"  {'─' * 60}")
    print(f"  OVERALL: {overall}")
    print(f"{'=' * 70}")

    if save:
        os.makedirs(BLANK_TEST_DIR, exist_ok=True)
        save_name = basename.replace('.png', '_blank_test.png')
        save_path = os.path.join(BLANK_TEST_DIR, save_name)
        stripped.save(save_path, "PNG")
        print(f"  Saved text-stripped version: {save_path}")

    return overall, results


def find_panel_path(panel_id):
    """Resolve a panel ID (e.g., 'P22', 'P22a') to its file path."""
    # Try standard cold open naming
    candidates = [
        os.path.join(PANELS_DIR, f"LTG_SB_cold_open_{panel_id}.png"),
        os.path.join(PANELS_DIR, f"LTG_SB_cold_open_{panel_id.upper()}.png"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    # Fallback: glob for any match
    pattern = os.path.join(PANELS_DIR, f"*{panel_id}*")
    matches = glob_mod.glob(pattern)
    if matches:
        return matches[0]
    return None


def main():
    parser = argparse.ArgumentParser(description="Visual Blank Test — storyboard panel QA")
    parser.add_argument("--panel", type=str, help="Panel ID (e.g., P22, P22a)")
    parser.add_argument("--file", type=str, help="Direct path to panel PNG")
    parser.add_argument("--all", action="store_true", help="Test all panels in panels/")
    parser.add_argument("--save", action="store_true", help="Save text-stripped PNGs")
    args = parser.parse_args()

    if not _HAS_NUMPY:
        print("WARNING: numpy not available. Most checks will be skipped.")
        print("Install numpy for full functionality: pip install numpy")

    if args.file:
        run_blank_test(args.file, save=args.save)
    elif args.panel:
        path = find_panel_path(args.panel)
        if path:
            run_blank_test(path, save=args.save)
        else:
            print(f"ERROR: Could not find panel {args.panel} in {PANELS_DIR}")
            sys.exit(1)
    elif args.all:
        pattern = os.path.join(PANELS_DIR, "LTG_SB_cold_open_*.png")
        files = sorted(glob_mod.glob(pattern))
        if not files:
            print(f"No panels found matching {pattern}")
            sys.exit(1)
        summary = {"PASS": 0, "WARN": 0, "FAIL": 0}
        for f in files:
            result = run_blank_test(f, save=args.save)
            if result:
                overall = result[0].split()[0]  # strip "(some checks skipped)"
                summary[overall] = summary.get(overall, 0) + 1

        print(f"\n{'=' * 70}")
        print(f"BATCH SUMMARY: {len(files)} panels tested")
        print(f"  PASS: {summary.get('PASS', 0)}  |  WARN: {summary.get('WARN', 0)}  |  FAIL: {summary.get('FAIL', 0)}")
        print(f"{'=' * 70}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
