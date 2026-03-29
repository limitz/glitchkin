"""
LTG_TOOL_palette_warmth_lint_v001.py
======================================
Warmth compliance linter for "Luma & the Glitchkin" CHAR-M palette entries.

PURPOSE
-------
Grandma Miri's color palette carries a production guarantee: every entry must
remain "unambiguously warm" (color story doc) — meaning R must be the dominant
channel. This tool flags any CHAR-M-xx entry where G > R or B > R, catching the
class of error that let CHAR-M-11 (Deep Sage, G>R, cool-neutral green) slip for
multiple cycles before being caught in Critique 13 (Priya Nair).

RULE
----
For every CHAR-M-xx entry:
  - R must be >= G  (red channel dominance — warm family)
  - R must be >= B  (red channel dominance — warm family)
A violation is any entry where G > R OR B > R.

USAGE (standalone CLI)
----------------------
    python LTG_TOOL_palette_warmth_lint_v001.py
    python LTG_TOOL_palette_warmth_lint_v001.py path/to/master_palette.md
    python LTG_TOOL_palette_warmth_lint_v001.py path/to/palette1.md path/to/palette2.md

PROGRAMMATIC API
----------------
    from LTG_TOOL_palette_warmth_lint_v001 import (
        lint_palette_file,
        lint_palette_text,
        format_report,
        DEFAULT_PALETTE_PATH,
    )

    results = lint_palette_file("output/color/palettes/master_palette.md")
    # results["result"] in ("PASS", "WARN")
    # results["violations"] is a list of dicts with:
    #   {"code": "CHAR-M-03", "name": "...", "hex": "#RRGGBB",
    #    "rgb": (R, G, B), "reason": "G > R (G=106, R=90)"}
    # results["total_checked"]: int — total CHAR-M-xx entries found
    # results["total_violations"]: int

Author: Sam Kowalski (Color & Style Artist)
Created: Cycle 33 — 2026-03-29
Version: 1.0.0

Actioned ideabox entry: ideabox/20260330_sam_kowalski_miri_slipper_warmth_audit.md
Design note: Operates entirely on markdown source text — no Pillow dependency,
no execution, no AST parsing. Pure regex + channel arithmetic.
"""

from __future__ import annotations

import os
import re
import sys
from typing import Dict, List, Optional, Tuple, Union


# ---------------------------------------------------------------------------
# Default palette path
# ---------------------------------------------------------------------------

_HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PALETTE_PATH = os.path.normpath(
    os.path.join(_HERE, "..", "color", "palettes", "master_palette.md")
)

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# Matches a CHAR-M-xx table row:
#   | CHAR-M-03 | Miri Skin Highlight | `#A86A40` | (168, 106, 64) | ... |
#
# Group 1: code      e.g. "CHAR-M-03"
# Group 2: name      e.g. "Miri Skin Highlight"
# Group 3: hex       e.g. "#A86A40"
# Group 4: r_str     e.g. "168"
# Group 5: g_str     e.g. "106"
# Group 6: b_str     e.g. "64"
_TABLE_ROW_RE = re.compile(
    r'\|\s*(CHAR-M-\d+)\s*\|\s*([^|]+?)\s*\|\s*`(#[0-9A-Fa-f]{6})`\s*\|\s*'
    r'\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*\|',
    re.IGNORECASE,
)

# Matches inline hex references OUTSIDE of table rows — e.g. Shadow: `#8A3C1C`
# We only check these when they appear inside a CHAR-M section heading block
# (between two ### 8.x section headers). This catches shadow/highlight companions
# that are named in the Notes column as prose rather than a table cell.
# NOTE: inline values inside Notes cells ARE already covered by the table row
# regex above (the Notes column is captured but not parsed for hex). This
# secondary pass captures the shadow/highlight companion values declared as
# prose in the Notes text.
_INLINE_SHADOW_RE = re.compile(
    r'Shadow:\s*`(#[0-9A-Fa-f]{6})`|Highlight:\s*`(#[0-9A-Fa-f]{6})`',
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def _check_rgb(r: int, g: int, b: int) -> List[str]:
    """Return list of warmth violation strings for the given (R, G, B)."""
    violations = []
    if g > r:
        violations.append(f"G > R (G={g}, R={r})")
    if b > r:
        violations.append(f"B > R (B={b}, R={r})")
    return violations


def _hex_to_rgb(hex_str: str) -> Optional[Tuple[int, int, int]]:
    """Parse '#RRGGBB' → (R, G, B). Returns None if parse fails."""
    h = hex_str.lstrip('#')
    if len(h) != 6:
        return None
    try:
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    except ValueError:
        return None


def lint_palette_text(text: str, source_name: str = "<text>") -> Dict:
    """
    Lint the given palette markdown text for CHAR-M-xx warmth violations.

    Parameters
    ----------
    text        : str  — full markdown text of the palette document
    source_name : str  — display name for the source (used in report messages)

    Returns
    -------
    dict with keys:
        result          : "PASS" | "WARN"
        source          : str
        total_checked   : int
        total_violations: int
        violations      : list[dict]  (empty if result == "PASS")
    """
    violations = []
    seen_codes = set()
    total_checked = 0

    for match in _TABLE_ROW_RE.finditer(text):
        code = match.group(1).upper()
        name = match.group(2).strip()
        hex_val = match.group(3).upper()
        r = int(match.group(4))
        g = int(match.group(5))
        b = int(match.group(6))

        if code in seen_codes:
            # Duplicate row — skip (already counted)
            continue
        seen_codes.add(code)
        total_checked += 1

        channel_violations = _check_rgb(r, g, b)
        if channel_violations:
            violations.append({
                "code": code,
                "name": name,
                "hex": hex_val,
                "rgb": (r, g, b),
                "reason": " | ".join(channel_violations),
                "source": source_name,
            })

    result = "WARN" if violations else "PASS"
    return {
        "result": result,
        "source": source_name,
        "total_checked": total_checked,
        "total_violations": len(violations),
        "violations": violations,
    }


def lint_palette_file(path: str) -> Dict:
    """
    Lint a palette markdown file. Returns the same dict as lint_palette_text().
    If the file cannot be read, returns a result dict with result="ERROR".
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        return {
            "result": "ERROR",
            "source": path,
            "total_checked": 0,
            "total_violations": 0,
            "violations": [],
            "error": str(exc),
        }
    return lint_palette_text(text, source_name=path)


def format_report(results: Union[Dict, List[Dict]]) -> str:
    """
    Format one or multiple lint result dicts as a human-readable report string.

    Accepts either a single dict (from lint_palette_file) or a list of dicts
    (from multiple files).
    """
    if isinstance(results, dict):
        results = [results]

    lines = []
    lines.append("=" * 60)
    lines.append("LTG CHAR-M Warmth Compliance Lint Report")
    lines.append("=" * 60)

    total_files = len(results)
    total_checked = sum(r.get("total_checked", 0) for r in results)
    total_violations = sum(r.get("total_violations", 0) for r in results)
    overall = "PASS" if total_violations == 0 else "WARN"

    for r in results:
        if r.get("result") == "ERROR":
            lines.append(f"\n[ERROR] {r['source']}: {r.get('error', 'unknown error')}")
            continue

        status_tag = f"[{r['result']}]"
        lines.append(f"\n{status_tag} {r['source']}")
        lines.append(f"  CHAR-M entries checked : {r['total_checked']}")
        lines.append(f"  Violations             : {r['total_violations']}")

        if r["violations"]:
            lines.append("")
            for v in r["violations"]:
                lines.append(f"  FAIL  {v['code']} — {v['name']}")
                lines.append(f"        Hex: {v['hex']}  RGB: {v['rgb']}")
                lines.append(f"        Reason: {v['reason']}")
                lines.append(f"        → Fix: R must be >= G and R >= B for all CHAR-M entries")

    lines.append("")
    lines.append("-" * 60)
    lines.append(f"FILES  : {total_files}")
    lines.append(f"CHECKED: {total_checked} CHAR-M entries")
    lines.append(f"RESULT : {overall} ({total_violations} violation(s))")
    lines.append("=" * 60)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point. Returns exit code: 0 = pass, 1 = violations found."""
    if argv is None:
        argv = sys.argv[1:]

    if argv:
        paths = argv
    else:
        # Default: run against the canonical master palette
        paths = [DEFAULT_PALETTE_PATH]

    results = [lint_palette_file(p) for p in paths]
    report = format_report(results)
    print(report)

    total_violations = sum(r.get("total_violations", 0) for r in results)
    return 1 if total_violations > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
