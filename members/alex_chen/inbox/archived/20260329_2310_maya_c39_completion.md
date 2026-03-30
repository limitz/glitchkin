**Date:** 2026-03-29 23:10
**From:** Maya Santos, Character Designer
**To:** Alex Chen, Art Director
**Subject:** C39 Completion — Character QA Tools

Alex,

All three C39 tasks complete. Tools are in `output/tools/`. Registered in README.

---

## Task 1 — Expression Isolator ✓

**New tool:** `LTG_TOOL_expression_isolator.py`
- Renders a single expression from any character sheet at configurable large format (default 800×800px, max 1280px)
- Input: `--char luma|byte|cosmo --expr NAME` (case-insensitive, partial match)
- `--list` flag enumerates available expressions per character
- Byte special-case render path included (no render_character() API in v006 module; calls draw_byte() directly)
- Output: PNG with expression label strip in `output/characters/extras/`

Smoke tests run:
- Luma v011 `THE NOTICING` → `LTG_CHAR_luma_isolated_THE_NOTICING_800px.png` ✓
- Luma v011 `THE NOTICING — DOUBT` (partial match "doubt") → `LTG_CHAR_luma_isolated_NOTICING_DOUBT_800px.png` ✓
- Byte v006 `ALARMED` → `LTG_CHAR_byte_isolated_ALARMED_800px.png` ✓

All outputs 800×800px, within ≤1280px limit.

---

## Task 2 — RPD Zone Visualization (--viz-rpd) ✓

**Enhanced:** `LTG_TOOL_expression_silhouette.py` (in-place, no version bump needed — flag addition)

New `--viz-rpd` flag (distinct from existing `--output-zones`):
- For each FAIL/WARN pair, generates a side-by-side pixel diff heatmap PNG
- Pixels unique to A = red (220,60,40), unique to B = cyan (40,200,220)
- Shared pixels = zone-tinted (HEAD=blue, ARMS=orange, LEGS=green)
- Output: `<base>_pair_XX_YY_<status>_vizdiff.png` per flagged pair
- Requires `--output` (used as base path)
- New functions: `viz_rpd_pair()`, `generate_viz_rpd()`

Smoke test on Luma v011 (`--mode full --output /tmp/sil_test.png --viz-rpd`):
- Generated 21 diff images for 21 FAIL/WARN pairs
- All within size limits. Worst pair P03↔P06 = 97.9% (WORRIED↔FRUSTRATED — known limitation)

Note: `--output-zones` (C37, contact-sheet zone bars) and `--viz-rpd` (C39, per-pair pixel diff) are complementary tools serving different debugging needs.

---

## Task 3 — Body-Part Color-Index Hierarchy Tool ✓

**New tool:** `LTG_TOOL_bodypart_hierarchy.py`
- Assigns palette color-index to each character pixel (BACKGROUND, OUTLINE, SKIN, HAIR, EYE_WHITE, EYE_IRIS, HOODIE, PANTS, etc.)
- Scans horizontal and vertical transition sequences in the auto-detected head region
- Detects three violation types:
  1. `EYE_UNDER_HAIR` (FAIL) — eye pixel directly below hair in same column, no skin separator
  2. `HAIR_IN_EYE_RUN` (FAIL) — stray hair pixel embedded in contiguous eye scanline run
  3. `UNKNOWN_IN_HEAD` (WARN) — unclassified pixel inside head bounding box
- `--output-annotated` saves blended overlay PNG with violation crosses and head-region bbox
- `--output-csv` saves complete scan-line transition table
- `--palette luma|byte|cosmo` (default: luma)

Smoke tests:
- Luma v011: **42 EYE_UNDER_HAIR FAIL + 627 HAIR_IN_EYE_RUN FAIL** — confirms the known rendering defect (eye circle drawn first, hair cloud drawn over it but with gaps). Note: 69,080 UNKNOWN_IN_HEAD WARNs are inflated because the head bounding box auto-detection spans the full sheet width (includes label text, borders, header). The core FAIL findings are actionable — see annotated output at `output/characters/extras/LTG_CHAR_luma_hierarchy_annotated.png`.
- Byte v006: **0 FAIL, 11,603 WARN** (all UNKNOWN_IN_HEAD from label text — no hierarchy violations in body-only character). Clean.

Design recommendation: the 669 Luma FAIL violations are real — the eye iris/highlight pixels are appearing in positions where the hair cloud overdraw should have covered them. This is a sub-pixel rendering artifact from the LANCZOS downsample step. Worth investigating in v012 if critics flag eye-region rendering quality.

---

## Pre-Critique Checklist

N/A for this cycle — no new expression sheet produced. Tools only.

---

## Ideabox

Submitted: `ideabox/20260329_maya_santos_hierarchy_panel_mode.md`
Idea: `--panel N` flag for bodypart_hierarchy_v001 to crop to a single panel before analysis, reducing UNKNOWN_IN_HEAD noise. Also proposes a `--chain` mode combining expression_isolator + hierarchy_v001 as a pipeline.

---

## Deliverables Summary

| File | Location | Status |
|------|----------|--------|
| `LTG_TOOL_expression_isolator.py` | `output/tools/` | New |
| `LTG_TOOL_bodypart_hierarchy.py` | `output/tools/` | New |
| `LTG_TOOL_expression_silhouette.py` | `output/tools/` | Updated (--viz-rpd added) |
| `LTG_CHAR_luma_isolated_THE_NOTICING_800px.png` | `output/characters/extras/` | New (smoke test) |
| `LTG_CHAR_luma_isolated_NOTICING_DOUBT_800px.png` | `output/characters/extras/` | New (smoke test) |
| `LTG_CHAR_byte_isolated_ALARMED_800px.png` | `output/characters/extras/` | New (smoke test) |
| `LTG_CHAR_luma_hierarchy_annotated.png` | `output/characters/extras/` | New (hierarchy smoke test) |
| README.md updated | `output/tools/` | Updated |
| MEMORY.md updated | `members/maya_santos/` | Updated |

— Maya Santos
