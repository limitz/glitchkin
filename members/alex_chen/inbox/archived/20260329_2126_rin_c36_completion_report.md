**Date:** 2026-03-29 21:26
**From:** Rin Yamamoto
**To:** Alex Chen
**Subject:** C36 Completion Report — SF02 v008 + Proportion Audit v002

Hi Alex,

C36 work complete. Two tasks delivered:

---

## 1. SF02 v008 — Fill Light Direction Fix (P1)

**File:** `output/tools/LTG_TOOL_style_frame_02_glitch_storm_v008.py`
**Output:** `output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v008.png` (1280×720)

Integrated Jordan Reed's C35 fill light fix (Sven Halvorsen C14 critique):

- **Fix 1 — Direction corrected:** Source now UPPER-RIGHT of each character
  (`fill_src_x = char_cx + int(char_h * 0.5)`, `fill_src_y = char_cy - int(char_h * 0.8)`)
  matching the storm crack position at upper-right canvas. Was incorrectly lower-left in v006/v007.
- **Fix 2 — Per-character silhouette mask:** HOT_MAGENTA gradient applied ONLY within
  character pixel zones via `_make_char_silhouette_mask_1080()` + `ImageChops.multiply()`.
  No longer bleeds onto background.
- **Alpha max 35** (was 40) — direct upper-right source is harder/cleaner than a bounce.
- **char_cx from geometry constants** — luma=W*0.45, byte=W*0.28, cosmo=W*0.62.
  No `get_char_bbox()` on full frame.

**Implementation note:** Jordan's fix module (`LTG_TOOL_sf02_fill_light_fix_c35.py`) has
hardcoded `W, H = 1280, 720` and cannot be called directly on a 1920×1080 image (PIL
alpha_composite raises "images do not match"). The algorithm was inlined at 1920×1080.
Submitted an ideabox idea to refactor the module to accept canvas_w/canvas_h parameters.

**QA result:** render_qa WARN (warm/cool separation 6.5) — expected for this intentionally
cold scene. Value range PASS (0–255), silhouette distinct, line weight PASS, color fidelity PASS.

All C35 fixes (Luma face, torso lean, hair stream) carried forward unchanged.

---

## 2. Proportion Audit v002 — Asymmetric Eye Detection

**File:** `output/tools/LTG_TOOL_proportion_audit_v002.py`
**Report:** `output/production/proportion_audit_c36.md`

New capability (C36 actioned ideabox):
- Detects `eye_r_left` / `eye_r_right = max(N, int(head_r * M))` patterns
- Reports both L/R ratios separately
- Issues ASYM-WARN if either eye is outside canonical spec (0.21–0.23) or if L/R diff > 10%
- Intentional asymmetry → ASYM-WARN (not FAIL), so sprint-face generators are not blocked

**C36 audit results (20 files scanned):**
- PASS: 3 (SF01 v004/v005, SF04 v004)
- ASYM-WARN: 2 (SF02 v007/v008 — eye_r_left=0.26, eye_r_right=0.17, intentional asymmetry)
- WARN: 1 (SF01 v003 — pre-C30 legacy, superseded)
- FAIL: 0
- N/A: 14 (no eyes: sprint without face, pixel-art, no Luma)

The ASYM-WARN for SF02 v007/v008 is expected — the FOCUSED DETERMINATION expression
uses asymmetric eyes by design. Flagging is informational for your review.

---

## README.md Updated
`output/tools/README.md` updated with entries for v008 and proportion_audit_v002.
Last-updated header updated.

## Ideabox
Submitted `20260330_rin_yamamoto_fill_light_resolution_adapter.md` — proposal to
refactor fix modules to accept canvas_w/canvas_h params for multi-resolution support.

Rin
