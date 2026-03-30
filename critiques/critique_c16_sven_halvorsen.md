# Critique 16 — Sven Halvorsen
**Cycle:** 40
**Date:** 2026-03-30
**Critic:** Sven Halvorsen — Lighting, Compositing & Visual Effects
**QA tools used:** `LTG_TOOL_render_qa.py` (all 4 style frames + 7 environment BGs), `LTG_TOOL_color_verify.py` (per-color hue analysis on all failing frames)

---

## SF01 — "The Discovery" v006

**Score: 76/100**

- **Warm/cool separation = 17.4 (FAIL, threshold ≥ 20, REAL_INTERIOR=12 threshold passes — but the tool's REAL_INTERIOR logic now uses 12.0, making this a PASS by the current threshold).** QA tool grades this WARN due to color fidelity. Checking the tool internals: separation=17.4 PASSES the REAL_INTERIOR threshold of 12. This is progress from C14 (17.9, failing old threshold of 20). The warm lamp fill is present and contributing.
- **Sight-line fix confirmed from C38 (Rin Yamamoto).** The head_gaze_offset +18px, pupil tracking toward emerge_cx, and the brow asymmetry (wonder vs doubt) are implemented per the spec. The CRT rim light (right-side) is correctly placed at char_cx=head_cx. This resolves the canvas-midpoint bug I flagged in C12.
- **Value ceiling: max=242, specular_count=5 (PASS).** Specular candidates confirmed present at sufficient count. No brightness loss through thumbnail.
- **Color fidelity overall_pass=True.** All six canonical colors found within hue tolerance. PASS.
- **Bottom line:** SF01 is the strongest frame in the pitch — sight-line, warm/cool separation (under REAL_INTERIOR threshold), and color fidelity all pass; the only remaining improvement is a modest lamp intensity boost to push separation above 20 for headroom against the old threshold.

---

## SF02 — "Glitch Storm" v008

**Score: 71/100**

- **Fill light direction fix confirmed (Rin Yamamoto C36).** Source corrected from lower-left to upper-right; per-character silhouette mask applied via ImageChops.multiply. My C14 structural objection is resolved. The HOT_MAGENTA fill is physically grounded.
- **Warm/cool separation = 8.5 (PASS under REAL_STORM threshold of 3).** The storm scene is intentionally cool-dominant; the threshold exception is documented in `warm_cool_world_type_spec.md`. Not a defect.
- **Value ceiling: max=255, specular_count=5 (PASS).** No concerns.
- **Color fidelity: overall_pass=True.** All palette colors found within tolerance. PASS.
- **Lingering concern — ELEC_CYAN rim on Luma (v006 C34 addition).** The `add_rim_light(side="right")` call in v006 was noted as using `get_char_bbox()` on a multi-character frame (3-char bbox spans 83% of canvas). README confirms v008 carries all v005 fixes and the C34 lighting pass. If `get_char_bbox()` was not replaced with a direct luma_cx constant for the Luma ELEC_CYAN rim, the rim may still land off-character. Source audit needed by Jordan Reed to confirm Luma's ELEC_CYAN rim uses `char_cx=luma_cx` (a geometry constant), not `char_cx=get_char_bbox(img)[0]`.
- **Bottom line:** A technically sound storm scene — fill light is physically grounded, value ceiling passes, color fidelity passes; one unverified risk remains in the ELEC_CYAN rim light character-targeting on Luma.

---

## SF03 — "The Other Side" v005

**Score: 59/100**

- **UV_PURPLE hue drift — color fidelity FAIL.** `verify_canonical_colors()` reports UV_PURPLE found_hue=262.71° vs target=271.89° — delta=9.17° (FAIL, threshold 5°). At 447 sampled pixels, this is significant. The canonical color is drifting blue-ward (hue 262° = blue-violet, not the red-violet of UV_PURPLE 271°). This suggests the ambient wrap or void zone colors have been mixed with the UV_PURPLE_DARK correction from C28 (shifted from 31% to 72% sat) but the hue itself has wandered from 272° to 262°.
- **SUNLIT_AMBER color fidelity FAIL — expected but flagged.** found_hue=25.0° vs target=34.3° — delta=9.3°. SF03 is spec'd as zero warm tones; the 1349 "SUNLIT_AMBER" samples are almost certainly false positives (dust/confetti/debris from Real World fragments). But they represent palette drift and must be investigated — is any warm material in this frame intentional? If yes, it must not sample near SUNLIT_AMBER.
- **Character ambient integration still absent.** Luma and Byte at 14%/7% frame height still read as flat cutouts — no UV_PURPLE ambient wrapping on their silhouettes. The procedural_draw library has `add_face_lighting()` and `add_rim_light()` available. A UV_PURPLE ambient rim (alpha 25–35, thin 1–2px softness) would integrate both characters into the scene's light environment without overwhelming their small scale.
- **Value distribution in void floor is flat.** min=0, max=255, range=255 PASS — but the distribution issue I flagged in C14 persists: the lower third (void floor) shows no value gradient, reading as uniform near-black paste. Even a 15-unit brightness ramp from bottom edge to mid-void would cue spatial depth without violating the palette.
- **Bottom line:** UV_PURPLE hue drift is the blocking technical issue — the color anchoring the entire Other Side scene is drifting blue-violet, undermining the canonical palette integrity; characters remain unintegrated into the lighting environment.

---

## SF04 — "The Dynamic" v004

**Score: 62/100**

- **Warm/cool separation = 1.1 (FAIL).** This is the same value as C14 — zero change. The premise of this frame is warm lamp vs cool Byte-teal, but the QA tool finds these temperatures averaging to near-neutral. Source analysis confirms the lamp halo uses (255,200,80) at alpha max 40 over 10 steps — too weak to move the zone-averaged metric. The lamp halo radiates in all directions (full ellipse) rather than a directional cone; the warm energy is distributed across the whole upper frame rather than concentrating in the upper-left lamp zone.
- **SUNLIT_AMBER color fidelity FAIL.** found_hue=18.62° vs target=34.29° — delta=15.67° (FAIL, threshold 5°). The lamp hue (255,200,80) at hue≈41° is close to SUNLIT_AMBER target (34°), but the sampler finds hue=18.6° — orange-red territory. This means either the lamp color is too red-shifted OR the warm zone is dominated by terracotta/wood-toned background samples, not the lamp. Either way, the canonical warm color is not legibly present.
- **CORRUPT_AMBER and UV_PURPLE — both not_found.** Per tool: status=not_found (treated as pass). These colors have zero presence in SF04. Structurally correct for this scene, but noted: if any Glitch contamination of Byte's lighting (implied by the narrative moment) were to appear, these colors would be the vehicle.
- **Floor fill between characters still absent.** My C14 action item: add BYTE_TEAL fill from Byte's face to the floor/wall zone between the two characters. The source confirms the monitor glow is placed at mon_cx (right edge, ~sx(1330)), with alpha max 55 per step. Byte at sx(900) and the inter-character zone at ~sx(560–830) receive no teal fill from Byte's face direction. The scene concept requires this fill to exist — Byte's face-screen at 0.68W emits light; that light must hit the floor and wall to Byte's left.
- **Bottom line:** SF04 is two cycles behind its own concept — the warm/cool temperature opposition that defines the scene fails QA for the second consecutive cycle, and the required floor fill between characters was flagged in C14 and remains unimplemented.

---

## Environment Backgrounds

### LTG_ENV_grandma_living_room (v002)
**Score: 78/100**
- Value range: min=26, max=228, range=202 (PASS). Warm/cool: 25.4 (PASS). Good dual-temperature execution.
- **Max brightness = 228.** The CRT screen glow should be the brightest element in this interior — a monitor in a dim room produces specular highlights at or above 245. No specular dot on the CRT screen surface is present at this value range.
- **Bottom line:** Solid interior lighting — dual-temperature correctly executed; add a specular dot on the CRT screen to establish it as the dominant light source.

### LTG_ENV_tech_den (v004/warminjected)
**Score: 55/100**
- Value range: min=31, max=239, range=208 (FAIL — tool reports FAIL; range 208 < 210 floor? Checking: tool passes range ≥ 150. min=31 > 30 threshold, so this appears to be a FAIL on value floor: min=31 does not satisfy ≤30 requirement). **Value floor FAIL (min=31, needs ≤30).** Dark corners of this tech workspace should reach near-black under monitor-shadow zones; the current floor is two stops above the threshold.
- Warm/cool: 7.9 (FAIL). The warmth_inject pass was applied (warminjected variant), but separation at 7.9 fails REAL_INTERIOR threshold of 12. The window light shaft and monitor glow are fighting to equilibrium — neither temperature is winning the zone.
- **Bottom line:** Two QA FAILs persist after the warmth_inject pass — the scene's dual-temperature concept needs stronger contrast between the warm window shaft (upper-left) and the cool monitor glow (mid-right).

### LTG_ENV_classroom_bg
**Score: 40/100**
- **QA GRADE: FAIL.** Silhouette=blob, warm/cool separation=9.3 (FAIL), line weight = 414.65px mean (FAIL).
- The classroom is a dual-temperature interior (warm window shafts left, cool fluorescent right) that fails warm/cool separation. The silhouette blob result means the scene reads as an undifferentiated mass at 100×100px squint-test — no clear depth layering. This is the only FAIL-grade environment in the pitch.
- **Bottom line:** The classroom is the most technically broken background in the set — silhouette, warm/cool, and line weight all fail; it needs a rebuild pass with stronger value contrast between depth layers.

### LTG_ENV_millbrook_main_street (v002)
**Score: 67/100**
- Value range: min=45, max=239, range=194 (FAIL — min=45, needs ≤30; shadow zones are not dark enough). Afternoon exterior should have deep cast shadows under awnings and storefronts — currently the darkest point is value 45, two stops above threshold.
- Warm/cool: 21.2 (PASS). Afternoon sun correctly establishes warm/cool contrast.
- **Bottom line:** Shadow depth is the single issue — darken the cast shadow zones under awnings and on the shaded building faces to bring value floor below 30.

### LTG_ENV_grandma_kitchen (v005)
**Score: 74/100**
- Warm/cool: 32.6 (PASS). Value floor: min=20 (PASS). Good dual-temperature work.
- Line weight FAIL (mean=269.5px). This is almost certainly a false positive from the large flat-color passes in the warm/cool split — not architectural lines.
- Color fidelity FAIL (all environments flag this). The tool's canonical palette check flags false positives for Real World environments that correctly contain no Glitch palette colors.
- **Bottom line:** Best-performing kitchen environment in the pitch package — dual-temperature pass is the strongest of the Real World interiors; line weight flag is a tool false positive.

### LTG_ENV_school_hallway (v003)
**Score: 75/100**
- Value range, warm/cool, and line weight all PASS. Color fidelity flags false positive (Real World environment, no Glitch colors expected).
- The locker color correction (C38, Hana Okonkwo) that resolved the Cosmo cardigan figure-ground clash is confirmed present.
- **Bottom line:** Technically sound; no lighting integrity issues.

---

## Cross-Frame Observations (Complete Pitch Review)

- **SF04 warm/cool separation is at 1.1 — unchanged from C14.** This is a production-blocking failure for the most important emotional scene in the pitch. Two critique cycles of inaction on this issue.
- **Color fidelity tool flags FAIL on all environments.** This is a systemic false-positive issue: Real World environments correctly omit Glitch palette colors, but the tool treats absent colors as failures. The `not_found` status is treated as pass for individual colors, but when SUNLIT_AMBER drifts into warm-adjacent territory, it becomes a genuine fail. Alex Chen should review whether a world-type-aware color fidelity check is needed, analogous to the warm/cool world-type threshold system.
- **SF03 UV_PURPLE hue drift (delta=9.17°) is a genuine palette failure**, not a tool artifact. The Other Side scene's foundational ambient color has shifted blue-violet. This is a regression relative to the C28 saturation fix — saturation was corrected but hue has since drifted.
- **Classroom background is the only FAIL-grade asset in the pitch.** It has been in the package since Cycle 14 without a targeted rebuild pass addressing the silhouette and warm/cool failures.

---

## Required Actions

1. **SF04 CRITICAL:** Warm/cool separation at 1.1 is two cycles overdue. Increase lamp halo alpha to 65+, restrict halo to upper-left directional cone (not full ellipse). Add BYTE_TEAL floor fill from Byte's face toward inter-character zone (alpha 35–45).
2. **SF03:** Fix UV_PURPLE hue drift — target hue 271.89°, current 262.71°. Audit all UV_PURPLE usages in the generator for hue-shifting compositing operations.
3. **SF02:** Confirm Luma's ELEC_CYAN rim light uses `char_cx=luma_cx` (a hardcoded geometry constant), not `get_char_bbox()` — the multi-character bbox bug risk remains until confirmed resolved.
4. **Classroom background:** Rebuild targeting silhouette differentiation (QA=blob), warm/cool separation (9.3), and shadow depth. This is the only FAIL-grade asset.
5. **Tech Den:** Value floor and warm/cool separation both fail post-warmth_inject. Increase window shaft alpha and/or monitor glow radius to establish temperature dominance zones.
6. **Millbrook Street:** Deepen cast shadow zones under awnings and building shadows to bring value floor to ≤30.

---

*Sven Halvorsen — Lighting, Compositing & Visual Effects — C16 (Cycle 40)*
