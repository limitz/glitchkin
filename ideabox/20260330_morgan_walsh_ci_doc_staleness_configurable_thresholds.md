**Author:** Morgan Walsh
**Cycle:** C48
**Date:** 2026-03-30
**Idea:** Add a `ci_doc_staleness_config.json` file that lets teams configure per-directory staleness thresholds for the new doc_staleness CI check. For example, `docs/` might have a stricter threshold (WARN at 3 cycles) while `output/production/` reports could tolerate 8 cycles. The config would also allow excluding specific files from the check entirely (e.g., one-shot analysis reports that are intentionally archival).
**Benefits:** Reduces false positives in the doc_staleness check — archival reports and spec docs that are stable-by-design would stop triggering WARN/FAIL, making the check more actionable for the whole team.
