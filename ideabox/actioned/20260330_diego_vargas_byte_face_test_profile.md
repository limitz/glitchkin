**Author:** Diego Vargas
**Cycle:** 43
**Date:** 2026-03-30
**Idea:** Add a Byte character profile to `LTG_TOOL_character_face_test.py` so `--char byte` works. Currently the tool only supports `luma`, `cosmo`, `miri`. Byte's face spec is well-established (cracked eye / normal eye geometry, expression states documented in byte.md and the expression sheet generator). A Byte face test would check: normal eye aperture (full-open vs squint lid), iris offset direction (sight-line rule), cracked eye processing dot divergence angle, mouth shape vs expression type. This would close the gap blocking me from running the face gate on P07 and P09 as required by Lee Tanaka's staging brief.
**Benefits:** Diego Vargas gets a runnable face gate for Byte panels. Lee Tanaka gets confidence that sight-line and expression geometry is machine-checked before delivery. Closes a tooling gap that affects every storyboard panel featuring Byte at any scale.
