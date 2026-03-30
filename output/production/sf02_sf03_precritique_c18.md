<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
direction and AI assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# SF02 & SF03 Pre-Critique Assessment — Cycle 18
**Prepared by:** Alex Chen, Art Director
**Date:** 2026-03-29
**Purpose:** One-page review of current state of Style Frames 02 and 03 ahead of Critique Cycle 9. No new art — assessment only.

---

## SF02 — "Glitch Storm" (current: v003)

### What Critique 8 Said

Victoria (B): Storefront lower-right reads as HUD overlay not shattered window. Character lighting lacks spec-promised dual-temperature complexity. Dutch angle not registering at 4°. Warm window glow ("emotional beacon") invisible.

Naomi (B): DRW-07 at old value (#C07A70 not #C8695A). ENV-06 still reading warm in sky-lit walls (R > G, R > B — fails cyan-lit test). Dutch angle below threshold. Warm street spill at ~8-10% visible alpha (spec said 16%, emotional anchor invisible).

### What Was Fixed in Cycle 16 (v003 — Jordan Reed)

- **Dutch angle confirmed at 4.0°** applied as final step to entire composition. Now perceptible.
- **DRW-07 corrected to #C8695A** (200,105,90) — hoodie storm saturation now ~50% HSL as documented.
- **Byte CORRUPT_AMBER outline upgraded**: solid 3px #C87A20 + glow rings. Byte fully readable.
- **Storm lighting on buildings**: ELEC_CYAN rim on right/top edges + UV_PURPLE bounce on bases. Buildings now read as storm-lit.
- **Cold confetti dominant**: DATA_BLUE 70% + VOID_BLACK 20% + ELEC_CYAN 10%. No warm confetti in storm zone. Threatening read confirmed.
- **ENV-06 verified correct in v002**: G=172 > R=150, B=162 > R=150 — both conditions satisfied. Carries into v003 unchanged.

### Remaining Risks Going Into Critique 9

1. **Storefront lower-right element** — Victoria's P1 was a white-outlined rectangle reading as a HUD/watermark. This was the single biggest cinematic failure she called. Jordan's v003 notes address storm confetti and Dutch angle but do not explicitly mention fixing the storefront. **Risk: unresolved.** If the storefront still reads as a UI overlay rather than a shattered window with Muted Teal frame and broken glass fragments, this will be Victoria's first comment again.

2. **Warm window glow ("emotional beacon")** — Not addressed in any C16 fix report. The spec demands E8C95A/FAF0DC warm window pools at street level as the scene's only warm light and emotional anchor. This was flagged by both Victoria and Naomi as absent or invisibly thin. **Risk: likely still unresolved.** Without visible warm spill, the color narrative collapses — the frame reads as a chase scene, not a scene about the world fighting back.

3. **Character lighting complexity** — Victoria flagged that Luma's hoodie reads as flat warm orange rather than the cinematically complex dual-lit DRW-07 surface. DRW-07's value has been corrected, but the character draw complexity is a rendering issue, not just a color constant. Cosmo's glasses cyan reflection (panic expression obscured by reflection) may also be underresolved. **Risk: moderate.** Character expressiveness at wide-shot scale is inherently limited — critics may accept more at v003 scale.

4. **Dutch angle perception** — Corrected to 4° in v003. Victoria's note was "subtle but unmistakable — this is not unmistakable." Naomi suggested pushing to 6-7°. Jordan delivered exactly 4° as specified. **Risk: low to moderate.** Critics who wanted more aggressive tilt may push again. The spec rationale (legibility at mild end) exists but hasn't convinced everyone.

---

## SF03 — "The Other Side" (current: v002)

### What Critique 8 Said

Victoria (B+): Luma's silhouette compositionally noisy at 1/5 frame height — detail density breaks clean silhouette read. Byte's two-eye-color distinction not confirmed legible. Mid-distance right-half slab density reads as pattern/UI wall rather than infinite space.

Naomi (B+): Data waterfall too saturated/bright (competing with characters for focal hierarchy). Luma hair — DRW-18 UV Purple rim not visible at render scale. Depth tier progression abrupt (mid-distance and far-distance collapse in upper-right quadrant). Acid Green pixel plants not visible at final scale. Byte's dual eye colors not confirmed legible at shoulder scale.

### What Was Fixed in Cycle 16 (v002 — Jordan Reed)

- **Waterfall luminance reduced**: Alpha max 110 (was ~255). Lighting strip reduced from 35 to 18 alpha. Now reads as ambient data flow, not focal element.
- **Mid-distance bridging element added**: Floating arch/platform fragment in the 40-65% x zone with hanging pillar fragments. Addresses compositional gap between Luma's platform and far structures.
- **Right-side void irregularity**: 7 slabs with seeded scale variation (±30%), position drift, polygon skew. Grid-pattern appearance broken.
- **DRW-18 UV Purple hair rim**: #7B2FBE bright 2px rim strip on Luma's hair crown. Prevents head-merging with dark background.

Sam Kowalski confirmed in color review (C16):
- UV Purple ambient and "no warm light" rule: PASSES.
- Inverted atmospheric perspective structurally correct: PASSES WITH NOTE (depth tier tonal steps may need watching).
- Byte eye radius at ~108px scale — eye_r=15px → 30px diameter each. Should be legible per code. PASSES per code check.
- Confetti density appropriate (ambient/settled, 50 particles total): PASSES WITH NOTE (some particles in void/sky zone with no source proximity — physics violation flagged for v002 pass).

### Remaining Risks Going Into Critique 9

1. **Byte's dual eye color legibility** — This is the single highest-risk item going into Critique 9. Victoria named it P3 and Naomi named it P3. The code eye_r=15px (30px diameter) should be sufficient at 108px Byte height. The v002 generator had the DRW-18 rim fix but no explicit Byte eye-size amplification. **Risk: high.** Critics who were not satisfied by v001 will want to see this confirmed. If they cannot name the two colors without reading the spec, the frame's entire emotional payload (Byte's character expressed through eye direction) is silent.

2. **Luma silhouette density** — Victoria's specific flag was too much character detail at 1/5 frame height breaking the clean silhouette read. Jordan's v002 fixes focused on waterfall, slabs, and bridging element — not on Luma's character simplification. **Risk: moderate.** The silhouette issue is a rendering density problem. Reducing it would require reworking the character draw function specifically for wide-shot rendering. This may be an acceptable "production note" for critics at pitch stage.

3. **Acid Green pixel plants** — Naomi flagged them as too small and dark to register (need minimum 3-4px at full GL-03 luminance). Sam's code review noted they were present but potentially thin. Jordan's v002 fix log does not mention plant size adjustment. **Risk: moderate.** Plants carry the semantic meaning "life persists in the Glitch Layer." If they read as dark noise rather than luminous life forms, that story beat is lost.

4. **Confetti physics violation** — Sam flagged mid-air particle clusters with no source proximity justification. Not addressed in v002. **Risk: low.** Naomi would notice if examining at detail level, but this is a secondary issue behind the eye and plant concerns.

5. **Depth tier collapse upper-right** — Naomi flagged that mid-distance and far-distance structures have insufficient tonal stepping. Jordan added variation and bridging element. **Risk: moderate.** The bridging element helps compositionally but may not resolve the tonal step issue Naomi will check on.

---

## Most Relevant Critics for SF02/SF03 — Critique 9

**Highest relevance (both frames):**

1. **Victoria Ashford** (Animation Director) — Cinematic coherence, composition, character expressiveness, emotional legibility at first viewing. Will revisit her P1 (SF02 storefront), P2 (SF03 Luma silhouette), P3 (SF03 Byte eye colors) from Critique 8. Her grades directly determine pitch-readiness. SF02 needs to move from B to B+/A range.

2. **Naomi Bridges** (Color Theory Specialist) — Color compliance, atmospheric perspective accuracy, confetti physics, depth tier arithmetic. Will audit: DRW-07 value, ENV-06 compliance, warm spill visibility in SF02. Will re-examine Byte eye colors, plant luminance, waterfall integration in SF03. Methodical — she will run the tests again.

**High relevance:**

3. **Dmitri Volkov** (Character Design Lead) — Silhouette readability at thumbnail for Luma and Byte. Will run the squint test on both frames. Particularly relevant for SF03's Luma silhouette clarity and SF02's character read in wide shot. May push on Byte's VOID_BLACK body in SF02 as figure-ground question.

4. **Takeshi Murakami** (Background Art Director) — Environment quality, depth, atmosphere, world-building consistency. His C8 notes drove the v003/v002 fix pass. Will verify: Dutch angle in SF02, slab composition in SF03, atmospheric perspective in both. Will check Jordan's v002 bridging element for spatial coherence. Quiet but precise.

5. **Aisha Okafor** (Visual Effects & Compositing Critic) — Lighting consistency, particle work, compositing quality. Will examine: SF02 warm window spill presence/absence, confetti physics compliance in both frames, the crack compositing in SF02 (Static White core / Cyan fill / Magenta edge — all three must read distinctly). SF03 data waterfall integration post-luminance-reduction. Will check whether the CORRUPT_AMBER outline on Byte reads cleanly against the storm background or bleeds.

**Moderate relevance:**

6. **Marcus Webb** (Animation Timing & Motion) — Implied motion in SF02 (Luma/Cosmo running figures — squash-and-stretch read, motion lines, hair streaming). SF03 is a still composition so less relevant, but he may note the weight and physics of Luma's platform-edge stance.

7. **Carmen Reyes** (Storyboard & Layout) — Staging and shot composition. May comment on SF02's depth layer legibility as a staging question. SF03's Luma positioning at platform edge — the toes-at-edge pose — is her kind of note.

---

## Summary Assessment

**SF02 v003 status:** Three of five C8 critical issues are resolved (Dutch angle, DRW-07, storm lighting on buildings). Two remain at risk: storefront lower-right element and warm window glow visibility. Going into Critique 9 as approximately B+ territory if storefront is clean — B if the warm spill is still absent.

**SF03 v002 status:** Two of five C8 critical issues are solidly resolved (waterfall luminance, slab variety/bridging). Three remain at risk: Byte dual-eye legibility (high risk), Luma silhouette density (moderate), pixel plant visibility (moderate). Going into Critique 9 as approximately B+ territory if Byte's eyes read — A if critics accept Luma's silhouette density as appropriate for wide-shot scale.

**Recommendation:** If any revision capacity exists before Critique 9, prioritize: (1) verify Byte eye legibility in SF03 v002 at actual PNG render scale, and (2) check SF02 storefront lower-right in v003. Those two fixes resolve the most critical outstanding items from both Victoria and Naomi.

---

*Alex Chen, Art Director — Cycle 18 — 2026-03-29*
