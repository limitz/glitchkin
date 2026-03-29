# Critique — Cycle 7
**Critic:** Victoria Ashford, Visual Development Consultant
**Specialty:** Overall visual coherence, storytelling through visuals, cinematic composition
**Date:** 2026-03-29
**Subject:** Style Frame 01 Rendered Composite — *Luma & the Glitchkin*

---

## OPENING STATEMENT

In Cycle 6 I issued a B- and identified seven specific, named, fixable problems. I stated plainly: fix those seven things, and this frame clears the B threshold. Fix all of them and push body rendering to match face resolution, and it earns a B+. The team claimed in their Statement of Work that all seven were addressed.

I have read every line of the updated `style_frame_01_rendered.py`. I am now grading what I found.

The short version: six of seven issues are genuinely fixed. One is partially fixed with a structural problem that reveals a new and more important compositional gap. And now that the structural scaffolding is finally sound, the frame's remaining weaknesses are different in character — they are no longer construction failures, they are storytelling failures. The frame can now be seen clearly enough to criticize properly.

That is progress. But it is not a finish line.

---

## VERIFICATION OF THE SEVEN CYCLE 6 ISSUES

I am going through each one, in the exact order I listed them.

---

### ISSUE 1: draw_lighting_overlay() — Was it implemented with real glow logic?

**VERDICT: FIXED. Genuinely.**

The function at lines 882–938 is a substantive implementation. It is no longer `pass`. What was there:

- A warm gold RGBA layer using concentric filled ellipses centered below the lamp position (`lamp_glow_cx`, `lamp_glow_cy`), composited exclusively onto the left half of the frame via a crop-and-paste (`img.crop((0, 0, W // 2, H))`). The alpha ramps from 0 at center outward — correct fill glow logic.
- A cold cyan RGBA layer using the same concentric ellipse approach, centered on the monitor wall midpoint, composited onto the right half with an 80px left spill. The spill is intentional and correctly implemented.

Both layers use `Image.alpha_composite` so they add light without destroying background detail. The warm zone does not contaminate the cold zone. The cold wash does not flatten the left-side warmth.

This is the correct approach. The implementation matches the intent. Credit is given.

One note for the record: the warm glow alpha peaks at only 28 per step (line 906: `alpha = int(28 * (1 - t))`), which is quite low. At this value, the warm pool may be nearly invisible at final render. The cold layer is at 22. Both are conservative — possibly so conservative that the effect is imperceptible. I cannot verify this without seeing the rendered PNG at 1920×1080, but the logic is correct. If the effect is invisible in practice, the team should increase these values. The fix is real; its potency is unverified.

---

### ISSUE 2: DUSTY_LAVENDER full-frame overlay — Was it removed?

**VERDICT: FIXED. Completely.**

The Step 6 in Cycle 6's `generate()` was:

```python
overlay = Image.new("RGB", (W, H), DUSTY_LAVENDER)
alpha_mask = Image.new("L", (W, H), 18)
img = Image.composite(overlay, img, alpha_mask)
```

In Cycle 7's `generate()`, Step 6 (lines 1033–1049) is the call to `draw_lighting_overlay()`. The flat lavender composite is gone. There is no full-frame `DUSTY_LAVENDER` overlay anywhere in the `generate()` function. DUSTY_LAVENDER appears in the palette (line 43) and in the bookshelf book colors (line 314) and as the keyboard fill (line 339), which are all appropriate local uses. It does not appear as a global composite.

The warm/cold color temperature contrast is now structurally unobstructed. This was the most important single fix in Cycle 7. It has been made correctly.

---

### ISSUE 3: Arm span — Is it now ~21% of canvas?

**VERDICT: FIXED. The claim is accurate.**

In Cycle 6, `luma_cx = int(W * 0.19) = 365px`. In Cycle 7, line 1012: `luma_cx = int(W * 0.29) = 557px`. The comment even acknowledges the fix: *"luma_cx moved to 29% (was 19%) — reduces arm span to anatomically plausible range."*

The arm target is `arm_target_x = scr_x0 - 20`. Working through the geometry: `scr_x0 = crt_x + scr_pad = (mw_x + int(mw_w * 0.22)) + 24`. `mw_x = int(W * 0.50) = 960`. `mw_w = int(W * 0.46) = 883`. `crt_x = 960 + int(883 * 0.22) = 960 + 194 = 1154`. `scr_x0 = 1154 + 24 = 1178`. `arm_target_x = 1178 - 20 = 1158`.

The arm starts at `arm_x_start = luma_x + torso_half_w + int(lean_offset * 0.8) = 557 + 44 + 22 = 623px`. The arm ends at 1158px. Span: 1158 - 623 = 535px. At 1920px width, that is 27.9% of frame width.

That is not 21%. The comment says 21%; the geometry says 28%. This is not a catastrophic discrepancy — 28% is a meaningful improvement over the Cycle 6 value of ~39% — but the team's own stated target of 21% was not achieved. The arm is still somewhat long. More importantly: the arm now has an elbow break (lines 529–558), which is the single biggest improvement, regardless of the span percentage. An arm with an elbow joint at 28% span reads far more naturally than a straight-line arm at 40% span. The elbow break at `elbow_x = (arm_x_start + arm_x_target) // 2` with `elbow_y = arm_y_start - 20` (a mere 20px upward arc) is modest — but it exists and it is correct in principle.

Credit given with annotation: the proportional target was not precisely hit, but the directional fix is genuine and the elbow break is the more important structural improvement.

---

### ISSUE 4: Neck geometry — Does it exist?

**VERDICT: FIXED. Properly.**

Lines 503–519 implement a neck trapezoid between `neck_top_y = torso_top - 30` and `neck_bot_y = torso_top + 10`. It is filled with `SKIN`, has a shadow line on the left edge in `SKIN_SH`, and correctly tracks the lean offset (`torso_top_cx = luma_x + int(lean_offset * 1.0)`). The head position is then set to `head_cy = torso_top - 10`, which places the head above the neck top by 20px — anatomically coherent.

The neck exists. It is a trapezoid. It connects. The floating head problem is resolved.

---

### ISSUE 5: Torso seam — Is it fixed with a gradient blend?

**VERDICT: FIXED. This is the best implementation in the script.**

Lines 471–483 implement a genuine row-by-row, pixel-by-pixel horizontal gradient blend across the torso. For every row between `torso_bot` and `torso_top`, and for every column within that row's width, the code computes:

```python
r_v = int(HOODIE_ORANGE[0] * (1 - t_x) + HOODIE_CYAN_LIT[0] * t_x)
```

This is correct linear interpolation from `HOODIE_ORANGE` on the warm left edge to `HOODIE_CYAN_LIT` on the cool right edge, per pixel. The lean offset is also integrated: `row_lean = int(lean_offset * t_y)`, so the warm-to-cool transition shifts rightward as the torso rises, tracking the forward lean. The hard vertical seam is gone. The transition is smooth.

This is a more technically careful implementation than I expected from this team at this stage. It is the right solution and it was implemented correctly.

---

### ISSUE 6: Vignette — Top/bottom only?

**VERDICT: FIXED. Correctly.**

Lines 1055–1068 implement two explicit horizontal band loops:

```python
for i in range(60):
    t = 1.0 - i / 60.0
    alpha_val = int(70 * t)
    v_draw.line([(0, i), (W, i)], fill=alpha_val)
for i in range(60):
    ...
    v_draw.line([(0, H - 1 - i), (W, H - 1 - i)], fill=alpha_val)
```

This draws 60-pixel dark bands at the top and bottom of the frame only. The left and right edges are not darkened. The `v_alpha` mask is initialized to `0` (transparent), meaning nothing outside the two bands is affected.

The warm left zone and cold right zone breathe as they should. The vignette now serves the composition's emotional argument rather than working against it.

---

### ISSUE 7: Blush ring — Removed?

**VERDICT: FIXED. Elegantly.**

Lines 703–716 implement the blush as an RGBA composite on a dedicated transparent layer:

```python
blush_layer = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
blush_draw  = ImageDraw.Draw(blush_layer)
blush_alpha = 80
blush_draw.ellipse([...], fill=(*BLUSH_LEFT, blush_alpha))
```

The `blush_alpha = 80` gives approximately 31% opacity — a soft flush that is visible without being a painted circle. The skin cover ellipses that previously erased the blush center are completely gone. No hard ring. The blush sits atop the skin as a soft semi-transparent tint.

This is the correct approach and it was executed correctly.

---

## SUMMARY OF CYCLE 6 ISSUE VERIFICATION

| Issue | Status |
|-------|--------|
| 1. draw_lighting_overlay() — real glow logic | FIXED (potency unverified, logic correct) |
| 2. DUSTY_LAVENDER overlay — removed | FIXED (completely) |
| 3. Arm span ~21% of canvas | PARTIALLY FIXED (28%, elbow break added — improved but target missed) |
| 4. Neck geometry — added | FIXED |
| 5. Torso seam — gradient blend | FIXED (best implementation in script) |
| 6. Vignette — top/bottom only | FIXED |
| 7. Blush ring — removed | FIXED |

Six of seven fixed. One partially fixed (arm span improved, not at stated target).

---

## NEW WEAKNESSES NOW VISIBLE

Here is where this critique becomes important. Fixing the structural failures has not produced a finished frame — it has revealed the next layer of problems. These are compositional and storytelling failures that the earlier structural noise was masking. I am now evaluating the frame on those higher terms.

---

### NEW FAILURE 1: The Two Characters Are Not in the Same Light

The most serious remaining compositional problem: Luma and Byte are both drawn with lighting information, but they do not share the same light source coordinates. Luma's warm side is her left; Byte's warm bounce light is applied to the upper-left of Byte's body. Since Byte is on the right side of the frame (at the monitor wall), the lamp — which is in the warm zone on the left — would cast light on Byte's left face as Byte faces left toward Luma. But Byte's body is a sphere emerging from a screen that is itself a light source. A character emerging from a glowing screen should be lit primarily from below and from behind (the screen behind it). Byte's current lighting has a warm bounce highlight on the upper-left — the correct direction for the distant lamp — but the screen directly behind Byte is not contributing any upward-cast fill on Byte's underbody. Byte floats in front of a glowing rectangle and does not appear to be lit by it.

This is a storytelling problem as much as a lighting problem. The monitor wall is the most dramatically charged element in the frame. It should be visibly, undeniably illuminating the characters that are near it. Byte is emerging from it and shows no evidence of being inside its light.

---

### NEW FAILURE 2: The Emotional Midpoint of the Composition Is Unlit

The narrative heart of Frame 01 is the gap between Luma's hand and Byte's tendril — the space of almost-touching. This gap is spatially located somewhere around x=900-1000 in the frame, between Luma at 29% (557px) and the screen edge at ~1158px. That midpoint is compositionally the most important region in the frame.

What is in that region? The back of the couch, some floor, some ambient background. There is no explicit lighting event at that location. The warm pool from `draw_lighting_overlay()` is cropped at `W // 2 = 960px` and does not reach the hand. The cold wash starts at `W // 2 - 80 = 880px` and barely touches it. The result is that the space between the two outstretched hands — the one region in this frame that needs to feel charged, electric, impossible — is probably the least lit area in the entire composition.

This is a direct storytelling failure. The frame must answer the question: what is in the space between these two hands? Right now, the answer is: nothing in particular. The answer should be: light. A breath of it. Something that makes the viewer feel the impossibility of what is about to happen.

---

### NEW FAILURE 3: Byte's Tendril Target Is Geometrically Incoherent

The tendril in `draw_byte()` uses a quadratic Bezier with these control point assignments (lines 841–846):

```python
cp1x = arm_start_x - int(byte_rx * 0.8)
cp1y = arm_start_y - int(byte_ry * 0.5)
cp2x = (arm_start_x + target_x) // 2
cp2y = (arm_start_y + target_y) // 2 - 20
# Simplified: quadratic approach
px = int((1-t)**2 * arm_start_x + 2*(1-t)*t * cp1x + t**2 * target_x)
```

This is labeled "quadratic approach" but the formula uses `cp1x` as the single control point while `cp2x` is computed but never used in the actual point calculation. A quadratic Bezier uses one control point: `P = (1-t)^2 * P0 + 2*(1-t)*t * P1 + t^2 * P2`. The code has that structure, using `cp1x` as the control — but `cp1x = arm_start_x - int(byte_rx * 0.8)` is to the left of Byte's body, not between Byte and Luma. This means the tendril curves first backward (away from Luma) before arcing toward the target. A tendril reaching eagerly toward someone should curve toward them, not arc away first.

The unused `cp2x` variable is also a code smell — it was likely intended for a cubic Bezier that was simplified mid-implementation without correcting the control point direction. The tendril will render as a backwards-arcing curve, which is the opposite of the reaching, yearning gesture the scene requires.

---

### NEW FAILURE 4: The Couch-to-Character Scale Problem Persists

I raised this in Cycle 6 and it was not addressed in Cycle 7. The couch still spans from `int(W * 0.04) = 77px` to `couch_right = int(W * 0.44) = 845px` — a total of 768px, which is 40% of the frame width. Luma is now at x=557 and her torso half-width is 44px, meaning her body spans approximately 88px wide. The couch she is sitting on is 768px wide. A couch that is 8.7x the width of the character sitting on it is a spatial absurdity. This makes Luma read as a small figure on an enormous piece of furniture rather than a teenager settled into a familiar couch. The domestic warmth the couch is meant to communicate — safety, home — is undermined by a piece of furniture that reads as a stage prop rather than a lived-in sofa.

This is not a new observation. It was Failure 7 in Cycle 6. It remains unaddressed.

---

### NEW FAILURE 5: The Lighting Overlay Alpha Values Are Almost Certainly Imperceptible

I flagged this in the Issue 1 verification, and it warrants its own section. The warm gold overlay uses `alpha = int(28 * (1 - t))` for each of 14 steps. At the innermost step (step 14, `t = 14/14 = 1.0`), alpha = 0. At the outermost step (step 1, `t = 1/14 ≈ 0.07`), alpha = `int(28 * 0.93) = 26`. Each step is composited on top of the previous, but since each subsequent step has a smaller radius and lower alpha, the actual center of the warm glow accumulates transparency across steps. The net result at the center of the warm pool — where the glow should be strongest — may be near-invisible.

The same issue applies to the cold layer (max alpha 22). These are very conservative values. If the `draw_lighting_overlay()` function is doing almost nothing perceptible in the final image, then the room lighting is effectively still flat, and the warm/cold split is still being carried entirely by the background gradient and the character-level lighting. The fix was implemented correctly in logic. Whether it does anything visible at these alpha values is genuinely uncertain. This needs to be tested and the values increased if the effect is not visible.

---

## THE LARGER ASSESSMENT

Let me say directly what this frame now is and what it is not.

What it is: a technically competent procedural rendering of a scene with two characters, a split color temperature, and an emotional premise. The worst structural failures are corrected. The lavender contamination is gone. The neck exists. The torso blends. The vignette serves the composition. The lighting overlay function is real. These are genuine improvements that moved the frame from "partially correct" to "substantially correct in structure."

What it is not: a frame that would survive a pitch room. The gap between Luma's hand and Byte's tendril — the emotional center, the one thing this frame must get right above all else — is compositionally empty. The tendril curves backward. The couch dwarfs the character. The lighting overlay may be invisible. Byte is not lit by the screen it is emerging from. These are not construction failures, which the team has demonstrated it can fix. These are compositional intelligence failures — failures to ask "what is this frame saying, and does every element serve that statement?"

The frame is now built. It is not yet told.

---

## GRADE: B

**Justification:**

Six of seven Cycle 6 issues are genuinely fixed. The torso gradient and the blush composite are executed with real craft. The lighting overlay is the correct architecture even if its potency is unverified. The vignette now serves the composition. The lavender contamination is gone. These are real improvements that clear the threshold I set for a B.

The B is not a B+ because: the arm span target was missed (28%, not 21%); the couch scale problem was ignored; the tendril control point logic curves the wrong direction; and the emotional midpoint of the composition is unlit. Any one of these alone might be a polish note. Together, they leave the frame short of the standard required for pitch use.

A B+ requires: demonstrating that the lighting overlay produces a visible effect at render, fixing the tendril Bezier direction, and addressing the couch scale. A proper B+ also requires Byte to be lit from its own screen — that is a new requirement for Cycle 8 that was not possible to identify until the structural noise was cleared.

The project is pitchable in outline. It is not yet pitchable in execution. The remaining distance is now fully defined. It is a question of whether the team will push to close it.

---

## WHAT SPECIFICALLY NEEDS TO HAPPEN IN CYCLE 8

**Priority 1 — Verify and increase draw_lighting_overlay alpha values.**
Run the script and evaluate the rendered output. If the warm gold pool and cold cyan wash are not visually distinct from the background without the overlay, the alpha values must be raised. Suggested starting point: warm peak alpha 55–65; cold peak alpha 40–50. The overlay must be perceptible.

**Priority 2 — Light the midpoint between the two hands.**
Add an explicit lighting event in the space between Luma's hand and Byte's tendril tip. This could be a small filled glow in pale electric cyan or a warm amber scatter — something that says "this space is charged." The emotional argument of the frame lives here. It should not be empty.

**Priority 3 — Fix the tendril Bezier control point direction.**
The control point `cp1x = arm_start_x - int(byte_rx * 0.8)` arcs the tendril backward (left of Byte's body) before curving toward Luma. Reverse the horizontal direction of `cp1x` so the tendril curves toward Luma from the start. The tendril should express eagerness, not hesitation.

**Priority 4 — Light Byte from its own screen.**
Byte is half-submerged in a glowing monitor. The underside of Byte's body should show a screen-colored upward-cast glow — a cyan fill, slightly brighter than the body fill, on the bottom quarter of Byte's body. This is a single `draw_filled_glow()` call aimed upward from below the screen plane. It will make Byte feel integrated into the scene rather than composited onto it.

**Priority 5 — Address the couch scale.**
The couch should not span 40% of the frame width when the character is 88px wide. Either reduce the couch width to roughly 200–250px total span, or scale Luma's torso width proportionally wider to match the furniture. The current ratio makes the character appear to be the size of a doll.

---

*Victoria Ashford*
*Visual Development Consultant — 30 years industry experience*
*Cycle 7 Review — 2026-03-29*
