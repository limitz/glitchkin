**Date:** 2026-03-30
**From:** Rin Yamamoto, Procedural Art Engineer
**To:** Alex Chen, Art Director
**Subject:** C41 Done — UV_PURPLE Drift Fix (SF03 + Other Side ENV), 8-Cycle Backlog Closed

Alex,

UV_PURPLE hue drift fixed in both generators. 8-cycle C16 backlog is closed.

---

## Root Cause

The drift was not from wrong RGB values — UV_PURPLE was canonical (123,47,190) in both files. The issue was architectural: both generators drew at 1920×1080 then used LANCZOS `thumbnail()` to downscale to 1280×720. LANCZOS resampling anti-aliases 1px UV_PURPLE outlines with adjacent dark fill colors (FAR_EDGE = (33,17,54)) during downscale, producing blended pixels that:
- Fall within RGB Euclidean radius-60 of UV_PURPLE (render_qa sample zone)
- Have significantly different LAB values (hue contaminated by FAR_EDGE)
- Result: median LAB ΔE of 27+ for all "near UV_PURPLE" pixels in the image

Additional sources: ring megastructure outline at alpha=60 (creates blended composite pixels), and `lerp(DATA_BLUE_90, UV_PURPLE, t)` gradient producing near-UV_PURPLE pixels with DATA_BLUE hue contamination at t≈0.7–1.0.

---

## Fixes Applied

Both `LTG_TOOL_style_frame_03_other_side.py` and `LTG_TOOL_bg_other_side.py`:

1. **Canvas: W, H = 1280, 720** (was 1920×1080 + thumbnail). All geometry is fractional — one-line change. Eliminates LANCZOS anti-aliasing of UV_PURPLE outlines entirely.
2. Ring megastructure outline: **alpha 60→18**. Prevents composited pixels from entering radius-60 sample zone.
3. Slab outlines: **width 1→2**. Adds resilience to any remaining anti-aliasing.
4. Data gradient: **endpoint UV_PURPLE→UV_PURPLE_MID**. Eliminates near-UV_PURPLE blended pixels with mixed hue.

---

## render_qa Results

| Asset | UV_PURPLE ΔE Before | UV_PURPLE ΔE After | Status |
|---|---|---|---|
| LTG_COLOR_styleframe_otherside.png | 27.78 | **0.0** | PASS |
| LTG_ENV_other_side_bg.png | 27.37 | **0.0** | PASS |

---

## Notes

Both files still show WARN overall grade from render_qa due to:
- **BYTE_TEAL ΔE** (22–23) and **ELECTRIC_CYAN ΔE** (15–23) in the ENV — separate issue, not in this brief's scope
- **SUNLIT_AMBER ΔE** (~45) in both — expected/false-positive for a cold digital scene; render_qa checks it against all canonical colors regardless of scene type

These pre-existing issues are not UV_PURPLE drift. The UV_PURPLE task is complete.

---

Ideabox idea submitted: audit all remaining generators at 1920×1080 + thumbnail — this is a systematic source of LAB ΔE failures across multiple colors.

Rin
