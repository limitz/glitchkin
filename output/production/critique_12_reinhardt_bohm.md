# Production Systems Audit — "Luma & the Glitchkin"
## Critic: Reinhardt Böhm — Production Design Systems Enforcer

**Audit Date:** 2026-03-29
**Cycle:** 27
**Method:** Reproducibility test — I attempted to produce and verify assets using only the available specification documents, then cross-referenced output against documentation.
**Scope:** Style guide completeness, naming convention compliance, generator reproducibility (3 selected), pitch package index currency, tools README accuracy.

---

## Audit Summary

| System | Rating | Violations Found |
|---|---|---|
| Style Guide Completeness | WARN | 6 undocumented decisions |
| Naming Convention Compliance | FAIL | 34+ non-compliant files active in output |
| Generator Reproducibility | WARN | 2 issues across 3 generators |
| Pitch Package Index Currency | WARN | Multiple unlisted files; 2 mismatch issues |
| Tools README Currency | FAIL | 22+ registered tools with wrong category prefix; 15+ unregistered tools |

Overall production system rating: **FAIL**

The documentation is substantially stronger than most productions I audit at this stage. Several areas are genuinely well-specified. But there are systemic failures that would stop a new engineer cold, and the tools registry has become dangerously detached from the actual state of the tools directory. These are not aesthetic opinions. These are specification failures. They are documented below.

---

## Section 1 — Style Guide Completeness

**Documents reviewed:**
- `output/style_guide.md`
- `output/production/character_sheet_standards_v001.md`
- `output/production/naming_conventions.md`
- `output/production/char_refinement_directive_c17.md`
- `output/color/palettes/master_palette.md` (referenced but not read in full)
- `output/production/production_bible.md`

**Rating: WARN**

The style guide has genuine strengths. The two-world color logic is clearly specified. The Corrupted Amber rule is documented in enough detail that a new artist could apply it correctly without asking a question. The skin tone system under multiple lighting conditions is paint-ready. The character sheet standards document is among the best I have seen for a production at this stage — label rules, HEAD_R values, line weight tiers, and construction guide policy are all precisely stated.

However, I found **6 undocumented decisions** that a new artist would have to resolve from their own judgment:

**Undocumented Decision 1:** The style guide (Section 3) states children are "3.5–4 heads tall." The character sheet standards (Section 3) states Luma is "4.5–5.0 HU" and Cosmo is "4.5–5.0 HU." These two documents give different answers to the same question. A new artist looking at both documents would not know which is authoritative. The style guide is v1.0 (not versioned after initial delivery); the character sheet standards are v001 from Cycle 22. Neither document references the other or states which supersedes which. This is **Conflict 1 between documents** — a new artist cannot resolve it without asking.

**Undocumented Decision 2:** The style guide states eyebrows are "thick, graphic shapes — not hair-like." The character sheet standards define brow weight precisely as "4px at 2× render → ~2px output (interior structure weight)." But neither document specifies eyebrow shape — are they tapered? Parallel? Squared ends? Arched? A new artist drawing a character from scratch would make this decision from taste. I found no shape specification for brows anywhere in the documentation reviewed.

**Undocumented Decision 3:** The style guide states mouths are "simple curved lines" that "can stretch and deform freely." The character sheet standards list expression labels and HEAD_R values but do not define mouth shape vocabulary. What distinguishes a GRUMPY closed-mouth from a FRUSTRATED closed-mouth? What is the canonical shape difference between CURIOUS and SEARCHING? No answer exists in any reviewed document. A new artist would interpolate from the existing expression sheets — which are not specifications, they are outputs.

**Undocumented Decision 4:** The Corrupted Amber rule defines the threshold as "Electric Cyan + Byte Teal together cover more than 35% of the visible background around Byte." The phrase "visible background around Byte" is undefined. Does "around" mean a bounding box? A fixed-radius sample zone? The entire visible frame? At production scale, when a new compositor applies this rule to a scene, two people following this specification exactly will get different answers. The threshold is specified; the measurement method is not.

**Undocumented Decision 5:** The style guide defines the skin tone system for Luma, Cosmo, and Grandma Miri under multiple lighting conditions. There is no skin tone specification for Cosmo under cyan-dominant lighting and no skin tone specification for Grandma Miri under warm lamp interior conditions. Both characters appear in scenes where these values would be needed. A new colorist would invent these values.

**Undocumented Decision 6:** The style guide states "Clothing folds are minimal — 2–3 key fold lines maximum." It does not specify where those fold lines go. Which costume surfaces fold? Under what conditions? For which characters? "2–3 fold lines" on a winter jacket is a different decision than on Luma's hoodie. A new artist would make this from taste.

---

## Section 2 — Naming Convention Compliance

**Rating: FAIL**

The naming convention document is well-written and the rationale is clear. It includes an explicit exemption for `output/production/` files. I applied the documented standard to all files outside that exemption.

I found **34 non-compliant files** currently active (not in legacy/) outside `output/production/`:

### 2.1 — Generators with Wrong Category Prefix (Active in `output/tools/`)

The naming convention states scripts in `output/tools/` must follow the LTG format. The registered convention for scripts is `LTG_TOOL_*`. The following files in `output/tools/` use incorrect category prefixes:

**LTG_CHAR_ prefixed generators (should be LTG_TOOL_):**
1. `output/tools/LTG_CHAR_luma_expression_sheet_v002.py`
2. `output/tools/LTG_CHAR_luma_expression_sheet_v003.py`
3. `output/tools/LTG_CHAR_luma_expression_sheet_v004.py`
4. `output/tools/LTG_CHAR_luma_expression_sheet_v005.py`
5. `output/tools/LTG_CHAR_luma_expression_sheet_v006.py`
6. `output/tools/LTG_CHAR_byte_expression_sheet_v004.py`
7. `output/tools/LTG_CHAR_cosmo_expression_sheet_v004.py`
8. `output/tools/LTG_CHAR_glitch_expression_sheet_v001.py`
9. `output/tools/LTG_CHAR_glitch_expression_sheet_v002.py`
10. `output/tools/LTG_CHAR_glitch_turnaround_v001.py`
11. `output/tools/LTG_CHAR_glitch_turnaround_v002.py`
12. `output/tools/LTG_CHAR_glitch_color_model_v001.py`
13. `output/tools/LTG_CHAR_cosmo_turnaround_v002.py`
14. `output/tools/LTG_CHAR_grandma_miri_expression_sheet_v003.py`
15. `output/tools/LTG_CHAR_luma_turnaround_v002.py`

**LTG_COLOR_ prefixed generators (should be LTG_TOOL_):**
16. `output/tools/LTG_COLOR_luma_color_model_v001.py`
17. `output/tools/LTG_COLOR_byte_color_model_v001.py`
18. `output/tools/LTG_COLOR_cosmo_color_model_v001.py`
19. `output/tools/LTG_COLOR_styleframe_luma_byte_v001.py`
20. `output/tools/LTG_COLOR_styleframe_luma_byte_v002.py`

**LTG_BRAND_ prefixed generator (should be LTG_TOOL_):**
21. `output/tools/LTG_BRAND_logo_v001.py`

The README notes this renaming was applied to several generators in Cycle 22, but the renaming was not completed. 21 generators in the active tools directory still carry the wrong category prefix.

### 2.2 — Generator Files Placed Outside `output/tools/`

The following `.py` generator files exist outside `output/tools/` and outside `output/production/` (which is exempt). These are pipeline artifacts, not output assets, and have no documented exception:

22. `output/backgrounds/environments/LTG_ENV_grandma_kitchen_v003.py`
23. `output/backgrounds/environments/LTG_ENV_tech_den_v004.py`
24. `output/backgrounds/environments/bg_glitch_layer_encounter.py`
25. `output/characters/main/LTG_CHAR_byte_expression_sheet_v004.py`
26. `output/characters/main/LTG_CHAR_cosmo_expression_sheet_v004.py`
27. `output/characters/main/LTG_CHAR_luma_expression_sheet_v004.py`
28. `output/color/style_frames/LTG_TOOL_style_frame_02_glitch_storm_v005.py`

Files 22–24 and 28 additionally carry naming convention violations (either wrong category prefix for their location, or generator using output-asset category code). File 24 (`bg_glitch_layer_encounter.py`) uses a legacy non-LTG prefix.

### 2.3 — Non-LTG Named Assets (Active, Non-Production, Not in Legacy/)

The following asset files are non-compliant and not in legacy/:

29. `output/characters/main/character_lineup.png`
30. `output/characters/main/luma_expressions.png`
31. `output/characters/main/luma_expression_sheet.png`
32. `output/characters/main/luma_face_closeup.png`
33. `output/characters/main/byte_expressions.png`
34. `output/characters/main/proportion_diagram.png`
35. `output/characters/main/silhouettes/character_silhouettes.png`
36. `output/characters/main/turnarounds/luma_turnaround.png`
37. `output/characters/main/turnarounds/byte_turnaround.png`
38. `output/characters/main/turnarounds/cosmo_turnaround.png`
39. `output/characters/main/turnarounds/miri_turnaround.png`
40. `output/backgrounds/environments/frame01_house_interior.png`
41. `output/backgrounds/environments/glitch_layer_frame.png`
42. `output/backgrounds/environments/bg_glitch_layer_encounter.png`
43. `output/color/style_frames/style_frame_01_rendered.png`
44. `output/color/color_keys/thumbnails/key01_sunny_afternoon.png`
45. `output/color/color_keys/thumbnails/key02_nighttime_glitch.png`
46. `output/color/color_keys/thumbnails/key03_glitch_layer_entry.png`
47. `output/color/color_keys/thumbnails/key04_quiet_moment.png`

The naming convention document acknowledges most of these as legacy-pending-rename and says to wait for reconciliation passes. After 27 cycles, these files remain. The reconciliation pass is not complete. Each one is a violation in the current state of the output directory.

### 2.4 — Test Files in Active Tools Directory

Two test output files exist in `output/tools/` with no LTG prefix and no version number:

48. `output/tools/test_face_lighting_v001.png`
49. `output/tools/test_procedural_draw_v001.png`

These are not production assets and should not be in the tools root. No exception is documented for them.

### 2.5 — Miscellaneous Non-LTG Named Files (Active, Non-Production)

The following files lack LTG naming and are not exempted:

50. `output/style_guide.md` — The style guide itself is not LTG-named. The naming convention gives the example `LTG_PROD_style_guide_v001.md`. This file should be `LTG_PROD_style_guide_v001.md` and should live in `output/production/`. (It currently lives in `output/` root, which is also undocumented.)
51. `output/backgrounds/environments/glitch_layer.md`
52. `output/backgrounds/environments/lumas_house_interior.md`
53. `output/backgrounds/environments/millbrook_main_street.md`
54. `output/backgrounds/environments/millbrook_school.md`

**Total active non-compliant files: 54+**

The naming convention document was written clearly. Compliance has not followed. A new engineer joining the production would encounter dozens of files that do not match the documented standard, with no reliable way to determine which name is canonical when both a legacy and a compliant copy exist.

---

## Section 3 — Generator Reproducibility

**Three generators selected:** `LTG_TOOL_luma_expression_sheet_v003.py`, `LTG_TOOL_bg_tech_den_v004.py`, `LTG_TOOL_colorkey_glitchstorm_gen_v001.py`

**Rating: WARN**

### 3.1 — Color Values as Named Constants

**LTG_TOOL_luma_expression_sheet_v003.py:** All palette colors are named constants at the top of the file. No inline tuples found in the palette section. PASS.

**LTG_TOOL_bg_tech_den_v004.py:** All palette colors are named constants. The file defines approximately 60 named color constants before any drawing code. No inline color tuples visible in the reviewed portion. PASS.

**LTG_TOOL_colorkey_glitchstorm_gen_v001.py:** All palette colors are named constants. The comment block explaining the ENV-06 correction is thorough and traceable. PASS.

All three generators comply with the named-constant requirement.

### 3.2 — File Paths: Hardcoded vs. Relative

**LTG_TOOL_luma_expression_sheet_v003.py:** Output path is constructed using `os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "characters", "main")` — relative to the script location. This is correct. The script will produce the right output regardless of working directory. PASS.

**LTG_TOOL_bg_tech_den_v004.py:** Output path is hardcoded as `"/home/wipkat/team/output/backgrounds/environments/LTG_ENV_tech_den_v004.png"`. This is a **hardcoded absolute path**. The script will break or produce output in the wrong location on any system that is not `/home/wipkat/team/`. This is a portability and reproducibility violation. **WARN — hardcoded absolute path.**

**LTG_TOOL_colorkey_glitchstorm_gen_v001.py:** `OUTPUT_DIR` is defined as the hardcoded absolute path `"/home/wipkat/team/output/color/color_keys/thumbnails"`. Same problem as tech den. **WARN — hardcoded absolute path.**

This pattern likely applies to many background generators since they share an output path convention. I did not audit all of them, but the two I checked (v004 tech den, colorkey generator) both hardcode paths. The luma expression sheet generator is the only one of the three that uses the correct pattern.

### 3.3 — Output Filename Accuracy

**LTG_TOOL_luma_expression_sheet_v003.py:** Output filename is `LTG_CHAR_luma_expression_sheet_v003.png`. This is the correct output asset name. PASS.

**LTG_TOOL_bg_tech_den_v004.py:** Output filename is `LTG_ENV_tech_den_v004.png`. This matches the expected asset. PASS.

**LTG_TOOL_colorkey_glitchstorm_gen_v001.py:** Output filename is `LTG_COLOR_colorkey_glitchstorm_v001.png`. This matches the expected asset. PASS.

### 3.4 — Seeded RNG / Reproducibility

**LTG_TOOL_luma_expression_sheet_v003.py:** No random elements visible in the reviewed code — character geometry is deterministic. PASS.

**LTG_TOOL_bg_tech_den_v004.py:** Uses `rng = random.Random(42)` — module-level seeded RNG. PASS.

**LTG_TOOL_colorkey_glitchstorm_gen_v001.py:** Uses `random.seed(202612)` called inside the draw function. PASS.

### 3.5 — Import Hygiene

All three generators use only `PIL/Pillow`, `math`, `os`, `random`, and `sys`. No undeclared or unusual dependencies. The tech den and colorkey generators import from standard library only plus Pillow. The luma expression sheet imports Pillow plus standard library. PASS for all three.

**Generator section finding:** The hardcoded absolute path issue is systemic. It is documented in two of the three sampled generators. A new engineer running any background generator on a different machine (or even a different user on the same machine) will get a path error or produce output to the wrong location. This has not been caught or corrected over multiple cycles. The correct pattern exists in `LTG_TOOL_luma_expression_sheet_v003.py` — it is not consistently followed.

---

## Section 4 — Documentation Currency (Pitch Package Index)

**Document:** `output/production/pitch_package_index.md`
**Rating: WARN**

The pitch package index is the most comprehensive asset tracking document I have encountered on a production of this size. The cross-referencing within it is unusually rigorous. However, I found the following gaps and mismatches:

### 4.1 — Files Listed in Index but Not Found at Stated Path

**Violation 1:** The index (Section 1.6, Cycle 25 Additions) lists SF04 generator as `/home/wipkat/team/output/tools/LTG_COLOR_styleframe_luma_byte_v001.py`. This file exists in the tools directory but is named with the `COLOR` category code, not `TOOL`. This is a naming violation (see Section 2 of this report) that the index records without flagging.

**Violation 2:** The index lists SF02 v005 as "PITCH READY" with no open items. The actual generator for SF02 v005 (`LTG_TOOL_style_frame_02_glitch_storm_v005.py` or `LTG_COLOR_styleframe_luma_byte_v002.py` for SF04) exists in `output/color/style_frames/` rather than `output/tools/`. Generator files misplaced outside the tools directory are not tracked in the index.

### 4.2 — Files Existing on Disk Not Listed in the Index

The following files are present in the output directory with no entry in the pitch package index:

- `output/color/style_frames/LTG_COLOR_styleframe_otherside_v004.png` — a v004 version of SF03 exists on disk, not listed in the index at all. The index lists v003 as canonical. Either v004 is an error or it supersedes v003 and the index has not been updated.
- `output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v002.png` — SF04 v002 exists on disk. The index lists only v001 as delivered (Cycle 25). v002 is not mentioned anywhere in the index.
- `output/characters/main/LTG_CHAR_luma_expression_sheet_v005.png` — listed in the index as the current sheet (Cycle 26). The index entry exists. However, `LTG_CHAR_luma_expression_sheet_v006.py` exists in `output/tools/`, implying a v006 output may have been generated. If so, the index is stale by one version.
- `output/characters/main/LTG_CHAR_grandma_miri_expression_sheet_v003.py` exists in tools — this implies a v003 of Miri's expression sheet exists or was generated. The index shows v002 as current. This is an ambiguity: either v003 was never run, or it was run and the output is not indexed.

### 4.3 — Internal Inconsistency in Index

The index header states last update was "Cycle 24." Multiple Cycle 25, 26, and 27 additions appear in the body. The header date is stale. A new reader relying on the header "Cycle 24" to assess currency would believe the document is two cycles behind its actual state.

---

## Section 5 — Pipeline Spec (Tools README)

**Document:** `output/tools/README.md`
**Rating: FAIL**

The README was last updated at Cycle 26 according to its header. I cross-referenced it against the actual contents of `output/tools/`.

### 5.1 — Tools in Directory Not Registered in README

The following tools exist on disk but have **no entry in the README Script Index:**

1. `LTG_CHAR_glitch_expression_sheet_v001.py`
2. `LTG_CHAR_glitch_expression_sheet_v002.py`
3. `LTG_CHAR_glitch_turnaround_v001.py`
4. `LTG_CHAR_glitch_turnaround_v002.py`
5. `LTG_CHAR_glitch_color_model_v001.py`
6. `LTG_CHAR_cosmo_turnaround_v002.py`
7. `LTG_CHAR_grandma_miri_expression_sheet_v003.py`
8. `LTG_CHAR_luma_expression_sheet_v005.py`
9. `LTG_CHAR_luma_expression_sheet_v006.py`
10. `LTG_CHAR_luma_turnaround_v002.py`
11. `LTG_COLOR_luma_color_model_v001.py`
12. `LTG_COLOR_byte_color_model_v001.py`
13. `LTG_COLOR_cosmo_color_model_v001.py`
14. `LTG_COLOR_styleframe_luma_byte_v001.py`
15. `LTG_COLOR_styleframe_luma_byte_v002.py`
16. `LTG_BRAND_logo_v001.py`
17. `LTG_TOOL_character_lineup_v004.py`
18. `LTG_TOOL_character_lineup_v005.py`
19. `LTG_TOOL_luma_classroom_pose_v001.py`
20. `LTG_TOOL_sb_act2_contact_sheet_v006.py`
21. `LTG_TOOL_sb_act1_full_contact_sheet_v001.py`
22. `LTG_TOOL_miri_turnaround_v001.py`
23. `LTG_TOOL_fidelity_check_c24.py`
24. `LTG_TOOL_procedural_draw_v001.py`

That is 24 tools absent from the registry.

### 5.2 — README References Tools Renamed but Still Lists Old Names as Active

The README entry for `LTG_TOOL_luma_expression_sheet_v002.py` states it "Previously misnamed `LTG_CHAR_luma_expression_sheet_v002.py` — renamed in Cycle 22." However, `LTG_CHAR_luma_expression_sheet_v002.py` still exists on disk in `output/tools/`. The rename was not a rename — both files co-exist. Same situation for `LTG_CHAR_luma_expression_sheet_v003.py`, `LTG_CHAR_luma_expression_sheet_v004.py`, `LTG_CHAR_byte_expression_sheet_v004.py`, and `LTG_CHAR_cosmo_expression_sheet_v004.py`. The README describes a state of the repository that does not exist.

### 5.3 — README Pipeline Health Section is 2 Cycles Stale

The "Pipeline Health — C24" section states the audit was performed on 2026-03-29 (Cycle 24). The README header says last updated Cycle 26. The pipeline health section was not updated when the README was updated. A new engineer reading this section would believe the last pipeline audit was 2 cycles ago and that the verified clean-import list reflects the current tool set. It does not — the 24 unregistered tools above were not in scope for that audit.

### 5.4 — README Registration Instructions Not Being Followed

The README contains explicit registration instructions: "When a new script is created, add a row to the Script Index above." 24 scripts were created and not registered. The instruction is present. Compliance is zero for tools created after Cycle 22.

---

## Consolidated Violation List

| # | Location | Violation | Severity |
|---|---|---|---|
| 1 | `style_guide.md` vs `character_sheet_standards_v001.md` | Conflicting head count specification (3.5–4 HU in style guide; 4.5–5.0 HU in standards) | CRITICAL |
| 2 | `style_guide.md` | Eyebrow shape unspecified (weight documented, shape not) | MODERATE |
| 3 | `style_guide.md` + all expression spec docs | Mouth shape vocabulary undefined across expression states | MODERATE |
| 4 | `style_guide.md` | "35% of visible background around Byte" — measurement method undefined | MODERATE |
| 5 | `style_guide.md` | Cosmo skin under cyan lighting: no spec | MODERATE |
| 6 | `style_guide.md` | Grandma Miri skin under warm lamp interior: no spec | MODERATE |
| 7 | `output/tools/` (15 files) | LTG_CHAR_ prefixed generators in tools dir — wrong category code | FAIL |
| 8 | `output/tools/` (5 files) | LTG_COLOR_ prefixed generators in tools dir — wrong category code | FAIL |
| 9 | `output/tools/` (1 file) | LTG_BRAND_ prefixed generator in tools dir — wrong category code | FAIL |
| 10 | `output/` (7 locations) | Generator `.py` files placed outside `output/tools/` | FAIL |
| 11 | `output/` (19 files) | Legacy non-LTG named assets still active, not moved to legacy/, no LTG-compliant copy | FAIL |
| 12 | `output/tools/` | Two test PNG files with no LTG naming, no version | WARN |
| 13 | `output/style_guide.md` | Style guide not LTG-named, stored in output root (not output/production/) | WARN |
| 14 | `output/backgrounds/` (4 files) | Non-LTG named .md spec files outside production/ | WARN |
| 15 | `LTG_TOOL_bg_tech_den_v004.py` | Hardcoded absolute output path | WARN |
| 16 | `LTG_TOOL_colorkey_glitchstorm_gen_v001.py` | Hardcoded absolute output path | WARN |
| 17 | `pitch_package_index.md` | Header states Cycle 24; document contains Cycle 26 additions | WARN |
| 18 | `pitch_package_index.md` | `LTG_COLOR_styleframe_otherside_v004.png` on disk, not indexed | WARN |
| 19 | `pitch_package_index.md` | `LTG_COLOR_styleframe_luma_byte_v002.png` on disk, not indexed | WARN |
| 20 | `pitch_package_index.md` | `LTG_CHAR_grandma_miri_expression_sheet_v003.py` in tools implies v003 output — index shows v002 as current | WARN |
| 21 | `tools/README.md` | 24 tools on disk have no README entry | FAIL |
| 22 | `tools/README.md` | README claims `LTG_CHAR_` files were renamed; old names still present on disk | FAIL |
| 23 | `tools/README.md` | Pipeline Health section is Cycle 24 (2 cycles stale) | WARN |
| 24 | `tools/README.md` | Registration instructions exist but are not followed | SYSTEMIC |

---

## Observations and What Needs Improvement

**On the style guide:** The foundation is strong. The two-world logic, the Corrupted Amber rule, the skin tone system — these are genuinely well-specified. The problems are at the edges where the style guide meets the character sheet standards. Fix the head count conflict first: decide which document is authoritative and add a cross-reference. Then fill the five remaining gaps. A new character artist today would get the head count wrong on Luma or Cosmo with a 50% probability, because both answers are in the documentation.

**On naming compliance:** This production has been aware of its naming compliance debt since at least Cycle 12. The pitch package index tracks "LTG rename outstanding" flags across dozens of assets. It is now Cycle 27 and those flags remain. The issue is not that the standard is unclear — it is excellent. The issue is that each cycle produces new non-compliant files faster than old ones are rectified. The `LTG_CHAR_` and `LTG_COLOR_` generator files in `output/tools/` are a new category of violation that appears to have started in Cycle 24–26 when the Glitch character set was developed. These are not grandfathered legacy files — they are recent work that ignored the established convention.

**On generators:** The hardcoded absolute path pattern is the most serious technical finding. `LTG_TOOL_luma_expression_sheet_v003.py` demonstrates the correct pattern. Use `os.path.dirname(os.path.abspath(__file__))` plus relative path construction. Apply this to every generator that currently hardcodes `/home/wipkat/team/`. This is a one-line fix per file.

**On the pitch package index:** The untracked v004 of SF03 (`LTG_COLOR_styleframe_otherside_v004.png`) and v002 of SF04 (`LTG_COLOR_styleframe_luma_byte_v002.png`) are the most urgent gaps. If a studio contact receives the pitch package and asks "is this the current version," the answer depends on files that are not in the index. The index's purpose is to prevent exactly that ambiguity.

**On the tools README:** 24 unregistered tools is a system breakdown. The README exists. The registration instructions are clear. They are not being followed. From Cycle 23 onward, the registry has fallen behind at a rate of approximately 4–5 tools per cycle. At current trajectory, the registry will represent fewer than half the active tools within 10 cycles. A new engineer trying to understand the pipeline from the README alone would miss every Glitch character generator, both SF04 generators, the character lineup v004 and v005, the procedural draw library, the fidelity check tool, and the miri turnaround generator.

---

## Final Count

**Undocumented design decisions:** 6
**Active naming violations:** 54+
**Generator path hardcoding violations:** 2 of 3 sampled (systemic pattern)
**Pitch package index gaps:** 4 confirmed
**Tools README unregistered scripts:** 24
**Tools README stale claims:** 2 categories

This production is further along than most I audit. The core specifications exist and are of good quality. The maintenance failure is in keeping the registry documents current as the output directory grows. A production system is only as useful as its currency. At current state, the tools README and the pitch package index are both unreliable guides to what actually exists in the project.

---

*Audit completed by Reinhardt Böhm — Production Design Systems Enforcer*
*2026-03-29 — Cycle 27*
