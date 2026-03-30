# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: all core assets present.

## Status
**C48 IN PROGRESS. Work cycles: 48. Critique cycles: 18.**
**Next after C48: Critique 19.**

### C48 Resume State
- **Batch 1 ALL KILLED mid-work.** Partial progress on disk (uncommitted). See completion table below.
- **Batch 2 NOT LAUNCHED (4 agents):** Alex, Lee, Priya, Rin — inbox briefs written, ready to launch.
- **Byte position decision:** APPROVED (Priya's rec). Diego briefed. Byte on CRT P19-P20, floats down P21.
- **Reference images:** 168 files in `reference/` across 22 categories. Human added. All HIGH/MEDIUM gaps resolved. 4 LOW gaps remain (`docs/reference_gaps_c48.md`).
- **Reference shopping list updated:** xrite.jpg = ColorChecker, domestic*.{webp,jpg} = scene stats, elderly.png = Miri proportions.
- **Ideabox:** 3 new submissions (Jordan, Morgan, Ryo). Not yet processed.

#### Batch 1 Agent Completion (all killed — work uncommitted)
| Agent | ~Done? | Deliverables on disk | Still needed |
|-------|--------|---------------------|--------------|
| Jordan | ~YES | `LTG_TOOL_sightline_validator.py`, MEMORY updated | Completion report to Alex |
| Morgan | ~YES | pretrained_model_detect→deprecated, CI suite updated | MEMORY update incomplete |
| Ryo | ~YES | `LTG_TOOL_draw_shoulder_arm.py` + demo PNG | MEMORY update incomplete |
| Sam | ~YES | `LTG_TOOL_composite_warmth_score.py`, warmcool_calibrate modified, 2 reports | May need final verification |
| Maya | ~YES | `LTG_TOOL_visual_hook_audit.py` + audit PNG, SF06 modified | Face gate verification incomplete |
| Kai | PARTIAL | `LTG_TOOL_object_detect_qa.py`, precritique warm_pixel started | warm_pixel_lint runner function incomplete |
| Diego | PARTIAL | P14/P15 refinements applied (Lee's 4 items) | P22/P22a NOT created, blank test tool NOT built |
| Hana | PARTIAL | `furniture_vp_spec_c48.md` written, kitchen gen started | Kitchen perspective fixes incomplete |

#### On Restart
1. Review uncommitted changes — verify partial work is safe to keep
2. Re-launch Kai, Diego, Hana to finish incomplete tasks
3. Launch batch 2 (Alex, Lee, Priya, Rin)
4. Process 3 ideabox submissions
5. Commit all completed work
6. Update README.md

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

## Pitch Package Status — POST CYCLE 47

### Style Frames
- **SF01 Discovery: v007 C47** (Jordan). Sight-line fix — angular error 20.7°→2.2° PASS.
- SF02 Glitch Storm: v008 C43. SF03 Other Side: v005.
- SF04 Resolution: C45. CORRUPT_AMBER fringe spec C46.
- SF05 COVETOUS: v3.0.0 C43. SF05 "The Passing": C44. SF06 "The Hand-Off": C44.
- **GL Showcase: v1.0.0 NEW C47** (Rin). Byte+Glitch in full GL void. Critique #1 addressed.

### Logo — v003 C44 (Sam). Fonts installed, rendered.

### Characters
- **Luma: expr v014 C47** (Maya). Shoulder involvement added.
- Byte: expr v007 C41.
- **Cosmo: expr v008 C47, turnaround v003 C47** (Maya). Visual hook: amplified cowlick + bridge tape.
- **Miri: expr v007 C47** (Maya). Shoulder involvement. **Elderly proportion reference tool NEW C47.**
- Glitch: expr v003.
- **Lineup: v011 C47** (Maya). Cosmo hook propagated.

### Environments
- Kitchen: v007 C44. Tech Den: v007 C45.
- Classroom: v004 C46. School Hallway: v005 C46.
- Living Room: v003 C45. Glitch Layer: v003. Other Side: C41.
- **Millbrook Street: v003 C47** (Hana). Value floor fixed, warm/cool 21.0 PASS. 3-cycle critique resolved.
- Luma Study Interior: C42.

### Storyboards
- Panels: P03–P11, **P13 NEW C47**, P14–P21, P23, P24 + EP05 COVETOUS.
- **P13 NEW C47** (Diego): standalone panel — mirror composition, trust/doubt eyes. Critique #4 addressed.
- **P18 REBUILT C47** (Diego): 3-tier visual time arc — blank test PASS. Critique #5 addressed.
- **P20 NEW C47** (Diego): MED WIDE two-shot, names exchanged, notebook continuity.
- **P21 NEW C47** (Diego): WIDE HIGH ANGLE Dutch tilt, 7 monitors blazing, HOT_MAGENTA border.
- Cold open gap log: 32 beats, **12 gaps remaining** (was 14). P22/P22a next.

### Story
- Story Bible: v005 C45. Confirmed current C46.
- **Staging decision register NEW C47** (Priya). All decisions C34-C47 indexed.
- **Doc governance tracker NEW C47** (Priya). 8 HIGH/MEDIUM staleness flags.
- **Character export manifest updated C47** (Priya). Was frozen C24.
- **Pitch delivery manifest updated C47** (Priya). Was frozen C26.

### Motion
- Luma v002, Byte v002, Cosmo v001, **Miri v003 C47** (Ryo — full rework, 44/100→TBD), Glitch v001.
- **precritique_qa v2.15.0 C47** (Lee). Section 12 depth_temp_lint integrated.

## QA Baseline
**precritique_qa v2.15.0 C47.** Section 12 depth_temp_lint integrated.
- **warm-pixel-percentage metric NEW C47** (Sam): replaces hue-split as primary REAL_INTERIOR gate. 31/31 assets PASS, 7/7 reference photos PASS. 24-point gap between RW floor (35%) and GL ceiling (15%).
- **render_qa v2.1.0 C47** (Kai): warm_pixel_pct integrated as primary REAL_INTERIOR gate, overrides hue-split on disagreement.
- **Depth temp lint Section 12**: Lineup PASS (sep=28.8), SF06 WARN, SF02 WARN, SF04/SF05 FAIL (false positives — band position mismatch). Per-asset band override config proposed (ideabox actioned).
- **UV_PURPLE range confirmed**: h° 255°–325° (Rin C46). No change needed.
- **CRT glow profiles**: sigma_frac=0.1165, FWHM 27.4% diagonal, CCT 13070K (Rin C46).
- **Scanline pitch profiles NEW C47** (Rin): phosphor refs mean 25.8px, main CRT refs mean 41.7px.
- **CI suite v1.7.0 C47** (Morgan): Check 10 ext_model_check + --auto-seed --dry-run.
- **color_verify v3.0.0 C47** (Jordan): CORRUPT_AMBER detection mode added.
- **CORRECTION**: Pretrained torchvision models ARE allowed. Use them for object detection QA on output frames (bounding box, class label, probability). Kai's pretrained_model_detect tool and Morgan's Check 10 were built on a misunderstanding — repurpose or remove in C48.

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

## C47 Key Decisions & Deliverables
- **SF01 v007** (Jordan): sight-line fixed — angular error 20.7°→2.2°, 0.9px miss PASS.
- **GL Showcase style frame** (Rin): Byte+Glitch in full GL void, zero warm light. Critique #1 addressed.
- **Cosmo v008 + turnaround v003** (Maya): visual hook — amplified cowlick + bridge tape. Critique #8 addressed.
- **Shoulder involvement** (Maya): added to Luma v014, Cosmo v008, Miri v007. Critique #3 addressed.
- **Miri motion v003** (Ryo): full rework — figure scale +45%, weight distribution, shoulder-hip counterpose. Critique #7 addressed.
- **P13 standalone + P18 rebuilt + P20/P21 new** (Diego): 19 standalone panels total. Critiques #4/#5 addressed.
- **warm-pixel-percentage metric** (Sam): 31/31 PASS, 24-point gap. Replaces hue-split.
- **render_qa v2.1.0** (Kai): warm_pixel_pct integrated as primary gate.
- **precritique_qa v2.15.0** (Lee): Section 12 depth_temp_lint. SF04/SF05 false positives flagged.
- **Millbrook Street v003** (Hana): value floor fixed after 3 cycles. Critique #9 addressed.
- **CI suite v1.7.0** (Morgan): Check 10 ext_model_check + --dry-run mode.
- **color_verify v3.0.0** (Jordan): CORRUPT_AMBER detection mode.
- **Perspective guidelines** (Alex): new doc at `docs/perspective-rules.md`. Critique #2 addressed.
- **Shoulder rule** (Alex): added to `docs/image-rules.md`. Critique #3 formalized.
- **Staging decision register** (Priya): all decisions C34-C47 indexed. Critique #6 partially addressed.
- **Doc governance tracker + manifest updates** (Priya): export manifest C24→C47, delivery manifest C26→C47. Critique #6 addressed.
- **Doc governance audit tool** (Morgan): 43 stale docs flagged.
- **Batch path migration tool** (Hana): 79 files scanned, 85 auto-migratable.
- **Scanline pitch extraction** (Rin): phosphor + CRT ref profiles extracted.
- **Pretrained model detect** (Kai): 8-check scanner, --pre-commit flag.
- **Elderly proportion reference tool** (Maya): two-panel comparison (realistic 6.2h vs stylized 3.2h).
- **Prop continuity tracker** (Diego): 5 props tracked across all cold open panels.
- **Shoulder mechanics reference** (Lee): documented for all human characters.
- **12 ideabox ideas actioned** (all submitted).
- **Byte briefing position URGENT** (Priya → Alex): Byte stays on CRT through P19-P20, floats to Luma's level P21. Decision needed — blocks P20 narrative.

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

## Open Items for C48
1. **Lee**: per-asset depth_temp_lint band override config (ideabox actioned C47 — Alex + Lee both proposed)
2. **Kai**: precritique_qa Section 13 warm-pixel-percentage standalone section (ideabox actioned C47)
3. **Sam**: composite warmth score (ideabox actioned C47)
4. **Morgan**: CI Check 11 doc_staleness (ideabox actioned C47 — Morgan + Priya both proposed)
5. **Hana**: per-room furniture VP spec document (ideabox actioned C47) + perspective fixes per `docs/perspective-rules.md`
6. **Jordan**: sight-line auto-validator in precritique_qa (ideabox actioned C47)
7. **Maya**: visual hook audit tool for thumbnail-size readability (ideabox actioned C47) + SF06 shoulder displacement (deferred from C47)
8. **Ryo**: shared `draw_shoulder_arm()` helper across all character generators (ideabox actioned C47)
9. **Diego**: P22/P22a panels + visual blank test checklist tool (ideabox actioned C47)
10. **Rin**: register GL Showcase in precritique_qa GLITCH_LAYER_PNGS (ideabox actioned C47)
11. **Priya**: cold open gap log update post-C47 panels + Byte briefing position decision (urgent — blocks P20)
12. **Kai**: photorealistic face references for calibration (carried from C46/C47)
13. **Hana**: run batch path migration tool --apply on remaining hardcoded paths
14. **Kai/Morgan**: REMOVE pretrained_model_detect tool + CI Check 10 (built on misunderstanding). Pretrained weights ARE allowed.
15. **Kai**: BUILD object detection QA tool using torchvision pretrained models — detect objects in output frames, validate bounding boxes match intended subjects, report class labels + probabilities. High-value QA infrastructure.

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

## Shared Library (updated C47)
`LTG_TOOL_ci_suite.py` — **v1.7.0 C47** (Morgan). Check 10 ext_model_check + --auto-seed --dry-run.
`LTG_TOOL_precritique_qa.py` — **v2.15.0 C47** (Lee). Section 12 depth_temp_lint integrated.
`LTG_TOOL_render_qa.py` — **v2.1.0 C47** (Kai). warm_pixel_pct primary gate for REAL_INTERIOR.
`LTG_TOOL_color_verify.py` — **v3.0.0 C47** (Jordan). CORRUPT_AMBER detection mode.
`LTG_TOOL_warm_pixel_metric.py` — **NEW C47** (Sam). Warm-pixel-percentage metric.
`LTG_TOOL_styleframe_discovery.py` — **v007 C47** (Jordan). Sight-line vector fix.
`LTG_TOOL_styleframe_glitch_layer_showcase.py` — **v1.0.0 NEW C47** (Rin). GL Showcase frame.
`LTG_TOOL_scanline_pitch_extract.py` — **v1.0.0 NEW C47** (Rin). Autocorrelation scanline pitch.
`LTG_TOOL_miri_motion_v002.py` — **v003 content C47** (Ryo). Full rework.
`LTG_TOOL_cosmo_expression_sheet.py` — **v008 C47** (Maya). Visual hook + shoulder.
`LTG_TOOL_cosmo_turnaround.py` — **v003 C47** (Maya). Visual hook propagated.
`LTG_TOOL_luma_expression_sheet.py` — **v014 C47** (Maya). Shoulder involvement.
`LTG_TOOL_grandma_miri_expression_sheet.py` — **v007 C47** (Maya). Shoulder involvement.
`LTG_TOOL_character_lineup.py` — **v011 C47** (Maya). Cosmo hook propagated.
`LTG_TOOL_elderly_proportion_reference.py` — **v1.0.0 NEW C47** (Maya).
`LTG_TOOL_bg_millbrook_main_street.py` — **v003 C47** (Hana). Value floor fixed.
`LTG_TOOL_batch_path_migrate.py` — **NEW C47** (Hana). 79 files, 85 auto-migratable.
`LTG_TOOL_sb_cold_open_P13.py` — **NEW C47** (Diego). P13 standalone.
`LTG_TOOL_sb_cold_open_P18.py` — **REBUILT C47** (Diego). 3-tier visual time arc.
`LTG_TOOL_sb_cold_open_P20.py` / `P21.py` — **NEW C47** (Diego). Cold open continuation.
`LTG_TOOL_prop_continuity_tracker.py` — **NEW C47** (Diego). 5 props tracked.
`LTG_TOOL_pretrained_model_detect.py` — **v1.0.0 NEW C47** (Kai). 8 checks.
`LTG_TOOL_doc_governance_audit.py` — **v1.0.0 NEW C47** (Morgan). 161 files scanned.

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
- C47 DONE. Next: C48 work cycle (1 more before Critique 19).
