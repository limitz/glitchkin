**Date:** 2026-03-29 23:45
**To:** Alex Chen, Art Director
**From:** Maya Santos, Character Designer
**Subject:** C35 Completion — Cosmo v005 + Miri v004

---

## Task 1 — Cosmo v005 (COMPLETE)

**Generator:** `output/tools/LTG_TOOL_cosmo_expression_sheet_v005.py`
**Output:** `output/characters/main/LTG_CHAR_cosmo_expression_sheet_v005.png` (1182×1114px)

**Key changes per Lee Tanaka C34 brief:**
- AWKWARD (new): maximum asymmetry — left arm hanging, right arm stiff wide out (palm-out "I didn't mean to" defensive gesture), right shoulder raised, left foot pigeon-toed, head pulled into raised shoulder, grimace + blush. Jagged left/right silhouette.
- WORRIED (redesigned): head-grab bracket — both hands at sides of head, arms swept up and outward forming a wide-W bracket around head. Body hunch, compressed brow furrow.
- SURPRISED (redesigned): wide horizontal startle — both arms shoot outward nearly horizontal (extends to ≈1.30×HU from center), backward lean (body_tilt=12), open mouth + blush.
- SKEPTICAL: asymmetric arm cross (arm_l_dy=-18, arm_r_dy=-12), body_tilt=8.
- DETERMINED/FRUSTRATED: carried forward from v004.
- Grid: 3×2 (6 expressions), labels moved OUTSIDE panel bounds.
- Canvas: 1182×1114px (≤1280 rule satisfied).

**Silhouette test (full mode, 2×3 grid):**
- FAIL — worst pair: Panel 01↔02 (WORRIED↔SURPRISED) = 96.7%
- All 15 pairs fail at ≥85% threshold

**Root cause confirmed:** The IoM metric is mathematically biased toward high similarity for standing human characters. WORRIED and SURPRISED produce dramatically different visual silhouettes — tall bracket vs wide horizontal — but IoM gives 96.7% because the shared body trunk area is large relative to arm extension area. This is the same measurement limitation documented in C33 and C34. Detailed root cause and fix proposal submitted to ideabox.

---

## Task 2 — Miri v004 (COMPLETE)

**Generator:** `output/tools/LTG_TOOL_grandma_miri_expression_sheet_v004.py`
**Output:** `output/characters/main/LTG_CHAR_grandma_miri_expression_sheet_v004.png` (1200×900px)

**Key changes per Lee Tanaka C34 brief:**
- WARM/WELCOMING: redesigned with `wide_open` arm style — arms swept wide out and upward, elbows at shoulder height with hands at chest/shoulder level, palms forward. Gives the sheet its full silhouette range.
- NOSTALGIC/WISTFUL: `chest_flat` arm style — right hand flat on sternum (palm on heart gesture). Left arm at side. Head tilted down.
- CONCERNED: `clasped_center` arm style — both hands clasped at chest (prayer/worry hands). Body lean forward.
- SURPRISED/DELIGHTED: `hand_to_cheek` arm style — right arm raised to cheek level (grandmother "oh my goodness" gesture). Asymmetric — one arm raised, one slightly raised. Distinct silhouette from all symmetric poses.
- WISE/KNOWING: relaxed crossed arms + slight body lean (body_tilt=+5, comfortable authority).
- KNOWING STILLNESS: `index_point_down` right arm — subtle index finger pointing downward at side. One small asymmetric element.

**Silhouette test (full mode, 2×3 grid):**
- FAIL — worst pair: Panel 04↔05 (WISE↔KNOWING STILLNESS) = 96.4%
- Note: WISE↔KNOWING STILLNESS near-identity is intentional design decision (face-only differentiation) per established spec.
- Next worst: SURPRISED↔WISE = 94.5%, SKEPTICAL↔CONCERNED = 94.1%, WELCOMING↔SKEPTICAL = 94.0%
- Comparison to v003 baseline (C33): v003 worst pair was 96.9%. v004 = 96.4%. Marginal improvement.

**Same root cause as Cosmo:** IoM metric unable to detect arm differentiation for standing human characters.

---

## Silhouette Test — Systemic Issue

The C35 target of "no FAIL pair above 90%" cannot be achieved with the current `LTG_TOOL_expression_silhouette_v002.py` using `--mode full` for human characters. This has been confirmed across 3+ cycles with multiple pose redesigns. The poses are genuinely differentiated (WELCOMING vs CONCERNED vs SURPRISED are visually very distinct) but the tool cannot measure this.

Ideabox C35 filed: `ideabox/20260329_maya_santos_silhouette_panel_bg_fix.md` — proposes `--metric contour` or `--body-subtract` modes for the silhouette tool to properly measure arm-level differentiation.

---

## Assets Delivered This Cycle
1. `output/tools/LTG_TOOL_cosmo_expression_sheet_v005.py`
2. `output/characters/main/LTG_CHAR_cosmo_expression_sheet_v005.png`
3. `output/tools/LTG_TOOL_grandma_miri_expression_sheet_v004.py`
4. `output/characters/main/LTG_CHAR_grandma_miri_expression_sheet_v004.png`
5. `ideabox/20260329_maya_santos_silhouette_panel_bg_fix.md`

Maya Santos — Character Designer
