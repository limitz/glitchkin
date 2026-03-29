# Storyboard Critique — Cycle 9
**Critic:** Carmen Reyes, Storyboard & Layout Supervisor
**Date:** 2026-03-29 22:00
**Subject:** Cycle 9 — Verification of Critical Fixes + Full 26-Panel Cold Open Final Assessment
**Reference:** panel_chaos_generator.py (Cycle 9), contact_sheet_generator.py, statement_of_work_cycle9.md, critic_feedback_c8_carmen.md

---

## The Brief I Gave

At the end of Cycle 8 I gave a B / 80% and said: fix four things, then show them to me.

1. Dutch tilt geometry in P14 and P24 — state 12°, deliver 12°.
2. P21 overhead angle — 40-45° isometric, not 90° straight down. Characters need profile.
3. P24 hero framing — Luma lower-left third, cropped at bottom, camera looking up.
4. Expression library — add 'settling', 'recognition', 'warmth' and apply them to P17, P18, P20.

I am now verifying each of these. I am not going to soften my assessment. I said I would raise the grade if these were fixed. I am going to determine whether they were.

---

## Verification Item 1: Dutch Tilt P14 / P24 — Does `apply_dutch_tilt()` Deliver a Real ±12°?

### What I found:

A new helper function has been added: `apply_dutch_tilt(img, degrees, bg_color)`.

The implementation:
```python
draw_area = img.crop((0, 0, PW, DRAW_H))
rotated = draw_area.rotate(degrees, resample=Image.BICUBIC, expand=False,
                           fillcolor=bg_color)
img.paste(rotated, (0, 0))
```

This uses `Image.rotate()` on the full canvas draw area (not a single floor line, not a slope polygon). The `expand=False` keeps it in-place; the `fillcolor` fills the rotated corners with the scene's background. The rotation applies to every pixel in the drawn scene — floor, walls, characters, props, annotations, everything. This is geometrically correct.

In the PANELS spec:
- P14: `dutch_tilt_deg=12` — 12° clockwise.
- P24: `dutch_tilt_deg=-12` — 12° counter-clockwise (negative = CCW in PIL's rotate convention). The comment reads "TRUE 12° Dutch tilt LEFT — canvas rotation."

The previous implementation used a sloped floor polygon that delivered approximately 0.7°–1.3° visually. The current implementation delivers the stated angle to every pixel in the image. This is not a floor line that suggests tilt — this is a rotated scene that IS tilted.

**Verdict: FIXED. The Dutch tilt geometry issue is resolved. P14 and P24 will render with genuine ±12° full-canvas rotation.**

One note I want on the record: the function does not use `expand=True`, which means at 12° rotation some content at the corners will be clipped. At 12°, the corner clip on a 480×222 draw area is approximately 24px in the worst corners. This is acceptable — it fills with the scene's dark background color, which reads as the tilt pushing out of frame. This is cinematic behavior, not an error. The clipping actually reinforces the Dutch tilt read.

---

## Verification Item 2: P21 Overhead — Is It 40-45° Isometric? Are Characters Distinguishable?

### What I found:

The `draw_p21()` function has been substantially redesigned. The camera angle annotation reads: "HIGH ANGLE 40-45° — not straight down — profiles visible."

**The spatial structure:** Back wall occupies the upper 38% of the draw area (`back_wall_bot = int(DRAW_H * 0.38)`). The floor plane fills 38% to the frame bottom. Perspective grid lines run from the back wall junction down through the floor. This is isometric staging — we see back wall and floor simultaneously. The 90° bird's-eye view had only a floor grid with overhead character stamps. This has depth.

**Luma rendering at high angle:**
- Shoulder mass as a horizontal ellipse (foreshortened from above)
- Partial face profile — skin-tone ellipse (`LUMA_SKIN`) with a visible eye element
- Dark hair mass above
- Arm foreshortened upward toward monitors (angled toward back wall)
- Foreshortened legs below shoulder mass

At 40-45° we legitimately see some of her front-facing profile. She is no longer a hair circle. The skin-tone face ellipse plus the dark hair mass plus the mint PJ shoulder ellipse creates a three-color character stamp that reads as Luma at wide-shot scale.

**Byte rendering at high angle:**
- Flat ellipse top face (foreshortened from above)
- Front face rectangle (profile visible at angle — the face with the cracked eye is on the rectangle, not the ellipse top)
- Spike rendered as a triangle above the top ellipse (spike is visible from above)
- Visible eye drawn on the front face rectangle

This is the key distinguishability fix I flagged: Byte's spike as a triangle from above. At wide-shot scale, the spike triangle on top of the cyan body is the identifying mark that separates Byte from the Glitchkin in the monitors.

**Glitchkin in monitors:** These are small rectangles and ellipse-faces at 6-12px, contained within the monitor bezels. They do not occupy the floor plane. The separation between "characters on floor" and "Glitchkin in monitors on back wall" is now spatial — they literally occupy different planes of the image.

**Verdict: FIXED. The camera angle is isometric/high-angle, not straight-down. Characters have profile. Byte's spike is the distinguishing mark from overhead. The Luma-vs-Byte-vs-Glitchkin confusion I flagged is resolved by plane separation.**

However, I want to register one remaining concern that is not a failure but is an honest note: Luma's face profile at this scale (the skin-tone ellipse is approximately 22px wide and 16px tall in the draw area) is distinguishable at full panel resolution but will be marginal at contact-sheet thumbnail scale (these panels are rendered at ~240px wide on the sheet). At thumbnail, Luma reads as a three-color shape (dark hair / skin face / mint PJ). That is enough. It is enough. But barely. If this show moves to production and this overhead shot appears in an animatic, the scale will need to increase before editorial review.

---

## Verification Item 3: P24 Hero Framing — Luma in Lower-Left Third, Cropped at Bottom?

### What I found:

The `draw_p24()` function has been redesigned for hero framing.

The placement:
```python
luma_cx = int(PW * 0.22)    # Left third of frame (not center)
luma_cy = int(DRAW_H * 0.72)  # Low — figure extends below frame bottom (cropped)
```

22% from left = lower-left third. Confirmed.

The body bottom: `body_bot = DRAW_H + 20` — the body rectangle is drawn 20 pixels PAST the draw area boundary. The legs are also drawn crossing `floor_y`. This is an intentional crop at the bottom edge. The figure extends past the frame.

Face placement: with `luma_cy = int(DRAW_H * 0.72)` and `draw_luma_face()` called at `luma_cy - 55` (the head offset from torso center), the face center is at approximately 61% from top of draw area. Given that DRAW_H = 222 and PH = 270, the face center is at pixel 135. In a 270px-tall panel, that is approximately the lower half of the draw area.

The body reads as a large foreground figure filling the lower-left: torso at 72% depth, arms extending to either side, legs cropped at bottom. This is the low-angle hero read.

The annotation: "THE HOOK FRAME — still point in the storm. Hold 1.5s — Luma lower-left, chaos fills frame." The Dutch tilt annotation: "WIDE — DUTCH 12° canvas rotate — low angle hero." Both are in the image.

Background: 35 Glitchkin with 4-7 sided irregular polygons (per the PANELS spec), plus pixel confetti at maximum saturation (80 particles, 5 colors), plus Byte on Luma's shoulder at `luma_cx + 44, luma_cy - 78` — Byte occupies the upper-left region above and to the right of Luma's head.

**Verdict: FIXED. Luma is in the lower-left third. The figure is cropped at the bottom (intentionally, body extends past frame). The camera angle reads as looking up at her. The Dutch tilt plus the lower-left placement creates the heroic low-angle-wide framing that was absent in Cycle 8.**

I note that with `luma_cy = int(DRAW_H * 0.72)` the figure might read as slightly "too low" — her face center is at 61% of the draw area, which puts her very much in the lower portion. This is not a failure. The question is whether the face reads against the chaos behind it at that depth. Given that the face uses the 'reckless' expression (large grin, star-pupils, bright white sclera) against a dark glitch background, the contrast should hold. The expression is correct. The placement is correct. The framing is executed.

---

## Verification Item 4: Expression Library — 'settling', 'recognition', 'warmth' Added and Applied?

### What I found:

All three states are implemented in `draw_luma_face()`:

**'settling' (P17):**
- Both eyes at full aperture (eh * 1.0 — open but not alarmed-wide)
- Dilated pupils (size 4 ellipses — wonder)
- Brows raised gently on both sides (not alarmed asymmetry)
- Mouth: arc curve (not rectangle scream) PLUS small oval gap below — soft open wonder breath

This is the "comma before the next exclamation" expression I specified. Open and attentive without the alarm state. The code comment explicitly cites my language from the Cycle 8 brief: "the comma before the next exclamation." Applied to P17 with `expression='settling'`. Byte's expression in P17 changed from 'alarmed' to 'resigned' — the comment reads "CYCLE 9 FIX: Expression 'resigned' not 'alarmed' — quiet beat, not alarm beat."

**'recognition' (P18):**
- LEFT eye at 0.9 aperture (more open — the raised-brow side)
- RIGHT eye at 0.55 aperture (narrowed — concentration squint)
- LEFT brow positioned higher (raised — the "aha!" brow)
- RIGHT brow lower, furrowed inward (concentration)
- Mouth: slight pursed arc (thinking, not smiling or open)

This is an asymmetric expression. The asymmetry is the point — I said "recognition, not curiosity" and the distinction is encoded in the eye aperture difference and the asymmetric brow line. Applied to P18 with `expression='recognition'`. The comment cites my language: "Carmen: 'recognition, not curiosity' — this is cognitive connection."

**'warmth' (P20):**
- Both eyes at 0.7 aperture (happiness squint — eyes slightly narrowed)
- Both brows gently raised (peaceful arc, not alarmed spike)
- Soft smile arc (not grin rectangle — the width is `r//3`, not `r//2`)
- Cheek lift lines (warmth crinkle — `fill=(180, 110, 70)`)

The comment cites my brief directly: "She is choosing warmth deliberately." This is deliberate emotional intent encoded in face geometry. Applied to P20 with `expression='warmth'`. The code comment notes: "CYCLE 9: Added 'settling' (P17), 'recognition' (P18), 'warmth' (P20) per Carmen's critique."

**Verdict: FULLY FIXED. All three expression states are implemented with geometric specificity, correctly applied to their target panels, and each is documented with the production rationale. The expression library gap that was showing across P17/P18/P20 is closed.**

The 'recognition' expression is the strongest of the three — the asymmetric eye aperture (0.9 vs 0.55) creates a genuinely distinct face from any of the other states. At panel scale, asymmetric expressions read at thumbnail where symmetric ones blend together. This was the hardest state to get right and they got it right.

---

## Summary of Fix Verification

| Issue (Cycle 8 Critical) | Status |
|---|---|
| Dutch tilt P14 — full canvas rotation via Image.rotate() | **FIXED** |
| Dutch tilt P24 — full canvas rotation via Image.rotate() | **FIXED** |
| P21 overhead — 40-45° isometric with character profiles | **FIXED** |
| P24 hero framing — Luma lower-left, cropped at bottom | **FIXED** |
| 'settling' expression added and applied to P17 | **FIXED** |
| 'recognition' expression added and applied to P18 | **FIXED** |
| 'warmth' expression added and applied to P20 | **FIXED** |
| P17 Byte expression — changed from 'alarmed' to 'resigned' | **FIXED** |

All four critical items from the Cycle 8 brief are resolved. Four additional fixes (P17 Byte expression, three expression states) go beyond the minimum brief. The team addressed the significant issues alongside the critical ones.

---

## Full 26-Panel Cold Open Assessment — Cycle 9 Eyes

### Does the sequence now function as a complete, compelling pitch sequence?

Yes.

I do not use the word "compelling" lightly. A pitch sequence has to do three things simultaneously: establish the world, establish the characters, and give the viewer a reason to come back. Let me evaluate each.

**World establishment:** The warm amber domestic world (P01-P07) against the cold CRT glitch world (P08 onward) is the visual thesis of the show. This color war is present in every panel after P07 — warm tones losing ground as the glitch asserts itself. By P24, the warm amber is only in Luma's PJ fabric and skin tone; everything else is cyan-magenta-acid. That progression is the show's visual argument: the world is changing and the warmth has to hold its ground. A network executive looking at this contact sheet will understand the world before reading a single caption.

**Character establishment:** Luma is curious, reckless, warm, and has been drawing Glitchkin in her margins for months without knowing they were real (P18 — the margin doodles are in the frame, visible, not just described). Byte is offended, dignified, resigned, and against his will stuck to a girl who might be the only person who could ever recognize what he is. P19 is still the strongest single panel in the sequence. The expression — offended, arms crossed, one finger raised then put down — tells us who Byte is in 270 pixels.

**Reason to come back:** The promise shot (P23) followed by the hook frame (P24) does this correctly. P23 shows us two characters facing the impossible together from behind — we cannot see their faces, we see their resolve. P24 shows us Luma's face: jaw set, star-pupils, reckless grin. This is a character who is delighted by the impossible. That is the show's promise. An audience watching this cold open will want to know what happens next not because of plot stakes but because they want to spend more time with someone who grins at chaos.

---

### What Takes This From B to A

I said I would raise the grade. I am raising it. But I am not raising it all the way and I am going to tell you exactly why.

**What is still not at A:**

**1. P22 — Glitchkin crowd still lacks shape variety.**
I flagged this in Cycle 8 as significant. The eight Glitchkin in P22 are all rectangles with circular face overlays. P24's Glitchkin are correctly varied (4-7 sided irregular polygons). The same variety logic was not applied back to P22. This is an inconsistency within the same sequence — P24 has the correct Glitchkin mob feel; P22's ECU screen feels like a different (lesser) version of the same creatures. An ECU should show MORE detail, not less variety. P22 is the panel where we see the Glitchkin closest. They should be the most varied here, not the least.

**2. P23 — Monitor bowing still compositionally underpowered.**
I raised this in Cycle 8. The five bowing monitors use radial gradient ellipses with values around `min(255, bv + 80)` where the base `bv` is low. The monitors are dark screens with moderate glowing. They should be straining, about to burst — "as if the screens are balloons being inflated from inside." The current render communicates "screen with glow." The promise shot's visual energy depends on those monitors feeling dangerous. They do not yet feel dangerous. They feel like they are displaying something unusual. This is a 25% energy level. It needs to be at 80%.

**3. P15 body language issues unresolved.**
The arm asymmetry (left arm should be HIGH and left, right arm pointing directly RIGHT — asymmetric spread-eagle), the leg angle (legs at 25° off vertical rather than closer to 90° for floor-level camera), and the body squash (circular torso, not horizontally compressed) were flagged as significant in Cycle 8. None of these appear in the Cycle 9 statement of work. P15 was not addressed this cycle. The glitch-forced hair symmetry (the most important visual in the panel) remains correctly executed, so the panel still works. But the physical comedy of the body language remains underperformed.

**4. The 26th panel — contact sheet — still says "Cycle 8 Contact Sheet."**
The contact sheet generator header reads: `"Ep.01 Cold Open — Cycle 8 Contact Sheet (P01–P25 complete)"` and `"2026-03-29 Cycle 8"`. These strings are not updated to Cycle 9. This is documentation hygiene, not a creative failure, but a contact sheet that says "Cycle 8" when the panels reflect Cycle 9 fixes will cause confusion in any production review. The arc labels in `arc_labels` also refer to wrong row placements if the panel count has shifted. These need to be updated.

---

### Panel-by-Panel Score Update (Changed Panels Only)

| Panel | Cycle 8 | Cycle 9 | Change |
|---|---|---|---|
| P14 | B- | B+ | Dutch tilt now geometrically correct |
| P17 | B | B+ | Settling expression + Byte expression corrected |
| P18 | B | A- | Recognition expression is genuinely distinct, notebook detail was already excellent |
| P20 | B+ | A- | Warmth expression is correctly executed as emotional intent, not default state |
| P21 | B- | B+ | Isometric angle fixed, character profiles readable |
| P24 | B- | B+ | Hero framing corrected, Dutch tilt present |

Unchanged panels retain their Cycle 8 scores. P15 remains B (unaddressed body language). P22 remains B (unaddressed Glitchkin shape variety). P23 remains B (monitor bowing underpowered).

---

## Final Verdict

The four critical fixes were made. They were made correctly and specifically. The team did not just change the code — they left documentation of WHY in the code comments, citing the exact language from my critique. That indicates the MEMORY.md lesson cycle is functioning correctly. The critique is being read, understood, retained, and applied with precision.

The expression work on 'recognition' is particularly strong. Asymmetric eye aperture (0.9 vs 0.55) creating a distinct "aha" brow on one side and a concentration squint on the other — this is production-grade character design thinking in a storyboard tool. When a future artist needs to rebuild this expression for animation, the rationale is in the code.

The remaining issues (P22 Glitchkin variety, P23 monitor energy, P15 body language, contact sheet version string) are real but none of them break the sequence. The cold open works. It has a beginning, a structural middle, and an ending that makes you want to see what happens next.

The show is here. It has been here since P22a's warm gold confetti spark.

**Final Grade: B+ / 87%**

*(Raised from B / 80% on the basis of all four critical fixes correctly implemented, expression library fully resolved, Byte's P17 expression corrected. Not yet A because P22 Glitchkin variety remains unaddressed, P23 monitor bowing is still underpowered, P15 body language was not touched this cycle, and the contact sheet carries stale version strings. These are the four items standing between B+ and A. Fix them in Cycle 10.)*

**Brief for Cycle 10:**

1. P22 — Glitchkin crowd shape variety. Match P24's 4-7 sided irregular polygon approach. An ECU of the crowd should show more variety, not less. Rectangles only is not enough.
2. P23 — Monitor bowing. These screens need to read as STRAINING. Increase the hot-spot gradient contrast on the bowing monitors. The promise shot's visual energy depends on the threat being visceral, not decorative.
3. P15 — Body language. Left arm high-and-left, right arm pointing directly right (asymmetric spread-eagle). Legs closer to 90° off vertical for floor-level camera. Horizontal torso compression (squash before impact). This is physical comedy — geometry must deliver the joke.
4. Contact sheet — Update version strings to Cycle 9. Fix arc label row placement if panels have shifted.

The work is getting there. Do not stop now.

— *Carmen Reyes*
