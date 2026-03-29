"""
LTG_TOOL_palette_warmth_lint_v002.py
======================================
Warmth compliance linter for "Luma & the Glitchkin" palette entries.

CHANGES FROM v001
-----------------
v002 (Cycle 34 — 2026-03-29):
  - Configurable character prefix list via JSON config file
    (default: output/tools/warmth_lint_config.json)
  - Default config includes CHAR-M (Grandma Miri) — same behaviour as v001
  - New API: load_config(), DEFAULT_CONFIG_PATH
  - format_report() header now reflects active prefix list
  - Report title updated: "LTG Warmth Compliance Lint Report"
  - Actioned from ideabox: ideabox/actioned/20260329_sam_kowalski_warmth_lint_scope_expansion.md

v001 (Cycle 33 — 2026-03-29):
  Original CHAR-M-only warmth linter.

PURPOSE
-------
Some characters carry a production colour guarantee: every palette entry for
that character must remain "unambiguously warm" — meaning R must be the
dominant channel. This tool flags any matching entry where G > R or B > R,
catching the class of error that let CHAR-M-11 (Deep Sage, G>R) slip for
multiple cycles before being caught in Critique 13 (Priya Nair).

RULE
----
For every matching CHAR-xx-nn entry (where xx is listed in the config):
  - R must be >= G  (red channel dominance — warm family)
  - R must be >= B  (red channel dominance — warm family)
A violation is any entry where G > R OR B > R.

CONFIG FILE: warmth_lint_config.json
-------------------------------------
{
  "warm_prefixes": ["CHAR-M", "CHAR-X"],
  "description": "Characters whose palette entries must be unambiguously warm (R dominant)"
}

If the config file is absent, the tool falls back to the default built-in config
(CHAR-M only), which preserves v001 behaviour.

USAGE (standalone CLI)
----------------------
    python LTG_TOOL_palette_warmth_lint_v002.py
    python LTG_TOOL_palette_warmth_lint_v002.py path/to/master_palette.md
    python LTG_TOOL_palette_warmth_lint_v002.py palette1.md palette2.md
    python LTG_TOOL_palette_warmth_lint_v002.py --config path/to/warmth_lint_config.json palette.md

PROGRAMMATIC API
----------------
    from LTG_TOOL_palette_warmth_lint_v002 import (
        lint_palette_file,
        lint_palette_text,
        format_report,
        load_config,
        DEFAULT_PALETTE_PATH,
        DEFAULT_CONFIG_PATH,
    )

    config = load_config()                       # loads from default config path
    config = load_config("path/to/config.json")  # loads from explicit path
    # config == {"warm_prefixes": ["CHAR-M"], ...}

    results = lint_palette_file("output/color/palettes/master_palette.md", config=config)
    # results["result"] in ("PASS", "WARN")
    # results["violations"] is a list of dicts with:
    #   {"code": "CHAR-M-03", "name": "...", "hex": "#RRGGBB",
    #    "rgb": (R, G, B), "reason": "G > R (G=106, R=90)", "source": "..."}
    # results["total_checked"]: int — total matching entries found
    # results["total_violations"]: int
    # results["prefixes_checked"]: list[str] — active prefix list

Author: Sam Kowalski (Color & Style Artist)
Created: Cycle 34 — 2026-03-29
Version: 2.0.0

Design note: Operates entirely on markdown source text — no Pillow dependency,
no execution, no AST parsing. Pure regex + channel arithmetic.
"""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Dict, List, Optional, Tuple, Union


# ---------------------------------------------------------------------------
# Default paths
# ---------------------------------------------------------------------------

_HERE = os.path.dirname(os.path.abspath(__file__))

DEFAULT_PALETTE_PATH = os.path.normpath(
    os.path.join(_HERE, "..", "color", "palettes", "master_palette.md")
)

DEFAULT_CONFIG_PATH = os.path.normpath(
    os.path.join(_HERE, "warmth_lint_config.json")
)

# Built-in fallback config (same behaviour as v001)
_BUILTIN_CONFIG = {
    "warm_prefixes": ["CHAR-M"],
    "description": "Characters whose palette entries must be unambiguously warm (R dominant)"
}


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

def load_config(path: Optional[str] = None) -> Dict:
    """
    Load the warmth lint config from a JSON file.

    Parameters
    ----------
    path : str or None
        Path to the config JSON file. If None, uses DEFAULT_CONFIG_PATH.
        If the file does not exist, falls back to the built-in CHAR-M-only config.

    Returns
    -------
    dict with keys:
        warm_prefixes : list[str]   — list of CHAR-XX prefix codes to check
        description   : str         — human-readable description (optional)
    """
    config_path = path if path is not None else DEFAULT_CONFIG_PATH

    try:
        with open(config_path, "r", encoding="utf-8") as fh:
            cfg = json.load(fh)
    except FileNotFoundError:
        # Graceful fallback — preserves v001 behaviour when no config file exists
        return dict(_BUILTIN_CONFIG)
    except (json.JSONDecodeError, OSError) as exc:
        sys.stderr.write(
            f"[warmth_lint] WARNING: Could not read config '{config_path}': {exc}\n"
            f"[warmth_lint] Falling back to built-in CHAR-M config.\n"
        )
        return dict(_BUILTIN_CONFIG)

    # Validate minimal structure
    if "warm_prefixes" not in cfg or not isinstance(cfg["warm_prefixes"], list):
        sys.stderr.write(
            f"[warmth_lint] WARNING: Config '{config_path}' missing 'warm_prefixes' list.\n"
            f"[warmth_lint] Falling back to built-in CHAR-M config.\n"
        )
        return dict(_BUILTIN_CONFIG)

    # Normalise prefix strings to uppercase, strip whitespace
    cfg["warm_prefixes"] = [str(p).strip().upper() for p in cfg["warm_prefixes"] if p]
    return cfg


# ---------------------------------------------------------------------------
# Regex pattern builder
# ---------------------------------------------------------------------------

def _build_table_row_re(prefixes: List[str]) -> re.Pattern:
    """
    Build a compiled regex that matches table rows for ANY of the given prefixes.

    Pattern matches:
      | CHAR-M-03 | Miri Skin Highlight | `#A86A40` | (168, 106, 64) | ... |
      | CHAR-X-01 | Some Color          | `#RRGGBB` | (R, G, B) | ... |

    Groups:
      1: code    e.g. "CHAR-M-03"
      2: name    e.g. "Miri Skin Highlight"
      3: hex     e.g. "#A86A40"
      4: r_str   e.g. "168"
      5: g_str   e.g. "106"
      6: b_str   e.g. "64"
    """
    # Build alternation from prefix list.  Each prefix like "CHAR-M" must
    # appear at the start of the code field followed by "-" + digits.
    escaped = [re.escape(p) for p in prefixes]
    prefix_alternation = "|".join(escaped)
    # Full code pattern: (CHAR-M|CHAR-X)-\d+
    code_pattern = rf"(?:{prefix_alternation})-\d+"

    pattern = (
        rf'\|\s*({code_pattern})\s*\|\s*([^|]+?)\s*\|\s*`(#[0-9A-Fa-f]{{6}})`\s*\|\s*'
        rf'\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*\|'
    )
    return re.compile(pattern, re.IGNORECASE)


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


def lint_palette_text(
    text: str,
    source_name: str = "<text>",
    config: Optional[Dict] = None,
) -> Dict:
    """
    Lint the given palette markdown text for warmth violations.

    Parameters
    ----------
    text        : str  — full markdown text of the palette document
    source_name : str  — display name for the source (used in report messages)
    config      : dict or None — warmth lint config (from load_config()).
                  If None, calls load_config() to get the default config.

    Returns
    -------
    dict with keys:
        result            : "PASS" | "WARN"
        source            : str
        total_checked     : int
        total_violations  : int
        violations        : list[dict]  (empty if result == "PASS")
        prefixes_checked  : list[str]
    """
    if config is None:
        config = load_config()

    prefixes = config.get("warm_prefixes", ["CHAR-M"])
    if not prefixes:
        prefixes = ["CHAR-M"]

    table_row_re = _build_table_row_re(prefixes)

    violations = []
    seen_codes: set = set()
    total_checked = 0

    for match in table_row_re.finditer(text):
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
        "prefixes_checked": list(prefixes),
    }


def lint_palette_file(
    path: str,
    config: Optional[Dict] = None,
) -> Dict:
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
            "prefixes_checked": [],
            "error": str(exc),
        }
    return lint_palette_text(text, source_name=path, config=config)


def format_report(
    results: Union[Dict, List[Dict]],
    config: Optional[Dict] = None,
) -> str:
    """
    Format one or multiple lint result dicts as a human-readable report string.

    Accepts either a single dict (from lint_palette_file) or a list of dicts
    (from multiple files).
    """
    if isinstance(results, dict):
        results = [results]

    # Collect active prefixes for the header
    all_prefixes: List[str] = []
    for r in results:
        for p in r.get("prefixes_checked", []):
            if p not in all_prefixes:
                all_prefixes.append(p)
    if not all_prefixes and config:
        all_prefixes = config.get("warm_prefixes", ["CHAR-M"])
    if not all_prefixes:
        all_prefixes = ["CHAR-M"]

    lines = []
    lines.append("=" * 60)
    lines.append("LTG Warmth Compliance Lint Report")
    lines.append(f"Prefixes checked: {', '.join(all_prefixes)}")
    lines.append("=" * 60)

    total_files = len(results)
    total_checked = sum(r.get("total_checked", 0) for r in results)
    total_violations = sum(r.get("total_violations", 0) for r in results)
    overall = "PASS" if total_violations == 0 else "WARN"

    for r in results:
        if r.get("result") == "ERROR":
            lines.append(f"\n[ERROR] {r['source']}: {r.get('error', 'unknown error')}")
            continue

        prefixes_this = r.get("prefixes_checked", all_prefixes)
        status_tag = f"[{r['result']}]"
        lines.append(f"\n{status_tag} {r['source']}")
        lines.append(f"  Prefixes checked       : {', '.join(prefixes_this)}")
        lines.append(f"  Matching entries checked: {r['total_checked']}")
        lines.append(f"  Violations              : {r['total_violations']}")

        if r["violations"]:
            lines.append("")
            for v in r["violations"]:
                lines.append(f"  FAIL  {v['code']} — {v['name']}")
                lines.append(f"        Hex: {v['hex']}  RGB: {v['rgb']}")
                lines.append(f"        Reason: {v['reason']}")
                lines.append(
                    f"        Fix: R must be >= G and R >= B "
                    f"for all {', '.join(prefixes_this)} entries"
                )

    lines.append("")
    lines.append("-" * 60)
    lines.append(f"FILES  : {total_files}")
    lines.append(f"CHECKED: {total_checked} matching entries")
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

    config_path: Optional[str] = None
    palette_paths: List[str] = []

    # Simple argument parsing
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--config":
            i += 1
            if i < len(argv):
                config_path = argv[i]
            else:
                sys.stderr.write("[warmth_lint] ERROR: --config requires a path argument\n")
                return 2
        else:
            palette_paths.append(arg)
        i += 1

    config = load_config(config_path)

    if not palette_paths:
        # Default: run against the canonical master palette
        palette_paths = [DEFAULT_PALETTE_PATH]

    results = [lint_palette_file(p, config=config) for p in palette_paths]
    report = format_report(results, config=config)
    print(report)

    total_violations = sum(r.get("total_violations", 0) for r in results)
    return 1 if total_violations > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
