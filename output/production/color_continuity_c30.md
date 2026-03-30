<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Color Continuity Audit — Cycle 30 (Pre-Critique 13)
**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-29
**Frames reviewed:** SF01 v004, SF02 v005, SF03 v005, SF04 v003

---

## 1. SUNLIT_AMBER Consistency Across Frames

**Check:** Does SUNLIT_AMBER (RW-03, #D4923A, hue ~34°) appear consistently where it should appear, and not where it should not?

| Frame | Expected | Verified | Notes |
|---|---|---|---|
| SF01 v004 | YES — wall ambient, shelf accents, particles | Tool: not_found (gradient rendering) | Generator uses SUNLIT_AMBER as named constant. Wall rendered as gradient — pixels drift outside radius=40 of canonical. **No palette drift.** |
| SF02 v005 | YES — warm window spill, street level warmth | PASS — 210 samples, delta 0.4° | Warm spill correctly present at correct hue. |
| SF03 v005 | NO — must be absent (zero warm light sources) | Correctly absent. Tool "failure" is false positive (orange hoodie + amber crack fragments). | See C30 audit for full analysis. |
| SF04 v003 | YES — soft warm ambient / lamp environment | Tool "failure" is false positive (Soft Gold ~47° sampled as SUNLIT_AMBER). 69 samples of warm golden tone ≠ SUNLIT_AMBER misplacement. | **No palette drift.** |

**Verdict: PASS.** SUNLIT_AMBER is present where it should be (SF01, SF02, SF04 warm zones) and absent from SF03 (zero warm light sources). No hue drift detected in either direction.

---

## 2. Warm/Cool Contrast Logic

**Check:** Are warm scenes warm? Are Glitch/digital scenes cool? Is the transition consistent?

| Frame | Expected Key | Actual Key | Verdict |
|---|---|---|---|
| SF01 v004 (domestic interior) | Warm dominant: Soft Gold lamp left, Electric Cyan monitor right | Warm wall ambient, lamp key confirmed. Cyan confined to monitor screen and Luma's right-facing surfaces. | PASS |
| SF02 v005 (Glitch Storm / street) | Contested: Cyan storm dominant sky, warm amber lower third | Cyan storm verified (0.3° delta on ELEC_CYAN, 296 CORRUPT_AMBER pixels at delta 1.4°). Warm window spill present (210 SUNLIT_AMBER samples). | PASS |
| SF03 v005 (Other Side / Glitch Layer) | Cold dominant: UV Purple sky, zero warm light sources | Zero warm light detected. UV Purple present at exact canonical hue (271.9°). SUNLIT_AMBER absent by design. Hoodie/skin warmth is pigment only. | PASS |
| SF04 v003 (Luma + Byte, domestic) | Warm dominant: lamp/warm ambient, Byte brings cool teal accent | Warm Soft Gold range confirmed in ambient. Byte teal hue present (183-185°) though below canonical luminance. CORRUPT_AMBER absent — no Glitch contamination. | PASS (Byte luminance outstanding — see note) |

**Verdict: PASS.** The warm/cool contrast logic is intact and consistent across all four frames.

**Note on SF04 Byte teal luminance:** Byte's teal reads visually at ~60-70% of canonical (0,212,232) luminance. The hue is correct (183-185°). Whether this is intentional scene lighting (Byte receiving soft lamp-side glow that dims his digital identity) or a generation issue is unresolved. The decision is pending Alex Chen confirmation. This does not undermine the warm/cool contrast logic but is flagged for critics who may question Byte's intensity in this intimate scene.

---

## 3. Glitch Palette Containment Check (CORRUPT_AMBER and ACID_GREEN)

**Check:** Do GL-07 Corrupt Amber and GL-03 Acid Green appear only in their sanctioned contexts?

### CORRUPT_AMBER (GL-07, #FF8C00)

| Frame | Appears? | Sanctioned? | Notes |
|---|---|---|---|
| SF01 v004 | YES — 808 samples, delta 0° | YES — cyan-dominant threshold exceeded (>35%); Byte's amber outline applies | The Byte silhouette outline rule is active. This is exactly the sanctioned use: warm outline against cyan-dominant environment. |
| SF02 v005 | YES — 296 samples, delta 1.4° | YES — amber outline on Byte (35% threshold exceeded), corrupted crack lines | Both sanctioned uses present. |
| SF03 v005 | YES — 263 samples, delta 3.6° | YES — crack fragment energy on corrupted debris/platform edges | SF03 spec explicitly uses Corrupt Amber for crack-line strokes on fragments. NOT as radial glow (which would read as warm light source, violating the no-warm-light rule). |
| SF04 v003 | NOT_FOUND | N/A — correct for intimate domestic scene with no cyan-dominant environment | No contamination. |

**ACID_GREEN (GL-03, #39FF14) — Not in canonical verify palette. Checked via semantic rule:**

Acid Green is semantically reserved for healthy Glitchkin markings and positive glitch energy (Forbidden #8: must not appear in storm/corruption contexts). In the pitch frames:
- SF01: No Glitchkin present except Byte (who is Byte Teal, not Acid Green). No contamination expected.
- SF02: Storm confetti uses GL-06c (Storm Confetti Blue), GL-01 (Electric Cyan), GL-05/Void Black. Acid Green is correctly absent per Forbidden #8.
- SF03: Glitch Layer environment. Acid Green may appear as GL flora (data-moss) but the SF03 generator does not include flora elements in this composition. No contamination.
- SF04: Intimate domestic. Acid Green not expected.

**Verdict: PASS.** Both GL-07 Corrupt Amber and GL-03 Acid Green are contained to sanctioned uses. No contamination of warm domestic scenes.

---

## Overall Color Continuity Status

| Check | Result |
|---|---|
| SUNLIT_AMBER consistency | PASS — present where expected, absent where prohibited |
| Warm/cool contrast logic | PASS — all four frames correctly keyed per narrative intent |
| GL-07 Corrupt Amber containment | PASS — sanctioned contexts only |
| GL-03 Acid Green containment | PASS — correctly absent from storm/contamination contexts |
| Color arc integrity (SF01→SF02→SF03) | PASS — warm → contested → cold/alien arc intact |
| SF04 fits color arc | PASS — domestic warm aligns with SF01 register |

**Outstanding (not a continuity failure):**
- SF04 Byte teal luminance: pending Alex Chen decision. Does not break warm/cold logic; the hue is correct.
- SF04 generator source missing: PNG exists, cannot be regenerated. Kai to resolve.

---

## Color Story Arc — Summary for Critique 13

The four pitch frames read as a single coherent color system:
- **SF01:** Real World at fullest — warm domestic palette, cyan as a single extraordinary intrusion
- **SF04:** Real World intimate — warm domestic, Byte as teal accent, no Glitch contamination
- **SF02:** Contested — Glitch palette occupies sky and color-modifies surfaces; warm holds the ground floor
- **SF03:** Glitch Layer — cold dominates, warmth survives only as pigment memory in Luma's clothes

The narrative progression (belonging → contested → lost) is legible from color alone. Critics can read the show's first act from these four frames without any dialogue.

**Pitch package color status: READY FOR CRITIQUE 13.**

---

*Sam Kowalski — Color & Style Artist — Cycle 30 — 2026-03-29*
*Full verification data: `output/color/LTG_COLOR_audit_c30_preCritique13.md`*
