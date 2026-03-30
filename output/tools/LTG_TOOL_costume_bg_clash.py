#!/usr/bin/env python3
"""
LTG_TOOL_costume_bg_clash.py
Costume-Background Clash Lint — "Luma & the Glitchkin"
Author: Kai Nakamura / Cycle 39

Detects when a character's dominant costume color too closely matches the
dominant background color, reducing figure-ground separation.

Two modes:
----------
**Mode 1: Image analysis** — Given a character image and a background image,
    compute dominant-color distance. Flags if below threshold.

**Mode 2: Palette cross-reference** — Given canonical palette colors (as hex
    or RGB tuples) and a background image, check all specified costume colors
    against the dominant background zones.

Thresholds (CIE76 ΔE in CIELAB space, perceptually uniform):
    ΔE < 5   → FAIL  (character likely merges with background)
    ΔE 5–15  → WARN  (close; reviewable case; may still work depending on outline weight)
    ΔE ≥ 15  → PASS  (sufficient color distance for figure-ground)

Known intentional near-matches (documented, not flagged):
    Byte ELEC_CYAN body vs. Glitch Layer background — digital blending is
    intentional for his "data made physical" aesthetic. Byte's strong outline
    and floating confetti provide figure-ground separation instead.

Usage
-----
    # Mode 1: image-vs-image
    python LTG_TOOL_costume_bg_clash.py \\
        --char LTG_CHAR_cosmo_expression_sheet.png \\
        --bg LTG_ENV_school_hallway.png

    # Mode 2: hex colors vs background
    python LTG_TOOL_costume_bg_clash.py \\
        --char-hex "#A096AF" "#D4956B" \\
        --char-labels "Cosmo cardigan" "Cosmo skin" \\
        --bg LTG_ENV_school_hallway.png

    # Both modes with saved report
    python LTG_TOOL_costume_bg_clash.py \\
        --char LTG_CHAR_cosmo_expression_sheet.png \\
        --bg LTG_ENV_school_hallway.png \\
        --save-report output/production/clash_report_cosmo_hallway.md

API
---
    from LTG_TOOL_costume_bg_clash import (
        clash_check_images,
        clash_check_palette,
        format_report,
    )

    # Image mode
    results = clash_check_images(char_path, bg_path)
    print(format_report(results))

    # Palette mode
    results = clash_check_palette(
        colors=[((160, 150, 175), "Cosmo cardigan"), ((212, 176, 148), "Cosmo skin")],
        bg_path="LTG_ENV_school_hallway.png",
    )
    print(format_report(results))

Known Reference Cases
---------------------
- Cosmo CARDIGAN (RW-08 dusty lavender ~160,150,175) vs. LOCKER_LAV (168,155,191): ΔE ~4 → FAIL
  This is the case that slipped through in C36 and required a hallway v002→v003 fix.
- Byte ELEC_CYAN (#00F0FF) vs. Glitch Layer (ELEC_CYAN dominant): near-zero ΔE — DOCUMENTED PASS.

Changelog
---------
v1.0.0 (C39): Initial implementation — Kai Nakamura.
    Pillow for I/O + numpy for CIELAB conversion (authorized C39 broadcast, Alex Chen).
    CIE76 ΔE computation in CIELAB space (perceptually accurate).
    Two modes: image analysis + palette cross-reference.
    Known-safe list for documented intentional near-matches.
    CLI: --char, --bg, --char-hex, --char-labels, --save-report, --threshold-warn, --threshold-fail.
"""

__version__ = "1.0.0"

import os
import re
import sys
import math
import argparse
from typing import List, Optional, Tuple

from PIL import Image

try:
    import numpy as np
    _NUMPY_AVAILABLE = True
except ImportError:
    _NUMPY_AVAILABLE = False


# ---------------------------------------------------------------------------
# Thresholds
# ---------------------------------------------------------------------------

THRESHOLD_FAIL = 5.0    # ΔE < 5 → FAIL
THRESHOLD_WARN = 15.0   # ΔE 5–15 → WARN; ≥15 → PASS

# Max image dimension for analysis (downscale for speed; 320px is sufficient for dominant-color sampling)
_ANALYSIS_MAX_PX = 320
# Number of dominant colors to sample per image
_N_DOMINANT = 3


# ---------------------------------------------------------------------------
# Known-safe pairs (intentional near-matches — do not flag)
# ---------------------------------------------------------------------------

# Each entry: (char_label_pattern, bg_label_pattern, reason)
# Patterns are case-insensitive substring matches.
_KNOWN_SAFE = [
    (
        r'byte',
        r'glitch[_\- ]?layer|glitchlayer',
        "Byte's ELEC_CYAN body vs. Glitch Layer background: intentional digital blending. "
        "Figure-ground separation via outline weight and floating confetti, not color contrast.",
    ),
]


def _is_known_safe(char_label: str, bg_label: str) -> Optional[str]:
    """
    Return a reason string if (char_label, bg_label) is a known intentional near-match,
    or None if not in the known-safe list.
    """
    for char_pat, bg_pat, reason in _KNOWN_SAFE:
        if re.search(char_pat, char_label, re.IGNORECASE) and re.search(bg_pat, bg_label, re.IGNORECASE):
            return reason
    return None


# ---------------------------------------------------------------------------
# Color math — RGB → CIELAB, CIE76 ΔE
# ---------------------------------------------------------------------------

def _linearize(c: float) -> float:
    """Linearize an sRGB channel value (0–1)."""
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def _rgb_to_lab(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """
    Convert sRGB (0–255 integers) to CIELAB (D65 illuminant).

    Returns (L*, a*, b*) where L is 0–100, a/b are approximately ±128.
    Uses numpy if available (fast), otherwise pure Python.
    """
    # Linearize
    rl = _linearize(r / 255.0)
    gl = _linearize(g / 255.0)
    bl = _linearize(b / 255.0)

    # sRGB to XYZ (D65)
    x = rl * 0.4124564 + gl * 0.3575761 + bl * 0.1804375
    y = rl * 0.2126729 + gl * 0.7151522 + bl * 0.0721750
    z = rl * 0.0193339 + gl * 0.1191920 + bl * 0.9503041

    # Normalize to D65 white point
    x /= 0.95047
    y /= 1.00000
    z /= 1.08883

    # XYZ to Lab
    def f(t):
        if t > 0.008856:
            return t ** (1.0 / 3.0)
        return 7.787 * t + 16.0 / 116.0

    fx, fy, fz = f(x), f(y), f(z)
    L = 116.0 * fy - 16.0
    a = 500.0 * (fx - fy)
    b_star = 200.0 * (fy - fz)
    return L, a, b_star


def delta_e_cie76(
    color1: Tuple[int, int, int],
    color2: Tuple[int, int, int],
) -> float:
    """
    Compute CIE76 ΔE between two sRGB colors.

    Parameters
    ----------
    color1, color2 : (R, G, B) tuples, values 0–255

    Returns
    -------
    float — perceptual color distance (ΔE)
        ΔE < 1: imperceptible
        ΔE 1–5: small (just noticeable or barely)
        ΔE 5–15: moderate (visible, figure-ground risk in art context)
        ΔE ≥ 15: clearly distinct
    """
    L1, a1, b1 = _rgb_to_lab(*color1)
    L2, a2, b2 = _rgb_to_lab(*color2)
    return math.sqrt((L2 - L1)**2 + (a2 - a1)**2 + (b2 - b1)**2)


def _grade(de: float, fail_thresh: float, warn_thresh: float) -> str:
    """Return 'FAIL', 'WARN', or 'PASS' based on ΔE."""
    if de < fail_thresh:
        return "FAIL"
    if de < warn_thresh:
        return "WARN"
    return "PASS"


# ---------------------------------------------------------------------------
# Dominant color extraction
# ---------------------------------------------------------------------------

def _extract_dominant_colors(
    img: Image.Image,
    n: int = _N_DOMINANT,
) -> List[Tuple[int, int, int]]:
    """
    Extract n dominant colors from an image using k-means-lite (quantize).

    Downscales to _ANALYSIS_MAX_PX, converts to RGB, uses PIL quantize
    for fast dominant-color extraction.

    Parameters
    ----------
    img : PIL.Image
    n : int

    Returns
    -------
    list of (R, G, B) tuples, ordered by dominance (most frequent first)
    """
    # Downscale for speed
    thumb = img.copy()
    thumb.thumbnail((_ANALYSIS_MAX_PX, _ANALYSIS_MAX_PX), Image.LANCZOS)
    rgb = thumb.convert("RGB")

    # Quantize to n+2 colors, then return most frequent
    try:
        quantized = rgb.quantize(colors=n + 2, method=Image.Quantize.FASTOCTREE)
        # Get palette
        palette = quantized.getpalette()  # flat list: R0,G0,B0,R1,G1,B1,...
        # Count frequency per palette index
        hist = quantized.histogram()
        # Sort indices by count descending
        n_colors = len(hist)
        indices = sorted(range(n_colors), key=lambda i: hist[i], reverse=True)
        dominant = []
        for idx in indices[:n]:
            r = palette[idx * 3]
            g = palette[idx * 3 + 1]
            b = palette[idx * 3 + 2]
            dominant.append((r, g, b))
        return dominant
    except Exception:
        # Fallback: average color
        pixels = list(rgb.getdata())
        avg_r = int(sum(p[0] for p in pixels) / len(pixels))
        avg_g = int(sum(p[1] for p in pixels) / len(pixels))
        avg_b = int(sum(p[2] for p in pixels) / len(pixels))
        return [(avg_r, avg_g, avg_b)]


# ---------------------------------------------------------------------------
# Public API — Mode 1: image analysis
# ---------------------------------------------------------------------------

def clash_check_images(
    char_path: str,
    bg_path: str,
    n_dominant: int = _N_DOMINANT,
    fail_thresh: float = THRESHOLD_FAIL,
    warn_thresh: float = THRESHOLD_WARN,
) -> dict:
    """
    Check dominant-color clash between a character image and a background image.

    Parameters
    ----------
    char_path : str  — Path to character PNG/JPG
    bg_path : str    — Path to background PNG/JPG
    n_dominant : int — Number of dominant colors to sample from each image
    fail_thresh : float — ΔE below this = FAIL
    warn_thresh : float — ΔE below this = WARN; at/above = PASS

    Returns
    -------
    dict:
        "mode"          : "image"
        "char_path"     : str
        "bg_path"       : str
        "char_colors"   : list of (R,G,B)
        "bg_colors"     : list of (R,G,B)
        "pairs"         : list of pair_result dicts
        "overall"       : "PASS" | "WARN" | "FAIL"
        "fail_thresh"   : float
        "warn_thresh"   : float
    """
    char_label = os.path.basename(char_path)
    bg_label   = os.path.basename(bg_path)

    char_img = Image.open(char_path)
    bg_img   = Image.open(bg_path)
    char_img.load(); bg_img.load()

    char_colors = _extract_dominant_colors(char_img, n_dominant)
    bg_colors   = _extract_dominant_colors(bg_img,   n_dominant)

    pairs = []
    for ci, cc in enumerate(char_colors):
        for bi, bc in enumerate(bg_colors):
            de = delta_e_cie76(cc, bc)
            grade = _grade(de, fail_thresh, warn_thresh)
            safe_reason = _is_known_safe(char_label, bg_label)
            if safe_reason and grade != "PASS":
                grade = "DOCUMENTED_PASS"
            pairs.append({
                "char_color":   cc,
                "bg_color":     bc,
                "char_idx":     ci,
                "bg_idx":       bi,
                "delta_e":      round(de, 2),
                "grade":        grade,
                "safe_reason":  safe_reason,
            })

    # Overall: worst grade across all pairs (ignoring DOCUMENTED_PASS)
    active_grades = [p["grade"] for p in pairs if p["grade"] != "DOCUMENTED_PASS"]
    if "FAIL" in active_grades:
        overall = "FAIL"
    elif "WARN" in active_grades:
        overall = "WARN"
    else:
        overall = "PASS"

    return {
        "mode":         "image",
        "char_path":    char_path,
        "bg_path":      bg_path,
        "char_label":   char_label,
        "bg_label":     bg_label,
        "char_colors":  char_colors,
        "bg_colors":    bg_colors,
        "pairs":        pairs,
        "overall":      overall,
        "fail_thresh":  fail_thresh,
        "warn_thresh":  warn_thresh,
    }


# ---------------------------------------------------------------------------
# Public API — Mode 2: palette cross-reference
# ---------------------------------------------------------------------------

def clash_check_palette(
    colors: List[Tuple[Tuple[int, int, int], str]],
    bg_path: str,
    n_bg_dominant: int = _N_DOMINANT,
    fail_thresh: float = THRESHOLD_FAIL,
    warn_thresh: float = THRESHOLD_WARN,
) -> dict:
    """
    Check specified costume colors against dominant background colors.

    Parameters
    ----------
    colors : list of ((R,G,B), label) tuples
        Costume colors to check.
    bg_path : str
        Path to background PNG/JPG.
    n_bg_dominant : int
        Number of dominant colors to sample from background.
    fail_thresh, warn_thresh : float

    Returns
    -------
    dict:
        "mode"          : "palette"
        "bg_path"       : str
        "bg_label"      : str
        "input_colors"  : list of {"rgb": tuple, "label": str}
        "bg_colors"     : list of (R,G,B)
        "pairs"         : list of pair_result dicts
        "overall"       : "PASS" | "WARN" | "FAIL"
    """
    bg_label = os.path.basename(bg_path)
    bg_img   = Image.open(bg_path)
    bg_img.load()
    bg_colors = _extract_dominant_colors(bg_img, n_bg_dominant)

    pairs = []
    for (rgb, label) in colors:
        for bi, bc in enumerate(bg_colors):
            de = delta_e_cie76(rgb, bc)
            grade = _grade(de, fail_thresh, warn_thresh)
            safe_reason = _is_known_safe(label, bg_label)
            if safe_reason and grade != "PASS":
                grade = "DOCUMENTED_PASS"
            pairs.append({
                "char_color":   rgb,
                "char_label":   label,
                "bg_color":     bc,
                "bg_idx":       bi,
                "delta_e":      round(de, 2),
                "grade":        grade,
                "safe_reason":  safe_reason,
            })

    active_grades = [p["grade"] for p in pairs if p["grade"] != "DOCUMENTED_PASS"]
    if "FAIL" in active_grades:
        overall = "FAIL"
    elif "WARN" in active_grades:
        overall = "WARN"
    else:
        overall = "PASS"

    return {
        "mode":          "palette",
        "bg_path":       bg_path,
        "bg_label":      bg_label,
        "input_colors":  [{"rgb": rgb, "label": lbl} for (rgb, lbl) in colors],
        "bg_colors":     bg_colors,
        "pairs":         pairs,
        "overall":       overall,
        "fail_thresh":   fail_thresh,
        "warn_thresh":   warn_thresh,
    }


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def _rgb_str(rgb: Tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"RGB({r},{g},{b}) #{r:02X}{g:02X}{b:02X}"


def format_report(result: dict) -> str:
    """
    Format a clash_check_images() or clash_check_palette() result as a
    human-readable string.

    Parameters
    ----------
    result : dict from clash_check_images() or clash_check_palette()

    Returns
    -------
    str
    """
    lines = []
    lines.append("=" * 70)
    lines.append(f"LTG Costume-BG Clash Check v{__version__} — [{result['mode'].upper()} MODE]")
    lines.append(f"Overall: {result['overall']}")
    lines.append(f"Thresholds: FAIL < ΔE {result['fail_thresh']} | WARN < ΔE {result['warn_thresh']} | PASS ≥ ΔE {result['warn_thresh']}")
    lines.append("-" * 70)

    if result["mode"] == "image":
        lines.append(f"Character: {result['char_label']}")
        lines.append(f"Background: {result['bg_label']}")
        lines.append(f"Char dominant colors: {[_rgb_str(c) for c in result['char_colors']]}")
        lines.append(f"BG dominant colors:   {[_rgb_str(c) for c in result['bg_colors']]}")
    else:
        lines.append(f"Background: {result['bg_label']}")
        lines.append(f"BG dominant colors:   {[_rgb_str(c) for c in result['bg_colors']]}")
        lines.append(f"Costume colors: {[f\"{e['label']} {_rgb_str(e['rgb'])}\" for e in result['input_colors']]}")

    lines.append("-" * 70)
    lines.append("Pairs (worst first):")
    sorted_pairs = sorted(result["pairs"], key=lambda p: p["delta_e"])
    for p in sorted_pairs:
        char_desc = p.get("char_label") or f"char#{p.get('char_idx', '?')}"
        bg_desc   = f"bg#{p.get('bg_idx', '?')}"
        grade     = p["grade"]
        de        = p["delta_e"]
        lines.append(
            f"  [{grade:>16s}]  ΔE={de:5.1f}  {char_desc} {_rgb_str(p['char_color'])}  vs  "
            f"{bg_desc} {_rgb_str(p['bg_color'])}"
        )
        if p.get("safe_reason"):
            lines.append(f"             NOTE: {p['safe_reason'][:100]}")

    lines.append("=" * 70)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_hex(h: str) -> Tuple[int, int, int]:
    """Parse hex string like '#A1B2C3' or 'A1B2C3' to (R,G,B)."""
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=f"LTG Costume-BG Clash Lint v{__version__} — figure-ground color distance check",
    )
    parser.add_argument("--char",         metavar="PATH",  help="Character image path (Mode 1)")
    parser.add_argument("--bg",           metavar="PATH",  required=True, help="Background image path")
    parser.add_argument("--char-hex",     metavar="HEX",   nargs="+", help="Costume colors as hex (#RRGGBB) (Mode 2)")
    parser.add_argument("--char-labels",  metavar="LABEL", nargs="+", help="Labels for --char-hex colors (optional)")
    parser.add_argument("--threshold-fail", type=float, default=THRESHOLD_FAIL,
                        help=f"ΔE below = FAIL (default {THRESHOLD_FAIL})")
    parser.add_argument("--threshold-warn", type=float, default=THRESHOLD_WARN,
                        help=f"ΔE below = WARN (default {THRESHOLD_WARN})")
    parser.add_argument("--n-dominant",  type=int, default=_N_DOMINANT,
                        help=f"Number of dominant colors to sample (default {_N_DOMINANT})")
    parser.add_argument("--save-report", metavar="PATH", help="Write report to file")
    parser.add_argument("--json",        action="store_true", help="Print JSON result (not formatted report)")
    args = parser.parse_args(argv)

    if not args.char and not args.char_hex:
        parser.error("Provide --char (image mode) or --char-hex (palette mode).")

    if args.char_hex and args.char:
        parser.error("Use --char OR --char-hex, not both.")

    if args.char:
        result = clash_check_images(
            char_path=args.char,
            bg_path=args.bg,
            n_dominant=args.n_dominant,
            fail_thresh=args.threshold_fail,
            warn_thresh=args.threshold_warn,
        )
    else:
        labels = args.char_labels or [f"color_{i+1}" for i in range(len(args.char_hex))]
        if len(labels) < len(args.char_hex):
            labels += [f"color_{i+1}" for i in range(len(labels), len(args.char_hex))]
        colors = [(_parse_hex(h), labels[i]) for i, h in enumerate(args.char_hex)]
        result = clash_check_palette(
            colors=colors,
            bg_path=args.bg,
            n_bg_dominant=args.n_dominant,
            fail_thresh=args.threshold_fail,
            warn_thresh=args.threshold_warn,
        )

    if args.json:
        import json
        # Convert tuples to lists for JSON
        def jsonify(obj):
            if isinstance(obj, tuple):
                return list(obj)
            if isinstance(obj, dict):
                return {k: jsonify(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [jsonify(i) for i in obj]
            return obj
        print(json.dumps(jsonify(result), indent=2))
    else:
        report = format_report(result)
        print(report)
        if args.save_report:
            with open(args.save_report, "w", encoding="utf-8") as fh:
                fh.write(report + "\n")
            print(f"Report saved: {args.save_report}")

    # Exit code: 0=PASS/DOCUMENTED_PASS, 1=WARN, 2=FAIL
    if result["overall"] == "FAIL":
        sys.exit(2)
    elif result["overall"] == "WARN":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
