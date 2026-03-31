#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_visual_blank_test.py
Visual Blank Test Checklist — Storyboard Panel QA Tool
Diego Vargas, Storyboard Artist — Cycle 49 (panel-type profiles added)

PURPOSE:
Every storyboard panel should communicate its beat WITHOUT text. If the beat lives only
in the captions/annotations, the panel has failed as a board. This tool:

1. Takes any storyboard panel PNG
2. Renders a text-stripped version (caption bar removed, annotation regions masked)
3. Applies panel-type-specific thresholds (ECU, MCU, WIDE, INSERT, OTS, TWO_SHOT)
4. Runs a checklist of visual readability metrics
5. Outputs PASS / WARN / FAIL per check, with an overall verdict

PANEL-TYPE PROFILES (C49):
  ECU        — Extreme close-up (face fills frame). Low FG/BG delta OK if internal
               contrast is strong. Depth cues not expected. Focal point concentrated.
  MCU        — Medium close-up. Character fills most of frame. Some BG visible.
               Moderate depth cues. Character presence in upper zone.
  WIDE       — Wide/establishing shot. Strong FG/BG contrast expected. Multi-zone
               composition required. Depth temperature rule applies fully.
  INSERT     — Prop/detail insert (notebook, screen). No character silhouette expected.
               Internal texture/contrast matters. No depth cue requirement.
  OTS        — Over-the-shoulder. Strong silhouette contrast (FG silhouette vs BG).
               Depth cues expected. Focal point in mid-frame.
  TWO_SHOT   — Two characters in frame. Multi-zone required. Depth cues expected.
               Character presence in left+right zones.
  DEFAULT    — Generic fallback (original C48 thresholds).

CHECKS:
  C1 — SILHOUETTE CONTRAST
  C2 — MULTI-ZONE COMPOSITION
  C3 — FOCAL POINT
  C4 — CHARACTER PRESENCE
  C5 — DEPTH CUES
  C6 — ARC COLOR BORDER

USAGE:
  python LTG_TOOL_visual_blank_test.py --panel P22
  python LTG_TOOL_visual_blank_test.py --panel P22 --type ECU
  python LTG_TOOL_visual_blank_test.py --file path/to/panel.png --type WIDE
  python LTG_TOOL_visual_blank_test.py --all         # auto-detects panel types
  python LTG_TOOL_visual_blank_test.py --all --save   # save text-stripped PNGs

OUTPUT:
  Prints checklist results per panel with applied profile. If --save, writes
  <panel>_blank_test.png to output/production/blank_tests/
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


# ---------------------------------------------------------------------------
# Panel-Type Profiles — threshold overrides per shot type
# ---------------------------------------------------------------------------
# Each profile is a dict of check_name -> {thresholds}.
# Missing keys fall back to DEFAULT profile values.

PROFILES = {
    "DEFAULT": {
        "C1_SILHOUETTE": {
            "delta_pass": 15, "delta_warn": 10,
            "std_pass": 20, "std_warn": 14,
        },
        "C2_MULTI_ZONE": {
            "spread_pass": 16, "spread_fail": 8,
        },
        "C3_FOCAL_POINT": {
            "diffuse_warn": 0.40,
        },
        "C4_CHAR_PRESENCE": {
            "ed_pass": 4, "ed_warn": 1.5,
        },
        "C5_DEPTH_CUES": {
            "delta_pass": 5,
        },
        "C6_ARC_BORDER": {
            "sat_pass": 0.30,
        },
    },
    "ECU": {
        # ECU panels fill the frame with a face or single element.
        # FG/BG delta is often low because there IS no distinct BG.
        # Internal contrast (center std) is the primary metric.
        "C1_SILHOUETTE": {
            "delta_pass": 8, "delta_warn": 5,
            "std_pass": 14, "std_warn": 10,
        },
        # Quadrant spread is naturally low on a face — relax threshold.
        "C2_MULTI_ZONE": {
            "spread_pass": 10, "spread_fail": 4,
        },
        # Focal energy should be concentrated (face features).
        "C3_FOCAL_POINT": {
            "diffuse_warn": 0.35,
        },
        # Edge density expected in upper region (face features, eyes, brows).
        "C4_CHAR_PRESENCE": {
            "ed_pass": 3, "ed_warn": 1.0,
        },
        # Depth cues NOT expected for ECU — exempt. Very low threshold.
        "C5_DEPTH_CUES": {
            "delta_pass": 2,
        },
        "C6_ARC_BORDER": {
            "sat_pass": 0.30,
        },
    },
    "MCU": {
        # Medium close-up. Character fills 60-80% of frame. Some BG.
        "C1_SILHOUETTE": {
            "delta_pass": 12, "delta_warn": 8,
            "std_pass": 18, "std_warn": 12,
        },
        "C2_MULTI_ZONE": {
            "spread_pass": 12, "spread_fail": 6,
        },
        "C3_FOCAL_POINT": {
            "diffuse_warn": 0.40,
        },
        "C4_CHAR_PRESENCE": {
            "ed_pass": 3, "ed_warn": 1.5,
        },
        "C5_DEPTH_CUES": {
            "delta_pass": 3,
        },
        "C6_ARC_BORDER": {
            "sat_pass": 0.30,
        },
    },
    "WIDE": {
        # Wide/establishing shots need strong spatial structure.
        "C1_SILHOUETTE": {
            "delta_pass": 18, "delta_warn": 12,
            "std_pass": 22, "std_warn": 16,
        },
        "C2_MULTI_ZONE": {
            "spread_pass": 18, "spread_fail": 10,
        },
        "C3_FOCAL_POINT": {
            "diffuse_warn": 0.45,
        },
        # Characters may be small — lower edge density OK.
        "C4_CHAR_PRESENCE": {
            "ed_pass": 3, "ed_warn": 1.2,
        },
        # Depth temperature rule applies fully.
        "C5_DEPTH_CUES": {
            "delta_pass": 6,
        },
        "C6_ARC_BORDER": {
            "sat_pass": 0.30,
        },
    },
    "INSERT": {
        # Prop/detail insert. No character silhouette expected.
        # Internal texture matters (notebook lines, screen pixels).
        "C1_SILHOUETTE": {
            "delta_pass": 8, "delta_warn": 4,
            "std_pass": 12, "std_warn": 8,
        },
        # Can be single-zone (one prop fills frame).
        "C2_MULTI_ZONE": {
            "spread_pass": 6, "spread_fail": 2,
        },
        "C3_FOCAL_POINT": {
            "diffuse_warn": 0.50,
        },
        # No character expected — edge density from prop detail only.
        "C4_CHAR_PRESENCE": {
            "ed_pass": 1.5, "ed_warn": 0.5,
        },
        # No depth cue expected for inserts.
        "C5_DEPTH_CUES": {
            "delta_pass": 1,
        },
        "C6_ARC_BORDER": {
            "sat_pass": 0.30,
        },
    },
    "OTS": {
        # Over-the-shoulder. FG silhouette vs BG subject.
        "C1_SILHOUETTE": {
            "delta_pass": 18, "delta_warn": 12,
            "std_pass": 20, "std_warn": 14,
        },
        "C2_MULTI_ZONE": {
            "spread_pass": 16, "spread_fail": 8,
        },
        "C3_FOCAL_POINT": {
            "diffuse_warn": 0.40,
        },
        "C4_CHAR_PRESENCE": {
            "ed_pass": 4, "ed_warn": 1.5,
        },
        "C5_DEPTH_CUES": {
            "delta_pass": 5,
        },
        "C6_ARC_BORDER": {
            "sat_pass": 0.30,
        },
    },
    "TWO_SHOT": {
        # Two characters in frame. Multi-zone required.
        "C1_SILHOUETTE": {
            "delta_pass": 14, "delta_warn": 10,
            "std_pass": 20, "std_warn": 14,
        },
        "C2_MULTI_ZONE": {
            "spread_pass": 14, "spread_fail": 8,
        },
        "C3_FOCAL_POINT": {
            # Two-shots can have diffuse energy (two focal points).
            "diffuse_warn": 0.50,
        },
        "C4_CHAR_PRESENCE": {
            "ed_pass": 4, "ed_warn": 1.5,
        },
        "C5_DEPTH_CUES": {
            "delta_pass": 4,
        },
        "C6_ARC_BORDER": {
            "sat_pass": 0.30,
        },
    },
}

# Panel-type auto-detection map: panel ID -> profile name.
# Derived from PANEL_MAP.md beat descriptions.
PANEL_TYPE_MAP = {
    "P01": "WIDE",
    "P02": "WIDE",
    "P03": "ECU",         # CU Monitor — single prop fills frame
    "P04": "WIDE",
    "P05": "MCU",         # MCU Monitor — camera inside shelf
    "P06": "ECU",         # CU Monitor Screen — Byte face pressed to glass
    "P07": "WIDE",        # MED WIDE, low angle, Dutch tilt
    "P08": "MCU",         # MED — Byte full body reveal
    "P09": "WIDE",        # MED WIDE — Byte floating, spots Luma
    "P10": "OTS",         # OTS — Byte's POV looking at Luma
    "P11": "ECU",         # ECU — Luma's closed eyes
    "P12": "TWO_SHOT",   # CU TWO-SHOT — Luma and Byte
    "P13": "TWO_SHOT",   # MIRROR COMPOSITION — two-shot
    "P14": "MCU",         # MED — Byte ricochets (action, but character fills frame)
    "P15": "MCU",         # MED — Luma hits floor
    "P16": "ECU",         # ECU — Luma's face pressed to floor
    "P17": "TWO_SHOT",   # MED two-shot stillness
    "P18": "INSERT",      # CU/INSERT — Notebook page
    "P19": "TWO_SHOT",   # MED two-shot dialogue
    "P20": "TWO_SHOT",   # MED WIDE two-shot
    "P21": "WIDE",        # WIDE HIGH ANGLE — re-escalation
    "P22": "ECU",         # ECU MONITOR — Glitchkin pressing
    "P22a": "MCU",        # MCU INSERT — Byte on shoulder
    "P23": "OTS",         # MED OTS reverse — backs to camera
    "P24": "WIDE",        # WIDE/MED — chaos apex
    "P25": "INSERT",      # TITLE CARD — pixel assembly
}


def get_profile(panel_type):
    """Get the threshold profile for a panel type, falling back to DEFAULT."""
    base = PROFILES["DEFAULT"].copy()
    if panel_type and panel_type.upper() in PROFILES:
        overrides = PROFILES[panel_type.upper()]
        for check_name, thresholds in overrides.items():
            if check_name in base:
                base[check_name] = {**base[check_name], **thresholds}
            else:
                base[check_name] = thresholds
    return base


def detect_panel_type(panel_path):
    """Auto-detect panel type from filename using PANEL_TYPE_MAP."""
    basename = os.path.basename(panel_path)
    # Try to extract panel ID from filename
    # Pattern: LTG_SB_cold_open_P22a.png -> P22a
    import re
    match = re.search(r'_P(\d+[a-z]?)\b', basename, re.IGNORECASE)
    if match:
        panel_id = "P" + match.group(1)
        if panel_id in PANEL_TYPE_MAP:
            return PANEL_TYPE_MAP[panel_id]
    # Act panels — default to MCU (reasonable for character panels)
    if 'act1_panel' in basename or 'act2_panel' in basename:
        return "MCU"
    # Episode panels
    if 'ep05_covetous' in basename:
        return "TWO_SHOT"  # Three-character triangulation
    return "DEFAULT"


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


def check_silhouette_contrast(img, profile):
    """C1: Foreground-background luminance delta.

    Uses two methods: (A) center-vs-edges mean delta, (B) overall luma standard
    deviation in the central region. Either passing is sufficient.
    """
    th = profile["C1_SILHOUETTE"]
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

    if delta_a >= th["delta_pass"] or center_std >= th["std_pass"]:
        detail = f"FG/BG delta={delta_a:.1f}, center std={center_std:.1f}"
        if delta_a < th["delta_pass"]:
            detail += " (internal contrast carries)"
        return "PASS", detail
    elif delta_a >= th["delta_warn"] or center_std >= th["std_warn"]:
        return "WARN", f"FG/BG delta={delta_a:.1f}, center std={center_std:.1f} (marginal)"
    return "FAIL", f"FG/BG delta={delta_a:.1f}, center std={center_std:.1f} (need delta>{th['delta_pass']} or std>{th['std_pass']})"


def check_multi_zone(img, profile):
    """C2: Quadrant variance — are there distinct spatial zones?"""
    th = profile["C2_MULTI_ZONE"]
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
    if spread < th["spread_fail"]:
        return "FAIL", f"Quadrant spread = {spread:.1f} (flat — need >{th['spread_fail']})"
    elif spread < th["spread_pass"]:
        return "WARN", f"Quadrant spread = {spread:.1f} (low variance — >{th['spread_pass']} ideal)"
    return "PASS", f"Quadrant spread = {spread:.1f}"


def check_focal_point(img, profile):
    """C3: Is there a clear region of highest visual energy?"""
    th = profile["C3_FOCAL_POINT"]
    if not _HAS_NUMPY:
        return "SKIP", "numpy not available"
    arr = np.array(img.convert('RGB')).astype(float)
    h, w = arr.shape[:2]
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

    hot_ratio = hot_count / total_blocks
    if hot_ratio > th["diffuse_warn"]:
        return "WARN", f"Energy spread across {hot_ratio:.0%} of frame (diffuse — may lack focal point)"
    return "PASS", f"Focal energy concentrated in {hot_ratio:.0%} of frame"


def check_character_presence(img, profile):
    """C4: Edge density — are characters/forms present?

    Checks both the central band AND the upper-center region (for MCU panels
    where the face is in the upper portion and body fills below). The higher
    of the two scores is used.
    """
    th = profile["C4_CHAR_PRESENCE"]
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

    if edge_density < th["ed_warn"]:
        return "FAIL", f"Edge density = {edge_density:.1f} ({source}) (no character-scale forms — need >{th['ed_warn']})"
    elif edge_density < th["ed_pass"]:
        return "WARN", f"Edge density = {edge_density:.1f} ({source}) (low — profile threshold >{th['ed_pass']})"
    return "PASS", f"Edge density = {edge_density:.1f} ({source})"


def check_depth_cues(img, profile):
    """C5: Warm/cool temperature separation between upper and lower halves."""
    th = profile["C5_DEPTH_CUES"]
    if not _HAS_NUMPY:
        return "SKIP", "numpy not available"
    arr = np.array(img.convert('RGB')).astype(float)
    h, w = arr.shape[:2]
    warmth = arr[:, :, 0] - arr[:, :, 2]  # positive = warm, negative = cool
    upper = np.mean(warmth[:h // 2, :])
    lower = np.mean(warmth[h // 2:, :])
    delta = abs(upper - lower)
    if delta < th["delta_pass"]:
        return "WARN", f"Warm/cool split = {delta:.1f} (flat depth — >{th['delta_pass']} needed)"
    return "PASS", f"Warm/cool split = {delta:.1f} (upper={upper:.1f}, lower={lower:.1f})"


def check_arc_border(img_full, profile):
    """C6: Is the arc-color border present? Checks the original full image (with border)."""
    th = profile["C6_ARC_BORDER"]
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
    saturation = np.max(border, axis=1) - np.min(border, axis=1)
    high_sat = np.mean(saturation > 60)
    if high_sat < th["sat_pass"]:
        return "WARN", f"Border saturation = {high_sat:.0%} pixels saturated (arc border may be missing)"
    return "PASS", f"Border saturation = {high_sat:.0%} pixels saturated — arc border present"


def run_blank_test(panel_path, save=False, panel_type=None):
    """Run the full blank test checklist on a single panel.

    Args:
        panel_path: Path to the panel PNG.
        save: If True, save text-stripped PNG.
        panel_type: Override panel type. If None, auto-detect.

    Returns:
        (overall_verdict, results_dict, detected_type) or None on error.
    """
    if not os.path.exists(panel_path):
        print(f"  ERROR: File not found: {panel_path}")
        return None

    # Detect or use provided panel type
    if panel_type:
        ptype = panel_type.upper()
    else:
        ptype = detect_panel_type(panel_path)

    profile = get_profile(ptype)

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
        verdict, detail = fn(stripped, profile)
        results[name] = (verdict, detail)

    # C6 uses full image (border is outside draw area)
    v6, d6 = check_arc_border(img_full, profile)
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
    print(f"BLANK TEST: {basename}  [profile: {ptype}]")
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

    return overall, results, ptype


def find_panel_path(panel_id):
    """Resolve a panel ID (e.g., 'P22', 'P22a') to its file path."""
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
    parser.add_argument("--type", type=str, default=None,
                        choices=["ECU", "MCU", "WIDE", "INSERT", "OTS", "TWO_SHOT", "DEFAULT"],
                        help="Override panel type (auto-detected if omitted)")
    parser.add_argument("--list-profiles", action="store_true",
                        help="Print all panel-type profiles and exit")
    args = parser.parse_args()

    if args.list_profiles:
        print("Panel-Type Profiles:")
        print("=" * 70)
        for ptype, checks in sorted(PROFILES.items()):
            print(f"\n  {ptype}:")
            for check_name, thresholds in sorted(checks.items()):
                th_str = ", ".join(f"{k}={v}" for k, v in thresholds.items())
                print(f"    {check_name}: {th_str}")
        print(f"\nAuto-detection map (PANEL_TYPE_MAP):")
        for pid, ptype in sorted(PANEL_TYPE_MAP.items()):
            print(f"    {pid} -> {ptype}")
        return

    if not _HAS_NUMPY:
        print("WARNING: numpy not available. Most checks will be skipped.")
        print("Install numpy for full functionality: pip install numpy")

    if args.file:
        run_blank_test(args.file, save=args.save, panel_type=args.type)
    elif args.panel:
        path = find_panel_path(args.panel)
        if path:
            run_blank_test(path, save=args.save, panel_type=args.type)
        else:
            print(f"ERROR: Could not find panel {args.panel} in {PANELS_DIR}")
            sys.exit(1)
    elif args.all:
        pattern = os.path.join(PANELS_DIR, "LTG_SB_cold_open_*.png")
        files = sorted(glob_mod.glob(pattern))
        # Also include episode panels and act panels
        ep_pattern = os.path.join(PANELS_DIR, "LTG_SB_ep*.png")
        files += sorted(glob_mod.glob(ep_pattern))
        if not files:
            print(f"No panels found matching {pattern}")
            sys.exit(1)
        summary = {"PASS": 0, "WARN": 0, "FAIL": 0}
        type_summary = {}
        for f in files:
            result = run_blank_test(f, save=args.save, panel_type=args.type)
            if result:
                overall, _results, ptype = result
                overall_key = overall.split()[0]  # strip "(some checks skipped)"
                summary[overall_key] = summary.get(overall_key, 0) + 1
                if ptype not in type_summary:
                    type_summary[ptype] = {"PASS": 0, "WARN": 0, "FAIL": 0}
                type_summary[ptype][overall_key] = type_summary[ptype].get(overall_key, 0) + 1

        print(f"\n{'=' * 70}")
        print(f"BATCH SUMMARY: {len(files)} panels tested")
        print(f"  PASS: {summary.get('PASS', 0)}  |  WARN: {summary.get('WARN', 0)}  |  FAIL: {summary.get('FAIL', 0)}")
        print(f"\n  By panel type:")
        for ptype, counts in sorted(type_summary.items()):
            print(f"    {ptype:12s}: PASS={counts.get('PASS',0)} WARN={counts.get('WARN',0)} FAIL={counts.get('FAIL',0)}")
        print(f"{'=' * 70}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
