# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: all core assets present; Cycle 25 major gap closures complete.

## Status
**Cycle 29 complete. Work cycles: 29. Critique cycles: 12.**
**Cycle 30 starts next. Critique Cycle 13 after Cycle 30.**

## Active Team (all 5 slots used)

| Member | Role | Reports To |
|--------|------|-----------|
| Alex Chen | Art Director | — |
| Maya Santos | Character Designer | Alex Chen |
| Sam Kowalski | Color & Style Artist | Alex Chen |
| Kai Nakamura | Tech Art Engineer | Alex Chen |
| Rin Yamamoto | Visual Stylization Artist (from C23) | Alex Chen |

**Inactive:** Jordan Reed (environments complete C22), Lee Tanaka (storyboard complete C21)

## Image Output Rule (MANDATORY — added C25)
**Prefer smallest resolution appropriate for the task. Hard limit: ≤ 1280px in both dimensions.**
Use `img.thumbnail((1280, 1280), Image.LANCZOS)` before saving. `thumbnail()` only shrinks — never upscales. Detail crops also ≤ 1280×1280px.
Rule is in: CLAUDE.md, all member MEMORYs, tools/README.md, character_sheet_standards_v001.md, naming_conventions.md.

## Image Handling Policy (C29 — all agents)
Before sending any image to Claude: prefer tools to extract insight; downscale if lower-res suffices; never send high-res unnecessarily. Vision limits: hallucination risk on tiny/rotated images; limited spatial reasoning; approximate counting. Rule in CLAUDE.md `## Image Handling`.

## Critique Format (C29)
Critics use compact format: Score (0–100) → bullet issues (≤2 lines each) → single Bottom line sentence. ≤15 lines per asset. No lengthy prose. Rule in CLAUDE.md `## Critics`.

## Pitch Package Status — POST CYCLE 29

### Style Frames
- **SF01 Discovery**: v004 NEW C29 (procedural pass: wobble, variable stroke, face lighting, rim right; blush fixed)
- **SF02 Glitch Storm**: v005
- **SF03 Other Side**: v005 (UV_PURPLE_DARK fixed C28)
- **SF04 Luma+Byte**: v003 (blush, Byte fill, rim right fixed C28)

### Logo
- **LTG_BRAND_logo_v001.png** — DECIDED C25

### Characters
- Luma: **expr v007 NEW C29** (3.2 heads, eye h×0.22 — P1 blockers CLOSED), turnaround v003, color model v001
- Byte: expr v004, turnaround v001, color model v001
- Cosmo: expr v004, turnaround v002, color model v001
- Miri: expr v003 (KNOWING expression), turnaround v001, color model v001
- Glitch: expr v003 (YEARNING/COVETOUS/HOLLOW; bilateral eyes = genuine feeling), turnaround v002, color model v001
- **Character lineup: v006 NEW C29** (3.2 heads — P1 blocker CLOSED)

### Environments
All complete (Kitchen, Tech Den, Glitch Layer, School Hallway, Millbrook Street)

### Documentation
- Pitch brief: `ltg_pitch_brief_v001.md` — COMPLETE
- Delivery manifest: `pitch_delivery_manifest_v001.md`
- Pitch audit: `pitch_audit_cycle29.md` — updated C29

## C30 Directives (Alex Chen)
- **Rin**: Verify SF01 v004 Luma proportions in scene context (3.2 heads, h×0.22 eyes)
- **Kai**: Drawing order audit across active generators; any remaining naming/README gaps
- **All**: Critique 13 prep — SF01 is weakest remaining asset

## Cycle 29 — Completed

### Alex Chen
- pitch_audit_cycle29.md updated; C30 risk profile raised; C30 directives issued

### Sam Kowalski
- No new outputs — color story and SF02 spec already reflected all C28 fixes

### Kai Nakamura
- LTG_TOOL_naming_cleanup_v001.py created + executed (producer ran it): 22 legacy files deleted
- README.md updated with C29 legacy archive section
- character_sheet_standards_v001.md line weight table verified correct

### Rin Yamamoto
- SF01 v004 (LTG_COLOR_styleframe_discovery_v004.png, 1280×720): wobble, variable stroke, face lighting (warm upper-left), rim right (CRT teal), blush fixed

### Maya Santos
- Luma expr v007 (1200×900): 3.2 heads (torso HR×2.10, pants HR×1.68), eye h×0.22 — CLOSES P1
- Lineup v006 (1280×508): LUMA_HEADS=3.2, HEAD_UNIT=87.5px, eye h×0.22 — CLOSES P1

## Critique 12 — Key Findings (reference)
All C28 P1 blockers resolved by end of C29:
- Luma proportions: ✓ expr v007 + lineup v006 (3.2 heads canonical)
- Eye spec conflict: ✓ h×0.22 throughout
- DATA_BLUE unregistered: ✓ GL-06c registered C28
- UV_PURPLE_DARK saturation: ✓ SF03 v005
- rim_light direction-agnostic: ✓ v1.2.0 side param
- 54+ naming violations: ✓ 22 legacy files deleted C29; stubs from C28

### Critic Scores (C12 — letter grades, pre-new-format)
- Daisuke: Byte B, Glitch B-, Cosmo B, Luma expr C, Luma turnaround C, lineup C+
- Priya: palette A-, production errors D
- Nkechi: overall B- — not yet emotionally pitch-ready
- Sven: SF03 PASS; SF01/SF02/SF04 WARN
- Reinhardt: overall FAIL — systemic maintenance failures

## Shared Library
`LTG_TOOL_render_lib_v001.py` (v1.1.0) — 8 functions incl. paper_texture
`LTG_TOOL_color_verify_v001.py` — canonical color hue verification
`LTG_TOOL_render_qa_v001.py` (v1.1.0) — full render QA (silhouette, value, color, warm/cool)
`LTG_TOOL_procedural_draw_v001.py` (v1.2.0) — wobble, variable stroke, rim light (side param), face lighting
`LTG_TOOL_naming_cleanup_v001.py` — C29. Removes legacy LTG_CHAR_/LTG_COLOR_ files (dry-run mode available)
**RETIRED C26 → legacy/:** stylize tools

## Canonical Palette Reminders
- Byte body = GL-01b #00D4E8 BYTE_TEAL (NOT #00F0FF)
- CORRUPT_AMBER = GL-07 #FF8C00 (255,140,0)
- HOT_MAGENTA = GL-02 #FF2D6B (NOT #FF0090)
- UV_PURPLE = #7B2FBE (not #6A0DAD — verify in master_palette.md)
- GL-06c STORM_CONFETTI_BLUE = #0A4F8C
- Cyan-lit surface: G > R AND B > R individually
- SF03: zero warm light; Classroom: zero Glitch palette

## Key Output Locations
- Style Frames: `output/color/style_frames/`
- Characters: `output/characters/main/`
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
