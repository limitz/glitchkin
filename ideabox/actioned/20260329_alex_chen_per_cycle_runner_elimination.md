**Date:** 2026-03-29
**From:** Alex Chen, Art Director
**Idea type:** Pipeline improvement / Tool maintenance

## Per-Cycle Runner Script Elimination

**Problem:**
Every time we run a batch QA pass, we create a new per-cycle runner script (e.g. `LTG_TOOL_color_qa_c37_runner.py`, `LTG_TOOL_proportion_audit_c37_runner.py`). These accumulate with each cycle, reference superseded asset paths, and inflate the tools directory.

**Proposed fix:**
Convert batch QA tools to accept a `--target-list qa_targets_current.json` parameter. One JSON config file (overwritten each cycle by whoever sets up the QA run) replaces per-cycle runners entirely. Old QA results stay in production reports — no history is lost. We just stop generating new Python files for what is essentially a config change.

**Effort:** 2–3 hours of Kai Nakamura time to retrofit the proportion_audit and color_qa tools. Savings: every future cycle that currently creates a runner script.

**Secondary benefit:** The JSON target list could be committed to git, giving us a lightweight record of which assets were in scope for each QA run (by looking at git history) without polluting the tools directory.

**For:** Kai Nakamura (Technical Art Engineer)
