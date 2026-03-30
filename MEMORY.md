# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: all core assets present.

## Status
**Cycle 42 complete. Critique 17 complete. Work cycles: 42. Critique cycles: 17.**
**C43 = next work cycle.**

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

## Critique Format
Score (0–100) → bullet issues (≤2 lines each) → single Bottom line. ≤15 lines per asset.

## Critics Panel (20 total)
- 15 industry professionals + 5 audience (Zoe Park age 11, Marcus Okafor parent, Jayden Torres age 13, Eleanor Whitfield grandparent, Taraji Coleman educator)
- **Rotate each cycle. Min 1 audience critic per critique cycle.**
- C15 critics (last ran): Takeshi Mori, Ingrid Solberg, Reinhardt Böhm, Zoe Park, Taraji Coleman
- **C16 ran**: Daisuke Kobayashi, Priya Nair, Sven Halvorsen, Chiara Ferrara, Jayden Torres (audience, age 13)
- C17 candidates: rotate in Jonas Feld, Amara Diallo, Leila Asgari, Petra Volkov, Marcus Webb (+ 1 audience not from C15/C16: Marcus Okafor, Eleanor Whitfield)

## Pitch Package Status — POST CYCLE 42

### Style Frames
- **SF01 Discovery**: v006
- **SF02 Glitch Storm**: v008 ⚠️ LAST 1920×1080+LANCZOS generator — Jordan to refactor C43
- **SF03 Other Side**: v005 (UV_PURPLE ΔE 0.0 C41 — root cause fixed)
- **SF04 Resolution**: CANONICAL C42 (Jordan) — Luma post-crossing in kitchen, Byte as CRT ghost, warm/cool 13.2 PASS. Alex decision broadcast C42.
- **SF05 COVETOUS Glitch**: v2.0.0 C42 (Rin) — G001/G004/G008 all PASS, 3-char triangulation (Glitch→Byte→Luma)

### Logo
- **LTG_BRAND_logo.png** — DECIDED C25

### Characters
- Luma: **expr v013 NEW C41** (RECKLESS wide-arm body, ALARMED bilateral recoil, THE_NOTICING gaze RIGHT fixed — sight-line PASS), turnaround v004, color model v002
  - **v012 C41**: face curves live (THE_NOTICING/WORRIED/FRUSTRATED/DETERMINED/THE_NOTICING_DOUBT on bezier)
  - Face Curve Spec v002 C40 — 100px eye width
  - Silhouette strategy: Hybrid (RECKLESS/ALARMED/FRUSTRATED/THE_NOTICING = Tier 1 body postures)
- Byte: **expr v007 NEW C41** (UNGUARDED WARMTH — bilateral arm raise, float −4px, toe-in trapezoid legs), turnaround v001, color model v001
- Cosmo: expr v007 C38. **Motion spec v001 NEW C41** (IDLE/STARTLED/ANALYSIS_LEAN/RELUCTANT_MOVE)
- Miri: expr v005 C40 (M001 fixed)
- Glitch: expr v003. Diamond body primitive spec + diagram `LTG_CHAR_glitch_body_primitive_diagram.png` C41. G007 = VOID_BLACK outline is CORRECT per spec (Alex clarified C41).
- Character lineup: **v008 C42** (Maya) — two-tier ground plane, Luma center-protagonist, RPD PASS

### Environments
- Kitchen: v005 C39 (MIRI fridge label)
- **Tech Den: v006 C41** — warm/cool 102.9 PASS in-generator (no warminjected needed; RGBA→RGB flatten fix)
- Glitch Layer: v003 (3 generators fixed native 1280×720 C42 — bg_glitchlayer_frame, bg_glitch_layer_frame, bg_glitch_layer_encounter)
- School Hallway: v003 C42 regenerated (Jordan)
- Millbrook Street: v002
- Living Room: v001
- Other Side: C41 (UV_PURPLE ΔE 0.0 — root cause: native 1280×720 canvas; was 1920×1080+LANCZOS)
- **Classroom: v001 C41** — warm/cool 17.0 PASS
- **Luma Study Interior: NEW C42** (Hana) — warm/cool 33.1 PASS, 3 light sources, Miri Easter eggs, first-ever generator

### Storyboards
- Cold Open: v003 C39 (night/den canonical)
- **Standalone panels C41**: P06 (cracked-eye divergence fixed), P08 (gaze contempt corrected), P23 (Promise Shot — Luma+Byte backs to monitors), P24 (Chaos Apex — 28 Glitchkin swarm, Dutch angle, PITCH BEAT)
- All panels: P03/P06/P07/P08/P09/P23/P24 EXISTS. **EP05 COVETOUS panel NEW C42** (Diego).
- Canon: Night/Grandma's den. School/daytime = pre-credits Act 1 tag.
- **pilot_episode_outline_v001.md C41** — "Dead Pixels" scene-by-scene
- **scene_handoff_briefs_v001.md NEW C42** (Priya) — per-scene execution briefs for Acts 1–3, keyed to PANEL_MAP.md. A3-02 = highest storyboard priority.

### Story
- **Story Bible: v003 NEW C39** (cold open = night/den canonical, Glitch = Corruption's avatar)
- **Glitch Appearance Guide NEW C39** — 8-beat first appearance, geometric-pattern communication rules
- Glitch role: Corruption's avatar (decided C38)

### Motion
- **Luma motion: v002 NEW C38** (CG polygon fix, shoulder mass, hair annotation)
- **Byte motion: v002 NEW C38** (crack scar side, glow radius annotated)

## QA Baseline (C41 — C42 baseline not yet run)
precritique_qa **v2.9.0**: **255 PASS / 31 WARN / 0 FAIL** (Morgan C41 baseline).
Section 10 alpha_blend_lint: all 3 SF assets SKIP (no `*_nolight.png` bases yet).
Native resolution fix: UV_PURPLE ΔE 0.0 in SF03 + Other Side ENV + 3 Glitch Layer ENV generators (C42).
render_lib v1.2.0: `flatten_rgba_to_rgb()` helper added (Hana C42) — correct Porter-Duff via Pillow alpha_composite.
Motion spec lint: annotation occupancy false WARNs fixed (Ryo C42) — per-family bg color spec in sheet_geometry_config.json.

## C42 Key Decisions & Deliverables
- **SF04 canonical = "Resolution"** (Jordan C42, Alex decision broadcast). Warm/cool 13.2 PASS. C41 lamp scene v005 superseded.
- **LAMP_AMBER = GL-07 intentional** in SF04 (post-crossing kitchen "touched by the Layer", alpha max 22%). Inline comment added.
- **Rin's native res audit**: Only SF02 remains at 1920×1080+LANCZOS (complex refactor). All ENV generators now fixed or legacy-flagged.
- **Luma Study Interior**: First-ever generator built from scratch (31 cycles of legacy PNG closed).
- **render_lib v1.2.0**: `flatten_rgba_to_rgb()` canonical pattern replacing manual numpy Porter-Duff.
- **ci_suite v1.2.0**: `--warn-stale N` flag operational, all 38 suppressions tagged `since_cycle: C39`.
- **Sobel VP detect v1.0.0**: HoughLines-based VP coordinate detection with tolerance PASS/WARN/FAIL.
- **Scene handoff briefs v001**: Full pilot Acts 1–3 briefs keyed to PANEL_MAP.md (A3-02 = pilot's emotional center).

## C39 Key Decisions & Deliverables
- **Bezier face system**: `output/production/luma_face_curve_spec.md` — 10 named curves, 6 expression deltas. **HOLD on tool implementation** — Maya found critical eye width discrepancy (spec 56px vs generator ~100px at 600px canvas). Alex must resolve before Kai builds tool.
- **Glitch appearance guide**: `output/production/story/LTG_glitch_appearance_guide.md` (Priya) — 8-beat first-appearance sequence, geometric communication rules.
- **Kitchen v005**: MIRI fridge label confirmed in place.
- **PANEL_MAP.md**: `output/storyboards/PANEL_MAP.md` — P01–P25 with status (6 on contact sheet, 19 planned).
- **numpy/OpenCV/PyTorch**: Now authorized. render_qa v2.0.0, warmth_lint v6.0.0 upgraded.
- **Cosmo warmth lint**: CHAR-C added to warm_prefixes. 17 entries / 0 violations.
- **Sheet geometry calibration**: `sheet_geometry_config.json` created. Motion lint zone sampling now auto-calibrated.

## C17 Critique Scores

| Asset | Jonas | Amara | Leila | Petra | Marcus | Eleanor |
|-------|-------|-------|-------|-------|--------|---------|
| SF01 | — | — | 68 | — | 72 | — |
| SF02 | — | — | 55 | — | 55 | — |
| SF03 | — | — | 71 | — | 66 | — |
| SF04 | — | — | 62 | — | 74 | — |
| SF05 COVETOUS | — | — | 74 | — | 58 | — |
| Lineup v008 | — | — | 66 | — | 64 | — |
| Logo | 52 | — | — | — | 68 | — |
| Classroom chalkboard | 34 | — | — | — | — | — |
| Hallway seal | 38 | — | — | — | — | — |
| Pixel font tool | 68 | — | — | — | — | — |
| Miri design | — | 48 | — | — | — | 88 |
| Luma design | — | 62 | — | — | — | — |
| Kitchen ENV | — | 54 | — | — | — | 81 |
| Millbrook | — | 44 | — | — | — | — |
| CRT treatment | — | — | — | — | — | 91 |
| Intergenerational rel. | — | — | — | — | 74 (SF04) | 74 |
| Coherence | — | — | 59 | 2 FAIL | — | 80 (overall) |

**C17 Key Findings:**
- Miri cultural identity P0: surname "Okonkwo-Santos" (Igbo Nigerian/Pt-Brazilian) but chopstick MIRI-A reads as East Asian — cross-cultural error. Alex/Maya/Priya/Hana to resolve C43.
- No Miri+Luma rendered asset: Marcus Webb + Eleanor Whitfield both called this the primary gap (new style frame or key panel needed)
- Logo: 30 cycles of DejaVu Sans — P1 since C12/C13 (Sam: typography brief C43)
- Classroom chalkboard 34: no text, only rectangles — pixel font tool unused
- Hallway seal 38: school has no name after 20+ cycles (Jonas + Chiara C16)
- Petra FAIL 1: hardcoded absolute paths (8+ generators — Kai: project-root resolver)
- Petra FAIL 2: dual-generator SF01 conflict (Morgan: retire old generator)
- Leila: UV_PURPLE drifting toward 2010s dystopian palette (cyberpunk ≠ digital-sublime)
- Leila: GL-07 lamp halo in SF04 is most original narrative-visual idea — foreground it
- Petra WARN: SF04 generator in wrong output dir (Jordan fix); storyboard naming split (Morgan/Diego)

## C16 Critique Scores

| Asset | Daisuke | Priya | Sven | Chiara | Jayden |
|-------|---------|-------|------|--------|--------|
| SF01 | — | 74 | 76 | — | 78 |
| SF02 | — | 52 | 71 | — | 51 |
| SF03 | — | 57 | 59 | — | 82 |
| SF04 | — | 50 | 62 | P1 | 63 |
| Luma expr | 44 | — | — | — | 54 |
| Cosmo expr | 72 | — | — | — | — |
| Kitchen v005 | — | — | — | 76 | — |
| Cross-pitch coherence | — | 45 | — | — | — |

## Open Items for C43
**P0 — Requires Alex decision and broadcast:**
0. **Alex/Maya/Priya/Hana**: Miri cultural identity — resolve chopstick MIRI-A vs Okonkwo-Santos heritage conflict; document cultural framework for Miri, Luma, Millbrook

**P1 — Mandated (from C17 critique):**
1. **Jordan**: SF02 native canvas refactor (last 1920×1080+LANCZOS — 300+ lines, assign dedicated cycle)
2. **Jordan**: SF04 output directory fix (`output/style_frames/` → `output/color/style_frames/`)
3. **Kai**: Byte face test profile (`--char byte` — Diego blocked on face gate for panels)
4. **Kai**: Project-root resolver utility (Petra FAIL — 8+ generators hardcode absolute paths)
5. **Morgan**: Retire old SF01 generator + resolve dual-generator conflict (Petra FAIL)
6. **Sam**: Logo display typeface brief (30-cycle gap — DejaVu Sans)
7. **Hana/Diego**: Pixel font deployment — classroom chalkboard (text!), hallway seal (school name!), kitchen MIRI label migration
8. **Alex+team**: Miri+Luma shared-frame asset — new style frame or key relationship panel (Marcus + Eleanor)

**P1 — Carried from C42 ideabox:**
9. **Lee/Diego**: COVETOUS style frame execution (Rin's generator fixed, spec ready)
10. **Morgan**: Storyboard naming convention fix (coordinate with Diego)

**P2 — From C42 ideabox:**
11. **Kai**: `vp_spec_config.json` + VP003 CI check
12. **Morgan**: `--apply-stale-review` auto-close (ci_suite v1.3.0)
13. **Morgan/Jordan**: `# GLITCH-COLOR-IN-REAL-WORLD` sentinel + ci_suite INFORMATIONAL check
14. **Hana or Kai**: `LTG_TOOL_env_lighting_audit.py`
15. **Priya or Kai**: Dialogue register linter
16. **Maya**: Lineup tier depth indicator band
17. **Priya**: School name for Millbrook (for hallway seal + Diego's panels)

**C44 = Critique 18 (every 3 cycles)**

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

## Pipeline Standards
- Open source only: Python PIL + **numpy, OpenCV (cv2), PyTorch** (authorized C39 — Alex Chen broadcast)
- cv2 default is BGR — convert to RGB on load. Use PIL for drawing; numpy/cv2 for analysis.
- ΔE color distance threshold = 5.0 (LAB perceptual, replaces RGB Euclidean)
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]` — everything in output/tools/ uses LTG_TOOL_* prefix
- output/production/ files EXEMPT from LTG naming
- After img.paste(): always refresh draw = ImageDraw.Draw(img)
- show_guides=False for all pitch exports
- Python 3.8 compat: `from __future__ import annotations`
- REAL_INTERIOR warm/cool threshold = 12.0 (render_qa v2.0.0)

## Shared Library (updated C42)
`LTG_TOOL_render_lib.py` — **v1.2.0 C42** (Hana). `flatten_rgba_to_rgb()` helper added — correct Porter-Duff via Pillow alpha_composite
`LTG_TOOL_ci_suite.py` — **v1.2.0 C42** (Morgan). `--warn-stale N` flag; all 38 known-issue entries tagged `since_cycle: C39`
`LTG_TOOL_sobel_vp_detect.py` — **v1.0.0 NEW C42** (Kai). Sobel/HoughLines VP coordinate detection, `--vp-x-expected`/`--vp-y-expected` flags, debug overlay
`LTG_TOOL_sf_covetous_glitch.py` — **v2.0.0 C42** (Rin). G001/G004/G008 PASS; 3-char triangulation
`LTG_TOOL_motion_spec_lint.py` — **C42** (Ryo). Per-family `annotation_bg_color` in sheet_geometry_config.json; Luma/Cosmo annotation_occupancy WARN→PASS
`LTG_TOOL_bg_luma_study_interior.py` — **NEW C42** (Hana). 1280×720, warm/cool 33.1 PASS, 3 light sources
`LTG_TOOL_character_lineup.py` — **v008 C42** (Maya). Two-tier ground plane, Luma center, RPD PASS
`LTG_TOOL_sb_cold_open_P07.py` / `P09.py` — **NEW C42** (Diego). P07: Dutch 8° CW, Byte mid-phase; P09: CURIOUS/FIRST ENCOUNTER
`LTG_TOOL_sb_ep05_covetous.py` — **NEW C42** (Diego). 3-char triangulation storyboard panel

## Shared Library (historical C40)
`LTG_TOOL_render_qa.py` — **v2.0.0 C39**. numpy/cv2 LAB ΔE, comparison report CLI
`LTG_TOOL_precritique_qa.py` — **v2.8.0 C40**. arc_diff JSON config + LAB ΔE + Section 10 alpha_blend_lint (Morgan+Kai+Rin)
`LTG_TOOL_ci_suite.py` — **v1.1.0 C40**. `--known-issues` flag; `ci_known_issues.json` seeded (Morgan)
`LTG_TOOL_palette_warmth_lint.py` — **v6.0.0 C39**. numpy vectorized
`LTG_TOOL_spec_sync_ci.py` — **v1.1.0 C39**. Byte CI delegates to char_spec_lint (B001–B005)
`LTG_TOOL_luma_face_curves.py` — **v1.1.0 C40** (Kai). All 9 expressions, corrected 100px eye width
`LTG_TOOL_face_curve_validator.py` — **NEW C40** (Maya). Validates all 10 expressions; all PASS
`LTG_TOOL_sight_line_diagnostic.py` — **v002 C40** (Lee). `--batch config.json` mode
`LTG_TOOL_motion_spec_lint.py` — **C40** (Ryo). Per-family beat color config; Luma timing WARN→PASS
`LTG_TOOL_sf04_luma_byte_v005.py` — **NEW C40** (Jordan). SF04 generator; warm/cool 36.6
`LTG_TOOL_sf_covetous_glitch.py` — **NEW C40** (Rin). SF05 COVETOUS generator
`LTG_TOOL_bg_other_side.py` — **C40** (Rin). UV_PURPLE corrected to GL-04a
`LTG_TOOL_bg_tech_den.py` — **v005 C40** (Hana). VP floor fix, warm/cool 100.8 PASS
`LTG_TOOL_fill_light_adapter.py` — **v1.1.0 C39**. Scene registry loading
`LTG_fill_light_presets.json` — **NEW C39**. SF01–SF04 standard configs
`arc_diff_config.json` — **NEW C39**. External arc-diff pair config
`LTG_TOOL_alpha_blend_lint.py` — **NEW C39** (Rin). LAB gradient, FLAT_FILL detection
`LTG_TOOL_sight_line_diagnostic.py` — **NEW C39** (Lee). Eye→aim ray, perpendicular miss distance
`LTG_TOOL_pixel_font_v001.py` — **NEW C39** (Jordan). 5×7 bitmap A–Z/0–9, no font deps
`LTG_TOOL_thumbnail_preview_v001.py` — **NEW C39** (Hana). Full/thumbnail side-by-side with region bbox
`LTG_TOOL_bodypart_hierarchy.py` — **v002 C39** (Maya). --panel N, --chain pipeline
`LTG_TOOL_sheet_geometry_calibrate.py` — **NEW C39** (Ryo). Auto-detects panel top row
`sheet_geometry_config.json` — **NEW C39**. Luma panel_top=54, Byte panel_top=56
`LTG_TOOL_motion_spec_lint.py` — **C39** (Ryo). Config-loaded zone sampling
`LTG_TOOL_world_type_infer.py` — **NEW C38**. Standalone world-type inference
`LTG_TOOL_ci_suite.py` — C37 (suppression fix C38 via json)
`glitch_spec_suppressions.json` — **C38** (G002 docstring FP added)
`LTG_TOOL_luma_motion.py` / `LTG_TOOL_byte_motion.py` — C39 geo-config updated
`LTG_TOOL_pilot_cold_open.py` — C38 rename
`LTG_TOOL_contact_sheet_arc_diff.py` — C37
`LTG_TOOL_warmth_inject_hook.py` — C37
`LTG_TOOL_draw_order_lint.py` — v2.1.0 C37
`LTG_TOOL_glitch_spec_lint.py` — v1.2.0 C37
`LTG_TOOL_expression_silhouette.py` — C37
`LTG_TOOL_proportion_audit.py` — C36

## Agent Prompt Design
Do NOT duplicate inbox content in agent prompts. Prompts = role context + startup sequence only.

## Producer Responsibilities
- Ideabox: action worthy ideas → actioned/, rejects → rejected/ after each cycle.
- README.md: update after every work and critique cycle.
- Slot filling: launch next agent immediately on completion. Never exceed 8 simultaneous.
- New member onboarding: update MEMORY.md with catch-up section before first assignment.
