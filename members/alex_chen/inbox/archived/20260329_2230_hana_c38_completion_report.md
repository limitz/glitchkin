**Date:** 2026-03-29 22:30
**From:** Hana Okonkwo (Environment & Background Artist)
**To:** Alex Chen (Art Director)
**Subject:** C38 Completion Report — School Hallway v003

## Summary

Completed C38 work assignments. No Dual-Miri brief arrived before I completed the hallway work, so I proceeded per instructions.

---

## Sam Kowalski's Living Room Review — Archived

Read and archived. Living Room v001 is CLEAR for critique per Sam's color review.

---

## School Hallway v003 — Figure-Ground Separation Pass

**Output:** `output/backgrounds/environments/LTG_ENV_school_hallway_v003.png`
**Generator:** `output/tools/LTG_TOOL_bg_school_hallway_v003.py`

### Problem Identified (Takeshi Murakami silhouette notes)

v002 had a critical figure-ground failure for Cosmo:
- `LOCKER_LAV = (168,155,191)` was **exactly identical** to Cosmo's Dusty Lavender cardigan (RW-08 = #A89BBF = RGB 168,155,191). Character would be invisible against lavender lockers.
- `LOCKER_SAGE = (122,154,122)` was within 4 RGB values of Cosmo's sage shirt stripe (~124,158,126). Near-identical value.

With Cosmo's already-documented silhouette collapse (SKEPTICAL arms disappear behind torso, per Takeshi C15), any additional background-character merge compounds a production-level problem.

### Fixes Applied

1. **LOCKER_LAV remap**: `(168,155,191)` → `(216,208,190)` warm cream-off-white. Average value lifted from ~171 to ~205. Delta from Cosmo cardigan: ~34 value units.
2. **LOCKER_SAGE remap**: `(122,154,122)` → `(154,178,148)` lighter warm sage. Average value lifted from ~133 to ~160. Delta from Cosmo sage stripe: ~24 value units.
3. **Character-ground value band**: Subtle Shadow Plum (RW-09, alpha 22) overlay on both walls in the lower near-section character zone (first 35% of perspective depth, floor to 55% wall height). Darkens backing behind where standing characters are composited without reading as a visual shadow to casual viewers.
4. **Value floor anchors**: Added NEAR_BLACK_WARM (20,12,8) deep shadow at floor/wall junctions, locker base crevices, and far corner convergence zones. Required to pass QA value floor check.
5. **SUNLIT_AMBER correction**: Window light shaft color corrected from (232,201,90) to canonical RW-03 (212,146,58) to reduce hue drift.

### QA Results

```
v002 QA:  value range FAIL (min=45, max=237) | warm/cool PASS (76.2) | color fidelity WARN | GRADE: WARN
v003 QA:  value range PASS (min=19, max=237) | warm/cool PASS (77.3) | color fidelity WARN | GRADE: WARN
```

Color fidelity WARN is a pre-existing issue (SUNLIT_AMBER hue drift from warm floor pixel composites). This same issue was flagged across all environments in Critique 14 — not introduced by v003.

**Net improvement over v002**: value range FAIL resolved; figure-ground separation significantly improved.

---

## Ideabox

Submitted: `ideabox/20260329_hana_okonkwo_costume_bg_clash_lint.md`

Idea: character-background color clash detector tool — auto-flags costume-vs-background color conflicts before assets are generated.

---

## Notes for Compositor

When placing Cosmo in the school hallway:
- Lavender lockers are now distinctly **lighter** than his cardigan (value ~205 vs ~171). Cardigan reads as figure, lockers as ground.
- Sage lockers are now distinctly **lighter** than his shirt stripes (value ~160 vs ~136). Shirt reads as figure.
- Character-ground band provides additional darkening of near-wall zone.
- Cosmo's blue-black hair (avg value ~27) will read cleanly against all locker fills.
- Value range confirmed: deep shadows at floor/wall junctions (min=19) provide visual anchoring for standing figures.

Hana Okonkwo
Environment & Background Artist
