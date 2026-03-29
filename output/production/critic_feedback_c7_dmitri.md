# Critic Feedback — Cycle 7
**Critic:** Dmitri Volkov, Character Design Lead
**Date:** 2026-03-29
**Subject:** Silhouette Sheet (Neutral + Action), Byte Expression Sheet, Luma Expression Sheet

---

## VERDICT UPFRONT

Cycle 7 is a genuine step forward. Every Priority 1 item from my Cycle 6 review has been addressed — not with placeholders or minimum viable patches, but with real thought applied to each problem. The canvas clipping is fixed. The dead canvas code is gone. GRUMPY now has a pixel eye. The mischievous smirk no longer produces a crescent blob. This team can take instruction, act on it precisely, and deliver measurably improved output. That matters.

But "measurably improved" is not the same as "ready." The work has moved from broken to functional. It has not yet moved from functional to exceptional. There are structural design problems that no amount of bug-fixing will solve — problems that require a designer to make active creative decisions rather than code corrections. This cycle, those problems are the thing standing between the package and a pitch-ready state. I am going to name them exactly.

---

## SECTION 1: BUG VERIFICATION — CYCLE 6 PRIORITY 1 ITEMS

### Bug 1 — Canvas Clipping: RESOLVED

`NEUTRAL_BASE` has been raised from 260 to 380. The math now works:

- Cosmo at `4.0 * HEAD_UNIT ≈ 320px` has his top at `380 - 320 = 60px` — 60 pixels of clearance above the tallest character. Safe.
- Luma at 280px has her top at `380 - 280 = 100px`. Her hair blob extends upward by approximately `int(r * 0.6) ≈ 21px`, giving a hair top of approximately y=79. Safe.
- `ACTION_BASE = 380 + 240 = 620`. Total canvas `H2 = 620 + 60 = 680px`. Action row characters render within that space.

Characters are no longer decapitated. This was the most critical functional failure in the previous cycle and it is cleanly resolved.

### Bug 2 — Dead Canvas Code: RESOLVED

The phantom `img`/`draw` canvas that was created, drawn upon, and then silently discarded has been removed entirely. The `generate()` function now creates a single canvas (`img2`/`draw2`) and saves it. No dead branches, no abandoned output. The code is structurally clean for the first time.

### Bug 3 — GRUMPY Pixel Eye: RESOLVED

GRUMPY's left eye symbol has been changed from `"normal"` to `"grumpy"`. A new `"grumpy"` grid has been added to the `grids` dictionary:

```
[0,0,0,0,0]
[1,0,0,0,1]
[1,1,1,1,1]
[1,0,0,0,1]
[0,0,0,0,0]
```

This is a minus-bar with corner anchor ticks — visually distinct from the POWERED DOWN `"flat"` bar (which has no corner marks), and legible as a scowl pattern. Byte's design language — the pixel eye as emotional display — is now intact in the first panel of the expression sheet.

One caveat I will register: the corner-tick pattern `[1,0,0,0,1]` on rows 1 and 3 is geometrically symmetric. At the rendered cell size (4px cells = 20px total grid at `byte_size=88`), this produces a box outline with a horizontal bar across the middle. The visual result is ambiguous — it reads as a "scowl rectangle" rather than a clear disgust symbol. This is functional but not the sharpest possible pixel-art solution. An asymmetric downward-arc pattern would have been more immediately readable as grumpiness. Resolved technically; design quality of the solution is "adequate."

### Bug 4 — Mischievous Smirk Crescent Artifact: RESOLVED

The broken `draw.chord()` teeth — which produced a thin upper-left crescent — has been replaced with an explicit filled polygon using seven anchor points:

```python
teeth_pts = [
    l_corner,                    # (cx-38, cy+30) — raised left corner
    (cx - 18, cy + 30),          # left inner curve
    (cx + 10, cy + 30),          # right inner curve
    (cx + 55, cy + 38),          # right corner — anchored at cheek
    (cx + 40, cy + 46),          # right bottom
    (cx + 0,  cy + 48),          # bottom centre
    (cx - 28, cy + 44),          # left bottom
]
```

The right corner is now anchored at `(cx + 55, cy + 38)` — significantly beyond the halfway point of the face (head radius = 100px, so cx+55 is more than halfway to the face edge). The smirk no longer terminates mid-cheek. The teeth polygon is a genuine tooth-shape, not a crescent artifact. This is the correct fix and it was implemented thoughtfully.

---

## SECTION 2: NEW ISSUES — CYCLE 7

The bugs are fixed. Now let me tell you what is still wrong. Because there is plenty.

---

### 2a. SILHOUETTE SHEET — Miri's arm fix is mechanically correct but design-incoherent

The Cycle 6 critique called out Miri's right arm as terminating mid-air (truncated by the bag). The Cycle 7 fix produces a forearm that emerges below the bag bottom edge, rendered at `forearm_top = bag_y + bag_h + int(hu * 0.05)` — approximately just below the bag. The forearm then extends downward with a hand ellipse at the end.

This is anatomically present, which is an improvement. But read the visual result: Miri's right arm has an upper arm that disappears behind the bag, a gap at bag level, and a forearm that appears below. The bag is positioned at `bag_y = body_top_y + int(body_h * 0.45)`, with `bag_h = int(hu * 0.55)` — so the bag occupies the mid-to-lower torso region on the right side. The arm emerges below this, effectively from hip level. The forearm is detached from the shoulder in any visual sense.

In silhouette terms — which is the entire purpose of this sheet — a detached forearm below a bag reads as a third limb, not a complete arm. The visual logic is not legible at squint distance. The fix satisfied the letter of my critique (arm no longer truncated) but not the spirit (arm reads as a coherent body part). A proper solution requires either: (a) showing a clear strap on the bag so the viewer's eye connects shoulder→strap→bag→arm, or (b) repositioning the bag so the full arm contour is visible.

**Design grade on this element: C+. Mechanically present; visually confusing.**

---

### 2b. SILHOUETTE SHEET — Byte's action pose still fails the squint test

I raised this in Cycle 6 as issue 1d. The team did not address it this cycle, and I see no evidence it was even considered. `tilt = int(s * 0.20)` still produces an 11-pixel body-top shift at Byte's scale. The extended right arm (arm_point_len = `int(s * 0.80)`) is the significant differentiator — at `s ≈ 56px`, that arm is 45 pixels long, which is the full width of Byte's body.

At thumbnail scale, you have a teal rectangle with a stick extending to the right. That is Byte pointing. It reads, but barely. The differentiation from neutral (rectangle, two stubs) is minimal. This is a character whose body language needs to compensate for the absence of a readable face at small scale. An arm extension does not compensate for zero body language. Byte's action pose still communicates urgency only at close range.

**This was Priority 3 in my Cycle 6 report. It should have been done. It was not.**

---

### 2c. BYTE EXPRESSIONS — Hover particle confetti still 4x4px

Issue 3d from Cycle 6 remains completely unaddressed. The confetti particles at `draw.rectangle([px, py, px+4, py+4], ...)` are still 4×4 pixels in a 240×320 panel. At normal viewing distance, they are invisible noise. At close range, they are pixel artifacts. Either enlarge them to 10×10 minimum or remove them. This was Priority 3 in Cycle 6 and it is still sitting there, unchanged. I do not understand why it was skipped — it is a two-number change. If the team is making conscious decisions about which items to defer, those decisions need to be documented in the work record, not silently omitted.

---

### 2d. BYTE EXPRESSIONS — GRUMPY body posture is still passive-lean

Issue 3b from Cycle 6 was the body tilt direction conflict for GRUMPY. The Cycle 7 code shows `body_tilt: -4` (changed from `+6`), and `arm_dy: -2` with `arm_l_dy: -2, arm_r_dy: -2`. The tilt has been reversed and reduced in magnitude. The arms have been raised slightly (from `arm_dy=10` to `arm_dy=-2`).

The result is a very slight leftward lean (-4px) with arms barely above neutral. This is marginally less defeated than the Cycle 6 version, but it still does not communicate grumpiness through the body. At `body_tilt=-4` the lean is negligible — it will read as upright. At `arm_dy=-2`, the arms are almost at neutral height. GRUMPY's body says "standing." It does not say "grumpy."

For comparison: CONFUSED has `body_tilt=-18` and ALARMED has `arm_dy=-16` (arms flung high). GRUMPY has `-4` and `-2`. These numbers are whispering. The body language should be shouting. A genuinely grumpy character needs either: squared-up confrontational (body_tilt=0, arms crossed or at -8 to -10 with reduced arm_x_scale suggesting crossed-arm energy), or aggressive forward lean (body_tilt=-12 to -15, arm_dy=-6 to -8 suggesting a "what do you want" posture). The current numbers feel like someone got cold feet mid-commit.

---

### 2e. LUMA EXPRESSION SHEET — Background color improvement is real but still timid

The backgrounds have been meaningfully improved compared to Cycle 6:
- Excitement: `(248, 238, 220)` — warm amber
- Worry: `(195, 212, 228)` — cool blue-grey
- Mischief: `(220, 205, 242)` — lavender

The Worry background is now genuinely cool — a meaningful change from the previous near-neutral. The Mischief background is a committed lavender rather than a whisper of purple. Credit is due.

However, at the scale these panels print on a pitch deck page (three panels side by side at approximately 3.5 inches wide each, on an 11x8.5 inch page), these backgrounds must read as distinct emotional environments from 8 feet away. My test: close one eye, squint at the three panels until the face details blur out. Can you still tell the three backgrounds apart? Almost. The blue-grey reads. The lavender reads. The warm amber might read as "lighter" compared to the others, but whether it reads as "warm/exciting" vs. "white" is uncertain at distance.

The Excitement panel needs more commitment. `(248, 238, 220)` is a light sand colour — warm, yes, but potentially reading as off-white. `(255, 210, 150)` or similar warm amber mid-tone would separate it from "neutral background" at pitch distance. Half a commit is still half a commit.

---

### 2f. LUMA EXPRESSION SHEET — Worried/Determined corrugator kink is present but subtle

The corrugator kink is now in the code:
```python
l_brow_pts = [(lex - 28, ley-30), (lex + 5, ley-24), (lex + 20, ley-20), (lex + 26, ley-24)]
```
The inner tip at `(lex + 26, ley-24)` kicks upward from `(lex + 20, ley-20)` by 4 pixels. This is anatomically correct for the corrugator muscle read. I will give credit: the dual emotion — Worried AND Determined — is now present in the brow geometry. This is a better expression than Cycle 6.

The issue is that 4 pixels of upward kick at this scale, with a 6px-wide brow line, is subtle enough to require close attention to notice. For a pitch expression sheet — where this face needs to communicate a dual emotional state to someone reading it for the first time — the kink should be more pronounced. The inner tip kick should be 7–8 pixels upward, not 4, so it registers without the viewer needing to already know what they're looking for. The read is there, but it is murmuring instead of speaking.

---

## SECTION 3: OVERARCHING DESIGN SYSTEM CONCERNS — ESCALATING PRIORITY

### 3a. Miri remains the weakest character in the package — and it is getting urgent

This is the third consecutive cycle I am writing this. Miri's design is a wide rectangle with a round head and a rectangular bag. Everything about her visual language says "generic placeholder character who has not received a design pass." Compare to every other character:

- **Luma**: A-line hoodie, chunky sneakers, cloud of curly hair, pocket bump, a dozen visual hooks telling you "chaotic kinetic energy."
- **Cosmo**: Rectangular narrow head, white-cutout glasses, notebook under arm, slender vertical proportions. Design language: "methodical, organized, slightly out of step with the physical world."
- **Byte**: Teal cube, cracked pixel eye, magenta scar markings, chunky proportions. Design language: "malfunctioning, resilient, visually alien."
- **Miri**: Rectangle body, circle head, rectangle bag. Design language: "character design is incomplete."

The bag tells us she carries things. It does not tell us who she is, what she wants, how she moves through the world, or what role she plays in the team dynamic. For a pitch package, this is the most damaging omission in the entire body of work. A buyer looking at the character lineup sees three fully-realized characters and one who looks like she was added to complete a roster minimum. That impression is impossible to unsee.

**Miri needs a design pass that gives her a personality-driven visual hook. This is not optional if this package is to be pitch-ready. It is Priority 0 for Cycle 8.**

---

### 3b. No composite reference image still — three cycles running

I requested a composite reference image showing all four characters at correct relative scale with faces visible in Cycle 6. The contact sheet and storyboard show scale relationships. The expression sheets isolate faces. Nothing in the package puts all four characters at correct proportional scale with legible faces simultaneously.

A pitch buyer needs to understand: "What does this world look like when all four characters are in the same frame?" Currently they cannot answer that question from the deliverables. The `contact_sheet_generator.py` tool exists. The character data exists. A composite reference page is achievable in one focused work session.

---

### 3c. Production verification gap — improved but not closed

The SoW for Cycle 7 lists the outputs and describes what was changed. It does not confirm that each generator was run, the output was opened, the output was visually reviewed, and the specific fix was confirmed to appear in the rendered image. This distinction matters enormously. The Cycle 6 canvas clipping bug was a coding error that would have been caught in 15 seconds if anyone had opened the PNG and looked at it. The Cycle 7 fixes appear to be correct in code — but "correct in code" and "correct in output" remain two different things until someone verifies the render.

For Cycle 8, the SoW should include a verification line for each output: "Generated, opened, visually confirmed [specific element]." Not a description of code changes. Evidence that the rendered output was examined.

---

## PRIORITY REQUIREMENTS FOR CYCLE 8

**Priority 0 — Character Design:**
1. **Miri full design pass.** She needs at minimum one personality-driven visual hook beyond the bag. Suggestions: a distinctive hairstyle that communicates her character function; a clothing detail that implies her role; a physical proportion choice (rounded vs. angular, settled vs. kinetic) that differentiates her from a generic placeholder. The bag stays — it is functional — but it is not a character design.

**Priority 1 — Must Fix:**
2. Miri's right arm in the action pose: redesign so the arm-body-bag visual relationship is legible at squint distance without requiring anatomical inference. Either show the strap connecting arm to bag, or show the full arm contour.
3. GRUMPY body posture: commit to a body language reading. Either squared-up confrontational or aggressive forward lean. The current -4/–2 values communicate "standing near neutral." They should be communicating disgust and confrontation.
4. Luma Worried/Determined corrugator kink: increase inner brow kick from 4px to 7-8px so the Worried component registers at pitch-deck viewing distance.
5. Excitement background: increase temperature commitment from `(248, 238, 220)` to a warmer mid-tone that reads as "warm/amber" not "off-white" at squint distance.

**Priority 2 — Design Integrity:**
6. Byte action pose: give Byte a more dramatic physical gesture. The extended-arm point is the right instinct but insufficient. Add a leg stance change, a body-height change (crouch or stretch), or a head lean that combined with the arm creates a whole-body dynamic read.
7. Produce the composite reference image showing all four characters at correct relative scale with legible face detail. This is now three cycles overdue.

**Priority 3 — Polish:**
8. Hover particle confetti: enlarge to 10×10px minimum, or remove. This item has been on the list for two cycles. It takes thirty seconds to fix.
9. GRUMPY pixel symbol: consider whether the scowl-rectangle reads clearly as disgust or whether a more asymmetric / expressively animated pattern would be stronger.

---

## CYCLE 7 GRADE ASSESSMENT

**Grade: B**

The grade rises from B- to B. Here is why:

All four Priority 1 items from Cycle 6 are resolved. The fixes are competent: NEUTRAL_BASE=380 is correctly calculated, the dead canvas is gone, the GRUMPY eye has a proper pixel symbol, the smirk geometry is repaired with a polygon rather than a chord. These were genuine technical corrections that required understanding the bugs, not just patching symptoms.

The Luma worried/determined expression is meaningfully improved — the corrugator kink changes the read from "pure determined" to a genuine dual emotion, even if the effect is subtle. The background color separation is improved. The GRUMPY body posture change (tilt reversed) shows the team understood the Cycle 6 note even if the execution was tentative.

The B ceiling is set by: (1) Miri remaining an incomplete character design for the third consecutive cycle — this is the single most damaging unresolved issue in the package; (2) multiple Cycle 6 Priority 3 items carried forward without address or documented deferral; (3) the ongoing absence of a composite reference image that would function as the anchor document for the entire pitch package.

The team is producing increasingly solid individual deliverables. The package as a whole is not yet integrated. A collection of individually-improved sheets is not a pitch package. A pitch package is a set of documents that together answer the question: "What is this show, who are these characters, and can this team produce it?" The answer to the first two questions is getting clearer. The answer to the third requires demonstrating end-to-end production coherence — and Miri, right now, is evidence that the team can polish individual elements while leaving a foundational design gap open.

A B grade says: the craft is improving and the discipline to act on critique is real. The creative ambition to take Miri from placeholder to character is what this cycle needed and did not deliver.

---

*"A character who has no design language is not a character. She is a body count."*

*Dmitri Volkov — Character Design Critic*
*"Run the generator. Open the file. Look at it. Then close the ticket."*
