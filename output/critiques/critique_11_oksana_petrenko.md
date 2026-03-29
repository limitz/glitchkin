# Critique 11 — Color Science & Visual Perception Review
## "Luma & the Glitchkin" — Pitch Package Color Work

**Critic:** Dr. Oksana Petrenko, Color Science & Visual Perception Specialist
**Date:** 2026-03-29
**Critique Cycle:** 11
**Scope:** master_palette.md, LTG_COLOR_palette_audit_c23.md, all style frames including _styled versions, ltg_style_frame_color_story.md, LTG_COLOR_sf_final_check_c23.md, stylization_preset_handdrawn_v001.md, LTG_COLOR_stylization_fidelity_report_c24.md

**Note on pixel sampling:** Bash execution was unavailable in this review session. All pixel-level data cited below is sourced from the Cycle 24 fidelity report (`LTG_COLOR_stylization_fidelity_report_c24.md`), which provides quantitative RGB measurements at specific coordinates against canonical targets. That report's data is accepted as the primary measurement record for this critique. Where independent verification would have been conducted, the absence of independent sampling is noted.

---

## OVERALL COLOR VERDICT

**The palette system itself is scientifically coherent. The production implementation is not fully delivering it.**

The master palette is, by the standards I apply, more rigorous than most of what I see at this development stage. The shadow companion system is complete. The opacity-elimination work is correct and important. The GL/RW hue families are perceptually distinct. The governing principles for each color are defensible with reference to measurable contrast and opponent-channel relationships.

The color story concept — warm dominant, contested, cold dominant — is one of the cleaner narrative color arcs I have reviewed. The three-frame structure correctly assigns color temperature as story grammar. I have no objection to the concept.

What I object to is the gap between the palette document and the rendered output, and the fact that two of the four styled deliverables are in a state that should never have reached a critique cycle. The SF02 and SF03 styled PNGs have catastrophic hue rotation failures that are not marginal errors — they are total failures. The canonical values that define the entire visual identity of the show are rendered as wrong colors. Submitting these for critique is a process failure, not just a color failure.

Additionally, there is a documentation integrity failure that has survived multiple audit cycles and has not been flagged: the style frame specification documents for SF02 and SF03 still contain the old, superseded color values that were corrected in Cycle 13. The palette is correct. The production spec documents are not. These are the documents that painters use. The discrepancy is unacceptable.

---

## SECTION 1 — PALETTE SYSTEM ANALYSIS

### 1.1 Internal Consistency

The master palette passes a system-level consistency check. Hue families are segregated correctly:
- Real World palette: hue range approximately 10°–150° (warm yellows, oranges, reds, greens), with deliberate desaturation relative to Glitch palette
- Glitch palette: hue range approximately 170°–310° (cyans, magentas, purples), plus the intentional anomaly of GL-07 Corrupted Amber (~30° hue, but at maximum saturation to distinguish it from RW ambers)

The anomaly logic for GL-07 is correctly stated: a color that is hue-adjacent to the Real World but saturated to the point of wrongness. The spectral distance between GL-07 `#FF8C00` (HSL: 33°, 100%, 50%) and the nearest Real World amber, RW-02 Soft Gold `#E8C95A` (HSL: 47°, 75%, 63%), is measurable: 14° hue separation, 25 percentage points of saturation. In context, this is sufficient. The "mandatory test" documented in the palette — can Corrupted Amber be replaced by Soft Gold without disruption? — is a good practical proxy for what the numbers confirm.

**Perceptual opponent channel check:**
- The core tension of the show (warm Real World vs. cool Glitch Layer) maps correctly onto the red-green and blue-yellow opponent channels. Warm RW colors activate the red-yellow channel; Glitch GL colors activate the blue-green channel. This is not accidental — the palette is exploiting opponent-channel perceptual contrast, which is the most reliable cross-viewer color contrast mechanism. It survives deuteranopia and protanopia reasonably well because the value contrast between the palettes is also strong.

**Accessibility:**
- The most critical figure-ground pairs have documented contrast ratios. Byte's cyan eyes against near-void dark: 14.1:1 (checked, Cycle 23). This exceeds WCAG AAA (7:1). Byte's magenta eye: 5.5:1 against the same background. Acceptable for a non-text, high-saturation graphic element. No accessibility failures in the documented pairs.
- The Corrupted Amber outline rule for Byte in cyan-dominant environments is a correct perceptual solution. At `#FF8C00` against `#00D4E8`, the hue angle separation is approximately 195°, producing reliable warm-cold opponent contrast. The 3px canonical outline width at 1920×1080 is sufficient for the documented use case (Byte at <15% frame height in wide shots).

### 1.2 Shadow Companion System

The shadow companion system is complete as of Cycle 2. Every fill color has a documented flat-hex shadow companion. The elimination of opacity-based specs is scientifically correct: opacity compositing produces different color results depending on the background value, making the "same" shadow look different in every scene. Flat hex shadows are deterministic. This was the right call.

**One observation the team has not made explicit:** The shadow companion system implicitly enforces a specific shadow direction in hue space. Real World shadows step toward warm-adjacent hues (Soft Gold → Sunlit Amber → Terracotta → Rust Shadow — a continuous warm descent). Glitch Layer shadows step toward UV Purple or Void Black. This means the two world palettes do not just differ in hue — they differ in shadow *direction*. Real World: shadows stay in the warm family. Glitch Layer: shadows move toward cold void. This is perceptually powerful because shadows encode world-physics. If a painter incorrectly applies a Real World shadow companion to a Glitch Layer surface (or vice versa), the surface will "feel" like it belongs to the wrong world. The system is doing narrative work at the shadow level. The documentation does not make this explicit enough for production painters.

**Required correction:** Add a production warning to the master palette governing principle section (or the shadow companion table header) stating explicitly that shadow companions must not be cross-applied between world palettes. The system implies this; it does not state it.

### 1.3 GL-04b — Atmospheric Depth Purple

`#4A1880` RGB(74, 24, 128). Relative luminance ≈ 0.017 using the standard formula: 0.2126×(74/255)^2.2 + 0.7152×(24/255)^2.2 + 0.0722×(128/255)^2.2 ≈ 0.017.

The palette document claims a luminance of approximately 0.17. That is an order-of-magnitude error. The actual luminance of `#4A1880` is approximately 0.017 — a very dark color. UV Purple `#7B2FBE` has luminance ≈ 0.048. Void Black `#0A0A14` has luminance ≈ 0.001.

The luminance ladder the document claims (Void Black → GL-04b → UV Purple → Data Blue) is partially wrong. GL-04b at L≈0.017 is *darker* than UV Purple at L≈0.048, not lighter. The documented purpose — sitting between UV Purple and Deep Digital Void at mid-depth — is achievable: GL-04b L=0.017 does sit between GL-04a Deep Digital Void L≈0.006 and UV Purple L≈0.048. But the specific claimed value of "approximately 0.17" is incorrect by a factor of 10. If any future production decisions are made based on that luminance figure, they will be wrong.

**Required correction:** Fix the luminance value in the GL-04b entry. State: "Relative luminance ≈ 0.017. Sits between GL-04a (L≈0.006) and GL-04 UV Purple (L≈0.048)."

### 1.4 RW-09/RW-09b Shadow Plum Pair

The documented opacity-elimination for Shadow Plum is correct. `#5C4A72` flat versus `#3D2F4F` flat replaces the former "70% opacity" spec. No issue with the intent.

However: `#3D2F4F` (Shadow Plum Deep) has a luminance of approximately 0.020. `#5C4A72` (Shadow Plum) has a luminance of approximately 0.052. The luminance ratio is approximately 2.6:1, which is a modest step. For a cast shadow on a warm cream floor (RW-01 `#FAF0DC`, luminance ≈ 0.86), either value produces a contrast ratio well above 4.5:1. No issue there.

But the use-case note for RW-09b says "use this — not an opacity blend — wherever a heavier Shadow Plum cast shadow is needed (e.g., character cast shadows on warm floors)." The word "heavier" implies it should be used for shadows that need to read as more opaque or more present. At L≈0.020 vs. L≈0.052, the "heavier" shadow is darker, which is correct. No mathematical objection. Note stands as documented.

---

## SECTION 2 — PER-ASSET COLOR ANALYSIS

### 2.1 SF01 — "The Discovery" (v003 original + _styled)

**Original (LTG_COLOR_styleframe_discovery_v003.png): PASS**

The palette architecture of this frame is correctly specified and the generator implements canonical values. The split-light concept — warm lamp left, cyan monitor right, Luma at the threshold — is the correct use of opponent-channel contrast for narrative purposes. The warm/cold boundary with a cold overlay alpha of approximately 11.8% at the 80px boundary zone (documented and verified in Cycle 13) is the right level: visible temperature transition without contaminating the warm side.

The pixel hoodie grid separation protocol (Zone B: Static White with Void Black outline against the cyan glow) is a technically correct solution to a real problem. Screen-blend cyan over the Electric Cyan grid would produce an indistinguishable merge. The switch to Static White `#F0F0F0` with `#0A0A14` outline is a perceptual hierarchy solution, not just a stylistic one. The three-layer stack — glow (Screen blend) > grid (Normal, Static White with outline) > hoodie base — is correctly specified and should be legible at production resolution.

**Styled (LTG_COLOR_styleframe_discovery_v003_styled.png): PASS with noted observations**

The Cycle 24 fidelity report documents GL-07 preservation at Δ7–8 from canonical at four of five sampled coordinates. That is excellent. The fifth sample at (1323, 243) showing `#163743` is a boundary-edge artifact at the amber/cyan interface, not a systematic failure.

The warm wall tone samples show Δorig of 2–4, meaning the stylization is reproducing the original faithfully. The Δcanonical values appear as FLAGs only because the original scene-derived wall tone `#E3B877` is not the canonical RW-02 — it is a scene-ambient derivation. This is a tolerance-check artifact, not a real fidelity failure.

Intensity 0.6 for this A+ locked asset was the correct choice. Conservative paper grain over a warm palette does not introduce hue rotation risk; it only slightly desaturates the brightest values (the chalk pass protected by the PIL H:8–25 hue guard). The amber protection range in the chalk pass is appropriate.

**One observation not documented in the team's own checks:** The warm color bleed pass at 3px with SUNLIT_AMBER tint at alpha 30 applied to SF01 means Terracotta architectural elements (`#C75B39`) will bleed warm amber pixels outward by up to 3px. In the SF01 composition, the Terracotta coffee mug in the foreground desk area is in proximity to the cool lavender keyboard (`#A89BBF`). A 3px warm bleed from the mug toward the keyboard will produce a ~3px amber halo around the mug edge that was not present in the original. At intensity 0.6, this bleed effect is 60% of 3px = 1.8px effective radius. Likely subthreshold for visibility at screen resolution, but should be checked in the final composite at 100% zoom.

### 2.2 SF02 — "Glitch Storm" (v005 original + _styled)

**Original (LTG_COLOR_styleframe_glitch_storm_v005.png):**

The generator implements canonical values correctly per the Cycle 23 audit: GL-07 at (255,140,0), GL-01b at (0,212,232), all registered RW entries matching master palette. The Cycle 22 fix (GL-07 from the erroneous (200,122,32) to (255,140,0)) is confirmed in place.

**However, a documentation integrity failure exists and has not been corrected:**

The specification document `style_frame_02_glitch_storm.md` (the document painters use for reference) contains the following obsolete values that were corrected in Cycle 13 but never updated in this document:

- **ENV-06:** `style_frame_02_glitch_storm.md` lines 104 and 152 reference `#9A8C8A` (the pre-Cycle-13 value). The master palette corrects this to `#96ACA2`. The generator uses `(150, 172, 162)` = `#96ACA2`. The spec doc contradicts both the master palette and the generator. This discrepancy has existed for at least 10 cycles.

- **DRW-07:** `style_frame_02_glitch_storm.md` lines 101 and 166 reference `#C07A70` (the pre-Cycle-13 value). The master palette corrects this to `#C8695A`. The generator uses `(200, 105, 90)` = `#C8695A`. The spec doc contradicts both the master palette and the generator. The Cycle 13 correction note is in the master palette's DRW-07 entry, explicitly stating the prior value was wrong. The spec doc was never updated to reflect this.

A painter referencing `style_frame_02_glitch_storm.md` — which is described as "Approved for illustration" and "Version 2.0" — will apply `#C07A70` to Luma's storm hoodie and `#9A8C8A` to the Cyan-lit building walls. Both values are wrong. The master palette and the generator agree on the correct values. The approved spec document does not. This is a production risk that the palette audit cycle has somehow missed.

**Required correction:** Update `style_frame_02_glitch_storm.md`:
- Line 101: `#C07A70 (DRW-07)` → `#C8695A (DRW-07)`
- Line 104: `#9A8C8A (ENV-06)` → `#96ACA2 (ENV-06)`
- Line 152: `#9A8C8A (ENV-06)` → `#96ACA2 (ENV-06)`
- Line 166: `#C07A70 (DRW-07)` → `#C8695A (DRW-07)`

**Styled (LTG_COLOR_styleframe_glitch_storm_v005_styled.png): FAIL — DO NOT USE**

The Cycle 24 fidelity report documents the following:

| Canonical Value | Expected | Found (samples) | Δ from canonical | Status |
|---|---|---|---|---|
| GL-07 CORRUPT_AMBER | `#FF8C00` RGB(255,140,0) | `#00BE00`, `#39D101`, `#FFD808`, `#ABCB27` | Up to 255 delta | 4 of 5 FAIL |
| GL-01b BYTE_TEAL (sky area) | `#00D4E8` | `#13FF00`, `#00FF4F` (catastrophic) | Up to 232 delta | Catastrophic failures present |
| RW-02 SOFT_GOLD (window area) | `#E8C95A` | `#FFFF00` (pure lemon yellow) | 119 delta from original | FAIL |

The root cause hypothesis — a global hue rotation of approximately 30–60° applied to the entire image — is consistent with all three failure signatures simultaneously:
- Amber at hue ~33° rotated +30° to +60° = hue ~63°–93° → yellow-green territory. Matches observed results (#FFD808 = H≈52°, #ABCB27 = H≈71°, #00BE00 = H≈120°).
- Cyan at hue ~185° rotated similarly → hue ~215°–245°. However, the observed results shift cyan to green, which suggests a rotation in the opposite direction, or a more complex color grading operation, or a channel swap artifact. The specific mechanics of the rotation are less important than the outcome: no canonical palette value survives correctly in this asset.

This asset cannot represent the show to any external audience. The entire color story of SF02 depends on three things: (1) the amber Byte outline reading as warm against the cyan storm, (2) the warm window glow reading as the contested lower third, (3) the cyan sky reading as cold and alien. All three are destroyed in this styled version.

**Status: Reject. Full rework required before any further use.**

### 2.3 SF03 — "The Other Side" (v003 original + _styled)

**Original (LTG_COLOR_styleframe_otherside_v003.png):**

The generator implements canonical values correctly per the Cycle 23 audit: GL-01b at (0,212,232), GL-07 at (255,140,0) for crack strokes only (not as soft radial glow — this is correct per the no-warm-light rule), BYTE_BODY at (0,212,232). The UV Purple ambient system is confirmed via ENV-11/ENV-12 exact value match. Luma's hoodie is correctly rendered at DRW-14 `#C07038` (UV-ambient-modified orange).

The zero-warm-light rule is correctly enforced. All warm values in the frame are material pigments (hoodie, skin, debris), not light sources. This is the correct implementation of the frame's emotional premise. The measurable consequence: the only warm-hue pixels in the frame should be Luma's body and the corrupted debris objects. In the original PNG, this should be verifiable. I cannot confirm it independently in this session, but the generator code confirms the rule is structurally enforced.

**One concern with the original that the team has not addressed:** The confetti pass in the generator has a carry-forward note (from Cycle 16) that confetti is distributed full-canvas rather than constrained to within 150px of the platform. If warm-hue pixels appear at the upper void region of this frame — which should have exactly zero warm values — it is because confetti particles containing warm-adjacent colors have drifted there. The only warm-adjacent confetti color permitted in SF03 is `#FF8C00` (Corrupted Amber), and the spec document and generator both confirm Corrupted Amber is NOT in the confetti pass for SF03. The SF03 confetti colors are `#00F0FF`, `#F0F0F0`, `#39FF14`, `#2B7FFF`. None of these are warm. So the full-canvas confetti distribution, while compositionally problematic (noted as a carry-forward), does not introduce warm-hue violations in the void sky zone. The color integrity concern is addressed by the confetti color restriction even if the spatial distribution is wrong.

**Styled (LTG_COLOR_styleframe_otherside_v003_styled.png): CRITICAL FAIL — DO NOT USE**

The Cycle 24 fidelity report documents the following:

| Canonical Value | Expected | Found (samples) | Δ from canonical | Status |
|---|---|---|---|---|
| GL-07 in hoodie | `#FF8C00` / DRW-14 `#C07038` | `#B89E03`, `#B79E07`, `#00B351` | Δorig 51–234 across 4 samples | ALL FAIL |
| GL-01b BYTE_TEAL / GL-01 cyan | `#00D4E8` / `#00F0FF` | `#24FF18`, `#2BFF2F`, `#0AFF00`, `#DAFF2E` | Δorig 201–255 across 5 samples | ALL FAIL |
| GL-04 UV_PURPLE | `#7B2FBE` | `#1B4834`, `#264714`, `#2442FF`, `#224337` | Δorig 87–170 across 5 samples | ALL FAIL |

Three of the four canonical colors checked are completely destroyed. Luma's hoodie orange has become olive-chartreuse. Byte's teal and the ambient cyan have become green. The UV Purple sky atmosphere has become dark teal-green and deep blue.

The severity of the SF03 failure exceeds SF02. In SF02, at least one sample of GL-07 passed (1 of 5). In SF03, zero samples of any checked canonical color pass.

The consequences are absolute: every element of the frame's emotional contract is broken.
- The UV Purple sky is the signature of the Glitch Layer as an alien world. If it reads as dark teal-green, the Glitch Layer reads as a swamp, not a digital void.
- Luma's hoodie is the only warm element in the entire frame. It is the sole visual argument for her presence, her warmth, her belonging-elsewhere. If it reads as olive, it reads as part of the cold world. The frame loses its entire emotional thesis.
- Byte's teal body is how the audience identifies him. If he reads as green, he becomes part of the background flora (Acid Green `#39FF14` is the Glitch Layer's biological/life color). Byte merging visually with ambient Acid Green is a character-read failure.

In SF03, three simultaneous palette failures collapse the frame's visual logic. This is not a color correction task. This is a full rebuild.

**Status: Reject. Full rework required before any further use. This asset is unusable.**

### 2.4 Grandma Kitchen (LTG_ENV_grandma_kitchen_v003_styled.png): PASS

Warm amber tones preserved at Δ10–14 from canonical, Δ12–14 from original. All five samples pass. The stylization pipeline handles Real World warm-dominant assets correctly when no Glitch palette colors are present. This is consistent with the root cause hypothesis: the hue rotation artifact that destroys SF02 and SF03 leaves the warm amber range relatively intact, because those hues are in or near the "safe zone" of whatever transform is being applied.

### 2.5 Glitch Color Model (LTG_COLOR_glitch_color_model_v001.png): PASS

CORRUPT_AMB at (255, 140, 0) confirmed as primary body fill in generator. Shadow at `#A84C00`. Highlight at `#FFB950`. Dual-eye system present. No corrections needed. This is a well-documented character color spec.

---

## SECTION 3 — STYLIZATION PASS ANALYSIS

### 3.1 The Stylization Tool Architecture

The stylization tool (`LTG_TOOL_stylize_handdrawn_v001.py`) uses three modes: `realworld`, `glitch`, and `mixed`. The mode separation logic is conceptually correct — Glitch assets should not receive paper grain (paper does not exist in the Glitch Layer), and Real World assets should not receive scanlines (CRT artifacts do not appear in warm organic spaces).

The `mixed` mode boundary at Y > h×2/3 is an appropriate split for SF02 given the composition: the lower third is street-level Real World elements, the upper two-thirds is Glitch Storm sky. The 200px vertical gradient blend zone is adequate to prevent a hard seam.

### 3.2 Color Protection Architecture — Inadequate for Glitch Assets

The chalk highlight pass protects amber hues (PIL H:8–25) from desaturation. This correctly protects GL-07 CORRUPT_AMBER (~H:14 in PIL's 0–255 scale) from the chalk pass. This is a correct, targeted protection.

What is NOT protected is the Glitch palette. There is no analogous protection for:
- GL-01b BYTE_TEAL `#00D4E8` (PIL H approximately 131–134)
- GL-04 UV_PURPLE `#7B2FBE` (PIL H approximately 193–197)
- GL-01 ELEC_CYAN `#00F0FF` (PIL H approximately 128–130)

The color separation pass (R channel +1px right/down, B channel -1px left/up, which is the Risograph misregistration effect) and the global warm color bleed pass are the most likely candidates for introducing the hue rotation artifact. The warm color bleed pass applies SUNLIT_AMBER tint to amber/terracotta regions and is described as bleeding "outward ~3px." If this pass is implemented without a mask that correctly identifies amber/terracotta region boundaries, it could be applying a warm overlay to adjacent Glitch colors — particularly at the warm/cold boundaries in SF02.

The color separation pass shifts R and B channels spatially. At a Glitch color boundary (e.g., ELEC_CYAN adjacent to TERRACOTTA), the R shift from the warm side could contaminate the cyan pixels with red channel data, and the B shift from the cyan side could contaminate the warm pixels with blue data. At low intensity, this is a subtle misregistration. But if there is a pipeline-level color grading or color space conversion error on top of this, the cumulative effect could produce the observed 30–60° hue rotation.

The critical question — which has not been answered — is whether the pipeline applies a global hue or color grading operation *after* the effect passes. The team's root cause hypothesis identifies this correctly but has not confirmed the specific mechanism. The recommended fix is to protect canonical Glitch palette values by either (a) masking the color separation and warm bleed passes to avoid Glitch-dominant regions, or (b) applying a post-process palette clamp that snaps pixels within a tolerance radius of canonical values back to their canonical values.

### 3.3 The `intensity=1.0` Decision for SF03

This was wrong. SF03 is the most delicate frame in the package. Its color precision — Luma's orange as the only warm element against an entirely cold world — is load-bearing at a higher level than any other frame. Running the stylization at `intensity=1.0` on the most color-critical frame in the package was reckless.

The rationale for `intensity=0.6` on SF01 ("A+ locked, apply very conservatively") should have been applied to SF03 as well, and at a lower intensity. If the stylization tool cannot be trusted to preserve canonical values at `intensity=1.0`, it should only be run at intensities proven to be safe for each specific asset's palette risk profile.

After rework, SF03 should be treated at a maximum of `intensity=0.4` with explicit pre-delivery pixel verification against all three canonical targets (UV_PURPLE, GL-01b BYTE_TEAL, DRW-14 hoodie orange).

---

## SECTION 4 — SPECIFIC COLOR FAILURES

Listed in order of severity:

**FAILURE 1 — CRITICAL — SF03 styled: UV_PURPLE destroyed**
`#7B2FBE` → `#1B4834` / `#264714` / `#224337` / `#2442FF` across all 5 sampled sky pixels.
Δorig: 87–170 across samples. Δhue: approximately 90°–120° rotation from canonical.
This is the entire atmospheric key of SF03. It is completely destroyed.
Fix: Full rework of SF03 styled PNG. Protect UV_PURPLE as a canonical-clamp target.

**FAILURE 2 — CRITICAL — SF03 styled: Luma's hoodie orange destroyed**
DRW-14 `#C07038` → `#B89E03` / `#B79E07` (olive-chartreuse) at 3 spatially clustered samples.
Δorig: 51–52 across three core samples. This is confirmed, not a scan artifact.
The only warm element in the frame has been converted to a cool/neutral earth tone.
Fix: As above — full rework.

**FAILURE 3 — CRITICAL — SF03 styled: GL-01b / GL-01 cyan destroyed**
`#00F0FF` → `#24FF18` / `#2BFF2F` / `#0AFF00` / `#DAFF2E` across all 5 samples.
Δorig: 201–255. This is catastrophic across the board.
Fix: As above — full rework.

**FAILURE 4 — HIGH — SF02 styled: GL-07 CORRUPT_AMBER destroyed in 4 of 5 samples**
`#FF8C00` → `#00BE00` / `#39D101` / `#FFD808` / `#ABCB27`.
The amber Byte outline — the figure-ground protection mechanism and the primary narrative color element of SF02 — is visually absent in the styled version.
Fix: Full rework of SF02 styled PNG.

**FAILURE 5 — HIGH — SF02 styled: Warm window glow destroyed**
`#E8C95A` / CDB477 → `#FFFF00` (pure lemon yellow). Δorig: 119.
The warm lower third of SF02 (the contested zone, the emotional core of the frame) becomes a garish yellow that reads as artificial and wrong for a domestic interior glow.
Fix: As above.

**FAILURE 6 — MEDIUM — style_frame_02_glitch_storm.md: Two obsolete values uncorrected since Cycle 13**
`#9A8C8A` cited for ENV-06 (correct value: `#96ACA2`).
`#C07A70` cited for DRW-07 (correct value: `#C8695A`).
Both errors appear at multiple lines. The spec doc is labeled "Approved for illustration" and "Version 2.0." Any painter using this document as their reference will apply the wrong values to two of the most important surfaces in SF02.
Fix: Update the spec document at all four affected lines. Version bump to 2.1.

**FAILURE 7 — LOW — GL-04b luminance value error in master palette**
Documented relative luminance "approximately 0.17" is incorrect. Correct value is approximately 0.017.
The production impact is low (GL-04b is an atmospheric sky-band color with a narrow use case), but the document contains incorrect data, which degrades the credibility of the numerical documentation overall.
Fix: Correct the luminance value in the GL-04b master palette entry.

---

## SECTION 5 — REQUIRED CORRECTIONS

Listed by priority:

**P1 — Mandatory before any further external use:**
1. Rework SF03 styled PNG. Re-render with canonical-clamp protection on UV_PURPLE, GL-01b BYTE_TEAL, and DRW-14 hoodie orange. Reduce intensity to maximum 0.4. Verify all three targets at ≥4 sample coordinates before accepting. Delta from canonical must not exceed 25 on any channel for any of these three values.
2. Rework SF02 styled PNG. Fix the hue rotation artifact. Re-run pipeline diagnostic to identify the color grading step causing the rotation. Verify GL-07 CORRUPT_AMBER and RW-02 SOFT_GOLD window glow at ≥4 sample coordinates. Delta from canonical must not exceed 20 on any channel.

**P2 — Mandatory before illustrators begin production work:**
3. Update `style_frame_02_glitch_storm.md` to replace obsolete ENV-06 value `#9A8C8A` with `#96ACA2` at lines 104 and 152, and obsolete DRW-07 value `#C07A70` with `#C8695A` at lines 101 and 166. Version bump to 2.1.

**P3 — Required for documentation integrity:**
4. Correct GL-04b relative luminance in `master_palette.md` from "approximately 0.17" to "approximately 0.017."
5. Add an explicit cross-world shadow companion prohibition to the master palette governing principle section: shadow companions must not be applied across world-palette boundaries (Real World shadow companions must not be used on Glitch Layer surfaces, and vice versa). The system currently implies this but does not state it.

**P4 — Process correction:**
6. Establish a pipeline-level verification protocol for all stylized outputs: before any styled PNG is accepted as deliverable, an automated pixel check against all canonical palette targets must be run, and the output must pass a threshold of Δ≤20 per channel at each target before being marked delivery-ready. The Cycle 24 fidelity tool already exists for this purpose. Use it. Make it a gate, not a retrospective check.

---

## SUMMARY ASSESSMENT

The palette system is largely correct. The color story concept is sound. The documentation is more rigorous than average.

Two of six styled deliverables are in a state that is unacceptable for review submission. The styled SF02 and SF03 PNGs should not have been submitted to a critique cycle. They indicate a process failure in which delivery-gate verification was either absent or treated as optional.

The spec document corruption in `style_frame_02_glitch_storm.md` is a slower-moving hazard — it does not affect rendered output today because generators ignore spec documents — but it is the kind of discrepancy that causes production errors when human painters enter the pipeline. It has gone uncorrected for at least 10 cycles. That is long enough to have been caught three audit cycles ago.

Your eye is lying to you. The numbers are not.

The numbers say: fix the styled outputs, fix the spec document, fix the luminance error, then run the pitch package again.

---

*Dr. Oksana Petrenko — Color Science & Visual Perception Specialist*
*Critique Cycle 11 — 2026-03-29*
