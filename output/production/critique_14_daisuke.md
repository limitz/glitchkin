# Critique 14 — Daisuke Kobayashi, Character Design Formalist
**Date:** 2026-03-29
**Cycle:** 34
**Assets Reviewed:**
- `LTG_CHAR_luma_expressions_v009.png` (primary C34 focus)
- `LTG_CHAR_byte_expression_sheet_v005.png`
- `LTG_CHAR_cosmo_expression_sheet_v004.png`
- `LTG_CHAR_grandma_miri_expression_sheet_v003.png`
- `LTG_CHAR_glitch_expression_sheet_v003.png`
- `LTG_CHAR_character_lineup_v007.png`

**Tools run:** `LTG_TOOL_expression_silhouette_v002.py` (--mode full + --mode arms), `LTG_TOOL_render_qa_v001.py`, `LTG_TOOL_lineup_palette_audit_v001.py`, `LTG_TOOL_char_spec_lint_v001.py`, `precritique_qa_c34.md` reviewed.

---

## LTG_CHAR_luma_expressions_v009.png — PRIMARY C34 FOCUS

**Score: 52/100**

- **FAIL (silhouette/full mode):** Worst pair P1↔P2 (CURIOUS↔DETERMINED) = 87.7%. Three FAIL pairs total. The arm-vocabulary redesign is real — DELIGHTED arms-up and FRUSTRATED crossed-arms ARE new shapes — but the middle cluster (CURIOUS, DETERMINED, WORRIED) has not escaped mutual similarity. CURIOUS lean + WORRIED self-hug share enough body mass at panel resolution to stay in FAIL range.
- **FAIL (silhouette/arms mode):** Worst pair P3↔P6 (SURPRISED↔FRUSTRATED) = 97.0% in arm region. Four FAIL pairs in arms mode. The center-mask at 28% is still letting the shared torso column dominate. SURPRISED Y-arms and FRUSTRATED crossed-arms should be maximally different shapes — 97% says the arm geometry is not landing at panel resolution.
- **Construction spec gap:** `draw_crossed_arms()` and `draw_self_hug_arms()` are new functions per v009 docstring — good. But the resulting pixel-level difference between crossed (mid-torso) vs self-hug (chest-level) is sub-4px at 1× render. At 373px panel width, a 4px arm-height delta is below the squint threshold. The silhouette tool confirms this.
- **Eye-width canonical:** L002 PASS (HR×0.22 confirmed). This C12/C32 P1 issue is closed.
- **Color fidelity:** WARN (QA tool). DELIGHTED and SURPRISED share the same hoodie color `(232, 112, 42)` — identical panel coloring erodes the emotional read when sheets are viewed at thumbnail scale.

**Bottom line:** Three FAIL pairs in full mode and four in arms mode after a full redesign pass is not a near-miss — the arm geometry changes are real but insufficient at production thumbnail scale, and the CURIOUS/DETERMINED/WORRIED cluster is still a shape family, not three distinct shapes.

---

## LTG_CHAR_byte_expression_sheet_v005.png

**Score: 68/100**

- **FAIL (silhouette):** P7↔P8 = 88.1%. One FAIL pair. Given the 10-expression 4×3 grid, one failure is the best result of any human-adjacent character. UNGUARDED WARMTH (P9 new expression) is the worst offender — the tool reads it as too similar to the expression directly adjacent.
- **Identity risk:** UNGUARDED WARMTH uses SOFT_GOLD confetti as its sole differentiator — this is a color signal, not a body-language signal. At silhouette level (black fill), the gold confetti disappears and the body pose must carry the expression. The arms-floating (-5 dy) and -4 body_tilt are a 9px delta — invisible at 200px thumbnail.
- **Cast coherence (fresh-eye review):** Byte's expression vocabulary has grown to 10 states. The COVETOUS/HOLLOW/UNGUARDED WARMTH interior expressions are narratively motivated. But at sheet scale, the pixel-symbol system (arrow, heart, star) is doing most of the differentiation work — the body-language is near-neutral across 6 of 10 expressions. This is the opposite of the Glitch sheet, where body IS the expression.
- **Color fidelity WARN:** QA. Not a character-specification issue — flagged for completeness.

**Bottom line:** Byte's sheet is the best-performing of the non-Glitch characters by metric but relies excessively on pixel symbols rather than body language for emotional differentiation, making half the expression set silhouette-deaf.

---

## LTG_CHAR_cosmo_expression_sheet_v004.png

**Score: 34/100**

- **CRITICAL FAIL (silhouette):** Worst pair P1↔P2 = 95.9%. Six FAIL pairs. This is the worst score of all character sheets. The C34 brief called out Cosmo's 96% C33 baseline; v004 is unchanged. If v004 was the sheet that went into C34 with no silhouette revision, the brief was not actioned for Cosmo.
- **Cross-sheet drift:** C12 P1 directed a canonical head-to-body ratio of 4.0 heads for Cosmo. Spec lint S001 PASS. But with six FAIL pairs, the body proportions — even if correctly specified — are not generating distinguishable silhouettes.
- **Body-language vocabulary:** The expression_pose_brief_c34.md was explicit: AWKWARD requires maximum asymmetry, WORRIED requires the head-grab bracket, SURPRISED requires horizontal arm-spread + backward lean. None of these are in the generator docstring for v004. This sheet has not been touched by the C34 brief.
- **Value ceiling:** QA shows max=241, not ≥225 spec minimum — this is marginal but passing. Line weight 1 outlier.

**Bottom line:** Cosmo v004 is the same sheet that scored at 96% similarity in C33 — the C34 brief's silhouette corrections have not been applied, and this sheet is functionally useless as an acting reference.

---

## LTG_CHAR_grandma_miri_expression_sheet_v003.png

**Score: 38/100**

- **CRITICAL FAIL (silhouette):** Worst pair P7↔P8 = 96.9%. Seven FAIL pairs, including 4 above 90%. KNOWING STILLNESS and WISE/KNOWING are by-design face-only (acknowledged), but WARM/WELCOMING↔NOSTALGIC↔CONCERNED form their own 93% cluster — these should be distinctly differentiated by the C34 brief.
- **C34 brief not applied:** The brief specified wide-open arms for WELCOMING, hand-to-chest for NOSTALGIC, clasped-hands for CONCERNED. v003 was created in C33 (KNOWING STILLNESS addition) and is the same sheet from C33. None of the pose vocabulary from the C34 brief is reflected.
- **M001 construction WARN:** Head-to-body ratio 3.2 not confirmed in generator. This is a persistent unresolved C12 directive.
- **Cast coherence concern:** Miri at v003 is softer and rounder than the C34 brief's CONCERNED/WELCOMING specifications — but the pose vocabulary is the problem, not the design. The design is correct for the character; the poses are too close to neutral to distinguish at production scale.

**Bottom line:** Seven FAIL pairs including a 96.9% worst-case, and the C34 brief's pose vocabulary has not been implemented — Miri v003 is a C33 partial update being presented as a C34-ready sheet.

---

## LTG_CHAR_glitch_expression_sheet_v003.png

**Score: 82/100**

- **PASS (silhouette):** Overall PASS, worst pair 71.1%. Glitch remains the only character that builds expressiveness into body geometry rather than face-only changes. This principle continues to work.
- **Active panel detection anomaly:** The silhouette tool detects only 5 active panels from a 9-panel 3×3 grid containing 9 filled expressions (NEUTRAL, MISCHIEVOUS, PANICKED, TRIUMPHANT, STUNNED, CALCULATING, YEARNING, COVETOUS, HOLLOW). The dark-BG sheets flag means COVETOUS, HOLLOW, and potentially CALCULATING are registering as near-background to the tool's panel classifier. This is not a visual failure — it is a tool blind spot for the new dark interior expressions. However: if the tool cannot classify them as active, a director doing a quick silhouette check will also lose 4 expressions in a dark room. The interior expressions (YEARNING, COVETOUS, HOLLOW) may need a subtle luminance separation to differentiate from the panel void.
- **C12 P8 unresolved:** Written construction spec for Glitch's diamond body primitive still absent. This remains open across two critique cycles.
- **Color fidelity PASS:** Only character sheet to pass QA color check. Glitch's restricted palette (CORRUPT_AMBER/HOT_MAG/UV_PURPLE) makes color management tractable.

**Bottom line:** Glitch passes where all others fail because the design philosophy is correct — body IS expression — but the new interior states (COVETOUS, HOLLOW) are visually indistinguishable from blank panels to automated tools, which suggests a luminance floor problem in those panels.

---

## LTG_CHAR_character_lineup_v007.png

**Score: 61/100**

- **Palette audit WRONG (legacy values):** `lineup_palette_audit_v001.py` flags legacy incorrect values detected alongside the canonical values — Byte body #00C0D2 and Byte shadow #0099A8 still present in the image. The C33 fix (#00A8B4) passes, but the presence of legacy pixel values indicates the generator is compositing from stale layer data or retaining pre-fix pixels. This needs investigation — a lineup where two color readings of Byte body co-exist in the PNG is ambiguous.
- **Staging:** Lineup v007 places five characters on a flat baseline with no vertical rhythm variation. Glitch hovers but the hover height (GLITCH_H = ~170px) is within the variation range of the other characters' natural height differences. The composition reads as five objects in a row, not a cast with narrative relationships. A height-stagger or half-step staging would communicate the cast's inter-character dynamics.
- **Silhouette test misapplied:** The tool auto-detected a 3×3 grid and reported lineup results as if it were an expression sheet — this is a tool limitation to document, not a design failure, but it means the lineup has no valid automated silhouette coverage this cycle.
- **Cross-sheet on-model (fresh eye):** With Luma now at v009 arm vocabulary and Byte at v005 with 10 expressions, the lineup's Luma (3.2 heads, eye r×0.22) matches the v009 expression sheet. This cross-sheet alignment is a genuine improvement from C12 where three different ratios coexisted.

**Bottom line:** The proportion alignment between lineup and expression sheet is finally consistent (Luma 3.2 heads throughout), but legacy palette pixels surviving in Byte's render and the flat staging both require resolution before this lineup functions as a production reference.

---

## Cast Coherence Review (fresh eyes — complete pitch)

The critical observation for C34: three of four human character expression sheets (Luma, Cosmo, Miri) were scheduled for silhouette-differentiation revision per the C34 brief. Only Luma received a revision pass. Cosmo v004 and Miri v003 are carrying forward from C33 unchanged. The pipeline implication: the brief existed, the tool existed, the deadline existed — two of three actionable sheets were not actioned.

At the cast level: Glitch (PASS, 71%) and Byte (FAIL, 88%, one pair) are the better-differentiated sheets. Luma (FAIL, 87.7%, three pairs) improved. Cosmo (FAIL, 95.9%, six pairs) and Miri (FAIL, 96.9%, seven pairs) are at C33 levels. A commissioning panel comparing these five sheets in sequence will see a performance gap between the machine character and the human characters that does not reflect the design quality — it reflects incomplete revision coverage.

---

## Priority Directives

1. **(P1 — Blocking)** Cosmo and Miri expression sheets must receive the same silhouette revision pass that Luma received in C34. The C34 brief is already written. Implement it.
2. **(P1 — Blocking)** Luma v009 three FAIL pairs must reach ≤1 FAIL pair at most. Focus: CURIOUS↔DETERMINED arm-height delta needs to exceed the 4px sub-threshold floor; use `--center-mask 0.36` to retest.
3. **(P2 — Serious)** Byte UNGUARDED WARMTH silhouette hook is color-only. The body-tilt + arm-float delta must be increased to register at 200px thumbnail scale.
4. **(P2 — Serious)** Glitch COVETOUS and HOLLOW luminance: add a minimum luminance floor to dark-BG interior panels so the silhouette tool (and human reviewers) can classify them as active.
5. **(P3 — Moderate)** Lineup v007: audit the Byte layer for legacy pixel contamination. The palette audit finding of both canonical AND legacy values in the same PNG is a production consistency defect.
6. **(P3 — Moderate)** C12 P8 remains open (Glitch construction spec). One sentence and one labeled diagram. This takes 20 minutes. It has been open two critique cycles.

---

*Daisuke Kobayashi — Character Design Formalist*
*Critique 14 — 2026-03-29*
