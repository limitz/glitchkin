#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_batch_path_migrate.py — Batch Hardcoded Path Migration Tool
"Luma & the Glitchkin" — Environment & Background / Hana Okonkwo / Cycle 47

Scans all Python files in output/tools/ for hardcoded /home/wipkat/team paths
and generates a migration report. Optionally applies safe automatic migrations
for the most common pattern (output path assignment).

This tool does NOT blindly sed-replace. It classifies each occurrence:
  - SAFE_AUTO:      single output path assignment → can auto-migrate to output_dir()
  - SAFE_MANUAL:    docstring/comment reference → cosmetic only, low risk
  - SAFE_FALLBACK:  ImportError fallback def for output_dir() → correct pattern, no action needed
  - SAFE_LITERAL:   string literal inside except/try block or advisory message → cosmetic, no action
  - NEEDS_REVIEW:   complex expression, multi-use, or non-output path → manual only

C49 update (Hana Okonkwo): added SAFE_FALLBACK and SAFE_LITERAL classifications.
  ~65 former NEEDS_REVIEW items were ImportError fallback defs — reclassified as SAFE_FALLBACK.
  Advisory message strings and subprocess script paths reclassified as SAFE_LITERAL.

Usage:
    python3 LTG_TOOL_batch_path_migrate.py                    # dry-run report
    python3 LTG_TOOL_batch_path_migrate.py --apply             # apply SAFE_AUTO only
    python3 LTG_TOOL_batch_path_migrate.py --report-json       # JSON report

Dependencies: none (stdlib only)
"""

import os
import re
import sys
import json
import argparse
import pathlib

# ── Constants ──────────────────────────────────────────────────────────────────
TOOLS_DIR = pathlib.Path(__file__).resolve().parent
HARDCODED_PREFIX = "/home/wipkat/team/"
OUTPUT_PREFIX = "/home/wipkat/team/output/"

# Pattern: variable = "/home/wipkat/team/output/..."
RE_OUTPUT_ASSIGN = re.compile(
    r'^(\s*)([\w.]+)\s*=\s*["\'](' + re.escape(OUTPUT_PREFIX) + r'[^"\']+)["\']\s*$'
)

# Pattern: in docstring or comment
RE_COMMENT = re.compile(r'^\s*#')
RE_DOCSTRING_LINE = re.compile(r'^\s*("""|\'\'\'|[^=]*' + re.escape(HARDCODED_PREFIX) + r')')

# Pattern: ImportError fallback def for output_dir (the correct migration pattern)
# Matches: def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)
RE_FALLBACK_DEF = re.compile(
    r'^\s+def\s+output_dir\(\*parts\)\s*:\s*return\s+pathlib\.Path\(["\']'
    + re.escape(OUTPUT_PREFIX.rstrip('/'))
    + r'["\']\)\.joinpath\(\*parts\)'
)
# Also match: return pathlib.Path("/home/wipkat/team/output").joinpath(*parts) on its own line
RE_FALLBACK_RETURN = re.compile(
    r'^\s+return\s+pathlib\.Path\(["\']'
    + re.escape(OUTPUT_PREFIX.rstrip('/'))
    + r'["\']\)\.joinpath\(\*parts\)'
)
# Pattern: ensure_dir fallback
RE_FALLBACK_ENSURE = re.compile(
    r'^\s+def\s+ensure_dir\('
)

# Pattern: BASE = "/home/wipkat/team/output" (standalone base assignment — known pattern)
RE_BASE_ASSIGN = re.compile(
    r'^\s*\w+\s*=\s*["\']' + re.escape(OUTPUT_PREFIX.rstrip('/')) + r'["\']\s*$'
)

# Pattern: string literal path inside a list, tuple, or function call (e.g. subprocess script paths)
RE_STRING_LITERAL_PATH = re.compile(
    r'^\s*["\']' + re.escape(HARDCODED_PREFIX) + r'[^"\']*["\']\s*,?\s*$'
)

# Pattern: advisory/message string containing the path (e.g. lines.append("... /home/wipkat/...")
RE_ADVISORY_STRING = re.compile(
    r'^\s*\w+\.append\(|^\s*print\(|^\s*.*["\'].*→.*' + re.escape(HARDCODED_PREFIX)
)

# Pattern: any hardcoded path
RE_ANY_HARDCODED = re.compile(re.escape(HARDCODED_PREFIX))


def classify_line(line, lineno, in_docstring):
    """Classify a line containing a hardcoded path."""
    stripped = line.strip()

    # Check if inside docstring or is a comment
    if in_docstring or stripped.startswith('#'):
        return "SAFE_MANUAL", "docstring/comment reference"

    # Check for ImportError fallback definitions — these ARE the correct migration pattern.
    # Files that already have try/except ImportError with a fallback def output_dir(*)
    # using the hardcoded path are fully migrated; the fallback is intentional.
    if RE_FALLBACK_DEF.match(line):
        return "SAFE_FALLBACK", "ImportError fallback def output_dir() — correct pattern"
    if RE_FALLBACK_RETURN.match(line):
        return "SAFE_FALLBACK", "ImportError fallback return — correct pattern"

    # Check for simple output path assignment
    m = RE_OUTPUT_ASSIGN.match(line)
    if m:
        indent, varname, path = m.group(1), m.group(2), m.group(3)
        rel = path[len(OUTPUT_PREFIX):]
        parts = rel.split('/')
        return "SAFE_AUTO", f"{varname} = output_dir({', '.join(repr(p) for p in parts)})"

    # Check for BASE = "/home/wipkat/team/output" standalone assignments
    if RE_BASE_ASSIGN.match(line):
        return "NEEDS_REVIEW", "BASE-style assignment — migrate to output_dir()"

    # Check for string literal paths in lists (e.g. subprocess script references)
    if RE_STRING_LITERAL_PATH.match(stripped):
        return "SAFE_LITERAL", "string literal path in list/call — cosmetic reference"

    # Check for advisory/message strings
    if RE_ADVISORY_STRING.match(stripped):
        return "SAFE_LITERAL", "advisory/log message containing path — cosmetic"

    # Everything else needs manual review
    return "NEEDS_REVIEW", "complex expression or non-standard pattern"


def scan_file(filepath):
    """Scan a single Python file for hardcoded paths."""
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except Exception:
        return results

    in_docstring = False
    docstring_char = None

    for i, line in enumerate(lines):
        # Track docstring state
        for ds in ['"""', "'''"]:
            count = line.count(ds)
            if count > 0:
                if not in_docstring:
                    in_docstring = True
                    docstring_char = ds
                    if count >= 2:
                        in_docstring = False
                elif ds == docstring_char:
                    in_docstring = False

        if RE_ANY_HARDCODED.search(line):
            classification, detail = classify_line(line, i + 1, in_docstring)
            results.append({
                "file": str(filepath),
                "line": i + 1,
                "content": line.rstrip(),
                "classification": classification,
                "detail": detail,
            })

    return results


def scan_all():
    """Scan all Python files in tools directory."""
    all_results = []
    for f in sorted(TOOLS_DIR.glob("*.py")):
        if f.name == pathlib.Path(__file__).name:
            continue  # skip self
        results = scan_file(f)
        if results:
            all_results.extend(results)
    return all_results


def apply_safe_auto(results):
    """Apply SAFE_AUTO migrations. Returns count of files modified."""
    # Group by file
    by_file = {}
    for r in results:
        if r["classification"] == "SAFE_AUTO":
            by_file.setdefault(r["file"], []).append(r)

    modified = 0
    for filepath, items in by_file.items():
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        changed = False
        for item in items:
            lineno = item["line"] - 1
            line = lines[lineno]
            m = RE_OUTPUT_ASSIGN.match(line)
            if m:
                indent, varname, path = m.group(1), m.group(2), m.group(3)
                rel = path[len(OUTPUT_PREFIX):]
                parts = rel.split('/')
                new_line = f'{indent}{varname} = output_dir({", ".join(repr(p) for p in parts)})\n'
                lines[lineno] = new_line
                changed = True

        if changed:
            # Check if import already exists
            content = ''.join(lines)
            if 'from LTG_TOOL_project_paths import' not in content:
                # Find first non-comment, non-docstring import line
                insert_idx = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        insert_idx = i
                        break
                import_block = (
                    "try:\n"
                    "    from LTG_TOOL_project_paths import output_dir, ensure_dir  # noqa: E402\n"
                    "except ImportError:\n"
                    "    import pathlib\n"
                    '    def output_dir(*parts): return pathlib.Path("/home/wipkat/team/output").joinpath(*parts)\n'
                    "    def ensure_dir(path): path.mkdir(parents=True, exist_ok=True); return path\n"
                )
                lines.insert(insert_idx, import_block)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            modified += 1

    return modified


def print_report(results):
    """Print human-readable report."""
    counts = {"SAFE_AUTO": 0, "SAFE_MANUAL": 0, "SAFE_FALLBACK": 0, "SAFE_LITERAL": 0, "NEEDS_REVIEW": 0}
    for r in results:
        counts[r["classification"]] = counts.get(r["classification"], 0) + 1

    total = len(results)
    files = len(set(r["file"] for r in results))

    print("=" * 72)
    print("LTG Batch Path Migration Report")
    print(f"  Total occurrences: {total}  in {files} files")
    print(f"  SAFE_AUTO: {counts['SAFE_AUTO']}  SAFE_MANUAL: {counts['SAFE_MANUAL']}  SAFE_FALLBACK: {counts['SAFE_FALLBACK']}  SAFE_LITERAL: {counts['SAFE_LITERAL']}  NEEDS_REVIEW: {counts['NEEDS_REVIEW']}")
    print("=" * 72)

    current_file = None
    for r in results:
        if r["file"] != current_file:
            current_file = r["file"]
            print(f"\n  {pathlib.Path(current_file).name}")
        tag = r["classification"]
        print(f"    L{r['line']:4d} [{tag:13s}] {r['detail']}")
        if tag == "NEEDS_REVIEW":
            print(f"         {r['content'].strip()[:80]}")

    print("\n" + "=" * 72)
    if counts["SAFE_AUTO"] > 0:
        print(f"Run with --apply to auto-migrate {counts['SAFE_AUTO']} SAFE_AUTO occurrences.")
    print("=" * 72)


def main():
    parser = argparse.ArgumentParser(description="Batch hardcoded path migration tool")
    parser.add_argument("--apply", action="store_true", help="Apply SAFE_AUTO migrations")
    parser.add_argument("--report-json", action="store_true", help="Output JSON report")
    args = parser.parse_args()

    results = scan_all()

    if args.report_json:
        print(json.dumps(results, indent=2))
        return

    print_report(results)

    if args.apply:
        n = apply_safe_auto(results)
        print(f"\nApplied SAFE_AUTO migrations to {n} file(s).")
        print("Run generators to verify, then commit.")


if __name__ == "__main__":
    main()
