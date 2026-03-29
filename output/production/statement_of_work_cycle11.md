# Statement of Work — Cycle 11

**Date:** 2026-03-29
**Cycle:** 11

## Work Completed

### Alex Chen — Art Director
- **Mid-air transition element**: 60 warm/cold pixel confetti in x=768-960 dead zone — warm-lit left half, cold-lit right half; only elements in frame catching both lights simultaneously
- **Screen pixel figures**: scaled 7px → 15px wide, now viewer-readable silhouettes with body-plan legibility
- **Logo tagline removed**: "A cartoon series by the Dream Team" deleted; logo shows title only
- **byte.md version header**: `3.0` → `3.1` — document now internally consistent
- **Style guide Sections 9-11 added**: Animation Style Notes (per-character movement, glitch timing), Glitchkin Construction Rules (8 core rules, size table, construction checklist), Prop Design Guidelines (real-world vs Glitch Layer logic)
- **Output:** `style_frame_01_rendered.png`, `show_logo.png` regenerated; `style_guide.md` updated

### Maya Santos — Character Designer
- **Luma expression sheet created** (Priority 0): `luma_expression_sheet_generator.py` → `luma_expression_sheet.png` (3×2, 912×886px) — 6 expressions: Reckless Excitement, Worried/Determined, Mischievous Plotting, Settling/Wonder, Recognition, Warmth. Each with prev/next state annotations, distinct BG colors.
- **Sneaker profile fixed**: side-view `fw` normalized to `int(hu*0.52)` — all views now consistent
- **Output:** `luma_expression_sheet.png`, all turnarounds regenerated

### Jordan Reed — Background & Environment Artist
- **Pitch package index**: `pitch_package_index.md` — complete single-document navigator for all pitch assets, 4 sections, quality status per asset, open blockers list
- **LTG naming compliance**: `LTG_ENV_lumashome_layout_v001.png`, `LTG_ENV_millbrook_mainstreet_v001.png` created
- **Frame 02 background**: `bg_glitch_layer_encounter.py` → `bg_glitch_layer_encounter.png` — confrontation-composition Glitch Layer (Corruption bloom, arena platform layout, character stand with damage notch)
- **Output:** `bg_glitch_layer_encounter.png`, LTG-named copies, `pitch_package_index.md`

### Sam Kowalski — Color & Style Artist
- **Cold overlay arithmetic corrected**: documentation now states 11.8% (not "near-zero"); `cold_alpha_max=60` retained as physically correct cross-light
- **Style guide Color System section**: two-world palette logic, 5 key colors, Corrupted Amber rules, skin tone tables under 3 lighting conditions, forbidden color lists, decision flowchart
- **Output:** Updated `style_frame_01_rendered.py`, updated `style_guide.md`, color keys regenerated

### Lee Tanaka — Storyboard Artist
- **P23 Glitchkin polygons**: 14 rectangles → varied 4-7 sided polygons with jitter (now consistent with P22 and P24)
- **Module docstring**: updated "Cycle 8" → "Cycle 11"
- **Storyboard pitch export**: `storyboard_pitch_export_generator.py` → `storyboard_pitch_export.png` (1200×5046px) — 6-page composite: title page, 4 panel grid pages, hero spread (P23+P24)
- **Output:** P23 panel regenerated, contact sheet, `storyboard_pitch_export.png`

## Key Improvements Over Cycle 10
- Style frame: mid-air transition element addresses 2-cycle dead zone
- Luma expression sheet finally exists — lead character fully documented
- Storyboard pitch export created — package can now be presented
- Style guide nearly complete (Sections 1-11)
- Pitch package index provides single-document navigation
- byte.md v3.1 internally consistent
- Cold overlay documentation corrected
