# Cycle 19 Background & Style Frame Deliverables — Jordan Reed

**Date:** 2026-03-29 24:00
**From:** Jordan Reed
**To:** Alex Chen
**Re:** Critique C9 Fix Pass — All 4 Tasks Complete

---

All four Critique C9 tasks are complete. Generators run clean, outputs saved.

---

## Task 1 — SF03 v003: CRITICAL Byte Body Fix ✓

**Generator:** `output/tools/LTG_TOOL_style_frame_03_other_side_v003.py`
**Output:** `output/color/style_frames/LTG_COLOR_styleframe_otherside_v003.png`

Fixes applied:
1. **BYTE_BODY = (0, 212, 232) GL-01b Byte Teal** — was (10,10,20) VOID BLACK. Byte was completely invisible against UV Purple ambient background. CRITICAL fix confirmed.
2. **Eye radius = max(15, h//5)** — was max(2, h//7) ≈ 10px. Both eyes now minimum 15px radius (30px diameter), clearly readable against dark background.
3. **Void Black diagonal slash REMOVED** from magenta eye — both eyes are now clean, unobstructed solid color fills.
All Cycle 16 carries: waterfall luminance, bridging element, right-side irregularity, Luma UV Purple hair rim.

---

## Task 2 — SF02 v004: Storefront + Warm Window Glow ✓

**Generator:** `output/tools/LTG_TOOL_style_frame_02_glitch_storm_v004.py`
**Output:** `output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v004.png`

Fixes applied:
1. **Damaged storefront window** (lower-right): replaced plain teal rectangle with:
   - Structural frame (steel/wood, dark) with 2 vertical + 1 horizontal divider creating 6 panes
   - 3 missing panes (open to dark interior), 3 surviving dirty glass panes
   - Crack lines radiating from 2 impact points (6-8 rays each with sub-branches)
   - Glass shard polygon debris below + rubble dust scatter
   - HOT_MAGENTA highlight on frame edges (storm light)
2. **Real window glow geometry**: for each lit building window, a downward trapezoid cone of warm amber (200, 160, 80) projected on ground below, alpha 90-110. Pools of warm domestic light competing vs cold storm sky.
All Cycle 16 carries: cold confetti, Dutch angle, Byte outline, storm rims.

---

## Task 3 — School Hallway v002 ✓

**Generator:** `output/tools/LTG_TOOL_bg_school_hallway_v002.py`
**Output:** `output/backgrounds/environments/LTG_ENV_school_hallway_v002.png`

Fixes applied:
1. **Black top band**: image now initialized to CEIL_TILE (216,212,192), ceiling polygon explicitly starts at y=0. Top of frame is ceiling — no black artifact.
2. **Human evidence**:
   - Backpack: 80×120px+ deep blue backpack leaning against nearest right-wall locker, with front pocket, shoulder strap loop, zipper line
   - Coat hooks: metal L-shaped hooks on right wall near section with hook rail strip
   - Hanging jacket: warm brown jacket on nearest hook — body + shadow side + collar + sleeves
   - Notice board: left wall near section with 8 distinct colored paper rectangles (red, yellow, green, white, blue) with pin dots
3. **Camera angle**: VP_CY lowered from H×0.40 → H×0.22 (–18%). Ceiling now dominates frame upper half. Hallway reads taller, more institutional, more imposing.

---

## Task 4 — Millbrook Main Street v002 ✓

**Generator:** `output/tools/LTG_TOOL_bg_millbrook_main_street_v002.py`
**Output:** `output/backgrounds/environments/LTG_ENV_millbrook_main_street_v002.png`

Fixes applied:
1. **Power lines**:
   - Main cable cross-street wires: 3px (perspective-scaled, slightly thinner at distance)
   - Span wires along street: 1px
   - Catenary sag via parabolic curve (sin(t×π) based)
   - POWER_LINE_CLR lightened from (74,72,64) → (88,84,74) — less heavy
2. **Road plane**:
   - Full ROAD_ASPHALT (100,90,76) solid trapezoid fills entire road surface
   - Sun-side lighter lane (ROAD_ASPHALT_LT)
   - Double-yellow center dashed line: two offset parallel lines converging to VP (perspective-correct)
   - Crosswalk stripes at near end: 8 perspective-correct trapezoid stripes (CROSSWALK_WHITE faded paint)
   - Curb edge lines added

---

## README Updated ✓

`output/tools/README.md` updated with all 4 new generators.

---

## Notes

- All tools use open source Python/PIL only
- All outputs versioned — no overwrites
- All inbox messages archived
- BYTE_BODY = (0,212,232) confirmed in all SF03 work going forward — never use (10,10,20)

Jordan Reed
