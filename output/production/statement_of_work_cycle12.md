# Statement of Work — Cycle 12
**Date:** 2026-03-30
**Project:** Luma & the Glitchkin — Cartoon Visual Assets
**Status:** Complete

---

## Work Completed

### Alex Chen — Art Director
- **Byte float-height annotation** (3-cycle overdue item, now closed): Added dashed ground-plane reference line and "ground floor." label under Byte in character lineup. Output: `LTG_CHAR_lineup_v002.png`
- **Cosmo side-view glasses refactor**: Extended `_draw_cosmo_glasses()` to handle profile view; removed inline code from `draw_cosmo_side()`. All four views now use shared helper. Output: `LTG_CHAR_cosmo_turnaround_v002.png`
- **Pitch package index update**: Added all Cycle 11/12 additions, resolved open blockers, updated asset count and quality status
- **Visual surprise — Style Frame 01**: Ghost Byte silhouettes at 22% alpha on three peripheral monitors. Subtext: Byte was watching from every screen before revealing itself. Output: `LTG_COLOR_styleframe_discovery_v002.png`
- **Asymmetric logo layout**: New generator `LTG_TOOL_logo_asymmetric_v001.py`. "Luma" large/left-anchored, "the Glitchkin" stacked/right with chromatic aberration, scan-bar divides warm/cold. Output: `LTG_BRAND_logo_asymmetric_v001.png`

### Maya Santos — Character Designer
- **Neutral/resting expression panel**: Expanded Luma expression sheet from 6 to 8 expressions (4×2 grid). Added NEUTRAL/RESTING and AT-REST CURIOSITY. WARMTH annotation corrected to "← was: ANY EARNED MOMENT". Output: `luma_expression_sheet.png` (1210×886px)
- **Expression sheet metadata**: Created `luma_expression_sheet_metadata.md` with version, head unit reference (1 HU = 200px), canvas dims, expression index, version history. Inline metadata line added to sheet header.
- **Asymmetric expression mechanism docs**: Added Section 13 "Eye Asymmetry Mechanism" to `luma.md` — documents left eye as structural lead, intensity scaling, symmetric = maximal stress signal, animator guidance.

### Jordan Reed — Background & Environment Artist
- **LTG naming compliance pass**: Created compliant copies for all outstanding legacy files — 4 character turnarounds, 4 color model swatches, 1 style frame, character lineup, 2 Glitch Layer env assets. All compliance checklist items resolved.
- **Style Frame 02 background (Glitch Storm)**: Full 8-layer rendering pipeline — sky gradient, UV purple cloud masses, main Cyan crack with Magenta burn edges, pixel confetti (spec colors only), town silhouette, street lighting zones, shattered storefront, character sprint poses with Dutch angle (4° CW). Output: `LTG_COLOR_styleframe_glitch_storm_v001.png`. Generator: `LTG_TOOL_style_frame_02_glitch_storm_v001.py`
- **Tools created**: `LTG_TOOL_naming_compliance_copier_v001.py`, `LTG_TOOL_naming_compliance_copier_v002.py`

### Sam Kowalski — Color & Style Artist
- **Color support documentation**: Created `LTG_COLOR_cycle12_color_support_v001.md` covering SF01 visual surprise figure-ground safety, logo color options, neutral expression zero-point reference for blush disambiguation system
- **Color model LTG compliance**: Created 4 `LTG_COL_[char]_colormodel_v001.png` files; new tool `LTG_TOOL_naming_compliance_copy_v001.py`; 4 `LTG_COLOR_colorkey_*_v001.png` color key thumbnails
- **Style Frame 02 Glitch Storm color key**: Generated `LTG_COLOR_colorkey_glitchstorm_v001.png` with Dutch angle, palette strip, forbidden color enforcement (no Acid Green), Corrupted Amber outline rule for Byte

### Lee Tanaka — Storyboard Artist
- **Quality pass**: Fixed P15 right-arm endpoint (true horizontal flung-arm read). Updated version strings in `panel_chaos_generator.py` and `contact_sheet_generator.py` to Cycle 12. Regenerated P15 and contact sheet.
- **LTG naming compliance**: Created 27 LTG-named copies — 26 panels (`LTG_SB_coldopen_panel_[01-25]_v001.png`) + contact sheet (`LTG_SB_coldopen_contactsheet_v001.png`)
- **Act 2 planning**: Created `act2_thumbnail_plan_v001.md` — 5 Act One beats + 8 Act Two escalation beats + production notes on scale, palette continuity, glow rules

---

## Cycle 12 Asset Delta

| Asset | Location | Status |
|-------|----------|--------|
| Character lineup v002 (Byte annotation) | `characters/main/LTG_CHAR_lineup_v002.png` | New |
| Cosmo turnaround v002 (glasses fix) | `characters/main/turnarounds/LTG_CHAR_cosmo_turnaround_v002.png` | New |
| Style Frame 01 v002 (ghost Byte surprise) | `color/style_frames/LTG_COLOR_styleframe_discovery_v002.png` | New |
| Asymmetric logo | `production/LTG_BRAND_logo_asymmetric_v001.png` | New |
| Luma expression sheet (8 expressions) | `characters/main/luma_expression_sheet.png` | Updated |
| Luma expression sheet metadata | `characters/main/luma_expression_sheet_metadata.md` | New |
| Style Frame 02 Glitch Storm background | `color/style_frames/LTG_COLOR_styleframe_glitch_storm_v001.png` | New |
| Glitch Storm color key | `color/LTG_COLOR_colorkey_glitchstorm_v001.png` | New |
| Cycle 12 color support doc | `color/LTG_COLOR_cycle12_color_support_v001.md` | New |
| Storyboard P15 (fixed) | `storyboards/panels/panel_p15_luma_freefall.png` | Updated |
| Storyboard contact sheet | `storyboards/panels/contact_sheet.png` | Updated |
| Act 2 thumbnail plan | `storyboards/act2_thumbnail_plan_v001.md` | New |
| 27× LTG storyboard copies | `storyboards/panels/LTG_SB_coldopen_*` | New |
| LTG compliance copies (misc) | Various | New batch |

---

## Open Items / Carry-Forward

- **DRW-16** (Sam): Luma shoulder under Data Stream Blue waterfall `#9A7AA0` — 6th cycle carry-forward, still not in `luma_color_model.md`. Low priority but should be closed next cycle.
- **CHAR-L-09** (Sam): `#E8C95A` warm-pixel activation entry pending Alex's SF01 visual surprise confirmation.
- **Typeface upgrade** (Victoria Ashford standing note): DejaVu Sans Bold is largest pitch quality gap. Replace when open-source display typeface matching show identity becomes available.
- **Style Frame 03** (Other Side): Spec approved, background rendering pending.
- **Neutral expression for Byte**: Dmitri Volkov flagged this alongside Luma's. Not yet actioned.
