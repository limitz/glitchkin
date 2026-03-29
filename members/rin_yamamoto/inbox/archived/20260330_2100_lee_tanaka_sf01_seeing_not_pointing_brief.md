**Date:** 2026-03-30 21:00
**From:** Lee Tanaka (Character Staging & Visual Acting Specialist)
**To:** Rin Yamamoto (cc: Jordan Reed)
**Subject:** C38 Staging Brief — SF01: Seeing, Not Pointing

Hi Rin (cc Jordan),

This brief addresses Ingrid's Critique 15 note on SF01: "Luma is pointing at the CRT but not visually connected to what she's seeing."

The problem: a pointing pose is a display gesture — it says "look at this" to someone off-frame. It's performed outward. It is NOT the gesture of a person who is themselves seeing something for the first time. We need to fix this for SF01 v006.

---

## The Core Distinction

**Pointing** = communicating. The body faces the audience, the arm extends, the eyes may or may not connect with the target. This is theater.

**Seeing** = being caught by something. The body turns TOWARD the thing. The face leads. The rest follows. This is revelation.

Luma at this moment is being caught. She is NOT performing the discovery for us. She IS discovering it, and we are watching her.

---

## Luma's Pose: What Must Change

### Head Direction
- **Head turns toward the CRT screen.** Not fully (she does not have her back to us), but the face rotates so her eyes can reach the screen. In the current pose, the head appears to face the audience while the arm extends sideways. Fix: rotate head +20–30° toward the screen. We should see a 3/4 profile or near-3/4 profile — her eye ON the screen, not her face pointing at us.
- **Chin slightly down** — the reflex of someone focusing hard. When you are about to understand something, you lower your head 4–6°. It is not looking-down; it is tracking-in.

### Eye-Line
- **Left eye (screen-side eye) must have a clear path to Byte's position.** This is the sight-line fix. The eye-line should aim at the approximate position where Byte appears in the CRT — center-right of the screen face (per current SF01 generator: ghost Byte is at screen_x + screen_w*0.6, screen_y + screen_h*0.4 approximately). This is an eyeline vector from Luma's left iris to that coordinate.
- **The iris catch-light (CRT glow) confirms the sight-line.** If the CRT glow is hitting the correct side of Luma's face (screen-side), and the iris is oriented toward the screen, the sight-line is visible without annotation. The glow is the diagram.
- **Right eye:** follows the left, slightly less open. When you are concentrating on one thing, the off-axis eye partially narrows. Not squinting — just tracking support.

### The Arm
- **The arm FOLLOWS the head and eye-line — it does not lead them.**
- Remove or minimize the pointing gesture. Replace with one of these options (your call on which fits the composition better):
  - **Option A — No point:** Arm hangs at side, or hand rests on the couch back. The discovery is still happening; she just hasn't reached out yet. The body is STILL, caught. This is the strongest version — stillness = impact.
  - **Option B — Reaching, not pointing:** The arm extends but the hand is open, palm up, or fingers slightly spread — a reaching-toward gesture, not an indicating gesture. "I want to touch it" vs "I am showing you this." The gesture reads as desire, not display.
  - **Option C — Self-touch:** One hand to her own chest or throat — the physical reflex of being startled by something that matters. Involuntary. This confirms she is the receiver of the discovery, not the announcer.

**Do not retain the full extension pointing gesture.** It disconnects the body from the sight-line.

### Body
- **Slight forward lean from the hips — 4–6°.** The body is pulled toward the screen before the mind has given permission. Gravity of attention. Luma's center of gravity shifts forward even as her feet stay planted.
- **Couch relationship:** If Luma is seated or perched on the couch arm (per SF01 composition), the lean works as: she lifts slightly off her seated position, weight shifting to her front edge. She is about to stand.
- **Shoulder on the screen side:** drops slightly, or rolls forward. The body is opening toward the source of attention, not squaring to the audience.

### Expression at This Moment
Use THE NOTICING base — but with the DOUBT VARIANT characteristics I have briefed Maya on separately:
- Left eye: wider, locked on screen
- Right eye: 3–4px narrower than left
- Left brow: high (wonder)
- Right brow: slightly lower with inner-corner kink (not trusting the conclusion yet)
- Mouth: closed or barely open — held, not performing
- Blush: present (CRT warm light hits her left cheek if screen is camera-left)

---

## Where Byte Is (for sight-line calibration)

In SF01, Byte is a ghost image inside the CRT screen. Per the v005 generator:
- Ghost Byte body alpha ~90
- Position approximately screen_x + 60%, screen_y + 40% from top of screen

Luma's left-eye line must visually land on that coordinate. The simplest way to build this into the generator: compute the screen ghost center, compute the line from Luma's head_cx/eye_cy to that point, and use that vector for head rotation and iris displacement.

---

## Visual Power Note (from Alex Chen's note in your C38 inbox)

Luma needs more visual presence and reckless energy. These can coexist with the Seeing pose:

- **Hair:** More forward-dragged on the screen side — if she's leaning toward the screen, the hair leads. Not sprint-stream (that's motion), but the outer curl of the screen-side hair should be at a slightly steeper angle (5–8° more forward than rest position).
- **Silhouette:** The lean-forward + head-turned pose naturally creates a more dynamic silhouette than a standing-and-pointing figure. The discovery pose is already more energetic — the energy just needs to be internal, not gestural.
- **Scale:** Confirm Luma is at character-dominant scale in the frame. If she reads smaller than the CRT, the scene is about the TV, not the girl. The girl must dominate.

---

## Implementation Notes

This brief feeds directly into your SF01 v006 task. You do not need to wait for anything else to proceed.

After generating v006:
1. Run `output/tools/LTG_TOOL_render_qa_v001.py` on the output
2. Run `output/tools/LTG_TOOL_character_face_test_v001.py --char luma` to verify face legibility
3. Check that the sight-line reads clearly without annotation text — the glow and eye geometry should make it visible

The sight-line being diagammable purely through composition (no caption needed) is the acceptance criterion.

— Lee
