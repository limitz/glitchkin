<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Expression Pose Vocabulary Brief — Cycle 34
**Author:** Lee Tanaka — Character Staging & Visual Acting Specialist
**Cycle:** 34
**Date:** 2026-03-29
**For:** Maya Santos (character design implementation)
**Subject:** Silhouette differentiation — actionable pose changes per character

---

## The Problem

Maya's `LTG_TOOL_expression_silhouette.py` C33 baseline run returned:

| Sheet | Result | Max Similarity |
|-------|--------|----------------|
| Luma v008 | FAIL | 91% |
| Cosmo v003 | FAIL | 96% |
| Miri v003 (Miri v002 in baseline) | FAIL | 94% |
| Glitch v003 | PASS | 71% |

All three human characters fail at 85% threshold. The combined_similarity measure (0.6×IoM + 0.4×XOR) confirms the silhouettes are indistinguishable between expressions at thumbnail scale. Glitch passes because the shape design builds differentiation into the body type — the human characters have not been designed with the same principle.

The fix is not to redesign the characters. The fix is to assign distinct body-language vocabulary to each expression so that the silhouette changes shape between emotional states.

---

## Why Silhouette Differentiation Matters

A commissioning editor reviewing a character sheet does the squint test in the first 3 seconds. If all 6+ expressions read as the same shape in different colors, the character is not expressive — they are decorative. The expressions must be distinct in outline, not just in face.

Glitch passes because each expression has a different body configuration: MISCHIEVOUS leans, PANICKED recoils, TRIUMPHANT arms-up, HOLLOW deflates. The body IS the expression. The human character sheets have not applied this principle consistently.

---

## Guiding Principle (applies to all three characters)

**Each expression must have a unique silhouette hook — one body-language element that changes shape at thumbnail scale.** The face contributes to the expression; the silhouette is what makes expressions distinguishable at a glance.

Silhouette hooks fall into four categories:
1. **Arm position** — where are the arms? Above head? Crossed? At sides? Extended?
2. **Lean direction** — torso forward, backward, sideways?
3. **Head angle** — tilted, turned, dropped?
4. **Width vs height change** — does the silhouette get wider (open arms) or taller (extended reach) or narrower (contracted/crossed)?

Each expression should use a different hook. No two expressions should share the same primary hook.

---

## Luma — Expression Pose Vocabulary

**Current sheet: v008 — 7 expressions (THE NOTICING + 6 legacy)**
**Tool:** `LTG_TOOL_luma_expression_sheet.py`

### THE NOTICING (v008 anchor) — STATUS: CORRECTLY DIFFERENTIATED
- Silhouette hook: right arm bent to chin. Body upright, wide stance.
- This is already correct and distinct. Do not change.

### CURIOUS — NEEDS STRONGER DIFFERENTIATION
**Current:** Body tilts forward, both arms extended — reaching out.
**Problem:** "arms extended" is shared with DETERMINED (arms at hips, still semi-extended).
**Change:**
- Increase forward lean to body_tilt = -int(HR * 0.28) (was -0.20). This exaggerates the lean and creates a more dramatic forward triangular silhouette.
- LEFT arm: extend further forward and upward (point gesture — not just level, but angled up 15–20°). The pointing is Luma's visual signature for curiosity; it should read as a pointing arm-spike in the silhouette.
- RIGHT arm: drop further back and down (trailing behind as she leans forward). This creates clear front/back arm asymmetry visible in silhouette.
- **Silhouette read:** diagonal forward-leaning shape with one spike (pointing arm) forward and one trailing.

### DETERMINED — NEEDS STRONGER DIFFERENTIATION
**Current:** Arms at hips, zero tilt, wide stance.
**Problem:** "arms at hips, zero tilt" is close to THE NOTICING profile.
**Change:**
- Both arms go to hips (this is correct — keep). But: fists at hips, elbows OUT. The elbows should visibly flare from the silhouette. `arm_l` and `arm_r` endpoints should extend out past the torso width before coming back to the hip.
- Add a fractional head-forward push (head leaning 5–8° toward camera). Achievable as cy_offset adjustment or by placing head slightly forward of neck in draw order.
- **Silhouette read:** wide-stance, elbows-out diamond shape at the torso. Distinct from THE NOTICING (which is narrow/upright at the arm zone).

### SURPRISED — NEEDS STRONGER DIFFERENTIATION
**Current:** Body tilts back, arms not clearly extended.
**Change:**
- Body leans BACK further: body_tilt = +int(HR * 0.22) (more pronounced recoil). This backward lean creates the opposite silhouette from CURIOUS's forward lean.
- Both arms: raise outward and upward — hands at shoulder height or above, elbows bent. The "hands up" shape is distinct from every other expression.
- Head: pulled back and slightly down (chin tuck of surprise). cy_offset -int(HR * 0.04) upward.
- **Silhouette read:** backward-leaning with wide raised arms. Instantly distinct from forward-lean expressions and contracted expressions.

### WORRIED — NEEDS COMPLETE REDESIGN
**Current:** Arms crossed, arms close to body. Nkechi C13: "arms-crossed generic concern."
**Problem:** WORRIED and THE NOTICING both have narrow arm profiles in the current silhouette.
**Change:**
- Keep arms crossed as the expression choice (it IS worry). But: make the crossed arms VISIBLE in silhouette.
  - Each crossed arm's elbow should extend further from the body than the hands. Currently the cross looks like a tight contracted shape. Make the elbows flare slightly — the arms wrap around the torso with visible elbow protrusions at body sides.
  - Add a slight body hunch: torso_h should contract (shorter), head drops toward shoulder (cy_offset lower by +int(HR * 0.06) = head closer to torso top).
- **Silhouette read:** hunched torso with crossed-arm elbow protrusions at sides. Distinct from NOTICING (upright) and DETERMINED (elbows-out open).

### DELIGHTED — NEEDS STRONGER DIFFERENTIATION
**Current:** Minimal differentiation from other upright poses.
**Change:**
- Both arms UP — raised overhead in a V or Y shape. This is the most distinct possible arm position and currently unused by any expression.
- Both feet may come slightly off ground (hop / bounce energy). Small lift.
- Head tilted back slightly — the physical behavior of uncontrolled laughter/delight.
- **Silhouette read:** wide-top Y or V shape with arms overhead. Uniquely tall silhouette. Cannot be confused with any other expression.

### FRUSTRATED — NEEDS STRONGER DIFFERENTIATION
**Current:** Arms folded, backward lean. Nkechi C13: "the adult's idea of child frustration."
**Change (both pose redesign AND emotional realism):**
- 12-year-old frustration is NOT backward lean + folded arms (that is adult sulking). 12-year-old frustration is: body facing the problem, arms reacting to it.
- ONE arm: flings out to the side — a gesture of exasperation, palm out (like "what even is this"). This creates a horizontal arm-spike to one side.
- OTHER arm: remains at side, slightly raised, fist closed (restrained frustration).
- Slight forward lean (she hasn't given up — she is annoyed).
- **Silhouette read:** asymmetric — one arm spiking sideways, body slightly forward. Distinct from every other expression through the one-sided arm extension.

---

## Cosmo — Expression Pose Vocabulary

**Current sheet: v003 — 6 expressions: THOUGHTFUL, SKEPTICAL, DELIGHTED, AWKWARD, WORRIED, SURPRISED**
**Tool:** `LTG_TOOL_cosmo_expression_sheet.py`
**C33 baseline: 96% similarity — worst of the three sheets**

Cosmo's design challenge: he is taller, thinner, more contained than Luma. His body naturally generates fewer wide silhouette changes. The fix is to assign him poses that exploit his proportions (long arms, tall frame) for distinct shapes.

### THOUGHTFUL — NEEDS STRONGER DIFFERENTIATION
**Current:** Likely standing neutral or slight lean.
**Change:**
- One arm raised — index finger touching glasses frame (adjusting glasses). This is Cosmo's character signature gesture.
- The glasses-touching gesture creates a specific arm angle (elbow at approximately 90°, raised to face height) that is uniquely Cosmo.
- Other arm: straight at side or tucked slightly behind back (intellectual containment).
- **Silhouette read:** one arm raised to face height with elbow visible. Distinct from neutral and from SKEPTICAL.

### SKEPTICAL — NEEDS STRONGER DIFFERENTIATION
**Current:** body_tilt adjustment from v001/v002 (main existing fix).
**Change:**
- Arms crossed (this is correct for SKEPTICAL). But: ADD leaning to one side (weight shift — he leans slightly left or right). This hip-shifted lean with crossed arms is the "eyebrow pose" of skepticism — it creates a diamond hip silhouette that is wider at one side.
- Head: slightly tilted to the side he's leaning toward.
- **Silhouette read:** leaning diamond shape — hip out, head tilted the same direction. Clear even in thumbnail.

### DELIGHTED — NEEDS STRONGER DIFFERENTIATION
**Current:** Unclear differentiation.
**Change:**
- This is Cosmo's most surprising emotional state — he does not delight easily. When he does, it shows in the body.
- Both hands: clap position or raised fists (but not both arms overhead like Luma's DELIGHTED). Cosmo's delight is more restrained — hands up to chest height, elbows bent, like a suppressed cheer.
- Body: small lean forward into the delight (he is trying to contain it).
- **Silhouette read:** front-facing with raised bent-arms-at-chest-height, forward lean. Distinct from THOUGHTFUL (one arm) and SURPRISED.

### AWKWARD — NEEDS COMPLETE REDESIGN
**Current:** Likely symmetric or near-neutral.
**Problem:** Awkward has no generic silhouette solution.
**Change:**
- AWKWARD = maximum asymmetry. One shoulder raised, one dropped. One foot turned inward (pigeon-toe inward rotation). One arm at side, one arm stiff with palm out (defensive "I didn't mean to" gesture).
- Head: pulled into the raised shoulder (turtle-neck gesture).
- **Silhouette read:** jagged asymmetric shape. Both left and right edges are at different heights. No other expression looks like this.

### WORRIED — NEEDS STRONGER DIFFERENTIATION
**Current:** Generic concern.
**Change:**
- Cosmo's WORRIED is different from Luma's. He is an analyst — his worry reads as thinking about outcomes.
- Both hands raised to the sides of his head (the "head-grab" gesture of someone running through scenarios). Arms form a wide bracket shape around the head.
- Body: slight hunch, head pressing downward into the hands.
- **Silhouette read:** wide-W shape at head level (arms + head = wide top). Distinct from all other expressions.

### SURPRISED — NEEDS STRONGER DIFFERENTIATION
**Current:** Blush added (v004). Pose unclear.
**Change:**
- Both arms: shoot outward from the body — near-horizontal, elbows slightly bent (startle reflex). This is the "hands out" startle.
- Body: recoils backward — backward lean.
- **Silhouette read:** wide horizontal arm-spread + backward lean. The combination of horizontal extent + backward lean is uniquely SURPRISED.

---

## Grandma Miri — Expression Pose Vocabulary

**Current sheet: v003 — 6 expressions: WARM/WELCOMING, NOSTALGIC/WISTFUL, CONCERNED, SURPRISED/DELIGHTED, WISE/KNOWING, KNOWING STILLNESS**
**Tool:** `LTG_TOOL_grandma_miri_expression_sheet.py`
**C33 baseline: 94% (v002 tested) — second worst**

Miri's design challenge: she is older, rounder, moves less dramatically than Luma or Cosmo. Her expressiveness is in gesture, not in sweeping body motion. The fix: assign each expression a distinct gesture that reads in silhouette at her scale.

**Key constraint (from Nkechi C13):** KNOWING STILLNESS and WISE/KNOWING are already face-only differentiated (body poses identical by design decision). This means the OTHER four expressions must carry maximum silhouette differentiation to compensate. If only two expressions are silhouette-distinct, the sheet is still failing.

### WARM/WELCOMING — STATUS: NEEDS STRONGER DIFFERENTIATION
**Current:** Likely arms open or hands forward.
**Change:**
- Both arms: wide open — elbows bent, forearms up, hands at chest/shoulder height, palms facing out (embrace invitation). This is the iconic welcoming gesture.
- Body: slight lean forward (toward whoever she is welcoming).
- **Silhouette read:** wide-top V or U shape from arms. Must be significantly wider than CONCERNED or NOSTALGIC.

### NOSTALGIC/WISTFUL — NEEDS STRONGER DIFFERENTIATION
**Current:** Likely subtle lean or hand-to-face.
**Change:**
- One hand to chest — palm flat on sternum (the "this hits me in the heart" gesture). This is a recognizable grandmotherly gesture.
- Other arm: at side or slightly in front of body, lower.
- Head: slightly tilted down, eyes looking up or slightly away (the wistful gaze direction).
- **Silhouette read:** compact — arms near body. Distinct from WELCOMING (which is wide) by being narrow.

### CONCERNED — NEEDS STRONGER DIFFERENTIATION
**Current:** Unclear from v002 baseline.
**Change:**
- Both hands clasped at chest level (prayer/worry hands). This is physically distinct from the flat-palm-chest of NOSTALGIC.
- Body: slight forward lean toward the person she is concerned about.
- Head: slightly forward and down — focused attention.
- **Silhouette read:** compact top (clasped hands, no wide arm spread), forward lean. Distinct from WELCOMING (wide) and NOSTALGIC (narrow/static).

### SURPRISED/DELIGHTED — NEEDS STRONGER DIFFERENTIATION
**Current:** v001 had some differentiation; unclear if preserved in v003.
**Change:**
- One hand to cheek (the grandmother "oh my goodness" gesture). The hand-to-cheek creates a clear arm-up-to-face silhouette element.
- Body: small pull-back (mild recoil of surprise).
- Other arm: slightly raised or at chest.
- **Silhouette read:** one arm raised to face level from the side. This is the asymmetric silhouette hook that distinguishes it from all the symmetric poses.

### WISE/KNOWING — KEEP EXISTING + REFINE
**Note:** This and KNOWING STILLNESS are intentionally face-differentiated only (per current design). Maintaining this is correct per the character spec. However, WISE/KNOWING needs a small pose hook to ensure the *sheet* passes the tool even if the two poses are related.
**Change:**
- Add: arms loosely crossed (not tight-worried, but relaxed-knowing). Crossed arms at rest = elder confidence.
- Slight weight to one side (comfortable authority lean).
- **Silhouette read:** relaxed crossed arms at mid-torso level. Different from CONCERNED (clasped at chest) and WELCOMING (wide open).

### KNOWING STILLNESS — KEEP EXISTING
**Current:** Heavy-lidded oblique gaze, asymmetric suppressed smile. Body likely near-neutral.
**This expression is intentionally face-differentiated.** However:
- To provide any silhouette difference from WISE/KNOWING: add ONE element: one hand raised slightly, index finger pointing down at her side (a very subtle "I know more than I'm saying" gesture). This gives the silhouette one small asymmetric element.
- Head: fractionally turned to show more 3/4 profile (not full front). This changes the hair silhouette slightly.
- **The silhouette will still be close to WISE/KNOWING.** Accept this. The score will improve from face-only differentiation to face + one gesture element differentiation.

---

## Implementation Notes for Maya

1. **Test the changes with `LTG_TOOL_expression_silhouette.py` after each sheet.** Target: PASS at 85% threshold. At minimum: no pair above 90%.

2. **Run `LTG_TOOL_render_qa.py` on the output sheet.** Use `asset_type="character_sheet"` to suppress false-positive warm/cool WARN.

3. **Name the outputs:** `LTG_CHAR_luma_expressions.png`, `LTG_CHAR_cosmo_expression_sheet.png`, `LTG_CHAR_grandma_miri_expression_sheet.png`. Generators: increment version numbers.

4. **Priority order:**
   - Luma: DELIGHTED (arms-up is most urgent — currently no expression uses the overhead arm hook), SURPRISED (backward lean + raised arms), FRUSTRATED (one-sided fling)
   - Cosmo: AWKWARD (most unique if redesigned), WORRIED (head-grab), SURPRISED
   - Miri: WELCOMING (wide open — gives the sheet its range), SURPRISED/DELIGHTED (hand-to-cheek)

5. **Do not change character proportions.** Head size, body height, eye width — all carry forward from current canonical specs.

6. **The face expressions may remain unchanged** for any expression where only the pose is being modified. The purpose of this brief is silhouette differentiation, not expression redesign.

---

*Lee Tanaka — Character Staging & Visual Acting Specialist — C34*
