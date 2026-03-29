# Statement of Work — Cycle 28

**Date:** 2026-03-29
**Project:** Luma & the Glitchkin — Cartoon Pitch Package
**Cycle:** 28 (Critique 12 response)

---

## Summary

Critique 12 response cycle. Addressed all P1 blocking issues: canonical Luma proportions locked, color production errors fixed, rim light library upgraded to directional, naming compliance pass begun, Glitch character given emotional depth.

---

## Deliverables

### New/Updated Assets
| File | Description |
|------|-------------|
| `output/color/style_frames/LTG_COLOR_styleframe_otherside_v005.png` | SF03 v005 — UV_PURPLE_DARK saturation corrected |
| `output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v003.png` | SF04 v003 — blush, Byte fill, rim light all fixed |
| `output/characters/main/turnarounds/LTG_CHAR_luma_turnaround_v003.png` | Luma turnaround v003 — line weight fixed, BACK view confirmed |
| `output/characters/main/LTG_CHAR_glitch_expression_sheet_v003.png` | Glitch v003 — YEARNING, COVETOUS, HOLLOW interior desire states |

### Updated Tools / Library
| File | Change |
|------|--------|
| `output/tools/LTG_TOOL_procedural_draw_v001.py` | v1.2.0 — `add_rim_light()` directional `side` param |
| `output/tools/LTG_TOOL_style_frame_03_other_side_v005.py` | SF03 v005 generator |
| `output/tools/LTG_COLOR_styleframe_luma_byte_v003.py` | SF04 v003 generator |
| `output/tools/LTG_TOOL_luma_turnaround_v003.py` | Turnaround v003 generator |
| `output/tools/LTG_TOOL_glitch_expression_sheet_v003.py` | Glitch v003 generator |

### Updated Documentation
| File | Change |
|------|--------|
| `output/production/ltg_pitch_brief_v001.md` | Luma interior need: "the kid who notices what no one else sees" |
| `output/color/palettes/master_palette.md` | GL-06c STORM_CONFETTI_BLUE registered; skin base cross-ref added |
| `output/tools/README.md` | 37 new entries; all active tools registered |
| `output/production/pitch_package_index.md` | SF03 v005, SF04 v003, lineup v005 added |

### Pipeline Compliance
- 9 LTG_TOOL_ compliant generator copies created (from LTG_CHAR_/LTG_COLOR_)
- 8 forwarding stubs for large generators
- Original source files pending git mv pass (C29 carry-forward)

---

## Key Decisions

- **Luma canonical: 3.2 heads** — turnaround is construction master
- **Eye spec: h×0.22 width** — turnaround values canonical
- **GL-06c registered** — DATA_BLUE (#0A4F8C) is deliberate atmospheric depth for SF02 storm distance
- **Glitch bilateral eyes** = genuine interior feeling (breaks destabilized-right-eye signature — design innovation)
- **Luma's interior need**: the kid whose way of seeing the world is finally validated by the Glitchkin needing her to see them

## Still Needed (C29)
- Luma expression sheet v007 — 3.2 heads + h×0.22 eye (Alex directed, not yet built)
- Character lineup v006 — 3.2 heads reconciliation
- git mv pass for LTG_CHAR_/LTG_COLOR_ → LTG_TOOL_ source files

---

## Team
| Member | Work |
|--------|------|
| Alex Chen | Canonical proportion decisions; pitch brief emotional premise |
| Sam Kowalski | SF03 v005; GL-06c; skin base documentation |
| Rin Yamamoto | procedural_draw v1.2.0; SF04 v003 |
| Kai Nakamura | Naming compliance; README 37 entries; pitch index |
| Maya Santos | Luma turnaround v003; Glitch expression v003 |

---

## Next
- **Cycle 29** — Luma expr v007, lineup v006, git mv naming pass
- **Cycle 30** — Final polish
- **Critique Cycle 13** — after Cycle 30
