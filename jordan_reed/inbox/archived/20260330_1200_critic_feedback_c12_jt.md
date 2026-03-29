**Date:** 2026-03-30 12:00
**From:** James "JT" Thornton, Technical Pipeline & Asset Quality Reviewer (Critique Cycle 7)
**To:** Jordan Reed, Background & Environment Artist
**Subject:** Cycle 12 Technical Critique — Pipeline & Tools Defects

Jordan,

I have completed my Cycle 12 review. Full critique is at `/home/wipkat/team/output/production/critic_feedback_c12_jt.md`. Overall grade: C+. The compliance copier tools themselves are well-written — the gaps are in the areas around the tools: registration, placement, and documentation accuracy.

Here is what you need to fix, in priority order:

---

### P2 — Tools registry is critically out of date

The README in `output/tools/` covers 7 scripts. There are at minimum 20 scripts in that directory. Six or more LTG-named tools created this cycle alone are not registered:
- `LTG_TOOL_naming_compliance_copier_v001.py` — not in README
- `LTG_TOOL_naming_compliance_copier_v002.py` — not in README
- `LTG_TOOL_naming_compliance_copy_v001.py` — not in README (and what is this — is it the same tool as the above two? The name is different: `_copy_` vs `_copier_`. Clarify or consolidate.)
- `LTG_TOOL_colorkey_glitchstorm_gen_v001.py` — not in README
- `LTG_TOOL_style_frame_02_glitch_storm_v001.py` — not in README
- `LTG_TOOL_logo_asymmetric_v001.py` — not in README

The rule is: you create a tool, you register it, same session. The README is the team's only way to know what tools exist. A 65%-missing registry is not useful.

Also: many legacy-named scripts that you presumably wrote or used are not in the README either (`character_lineup_generator.py`, `character_turnaround_generator.py`, `contact_sheet_generator.py`, `logo_generator.py`, `panel_chaos_generator.py`, `panel_interior_generator.py`, `storyboard_pitch_export_generator.py`, `style_frame_01_rendered.py`, `style_frame_generator.py`). These all need entries.

---

### P2 — Misplaced and misnamed files

**`LTG_CHAR_luma_expression_sheet_v002.py`** is in `output/tools/`. A Python script is a tool. It should be named `LTG_TOOL_*`, not `LTG_CHAR_*`. Character assets (`.md`, `.png`) live in `characters/`. Scripts live in `tools/` with a `TOOL` category code. Fix the name and confirm the file is in the right place.

**`bg_glitch_layer_encounter.py`** is loose in `output/backgrounds/environments/`. This is a generator script — it belongs in `output/tools/`. Move it, rename it to `LTG_TOOL_*`, and register it in the README.

---

### P2 — `LTG_ENV_glitchlayer_frame_v002.png` version logic

In the checklist you note that `v001` (81,483 bytes) is the newer regeneration and `v002` (80,664 bytes) is the older legacy copy. Version numbers mean chronological order — higher is newer. You have an older file at a higher version number. You documented it, which is better than nothing, but documenting a known-wrong thing and marking it ✓ is not the same as fixing it. Raise this with Alex Chen for a decision — it may require a `v003` canonical copy, or a note in the index designating `v001` as canonical and `v002` as a legacy-provenance copy.

---

### P3 — Compliance checklist is out of sync with file system

The "Still Outstanding" section of the compliance checklist still lists all 25 storyboard panels as needing a batch rename. The file system shows all 25 have LTG-compliant copies (`LTG_SB_coldopen_panel_01_v001.png` through `_25`, plus `_22a` and the contact sheet). This work is done. Update the checklist to reflect reality. Also attribute who did it and when — unattributed work in a production pipeline is a tracking problem.

---

### Code note — compliance copier tools

The tools are well-structured and safe. One future-maintenance flag: `BASE = "/home/wipkat/team/output"` is hardcoded. Not a blocker now, but if the repo ever moves or is handed off, every tool breaks. Consider making it relative to `__file__` or accepting it as a CLI argument in a future version.

---

The compliance work you did this cycle is real. All the key LTG-named copies are on disk and confirmed. The problem is the documentation around the work — the registry, the checklist, the placement of scripts. Those are fixable and they need to be fixed this cycle.

— JT
