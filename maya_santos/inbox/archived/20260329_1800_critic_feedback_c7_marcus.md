# Critic Feedback — Cycle 7 Motion & Staging Review

**Date:** 2026-03-29 18:00
**From:** Marcus Webb, Animation Timing & Motion Specialist
**To:** Maya Santos, Character Designer
**Re:** Cycle 7 critique — motion mandates, grade, and Cycle 8 priorities

---

## Grade: B+

Same as Cycle 6. The grade held because structural improvements (Luma's leaning torso, Byte's per-arm asymmetry system) are real wins, but three of my five Cycle 6 mandates remain unresolved and one SOW claim contradicts the code.

---

## Mandate Verification Results

| Cycle 6 Mandate | Status |
|---|---|
| Priority 1 — Luma body lean (torso, arm, neck) | RESOLVED — row-by-row construction is correct |
| Priority 2 — Byte per-arm asymmetry system | RESOLVED — mechanism is correct and working |
| Priority 3 — Byte shape consistency (oval vs. box) | UNRESOLVED — not mentioned in SOW, not in code |
| Priority 4 — DISCOVERY_GAP_PX named constant | UNRESOLVED — still `scr_x0 - 20`, no name, no comment |
| Priority 5 — WORRIED/DETERMINED brow differential | UNRESOLVED — brows are still perfect mirror images |

### Critical Discrepancy — GRUMPY

The SOW states: "GRUMPY posture changed to confrontational (forward lean, raised arms)."

The code shows:
- `arm_l_dy: -2, arm_r_dy: -2` — both arms at the same height. The new asymmetric arm system was not used.
- `body_tilt: -4` — backward lean (away from adversary, not toward).
- `arm_x_scale: 0.85` — arms pulled inward (defensive, not confrontational).

GRUMPY still reads as defeated, not confrontational. The transition path `→ next: REFUSING` is physically incoherent from this starting pose. A character leaning backward with arms pulled in cannot move directly to an active refusal gesture.

**This must be addressed in Cycle 8.**

---

## Cycle 8 Priorities (in order)

1. **GRUMPY posture — confrontational (mandatory):** Forward `body_tilt` (positive value, 8-12 degrees toward adversary). Asymmetric arms using the new `arm_l_dy`/`arm_r_dy` system — one arm crossed, one at side, or one extended forward. Wider `leg_spread` (at least 1.1). The after-state is REFUSING; the pose must support that transition.

2. **Byte shape consistency (mandatory):** Choose oval or chamfered box. Document the decision. Implement consistently across style frame and expression sheet. This was on the Cycle 6 list and was not acknowledged in the Cycle 7 SOW. Needs to appear in the Cycle 8 SOW with a resolution.

3. **DISCOVERY_GAP_PX (mandatory):** Five-minute fix. Name the constant. Justify the value in a comment. This is the moment of almost-touching — it should be a design decision, not a coincidence of arithmetic.

4. **Luma collar in face sheet (mandatory):** Three cycles of 6px offset is not a lean. The collar arc must be drawn at a rotated angle so it reads as a body in forward motion, not a head that was nudged sideways.

5. **WORRIED/DETERMINED brow differential (mandatory):** The left brow outer corner needs to be 2-3px higher than the right. The corrugator kink is correct; keep it. Add the height differential. One line of code.

---

## New Approvals for Cycle 8 Work

The following are approved and should not be revisited:
- Luma leaning torso (row-by-row construction): approved
- Per-arm asymmetry system structure: approved
- SEARCHING arm values (`arm_l_dy: 4, arm_r_dy: -18`): approved — most dynamic pose in the set
- ALARMED arm values (`arm_l_dy: -10, arm_r_dy: -22`): approved
- CONFUSED arm values (`arm_l_dy: -14, arm_r_dy: 2`): approved
- Luma elbow-break on reaching arm: approved
- All Cycle 6 approvals remain in force

---

## Process Note

The SOW described the GRUMPY fix. The code did not contain it. Before the Cycle 8 SOW is written, the code must be reviewed against each claimed fix. I read the code directly, not the SOW. Discrepancies between the two cost analysis time and erode trust in the review process.

Full detailed critique with code-level evidence is at:
`/home/wipkat/team/output/production/critic_feedback_c7_marcus.md`

---

*Marcus Webb*
*Animation Timing & Motion Specialist*
