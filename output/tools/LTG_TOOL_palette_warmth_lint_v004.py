"""
LTG_TOOL_palette_warmth_lint_v004.py
======================================
Warmth compliance linter for "Luma & the Glitchkin" palette entries.

CHANGES FROM v003
-----------------
v004 (Cycle 36 — 2026-03-30):
  - Per-world warm/cool threshold mode via --world-type flag.
    Accepted values: REAL, OTHER_SIDE, GLITCH  (case-insensitive).
    When --world-type is provided, the linter applies an additional
    warm/cool threshold check against the "world_presets" config.
  - Auto-inference of world type from generator filename:
    * SF01/sf01 / "discovery" keyword             → REAL
    * SF02/sf02 / "glitch_storm" / "storm"        → REAL  (warm window accents permitted)
    * SF04/sf04 / "classroom" / "kitchen" /
      "hallway" / "tech_den" / "main_street" /
      "millbrook" / "grandma"                     → REAL
    * SF03/sf03 / "other_side" / "otherside"      → OTHER_SIDE
    * "glitch_layer" / "glitch_encounter" /
      "glitch_world"                              → GLITCH
    Unknown filenames: world-type = None (warmth check only, no threshold check).
  - New function: infer_world_type(filename_or_path) → "REAL"|"OTHER_SIDE"|"GLITCH"|None
  - World-type threshold check is ADVISORY (WARN, not FAIL) when warm-cold ratio is
    outside the expected range for that world type.
  - format_report() now includes world-type section when world_type is set.
  - CLI --world-type flag; also auto-applied when linting a file whose name is
    inferrable (can be suppressed with --no-auto-world-type).
  - CHAR-L hoodie warmth guarantee expanded: warm_prefixes now includes "CHAR-L".
    Only CHAR-L hoodie entries appear in table format (CHAR-L-04, CHAR-L-08, CHAR-L-11);
    other CHAR-L entries (skin, jeans, shoes) are prose-format only and are NOT matched
    by the table-row regex. This is intentional by design — jeans are blue (B>R).
    See master_palette.md "CHAR-L Hoodie Warmth Guarantee Table" (Cycle 36 addition).
  - ltg_warmth_guarantees.json is the primary config file (takes priority over
    warmth_lint_config.json). Contains world_presets + expanded warm_prefixes.
  - All v003 functionality (soft_tolerance, --strict, config file) preserved unchanged.
  - Actioned from C36 inbox: 20260330_0900_c36_warmth_lint.md

v003 (Cycle 35 — 2026-03-29):
  - Soft-tolerance mode via "soft_tolerance" JSON config key.

v002 (Cycle 34 — 2026-03-29):
  - Configurable character prefix list via JSON config file.

v001 (Cycle 33 — 2026-03-29):
  - Original CHAR-M-only warmth linter.

PURPOSE
-------
Two complementary checks:

1. Per-character warmth guarantee (inherited from v003):
   Every palette entry for warm-guaranteed characters (CHAR-M by default) must have
   R as the dominant channel (within configured soft tolerance).

2. Per-world warm/cool threshold (NEW in v004):
   For a given generator or style frame, the overall warm tone presence in the
   rendered image should match the expected world archetype:
     REAL         → warm/cool threshold >= 12  (lamp-lit interiors, warm windows)
     OTHER_SIDE   → warm/cool threshold ~  0   (cold/digital, zero warm)
     GLITCH       → warm/cool threshold =  0   (warm presence is a FAIL)
   Note: This check operates on the PALETTE ENTRIES in the master_palette.md,
   not on rendered pixel data. It flags whether the palette doc contains entries
   consistent with the world type.

CONFIG FILE: warmth_lint_config.json (v004 compatible — same as v003)
----------------------------------------------------------------------
{
  "warm_prefixes": ["CHAR-M"],
  "soft_tolerance": {"G": 0, "B": 0},
  "world_presets": {
    "REAL":       {"warm_cool_threshold": 12, "note": "..."},
    "OTHER_SIDE": {"warm_cool_threshold": 0,  "note": "..."},
    "GLITCH":     {"warm_cool_threshold": 0,  "note": "..."}
  }
}

Reads world_presets from config if present; falls back to built-in defaults.

WORLD-TYPE AUTO-INFERENCE
--------------------------
infer_world_type("LTG_TOOL_styleframe_discovery_v004.py") → "REAL"
infer_world_type("LTG_TOOL_style_frame_03_other_side_v003.py") → "OTHER_SIDE"
infer_world_type("LTG_TOOL_bg_glitch_layer_encounter_v001.py") → "GLITCH"
infer_world_type("LTG_TOOL_grandma_miri_expression_sheet_v003.py") → "REAL"
infer_world_type("LTG_TOOL_cosmo_turnaround_v002.py") → None  (no world context)

USAGE (standalone CLI)
----------------------
    python LTG_TOOL_palette_warmth_lint_v004.py
    python LTG_TOOL_palette_warmth_lint_v004.py path/to/master_palette.md
    python LTG_TOOL_palette_warmth_lint_v004.py --config path/to/config.json palette.md
    python LTG_TOOL_palette_warmth_lint_v004.py --strict palette.md
    python LTG_TOOL_palette_warmth_lint_v004.py --world-type REAL palette.md
    python LTG_TOOL_palette_warmth_lint_v004.py --world-type OTHER_SIDE palette.md
    python LTG_TOOL_palette_warmth_lint_v004.py --infer-world-type generator.py palette.md
    python LTG_TOOL_palette_warmth_lint_v004.py --no-auto-world-type palette.md

PROGRAMMATIC API
----------------
    from LTG_TOOL_palette_warmth_lint_v004 import (
        lint_palette_file,
        lint_palette_text,
        format_report,
        load_config,
        infer_world_type,
        DEFAULT_PALETTE_PATH,
        DEFAULT_CONFIG_PATH,
        DEFAULT_GUARANTEES_PATH,
    )

    # Basic usage — loads ltg_warmth_guarantees.json (CHAR-M + CHAR-L):
    config = load_config()
    results = lint_palette_file("output/color/palettes/master_palette.md", config=config)

    # With world-type:
    results = lint_palette_file(
        "output/color/palettes/master_palette.md",
        config=config,
        world_type="REAL",
    )

    # Auto-infer from generator path:
    world_type = infer_world_type("LTG_TOOL_styleframe_discovery_v004.py")
    results = lint_palette_file(palette_path, config=config, world_type=world_type)

    # CI: get warm_cool_threshold for a world type
    # python LTG_TOOL_palette_warmth_lint_v004.py --world-type GLITCH --world-threshold-only
    # (prints threshold integer to stdout)

Author: Kai Nakamura (Tech Art Engineer) — coordinating with Sam Kowalski (Color & Style)
Version: 4.0.0
Cycle: 36 — 2026-03-30

Design note: Operates entirely on markdown source text — no Pillow dependency.
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

DEFAULT_GUARANTEES_PATH = os.path.normpath(
    os.path.join(_HERE, "ltg_warmth_guarantees.json")
)

# Built-in fallback config
_BUILTIN_CONFIG: Dict = {
    "warm_prefixes": ["CHAR-M", "CHAR-L"],
    "soft_tolerance": {"G": 0, "B": 0},
    "description": (
        "Characters whose palette entries must be unambiguously warm "
        "(R dominant). CHAR-M = Grandma Miri (all entries). "
        "CHAR-L = Luma hoodie entries ONLY (CHAR-L-04, CHAR-L-08, CHAR-L-11) — "
        "these are the only CHAR-L entries in table format; skin/jeans/shoes "
        "are prose-format only and are intentionally excluded. "
        "Default: strict (no G or B may exceed R). "
        "Set soft_tolerance.B > 0 to allow warm-neutral bridge colours."
    ),
}

# Default tolerance when key is missing from config
_DEFAULT_TOLERANCE: Dict[str, int] = {"G": 0, "B": 0}

# ── Built-in world presets ──────────────────────────────────────────────────
# These mirror the world_presets block in warmth_lint_config.json.
# The config file values take precedence if present.

_BUILTIN_WORLD_PRESETS: Dict[str, Dict] = {
    "REAL": {
        "warm_cool_threshold": 12,
        "note": (
            "Lamp-lit warm interior / daytime exterior. Warm presence expected. "
            "SF01/SF04 archetypes. Real-world environments (not storm)."
        ),
    },
    "REAL_STORM": {
        "warm_cool_threshold": 6,
        "note": (
            "Contested real-world storm scene (SF02 archetype). Cool sky dominant; "
            "warm tones present only as subdued window glow accents (alpha 110–115). "
            "Threshold 6 (not 12) reflects intentional cool-dominant palette. "
            "Kai Nakamura C39: split from REAL to prevent persistent false WARNs on SF02."
        ),
    },
    "OTHER_SIDE": {
        "warm_cool_threshold": 0,
        "note": (
            "Digital CRT world — cold dominant, zero warm tones. SF03 archetype. "
            "Any warm entry in the palette for this world context is advisory."
        ),
    },
    "GLITCH": {
        "warm_cool_threshold": 0,
        "note": (
            "Glitch Layer / Glitch World — warm tones are PROHIBITED. "
            "Near-zero warm/cool ratio is CORRECT. "
            "Warm presence (not absence) would be a FAIL."
        ),
    },
}

VALID_WORLD_TYPES = frozenset(_BUILTIN_WORLD_PRESETS.keys())


# ---------------------------------------------------------------------------
# World-type auto-inference
# ---------------------------------------------------------------------------

# Inference rules: list of (regex_pattern, world_type_string)
# Evaluated in order; first match wins.
_WORLD_INFERENCE_RULES: List[Tuple[re.Pattern, str]] = [
    # OTHER_SIDE (SF03 / "other side" / CRT world interior)
    (re.compile(
        r'(sf03|other[_\-]?side|otherside|crt[_\-]?world)',
        re.IGNORECASE,
    ), "OTHER_SIDE"),

    # GLITCH world environments
    (re.compile(
        r'(glitch[_\-]?layer|glitch[_\-]?encounter|glitch[_\-]?world)',
        re.IGNORECASE,
    ), "GLITCH"),

    # REAL_STORM — SF02 / glitch_storm (contested real-world storm; cool-dominant palette)
    # Split from REAL in C39: warm/cool threshold 6 (not 12) for storm scenes.
    (re.compile(
        r'(sf02|glitch[_\-]?storm|style[_\-]?frame[_\-]?02)',
        re.IGNORECASE,
    ), "REAL_STORM"),

    # REAL — SF01/SF04 style frames (explicitly named; excludes SF02 — handled above)
    (re.compile(
        r'(sf01|sf04|discovery|style[_\-]?frame[_\-]?0[14])',
        re.IGNORECASE,
    ), "REAL"),

    # REAL — Real-world environment backgrounds (interiors/exteriors)
    (re.compile(
        r'(classroom|kitchen|hallway|tech[_\-]?den|main[_\-]?street|'
        r'millbrook|grandma|luma[_\-]?house|backyard)',
        re.IGNORECASE,
    ), "REAL"),

    # REAL — Any "act" scene or general "bg" that is NOT glitch/otherside
    (re.compile(
        r'(scene|interior|exterior|daytime|night[_\-]?street)',
        re.IGNORECASE,
    ), "REAL"),
]


def infer_world_type(filename_or_path: str) -> Optional[str]:
    """
    Infer the world type (REAL | OTHER_SIDE | GLITCH) from a generator filename or path.

    Parameters
    ----------
    filename_or_path : str
        File path or basename of a generator script (e.g. LTG_TOOL_styleframe_discovery_v004.py).

    Returns
    -------
    str | None
        "REAL", "OTHER_SIDE", or "GLITCH" if the filename matches a known pattern.
        None if the world context cannot be inferred (e.g. character sheet, logo, abstract tool).

    Examples
    --------
    >>> infer_world_type("LTG_TOOL_styleframe_discovery_v004.py")
    'REAL'
    >>> infer_world_type("LTG_TOOL_style_frame_03_other_side_v003.py")
    'OTHER_SIDE'
    >>> infer_world_type("LTG_TOOL_bg_glitch_layer_encounter_v001.py")
    'GLITCH'
    >>> infer_world_type("LTG_TOOL_luma_expression_sheet_v007.py")
    None
    """
    basename = os.path.basename(filename_or_path)
    for pattern, world_type in _WORLD_INFERENCE_RULES:
        if pattern.search(basename):
            return world_type
    return None


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

def load_config(path: Optional[str] = None) -> Dict:
    """
    Load the warmth lint config from a JSON file.

    Priority order (v004):
      1. ltg_warmth_guarantees.json (DEFAULT_GUARANTEES_PATH) — preferred
      2. warmth_lint_config.json (DEFAULT_CONFIG_PATH or path arg) — legacy fallback
      3. Built-in config (_BUILTIN_CONFIG) — last resort

    Parameters
    ----------
    path : str or None
        Path to a config JSON file. If None, tries DEFAULT_GUARANTEES_PATH first,
        then DEFAULT_CONFIG_PATH. If a path is explicitly provided, it is used
        directly (no guarantees-file priority override).

    Returns
    -------
    dict with keys:
        warm_prefixes  : list[str]          — prefix codes to check
        soft_tolerance : dict[str, int]     — {"G": int, "B": int}
        description    : str                — human-readable description (optional)
        world_presets  : dict               — per-world threshold config
    """
    # When no explicit path given, try ltg_warmth_guarantees.json first
    if path is None:
        for candidate in [DEFAULT_GUARANTEES_PATH, DEFAULT_CONFIG_PATH]:
            try:
                with open(candidate, "r", encoding="utf-8") as fh:
                    cfg = json.load(fh)
                break
            except FileNotFoundError:
                continue
            except (json.JSONDecodeError, OSError) as exc:
                sys.stderr.write(
                    f"[warmth_lint] WARNING: Could not read '{candidate}': {exc}\n"
                )
                continue
        else:
            # Both files missing/unreadable — use built-in
            return dict(_BUILTIN_CONFIG)
    else:
        config_path = path
        try:
            with open(config_path, "r", encoding="utf-8") as fh:
                cfg = json.load(fh)
        except FileNotFoundError:
            return dict(_BUILTIN_CONFIG)
        except (json.JSONDecodeError, OSError) as exc:
            sys.stderr.write(
                f"[warmth_lint] WARNING: Could not read config '{config_path}': {exc}\n"
                f"[warmth_lint] Falling back to built-in config.\n"
            )
            return dict(_BUILTIN_CONFIG)

    # Validate and normalise warm_prefixes
    if "warm_prefixes" not in cfg or not isinstance(cfg["warm_prefixes"], list):
        sys.stderr.write(
            f"[warmth_lint] WARNING: Config missing 'warm_prefixes' list.\n"
            f"[warmth_lint] Falling back to built-in config.\n"
        )
        return dict(_BUILTIN_CONFIG)

    cfg["warm_prefixes"] = [str(p).strip().upper() for p in cfg["warm_prefixes"] if p]

    # Validate and normalise soft_tolerance (optional key)
    raw_tol = cfg.get("soft_tolerance", {})
    if not isinstance(raw_tol, dict):
        raw_tol = {}
    tolerance: Dict[str, int] = {
        "G": max(0, int(raw_tol.get("G", _DEFAULT_TOLERANCE["G"]))),
        "B": max(0, int(raw_tol.get("B", _DEFAULT_TOLERANCE["B"]))),
    }
    cfg["soft_tolerance"] = tolerance

    # Normalise world_presets if present — merge with built-in defaults
    raw_presets = cfg.get("world_presets", {})
    if isinstance(raw_presets, dict):
        merged = dict(_BUILTIN_WORLD_PRESETS)
        for key, val in raw_presets.items():
            k = key.upper()
            if isinstance(val, dict):
                merged[k] = val
        cfg["world_presets"] = merged
    else:
        cfg["world_presets"] = dict(_BUILTIN_WORLD_PRESETS)

    return cfg


# ---------------------------------------------------------------------------
# Regex pattern builder  (unchanged from v002/v003)
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
# Core warmth check (per-channel, unchanged from v003)
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
    margin_g = g - r
    margin_b = b - r

    if margin_g > tol_g:
        violations.append(f"G > R by {margin_g} (tolerance={tol_g})")
    if margin_b > tol_b:
        violations.append(f"B > R by {margin_b} (tolerance={tol_b})")

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
# World-type threshold analysis (NEW in v004)
# ---------------------------------------------------------------------------

def _analyse_world_warmth(
    entries: List[Dict],
    world_type: str,
    config: Dict,
) -> Dict:
    """
    Analyse the palette entries for world-type warm/cool consistency.

    Parameters
    ----------
    entries    : list of dicts — parsed palette entries (code, name, hex, rgb)
    world_type : "REAL" | "OTHER_SIDE" | "GLITCH"
    config     : loaded config dict (contains world_presets)

    Returns
    -------
    dict:
        world_type         : str
        threshold          : int   — expected warm_cool_threshold from config
        warm_entries       : int   — entries with R dominant (R >= G and R >= B)
        cool_entries       : int   — entries with G or B dominant
        warm_ratio_pct     : float — warm_entries / total * 100
        threshold_met      : bool  — True if warm_ratio_pct >= threshold (for REAL)
                                     or warm_ratio_pct == 0 (for OTHER_SIDE/GLITCH)
        advisory_warnings  : list[str]
        note               : str   — human-readable world preset note
    """
    presets = config.get("world_presets", _BUILTIN_WORLD_PRESETS)
    preset  = presets.get(world_type.upper(), _BUILTIN_WORLD_PRESETS.get(world_type.upper(), {}))
    threshold = preset.get("warm_cool_threshold", 0)
    note      = preset.get("note", "")

    # We classify each entry against the full palette — using all parsed entries
    # (not just warm-guaranteed characters) for a holistic world-warmth picture.
    total  = len(entries)
    warm_count = 0
    cool_count = 0

    for entry in entries:
        r, g, b = entry["rgb"]
        if r >= g and r >= b:
            warm_count += 1
        else:
            cool_count += 1

    warm_ratio = (warm_count / total * 100) if total > 0 else 0.0
    advisory = []

    wt = world_type.upper()
    if wt == "REAL":
        # Expect warm_ratio >= threshold
        threshold_met = warm_ratio >= threshold
        if not threshold_met:
            advisory.append(
                f"REAL world expected warm ratio ≥ {threshold:.0f}%; "
                f"found {warm_ratio:.1f}% ({warm_count}/{total} entries warm). "
                f"Consider whether warm palette entries are adequately represented."
            )
    elif wt in ("OTHER_SIDE", "GLITCH"):
        # Expect warm_ratio == 0 (or very low)
        threshold_met = warm_ratio == 0
        if warm_count > 0:
            advisory.append(
                f"{wt} world should have 0 warm entries; "
                f"found {warm_count}/{total} warm entries ({warm_ratio:.1f}%). "
                f"Check whether any REAL-world warm colours have leaked into this world's palette."
            )
    else:
        threshold_met = True  # Unknown world type — no advisory

    return {
        "world_type": world_type.upper(),
        "threshold": threshold,
        "warm_entries": warm_count,
        "cool_entries": cool_count,
        "total_entries": total,
        "warm_ratio_pct": warm_ratio,
        "threshold_met": threshold_met,
        "advisory_warnings": advisory,
        "note": note,
    }


# ---------------------------------------------------------------------------
# Palette entry parser (for world-type analysis)
# ---------------------------------------------------------------------------

def _parse_all_palette_entries(text: str) -> List[Dict]:
    """
    Parse all palette table rows from the markdown (any code prefix).
    Used for world-type warmth analysis (needs the full palette picture).

    Returns list of dicts: {code, name, hex, rgb: (r,g,b)}
    """
    # Match any table row with a hex code and RGB triple
    row_re = re.compile(
        r'\|\s*([A-Z0-9\-]+)\s*\|\s*([^|]+?)\s*\|\s*`(#[0-9A-Fa-f]{6})`\s*\|\s*'
        r'\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*\|',
        re.IGNORECASE,
    )
    entries = []
    seen = set()
    for m in row_re.finditer(text):
        code = m.group(1).upper()
        if code in seen:
            continue
        seen.add(code)
        entries.append({
            "code": code,
            "name": m.group(2).strip(),
            "hex": m.group(3).upper(),
            "rgb": (int(m.group(4)), int(m.group(5)), int(m.group(6))),
        })
    return entries


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def lint_palette_text(
    text: str,
    source_name: str = "<text>",
    config: Optional[Dict] = None,
    world_type: Optional[str] = None,
) -> Dict:
    """
    Lint the given palette markdown text for warmth violations.

    Parameters
    ----------
    text        : str  — full markdown text of the palette document
    source_name : str  — display name for the source
    config      : dict or None — from load_config(); if None, calls load_config().
    world_type  : str | None  — "REAL", "OTHER_SIDE", or "GLITCH".
                                If provided, adds world-type warmth analysis
                                (advisory only — does not change result/violations).

    Returns
    -------
    dict with keys:
        result            : "PASS" | "WARN"
        source            : str
        total_checked     : int
        total_violations  : int
        violations        : list[dict]  — each has: code, name, hex, rgb, reason, margin, source
        prefixes_checked  : list[str]
        tolerance_used    : dict[str, int]
        world_analysis    : dict | None  — populated only when world_type is provided
    """
    if config is None:
        config = load_config()

    prefixes = config.get("warm_prefixes", ["CHAR-M"])
    if not prefixes:
        prefixes = ["CHAR-M"]

    tolerance = config.get("soft_tolerance", _DEFAULT_TOLERANCE)

    # ── Per-character warmth check (v003 logic, unchanged) ─────────────────
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

    # ── Per-world warmth analysis (v004 addition) ──────────────────────────
    world_analysis = None
    if world_type is not None:
        wt_upper = world_type.upper()
        if wt_upper not in VALID_WORLD_TYPES:
            sys.stderr.write(
                f"[warmth_lint] WARNING: Unknown world_type '{world_type}'. "
                f"Valid: {sorted(VALID_WORLD_TYPES)}. World analysis skipped.\n"
            )
        else:
            all_entries = _parse_all_palette_entries(text)
            world_analysis = _analyse_world_warmth(all_entries, wt_upper, config)

    return {
        "result": result,
        "source": source_name,
        "total_checked": total_checked,
        "total_violations": len(violations),
        "violations": violations,
        "prefixes_checked": list(prefixes),
        "tolerance_used": dict(tolerance),
        "world_analysis": world_analysis,
    }


def lint_palette_file(
    path: str,
    config: Optional[Dict] = None,
    world_type: Optional[str] = None,
) -> Dict:
    """
    Lint a palette markdown file. Returns the same dict as lint_palette_text().
    If the file cannot be read, returns a result dict with result="ERROR".

    Parameters
    ----------
    path       : str  — path to the palette markdown file
    config     : dict | None  — from load_config()
    world_type : str | None   — "REAL", "OTHER_SIDE", or "GLITCH"
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
            "world_analysis": None,
            "error": str(exc),
        }
    return lint_palette_text(text, source_name=path, config=config, world_type=world_type)


def format_report(
    results: Union[Dict, List[Dict]],
    config: Optional[Dict] = None,
) -> str:
    """
    Format one or multiple lint result dicts as a human-readable report string.

    Accepts either a single dict (from lint_palette_file) or a list of dicts.
    Includes world-type section when world_analysis is present.
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
    lines.append("LTG Warmth Compliance Lint Report — v4.0.0")
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

        # ── World-type section (v004) ──────────────────────────────────────
        wa = r.get("world_analysis")
        if wa is not None:
            lines.append("")
            lines.append(f"  World-Type Analysis: {wa['world_type']}")
            lines.append(f"  {wa.get('note', '')}")
            lines.append(
                f"  Warm entries: {wa['warm_entries']}/{wa['total_entries']} "
                f"({wa['warm_ratio_pct']:.1f}%)  "
                f"Expected warm_cool_threshold: {wa['threshold']}%"
            )
            threshold_met = wa.get("threshold_met", True)
            lines.append(f"  Threshold met: {'YES' if threshold_met else 'ADVISORY — see below'}")
            for advisory in wa.get("advisory_warnings", []):
                lines.append(f"  ADVISORY: {advisory}")

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
    world_type: Optional[str] = None
    infer_from_path: Optional[str] = None
    auto_world_type: bool = True   # auto-infer from palette filename by default
    world_threshold_only: bool = False  # CI mode: print threshold int and exit

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
        elif arg == "--world-type":
            i += 1
            if i < len(argv):
                world_type = argv[i].upper()
                if world_type not in VALID_WORLD_TYPES:
                    sys.stderr.write(
                        f"[warmth_lint] ERROR: --world-type must be one of "
                        f"{sorted(VALID_WORLD_TYPES)}, got '{world_type}'\n"
                    )
                    return 2
            else:
                sys.stderr.write("[warmth_lint] ERROR: --world-type requires a value\n")
                return 2
        elif arg == "--world-threshold-only":
            # CI mode: print warm_cool_threshold for the given --world-type and exit
            world_threshold_only = True
        elif arg == "--infer-world-type":
            i += 1
            if i < len(argv):
                infer_from_path = argv[i]
            else:
                sys.stderr.write("[warmth_lint] ERROR: --infer-world-type requires a file path\n")
                return 2
        elif arg == "--no-auto-world-type":
            auto_world_type = False
        else:
            palette_paths.append(arg)
        i += 1

    config = load_config(config_path)

    if force_strict:
        config["soft_tolerance"] = {"G": 0, "B": 0}

    # --world-threshold-only: CI mode — print the threshold integer and exit
    if world_threshold_only:
        if world_type is None:
            sys.stderr.write(
                "[warmth_lint] ERROR: --world-threshold-only requires --world-type "
                "(e.g. --world-type GLITCH --world-threshold-only)\n"
            )
            return 2
        presets = config.get("world_presets", _BUILTIN_WORLD_PRESETS)
        preset = presets.get(world_type)
        if preset is None:
            sys.stderr.write(
                f"[warmth_lint] ERROR: Unknown world type '{world_type}'. "
                f"Valid: {sorted(VALID_WORLD_TYPES)}\n"
            )
            return 2
        # Print only the integer — suitable for shell variable capture:
        # THRESH=$(python LTG_TOOL_palette_warmth_lint_v004.py --world-type GLITCH --world-threshold-only)
        print(preset.get("warm_cool_threshold", 0))
        return 0

    if not palette_paths:
        palette_paths = [DEFAULT_PALETTE_PATH]

    # Determine effective world type
    effective_world_type = world_type  # explicit flag wins

    if effective_world_type is None and infer_from_path:
        inferred = infer_world_type(infer_from_path)
        if inferred:
            effective_world_type = inferred
            sys.stderr.write(
                f"[warmth_lint] Auto-inferred world type '{inferred}' "
                f"from '{os.path.basename(infer_from_path)}'\n"
            )
        else:
            sys.stderr.write(
                f"[warmth_lint] Could not infer world type from "
                f"'{os.path.basename(infer_from_path)}' — world-type check skipped.\n"
            )

    # Auto-infer from palette path itself if it contains world hints
    if effective_world_type is None and auto_world_type and len(palette_paths) == 1:
        inferred = infer_world_type(palette_paths[0])
        if inferred:
            effective_world_type = inferred
            sys.stderr.write(
                f"[warmth_lint] Auto-inferred world type '{inferred}' "
                f"from palette path '{os.path.basename(palette_paths[0])}'\n"
            )

    results = [
        lint_palette_file(p, config=config, world_type=effective_world_type)
        for p in palette_paths
    ]
    report = format_report(results, config=config)
    print(report)

    total_violations = sum(r.get("total_violations", 0) for r in results)
    return 1 if total_violations > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
