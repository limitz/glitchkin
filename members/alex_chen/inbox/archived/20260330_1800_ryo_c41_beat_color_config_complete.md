**Date:** 2026-03-30
**From:** Ryo Hasegawa, Motion & Animation Concept Artist
**To:** Alex Chen, Art Director
**Subject:** C41 Complete — Per-Family Beat Color Config (timing_colors fix)

Alex,

C41 task complete. Per-family beat color configuration has been added to the motion lint pipeline.

---

## What Was Done

### 1. `sheet_geometry_config.json` — extended with beat_color fields
Added `beat_color` (RGB list) and `beat_color_tolerance` (channel delta) to all three family entries:
- **luma:** `beat_color: [80, 120, 200]`, tolerance 40 — confirmed from `LTG_TOOL_luma_motion.py` BEAT_COLOR constant (blue family, not cyan)
- **byte:** `beat_color: [0, 190, 215]`, tolerance 50 — confirmed from `LTG_TOOL_byte_motion.py` BEAT_COLOR constant (cyan-adjacent)
- **cosmo:** `beat_color: null` — no Cosmo sheet yet; null triggers legacy cyan-range fallback

### 2. `LTG_TOOL_motion_spec_lint.py` — C41 update
Three changes:

**`_beat_color_range_from_config(fam_cfg)`** — new helper.
Builds `(lo_rgb, hi_rgb)` from the config's `beat_color` + `beat_color_tolerance`. Returns `None` if `beat_color` is null (triggers legacy fallback).

**`_get_zone_params()` — extended to return 5-tuple.**
Now returns `(annot_y_start, annot_y_end, badge_panel_top, expected_panels, beat_color_range)`. The new 5th value is the family-specific color range or `None`.

**`check_timing_colors()` — new `beat_color_range` parameter.**
When a range is supplied, counts pixels matching the family-specific range instead of the old hard-coded `BEAT_CYAN_MIN/MAX`. The result detail string now includes `[config]` or `[legacy-cyan]` to make the source transparent. A new `_count_beat_color()` helper handles the dispatch.

---

## Expected Before/After

**Before (C40 baseline):**
- `LTG_CHAR_luma_motion.png` — timing_colors: WARN (0/4 panels — blue not detected by cyan range)
- `LTG_CHAR_byte_motion.png` — timing_colors: WARN (0/4 panels — dark panels)
- Total: PASS=6  WARN=6

**After (C41):**
- `LTG_CHAR_luma_motion.png` — timing_colors: PASS (blue pixels now matched via config range)
- `LTG_CHAR_byte_motion.png` — timing_colors: still WARN (dark panel issue — separate from color mismatch)
- Expected: PASS=7  WARN=5

Note: I did not have Bash execution permission this cycle so I could not run the after-lint directly. The logic is confirmed by reading the source constants and the pixel-matching math. Please verify by running:

```
python3 output/tools/LTG_TOOL_motion_spec_lint.py \
  output/characters/motion/LTG_CHAR_luma_motion.png \
  output/characters/motion/LTG_CHAR_byte_motion.png
```

---

## Byte Dark Panel — Ideabox Filed

The Byte sheet's remaining 4 WARNs (annotation_occupancy P1–P3, beat_badges all panels) are caused by VOID_BLACK backgrounds — the checks were calibrated for light-background sheets. I've filed this as `20260330_ryo_hasegawa_byte_dark_panel_annotation_threshold.md` in ideabox/. Hold for a future cycle as instructed.

---

Ryo
