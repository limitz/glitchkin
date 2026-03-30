#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_multi_char_face_gate.py
Multi-Character Face Gate — validates face legibility for all characters
in a multi-character composition (style frames, lineup, etc.).

C49 — Maya Santos (Character Designer)

Purpose:
  The single-character face test (LTG_TOOL_character_face_test.py) validates
  expression variants for one character at a time in isolation. This tool
  validates face legibility for ALL characters as they actually appear in a
  composed multi-character image (SF06, lineup, etc.), where scale, overlap,
  and lighting may degrade face reads.

Approach:
  1. Load the target PNG.
  2. For each character in the manifest, crop the face region (head_cx, head_cy,
     head_r from the manifest).
  3. Analyze the face crop:
     - EYE_CONTRAST: dark-vs-light region count in the eye zone (top 60% of face).
       Eyes need dark pupils against lighter sclera/skin.
     - FEATURE_COUNT: number of distinct dark features (eyes, brows, mouth)
       detected via connected-component analysis on thresholded face crop.
     - MIN_FEATURE_SIZE: smallest feature must be >= 2px in both dimensions
       (below 2px = invisible at render scale).
  4. Report PASS / WARN / FAIL per character, plus overall verdict.

Manifests:
  Pre-defined manifests for known compositions. Custom manifests via JSON.
  Each entry: {"char": str, "head_cx": int, "head_cy": int, "head_r": int}

  Known manifests:
    sf06   — SF06 "The Hand-Off" (Miri + Luma)
    lineup — Character Lineup v011 (Cosmo + Miri + Luma + Byte + Glitch)

Usage:
  python3 LTG_TOOL_multi_char_face_gate.py --manifest sf06
  python3 LTG_TOOL_multi_char_face_gate.py --manifest lineup
  python3 LTG_TOOL_multi_char_face_gate.py --manifest custom.json --image path/to/image.png
  python3 LTG_TOOL_multi_char_face_gate.py --manifest sf06 --output report.png

Output:
  - Console report with per-character PASS/WARN/FAIL
  - Optional diagnostic PNG showing face crops with annotations (<=1280px)
  - Exit code: 0=PASS, 1=WARN, 2=FAIL

Integration with precritique_qa:
  Import and call run_multi_char_face_gate(image_path, manifest) which returns
  a dict with per-character results and overall verdict. The precritique_qa
  pipeline can add this as Section 14.
"""

import os
import sys
import json
import argparse
import math
from PIL import Image, ImageDraw

# ── Output rule: hard limit ≤ 1280px in both dimensions ──────────────────────
MAX_DIM = 1280

# ── Paths ────────────────────────────────────────────────────────────────────
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(TOOLS_DIR, os.pardir)
PRODUCTION_DIR = os.path.join(OUTPUT_DIR, "production")

# ── Palette for diagnostic output ────────────────────────────────────────────
PASS_COLOR = (60, 200, 80)
WARN_COLOR = (220, 160, 40)
FAIL_COLOR = (220, 60, 60)
HEADER_COLOR = (0, 220, 240)
LABEL_COLOR = (200, 200, 200)
PANEL_BG = (28, 28, 36)

# ── Thresholds ───────────────────────────────────────────────────────────────
# Minimum number of distinct dark features in face region for PASS
MIN_FEATURES_PASS = 3      # eyes (2) + mouth or brows (1+)
MIN_FEATURES_WARN = 2      # at least 2 features visible
# Minimum feature size in pixels (width or height)
MIN_FEATURE_PX = 2
# Eye contrast: minimum luminance difference between darkest and lightest
# regions in the eye zone
MIN_EYE_CONTRAST_PASS = 40
MIN_EYE_CONTRAST_WARN = 25
# Dark pixel threshold for feature detection (luminance)
DARK_THRESHOLD = 100

# ── Byte detection ───────────────────────────────────────────────────────────
# Byte uses pixel-grid eyes, not organic face features.
# For Byte: check for distinct colored pixel clusters (teal + magenta).
BYTE_TEAL_RANGE = ((0, 160, 180), (50, 255, 255))    # teal eye pixels
BYTE_MAG_RANGE = ((200, 20, 60), (255, 100, 150))     # magenta crack pixels

# ── Pre-defined manifests ────────────────────────────────────────────────────
# SF06: "The Hand-Off" — Miri (left) + Luma (right)
# Positions computed from LTG_TOOL_sf_miri_luma_handoff.py constants:
#   W=1280, H=720, GROUND_Y=int(720*0.90)=648
#   Miri: cx=int(1280*0.285)=364, HR=42, HU=84, total_h=int(84*3.2)=268
#         head_cy = 648-268+42 = 422
#         C49 elder lean: head_cx = 364 + int(84*0.04) = 367
#   Luma: cx=int(1280*0.72)=921, HR=46, HU=92, total_h=int(92*3.5)=322
#         head_cy = 648-322+46 = 372
MANIFEST_SF06 = {
    "name": "sf06_miri_luma_handoff",
    "image": os.path.join(OUTPUT_DIR, "color", "style_frames",
                          "LTG_COLOR_sf_miri_luma_handoff.png"),
    "characters": [
        {"char": "miri", "head_cx": 367, "head_cy": 422, "head_r": 42},
        {"char": "luma", "head_cx": 921, "head_cy": 372, "head_r": 46},
    ],
}

# Lineup: 5 characters
# From LTG_TOOL_character_lineup.py:
#   IMG_H=560, HEAD_UNIT=87.5, LEFT_MARGIN=100, CHAR_SPACING=240
#   FG_GROUND_Y=int(560*0.78)=436, BG_GROUND_Y=int(560*0.70)=392
#   FG_SCALE=1.03, BG_SCALE=1.00
#   LUMA_RENDER_H=280, *1.03=288. head_r = 280/(3.2*2) * 1.03 ≈ 45
#   Cosmo: COSMO_H=350, head_r = 350/(4.0*2) ≈ 44
#   Miri: MIRI_H=280, head_r = 280/(3.2*2) ≈ 44
#   Byte body oval: BYTE_H=162*1.03≈167. Not organic face — special handling.
#   Glitch: GLITCH_H=170. Non-humanoid — exempt from face gate.
#
# Character X positions: cosmo=160, miri=400, luma=640, byte=860, glitch=1100
# Head CY = ground_y - char_height + head_r (approx, varies by draw func)
_LINEUP_IMG = os.path.join(OUTPUT_DIR, "characters", "main",
                           "LTG_CHAR_character_lineup.png")
MANIFEST_LINEUP = {
    "name": "character_lineup_v011",
    "image": _LINEUP_IMG,
    "characters": [
        {"char": "cosmo",  "head_cx": 160, "head_cy": 130, "head_r": 44},
        {"char": "miri",   "head_cx": 400, "head_cy": 155, "head_r": 44},
        {"char": "luma",   "head_cx": 640, "head_cy": 195, "head_r": 45},
        {"char": "byte",   "head_cx": 860, "head_cy": 310, "head_r": 38,
         "type": "byte"},
        {"char": "glitch", "head_cx": 1100, "head_cy": 280, "head_r": 35,
         "type": "exempt"},
    ],
}

KNOWN_MANIFESTS = {
    "sf06": MANIFEST_SF06,
    "lineup": MANIFEST_LINEUP,
}


# ── Analysis Functions ───────────────────────────────────────────────────────

def crop_face_region(img, head_cx, head_cy, head_r, margin=0.3):
    """Crop the face region from the image.

    Returns a PIL Image crop of the face area (head circle + margin).
    The face region is the upper 70% of the head circle (forehead to chin),
    plus a small margin for brows.
    """
    m = int(head_r * margin)
    # Face is roughly upper 70% of head circle
    x1 = max(0, head_cx - head_r - m)
    y1 = max(0, head_cy - head_r - m)
    x2 = min(img.width, head_cx + head_r + m)
    y2 = min(img.height, head_cy + int(head_r * 0.7) + m)
    return img.crop((x1, y1, x2, y2))


def analyze_face_organic(face_crop):
    """Analyze an organic character's face crop for legibility.

    Returns dict with:
      eye_contrast: luminance range in eye zone
      feature_count: number of distinct dark features
      min_feature_size: smallest feature dimension in px
      verdict: PASS / WARN / FAIL
      details: list of detail strings
    """
    import numpy as np

    arr = np.array(face_crop.convert("L"))  # grayscale
    h, w = arr.shape
    details = []

    # Eye zone: top 60% of face crop (where eyes and brows live)
    eye_zone = arr[:int(h * 0.6), :]
    if eye_zone.size == 0:
        return {"eye_contrast": 0, "feature_count": 0,
                "min_feature_size": 0, "verdict": "FAIL",
                "details": ["Face crop too small for analysis"]}

    # Eye contrast: difference between darkest and lightest regions
    # Use percentile to avoid outlier single pixels
    dark_val = float(np.percentile(eye_zone, 5))
    light_val = float(np.percentile(eye_zone, 95))
    eye_contrast = light_val - dark_val
    details.append(f"eye_contrast={eye_contrast:.1f} (dark={dark_val:.0f}, light={light_val:.0f})")

    # Feature detection: threshold to find dark features
    # Adaptive threshold based on median luminance
    median_lum = float(np.median(arr))
    threshold = min(DARK_THRESHOLD, median_lum - 20)
    threshold = max(30, threshold)

    binary = (arr < threshold).astype(np.uint8)

    # Connected component analysis (simple flood-fill approach)
    features = _find_connected_components(binary)
    feature_count = len(features)
    details.append(f"feature_count={feature_count} (threshold={threshold:.0f})")

    # Minimum feature size
    min_size = 999
    for (fy, fx, fh, fw) in features:
        min_dim = min(fh, fw)
        if min_dim < min_size:
            min_size = min_dim
    if feature_count == 0:
        min_size = 0
    details.append(f"min_feature_size={min_size}px")

    # Verdict
    verdict = "PASS"
    reasons = []

    if eye_contrast < MIN_EYE_CONTRAST_WARN:
        verdict = "FAIL"
        reasons.append(f"eye_contrast {eye_contrast:.0f} < {MIN_EYE_CONTRAST_WARN}")
    elif eye_contrast < MIN_EYE_CONTRAST_PASS:
        verdict = "WARN"
        reasons.append(f"eye_contrast {eye_contrast:.0f} < {MIN_EYE_CONTRAST_PASS}")

    if feature_count < MIN_FEATURES_WARN:
        verdict = "FAIL"
        reasons.append(f"feature_count {feature_count} < {MIN_FEATURES_WARN}")
    elif feature_count < MIN_FEATURES_PASS:
        if verdict != "FAIL":
            verdict = "WARN"
        reasons.append(f"feature_count {feature_count} < {MIN_FEATURES_PASS}")

    if feature_count > 0 and min_size < MIN_FEATURE_PX:
        # Small features are common from anti-aliased edges and fine detail
        # lines (wrinkles, brow strokes). Only escalate to WARN if feature
        # count is also low (indicating the small features ARE the face).
        if feature_count < MIN_FEATURES_PASS:
            if verdict != "FAIL":
                verdict = "WARN"
            reasons.append(f"min_feature {min_size}px < {MIN_FEATURE_PX}px (low feature count)")
        else:
            details.append(f"NOTE: min_feature {min_size}px < {MIN_FEATURE_PX}px "
                           f"(fine detail; {feature_count} features total — acceptable)")

    if reasons:
        details.append("reasons: " + "; ".join(reasons))

    return {
        "eye_contrast": eye_contrast,
        "feature_count": feature_count,
        "min_feature_size": min_size,
        "verdict": verdict,
        "details": details,
    }


def analyze_face_byte(face_crop):
    """Analyze Byte's face crop for pixel-grid eye legibility.

    Byte uses colored pixel-grid eyes (teal normal + magenta cracked),
    not organic features. Check for presence of teal and magenta clusters.

    Some generators (e.g. lineup) render Byte's cracked right eye as a dark
    iris in white sclera instead of magenta pixel grid. The gate accepts EITHER
    magenta cracked-eye OR dark-pupil-in-sclera as valid L/R differentiation,
    but flags missing magenta as a NOTE (not a gate failure).
    """
    import numpy as np

    arr = np.array(face_crop.convert("RGB"))
    h, w, _ = arr.shape
    details = []

    # Count teal pixels (Byte's normal eye)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    teal_mask = (r < 80) & (g > 150) & (b > 170)
    teal_count = int(np.sum(teal_mask))

    # Count magenta pixels (Byte's cracked eye — canonical spec)
    mag_mask = (r > 180) & (g < 120) & (b > 50) & (b < 160)
    mag_count = int(np.sum(mag_mask))

    # Count white sclera pixels (alternative cracked eye representation)
    white_mask = (r > 220) & (g > 220) & (b > 220)
    white_count = int(np.sum(white_mask))

    # Count dark pupil pixels (alternative right eye)
    dark_mask = (r < 80) & (g < 60) & (b < 50)
    dark_count = int(np.sum(dark_mask))

    details.append(f"teal_px={teal_count}, magenta_px={mag_count}")
    details.append(f"white_sclera_px={white_count}, dark_pupil_px={dark_count}")

    total_px = h * w
    teal_pct = (teal_count / total_px * 100) if total_px > 0 else 0

    # Verdict: need teal eye visible + some form of L/R differentiation
    verdict = "PASS"
    reasons = []

    if teal_count < 3:
        verdict = "FAIL"
        reasons.append(f"teal_px={teal_count} < 3 (normal eye invisible)")
    elif teal_count < 8:
        verdict = "WARN"
        reasons.append(f"teal_px={teal_count} < 8 (normal eye marginal)")

    # L/R differentiation: either magenta cracked eye OR dark-in-white eye
    has_mag_eye = mag_count >= 2
    has_alt_eye = white_count >= 3 and dark_count >= 2

    if not has_mag_eye and not has_alt_eye:
        if verdict != "FAIL":
            verdict = "FAIL"
        reasons.append("no cracked eye detected (neither magenta nor dark-in-sclera)")
    elif not has_mag_eye and has_alt_eye:
        # Alternative representation is OK — just note it
        details.append("NOTE: cracked eye uses dark-pupil-in-sclera (not magenta pixel grid)")

    # Check spatial differentiation between eye regions
    if teal_count >= 3:
        teal_cx = float(np.mean(np.where(teal_mask)[1]))
        # Check against whichever cracked eye representation exists
        if has_mag_eye:
            other_cx = float(np.mean(np.where(mag_mask)[1]))
            label = "magenta"
        elif has_alt_eye:
            other_cx = float(np.mean(np.where(dark_mask)[1]))
            label = "dark_pupil"
        else:
            other_cx = teal_cx
            label = "none"
        if label != "none":
            separation = abs(teal_cx - other_cx)
            details.append(f"eye_separation={separation:.1f}px (teal vs {label})")
            if separation < 3:
                if verdict != "FAIL":
                    verdict = "WARN"
                reasons.append(f"eye_separation {separation:.0f}px < 3px (not differentiated)")

    if reasons:
        details.append("reasons: " + "; ".join(reasons))

    return {
        "teal_count": teal_count,
        "mag_count": mag_count,
        "verdict": verdict,
        "details": details,
    }


def _find_connected_components(binary, min_area=3):
    """Simple connected component analysis on a binary (0/1) numpy array.

    Returns list of (y, x, h, w) bounding boxes for components with area >= min_area.
    Uses scipy if available, otherwise falls back to a simple scan approach.
    """
    import numpy as np

    try:
        from scipy import ndimage
        labeled, num_features = ndimage.label(binary)
        components = []
        for i in range(1, num_features + 1):
            ys, xs = np.where(labeled == i)
            area = len(ys)
            if area >= min_area:
                components.append((int(ys.min()), int(xs.min()),
                                   int(ys.max() - ys.min() + 1),
                                   int(xs.max() - xs.min() + 1)))
        return components
    except ImportError:
        pass

    # Fallback: simple row-based scan (less accurate but works without scipy)
    import numpy as np
    h, w = binary.shape
    visited = np.zeros_like(binary, dtype=bool)
    components = []

    for y in range(h):
        for x in range(w):
            if binary[y, x] and not visited[y, x]:
                # BFS flood fill
                queue = [(y, x)]
                visited[y, x] = True
                min_y, max_y, min_x, max_x = y, y, x, x
                area = 0
                while queue:
                    cy, cx = queue.pop(0)
                    area += 1
                    min_y = min(min_y, cy)
                    max_y = max(max_y, cy)
                    min_x = min(min_x, cx)
                    max_x = max(max_x, cx)
                    for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                        ny, nx = cy+dy, cx+dx
                        if 0 <= ny < h and 0 <= nx < w and binary[ny,nx] and not visited[ny,nx]:
                            visited[ny, nx] = True
                            queue.append((ny, nx))
                if area >= min_area:
                    components.append((min_y, min_x, max_y - min_y + 1, max_x - min_x + 1))

    return components


# ── Main gate function ───────────────────────────────────────────────────────

def run_multi_char_face_gate(image_path, manifest):
    """Run multi-character face gate on an image.

    Args:
        image_path: path to the PNG image
        manifest: dict with "characters" list, each entry having
                  char, head_cx, head_cy, head_r, and optional type

    Returns:
        dict with:
          results: list of per-character result dicts
          overall: "PASS" / "WARN" / "FAIL"
          summary: human-readable summary string
    """
    img = Image.open(image_path).convert("RGB")
    results = []

    for entry in manifest["characters"]:
        char_name = entry["char"]
        head_cx = entry["head_cx"]
        head_cy = entry["head_cy"]
        head_r = entry["head_r"]
        char_type = entry.get("type", "organic")

        # Crop face region
        face_crop = crop_face_region(img, head_cx, head_cy, head_r)

        if char_type == "exempt":
            result = {
                "char": char_name,
                "head_cx": head_cx, "head_cy": head_cy, "head_r": head_r,
                "verdict": "SKIP",
                "details": [f"{char_name}: exempt from face gate (non-humanoid)"],
                "face_crop": face_crop,
            }
        elif char_type == "byte":
            analysis = analyze_face_byte(face_crop)
            result = {
                "char": char_name,
                "head_cx": head_cx, "head_cy": head_cy, "head_r": head_r,
                "verdict": analysis["verdict"],
                "details": analysis["details"],
                "face_crop": face_crop,
            }
        else:
            analysis = analyze_face_organic(face_crop)
            result = {
                "char": char_name,
                "head_cx": head_cx, "head_cy": head_cy, "head_r": head_r,
                "verdict": analysis["verdict"],
                "details": analysis["details"],
                "face_crop": face_crop,
                "eye_contrast": analysis["eye_contrast"],
                "feature_count": analysis["feature_count"],
                "min_feature_size": analysis["min_feature_size"],
            }

        results.append(result)

    # Overall verdict
    verdicts = [r["verdict"] for r in results if r["verdict"] != "SKIP"]
    if "FAIL" in verdicts:
        overall = "FAIL"
    elif "WARN" in verdicts:
        overall = "WARN"
    elif not verdicts:
        overall = "SKIP"
    else:
        overall = "PASS"

    # Summary
    lines = [f"Multi-Char Face Gate: {manifest.get('name', 'custom')} — {overall}"]
    for r in results:
        lines.append(f"  {r['char']:<10s} [{r['verdict']}]  head_r={r['head_r']}px")
        for d in r["details"]:
            lines.append(f"    {d}")

    return {
        "results": results,
        "overall": overall,
        "summary": "\n".join(lines),
    }


def build_diagnostic_png(gate_result, out_path):
    """Build a diagnostic contact sheet showing face crops with gate results.

    Each character gets a panel: face crop (zoomed 3x) + verdict + details.
    Total width <= 1280px.
    """
    results = gate_result["results"]
    n = len(results)

    zoom = 3
    panel_w = 200
    panel_h = 200
    header_h = 40
    label_h = 60

    sheet_w = min(MAX_DIM, n * (panel_w + 8) + 8)
    sheet_h = min(MAX_DIM, header_h + panel_h + label_h + 16)

    sheet = Image.new("RGB", (sheet_w, sheet_h), (18, 18, 26))
    sd = ImageDraw.Draw(sheet)

    # Header
    overall = gate_result["overall"]
    overall_col = PASS_COLOR if overall == "PASS" else (WARN_COLOR if overall == "WARN" else FAIL_COLOR)
    header_txt = f"MULTI-CHAR FACE GATE  [{overall}]  C49"
    sd.text((8, 10), header_txt, fill=overall_col)

    for idx, r in enumerate(results):
        px = 8 + idx * (panel_w + 8)
        py = header_h + 4

        # Draw face crop (zoomed)
        crop = r.get("face_crop")
        if crop:
            zoomed = crop.resize((min(panel_w - 4, crop.width * zoom),
                                  min(panel_h - 20, crop.height * zoom)),
                                 Image.NEAREST)
            # Center in panel
            ox = px + (panel_w - zoomed.width) // 2
            oy = py + (panel_h - 20 - zoomed.height) // 2
            sheet.paste(zoomed, (ox, oy))
            sd = ImageDraw.Draw(sheet)  # refresh after paste

        # Verdict border
        v = r["verdict"]
        v_col = (PASS_COLOR if v == "PASS" else
                 WARN_COLOR if v == "WARN" else
                 FAIL_COLOR if v == "FAIL" else LABEL_COLOR)
        sd.rectangle([px, py, px + panel_w, py + panel_h], outline=v_col, width=2)

        # Label
        label_y = py + panel_h + 4
        sd.text((px + 2, label_y),
                f"{r['char'].upper()} [{v}] r={r['head_r']}px",
                fill=v_col)
        # First detail line
        if r["details"]:
            detail_text = r["details"][0][:30]
            sd.text((px + 2, label_y + 14), detail_text, fill=LABEL_COLOR)

    sheet.thumbnail((MAX_DIM, MAX_DIM), Image.LANCZOS)
    sheet.save(out_path)
    print(f"[multi_char_face_gate] Diagnostic PNG: {out_path} ({sheet.width}x{sheet.height}px)")
    return out_path


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Multi-Character Face Gate — validates face legibility "
                    "for all characters in a multi-character composition."
    )
    parser.add_argument("--manifest", required=True,
                        help="Manifest name (sf06, lineup) or path to custom JSON")
    parser.add_argument("--image", default=None,
                        help="Image path (overrides manifest default)")
    parser.add_argument("--output", default=None,
                        help="Diagnostic PNG output path (optional)")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON to stdout")
    args = parser.parse_args()

    # Load manifest
    if args.manifest in KNOWN_MANIFESTS:
        manifest = KNOWN_MANIFESTS[args.manifest]
    else:
        # Try loading as JSON file
        if not os.path.isfile(args.manifest):
            print(f"[ERROR] Unknown manifest: {args.manifest}", file=sys.stderr)
            print(f"Known manifests: {', '.join(KNOWN_MANIFESTS.keys())}", file=sys.stderr)
            return 2
        with open(args.manifest, "r") as f:
            manifest = json.load(f)

    # Image path
    image_path = args.image or manifest.get("image")
    if not image_path or not os.path.isfile(image_path):
        print(f"[ERROR] Image not found: {image_path}", file=sys.stderr)
        return 2

    # Run gate
    result = run_multi_char_face_gate(image_path, manifest)

    # Console output
    print()
    print(result["summary"])
    print()

    # JSON output
    if args.json:
        json_result = {
            "overall": result["overall"],
            "manifest": manifest.get("name", "custom"),
            "characters": [],
        }
        for r in result["results"]:
            entry = {k: v for k, v in r.items() if k != "face_crop"}
            json_result["characters"].append(entry)
        print(json.dumps(json_result, indent=2))

    # Diagnostic PNG
    if args.output:
        out_path = os.path.abspath(args.output)
    else:
        os.makedirs(PRODUCTION_DIR, exist_ok=True)
        manifest_name = manifest.get("name", "custom")
        out_path = os.path.join(PRODUCTION_DIR,
                                f"LTG_PROD_multi_char_face_gate_{manifest_name}.png")

    build_diagnostic_png(result, out_path)

    # Exit code
    if result["overall"] == "FAIL":
        return 2
    elif result["overall"] == "WARN":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
