# Cycle 8 Character Design — Complete
**Date:** 2026-03-29 20:00
**From:** Maya Santos, Character Designer
**To:** Alex Chen, Art Director

---

Cycle 8 character design work is complete. All Dmitri + Marcus priority mandates addressed.

## Deliverables

**silhouette_generator.py** — Miri complete visual identity redesign:
- **MIRI-A:** Tall oval bun + V-pair chopstick spikes + wide inverted-flare cardigan + soldering iron. Communicates "maker grandmother" at squint distance.
- **MIRI-B:** Wide rounded side-puffs (distinct from Luma's vertical cloud) + tech apron with circuit-board pocket (NEG_SPACE dot grid). Communicates "homey warmth + circuits."
- Both variants added as columns 4 and 5 in the silhouette sheet for side-by-side comparison.

**byte_expressions_generator.py:**
- GRUMPY is now confrontational: `body_tilt=-8` (forward lean), `arm_l_dy=-6, arm_r_dy=-10` (raised/asymmetric), `arm_x_scale=1.1` (wide stance). Was previously reading as defeated.
- Byte body is now **OVAL** (ellipse) throughout the expression sheet, matching `style_frame_01_rendered.py`. Chamfered-box polygon retired. Choice documented in code.

**luma_face_generator.py:**
- WORRIED/DETERMINED: 8px brow height differential (left outer at -38, right at -30). 4px was too subtle for pitch-deck distance.
- Collar is now a **rotated arc** (rotation matrix on polygon points), not an x-offset. Each expression has its own tilt angle (8° excitement, 2° worried, -5° mischief).

## Outputs (all verified)
- `/home/wipkat/team/output/characters/main/silhouettes/character_silhouettes.png`
- `/home/wipkat/team/output/characters/main/byte_expressions.png`
- `/home/wipkat/team/output/characters/main/luma_expressions.png`
- `/home/wipkat/team/output/characters/main/luma_face_closeup.png`

Full SOW: `/home/wipkat/team/output/production/statement_of_work_cycle8.md`

---

*Maya Santos*
