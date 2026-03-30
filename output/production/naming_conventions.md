# Naming Conventions — Unified Production Standard
# "Luma & the Glitchkin" — Production Reference

**Document Author:** Alex Chen, Art Director
**Date:** 2026-03-29
**Version:** 1.1 (Cycle 13 — BRAND and COL categories ratified; LTG_COL_ retired)
**Status:** APPROVED — MANDATORY FOR ALL PRODUCTION ASSETS

---

## Overview

This document establishes the single canonical file naming system for all production assets on "Luma & the Glitchkin." All team members must follow this system from the date of this document's approval. Assets created under prior systems will be reconciled on the schedule noted below.

**There is one system. Use it.**

---

## The Canonical Format

```
[SHOW_CODE]_[CATEGORY]_[descriptor]_v[###].[ext]
```

### Components

| Component | Definition | Values |
|---|---|---|
| `SHOW_CODE` | Fixed identifier for this production | `LTG` (Luma The Glitchkin) |
| `CATEGORY` | Asset category abbreviation | See Category Codes table below |
| `descriptor` | Human-readable description of the specific asset | Lowercase, words separated by underscores |
| `v[###]` | Three-digit zero-padded version number | `v001`, `v002` … `v999` |
| `[ext]` | File extension | `png`, `pdf`, `md`, `kra`, `py`, `svg`, etc. |

### Category Codes

| Code | Category | Description |
|---|---|---|
| `CHAR` | Character | Character design sheets, model sheets, expressions |
| `ENV` | Environment / Background | Location paintings, background layouts, props |
| `FX` | Visual Effects | Particle systems, FX reference sheets, FX specs |
| `SB` | Storyboard | Panel sequences, thumbnails, animatics |
| `PROD` | Production | Production documents, bibles, specifications |
| `COLOR` | Color | Palette files, color keys, style frames, color models |
| `PROP` | Prop | Interactive objects, hand props, set dressing items |
| `TOOL` | Tool / Script | Reusable pipeline scripts, brushes, templates |
| `BRAND` | Brand / Identity | Show logos, title treatments, brand identity assets, pitch graphics |

**Cycle 13 category ratification notes (Alex Chen, Art Director):**

**`BRAND` — RATIFIED.** `LTG_BRAND_*` is the correct category for show logos, title cards, lockups, and brand identity assets. These are distinct from `PROD` (production administration documents) and `COLOR` (color scripts / palettes). `LTG_BRAND_logo_asymmetric.png` and subsequent logo assets use this code correctly. Added to spec.

**`COL` — RETIRED. Use `COLOR`.** `LTG_COL_*` files created by Sam Kowalski (e.g., `LTG_COL_luma_colormodel.png`) used a non-approved shorthand. `COL` is not a valid category code and never was. The canonical code is `COLOR`. The `LTG_COLOR_*_color_model_swatches_v001.png` versions created by Jordan Reed are the correct replacements. Any `LTG_COL_*` files should be treated as non-compliant — do not create new files with `COL` prefix. Existing `LTG_COL_*` files will be addressed in the batch reconciliation pass. Do not rename them individually.

---

## Examples — One Per Asset Type

### Character Assets
```
LTG_CHAR_luma_designsheet_v001.png
LTG_CHAR_luma_turnaround_front_v002.png
LTG_CHAR_luma_expressions_v001.png
LTG_CHAR_byte_designsheet_v001.png
LTG_CHAR_byte_pixelface_expressions_v003.png
LTG_CHAR_cosmo_designsheet_v001.png
LTG_CHAR_grandma_miri_designsheet_v001.png
LTG_CHAR_glitchkin_ep01_wrangler_v001.png
```

### Environment / Background Assets
```
LTG_ENV_millbrook_lumahome_exterior_day_v001.png
LTG_ENV_millbrook_lumahome_study_interior_v001.png
LTG_ENV_millbrook_school_exterior_v001.png
LTG_ENV_glitchlayer_entrance_v001.png
LTG_ENV_millbrook_towncenter_day_v001.png
LTG_ENV_junkyard_exterior_v001.png
```

### FX / Effects Assets
```
LTG_FX_confetti_density_scale_v001.md
LTG_FX_spec_cold_open_ep01_v001.md
LTG_FX_byte_float_physics_v001.md
LTG_FX_corruption_visual_brief_v001.md
LTG_FX_confetti_particle_sheet_v001.png
```

### Storyboard Assets
```
LTG_SB_ep01_cold_open_seq01_v001.pdf
LTG_SB_ep01_act01_seq03_v002.pdf
LTG_SB_ep01_thumbnails_v001.pdf
LTG_SB_ep02_act02_seq07_v001.pdf
```

### Production Documents
```
LTG_PROD_production_bible_v002.md
LTG_PROD_naming_conventions_v001.md
LTG_PROD_style_guide_v001.md
LTG_PROD_statement_of_work_cycle01_v001.md
LTG_PROD_byte_float_physics_v001.md
```

### Color Assets
```
LTG_COLOR_palette_realworld_v001.png
LTG_COLOR_palette_glitchlayer_v001.png
LTG_COLOR_key_ep01_act02_v001.png
LTG_COLOR_styleframe_ep01_cold_open_panel07_v001.png
LTG_COLOR_palette_realworld_v001.ase
```

### Prop Assets
```
LTG_PROP_crt_monitor_miri_v001.png
LTG_PROP_cosmo_notebook_v001.png
LTG_PROP_luma_hoodie_detail_v001.png
```

### Tool / Script Assets
```
LTG_TOOL_confetti_particle_emitter_v001.py
LTG_TOOL_color_palette_swatch_template_v001.ase
LTG_TOOL_asset_naming_validator_v001.sh
```

---

## Version Numbering Rules

- **Always three digits:** `v001`, `v002`, `v023`, `v100`. Never `v1`, `v01`, or unpadded numbers.
- **Never overwrite.** Increment the version number at every save. Previous versions are kept.
- **The highest version number is canonical** unless the file is marked `_FINAL` (see below).
- Versions reset to `v001` only when a file is meaningfully restarted from scratch — and even then, old versions are archived, not deleted.

---

## The `_FINAL` Suffix — Canonical Definition

The `_FINAL` suffix is appended **after the version number** and **before the extension:**

```
LTG_CHAR_luma_designsheet_v004_FINAL.png
```

### What `_FINAL` means:
**"This file is approved for delivery to the production pipeline. Do not modify without Art Director sign-off."**

`_FINAL` is a **pipeline status flag**, not a version number. It does not mean there will be no further versions. A `_FINAL` file may be superseded by a higher version if revisions are required — but only after written approval from Alex Chen (Art Director).

### What `_FINAL` does NOT mean:
- It does not mean the file is the only version or the last version ever.
- It does not replace the version number (`_v004_FINAL` is correct; `_FINAL` without a version number is not permitted).
- It does not grant permission to skip Art Director review on the next version.

### Who can apply `_FINAL`:
Only the Art Director (Alex Chen) or a team member acting under explicit written delegation from the Art Director.

---

## Bit Depth Standard

| Use Case | Bit Depth | Format |
|---|---|---|
| All production assets (character, background, FX, color reference) | **16-bit** | PNG |
| Web / presentation exports | **8-bit** | PNG or JPEG |
| Storyboard exports | 8-bit | PDF or PNG |
| Source working files (Krita, OpenToonz) | 16-bit minimum | Native format (.kra, .xdts, .svg) |

**Rule:** When in doubt, use 16-bit. Downsampling from 16-bit to 8-bit is lossless; upsampling is not.

---

## Blend Mode Terminology

All blend mode names used throughout production documents (Screen, Multiply, Overlay, Add, Normal, etc.) refer to **Natron's blend mode terminology**. These names are consistent with the broader open source compositor ecosystem and match the common industry-standard naming convention. They do not refer to any proprietary software's labels.

---

## Production Documents — Naming Exemption

**Cycle 25 decision (Kai Nakamura / Technical Art Engineer, ratified in assignment):**

Files in `output/production/` are **explicitly exempt** from the LTG naming format.

### Rationale

Production-administration documents (bibles, briefs, critiques, statements of work,
pitch indexes, etc.) are human-facing reference material, not versioned pipeline
assets. Renaming them to `LTG_PROD_*` format would:

1. Break cross-references in dozens of existing docs.
2. Add version numbers that are meaningless for non-iterating reference documents.
3. Provide no workflow benefit — these files are not consumed by pipeline scripts.

### Rule (mandatory)

- Files **inside `output/production/`**: use **descriptive names only** (e.g.,
  `production_bible.md`, `naming_conventions.md`, `sow_cycle25.md`).
  Do **not** apply the `LTG_[CATEGORY]_descriptor_v[###]` format.
- Files **outside `output/production/`**: the standard LTG format applies as stated
  in this document. No other exemptions exist.

### What is NOT exempt

Pipeline assets that happen to live in production subfolders (e.g., `output/production/tools/`
or `output/production/templates/`) must still follow the LTG naming convention.

---

## Image Output Standards

**Added Cycle 25 — applies to all raster image assets.**

- **Prefer the smallest resolution appropriate for the task.** High resolution is only justified when fine detail must be inspected.
- **Hard limit:** Every saved PNG/JPG must be ≤ 1280px in both width and height.
- Resize with `img.thumbnail((1280, 1280), Image.LANCZOS)` before saving — aspect ratio is preserved automatically.
- For close-up detail inspection: produce a cropped region rather than a full large image. The crop must also be ≤ 1280×1280px.

---

## Retired Prefix Systems

The following naming prefix systems are **retired as of this document's approval date (2026-03-29):**

| Retired Prefix | Source | Retirement Reason |
|---|---|---|
| `LH_INT_` | Early environment documents (interior background system) | Conflicts with canonical `LTG_ENV_` system |
| `GL_` | Early environment documents (Glitch Layer system) | Conflicts with canonical `LTG_ENV_glitchlayer_` system |

### Reconciliation Schedule
Assets currently named under retired systems will be reconciled and renamed as part of the **Environment Document v3.0** revision, which will be the first environment document to use the canonical `LTG_ENV_` prefix throughout. Until then:
- **Do not create new assets** using `LH_INT_` or `GL_` prefixes.
- **Do not rename existing retired-prefix assets** in isolation — wait for the v3.0 reconciliation pass to avoid version tracking confusion.
- If you receive an asset with a retired prefix, flag it to the Art Director before incorporating it into new work.

---

## Descriptor Formatting Rules

- **Lowercase only.** No CamelCase, no ALL_CAPS in the descriptor field.
- **Words separated by underscores.** No spaces, no hyphens.
- **Be specific but concise.** `ep01_cold_open_panel07` is correct. `stuff_for_episode_one_v2` is not.
- **Episode references:** Use `ep[##]` format — `ep01`, `ep02`, not `episode1` or `E1`.
- **Sequence references:** Use `seq[##]` format — `seq01`, `seq07`.
- **Act references:** Use `act[#]` format — `act01`, `act02`, `act03`.
- **Character references in filenames:** Use lowercase short names: `luma`, `byte`, `cosmo`, `miri`, `glitchkin`.
- **Time of day qualifiers:** `_day`, `_night`, `_dusk`. Applied at the end of the descriptor, before the version number.

---

## Frequently Asked Questions

**Q: What if my file has more than one category?**
Use the primary category — the one that best describes the file's main purpose. If a file is genuinely split-purpose (e.g., a color key that is also a style frame), use `COLOR` and note the dual function in the file's metadata or in the accompanying production document.

**Q: What if I need a subdescriptor (e.g., front view vs. side view of a turnaround)?**
Add it to the descriptor field: `LTG_CHAR_luma_turnaround_front_v001.png` and `LTG_CHAR_luma_turnaround_side_v001.png`. The convention supports multi-word descriptors.

**Q: Can I shorten `LTG` for internal use?**
No. The show code is always `LTG`. Consistency across all files is the point.

**Q: What about source files vs. export files?**
Same name, different extension. The Krita source file and its PNG export share a name: `LTG_CHAR_luma_designsheet_v001.kra` and `LTG_CHAR_luma_designsheet_v001.png`. OpenToonz scene files use `.xdts`; Inkscape files use `.svg`. This makes source-export pairing unambiguous.

---

*Document maintained by: Alex Chen, Art Director*
*Naming convention questions: bring to Art Director before creating files, not after.*
*Compliance with this document is mandatory from 2026-03-29 onward.*
