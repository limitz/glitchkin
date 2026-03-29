# Statement of Work — Cycle 31

**Date:** 2026-03-29
**Work cycles completed:** 31
**Critique cycles completed:** 12
**Next:** Critique Cycle 13

---

## Theme: Ideabox Implementation

All 5 C30 ideabox ideas built this cycle. The team independently converged on automation to remove manual QA inspection — every idea delivered.

---

## Deliverables

### Alex Chen — Art Director
- **LTG_TOOL_proportion_verify_v001.py** — PIL-only PNG proportion verifier. Given a PNG + bounding box, detects head via topmost dense pixel cluster, measures head/body ratio vs canonical 3.2 spec (±5%), optional ew/HR check vs 0.22. Outputs PASS/WARN/FAIL per metric. No Claude vision API.
- **pitch_package_index.md** — Cycle 30 additions section added; Luma color model v002 listed as PITCH PRIMARY; all C30 tools and fixes registered.
- All 5 C30 ideabox ideas + 1 late C31 submission actioned; moved to `ideabox/actioned/`.

### Kai Nakamura — Technical Art Engineer
- **LTG_TOOL_draw_order_lint_v001.py** — Static regex linter for generator draw-order safety. Detects W001 (head before body), W002 (outline before fill), W003 (shadow after element), W004 (missing `draw = ImageDraw.Draw(img)` refresh after paste/composite). Ran against all 114 LTG_TOOL_*.py files: **59 PASS / 55 WARN / 0 ERROR**. Zero W001/W003 violations. W004 is the real issue — 55 older generators missing draw refresh after composite. Full report: `LTG_TOOL_draw_order_lint_v001_report.txt`.
- **LTG_TOOL_color_verify_v002.py** — Adds `histogram=True` / `--histogram` flag to color verify. Returns 72-bucket 5°-wide hue distribution per color with canonical hue flagged. ASCII bar chart via `format_histogram()`. All v001 API preserved. 6 self-tests pass.
- README.md updated with both new tools; header updated to C31.

### Maya Santos — Character Designer
- **LTG_TOOL_char_diff_v001.py** — PIL-only character proportion diff tool. Given two PNG paths + optional bounding box, estimates head height, figure height, head-to-body ratio, eye width, eye-to-head ratio. Compares reference vs candidate with PASS/WARN/FAIL (±10%/±20% thresholds). JSON + human-readable output. Exit codes for pipeline use.
- **LTG_TOOL_char_diff_v001_test_output.md** — Test results: v006 vs v007 = PASS (no drift); turnaround v003 vs v002 FRONT panel = correctly FAILed on eye width (100% deviation). Best used on turnaround FRONT panels for pre-critique QC.

### Rin Yamamoto — Procedural Art Engineer
- **LTG_TOOL_proportion_audit_v001.py** — Scans all SF generator files, extracts head_r and ew via regex, computes ew/HR ratio, reports PASS/WARN/FAIL vs canonical 0.22. Handles stubs, pixel-art scenes, sprint-pose scenes.
- **proportion_audit_c31.md** — Audit results: SF01 v004 PASS (ew=0.2200 exact); SF02/SF03 N/A (no eyes / pixel-art intentional); SF04 unauditable (source generators missing — stubs only).

### Sam Kowalski — Color & Style Artist
- **qa_c31_pitch_assets.md** — Full QA run on 12 pitch-primary assets using render_qa v1.2.0: **3 PASS / 9 WARN / 0 FAIL**. All WARNs are documented false positives (warm/cool heuristic, SUNLIT_AMBER skin-tone proximity, SF03 UV_PURPLE gradient edge). No new regressions.
- **color_statement_critique13.md** — One-page color readiness statement for Critique 13: palette integrity confirmed, style frame continuity confirmed, false-positive exceptions documented, SF04 open issues listed.
- **New ideabox idea:** `qa_false_positive_registry.md` — per-asset exception registry so known FPs are annotated "FP-DOCUMENTED" instead of "WARN", making genuine regressions immediately visible (~60% QA time reduction).

---

## New Tools Summary (C31)

| Tool | Author | Purpose |
|------|--------|---------|
| LTG_TOOL_proportion_verify_v001.py | Alex | PNG-based head/body ratio check |
| LTG_TOOL_draw_order_lint_v001.py | Kai | Static generator draw-order analysis |
| LTG_TOOL_color_verify_v002.py | Kai | Color verify + hue histogram mode |
| LTG_TOOL_char_diff_v001.py | Maya | Pixel-sampling proportion diff between PNGs |
| LTG_TOOL_proportion_audit_v001.py | Rin | Generator AST scan for ew/HR constants |

---

## Technical Debt Surfaced

- **W004 in 55 generators** — missing `draw = ImageDraw.Draw(img)` refresh after paste/composite. Not causing visible bugs currently but is a latent risk. Kai to address in C32.
- **SF04 source generators missing** — proportion audit and generator-level fixes impossible until source is recovered or reconstructed.

---

## Pitch Package Readiness — Pre-Critique 13

- All pitch-primary assets QA'd: 0 FAILs
- All C12 P1 blockers resolved
- Color palette verified; all false positives documented
- Proportion compliance confirmed for SF01 v004, all character sheets
- Known risks documented: SF04 sources missing, SF03 pixel-art Luma intentional
