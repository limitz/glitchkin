**Date:** 2026-03-29 19:00
**To:** Alex Chen
**From:** Producer
**Re:** Cycle 26 — Art Director Assignment

---

## Context
Six messages from the producer are in your inbox. Process and archive each one. Summary of required actions:

---

## 1. Generate New Critics Panel (CRITICAL — replaces existing)
Producer: "new panel of critics, much more critical than the previous."

Replace the current 15 critics in `CRITICS.md` with a new panel of 15.
The new panel must be MORE brutal, more specialized, and more unforgiving than the current one.
Criteria for new panel:
- Each critic is a world-class professional with zero patience for near-misses
- Mix of specialists: animation craft, visual storytelling, character design, color/lighting, production design, concept originality, technical art, child development, cultural authenticity, compositing/FX, typography/brand, art history, draftsmanship, background art, industry experience
- Every critic has a distinct and brutal critique style — no two critics sound alike
- Every critic writes their own bio file in `critics/[name].md`

Process:
1. Write `CRITICS.md` with 15 new critics
2. Write a bio file for each in `critics/` directory
3. Note: when critique runs, each critic must look at **ALL work in output/**, not just the latest cycle

---

## 2. Investigate Luma Style Inconsistency
Producer: "The LUMA expression sheet looks nothing like the other images, like LTG_CHAR_luma_classroom_pose_v002. I prefer the look in the classroom pose."

Action:
- Compare `LTG_CHAR_luma_expression_sheet_v005.png` (or the generator) against `LTG_CHAR_luma_classroom_pose_v002.png`
- Identify the specific differences: line quality, construction method, color palette, proportions
- Write a directive to Maya specifying exactly what needs to align with the classroom pose style
- Send the directive to `members/maya_santos/inbox/`

---

## 3. Update README (Be Proud)
Producer: "don't be apologetic for being an AI, be proud of it!"

Find `README.md` in the project root. Update the Alex Chen art director section — rewrite it to be confident, direct, and proud about the team being AI-driven. Remove any apologetic language.

---

## 4. Update Rin's Role — Procedural Generation (not post-processing)
Producer: "I would like to make sure that Rin is working alongside Kai on the procedural generation of assets, not as a postprocessing step. Handdrawn stylization and other effects start there."

Actions:
- Update Rin's entry in `TEAM.md`: change role to "Procedural Art Engineer" (or similar)
- Update `members/rin_yamamoto/PROFILE.md` to reflect the new role
- Send Rin an inbox message explaining:
  - The role shift: from post-processing to integrated procedural generation
  - She should work with Kai to build stylization directly into the generation pipeline
  - The stylize_handdrawn tool (post-process) remains for legacy assets; new work integrates style at generation time
  - Direct her to study `/home/wipkat/artistry` — a separate AI artist project with learned techniques: wobble paths, variable stroke weight, silhouette-first pipeline, volumetric face lighting, rim lights, three-tier line weight in Cairo. These techniques should be extracted and integrated into the LTG PIL pipeline.

---

## 5. Aesthetics + Rendering Pipeline — 3-Cycle Focus
Producer: "Focus on aesthetics and the rendering pipeline the next 3 cycles. Make tools to assess the quality of the rendering and use them for quality control and internal refinement."

This is a 3-cycle directive (C26, C27, C28). For C26:
- Write a quality assessment brief documenting what "rendering quality" means for LTG:
  - Silhouette readability at thumbnail scale
  - Line weight consistency (3-tier standard)
  - Value range (dark anchor, full spectrum)
  - Color fidelity (canonical palette)
  - Lighting logic (warm/cool separation, light source consistency)
- Send this brief to Kai's inbox as the QA tool specification

---

## Priority Order
1. Luma inconsistency investigation → directive to Maya (she can start immediately)
2. Rin role update + artistry brief
3. New critics panel (significant work)
4. README update
5. QA brief to Kai

— Producer
