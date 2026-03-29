**Date:** 2026-03-29 21:00
**To:** Maya Santos
**From:** Alex Chen
**Re:** CRITICAL — Luma Style Alignment: Expression Sheet v005 Must Match Classroom Pose

---

## Problem Statement

The producer has flagged a visual inconsistency: `LTG_CHAR_luma_expression_sheet_v005.png` looks like a different character from `LTG_CHAR_luma_classroom_pose_v002.png`. The classroom pose is the preferred style. The expression sheet v005 must be rebuilt to match it.

This is a **v006 rebuild of the expression sheet** — full regen, not a patch.

---

## Specific Differences Identified (Generator Analysis)

I compared the two generators line by line. Here is what is wrong with v005 and what the classroom pose does right:

---

### 1. LINE WEIGHT — Critical

**Classroom pose (correct):** `outline=LINE, width=2` to `width=3` on head ellipse, arms, body. Clean, moderate weight. Lines feel hand-drawn at comfortable weight.

**v005 (wrong):** `outline=LINE, width=6` to `width=8` on head, eyes, hair. These are nearly twice as heavy. At 1200×900 output this produces thick, cartoony outlines that look overworked and different from the pose sheet style.

**Fix:** Reduce all outline widths in v005 to match classroom pose — `width=2` for detail, `width=3` for structure, `width=4` only on the head outline. Three-tier line weight.

---

### 2. HAIR CONSTRUCTION — Critical

**Classroom pose (correct):** Hair is drawn as 8 overlapping small-to-mid ellipses that individually suggest curls/cloud shapes. There is visual texture and curl identity. `draw.ellipse([cx-155, cy-195, cx+145, cy+40], fill=HAIR)` + 7 more. Plus foreground strand arcs: `draw.arc([cx-60, cy-195, cx-10, cy-140], ...)` for strand detail.

**v005 (wrong):** Hair is drawn as 2-3 large mass ellipses + fringe ellipses + a Bezier highlight. This produces a flat, solid hair blob with a single smooth outline. No individual curl suggestion. The character reads as having a smooth helmet, not the textured curly cloud of the classroom pose.

**Fix:** Rebuild hair in v006 using the classroom pose's multi-ellipse curl approach. Use 7-9 overlapping ellipses of varying sizes. Add foreground strand arcs for texture. Keep the Bezier highlight line — that is the one good element in v005's hair.

---

### 3. HEAD CONSTRUCTION — Moderate

**Classroom pose (correct):** Head is drawn as a primary ellipse + extended chin ellipse + cheek nub ellipses (`cx-head_r-12` to `cx-head_r+14`). The cheek nubs give Luma her signature soft, round cheek protrusion. Head radius: `head_r = 100`.

**v005 (wrong):** Head is drawn as a primary ellipse + small jaw ellipse only. No cheek nub ellipses. The result is a simpler, more generic head shape that loses Luma's cheek character. HEAD_R = 52 (scaled 2x to 104 — effectively same size, but construction differs).

**Fix:** Re-add the cheek nub ellipses to v006. Left cheek: `cx - head_r - 12` to `cx - head_r + 14`. Right cheek: `cx + head_r - 14` to `cx + head_r + 12`. These are small but they define her face shape.

---

### 4. HOODIE COLOR — Moderate

**Classroom pose:** `HOODIE_C = (120, 155, 130)` — muted sage-green. This is the At-Rest Curiosity hoodie, intentionally desaturated.

**v005:** `HOODIE = (232, 112, 42)` — bright HOODIE ORANGE. Expression-specific. This is correct for pitch export (each expression should have a mood-tinted hoodie per the v005 spec). However the per-expression hoodie color variation itself is fine — keep it. The issue is construction, not color.

**Note:** Keep the per-expression hoodie color map from v005. It was a good design decision.

---

### 5. SKIN PALETTE — Minor

**Classroom pose:** `SKIN = (200, 136, 90)`, `SKIN_SH = (168, 104, 56)`, `SKIN_HL = (232, 184, 136)`.

**v005:** `SKIN = (200, 136, 90)` (matches), `SKIN_SH = (160, 104, 64)` (very close), `SKIN_HL = (223, 160, 112)` (slightly different). These are close enough — no change required.

---

### 6. RENDER APPROACH — Note

**v005** uses a 2× render scale with LANCZOS downsample. This is a good technique for AA quality. Retain it in v006.

However, the line width values specified must account for the 2× render factor. `width=3` at output becomes `width=6` in the render buffer — which matches the heavy lines we are seeing. **Solution:** At 2× render, use `width=3` for structure lines and `width=4` for head outline. After downsampling, these will read as ~1.5 and 2px respectively at output — clean and appropriate.

---

## Summary of Changes Required for v006

| Element | v005 (wrong) | v006 (target = classroom pose style) |
|---------|-------------|--------------------------------------|
| Line weight | width=6–8 (too heavy) | width=3–4 at 2× render (=1.5–2px output) |
| Hair construction | 3 large mass ellipses, smooth outline | 7–9 curl ellipses + foreground strand arcs |
| Cheek nubs | Missing | Restore left+right cheek nub ellipses |
| Head outline | Single ellipse+jaw | Primary ellipse + chin + cheek nubs |
| Per-expression hoodie color | Keep as-is | Keep |
| 2× render + LANCZOS | Keep | Keep |
| Full-body silhouette differentiation | Keep | Keep — this was the correct C25 fix |
| 6-expression 3×2 layout | Keep | Keep |

---

## Output Target

- `output/characters/main/LTG_CHAR_luma_expression_sheet_v006.png`
- Generator: `output/tools/LTG_CHAR_luma_expression_sheet_v006.py`
- Canvas: 1200×900, 3×2
- Reference: `LTG_CHAR_luma_classroom_pose_v002.png` is the style benchmark

Report back when complete.

— Alex Chen, Art Director
