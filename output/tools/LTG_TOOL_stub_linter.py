#!/usr/bin/env python3
"""
LTG_TOOL_stub_linter.py
Stub Integrity Linter — "Luma & the Glitchkin"
Author: Kai Nakamura / Cycle 33

Scans all .py files in output/tools/ for broken imports — specifically any
`import LTG_CHAR_*`, `import LTG_COLOR_*`, `import LTG_BRAND_*`, or
`from LTG_CHAR_* import ...` etc. that reference deleted originals (non-LTG_TOOL_
prefixed files).

For each broken import, reports:
  - Which file contains the broken import
  - The import statement text
  - Whether a canonical LTG_TOOL_* replacement is detectable
  - Whether the target file exists on disk

Usage:
    python LTG_TOOL_stub_linter.py [directory]
    python LTG_TOOL_stub_linter.py --pre-commit

API:
    from LTG_TOOL_stub_linter import lint_directory, format_report

    results = lint_directory("/path/to/output/tools")
    print(format_report(results))
"""

__version__ = "1.0.0"

import os
import re
import sys

# Patterns that look like old-style (non-LTG_TOOL_) module imports
_IMPORT_PATTERNS = [
    # import LTG_CHAR_xxx, import LTG_COLOR_xxx, import LTG_BRAND_xxx
    re.compile(r'^\s*import\s+(LTG_(?:CHAR|COLOR|BRAND|ENV)_\S+)', re.MULTILINE),
    # from LTG_CHAR_xxx import ...
    re.compile(r'^\s*from\s+(LTG_(?:CHAR|COLOR|BRAND|ENV)_\S+)\s+import', re.MULTILINE),
]

# Pattern for detecting forwarding / alias imports that reference LTG_TOOL_* directly
# These are valid and should not be flagged
_VALID_TOOL_IMPORT = re.compile(r'LTG_TOOL_')


def _module_to_filename(module_name):
    """Convert a Python module name to a .py filename."""
    # strip any trailing 'as _xxx' type suffixes that may have leaked in
    module_name = module_name.strip().split()[0]
    return module_name + ".py"


def _find_canonical_replacement(module_name, tools_dir):
    """
    Given a non-LTG_TOOL_ module name like LTG_CHAR_luma_expression_sheet_v005,
    attempt to find the matching LTG_TOOL_* canonical on disk.

    Strategy: strip the category prefix (LTG_CHAR_/LTG_COLOR_/etc.) and look for
    LTG_TOOL_<rest>.py in tools_dir.

    Returns (canonical_name, exists_on_disk) or (None, False).
    """
    # e.g. LTG_CHAR_luma_expression_sheet_v005 -> luma_expression_sheet_v005
    m = re.match(r'^LTG_(?:CHAR|COLOR|BRAND|ENV)_(.*)', module_name)
    if not m:
        return None, False
    stem = m.group(1)
    canonical = f"LTG_TOOL_{stem}"
    filename = canonical + ".py"
    exists = os.path.isfile(os.path.join(tools_dir, filename))
    return canonical, exists


def lint_file(filepath, tools_dir=None):
    """
    Lint a single Python file for broken old-style imports.

    Parameters
    ----------
    filepath : str
        Absolute path to the .py file to lint.
    tools_dir : str or None
        Directory to search for canonical replacements. Defaults to the file's
        parent directory.

    Returns
    -------
    dict with keys:
        file        : str  — absolute path
        issues      : list of dicts, each with:
                        line_no     : int
                        statement   : str (full import line stripped)
                        module      : str (imported module name)
                        target_exists : bool (does the .py file exist on disk?)
                        canonical   : str or None
                        canonical_exists : bool
        status      : "PASS" | "WARN" | "ERROR"
            PASS  — no broken imports
            WARN  — imports found but target file exists on disk (may still work)
            ERROR — imports found AND target file is missing from disk
    """
    if tools_dir is None:
        tools_dir = os.path.dirname(os.path.abspath(filepath))

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as fh:
            source = fh.read()
    except OSError as exc:
        return {
            "file": filepath,
            "issues": [],
            "status": "ERROR",
            "read_error": str(exc),
        }

    lines = source.splitlines()
    issues = []

    for pattern in _IMPORT_PATTERNS:
        for match in pattern.finditer(source):
            raw_module = match.group(1).strip()
            # Skip if it contains LTG_TOOL_ (valid)
            if _VALID_TOOL_IMPORT.search(raw_module):
                continue

            # Find line number
            line_no = source[:match.start()].count('\n') + 1
            statement = lines[line_no - 1].strip() if line_no <= len(lines) else match.group(0).strip()

            target_file = _module_to_filename(raw_module)
            target_exists = os.path.isfile(os.path.join(tools_dir, target_file))

            canonical, canonical_exists = _find_canonical_replacement(raw_module, tools_dir)

            issues.append({
                "line_no": line_no,
                "statement": statement,
                "module": raw_module,
                "target_exists": target_exists,
                "canonical": canonical,
                "canonical_exists": canonical_exists,
            })

    if not issues:
        status = "PASS"
    elif any(not iss["target_exists"] for iss in issues):
        status = "ERROR"
    else:
        status = "WARN"

    return {
        "file": filepath,
        "issues": issues,
        "status": status,
    }


def lint_directory(directory, pattern="*.py", skip_legacy=True):
    """
    Lint all Python files in a directory.

    Parameters
    ----------
    directory : str
        Directory to scan.
    pattern : str
        Glob pattern (default "*.py").
    skip_legacy : bool
        If True (default), skips the legacy/ subdirectory.

    Returns
    -------
    list of result dicts from lint_file().
    """
    import fnmatch
    results = []
    for fname in sorted(os.listdir(directory)):
        if skip_legacy and fname == "legacy":
            continue
        if not fnmatch.fnmatch(fname, pattern):
            continue
        fpath = os.path.join(directory, fname)
        if not os.path.isfile(fpath):
            continue
        results.append(lint_file(fpath, tools_dir=directory))
    return results


def format_report(results, include_pass=False):
    """
    Format a list of lint results into a human-readable report string.

    Parameters
    ----------
    results : list of dicts from lint_file() / lint_directory()
    include_pass : bool
        If True, also lists PASS files. Default False (only WARN/ERROR).

    Returns
    -------
    str
    """
    lines = []
    lines.append("=" * 70)
    lines.append("LTG Stub Integrity Linter — Report")
    lines.append(f"Files scanned: {len(results)}")
    errors  = [r for r in results if r["status"] == "ERROR"]
    warns   = [r for r in results if r["status"] == "WARN"]
    passes  = [r for r in results if r["status"] == "PASS"]
    lines.append(f"  PASS : {len(passes)}")
    lines.append(f"  WARN : {len(warns)}")
    lines.append(f"  ERROR: {len(errors)}")
    lines.append("=" * 70)

    for result in results:
        status = result["status"]
        if status == "PASS" and not include_pass:
            continue
        fname = os.path.basename(result["file"])
        lines.append(f"\n[{status}] {fname}")

        if "read_error" in result:
            lines.append(f"  READ ERROR: {result['read_error']}")
            continue

        for iss in result.get("issues", []):
            lines.append(f"  Line {iss['line_no']:>4}: {iss['statement']}")
            lines.append(f"           Module  : {iss['module']}")
            lines.append(f"           On disk : {'YES' if iss['target_exists'] else 'NO  <-- MISSING'}")
            if iss["canonical"]:
                ck = "EXISTS" if iss["canonical_exists"] else "NOT FOUND"
                lines.append(f"           Canonical candidate: {iss['canonical']} ({ck})")
            else:
                lines.append(f"           Canonical candidate: (none identified)")

    lines.append("\n" + "=" * 70)
    if errors:
        lines.append("ACTION REQUIRED: The ERROR files above have broken imports —")
        lines.append("their imported modules are missing from disk. Fix before running.")
    elif warns:
        lines.append("WARN: Imports reference non-LTG_TOOL_ modules; files exist on disk")
        lines.append("but consider migrating to canonical LTG_TOOL_ equivalents.")
    else:
        lines.append("All scanned files pass stub integrity check.")
    lines.append("=" * 70)

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="LTG Stub Integrity Linter v1.0.0 — scan for broken imports"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=os.path.dirname(os.path.abspath(__file__)),
        help="Directory to scan (default: this file's directory)"
    )
    parser.add_argument(
        "--include-pass", action="store_true",
        help="Include PASS files in report output"
    )
    parser.add_argument(
        "--pre-commit", action="store_true",
        help="Exit with code 1 if any ERROR results found (for CI/pre-commit use)"
    )
    parser.add_argument(
        "--include-legacy", action="store_true",
        help="Also scan the legacy/ subdirectory"
    )
    parser.add_argument(
        "--save-report", metavar="PATH",
        help="Save report to this path instead of printing to stdout"
    )
    args = parser.parse_args()

    results = lint_directory(
        args.directory,
        skip_legacy=not args.include_legacy,
    )
    report = format_report(results, include_pass=args.include_pass)

    if args.save_report:
        with open(args.save_report, 'w', encoding='utf-8') as fh:
            fh.write(report)
        print(f"Report saved to: {args.save_report}")
    else:
        print(report)

    if args.pre_commit:
        errors = [r for r in results if r["status"] == "ERROR"]
        if errors:
            print(f"\nPRE-COMMIT FAIL: {len(errors)} broken stub(s) found.", file=sys.stderr)
            sys.exit(1)
        else:
            sys.exit(0)


if __name__ == "__main__":
    main()
