# Critic Feedback — Cycle 5
**Critic:** Dmitri Volkov, Character Design Lead
**Date:** 2026-03-29
**Subject:** Silhouettes, Luma Face Closeup, Byte Expression Sheet

---

## VERDICT UPFRONT

Progress. Real progress. Cycle 4's catastrophic silhouette failure — Luma and Miri as indistinguishable blobs — has been addressed. The silhouette sheet now passes a basic squint test where it previously failed completely. Byte's expression sheet is a genuine creative asset. But there is sloppiness that would get this package rejected at any serious pitch meeting. Read carefully.

---

## 1. CHARACTER SILHOUETTES — `character_silhouettes.png`

### What Was Fixed
- **Luma's silhouette is now distinct from Miri's.** The trapezoid A-line hoodie and the oversized chunky sneakers work exactly as intended. At thumbnail scale, Luma reads as a flared-bottom shape with big round feet versus Miri's taller round-head-on-rectangle shape. This was the critical Cycle 4 failure and it has been corrected. Credit where due.
- **Byte is tiny and chamfered.** The micro size differential is preserved and Byte's boxy silhouette reads at all scales. The stubby arm nubs add to legibility.
- **Cosmo has a vertical narrow-tall read** with the notebook arm extension providing a secondary hook. Acceptable.

### What Still Fails

**1a. Cosmo's glasses are invisible.**
The glasses on Cosmo are drawn as filled-black ellipses over a black silhouette. They provide zero read. They are invisible. The code confirms this: glasses are drawn `fill=SILHOUETTE` — the same near-black color as the body. This is a fundamental silhouette construction error. A silhouette sheet exists to prove readability in pure shape. If Cosmo's defining characteristic — the thing that makes him "the scholar" — doesn't register as a negative-space feature (white circles cut from the silhouette) or a protruding shape, then Cosmo has no face-level recognition. He just looks like a thin rectangle. Fix: glasses must be a white (negative space) cutout in the silhouette, or the lenses must protrude as a separate shape beyond the head profile.

**1b. Luma's pocket bump is visually inert.**
The code adds a pocket bump on the right side of the hoodie. In the rendered image it is swallowed by the hem and reads as nothing. At thumbnail scale: invisible. If the pocket bump is supposed to be a secondary silhouette hook for Luma's hoodie design, it needs to protrude beyond the hem silhouette edge, not sit inside it. Currently it adds zero read value.

**1c. Cosmo's feet are absent.**
Cosmo's legs terminate without any foot shape. Compared to Luma's emphatic chunky sneakers and even Miri's simple block feet, Cosmo just... stops. His legs are stick-thin rectangles that end at the ground line. This isn't a stylistic choice — it reads as unfinished. Add a minimal foot shape to complete the silhouette.

**1d. Miri's design is still dangerously generic.**
Miri is round head + wide rectangle body + stub legs. That is literally the most default character silhouette possible. We are told she is "the steady one," but steady should not mean visually characterless. She has no distinctive hook — no accessory, no prop, no hairstyle feature, no clothing element that sets her apart. She will be confused with any placeholder character in any other cartoon. This needs a design pass before the pitch package.

**1e. Scale relationships need a ground-plane anchor.**
Byte reads as very small but the relationship between Byte and the humans is ambiguous. Is Byte 20% of Luma's height? The code says `s = int(LUMA_H * 0.20)` which gives Byte roughly 56px versus Luma's 280px. That's a 5:1 height ratio — dramatic. But in the rendered image the horizontal spread of Byte's arms and the spacing between characters makes Byte look closer to 25% scale. Consider compositing them closer together to make the scale drama clearer on the squint test.

---

## 2. LUMA FACE CLOSEUP — `luma_face_closeup.png`

### What Was Fixed
- **The face is warm, expressive, and characterful.** The reckless excitement grin reads clearly. Large eyes, arched brows, high blush, and the wide chord smile communicate the correct emotional temperature. This is a competent cartoon face.
- **The curly hair mass is distinctive.** The asymmetric curl cloud establishes Luma's silhouette even at face level. This is one of the better choices in the whole package — the hair alone sells "this specific character."
- **The hoodie collar detail** with the cyan pixel hint is a nice touch that ties Luma to the digital world.

### What Still Fails

**2a. The expression is technically correct but emotionally shallow.**
"Reckless Excitement" should feel dangerous — a kid who is about to do something inadvisable and knows it and doesn't care. What we have is a standard cartoon happy face. The grin is symmetric and clean. The eyes are wide but not mischievous — they lack the asymmetric spark (one brow higher, one eye slightly squinting) that separates "excited" from "recklessly excited." This distinction matters enormously for character voice. A pitch buyer needs to understand Luma's personality from a single face. Right now they'd read her as "happy kid." That's not specific enough.

**2b. One expression is not a face closeup sheet.**
The luma_face_generator.py has an expression parameter but generates a single image. For a pitch package, you need minimum 3 expressions from the same character to demonstrate emotional range. Reckless Excitement, Worried Uncertainty, and Frustrated Determination would give buyers confidence in the character's versatility. A single expression is a character icon, not a character sheet.

**2c. The nose is too timid.**
Two tiny shadow dots and a faint arc. At production scale this could be fine — simplified noses are standard. But for a pitch closeup image, at 600x600px, the nose reads as nearly absent. This makes the face feel incomplete around the center mass. A slightly more committed nose shape (even just a small rounded bump or a definite arc) would anchor the face proportions better.

**2d. The curl detail circles in the hair background are a mistake.**
The code draws faint circular outlines over the hair background (`draw.ellipse(..., outline=(40, 25, 12), width=2)`) for "individual curl definition." In the rendered image these appear as muddy brownish circles sitting on top of the hair and read as artifacts or errors rather than detail. They make the hair look dirty and unresolved. Remove them or replace with a genuine texture approach.

---

## 3. BYTE EXPRESSION SHEET — `byte_expressions.png`

### What Works — And Works Well
This is the strongest asset in the package. The pixel-eye system is a clever, distinctive design choice. The 5x5 grid symbols (!, ?, heart, loading, flat) give Byte a visual vocabulary that is immediately readable and completely unlike anything the human characters do. The dark background is the correct choice — Byte's teal body pops. The magenta scar markings add asymmetry and history to what could otherwise be a generic robot cube.

The POWERED DOWN expression with flat line eyes is genuinely good. The GRUMPY with the downturned mouth is the clearest emotional read. The pixel eye system as a concept is distinctive enough to be a merchandising and animation hook.

### What Still Fails

**3a. The right eye is doing nothing 5 out of 6 times.**
The code gives Byte a "cracked pixel display" left eye and a "normal" right eye. The normal eye is a basic iris-pupil circle. The result: in every expression except POWERED DOWN, one eye is doing interesting character work and the other is a generic cartoon eye that belongs to a completely different character. This asymmetry is presumably intentional — the cracked damaged eye versus the working eye — but it reads as unresolved. Either lean fully into the asymmetry (make the normal eye's expression complement the pixel eye meaningfully) or give the right eye its own pixel-display type with a different expression mode. As-is, the right eye is dead weight.

**3b. RELUCTANT JOY and CONFUSED are not distinct enough at a glance.**
The pixel-eye symbols for these two are different (heart vs. question mark) but the mouth shapes are both small and similar. CONFUSED has a squiggle mouth; RELUCTANT JOY has a small upturn. At speed — which is how these would be evaluated — the two panels look nearly identical except for the left eye symbol. The whole-body emotional read needs to differ more. Add a physical posture suggestion (tilted head for CONFUSED, rigid clenched-arm posture for reluctant joy) to differentiate them.

**3c. ALARMED needs to be more alarming.**
The "!" pixel eye symbol is the right choice. But the mouth is a small O circle — the same shape as SEARCHING/CURIOUS. Alarmed should have a larger open mouth, the jaw should drop further, and ideally the body should convey tension (arms up, torso rigid). Currently ALARMED and SEARCHING are nearly identical body reads.

**3d. The expression labels at the top of each panel are too small and low-contrast.**
`eye: normal`, `eye: loading` etc. in grey text on dark background. These are annotation labels, not design elements. They're useful for the team's internal communication but in a pitch package they look like a programmer's debug overlay. For any external-facing version of this sheet, those technical labels need to go or be redesigned as clean typographic callouts.

---

## 4. CODE QUALITY REVIEW

### `silhouette_generator.py`
The trapezoid body polygon for Luma is a solid approach. The major bug is the glasses rendering for Cosmo — filling glasses with the same SILHOUETTE color makes them invisible. This must be corrected. The pocket_x calculation places the pocket at `cx + int(hem_w * 0.55)` which is inside the hem boundary, not outside it — this is why the pocket reads as nothing. Cosmo has no foot geometry at all — the legs simply end.

### `luma_face_generator.py`
Clean, readable code. The expression system is in place (`if expression == "reckless_excitement":`) but only one expression branch is implemented. The arch eyebrow code at line 88-90 uses a pts list passed to `draw.line()` — this is a polyline approximation of a curved brow, which gives a jagged result. A proper arc call would produce a smoother brow. The stray curl arc overlays at lines 119-120 partially obscure the upper face and don't read as intentional design.

### `byte_expressions_generator.py`
The pixel symbol grid system is well-designed and extensible. The EXPRESSIONS list is a clean data structure. Main issue: the right-eye logic at line 168 only branches for "flat" — all other expressions get the same "normal" right eye. This means the right eye has zero expression contribution in 5 of 6 panels. The hover particle confetti is a nice touch but at the rendered size (4x4 pixel squares) it's barely visible and reads as noise.

---

## CYCLE 6 REQUIRED IMPROVEMENTS

**Priority 1 — Must Fix Before Any External Pitch Use:**
1. Cosmo's glasses must render as negative space (white cutout) in the silhouette sheet
2. Luma face closeup must be expanded to a minimum 3-expression sheet
3. Byte's right eye must carry emotional information — the "always normal" default is wasted design space

**Priority 2 — Character Design Integrity:**
4. Miri needs a distinctive visual hook — one accessory or clothing element that uniquely identifies her
5. Luma's "reckless excitement" must read as mischievous, not just happy — adjust brow asymmetry and add a hint of squint to one eye
6. ALARMED and SEARCHING must be visually differentiated at body-read level, not just eye symbol

**Priority 3 — Polish for Pitch Package:**
7. Remove the debug-style annotation labels from Byte's expression sheet for any external version
8. Luma's hair curl detail circles (the brownish outline overlays) should be removed — they read as artifacts
9. Cosmo needs foot geometry
10. The pocket bump on Luma's hoodie must protrude outside the hem boundary to register in silhouette

---

## OVERALL ASSESSMENT

Cycle 5 addressed the critical silhouette failure. That was the right priority. Byte's expression sheet is the most finished-looking asset this team has produced and is genuinely pitch-adjacent. Luma's face has warmth and is on the right track.

But "on the right track" is not the same as "ready." The missing glasses read on Cosmo is an inexcusable regression — that is a squint-test failure on a squint-test sheet. Luma's single expression face is not a character sheet, it's a portrait. And Byte's dead right eye undermines the entire expressiveness claim.

The team is learning. The tools are improving. The design language (pixel eyes, teal-and-magenta Byte, curly-haired Luma, trapezoid hoodie) is starting to cohere into something real. Cycle 6 has a clear path. Do not ship to any external party until Priority 1 items are resolved.

---
*Dmitri Volkov — Character Design Critic*
*"If it doesn't read at thumbnail size, it doesn't exist."*
