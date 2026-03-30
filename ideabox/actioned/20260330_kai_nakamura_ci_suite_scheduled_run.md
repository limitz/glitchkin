**Author:** Kai Nakamura
**Cycle:** 37
**Date:** 2026-03-30
**Idea:** Now that `LTG_TOOL_ci_suite.py` exists, the producer could schedule it to run automatically before every git commit using a pre-commit hook (shell script: `python output/tools/LTG_TOOL_ci_suite.py --fail-on FAIL --no-details`). This would catch P1 violations — broken imports, spec FAILs — before they land in history, with zero overhead per developer. The hook only needs 5–10 lines of shell. Store it in `output/tools/install_ci_hook.sh` so any team member can install it with one command.
**Benefits:** Prevents P1 spec regressions from being committed. Particularly valuable now that we have 5+ character specs and complex draw-order rules. Currently the suite is only run manually; automating via pre-commit means it always runs without anyone remembering. Low cost to implement; high value for pipeline integrity.
