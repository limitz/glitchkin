# Idea: Expression RPD Snapshot Report — Baseline Delta Tracking

**Submitted by:** Maya Santos
**Cycle:** 41
**Category:** Tool / QA

## Problem

Each time an expression sheet is updated (Luma v011→v012→v013, Byte v006→v007), we run the RPD silhouette tool and check results manually. There's no persistent record of what changed between versions — only the current run's WARN/FAIL table. This means:

1. A regression (expression pair silhouette going from PASS to WARN) may not be noticed unless someone cross-references old notes.
2. "Expected FAIL" vs "new FAIL" is tracked in human memory (MEMORY.md) rather than in a machine-readable diff.
3. When multiple designers work on the same sheet across cycles, there's no audit trail of silhouette health over time.

## Proposed Fix

Add a `--snapshot PATH` flag to `LTG_TOOL_silhouette_rpd.py`. When specified:

1. After running RPD checks, write the full result dict (all pair scores + PASS/WARN/FAIL labels) to a JSON snapshot file at PATH.
2. If PATH already exists (previous snapshot), produce a diff report: pairs that changed grade (PASS→WARN, WARN→FAIL, FAIL→PASS, etc.), newly added pairs, removed pairs.
3. Print the diff summary to stdout alongside the regular report.
4. In the viz output (when `--viz-rpd` is used), mark pairs that REGRESSED in a different color (e.g. amber instead of yellow for WARN regressions vs stable WARNs).

## Usage

```bash
# First run — creates baseline
python LTG_TOOL_silhouette_rpd.py output/characters/main/LTG_CHAR_luma_expression_sheet.png \
  --rows 3 --cols 3 --snapshot output/production/luma_rpd_snapshot.json

# Subsequent run — diffs against baseline, prints regressions
python LTG_TOOL_silhouette_rpd.py output/characters/main/LTG_CHAR_luma_expression_sheet.png \
  --rows 3 --cols 3 --snapshot output/production/luma_rpd_snapshot.json
```

## Priority

Medium. Not blocking, but would have caught the WORRIED↔FRUSTRATED FAIL becoming load-bearing context across 3 cycles sooner.
