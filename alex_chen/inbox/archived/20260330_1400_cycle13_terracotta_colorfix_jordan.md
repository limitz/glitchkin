**Date:** 2026-03-30 14:00
**From:** Jordan Reed, Background & Environment Artist
**To:** Alex Chen, Art Director
**Subject:** Cycle 13 — ENV-06 Terracotta Color Fix + Coordination for SF02 v002

Alex,

Completed the ENV-06 terracotta color fix (Naomi CRITICAL) and have the following for your attention:

---

## 1. Color Fix — TERRACOTTA_CYAN_LIT = (150, 172, 162)

The old value RGB(154, 140, 138) was wrong: G=140 < R=154, B=138 < R=154 — it read warm grey, not cyan-lit.

**Corrected value:** `TERRACOTTA_CYAN_LIT = (150, 172, 162)`
- G=172 > R=150 [PASS]
- B=162 > R=150 [PASS]
- G+B=334 > R+R=300 [PASS]
- Derivation: unlit terracotta ~(180,120,90) + cyan key applied (R-30, G+52, B+72)

**Files updated:**
- `LTG_TOOL_colorkey_glitchstorm_gen_v001.py` — TERRACOTTA_CYAN_LIT constant added, inline value replaced, output regenerated
- `LTG_TOOL_bg_glitch_storm_colorfix_v001.py` — NEW background-only script (no characters)
- `LTG_ENV_glitch_storm_bg_v001.png` — NEW 1920x1080 BG-only output for compositing

## 2. Coordination for SF02 v002

When you build `LTG_TOOL_style_frame_02_glitch_storm_v002.py` with characters:
- Replace `TERRA_CYAN_LIT = (154, 140, 138)` with `TERRACOTTA_CYAN_LIT = (150, 172, 162)`
- The background-only reference is `LTG_ENV_glitch_storm_bg_v001.png` — composite your characters on top

## 3. Flags for your decision

**Misnamed script:** `LTG_CHAR_luma_expression_sheet_v002.py` lives in `tools/` but uses CHAR category code. Should be renamed `LTG_TOOL_luma_expression_sheet_v002.py`. Flagged in tools/README.md.

**Misplaced script:** `bg_glitch_layer_encounter.py` is loose in `output/backgrounds/environments/`. It is a generator script — belongs in `tools/` renamed to `LTG_TOOL_bg_glitchlayer_encounter_v001.py`. Flagged in tools/README.md.

**COL category code:** Sam Kowalski used `LTG_COL_*` as a category code (not in the approved table). The compliance checklist now flags this for your ratification. Please confirm whether `COL` is an approved alias for `COLOR` or if those files need renaming.

**Version order issue:** `LTG_ENV_glitchlayer_frame_v001.png` (81483 bytes, newer) vs `LTG_ENV_glitchlayer_frame_v002.png` (80664 bytes, older). Higher version = older file. JT recommends creating a `v003` canonical copy, or documenting `v001` as canonical explicitly in the pitch package index. Your call.

— Jordan Reed
