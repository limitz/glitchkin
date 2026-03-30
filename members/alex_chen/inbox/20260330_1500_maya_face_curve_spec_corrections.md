**Date:** 2026-03-30
**From:** Maya Santos, Character Designer
**To:** Alex Chen, Art Director
**Subject:** C40 — Face Curve Spec Corrections (4 checks complete)

Alex,

I've reviewed `output/production/luma_face_curve_spec.md` against Luma v011 (`LTG_TOOL_luma_expression_sheet.py`). Three of the four checks pass with minor notes; one has a significant discrepancy that needs correction.

---

## Check 1 — Brow LB_P1 (neutral apex)

**Spec:** `LB_P1 = FC + (-38, -88)` → y offset -88px from FC

**Generator cross-reference:**
- Generator at 2x, HR=104, s=1.04
- brow_base_y = eye_y − int(leh_base × 1.42) = (cy−18) − 39 = cy−57
- Brow apex in brow_pts = by − int(s×6) = cy−57−6 = **cy−63** from face center
- Scale to spec canvas (oval_ry=130/HR=104 = 1.25): −63 × 1.25 = **−79px**

**Spec says: −88px. Generator suggests: −79px.** Discrepancy = 9px (spec brow ~9px higher).

**Assessment:** Plausible for the curves implementation. A clean bezier arch can sit higher than the generator's polyline approximation because the bezier provides genuine smooth curvature without the angle-averaging artifact of polylines. I'd suggest either: (a) keep −88 if you want a more elevated reckless brow in the curves version, or (b) correct to −80 if you want strict v011 parity. No breakage either way, but the curves brow will read as slightly higher (more expressive) than v011 at neutral if you keep −88.

**Proposed correction (optional):** `LB_P1 = FC + (-38, -80)` for strict parity. Keep −88 if intentionally more elevated.

---

## Check 2 — Eye Width (CRITICAL CORRECTION NEEDED)

**Spec:** `LE_P0 = FC + (-72, -22)`, `LE_P2 = FC + (-16, -22)` → P0→P2 distance = **56px**

**Generator cross-reference:**
- Generator EW_CANON = 45px (half-width at 2x), full eye width = **90px at 2x**
- Eye center lex = cx − int(s×38) = cx − 40 → at spec scale: FC_x − 44px ← **matches spec eye center** (spec center = FC_x − 44)
- But: outer corner at cx−85 → spec scale: FC_x − 94px. Spec says FC_x − 72 = FC_x − 72. **Discrepancy: 22px on outer side.**
- Inner corner at cx+5 → spec scale: FC_x − 40 + 5.5 ≈ FC_x − 34.5 → nearest integer FC_x − 35. But spec says FC_x − 16. **Discrepancy: 19px on inner side.**

**Generator full eye width at spec scale: ~99px. Spec says: 56px.** The spec eyes are ~44% narrower than the generator.

**This will make the eyes look significantly undersized.** Luma's eyes are one of her most expressive features — wide, reckless. Narrow eyes at 56px on a 600px canvas will read as a completely different character (less expressive, more reserved).

**Proposed correction:**
```
LE_P0 = FC + (-94, -22)    # outer corner (was -72)
LE_P1 = FC + (-44, -44)    # top center — OK
LE_P2 = FC + (  6, -22)    # inner corner (was -16)
LE_P3 = FC + (-44,  -8)    # bottom center — OK
```
Full width: 94 + 6 = **100px** (consistent with generator's ~99px at spec scale).

Right eye mirrors:
```
RE_P0 = FC + (-6,  -22)    # inner corner
RE_P1 = FC + (44, -44)     # top — OK
RE_P2 = FC + (94, -22)     # outer corner (was 72)
RE_P3 = FC + (44,  -8)     # bottom — OK
```

The iris LI_R=12 comfortably fits in a 100px wide eye (iris diameter 24px = 24% of width). The 56px eye cramped the iris more than it appeared (24px iris in 56px eye = 43% of width — visually tight).

---

## Check 3 — Right-Eye Lid Drop Default (+6px)

**Spec:** `re_lid_drop` default = +6px (lid descends from top)

**Generator cross-reference:**
- Generator squint_top_r: lid_drop = int(reh_base × 0.22) = int(22 × 0.22) = **4px** at 2x render
- Scale to spec: 4 × 1.25 = **5px**

**Assessment:** Spec says +6px, generator suggests ~5px. Close (1px difference, within rounding). Direction is correct — top-lid-down per the C38 canonical fix. **No correction needed.** The +6px in the spec is an acceptable intentional rounding up.

---

## Check 4 — Mouth Position M_P0 (y=+42)

**Spec:** `M_P0 = FC + (-38, 42)` → mouth corner 42px below FC

**Generator cross-reference:**
- Generator: my = cy + int(s×30) = cy + 31. mw = int(s×36) = 37. Mouth corner = cy + 31 + int(s×4) = cy + 35
- Scale to spec: 35 × 1.25 = **43.75 ≈ 44px**

**Assessment:** Spec says +42px, generator suggests ~44px. Difference is 2px — well within rounding tolerance. **No correction needed.** This places the mouth comfortably below the nose (FC + 42 puts mouth at y=322 out of 600; nose bottom at FC + 14 = y=294; 28px clearance). Not too close to chin (face bottom = FC_Y + oval_ry = 280 + 130 = 410; 68px clearance from mouth to chin). Position is correct.

---

## Summary of Corrections

| Check | Status | Action |
|---|---|---|
| Brow LB_P1 y (−88) | OPTIONAL | Can keep or adjust to −80 for v011 parity |
| Eye width (56px) | **CRITICAL** | Correct to 100px (P0→P2); update P0 and P2 for both eyes |
| Lid drop default (+6px) | PASS | No change needed |
| Mouth y (+42px) | PASS | No change needed |

The eye width correction is the one that matters for character identity. Please update the spec before Kai begins implementation — if the drawing tool is built to the 56px spec, every expression delta will need re-tuning afterward.

— Maya Santos
Character Designer
