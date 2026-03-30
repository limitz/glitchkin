<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Legacy Tools Archive

**Archived by:** Kai Nakamura (Technical Art Engineer)
**Archive date:** Cycle 25 — 2026-03-29

---

## Why these files are here

These scripts were created in early production cycles before the LTG naming
convention was established. Each has a fully-compliant `LTG_TOOL_*` equivalent
in `output/tools/`. The originals were retained as a precaution through the
naming migration (Cycles 12–22) but were never removed.

**These files are superseded. Use the LTG-named versions for all new work.**

---

## Archived files and their LTG equivalents

| Legacy file | LTG equivalent |
|---|---|
| `bg_glitch_layer_frame.py` | `LTG_TOOL_bg_glitch_layer_frame.py` (+ v003) |
| `bg_house_interior_frame01.py` | `LTG_TOOL_bg_grandma_kitchen.py` (+ later versions) |
| `bg_layout_generator.py` | `LTG_TOOL_bg_tech_den.py`, `LTG_TOOL_bg_other_side.py`, etc. |
| `byte_expressions_generator.py` | `LTG_TOOL_byte_expression_sheet.py` (+ later versions) |
| `character_lineup_generator.py` | `LTG_TOOL_character_lineup.py` |
| `character_turnaround_generator.py` | `LTG_TOOL_miri_turnaround.py` (and related turnaround tools) |
| `color_key_generator.py` | `LTG_TOOL_colorkey_glitchstorm_gen.py`, `LTG_TOOL_colorkey_otherside_gen.py` |
| `color_swatch_generator.py` | `LTG_TOOL_glitch_color_model.py` (and related color model tools) |
| `contact_sheet_generator.py` | `LTG_TOOL_sb_act1_contact_sheet.py` (+ later versions) |
| `logo_generator.py` | `LTG_TOOL_logo_asymmetric.py` (+ v002) |
| `luma_expression_sheet_generator.py` | `LTG_TOOL_luma_expression_sheet.py` (+ later versions) |
| `luma_face_generator.py` | `LTG_TOOL_luma_expression_sheet.py` |
| `panel_chaos_generator.py` | `LTG_TOOL_sb_panel_a207.py` (and other panel tools) |
| `panel_interior_generator.py` | `LTG_TOOL_sb_panel_a104_kitchen.py` (and other panel tools) |
| `proportion_diagram.py` | Character sheets (`LTG_TOOL_luma_expression_sheet.py`, etc.) |
| `silhouette_generator.py` | `LTG_TOOL_luma_act2_standing_pose.py` (and pose tools) |
| `storyboard_panel_generator.py` | `LTG_TOOL_sb_panel_a101.py` (and all `LTG_TOOL_sb_panel_*` tools) |
| `storyboard_pitch_export_generator.py` | `LTG_TOOL_sb_act2_contact_sheet.py` (pitch export) |
| `style_frame_01_rendered.py` | `LTG_TOOL_style_frame_01_discovery.py` |
| `style_frame_generator.py` | All `LTG_TOOL_style_frame_*` tools |

---

## Policy

- Do not run these scripts for new production work. Use the LTG-named equivalents.
- Do not delete these files — they are preserved for historical reference and diff audit.
- Do not create new files in this directory — it is a read-only archive.
