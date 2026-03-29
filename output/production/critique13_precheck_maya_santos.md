# Critique 13 Pre-Check — Character Asset Audit
**Author:** Maya Santos, Character Designer
**Date:** 2026-03-29 (Cycle 30)
**Purpose:** Identify remaining inconsistencies across character sheets before Critique 13 review.

---

## 1. Luma Color Model — FIXED (v002 generated)

**Issue (v001):** Silhouette eye proportions used eye_r_x=14 (~head_r×0.30). Canonical spec from expression sheet v007 and turnaround v003 is ew = HR×0.22.

**Fix:** `LTG_TOOL_luma_color_model_v002.py` generated. Eye width corrected to `int(head_r * 0.22)` = ~10px. Cheek nubs added to head (classroom-style). Head label updated to "3.2 heads". Output: `LTG_COLOR_luma_color_model_v002.png`.

**Status:** RESOLVED — v002 is the new canonical color model for Luma.

---

## 2. Expression Sheet Line Weights — Status by Character

| Character | Sheet | Head outline at 2× | Structure at 2× | Canonical? | Notes |
|---|---|---|---|---|---|
| Luma | v007 | width=4 | width=3 | YES | Canonical standard met |
| Glitch | v003 | N/A (pixel body) | varies | N/A | Non-human: no head-outline equivalent |
| Cosmo | v004 | width=2 (1× native) | width=2 | CLOSE | No 2× render — 1× widths are in standard range |
| Byte | v004 | width=3 (body oval) | width=2–3 | PARTIAL | Right organic eye eyelid arcs: width=5/6/8 at 1× native — exceeds standard for droopy/resigned/storm states |
| Miri | v003 | width=6 at 2× (~3px actual) | width=4 at 2× (~2px actual) | NO | Silhouette 50% heavier than canonical. Grandfathered (pre-dates standards doc). **Will likely be flagged by Critique 13.** |

---

## 3. Luma Expression Sheet v007 + Lineup v006 — Proportion Fix

Both assets were completed in C29 with the correct 3.2-head proportion and ew=HR×0.22 eyes. These are consistent with each other and the turnaround v003.

**Status:** RESOLVED — no remaining proportion inconsistency on the Luma main assets.

---

## 4. Cosmo Tool Version Chain — Known Issue (not fixed)

`LTG_TOOL_cosmo_expression_sheet_v004.py` is byte-identical to v003 and outputs `LTG_CHAR_cosmo_expression_sheet_v003.png`. The v004 PNG file exists independently.

**Status:** KNOWN DEFECT — not fixed in C30 (requires rebuild to resolve properly). Documented in character_sheet_standards_v001.md inconsistency log.

---

## 5. Miri v003 Stub — Broken Generator

`LTG_TOOL_grandma_miri_expression_sheet_v003.py` is a stub that imports from `LTG_CHAR_grandma_miri_expression_sheet_v003` which no longer exists. The PNG `LTG_CHAR_grandma_miri_expression_sheet_v003.png` was generated before the rename and exists correctly.

The v003 generator needs to be rebuilt as a self-contained file. The PNG output is visually correct (C25 KNOWING STILLNESS 6th panel). This is a generator maintenance issue, not a visual quality issue.

**Status:** KNOWN DEFECT — stub generator broken. PNG is correct. Not fixed in C30. Recommend rebuild in C31 if Miri is scheduled for review.

---

## 6. Character Sheet Standards Doc — UPDATED

`output/production/character_sheet_standards_v001.md` Section 7 updated to reflect actual current sheet versions:
- Luma: v007 (was v003)
- Cosmo: v004 (was v003)
- Byte: v004 (was v003)
- Miri: v003 (was v002)
- Glitch: v003 (new — was not in table)

Known inconsistencies logged in doc under Section 7 footnote.

---

## Summary for Critique 13

**Things critics are likely to flag:**
1. Miri silhouette line weight (6px at 2× = ~3px actual) vs canonical 2px — may look noticeably heavier than Luma/Cosmo.
2. Byte's droopy/resigned/storm eye arc weights (5–8px at 1× native) — aesthetically justified but technically non-standard.

**Things that are now solid:**
- Luma proportion chain (expr v007, lineup v006, turnaround v003) is fully consistent at 3.2 heads + ew=HR×0.22.
- Luma color model v002 now matches v007 face proportions.
- Character sheet standards doc reflects actual current versions.
- All main assets within ≤1280px image size rule.

---

*Maya Santos — Character Designer — Cycle 30*
