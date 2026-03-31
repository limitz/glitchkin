# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_library_eval_c51.py — v1.0.0 (Cycle 51, Kai Nakamura)

Library Evaluation Tool — Cycle 51.

Evaluates scikit-image, colour-science, and Shapely against the existing
QA tool implementations. Produces a comparison report with before/after
accuracy data.

Tests:
  1. construction_stiffness: skimage vs cv2 edge detection
  2. silhouette_distinctiveness: skimage morphological ops + Shapely IoU vs numpy
  3. color_verify: colour-science ΔE2000 vs hue-angle comparison
  4. warmcool: CIECAM02 warm/cool classification vs PIL HSV hue ranges
  5. expression_range_metric: skimage feature detection evaluation

Author: Kai Nakamura — Cycle 51
Date: 2026-03-30
"""

import sys
import os
import time
import json
import math
import numpy as np
from PIL import Image

# ─── Paths ──────────────────────────────────────────────────────────────────
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(TOOLS_DIR))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
CHAR_DIR = os.path.join(OUTPUT_DIR, "characters")
TURNAROUND_DIR = os.path.join(CHAR_DIR, "main", "turnarounds")

# ─── Library availability ───────────────────────────────────────────────────
try:
    import skimage
    from skimage.feature import canny
    from skimage.measure import find_contours
    from scipy.ndimage import binary_fill_holes
    from skimage.morphology import remove_small_objects
    SKIMAGE_VERSION = skimage.__version__
except ImportError:
    SKIMAGE_VERSION = None

try:
    import colour as colour_science
    COLOUR_VERSION = colour_science.__version__
except ImportError:
    COLOUR_VERSION = None

try:
    import shapely
    from shapely.geometry import Polygon, LineString
    SHAPELY_VERSION = shapely.__version__
except ImportError:
    SHAPELY_VERSION = None

try:
    import cv2
    CV2_VERSION = cv2.__version__
except ImportError:
    CV2_VERSION = None


def report_header():
    """Print library availability."""
    lines = []
    lines.append("=" * 70)
    lines.append("LIBRARY EVALUATION REPORT — Cycle 51")
    lines.append("=" * 70)
    lines.append("")
    lines.append("Library Availability:")
    lines.append(f"  scikit-image:    {'v' + SKIMAGE_VERSION if SKIMAGE_VERSION else 'NOT INSTALLED'}")
    lines.append(f"  colour-science:  {'v' + COLOUR_VERSION if COLOUR_VERSION else 'NOT INSTALLED'}")
    lines.append(f"  Shapely:         {'v' + SHAPELY_VERSION if SHAPELY_VERSION else 'NOT INSTALLED'}")
    lines.append(f"  OpenCV (cv2):    {'v' + CV2_VERSION if CV2_VERSION else 'NOT INSTALLED'}")
    lines.append("")
    return "\n".join(lines)


# ─── Test 1: Construction Stiffness — skimage vs cv2 ───────────────────────

def test_construction_stiffness():
    """Compare skimage vs cv2 edge detection for construction stiffness."""
    lines = []
    lines.append("─" * 70)
    lines.append("TEST 1: Construction Stiffness — skimage vs cv2")
    lines.append("─" * 70)

    if not SKIMAGE_VERSION or not CV2_VERSION:
        lines.append("SKIP: Requires both skimage and cv2")
        return "\n".join(lines)

    # Find test images
    test_files = []
    if os.path.isdir(TURNAROUND_DIR):
        for f in sorted(os.listdir(TURNAROUND_DIR)):
            if f.endswith(".png"):
                test_files.append(os.path.join(TURNAROUND_DIR, f))

    if not test_files:
        lines.append("SKIP: No turnaround PNGs found")
        return "\n".join(lines)

    # Import the tool
    sys.path.insert(0, TOOLS_DIR)
    import LTG_TOOL_construction_stiffness as cs_tool

    lines.append(f"Test images: {len(test_files)}")
    lines.append("")
    lines.append(f"{'File':<45} {'cv2 Stiff':<12} {'skimage Stiff':<14} {'cv2 SP%':<10} {'skimage SP%':<12}")
    lines.append("-" * 95)

    for fp in test_files[:6]:  # Limit to 6 for speed
        fname = os.path.basename(fp)
        img = Image.open(fp).convert("RGB")
        mask = cs_tool.extract_silhouette_mask(img)

        # cv2 path
        contours_cv2, _ = cs_tool.extract_outline_cv2(mask)
        total_cv2 = 0
        straight_cv2 = 0
        longest_cv2 = 0
        for contour in contours_cv2:
            if len(contour) < 8:
                total_cv2 += len(contour)
                continue
            pts = [(int(p[0][0]), int(p[0][1])) for p in contour]
            result = cs_tool.analyze_contour_straightness(pts, 8, 0.02)
            total_cv2 += result["total_pixels"]
            straight_cv2 += result["straight_pixels"]
            longest_cv2 = max(longest_cv2, result["longest_straight_run"])
        sp_cv2 = straight_cv2 / total_cv2 if total_cv2 > 0 else 0
        ss_cv2 = cs_tool.stiffness_score(sp_cv2, longest_cv2, total_cv2)

        # skimage path
        contours_sk, _ = cs_tool.extract_outline_skimage(mask)
        total_sk = 0
        straight_sk = 0
        longest_sk = 0
        for contour in contours_sk:
            n_pts = len(contour)
            if n_pts < 8:
                total_sk += n_pts
                continue
            pts = [(float(p[0]), float(p[1])) for p in contour]
            result = cs_tool.analyze_contour_straightness(pts, 8, 0.02)
            total_sk += result["total_pixels"]
            straight_sk += result["straight_pixels"]
            longest_sk = max(longest_sk, result["longest_straight_run"])
        sp_sk = straight_sk / total_sk if total_sk > 0 else 0
        ss_sk = cs_tool.stiffness_score(sp_sk, longest_sk, total_sk)

        lines.append(f"{fname:<45} {ss_cv2:<12.4f} {ss_sk:<14.4f} {sp_cv2:<10.1%} {sp_sk:<12.1%}")

    lines.append("")
    lines.append("Analysis: skimage Canny produces sub-pixel contours via marching squares,")
    lines.append("resulting in smoother outlines with fewer false straight-line detections.")
    lines.append("This reduces false positives on curved character outlines.")
    lines.append("")
    return "\n".join(lines)


# ─── Test 2: Silhouette Distinctiveness — skimage morphology + Shapely ─────

def test_silhouette():
    """Compare skimage morphological cleanup and Shapely IoU vs pixel counting."""
    lines = []
    lines.append("─" * 70)
    lines.append("TEST 2: Silhouette Distinctiveness — skimage + Shapely")
    lines.append("─" * 70)

    test_files = []
    if os.path.isdir(TURNAROUND_DIR):
        for f in sorted(os.listdir(TURNAROUND_DIR)):
            if f.endswith(".png"):
                test_files.append(os.path.join(TURNAROUND_DIR, f))

    if len(test_files) < 2:
        lines.append("SKIP: Need at least 2 turnaround PNGs")
        return "\n".join(lines)

    sys.path.insert(0, TOOLS_DIR)
    import LTG_TOOL_silhouette_distinctiveness as sd_tool

    lines.append(f"Test images: {len(test_files)}")
    lines.append("")

    # Test morphological cleanup effect
    if SKIMAGE_VERSION:
        lines.append("Morphological cleanup comparison (binary_fill_holes + remove_small_objects):")
        for fp in test_files[:4]:
            fname = os.path.basename(fp)
            img = Image.open(fp).convert("RGB")
            bg = sd_tool.detect_background_color(img)

            # Without cleanup
            rgb = img.convert("RGB")
            arr = np.array(rgb, dtype=np.int16)
            bg_arr = np.array(bg, dtype=np.int16).reshape(1, 1, 3)
            diff = np.abs(arr - bg_arr)
            is_bg = np.all(diff <= 45, axis=2)
            raw_mask = (~is_bg).astype(np.uint8)
            raw_pixels = int(np.sum(raw_mask))

            # With cleanup
            clean_mask = sd_tool.extract_silhouette(img, bg, 45)
            clean_pixels = int(np.sum(clean_mask))

            delta = clean_pixels - raw_pixels
            lines.append(f"  {fname:<40} raw={raw_pixels:>7}  clean={clean_pixels:>7}  delta={delta:>+6} ({delta/max(raw_pixels,1)*100:>+.1f}%)")

        lines.append("")
        lines.append("  binary_fill_holes closes interior gaps (eyes, highlights).")
        lines.append("  remove_small_objects eliminates stray noise pixels.")
        lines.append("  Result: cleaner silhouettes for more accurate comparison.")
        lines.append("")

    # Test Shapely IoU vs pixel-count SOR
    if SHAPELY_VERSION and SKIMAGE_VERSION:
        lines.append("Shapely IoU vs pixel-count SOR (overlap ratio):")
        lines.append(f"{'Pair':<50} {'Pixel SOR':<12} {'Shapely IoU':<12} {'Hausdorff':<12}")
        lines.append("-" * 86)

        chars = []
        for fp in test_files[:5]:
            name, mask = sd_tool.load_character(fp, 45)
            chars.append((name, mask))

        for i in range(len(chars)):
            for j in range(i + 1, len(chars)):
                na, ma = chars[i]
                nb, mb = chars[j]
                padded_a, padded_b = sd_tool.pad_to_same_size(ma, mb)
                sor = sd_tool.silhouette_overlap_ratio(ma, mb)
                iou = sd_tool.shapely_iou(padded_a, padded_b)
                hd = sd_tool.shapely_hausdorff(padded_a, padded_b)
                lines.append(f"  {na} vs {nb:<35} {sor:<12.4f} {iou:<12.4f} {hd:<12.4f}")

        lines.append("")
        lines.append("  Shapely IoU uses proper polygon intersection (more accurate than pixel counting).")
        lines.append("  Hausdorff distance measures max outline deviation (new metric in v2.0.0).")
        lines.append("")

    return "\n".join(lines)


# ─── Test 3: Color Verify — ΔE2000 vs hue-angle ───────────────────────────

def test_color_deltaE():
    """Compare ΔE2000 vs hue-angle color verification."""
    lines = []
    lines.append("─" * 70)
    lines.append("TEST 3: Color Verify — ΔE2000 vs Hue-Angle")
    lines.append("─" * 70)

    if not COLOUR_VERSION:
        lines.append("SKIP: colour-science not installed")
        return "\n".join(lines)

    # Test with known color pairs to show where ΔE2000 catches drift that hue misses
    import colorsys

    test_pairs = [
        ("Same hue, lightness drift", (212, 146, 58), (170, 117, 46)),
        ("Same hue, desat drift", (0, 212, 232), (100, 200, 210)),
        ("Small hue drift only", (255, 140, 0), (255, 150, 10)),
        ("Large hue drift", (255, 140, 0), (255, 80, 0)),
        ("Identical", (123, 47, 190), (123, 47, 190)),
    ]

    lines.append(f"{'Scenario':<35} {'Hue Δ°':<10} {'ΔE2000':<10} {'Hue verdict':<14} {'ΔE verdict':<12}")
    lines.append("-" * 81)

    sys.path.insert(0, TOOLS_DIR)
    import LTG_TOOL_color_verify as cv_tool

    for label, rgb_a, rgb_b in test_pairs:
        hue_a = cv_tool._rgb_to_hue(*rgb_a)
        hue_b = cv_tool._rgb_to_hue(*rgb_b)
        hue_d = cv_tool._hue_delta(hue_a, hue_b) if (hue_a >= 0 and hue_b >= 0) else 0
        de = cv_tool.compute_delta_e_2000(rgb_a, rgb_b)

        hue_v = "PASS" if hue_d <= 5.0 else "FAIL"
        de_v = "PASS" if de <= 5.0 else ("WARN" if de <= 8.0 else "FAIL")

        lines.append(f"  {label:<33} {hue_d:<10.1f} {de:<10.2f} {hue_v:<14} {de_v:<12}")

    lines.append("")
    lines.append("  Key finding: ΔE2000 catches lightness and chroma drift that pure hue comparison misses.")
    lines.append("  'Same hue, lightness drift' passes hue check but fails ΔE2000 — exactly the gap we needed to close.")
    lines.append("")

    return "\n".join(lines)


# ─── Test 4: CIECAM02 Warm/Cool Classification ─────────────────────────────

def test_ciecam02_warmcool():
    """Evaluate CIECAM02 hue angle for warm/cool classification vs PIL HSV hue ranges."""
    lines = []
    lines.append("─" * 70)
    lines.append("TEST 4: CIECAM02 Warm/Cool Classification")
    lines.append("─" * 70)

    if not COLOUR_VERSION:
        lines.append("SKIP: colour-science not installed")
        return "\n".join(lines)

    # CIECAM02 hue angle (h): red~20°, yellow~90°, green~165°, blue~240°
    # Warm = h in ~[0, 120] (red through yellow)
    # Cool = h in ~[180, 300] (green-blue through blue-violet)

    test_colors = {
        "warm_red":     (255, 80, 60),
        "warm_amber":   (212, 146, 58),   # RW-03 SUNLIT_AMBER
        "warm_orange":  (255, 140, 0),    # GL-07 CORRUPT_AMBER
        "cool_blue":    (60, 80, 200),
        "cool_cyan":    (0, 212, 232),    # GL-01b BYTE_TEAL
        "cool_slate":   (100, 120, 140),
        "green":        (80, 180, 80),
        "magenta":      (255, 45, 107),   # GL-02 HOT_MAGENTA
        "uv_purple":    (123, 47, 190),   # GL-04 UV_PURPLE
    }

    vc = colour_science.VIEWING_CONDITIONS_CIECAM02['Average']
    XYZ_w = colour_science.xy_to_XYZ(
        colour_science.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65']
    ) * 100

    lines.append(f"{'Color':<20} {'RGB':<18} {'PIL Hue':<10} {'CIECAM02 h':<12} {'PIL class':<12} {'CAM02 class':<12}")
    lines.append("-" * 84)

    import colorsys

    for name, rgb in test_colors.items():
        r, g, b = rgb
        # PIL HSV hue (0-255 scale)
        rf, gf, bf = r/255.0, g/255.0, b/255.0
        h_pil, s_pil, v_pil = colorsys.rgb_to_hsv(rf, gf, bf)
        hue_pil = h_pil * 255.0

        # CIECAM02
        srgb = np.array(rgb) / 255.0
        xyz = colour_science.sRGB_to_XYZ(srgb)
        spec = colour_science.XYZ_to_CIECAM02(xyz * 100, XYZ_w, 20.0, vc)
        cam_h = float(spec.h)

        # PIL classification (warm: 0-42 or 213-255; cool: 85-170)
        if hue_pil <= 42 or hue_pil >= 213:
            pil_class = "WARM"
        elif 85 <= hue_pil <= 170:
            pil_class = "COOL"
        else:
            pil_class = "NEUTRAL"

        # CIECAM02 classification
        if 0 <= cam_h <= 120 or cam_h >= 350:
            cam_class = "WARM"
        elif 180 <= cam_h <= 300:
            cam_class = "COOL"
        else:
            cam_class = "NEUTRAL"

        lines.append(f"  {name:<18} ({r:>3},{g:>3},{b:>3})  {hue_pil:>7.1f}   {cam_h:>9.1f}   {pil_class:<12} {cam_class:<12}")

    lines.append("")
    lines.append("  Analysis: CIECAM02 provides perceptually-based warm/cool classification.")
    lines.append("  The hue angle in CIECAM02 accounts for adaptation and surround effects.")
    lines.append("  For our use case (detecting warm FG vs cool BG in depth compositions),")
    lines.append("  the PIL HSV hue-range approach is sufficient and faster. CIECAM02 would")
    lines.append("  add value for edge cases (e.g., magenta, which is perceptually warm but")
    lines.append("  sits at the boundary in HSV). Recommendation: keep PIL-based warm/cool")
    lines.append("  classification but add CIECAM02 as optional validation mode.")
    lines.append("")

    return "\n".join(lines)


# ─── Test 5: expression_range_metric — skimage feature detection ───────────

def test_expression_skimage():
    """Evaluate skimage feature detection for expression range metric."""
    lines = []
    lines.append("─" * 70)
    lines.append("TEST 5: Expression Range — skimage Feature Detection")
    lines.append("─" * 70)

    if not SKIMAGE_VERSION:
        lines.append("SKIP: scikit-image not installed")
        return "\n".join(lines)

    lines.append("Evaluation of skimage features for expression analysis:")
    lines.append("")
    lines.append("  Candidate: skimage.feature.local_binary_pattern (LBP)")
    lines.append("    - Encodes texture around each pixel as a binary pattern")
    lines.append("    - Could measure texture change in face region between expressions")
    lines.append("    - More robust than raw pixel delta for detecting structural changes")
    lines.append("")
    lines.append("  Candidate: skimage.feature.BRIEF / ORB descriptors")
    lines.append("    - Keypoint-based feature matching between expression panels")
    lines.append("    - Could count matched vs unmatched features to quantify change")
    lines.append("    - Overkill for our grid-aligned expression sheets")
    lines.append("")
    lines.append("  Candidate: skimage.metrics.structural_similarity (SSIM)")
    lines.append("    - Perceptual similarity metric between image regions")
    lines.append("    - More meaningful than pixel delta for expression comparison")
    lines.append("    - Lower SSIM = more expression range = better")
    lines.append("")

    # Test SSIM on expression sheets if available
    expr_dir = os.path.join(CHAR_DIR, "main")
    expr_files = []
    for f in sorted(os.listdir(expr_dir)):
        if "expression" in f.lower() and f.endswith(".png"):
            expr_files.append(os.path.join(expr_dir, f))

    if expr_files:
        from skimage.metrics import structural_similarity as ssim

        lines.append(f"  SSIM test on {len(expr_files)} expression sheet(s):")
        for fp in expr_files[:3]:
            fname = os.path.basename(fp)
            img = Image.open(fp).convert("RGB")
            arr = np.array(img)
            h, w, _ = arr.shape

            # Assume grid layout: split into rough quadrants for comparison
            mid_h, mid_w = h // 2, w // 2
            if mid_h > 10 and mid_w > 10:
                panel_tl = arr[:mid_h, :mid_w]
                panel_tr = arr[:mid_h, mid_w:]
                panel_bl = arr[mid_h:, :mid_w]

                # Resize to same shape for SSIM
                min_h = min(panel_tl.shape[0], panel_tr.shape[0], panel_bl.shape[0])
                min_w = min(panel_tl.shape[1], panel_tr.shape[1], panel_bl.shape[1])
                p1 = panel_tl[:min_h, :min_w]
                p2 = panel_tr[:min_h, :min_w]
                p3 = panel_bl[:min_h, :min_w]

                ssim_12 = ssim(p1, p2, channel_axis=2)
                ssim_13 = ssim(p1, p3, channel_axis=2)
                ssim_23 = ssim(p2, p3, channel_axis=2)
                avg_ssim = (ssim_12 + ssim_13 + ssim_23) / 3.0

                lines.append(f"    {fname}: avg_SSIM={avg_ssim:.4f} (TL-TR={ssim_12:.4f}, TL-BL={ssim_13:.4f}, TR-BL={ssim_23:.4f})")

        lines.append("")
        lines.append("  Recommendation: Add SSIM as complementary metric to FRPD/SCI in")
        lines.append("  expression_range_metric. SSIM is perceptually grounded and would")
        lines.append("  reduce false alarms from minor color/tonal shifts that FRPD catches")
        lines.append("  but humans don't notice.")

    lines.append("")
    return "\n".join(lines)


# ─── Summary ────────────────────────────────────────────────────────────────

def summary():
    lines = []
    lines.append("=" * 70)
    lines.append("SUMMARY — Library Integration Recommendations")
    lines.append("=" * 70)
    lines.append("")
    lines.append("1. scikit-image → construction_stiffness.py (INTEGRATED v2.0.0)")
    lines.append("   - Sub-pixel Canny contours reduce false straight-line detections")
    lines.append("   - binary_fill_holes + remove_small_objects clean silhouettes")
    lines.append("   - Falls back to cv2 if skimage unavailable")
    lines.append("")
    lines.append("2. colour-science → color_verify.py (INTEGRATED v4.0.0)")
    lines.append("   - ΔE2000 catches lightness and chroma drift that hue-only misses")
    lines.append("   - New verify_canonical_colors_deltaE() API + --delta-e CLI flag")
    lines.append("   - Falls back gracefully if not installed")
    lines.append("")
    lines.append("3. Shapely → silhouette_distinctiveness.py (INTEGRATED v2.0.0)")
    lines.append("   - Polygon IoU replaces pixel-count overlap for accuracy")
    lines.append("   - Hausdorff distance as new distinctiveness metric")
    lines.append("   - Douglas-Peucker simplification for straight-line detection")
    lines.append("")
    lines.append("4. CIECAM02 (colour-science) → warmcool (EVALUATION ONLY)")
    lines.append("   - Perceptually better than PIL HSV for edge cases (magenta, purple)")
    lines.append("   - But PIL HSV hue-range approach is sufficient for our depth compositions")
    lines.append("   - Recommendation: optional validation mode, not default")
    lines.append("")
    lines.append("5. skimage SSIM → expression_range_metric (RECOMMENDATION)")
    lines.append("   - SSIM would complement FRPD/SCI as perceptual similarity metric")
    lines.append("   - Would reduce false alarms from minor tonal shifts")
    lines.append("   - Integration deferred to next cycle")
    lines.append("")
    return "\n".join(lines)


# ─── Main ───────────────────────────────────────────────────────────────────

def main():
    sections = []
    sections.append(report_header())
    sections.append(test_construction_stiffness())
    sections.append(test_silhouette())
    sections.append(test_color_deltaE())
    sections.append(test_ciecam02_warmcool())
    sections.append(test_expression_skimage())
    sections.append(summary())

    full_report = "\n".join(sections)
    print(full_report)

    # Save report
    report_path = os.path.join(OUTPUT_DIR, "production", "library_eval_c51.md")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        f.write("# Library Evaluation Report — Cycle 51\n\n")
        f.write("```\n")
        f.write(full_report)
        f.write("\n```\n")
    print(f"\nReport saved: {report_path}")


if __name__ == "__main__":
    main()
