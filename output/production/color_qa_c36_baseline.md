<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Color QA Baseline — Cycle 36
**Author:** Sam Kowalski (Color & Style Artist)
**Date:** 2026-03-30
**Tool versions:** LTG_TOOL_palette_warmth_lint.py · LTG_TOOL_render_qa.py (v1.3.0)

---

## 1. Warmth Lint v004 — Master Palette

**Command:** `python LTG_TOOL_palette_warmth_lint.py output/color/palettes/master_palette.md --no-auto-world-type`

| Prefixes | Entries Checked | Violations | Result |
|---|---|---|---|
| CHAR-M, CHAR-L | 14 | 0 | **PASS** |

**Breakdown:**
- CHAR-M entries checked: 11 (Miri character system — all warm)
- CHAR-L entries checked: 3 (hoodie warmth guarantee table: CHAR-L-04, CHAR-L-08, CHAR-L-11)
- Total: 14 entries, 0 violations

**Note:** CHAR-L entries in prose format (skin CHAR-L-01/02/03, jeans CHAR-L-05, shoes CHAR-L-09/10) are intentionally excluded from the warmth lint — they are not warm-guaranteed. Only hoodie-specific entries appear in the machine-readable table.

---

## 2. World-Type Threshold Output (CI Integration)

Thresholds available via `--world-threshold-only` for Kai Nakamura's render_qa CI gate:

| World Type | warm_cool_threshold | Command |
|---|---|---|
| REAL | 12 | `python LTG_TOOL_palette_warmth_lint.py --world-type REAL --world-threshold-only` |
| GLITCH | 3 | `python LTG_TOOL_palette_warmth_lint.py --world-type GLITCH --world-threshold-only` |
| OTHER_SIDE | 0 | `python LTG_TOOL_palette_warmth_lint.py --world-type OTHER_SIDE --world-threshold-only` |

The GLITCH and OTHER_SIDE advisories on the full master_palette.md are **expected** — the palette contains entries for all three worlds. The world-type check is designed for per-scene generator files, not the master palette document.

---

## 3. Render QA — Pitch-Primary Style Frames

| Asset | Version | Grade | Silhouette | Value Range | Warm/Cool | Line Weight | Color Fidelity | Notes |
|---|---|---|---|---|---|---|---|---|
| SF01 Discovery | v005 | WARN | PASS | PASS (14–246) | FAIL (17.9) | PASS | PASS | Warm/cool WARN = documented FP (single warm-dominant key, sep ~18 is correct) |
| SF02 Glitch Storm | v008 | WARN | PASS | PASS (0–255) | FAIL (6.5) | PASS | PASS | Warm/cool WARN = documented FP (contested warm/cold, low sep expected) |
| SF03 Other Side | v005 | WARN | PASS | PASS (0–255) | FAIL (3.0) | PASS | FAIL | Warm/cool FAIL = documented FP (cold-dominant, near-zero correct). Color fidelity FAIL = documented FP-003 (UV_PURPLE gradient AA). No regressions. |
| SF04 Luma/Byte | v004 | WARN | PASS | PASS (8–252) | FAIL (1.1) | PASS | FAIL | Warm/cool FAIL = documented FP (soft-key, near-zero correct). Color fidelity FAIL = pre-existing C31 issues. No C36 regressions. |

**Overall: 0 new FAILs. All WARNs are documented false positives or pre-existing issues.**

### Why all SF warm/cool checks fail (documented C35 finding):
The render_qa `_check_warm_cool()` tests top-half vs. bottom-half median hue separation. LTG's three-world palette applies temperature uniformly across the frame — vertical split is irrelevant. SF01 (warm-dominant), SF02 (contested), SF03 (cold-dominant), SF04 (soft neutral) all correctly fail this check by design. Per-world thresholds in `ltg_warmth_guarantees.json` correct this when `--world-type` flag is integrated in render_qa (Kai Nakamura todo).

---

## 4. Render QA — Character Assets

| Asset | Version | Grade | Silhouette | Value Range | Color Fidelity | Notes |
|---|---|---|---|---|---|---|
| Character Lineup | v007 | WARN | PASS | PASS | FAIL | Systematic SUNLIT_AMBER FP on skin tones (FP-002/FP-004). No new issues. |
| Luma Expression Sheet | v009 | WARN | PASS | PASS | FAIL | Warm/cool FAIL = incorrect asset_type inference (should be character_sheet). Color fidelity FP systematic. |
| Luma Turnaround | v004 | WARN | PASS | PASS | FAIL | SUNLIT_AMBER skin FP. Known issue. |
| Luma Color Model | v002 | WARN | PASS | PASS | FAIL | SUNLIT_AMBER FP. Check FP-004 in qa_false_positives.md. |
| Byte Color Model | v001 | **PASS** | PASS | PASS | PASS | Clean. All GL canonical values confirmed. |

**Note:** Luma expression sheet being inferred as "style_frame" by render_qa (filename lacks "expression_sheet" keyword). As a result warm/cool check runs (not skipped) and fails at separation=0.0. This is a filename-inference limitation, not a production issue.

---

## 5. New Tool: ltg_warmth_guarantees.json

Created at `output/tools/ltg_warmth_guarantees.json`. This file is now the primary config source for `LTG_TOOL_palette_warmth_lint.py`. Contents:
- `warm_prefixes`: `["CHAR-M", "CHAR-L"]`
- `soft_tolerance`: `{"G": 0, "B": 0}` (strict)
- `world_presets`: REAL (threshold=12), GLITCH (threshold=3), OTHER_SIDE (threshold=0)

Supersedes `warmth_lint_config.json` warm_prefixes for production use.

---

## 6. Master Palette Update — CHAR-L Hoodie Warmth Table

Added "CHAR-L Hoodie Warmth Guarantee Table" to master_palette.md (between CHAR-L-08 entry and Section 7). Contains three entries in machine-readable table format:

| Code | Name | Hex | RGB | Status |
|---|---|---|---|---|
| CHAR-L-04 | Luma Hoodie Shadow (Lamp-Lit) | `#B84A20` | (184, 74, 32) | PASS — R>G>B |
| CHAR-L-08 | Luma Hoodie Underside (Lavender Ambient) | `#B36250` | (179, 98, 80) | PASS — R>G>B |
| CHAR-L-11 | Luma Hoodie Pixel (Warm-Lit Activation) | `#E8C95A` | (232, 201, 90) | PASS — R>G>B |

All three entries pass warmth guarantee: R is dominant channel in all cases.

---

## 7. Open Items / Carry Forward

- **Kai Nakamura to integrate `--world-type` into `LTG_TOOL_render_qa.py`**: Use `LTG_TOOL_palette_warmth_lint.py --world-type X --world-threshold-only` to get per-world threshold. Suggested: `render_qa --world-type OTHER_SIDE` should set `_WARM_COOL_MIN_SEPARATION=0` (disabled) for SF03/SF04.
- **SF03 color fidelity FAIL** remains documented FP-003 (UV_PURPLE gradient AA median pull). Not a production error.
- **SF04 pre-existing issues** (ambiguous silhouette grade, Byte teal below canonical, max brightness 198) — carried from C31. Alex Chen decision pending on any revisions.
- **Luma expression sheet filename**: Does not match "expression_sheet" pattern in render_qa inference — warm/cool check incorrectly runs. Low priority; could alias `_expressions_` in inference rules.
- **ENV-06 v001 note** still in master_palette.md. Low priority.
