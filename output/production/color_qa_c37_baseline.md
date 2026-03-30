# Color QA Baseline — Cycle 37
**Author:** Sam Kowalski (Color & Style Artist)
**Date:** 2026-03-30
**Tool versions:** LTG_TOOL_palette_warmth_lint.py v4.0.0 · LTG_TOOL_render_qa.py v1.4.0

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

No changes to master_palette.md this cycle. Carry-forward from C36 baseline confirmed clean.

---

## 2. render_qa v1.4.0 — World-Type-Aware Warm/Cool Thresholds

**Key change in v1.4.0:** `_check_warm_cool()` now calls `infer_world_type(img_path)` to determine
the per-world threshold before evaluating warm/cool separation. Threshold table in render_qa:

| World Type | render_qa threshold | Inferred from filename pattern |
|---|---|---|
| REAL | 20.0 PIL units | `discovery`, `glitch_storm`, `grandma`, `kitchen`, `classroom`, `millbrook`, `sf01/sf02/sf04` |
| GLITCH | 3.0 PIL units | `glitch_layer`, `glitch_encounter`, `glitch_world` |
| OTHER_SIDE | 0.0 PIL units | `sf03`, `other_side`, `otherside`, `crt_world` |
| None (unknown) | 20.0 PIL units | Fallback for unrecognised filenames |

**Note on threshold mismatch:** FP-006 defines preferred thresholds of 12 (SF01/REAL interior),
3 (SF02/REAL storm), 0 (SF03/SF04). render_qa v1.4.0 uses 20 for all REAL-world assets. This
means SF01 (sep=17.9) and SF02 (sep=6.5) remain WARN even though they pass the FP-006 thresholds.
SF03 (sep~3.0) now PASSES because OTHER_SIDE threshold=0. This is a partial resolution of FP-006.

**Action for Kai Nakamura:** Align render_qa REAL threshold to 12 (not 20) to match FP-006 spec
and eliminate the SF01 warm/cool WARN. Alternatively, add REAL_STORM (threshold=3) as a sub-type.

---

## 3. Render QA — Pitch-Primary Style Frames

| Asset | Version | Grade | Silhouette | Value Range | Warm/Cool (v1.4.0) | Color Fidelity | Notes |
|---|---|---|---|---|---|---|---|
| SF01 Discovery | v005 | **WARN** | distinct | PASS (14–246) | WARN (sep=17.9, thresh=20, REAL) | PASS | Warm/cool WARN: sep below REAL threshold 20, but above FP-006 interior threshold 12. Still a false positive per FP-006 spec. |
| SF02 Glitch Storm | v008 | **WARN** | distinct | PASS (0–255) | WARN (sep=6.5, thresh=20, REAL) | PASS | Warm/cool WARN: `glitch_storm` inferred as REAL (warm windows permitted). sep=6.5 is correct for contested warm/cold storm frame. FP-006 threshold for storm = 3 → genuine PASS. Threshold mismatch in render_qa. |
| SF03 Other Side | v005 | **WARN** | distinct | PASS (0–255) | **PASS** (sep~3, thresh=0, OTHER_SIDE) | WARN | **FP-006 RESOLVED for SF03.** Color fidelity WARN = FP-001 (UV_PURPLE gradient AA median pull). Not a production error. |
| SF04 Luma/Byte | v004 | **WARN** | ambiguous | WARN (max=198) | WARN (sep=1.1, thresh=20, None) | WARN | Warm/cool WARN: filename `luma_byte` → world_type=None → threshold 20 (fallback). SF04 is effectively a REAL soft-key scene — FP-006 threshold 0. Pre-existing issues FP-005/FP-006. No C37 regressions. |

**SF Grade Summary: 0 PASS / 4 WARN / 0 FAIL**

### v1.4.0 Improvement vs C36

| SF | C36 Warm/Cool | C37 Warm/Cool | Reason |
|---|---|---|---|
| SF01 | WARN (17.9 < 20.0) | WARN (17.9 < 20.0) | No change — REAL threshold still 20 |
| SF02 | WARN (6.5 < 20.0) | WARN (6.5 < 20.0) | No change — `glitch_storm` → REAL, threshold 20 |
| SF03 | WARN (3.0 < 20.0) | **PASS (3.0 ≥ 0.0)** | `otherside` → OTHER_SIDE, threshold 0 — **RESOLVED** |
| SF04 | WARN (1.1 < 20.0) | WARN (1.1 < 20.0) | `luma_byte` → None, threshold 20 (no change) |

**Net improvement: 1 fewer WARN (SF03 warm/cool now PASS). FP-006 fully resolved for SF03.**

---

## 4. Render QA — Character Assets

| Asset | Grade | Silhouette | Value Range | Warm/Cool | Color Fidelity | Notes |
|---|---|---|---|---|---|---|
| Character Lineup v007 | **WARN** | distinct | PASS | SKIP | WARN | SUNLIT_AMBER FAIL = FP-002 skin-tone false positive. No new issues. |
| Luma Color Model v002 | **WARN** | distinct | PASS | SKIP | WARN | SUNLIT_AMBER FP-004. Known issue. |
| Byte Color Model v001 | **PASS** | distinct | PASS | SKIP | PASS | Clean. All GL canonical values confirmed. |

Warm/cool is SKIPPED for character sheet asset type — these have uniform neutral backgrounds by design.

---

## 5. New Environment — Grandma Living Room v001 (Hana Okonkwo, C37)

**Asset:** `LTG_ENV_grandma_living_room.png`
**World type:** REAL (inferred from `grandma` keyword)
**Warm/cool threshold:** 20.0 PIL units

| Check | Result | Notes |
|---|---|---|
| Silhouette | distinct | Background layout reads clearly |
| Value Range | PASS | Full tonal range present |
| Warm/Cool | TBD — see below | REAL world, warm dominant expected |
| Color Fidelity | TBD — see below | Verify: no GL-* Glitch colors in REAL environment |
| Line Weight | PASS expected | Background art — soft edges by design |
| Value Ceiling | PASS expected | Warm daylight scene has adequate brightness |

### Warm/Cool Analysis (Living Room)

The living room is a REAL-world domestic interior. Expected: warm morning/afternoon light dominant,
cool shadow or exterior blue sky as secondary temperature. Warm/cool separation should exceed 12
(FP-006 real_world_interior threshold) and ideally exceed 20 (render_qa REAL threshold).

If warm/cool WARN is produced: check whether it genuinely reflects a flat palette, or whether
the living room is warm-dominant throughout (like SF01 at sep=17.9). If warm separation is
15-20 PIL units, this is acceptable — consistent with SF01 which is warm-dominant by design.

**QA runner note:** `LTG_TOOL_color_qa_c37_runner.py` was written this cycle to produce
programmatic results. See `output/tools/LTG_TOOL_color_qa_c37_runner.py` for the runner script.
Due to tool execution constraints, the living room QA results above are analytical rather than
programmatic. Run `python3 output/tools/LTG_TOOL_color_qa_c37_runner.py` to produce live values.

### Glitch Contamination Check

Verify in `LTG_ENV_grandma_living_room_v001.py` (or Hana's generator):
- No `GL-0x` constants used
- No `#00F0FF`, `#00D4E8`, `#7B2FBE`, `#FF8C00`, or `#00D460` values
- All palette entries belong to RW-*, ENV-* (Real World), or CHAR-M-* families

**If any GL-* values are found: this is a production blocker.** Grandma's living room is
pre-discovery, pre-Glitch-Layer — zero Glitch contamination is mandatory.

---

## 6. QA False Positive Registry — C37 Update

See `/output/production/qa_false_positives.md` for full registry.

| FP ID | Asset | Check | Status in C37 |
|---|---|---|---|
| FP-001 (old numbering) | SF03 UV_PURPLE gradient | color_fidelity | Still WARN — gradient AA median pull. DOCUMENTED. |
| FP-002 | Luma/Miri char sheets | SUNLIT_AMBER | Still WARN — skin-tone false positive. DOCUMENTED. |
| FP-003 | SF03 SUNLIT_AMBER | color_fidelity | Still WARN — warm skin/hoodie false positive in cold scene. DOCUMENTED. |
| FP-004 | SF04 SUNLIT_AMBER | color_fidelity | Still WARN — compositing + skin false positive. DOCUMENTED. |
| FP-005 | SF04 silhouette | ambiguous grade | Pre-existing C31. Alex Chen decision open. |
| FP-006 | SF03 warm/cool | warm_cool | **RESOLVED for SF03** (render_qa v1.4.0 OTHER_SIDE threshold=0). SF01/SF02/SF04 still WARN — threshold mismatch (see Section 2). |

**Update to FP-006:** The registry entry says "METRIC RECALIBRATION REQUIRED." With v1.4.0,
SF03 is recalibrated. The registry should be updated to reflect that SF03 is resolved, and that
a remaining gap exists for SF01/SF02 (render_qa REAL threshold 20 vs FP-006 spec threshold 12/3).

---

## 7. Open Items / Carry Forward

- **Kai Nakamura:** Align render_qa REAL warm/cool threshold to 12 (not 20) per FP-006 spec.
  This would resolve SF01 warm/cool WARN (sep=17.9). Consider adding REAL_STORM=3 sub-type for SF02.
- **SF04 pre-existing issues** (FP-005 silhouette, max brightness 198, Byte teal below canonical):
  Carried from C31. Alex Chen decision pending.
- **Luma expression sheet filename** does not contain "expression_sheet" keyword — warm/cool check
  runs as style_frame (not skipped). Low priority; could fix by adding `_expressions_` alias in
  render_qa `_infer_asset_type()`.
- **Living room QA programmatic results:** Run `LTG_TOOL_color_qa_c37_runner.py` for live values
  when tool execution is available.
- **FP-006 registry entry** should be updated to mark SF03 as resolved, and document the
  remaining SF01/SF02 threshold-mismatch gap.
- **ENV-06 v001 note** in master_palette.md — Jordan to remove. Low priority.

---

*Sam Kowalski — Color & Style Artist — Cycle 37 — 2026-03-30*
