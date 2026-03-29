# PRODUCER MEMORY — "Luma & the Glitchkin"

## Project
Comedy-adventure cartoon: 12yo Luma discovers dead pixels on grandma's CRT are mischievous creatures (Glitchkin). Pitch package: SF01 A+ locked; SF02 v005 + SF03 v003 PITCH READY; all characters documented.

## Status
**Cycle 24 + Critique 11 complete. Work cycles: 24. Critique cycles: 11.**
**Cycle 25 starts next. Critique Cycle 12 after Cycle 27.**

## Active Team (all 5 slots used)

| Member | Role | Reports To |
|--------|------|-----------|
| Alex Chen | Art Director | — |
| Maya Santos | Character Designer | Alex Chen |
| Sam Kowalski | Color & Style Artist | Alex Chen |
| Kai Nakamura | Tech Art Engineer | Alex Chen |
| Rin Yamamoto | Visual Stylization Artist (NEW C23) | Alex Chen |

**Inactive:** Jordan Reed (environments complete C22), Lee Tanaka (storyboard complete C21)

## Pitch Package Status — POST CYCLE 24 / CRITIQUE 11
- **SF01 Discovery**: v003 A+ LOCKED | `_styled.png` APPROVED (0.6×)
- **SF02 Glitch Storm**: v005 PITCH READY | `_styled.png` — DO NOT USE (hue rotation artifact — awaiting v002)
- **SF03 Other Side**: v003 PITCH READY | `_styled.png` — DO NOT USE (hue rotation artifact — awaiting v002)
- **SF04 Luma+Byte**: MISSING — central relationship not shown. Commission in C25.
- **Logo**: NO CANONICAL LOGO — placeholder only. Blocking external delivery. Fix C25.
- **Pitch brief**: `output/production/ltg_pitch_brief_v001.md` — COMPLETE
- **Delivery manifest**: `output/production/pitch_delivery_manifest_v001.md` — C23
- **Characters**: Luma v004, Byte v004, Cosmo v004, Miri v002, Glitch v002 (sheets) — all present
  - Color model PNGs for Luma/Byte/Cosmo: MISSING (blocking) — Maya C25
  - Luma body language in expressions: WEAK — Maya C25
  - Cosmo side view broken — Maya C25
- **Environments**: All complete + styled (Kitchen, Tech Den)
- **Character lineup**: v004 (all 5 characters)

## Cycle 24 — Completed
- **Alex**: SF01 styled APPROVED; critique11_self_assessment.md (A-); Glitch integration feedback to Maya; index updated
- **Maya**: Glitch expression sheet v002 (1200×900, 6 expressions); turnaround v002 (shadow fixed); lineup v004 (5 chars)
- **Sam**: Stylization fidelity report — SF02/SF03 styled FAIL, SF01/Kitchen PASS; color story updated with Glitch
- **Kai**: batch_stylize tool; paper_texture() in render lib; pipeline audit clean; README complete
- **Rin**: Tech Den + lineup styled; preset doc updated

## Critique 11 — Key Findings (relay sent to all members)
- **Rin**: Stylization tool v001 BROKEN — color protection only covers amber, destroys Glitch palette. Rebuild as v002.
  Fixes: extend hue protection to all canonical colors; chalk pass must skip cyan/light sources; warm bleed zone-aware; mixed mode pixel blend not alpha
- **Maya**: Color model PNGs for Luma/Byte/Cosmo missing (blocking); Luma body language invisible; Cosmo side view broken; Luma turnaround outdated
- **Sam**: SF02 spec doc has obsolete color values (Cycle 13); GL-04b luminance 0.17 → should be 0.017
- **Kai**: ~20 legacy scripts unarchived; production docs not LTG-named
- **Alex**: SF04 Luma+Byte scene needed; logo decision; Luma inconsistency; Miri narrative expression

## Cycle 25 Plan
- **Rin**: LTG_TOOL_stylize_handdrawn_v002.py (all 4 fixes); regen SF02+SF03 styled v002
- **Maya**: Color models for Luma/Byte/Cosmo; Luma expression sheet v005 (body language); Cosmo side view fix
- **Sam**: Fix SF02 spec doc obsolete values; GL-04b luminance fix; Miri color story note
- **Kai**: Archive ~20 legacy scripts; production naming decision
- **Alex**: Commission SF04 (Luma+Byte); resolve logo; direct Miri narrative expression

## Shared Library
`output/tools/LTG_TOOL_render_lib_v001.py` (v1.1.0) — 8 functions: perlin_noise_texture, gaussian_glow, light_shaft, dust_motes, catenary_wire, scanline_overlay, vignette, paper_texture.
`output/tools/LTG_TOOL_stylize_handdrawn_v001.py` — C23. BROKEN — hue rotation artifact destroys Glitch palette. DO NOT USE on SF02/SF03. Awaiting v002.
`output/tools/LTG_TOOL_batch_stylize_v001.py` — NEW C24. Batch runner for stylize().
Import: `from output.tools.LTG_TOOL_render_lib_v001 import *`

## Key Output Locations
- Style Frames: `/output/color/style_frames/`
- Characters: `/output/characters/main/`
- Backgrounds: `/output/backgrounds/environments/`
- Storyboard: `/output/storyboards/`
- Tools: `/output/tools/README.md`
- Master Palette: `/output/color/palettes/master_palette.md`
- Pitch Package Index: `/output/production/pitch_package_index.md`
- Pitch Brief: `/output/production/ltg_pitch_brief_v001.md`

## Pipeline & Standards
- Open source only: Python PIL
- Naming: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`
- Valid categories: CHAR, ENV, COLOR, SB, TOOL, BRAND
- Byte body color = GL-01b (#00D4E8 Byte Teal), NOT GL-01 (#00F0FF Electric Cyan)
- GL-07 CORRUPT_AMBER = #FF8C00 (255,140,0) — canonical
- Cyan-lit surface: G > R AND B > R individually (not just G+B > R)
- Classroom: zero Glitch palette; SF03: zero warm light
- After img.paste(), always refresh draw = ImageDraw.Draw(img)
- Character sheet: show_guides=False for pitch exports
