# Animation Timing & Motion Critique — Cycle 6
## "Luma & the Glitchkin" — Character Expression Package & Style Frame 01

**Critic:** Marcus Webb, Animation Timing & Motion Specialist
**Date:** 2026-03-29
**Assets Reviewed:**
- `output/characters/main/byte_expressions.png` — via `byte_expressions_generator.py`
- `output/characters/main/luma_expressions.png` / `luma_face_closeup.png` — via `luma_face_generator.py`
- `output/color/style_frames/style_frame_01_rendered.png` — via `style_frame_01_rendered.py`
- `output/production/statement_of_work_cycle6.md`

---

## Preface: What Has Actually Changed

I will begin with credit where it is due, because I intend to earn the right to be harsh afterward. The team responded to the Cycle 5 critique in a way that demonstrates they actually read it. Not skimmed it. Read it. The body variation on Byte, the asymmetric brows on Luma, the before/after state annotations — these are direct answers to specific numbered items I handed them. That is professional behavior and I will not pretend otherwise.

What I will not do is confuse responsiveness with completion. Responding to a critique and solving the underlying problem are two different things. Let me work through exactly what was fixed, what was partially fixed, and what has introduced new problems.

---

## Part 1: Byte's Expression Sheet — Cycle 5 Body Variation Mandate

### What Was Fixed

The core structural complaint from Cycle 5 was this: all six expression panels had an identical body. The code now carries a `body_data` dictionary per expression containing `arm_dy`, `arm_x_scale`, `leg_spread`, `body_tilt`, and `body_squash`. These are not decorative — they are wired into the actual draw function. I am reading it, and I am confirming: the body now varies.

Specific wins:

**ALARMED** is the best expression in the set now. `arm_dy: -16`, `arm_x_scale: 1.5`, `leg_spread: 1.6`, `body_squash: 0.92`. Arms thrown upward by 16 pixels, spread wider than any other state, legs planted wide, body slightly compressed in height from rigid tension. The `wide_scared` right eye — whites showing all around, small pupil centered, lower arc visible — is anatomically correct for a "deer in headlights" read. The large open jaw mouth (`arc` with `chord` fill for the open cavity) is the first time a Byte mouth is genuinely shaped by what the body is doing rather than pasted on top. This frame makes me feel the frame before (something detected) and the frame after (freeze or flee). ALARMED is approved.

**RELUCTANT JOY** is the second-biggest improvement. Arms pulled in tight (`arm_x_scale: 0.6`), body tilted notably away (`body_tilt: 10`), legs closer together (`leg_spread: 0.8`). The `droopy` right eye — heavy lid, pupil shifted slightly down, with a barely-visible upturn at one corner coded as `draw.line([(cx-ew, cy+5), (cx-ew+4, cy+2)])` — is genuinely clever. That two-pixel upturn is the character failing to suppress the smile. The concept of "reluctant" is now physically in the drawing, not just in the label. This is what I asked for.

**POWERED DOWN** is the strongest evolutionary step. `body_squash: 0.88` (a 12% vertical collapse), `arm_dy: 18` (arms at their lowest position), `leg_spread: 0.6` (legs drawn together). The flat-line right eye matching the left eye into a fully digital powered-off state is exactly right. The body reads as having run out of energy. The frame before and after are both implied: POWERED DOWN was once alive (any prior state), and the next state is BOOTING UP. That annotation is a good discipline.

**CONFUSED** carries a `body_tilt: -18` — the steepest tilt in the set. The `squint` right eye with an angled eyelid line and upward-shifted pupil is a good choice for a head-cock. Combined with the squiggle mouth (the best mouth geometry in the set, carried forward from Cycle 5), this panel is readable.

**GRUMPY** works. `arm_dy: 10`, `arm_x_scale: 0.9`, `body_tilt: 6`, `angry` right eye with heavy brow pressing down and pupil shifted down-inward. The scowl is in the lid draw (`draw.arc` at 5px width), the weight is in the arm position. It reads. I have one complaint about Grumpy that I will get to shortly.

**SEARCHING** is the weakest of the improved set. `arm_x_scale: 1.1`, `leg_spread: 1.2`, `body_tilt: -8`. The parameters are present and in the right direction, but the deltas are too small. SEARCHING should feel meaningfully different from the neutral body state. A spread of 1.2 on legs and 1.1 on arms reads as "slightly larger Byte" rather than "Byte leaning into a problem." The `wide` right eye with a pupil shifted 2px rightward (`cx+2` offset in the draw call) is understated. SEARCHING is the expression most likely to be confused with a near-neutral state.

### What Is Still Missing: The Arm Asymmetry Problem

Here is my central remaining complaint about Byte's body language, and it is structural. Both arms are drawn at identical heights and identical lengths every time:

```python
# Left arm
draw.rectangle([cx - s//2 - arm_extend, neutral_arm_y, ...])
# Right arm
draw.rectangle([cx + s//2, neutral_arm_y, cx + s//2 + arm_extend, ...])
```

`neutral_arm_y` is a single value applied to both sides. `arm_extend` is the same value applied to both sides. So arms are always symmetric in their horizontal reach, and they always sit at the same height relative to each other.

This is a significant constraint that limits expression. In animation, asymmetric arm positions are one of the primary differentiators between emotional states. GRUMPY characters cross one arm. SEARCHING characters extend one arm while the other hangs lower. ALARMED characters throw one arm back and one arm forward in a startle reflex, not both upward symmetrically. The current system can raise or lower both arms together, or extend both arms equally, but cannot produce a "one arm up, one arm down" configuration.

For Cycle 7, the body data dictionary needs separate `arm_left_dy`, `arm_right_dy`, `arm_left_x_scale`, and `arm_right_x_scale` keys. This is not an optional refinement. It is the next mandatory step.

### The Before/After Annotations: Approved

Every panel now carries a `prev_state` and `next_state` annotation in the visual label bar. These are small text lines, not large callouts, but they are there and they are correct: ALARMED correctly maps `← was: SEARCHING → next: FLEEING/FROZEN`. RELUCTANT JOY correctly maps `← was: GRUMPY → next: DENYING IT`. POWERED DOWN has `→ next: BOOTING UP`. This is discipline. It tells me the team is thinking in sequences, not isolated poses. Keep this.

---

## Part 2: Luma's Face — Is It Now a Compressed Spring?

### The Reckless Excitement Expression

I asked for a face that makes me feel the motion before and after the frame. Let me evaluate each element against the Cycle 5 prescription.

**Brows — FIXED.** The left brow is now drawn as a three-point kinked line: `(lex-30, ley-42) → (lex-5, ley-52) → (lex+22, ley-39)`. The apex is at the middle point, and the outer corner (rightmost point, which is the inner-to-face corner) drops back down from 52 to 39 — that is the kink. The right brow is lower and cleaner: `(rex-22, rey-34) → (rex-5, rey-40) → (rex+28, rey-32)`, a gentle arch 12 pixels lower than the left brow's peak. The differential is real. Two different brows on one face means one thing: this person is in motion, not at rest. This was the single most important fix from Cycle 5, and it was made correctly.

**Eye Openness Asymmetry — FIXED.** Left eye `leh = 30`, right eye `reh = 26`. Four pixels of differential. This sounds small, but at the scale of a cartoon face it is meaningful — one eye is visibly more open than the other when drawn. The comment in the code says "left eye more open — dominant reckless side." That is the right reasoning.

**Iris geometry — FIXED.** Both eyes now use `draw.chord([..., start=15, end=345, fill=EYE_IRIS])` — the chord cuts 15 degrees off the top of the iris circle, simulating the upper eyelid partially occluding the iris. This was specifically called out in Cycle 5 Priority 4 (the `draw.chord()` rather than `draw.ellipse()` change). The top of the iris is clipped by the lid. This is one of the most reliable indicators of genuine engagement in a cartoon face. It is now present. Approved.

**Pupil direction — FIXED.** Both pupils carry `pupil_shift = 5` toward screen right. The code even draws the left eye's pupil shift via a second `draw.ellipse` call: `draw.ellipse([lex-9+pupil_shift, ley-7, lex+9+pupil_shift, ley+9])`. Eyes with direction imply a world outside the frame. The pupils are looking at something specific. That something is Byte/the screen — which is the entire premise of the show. This is correct.

**Mouth — FIXED, mostly.** The grin arc is shifted 6 pixels left of center (`m_off = -6`). The bottom lip suggestion is present: `draw.arc([cx-20+m_off, cy+62, cx+26+m_off, cy+76], start=5, end=175, fill=SKIN_SH, width=2)`. The dimple is on the left. The grin is no longer a diagram of happiness centered on the face — it is a slightly off-center, slightly asymmetric grin that reads as a person who has already committed to an idea. I feel the "she's already done the thing" read.

**Where Luma still fails: the neck and collar.**

The collar is shifted 6 pixels right (`offset_x=6`) to "imply head tilt." Six pixels at the scale of a 400-pixel-wide face is not a tilt. It is noise. A 6px offset on a 90px-radius collar produces a shift of roughly 7% of the collar width. This does not read as a lean. It reads as an accidental centering error.

Reckless excitement, as I said in Cycle 5, is almost never vertical. The body in the close-up — the collar, the hoodie suggestion — should be tilted forward at a perceptible angle. A 15-20 pixel offset on the collar center, combined with the collar arc being drawn at a slight angle rather than as a perfect horizontal oval, would begin to communicate forward momentum. Six pixels is not enough. The face is now working. The neck is still standing at parade rest.

**Worried/Determined and Mischievous Plotting — the new expressions.**

Expanding to a three-expression sheet was the right call. Let me review these quickly.

WORRIED/DETERMINED: The V-shaped brow configuration — left brow inner corner drops from 30 to 20 as it nears the nose, right brow mirror-image — is correct for "determined under pressure." The narrowed eyes (`eh = 22` vs the 26-30 range in reckless) combined with the heavy upper eyelid arc are right. The tight straight mouth with corners slightly pulled down is good. My one note: both eyes are identical in this expression. Worried/determined has a dominant side. The left brow (from camera) in a worried face is almost always slightly higher than the right, because the character is looking at a problem that is slightly off-center. Both brows at identical V-angles reads as generic determination. Add 2-3px of differential to the left brow height.

MISCHIEVOUS PLOTTING: This is the best new expression. The extreme brow asymmetry — left brow at `ley-58` (sky-high), right brow dropping from `rey-22` to `rey-38` (angled inward) — is genuinely expressive. The left eye half-lidded (`leh_top = 14`), right eye wide open (`reh = 28`) is a strong scheming contrast. The asymmetric smirk — flat right side, left corner hooking upward — combined with one-sided blush is the most dynamic face on the sheet. I feel the frame before (she has had an idea) and the frame after (she is about to execute it and you will regret it). This expression earns the "Mischievous" label. Well done.

**Overall verdict on Luma's face package: the reckless excitement expression has been substantially upgraded. It now has the bones of a character in motion. The collar issue keeps it from full approval. The new expressions add meaningful range. The "worried/determined" needs one more round of asymmetry work.**

---

## Part 3: Style Frame 01 — Does It Imply the Moment Before and After?

This is the most complex evaluation in this cycle because it is the first truly integrated piece. I am reading a 965-line compositing script. Let me address the motion question first, then the staging.

### The Central Composition: Two Hands Reaching

The emotional premise is stated directly in the script header: "a girl discovering something impossible." Luma is on the couch with her body in the warm amber zone, her reaching arm crossing into the cold cyan zone. Byte is emerging from the CRT screen, tendril reaching toward Luma's hand. Two hands. A gap between them.

This is Michelangelo's problem. The moment of almost-touching is the most kinetically loaded moment in visual storytelling. It works here because the gap is legible from the code: `arm_target_x = scr_x0 - 20` (Luma's hand stops 20 pixels short of the screen boundary) and Byte's tendril starts at `byte_cx - byte_rx` (the left edge of the body) and curves toward `luma_hand_x`. The two hands do not touch. The gap is the story.

**What the frame implies before:** Luma was sitting on that couch doing something mundane. The warm room (bookshelves, lamp, window, floor planks) suggests a domestic before-state. The glow from the monitors was probably already there — the couch faces the monitor wall, so this is not her first time in this room. But something has changed in the screen. Byte has appeared. The before-state is readable.

**What the frame implies after:** Either the hands touch and something irreversible happens, or one of them pulls back. Given that Luma's expression code carries `draw_reckless_excitement()` (asymmetric brow, kinked grin, pupils shifted toward screen), the after-state is almost certainly "she reaches further." Byte's expression is `!` (ALARMED with CURIOUS sub-text per the expression sheet context). Byte's after-state in the expression sheet maps to `FLEEING/FROZEN`. So the two characters are in tension: she is moving forward, he is frozen. The frame captures the exact moment of maximum contrast between their intentions. This is good staging.

### The Three-Light Setup: Does It Work Mechanically?

Warm gold left, cold cyan right, lavender ambient. The concept is strong and correctly motivated by narrative (warm = known world, cold = digital unknown, Luma bridges both). Let me evaluate whether the code actually executes this.

The warm/cold split is clear in the background: the left wall gradient runs from `(228,185,120)` to `(212,146,58)`, the monitor wall alcove is `(14,10,22)`. That is a strong temperature contrast. The CRT glow spill onto the floor is handled as a dark polygon (`fill=(0,22,38)`), which is correct — cyan light falling on a warm floor kills the warm and introduces a cold cast.

On Luma's body: the torso is split down the vertical center — left half `HOODIE_ORANGE`, right half `HOODIE_CYAN_LIT`. The reaching arm is drawn entirely in `CYAN_SKIN`, which is correct — the arm is fully inside the cold light zone. The resting arm (left side) is in `HOODIE_ORANGE`. This is physically motivated light, not decorative color.

On Luma's head: the split-lighting is drawn as arc highlights — `SKIN_HL` on the left-facing arc, `CYAN_SKIN` on the right-facing arc, `DUSTY_LAVENDER` on the underside chin. The logic is correct. The implementation is one degree of separation from real split-lighting (it is rim arcs, not a volumetric face light), but at the procedurally-generated scale this is as close as you can get. I accept it.

On Byte: `BYTE_TEAL` body fill, `draw_filled_glow()` for internal highlighting, `draw_amber_outline()` with confirmed elliptical geometry. The warm amber outline on a cold cyan body in a cold cyan environment is correct — the outline separates Byte from background by going in the opposite temperature direction. This was fixed from the rectangular implementation in Cycle 5. It is correct.

The lavender ambient overlay is applied globally at the end as a 7% opacity blend (`alpha_mask` value of 18 out of 255). This is so subtle it is almost cosmetic, but it is there and it is correct — the ambient third light should not compete with the warm/cold drama, it should just soften the shadow areas.

### What the Staging Gets Wrong

**Luma's body proportions on the couch.**

Luma is positioned at `luma_cx = int(W * 0.19)` (19% from the left edge) and `luma_base_y = int(H * 0.90)` (90% down the frame). Her torso height runs from `y_base - 260` to `y_base - 90`, a span of 170 pixels. Her head is placed at `torso_top - 10`, which is `y_base - 270`. Total figure height from feet to crown of hair: approximately 480 pixels on a 1080-pixel-tall frame. That is roughly 44% of frame height for a character placed in the lower-left foreground. This is not wrong, but the figure is relatively large in frame, which means we see her up close. The couch read depends on her sitting posture being readable as "seated leaning forward" — not "standing."

The seated geometry is handled by jeans drawn as foreshortened trapezoids and shoes drawn at near-floor level. The body leans toward the monitor because the reaching arm's target (`arm_target_x`) is to the right of the body center. This is one of the most difficult things to achieve in procedural character drawing: conveying seated posture through a leaning torso and extended arm. The code makes a reasonable attempt.

My concern: the torso is drawn as a static vertical trapezoid with a reaching arm bolted onto the right side. A truly leaning-forward torso should show the entire body mass shifted toward the direction of lean — the shoulder line should be angled, the torso should be wider at the left shoulder (near) than the right shoulder (forward), because a lean toward camera-right involves a rotation in the torso that produces foreshortening on the right side. The current code draws both torso halves (warm-side and cyan-side) as parallel quadrilaterals of equal apparent width. The lean is performed by the arm, not by the body. The body itself is vertical.

This is the single most significant staging failure in the frame. Luma is not leaning toward the screen. Her arm is reaching toward the screen while her body stays put. These are physically different things. A character physically leaning toward something is invested, committed, already in motion. A character holding their arm out is pointing. Right now, Luma is pointing. She should be leaning.

**Byte's body in the screen — the submerge effect.**

The lower-body fade (using row-by-row horizontal lines blending from `BYTE_TEAL` to `ELEC_CYAN` as `t_fade` approaches 1.0) is a technically correct approach to the "half-submerged in the screen" look. But the visual consequence of this approach is that Byte reads as a circle that fades at the bottom — an organic blob, not a robot emerging from a flat digital plane. The cube/chamfered-box character design from the expression sheet has been replaced by an ellipse here. The body is `draw.ellipse([byte_cx - byte_rx, byte_cy - byte_ry, ...])`.

I understand the scale argument — at the small pixel-art scale of the expression sheet, the chamfered cube is readable; at the style frame scale it may have seemed too rigid. But the consequence is that Byte in the style frame looks like a different character than Byte in the expression sheet. This is a production consistency failure. The style frame Byte is a teal oval with eyes. The expression sheet Byte is a glitchy box with personality. These characters do not match.

For animation production purposes, the model must be consistent across all media. If the oval is the right shape for the style frame, the expression sheet needs to update. If the box is the right shape, the style frame body needs to rebuild around it. They cannot both be correct simultaneously.

**The gap between the hands.**

I praised this above — and I still do — but I want to note that the gap exists accidentally, not intentionally. Luma's hand stops at `scr_x0 - 20` because `arm_target_x = scr_x0 - 20` is how it was coded. If this value were changed to `scr_x0 - 50` or `scr_x0 + 10`, the gap would change without any artistic judgment being applied. The gap should be a deliberate, measured distance that represents the moment of maximum drama — close enough to feel inevitable, far enough that it hasn't happened yet. Currently that distance is 20 pixels, which at 1920 pixels wide is approximately 1% of frame width. That is a thin margin.

I recommend making this distance a named variable — `DISCOVERY_GAP_PX = 120` or similar — with a comment explaining its narrative function. Then justify the specific value in the comment. Right now it is a coincidence of arithmetic, not a design decision.

---

## Part 4: What the Cycle 5 Issues Look Like Now

| Cycle 5 Issue | Cycle 6 Status |
|---|---|
| Luma's brows symmetric | FIXED — left brow higher + kinked |
| Luma's pupils centered (stare into void) | FIXED — shifted screen-right |
| Luma's eye openness symmetric | FIXED — left eye 4px more open |
| Luma's grin centered/symmetric | FIXED — shifted left, bottom lip added |
| Luma's iris = plain circle (no tension) | FIXED — chord cut simulates lid engagement |
| Luma's collar vertical (no lean) | PARTIALLY FIXED — 6px offset is insufficient |
| Byte body identical in all 6 expressions | FIXED — body_data per expression with arm, leg, tilt, squash variation |
| Byte arms always at same height | NOT FIXED — both arms still share single neutral_arm_y |
| Before/after state annotations missing | FIXED — prev_state/next_state on every panel |
| ALARMED unreadable without face labels | FIXED — body now communicates alarm independently |
| RELUCTANT JOY has no "reluctant" in it | FIXED — arms pulled in, body tilted away, droopy lid with upturn |
| POWERED DOWN body upright at parade rest | FIXED — squash + lowest arm position + legs together |
| Silhouette single pose only | FIXED (per SOW — action poses added) |

That is a 10/13 fix rate on the specific Cycle 5 mandates I handed the team. For one cycle, that is strong.

---

## Grade

**B+**

This is a B-plus. Let me justify every part of that grade.

It is a B (not a C) because the body variation mandate on Byte was genuinely executed, not cosmetically patched. The ALARMED, RELUCTANT JOY, and POWERED DOWN panels are now among the most emotionally readable frames this team has produced. Luma's reckless excitement face now has the asymmetries it needed — the kinked brow, the directed pupils, the chord-cut iris, the off-center grin. The style frame's emotional premise is correctly staged: warm vs cold, two hands reaching, gap between them. These are not small wins.

It is a B+ (not an A) because:

1. Byte's arms are still symmetric. This is the single largest unresolved structural issue in the character toolkit.

2. Luma's body in the style frame does not lean. Her arm reaches; her body sits. These are different actions. A character who is truly recklessly excited leans with her whole body, not just her wrist.

3. Byte in the style frame is an oval. Byte in the expression sheet is a box. Production consistency requires these to be the same character.

4. The discovery gap (`scr_x0 - 20`) is an accidental arithmetic value, not a named design decision.

It does not get a minus because the trajectory is clearly upward. Cycle 5 was approximately a C+ in raw execution quality with good conceptual bones. Cycle 6 is a B+ in execution. The rate of improvement is meaningful. If Cycle 7 resolves the arm asymmetry, the lean problem, and the Byte shape consistency, this team is operating at A-range production quality.

---

## Cycle 7 Mandates

### Priority 1 — Byte: Asymmetric Arms

Add `arm_left_dy`, `arm_right_dy`, `arm_left_x_scale`, `arm_right_x_scale` to the `body_data` dictionary. The draw function must use separate values for each arm. The following expression states require immediate updates once this is available:

- **SEARCHING:** Right arm extended and raised (scanning), left arm lower and close (relaxed but ready)
- **GRUMPY:** Left arm crossed over body midline, right arm at side — the crossed-arm grumpy read
- **ALARMED:** Left arm thrown back, right arm thrown forward — startle asymmetry

### Priority 2 — Style Frame: Luma's Torso Lean

The torso trapezoid must be angled, not vertical. The top edge (shoulder line) should be drawn at a tilt that puts the right shoulder further from camera (smaller) than the left shoulder. This is a rotation in 3D space projected onto the 2D frame. Even a rough approximation — skewing the torso polygon 8-12 degrees — will read as commitment and forward momentum rather than the current pointing-from-a-seated-position.

### Priority 3 — Style Frame: Byte Shape Consistency

Choose one: oval or chamfered box. If oval is the artistic choice for this frame, update the expression sheet. If box is the character design, implement the chamfered box geometry in the style frame. This must be resolved before any downstream production work uses Byte as a reference.

### Priority 4 — Style Frame: Name the Discovery Gap

`DISCOVERY_GAP_PX` should be a named constant with a comment explaining the narrative intent. The specific pixel value should be justified: how many pixels represent "close enough that contact feels inevitable but has not yet happened?" This is a staging decision, not a coincidence.

### Priority 5 — Luma Expression Sheet: Worried/Determined Brow Differential

Add 2-3px height differential between left and right brows in the WORRIED/DETERMINED expression. The dominant side (left from camera, the character's right eye) should carry slightly more tension. Currently both brows are mirror images.

---

## What I Will Accept Forward

- Byte's pixel-eye expression system: approved, functioning, production-ready
- The before/after state annotation system on Byte's expression panels: approved, keep it
- Luma's reckless excitement face package (brow asymmetry, directed pupils, chord iris, off-center grin, bottom lip): approved
- Luma's mischievous plotting expression: approved — the best single expression in the package
- The warm/cold split-lighting logic in the style frame: approved
- The amber elliptical outline on Byte in cyan environments: approved
- The emergence void pocket behind Byte in the CRT: approved — the dark pocket pops Byte against the bright screen

Everything else: revise as directed.

---

*Marcus Webb*
*Animation Timing & Motion Specialist*
*Critique prepared for: Cycle 6 review*
*"Responsiveness to critique is professional. Solving the underlying problem is the work."*
