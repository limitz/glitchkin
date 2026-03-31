#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_char_interface.py
Character Renderer Interface Contract — v1.1.0
"Luma & the Glitchkin" — Cycle 53 / Morgan Walsh
v1.1.0: Morgan Walsh / Cycle 54 — check_inline_char_drawing false positive fix:
  - word-boundary matching for body-part patterns (draw_eye no longer matches draw_eye_glow)
  - delegate-wrapper detection: character draw functions that call canonical modules
    (LTG_TOOL_char_*, _draw_*_canonical) without using raw Cairo/PIL primitives are
    treated as modular-compliant and not flagged

Defines the standard interface that all modular character renderers (char_*.py)
must implement. Scene generators import from char_* modules instead of drawing
characters inline.

Standard function signature:
    draw_<character>(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface

This module provides:
  - REQUIRED_EXPORTS: the set of function names every char module must export
  - CharModuleSpec: dataclass describing what a char module provides
  - validate_char_module(module) -> ValidationResult: checks compliance
  - EXPRESSION_NAMES: canonical expression set per character
  - POSE_NAMES: canonical pose set
  - FACING_VALUES: valid facing directions
  - SCENE_LIGHTING_KEYS: valid scene lighting dict keys

Usage:
    from LTG_TOOL_char_interface import validate_char_module
    import char_luma
    result = validate_char_module(char_luma, character="luma")
    if not result.ok:
        for issue in result.issues:
            print(issue)
"""

import inspect
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

__version__ = "1.1.0"

# ── Canonical values ─────────────────────────────────────────────────────────

FACING_VALUES = frozenset({"left", "right", "front", "back", "three_quarter"})

SCENE_LIGHTING_KEYS = frozenset({
    "key_direction",   # str: "left", "right", "above", "below"
    "key_color",       # tuple (R, G, B)
    "fill_color",      # tuple (R, G, B)
    "ambient_color",   # tuple (R, G, B)
    "intensity",       # float 0.0-1.0
})

# Per-character canonical expressions (from expression sheets)
EXPRESSION_NAMES = {
    "luma": frozenset({
        "neutral", "curious", "determined", "worried", "surprised",
        "joyful", "frustrated", "awestruck",
    }),
    "cosmo": frozenset({
        "neutral", "skeptical", "excited", "thinking", "annoyed",
        "proud", "concerned", "laughing",
    }),
    "byte": frozenset({
        "neutral", "curious", "glitching", "determined", "sad",
        "playful", "alert", "protective",
    }),
    "glitch": frozenset({
        "neutral", "menacing", "covetous", "scattered", "forming",
        "angry", "cunning", "dissolving",
    }),
    "miri": frozenset({
        "neutral", "warm", "concerned", "nostalgic", "surprised",
        "wise", "knowing", "welcoming",
    }),
}

POSE_NAMES = frozenset({
    "standing", "walking", "running", "sitting", "crouching",
    "reaching", "pointing", "arms_crossed", "hands_on_hips",
    "custom",  # for scene-specific poses with extra kwargs
})

# ── Required exports ─────────────────────────────────────────────────────────

# Every char_*.py module MUST export a function named draw_<character> with this
# signature. The function returns a cairo.ImageSurface (ARGB) with the character
# rendered at the requested scale, expression, pose, and facing direction.
#
# Parameters:
#   expression: str     — one of EXPRESSION_NAMES[character]
#   pose: str           — one of POSE_NAMES
#   scale: float        — multiplier (1.0 = reference sheet scale)
#   facing: str         — one of FACING_VALUES
#   scene_lighting: dict | None — keys from SCENE_LIGHTING_KEYS, or None for neutral
#
# Returns:
#   cairo.ImageSurface  — ARGB surface, pre-multiplied alpha
#
# Optional exports (recommended):
#   CHARACTER_NAME: str         — e.g. "luma"
#   CHARACTER_SPEC_VERSION: str — e.g. "v015"
#   get_bounds(expression, pose, scale, facing) -> (w, h)
#       Returns the bounding box dimensions without rendering.
#       Useful for layout planning in scene generators.

REQUIRED_DRAW_PREFIX = "draw_"

OPTIONAL_EXPORTS = frozenset({
    "CHARACTER_NAME",
    "CHARACTER_SPEC_VERSION",
    "get_bounds",
})


# ── Validation ───────────────────────────────────────────────────────────────

@dataclass
class ValidationResult:
    """Result of validate_char_module()."""
    ok: bool = True
    module_name: str = ""
    character: str = ""
    draw_func_name: str = ""
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    exports_found: Set[str] = field(default_factory=set)


def validate_char_module(module: Any, character: Optional[str] = None) -> ValidationResult:
    """
    Check that a char_*.py module exports the required interface.

    Parameters
    ----------
    module : module
        An imported char_*.py module.
    character : str | None
        Character name (e.g. "luma"). If None, inferred from module name
        (char_luma -> "luma") or from CHARACTER_NAME attribute.

    Returns
    -------
    ValidationResult
        .ok is True if all required checks pass. .issues lists failures.
        .warnings lists non-blocking recommendations.
    """
    result = ValidationResult()
    result.module_name = getattr(module, "__name__", str(module))

    # Resolve character name
    if character:
        result.character = character
    elif hasattr(module, "CHARACTER_NAME"):
        result.character = module.CHARACTER_NAME
    else:
        # Infer from module name: char_luma -> luma
        mod_name = result.module_name.split(".")[-1]
        if mod_name.startswith("char_"):
            result.character = mod_name[5:]
        else:
            result.character = mod_name

    # Check for draw_<character> function
    draw_name = f"draw_{result.character}"
    result.draw_func_name = draw_name

    if not hasattr(module, draw_name):
        # Also accept any draw_* function
        draw_funcs = [n for n in dir(module) if n.startswith(REQUIRED_DRAW_PREFIX) and callable(getattr(module, n))]
        if draw_funcs:
            result.warnings.append(
                f"No '{draw_name}' found, but has: {', '.join(draw_funcs)}. "
                f"Consider renaming to '{draw_name}' for interface compliance."
            )
        else:
            result.issues.append(f"MISSING: required function '{draw_name}' not found")
            result.ok = False
            return result

    draw_fn = getattr(module, draw_name, None)
    if draw_fn is None:
        # Fallback already handled above
        return result

    if not callable(draw_fn):
        result.issues.append(f"'{draw_name}' exists but is not callable")
        result.ok = False
        return result

    result.exports_found.add(draw_name)

    # Check function signature
    try:
        sig = inspect.signature(draw_fn)
        params = list(sig.parameters.keys())
        expected_params = ["expression", "pose", "scale", "facing", "scene_lighting"]

        for ep in expected_params:
            if ep not in params:
                result.issues.append(
                    f"SIGNATURE: '{draw_name}' missing parameter '{ep}'. "
                    f"Expected: ({', '.join(expected_params)})"
                )
                result.ok = False
    except (ValueError, TypeError):
        result.warnings.append(f"Could not inspect signature of '{draw_name}'")

    # Check optional exports
    for opt in OPTIONAL_EXPORTS:
        if hasattr(module, opt):
            result.exports_found.add(opt)
        else:
            result.warnings.append(f"OPTIONAL: '{opt}' not exported (recommended)")

    # Check CHARACTER_NAME matches
    if hasattr(module, "CHARACTER_NAME"):
        cn = module.CHARACTER_NAME
        if cn != result.character:
            result.warnings.append(
                f"CHARACTER_NAME='{cn}' does not match expected '{result.character}'"
            )

    return result


# ── Scene generator compliance check ─────────────────────────────────────────

# Patterns that indicate inline character drawing in scene generators.
# Used by the CI lint (check 14: char_modular_lint).

# Body part drawing function names that should only appear in char_* modules,
# NOT in scene generators (style frames, storyboard panels, etc.).
# These are matched as whole words so draw_eye does NOT match draw_eye_glow.
INLINE_CHAR_DRAW_PATTERNS = [
    "draw_head", "draw_torso", "draw_body", "draw_arm", "draw_leg",
    "draw_face", "draw_hair", "draw_eye", "draw_hand", "draw_foot",
    "draw_shoulder", "draw_nose", "draw_mouth", "draw_brow",
]

# Scene generator filename patterns
SCENE_GENERATOR_PREFIXES = [
    "LTG_TOOL_style_frame_",
    "LTG_TOOL_sf_",
    "LTG_TOOL_styleframe_",
    "LTG_TOOL_sb_",
    "LTG_TOOL_pilot_",
]

# Files exempt from the inline character drawing lint
# (character-specific tools that legitimately define body part functions)
CHAR_MODULE_PREFIXES = [
    "LTG_TOOL_luma_",
    "LTG_TOOL_cosmo_",
    "LTG_TOOL_byte_",
    "LTG_TOOL_glitch_",
    "LTG_TOOL_miri_",
    "LTG_TOOL_grandma_miri_",
    "LTG_TOOL_character_",
    "LTG_TOOL_char_",
    "LTG_TOOL_draw_shoulder_arm",
    "LTG_TOOL_bodypart_",
    "LTG_TOOL_elderly_",
    "char_",
]

# Per-character draw function name prefixes in scene generators.
# A function *defined* in a scene generator whose name starts with one of
# these prefixes is a candidate for inline character rendering.  Whether
# it is truly inline (BAD) or a delegate wrapper (OK) is decided by
# _func_body_is_delegate() below.
CHAR_DRAW_FUNC_PREFIXES = [
    "draw_luma",
    "draw_cosmo",
    "draw_miri",
    "draw_byte",
    "draw_glitch",
]

# Cairo / PIL drawing primitive call patterns that indicate a function is
# performing raw (inline) character rendering rather than delegating.
# Any of these appearing in a function body = inline drawing.
_CAIRO_PRIMITIVE_RE = re.compile(
    r"\bctx\.(move_to|line_to|curve_to|arc|arc_negative|rel_move_to|"
    r"rel_line_to|rel_curve_to|rectangle|fill|stroke|paint|"
    r"set_source_rgba?|set_line_width)\s*\("
)
_PIL_PRIMITIVE_RE = re.compile(
    r"\bdraw\.(polygon|ellipse|line|rectangle|pieslice|chord|arc|"
    r"rounded_rectangle)\s*\("
)

# Patterns that indicate a canonical character module is being used —
# function is a delegate wrapper, not inline drawing.
# Matches:
#   _draw_luma_canonical(...)  — local alias imported from LTG_TOOL_char_luma
#   LTG_TOOL_char_luma         — direct module reference
#   from LTG_TOOL_char_        — import statement for a char module
_CANONICAL_CALL_RE = re.compile(
    r"(_draw_(?:luma|cosmo|byte|glitch|miri)_canonical|"
    r"LTG_TOOL_char_(?:luma|cosmo|byte|glitch|miri)|"
    r"from\s+LTG_TOOL_char_)"
)


def _extract_func_body_lines(lines: List[str], def_lineno: int) -> List[str]:
    """
    Given a list of file lines and the 1-based line number of a 'def' statement,
    return all lines belonging to the function body (excluding the def line itself).

    Works for functions indented at any level.  Stops when indentation returns
    to or below the def-line indentation level (next top-level def/class/etc.)
    or at EOF.
    """
    if def_lineno < 1 or def_lineno > len(lines):
        return []

    def_line = lines[def_lineno - 1]
    def_indent = len(def_line) - len(def_line.lstrip())

    body: List[str] = []
    for raw in lines[def_lineno:]:  # lines after the def
        stripped = raw.strip()
        if not stripped:
            body.append(raw)  # blank lines are still part of body
            continue
        indent = len(raw) - len(raw.lstrip())
        if indent <= def_indent and stripped:
            # Back to same or outer indentation — body ended
            break
        body.append(raw)
    return body


def _collect_canonical_imports(lines: List[str]) -> Set[str]:
    """
    Scan a file's lines for imports from LTG_TOOL_char_* modules.
    Returns the set of names imported from those modules.

    Handles:
      from LTG_TOOL_char_luma import draw_luma
      from LTG_TOOL_char_luma import draw_luma as _draw_luma_canonical
    """
    imported: Set[str] = set()
    _import_re = re.compile(
        r"from\s+LTG_TOOL_char_\w+\s+import\s+(.+)"
    )
    for line in lines:
        m = _import_re.search(line.strip())
        if not m:
            continue
        # Parse comma-separated imports (possibly with 'as' aliases)
        names_part = m.group(1)
        for part in names_part.split(","):
            part = part.strip()
            if " as " in part:
                # e.g. "draw_luma as _draw_luma_canonical" — capture both
                orig, alias = [x.strip() for x in part.split(" as ", 1)]
                imported.add(orig)
                imported.add(alias)
            else:
                imported.add(part)
    return imported


def _func_body_is_delegate(
    body_lines: List[str],
    canonical_names: Optional[Set[str]] = None,
) -> bool:
    """
    Return True if the function body is a *delegate wrapper* to a canonical
    character module rather than performing inline drawing.

    A body is a delegate when:
      - It does NOT contain direct Cairo ctx.* or PIL draw.* primitive calls
      AND at least one of:
        * It calls a name from canonical_names (imported from LTG_TOOL_char_*)
        * It contains a reference to _draw_*_canonical or LTG_TOOL_char_*

    A body with raw primitives (regardless of canonical refs) = inline = BAD.

    Parameters
    ----------
    body_lines : list[str]
        Lines belonging to the function body.
    canonical_names : set[str] | None
        Names imported from LTG_TOOL_char_* modules in the enclosing file.
    """
    body_text = "\n".join(body_lines)
    has_primitives = bool(
        _CAIRO_PRIMITIVE_RE.search(body_text) or
        _PIL_PRIMITIVE_RE.search(body_text)
    )

    if has_primitives:
        # Contains raw drawing — not a delegate, regardless of canonical refs
        return False

    # Check for canonical module references in the body
    has_canonical_ref = bool(_CANONICAL_CALL_RE.search(body_text))

    # Check if body calls any name imported from a char module
    has_canonical_call = False
    if canonical_names:
        for name in canonical_names:
            if name and re.search(r"\b" + re.escape(name) + r"\s*\(", body_text):
                has_canonical_call = True
                break

    if has_canonical_ref or has_canonical_call:
        # No raw primitives + calls canonical module — it's a delegate wrapper
        return True

    # No raw primitives, no canonical call either — small utility function;
    # treat as delegate if body is trivial (≤ 3 non-blank lines).
    non_blank = [l for l in body_lines if l.strip()]
    return len(non_blank) <= 3


def check_inline_char_drawing(filepath: str) -> List[Dict[str, Any]]:
    """
    Check a single file for inline character drawing patterns.

    False positive prevention (v1.1.0):
    1. Body-part patterns are matched as whole words (draw_eye does not match
       draw_eye_glow).
    2. Per-character function definitions (draw_luma, draw_byte, …) in scene
       generators are only flagged when their function body contains direct
       Cairo ctx.* / PIL draw.* primitive calls.  Thin delegate wrappers that
       call canonical char modules without raw primitives are not flagged.

    Parameters
    ----------
    filepath : str
        Path to a .py file.

    Returns
    -------
    list[dict]
        Each dict: {"line": int, "text": str, "pattern": str, "severity": "WARN"|"INFO"}
        Empty list if no issues found.
    """
    import os

    basename = os.path.basename(filepath)

    # Skip non-scene generators
    is_scene_gen = any(basename.startswith(p) for p in SCENE_GENERATOR_PREFIXES)
    if not is_scene_gen:
        return []

    # Skip if it's also a char module (edge case)
    is_char_module = any(basename.startswith(p) for p in CHAR_MODULE_PREFIXES)
    if is_char_module:
        return []

    issues = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (OSError, UnicodeDecodeError):
        return []

    # Collect names imported from canonical char modules in this file.
    # Used by _func_body_is_delegate to identify delegate calls.
    canonical_names = _collect_canonical_imports(lines)

    # Build word-boundary regexes for body-part patterns (done once)
    _body_part_res = [
        (pat, re.compile(r"\bdef\s+" + re.escape(pat) + r"\b"))
        for pat in INLINE_CHAR_DRAW_PATTERNS
    ]

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Skip comments
        if stripped.startswith("#"):
            continue

        # ── Check 1: body-part function definitions (whole-word match) ─────
        for pat, pat_re in _body_part_res:
            if pat_re.search(stripped):
                issues.append({
                    "line": i,
                    "text": stripped[:120],
                    "pattern": pat,
                    "severity": "WARN",
                })
                break  # at most one body-part hit per line

        # ── Check 2: per-character draw function definitions ────────────────
        # Match "def draw_luma...", "def draw_byte...", etc.
        # glitch(?!kin) prevents draw_glitchkin_swarm from matching the glitch branch.
        char_func_match = re.search(
            r"\bdef\s+(draw_(?:luma|cosmo|miri|byte|glitch(?!kin))\w*)\s*\(", stripped
        )
        if char_func_match:
            func_name = char_func_match.group(1)
            # Don't double-count if already flagged by body-part check above
            already = any(iss["line"] == i for iss in issues)
            if not already:
                # Extract the function body and decide: delegate or inline?
                body = _extract_func_body_lines(lines, i)
                if not _func_body_is_delegate(body, canonical_names=canonical_names):
                    issues.append({
                        "line": i,
                        "text": stripped[:120],
                        "pattern": f"inline:{func_name}",
                        "severity": "WARN",
                    })

    return issues


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    """Validate a char_* module or scan for inline character drawing."""
    import argparse
    import glob
    import os

    parser = argparse.ArgumentParser(
        description="Character interface validator and inline drawing scanner"
    )
    parser.add_argument(
        "--validate", metavar="MODULE",
        help="Validate a char_* module (e.g. char_luma)",
    )
    parser.add_argument(
        "--character", metavar="NAME",
        help="Character name for validation (e.g. luma)",
    )
    parser.add_argument(
        "--scan-inline", metavar="DIR",
        help="Scan directory for inline character drawing in scene generators",
    )
    args = parser.parse_args()

    if args.validate:
        # Add tools dir to path
        tools_dir = os.path.dirname(os.path.abspath(__file__))
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        try:
            mod = __import__(args.validate)
        except ImportError as e:
            print(f"ERROR: Cannot import '{args.validate}': {e}")
            sys.exit(1)
        result = validate_char_module(mod, character=args.character)
        print(f"Module: {result.module_name}")
        print(f"Character: {result.character}")
        print(f"Draw function: {result.draw_func_name}")
        print(f"Status: {'PASS' if result.ok else 'FAIL'}")
        if result.issues:
            print("\nIssues:")
            for iss in result.issues:
                print(f"  FAIL  {iss}")
        if result.warnings:
            print("\nWarnings:")
            for w in result.warnings:
                print(f"  WARN  {w}")
        if result.exports_found:
            print(f"\nExports found: {', '.join(sorted(result.exports_found))}")
        sys.exit(0 if result.ok else 1)

    elif args.scan_inline:
        scan_dir = args.scan_inline
        all_issues = []
        pattern = os.path.join(scan_dir, "*.py")
        for fpath in sorted(glob.glob(pattern)):
            issues = check_inline_char_drawing(fpath)
            if issues:
                all_issues.append((os.path.basename(fpath), issues))

        if all_issues:
            total = sum(len(iss) for _, iss in all_issues)
            print(f"INLINE CHARACTER DRAWING: {total} issue(s) in {len(all_issues)} file(s)")
            print("=" * 72)
            for fname, issues in all_issues:
                print(f"\n  {fname}:")
                for iss in issues:
                    print(f"    L{iss['line']:4d}  [{iss['severity']}]  {iss['text']}")
            sys.exit(1)
        else:
            print("PASS: No inline character drawing found in scene generators.")
            sys.exit(0)

    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
