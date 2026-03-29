# Critic Feedback — Cycle 6
**Critic:** Dmitri Volkov, Character Design Lead
**Date:** 2026-03-29
**Subject:** Silhouettes (Neutral + Action), Luma Expression Sheet, Byte Expression Sheet

---

## VERDICT UPFRONT

This is the best cycle this team has produced. That is not a compliment — it is an observation, and a limited one. Every Priority 1 item from Cycle 5 has been addressed in code. The team read the critique and acted on it. That earns them something. But Cycle 6 reveals that fixing checklist items is not the same as achieving design excellence, and several of the "fixes" introduce new problems while solving old ones. The work is now in a zone where the obvious errors are gone and the subtle, harder-to-name errors are what stand between this package and something genuinely pitch-ready. Those subtler errors are what I am here to excavate.

---

## SECTION 1: CHARACTER SILHOUETTES

### Cycle 5 Issues — Resolution Status

**Cosmo's glasses as negative space — RESOLVED.**
The fix is correct and properly engineered. The double-draw approach (line 104-112: outer rim in SILHOUETTE, inner lens in NEG_SPACE) produces exactly the right result: a white cutout that registers as glasses even at thumbnail scale. The bridge rectangle (line 114) completes the read. This was the most critical failure in Cycle 5 and it has been solved cleanly. Full credit.

**Luma's pocket bump protrudes outside hem — RESOLVED.**
The calculation at line 61 correctly computes `hem_edge_at_mid` as the actual hem boundary at mid-body height, and the pocket rectangle starts at that edge and extends outward. The logic is sound. The bump will read.

**Cosmo's feet added — RESOLVED.**
Feet are present. They are minimal ellipses, which is the right stylistic choice for Cosmo. They complete his silhouette without overpowering his narrow-rectangle body read.

**Miri's distinctive visual hook — PARTIALLY RESOLVED.**
The shoulder bag (lines 187-194) is a genuine improvement over zero distinguishing features. The bag protrudes from the right side of the body, breaking the pure rectangle. However — see new issue 1c below.

---

### NEW ISSUES — Cycle 6

**1a. The layout code is a mess and it is producing a broken output.**
This is the most serious structural problem in the generator and it appears to have been written in haste. Look at the `generate()` function starting at line 465. A first image `img` is created at dimensions `W x H` (approximately 760 x 560). Then, starting at line 504, a SECOND image `img2` is created at `W x 600`. The first image is drawn on with `draw`, then silently abandoned — `img.save()` is never called. Only `img2.save(output_path)` runs. This means the title text written to `draw` at line 486 is discarded. The "NEUTRAL" and "ACTION" row labels at lines 523-524 are computed from `NEUTRAL_BASE - 220` which equals `260 - 220 = 40` — barely at the top of the canvas. The "ACTION" label at `ACTION_BASE - 220 = 500 - 220 = 280` puts it at the vertical midpoint, which is reasonably correct, but only by accident. This generator has dead code that creates a phantom canvas and then throws it away. That is not a minor style issue. It is a bug that reveals the code was not reviewed after writing.

**1b. The two-row layout has a critical vertical crowding problem.**
`NEUTRAL_BASE = 260` and `ACTION_BASE = 500`. That gives 240 pixels of vertical space for each row. Luma is 280px tall. Luma's silhouette is drawn with `base_y = NEUTRAL_BASE = 260` and the head starts at `base_y - LUMA_H = 260 - 280 = -20`. Luma's head is being clipped at the top of the canvas. This is not recoverable at render time — her hair blob, drawn at `hy - int(r*0.6)`, goes even further negative. The character is cropped. The same applies to Cosmo, who is `4.0 * HEAD_UNIT = 320px` tall — he extends to `260 - 320 = -60px`, cutting off 60 pixels of his head. This is a fundamental miscalculation. The team added a second row without recalculating whether the characters fit in the new geometry.

**1c. Miri's bag arm — the "right arm" is vestigial and incoherent.**
In `draw_miri_action()`, the comment at line 444 reads: `"Right arm similarly (but bag occupies that space, just show upper arm)."` The upper arm drawn (lines 445-446) terminates at `arm_y + int(arm_h * 0.45)` — roughly halfway down. So Miri's right arm ends mid-air. A character whose right arm is swallowed by a bag and whose left arm is visually present reads as asymmetrically incomplete. This is different from intentional asymmetry — it reads as an oversight. The bag-plus-arm relationship needs a design decision: either show the arm emerging below the bag, or draw the strap clearly so the visual logic is legible.

**1d. Byte's action pose barely differs from the neutral pose in silhouette terms.**
The action pose tilts the body top (`tilt = int(s * 0.20)`) and extends one arm to full length. At Byte's scale — 56 pixels tall — the tilt produces a body-top shift of roughly 11 pixels and the extended arm adds approximately 45 pixels to the right. From a squint-test perspective, the action Byte is "rectangle with a longer stick on one side." The neutral Byte is "rectangle with two short sticks." This is a meaningful difference at close range but collapses at thumbnail scale where you lose the arm detail entirely. Byte needs a more dramatic physical gesture for the action row — or the action row is not pulling its weight.

**1e. Column spacing vs. character width conflicts.**
`COL_W = 180` and there are 4 characters, giving a total width of approximately 760px. Luma's hem width is `hem_w = int(HEAD_UNIT * 0.70)` = approximately 56px to each side, giving a total Luma width of ~112px plus the pocket bump of `int(HEAD_UNIT * 0.30)` = ~24px more. Her action pose with the raised arm adds `cx + shoulder_w + lean + int(hu*0.22)` — potentially 100+ pixels rightward from center. At `col_cx = 50 + i * 180`, Luma is at x=50 and her extended arm action elements could reach x=50+100 = 150 — close to Cosmo's center at x=230. Characters in adjacent columns may overlap in action poses. This was not calculated.

---

## SECTION 2: LUMA EXPRESSION SHEET

### Cycle 5 Issues — Resolution Status

**Single expression expanded to 3-expression sheet — RESOLVED AND GENUINELY WELL DONE.**
The three expressions — Reckless Excitement, Worried/Determined, Mischievous Plotting — form a coherent emotional range that demonstrates the character's versatility. This is the correct trio: high energy, internal conflict, scheming. A pitch buyer reading these three faces understands Luma's dramatic register immediately. This was the second most critical Cycle 5 failure and it has been fixed with real creative ambition, not just mechanical compliance.

**Reckless Excitement asymmetry — RESOLVED.**
The brow asymmetry (left brow higher and kinked at line 126, right brow lower and cleaner at line 129) is the correct implementation. The pupil shift (lines 115-122) is a strong touch — both eyes looking screen-right implies the thing she's excited about is off-panel. The off-center grin (mouth arc shifted 6px left at line 136) reinforces the lopsided excitement. This is meaningfully better than Cycle 5's symmetric happy face.

**Curl artifact outlines removed — RESOLVED.**
The `_draw_hair_mass()` function (lines 29-39) now consists solely of fill ellipses with an explicit comment confirming the removal. No outline artifacts. The hair reads as a clean organic mass.

**Nose — still timid but this is a stylistic tolerance call.**
The nose remains two shadow dots and an arc (lines 56-58). At the 400x440 face panel size this is slightly more committed than the 600px closeup where it read as nearly absent. Acceptable at this scale.

---

### NEW ISSUES — Cycle 6

**2a. The Mischievous Plotting expression has a broken smirk geometry.**
The smirk is drawn in two pieces (lines 260-263):
- The right half: `draw.line([(cx-2, cy+36), (cx+36, cy+38)]` — a near-horizontal line from just left of center to far right.
- The left hook: `smirk_pts = [(cx-38, cy+32), (cx-20, cy+28), (cx-2, cy+36)]` — curving upward to the left.

The problem is the right half ends at `cx+36` which is well inside the face (head radius is 100px, so face extends to ~cx+100). The right corner of the mouth at `(cx+36, cy+38)` is orphaned in the middle of the face — it is not anchored to a corner dimple or jaw edge. The smirk looks cut off on the right side. A complete smirk should have a defined right corner even if that corner is flat. Currently the face reads as having a mouth that terminates mid-cheek.

**2b. The teeth chord for Mischievous Plotting is undersized and mispositioned.**
`draw.chord([cx-36, cy+28, cx+4, cy+46], start=5, end=100)` — the bounding box runs from `cx-36` to `cx+4`, meaning the teeth are left-shifted by ~16 pixels. The chord ends at angle 100°, which captures roughly the upper-left quadrant of an ellipse — this produces a small crescent in the upper-left area of the bounding box. This is not teeth. This is a visual artifact that reads as a blotch. The teeth should be a symmetric chord under the smirk arc, not a thin crescent tangent.

**2c. Worried/Determined is the weakest of the three expressions.**
The narrowed eyes (height reduced to 22 from 26-30) produce a subtly different look at this scale, but "subtle" is the enemy of a pitch expression sheet. The V-brow furrowing is well-executed in code (lines 194-198). The mouth — a straight line with downturned corners (lines 203-206) — is anatomically correct but emotionally underpowered. Worried/Determined should show the tension between the two states: the furrow is pure Determined, but what sells WORRIED is a slight tremor in the face — a raised inner brow corner (the corrugator muscle, which produces the "worried" kink at the inner brow tip), not just a V-furrow. The current expression reads as pure Determined, with Worried nowhere visible. This is a missed emotional duality.

**2d. Background colors are too timid to serve as emotional signal.**
`BG = (245, 240, 232)` — warm off-white. `BG_WORRY = (220, 230, 238)` — slightly blue-grey. `BG_MISCH = (235, 228, 245)` — slightly lavender. These colors are so close to each other (all within ~25 points on any channel) that they function as variations of "light" rather than as distinct emotional environments. At print scale or on a projected pitch deck, these panels will read as three versions of the same neutral background. If the background is worth coding, it should be worth making meaningful. Worry should be cold and desaturated. Mischief should have a warm purple glow. Excitement should be warm amber. The current palette distinction is invisible.

**2e. The expression sheet has no character scale reference or line-of-action indicator.**
Three floating heads. No neck-to-shoulder indication, no body language context. For a character expressions sheet intended for a pitch package, some minimal shoulder/collar indication would anchor each face in a body. The collar element exists in the code (`_draw_collar()`) and is called for all three expressions — this is good. But the faces are drawn at `face_cy = py + FACE_H // 2 + 20` in a 440px-tall panel at 400x440 resolution. The collar at `cy + head_r + 10 = cy + 110` may be partially outside the panel boundary depending on `face_cy`. At `face_cy = 240`, collar renders at y=350, inside a 440px-tall panel — safe. But this math should be explicit, not implicit.

---

## SECTION 3: BYTE EXPRESSION SHEET

### Cycle 5 Issues — Resolution Status

**Byte's right eye now carries emotion — RESOLVED AND IMPRESSIVELY SO.**
The `draw_right_eye()` function (lines 158-228) implements six distinct styles: flat, wide, wide_scared, angry, droopy, squint. Each is meaningfully different. The ALARMED `wide_scared` style (lines 180-189) with whites showing all around and a small centered pupil is the best single facial element in the entire Cycle 6 package — it is the "deer-in-headlights" read done correctly. The GRUMPY `angry` style with the heavy upper lid and downward-inward shifted pupil is a legitimate glare. The RELUCTANT JOY `droopy` style with the suppressed upturn at the corner (line 211) is the cleverest emotional acting in the script. This was the most egregious failure in Cycle 5 and it has been addressed with genuine craft.

**ALARMED and SEARCHING differentiated at body level — RESOLVED.**
The body_data system is a strong architectural decision. ALARMED has `arm_dy=-16, arm_x_scale=1.5, leg_spread=1.6, body_squash=0.92` — arms high and wide, legs splayed, body compressed. SEARCHING has `arm_dy=-4, arm_x_scale=1.1, leg_spread=1.2, body_tilt=-8` — leaning, reaching, exploring. These are genuinely distinct body reads. CONFUSED adds `body_tilt=-18` — the biggest tilt value in the set — which produces a strongly canted body suggesting the head-tilt confusion read. The body_data architecture is the single best design tool this team has built, and it works.

**Debug-style annotation labels redesigned — PARTIALLY RESOLVED.**
The annotation bar has been redesigned from "eye: loading" debug text to prev/next state context labels (`← was: SEARCHING`, `→ next: ALARMED/FOUND`). This is a conceptual improvement — it turns the annotation from a debugging artifact into narrative context. However, the text color `(120, 110, 140)` on `(10, 8, 18)` background is still low contrast at 11pt. And these labels are still programmer-facing in tone. For a pitch package, they need to either become bold typographic design elements or disappear entirely. "← was: SEARCHING" is not pitch language.

---

### NEW ISSUES — Cycle 6

**3a. GRUMPY's left eye uses the "normal" symbol, not a pixel-symbol.**
`draw_pixel_symbol()` is called with `cracked_symbol = "normal"` for GRUMPY (line 30 in the EXPRESSIONS list). The `draw_pixel_symbol()` function handles this at line 136: `grid = grids.get(symbol)` returns None for "normal", which triggers the normal iris-pupil eye draw instead of a pixel grid (lines 139-143). So GRUMPY's left eye — the cracked pixel display — is not displaying a pixel symbol. It is displaying a generic cartoon eye. This means GRUMPY has two organic eyes and zero pixel-display elements. Byte's entire design language is the pixel eye. GRUMPY is the one expression where that design language goes completely absent, and it is the first expression in the sheet. This is not an intentional design choice — it is a data entry error. GRUMPY should have a pixel symbol: either a downward line (disgust bar), a flat minus sign variant, or something custom. The "normal" value should not exist in the left-eye data column.

**3b. The GRUMPY body tilt direction conflicts with the emotional read.**
`body_tilt = 6` for GRUMPY — a slight rightward lean of the body top. Combined with `arm_dy=10` (arms lower than neutral, "slumped") this produces a character who is leaning slightly right with arms hanging. For disgust/grumpiness, you typically want either a squared-up confrontational stance (arms crossed, body upright) or an aggressive forward lean. A passive right-lean with drooping arms reads as tired or defeated, not grumpy. Compare this to CONFUSED which tilts at -18 for a strong visual lean. GRUMPY's lean is ambiguous at 6 pixels.

**3c. The pixel symbol for "!" renders as 3 pixels tall in context.**
At `byte_size = 88` (line 398), `eye_size = s // 4 = 22`. The `draw_pixel_symbol` function computes `cell = size // 5 = 22 // 5 = 4` pixels. The "!" grid has active pixels in column 2, rows 0, 1, 2, and 4. Each pixel is `4x4` minus 2px border = `2x2` effective. The exclamation mark is rendered as five 2x2 pixel squares in a vertical column, with a gap for the dot. At this scale the "!" is barely distinguishable from a vertical smear. The same applies to "?" — a 5x5 grid at 4px cells is 20x20 pixels total, with a border, yielding roughly a 16x16 effective rendering area. These symbols work at larger scales but at byte_size=88 they are at the edge of readability. The eye_size should be increased relative to the body, or byte_size should be increased for this sheet.

**3d. The hover particle confetti contributes nothing at this scale.**
Four 4x4 pixel squares below the feet (lines 360-366). At PANEL_W=240, PANEL_H=320, these dots are 4 pixels in a 240-pixel-wide frame — invisible noise. Either increase them to meaningful size (8x8 minimum, ideally 10x10 with varied shapes) or remove them. As rendered, they are invisible at normal viewing distance and draw the eye as noise artifacts when seen at close range.

---

## SECTION 4: OVERARCHING DESIGN SYSTEM CONCERNS

**4a. Miri remains underpowered as a character despite the bag.**
The shoulder bag is present and functional as a silhouette hook. But look at the cast: Luma has an A-line hoodie, chunky sneakers, curly hair cloud, and a pocket bump. Cosmo has a rectangular head with white-cutout glasses, a notebook, and slender proportions. Byte is a teal cube with a cracked pixel eye and magenta scars. Miri has... a wide rectangle body, a round head, and a bag that is a rectangle. Her design language is "rectangle + rectangle + circle." The bag differentiates her silhouette at a narrow angle but adds zero personality or story. What does Miri's design tell us about who she is? Nothing yet. A bag says "she carries things." That is not character.

**4b. No inter-character scale comparison across sheets.**
Silhouettes confirm the 5:1 height ratio between Luma and Byte. Luma's face sheet uses 400x440 per panel. Byte's expression sheet uses PANEL_W=240 at byte_size=88. There is no document in this package that puts all characters at their correct relative sizes side by side with faces visible. A pitch buyer needs to understand both "what do they look like" and "how do they relate spatially." These sheets answer each question separately and never together.

**4c. The production pipeline is accruing technical debt.**
The dead canvas in `silhouette_generator.py` (creating `img`, drawing on it, never saving it) is symptomatic of code that is growing via accretion rather than design. When tools accumulate dead code, the risk of the wrong output being saved — or no output being saved — increases with every cycle. These generators need a cleanup pass where someone runs them, verifies the output path, confirms the canvas dimensions match the content, and removes dead branches.

---

## CYCLE 7 REQUIRED IMPROVEMENTS

**Priority 1 — Must Fix Before Any External Pitch Use:**
1. `silhouette_generator.py`: Remove the dead `img`/`draw` canvas. Recalculate `NEUTRAL_BASE` to at least `LUMA_H + 20 = 300` to prevent character clipping at the top of the canvas. Verify ACTION_BASE leaves sufficient room for the tallest character plus action pose extensions.
2. `byte_expressions_generator.py`: Replace "normal" in GRUMPY's left-eye data with a pixel symbol appropriate to disgust (suggest a downward-arc pixel pattern, or a minus-sign grid `[0,0,0,0,0; 0,0,0,0,0; 1,1,1,1,1; 0,0,0,0,0; 0,0,0,0,0]` — but distinct from "flat" which is already used for POWERED DOWN).
3. `luma_face_generator.py`: Fix the Mischievous Plotting smirk — the right corner of the mouth must be anchored at a face-edge point, and the teeth chord must be repositioned symmetrically under the smirk arc.

**Priority 2 — Character Design Integrity:**
4. Luma's `draw_worried_determined()`: Add the inner-brow kink that marks the WORRIED component. The current expression reads as pure determination. One small raised-kink point at the inner end of each brow (the V-bottom should slightly lift on the inner side to produce the corrugator-muscle read) would split the emotion correctly.
5. Miri needs a design pass beyond the bag. One character-specific visual element that communicates personality, not utility. Suggested directions: a distinctive hairstyle (bun with a pencil through it? blunt-cut bangs?), a specific clothing pattern, or a prop that implies her role in the team's dynamic.
6. Luma expression panel backgrounds: increase color temperature separation between the three expressions so they read as distinct zones on a printed pitch page.

**Priority 3 — Polish and Scale:**
7. Byte `byte_size` on the expression sheet should be increased to at least 100 (from 88) to ensure pixel eye symbols render at a minimum cell size of 4px effective, giving symbols a 12x12 useful area.
8. Hover particle confetti: increase to 10x10px minimum or remove.
9. Byte's GRUMPY body tilt: adjust from +6 to either 0 (squared confrontational) or +12 (more assertive lean) with arm_dy raised to -5 (arms up, more aggressive posture, less defeated).
10. Produce one composite reference image showing all 4 characters at correct relative scale with face detail visible — this does not need to be a new generator, it can be assembled from existing outputs, but it needs to exist in the pitch package.

---

## OVERALL ASSESSMENT

**Grade: B−**

Here is how this grade is justified:

The three Priority 1 items from Cycle 5 have all been addressed. The body-data architecture for Byte is genuinely sophisticated and the right-eye system is the most improved single element across the entire run of this project. The three-expression Luma sheet demonstrates real creative ambition. The action pose row shows the team thinking about character in motion, not just in neutral position.

Against that: there is a canvas-clipping bug that means the primary silhouette sheet is likely rendering characters with their heads cut off. There is a data entry error that strips Byte of his defining design feature in the first panel of his expression sheet. There is a broken smirk geometry in the most interesting of the three Luma expressions. These are not style points — they are functional failures in the deliverables.

A B− says: you have learned to think like character designers. You have not yet learned to test and verify like production artists. The gap between "the code is conceptually correct" and "the output is clean and verified" is where this team continues to lose ground. Cycle 7 must include a review pass where someone runs every generator and looks at the output before declaring work complete.

"Elegant code that produces a clipped character is worse than inelegant code that produces a complete one."

---

*Dmitri Volkov — Character Design Critic*
*"The squint test applies to the code too. If you can't tell what a function is doing at a glance, it is going to produce errors you won't catch until the pitch meeting."*
