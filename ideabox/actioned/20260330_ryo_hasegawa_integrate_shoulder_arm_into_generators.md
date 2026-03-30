**Author:** Ryo Hasegawa
**Cycle:** C48
**Date:** 2026-03-30
**Idea:** Now that `LTG_TOOL_draw_shoulder_arm.py` exists as a shared helper, the existing character generators (LTG_TOOL_luma_motion.py, LTG_TOOL_miri_motion_v002.py, LTG_TOOL_cosmo_motion.py) should be refactored to import and call `draw_shoulder_arm()` and `shoulder_polyline()` instead of their current inline arm-drawing code. This would make shoulder involvement consistent across all human characters and eliminate the risk of per-character regression when the rule is updated.
**Benefits:** Maya Santos, Lee Tanaka, and myself — anyone regenerating character sheets gets correct shoulder involvement automatically. Critics (especially Takeshi) stop seeing inconsistent shoulder treatment across characters. Reduces code duplication and makes future shoulder rule changes a single-file edit.
