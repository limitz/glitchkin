#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_char_module_test.py — Modular Character Renderer Validation
Kai Nakamura / Cycle 53

Validates that each char_*.py module conforms to the modular renderer interface:
  1. Module exports the expected draw function with correct signature
  2. Function returns a valid cairo.ImageSurface for each supported expression
  3. Output dimensions are reasonable (20-2560px range)
  4. Alpha channel is clean (no fringing — <5% semi-transparent pixels)

Usage:
  python3 LTG_TOOL_char_module_test.py [--module char_luma.py] [--all] [--json] [--report path.md]

  --module    Path to specific char_*.py module to test
  --all       Auto-discover and test all char_*.py modules in output/tools/
  --json      Output results as JSON
  --report    Write markdown report to specified path

Expected module interface (defined by LTG_TOOL_char_interface.py):
  draw_<character>(expression, pose, scale, facing, scene_lighting) -> cairo.ImageSurface

  Parameters:
    expression:     str — expression name (e.g. "neutral", "happy", "curious")
    pose:           str — pose name (e.g. "standing", "sitting") [default: "standing"]
    scale:          float — render scale factor [default: 1.0]
    facing:         str — "front", "left", "right", "back" [default: "front"]
    scene_lighting: dict or None — lighting parameters [default: None]

  Returns:
    cairo.ImageSurface (FORMAT_ARGB32) with the rendered character.

Author: Kai Nakamura — Cycle 53
Date: 2026-03-31
"""

import sys
import os
import argparse
import json
import importlib
import importlib.util
import inspect
from pathlib import Path

import numpy as np

try:
    import cairo
    _CAIRO_AVAILABLE = True
except ImportError:
    _CAIRO_AVAILABLE = False

# ─── CONFIG ──────────────────────────────────────────────────────────────────

MIN_DIM = 20
MAX_DIM = 2560
MAX_FRINGE_RATIO = 0.05  # max 5% semi-transparent pixels

# Known character module patterns
CHAR_MODULE_PATTERN = "LTG_TOOL_char_*.py"

# Expected draw function name pattern: draw_<character_name>
DRAW_FUNC_PREFIX = "draw_"

# Standard expressions every module should support at minimum
STANDARD_EXPRESSIONS = ["neutral"]

# ─── PATH SETUP ──────────────────────────────────────────────────────────────

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))


# ─── MODULE DISCOVERY ────────────────────────────────────────────────────────

def discover_char_modules(search_dir=None):
    """Find all LTG_TOOL_char_<character>.py modules in the given directory.

    Excludes non-renderer char_ tools (char_spec_lint, char_compare, char_diff,
    char_interface, char_module_test).
    Returns list of Path objects.
    """
    if search_dir is None:
        search_dir = TOOLS_DIR
    search_dir = Path(search_dir)

    # Character renderer modules: LTG_TOOL_char_<name>.py where <name> is a character
    EXCLUDE_SUFFIXES = {"_spec_lint", "_compare", "_diff", "_interface", "_module_test",
                        "_color_enhance"}
    modules = sorted(search_dir.glob("LTG_TOOL_char_*.py"))
    result = []
    for m in modules:
        if not m.is_file():
            continue
        stem = m.stem  # LTG_TOOL_char_luma
        suffix = stem.replace("LTG_TOOL_char", "")  # _luma
        if any(suffix.endswith(ex) for ex in EXCLUDE_SUFFIXES):
            continue
        result.append(m)
    return result


def load_module(module_path):
    """Import a Python module from file path. Returns (module, error_string)."""
    module_path = Path(module_path)
    module_name = module_path.stem

    try:
        spec = importlib.util.spec_from_file_location(module_name, str(module_path))
        if spec is None:
            return None, f"Could not create import spec for {module_path.name}"
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod, None
    except Exception as exc:
        return None, f"Import error: {exc}"


# ─── VALIDATION ──────────────────────────────────────────────────────────────

def find_draw_function(mod):
    """Find the primary draw_* function in a module.

    Returns (func, func_name) or (None, error_string).
    """
    draw_funcs = []
    for name, obj in inspect.getmembers(mod, inspect.isfunction):
        if name.startswith(DRAW_FUNC_PREFIX) and not name.startswith("draw_"):
            continue
        if name.startswith(DRAW_FUNC_PREFIX):
            draw_funcs.append((name, obj))

    if not draw_funcs:
        return None, "No draw_* function found in module"

    # Prefer the function matching the module name pattern
    mod_name = Path(inspect.getfile(mod)).stem
    # LTG_TOOL_char_luma -> draw_luma
    char_name = mod_name.replace("LTG_TOOL_char_", "").replace("char_", "")
    expected_name = DRAW_FUNC_PREFIX + char_name
    for name, func in draw_funcs:
        if name == expected_name:
            return func, name

    # Fall back to first draw_ function
    return draw_funcs[0][1], draw_funcs[0][0]


def check_function_signature(func, func_name):
    """Verify the function accepts the standard parameters.

    Returns list of issues (empty = all OK).
    """
    issues = []
    sig = inspect.signature(func)
    params = list(sig.parameters.keys())

    # Must accept 'expression' as first parameter
    if len(params) < 1:
        issues.append(f"{func_name}() takes no parameters — needs at least 'expression'")
        return issues

    if params[0] != "expression":
        issues.append(f"{func_name}() first parameter is '{params[0]}', expected 'expression'")

    # Check for standard optional parameters
    expected_optionals = {"pose", "scale", "facing", "scene_lighting"}
    param_names = set(params)
    missing_optionals = expected_optionals - param_names

    # Missing optionals are warnings, not errors
    for opt in sorted(missing_optionals):
        issues.append(f"WARN: {func_name}() missing optional parameter '{opt}'")

    return issues


def check_surface_output(func, func_name, expression="neutral"):
    """Call the function and validate the returned surface.

    Returns (result_dict, surface_or_None).
    """
    result = {
        "expression": expression,
        "called": False,
        "returned_surface": False,
        "dimensions_ok": False,
        "alpha_clean": False,
        "width": None,
        "height": None,
        "fringe_ratio": None,
        "issues": [],
        "verdict": "FAIL",
    }

    if not _CAIRO_AVAILABLE:
        result["issues"].append("pycairo not installed — cannot validate surface output")
        return result, None

    # Call the function
    try:
        surface = func(expression=expression)
        result["called"] = True
    except TypeError:
        # Try positional
        try:
            surface = func(expression)
            result["called"] = True
        except Exception as exc:
            result["issues"].append(f"Call failed: {exc}")
            return result, None
    except Exception as exc:
        result["issues"].append(f"Call failed: {exc}")
        return result, None

    # Check return type
    if not isinstance(surface, cairo.ImageSurface):
        result["issues"].append(
            f"Returned {type(surface).__name__}, expected cairo.ImageSurface"
        )
        return result, None

    result["returned_surface"] = True

    # Check dimensions
    w = surface.get_width()
    h = surface.get_height()
    result["width"] = w
    result["height"] = h

    if w < MIN_DIM or h < MIN_DIM:
        result["issues"].append(f"Too small: {w}x{h} (min {MIN_DIM}x{MIN_DIM})")
    elif w > MAX_DIM or h > MAX_DIM:
        result["issues"].append(f"Too large: {w}x{h} (max {MAX_DIM}x{MAX_DIM})")
    else:
        result["dimensions_ok"] = True

    # Check alpha channel cleanliness
    try:
        buf = surface.get_data()
        arr = np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 4).copy()
        alpha = arr[:, :, 3]

        # Count semi-transparent pixels (fringing)
        total_pixels = alpha.size
        # Pixels that are neither fully transparent nor fully opaque
        fringe_pixels = int(np.sum((alpha > 10) & (alpha < 245)))
        fringe_ratio = fringe_pixels / total_pixels if total_pixels > 0 else 0.0
        result["fringe_ratio"] = round(fringe_ratio, 4)

        if fringe_ratio < MAX_FRINGE_RATIO:
            result["alpha_clean"] = True
        else:
            result["issues"].append(
                f"Alpha fringing: {fringe_ratio:.1%} semi-transparent pixels "
                f"(max {MAX_FRINGE_RATIO:.0%})"
            )
    except Exception as exc:
        result["issues"].append(f"Alpha check error: {exc}")

    # Verdict
    if result["returned_surface"] and result["dimensions_ok"] and result["alpha_clean"]:
        result["verdict"] = "PASS"
    elif result["returned_surface"] and result["dimensions_ok"]:
        result["verdict"] = "WARN"  # alpha issue but surface is valid

    return result, surface


def get_supported_expressions(mod):
    """Try to discover supported expressions from the module.

    Checks for EXPRESSIONS, SUPPORTED_EXPRESSIONS, or expressions attribute.
    Falls back to STANDARD_EXPRESSIONS.
    """
    for attr_name in ("EXPRESSIONS", "SUPPORTED_EXPRESSIONS", "expressions"):
        val = getattr(mod, attr_name, None)
        if isinstance(val, (list, tuple)) and len(val) > 0:
            return list(val)
        if isinstance(val, dict) and len(val) > 0:
            return list(val.keys())

    return STANDARD_EXPRESSIONS


# ─── FULL MODULE TEST ────────────────────────────────────────────────────────

def validate_module(module_path):
    """Run full validation on a single char_*.py module.

    Returns dict with all test results.
    """
    module_path = Path(module_path)
    result = {
        "module": module_path.name,
        "path": str(module_path),
        "import_ok": False,
        "function_found": False,
        "function_name": None,
        "signature_issues": [],
        "expressions_tested": [],
        "expression_results": [],
        "overall": "FAIL",
    }

    # Step 1: Import
    mod, err = load_module(module_path)
    if err:
        result["import_error"] = err
        return result
    result["import_ok"] = True

    # Step 2: Find draw function
    func_or_err, name_or_msg = find_draw_function(mod)
    if func_or_err is None:
        result["function_error"] = name_or_msg
        return result
    result["function_found"] = True
    result["function_name"] = name_or_msg
    func = func_or_err
    func_name = name_or_msg

    # Step 3: Check signature
    sig_issues = check_function_signature(func, func_name)
    result["signature_issues"] = sig_issues

    # Step 4: Get expressions to test
    expressions = get_supported_expressions(mod)
    result["expressions_tested"] = expressions

    # Step 5: Test each expression
    pass_count = 0
    warn_count = 0
    fail_count = 0

    for expr in expressions:
        expr_result, _ = check_surface_output(func, func_name, expr)
        result["expression_results"].append(expr_result)

        if expr_result["verdict"] == "PASS":
            pass_count += 1
        elif expr_result["verdict"] == "WARN":
            warn_count += 1
        else:
            fail_count += 1

    result["pass"] = pass_count
    result["warn"] = warn_count
    result["fail"] = fail_count

    # Overall verdict
    has_sig_errors = any(not i.startswith("WARN:") for i in sig_issues)
    if fail_count > 0 or has_sig_errors:
        result["overall"] = "FAIL"
    elif warn_count > 0 or sig_issues:
        result["overall"] = "WARN"
    else:
        result["overall"] = "PASS"

    return result


def validate_all(search_dir=None):
    """Discover and validate all char_*.py modules.

    Returns list of per-module result dicts.
    """
    modules = discover_char_modules(search_dir)
    results = []

    if not modules:
        print("[char_module_test] No char_*.py modules found.")
        return results

    for mod_path in modules:
        print(f"[char_module_test] Testing {mod_path.name}...")
        result = validate_module(mod_path)
        results.append(result)
        print(f"  → {result['overall']}")

    return results


# ─── REPORT ──────────────────────────────────────────────────────────────────

def format_report(results, run_ts=None):
    """Format results as Markdown report."""
    import datetime
    if run_ts is None:
        run_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "# Modular Character Renderer Validation Report",
        "",
        f"**Run date:** {run_ts}",
        f"**Script:** LTG_TOOL_char_module_test.py v1.0.0",
        f"**Modules tested:** {len(results)}",
        "",
    ]

    if not results:
        lines.append("_No char_*.py modules found to test._")
        return "\n".join(lines)

    # Summary table
    pass_total = sum(1 for r in results if r["overall"] == "PASS")
    warn_total = sum(1 for r in results if r["overall"] == "WARN")
    fail_total = sum(1 for r in results if r["overall"] == "FAIL")

    lines.append(f"**PASS: {pass_total}  WARN: {warn_total}  FAIL: {fail_total}**")
    lines.append("")
    lines.append("| Module | Function | Expressions | Result |")
    lines.append("|---|---|---|---|")

    for r in results:
        func = r.get("function_name", "?")
        n_expr = len(r.get("expressions_tested", []))
        lines.append(f"| {r['module']} | {func} | {n_expr} | {r['overall']} |")

    lines.append("")

    # Detail sections
    for r in results:
        lines.append(f"## {r['module']}")
        lines.append("")

        if not r["import_ok"]:
            lines.append(f"**FAIL — Import error:** {r.get('import_error', '?')}")
            lines.append("")
            continue

        if not r["function_found"]:
            lines.append(f"**FAIL — No draw function:** {r.get('function_error', '?')}")
            lines.append("")
            continue

        lines.append(f"- Function: `{r['function_name']}()`")

        if r["signature_issues"]:
            lines.append("- Signature issues:")
            for issue in r["signature_issues"]:
                lines.append(f"  - {issue}")

        lines.append(f"- Expressions tested: {', '.join(r.get('expressions_tested', []))}")
        lines.append("")

        for er in r.get("expression_results", []):
            expr = er["expression"]
            v = er["verdict"]
            dims = f"{er['width']}x{er['height']}" if er["width"] else "?"
            fringe = f"{er['fringe_ratio']:.1%}" if er.get("fringe_ratio") is not None else "?"
            lines.append(f"### Expression: {expr} — {v}")
            lines.append(f"  - Returned surface: {er['returned_surface']}")
            lines.append(f"  - Dimensions: {dims}  |  Alpha fringe: {fringe}")
            if er["issues"]:
                for issue in er["issues"]:
                    lines.append(f"  - {issue}")
            lines.append("")

    return "\n".join(lines)


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="LTG Modular Character Renderer Validation"
    )
    parser.add_argument("--module", type=str,
                        help="Path to specific char_*.py module to test")
    parser.add_argument("--all", action="store_true",
                        help="Auto-discover and test all char_*.py modules")
    parser.add_argument("--search-dir", type=str, default=None,
                        help="Directory to search for char_*.py modules (default: output/tools/)")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON")
    parser.add_argument("--report", type=str, default=None,
                        help="Write markdown report to specified path")
    args = parser.parse_args()

    if not _CAIRO_AVAILABLE:
        print("[char_module_test] ERROR: pycairo not installed. Cannot validate cairo surfaces.")
        sys.exit(2)

    if args.module:
        results = [validate_module(args.module)]
    elif args.all or True:  # default to --all
        results = validate_all(args.search_dir)
    else:
        results = validate_all(args.search_dir)

    if args.json:
        print(json.dumps(results, indent=2, default=str))
    elif args.report:
        report = format_report(results)
        Path(args.report).write_text(report, encoding="utf-8")
        print(f"[char_module_test] Report written to: {args.report}")
    else:
        # Print summary
        for r in results:
            func = r.get("function_name", "?")
            print(f"  {r['module']}: {r['overall']} (func={func}, "
                  f"pass={r.get('pass', 0)}, warn={r.get('warn', 0)}, fail={r.get('fail', 0)})")

    # Exit code
    if any(r["overall"] == "FAIL" for r in results):
        sys.exit(2)
    elif any(r["overall"] == "WARN" for r in results):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
