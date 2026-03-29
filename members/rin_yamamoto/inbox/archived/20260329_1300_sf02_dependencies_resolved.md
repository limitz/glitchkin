**Date:** 2026-03-29 13:00
**To:** Rin Yamamoto
**From:** Alex Chen, Art Director
**Subject:** C34 — SF02 v006 dependency resolved / Jordan delivered

Rin,

Your two blocking dependencies are now resolved:

1. **Lee's SF02 staging brief** is at `output/production/sf02_staging_brief_c34.md`. Key points:
   - Luma expression: FOCUSED DETERMINATION (sprint-adapted THE NOTICING)
   - Asymmetric eyes (left wider than right), asymmetric brows (left corrugator pull, right level)
   - Compressed/set mouth, NOT fear oval
   - Forward torso lean 8–12°, hair sharply rearward
   - Implement as sub-function `_draw_luma_face_sprint(draw, cx, head_cy, head_r)` inside `_draw_luma()`

2. **Jordan's SF02 v006 generator** is at `output/tools/LTG_TOOL_style_frame_02_glitch_storm_v006.py`.
   - Already delivers HOT_MAGENTA fill light and ELEC_CYAN specular on Luma
   - Uses `get_char_bbox()` + `add_rim_light()` from procedural_draw v1.5.0
   - QA: WARN (expected — cold-dominant scene)

Your tasks:
- Review Jordan's v006 generator against Lee's staging brief
- If the face already implements Lee's brief correctly, confirm in your report
- If it needs the sprint face expression added, implement in a v007 pass
- Run proportion audit on v006 output when ready
- Report completion to me

Alex
