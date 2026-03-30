# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: all core assets present.

## Status
**Cycle 46 complete. Critique 18 complete. Work cycles: 46. Critique cycles: 18.**
**Next: C47 work cycle.**

## Active Team (12 slots)

| Member | Role | Reports To |
|--------|------|-----------|
| Alex Chen | Art Director | — |
| Maya Santos | Character Designer | Alex Chen |
| Sam Kowalski | Color & Style Artist | Alex Chen |
| Kai Nakamura | Tech Art Engineer | Alex Chen |
| Rin Yamamoto | Visual Stylization Artist | Alex Chen |
| Jordan Reed | Style Frame Art Specialist | Alex Chen |
| Lee Tanaka | Character Staging & Visual Acting Specialist | Alex Chen |
| Morgan Walsh | Pipeline Automation Specialist | Alex Chen |
| Diego Vargas | Storyboard Artist | Alex Chen |
| Priya Shah | Story & Script Developer | Alex Chen |
| Hana Okonkwo | Environment & Background Artist | Alex Chen |
| Ryo Hasegawa | Motion & Animation Concept Artist | Alex Chen |

**Agent scheduling:** Max 8 simultaneous. Launch next agent immediately when a slot opens. NEVER exceed 8.

## Image Output Rule (MANDATORY)
**Hard limit: ≤ 1280px in both dimensions.** Native canvas 1280×720. NEVER use `.thumbnail()` — causes LAB drift up to 47°.

## Critique Format
Score (0–100) → bullet issues (≤2 lines each) → single Bottom line. ≤15 lines per asset.

## Critics Panel (20 total)
- 15 industry professionals + 5 audience (Zoe Park age 11, Marcus Okafor parent, Jayden Torres age 13, Eleanor Whitfield grandparent, Taraji Coleman educator)
- **Rotate each cycle. Min 1 audience critic per critique cycle.**
- C16 critics: Daisuke Kobayashi, Priya Nair, Sven Halvorsen, Chiara Ferrara, Jayden Torres
- C17 critics: Jonas Feld, Amara Diallo, Leila Asgari, Petra Volkov, Marcus Webb, Eleanor Whitfield
- **C18 (done)**: Takeshi Mori, Ingrid Solberg, Reinhardt Böhm, Chiara Ferrara, Zoe Park (audience)
- **C19 candidates**: rotate away from C17/C18. Consider: Daisuke, Priya Nair, Sven, Marcus Webb + audience (Marcus Okafor, Jayden Torres, Taraji Coleman)

## Pitch Package Status — POST CYCLE 46

### Style Frames
- SF01 Discovery: v006. SF02 Glitch Storm: v008 C43. SF03 Other Side: v005.
- **SF04 Resolution**: C45 (Jordan). CORRUPT_AMBER fringe spec doc **NEW C46** (Jordan).
- SF05 COVETOUS: v3.0.0 C43. SF05 "The Passing": C44. SF06 "The Hand-Off": C44.

### Logo — v003 C44 (Sam). Fonts installed, rendered.

### Characters
- Luma: expr v013 C41, turnaround v004, color model v002. **3.2 heads tall** (Maya C46 correction).
- Byte: expr v007 C41. Cosmo: expr v007 C38.
- Miri: expr v006 C44. Motion v002 C45. **Elderly proportion reference gap = HIGH** (Maya C46).
- Glitch: expr v003. Motion v001 C44.
- Lineup: v010 C45.

### Environments
- Kitchen: v007 C44. Tech Den: v007 C45 (path migrated).
- **Classroom: v004 C46** (Hana). Hardcoded path migrated.
- **School Hallway: v005 C46** (Hana). Hardcoded path migrated.
- Living Room: v003 C45. Glitch Layer: v003. Other Side: C41.
- Millbrook Street: v002. Luma Study Interior: C42.

### Storyboards
- Panels: P03–P11, P14–P19, P23, P24 + EP05 COVETOUS.
- **P18 NEW C46** (Diego): CU notebook doodles — Luma processing THE NOTICING.
- **P19 NEW C46** (Diego): MED Byte "preferred term is Glitchkin" — comedy beat.
- **Cold open gap log NEW C46** (Priya): 32 beats, 14 gaps remaining. P20/P21 next.

### Story
- Story Bible: v005 C45 (Priya). Confirmed current C46.
- Relationship frame brief: C44. Quiet Frame Spec: C45.

### Motion
- Luma v002, Byte v002, Cosmo v001, Miri v002, Glitch v001.
- precritique_qa v2.14.1 C45. Dark-sheet annotation_occupancy fix (Ryo C46).

## QA Baseline
**precritique_qa v2.14.1.** Full re-run still needed.
- **warm/cool threshold concern**: Sam's calibration tool shows 6/7 real interior photos fall below REAL_INTERIOR 12.0 (median 2.30). Metric may need revision — warm-pixel-percentage proposed as complement/replacement.
- **UV_PURPLE range confirmed**: h° 255°–325° validated by Rin C46 survey. No change needed.
- **CRT glow profiles extracted**: Rin C46 — sigma_frac=0.1165, FWHM 27.4% canvas diagonal, CCT 13070K.
- **Face test gate**: Kai C46 calibration tool built. No threshold changes recommended (deviations = intentional cartoon stylization).
- **Depth temp lint v1.0.0** (Lee C46): Lineup WARN (sep=9.1, correct direction). Precritique integration proposed.

## C45 Key Decisions & Deliverables
- **Depth Temperature Rule** codified in `docs/image-rules.md` (Lee). Warm=FG, cool=BG. Applies to Real World / mixed-space; Glitch Layer exempt.
- **UV_PURPLE linter v1.1.0** (Rin) — GLITCH_DARK_SCENE subtype; COVETOUS FAILs resolved (both PASS).
- **Lineup v010** (Maya) — dual-warmth tier depth bands (Option C). Face gate PASS.
- **Miri motion spec v002** (Ryo) — WARMTH BURST / FOND SETTLE added. 6 motion sheets total.
- **P16/P17 cold open panels** (Diego). P16: ECU floor/eye. P17: still beat, chip falls.
- **Story Bible v005** (Priya) — FLAG 05 closed, SF05/SF06 incorporated.
- **Pilot cold open beat outline v001** (Priya) — gap analysis, P18/P19 flagged next.
- **CI suite v1.5.0** (Morgan) — known_issues suppression on dual_output + thumbnail checks. 244 entries seeded. OVERALL WARN (exit 0).
- **26 legacy storyboard PNGs** moved to `panels/legacy/` (Morgan).
- **char_spec_lint v1.3.0** (Kai) — filename fix for all 4 canonical character generators (no-version-suffix).
- **Living Room v003** (Hana) — CRT centered, warm-left/cool-right staging, aligns to SF06.
- **Tech Den v007** (Hana) — hardcoded path migrated to `output_dir()`.
- **SF04 updated** (Jordan) — lamp halo +31%, CRT doorway CORRUPT_AMBER fringe. render_qa warm/cool 13.2 PASS.
- **Color script analysis** (Sam) — 6-frame warm/cool arc confirmed coherent.
- **Reference shopping list** created — `docs/reference_shopping_list.md`. Sam responded; 11 remaining in C46.
- **Alex dispatched C46 briefs** to all 11 members. Note: Rin's GLITCH_DARK_SCENE brief was already done — clarification sent.

## C46 Key Decisions & Deliverables
- **P18 + P19 storyboard panels** (Diego). Cold open now through P19. P20/P21 next.
- **Cold open gap log** (Priya). 32 beats mapped, 14 gaps remaining.
- **depth_temp_lint.py v1.0.0** (Lee). Lineup WARN sep=9.1 (correct direction).
- **warmcool_scene_calibrate.py** (Sam). REAL_INTERIOR 12.0 may need revision — real photos median 2.30.
- **UV_PURPLE hue survey** (Rin). h° 255°–325° confirmed. No linter change.
- **glow_profile_extract.py v1.0.0** (Rin). 17 CRT refs processed. Recommended sigma_frac=0.1165.
- **CI suite v1.6.0** (Morgan). `--auto-seed` flag for new FAIL auto-seeding.
- **Classroom v004 + School Hallway v005** (Hana). Hardcoded paths migrated.
- **CORRUPT_AMBER fringe spec** (Jordan). Formal spec at `output/production/corrupt_amber_fringe_spec.md`.
- **face_metric_calibrate.py** (Kai). 52 faces detected, no threshold changes recommended.
- **Maya**: Luma 3.2-head correction, elderly Miri reference gap HIGH, reference response delivered.
- **11 ideabox ideas actioned** (all submitted).
- **Lee carry-forward**: P1 SF06 staging review + P2 Byte P14/P15 staging check.

## Critique 18 Results
**Critics:** Takeshi Mori, Ingrid Solberg, Reinhardt Böhm, Chiara Ferrara, Zoe Park (audience)

### Cross-Critic Top Issues (action for C47)
1. **No Glitch Layer in pitch sequence** (Zoe). The show's USP is invisible — need GL showcase panel/frame.
2. **Systemic perspective: furniture in flat elevation** (Chiara). All Real World interiors affected. VP detect universal FAIL.
3. **Arms without shoulder involvement** (Takeshi). Persistent since C15 across all human characters.
4. **P13 still needs standalone panel** (Ingrid). Thematic fulcrum missing from storyboard.
5. **P18 fails blank test** (Ingrid). Notebook insert is text-dependent — needs visual timestamps.
6. **23 undocumented decisions / doc governance** (Reinhardt). Character export manifest frozen C24. Production bible untouched C01.
7. **Miri motion v002 = weakest sheet** (Takeshi, 44/100). Poses labeled not performed.
8. **Cosmo needs stronger visual hook** (Zoe). "Anxious kid in glasses" not distinctive enough.
9. **Millbrook Street value floor persists** (Chiara, 55/100). 3 cycles unfixed.
10. **SF01 sight-line still broken** (Ingrid). Persists across critique cycles.

### Scores Summary
| Critic | Focus | Overall/Top Score | Lowest |
|--------|-------|-------------------|--------|
| Takeshi Mori | Pose/performance | P16: 71, Byte ECU: 72 | Miri motion: 44 |
| Ingrid Solberg | Visual narrative | Combined: 76 | Lineup: 70 |
| Reinhardt Böhm | Production systems | Overall: 38 | Naming: 28 |
| Chiara Ferrara | Environments | School Hallway: 74 | GL Frame: 52 |
| Zoe Park (11) | Audience | Overall: 78 | — |

### Positive Signals
- Zoe wants episode 2 (core metric PASS)
- Ingrid: combined score up from 72→76; gap log scored 85
- Chiara: color infrastructure now solid
- Takeshi: Byte COVETOUS barrier pose = best performance in pitch
- Sam's warmcool calibration praised across critics

## Open Items for C47
1. **Sam/Kai**: warm/cool metric revision (warm-pixel-percentage as complement to hue-split)
2. **Lee**: depth_temp_lint precritique_qa Section 12 integration (ideabox actioned)
3. **Morgan**: CI auto-seed `--dry-run` mode (ideabox actioned)
4. **Hana**: batch path migration script for remaining ~20 hardcoded path files (ideabox actioned)
5. **Rin**: scanline pitch extraction tool (ideabox actioned)
6. **Jordan**: CORRUPT_AMBER detection mode in color_verify (ideabox actioned)
7. **Maya**: elderly proportion reference acquisition + comparison overlay (ideabox actioned)
8. **Kai**: photorealistic face references for calibration (ideabox actioned)
9. **Diego**: P20/P21 panels + prop continuity tracker (ideabox actioned)
10. **Priya**: staging decision register (ideabox actioned)
11. **Lee**: SF06 staging review + Byte P14/P15 staging check (carried from C46)
12. **All**: torchvision pretrained model detection for asset QA (Producer ideabox actioned)

## Canonical Palette
- Byte body = GL-01b #00D4E8 BYTE_TEAL (NOT #00F0FF)
- CORRUPT_AMBER = GL-07 #FF8C00
- HOT_MAGENTA = GL-02 #FF2D6B
- UV_PURPLE = #7B2FBE
- CHAR-L-11 = #00F0FF Electric Cyan
- SF03: zero warm light; Classroom: zero Glitch palette
- Byte shape = OVAL (NOT triangles — retired C8)
- Cosmo glasses = 7° tilt ±2°
- CHAR-M-11 slipper = #C4907A
- CHAR-C-02 = #B89A78 Cosmo Skin Shadow
- CHAR-C-03 = #EED4B0 Cosmo Skin Highlight
- Cosmo cardigan RW-08 #A89BBF Dusty Lavender = COOL (intentional)
- Miri hair accessory = **wooden hairpins** RGB(92,58,32) — NOT chopsticks (FLAG 05 CLOSED C44)

## Key Output Locations
- Style Frames: `output/color/style_frames/`
- Characters: `output/characters/main/`, motion: `output/characters/motion/`
- Environments: `output/backgrounds/environments/`
- Storyboards: `output/storyboards/`
- Story/Script: `output/production/story/`
- Tools: `output/tools/`, deprecated: `output/tools/deprecated/`
- Master Palette: `output/color/palettes/master_palette.md`
- Pitch Package Index: `output/production/pitch_package_index.md`
- Fonts: `assets/fonts/` (Nunito-Bold.ttf + SpaceGrotesk-Bold.ttf — install needed)

## Pipeline Standards
- Open source only: Python PIL + numpy, OpenCV (cv2), PyTorch (authorized C39)
- cv2 default is BGR — convert to RGB on load.
- ΔE color distance threshold = 5.0 (LAB perceptual)
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`
- output/production/ files EXEMPT from LTG naming
- After img.paste(): always refresh draw = ImageDraw.Draw(img)
- show_guides=False for all pitch exports
- Python 3.8 compat: `from __future__ import annotations`
- REAL_INTERIOR warm/cool threshold = 12.0
- **NEVER use `.thumbnail()` in generators** — native 1280×720 canvas only
- Paths: use `LTG_TOOL_project_paths.project_root()` — never hardcode `/home/wipkat/team`

## Shared Library (updated C46)
`LTG_TOOL_ci_suite.py` — **v1.6.0 C46** (Morgan). `--auto-seed` flag for new FAIL auto-seeding.
`LTG_TOOL_depth_temp_lint.py` — **v1.0.0 NEW C46** (Lee). Depth Temperature Grammar Linter.
`LTG_TOOL_warmcool_scene_calibrate.py` — **NEW C46** (Sam). Reference photo warm/cool threshold validation.
`LTG_TOOL_glow_profile_extract.py` — **v1.0.0 NEW C46** (Rin). CRT phosphor glow Gaussian fit.
`LTG_TOOL_face_metric_calibrate.py` — **NEW C46** (Kai). Face test gate calibration from anatomy refs.
`LTG_TOOL_uv_hue_survey_c46.py` — **NEW C46** (Rin). UV_PURPLE hue-family range survey tool.
`LTG_TOOL_sb_cold_open_P18.py` / `P19.py` — **NEW C46** (Diego). P18: notebook doodles; P19: Byte dialogue.
`LTG_TOOL_bg_classroom.py` — **v004 C46** (Hana). Hardcoded path migrated.
`LTG_TOOL_bg_school_hallway.py` — **v005 C46** (Hana). Hardcoded path migrated.
`corrupt_amber_fringe_spec.md` — **NEW C46** (Jordan). Formal CORRUPT_AMBER fringe band spec.
`cold_open_gap_log.md` — **NEW C46** (Priya). Beat-to-panel mapping, 14 gaps remaining.

## Shared Library (historical C44)
`LTG_TOOL_character_face_test.py` — **C44** (Kai). `--char byte` live. Pixel-grid eyes, FG-B01/B02/B03.
`LTG_TOOL_char_spec_lint.py` — **v1.2.0 C44** (Kai). Data-driven M004 via `char_spec_token_config.json`.
`char_spec_token_config.json` — **NEW C44** (Kai). Token lists for M004+ — JSON-editable.
`LTG_TOOL_uv_purple_linter.py` — **v1.0.0 NEW C44** (Rin). UV_PURPLE dominance + warm contamination checks.
`LTG_TOOL_world_type_infer.py` — **v1.2.0 C44** (Rin). covetous_glitch/sf_covetous patterns added.
`LTG_TOOL_ci_suite.py` — **v1.4.0 C44** (Morgan). Check 7 hardcoded-path, Check 8 thumbnail-lint, Check 9 motion-coverage.
`LTG_TOOL_glitch_motion.py` — **v001 NEW C44** (Ryo). 4-panel Glitch motion spec.
`LTG_TOOL_style_frame_05_relationship.py` — **NEW C44** (Jordan). SF05 "The Passing" kitchen pre-dawn.
`LTG_TOOL_sf_miri_luma_handoff.py` — **NEW C44** (Maya). SF06 "The Hand-Off" living room.
`LTG_TOOL_logo_asymmetric.py` — **v003 C44** (Sam). Nunito Bold + Space Grotesk Bold font loaders.
`LTG_TOOL_sb_caption_retrofit.py` — **NEW C44** (Diego). 3-tier caption bar retrofit.
`LTG_TOOL_bg_grandma_kitchen.py` — **v007 C44** (Hana). line_weight FAIL fixed.
`LTG_TOOL_character_lineup.py` — **v009 C44** (Maya). Wooden hairpin atomic update.
`LTG_TOOL_sb_cold_open_P14.py` / `P15.py` — **NEW C44** (Diego). P14: Byte ricochet; P15: Luma floor.

## Shared Library (historical C43)
`LTG_TOOL_project_paths.py` — v1.0.0 C43. `project_root()` anchor + `--audit` CLI.
`vp_spec_config.json` — v1.0.0 C43. 11 ENV VP specs.
`LTG_TOOL_sobel_vp_detect.py` — v1.1.0 C43. `--vp-config` batch mode.
`LTG_TOOL_ci_suite.py` — v1.3.0 C43. Check 6 dual-output detection.
`LTG_TOOL_precritique_qa.py` — v2.12.0 C43. Glitch motion added (Ryo).
`LTG_TOOL_miri_motion.py` — v001 C43. 4-beat Miri vocabulary.
`LTG_TOOL_sf_covetous_glitch_c43.py` — v3.0.0 C43. COVETOUS with Luma face.
`LTG_TOOL_bg_classroom.py` — v003 C43. Pixel font chalkboard.
`LTG_TOOL_bg_school_hallway.py` — v004 C43. MILLBROOK MIDDLE SCHOOL seal.
`LTG_TOOL_style_frame_02_glitch_storm.py` — C43 native rewrite. 1280×720.

## Agent Prompt Design
Do NOT duplicate inbox content in agent prompts. Prompts = role context + startup sequence only.

## Producer Responsibilities
- Ideabox: action → actioned/, reject → rejected/ after each cycle.
- README.md: update after every work and critique cycle.
- Slot filling: launch next agent immediately on completion. Never exceed 8 simultaneous.
- C46 + Critique 18 DONE. Next: C47 work cycle.
