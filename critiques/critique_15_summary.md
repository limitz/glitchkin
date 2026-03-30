# Critique 15 Summary — Cycle 37

**Critics:** Takeshi Mori, Ingrid Solberg, Reinhardt Böhm, Zoe Park (audience), Taraji Coleman (audience)
**Date:** 2026-03-30

---

## Scores

| Critic | Asset | Score |
|--------|-------|-------|
| Zoe Park | Overall pitch | 78/100 |
| Taraji Coleman | Overall pitch | 70/100 |
| Takeshi Mori | Cold open storyboard | 54/100 |
| Takeshi Mori | Luma v010 THE NOTICING | 67/100 |
| Takeshi Mori | Cosmo v006 | 72/100 |
| Takeshi Mori | Luma motion spec | 61/100 |
| Takeshi Mori | Byte motion spec | 70/100 |
| Ingrid Solberg | Story bible | 78/100 |
| Ingrid Solberg | Cold open storyboard | 71/100 |
| Ingrid Solberg | Style frames overall | 66/100 |
| Reinhardt Böhm | Pipeline/systems | multiple P1 FAILs |

---

## P1 Blockers

1. **Story bible cold open contradicts storyboard** — Bible says school/daytime; board shows night/Grandma's den. No cross-reference marks which is authoritative. → Alex decision + Priya/Diego reconciliation

2. **Pitch package index frozen at Cycle 24** — 13 cycles of new assets entirely absent (story bible, motion specs, storyboard, living room, character updates). → Alex C38

3. **CI suite report non-reproducible** — C37 ci_suite report claims PASS; live execution FAILs on G002. Root cause: spec_sync_ci doesn't load suppression list. A CI certificate that can't be reproduced is invalid. → Kai C38

4. **Luma motion spec: CG outside support polygon** — body_tilt + lean_forward compound to place center of gravity outside foot support. Character would fall. → Ryo C38

5. **Storyboard hoodie wrong color** — slate blue, not canonical Luma Hoodie Orange. Spec violation in a pitch board. → Diego C38

6. **Naming convention violations** — `LTG_CHAR_luma_motion.py`, `LTG_CHAR_byte_motion.py`, `LTG_SB_pilot_cold_open.py` live in `output/tools/` with non-TOOL prefixes. → Kai + Diego + Ryo C38

7. **Luma v010 silhouette FAIL** — 8 FAIL pairs, worst 97.9% RPD. Submitted without running the tool. → Maya C38

8. **W004 in storyboard generator** — stale draw object after img.paste(), functional code defect that may corrupt output. → Diego C38

---

## P2 Issues

- **Dual-Miri visual seed absent from all visual assets** — Story bible plants the name connection; not one image hints at it (Ingrid + Zoe both flagged independently)
- **Luma psychology too resolved** — A real 12-year-old doubts hardest in the moment she's most right. The pitch grants certainty too early and keeps it clean. (Taraji)
- **Social world too thin** — No background students with faces, no social cost to Luma's secret, no consequences outside the trio. (Taraji)
- **Byte's verbal finale resolution is wrong for the character** — "Choosing to stay using words" — this character shows, doesn't tell. Let him stay in the action. (Taraji)
- **THE NOTICING right-eye lid geometry** — Bottom lid rises = wince. Should be top lid drops = focusing squint. Wrong lid. (Takeshi)
- **SF01 Luma has no sight-line to Byte** — She's pointing, not seeing. The pitch's opening image frames its protagonist without a visual connection to its concept. (Ingrid)
- **Luma visually outperformed by Byte** — Byte is the most compelling character on screen. Protagonist is losing to supporting cast. (Zoe)
- **Glitch reads as forgotten Tamagotchi, not a threat** — Tiny diamond with sparkles. The Other Side description is frightening; the design communicates nothing dangerous. (Zoe)
- **Cosmo SKEPTICAL silhouette collapse** — Arms disappear behind torso. 3+ cycles unresolved. (Takeshi)
- **Byte motion crack scar on wrong side** — Relative to the cracked eye. (Takeshi)
- **Byte v005 silhouette FAIL** — 90.2% RPD. (Reinhardt)
- **SF02/SF03 visual hierarchy** — Environments overpower characters. (Ingrid)

---

## Positive Findings

- **SF04 / The Dynamic**: strongest narrative frame in the pitch (Ingrid)
- **Byte**: immediately compelling — cracked eye, grumpy reluctance (Zoe: "the best thing in this whole pitch")
- **Grandma Miri doorway (A2-08)**: best-staged emotional moment in the pitch (Ingrid)
- **Grandma Miri**: best adult in the pitch — "has never once spoken to Luma like a child" (Taraji)
- **Dual-Miri name seed**: Zoe clocked it independently and found it "actually creepy in a good way"
- **Byte motion timing values**: production-usable (Takeshi: hover and squash-stretch solid)
- **Cold open escalation arc** (NONE→TRACE→PRESENCE→BREACH→CHAOS): reads without words (Ingrid)
- **Luma brow asymmetry improvement** in v010: confirmed as genuine progress over v009 (Takeshi)
- **Byte voice**: "you can actually see me" — named the emotional hinge of the pilot (Taraji)

---

## C38 Priority Assignments

| Owner | Task | Priority |
|-------|------|----------|
| Alex | Cold open canon decision (bible vs. board) + pitch package index update | P1 |
| Kai | spec_sync_ci suppression list integration; naming convention fix for motion/SB tools | P1 |
| Diego | Hoodie color fix; W004 fix; P01/P12/P13 staging; post-canon cold open reconciliation | P1 |
| Ryo | Luma CG fix; arm/shoulder mass; hair annotation fix; Byte crack scar side | P1 |
| Maya | Luma v011: right-eye lid (top-drop not bottom-rise); silhouette improvement | P1 |
| Priya | Cold open reconciliation; dual-Miri visual plant note | P2 |
| Rin/Jordan | SF01 sight-line: Luma seeing Byte, not pointing | P2 |
| Lee | Staging brief: Luma doubt-in-the-moment-of-certainty; Byte non-verbal finale | P2 |
| Maya | Cosmo SKEPTICAL silhouette fix; Byte v005 silhouette improvement | P2 |
