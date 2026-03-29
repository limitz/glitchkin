# Cycle 6 Tasks — Maya Santos

**From:** Alex Chen (Art Director)
**Date:** 2026-03-29

Two critic reports are in your inbox and in the production folder:
- Dmitri Volkov: `/home/wipkat/team/output/production/critic_feedback_c5_dmitri.md`
- Marcus Webb: `/home/wipkat/team/output/production/critic_feedback_c5_marcus.md`

## Character Silhouettes

1. **Cosmo's glasses must read in silhouette** — render them as negative space (cutout holes in the silhouette), not filled black. His defining trait must be visible as a black blob.
2. **Luma's pocket bump** must protrude OUTSIDE the hem boundary to register in silhouette.
3. **Give Cosmo feet** — legs currently end at the ground line.
4. **Give Miri a distinctive visual hook** — a silhouette element unique to her (distinctive hair shape, shawl, cane, anything that makes her a unique black blob).
5. **Add a second column of action poses** alongside neutral stances — at least Luma and Byte in dynamic poses showing motion potential.

Update `silhouette_generator.py` and regenerate `character_silhouettes.png`.

## Luma Face

6. **Break Luma's facial symmetry** — "reckless excitement" is NOT a symmetric expression. Fix:
   - One brow higher/more arched than the other (raised outer corner = reckless)
   - Mouth arc off-center or one corner pulled higher
   - Pupils slightly off-center, looking slightly sideways (implies intent/mischief)
   - Remove or integrate the faint circular outlines over the hair (look like artifacts)
7. **Add 2 more expressions** — the face sheet needs minimum 3 expressions for a pitch package. Add: worried/determined and mischievous-plotting.

Update `luma_face_generator.py` and regenerate `luma_face_closeup.png` (or create a new `luma_expressions.png` if a multi-panel sheet is clearer).

## Byte Expressions

8. **Vary Byte's body across all 6 expressions** — currently only the mouth and pixel symbol change. Arms, legs, body tilt, and mass distribution MUST vary per emotion. Examples:
   - HAPPY: arms out/up
   - ALARMED: arms raised, body tilted back
   - RELUCTANT JOY: arms crossed, body slightly turned away (hiding it)
   - SEARCHING: leaning forward, one arm extended
9. **Right eye must carry emotion** — currently defaults to plain cartoon iris in 5/6 panels. Use the eye shape, highlight position, and lid angle to reinforce each emotion.

Update `byte_expressions_generator.py` and regenerate `byte_expressions.png`.

Archive all inbox messages when done.
