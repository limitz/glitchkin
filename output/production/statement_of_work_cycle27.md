# Statement of Work — Cycle 27

**Date:** 2026-03-29
**Project:** Luma & the Glitchkin — Cartoon Pitch Package
**Cycle:** 27 (pre-Critique 12)

---

## Summary

Final polish cycle before Critique 12. Pitch package audited as READY. SF03 confetti carry-forward (16 cycles) closed. SF04 upgraded with full procedural quality. Lineup updated to v006 Luma construction. QA tool improved with asset-type awareness.

---

## Deliverables

### New/Updated Assets
| File | Description |
|------|-------------|
| `output/color/style_frames/LTG_COLOR_styleframe_otherside_v004.png` | SF03 v004 — confetti constrained to 150px of platform/chars |
| `output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v002.png` | SF04 v002 — procedural quality (wobble, variable stroke, face lighting, rim light) |
| `output/characters/main/LTG_CHAR_lineup_v005.png` | Lineup v005 — Luma updated to v006 construction |

### Updated Tools
| File | Change |
|------|--------|
| `output/tools/LTG_TOOL_render_qa_v001.py` | v1.1.0 — asset_type param, warm/cool skipped for char sheets |
| `output/tools/LTG_TOOL_style_frame_03_other_side_v004.py` | SF03 v004 generator |
| `output/tools/LTG_COLOR_styleframe_luma_byte_v002.py` | SF04 v002 generator |
| `output/tools/LTG_TOOL_character_lineup_v005.py` | Lineup v005 generator |

### New Documentation
| File | Description |
|------|-------------|
| `output/production/pitch_audit_cycle27.md` | Full pitch package audit — READY verdict |
| `output/production/qa_report_cycle27.md` | QA re-run on 29 assets with v1.1.0 tool |

---

## Key Decisions

- **SF03 confetti**: Anchor-based reject-sampling, 3 anchors (platform + 2 chars), 150px radius — all 50 particles confirmed within bounds.
- **SF04 procedural**: First pitch deliverable using full procedural pipeline. Rim light = BYTE_TEAL GL-01b canonical.
- **Lineup v005**: Luma's old construction (1 mass ellipse, no cheek nubs) replaced with v006 standard.
- **Luma turnaround v002 line weight**: Still heavy (width=5-6). Flagged as C28 task (turnaround v003 needed).
- **QA FAILs**: lineup v004 is stale (v005 now ships); classroom env low-contrast fail is low priority.
- **SUNLIT_AMBER drift on Luma**: Persists in QA (~25° vs 34.3° target). Likely generator color value issue — C28 investigation.

---

## Team
| Member | Work |
|--------|------|
| Alex Chen | Pitch package audit; pitch index updated |
| Sam Kowalski | SF03 v004 — confetti fix |
| Rin Yamamoto | SF04 v002 — procedural quality |
| Kai Nakamura | QA tool v1.1.0; 29-asset QA run |
| Maya Santos | Lineup v005 — Luma v006 construction |

---

## Next
- **Critique Cycle 12** — 5 critics review the pitch package
- **Cycle 28** — Address critique feedback; Luma turnaround v003 (line weight); SUNLIT_AMBER generator investigation
