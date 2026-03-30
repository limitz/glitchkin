**Date:** 2026-03-30
**From:** Morgan Walsh
**Subject:** Doc Governance Audit — C47 (Reinhardt CRITIQUE #6 response)

## Summary

Reinhardt flagged 23 undocumented decisions and a stale character export manifest. I built `LTG_TOOL_doc_governance_audit.py` and ran a full scan of all 161 .md files under docs/ and output/.

## Key Findings

**43 STALE files** (10+ cycles since last cycle reference):

### Critical (20+ cycles stale)
| Age | Last Cycle | File | Notes |
|---|---|---|---|
| 44 | C3 | output/storyboards/ep01_cold_open.md | Original cold open — predates all current panels |
| 38 | C9 | output/production/pitch_readiness_c21.md | Pitch readiness from C21 era |
| 38 | C9 | output/color/style_frames/sf02_color_notes.md | SF02 completely rebuilt since C9 |
| 35 | C12 | output/characters/main/byte.md | Byte spec — 35 cycles stale |
| 31 | C16 | output/production/sf02_sf03_precritique_c18.md | Ancient pre-critique |
| 28 | C19 | output/characters/color_models/luma_color_model.md | Luma color model |
| 25 | C22 | output/color/palettes/LTG_COLOR_palette_audit_c23.md | Palette audit |
| 25 | C22 | output/color/style_frames/LTG_COLOR_sf_final_check_c23.md | SF final check |

### Character export manifest (Reinhardt's specific flag)
- `output/characters/main/character_export_manifest.md` — NO cycle reference at all. Listed in the NO_CYCLE_REF category. Likely frozen since C24 as Reinhardt noted.

### 58 NO_CYCLE_REF files
These have no C<number> references. Some are valid specs (docs/work.md, docs/pil-standards.md). Others may need attention:
- `output/characters/main/character_export_manifest.md` — the one Reinhardt flagged
- `output/characters/main/cosmo.md` — Cosmo spec with no cycle ref
- `output/characters/main/character_lineup.md` — lineup spec
- `output/production/pitch_delivery_manifest.md` — pitch manifest
- `output/production/naming_conventions.md` — naming doc
- `output/production/story/LTG_glitch_appearance_guide.md` — Glitch guide
- `output/style_guide.md` — master style guide

## Full Report
Saved to: `output/production/doc_governance_audit_c47.md`

## Tool
`output/tools/LTG_TOOL_doc_governance_audit.py` — reusable, CLI + module API. Run anytime with `--stale-threshold N` to adjust.

## Recommendation
Prioritize the character specs (byte.md at C12, luma.md at C34, glitch.md at C35, cosmo.md with no cycle ref) and the character_export_manifest since Reinhardt specifically flagged it. The 20+ cycle stale docs are likely candidates for either archival or a refresh pass.
