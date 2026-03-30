#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_spec_extractor.py
Character Spec Extractor — "Luma & the Glitchkin"
Author: Kai Nakamura / Cycle 35

Parses character .md spec files and extracts key numeric constraints
automatically, reducing manual maintenance of char_spec_lint checks and
keeping lint checks in sync with the spec documents.

Extracted constraint categories
---------------------------------
  head_ratio        Total height in head units (e.g. 3.2 for Luma, 4.0 for Cosmo)
  eye_coeff         Eye-width coefficient relative to head-radius (e.g. 0.22)
  colors            Hex color values tagged by associated label in the spec
  numeric_const     Dimensionless numeric constants (degrees, pixel ratios, counts)
  line_weights      Line weight values (width=N at render scale)
  counts            Integer counts of specific design elements (e.g. 5 hair curls)

Output format
--------------
  Python dict (JSON-serialisable) with the structure:

    {
      "character": "luma",
      "source_file": "path/to/luma.md",
      "extracted_at": "YYYY-MM-DD",
      "head_ratio": 3.2,
      "eye_coeff": 0.22,
      "colors": [
          {"label": "Hoodie", "hex": "#E8722A", "rgb": [232, 114, 42]},
          ...
      ],
      "numeric_const": [
          {"label": "glasses_tilt_neutral", "value": 7.0, "unit": "degrees"},
          ...
      ],
      "line_weights": [
          {"label": "head_outline", "width": 4, "render_scale": 2},
          ...
      ],
      "counts": [
          {"label": "hair_curls", "value": 5},
          ...
      ],
      "raw_notes": ["..."]   # bullet notes that mention numbers but were not classified
    }

Usage (standalone)
-------------------
    python LTG_TOOL_spec_extractor.py luma
    python LTG_TOOL_spec_extractor.py cosmo --json
    python LTG_TOOL_spec_extractor.py --all
    python LTG_TOOL_spec_extractor.py --all --save-dir output/specs/

API
----
    from LTG_TOOL_spec_extractor import extract_spec, extract_all, format_spec_report

    result = extract_spec("luma", spec_dir="/path/to/output/characters")
    print(format_spec_report(result))
"""

__version__ = "1.0.0"

import os
import re
import sys
import json
from datetime import date
from typing import Optional


# ── Spec file locations ──────────────────────────────────────────────────────

# Default search roots (relative paths resolved from this script's directory)
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT   = os.path.dirname(_SCRIPT_DIR)  # output/ parent

_CHAR_PATHS = {
    "luma":  ["output/characters/main/luma.md"],
    "cosmo": ["output/characters/main/cosmo.md"],
    "miri":  ["output/characters/supporting/grandma_miri.md"],
    "byte":  ["output/characters/main/byte.md"],
    "glitch": ["output/characters/main/glitch.md"],
}

ALL_CHARACTERS = list(_CHAR_PATHS.keys())


# ── Regex patterns ───────────────────────────────────────────────────────────

# Head ratio: "total height: N.N heads" or "**Total height: N.N heads**"
_HEAD_RATIO_RE = re.compile(
    r'total\s+height[:\s*]*([0-9]+\.?[0-9]*)\s*head',
    re.IGNORECASE
)

# Fallback: "N.N heads" near proportions section
_HEAD_RATIO_FALLBACK_RE = re.compile(
    r'\b([0-9]+\.[0-9]+)\s+heads\b',
    re.IGNORECASE
)

# Eye coefficient: "HR × 0.22" or "× 0.22" or "* 0.22" near "eye"
_EYE_COEFF_RE = re.compile(
    r'(?:HR|head[_\s]?r(?:adius)?)\s*[×x\*]\s*([0-9]+\.[0-9]+)',
    re.IGNORECASE
)

# Fallback eye coefficient: "0.N heads" near eye/width context in a proportion table
_EYE_COEFF_FALLBACK_RE = re.compile(
    r'[Ee]ye[^\n]*?([0-9]+\.[0-9]+)\s*x?\s*head',
    re.IGNORECASE
)

# Hex color: #RRGGBB or #RGB anywhere, plus the label on the same line
_HEX_RE = re.compile(
    r'([^\n]*?)\(?\s*(#[0-9A-Fa-f]{6}|#[0-9A-Fa-f]{3})\s*\)?'
)

# Degrees: "N degrees" or "N.N degrees" with surrounding context
_DEGREES_RE = re.compile(
    r'([^\n]*?)\b([0-9]+(?:\.[0-9]+)?)\s+degree[s]?',
    re.IGNORECASE
)

# Line weights: "width=N at 2× render" or "width = N"
_LINE_WEIGHT_RE = re.compile(
    r'([^\n]*?)\bwidth\s*=\s*([0-9]+)\b([^\n]*)',
    re.IGNORECASE
)

# Integer counts: "exactly N" or "always N" near a design element keyword
_COUNT_KEYWORDS = ['curl', 'spiral', 'expression', 'panel', 'panel', 'spike', 'freckle', 'strand', 'dot', 'step']
_EXACT_COUNT_RE = re.compile(
    r'(?:exactly|always|locked)\s+([0-9]+)\s+([a-z][a-z\s\-]+)',
    re.IGNORECASE
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _hex_to_rgb(h):
    """Convert #RRGGBB hex to (R, G, B) tuple."""
    h = h.lstrip('#')
    if len(h) == 3:
        h = h[0]*2 + h[1]*2 + h[2]*2
    return [int(h[i:i+2], 16) for i in (0, 2, 4)]


def _clean_label(text, max_len=50):
    """Extract a clean label from a surrounding text snippet."""
    # Remove markdown syntax
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'`[^`]*`', '', text)
    text = re.sub(r'\[[^\]]*\]', '', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Truncate
    if len(text) > max_len:
        text = text[:max_len].rsplit(' ', 1)[0] + '...'
    return text or 'unknown'


def _slugify(label):
    """Convert label to a snake_case key."""
    label = re.sub(r'[^\w\s]', '', label.lower())
    label = re.sub(r'\s+', '_', label.strip())
    return label[:40]


def _resolve_spec_path(char_name, spec_dir=None):
    """Return the absolute path to a character's spec .md file."""
    if spec_dir is None:
        spec_dir = _REPO_ROOT
    candidates = _CHAR_PATHS.get(char_name.lower(), [])
    for rel in candidates:
        full = os.path.join(spec_dir, rel)
        if os.path.isfile(full):
            return full
    # Last-resort search
    search_dirs = [
        os.path.join(spec_dir, "output", "characters", "main"),
        os.path.join(spec_dir, "output", "characters", "supporting"),
        os.path.join(spec_dir, "characters", "main"),
        os.path.join(spec_dir, "characters", "supporting"),
    ]
    for sdir in search_dirs:
        if not os.path.isdir(sdir):
            continue
        for fname in os.listdir(sdir):
            if char_name.lower() in fname.lower() and fname.endswith('.md'):
                return os.path.join(sdir, fname)
    return None


def _read_md(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        return fh.read()


# ── Extraction functions ──────────────────────────────────────────────────────

def _extract_head_ratio(source):
    """Extract total height in head units."""
    m = _HEAD_RATIO_RE.search(source)
    if m:
        return float(m.group(1))
    # Fallback: look for "N.N heads" in proportions section
    prop_idx = source.lower().find('proportion')
    if prop_idx >= 0:
        snippet = source[prop_idx:prop_idx + 600]
        m2 = _HEAD_RATIO_FALLBACK_RE.search(snippet)
        if m2:
            val = float(m2.group(1))
            # Filter obvious non-ratios (line widths etc)
            if 1.5 <= val <= 6.0:
                return val
    return None


def _extract_eye_coeff(source):
    """Extract eye-width coefficient relative to head radius."""
    m = _EYE_COEFF_RE.search(source)
    if m:
        return float(m.group(1))
    # Fallback: look near "eye" keyword
    eye_idx = source.lower().find('eye size')
    if eye_idx < 0:
        eye_idx = source.lower().find('eye width')
    if eye_idx >= 0:
        snippet = source[eye_idx:eye_idx + 300]
        m2 = re.search(r'([0-9]+\.[0-9]+)\s*x\s*head', snippet, re.IGNORECASE)
        if m2:
            return float(m2.group(1))
    return None


def _extract_colors(source):
    """Extract named hex colors from the spec."""
    colors = []
    seen_hex = set()
    lines = source.split('\n')
    for line in lines:
        for m in _HEX_RE.finditer(line):
            context = m.group(1)
            hex_val  = m.group(2).upper()
            if len(hex_val) == 4:
                # Expand #RGB to #RRGGBB
                hex_val = '#' + hex_val[1]*2 + hex_val[2]*2 + hex_val[3]*2
            if hex_val in seen_hex:
                continue
            seen_hex.add(hex_val)
            label = _clean_label(context)
            if not label or label == 'unknown':
                # Try the whole line context before the hex
                label = _clean_label(line.split(hex_val)[0])
            try:
                rgb = _hex_to_rgb(hex_val)
                colors.append({
                    "label": label,
                    "hex": hex_val,
                    "rgb": rgb
                })
            except (ValueError, IndexError):
                pass
    return colors


def _extract_numeric_const(source):
    """Extract numeric constants (degrees, ratios) with labels."""
    consts = []
    seen = set()

    # Degrees
    for m in _DEGREES_RE.finditer(source):
        context = m.group(1)
        value   = float(m.group(2))
        label   = _clean_label(context)
        key = (label[:20], value)
        if key not in seen:
            seen.add(key)
            consts.append({
                "label": label,
                "value": value,
                "unit": "degrees"
            })

    # Head-fraction ratios mentioned explicitly (e.g. "0.06x head width")
    ratio_re = re.compile(
        r'([^\n]*?)\b([0-9]+\.[0-9]+)\s*x\s*head',
        re.IGNORECASE
    )
    for m in ratio_re.finditer(source):
        context = m.group(1)
        value   = float(m.group(2))
        label   = _clean_label(context)
        key = (label[:20], value)
        if key not in seen and 0.001 < value < 10.0:
            seen.add(key)
            consts.append({
                "label": label,
                "value": value,
                "unit": "head_fraction"
            })

    return consts


def _extract_line_weights(source):
    """Extract line weight specifications."""
    weights = []
    seen = set()
    for m in _LINE_WEIGHT_RE.finditer(source):
        context_pre  = m.group(1)
        width        = int(m.group(2))
        context_post = m.group(3)
        full_context = context_pre + ' width=' + str(width) + ' ' + context_post
        label = _clean_label(full_context)

        # Detect render scale mention
        scale_m = re.search(r'(\d+)[\s]*[×x]?\s*render', context_post, re.IGNORECASE)
        render_scale = int(scale_m.group(1)) if scale_m else None

        key = (label[:20], width)
        if key not in seen and 0 < width <= 20:
            seen.add(key)
            entry = {"label": label, "width": width}
            if render_scale:
                entry["render_scale"] = render_scale
            weights.append(entry)

    return weights


def _extract_counts(source):
    """Extract exact integer counts of design elements."""
    counts = []
    seen = set()
    for m in _EXACT_COUNT_RE.finditer(source):
        value = int(m.group(1))
        noun  = m.group(2).strip().rstrip('s').rstrip('s').rstrip()
        # Filter out overly long nouns
        if len(noun) > 30:
            noun = noun[:30]
        key = (noun[:20], value)
        if key not in seen:
            seen.add(key)
            counts.append({
                "label": _slugify(noun),
                "value": value
            })
    return counts


def _extract_raw_notes(source):
    """Collect lines that mention numbers but were not fully classified."""
    notes = []
    seen = set()
    for line in source.split('\n'):
        line = line.strip()
        if not line:
            continue
        # Lines with numbers and spec-relevant keywords
        if re.search(r'\b(must|always|never|exactly|locked|canonical|spec)\b', line, re.IGNORECASE):
            if re.search(r'\b\d+\b', line):
                key = line[:60]
                if key not in seen:
                    seen.add(key)
                    notes.append(line[:120])
    return notes[:20]  # cap at 20 notes


# ── Public API ────────────────────────────────────────────────────────────────

def extract_spec(char_name, spec_dir=None):
    """
    Parse a character's spec .md file and extract numeric constraints.

    Parameters
    ----------
    char_name : str
        One of: "luma", "cosmo", "miri", "byte", "glitch"
    spec_dir : str, optional
        Root directory to resolve spec paths from.
        Defaults to the repository root (parent of output/tools/).

    Returns
    -------
    dict
        Extracted spec with keys: character, source_file, extracted_at,
        head_ratio, eye_coeff, colors, numeric_const, line_weights, counts,
        raw_notes, errors.
    """
    char_name = char_name.lower()
    result = {
        "character":    char_name,
        "source_file":  None,
        "extracted_at": date.today().isoformat(),
        "head_ratio":   None,
        "eye_coeff":    None,
        "colors":       [],
        "numeric_const": [],
        "line_weights": [],
        "counts":       [],
        "raw_notes":    [],
        "errors":       [],
    }

    if char_name not in _CHAR_PATHS:
        result["errors"].append(f"Unknown character '{char_name}'. Known: {ALL_CHARACTERS}")
        return result

    path = _resolve_spec_path(char_name, spec_dir)
    if path is None:
        result["errors"].append(f"Spec file not found for '{char_name}'")
        return result

    result["source_file"] = path

    try:
        source = _read_md(path)
    except OSError as e:
        result["errors"].append(f"Cannot read {path}: {e}")
        return result

    result["head_ratio"]   = _extract_head_ratio(source)
    result["eye_coeff"]    = _extract_eye_coeff(source)
    result["colors"]       = _extract_colors(source)
    result["numeric_const"] = _extract_numeric_const(source)
    result["line_weights"] = _extract_line_weights(source)
    result["counts"]       = _extract_counts(source)
    result["raw_notes"]    = _extract_raw_notes(source)

    return result


def extract_all(spec_dir=None):
    """
    Extract specs for all known characters.

    Returns
    -------
    list[dict]
        One result dict per character.
    """
    return [extract_spec(c, spec_dir) for c in ALL_CHARACTERS]


def format_spec_report(result_or_list):
    """
    Format extracted spec(s) as a human-readable text report.

    Parameters
    ----------
    result_or_list : dict or list[dict]
        Single result dict or list of result dicts from extract_spec / extract_all.

    Returns
    -------
    str
    """
    if isinstance(result_or_list, dict):
        results = [result_or_list]
    else:
        results = result_or_list

    lines = []
    lines.append("=" * 70)
    lines.append(f"LTG Spec Extractor v{__version__} — Extracted Constraints Report")
    lines.append(f"Generated: {date.today().isoformat()}")
    lines.append("=" * 70)
    lines.append("")

    for r in results:
        char = r["character"].upper()
        lines.append(f"{'─'*50}")
        lines.append(f"  Character: {char}")
        if r["source_file"]:
            lines.append(f"  Source:    {os.path.basename(r['source_file'])}")
        if r["errors"]:
            for e in r["errors"]:
                lines.append(f"  ERROR: {e}")
            lines.append("")
            continue

        # Head ratio
        if r["head_ratio"] is not None:
            lines.append(f"  Head ratio:    {r['head_ratio']} heads")
        else:
            lines.append(f"  Head ratio:    NOT FOUND")

        # Eye coefficient
        if r["eye_coeff"] is not None:
            lines.append(f"  Eye coeff:     HR × {r['eye_coeff']}")
        else:
            lines.append(f"  Eye coeff:     NOT FOUND")

        # Colors
        lines.append(f"  Colors ({len(r['colors'])} found):")
        for c in r["colors"][:15]:  # cap display at 15
            lines.append(f"    {c['hex']}  rgb{tuple(c['rgb'])}  — {c['label'][:50]}")
        if len(r["colors"]) > 15:
            lines.append(f"    ... and {len(r['colors'])-15} more")

        # Numeric constants
        if r["numeric_const"]:
            lines.append(f"  Numeric constants ({len(r['numeric_const'])}):")
            for n in r["numeric_const"][:10]:
                lines.append(f"    {n['value']} {n['unit']:14s}  — {n['label'][:50]}")

        # Line weights
        if r["line_weights"]:
            lines.append(f"  Line weights ({len(r['line_weights'])}):")
            for w in r["line_weights"][:8]:
                scale_str = f" @ {w['render_scale']}× render" if "render_scale" in w else ""
                lines.append(f"    width={w['width']}{scale_str}  — {w['label'][:50]}")

        # Counts
        if r["counts"]:
            lines.append(f"  Element counts ({len(r['counts'])}):")
            for c in r["counts"]:
                lines.append(f"    {c['value']:3d}  — {c['label']}")

        # Raw notes
        if r["raw_notes"]:
            lines.append(f"  Spec constraints (raw, {len(r['raw_notes'])}):")
            for n in r["raw_notes"][:5]:
                lines.append(f"    • {n[:80]}")

        lines.append("")

    lines.append("=" * 70)
    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

def _parse_args():
    import argparse
    p = argparse.ArgumentParser(
        description="LTG Spec Extractor — parse character spec .md files for numeric constraints"
    )
    p.add_argument(
        "character",
        nargs="?",
        choices=ALL_CHARACTERS + ["all"],
        help="Character to extract (or 'all' for all characters)"
    )
    p.add_argument(
        "--all", action="store_true",
        help="Extract all characters (same as 'all' positional)"
    )
    p.add_argument(
        "--json", action="store_true",
        help="Output as JSON instead of human-readable report"
    )
    p.add_argument(
        "--spec-dir", default=None,
        help="Root directory to resolve spec paths from (default: repo root)"
    )
    p.add_argument(
        "--save-dir", default=None,
        help="Directory to save output files (one per character or one combined)"
    )
    p.add_argument(
        "--save-report", default=None,
        help="Path to save text report"
    )
    return p.parse_args()


def main():
    args = _parse_args()

    spec_dir = args.spec_dir

    # Determine which characters to process
    if args.all or args.character == "all":
        results = extract_all(spec_dir)
    elif args.character:
        results = [extract_spec(args.character, spec_dir)]
    else:
        # Default: all
        results = extract_all(spec_dir)

    if args.json:
        output = json.dumps(results, indent=2)
        print(output)
    else:
        report = format_spec_report(results)
        print(report)

    # Save outputs
    if args.save_dir:
        os.makedirs(args.save_dir, exist_ok=True)
        for r in results:
            char = r["character"]
            # Save JSON
            json_path = os.path.join(args.save_dir, f"spec_{char}.json")
            with open(json_path, 'w', encoding='utf-8') as fh:
                json.dump(r, fh, indent=2)
            print(f"  Saved: {json_path}", file=sys.stderr)

    if args.save_report:
        report = format_spec_report(results)
        with open(args.save_report, 'w', encoding='utf-8') as fh:
            fh.write(report)
        print(f"Report saved: {args.save_report}", file=sys.stderr)

    # Exit code: 1 if any character had errors
    has_errors = any(r["errors"] for r in results)
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
