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

### 8. Reconciliation Status (as of Cycle 9)

The existing output folder contains files named under the pre-convention system. These are not yet renamed — the reconciliation pass is pending and must be done as a coordinated batch (not file-by-file). Until then:

- **Do NOT rename existing legacy files in isolation** — wait for the batch reconciliation pass coordinated by Alex Chen.
- **Do apply the convention to ALL new files** created from Cycle 9 forward. No new non-compliant filenames.
- If you need to produce a new version of a legacy file, name the new version correctly (LTG-compliant) and note the prior filename in the file's header.

---

## One-Sentence Summary

**Every file you create from Cycle 9 forward must be:**
`LTG_[CATEGORY]_[lowercase_descriptor]_v[###].[ext]`

If you are unsure, check `naming_conventions.md` or ask Alex Chen before creating the file — not after.

---

*Sam Kowalski — Cycle 9 (2026-03-29)*
*Created per Fiona O'Sullivan Cycle 8 critique: naming_conventions.md is clear; compliance is the gap. This checklist is the operational bridge.*
