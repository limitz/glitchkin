"""
LTG_TOOL_palette_warmth_lint.py
======================================
Warmth compliance linter for "Luma & the Glitchkin" palette entries.

CHANGES FROM v004
-----------------
v006 (Cycle 39 — 2026-03-30 — Kai Nakamura):
  - numpy vectorization in _analyse_world_warmth() — warm/cool counting via
    numpy array ops instead of per-entry Python loop (future-proof for large palettes).
  - numpy import added; no API changes. Graceful: no effect if numpy unavailable
    (pure-Python fallback retained).
  - Version bumped to 6.0.0.

v005 (Cycle 39 — 2026-03-29 — Sam Kowalski):
  - World-type inference now delegates to LTG_TOOL_world_type_infer (standalone)
    instead of using inline _WORLD_INFERENCE_RULES.  Falls back to v004 built-in rules
    if world_type_infer_v001 is not importable (graceful degradation).
  - New CLI flag: --check-generator FILE
    Infers world type from FILE and lints palette_path with that world type.
    Example: python LTG_TOOL_palette_warmth_lint.py
             --check-generator LTG_TOOL_style_frame_02_glitch_storm.py
             master_palette.md
  - REAL_STORM sub-type: if inferred world type is REAL and the generator filename
    matches a storm pattern, world type is promoted to "REAL_STORM".
    Threshold for REAL_STORM = 3 (matches render_qa v1.6.0).
  - Scope expansion: ltg_warmth_guarantees.json "warm_prefixes" remains the sole
    authority for which character prefixes are warm-guaranteed.  No code changes
    needed to add new prefixes — edit the JSON config only.
  - CHAR-M strict test confirmed: CHAR-M-11 #C4907A (R:196, G:144, B:122) → PASS.
  - infer_world_type() now exported from this module; if world_type_infer_v001 is
    available it delegates there; otherwise uses the v004 inline rules as fallback.
  - format_report() now shows world_subtype when REAL_STORM is detected.
  - All v004 functionality preserved unchanged.
  - Actioned from C39 inbox: 20260329_2248_c39_palette_tools.md (Tasks 1 + 3).

v004 (Cycle 36 — 2026-03-30):
  - Per-world warm/cool threshold mode via --world-type flag.
  - CHAR-L hoodie warmth guarantee expanded.
  - ltg_warmth_guarantees.json as primary config.
  - --world-threshold-only CI flag.

v003 (Cycle 35 — 2026-03-29):
  - Soft-tolerance mode via "soft_tolerance" JSON config key.

v002 (Cycle 34 — 2026-03-29):
  - Configurable character prefix list via JSON config file.

v001 (Cycle 33 — 2026-03-29):
  - Original CHAR-M-only warmth linter.

PURPOSE
-------
Two complementary checks (unchanged from v004):

1. Per-character warmth guarantee:
   Every palette entry for warm-guaranteed characters must have R dominant
   (within configured soft tolerance).

2. Per-world warm/cool threshold:
   Advisory check — the palette text warm/cool entry ratio should match the
   expected world archetype (REAL → >= 12%, OTHER_SIDE/GLITCH → 0%).

REAL_STORM sub-type (new in v005):
   When world type is REAL but the generator filename contains a storm keyword
   (glitch_storm, sf02, storm_sf, style_frame_02), the sub-type REAL_STORM is
   used with threshold=3.  Same as render_qa v1.6.0 REAL_STORM.

CONFIG FILE (unchanged from v004)
----------------------------------------------------------------------
Priority: ltg_warmth_guarantees.json > warmth_lint_config.json > built-in

WORLD-TYPE AUTO-INFERENCE (v005)
---------------------------------
infer_world_type("LTG_TOOL_styleframe_discovery.py")              → "REAL"
infer_world_type("LTG_TOOL_style_frame_02_glitch_storm.py")       → "REAL" → "REAL_STORM"
infer_world_type("LTG_TOOL_style_frame_03_other_side.py")         → "OTHER_SIDE"
infer_world_type("LTG_TOOL_bg_glitch_layer_encounter.py")         → "GLITCH"
infer_world_type("LTG_CHAR_grandma_miri_expression_sheet_v004.py")     → "REAL"
infer_world_type("LTG_TOOL_cosmo_turnaround.py")                  → None

USAGE (standalone CLI)
----------------------
    python LTG_TOOL_palette_warmth_lint.py
    python LTG_TOOL_palette_warmth_lint.py path/to/master_palette.md
    python LTG_TOOL_palette_warmth_lint.py --config path/to/config.json palette.md
    python LTG_TOOL_palette_warmth_lint.py --strict palette.md
    python LTG_TOOL_palette_warmth_lint.py --world-type REAL palette.md
    python LTG_TOOL_palette_warmth_lint.py --world-type REAL_STORM palette.md
    python LTG_TOOL_palette_warmth_lint.py --check-generator generators/LTG_TOOL_bg_glitch_storm_v008.py palette.md
    python LTG_TOOL_palette_warmth_lint.py --infer-world-type generator.py palette.md
    python LTG_TOOL_palette_warmth_lint.py --no-auto-world-type palette.md
    python LTG_TOOL_palette_warmth_lint.py --world-type GLITCH --world-threshold-only

PROGRAMMATIC API (backward compatible with v004)
----------------
    from LTG_TOOL_palette_warmth_lint import (
        lint_palette_file,
        lint_palette_text,
        format_report,
        load_config,
        infer_world_type,
        infer_world_subtype,
        DEFAULT_PALETTE_PATH,
        DEFAULT_CONFIG_PATH,
        DEFAULT_GUARANTEES_PATH,
    )

Author: Sam Kowalski (Color & Style Artist) — Cycle 39
Based on: LTG_TOOL_palette_warmth_lint.py (Kai Nakamura / Sam Kowalski, Cycle 36)
Version: 6.0.0

Design note: Operates entirely on markdown source text — no Pillow dependency.
"""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Dict, List, Optional, Tuple, Union

try:
    import numpy as np
    _NP_AVAILABLE = True
except ImportError:
    np = None  # type: ignore
    _NP_AVAILABLE = False


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


# ---------------------------------------------------------------------------
# Optional: standalone world-type inference (v005 — uses world_type_infer_v001)
# Falls back to v004 inline rules if not available.
# ---------------------------------------------------------------------------
try:
    from LTG_TOOL_world_type_infer import (
        infer_world_type as _infer_world_type_standalone,
        get_warm_cool_threshold as _get_threshold_standalone,
        WARM_COOL_THRESHOLDS as _STANDALONE_THRESHOLDS,
    )
    _WORLD_INFER_STANDALONE = True
except ImportError:
    _WORLD_INFER_STANDALONE = False
    _infer_world_type_standalone = None
    _get_threshold_standalone = None
    _STANDALONE_THRESHOLDS = None


# ---------------------------------------------------------------------------
# Built-in fallback config (mirrors v004)
# ---------------------------------------------------------------------------

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


# ── Built-in world presets (matches warmth_lint_v004 / render_qa v1.6.0) ───
_BUILTIN_WORLD_PRESETS: Dict[str, Dict] = {
    "REAL": {
        "warm_cool_threshold": 12,
        "note": (
            "Lamp-lit warm interior / daytime exterior. Warm presence expected. "
            "SF01/SF04 archetypes. Real-world environments."
        ),
    },
    "REAL_INTERIOR": {
        "warm_cool_threshold": 12,
        "note": (
            "Lamp-lit warm interior (SF01 / classroom / kitchen / living room). "
            "Same threshold as REAL — sub-type for clarity."
        ),
    },
    "REAL_STORM": {
        "warm_cool_threshold": 3,
        "note": (
            "Contested storm / Glitch-invasion scene (SF02 Glitch Storm). "
            "Warm building-window accents only — warm/cool threshold lowered to 3."
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
        "warm_cool_threshold": 3,
        "note": (
            "Glitch Layer / Glitch World — warm tones should be near-zero. "
            "Electric Cyan + UV Purple dominant. Near-zero warm/cool ratio correct."
        ),
    },
}

VALID_WORLD_TYPES = frozenset(_BUILTIN_WORLD_PRESETS.keys())


# Storm filename pattern — for REAL → REAL_STORM sub-typing (mirrors render_qa v1.6.0)
_REAL_STORM_PATTERN = re.compile(
    r'(glitch[_\-]?storm|storm[_\-]?sf|sf02|style[_\-]?frame[_\-]?02)',
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# World-type inference
# ---------------------------------------------------------------------------

# Inline fallback rules (used when world_type_infer_v001 is not importable)
_FALLBACK_WORLD_RULES: List[Tuple[re.Pattern, str]] = [
    (re.compile(r'(sf03|other[_\-]?side|otherside|crt[_\-]?world)', re.IGNORECASE), "OTHER_SIDE"),
    (re.compile(r'(glitch[_\-]?layer|glitch[_\-]?encounter|glitch[_\-]?world)', re.IGNORECASE), "GLITCH"),
    (re.compile(r'(sf01|sf02|sf04|discovery|glitch[_\-]?storm|style[_\-]?frame[_\-]?0[124]|luma[_\-]?byte)', re.IGNORECASE), "REAL"),
    (re.compile(r'(classroom|kitchen|hallway|tech[_\-]?den|main[_\-]?street|millbrook|grandma|luma[_\-]?house|backyard|living[_\-]?room)', re.IGNORECASE), "REAL"),
    (re.compile(r'(scene|interior|exterior|daytime|night[_\-]?street)', re.IGNORECASE), "REAL"),
]


def infer_world_type(filename_or_path: str) -> Optional[str]:
    """
    Infer the world type (REAL | OTHER_SIDE | GLITCH) from a generator filename or path.

    v005: delegates to LTG_TOOL_world_type_infer if available,
    otherwise falls back to v004 inline rules.

    Returns "REAL", "OTHER_SIDE", "GLITCH", or None.
    Does NOT return "REAL_STORM" — use infer_world_subtype() for that.

    Examples
    --------
    >>> infer_world_type("LTG_TOOL_styleframe_discovery.py")
    'REAL'
    >>> infer_world_type("LTG_TOOL_style_frame_03_other_side.py")
    'OTHER_SIDE'
    >>> infer_world_type("LTG_TOOL_bg_glitch_layer_encounter.py")
    'GLITCH'
    >>> infer_world_type("LTG_CHAR_grandma_miri_expression_sheet_v004.py")
    'REAL'
    >>> infer_world_type("LTG_TOOL_cosmo_turnaround.py")  # no world context
    None
    """
    if _WORLD_INFER_STANDALONE and _infer_world_type_standalone is not None:
        return _infer_world_type_standalone(filename_or_path)
    # Fallback: inline rules
    basename = os.path.basename(filename_or_path)
    for pattern, world_type in _FALLBACK_WORLD_RULES:
        if pattern.search(basename):
            return world_type
    return None


def infer_world_subtype(filename_or_path: str) -> Optional[str]:
    """
    Infer world type including REAL_STORM sub-type (v005 new).

    First calls infer_world_type().  If the result is "REAL" and the filename
    matches the storm pattern, returns "REAL_STORM" instead of "REAL".
    All other world types are returned unchanged.

    Returns "REAL_INTERIOR", "REAL_STORM", "GLITCH", "OTHER_SIDE", or None.

    Examples
    --------
    >>> infer_world_subtype("LTG_COLOR_styleframe_glitch_storm.png")
    'REAL_STORM'
    >>> infer_world_subtype("LTG_COLOR_styleframe_discovery.png")
    'REAL_INTERIOR'
    >>> infer_world_subtype("LTG_TOOL_bg_grandma_kitchen.py")
    'REAL_INTERIOR'
    """
    base_type = infer_world_type(filename_or_path)
    if base_type == "REAL":
        basename = os.path.basename(filename_or_path)
        if _REAL_STORM_PATTERN.search(basename):
            return "REAL_STORM"
        return "REAL_INTERIOR"
    return base_type


# ---------------------------------------------------------------------------
# Config loading (identical to v004)
# ---------------------------------------------------------------------------

def load_config(path: Optional[str] = None) -> Dict:
    """
    Load the warmth lint config from a JSON file.

    Priority order:
      1. ltg_warmth_guarantees.json (DEFAULT_GUARANTEES_PATH) — preferred
      2. warmth_lint_config.json (DEFAULT_CONFIG_PATH or path arg) — legacy fallback
      3. Built-in config (_BUILTIN_CONFIG) — last resort
    """
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
                    f"[warmth_lint_v005] WARNING: Could not read '{candidate}': {exc}\n"
                )
                continue
        else:
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
                f"[warmth_lint_v005] WARNING: Could not read config '{config_path}': {exc}\n"
                f"[warmth_lint_v005] Falling back to built-in config.\n"
            )
            return dict(_BUILTIN_CONFIG)

    if "warm_prefixes" not in cfg or not isinstance(cfg["warm_prefixes"], list):
        sys.stderr.write(
            "[warmth_lint_v005] WARNING: Config missing 'warm_prefixes' list.\n"
            "[warmth_lint_v005] Falling back to built-in config.\n"
        )
        return dict(_BUILTIN_CONFIG)

    cfg["warm_prefixes"] = [str(p).strip().upper() for p in cfg["warm_prefixes"] if p]

    raw_tol = cfg.get("soft_tolerance", {})
    if not isinstance(raw_tol, dict):
        raw_tol = {}
    tolerance: Dict[str, int] = {
        "G": max(0, int(raw_tol.get("G", _DEFAULT_TOLERANCE["G"]))),
        "B": max(0, int(raw_tol.get("B", _DEFAULT_TOLERANCE["B"]))),
    }
    cfg["soft_tolerance"] = tolerance

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
# Regex pattern builder (unchanged from v004)
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
# Core warmth check (unchanged from v004)
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
# World-type threshold analysis (mirrors v004)
# ---------------------------------------------------------------------------

def _get_world_threshold(world_type: Optional[str], config: Dict) -> float:
    """
    Get warm/cool threshold for the given world type from config or built-in presets.
    Accepts REAL_STORM sub-type (v005).
    """
    presets = config.get("world_presets", _BUILTIN_WORLD_PRESETS)
    # Normalise
    wt = (world_type or "REAL").upper()
    preset = presets.get(wt, _BUILTIN_WORLD_PRESETS.get(wt, {}))
    return float(preset.get("warm_cool_threshold", 12))


def _analyse_world_warmth(
    entries: List[Dict],
    world_type: str,
    config: Dict,
) -> Dict:
    """
    Analyse the palette entries for world-type warm/cool consistency.
    Accepts REAL_STORM as world_type (v005).
    """
    presets = config.get("world_presets", _BUILTIN_WORLD_PRESETS)
    preset = presets.get(world_type.upper(), _BUILTIN_WORLD_PRESETS.get(world_type.upper(), {}))
    threshold = preset.get("warm_cool_threshold", 0)
    note = preset.get("note", "")

    total = len(entries)

    if _NP_AVAILABLE and total > 0:
        # v6.0.0: numpy vectorization — build RGB array, count warm entries in one op
        rgb_arr = np.array([e["rgb"] for e in entries], dtype=np.int32)  # (N, 3)
        R, G, B = rgb_arr[:, 0], rgb_arr[:, 1], rgb_arr[:, 2]
        warm_mask = (R >= G) & (R >= B)
        warm_count = int(warm_mask.sum())
        cool_count = total - warm_count
    else:
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
    if wt in ("REAL", "REAL_INTERIOR"):
        threshold_met = warm_ratio >= threshold
        if not threshold_met:
            advisory.append(
                f"{wt} world expected warm ratio ≥ {threshold:.0f}%; "
                f"found {warm_ratio:.1f}% ({warm_count}/{total} entries warm)."
            )
    elif wt == "REAL_STORM":
        # Storm scene: low warm expected but not zero — threshold=3%
        threshold_met = warm_ratio >= threshold
        if not threshold_met:
            advisory.append(
                f"REAL_STORM world expected warm ratio ≥ {threshold:.0f}%; "
                f"found {warm_ratio:.1f}% ({warm_count}/{total} entries warm). "
                f"Warm window accents should still be present in the storm palette."
            )
    elif wt in ("OTHER_SIDE", "GLITCH"):
        threshold_met = warm_ratio == 0
        if warm_count > 0:
            advisory.append(
                f"{wt} world should have 0 warm entries; "
                f"found {warm_count}/{total} warm entries ({warm_ratio:.1f}%). "
                f"Check whether REAL-world warm colours have leaked into this world's palette."
            )
    else:
        threshold_met = True

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
# Palette entry parser (unchanged from v004)
# ---------------------------------------------------------------------------

def _parse_all_palette_entries(text: str) -> List[Dict]:
    """Parse all palette table rows from the markdown (any code prefix)."""
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
    world_type  : str | None  — "REAL", "REAL_INTERIOR", "REAL_STORM", "OTHER_SIDE",
                                or "GLITCH". If provided, adds world-type warmth analysis
                                (advisory only — does not change result/violations).

    Returns
    -------
    dict with keys:
        result            : "PASS" | "WARN"
        source            : str
        total_checked     : int
        total_violations  : int
        violations        : list[dict]
        prefixes_checked  : list[str]
        tolerance_used    : dict[str, int]
        world_analysis    : dict | None
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
                "reason": "; ".join(channel_violations),
                "margin": margin,
                "source": source_name,
            })

    result = "WARN" if violations else "PASS"

    # World-type warmth analysis (advisory only)
    world_analysis = None
    if world_type is not None:
        all_entries = _parse_all_palette_entries(text)
        world_analysis = _analyse_world_warmth(all_entries, world_type, config)

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
    palette_path: str = None,
    config: Optional[Dict] = None,
    world_type: Optional[str] = None,
    strict: bool = False,
) -> Dict:
    """
    Lint a palette markdown file for warmth violations.

    Parameters
    ----------
    palette_path : str or None — path to the palette .md file.
                                 Defaults to DEFAULT_PALETTE_PATH.
    config       : dict or None — from load_config(); if None, calls load_config().
    world_type   : str | None   — passed to lint_palette_text().
    strict       : bool         — if True, override tolerance to {"G": 0, "B": 0}.

    Returns the same dict as lint_palette_text().
    """
    if palette_path is None:
        palette_path = DEFAULT_PALETTE_PATH

    try:
        with open(palette_path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except FileNotFoundError:
        return {
            "result": "ERROR",
            "source": str(palette_path),
            "error": f"File not found: {palette_path}",
            "total_checked": 0,
            "total_violations": 0,
            "violations": [],
            "prefixes_checked": [],
            "tolerance_used": {},
            "world_analysis": None,
        }

    if config is None:
        config = load_config()

    if strict:
        config = dict(config)
        config["soft_tolerance"] = {"G": 0, "B": 0}

    return lint_palette_text(text, source_name=str(palette_path), config=config, world_type=world_type)


# ---------------------------------------------------------------------------
# Report formatter (extended from v004 to show REAL_STORM sub-type)
# ---------------------------------------------------------------------------

def format_report(result: Dict, verbose: bool = False) -> str:
    """
    Format a lint result dict as a human-readable string.

    Parameters
    ----------
    result  : dict — from lint_palette_text() or lint_palette_file()
    verbose : bool — if True, include margin details per violation

    Returns
    -------
    str — formatted report
    """
    lines = []
    source = result.get("source", "<unknown>")
    res    = result.get("result", "UNKNOWN")
    total  = result.get("total_checked", 0)
    viols  = result.get("total_violations", 0)
    pfxs   = result.get("prefixes_checked", [])
    tol    = result.get("tolerance_used", {})

    lines.append(f"Palette Warmth Lint — {source}")
    lines.append(f"  Result   : {res}")
    lines.append(f"  Checked  : {total} entries  (prefixes: {', '.join(pfxs)})")
    lines.append(f"  Tolerance: G±{tol.get('G', 0)}, B±{tol.get('B', 0)}")
    lines.append(f"  Violations: {viols}")

    if result.get("error"):
        lines.append(f"  ERROR: {result['error']}")
        return "\n".join(lines)

    for v in result.get("violations", []):
        r, g, b = v["rgb"]
        lines.append(
            f"    [{v['code']}] {v['name']} — {v['hex']} ({r},{g},{b})"
            f"  ← {v['reason']}"
        )
        if verbose and "margin" in v:
            m = v["margin"]
            lines.append(
                f"      margin: G-R={m['G']:+d}, B-R={m['B']:+d}"
            )

    # World-type analysis block
    wa = result.get("world_analysis")
    if wa:
        wt       = wa.get("world_type", "UNKNOWN")
        thr      = wa.get("threshold", 0)
        w_warm   = wa.get("warm_entries", 0)
        w_total  = wa.get("total_entries", 0)
        w_ratio  = wa.get("warm_ratio_pct", 0.0)
        w_met    = wa.get("threshold_met", True)
        note     = wa.get("note", "")
        adv      = wa.get("advisory_warnings", [])

        lines.append("")
        lines.append(f"  World-Type Analysis: {wt}")
        lines.append(f"    Warm/cool threshold : {thr}")
        lines.append(f"    Warm entries        : {w_warm}/{w_total} ({w_ratio:.1f}%)")
        lines.append(f"    Threshold met       : {'YES' if w_met else 'NO (advisory)'}")
        if note:
            lines.append(f"    Note: {note}")
        for aw in adv:
            lines.append(f"    ADVISORY: {aw}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    """
    CLI entry point.

    Returns 0 on PASS, 1 on WARN/violations, 2 on error.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="LTG palette warmth compliance linter v005",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "palette",
        nargs="?",
        default=None,
        help="Path to palette markdown file. Defaults to master_palette.md.",
    )
    parser.add_argument(
        "--config",
        metavar="CONFIG",
        default=None,
        help="Path to warmth lint JSON config file.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        default=False,
        help="Force strict mode (tolerance={G:0, B:0}) regardless of config.",
    )
    parser.add_argument(
        "--world-type",
        metavar="WORLD",
        default=None,
        help=(
            "Override world type for advisory threshold check. "
            "Values: REAL, REAL_INTERIOR, REAL_STORM, OTHER_SIDE, GLITCH."
        ),
    )
    parser.add_argument(
        "--check-generator",
        metavar="GENERATOR_FILE",
        default=None,
        help=(
            "Infer world type from GENERATOR_FILE and apply it to the palette lint. "
            "REAL_STORM sub-typing is applied if the generator filename matches a storm pattern."
        ),
    )
    parser.add_argument(
        "--infer-world-type",
        metavar="GENERATOR",
        default=None,
        help="Infer and print world type from GENERATOR filename. Does not run lint.",
    )
    parser.add_argument(
        "--no-auto-world-type",
        action="store_true",
        default=False,
        help="Disable automatic world-type inference from palette filename.",
    )
    parser.add_argument(
        "--world-threshold-only",
        action="store_true",
        default=False,
        help="Print the warm/cool threshold integer for --world-type and exit.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Include per-violation margin details in report.",
    )

    args = parser.parse_args()

    # --infer-world-type: just infer and exit
    if args.infer_world_type:
        wt = infer_world_type(args.infer_world_type)
        ws = infer_world_subtype(args.infer_world_type)
        print(f"World type  : {wt}")
        print(f"World subtype: {ws}")
        return 0

    # --world-threshold-only: print threshold and exit
    if args.world_threshold_only:
        if not args.world_type:
            sys.stderr.write("[warmth_lint_v005] ERROR: --world-threshold-only requires --world-type.\n")
            return 2
        cfg = load_config(args.config)
        thr = _get_world_threshold(args.world_type.upper(), cfg)
        print(int(thr))
        return 0

    palette_path = args.palette or DEFAULT_PALETTE_PATH
    cfg = load_config(args.config)

    # Determine world type
    world_type = None
    if args.world_type:
        world_type = args.world_type.upper()
    elif args.check_generator:
        # Infer from generator and apply REAL_STORM sub-typing
        world_type = infer_world_subtype(args.check_generator)
        if world_type:
            print(f"[warmth_lint_v005] Inferred world type from generator: {world_type}")
    elif not args.no_auto_world_type:
        # Auto-infer from palette filename (same as v004)
        raw_wt = infer_world_type(palette_path)
        if raw_wt is not None:
            world_type = infer_world_subtype(palette_path)

    result = lint_palette_file(
        palette_path=palette_path,
        config=cfg,
        world_type=world_type,
        strict=args.strict,
    )

    print(format_report(result, verbose=args.verbose))

    res = result.get("result", "ERROR")
    if res == "PASS":
        return 0
    elif res == "WARN":
        return 1
    else:
        return 2


if __name__ == "__main__":
    sys.exit(main())
