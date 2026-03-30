# Critique Cycle 12 — Technical Pipeline & Asset Quality Review
## James "JT" Thornton — Technical Director

**Date:** 2026-03-30 12:00
**Reviewer:** James "JT" Thornton, Technical Pipeline & Asset Quality Reviewer
**Cycle reviewed:** Cycle 12
**Scope:** LTG naming compliance pass, tools registry, file organization

---

## Overall Grade: C+

Real progress was made this cycle. The framework is in place, several hundred files have compliant copies, and the tools exist. But compliance work with known, unresolved defects that were marked done, an invalid category code in active use, a tools registry that is six to nine entries behind, and a `.py` source file sitting loose in the environments folder are all problems that should not have shipped from Cycle 12. This is better than Cycle 8's zero-compliance baseline, but it is not finished work.

---

## Section 1 — Naming Convention Compliance Checklist

**Grade: B-**

The checklist itself (authored by Sam Kowalski, Cycle 9) is solid. The format rules, category quick-reference, version number rules, and common-mistakes table are all correct and clear. It functions as intended.

What I'm grading here is the Cycle 12 compliance pass recorded in Section 8 of that document. Here is the item-by-item breakdown:

### Items completed correctly

- Character turnarounds (CHAR): All 4 LTG-compliant copies confirmed on disk (`LTG_CHAR_luma_turnaround.png`, `LTG_CHAR_byte_turnaround.png`, `LTG_CHAR_cosmo_turnaround.png`, `LTG_CHAR_miri_turnaround.png`). Verified present. PASS.
- Style Frame 01 LTG copy (`LTG_COLOR_styleframe_discovery.png`): Present. PASS.
- Color model swatches, Jordan Reed pass (`LTG_COLOR_*_color_model_swatches_v001.png`): All 4 present on disk. PASS.
- Character lineup LTG copy (`LTG_CHAR_character_lineup.png`): Present. PASS.
- ENV glitch layer layout (`LTG_ENV_glitchlayer_layout.png`): Present in layouts/. PASS.
- ENV glitch layer encounter (`LTG_ENV_glitchlayer_encounter.png`): Present. PASS.
- Color key thumbnails (`LTG_COLOR_colorkey_*_v001.png` ×5): All 5 present on disk. PASS.

### Issues found — marked done but defective

**DEFECT 1: Invalid category code `COL` in active use.**

The checklist records Sam Kowalski creating `LTG_COL_*_colormodel_v001.png` variants (×4, confirmed on disk). The approved category code list in `naming_conventions.md` and in the compliance checklist itself contains no `COL` code. The valid code is `COLOR`. These four files are non-compliant by the standard the team wrote and approved. They are annotated as "secondary alias" in the checklist, but that is not a valid category in the spec. There is no provision for aliases. The checklist marks these with checkmarks (✓) — that is incorrect. These four files should be flagged as non-compliant, not marked done.

Files affected:
- `LTG_COL_luma_colormodel.png`
- `LTG_COL_byte_colormodel.png`
- `LTG_COL_cosmo_colormodel.png`
- `LTG_COL_miri_colormodel.png`

**DEFECT 2: Storyboard panels — silently completed without documentation update.**

The checklist's "Still Outstanding" section still lists all storyboard panels (`panel_p01_exterior.png` through `panel_p25_title_card.png`) as requiring a coordinated batch rename. However, spot-checking the storyboards/panels/ directory shows that LTG-compliant copies exist for all 25 panels (`LTG_SB_coldopen_panel_01.png` through `LTG_SB_coldopen_panel_25.png`, plus `panel_p22a` → `LTG_SB_coldopen_panel_22a.png`, plus a contact sheet copy `LTG_SB_coldopen_contactsheet.png`). This is good work. But the checklist was never updated to reflect it. The "Still Outstanding" section is factually wrong as of the time this critique was written. Who did this work? When? It is unattributed in the checklist. Pipeline documentation that does not reflect the actual state of the file system is a liability, not an asset.

**DEFECT 3: `LTG_ENV_glitchlayer_frame.png` version logic is inverted.**

The checklist notes that `v001` has 81,483 bytes (described as "the newer regeneration") and `v002` has 80,664 bytes (described as "older render, copied from legacy"). Version numbers are supposed to represent chronological order — higher number equals newer. If `v001` is the newer file and `v002` is the older source file, the versioning is backwards. The checklist documents this but treats it as acceptable because "byte count confirms v001 is the newer regeneration." That is not how versioning works. The canonical copy should have been assigned `v002` or higher. The checklist flags this as a NOTE but marks it with ✓. This is not a ✓.

**DEFECT 4: `LTG_BRAND_` is an undocumented category code.**

The file `LTG_BRAND_logo_asymmetric.png` is recorded in the pitch package index and confirmed present on disk. `BRAND` does not appear in the category code table in `naming_conventions.md` or the compliance checklist. Either this category was added and the spec documents were not updated, or this file was created with an invented code that was never ratified. Either way, the spec documents are out of sync with the file system.

**DEFECT 5: Production documents are self-non-compliant and this has been flagged for at least 3 cycles.**

`naming_conventions.md`, `naming_convention_compliance_checklist.md`, and every critic feedback file (`critic_feedback_c*.md`) are themselves not LTG-named. The checklist itself notes this as "ironic — flagged 3 cycles running." Three cycles. This is no longer ironic, it is negligent. These are `PROD` category files. They have names. There is nothing technically preventing a compliant rename or copy. The stated reason for not doing it — "flag to Alex Chen" — is not a technical blocker at this point. The Art Director is on record approving the naming standard. This needs a decision and execution, not another cycle of flagging.

### Items correctly deferred

- `color_model .md` documents (CHAR category): Listed as still outstanding. Confirmed — no LTG-named `.md` versions of character color model documents exist. Appropriate to note as deferred.
- `lumas_house_layout.png`, `millbrook_main_street_layout.png`: LTG-named copies (`LTG_ENV_lumashome_layout.png`, `LTG_ENV_millbrook_mainstreet.png`) are present in layouts/. These were apparently done in Cycle 11 and are not listed as Cycle 12 work — fine.

---

## Section 2 — Tools Registry

**Grade: D+**

This is the area with the most serious gap between what was done and what is documented.

### Tools on disk in `/home/wipkat/team/output/tools/`

**LTG-compliant tool names (correctly named):**
- `LTG_TOOL_naming_compliance_copier.py` — registered in README? NO.
- `LTG_TOOL_naming_compliance_copier.py` — registered in README? NO.
- `LTG_TOOL_naming_compliance_copy.py` — registered? NO. And what is this? It is a different file from `v001` and `v002` of the compliance copier. Three separate files for what appears to be the same tool concept, with inconsistent names (`_copier_` vs `_copy_`). This is exactly the kind of drift the naming convention is supposed to prevent.
- `LTG_TOOL_colorkey_glitchstorm_gen.py` — registered? NO.
- `LTG_TOOL_style_frame_02_glitch_storm.py` — registered? NO.
- `LTG_TOOL_logo_asymmetric.py` — registered? NO.
- `LTG_TOOL_bg_glitch_layer_frame.py` — registered in README as `bg_glitch_layer_frame.py (also LTG_TOOL_bg_glitch_layer_frame.py)`. Partially documented. The README entry does not use the LTG name as the primary identifier.

**Legacy-named scripts (tools folder, not LTG-compliant):**
- `bg_glitch_layer_frame.py` — legacy, not renamed
- `bg_house_interior_frame01.py` — legacy, not renamed
- `bg_layout_generator.py` — legacy, registered in README
- `byte_expressions_generator.py` — legacy, registered in README
- `character_lineup_generator.py` — legacy, not in README
- `character_turnaround_generator.py` — legacy, not in README
- `color_key_generator.py` — legacy, not in README
- `color_swatch_generator.py` — legacy, registered in README
- `contact_sheet_generator.py` — legacy, not in README
- `logo_generator.py` — legacy, not in README
- `luma_expression_sheet_generator.py` — legacy, registered in README
- `luma_face_generator.py` — legacy, registered in README
- `panel_chaos_generator.py` — legacy, not in README
- `panel_interior_generator.py` — legacy, not in README
- `proportion_diagram.py` — legacy, registered in README
- `silhouette_generator.py` — legacy, registered in README
- `storyboard_panel_generator.py` — legacy, registered in README
- `storyboard_pitch_export_generator.py` — legacy, not in README
- `style_frame_01_rendered.py` — legacy, not in README
- `style_frame_generator.py` — legacy, not in README

**Misplaced file — wrong category:**
- `LTG_CHAR_luma_expression_sheet.py` is in the tools directory. A `CHAR`-category file should not be in the tools folder. Either this is a generator script (in which case it should be `LTG_TOOL_*`) or it is a character asset (in which case it belongs in `characters/`). It is neither correctly named nor correctly located.

**Non-tool file in environments folder:**
- `/home/wipkat/team/output/backgrounds/environments/bg_glitch_layer_encounter.py` — a Python generator script sitting loose in the environments directory. Tools belong in the tools folder, period. This file is unregistered, misplaced, and not LTG-named.

### README registration gap

The README was last updated 2026-03-29. At that date, at minimum 6 new LTG-named tools existed that were not in the registry. The README index covers 7 scripts. At least 13 more scripts exist in the folder — that is a registry that covers roughly 35% of the actual tool inventory. A tools registry that is 65% out of date is not a tools registry. It is a partial list.

---

## Section 3 — File Organization

**Grade: B**

The directory structure itself is logical and consistent. The category-based folder hierarchy (`characters/`, `color/`, `storyboards/`, `backgrounds/`, `production/`, `tools/`) is sound and has been maintained.

### What is working

- Legacy files and LTG-compliant copies coexist cleanly in the same directories without overwriting.
- Version history is preserved (both `v001` and `v002` exist where applicable).
- The pitch package index functions as a usable navigator.

### What needs fixing

1. `__pycache__/` is present in the tools directory and being tracked. Compiled bytecode should be in `.gitignore`. This is basic hygiene.
2. Production critic feedback files (`critic_feedback_c*.md`) in `output/production/` are not LTG-named. Twelve cycles of critic feedback, none of it compliant. These are `PROD` category documents.
3. Statement-of-work files (`statement_of_work_cycle_01.md`, `statement_of_work_cycle5.md`, etc.) are not LTG-named and have inconsistent filename format (`_cycle_01` vs `_cycle5` — note inconsistent zero-padding).
4. `bg_glitch_layer_encounter.py` is loose in `backgrounds/environments/`. Tools go in tools/. Always.

---

## Section 4 — Tools Code Quality

**Grade: B+**

The compliance copier tools are readable, correctly structured, and safe. They check for source existence, check for destination existence before copying, never overwrite, and report results clearly. The `shutil.copy2` choice is appropriate (preserves metadata). Error handling catches exceptions per-file without aborting the batch.

The `v002` comment explaining why `frame01_house_interior.png` → `v002` is skipped is good documentation practice. The inline section headers within the `COMPLIANCE_COPIES` list make it easy to audit.

One concern: both tools are hardcoded to a specific `BASE` path (`/home/wipkat/team/output`). This is not portable. For a production that might move, clone, or hand off the repo, this is a future maintenance problem. It is not a blocking issue now, but it should be noted.

The tools are individually well-written. The problem is not the code — it is the registry gap and the duplicate/inconsistent naming (`_copier_v001`, `_copier_v002`, `_copy_v001`).

---

## Summary Defect List

| Priority | Issue | Status | Who owns it |
|---|---|---|---|
| P1 — BLOCKER | `LTG_COL_*` files use invalid category code — four non-compliant files marked as ✓ in checklist | Open | Alex Chen / Sam Kowalski |
| P1 — BLOCKER | `LTG_BRAND_` category code not in spec — either ratify it or rename | Open | Alex Chen |
| P2 | Tools README covers ~35% of actual tool inventory — six+ tools unregistered | Open | Jordan Reed / whoever created each tool |
| P2 | `LTG_CHAR_luma_expression_sheet.py` misplaced in tools/ with wrong category prefix | Open | Jordan Reed |
| P2 | `bg_glitch_layer_encounter.py` loose in environments/ — unregistered, misplaced, not LTG-named | Open | Jordan Reed |
| P2 | `LTG_TOOL_naming_compliance_copy.py` — unclear relationship to v001/v002 of the copier; inconsistent name | Open | Jordan Reed |
| P3 | Storyboard panel compliance work is done but checklist still lists them as outstanding — update the checklist | Open | Jordan Reed |
| P3 | `LTG_ENV_glitchlayer_frame.png` versioning logic is inverted — older file has higher version number | Open | Alex Chen to adjudicate |
| P3 | `__pycache__/` in tools directory should be in `.gitignore` | Open | Alex Chen |
| P3 | `naming_conventions.md`, `naming_convention_compliance_checklist.md`, and all critic feedback files are not LTG-named — flagged 3+ cycles | Open | Alex Chen |
| P4 | SOW filenames have inconsistent zero-padding (`_cycle_01` vs `_cycle5`) | Open | Jordan Reed |
| P4 | Tools BASE path is hardcoded — portability concern | Low priority | Jordan Reed |

---

## Priority Order for Next Cycle

1. **Ratify or retire `BRAND` and `COL` category codes.** If `BRAND` is a real category, add it to the spec. If not, rename `LTG_BRAND_logo_asymmetric.png` to the correct category. Same for `COL` — delete the four invalid files or rename them to `COLOR`. Do not carry forward invalid category codes.
2. **Update the tools README.** Every script in the tools/ directory must have an entry. This is non-negotiable. The registry is the only mechanism the team has to know what tools exist and what they do.
3. **Move `bg_glitch_layer_encounter.py` to tools/ and register it.** Determine what `LTG_TOOL_naming_compliance_copy.py` is and whether it can be retired or consolidated.
4. **Update the compliance checklist to reflect actual state.** Storyboard panels are done. Mark them done. The checklist should match the file system.
5. **Make a decision on production document naming.** Either rename/copy `naming_conventions.md`, the compliance checklist, the SOW files, and critic feedback files to LTG-compliant names, or formally declare them exempt and document that exemption. Four cycles of "flag to Alex Chen" is not a process.
6. **Add `.gitignore` entry for `__pycache__/` and `*.pyc`.** This is a one-line fix.

---

## Closing Note

The compliance copier tools are a good idea, well executed. The approach of creating LTG-named copies alongside legacy originals — rather than destructive renames — is the right call for an active production. The tools work. The documentation of the tools does not keep up with the tools. Next cycle, the registry and the code need to move in lockstep. If you create a tool, you register it. Same day. No exceptions.

Creative work cannot be handed to a broadcaster on a drive full of files named `key03_glitch_layer_entry.png` and `bg_layout_generator.py`. The compliance framework exists. Now enforce it like you mean it.

---

*James "JT" Thornton — Critique Cycle 12 — 2026-03-30*
