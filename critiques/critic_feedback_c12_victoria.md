# Critique — Cycle 12
**Critic:** Victoria Ashford, Visual Development Consultant
**Specialty:** Overall visual coherence, storytelling through visuals, cinematic composition
**Date:** 2026-03-30
**Subject:** Style Frame 01 v002 (Ghost Byte) + Asymmetric Logo — *Luma & the Glitchkin*

---

## OPENING STATEMENT

In Cycle 11 I awarded an A and specified two A+ gaps: a visual surprise element in Style Frame 01, and an asymmetric logo layout. The Statement of Work for Cycle 12 claims both delivered. I will now examine each against the rendered output and the generating code with the same rigor I have applied for twelve cycles.

I have looked at both images. I have read both generators in full. My findings follow.

---

## ASSESSMENT 1 — GHOST BYTE CONCEPT (Style Frame 01 v002)

### The Concept

The implemented surprise is a ghost Byte silhouette on three peripheral monitors — top-left, top-right, and mid-right — while the main CRT shows Byte emerging in full. The intended narrative read: Byte has been watching Luma through every screen before choosing to reveal itself. "A girl discovering something digital" becomes "something digital that has been waiting for her."

This is the right kind of idea. It earns its place as an A+ candidate. It adds a story layer that was not in the original brief, it does not overwrite any existing element, and it respects the viewing hierarchy — the main emergence point is still the dominant read, which is correct.

The concept alone is not sufficient for A+. What matters is whether it executes.

### Viewing the Rendered Output

I examined `LTG_COLOR_styleframe_discovery.png` at full resolution.

**What I can confirm is working:**

The ghost oval forms are present on the peripheral monitors. At full resolution, the top-right and mid-right monitors do show a faint oval form with two bright-point eye glints. The story beat — Byte's silhouette watching from adjacent screens — is perceptible on careful second-look inspection. The eye glints at alpha 60–70 over the ghost body's alpha 55 create the correct hierarchy within the ghost form itself: you read the form first, then notice the eyes inside it, which is exactly the right order.

The color choice is intelligent. The ghost body at `(0, 53, 58, 55)` — approximately 23% of BYTE_TEAL — reads as a dark pressure against the cyan screen field rather than a drawing on top of it. It is, correctly, an absence that has a shape rather than a presence. That is how a ghost should work.

**What is failing:**

The top-left monitor ghost is not legible in the rendered image at any reasonable viewing condition. Looking at the full-resolution PNG, the warm amber glow from the lamp zone bleeds into the left portion of the monitor wall, which reduces the contrast between the dark ghost form `(0, 53, 58)` and the screen background in that region. The top-left monitor sits in the warm overlap zone where the amber light is at its most diffuse. At alpha 55, the ghost form on that screen has insufficient contrast to read. One of the three ghost instances does not land.

More fundamentally: the monitors themselves in the rendered frame are relatively small. At the composition's full 1920×1080 scale, the peripheral monitors occupy roughly 120×90px each. At those dimensions, `g_rx = int(gs_mw * 0.28)` yields approximately 34px radius horizontally, and `g_ry = int(gs_mh * 0.38)` approximately 34px vertical — a ghost oval that spans perhaps 68×68px on a 120×90px screen. That is a reasonable proportion. But the code also allocates `e_r = max(2, int(g_rx * 0.20))` for eye radius, which works out to approximately 6–7px per eye glint. At a standard pitch deck presentation size — a 1920×1080 frame shown on a projector or displayed in a deck at maybe 800–1000px wide — these eye glints will reduce to 2–3px. That is below the threshold of intentionality. At slide size they read as render noise, not as eyes.

**The calibration problem:**

The ghost is calibrated for full-resolution careful inspection. That is one valid context — a developer looking closely at a pitch asset, or a reviewer reading the art file. It is not the primary context. The primary context for a pitch frame is: displayed on a projector at 16:9 at approximately 1/3 actual pixel density, viewed from 8–15 feet away, by an executive whose attention you have for perhaps 4–6 seconds per slide. Under those conditions, the ghost Byte silhouettes on the peripheral monitors are invisible.

This is the central failure of the execution. The concept asks for "subtle enough to reward the careful viewer, not obvious on first glance." That is correct. But there is a third condition that the implementation missed: it must be legible under pitch conditions, not just under close inspection. "Subtle" does not mean "invisible at normal viewing size." A surprise element that requires a magnifying glass is not a surprise — it is a secret the audience never discovers.

**What does work at pitch conditions:**

The main CRT with Byte emerging works at any scale. The warm/cold split is visible at thumbnail size. Luma's posture — leaning in, one arm extended — reads at any scale. The ghost Bytes do not.

### Ghost Byte Verdict

The concept is correct. The implementation is set to the wrong threshold. The ghost forms are visible at full resolution under careful inspection and invisible at pitch conditions. For the surprise element to work as designed — rewarding the careful viewer without announcing itself to the casual one — the ghost needs to be calibrated to "visible but deniable at 800px wide" rather than "barely perceptible at 1920px wide."

Specifically: the ghost body alpha needs to rise from 55 to approximately 80–100, the eye glints need to rise from 60–70 to 90–120, and the top-left monitor ghost should be relocated to a mid or right-side monitor that sits in the cold monitor zone where there is no warm light contamination. Three ghosts may be one too many — two strong ghosts land better than three where one is lost.

**Grade for ghost Byte execution: B+**

The concept earns full marks. The calibration earns a B. The top-left ghost failure earns a minus. Overall: B+. This is not A+. It is close. One revision pass with adjusted alpha values and strategic monitor selection would get it there.

---

## ASSESSMENT 2 — ASYMMETRIC LOGO LAYOUT

### What Was Requested

Cycle 11 A+ P2: Luma larger and left-anchored, "& the Glitchkin" smaller and stacked right, glitch treatment as visual counterweight. Balance through contrast, not symmetry.

### Reviewing the Rendered Output

I examined `LTG_BRAND_logo_asymmetric.png` at full resolution.

**What is working:**

The compositional hierarchy is correct and immediately readable. "Luma" at 180pt is dominant left; "& the Glitchkin" stacks right at smaller scale. The warm amber zone on the left against the cold cyan zone on the right maps the show's color language directly onto the brand mark. The left–right thermal division with warm corner accents on the left two corners and cold accents on the right two is a clean, purposeful touch — it extends the frame's visual logic into the identity system without overcomplicating it.

The background glow work is strong. The large amber halo behind "Luma" and the concentrated cyan glow behind the stacked Glitchkin text give each element a presence that extends beyond its letterforms. The warm/cold boundary at roughly 50% canvas width with the 1px deep cyan divider at 25 alpha is the correct level of restraint — it articulates the division without making it a diagram.

The bi-color pixel noise bar at the bottom — warm amber on the left half, deep cyan on the right, with the pixel scatter bridging the seam — is a small detail that pays off the design. It feels designed, not decorated.

**What is not working:**

The "&" connector is doing too little. At 56pt in WARM_CREAM with a dark shadow, it sits in the middle section but does not actively mediate the transition. It reads as punctuation that happens to be there. The "&" is the hinge of the composition — "Luma" and "the Glitchkin" are two worlds, and the "&" is the connection between them. At current size and color, it is a neutral mark. It needs either more visual character (a slight glitch treatment suggesting it lives in both worlds simultaneously) or better color handling — a gradient or split treatment where the warm side of the glyph is amber and the cold side is cyan, making the "&" the literal crossing point.

The stacking of "the" and "Glitchkin" is correct in principle but the execution has a gap I need to name. "the" at 38pt in ELEC_CYAN reads fine as a small label. But the vertical gap between "the" and "Glitchkin" at 4% of canvas height is slightly generous — it creates a mild disconnection between the two lines of the stack. They read as two separate elements sitting near each other rather than one unit. Tighten the inter-line gap by approximately half and they will read as a proper vertical lockup.

The "Glitchkin" glitch treatment — chromatic aberration, pixel scatter at count 60, horizontal slice displacement — is the visual counterweight the brief called for. It delivers. The electric cyan primary with magenta ghost and UV purple diagonal reads as controlled digital chaos. It does not compete with "Luma" — it energizes the right half of the frame with a different kind of weight. This is the core asymmetric logic working correctly.

**The typeface constraint, again:**

I noted in Cycle 11 that DejaVu Sans Bold is the single largest remaining gap between current output and professional pitch standard. That gap is more visible in the asymmetric layout than in the symmetric one. When "Luma" is at 180pt occupying the dominant left half of a 1200×480 canvas, the letterforms are the hero. At that scale, DejaVu Sans Bold is a system font doing its best to be a display typeface. The l–u–m–a letterforms are serviceable. They are not distinctive. A pitch room will see them at exactly this size and will register, perhaps unconsciously, that this is a tool-generated title rather than a designed one. The glitch treatments, the glow, the color system — all of it works. The underlying letterform at 180pt undermines it.

I am not changing the grade on this basis — the tool constraint is documented and accepted. But I want the team to understand that the asymmetric layout, by enlarging "Luma" to dominant size, has made the typeface problem more visible, not less. This is not an argument against the asymmetric layout. It is an argument for treating the typeface replacement as a higher priority than it has been.

**Asymmetric Logo Verdict**

The compositional concept is correct and well-executed. The warm/cold division, the size hierarchy, the glitch counterweight, the background zone structure — these all deliver on the brief. Two specific fixes needed: the "&" connector needs active treatment to function as a narrative hinge rather than punctuation, and the "the/Glitchkin" inter-line gap should tighten. These are refinements, not structural problems.

**Grade for asymmetric logo: A-**

The concept arrives. The two specific details above are the gap between A- and A.

---

## OVERALL PACKAGE STATUS — CYCLE 12

Having reviewed the two Cycle 12 deliverables alongside the complete pitch package index, I am now reviewing the overall package completeness for pitch readiness.

**What is pitch-ready:**

- Character design sheets, turnarounds, color models, lineup — complete and accepted across the board
- Storyboard cold open — all 25 panels delivered and accepted
- Style guide — 11 sections, complete
- Production bible — accepted
- Environment designs — all three environments documented with compositing-ready BG frames
- Color palette and color keys — complete
- Show logo (symmetric, v001) — accepted

**What remains incomplete:**

Style Frame 02 (Glitch Storm) has a BG delivered in Cycle 12 but no composite pass yet. This is a material gap. A three-frame style package with two frames finalized and one sitting at BG-only is not a three-frame package. The Glitch Storm frame is the show's most dramatic visual premise — the night sky splitting open, the town in shadow, Luma and Cosmo and Byte small against the scale of it. That frame, properly composited, would be the pitch deck's second strongest image. It has been "pending compositing by Sam Kowalski" for one full cycle. That work must happen before external pitch use.

Style Frame 03 (Other Side) has no BG and no composite. At this stage of the package I am not holding the pitch hostage to Frame 03 — the cold open storyboard covers the narrative territory and Frame 01 is the hero. But a three-frame target that ends the cycle at 1.5/3 completed is worth naming plainly.

The logo tagline placeholder: resolved. The Byte version header: resolved. Both noted and confirmed.

The LTG naming compliance pass — numerous legacy files still carry non-compliant names despite a compliance tool now existing. The naming conventions document is not itself LTG-named, which the index has flagged three cycles running. This is an internal discipline issue, not a pitch-blocking issue. It remains untidy.

The cold overlay arithmetic flag from Naomi Bridges (Cycle 10) remains open. I reviewed the corrected arithmetic in Cycle 10 and my opinion is that the visual decision to retain cold_alpha_max=60 is correct — the 12% cold cyan cross-light reads as a plausible three-light transition, not a contamination. The flag should be formally closed with a notation that the arithmetic was recalculated, the visual result was re-evaluated, and the original value was retained by design decision. Leaving it open as a paperwork item is unnecessary.

---

## PRIORITY PUNCH LIST — CYCLE 13

| Priority | Item | What Is Needed |
|----------|------|----------------|
| **P0** | Style Frame 02 composite | Sam Kowalski must complete the character composite pass over Jordan Reed's BG. This is blocking a complete three-frame pitch package. No further deferral. |
| **P1** | Ghost Byte alpha calibration | Raise ghost body alpha from 55 to 80–100. Raise eye glint alpha from 60–70 to 90–120. Relocate the top-left monitor ghost to a mid or right monitor (warm-zone contamination kills it where it currently sits). Optionally reduce from three instances to two strong instances. The concept is right; the calibration is wrong. |
| **P2** | "&" connector treatment | The "&" in the asymmetric logo needs active visual treatment — a warm-to-cold gradient, a split color treatment, or a subtle glitch pass — to function as a narrative hinge between the two characters' worlds. Currently it is punctuation. It should be a character in its own right. |
| **P3** | "the/Glitchkin" inter-line gap | Reduce the vertical gap between "the" and "Glitchkin" in the stacked lockup by approximately half. They need to read as one unit. |
| **NOTE** | Naomi Bridges cold overlay flag | Close this formally. The arithmetic was verified correct. The design decision to retain the value was made and documented. The open flag is a bookkeeping item, not a production issue. |
| **NOTE** | Typeface | When an open-source or licensed display typeface becomes available for "Luma," it should be the first substitution made to the logo generator. The asymmetric layout at 180pt has raised the visibility of this gap. This is not Cycle 13 blocking but it is the single largest remaining distance between this package and professional pitch standard. |

---

## GRADES — CYCLE 12

| Deliverable | Grade | Reasoning |
|-------------|-------|-----------|
| Ghost Byte concept | A | The right idea, correctly motivated, correctly placed in the narrative logic of the frame |
| Ghost Byte execution | B+ | Alpha calibration set to wrong threshold; top-left instance lost to warm contamination |
| Style Frame 01 v002 (combined) | B+ | Concept earns A, execution earns B+. Cannot award A+ on concept alone. |
| Asymmetric logo composition | A | Hierarchy, counterweight, background zones, glitch treatment — all correct |
| Asymmetric logo detail | B+ | "&" connector and "the/Glitchkin" gap are two specific, fixable deficits |
| Asymmetric logo overall | **A-** | One revision pass from A |
| Overall package readiness | **A-** | The package is pitch-capable at its current state if Frame 02 is composited. Without Frame 02, it is A- material presenting as incomplete. |

---

## CLOSING ASSESSMENT

The team is close. Genuinely close. The distance between where this package sits now and A+ is not a structural rebuild — it is two calibration decisions (ghost alpha, "&" connector) and one outstanding composite (Frame 02). Those are revision-scale tasks, not new work.

The ghost Byte concept is the most encouraging development in several cycles. The team found an idea that adds story without removing anything, uses the visual system the frame already has, and rewards attention. That is design intelligence, not just execution. The calibration failure is a technical problem with a one-line fix. Fix the alpha values, relocate the warm-zone ghost, and the surprise element will land as intended.

The asymmetric logo delivers the composition I asked for. The "&" note is the one thing I will not let go of: in a show called "Luma & the Glitchkin," the "&" is the show's premise in a single character. Make it count.

If Frame 02 is composited in Cycle 13 and the two specific logo fixes are made, I will re-evaluate for A+. The ghost Byte alpha revision is required for any A+ conversation on the style frame. I am not moving the goalpost. I am telling the team exactly where the goalpost is.

---

*Victoria Ashford*
*Visual Development Consultant — 30 years industry experience*
*Cycle 12 Review — 2026-03-30*
