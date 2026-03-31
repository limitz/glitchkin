# Pre-Critique QA Report — C52

**Run date:** 2026-03-31 01:00
**Script:** LTG_TOOL_precritique_qa.py v2.11.0

---

## Overall Result

**FAIL** — PASS: 456  WARN: 66  FAIL: 3

> **README SYNC WARNING:** 30 discrepancy(ies) detected — 30 UNLISTED, 0 GHOST. See Section 7 for details. Update README Script Index before critique.


| Section | Result | PASS | WARN | FAIL |
|---|---|---|---|---|
| Render QA (pitch PNGs)         | WARN   | 0  | 6  | 0  |
| Color Verify (style frames)    | WARN | 1 | 3 | 0 |
| Proportion Verify (char sheets)| FAIL  | 1  | 2  | 1  |
| Stub Linter (tools dir)        | PASS   | 204   | 0   | 0   |
| Palette Warmth Lint            | PASS| 17| 0| 0|
| Glitch Spec Lint               | WARN | 9 | 16 | 0 |
| README Script Index Sync       | WARN | 169 | 30 | 0 |
| Motion Spec Lint               | WARN | 32 | 4 | 0 |
| Alpha Blend Lint               | PASS | 1 | 0 | 0 |
| UV_PURPLE Dominance Lint       | FAIL   | 3   | 3   | 1   |
| Depth Temperature Lint         | WARN   | 3   | 2   | 0   |
| Silhouette Distinctiveness     | FAIL   | 5   | 3   | 2   |
| Expression Range Metric        | WARN   | 4   | 1   | 0   |
| Construction Stiffness         | WARN   | 4   | 1   | 0   |

---

## 0. Delta Report

**Delta since last run (C52 @ 2026-03-31 00:59): +0 FAIL, -1 WARN, -3 resolved**

_Compared against: C52 run @ 2026-03-31 00:59_

**New WARNs since last run:**
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P20_cairo.py` (on disk, not in README Script Index)

**Resolved since last run (previously WARN/FAIL, now PASS):**
  - [Color Verify] - LTG_COLOR_styleframe_discovery.png / BYTE_TEAL: ΔE2000=6.61 (WARN)
  - [Color Verify] - LTG_COLOR_styleframe_discovery.png / HOT_MAGENTA: ΔE2000=5.50 (WARN)
  - [Motion Spec Lint] - LTG_CHAR_luma_motion.png: WARN: beat_badges: beat badge occupancy  P1: 8.0% — WARN no badge  |  P2: 11.5% — WARN no badge  |  P3: 14.1% — WARN no badge  |  P4: 11.6% — WARN no badge

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
  - LTG_COLOR_styleframe_sf04.png / line_weight: WARN — Line weight inconsistency — 3 outlier widths detected (mean=241.6px, std=458.0px)
  - LTG_BRAND_logo.png / color_fidelity: WARN
  - LTG_BRAND_logo.png / warm_cool: WARN — composite=0.1707 FAIL for REAL_INTERIOR (primary metric v2.2.0 overrides hue-split PASS)
  - storyboard_pitch_export.png / color_fidelity: WARN


## 2. Color Verify — Style Frames — **WARN**

PASS: 1  WARN: 3  FAIL: 0  Missing: 0


**Flagged items:**
  - LTG_COLOR_styleframe_glitch_storm.png / BYTE_TEAL: ΔE2000=5.48 (WARN)
  - LTG_COLOR_styleframe_otherside.png / BYTE_TEAL: ΔE2000=5.77 (WARN)
  - LTG_COLOR_styleframe_otherside.png / SUNLIT_AMBER: ΔE2000=13.02 (FAIL)
  - LTG_COLOR_styleframe_sf04.png / SUNLIT_AMBER: ΔE2000=7.24 (WARN)


## 3. Proportion Verify — Character Sheets — **FAIL**

PASS: 1  WARN: 2  FAIL: 1  Missing: 0


**Flagged items:**
  - LTG_CHAR_luma_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - LTG_CHAR_cosmo_turnaround.png: FAIL — ratio=17.84 (spec=3.2, tol=±5%)
  - LTG_CHAR_miri_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - LTG_CHAR_glitch_turnaround.png: SKIP proportion check (Glitch non-humanoid)


## 4. Stub Linter — output/tools/ — **PASS**

PASS: 204  WARN: 0  FAIL: 0  Missing: 0


_No issues found._


## 5. Palette Warmth Lint — master_palette.md — **PASS**

PASS: 17  WARN: 0  FAIL: 0  Missing: 0


_No issues found._


## 6. Glitch Spec Lint — Generators — **WARN**

PASS: 9  WARN: 16  FAIL: 0  Missing: 0


_(Non-Glitch files: 179 skipped)_

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
  - LTG_TOOL_character_face_test.py: G003: Multi-Glitchkin frame has only 1 unique expression(s) — at least 2 required. Found: ['NEUTRAL']
  - LTG_TOOL_character_face_test.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - LTG_TOOL_character_face_test.py: G006: Possible organic/warm fill detected — fill=(120, 120, 140). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_character_face_test.py: G006: Possible organic/warm fill detected — fill=(120, 120, 140). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_character_face_test.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(184, 154, 120). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(184, 154, 120). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(168, 152, 140). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(212, 149, 107). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(212, 149, 107). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(138, 122, 112). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(138, 122, 112). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(212, 130, 90). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(140, 120, 100). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_color_verify.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - LTG_TOOL_color_verify.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_fidelity_check_c24.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - LTG_TOOL_fidelity_check_c24.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_glitch_color_model.py: G006: Possible organic/warm fill detected — fill=(200, 160, 80). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_glitch_motion.py: G003: Multi-Glitchkin frame has only 0 unique expression(s) — at least 2 required. Found: none
  - LTG_TOOL_glitch_motion.py: G004: Draw order FAIL — HOT_MAG crack line appears BEFORE body fill polygon. Crack must be drawn after fill (spec §2.3 stacking order).
  - LTG_TOOL_glitch_turnaround.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_library_eval_c51.py: G003: Multi-Glitchkin frame has only 1 unique expression(s) — at least 2 required. Found: ['NEUTRAL']
  - LTG_TOOL_style_frame_02_glitch_storm.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_style_frame_03_other_side.py: G004: Draw order FAIL — HOT_MAG crack line appears BEFORE body fill polygon. Crack must be drawn after fill (spec §2.3 stacking order).
  - LTG_TOOL_style_frame_03_other_side.py: G008: Interior states (YEARNING/COVETOUS/HOLLOW) detected but no bilateral eye rule found. Spec §6.3: interior states require IDENTICAL left+right eye glyphs — asymmetric destabilization must be SKIPPED for these states.
  - LTG_TOOL_style_frame_04_resolution.py: G006: Possible organic/warm fill detected — fill=(175, 140, 95). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_style_frame_04_resolution.py: G006: Possible organic/warm fill detected — fill=(190, 140, 70). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_style_frame_04_resolution.py: G006: Possible organic/warm fill detected — fill=(160, 155, 148). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_styleframe_glitch_layer_showcase.py: G004: Draw order FAIL — HOT_MAG crack line appears BEFORE body fill polygon. Crack must be drawn after fill (spec §2.3 stacking order).


## 7. README Script Index Sync — **WARN**

PASS: 169  WARN: 30  FAIL: 0  Missing: 0


_(Tools on disk: 199  |  Tools listed in README: 295)_

> **ACTION REQUIRED:** 30 tool(s) on disk not listed in README and 0 README entry(ies) with no corresponding file. Update `output/tools/README.md` Script Index before next critique cycle.

**Flagged items:**
  - UNLISTED: `LTG_TOOL_batch_path_migrate.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_byte_turnaround.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_composite_warmth_score.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_contact_shadow.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_draw_shoulder_arm.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_face_metric_calibrate.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_freetype_eval.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_gesture_line_lint.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_luma_cairo_expressions.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_luma_motion_prototype_c51.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_object_detect_qa.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_prop_continuity_tracker.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_char_draw.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P09_cairo.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P10_cairo.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P13.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P13_cairo.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P15_cairo.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P17_cairo.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P17_chartest.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P18.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P19.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P20.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P20_cairo.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P21.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P25.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_scale_reference_sheet.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_styleframe_discovery_scenelit.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_visual_hook_audit.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_wand_compositing_eval.py` (on disk, not in README Script Index)


## 8. Motion Spec Lint — motion sheets — **WARN**

PASS: 32  WARN: 4  FAIL: 0  Missing: 0


Target sheets:
  - `LTG_CHAR_luma_motion.png` (expected 4 panels, found)
  - `LTG_CHAR_byte_motion.png` (expected 4 panels, found)
  - `LTG_CHAR_cosmo_motion.png` (expected 4 panels, found)
  - `LTG_CHAR_miri_motion.png` (expected 4 panels, found)
  - `LTG_CHAR_miri_motion_v002.png` (expected 4 panels, found)
  - `LTG_CHAR_glitch_motion.png` (expected 4 panels, found)

**Flagged items:**
  - LTG_CHAR_byte_motion.png: WARN: annotation_occupancy: [bg:dark-bright]  P1: 0.0% occupancy — WARN low  |  P2: 0.0% occupancy — WARN low  |  P3: 0.0% occupancy — WARN low  |  P4: 5.3% occupancy
  - LTG_CHAR_byte_motion.png: WARN: beat_badges: beat badge occupancy  P1: 0.0% — WARN no badge  |  P2: 0.0% — WARN no badge  |  P3: 0.0% — WARN no badge  |  P4: 0.0% — WARN no badge
  - LTG_CHAR_byte_motion.png: WARN: timing_colors: BEAT_COLOR [config] in 0/4 panels (0%)
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

## 10. Alpha Blend Lint — Fill-Light Composition — **PASS**

_Checks fill-light blending quality on composited style frames. Requires unlit base images (`*_nolight.png`) alongside composited outputs. FLAT_FILL = FAIL (no radial falloff). LOW_SIGNAL = WARN (fill too subtle). Assets skip gracefully when base is absent — not a defect._

PASS: 1  WARN: 0  FAIL: 0  Skipped: 2

### SF01 Discovery (Luma — warm lamp fill)
  - Zone `luma`: **PASS** — PASS — radial falloff detected

### SF02 Glitch Storm (Luma/Byte/Cosmo — HOT_MAGENTA fill)
  - *SKIP — Base image not found: LTG_COLOR_styleframe_glitch_storm_nolight.png*

### SF04 Resolution (Jordan C42 canonical — warm light + cool floor bounce)
  - *SKIP — Base image not found: LTG_COLOR_styleframe_sf04_nolight.png*

---

## 11. UV_PURPLE Dominance Lint — Glitch Layer Colour Balance — **FAIL**

_Verifies UV_PURPLE (#7B2FBE) + ELEC_CYAN (#00F0FF) are the dominant colours in Glitch Layer images. Core world-rule: Glitch Layer = UV_PURPLE/ELEC_CYAN dominant, zero warm light. Check A: combined fraction of non-black pixels — PASS ≥ 20%, WARN 10–19%, FAIL < 10%. Check B: warm-hue contamination (LAB h° 30°–80°, chroma C* ≥ 8) — PASS < 5%, WARN ≥ 5%._

PASS: 3  WARN: 3  FAIL: 1  Skip: 0

### LTG_COLOR_sf_covetous_glitch.png — **PASS**
  - Check A (UV_PURPLE + ELEC_CYAN Dominance): **PASS**
    [GLITCH_DARK_SCENE] Combined UV_PURPLE-family+ELEC_CYAN = 97.1% of non-black pixels (ΔE-match=0.6%, hue-family=97.1%). ≥ 20% — PASS. UV_PURPLE hue-family pixels (h° 255°–325°, C* ≥ 8) = 96.7% of non-black.
  - Check B (Warm-Hue Contamination): **PASS**
    Warm-hue pixels (LAB h° 30°–80°, chroma C* ≥ 8) = 2.1% of total pixels (19232/921600). < 5% — PASS.

### LTG_SF_covetous_glitch_v001.png — **PASS**
  - Check A (UV_PURPLE + ELEC_CYAN Dominance): **PASS**
    [GLITCH_DARK_SCENE] Combined UV_PURPLE-family+ELEC_CYAN = 98.9% of non-black pixels (ΔE-match=0.2%, hue-family=98.9%). ≥ 20% — PASS. UV_PURPLE hue-family pixels (h° 255°–325°, C* ≥ 8) = 98.9% of non-black.
  - Check B (Warm-Hue Contamination): **PASS**
    Warm-hue pixels (LAB h° 30°–80°, chroma C* ≥ 8) = 0.7% of total pixels (6456/921600). < 5% — PASS.

### LTG_COLOR_styleframe_glitch_layer_showcase.png — **FAIL**
  - Check A (UV_PURPLE + ELEC_CYAN Dominance): **FAIL**
    Combined UV_PURPLE+ELEC_CYAN = 0.6% of non-black pixels (UV_PURPLE=0.0%, ELEC_CYAN=0.6%). < 10% — FAIL. Structural violation: Glitch Layer must be UV_PURPLE+ELEC_CYAN dominant.
  - Check B (Warm-Hue Contamination): **PASS**
    Warm-hue pixels (LAB h° 30°–80°, chroma C* ≥ 8) = 0.1% of total pixels (841/921600). < 5% — PASS.

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

## 12. Depth Temperature Lint — Warm=FG / Cool=BG Grammar — **WARN**

_Validates the Depth Temperature Rule (docs/image-rules.md, codified C45): warm color = foreground, cool color = background. Checks multi-character and multi-tier compositions. Glitch Layer scenes exempt. PASS: FG warmer than BG by >= threshold. WARN: correct direction but insufficient separation. FAIL: inverted depth grammar._

PASS: 3  WARN: 2  FAIL: 0  Skip: 1

### Character Lineup — **PASS**
  - FG warmth: 32.2  BG warmth: 3.4  separation: 28.8  threshold: 12.0

### SF05 The Passing — **PASS**
  - FG warmth: 92.8  BG warmth: -23.3  separation: 116.1  threshold: 12.0
  - Band override: FG=0.4 BG=0.85 (from depth_temp_band_overrides.json)

### SF06 The Hand-Off — **WARN**
  - FG warmth: 64.0  BG warmth: 53.4  separation: 10.6  threshold: 12.0

### SF04 Resolution — **PASS**
  - FG warmth: 39.6  BG warmth: 11.0  separation: 28.6  threshold: 12.0
  - World type: REAL
  - Band override: FG=0.55 BG=0.85 (from depth_temp_band_overrides.json)

### SF02 Glitch Storm — **WARN**
  - FG warmth: -24.5  BG warmth: -25.6  separation: 1.1  threshold: 3.0
  - World type: REAL_STORM

### COVETOUS Style Frame — *SKIP*
  - *SKIP — SKIP: GLITCH scene exempt from Depth Temperature Rule*

---

## 13. Warm Pixel Percentage — World-Type Threshold Validation — **PASS**

_Validates warm-pixel-percentage against world-type thresholds using Sam Kowalski's LTG_TOOL_warm_pixel_metric (C47). REAL_INTERIOR: warm_pct >= 35%. REAL_STORM: warm_pct >= 5%. GLITCH: warm_pct <= 15%. OTHER_SIDE: warm_pct <= 5%._

PASS: 10  WARN: 0  FAIL: 0  Skip: 0

### SF01 Discovery — **PASS**
  - warm_pct: 59.2%  cool_pct: 37.7%  chromatic_warm_pct: 61.1%
  - World type: REAL_INTERIOR  verdict: PASS
  - warm_pct 59.2% >= 35.0% minimum

### SF04 Resolution — **PASS**
  - warm_pct: 76.5%  cool_pct: 2.4%  chromatic_warm_pct: 97.0%
  - World type: REAL_INTERIOR  verdict: PASS
  - warm_pct 76.5% >= 35.0% minimum

### SF05 The Passing — **PASS**
  - warm_pct: 74.8%  cool_pct: 18.6%  chromatic_warm_pct: 80.0%
  - World type: REAL_INTERIOR  verdict: PASS
  - warm_pct 74.8% >= 35.0% minimum

### SF06 The Hand-Off — **PASS**
  - warm_pct: 61.5%  cool_pct: 4.4%  chromatic_warm_pct: 93.4%
  - World type: REAL_INTERIOR  verdict: PASS
  - warm_pct 61.5% >= 35.0% minimum

### SF02 Glitch Storm — **PASS**
  - warm_pct: 11.1%  cool_pct: 50.8%  chromatic_warm_pct: 17.9%
  - World type: REAL_STORM  verdict: PASS
  - warm_pct 11.1% >= 5.0% minimum

### COVETOUS Style Frame — **PASS**
  - warm_pct: 2.2%  cool_pct: 9.5%  chromatic_warm_pct: 19.0%
  - World type: GLITCH  verdict: PASS
  - warm_pct 2.2% <= 15.0% maximum

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
  - warm_pct: 1.6%  cool_pct: 24.7%  chromatic_warm_pct: 6.2%
  - World type: OTHER_SIDE  verdict: PASS
  - warm_pct 1.6% <= 5.0% maximum

---

## 14. Sightline Validation — Gaze Angular Error — **FAIL**

_Validates sight-line angular accuracy using Jordan Reed's LTG_TOOL_sightline_validator (C48). Pixel-based eye/pupil detection on rendered PNGs. PASS < 5 deg, WARN 5-15 deg, FAIL > 15 deg angular error._

PASS: 0  WARN: 0  FAIL: 1  Skip: 0

### SF01 Luma -> CRT — **FAIL**
  - Angular error: 17.7 deg
  - Miss distance: 87.9 px
  - Sight-line angular error: 17.7 deg (gaze -59.3 deg, ideal -41.6 deg). Miss at target range: 87.9px. Grade: FAIL.

---

## 15. Silhouette Distinctiveness — Character Shape Uniqueness — **FAIL**

_Pairwise silhouette comparison of character turnarounds at multiple scales. Measures Silhouette Overlap Ratio (SOR) and Width Profile Correlation (WPC). DS = 1.0 - (0.5*SOR + 0.5*WPC). PASS: DS >= 0.30. WARN: DS 0.15-0.30. FAIL: DS < 0.15._

PASS: 5  WARN: 3  FAIL: 2  Skip: 0

Characters analyzed: luma_turnaround, cosmo_turnaround, miri_turnaround, byte_turnaround, glitch_turnaround

### luma_turnaround vs cosmo_turnaround — **WARN**
  - Worst DS: 0.2995 (at 100%)
  - 100%: DS=0.2995  SOR=0.8501  WPC=0.5510  Hausdorff: 0.1184
  - 50%: DS=0.3412  SOR=0.8528  WPC=0.4648  Hausdorff: 0.1203
  - 25%: DS=0.3481  SOR=0.8435  WPC=0.4603  Hausdorff: 0.1178

### luma_turnaround vs miri_turnaround — **FAIL**
  - Worst DS: 0.0110 (at 25%)
  - 100%: DS=0.0118  SOR=0.9764  WPC=1.0000  Hausdorff: 0.0000
  - 50%: DS=0.0123  SOR=0.9754  WPC=1.0000  Hausdorff: 0.0000
  - 25%: DS=0.0110  SOR=0.9780  WPC=1.0000  Hausdorff: 0.0000

### luma_turnaround vs byte_turnaround — **PASS**
  - Worst DS: 0.7750 (at 100%)
  - 100%: DS=0.7750  SOR=0.1775  WPC=0.2724  Hausdorff: 0.1318
  - 50%: DS=0.7814  SOR=0.1777  WPC=0.2595  Hausdorff: 0.1329
  - 25%: DS=0.7964  SOR=0.1784  WPC=0.2289  Hausdorff: 0.1346

### luma_turnaround vs glitch_turnaround — **PASS**
  - Worst DS: 1.0000 (at None)
  - 100%: DS=1.0000  SOR=0.0512  WPC=-0.0771  Hausdorff: 0.2133
  - 50%: DS=1.0000  SOR=0.0503  WPC=-0.0571  Hausdorff: 0.2131
  - 25%: DS=1.0000  SOR=0.0329  WPC=-0.1165  Hausdorff: 0.2118

### cosmo_turnaround vs miri_turnaround — **FAIL**
  - Worst DS: 0.0353 (at 25%)
  - 100%: DS=0.0353  SOR=0.9294  WPC=1.0000  Hausdorff: 0.0000
  - 50%: DS=0.0362  SOR=0.9276  WPC=1.0000  Hausdorff: 0.0000
  - 25%: DS=0.0353  SOR=0.9295  WPC=1.0000  Hausdorff: 0.0000

### cosmo_turnaround vs byte_turnaround — **PASS**
  - Worst DS: 0.8734 (at 25%)
  - 100%: DS=0.8921  SOR=0.1050  WPC=0.1109  Hausdorff: 0.1313
  - 50%: DS=0.8915  SOR=0.1051  WPC=0.1120  Hausdorff: 0.1320
  - 25%: DS=0.8734  SOR=0.1089  WPC=0.1443  Hausdorff: 0.1454

### cosmo_turnaround vs glitch_turnaround — **PASS**
  - Worst DS: 0.9845 (at 100%)
  - 100%: DS=0.9845  SOR=0.0979  WPC=-0.6695  Hausdorff: 0.2170
  - 50%: DS=0.9858  SOR=0.0959  WPC=-0.6582  Hausdorff: 0.2176
  - 25%: DS=0.9873  SOR=0.0901  WPC=-0.6743  Hausdorff: 0.2147

### miri_turnaround vs byte_turnaround — **WARN**
  - Worst DS: 0.2739 (at 25%)
  - 100%: DS=0.2761  SOR=0.4479  WPC=1.0000  Hausdorff: 0.0000
  - 50%: DS=0.2758  SOR=0.4484  WPC=1.0000  Hausdorff: 0.0000
  - 25%: DS=0.2739  SOR=0.4521  WPC=1.0000  Hausdorff: 0.0000

### miri_turnaround vs glitch_turnaround — **WARN**
  - Worst DS: 0.2036 (at 50%)
  - 100%: DS=0.2044  SOR=0.5911  WPC=1.0000  Hausdorff: 0.0000
  - 50%: DS=0.2036  SOR=0.5927  WPC=1.0000  Hausdorff: 0.0000
  - 25%: DS=0.2110  SOR=0.5780  WPC=1.0000  Hausdorff: 0.0000

### byte_turnaround vs glitch_turnaround — **PASS**
  - Worst DS: 0.9662 (at 25%)
  - 100%: DS=0.9688  SOR=0.0645  WPC=-0.4593  Hausdorff: 0.1521
  - 50%: DS=0.9670  SOR=0.0681  WPC=-0.4689  Hausdorff: 0.1521
  - 25%: DS=0.9662  SOR=0.0719  WPC=-0.4645  Hausdorff: 0.1543

---

## 16. Expression Range Metric — Facial Variation — **WARN**

_Measures expression variation across expression sheet panels using Face Region Pixel Delta (FRPD) and Structural Change Index (SCI). Aggregate Expression Range Score (ERS) = mean FRPD across all pairs. PASS: ERS >= 0.10. WARN: ERS 0.05-0.10. FAIL: ERS < 0.05._

PASS: 4  WARN: 1  FAIL: 0  Skip: 0

### Luma Expressions — **PASS**
  - Grid: 3x3  Valid panels: 9  ERS: 0.3191  Verdict: PASS
  - Pairs: 36 total — PASS: 36  WARN: 0  FAIL: 0

### Byte Expressions — **PASS**
  - Grid: 4x3  Valid panels: 10  ERS: 0.2598  Verdict: PASS
  - Pairs: 45 total — PASS: 35  WARN: 9  FAIL: 1

### Cosmo Expressions — **PASS**
  - Grid: 3x3  Valid panels: 9  ERS: 0.2137  Verdict: PASS
  - Pairs: 36 total — PASS: 29  WARN: 7  FAIL: 0

### Glitch Expressions — **WARN**
  - Grid: 3x3  Valid panels: 6  ERS: 0.0672  Verdict: WARN
  - Pairs: 15 total — PASS: 3  WARN: 12  FAIL: 0

### Miri Expressions — **PASS**
  - Grid: 3x3  Valid panels: 9  ERS: 0.2715  Verdict: PASS
  - Pairs: 36 total — PASS: 33  WARN: 3  FAIL: 0

---

## 17. Construction Stiffness — Organic Shape Quality — **WARN**

_Detects overly straight/rectangular character construction via contour straightness analysis. Uses skimage sub-pixel contours + Shapely when available. Stiffness Score = 0.6*straight_pct + 0.4*(longest_run/total). PASS: SS <= 0.25. WARN: SS 0.25-0.40. FAIL: SS > 0.40._

PASS: 4  WARN: 1  FAIL: 0  Skip: 0

### Luma Turnaround — **WARN**
  - Stiffness: 0.2811  Straight%: 45.1%  Longest run: 560px  Total outline: 21525px
  - Backend: skimage+shapely

### Cosmo Turnaround — **PASS**
  - Stiffness: 0.1734  Straight%: 28.5%  Longest run: 82px  Total outline: 15027px
  - Backend: skimage+shapely

### Miri Turnaround — **PASS**
  - Stiffness: 0.2476  Straight%: 40.6%  Longest run: 188px  Total outline: 20302px
  - Backend: skimage+shapely

### Byte Turnaround — **PASS**
  - Stiffness: 0.1153  Straight%: 18.9%  Longest run: 20px  Total outline: 4962px
  - Backend: skimage+shapely

### Glitch Turnaround — **PASS**
  - Stiffness: 0.1123  Straight%: 17.9%  Longest run: 65px  Total outline: 5272px
  - Backend: skimage+shapely

---

*Generated by LTG_TOOL_precritique_qa.py v3.0.0 — Kai Nakamura (C52: Sections 15/16/17 Character Quality Metrics); Morgan Walsh (C49: Section 14 Sightline Validation added); Lee Tanaka (C48: Section 12 per-asset band overrides); Kai Nakamura (C48: Section 13 Warm Pixel Percentage added); Rin Yamamoto (C44: Section 11 UV_PURPLE Dominance Lint); Ryo Hasegawa (C46: motion spec dark-sheet fix, C45: glitch motion); Rin Yamamoto (C43: SF04 FILL_LIGHT_ASSETS path fix)*