# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: all core assets present.

## Status
**Cycle 34 complete. Work cycles: 34. Critique cycles: 13.**
**Critique 14 complete. Work cycles: 34. Critique cycles: 14.**
**Cycle 35 starts next.**

## Active Team (8 slots — expanded C34)

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

**Cost discipline:** Morgan's mandate is tool-first QA. Max 8 agents simultaneous.

## Image Output Rule (MANDATORY)
**Hard limit: ≤ 1280px in both dimensions.** Use `img.thumbnail((1280,1280), Image.LANCZOS)` before saving. QA pipeline (v1.2.0) now auto-downscales before checks.

## Image Handling Policy (all agents)
Before sending any image to Claude: prefer tools; downscale if lower-res suffices; never send high-res unnecessarily. Vision limits: hallucination on tiny/rotated images; limited spatial reasoning; approximate counting. Rule in CLAUDE.md.

## Critique Format
Critics use: Score (0–100) → bullet issues (≤2 lines each) → single Bottom line sentence. ≤15 lines per asset. Rule in CLAUDE.md.

## Pitch Package Status — POST CYCLE 34

### Style Frames
- **SF01 Discovery**: v005 (rim_light bug fixed C34 — was flooding ELEC_CYAN)
- **SF02 Glitch Storm**: **v006 NEW C34** (HOT_MAGENTA fill light + ELEC_CYAN specular on Luma; Jordan Reed)
- **SF03 Other Side**: v005 (Luma = intentional pixel-art silhouette; unchanged)
- **SF04 Luma+Byte**: v004 (rim_light bug fixed C34 — was flooding warm amber)

### Logo
- **LTG_BRAND_logo_v001.png** — DECIDED C25

### Characters
- Luma: **expr v009 NEW C34** (eye-width 22px=HR×0.22, pose vocabulary for silhouette differentiation), turnaround v004, color model v002
- Byte: expr v005 (UNGUARDED WARMTH), turnaround v001, color model v001
- Cosmo: expr v004, turnaround v002, color model v001
- Miri: expr v003 (KNOWING STILLNESS), turnaround v001
- Glitch: expr v003 (YEARNING/COVETOUS/HOLLOW), turnaround v002, color model v001
- Character lineup: v007 (unchanged)

### Environments
All complete (Kitchen, Tech Den, Glitch Layer, School Hallway, Millbrook Street)

## Critical Bug Fixed C34 — add_rim_light() Canvas Flood
`edge_mask.convert("RGBA")` set alpha=255 everywhere (not edge mask value), flooding entire canvas with rim color. Fixed: use edge_mask directly as alpha channel. Affected SF01 v004/v005, SF02 v006, SF04 v004 — all regenerated.

## Critique 14 — Key Findings (C35 priorities)

### P1 — Blockers
- **Luma has NO FACE in SF02** (3rd cycle): `_draw_luma()` in v006 identical to v005. Lee's staging brief exists and was never implemented. P0. → Rin implements `_draw_luma_face_sprint()`, Jordan reviews
- **Cosmo v005 + Miri v004**: C34 pose brief existed; neither sheet was touched. Cosmo=34, Miri=38. → Maya P1
- **Glitch G002**: all generators produce body wider than tall (opposite of spec) → Kai
- **Warm/cool separation systemic failure**: SF01=17.9, SF02=6.5, SF03=3.1, SF04=1.1 (threshold=20). Design system problem → Alex to decide: calibrate metric or fix frames
- **Kitchen v003 + Hallway v002 need rebuilds**: Chiara flagged both as "does not belong" (12 cycles of character evolution not touching them). School Hallway perspective bug fixed by Producer (t**0.6 → t**2 across 4 perspective calculations). → Jordan (Kitchen rebuild), Rin or Jordan (Hallway rebuild)

### P2
- SF02 fill light direction wrong: bounce applies lower-left but storm crack is upper-right
- SF02 get_char_bbox multi-char bug: bbox spans 83% canvas (3 chars), meaningless char_cx for rim light
- SUNLIT_AMBER drift in SF04: 15.7° hue drift (Nkechi) — Art Director call needed
- Luma THE NOTICING still not landing to critic satisfaction (v009=52-58/100)
- Glitch Layer has no HOT_MAGENTA — emotional fissures absent from Glitch's world

### C14 Scores
- Daisuke: Luma v009=52, Cosmo=34, Miri=38, Byte=68, Glitch=82, Lineup=61
- Priya: SF02=44, SF01=71, SF03=58, SF04=62, cross-pitch=38
- Sven: SF02=44, SF01=72, SF03=61, SF04=74
- Chiara: Kitchen=58, TechDen=62, GlitchLayer=74, Street=71, Hallway=55
- Nkechi: Luma=58, SF02=72, SF04=65, Overall=68

## Known Open Items for C35
1. SF02 v007: Luma face (Rin + Lee + Jordan)
2. Cosmo v005 + Miri v004 (Maya)
3. Glitch G002 fix (Kai)
4. Warm/cool system decision (Alex + Sam)
5. Kitchen v004 rebuild (Jordan)
6. Hallway v003 rebuild (Jordan or Rin) — perspective fixed, SUNLIT_AMBER/scale remain
7. 35 unlisted README tools + value ceiling guard tool (Morgan)

## Ideabox — C30 (5 ideas, all filed)
- Alex: proportion verifier tool (actioned → Kai C31)
- Maya: character diff tool
- Sam: color verify gradient/histogram mode
- Kai: draw order linter
- Rin: proportion audit tool (SF generators)
**Theme:** team converged independently on automation to remove manual QA inspection

## Cycle 31 — Completed (Ideabox Implementation)

### Alex Chen
- LTG_TOOL_proportion_verify_v001.py built; pitch index updated; all 6 ideabox ideas actioned

### Kai Nakamura
- LTG_TOOL_draw_order_lint_v001.py: 59 PASS / 55 WARN (W004 = missing draw refresh, 55 files)
- LTG_TOOL_color_verify_v002.py: hue histogram mode added; all v001 API preserved

### Maya Santos
- LTG_TOOL_char_diff_v001.py: proportion diff tool; best used on turnaround FRONT panels

### Rin Yamamoto
- LTG_TOOL_proportion_audit_v001.py: SF01 v004 PASS (ew=0.22); SF04 unauditable (stubs)

### Sam Kowalski
- QA run: 3 PASS / 9 WARN / 0 FAIL on 12 pitch assets; color_statement_critique13.md written
- New ideabox idea: QA false-positive registry (FP-DOCUMENTED annotations)

## Cycle 30 — Completed

### Alex Chen
- pitch_audit_cycle30.md; C30+C31 directives sent

### Maya Santos
- Luma color model v002 (eye width fixed HR×0.22); critique13_precheck written; character_sheet_standards updated

### Sam Kowalski
- master_palette.md CHAR-L-11 fix (C14 copy-error: #00D4E8→#00F0FF); color story SF01 ref updated; full color audit; all 4 SFs PASS

### Kai Nakamura
- render_qa_v001.py → v1.2.0 (auto-downscale); README + pitch index updated; draw order audit PASS

### Rin Yamamoto
- SF01 v004 eye width fixed (HR×0.25→HR×0.22); heights confirmed 3.2 heads; SF02/SF03 checked

## Shared Library
`LTG_TOOL_render_lib_v001.py` (v1.1.0)
`LTG_TOOL_color_verify_v001.py` — use v002 for new work
`LTG_TOOL_color_verify_v002.py` — C31. Adds hue histogram mode (--histogram)
`LTG_TOOL_render_qa_v001.py` (v1.2.0 — C30. Auto-downscale before QA)
`LTG_TOOL_procedural_draw_v001.py` (v1.2.0 — rim light side param, face lighting)
`LTG_TOOL_proportion_verify_v001.py` — C31. PNG-based head/body ratio check
`LTG_TOOL_proportion_audit_v001.py` — C31. Scans SF generators for ew/HR constants
`LTG_TOOL_char_diff_v001.py` — C31. Pixel-sampling proportion diff between two PNGs
`LTG_TOOL_draw_order_lint_v001.py` — C31. Static draw-order linter (55 W004s in older generators)
`LTG_TOOL_naming_cleanup_v001.py` — executed C29 (22 files deleted)

## Cycle 32 — Completed

### Alex Chen
- Eye-width canon: `ew = int(head_r * 0.22)`, head_r = RADIUS. Avoid `h`. Documented in character_sheet_standards + luma.md.
- luma.md: 3.5→3.2 heads, all canonical proportions documented
- SF04 Byte teal: accepted as SCENE-LIGHTING

### Maya Santos
- Luma expr v008: THE NOTICING (chin-touch, asymmetric eyes, zero tilt — distinct silhouette)
- glitch.md: full 11-section diamond construction spec

### Sam Kowalski
- CHAR-L-11 cross-ref fixed; CHAR-M-11 Miri slippers → warm #C4907A; DRW-18 warmth clarified
- Color story SF03 Key Color Tension corrected

### Rin Yamamoto
- procedural_draw v1.3.0: add_rim_light() char_cx param (character-relative side mask)
- SF01 v005: char_cx fix applied
- SF04 rebuilt: value ceiling 255 (was 198/FAIL), monitor contribution, canonical specs
- Luma turnaround v004: ew = int(head_r * 0.22) across all views

### Kai Nakamura
- 8 broken forwarding stubs fixed (imported deleted LTG_CHAR_* files)
- Cosmo v004 generator fixed (correct filename + SURPRISED blush)
- W004: most warnings are linter false positives — scope-aware linter needed (ideabox)

## Critique 13 — Key Findings (C32 priorities)

### P1 — Blockers
- **Eye-width semantic mismatch**: `h`=head-radius in v007 (ew=22px) vs `h`=head-height in turnaround v003 (ew=84px) — 3.8× discrepancy. Must canonize one definition across ALL docs/generators (Alex + Maya + Rin)
- **Broken forwarding stubs**: C29 cleanup deleted LTG_CHAR_* originals; C28 stubs import from them → ModuleNotFoundError on 8+ generators (Kai)
- **luma.md says 3.5 heads**: contradicts v007 3.2 canon (Alex — 1-line fix)
- **add_rim_light() canvas-midpoint bug**: side="right" uses x>0.50W, excludes left-of-center characters; fix to character-relative bounding box (Rin → v1.3.0)
- **SF04 generator rebuild**: value ceiling 198 (FAIL), stubs only, silhouette broken (Rin)
- **CHAR-L-11 cross-ref hex**: still cites #00D4E8; must be #00F0FF (Sam — 1-line fix)
- **Luma signature expression**: v008 needed — "noticing" face, the central pitch promise (Maya)
- **Glitch diamond construction spec**: 2 consecutive critiques, still not written (Maya)

### P2
- Byte shadow color in lineup: 2 cycles unresolved
- Byte unguarded warmth state missing from expr sheet
- SF02 Luma interiority during sprint absent (C+)
- CHAR-M-11 Miri slippers contradict warm-palette guarantee
- Glitch has no spec file
- Cosmo v004 generator outputs wrong filename
- SF02 characters: no magenta fill light / no cyan specular
- 55 W004 lint warnings (missing draw refresh) unaddressed
- Luma v007 body proportion actually 3.12 heads due to neck segment

### Critic Scores (C13)
- Daisuke: Luma expr v007=62, turnaround=71, lineup=74, color model=80, Glitch expr=72
- Priya: palette=82, SF01=84, SF02=78, SF03=76, SF04=68, color story=87
- Sven: SF01=72, SF02=68, SF03=81, SF04=52
- Reinhardt: 64 (up from FAIL — conditional)
- Nkechi: B overall (up from B-)

## Producer Responsibilities
- **Ideabox review**: after each cycle, producer reviews ideabox/, actions worthy ideas → actioned/, rejects → rejected/.
- **README.md**: update after every work and critique cycle — latest asset versions, team roster, progress counters. Never touch the intro text.
- **Agent prompts**: do NOT duplicate inbox content. Prompts = role context + startup sequence only.

## Agent Prompt Design (C32 lesson)
Do NOT duplicate inbox message content in agent prompts. The inbox message IS the assignment. Agent prompts should only contain: role context, startup sequence (read CLAUDE.md, PROFILE.md, MEMORY.md, tools/README.md, then inbox). Task detail belongs in the inbox only — duplication causes drift.

## Technical Debt
- **SF04 source generators missing**: proportion audit impossible; stubs only on disk
- **W004 warnings**: largely false positives per Kai C32 investigation; scope-aware linter queued C34

## Canonical Palette Reminders
- Byte body = GL-01b #00D4E8 BYTE_TEAL (NOT #00F0FF)
- CORRUPT_AMBER = GL-07 #FF8C00 (255,140,0)
- HOT_MAGENTA = GL-02 #FF2D6B (NOT #FF0090)
- UV_PURPLE = #7B2FBE (verify in master_palette.md)
- GL-06c STORM_CONFETTI_BLUE = #0A4F8C
- CHAR-L-11 Constraint 1 = #00F0FF Electric Cyan (fixed C30 — was #00D4E8)
- SF03: zero warm light; Classroom: zero Glitch palette

## Key Output Locations
- Style Frames: `output/color/style_frames/`
- Characters: `output/characters/main/`, color models: `output/characters/color_models/`
- Environments: `output/backgrounds/environments/`
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
- Python 3.8 compat: use `from __future__ import annotations` + `typing` module imports (no `list[str]` subscript)

## Cycle 33 — Completed (Ideabox Implementation Round 2)

### Alex Chen
- Character lineup v007: Byte shadow GL-01a fix (#00A8B4), Miri slipper warm fix (#C4907A)
- Byte expr v005 directive sent to Maya (UNGUARDED WARMTH)
- Pitch package index updated through C32
- Ideabox: lineup palette audit tool proposal

### Maya Santos
- LTG_TOOL_expression_silhouette_v001.py: silhouette differentiation test; combined IoM+XOR metric; auto-detects grid; dark-BG support
- Miri expr v003 rebuilt properly (was broken stub); KNOWING STILLNESS 6th expression
- Byte expr v005: UNGUARDED WARMTH (star+heart eyes, gold confetti, body leaning in)
- C33 baseline: all human chars FAIL at 85% threshold — design problem, not tool problem

### Sam Kowalski
- LTG_TOOL_palette_warmth_lint_v001.py: warm-channel compliance check for CHAR-M; 0 violations C33 baseline
- SF04 Byte teal exception formally documented in master_palette.md

### Kai Nakamura
- LTG_TOOL_stub_linter_v001.py: scans for broken LTG_CHAR_*/LTG_COLOR_* imports; --pre-commit CI flag
- LTG_TOOL_glitch_spec_lint_v001.py: G001–G008 checks against glitch.md; SKIP non-Glitch files

### Rin Yamamoto
- procedural_draw v1.4.0: get_char_bbox(img, threshold) utility added
- SF02/SF03 audit: neither calls add_rim_light() — both draw lighting as direct geometry; no latent bugs

## Ideabox — C33 (5 ideas, all actioned → C34)
- Rin: scene_snapshot() diagnostic crop utility
- Kai: general char spec linter framework (all characters, not just Glitch)
- Sam: warmth lint scope expansion (configurable prefix list via JSON)
- Alex: lineup palette audit tool
- Maya: expression silhouette --mode arms (regional similarity)

## Shared Library (updated C34)
`LTG_TOOL_procedural_draw_v001.py` (**v1.5.0** — scene_snapshot() added; add_rim_light() flood bug fixed C34)
`LTG_TOOL_expression_silhouette_v002.py` — C34. Adds --mode arms (arm/shoulder region comparison)
`LTG_TOOL_palette_warmth_lint_v002.py` — C34. Configurable prefix list via warmth_lint_config.json
`LTG_TOOL_char_spec_lint_v001.py` — C34. General spec linter (Luma/Cosmo/Miri; 5 checks each)
`LTG_TOOL_draw_order_lint_v002.py` — C34. Scope-aware W004; 147→69 warnings (53% FP reduction)
`LTG_TOOL_lineup_palette_audit_v001.py` — C34. Verifies lineup PNG body colors vs master_palette.md
`LTG_TOOL_precritique_qa_v001.py` — C34. Chains 6 QA tools; consolidated Markdown report
`LTG_TOOL_expression_silhouette_v001.py` — C33. (superseded by v002 for new work)
`LTG_TOOL_stub_linter_v001.py` — C33. Broken import scanner; --pre-commit flag
`LTG_TOOL_glitch_spec_lint_v001.py` — C33. Glitchkin generator validator (G001–G008)
`LTG_TOOL_palette_warmth_lint_v001.py` — C33. (superseded by v002)
