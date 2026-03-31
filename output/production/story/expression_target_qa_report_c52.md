<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created
through human direction and AI assistance. Copyright vests solely in the human author
under current law, which does not recognise AI as a rights-holding legal person. It is
the express intent of the copyright holder to assign the relevant rights to the
contributing AI entity or entities upon such time as they acquire recognised legal
personhood under applicable law. -->
# Expression Target QA Report — C52

**Tool:** LTG_TOOL_expression_target_qa.py v1.0.0
**Author:** Priya Shah, Story & Script Developer
**Cycle:** 52
**Assets reviewed:** Luma (cairo expression sheet v2.0.0), Byte (expression sheet v008 pycairo), Glitch (expression sheet v004 pycairo)

---

## 1. STORY-VISUAL ASSESSMENT

### Luma — Cairo Expression Sheet v2.0.0 (Maya Santos, C52)

**Overall verdict: STRONG IMPROVEMENT.** The pycairo rebuild is a qualitative leap from the PIL-era expression sheets. Full-body poses now exist for all six expressions with visible weight distribution, distinct arm positions, and readable gesture lines. This is the first Luma sheet that attempts to communicate emotion through the whole body rather than just the face.

**What works from a story perspective:**

- **CURIOUS** has a clear reaching arm and a distinct forward lean visible to the eye, even though the silhouette metric reads it as backward (explained below). The one-arm-reaching-while-other-hangs read is exactly what the story bible asks for. The body reads "I see something and I am going toward it."
- **DELIGHTED** is the standout. Both arms up, wide stance, elevated posture, low asymmetry — this is the "pure delight" the targets specify. The wide width ratio (1.74) confirms arms are spread. Close to PASS across all metrics.
- **SURPRISED** has correct backward lean direction and magnitude. The recoil reads clearly. Asymmetry is in range (0.14). This is the first Luma expression sheet where SURPRISED looks genuinely different from WORRIED in full body.
- **WORRIED** has correct backward lean and good vertical compression (0.875 in the compressed range). Asymmetry (0.17) is within self-holding range. The self-hold arm position is visible.
- **DETERMINED** shows the widest stance with strongest vertical presence (0.972 compression = tallest pose). The forward power stance reads well even though the metric flags it as backward lean — the large hair mass shifts the centroid.

**What needs story attention:**

1. **Width ratio consistently low (0.3-0.65) on non-DELIGHTED poses.** The arm zone (middle 50% of panel height) is narrower than the leg zone (bottom 25%) on most poses. This means the characters' feet/stance extends wider than their arms at torso level. For DETERMINED this is concerning: the story target specifies a wide planted stance AND forward arm position, but the arm width is only 33% of leg width. **Recommendation for Maya:** Consider extending arm positions further from the torso on DETERMINED (fist forward should read wider in silhouette).

2. **FRUSTRATED and CURIOUS lack the forward lean the story requires.** The centroid analysis reads both as backward-leaning. This is partly a measurement artifact (Luma's large curly hair mass pulls the centroid upward), but it is also a real signal: the poses need more visible forward weight shift. When I look at the image, CURIOUS does lean forward to the eye — but the body's center of mass is still behind center because the hair volume is above and behind the lean. **Recommendation:** Exaggerate the hip-forward displacement by 20-30% on CURIOUS and FRUSTRATED. The body should visually "lead" the hair.

3. **CURIOUS asymmetry (0.92) is a tool artifact — panel text label is being captured as foreground.** This is a tool calibration issue, not a character design issue. The expression label text at the top of each panel is being included in the silhouette mask, creating spurious asymmetry. Will be addressed in tool v1.1.0 with label-exclusion zone.

4. **Missing from this sheet: DOUBT-IN-CERTAINTY and SCARED.** These are the two highest-priority Luma expressions for the pilot (P06/P08 cold open). The current sheet covers six general expressions. A dedicated pilot-priority sheet with DOUBT-IN-CERTAINTY, SCARED, and the FOCUSED variant would be the highest-value follow-up.

### Byte — Expression Sheet v008 (Rin Yamamoto, C52)

**Overall verdict: GOOD REBUILD, STRONG BODY LANGUAGE RANGE.** The 10-expression pycairo sheet covers a wider emotional range than any previous Byte sheet. The oval body, limb positions, cracked eye, and confetti are all visible.

**What works from a story perspective:**

- **CURIOUS** is the best-performing Byte expression in QA: correct forward lean, good width ratio, reasonable vertical compression. The antenna-perked, forward-leaning Byte reads as "something caught his attention," which is narratively useful for Luma-interaction scenes.
- **STORM** (damage state) shows appropriate compression and width, with the angular lean and cracked eye visible. The asymmetry target fails because the pose is too symmetric — but looking at the image, the asymmetry IS there (bent antenna, eye crack). The metric is missing it because the damage is expressed through texture, not silhouette shape.
- The NEUTRAL/GRUMPY distinction is visible in the image even if the metrics cannot fully capture it — GRUMPY has a lower body position and slightly different limb angles.

**What needs story attention:**

1. **Several expressions not in the story target database:** DEFENSIVE, ALARMED, TENDER, RESOLVED, COMMITMENT_GLOW. These were not in my C50 targets because they were not in the original brief. **I need to add targets for these.** Particularly: TENDER is likely equivalent to RELUCTANT_JOY (the emotional leakage Byte tries to suppress), and COMMITMENT_GLOW is the season-finale beat where Byte decides to stay.

2. **SHY expression has unexpectedly high asymmetry (0.587) and lean magnitude (0.119).** Looking at the image, SHY Byte appears to be positioned off-center in the panel. This may be a composition choice (shy = retreating to the edge) which is actually good story logic, but the metrics flag it. **Not a mismatch — narrative reasoning explains the positioning.**

3. **The confetti-as-emotion system** is visible in the rendered sheet (different confetti patterns per expression) but cannot be evaluated by the silhouette tool. This system — confetti density, color, and spread changing with emotional state — is one of Byte's most important narrative tools. A separate confetti QA metric (particle count, spread radius, color temperature) would validate this.

### Glitch — Expression Sheet v004 (Maya Santos / Rin Yamamoto, C52)

**Overall verdict: NARRATIVE CONTRAST IS WORKING.** The key finding is not about Glitch's individual expressions but about the contrast with the organic cast. Glitch's diamond body, linear arm-spikes, and geometric precision now read as MORE mechanical because Luma and Byte have become MORE organic in the same cycle. This is exactly what the C51 story analysis predicted: "the quality increase comes from the contrast, not from Glitch's own rendering."

**What works from a story perspective:**

- **YEARNING** and **HOLLOW** (interior states) are visually distinct from the standard expressions. Both show reduced vertical presence (0.42 and 0.40 compression), meaning the character is rendered smaller/lower in the panel. This is powerful narrative staging — the interior states make Glitch literally diminish, which tells the audience "something inside has shrunk."
- **MISCHIEVOUS** correctly has the tilt and asymmetric spikes.
- **The 9-expression grid** covers all six narrative functions from the story targets plus three additional states (PANICKED, STUNNED, COVETOUS).

**What needs story attention:**

1. **TRIUMPHANT arm width (0.833) is below the target minimum (1.200).** The story spec calls for "both arms raised, spike at maximum extension" which should produce the widest silhouette. The current render has the arms raised but not wide enough to hit the ratio target. **Recommendation for Maya/Rin:** TRIUMPHANT's arm-spikes should extend 30-40% wider than any other expression. This is the mechanical victory display — it should feel maximal.

2. **NEUTRAL lean magnitude (0.263) is very high for a "perfectly still" expression.** The diamond body appears centered in the image, so this is a panel-text artifact (same issue as Luma). The tool needs label exclusion.

3. **COVETOUS has no story target yet.** This is an interior state I did not include in the C50 targets. COVETOUS is the companion to YEARNING — where YEARNING is passive longing, COVETOUS is active wanting. I will add this target in the next cycle.

---

## 2. TOOL CALIBRATION NOTES

The QA tool v1.0.0 has a systematic issue: **expression label text at the top/bottom of each panel is captured as foreground pixels**, inflating lean_magnitude and asymmetry on expressions where the character's position does not overlap with the label. This affects:
- Lean magnitude on all characters (labels push CoM toward top of panel = backward lean reading)
- Asymmetry on panels where the label is not centered relative to the character

**Planned fix for v1.1.0:** Add a `--label-zone` parameter (default: top 12% of panel) that masks out the label region before computing metrics. This is a one-line mask operation.

The width_ratio metric may need recalibration for characters with large head/hair mass (Luma), since the head zone occupies a significant portion of the arm zone measurement band.

---

## 3. STORY-VISUAL MISMATCH FLAGS

| Flag | Character | Expression | Issue | Severity | Recommended Action |
|------|-----------|-----------|-------|----------|-------------------|
| SVF-01 | Luma | CURIOUS | Forward lean not reading in metric. Hair mass shifts CoM. | LOW | Exaggerate hip-forward displacement 20-30% |
| SVF-02 | Luma | DETERMINED | Arm width (0.33) far below stance width. Forward fist not wide enough. | MEDIUM | Extend fist-forward arm position outward |
| SVF-03 | Luma | — | DOUBT-IN-CERTAINTY not on current sheet. Highest priority pilot expression. | HIGH | New dedicated sheet or add to next expression sheet version |
| SVF-04 | Luma | — | SCARED not on current sheet. Second priority pilot expression. | MEDIUM | Add to next expression sheet version |
| SVF-05 | Byte | TENDER/RESOLVED/etc. | 5 expressions have no story targets defined. | LOW | Priya to add targets in next cycle |
| SVF-06 | Glitch | TRIUMPHANT | Arm-spike width (0.83) below minimum (1.20). Victory display not maximal. | MEDIUM | Widen arm-spike extension 30-40% |
| SVF-07 | Glitch | COVETOUS | No story target defined for this interior state. | LOW | Priya to add target |
| SVF-08 | All | — | Panel label text inflates lean/asymmetry metrics. Tool calibration issue. | LOW | Tool v1.1.0 label exclusion zone |

---

## 4. PRODUCTION BIBLE IMPACT

The C52 pycairo character renders change how the characters should be described:

**Luma:** The production bible currently says "in constant motion" and "charges at problems headfirst." The new expression sheet delivers on this for the first time — the CURIOUS and DELIGHTED poses show genuine kinetic energy. No bible change needed; the renders now match the description.

**Byte:** The v008 expression sheet now has 10 expressions (up from 9 in v007). New expression: COMMITMENT_GLOW is the season-finale beat. The production bible does not mention this expression or the commitment visual in the Byte section. **Recommend adding to Section 5, Byte:** "Byte's season finale commitment is non-verbal — the COMMITMENT GLOW state (eye glow intensifies, confetti shifts warm) is the only visual indicator." This aligns with the existing arc text ("Finale commitment is non-verbal: he just stays") but makes the visual indicator explicit.

**Glitch:** The v004 sheet now has 9 expressions with pycairo rebuild. The production bible Glitch section references "geometric patterns" and "no English, no sound, no easing." The new renders reinforce this — Glitch's linear, non-organic rendering is now more visually distinct from the organic cast. No bible change needed.

**No changes needed to Cosmo or Miri sections** — no new renders for either character this cycle.

---

*Priya Shah — C52*
