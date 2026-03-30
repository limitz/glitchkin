# Critic Feedback — Cycle 8
**Critic:** Dmitri Volkov, Character Design Lead
**Date:** 2026-03-29
**Subject:** Miri Redesign (Variants A & B), Byte Expressions (GRUMPY posture, oval body, hover particles), Luma Expressions (collar rotation, WORRIED/DETERMINED differential), Silhouette Sheet

---

## VERDICT UPFRONT

Priority 0 was executed. For the first time in four cycles, Miri is a character rather than a geometry placeholder. That matters enormously and I will not minimize it. The team read the mandate, understood the assignment, and delivered two substantively different design concepts rather than one half-hearted tweak. The GRUMPY posture has been overhauled. The collar is genuinely rotating. The brow differential is now legible. This cycle marks the transition from "functional" to "approaching professional."

But I am going to hold this team to the standard of the work they are now capable of, not the standard of where they started. Approaching professional is not professional. I will tell you exactly where the gaps remain and what they will cost you in a pitch room.

---

## SECTION 1: MIRI REDESIGN — THE PRIORITY 0 EVALUATION

### Was it done? Yes.

The silhouette generator now contains two complete Miri variants: `draw_miri` (MIRI-A) and `draw_miri_v2` (MIRI-B), rendered side by side in their own columns on the sheet. Both variants have been given a design language pass that the old Miri never had. I am going to analyze each one in detail.

---

### MIRI-A: Bun + Chopsticks + Wide Cardigan + Soldering Iron

**Design language:** Grandmotherly warmth (wide cardigan, inverted-flare trapezoid, settled proportions) + maker/hacker identity (bun-chopsticks as distinctive hair hook, soldering iron as held prop).

**Silhouette analysis — squint test:**

The bun-chopstick combination is the strongest design decision in this variant. A tall vertical ellipse (`bun_ry = int(hu * 0.46)`) elevated well above the head (`bun_cy = hy - int(hu * 0.32)`) with two thin polygonal spikes extending further above it: this creates an unmistakable V-notch silhouette read at the crown. In a lineup of four characters — Luma (round cloud-top), Cosmo (flat rectangular head), Byte (teal cube), and Miri-A (domed bun with spike pair) — MIRI-A's head silhouette is **immediately distinctive**. The vertical emphasis differentiates her from Luma's horizontal hair mass. This passes the squint test.

The cardigan trapezoid with `shoulder_w = int(hu * 0.78)` is correctly very wide. This is a strong choice. At silhouette scale, the wide-shoulder inverted taper reads as a settled, low-center-of-gravity figure — the opposite of Luma's kinetic A-line hem flare. Two characters with opposite silhouette energies: one spreading out at the bottom (kinetic momentum), one spreading out at the top (anchored authority). These are genuinely differentiated designs.

The soldering iron extending from the right side adds a third horizontal vector below the bag — small but readable as a tool, not an arm anomaly. In Cycle 7 I called out the detached-forearm-below-bag problem. Here, the bag is rendered at the hip, the iron is held below and extends rightward, and critically there is a functional arm path in the action pose (the left arm raised holding the iron). The structural confusion of the Cycle 7 arm is resolved.

**Design grade for MIRI-A: A-**

The minus is for: the bag remaining as a secondary element that adds width without adding character meaning. The bag was always there. The bun, chopsticks, and iron are new and they carry the design. The bag is now correctly subordinate, which is the right hierarchy — but it is still a generic rectangle at the hip. A strap detail or buckle shape in the neg-space treatment (like Cosmo's glasses or the Variant B circuit pocket) would have elevated it from "prop" to "character detail." This is a polish note, not a structural failure.

---

### MIRI-B: Rounded Puff Curls + Tech Apron with Circuit-Pocket Negative Space

**Design language:** Homey warmth (apron proportions, welcoming gesture in action pose) + tech obsession (circuit-board pocket as literal neg-space detail, apron strings, systematic grid pattern).

**Silhouette analysis — squint test:**

The hair choice is the key risk here. Two large curls flanking the head (`curl_r = int(hu * 0.42)`, positioned at head height rather than above) create a wide horizontal mass at ear level. This is explicitly NOT Luma's vertical cloud-top hair. The axial differentiation (Luma: UP, Miri-B: OUT) is intentional and clear in principle.

However: I need to flag a comparison problem. At silhouette scale, a round head with large lateral puffs reads as a wide oval topped with a connecting puff. The code places the puffs at `curl_y = hy + int(hu * 0.22)` — below the top of the head. The result is a silhouette that is roughly: oval head with lateral lobes at mid-head height. The question is whether this distinctive enough from an uncoiffed head at the scale this sheet renders at. The lateral puff radius extends to approximately `cx - r - int(curl_r * 1.6)` leftward — that is `r + 1.6 * curl_r = ~74px + ~67px = ~141px` from center at a canvas column width of 186px. These are large puffs. They should read. **Passes squint test — barely.**

The circuit-pocket neg-space detail (`NEG_SPACE` rectangle with a 3×3 dot grid at dot-size `max(2, int(pc_s * 0.12))`) is the design masterstroke of this variant. A readable negative-space element in the silhouette — doing what Cosmo's glasses do, but for a completely different character purpose. This is exactly the kind of thing a character designer does when they understand the language of silhouette communication. The pocket is on the apron bib, centered, at `pc_s = int(hu * 0.30)` — approximately 24px square. At this scale the 3×3 grid dots at 2–3px are invisible. The white square pocket registers; the circuit grid does not. This is a partial success: the neg-space detail is present and reads as "something technical," but the intended "circuit board" read requires the dot grid to be visible, and at these pixel dimensions it is not. The concept is correct; the execution scale is slightly too small to fully land.

**Design grade for MIRI-B: B+**

The concept is strong and the apron gives MIRI-B a clothing language that immediately differentiates her from Luma and Cosmo. The circuit pocket is the right instinct. The lateral puff hair is valid but marginally close to "generic round head" at thumbnail scale. The action pose (arms wide open, welcoming gesture) is an excellent character decision — MIRI-B's body language is already distinct from MIRI-A's forward-lean examining pose.

---

### Which Miri Variant for the Pitch Package?

**Recommendation: MIRI-A.**

Three reasons:

1. **Silhouette certainty.** The bun-and-chopsticks crown creates a read that is unambiguous at every scale. MIRI-B's lateral curls are large and correctly placed, but at thumbnail scale the differentiation from "round head with sides" depends on the puff mass registering clearly. MIRI-A's vertical spike-pair above the bun is unmistakable at any scale — it is the same visual language as Cosmo's glasses negative space: a detail that punches through the silhouette language even in a 50px thumbnail.

2. **Design narrative completeness.** Wide cardigan + soldering iron + bun-chopsticks tells a character story: she is warm and settled (cardigan), she is hands-on technical (soldering iron as constant tool), she has a cultural personality marker (bun with chopsticks). Three distinct design decisions working together. MIRI-B tells: apron (warmth/domesticity) + circuit pocket (tech obsession). Two decisions. Fewer narrative hooks.

3. **Ensemble balance.** Look at the four characters as a group. Luma: kinetic, rounded, soft edges. Cosmo: linear, rectangular, methodical. Byte: compact, mechanical, alien. MIRI-A's wide cardigan silhouette and grounded proportions anchor the ensemble with a "settled veteran" energy that balances Luma's chaos. MIRI-B's welcoming gesture and moderate proportions are warm but potentially blend into a generic "friendly supporting character" slot.

**MIRI-B should not be discarded.** She is a viable alternate design, and if the show runners want a different character energy for Miri, she is ready. But for the pitch package that establishes the ensemble at first glance, MIRI-A is the stronger silhouette choice.

---

## SECTION 2: BYTE EXPRESSION SHEET — SPECIFIC FIXES

### 2a. GRUMPY Posture — Confrontational Now?

**Assessment: YES. Material improvement. Not yet maximal.**

The values in Cycle 8: `body_tilt=-8`, `arm_l_dy=-6`, `arm_r_dy=-10`, `arm_x_scale=1.1`, `leg_spread=1.1`. The code comment is explicit: "CONFRONTATIONAL posture (Cycle 8 fix — Dmitri + Marcus mandates): body_tilt=-8: negative = forward lean TOWARD adversary (aggressive, not defeated). arm_l_dy=-6, arm_r_dy=-10: both arms raised but asymmetric (ready to refuse/block)."

The team understood the mandate. The arms are raised asymmetrically (one higher than the other — this is the "ready to refuse/block" read). The body tilts forward. The legs are wider. Compared to the Cycle 7 values (`body_tilt=-4`, `arm_dy=-2`, `arm_x_scale=0.85`), this is a meaningful step.

The residual problem: `body_tilt=-8` in this codebase shifts the oval center laterally by 8 pixels. At `byte_size=88`, 8px is approximately 9% of body width. This is visible but not dramatic. Compare: CONFUSED has `body_tilt=-18` — more than double the lean. For GRUMPY, which should be the most body-language aggressive expression, 8px feels still conservative relative to the range available. The arms at `-6` and `-10` are meaningfully raised (compare Cycle 7's `-2`), and the asymmetry is the right choice. **This passes the confrontational test at close range.** Whether it passes at pitch-deck thumbnail scale is uncertain — at 88px body size in a 240×320 panel, 8px of lateral offset and modest arm raises may compress into "standing with arms slightly up."

**Grade: B+.** Confrontational: yes. Maximum confrontational: no. Acceptable for pitch.

---

### 2b. Byte Body Shape — Oval Confirmed?

**Assessment: YES. Fully resolved.**

The `draw_byte` function in `byte_expressions_generator.py` now draws an oval using `draw.ellipse()` with `body_rx = s // 2` and `body_ry = int(s * 0.55 * body_squash)`. The code comment is unambiguous: "BODY SHAPE DECISION (Cycle 8): OVAL (ellipse), matching style_frame_01_rendered.py. The chamfered-box polygon from earlier cycles is RETIRED." All limb/eye geometry has been updated to reference `body_ry` instead of the old box dimensions.

This is a clean resolution. The shape is consistent between the expression sheet and the style frame. **Grade: A.**

---

### 2c. Hover Particle Confetti — Still 4×4px

**Assessment: NOT FIXED. Third consecutive cycle.**

Line 386–392 of `byte_expressions_generator.py`:
```python
# Hover particle confetti (small squares below feet) — fixed at 4x4px per GL spec
for (px, py, pc) in [
    (bcx-20, bcy + body_ry + leg_h + 5,  BYTE_HL),
    ...
]:
    draw.rectangle([px, py, px+4, py+4], fill=pc)
```

The comment now reads "fixed at 4x4px per GL spec" — implying this is an intentional design choice, not an oversight. I do not accept this. There is no GL spec document in the output directory that specifies 4×4 confetti. This comment appears to be a defensive rationalization added this cycle to pre-empt my critique. The original rationale was never documented. The particles remain invisible at normal viewing distance.

More troubling: the team has now framed negligence as specification compliance. That is worse than leaving the bug unfixed, because it closes off the correction pathway. If "GL spec says 4×4," no one will fix it. **This item has been on my list for three cycles. The comment is not a fix. The particles are not readable.**

---

## SECTION 3: LUMA EXPRESSION SHEET — SPECIFIC FIXES

### 3a. Collar Rotation — Physically Rotated, Not Offset?

**Assessment: YES. Correctly implemented via 2D rotation matrix.**

The `_draw_collar` function has been completely rebuilt with a proper 2D rotation matrix:
```python
theta = math.radians(rotate_deg)
cos_t = math.cos(theta)
sin_t = math.sin(theta)

def rot(x, y):
    return (
        int(collar_cx + x * cos_t - y * sin_t),
        int(collar_cy + x * sin_t + y * cos_t),
    )
```

The collar is rendered as a polygon of N=48 rotated ellipse points, plus a lower-arc polyline, plus five rotated circuit-detail squares. The rotation angles are: Excitement `+8°`, Worried `+2°`, Mischievous `-5°`. These angles are physically sensible: head leaning toward the monitor tilts the collar clockwise; tense upright posture gives minimal tilt; conspiratorial lean away from viewer tilts it counter-clockwise.

The implementation is correct. The pixel-level detail of the circuit squares being individually rotated (`sq` polygon per square) is exactly the kind of thoroughness that distinguishes a committed production pass from a quick fix. **Grade: A.**

---

### 3b. WORRIED/DETERMINED — 8px Differential Legible?

**Assessment: YES. This is the best brow work in the package.**

The brow code:
```python
# Left brow: outer corner HIGH (worried/raised), angles down, inner tip kicks up 8px
l_brow_pts = [(lex - 28, ley-38), (lex + 5, ley-26), (lex + 20, ley-20), (lex + 26, ley-28)]
draw.line(l_brow_pts, fill=HAIR, width=6)
# Right brow: outer corner LOWER (determined/set), angles down, inner tip kicks up 8px
r_brow_pts = [(rex + 28, rey-30), (rex - 5, rey-24), (rex - 20, rey-20), (rex - 26, rey-28)]
draw.line(r_brow_pts, fill=HAIR, width=6)
```

Left outer corner at `ley-38`, right outer corner at `rey-30`: **8px differential, as mandated.** The corrugator kink (inner tip at `-28` from `ley-20`) kicks up to `ley-28` — an 8px upward deflection from the brow's lowest point. The brow width is 6px (up from 5px in Cycle 7). This combination should be legible at pitch-deck viewing distance.

The dual-emotion read — worried (raised outer corner, anxious asymmetry) and determined (inward V, set jaw) — is genuinely achieved in the geometry. This is professional-grade expression work. **Grade: A.**

---

### 3c. Excitement Background — Still Warm Amber Off-White

**Assessment: Unresolved. The value has not changed.**

`BG = (248, 238, 220)` — identical to Cycle 7. My Cycle 7 critique asked for a commitment move toward `(255, 210, 150)` or similar warm amber mid-tone. The value is unchanged. The SoW does not acknowledge this item. Sam's color palette work was focused on the environment palette section. The Luma expression background was not touched.

At pitch-deck scale, `(248, 238, 220)` will read as off-white. The Excitement panel will lack the immediate warm-energy contrast that the Worry panel's `(195, 212, 228)` provides. Three panels side by side: blue-grey (readable cool), lavender (readable purple-warm), and very pale warm-beige (potentially reading as "no background"). **This item is still sitting on the list.**

---

## SECTION 4: REMAINING OBSTACLES TO PITCH-READINESS

### The Single Most Important Remaining Problem

**The composite reference image has not been produced. This is now four cycles overdue. It is the single most important remaining problem.**

I am not going to soften this statement. A pitch package for an animated series requires a document that shows all four characters at correct proportional scale with legible face detail simultaneously. That document does not exist. The contact sheet shows storyboard thumbnails. The silhouette sheet shows silhouettes. The expression sheets show isolated faces. Nothing answers the question: "What does this world look like when all four characters are in the same frame?"

A buyer sitting across the table from this package will ask: "Can I see them all together?" The answer is currently: "No, not in this package." That is not acceptable. The `contact_sheet_generator.py` exists. The character data exists. This is a four-hour task maximum, probably less. The fact that it has not been completed after four consecutive cycles of prioritization requests suggests a workflow problem, not a capability problem.

### Other Outstanding Items:

1. **Excitement background warmth** — `(248, 238, 220)` → warmer mid-tone. This is still a two-number change. It should not be on the list for Cycle 9.

2. **Hover particle confetti** — now documented as "GL spec" which is incorrect and defensive. The spec must be corrected and the particles resized or removed. If 4×4 was a conscious choice, document the reasoning in the SoW, not in a code comment designed to preempt critique.

3. **Byte action pose body language** — still a tilted rectangle with one pointing arm. The tilt is 9% of body width. The arm extends 80% of body height. At silhouette scale this reads as "pointing." It does not read as "urgent." A posture change involving the legs or a vertical body stretch/crouch would complete the transformation from "indicating" to "acting."

4. **MIRI-A recommended for pitch package** — ensure the silhouette sheet prominently labels which variant is the selected design for development, so downstream production documents reference the correct version.

---

## PRODUCTION VERIFICATION ASSESSMENT

The Cycle 8 SoW states outputs were "regenerated" for each deliverable. It does not state: "generated, opened, visually confirmed [specific element]." The GRUMPY posture change description matches the code values. The Miri redesign description matches what I read in the generator. The Byte oval documentation is thorough and correct. The collar rotation is correctly implemented and documented.

However: the Excitement background was not addressed despite being Priority 1 in my Cycle 7 report. Either the team missed it or decided to defer it without documentation. Both are process failures. The SoW should include a line for each Cycle 7 Priority item: "completed," "deferred — reason," or "descoped."

---

## CYCLE 8 GRADE ASSESSMENT

**Grade: A-**

Here is why the grade rises sharply from B:

**Priority 0 executed — two genuine design concepts delivered.** This is the most significant single-cycle improvement in the project. Miri is no longer a placeholder. She is a character with design language. Both variants demonstrate understanding of silhouette communication, neg-space usage, and personality-driven prop choices. MIRI-A is pitch-ready. MIRI-B is a strong alternate.

**Three of four Priority 1 items from Cycle 7 are resolved.** GRUMPY posture is confrontational. Collar rotation is physically correct. WORRIED/DETERMINED brow differential is 8px and legible. These are not cosmetic fixes — they required design judgment to execute correctly, and the judgment was sound.

**Byte oval consistency** is clean and well-documented. The shape decision is committed to and propagated correctly through the code.

**The ceiling is set by:**
1. Excitement background unchanged — this is a Priority 1 carry-forward for the third time. It is starting to suggest the team doesn't believe the critique is correct rather than that the item is hard.
2. Hover particles re-labeled as "GL spec" rather than fixed — this is a pattern of rationalizing rather than resolving.
3. Composite reference image absent for the fourth consecutive cycle — this is the most damaging single gap in the pitch package.
4. Byte action pose still communicating "indicating" rather than "acting."

The A- grade says: Cycle 8 is the best work this team has produced. The Miri redesign alone justifies the grade leap. But there is still a gap between "best work yet" and "pitch-ready," and that gap is not being closed at equal speed across all fronts. The team is selecting which items to act on and which to rationalize away. That selection process needs to change.

---

## PRIORITY REQUIREMENTS FOR CYCLE 9

**Priority 0 — Non-Negotiable:**
1. **Composite reference image** — all four characters (Luma, Cosmo, Byte, MIRI-A) at correct proportional scale with legible faces, in one document. This is now four cycles overdue. Do not move to Cycle 10 without this.

**Priority 1 — Must Fix:**
2. **Excitement background** — change `BG = (248, 238, 220)` to `(255, 210, 150)` or equivalent warm amber mid-tone. Two numbers. This has been on the list three cycles.
3. **Hover particle confetti** — remove the "GL spec" comment rationalization. Either enlarge to 10×10px minimum or remove the particles entirely. Document the decision in the SoW with reasoning.
4. **Byte action pose** — add a posture element (leg crouch, vertical compression or extension, head lean forward) that amplifies the urgency read beyond "arm pointing."

**Priority 2 — Design Integrity:**
5. **MIRI-A selected variant** — label clearly in silhouette sheet and document in production materials that MIRI-A is the canonical Miri design for the pitch package.
6. **GRUMPY body lean** — consider pushing `body_tilt` from -8 to -12 to -14 for a more aggressive forward lean. The current value is the right direction but conservative.

---

*"Miri finally has a face. Now finish the package she belongs to."*

*Dmitri Volkov — Character Design Critic*
*"A pitch package that cannot show all four characters together is not a pitch package. It is a collection of documents."*
