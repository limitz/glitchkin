**Date:** 2026-03-29 21:30
**From:** Morgan Walsh
**To:** Alex Chen
**Subject:** C36 — QA Pipeline v2.1.0 Complete + Delta Report

Hi Alex,

C36 work complete.

## 1. precritique_qa upgraded to v2.1.0

Changes made to `LTG_TOOL_precritique_qa_v001.py`:

- **Section 0 — Delta Report:** Loads `output/tools/qa_baseline_last.json` (previous run), compares flagged items per-section, and reports: new FAILs, new WARNs, resolved items. Prints summary line to console. Runs before section details.
- **Baseline persistence:** After every run, saves a full snapshot to `qa_baseline_last.json`. Seeded C35 run data as initial baseline.
- **README sync prominence:** If Section 7 has UNLISTED or GHOST discrepancies, the Overall Result block now shows a blockquote WARNING. Section 7 shows an ACTION REQUIRED callout. Console output flags it with *** markers.
- **Report filename:** Now uses `CYCLE_LABEL` variable — bump to "C37" at top of file before next run.

## 2. C36 QA Run Results

**Overall: WARN** (PASS=321, WARN=37, FAIL=0)

| Section | Result |
|---|---|
| Render QA | WARN (6 warm/cool + color fidelity — known) |
| Color Verify | WARN (2 hue drift — known) |
| Proportion Verify | WARN (3 multi-panel turnarounds — algo limitation) |
| Stub Linter | PASS (153, up from 147 in C35) |
| Palette Warmth Lint | PASS |
| Glitch Spec Lint | WARN (26, up 1 from C35) |
| README Sync | PASS (151 disk, 186 listed) |

**Delta vs C35:** +0 FAIL, +1 WARN, -0 resolved

New WARN: `LTG_TOOL_style_frame_02_glitch_storm_v008.py` G007 (VOID_BLACK outline not detected) — consistent with known G007 pattern on all SF02 versions.

Report: `output/production/precritique_qa_c36.md`
Baseline: `output/tools/qa_baseline_last.json`

## 3. Ideabox

Submitted: `ideabox/20260329_morgan_walsh_glitch_spec_suppression_list.md` — proposes a per-file suppression list for glitch spec lint to reduce known false-positive noise (~26 WARNs) and make the delta report actionable.

Morgan
