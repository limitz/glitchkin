#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_char_interface.py
Character Renderer Interface Contract — v1.0.0
"Luma & the Glitchkin" — Cycle 53 / Morgan Walsh

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
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

__version__ = "1.0.0"

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
# NOT in scene generators (style frames, storyboard panels, etc.)
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

# Additional per-character draw function patterns in scene generators
# These indicate inline character rendering (should be imported from char_*)
INLINE_CHAR_FUNC_PATTERNS = [
    r"def draw_luma",
    r"def draw_cosmo",
    r"def draw_miri",
    r"def draw_byte",
    r"def draw_glitch",
]


def check_inline_char_drawing(filepath: str) -> List[Dict[str, Any]]:
    """
    Check a single file for inline character drawing patterns.

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
    import re

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

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Skip comments and strings
        if stripped.startswith("#"):
            continue
        # Check for inline body part drawing function definitions
        for pattern in INLINE_CHAR_DRAW_PATTERNS:
            if f"def {pattern}" in stripped:
                issues.append({
                    "line": i,
                    "text": stripped[:120],
                    "pattern": pattern,
                    "severity": "WARN",
                })
        # Check for character-specific inline draw functions
        for pat in INLINE_CHAR_FUNC_PATTERNS:
            if re.search(pat, stripped):
                # Don't double-count if already caught by body part patterns
                already = any(iss["line"] == i for iss in issues)
                if not already:
                    issues.append({
                        "line": i,
                        "text": stripped[:120],
                        "pattern": pat,
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
