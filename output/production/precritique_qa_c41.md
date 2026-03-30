# Pre-Critique QA Report — C41

**Run date:** 2026-03-30 02:28
**Script:** LTG_TOOL_precritique_qa.py v2.9.0

---

## Overall Result

**WARN** — PASS: 259  WARN: 31  FAIL: 0

| Section | Result | PASS | WARN | FAIL |
|---|---|---|---|---|
| Render QA (pitch PNGs)         | WARN   | 0  | 6  | 0  |
| Color Verify (style frames)    | WARN | 0 | 4 | 0 |
| Proportion Verify (char sheets)| WARN  | 1  | 3  | 0  |
| Stub Linter (tools dir)        | PASS   | 118   | 0   | 0   |
| Palette Warmth Lint            | PASS| 17| 0| 0|
| Glitch Spec Lint               | WARN | 3 | 13 | 0 |
| README Script Index Sync       | PASS | 113 | 0 | 0 |
| Motion Spec Lint               | WARN | 7 | 5 | 0 |

---

## 0. Delta Report

**Delta since last run (C41 @ 2026-03-30 02:26): +0 FAIL, -4 WARN, -4 resolved**

_Compared against: C41 run @ 2026-03-30 02:26_

**Resolved since last run (previously WARN/FAIL, now PASS):**
  - [README Sync] - UNLISTED: `LTG_TOOL_colorkey_glitch_covetous_gen.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P03.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P06.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_cold_open_P08.py` (on disk, not in README Script Index)

---

## 1. Render QA — Pitch PNGs — **WARN**

PASS: 0  WARN: 6  FAIL: 0  Missing: 0


Target files:
  - `LTG_COLOR_styleframe_discovery.png` (found)
  - `LTG_COLOR_styleframe_glitch_storm.png` (found)
  - `LTG_COLOR_styleframe_otherside.png` (found)
  - `LTG_COLOR_styleframe_luma_byte.png` (found)
  - `LTG_BRAND_logo.png` (found)
  - `storyboard_pitch_export.png` (found)

**Flagged items:**
  - LTG_COLOR_styleframe_discovery.png / color_fidelity: WARN
  - LTG_COLOR_styleframe_glitch_storm.png / color_fidelity: WARN
  - LTG_COLOR_styleframe_otherside.png / color_fidelity: WARN
  - LTG_COLOR_styleframe_luma_byte.png / color_fidelity: WARN
  - LTG_COLOR_styleframe_luma_byte.png / warm_cool: WARN — Flat palette — warm/cool separation is 1.1 PIL units (minimum 12.0 required)
  - LTG_BRAND_logo.png / color_fidelity: WARN
  - storyboard_pitch_export.png / color_fidelity: WARN


## 2. Color Verify — Style Frames — **WARN**

PASS: 0  WARN: 4  FAIL: 0  Missing: 0


**Flagged items:**
  - LTG_COLOR_styleframe_discovery.png / BYTE_TEAL: LAB ΔE=22.83 (threshold=5.0)
  - LTG_COLOR_styleframe_discovery.png / UV_PURPLE: LAB ΔE=36.19 (threshold=5.0)
  - LTG_COLOR_styleframe_discovery.png / HOT_MAGENTA: LAB ΔE=17.89 (threshold=5.0)
  - LTG_COLOR_styleframe_discovery.png / SUNLIT_AMBER: LAB ΔE=16.76 (threshold=5.0)
  - LTG_COLOR_styleframe_glitch_storm.png / CORRUPT_AMBER: LAB ΔE=10.10 (threshold=5.0)
  - LTG_COLOR_styleframe_glitch_storm.png / BYTE_TEAL: LAB ΔE=21.79 (threshold=5.0)
  - LTG_COLOR_styleframe_glitch_storm.png / UV_PURPLE: LAB ΔE=29.02 (threshold=5.0)
  - LTG_COLOR_styleframe_glitch_storm.png / HOT_MAGENTA: LAB ΔE=11.18 (threshold=5.0)
  - LTG_COLOR_styleframe_glitch_storm.png / ELECTRIC_CYAN: LAB ΔE=11.75 (threshold=5.0)
  - LTG_COLOR_styleframe_glitch_storm.png / SUNLIT_AMBER: LAB ΔE=47.04 (threshold=5.0)
  - LTG_COLOR_styleframe_otherside.png / BYTE_TEAL: LAB ΔE=22.83 (threshold=5.0)
  - LTG_COLOR_styleframe_otherside.png / UV_PURPLE: LAB ΔE=27.78 (threshold=5.0)
  - LTG_COLOR_styleframe_otherside.png / ELECTRIC_CYAN: LAB ΔE=7.68 (threshold=5.0)
  - LTG_COLOR_styleframe_otherside.png / SUNLIT_AMBER: LAB ΔE=44.94 (threshold=5.0)
  - LTG_COLOR_styleframe_luma_byte.png / BYTE_TEAL: LAB ΔE=19.72 (threshold=5.0)
  - LTG_COLOR_styleframe_luma_byte.png / ELECTRIC_CYAN: LAB ΔE=22.83 (threshold=5.0)
  - LTG_COLOR_styleframe_luma_byte.png / SUNLIT_AMBER: LAB ΔE=39.46 (threshold=5.0)


## 3. Proportion Verify — Character Sheets — **WARN**

PASS: 1  WARN: 3  FAIL: 0  Missing: 0


**Flagged items:**
  - LTG_CHAR_luma_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - LTG_CHAR_cosmo_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - LTG_CHAR_miri_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - LTG_CHAR_glitch_turnaround.png: SKIP proportion check (Glitch non-humanoid)


## 4. Stub Linter — output/tools/ — **PASS**

PASS: 118  WARN: 0  FAIL: 0  Missing: 0


_No issues found._


## 5. Palette Warmth Lint — master_palette.md — **PASS**

PASS: 17  WARN: 0  FAIL: 0  Missing: 0


_No issues found._


## 6. Glitch Spec Lint — Generators — **WARN**

PASS: 3  WARN: 13  FAIL: 0  Missing: 0


_(Non-Glitch files: 102 skipped)_

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
  - LTG_TOOL_color_verify.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - LTG_TOOL_color_verify.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_fidelity_check_c24.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - LTG_TOOL_fidelity_check_c24.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_glitch_color_model.py: G006: Possible organic/warm fill detected — fill=(200, 160, 80). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - LTG_TOOL_glitch_turnaround.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_sf_covetous_glitch.py: G001: rx=68 is outside spec range [28–56] (spec ref: 34)
  - LTG_TOOL_sf_covetous_glitch.py: G001: rx=68 is outside spec range [28–56] (spec ref: 34)
  - LTG_TOOL_sf_covetous_glitch.py: G001: rx=68 is outside spec range [28–56] (spec ref: 34)
  - LTG_TOOL_sf_covetous_glitch.py: G001: ry=76 is outside spec range [28–64] (spec ref: 38)
  - LTG_TOOL_sf_covetous_glitch.py: G001: ry=76 is outside spec range [28–64] (spec ref: 38)
  - LTG_TOOL_sf_covetous_glitch.py: G004: Draw order FAIL — HOT_MAG crack line appears BEFORE body fill polygon. Crack must be drawn after fill (spec §2.3 stacking order).
  - LTG_TOOL_sf_covetous_glitch.py: G008: Interior states (YEARNING/COVETOUS/HOLLOW) detected but no bilateral eye rule found. Spec §6.3: interior states require IDENTICAL left+right eye glyphs — asymmetric destabilization must be SKIPPED for these states.
  - LTG_TOOL_style_frame_02_glitch_storm.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_style_frame_03_other_side.py: G004: Draw order FAIL — HOT_MAG crack line appears BEFORE body fill polygon. Crack must be drawn after fill (spec §2.3 stacking order).
  - LTG_TOOL_style_frame_03_other_side.py: G008: Interior states (YEARNING/COVETOUS/HOLLOW) detected but no bilateral eye rule found. Spec §6.3: interior states require IDENTICAL left+right eye glyphs — asymmetric destabilization must be SKIPPED for these states.


## 7. README Script Index Sync — **PASS**

PASS: 113  WARN: 0  FAIL: 0  Missing: 0


_(Tools on disk: 113  |  Tools listed in README: 230)_

_No issues found._


## 8. Motion Spec Lint — motion sheets — **WARN**

PASS: 7  WARN: 5  FAIL: 0  Missing: 0


Target sheets:
  - `LTG_CHAR_luma_motion.png` (expected 3 panels, found)
  - `LTG_CHAR_byte_motion.png` (expected 4 panels, found)

**Flagged items:**
  - LTG_CHAR_luma_motion.png: WARN: annotation_occupancy: P1: 4.4% occupancy  |  P2: 0.8% occupancy — WARN low  |  P3: 3.1% occupancy — WARN low
  - LTG_CHAR_luma_motion.png: WARN: beat_badges: beat badge occupancy  P1: 13.5% — WARN no badge  |  P2: 0.3% — WARN no badge  |  P3: 40.6%
  - LTG_CHAR_byte_motion.png: WARN: annotation_occupancy: P1: 0.0% occupancy — WARN low  |  P2: 0.0% occupancy — WARN low  |  P3: 0.0% occupancy — WARN low  |  P4: 4.8% occupancy
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

### SF04 Luma+Byte (fill light adapter — SF04 scene preset)
  - *SKIP — Base image not found: LTG_COLOR_styleframe_luma_byte_nolight.png*

---

*Generated by LTG_TOOL_precritique_qa.py v2.9.0 — Morgan Walsh (C41: cycle bump, CYCLE_LABEL=C41)*