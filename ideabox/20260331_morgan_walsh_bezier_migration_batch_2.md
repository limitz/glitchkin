**Author:** Morgan Walsh
**Date:** 2026-03-31
**Cycle:** C52

## Idea: Complete Bezier Migration — Remaining 4 Files

**Problem:** 4 files still have fully hand-rolled bezier functions (not yet delegating to curve_utils): luma_construction_prototype, luma_gesture_prototype, sb_cold_open_P17_chartest, grandma_miri_expression_sheet. The new bezier_migration_lint CI check (Check 12) will flag these as WARN each run until migrated.

**Proposal:** Migrate the remaining 4 files in a single batch next cycle. The pattern is established from C52 batch 1 (4 files migrated). Each migration is mechanical: import from curve_utils, replace local def with thin delegate wrapper.

**Benefit:** Clears the bezier_migration_lint WARN, completes the consolidation effort. All bezier math flows through the optimized bezier library (vectorized evaluate_multi) instead of per-step Python loops. Future curve changes only need one file edit.
