# Production Design Systems & Style Consistency Audit
## "Luma & the Glitchkin" — Pitch Package
### Critique 11 — Gunnar Eriksson

**Critic:** Gunnar Eriksson, Production Design Systems & Style Consistency Enforcer
**Date:** 2026-03-29
**Cycle:** 24 (post-stylization delivery)
**Scope:** Cross-asset consistency audit, naming convention compliance, style guide adherence, production viability

---

## OVERALL COMPLIANCE VERDICT

**NON-COMPLIANT. Production-ready in core visual language. Not production-ready in pipeline hygiene.**

The show's visual design system is internally coherent where the team has followed it. The two-world color architecture (warm/organic Real World vs. cold/digital Glitch Layer) is consistently applied across the primary assets reviewed. The 3-tier line weight standard is documented and present in the current expression sheet versions. The master palette is comprehensive, with shadow companions, derived/modified colors, and forbidden combinations documented to a high standard.

However, the naming convention system has been violated at scale and the violations remain unresolved after multiple cycles. Legacy filenames coexist with LTG-compliant filenames in every asset category. The production document naming system is non-compliant without exception. Superseded asset versions remain on disk without archival in a significant portion of directories. The Glitch character sheet does not comply with the canvas and grid standards established by `character_sheet_standards_v001.md`. Three principal character color models do not exist as visual production references.

These are not aesthetic weaknesses. They are system failures. A new artist hired onto this production would face contradictory, ambiguous file structures on day one.

*"Consistent or inconsistent. There is no third category. 'Close enough' is a form of inconsistent."*

---

## CATEGORY-BY-CATEGORY FINDINGS

### CATEGORY 1: STYLE GUIDE — `output/style_guide.md`

| Element | Status | Finding |
|---|---|---|
| Two-world color architecture | COMPLIANT | Real World warm palette / Glitch Layer cool palette distinction is internally consistent. Governing principles documented. |
| Line weight standard | COMPLIANT | 3-tier system (silhouette 4px / interior ~2px / detail ~1–1.5px at output) documented in `character_sheet_standards_v001.md`. Brow weight error (Cycle 19 fix: 10px→4px) resolved. Current sheets compliant. |
| Line color | COMPLIANT | `#3B2820` (Deep Cocoa) is the universal line color, not pure black. Documented in master palette RW-11. Present in character specs. |
| Construction guide policy | COMPLIANT | Policy is clear: OFF by default in pitch output, ON only for production reference. `LTG_CHAR_luma_expression_sheet_v004_guides.png` correctly labelled as internal-only. |
| Void Black minimum | COMPLIANT | `#0A0A14` documented as minimum fill/area value. `#050508` exception properly scoped to crevice shadows and void abyss only. |
| Style guide own filename | NON-COMPLIANT | `style_guide.md` — does not follow `LTG_[CATEGORY]_[descriptor]_v[###].[ext]` format. This is the master visual reference document for the production. It does not comply with the naming system it establishes. This has been flagged in the pitch package index for "3 cycles running." Three cycles of deferral on the document that establishes the rules is not acceptable. |

**Category 1 Verdict: COMPLIANT on content. NON-COMPLIANT on self-naming.**

---

### CATEGORY 2: MASTER COLOR PALETTE — `output/color/palettes/master_palette.md`

| Element | Status | Finding |
|---|---|---|
| Real World palette documentation | COMPLIANT | RW-01 through RW-13 + shadow companions fully documented. Use-case rules present for each swatch. |
| Glitch palette documentation | COMPLIANT | GL-01 through GL-08a + depth tier derived values fully documented. Shadow companion table present. |
| Derived/modified colors | COMPLIANT | DRW-01 through DRW-18 documented with source derivations. Scene-specific scoping enforced. |
| ENV derived colors | COMPLIANT | ENV-01 through ENV-13 documented with correction history. ENV-06 cyan-lit correction from Cycle 13 documented and traced to generator. |
| Forbidden combinations | NOT VERIFIED | Section 4 not reviewed in this audit pass. Known to exist from index reference. |
| Opacity-based specs | COMPLIANT | Cycle 2 audit eliminated opacity-based specs. All shadows are flat hex values. ENV-03 warm spill canonical alpha documented. |
| Skin Shadow vs. Rust Shadow distinction | COMPLIANT | RGB channel values for both documented; use-case separation enforced in text. The 22-point blue-channel gap and 32-point green-channel gap are called out as potential painter confusion vectors with corrective scoping. |
| GL-07 Corrupted Amber Cycle 22 fix | COMPLIANT | Canonical value confirmed as `#FF8C00`. Four-version error (`#C87A20`) in SF02 generator corrected in v005. Generator and palette now agree. |
| JEANS_BASE UV-ambient rule | COMPLIANT | Documented Cycle 22. |
| Palette document own filename | NON-COMPLIANT | `master_palette.md` does not conform to `LTG_COLOR_[descriptor]_v[###].md` format. The single source of truth for all color decisions does not follow the naming system. Same systemic failure as `style_guide.md`. |
| Cold overlay arithmetic (DRW-01 / SF01) | COMPLIANT | C10-1 resolved Cycle 13. Documented with verified arithmetic. Prior incorrect comment corrected. |

**Category 2 Verdict: COMPLIANT on content. NON-COMPLIANT on self-naming.**

---

### CATEGORY 3: CHARACTER SHEETS — `output/characters/main/`

| Asset | Status | Finding |
|---|---|---|
| Luma expression sheet v004 | COMPLIANT | 6 expressions, 3×2 grid, 1200×900, construction guides OFF, CURIOUS upgraded. Current canonical per Cycle 22. No blocking issues. |
| Byte expression sheet v004 | COMPLIANT | 9 expressions, 3×3 grid, STORM/CRACKED compliant with byte.md Section 9B. 4×2 to 3×3 upgrade documented. Cracked-eye glyph spec-correct. |
| Cosmo expression sheet v004 | COMPLIANT | 6 expressions, 3×2. SKEPTICAL arm posture corrected. All 6 expressions distinct. |
| Grandma Miri expression sheet v002 | COMPLIANT | 5 full-body expressions, 3×2 (5th slot intentional per standard). Distinct posture silhouettes. Dmitri C-grade root cause resolved. |
| Glitch expression sheet v002 | NON-COMPLIANT | Exists at 800×800px on a 2×2 grid. `character_sheet_standards_v001.md` Section 5 mandates 1200×900 canvas for character expression sheets. Glitch is a character that appears in the pitch package. The standard is binding from Cycle 22 onward. 800×800 / 2×2 is non-compliant. Each expression panel at this canvas size is 400×400 — insufficient for the body detail and expression read standards defined in the style guide. |
| Byte expression sheets v001–v003 | NON-COMPLIANT (superseded) | Superseded versions remain on disk in the same directory as v004. No archival separation. A new artist cannot immediately identify which version is canonical without reading the index. Superseded character sheets for Luma and Cosmo (v002, v003) share this problem. |
| Luma expression sheet v004 guides | COMPLIANT | Correctly labelled as internal reference. Correctly excluded from pitch package assets. |
| Character lineup v003 | COMPLIANT | Float-gap annotation present. Four-character lineup. LTG-named. |
| Character lineup v004 | STATUS UNCLEAR | `LTG_CHAR_lineup_v004.png` exists on disk but is listed only as a Cycle 24 open item ("Glitch added to character lineup") with LOWER priority. If Glitch has been added without being documented in the index, this is a version control failure. If it has not yet been added, it is a pre-canonical file that should not be in the main directory yet. Either state is non-compliant. |
| Turnarounds (4 characters) | NON-COMPLIANT (naming) | Legacy filenames `byte_turnaround.png`, `cosmo_turnaround.png`, `luma_turnaround.png`, `miri_turnaround.png` coexist with LTG-compliant copies. LTG-compliant copies are present (`LTG_CHAR_*_turnaround_v001.png`). Originals should be archived or removed. Current state: two sets of files, one compliant, one not, in the same directory. |
| Glitch turnaround v001 | NON-COMPLIANT | Generator script `LTG_CHAR_glitch_turnaround_v001.py` is stored in `output/tools/` — correct category for tools. However this is a `CHAR` category tool using `CHAR` naming rather than `TOOL` naming. This contradicts the Cycle 22 directive that renamed Luma/Byte/Cosmo expression sheet generators from `LTG_CHAR_*` to `LTG_TOOL_*`. Three generators were renamed. The Glitch generators were not. |
| Color model visual PNGs (Luma, Byte, Cosmo) | NON-COMPLIANT | `grandma_miri_color_model.md` and `LTG_COLOR_grandma_miri_color_model_v001.png` both exist. Glitch character has a visual color model PNG. Luma, Byte, and Cosmo have `.md` specifications only. No visual production reference PNG exists for the three lead characters. A new colorist cannot verify palette compliance by reading a markdown file. The spec document exists; the deliverable does not. |

**Category 3 Verdict: CURRENT canonical sheets COMPLIANT. Glitch sheet NON-COMPLIANT with canvas standard. Supporting file hygiene NON-COMPLIANT.**

---

### CATEGORY 4: BACKGROUNDS / ENVIRONMENTS — `output/backgrounds/environments/`

| Asset | Status | Finding |
|---|---|---|
| Grandma Kitchen v003 | COMPLIANT | Three-wall texture, perspective-correct floor grid, CRT glow, Real World palette only. Current canonical. |
| Tech Den v004 | COMPLIANT | Three individuated monitor glow zones, light shaft in desk zone, inhabited (Cosmo's jacket visible). Real World palette only in correct zone. |
| School Hallway v002 | COMPLIANT | Ceiling artifact resolved, human evidence present, camera height corrected. |
| Millbrook Main Street v002 | COMPLIANT | Power lines with catenary sag, road plane with center lines, crosswalk. |
| Classroom BG v002 | COMPLIANT | Dual-source lighting, inhabitant evidence. Supersedes v001. |
| Glitch Layer frame v003 | COMPLIANT | Scanline overlay as final pass. Canonical Cycle 21 version. |
| Other Side BG v002 | COMPLIANT | Background-only. Spec-compliant. |
| Legacy filenames coexisting with LTG copies | NON-COMPLIANT | `bg_glitch_layer_encounter.png` (no LTG prefix) coexists with `LTG_ENV_glitchlayer_encounter_v001.png`. `frame01_house_interior.png` coexists with `LTG_ENV_lumashome_study_interior_v001.png`. `glitch_layer_frame.png` coexists with `LTG_ENV_glitchlayer_frame_v001.png`. These are duplicates: non-LTG originals and LTG-compliant copies exist side by side. Originals have not been archived. Three ENV environments in this state. |
| Superseded environment versions present | NON-COMPLIANT | `LTG_ENV_tech_den_v001.png`, `v002.png`, `v003.png` remain on disk alongside canonical `v004.png`. Same pattern for `grandma_kitchen` v001/v002/v003, `school_hallway` v001/v002, `glitch_layer_frame` v001/v002/v003. No archival separation. At production scale with multiple artists per environment, this version proliferation is a continuous source of artist error — the wrong version will be used. |
| `bg_glitch_layer_encounter.py` in environments directory | NON-COMPLIANT | A generator script (`bg_glitch_layer_encounter.py`) is stored in the `output/backgrounds/environments/` directory. Tools belong in `output/tools/`. This file's presence in the environment output folder contaminates the asset directory with source code. |

**Category 4 Verdict: Current canonical versions COMPLIANT on visual content. File hygiene NON-COMPLIANT across multiple instances.**

---

### CATEGORY 5: STYLE FRAMES — `output/color/style_frames/`

| Asset | Status | Finding |
|---|---|---|
| SF01 Discovery v003 | COMPLIANT | Ghost Byte alpha calibrated. Victoria A+. Warm/Real World palette dominant. LOCKED. |
| SF01 Discovery v003 styled | COMPLIANT | Hand-drawn stylization applied with realworld mode. Paper tooth treatment. Approved as pitch primary. |
| SF02 Glitch Storm v005 | COMPLIANT | GL-07 `#FF8C00` corrected. Window pane alpha 115/110. Color story matches rendered output. |
| SF02 Glitch Storm v005 styled | STATUS PENDING | Zone-blended stylization delivered. Director confirmation pending per Cycle 24 status table. A pitch asset that is "delivered — pending director confirmation" is not in a confirmed compliance state. |
| SF03 Other Side v003 | COMPLIANT | Byte body GL-01b corrected. Eye radius ≥15px. Void Black slash removed. |
| SF03 Other Side v003 styled | STATUS PENDING | Full glitch treatment delivered. Byte body read confirmation pending per Cycle 24 status table. Same issue as SF02 styled: unconfirmed status is not compliant status. |
| Superseded style frame versions | NON-COMPLIANT | Versions v001 through v004 of SF02 remain in directory alongside v005. Versions v001 and v002 of SF03 remain alongside v003. These are not archived. Discovery v001 and v002 remain alongside v003. In the same folder: 13 style frame PNGs for three style frames. A new compositor has no visual indication of which is canonical without reading the index. |
| `LTG_TOOL_style_frame_02_glitch_storm_v005.py` in style_frames directory | NON-COMPLIANT | A generator script stored in the style frames output folder. Tools belong in `output/tools/`. |
| Color story document filename | NON-COMPLIANT | `ltg_style_frame_color_story.md` does not follow `LTG_COLOR_[descriptor]_v[###].md` format. `ltg_` prefix is not the `LTG_` system — it appears to be a manual non-standard prefix. This file should be `LTG_COLOR_styleframe_color_story_v001.md`. |

**Category 5 Verdict: Canonical approved versions COMPLIANT. Superseded versions NOT ARCHIVED. Two pending-confirmation assets in unverified state. File hygiene NON-COMPLIANT.**

---

### CATEGORY 6: STORYBOARDS — `output/storyboards/`

| Asset | Status | Finding |
|---|---|---|
| Act 2 contact sheet v005/v006 | COMPLIANT | 12-panel arc, LTG-named, arc-coded borders. |
| Act 1 full contact sheet v001 | COMPLIANT | 5-panel combined Act 1 sheet. LTG-named. |
| LTG-named storyboard panels | COMPLIANT | All act-numbered panels (`LTG_SB_coldopen_panel_*`, `LTG_SB_act1_panel_*`, `LTG_SB_act2_panel_*`) follow naming convention. Versioning present. Superseded versions correctly incremented. |
| Legacy cold open panels (P01–P25) | NON-COMPLIANT (naming) | 27 files using `panel_p[##]_[descriptor].png` format remain on disk in `output/storyboards/panels/`. These do not follow the LTG naming system. Their LTG-compliant equivalents (`LTG_SB_coldopen_panel_[##]_v001.png`) exist in the same directory. Acknowledged in the pitch package index for multiple cycles as "LTG rename outstanding." This is not a rename issue — the LTG versions have been created. The legacy originals need to be archived. |
| `contact_sheet.png` (legacy) | NON-COMPLIANT | Non-LTG filename for the cold open contact sheet. LTG equivalent exists. Original not archived. |
| Non-LTG storyboard documents | NON-COMPLIANT | `ep01_cold_open.md`, `act2_thumbnail_plan_v001.md`, `act2_thumbnail_plan_v002.md` do not use LTG naming. These are production reference documents (`LTG_SB_*` or `LTG_PROD_*` format expected). |

**Category 6 Verdict: Current canonical storyboard assets COMPLIANT on naming. Legacy originals NOT ARCHIVED. Non-LTG documents present.**

---

### CATEGORY 7: PRODUCTION DOCUMENTS — `output/production/`

| Asset | Status | Finding |
|---|---|---|
| `pitch_package_index.md` | NON-COMPLIANT | The master navigator for all pitch assets does not use LTG naming. Expected: `LTG_PROD_pitch_package_index_v001.md`. |
| `production_bible.md` | NON-COMPLIANT | Expected: `LTG_PROD_production_bible_v[###].md`. |
| `naming_conventions.md` | NON-COMPLIANT | The naming conventions document does not follow the naming conventions it defines. This has been flagged in the pitch package index as "ironic — flagged 3 cycles running." Three cycles. The naming_conventions.md is version 1.1 and has never been renamed. |
| `naming_convention_compliance_checklist.md` | NON-COMPLIANT | Same as above. |
| `character_sheet_standards_v001.md` | NON-COMPLIANT | Expected category: `PROD`. Expected name: `LTG_PROD_character_sheet_standards_v001.md`. Note: the document's own footer cites itself as `LTG_PROD_character_sheet_standards_v001.md` — the intended correct name. The actual filename on disk does not match its own stated name. |
| `byte_float_physics.md` | NON-COMPLIANT | Expected: `LTG_FX_byte_float_physics_v001.md` (per naming_conventions.md example `LTG_FX_byte_float_physics_v001.md`). The naming conventions document provides this exact example — the file is named differently than its own spec's example. |
| `fx_spec_cold_open.md` | NON-COMPLIANT | Expected: `LTG_FX_spec_cold_open_ep01_v001.md`. |
| `fx_confetti_density_scale.md` | NON-COMPLIANT | Expected: `LTG_FX_confetti_density_scale_v001.md`. |
| `corruption_visual_brief.md` | NON-COMPLIANT | Expected: `LTG_PROD_corruption_visual_brief_v[###].md` or `LTG_FX_corruption_visual_brief_v[###].md`. |
| `production_bible.md` | NON-COMPLIANT | Expected: `LTG_PROD_production_bible_v[###].md`. |
| `storyboard_pitch_export.png` | NON-COMPLIANT | Expected: `LTG_SB_[descriptor]_v[###].png`. |
| `show_logo.png` | NON-COMPLIANT | Expected: `LTG_BRAND_show_logo_v[###].png`. Placeholder tagline issue additionally unresolved (see separate finding below). |
| `ltg_pitch_brief_v001.md` | NON-COMPLIANT | Non-standard prefix `ltg_` (lowercase) instead of `LTG_`. Expected: `LTG_PROD_pitch_brief_v001.md`. |
| Statement of work files | NON-COMPLIANT | `statement_of_work_cycle[##].md` / `statement_of_work_cycle_01.md` (inconsistent between cycles). Expected: `LTG_PROD_sow_cycle[##]_v001.md`. Multiple cycles inconsistent with each other. |
| Critique and feedback files | NON-COMPLIANT | `critic_feedback_c[##]_[name].md` and `critique_c[##]_[name]_[surname].md` formats mixed and non-LTG. Production archive function — not pitch-facing — but they occupy production space without system compliance. |
| `LTG_BRAND_logo_asymmetric_v001.png`, `v002.png` | COMPLIANT | Two LTG-branded logo files. LTG-named, versioned. |

**Category 7 Verdict: NON-COMPLIANT. No production document except the two brand logo files uses the LTG naming system. Zero production documents are LTG-compliant.**

---

### CATEGORY 8: TOOLS DIRECTORY — `output/tools/`

| Element | Status | Finding |
|---|---|---|
| LTG-named generators (TOOL category) | COMPLIANT | `LTG_TOOL_*` generators correctly categorized and named. Tools index (README.md) documents all tools. |
| Remaining `LTG_CHAR_*` generators in tools/ | NON-COMPLIANT | `LTG_CHAR_luma_expression_sheet_v002.py`, `LTG_CHAR_luma_expression_sheet_v003.py`, `LTG_CHAR_luma_expression_sheet_v004.py`, `LTG_CHAR_byte_expression_sheet_v004.py`, `LTG_CHAR_cosmo_expression_sheet_v004.py`, `LTG_CHAR_glitch_expression_sheet_v001.py`, `LTG_CHAR_glitch_expression_sheet_v002.py`, `LTG_CHAR_glitch_turnaround_v001.py`, `LTG_CHAR_glitch_color_model_v001.py` are in the tools directory but use `CHAR` category prefix rather than `TOOL`. Cycle 22 renamed Luma v002/v003/v004 and Byte v004 and Cosmo v004 — the README states this. However, the old filenames remain on disk in `output/tools/`. The renamed versions are also present. This means both `LTG_CHAR_luma_expression_sheet_v004.py` AND `LTG_TOOL_luma_expression_sheet_v004.py` exist. Double files. Rename executed but originals not deleted. |
| Legacy (non-LTG) scripts | NON-COMPLIANT | `bg_glitch_layer_frame.py`, `bg_house_interior_frame01.py`, `bg_layout_generator.py`, `byte_expressions_generator.py`, `character_lineup_generator.py`, `character_turnaround_generator.py`, `color_key_generator.py`, `color_swatch_generator.py`, `contact_sheet_generator.py`, `logo_generator.py`, `luma_expression_sheet_generator.py`, `luma_face_generator.py`, `panel_chaos_generator.py`, `panel_interior_generator.py`, `proportion_diagram.py`, `silhouette_generator.py`, `storyboard_panel_generator.py`, `storyboard_pitch_export_generator.py`, `style_frame_01_rendered.py`, `style_frame_generator.py` — 20 scripts with no LTG prefix. Documented in README as "legacy." Not archived. |
| Tools README.md | NON-COMPLIANT | `README.md` does not use LTG naming. Expected: `LTG_TOOL_index_v001.md` or `LTG_PROD_tools_index_v001.md`. |

**Category 8 Verdict: NON-COMPLIANT on legacy file retention. Renamed files not cleaned up. 20 legacy scripts present without archival.**

---

## NON-COMPLIANCE LIST — PRIORITIZED BY SEVERITY

### SEVERITY 1 — PRODUCTION BLOCKING

| ID | Item | File(s) | Issue |
|---|---|---|---|
| NC-01 | Glitch expression sheet canvas non-compliance | `LTG_CHAR_glitch_expression_sheet_v002.png` | 800×800 / 2×2 grid violates `character_sheet_standards_v001.md` Section 5 mandate of 1200×900. Current sheet is under-spec for its required production function. A buyer cannot assess character expressiveness at this canvas. |
| NC-02 | No visual color models for three lead characters | (missing) `LTG_COLOR_luma_color_model_v001.png`, `LTG_COLOR_byte_color_model_v001.png`, `LTG_COLOR_cosmo_color_model_v001.png` | Color model PNGs for Grandma Miri and Glitch exist. Luma, Byte, Cosmo have `.md` specs only. A new artist or studio colorist cannot verify production compliance from a markdown file. The three-lead asymmetry is a structural gap. |
| NC-03 | Stylized style frames in unconfirmed state | `LTG_COLOR_styleframe_glitch_storm_v005_styled.png`, `LTG_COLOR_styleframe_otherside_v003_styled.png` | Cycle 24 status table shows these as "delivered — pending director confirmation." Pitch package index designates the non-stylized versions as pitch primaries but implies stylized versions will supersede them. The canonical pitch primary for SF02 and SF03 is currently ambiguous. |
| NC-04 | `LTG_CHAR_lineup_v004.png` undocumented | `LTG_CHAR_lineup_v004.png` | File exists on disk. Pitch package index lists Glitch addition to lineup as a Cycle 24 LOWER priority open item. If the file was generated before official index documentation, it is pre-canonical content in the main production directory. If it contains Glitch, the character lineup section of the index needs immediate update. Either way: undocumented asset in pitch package directory. |

### SEVERITY 2 — PIPELINE HYGIENE FAILURES

| ID | Item | File(s) | Issue |
|---|---|---|---|
| NC-05 | Generator scripts in output asset directories | `bg_glitch_layer_encounter.py` (in `environments/`), `LTG_TOOL_style_frame_02_glitch_storm_v005.py` (in `style_frames/`) | Tools must be in `output/tools/`. Source code in asset output directories contaminates the output structure. Artists and compositors searching for assets encounter scripts. |
| NC-06 | LTG rename completed but originals not archived — characters | `byte_turnaround.png`, `cosmo_turnaround.png`, `luma_turnaround.png`, `miri_turnaround.png` (in `turnarounds/`); `byte_expressions.png`, `character_lineup.png`, `luma_expression_sheet.png`, `luma_expressions.png`, `luma_face_closeup.png`, `proportion_diagram.png` (in `main/`) | LTG-compliant copies were created. Originals were not archived. Two copies of the same asset exist. |
| NC-07 | LTG rename completed but originals not archived — environments | `bg_glitch_layer_encounter.png`, `frame01_house_interior.png`, `glitch_layer_frame.png` (in `environments/`) | Same as NC-06. LTG-compliant copies exist. Originals present. |
| NC-08 | LTG rename completed but originals not archived — storyboards | `panel_p[01–25]_*.png`, `contact_sheet.png` (27 files in `storyboards/panels/`) | 27 non-LTG storyboard panels with LTG equivalents in the same directory. Acknowledged for multiple cycles as housekeeping. The LTG versions exist — the originals need to be moved to an archive subdirectory. |
| NC-09 | Renamed generator files not cleaned up | `LTG_CHAR_luma_expression_sheet_v002.py`, `v003.py`, `v004.py`, `LTG_CHAR_byte_expression_sheet_v004.py`, `LTG_CHAR_cosmo_expression_sheet_v004.py` (in `output/tools/`) | Cycle 22 rename created `LTG_TOOL_*` versions. The `LTG_CHAR_*` originals remain. Both exist. The rename was executed; the cleanup was not. Additionally: `LTG_CHAR_glitch_expression_sheet_v001.py`, `v002.py`, `LTG_CHAR_glitch_turnaround_v001.py`, `LTG_CHAR_glitch_color_model_v001.py` were never renamed — these are Glitch character generators that post-date the CHAR→TOOL rename directive. |
| NC-10 | Superseded character sheets not archived | `LTG_CHAR_luma_expression_sheet_v002.png`, `v003.png`, `LTG_CHAR_byte_expression_sheet_v001.png`, `v002.png`, `v003.png`, `LTG_CHAR_cosmo_expression_sheet_v001.png`, `v002.png`, `v003.png`, `LTG_CHAR_grandma_miri_expression_sheet_v001.png` (in `characters/main/`) | Superseded versions coexist with canonical current versions in the same directory. At production scale, this creates version selection errors. The index says "use v003" or "use v004" — but a new artist reading a file listing has no visual cue of canonical status. |
| NC-11 | Superseded environment BGs not archived | Multiple versions of Tech Den (v001–v003), Grandma Kitchen (v001–v002), School Hallway (v001), Glitch Layer frame (v001–v002), Other Side BG (v001) alongside current canonical versions in `environments/` | Same issue as NC-10 applied to environments. |
| NC-12 | Superseded style frames not archived | SF01 v001–v002, SF02 v001–v004, SF03 v001–v002 alongside canonical versions in `style_frames/` | 13 style frame PNGs in one directory for three style frames. No folder separation between archived and canonical. |

### SEVERITY 3 — NAMING SYSTEM NON-COMPLIANCE (SYSTEMIC)

| ID | Item | File(s) | Issue |
|---|---|---|---|
| NC-13 | All production documents use non-LTG naming | `production_bible.md`, `naming_conventions.md`, `naming_convention_compliance_checklist.md`, `character_sheet_standards_v001.md`, `style_guide.md`, `master_palette.md`, `byte_float_physics.md`, `fx_spec_cold_open.md`, `fx_confetti_density_scale.md`, `corruption_visual_brief.md`, `storyboard_pitch_export.png`, `show_logo.png`, `ltg_pitch_brief_v001.md`, all statement_of_work files, all critique files | Zero production documents use the `LTG_[CATEGORY]_[descriptor]_v[###].[ext]` format. The naming system has been mandatory from Cycle 13. Not one production document was retroactively renamed. The naming conventions document cannot be enforced by a system that the document itself violates. |
| NC-14 | `naming_conventions.md` self-violation | `naming_conventions.md` | Three-cycle-documented irony. The document that defines the naming system is not named according to the naming system. This is not cosmetic. It signals to every new team member that compliance is optional. |
| NC-15 | Legacy scripts not archived in tools/ | 20 scripts (see Category 8) | Non-LTG legacy scripts remain active in `output/tools/` alongside LTG-compliant tools. They are documented as "legacy" in the README but not archived. The README documents their LTG-compliant replacements — the originals serve no production function and represent ambiguity. |

---

## WHAT IS PRODUCTION-READY

The following assets are compliant with the established design system, correctly named, and at their current canonical version. A new artist could use these as references and produce consistent work.

| Asset | File | State |
|---|---|---|
| Luma expression sheet | `LTG_CHAR_luma_expression_sheet_v004.png` | PRODUCTION READY |
| Byte expression sheet | `LTG_CHAR_byte_expression_sheet_v004.png` | PRODUCTION READY |
| Cosmo expression sheet | `LTG_CHAR_cosmo_expression_sheet_v004.png` | PRODUCTION READY |
| Grandma Miri expression sheet | `LTG_CHAR_grandma_miri_expression_sheet_v002.png` | PRODUCTION READY |
| Character lineup | `LTG_CHAR_lineup_v003.png` | PRODUCTION READY |
| Grandma Miri color model (visual) | `LTG_COLOR_grandma_miri_color_model_v001.png` | PRODUCTION READY |
| SF01 Discovery | `LTG_COLOR_styleframe_discovery_v003.png` (and styled variant) | PRODUCTION READY |
| SF02 Glitch Storm | `LTG_COLOR_styleframe_glitch_storm_v005.png` | PRODUCTION READY (non-stylized confirmed) |
| SF03 Other Side | `LTG_COLOR_styleframe_otherside_v003.png` | PRODUCTION READY (non-stylized confirmed) |
| Grandma Kitchen | `LTG_ENV_grandma_kitchen_v003.png` | PRODUCTION READY |
| Tech Den | `LTG_ENV_tech_den_v004.png` | PRODUCTION READY |
| School Hallway | `LTG_ENV_school_hallway_v002.png` | PRODUCTION READY |
| Millbrook Main Street | `LTG_ENV_millbrook_main_street_v002.png` | PRODUCTION READY |
| Classroom BG | `LTG_ENV_classroom_bg_v002.png` | PRODUCTION READY |
| Glitch Layer frame | `LTG_ENV_glitchlayer_frame_v003.png` | PRODUCTION READY |
| Other Side BG | `LTG_ENV_other_side_bg_v002.png` | PRODUCTION READY |
| Act 2 storyboard contact sheet | `LTG_SB_act2_contact_sheet_v005.png` (or v006) | PRODUCTION READY |
| LTG brand logos | `LTG_BRAND_logo_asymmetric_v001.png`, `LTG_BRAND_logo_asymmetric_v002.png` | PRODUCTION READY |
| Master palette content | `output/color/palettes/master_palette.md` | CONTENT: PRODUCTION READY. Filename: non-compliant. |
| Character sheet standards | `output/production/character_sheet_standards_v001.md` | CONTENT: PRODUCTION READY. Filename: non-compliant. |
| Render library | `LTG_TOOL_render_lib_v001.py` | PRODUCTION READY |
| Stylization tool | `LTG_TOOL_stylize_handdrawn_v001.py` | PRODUCTION READY |

---

## REQUIRED ACTIONS BEFORE NEXT EXTERNAL PITCH PRESENTATION

1. Rebuild Glitch expression sheet at 1200×900 / 3×2 (NC-01).
2. Generate visual color model PNGs for Luma, Byte, and Cosmo (NC-02).
3. Confirm and document canonical status of SF02 and SF03 stylized versions (NC-03).
4. Verify, document, or archive `LTG_CHAR_lineup_v004.png` (NC-04).
5. Archive all legacy non-LTG filenames from asset directories into `archived/` subdirectories (NC-06, NC-07, NC-08).
6. Remove or archive post-rename `LTG_CHAR_*` generator originals from `output/tools/` (NC-09).

---

*Consistent or inconsistent. There is no third category. 'Close enough' is a form of inconsistent.*

*— Gunnar Eriksson*
*2026-03-29*
