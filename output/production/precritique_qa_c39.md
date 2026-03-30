<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Pre-Critique QA Report — C39

**Run date:** 2026-03-30 01:23
**Script:** LTG_TOOL_precritique_qa.py v2.4.0

---

## Overall Result

**WARN** — PASS: 238  WARN: 32  FAIL: 0

> **README SYNC WARNING:** 1 discrepancy(ies) detected — 1 UNLISTED, 0 GHOST. See Section 7 for details. Update README Script Index before critique.


| Section | Result | PASS | WARN | FAIL |
|---|---|---|---|---|
| Render QA (pitch PNGs)         | WARN   | 0  | 6  | 0  |
| Color Verify (style frames)    | WARN | 0 | 4 | 0 |
| Proportion Verify (char sheets)| WARN  | 1  | 3  | 0  |
| Stub Linter (tools dir)        | PASS   | 109   | 0   | 0   |
| Palette Warmth Lint            | PASS| 17| 0| 0|
| Glitch Spec Lint               | WARN | 2 | 12 | 0 |
| README Script Index Sync       | WARN | 103 | 1 | 0 |
| Motion Spec Lint               | WARN | 6 | 6 | 0 |

---

## 0. Delta Report

**Delta since last run (C39 @ 2026-03-29 23:05): +0 FAIL, -12 WARN, -55 resolved**

_Compared against: C39 run @ 2026-03-29 23:05_

**New WARNs since last run:**
  - [Render QA] - LTG_BRAND_logo.png / color_fidelity: WARN
  - [Render QA] - LTG_BRAND_logo.png / warm_cool: WARN — Flat palette — warm/cool separation is 9.1 PIL units (minimum 12.0 required)
  - [Render QA] - LTG_COLOR_styleframe_discovery.png / color_fidelity: WARN
  - [Render QA] - LTG_COLOR_styleframe_discovery.png / warm_cool: WARN — Flat palette — warm/cool separation is 7.4 PIL units (minimum 12.0 required)
  - [Render QA] - LTG_COLOR_styleframe_glitch_storm.png / color_fidelity: WARN
  - [Render QA] - LTG_COLOR_styleframe_luma_byte.png / color_fidelity: WARN
  - [Render QA] - LTG_COLOR_styleframe_otherside.png / color_fidelity: WARN
  - [Render QA] - storyboard_pitch_export.png / color_fidelity: WARN
  - [Color Verify] - LTG_COLOR_styleframe_discovery.png / BYTE_TEAL: LAB ΔE=22.83 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_discovery.png / HOT_MAGENTA: LAB ΔE=17.89 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_discovery.png / SUNLIT_AMBER: LAB ΔE=16.76 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_discovery.png / UV_PURPLE: LAB ΔE=36.19 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_glitch_storm.png / BYTE_TEAL: LAB ΔE=21.79 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_glitch_storm.png / CORRUPT_AMBER: LAB ΔE=10.10 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_glitch_storm.png / ELECTRIC_CYAN: LAB ΔE=11.75 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_glitch_storm.png / HOT_MAGENTA: LAB ΔE=11.18 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_glitch_storm.png / SUNLIT_AMBER: LAB ΔE=47.04 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_glitch_storm.png / UV_PURPLE: LAB ΔE=29.02 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_luma_byte.png / BYTE_TEAL: LAB ΔE=19.72 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_luma_byte.png / ELECTRIC_CYAN: LAB ΔE=22.83 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_luma_byte.png / SUNLIT_AMBER: LAB ΔE=39.46 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_otherside.png / BYTE_TEAL: LAB ΔE=22.83 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_otherside.png / CORRUPT_AMBER: LAB ΔE=19.44 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_otherside.png / ELECTRIC_CYAN: LAB ΔE=7.68 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_otherside.png / SUNLIT_AMBER: LAB ΔE=44.94 (threshold=5.0)
  - [Color Verify] - LTG_COLOR_styleframe_otherside.png / UV_PURPLE: LAB ΔE=27.78 (threshold=5.0)
  - [Proportion Verify] - LTG_CHAR_cosmo_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - [Proportion Verify] - LTG_CHAR_glitch_turnaround.png: SKIP proportion check (Glitch non-humanoid)
  - [Proportion Verify] - LTG_CHAR_luma_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - [Proportion Verify] - LTG_CHAR_miri_turnaround.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - [Glitch Spec Lint] - LTG_CHAR_byte_motion.py: G003: Multi-Glitchkin frame has only 1 unique expression(s) — at least 2 required. Found: ['NEUTRAL']
  - [Glitch Spec Lint] - LTG_CHAR_byte_motion.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_CHAR_byte_motion.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_bg_glitch_storm_colorfix.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_bg_glitch_storm_colorfix.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_bg_other_side.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_byte_motion.py: G003: Multi-Glitchkin frame has only 0 unique expression(s) — at least 2 required. Found: none
  - [Glitch Spec Lint] - LTG_TOOL_byte_motion.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_byte_motion.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_character_face_test.py: G003: Multi-Glitchkin frame has only 1 unique expression(s) — at least 2 required. Found: ['NEUTRAL']
  - [Glitch Spec Lint] - LTG_TOOL_character_face_test.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_character_face_test.py: G006: Possible organic/warm fill detected — fill=(120, 120, 140). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_character_face_test.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(138, 122, 112). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(168, 152, 140). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(184, 154, 120). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(212, 130, 90). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_character_lineup.py: G006: Possible organic/warm fill detected — fill=(212, 149, 107). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_color_verify.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_color_verify.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_glitch_color_model.py: G006: Possible organic/warm fill detected — fill=(200, 160, 80). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_glitch_turnaround.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_02_glitch_storm.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_03_other_side.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [README Sync] - UNLISTED: `LTG_TOOL_sheet_geometry_calibrate.py` (on disk, not in README Script Index)
  - [Motion Spec Lint] - LTG_CHAR_byte_motion.png: WARN: annotation_occupancy: P1: 0.0% occupancy — WARN low  |  P2: 0.0% occupancy — WARN low  |  P3: 0.0% occupancy — WARN low  |  P4: 4.8% occupancy
  - [Motion Spec Lint] - LTG_CHAR_byte_motion.png: WARN: beat_badges: beat badge occupancy  P1: 0.0% — WARN no badge  |  P2: 0.0% — WARN no badge  |  P3: 0.0% — WARN no badge  |  P4: 0.0% — WARN no badge
  - [Motion Spec Lint] - LTG_CHAR_byte_motion.png: WARN: timing_colors: BEAT_COLOR cyan in 0/4 panels (0%)
  - [Motion Spec Lint] - LTG_CHAR_luma_motion.png: WARN: annotation_occupancy: P1: 4.4% occupancy  |  P2: 0.8% occupancy — WARN low  |  P3: 3.1% occupancy — WARN low
  - [Motion Spec Lint] - LTG_CHAR_luma_motion.png: WARN: beat_badges: beat badge occupancy  P1: 13.5% — WARN no badge  |  P2: 0.3% — WARN no badge  |  P3: 40.6%
  - [Motion Spec Lint] - LTG_CHAR_luma_motion.png: WARN: timing_colors: BEAT_COLOR cyan in 0/3 panels (0%)

**Resolved since last run (previously WARN/FAIL, now PASS):**
  - [Render QA] - LTG_BRAND_logo_v001.png / warm_cool: WARN — Flat palette — warm/cool separation is 0.0 PIL units (minimum 12.0 required)
  - [Render QA] - LTG_COLOR_styleframe_luma_byte_v004.png / color_fidelity: WARN
  - [Render QA] - LTG_COLOR_styleframe_luma_byte_v004.png / warm_cool: WARN — Flat palette — warm/cool separation is 1.1 PIL units (minimum 12.0 required)
  - [Render QA] - LTG_COLOR_styleframe_otherside_v005.png / color_fidelity: WARN
  - [Color Verify] - LTG_COLOR_styleframe_luma_byte_v004.png / SUNLIT_AMBER: hue drift 15.7° (target=34, found=19)
  - [Color Verify] - LTG_COLOR_styleframe_otherside_v005.png / SUNLIT_AMBER: hue drift 9.3° (target=34, found=25)
  - [Color Verify] - LTG_COLOR_styleframe_otherside_v005.png / UV_PURPLE: hue drift 9.2° (target=272, found=263)
  - [Proportion Verify] - LTG_CHAR_cosmo_turnaround_v002.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - [Proportion Verify] - LTG_CHAR_glitch_turnaround_v002.png: SKIP proportion check (Glitch non-humanoid)
  - [Proportion Verify] - LTG_CHAR_luma_turnaround_v004.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - [Proportion Verify] - LTG_CHAR_miri_turnaround_v001.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - [Glitch Spec Lint] - LTG_CHAR_byte_motion_v002.py: G003: Multi-Glitchkin frame has only 1 unique expression(s) — at least 2 required. Found: ['NEUTRAL']
  - [Glitch Spec Lint] - LTG_CHAR_byte_motion_v002.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_CHAR_byte_motion_v002.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_bg_glitch_storm_colorfix_v001.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_bg_glitch_storm_colorfix_v001.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_bg_other_side_v002.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_byte_motion_v001.py: G003: Multi-Glitchkin frame has only 1 unique expression(s) — at least 2 required. Found: ['NEUTRAL']
  - [Glitch Spec Lint] - LTG_TOOL_byte_motion_v001.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_byte_motion_v001.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_byte_motion_v003.py: G003: Multi-Glitchkin frame has only 0 unique expression(s) — at least 2 required. Found: none
  - [Glitch Spec Lint] - LTG_TOOL_byte_motion_v003.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_byte_motion_v003.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_character_face_test_v001.py: G003: Multi-Glitchkin frame has only 1 unique expression(s) — at least 2 required. Found: ['NEUTRAL']
  - [Glitch Spec Lint] - LTG_TOOL_character_face_test_v001.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_character_face_test_v001.py: G006: Possible organic/warm fill detected — fill=(120, 120, 140). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_character_face_test_v001.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_color_verify_v001.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_color_verify_v002.py: G005: UV_PURPLE shadow offset (+3,+4) not detected. Spec §2.2 requires UV_PURPLE shadow polygon before body fill.
  - [Glitch Spec Lint] - LTG_TOOL_glitch_color_model_v001.py: G006: Possible organic/warm fill detected — fill=(200, 160, 80). Glitch body fill must use CORRUPT_AMBER family only (spec §10).
  - [Glitch Spec Lint] - LTG_TOOL_glitch_turnaround_v001.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_glitch_turnaround_v002.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_02_glitch_storm_v001.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_02_glitch_storm_v002.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_02_glitch_storm_v003.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_02_glitch_storm_v004.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_02_glitch_storm_v006.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_02_glitch_storm_v007.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_02_glitch_storm_v008.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_03_other_side_v001.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_03_other_side_v002.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_03_other_side_v003.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_03_other_side_v004.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [Glitch Spec Lint] - LTG_TOOL_style_frame_03_other_side_v005.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - [README Sync] - UNLISTED: `LTG_TOOL_bg_school_hallway_v003.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_costume_bg_clash_v001.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_env_grandma_living_room_v002.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sb_pilot_cold_open_v003.py` (on disk, not in README Script Index)
  - [README Sync] - UNLISTED: `LTG_TOOL_sight_line_diagnostic_v001.py` (on disk, not in README Script Index)
  - [Motion Spec Lint] - LTG_CHAR_byte_motion_v003.png: WARN: annotation_occupancy: P1: 0.0% occupancy — WARN low  |  P2: 0.0% occupancy — WARN low  |  P3: 0.0% occupancy — WARN low  |  P4: 4.5% occupancy
  - [Motion Spec Lint] - LTG_CHAR_byte_motion_v003.png: WARN: beat_badges: beat badge occupancy  P1: 0.0% — WARN no badge  |  P2: 0.0% — WARN no badge  |  P3: 0.0% — WARN no badge  |  P4: 0.0% — WARN no badge
  - [Motion Spec Lint] - LTG_CHAR_byte_motion_v003.png: WARN: timing_colors: BEAT_COLOR cyan in 0/4 panels (0%)
  - [Motion Spec Lint] - LTG_CHAR_luma_motion_v002.png: WARN: annotation_occupancy: P1: 4.2% occupancy  |  P2: 0.8% occupancy — WARN low  |  P3: 3.0% occupancy — WARN low
  - [Motion Spec Lint] - LTG_CHAR_luma_motion_v002.png: WARN: beat_badges: beat badge occupancy  P1: 13.3% — WARN no badge  |  P2: 0.0% — WARN no badge  |  P3: 40.6%
  - [Motion Spec Lint] - LTG_CHAR_luma_motion_v002.png: WARN: timing_colors: BEAT_COLOR cyan in 0/3 panels (0%)

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
  - LTG_COLOR_styleframe_discovery.png / warm_cool: WARN — Flat palette — warm/cool separation is 7.4 PIL units (minimum 12.0 required)
  - LTG_COLOR_styleframe_glitch_storm.png / color_fidelity: WARN
  - LTG_COLOR_styleframe_otherside.png / color_fidelity: WARN
  - LTG_COLOR_styleframe_luma_byte.png / color_fidelity: WARN
  - LTG_BRAND_logo.png / color_fidelity: WARN
  - LTG_BRAND_logo.png / warm_cool: WARN — Flat palette — warm/cool separation is 9.1 PIL units (minimum 12.0 required)
  - storyboard_pitch_export.png / color_fidelity: WARN
  - storyboard_pitch_export.png / warm_cool: WARN — Flat palette — warm/cool separation is 4.6 PIL units (minimum 12.0 required)


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
  - LTG_COLOR_styleframe_otherside.png / CORRUPT_AMBER: LAB ΔE=19.44 (threshold=5.0)
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

PASS: 109  WARN: 0  FAIL: 0  Missing: 0


_No issues found._


## 5. Palette Warmth Lint — master_palette.md — **PASS**

PASS: 17  WARN: 0  FAIL: 0  Missing: 0


_No issues found._


## 6. Glitch Spec Lint — Generators — **WARN**

PASS: 2  WARN: 12  FAIL: 0  Missing: 0


_(Non-Glitch files: 95 skipped)_

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
  - LTG_TOOL_style_frame_02_glitch_storm.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).
  - LTG_TOOL_style_frame_03_other_side.py: G007: VOID_BLACK outline on body polygon not detected. Spec §2.2 requires draw.polygon(pts, outline=VOID_BLACK, width=3).


## 7. README Script Index Sync — **WARN**

PASS: 103  WARN: 1  FAIL: 0  Missing: 0


_(Tools on disk: 104  |  Tools listed in README: 220)_

> **ACTION REQUIRED:** 1 tool(s) on disk not listed in README and 0 README entry(ies) with no corresponding file. Update `output/tools/README.md` Script Index before next critique cycle.

**Flagged items:**
  - UNLISTED: `LTG_TOOL_sheet_geometry_calibrate.py` (on disk, not in README Script Index)


## 8. Motion Spec Lint — motion sheets — **WARN**

PASS: 6  WARN: 6  FAIL: 0  Missing: 0


Target sheets:
  - `LTG_CHAR_luma_motion.png` (expected 3 panels, found)
  - `LTG_CHAR_byte_motion.png` (expected 4 panels, found)

**Flagged items:**
  - LTG_CHAR_luma_motion.png: WARN: annotation_occupancy: P1: 4.4% occupancy  |  P2: 0.8% occupancy — WARN low  |  P3: 3.1% occupancy — WARN low
  - LTG_CHAR_luma_motion.png: WARN: beat_badges: beat badge occupancy  P1: 13.5% — WARN no badge  |  P2: 0.3% — WARN no badge  |  P3: 40.6%
  - LTG_CHAR_luma_motion.png: WARN: timing_colors: BEAT_COLOR cyan in 0/3 panels (0%)
  - LTG_CHAR_byte_motion.png: WARN: annotation_occupancy: P1: 0.0% occupancy — WARN low  |  P2: 0.0% occupancy — WARN low  |  P3: 0.0% occupancy — WARN low  |  P4: 4.8% occupancy
  - LTG_CHAR_byte_motion.png: WARN: beat_badges: beat badge occupancy  P1: 0.0% — WARN no badge  |  P2: 0.0% — WARN no badge  |  P3: 0.0% — WARN no badge  |  P4: 0.0% — WARN no badge
  - LTG_CHAR_byte_motion.png: WARN: timing_colors: BEAT_COLOR cyan in 0/4 panels (0%)


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

*Generated by LTG_TOOL_precritique_qa.py v2.6.0 — Morgan Walsh (arc-diff gate S9 + lineup suppression expansion C39)*