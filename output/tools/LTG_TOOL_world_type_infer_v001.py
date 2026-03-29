"""
LTG_TOOL_world_type_infer_v001.py
===================================
Standalone world-type inference helper for "Luma & the Glitchkin."

Infers the production world type (REAL | OTHER_SIDE | GLITCH) from any LTG asset
filename or path — generator scripts (.py) and rendered images (.png, .jpg) alike.
Provides the canonical warm/cool threshold for that world type, matching the values
in warmth_lint_v004 world_presets and render_qa v1.5.0.

This module is intentionally lightweight (stdlib + re only) so any pipeline tool
can import it without pulling in the full palette_warmth_lint_v004 module.

Usage as module:
    from LTG_TOOL_world_type_infer_v001 import infer_world_type, get_warm_cool_threshold

    wt  = infer_world_type("LTG_COLOR_styleframe_discovery_v004.png")  # → "REAL"
    thr = get_warm_cool_threshold(wt)                                   # → 12.0

Usage as CLI:
    python LTG_TOOL_world_type_infer_v001.py path/to/asset.png
    python LTG_TOOL_world_type_infer_v001.py --threshold path/to/asset.png
    python LTG_TOOL_world_type_infer_v001.py --batch output/color/style_frames/
    python LTG_TOOL_world_type_infer_v001.py --list-rules

Author: Sam Kowalski (Color & Style Artist) — Cycle 38
Version: 1.0.0

Changelog:
  1.1.0 (Cycle 39): REAL_STORM sub-type added (Kai Nakamura, per Alex Chen brief).
                    SF02 "Glitch Storm" is a contested real-world storm scene with
                    intentionally cool-dominant palette. Split from REAL to prevent
                    persistent false WARNs on SF02 warm/cool check (sep~6.5 < REAL
                    threshold 12). REAL_STORM threshold = 3.0 PIL units.
                    New constants: WORLD_REAL_STORM, WORLD_REAL_INTERIOR.
                    WARM_COOL_THRESHOLDS updated: REAL_STORM=3.0, REAL_INTERIOR=12.0.
                    Inference rules updated: sf02/glitch_storm → REAL_STORM (new rule
                    inserted before the REAL rule). REAL rule scope narrowed to
                    sf01/sf04/discovery only.
  1.0.0 (Cycle 38): Initial implementation. Standalone extraction of the
                    infer_world_type() logic from LTG_TOOL_palette_warmth_lint_v004.
                    Adds get_warm_cool_threshold(), batch mode, rule listing,
                    and --threshold CLI flag. Coordinates with render_qa v1.5.0
                    (REAL threshold fix) and Miri slipper audit C38.
"""

from __future__ import annotations

import os
import re
import sys
import glob
from typing import Dict, List, Optional, Tuple


__version__ = "1.1.0"  # C39: REAL_STORM sub-type added (Kai Nakamura)
__author__  = "Sam Kowalski"


# ---------------------------------------------------------------------------
# World type constants
# ---------------------------------------------------------------------------

WORLD_REAL         = "REAL"
WORLD_REAL_STORM   = "REAL_STORM"    # v1.1.0: SF02 storm sub-type (cool-dominant)
WORLD_REAL_INTERIOR = "REAL_INTERIOR"  # v1.1.0: alias for warm lamp-lit interiors
WORLD_OTHER_SIDE   = "OTHER_SIDE"
WORLD_GLITCH       = "GLITCH"

# Canonical warm/cool separation thresholds (PIL hue units, 0-255 scale)
# Must match render_qa v1.6.0 _WORLD_WARM_COOL_THRESHOLD and
# warmth_lint_v004 world_presets (updated C39).
# v1.1.0: REAL_STORM added (threshold=3.0); REAL kept for backward-compat (=REAL_INTERIOR).
WARM_COOL_THRESHOLDS: Dict[Optional[str], float] = {
    WORLD_REAL:           12.0,   # backward-compat; treated as REAL_INTERIOR
    WORLD_REAL_INTERIOR:  12.0,   # lamp-lit interiors / daytime exteriors
    WORLD_REAL_STORM:      3.0,   # contested storm scenes (SF02); cool-dominant by design
    WORLD_GLITCH:          3.0,   # near-zero warm; only tiny hot-spot residual allowed
    WORLD_OTHER_SIDE:      0.0,   # fully digital, zero warm — skip warm/cool check
    None:                 12.0,   # unknown world; apply conservative REAL default
}

# Human-readable descriptions for each world type
WORLD_DESCRIPTIONS: Dict[Optional[str], str] = {
    WORLD_REAL: (
        "Real World — lamp-lit interiors or daytime exteriors. "
        "Warm palette dominant. Glitch palette forbidden."
    ),
    WORLD_REAL_STORM: (
        "Real World Storm — contested exterior storm scene (SF02 archetype). "
        "Cool sky dominant; warm tones present only as subdued window glow accents. "
        "Threshold 3 — intentionally cool-dominant, not a defect."
    ),
    WORLD_REAL_INTERIOR: (
        "Real World Interior — warm lamp-lit interior or calm daytime exterior. "
        "Alias for REAL. Threshold 12 — warm presence expected."
    ),
    WORLD_GLITCH: (
        "Glitch Layer — digital void space. "
        "Electric Cyan + UV Purple dominant. Near-zero warm."
    ),
    WORLD_OTHER_SIDE: (
        "The Other Side — deep CRT interior. "
        "Fully cold/digital. Zero warm light sources."
    ),
    None: (
        "Unknown world — no filename pattern match. "
        "Applies conservative REAL warm/cool threshold."
    ),
}


# ---------------------------------------------------------------------------
# Inference rules  (evaluated in order; first match wins)
# ---------------------------------------------------------------------------
# Each rule: (compiled_regex, world_type_string, human_readable_note)
# Patterns are case-insensitive and match against the basename only.

_INFERENCE_RULES: List[Tuple[re.Pattern, str, str]] = [
    # ---- OTHER_SIDE (SF03 / "other side" / CRT world) ----------------------
    (
        re.compile(r'(sf03|other[_\-]?side|otherside|crt[_\-]?world)', re.IGNORECASE),
        WORLD_OTHER_SIDE,
        "SF03 / other-side / CRT world keyword",
    ),

    # ---- GLITCH Layer environments -----------------------------------------
    (
        re.compile(
            r'(glitch[_\-]?layer|glitch[_\-]?encounter|glitch[_\-]?world)',
            re.IGNORECASE,
        ),
        WORLD_GLITCH,
        "Glitch Layer / encounter / world keyword",
    ),

    # ---- REAL_STORM — SF02 glitch_storm (cool-dominant storm scene) ----------
    # v1.1.0: split from REAL. Must appear before the REAL rule.
    (
        re.compile(
            r'(sf02|glitch[_\-]?storm|style[_\-]?frame[_\-]?02)',
            re.IGNORECASE,
        ),
        WORLD_REAL_STORM,
        "SF02 / glitch_storm — contested real-world storm (cool-dominant; threshold=3)",
    ),

    # ---- REAL — named style frames (SF01, SF04) ----------------------------
    # v1.1.0: sf02/glitch_storm removed — handled by REAL_STORM rule above.
    (
        re.compile(
            r'(sf01|sf04|discovery|'
            r'style[_\-]?frame[_\-]?0[14]|luma[_\-]?byte)',
            re.IGNORECASE,
        ),
        WORLD_REAL,
        "SF01/SF04 — discovery / style_frame 01/04 / luma_byte (SF04)",
    ),

    # ---- REAL — Real World environment backgrounds -------------------------
    (
        re.compile(
            r'(classroom|kitchen|hallway|tech[_\-]?den|main[_\-]?street|'
            r'millbrook|grandma|luma[_\-]?house|backyard|living[_\-]?room)',
            re.IGNORECASE,
        ),
        WORLD_REAL,
        "Real World env background keyword (classroom / kitchen / hallway / etc.)",
    ),

    # ---- REAL — Generic scene / interior / exterior keywords ---------------
    (
        re.compile(
            r'(scene|interior|exterior|daytime|night[_\-]?street)',
            re.IGNORECASE,
        ),
        WORLD_REAL,
        "Generic Real World scene keyword (scene / interior / exterior / etc.)",
    ),
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def infer_world_type(filename_or_path: str) -> Optional[str]:
    """
    Infer the production world type from an asset filename or path.

    Works with both generator scripts (.py) and rendered images (.png, .jpg, .webp).
    Matching is performed against the basename only (directory path is ignored).

    Parameters
    ----------
    filename_or_path : str
        Any path or filename referencing an LTG asset.
        Examples: "LTG_COLOR_styleframe_discovery_v004.png",
                  "LTG_TOOL_bg_grandma_kitchen_v004.py",
                  "/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v008.png"

    Returns
    -------
    str | None
        "REAL", "OTHER_SIDE", or "GLITCH" on a match.
        None if no world context can be inferred (character sheets, logos,
        abstract tools, color models).

    Examples
    --------
    >>> infer_world_type("LTG_COLOR_styleframe_discovery_v004.png")
    'REAL'
    >>> infer_world_type("LTG_TOOL_style_frame_03_other_side_v005.py")
    'OTHER_SIDE'
    >>> infer_world_type("LTG_TOOL_bg_glitch_layer_encounter_v001.py")
    'GLITCH'
    >>> infer_world_type("LTG_ENV_grandma_kitchen_v004.png")
    'REAL'
    >>> infer_world_type("LTG_CHAR_luma_expressions_v010.png")  # character sheet
    None
    >>> infer_world_type("LTG_BRAND_logo_v001.png")
    None
    """
    basename = os.path.basename(filename_or_path)
    for pattern, world_type, _note in _INFERENCE_RULES:
        if pattern.search(basename):
            return world_type
    return None


def get_warm_cool_threshold(world_type: Optional[str]) -> float:
    """
    Return the canonical warm/cool separation threshold (PIL hue units) for a world type.

    These values match render_qa v1.5.0 and warmth_lint_v004 world_presets:
      REAL       → 12.0 (lamp-lit interiors; warm accents present)
      GLITCH     →  3.0 (near-zero warm)
      OTHER_SIDE →  0.0 (skip warm/cool check; fully digital)
      None       → 12.0 (conservative REAL default for unknown world)

    Parameters
    ----------
    world_type : str | None
        Value returned by infer_world_type().

    Returns
    -------
    float
        Minimum warm/cool PIL hue separation required to PASS render_qa check D.
    """
    return WARM_COOL_THRESHOLDS.get(world_type, WARM_COOL_THRESHOLDS[None])


def infer_and_threshold(filename_or_path: str) -> Tuple[Optional[str], float]:
    """
    Convenience: return (world_type, warm_cool_threshold) for a single asset path.

    Parameters
    ----------
    filename_or_path : str

    Returns
    -------
    (str | None, float)
        World type string (or None) and the corresponding threshold.

    Examples
    --------
    >>> infer_and_threshold("LTG_COLOR_styleframe_discovery_v004.png")
    ('REAL', 12.0)
    >>> infer_and_threshold("LTG_COLOR_styleframe_otherside_v005.png")
    ('OTHER_SIDE', 0.0)
    """
    wt = infer_world_type(filename_or_path)
    return wt, get_warm_cool_threshold(wt)


def list_rules() -> List[Dict]:
    """
    Return the ordered list of inference rules as structured dicts.

    Each dict has keys: pattern (str), world_type (str), note (str).
    Rules are evaluated in order; the first match wins.

    Returns
    -------
    list[dict]
    """
    return [
        {
            "pattern":    rule[0].pattern,
            "flags":      "IGNORECASE",
            "world_type": rule[1],
            "note":       rule[2],
        }
        for rule in _INFERENCE_RULES
    ]


def batch_infer(directory_or_paths, extensions=(".png", ".jpg", ".py")) -> List[Dict]:
    """
    Infer world types for all matching files in a directory or a list of paths.

    Parameters
    ----------
    directory_or_paths : str | list[str]
        Either a directory path (all files with matching extensions are scanned)
        or a list of explicit file paths.
    extensions : tuple[str, ...]
        File extensions to include (lowercase). Ignored if explicit paths supplied.

    Returns
    -------
    list[dict]
        Each dict: {"path": str, "basename": str, "world_type": str|None, "threshold": float}
    """
    if isinstance(directory_or_paths, str) and os.path.isdir(directory_or_paths):
        paths = [
            os.path.join(directory_or_paths, f)
            for f in sorted(os.listdir(directory_or_paths))
            if os.path.splitext(f)[1].lower() in extensions
        ]
    else:
        paths = list(directory_or_paths)

    results = []
    for p in paths:
        wt, thr = infer_and_threshold(p)
        results.append({
            "path":       p,
            "basename":   os.path.basename(p),
            "world_type": wt,
            "threshold":  thr,
        })
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _format_result(path: str, world_type: Optional[str], threshold: float) -> str:
    basename = os.path.basename(path)
    wt_str   = world_type if world_type is not None else "UNKNOWN"
    desc     = WORLD_DESCRIPTIONS.get(world_type, WORLD_DESCRIPTIONS[None])
    return (
        f"  {basename}\n"
        f"    world_type : {wt_str}\n"
        f"    threshold  : {threshold} PIL hue units (warm/cool min separation)\n"
        f"    note       : {desc}\n"
    )


def _cli(argv: List[str]) -> int:
    """
    CLI entry point.

    Modes:
      python LTG_TOOL_world_type_infer_v001.py <path> [<path> ...]
          Infer world type for one or more file paths.

      python LTG_TOOL_world_type_infer_v001.py --threshold <path>
          Print only the float threshold to stdout (for shell capture).

      python LTG_TOOL_world_type_infer_v001.py --batch <directory>
          Scan directory and print world types for all .png/.py files.

      python LTG_TOOL_world_type_infer_v001.py --list-rules
          Print the ordered inference rule table.
    """
    if not argv:
        print(f"LTG_TOOL_world_type_infer_v001  v{__version__}")
        print("Usage:")
        print("  python LTG_TOOL_world_type_infer_v001.py <path> [<path> ...]")
        print("  python LTG_TOOL_world_type_infer_v001.py --threshold <path>")
        print("  python LTG_TOOL_world_type_infer_v001.py --batch <directory>")
        print("  python LTG_TOOL_world_type_infer_v001.py --list-rules")
        return 0

    # --list-rules
    if "--list-rules" in argv:
        print(f"LTG World-Type Inference Rules (v{__version__})")
        print("=" * 60)
        for i, rule in enumerate(list_rules(), 1):
            print(f"Rule {i}: {rule['world_type']}")
            print(f"  Pattern : {rule['pattern']}  [{rule['flags']}]")
            print(f"  Note    : {rule['note']}")
            print()
        print("Evaluation order: first match wins; returns None if no rule matches.")
        return 0

    # --threshold <path>  (prints only the float for shell capture)
    if "--threshold" in argv:
        idx = argv.index("--threshold")
        if idx + 1 >= len(argv):
            print("ERROR: --threshold requires a path argument", file=sys.stderr)
            return 2
        target = argv[idx + 1]
        wt, thr = infer_and_threshold(target)
        print(thr)
        return 0

    # --batch <directory>
    if "--batch" in argv:
        idx = argv.index("--batch")
        if idx + 1 >= len(argv):
            print("ERROR: --batch requires a directory argument", file=sys.stderr)
            return 2
        directory = argv[idx + 1]
        if not os.path.isdir(directory):
            print(f"ERROR: Not a directory: {directory}", file=sys.stderr)
            return 2
        results = batch_infer(directory)
        print(f"LTG World-Type Batch Report  [{directory}]")
        print("=" * 60)
        # Group by world type
        by_world: Dict[Optional[str], List[Dict]] = {}
        for r in results:
            by_world.setdefault(r["world_type"], []).append(r)
        for wt in [WORLD_REAL, WORLD_GLITCH, WORLD_OTHER_SIDE, None]:
            files = by_world.get(wt, [])
            if not files:
                continue
            label = wt if wt else "UNKNOWN"
            print(f"\n  [{label}]  threshold={WARM_COOL_THRESHOLDS[wt]}")
            for r in files:
                print(f"    {r['basename']}")
        print(f"\nTotal: {len(results)} files scanned.")
        return 0

    # Default: infer world type for each path provided
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print("No paths provided.", file=sys.stderr)
        return 2

    print(f"LTG World-Type Inference  (v{__version__})")
    print("=" * 60)
    all_unknown = True
    for p in paths:
        wt, thr = infer_and_threshold(p)
        print(_format_result(p, wt, thr))
        if wt is not None:
            all_unknown = False
    return 0


if __name__ == "__main__":
    sys.exit(_cli(sys.argv[1:]))
