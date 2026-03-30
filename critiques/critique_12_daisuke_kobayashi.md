# Critique 12 — Daisuke Kobayashi, Character Design Formalist
**Date:** 2026-03-29
**Assets Reviewed:**
- `LTG_CHAR_luma_expression_sheet_v006.py` + turnaround `LTG_CHAR_luma_turnaround_v002.py`
- `LTG_CHAR_byte_expression_sheet.py`
- `LTG_CHAR_cosmo_expression_sheet.py`
- `LTG_CHAR_grandma_miri_expression_sheet_v003.py`
- `LTG_CHAR_glitch_expression_sheet_v002.py`
- `LTG_TOOL_character_lineup.py`
- `character_sheet_standards.md`

---

## Methodology

I reduce every design to its construction primitives and then check whether those primitives are specified consistently across all documents that are supposed to describe the same character. My unit of measurement is whatever the code uses: pixel offsets, multiplier fractions, or head-unit ratios. Inconsistency between documents is not a style choice. It is a production defect.

---

## Issue 1 — CRITICAL: Luma head-unit ratio conflict between expression sheet v006 and turnaround v002

This is the most serious problem in the current package. The two primary documents that define Luma are not describing the same character.

**Expression sheet v006:**
- `HEAD_R = 52` at 1× canvas (1200px wide)
- `HR = 104` at 2× render
- Total body height computed as: `torso_h = HR * 1.80` = 187px at 2×. Pants height `HR * 1.60` = 166px at 2×. Shoes add roughly `HR * 0.42` = 44px. Total character height ≈ head (HR = 104) + neck (HR * 0.18 = 19) + torso (187) + legs (166) + shoes (44) ≈ **520px at 2×** = **260px at 1×**.
- At 1× output, head diameter = 104px. Body height ≈ 260px. **Head-to-body ratio = 104 / 260 ≈ 0.40, or approximately 2.5 heads tall.**

**Turnaround v002:**
- `hu()` function: `CHAR_DRAW_H / 3.2` where `CHAR_DRAW_H = int(BODY_H * 0.86)` = `int(612 * 0.86)` = 526px at 1×. So `hu() = 526 / 3.2 ≈ 164px` at 1×.
- Head radius = `h * 0.50` where `h = hu() * SCALE = 328px` at 2×. So head_r = 164px at 2×, meaning head diameter = 328px at 2×, **164px at 1×**.
- Docstring explicitly states: **"Luma is ~3.2 heads tall."**

**Character lineup v005:**
- `LUMA_HEADS = 3.5` — a third different value.
- `LUMA_RENDER_H = 280px`. Head radius `r = int(hu * 0.46)` where `hu = 280 / 3.5 = 80px`. So head radius ≈ 37px, diameter ≈ 74px. That is consistent with 3.5 heads tall at this render height. ✓ (internally consistent but disagrees with both other documents)

**Summary of Luma's head-to-body ratio across documents:**

| Document | Stated Ratio | Computed Ratio |
|---|---|---|
| Expression sheet v006 | (not stated) | ~2.5 heads tall |
| Turnaround v002 | 3.2 heads tall | 3.2 heads tall |
| Lineup v005 | 3.5 heads tall | 3.5 heads tall |
| Standards doc v001 | Not explicitly stated for ratio | — |

Three documents. Three different ratios. **If I gave this package to fifteen animators, I would get three different body proportions before they even started posing the character.** This is not acceptable.

The expression sheet v006 HEAD_R of 52px at a 1200px canvas — with the body constructed using `HR * 1.80` for torso height — produces a character proportionally shorter and more squat than the turnaround. The v006 expression sheet's `HEAD_R` was likely reduced at some point during the line-weight-reduction cycles without recalibrating body geometry. This is exactly the kind of drift that happens when construction constants are edited in isolation.

**Directive:** Establish one canonical head-to-body ratio for Luma, document it explicitly in `character_sheet_standards.md`, and reconcile all three generators to produce the same ratio. The turnaround's ratio (3.2) should be considered the master reference since it is the most recently updated document with an explicit stated value. The lineup at 3.5 should be corrected to 3.2. The expression sheet must be verified to produce 3.2 heads.

---

## Issue 2 — CRITICAL: Turnaround v002 head outline line weight violates the v006 standard at the 3/4 view

**Expression sheet v006 head outline:** `width=4` at 2× render.

**Turnaround v002:**
- FRONT view: head outline draws the main ellipse with `fill=SKIN` only (no `outline=` argument on the fill pass). Outline is drawn separately with `outline=LINE, width=6`. **Width=6 at 2× — 50% heavier than the v006 standard of width=4.**
- 3/4 view: `draw.ellipse(..., outline=LINE, width=6)` — again width=6.
- SIDE view: `draw.ellipse(..., outline=LINE, width=4)` — correct at this one view.

This is a consistency failure within the turnaround itself: the front and 3/4 views use width=6 while the side view uses width=4. The front and 3/4 views will render with a noticeably heavier outline than the expression sheet. When a scene director compares the turnaround front view to the expression sheet, they will see a different character weight.

Additionally, the 3/4 view cheek nub outlines (`width=4`) are heavier than the v006 spec (`width=3`). The front view cheek nubs (`width=4`) have the same problem.

**Directive:** Turnaround FRONT and 3/4 head outlines must be corrected to `width=4` at 2×. Cheek nub outlines corrected to `width=3`. The standards document must explicitly bind turnaround line weights to the same three-tier table as the expression sheets.

---

## Issue 3 — SERIOUS: Luma turnaround BACK view is absent from the specification

The turnaround docstring lists four views: `["FRONT", "3/4", "SIDE", "BACK"]`. I can confirm the front, 3/4, and side views are implemented in the code. The back view function is not present in the portions I reviewed, and I was not given a file that definitively contains it.

**If the BACK view is not implemented:** A production turnaround with three of four views is not a turnaround. It is a partial reference that forces an animator who needs to draw Luma from behind to invent the back view from scratch. In a production, "from scratch" means fifteen different back views.

What does Luma's hoodie look like from behind? Where does the hair fall? What is the shape of the rear silhouette? None of these are answerable from the current documentation.

**Directive:** Confirm whether the BACK view is implemented in the full turnaround file. If not, implement it. The back view must show: back of hoodie, hood shape, hair silhouette from rear, rear pants/shoe silhouette.

---

## Issue 4 — SERIOUS: Grandma Miri head construction is a different primitive family from all other human characters

**Luma head:** circle + lower-half ellipse fill + cheek nubs. Based on a 1.0 ratio (nearly perfect circle).

**Cosmo head:** `rounded_rectangle` with `radius = hu * 0.12`. hw:hh ratio = 0.43:0.50 — wider than tall, giving a horizontal-oval-ish box.

**Grandma Miri head:** `draw.ellipse([cx - HR, cy - ry, cx + HR, cy + ry])` where `ry = HR * 0.94` — so a near-circle (slightly compressed vertically, 94% of full circle). She also has a jaw ellipse that extends down.

Each of these is from a different construction family: circle, box, oval. This is fine if it is intentional design differentiation, but it is only acceptable if each construction is **fully specified so that a different artist can reproduce it**. The current documentation has none of the following:

- No construction overlay showing what primitive drives the Miri head. Is the 94% compression intentional? What is the jaw ellipse's relationship to the main head circle? (It drops to `cy + ry * 0.80` which is 75% down the head, with height `iry * 0.22` each way — none of this is named or diagrammed.)
- No documented explanation of why Cosmo's head is a rounded-rectangle while Luma's is a circle. If this is a character-differentiating design choice, it must be stated.
- No written "from primitives" spec for any of these. Can a new artist reconstruct Miri's head shape from a written description? No. They would need to guess the 0.94 vertical compression and the jaw ellipse parameters.

**Directive:** Add a construction-geometry section to the standards document (or individual character sheets) for each human character head. State explicitly: what is the primary shape, what modifications are applied, and what ratio governs each modification. A single diagram with labeled dimensions is worth more than a thousand words.

---

## Issue 5 — SERIOUS: Luma turnaround vs lineup — eye specification conflict

**Expression sheet v006 eyes:** `ew = HR * 0.28`, `leh_base = HR * 0.28`, `reh_base = HR * 0.22`. Eye separation: left eye at `cx - HR * 0.38`, right eye at `cx + HR * 0.38`. This means eye center-to-center distance = `HR * 0.76`.

**Turnaround FRONT view eyes:** `ew = h * 0.22`, `eh = h * 0.15`. Eye separation: `sep = h * 0.36`, so left at `cx - sep`, right at `cx + sep`, center-to-center = `h * 0.72`.

At the same head radius (HR = h at 2×), these are:
- Expression sheet eye width ratio: 0.28 of head radius
- Turnaround eye width ratio: 0.22 of head radius — the turnaround eyes are **21% narrower** than the expression sheet eyes.
- Expression sheet eye height ratio: 0.28 (left), 0.22 (right)
- Turnaround eye height ratio: 0.15 — **the turnaround eyes are 32-46% shorter** than the expression sheet.

These are not minor differences. The turnaround eyes produce a noticeably smaller, more subdued eye than the expression sheet. The expression sheet near-circular eye is a key character identifier. The turnaround's horizontally wider but vertically flattened eye reads as a different character.

Additionally, the turnaround uses a single `sep = h * 0.36` for both eyes (symmetric spacing from center), while the expression sheet places left and right eyes at independent positions (`cx - HR*0.38` and `cx + HR*0.38`). These are numerically close but the expression sheet uses HR-relative offsets while the turnaround uses h-relative offsets, and since `h = hu() * SCALE` and the head radius in the turnaround is `int(h * 0.50)`, the effective relationships are not the same.

**Directive:** The expression sheet eye specification (proportions relative to head radius) must be extracted into a shared parameter table and used consistently across both the expression sheet and the turnaround FRONT view. The eye is the single most character-identifying feature. It cannot vary between the two primary reference documents.

---

## Issue 6 — MODERATE: Lineup v005 Byte shadow color does not match expression sheet v004

**Byte expression sheet v004:** `BYTE_SH = (0, 168, 192)` — "#00A8C0 Deep Cyan" (corrected in v002 per Cycle 16 critique).

**Lineup v005:** `BYTE_SH = (0, 144, 176)` — a distinctly darker, more desaturated cyan.

This is a color continuity failure. The lineup Byte will read as darker-bodied than the expression sheet Byte. The v004 expression sheet fix specifically called out the shadow color correction. The lineup was not updated to match.

**Directive:** Correct `BYTE_SH` in the lineup to `(0, 168, 192)` to match v004 canonical value.

---

## Issue 7 — MODERATE: Grandma Miri body outline is width=6, violating the three-tier standard

**Standards doc v001, Section 6 three-tier table:** Silhouette = 8px at 2× render. But Section 6 also says brows are interior structure (4px), not silhouette weight.

**Grandma Miri torso polygon outline:** `width=6` at 2× render. Her brow arcs use `width=4`. Her eye outlines use `width=6`.

The standards document defines silhouette as 8px and interior structure as 4px. Miri's torso at width=6 sits between the two tiers — it is neither properly silhouette weight nor interior structure weight. This ambiguity in the body outline must be resolved. Either Miri's body is silhouette weight (upgrade to 8px) or it is a thicker interior weight (acceptable at 6px only if documented as an intentional exception for her softer design language).

Additionally, the Miri head outline (`draw.ellipse(... width=6)`) is at 6px while Luma's head outline in v006 is 4px. The standards document specifies head outline = 8px silhouette weight at 2×. Neither Luma (4px) nor Miri (6px) matches the documented standard. The table in `character_sheet_standards.md` says silhouette is 8px — but then the notes say the "Cycle 19 correction" changed brow weight from 10px to 4px, which is cited as the "canonical fix reference." This suggests the 8px/4px/2px table in Section 6 may be aspirational or outdated. **The actual values in the generator code do not match the table.** This contradiction must be resolved in the standards document.

**Directive:** Audit the three-tier table in `character_sheet_standards.md` against actual generator values for each character. Either update the table to reflect actual practice or update all generators to comply with the table. Do not leave a document that says "8px silhouette" when every generator uses 4-6px for head outlines.

---

## Issue 8 — MODERATE: Glitch sheet lacks a written construction spec for its body primitive

The Glitch body is constructed via `diamond_pts()`: a four-point polygon with parameterized tilt, squash, and stretch. This is the most unusual body construction in the lineup — not a circle, not a rectangle, but a rhombus. The parameters are:
- `rx`: half-width
- `ry`: half-height
- `top`, `right`, `bot`, `left` points computed with trigonometric offsets

However, none of this is documented as a construction spec. The four vertices are derived from `rx` and `ry` with small offsets (`rx * 0.15`, `rx * 0.2`) that affect the shape. Can a different artist reproduce this diamond from a written spec? Currently: no. They would need to read the code to understand the shape.

**Directive:** Write a one-paragraph "construction from primitives" spec for Glitch: what is the base shape, what are the proportional rules for its four vertices relative to the body center, and how does tilt affect it. This does not need to be elaborate — three sentences and one labeled diagram would suffice.

---

## Issue 9 — MINOR: Cosmo head is documented as `rounded_rectangle` but the construction falls back silently

The `_draw_cosmo_head()` function uses `try: draw.rounded_rectangle()` with a `except AttributeError:` fallback that re-implements the rounded rectangle manually. The fallback exists for older Pillow versions. This means Cosmo's head geometry varies depending on which version of Pillow is installed. The fallback shape (four corner arcs + three rectangles) is a different rendering than the native `rounded_rectangle()`. If a critic or reviewer is running a different Pillow version, they will see a slightly different head shape.

This is not a severe production issue but it is a specification ambiguity. If two artists build their models from the output of different Pillow versions, they are working from different reference images.

**Directive:** Lock the Pillow version in the production environment and remove the fallback, or document that the fallback path produces an intentionally equivalent shape. If the project is using a fixed virtual environment this is already resolved — if so, document it.

---

## Issue 10 — MINOR: Cosmo body tilt formula has no upper-bound clamp

The Cosmo tilt formula is `tilt_off = int(body_tilt * 2.5)`. For `SURPRISED` (body_tilt=5), this produces 12.5px. For `SKEPTICAL` (body_tilt=6), 15px. These are within reason.

However, there is no documented maximum body_tilt value for Cosmo. If a future expression or pose requires body_tilt=20, the tilt_off would be 50px, which at panel scale (PANEL_W = 280px) would push the torso top significantly off-center. The formula multiplier of 2.5 was calibrated empirically ("squint test at 200px thumbnail") — but there is no locked range.

**Directive:** Document the valid range for `body_tilt` in the Cosmo expression spec: minimum, maximum, and the calibration basis for the 2.5 multiplier. Future expression additions must respect this range.

---

## Summary Ratings

| Character | Sheet | Rating | Primary Issue |
|---|---|---|---|
| Luma | Expression sheet v006 | **C** | Head-to-body ratio inconsistent with turnaround (2.5 vs 3.2 heads tall); eye spec conflicts with turnaround |
| Luma | Turnaround v002 | **C** | Line weight violations vs v006 standard; eye spec conflicts with expression sheet; back view confirmation needed |
| Byte | Expression sheet v004 | **B** | Internally consistent; 9-expression grid well-structured; construction clear from code. Lineup shadow color mismatch is external |
| Cosmo | Expression sheet v004 | **B** | Tilt fix is correct and effective. Head primitive underdocumented. Brow asymmetry is specific and producible |
| Grandma Miri | Expression sheet v003 | **C** | Line weight violations; head/body construction not documented to replicable-from-description standard; jaw ellipse parameters undocumented |
| Glitch | Expression sheet v002 | **B-** | 6-expression grid well-differentiated; construction is unusual but internally consistent. Not documented to spec |
| Character lineup v005 | — | **C+** | Luma reconstruction is improved but head-to-body ratio (3.5 heads) contradicts turnaround (3.2 heads). Byte shadow color mismatch |

---

## Priority Directives (ordered by severity)

1. **(P1 — Blocking)** Resolve Luma's head-to-body ratio. Pick one canonical ratio, put it in the standards doc, and make every generator use it. The turnaround's 3.2 is the recommended master.

2. **(P1 — Blocking)** Reconcile Luma's eye specification between v006 expression sheet and v002 turnaround. Eye width, height, and position ratios must be identical in both documents.

3. **(P1 — Blocking)** Confirm or implement the BACK view in the turnaround. A four-view turnaround is not complete with three views.

4. **(P2 — Serious)** Fix turnaround FRONT and 3/4 head outline weights to match v006 (width=4, not width=6).

5. **(P2 — Serious)** Audit and reconcile the three-tier line weight table in `character_sheet_standards.md` against actual generator values. It currently documents values that no generator uses.

6. **(P2 — Serious)** Write a "construction from primitives" section for Miri's head, Cosmo's head, and Glitch's body in the standards document or character-specific files.

7. **(P3 — Moderate)** Fix Byte shadow color in lineup v005 to `(0, 168, 192)`.

8. **(P3 — Moderate)** Document valid body_tilt range for Cosmo.

9. **(P4 — Minor)** Lock or remove Pillow version fallback in Cosmo's head drawing function.

---

## Closing Observation

The character construction has improved measurably since earlier cycles. Byte is the best-documented character in the package — its construction is consistent, its expression space is differentiated, and the damage state (STORM/CRACKED) is precisely specified. Glitch is conceptually clear, even if underdocumented.

Luma is the protagonist. She appears in more documents than any other character. She therefore has more opportunities for cross-document drift, and she has taken all of them. The expression sheet and turnaround for the same character should be built from the same proportional constants. They are not. This is not a creative difference. It is an engineering problem that will compound into an on-model problem the moment a second artist draws this character.

The team has the right instincts — construction guides are implemented, render scales are consistent, line weight tiers are defined. The problem is that the implementation has drifted from the documentation, and the documentation has drifted between documents. Close the gaps. Lock the constants. Make one canonical spec per character that all documents derive from, not several documents that each define their own version.

---

*Daisuke Kobayashi — Character Design Formalist*
*Critique 12 — 2026-03-29*
