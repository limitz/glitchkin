# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
#!/usr/bin/env python3
"""
LTG_TOOL_ci_suite.py
CI Suite — "Luma & the Glitchkin"
Author: Kai Nakamura / Cycle 37
v1.1.0: Morgan Walsh / Cycle 40 — --known-issues flag

Runs all LTG tool-pipeline CI checks in sequence and produces a combined report.

Checks run (in order)
---------------------
1. stub_linter             — broken import detection (old-style LTG_CHAR_/COLOR_ refs)
2. draw_order_lint         — draw order violations (W001–W004, back-pose suppression)
3. glitch_spec_lint        — Glitchkin generator spec compliance (G001–G008)
4. spec_sync_ci            — P1 character spec CI gate (Luma/Cosmo/Miri/Byte/Glitch)
5. char_spec_lint          — Detailed character spec (L001–L005, S001–S005, M001–M005)

Pass/fail threshold
-------------------
--fail-on WARN  → exit 1 if any check produces WARN or FAIL result
--fail-on FAIL  → exit 1 only if a check produces a hard FAIL (P1 violation)
                  (default; WARNs are advisory)

Known-issues list
-----------------
--known-issues PATH  → load a JSON file of expected/pre-existing WARNs.
  Matching issues are annotated as KNOWN in the report so true regressions
  stand out. KNOWN issues do not suppress the overall WARN/FAIL grade —
  they are informational only (mirrors glitch_spec_lint suppressions.json).

  JSON format (see ci_known_issues.json):
    {
      "known_issues": [
        {"check": "draw_order_lint", "file": "foo.py", "code": "W004", "reason": "..."},
        ...
      ]
    }
  Fields:
    check — one of: stub_linter, draw_order_lint, glitch_spec_lint,
                    spec_sync_ci, char_spec_lint
    file  — basename of the file producing the issue (e.g. "LTG_TOOL_foo.py")
    code  — warning/error code (e.g. "W004", "G007"); null = match any code for this file
    reason — human-readable explanation (shown in report)

Exit codes
----------
  0  All checks passed at the configured threshold
  1  One or more checks failed at the configured threshold
  2  Usage / import error

Usage
-----
    python LTG_TOOL_ci_suite.py
    python LTG_TOOL_ci_suite.py --fail-on WARN
    python LTG_TOOL_ci_suite.py --fail-on FAIL
    python LTG_TOOL_ci_suite.py --tools-dir /path/to/output/tools
    python LTG_TOOL_ci_suite.py --save-report PATH
    python LTG_TOOL_ci_suite.py --known-issues ci_known_issues.json

API
---
    from LTG_TOOL_ci_suite import run_suite, format_suite_report, load_known_issues

    known = load_known_issues("ci_known_issues.json")
    result = run_suite(tools_dir="/path/to/output/tools", fail_on="FAIL",
                       known_issues=known)
    print(format_suite_report(result))
    # result["exit_code"] is 0 (pass) or 1 (fail)
    # result["checks"] is dict keyed by check name
    # Each check result["known_count"] shows how many issues were flagged KNOWN

Changelog
---------
v1.0.0 (C37): Initial implementation. (Kai Nakamura)
v1.1.0 (C40): --known-issues PATH flag. Loads expected WARNs from JSON;
              marks matching issues as KNOWN in report output.
              known_count added to each check result.
              format_suite_report() shows KNOWN annotation in summary.
              load_known_issues() exported for programmatic use.
              (Morgan Walsh)
"""

__version__ = "1.1.0"

import os
import sys
import json
import argparse
from typing import Dict, List, Optional

# ── Resolve tools dir ─────────────────────────────────────────────────────────

_HERE = os.path.dirname(os.path.abspath(__file__))


def _tools_dir_or_default(tools_dir):
    return tools_dir if tools_dir else _HERE


def _add_to_path(tools_dir):
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)


# ── Known-issues support ──────────────────────────────────────────────────────

def load_known_issues(path):
    """
    Load a known-issues JSON file. Returns a dict keyed by check name,
    each value a list of {file, code, reason} dicts.

    Parameters
    ----------
    path : str | None
        Path to the known-issues JSON file, or None to return empty dict.

    Returns
    -------
    dict  { check_name: [ {file, code, reason}, ... ] }
    """
    if not path:
        return {}
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        result = {}
        for entry in data.get("known_issues", []):
            check = entry.get("check", "")
            if not check:
                continue
            if check not in result:
                result[check] = []
            result[check].append({
                "file":   entry.get("file", ""),
                "code":   entry.get("code"),    # may be None = match any code
                "reason": entry.get("reason", ""),
            })
        return result
    except Exception as exc:
        # Silently return empty on load failure — do not break CI run
        return {"_load_error": str(exc)}


def _is_known(check_name, filename, code_str, known_issues):
    """
    Return (is_known, reason) for a specific (check, file, code) triple.

    Matching rules:
    - known entry.file must equal os.path.basename(filename)
    - known entry.code must equal code_str OR be None (wildcard)
    """
    if not known_issues:
        return False, ""
    basename = os.path.basename(filename)
    for entry in known_issues.get(check_name, []):
        if entry["file"] == basename:
            if entry["code"] is None or entry["code"] == code_str:
                return True, entry.get("reason", "")
    return False, ""


def _annotate_details_with_known(details_str, check_name, known_issues):
    """
    Walk through a detail report string line by line and append
    '[KNOWN]' after lines that match a known-issue entry.
    Returns annotated string and count of known annotations.
    """
    if not known_issues or check_name not in known_issues:
        return details_str, 0
    lines = details_str.splitlines()
    out = []
    known_count = 0
    for line in lines:
        # Try to extract file basename and code from typical linter report lines.
        # Draw order: "WARN   LTG_TOOL_foo.py  (N warning(s))"
        # Glitch spec: "[WARN] LTG_TOOL_foo.py"
        # Individual issue: "  [W004] line N: ..."  or "  - Gxxx: ..."
        marked = False
        # Check for file-level WARN header lines
        import re as _re
        m = _re.search(r'(?:WARN\s+|WARN\]?\s+)(LTG_\S+\.py)', line)
        if m:
            fname = m.group(1).strip()
            known, reason = _is_known(check_name, fname, None, known_issues)
            if known:
                out.append(line + f"  [KNOWN: {reason[:60]}]" if reason else line + "  [KNOWN]")
                known_count += 1
                marked = True
        # Check for individual issue lines with code (W004, G007, etc.)
        if not marked:
            m2 = _re.search(r'\[(W\d{3}|G\d{3})\]', line)
            if m2:
                code = m2.group(1)
                # Look for nearby file context — scan preceding lines for a filename
                # (simplified: check if any known issue for this check matches this code
                # with wildcard file — useful for broad suppressions)
                for entry in known_issues.get(check_name, []):
                    if (entry["code"] == code or entry["code"] is None):
                        out.append(line + "  [KNOWN]")
                        known_count += 1
                        marked = True
                        break
        if not marked:
            out.append(line)
    return "\n".join(out), known_count


# ── Check 1: stub_linter ─────────────────────────────────────────────────

def _run_stub_linter(tools_dir):
    """Run stub integrity linter. Returns (status, summary, details)."""
    try:
        import LTG_TOOL_stub_linter as stub
        results = stub.lint_directory(tools_dir)
        error_count  = sum(1 for r in results if r.get("result") == "ERROR")
        warn_count   = sum(1 for r in results if r.get("result") == "WARN")
        pass_count   = sum(1 for r in results if r.get("result") == "PASS")
        # stub linter: ERROR = broken import found = hard fail; WARN = ambiguous
        if error_count:
            status = "FAIL"
        elif warn_count:
            status = "WARN"
        else:
            status = "PASS"
        summary = f"{len(results)} file(s) — {pass_count} PASS / {warn_count} WARN / {error_count} ERROR"
        details = stub.format_report(results)
        return status, summary, details
    except ImportError as exc:
        return "ERROR", f"Could not import stub linter: {exc}", ""


# ── Check 2: draw_order_lint ─────────────────────────────────────────────

def _run_draw_order_lint(tools_dir):
    """Run scope-aware draw-order linter. Returns (status, summary, details)."""
    try:
        import LTG_TOOL_draw_order_lint as dol
        results = dol.lint_directory(tools_dir)
        warn_count = sum(1 for r in results if r.get("result") == "WARN")
        pass_count = sum(1 for r in results if r.get("result") == "PASS")
        err_count  = sum(1 for r in results if r.get("result") == "ERROR")
        # draw_order: WARN = advisory, ERROR = file read error
        if err_count:
            status = "FAIL"
        elif warn_count:
            status = "WARN"
        else:
            status = "PASS"
        summary = f"{len(results)} file(s) — {pass_count} PASS / {warn_count} WARN / {err_count} ERROR"
        details = dol.format_report(results, include_pass=False)
        return status, summary, details
    except ImportError as exc:
        return "ERROR", f"Could not import draw_order_lint: {exc}", ""


# ── Check 3: glitch_spec_lint ───────────────────────────────────────────

def _run_glitch_spec_lint(tools_dir):
    """Run Glitch spec linter with suppression list. Returns (status, summary, details)."""
    try:
        import LTG_TOOL_glitch_spec_lint as gsl
        results = gsl.lint_directory(tools_dir)
        warn_count = sum(1 for r in results if r.get("status") == "WARN")
        pass_count = sum(1 for r in results if r.get("status") == "PASS")
        # glitch spec: WARN = violation; no hard FAIL grade (all violations are WARNs)
        status = "WARN" if warn_count else "PASS"
        total_suppressed = sum(r.get("suppressed_count", 0) for r in results)
        sup_note = f" ({total_suppressed} suppressed)" if total_suppressed else ""
        summary = (
            f"{len(results)} Glitch generator(s) — {pass_count} PASS / {warn_count} WARN{sup_note}"
        )
        details = gsl.format_report(results)
        return status, summary, details
    except ImportError as exc:
        return "ERROR", f"Could not import glitch_spec_lint: {exc}", ""


# ── Check 4: spec_sync_ci ───────────────────────────────────────────────

def _run_spec_sync_ci(tools_dir):
    """Run spec sync CI gate. Returns (status, summary, details)."""
    try:
        import LTG_TOOL_spec_sync_ci as ssc
        ci_result = ssc.run_ci(chars=ssc.ALL_CHARS, tools_dir=tools_dir)
        exit_code = ci_result.get("exit_code", 0)
        # exit_code 1 = P1 FAIL; exit_code 0 = pass
        if exit_code == 1:
            status = "FAIL"
        else:
            status = "PASS"
        # Count per-char results
        chars = ci_result.get("chars", {})
        fail_chars = [ch for ch, r in chars.items() if r.get("p1_fail", False)]
        warn_chars = [ch for ch, r in chars.items() if r.get("warn_count", 0) > 0 and not r.get("p1_fail", False)]
        summary = (
            f"5 character(s) — "
            f"{len(fail_chars)} P1 FAIL: {fail_chars if fail_chars else 'none'} / "
            f"{len(warn_chars)} WARN: {warn_chars if warn_chars else 'none'}"
        )
        details = ssc.format_ci_report(ci_result)
        return status, summary, details
    except ImportError as exc:
        return "ERROR", f"Could not import spec_sync_ci: {exc}", ""


# ── Check 5: char_spec_lint ─────────────────────────────────────────────

def _run_char_spec_lint(tools_dir):
    """Run detailed character spec linter. Returns (status, summary, details)."""
    try:
        import LTG_TOOL_char_spec_lint as csl
        results = csl.lint_all(tools_dir)
        fail_count = sum(1 for r in results if r.get("result") == "FAIL")
        warn_count = sum(1 for r in results if r.get("result") == "WARN")
        pass_count = sum(1 for r in results if r.get("result") == "PASS")
        # char spec: FAIL = canonical value actively violates spec
        if fail_count:
            status = "FAIL"
        elif warn_count:
            status = "WARN"
        else:
            status = "PASS"
        summary = f"3 character(s) — {pass_count} PASS / {warn_count} WARN / {fail_count} FAIL"
        details = csl.format_report(results)
        return status, summary, details
    except ImportError as exc:
        return "ERROR", f"Could not import char_spec_lint: {exc}", ""


# ── Suite runner ──────────────────────────────────────────────────────────────

_CHECKS = [
    ("stub_linter",       _run_stub_linter,    "Stub Integrity Linter"),
    ("draw_order_lint",   _run_draw_order_lint, "Draw Order Linter"),
    ("glitch_spec_lint",  _run_glitch_spec_lint, "Glitch Spec Linter"),
    ("spec_sync_ci",      _run_spec_sync_ci,   "Spec Sync CI Gate"),
    ("char_spec_lint",    _run_char_spec_lint,  "Char Spec Linter"),
]


def run_suite(tools_dir=None, fail_on="FAIL", known_issues=None):
    """
    Run all CI checks and return a combined result dict.

    Parameters
    ----------
    tools_dir : str | None
        Path to output/tools/. Defaults to the directory of this script.
    fail_on : "WARN" | "FAIL"
        Threshold for exit code 1:
          "FAIL" — only hard FAIL results trigger exit code 1 (default)
          "WARN" — any WARN or FAIL triggers exit code 1
    known_issues : dict | None
        Loaded known-issues dict from load_known_issues(). When provided,
        matching issues are annotated as KNOWN in the detail report.
        KNOWN annotations are informational — they do not suppress the
        overall WARN/FAIL grade.

    Returns
    -------
    dict
        {
          "tools_dir":      str,
          "fail_on":        str,
          "checks":         { check_name: {"label": str, "status": str,
                                           "summary": str, "details": str,
                                           "known_count": int} },
          "overall_status": "PASS" | "WARN" | "FAIL" | "ERROR",
          "exit_code":      int,   # 0 = pass, 1 = fail at threshold, 2 = import error
          "known_issues_path": str | None,
          "total_known":    int,
        }
    """
    tools_dir = _tools_dir_or_default(tools_dir)
    _add_to_path(tools_dir)

    fail_on = fail_on.upper()
    if fail_on not in ("WARN", "FAIL"):
        fail_on = "FAIL"

    if known_issues is None:
        known_issues = {}

    results = {}
    any_error  = False
    any_fail   = False
    any_warn   = False
    total_known = 0

    for (key, runner, label) in _CHECKS:
        status, summary, details = runner(tools_dir)
        # Annotate details with KNOWN markers where applicable
        annotated_details, known_count = _annotate_details_with_known(
            details, key, known_issues
        )
        # Annotate summary with known count if any
        summary_annotated = summary
        if known_count > 0:
            summary_annotated = f"{summary}  [{known_count} KNOWN]"
        total_known += known_count
        results[key] = {
            "label":       label,
            "status":      status,
            "summary":     summary_annotated,
            "details":     annotated_details,
            "known_count": known_count,
        }
        if status == "ERROR":
            any_error = True
        elif status == "FAIL":
            any_fail = True
        elif status == "WARN":
            any_warn = True

    # Determine overall status
    if any_error:
        overall_status = "ERROR"
        exit_code = 2
    elif any_fail:
        overall_status = "FAIL"
        exit_code = 1
    elif any_warn and fail_on == "WARN":
        overall_status = "WARN"
        exit_code = 1
    elif any_warn:
        overall_status = "WARN"
        exit_code = 0
    else:
        overall_status = "PASS"
        exit_code = 0

    return {
        "tools_dir":        tools_dir,
        "fail_on":          fail_on,
        "checks":           results,
        "overall_status":   overall_status,
        "exit_code":        exit_code,
        "total_known":      total_known,
    }


# ── Reporting ─────────────────────────────────────────────────────────────────

def format_suite_report(suite_result, include_details=True):
    """
    Format the suite result dict as a human-readable string.

    Parameters
    ----------
    suite_result   : dict from run_suite()
    include_details: bool — if True, append each check's full detail report

    Returns
    -------
    str
    """
    lines = []
    lines.append("=" * 72)
    lines.append(f"LTG CI Suite v{__version__} — Combined Report")
    lines.append(f"Tools dir : {suite_result['tools_dir']}")
    lines.append(f"Fail-on   : {suite_result['fail_on']}")
    lines.append("=" * 72)

    STATUS_ICONS = {"PASS": "✓", "WARN": "⚠", "FAIL": "✗", "ERROR": "!"}

    for key, info in suite_result["checks"].items():
        icon = STATUS_ICONS.get(info["status"], "?")
        lines.append(f"  {icon} [{info['status']:5}] {info['label']}")
        lines.append(f"          {info['summary']}")

    lines.append("")
    overall = suite_result["overall_status"]
    icon = STATUS_ICONS.get(overall, "?")
    known_total = suite_result.get("total_known", 0)
    known_note = f"  ({known_total} KNOWN issues annotated)" if known_total else ""
    lines.append(f"  {icon} OVERALL: {overall}  (exit code {suite_result['exit_code']}){known_note}")
    if known_total:
        lines.append(
            "    NOTE: KNOWN issues are pre-existing/expected — annotated for visibility only."
        )
        lines.append(
            "    They do not suppress the overall grade. Remove entries from ci_known_issues.json"
        )
        lines.append("    once the underlying issue is fixed.")
    lines.append("=" * 72)

    if include_details:
        for key, info in suite_result["checks"].items():
            if info["details"]:
                lines.append(f"\n{'─' * 72}")
                lines.append(f"Detail: {info['label']}")
                lines.append("─" * 72)
                lines.append(info["details"])

    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=f"LTG CI Suite v{__version__} — runs all pipeline CI checks in sequence"
    )
    parser.add_argument(
        "--fail-on",
        choices=["WARN", "FAIL"],
        default="FAIL",
        help="Exit code 1 threshold: FAIL (default) or WARN",
    )
    parser.add_argument(
        "--tools-dir",
        default=None,
        metavar="PATH",
        help="Path to output/tools/ (default: directory of this script)",
    )
    parser.add_argument(
        "--save-report",
        default=None,
        metavar="PATH",
        help="Save full report to this file",
    )
    parser.add_argument(
        "--no-details",
        action="store_true",
        help="Suppress per-check detail sections from output",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output machine-readable JSON (summaries only, no detail blocks)",
    )
    parser.add_argument(
        "--known-issues",
        default=None,
        metavar="PATH",
        help=(
            "JSON file of expected/pre-existing WARNs. Matching issues are annotated "
            "as KNOWN in the report. Does not suppress WARN/FAIL grade. "
            "Default: ci_known_issues.json in tools-dir (if present)."
        ),
    )
    args = parser.parse_args()

    # Resolve known-issues path: explicit flag > auto-discover in tools-dir
    known_issues_path = args.known_issues
    if not known_issues_path:
        tools_dir_resolved = args.tools_dir if args.tools_dir else _HERE
        auto_path = os.path.join(tools_dir_resolved, "ci_known_issues.json")
        if os.path.exists(auto_path):
            known_issues_path = auto_path

    known_issues = load_known_issues(known_issues_path)
    if "_load_error" in known_issues:
        print(f"Warning: could not load known-issues file: {known_issues['_load_error']}", file=sys.stderr)
        known_issues = {}

    suite_result = run_suite(
        tools_dir=args.tools_dir, fail_on=args.fail_on, known_issues=known_issues
    )

    if args.json_output:
        # Remove detail blocks for JSON (they can be large)
        json_result = dict(suite_result)
        json_result["checks"] = {
            k: {kk: vv for kk, vv in v.items() if kk != "details"}
            for k, v in suite_result["checks"].items()
        }
        print(json.dumps(json_result, indent=2))
    else:
        report = format_suite_report(suite_result, include_details=not args.no_details)
        if args.save_report:
            with open(args.save_report, "w", encoding="utf-8") as fh:
                fh.write(report)
            print(f"Report saved to: {args.save_report}")
        else:
            print(report)

    sys.exit(suite_result["exit_code"])


if __name__ == "__main__":
    main()
