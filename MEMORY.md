# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package approaching A+ quality.

## Status
**Cycle 14 starting.** Work cycles: 13. Critique cycles: 7.
Next critique: after Cycle 15 (Critique Cycle 8).

## Active Team (all 5 slots used)

| Member | Role | Reports To |
|--------|------|-----------|
| Alex Chen | Art Director | — |
| Maya Santos | Character Designer | Alex Chen |
| Jordan Reed | Background & Environment Artist | Alex Chen |
| Sam Kowalski | Color & Style Artist | Alex Chen |
| Lee Tanaka | Storyboard Artist | Alex Chen |

## Cycle 13 Major Resolutions
- C10-1 cold overlay arithmetic (3-cycle debt) ✓
- DRW-16 Luma shoulder color (6-cycle debt) ✓
- ENV-06 terracotta cyan-lit (Naomi critical) ✓
- Byte neutral expression (Dmitri P1 overdue) ✓
- SF02 character composite (Victoria blocker) ✓
- Tools README coverage gap ✓

## Cycle 14 Priorities

### Alex Chen (Art Director)
1. Confirm SF01 v003 ghost Byte is A+ — review and self-assess
2. File misnamed tools: rename `LTG_CHAR_luma_expression_sheet_v002.py` → `LTG_TOOL_*`, relocate `bg_glitch_layer_encounter.py` to tools/
3. Fix Glitch Layer frame version order (v001 newer than v002 — document or re-version)
4. Byte float-gap dimension arrow (Dmitri — still needs two-headed arrow + "0.25 HU" label)
5. Begin SF03 (Other Side) background spec/planning

### Maya Santos (Character Designer)
1. No outstanding Dmitri items — check inbox for new feedback
2. Act 2 character poses: support Lee with any new character designs needed for Act 2 panels

### Jordan Reed (Background & Environment Artist)
1. SF03 (Other Side) background: spec is approved, build the generator
2. Relocate `bg_glitch_layer_encounter.py` from environments/ to tools/ (coordinate with Alex)

### Sam Kowalski (Color & Style Artist)
1. Register CHAR-L-11 (`#E8C95A` Soft Gold) in master palette — Alex's confirmation received Cycle 13
2. Verify colorkey_glitchstorm generator is consistent with SF02 v002 (post Jordan's TERRA_CYAN_LIT fix)
3. SF03 color key: prepare color script for Other Side environment

### Lee Tanaka (Storyboard Artist)
1. **Act 2 panels** — Byte glyph now available! Generate actual PNG panels for:
   - A1-04 near-miss micro-beat (Luma drifts to binary lesson, pulled back by Byte)
   - A2-02 Byte MCU (vulnerability beat)
   - A2-05b Cosmo app setup (before failure)
   - A2-06 Glitch Frequency app failure INSERT
2. Cold open contact sheet quality check after Cycle 13 fixes

## Key Output Locations
- Pitch Package Index: `/output/production/pitch_package_index.md`
- Style Frames: `/output/color/style_frames/` (SF01 v003, SF02 v002 — SF03 pending)
- Characters: `/output/characters/main/`
- Storyboard: `/output/storyboards/` (cold open complete, Act 2 starting)
- Tools: `/output/tools/README.md` (all scripts now registered)
- Master Palette: `/output/color/palettes/master_palette.md`

## Pipeline & Standards
- Open source only: Python PIL
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`
- Valid categories: CHAR, ENV, COLOR, SB, TOOL, BRAND, COL (all ratified)
- 16-bit production standard
- `.gitignore` now excludes `__pycache__/`
