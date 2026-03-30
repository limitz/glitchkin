# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: all core assets present.

## Status
**Cycle 43 complete. Critique 17 complete. Work cycles: 43. Critique cycles: 17.**
**C44 = next work cycle. Critique 18 due after C45.**

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

**Agent scheduling:** Max 8 simultaneous. Launch next agent immediately when a slot opens. Dependency-blockers go first. NEVER exceed 8 — do not launch agent 9 until one of the first 8 completes.

## Image Output Rule (MANDATORY)
**Hard limit: ≤ 1280px in both dimensions.** Use `img.thumbnail((1280,1280), Image.LANCZOS)` before saving.
**WARNING:** `.thumbnail()` on 1920px → 1280px averages 1.5px strips — warm hues drift up to 47° LAB. Use native canvas (1280×720) instead. See Jordan's C43 SF02 refactor.

## Critique Format
Score (0–100) → bullet issues (≤2 lines each) → single Bottom line. ≤15 lines per asset.

## Critics Panel (20 total)
- 15 industry professionals + 5 audience (Zoe Park age 11, Marcus Okafor parent, Jayden Torres age 13, Eleanor Whitfield grandparent, Taraji Coleman educator)
- **Rotate each cycle. Min 1 audience critic per critique cycle.**
- C15 critics: Takeshi Mori, Ingrid Solberg, Reinhardt Böhm, Zoe Park, Taraji Coleman
- C16 critics: Daisuke Kobayashi, Priya Nair, Sven Halvorsen, Chiara Ferrara, Jayden Torres
- C17 critics: Jonas Feld, Amara Diallo, Leila Asgari, Petra Volkov, Marcus Webb, Eleanor Whitfield
- **C18 candidates**: rotate in Takeshi Mori, Ingrid Solberg, Reinhardt Böhm, Chiara Ferrara, + 1 audience not from C16/C17 (Zoe Park, Marcus Okafor, Jayden Torres, Taraji Coleman)

## Pitch Package Status — POST CYCLE 43

### Style Frames
- **SF01 Discovery**: v006
- **SF02 Glitch Storm**: **v008 C43 — native 1280×720 COMPLETE** (Jordan). SUNLIT_AMBER ΔE 1.1 PASS (was 47.04). No more 1920+LANCZOS generators.
- **SF03 Other Side**: v005 (UV_PURPLE ΔE 0.0 C41)
- **SF04 Resolution**: CANONICAL C42 (Jordan). Output dir fixed C43 → `output/color/style_frames/`. Warm/cool 13.2 PASS.
- **SF05 COVETOUS Glitch**: **v3.0.0 C43** (Lee). Luma SENSING UNEASE face added — face gate PASS. ACID_GREEN covet-vector sight-line. UV_PURPLE rim on Luma shoulder.

### Logo
- **LTG_BRAND_logo.png** — DECIDED C25. DejaVu Sans — **typography brief C43** (Sam). 5 candidates evaluated; primary rec: Nunito Bold + Space Grotesk Bold. Alex decision pending C44.

### Characters
- Luma: expr v013 C41, turnaround v004, color model v002. Face curves live (v1.1.0 Kai).
- Byte: expr v007 C41, turnaround v001, color model v001. **`--char byte` face test profile: STILL MISSING** (Kai — C44 P1).
- Cosmo: expr v007 C38. Motion spec v001 C41.
- Miri: expr v005 C40. **FLAG 05 OPEN**: chopstick MIRI-A = cross-cultural error (Amara Diallo C17). Replace with wooden hairpins — Alex confirmation pending C44. Maya assessed: 6 files to update atomically. Motion spec v001 NEW C43 (Ryo).
- Glitch: expr v003. Body primitive diagram C41. No motion spec — Ryo flagged.
- Character lineup: v008 C42 (Maya). **Miri+Luma shared-frame asset: OPEN GAP** (Marcus Webb + Eleanor Whitfield C17 — highest priority new asset for C44).

### Environments
- Kitchen: **v006 C43** — MIRI label via canonical draw_pixel_text(). Warm/cool 32.6 PASS.
- Tech Den: v006 C41 — warm/cool 102.9 PASS.
- Glitch Layer: v003 (3 generators native 1280×720 C42).
- **School Hallway: v004 C43** — MILLBROOK MIDDLE SCHOOL seal (pixel font). Canonical school name confirmed Story Bible v004.
- Millbrook Street: v002.
- Living Room: v001.
- Other Side: C41 (UV_PURPLE ΔE 0.0).
- Classroom: **v003 C43** — chalkboard text deployed ("1011 XOR 0110", "F X  2X 5"). Warm/cool 17.0 PASS.
- Luma Study Interior: NEW C42. Warm/cool 33.1 PASS.

### Storyboards
- Cold Open: v003 C39 (night/den canonical).
- Panels: P03/P06/P07/P08/P09/P23/P24 + EP05 COVETOUS + **P10/P11 NEW C43** (Diego). P10: OTS Byte POV pre-discovery. P11: ECU Luma closed eyes/brow twitch threshold.
- Three-tier caption hierarchy (Jonas Feld C17): implemented on P10/P11. **Caption retrofit tool for P03–P09/P23/P24: C44** (Diego).
- PANEL_MAP.md: P01–P25 with status. Storyboard naming audit complete C43 — legacy `LTG_SB_coldopen_panel_XX` (26 files) NOT yet renamed (tool hardcodes). Morgan to add CI action C44.

### Story
- **Story Bible: v004 C43** (Priya). Miri heritage confirmed: Igbo-Nigerian + Brazilian-descended. Millbrook = Ohio/Indiana region, post-war, modest industrial past. School = MILLBROOK MIDDLE SCHOOL. FLAG 05 open.
- **Miri Cultural Identity Brief: NEW C43** (`output/production/story/LTG_miri_cultural_identity_brief.md`). Chopstick → wooden hairpins spec. Cultural framework documented.
- Scene handoff briefs v001 C42. Pilot outline v001 C41.

### Motion
- Luma motion: v002 C38.
- Byte motion: v002 C38.
- Cosmo motion: v001 C41.
- **Miri motion: v001 NEW C43** (Ryo). WARM ATTENTION / SHARP ASSESSMENT / PROUD QUIET JOY / PATIENT CORRECTION. Lint: 6 PASS / 0 WARN / 0 FAIL.

## QA Baseline
**precritique_qa v2.11.0 C43** (Ryo). SF04 path corrected; all 4 motion sheets covered; motion lint: 20 PASS / 4 WARN / 0 FAIL.
**QA re-run required** — scope changed (SF04 path, Miri motion added).
Section 10 alpha_blend_lint: **NOW UNBLOCKED** — Rin added `--save-nolight` to SF01/SF02/SF04. Run `--save-nolight` to generate base images.

## C43 Key Decisions & Deliverables
- **SF02 native refactor complete** — LANCZOS era over. `.thumbnail()` on 1920→1280 = up to 47° LAB drift. Canonical pattern: native 1280×720 canvas.
- **SF04 output dir fixed** — `output/color/style_frames/` canonical.
- **SF05 COVETOUS v3.0.0** — Luma face (SENSING UNEASE) + covet-vector sight-line + UV rim.
- **`LTG_TOOL_project_paths.py` v1.0.0** (Kai) — `project_root()` resolver, `--audit` CLI. 94 files need migration; CI gate ideabox → C44 Morgan.
- **`vp_spec_config.json` v1.0.0** (Kai) — 11 ENV VP specs. `sobel_vp_detect` v1.1.0 batch mode.
- **CI suite v1.3.0** (Morgan) — Check 6: dual-output-file detection. SF01 legacy retired to `deprecated/`.
- **Pixel font deployed**: classroom chalkboard + kitchen MIRI label + hallway seal (MILLBROOK MIDDLE SCHOOL).
- **Story Bible v004** — Miri cultural framework, Millbrook location, school name canonical.
- **Miri cultural identity brief** — FLAG 05 open (chopstick→hairpin). Maya assessed 6-file impact; awaiting Alex C44 confirmation.
- **Typography brief** — 5 OFL font candidates; primary rec Nunito Bold + Space Grotesk Bold. Alex decides C44.
- **Miri motion spec v001** — 4-beat vocabulary; lint PASS.
- **P10/P11 new panels** — Three-tier caption hierarchy (Jonas Feld P1) implemented.
- **`--save-nolight` flag** (Rin) — unlocks Section 10 alpha_blend_lint.

## Open Items for C44
**P0 — Decision needed:**
0. **Alex**: Confirm chopstick→wooden hairpin for Miri (FLAG 05). Maya has 6-file list + lint constraint. Atomic commit required.
1. **Alex**: Choose logo display typeface from Sam's brief (Nunito+Space Grotesk primary rec).

**P1 — High priority:**
2. **Kai**: `--char byte` face test profile (still missing — Diego/Lee/Rin blocked on Byte face gate)
3. **Maya**: Execute Miri chopstick→hairpin change (6 files, atomic — after Alex confirmation)
4. **Jordan/Priya/Maya**: Miri+Luma relationship style frame (biggest pitch gap per C17 — "CRT as matrilineal heirloom")
5. **Diego**: Caption retrofit tool + apply to P03–P09/P23/P24 (Jonas Feld P1)
6. **Morgan**: Path migration C44 — 94 generators, use `LTG_TOOL_project_paths.py`
7. **Morgan**: CI gate for hardcoded paths (`--audit` in ci_suite) + `.thumbnail(` lint check

**P2 — Actioned ideabox:**
8. **Sam/Kai**: `assets/fonts/` directory + font pipeline integration (after Alex typeface decision)
9. **Morgan**: Retired tools section in README Script Index
10. **Kai**: char_spec_lint token config (data-driven JSON/TOML, M004 etc.)
11. **Kai or Morgan**: UV_PURPLE dominance linter for Glitch Layer generators (Rin ideabox)
12. **Morgan**: Motion sheet coverage check in ci_suite (Glitch has no motion spec)
13. **Hana or Kai**: Pixel font perspective-scale helper (chalkboard text recession)
14. **Ryo**: Glitch motion spec (no motion spec exists)
15. **Maya**: Lineup tier depth indicator band (carried from C43)

**C45 = Critique 18 (every 3 cycles)**

## Canonical Palette
- Byte body = GL-01b #00D4E8 BYTE_TEAL (NOT #00F0FF)
- CORRUPT_AMBER = GL-07 #FF8C00
- HOT_MAGENTA = GL-02 #FF2D6B
- UV_PURPLE = #7B2FBE
- CHAR-L-11 = #00F0FF Electric Cyan
- SF03: zero warm light; Classroom: zero Glitch palette
- Byte shape = OVAL (NOT triangles — retired C8)
- Cosmo glasses = 7° tilt ±2°
- CHAR-M-11 slipper = #C4907A (NOT #5A7A5A — corrected C32, propagated C38)
- CHAR-C-02 = #B89A78 Cosmo Skin Shadow (warm, guaranteed)
- CHAR-C-03 = #EED4B0 Cosmo Skin Highlight (warm, guaranteed)
- Cosmo cardigan RW-08 #A89BBF Dusty Lavender = COOL (intentional, NOT warm-guaranteed)

## Key Output Locations
- Style Frames: `output/color/style_frames/`
- Characters: `output/characters/main/`, motion: `output/characters/motion/`
- Environments: `output/backgrounds/environments/`
- Storyboards: `output/storyboards/`
- Story/Script: `output/production/story/`
- Tools: `output/tools/`
- Master Palette: `output/color/palettes/master_palette.md`
- Pitch Package Index: `output/production/pitch_package_index.md`
- Deprecated tools: `output/tools/deprecated/`

## Pipeline Standards
- Open source only: Python PIL + **numpy, OpenCV (cv2), PyTorch** (authorized C39)
- cv2 default is BGR — convert to RGB on load. Use PIL for drawing; numpy/cv2 for analysis.
- ΔE color distance threshold = 5.0 (LAB perceptual, replaces RGB Euclidean)
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]` — everything in output/tools/ uses LTG_TOOL_* prefix
- output/production/ files EXEMPT from LTG naming
- After img.paste(): always refresh draw = ImageDraw.Draw(img)
- show_guides=False for all pitch exports
- Python 3.8 compat: `from __future__ import annotations`
- REAL_INTERIOR warm/cool threshold = 12.0 (render_qa v2.0.0)
- **NEVER use `.thumbnail()` on generators** — use native canvas (1280×720). `.thumbnail()` causes LAB drift up to 47°.
- Paths: use `LTG_TOOL_project_paths.py` `project_root()` — never hardcode `/home/wipkat/team`.

## Shared Library (updated C43)
`LTG_TOOL_project_paths.py` — **v1.0.0 NEW C43** (Kai). `project_root()` anchor on CLAUDE.md; `output_dir/tools_dir/resolve_output()`; `--audit` CLI.
`vp_spec_config.json` — **v1.0.0 NEW C43** (Kai). 11 ENV VP specs (7 real-world, 4 glitch-layer null).
`LTG_TOOL_sobel_vp_detect.py` — **v1.1.0 C43** (Kai). `--vp-config` batch mode.
`LTG_TOOL_ci_suite.py` — **v1.3.0 C43** (Morgan). Check 6: dual-output-file detection.
`LTG_TOOL_precritique_qa.py` — **v2.11.0 C43** (Ryo). All 4 motion sheets; SF04 path corrected.
`LTG_TOOL_miri_motion.py` — **v001 NEW C43** (Ryo). 4-panel motion spec, lint PASS.
`LTG_TOOL_sf_covetous_glitch_c43.py` — **v3.0.0 C43** (Lee). Luma SENSING UNEASE face; covet-vector sight-line.
`LTG_TOOL_bg_classroom.py` — **v003 C43** (Hana). Pixel font on chalkboard.
`LTG_TOOL_bg_grandma_kitchen.py` — **v006 C43** (Hana). MIRI label via draw_pixel_text().
`LTG_TOOL_bg_school_hallway.py` — **v004 C43** (Diego). MILLBROOK MIDDLE SCHOOL seal.
`LTG_TOOL_style_frame_02_glitch_storm.py` — **C43 native rewrite** (Jordan). 1280×720 native.
`LTG_TOOL_styleframe_discovery.py` — **C43** (Rin). `--save-nolight` flag added.
`LTG_TOOL_style_frame_04_resolution.py` — **C43** (Jordan/Rin). Output dir fixed + `--save-nolight`.

## Shared Library (historical C42)
`LTG_TOOL_render_lib.py` — **v1.2.0 C42** (Hana). `flatten_rgba_to_rgb()` helper.
`LTG_TOOL_ci_suite.py` — **v1.2.0 C42** (Morgan). `--warn-stale N` flag.
`LTG_TOOL_sobel_vp_detect.py` — **v1.0.0 C42** (Kai). Sobel/HoughLines VP detection.
`LTG_TOOL_sf_covetous_glitch.py` — **v2.0.0 C42** (Rin). G001/G004/G008 PASS.
`LTG_TOOL_motion_spec_lint.py` — **C42** (Ryo). Per-family beat color config.
`LTG_TOOL_bg_luma_study_interior.py` — **NEW C42** (Hana). 1280×720, warm/cool 33.1 PASS.
`LTG_TOOL_character_lineup.py` — **v008 C42** (Maya). Two-tier ground plane.
`LTG_TOOL_sb_cold_open_P07.py` / `P09.py` — **NEW C42** (Diego). P07 Dutch 8° CW; P09 FIRST ENCOUNTER.
`LTG_TOOL_sb_ep05_covetous.py` — **NEW C42** (Diego). 3-char triangulation storyboard.
`LTG_TOOL_render_qa.py` — **v2.0.0 C39**. numpy/cv2 LAB ΔE.
`LTG_TOOL_precritique_qa.py` — **v2.9.0 C41** baseline (255 PASS / 31 WARN / 0 FAIL).
`LTG_TOOL_palette_warmth_lint.py` — **v6.0.0 C39**. numpy vectorized.
`LTG_TOOL_luma_face_curves.py` — **v1.1.0 C40** (Kai). All 9 expressions, 100px eye width.
`LTG_TOOL_face_curve_validator.py` — **NEW C40** (Maya). All 10 expressions PASS.
`LTG_TOOL_sight_line_diagnostic.py` — **v002 C40** (Lee). `--batch config.json`.
`LTG_TOOL_pixel_font_v001.py` — **NEW C39** (Jordan). 5×7 bitmap A–Z/0–9.
`LTG_TOOL_fill_light_adapter.py` — **v1.1.0 C39**.
`LTG_TOOL_alpha_blend_lint.py` — **NEW C39** (Rin). LAB gradient, FLAT_FILL detection.
`LTG_TOOL_bodypart_hierarchy.py` — **v002 C39** (Maya).
`LTG_TOOL_world_type_infer.py` — **NEW C38**.

## Agent Prompt Design
Do NOT duplicate inbox content in agent prompts. Prompts = role context + startup sequence only.

## Producer Responsibilities
- Ideabox: action worthy ideas → actioned/, rejects → rejected/ after each cycle.
- README.md: update after every work and critique cycle.
- Slot filling: launch next agent immediately on completion. Never exceed 8 simultaneous.
- New member onboarding: update MEMORY.md with catch-up section before first assignment.
