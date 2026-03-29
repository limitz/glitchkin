# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: all core assets present.

## Status
**Cycle 32 complete. Work cycles: 32. Critique cycles: 13.**
**Cycle 33 starts next. Critique 14 after Cycle 34.**

## Active Team (all 5 slots used)

| Member | Role | Reports To |
|--------|------|-----------|
| Alex Chen | Art Director | — |
| Maya Santos | Character Designer | Alex Chen |
| Sam Kowalski | Color & Style Artist | Alex Chen |
| Kai Nakamura | Tech Art Engineer | Alex Chen |
| Rin Yamamoto | Visual Stylization Artist (from C23) | Alex Chen |

**Inactive:** Jordan Reed (environments complete C22), Lee Tanaka (storyboard complete C21)

## Image Output Rule (MANDATORY)
**Hard limit: ≤ 1280px in both dimensions.** Use `img.thumbnail((1280,1280), Image.LANCZOS)` before saving. QA pipeline (v1.2.0) now auto-downscales before checks.

## Image Handling Policy (all agents)
Before sending any image to Claude: prefer tools; downscale if lower-res suffices; never send high-res unnecessarily. Vision limits: hallucination on tiny/rotated images; limited spatial reasoning; approximate counting. Rule in CLAUDE.md.

## Critique Format
Critics use: Score (0–100) → bullet issues (≤2 lines each) → single Bottom line sentence. ≤15 lines per asset. Rule in CLAUDE.md.

## Pitch Package Status — POST CYCLE 30

### Style Frames
- **SF01 Discovery**: v005 NEW C32 (char_cx rim light fix; Luma right silhouette correctly lit)
- **SF02 Glitch Storm**: v005
- **SF03 Other Side**: v005 (Luma = intentional pixel-art silhouette — may draw C13 scrutiny)
- **SF04 Luma+Byte**: v004 NEW C32 (full rebuild: value ceiling 255, monitor contribution, canonical specs)

### Logo
- **LTG_BRAND_logo_v001.png** — DECIDED C25

### Characters
- Luma: **expr v008 NEW C32** (THE NOTICING anchor expression; 3.2 heads, eye head_r×0.22), **turnaround v004 NEW C32** (ew=head_r×0.22 canonical), color model v002
- Byte: expr v004, turnaround v001, color model v001
- Cosmo: expr v004 (generator is dupe of v003 — PNG correct), turnaround v002, color model v001
- Miri: expr v003 (KNOWING), turnaround v001 (stub generator broken — PNG correct)
- Glitch: expr v003 (YEARNING/COVETOUS/HOLLOW; bilateral eyes = genuine feeling), turnaround v002, color model v001
- Character lineup: v006 (3.2 heads)

### Environments
All complete (Kitchen, Tech Den, Glitch Layer, School Hallway, Millbrook Street)

### Documentation
- Pitch brief: `ltg_pitch_brief_v001.md` — COMPLETE
- Delivery manifest: `pitch_delivery_manifest_v001.md`
- Pitch audit C30: `pitch_audit_cycle30.md`
- Color audit C30: `LTG_COLOR_audit_c30_preCritique13.md` — all 4 SFs PASS
- Color continuity: `color_continuity_c30.md`

## Known Risks for Critique 13
1. SF04 source generators = stubs (cannot regenerate)
2. Miri v003 stub generator broken (PNG correct)
3. Cosmo v004 generator = dupe of v003 (PNG correct)
4. SF03 Luma = pixel-art silhouette (intentional — may draw style-consistency critique)
5. Byte teal in SF04 at 60–70% luminance (intentional dual-lighting — Alex's call)
6. Miri v003 line weight slightly heavy (silhouette=6 at 2× vs canonical ~4)
7. Byte v004 droopy/storm eye arcs at width=5–8 at 1× (may draw scrutiny)

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
- **Ideabox review**: after each cycle, producer (not Alex) reviews ideabox/, actions worthy ideas, moves them to ideabox/actioned/.
- **Agent prompts**: do NOT duplicate inbox content. Prompts = role context + startup sequence only.

## Agent Prompt Design (C32 lesson)
Do NOT duplicate inbox message content in agent prompts. The inbox message IS the assignment. Agent prompts should only contain: role context, startup sequence (read CLAUDE.md, PROFILE.md, MEMORY.md, tools/README.md, then inbox). Task detail belongs in the inbox only — duplication causes drift.

## Technical Debt (C31)
- **W004 in 55 generators**: missing draw refresh after paste/composite — latent bug risk, Kai to fix C32
- **SF04 source generators missing**: proportion audit impossible; stubs only on disk

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
