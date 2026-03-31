# Pre-Critique QA Report — C53

**Run date:** 2026-03-31 15:13
**Script:** LTG_TOOL_precritique_qa.py v2.11.0

---

## Overall Result

**FAIL** — PASS: 431  WARN: 91  FAIL: 1

> **README SYNC WARNING:** 50 discrepancy(ies) detected — 47 UNLISTED, 3 GHOST. See Section 7 for details. Update README Script Index before critique.


| Section | Result | PASS | WARN | FAIL |
|---|---|---|---|---|
| Render QA (pitch PNGs)         | WARN   | 0  | 6  | 0  |
| Color Verify (style frames)    | WARN | 0 | 4 | 0 |
| Proportion Verify (char sheets)| WARN  | 1  | 3  | 0  |
| Stub Linter (tools dir)        | PASS   | 200   | 0   | 0   |
| Palette Warmth Lint            | PASS| 17| 0| 0|
| Glitch Spec Lint               | WARN | 5 | 19 | 0 |
| README Script Index Sync       | WARN | 149 | 50 | 0 |
| Motion Spec Lint               | WARN | 33 | 3 | 0 |
| Alpha Blend Lint               | WARN | 1 | 1 | 0 |
| UV_PURPLE Dominance Lint       | FAIL   | 3   | 3   | 1   |
| Depth Temperature Lint         | FAIL   | 3   | 1   | 1   |
| Silhouette Distinctiveness     | FAIL   | 6   | 3   | 1   |
| Expression Range Metric        | PASS   | 5   | 0   | 0   |
| Construction Stiffness         | WARN   | 4   | 1   | 0   |
| Char Quality Regression Gate   | WARN   | 1   | 2   | 0   |

---

## 0. Delta Report

**Delta since last run (C52 @ 2026-03-31 01:00): -1 FAIL, +24 WARN, -38 resolved**

_Compared against: C52 run @ 2026-03-31 01:00_

**New FAILs since last run:**
  - [Color Verify] - LTG_COLOR_styleframe_glitch_storm.png / SUNLIT_AMBER: ΔE2000=11.29 (FAIL)
  - [Color Verify] - LTG_COLOR_styleframe_otherside.png / SUNLIT_AMBER: ΔE2000=9.35 (FAIL)

**New WARNs since last run:**
  - [Color Verify] - LTG_COLOR_styleframe_discovery.png / CORRUPT_AMBER: ΔE2000=6.61 (WARN)
  - [Color Verify] - LTG_COLOR_styleframe_sf04.png / BYTE_TEAL: ΔE2000=5.43 (WARN)
  - [Color Verify] - LTG_COLOR_styleframe_sf04.png / SUNLIT_AMBER: ΔE2000=7.25 (WARN)
  - [Proportion Verify] - LTG_CHAR_cosmo_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - [Glitch Spec Lint] - LTG_TOOL_char_glitch.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_glitch_expression_sheet.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_glitch_expression_sheet.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_glitch_motion.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_glitch_motion.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_glitch_turnaround.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_sb_ep05_covetous.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_sf_covetous_glitch.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_sf_covetous_glitch.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_sf_covetous_glitch_c43.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_sf_covetous_glitch_c43.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_03_other_side.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_styleframe_glitch_layer_showcase.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_styleframe_glitch_layer_showcase.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [README Sync] - GHOST: `LTG_TOOL_sb_cold_open_P{02-25}.py` (in README, not on disk)
  - [README Sync] - GHOST: `LTG_TOOL_sb_panel_a10{1-4}*.py` (in README, not on disk)
  - [README Sync] - GHOST: `LTG_TOOL_sb_panel_a20{1-8}*.py` (in README, not on disk)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P02.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P03.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P04.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P05.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P06.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P07.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P08.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P09.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P10.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P11.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P12.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P14.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P15.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P16.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P17.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P21_cairo.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P22.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P22a.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P23.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P23_cairo.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P24.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_panel_a101.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_panel_a102.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_panel_a103.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_panel_a104_kitchen.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_panel_a201.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_panel_a202.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_panel_a203.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_panel_a204.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_panel_a205.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_panel_a206_insert.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_panel_a207.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_panel_a207b.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_panel_a208.py` (on disk, not in README Script Index)
  - [Motion Spec Lint] - LTG_CHAR_glitch_motion.png: WARN: annotation_occupancy: [bg:dark-bright]  P1: 0.0% occupancy — WARN low  |  P2: 0.0% occupancy — WARN low  |  P3: 0.0% occupancy — WARN low  |  P4: 0.0% occupancy — WARN low
  - [Motion Spec Lint] - LTG_CHAR_glitch_motion.png: WARN: beat_badges: beat badge occupancy  P1: 0.0% — WARN no badge  |  P2: 0.0% — WARN no badge  |  P3: 0.0% — WARN no badge  |  P4: 0.0% — WARN no badge

**Resolved since last run (previously WARN/FAIL, now PASS):**
  - [Render QA] - LTG_COLOR_styleframe_sf04.png / line_weight: WARN — Line weight inconsistency — 3 outlier widths detected (mean=241.6px, std=458.0px)
  - [Color Verify] - LTG_COLOR_styleframe_glitch_storm.png / BYTE_TEAL: ΔE2000=5.48 (WARN)
  - [Color Verify] - LTG_COLOR_styleframe_otherside.png / BYTE_TEAL: ΔE2000=5.77 (WARN)
  - [Color Verify] - LTG_COLOR_styleframe_otherside.png / SUNLIT_AMBER: ΔE2000=13.02 (FAIL)
  - [Color Verify] - LTG_COLOR_styleframe_sf04.png / SUNLIT_AMBER: ΔE2000=7.24 (WARN)
  - [Proportion Verify] - LTG_CHAR_cosmo_turnaround.png: FAIL — ratio=17.84 (spec=3.2, tol=±5%)
  - [Glitch Spec Lint] - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(138, 122, 112). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(140, 120, 100). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(168, 152, 140). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(184, 154, 120). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(212, 130, 90). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(212, 149, 107). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_fidelity_check_c24.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_fidelity_check_c24.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_glitch_motion.py: G004: Draw order FAIL — HOT_MAG crack line appears BEFORE body fill polygon. Crack must be drawn after fill (spec §2.3 stacking order).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_03_other_side.py: G004: Draw order FAIL — HOT_MAG crack line appears BEFORE body fill polygon. Crack must be drawn after fill (spec §2.3 stacking order).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_03_other_side.py: G008: Interior states (YEARNING/COVETOUS/HOLLOW) detected but no bilateral eye rule found. Spec §6.3: interior states require IDENTICAL left+right eye glyphs — asymmetric destabilization must be SKIPPED for these states.
  - [Glitch Spec Lint] - LTG_TOOL_styleframe_glitch_layer_showcase.py: G004: Draw order FAIL — HOT_MAG crack line appears BEFORE body fill polygon. Crack must be drawn after fill (spec §2.3 stacking order).
  - [README Sync] - UNLISTED: `LTG_TOOL_batch_path_migrate.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_byte_turnaround.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_composite_warmth_score.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_contact_shadow.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_draw_shoulder_arm.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_face_metric_calibrate.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_freetype_eval.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_gesture_line_lint.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_luma_cairo_expressions.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_luma_motion_prototype_c51.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_object_detect_qa.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_prop_continuity_tracker.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_char_draw.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_scale_reference_sheet.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_styleframe_discovery_scenelit.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_visual_hook_audit.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_wand_compositing_eval.py` (on disk, not in README Script Index)
  - [Motion Spec Lint] - LTG_CHAR_byte_motion.png: WARN: annotation_occupancy: [bg:dark-bright]  P1: 0.0% occupancy — WARN low  |  P2: 0.0% occupancy — WARN low  |  P3: 0.0% occupancy — WARN low  |  P4: 5.3% occupancy
  - [Motion Spec Lint] - LTG_CHAR_byte_motion.png: WARN: beat_badges: beat badge occupancy  P1: 0.0% — WARN no badge  |  P2: 0.0% — WARN no badge  |  P3: 0.0% — WARN no badge  |  P4: 0.0% — WARN no badge
  - [Motion Spec Lint] - LTG_CHAR_byte_motion.png: WARN: timing_colors: BEAT_COLOR [config] in 0/4 panels (0%)

---

## 1. Render QA — Pitch PNGs — **WARN**

PASS: 0  WARN: 6  FAIL: 0  Missing: 0


Target files:
  - `LTG_COLOR_styleframe_discovery.png` (found)
  - `LTG_COLOR_styleframe_glitch_storm.png` (found)
  - `LTG_COLOR_styleframe_otherside.png` (found)
  - `LTG_COLOR_styleframe_sf04.png` (found)
  - `LTG_BRAND_logo.png` (found)
  - `storyboard_pitch_export.png` (found)

**Flagged items:**
  - LTG_COLOR_styleframe_discovery.png / color_fidelity: WARN
  - LTG_COLOR_styleframe_glitch_storm.png / color_fidelity: WARN
  - LTG_COLOR_styleframe_otherside.png / color_fidelity: WARN
  - LTG_COLOR_styleframe_sf04.png / color_fidelity: WARN
  - LTG_BRAND_logo.png / color_fidelity: WARN
  - LTG_BRAND_logo.png / warm_cool: WARN — composite=0.1707 FAIL for REAL_INTERIOR (primary metric v2.2.0 overrides hue-split PASS)
  - storyboard_pitch_export.png / color_fidelity: WARN


## 2. Color Verify — Style Frames — **WARN**

PASS: 0  WARN: 4  FAIL: 0  Missing: 0


**Flagged items:**
  - LTG_COLOR_styleframe_discovery.png / CORRUPT_AMBER: ΔE2000=6.61 (WARN)
  - LTG_COLOR_styleframe_glitch_storm.png / SUNLIT_AMBER: ΔE2000=11.29 (FAIL)
  - LTG_COLOR_styleframe_otherside.png / SUNLIT_AMBER: ΔE2000=9.35 (FAIL)
  - LTG_COLOR_styleframe_sf04.png / BYTE_TEAL: ΔE2000=5.43 (WARN)
  - LTG_COLOR_styleframe_sf04.png / SUNLIT_AMBER: ΔE2000=7.25 (WARN)


## 3. Proportion Verify — Character Sheets — **WARN**

PASS: 1  WARN: 3  FAIL: 0  Missing: 0


**Flagged items:**
  - LTG_CHAR_luma_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - LTG_CHAR_cosmo_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - LTG_CHAR_miri_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - LTG_CHAR_glitch_turnaround.png: SKIP proportion check (Glitch non-humanoid)


## 4. Stub Linter — output/tools/ — **PASS**

PASS: 200  WARN: 0  FAIL: 0  Missing: 0


_No issues found._


## 5. Palette Warmth Lint — master_palette.md — **PASS**

PASS: 17  WARN: 0  FAIL: 0  Missing: 0


_No issues found._


## 6. Glitch Spec Lint — Generators — **WARN**

PASS: 5  WARN: 19  FAIL: 0  Missing: 0


_(Non-Glitch files: 176 skipped)_

**Flagged items:**
  - LTG_CHAR_byte_motion.py: G003: Multi-Glitchkin frame has only 1 unique expression(s) — at least 2 required. Found: ['NEUTRAL']
  - LTG_CHAR_byte_motion.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - LTG_CHAR_byte_motion.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_bg_glitch_storm_colorfix.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - LTG_TOOL_bg_glitch_storm_colorfix.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_bg_other_side.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_byte_motion.py: G003: Multi-Glitchkin frame has only 0 unique expression(s) — at least 2 required. Found: none
  - LTG_TOOL_byte_motion.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - LTG_TOOL_byte_motion.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_char_glitch.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_character_face_test.py: G003: Multi-Glitchkin frame has only 1 unique expression(s) — at least 2 required. Found: ['NEUTRAL']
  - LTG_TOOL_character_face_test.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - LTG_TOOL_character_face_test.py: G006: Possible organic/warm fill detected — fill=(120, 120, 140). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_character_face_test.py: G006: Possible organic/warm fill detected — fill=(120, 120, 140). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_character_face_test.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_color_verify.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - LTG_TOOL_color_verify.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_glitch_color_model.py: G006: Possible organic/warm fill detected — fill=(200, 160, 80). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_glitch_expression_sheet.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - LTG_TOOL_glitch_expression_sheet.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_glitch_motion.py: G003: Multi-Glitchkin frame has only 0 unique expression(s) — at least 2 required. Found: none
  - LTG_TOOL_glitch_motion.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - LTG_TOOL_glitch_motion.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_glitch_turnaround.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - LTG_TOOL_glitch_turnaround.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_library_eval_c51.py: G003: Multi-Glitchkin frame has only 1 unique expression(s) — at least 2 required. Found: ['NEUTRAL']
  - LTG_TOOL_sb_ep05_covetous.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_sf_covetous_glitch.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - LTG_TOOL_sf_covetous_glitch.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_sf_covetous_glitch_c43.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - LTG_TOOL_sf_covetous_glitch_c43.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_style_frame_02_glitch_storm.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_style_frame_03_other_side.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_style_frame_04_resolution.py: G006: Possible organic/warm fill detected — fill=(175, 140, 95). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_style_frame_04_resolution.py: G006: Possible organic/warm fill detected — fill=(190, 140, 70). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_style_frame_04_resolution.py: G006: Possible organic/warm fill detected — fill=(160, 155, 148). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_styleframe_glitch_layer_showcase.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - LTG_TOOL_styleframe_glitch_layer_showcase.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).


## 7. README Script Index Sync — **WARN**

PASS: 149  WARN: 50  FAIL: 0  Missing: 0


_(Tools on disk: 196  |  Tools listed in README: 154)_

> **ACTION REQUIRED:** 47 tool(s) on disk not listed in README and 3 README entry(ies) with no corresponding file. Update `output/tools/README.md` Script Index before next critique cycle.

**Flagged items:**
  - UNLISTED: `LTG_TOOL_sb_cold_open_P02.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P03.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P04.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P05.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P06.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P07.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P08.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P09.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P09_cairo.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P10.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P10_cairo.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P11.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P12.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P13.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P13_cairo.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P14.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P15.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P15_cairo.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P16.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P17.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P17_cairo.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P17_chartest.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P18.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P19.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P20.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P20_cairo.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P21.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P21_cairo.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P22.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P22a.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P23.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P23_cairo.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P24.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P25.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_panel_a101.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_panel_a102.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_panel_a103.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_panel_a104_kitchen.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_panel_a201.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_panel_a202.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_panel_a203.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_panel_a204.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_panel_a205.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_panel_a206_insert.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_panel_a207.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_panel_a207b.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_panel_a208.py` (on disk, not in README Script Index)
  - GHOST: `LTG_TOOL_sb_cold_open_P{02-25}.py` (in README, not on disk)
  - GHOST: `LTG_TOOL_sb_panel_a10{1-4}*.py` (in README, not on disk)
  - GHOST: `LTG_TOOL_sb_panel_a20{1-8}*.py` (in README, not on disk)


## 8. Motion Spec Lint — motion sheets — **WARN**

PASS: 33  WARN: 3  FAIL: 0  Missing: 0


Target sheets:
  - `LTG_CHAR_luma_motion.png` (expected 4 panels, found)
  - `LTG_CHAR_byte_motion.png` (expected 4 panels, found)
  - `LTG_CHAR_cosmo_motion.png` (expected 4 panels, found)
  - `LTG_CHAR_miri_motion.png` (expected 4 panels, found)
  - `LTG_CHAR_miri_motion_v002.png` (expected 4 panels, found)
  - `LTG_CHAR_glitch_motion.png` (expected 4 panels, found)

**Flagged items:**
  - LTG_CHAR_glitch_motion.png: WARN: annotation_occupancy: [bg:dark-bright]  P1: 0.0% occupancy — WARN low  |  P2: 0.0% occupancy — WARN low  |  P3: 0.0% occupancy — WARN low  |  P4: 0.0% occupancy — WARN low
  - LTG_CHAR_glitch_motion.png: WARN: beat_badges: beat badge occupancy  P1: 0.0% — WARN no badge  |  P2: 0.0% — WARN no badge  |  P3: 0.0% — WARN no badge  |  P4: 0.0% — WARN no badge
  - LTG_CHAR_glitch_motion.png: WARN: timing_colors: BEAT_COLOR [config] in 0/4 panels (0%)


## 9. Arc-Diff Gate — Contact Sheet Changelog

_Informational only — does not affect overall PASS/WARN/FAIL score._
_WARN = panel removed (story continuity risk). NOTE = changed panels (critics: prioritize review of these)._

### Act 2 contact sheet v005→v006
  - *arc-diff module could not be loaded*
  - _NOTE: arc-diff tool unavailable — skipping_

### Act 1 cold open contact sheet v001→v002
  - *arc-diff module could not be loaded*
  - _NOTE: arc-diff tool unavailable — skipping_

---

## 10. Alpha Blend Lint — Fill-Light Composition — **WARN**

_Checks fill-light blending quality on composited style frames. Requires unlit base images (`*_nolight.png`) alongside composited outputs. FLAT_FILL = FAIL (no radial falloff). LOW_SIGNAL = WARN (fill too subtle). Assets skip gracefully when base is absent — not a defect._

PASS: 1  WARN: 1  FAIL: 0  Skipped: 1

### SF01 Discovery (Luma — warm lamp fill)
  - Zone `luma`: **PASS** — PASS — radial falloff detected

### SF02 Glitch Storm (Luma/Byte/Cosmo — HOT_MAGENTA fill)
  - *SKIP — Base image not found: LTG_COLOR_styleframe_glitch_storm_nolight.png*

### SF04 Resolution (Jordan C42 canonical — warm light + cool floor bounce)
  - Zone `luma`: LOW_SIGNAL — LOW_SIGNAL — fill contribution below noise floor (advisory)

---

## 11. UV_PURPLE Dominance Lint — Glitch Layer Colour Balance — **FAIL**

_Verifies UV_PURPLE (#7B2FBE) + ELEC_CYAN (#00F0FF) are the dominant colours in Glitch Layer images. Core world-rule: Glitch Layer = UV_PURPLE/ELEC_CYAN dominant, zero warm light. Check A: combined fraction of non-black pixels — PASS ≥ 20%, WARN 10–19%, FAIL < 10%. Check B: warm-hue contamination (LAB h° 30°–80°, chroma C* ≥ 8) — PASS < 5%, WARN ≥ 5%._

PASS: 3  WARN: 3  FAIL: 1  Skip: 0

### LTG_COLOR_sf_covetous_glitch.png — **PASS**
  - Check A (UV_PURPLE + ELEC_CYAN Dominance): **PASS**
    [GLITCH_DARK_SCENE] Combined UV_PURPLE-family+ELEC_CYAN = 97.3% of non-black pixels (ΔE-match=0.6%, hue-family=97.3%). ≥ 20% — PASS. UV_PURPLE hue-family pixels (h° 255°–325°, C* ≥ 8) = 96.9% of non-black.
  - Check B (Warm-Hue Contamination): **PASS**
    Warm-hue pixels (LAB h° 30°–80°, chroma C* ≥ 8) = 1.7% of total pixels (15821/921600). < 5% — PASS.

### LTG_SF_covetous_glitch_v001.png — **PASS**
  - Check A (UV_PURPLE + ELEC_CYAN Dominance): **PASS**
    [GLITCH_DARK_SCENE] Combined UV_PURPLE-family+ELEC_CYAN = 98.9% of non-black pixels (ΔE-match=0.2%, hue-family=98.9%). ≥ 20% — PASS. UV_PURPLE hue-family pixels (h° 255°–325°, C* ≥ 8) = 98.9% of non-black.
  - Check B (Warm-Hue Contamination): **PASS**
    Warm-hue pixels (LAB h° 30°–80°, chroma C* ≥ 8) = 0.7% of total pixels (6456/921600). < 5% — PASS.

### LTG_COLOR_styleframe_glitch_layer_showcase.png — **FAIL**
  - Check A (UV_PURPLE + ELEC_CYAN Dominance): **FAIL**
    Combined UV_PURPLE+ELEC_CYAN = 0.5% of non-black pixels (UV_PURPLE=0.0%, ELEC_CYAN=0.5%). < 10% — FAIL. Structural violation: Glitch Layer must be UV_PURPLE+ELEC_CYAN dominant.
  - Check B (Warm-Hue Contamination): **PASS**
    Warm-hue pixels (LAB h° 30°–80°, chroma C* ≥ 8) = 0.1% of total pixels (929/921600). < 5% — PASS.

### LTG_ENV_glitchlayer_frame.png — **WARN**
  - Check A (UV_PURPLE + ELEC_CYAN Dominance): **WARN**
    Combined UV_PURPLE+ELEC_CYAN = 17.0% of non-black pixels (UV_PURPLE=0.9%, ELEC_CYAN=16.0%). 10–19% — WARN. Glitch Layer scenes should have stronger UV_PURPLE/ELEC_CYAN presence.
  - Check B (Warm-Hue Contamination): **PASS**
    Warm-hue pixels (LAB h° 30°–80°, chroma C* ≥ 8) = 0.0% of total pixels (0/921600). < 5% — PASS.

### LTG_ENV_glitchlayer_encounter.png — **WARN**
  - Check A (UV_PURPLE + ELEC_CYAN Dominance): **WARN**
    Combined UV_PURPLE+ELEC_CYAN = 17.4% of non-black pixels (UV_PURPLE=0.0%, ELEC_CYAN=17.4%). 10–19% — WARN. Glitch Layer scenes should have stronger UV_PURPLE/ELEC_CYAN presence.
  - Check B (Warm-Hue Contamination): **PASS**
    Warm-hue pixels (LAB h° 30°–80°, chroma C* ≥ 8) = 0.0% of total pixels (0/921600). < 5% — PASS.

### bg_glitch_layer_encounter.png — **PASS**
  - Check A (UV_PURPLE + ELEC_CYAN Dominance): **PASS**
    Combined UV_PURPLE+ELEC_CYAN = 22.7% of non-black pixels (UV_PURPLE=0.9%, ELEC_CYAN=21.8%). ≥ 20% — PASS.
  - Check B (Warm-Hue Contamination): **PASS**
    Warm-hue pixels (LAB h° 30°–80°, chroma C* ≥ 8) = 0.0% of total pixels (0/921600). < 5% — PASS.

### glitch_layer_frame.png — **WARN**
  - Check A (UV_PURPLE + ELEC_CYAN Dominance): **WARN**
    Combined UV_PURPLE+ELEC_CYAN = 17.1% of non-black pixels (UV_PURPLE=1.1%, ELEC_CYAN=16.0%). 10–19% — WARN. Glitch Layer scenes should have stronger UV_PURPLE/ELEC_CYAN presence.
  - Check B (Warm-Hue Contamination): **PASS**
    Warm-hue pixels (LAB h° 30°–80°, chroma C* ≥ 8) = 0.0% of total pixels (0/921600). < 5% — PASS.

---

## 12. Depth Temperature Lint — Warm=FG / Cool=BG Grammar — **FAIL**

_Validates the Depth Temperature Rule (docs/image-rules.md, codified C45): warm color = foreground, cool color = background. Checks multi-character and multi-tier compositions. Glitch Layer scenes exempt. PASS: FG warmer than BG by >= threshold. WARN: correct direction but insufficient separation. FAIL: inverted depth grammar._

PASS: 3  WARN: 1  FAIL: 1  Skip: 1

### Character Lineup — **PASS**
  - FG warmth: 27.6  BG warmth: -32.8  separation: 60.4  threshold: 12.0

### SF05 The Passing — **PASS**
  - FG warmth: 86.1  BG warmth: -23.3  separation: 109.3  threshold: 12.0
  - Band override: FG=0.4 BG=0.85 (from depth_temp_band_overrides.json)

### SF06 The Hand-Off — **WARN**
  - FG warmth: 13.3  BG warmth: 9.3  separation: 4.0  threshold: 12.0

### SF04 Resolution — **PASS**
  - FG warmth: 35.0  BG warmth: 14.9  separation: 20.2  threshold: 12.0
  - World type: REAL
  - Band override: FG=0.55 BG=0.85 (from depth_temp_band_overrides.json)

### SF02 Glitch Storm — **FAIL**
  - FG warmth: -23.3  BG warmth: -23.1  separation: -0.2  threshold: 3.0
  - World type: REAL_STORM

### COVETOUS Style Frame — *SKIP*
  - *SKIP — SKIP: GLITCH scene exempt from Depth Temperature Rule*

---

## 13. Warm Pixel Percentage — World-Type Threshold Validation — **PASS**

_Validates warm-pixel-percentage against world-type thresholds using Sam Kowalski's LTG_TOOL_warm_pixel_metric (C47). REAL_INTERIOR: warm_pct >= 35%. REAL_STORM: warm_pct >= 5%. GLITCH: warm_pct <= 15%. OTHER_SIDE: warm_pct <= 5%._

PASS: 10  WARN: 0  FAIL: 0  Skip: 0

### SF01 Discovery — **PASS**
  - warm_pct: 59.4%  cool_pct: 37.3%  chromatic_warm_pct: 61.4%
  - World type: REAL_INTERIOR  verdict: PASS
  - warm_pct 59.4% >= 35.0% minimum

### SF04 Resolution — **PASS**
  - warm_pct: 75.9%  cool_pct: 6.0%  chromatic_warm_pct: 92.7%
  - World type: REAL_INTERIOR  verdict: PASS
  - warm_pct 75.9% >= 35.0% minimum

### SF05 The Passing — **PASS**
  - warm_pct: 74.7%  cool_pct: 18.7%  chromatic_warm_pct: 80.0%
  - World type: REAL_INTERIOR  verdict: PASS
  - warm_pct 74.7% >= 35.0% minimum

### SF06 The Hand-Off — **PASS**
  - warm_pct: 53.0%  cool_pct: 46.5%  chromatic_warm_pct: 53.3%
  - World type: REAL_INTERIOR  verdict: PASS
  - warm_pct 53.0% >= 35.0% minimum

### SF02 Glitch Storm — **PASS**
  - warm_pct: 11.1%  cool_pct: 50.7%  chromatic_warm_pct: 17.9%
  - World type: REAL_STORM  verdict: PASS
  - warm_pct 11.1% >= 5.0% minimum

### COVETOUS Style Frame — **PASS**
  - warm_pct: 2.1%  cool_pct: 9.2%  chromatic_warm_pct: 18.6%
  - World type: GLITCH  verdict: PASS
  - warm_pct 2.1% <= 15.0% maximum

### COVETOUS v001 — **PASS**
  - warm_pct: 0.7%  cool_pct: 10.6%  chromatic_warm_pct: 6.5%
  - World type: GLITCH  verdict: PASS
  - warm_pct 0.7% <= 15.0% maximum

### Glitch Layer Frame — **PASS**
  - warm_pct: 0.0%  cool_pct: 87.2%  chromatic_warm_pct: 0.0%
  - World type: GLITCH  verdict: PASS
  - warm_pct 0.0% <= 15.0% maximum

### Glitch Layer Encounter — **PASS**
  - warm_pct: 1.9%  cool_pct: 67.6%  chromatic_warm_pct: 2.8%
  - World type: GLITCH  verdict: PASS
  - warm_pct 1.9% <= 15.0% maximum

### SF03 Other Side — **PASS**
  - warm_pct: 1.8%  cool_pct: 24.5%  chromatic_warm_pct: 6.7%
  - World type: OTHER_SIDE  verdict: PASS
  - warm_pct 1.8% <= 5.0% maximum

---

## 14. Sightline Validation — Gaze Angular Error — **FAIL**

_Validates sight-line angular accuracy using Jordan Reed's LTG_TOOL_sightline_validator (C48). Pixel-based eye/pupil detection on rendered PNGs. PASS < 5 deg, WARN 5-15 deg, FAIL > 15 deg angular error._

PASS: 0  WARN: 0  FAIL: 1  Skip: 0

### SF01 Luma -> CRT — **FAIL**
  - Angular error: 106.0 deg
  - Miss distance: 338.4 px
  - Sight-line angular error: 106.0 deg (gaze -140.4 deg, ideal -34.3 deg). Miss at target range: 338.4px. Grade: FAIL. [LOW CONFIDENCE: eyes are small — pixel detection may be inaccurate. Use construction mode for authoritative results.]

---

## 15. Silhouette Distinctiveness — Character Shape Uniqueness — **FAIL**

_Pairwise silhouette comparison of character turnarounds at multiple scales. Measures Silhouette Overlap Ratio (SOR) and Width Profile Correlation (WPC). DS = 1.0 - (0.5*SOR + 0.5*WPC). PASS: DS >= 0.30. WARN: DS 0.15-0.30. FAIL: DS < 0.15._

PASS: 6  WARN: 3  FAIL: 1  Skip: 0

Characters analyzed: luma_turnaround, cosmo_turnaround, miri_turnaround, byte_turnaround, glitch_turnaround

### luma_turnaround vs cosmo_turnaround — **FAIL**
  - Worst DS: 0.1180 (at 50%)
  - 100%: DS=0.1321  SOR=0.7692  WPC=0.9666  Hausdorff: 0.0503
  - 50%: DS=0.1180  SOR=0.7679  WPC=0.9960  Hausdorff: 0.0487
  - 25%: DS=0.1292  SOR=0.7521  WPC=0.9894  Hausdorff: 0.0515

### luma_turnaround vs miri_turnaround — **WARN**
  - Worst DS: 0.1548 (at 25%)
  - 100%: DS=0.1592  SOR=0.7147  WPC=0.9670  Hausdorff: 0.0511
  - 50%: DS=0.1556  SOR=0.7207  WPC=0.9680  Hausdorff: 0.0523
  - 25%: DS=0.1548  SOR=0.7369  WPC=0.9536  Hausdorff: 0.0723

### luma_turnaround vs byte_turnaround — **PASS**
  - Worst DS: 0.4378 (at 100%)
  - 100%: DS=0.4378  SOR=0.5436  WPC=0.5808  Hausdorff: 0.1025
  - 50%: DS=0.4740  SOR=0.5449  WPC=0.5072  Hausdorff: 0.0843
  - 25%: DS=0.4916  SOR=0.5451  WPC=0.4718  Hausdorff: 0.1081

### luma_turnaround vs glitch_turnaround — **PASS**
  - Worst DS: 0.5718 (at 25%)
  - 100%: DS=0.5767  SOR=0.6275  WPC=0.2192  Hausdorff: 0.1470
  - 50%: DS=0.5980  SOR=0.6195  WPC=0.1845  Hausdorff: 0.1459
  - 25%: DS=0.5718  SOR=0.6271  WPC=0.2293  Hausdorff: 0.1489

### cosmo_turnaround vs miri_turnaround — **WARN**
  - Worst DS: 0.1679 (at 50%)
  - 100%: DS=0.1845  SOR=0.6810  WPC=0.9500  Hausdorff: 0.0657
  - 50%: DS=0.1679  SOR=0.6996  WPC=0.9646  Hausdorff: 0.0656
  - 25%: DS=0.1899  SOR=0.6682  WPC=0.9520  Hausdorff: 0.0964

### cosmo_turnaround vs byte_turnaround — **PASS**
  - Worst DS: 0.4025 (at 100%)
  - 100%: DS=0.4025  SOR=0.6259  WPC=0.5692  Hausdorff: 0.1170
  - 50%: DS=0.4355  SOR=0.6264  WPC=0.5026  Hausdorff: 0.0921
  - 25%: DS=0.4414  SOR=0.6208  WPC=0.4963  Hausdorff: 0.1199

### cosmo_turnaround vs glitch_turnaround — **PASS**
  - Worst DS: 0.4863 (at 25%)
  - 100%: DS=0.4936  SOR=0.7338  WPC=0.2790  Hausdorff: 0.1411
  - 50%: DS=0.5262  SOR=0.7358  WPC=0.2118  Hausdorff: 0.1412
  - 25%: DS=0.4863  SOR=0.7512  WPC=0.2761  Hausdorff: 0.1412

### miri_turnaround vs byte_turnaround — **PASS**
  - Worst DS: 0.3980 (at 100%)
  - 100%: DS=0.3980  SOR=0.6137  WPC=0.5904  Hausdorff: 0.1035
  - 50%: DS=0.5398  SOR=0.6187  WPC=0.3017  Hausdorff: 0.0814
  - 25%: DS=0.4344  SOR=0.6176  WPC=0.5135  Hausdorff: 0.1043

### miri_turnaround vs glitch_turnaround — **PASS**
  - Worst DS: 0.5076 (at 100%)
  - 100%: DS=0.5076  SOR=0.7569  WPC=0.2278  Hausdorff: 0.1470
  - 50%: DS=0.5957  SOR=0.7537  WPC=0.0549  Hausdorff: 0.1464
  - 25%: DS=0.5118  SOR=0.7441  WPC=0.2469  Hausdorff: 0.1646

### byte_turnaround vs glitch_turnaround — **WARN**
  - Worst DS: 0.2363 (at 50%)
  - 100%: DS=0.2690  SOR=0.9360  WPC=0.5299  Hausdorff: 0.1539
  - 50%: DS=0.2363  SOR=0.9359  WPC=0.5986  Hausdorff: 0.1570
  - 25%: DS=0.2905  SOR=0.9423  WPC=0.4798  Hausdorff: 0.1531

---

## 16. Expression Range Metric — Facial Variation — **PASS**

_Measures expression variation across expression sheet panels using Face Region Pixel Delta (FRPD) and Structural Change Index (SCI). Aggregate Expression Range Score (ERS) = mean FRPD across all pairs. PASS: ERS >= 0.10. WARN: ERS 0.05-0.10. FAIL: ERS < 0.05._

PASS: 5  WARN: 0  FAIL: 0  Skip: 0

### Luma Expressions — **PASS**
  - Grid: 3x3  Valid panels: 9  ERS: 0.3249  Verdict: PASS
  - Pairs: 36 total — PASS: 36  WARN: 0  FAIL: 0

### Byte Expressions — **PASS**
  - Grid: 4x3  Valid panels: 10  ERS: 0.2617  Verdict: PASS
  - Pairs: 45 total — PASS: 39  WARN: 5  FAIL: 1

### Cosmo Expressions — **PASS**
  - Grid: 3x3  Valid panels: 9  ERS: 0.2176  Verdict: PASS
  - Pairs: 36 total — PASS: 30  WARN: 6  FAIL: 0

### Glitch Expressions — **PASS**
  - Grid: 3x3  Valid panels: 9  ERS: 0.1391  Verdict: PASS
  - Pairs: 36 total — PASS: 23  WARN: 13  FAIL: 0

### Miri Expressions — **PASS**
  - Grid: 3x3  Valid panels: 9  ERS: 0.2620  Verdict: PASS
  - Pairs: 36 total — PASS: 33  WARN: 3  FAIL: 0

---

## 17. Construction Stiffness — Organic Shape Quality — **WARN**

_Detects overly straight/rectangular character construction via contour straightness analysis. Uses skimage sub-pixel contours + Shapely when available. Stiffness Score = 0.6*straight_pct + 0.4*(longest_run/total). PASS: SS <= 0.25. WARN: SS 0.25-0.40. FAIL: SS > 0.40._

PASS: 4  WARN: 1  FAIL: 0  Skip: 0

### Luma Turnaround — **PASS**
  - Stiffness: 0.2255  Straight%: 36.0%  Longest run: 560px  Total outline: 23936px
  - Backend: skimage+shapely

### Cosmo Turnaround — **WARN**
  - Stiffness: 0.2801  Straight%: 44.9%  Longest run: 560px  Total outline: 20293px
  - Backend: skimage+shapely

### Miri Turnaround — **PASS**
  - Stiffness: 0.2175  Straight%: 34.7%  Longest run: 560px  Total outline: 24037px
  - Backend: skimage+shapely

### Byte Turnaround — **PASS**
  - Stiffness: 0.2451  Straight%: 39.6%  Longest run: 200px  Total outline: 10825px
  - Backend: skimage+shapely

### Glitch Turnaround — **PASS**
  - Stiffness: 0.1747  Straight%: 28.8%  Longest run: 70px  Total outline: 14573px
  - Backend: skimage+shapely

---

## 18. Character Quality Regression Gate — C52 Baseline Check — **WARN**

_Compares current character quality metrics (stiffness, expression range, silhouette distinctiveness) against C52 baseline. Regression flags WARN (not FAIL — temporary regression expected during modular renderer rebuild)._

PASS: 1  WARN: 2  FAIL: 0  Skip: 0

| Metric | C52 Baseline | Current | Status |
|---|---|---|---|
| Stiffness (lower=better) | 0.092 | 0.1747 | WARN regression |
| Expression Range (higher=better) | 0.325 | 0.3249 | PASS |
| Silhouette FAIL pairs (lower=better) | 0 | 1 | WARN regression |

**Regressions detected:**
  - Stiffness regressed: 0.1747 > baseline 0.092 + 0.05 tolerance
  - Silhouette FAIL pairs increased: 1 > baseline 0

---

*Generated by LTG_TOOL_precritique_qa.py v3.1.0 — Kai Nakamura (C53: Section 18 Regression Gate, cairo surface support); Kai Nakamura (C52: Sections 15/16/17 Character Quality Metrics); Morgan Walsh (C49: Section 14 Sightline Validation added); Lee Tanaka (C48: Section 12 per-asset band overrides); Kai Nakamura (C48: Section 13 Warm Pixel Percentage added); Rin Yamamoto (C44: Section 11 UV_PURPLE Dominance Lint); Ryo Hasegawa (C46: motion spec dark-sheet fix, C45: glitch motion); Rin Yamamoto (C43: SF04 FILL_LIGHT_ASSETS path fix)*