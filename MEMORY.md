# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: all core assets present; Cycle 25 major gap closures complete.

## Status
**Cycle 26 complete. Work cycles: 26. Critique cycles: 11.**
**Cycle 27 starts next. Critique Cycle 12 after Cycle 27.**

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
53 existing images resized in-place (C25 resize pass).

## Pitch Package Status — POST CYCLE 25

### Style Frames
- **SF01 Discovery**: v003
- **SF02 Glitch Storm**: v005
- **SF03 Other Side**: v003
- **SF04 Luma+Byte**: v001 — Luma CURIOUS, Byte WORRIED on shoulder, dual warm/cool lighting. **Byte teal = intentional blend** (BYTE_FILL (0,190,210) + BYTE_SH (0,110,140) α180 shadow — not a palette error)
- **Note:** All `*_styled*.png` post-processing outputs DELETED C26. Rin's role is now procedural generation, not post-processing. Stylize tools → legacy/.

### Logo
- **LTG_BRAND_logo_v001.png** — DECIDED C25 (asymmetric layout, A grade). Closes 24-cycle ambiguity.

### Characters
- Luma: expr **v006** NEW C26 (line weight canonical — 3-tier: head=4, structure=3, detail=2 at 2× render), turnaround v002 (Act 2 proportions), color model v001
- Byte: expr v004, turnaround v001, color model v001 NEW C25
- Cosmo: expr v004, turnaround v002 (side view fixed) NEW C25, color model v001 NEW C25
- Miri: expr v003 (KNOWING expression added) NEW C25, turnaround v001, color model v001
- Glitch: expr v002, turnaround v002, color model v001
- Character lineup: v004 (all 5)

### Environments
All complete (Kitchen, Tech Den, Glitch Layer, School Hallway, Millbrook Street) — styled versions present

### Documentation
- Pitch brief: `ltg_pitch_brief_v001.md` — COMPLETE
- Delivery manifest: `pitch_delivery_manifest_v001.md`
- Pitch package index: updated C25

## Cycle 26 — Completed

### Maya Santos
- Luma expression sheet v006 — line weight canonical spec: head=4, structure=3, detail=2 at 2× render (~2/1.5/1px output). Hair + cheek nubs correct. 1200×900.

### Alex Chen
- pitch_package_index.md: all 8 styled asset refs removed; stylization pipeline note added
- pitch_delivery_manifest_v001.md: styled files removed from delivery
- output/tools/README.md: stylize tools marked RETIRED C26, legacy section added
- SF04 Byte teal CONFIRMED INTENTIONAL: dual lighting blend (warm window + cool monitor)

### Rin Yamamoto
- `LTG_TOOL_procedural_draw_v001.py` → v1.1.0: added `add_face_lighting()` — 4-layer volumetric split-light (brow shadow, nose-on-cheek shadow, chin-on-neck shadow, highlight accent). PIL-native, seeded.
- Test: `output/tools/test_face_lighting_v001.png` (600×300px)
- All 5 stale inbox messages archived. Post-processing pipeline fully retired.

### Sam Kowalski
- UV_PURPLE carry-forward CLOSED (no styled outputs)
- GL-04b luminance VERIFIED = 0.017 (C25 fix intact)
- SUNLIT_AMBER QC false positive documented: radius=40 samples skin pixels on character sheets; not a real palette error

### Kai Nakamura (C26 earlier)
- LTG_TOOL_render_qa_v001.py — full QA pipeline; ran on 8 C25 assets

---

## Cycle 25 — Completed

### Rin Yamamoto
- LTG_TOOL_stylize_handdrawn_v002.py — 4 critical fixes: full 6-color hue protection, chalk pass exclusions (cyan+light sources), warm bleed zone gate, mixed mode cross-dissolve
- SF02 + SF03 styled v002 regenerated. SF01 LOCKED — not re-processed.
- Verify warning: hue drift warnings on cyan/purple expected in glitch mode (geometric channel offset = intentional aesthetic, not palette corruption)

### Kai Nakamura
- LTG_TOOL_color_verify_v001.py — `verify_canonical_colors(img, palette_dict, max_delta_hue=5)` + `get_canonical_palette()`
- 20 legacy tool scripts → `output/tools/legacy/`; 27 legacy storyboard panels → `output/storyboards/panels/legacy/`
- Production doc naming exemption documented in naming_conventions.md
- LTG_TOOL_batch_stylize_v001.py → v1.1.0 (calls v002 stylize, adds color verify per job)
- **HOT_MAGENTA canonical: #FF2D6B (NOT #FF0090)** — always verify in master_palette.md

### Sam Kowalski
- SF02 spec doc: ENV-06 #96ACA2 and DRW-07 #C8695A corrected (4 locations — was Cycle 13 stale values)
- Master palette GL-04b luminance: 0.17 → 0.017 (order-of-magnitude error fixed)
- Color story: Miri bridge-character section added (warm palette encodes prior Glitch knowledge)

### Alex Chen
- SF04 Luma+Byte created — closes Critique 11 P1 gap (core relationship was invisible)
- Logo canonical decision made — closes 24-cycle ambiguity
- Luma canonical = expression sheet v004 (directed Maya); Miri KNOWING expression directed

### Maya Santos
- Color models for Luma, Byte, Cosmo (800×500 each, 14 swatches, same format as Glitch model)
- Luma expression sheet v005: full body, every expression unique at silhouette level (6 poses)
- Cosmo turnaround v002: side view fixed (profile head polygon, stripe depth lines, staggered legs)
- Luma turnaround v002: Act 2 proportions (3.2 heads, A-line hoodie, chunky sneakers)
- Miri expression sheet v003: KNOWING STILLNESS added (6th panel — narrative secret)
- Note: Alex's direction arrived after Maya completed; she used correct fallback (expr sheet v004 canonical)

## Shared Library
`LTG_TOOL_render_lib_v001.py` (v1.1.0) — 8 functions incl. paper_texture
`LTG_TOOL_color_verify_v001.py` — canonical color hue verification
`LTG_TOOL_render_qa_v001.py` — C26. Full render QA (silhouette, value, color, warm/cool)
`LTG_TOOL_procedural_draw_v001.py` (v1.1.0) — C26. Wobble lines, variable stroke, rim light, silhouette/value test, **add_face_lighting() NEW C26**
**RETIRED C26 → legacy/:** `LTG_TOOL_stylize_handdrawn_v001.py`, `LTG_TOOL_stylize_handdrawn_v002.py`, `LTG_TOOL_batch_stylize_v001.py`

## Canonical Palette Reminders
- Byte body = GL-01b #00D4E8 BYTE_TEAL (NOT #00F0FF)
- CORRUPT_AMBER = GL-07 #FF8C00 (255,140,0)
- HOT_MAGENTA = GL-02 #FF2D6B (NOT #FF0090)
- UV_PURPLE = #7B2FBE (not #6A0DAD — verify in master_palette.md)
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
