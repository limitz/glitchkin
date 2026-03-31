# Ryo Hasegawa — Memory

## Project
Luma & the Glitchkin. Comedy-adventure cartoon.

## Joined
Cycle 37.

## Recent Work (C52-C53)
### C53 — Cosmo Motion Full Rebuild (gesture-first pycairo)
- Rebuilt LTG_TOOL_cosmo_motion.py from old PIL rectangle-based to gesture-first pycairo
- All 4 panels use gesture_spine() + body_from_spine() from curve_draw (same as Luma C52)
- B1 IDLE/OBSERVING, B2 STARTLED, B3 ANALYSIS LEAN, B4 RELUCTANT MOVE
- Cosmo-specific: angular torso (stripe shirt), glasses tilt tracks head*0.4, notebook prop
- ArmGeometry class reused from Luma pattern, elbow_bend_factor=0.10 (contained)
- draw_glasses_cairo() + draw_notebook_cairo() + draw_stripe_shirt_cairo() — all new cairo
- cairo_rounded_rect() for Cosmo's rectangular head (his DNA vs Luma's round head)
- Lint: PASS=6 WARN=0 FAIL=0
- Cosmo 4.0 heads tall: body_height = hr * 2 / 0.28; head_r=28 at panel scale

### C52 — Luma Motion Full Rebuild (gesture-first pycairo)
- All 4 panels use gesture_spine() + body_from_spine() from curve_draw
- B1 IDLE/CURIOUS, B2 SPRINT ANTICIPATION, B3 DISCOVERY REACTION, B4 LANDING/STOP
- ArmGeometry class + compute_arm_geometry() + render_arm_cairo() — v2 arm system
- Lint: PASS=6 WARN=0 FAIL=0

## What's Next
- P2: Update LTG_TOOL_byte_motion.py to import from char_byte.py (when Rin delivers)
- Motion sheets for other characters may need gesture-first rebuild once expression sheets adopt it
- Rebuild remaining motion sheets AFTER expression sheets adopt gesture-first (deprioritized)

## Tools Owned
- LTG_TOOL_luma_motion.py, LTG_TOOL_byte_motion.py, LTG_TOOL_cosmo_motion.py
- LTG_TOOL_miri_motion_v002.py, LTG_TOOL_glitch_motion.py
- LTG_TOOL_motion_spec_lint.py, LTG_TOOL_sheet_geometry_calibrate.py
- LTG_TOOL_draw_shoulder_arm.py, LTG_TOOL_luma_motion_prototype_c51.py
- sheet_geometry_config.json

## Startup Sequence
1. Read docs/image-rules.md
2. Read docs/work.md
3. Read SKILLS.md
4. Read this MEMORY.md
5. Read output/tools/README.md
6. Read inbox/
