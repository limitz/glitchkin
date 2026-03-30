<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Pitch Package Audit — Cycle 29
**Prepared by:** Alex Chen, Art Director
**Date:** 2026-03-29
**Purpose:** Pre-Critique 13 audit — identify weakest asset, predict Critique 13 targets, direct Cycle 30.

---

## Current Asset State (end of Cycle 28 / start of Cycle 29)

### Confirmed C28 deliveries:
- Luma turnaround v003 — line weight normalized (all 4 views: head=4, structure=3, detail=2)
- Glitch expression sheet v003 — expanded to 9 expressions, YEARNING/COVETOUS/HOLLOW added
- SF03 v005 — UV_PURPLE_DARK saturation fixed (31% → 72%, deep void reads correctly)
- SF04 v003 — blush (peach not orange-red), Byte fill (GL-01b canonical), rim light (right side only)
- GL-06c registered in master_palette.md
- Luma skin base cross-reference documented (Section 7.7)
- Pitch brief interior need updated (Luma feels invisible; Glitchkin are the first things that need her to see them)
- Procedural draw library v1.2.0 — `add_rim_light()` gains `side` parameter
- Pipeline naming compliance: forwarding stubs + legacy archives + tools README updated

### C29 in-progress (expected to land this cycle):
- Maya: Luma expression sheet v007 (3.2 heads + h×0.22 eyes)
- Maya: Character lineup v006 (3.2 heads, consistent with v007)
- Rin: SF01 v004 (procedural quality lift, replace stale v003)
- Kai: `git mv` pass for LTG_TOOL_ renaming (forwarding stubs → canonical names)

---

## 1. Weakest Remaining Asset After This Cycle's Work Completes

**SF01 — Discovery (v003/v004)**

SF01 is the single weakest asset in the pitch package, regardless of whether v004 lands this cycle.

- v003 has been flagged as visually inconsistent with the expression sheets for multiple cycles — Luma's face/body proportions in v003 predate the 3.2-head canonical spec established in turnaround v002/v003.
- v004 is being built by Rin with a procedural quality focus, but the original proportional inconsistency was never formally addressed in Rin's C29 brief.
- SF01 is the **first visual hook** — the discovery moment that sells the premise. It is the frame critics look at first and longest.
- Every other style frame (SF02, SF03, SF04) now has a recent pitch-primary version with documented fixes. SF01 has the oldest resolved version.

If v004 lands with corrected Luma proportions, SF01 becomes competitive. If v004 is a procedural lift without proportional correction, SF01 remains the weakest link.

**Secondary weak asset: Luma expression sheet v006 (→ v007 in progress)**

v006 still has the wrong head-to-body ratio (~2.5 not 3.2) and over-wide eyes (HR×0.28 vs h×0.22). v007 is in progress and is P1. If v007 lands, this is resolved. The fact that the expression sheet has been open for correction since C28 is a risk — critics will note the version number gap.

---

## 2. Top 3 Things Critique 13 Will Likely Target

### Target 1 — Luma consistency across assets (Daisuke, Priya, Reinhardt)
This is the multi-cycle open wound. Even after v007 lands, critics will check:
- Does the expression sheet match the turnaround?
- Does the lineup match the expression sheet?
- Does SF01 match all three?

If SF01 v004 is still proportionally off while the character sheets are fixed, this inconsistency becomes **more visible**, not less. Critics will use v007 as the new benchmark and find SF01 falling short.

### Target 2 — Drawing order / layer depth errors (Producer directive, Cycle 29)
The producer flagged consistent drawing-order problems across multiple cycles — shapes that should be behind other shapes appear in front. This is a pipeline-level issue. With 30+ assets on disk, at least a few will show this defect. Critics with a technical eye (Reinhardt, Sven, Daisuke) will notice.

### Target 3 — Naming compliance incomplete / forwarding stubs visible (Reinhardt)
Reinhardt has flagged naming convention issues across multiple critique cycles. C28's fix created forwarding stubs that import from the old filenames — this is not a finished solution. Until the `git mv` pass is done and stubs are removed, the pipeline has a structural inconsistency. Reinhardt will likely check whether the C12 directives were truly resolved or merely patched.

---

## 3. Cycle 30 Focus — Final Cycle Before Critique 13

### P1 — SF01 v004 proportional correction
**Assign to Rin** (or Maya to spec-check Rin's output): SF01 v004 must draw Luma at 3.2 heads with h×0.22 eyes. This is not optional — if SF01 still mismatches the character sheets, Critique 13 will open it as a blocker.

Rin's C29 brief was procedural quality. Add a second brief: cross-check Luma proportions in SF01 v004 against turnaround v003 construction spec before final render.

### P2 — Drawing order audit across all generators
**Assign to Kai** or run as a QA pass: Review every active generator in output/tools/ for draw-order errors. Any shape that should be occluded by another shape must be drawn first (painter's algorithm). Focus on character generators and style frames where character/background layering is complex. Document findings. Fix the worst offenders.

### P3 — Git mv naming pass + stub removal
**Assign to Kai**: Complete the formal `git mv` pass to rename original LTG_CHAR_/LTG_COLOR_ source files to LTG_TOOL_ and delete forwarding stubs. Reinhardt will check this. This is a one-time cleanup, and Cycle 30 is the last opportunity before Critique 13.

### P4 — Ideabox review
**Alex Chen (this cycle)**: First pass on ideabox for cross-team collaboration ideas. Route any actionable ideas to the appropriate team members.

---

## Verdict

The pitch package is structurally sound and dramatically stronger than it was at Critique 12. The three active risks are: SF01 proportional consistency with the corrected character sheets, pipeline drawing-order errors surfacing in critic review, and naming compliance remaining in a half-finished state.

Cycle 30 must resolve all three. If those land clean, Critique 13 will have to work hard to find issues.

## 4. End-of-Cycle 29 Status Note

**As of 2026-03-29 (post-C28 completion report review):**

The C29 in-progress items listed above did NOT complete before this audit was finalized:
- Maya: Luma expression sheet v007 — NOT YET DELIVERED (still pending)
- Maya: Character lineup v006 — NOT YET DELIVERED (still pending)
- Rin: SF01 v004 — NOT YET DELIVERED (still pending)
- Kai: git mv naming pass — NOT YET DELIVERED (still pending)

This means the Cycle 29 risk profile going into Cycle 30 is elevated. The proportion inconsistency on Luma expression sheet v006 is still live. SF01 v003 remains the pitch primary for the discovery frame. The naming compliance forwarding stubs are still in place.

**Image Handling Policy (new — applies to all agents including Art Director):**
- Before sending any image to Claude for inspection, ask if a tool can extract the needed insight instead.
- Before sending an image, ask if lower resolution suffices. Downscale if yes.
- Never send high-resolution images to Claude unless absolutely necessary.
- Vision limitations: hallucination risk on low-quality/rotated/tiny images; limited spatial reasoning; approximate counting only.

This policy is now active and must be propagated to all team members in Cycle 30 directives.

---

*Alex Chen, Art Director — Cycle 29 — 2026-03-29 (updated post-cycle review)*
