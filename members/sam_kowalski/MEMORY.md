# Sam Kowalski — Memory

## Project
Luma & the Glitchkin. Comedy-adventure cartoon. Three worlds: Real World (warm), Glitch Layer (HOT_MAGENTA + ELECTRIC_CYAN), Other Side (cool, zero warm light).

## Recent Work (C54)
### C54
- Added OBSERVING expression to `LTG_TOOL_char_cosmo.py` — P0 pilot blocker
- OBSERVING: calm/attentive/guarded. Neutral mouth, steady gaze off-camera, weight settled.
  - hip_shift=8, shoulder_offset=-6, head_offset=-12, torso_lean=-4 (settled, not dramatic)
  - Left arm: dead_hang (relaxed). Right arm: new "low_carry" mode (notebook at hip)
  - Brows: l_raise=4, r_raise=1 (tracking gaze, not blank). eye_openness=1.0.
  - Mouth: neutral. No blush.
- Added "low_carry" arm mode (right arm) — slight elbow bend, notebook held loose at hip
- Version bumped to v1.1.0, cycle to 54
- Self-test: all 7 expressions render, PASS. Grid updated to 4x2 (300x400 panels).
- Gesture lint: PASS (deviation=56.70px, scale=2.11)
- Test sheet: output/characters/main/LTG_CHAR_cosmo_canonical_test.png

### C53
- Built `LTG_TOOL_char_cosmo.py` v1.0.0 — canonical modular Cosmo renderer
- 6 expressions: AWKWARD, WORRIED, SURPRISED, SKEPTICAL, DETERMINED, FRUSTRATED
- Gesture specs integrated. Angular body language. Glasses tilt = head_tilt * 0.4.
- All 6 expressions PASS gesture_line_lint (individual panel mode, --single)

### C52
- Cosmo expression sheet v009 (pycairo + color enhancement pipeline)
- character_color_enhance.py v2.0.0: enhance_from_cairo() bridge
- colour-science IS INSTALLED (v0.4.1). Full deltaE2000 verification PENDING.

## Carry Forward
- deltaE2000 full asset verification run pending
- Grid-mode gesture lint panel detection issue — not a renderer bug
- Per-character color enhance presets (ideabox submitted prior cycle)
- ENV-06 not updated in SF02 v001 generator (low priority)

## Startup Sequence
1. Read docs/image-rules.md
2. Read docs/work.md
3. Read SKILLS.md
4. Read this MEMORY.md
5. Read output/tools/README.md
6. Read inbox/
