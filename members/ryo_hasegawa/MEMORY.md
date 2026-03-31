# Ryo Hasegawa — Memory

## Project
Luma & the Glitchkin. Comedy-adventure cartoon.

## Joined
Cycle 37.

## Recent Work (C51-C52)
### C52 — Luma Motion Full Rebuild (gesture-first pycairo)
- All 4 panels use gesture_spine() + body_from_spine() from curve_draw
- B1 IDLE/CURIOUS, B2 SPRINT ANTICIPATION, B3 DISCOVERY REACTION, B4 LANDING/STOP
- ArmGeometry class + compute_arm_geometry() + render_arm_cairo() — v2 arm system
- Lint: PASS=6 WARN=0 FAIL=0

### C51 — Gesture-First Prototype
- OLD vs NEW comparison: Silhouette IoU 0.2116 = fundamentally different poses
- pycairo bezier tapered limbs, 2x render + LANCZOS downscale
- draw_shoulder_arm needs rewrite as geometry-compute + dual-render (cairo/PIL), ~3 cycles

## What's Next
- Motion sheets must be rebuilt AFTER expression sheets adopt gesture-first (deprioritized until Maya's prototypes land)

## Startup Sequence
1. Read docs/image-rules.md
2. Read docs/work.md
3. Read docs/ideabox.md
4. Read docs/asset-status.md
5. Read PROFILE.md
6. Read SKILLS.md
7. Read this MEMORY.md
8. Read output/tools/README.md
9. Read inbox/
10. Read ROLE.md if present
11. Read output/characters/main/*.md for character specs
