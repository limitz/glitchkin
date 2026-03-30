**Author:** Morgan Walsh
**Cycle:** 40
**Date:** 2026-03-30
**Idea:** Add a `cycle_added` field to each entry in `ci_known_issues.json`, and add a `--warn-stale N` flag to `LTG_TOOL_ci_suite.py` that emits a separate STALE warning if a known issue has been in the file for more than N cycles without being fixed. This prevents the file from becoming a permanent graveyard — items added in C39 that are still present in C41/C42 get flagged as stale, prompting either a fix or an explicit decision to keep them.
**Benefits:** Keeps the known-issues list honest. Right now the file could silently accumulate entries that nobody ever fixes. The stale mechanism gives the producer and art director visibility into which technical debt items are aging. Low cost to implement (just compare cycle_added against current CYCLE_LABEL at report time). Helps Kai track which W004/G00x FPs are genuinely pre-existing vs which ones slipped in unnoticed during a cycle.
