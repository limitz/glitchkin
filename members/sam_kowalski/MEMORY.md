# Sam Kowalski — Memory

## Project
Luma & the Glitchkin. Comedy-adventure cartoon. Three worlds: Real World (warm), Glitch Layer (HOT_MAGENTA + ELECTRIC_CYAN), Other Side (cool, zero warm light).

## Recent Work (C53)
### C53
- Built `LTG_TOOL_char_cosmo.py` v1.0.0 — canonical modular Cosmo renderer
- Exports: `draw_cosmo(expression, pose, scale, facing, scene_lighting) -> (cairo.ImageSurface, geom)`
- 6 expressions: AWKWARD, WORRIED, SURPRISED, SKEPTICAL, DETERMINED, FRUSTRATED
- Gesture specs from Lee Tanaka's cosmo_gesture_spec_c52.md integrated as GESTURE_SPECS dict
- Angular body language: low bulge_frac (0.03) on torso polygon, visible joint breaks
- Glasses tilt = head_tilt * 0.4 (auto-computed when glasses_tilt=None)
- C47 shoulder involvement on all poses
- Visual hooks preserved: amplified cowlick (0.15 heads) + bridge tape
- Color enhancement via optional enhance_color param (uses enhance_from_cairo)
- WORRIED and DETERMINED offsets amplified beyond original spec to pass gesture lint
  - WORRIED: hip_shift 0->6, shoulder_offset 0->-8, head_offset -10->-22, torso_lean -4->-14
  - DETERMINED: hip_shift -8->-12, shoulder_offset 12->16, head_offset 8->12, torso_lean -14->-20
- All 6 expressions PASS gesture_line_lint (individual panel mode, --single)
- Grid-mode lint fails due to panel detection issue (not a renderer bug)
- Test sheet: output/characters/main/LTG_CHAR_cosmo_canonical_test.png

### C52
- Cosmo expression sheet v009 (pycairo + color enhancement pipeline)
- character_color_enhance.py v2.0.0: enhance_from_cairo() bridge
- colour-science IS INSTALLED (v0.4.1). Full deltaE2000 verification PENDING.

## Carry Forward
- deltaE2000 full asset verification run pending
- Grid-mode gesture lint panel detection issue — may need linter fix or sheet layout change
- Per-character color enhance presets (ideabox submitted prior cycle)
- ENV-06 not updated in SF02 v001 generator (low priority)

## Startup Sequence
1. Read docs/image-rules.md
2. Read docs/work.md
3. Read SKILLS.md
4. Read this MEMORY.md
5. Read output/tools/README.md
6. Read inbox/
