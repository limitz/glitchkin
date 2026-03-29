# Statement of Work — Cycle 26

**Date:** 2026-03-29
**Project:** Luma & the Glitchkin — Cartoon Pitch Package
**Cycle:** 26 of 26 complete

---

## Summary

Cycle 26 focused on pipeline cleanup (retiring the post-processing stylization workflow), character asset refinement (Luma expression sheet line weight canonical spec), and procedural art tooling (volumetric face lighting).

---

## Deliverables

### New Assets
| File | Description |
|------|-------------|
| `output/characters/main/LTG_CHAR_luma_expression_sheet_v006.png` | Luma expression sheet rebuilt to classroom pose line weight standard |
| `output/tools/LTG_CHAR_luma_expression_sheet_v006.py` | Generator for v006 |
| `output/tools/test_face_lighting_v001.png` | Test image for add_face_lighting() |

### Updated Tools
| File | Change |
|------|--------|
| `output/tools/LTG_TOOL_procedural_draw_v001.py` | v1.1.0 — added `add_face_lighting()` |

### Updated Documentation
| File | Change |
|------|--------|
| `output/production/pitch_package_index.md` | Removed all 8 styled asset references; pipeline retirement noted |
| `output/production/pitch_delivery_manifest_v001.md` | Styled files removed from delivery |
| `output/tools/README.md` | Stylize tools marked RETIRED; legacy section added |

### Retired (moved to legacy/)
- `LTG_TOOL_stylize_handdrawn_v001.py`
- `LTG_TOOL_stylize_handdrawn_v002.py`
- `LTG_TOOL_batch_stylize_v001.py`

---

## Key Decisions

- **SF04 Byte teal**: Confirmed intentional — dual scene lighting blend (warm window left + cool monitor right). Not a palette error.
- **Line weight canonical spec**: 3-tier at 2× render — head outline = width 4, structure = width 3, detail = width 2. Produces ~2/1.5/1px at output. Now locked as production standard for all Luma generators.
- **Post-processing pipeline fully retired**: No styled PNGs. Hand-drawn quality built in at generation time.
- **SUNLIT_AMBER QC false positive**: `verify_canonical_colors()` radius=40 samples skin tone pixels on character sheets; these are not SUNLIT_AMBER failures. QC tool limitation documented.

---

## Team
| Member | Work |
|--------|------|
| Maya Santos | Luma expression sheet v006 |
| Alex Chen | Document cleanup; SF04 Byte teal decision |
| Rin Yamamoto | add_face_lighting() in procedural draw lib |
| Sam Kowalski | Carry-forward cleanup; GL-04b verified; false positive documented |
| Kai Nakamura | C26 earlier: LTG_TOOL_render_qa_v001.py |

---

## Next
- **Cycle 27** — standard work cycle
- **Critique Cycle 12** — after Cycle 27
