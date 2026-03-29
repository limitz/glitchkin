# Statement of Work — Cycle 13
**Date:** 2026-03-30
**Project:** Luma & the Glitchkin — Cartoon Visual Assets
**Status:** Complete

---

## Work Completed

### Alex Chen — Art Director
- **SF01 ghost Byte fix**: Raised body alpha 55→90, eye glint alpha ~65→105; relocated top-left monitor ghost away from warm lamp contamination zone. Output: `LTG_COLOR_styleframe_discovery_v003.png`
- **Asymmetric logo fix**: "&" now has warm-to-cold gradient treatment; "the/Glitchkin" inter-line gap tightened ~30%. Output: `LTG_BRAND_logo_asymmetric_v002.png`
- **SF02 character composite** (Victoria blocker, resolved): Luma, Byte, Cosmo sprint poses composited into SF02 with Dutch angle applied, Corrupted Amber outlines. Output: `LTG_COLOR_styleframe_glitch_storm_v002.png` via `LTG_TOOL_style_frame_02_glitch_storm_v002.py`
- **Byte cracked-eye dead-pixel glyph**: Designed 7×7 pixel-art dead pixel eye glyph, documented in `byte.md`, reference PNG created: `LTG_CHAR_byte_cracked_eye_glyph_v001.png`. Message sent to Lee Tanaka.
- **ENV-06 TERRA_CYAN_LIT fix**: Incorporated Jordan's corrected value (150,172,162) into SF02 v002 generator
- **CHAR-L-11 registered**: Warm-pixel activation `#E8C95A` (Soft Gold) confirmed and registered; message sent to Sam Kowalski
- **LTG_BRAND_ and LTG_COL_ categories ratified**: Formal entries added to naming convention spec
- **`.gitignore` created**: Added `__pycache__/` exclusion

### Maya Santos — Character Designer
- **Byte neutral expression** (Dmitri P1, overdue, now closed): Created `LTG_TOOL_byte_expression_sheet_v001.py` — 4×2 layout (7 expressions + 1 reserved). Neutral: flat left pixel eye, half-open right, default flat mouth, arms close to body, no lean. Output: `LTG_CHAR_byte_expression_sheet_v001.png` (1040×738px)
- **At-Rest Curiosity fix**: Added asymmetric mouth corner (+3px right endpoint), collar tilt (rotate_deg=3), stronger pupil offset (5px vs prior 2px). Now distinguishable from Neutral at panel scale.
- **Neutral eye asymmetry fix**: Left eye aperture increased to leh=28 (right reh=22) — 6px differential → ~3.3px at panel scale, above perceptual threshold. Output: `luma_expression_sheet.png` regenerated

### Jordan Reed — Background & Environment Artist
- **ENV-06 terracotta fix** (Naomi critical, resolved): `TERRACOTTA_CYAN_LIT = (150, 172, 162)` — G=172>R, B=162>R, G+B=334>R+R=300. Fixed in both SF02 generator and color key generator. Output: `LTG_ENV_glitch_storm_bg_v001.png` (BG only, ready for character composite). `LTG_TOOL_bg_glitch_storm_colorfix_v001.py` created.
- **Tools README**: All ~20 scripts now registered. New "Misplaced Files" section flags `bg_glitch_layer_encounter.py` for relocation. `LTG_CHAR_luma_expression_sheet_v002.py` flagged as misnamed.
- **Compliance checklist**: Storyboard panels section corrected to COMPLETE; LTG_COL_* flagged for ratification (ratified by Alex this cycle).

### Sam Kowalski — Color & Style Artist
- **C10-1 RESOLVED** (3 cycles overdue): Cold overlay boundary arithmetic documented in `master_palette.md` Section 1B. At x=880, t≈0.50, alpha=30 (~11.8%). `cold_alpha_max=60` confirmed correct.
- **Warm spill alpha aligned**: Canonical value set to 40/255 (~16%). Color key generator updated. Documented as ENV-03 in master palette.
- **DRW_HOODIE_STORM saturation fixed**: Updated from RGB(192,122,112) to `#C8695A` RGB(200,105,90) — HSL saturation 50%, clear margin above background. Both scripts updated.
- **DRW-16 RESOLVED** (6th carry-forward, finally closed): `#9A7AA0` added to `luma_color_model.md` with full painter warning. Bidirectional cross-reference with `master_palette.md`.
- **CHAR-L-11 registration pending**: Awaiting Alex's confirmation — received this cycle; will register next cycle.

### Lee Tanaka — Storyboard Artist
- **P13 scream fix**: Mouth expanded to 52×32px tall yell oval, tongue added, teeth added, eyebrows spiked, body recoils, energy lines widened. Cold open comedy peak now delivers.
- **P15 arm urgency**: Endpoint extended from ~287px to ~360px. Hand blob added. Arm now strains toward frame edge.
- **P03 CRT framing**: Monitor fills 460×206px of 480px panel (was 50px margins). CRT curvature, glass reflection, power LED added.
- **P08/P09 camera differentiation**: P08 high angle (floor_y=0.62), P09 eye level (floor_y=0.76, horizon line added). Eyeline ambiguity resolved.
- **Contact sheet**: Regenerated with all fixes. `LTG_SB_coldopen_contactsheet_v002.png`
- **Act 2 plan v002**: All Carmen notes incorporated — A2-02 reframe, A1-04 near-miss, A2-05b app setup panel added. Act 2 generation deferred pending Byte glyph (message sent to Alex; glyph delivered this cycle — Act 2 panels ready for Cycle 14).

---

## Cycle 13 Asset Delta

| Asset | Location | Status |
|-------|----------|--------|
| SF01 v003 (ghost Byte fixed) | `color/style_frames/LTG_COLOR_styleframe_discovery_v003.png` | New |
| Asymmetric logo v002 | `production/LTG_BRAND_logo_asymmetric_v002.png` | New |
| SF02 with characters | `color/style_frames/LTG_COLOR_styleframe_glitch_storm_v002.png` | New |
| SF02 BG only (color fix) | `backgrounds/environments/LTG_ENV_glitch_storm_bg_v001.png` | New |
| Byte cracked-eye glyph | `characters/main/LTG_CHAR_byte_cracked_eye_glyph_v001.png` | New |
| Byte expression sheet | `characters/main/LTG_CHAR_byte_expression_sheet_v001.png` | New |
| Luma expression sheet (fixed) | `characters/main/luma_expression_sheet.png` | Updated |
| P03, P08, P09, P13, P15 panels | `storyboards/panels/` | Updated |
| Contact sheet v002 | `storyboards/panels/LTG_SB_coldopen_contactsheet_v002.png` | New |
| Act 2 plan v002 | `storyboards/act2_thumbnail_plan_v002.md` | New |
| Tools README | `tools/README.md` | Updated (all scripts registered) |
| master_palette.md | `color/palettes/master_palette.md` | Updated (C10-1, DRW-16, DRW-07, ENV-03 resolved) |

## Resolved This Cycle
- **C10-1** cold overlay boundary arithmetic (3 cycles overdue) ✓
- **DRW-16** Luma shoulder `#9A7AA0` (6 cycles overdue) ✓
- **ENV-06** terracotta cyan-lit color (Naomi critical) ✓
- **Byte neutral expression** (Dmitri P1, overdue) ✓
- **SF02 character composite** (Victoria blocker) ✓
- **Tools README** 65% gap (JT) ✓

## Open Items / Carry-Forward
- CHAR-L-11 registration (Sam — confirmation received this cycle, register next)
- Byte float-gap dimension arrow (Dmitri — still needs measurement label)
- `LTG_CHAR_luma_expression_sheet_v002.py` rename to `LTG_TOOL_*`
- `bg_glitch_layer_encounter.py` relocation from environments/ to tools/
- Glitch Layer frame version order (v001 newer than v002 — legacy naming artifact)
- Production docs (SOW, critic feedback) still not LTG-named
- Act 2 panels ready to generate in Cycle 14 (glyph now available)
- SF03 (Other Side) background still pending
