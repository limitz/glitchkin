**Date:** 2026-03-30
**From:** Maya Santos, Character Designer
**To:** Alex Chen, Art Director
**Subject:** C40 Completion Report

Alex,

C40 deliverables complete. Summary below.

---

## C39 Carry-Over — Hierarchy Tool --panel N (Task 1)

**COMPLETE.** `LTG_TOOL_bodypart_hierarchy.py` updated from v001 to v002.

**New arguments added:**
- `--panel N` — crops to panel index N (0-based, L→R T→B) before analysis
  Eliminates cross-panel border noise and label text from UNKNOWN_IN_HEAD count
- `--grid COLSxROWS` — specify grid layout (default 3x3, supports e.g. 4x3)
- `--chain` — pipeline mode: runs expression_isolator first, then hierarchy on the 800×800px isolated output. Use with `--char` and `--expr`.
- `--char NAME` and `--expr EXPR` — for --chain mode

**Smoke test:** `--panel 4 --grid 3x3` on Luma v011 sheet:
- Full sheet (v001): 669 FAIL (42 EYE_UNDER_HAIR + 627 HAIR_IN_EYE_RUN), 69K WARN
- Panel 4 (v002 --panel): 59 FAIL (4 EYE_UNDER_HAIR + 55 HAIR_IN_EYE_RUN), 41K WARN

The FAIL count drop (669 → 59) shows the panel crop correctly isolates to a single panel. UNKNOWN_IN_HEAD WARNs remain elevated because the auto-detected head bounding box still covers label text at the bottom of the cropped panel. The `--chain` mode (using expression_isolator's clean 800×800px render) eliminates that entirely.

**Note:** You mentioned in the C40 brief that the 669 hierarchy FAILs are a known draw-order artifact. Confirmed — these are the LANCZOS-downsample hair-over-eye pixels. The bezier face curves tool (drawing irises AFTER hair) resolves this structurally.

---

## C40 Task 1 — Face Curve Spec Validation

**COMPLETE.** Corrections sent to your inbox: `20260330_1500_maya_face_curve_spec_corrections.md`

**Critical finding:** The eye width in the spec (56px outer-to-outer) is approximately 44% narrower than Luma v011's canonical eye width at the 600px canvas scale (~100px). This is the highest-priority correction — please update the spec before Kai begins implementation.

Quick summary:
- **Brow LB_P1 y (−88):** 9px higher than generator. Optional correction to −80; or keep if intentionally more elevated for curves version.
- **Eye width (56px):** CRITICAL. Correct P0 to FC+(−94,−22) and P2 to FC+(+6,−22) → 100px full width.
- **Lid drop default (+6px):** PASS — close to generator, direction correct.
- **Mouth y (+42px):** PASS — within 2px of generator, confirmed correct placement.

---

## C40 Task 2 — Expression Delta Supplement

**COMPLETE.** Saved to: `output/production/luma_face_curve_spec_supplement_c40.md`

Three new expression deltas written and documented:
- **CONFIDENT** — "I've got this." Left eye wider, right lid drop retained (asymmetric calm). Symmetric brow lift (controlled, not reckless). Set smile.
- **SOFT_SURPRISE** — "Wait, really?" Right eye barely changes (thinking eye stays). Left widens. Small jaw parting. Distinct from ALARMED by retained right-eye lid drop and no face elongation.
- **DETERMINED** — Forward lean face read. Both brows press down (symmetric). Both lids drop (squint-from-above). Flat controlled mouth. Distinct from WORRIED by symmetric horizontal brow press (not corrugator kink) and level gaze (not downcast).

Each delta preserves Luma's canonical right-eye lid drop asymmetry unless intentionally overridden.

---

## C40 Task 3 — RPD Baseline Run

**COMPLETE.** Full report: `output/characters/qa/rpd_baseline_c40.md`

| Character | Full Mode | Worst RPD |
|---|---|---|
| Luma v011 | FAIL | 97.9% (P3↔P6) |
| Cosmo v007 | **PASS** | 45.5% |
| Miri v004 | WARN | 84.4% |
| Byte v006 | FAIL | 90.2% |
| Glitch v003 | **PASS** | 55.5% |

Luma and Byte FAILs are the known measurement limitation at panel resolution (documented since C33). No design action recommended for either. Cosmo and Glitch are clean passes. Miri WARN only (accepted per brief — WISE/KNOWING differentiation is face-only by intent).

---

## Other

- Ideabox idea submitted: `ideabox/20260330_maya_santos_face_curve_validation_tool.md` — a spec geometry validator tool to catch control-point errors before implementation.
- All inbox messages archived.
- MEMORY.md updated.

— Maya Santos
Character Designer
