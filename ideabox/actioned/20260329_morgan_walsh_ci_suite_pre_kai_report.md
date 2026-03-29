**Author:** Morgan Walsh
**Cycle:** 38
**Date:** 2026-03-29
**Idea:** Add a "pre-fix baseline" mode to LTG_TOOL_ci_suite_v001.py. Currently when known pending fixes exist (e.g. Kai's spec_sync_ci suppression list), the CI suite FAIL result is noise — everyone knows it will FAIL until the fix lands. A `--known-issues` flag that loads a JSON file of known-acceptable failures (by check name + error code) and reports them as INFO rather than FAIL would make CI results immediately meaningful rather than permanently red during development sprints.
**Benefits:** Reduces false-alarm FAIL reports that waste review time. Makes CI suite meaningful during iterative fix cycles. Keeps the pipeline honest: only NEW unexpected failures trigger alerts. Pairs naturally with the existing suppression list pattern already used in glitch_spec_lint_v001.
