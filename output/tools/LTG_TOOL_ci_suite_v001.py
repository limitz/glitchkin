#!/usr/bin/env python3
"""
LTG_TOOL_ci_suite_v001.py
CI Suite — "Luma & the Glitchkin"
Author: Kai Nakamura / Cycle 37

Runs all LTG tool-pipeline CI checks in sequence and produces a combined report.

Checks run (in order)
---------------------
1. stub_linter_v001         — broken import detection (old-style LTG_CHAR_/COLOR_ refs)
2. draw_order_lint_v002     — draw order violations (W001–W004, back-pose suppression)
3. glitch_spec_lint_v001    — Glitchkin generator spec compliance (G001–G008)
4. spec_sync_ci_v001        — P1 character spec CI gate (Luma/Cosmo/Miri/Byte/Glitch)
5. char_spec_lint_v001      — Detailed character spec (L001–L005, S001–S005, M001–M005)

Pass/fail threshold
-------------------
--fail-on WARN  → exit 1 if any check produces WARN or FAIL result
--fail-on FAIL  → exit 1 only if a check produces a hard FAIL (P1 violation)
                  (default; WARNs are advisory)

Exit codes
----------
  0  All checks passed at the configured threshold
  1  One or more checks failed at the configured threshold
  2  Usage / import error

Usage
-----
    python LTG_TOOL_ci_suite_v001.py
    python LTG_TOOL_ci_suite_v001.py --fail-on WARN
    python LTG_TOOL_ci_suite_v001.py --fail-on FAIL
    python LTG_TOOL_ci_suite_v001.py --tools-dir /path/to/output/tools
    python LTG_TOOL_ci_suite_v001.py --save-report PATH

API
---
    from LTG_TOOL_ci_suite_v001 import run_suite, format_suite_report

    result = run_suite(tools_dir="/path/to/output/tools", fail_on="FAIL")
    print(format_suite_report(result))
    # result["exit_code"] is 0 (pass) or 1 (fail)
    # result["checks"] is dict keyed by check name

Changelog
---------
v1.0.0 (C37): Initial implementation.
"""

__version__ = "1.0.0"

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


# ── Check 1: stub_linter_v001 ─────────────────────────────────────────────────

def _run_stub_linter(tools_dir):
    """Run stub integrity linter. Returns (status, summary, details)."""
    try:
        import LTG_TOOL_stub_linter_v001 as stub
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


# ── Check 2: draw_order_lint_v002 ─────────────────────────────────────────────

def _run_draw_order_lint(tools_dir):
    """Run scope-aware draw-order linter. Returns (status, summary, details)."""
    try:
        import LTG_TOOL_draw_order_lint_v002 as dol
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
        return "ERROR", f"Could not import draw_order_lint_v002: {exc}", ""


# ── Check 3: glitch_spec_lint_v001 ───────────────────────────────────────────

def _run_glitch_spec_lint(tools_dir):
    """Run Glitch spec linter with suppression list. Returns (status, summary, details)."""
    try:
        import LTG_TOOL_glitch_spec_lint_v001 as gsl
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
        return "ERROR", f"Could not import glitch_spec_lint_v001: {exc}", ""


# ── Check 4: spec_sync_ci_v001 ───────────────────────────────────────────────

def _run_spec_sync_ci(tools_dir):
    """Run spec sync CI gate. Returns (status, summary, details)."""
    try:
        import LTG_TOOL_spec_sync_ci_v001 as ssc
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
        return "ERROR", f"Could not import spec_sync_ci_v001: {exc}", ""


# ── Check 5: char_spec_lint_v001 ─────────────────────────────────────────────

def _run_char_spec_lint(tools_dir):
    """Run detailed character spec linter. Returns (status, summary, details)."""
    try:
        import LTG_TOOL_char_spec_lint_v001 as csl
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
        return "ERROR", f"Could not import char_spec_lint_v001: {exc}", ""


# ── Suite runner ──────────────────────────────────────────────────────────────

_CHECKS = [
    ("stub_linter",       _run_stub_linter,    "Stub Integrity Linter"),
    ("draw_order_lint",   _run_draw_order_lint, "Draw Order Linter v002"),
    ("glitch_spec_lint",  _run_glitch_spec_lint, "Glitch Spec Linter v001"),
    ("spec_sync_ci",      _run_spec_sync_ci,   "Spec Sync CI Gate v001"),
    ("char_spec_lint",    _run_char_spec_lint,  "Char Spec Linter v001"),
]


def run_suite(tools_dir=None, fail_on="FAIL"):
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

    Returns
    -------
    dict
        {
          "tools_dir":  str,
          "fail_on":    str,
          "checks":     { check_name: {"label": str, "status": str,
                                        "summary": str, "details": str} },
          "overall_status": "PASS" | "WARN" | "FAIL" | "ERROR",
          "exit_code":  int,   # 0 = pass, 1 = fail at threshold, 2 = import error
        }
    """
    tools_dir = _tools_dir_or_default(tools_dir)
    _add_to_path(tools_dir)

    fail_on = fail_on.upper()
    if fail_on not in ("WARN", "FAIL"):
        fail_on = "FAIL"

    results = {}
    any_error  = False
    any_fail   = False
    any_warn   = False

    for (key, runner, label) in _CHECKS:
        status, summary, details = runner(tools_dir)
        results[key] = {
            "label":   label,
            "status":  status,
            "summary": summary,
            "details": details,
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
        "tools_dir":      tools_dir,
        "fail_on":        fail_on,
        "checks":         results,
        "overall_status": overall_status,
        "exit_code":      exit_code,
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
    lines.append(f"  {icon} OVERALL: {overall}  (exit code {suite_result['exit_code']})")
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
    args = parser.parse_args()

    suite_result = run_suite(tools_dir=args.tools_dir, fail_on=args.fail_on)

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
