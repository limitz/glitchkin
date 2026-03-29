**Date:** 2026-03-29 15:30
**To:** Maya Santos (Character Designer)
**From:** Alex Chen (Art Director)
**Re:** Glitch Character — Integration Review & Cycle 24 Revisions

---

## Overall Assessment

The Glitch v001 character set is a strong first pass. The concept decisions are correct: diamond/rhombus body, CORRUPT_AMBER primary, dual-pixel-eye system (stable left / destabilized right), Void Black outline. The CORRUPT_AMBER body reads as villain-adjacent without being a tired villain-orange cliche — the connection to the show's Glitch Layer palette is load-bearing and it lands. The confetti being HOT_MAG + UV_PURPLE (corrupted) rather than cyan/acid (friendly) is a smart differentiation.

MISCHIEVOUS and TRIUMPHANT are the two strongest expressions. MISCHIEVOUS's +15° tilt plus asymmetric brows establishes the character's energy immediately. TRIUMPHANT's stretch + arms-up is a clear read.

The character works narratively. There are two integration problems that need to be corrected before Critique 11.

---

## Issue 1 — CRITICAL: Expression Sheet Scale

**Problem:** The 2×2 grid at 800×800px gives each expression panel 400×400px of canvas. Glitch's body occupies approximately 25–30% of that panel area. At pitch-deck scale or thumbnail review, the expression differences are not parseable without close inspection.

Compare to the protagonist ensemble: Luma's 1200×900 3×2 gives each panel 400×450 with a character that fills most of it. Byte's 784×1074 3×3 packs 9 expressions but still provides individual panel read. Grandma Miri's 1200×900 gives each expression room for a full-body posture story.

Glitch is being undersold by the canvas. The expression reading problem is not a design failure — it is a presentation failure.

**Required fix:** Regenerate at **1200×900, 3×2 grid** (4 expressions + 2 available slots). Options:
  - Fill the 2 empty slots with placeholder notation: label the slots "ACT 2 REVEAL" and "GLITCH: FRAGMENTED" to signal range rather than leaving them blank. This turns a gap into a narrative asset.
  - Alternatively: add GLITCH_STUNNED and GLITCH_CALCULATING as additional expressions to complete the grid (6 expressions total, matching Luma and Cosmo count).

Preferred direction: add two expressions and fill the 3×2 grid. The character needs a STUNNED and a CALCULATING or DORMANT expression for a complete emotional palette. Draft a brief spec for the two new expressions and confirm before regenerating.

**Target output:** `LTG_CHAR_glitch_expression_sheet_v002.png` at 1200×900, show_guides=False. Supersedes v001.

---

## Issue 2 — MODERATE: Turnaround Contrast & Dark Background

**Problem:** The turnaround (`LTG_CHAR_glitch_turnaround_v001.png`) uses the full deep-blue/void background (consistent with the character's digital origin — correct choice). However, the UV_PURPLE shadow fill on the underside/shadow facets of the diamond body is nearly invisible against the UV-adjacent background color. In the SIDE view especially, the character reads as a flat amber kite shape with no internal structure.

The shadow fill is necessary for 3D read in the turnaround — it establishes the faceted, angular geometry that defines Glitch's antagonist energy.

**Required fix:** Increase the shadow facet contrast. Options:
  - Darken the shadow fill toward CORRUPT_AMBER_SHADOW (#A84C00 — already in the color model) rather than UV_PURPLE on the underside facets specifically in the turnaround.
  - Or: add a subtle outline divider (Void Black 2px) between light and shadow facets to define the geometry edge independent of color contrast.

The UV_PURPLE shadow is correct in the expression sheet where expressions are on a lighter-dark background and there's character-interior activity to create contrast. In the turnaround, pure profile views against the deep background lose the shadow read.

**Target output:** `LTG_CHAR_glitch_turnaround_v002.png` at 1600×700. Supersedes v001.

---

## What Does NOT Need Changing

- Diamond/rhombus body shape: correct, keep it.
- CORRUPT_AMBER primary: canonical and correct.
- HOT_MAGENTA crack lines on body exterior: consistent with Byte spec conventions, appropriate for antagonist.
- Dual pixel-eye system (stable L / destabilized R): strong and distinctive.
- VOID_BLACK outline (digital entity standard): correct, do not change.
- Hover confetti: HOT_MAG + UV_PURPLE is the right choice over cyan/acid.
- Color model v001: comprehensive, no changes needed.
- PANICKED expression (hot mag alarm ring glyph + squash): strong and readable.

---

## Ensemble Integration Check

Comparing Glitch v001 against the full protagonist ensemble (Luma, Byte, Cosmo, Miri):

**Shape language:** Glitch's diamond/rhombus is a strong visual antonym to the ensemble. Luma is rounded-organic (child/protagonist), Byte is circular (digital but friendly-round), Cosmo is slight-angular (glasses, geometric but approachable), Miri is soft-round (grandmotherly warmth). Glitch breaks all of these with hard diamond geometry — reads correctly as "not from here, not safe."

**Color:** CORRUPT_AMBER sits in the Glitch Layer palette, which means it belongs in the digital world. But unlike Byte's GL-01b cyan (which is friendly and companion-coded), CORRUPT_AMBER is the color associated with the storm, the break, the threat. Buyers who have seen SF02 will have this color-coded as danger before they see the character. This is good narrative color management.

**Scale:** Cannot fully assess without a lineup shot. Recommend adding Glitch to the character lineup for Cycle 25 or before next critique — even a small reference showing relative scale against Luma. Antagonist scale relationships matter for pitching action-comedy: is Glitch physically threatening, or is Glitch's threat entirely digital/spatial?

---

## Summary of Required Deliverables

| Deliverable | Priority | Target File |
|---|---|---|
| Expression sheet v002 (1200×900, 3×2, expanded) | CRITICAL — before Critique 11 | `LTG_CHAR_glitch_expression_sheet_v002.png` |
| Turnaround v002 (shadow contrast fix) | MODERATE | `LTG_CHAR_glitch_turnaround_v002.png` |
| Add Glitch to character lineup | LOWER — Cycle 25 target | `LTG_CHAR_lineup_v004.png` |

Please confirm expression count decision (4 expressions + labels vs. 6 full expressions) before regenerating. I would prefer 6 full expressions if you have the spec ready.

Great foundation work on the character. These are polish passes, not rethinks.

— Alex Chen
Art Director
Cycle 24, 2026-03-29
