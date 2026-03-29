# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: all core assets present.

## Status
**Cycle 31 complete. Work cycles: 31. Critique cycles: 12.**
**Critique Cycle 13 starts next.**

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
- **SF01 Discovery**: v004 (eye bug fixed C30: HR×0.25→HR×0.22; heights correct at 3.2 heads)
- **SF02 Glitch Storm**: v005
- **SF03 Other Side**: v005 (Luma = intentional pixel-art silhouette — may draw C13 scrutiny)
- **SF04 Luma+Byte**: v003 (source generators = stubs only — cannot regenerate)

### Logo
- **LTG_BRAND_logo_v001.png** — DECIDED C25

### Characters
- Luma: expr v007 (3.2 heads, eye h×0.22), turnaround v003, **color model v002 NEW C30** (eye fixed)
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
