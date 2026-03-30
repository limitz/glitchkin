# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_face_curves_caller_audit.py
Face Curves Caller Audit — "Luma & the Glitchkin"
Author: Kai Nakamura / Cycle 42
Purpose: Scan all LTG_TOOL_*.py generators for inline Luma face drawing code
         and identify migration candidates for the draw_luma_face() bezier API.

Background
----------
LTG_TOOL_luma_face_curves.py v1.1.0 (C41) defines the canonical bezier face
system for Luma — 9 expressions, spec v002, 100px canonical eye width.
As of C42, no generators import draw_luma_face(); all use inline ad-hoc drawing.

This tool produces a migration readiness report:
  - USING_API: already uses draw_luma_face() from luma_face_curves module
  - INLINE_CANDIDATE: has inline Luma face drawing — candidate for migration
  - NO_LUMA_FACE: no inline Luma face drawing found — skip

Usage
-----
    python LTG_TOOL_face_curves_caller_audit.py [tools_dir] [--save-report PATH]

    tools_dir   Path to output/tools/ directory. Default: same dir as this script.
    --save-report PATH   Write report to file (default: LTG_TOOL_face_curves_caller_audit_report.txt)

API
---
    from LTG_TOOL_face_curves_caller_audit import audit_directory, format_report

    results = audit_directory("/path/to/output/tools/")
    print(format_report(results))

Inline Face Drawing Detection Patterns
--------------------------------------
The audit looks for:
  1. Import of draw_luma_face / luma_face_curves (API usage)
  2. Function definitions containing "luma" + "face" in the name
  3. Eye-width constants: eye_w=N, EW_CANON, ew=N, eye_sep=N
  4. Named expressions for Luma: RECKLESS, THE_NOTICING, WORRIED, ALARMED,
     FRUSTRATED, DETERMINED, CONFIDENT, SOFT_SURPRISE — in a Luma context
  5. References to face_center / fc / head_cy alongside oval/blush/eye draw calls

Migration Readiness Criteria
-----------------------------
READY_HIGH:    Uses proportion-scaling (HR/s or canvas-relative). Bezier API
               accepts fc=(cx, cy) at any scale — migration is a wrapper call.

READY_MEDIUM:  Uses absolute pixel coords for a known canvas size.
               Needs rescaling constants but structure maps well.

READY_LOW:     Complex inline system with many expressions, expression params,
               or expression dicts. Replacement requires significant refactor;
               the bezier API may not cover all expressions needed.

NOT_APPLICABLE: Not a Luma face generator (e.g. storyboard panel drawing Miri
                or Cosmo, or a CI/lint tool with face-related text in docstrings).

Changelog
---------
v1.0.0 (C42): Initial implementation. Static regex analysis — no AST/execution.
"""

from __future__ import annotations

__version__ = "1.0.0"

import os
import re
import sys
import glob as glob_module
from typing import List, Dict, Any

# ── Detection Patterns ────────────────────────────────────────────────────────

# Pattern 1: API import from face_curves module
_RE_API_IMPORT = re.compile(
    r'from\s+LTG_TOOL_luma_face_curves\s+import|'
    r'import\s+LTG_TOOL_luma_face_curves|'
    r'draw_luma_face\s*\('
)

# Pattern 2: Inline function defs with luma + face in name
_RE_INLINE_FACE_FN = re.compile(
    r'def\s+(_draw_luma_face\w*|draw_luma_face_\w+|_draw_luma_head\b|'
    r'_draw_\w+_face\b|_draw_luma_expression\w*)',
    re.IGNORECASE
)

# Pattern 3: Luma expression name references (in a draw context)
_RE_EXPRESSION_NAMES = re.compile(
    r'\b(RECKLESS|THE_NOTICING|WORRIED|ALARMED|FRUSTRATED|DETERMINED|'
    r'CONFIDENT|SOFT_SURPRISE|DELIGHTED|EXCITED)\b'
)

# Pattern 4: Eye geometry constants typical of Luma
_RE_EYE_GEOMETRY = re.compile(
    r'EW_CANON\s*=|eye_w\s*=\s*\d|ew\s*=\s*\d{2,3}\b|'
    r'eye_half\s*=|EYE_W\s*=\s*\d'
)

# Pattern 5: draw_eyes_full or similar compound face helpers
_RE_DRAW_EYES = re.compile(
    r'def\s+draw_eyes_full|def\s+draw_eyes\b|draw_eyes_full\s*\('
)

# Pattern 6: "luma" context keywords suggesting this is a Luma file
_RE_LUMA_CONTEXT = re.compile(
    r'\bluma\b|\bLuma\b|\bLUMA\b',
    re.IGNORECASE
)

# Pattern 7: Proportion system (HR/scale-based = READY_HIGH)
_RE_PROPORTION_SCALE = re.compile(
    r'\bHR\s*=\s*HEAD_R\s*\*|HR\s*/\s*100|s\s*=\s*HR\s*/\s*100|'
    r'RENDER_SCALE\s*=\s*\d'
)

# Pattern 8: Absolute pixel coords (canvas-specific = READY_MEDIUM)
_RE_ABSOLUTE_PIXELS = re.compile(
    r'face_cx\s*=\s*\d{2,4}|fc\s*=\s*\(\s*\d{3}|head_cy\s*=\s*\d{2,4}'
)

# ── Audit Logic ───────────────────────────────────────────────────────────────

def audit_file(filepath: str) -> Dict[str, Any]:
    """
    Audit a single Python file for Luma face drawing patterns.

    Parameters
    ----------
    filepath : str — path to .py file

    Returns
    -------
    dict with keys:
        file          : str — basename
        filepath      : str — full path
        status        : "USING_API" | "INLINE_CANDIDATE" | "NO_LUMA_FACE"
        readiness     : "READY_HIGH" | "READY_MEDIUM" | "READY_LOW" | "NOT_APPLICABLE" | None
        api_imports   : list[str] — lines matching API import pattern
        inline_fns    : list[str] — inline face function definitions found
        expression_refs : list[str] — expression names found
        eye_geometry  : list[str] — eye geometry constant lines found
        notes         : list[str] — human-readable observations
    """
    basename = os.path.basename(filepath)
    result = {
        "file": basename,
        "filepath": filepath,
        "status": "NO_LUMA_FACE",
        "readiness": None,
        "api_imports": [],
        "inline_fns": [],
        "expression_refs": [],
        "eye_geometry": [],
        "notes": [],
    }

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
            source = fh.read()
    except OSError as exc:
        result["notes"].append(f"READ ERROR: {exc}")
        return result

    lines = source.splitlines()

    # Check API usage
    for i, line in enumerate(lines, 1):
        if _RE_API_IMPORT.search(line):
            result["api_imports"].append(f"L{i}: {line.strip()}")

    # Check inline face functions
    for i, line in enumerate(lines, 1):
        if _RE_INLINE_FACE_FN.search(line):
            result["inline_fns"].append(f"L{i}: {line.strip()}")

    # Check expression name references
    expr_seen = set()
    for i, line in enumerate(lines, 1):
        for m in _RE_EXPRESSION_NAMES.finditer(line):
            name = m.group(1)
            if name not in expr_seen:
                expr_seen.add(name)
                result["expression_refs"].append(f"L{i}: {name}")

    # Check eye geometry
    for i, line in enumerate(lines, 1):
        if _RE_EYE_GEOMETRY.search(line):
            result["eye_geometry"].append(f"L{i}: {line.strip()}")
        if _RE_DRAW_EYES.search(line):
            result["eye_geometry"].append(f"L{i}: {line.strip()}")

    # Determine status
    has_luma_context = bool(_RE_LUMA_CONTEXT.search(source))

    if result["api_imports"]:
        result["status"] = "USING_API"
        result["readiness"] = "NOT_APPLICABLE"
        result["notes"].append("Already using draw_luma_face() API — no migration needed.")
        return result

    if result["inline_fns"] or (result["eye_geometry"] and has_luma_context):
        result["status"] = "INLINE_CANDIDATE"
    elif result["expression_refs"] and has_luma_context:
        # Expression names present but no explicit face drawing — may be params/data only
        result["status"] = "INLINE_CANDIDATE"
        result["notes"].append(
            "Expression names found in Luma context — verify if inline face drawing is present."
        )
    else:
        result["status"] = "NO_LUMA_FACE"
        result["readiness"] = "NOT_APPLICABLE"
        return result

    # Determine readiness for INLINE_CANDIDATE
    uses_proportion = bool(_RE_PROPORTION_SCALE.search(source))
    uses_absolute = bool(_RE_ABSOLUTE_PIXELS.search(source))
    n_expressions = len(expr_seen)

    if uses_proportion and n_expressions <= 2:
        result["readiness"] = "READY_HIGH"
        result["notes"].append(
            "Proportional coordinate system (HR/s) detected — bezier API wraps cleanly. "
            "Low expression count; migration is a bounded replacement."
        )
    elif uses_proportion and n_expressions > 2:
        result["readiness"] = "READY_MEDIUM"
        result["notes"].append(
            f"Proportional system detected but {n_expressions} expression variants found. "
            "Each expression must map to a bezier delta — verify coverage in luma_face_curves v1.1.0 "
            "before migrating."
        )
    elif uses_absolute:
        result["readiness"] = "READY_MEDIUM"
        result["notes"].append(
            "Absolute pixel coords detected. Canvas-specific values need rescaling to "
            "600px face-curves coordinate space. Migration possible but requires arithmetic."
        )
    else:
        result["readiness"] = "READY_LOW"
        result["notes"].append(
            "Complex inline face system — no clear proportional scale or absolute-coord pattern. "
            "Manual analysis required before migration."
        )

    # Additional notes
    if result["eye_geometry"]:
        result["notes"].append(
            f"{len(result['eye_geometry'])} eye geometry definition(s) found — "
            "verify these are for Luma (not Miri/Cosmo)."
        )
    if result["inline_fns"]:
        fn_names = [ln.split("def ")[1].split("(")[0].strip()
                    for ln in result["inline_fns"] if "def " in ln]
        result["notes"].append(
            f"Inline face functions: {', '.join(fn_names)}"
        )

    return result


def audit_directory(directory: str, skip_legacy: bool = True) -> List[Dict[str, Any]]:
    """
    Audit all LTG_TOOL_*.py files in a directory.

    Parameters
    ----------
    directory   : str — path to tools directory
    skip_legacy : bool — if True, skip files in legacy/ subdirectory (default True)

    Returns
    -------
    list[dict] — one result per file audited
    """
    pattern = os.path.join(directory, "LTG_TOOL_*.py")
    files = sorted(glob_module.glob(pattern))

    if skip_legacy:
        legacy_dir = os.path.join(directory, "legacy")
        files = [f for f in files if not f.startswith(legacy_dir)]

    results = []
    for filepath in files:
        results.append(audit_file(filepath))
    return results


def format_report(results: List[Dict[str, Any]], include_no_luma: bool = False) -> str:
    """
    Format audit results as a human-readable Markdown report.

    Parameters
    ----------
    results        : list[dict] — from audit_directory() or audit_file()
    include_no_luma : bool — include NO_LUMA_FACE entries (default False — omits for brevity)

    Returns
    -------
    str — formatted report
    """
    using_api   = [r for r in results if r["status"] == "USING_API"]
    candidates  = [r for r in results if r["status"] == "INLINE_CANDIDATE"]
    no_luma     = [r for r in results if r["status"] == "NO_LUMA_FACE"]

    lines = [
        "# Face Curves Caller Audit Report",
        f"Tool: LTG_TOOL_face_curves_caller_audit.py v{__version__}",
        f"Files scanned: {len(results)}",
        "",
        f"## Summary",
        f"- USING_API (no action needed): {len(using_api)}",
        f"- INLINE_CANDIDATE (migration candidates): {len(candidates)}",
        f"- NO_LUMA_FACE (not applicable): {len(no_luma)}",
        "",
    ]

    if using_api:
        lines.append("## Currently Using draw_luma_face() API")
        for r in using_api:
            lines.append(f"### {r['file']}")
            for imp in r["api_imports"]:
                lines.append(f"  - {imp}")
        lines.append("")

    if candidates:
        lines.append("## Inline Candidates (Migration Targets)")
        lines.append("")

        ready_high   = [r for r in candidates if r["readiness"] == "READY_HIGH"]
        ready_medium = [r for r in candidates if r["readiness"] == "READY_MEDIUM"]
        ready_low    = [r for r in candidates if r["readiness"] == "READY_LOW"]

        for label, group in [
            ("READY_HIGH — Straightforward migration", ready_high),
            ("READY_MEDIUM — Moderate effort", ready_medium),
            ("READY_LOW — Complex; manual analysis needed", ready_low),
        ]:
            if not group:
                continue
            lines.append(f"### {label}")
            for r in group:
                lines.append(f"**{r['file']}**")
                if r["inline_fns"]:
                    fns = [ln.split("def ")[1].split("(")[0] for ln in r["inline_fns"] if "def " in ln]
                    lines.append(f"  - Inline functions: {', '.join(fns)}")
                if r["expression_refs"]:
                    lines.append(f"  - Expressions: {', '.join(r['expression_refs'])}")
                if r["eye_geometry"]:
                    lines.append(f"  - Eye geometry lines: {len(r['eye_geometry'])}")
                for note in r["notes"]:
                    lines.append(f"  - NOTE: {note}")
                lines.append("")

    if include_no_luma and no_luma:
        lines.append("## No Luma Face Drawing Found")
        for r in no_luma:
            lines.append(f"  - {r['file']}")
        lines.append("")

    lines.append("---")
    lines.append("Migration guide: see docs/face_curves_migration.md (proposed)")
    lines.append(f"Face curves API: LTG_TOOL_luma_face_curves.py v1.1.0 — draw_luma_face(draw, fc, expression)")

    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Audit LTG_TOOL generators for face_curves API usage / migration readiness."
    )
    parser.add_argument(
        "tools_dir",
        nargs="?",
        default=os.path.dirname(os.path.abspath(__file__)),
        help="Path to output/tools/ directory (default: same dir as this script)"
    )
    parser.add_argument(
        "--save-report",
        metavar="PATH",
        default=None,
        help="Write Markdown report to file (default: LTG_TOOL_face_curves_caller_audit_report.txt "
             "in tools_dir)"
    )
    parser.add_argument(
        "--include-no-luma",
        action="store_true",
        default=False,
        help="Include files with no Luma face drawing in the report"
    )
    parser.add_argument(
        "--include-legacy",
        action="store_true",
        default=False,
        help="Include legacy/ subdirectory files"
    )
    args = parser.parse_args()

    tools_dir = args.tools_dir
    if not os.path.isdir(tools_dir):
        print(f"ERROR: tools directory not found: {tools_dir}", file=sys.stderr)
        sys.exit(2)

    results = audit_directory(tools_dir, skip_legacy=not args.include_legacy)
    report  = format_report(results, include_no_luma=args.include_no_luma)

    print(report)

    # Determine save path
    save_path = args.save_report
    if save_path is None:
        save_path = os.path.join(
            tools_dir, "LTG_TOOL_face_curves_caller_audit_report.txt"
        )

    try:
        with open(save_path, "w", encoding="utf-8") as fh:
            fh.write(report)
        print(f"\nReport saved to: {save_path}", file=sys.stderr)
    except OSError as exc:
        print(f"WARNING: could not save report: {exc}", file=sys.stderr)

    # Exit code: 0 = all using API or none, 1 = candidates found
    n_candidates = sum(1 for r in results if r["status"] == "INLINE_CANDIDATE")
    sys.exit(1 if n_candidates > 0 else 0)


if __name__ == "__main__":
    main()
