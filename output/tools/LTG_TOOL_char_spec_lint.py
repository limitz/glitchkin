# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_char_spec_lint.py
General Character Spec Linter — "Luma & the Glitchkin"
Author: Kai Nakamura / Cycle 34

Validates character generator Python source code against canonical character
spec files (output/characters/main/*.md and supporting/*.md).

Checks performed per character
-------------------------------
Shared checks (all characters):
  C001  Head-to-body ratio constant present and within ±10% of spec
  C002  Eye-width formula uses correct coefficient (within ±15% of spec)
  C003  Canonical palette colors present (spot-check key body colors)

Character-specific checks:
  Luma:
    L001  Head-to-body ratio == 3.2 (±10%) — total height 3.2 heads
    L002  Eye-width = HR * 0.22 (±15%) — head-radius × 0.22
    L003  Hoodie color present: HOODIE ~ #E8722A (Warm Orange) ± broad tolerance
    L004  Hair curl count: exactly 5 curl indicators in hair-drawing code
    L005  Pixel-pattern colors present: PX_CYAN (#00F0FF) and PX_MAG (#FF2D6B)

  Cosmo:
    S001  Head-to-body ratio == 4.0 (±10%)
    S002  Eye-width = HR * 0.18 (±15%) — cosmo spec: ~0.18x head width
    S003  Glasses tilt neutral == 7 degrees (±2 degrees)
    S004  Frame thickness = 0.06x head unit (within ±25%)
    S005  Notebook color present: NOTEBOOK ~ #5B8DB8 (Cerulean Blue) ± tolerance

  Miri:
    M001  Head-to-body ratio == 3.2 (±10%)
    M002  Eye-width = HR * 0.16 (±20%) — miri spec: ~0.16x head width
    M003  Permanent blush color present: BLUSH_PERM ~ #D4956B ± tolerance
    M004  Chopstick/bun hair indicator present in code
    M005  Crow's feet drawing indicator present (aging detail)

  Byte (C39 addition — Kai Nakamura):
    B001  Body oval wider than tall (bw ≥ bh or oval_w ≥ oval_h) — spec 1.0:0.85 W:H
    B002  Body color present: BYTE_TEAL/BYTE_BODY ~ #00D4E8 (GL-01b Byte Teal) ± tolerance
    B003  Hot Magenta cracked-eye crack indicator present (HOT_MAG / HOT_MAGENTA)
    B004  Pixel confetti (floating mechanism) indicator present in code
    B005  Eye pixel grid is 5×5 (pixel_size, PIXEL_SIZE, grid dim 5 near eye-drawing code)

Results: per-character PASS / WARN / FAIL report.
  FAIL  = canonical constant present but value violates spec
  WARN  = check could not be confirmed (constant absent or ambiguous)
  PASS  = check confirmed

Usage (standalone):
    python LTG_TOOL_char_spec_lint.py
    python LTG_TOOL_char_spec_lint.py --char luma
    python LTG_TOOL_char_spec_lint.py --char cosmo --char miri
    python LTG_TOOL_char_spec_lint.py --char byte
    python LTG_TOOL_char_spec_lint.py --save-report PATH

Changelog
---------
v1.1.0 (C39): Byte checks added (B001–B005) — Kai Nakamura.
    B001 body oval W:H ratio (wider than tall).
    B002 body color #00D4E8 Byte Teal (GL-01b).
    B003 Hot Magenta crack indicator.
    B004 pixel confetti floating mechanism.
    B005 5×5 pixel eye grid.
    Byte added to _CHAR_REGISTRY with generator patterns.
v1.0.0 (C34): Initial implementation — Luma/Cosmo/Miri checks.

API:
    from LTG_TOOL_char_spec_lint import lint_character, lint_all, format_report

    results = lint_all("/path/to/output/tools")
    print(format_report(results))
"""

__version__ = "1.1.0"  # C39: Byte checks added (B001–B005) — Kai Nakamura

import os
import re
import sys
import glob as _glob
from typing import Optional

# ── Spec definitions ──────────────────────────────────────────────────────────

# Each spec entry:
#   "char"      : short name used in CLI / results
#   "generators": list of glob patterns to find this character's generators
#   "checks"    : list of check dicts

# Tolerances
HEAD_RATIO_TOL = 0.10    # ±10% on head-to-body ratio
EYE_COEFF_TOL  = 0.15    # ±15% on eye-width coefficient
COLOR_TOL      = 50      # Manhattan distance on RGB (lenient palette check)


# ── Color helpers ─────────────────────────────────────────────────────────────

def _hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _color_distance(a, b):
    """Manhattan RGB distance."""
    return sum(abs(x - y) for x, y in zip(a, b))


def _rgb_tuple_re(r, g, b, tol=COLOR_TOL):
    """Build a regex that matches an RGB tuple within tol of (r,g,b)."""
    # We'll scan for literal tuples in source; we do a numeric extraction approach
    return re.compile(
        r'\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)'
    )


# ── Source scanning helpers ───────────────────────────────────────────────────

def _read_source(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read(), f.readlines() if False else None
    except OSError as e:
        return None, str(e)


def _read_lines(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return f.readlines(), None
    except OSError as e:
        return None, str(e)


def _extract_numeric_constant(source, names):
    """
    Try to find `NAME = <number>` for any of the given constant names.
    Returns (name_found, float_value) or (None, None).
    """
    for name in names:
        pattern = re.compile(
            r'\b' + re.escape(name) + r'\s*=\s*([0-9]+(?:\.[0-9]+)?)',
            re.IGNORECASE,
        )
        m = pattern.search(source)
        if m:
            return name, float(m.group(1))
    return None, None


def _extract_rgb_constant(source, names):
    """
    Try to find `NAME = (r, g, b)` for any of the given constant names.
    Returns (name_found, (r,g,b)) or (None, None).
    """
    for name in names:
        pattern = re.compile(
            r'\b' + re.escape(name) + r'\s*=\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)',
        )
        m = pattern.search(source)
        if m:
            return name, (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None, None


def _find_float_near_keyword(source, keyword, coeff_target, tol=0.15, context=120):
    """
    Near *keyword* (within *context* chars), look for a float like 0.22 close to coeff_target.
    Returns (found_value, pass) or (None, False).
    """
    positions = [m.start() for m in re.finditer(re.escape(keyword), source, re.IGNORECASE)]
    for pos in positions:
        snippet = source[max(0, pos - context) : pos + context]
        floats = re.findall(r'\b0\.\d+', snippet)
        for f in floats:
            val = float(f)
            if abs(val - coeff_target) / coeff_target <= tol:
                return val, True
    return None, False


def _keyword_present(source, keywords):
    """Return True if any of *keywords* appears in source (case-insensitive)."""
    for kw in keywords:
        if re.search(re.escape(kw), source, re.IGNORECASE):
            return True
    return False


# ── Per-check functions ───────────────────────────────────────────────────────

def _check_head_ratio(source, spec_ratio, tol, char_label, check_code):
    """C001 / L001 / S001 / M001 — head-to-body ratio."""
    issues = []
    # Look for HEAD_R, HR, head_r, HEAD_UNITS, or numeric body height ratio patterns
    # Strategy: find figure_height / head_height style ratio, or direct constants
    # Heuristic: look for ratio constants like 3.2, 4.0 near "head" keyword
    ratio_re = re.compile(r'\b(3\.[0-9]+|4\.[0-9]+)\b')
    spec_str = str(spec_ratio)
    if spec_str in source or str(spec_ratio).rstrip('0').rstrip('.') in source:
        # Exact spec ratio string present — good sign
        return "PASS", []
    # Look for any ratio-like float
    matches = ratio_re.findall(source)
    close = [float(v) for v in matches if abs(float(v) - spec_ratio) / spec_ratio <= tol]
    if close:
        return "PASS", []
    if matches:
        # Found ratios but none close to spec
        issues.append({
            "code": check_code,
            "result": "FAIL",
            "message": (
                f"{check_code}: Head-to-body ratio: spec={spec_ratio}, "
                f"found candidates {matches[:5]} — none within {int(tol*100)}% of spec."
            ),
        })
        return "FAIL", issues
    # No ratio found at all — WARN
    issues.append({
        "code": check_code,
        "result": "WARN",
        "message": (
            f"{check_code}: Head-to-body ratio {spec_ratio} not confirmed. "
            f"No ratio-like constant near spec value found."
        ),
    })
    return "WARN", issues


def _check_eye_coeff(source, spec_coeff, tol, check_code):
    """L002 / S002 / M002 — eye-width coefficient."""
    issues = []
    found_val, found = _find_float_near_keyword(source, 'HR', spec_coeff, tol, context=160)
    if not found:
        found_val, found = _find_float_near_keyword(source, 'head_r', spec_coeff, tol, context=160)
    if not found:
        found_val, found = _find_float_near_keyword(source, 'HEAD_R', spec_coeff, tol, context=160)
    if found:
        return "PASS", []
    # Maybe the ew= assignment uses the literal coefficient
    ew_re = re.compile(r'\bew\s*=\s*int\s*\([A-Za-z_]+\s*\*\s*(0\.\d+)\s*\)')
    m = ew_re.search(source)
    if m:
        val = float(m.group(1))
        if abs(val - spec_coeff) / spec_coeff <= tol:
            return "PASS", []
        else:
            issues.append({
                "code": check_code,
                "result": "FAIL",
                "message": (
                    f"{check_code}: Eye-width coefficient: spec={spec_coeff}, "
                    f"found ew=int(HR*{val}) — deviation "
                    f"{abs(val-spec_coeff)/spec_coeff*100:.1f}% (limit {int(tol*100)}%)."
                ),
            })
            return "FAIL", issues
    # Not found — WARN
    issues.append({
        "code": check_code,
        "result": "WARN",
        "message": (
            f"{check_code}: Eye-width coefficient {spec_coeff} not confirmed in source. "
            f"Check that `ew = int(HR * {spec_coeff})` pattern is present."
        ),
    })
    return "WARN", issues


def _check_rgb_color(source, spec_hex, constant_names, check_code, label, tol=COLOR_TOL):
    """C003 / palette check — canonical RGB color present."""
    issues = []
    spec_rgb = _hex_to_rgb(spec_hex)
    found_name, found_rgb = _extract_rgb_constant(source, constant_names)
    if found_rgb is not None:
        dist = _color_distance(found_rgb, spec_rgb)
        if dist <= tol:
            return "PASS", []
        else:
            issues.append({
                "code": check_code,
                "result": "FAIL",
                "message": (
                    f"{check_code}: {label}: constant {found_name}={found_rgb} "
                    f"is {dist} Manhattan distance from spec {spec_rgb} ({spec_hex}). "
                    f"Limit={tol}."
                ),
            })
            return "FAIL", issues
    # Try scanning all RGB tuples in source for proximity
    all_tuples = re.findall(r'\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', source)
    close = [t for t in all_tuples
             if _color_distance((int(t[0]), int(t[1]), int(t[2])), spec_rgb) <= tol]
    if close:
        return "PASS", []
    # Not found
    issues.append({
        "code": check_code,
        "result": "WARN",
        "message": (
            f"{check_code}: {label}: canonical color {spec_hex} ({spec_rgb}) "
            f"not found in source (checked names {constant_names}, scanned all tuples). "
            f"Tolerance={tol}."
        ),
    })
    return "WARN", issues


def _check_keyword_present(source, keywords, check_code, label):
    """Generic keyword presence check — returns PASS or WARN."""
    issues = []
    if _keyword_present(source, keywords):
        return "PASS", []
    issues.append({
        "code": check_code,
        "result": "WARN",
        "message": (
            f"{check_code}: {label}: expected keyword(s) {keywords} not found in source."
        ),
    })
    return "WARN", issues


def _check_luma_curl_count(source, check_code):
    """L004 — exactly 5 curl indicators in hair drawing code."""
    issues = []
    # Look for curl_count=5, NUM_CURLS=5, range(5), or exactly 5 ellipse calls in hair section
    # Strategy: find constants like CURL_COUNT, NUM_CURLS = 5, or range(5) near "curl"/"hair"
    direct = re.search(r'\b(CURL_COUNT|NUM_CURLS|curl_count|num_curls)\s*=\s*5\b', source)
    if direct:
        return "PASS", []
    # Look for range(5) near hair or curl context
    hair_section = re.search(
        r'(def draw.*hair|# hair|# curl|HAIR_CURL)',
        source, re.IGNORECASE,
    )
    if hair_section:
        snippet = source[hair_section.start(): hair_section.start() + 800]
        if re.search(r'\brange\s*\(\s*5\s*\)', snippet):
            return "PASS", []
        # Count ellipse calls in snippet
        ellipse_calls = len(re.findall(r'draw\.ellipse', snippet))
        if 4 <= ellipse_calls <= 7:
            # Ambiguous but plausible; count as PASS with note
            return "PASS", []
    # Check for literal `5` near "curl" or "spiral"
    if re.search(r'\b5\b.*\b(curl|spiral|ringlet)\b|\b(curl|spiral|ringlet)\b.*\b5\b',
                 source, re.IGNORECASE):
        return "PASS", []
    issues.append({
        "code": check_code,
        "result": "WARN",
        "message": (
            f"{check_code}: Luma curl count: spec requires exactly 5 curls. "
            f"No clear CURL_COUNT=5 constant or range(5) in hair context found. "
            f"Verify hair generator uses exactly 5 curl indicators."
        ),
    })
    return "WARN", issues


def _check_cosmo_glasses_tilt(source, check_code):
    """S003 — glasses tilt neutral = 7 degrees (±2)."""
    issues = []
    # Look for glasses_tilt=7 in EXPRESSIONS list or NEUTRAL_TILT=7 constant
    tilt_re = re.compile(r"glasses_tilt['\"]?\s*:\s*(\d+)")
    matches = tilt_re.findall(source)
    neutral_found = None
    if matches:
        # First match is often the NEUTRAL expression
        first_val = int(matches[0])
        if abs(first_val - 7) <= 2:
            return "PASS", []
        neutral_found = first_val
    # Check for direct constant
    m = re.search(r'\b(NEUTRAL_TILT|GLASSES_TILT|tilt_neutral)\s*=\s*(\d+)', source)
    if m:
        val = int(m.group(2))
        if abs(val - 7) <= 2:
            return "PASS", []
        neutral_found = val
    if neutral_found is not None:
        issues.append({
            "code": check_code,
            "result": "FAIL",
            "message": (
                f"{check_code}: Cosmo glasses tilt: spec=7°±2, found neutral={neutral_found}°."
            ),
        })
        return "FAIL", issues
    issues.append({
        "code": check_code,
        "result": "WARN",
        "message": (
            f"{check_code}: Cosmo glasses tilt neutral=7° not confirmed. "
            f"Add `glasses_tilt: 7` in the NEUTRAL expression definition."
        ),
    })
    return "WARN", issues


def _check_cosmo_frame_thickness(source, check_code):
    """S004 — frame thickness = 0.06x head unit (±25%)."""
    issues = []
    spec = 0.06
    tol  = 0.25
    found_val, found = _find_float_near_keyword(
        source, 'frame_w', spec, tol, context=200,
    )
    if not found:
        found_val, found = _find_float_near_keyword(
            source, 'FRAME_W', spec, tol, context=200,
        )
    if not found:
        # Look for `int(hu * 0.06)` or `int(HEAD_R * 0.06)` pattern
        m = re.search(r'int\s*\(\s*[a-zA-Z_]+\s*\*\s*(0\.\d+)\s*\)', source)
        if m:
            val = float(m.group(1))
            if abs(val - spec) / spec <= tol:
                return "PASS", []
            # If the found val is way off, it might be something else — just warn
    if found:
        return "PASS", []
    # frame_w = max(3, int(hu * X)) pattern
    m = re.search(
        r'frame_w\s*=\s*max\s*\(\s*\d+\s*,\s*int\s*\(\s*[a-z_]+\s*\*\s*(0\.\d+)\s*\)\s*\)',
        source,
    )
    if m:
        val = float(m.group(1))
        if abs(val - spec) / spec <= tol:
            return "PASS", []
        issues.append({
            "code": check_code,
            "result": "FAIL",
            "message": (
                f"{check_code}: Cosmo frame thickness: spec=0.06×hu, found={val}×hu "
                f"(deviation {abs(val-spec)/spec*100:.1f}%, limit {int(tol*100)}%)."
            ),
        })
        return "FAIL", issues
    issues.append({
        "code": check_code,
        "result": "WARN",
        "message": (
            f"{check_code}: Cosmo frame thickness 0.06×hu not confirmed. "
            f"Expected pattern: `frame_w = max(N, int(hu * 0.06))`."
        ),
    })
    return "WARN", issues


# ── Byte-specific checks ─────────────────────────────────────────────────────

def _check_byte_oval_ratio(source, check_code):
    """
    B001 — Body oval wider than tall (bw >= bh).

    Spec: oval is ~1.0:0.85 (W:H) — wider than tall.
    Failure: if bh > bw explicitly (taller than wide).
    Warn: if no distinguishable bw/bh constants found.
    """
    issues = []
    # Look for bw/bh or body_w/body_h assignments
    bw_re = re.compile(r'\b(bw|body_w|BODY_W|oval_w|OW)\s*=\s*([0-9]+(?:\.[0-9]+)?)')
    bh_re = re.compile(r'\b(bh|body_h|BODY_H|oval_h|OH)\s*=\s*([0-9]+(?:\.[0-9]+)?)')
    bw_matches = [(m.group(1), float(m.group(2))) for m in bw_re.finditer(source)]
    bh_matches = [(m.group(1), float(m.group(2))) for m in bh_re.finditer(source)]

    if bw_matches and bh_matches:
        bw_val = bw_matches[0][1]
        bh_val = bh_matches[0][1]
        if bw_val >= bh_val:
            return "PASS", []
        else:
            issues.append({
                "code": check_code,
                "result": "FAIL",
                "message": (
                    f"{check_code}: Byte oval ratio: spec requires width >= height "
                    f"(~1.0:0.85 W:H). Found bw={bw_val} < bh={bh_val} — taller than wide. "
                    f"Byte's body oval must be wider-than-tall (spec §2, §4)."
                ),
            })
            return "FAIL", issues

    # Also accept: int(bw * 0.85) style height derivation
    if re.search(r'\b(bh|body_h|oval_h)\s*=\s*int\s*\([a-z_]+\s*\*\s*0\.[78]\d\)', source):
        return "PASS", []

    # Not found — WARN
    issues.append({
        "code": check_code,
        "result": "WARN",
        "message": (
            f"{check_code}: Byte oval W:H ratio not confirmed. "
            f"Expected `bw` and `bh` (or body_w/body_h) constants with bw >= bh. "
            f"Spec: oval is ~1.0:0.85 W:H (wider than tall)."
        ),
    })
    return "WARN", issues


def _check_byte_pixel_eye_grid(source, check_code):
    """
    B005 — Byte's eye pixel grid must be 5x5.

    Look for pixel_size=5, PIXEL_SIZE=5, or grid_dim=5 near eye-drawing code.
    Also accept eye_size=5 or a literal `5` near "pixel_eye" or "eye_grid".
    """
    issues = []
    # Direct constant
    if re.search(r'\b(PIXEL_SIZE|pixel_size|GRID_DIM|grid_dim|eye_grid_sz)\s*=\s*5\b', source):
        return "PASS", []
    # 5x5 literal near eye-drawing keywords
    eye_context = re.search(
        r'(draw.*pixel.*eye|pixel.*eye.*draw|eye_grid|5\s*[x×]\s*5)',
        source, re.IGNORECASE,
    )
    if eye_context:
        snippet = source[max(0, eye_context.start() - 200): eye_context.start() + 400]
        if re.search(r'\b5\s*,\s*5\b|\b5\s*[x×]\s*5\b|range\s*\(\s*5\s*\)', snippet):
            return "PASS", []
    # Check for range(5) near any pixel or eye drawing section
    pixel_section = re.search(r'(def draw.*eye|# eye|PIXEL|pixel_col)', source, re.IGNORECASE)
    if pixel_section:
        snippet = source[pixel_section.start(): pixel_section.start() + 600]
        if len(re.findall(r'range\s*\(\s*5\s*\)', snippet)) >= 2:
            # Two range(5) loops = 5x5 grid
            return "PASS", []
    issues.append({
        "code": check_code,
        "result": "WARN",
        "message": (
            f"{check_code}: Byte 5x5 pixel-eye grid not confirmed. "
            f"Expected `PIXEL_SIZE = 5` or `range(5)` double-loop near eye-drawing code. "
            f"Spec: 5×5 pixel grid per eye (byte.md §5)."
        ),
    })
    return "WARN", issues


# ── Per-character lint functions ──────────────────────────────────────────────

def _lint_luma(source, filepath):
    results = []
    fname = os.path.basename(filepath)

    # L001 head-to-body ratio 3.2
    r, issues = _check_head_ratio(source, 3.2, HEAD_RATIO_TOL, "Luma", "L001")
    results.append({"check": "L001", "result": r, "issues": issues})

    # L002 eye-width coefficient 0.22
    r, issues = _check_eye_coeff(source, 0.22, EYE_COEFF_TOL, "L002")
    results.append({"check": "L002", "result": r, "issues": issues})

    # L003 hoodie color #E8722A
    r, issues = _check_rgb_color(
        source, "#E8722A", ["HOODIE", "HOODIE_BASE", "hoodie", "hoodie_col"],
        "L003", "Luma hoodie #E8722A", tol=COLOR_TOL,
    )
    results.append({"check": "L003", "result": r, "issues": issues})

    # L004 curl count 5
    r, issues = _check_luma_curl_count(source, "L004")
    results.append({"check": "L004", "result": r, "issues": issues})

    # L005 pixel pattern colors
    r_cyan, issues_cyan = _check_rgb_color(
        source, "#00F0FF", ["PX_CYAN", "PIXEL_CYAN", "LACES", "px_cyan"],
        "L005a", "PX_CYAN #00F0FF", tol=30,
    )
    r_mag, issues_mag = _check_rgb_color(
        source, "#FF2D6B", ["PX_MAG", "PIXEL_MAG", "px_mag"],
        "L005b", "PX_MAG #FF2D6B", tol=30,
    )
    if r_cyan == "PASS" and r_mag == "PASS":
        results.append({"check": "L005", "result": "PASS", "issues": []})
    elif r_cyan == "FAIL" or r_mag == "FAIL":
        all_issues = issues_cyan + issues_mag
        results.append({"check": "L005", "result": "FAIL", "issues": all_issues})
    else:
        all_issues = issues_cyan + issues_mag
        results.append({"check": "L005", "result": "WARN", "issues": all_issues})

    return results


def _lint_cosmo(source, filepath):
    results = []

    # S001 head-to-body ratio 4.0
    r, issues = _check_head_ratio(source, 4.0, HEAD_RATIO_TOL, "Cosmo", "S001")
    results.append({"check": "S001", "result": r, "issues": issues})

    # S002 eye coefficient ~0.18
    r, issues = _check_eye_coeff(source, 0.18, 0.20, "S002")
    results.append({"check": "S002", "result": r, "issues": issues})

    # S003 glasses tilt neutral 7°
    r, issues = _check_cosmo_glasses_tilt(source, "S003")
    results.append({"check": "S003", "result": r, "issues": issues})

    # S004 frame thickness 0.06
    r, issues = _check_cosmo_frame_thickness(source, "S004")
    results.append({"check": "S004", "result": r, "issues": issues})

    # S005 notebook color #5B8DB8
    r, issues = _check_rgb_color(
        source, "#5B8DB8", ["NOTEBOOK", "NOTEBOOK_COL", "notebook"],
        "S005", "Notebook #5B8DB8", tol=COLOR_TOL,
    )
    results.append({"check": "S005", "result": r, "issues": issues})

    return results


def _lint_miri(source, filepath):
    results = []

    # M001 head-to-body ratio 3.2
    r, issues = _check_head_ratio(source, 3.2, HEAD_RATIO_TOL, "Miri", "M001")
    results.append({"check": "M001", "result": r, "issues": issues})

    # M002 eye coefficient ~0.16
    r, issues = _check_eye_coeff(source, 0.16, 0.20, "M002")
    results.append({"check": "M002", "result": r, "issues": issues})

    # M003 permanent blush #D4956B
    r, issues = _check_rgb_color(
        source, "#D4956B", ["BLUSH_PERM", "BLUSH_BASE", "PERM_BLUSH", "blush_perm"],
        "M003", "Perm blush #D4956B", tol=COLOR_TOL,
    )
    results.append({"check": "M003", "result": r, "issues": issues})

    # M004 chopstick / bun hair indicator
    r, issues = _check_keyword_present(
        source,
        ["chopstick", "bun", "CHOPSTICK", "BUN", "chop_stick"],
        "M004",
        "Bun/chopstick hair element",
    )
    results.append({"check": "M004", "result": r, "issues": issues})

    # M005 crow's feet detail
    r, issues = _check_keyword_present(
        source,
        ["crow", "crinkle", "CROW", "smile_line", "smile line", "laugh_line"],
        "M005",
        "Crow's feet / smile-line detail",
    )
    results.append({"check": "M005", "result": r, "issues": issues})

    return results


def _lint_byte(source, filepath):
    """
    Byte-specific spec checks (B001–B005).

    Added C39 (Kai Nakamura). Byte's pixel-eye 5x5 grid and oval-body construction
    have drifted in expression sheet generators — these checks gate against regressions.
    """
    results = []

    # B001 body oval wider than tall
    r, issues = _check_byte_oval_ratio(source, "B001")
    results.append({"check": "B001", "result": r, "issues": issues})

    # B002 body color #00D4E8 (GL-01b Byte Teal)
    r, issues = _check_rgb_color(
        source, "#00D4E8",
        ["BYTE_TEAL", "BYTE_BODY", "BODY_COL", "body_col", "TEAL", "GL01B"],
        "B002", "Byte Teal #00D4E8 (GL-01b)", tol=COLOR_TOL,
    )
    results.append({"check": "B002", "result": r, "issues": issues})

    # B003 Hot Magenta crack indicator
    r, issues = _check_keyword_present(
        source,
        ["HOT_MAG", "HOT_MAGENTA", "hot_mag", "hot_magenta", "CRACK", "crack_line"],
        "B003",
        "Hot Magenta cracked-eye crack indicator",
    )
    results.append({"check": "B003", "result": r, "issues": issues})

    # B004 pixel confetti (floating mechanism)
    r, issues = _check_keyword_present(
        source,
        ["confetti", "CONFETTI", "pixel_sq", "PIXEL_SQ", "float_px", "floating"],
        "B004",
        "Pixel confetti / floating mechanism",
    )
    results.append({"check": "B004", "result": r, "issues": issues})

    # B005 5x5 pixel eye grid
    r, issues = _check_byte_pixel_eye_grid(source, "B005")
    results.append({"check": "B005", "result": r, "issues": issues})

    return results


# ── Character registry ────────────────────────────────────────────────────────

# Maps short name → (generator glob pattern(s), lint function)
_CHAR_REGISTRY = {
    "luma": {
        "patterns": [
            "LTG_TOOL_luma_expression_sheet_v*.py",
            "LTG_TOOL_luma_turnaround_v*.py",
        ],
        "lint_fn": _lint_luma,
        "label": "Luma",
    },
    "cosmo": {
        "patterns": [
            "LTG_TOOL_cosmo_expression_sheet_v*.py",
            "LTG_TOOL_cosmo_turnaround_v*.py",
        ],
        "lint_fn": _lint_cosmo,
        "label": "Cosmo",
    },
    "miri": {
        "patterns": [
            "LTG_TOOL_grandma_miri_expression_sheet_v*.py",
        ],
        "lint_fn": _lint_miri,
        "label": "Grandma Miri",
    },
    "byte": {
        "patterns": [
            "LTG_TOOL_byte_expression_sheet_v*.py",
            "LTG_TOOL_byte_expressions_generator.py",
        ],
        "lint_fn": _lint_byte,
        "label": "Byte",
    },
}


def _resolve_generators(char_name, tools_dir):
    """Return list of matching generator paths for *char_name* in *tools_dir*."""
    cfg = _CHAR_REGISTRY[char_name]
    paths = []
    for pattern in cfg["patterns"]:
        full = os.path.join(tools_dir, pattern)
        found = sorted(_glob.glob(full))
        # Return only the latest version (highest sort order) per pattern
        if found:
            paths.append(found[-1])
    return paths


# ── Public API ────────────────────────────────────────────────────────────────

def lint_character(char_name, tools_dir=None):
    """
    Lint all generator files for *char_name* against the character spec.

    Parameters
    ----------
    char_name : str
        One of "luma", "cosmo", "miri", "byte".
    tools_dir : str | None
        Directory containing LTG_TOOL_*.py files.
        Defaults to the directory containing this script.

    Returns
    -------
    dict:
        "char"      : str — character name
        "label"     : str — display label
        "files"     : list of str — generator paths linted
        "checks"    : list of check result dicts
        "summary"   : dict {"PASS": int, "WARN": int, "FAIL": int}
        "overall"   : "PASS" | "WARN" | "FAIL"
        "error"     : str | None
    """
    if char_name not in _CHAR_REGISTRY:
        return {
            "char": char_name, "label": char_name, "files": [],
            "checks": [], "summary": {}, "overall": "ERROR",
            "error": f"Unknown character '{char_name}'. Use: {list(_CHAR_REGISTRY.keys())}",
        }

    if tools_dir is None:
        tools_dir = os.path.dirname(os.path.abspath(__file__))

    cfg = _CHAR_REGISTRY[char_name]
    paths = _resolve_generators(char_name, tools_dir)

    if not paths:
        return {
            "char": char_name, "label": cfg["label"], "files": [],
            "checks": [], "summary": {"PASS": 0, "WARN": 0, "FAIL": 0},
            "overall": "WARN",
            "error": (
                f"No generator files found for '{char_name}' in {tools_dir}. "
                f"Patterns: {cfg['patterns']}"
            ),
        }

    # Use the most recently modified file (glob returns last version alphabetically)
    # The patterns already return latest by sort; use the first resolved path
    target_path = paths[0]
    source, read_err = _read_source(target_path)
    if source is None:
        return {
            "char": char_name, "label": cfg["label"], "files": [target_path],
            "checks": [], "summary": {"PASS": 0, "WARN": 0, "FAIL": 0},
            "overall": "ERROR",
            "error": f"Could not read {target_path}: {read_err}",
        }

    check_results = cfg["lint_fn"](source, target_path)

    summary = {"PASS": 0, "WARN": 0, "FAIL": 0}
    for cr in check_results:
        summary[cr["result"]] = summary.get(cr["result"], 0) + 1

    if summary.get("FAIL", 0) > 0:
        overall = "FAIL"
    elif summary.get("WARN", 0) > 0:
        overall = "WARN"
    else:
        overall = "PASS"

    return {
        "char": char_name,
        "label": cfg["label"],
        "files": [target_path],
        "checks": check_results,
        "summary": summary,
        "overall": overall,
        "error": None,
    }


def lint_all(tools_dir=None):
    """
    Lint all registered characters.

    Returns list of lint_character() result dicts.
    """
    if tools_dir is None:
        tools_dir = os.path.dirname(os.path.abspath(__file__))
    return [lint_character(name, tools_dir) for name in _CHAR_REGISTRY]


def format_report(results):
    """
    Format a list of lint_character() results as a human-readable string.

    Parameters
    ----------
    results : list of dicts (output of lint_character / lint_all)

    Returns
    -------
    str
    """
    lines_out = []
    total_pass = total_warn = total_fail = 0

    for r in results:
        label = r.get("label", r.get("char", "?"))
        overall = r.get("overall", "ERROR")
        files = r.get("files", [])
        file_str = os.path.basename(files[0]) if files else "(no file)"

        lines_out.append(f"\n{'='*70}")
        lines_out.append(f"{overall:6}  {label}  ({file_str})")
        lines_out.append(f"{'='*70}")

        if r.get("error"):
            lines_out.append(f"  ERROR: {r['error']}")
            continue

        for cr in r.get("checks", []):
            res = cr["result"]
            code = cr["check"]
            if res == "PASS":
                lines_out.append(f"  PASS  [{code}]")
            else:
                for issue in cr.get("issues", []):
                    tag = f"  {res:4}  [{code}] {issue['message']}"
                    lines_out.append(tag)
                if not cr.get("issues"):
                    lines_out.append(f"  {res:4}  [{code}]")

        s = r.get("summary", {})
        lines_out.append(
            f"\n  Summary: {s.get('PASS',0)} PASS / {s.get('WARN',0)} WARN / "
            f"{s.get('FAIL',0)} FAIL  →  {overall}"
        )
        total_pass += s.get("PASS", 0)
        total_warn += s.get("WARN", 0)
        total_fail += s.get("FAIL", 0)

    lines_out.append(f"\n{'='*70}")
    lines_out.append(
        f"TOTAL: {total_pass} PASS / {total_warn} WARN / {total_fail} FAIL "
        f"across {len(results)} character(s)"
    )
    return "\n".join(lines_out)


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="LTG Character Spec Linter v{} — validates generators against spec".format(
            __version__
        )
    )
    parser.add_argument(
        "--char", action="append", dest="chars",
        choices=list(_CHAR_REGISTRY.keys()),
        help="Character(s) to lint (default: all)",
    )
    parser.add_argument(
        "--tools-dir",
        default=None,
        help="Path to output/tools/ directory (default: directory containing this script)",
    )
    parser.add_argument(
        "--save-report", default=None,
        help="Save report to this path",
    )
    args = parser.parse_args()

    tools_dir = args.tools_dir or os.path.dirname(os.path.abspath(__file__))
    chars = args.chars or list(_CHAR_REGISTRY.keys())

    results = [lint_character(c, tools_dir) for c in chars]
    report = format_report(results)

    print("=" * 70)
    print(f"LTG Character Spec Linter — v{__version__}")
    print("=" * 70)
    print(report)

    if args.save_report:
        save_path = args.save_report
    else:
        save_path = os.path.join(tools_dir, "LTG_TOOL_char_spec_lint_report.txt")

    try:
        with open(save_path, "w", encoding="utf-8") as fh:
            fh.write(f"LTG Character Spec Linter — v{__version__}\n")
            fh.write("=" * 70 + "\n\n")
            fh.write(report)
            fh.write("\n")
        print(f"\nReport saved to: {save_path}")
    except OSError as exc:
        print(f"\nCould not save report: {exc}")

    has_fail = any(r.get("overall") == "FAIL" for r in results)
    sys.exit(1 if has_fail else 0)
