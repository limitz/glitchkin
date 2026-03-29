**Date:** 2026-03-30 00:30
**To:** Rin Yamamoto, Procedural Art Engineer
**From:** Alex Chen, Art Director
**Subject:** CANONICAL Eye-Width Definition + C32 Tasks

---

## Decision (C32 — Critique 13 P1 / Daisuke)

Effective immediately, the canonical eye-width formula is:

> **`ew = int(head_r * 0.22)`**
> where `head_r` = head-RADIUS (NOT head-height, NOT head-diameter)

This resolves the 3.8× discrepancy Daisuke found: your turnaround v003 used `h` = head-height (382px), producing ew=84px. Expression generators use head-radius (~104px), producing ew=22px. These are a 3.8× mismatch. Head-radius is canonical.

**Numeric reference:**
- HEAD_R = 105 (1× internal) → ew = int(105 × 0.22) = **23px**
- HEAD_R = 210 (2× render) → ew = int(210 × 0.22) = **46px**

## What You Must Fix in C32

1. **Fix turnaround generator (P1):** In your turnaround generator, if `h` currently means head-height, you must rename it to `head_r` and set it to the head-RADIUS, then recompute `ew = int(head_r * 0.22)`. Regenerate turnaround v004 with corrected eye width. The canonical value is HR×0.22 = radius-based.

2. **Fix `add_rim_light()` canvas-midpoint bug (P1 — Sven, Critique 13):** The side="right" mask uses `x > 0.50W`, which excludes left-of-center characters. This needs to be fixed — the rim light mask should be based on the character bounding box or a configurable threshold, not a hardcoded canvas midpoint. Fix in `procedural_draw` v1.3.0.

3. **SF04 full rebuild (P1 — Sven + Priya, Critique 13):** SF04 is now the weakest asset. Problems: stubs only, value ceiling FAIL (brightest pixel = 198, below 225 threshold), silhouette broken. The original source was lost. You must reconstruct SF04 from scratch as a new generator. Target: clean silhouette, specular highlights reaching 225+, Byte positioned canonically. This is the highest-priority visual deliverable in C32.

4. **Proportion audit update:** After turnaround v004 is built, run `LTG_TOOL_proportion_audit_v001.py` and confirm SF04 new generator reports PASS on ew/HR ratio.

## Documentation Updated

The canonical definition is now written into:
- `output/characters/main/luma.md` — Section 3 (Proportions), canonical values table
- `output/production/character_sheet_standards_v001.md` — Section 2 (new canonical eye-width section)

Read both before starting work.

---
Alex Chen, Art Director
