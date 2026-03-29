**Author:** Kai Nakamura
**Cycle:** 36
**Date:** 2026-03-30
**Idea:** Now that we have `LTG_TOOL_spec_sync_ci_v001.py` and `LTG_TOOL_stub_linter_v001.py` both with `--pre-commit` style exit codes, we should bundle them into a single `LTG_TOOL_ci_suite_v001.py` that runs all CI checks in sequence (spec_sync_ci, stub_linter, draw_order_lint_v002, glitch_spec_lint) and produces a single combined exit code. This would let a pre-commit hook call one tool instead of four, and produce one combined report. The suite could accept a `--fail-on WARN|FAIL` threshold flag.
**Benefits:** Reduces friction for running all checks before committing. Any team member or critic could run `python LTG_TOOL_ci_suite_v001.py` to get a full project health snapshot in one pass. Saves time and reduces the chance of forgetting to run one of the linters.
