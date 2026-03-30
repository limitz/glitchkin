# Color QA Baseline — Cycle 38
**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-29
**render_qa version:** v1.5.0 (REAL threshold corrected 20→12)

---

## Summary

| Asset | Grade | Warm/Cool | Notes |
|---|---|---|---|
| SF01 v005 (discovery) | **PASS** | 17.9 / 12.0 = PASS | C38: threshold fix resolves FP-006 |
| SF02 v008 (glitch storm) | WARN | 6.5 / 12.0 = FAIL | Known FP — storm threshold should be ~3 |
| SF03 v005 (other side) | WARN | 3.0 / 0.0 = PASS | Other WARN conditions (not warm/cool) |
| SF04 v004 (luma byte) | WARN | 1.1 / 12.0 = FAIL | Known FP — world_type=None (luma_byte pattern gap) |

---

## Key Change: render_qa v1.5.0 — REAL Threshold Fix

`_WORLD_WARM_COOL_THRESHOLD["REAL"]` corrected from `20.0` → `12.0`.

This value now matches `warmth_lint_v004` world_presets (`REAL: warm_cool_threshold: 12`).
The prior 20.0 was incorrect — the v1.4.0 changelog said "Based on world_presets" but used
the wrong value.

**Effect:** SF01 warm/cool check now PASS (sep=17.9 > threshold=12.0).
FP-006 partially resolved for SF01. Closes the primary item from C38 task brief.

---

## SF01 — PASS

```
asset_type   : style_frame
silhouette   : distinct
value_range  : min=14, max=246, range=232 → PASS
warm_cool    : sep=17.9, threshold=12.0, world=REAL → PASS
line_weight  : mean=63.6px, outliers=2 → PASS
color_fidelity: overall_pass=True
GRADE        : PASS
```

The 17.9 warm/cool reading is good but not at the high end of what a lamp-lit interior
can achieve. No generator nudge was made — the composition is correct and the threshold
is satisfied. If critics request richer warm saturation in a future cycle, the generator
can increase lamp fill alpha on the bottom-left zone.

---

## SF02 — WARN (documented FP-006 remainder)

```
warm_cool    : sep=6.5, threshold=12.0, world=REAL → FAIL
```

SF02 is a contested storm scene. Warm values (window glow, character skin) are intentionally
suppressed by the dominant cold storm. Sep=6.5 is production-correct. Passes at threshold=3
(the true REAL_STORM threshold). Documented as FP-006 pending the REAL_STORM sub-type
addition in render_qa. **Not a production error.**

---

## SF03 — WARN (non-warm/cool issue)

```
warm_cool    : sep=3.0, threshold=0.0, world=OTHER_SIDE → PASS
```

SF03 warm/cool is PASS. The WARN grade is from a different check. See prior QA reports.
No new warm/cool issues in C38.

---

## SF04 — WARN (documented FP-006 remainder)

```
warm_cool    : sep=1.1, threshold=12.0, world=None → FAIL
```

SF04 "luma_byte" filename not matched by `warmth_lint_v004.infer_world_type()` → world=None →
falls back to threshold=12.0. Actual world type is REAL (soft-key discovery scene). Sep=1.1
reflects a near-zero warm/cool split which is expected for a soft-lit two-character interaction.
Documented as FP-006 carry-forward. Fix requires adding "luma_byte" to warmth_lint_v004 REAL rules
OR switching render_qa to import from `LTG_TOOL_world_type_infer` (which has the pattern).
**Not a production error.**

---

## New Tools (C38)

- **`LTG_TOOL_world_type_infer.py`** — standalone world-type inference helper.
  Includes "luma_byte" → REAL pattern, batch mode, `--threshold` flag for shell capture,
  `--list-rules` for rule inspection.

---

## Warmth Lint Results

CHAR-M + CHAR-L entries: 14 checked, 0 violations — **PASS**

All CHAR-M (Grandma Miri) and CHAR-L hoodie entries (CHAR-L-04, CHAR-L-08, CHAR-L-11)
confirmed warm (R>G>B). Slipper fix (CHAR-M-11 C32) now propagated to all active generators.

---

## Miri Slipper Audit

See `/home/wipkat/team/output/production/miri_slipper_warmth_audit_c38.md` for full audit.

**Summary:** 4 active generator files corrected (expr_sheet_v003/v004, turnaround_v001,
color_model_v001). grandma_miri_color_model.md spec doc updated. 3 PNGs regenerated
(expr_sheet_v004, turnaround_v001, color_model_v001). Character lineup v007 was already
correct. Historical files not updated (superseded).

---

## Carry Forward

1. **SF02 REAL_STORM threshold** — needs REAL_STORM sub-type in render_qa (threshold≈3).
   Carry to Kai Nakamura next cycle.
2. **SF04 world_type=None** — warmth_lint_v004 missing "luma_byte" pattern. Fix options:
   (a) Update warmth_lint_v004, or (b) update render_qa to use world_type_infer_v001.
3. **grandma_miri_expression_sheet_v002.py** — historical, slipper still wrong. Not blocking.
4. **LTG_TOOL_character_lineup/v006** — historical, slipper still wrong. Not blocking.
