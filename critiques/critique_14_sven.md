# Critique 14 — Sven Halvorsen
**Cycle:** 34
**Date:** 2026-03-29
**Critic:** Sven Halvorsen — Lighting, Compositing & Technical Style Frame Quality
**QA tools used:** `LTG_TOOL_render_qa.py` (all 4 pitch PNGs), `LTG_TOOL_proportion_audit.py`, source code audit of all 4 generators

---

## SF02 — "Glitch Storm" v006 (PRIMARY FOCUS)

**Score: 44/100**

- **[CRITICAL — STAGING BRIEF NOT IMPLEMENTED]** Lee Tanaka's sf02_staging_brief_c34.md demanded: eyes, asymmetric brows, compressed mouth, and forward lean (8–12°) on Luma. The `_draw_luma()` function in v006 is identical to v005 — zero face elements, zero body tilt. The staging brief was fully ignored.
- **Fill light source logic is incorrect.** HOT_MAGENTA fill is described as "ground bounce from storm crack (upper-right)" but is applied from lower-LEFT of each character. A crack at upper-right produces a fill from the upper-right side, not lower-left. This is not a light bounce — it is a decorative tint from nowhere.
- **Radial fill does not mask to character silhouette.** The `draw_magenta_fill_light()` function paints an unmasked radial gradient in character zones. It applies HOT_MAGENTA to background pixels equally — not a character fill light, a canvas tint.
- **`get_char_bbox()` detects all three characters combined** (bbox cx=740, left=204, right=1276 — spanning 83% of canvas width). With Byte at ~28%, Luma at ~45%, Cosmo at ~62%, the combined bbox center (cx=740) drifts rightward. The `add_rim_light()` char_cx uses this bloated center — rim light lands between characters, not on Luma's silhouette.
- **QA: warm/cool separation = 6.5 (FAIL, threshold ≥ 20).** Scene is dominated by cold tones at all vertical zones. The magenta fill at alpha max 40 is too weak to push warm/cool separation into passing range, and it is compositionally wrong anyway (wrong source direction).
- **Value ceiling = 246 (PASS) but max = 246 not 255.** Specular points added post-thumbnail do not reach the spec value of ≥ 225 — they do, but only through a workaround, not from the lighting system itself. The specular pass is a patch on top of an underlit frame.
- **Bottom line:** v006 delivered cosmetic light overlays but skipped the primary deliverable — Luma's face — and the fill light physics are internally contradictory; this is two consecutive cycles of the same structural failure.

---

## SF01 — "The Discovery" v005

**Score: 72/100**

- **Rim light char_cx fix (C32) is correctly implemented.** `add_rim_light(char_cx=head_cx)` at ~x=0.29W — the canvas-midpoint bug is resolved. Rim contributes to Luma's right shoulder/arm. This is a PASS.
- **QA: warm/cool separation = 17.9 (FAIL, threshold ≥ 20).** Close but still failing. The domestic scene has a warm lamp, but the CRT glow (cool) and ambient mid-tones are pulling the separation below threshold. The warm zone needs a stronger upper-half warm push — lamp intensity may need lifting 10–15%.
- **Value range: min=14, max=246, range=232 (PASS).** Acceptable. No floor-to-ceiling crush.
- **Ghost Byte alpha at 90 (from v003 fix) now reads at this scale.** The two ghost screens (top-right + mid-left) are compositionally correct. No issues here.
- **Bottom line:** The rim light fix is real and working; the lingering warm/cool separation failure is the only blocking technical issue remaining in this frame.

---

## SF03 — "The Other Side" v005

**Score: 61/100**

- **Value range in Glitch Layer: QA min=0, max=255, range=255 (PASS).** Full range present. However the issue is not range — it is value distribution. The dark zones (UV_PURPLE_DARK at 72% sat — the C28 fix) read as flat dark paste at the bottom third. There is no value gradient within the void; it is uniformly near-black with no depth cueing.
- **QA: warm/cool separation = 3.0 (FAIL).** Expected for a pure-digital scene (no warm tones per spec). The tool flags it, but this is a correct scene design choice — the QA result is not actionable here.
- **QA: color fidelity FAIL.** The tool reports `overall_pass=False` for SF03. This warrants attention — canonical colors may not be sampling-detectable at pitch canvas scale, or there is a palette drift.
- **Add_rim_light not used in v005.** SF03 was never upgraded to the procedural draw library. Luma and Byte at this frame's small scale (~14% and 7% of H) may not need full rim lighting, but the absence of any UV_PURPLE ambient wrap on character silhouettes means they read as cutouts against the background rather than as figures existing within the light environment.
- **Inverted atmospheric perspective is present** — far slabs are darker and more purple. This is correctly implemented. The depth system works at a structural level.
- **Bottom line:** The frame's chief technical failure is the flat void floor — no depth within the dark zone — and character figures that have zero ambient light wrapping to integrate them into the scene.

---

## SF04 — "The Dynamic" v004

**Score: 74/100**

- **Byte's teal monitor glow lights Byte's right flank only** (`byte_cx` to `byte_cx + ex` — rightward only). It does NOT cross to Luma's position. The large CRT background monitor at x=1330 has an environment glow, but its alpha max is 55 per-step — weak. Luma's only lighting is warm lamp rim (left) and BYTE_TEAL rim (right edge). The room atmosphere between the two characters shows no teal fill from Byte's own screen. This is a missing bounce: Byte's face emits strong cyan light — the floor and wall zone between the characters should carry visible teal fill.
- **Rim lights are correctly implemented with char_cx.** Both Luma (char_cx=luma_head_cx) and Byte (char_cx=byte_cx) use character-relative splits. The bug from earlier cycles is resolved.
- **QA: warm/cool separation = 1.1 (FAIL).** Extremely low. The warm/cool opposition is conceptually the entire point of this frame (warm lamp vs cool Byte). The fact that QA reads near-zero separation means the tones are averaging to a single mid-temperature. The warm lamp zone and the teal monitor zone are either too small or too mixed at sampling resolution.
- **QA: color fidelity FAIL.** Same flag as SF03 — `overall_pass=False`. Canonical colors may be underrepresented in area sampling.
- **Value ceiling: max=252, range=244 (PASS).** SPECULAR_WHITE core on the spark interaction effect is working.
- **Bottom line:** The conceptual light logic is correct (warm lamp vs cool Byte-teal) but the implementation volume is insufficient — environment fill between characters is too weak to read on a commissioning monitor, and QA confirms near-zero warm/cool separation.

---

## Cross-Frame Observations (Fresh Eyes on Complete Pitch)

- **None of the four style frames exceed a warm/cool QA separation of 20.** This is a persistent system-wide failure. The pitch as a set reads as temperature-neutral. Commissioning panels expect contrast between lighting environments; four frames that all fail warm/cool separation is a red flag for the production design's legibility.
- **SF03 and SF04 both show color fidelity QA FAIL.** This may indicate that canonical palette colors are present but not in sufficient pixel area to register — or that there are palette drift issues below the team's detection threshold. `LTG_TOOL_color_verify.py --histogram` should be run on both frames to identify which colors are missing.
- **The proportion audit correctly marks SF02 v001–v006 as N/A (no eyes).** But this now reads as evidence of a persistent structural choice to render Luma without a face in the storm scene. v006 had explicit instructions to add a face. The N/A is no longer acceptable — it is an unaddressed defect.

---

## Required Actions for Next Cycle

1. **SF02 CRITICAL:** Implement `_draw_luma_face_sprint()` per Lee Tanaka's brief — eyes, brows (asymmetric), compressed mouth. Forward lean 8–12°. This must be done before any further lighting passes.
2. **SF02:** Rebuild magenta fill light with correct source direction (upper-right bounce, not lower-left) and mask to character pixel zones — not unmasked canvas ellipses.
3. **SF02:** Replace `get_char_bbox()` call in `draw_cyan_specular_luma()` with direct Luma-specific `luma_cx` constant. Multi-character frame confuses the bbox detection.
4. **SF04:** Add teal fill from Byte's face to the floor/wall zone between the two characters. Alpha 30–45, extending leftward from Byte toward Luma's position.
5. **ALL FRAMES:** Run `LTG_TOOL_color_verify.py --histogram` on SF03 and SF04 to diagnose the color fidelity FAIL before next critique cycle.
6. **SF03:** Add UV_PURPLE ambient wrap on Luma and Byte silhouettes — even at 7% and 14% scale, a thin ambient edge prevents the cutout appearance.

---

*Sven Halvorsen — Lighting, Compositing & Technical Quality — C34*
