# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: all core assets present.

## Status
**Cycle 45 complete. Critique 17 complete. Work cycles: 45. Critique cycles: 17.**
**C46 = Critique 18 (every 3 cycles — due C46). Run critics after C46 work cycle.**

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
- C15 critics: Takeshi Mori, Ingrid Solberg, Reinhardt Böhm, Zoe Park, Taraji Coleman
- C16 critics: Daisuke Kobayashi, Priya Nair, Sven Halvorsen, Chiara Ferrara, Jayden Torres
- C17 critics: Jonas Feld, Amara Diallo, Leila Asgari, Petra Volkov, Marcus Webb, Eleanor Whitfield
- **C18 candidates (C45)**: Takeshi Mori, Ingrid Solberg, Reinhardt Böhm, Chiara Ferrara + 1 audience not from C16/C17 (Zoe Park, Marcus Okafor, Jayden Torres, Taraji Coleman)

## Pitch Package Status — POST CYCLE 45

### Style Frames
- **SF01 Discovery**: v006
- **SF02 Glitch Storm**: v008 C43 native 1280×720. SUNLIT_AMBER ΔE 1.1 PASS.
- **SF03 Other Side**: v005 (UV_PURPLE ΔE 0.0 C41)
- **SF04 Resolution**: CANONICAL C42, updated C45 (Jordan). Lamp halo radius +31% (α max 35%), CRT doorway CORRUPT_AMBER contamination fringe added. render_qa warm/cool 13.2 PASS.
- **SF05 COVETOUS**: v3.0.0 C43 (Lee). Luma SENSING UNEASE face PASS.
- **SF05 "The Passing"** NEW C44 (Jordan): Kitchen pre-dawn, mug of tea, CRT through doorway. Warm/cool 16.7 PASS. `LTG_TOOL_style_frame_05_relationship.py` / `LTG_COLOR_styleframe_sf05.png`. ⚠️ Naming conflict with COVETOUS SF05 — Alex to confirm numbering scheme.
- **SF06 "The Hand-Off"** NEW C44 (Maya): Living room, Miri (arm extended) + CRT (center) + Luma (forward lean). `LTG_TOOL_sf_miri_luma_handoff.py` / `LTG_COLOR_sf_miri_luma_handoff.png`. Closes C17 most-cited gap. Living Room v003 C45 (Hana) now aligned to this staging.

### Logo
- **LTG_BRAND_logo_asymmetric.py v003 C44** (Sam). Nunito Bold (Luma) + Space Grotesk Bold (Glitchkin). `assets/fonts/` directory created with README + download instructions. **Fonts not yet installed** — run `assets/fonts/README.md` wget commands to activate. Falls back to DejaVu Sans silently if fonts absent.

### Characters
- Luma: expr v013 C41, turnaround v004, color model v002.
- Byte: expr v007 C41. `--char byte` face test **NOW LIVE** (Kai C44).
- Cosmo: expr v007 C38. Motion spec v001 C41.
- Miri: **expr v006 C44** (Maya). **FLAG 05 CLOSED** — wooden hairpins. Story Bible v005 C45 (Priya) fully reflects this. Motion spec **v002 C45** (Ryo): OBSERVING STILL / RECOGNITION / WARMTH BURST / FOND SETTLE.
- Glitch: expr v003. Body primitive diagram C41. **Motion spec v001 NEW C44** (Ryo): PREDATORY STILL / COVETOUS REACH / CORRUPTION SURGE / RETREAT.
- Character lineup: **v010 C45** (Maya). Dual-warmth tier depth bands (Option C): warm amber FG, cool slate BG. Face gate PASS baseline confirmed.

### Environments
- Kitchen: **v007 C44** (Hana). line_weight FAIL resolved (paper_texture + vignette + flatten). Warm/cool 32.9 PASS.
- Tech Den: v006 C41.
- Glitch Layer: v003. UV_PURPLE linter: COVETOUS FAILs (UV_PURPLE_DARK variant → hue-angle fix pending C45), ENV WARNs (~17%).
- Classroom: v003 C43 (pixel font deployed).
- School Hallway: v004 C43 (MILLBROOK MIDDLE SCHOOL).
- Millbrook Street: v002.
- Living Room: **v003 C45** (Hana). CRT centered, warm-left/cool-right staging pass added, aligns to SF06.
- Other Side: C41.
- Luma Study Interior: NEW C42.

### Storyboards
- Cold Open: v003 C39 (night/den canonical).
- Panels: P03–P11, P14–P17, P23, P24 + EP05 COVETOUS. All caption-retrofitted (3-tier hierarchy). P16 C45 (Diego): ECU Luma face/floor, Byte tracking. P17 C45 (Diego): MED still beat, chip falls, depth temp rule applied. Pilot cold open beat outline v001 (Priya C45) — gap analysis complete.
- 26 legacy `LTG_SB_coldopen_panel_XX` PNGs: **MOVED** to `panels/legacy/` (Morgan C45).
- PANEL_MAP: P16/P17 → EXISTS. Next: P18 (notebook doodles), P19 (Byte "preferred term is Glitchkin").

### Story
- Story Bible: **v005 C45** (Priya). FLAG 05 closed throughout; SF05/SF06 incorporated as staging references.
- **Relationship frame brief**: NEW C44 (`output/production/story/LTG_relationship_frame_brief.md`). A1-01 kitchen morning, mug of tea, logline: "The woman who owns this house hands the girl who inherited her eyes a cup of tea, and neither of them mentions the television."
- Quiet Frame Spec: ideabox actioned → Jordan C45.

### Motion
- Luma: v002 C38.
- Byte: v002 C38.
- Cosmo: v001 C41.
- Miri: v001 C43.
- **Glitch: v001 NEW C44** (Ryo). PREDATORY STILL / COVETOUS REACH / CORRUPTION SURGE / RETREAT. CORRUPT_AMBER beat color.
- precritique_qa **v2.14.1 C45** — all 6 motion sheets (Miri v002 added); GLITCH_DARK_SCENE COVETOUS subtype fix.
- annotation_occupancy false WARNs on Byte/Glitch dark sheets: Ryo ideabox actioned → C45.

## QA Baseline
**precritique_qa v2.14.1 C45** (Ryo). All 6 motion sheets. Section 11 UV_PURPLE with GLITCH_DARK_SCENE subtype (Rin C45). Dark-sheet annotation_occupancy fix (Ryo C45 — byte/glitch false WARNs resolved). **Full re-run needed C46.**

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

## Open Items for C46 (Critique 18)
**C46 = Critique 18 — run critics AFTER C46 work cycle**

**C46 work:**
1. **Priya**: story bible v005 already done — check Alex brief for any residuals
2. **Diego**: P18 (notebook doodles) + P19 (Byte "preferred term is Glitchkin")
3. **Ryo**: Glitch motion G004 draw-order fix (HOT_MAG crack before body fill)
4. **Rin**: UV_PURPLE hue-family range review (h° 255°–325° calibration) — see ideabox
5. **Kai**: readme_sync `--draft-entry` flag
6. **Lee/Maya**: `LTG_TOOL_depth_temp_lint.py` (depth grammar linter, integrate precritique_qa)
7. **Morgan**: CI `--auto-seed` flag for new FAIL auto-seeding
8. **Hana**: ENV hardcoded path audit — classroom + school_hallway
9. **Jordan**: CORRUPT_AMBER fringe band spec doc
10. **Sam**: `LTG_TOOL_warmcool_scene_calibrate.py` (once reference photo acquired)
11. **All members**: respond to reference shopping list (`docs/reference_shopping_list.md`) in inbox
12. **Diego/Priya**: cold open scene gap log (persistent beat gap tracking doc)

**Critique 18 (C46):**
- 5 critics: Takeshi Mori, Ingrid Solberg, Reinhardt Böhm, Chiara Ferrara + 1 audience (Zoe Park, Marcus Okafor, Jayden Torres, or Taraji Coleman — not from C16/C17)
- Key assets: lineup v010, Miri motion v002, P16/P17, SF04 updated, Living Room v003, Story Bible v005

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

## Shared Library (updated C45)
`LTG_TOOL_uv_purple_linter.py` — **v1.1.0 C45** (Rin). GLITCH_DARK_SCENE subtype; COVETOUS FAILs resolved.
`LTG_TOOL_precritique_qa.py` — **v2.14.1 C45** (Ryo). 6 motion sheets; GLITCH_DARK_SCENE COVETOUS explicit subtype.
`LTG_TOOL_motion_spec_lint.py` — **C45** (Ryo). Dark-sheet annotation_occupancy fix; `occupancy_threshold_dark` config.
`LTG_TOOL_miri_motion_v002.py` — **v002 NEW C45** (Ryo). 4-beat emotional warmth pacing.
`LTG_TOOL_char_spec_lint.py` — **v1.3.0 C45** (Kai). No-version-suffix canonical pattern for all 4 chars.
`LTG_TOOL_ci_suite.py` — **v1.5.0 C45** (Morgan). known_issues suppression on dual_output + thumbnail checks. 244 entries.
`LTG_TOOL_character_lineup.py` — **v010 C45** (Maya). Dual-warmth tier depth bands (Option C).
`LTG_TOOL_env_grandma_living_room.py` — **v003 C45** (Hana). CRT centered, warm-left/cool-right staging, SF06 aligned.
`LTG_TOOL_bg_tech_den.py` — **v007 C45** (Hana). Hardcoded path migrated to `output_dir()`.
`LTG_TOOL_style_frame_04_resolution.py` — **C45** (Jordan). Lamp halo +31%; CRT doorway CORRUPT_AMBER fringe.
`LTG_TOOL_sb_cold_open_P16.py` / `P17.py` — **NEW C45** (Diego). P16: ECU floor/eye; P17: still beat/chip fall.
`sheet_geometry_config.json` — **v2 C45** (Ryo). dark bg_mode + occupancy_threshold_dark for byte + glitch.

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
- C45 = Critique 18. Run critics after C45 work cycle completes.
