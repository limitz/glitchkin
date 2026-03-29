# Statement of Work — Cycle 22

**Project:** Luma & the Glitchkin — Pitch Package
**Date:** 2026-03-29
**Work Cycles:** 22 | **Critique Cycles:** 10 (completed this cycle)

---

## Critique Cycle 10 Summary

Five critics reviewed the full pitch package state following Cycles 20–21.

| Critic | Focus | Key Finding |
|--------|-------|-------------|
| Victoria Ashford | Pitch readiness, SF02/SF03, Luma/Byte sheets | 3 conditions to pitch-ready; pitch brief critical gap |
| Dmitri Volkov | Byte v003, Miri v002, Cosmo v003 | Byte STORM/CRACKED glyph non-compliant (6+ deviations); Cosmo SKEPTICAL/SURPRISED collision |
| Naomi Bridges | Color story doc, SF02 pane alpha, JEANS_BASE | GL-07 CORRUPT_AMBER factual error; character-warmth hierarchy inverted |
| Fiona O'Sullivan | ltg_render_lib, tool naming, char sheet consistency | Non-compliant library filename unacceptable as pipeline foundation |
| Takeshi Murakami | Tech Den v003, Kitchen v002, Glitch Layer v003 | Light shaft not solved — renegotiated. SOLVE it. |

---

## Deliverables Produced

### Alex Chen (Art Director)
- `output/production/ltg_pitch_brief_v001.md` — ONE-PAGE PITCH BRIEF (critical gap closed): Premise, Tone, Audience, Format, Visual Identity Statement. ~185 words, pitch-deck quality.
- `output/production/character_sheet_standards_v001.md` — Binding standards for all future character sheets: label format, HEAD_R mapping, head unit ranges, construction guide policy, 3-tier line weight table.
- `output/production/pitch_package_index.md` — Updated through Cycle 22. Package completeness status: standalone pitch brief NOW COMPLETE.

### Maya Santos (Character Designer)
- `output/characters/main/LTG_CHAR_byte_expression_sheet_v004.png` — Byte sheet rebuilt: STORM/CRACKED glyph corrected per Section 9B canonical (all 6 deviations resolved, DIM_PX to #005064, crack line to void black); STORM/RESIGNED differentiation via arm asymmetry (6/22 vs 14/14); RELUCTANT JOY perked antenna; POWERED DOWN squash 0.75.
- `output/characters/main/LTG_CHAR_cosmo_expression_sheet_v004.png` — SKEPTICAL redesigned as lateral containment (arms 2/2 + body_squash 0.92) — no longer reads as SURPRISED at thumbnail.
- `output/characters/main/LTG_CHAR_luma_expression_sheet_v004.png` — Clean pitch export (no construction guides).
- `output/characters/main/LTG_CHAR_luma_expression_sheet_v004_guides.png` — Production reference export (with guides).
- CURIOUS expression upgraded from marginal to confident squint-test pass.

### Jordan Reed (Background & Environment Artist) — FINAL CYCLE
- `output/backgrounds/environments/LTG_ENV_tech_den_v004.png` — Light shaft repositioned to desk zone (apex at 105,265; base at desk surface), shaft width ~200px, max_alpha 150; THREE individuated monitor glow spills replacing single wash.
- `output/backgrounds/environments/LTG_ENV_grandma_kitchen_v003.png` — Wall texture extended to left/right walls (side alpha -35%); floor grid conflict resolved (single perspective-correct linoleum system, converges to vp_x).

### Sam Kowalski (Color & Style Artist)
- `output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v005.png` — Window pane alpha reduced to 115/110 (character-warmth hierarchy restored); CORRUPT_AMBER corrected to GL-07 #FF8C00.
- `output/color/palettes/master_palette.md` — JEANS_BASE UV-ambient variant documented; Gap 3 marked RESOLVED.
- `output/color/style_frames/ltg_style_frame_color_story.md` — Three-sentence pitch callout elevated to prominent header; GL-07 value fully reconciled with generator.

### Kai Nakamura (Technical Art Engineer)
- `output/tools/LTG_TOOL_render_lib_v001.py` — Canonical LTG-compliant rename of shared rendering library. `__version__ = "1.0.0"` added. Dead alpha floor fixed in `gaussian_glow()`.
- `output/tools/ltg_render_lib.py` — Deprecated; now a compatibility wrapper that re-exports from canonical file. Scheduled for removal Cycle 23.
- `output/tools/README.md` — All deferred items resolved: CHAR→TOOL renames applied, misplaced files section cleared.
- Coordinated with Jordan Reed on import path for Cycle 22 generators.

---

## Team Structure Changes (Effective Cycle 23)

**Deactivated:** Jordan Reed — all major environments complete.
**Added:** Rin Yamamoto — Visual Stylization Artist. Specializes in rendering algorithms that simulate hand-drawn, organic aesthetics. Will apply stylization post-processing passes to pitch package assets.

---

## Pitch Package Status (post-Cycle 22)

| Asset | Status |
|-------|--------|
| SF01 Discovery | A+ LOCKED |
| SF02 Glitch Storm v005 | Window alpha fixed, CORRUPT_AMBER fixed — READY |
| SF03 Other Side v003 | Byte visibility fixed, Byte GL-01b correct — READY |
| Luma expression sheet v004 | Clean pitch export available — READY |
| Byte expression sheet v004 | Glyph spec compliant — READY |
| Cosmo expression sheet v004 | SKEPTICAL containment fixed — READY |
| Miri expression sheet v002 | Previously approved — READY |
| Act 1+2 storyboard | Complete (contact sheets v002/v006) — READY |
| Tech Den v004 | Light shaft + monitor glow solved — READY |
| Kitchen v003 | Wall texture + floor grid resolved — READY |
| One-page pitch brief | WRITTEN — READY |
| Master palette | Fully documented — READY |

**Overall Status: PITCH READY** (pending Critique Cycle 11 validation)

---

*Next: Cycle 23 — Rin Yamamoto's stylization pass on pitch package assets. Critique Cycle 11 after Cycle 24.*
