# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: all core assets present.

## Status
**Cycle 36 complete. Work cycles: 36. Critique cycles: 14.**
**Next critique at C37 (critique every 3 work cycles — C37 IS a critique cycle).**

## Active Team (12 slots — expanded C37)

| Member | Role | Reports To |
|--------|------|-----------|
| Alex Chen | Art Director | — |
| Maya Santos | Character Designer | Alex Chen |
| Sam Kowalski | Color & Style Artist | Alex Chen |
| Kai Nakamura | Tech Art Engineer | Alex Chen |
| Rin Yamamoto | Visual Stylization Artist (from C23) | Alex Chen |
| Jordan Reed | Style Frame Art Specialist (reactivated C34) | Alex Chen |
| Lee Tanaka | Character Staging & Visual Acting Specialist (reactivated C34) | Alex Chen |
| Morgan Walsh | Pipeline Automation Specialist (new C34) | Alex Chen |
| Diego Vargas | Storyboard Artist (new C37) | Alex Chen |
| Priya Shah | Story & Script Developer (new C37) | Alex Chen |
| Hana Okonkwo | Environment & Background Artist (new C37) | Alex Chen |
| Ryo Hasegawa | Motion & Animation Concept Artist (new C37) | Alex Chen |

**Agent scheduling:** Max 8 simultaneous agents. 12 members → 2 batches per cycle. Longest-running tasks start first.

## Image Output Rule (MANDATORY)
**Hard limit: ≤ 1280px in both dimensions.** Use `img.thumbnail((1280,1280), Image.LANCZOS)` before saving. QA pipeline (v1.2.0) now auto-downscales before checks.

## Image Handling Policy (all agents)
Before sending any image to Claude: prefer tools; downscale if lower-res suffices; never send high-res unnecessarily. Vision limits: hallucination on tiny/rotated images; limited spatial reasoning; approximate counting. Rule in CLAUDE.md.

## Critique Format
Critics use: Score (0–100) → bullet issues (≤2 lines each) → single Bottom line sentence. ≤15 lines per asset. Rule in CLAUDE.md.

## Critics Panel (20 total)
- 15 industry professionals (Takeshi, Ingrid, Daisuke, Priya N, Marcus W, Chiara, Samuel, Yuki, Reinhardt, Amara, Jonas, Leila, Sven, Nkechi, Petra)
- 5 audience members (Zoe Park age 11, Marcus Okafor parent, Jayden Torres age 13, Eleanor Whitfield grandparent, Taraji Coleman educator) — added C36
- **Rotate critics each cycle. Min 1 audience critic per critique cycle. All 20 get roughly equal rotation.**

## Pitch Package Status — POST CYCLE 36

### Style Frames
- **SF01 Discovery**: v005 (unchanged)
- **SF02 Glitch Storm**: **v008 NEW C36** (upper-right fill light, per-char silhouette mask — Sven P1 resolved)
- **SF03 Other Side**: v005 (unchanged)
- **SF04 Luma+Byte**: v004 (unchanged)

### Logo
- **LTG_BRAND_logo_v001.png** — DECIDED C25

### Characters
- Luma: expr v009, turnaround v004, color model v002
- Byte: expr v005, turnaround v001, color model v001
- Cosmo: expr v005 **P1 FAIL: glasses tilt 10° vs spec 7°±2 → Maya C37 (v006)**
- Miri: expr v004
- Glitch: expr v003 (body ratio fixed C35)
- Character lineup: v007

### Environments
- Kitchen: v004
- Tech Den: **v004_warminjected NEW C36** (warm/cool 7.9→23.2 PASS)
- Glitch Layer: v003
- School Hallway: v002
- Millbrook Street: v002

## QA Baseline (C36)
precritique_qa v2.1.0: **321 PASS / 37 WARN / 0 FAIL**
Delta vs C35: +0 FAIL, +1 WARN (SF02 v008 G007 — known pattern), -0 resolved

## Critical Bug Fixed C34 — add_rim_light() Canvas Flood
`edge_mask.convert("RGBA")` set alpha=255 everywhere. Fixed: use edge_mask directly as alpha channel.

## C36 Key Lessons
- **RPD metric**: IoM was mathematically broken for standing humans (subset geometry bias). v003 Regional Pose Delta = column-projection Pearson correlation per zone. Works correctly.
- **Jordan's fill light module hardcoded to 1280×720**: PIL failures on other resolutions. Rin inlined. Fix actioned C37 (canvas_w/canvas_h params).
- **Tech Den warmth**: needed cool-bottom injection, not warm-top — top was already amber. warmth_inject now auto-detects correct injection direction.
- **Cosmo P1**: glasses tilt 10° vs spec 7°±2. Caught by spec_sync_ci first run. Maya C37.
- **Audience critics added**: 5 real-people critics (target audience). CLAUDE.md: min 1 per critique cycle. Guard artistic integrity — don't chase approval.

## Open Items for C37
1. **Cosmo v006**: glasses tilt fix (Maya) — P1 CI FAIL
2. **RPD zone visualization** --output-zones flag (Maya)
3. **Fill light resolution adapter**: canvas_w/canvas_h params (Rin)
4. **Glitch spec suppression list**: `glitch_spec_suppressions.json` (Kai)
5. **Draw order back-pose suppression**: `# LINT: back_pose` block comment (Kai)
6. **Warmth inject generator hook**: --check-warmth flag in env generators (Jordan/Hana)
7. **CI suite consolidation**: `LTG_TOOL_ci_suite_v001.py` (Kai)
8. **Contact sheet arc-diff tool** (Lee)
9. **World-type inference in render_qa** (Kai/Sam)
10. **New members onboarding** (C37 first cycle): Diego (storyboards), Priya (story bible), Hana (environments), Ryo (motion specs)
11. **Luma "THE NOTICING" still scoring 52-58**: C37 priority for Maya

## C36 Ideabox — All 8 Actioned → C37
Morgan: glitch spec suppression | Alex: draw order back-pose | Jordan: warmth inject hook | Kai: CI suite | Lee: contact sheet arc-diff | Maya: RPD zone viz | Rin: fill light adapter | Sam: world-type render_qa

## Warm/cool QA (C35 lesson, still valid)
Warmth metric measures TOP vs BOTTOM half hue — per-world presets in warmth_lint_config.json. SF03/SF04 near-zero warm ratio is CORRECT. v004 adds --world-type flag + auto-inference.

## Known False Positives (qa_false_positives.md)
- SUNLIT_AMBER drift in SF04: skin-tone overlap + compositing artifact. No fix.
- UV_PURPLE anti-aliasing WARNs: expected on all Glitch Layer assets.
- G007 on SF02: expected pattern on all SF02 versions.

## Canonical Palette Reminders
- Byte body = GL-01b #00D4E8 BYTE_TEAL (NOT #00F0FF)
- CORRUPT_AMBER = GL-07 #FF8C00 (255,140,0)
- HOT_MAGENTA = GL-02 #FF2D6B (NOT #FF0090)
- UV_PURPLE = #7B2FBE (verify in master_palette.md)
- GL-06c STORM_CONFETTI_BLUE = #0A4F8C
- CHAR-L-11 Constraint 1 = #00F0FF Electric Cyan (fixed C30)
- SF03: zero warm light; Classroom: zero Glitch palette

## Key Output Locations
- Style Frames: `output/color/style_frames/`
- Characters: `output/characters/main/`, color models: `output/characters/color_models/`
- Motion Specs: `output/characters/motion/` (new C37)
- Environments: `output/backgrounds/environments/`
- Storyboards: `output/storyboards/` (new C37)
- Story/Script: `output/production/story/` (new C37)
- Tools: `output/tools/` (legacy → `output/tools/legacy/`)
- Master Palette: `output/color/palettes/master_palette.md`
- Pitch Package Index: `output/production/pitch_package_index.md`

## Pipeline Standards
- Open source only: Python PIL
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`
- Categories: CHAR, ENV, COLOR, SB, TOOL, BRAND
- output/production/ files EXEMPT from LTG naming
- After img.paste(): always refresh draw = ImageDraw.Draw(img)
- show_guides=False for all pitch exports
- Python 3.8 compat: use `from __future__ import annotations` + `typing` module imports

## Shared Library (updated C36)
`LTG_TOOL_precritique_qa_v001.py` — **v2.1.0 C36**. Delta report (Section 0), baseline persistence, README sync prominence
`LTG_TOOL_expression_silhouette_v003.py` — **C36**. RPD metric replaces IoM; arms mode fixed
`LTG_TOOL_spec_sync_ci_v001.py` — **C36**. CI gate all 5 chars; C36 baseline: Cosmo P1 FAIL
`LTG_TOOL_palette_warmth_lint_v004.py` — **C36**. --world-type flag, CHAR-L expansion, auto-inference
`LTG_TOOL_warmth_inject_v001.py` — **C36**. Env warm/cool injection utility
`LTG_TOOL_proportion_audit_v002.py` — **C36**. Asymmetric eye detection
`ltg_warmth_guarantees.json` — **C36**. Primary warmth config (CHAR-M + CHAR-L hoodie)
`LTG_TOOL_procedural_draw_v001.py` (v1.5.0)
`LTG_TOOL_render_qa_v001.py` — v1.3.0
`LTG_TOOL_character_face_test_v001.py` — C35. Mandatory gate in 4 ROLE.md files
`LTG_TOOL_spec_extractor_v001.py` — C35
`LTG_TOOL_char_spec_lint_v001.py` — C34
`LTG_TOOL_draw_order_lint_v002.py` — C34. Scope-aware W004
`LTG_TOOL_expression_silhouette_v002.py` — C34 (superseded by v003)

## Agent Prompt Design
Do NOT duplicate inbox message content in agent prompts. Prompts = role context + startup sequence. Task detail belongs in inbox only.

## Producer Responsibilities
- **Ideabox review**: after each cycle, action worthy ideas → actioned/, rejects → rejected/.
- **README.md**: update after every work and critique cycle.
- **Batch ordering**: longest-running agents start first in each batch.
- **New member onboarding**: update MEMORY.md with catch-up section before first assignment.
