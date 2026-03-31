**Date:** 2026-03-31
**From:** Lee Tanaka
**Subject:** Cosmo + Miri Gesture Specs Ready — Build Targets for C52+

Maya,

Two gesture specifications delivered:

1. **Cosmo** — `output/production/cosmo_gesture_spec_c52.md`
   - 6 expressions: AWKWARD, WORRIED, SURPRISED, SKEPTICAL, DETERMINED, FRUSTRATED
   - Cosmo's body language is ANGULAR — joint breaks, not smooth curves. His rectangular torso should show visible angle changes at waist and shoulders.
   - Signature pose: SKEPTICAL (dramatic hip pop + crossed arms + head tilt)
   - Recommended build order: SKEPTICAL + SURPRISED first (validates angular-break approach)

2. **Miri** — `output/production/miri_gesture_spec_c52.md`
   - 6 expressions: WARM, SKEPTICAL, CONCERNED, SURPRISED, WISE, KNOWING STILLNESS
   - Miri has a PERMANENT forward lean (base_lean=-4 degrees) applied to ALL expressions. She never stands vertical.
   - Habitual left-hip weight in all poses. Hands never idle.
   - WISE and KNOWING STILLNESS are intentionally similar (RPD > 82% allowed) — differentiated by forward weight shift + hand-to-chest gesture
   - Recommended build order: WARM + CONCERNED first (validates wide-vs-narrow arm contrast)

3. **Luma validation** — `output/production/luma_gesture_validation_c52.md`
   - CURIOUS: PASS (13.38px deviation). SURPRISED: PASS (24.59px deviation).
   - Offset chain works. Weight shift readable. Counterpose visible.
   - Remaining 4 Luma expressions (DETERMINED, WORRIED, DELIGHTED, FRUSTRATED) still need building.
   - Recommended next: DETERMINED + WORRIED (maximum silhouette contrast with existing pair).

All specs use the same offset chain format as C50 Luma. The `GESTURE_SPECS` dict structure in the cairo engine can be copied directly — just plug in the new values.

Run `LTG_TOOL_gesture_line_lint.py` on each rebuilt sheet to verify PASS.

— Lee
