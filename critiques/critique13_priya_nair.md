# Color Critique — Cycle 13
**Critic:** Priya Nair, Color Theory and Emotional Palette Specialist
**Date:** 2026-03-29
**Tools run:** LTG_TOOL_color_verify.py (--histogram), LTG_TOOL_render_qa.py (all four pitch frames)
**Scope:** master_palette.md (v2.0+), SF01 v004, SF02 v005, SF03 v005, SF04 v003, color story document (ltg_style_frame_color_story.md)

---

## C12 Directive Resolution Status

| C12 Priority | Directive | Status |
|---|---|---|
| P1 | DATA_BLUE_STORM register GL-06c | RESOLVED (C28) ✓ |
| P1 | UV_PURPLE_DARK saturation → GL-04a (58,16,96) | RESOLVED (C28, SF03 v005) ✓ |
| P2 | SF04 blush fix → #E8A87C per character model | RESOLVED (C28, SF04 v003) ✓ |
| P2 | SF04 Byte body fill → canonical GL-01b #00D4E8 | PARTIALLY RESOLVED — see SF04 section |
| P2 | Luma skin base three-value conflict | RESOLVED (C9 skin system, confirmed) ✓ |
| P3 | HOODIE_AMBIENT #B36250 registration | RESOLVED — registered as CHAR-L-08 ✓ |
| P3 | SF04 cool-key hoodie derivation (monitor-facing) | NOT RESOLVED — see SF04 section |
| P3 | Cosmo skin divergence document | RESOLVED — CHAR-C-01 registered with rationale ✓ |
| P3 | Grandma Miri slippers cool-green contradiction | NOT RESOLVED — CHAR-M-11 #5A7A5A unchanged |
| P4 | Cosmo Cerulean Blue palette assignment | NOT RESOLVED |

Three P1 directives closed. One new error introduced (CHAR-L-11 cross-reference), two P3 items outstanding across eight cycles.

---

## ASSET 1 — master_palette.md

**Score: 82 / 100**

- CHAR-L-11 entry has a persisting internal contradiction: Constraint 1 was corrected in C30 to cite `#00F0FF` (GL-01 Electric Cyan) for neutral/cold hoodie pixel accents — correct. However, the **Cross-reference line directly below** (line 1174) still reads `GL-01 (\`#00D4E8\`)`. The hex cited in the cross-reference is Byte Teal (GL-01b), not Electric Cyan. The fix was applied to one line, not both. A painter reading the cross-reference without reading Constraint 1 will apply Byte Teal to hoodie pixels — exactly the error the C30 correction was meant to prevent.
- CHAR-M-11 (Miri slippers): `#5A7A5A` is Deep Sage (HSL ~120°, 15%, 42%) — a cool-green that contradicts the color story document's unambiguous-warmth guarantee for Miri. This was flagged P3 in C12. The color story document says Miri's palette must never signal the GL teal/green family before recontextualization; the slippers are at ground plane in every standing wide shot and read as a subtle cool intrusion. Eight cycles without resolution is not a scheduling problem — it is a decision being avoided.
- The shadow companion table in Section 2 and GL numbering are complete and unbroken. GL-06c derivation is properly documented with scene restriction.

**Bottom line:** The palette system is architecturally excellent and the GL-06c and UV_PURPLE_DARK resolutions were correct — but the CHAR-L-11 cross-reference still carries the wrong hex, and Miri's slippers still undermine the color story's warm guarantee.

---

## ASSET 2 — SF01 v004 — Discovery (Rin Yamamoto C29 procedural quality lift)

**Score: 84 / 100**

- color_verify_v002 result: overall_pass=True. CORRUPT_AMBER Δ0.0°, HOT_MAGENTA Δ0.0°, ELECTRIC_CYAN Δ0.4° — all exact or trivial. BYTE_TEAL Δ2.1° (828K pixels at 180–185°, only 9K at canonical 185–190°): the histogram reveals the dominant cyan mass sits slightly below the GL-01b canonical bucket. At 2.1° delta this passes tolerance but the 98:1 pixel ratio between the sub-canonical and canonical buckets suggests the frame's large cyan fill is rendering at the Electric Cyan hue angle (180–185°) rather than the Byte Teal angle (185–190°). This is expected and consistent with prior audits (the cyan-dominant fill is scene emission, not character fill) — but it warrants an inline comment in the generator for future reviewers who may interpret it as a Byte Teal calibration error.
- render_qa: value range 14–241 (range 227) — PASS. Warm/cool separation = 0.0 — WARN. The 0.0 warm/cool result is a tool limitation: the zone-sampling method fails on a split-left-right frame where warm and cool zones are laterally arranged, not vertically. Not a production defect.
- The procedural quality lift (wobble_polygon, variable_stroke, volumetric face lighting) elevates this frame above raster-smooth, which is correct for the show's hand-drawn-digital hybrid intent. The warm lamp left / cold screen right architecture remains sound.
- One outstanding: the HOODIE_AMBIENT value `#B36250` (CHAR-L-08) is now registered — the C12 P3 resolution is confirmed. No decoration-without-narrative-role color is present.

**Bottom line:** SF01 v004 is the strongest of the four pitch frames in color terms — the warm/cold split is architecturally correct, canonical values are confirmed, and the procedural quality lift integrates without hue contamination.

---

## ASSET 3 — SF02 v005 — Glitch Storm

**Score: 78 / 100**

- color_verify_v002: overall_pass=True. All five present colors PASS (Δ ≤ 1.6°). CORRUPT_AMBER histogram: 180 pixels at canonical 30–35°, 113 at 35–40°. The 40% non-canonical tail is visible — the histogram shows the amber pixels are spread across a 10° range rather than concentrated at the target. At 296 total samples and 1.4° median delta this passes tolerance, but the spread is wider than SF01's near-zero-delta CORRUPT_AMBER cluster. Monitor over multiple cycles for drift.
- HOT_MAGENTA histogram: 295 pixels in the 335–340° sub-canonical bucket, 808 in the canonical 340–345° bucket. A 27% non-canonical tail. Same caution applies — hue spread is wider here than in SF01. Not a failure, but not tight.
- GL-06c (#0A4F8C) registration is confirmed and the atmospheric depth rationale is sound. The distinction between GL-06 (close-field navigable blue) and GL-06c (storm distance oppressive near-navy) is now formally documented with derivation formula. This was the C12 P1 resolution — it is correct.
- render_qa: value range 0–255 (full range) — PASS. Warm/cool separation = 6.5 — marginal. The contested warm-cold thesis of SF02 means this result is expected: neither zone dominates, which is the narrative intent. The tool is flagging the frame for not having strong warm/cool separation, but the point of SF02 is that warm and cold are at war. This is a correct narrative outcome being penalized by a tool designed for single-temperature-dominant frames.
- ENV-06 (#96ACA2) confirmed correct in v005 per prior audit. G=172 > R=150, B=162 > R=150 — correctly cyan-lit.

**Bottom line:** SF02 v005 passes all canonical color checks; the GL-06c documentation resolves the dominant undocumented cold, but the CORRUPT_AMBER and HOT_MAGENTA hue histograms show non-trivial spread that must be monitored for drift in future versions.

---

## ASSET 4 — SF03 v005 — The Other Side

**Score: 76 / 100**

- color_verify_v002: overall_pass=False (tool). UV_PURPLE FAIL (found 262.7° vs canonical 271.9°, Δ9.2°) and SUNLIT_AMBER FAIL (found 25.0° vs canonical 34.3°, Δ9.3°) — both documented false positives per pre-critique audit. UV_PURPLE histogram confirms this: 132 pixels at the canonical 270–275° bucket, pulled to 262.7° median by the 72+93+111 gradient/transition pixels in the 250–265° range. The canonical UV Purple is present. SUNLIT_AMBER false positive is confirmed — 1,349 pixels with hue 20–30° are GL-07 crack glow and HOODIE_UV_MOD (192,112,56), not SUNLIT_AMBER. Zero warm light sources in this frame is correctly enforced.
- UV_PURPLE_DARK saturation correction (C28, v005): GL-04a (58,16,96) = HSL (273°, 72%, 22%) replaces the prior (43,32,80) = HSL (261°, 31%, 22%). The C12 P1 directive is confirmed resolved. The deepest voids are now chromatically active, not grey-purple.
- render_qa: value range 0–255 — PASS. Warm/cool separation = 3.0 — FAIL (tool). Expected: SF03 is cold-dominant by design. The 3.0 separation is the correct result for an inverted atmospheric perspective frame where warmth survives only as pigment memory. Not a production defect.
- The DRW-18 hair base `#1A0F0A` (HSL ~18°, 45%, 7%) issue from C12 is not resolved. At 7% lightness, the warm undertone is perceptually absent — only the UV Purple rim sheen on the hair crown does narrative work. The color story document claims residual warmth in the hair base, but the actual value cannot carry that claim at 7% lightness. This was raised in C12 and is still unaddressed. It is a philosophical gap between the documented intent and the rendered result.
- Inverted atmospheric perspective implementation is still sound in principle. The BYTE_BODY = (0,212,232) GL-01b fix from C9 is confirmed in the generator and in the histogram (184.5° median, 1,243 samples — within tolerance).

**Bottom line:** SF03 v005 correctly resolves the C12 P1 UV_PURPLE_DARK saturation failure and enforces the zero-warm-light rule, but the DRW-18 hair warmth claim remains visually unsupported at 7% lightness — a documented intent that the rendered value cannot deliver.

---

## ASSET 5 — SF04 v003 — Luma & Byte

**Score: 68 / 100**

- color_verify_v002: overall_pass=False. All GL colors not_found (0 pixels within radius=40 of canonical values). This confirms the Cycle 26 finding: Byte's teal is present at hue 183–185° (per prior 29K-pixel analysis) but at luminance ~60–70% of canonical GL-01b (0,212,232). The tool cannot reach these dimmer teal values from the canonical center. The color story document states "Byte's body fill in v003 is confirmed at GL-01b (#00D4E8, Byte Teal)" — but the tool shows zero GL-01b pixels in radius. The generator source files are missing (stubs only — confirmed in C30 audit). Without the generator, Byte's actual rendered value cannot be verified against canonical. The "confirmed" status in the color story document is based on generator source code inspection from a prior cycle, not from the current output PNG. This is unresolved documentation risk.
- SUNLIT_AMBER FAIL (Δ12.4°, n=69, hue 45–50°): confirmed false positive — these are Soft Gold (RW-02) range values from lamp glow, not SUNLIT_AMBER. 69 samples at hue 46–47° is consistent with warm background lamp spill.
- render_qa: value range 12–198 (range 186) — FAIL (tool threshold: range ≥150 passes, but max pixel is 198 vs expected ≥225). The brightest pixel in SF04 v003 is 198, below the QA threshold of 225. This means the frame has no strong specular pops — it is compressed into a mid-register. For a frame designed to show Byte as a glowing entity adjacent to a warm lamp, the value ceiling at 198 is too low. Byte's teal glow should be reaching toward 240+ in its brightest pixels. Silhouette: ambiguous (QA tool result). Warm/cool separation 0.0 — WARN.
- C12 P2 blush correction: SF04 v003 blush is documented as corrected to soft rose-pink per the color story document. With no generator source to verify, I accept the team's attestation.
- C12 P3 cool-key hoodie derivation: The monitor-facing (Byte Teal key) hoodie surface in SF04 still has no registered DRW entry. Luma's orange hoodie in a scene with GL-01b as the dominant cool key should produce a hoodie modification analogous to DRW-07 (storm cyan key) or DRW-03 (CRT electric cyan key). No such derivation exists in master_palette.md. The warm shadow `#B84A20` being applied to a Byte-Teal-facing surface is thermally incorrect. This C12 P3 directive was not actioned.

**Bottom line:** SF04 v003 has three compounding weaknesses — value ceiling too low at 198 (Byte should glow), missing monitor-facing hoodie derivation, and missing generator source making canonical color verification impossible; these together represent the weakest pitch frame in the set.

---

## ASSET 6 — Color Story Document (ltg_style_frame_color_story.md)

**Score: 87 / 100**

- The three-sentence arc remains the clearest color-narrative summary I have encountered on this production. The warm→contested→cold/alien logic is architecturally sound and correctly describes what the palettes are actually doing.
- GL-06c STORM_CONFETTI_BLUE note added to SF02 section is precise and correct. The distinction between GL-06 (close-field navigable) and GL-06c (storm atmospheric) is now documented in the narrative context where it matters.
- SF04 section (C28/C29 addition): The three documented fixes are explained with their narrative consequences. The blush correction rationale (curiosity-delight vs. distress) is exactly what a color story document should contain. The Byte teal canonical explanation is sound.
- Glitch interior desire states (YEARNING/COVETOUS/HOLLOW) and bilateral eye rule: well-documented, narratively coherent. UV_PURPLE bilateral for YEARNING is the correct assignment — the void color for a character who yearns for something in the deep cold.
- Grandma Miri bridge character section: the "warmth as camouflage" argument is conceptually strong. However, the document still states "her space should read as unambiguously warm" while CHAR-M-11 (house slippers) contradict this at the ground plane. The document makes a promise the color model does not keep.
- C12 Issue 1 (DRW-14 saturation arithmetic not shown): still unresolved. The document asserts that Luma's hoodie warmth survives in the Glitch Layer because organic pigment retains hue identity under cool ambient. The spectral arithmetic (78%→55% saturation, 57%→48% value, hue preserved at ~22°) is correct — DRW-14 confirms it — but the document does not show this. It states the conclusion without the proof. Painters who need to derive equivalent values for new Glitch Layer scenes have no arithmetic model to follow.

**Bottom line:** The color story document is strong narrative writing that correctly encodes the emotional arc — its remaining weaknesses are a missing arithmetic model for pigment-persistence under cool ambient, and a warm-palette guarantee for Miri that the actual color model (CHAR-M-11) undercuts.

---

## SUMMARY OF ACTIONABLE DIRECTIVES — C13

**P1 — Fix CHAR-L-11 cross-reference hex in master_palette.md.** Line 1174 reads `GL-01 (\`#00D4E8\`)` — this is the wrong hex. Must read `GL-01 (\`#00F0FF\`)`. The Constraint 1 text was corrected in C30; the cross-reference line was not. A single-line fix that is blocking correct palette application for cold-scene hoodie pixels.

**P2 — Rebuild or reconstruct SF04 generator source.** The generator stubs for v001/v002/v003 reference original source files that are not on disk. Without source, canonical color cannot be verified, Byte's teal luminance cannot be confirmed, and the frame cannot be regenerated for any required fix. This is a production risk that has been carried forward since C26 — it must be addressed before pitch.

**P2 — SF04 value ceiling: brightest pixel at 198 is too low.** The frame's maximum luminance should reach 225+ on Byte's glowing teal surfaces. At 198, Byte does not glow — he sits at the same value ceiling as the background. The luminance hierarchy (character > background) breaks down. Fix requires either generator rebuild (see above) or a levels correction pass.

**P2 — Register SF04 monitor-facing hoodie derivation.** Luma's hoodie surface facing GL-01b Byte Teal key requires a DRW entry documenting what the orange hoodie looks like under a Byte Teal cool dominant key. DRW-07 exists for storm cyan, DRW-03 for CRT electric cyan — the bedroom lamp+monitor scene has no equivalent. The surface is currently rendered with warm shadow (#B84A20), which is thermally wrong for a cool-key-facing surface.

**P3 — Resolve Grandma Miri slippers (CHAR-M-11 #5A7A5A).** Deep Sage is a cool-green at 120° HSL. On the ground plane of a character whose palette must read as unambiguously warm, this registers as a subtle GL family signal. Eleven cycles without resolution. Either change to a warm earth tone (ochre, warm tan, terracotta family) or write a specific documented rationale into both the color model and the color story document.

**P3 — Add DRW-14 pigment-persistence arithmetic to color story document.** The argument that Luma's hoodie warmth survives in the Glitch Layer is correct but undocumented numerically. Show: base orange (78% sat, 57% val) → UV ambient → DRW-14 (55% sat, 48% val), hue angle preserved at ~22°. This gives painters a derivation model for any future Glitch Layer scene where a Real World warm pigment appears.

---

## Overall Color System Assessment

The two C12 P1 resolutions (GL-06c registration and UV_PURPLE_DARK saturation correction) were the right calls and were executed correctly. The palette documentation system is more rigorous than industry standard for this stage of production. The three-palette arc (warm/contested/cold-alien) is cleanly encoded and holds up under tool analysis.

The remaining problems concentrate in SF04, which has more unresolved issues than any other single asset: missing generator source, luminance ceiling failure, missing cool-key hoodie derivation, and unverifiable canonical Byte teal. SF04 is structurally the most important frame for character dynamics — it is the only frame showing Luma and Byte in direct relation — and it is the least technically solid. This must be addressed before pitch.

*Priya Nair — 2026-03-29*
