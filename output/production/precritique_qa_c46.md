# Pre-Critique QA Report — C46

**Run date:** 2026-03-30 11:27
**Script:** LTG_TOOL_precritique_qa.py v2.11.0

---

## Overall Result

**WARN** — PASS: 321  WARN: 39  FAIL: 0

> **README SYNC WARNING:** 8 discrepancy(ies) detected — 7 UNLISTED, 1 GHOST. See Section 7 for details. Update README Script Index before critique.


| Section | Result | PASS | WARN | FAIL |
|---|---|---|---|---|
| Render QA (pitch PNGs)         | WARN   | 0  | 6  | 0  |
| Color Verify (style frames)    | WARN | 0 | 4 | 0 |
| Proportion Verify (char sheets)| WARN  | 1  | 3  | 0  |
| Stub Linter (tools dir)        | PASS   | 141   | 0   | 0   |
| Palette Warmth Lint            | PASS| 17| 0| 0|
| Glitch Spec Lint               | WARN | 7 | 14 | 0 |
| README Script Index Sync       | WARN | 129 | 8 | 0 |
| Motion Spec Lint               | WARN | 26 | 4 | 0 |
| Alpha Blend Lint               | PASS | 0 | 0 | 0 |
| UV_PURPLE Dominance Lint       | WARN   | 0   | 1   | 0   |

---

## 0. Delta Report

**Delta since last run (C44 @ 2026-03-30 08:28): +0 FAIL, +7 WARN, -4 resolved**

_Compared against: C44 run @ 2026-03-30 08:28_

**New FAILs since last run:**
  - [Glitch Spec Lint] - LTG_TOOL_glitch_motion.py: G004: Draw order FAIL — HOT_MAG crack line appears BEFORE body fill polygon. Crack must be drawn after fill (spec §2.3 stacking order).

**New WARNs since last run:**
  - [Render QA] - LTG_COLOR_styleframe_sf04.png / line_weight: WARN — Line weight inconsistency — 3 outlier widths detected (mean=241.6px, std=458.0px)
  - [Color Verify] - LTG_COLOR_styleframe_sf04.png / SUNLIT_AMBER: LAB ΔE=31.29 (threshold=5.0)
  - [Glitch Spec Lint] - LTG_TOOL_glitch_motion.py: G003: Multi-Glitchkin frame has only 0 unique expression(s) — at least 2 required. Found: none
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_04_resolution.py: G006: Possible organic/warm fill detected — fill=(160, 155, 148). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_04_resolution.py: G006: Possible organic/warm fill detected — fill=(175, 140, 95). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_04_resolution.py: G006: Possible organic/warm fill detected — fill=(190, 140, 70). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [README Sync] - GHOST: `LTG_TOOL_style_frame_01_discovery.py` (in README, not on disk)
  - [README Sync] - UNLISTED: `LTG_TOOL_lineup_tier_depth_sketch.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_caption_retrofit.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P14.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P15.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sf_miri_luma_handoff.py` (on disk, not in README Script Index)
  - [Motion Spec Lint] - LTG_CHAR_byte_motion.png: WARN: annotation_occupancy: [bg:dark-bright]  P1: 0.0% occupancy — WARN low  |  P2: 0.0% occupancy — WARN low  |  P3: 0.0% occupancy — WARN low  |  P4: 5.3% occupancy

**Resolved since last run (previously WARN/FAIL, now PASS):**
  - [Render QA] - LTG_COLOR_styleframe_sf04.png / line_weight: WARN — Line weight inconsistency — 3 outlier widths detected (mean=263.9px, std=449.6px)
  - [Color Verify] - LTG_COLOR_styleframe_sf04.png / SUNLIT_AMBER: LAB ΔE=31.38 (threshold=5.0)
  - [README Sync] - UNLISTED: `LTG_TOOL_sf_covetous_glitch_c43.py` (on disk, not in README Script Index)
  - [Motion Spec Lint] - LTG_CHAR_byte_motion.png: WARN: annotation_occupancy: [bg:legacy-broad]  P1: 0.0% occupancy — WARN low  |  P2: 0.0% occupancy — WARN low  |  P3: 0.0% occupancy — WARN low  |  P4: 4.8% occupancy

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


## 3. Proportion Verify — Character Sheets — **WARN**

PASS: 1  WARN: 3  FAIL: 0  Missing: 0


**Flagged items:**
  - LTG_CHAR_luma_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - LTG_CHAR_cosmo_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - LTG_CHAR_miri_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - LTG_CHAR_glitch_turnaround.png: SKIP proportion check (Glitch non-humanoid)


## 4. Stub Linter — output/tools/ — **PASS**

PASS: 141  WARN: 0  FAIL: 0  Missing: 0


_No issues found._


## 5. Palette Warmth Lint — master_palette.md — **PASS**

PASS: 17  WARN: 0  FAIL: 0  Missing: 0


_No issues found._


## 6. Glitch Spec Lint — Generators — **WARN**

PASS: 7  WARN: 14  FAIL: 0  Missing: 0


_(Non-Glitch files: 120 skipped)_

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


## 7. README Script Index Sync — **WARN**

PASS: 129  WARN: 8  FAIL: 0  Missing: 0


_(Tools on disk: 136  |  Tools listed in README: 250)_

> **ACTION REQUIRED:** 7 tool(s) on disk not listed in README and 1 README entry(ies) with no corresponding file. Update `output/tools/README.md` Script Index before next critique cycle.

**Flagged items:**
  - UNLISTED: `LTG_TOOL_lineup_tier_depth_sketch.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_caption_retrofit.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P10.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P11.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P14.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sb_cold_open_P15.py` (on disk, not in README Script Index)
  - UNLISTED: `LTG_TOOL_sf_miri_luma_handoff.py` (on disk, not in README Script Index)
  - GHOST: `LTG_TOOL_style_frame_01_discovery.py` (in README, not on disk)


## 8. Motion Spec Lint — motion sheets — **WARN**

PASS: 26  WARN: 4  FAIL: 0  Missing: 0


Target sheets:
  - `LTG_CHAR_luma_motion.png` (expected 4 panels, found)
  - `LTG_CHAR_byte_motion.png` (expected 4 panels, found)
  - `LTG_CHAR_cosmo_motion.png` (expected 4 panels, found)
  - `LTG_CHAR_miri_motion.png` (expected 4 panels, found)
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

PASS: 0  WARN: 1  FAIL: 0  Skip: 0

  - *ERROR — LTG_TOOL_uv_purple_linter could not be loaded*

_No Glitch Layer assets registered._

---

*Generated by LTG_TOOL_precritique_qa.py v2.13.0 — Rin Yamamoto (C44: Section 11 UV_PURPLE Dominance Lint added; world_type_infer v1.2.0); Ryo Hasegawa (C45: glitch motion; C44: cosmo+miri, luma panel count); Rin Yamamoto (C43: SF04 FILL_LIGHT_ASSETS path fix)*