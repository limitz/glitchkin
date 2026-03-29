**Author:** Rin Yamamoto
**Cycle:** 37
**Date:** 2026-03-30
**Idea:** The proportion_audit_v002 tool has its report output path hardcoded to `proportion_audit_c36.md`. Every cycle a new runner wrapper (like `LTG_TOOL_proportion_audit_c37_runner.py`) is needed to produce the correctly-labelled report. This is wasteful and error-prone. The fix: add a `--cycle N` CLI flag to `LTG_TOOL_proportion_audit_v002.py` (or a future v003) so the report heading and output path update automatically to `proportion_audit_c{N}.md`. A default of `--cycle current` could infer the cycle number from the most recent statement of work or a config file.
**Benefits:** Eliminates the need for per-cycle runner wrapper scripts. Any team member can run `python3 LTG_TOOL_proportion_audit_v002.py --cycle 38` and get a correctly-titled C38 report without any additional code. Reduces file clutter in output/tools/ and keeps audit tooling maintainable long-term.
