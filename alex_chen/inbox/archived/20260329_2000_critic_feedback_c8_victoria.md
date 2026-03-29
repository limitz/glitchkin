# Critic Feedback — Cycle 8 — Victoria Ashford
**Date:** 2026-03-29 20:00
**From:** Victoria Ashford, Visual Development Consultant
**To:** Alex Chen, Art Director
**Subject:** Cycle 8 Review — Style Frame 01 — Grade B+

---

## GRADE: B+

Four of five Cycle 7 issues are genuinely fixed. The frame is now structurally sound and the emotional center — the charged gap between the two hands — is the best single addition to date. The screen-glow conceptually integrates Byte. The tendril correctly arcs toward Luma. The lighting overlay is perceptible.

---

## VERIFICATION SUMMARY

| Issue | Status |
|-------|--------|
| 1. Lighting overlay alpha raised (60-80) — perceptible warm/cold split | FIXED — peak alpha ~65 warm / ~56 cold; compositing correct |
| 2. Charged gap — luminous event at emotional midpoint | FIXED — well-executed glow + 18px scatter; best new addition |
| 3. Tendril direction — CP1 arcs toward Luma | FIXED — cp1x now places control point one-third toward Luma |
| 4. Byte screen-glow — upward ELEC_CYAN on underbody | FIXED conceptually — but see Priority 1 below |
| 5. Couch scale — 768px / 40% of frame | **NOT FIXED — third consecutive cycle** |

---

## FOUR NEW PROBLEMS FOR CYCLE 9

**Priority 0 — Couch scale. This will not be deferred a fourth time.**
`couch_left = int(W * 0.04) = 77px`, `couch_right = int(W * 0.44) = 845px`. Span = 768px = 40% of frame. Luma's body = 88px wide. Ratio = 8.7:1. A readable ratio is 4:1 or less. Fix: move `couch_left` to approximately `W * 0.16` and `couch_right` to `W * 0.38` — approximately 420px span, still generous.

**Priority 1 — Screen-glow / submerge vertical overlap.**
`screen_glow` is centered at `byte_cy + 0.55 * byte_ry`. The submerge effect starts at `byte_cy + 0.50 * byte_ry` and paints near-black rows over the same region. These two effects overlap from ~0.50 to ~0.85 of `byte_ry`. The submerge likely paints over the screen-glow before it reaches the viewer. Separate the vertical ranges: either start the submerge at `0.70 * byte_ry` or confine the screen-glow to the bottom-most quarter only.

**Priority 2 — False code comment at line 1157.**
"body at 29% means arm span is ~21% of canvas" — this is incorrect. The computed geometry produces 28%. The comment has been false since Cycle 7 and was carried into Cycle 8 unchanged. Correct it.

**Priority 3 — Verify draw-order interaction between atmospheric overlay and characters.**
Characters are drawn at STEP 3-5 with baked-in lighting. The atmospheric overlay is applied at STEP 6 on top of the characters. This means warm gold is composited onto Luma's already-warm hoodie and cold cyan onto her already-cyan arm. At 25% opacity this may be tolerable, but it has not been checked. Run the output and confirm the arm is not washed out and the hoodie is not yellowed. If either is happening, apply the overlay before drawing the characters or reduce the alpha.

**Priority 4 (scene dressing) — Add mid-frame transitional interest.**
The zone x=768–960 (between the lamp and the monitor wall boundary) is visually inert. This is the literal crossing point between Luma's world and Byte's world. Anything that catches both warm and cold light simultaneously — a cable on the floor, a cushion edge catching rim light, a dust haze — would dramatically intensify the sense that two worlds are meeting here.

---

## PATH TO A-

Fix the couch (Priority 0). Resolve the screen-glow/submerge overlap (Priority 1). Confirm the overlay does not overcook character fills (Priority 3). Those three items, confirmed in the rendered output, produce an A-.

Full critique at: `/home/wipkat/team/output/production/critic_feedback_c8_victoria.md`

---

*Victoria Ashford*
*2026-03-29 20:00*
