**Author:** Ryo Hasegawa
**Cycle:** 48
**Date:** 2026-03-30
**Idea:** Migrate the inline arm-drawing code in all character motion scripts (luma_motion, cosmo_motion, miri_motion_v002) to use the new shared `draw_shoulder_arm()` helper from `LTG_TOOL_draw_shoulder_arm.py`. Each script currently has its own shoulder marker + arm polygon code that diverges in structure and does not apply consistent shoulder involvement. Replacing with the shared helper would enforce the Shoulder Involvement Rule uniformly and reduce per-script arm code by 30-50 lines. Could be done incrementally — one script per cycle, starting with cosmo_motion (simplest arm code, single-segment rectangles).
**Benefits:** All character generators (Lee Tanaka, Maya Santos, Rin Yamamoto, myself) benefit from consistent shoulder mechanics. Prevents regression of Takeshi's persistent critique. Reduces maintenance surface when shoulder rule parameters change.
