"""
LTG_TOOL_palette_warmth_lint_v003.py
======================================
Warmth compliance linter for "Luma & the Glitchkin" palette entries.

CHANGES FROM v002
-----------------
v003 (Cycle 35 — 2026-03-29):
  - Soft-tolerance mode via "soft_tolerance" JSON config key.
    `soft_tolerance: {"G": 0, "B": 10}` (default 0 = strict, same as v002).
    A value of 10 means "G may exceed R by at most 10 counts without flagging".
    Both channels have independent tolerance values.
  - Default config ships with soft_tolerance = {"G": 0, "B": 0} (strict — preserves v002
    behaviour if config is absent or soft_tolerance key is missing).
  - Violations now include margin info: "G > R by 15 (tolerance=0)" — clearer diagnostics.
  - CLI --strict flag forces tolerance to 0 regardless of config (useful for CI).
  - Actioned from C34 ideabox: ideabox/actioned/20260329_sam_kowalski_warmth_lint_multi_channel.md

v002 (Cycle 34 — 2026-03-29):
  - Configurable character prefix list via JSON config file.
  - Default config: output/tools/warmth_lint_config.json.

v001 (Cycle 33 — 2026-03-29):
  - Original CHAR-M-only warmth linter.

PURPOSE
-------
Some characters carry a production colour guarantee: every palette entry for
that character must remain "unambiguously warm" — meaning R must be the
dominant channel (within the configured tolerance).

RULE (soft-tolerance mode)
--------------------------
For every matching CHAR-xx-nn entry:
  - G - R <= soft_tolerance["G"]   (G may exceed R by at most G-tolerance counts)
  - B - R <= soft_tolerance["B"]   (B may exceed R by at most B-tolerance counts)

Default: soft_tolerance = {"G": 0, "B": 0} → strict (same as v002, flags ANY G > R or B > R).

CONFIG FILE: warmth_lint_config.json (v003 extension)
------------------------------------------------------
{
  "warm_prefixes": ["CHAR-M"],
  "soft_tolerance": {"G": 0, "B": 0},
  "description": "..."
}

soft_tolerance is optional — if absent, defaults to {"G": 0, "B": 0} (strict).
Set "B": 10 to allow warm-adjacent dusty lavenders/grays with B up to R+10.

USAGE (standalone CLI)
----------------------
    python LTG_TOOL_palette_warmth_lint_v003.py
    python LTG_TOOL_palette_warmth_lint_v003.py path/to/master_palette.md
    python LTG_TOOL_palette_warmth_lint_v003.py --config path/to/config.json palette.md
    python LTG_TOOL_palette_warmth_lint_v003.py --strict palette.md  # forces tolerance=0

PROGRAMMATIC API
----------------
    from LTG_TOOL_palette_warmth_lint_v003 import (
        lint_palette_file,
        lint_palette_text,
        format_report,
        load_config,
        DEFAULT_PALETTE_PATH,
        DEFAULT_CONFIG_PATH,
    )

    config = load_config()
    # config == {"warm_prefixes": ["CHAR-M"], "soft_tolerance": {"G": 0, "B": 0}}

    results = lint_palette_file("output/color/palettes/master_palette.md", config=config)
    # Violations dict gains "margin" field: {"code": ..., "margin": {"G": 15, "B": 0}, ...}

    # Force strict mode regardless of config:
    strict_cfg = {**config, "soft_tolerance": {"G": 0, "B": 0}}
    results_strict = lint_palette_file(path, config=strict_cfg)

Author: Sam Kowalski (Color & Style Artist)
Created: Cycle 35 — 2026-03-29
Version: 3.0.0

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

# Built-in fallback config — strict, CHAR-M only (same behaviour as v001/v002)
_BUILTIN_CONFIG: Dict = {
    "warm_prefixes": ["CHAR-M"],
    "soft_tolerance": {"G": 0, "B": 0},
    "description": (
        "Characters whose palette entries must be unambiguously warm "
        "(R dominant). Default: strict (no G or B may exceed R). "
        "Set soft_tolerance.B > 0 to allow warm-neutral bridge colours."
    ),
}

# Default tolerance when key is missing from config
_DEFAULT_TOLERANCE: Dict[str, int] = {"G": 0, "B": 0}


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
        If the file does not exist, falls back to the built-in CHAR-M strict config.

    Returns
    -------
    dict with keys:
        warm_prefixes  : list[str]          — prefix codes to check
        soft_tolerance : dict[str, int]     — {"G": int, "B": int} per-channel tolerance
        description    : str                — human-readable description (optional)
    """
    config_path = path if path is not None else DEFAULT_CONFIG_PATH

    try:
        with open(config_path, "r", encoding="utf-8") as fh:
            cfg = json.load(fh)
    except FileNotFoundError:
        return dict(_BUILTIN_CONFIG)
    except (json.JSONDecodeError, OSError) as exc:
        sys.stderr.write(
            f"[warmth_lint] WARNING: Could not read config '{config_path}': {exc}\n"
            f"[warmth_lint] Falling back to built-in CHAR-M strict config.\n"
        )
        return dict(_BUILTIN_CONFIG)

    # Validate and normalise warm_prefixes
    if "warm_prefixes" not in cfg or not isinstance(cfg["warm_prefixes"], list):
        sys.stderr.write(
            f"[warmth_lint] WARNING: Config '{config_path}' missing 'warm_prefixes' list.\n"
            f"[warmth_lint] Falling back to built-in CHAR-M strict config.\n"
        )
        return dict(_BUILTIN_CONFIG)

    cfg["warm_prefixes"] = [str(p).strip().upper() for p in cfg["warm_prefixes"] if p]

    # Validate and normalise soft_tolerance (optional key)
    raw_tol = cfg.get("soft_tolerance", {})
    if not isinstance(raw_tol, dict):
        sys.stderr.write(
            f"[warmth_lint] WARNING: 'soft_tolerance' must be a dict. Using strict defaults.\n"
        )
        raw_tol = {}
    tolerance: Dict[str, int] = {
        "G": max(0, int(raw_tol.get("G", _DEFAULT_TOLERANCE["G"]))),
        "B": max(0, int(raw_tol.get("B", _DEFAULT_TOLERANCE["B"]))),
    }
    cfg["soft_tolerance"] = tolerance

    return cfg


# ---------------------------------------------------------------------------
# Regex pattern builder  (unchanged from v002)
# ---------------------------------------------------------------------------

def _build_table_row_re(prefixes: List[str]) -> re.Pattern:
    """
    Build a compiled regex that matches table rows for ANY of the given prefixes.

    Groups:
      1: code    e.g. "CHAR-M-03"
      2: name    e.g. "Miri Skin Highlight"
      3: hex     e.g. "#A86A40"
      4: r_str   e.g. "168"
      5: g_str   e.g. "106"
      6: b_str   e.g. "64"
    """
    escaped = [re.escape(p) for p in prefixes]
    prefix_alternation = "|".join(escaped)
    code_pattern = rf"(?:{prefix_alternation})-\d+"

    pattern = (
        rf'\|\s*({code_pattern})\s*\|\s*([^|]+?)\s*\|\s*`(#[0-9A-Fa-f]{{6}})`\s*\|\s*'
        rf'\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*\|'
    )
    return re.compile(pattern, re.IGNORECASE)


# ---------------------------------------------------------------------------
# Core logic — updated for soft tolerance
# ---------------------------------------------------------------------------

def _check_rgb(
    r: int, g: int, b: int,
    tolerance: Optional[Dict[str, int]] = None,
) -> Tuple[List[str], Dict[str, int]]:
    """
    Return (violation_strings, margin_dict) for the given (R, G, B).

    tolerance : dict with keys "G" and "B" (integers >= 0).
                G violation iff G - R > tolerance["G"]
                B violation iff B - R > tolerance["B"]
                Default: strict ({"G": 0, "B": 0}).

    margin_dict : {"G": G - R, "B": B - R} — positive = exceeds R by that amount.
    """
    if tolerance is None:
        tolerance = _DEFAULT_TOLERANCE

    tol_g = tolerance.get("G", 0)
    tol_b = tolerance.get("B", 0)

    violations: List[str] = []
    margin_g = g - r   # positive if G exceeds R
    margin_b = b - r   # positive if B exceeds R

    if margin_g > tol_g:
        violations.append(
            f"G > R by {margin_g} (tolerance={tol_g})"
        )
    if margin_b > tol_b:
        violations.append(
            f"B > R by {margin_b} (tolerance={tol_b})"
        )

    return violations, {"G": margin_g, "B": margin_b}


def _hex_to_rgb(hex_str: str) -> Optional[Tuple[int, int, int]]:
    """Parse '#RRGGBB' → (R, G, B). Returns None if parse fails."""
    h = hex_str.lstrip('#')
    if len(h) != 6:
        return None
    try:
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

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
    source_name : str  — display name for the source
    config      : dict or None — from load_config(); if None, calls load_config().

    Returns
    -------
    dict with keys:
        result            : "PASS" | "WARN"
        source            : str
        total_checked     : int
        total_violations  : int
        violations        : list[dict]  — each has: code, name, hex, rgb, reason, margin, source
        prefixes_checked  : list[str]
        tolerance_used    : dict[str, int]  — {"G": int, "B": int}
    """
    if config is None:
        config = load_config()

    prefixes = config.get("warm_prefixes", ["CHAR-M"])
    if not prefixes:
        prefixes = ["CHAR-M"]

    tolerance = config.get("soft_tolerance", _DEFAULT_TOLERANCE)

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
            continue
        seen_codes.add(code)
        total_checked += 1

        channel_violations, margin = _check_rgb(r, g, b, tolerance=tolerance)
        if channel_violations:
            violations.append({
                "code": code,
                "name": name,
                "hex": hex_val,
                "rgb": (r, g, b),
                "reason": " | ".join(channel_violations),
                "margin": margin,
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
        "tolerance_used": dict(tolerance),
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
            "tolerance_used": _DEFAULT_TOLERANCE,
            "error": str(exc),
        }
    return lint_palette_text(text, source_name=path, config=config)


def format_report(
    results: Union[Dict, List[Dict]],
    config: Optional[Dict] = None,
) -> str:
    """
    Format one or multiple lint result dicts as a human-readable report string.

    Accepts either a single dict (from lint_palette_file) or a list of dicts.
    """
    if isinstance(results, dict):
        results = [results]

    # Collect active prefixes and tolerance for the header
    all_prefixes: List[str] = []
    tolerance_display: Dict[str, int] = _DEFAULT_TOLERANCE
    for r in results:
        for p in r.get("prefixes_checked", []):
            if p not in all_prefixes:
                all_prefixes.append(p)
        if "tolerance_used" in r:
            tolerance_display = r["tolerance_used"]
    if not all_prefixes and config:
        all_prefixes = config.get("warm_prefixes", ["CHAR-M"])
    if not all_prefixes:
        all_prefixes = ["CHAR-M"]

    mode_str = (
        "strict"
        if tolerance_display.get("G", 0) == 0 and tolerance_display.get("B", 0) == 0
        else f"soft (G±{tolerance_display.get('G', 0)}, B±{tolerance_display.get('B', 0)})"
    )

    lines = []
    lines.append("=" * 60)
    lines.append("LTG Warmth Compliance Lint Report")
    lines.append(f"Prefixes checked: {', '.join(all_prefixes)}")
    lines.append(f"Mode: {mode_str}")
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
        tol_this = r.get("tolerance_used", _DEFAULT_TOLERANCE)
        status_tag = f"[{r['result']}]"
        lines.append(f"\n{status_tag} {r['source']}")
        lines.append(f"  Prefixes checked        : {', '.join(prefixes_this)}")
        lines.append(f"  Soft tolerance          : G±{tol_this.get('G', 0)}, B±{tol_this.get('B', 0)}")
        lines.append(f"  Matching entries checked: {r['total_checked']}")
        lines.append(f"  Violations              : {r['total_violations']}")

        if r["violations"]:
            lines.append("")
            for v in r["violations"]:
                margin = v.get("margin", {})
                lines.append(f"  FAIL  {v['code']} — {v['name']}")
                lines.append(f"        Hex: {v['hex']}  RGB: {v['rgb']}")
                lines.append(f"        Reason: {v['reason']}")
                lines.append(
                    f"        Margin: G−R={margin.get('G', '?'):+d}, B−R={margin.get('B', '?'):+d}"
                )
                lines.append(
                    f"        Fix: R must be >= G and R >= B "
                    f"(within tolerance) for all {', '.join(prefixes_this)} entries"
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
    """CLI entry point. Returns exit code: 0 = pass, 1 = violations found, 2 = usage error."""
    if argv is None:
        argv = sys.argv[1:]

    config_path: Optional[str] = None
    palette_paths: List[str] = []
    force_strict: bool = False

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
        elif arg == "--strict":
            force_strict = True
        else:
            palette_paths.append(arg)
        i += 1

    config = load_config(config_path)

    # --strict flag overrides any config-defined tolerance
    if force_strict:
        config["soft_tolerance"] = {"G": 0, "B": 0}

    if not palette_paths:
        palette_paths = [DEFAULT_PALETTE_PATH]

    results = [lint_palette_file(p, config=config) for p in palette_paths]
    report = format_report(results, config=config)
    print(report)

    total_violations = sum(r.get("total_violations", 0) for r in results)
    return 1 if total_violations > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
