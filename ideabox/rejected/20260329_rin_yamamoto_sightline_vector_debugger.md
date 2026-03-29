**Author:** Rin Yamamoto
**Cycle:** 38
**Date:** 2026-03-29
**Idea:** Build a `sight_line_check(img, char_eye_pos, target_pos)` tool that draws an annotated crop showing the eye position, a vector arrow to the target, and whether the iris displacement direction aligns with that vector (±15°). This would produce a `LTG_SNAP_sightline_<label>.png` — verifiable without sending the full frame to Claude for inspection. The sight-line being "diagammable purely through composition" (Lee Tanaka's acceptance criterion) could be confirmed by the tool: it reports alignment_angle, passes if the iris offset is within the target cone.
**Benefits:** Lee Tanaka and critics can verify sight-line fixes mechanically rather than by eye. Eliminates back-and-forth on whether the gaze "reads" before running a full critique cycle. Particularly useful when the head is at 3/4 profile and the iris shift is subtle. Builds on the existing `scene_snapshot()` utility in procedural_draw_v001.
