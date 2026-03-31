# Maya Santos — Memory

## Cycle 58 — Nose/Mouth/Hairline fixes — COMPLETE

### Tasks (from inbox, human feedback)

**1. Nose not visible (all views)**
- Front: replaced 2.5s dot with upturned nose arc + two nostril dots
- Side-R: enlarged nose bump protrusion (peak 24s, was 18s); adjusted bezier control points
- Side-L: nose_x_base moved from -head_rx*0.82 → -head_rx*0.94 (anchored at face edge, matching side-R); larger control points to match
- 3/4: replaced tiny 5s curve with larger arc (9s wide) + near-side nostril dot

**2. Mouth too high (all views)**
- Front: mouth_y 0.44 → 0.56 head_r
- Side-R: mouth_y 0.42 → 0.54 head_r
- Side-L: mouth_y 0.42 → 0.54, mouth_x_base -0.30 → -0.62 (was not at face edge, now matches side-R logic)
- 3/4: mouth_y 0.44 → 0.56 head_r

**3. Hairline looks off (all views)**
- Front: raised large low-center hair blobs from by=-0.45 → by=-0.58, reduced bry from 0.42 → 0.38; side blobs raised from by=-0.30 → by=-0.42
- 3/4: same treatment (by=-0.45 → by=-0.58 for center blobs)
- Side-R: cleaned up blob at (-0.15, -0.60) — pulled back to (-0.28, -0.65); removed the face-side blob (0.20, -0.70) → pushed to (0.10, -0.75) with smaller radius
- Side-L: mirrored side-R hairline fixes

**Test:** char_module_test PASS (7/7 Luma expressions). Turnaround regenerated.

**Deliverables:**
- `LTG_TOOL_char_luma.py` — updated in-place
- `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround.png` — regenerated (1280x560)

**Completion message sent to Producer inbox.**

## Cycle 57 — Turnaround arm/torso/face fixes — COMPLETE
- Side/3q torso foreshortening, inline arm code, nose/mouth face edge positioning
- `LTG_TOOL_char_luma.py` v1.2.0

## Cycle 56 — Leg centering fix — COMPLETE
- All views: legs at hip_cx, hip bridge bw=leg_w_top*1.4

## Tools Owned (active)
- LTG_TOOL_char_luma.py (C58 nose/mouth/hairline)
- LTG_TOOL_char_miri.py v1.0.0 (C53)
- LTG_TOOL_luma_turnaround.py v007 (C55)
- (full list in SKILLS.md)

## Next Cycle Priorities
- Cosmo module test is FAIL (pre-existing, not caused by C58 changes) — send note to Alex Chen
- Migrate luma_cairo_expressions.py to import from char_luma.py
- Cosmo expression rebuild
