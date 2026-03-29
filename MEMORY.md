# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: all core assets present; Cycle 25 major gap closures complete.

## Status
**Cycle 28 complete. Work cycles: 28. Critique cycles: 12.**
**Cycle 29 starts next. Critique Cycle 13 after Cycle 30.**

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
- **SF03 Other Side**: v005 NEW C28 (UV_PURPLE_DARK saturation fixed: 31%→72%; GL-04a #3A1060)
- **SF04 Luma+Byte**: v003 NEW C28 (blush fixed #E8A87C, Byte fill canonical GL-01b, rim light right-side only)
- **Note:** All `*_styled*.png` post-processing outputs DELETED C26. Rin's role is now procedural generation, not post-processing. Stylize tools → legacy/.

### Logo
- **LTG_BRAND_logo_v001.png** — DECIDED C25 (asymmetric layout, A grade). Closes 24-cycle ambiguity.

### Characters
- Luma: expr v006 (line weight canonical), **turnaround v003 NEW C28** (line weight fixed, BACK view confirmed), color model v001
  - **STILL NEEDED C29: expr v007** (3.2 heads + eye spec h×0.22 reconciliation — Alex directed, not yet built)
- Byte: expr v004, turnaround v001, color model v001
- Cosmo: expr v004, turnaround v002, color model v001
- Miri: expr v003 (KNOWING expression), turnaround v001, color model v001
- Glitch: **expr v003 NEW C28** (9 panels: added YEARNING/COVETOUS/HOLLOW interior states; bilateral eyes = genuine feeling tell), turnaround v002, color model v001
- Character lineup: v005 (Luma v006 construction)
  - **STILL NEEDED C29: lineup v006** (3.2 heads — Alex directed, not yet built)

### Environments
All complete (Kitchen, Tech Den, Glitch Layer, School Hallway, Millbrook Street)

### Documentation
- Pitch brief: `ltg_pitch_brief_v001.md` — COMPLETE
- Delivery manifest: `pitch_delivery_manifest_v001.md`
- Pitch package index: updated C25

## Cycle 28 — Completed

### Alex Chen
- Canonical Luma ratio locked: **3.2 heads** (turnaround = construction master)
- Canonical eye width: **h×0.22** (turnaround values)
- Pitch brief updated: Luma's interior need — "the kid who notices what no one else sees; Glitchkin need her to see them"
- Maya directed: build expr v007 + lineup v006 (3.2 heads compliance)

### Sam Kowalski
- GL-06c STORM_CONFETTI_BLUE (#0A4F8C) registered in master_palette.md
- SF03 v005: UV_PURPLE_DARK corrected (31%→72% saturation, GL-04a #3A1060)
- Luma skin base cross-reference: RW-10 neutral, CHAR-L-01 lamp-lit — both correct in context

### Rin Yamamoto
- `LTG_TOOL_procedural_draw_v001.py` → v1.2.0: `add_rim_light()` gains `side` param (right/left/top/bottom/all)
- SF04 v003: blush #E8A87C, Byte fill GL-01b canonical, rim `side="right"`

### Kai Nakamura
- 9 LTG_TOOL_ compliant copies created for Glitch/logo/color model generators
- 8 forwarding stubs for large generators (original files pending git mv pass)
- 37 new README entries; pitch index updated with SF03 v005, SF04 v003, lineup v005
- **Carry-forward C29:** original LTG_CHAR_/LTG_COLOR_ source files still on disk — need git mv pass

### Maya Santos
- Luma turnaround v003: line weight fixed (all views), BACK view confirmed present, 1280×560
- Glitch expr v003: 9 panels, YEARNING/COVETOUS/HOLLOW added. **Bilateral eyes = genuine feeling** (breaks destabilized-right-eye signature)

---

## Critique 12 — Key Findings (C28 priorities)

### P1 — Blockers
- **Luma proportions inconsistent**: expr sheet ~2.5 heads, turnaround 3.2, lineup ~3.5. Alex decided: **3.2 canonical** (turnaround is master)
- **Luma eye spec conflict**: v006 eye width HR×0.28 vs turnaround h×0.22 (21% narrower). Must reconcile.
- **DATA_BLUE in SF02 unregistered**: #0A4F8C carries 70% of cold confetti — register or correct (Sam)
- **UV_PURPLE_DARK in SF03 wrong saturation**: 31% vs 72% — going grey-purple (Sam)
- **add_rim_light() direction-agnostic**: applies to ALL edges, not just correct side — must add `side` param (Rin → v1.2.0)
- **54+ naming violations**: generators use `LTG_CHAR_/LTG_COLOR_` prefix instead of `LTG_TOOL_` (Kai)

### P2
- Luma skin base 3-way conflict (#C4A882 / #C8885A / #C8885A) — document both as neutral+lamp-lit (Sam)
- SF04 blush wrong (reads pain/fever) — fix RGB (Sam + Rin)
- SF04 Byte body fill (0,190,210) drifts from canonical (0,212,232) (Rin)
- 24 tools unregistered in README (Kai)
- SF03 v004, SF04 v002, lineup v005 not in pitch index (Kai)
- **Pitch brief lacks Luma's interior need** — "sees world differently" is not a motivation (Alex)
- Glitch emotionally hollow — needs interior desire expression (Maya)
- Luma turnaround v002 line weight still heavy (Maya — already flagged)
- Style guide head-to-body ratio conflicts with character sheet standards (Reinhardt)

### Critic Grades
- Daisuke: Byte B, Glitch B-, Cosmo B, Luma expr C, Luma turnaround C, lineup C+
- Priya: palette architecture A-, production errors D (P1/P2 issues)
- Nkechi: overall B- — not yet emotionally pitch-ready
- Sven: SF03 PASS; SF01/SF02/SF04 WARN; 14 lighting inconsistencies
- Reinhardt: overall FAIL — solid foundation, systemic maintenance failures

---

## Cycle 27 — Completed

### Alex Chen
- Pitch package audit: all assets confirmed present on disk → VERDICT: READY for Critique 12
- pitch_audit_cycle27.md written; pitch_package_index.md updated (Luma v006, C27 additions)

### Sam Kowalski
- SF03 v004: confetti constrained to within 150px of anchors (C16 carry-forward CLOSED)

### Rin Yamamoto
- SF04 v002: wobble outlines, variable_stroke, add_face_lighting(), add_rim_light() — first pitch asset with full procedural quality

### Kai Nakamura
- LTG_TOOL_render_qa_v001.py v1.1.0: asset_type param, warm/cool skipped for character sheets
- QA re-run 29 assets: 6 PASS / 21 WARN / 2 FAIL
  - FAIL: lineup v004 (stale — v005 now exists); classroom env (low contrast, low priority)
  - SUNLIT_AMBER hue drift on Luma persists — needs generator investigation
  - Style frame warm/cool WARN = expected dramatic lighting

### Maya Santos
- Lineup v005: Luma updated to v006 construction (8-ellipse hair, cheek nubs, near-circular eyes)
- Luma turnaround v002 line weight flagged for C28 (still using heavy width=5-6)

---

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
