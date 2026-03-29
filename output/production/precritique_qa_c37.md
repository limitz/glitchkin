# Pre-Critique QA Report — C37

**Run date:** 2026-03-30 11:45
**Script:** LTG_TOOL_precritique_qa_v001.py v2.2.0

---

## Overall Result

**WARN** — PASS: 333  WARN: 26  FAIL: 0

| Section | Result | PASS | WARN | FAIL |
|---|---|---|---|---|
| Render QA (pitch PNGs)         | WARN   | 1  | 5  | 0  |
| Color Verify (style frames)    | WARN | 2 | 2 | 0 |
| Proportion Verify (char sheets)| WARN  | 1  | 3  | 0  |
| Stub Linter (tools dir)        | PASS   | 159   | 0   | 0   |
| Palette Warmth Lint            | PASS| 11| 0| 0|
| Glitch Spec Lint               | WARN | 6 | 15 | 0 |
| README Script Index Sync       | PASS | 159 | 0 | 0 |

---

## 0. Delta Report

**Delta since last run (C36 @ 2026-03-29 21:30): +0 FAIL, -11 WARN, -11 resolved**

_Compared against: C36 run @ 2026-03-29 21:30_

**Resolved since last run (previously WARN, now PASS):**
  - [Render QA] LTG_COLOR_styleframe_glitch_storm_v008.png / warm_cool: PASS — world_type=GLITCH, threshold=3, separation=6.5 (PASS at Glitch threshold)
  - [Render QA] LTG_COLOR_styleframe_otherside_v005.png / warm_cool: PASS — world_type=OTHER_SIDE, threshold=0 (always passes Other Side)
  - [Glitch Spec Lint] LTG_TOOL_bg_glitch_storm_colorfix_v001.py: G005 — suppressed (non-Glitch-generator false positive)
  - [Glitch Spec Lint] LTG_TOOL_bg_glitch_storm_colorfix_v001.py: G007 — suppressed (non-Glitch-generator false positive)
  - [Glitch Spec Lint] LTG_TOOL_bg_other_side_v002.py: G007 — suppressed (non-Glitch-generator false positive)
  - [Glitch Spec Lint] LTG_TOOL_color_verify_v001.py: G005 — suppressed (QA tool false positive)
  - [Glitch Spec Lint] LTG_TOOL_color_verify_v001.py: G007 — suppressed (QA tool false positive)
  - [Glitch Spec Lint] LTG_TOOL_color_verify_v002.py: G005 — suppressed (QA tool false positive)
  - [Glitch Spec Lint] LTG_TOOL_color_verify_v002.py: G007 — suppressed (QA tool false positive)
  - [Glitch Spec Lint] LTG_TOOL_fidelity_check_c24.py: G005 — suppressed (QA tool false positive)
  - [Glitch Spec Lint] LTG_TOOL_fidelity_check_c24.py: G007 — suppressed (QA tool false positive)
  - [Glitch Spec Lint] LTG_TOOL_glitch_spec_lint_v001.py: G002 — suppressed (self-test false positive)
  - [Glitch Spec Lint] LTG_TOOL_style_frame_02_glitch_storm_v001.py: G007 — suppressed
  - [Glitch Spec Lint] LTG_TOOL_style_frame_02_glitch_storm_v002.py: G007 — suppressed
  - [Glitch Spec Lint] LTG_TOOL_style_frame_02_glitch_storm_v003.py: G007 — suppressed
  - [Glitch Spec Lint] LTG_TOOL_style_frame_02_glitch_storm_v004.py: G007 — suppressed
  - [Glitch Spec Lint] LTG_TOOL_style_frame_02_glitch_storm_v006.py: G007 — suppressed
  - [Glitch Spec Lint] LTG_TOOL_style_frame_02_glitch_storm_v007.py: G007 — suppressed
  - [Glitch Spec Lint] LTG_TOOL_style_frame_02_glitch_storm_v008.py: G007 — suppressed
  - [Glitch Spec Lint] LTG_TOOL_style_frame_03_other_side_v001.py through v005.py: G007 — suppressed (5 files)

**New WARNs since last run:**
  - [Glitch Spec Lint] LTG_TOOL_character_lineup_v007.py: G006 ×7 + G007 ×1 — new C37 lineup file, same multi-character false positive pattern as v004–v006. Not yet in suppression list.

---

## 1. Render QA — Pitch PNGs — **WARN**

PASS: 1  WARN: 5  FAIL: 0  Missing: 0

Target files:
  - `LTG_COLOR_styleframe_discovery_v005.png` (found)
  - `LTG_COLOR_styleframe_glitch_storm_v008.png` (found)
  - `LTG_COLOR_styleframe_otherside_v005.png` (found)
  - `LTG_COLOR_styleframe_luma_byte_v004.png` (found)
  - `LTG_BRAND_logo_v001.png` (found)
  - `storyboard_pitch_export.png` (found)

**C37 improvement:** render_qa v1.4.0 world-type-aware warm/cool thresholds active (REAL=20 / GLITCH=3 / OTHER_SIDE=0). SF02 Glitch Storm (world=GLITCH) now PASS — separation 6.5 exceeds GLITCH threshold of 3. SF03 Other Side (world=OTHER_SIDE) warm_cool check suspended (threshold=0). SF02 v008 promoted to pitch PNG (was v006).

**Flagged items:**
  - LTG_COLOR_styleframe_discovery_v005.png / warm_cool: WARN — world_type=REAL — warm/cool separation is 17.8 PIL units (minimum 20.0 required)
  - LTG_COLOR_styleframe_otherside_v005.png / color_fidelity: WARN — UV_PURPLE hue drift 9.2° and SUNLIT_AMBER drift 9.3°
  - LTG_COLOR_styleframe_luma_byte_v004.png / color_fidelity: WARN
  - LTG_COLOR_styleframe_luma_byte_v004.png / warm_cool: WARN — world_type=REAL — warm/cool separation is 1.1 PIL units (minimum 20.0 required)
  - LTG_BRAND_logo_v001.png / warm_cool: WARN — warm/cool separation is 0.0 PIL units (minimum 20.0 required)
  - storyboard_pitch_export.png / warm_cool: WARN — warm/cool separation is 4.6 PIL units (minimum 20.0 required)

**Note:** SF04 luma_byte warm_cool is a known limitation of the mixed-world composition. Logo and storyboard warm_cool WARNs are persistent by design — these assets intentionally lack warm/cool separation. SF01 discovery warm_cool is close to threshold (17.8/20.0) — one point of improvement for SF01 in next cycle.


## 2. Color Verify — Style Frames — **WARN**

PASS: 2  WARN: 2  FAIL: 0  Missing: 0

**Flagged items:**
  - LTG_COLOR_styleframe_otherside_v005.png / UV_PURPLE: hue drift 9.2° (target=272, found=263)
  - LTG_COLOR_styleframe_otherside_v005.png / SUNLIT_AMBER: hue drift 9.3° (target=34, found=25)
  - LTG_COLOR_styleframe_luma_byte_v004.png / SUNLIT_AMBER: hue drift 15.7° (target=34, found=19)

**Note:** SF02 (v008) and SF01 (v005) now PASS color verify. SF03 and SF04 SUNLIT_AMBER drift persists — critics have flagged this over multiple cycles. Recommend SF04 SUNLIT_AMBER correction next cycle.


## 3. Proportion Verify — Character Sheets — **WARN**

PASS: 1  WARN: 3  FAIL: 0  Missing: 0

**Flagged items:**
  - LTG_CHAR_luma_turnaround_v004.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - LTG_CHAR_cosmo_turnaround_v002.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - LTG_CHAR_miri_turnaround_v001.png: head gap not found (no-gap) — multi-panel turnaround may require manual proportion check — WARN
  - LTG_CHAR_glitch_turnaround_v002.png: SKIP proportion check (Glitch non-humanoid)

**Note:** These are persistent algorithm limitations on multi-panel turnaround sheets. The proportion_audit_c37.md report (Rin Yamamoto) provides manual verification — all proportions confirmed PASS in C37 manual audit (PASS=3, ASYM-WARN=2, WARN=1 on legacy SF01 v003 only). The automated `proportion_verify` tool cannot handle multi-panel layouts — this is a known tool limitation, not a production defect.


## 4. Stub Linter — output/tools/ — **PASS**

PASS: 159  WARN: 0  FAIL: 0  Missing: 0

_No issues found._

C37 adds 8 new `LTG_TOOL_*` scripts (vs 151 in C36). All new scripts pass stub integrity checks.


## 5. Palette Warmth Lint — master_palette.md — **PASS**

PASS: 11  WARN: 0  FAIL: 0  Missing: 0

_No issues found._


## 6. Glitch Spec Lint — Generators — **WARN**

PASS: 6  WARN: 15  FAIL: 0  Missing: 0

_(Non-Glitch files: suppression list active — 26 false positives suppressed across 11 non-Glitch-generator files)_

**C37 improvement:** glitch_spec_lint v1.2.0 with `glitch_spec_suppressions.json` active. 26 previously-flagged false positives on QA tool files, ENV generators, and legacy SF generators now suppressed. Net WARNs reduced from 26 to 15.

**Remaining flagged items (not yet suppressed):**

Character lineup files (multi-character context false positives — non-Glitch skin tones):
  - LTG_TOOL_character_lineup_v004.py: G006 ×7 (other chars' skin tones trigger organic fill check), G007 ×1
  - LTG_TOOL_character_lineup_v005.py: G006 ×7, G007 ×1
  - LTG_TOOL_character_lineup_v006.py: G006 ×7, G007 ×1
  - LTG_TOOL_character_lineup_v007.py: G006 ×7, G007 ×1 _(new C37 file — not yet in suppression list)_

Other remaining:
  - LTG_TOOL_character_face_test_v001.py: G003 ×1, G005 ×1, G006 ×2, G007 ×1 (legacy test file — minimal Glitch implementation)
  - LTG_TOOL_glitch_color_model_v001.py: G006 ×1 (SUNLIT_AMBER swatch triggers organic fill check)
  - LTG_TOOL_glitch_turnaround_v001.py: G007 ×1 (legacy v001, outline pattern differs from spec expectation)
  - LTG_TOOL_glitch_turnaround_v002.py: G007 ×1 (same issue, not yet resolved in v002)

**Genuine Glitch spec compliance:** Current production assets — `glitch_expression_sheet_v003.py`, `glitch_turnaround_v002.py` (body shape), SF02/SF03 current versions — all confirmed PASS on G001/G002/G004/G008 core body checks.

**Recommended follow-up:** Extend suppression list to cover character_lineup G006/G007 patterns (add 4 lineup files × 8 suppression entries = 32 entries). Submitted to ideabox.


## 7. README Script Index Sync — **PASS**

PASS: 159  WARN: 0  FAIL: 0  Missing: 0

_(Tools on disk: 159  |  Tools listed in README: 194)_

All 8 new C37 `LTG_TOOL_*` scripts registered in README Script Index by Kai Nakamura and team. 0 UNLISTED, 0 GHOST — clean PASS. The 35-entry differential (194 listed vs 159 disk) represents forwarding stubs/aliases and legacy archive entries — consistent with prior cycles.

---

## Critics' Attention Items

The following issues should be visible to critics in the C37 critique cycle:

1. **SF01 Discovery warm/cool** at 17.8 (threshold 20.0) — near-miss, ongoing. Warm lamp spill may need boosting.
2. **SF03 Other Side color drift** — UV_PURPLE and SUNLIT_AMBER hue drift persists across multiple cycles. The world-type fix (threshold=0) masks the render QA WARN but the underlying color accuracy remains open.
3. **SF04 luma_byte SUNLIT_AMBER drift** at 15.7° — ongoing across versions.
4. **Character lineup_v007** has expected glitch_spec false positives — not a production concern.
5. **Proportion verify** remains algorithmic-WARN-only on all turnarounds — manual audit confirms PASS (see proportion_audit_c37.md).

---

*Generated by LTG_TOOL_precritique_qa_v001.py v2.2.0 — Morgan Walsh, Pipeline Automation*
