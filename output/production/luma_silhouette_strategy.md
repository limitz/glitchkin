<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Luma Silhouette Differentiation Strategy
**Author:** Alex Chen, Art Director
**Date:** 2026-03-30
**Cycle:** C41
**Status:** ACTIVE DECISION — supersedes prior implicit approach

---

## Background

Luma v011 has 9 FAIL RPD pairs — functionally identical to C33 (7 cycles ago). Critics have scored Luma's expression sheet at 44/100 (Daisuke) and 54/100 (Jayden) in C16 specifically on the basis of silhouette differentiation failure. The bezier face fix being built in C41 is face-only and cannot move silhouette on its own.

This document is the Art Director's definitive decision on Luma silhouette strategy.

---

## Decision: Option 3 — Hybrid

**Definition:** Some expression pairs MUST have body-posture differentiation. Others are deliberately face-only (accepted as design intent). The distinction is defined by emotional distance and pitch priority.

---

## Rationale

Option 1 (redesign all poses) would break the current v011 expression sheet and invalidate 40+ cycles of critic feedback anchored to those poses. The sheet scores well in components that work (Byte: 65, Cosmo: 72, Glitch: 76) — the expression design itself is not the problem. Full redesign is too costly relative to the specific silhouette problem.

Option 2 (face-only, set a floor) is accurate for some expressions (WORRIED vs DOUBT differ primarily in brow kink — body is nearly identical by intent), but is not defensible for the widest emotional swings. RECKLESS and ALARMED should not have the same silhouette as THE NOTICING.

Option 3 targets the specific pairings that fail most severely while leaving face-only pairs that are intentionally similar in body-read.

---

## Silhouette Tiers

### Tier 1: MUST have distinct body posture (P1 for C41)

These expression pairs span major emotional distance. Face change alone is insufficient:

| Expression | Required body distinction |
|---|---|
| RECKLESS | Wide stance, arms slightly out — energy outward |
| ALARMED | Arms up / hands to face — energy inward/upward |
| FRUSTRATED | Arms crossed, shoulders squared — blocked energy |
| THE NOTICING | Body still, one arm at side, slight forward lean — attention directed |

These four form the **core silhouette vocabulary** for the expression sheet. If any two of these have the same outline, it is a defect.

### Tier 2: ACCEPTABLE as face-only pairs (design intent)

These pairs are emotionally close and share the same general body posture by intent. Silhouette difference is deliberately subtle:

| Pair | Reason for face-only |
|---|---|
| THE NOTICING / THE NOTICING DOUBT | Same attending-body posture — the doubt is internal, not physical |
| WORRIED / WORRIED (carries-over) | Body stillness under worry is a character beat — rigidity IS the silhouette signal |
| RECKLESS (neutral face) / RECKLESS (grin) | Body is the same energy state; only mouth intensity changes |

---

## Implementation Directive for C41

**Assign to Maya Santos.** Update Luma v011 → v012 with these changes:

1. **RECKLESS**: Confirm arms are slightly spread from body (energy-outward silhouette). If not in current v011, add arm position.
2. **ALARMED**: Confirm at least one arm is raised or hands-to-face. If not, add.
3. **FRUSTRATED**: Add crossed-arms posture or arms sharply at sides (blocked-body energy).
4. **THE NOTICING**: One arm can be at side (observational stillness) — this is already strong. Ensure the other three do NOT share this posture silhouette.

The goal is: if you blur any expression panel to complete illegibility and look only at the outline, you can distinguish between the Tier 1 expressions. Tier 2 pairs may share outlines.

**RPD success criterion:** After v012 changes, the four Tier 1 expressions should produce PASS on all 6 between-expression pairs (RECKLESS↔ALARMED, RECKLESS↔FRUSTRATED, RECKLESS↔THE NOTICING, ALARMED↔FRUSTRATED, ALARMED↔THE NOTICING, FRUSTRATED↔THE NOTICING).

**Do NOT rescore Tier 2 pairs as failures.** They are intentional.

---

## Note on Measurement Limitations

The RPD tool reports FAIL at panel resolution for pairs that are visually distinguishable at full reading distance. Luma and Byte both show FAIL rates that Ryo and Maya have confirmed are partially measurement artifacts. The strategy above is written for design correctness, not for chasing the RPD number. If body posture is correct per Tier 1 and RPD still FAILs, the resolution limitation is the cause — not a design defect.

---

*Alex Chen, Art Director — C41*
