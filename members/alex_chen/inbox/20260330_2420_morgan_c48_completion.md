**Date:** 2026-03-30
**From:** Morgan Walsh
**Subject:** C48 Completion — ci_suite v1.8.0

Alex,

C48 tasks complete. Summary:

## Task 1: REMOVED Check 10 ext_model_check
- `check_ext_models()`, `_run_ext_model_check()`, and `_EXT_MODEL_PATTERNS` fully removed from `LTG_TOOL_ci_suite.py`
- ext_model_check section removed from `collect_new_fails()` auto-seed logic
- No stubs left — clean removal as requested
- No entries existed in `ci_known_issues.json` for ext_model_check, so no JSON cleanup needed
- Kai's standalone `LTG_TOOL_pretrained_model_detect.py` is unaffected (separate tool, not in CI gate)

## Task 2: NEW Check 10 doc_staleness
- Reuses Check 10 slot (total check count stays at 10)
- Delegates to `LTG_TOOL_doc_governance_audit.audit_docs()` for scanning
- Thresholds: WARN at 5+ cycles stale, FAIL at 10+ cycles stale
- Reads `CYCLE_LABEL` env var (same as `--cycle` flag) for current cycle
- `check_doc_staleness(current_cycle, warn_age, fail_age)` exported for programmatic use
- Files with no cycle reference are reported as INFO (not scored)

## Version
- ci_suite bumped to v1.8.0
- doc_governance_audit default cycle updated to 48
- README updated (header + C48 Updates section + changelog)

## Note
Could not run the suite to get a live baseline — Bash execution was restricted during this session. Syntax check passed. The new check should produce WARN/FAIL on first run given the 43 STALE + 58 NO_REF docs from the C47 audit.

Ideabox: per-directory configurable staleness thresholds submitted.
