#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_ci_suite.py
CI Suite — "Luma & the Glitchkin"
Author: Kai Nakamura / Cycle 37
v1.1.0: Morgan Walsh / Cycle 40 — --known-issues flag
v1.2.0: Morgan Walsh / Cycle 42 — --warn-stale N flag
v1.6.0: Morgan Walsh / Cycle 46 — --auto-seed flag
v1.7.0: Morgan Walsh / Cycle 47 — --dry-run flag, Check 10 ext_model_check
v1.8.0: Morgan Walsh / Cycle 48 — Remove Check 10, add Check 10 doc_staleness
v1.9.0: Morgan Walsh / Cycle 49 — Check registry + per-directory doc_staleness thresholds
v2.0.0: Morgan Walsh / Cycle 52 — Checks 11-13: dep_availability, bezier_migration_lint, tool_naming_lint
v2.1.0: Morgan Walsh / Cycle 53 — Check 14: char_modular_lint (inline char drawing detection)

Runs all LTG tool-pipeline CI checks in sequence and produces a combined report.

Check Registry (ci_check_registry.json)
---------------------------------------
Checks are now config-driven. The file ci_check_registry.json in the tools
directory defines which check function occupies each slot (1-10). To swap a
check, edit the JSON — no code changes needed. Swap history is tracked in
the same file under "swap_history".

If ci_check_registry.json is absent, the suite falls back to the hardcoded
_CHECKS list (backwards compatible).

Registry JSON format:
    {
      "slots": [
        {"slot": 1, "check": "stub_linter", "label": "...", "enabled": true},
        ...
      ],
      "swap_history": [
        {"slot": 10, "old_check": "ext_model_check", "new_check": "doc_staleness",
         "cycle": "C48", "date": "2026-03-28", "reason": "..."},
        ...
      ]
    }

Per-directory doc_staleness thresholds (doc_staleness_config.json)
-----------------------------------------------------------------
The doc_staleness check now loads per-directory thresholds from
doc_staleness_config.json. Different directories age differently:
output/tools/ docs have longer shelf life than docs/ core specs.

Thresholds are matched by path prefix (relative to project root). More
specific prefixes take priority. Falls back to global defaults if no
config file is found.

Config JSON format:
    {
      "default": {"warn_age": 5, "fail_age": 10},
      "overrides": [
        {"path_prefix": "output/tools/", "warn_age": 8, "fail_age": 15, "reason": "..."},
        ...
      ]
    }

Default checks (in order)
-------------------------
1. stub_linter             — broken import detection (old-style LTG_CHAR_/COLOR_ refs)
2. draw_order_lint         — draw order violations (W001–W004, back-pose suppression)
3. glitch_spec_lint        — Glitchkin generator spec compliance (G001–G008)
4. spec_sync_ci            — P1 character spec CI gate (Luma/Cosmo/Miri/Byte/Glitch)
5. char_spec_lint          — Detailed character spec (L001–L005, S001–S005, M001–M005)
6. dual_output_check       — dual-generator output file conflict detection
7. hardcoded_path_check    — /home/-prefixed absolute paths in active generators
8. thumbnail_lint          — unwhitelisted .thumbnail() calls
9. motion_sheet_coverage   — motion sheet coverage for characters with expression sheets
10. doc_staleness          — documentation freshness (per-directory thresholds)
11. dep_availability       — required library availability (bezier, Shapely, pycairo)
12. bezier_migration_lint  — hand-rolled bezier function migration status
13. tool_naming_lint       — LTG_TOOL_ prefix enforcement on .py files
14. char_modular_lint      — inline character drawing in scene generators

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
        {"check": "draw_order_lint", "file": "foo.py", "code": "W004",
         "reason": "...", "since_cycle": "C39"},
        ...
      ]
    }
  Fields:
    check       — one of: stub_linter, draw_order_lint, glitch_spec_lint,
                          spec_sync_ci, char_spec_lint
    file        — basename of the file producing the issue (e.g. "LTG_TOOL_foo.py")
    code        — warning/error code (e.g. "W004", "G007"); null = match any code for this file
    reason      — human-readable explanation (shown in report)
    since_cycle — cycle label when the entry was added (e.g. "C39").
                  Used by --warn-stale N to identify aged suppressions.

Stale suppression detection
----------------------------
--warn-stale N  → emit a STALE_KNOWN WARN for any known-issue entry whose
  since_cycle is N or more cycles behind the current cycle label.
  Current cycle is derived from --cycle LABEL or the CYCLE_LABEL env var.
  Cycle labels must follow the pattern C<number> (e.g. C39, C42).
  Example: --warn-stale 4 --cycle C43 flags entries added at C39 or earlier.

  Stale entries are listed in the suite report header and contribute to the
  overall WARN count (but not FAIL count). This nudges the team to review and
  either close or confirm each long-lived suppression.

Auto-seeding new FAILs
----------------------
--auto-seed  → after the suite runs, any new FAIL not already present in
  ci_known_issues.json is automatically added with status "new" and the
  current date. A summary of auto-seeded entries is printed after the
  report. The known-issues JSON file is updated in place.

  Without this flag, default behavior is unchanged — no auto-seeding.

  --auto-seed --dry-run  → preview what would be seeded without modifying
  ci_known_issues.json. Prints the same summary as --auto-seed but prefixes
  it with "[DRY RUN]" and does not write to disk. Useful for auditing
  before committing to suppression entries.

  Auto-seeded entries use the following fields:
    check       — check name that produced the FAIL
    file        — basename of the offending file
    code        — warning/error code (or null if not applicable)
    reason      — "auto-seeded by --auto-seed on YYYY-MM-DD"
    since_cycle — current cycle label (from --cycle or CYCLE_LABEL env var)
    status      — "new" (distinguishes auto-seeded from manually curated)

  Supported checks for auto-seeding:
    hardcoded_path_check, thumbnail_lint, dual_output_check,
    stub_linter, char_spec_lint, spec_sync_ci

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
    python LTG_TOOL_ci_suite.py --warn-stale 4 --cycle C43
    python LTG_TOOL_ci_suite.py --auto-seed --cycle C47
    python LTG_TOOL_ci_suite.py --auto-seed --dry-run --cycle C47

API
---
    from LTG_TOOL_ci_suite import run_suite, format_suite_report
    from LTG_TOOL_ci_suite import load_known_issues, load_known_issues_raw
    from LTG_TOOL_ci_suite import check_stale_known_issues
    from LTG_TOOL_ci_suite import check_dual_output
    from LTG_TOOL_ci_suite import check_hardcoded_paths
    from LTG_TOOL_ci_suite import check_thumbnail_lint
    from LTG_TOOL_ci_suite import check_motion_coverage
    from LTG_TOOL_ci_suite import collect_new_fails, auto_seed_known_issues
    from LTG_TOOL_ci_suite import check_doc_staleness
    from LTG_TOOL_ci_suite import load_check_registry
    from LTG_TOOL_ci_suite import check_dep_availability
    from LTG_TOOL_ci_suite import check_bezier_migration
    from LTG_TOOL_ci_suite import check_tool_naming
    from LTG_TOOL_ci_suite import check_char_modular

    known     = load_known_issues("ci_known_issues.json")
    known_raw = load_known_issues_raw("ci_known_issues.json")
    stale = check_stale_known_issues(known_raw, current_cycle="C43", max_age=4)
    result = run_suite(tools_dir="/path/to/output/tools", fail_on="FAIL",
                       known_issues=known, known_issues_raw=known_raw,
                       warn_stale=4, current_cycle="C43")
    print(format_suite_report(result))
    # result["exit_code"] is 0 (pass) or 1 (fail)
    # result["checks"] is dict keyed by check name
    # Each check result["known_count"] shows how many issues were flagged KNOWN
    # result["stale_known"] is a list of stale entry dicts (empty if warn_stale not set)
    # result["stale_warn"] is True if any stale known issues were found

Changelog
---------
v1.0.0 (C37): Initial implementation. (Kai Nakamura)
v1.1.0 (C40): --known-issues PATH flag. Loads expected WARNs from JSON;
              marks matching issues as KNOWN in report output.
              known_count added to each check result.
              format_suite_report() shows KNOWN annotation in summary.
              load_known_issues() exported for programmatic use.
              (Morgan Walsh)
v1.2.0 (C42): --warn-stale N flag. Emits STALE_KNOWN WARN for known-issue
              entries whose since_cycle is N or more cycles behind current cycle.
              --cycle LABEL flag to specify current cycle (fallback: CYCLE_LABEL
              env var). since_cycle field added to ci_known_issues.json schema.
              check_stale_known_issues() exported for programmatic use.
              stale_known list added to run_suite() result dict.
              (Morgan Walsh)
v1.3.0 (C43): Check 6 — dual_output_check. Scans all .py files in tools_dir
              for hardcoded LTG_* output filenames. FAIL if two or more active
              (non-deprecated, non-legacy) generators write to the same output
              file. Prevents dual-generator provenance ambiguity (Petra Volkov
              C17 FAIL — LTG_TOOL_style_frame_01_discovery.py conflict).
              check_dual_output() exported for programmatic use.
              (Morgan Walsh)
v1.4.0 (C44): Check 7 — hardcoded_path_check. Uses audit_hardcoded_paths()
              from LTG_TOOL_project_paths to detect /home/-prefixed absolute
              paths in active generators. FAIL on any hit not suppressed by
              ci_known_issues.json. Pre-existing hits seeded as known-issues.
              check_hardcoded_paths() exported for programmatic use.
              Check 8 — thumbnail_lint. FAIL if any active generator contains
              img.thumbnail( or .thumbnail((1920 without an inline
              # ltg-thumbnail-ok suppression comment on the same line.
              QA/analysis tools may whitelist via # ltg-thumbnail-ok.
              check_thumbnail_lint() exported for programmatic use.
              Check 9 — motion_sheet_coverage. WARN if any character has an
              expression sheet PNG in output/characters/main/ but no motion
              PNG in output/characters/motion/. check_motion_coverage()
              exported for programmatic use.
              (Morgan Walsh)
v1.5.0 (C45): known_issues suppression added to dual_output_check and
              thumbnail_lint. Both checks now load ci_known_issues.json (same
              as hardcoded_path_check) — files listed as KNOWN contribute to
              WARN only, not FAIL. Enables seeding baseline false-positives
              (contact-sheet/caption-retrofit dual-output patterns; legacy
              thumbnail() calls pending native-canvas migration) so CI reports
              WARN instead of FAIL while backlog is worked down.
              (Morgan Walsh)
v1.6.0 (C46): --auto-seed flag. After running the full CI suite, any new
              FAIL not already in ci_known_issues.json is automatically added
              with status "new" and the current date. Prints a summary of
              auto-seeded entries. Default behavior (no flag) unchanged.
              collect_new_fails() and auto_seed_known_issues() exported for
              programmatic use.
              (Morgan Walsh)
v1.7.0 (C47): --dry-run flag for --auto-seed. Previews what would be seeded
              without writing to ci_known_issues.json. Prints [DRY RUN]
              prefixed summary. Useful for auditing before committing.
              Check 10 — ext_model_check. Scans all .py files in tools_dir
              for imports of pretrained model weights (torchvision.models,
              torch.hub, transformers, huggingface_hub, .load_state_dict
              with URL downloads). FAIL if found, with file + line number.
              check_ext_models() exported for programmatic use.
              (Morgan Walsh)
v1.8.0 (C48): REMOVED Check 10 ext_model_check — pretrained models ARE
              allowed (policy correction). check_ext_models() removed.
              NEW Check 10 — doc_staleness. Uses LTG_TOOL_doc_governance_audit
              to flag stale documentation. WARN for docs not updated in 5+
              cycles, FAIL for 10+ cycles. Configurable thresholds via
              doc_staleness_warn_age and doc_staleness_fail_age params.
              check_doc_staleness() exported for programmatic use.
              (Morgan Walsh)
v1.9.0 (C49): CI Check Registry — config-driven check slot management.
              ci_check_registry.json defines which check occupies each slot.
              Checks can be swapped, enabled/disabled, or reordered by editing
              the JSON — no code changes needed. Swap history tracked in the
              same file. Falls back to hardcoded _CHECKS list if registry
              absent (fully backwards compatible).
              load_check_registry() exported for programmatic use.
              Per-directory doc_staleness thresholds — doc_staleness_config.json
              provides per-directory warn_age/fail_age overrides. Matched by
              path prefix (most specific wins). Falls back to global defaults
              if config absent.
              (Morgan Walsh)
v2.0.0 (C52): Check 11 — dep_availability. Verifies required pipeline
              libraries (bezier, Shapely, pycairo) are importable. WARN if
              any missing. check_dep_availability() exported.
              Check 12 — bezier_migration_lint. Wraps curve_utils --audit
              to detect files still using hand-rolled bezier functions.
              WARN for pending migrations. check_bezier_migration() exported.
              Check 13 — tool_naming_lint. Enforces LTG_TOOL_ prefix on all
              .py files in tools dir. Legacy/deprecated subdirs exempt.
              WARN for non-compliant files. check_tool_naming() exported.
              (Morgan Walsh)
"""

__version__ = "2.1.0"

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


# ── Check Registry ───────────────────────────────────────────────────────────

def load_check_registry(tools_dir=None):
    """
    Load the CI check registry from ci_check_registry.json.

    Parameters
    ----------
    tools_dir : str | None
        Path to output/tools/. Defaults to the directory of this script.

    Returns
    -------
    dict | None
        The parsed registry dict, or None if the file is absent or invalid.
        Registry structure: {"slots": [...], "swap_history": [...]}
    """
    td = _tools_dir_or_default(tools_dir)
    reg_path = os.path.join(td, "ci_check_registry.json")
    if not os.path.exists(reg_path):
        return None
    try:
        with open(reg_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data
    except (OSError, json.JSONDecodeError):
        return None


def _resolve_checks_from_registry(registry):
    """
    Convert a registry dict into the _CHECKS list format.

    Parameters
    ----------
    registry : dict
        Parsed ci_check_registry.json data.

    Returns
    -------
    list[tuple]
        List of (check_name, runner_func, label) tuples, same format as _CHECKS.
        Only enabled slots are included, sorted by slot number.
    """
    # Map check names to runner functions
    _RUNNER_MAP = {
        "stub_linter":          _run_stub_linter,
        "draw_order_lint":      _run_draw_order_lint,
        "glitch_spec_lint":     _run_glitch_spec_lint,
        "spec_sync_ci":         _run_spec_sync_ci,
        "char_spec_lint":       _run_char_spec_lint,
        "dual_output_check":    _run_dual_output_check,
        "hardcoded_path_check": _run_hardcoded_path_check,
        "thumbnail_lint":       _run_thumbnail_lint,
        "motion_sheet_coverage":_run_motion_coverage,
        "doc_staleness":        _run_doc_staleness,
        "dep_availability":     _run_dep_availability,
        "bezier_migration_lint":_run_bezier_migration_lint,
        "tool_naming_lint":     _run_tool_naming_lint,
        "char_modular_lint":    _run_char_modular_lint,
    }

    slots = registry.get("slots", [])
    # Sort by slot number
    slots_sorted = sorted(slots, key=lambda s: s.get("slot", 0))

    checks = []
    for slot in slots_sorted:
        if not slot.get("enabled", True):
            continue
        check_name = slot.get("check", "")
        label = slot.get("label", check_name)
        runner = _RUNNER_MAP.get(check_name)
        if runner is None:
            # Unknown check name — create an error runner
            def _make_unknown_runner(name):
                def _unknown(tools_dir):
                    return "ERROR", f"Unknown check '{name}' — not in runner map", ""
                return _unknown
            runner = _make_unknown_runner(check_name)
        checks.append((check_name, runner, label))

    return checks


def _get_checks(tools_dir):
    """
    Get the check list, preferring the registry if available.
    Falls back to the hardcoded _CHECKS list.

    Parameters
    ----------
    tools_dir : str
        Path to output/tools/.

    Returns
    -------
    list[tuple]
        List of (check_name, runner_func, label) tuples.
    str
        Source: "registry" or "hardcoded".
    """
    registry = load_check_registry(tools_dir)
    if registry is not None:
        checks = _resolve_checks_from_registry(registry)
        if checks:
            return checks, "registry"
    return _CHECKS, "hardcoded"


# ── Doc staleness config ─────────────────────────────────────────────────────

def _load_doc_staleness_config(tools_dir=None):
    """
    Load per-directory doc staleness thresholds from doc_staleness_config.json.

    Returns
    -------
    dict | None
        The parsed config dict, or None if absent/invalid.
        Structure: {"default": {warn_age, fail_age}, "overrides": [...]}
    """
    td = _tools_dir_or_default(tools_dir)
    cfg_path = os.path.join(td, "doc_staleness_config.json")
    if not os.path.exists(cfg_path):
        return None
    try:
        with open(cfg_path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None


def _get_thresholds_for_path(rel_path, config):
    """
    Get (warn_age, fail_age) for a given relative path using the config.
    Most specific (longest) matching path_prefix wins.

    Parameters
    ----------
    rel_path : str
        File path relative to project root (forward slashes).
    config : dict
        Parsed doc_staleness_config.json.

    Returns
    -------
    tuple[int, int]
        (warn_age, fail_age)
    """
    default_warn = config.get("default", {}).get("warn_age", 5)
    default_fail = config.get("default", {}).get("fail_age", 10)

    best_prefix_len = 0
    best_warn = default_warn
    best_fail = default_fail

    # Normalise path separators
    norm_path = rel_path.replace("\\", "/")

    for override in config.get("overrides", []):
        prefix = override.get("path_prefix", "").replace("\\", "/")
        if norm_path.startswith(prefix) and len(prefix) > best_prefix_len:
            best_prefix_len = len(prefix)
            best_warn = override.get("warn_age", default_warn)
            best_fail = override.get("fail_age", default_fail)

    return best_warn, best_fail


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


def load_known_issues_raw(path):
    """
    Load a known-issues JSON file and return the raw list of entry dicts.
    Used by check_stale_known_issues() which needs the full entry including
    the since_cycle field.

    Parameters
    ----------
    path : str | None
        Path to the known-issues JSON file, or None to return empty list.

    Returns
    -------
    list  [ {check, file, code, reason, since_cycle, ...}, ... ]
          Empty list on any error.
    """
    if not path:
        return []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data.get("known_issues", [])
    except Exception:
        return []


def _parse_cycle_number(cycle_label):
    """
    Parse a cycle label such as 'C42' into an integer (42).
    Returns None if the label does not match the expected pattern.
    """
    import re as _re
    m = _re.match(r'^[Cc](\d+)$', str(cycle_label).strip())
    if m:
        return int(m.group(1))
    return None


def check_stale_known_issues(known_issues_raw, current_cycle, max_age):
    """
    Return a list of known-issue entries that are considered stale.

    An entry is stale when:
        current_cycle_number - since_cycle_number >= max_age

    Parameters
    ----------
    known_issues_raw : list
        The raw list from the 'known_issues' key of the JSON file, i.e.
        each element is a dict with at least 'check', 'file', 'code',
        'reason', and optionally 'since_cycle'.
    current_cycle : str
        Cycle label for the current run, e.g. "C42".
    max_age : int
        Emit a stale warning when an entry's age (in cycles) is >= this value.

    Returns
    -------
    list of dict
        Each dict is a copy of the entry with an added 'age' key showing
        how many cycles old it is.  Entries without a since_cycle field are
        skipped (cannot determine age).
    """
    if max_age is None or max_age <= 0:
        return []
    current_num = _parse_cycle_number(current_cycle)
    if current_num is None:
        return []
    stale = []
    for entry in (known_issues_raw or []):
        sc = entry.get("since_cycle")
        if not sc:
            continue
        sc_num = _parse_cycle_number(sc)
        if sc_num is None:
            continue
        age = current_num - sc_num
        if age >= max_age:
            stale_entry = dict(entry)
            stale_entry["age"] = age
            stale.append(stale_entry)
    return stale


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


# ── Check 6: dual_output_check ─────────────────────────────────────────────

def check_dual_output(tools_dir):
    """
    Scan all active .py files in tools_dir for LTG_* output filenames.
    Return a dict of {output_filename: [list_of_generators]} for any output
    filename claimed by more than one active generator.

    "Active" means: not in deprecated/ or legacy/ subdirectories, and not
    the script itself (ci_suite) or stub/lint/qa tools (which read but don't
    write).

    Parameters
    ----------
    tools_dir : str
        Path to the output/tools/ directory.

    Returns
    -------
    dict  { "LTG_FOO_bar.png": ["gen_a.py", "gen_b.py"], ... }
          Only entries with 2+ generators are returned.
    """
    import re as _re
    # Pattern: LTG_ followed by category prefix, then a filename with .png/.svg/.json/.md
    # Matches string literals in source: "LTG_COLOR_foo.png", 'LTG_ENV_bar.png', etc.
    _OUTFILE_PAT = _re.compile(r'["\']?(LTG_(?:COLOR|ENV|CHAR|BRAND|SB|TOOL|PROD)_[A-Za-z0-9_.]+\.(?:png|svg|json|md))["\']?')

    # Tool files we should skip (CI/QA/lint tools that reference filenames but don't generate them)
    _SKIP_PREFIXES = (
        "LTG_TOOL_ci_suite",
        "LTG_TOOL_precritique_qa",
        "LTG_TOOL_readme_sync",
        "LTG_TOOL_stub_linter",
        "LTG_TOOL_draw_order_lint",
        "LTG_TOOL_glitch_spec_lint",
        "LTG_TOOL_spec_sync_ci",
        "LTG_TOOL_char_spec_lint",
        "LTG_TOOL_render_qa",
        "LTG_TOOL_color_fidelity",
        "LTG_TOOL_proportion_verify",
        "LTG_TOOL_proportion_audit",
        "LTG_TOOL_fidelity_check",
        "LTG_TOOL_naming_compliance",
        "LTG_TOOL_naming_cleanup",
        "LTG_TOOL_face_curves_caller_audit",
        "LTG_TOOL_project_paths",
        "LTG_TOOL_sobel_vp_detect",
        "LTG_TOOL_vanishing_point_lint",
        "LTG_TOOL_world_type_infer",
        "LTG_TOOL_alpha_blend_lint",
        "LTG_TOOL_fill_light_adapter",
        "LTG_TOOL_sight_line_diagnostic",
        "LTG_TOOL_motion_spec_lint",
        "LTG_TOOL_palette_warmth_lint",
        "LTG_TOOL_arc_diff",
        "LTG_TOOL_contact_sheet_arc_diff",
        "run_",
    )

    output_map = {}  # { output_filename: [generator_basename, ...] }

    tools_path = os.path.abspath(tools_dir)
    for fname in sorted(os.listdir(tools_path)):
        if not fname.endswith(".py"):
            continue
        # Skip CI/QA/lint tools
        if any(fname.startswith(pfx) for pfx in _SKIP_PREFIXES):
            continue
        fpath = os.path.join(tools_path, fname)
        if not os.path.isfile(fpath):
            continue
        try:
            src = open(fpath, "r", encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        # Look for save/output assignment patterns that suggest this file GENERATES an output
        # Heuristic: file must contain .save( or img.save to be a generator
        if ".save(" not in src and "ImageDraw" not in src:
            continue
        matches = set(_OUTFILE_PAT.findall(src))
        # Filter to only LTG_COLOR_/LTG_ENV_/LTG_CHAR_/LTG_BRAND_/LTG_SB_ outputs
        # (exclude LTG_TOOL_ references which are script-name refs, not outputs)
        for m in matches:
            if m.startswith("LTG_TOOL_"):
                continue
            output_map.setdefault(m, []).append(fname)

    # Return only conflicts (2+ generators per output)
    return {k: v for k, v in output_map.items() if len(v) >= 2}


def _run_dual_output_check(tools_dir):
    """Run dual-output-file check. Returns (status, summary, details).

    Files listed in ci_known_issues.json under check='dual_output_check'
    are treated as KNOWN (pre-existing / by-design patterns such as contact
    sheets and caption-retrofit tools). Known files contribute to WARN count
    only — not FAIL. New unrecognised conflicts cause FAIL.
    """
    try:
        conflicts = check_dual_output(tools_dir)
        if not conflicts:
            return "PASS", "0 output filename conflict(s)", ""

        # Load known-issues to distinguish by-design from real conflicts
        _ki_path = os.path.join(tools_dir, "ci_known_issues.json")
        _known_generators = set()
        if os.path.exists(_ki_path):
            try:
                with open(_ki_path, "r", encoding="utf-8") as _fh:
                    _ki_data = json.load(_fh)
                for _entry in _ki_data.get("known_issues", []):
                    if _entry.get("check") == "dual_output_check":
                        _known_generators.add(_entry.get("file", ""))
            except (OSError, json.JSONDecodeError):
                pass

        # A conflict is "new" if ANY generator in the conflict group is not known
        # A conflict is "known" only if ALL generators in the group are known
        new_conflicts = {}
        known_conflicts = {}
        for outfile, generators in conflicts.items():
            unknown_gens = [g for g in generators if g not in _known_generators]
            if unknown_gens:
                new_conflicts[outfile] = generators
            else:
                known_conflicts[outfile] = generators

        lines = []
        if new_conflicts:
            lines.append(f"NEW DUAL-OUTPUT CONFLICTS ({len(new_conflicts)} output file(s)):")
            for outfile, generators in sorted(new_conflicts.items()):
                lines.append(f"  {outfile}")
                for g in generators:
                    lines.append(f"    ← {g}")
        if known_conflicts:
            lines.append(f"KNOWN DUAL-OUTPUT (by-design patterns — {len(known_conflicts)} output file(s)):")
            for outfile, generators in sorted(known_conflicts.items()):
                lines.append(f"  {outfile}  [KNOWN]")
                for g in generators:
                    lines.append(f"    ← {g}")

        details = "\n".join(lines)
        total_gen = sum(len(v) for v in conflicts.values())
        if new_conflicts:
            summary = (
                f"{len(new_conflicts)} NEW conflict(s) + {len(known_conflicts)} KNOWN — "
                f"{total_gen} generator(s) involved"
            )
            return "FAIL", summary, details
        else:
            summary = (
                f"{len(known_conflicts)} KNOWN conflict(s) (all by-design) — "
                f"{total_gen} generator(s) involved"
            )
            return "WARN", summary, details
    except Exception as exc:
        return "ERROR", f"dual_output_check error: {exc}", ""


# ── Check 7: hardcoded_path_check ─────────────────────────────────────────────

def check_hardcoded_paths(tools_dir):
    """
    Scan all active .py files in tools_dir for hardcoded /home/ paths.
    Uses audit_hardcoded_paths() from LTG_TOOL_project_paths.

    Returns
    -------
    list[dict]  Each entry: {file, line, text}
                Only files in tools_dir root (not deprecated/ subdirectory).
    """
    _add_to_path(tools_dir)
    try:
        import LTG_TOOL_project_paths as pp
        findings = pp.audit_hardcoded_paths(tools_directory=tools_dir)
        # Filter out deprecated/ subdirectory files (audit already only does *.py in root)
        return findings
    except ImportError:
        return None  # signals import failure


def _run_hardcoded_path_check(tools_dir):
    """Run hardcoded path check. Returns (status, summary, details).

    Files listed in ci_known_issues.json under check='hardcoded_path_check'
    are treated as KNOWN (pre-existing migration backlog) — they contribute
    to WARN count but not FAIL. Files not in known_issues cause FAIL.
    This lets CI be green on first pass while new violations still block.
    """
    try:
        findings = check_hardcoded_paths(tools_dir)
        if findings is None:
            return "ERROR", "Could not import LTG_TOOL_project_paths", ""
        if not findings:
            return "PASS", "0 hardcoded /home/ path(s) in active generators", ""

        # Load known-issues to distinguish pre-existing from new violations
        _ki_path = os.path.join(tools_dir, "ci_known_issues.json")
        _known_files = set()
        if os.path.exists(_ki_path):
            try:
                with open(_ki_path, "r", encoding="utf-8") as _fh:
                    _ki_data = json.load(_fh)
                for _entry in _ki_data.get("known_issues", []):
                    if _entry.get("check") == "hardcoded_path_check":
                        _known_files.add(_entry.get("file", ""))
            except (OSError, json.JSONDecodeError):
                pass

        # Group by file
        by_file = {}
        for f in findings:
            by_file.setdefault(f["file"], []).append(f)

        new_files = sorted(k for k in by_file if k not in _known_files)
        known_files = sorted(k for k in by_file if k in _known_files)

        lines = []
        for fname in new_files:
            hits = by_file[fname]
            lines.append(f"  FAIL  {fname}  ({len(hits)} hit(s)) — not in known_issues")
            for h in hits:
                lines.append(f"    L{h['line']:4d}  {h['text'][:80]}")
        for fname in known_files:
            hits = by_file[fname]
            lines.append(f"  KNOWN {fname}  ({len(hits)} hit(s)) — migration backlog")
            for h in hits:
                lines.append(f"    L{h['line']:4d}  {h['text'][:80]}")

        if lines:
            lines.append("  → Migrate: replace /home/wipkat/team/output/... with output_dir() from LTG_TOOL_project_paths")
            lines.append("  → Add entry to ci_known_issues.json under hardcoded_path_check once resolved")

        details = "\n".join(lines)
        total_hits = sum(len(v) for v in by_file.values())
        if new_files:
            summary = (
                f"{total_hits} hardcoded /home/ occurrence(s) in {len(by_file)} file(s): "
                f"{len(new_files)} NEW (FAIL) + {len(known_files)} KNOWN (migration backlog)"
            )
            return "FAIL", summary, details
        else:
            summary = (
                f"{total_hits} hardcoded /home/ occurrence(s) in {len(by_file)} KNOWN file(s) "
                f"(migration backlog — no new violations)"
            )
            return "WARN", summary, details
    except Exception as exc:
        return "ERROR", f"hardcoded_path_check error: {exc}", ""


# ── Check 8: thumbnail_lint ────────────────────────────────────────────────────

def check_thumbnail_lint(tools_dir):
    """
    Scan all active .py files in tools_dir for thumbnail() calls in generator
    context. Lines with '# ltg-thumbnail-ok' on the same line are whitelisted.

    Detects patterns:
      - img.thumbnail(
      - .thumbnail((1920
    (both indicate LANCZOS downscale from an oversized canvas — pipeline error)

    Returns
    -------
    list[dict]  Each entry: {file, line, text}
                Only files in tools_dir root.
    """
    import re as _re
    _THUMB_PAT = _re.compile(r'\.thumbnail\(')
    _WHITELIST  = "# ltg-thumbnail-ok"

    # Skip CI/QA/analysis tools (they may call thumbnail for inspection, not generation)
    _SKIP_PREFIXES = (
        "LTG_TOOL_ci_suite",
        "LTG_TOOL_precritique_qa",
        "LTG_TOOL_readme_sync",
        "LTG_TOOL_stub_linter",
        "LTG_TOOL_draw_order_lint",
        "LTG_TOOL_glitch_spec_lint",
        "LTG_TOOL_spec_sync_ci",
        "LTG_TOOL_char_spec_lint",
        "LTG_TOOL_render_qa",
        "LTG_TOOL_color_fidelity",
        "LTG_TOOL_proportion_verify",
        "LTG_TOOL_proportion_audit",
        "LTG_TOOL_fidelity_check",
        "LTG_TOOL_naming_compliance",
        "LTG_TOOL_naming_cleanup",
        "LTG_TOOL_face_curves_caller_audit",
        "LTG_TOOL_project_paths",
        "LTG_TOOL_sobel_vp_detect",
        "LTG_TOOL_vanishing_point_lint",
        "LTG_TOOL_world_type_infer",
        "LTG_TOOL_alpha_blend_lint",
        "LTG_TOOL_fill_light_adapter",
        "LTG_TOOL_sight_line_diagnostic",
        "LTG_TOOL_motion_spec_lint",
        "LTG_TOOL_palette_warmth_lint",
        "LTG_TOOL_arc_diff",
        "LTG_TOOL_contact_sheet_arc_diff",
        "LTG_TOOL_render_lib",
        "run_",
    )

    findings = []
    tools_path = os.path.abspath(tools_dir)
    for fname in sorted(os.listdir(tools_path)):
        if not fname.endswith(".py"):
            continue
        if any(fname.startswith(pfx) for pfx in _SKIP_PREFIXES):
            continue
        fpath = os.path.join(tools_path, fname)
        if not os.path.isfile(fpath):
            continue
        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as fh:
                lines = fh.readlines()
        except OSError:
            continue
        for lineno, line in enumerate(lines, 1):
            if _THUMB_PAT.search(line) and _WHITELIST not in line:
                findings.append({"file": fname, "line": lineno, "text": line.rstrip()})
    return findings


def _run_thumbnail_lint(tools_dir):
    """Run thumbnail lint check. Returns (status, summary, details).

    Files listed in ci_known_issues.json under check='thumbnail_lint' are
    treated as KNOWN (pre-existing migration backlog or legitimate analysis
    tools). KNOWN files contribute to WARN count only — not FAIL. New files
    with unwhitelisted thumbnail() calls cause FAIL.
    """
    try:
        findings = check_thumbnail_lint(tools_dir)
        if not findings:
            return "PASS", "0 unwhitelisted thumbnail() call(s) in active generators", ""

        # Load known-issues to separate backlog from new violations
        _ki_path = os.path.join(tools_dir, "ci_known_issues.json")
        _known_files = set()
        if os.path.exists(_ki_path):
            try:
                with open(_ki_path, "r", encoding="utf-8") as _fh:
                    _ki_data = json.load(_fh)
                for _entry in _ki_data.get("known_issues", []):
                    if _entry.get("check") == "thumbnail_lint":
                        _known_files.add(_entry.get("file", ""))
            except (OSError, json.JSONDecodeError):
                pass

        by_file = {}
        for f in findings:
            by_file.setdefault(f["file"], []).append(f)

        new_files    = sorted(k for k in by_file if k not in _known_files)
        known_files  = sorted(k for k in by_file if k in _known_files)

        lines = []
        for fname in new_files:
            hits = by_file[fname]
            lines.append(f"  FAIL  {fname}  ({len(hits)} hit(s))")
            for h in hits:
                lines.append(f"    L{h['line']:4d}  {h['text'][:80]}")
            lines.append(f"         → Use native 1280×720 canvas instead.")
            lines.append(f"         → Add '# ltg-thumbnail-ok' to whitelist legitimate analysis uses.")
        for fname in known_files:
            hits = by_file[fname]
            lines.append(f"  KNOWN {fname}  ({len(hits)} hit(s)) — migration backlog")
            for h in hits:
                lines.append(f"    L{h['line']:4d}  {h['text'][:80]}")

        details = "\n".join(lines)
        total_hits = sum(len(v) for v in by_file.values())
        if new_files:
            summary = (
                f"{total_hits} unwhitelisted .thumbnail() call(s) in "
                f"{len(by_file)} generator(s): {len(new_files)} NEW (FAIL) + "
                f"{len(known_files)} KNOWN (migration backlog)"
            )
            return "FAIL", summary, details
        else:
            summary = (
                f"{total_hits} .thumbnail() call(s) in {len(by_file)} KNOWN generator(s) "
                f"(migration backlog — no new violations)"
            )
            return "WARN", summary, details
    except Exception as exc:
        return "ERROR", f"thumbnail_lint error: {exc}", ""


# ── Check 9: motion_sheet_coverage ────────────────────────────────────────────

def check_motion_coverage(tools_dir):
    """
    Check that every character with an expression sheet PNG in
    output/characters/main/ also has a motion PNG in output/characters/motion/.

    Expression sheets are identified by pattern: LTG_CHAR_<name>_expression_sheet.png
    Motion sheets are identified by pattern: LTG_CHAR_<name>_motion.png

    Returns
    -------
    list[str]  Character names missing a motion sheet. Empty = all present.
    """
    # Infer output/ root from tools_dir (tools_dir is output/tools/)
    tools_path = os.path.abspath(tools_dir)
    output_root = os.path.dirname(tools_path)  # output/
    main_dir   = os.path.join(output_root, "characters", "main")
    motion_dir = os.path.join(output_root, "characters", "motion")

    if not os.path.isdir(main_dir) or not os.path.isdir(motion_dir):
        return None  # directories not found — skip

    import re as _re
    expr_pat   = _re.compile(r"LTG_CHAR_([a-z_]+)_expression_sheet\.png$", _re.IGNORECASE)
    motion_pat = _re.compile(r"LTG_CHAR_([a-z_]+)_motion\.png$", _re.IGNORECASE)

    expr_chars   = set()
    motion_chars = set()

    for fname in os.listdir(main_dir):
        m = expr_pat.match(fname)
        if m:
            expr_chars.add(m.group(1).lower())

    for fname in os.listdir(motion_dir):
        m = motion_pat.match(fname)
        if m:
            motion_chars.add(m.group(1).lower())

    missing = sorted(expr_chars - motion_chars)
    return missing


def _run_motion_coverage(tools_dir):
    """Run motion sheet coverage check. Returns (status, summary, details)."""
    try:
        missing = check_motion_coverage(tools_dir)
        if missing is None:
            return "WARN", "characters/main/ or characters/motion/ not found — skipping", ""
        if not missing:
            return "PASS", "All characters with expression sheets have motion sheets", ""
        details_lines = []
        for char in missing:
            details_lines.append(
                f"  WARN  {char}: LTG_CHAR_{char}_expression_sheet.png exists "
                f"but LTG_CHAR_{char}_motion.png is missing"
            )
        details = "\n".join(details_lines)
        summary = (
            f"{len(missing)} character(s) missing motion sheet: "
            f"{', '.join(missing)}"
        )
        return "WARN", summary, details
    except Exception as exc:
        return "ERROR", f"motion_coverage error: {exc}", ""


# ── Check 10: Doc Staleness ───────────────────────────────────────────────────


def check_doc_staleness(current_cycle=49, warn_age=5, fail_age=10,
                        project_root=None, tools_dir=None):
    """
    Check documentation freshness by delegating to LTG_TOOL_doc_governance_audit.

    When doc_staleness_config.json is present in tools_dir, per-directory
    thresholds override the global warn_age/fail_age defaults. Each doc is
    evaluated against the most specific matching path prefix.

    Parameters
    ----------
    current_cycle : int
        Current cycle number (e.g. 49).
    warn_age : int
        Global default cycles for WARN (default 5). Overridden by config.
    fail_age : int
        Global default cycles for FAIL (default 10). Overridden by config.
    project_root : str | None
        Project root directory. Auto-detected if None.
    tools_dir : str | None
        Path to output/tools/. Used to locate doc_staleness_config.json.

    Returns
    -------
    dict
        {
          "warn_docs": list[dict],   # docs stale >= warn_age but < fail_age
          "fail_docs": list[dict],   # docs stale >= fail_age
          "no_cycle_ref": list[dict], # docs with no cycle reference
          "recent_docs": list[dict],  # docs that are fresh
          "total_scanned": int,
          "config_source": str,       # "per_directory" or "global"
        }
        Each doc dict has: path, max_cycle (int or None), age (int or None).
        When per-directory config is active, docs also have: threshold_warn, threshold_fail.
    """
    try:
        from LTG_TOOL_doc_governance_audit import audit_docs
    except ImportError:
        return {
            "warn_docs": [], "fail_docs": [], "no_cycle_ref": [],
            "recent_docs": [], "total_scanned": 0, "config_source": "global",
            "_error": "Could not import LTG_TOOL_doc_governance_audit",
        }

    # Load per-directory config if available
    ds_config = _load_doc_staleness_config(tools_dir)

    # Run the audit with a very low threshold (1) so we get ALL docs with cycle refs
    # back as either "stale" or "recent". We then apply our own thresholds per doc.
    # Use warn_age=1 to get everything classified.
    result = audit_docs(
        current_cycle=current_cycle,
        stale_threshold=1,  # get everything with age >= 1 as "stale"
        project_root=project_root,
    )

    # Combine stale + recent — we re-classify with per-directory thresholds
    all_docs = list(result.get("stale", [])) + list(result.get("recent", []))

    warn_docs = []
    fail_docs = []
    recent_docs = []

    if ds_config is not None:
        # Per-directory mode
        config_source = "per_directory"
        for entry in all_docs:
            doc_warn, doc_fail = _get_thresholds_for_path(entry["path"], ds_config)
            entry_out = dict(entry)
            entry_out["threshold_warn"] = doc_warn
            entry_out["threshold_fail"] = doc_fail
            age = entry.get("age", 0)
            if age >= doc_fail:
                fail_docs.append(entry_out)
            elif age >= doc_warn:
                warn_docs.append(entry_out)
            else:
                recent_docs.append(entry_out)
    else:
        # Global mode (backwards compatible)
        config_source = "global"
        for entry in all_docs:
            age = entry.get("age", 0)
            if age >= fail_age:
                fail_docs.append(entry)
            elif age >= warn_age:
                warn_docs.append(entry)
            else:
                recent_docs.append(entry)

    # Sort
    fail_docs.sort(key=lambda x: -x.get("age", 0))
    warn_docs.sort(key=lambda x: -x.get("age", 0))
    recent_docs.sort(key=lambda x: -x.get("age", 0))

    return {
        "warn_docs": warn_docs,
        "fail_docs": fail_docs,
        "no_cycle_ref": result.get("no_cycle_ref", []),
        "recent_docs": recent_docs,
        "total_scanned": result.get("total_scanned", 0),
        "config_source": config_source,
    }


def _run_doc_staleness(tools_dir):
    """Run doc staleness check. Returns (status, summary, details).

    Loads per-directory thresholds from doc_staleness_config.json if present.
    """
    # Derive current cycle from env or default to 49
    cycle_str = os.environ.get("CYCLE_LABEL", "C49")
    try:
        current_cycle = int(cycle_str.lstrip("Cc"))
    except (ValueError, AttributeError):
        current_cycle = 49

    try:
        result = check_doc_staleness(current_cycle=current_cycle, tools_dir=tools_dir)
    except Exception as exc:
        return "ERROR", f"doc_staleness error: {exc}", ""

    if result.get("_error"):
        return "ERROR", result["_error"], ""

    fail_docs = result["fail_docs"]
    warn_docs = result["warn_docs"]
    no_ref = result["no_cycle_ref"]
    total = result["total_scanned"]
    config_source = result.get("config_source", "global")

    details_lines = []
    if config_source == "per_directory":
        details_lines.append("(Using per-directory thresholds from doc_staleness_config.json)")
        details_lines.append("")

    if fail_docs:
        details_lines.append(f"FAIL — {len(fail_docs)} doc(s) past fail threshold:")
        for d in fail_docs:
            threshold_note = ""
            if "threshold_fail" in d:
                threshold_note = f"  [threshold: {d['threshold_fail']}]"
            details_lines.append(
                f"  FAIL  C{d['max_cycle']:<3d}  (age {d['age']:>2d})  {d['path']}{threshold_note}"
            )
    if warn_docs:
        details_lines.append(f"WARN — {len(warn_docs)} doc(s) past warn threshold:")
        for d in warn_docs:
            threshold_note = ""
            if "threshold_warn" in d:
                threshold_note = f"  [threshold: {d['threshold_warn']}]"
            details_lines.append(
                f"  WARN  C{d['max_cycle']:<3d}  (age {d['age']:>2d})  {d['path']}{threshold_note}"
            )
    if no_ref:
        details_lines.append(f"INFO — {len(no_ref)} doc(s) with no cycle reference (not scored)")

    details = "\n".join(details_lines)

    if fail_docs:
        summary = (
            f"{len(fail_docs)} FAIL + {len(warn_docs)} WARN "
            f"out of {total} docs scanned ({config_source} thresholds)"
        )
        return "FAIL", summary, details
    elif warn_docs:
        summary = (
            f"{len(warn_docs)} WARN out of {total} docs scanned ({config_source} thresholds)"
        )
        return "WARN", summary, details
    else:
        summary = f"All {total} docs are fresh ({config_source} thresholds)"
        return "PASS", summary, details


# ── Check 11: dep_availability — library dependency check ────────────────────

_REQUIRED_DEPS = [
    ("bezier", "pip install bezier", "Bezier curve math (LTG_TOOL_curve_utils)"),
    ("shapely", "pip install Shapely", "Silhouette polygon ops (LTG_TOOL_curve_utils)"),
    ("cairo", "pip install pycairo", "Character rendering (bezier strokes, anti-alias)"),
]


def check_dep_availability(tools_dir=None):
    """
    Check that required pipeline libraries are importable.

    Returns
    -------
    dict  {"status": str, "available": list, "missing": list}
    """
    available = []
    missing = []
    for mod_name, install_cmd, description in _REQUIRED_DEPS:
        try:
            __import__(mod_name)
            available.append(mod_name)
        except ImportError:
            missing.append({"module": mod_name, "install": install_cmd,
                            "description": description})
    return {
        "status": "FAIL" if missing else "PASS",
        "available": available,
        "missing": missing,
    }


def _run_dep_availability(tools_dir):
    """Run dependency availability check. Returns (status, summary, details)."""
    result = check_dep_availability(tools_dir)
    n_ok = len(result["available"])
    n_miss = len(result["missing"])
    total = n_ok + n_miss
    if n_miss:
        details_lines = [f"MISSING — {n_miss} required library/libraries not importable:"]
        for m in result["missing"]:
            details_lines.append(
                f"  FAIL  {m['module']:<12s}  ({m['description']})  — install: {m['install']}"
            )
        if n_ok:
            details_lines.append(f"\nAvailable ({n_ok}): {', '.join(result['available'])}")
        details = "\n".join(details_lines)
        return "WARN", f"{n_miss} missing out of {total} required deps", details
    else:
        return "PASS", f"All {total} required deps available", ""


# ── Check 12: bezier_migration_lint — hand-rolled bezier detection ───────────

def check_bezier_migration(tools_dir=None):
    """
    Run the curve_utils audit to find files with hand-rolled bezier functions.

    Returns
    -------
    dict  {"status": str, "migrated": int, "partial": int, "pending": int,
           "total": int, "pending_files": list}
    """
    td = _tools_dir_or_default(tools_dir)
    _add_to_path(td)
    try:
        import LTG_TOOL_curve_utils as cu
        if hasattr(cu, "audit_hand_rolled_bezier"):
            audit = cu.audit_hand_rolled_bezier(td)
            migrated = sum(1 for r in audit if r.get("status") == "MIGRATED")
            partial = sum(1 for r in audit if r.get("status") == "PARTIAL")
            pending = sum(1 for r in audit if r.get("status") == "NOT_MIGRATED")
            pending_files = [
                r.get("file", "?") for r in audit
                if r.get("status") == "NOT_MIGRATED"
            ]
            total = len(audit)
            status = "PASS" if pending == 0 else "WARN"
            return {
                "status": status, "migrated": migrated, "partial": partial,
                "pending": pending, "total": total, "pending_files": pending_files,
            }
        else:
            return {"status": "ERROR", "migrated": 0, "partial": 0,
                    "pending": 0, "total": 0, "pending_files": [],
                    "_error": "audit_hand_rolled_bezier not found in curve_utils"}
    except ImportError as exc:
        return {"status": "ERROR", "migrated": 0, "partial": 0,
                "pending": 0, "total": 0, "pending_files": [],
                "_error": f"curve_utils import error: {exc}"}


def _run_bezier_migration_lint(tools_dir):
    """Run bezier migration lint. Returns (status, summary, details)."""
    result = check_bezier_migration(tools_dir)
    if result.get("_error"):
        return "ERROR", f"bezier_migration_lint error: {result['_error']}", ""
    m = result["migrated"]
    pa = result["partial"]
    pe = result["pending"]
    total = result["total"]
    if pe > 0:
        details_lines = [f"PENDING — {pe} file(s) still using hand-rolled bezier:"]
        for f in result["pending_files"]:
            details_lines.append(f"  WARN  {f}")
        if pa > 0:
            details_lines.append(f"\nPartial migrations: {pa}")
        details_lines.append(f"Fully migrated: {m}")
        details = "\n".join(details_lines)
        return "WARN", f"{pe} pending, {pa} partial, {m} migrated (of {total})", details
    else:
        summary = f"All {total} bezier files migrated ({m} full, {pa} partial)"
        return "PASS", summary, ""


# ── Check 13: tool_naming_lint — LTG_TOOL_ prefix enforcement ───────────────

# Files exempt from the naming convention (known non-tool scripts)
_NAMING_EXEMPT = {
    "__init__.py", "__pycache__",
}


def check_tool_naming(tools_dir=None):
    """
    Check that all .py files in tools_dir follow the LTG_TOOL_ prefix convention.
    Files in legacy/ and deprecated/ subdirectories are exempt from the prefix
    requirement (but flagged as INFO). Files starting with __ are exempt.

    Returns
    -------
    dict  {"status": str, "compliant": list, "non_compliant": list, "exempt": list}
    """
    import glob as _glob
    td = _tools_dir_or_default(tools_dir)
    compliant = []
    non_compliant = []
    exempt = []

    # Only scan top-level .py files (not subdirectories like legacy/, deprecated/)
    pattern = os.path.join(td, "*.py")
    for fpath in sorted(_glob.glob(pattern)):
        basename = os.path.basename(fpath)
        if basename in _NAMING_EXEMPT or basename.startswith("__"):
            exempt.append(basename)
            continue
        if basename.startswith("LTG_TOOL_"):
            compliant.append(basename)
        else:
            non_compliant.append(basename)

    status = "WARN" if non_compliant else "PASS"
    return {
        "status": status,
        "compliant": compliant,
        "non_compliant": non_compliant,
        "exempt": exempt,
    }


def _run_tool_naming_lint(tools_dir):
    """Run tool naming convention lint. Returns (status, summary, details)."""
    result = check_tool_naming(tools_dir)
    n_ok = len(result["compliant"])
    n_bad = len(result["non_compliant"])
    total = n_ok + n_bad
    if n_bad:
        details_lines = [
            f"NON-COMPLIANT — {n_bad} file(s) missing LTG_TOOL_ prefix:"
        ]
        for f in result["non_compliant"]:
            details_lines.append(f"  WARN  {f}")
        details_lines.append(f"\nCompliant: {n_ok} file(s)")
        details = "\n".join(details_lines)
        return "WARN", f"{n_bad} non-compliant out of {total} .py files", details
    else:
        return "PASS", f"All {total} .py files follow LTG_TOOL_ naming convention", ""


# ── Check 14: char_modular_lint — inline character drawing in scene generators ─

def check_char_modular(tools_dir=None):
    """
    Detect inline character drawing in scene generators.
    Scene generators should import from char_*.py modules, not draw
    characters inline.

    Returns
    -------
    dict  {"status": str, "files_scanned": int, "files_with_issues": int,
           "total_issues": int, "issues": list[dict]}
    """
    import glob as _glob
    td = _tools_dir_or_default(tools_dir)
    try:
        from LTG_TOOL_char_interface import check_inline_char_drawing
    except ImportError:
        return {
            "status": "ERROR",
            "files_scanned": 0,
            "files_with_issues": 0,
            "total_issues": 0,
            "issues": [],
            "error": "LTG_TOOL_char_interface.py not found",
        }

    pattern = os.path.join(td, "*.py")
    files_scanned = 0
    all_issues = []

    for fpath in sorted(_glob.glob(pattern)):
        files_scanned += 1
        issues = check_inline_char_drawing(fpath)
        if issues:
            all_issues.append({
                "file": os.path.basename(fpath),
                "issues": issues,
            })

    total_issues = sum(len(f["issues"]) for f in all_issues)
    # WARN (not FAIL) because this is a tracking metric — migration is incremental
    status = "WARN" if all_issues else "PASS"
    return {
        "status": status,
        "files_scanned": files_scanned,
        "files_with_issues": len(all_issues),
        "total_issues": total_issues,
        "issues": all_issues,
    }


def _run_char_modular_lint(tools_dir):
    """Run character modular compliance lint. Returns (status, summary, details)."""
    result = check_char_modular(tools_dir)
    if result.get("error"):
        return "ERROR", result["error"], ""
    n_files = result["files_with_issues"]
    n_issues = result["total_issues"]
    scanned = result["files_scanned"]
    if n_issues:
        details_lines = [
            f"INLINE CHARACTER DRAWING — {n_issues} function(s) in {n_files} scene generator(s):"
        ]
        for entry in result["issues"]:
            details_lines.append(f"\n  {entry['file']}:")
            for iss in entry["issues"]:
                details_lines.append(f"    L{iss['line']:4d}  [{iss['severity']}]  {iss['text'][:100]}")
        details = "\n".join(details_lines)
        return "WARN", f"{n_issues} inline char draws in {n_files}/{scanned} scene generators", details
    else:
        return "PASS", f"No inline character drawing in {scanned} scene generators", ""


# ── Suite runner ──────────────────────────────────────────────────────────────

_CHECKS = [
    ("stub_linter",          _run_stub_linter,          "Stub Integrity Linter"),
    ("draw_order_lint",      _run_draw_order_lint,      "Draw Order Linter"),
    ("glitch_spec_lint",     _run_glitch_spec_lint,     "Glitch Spec Linter"),
    ("spec_sync_ci",         _run_spec_sync_ci,         "Spec Sync CI Gate"),
    ("char_spec_lint",       _run_char_spec_lint,       "Char Spec Linter"),
    ("dual_output_check",    _run_dual_output_check,    "Dual-Output File Check"),
    ("hardcoded_path_check", _run_hardcoded_path_check, "Hardcoded Path Check"),
    ("thumbnail_lint",       _run_thumbnail_lint,       "Thumbnail Lint"),
    ("motion_sheet_coverage",_run_motion_coverage,      "Motion Sheet Coverage"),
    ("doc_staleness",         _run_doc_staleness,         "Doc Staleness Check"),
    ("dep_availability",      _run_dep_availability,      "Dependency Availability"),
    ("bezier_migration_lint", _run_bezier_migration_lint, "Bezier Migration Lint"),
    ("tool_naming_lint",      _run_tool_naming_lint,      "Tool Naming Convention"),
    ("char_modular_lint",     _run_char_modular_lint,     "Char Modular Compliance"),
]


def run_suite(tools_dir=None, fail_on="FAIL", known_issues=None,
              warn_stale=None, current_cycle=None,
              known_issues_raw=None):
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
    warn_stale : int | None
        When set to N, emit a STALE_KNOWN WARN for any known-issue entry
        whose since_cycle is N or more cycles behind current_cycle.
        Contributes to overall WARN count (not FAIL). Default: None (disabled).
    current_cycle : str | None
        Cycle label for the current run (e.g. "C42"). Required when
        warn_stale is set. Falls back to CYCLE_LABEL env var if None.
    known_issues_raw : list | None
        Raw known-issue list from load_known_issues_raw(). Required for
        stale detection. If None and warn_stale is set, stale check is skipped.

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
          "total_known":    int,
          "stale_known":    list,  # stale entry dicts (empty if warn_stale not set)
          "stale_warn":     bool,  # True if any stale known issues found
        }
    """
    tools_dir = _tools_dir_or_default(tools_dir)
    _add_to_path(tools_dir)

    fail_on = fail_on.upper()
    if fail_on not in ("WARN", "FAIL"):
        fail_on = "FAIL"

    if known_issues is None:
        known_issues = {}

    # Resolve current_cycle from env var fallback
    if current_cycle is None:
        current_cycle = os.environ.get("CYCLE_LABEL", "")

    # Stale known-issue detection
    stale_known = []
    if warn_stale and known_issues_raw is not None:
        stale_known = check_stale_known_issues(known_issues_raw, current_cycle, warn_stale)

    # Resolve checks from registry (config-driven) or fallback to hardcoded
    active_checks, checks_source = _get_checks(tools_dir)

    results = {}
    any_error  = False
    any_fail   = False
    any_warn   = False
    total_known = 0

    for (key, runner, label) in active_checks:
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

    # Stale WARNs contribute to overall WARN (not FAIL)
    stale_warn = len(stale_known) > 0
    if stale_warn:
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
        "stale_known":      stale_known,
        "stale_warn":       stale_warn,
        "checks_source":    checks_source,
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
    checks_source = suite_result.get("checks_source", "hardcoded")
    lines.append(f"Checks    : {checks_source}")
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

    # Stale known-issue section
    stale_known = suite_result.get("stale_known", [])
    if stale_known:
        lines.append("")
        lines.append(f"  ⚠ STALE_KNOWN: {len(stale_known)} suppression(s) are aged and need review")
        lines.append(
            "    These entries have been in ci_known_issues.json for a long time."
        )
        lines.append(
            "    Review each: confirm the underlying issue is still a genuine FP,"
        )
        lines.append(
            "    then either extend the reason note or remove the entry if the issue is fixed."
        )
        for entry in stale_known:
            age = entry.get("age", "?")
            sc = entry.get("since_cycle", "?")
            lines.append(
                f"      [{entry.get('check','?')}] {entry.get('file','?')} "
                f"code={entry.get('code','?')}  since={sc}  age={age} cycle(s)"
            )
            reason = entry.get("reason", "")
            if reason:
                lines.append(f"        reason: {reason[:80]}")

    lines.append("=" * 72)

    if include_details:
        for key, info in suite_result["checks"].items():
            if info["details"]:
                lines.append(f"\n{'─' * 72}")
                lines.append(f"Detail: {info['label']}")
                lines.append("─" * 72)
                lines.append(info["details"])

    return "\n".join(lines)


# ── Auto-seed support ────────────────────────────────────────────────────────

def collect_new_fails(suite_result, tools_dir=None):
    """
    Inspect a suite result and return a list of new FAIL entries suitable for
    seeding into ci_known_issues.json. Only returns entries not already present
    in the known-issues file.

    For checks with structured raw data (hardcoded_path_check, thumbnail_lint,
    dual_output_check), re-runs the raw check function and diffs against the
    existing known-issues file. For other checks (stub_linter, char_spec_lint,
    spec_sync_ci), parses the detail output to extract file/code info.

    Parameters
    ----------
    suite_result : dict
        Result from run_suite().
    tools_dir : str | None
        Path to output/tools/. Defaults to suite_result["tools_dir"].

    Returns
    -------
    list[dict]
        Each entry: {check, file, code, reason_suffix}
        where reason_suffix describes what was detected.
    """
    import re as _re
    tools_dir = tools_dir or suite_result.get("tools_dir", _HERE)
    checks = suite_result.get("checks", {})
    new_entries = []

    # Load existing known files per check for dedup
    _ki_path = os.path.join(tools_dir, "ci_known_issues.json")
    _existing = {}  # {check: set(file)}
    _existing_pairs = {}  # {check: set((file, code))}
    if os.path.exists(_ki_path):
        try:
            with open(_ki_path, "r", encoding="utf-8") as _fh:
                _ki_data = json.load(_fh)
            for _entry in _ki_data.get("known_issues", []):
                ck = _entry.get("check", "")
                fn = _entry.get("file", "")
                cd = _entry.get("code")
                _existing.setdefault(ck, set()).add(fn)
                _existing_pairs.setdefault(ck, set()).add((fn, cd))
        except (OSError, json.JSONDecodeError):
            pass

    # ── hardcoded_path_check: re-run raw check ──
    hpc = checks.get("hardcoded_path_check", {})
    if hpc.get("status") == "FAIL":
        try:
            findings = check_hardcoded_paths(tools_dir)
            if findings:
                known_files = _existing.get("hardcoded_path_check", set())
                by_file = {}
                for f in findings:
                    by_file.setdefault(f["file"], []).append(f)
                for fname in sorted(by_file):
                    if fname not in known_files:
                        hits = by_file[fname]
                        new_entries.append({
                            "check": "hardcoded_path_check",
                            "file": fname,
                            "code": None,
                            "reason_suffix": f"{len(hits)} hardcoded /home/ path(s) — migration backlog",
                        })
        except Exception:
            pass

    # ── thumbnail_lint: re-run raw check ──
    tl = checks.get("thumbnail_lint", {})
    if tl.get("status") == "FAIL":
        try:
            findings = check_thumbnail_lint(tools_dir)
            if findings:
                known_files = _existing.get("thumbnail_lint", set())
                by_file = {}
                for f in findings:
                    by_file.setdefault(f["file"], []).append(f)
                for fname in sorted(by_file):
                    if fname not in known_files:
                        hits = by_file[fname]
                        new_entries.append({
                            "check": "thumbnail_lint",
                            "file": fname,
                            "code": None,
                            "reason_suffix": f"{len(hits)} unwhitelisted .thumbnail() call(s) — migration backlog",
                        })
        except Exception:
            pass

    # ── dual_output_check: re-run raw check ──
    doc = checks.get("dual_output_check", {})
    if doc.get("status") == "FAIL":
        try:
            conflicts = check_dual_output(tools_dir)
            known_gens = _existing.get("dual_output_check", set())
            for outfile, generators in sorted(conflicts.items()):
                for gen in generators:
                    if gen not in known_gens:
                        new_entries.append({
                            "check": "dual_output_check",
                            "file": gen,
                            "code": None,
                            "reason_suffix": f"dual-output conflict on {outfile}",
                        })
        except Exception:
            pass

    # ── stub_linter: parse detail for ERROR lines ──
    sl = checks.get("stub_linter", {})
    if sl.get("status") == "FAIL":
        details = sl.get("details", "")
        known_files = _existing.get("stub_linter", set())
        for m in _re.finditer(r'(LTG_\S+\.py)\s.*?ERROR', details):
            fname = m.group(1)
            if fname not in known_files:
                new_entries.append({
                    "check": "stub_linter",
                    "file": fname,
                    "code": None,
                    "reason_suffix": "broken import detected by stub linter",
                })

    # ── char_spec_lint: parse detail for FAIL lines ──
    csl = checks.get("char_spec_lint", {})
    if csl.get("status") == "FAIL":
        details = csl.get("details", "")
        known_pairs = _existing_pairs.get("char_spec_lint", set())
        for m in _re.finditer(r'\[([LMS]\d{3})\].*?FAIL.*?(LTG_\S+\.py)', details):
            code = m.group(1)
            fname = m.group(2)
            if (fname, code) not in known_pairs:
                new_entries.append({
                    "check": "char_spec_lint",
                    "file": fname,
                    "code": code,
                    "reason_suffix": f"char spec {code} violation",
                })
        # Also try reverse pattern: file then code
        for m in _re.finditer(r'(LTG_\S+\.py).*?\[([LMS]\d{3})\].*?FAIL', details):
            fname = m.group(1)
            code = m.group(2)
            if (fname, code) not in known_pairs:
                new_entries.append({
                    "check": "char_spec_lint",
                    "file": fname,
                    "code": code,
                    "reason_suffix": f"char spec {code} violation",
                })

    # ── spec_sync_ci: parse detail for P1 FAIL chars ──
    ssc = checks.get("spec_sync_ci", {})
    if ssc.get("status") == "FAIL":
        details = ssc.get("details", "")
        known_files = _existing.get("spec_sync_ci", set())
        for m in _re.finditer(r'P1 FAIL.*?(\w+)', details):
            char_name = m.group(1).lower()
            entry_file = f"spec_sync_{char_name}"
            if entry_file not in known_files:
                new_entries.append({
                    "check": "spec_sync_ci",
                    "file": entry_file,
                    "code": "P1",
                    "reason_suffix": f"spec sync P1 failure for {char_name}",
                })

    # Deduplicate (same check+file+code)
    seen = set()
    deduped = []
    for e in new_entries:
        key = (e["check"], e["file"], e["code"])
        if key not in seen:
            seen.add(key)
            deduped.append(e)
    return deduped


def auto_seed_known_issues(new_fails, known_issues_path, cycle_label=None):
    """
    Write new FAIL entries into ci_known_issues.json.

    Parameters
    ----------
    new_fails : list[dict]
        Entries from collect_new_fails(). Each has: check, file, code,
        reason_suffix.
    known_issues_path : str
        Path to the ci_known_issues.json file.
    cycle_label : str | None
        Current cycle label (e.g. "C46"). Used for since_cycle field.

    Returns
    -------
    int  Number of entries written.
    """
    if not new_fails or not known_issues_path:
        return 0

    from datetime import date as _date
    today = _date.today().isoformat()

    # Load existing JSON
    try:
        with open(known_issues_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError):
        data = {"known_issues": []}

    entries = data.get("known_issues", [])

    count = 0
    for fail in new_fails:
        entry = {
            "check": fail["check"],
            "file": fail["file"],
            "code": fail["code"],
            "reason": f"auto-seeded by --auto-seed on {today} — {fail['reason_suffix']}",
            "since_cycle": cycle_label or "",
            "status": "new",
        }
        entries.append(entry)
        count += 1

    data["known_issues"] = entries

    with open(known_issues_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    return count


def format_auto_seed_summary(new_fails):
    """
    Format a human-readable summary of auto-seeded entries.

    Parameters
    ----------
    new_fails : list[dict]
        Entries from collect_new_fails().

    Returns
    -------
    str
    """
    if not new_fails:
        return ""
    lines = []
    lines.append("")
    lines.append("=" * 72)
    lines.append(f"AUTO-SEED SUMMARY: {len(new_fails)} new entry/entries added to ci_known_issues.json")
    lines.append("=" * 72)
    for entry in new_fails:
        code_str = entry["code"] if entry["code"] else "(any)"
        lines.append(f"  + [{entry['check']}] {entry['file']}  code={code_str}")
        lines.append(f"    {entry['reason_suffix']}")
    lines.append("=" * 72)
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
    parser.add_argument(
        "--warn-stale",
        default=None,
        type=int,
        metavar="N",
        help=(
            "Emit a STALE_KNOWN WARN for any known-issue entry whose since_cycle "
            "is N or more cycles behind the current cycle (see --cycle). "
            "Contributes to overall WARN count. Example: --warn-stale 4"
        ),
    )
    parser.add_argument(
        "--cycle",
        default=None,
        metavar="LABEL",
        help=(
            "Current cycle label (e.g. C42). Used with --warn-stale to compute "
            "suppression age. Falls back to CYCLE_LABEL environment variable."
        ),
    )
    parser.add_argument(
        "--auto-seed",
        action="store_true",
        default=False,
        help=(
            "After running the suite, auto-add any new FAIL (not already in "
            "ci_known_issues.json) with status 'new' and the current date. "
            "Prints a summary of seeded entries. Default behavior (no flag) "
            "is unchanged — no auto-seeding."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help=(
            "Use with --auto-seed to preview what would be seeded without "
            "modifying ci_known_issues.json. Prints [DRY RUN] prefixed "
            "summary. Has no effect without --auto-seed."
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

    known_issues_raw = load_known_issues_raw(known_issues_path) if known_issues_path else []

    suite_result = run_suite(
        tools_dir=args.tools_dir,
        fail_on=args.fail_on,
        known_issues=known_issues,
        warn_stale=args.warn_stale,
        current_cycle=args.cycle,
        known_issues_raw=known_issues_raw,
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

    # ── Auto-seed new FAILs ──
    if args.auto_seed:
        resolved_tools_dir = args.tools_dir if args.tools_dir else _HERE
        new_fails = collect_new_fails(suite_result, tools_dir=resolved_tools_dir)
        if new_fails:
            # Resolve cycle label
            cycle = args.cycle or os.environ.get("CYCLE_LABEL", "")
            seed_path = known_issues_path
            if not seed_path:
                seed_path = os.path.join(resolved_tools_dir, "ci_known_issues.json")
            if args.dry_run:
                summary = format_auto_seed_summary(new_fails)
                # Prefix with [DRY RUN] marker
                summary = summary.replace(
                    "AUTO-SEED SUMMARY:",
                    "[DRY RUN] AUTO-SEED SUMMARY (no files modified):",
                )
                print(summary)
                print(f"\n[DRY RUN] {len(new_fails)} entry/entries WOULD be written to {seed_path}")
            else:
                count = auto_seed_known_issues(new_fails, seed_path, cycle_label=cycle)
                summary = format_auto_seed_summary(new_fails)
                print(summary)
                print(f"\n{count} entry/entries written to {seed_path}")
        else:
            dry_label = "[DRY RUN] " if args.dry_run else ""
            print(f"\n{dry_label}--auto-seed: no new FAILs to seed.")

    sys.exit(suite_result["exit_code"])


if __name__ == "__main__":
    main()
