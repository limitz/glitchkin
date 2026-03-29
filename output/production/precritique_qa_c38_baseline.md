# Pre-Critique QA Baseline — C38

**Date:** 2026-03-29
**Run by:** Morgan Walsh (Pipeline Automation Specialist)
**Tool:** LTG_TOOL_precritique_qa_v001.py v2.3.0
**Full report:** output/production/precritique_qa_c38.md

---

## Summary

| Metric | C38 | C37 | Delta |
|---|---|---|---|
| PASS | 343 | 333 | +10 |
| WARN | 38 | 26 | +12 |
| FAIL | 0 | 0 | 0 |
| **Overall** | **WARN** | **WARN** | — |

---

## Section Results

| Section | Result | PASS | WARN | FAIL | Notes |
|---|---|---|---|---|---|
| Render QA (pitch PNGs) | WARN | 0 | 6 | 0 | SF01 warm_cool=17.8/20.0 (REAL_INTERIOR threshold fix pending Kai) |
| Color Verify | WARN | 2 | 2 | 0 | SF03 + SF-LumaBytes color fidelity advisory |
| Proportion Verify | WARN | 1 | 3 | 0 | Known false positives on multi-panel turnarounds |
| Stub Linter | PASS | 166 | 0 | 0 | +7 vs C37 (new tools added) |
| Palette Warmth Lint | PASS | 11 | 0 | 0 | All CHAR-M entries clean |
| Glitch Spec Lint | WARN | 3 | 27 | 0 | +1 vs C37; persistent false positives in lineup/legacy files |
| README Script Index Sync | PASS | 160 | 0 | 0 | 2 unlisted tools registered this cycle (color_qa_c37_runner, luma_expression_sheet_v011) |

---

## WARN Detail

### Render QA
- **SF01 warm_cool:** 17.8/20.0 — REAL_INTERIOR threshold should be 12 (Kai fix pending)
- **SF02 warm_cool:** 6.5/20.0 — GLITCH world, threshold=3, expected WARN (cold dominant is correct)
- **SF-LumaByte warm_cool:** 1.1/20.0 — expected advisory
- **Logo warm_cool:** 0.0/20.0 — expected advisory
- **Storyboard warm_cool:** 4.6/20.0 — expected advisory
- **SF03/SF-LumaByte color_fidelity:** advisory WARNs

### Glitch Spec Lint (+1 vs C37)
- 27 WARNs: persistent false positives in lineup_v004–v007 files + legacy test files
- Same pattern as C37 — suppression list expansion still needed (ideabox C37)
- v011 luma expression sheet adds no new Glitch lint WARNs (SKIP)

---

## Actions Required Before C38 Critique

| Priority | Item | Owner | Status |
|---|---|---|---|
| P1 | spec_sync_ci: load suppression list (G002 FAIL in CI) | Kai Nakamura | PENDING |
| P1 | Naming convention violations: LTG_CHAR_*motion* + LTG_SB_* | Kai Nakamura | PENDING |
| P1-adj | REAL_INTERIOR render_qa threshold: 12 (not 20) | Kai Nakamura | PENDING |
| INFO | Glitch spec suppression list expansion for lineup_v004–v007 | Future cycle | BACKLOG |

---

## CI Suite Status (Pre-Kai Fixes)

See: output/production/ci_suite_c38_report.md

- Stub Linter: **PASS** (166)
- Draw Order Linter: WARN (37 advisory)
- Glitch Spec Linter: WARN (27)
- Spec Sync CI Gate: **FAIL** — G002 P1 (suppression list not loaded — Kai fix pending)
- Char Spec Linter: PASS

**Overall: FAIL** (exit 1 at --fail-on FAIL threshold)
**Expected behavior** — CI suite will be re-run after Kai's spec_sync_ci fix.
