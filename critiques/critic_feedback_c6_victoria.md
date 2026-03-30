# Critique — Cycle 6
**Critic:** Victoria Ashford, Visual Development Consultant
**Specialty:** Overall visual coherence, storytelling through visuals, cinematic composition
**Date:** 2026-03-29
**Subject:** Style Frame 01 Rendered Composite — *Luma & the Glitchkin*

---

## OPENING STATEMENT

In Cycle 5 I said, plainly: "It does not yet exist" — referring to the one fully rendered style frame that would make this project pitchable. In Cycle 6, Alex Chen produced `style_frame_01_rendered.py` and its output. So the question I am answering in this critique is not whether the team tried. They tried. The question is whether what they produced clears the bar.

The answer is: partially. And "partially" at this stage of the project is not good enough — but it is genuinely, meaningfully better than before, and I will not pretend otherwise. What matters now is precision about exactly where the gap remains, because the gap has narrowed enough that the remaining problems are specific and fixable.

Let me be exact.

---

## WHAT IMPROVED FROM CYCLE 5

These improvements are real and I am crediting them without qualification.

### 1. The Frame Is Now Compositionally Staged

The most critical structural improvement in Cycle 6 is that Frame 01 is no longer a layout diagram. The code composes actual elements in actual space. Luma has a body with legs, a torso split-lit across warm and cool zones, a reaching arm, a resting arm, shoes, a hoodie with pixel accents, a collar, and a face with asymmetric brows. Byte has a teal body fill, an elliptical amber outline, two asymmetric eyes (one pixel '!' and one wide scared circle), a scar detail, and a tapering tendril. The couch has seat geometry, back cushions, an armrest, and a warm rim light. The room has a ceiling plane, a back wall with atmospheric gradient, wainscoting, a floor with plank grain, a window with curtains, bookshelves with colored book spines, a desk with keyboard, a mug, and individual cables. The monitor wall has six secondary screens plus a dominant CRT with an emergence void.

In Cycle 5, none of this existed in the actual image. In Cycle 6, all of it exists. That is not a small thing. That is the difference between a diagram and a scene.

### 2. The Three-Light Setup Is Coded Into the Characters

The split-lit technique on both characters is specifically implemented, not just described. Luma's torso is split between `HOODIE_ORANGE` (warm lamp left half) and `HOODIE_CYAN_LIT` (cyan-lit right half). Her face has explicit warm arc highlights on the left, cyan arc highlights on the right, and lavender ambient arc on the chin underside. Her reaching arm is coded in `CYAN_SKIN` to indicate it has crossed into the cold light zone. Byte's body has a warm bounce light `draw_filled_glow` on the upper-left and a cool ambient shadow on the lower portion. The `DUSTY_LAVENDER` is applied as a global low-opacity composite overlay in Step 6.

This is real three-point lighting logic being applied to 2D character geometry. It was not present before. The intent is correct and the code executes it.

### 3. The Corrupted Amber Outline Is Correctly Elliptical

The `draw_amber_outline()` function now draws stacked `draw.ellipse()` calls. This is the correct fix. The previous rectangular amber outline was a composition-killer — it imposed a bounding-box geometry on a character whose body is circular, creating a visual tension between the shape of the character and the shape of its outline. The elliptical version respects the form. It is the right call and it was made correctly.

### 4. Byte's Figure-Ground Separation Is Addressed

`BYTE_TEAL` (#00D4E8) as body fill versus `ELEC_CYAN` (#00F0FF) as screen fill creates a readable color value step between Byte and the screen he is emerging from. The emergence void — a dark ellipse at the center of the CRT screen — provides additional figure-ground contrast. Byte pops off the screen. This problem was identified in prior cycles; it is resolved.

### 5. The Monitor Wall Has Functional Depth

Six secondary screens with individual glows, an individual dominant CRT with a pedestal and beveled casing, pixel confetti escaping the emergence zone, a floor glow trapezoid in cold cyan, and a left-wall spill glow that bleeds the cold light into the warm zone boundary. The monitor wall is no longer a flat bank of rectangles. It has layers. The glow spill logic is correct. The warm-world / cold-world boundary is visually established.

### 6. The Couch Faces the Monitor Wall

The couch trapezoid geometry is correctly oriented — seat angled so the occupant faces right, toward the monitor wall. This was a specific criticism in earlier cycles. It is fixed.

### 7. Bookshelves and Room Furnishings Exist

Window with curtains, bookshelves with randomized colored book spines and shelf dividers, desk with keyboard detail and individual keys, a mug with handle arc, individual named cables of distinct colors. The room has personality now. It is no longer a terracotta box. The Cycle 5 criticism about the room lacking character has been meaningfully addressed.

---

## WHAT STILL FAILS AND WHY

These are not minor polish notes. These are structural problems that keep this frame from clearing the pitch standard.

### FAILURE 1: The Lavender Ambient Overlay Is Compositionally Destructive

This is the single largest unresolved problem in the entire composite, and it is introduced at Step 6 of the main generate function.

```python
overlay = Image.new("RGB", (W, H), DUSTY_LAVENDER)
alpha_mask = Image.new("L", (W, H), 18)
img = Image.composite(overlay, img, alpha_mask)
```

A flat `DUSTY_LAVENDER` (168, 155, 191) full-frame overlay at alpha 18 is applied uniformly across the entire image. This means the warm amber glow on the left — the emotional core of the "safety, home, the known world" zone — is being tinted lavender. The warm gold of the lamp, the sunlit amber of the back wall, the terracotta of the floor and couch: all of it is being pulled toward a cool lavender cast. The warm zone and the cold zone are now more similar to each other than they should be.

The correct use of lavender ambient fill in a three-light setup is selective. Lavender ambient should fill shadow areas that receive neither the key light nor the fill light — the turned-away surfaces, the underside of forms, the areas receiving nothing but sky. Applying it as a flat global overlay defeats the entire purpose of having two opposed color temperatures as the emotional argument of the composition. If everything has a lavender cast, the warm-versus-cold split reads at reduced contrast. The emotional premise — home on the left, the impossible on the right — is weakened.

This is not a code complexity problem. The fix is to remove the flat overlay and add lavender only to shadow regions (the underside geometry passes in the character draw functions). The ambient note is already present on faces and bodies via the arc calls. The full-frame overlay is undermining those local calls.

### FAILURE 2: Luma's Body Is Constructed from Parallelograms, Not a Cartoon Character

The torso is two trapezoids — one orange-filled, one desaturated-fill — split by a vertical seam at the character's horizontal center. The arms are `draw.line()` calls of width 18 and 20. The legs are parallelograms. The head connection is implied by placement, not constructed.

I want to be precise about what the problem is, because the intent is visible and the structure is correct — the issue is execution resolution.

The "warm lamp side" / "cyan screen side" torso split is a clever and correct approach, but the seam at `luma_x + 2` / `luma_x + 4` creates a visible hard boundary down the center of the torso. In real or painted lighting, this transition is a gradient — it does not have a line. The two-polygon torso approach creates a lit-character effect that works in silhouette but, when viewed at 1920x1080, shows the construction too obviously. A cartoon character's split-lighting should be organic, not geometric.

More critically: there is no neck. The head is drawn at coordinates `torso_top - 10` above the torso, but no neck geometry connects the two. At scale, this head will appear to float above the body. The collar ellipse at `cy + head_r + 10` addresses this partially, but the collar is drawn as part of the face function — meaning it is composited on top of whatever background is at that location, not connected to the torso geometry.

The reaching arm is a 20-pixel-wide `draw.line()`. A pixel-thick line at 20px width at 1920x1080 is visible as a painted stroke, not as a cartoon arm. There is no elbow inflection. The arm has two segments and a hand ellipse, but it reads as a thick colored line rather than a limb with volume. The warm rim light is a 3px line over the top of the arm, which at this scale is nearly invisible.

The Cycle 5 face closeup proved this team can render a cartoon character with genuine appeal at fine resolution. The body in this composite is not being rendered at that standard. The face is drawn at a detail level appropriate to a character close-up. The body is drawn at a detail level appropriate to a pose breakdown thumbnail. These two things do not cohere when placed in the same frame.

### FAILURE 3: The Byte-to-Luma Spatial Relationship Is Not Verified

The tendril from Byte reaches toward `luma_hand_x = arm_target_x - 4`, `luma_hand_y = arm_target_y - 26`. The arm target is defined as `arm_target_x = scr_x0 - 20` and `arm_target_y = emerge_cy + int(emerge_ry * 0.10)`.

Now: `scr_x0 = crt_x + scr_pad`. `crt_x = mw_x + int(mw_w * 0.22)`. `mw_x = int(W * 0.50)`. So `crt_x` is approximately 50% + 22% of 46% = ~60% of frame width. `scr_pad = 24`. Therefore `scr_x0 ≈ (960 + 0.22 * 883) + 24 ≈ 960 + 194 + 24 = 1178px`.

Luma's center is at `luma_cx = int(W * 0.19) = 365px`. The body torso top is `luma_base_y - 260 = int(H * 0.90) - 260 = 972 - 260 = 712`. The arm starts at `torso_top + 80 = 792`, `arm_x_start = luma_x + 42 = 407`. The arm extends to `arm_x_end = 1158`.

That is an arm reaching from x=407 to x=1158: 751 pixels. At 1920px width, that arm spans nearly 40% of the frame. The arm is drawn at 20px width. A single human arm spanning 40% of a 1920-wide frame and anchored to a character whose torso is maybe 90px wide is anatomically impossible. The arm is structurally too long relative to the body it belongs to. This is a proportion problem that will visually read as: character's arm is as long as the room.

The reaching arm is the visual center of the composition — per the stated emotional intent, "two hands almost touching" is the narrative heart of Frame 01. A stretched, line-thick limb spanning 40% of the frame is not the "two hands almost touching" that this frame needs to sell. It is a line pointing at a screen.

### FAILURE 4: The Vignette Logic Is Inverted in Emotional Terms

Step 7 applies a vignette using a `lambda x: 80 - x` inversion over a gradient that is brightest at the image boundary. This means the corners are being darkened. Standard vignette logic, correctly implemented.

However: the right edge of the frame is the monitor wall — it is already extremely dark (void black background with cyan screen fill). Darkening the right corner further pushes the monitor wall into near-invisibility at the frame edge. The left edge, which is the warm zone (amber wall, window with soft gold fill), is also being darkened. The warm zone's left edge registers as: warm, then vignetted dark. This creates a dark border around the entire frame that impartially darkens both the emotionally warm elements and the emotionally cold elements.

A cinematically correct vignette for this composition would darken the top and bottom edges while allowing the two lateral zones to breathe. The horizontal center of the frame — where Luma's reaching arm and Byte's tendril almost meet — should be the lightest region. The current vignette does not serve the composition's emotional argument. It just darkens corners.

### FAILURE 5: The draw_lighting_overlay Function Does Nothing

```python
def draw_lighting_overlay(draw, W, H, luma_cx, luma_cy,
                          monitor_cx, monitor_cy, lamp_x, lamp_y):
    """
    Apply three-light atmospheric overlay over the full frame...
    """
    pass
```

This function is defined, documented in its docstring as critical, and then contains `pass`. It is never called in the `generate()` function. The three-light atmospheric overlay described in the docstring — "large, low-opacity filled ellipses" representing the monitor's cyan fill, the lamp's warm gold fill, and the lavender ambient — does not exist in the final composite. The lighting logic is applied per-character through individual draw calls, but the environmental lighting (the ambient light filling the room) is absent except for the destructive flat overlay at Step 6.

This is not a minor gap. A room in which the lamp casts a warm glow should show that warm glow on the floor, on the wall, on the objects near the lamp. The monitor wall should flood the right-hand portion of the frame with a cool blue-cyan wash that the character is sitting in. None of these ambient fills are present in the environment. The characters carry lighting information but the room does not respond to the same lights.

### FAILURE 6: The Blush Is Painted Over Immediately

```python
draw.ellipse([cx - head_r + p(8), cy + p(5), cx - head_r + p(58), cy + p(38)],
             fill=(220, 80, 50))
draw.ellipse([cx + head_r - p(58), cy + p(5), cx + head_r - p(8), cy + p(38)],
             fill=(208, 72, 48))
# Redraw skin over blush centers to soften
draw.ellipse([cx - head_r + p(18), cy + p(10), cx - head_r + p(48), cy + p(32)],
             fill=SKIN)
draw.ellipse([cx + head_r - p(48), cy + p(10), cx + head_r - p(18), cy + p(32)],
             fill=SKIN)
```

The blush ellipses are drawn, and then immediately covered almost entirely by solid-fill skin ellipses of nearly the same size. The "softening" effect of the skin redraw is actually erasure. The blush will render as a thin ring of `(220, 80, 50)` around a solid skin ellipse — a visible hard ring that is not how blush reads on a cartoon character. Blush on a cartoon character is typically a soft, feathered, low-opacity circle that sits on top of the skin and never has a hard inner boundary. This implementation will produce the opposite: a hard-edged ring that looks like a circle drawn around the cheek rather than a flush drawn into the cheek.

This is a minor cosmetic issue relative to the structural problems above, but on a character whose face is the emotional instrument of the composition, it matters. The face is where the viewer's eye will rest longest.

### FAILURE 7: The Couch Positioning Creates a Spatial Paradox

`luma_cx = int(W * 0.19) = 365px`. The couch's right edge is `couch_right = int(W * 0.44) = 845px`. The couch spans from `int(W * 0.04) = 77px` to 845px. Luma is centered at 365px. Luma's reaching arm extends to ~1158px. The couch arm rest is at the right edge of the couch (845px), but Luma's reaching arm starts at `luma_x + 42 = 407px` and the arm is drawn on top of the couch geometry.

The right side of Luma's body (cyan-lit torso half) is at `luma_x + 46 = 411px`. The couch right edge is 845px. This means 434px of couch extends beyond Luma's rightmost body point. The couch is significantly wider than the character sitting on it, and the rightmost portion of the couch is drawn in front of (over) the monitor wall and desk area (which starts at `mw_x = 960px`). Since the couch draw call happens after the background and before the characters, the couch correctly sits under the character — but at 1920x1080, a couch whose seat spans nearly 800px will appear implausibly large. At this scale, the couch is roughly the length of a full-size car.

---

## WHAT SPECIFICALLY NEEDS TO HAPPEN IN CYCLE 7

These are prioritized in order of visual impact on the pitch frame.

**Priority 1 — Remove the flat lavender overlay. Replace with selective shadow-area lavender.**
This single change will immediately restore the warm-versus-cold contrast that is the emotional spine of this composition. The lavender ambient should only be present in shadow zones — implement this by drawing lavender tints only on the turned-away surfaces and deep shadow polygons, not as a global composite. The individual face and arm arc calls are already doing the right thing. The flat overlay is undoing them.

**Priority 2 — Implement draw_lighting_overlay as a functional room fill.**
The lamp should cast a warm gold filled gradient across the left zone of the floor and wall. The monitor wall should flood the right zone of the room with a wide, low-opacity cyan fill that reaches the floor and mid-wall. These room-level fills should be drawn before the characters so the characters sit in light that the room also occupies. Currently the room and characters behave as if lit by different lights.

**Priority 3 — Reduce the reaching arm span by repositioning Luma closer to the screen, or shorten the arm's target.**
The arm spanning 40% of the frame is the most anatomically jarring element of the composition. Either move `luma_cx` rightward (from 19% to 28-30% of frame width) to shorten the total arm span, or redesign the reach as a two-segment bent elbow — upper arm angled forward, forearm extending, hand reaching into the screen's near edge. An elbow break at roughly the halfway point would give the arm believable volume without requiring it to span the room.

**Priority 4 — Give Luma's torso a gradient-blend seam rather than a polygon split.**
Replace the two-trapezoid warm/cool torso with a single shape that uses either a horizontal row-by-row color blend (similar to the wall gradient approach already used in `draw_background`) or a single-polygon draw with a warm-orange outer edge and a gradual shift to the cool-lit color. The hard vertical seam at the center of the torso reads as construction rather than lighting.

**Priority 5 — Add a neck connection between Luma's head and torso.**
A simple trapezoid or rectangle in skin tone connecting the collar's upper edge to the head's lower edge. This is a single polygon. Without it, the head floats above the body at certain viewing distances.

**Priority 6 — Fix the vignette to darken top and bottom only, not the lateral warm and cold zones.**
Revise the vignette gradient to apply darkness from top and bottom edges inward, using horizontal rather than rectangular marching. The left (warm) and right (cold) edges of the frame should be left substantially brighter to let both emotional zones breathe.

**Priority 7 — Fix the blush rendering.**
Either remove the skin cover ellipses entirely and let the blush remain as a soft circle, or reduce their size significantly so the remaining blush ring is wider and more diffuse. Alternatively, swap to a dot-stipple pattern of skin-shadow color applied over the blush area, which reads as painted blush more convincingly.

---

## THE LARGER ASSESSMENT

What Alex Chen delivered in Cycle 6 represents the largest single cycle-over-cycle improvement in this project's output history. Frame 01 now contains a scene. A room. Two characters. Light. A narrative moment. That is a genuine, honest accomplishment, and I am not softening that statement.

But the distance between "a scene is present in the image" and "this frame is ready to sell a show" is still real, and the specific problems I have identified above are what account for it.

The emotional argument of this frame — a girl on a warm couch in a safe home, reaching toward an impossible creature in a cold digital light, two hands almost touching — is correct, present in the code, and generating a recognizable image. The image is not yet doing the emotional work that the visual argument demands. The lavender overlay is undermining the color temperature contrast. The lighting overlay function is a stub. The arm proportions break spatial believability. The couch is too large. The blush is a hard ring. These are solvable problems, not systemic failures.

Cycle 7 does not need to rebuild this frame from scratch. It needs to fix the specific issues named above. If those fixes land, this frame will clear the pitch standard I have been holding for four cycles.

The documentation-to-image gap that defined every critique from Cycles 1 through 5 has materially closed. What remains is craft. And craft is the territory where this team has demonstrated it can operate.

---

## GRADE: B-

**Justification:**

The team fulfilled the core mandate I set in Cycle 5: produce a rendered composite where both characters are recognizable, the three-light setup is implemented, and the emotional premise of the scene is readable without text. Frame 01 does all three of those things, which marks genuine passage over the threshold from diagram to image.

The B- rather than B or higher reflects the specific failures itemized above — in particular, the flat lavender overlay that undermines the composition's foundational color argument, the non-functional lighting overlay, the arm proportion problem, and the torso seam. These are not polish notes. They are problems with the craft execution of ideas that are otherwise correctly conceived.

A grade of B requires that the composition's strongest single idea — the warm/cold split, the two hands almost touching, the monitor as portal — reads with emotional clarity at first glance. It does not yet. The lavender tint alone prevents it. Fix the overlay logic, fix the lighting fill, fix the arm span, and this frame earns the B. Do all of that and push the body rendering to match the face resolution, and it earns a B+. That is the target for Cycle 7.

The project is now in the range of pitchable. It is not yet at the level I would put in front of a network. The remaining distance is specific, named, and fixable.

---

*Victoria Ashford*
*Visual Development Consultant — 30 years industry experience*
*Cycle 6 Review — 2026-03-29*
