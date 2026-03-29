# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: all core assets present.

## Status
**Cycle 37 complete. Work cycles: 37. Critique cycles: 14 (Critique 15 just ran — see below).**
**Next critique at C40 (every 3 work cycles).**

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
| Diego Vargas | Storyboard Artist (joined C37) | Alex Chen |
| Priya Shah | Story & Script Developer (joined C37) | Alex Chen |
| Hana Okonkwo | Environment & Background Artist (joined C37) | Alex Chen |
| Ryo Hasegawa | Motion & Animation Concept Artist (joined C37) | Alex Chen |

**Agent scheduling:** Max 8 simultaneous. Launch next agent immediately when a slot opens. Dependency-blockers go first regardless of task size.

## Image Output Rule (MANDATORY)
**Hard limit: ≤ 1280px in both dimensions.** Use `img.thumbnail((1280,1280), Image.LANCZOS)` before saving.

## Critique Format
Score (0–100) → bullet issues (≤2 lines each) → single Bottom line. ≤15 lines per asset.

## Critics Panel (20 total)
- 15 industry professionals + 5 audience (Zoe Park age 11, Marcus Okafor parent, Jayden Torres age 13, Eleanor Whitfield grandparent, Taraji Coleman educator)
- **Rotate each cycle. Min 1 audience critic per critique cycle.**
- C14 critics: Daisuke, Priya N, Sven, Chiara, Nkechi
- C15 critics (just ran): Takeshi Mori, Ingrid Solberg, Reinhardt Böhm, Zoe Park, Taraji Coleman

## Pitch Package Status — POST CYCLE 37

### Style Frames
- **SF01 Discovery**: v005
- **SF02 Glitch Storm**: v008 (fill light fixed C36)
- **SF03 Other Side**: v005
- **SF04 Luma+Byte**: v004

### Logo
- **LTG_BRAND_logo_v001.png** — DECIDED C25

### Characters
- Luma: **expr v010 NEW C37** (THE NOTICING: center slot, stronger asymmetry, lip-touch gesture), turnaround v004, color model v002
- Byte: expr v005, turnaround v001, color model v001
- Cosmo: **expr v006 NEW C37** (glasses tilt fixed 10°→7°, CI PASS)
- Miri: expr v004
- Glitch: expr v003
- Character lineup: v007

### Environments
- Kitchen: v004
- Tech Den: v004_warminjected
- Glitch Layer: v003
- School Hallway: v002
- Millbrook Street: v002
- **Living Room: v001 NEW C37** (CRT focal point, QA PASS)

### New Asset Categories (C37)
- **Storyboards**: `output/storyboards/LTG_SB_pilot_cold_open_v001.png` (6-panel cold open)
- **Story**: `output/production/story/story_bible_v001.md` — pilot "Dead Pixels", full world rules, character voices
- **Motion**: `output/characters/motion/LTG_CHAR_luma_motion_v001.png`, `LTG_CHAR_byte_motion_v001.png`

## QA Baseline (C37)
precritique_qa v2.2.0: **333 PASS / 26 WARN / 0 FAIL**
CI suite: WARN (0 hard FAILs). SF03 warm/cool: PASS (render_qa v1.4.0).

## C37 Key Lessons
- **Story bible revealed**: Grandma Miri and Glitch Layer Miri share a name intentionally — season 1 finale seed. No visual plant yet. Alex flag pending.
- **Byte shape spec inconsistency**: production_bible.md still says triangles/jagged polygons. Canonical = oval. 1-line fix queued.
- **Glitch character narrative status**: The diamond-body "Glitch" in glitch.md has no narrative role in the story bible. Priya flagged to Alex.
- **THE NOTICING v010**: moved to center slot, stronger. Untested by critics — remains highest risk.
- **Motion secondary standards now canonical**: hoodie lag +0.5 beats, hair lag +1.0 beat, Byte hover 0.5Hz ±6px.
- **Hana's dual-temp split pass**: warm/cool QA for REAL interiors requires top-half warm overlay + bottom-half cool overlay BEFORE deep shadows. 5 iterations to tune.

## Open Items for C38
1. P4/P6 storyboard refinements (Diego, per Lee)
2. Grandma Miri / Glitch Layer Miri visual plant (Alex + Diego)
3. production_bible.md Byte shape fix (Priya or Alex — 1 line)
4. Glitch character narrative role clarification (Priya + Alex)
5. SF01 warm/cool near-miss 17.8/20.0 → REAL_INTERIOR threshold fix (Sam + Kai)
6. All 12 C37 ideabox ideas queued C38

## Known Open Items (Carry-Forward)
- Luma THE NOTICING: critics have scored 52-58 for 4+ cycles. v010 is the strongest attempt yet.
- SF01 warm/cool: 17.8/20.0 — near-miss, REAL_INTERIOR threshold (12) would clear it.

## Canonical Palette
- Byte body = GL-01b #00D4E8 BYTE_TEAL (NOT #00F0FF)
- CORRUPT_AMBER = GL-07 #FF8C00
- HOT_MAGENTA = GL-02 #FF2D6B
- UV_PURPLE = #7B2FBE
- CHAR-L-11 = #00F0FF Electric Cyan
- SF03: zero warm light; Classroom: zero Glitch palette
- Byte shape = OVAL (NOT triangles — retired C8)
- Cosmo glasses = 7° tilt ±2°

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
- Open source only: Python PIL
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`
- output/production/ files EXEMPT from LTG naming
- After img.paste(): always refresh draw = ImageDraw.Draw(img)
- show_guides=False for all pitch exports
- Python 3.8 compat: `from __future__ import annotations`

## Shared Library (updated C37)
`LTG_TOOL_render_qa_v001.py` — **v1.4.0 C37**. World-type-aware thresholds
`LTG_TOOL_ci_suite_v001.py` — **C37**. All 5 CI checks in one command
`LTG_TOOL_contact_sheet_arc_diff_v001.py` — **C37**. Panel-level diff for expression sheets
`LTG_TOOL_warmth_inject_hook_v001.py` — **C37**. Shared hook module for env generators
`LTG_TOOL_draw_order_lint_v002.py` — **v2.1.0 C37**. Back-pose suppression
`LTG_TOOL_glitch_spec_lint_v001.py` — **v1.2.0 C37**. 26 FPs suppressed
`glitch_spec_suppressions.json` — **C37**
`LTG_TOOL_expression_silhouette_v003.py` — **C37**. --output-zones flag added
`LTG_TOOL_sf02_fill_light_fix_c35.py` — **C37**. Resolution-independent (canvas_w/canvas_h)
`LTG_TOOL_precritique_qa_v001.py` — **v2.2.0 C37**
`LTG_TOOL_spec_sync_ci_v001.py` — C36
`LTG_TOOL_palette_warmth_lint_v004.py` — C36
`LTG_TOOL_warmth_inject_v001.py` — C36
`LTG_TOOL_proportion_audit_v002.py` — C36
`LTG_TOOL_procedural_draw_v001.py` — v1.5.0
`LTG_TOOL_character_face_test_v001.py` — C35

## Agent Prompt Design
Do NOT duplicate inbox content in agent prompts. Prompts = role context + startup sequence only.

## Producer Responsibilities
- Ideabox: action worthy ideas → actioned/, rejects → rejected/ after each cycle.
- README.md: update after every work and critique cycle.
- Slot filling: launch next agent immediately on completion. Dependency-blockers queue first.
- New member onboarding: update MEMORY.md with catch-up section before first assignment.
