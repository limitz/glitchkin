# Maya Santos — Memory

## Cycle 57 — Turnaround arm/torso/face fixes — COMPLETE

### Task: Fix arms, torso width, nose/mouth in side and 3/4 views (human feedback)

**Fixes applied to `LTG_TOOL_char_luma.py` v1.2.0:**

**Torso width (foreshortening):**
- Side view: `sh_w` → `head_r * 0.50` (was 0.80), `w_bot` → `head_r * 0.40` (was 0.55)
- 3/4 view: `sh_w` → `head_r * 0.70` (was 0.88), `w_bot` → `head_r * 0.48` (was 0.58)
- Side-L: `sh_w` → `head_r * 0.50` (was 0.80), `w_bot` → `head_r * 0.40` (was 0.55)
- Front view unchanged (sh_w=0.95, w_bot=0.62)

**Arms (side and 3/4 views):**
- Replaced `_draw_arms()` dispatch in both `_draw_luma_on_context` (side) and
  `_draw_luma_threequarter` with inline arm drawing (same pattern as side-L)
- Side view: near arm (+rs_pt, forward) and far arm (+ls_pt, back) hang
  naturally at hip/waist height — shoulder+30s+28s descent = hand near hip
- 3/4 view: near arm (rs_pt) prominent, far arm (ls_pt) slightly smaller/behind
- Side-L arm code unchanged (was already correct)

**Face features (side view):**
- Nose: `nose_x_base` → `head_rx * 0.94` (was 0.82) — anchored AT face edge
  so bump protrudes clearly outside head oval
- Mouth: `mouth_x_base` → `head_rx * 0.62` (was 0.30) — moved near face edge

**Deliverables:**
- `LTG_TOOL_char_luma.py` — updated in-place (v1.2.0)
- `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png` regenerated

**Test:** char_module_test PASS (7/7 expressions), all three views render cleanly.

**Completion message sent to Producer inbox.**

## Cycle 56 — Leg centering fix — COMPLETE
- `_draw_luma_on_context`, `_draw_luma_threequarter`, `_draw_luma_side_l`: all legs at hip_cx
- Hip bridge `hip_bw = leg_w_top * 1.4`

## Tools Owned (active)
- LTG_TOOL_char_luma.py v1.2.0 (C57)
- LTG_TOOL_char_miri.py v1.0.0 (C53)
- LTG_TOOL_luma_turnaround.py v007 (C55)
- (full list in SKILLS.md)

## Next Cycle Priorities
- Migrate luma_cairo_expressions.py to import from char_luma.py v1.2.0
- Cosmo expression rebuild
- Run face gate on side/side-L profile views
