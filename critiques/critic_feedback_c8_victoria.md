# Critique — Cycle 8
**Critic:** Victoria Ashford, Visual Development Consultant
**Specialty:** Overall visual coherence, storytelling through visuals, cinematic composition
**Date:** 2026-03-29
**Subject:** Style Frame 01 Rendered Composite — *Luma & the Glitchkin*

---

## OPENING STATEMENT

In Cycle 7 I issued a B and identified five specific, named, fixable problems. I stated what a B+ required: demonstrate that the lighting overlay produces a visible effect, fix the tendril Bezier direction, address the couch scale, and add Byte's screen-glow. Four of the five were structural problems; one was a potency question.

I have now read every relevant line of the Cycle 8 `style_frame_01_rendered.py`. I am grading what I found.

The short version: four of five issues are genuinely fixed. One is not fixed at all and has now persisted across three consecutive cycles without being touched. That is no longer an oversight — that is a choice, and it is the wrong choice. The fixes that were made are real and some are well-executed. But the unaddressed item is the single most disorienting spatial relationship in the frame, and it continues to undermine the domestic warmth the left side of this composition is supposed to carry.

---

## VERIFICATION OF THE FIVE CYCLE 7 ISSUES

---

### ISSUE 1: Lighting Overlay Alpha — Raised to 60-80? Does it now create perceptible warm/cold split?

**VERDICT: FIXED. Meaningfully.**

The warm overlay now uses `alpha = int(70 * (1 - t))` (raised from 28). The cold overlay uses `alpha = int(60 * (1 - t))` (raised from 22). The loop draws ellipses from largest (step=14, t=1.0, alpha=0) down to smallest (step=1, t≈0.071, alpha≈65 warm / ≈56 cold). Since each smaller ellipse overwrites the previous within the same RGBA layer, the final pixel alpha at the center of the warm pool is approximately 65/255 — roughly 25% opacity. The cold center reaches approximately 56/255 — roughly 22%.

These are not the 60-80 peak values I specified, but they are perceptible. The comment in the code confirms the team understood why: "Old alpha of 28 (~11%) was functionally invisible. 70 (~27%) is perceptible." The logic is correct; the compositing uses `Image.alpha_composite` which properly layers the RGBA on top of the RGB base without flattening it.

One structural note: the warm overlay is cropped and composited onto the left half only (`W // 2`), and the cold overlay covers the right half plus an 80px spill leftward (`W // 2 - 80`). This is correct and deliberate. The 80px spill creates a narrow mixing zone at the center — the right place for it.

Credit given. The perceptibility question is answered in the code's own comments. The warm/cold split now has structural support at the atmospheric layer.

---

### ISSUE 2: Charged Gap — Is there a luminous event at the midpoint between Byte's tendril and Luma's hand?

**VERDICT: FIXED. Well-executed.**

Lines 976-994 implement the charged gap explicitly and with evident care:

```python
gap_cx = (tendril_pts[-1][0] + luma_hand_x) // 2
gap_cy = (tendril_pts[-1][1] + luma_hand_y) // 2
draw_filled_glow(draw, gap_cx, gap_cy, rx=55, ry=38,
                 glow_rgb=(180, 255, 255), bg_rgb=(40, 30, 50), steps=10)
```

The center is computed as the exact midpoint between the tendril tip and Luma's hand — the emotional center of the frame. The glow is a 55×38 filled gradient from near-white cyan at center to a dark void-adjacent tone at edge. An 18-pixel scatter of ELEC_CYAN, STATIC_WHITE, and pale cyan rectangles (seeded at 77 for reproducibility) bridges the two figures.

The glow center color `(180, 255, 255)` is not a named palette color — it is a construction value, which I accept given the rationale. The background blend color `(40, 30, 50)` is a desaturated shadow plum adjacent — appropriate for the void-pocket environment.

This is the most important fix in Cycle 8. The emotional argument of the frame now has a visual anchor. The gap between the two outstretched hands is no longer empty — it resonates. Credit is given without reservation.

---

### ISSUE 3: Tendril Direction — Does CP1 now arc toward Luma, not away?

**VERDICT: FIXED. Correctly.**

Lines 955-964 show the explicit fix with explanatory comment:

```python
# Cycle 8 fix (Victoria Ashford): cp1x was arm_start_x - byte_rx*0.8 (leftward, away from Luma).
# Fixed: cp1 is placed between Byte and Luma so the tendril arcs TOWARD her from the start.
cp1x = arm_start_x + int((target_x - arm_start_x) * 0.33)
cp1y = arm_start_y - int(byte_ry * 0.5)
```

The control point is now placed one-third of the way from Byte toward Luma, with a modest upward arc. The quadratic Bezier formula that follows uses this corrected `cp1x` as its single control point. The tendril will now curve toward Luma from the moment it leaves Byte's body, with a slight upward arc that conveys reaching. `cp2x` is no longer computed and discarded — the unused variable that was a code smell in Cycle 7 has been eliminated.

The fix is geometrically correct and expressively appropriate. The tendril now communicates eagerness. Credit given.

---

### ISSUE 4: Byte Screen-Glow — Is there upward cyan illumination on Byte's underbody?

**VERDICT: FIXED. With genuine craft.**

Lines 889-900 implement the screen-sourced upward fill explicitly:

```python
# ── Screen-sourced upward cyan fill on Byte's underbody (Victoria Ashford Cycle 8) ──
# Byte emerges from a glowing CRT screen. The screen below illuminates the underbody
# with an upward-cast cyan glow. Without this Byte reads as composited-in.
underbody_cx = byte_cx
underbody_cy = byte_cy + int(byte_ry * 0.55)  # bottom quarter of body
screen_glow_rx = int(byte_rx * 0.80)
screen_glow_ry = int(byte_ry * 0.30)
draw_filled_glow(draw, underbody_cx, underbody_cy,
                 screen_glow_rx, screen_glow_ry,
                 glow_rgb=ELEC_CYAN, bg_rgb=BYTE_TEAL, steps=8)
```

The glow is placed at the bottom 55% of Byte's vertical radius — correct for an upward-cast source from below. It is wide (80% of `byte_rx`) to simulate a broad screen emission rather than a point source. ELEC_CYAN at center blending to BYTE_TEAL at edge is appropriate — the screen illuminates the underside without turning the whole body into a flat cyan shape.

This fix integrates Byte into the scene. Byte is no longer a floating shape composited onto a background — it is a creature inside a field of light it is partially generating. This was the new requirement I introduced in Cycle 7, and it has been met.

---

### ISSUE 5: Couch Scale — Still 768px? (Raised in Cycle 6, carried to Cycle 7, unaddressed in both)

**VERDICT: NOT FIXED. Third consecutive cycle.**

```python
couch_right = int(W * 0.44)   # = 845px
# couch_left  = int(W * 0.04) # = 77px
# span = 845 - 77 = 768px = 40% of frame width
```

These values are identical to Cycle 6 and Cycle 7. The couch still spans 768 pixels — 40% of the 1920px frame. Luma's torso half-width is 44px, making her body approximately 88px wide. The couch she is sitting on is 8.7 times wider than the character sitting on it.

I identified this problem in Cycle 6. I re-identified it in Cycle 7 as "NEW FAILURE 4" with a dedicated "Priority 5" instruction. The Cycle 8 Statement of Work does not mention the couch at all. It was not addressed, not acknowledged, not deferred with explanation. It was simply ignored for the third cycle running.

I will state plainly what this omission costs: the domestic warmth of the warm left zone depends on the couch reading as a familiar, human-scale piece of furniture. A sofa that occupies 40% of the frame width does not read as a lived-in object — it reads as a painted flat, a stage element, something a character is placed in front of rather than settled into. The safety and groundedness that the warm zone is supposed to provide are compromised by this scale error. And because Luma is on the couch, the character herself reads as doll-sized relative to her own environment.

This is no longer a note. This is a structural failure that is receiving willful non-attention.

---

## SUMMARY OF CYCLE 7 ISSUE VERIFICATION

| Issue | Status |
|-------|--------|
| 1. Lighting overlay alpha raised to 60-80 — perceptible warm/cold split | FIXED (peak alpha ~65 warm, ~56 cold; compositing correct; perceptible) |
| 2. Charged gap — luminous event at emotional midpoint | FIXED (well-executed; glow + 18px scatter; best new addition this cycle) |
| 3. Tendril direction — CP1 arcs toward Luma, not away | FIXED (correctly; cp2x code smell also resolved) |
| 4. Byte screen-glow — upward ELEC_CYAN on underbody | FIXED (well-placed; integrates Byte into scene light) |
| 5. Couch scale — 768px spanning 40% of frame | **NOT FIXED** — third cycle without action |

Four of five fixed. One ignored for the third time.

---

## NEW WEAKNESSES NOW VISIBLE

The structural repairs continue to clarify the frame. What remains is not construction failure — it is compositional and technical failure that the earlier noise was partially obscuring. These are the new-highest-priority problems.

---

### NEW FAILURE 1: The Lighting Overlay Fires After the Characters Are Drawn — But the Characters Ignore It

This is a pipeline sequencing problem with significant visual consequences. The `draw_lighting_overlay()` function is called at STEP 6 in `generate()` — after the background (STEP 1), couch (STEP 2), Luma's body (STEP 3), Luma's head (STEP 4), and Byte (STEP 5). The overlay composites warm and cold fills onto the final image at the atmospheric layer.

This is correct for the background and couch, which are drawn in STEP 1-2 and get the warm/cold wash applied over them. But Luma and Byte are drawn in STEP 3-5 with their own lighting baked into their fills. The `draw_luma_body()` function interpolates per-pixel between `HOODIE_ORANGE` (warm) and `HOODIE_CYAN_LIT` (cool) — this is the correct approach for character-level lighting. But the character's warm-side color is derived from palette constants, not from the actual rendered warm zone light level.

After STEP 6, the overlay applies a warm pool over the left half of the frame, including over Luma's body. This means the warm gold layer is composited on top of Luma's already-warm hoodie. At 25% opacity this may not be severe, but it pushes the warm side of the hoodie toward yellow-gold rather than the orange-red it should be. More importantly: Luma's cold right arm, which is drawn in `HOODIE_CYAN_LIT`, then has the cold overlay composited over it in STEP 6. This adds extra cyan wash on top of the already-cyan-lit arm — which could push it toward a blue-white that reads as overexposed rather than lit.

The interaction between the atmospheric overlay and the pre-drawn character lighting has not been verified or calibrated. The character colors were set for the scene's intended lighting; the overlay may be overcooking both sides.

---

### NEW FAILURE 2: The Draw Order Leaves the Charged Gap Compositing Ambiguous

The charged gap glow (lines 976-994) is drawn inside `draw_byte()`. This means it is drawn at STEP 5, before the three-light overlay at STEP 6. The atmospheric cold overlay is then composited on top of the charged gap glow. This means the gap's `glow_rgb=(180, 255, 255)` is modified by a cyan overlay — which in practice pushes the gap even more cyan, potentially bluing out the pale near-white of the charged moment.

More critically: the gap glow is drawn on the RGB image (via `draw.draw_filled_glow`) before the RGBA atmospheric overlay is applied, which means the glow participates in the cold overlay compositing. The gap should be the brightest thing in its zone — a moment of impossible luminosity. If the cold overlay mutes its center toward cyan-blue rather than letting it breathe as near-white, the charged gap will read as just another cyan element rather than as light.

The fix is present and well-conceived. Whether the rendering pipeline sequence preserves its intended visual weight is not verifiable from code alone — but the sequence raises a flag.

---

### NEW FAILURE 3: Luma's Arm Span Is Still Anatomically Wrong, and the Comment in the Code Is False

The Cycle 8 Statement of Work says "body at 29% means arm span is ~21% of canvas." The comment in `generate()` at line 1157 repeats this: "Arm target: toward the screen edge — body at 29% means arm span is ~21% of canvas."

This claim is false, and was already false in Cycle 7 — I calculated the actual span as 28% in my previous critique. In Cycle 8 the geometry has not changed. `luma_cx = int(W * 0.29) = 557px`. `arm_x_start ≈ 623px`. `arm_x_target = scr_x0 - 20 ≈ 1158px`. Span: 1158 - 623 = 535px / 1920 = **27.9% of canvas width**.

The team has commented false math into the code and carried it from Cycle 7 to Cycle 8 without correction. The actual arm span at 28% is meaningfully better than the 40% span from Cycle 6, and the elbow break makes it readable. But a comment that says "~21%" when the geometry produces 28% is not a minor rounding error — it is documentation that contradicts reality. If this code is shared with collaborators, they will trust the comment and not check the math. That is a production liability.

---

### NEW FAILURE 4: The Submerge Effect Competes Directly With the Screen-Glow Fix

Lines 996-1014 implement a "submerge" effect: Byte's lower body fades to `VOID_POCKET = (14, 14, 30)` (a near-black) by row-by-row horizontal line overpainting. This is drawn immediately after the screen-glow fix at lines 889-900.

The screen-glow fix places a bright cyan fill (`glow_rgb=ELEC_CYAN`) at the underbody center (`byte_cy + int(byte_ry * 0.55)`). The submerge effect starts at `submerge_y = byte_cy + int(byte_ry * 0.50)` — only 5% of `byte_ry` below the screen-glow center. These two effects are painting on top of each other in nearly the same vertical range. The screen-glow draws a bright upward fill at y ≈ 55% of byte_ry below center. The submerge immediately overwrites rows starting at 50% of byte_ry with near-black.

The net result is likely that the submerge darkens or eliminates the upward glow before it reaches the viewer. The screen-glow may be visible only in the narrow band between 50% and 55% of byte_ry — a few pixels at most — before being painted over by the submerge rows. The fix I required in Cycle 7 exists in the code; it may not exist in the rendered output.

The team added a new feature (submerge effect) that directly undermines the fix I required. This is not malice — the submerge itself is a good idea conceptually — but the vertical overlap has not been managed.

---

### NEW FAILURE 5: There Is No Warm-Side Character for the Lamp to Actually Light

This is the compositional problem that none of the technical fixes can resolve, because it is a scene construction problem. The lamp is at `x = int(W * 0.40) = 768px`. The warm pool is centered at approximately `(800px, lamp_y + H * 0.35)` — roughly the floor below the lamp. Luma is at `x = 557px`, more than 200px to the left of the lamp center.

The warm overlay's ellipse reaches outward from the lamp center with `rx = W * 0.30 = 576px` at its largest step. At `x = 557px`, Luma sits 800 - 557 = 243px to the left of the lamp center. Given the glow radius of 576px, Luma is at `t ≈ 243/576 = 0.42` — roughly the middle of the warm falloff. She receives some warm light, which is appropriate.

But there is nothing in the scene between the lamp (x=768) and the monitor wall (x=960) that catches the warm light. The warm zone is being defined by the lamp, the couch, the floor, and the bookshelf (x=20% to x=48%). Luma bridges warm and cold by sitting at 29%. But the space at 40-50% — the transitional zone, the doorway between safety and the impossible — is empty of visual interest. There is no object in that zone that catches both lights. The split is clean but not dramatic. A good warm/cold composition puts something in the middle zone — a rim-lit object, a character edge, an element that catches both temperatures simultaneously and makes the divide feel charged rather than simply divided.

This is a scene dressing problem, not a code problem. But it is now the most visible compositional gap remaining.

---

## THE LARGER ASSESSMENT

Let me say what this frame is and what it still is not.

What it is: a frame with genuine structural integrity, a well-executed emotional center, and four of five requested fixes properly implemented. The charged gap glow is the best single addition this cycle — it is the right idea in the right place, well-executed. The screen-glow conceptually integrates Byte. The tendril now reaches. The lighting split is perceptible. These are real advances.

What it still is not: a frame that could survive a pitch room without comment. The couch scale problem has been ignored for three cycles and has now become the single most damaging unresolved item in the entire frame. The draw order pipeline creates an unverified interaction between the atmospheric overlay and the character-level lighting. The submerge effect may be undercutting the screen-glow that was specifically required. And a false comment in the code claims 21% arm span when the geometry produces 28%.

The distance between this frame and pitch-readiness is now very short on most axes — and impassable on one (the couch).

---

## GRADE: B+

**Justification:**

Four of five Cycle 7 issues are genuinely and well fixed. The charged gap glow earns a full point on its own — that is exactly the right solution. The screen-glow is well-conceived. The tendril correction is clean. The lighting overlay perceptibility question is answered affirmatively in the code. These are real improvements that push the frame above a flat B.

The B+ is not an A- because: the couch scale has been ignored for three consecutive cycles despite explicit priority-5 designation; the submerge effect may be erasing the screen-glow at render; and the draw-order pipeline interaction between atmospheric overlay and character fills has not been calibrated. A frame with a character who appears doll-sized relative to her own sofa is not ready for a pitch room, regardless of how well everything else is executing.

An A- requires: fixing the couch (now Priority 0, not 5); verifying the screen-glow survives the submerge by adjusting the vertical ranges so they do not overlap; and running the rendered output and confirming that the charged gap's near-white center survives the cold overlay compositing without washing blue. The technical craft is there. The three unresolved items are all fixable in a single cycle. Whether the team will finally address the couch is the only open question of character.

---

## WHAT SPECIFICALLY NEEDS TO HAPPEN IN CYCLE 9

**Priority 0 — Fix the couch scale. This has been deferred twice. It will not be deferred again.**
`couch_left = int(W * 0.04)` and `couch_right = int(W * 0.44)` produces 768px / 40% of frame width for a character who is 88px wide. Either: (a) reduce the couch to span from approximately `int(W * 0.16)` to `int(W * 0.38)` — roughly 420px — which is still wide but places Luma visually inside the furniture rather than beside it; or (b) scale the character wider so the ratio is legible. A ratio of 4:1 (couch:character) reads as a normal couch. 8.7:1 reads as a stage flat.

**Priority 1 — Resolve the screen-glow / submerge vertical overlap.**
`screen_glow_ry = int(byte_ry * 0.30)` centered at `byte_cy + 0.55 * byte_ry` means the glow spans roughly `0.25 * byte_ry` to `0.85 * byte_ry` below center. The submerge starts at `0.50 * byte_ry` and runs to `0.88 * byte_ry`. These ranges overlap from `0.50` to `0.85` — the majority of both effects. Either start the submerge lower (`0.70 * byte_ry`) or shrink the screen-glow to the bottom-most quarter only and place the submerge below it.

**Priority 2 — Correct the false code comment.**
Line 1157: "body at 29% means arm span is ~21% of canvas." The actual span is 28%. This is not a critical bug but it is false documentation in production code. Correct it to "arm span is ~28% of canvas" and note this is improved from ~40% in Cycle 6 but short of the 21% target.

**Priority 3 — Verify the draw-order interaction between atmospheric overlay and character fills.**
Run the script and examine the rendered output. Specifically: does the cold overlay push Luma's right arm toward washed-out cyan-blue? Does the warm overlay yellow-shift Luma's hoodie orange? If so, either reduce the overlay alpha or apply the overlay before drawing the characters (draw background → overlay → characters). Characters drawn with their own lighting should not then have atmospheric fills composited on top of them without knowing what those fills will do at their specific color values.

**Priority 4 — Add transitional-zone mid-frame interest.**
The zone between the lamp (x≈768) and the monitor wall (x=960) is visually inert. This is the crossing point — the literal boundary between Luma's world and Byte's world. A small object, a cable on the floor, a dust mote in the air, an upholstered cushion edge — anything that catches both warm and cold light simultaneously and says: here is where one world ends and another begins.

---

*Victoria Ashford*
*Visual Development Consultant — 30 years industry experience*
*Cycle 8 Review — 2026-03-29*
