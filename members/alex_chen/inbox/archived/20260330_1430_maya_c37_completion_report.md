**Date:** 2026-03-30 14:30
**From:** Maya Santos, Character Designer
**To:** Alex Chen, Art Director
**Subject:** C37 Completion Report — Cosmo v006 + Silhouette --output-zones + Luma v010

Hi Alex,

All three C37 tasks complete. Full pre-critique checklist run.

---

## 1. Cosmo v006 — S003 Glasses Tilt Fix (P1 RESOLVED)

**Generator:** `output/tools/LTG_TOOL_cosmo_expression_sheet_v006.py`
**Output:** `output/characters/main/LTG_CHAR_cosmo_expression_sheet_v006.png` (1182×1114px)

**Fix applied:** v005 had glasses_tilt=10° on 3 expressions — all now corrected:
- AWKWARD: 10° → 7° (spec target)
- SURPRISED: 10° → 7° (spec target)
- FRUSTRATED/DEFEATED: 10° → 7° (spec target)
- SKEPTICAL: 9° (retained — at tolerance ceiling, within ±2°)
- DETERMINED: 7° (already compliant)
- WORRIED: 8° (already compliant)

**spec_sync_ci result:** `CI PASS — 0 P1 violations`
- S003 PASS confirmed on v006
- One S002 advisory WARN (eye-width coefficient — not P1, pre-existing)

**Silhouette test (RPD v3, --mode full):**
- Worst pair: AWKWARD↔SKEPTICAL — RPD 75.4% (WARN)
- OVERALL: WARN (no FAILs)
- No silhouette regression from v005

---

## 2. Silhouette Tool -- output-zones Flag (Actioned Ideabox C36)

**Tool modified in-place:** `output/tools/LTG_TOOL_expression_silhouette_v003.py`

`--output-zones` flag added. When used with `--output` and `--mode full`:
- Draws colored left-edge zone bars on each panel in the contact sheet
- HEAD zone = blue bar, ARMS zone = orange bar, LEGS zone = green bar
- Bars are positioned at the actual bounding-box-derived zone boundaries
- Does not alter scoring logic, JSON output, or exit codes

Usage:
```
python3 LTG_TOOL_expression_silhouette_v003.py sheet.png --mode full --output sil.png --output-zones
```

All existing behavior preserved.

---

## 3. Luma v010 — THE NOTICING Rework

**Generator:** `output/tools/LTG_TOOL_luma_expression_sheet_v010.py`
**Output:** `output/characters/main/LTG_CHAR_luma_expressions_v010.png` (1200×900px)

THE NOTICING was scoring 52-58/100 with critics despite correct pose geometry (chin-touch, asymmetric eyes, wide stance). Diagnosed 7 issues — all addressed in v010:

| Issue | v009 | v010 Fix |
|---|---|---|
| Eye asymmetry too subtle at panel scale | r_open=0.85 (15% diff) | r_open=0.65 (35% diff) — survives LANCZOS |
| Left brow lift not readable | brow_l_dy=-HR*0.14 | brow_l_dy=-HR*0.22 (dramatically higher) |
| Gaze reads "wandering" not "tracking" | gaze_dy=0.15 (down) | gaze_dy=0.0 (pure lateral) |
| Hand gesture too casual | chin-touch ellipse | finger-to-lower-lip (vertical forearm diagonal) |
| Panel BG too pale/passive | (218,226,235) | (195,210,228) — deeper blue-grey |
| Hoodie blends into BG | (130,148,172) | (105,128,162) — richer slate |
| Corner position = scan-and-dismiss | Slot 0 (top-left) | Slot 4 (CENTER) — eye returns here |

Additionally: subtle blush=30 added (recognition has warmth), tiny body_tilt +HR*0.03 lean.
All other 6 expressions unchanged from v009.

**Pre-critique checklist:**
1. RPD silhouette (--mode full): FAIL — worst pair WORRIED↔FRUSTRATED 97.9%. KNOWN tool limitation at panel resolution for standing human chars (documented C33–C36, unchanged from v009 baseline). Not a design defect.
2. RPD arms mode (--center-mask 0.36): FAIL — same known limitation.
3. Pose vocabulary diversity: THE NOTICING (one arm diagonal/vertical) is distinct from all 6 others. No two expressions share primary arm pose.
4. Line weight 3-tier: confirmed (silhouette 3-4px, interior 2px, detail 1px).
5. Eye-width: ew = int(HEAD_HEIGHT_2X × 0.22) = 45px at 2x — canonical.
6. Labels: ALL CAPS, correct.
7. Canvas: 1200×900 ≤ 1280px. Compliant.

---

## Summary

| Deliverable | Status |
|---|---|
| Cosmo v006 generator | COMPLETE |
| Cosmo v006 PNG | COMPLETE — 1182×1114px |
| spec_sync_ci cosmo | CI PASS, 0 P1 violations |
| Silhouette --output-zones | COMPLETE — in-place on v003 |
| Luma v010 generator | COMPLETE |
| Luma v010 PNG | COMPLETE — 1200×900px |
| Ideabox C37 | SUBMITTED |

Maya Santos
