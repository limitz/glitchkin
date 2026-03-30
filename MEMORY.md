# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: all core assets present.

## Status
**Cycle 38 complete. Critique 15 complete. Work cycles: 38. Critique cycles: 15.**
**Next critique at C39 (every 3 work cycles — C39 is the cycle).**

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
- C16 candidates: Daisuke, Priya N, Sven, Chiara, Nkechi (+ 1 audience not from C15)

## Pitch Package Status — POST CYCLE 38

### Style Frames
- **SF01 Discovery**: v006 (sight-line fixed, gaze on Byte, reaching palm, DOUBT VARIANT brow)
- **SF02 Glitch Storm**: v008
- **SF03 Other Side**: v005
- **SF04 Luma+Byte**: v004

### Logo
- **LTG_BRAND_logo.png** — DECIDED C25

### Characters
- Luma: **expr v011 NEW C38** (right eye squint fixed top-lid-drops, DOUBT VARIANT slot 7, chin-forward thrust), turnaround v004, color model v002
- Byte: **expr v006 NEW C38** (silhouette gate run, RPD fixed), turnaround v001, color model v001
- Cosmo: **expr v007 NEW C38** (SKEPTICAL arm geometry fixed)
- Miri: **expr v004 regenerated C38** (CHAR-M-11 slipper color corrected #5A7A5A→#C4907A)
- Glitch: expr v003
- Character lineup: v007

### Environments
- Kitchen: v004 (v005 Dual-Miri plant queued C39)
- Tech Den: v004_warminjected
- Glitch Layer: v003
- **School Hallway: v003 NEW C38** (figure-ground fix — locker vs Cosmo cardigan)
- Millbrook Street: v002
- Living Room: v001

### Storyboards
- **Cold Open: v002 NEW C38** (hoodie orange, W004 fixed, P4/P6 staging improved)
- Canon: Night/Grandma's den. School/daytime = pre-credits Act 1 tag.

### Story
- **Story Bible: v002 NEW C38** (social world: Dev Patel-Huang + Preethi Okafor, Luma doubt arc, Byte non-verbal finale)
- Cold open pending v003 (canon now decided — night/den)
- Glitch role: Corruption's avatar (decided C38)

### Motion
- **Luma motion: v002 NEW C38** (CG polygon fix, shoulder mass, hair annotation)
- **Byte motion: v002 NEW C38** (crack scar side, glow radius annotated)

## QA Baseline (C38)
precritique_qa v2.3.0: **343 PASS / 38 WARN / 0 FAIL**
CI suite: PASS (suppression fix resolved G002 false positive).
SF01 warm/cool: PASS (17.8 > REAL_INTERIOR threshold 12.0).

## C38 Key Decisions
- **Cold open canon**: night/Grandma's den (Diego's storyboard). School/daytime = Act 1 pre-credits tag.
- **Glitch character**: Corruption's avatar — named Glitchkin consumed by the Corruption. Personal Byte backstory.
- **Dual-Miri plant**: handwritten "MIRI" fridge label in Kitchen v004→v005 (Jordan to execute C39).

## Open Items for C39
1. Diego: P01 neighborhood context, P12 two-shot reframe, P13 Luma/Byte mirror composition (unblocked)
2. Priya: story_bible v003 (cold open night/den + Glitch = Corruption's avatar)
3. Jordan: Kitchen v004→v005 Dual-Miri fridge label
4. Morgan: Re-run CI suite post-Kai fixes to confirm clean result
5. SF02 warm/cool still WARN (sep=6.5, storm scene, threshold ~3 needed)
6. All 13 C38 ideabox ideas queued C39 (costume-bg clash lint, sight-line check, CG polygon lint, brow-diff QA, docstring stripping, CI --known-issues, palette drift hook, etc.)
7. `my_idea_1.md` (unattributed): body-part color-index hierarchy tool for eye-inside-hair detection

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
- Open source only: Python PIL (no numpy in active tools)
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]` — everything in output/tools/ uses LTG_TOOL_* prefix
- output/production/ files EXEMPT from LTG naming
- After img.paste(): always refresh draw = ImageDraw.Draw(img)
- show_guides=False for all pitch exports
- Python 3.8 compat: `from __future__ import annotations`
- REAL_INTERIOR warm/cool threshold = 12.0 (render_qa v1.5.0)

## Shared Library (updated C38)
`LTG_TOOL_render_qa.py` — **v1.5.0 C38**. REAL_INTERIOR threshold 12.0
`LTG_TOOL_precritique_qa.py` — **v2.3.0 C38**
`LTG_TOOL_world_type_infer.py` — **NEW C38**. Standalone world-type inference
`LTG_TOOL_ci_suite.py` — C37 (suppression fix C38 via json)
`LTG_TOOL_spec_sync_ci.py` — C38 (G002 suppression added)
`glitch_spec_suppressions.json` — **C38** (G002 docstring FP added)
`LTG_TOOL_luma_motion.py` / `LTG_TOOL_byte_motion.py` / `LTG_TOOL_pilot_cold_open.py` — renamed from CHAR/SB prefixes C38
`LTG_TOOL_contact_sheet_arc_diff.py` — C37
`LTG_TOOL_warmth_inject_hook.py` — C37
`LTG_TOOL_draw_order_lint.py` — v2.1.0 C37
`LTG_TOOL_glitch_spec_lint.py` — v1.2.0 C37
`LTG_TOOL_expression_silhouette.py` — C37
`LTG_TOOL_sf02_fill_light_fix_c35.py` — C37
`LTG_TOOL_proportion_audit.py` — C36

## Agent Prompt Design
Do NOT duplicate inbox content in agent prompts. Prompts = role context + startup sequence only.

## Producer Responsibilities
- Ideabox: action worthy ideas → actioned/, rejects → rejected/ after each cycle.
- README.md: update after every work and critique cycle.
- Slot filling: launch next agent immediately on completion. Never exceed 8 simultaneous.
- New member onboarding: update MEMORY.md with catch-up section before first assignment.
