# Critique 11 — Visual Effects, Lighting & Compositing
**Critic:** Nadia Okonkwo — VFX, Lighting & Compositing
**Project:** Luma & the Glitchkin — Pitch Package
**Date:** 2026-03-29
**Assets reviewed:**
- `output/color/style_frames/` — SF01 discovery, SF02 glitch_storm, SF03 otherside (originals + _styled)
- `output/backgrounds/environments/` — LTG_ENV_tech_den + _styled, LTG_ENV_grandma_kitchen + _styled
- `output/tools/LTG_TOOL_stylize_handdrawn.py`
- `output/tools/LTG_TOOL_render_lib.py`
- `output/production/stylization_preset_handdrawn.md`

---

## Overall FX / Lighting Verdict

**CONDITIONAL PASS — SEVEN TECHNICAL FAILURES REQUIRING CORRECTION BEFORE FINAL PITCH.**

The conceptual lighting architecture of this project is genuinely strong. The three-point warm/cyan/lavender model in SF01, the contested battlefield lighting of SF02, and the no-warm-light rule of SF03 are all coherent, purposeful, and correctly executed at the compositional level. The colour team understands what light is supposed to be *doing* narratively. That is the foundation.

The problems are in the execution layer: the stylization pipeline, the compositing tools, and several structural FX decisions that break the very lighting logic the colour team has built. The pipeline is treating stylization as a cosmetic pass. It is not. Every stylization operation is a compositing event, and every compositing event that does not respect the lighting structure of the frame is a lighting lie.

Seven failures. None are unfixable. Some will require a pipeline change. All must be addressed.

---

## Per-Asset Lighting Analysis

### SF01 — "The Discovery" (discovery_v003, discovery_v003_styled)

**Lighting concept: CORRECT. Execution: GOOD WITH ONE FAILURE.**

The three-source model — CRT cyan from the right, warm gold from the upper-left window, cool lavender ambient fill — is the strongest lighting setup in this package. The internal logic holds. Cyan washes the right-facing surfaces, warm gold catches left-side rim, lavender prevents the shadow-side from going void. The directional specificity (screen right, window upper-left) is documented and consistent in the frame spec. The blending mode decisions (Screen for glow spill and rim light, Multiply for scan-line texture on CRT only, Normal for specular pops) are technically correct choices. Screen mode for additive luminous sources, Multiply for darkening textures into the screen — these are right.

**Pixel data analysis — SF01 pre/post-stylization:**

Pre-styled mean: R=91.9 G=100.6 B=76.2 | Post-styled: R=93.5 G=101.2 B=77.6

The styled version shows a net increase of R+1.6, G+0.6, B+1.4 overall. This is the warm colour bleed pass adding amber warmth across the entire frame. The green channel increase is the paper grain noise composited at near-equal RGB.

**Warm_pct pre-styled: 51.8% | Warm_pct post-styled: 51.8%** — unchanged. Good. The warm bleed pass is not shifting the dominant colour balance of the frame.

**FAILURE 01 — WARM BLEED BLEEDS ACROSS THE CYAN THRESHOLD**

The warm colour bleed pass (`_pass_color_bleed`) in the stylization tool detects warm-hue regions (R>140, G>80, B<120, R>G×1.2, R>B×1.5) and bleeds a SUNLIT_AMBER tint 3px outward from those regions. In SF01, the warm left half of the frame bleeds warmth rightward. The problem: the boundary between Luma's cyan-lit right-side skin (DRW-01 `#7ABCBA`) and her warm-lit left-side skin (DRW-04 `#D4B88A`) is the primary lighting boundary in the entire frame. This boundary is the physical threshold between two worlds. The warm bleed at a 3px radius is injecting amber warmth into the cyan skin zone. It is violating the lighting logic by making the cyan-lit side of her face appear warmer than the scene lighting permits. The paper warm grain at alpha 18 (intensity 0.6 = alpha 10.8 effective) is manageable, but the colour bleed at alpha 18 effective (30 × 0.6) is not negligible at a hard chromatic boundary.

This is not confirmed with pixel measurement, but it is structurally guaranteed by the algorithm. A warm-region dilation that does not respect chromatic zone boundaries WILL bleed warm pigment across lighting boundaries.

**Required correction:** The colour bleed pass must include a luminance-and-hue gate: do not bleed warm tint into pixels that are already in the cyan family (R<G, or B>R+20). This protects the hard lighting boundary at Luma's face split. Without this gate, SF01 is the most damaged asset in the package — the face split is the entire point of the frame.

**FAILURE 02 — CHALK HIGHLIGHT PASS INTERACTS WITH CRT GLOW BLOOM**

The chalk highlight pass desaturates pixels where V>216 (top 15% brightness) by 12 S-units, protected only for the amber hue range (PIL hue 8–25). The CRT screen bloom in SF01 produces high-brightness cyan pixels (Electric Cyan #00F0FF at high luminance will be in V>216 territory). The chalk pass will therefore desaturate the cyan specular pops and glow zone. These are light, not material. Desaturating a light source's peak luminance by 12 S-units changes its apparent colour temperature. The CRT screen ceases to read as purely electric cyan and drifts toward white. This is a compositing error — the chalk pass does not distinguish between material highlights (which should receive the chalk treatment) and light-source glows (which must not).

The visible consequence: in the styled output, the CRT screen's cyan peak will be slightly desaturated, weakening the colour temperature contrast between the screen and the warm room. The entire chromatic premise of SF01 is that contrast.

**Required correction:** The chalk highlight pass must exclude pixels that are part of a glow layer or screen-lit zone. The simplest implementation: exclude pixels where the blue channel exceeds the red channel AND the saturation before desaturation is above 180 in PIL HSV scale (highly saturated cyan = a light source, not chalk). Do not desaturate the CRT.

---

### SF02 — "Glitch Storm" (glitch_storm_v005, glitch_storm_v005_styled)

**Lighting concept: STRONG. Mixed-mode stylization: STRUCTURALLY SOUND WITH ONE CRITICAL FAILURE.**

The primary light (the Crack, upper right, Electric Cyan), secondary light (Hot Magenta from storm mass edges, ambient diffuse), and tertiary light (warm building windows at street level) are internally consistent. Cast shadow direction from Luma and Cosmo pointing left-away-from-crack is correct. The colour temperature gradient from upper void (cyan-dominant, no warm) to middle buildings (contested) to lower street (warm vs cyan pool) is a coherent lighting model.

The mixed-mode stylization (glitch upper two-thirds, realworld lower third, 200px blend zone) is the correct structural call. The frame *needs* two different surface qualities: the glitch sky should feel digital and sharp; the street-level world should feel organic and inhabited.

**Pixel data analysis — SF02 pre/post stylization:**

Pre-styled bottom third mean: R=39.3 G=46.0 B=59.8 lum=45.5
Post-styled bottom third mean: R=42.2 G=48.8 B=62.1 lum=48.3

The bottom third (street level, Real World zone, realworld stylization) shows: R+2.9, G+2.8, B+2.3. Luminance increase of +2.8. The warm bleed is adding slight warmth and the paper grain is lifting the overall luminance slightly. This is acceptable. The warm colour balance of the bottom third is preserved.

Pre-styled top third mean: R=17.9 G=16.2 B=30.2 lum=17.6
Post-styled top third mean: R=17.7 G=16.1 B=30.2 lum=17.5

Top third (glitch storm sky, glitch stylization) is essentially unchanged — R-0.2, G-0.1, B unchanged. The edge sharpening and colour separation passes are largely preserving the tonal balance, and the scanline overlay at alpha 10 is correctly subtle. This is right.

**FAILURE 03 — MIXED MODE GRADIENT MASK APPLIED TO ALPHA CHANNEL, NOT AS A BLEND**

The mixed-mode compositing in `_apply_mixed_treatment()` applies the vertical gradient mask by multiplying it against the alpha channel of the glitch-treated version, then alpha-compositing over the realworld version. The logical problem: the glitch-treated image has full alpha (255) everywhere because it was generated from a fully opaque source. Multiplying the gradient mask into the glitch image's alpha channel creates a gradient-transparency effect — the transition zone becomes *semi-transparent* rather than a genuine graduated blend between two treatments.

This means: in the 200px blend zone, the glitch-treated layer is composited at partial opacity over the realworld-treated layer. The result is not "smooth transition between two stylization treatments" — it is "glitch treatment fading to transparent, revealing realworld treatment underneath." These are not the same operation. In areas with detail (buildings at the sky/street boundary), semi-transparent glitch layers over realworld layers will produce double-edge artifacts where the RGB channel separation (from glitch treatment) is partially visible on top of the soft line-wobble (from realworld treatment). In a scene where the horizon line is the critical compositional boundary, this is a visible artifact.

**Required correction:** The mixed-mode transition should blend the two fully-opaque treatments using a luminosity-preserving weighted average, not by reducing alpha. Implementation: `result_pixel = realworld_pixel * (1 - mask_value/255) + glitch_pixel * (mask_value/255)` for each pixel in the blend zone. This produces a genuine cross-dissolve between treatments without introducing transparency artifacts.

**FAILURE 04 — COLOUR SEPARATION SHIFT DIRECTION WRONG FOR THE LIGHTING CONTEXT**

The colour separation pass in glitch mode shifts the R channel +shift right/down, B channel -shift left/up. The stated reference is Risograph print misregistration. In a Risograph, misregistration is random in direction and consistent in magnitude across the print run — it has no directional relationship to scene lighting.

In this frame, the primary light source (the Crack) is at the upper right. The colour separation is shifting the R channel toward the light source and the B channel away from it. Viewed from a compositing perspective: the cyan-lit surfaces in this frame already have B>R (they are blue-dominant). Shifting B upward and left — toward the shadow zone — means the blue channel separation creates a ghost of cyan light where there is no cyan light. Simultaneously, the R channel shift downward/rightward places warm-red ghosts at the base of elements that receive no warm light. The misregistration is accidentally mimicking a secondary warm fill light from below-right that does not exist in the scene. This is a subtle effect at 1-2px, but at the sky/building boundary where contrast is high, it reads as incorrect chromatic aberration — directional and wrong.

**Required correction:** For glitch treatment applied to directionally lit scenes, the colour separation shift direction should be perpendicular to the primary light direction, not aligned with it. For SF02 with light from upper-right: shift R horizontally (not toward/away from light) and B horizontally opposite. Alternatively, use a purely horizontal shift (R left 1px, B right 1px) to simulate the horizontal CRT phosphor drift convention. This removes the directional lighting conflict.

---

### SF03 — "The Other Side" (otherside_v003, otherside_v003_styled)

**Lighting concept: EXCEPTIONAL. Glitch stylization: MOSTLY CORRECT WITH ONE SYSTEMIC FAILURE.**

The zero-warm-light rule is correctly enforced at the generator level. The UV Purple omnidirectional ambient with under-lighting from the circuit traces, secondary blue-white from the data waterfall, and the deliberate absence of any warm light source — this is sophisticated and rare. Most animated environments add an ambient warm fill out of habit. Not doing that here is a meaningful compositional choice.

The inverse atmospheric perspective (bright-saturated near, purple-dark at distance) is correctly implemented and it is one of the most visually distinctive decisions in the package.

**Pixel data analysis — SF03 pre/post stylization:**

Pre-styled: R=28.8 G=22.8 B=51.9 lum=28.2 (UV Purple dominant — correct)
Post-styled: R=28.6 G=22.6 B=50.6 lum=27.9 (Blue channel dropped by 1.3)

The blue channel dropped 1.3 units after glitch stylization. This is attributable to the colour separation pass reducing the B channel in the upward-shift direction. The frame is UV Purple-dominant (B>R by a large margin), and anything that reduces B reduces the purple dominance of the ambient. The effect is a subtle de-purpling of the Glitch Layer environment.

Additionally the warm_pct rose from 1.0% to 1.8% post-stylization — nearly doubled, though still small in absolute terms. This is the warm colour bleed pass introducing amber warmth into a frame that is designed to have zero warm light. In SF03, any warm pixel is either intentional pigment (Luma's hoodie/skin, Real World debris) or a pipeline error. A warm_pct increase post-stylization means the pipeline is adding warm light that the designer specifically excluded.

**FAILURE 05 — WARM COLOUR BLEED PASS RUNS ON SF03 VIA THE GLITCH TREATMENT**

The glitch treatment in `_apply_glitch_treatment()` does NOT include the warm colour bleed pass. However, if at any point the pipeline runs `_apply_realworld_treatment()` on an asset that subsequently receives `_apply_glitch_treatment()`, or if there is a mode=glitch call that inherits warm bleed from a previous pass, the bleed contamination occurs.

Reviewing the code: `_apply_glitch_treatment()` calls only scanlines, colour separation, edge sharpening — no warm bleed. The warm_pct increase from 1.0% to 1.8% in SF03 is more likely attributable to the colour separation pass shifting the B channel upward (reducing blue-dominant pixels) and thereby reducing the denominator of the warm_pct calculation, allowing existing warm pixels to register more strongly as a fraction — not that new warm pixels are being added. However: this still represents a compositing problem. The glitch treatment's colour separation is measurably shifting the UV Purple ambient toward a less purple, less cool balance. In a frame where "no warm light" is the central emotional statement, a 0.8% warm_pct increase and a 1.3-unit B-channel drop are not negligible.

**Required correction:** The colour separation pass must be calibrated against a scene's dominant hue. For UV-Purple-dominant scenes (B-channel dominant), do not shift B upward in the misregistration — this reduces the frame's blue-purple dominance. In purple-dominant scenes, the B channel must be the stable anchor. Shift R and G only, keeping B as the hue reference channel.

---

### Tech Den (LTG_ENV_tech_den, _styled)

**Lighting concept: CORRECTED AND LARGELY WORKING. One structural issue persists.**

The v004 corrections are visible and correct in direction. The light shaft repositioned to the desk zone (apex at window, base landing on desk at Y~395) is physically plausible. The three individualised monitor glow spills replacing the single uniform ambient wash is the right call — a single wide desk wash was not a light event, it was a fill. Three separate gaussian_glow calls per monitor correctly model three separate point sources.

**Pixel data analysis — Tech Den pre/post stylization:**

Pre-styled top third: R=216.3 G=205.7 B=180.7 lum=206.2
Post-styled top third: R=214.3 G=204.9 B=184.2 lum=205.4

Top third (ceiling and upper wall zone): B raised by +3.5 units, R dropped by 2.0, G dropped by 0.8. Net effect: the ceiling reads cooler after stylization. The paper grain adds equal R/G/B, so this shift is from the chalk highlight pass desaturating warm specular highlights in the bright ceiling zone (which has high luminance values from window light spillage). The ceiling's warm cream (#FAF0DC type) is having its warm highlights slightly desaturated.

Pre-styled warm_pct: 55.7% | Post-styled: 43.8% — a drop of 11.9 percentage points.

This is significant. The Real World warm environments should retain or slightly increase their warm percentage after a realworld stylization pass (paper grain adds neutrally, warm bleed should add slightly warm). Instead, warmth is dropping by nearly 12 percentage points. This confirms the chalk highlight pass is desaturating warm highlights in the Tech Den at scale. The chalk pass removes saturation from V>216 pixels — in a bright warm room with significant window light, a substantial portion of the wall and ceiling pixels exceed V=216, and those pixels are warm. The chalk pass is systematically cooling the Tech Den.

**FAILURE 06 — CHALK HIGHLIGHT PASS IS COOLING REAL WORLD WARM ENVIRONMENTS**

This is the most damaging failure in the stylization pipeline. The chalk highlight pass was designed to kill "plastic digital highlight look" by desaturating the top 15% of luminance values. In the context of SF01 at intensity 0.6, this was tolerable. In the Tech Den and Kitchen at intensity 0.8 and 1.0 respectively, the warm rooms are extremely bright (high luminance from window light) and the warm pigments are in the orange/amber family — outside the amber hue protection range of H:8–25 in PIL space, which only protects the narrow CORRUPT_AMBER orange band. The broader warm cream, sunlit amber, and warm gold values used throughout the Real World environments fall outside this protection range. They are being desaturated by the chalk pass.

The Tech Den warm_pct dropping from 55.7% to 43.8% is a 12-point drop. The Kitchen warm_pct dropping from 95.5% to 72.9% is a 22.6-point drop — nearly a quarter of the kitchen's warm character is being removed by the chalk pass alone. This is not stylization. This is lighting damage.

**Required correction — HIGH PRIORITY:** The amber hue protection range must be substantially widened to cover all warm-orange and warm-cream tones, not just CORRUPT_AMBER. In PIL HSV space (H: 0–255), warm yellows and ambers occupy approximately H:0 to H:38. The current protection range H:8–25 protects only saturated orange-amber. The complete warm family (from terracotta/red-orange through amber through warm gold through warm cream) should be protected from the chalk desaturation. A protection range of approximately H:0 to H:40 and separately H:230–255 (the red-orange wrap-around) would correctly protect the Real World warm palette while still allowing the chalk pass to operate on neutral and cool-toned highlights.

This is not a minor calibration. The current implementation is systematically stripping warmth from every Real World warm environment that receives the realworld stylization treatment.

---

### Kitchen (LTG_ENV_grandma_kitchen, _styled)

**Lighting concept: CORRECT. Stylization damage: SEVERE.**

The kitchen lighting model is good. Morning sunlight through the window (warm amber/gold), ambient column gradient falloff into the room, floor light pool under window, CRT TV glow through doorway (correctly desaturated to CRT_SCREEN_GLOW (60, 120, 140) — a muted blue-green appropriate for a deep-plane far source, not the full Electric Cyan that would break the Real World palette rules). The perspective-correct floor grid from v003 is technically correct. The worn path trapezoid is a convincing real-world detail.

**Pixel data analysis — Kitchen pre/post stylization:**

Pre-styled mean: R=214.7 G=195.5 B=159.7 | Post-styled: R=212.4 G=194.8 B=164.6
Pre-styled warm_pct: 95.5% | Post-styled: 72.9%

The kitchen has lost 22.6 points of warm percentage. The B-channel increased by 4.9 units (the chalk pass and paper grain are collectively cooling the whites and near-whites). The R-channel dropped by 2.3. This is unambiguously damaging. The kitchen at 72.9% warm is still warm, but it has been measurably cooled by the stylization pass. The morning-light quality — which is the environmental counterpart to SF01's "warm world is safe" colour argument — is being undercut by the pipeline.

The critical detail: `CEILING_WARM = (248, 238, 214)` has luminance approximately 237. This pixel is directly in the chalk pass's V>216 target zone. The warm cream ceiling — the brightest element in the kitchen — is being desaturated by every pass of the chalk treatment. The ceiling is the largest solid warm surface in the frame. Systematically cooling it cools the room.

**FAILURE 07 — CRT GLOW IN DOORWAY IS NOT RECEIVING ITS OWN PROTECTION**

The CRT TV in the adjacent room is a key story element — the presence of this glowing screen through the doorway is the narrative foreshadowing of what is coming. The glow is rendered at CRT_SCREEN_GLOW (60, 120, 140) and CRT_GLOW_FLOOR (90, 140, 155). These are in the teal family. The chalk highlight pass does not target these values (they are not V>216). However: the dual-ring glow system (primary radius 80 + ambient radius 130) is being composited into an image that subsequently receives a vignette via the stylization pipeline.

The stylization preset runs a vignette (strength 40 at intensity 1.0) at the REALWORLD treatment level. The vignette darkens the edges and corners of the image. The CRT doorway is positioned at the LEFT SIDE of the kitchen frame — it is in the corner/edge zone that the vignette darkens. The faint CRT glow (already low alpha at 8 in the ambient ring) is being further suppressed by the vignette. The story signal is being composited over and muted.

Check the vignette falloff: `rx = int(cx * (1.0 - t * 0.55))` means the vignette extends to 55% of half-width inward — it reaches the left doorway zone at full strength. A faint glow at alpha 8 that has been vignetted could reduce to near-imperceptible alpha. The CRT as story element is disappearing in the styled output.

**Required correction:** The vignette pass must not apply to the story-CRT zone. Implement a radial exclusion zone around the doorway/CRT position in the kitchen, or reduce the vignette strength-per-zone to preserve the CRT glow's visibility. The glow was deliberately built with a dual-ring system to ensure atmospheric presence — the vignette is undoing that engineering. Alternatively, apply the CRT glow as a post-stylization composite so it is not subject to the vignette.

---

## Stylization Impact Assessment

### What the stylization does well:

1. **Paper grain** — correct approach, correct alpha (18 at intensity 1.0). The noise texture at 1/4 resolution upscaled with NEAREST preserves grain character. No visible tiling artifacts at 1920x1080. The choice to use neutral grayscale grain (not warm tinted) means the grain itself adds texture without introducing colour casts — the correct approach.

2. **Line wobble** — the per-row sinusoidal displacement is subtle and effective at producing ink-on-paper variation. The maximum ±2px displacement is correctly calibrated for 1920px width. At 480px thumbnail scale (per the legibility requirement), this effect disappears appropriately.

3. **Glitch scanlines** — alpha 10 at intensity 1.0 is correctly subliminal. Does not degrade legibility. The CRT reference reads correctly without overwhelming the image.

4. **RGB colour separation** — 1-2px offset is correctly calibrated. The Risograph reference reads. At correct direction (see Failure 04), this would be a strong glitch-identity effect.

5. **Edge sharpening for glitch mode** — UnsharpMask(radius=1.5, percent=120, threshold=3) is appropriate. Crisp geometry without haloing. The threshold of 3 prevents noise amplification. This is correct.

6. **Mixed-mode zone split** — the 2/3 upper glitch / 1/3 lower realworld split for SF02 is the correct compositional decision. The blend zone concept is sound (implementation problem is in Failure 03, not the concept).

7. **CORRUPT_AMBER protection in chalk pass** — the hue range guard for GL-07 is technically correct for that specific colour. The concept is right. The range is too narrow (see Failure 06), but the mechanism is right.

### What the stylization is failing:

1. It does not respect lighting zone boundaries (Failures 01, 05).
2. The chalk pass systematically damages warm Real World environments (Failure 06).
3. The mixed-mode compositing introduces transparency artifacts rather than a cross-dissolve (Failure 03).
4. The colour separation direction conflicts with scene lighting geometry (Failure 04).
5. The vignette suppresses a key story element — the CRT doorway glow (Failure 07).
6. The CRT glow highlight is being desaturated by the chalk pass (Failure 02).

The tool is well-engineered in its individual passes. It is poorly integrated with the lighting logic of the specific frames it is treating. It is treating all images as generic content rather than as frames with known, documented, compositionally critical lighting structures.

---

## Specific Technical Failures — Summary Table

| ID | Failure | Asset(s) Affected | Severity |
|----|---------|-------------------|----------|
| F01 | Warm colour bleed crosses cyan/warm skin boundary at Luma's face split | SF01 | CRITICAL |
| F02 | Chalk highlight pass desaturates CRT glow/bloom (light source, not material) | SF01 | HIGH |
| F03 | Mixed-mode gradient uses alpha transparency instead of cross-dissolve blend | SF02 | HIGH |
| F04 | RGB channel separation direction aligns with scene light direction — wrong | SF02, SF03 | MEDIUM |
| F05 | Colour separation reduces UV Purple blue-channel dominance in SF03 | SF03 | MEDIUM |
| F06 | Chalk pass hue protection range too narrow — cools all warm Real World rooms | Kitchen, Tech Den, SF01 | CRITICAL |
| F07 | Vignette suppresses CRT story-glow in kitchen doorway | Kitchen | HIGH |

---

## Required Corrections

### CRITICAL (must fix before pitch):

**C1 — Expand chalk pass warm protection range.**
Current: H:8–25 (PIL 0–255). Required: H:0–42 (covering the full warm-orange-amber-gold range) AND H:230–255 (red wrap-around). This is the single most damaging failure in the pipeline. It is stripping warmth from every Real World environment the tool touches.

**C2 — Add hue/saturation gate to warm colour bleed pass.**
Do not bleed amber warmth into pixels where (B - R > 15) OR where the local average hue is in the cyan family. The current implementation has no awareness of lighting zone boundaries. The face split in SF01 is the frame's primary compositional element. Protect it.

### HIGH (must fix or document as known defect):

**C3 — Replace mixed-mode alpha compositing with cross-dissolve blend.**
The gradient transition between glitch and realworld treatments should use weighted pixel averaging, not alpha channel manipulation. Build a per-pixel lerp function in the blend zone rather than the current alpha_composite of a partially transparent glitch layer.

**C4 — Protect light-source glows from chalk desaturation.**
Add a second channel condition to the chalk pass: do not desaturate pixels where (B - R > 20 AND saturation > 150 PIL scale). These are saturated cyan/blue glows — light sources. Material highlights are warm or neutral. Light-source highlights are cool and saturated.

**C5 — Implement post-stylization CRT glow composite for kitchen.**
The CRT doorway glow must be composited AFTER the vignette pass, or the vignette must include an exclusion zone around the doorway. The glow was engineered with a dual-ring system specifically to ensure atmospheric presence — do not let the vignette undo that.

### MEDIUM (fix before production, tolerable for pitch with documentation):

**C6 — Reorient RGB channel separation to be perpendicular to primary light direction.**
For SF02 (light from upper-right), shift R and B horizontally rather than toward/away from the light source. For SF03 (omnidirectional UV ambient), horizontal shift is acceptable as there is no single primary light direction to conflict with.

**C7 — Calibrate colour separation pass for dominant-hue preservation.**
In blue/purple dominant scenes (SF03), protect the B channel as the hue anchor. Shift R and G only. In warm-dominant scenes (kitchen, tech den), protect the R channel as the hue anchor. The shift direction should stabilise the dominant hue, not erode it.

---

## The Underlying Issue

The stylization tool was built as a general-purpose pass. The individual effects are calibrated and documented. But it has been deployed against frames with extremely specific, well-documented lighting structures, and nobody ran the question: "what does each pass do to each lighting boundary in this specific frame?"

That question must be asked for every asset before every stylization run. The tool needs a mode for frame-aware processing — not just "realworld / glitch / mixed" as content categories, but with frame-specific overrides for protection zones. Every frame in this package has documented lighting boundaries (the face-split in SF01, the sky/street division in SF02, the zero-warm-light rule in SF03, the story CRT in the kitchen). Those boundaries should be codified as stylization parameters — not aesthetic choices left to the tool's generic algorithm.

Bad lighting is a visual lie. So is a stylization pass that erodes the lighting you built.

---

*Nadia Okonkwo — 2026-03-29*
