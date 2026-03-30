**Date:** 2026-03-30
**From:** Jordan Reed
**Subject:** C49 Complete — sightline_validator v2.0.0 pixel detection mode

## Deliverables
- `LTG_TOOL_sightline_validator.py` v2.0.0 — pixel detection mode for rendered PNGs
- Ideabox: `20260330_jordan_reed_high_res_gaze_crop_mode.md`
- README.md updated (C49 Jordan Reed section added)
- Inbox archived

## New APIs
- `detect_eyes_from_png(image_path, search_box, ...)` — detects eye-white regions and pupil positions using color matching + morphological clustering (SciPy ndimage)
- `validate_sightline_from_png(image_path, target, search_box, ...)` — end-to-end pixel gaze validation
- `_pair_eyes(eyes)` — pairs detected eyes into left/right by horizontal alignment
- Confidence rating: HIGH (eye_w >= 30px), LOW (15-30px), VERY_LOW (<15px)
- CLI: `--png PATH --target TX TY`, `--pixel-test`, `--self-test`

## Test Results

### Construction mode (v1.0.0 — unchanged)
All 5 self-tests PASS. SF01 v007: 2.3 deg angular error (PASS).

### Pixel detection mode (v2.0.0 — new)
**SF01 v007 test:**
- Eye detection: 2 eyes found at (413, 428) and (436, 430) — matches construction within 2px
- Confidence: LOW (avg eye width 15px)
- Gaze angle: -96 deg (pixel) vs -21 deg (construction) — 75 deg delta

### Accuracy Assessment
**Pixel detection cannot reliably determine gaze DIRECTION at style-frame scale.**

Root cause: At 1280x720 with head_r ~44px, each eye is only 15px wide. The pupil shift (the signal we need to measure) is p(8) = 4px. This 4px offset is below the noise floor of pixel centroid estimation because:
1. The pupil dot (12px wide) fills most of the iris area — its centroid is dominated by the symmetric iris mass
2. Brow/lid outlines use the same dark colors (V=20-30) as the pupil — they contaminate any expanded search
3. Expression asymmetry (wonder/squint) creates sclera distribution biases that dwarf the gaze signal

**Pixel mode IS reliable for:**
- Eye presence detection (found/not found)
- Eye position estimation (within 2px of construction)
- Larger-scale renders where eye_w >= 30px (expression sheets, close-up panels)

**Recommendation:** Construction mode remains authoritative for gaze validation at style-frame scale. Pixel mode should be used for eye presence/position checks only. See ideabox for "gaze crop" proposal that would make pixel gaze validation viable.

## Diagnostic Files
- `output/production/sightline_pixel_debug_c49.py` — color sampling debug
- `output/production/sightline_pixel_debug2_c49.py` — sclera distribution analysis
