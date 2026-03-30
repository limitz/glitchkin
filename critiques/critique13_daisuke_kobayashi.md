# Critique 13 — Daisuke Kobayashi, Character Design Formalist
**Date:** 2026-03-29
**Cycle:** 13
**Assets Reviewed:**
- `LTG_CHAR_luma_expressions.png` / `LTG_TOOL_luma_expression_sheet.py`
- `LTG_CHAR_luma_turnaround.png` / `LTG_TOOL_luma_turnaround.py`
- `LTG_CHAR_luma_lineup.png` / `LTG_TOOL_character_lineup.py`
- `LTG_COLOR_luma_color_model.png` / `LTG_TOOL_luma_color_model.py`
- `LTG_CHAR_glitch_expression_sheet.png` / `LTG_TOOL_glitch_expression_sheet.py`

---

## LUMA — Expression Sheet v007

**Score: 62 / 100**

- **P1 — CRITICAL: Body proportion claim is incorrect.** Docstring states "Yields 3.2 heads." Actual code arithmetic: head top = `head_cy − HR`; ground = `head_cy + 545`; total = 649px at 2×; head diameter = 208px; ratio = **3.12**, not 3.2. The fix addressed the torso_h multiplier (HR×1.80→HR×2.10) but the neck segment (HR + HR×0.10 + HR×0.08 = HR×1.18) adds extra height outside the proportion calc, causing undershoot. Claim and code do not agree.
- **P1 — CRITICAL: Eye width "h×0.22" fix produced the wrong result.** In v007, `ew = int(HR * 0.22)` where HR = head radius = 104px at 2×; ew = 22px. In turnaround v003, `ew = int(h * 0.22)` where h = one head unit = 382px at 2×; ew = 84px. Both labeled "h×0.22" but `h` refers to head radius in v007 and head height in v003. Eye width ratio to head radius: v007 = 0.21, turnaround = 0.44. The C12 P1 directive cited ew=h×0.22 from the turnaround — but the two generators use `h` to mean different things. C29 fixed the label but not the semantic. Eyes are **still mismatched across the two primary reference documents**.
- **P2 — SERIOUS: 6 body poses differentiate silhouettes, which is correct; but the per-expression hoodie color tint changes the character's palette per panel.** This is an undocumented design decision. If an animator uses the CURIOUS panel (cool blue hoodie) and the DETERMINED panel (warm amber hoodie) as on-model reference simultaneously, they will produce two visually different characters. Color tint variants are valid, but must be labeled and documented in the character spec. Currently not in `luma.md` or `character_sheet_standards.md`.
- **P3 — MODERATE: Brow weight at 2× render = width=2 (line 182 in `draw_eyes_full`).** Standards doc Section 6 and `draw_eyes_full` docstring both state brows = structure weight = width=3. FRONT view turnaround brows also use width=2 (line 182 of turnaround). Both documents are internally consistent at width=2 but both contradict the standards table. The standard says 3, the code says 2 in both places — update the table or the generators.

**Bottom line:** The C12 P1 body proportion directive was addressed structurally but the arithmetic still misses 3.2 by 2.5%, and the eye-width "fix" produced a new mismatch because the same spec string ("h×0.22") was applied to different reference variables in two documents.

---

## LUMA — Turnaround v003

**Score: 71 / 100**

- **P1 — CRITICAL: Eye width cross-document mismatch is not resolved (see above).** Turnaround FRONT ew = int(h×0.22) = 84px at 2×. Expression sheet v007 ew = int(HR×0.22) = 22px at 2×. These describe eyes of radically different sizes relative to the head. A field animator comparing both sheets will draw different characters.
- **P2 — SERIOUS: SIDE view eyes are significantly narrower than FRONT view.** SIDE: `ew = int(h * 0.16)`, `eh = int(h * 0.13)` (lines 485). FRONT: `ew = int(h * 0.22)`, `eh = int(h * 0.15)`. Eye width drops 27% from front to side. This may be intentional foreshortening but it is not documented. The SIDE eye width relative to head_r: 0.32 (vs 0.44 front). Without documentation, an animator drawing the 3/4-to-side transition will not know whether to interpolate or step the eye width.
- **P2 — SERIOUS: 3/4 view head radius is `int(h * 0.48)` (foreshortened) but no documentation explains the foreshortening rule.** Is the 0.48 a fixed ratio? Does it follow a perspective formula? Without a stated rule, two artists drawing the 3/4 view will use two different foreshortening amounts.
- **P3 — MODERATE: Hood visible from BACK view is drawn flat (width=3 polygon) with no volumetric depth cue.** The hood shape is a simple trapezoid. A director cannot tell from this reference whether the hood lies flat, protrudes, or has padding. One labeled dimension or a depth note would resolve this ambiguity.
- Line weights: CONFIRMED FIXED — head outline = width=4, structure = width=3, detail = width=2 throughout all four views. BACK view confirmed present. C12 P2 and P3 are resolved.

**Bottom line:** Line weight and BACK view issues from C12 are resolved; the persistent eye-width mismatch and absence of documented foreshortening rules remain production risks.

---

## LUMA — Lineup v006

**Score: 74 / 100**

- **P2 — SERIOUS: Byte shadow color still incorrect.** `BYTE_SH = (0, 144, 176)`. Canonical value (expression sheet v004) = `(0, 168, 192)`. This C12 P3 (Moderate) directive was not acted on. At lineup scale the difference is visible — Byte reads as darker and more muted in the lineup than on its own expression sheet.
- **P2 — SERIOUS: Lineup Luma eye width = `int(r * 0.22)` where r = head radius ≈ 40px.** `ew = int(40 * 0.22) = 8px`. This is consistent with v007 (same formula, same variable meaning). But because the turnaround uses a different formula producing 44% of head_r, the lineup Luma reads with smaller eyes than the turnaround Luma. The inconsistency now propagates across three documents: lineup + expression sheet on one side, turnaround on the other.
- **P3 — MODERATE: LUMA_RENDER_H = 280px, HEAD_UNIT = 87.5px.** The lineup head unit is 87.5px vs turnaround head unit at 1× = 191px. These are different render scales, which is expected — but nowhere in the lineup is there a cross-reference back to the canonical head unit. A production supervisor looking at the lineup cannot verify that the lineup head unit is proportionally consistent with the turnaround. A single annotation tying LUMA_RENDER_H to the canonical 3.2-head spec would close this.
- **P4 — MINOR: Glitch GLITCH_H = int(BYTE_H * 1.05).** Glitch is defined by its relationship to Byte, not by a canonical self-contained proportion. If Byte's height changes, Glitch's height silently shifts. Document Glitch's intended standalone height in lineup inches/heads alongside the derived formula.

**Bottom line:** 3.2-head ratio is correct and all five characters are present; the Byte shadow mismatch from C12 remains unaddressed, and the eye-width inconsistency propagates from the main sheets into this document.

---

## LUMA — Color Model v002

**Score: 80 / 100**

- **P2 — SERIOUS: Color model silhouette uses `head_r = 46` with a simplified one-ellipse hair mass.** The canonical Luma hair is an 8-ellipse curl cloud. The color model shows a single flat oval hair mass. At this document's purpose (palette reference) the simplified silhouette is acceptable — but the hair color `HAIR_HL = (61, 31, 15)` is used on a single arc highlight that reads as a simple dome, not the cloud structure. An artist using this document as their only Luma reference will not know the hair is a cloud of 8 ellipses.
- **P3 — MODERATE: Skin palette lists two skin tone variants:** `#C8885A (200, 136, 90)` labeled "lamp-lit base" and `#C4A882 (196, 168, 130)` labeled "neutral base RW-10." These are different colors for the same face in different lighting contexts. The relationship between them is not documented. Which one does the expression sheet use? (Answer: v007 uses `SKIN = (200, 136, 90)`, the lamp-lit variant.) An animator needs to know which skin base is canonical for each lighting zone.
- **P4 — MINOR: Canvas background is near-black `(22, 14, 8)` which is correct for pitch display; however no note indicates this is a display background, not a production cel background.** Standard housekeeping.
- Eye width fix: CONFIRMED — `eye_r_x = int(head_r * 0.22)` = 10px at head_r=46. Consistent with v007 formula (same variable meaning: head radius). C30 fix applied correctly.

**Bottom line:** Eye width fix is confirmed; the simplified hair mass and undocumented dual-skin-tone relationship are the remaining documentation gaps for this asset.

---

## GLITCH — Expression Sheet v003

**Score: 72 / 100**

- **P1 — CRITICAL: `diamond_pts()` construction still has no written spec.** C12 Issue 8 directed: "Write a one-paragraph construction-from-primitives spec for Glitch." Not present in v003 or in any associated `.md` file I could locate. The formula is: top=(cx+rx×0.15×sinθ, cy−ry_eff+rx×0.15×cosθ), right=(cx+rx×cos(−θ), cy+rx×0.2×sin(−θ)), bot=(cx−rx×0.15×sinθ, cy+ry_eff×1.15), left=(cx−rx×cos(−θ), cy−rx×0.2×sin(−θ)). None of this is in any spec document. An animator drawing Glitch by hand cannot reproduce these vertices from anything other than the code.
- **P2 — SERIOUS: New interior expressions (YEARNING, COVETOUS, HOLLOW) use pixel glyphs only — no body or arm differentiation from existing states.** YEARNING: arms hang low (arm_dy=0, default), no body tilt. HOLLOW: slightly deflated (squash=0.88). COVETOUS: tilt=+12, arms reaching. Squint test: YEARNING and HOLLOW share near-identical body silhouettes. At thumbnail scale these three states collapse into one read. Interior emotional states still need exterior body-language anchors to survive production.
- **P2 — SERIOUS: COVETOUS eye glyph is identical left and right** (both `[[5,5,5],[0,5,0],[0,0,0]]`). The established glyph system uses right-eye destabilization to signal emotional asymmetry. COVETOUS deliberately overrides this (docstring: "bilateral focus"). The override is valid but unspecified — it contradicts the documented right-eye destabilization rule without noting the exception. Future animators will see the pattern broken and not know whether it is intentional.
- **P3 — MODERATE: Nine-expression 3×3 grid means interior states share row-3 with the original performance states in a non-obvious grouping.** Row 1: NEUTRAL, MISCHIEVOUS, PANICKED. Row 2: TRIUMPHANT, STUNNED, CALCULATING. Row 3: YEARNING, COVETOUS, HOLLOW. Row 3 is not labeled as "interior states" anywhere in the sheet. A director or layout artist reading the sheet has no visual cue that row 3 represents a different register of performance.

**Bottom line:** The 9-panel expansion does what C12 asked (add interior desire) and the three new glyphs are emotionally specific — but the diamond construction still has no spec document, the YEARNING/HOLLOW body-language distinction collapses at thumbnail, and the 3×3 grid needs a row-group label to communicate the interior/exterior split.

---

## Cross-Document Summary

| Asset | Score | Primary Blocking Issue |
|---|---|---|
| Luma expr v007 | **62** | Body ratio claims 3.2, code produces 3.12; eye-width fix created new semantic mismatch |
| Luma turnaround v003 | **71** | Eye-width mismatch with expr sheet persists; side-view foreshortening undocumented |
| Lineup v006 | **74** | Byte shadow color C12 P3 still unresolved; eye-width mismatch propagates |
| Color model v002 | **80** | Eye fix confirmed; simplified hair mass; dual-skin-tone undocumented |
| Glitch expr v003 | **72** | Diamond spec still absent; interior states collapse at thumbnail |

---

## Priority Directives (ordered by severity)

1. **(P1 — Blocking)** Unify the eye-width variable semantics. The spec string "h×0.22" means head-height in the turnaround and head-radius in the expression sheet. Pick one canonical definition (I recommend: **ew = head_radius × 0.44** if matching the turnaround, or **ew = head_radius × 0.22** if the expression sheet is the master) and rebuild both documents from that single constant. Do not allow `h` to mean different things in sibling documents.

2. **(P1 — Blocking)** Verify the expression sheet v007 body proportion arithmetic. The code produces 3.12 heads, not 3.2. Either adjust the torso + leg constants to close the gap, or document that 3.2 is a nominal approximation and state the true computed ratio in the docstring.

3. **(P1 — Blocking)** Write a construction-from-primitives spec for Glitch's `diamond_pts()` body. Three sentences and one labeled diagram. This directive is now two critique cycles old.

4. **(P2 — Serious)** Document the turnaround's foreshortening rules: what head_r fraction is used per view, and why, so that interpolated views (e.g., over-shoulder) can be derived consistently.

5. **(P2 — Serious)** Fix Byte shadow color in lineup v006 to `(0, 168, 192)`. This directive is now two critique cycles old.

6. **(P2 — Serious)** Differentiate YEARNING and HOLLOW body silhouettes so they survive a squint test at 100px thumbnail.

7. **(P3 — Moderate)** Document the per-expression hoodie color tints in `luma.md` or the character sheet standards. These are currently invisible to anyone who does not read the generator source.

8. **(P3 — Moderate)** Reconcile brow line weight: standards doc says width=3, both generators use width=2. Update one to match the other.

9. **(P3 — Moderate)** Add a row-group label to the Glitch 3×3 grid distinguishing "performance states" (rows 1–2) from "interior desire states" (row 3).

10. **(P4 — Minor)** Annotate the color model's dual skin tones with a lighting zone guide: which base for Real World, which for Glitch Layer scenes.

---

## Closing Assessment

The team addressed the most visible structural issues from C12: line weights in the turnaround are corrected, the BACK view exists, and the 3.2-head directive has been applied across three documents. These are real improvements.

However, the central C12 finding — "three documents, three different ratios" — has been replaced by a subtler version of the same problem: two documents both claim "h×0.22" but use `h` to mean different things. The eye size discrepancy has not closed; it has been obscured by a shared label. This is the kind of drift that production models rely on tooling to catch, which is exactly why a proportion audit tool was built. I recommend that tool be updated to check ew/head_radius ratio (not ew/head_unit ratio) and run against all generators, not just style frames.

The Glitch construction spec is two cycles overdue. That directive will appear in Critique 14 with the same wording unless acted on.

---

*Daisuke Kobayashi — Character Design Formalist*
*Critique 13 — 2026-03-29*
