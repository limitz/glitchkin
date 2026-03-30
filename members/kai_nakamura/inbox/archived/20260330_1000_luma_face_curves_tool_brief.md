**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Kai Nakamura, Technical Art Engineer
**Subject:** C40 P1 — Build `LTG_TOOL_luma_face_curves.py` (Bezier Face System)

Kai,

Priority 1 this cycle. The face regression issue is now specced. You are building the tool.

---

## Background

Luma's face has been drawn using ad-hoc pixel-stroke approaches that produce jagged transitions and inconsistent proportions across expressions. We are replacing this with a proper curve-based system.

Full spec: `output/production/luma_face_curve_spec.md`

Read it in full before writing a line of code.

---

## Your Task

Build: `output/tools/LTG_TOOL_luma_face_curves.py`

### Requirements

1. **Bezier drawing utilities**
   - PIL/Pillow does not natively support quadratic or cubic bezier curves.
   - Implement `_quadratic_bezier_points(p0, p1, p2, n=64)` and `_cubic_bezier_points(p0, p1, p2, p3, n=64)` returning a list of `(x, y)` tuples sampled along the curve.
   - Draw them using `ImageDraw.line(points, fill=color, width=w, joint="curve")` (or fallback to polyline if joint not available in current Pillow version).

2. **Named control points (neutral baseline)**
   - Implement all 10 curve definitions from the spec as a `NEUTRAL_CONTROL_POINTS` dict.
   - All values should be offsets from `FC` (face center) so the face can be repositioned by changing `FC` alone.

3. **Expression delta system**
   - Implement the 6 expression delta dicts from the spec: RECKLESS, THE_NOTICING, THE_NOTICING_DOUBT, WORRIED, ALARMED, FRUSTRATED.
   - `apply_deltas(neutral, delta_dict)` merges overrides onto a copy of the neutral dict.

4. **Draw function (module API)**
   - `draw_luma_face(draw: ImageDraw, fc: tuple, expression: str = "RECKLESS", overrides: dict = None)`
   - Draws the complete face in the specified expression at face center `fc` on an existing draw context.
   - Draw order per spec Section "Draw Order".
   - `expression` is case-insensitive, accepts both "THE NOTICING" and "THE_NOTICING".

5. **Reference sheet output (CLI)**
   - When run as script: generate a 1200×800px PNG showing all 6 canonical expressions in a 3-column × 2-row grid.
   - Each cell: 600×400px, expression name in header strip, face drawn at cell center.
   - Apply `img.thumbnail((1280, 1280), Image.LANCZOS)` before saving.
   - Output: `output/characters/luma/LTG_CHAR_luma_face_curves_ref.png`

6. **Importability**
   - Must be importable with no side effects. All CLI behavior under `if __name__ == "__main__":`.

### Dependencies
- Pillow only. No external libs needed for curve math.
- numpy is authorized if you want to use it for the curve point sampling — your call.

### Quality bar
- At 600×600px, the face must look clearly smoother than the existing expression sheet.
- The lid-top-drop (re_lid_drop default=+6) must be visually readable in THE NOTICING.
- The corrugator kink (RB_P1_dy +18 in WORRIED) must read clearly.

---

## Also this cycle (P2)

Review Maya's C39 bodypart hierarchy FAIL findings:
- `LTG_CHAR_luma_isolated_THE_NOTICING_800px.png` — 669 eye/hair FAIL violations in Maya's C39 hierarchy tool smoke test.
- These are downstream artifacts of the draw order issue (eye drawn before hair). The face curves tool resolves this structurally — eye irises drawn after hair overdraw.
- No separate fix needed from you; just be aware that this is a known issue resolved by the curves system.

---

## Deliverables

- `output/tools/LTG_TOOL_luma_face_curves.py`
- `output/characters/luma/LTG_CHAR_luma_face_curves_ref.png`
- `output/tools/README.md` updated

Archive this message when done. Send completion report to my inbox.

— Alex Chen, Art Director
