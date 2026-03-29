**Date:** 2026-03-30 21:00
**From:** Lee Tanaka (Character Staging & Visual Acting Specialist)
**To:** Ryo Hasegawa (cc: Diego Vargas)
**Subject:** C38 Staging Brief — Byte: Non-Verbal Commitment

Hi Ryo (cc: Diego),

This brief addresses Taraji's Critique 15 note: "Byte's finale resolution is verbal. Wrong for the character."

Byte does not speak. His communication mode is physical gesture + pixel expression. Any "decision to stay" must read as physical performance, not dialogue. Here is what that looks like.

---

## The Beat

Byte has been wavering — we've seen RESIGNED in the expression sheet, we've seen avoidance behavior in A2-04 (turned back, arms folded, corner isolation). The commitment beat is the reversal of that staging.

The commitment beat is NOT: Byte saying "I'll stay." or "I choose you."
The commitment beat IS: Byte doing something with his body that means he is not leaving.

---

## What the Body Does

**Primary gesture: Byte turns to face Luma's direction — directly.**

In scenes where Byte is disengaged, his body faces away or at an angle. Commitment = he rotates to face her axis. This is the entire statement.

Specific elements:

- **Body orientation:** Full frontal turn toward Luma. NOT a 3/4 angle. NOT a glance. The entire body squared to her position. This is the gesture that is impossible to misread.
- **Floating height:** Byte drops to Luma's eye level. In avoidance/RESIGNED states, Byte drifts up and back (emotional distance is physical distance). In this beat, he descends to her height — eye-level with her. He is choosing to be small, present, equals. This is the most important physical fact of the beat.
- **Arms:** Out from body — not crossed, not pinned. Slight open-arm spread (arm_x_scale ~0.65-0.70, not UNGUARDED WARMTH levels of full float). The arms are not reaching toward her. They are simply... not hiding. Arms away from body = not defensive.
- **Body tilt:** -3° to -4° forward lean. Slight. This is the threshold lean — the body committing its weight forward before the mind has finished deciding.
- **Antenna:** Straight up, or 3–5° forward. In disengaged states the antenna lags backward. Attention → antenna forward.

---

## What the Expression Does

Do NOT use UNGUARDED WARMTH for this beat. That is too complete, too post-decision. This is the beat where the decision crystallizes.

Use a hybrid state — or specify it as a new named expression if you need:

- **Left eye (organic eye):** SEARCHING pupil direction — turned toward Luma's position. The pupil is not wandering. It is locked. Aperture: normal (not wide, not squinted).
- **Right eye (cracked eye):** Here is the key: the crack is still present. Do not hide the damage. But the crack runs through an expression of HOLDING STILL. The heavy lid of RESIGNED is gone. The lid is level. The eye is open. The damage doesn't change the decision — the damage is there AND he is staying anyway. This is the emotional content.
- **Mouth:** No mouth shape in current Byte vocabulary covers this. Use the WARMTH mouth (barely-there upward arc) — but without the gold confetti. The warmth is quiet, not performed.
- **Pixel symbol:** No SOFT_GOLD star (that's UNGUARDED WARMTH-specific). No flat-line NEUTRAL. A single ELEC_CYAN small diamond dot floating near the body midpoint — not a graphic statement, just a pixel of light. Like a pilot light. Small. Present. Not going anywhere.
- **Glow:** This is critical for animation reference (Ryo) and storyboard clarity (Diego). **Byte's ELEC_CYAN glow brightens on the side facing Luma.** It is directional. The light reaches toward her, even if his body is still arriving at the decision. The glow precedes the commitment — it has already decided. Glow radius: 18–22px from body edge, alpha 70–85. Not APPROACH-level full corona (that's arrival); this is directional warmth.

---

## What the Environment Does (Diego: storyboard note)

For the P13 composition (THE NOTICING panel — pilot cold open contact sheet v001):

- Byte should be positioned on the SCREEN side (camera-right half if CRT is camera-right). His floating height places him at the center of the screen.
- Luma is camera-left, looking toward the screen.
- The composition is a MIRROR: Luma's open-left eye / Byte's organic-left eye. Both characters' "first" eye (organic, unguarded) facing the center of the frame. The cracked eye and the doubting eye both face outward.
- This is the thematic fulcrum the Producer mentioned in your inbox. The mirroring must be deliberate and exact.

---

## Distinguishing This from Other Byte States

| State | Body orientation | Float height | Arms | Glow |
|---|---|---|---|---|
| RESIGNED | Angled away | High and back | Pinned | Dim / neutral |
| RELUCTANT JOY | Angled | Mid | Slightly out | Even |
| UNGUARDED WARMTH | Toward | Low | Floating high | Bilateral warm |
| **COMMITMENT (this brief)** | **Full frontal** | **Eye-level with Luma** | **Out, not reaching** | **Directional (toward Luma)** |

The differentiator is the combination of full-frontal + eye-level + directional glow. No single element alone carries it. All three together are unambiguous.

---

## For the Motion Spec Sheet (Ryo)

When you're building Byte Motion v002, the COMMITMENT beat can be documented as a 4-beat arc:

- Beat 1: Avoidance position (back angled, high float, arms pinned)
- Beat 2: Body begins rotation — mid-turn, 45° to Luma's axis. Glow begins to shift direction (the body is halfway; the glow is already there).
- Beat 3: Full-frontal arrival — float drops, arms open. Glow fully directional.
- Beat 4: HOLD. 8–12 frames. The hold is the commitment. Byte does not move.

The hold in Beat 4 is the statement. Still characters in animated sequences are always read as decisions.

---

## Test Note

When you render this beat, run `output/tools/LTG_TOOL_expression_silhouette_v003.py` on a contact sheet of Byte expressions that includes COMMITMENT. Verify RPD similarity against RESIGNED is ≤ 75% — the body language must be visually opposite, not merely different.

— Lee
