#!/usr/bin/env python3
"""
LTG_TOOL_spec_sync_ci.py
Spec Sync CI Gate — "Luma & the Glitchkin"
Author: Kai Nakamura / Cycle 36

Runs character specification linters against all character generators and
exits non-zero if any P1 (proportion/construction) violations are found.

What counts as a P1 violation?
--------------------------------
For Luma / Cosmo / Grandma Miri  (char_spec_lint_v001):
  result == "FAIL" on any individual check  →  P1 violation.
  WARN is NOT a P1 violation (missing constant = uncertain, not wrong).

For Glitch  (glitch_spec_lint_v001):
  result == "FAIL" on any of G001/G002 (geometry checks)  →  P1 violation.
  G003–G008 WARNs are design-quality issues, not P1 construction violations.

For Byte  (char_spec_lint_v001 B001–B005 via lint_character("byte", ...)):
  B001 body oval W:H ratio (wider than tall).
  B002 body color #00D4E8 Byte Teal (GL-01b).
  B003 Hot Magenta crack indicator.
  B004 pixel confetti floating mechanism.
  B005 5×5 pixel eye grid.
  P1 = FAIL-grade checks only; WARNs are advisory.
  (v1.1.0 C39: delegates to char_spec_lint instead of inline scan.)

Characters covered (default: all)
----------------------------------
  luma, cosmo, miri, byte, glitch

Usage
-----
    python LTG_TOOL_spec_sync_ci.py
    python LTG_TOOL_spec_sync_ci.py --chars all
    python LTG_TOOL_spec_sync_ci.py --chars luma cosmo
    python LTG_TOOL_spec_sync_ci.py --chars glitch --tools-dir /path/to/tools
    python LTG_TOOL_spec_sync_ci.py --json          # machine-readable output

Exit codes
----------
  0  All P1 checks passed (WARNs are acceptable — advisory only)
  1  One or more P1 FAILs detected
  2  Usage error

API
---
    from LTG_TOOL_spec_sync_ci import run_ci, format_ci_report

    result = run_ci(chars=["luma", "glitch"], tools_dir="/path/to/tools")
    print(format_ci_report(result))
    # result["exit_code"] is 0 (pass) or 1 (fail)
"""

__version__ = "1.1.0"  # C39: Byte delegation to char_spec_lint (B001–B005) — Kai Nakamura

import os
import sys
import json
import glob as _glob
from typing import Dict, List, Optional, Tuple

# ── Paths ─────────────────────────────────────────────────────────────────────

_HERE = os.path.dirname(os.path.abspath(__file__))

ALL_CHARS = ["luma", "cosmo", "miri", "byte", "glitch"]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_source(path: str) -> Optional[str]:
    """Return file source as string, or None on error."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return None


def _latest_glob(tools_dir: str, *patterns: str) -> Optional[str]:
    """
    Return the alphabetically last file matching any of *patterns* in tools_dir.
    Returns None if no file matches.
    """
    candidates = []
    for pat in patterns:
        candidates.extend(_glob.glob(os.path.join(tools_dir, pat)))
    if not candidates:
        return None
    return sorted(candidates)[-1]


# ── Per-character CI runners ──────────────────────────────────────────────────

def _run_char_spec_lint(char_name: str, tools_dir: str) -> Dict:
    """
    Run char_spec_lint_v001 for luma/cosmo/miri.
    Returns a normalised result dict.
    """
    # Import dynamically so this tool is self-contained when the lib is available
    lint_module_path = os.path.join(tools_dir, "LTG_TOOL_char_spec_lint.py")
    if not os.path.isfile(lint_module_path):
        return {
            "char": char_name,
            "overall": "ERROR",
            "summary": {"PASS": 0, "WARN": 0, "FAIL": 0},
            "p1_fails": [],
            "all_checks": [],
            "file_linted": None,
            "error": f"Dependency not found: {lint_module_path}",
        }

    # Add tools_dir to path so the import works
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("_char_spec_lint", lint_module_path)
        mod  = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        result = mod.lint_character(char_name, tools_dir)
    except Exception as exc:
        return {
            "char": char_name,
            "overall": "ERROR",
            "summary": {"PASS": 0, "WARN": 0, "FAIL": 0},
            "p1_fails": [],
            "all_checks": [],
            "file_linted": None,
            "error": f"char_spec_lint error: {exc}",
        }

    # Extract P1 failures (FAIL-grade checks only)
    p1_fails = [
        cr for cr in result.get("checks", [])
        if cr["result"] == "FAIL"
    ]

    files = result.get("files", [])
    return {
        "char": char_name,
        "overall": result.get("overall", "ERROR"),
        "summary": result.get("summary", {}),
        "p1_fails": p1_fails,
        "all_checks": result.get("checks", []),
        "file_linted": files[0] if files else None,
        "error": result.get("error"),
    }


def _run_glitch_spec_lint(tools_dir: str) -> Dict:
    """
    Run glitch_spec_lint_v001.  P1 violations = G001 or G002 FAIL.
    """
    lint_module_path = os.path.join(tools_dir, "LTG_TOOL_glitch_spec_lint.py")
    if not os.path.isfile(lint_module_path):
        return {
            "char": "glitch",
            "overall": "ERROR",
            "summary": {"PASS": 0, "WARN": 0, "FAIL": 0},
            "p1_fails": [],
            "all_checks": [],
            "file_linted": None,
            "error": f"Dependency not found: {lint_module_path}",
        }

    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("_glitch_spec_lint", lint_module_path)
        mod  = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        # lint_directory returns a list of per-file result dicts
        raw_results = mod.lint_directory(tools_dir, skip_legacy=True)
    except Exception as exc:
        return {
            "char": "glitch",
            "overall": "ERROR",
            "summary": {"PASS": 0, "WARN": 0, "FAIL": 0},
            "p1_fails": [],
            "all_checks": [],
            "file_linted": None,
            "error": f"glitch_spec_lint error: {exc}",
        }

    # Filter to P1 checks only: G001 (geometry width/height), G002 (mass ratio)
    # Note: glitch_spec_lint issues is a list[str] (not dicts); status key = "status"
    P1_PREFIXES = ("G001:", "G002:")
    p1_fails = []
    all_checks = []
    files_linted = []

    for file_result in raw_results:
        # glitch_spec_lint uses "status" (not "result") and skips SKIP entries itself
        status = file_result.get("status", "WARN")
        fpath  = file_result.get("file", "?")
        files_linted.append(fpath)

        for issue_str in file_result.get("issues", []):
            # Determine check code from issue string prefix (e.g. "G001: ...")
            code = issue_str.split(":")[0].strip() if ":" in issue_str else "G???"
            issue_dict = {
                "code": code,
                "result": "FAIL",   # glitch_spec_lint only emits issues on violations
                "message": issue_str,
            }
            all_checks.append({
                "check": code,
                "result": "FAIL",
                "issues": [issue_dict],
                "file": fpath,
            })
            if any(issue_str.startswith(p) for p in P1_PREFIXES):
                p1_fails.append({
                    "check": code,
                    "result": "FAIL",
                    "issues": [issue_dict],
                    "file": fpath,
                })

    has_fail = len(p1_fails) > 0
    summary_counts = {"PASS": 0, "WARN": 0, "FAIL": 0}
    for fr in raw_results:
        s = fr.get("status", "WARN")
        summary_counts[s] = summary_counts.get(s, 0) + 1

    glitch_overall = "FAIL" if has_fail else ("WARN" if summary_counts.get("WARN", 0) else "PASS")
    return {
        "char": "glitch",
        "overall": glitch_overall,
        "summary": summary_counts,
        "p1_fails": p1_fails,
        "all_checks": all_checks,
        "file_linted": ", ".join(os.path.basename(f) for f in files_linted[:3]) if files_linted else None,
        "error": None,
    }


def _run_byte_lint(tools_dir: str) -> Dict:
    """
    Run Byte spec checks via char_spec_lint_v001 lint_character("byte", ...).

    Provides B001–B005 checks (5 checks) instead of the prior 2-check inline scan.
    Delegates entirely to char_spec_lint so Byte gets the same treatment as
    Luma/Cosmo/Miri.

    Changed in v1.1.0 (C39 — Kai Nakamura): replaces inline B001/B002 scan
    with full char_spec_lint delegation (B001–B005).
    """
    return _run_char_spec_lint("byte", tools_dir)


# ── Public API ────────────────────────────────────────────────────────────────

def run_ci(
    chars: Optional[List[str]] = None,
    tools_dir: Optional[str] = None,
) -> Dict:
    """
    Run the Spec Sync CI gate.

    Parameters
    ----------
    chars : list[str] | None
        Characters to lint. Defaults to ALL_CHARS = ["luma", "cosmo", "miri", "byte", "glitch"].
        Pass "all" or None to run all.
    tools_dir : str | None
        Path to output/tools/. Defaults to the directory containing this script.

    Returns
    -------
    dict:
        "chars_requested"  : list[str]
        "results"          : list[dict]  — per-character result dicts
        "total_p1_fails"   : int
        "total_warns"      : int
        "total_passes"     : int
        "exit_code"        : int  — 0 = all P1 pass, 1 = P1 fail(s) detected
        "summary_line"     : str  — one-line human-readable summary
    """
    if tools_dir is None:
        tools_dir = _HERE

    if chars is None or chars == ["all"] or chars == "all":
        chars = list(ALL_CHARS)

    # Validate
    unknown = [c for c in chars if c not in ALL_CHARS]
    if unknown:
        raise ValueError(
            f"Unknown character(s): {unknown}. Valid choices: {ALL_CHARS}"
        )

    results = []
    for char in chars:
        if char in ("luma", "cosmo", "miri"):
            r = _run_char_spec_lint(char, tools_dir)
        elif char == "glitch":
            r = _run_glitch_spec_lint(tools_dir)
        elif char == "byte":
            r = _run_byte_lint(tools_dir)
        else:
            r = {
                "char": char, "overall": "ERROR",
                "summary": {}, "p1_fails": [], "all_checks": [],
                "file_linted": None, "error": f"No linter registered for '{char}'",
            }
        results.append(r)

    total_p1 = sum(len(r["p1_fails"]) for r in results)
    total_warn = sum(r["summary"].get("WARN", 0) for r in results)
    total_pass = sum(r["summary"].get("PASS", 0) for r in results)
    exit_code = 1 if total_p1 > 0 else 0

    # Build per-character pass/fail summary
    per_char = []
    for r in results:
        nfail = len(r["p1_fails"])
        label = r["char"].upper()
        per_char.append(f"{label}:{'FAIL' if nfail else r['overall']}")

    summary_line = (
        f"P1 violations: {total_p1}  |  "
        f"Per-char: {', '.join(per_char)}  |  "
        f"{'CI FAIL' if exit_code else 'CI PASS'}"
    )

    return {
        "chars_requested": list(chars),
        "results": results,
        "total_p1_fails": total_p1,
        "total_warns": total_warn,
        "total_passes": total_pass,
        "exit_code": exit_code,
        "summary_line": summary_line,
    }


def format_ci_report(ci_result: Dict) -> str:
    """
    Format a run_ci() result dict as a human-readable report string.

    Parameters
    ----------
    ci_result : dict — output of run_ci()

    Returns
    -------
    str
    """
    lines = []
    lines.append("=" * 72)
    lines.append(f"LTG Spec Sync CI Gate — v{__version__}")
    lines.append(f"Characters: {', '.join(ci_result['chars_requested'])}")
    lines.append("=" * 72)

    for r in ci_result["results"]:
        char_label = r["char"].upper()
        overall = r.get("overall", "ERROR")
        file_str = r.get("file_linted") or "(no file found)"
        if file_str and len(file_str) > 60:
            file_str = "..." + file_str[-57:]

        lines.append("")
        lines.append(f"  {'─'*68}")
        lines.append(f"  {overall:6}  {char_label}  [{os.path.basename(file_str) if file_str else '—'}]")
        lines.append(f"  {'─'*68}")

        if r.get("error"):
            lines.append(f"  ERROR: {r['error']}")
            continue

        s = r.get("summary", {})
        lines.append(
            f"  Checks: {s.get('PASS',0)} PASS / {s.get('WARN',0)} WARN / {s.get('FAIL',0)} FAIL"
        )

        p1_fails = r.get("p1_fails", [])
        if p1_fails:
            lines.append(f"\n  P1 VIOLATIONS ({len(p1_fails)}):")
            for fail in p1_fails:
                check_code = fail.get("check", "?")
                for issue in fail.get("issues", []):
                    msg = issue.get("message", str(issue))
                    lines.append(f"    FAIL [{check_code}] {msg}")
        else:
            lines.append("  No P1 violations.")

        # Also surface WARNs for advisory
        all_checks = r.get("all_checks", [])
        warns = [c for c in all_checks if c.get("result") == "WARN"]
        if warns:
            lines.append(f"\n  Advisory WARNs ({len(warns)}) — not a CI failure:")
            for w in warns[:5]:
                code = w.get("check", "?")
                for issue in w.get("issues", [])[:1]:
                    msg = issue.get("message", str(issue))
                    # Truncate long messages
                    if len(msg) > 100:
                        msg = msg[:97] + "..."
                    lines.append(f"    WARN [{code}] {msg}")
            if len(warns) > 5:
                lines.append(f"    ... and {len(warns)-5} more advisory warns.")

    lines.append("")
    lines.append("=" * 72)
    lines.append(ci_result.get("summary_line", ""))
    exit_code = ci_result.get("exit_code", 1)
    lines.append(
        f"CI RESULT: {'FAIL — P1 violations must be fixed before merge.' if exit_code else 'PASS'}"
    )
    lines.append("=" * 72)
    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            f"LTG Spec Sync CI Gate v{__version__} — "
            "fails if any P1 character-spec violations are found."
        )
    )
    parser.add_argument(
        "--chars",
        nargs="+",
        default=["all"],
        metavar="CHAR",
        help=(
            f"Characters to lint (default: all). "
            f"Choices: {', '.join(ALL_CHARS + ['all'])}"
        ),
    )
    parser.add_argument(
        "--tools-dir",
        default=None,
        help="Path to output/tools/ directory (default: this script's directory)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output machine-readable JSON instead of human report",
    )
    parser.add_argument(
        "--save-report",
        default=None,
        metavar="PATH",
        help="Save human-readable report to PATH",
    )
    args = parser.parse_args()

    # Normalise --chars all → ALL_CHARS
    requested_chars = args.chars
    if requested_chars == ["all"]:
        requested_chars = list(ALL_CHARS)
    else:
        # Validate each entry
        invalid = [c for c in requested_chars if c not in ALL_CHARS and c != "all"]
        if invalid:
            parser.error(
                f"Unknown character(s): {invalid}. "
                f"Valid: {', '.join(ALL_CHARS + ['all'])}"
            )
        requested_chars = [c for c in requested_chars if c != "all"]

    tools_dir = args.tools_dir or _HERE

    try:
        ci_result = run_ci(chars=requested_chars, tools_dir=tools_dir)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)

    if args.json:
        # Serialise: replace any non-JSON-safe values
        import copy
        safe = copy.deepcopy(ci_result)
        print(json.dumps(safe, indent=2, default=str))
    else:
        report = format_ci_report(ci_result)
        print(report)

        if args.save_report:
            save_path = args.save_report
        else:
            save_path = os.path.join(tools_dir, "LTG_TOOL_spec_sync_ci_report.txt")

        try:
            with open(save_path, "w", encoding="utf-8") as fh:
                fh.write(report)
                fh.write("\n")
            print(f"\nReport saved to: {save_path}")
        except OSError as exc:
            print(f"\nCould not save report: {exc}", file=sys.stderr)

    sys.exit(ci_result["exit_code"])
