# Statement of Work — Cycle 14
**Date:** 2026-03-30
**Project:** Luma & the Glitchkin — Cartoon Visual Assets
**Status:** Complete

---

## Work Completed

### Alex Chen — Art Director
- **Byte float-gap dimension arrow** (Dmitri P1, finally fully resolved): Replaced caption label with proper engineering dimension arrow — two-headed vertical, serif ticks, "0.25 HU" label. Output: `LTG_CHAR_lineup_v003.png` via `LTG_TOOL_character_lineup_v003.py`
- **Misnamed/misplaced tool fixes**: Created `LTG_TOOL_luma_expression_sheet_v002.py` (correct category), `LTG_TOOL_bg_glitch_layer_encounter_v001.py` (relocated copy). Documented Glitch Layer frame version order in compliance checklist.
- **SF03 Other Side spec**: Created `/output/production/sf03_other_side_spec.md` — full technical generator spec: 5 depth layers, RGB values, inverted atmospheric perspective rule, character placement, draw order. Sent to Jordan Reed.
- **SF01 v003 self-assessment**: **Grade A+ — LOCKED.** Ghost Bytes pitch-visible at alpha 90/105. Warm zone clean. No further changes. Assessment documented.

### Maya Santos — Character Designer
- **Cosmo expression sheet**: Created `LTG_TOOL_cosmo_expression_sheet_v001.py` — 3×2 grid with Neutral, Frustrated/Defeated, Determined, Skeptical. Notebook open/tucked state used as emotional signal. Output: `LTG_CHAR_cosmo_expression_sheet_v001.png` (912×946px)
- **Luma classroom pose**: Created `LTG_TOOL_luma_classroom_pose_v001.py` — seated at desk, AT-REST CURIOSITY expression, head tilt 8° toward blackboard, pen tapping, elbow lean. Output: `LTG_CHAR_luma_classroom_pose_v001.png`
- **Byte gap flagged**: Byte missing RESIGNED expression for A2-02. Flagged to Alex Chen; Lee notified to use NEUTRAL as staging approximation.

### Jordan Reed — Background & Environment Artist
- **SF03 Other Side background**: Built `LTG_TOOL_bg_other_side_v001.py` — pure digital void space: perspective pixel grid floor, 3-tier floating platforms (NEAR cyan / MID desaturated / FAR void), aurora bands, isometric geometry cubes, data streams, CRT vignette. Zero warm tones. Output: `LTG_ENV_other_side_bg_v001.png` (1920×1080, 275KB)
- **Classroom background**: Built `LTG_TOOL_bg_classroom_v001.py` — 3/4 angle back-right view, 3 depth tiers, dual-temperature lighting (warm gold window shafts + cool fluorescent pools), binary lesson on whiteboard, Luma's pixel sticker desk. Output: `LTG_ENV_classroom_bg_v001.png` (1920×1080)
- Both tools registered in README

### Sam Kowalski — Color & Style Artist
- **CHAR-L-11 registered**: `#E8C95A` Soft Gold warm-pixel activation added to master palette Section 5. CHAR-L-09 thread fully closed.
- **SF03 Other Side color key**: Planning doc `LTG_COLOR_colorkey_otherside_v001.md` + generator + `LTG_COLOR_colorkey_otherside_v001.png`. Five depth zones, forbidden color list, character support notes, comparison table vs SF01/SF02.
- **Colorkey Glitchstorm verified**: Already consistent with TERRA_CYAN_LIT (150,172,162). No changes needed.
- **Classroom color key**: `LTG_COLOR_colorkey_classroom_v001.md` — warm neutral daylight + institutional fluorescent, zero Glitch palette contamination. Key note: Luma's hoodie pixels must stay Warm Cream in pre-discovery scenes.

### Lee Tanaka — Storyboard Artist
- **4 Act 2 panels generated** via `LTG_TOOL_act2_panels_cycle14_v001.py`:
  - `LTG_SB_act2_panel_a104_v001.png` — Classroom near-miss: sight-line triangle (Luma→board→Byte napping in eraser tray)
  - `LTG_SB_act2_panel_a202_v001.png` — Byte MCU vulnerability: cracked-eye glyph at full legibility, resigned expression, Byte fills 60%+ of frame
  - `LTG_SB_act2_panel_a205b_v001.png` — Cosmo app setup: GLITCH FREQ UI visible, confident pose, pixel confetti
  - `LTG_SB_act2_panel_a206_v001.png` — App failure INSERT: full-frame screen crash, static bars, magenta X, "SIGNAL LOST: ERR 0xFF"
- **Act 2 contact sheet**: `LTG_SB_act2_contactsheet_v001.png` — 2×2, arc reads classroom→vulnerability→setup→crash

---

## Cycle 14 Asset Delta

| Asset | Location | Status |
|-------|----------|--------|
| Character lineup v003 (dimension arrow) | `characters/main/LTG_CHAR_lineup_v003.png` | New |
| Cosmo expression sheet | `characters/main/LTG_CHAR_cosmo_expression_sheet_v001.png` | New |
| Luma classroom pose | `characters/main/LTG_CHAR_luma_classroom_pose_v001.png` | New |
| SF03 Other Side background | `backgrounds/environments/LTG_ENV_other_side_bg_v001.png` | New |
| Classroom background | `backgrounds/environments/LTG_ENV_classroom_bg_v001.png` | New |
| SF03 color key | `color/color_keys/thumbnails/LTG_COLOR_colorkey_otherside_v001.png` | New |
| Act 2 panels (×4) | `storyboards/` | New |
| Act 2 contact sheet | `storyboards/LTG_SB_act2_contactsheet_v001.png` | New |
| SF03 spec | `production/sf03_other_side_spec.md` | New |
| SF01 v003 assessment | `production/sf01_v003_assessment.md` | New |

## Resolved This Cycle
- **Byte float-gap dimension arrow** (Dmitri, multi-cycle) ✓
- **SF01 v003 locked at A+** ✓
- **CHAR-L-11** registered ✓
- **Misnamed/misplaced tools** corrected ✓
- **Glitch Layer frame version order** documented ✓

## Open Items / Carry-Forward
- Byte RESIGNED expression (A2-02 uses NEUTRAL approximation for now)
- SF03 character composite (Other Side BG complete; needs Luma+Byte composited = Style Frame 03)
- Act 2 panels A2-07 onward (queue building)
- Production docs still not LTG-named (ongoing low-priority)
