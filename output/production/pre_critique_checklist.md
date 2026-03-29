# Pre-Critique Checklist — "Luma & the Glitchkin"

**Prepared by:** Alex Chen, Art Director
**Date:** 2026-03-29
**Origin:** Actioned from C34 Ideabox idea — `ideabox/20260329_alex_chen_expression_sheet_silhouette_regression.md`
**Cycle created:** C35

---

## Purpose

This checklist is a **mandatory gate** before any expression sheet version is promoted to PITCH PRIMARY or reported as complete to the Art Director. The checklist prevents silhouette regression and format violations from entering the critique cycle.

Every character designer must run and document these checks before filing a completion report. The completion report must include the checklist scores.

---

## Checklist — Expression Sheet Promotion Gate

All items marked **(REQUIRED)** must PASS before promotion. Items marked **(WARN)** may be accepted with documented justification but must be flagged.

### 1. Silhouette Full-Mode Test (REQUIRED)

Run `LTG_TOOL_expression_silhouette_v002.py` in `--mode full` on the expression sheet PNG.

**Requirement:** No pair may exceed **88% similarity** (lower is more distinct).

| Result | Action |
|---|---|
| All pairs ≤ 88% | PASS — proceed |
| Any pair 88%–93% | WARN — document the pair and justify in completion report |
| Any pair > 93% | FAIL — do not promote; revise arm/body poses |

Document the worst pair score in your completion report.

### 2. Silhouette Arms-Mode Diagnostic (WARN — diagnostic only, not a gate)

Run `LTG_TOOL_expression_silhouette_v002.py` in `--mode arms --center-mask 0.36` as a supplemental diagnostic.

This mode is **not a hard gate** (C34 finding: torso dominates arm band at panel resolution). Use it to identify which arms are most similar and target those for further differentiation.

Document in completion report: worst arms-mode pair and score.

### 3. Pose Vocabulary Diversity Check (REQUIRED)

Each expression must have a distinctly different primary arm pose. Check against this vocabulary:

| Pose | Symbol | Can appear once only |
|---|---|---|
| Arms at sides (neutral) | NEUTRAL | Yes — only one neutral per sheet |
| Arms crossed | CROSS | Yes |
| Self-hug (arms wrap chest) | SELF_HUG | Yes |
| One arm raised above head | ARM_HIGH_SINGLE | Yes |
| Both arms raised (Y-shape or V) | ARM_HIGH_BOTH | Yes |
| Arms reaching out (both) | ARM_OUT_BOTH | Yes |
| One arm reaching, one relaxed | ARM_OUT_SINGLE | Yes |
| Fists at hips (elbow flare) | FIST_HIP | Yes |
| One hand to face/chin | FACE_TOUCH | Yes |

**Requirement:** No two expressions on the same sheet may use the same primary arm pose code, with the exception of face/upper-body expressions where arm distinction is contextually impractical (document the exception).

### 4. Line Weight Standards (REQUIRED)

Verify the output PNG conforms to the 3-tier line weight system (per `character_sheet_standards_v001.md` Section 6):

| Tier | Expected output width | Check |
|---|---|---|
| Silhouette / head outline | ~2px | Visual check: silhouette reads clearly heavier than interior lines |
| Interior structure | ~1.5px | Brows, eyelids, costume seams |
| Detail | ~1px | Crinkle lines, decorative stitching |

Silhouette must visibly outweigh interior structure. If both appear the same weight, the generator has a line weight error.

### 5. Eye-Width Canonical Formula (REQUIRED)

If the character uses the `ew = int(head_r_rendered × 0.22)` formula (Luma, Cosmo, Miri), confirm the generator uses the correct value from `character_sheet_standards_v001.md` Section 2.

**Never apply 0.22 to head-diameter or head-height.** Document the `head_r_rendered` value used and the resulting `ew` in your completion report.

### 6. Label Format (REQUIRED)

All expression labels in the output PNG must:
- Be ALL CAPS
- Conform to label format rules in `character_sheet_standards_v001.md` Section 1
- Match the `EXPR_LABELS` dict in the generator source exactly

### 7. Canvas and Grid Standards (REQUIRED)

Verify against `character_sheet_standards_v001.md` Section 5:
- Canvas: 1200×900 (or documented exception)
- Output PNG: ≤ 1280px in both dimensions
- Background: near-void dark `(28, 20, 14)` or character-specific equivalent

### 8. No Regression from Previous Version (REQUIRED)

Compare the new version against the previous version. If any expression is visually worse (less distinctive, less legible at 200px thumbnail, or worse silhouette score), it must be explicitly addressed and improved before promotion.

**Do not accept a new version where any expression is a net regression.**

---

## Completion Report Template

When filing a completion report for a new expression sheet version, include the following section:

```
## Pre-Critique Checklist Results

| Check | Result | Notes |
|---|---|---|
| Silhouette full-mode (worst pair) | [score %] PASS/WARN/FAIL | [pair name] |
| Silhouette arms-mode (worst pair) | [score %] DIAG only | [pair name] |
| Pose vocabulary unique | PASS/FAIL | [any exceptions] |
| Line weight 3-tier | PASS/FAIL | |
| Eye-width formula | PASS/N/A | ew=[px] from head_r_rendered=[px] |
| Label format | PASS/FAIL | |
| Canvas/grid standards | PASS/FAIL | |
| No regression | PASS/FAIL | [note any improved/unchanged expressions] |
```

If any REQUIRED item is FAIL, do not submit the completion report. Fix the issue and re-run.

---

## Enforcement

This checklist is mandatory from **Cycle 35 onward** for all expression sheet promotions.

Alex Chen will reject any completion report that does not include this checklist summary. Critics regularly flag silhouette and line weight issues — these must be caught before critique, not during.

The silhouette test tool is: `output/tools/LTG_TOOL_expression_silhouette_v002.py`

---

*Alex Chen, Art Director — Cycle 35*
