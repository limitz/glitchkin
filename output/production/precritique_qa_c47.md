# Pre-Critique QA Report — C47

**Run date:** 2026-03-30 15:39
**Script:** LTG_TOOL_precritique_qa.py v2.11.0

---

## Overall Result

**FAIL** — PASS: 359  WARN: 36  FAIL: 1

> **README SYNC WARNING:** 5 discrepancy(ies) detected — 5 UNLISTED, 0 GHOST. See Section 7 for details. Update README Script Index before critique.


| Section | Result | PASS | WARN | FAIL |
|---|---|---|---|---|
| Render QA (pitch PNGs)         | WARN   | 0  | 6  | 0  |
| Color Verify (style frames)    | WARN | 0 | 4 | 0 |
| Proportion Verify (char sheets)| FAIL  | 1  | 2  | 1  |
| Stub Linter (tools dir)        | PASS   | 156   | 0   | 0   |
| Palette Warmth Lint            | PASS| 17| 0| 0|
| Glitch Spec Lint               | WARN | 7 | 15 | 0 |
| README Script Index Sync       | WARN | 146 | 5 | 0 |
| Motion Spec Lint               | WARN | 32 | 4 | 0 |
| Alpha Blend Lint               | PASS | 0 | 0 | 0 |
| UV_PURPLE Dominance Lint       | WARN   | 3   | 3   | 0   |
| Depth Temperature Lint         | FAIL   | 1   | 2   | 2   |

---

## 0. Delta Report

**Delta since last run (C47 @ 2026-03-30 15:38): +1 FAIL, -2 WARN, -3 resolved**

_Compared against: C47 run @ 2026-03-30 15:38_

**New FAILs since last run:**
  - [Proportion Verify] - LTG_CHAR_cosmo_turnaround.png: FAIL — ratio=17.84 (spec=3.2, tol=±5%)

**New WARNs since last run:**
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P13.py` (on disk, not in README Script Index)

**Resolved since last run (previously WARN/FAIL, now PASS):**
  - [Proportion Verify] - LTG_CHAR_cosmo_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - [README Sync] - UNLISTED: `LTG_TOOL_scanline_pitch_extract.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_styleframe_glitch_layer_showcase.py` (on disk, not in README Script Index)

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
  - storyboard_pitch_export.png / color_fidelity: WARN


## 2. Color Verify — Style Frames — **WARN**

PASS: 0  WARN: 4  FAIL: 0  Missing: 0


**Flagged items:**
  - LTG_COLOR_styleframe_discovery.png / BYTE_TEAL: LAB ΔE=22.83 (threshold=5.0)
  - LTG_COLOR_styleframe_discovery.png / UV_PURPLE: LAB ΔE=36.19 (threshold=5.0)
  - LTG_COLOR_styleframe_discovery.png / HOT_MAGENTA: LAB ΔE=17.89 (threshold=5.0)
  - LTG_COLOR_styleframe_discovery.png / SUNLIT_AMBER: LAB ΔE=16.76 (threshold=5.0)
  - LTG_COLOR_styleframe_glitch_storm.png / CORRUPT_AMBER: LAB ΔE=8.77 (threshold=5.0)
  - LTG_COLOR_styleframe_glitch_storm.png / BYTE_TEAL: LAB ΔE=22.83 (threshold=5.0)
  - LTG_COLOR_styleframe_glitch_storm.png / UV_PURPLE: LAB ΔE=9.80 (threshold=5.0)
  - LTG_COLOR_styleframe_glitch_storm.png / HOT_MAGENTA: LAB ΔE=6.08 (threshold=5.0)
  - LTG_COLOR_styleframe_glitch_storm.png / ELECTRIC_CYAN: LAB ΔE=10.25 (threshold=5.0)
  - LTG_COLOR_styleframe_glitch_storm.png / SUNLIT_AMBER: LAB ΔE=26.48 (threshold=5.0)
  - LTG_COLOR_styleframe_otherside.png / BYTE_TEAL: LAB ΔE=22.83 (threshold=5.0)
  - LTG_COLOR_styleframe_otherside.png / SUNLIT_AMBER: LAB ΔE=44.94 (threshold=5.0)
  - LTG_COLOR_styleframe_sf04.png / BYTE_TEAL: LAB ΔE=30.53 (threshold=5.0)
  - LTG_COLOR_styleframe_sf04.png / SUNLIT_AMBER: LAB ΔE=31.29 (threshold=5.0)


## 3. Proportion Verify — Character Sheets — **FAIL**

PASS: 1  WARN: 2  FAIL: 1  Missing: 0


**Flagged items:**
  - LTG_CHAR_luma_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - LTG_CHAR_cosmo_turnaround.png: FAIL — ratio=17.84 (spec=3.2, tol=±5%)
  - LTG_CHAR_miri_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - LTG_CHAR_glitch_turnaround.png: SKIP proportion check (Glitch non-humanoid)


## 4. Stub Linter — output/tools/ — **PASS**

PASS: 156  WARN: 0  FAIL: 0  Missing: 0


_No issues found._


## 5. Palette Warmth Lint — master_palette.md — **PASS**

PASS: 17  WARN: 0  FAIL: 0  Missing: 0


_No issues found._


## 6. Glitch Spec Lint — Generators — **WARN**

PASS: 7  WARN: 15  FAIL: 0  Missing: 0


_(Non-Glitch files: 134 skipped)_

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
  - LTG_TOOL_style_frame_02_glitch_storm.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_style_frame_03_other_side.py: G004: Draw order FAIL — HOT_MAG crack line appears BEFORE body fill polygon. Crack must be drawn after fill (spec §2.3 stacking order).
  - LTG_TOOL_style_frame_03_other_side.py: G008: Interior states (YEARNING/COVETOUS/HOLLOW) detected but no bilateral eye rule found. Spec §6.3: interior states require IDENTICAL left+right eye glyphs — asymmetric destabilization must be SKIPPED for these states.
  - LTG_TOOL_style_frame_04_resolution.py: G006: Possible organic/warm fill detected — fill=(175, 140, 95). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_style_frame_04_resolution.py: G006: Possible organic/warm fill detected — fill=(190, 140, 70). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_style_frame_04_resolution.py: G006: Possible organic/warm fill detected — fill=(160, 155, 148). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_styleframe_glitch_layer_showcase.py: G004: Draw order FAIL — HOT_MAG crack line appears BEFORE body fill polygon. Crack must be drawn after fill (spec §2.3 stacking order).


## 7. README Script Index Sync — **WARN**

PASS: 146  WARN: 5  FAIL: 0  Missing: 0


_(Tools on disk: 151  |  Tools listed in README: 266)_

> **ACTION REQUIRED:** 5 tool(s) on disk not listed in README and 0 README entry(ies) with no corresponding file. Update `output/tools/README.md` Script Index before next critique cycle.

**Flagged items:**
  - UNLISTED: `LTG_TOOL_batch_path_migrate.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_face_metric_calibrate.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P13.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P18.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P19.py` (on disk, not in README Script Index)


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
  - LTG_CHAR_luma_motion.png: WARN: beat_badges: beat badge occupancy  P1: 13.5% — WARN no badge  |  P2: 16.5%  |  P3: 3.1% — WARN no badge  |  P4: 19.0%
  - LTG_CHAR_byte_motion.png: WARN: annotation_occupancy: [bg:dark-bright]  P1: 0.0% occupancy — WARN low  |  P2: 0.0% occupancy — WARN low  |  P3: 0.0% occupancy — WARN low  |  P4: 5.3% occupancy
  - LTG_CHAR_byte_motion.png: WARN: beat_badges: beat badge occupancy  P1: 0.0% — WARN no badge  |  P2: 0.0% — WARN no badge  |  P3: 0.0% — WARN no badge  |  P4: 0.0% — WARN no badge
  - LTG_CHAR_byte_motion.png: WARN: timing_colors: BEAT_COLOR [config] in 0/4 panels (0%)


## 9. Arc-Diff Gate — Contact Sheet Changelog

_Informational only — does not affect overall PASS/WARN/FAIL score._
_WARN = panel removed (story continuity risk). NOTE = changed panels (critics: prioritize review of these)._

### Act 2 contact sheet v005→v006
  - OLD panels: 12  NEW panels: 12  SAME: 12  CHANGED: 0  ADDED: 0  REMOVED: 0
  - Arc-diff PNG: `arc_diff_act2_c39.png`
  - _PASS: 12 panel(s) unchanged, 0 changed, 0 added, 0 removed._

### Act 1 cold open contact sheet v001→v002
  - OLD panels: 35  NEW panels: 35  SAME: 35  CHANGED: 0  ADDED: 0  REMOVED: 0
  - Arc-diff PNG: `arc_diff_act1_c39.png`
  - _PASS: 35 panel(s) unchanged, 0 changed, 0 added, 0 removed._

---

## 10. Alpha Blend Lint — Fill-Light Composition — **PASS**

_Checks fill-light blending quality on composited style frames. Requires unlit base images (`*_nolight.png`) alongside composited outputs. FLAT_FILL = FAIL (no radial falloff). LOW_SIGNAL = WARN (fill too subtle). Assets skip gracefully when base is absent — not a defect._

PASS: 0  WARN: 0  FAIL: 0  Skipped: 3

### SF01 Discovery (Luma — warm lamp fill)
  - *SKIP — Base image not found: LTG_COLOR_styleframe_discovery_nolight.png*

### SF02 Glitch Storm (Luma/Byte/Cosmo — HOT_MAGENTA fill)
  - *SKIP — Base image not found: LTG_COLOR_styleframe_glitch_storm_nolight.png*

### SF04 Resolution (Jordan C42 canonical — warm light + cool floor bounce)
  - *SKIP — Base image not found: LTG_COLOR_styleframe_sf04_nolight.png*

---

## 11. UV_PURPLE Dominance Lint — Glitch Layer Colour Balance — **WARN**

_Verifies UV_PURPLE (#7B2FBE) + ELEC_CYAN (#00F0FF) are the dominant colours in Glitch Layer images. Core world-rule: Glitch Layer = UV_PURPLE/ELEC_CYAN dominant, zero warm light. Check A: combined fraction of non-black pixels — PASS ≥ 20%, WARN 10–19%, FAIL < 10%. Check B: warm-hue contamination (LAB h° 30°–80°, chroma C* ≥ 8) — PASS < 5%, WARN ≥ 5%._

PASS: 3  WARN: 3  FAIL: 0  Skip: 0

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

PASS: 1  WARN: 2  FAIL: 2  Skip: 1

### Character Lineup — **PASS**
  - FG warmth: 32.2  BG warmth: 3.4  separation: 28.8  threshold: 12.0

### SF05 The Passing — **FAIL**
  - FG warmth: 3.0  BG warmth: 13.3  separation: -10.3  threshold: 12.0

### SF06 The Hand-Off — **WARN**
  - FG warmth: 64.0  BG warmth: 53.0  separation: 11.0  threshold: 12.0

### SF04 Resolution — **FAIL**
  - FG warmth: 12.9  BG warmth: 24.1  separation: -11.2  threshold: 12.0
  - World type: REAL

### SF02 Glitch Storm — **WARN**
  - FG warmth: -24.5  BG warmth: -25.6  separation: 1.1  threshold: 3.0
  - World type: REAL_STORM

### COVETOUS Style Frame — *SKIP*
  - *SKIP — SKIP: GLITCH scene exempt from Depth Temperature Rule*

---

*Generated by LTG_TOOL_precritique_qa.py v2.15.0 — Lee Tanaka (C47: Section 12 Depth Temperature Lint added); Rin Yamamoto (C44: Section 11 UV_PURPLE Dominance Lint); Ryo Hasegawa (C46: motion spec dark-sheet fix, C45: glitch motion); Rin Yamamoto (C43: SF04 FILL_LIGHT_ASSETS path fix)*