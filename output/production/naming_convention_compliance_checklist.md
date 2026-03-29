# Naming Convention Compliance Checklist
# "Luma & the Glitchkin" — Production Reference

**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-29
**Status:** Cycle 9 — First issue
**Reference doc:** `naming_conventions.md` (Alex Chen, 2026-03-29, v1.0 APPROVED)

> Fiona O'Sullivan (Cycle 8 critique) found zero naming convention compliance in the output folder.
> The naming_conventions.md document is clear, specific, and mandatory. This checklist is not a
> rewrite of that document — it is a fast pre-save checklist for every team member to use at the
> moment of file creation or handoff.

---

## Before You Save Any File — Run This Checklist

### 1. Format Check
Does the filename follow this exact pattern?

```
[SHOW_CODE]_[CATEGORY]_[descriptor]_v[###].[ext]
```

- [ ] Starts with `LTG_` (always, no exceptions, no shortening)
- [ ] Has a valid CATEGORY code (see Quick Reference below)
- [ ] Descriptor is lowercase with underscores — no spaces, no hyphens, no CamelCase
- [ ] Version is three digits: `v001`, `v002`, `v023` — NOT `v1` or `v01` or unpadded
- [ ] File extension is lowercase and appropriate for the file type

---

### 2. Category Code Quick Reference

Use the right code or ask the Art Director:

| I am saving a... | Use this code |
|---|---|
| Character design, turnaround, expression sheet | `CHAR` |
| Background painting, environment layout, location reference | `ENV` |
| Particle system spec, FX reference, visual effects document | `FX` |
| Storyboard panels, animatic, thumbnail sequence | `SB` |
| Production document, bible, specification, SOW, schedule | `PROD` |
| Color palette, color key, style frame | `COLOR` |
| Prop design sheet, hand prop reference | `PROP` |
| Script, tool, template, pipeline utility | `TOOL` |

When in doubt — one primary category. If the file is genuinely two things (e.g., a color key that is also a style frame), use `COLOR` and note the dual function in the file itself.

---

### 3. Descriptor Formatting Rules — Quick Check

- [ ] All lowercase: `luma_designsheet` not `Luma_DesignSheet`
- [ ] Underscores between words: `ep01_cold_open` not `ep01-cold-open`
- [ ] Episode references: `ep01`, `ep02` — NOT `episode1`, `E1`, `ep_1`
- [ ] Sequence references: `seq01`, `seq07` — NOT `sequence_1`, `seq_7`
- [ ] Act references: `act01`, `act02` — NOT `act_1`, `act1`
- [ ] Character names in filenames: `luma`, `byte`, `cosmo`, `miri`, `glitchkin` (lowercase short names only)
- [ ] Time of day at the end of the descriptor, before version: `_day`, `_night`, `_dusk`
- [ ] Specific but concise: `ep01_cold_open_panel07` YES — `stuff_for_episode_one_v2` NO

---

### 4. Version Number Rules — Quick Check

- [ ] Three digits, zero-padded: `v001`, `v023`, `v100`
- [ ] Never overwrite — always increment. v002 exists alongside v001.
- [ ] Highest number = canonical (unless `_FINAL` is applied)
- [ ] `_FINAL` suffix: only the Art Director (Alex Chen) can apply it. Format: `v004_FINAL` — never `_FINAL` without a version number.

---

### 5. Common Mistakes — Do Not Do These

| Wrong | Right |
|---|---|
| `byte.md` | `LTG_CHAR_byte_designsheet_v001.md` |
| `byte_expressions.png` | `LTG_CHAR_byte_expressions_v001.png` |
| `frame01_house_interior.png` | `LTG_ENV_lumas_house_int_v001.png` |
| `style_frame_01_rendered.png` | `LTG_COLOR_styleframe_discovery_v001.png` |
| `master_palette.md` | `LTG_COLOR_palette_master_v002.md` |
| `production_bible.md` | `LTG_PROD_production_bible_v003.md` |
| `panel_p01_exterior.png` | `LTG_SB_ep01_cold_open_p01_v001.png` |
| `bg_layout_generator.py` | `LTG_TOOL_bg_layout_generator_v001.py` |
| `naming_conventions.md` | `LTG_PROD_naming_conventions_v001.md` |
| `critic_feedback_c8_naomi.md` | `LTG_PROD_critic_feedback_c8_naomi_v001.md` |

---

### 6. Retired Prefix Check

- [ ] Does the filename begin with `LH_INT_`? → STOP. Retired. Use `LTG_ENV_` instead.
- [ ] Does the filename begin with `GL_`? → STOP. Retired. Use `LTG_ENV_glitchlayer_` instead.
- [ ] If you receive a file with a retired prefix: flag it to Alex Chen before using it. Do NOT rename it in isolation.

---

### 7. Source File / Export Pairing

Source files and their exports share the same name — only the extension differs:

```
LTG_CHAR_luma_designsheet_v001.kra   ← Krita source
LTG_CHAR_luma_designsheet_v001.png   ← PNG export
```

- [ ] Does your export share the same name as its source file (different extension only)?

---

### 8. Reconciliation Status (updated Cycle 12 — Jordan Reed, 2026-03-29)

The existing output folder contains files named under the pre-convention system. These are not yet renamed — the reconciliation pass is pending and must be done as a coordinated batch (not file-by-file). Until then:

- **Do NOT rename existing legacy files in isolation** — wait for the batch reconciliation pass coordinated by Alex Chen.
- **Do apply the convention to ALL new files** created from Cycle 9 forward. No new non-compliant filenames.
- If you need to produce a new version of a legacy file, name the new version correctly (LTG-compliant) and note the prior filename in the file's header.

#### Cycle 12 Compliance Pass — Completed (Jordan Reed, 2026-03-29)

LTG-compliant copies created alongside legacy originals (originals untouched):

**Character Turnarounds (CHAR):**
- `luma_turnaround.png` → `LTG_CHAR_luma_turnaround_v001.png` ✓
- `byte_turnaround.png` → `LTG_CHAR_byte_turnaround_v001.png` ✓
- `cosmo_turnaround.png` → `LTG_CHAR_cosmo_turnaround_v001.png` ✓
- `miri_turnaround.png` → `LTG_CHAR_miri_turnaround_v001.png` ✓

**Style Frames (COLOR):**
- `style_frame_01_rendered.png` → `LTG_COLOR_styleframe_discovery_v001.png` ✓
- Style Frame 02 BG newly created: `LTG_COLOR_styleframe_glitch_storm_v001.png` ✓

**Color Model Swatches (COLOR):**
- `luma_swatches.png` → `LTG_COLOR_luma_color_model_swatches_v001.png` ✓
- `byte_swatches.png` → `LTG_COLOR_byte_color_model_swatches_v001.png` ✓
- `cosmo_swatches.png` → `LTG_COLOR_cosmo_color_model_swatches_v001.png` ✓
- `grandma_miri_swatches.png` → `LTG_COLOR_grandma_miri_color_model_swatches_v001.png` ✓

**Character Supporting Assets (CHAR):**
- `character_lineup.png` → `LTG_CHAR_character_lineup_v001.png` ✓

**Environment Assets (ENV):**
- `glitch_layer_layout.png` → `LTG_ENV_glitchlayer_layout_v001.png` ✓ (layouts/)
- `bg_glitch_layer_encounter.png` → `LTG_ENV_glitchlayer_encounter_v001.png` ✓
- `LTG_ENV_glitchlayer_frame_v001.png` — CANONICAL (81483 bytes, regenerated Cycle 11)
- `LTG_ENV_glitchlayer_frame_v002.png` — NOTE: copied from legacy `glitch_layer_frame.png`
  (80664 bytes, older render). v001 is canonical — higher byte count confirms it is the newer regeneration.

**Color Key Thumbnails (COLOR) — Sam Kowalski Cycle 12 pass (2026-03-30):**
- `key01_sunny_afternoon.png` → `LTG_COLOR_colorkey_sunny_afternoon_v001.png` ✓
- `key02_nighttime_glitch.png` → `LTG_COLOR_colorkey_nighttime_glitch_v001.png` ✓
- `key03_glitch_layer_entry.png` → `LTG_COLOR_colorkey_glitchlayer_entry_v001.png` ✓
- `key04_quiet_moment.png` → `LTG_COLOR_colorkey_quiet_moment_v001.png` ✓
- NEW: `LTG_COLOR_colorkey_glitchstorm_v001.png` — SF02 Glitch Storm key (no legacy source, new file) ✓
**Character Color Model Swatches (COL) — Sam Kowalski Cycle 12 pass (2026-03-30):**
Note: Jordan Reed created LTG_COLOR_*_color_model_swatches_v001.png versions above.
Sam Kowalski created LTG_COL_*_colormodel_v001.png variants per Priority 2 task spec.
Both exist for cross-reference; use Jordan Reed's LTG_COLOR_ versions as canonical.
- `luma_swatches.png` → `LTG_COL_luma_colormodel_v001.png` ✓ (secondary alias)
- `byte_swatches.png` → `LTG_COL_byte_colormodel_v001.png` ✓ (secondary alias)
- `cosmo_swatches.png` → `LTG_COL_cosmo_colormodel_v001.png` ✓ (secondary alias)
- `grandma_miri_swatches.png` → `LTG_COL_miri_colormodel_v001.png` ✓ (secondary alias)

**Still Outstanding (require coordinated batch rename by Alex Chen):**
- All storyboard panels (panel_p01_exterior.png through panel_p25_title_card.png → LTG_SB_*)
- All legacy background layout and environment PNGs not yet LTG-named
- color_model .md documents (CHAR category, not yet addressed)
- `naming_conventions.md` and `naming_convention_compliance_checklist.md` themselves (PROD rename irony — flag to Alex Chen)

**Tools created this cycle (TOOL):**
- `LTG_TOOL_naming_compliance_copier_v001.py` — copies legacy assets to LTG-named versions
- `LTG_TOOL_naming_compliance_copier_v002.py` — ENV pass
- `LTG_TOOL_style_frame_02_glitch_storm_v001.py` — Style Frame 02 BG generator

---

## One-Sentence Summary

**Every file you create from Cycle 9 forward must be:**
`LTG_[CATEGORY]_[lowercase_descriptor]_v[###].[ext]`

If you are unsure, check `naming_conventions.md` or ask Alex Chen before creating the file — not after.

---

*Sam Kowalski — Cycle 9 (2026-03-29)*
*Created per Fiona O'Sullivan Cycle 8 critique: naming_conventions.md is clear; compliance is the gap. This checklist is the operational bridge.*
