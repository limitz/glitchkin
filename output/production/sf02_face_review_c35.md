# SF02 Luma Face — C35 Review Assessment
**Author:** Lee Tanaka — Character Staging & Visual Acting Specialist
**Cycle:** 35
**Date:** 2026-03-29

---

## Status

SF02 v007 was not yet delivered at time of this review (Rin Yamamoto implementing in C35).
This document records:
1. Pre-implementation baseline assessment (v006 state)
2. Face legibility tool results (run on parametric model at r=23)
3. Acceptance criteria for v007 sign-off

---

## 1. Baseline Assessment — v006 State

**Luma face in v006:** NO FACE DRAWN. The `_draw_luma()` function renders:
- Body: torso ellipse + two arm lines + two leg lines
- Head: skin fill + hair arc (dark + magenta)
- Zero eye geometry, zero brow geometry, zero mouth geometry

**Root cause:** Jordan Reed's v006 was scoped to lighting passes (magenta fill light +
cyan specular). The face implementation task was assigned to Rin for v007.

**Impact:** Third consecutive cycle with no facial expression on the protagonist of the
pitch's most dramatic action frame. Nkechi Adeyemi's C13 critique (69/C+) cited this as
the primary deficit. Two consecutive cycles confirmed.

---

## 2. Face Legibility Tool Results (LTG_TOOL_character_face_test_v001.py)

Tool output: `output/production/LTG_TOOL_face_test_luma_r23_v001.png`
Run parameters: `--char luma --head-r 23 --variants 6 --scale 3`

| Variant             | Result | Notes |
|---------------------|--------|-------|
| NEUTRAL (no face)   | FAIL   | Current v006 state — expressionless |
| FOCUSED DET. (brief spec) | PASS | Left eye r=4, right r=3, L-brow inward, jaw set |
| FEAR (wide+open mouth) | WARN | Reads as fear, not determination — wrong emotion |
| DETERMINED+ (sym brows) | PASS | Valid alt if asymmetric is too complex at scale |
| TOO SMALL (r=2px)   | FAIL   | Eyes below readable threshold at sprint scale |
| EYES ONLY (no mouth) | PASS  | Minimal viable face — acceptable fallback |

**Key finding:** Eye radius ≥ 4px (≥ 0.17 × head_r) is the minimum readable threshold at
sprint scale (r=23). The brief's FOCUSED DETERMINATION spec (eye_r_L=4, eye_r_R=3, asymmetric
brow L-inward, compressed mouth) is confirmed PASS.

---

## 3. Acceptance Criteria for v007 Sign-Off

v007 is acceptable if ALL of the following are true:

**Face elements present:**
- [ ] Two eyes drawn (at least eye_r=3 minimum, eye_r=4 preferred for left)
- [ ] Two brow lines drawn (left brow inner end lower OR right brow level/fractionally raised)
- [ ] Mouth mark drawn (compressed horizontal or small oval, NOT open O)

**Expression reads as DETERMINATION, not fear:**
- [ ] Eyes NOT both symmetric and wide (that's fear/surprise)
- [ ] Brows NOT both arched high (that's surprise)
- [ ] Mouth NOT wide open oval (that's fear or joy)

**Body geometry (brief spec):**
- [ ] Forward torso lean visible (8–12° or equivalent pixel offset)
- [ ] Hair stream angle steeper/more horizontal than v006

**Technical:**
- [ ] Image ≤ 1280×1280px (W=1920 > limit — MUST use thumbnail() or render at 1280W max)
- [ ] Luma char_cx hardcoded for rim light (not full-frame bbox result)
- [ ] Output saved as `LTG_COLOR_styleframe_glitch_storm_v007.png`

**Hard failure conditions (any = reject):**
- No face drawn (NEUTRAL baseline = FAIL, same as v004/v005/v006)
- Eyes rendered at r≤2px (invisible at sprint scale)
- Wide open O mouth (reads as fear — wrong emotional key for this character moment)

---

## 4. What Lee Will Do When v007 Is Delivered

1. Run `LTG_TOOL_expression_silhouette_v002.py` on a Luma-cropped region of the PNG
2. Check silhouette similarity score between NEUTRAL (no face) and v007 face variants
3. If score < 0.72 (passes WARN threshold in --arms mode), the face is differentiating the
   silhouette — acceptable
4. Write final sign-off or revision request to Rin

---

*Lee Tanaka — Character Staging & Visual Acting Specialist — C35*
