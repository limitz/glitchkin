# Pitch Package Audit — Cycle 27
**Prepared by:** Alex Chen, Art Director
**Date:** 2026-03-29
**Purpose:** Pre-Critique 12 audit — verify all indexed pitch assets exist on disk and identify any gaps.

---

## PRESENT: Confirmed Assets on Disk

### Style Frames
- `output/color/style_frames/LTG_COLOR_styleframe_discovery_v003.png` — SF01 v003 (UNLOCKED, open for v004)
- `output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v005.png` — SF02 v005 (PITCH READY)
- `output/color/style_frames/LTG_COLOR_styleframe_otherside_v003.png` — SF03 v003 (PITCH READY)
- `output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v001.png` — SF04 v001 (Luma+Byte dynamic)

### Character Expression Sheets
- `output/characters/main/LTG_CHAR_luma_expression_sheet_v006.png` — Luma v006 (line weight fix, C27 DELIVERED)
- `output/characters/main/LTG_CHAR_byte_expression_sheet_v004.png` — Byte v004 (PITCH READY)
- `output/characters/main/LTG_CHAR_cosmo_expression_sheet_v004.png` — Cosmo v004 (PITCH READY)
- `output/characters/main/LTG_CHAR_grandma_miri_expression_sheet_v003.png` — Miri v003 (KNOWING expression — DELIVERED)
- `output/characters/main/LTG_CHAR_glitch_expression_sheet_v002.png` — Glitch v002 (1200x900, 6 expressions — PITCH READY)

### Character Turnarounds
- `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround_v002.png` — Luma v002
- `output/characters/main/turnarounds/LTG_CHAR_byte_turnaround_v001.png` — Byte v001
- `output/characters/main/turnarounds/LTG_CHAR_cosmo_turnaround_v002.png` — Cosmo v002 (glasses fix)
- `output/characters/main/turnarounds/LTG_CHAR_miri_turnaround_v001.png` — Miri v001
- `output/characters/main/turnarounds/LTG_CHAR_glitch_turnaround_v002.png` — Glitch v002 (shadow fix)

### Character Lineup
- `output/characters/main/LTG_CHAR_lineup_v004.png` — All 5 characters including Glitch

### Logo / Brand
- `output/production/LTG_BRAND_logo_v001.png` — Canonical show logo (A grade, Victoria Ashford C13)

### Color Models (visual PNGs)
- `output/characters/color_models/LTG_COLOR_luma_color_model_v001.png`
- `output/characters/color_models/LTG_COLOR_byte_color_model_v001.png`
- `output/characters/color_models/LTG_COLOR_cosmo_color_model_v001.png`
- `output/characters/color_models/LTG_COLOR_grandma_miri_color_model_v001.png`
- All 4 `.md` color model specs present

### Color Swatches
- `output/characters/color_models/swatches/luma_swatches.png`
- `output/characters/color_models/swatches/byte_swatches.png`
- `output/characters/color_models/swatches/cosmo_swatches.png`
- `output/characters/color_models/swatches/grandma_miri_swatches.png`

### Environments
- `output/backgrounds/environments/LTG_ENV_grandma_kitchen_v003.png` — Kitchen (latest)
- `output/backgrounds/environments/LTG_ENV_tech_den_v004.png` — Tech Den (latest)
- `output/backgrounds/environments/LTG_ENV_glitchlayer_frame_v002.png` — Glitch Layer
- `output/backgrounds/environments/LTG_ENV_school_hallway_v002.png` — School Hallway (latest)
- `output/backgrounds/environments/LTG_ENV_millbrook_main_street_v002.png` — Millbrook Street (latest)
- `output/backgrounds/environments/LTG_ENV_classroom_bg_v002.png` — Classroom
- `output/backgrounds/environments/LTG_ENV_lumashome_study_interior_v001.png` — Luma's House

---

## MISSING: Referenced in Index but Not Found

None. All assets referenced in the pitch_package_index.md (including C24/C25 additions) are confirmed present on disk.

**Note:** The index references Miri v003 as "IN PROGRESS" (C25 status) — the file is now DELIVERED and present on disk. Index needs update.

---

## GAPS: Assets That Should Exist But Are Not in the Index

1. **Luma expression sheet v006** — Maya delivered C27; not yet in the index (was v005 as of last index update). Index needs version bump.
2. **Luma expression sheet v005** — Present on disk; index currently points to v005 as the latest Luma sheet. Superseded by v006.
3. **C26 completions not reflected in index:**
   - `LTG_TOOL_procedural_draw_v001.py` v1.1.0 (Rin's face lighting — not a pitch deliverable, but worth noting in tools section)
   - Pipeline retirement note: all `*_styled*.png` files removed C26; index Cycle 24 note covers this but no formal C26 additions section exists
4. **Miri expression sheet v003 status** — File exists but index still shows "IN PROGRESS" from Cycle 25. Now DELIVERED.
5. **No Cycle 26 additions section** in the index. C26 work (Luma v005 style fix, Luma turnaround v002 front view fix, QA tool) should be documented.

---

## VERDICT: READY for Critique 12

**Overall: READY**

All primary pitch assets are present on disk. The package is structurally complete:
- 4 style frames covering all 3 narrative worlds + character dynamic
- 5 character expression sheets (all main + supporting cast), all at current version
- 5 character turnarounds including Glitch
- All-5 character lineup
- Canonical logo
- 7 environment renders covering all key locations
- Full storyboard (25 cold open panels + Act 2 arc)
- Production bible, style guide, pitch brief, master palette

**Key C27 improvements landing before Critique 12:**
- Luma expression sheet v006: line weights now match classroom pose standard (3-tier system, no more heavy manga outlines)
- Miri v003: KNOWING expression present (narrative secret now visible in character design)
- Rin's volumetric face lighting: `add_face_lighting()` now available in procedural draw library

**Active open item (non-blocking):**
- SF01 v003 UNLOCKED — v004 not yet delivered. SF01 ships as v003 for Critique 12. This is the weakest link: Luma face/body inconsistency vs. expression sheets remains visible to critics. Flag for C28 if critics reprise.

**SUNLIT_AMBER QC false positive:** Sam flagged that `LTG_TOOL_color_verify_v001.py` will false-positive on Luma/Miri character sheets due to skin tone hue overlap. Kai should apply manual validation workaround for C27 QA pass; not a rendering defect.

---

*Alex Chen, Art Director — Cycle 27 — 2026-03-29*
