**Date:** 2026-03-30
**From:** Jordan Reed
**Subject:** C47 Completion — SF01 Sight-line Fix + CORRUPT_AMBER Detection Mode

## P1: SF01 Sight-line Fix (Ingrid Critique #10) — DONE

**Root cause:** pupil_shift was horizontal-only (dx=p(8), dy=0). Byte is at -20.7 degrees from Luma's eye midpoint (above-right of her). The horizontal-only shift made gaze read as "looking past" Byte to the right, not AT Byte.

**Fix:** pupil_shift now computed as a vector aimed from mid-eye to Byte target coordinates (both X and Y components). Same magnitude. `draw_luma_head_v006()` gains `byte_cy_target` parameter.

**Verification:**
- Sight-line diagnostic: PASS — 0.9px miss (threshold 15px), angular error 2.2 deg (was 20.7 deg)
- render_qa: warm/cool 17.4 PASS, value 14-242 PASS, GRADE: WARN (pre-existing baseline)
- color_verify: all 6 canonical PASS
- Face test gate: head_r=44px — not triggered; key expressions PASS

## P2: CORRUPT_AMBER Detection Mode — DONE

Added `detect_corrupt_amber()` to `LTG_TOOL_color_verify.py` (v3.0.0). Uses RGB Euclidean distance (radius 30) to find GL-07 pixels — cleanly excludes SUNLIT_AMBER which is ~50 away in RGB space.

**Classification:** sanctioned (within CRT box + composited V <= 0.45) vs violation (full-opacity or outside box).

**CLI:** `--corrupt-amber` flag + optional `--crt-box X0 Y0 X1 Y1`.

**Validation:** SF01 correctly flags 808 full-opacity portal outline pixels as violations. SF04 correctly detects 0 full-opacity GL-07 (fringe is at 15% alpha, composited too dim to match).

All existing self-tests PASS. API fully backward-compatible.

## Files Changed
- `output/tools/LTG_TOOL_styleframe_discovery.py` — v007 sight-line fix
- `output/tools/LTG_TOOL_color_verify.py` — v3.0.0 CORRUPT_AMBER detection
- `output/tools/README.md` — C47 updates section
- `output/production/sf01_sightline_debug_c47.py` — geometry verification script
- `output/production/LTG_SNAP_sightline_sf01_v007_c47.png` — sight-line diagnostic output
