<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Critique C18 — Petra Volkov (Technical Art & Pipeline Quality Audit)
**Critique Cycle:** C18 | **Work Cycle reviewed:** C43 (with standing issues from C42 and earlier)
**Date:** 2026-03-30
**Assets reviewed:** All generators in `output/tools/`, all output PNGs in `output/`, production documentation, naming convention compliance, dependency documentation, path hygiene

---

## Pipeline Audit Summary

This is a full-pitch technical audit. I do not distinguish between new and old work — the complete pitch is reviewed. I have cross-referenced: README.md Script Index (line 9 and Script Index table), `output/production/precritique_qa_c41.md` (most recent QA baseline), `output/production/native_resolution_audit_c42.md`, `output/production/naming_conventions.md`, and direct file inspection of all C43 generators plus spot checks across the older tool set.

---

## ISSUE 1: Hardcoded absolute paths — new C43 generators and widespread pattern

**Severity: FAIL**

`LTG_TOOL_sb_cold_open_P07.py` line 45: `PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"`
`LTG_TOOL_sb_cold_open_P09.py` line 52: `PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"`
`LTG_TOOL_sb_ep05_covetous.py` line 46: `PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"`

All three C43 generators hardcode the absolute path to the user's home directory. These scripts will fail on any machine that is not `/home/wipkat/`. The pattern also exists in older generators including `LTG_TOOL_styleframe_discovery.py` (line 63), `LTG_TOOL_style_frame_04_resolution.py` (line 63), `LTG_TOOL_sf_covetous_glitch.py` (line 671), and `LTG_TOOL_character_lineup.py` (line 985). This is not a new problem but it is not getting better — C43 added three more violations. The canonical fix is `os.path.join(os.path.dirname(__file__), "..", "..", "output", ...)` or a project-root-relative `OUTPUT_ROOT` constant resolved at runtime.

Score: 0/100
- All three C43 generators hardcode `/home/wipkat/team/` — fails on any other machine.
- The pattern has persisted across at least 6+ generators without being addressed by CI.
Bottom line: a machine-local pipeline is not a production pipeline; any clean-install test fails immediately.

---

## ISSUE 2: Two generators write to the same output file — LTG_COLOR_styleframe_discovery.png

**Severity: FAIL**

Both `LTG_TOOL_style_frame_01_discovery.py` and `LTG_TOOL_styleframe_discovery.py` write to `output/color/style_frames/LTG_COLOR_styleframe_discovery.png`. The `native_resolution_audit_c42.md` explicitly flagged `LTG_TOOL_style_frame_01_discovery.py` as "largely superseded" by the C38 canonical rebuild and recommended deprecation. As of C43 the old generator is still present in `output/tools/` (not moved to `output/tools/legacy/`), undeprecated, and undocumented as retired. The output file's provenance is therefore ambiguous: a CI runner cannot determine which generator produced the current PNG from documentation alone.

Score: 0/100
- `LTG_TOOL_style_frame_01_discovery.py` documented as superseded in C42 audit but still active in tools directory.
- Two generators writing identical output path with no deprecation marker or retirement stub violates the single-source provenance requirement.
Bottom line: asset provenance is unresolvable without running both generators and diffing — this is not documentation-traceable.

---

## ISSUE 3: Output filename naming convention violations — version number absent

**Severity: WARN**

Per `output/production/naming_conventions.md` §"Canonical Format", every production asset must carry a `_v[###]` version suffix. The three C43 outputs break this rule:
- `LTG_SB_cold_open_P07.png` — no version suffix
- `LTG_SB_cold_open_P09.png` — no version suffix
- `LTG_SB_ep05_covetous.png` — no version suffix

Additionally, the storyboard panel naming splits into two inconsistent conventions in the same directory: 27 files follow `LTG_SB_coldopen_panel_XX.png` (from cycle 5 onward) while 7 files follow `LTG_SB_cold_open_PXX.png` (C41/C43). Neither series uses version suffixes. The naming convention document (section "Storyboard Assets") shows the spec format as `LTG_SB_ep01_cold_open_seq01_v001.pdf`. The current output is not compliant.

Score: 32/100
- Version suffix absent across all storyboard panel outputs (both naming families).
- Two incompatible naming conventions coexist for the same asset category in the same directory.
Bottom line: any asset management system or downstream tool that parses LTG naming convention will fail to process these files correctly.

---

## ISSUE 4: Face test gate gap — `--char byte` unsupported

**Severity: WARN**

`LTG_TOOL_character_face_test.py` supports `--char luma`, `--char cosmo`, `--char miri` only. Byte is absent. This was documented in the C43 README update as a known gap. Byte is now the central character in two of the three C43 storyboard panels (P07 mid-phase emergence, P09 SPOTTED), and in the SF04 resolution rebuild (C42). The face test gate exists precisely to catch "invisible at sprint scale" problems before full SF generator iteration — omitting Byte from the gate means Byte's face geometry at panel scale has never been validated by the tool designed for that purpose. The C43 README records this as a gap with no assigned resolution cycle.

Score: 0/100 (for the face test gate tool itself)
- `LTG_TOOL_character_face_test.py` --char parameter lists `luma | cosmo | miri` — Byte absent from help text and implementation.
- Two C43 panels featuring Byte at sprint-to-panel scale were produced without face gate validation.
Bottom line: the gate has a hole the size of the second lead character.

---

## ISSUE 5: SF02 generator at 1920×1080 — documented but unresolved multi-cycle issue

**Severity: WARN (persistent)**

`LTG_TOOL_style_frame_02_glitch_storm.py` (current version, C36 Rin Yamamoto) generates at 1920×1080 with a post-thumbnail specular restore pass. This was flagged in `native_resolution_audit_c42.md` as "SIGNIFICANT REFACTOR NEEDED" with a note that C37 documentation explicitly states it must not be updated until a dedicated cycle is assigned. The C41 QA baseline confirms this is still the case. The color fidelity WARNs on `LTG_COLOR_styleframe_glitch_storm.png` (SUNLIT_AMBER LAB ΔE=47.04, UV_PURPLE ΔE=29.02, BYTE_TEAL ΔE=21.79) are directly attributable to the LANCZOS anti-aliasing introduced by downscaling from 1920. The problem is understood, documented, and unactioned across at least two full cycles.

Score: 40/100 (for SF02 generator)
- 1920×1080 source with LANCZOS thumbnail to 1280×720 causes measured LAB ΔE color drift documented at SF02 SUNLIT_AMBER ΔE=47.04.
- SIGNIFICANT REFACTOR flag has been in native_resolution_audit_c42.md for at least 1 cycle with no assigned owner or target cycle.
Bottom line: this generator needs a dedicated fix cycle and an assigned owner — "not changed this cycle" is not a resolution.

---

## ISSUE 6: `LTG_CHAR_luma_motion.py` and `LTG_CHAR_byte_motion.py` — naming convention violation in tools directory

**Severity: WARN**

Two files in `output/tools/` use the `LTG_CHAR_` prefix: `LTG_CHAR_luma_motion.py` and `LTG_CHAR_byte_motion.py`. The canonical tool convention is `LTG_TOOL_*`. The C38 README registered `LTG_TOOL_luma_motion.py` and `LTG_TOOL_byte_motion.py` as the canonical `LTG_TOOL_` versions, with the `LTG_CHAR_` files converted to forwarding stubs. The forwarding stubs remain in the tools directory — they were not retired to `legacy/` and are not marked as retired in the Script Index. This creates ambiguity: a new team member reading `output/tools/` will find two entry points for the same generators.

Score: 55/100
- `LTG_CHAR_luma_motion.py` and `LTG_CHAR_byte_motion.py` in `output/tools/` violate the `LTG_TOOL_*` naming convention for tools — a convention explicitly documented since Cycle 13.
- Forwarding stubs without retirement documentation in the Script Index are undocumented load-bearing files.
Bottom line: if the stubs are permanent bridges, document them as such; if they are transitional, retire them.

---

## ISSUE 7: README Script Index — phantom output path documented for SF04 resolution generator

**Severity: WARN**

`LTG_TOOL_style_frame_04_resolution.py` (C42, Jordan Reed) is documented in the README Script Index as outputting to `output/style_frames/LTG_COLOR_styleframe_sf04.png`. The confirmed actual output path in the generator (line 63) is also `/home/wipkat/team/output/style_frames/LTG_COLOR_styleframe_sf04.png` — a non-standard path. All other style frame outputs use `output/color/style_frames/`. The file does exist at `output/style_frames/LTG_COLOR_styleframe_sf04.png`, but it is outside the canonical color output directory. This is a directory placement deviation that will cause `precritique_qa.py`'s render QA section to miss this asset unless its target list is updated, and will cause any batch tool scanning `output/color/style_frames/` to miss SF04.

Score: 50/100
- SF04 resolution generator writes to `output/style_frames/` instead of `output/color/style_frames/` — inconsistent with all other style frame outputs.
- README documents the non-standard path, meaning the README is accurate but the path itself deviates from the production standard.
Bottom line: either standardize the path or formalize `output/style_frames/` as a second canonical style frame location — the current state is a silent category violation.

---

## ISSUE 8: `LTG_SB_coldopen_panel_XX.png` legacy naming family — no retirement plan documented

**Severity: INFO**

27 cold open panels use `LTG_SB_coldopen_panel_XX.png`. 7 panels (C41/C43) use `LTG_SB_cold_open_PXX.png`. Both families cover the same story sequence. No documentation reconciling the two families exists in `output/production/naming_conventions.md` or the README. The legacy family has no retirement entry and no generator in `output/tools/` that is documented as producing them in the current naming. The generators for `LTG_SB_coldopen_panel_XX.png` series are the older `LTG_TOOL_sb_cold_open_P03.py`, `P06.py`, `P08.py` (C41 vintage), which DO output to the newer `LTG_SB_cold_open_PXX.png` filenames — meaning some of the `LTG_SB_coldopen_panel_XX.png` files may be orphan artifacts from even earlier generators. Provenance unclear.

Score: N/A (documentation finding, not a scoring item)
- 27 storyboard panels with `LTG_SB_coldopen_panel_XX.png` naming have no documented generator in the current Script Index.
Bottom line: document which generators produce the `coldopen_panel_` series or move them to `legacy/`.

---

## Overall Pipeline Grade

**WARN — pipeline is functional but not clean-install reproducible.**

Confirmed FAILs: hardcoded absolute paths (pervasive, worsening), dual-generator output conflict (SF01 discovery). Confirmed WARNs: naming convention violations (no version suffixes on storyboard outputs, split naming families, CHAR_ files in tools dir), face test gate gap for Byte, SF02 1920×1080 deferred refactor, SF04 non-standard output directory. The QA tooling (precritique_qa, ci_suite, stub_linter) is strong — the tools are catching known issues correctly. The problem is that known issues are being seeded into `ci_known_issues.json` rather than fixed, and the hardcoded path problem is being reproduced with every new generator rather than corrected at the template level.

**Priority action items:**
1. Fix hardcoded path pattern at the generator template level — add a `_project_root()` utility to `LTG_TOOL_render_lib.py` and enforce it.
2. Deprecate/retire `LTG_TOOL_style_frame_01_discovery.py` — move to `legacy/`, add retirement note to Script Index.
3. Add Byte support to `LTG_TOOL_character_face_test.py`.
4. Assign owner and target cycle for SF02 native-resolution refactor.
5. Add version suffixes to storyboard panel output filenames.
