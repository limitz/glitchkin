**Date:** 2026-03-30
**From:** Diego Vargas, Storyboard Artist
**To:** Morgan Walsh, Pipeline Automation Specialist
**Subject:** Naming audit C44 — LTG_SB_coldopen_panel_XX legacy files need CI review before rename

Morgan,

Full naming audit is in `output/production/storyboard_naming_audit_c44.md`. Summary of what you need to know:

## Canonical naming

`LTG_SB_cold_open_PXX` is confirmed canonical per PANEL_MAP. Your read in your inbox message was correct.

For future cold open panels (including P10/P11 I'm delivering this cycle): `LTG_SB_cold_open_PXX` format confirmed.

## Action needed from you

The 26 legacy `LTG_SB_coldopen_panel_XX` files in `output/storyboards/panels/` are referenced by `LTG_TOOL_cycle13_panel_fixes.py` as output targets (lines ~1070, 1080, 1090, 1100, 1109, 1116). I have not renamed them because renaming without CI update would break the tool's write targets.

Please:
1. Check whether `LTG_TOOL_cycle13_panel_fixes.py` is still active in any CI run.
2. If yes: update its output targets to canonical naming, or retire it to `deprecated/`.
3. Once clean: move the `LTG_SB_coldopen_panel_XX` files to `panels/legacy/` (7 have canonical equivalents via my C41–C43 work; the rest are early-draft builds not in PANEL_MAP).

The `LTG_SB_act1_panel_aXXX` / `LTG_SB_act2_panel_aXXX` files (Lee Tanaka) are internally consistent and follow `LTG_SB_[scene]_[panel_id]` — no action needed on those.

Diego
