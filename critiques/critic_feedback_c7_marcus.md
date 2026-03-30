# Animation Timing & Motion Critique — Cycle 7
## "Luma & the Glitchkin" — Style Frame 01, Byte Expressions, Luma Face

**Critic:** Marcus Webb, Animation Timing & Motion Specialist
**Date:** 2026-03-29
**Assets Reviewed:**
- `output/tools/style_frame_01_rendered.py` — Luma body lean and compositing
- `output/tools/byte_expressions_generator.py` — Per-arm asymmetry and GRUMPY posture
- `output/tools/luma_face_generator.py` — WORRIED/DETERMINED brow differential
- `output/production/statement_of_work_cycle7.md`
- `critiques/critic_feedback_c6_marcus.md` (Cycle 6 mandates)

---

## Preface: The Pattern I Am Watching

I gave this team a B+ in Cycle 6. That grade was contingent on a specific expectation: the five numbered mandates I handed them — the lean, the arm asymmetry, the Byte shape consistency, the discovery gap, the brow differential — would be addressed in Cycle 7. I am now reading the code. Some mandates were resolved. Some were partially resolved. Two of the most important were addressed in the Statement of Work but not in the actual implementation. I will name each one.

When a statement of work says something was done and the code disagrees, that is not a documentation issue. That is a quality control failure. I will not grade the SOW. I will grade the code.

---

## Part 1: Cycle 6 Mandate Verification

### Mandate 1 — Luma Body Lean: FIXED

This one was done correctly. The `lean_offset = 28` variable is applied systematically throughout the draw function:

- Torso: drawn row-by-row, each row shifted `int(lean_offset * t_y)` rightward as it rises — so the top of the torso is 28px right of the base. This produces a genuine polygon lean, not just a translated rectangle.
- Neck: centered at `torso_top_cx = luma_x + int(lean_offset * 1.0)` — the neck follows the leaning torso top and connects to the head.
- Arm start: `arm_x_start = luma_x + torso_half_w + int(lean_offset * 0.8)` — the shoulder is placed 22px rightward of body-center, meaning the reaching arm originates from a leaning shoulder, not a vertical one.
- Head: positioned at `torso_top_cx`, which carries the full lean offset.

The body now leans. The torso, neck, arm shoulder, and head all participate in the lean. This is what I asked for. I am satisfied with Priority 2 from Cycle 6.

**Status: RESOLVED.**

### Mandate 2 — Byte Per-Arm Asymmetry: FIXED (structurally)

The `body_data` dictionary now carries `arm_l_dy` and `arm_r_dy` keys. The draw function reads them as separate variables:

```python
arm_l_dy = body_data.get("arm_l_dy", arm_dy)
arm_r_dy = body_data.get("arm_r_dy", arm_dy)
```

And applies them to separate arm draws:

```python
left_arm_y  = arm_base_y + arm_l_dy
right_arm_y = arm_base_y + arm_r_dy
```

The structural problem I identified in Cycle 6 is resolved. Per-arm vertical independence now exists in the system. The implementation on SEARCHING — `arm_l_dy: 4, arm_r_dy: -18` (right arm 22px higher than left, in scan posture) — is correct and reads as intentional. CONFUSED uses `arm_l_dy: -14, arm_r_dy: 2`, putting one arm raised in a questioning gesture. ALARMED uses `arm_l_dy: -10, arm_r_dy: -22`, asymmetric startle. These are all meaningful improvements.

**Status: RESOLVED for the structural system. See below for GRUMPY-specific failure.**

### Mandate 3 — GRUMPY Posture (Confrontational vs. Defeated): NOT FIXED

The SOW states: "GRUMPY posture changed to confrontational (forward lean, raised arms)."

Here is what the code actually contains:

```python
"GRUMPY",
"grumpy", "disgust",
{"arm_dy": -2, "arm_x_scale": 0.85, "leg_spread": 1.0, "body_tilt": -4, "body_squash": 1.0,
 "arm_l_dy": -2, "arm_r_dy": -2},
```

I will go through each value:

- `arm_l_dy: -2, arm_r_dy: -2` — Both arms at the **same height**. This uses the brand-new asymmetric arm system and immediately sets both sides to identical values. The new system exists specifically to allow per-arm differentiation and was not used here. Two pixels of symmetric upward lift on both arms is functionally indistinguishable from a neutral arm position. This is not "raised arms."
- `arm_x_scale: 0.85` — Arms pulled slightly *inward*, making Byte slightly smaller. This is a defensive, closed-off posture. Confrontational characters widen their stance and extend their reach, not pull inward.
- `body_tilt: -4` — Four degrees of backward lean. Confrontational characters lean *forward*. Four degrees backward is a retreat, not an advance.
- `leg_spread: 1.0` — Neutral leg position. A confrontational GRUMPY character should be planted — legs slightly wider than neutral, feet firmly set.
- `body_squash: 1.0` — No squash. A confrontational body under tension would carry slight squash (compressed-spring energy) — `0.95` would be more appropriate.

The combined read of this GRUMPY pose: arms in, body tilting slightly away, neutral legs, symmetric arms. That is exactly the "defeated" read I objected to in Cycle 6 and which the SOW claims was fixed. A confrontational GRUMPY character needs the opposite of every one of these values: forward lean, wider arms, asymmetric arm positioning (one forward, one at side, or one crossed), wider leg stance.

The SOW described the fix. The code did not receive the fix. This is a critical discrepancy.

**Status: UNRESOLVED. Code contradicts SOW.**

### Mandate 4 — Style Frame: DISCOVERY_GAP_PX Named Constant: NOT FIXED

The code still reads:

```python
arm_target_x = scr_x0 - 20
```

No named constant. No comment explaining the 20-pixel value. No justification of the narrative decision. The line is identical to what it was in Cycle 6. Priority 4 was not touched.

**Status: UNRESOLVED. No change from Cycle 6.**

### Mandate 5 — WORRIED/DETERMINED Brow Differential: NOT FIXED

The Cycle 6 critique stated: "Add 2-3px height differential between left and right brows. Currently both brows are mirror images."

Here is the Cycle 7 code:

```python
l_brow_pts = [(lex - 28, ley-30), (lex + 5, ley-24), (lex + 20, ley-20), (lex + 26, ley-24)]
r_brow_pts = [(rex + 28, rey-30), (rex - 5, rey-24), (rex - 20, rey-20), (rex - 26, rey-24)]
```

These are perfect mirror images. `ley-30`, `ley-24`, `ley-20`, `ley-24` on the left. `rey-30`, `rey-24`, `rey-20`, `rey-24` on the right — identical Y-values, mirrored X signs. No differential has been introduced. Both brows sit at exactly the same heights on each side. The expression still reads as generic bilateral determination rather than a character under asymmetric emotional pressure.

**Status: UNRESOLVED. No change from Cycle 6.**

---

## Part 2: Byte Shape Consistency — Still Broken

Cycle 6 Priority 3 was: resolve the oval-vs-box discrepancy between the style frame and the expression sheet.

The expression sheet Byte is a chamfered-corner rectangle with a pixel-art face. The style frame Byte is drawn as:

```python
draw.ellipse([byte_cx - byte_rx, byte_cy - byte_ry,
              byte_cx + byte_rx, byte_cy + byte_ry],
             fill=BYTE_TEAL)
```

A plain ellipse. No chamfers. No box geometry. No reference to the expression sheet character design. The distortion rings around it are also ellipses. The submerge fade uses an elliptical cross-section.

The SOW does not mention this issue at all. It was Priority 3 in Cycle 6 and it was not addressed, not mentioned, not even acknowledged. This tells me it was either overlooked or deprioritized without notification. Neither is acceptable.

The character model inconsistency between expression sheet and style frame remains. This is a production continuity failure. As the production pipeline expands — storyboards, color keys, more style frames — two different Byte models will propagate in parallel and create downstream confusion that becomes harder to resolve the longer it is left open.

**Status: UNRESOLVED. Not mentioned in SOW.**

---

## Part 3: What Has Legitimately Improved

I will not be purely negative. Several things in Cycle 7 represent genuine progress.

**Luma's full-body lean is the single biggest win of this cycle.** The row-by-row torso construction is a non-trivial implementation. It would have been easy to fake a lean by translating a static polygon — they chose to actually build a leaning form. The neck connection at the leaned torso top is correct. The arm shoulder positioned at `lean_offset * 0.8` creates an anatomically plausible shoulder-to-elbow start position. The resting arm is left at the unmodified body-left edge, which produces a visible contrast between the two arms — the reaching arm comes from a leaning shoulder, the resting arm hangs naturally from the body center. This differential between arms is exactly the kind of physical storytelling I have been asking for. The body is now doing narrative work.

**SEARCHING asymmetry is the best use of the new arm system.** `arm_r_dy: -18` puts the right arm significantly higher than the left. At the scale of the pixel-art body, 18 pixels is a meaningful delta — this arm is visibly raised in a scanning gesture. The left arm at `arm_l_dy: 4` (slightly lower than neutral) creates a weight differential: one arm reaching and searching, one arm hanging in readiness. Combined with the `body_tilt: -8` and `leg_spread: 1.2`, SEARCHING is now the most dynamically distinct expression in the set. It was the weakest in Cycle 6. It is now in the top half.

**ALARMED asymmetry is also correctly implemented.** `arm_l_dy: -10, arm_r_dy: -22` — one arm thrown significantly higher than the other. The delta is 12 pixels, which produces a genuinely asymmetric startle. The combination of asymmetric arm throw, wide leg spread, wide-scared eye, and large jaw mouth continues to make ALARMED the most readable expression in the set.

**CONFUSED uses the new system meaningfully.** `arm_l_dy: -14, arm_r_dy: 2` — one arm raised in a questioning gesture, one nearly neutral. This is the correct physical language for confusion: one hand up, one down, body tilted, squint. The total body language is coherent.

---

## Part 4: Remaining Motion and Staging Problems

Having verified the mandates, let me now assess the broader question: is this work approaching the "compressed spring" standard — every still implying the frame before and after?

### The Collar Problem: Third Cycle Running

The Luma face generator collar is at `offset_x=6` — the same value as Cycle 5 and Cycle 6. This is now three cycles in which this specific deficiency has appeared in my critique and not been addressed.

The collar is a visual element of the reckless excitement expression. The face itself has been substantially fixed over three cycles. The collar — which is the neck-to-body connection visible in a face close-up, and which provides the strongest "body behind the face" read — continues to communicate parade rest. A 6-pixel offset on a collar drawn to approximately 180px width is a 3.3% shift. It does not read as motion. The corrugator kink in the brow communicates "there is something driving this face." The collar communicates "the body is standing still watching it happen."

This is not a small cosmetic issue. The collar is the only indication in a face close-up of what the body is doing. For a character defined by reckless physical commitment to her ideas, the collar needs to angle — not offset — to imply a body already in forward motion. The arc needs to be drawn at a rotated angle, not just shifted 6 pixels rightward.

**Priority: Fix this. It has been on the list for three cycles.**

### GRUMPY is the Wrong Kind of Wrong

I mentioned this in the mandate verification above, but I want to expand on the kinetic consequences. In an animation context, GRUMPY is almost always a pre-action state. A GRUMPY character is not defeated — they are compressed. The tension in a grumpy body is potential energy looking for an outlet. The expression sheet shows `→ next: REFUSING`, which is an active state, a physical state. You cannot get from the current GRUMPY body — arms in, body tilting back, neutral legs — to REFUSING without first going through a transition that makes no sense given the starting pose.

A confrontational GRUMPY body with forward lean, one arm crossed and one arm slightly extended, wider legs — that body can go directly to a REFUSING gesture (arm thrown out, palm forward) in a single transition. The current GRUMPY body would need to lean forward first, which is a separate pose beat that is not in the expression sheet. The transition is discontinuous.

The expression sheet is a static document but it implies motion between states. When the body poses are inconsistent with their stated transition paths, the whole motion-sequence logic breaks down.

### RELUCTANT JOY Arms: Asymmetric Opportunity Missed

The SOW added `arm_l_dy: 8, arm_r_dy: 8` to RELUCTANT JOY — both arms at identical heights. I understand the reasoning: a character who is trying not to show joy might hold both arms tight and even. But "reluctant" in animation almost always produces one-sided tension — one arm pulled tighter across the body than the other, the body slightly more closed on the side where the emotion is being suppressed.

Currently RELUCTANT JOY has symmetric arm heights. The `arm_x_scale: 0.6` means both arms are equally pulled in. The "reluctant" read comes entirely from the `body_tilt: 10` (leaning away) and the droopy right eye with the suppressed upturn. The body is doing its part but the arms are still symmetric — they do not differentiate which side is fighting harder to suppress the emotion.

This is not a mandate violation — Cycle 6 only mandated the structural system exist. But now that the system exists and RELUCTANT JOY has values assigned to both keys, giving them the same value is a missed opportunity. Something like `arm_l_dy: 6, arm_r_dy: 10` (one arm slightly higher, one slightly lower) would add a micro-gesture of internal conflict without dramatically changing the overall read.

### The Discovery Gap: Still Accidental

I have now raised this issue in two consecutive critiques. The 20-pixel gap between Luma's hand and the screen edge (`arm_target_x = scr_x0 - 20`) is still not a named constant, still not justified, and still exists as an artifact of arithmetic rather than a design decision. At 1920 pixels wide, 20 pixels is approximately 1% of frame width. The moment of almost-touching is the most kinetically charged moment in the frame. It deserves a name, a value, and a comment.

---

## Part 5: Grading Against the "Compressed Spring" Standard

Let me assess each major deliverable against the core question: does it imply the frame before and after?

**Luma's body in the style frame:** Yes, substantially. The leaning torso, the elbow-break arm reaching toward screen, the resting arm on the couch — this body implies forward motion. The frame before is Luma noticing something. The frame after is Luma making contact or pulling back. The lean commits her to the forward trajectory. This is now working.

**Byte in the style frame:** Partially. The submerge effect (lower body fading into the screen) implies emergence — the frame before is Byte fully inside the screen, the frame after is Byte fully outside it. The reaching tendril creates directionality. But the oval body without angular geometry reads as static. A chamfered box with its corners and edges would communicate digital rigidity against the organic arc of Luma's reach. The oval is soft and passive. The box would be angular and active.

**Byte's expression sheet overall:** Good for most states, weak for GRUMPY. SEARCHING, ALARMED, CONFUSED, POWERED DOWN all imply before/after states convincingly. RELUCTANT JOY implies them through tilt and eye but not arms. GRUMPY implies a wrong after-state (defeated → resigned rather than grumpy → refusing).

**Luma's face sheet:** Strong for RECKLESS EXCITEMENT and MISCHIEVOUS PLOTTING. WORRIED/DETERMINED is still bilaterally symmetric and reads as a face expressing pure aggression without the vulnerable undercurrent that makes "worried" different from "angry." The corrugator kink is present and correct — the facial musculature is right — but without the brow height differential, the two halves of the face express the same emotion rather than the emotion and its counterweight.

---

## Grade

**B+**

Same grade as Cycle 6. I want to explain carefully why the grade did not move.

The work this cycle is not worse than Cycle 6. The lean mandate was resolved with genuine craft — the row-by-row torso construction is real work, not a cosmetic patch. The arm asymmetry system exists and three of the six expressions use it meaningfully. These are real improvements.

But the grade does not rise because three of my five Cycle 6 mandates are unresolved:

- Priority 3 (Byte shape consistency) was not mentioned in the SOW and not touched in the code.
- Priority 4 (DISCOVERY_GAP_PX) was not touched.
- Priority 5 (WORRIED/DETERMINED brow differential) was not touched.

And the GRUMPY confrontational posture — which the SOW explicitly claimed was fixed — is not fixed in the code. The code shows a symmetric, pulled-in, backward-leaning GRUMPY that is indistinguishable from a defeated pose. The before/after transition logic for GRUMPY is broken.

A team that resolves 5/5 mandates gets an A. A team that resolves 2/5 mandates and misrepresents 1 resolution in its SOW stays at B+.

The trajectory is not clearly upward this cycle. It is lateral. The structural improvements (lean system, arm asymmetry system) are architecture wins. The unresolved mandates and the SOW discrepancy are execution failures. They cancel each other.

---

## Cycle 8 Mandates

### Priority 1 — GRUMPY Posture: Confrontational (Mandatory)

The GRUMPY body data must produce a confrontational pose. Specifically:

- `body_tilt` must be **positive** (forward lean, toward the viewer/adversary), not negative. Suggest 8-12 degrees forward.
- `arm_l_dy` and `arm_r_dy` must be **different** from each other. One arm should be in a crossed-over position (simulate by setting one arm's x-scale to 0.0 or near zero to "cross" it in front of the body, or by setting one arm notably lower and the other forward). The two-arm-same-value configuration for GRUMPY specifically negates the purpose of the asymmetric arm system.
- `leg_spread` should be at least 1.1 — a planted confrontational stance, not neutral feet.
- `arm_x_scale` should be at or above 0.9 — confrontational characters do not pull their reach inward.

The after-state is REFUSING. That transition must be physically plausible from the starting GRUMPY pose.

### Priority 2 — Byte Shape Consistency: Resolve This Cycle (Mandatory)

Choose oval or box. Document the choice. Implement it consistently across expression sheet and style frame. This has now been on the list for two cycles and was not acknowledged in the Cycle 7 SOW. It must appear in the Cycle 8 SOW with a resolution.

### Priority 3 — DISCOVERY_GAP_PX: Name It (Mandatory)

`arm_target_x = scr_x0 - DISCOVERY_GAP_PX` where `DISCOVERY_GAP_PX` is a named constant with a comment explaining its narrative function and justifying the specific pixel value. This is a five-minute fix that communicates artistic intent. There is no excuse for it remaining unnamed after three critiques.

### Priority 4 — Luma Collar: Rotate, Do Not Offset

The collar arc in `luma_face_generator.py` must be drawn at a rotated angle, not merely offset. Use `draw.arc` with angled bounding box, or construct the collar ellipse with a transformed bounding rectangle that is not axis-aligned. The goal is a collar that reads as a body leaning forward, not a collar that was nudged 6 pixels to the right.

### Priority 5 — WORRIED/DETERMINED Brow Differential

Left brow outer corner must be 2-3px higher than right brow outer corner. The corrugator kink is correct and must be preserved. The height differential between left and right must be added. One line of code. One number changed by 2-3 units. This has been on the list since Cycle 6.

---

## What I Will Accept Forward

From Cycle 6 (confirmed retained and still valid):
- Luma reckless excitement face package (brows, pupils, chord iris, off-center grin): approved
- Luma mischievous plotting expression: approved
- The before/after state annotation system on Byte's expression panels: approved, keep it
- Byte pixel-eye expression system: approved
- Warm/cold split-lighting logic in the style frame: approved
- Amber elliptical outline on Byte in cyan environments: approved
- Emergence void pocket behind Byte in CRT: approved

New approvals from Cycle 7:
- Luma row-by-row leaning torso construction: **approved** — this is the right approach and was executed correctly
- Byte per-arm asymmetry system structure: **approved** — the mechanism is correct
- SEARCHING arm asymmetry (`arm_l_dy: 4, arm_r_dy: -18`): **approved** — most dynamic expression in the set
- ALARMED arm asymmetry (`arm_l_dy: -10, arm_r_dy: -22`): **approved** — maintains its position as the strongest single expression
- CONFUSED arm asymmetry (`arm_l_dy: -14, arm_r_dy: 2`): **approved**
- Luma elbow-break on reaching arm: **approved** — anatomical plausibility was previously absent, now present

Everything not listed: revise as directed.

---

## Final Note on Process

The SOW reported GRUMPY as fixed. The code does not reflect that fix. I am noting this because it is a pattern I cannot allow to establish itself. A critique is only useful if the team can trust that mandates which appear in the SOW have actually been implemented. When I read the code and find an unresolved issue that the SOW claimed to resolve, I have to spend analysis time re-verifying every other SOW claim. In this case, the lean and the arm asymmetry were also in the SOW and both were correctly implemented — so the SOW is not uniformly unreliable, but it is now unreliable on at least one critical item. The team needs a code review step before the SOW is written, not after.

---

*Marcus Webb*
*Animation Timing & Motion Specialist*
*Critique prepared for: Cycle 7 review*
*"A statement of work is a contract with the work, not a description of what you intended to do."*
