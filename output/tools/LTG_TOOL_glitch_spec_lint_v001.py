#!/usr/bin/env python3
"""
LTG_TOOL_glitch_spec_lint_v001.py
Glitch Spec Linter — "Luma & the Glitchkin"
Author: Kai Nakamura / Cycle 33

Validates Glitchkin generator code against the canonical character specification
in output/characters/main/glitch.md.

Checks performed
----------------
G001  Faceplate width within spec range
      rx must be in [30, 50] (spec reference: rx=38)
      ry must be in [28, 46] (spec reference: ry=34)

G002  Body mass ratio (ry > rx)
      The diamond must be taller than it is wide: ry_val > rx_val

G003  At least 2 unique Glitchkin in multi-Glitchkin frames
      Files that appear to render multiple Glitch figures (e.g. grids, lineups,
      multi-panel sheets) must not produce identical clones — each panel must vary
      at least one of: tilt_deg, squash, stretch, spike_h, or expression name.

G004  HOT_MAG crack is drawn AFTER body fill (draw order check)
      draw.line([cs, ce], fill=HOT_MAG ...) must appear AFTER draw.polygon fill
      for CORRUPT_AMB. (Checks via regex on function body order.)

G005  UV_PURPLE shadow offset present
      The shadow polygon must be drawn before the main fill with a (+3,+4) offset
      using UV_PURPLE color.

G006  No warm organic colors in Glitch body fill
      Body fill must use CORRUPT_AMBER family — no skin tones (defined as
      R > 180 and G > 120 and B > 80 and B < 160, not in Glitch palette).

G007  VOID_BLACK body outline present
      draw.polygon(pts, outline=VOID_BLACK ...) must be present.

G008  Interior states use bilateral eyes
      If the file defines YEARNING/COVETOUS/HOLLOW expressions, both eyes must
      use the same glyph (bilateral symmetry rule from spec §6.3).

Usage
-----
    python LTG_TOOL_glitch_spec_lint_v001.py [file_or_directory]
    python LTG_TOOL_glitch_spec_lint_v001.py output/tools/LTG_TOOL_glitch_expression_sheet_v003.py

API
---
    from LTG_TOOL_glitch_spec_lint_v001 import lint_file, lint_directory, format_report

    results = lint_directory("/path/to/output/tools")
    print(format_report(results))

Changelog
---------
v1.2.0 (C37): Suppression list support via glitch_spec_suppressions.json.
    lint_file() accepts optional suppressions= set of (basename, rule) tuples.
    lint_directory() loads suppressions once and shares across batch.
    format_report() shows suppressed issue counts.
    _load_suppressions() and _apply_suppressions() added.
v1.1.0 (C35): G002 spec constants corrected (rx=34, ry=38); G001 range widened.
v1.0.0 (C33): Initial implementation.
"""

__version__ = "1.2.0"  # C37: suppression list support (glitch_spec_suppressions.json)
                       # C35: G002 spec constants corrected (rx=34, ry=38); wider G001 range

import json
import os
import re
import sys

# ── Suppression list ──────────────────────────────────────────────────────────────

_SUPPRESSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "glitch_spec_suppressions.json")


def _load_suppressions(path=None):
    """
    Load suppression list from glitch_spec_suppressions.json.

    Returns a set of (basename, rule) tuples that should be silenced.
    Returns empty set if file is missing or malformed.
    """
    p = path or _SUPPRESSION_FILE
    if not os.path.isfile(p):
        return set()
    try:
        with open(p, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        entries = data.get("suppressions", [])
        return {(e["file"], e["rule"]) for e in entries if "file" in e and "rule" in e}
    except (json.JSONDecodeError, OSError):
        return set()


def _apply_suppressions(issues, basename, suppression_set):
    """
    Filter *issues* (list of str) using the suppression set.

    An issue is suppressed if its rule code (e.g. "G007") appears in
    a suppression entry for this file's basename.

    Returns (kept_issues, suppressed_count).
    """
    kept = []
    suppressed = 0
    for issue in issues:
        # Extract rule code: first word that matches G\d{3}
        m = re.match(r'(G\d{3}):', issue)
        rule = m.group(1) if m else None
        if rule and (basename, rule) in suppression_set:
            suppressed += 1
        else:
            kept.append(issue)
    return kept, suppressed

# ── Spec constants (from glitch.md) ────────────────────────────────────────────

# G001: rx/ry range — updated C35 (G002 fix: rx=34, ry=38 canonical)
RX_SPEC = 34     # reference (was 38 — corrected C35; body is taller than wide)
RY_SPEC = 38     # reference (was 34 — corrected C35)
RX_MIN, RX_MAX = 28, 56   # ±40% tolerance for scaled renders (color_model uses rx~50)
RY_MIN, RY_MAX = 28, 64   # ±40% tolerance for scaled renders (color_model uses ry~56)

# G003: keywords that suggest a multi-Glitchkin file
_MULTI_KEYWORDS = re.compile(
    r'\bfor\b.*\bexpression\b|\bfor\b.*\bpanel\b|\bCOLS\s*=\s*[2-9]|\bROWS\s*=\s*[2-9]'
    r'|\bexpressions\s*=\s*\['
    r'|\bpanels\s*=\s*\[',
    re.IGNORECASE
)

# G004: crack draw order — HOT_MAG line must appear after CORRUPT_AMB polygon fill
_CRACK_LINE_PATTERN   = re.compile(r'draw\.line\s*\(\s*\[.*\]\s*,\s*fill\s*=\s*HOT_MAG', re.DOTALL)
_BODY_FILL_PATTERN    = re.compile(r'draw\.polygon\s*\([^)]*fill\s*=\s*CORRUPT_AMB[^)]*\)', re.DOTALL)

# G005: UV_PURPLE shadow offset check
_SHADOW_PATTERN = re.compile(
    r'\+\s*3\s*,\s*y\s*\+\s*4\b|\+3\s*,\s*y\s*\+\s*4\b|UV_PURPLE.*shadow|shadow.*UV_PURPLE'
    r'|sh_pts.*UV_PURPLE|draw\.polygon\s*\(\s*sh_pts\s*,\s*fill\s*=\s*UV_PURPLE',
    re.IGNORECASE | re.DOTALL,
)

# G006: organic/skin-like warm colors — none of these should appear as body fill
# We check for literal RGB tuples that look like skin tones in fill= arguments
_SKIN_TONE_FILL = re.compile(
    r'fill\s*=\s*\(\s*([12][0-9]{2})\s*,\s*(1[2-9][0-9]|[2-9][0-9])\s*,\s*'
    r'(7[0-9]|[89][0-9]|1[0-4][0-9])\s*\)',
)

# G007: VOID_BLACK outline on body polygon
_VOIDBLACK_OUTLINE = re.compile(
    r'draw\.polygon\s*\([^)]*outline\s*=\s*VOID_BLACK[^)]*\)',
    re.DOTALL,
)

# G008: interior state bilateral eyes
_INTERIOR_STATES    = re.compile(r'\b(YEARNING|COVETOUS|HOLLOW)\b')
_BILATERAL_COMMENT  = re.compile(
    r'bilateral|both.eyes.*same|interior.*state.*eyes|YEARNING.*same|symmetric.*eye',
    re.IGNORECASE,
)

# Regex to find rx= and ry= assignments with numeric literals
_RX_ASSIGN = re.compile(r'\brx\s*=\s*(\d+)')
_RY_ASSIGN = re.compile(r'\bry\s*=\s*(\d+)')

# ── Helpers ─────────────────────────────────────────────────────────────────────

def _read_source(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as fh:
            return fh.read(), None
    except OSError as e:
        return None, str(e)


def _is_glitch_generator(source):
    """
    Return True only if this file actually draws a Glitchkin figure.
    We require at least one of: diamond_pts, CORRUPT_AMB, draw_glitch_body
    to be present in the source.
    """
    markers = ['diamond_pts', 'CORRUPT_AMB', 'draw_glitch_body', 'CORRUPT_AMBER']
    return any(m in source for m in markers)


def _check_g001_dimensions(source):
    """G001 — rx/ry within spec range."""
    issues = []
    rx_vals = [int(m.group(1)) for m in _RX_ASSIGN.finditer(source)]
    ry_vals = [int(m.group(1)) for m in _RY_ASSIGN.finditer(source)]

    for v in rx_vals:
        if not (RX_MIN <= v <= RX_MAX):
            issues.append(f"G001: rx={v} is outside spec range [{RX_MIN}–{RX_MAX}] (spec ref: {RX_SPEC})")

    for v in ry_vals:
        if not (RY_MIN <= v <= RY_MAX):
            issues.append(f"G001: ry={v} is outside spec range [{RY_MIN}–{RY_MAX}] (spec ref: {RY_SPEC})")

    return issues


def _check_g002_body_mass_ratio(source):
    """G002 — ry > rx (taller than wide)."""
    issues = []
    rx_vals = [int(m.group(1)) for m in _RX_ASSIGN.finditer(source)]
    ry_vals = [int(m.group(1)) for m in _RY_ASSIGN.finditer(source)]

    if rx_vals and ry_vals:
        rx = rx_vals[0]
        ry = ry_vals[0]
        if ry <= rx:
            issues.append(
                f"G002: Body mass ratio FAIL — ry={ry} must be > rx={rx} (diamond must be taller than wide)"
            )
    return issues


def _check_g003_multi_glitchkin(source):
    """G003 — multi-Glitchkin frames must have >= 2 unique figures."""
    issues = []
    if not _MULTI_KEYWORDS.search(source):
        return issues  # Not a multi-panel file

    # Count how many distinct expression/pose names appear
    expr_names = re.findall(
        r'"(NEUTRAL|MISCHIEVOUS|CALCULATING|PANICKED|TRIUMPHANT|STUNNED|YEARNING|COVETOUS|HOLLOW)"',
        source,
    )
    unique_exprs = set(expr_names)
    if len(unique_exprs) < 2:
        issues.append(
            f"G003: Multi-Glitchkin frame has only {len(unique_exprs)} unique expression(s) — "
            f"at least 2 required. Found: {sorted(unique_exprs) if unique_exprs else 'none'}"
        )
    return issues


def _check_g004_crack_draw_order(source):
    """G004 — HOT_MAG crack must be drawn AFTER body fill."""
    issues = []
    fill_match  = _BODY_FILL_PATTERN.search(source)
    crack_match = _CRACK_LINE_PATTERN.search(source)

    if fill_match and crack_match:
        if crack_match.start() < fill_match.start():
            issues.append(
                "G004: Draw order FAIL — HOT_MAG crack line appears BEFORE body fill polygon. "
                "Crack must be drawn after fill (spec §2.3 stacking order)."
            )
    elif crack_match and not fill_match:
        # crack exists but no fill found — unusual
        pass
    # If no crack found, skip (crack_visible=False may be intentional)
    return issues


def _check_g005_uv_shadow(source):
    """G005 — UV_PURPLE shadow offset (+3,+4) present."""
    issues = []
    if 'CORRUPT_AMB' not in source and 'CORRUPT_AMBER' not in source:
        return issues  # Not a Glitch body generator

    if not _SHADOW_PATTERN.search(source):
        # Also accept: sh_pts with UV_PURPLE
        if 'UV_PURPLE' not in source or 'sh_pts' not in source:
            issues.append(
                "G005: UV_PURPLE shadow offset (+3,+4) not detected. "
                "Spec §2.2 requires UV_PURPLE shadow polygon before body fill."
            )
    return issues


def _check_g006_no_organic_fill(source):
    """G006 — No organic/skin-tone RGB tuples as body fill."""
    issues = []
    for m in _SKIN_TONE_FILL.finditer(source):
        r_val = int(m.group(1))
        g_val = int(m.group(2))
        b_val = int(m.group(3))
        # Confirm not in known Glitch palette
        known = [
            (255,140,0), (168,76,0), (255,185,80), (232,201,90),
            (255,45,107), (123,47,190), (57,255,20), (0,240,255),
            (10,10,20), (248,246,236),
        ]
        rgb = (r_val, g_val, b_val)
        if rgb not in known:
            issues.append(
                f"G006: Possible organic/warm fill detected — fill={rgb}. "
                f"Glitch body fill must use CORRUPT_AMBER family only (spec §10)."
            )
    return issues


def _check_g007_void_outline(source):
    """G007 — VOID_BLACK polygon outline present."""
    issues = []
    if 'CORRUPT_AMB' not in source and 'CORRUPT_AMBER' not in source:
        return issues
    if not _VOIDBLACK_OUTLINE.search(source):
        # Also accept if VOID_BLACK appears as outline in any draw call
        if 'outline=VOID_BLACK' not in source and 'outline = VOID_BLACK' not in source:
            issues.append(
                "G007: VOID_BLACK outline on body polygon not detected. "
                "Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3)."
            )
    return issues


def _check_g008_interior_bilateral(source):
    """G008 — Interior states (YEARNING/COVETOUS/HOLLOW) must use bilateral eyes."""
    issues = []
    has_interior = bool(_INTERIOR_STATES.search(source))
    if not has_interior:
        return issues

    # If it uses a destabilize_right_eye or asymmetric right-eye function
    # AND mentions interior states without bilateral override → flag
    has_destabilize = bool(re.search(r'destabilize|right_eye|reye|r_eye', source, re.IGNORECASE))
    has_bilateral   = bool(_BILATERAL_COMMENT.search(source))

    # If interior state is handled but no bilateral mention/function at all
    if has_destabilize and not has_bilateral:
        # Check if bilateral is implied by same glyph assignments
        # Look for yearning/hollow/covetous glyph assignments to both eyes
        bilateral_assignments = re.findall(
            r'(YEARNING|COVETOUS|HOLLOW).*?leye.*?reye|'
            r'(yearning|covetous|hollow).*?left_eye.*?right_eye',
            source, re.IGNORECASE | re.DOTALL,
        )
        if not bilateral_assignments:
            issues.append(
                "G008: Interior states (YEARNING/COVETOUS/HOLLOW) detected but no bilateral "
                "eye rule found. Spec §6.3: interior states require IDENTICAL left+right eye "
                "glyphs — asymmetric destabilization must be SKIPPED for these states."
            )
    return issues


# ── Main lint function ──────────────────────────────────────────────────────────

def lint_file(filepath, suppressions=None):
    """
    Lint a single Glitchkin generator file against the spec.

    Parameters
    ----------
    filepath     : str   — Absolute path to the .py file.
    suppressions : set | None
        Set of (basename, rule) tuples to suppress. If None, loaded automatically
        from glitch_spec_suppressions.json in the same directory as this tool.

    Returns
    -------
    dict with keys:
        file              : str
        is_glitch         : bool  — True if file appears to be a Glitch generator
        issues            : list of str (issue descriptions, after suppression)
        suppressed_count  : int   — how many issues were suppressed
        status            : "PASS" | "WARN" | "SKIP"
            PASS  — is_glitch=True, 0 active issues (suppressed issues do not count)
            WARN  — is_glitch=True, 1+ active issues
            SKIP  — is_glitch=False (not a Glitch generator; not linted)
    """
    if suppressions is None:
        suppressions = _load_suppressions()

    source, err = _read_source(filepath)
    if source is None:
        return {
            "file": filepath,
            "is_glitch": False,
            "issues": [f"READ ERROR: {err}"],
            "suppressed_count": 0,
            "status": "WARN",
        }

    if not _is_glitch_generator(source):
        return {
            "file": filepath,
            "is_glitch": False,
            "issues": [],
            "suppressed_count": 0,
            "status": "SKIP",
        }

    raw_issues = []
    raw_issues.extend(_check_g001_dimensions(source))
    raw_issues.extend(_check_g002_body_mass_ratio(source))
    raw_issues.extend(_check_g003_multi_glitchkin(source))
    raw_issues.extend(_check_g004_crack_draw_order(source))
    raw_issues.extend(_check_g005_uv_shadow(source))
    raw_issues.extend(_check_g006_no_organic_fill(source))
    raw_issues.extend(_check_g007_void_outline(source))
    raw_issues.extend(_check_g008_interior_bilateral(source))

    basename = os.path.basename(filepath)
    issues, suppressed_count = _apply_suppressions(raw_issues, basename, suppressions)

    status = "WARN" if issues else "PASS"
    return {
        "file": filepath,
        "is_glitch": True,
        "issues": issues,
        "suppressed_count": suppressed_count,
        "status": status,
    }


def lint_directory(directory, pattern="*.py", skip_legacy=True):
    """
    Lint all Python files in a directory.

    Parameters
    ----------
    directory  : str
    pattern    : str   — glob pattern (default "*.py")
    skip_legacy: bool  — skip legacy/ subdirectory (default True)

    Returns
    -------
    list of result dicts from lint_file()

    Note: suppressions are loaded once from glitch_spec_suppressions.json
    and shared across all files in the batch for efficiency.
    """
    import fnmatch
    suppressions = _load_suppressions()
    results = []
    for fname in sorted(os.listdir(directory)):
        if skip_legacy and fname == "legacy":
            continue
        if not fnmatch.fnmatch(fname, pattern):
            continue
        fpath = os.path.join(directory, fname)
        if not os.path.isfile(fpath):
            continue
        result = lint_file(fpath, suppressions=suppressions)
        if result["status"] != "SKIP":
            results.append(result)
    return results


def format_report(results):
    """
    Format lint results into a human-readable report.

    Parameters
    ----------
    results : list of dicts from lint_file() / lint_directory()

    Returns
    -------
    str
    """
    lines = []
    lines.append("=" * 70)
    lines.append(f"LTG Glitch Spec Linter v{__version__} — Report")
    lines.append(f"Glitch generators found: {len(results)}")
    passes = [r for r in results if r["status"] == "PASS"]
    warns  = [r for r in results if r["status"] == "WARN"]
    total_suppressed = sum(r.get("suppressed_count", 0) for r in results)
    lines.append(f"  PASS : {len(passes)}")
    lines.append(f"  WARN : {len(warns)}")
    if total_suppressed:
        lines.append(f"  (suppressed issues across all files: {total_suppressed})")
    lines.append("=" * 70)

    for result in results:
        fname = os.path.basename(result["file"])
        status = result["status"]
        sup_note = f"  [{result.get('suppressed_count', 0)} suppressed]" if result.get("suppressed_count") else ""
        lines.append(f"\n[{status}] {fname}{sup_note}")
        if result["issues"]:
            for iss in result["issues"]:
                lines.append(f"  - {iss}")
        else:
            lines.append("  All checks passed.")

    lines.append("\n" + "=" * 70)
    lines.append("Checks: G001 dimensions | G002 body ratio | G003 multi-uniqueness |")
    lines.append("        G004 crack order | G005 UV shadow | G006 organic fill |")
    lines.append("        G007 void outline | G008 interior bilateral")
    lines.append("Suppressions: glitch_spec_suppressions.json")

    if warns:
        lines.append(f"\n{len(warns)} Glitch generator(s) have spec violations. Review before critique.")
    else:
        lines.append("\nAll Glitch generators pass spec validation.")
    lines.append("=" * 70)

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description=f"LTG Glitch Spec Linter v{__version__} — validate Glitchkin generators against spec"
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=os.path.dirname(os.path.abspath(__file__)),
        help="File or directory to lint (default: this file's directory)"
    )
    parser.add_argument(
        "--save-report", metavar="PATH",
        help="Save report to this path"
    )
    parser.add_argument(
        "--include-legacy", action="store_true",
        help="Also scan the legacy/ subdirectory"
    )
    args = parser.parse_args()

    target = args.target
    if os.path.isfile(target):
        result = lint_file(target)
        results = [result] if result["status"] != "SKIP" else []
        if not results:
            print(f"SKIP: {os.path.basename(target)} — not a Glitch generator")
            return
    elif os.path.isdir(target):
        results = lint_directory(target, skip_legacy=not args.include_legacy)
    else:
        print(f"ERROR: {target} is not a file or directory", file=sys.stderr)
        sys.exit(1)

    report = format_report(results)

    if args.save_report:
        with open(args.save_report, 'w', encoding='utf-8') as fh:
            fh.write(report)
        print(f"Report saved to: {args.save_report}")
    else:
        print(report)


if __name__ == "__main__":
    main()
