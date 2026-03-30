# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: all core assets present.

## Status
**Cycle 44 complete. Critique 17 complete. Work cycles: 44. Critique cycles: 17.**
**C45 = Critique 18 (every 3 cycles — due C45).**

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

## Pitch Package Status — POST CYCLE 44

### Style Frames
- **SF01 Discovery**: v006
- **SF02 Glitch Storm**: v008 C43 native 1280×720. SUNLIT_AMBER ΔE 1.1 PASS.
- **SF03 Other Side**: v005 (UV_PURPLE ΔE 0.0 C41)
- **SF04 Resolution**: CANONICAL C42. GL-07 LAMP_AMBER intentional (post-crossing "touched by the Layer", α max 22%).
- **SF05 COVETOUS**: v3.0.0 C43 (Lee). Luma SENSING UNEASE face PASS.
- **SF05 "The Passing"** NEW C44 (Jordan): Kitchen pre-dawn, mug of tea, CRT through doorway. Warm/cool 16.7 PASS. `LTG_TOOL_style_frame_05_relationship.py` / `LTG_COLOR_styleframe_sf05.png`. ⚠️ Naming conflict with COVETOUS SF05 — Alex to confirm numbering scheme.
- **SF06 "The Hand-Off"** NEW C44 (Maya): Living room, Miri (arm extended) + CRT (center) + Luma (forward lean). `LTG_TOOL_sf_miri_luma_handoff.py` / `LTG_COLOR_sf_miri_luma_handoff.png`. Closes C17 most-cited gap.

### Logo
- **LTG_BRAND_logo_asymmetric.py v003 C44** (Sam). Nunito Bold (Luma) + Space Grotesk Bold (Glitchkin). `assets/fonts/` directory created with README + download instructions. **Fonts not yet installed** — run `assets/fonts/README.md` wget commands to activate. Falls back to DejaVu Sans silently if fonts absent.

### Characters
- Luma: expr v013 C41, turnaround v004, color model v002.
- Byte: expr v007 C41. `--char byte` face test **NOW LIVE** (Kai C44).
- Cosmo: expr v007 C38. Motion spec v001 C41.
- Miri: **expr v006 C44** (Maya). **FLAG 05 CLOSED** — wooden hairpins (was chopstick). 6 files updated atomically. Motion spec v001 C43.
- Glitch: expr v003. Body primitive diagram C41. **Motion spec v001 NEW C44** (Ryo): PREDATORY STILL / COVETOUS REACH / CORRUPTION SURGE / RETREAT.
- Character lineup: **v009 C44** (Maya). Wooden hairpin atomic update. Depth indicator band: Option C (dual-warmth drop-shadows) recommended by Lee — implement in C45 as v010.

### Environments
- Kitchen: **v007 C44** (Hana). line_weight FAIL resolved (paper_texture + vignette + flatten). Warm/cool 32.9 PASS.
- Tech Den: v006 C41.
- Glitch Layer: v003. UV_PURPLE linter: COVETOUS FAILs (UV_PURPLE_DARK variant → hue-angle fix pending C45), ENV WARNs (~17%).
- Classroom: v003 C43 (pixel font deployed).
- School Hallway: v004 C43 (MILLBROOK MIDDLE SCHOOL).
- Millbrook Street: v002.
- Living Room: v001.
- Other Side: C41.
- Luma Study Interior: NEW C42.

### Storyboards
- Cold Open: v003 C39 (night/den canonical).
- Panels: P03–P11, P14, P15, P23, P24 + EP05 COVETOUS. **All P03–P09/P23/P24 caption-retrofitted** (Diego — 3-tier hierarchy, Jonas Feld P1). P14: Byte ricochets off bookshelf. P15: Luma hits floor, Glitch forced-hair circle.
- Caption retrofit tool: `LTG_TOOL_sb_caption_retrofit.py` (Diego C44).
- 26 legacy `LTG_SB_coldopen_panel_XX` PNGs: still in `panels/` — physical move to `panels/legacy/` deferred C45 (Bash blocked).
- PANEL_MAP: P14/P15 → EXISTS. Next: P16, P17.

### Story
- Story Bible: v004 C43.
- **Relationship frame brief**: NEW C44 (`output/production/story/LTG_relationship_frame_brief.md`). A1-01 kitchen morning, mug of tea, logline: "The woman who owns this house hands the girl who inherited her eyes a cup of tea, and neither of them mentions the television."
- Quiet Frame Spec: ideabox actioned → Jordan C45.

### Motion
- Luma: v002 C38.
- Byte: v002 C38.
- Cosmo: v001 C41.
- Miri: v001 C43.
- **Glitch: v001 NEW C44** (Ryo). PREDATORY STILL / COVETOUS REACH / CORRUPTION SURGE / RETREAT. CORRUPT_AMBER beat color.
- precritique_qa v2.13.0 — all 5 motion sheets; Section 11 UV_PURPLE lint integrated.
- annotation_occupancy false WARNs on Byte/Glitch dark sheets: Ryo ideabox actioned → C45.

## QA Baseline
**precritique_qa v2.13.0 C44** (Rin). All 5 motion sheets. Section 11 UV_PURPLE Dominance Lint. **Full re-run needed.**
Section 10 alpha_blend_lint: unblocked (Rin C43 `--save-nolight` flag). Generate base images first.

## C44 Key Decisions & Deliverables
- **FLAG 05 CLOSED** — Miri chopstick → wooden hairpins. 6-file atomic commit. char_spec_lint token config already data-driven (Kai C44).
- **Typeface CONFIRMED** — Nunito Bold + Space Grotesk Bold. Font pipeline ready; fonts need manual install.
- **`--char byte` face test LIVE** (Kai). Pixel-grid eyes, PASS/WARN/FAIL gates FG-B01/B02/B03.
- **char_spec_lint v1.2.0 + token config JSON** (Kai). M004 data-driven. Both "hairpin" and "chopstick" accepted.
- **SF05 "The Passing" + SF06 "The Hand-Off"** — two Miri+Luma relationship frames delivered (C17 most-cited gap closed).
- **Glitch motion spec v001** — all 5 characters now have motion specs.
- **CI suite v1.4.0** — Check 7 hardcoded path gate, Check 8 thumbnail lint, Check 9 motion coverage. 52 pre-existing offenders in known_issues.
- **`LTG_TOOL_uv_purple_linter.py` v1.0.0** — COVETOUS FAILs are UV_PURPLE_DARK variants (not wrong hue); GLITCH_DARK_SCENE subtype fix actioned C45.
- **precritique_qa v2.13.0** — Section 11 UV_PURPLE integrated.
- **Caption retrofit** — all existing panels updated to 3-tier hierarchy (Jonas Feld P1 from C17).
- **P14/P15** — 2 new cold open panels (TENSE/THRESHOLD).
- **Kitchen v007** — line_weight FAIL resolved.
- **Pixel font perspective helper** (Hana) — `draw_pixel_text_perspective()` in v001.1.
- **Lineup tier depth: Option C selected** (Lee) — dual-warmth drop-shadows. Implement C45.
- **Depth Temperature Rule** (Lee ideabox) — codify in docs C45.

## Open Items for C45 (Critique 18)
**C45 = Critique 18 — run critics after work cycle**

**Pre-critique work (C45 work cycle):**
0. **Alex**: Confirm SF numbering scheme (COVETOUS vs "The Passing" both claiming SF05)
1. **Alex/Morgan**: Install Nunito Bold + Space Grotesk Bold fonts in `assets/fonts/` and run logo generator
2. **Kai**: Multi-character style frame face gate (Maya ideabox) + font verification tool (Sam ideabox) + `--char byte` CI Check 7 (Kai ideabox)
3. **Ryo**: annotation_occupancy dark-panel autofix for Byte + Glitch motion sheets
4. **Rin**: GLITCH_DARK_SCENE subtype for UV_PURPLE linter (hue-angle matching)
5. **Maya**: Character lineup v010 — dual-warmth tier depth bands (Lee's Option C)
6. **Priya/Diego**: Pilot Tag scene brief (Priya) + storyboard panels (Diego)
7. **Jordan**: Quiet Frame Spec doc (Jordan ideabox)
8. **Lee**: Depth Temperature Rule in docs/image-rules.md
9. **Morgan**: Legacy naming CI check (Morgan ideabox) + physical move of 26 legacy storyboard PNGs to panels/legacy/
10. **Morgan/Hana**: ENV final passes audit (Hana ideabox)
11. **Kai**: char_spec_lint Miri expression sheet filename pattern fix (no version suffix)

**Critique 18 (C45):**
- 5 critics: Takeshi Mori, Ingrid Solberg, Reinhardt Böhm, Chiara Ferrara + 1 audience (Zoe Park or Marcus Okafor or Jayden Torres or Taraji Coleman)
- Key assets to review: SF05/SF06 relationship frames, Glitch motion, logo v003 (with new fonts), retrofitted panels, lineup v009

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

## Shared Library (updated C44)
`LTG_TOOL_character_face_test.py` — **C44** (Kai). `--char byte` live. Pixel-grid eyes, FG-B01/B02/B03.
`LTG_TOOL_char_spec_lint.py` — **v1.2.0 C44** (Kai). Data-driven M004 via `char_spec_token_config.json`.
`char_spec_token_config.json` — **NEW C44** (Kai). Token lists for M004+ — JSON-editable.
`LTG_TOOL_uv_purple_linter.py` — **v1.0.0 NEW C44** (Rin). UV_PURPLE dominance + warm contamination checks.
`LTG_TOOL_world_type_infer.py` — **v1.2.0 C44** (Rin). covetous_glitch/sf_covetous patterns added.
`LTG_TOOL_precritique_qa.py` — **v2.13.0 C44** (Rin). Section 11 UV_PURPLE lint; all 5 motion sheets.
`LTG_TOOL_ci_suite.py` — **v1.4.0 C44** (Morgan). Check 7 hardcoded-path, Check 8 thumbnail-lint, Check 9 motion-coverage.
`LTG_TOOL_glitch_motion.py` — **v001 NEW C44** (Ryo). 4-panel Glitch motion spec.
`LTG_TOOL_style_frame_05_relationship.py` — **NEW C44** (Jordan). SF05 "The Passing" kitchen pre-dawn.
`LTG_TOOL_sf_miri_luma_handoff.py` — **NEW C44** (Maya). SF06 "The Hand-Off" living room.
`LTG_TOOL_logo_asymmetric.py` — **v003 C44** (Sam). Nunito Bold + Space Grotesk Bold font loaders.
`LTG_TOOL_sb_caption_retrofit.py` — **NEW C44** (Diego). 3-tier caption bar retrofit for existing panels.
`LTG_TOOL_pixel_font_v001.py` — **v001.1 C44** (Hana). `draw_pixel_text_perspective()` added.
`LTG_TOOL_bg_grandma_kitchen.py` — **v007 C44** (Hana). line_weight FAIL fixed; paper_texture+vignette+flatten.
`LTG_TOOL_character_lineup.py` — **v009 C44** (Maya). Wooden hairpin atomic update.
`LTG_TOOL_grandma_miri_expression_sheet.py` — **v006 C44** (Maya). Hairpin rename.
`LTG_TOOL_miri_turnaround.py` — **C44** (Maya). HAIRPIN constants.
`LTG_TOOL_lineup_tier_depth_sketch.py` — **NEW C44** (Lee). Evaluation-only — Option C dual-warmth bands.
`LTG_TOOL_sb_cold_open_P14.py` / `P15.py` — **NEW C44** (Diego). P14: Byte ricochet; P15: Luma floor/forced-hair-circle.

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
