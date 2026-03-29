# Critic Feedback — Cycle 11
**Critic:** Dmitri Volkov, Character Design Lead
**Date:** 2026-03-30
**Subject:** Luma Expression Sheet (Priority 0), Sneaker Profile Normalization, Pitch Package Status

---

## VERDICT UPFRONT

Cycle 11 delivered. The Priority 0 item is done, it is done correctly, and it closes the last significant gap in the character documentation package. The sneaker profile inconsistency — which I gave two cycles of final notices — is fixed. The `0.65` is gone. `0.52` is consistent across all four views. I will not mention it again.

The package can now go in front of a development executive. That is a different statement from any I have made in ten cycles of review.

I will document exactly what was delivered, where it succeeds, and what still falls short of the absolute best. There is always something.

---

## SECTION 1: LUMA EXPRESSION SHEET — PRIORITY 0 VERIFICATION

### Existence and Format

File confirmed at `/home/wipkat/team/output/characters/main/luma_expression_sheet.png`.

Dimensions: **912 × 886 px**. Format: RGB. File size: 138K. The 3×2 grid is present. Six panels, confirmed.

The generator (`luma_expression_sheet_generator.py`) matches the structural specification I gave in Cycle 10 exactly:
- 3 cols × 2 rows at `PANEL_W = 280`, `PANEL_H = 390`
- Dark label bar at panel bottom with expression name, `prev_state`, `next_state`
- Distinct background color per panel — all six colors are immediately distinguishable
- Full body drawn beneath each face (hoodie + arms + legs + sneakers)
- Dark canvas background `(30, 22, 16)` matching Byte sheet aesthetic

This is structurally correct. It matches the Byte expression sheet format. It should have existed three cycles ago. It exists now.

### The Six Expressions — Distinctness and Readability

I reviewed all six expression functions in detail and examined the rendered output.

**1. Reckless Excitement** — The signature grin is present: the asymmetric off-center grin, dual brow arches, high cheek blush at full alpha `(220, 80, 50, 110)`. Orange hoodie `HOODIE_O`. Warm amber `BG_EXCITE`. Right eye pupil is shifted `ps=5` laterally — the broken symmetry that is Luma's defining visual tick. The collar is rotated +8° for energy. This is readable at thumbnail scale. Grade: correct.

**2. Worried / Determined** — Corrugator brow kink implemented via a four-point polyline with the V-shape kink at the inner brow `(lex+5, ley-26)`. The mouth is a straight horizontal line with downturned corners — the tense press, not a frown, not a scream. Dark hoodie `HOODIE_W = (52, 38, 24)` on cool blue-grey background `BG_WORRY`. Blush is subdued, alpha 55. This reads as internal conflict without tipping into distress. The emotion is legible. Grade: correct.

**3. Mischievous Plotting** — The left eye is squinted (top height 14px vs bottom 20px asymmetric ellipse), the right eye is full open (eh=28). Sky-high left brow `(lex-5, ley-58)` versus a rising right brow `(rex+5, rey-30) → (rex+28, rey-38)`. The smirk is drawn as a right-sided partial arc with exposed teeth polygon, shifted right of center. Collar tilted -5°. Magenta-purple `BG_MISCH`. This is the most visually complex of the six and it reads correctly. The asymmetric eye pair is the right choice — it creates visual tension without cartoonish exaggeration. Grade: correct.

**4. Settling / Wonder** — Wide symmetric eyes `(ew=28, eh=30)`, dilated pupils `(ley-9, ley+9)`. Both brows raised in identical gentle arcs — this is deliberate and correct: it distinguishes wonder from the asymmetric mischief and the corrugator-kink of determination. The soft open mouth — gentle arc with a small oval gap `(cx-14, mouth_y+4, cx+14, mouth_y+20)` — reads as intake of breath, not a scream. Steel blue hoodie, soft teal-mint background. This expression is the quietest of the six and it correctly communicates emotional deceleration. Grade: correct.

**5. Recognition** — ONE brow sky-high `(lex-2, ley-60)`, the other level `(rex+2, rey-32)`. Left eye more open `(leh=26)`, right eye squinted in concentration `(reh=20)`. The slight open mouth — `arc + small oval` — is the cognitive pause read. This is the hardest expression to get right because it requires reading two conflicting signals simultaneously (excitement AND concentration). The asymmetric brow pair delivers this. Deep blue hoodie, medium periwinkle background. Grade: correct.

**6. Warmth** — Symmetric slightly-narrowed eyes `(eh=20)`, heavier upper lid arc (width 5). Gentle genuine smile arc `(cx-34, cy+28, cx+34, cy+56)` — NO teeth. The cheek crinkle lines (four diagonal strokes, `SKIN_SH` color, width 2) are present on both sides. Warm gold hoodie `HOODIE_WA`, soft peach background `BG_WARMTH`. This is the correct final expression in the sequence — deliberately understated after the dynamic range of the preceding five. Grade: correct.

### The Emotional Arc — prev/next Annotations

The annotation system creates a coherent reading sequence:

```
RECKLESS EXCITEMENT:  ← was: ANY STATE          → next: CHARGING IN
WORRIED/DETERMINED:   ← was: CALM               → next: TAKING ACTION
MISCHIEVOUS PLOTTING: ← was: BORED              → next: EXECUTING PLAN
SETTLING/WONDER:      ← was: EXCITEMENT         → next: CURIOSITY
RECOGNITION:          ← was: CONFUSION          → next: CONNECTING
WARMTH:               ← was: RECOGNITION        → next: CONNECTION
```

This is a functional emotional arc with clear narrative logic. The sequence from the bottom row (Settling → Recognition → Warmth) traces the emotional throughline of the pilot episode. The top row (Excitement → Worry → Mischief) covers Luma's reactive states. A director reading this sheet can immediately map expressions to scenes.

**One annotation issue I will flag:** "WARMTH: ← was: RECOGNITION" is editorially consistent, but the "was: RECOGNITION" annotation creates an implicit dependency between panel 5 and panel 6 that constrains how WARMTH can be used as a standalone expression. A warmth response does not always require prior recognition — it can come from familiarity, from memory, from choice. The annotation is not wrong for the pilot context, but it is slightly over-specific for a general expression documentation sheet. This is a nuance, not a defect.

### The Asymmetric Expression Mechanism

My Cycle 10 brief asked Maya to document "the right-eye rule and whether Luma has an equivalent asymmetric expression mechanism."

The answer is now documented implicitly in the code:
- Reckless Excitement: right eye pupil offset `ps=5` (the asymmetric tick)
- Mischievous Plotting: left eye squinted, right eye fully open (opposite asymmetry)
- Recognition: left eye open, right eye squinted (concentration-side asymmetry)

Luma's asymmetric mechanism is NOT a fixed "right-eye rule" as Byte has a fixed right-eye organic iris. Luma's asymmetry SHIFTS depending on the emotional state — which eye is dominant changes. This is more complex and more expressive than Byte's fixed asymmetry. It is not documented explicitly in the sheet (it requires reading the code), but it is encoded correctly. A character bible annotation would make this discoverable without code access. That is a future task.

**Grade for Luma Expression Sheet: A**

---

## SECTION 2: SNEAKER PROFILE — NORMALIZATION VERIFIED

`draw_luma_side()` in `character_turnaround_generator.py`:

```python
# Sneaker in profile — elongated oval
# Cycle 11 fix: normalized to 0.52 to match front/back view proportions (was 0.65)
fw = int(hu * 0.52)
```

The comment documents the change and names the previous value. This is the correct way to document a correction: name what it was, name what it is now, name the reason. The `0.65` is gone from all four views.

Verification across all four Luma turnaround views:
- `draw_luma_front()`: `fw = int(hu * 0.52)` — confirmed
- `draw_luma_three_quarter()`: `fw = int(hu * 0.52)` — confirmed
- `draw_luma_side()`: `fw = int(hu * 0.52)` — confirmed
- `draw_luma_back()`: `fw = int(hu * 0.52)` — confirmed

All four views are now consistent. The correction that I gave two cycles of final notices to has been executed. It is one number change. It was always one number change.

**Grade for Sneaker Normalization: A**

The A is unqualified. The correction is complete and correctly commented.

---

## SECTION 3: ITEMS CARRIED FROM CYCLE 10 — STATUS

**Byte float-height annotation in lineup (Priority 1 from Cycle 10):**

I searched the turnaround generator for the relevant keywords (ground floor, float height, baseline label, ground plane). No matches. I did not find evidence this was addressed in Cycle 11.

The SOW confirms this item was not assigned to any team member in Cycle 11. The team focused on the Priority 0 item and the sneaker fix. This is a defensible choice — prioritization requires choosing, and the Priority 0 item was the correct priority. However, the float-height annotation gap now carries to Cycle 12. It is a documentation gap, not a design defect, but it will be asked about in a pitch room.

**Status: NOT RESOLVED. Carries to Cycle 12.**

**Cosmo side-view glasses — _draw_cosmo_glasses() unification (Priority 2 from Cycle 10):**

`draw_cosmo_side()` (lines 665–721): The side-view glasses are drawn as a standalone inline implementation — `draw.ellipse()` for the rim, `draw.ellipse()` for the NEG_SPACE lens, `draw.rectangle()` for the ear arm. It does NOT call `_draw_cosmo_glasses()`. The Cycle 10 issue is not resolved.

The current implementation is not wrong — the side-view glasses are functionally correct: rim present, NEG_SPACE lens cutout present, ear arm present. But the consistency guarantee that makes the front/3/4/back glasses so strong is still absent from the side view. `_draw_cosmo_glasses()` is not called. If the glasses geometry is ever updated, the side view will diverge silently.

**Status: NOT RESOLVED. Carries to Cycle 12.**

---

## SECTION 4: THE EXPRESSION SHEET AS A PITCH DOCUMENT

I reviewed the rendered output directly.

The six panels are visually distinct at thumbnail scale. The warm/cool color separation between the background palette groups creates a natural visual rhythm: Excitement (warm) / Worry (cool) / Mischief (warm-purple) on the top row; Wonder (teal-cool) / Recognition (periwinkle-cool) / Warmth (peach-warm) on the bottom row. The temperature shift from top-right to bottom reads as emotional arc, which is correct.

The hoodie color changing per expression panel is a strong choice. Each panel's hoodie color is tuned to the emotion — dark for Worry, magenta-purple for Mischief, warm gold for Warmth. This is the correct approach: costume color as emotional signifier. It also means every panel has a distinct dominant color, which aids quick scanning.

The full-body render beneath each face is the right format choice. An expression sheet that shows only heads is half a design document. Showing the body with the emotion (arm positions, collar rotation, body tilt) creates a complete pose signal, not merely a face signal. Luma's body language reads with her face.

**What I would still like to see that is not present:**

1. The sheet shows six emotions but does not include a neutral/default pose. A neutral panel — where does Luma rest? — anchors the range. Without a neutral reference, the "distance" of each emotion from baseline is harder to read. This is a standard expression sheet convention that was not followed. The Byte expression sheet has this same gap. Both sheets should have a neutral panel. Six expressions plus neutral would require a 7-panel layout (not a clean 3×2), or expanding to a 4×2 (8 panels). This is worth doing.

2. The sheet has no scale reference. There is no head-unit ruler, no height notation, no "at broadcast resolution" note. The Byte documentation set has a character specification file. Luma's expression sheet is currently undocumented in terms of scale. The header line reads correctly ("LUMA — Expression Sheet — Luma & the Glitchkin") but does not include dimensions, head unit, or version number.

These are polish items. They do not prevent pitching. They prevent production.

---

## SECTION 5: OVERALL CYCLE ASSESSMENT

### What Cycle 11 Resolved

- **Luma expression sheet**: existed and is correct — **Priority 0: done**
- **Sneaker profile normalization**: `0.65` → `0.52`, all four views — **Priority 1: done**
- **Style frame dead zone**: mid-air transition element in x=768–960 — **done**
- **Storyboard pitch export**: created and delivered — **done**
- **Pitch package index**: single-document navigator — **done**
- **Style guide sections 9–11**: animation, Glitchkin construction, prop design — **done**
- **Background design package**: two real-world environment frames exist — **partially done** (see Priority 2 carry)

This is a strong cycle. The two items I ranked Priority 0 and Priority 1 in my Cycle 10 brief were both executed correctly.

### What Remains for Cycle 12

Ranked:

**Priority 1 — Must fix:**
1. **Byte float-height annotation** — ground-plane reference line in the character lineup. One annotation. This is its third notice.

**Priority 2 — Should fix:**
2. **Cosmo side-view glasses** — refactor to call `_draw_cosmo_glasses()`. Consistency guarantee is absent. This is its second notice.
3. **Neutral expression panel** — both the Luma and Byte expression sheets are missing a neutral/resting pose. This is a standard expression sheet convention.
4. **Luma expression sheet metadata** — add head unit, version, and dimension annotation to the sheet header or a companion specification file.

**Priority 3 — Polish:**
5. **Background documentation** — the two real-world environment frames exist. They need titles, production notes, and integration into the pitch package index.
6. **Luma asymmetric expression mechanism** — document in character bible so it is discoverable without code access.

---

## CYCLE 11 GRADE

**Grade: A**

The A is for executing both assigned priority items correctly and completely. The Luma expression sheet is a real document. It matches the Byte sheet format. It contains six distinct, readable expressions with a coherent emotional arc and full-body rendering. The sneaker normalization is complete across all four views and correctly commented. The team also delivered substantial secondary work — pitch export, style guide completion, pitch package index, additional background frames — none of which was in my brief.

The A is not A+. The A+ requires the missing items to be gone: the Byte float-height annotation that has carried for two cycles, the Cosmo side-view glasses inconsistency that has carried for two cycles, and the neutral expression panel gap in both expression sheets. These are not hard problems. They have been hard to prioritize. Prioritize them.

The package is now pitch-ready. It was not pitch-ready after Cycle 10. It is pitch-ready after Cycle 11. That is the work. The remaining items improve it from pitch-ready to production-ready. That is the next stage of work.

---

*"The lead character now has a documented face. Six expressions, six bodies, six emotional positions. This is the minimum. Now make it better."*

*Dmitri Volkov — Character Design Critic*
*"Pitch-ready is not the finish line. It is the starting gate."*
