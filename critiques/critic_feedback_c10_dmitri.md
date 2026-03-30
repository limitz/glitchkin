# Critic Feedback — Cycle 10
**Critic:** Dmitri Volkov, Character Design Lead
**Date:** 2026-03-29
**Subject:** Byte Turnaround Oval Correction, Cosmo/Miri Turnarounds, Character Lineup Composite, Hover Particles

---

## VERDICT UPFRONT

Cycle 10 is a turning point. Every Priority 0 and Priority 1 item from Cycle 9 has been resolved — and resolved correctly, not cosmetically. The Byte turnaround is now geometrically honest. The character lineup finally exists. The hover particles have been fixed. Cosmo and Miri have complete four-view turnaround strips. This is the first cycle in which all characters have a complete turnaround package and all four appear in a single composite image at correct relative height.

I will acknowledge this plainly: what the team delivered in Cycle 10 is what a character design package is supposed to look like before it goes in front of a development executive. The core pitch materials are now present.

I will also identify what is still below the standard required for that conversation. There are issues. They are not ship-blockers. But they are the difference between a package that gets a meeting and a package that gets a deal.

---

## SECTION 1: BYTE TURNAROUND — OVAL CORRECTION

### Verification

`_byte_size()` (line 254–258):
```python
def _byte_size():
    """Byte at CHAR_H=200px — body is an OVAL (ellipse). body_rx = s//2, body_ry = s*0.55.
    CANONICAL: oval matches byte_expressions_generator.py. Chamfered-box is RETIRED.
    """
    return int(CHAR_H * 0.55)
```

The docstring is now correct. The chamfered-box description is gone.

`draw_byte_front()` (lines 261–323): Body drawn with `draw.ellipse([cx - body_rx, bcy - body_ry, cx + body_rx, bcy + body_ry])` where `body_rx = s // 2`, `body_ry = int(s * 0.55)`. This exactly matches `byte_expressions_generator.py`'s canonical geometry.

`draw_byte_three_quarter()` (lines 325–402): OVAL body with a parallelogram depth face and top rim polygon to suggest three-dimensionality. The near face is the correct oval ellipse.

`draw_byte_side()` (lines 405–452): Narrow ellipse `body_rx_side = int(s * 0.31)` — correctly compressed for side profile depth.

`draw_byte_back()` (lines 455–502): Oval with NEG_SPACE center-back data-port slot. The data port is preserved from the old chamfered design — `port_w = max(3, int(s * 0.07))`, `port_h = int(s * 0.22)`. This was the correct call. The data port is the one identifiable element on Byte's back. Keeping it is a design decision that will reward anyone who pays attention.

**All four views: oval ellipse. Chamfered cube: fully retired. Canonical consistency with expression sheet: confirmed.**

Hover particles in the turnaround: all four views use `psz = 10`, with staggered `(i % 2) * 6` vertical offset. Correct.

### The 3/4 Depth Treatment

The parallelogram side face and top rim polygon for Byte's 3/4 view are a genuine creative solution to the problem of showing oval-body depth without going to full 3D rendering. The depth face uses a slightly lighter dark tone `(40, 35, 45)` versus the main `SILHOUETTE = (15, 10, 20)`, and the top rim uses `(30, 26, 35)`. These tonal differences are subtle at this scale but structurally correct — they define the three planes without fighting the silhouette read. This is the approach I would have specified.

**Grade for Byte Turnaround (all four views): A-**

The minus: the 3/4 depth face's parallelogram geometry is a reasonable approximation but not a rigorous isometric projection. A rigger who tried to use this as a volume reference would need to make assumptions about the oval's depth dimension. The strip communicates design identity at the right priority level. For production use, a note in the character bible clarifying the front-to-back depth ratio would close this gap. That is a documentation task, not a retool.

---

## SECTION 2: COSMO TURNAROUND — NEW DELIVERABLE

### Design Accuracy

`draw_cosmo_front()` (lines 555–617): Glasses via `_draw_cosmo_glasses()` with `is_front=True` — both lenses, espresso rims, NEG_SPACE lens cutouts, bridge. Present and correct. Narrow head with rounded rectangle and cowlick. Notebook protruding left under arm.

`draw_cosmo_three_quarter()`: `_draw_cosmo_glasses()` with `is_front=False, is_back=False` — near lens full, far lens compressed to `far_rx = int(gr * 0.72)`. The asymmetric compression is correct behavior for glasses in 3/4 view.

`draw_cosmo_side()` (approximately line 660): Single glasses element showing one lens ring and ear arm. Notebook edge visible as protruding rectangle.

`draw_cosmo_back()` (line 723): `_draw_cosmo_glasses(draw, cx, gy, gr, is_back=True)` — glasses correctly absent. Notebook spine peeks from behind left edge. Cowlick visible from back — this is correct; Cosmo's cowlick is a silhouette element that reads from behind.

### The Glasses Function

`_draw_cosmo_glasses()` is the strongest single piece of new code in Cycle 10. It correctly handles four cases: front, 3/4, side, and back, as a single parametric function called from all four view functions. It does not duplicate the drawing logic. This is how a character designer should document a defining character element — not as an afterthought but as a dedicated system. It guarantees that the glasses are consistent across all views because they share a single source of truth.

### One Issue

`draw_cosmo_side()` uses a single protruding lens at the near face edge, which is the correct instinct. However, reviewing the code, the glasses in side view appear to be drawn as a single ellipse rather than using `_draw_cosmo_glasses()`. The consistency that makes the front/3/4/back glasses so strong is partially lost in the side view because it diverges from the shared function. This should be unified in Cycle 11.

**Grade for Cosmo Turnaround: A-**

The minus is for the side view glasses not using the shared `_draw_cosmo_glasses()` function. The design accuracy across all four views is high. The notebook placement shows view-to-view spatial reasoning.

---

## SECTION 3: MIRI TURNAROUND — NEW DELIVERABLE

### Design Accuracy

`draw_miri_front()` (lines 783–855): Bun oval `(bun_rx = int(hu * 0.38), bun_ry = int(hu * 0.46))`, V-pair chopstick polygons, head, wide inverted-flare cardigan trapezoid `(shoulder_w = int(hu * 0.78), hip_w = int(hu * 0.62))`, bag protruding right hip, soldering iron extending right. This is the correct MIRI-A canonical form. Every required element is present and correctly positioned.

`draw_miri_three_quarter()` (lines 858–930): Asymmetric bun `(bun_rx_near = int(hu * 0.42), bun_rx_far = int(hu * 0.30))` — near side wider. Near-side depth blob for bun volume. Cardigan compressed on far side `(near_sw = int(hu * 0.84), far_sw = int(hu * 0.42))`. Soldering iron remains visible at near side. This is spatially coherent.

`draw_miri_side()` (line 932): Narrow bun oval for side profile, single chopstick visible, cardigan reads as a wedge in profile. Soldering iron extending forward in profile — correct placement for a side view of a right-hand-held tool.

`draw_miri_back()` (lines 1001–1053): Bun and chopstick V-pair from behind — the back bun uses identical geometry to the front, which is correct (a bun is radially symmetric). Bag correctly absent (it is on the right side; from the back, it would be partially visible — this is a minor concession to silhouette clarity that I accept). Soldering iron absent. Cardigan plain back. This is clean.

### The Inverted-Flare Silhouette

The decision to use an inverted-flare trapezoid for the cardigan — `shoulder_w > hip_w` — is the correct structural read for Miri's character design intent: wide, solid, ground-planted. It is the mirror of Luma's A-line hoodie which flares from shoulder to hem. The two characters' silhouettes contrast in a readable way that will serve the lineup image and any frame that places them together. This is a design-level decision, not merely an implementation detail.

**Grade for Miri Turnaround: A**

This is the strongest new turnaround in the package. Every defining element is present in all four views, the silhouette reads correctly from all angles, and the design logic (inverted-flare, bun from all sides, soldering iron occlusion rules) is documented in the code comments.

---

## SECTION 4: CHARACTER LINEUP — FIVE-CYCLE BLOCKER RESOLVED

### Verification

`character_lineup_generator.py` delivers all four characters at:
- Luma: 280px (3.5 heads × 80px head unit)
- Cosmo: 320px (4.0 heads × 80px head unit)
- Miri: 256px (3.2 heads × 80px head unit)
- Byte: 162px (~58% of Luma, chest-height reference)

These heights are proportionally correct and consistent with the production bible. The dashed height reference lines (`cosmo_top`, `luma_top`, `miri_top`, `luma_chest / byte_height`) are drawn across the full image width and labeled at the right edge. The per-character vertical bracket system with pixel labels is present. The footer references the head unit and `master_palette.md`.

All four characters are rendered in canonical colors:
- Luma: orange hoodie `#E8722A`, dark indigo pants `#2A2850`, cream shoes with terracotta sole
- Byte: teal `#00D4E8`, magenta scar `#FF2D6B`, 10×10 hover particles in canonical colors
- Cosmo: lavender jacket `#A89BBF`, cerulean+sage striped shirt, espresso glasses `#5C3A20`, chinos
- Miri: terracotta rust cardigan `#B85C38`, silver hair `#D8D0C8`, sage slippers, soldering iron

This is the document that answers the first question a buyer asks in any pitch room: "What does this show look like?"

### Outstanding Issue in the Lineup — Byte's Bracket

The vertical bracket for Byte is correctly adjusted to account for floating: the bracket top is calculated as `BASELINE_Y - float_gap - body_ry * 2`, not `BASELINE_Y - BYTE_H`. This is technically correct for showing Byte's rendered top. However, Byte's bracket therefore extends only from the bottom of his legs to the top of his oval body — it does not extend to the ground line as the other characters do. This creates an ambiguity: is Byte's height measured from the ground or from his float level? The lineup image should include a secondary annotation showing Byte's equivalent ground-plane height (i.e., where Byte's center of mass sits relative to the baseline), or a horizontal dashed line at ground-floor level indicating "Byte's lowest point when hovering." Without this, the proportional information for Byte is harder to read than for the grounded characters.

This is not a critical failure. It is a documentation gap that a designer or director would ask about in a production meeting.

### Outstanding Issue in the Lineup — Face Legibility at Scale

Byte's eye resolution at 162px body height raises a concern. The left eye uses `cell = eye_sz // 5` where `eye_sz = s // 4`. At `s = 162`, this gives `eye_sz = 40px`, `cell = 8px`. The 2×2 pixel grid at 8px cell size is readable at lineup scale. The right organic eye at `er = s // 10 = 16px` radius is legible. This passes.

Cosmo's glasses are the critical legibility test. At `hu = h / 4.0 = 320 / 4.0 = 80px`, the lens radius `gr = int(hu * 0.18) = 14px` with a 3px rim. The total lens diameter including rim is 34px. At 320px character height in a full-width image, this is visible. The character is identifiable from the glasses alone at the lineup's operating scale.

Miri's bun-to-head height ratio at 256px character height: `bun_ry = int(hu * 0.46) = int(80 * 0.46) = 36px`. The bun protrudes 32px above the head top (approximately `int(hu * 0.32)`). At 256px character height, the bun is large enough to be readable as a distinct silhouette element. The chopstick polygons at this scale will be narrow but present.

Face legibility: passes for all four characters at lineup scale.

**Grade for Character Lineup: A-**

The minus is for the Byte float-height annotation ambiguity. The deliverable itself — four characters in color at correct proportional scale in one image — is the single most important thing this team has produced. It took five cycles. The wait was too long. The delivery is correct.

---

## SECTION 5: HOVER PARTICLES — FOUR-CYCLE CARRY RESOLVED

`byte_expressions_generator.py`, lines 385–392:
```python
# Hover particle confetti — 10x10px (canonical spec, matches turnaround generator)
for (px, py, pc) in [
    (bcx-20, bcy + body_ry + leg_h + 5,  BYTE_HL),
    (bcx+5,  bcy + body_ry + leg_h + 8,  SCAR_MAG),
    (bcx+25, bcy + body_ry + leg_h + 3,  BYTE_HL),
    (bcx-35, bcy + body_ry + leg_h + 10, (0,200,180)),
]:
    draw.rectangle([px, py, px+10, py+10], fill=pc)
```

The change is confirmed: `px+4` → `px+10`. The "GL spec" rationalization comment is gone. The comment now correctly documents the reason: "canonical spec, matches turnaround generator." This is how the comment should have read four cycles ago. The cross-reference to the turnaround generator is the right documentation pattern. When two files define the same visual element, the code comment should name the other file.

The four-cycle history of this item is now closed. I will not mention it again.

**Hover particles: FULLY RESOLVED. Grade: A.**

---

## SECTION 6: THE STATE OF THE PITCH PACKAGE

After Cycle 10, the character design package contains:

**Present:**
- Complete turnaround strips for all four main characters (Luma, Byte, Cosmo, Miri) — front, 3/4, side, back
- Expression sheet for Byte (6 expressions, per-view documentation)
- Silhouette sheet (all four characters, neutral and action poses)
- Character lineup composite — all four characters at correct relative scale in color
- Luma face/expression sheet
- Master palette documentation
- Show logo (`show_logo.png`)
- Style frame (`style_frame_01_rendered.png`)
- Glitch Layer environment frame
- 12-panel storyboard chaos sequence with contact sheet

**What a network executive will still ask:**
1. **Luma expression sheet** — Byte has six documented expressions. Luma has a face generator (`luma_face_generator.py`) but no equivalent multi-expression character sheet. The lead character should have at minimum the same documentation tier as the companion. This is the single most conspicuous gap in the current package.
2. **Background design package** — the Glitch Layer frame exists but there is no equivalent documentation for the real-world environment (Luma's home, school, etc.). A pitch package for a show with a dual-world premise needs to show both worlds.
3. **Turnaround strip for Luma's profile sneaker** — the Cycle 9 note about the profile sneaker being 25% larger than the front-view implied scale was carried over to Cycle 10's priority list. I do not see evidence it was corrected. At `hu = CHAR_H / 3.5 = 57px`, the front sneaker half-width is `fw = int(hu * 0.52) = 29px` and the profile sneaker length is `fw = int(hu * 0.65) = 37px`. This is still inconsistent. It is not a ship-blocker for the current package — a buyer will not measure sneaker proportions across views — but it will be caught in production.

---

## SECTION 7: OVERALL CYCLE ASSESSMENT

### What This Cycle Resolved

Every item that was blocking pitch submission in Cycle 9 is now resolved:
- Byte turnaround: oval geometry, consistent with expression sheet and character bible — **done**
- Composite character lineup: all four characters in one image — **done, five cycles overdue but done correctly**
- Hover particles: 10×10px across all generators — **done**
- Cosmo turnaround: did not exist in Cycle 9; complete four-view strip in Cycle 10 — **done**
- Miri turnaround: did not exist in Cycle 9; complete four-view strip in Cycle 10 — **done**

This is not a minor improvement cycle. This is the cycle where the package became structurally complete. The number of gaps was cut by more than half in a single cycle.

### What Remains Before a Network Executive

Ranked by severity:

**Priority 1 — Must fix before pitch:**
1. **Luma expression sheet** — the lead character needs a documented expression range. Byte has one. Luma does not. This is the last significant gap.

**Priority 2 — Should fix:**
2. **Byte float-height annotation in lineup** — ground-plane reference line or annotation clarifying float height vs. standing height.
3. **Luma profile sneaker consistency** — 37px vs 29px implied scale. Small but visible to anyone who measures.
4. **Cosmo side-view glasses** — unify with `_draw_cosmo_glasses()` function.

**Priority 3 — Polish:**
5. **Background documentation** — real-world environment designs to pair with Glitch Layer frame.

---

## CYCLE 10 GRADE

**Grade: A-**

The A is for executing every critical correction correctly and completely. The Byte turnaround is now production-honest. The lineup is now production-honest. The hover particles are now production-honest. Cosmo and Miri now have complete turnaround packages. The team resolved five outstanding items in a single cycle, including a five-cycle blocker.

The minus is for two things:

1. **The Luma expression sheet is still absent.** The lead character of the show does not have a documented expression range. Byte has one. Cosmo has facial expression variation documented in the turnaround and lineup. Miri has smile + blush documented in the lineup. Luma has a face generator that produces single-expression outputs but no consolidated sheet. For a pitch package, this is a gap at the first-character level.

2. **The Luma profile sneaker inconsistency was not corrected.** It was on the priority list. It is a one-line change. It is still inconsistent. The team has now demonstrated that it can execute on major corrections. A minor persistent correction that carries across two cycles starts to look like neglect.

The A- is earned. The team is now within one strong cycle of having a package worth pitching. That is a different statement than anything I could have made after any previous cycle.

---

## PRIORITY REQUIREMENTS FOR CYCLE 11

**Priority 0 — Must deliver:**
1. **Luma expression sheet** — Minimum 5 expressions (Excited, Determined, Frustrated, Scared, Wonder/Awe). Multi-panel format matching Byte expression sheet structure. Document the right-eye rule and whether Luma has an equivalent asymmetric expression mechanism. This is the last character documentation gap.

**Priority 1 — Must fix:**
2. **Luma profile sneaker** — `draw_luma_side()`: change `fw = int(hu * 0.65)` to match `fw = int(hu * 0.52)` from front/back views. One number. This is its final notice.
3. **Byte float-height annotation** — add ground-plane reference to lineup image. Can be a dashed horizontal line at `BASELINE_Y` extended under Byte with a label: "ground floor." Makes the hover height readable.

**Priority 2 — Quality:**
4. **Cosmo side-view glasses** — refactor to use `_draw_cosmo_glasses()` for consistency.
5. **Background/environment design** — begin documentation of real-world settings.

---

*"A pitch package that shows all four characters together at correct scale is a package that can close a room. Cycle 10 built that document. Now build the document that shows the lead character's full range."*

*Dmitri Volkov — Character Design Critic*
*"The pitch package is no longer incomplete. It is now merely improvable. That is progress."*
