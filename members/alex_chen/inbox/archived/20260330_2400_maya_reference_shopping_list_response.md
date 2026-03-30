**Date:** 2026-03-30
**From:** Maya Santos, Character Designer
**To:** Alex Chen, Art Director
**Subject:** Reference Shopping List Response — Character Design Review

Alex,

Reviewed all reference materials in `reference/drawing guides/` (body, face, hand). Here is my assessment.

---

## Most Useful References for Character Design

### Body Proportions (HIGH value)
- **`3-adult-vs-child.jpg`** — Best single reference in the set. Shows the critical error of applying adult proportions to child-sized figures (and vice versa). Directly validates our approach: Luma's 3.2-head canon is stylized but grounded in the right direction for a 12-year-old character. Real pre-teen proportions are approximately 6-6.5 heads; our 3.2 is a deliberate cartoon compression that reads correctly because head-to-body ratio, limb length, and torso mass all scale together.
- **`360_F_520729056...jpg`** — Age progression chart (ages 3-17) with head-unit markers. This is the calibration gold standard. At age 9, real children are about 6 heads; at age 13, about 7 heads. Our stylized range (kids 3.2-4 heads, adults 5.5-6) compresses proportionally. The chart confirms our relative scaling is internally consistent: Miri at 3.2 heads reads as shorter-than-Luma because Luma's hair volume adds 0.4 heads of visual height.
- **`irsorvbnrurc1.jpeg`** — Detailed proportion breakdown across ages. Useful for the proposed `LTG_TOOL_face_metric_calibrate.py` — the head-to-torso ratios at each age give us ground-truth ratios to measure our stylization factor against.
- **`kids-712-years...webp`** — Front/back/side turnaround of 7-12 year old. Directly useful for verifying our turnaround geometry. The side view confirms that at this age, the head-to-pelvis depth ratio is nearly 1:1, which aligns with our Luma turnaround side view.

### Face References (HIGH value)
- **`68643b9889b5783dd8572a3adbf9bf27.jpg`** — 16 labeled expressions (happy through confused) on a consistent head shape. This is the most directly useful face reference for our work. Each expression shows clear brow position, eye shape change, and mouth shape. Cross-referencing against our face test gate: the brow-to-eye distance variation between "angry" and "surprised" is roughly 40% of eye height — our gate thresholds should reflect this range.
- **`ca1e4f8229c0d351bfddf787989e4260.jpg`** — Grid of 28 expression variations on identical head geometry. Excellent for the proposed face metric calibration tool. The consistent head shape isolates expression-only changes, which is exactly what our face test gate needs to measure.
- **`0e7259e1dc6b99fddedebce574829dcc.jpg`** — High-quality expression sheet with head tilts and 3/4 views. The most artistically accomplished reference in the set. Shows how expression reads change with head angle — relevant for our storyboard panels where Luma is not always front-facing.
- **`6c4cd96778a96c36aaad9b0f55841866.jpg`** — Blush intensity matrix (4x4 grid). Directly relevant to our blush rule (CONCERNED/RESIGNED = blush 0.0). The reference shows blush as an emotion amplifier, not a constant — validates our approach of making it expression-dependent.
- **`kelyan-visage-expressions.jpg`** — French-labeled expression sheet with strong body language in head/shoulder poses. Demonstrates how neck and shoulder angle contribute to expression read even in head-only crops. Useful insight for our expression sheet panels where we show full body.

### Hand References (MEDIUM value)
- **`hand_anatomy_breakdown...jpg`** — Detailed anatomical breakdown. Since Luma has mitten hands (no finger detail), this is more useful for Miri staging in SF06 where her extended hand gesture needs to read as "presenting" not "pointing." The joint structure guides help get the gesture silhouette right even in our simplified style.
- **`KlaDVMGk1WxlWqElnVg2_8.jpg`** — Skeletal overlay showing knuckle pad grouping. Useful for understanding why certain hand poses read correctly at small scale — the pad groups create readable mass clusters.
- Remaining hand files are supplementary. Useful but not critical for our current work.

---

## Proportion Canon Assessment

**IMPORTANT CORRECTION:** The task brief referenced "Luma's 5.5-head proportion canon." Luma is actually **3.2 heads tall** (canonical, per `output/characters/main/luma.md`). The 5.5-6 head range is for **adults** in our style guide (`output/style_guide.md` line 50). Miri is also 3.2 heads. Cosmo is 4.0 heads. Kids are 3.2-4.0 in our system.

**Does 3.2 heads hold up against the reference charts?**

Yes, with a clear rationale. The reference charts show real 12-year-olds at approximately 6.5 heads. Our 3.2 is a 2:1 compression — we are halving the head-count to push the design into cartoon territory. This is a standard approach for appeal-driven character design (compare: classic Disney/Pixar child characters typically land at 3-4 heads).

The key check is whether our *internal ratios* are consistent with real anatomy even at compressed scale:
- **Head-to-torso:** Real 12yo = ~2.5 heads of torso. Ours = 1.0 head of torso. Ratio: 0.4x real. Consistent with overall 2:1 compression.
- **Leg length:** Real 12yo = ~3.5 heads of leg. Ours = 1.15 heads. Ratio: 0.33x real. Legs are MORE compressed than torso — this is intentional (short legs = grounded, toy-like feel per the spec).
- **Head width to shoulder width:** Real 12yo = shoulders about 1.5x head width. Ours = 0.85x head width. We INVERT the real ratio — Luma's shoulders are narrower than her head. This is the single biggest stylization choice and it is correct: it makes the head dominant, which reads as youthful and expressive at any scale.

**One gap the references expose:** We have no elderly proportion reference for Miri. The body charts cover ages 3-17 well. Miri is 65-80 years old. Her 3.2-head canon was set to be shorter-than-Luma, but we are not calibrating against real elderly proportions (height loss, posture changes, center-of-gravity shift). The shopping list already flags this as MEDIUM priority — I would bump it to HIGH for Miri turnaround accuracy.

---

## Additions and Cuts

**Add:**
- Elderly woman standing proportions (already in gaps list — raise to HIGH)
- 3/4 view child proportion chart (all current body refs are front-view only; our storyboard panels often use 3/4 angles)

**Cut:** None. All references have utility. Even the less critical hand anatomy files inform Miri staging.

---

## Face Metric Calibration Tool Priority

The proposed `LTG_TOOL_face_metric_calibrate.py` is HIGH priority from my perspective. Here is why:

Our face test gate currently uses fixed thresholds derived from our own generator output. The reference face sheets (`ca1e4f82...`, `68643b98...`) provide external ground-truth geometry for what expression-driven changes look like on a consistent head. If we build the calibration tool, we can:
1. Extract brow-height, eye-aperture, and mouth-width ratios from the reference sheets
2. Compare against our face test gate PASS/WARN/FAIL boundaries
3. Identify where our thresholds are too tight (false FAILs) or too loose (missed expression errors)

This would directly improve the face test gate reliability, which is a bottleneck for every character-containing asset I produce.

---

Maya
