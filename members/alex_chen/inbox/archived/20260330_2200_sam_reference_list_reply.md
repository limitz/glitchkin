**Date:** 2026-03-30 22:00
**From:** Sam Kowalski, Color & Style Artist
**To:** Producer (via Alex Chen)
**Subject:** Reference Shopping List — Color/Palette Reactions

---

Hi,

Responses to your three questions on the reference shopping list:

---

## 1. Which colour/palette references are most useful for my QA and colour work?

**Top priority:**

- **Interior lighting photographs (pre-dawn kitchen, single-lamp living room):** These are directly actionable. My warm/cool QA thresholds (REAL_INTERIOR=12.0, REAL_STORM=3.0) were derived analytically, not from measured real scenes. A reference photo of a pre-dawn kitchen lit by a single incandescent would let `LTG_TOOL_warmcool_scene_calibrate.py` either validate the 12.0 threshold or flag it as wrong. SF05 ("The Passing") uses warm/cool sep=16.7 — I'd like to know if a real equivalent reads at 15–18 or something very different.

- **Depth/atmospheric perspective photos (FG/MG/BG room):** The Depth Temperature Rule (warm=FG, cool=BG) is now codified. A reference with measurable per-zone hue temperatures would let me verify that our FG-amber / BG-slate split is in the right ratio. The lineup v009 depth bands will directly benefit from this.

- **Glitch art (hue histogram reference):** Useful for validating the UV_PURPLE (hue 260°–300°) dominance threshold. The GL palette hue spread should be analogous to established pixel art conventions. A Creative Commons glitch art reference that passes the UV_PURPLE linter would be a useful canary.

**Lower priority for my specific work:**
- CRT phosphor photos are more relevant to Jordan/Hana's generators than my palette QA.
- Anatomy references are Maya/Lee territory.

---

## 2. Would Munsell and Macbeth ColorChecker references help calibrate the ΔE=5.0 threshold?

**Yes — the Macbeth ColorChecker specifically.**

The ΔE=5.0 threshold in `precritique_qa` was set by Kai Nakamura and has been the production standard since C39. It seems correct empirically (it catches GL-07 #FF8C00 mutations but passes the SUNLIT_AMBER skin-overlap false positives after investigation), but it has never been calibrated against a known perceptual standard.

The Macbeth ColorChecker contains known adjacent-swatch pairs with documented ΔE values. If I can load a digitised CC-licensed version and run `LTG_TOOL_delta_e_calibrate.py` against it, I can confirm what real-world perceptual difference ΔE=5.0 corresponds to. My hypothesis is that 5.0 is slightly tight — it catches differences that viewers would notice in an annotation context but might not notice at pitch projection resolution.

**Munsell:** Useful but secondary. Munsell distance vs CIELAB ΔE calibration would help me understand whether visually similar palette swatches (e.g., RW-02 Soft Gold vs. RW-03 SUNLIT_AMBER) have inflated ΔE readings due to CIELAB non-uniformity at high chroma. This would directly address the SUNLIT_AMBER false-positive class (FP-003, FP-005 in `qa_false_positives.md`).

---

## 3. Additions from a colour science perspective?

**1. Illuminant reference: D50 vs. D65 comparison patch**
Our monitors almost certainly render under D65 (sRGB standard). Our production is a warm-dominant Real World + cold GL Glitch Layer. If any downstream printing or projection uses D50 (print standard), all warm values will appear marginally yellower and all cool values marginally bluer. A small D50/D65 comparison patch would quantify this shift for GL-07 CORRUPT_AMBER (#FF8C00) specifically — it is the most saturation-sensitive value in our palette and the one most likely to shift on a D50 display.

**2. Hunt effect / simultaneous contrast swatch pairs**
GL-07 CORRUPT_AMBER reads differently against UV_PURPLE (near-complementary = maximum vibration) vs. against Real World warm (same hue family = lower contrast). A simultaneous contrast reference — orange swatch on purple field vs. orange swatch on amber field — would let me quantify the perceptual "pop" difference and back it with a number rather than a judgment call. Useful for defending the GL-07 amber-outline spec to critics.

**3. Bezold-Brücke hue shift reference**
At high luminance, warm hues shift toward yellow and cool hues shift toward blue-green. Our Electric Cyan (#00F0FF) is already at near-maximum luminance. A B-B reference chart would confirm whether #00F0FF at full luminance reads perceptually as 180° (blue-green) or closer to 200° — which affects how I specify the "complementary warmth" of GL-07. Low priority but would sharpen the physics behind the spec language.

---

Sam
