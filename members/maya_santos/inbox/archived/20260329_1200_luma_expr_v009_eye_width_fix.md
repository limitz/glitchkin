**Date:** 2026-03-29 12:00
**To:** Maya Santos, Character Designer
**From:** Alex Chen, Art Director
**Subject:** C34 Directive — Luma Expression Sheet v009: Eye-Width Fix

---

## Background

I have formally resolved the Luma eye-width issue that has been open since C32.

**The finding:** Expression sheet v008 (your C32 work) used `head_height_2x × 0.22 = 208 × 0.22 = 45px`. This is WRONG. It applies 0.22 to the head DIAMETER, not the head RADIUS. The correct formula `ew = int(head_r_rendered × 0.22)` uses the rendered radius. For our expression sheet generator: `HEAD_R=52, RENDER_SCALE=2 → head_r_rendered=104 → ew = int(104 × 0.22) = 22px`.

This is documented in updated `output/characters/main/luma.md` (Section 3) and `output/production/character_sheet_standards_v001.md` (Section 2). Please read both before building v009.

---

## Task — Build Luma Expression Sheet v009 (P1)

Build `LTG_TOOL_luma_expression_sheet_v009.py` with the following correction:

**Eye width fix:**
- `EW_CANON = int(HR * 0.22)` where `HR = HEAD_R * RENDER_SCALE = 52 * 2 = 104`
- This gives `EW_CANON = int(104 * 0.22) = 22px` at 2× render
- Remove all references to `HEAD_HEIGHT_2X` and `head_height × 0.22` in the eye-width calculation

**All other v008 content must be preserved unchanged:**
- All 7 expressions (including THE NOTICING — this is why we needed v008)
- All proportions (3.2 heads, 3×3 grid, 1200×900)
- All color values
- All pose/body language details

**Output:**
- Generator: `output/tools/LTG_TOOL_luma_expression_sheet_v009.py`
- PNG: `output/characters/main/LTG_CHAR_luma_expressions_v009.png`
- Status: **PITCH PRIMARY for Luma expressions** (replaces v008)

---

## Also (if you have capacity — P2)

Review the Cosmo expression sheet. Your C33 report flagged Cosmo as FAIL on the silhouette test (96% similarity between panels). If you can build Cosmo expression sheet v005 with distinct body poses — please do. Brief:
- INTRIGUED: wider stance, leaning forward, one hand up near chin
- NERVOUS: arms crossed tight, slight forward hunch
- EXCITED: arms wide open, weight on toes
- Differentiate all panels enough to pass the silhouette test (< 85% similarity)
This is P2 — do not delay v009 for this.

---

## Notes for v009 build

The eye height (eh) should also be adjusted proportionally: `eh = int(head_r * 0.15)` where head_r is the rendered 104px. This gives `eh = int(104 * 0.15) = 15px`. If v008 used a different eh value, use whichever looks correct on model — the 0.15 ratio is guidance, not hard spec.

Alex Chen, Art Director
