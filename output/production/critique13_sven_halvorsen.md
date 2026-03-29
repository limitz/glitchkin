# Critique 13 — Lighting, Compositing, and Visual Effects
**Critic:** Sven Halvorsen
**Date:** 2026-03-29
**Scope:** Style frames SF01–SF04, current pitch primaries
**Method:** Generator code analysis + `LTG_TOOL_render_qa_v001.py` warm/cool checks + `LTG_TOOL_color_verify_v001.py` fidelity checks

---

## QA Tool Run Summary

| Frame | Silhouette | Value Range | Warm/Cool Sep | Color Fidelity | Grade |
|---|---|---|---|---|---|
| SF01 v004 | distinct | 14–241 (range 227) PASS | 0.0 FAIL | PASS | WARN |
| SF02 v005 | distinct | 0–255 (range 255) PASS | 6.5 FAIL | PASS | WARN |
| SF03 v005 | distinct | 0–255 (range 255) PASS | 3.0 FAIL | FAIL* | WARN |
| SF04 v003 | **ambiguous** | 12–198 (range 186) **FAIL** | 0.0 FAIL | FAIL** | WARN |

*SF03 color fidelity FAIL: UV_PURPLE 9.2° drift and SUNLIT_AMBER false positive — both documented as gradient/radius false positives in C30 audit. Canonical UV_PURPLE pixels confirmed at exact hue. Accepted as false positive.

**SF04 color fidelity FAIL: SUNLIT_AMBER 12.4° drift is Soft Gold family (false positive, 69 samples). All GL colors not_found — Byte teal below canonical luminance (known outstanding concern, pending Alex Chen decision).

Warm/cool separation failures on SF01–SF04: the QA tool samples top half vs. bottom half of canvas. SF01 and SF04 use left/right warm-cool splits, not top/bottom — this is a tool limitation for these compositions, not a production error. SF02 and SF03 have genuine top/bottom cold dominance, so low separation scores on those frames warrant inspection.

---

## SF01 — The Discovery (v004)
**Score: 72 / WARN**

- **C12 #1 RESOLVED** — `add_face_lighting(light_dir=(-1,-1))` now applied; face receives anatomically correct upper-left shadow geometry (brow, nose, chin layers). The lamp-facing direction issue from C12 is closed.
- **C12 #11 RESOLVED** — `add_rim_light(side="right")` correctly restricts CRT teal rim to right half of canvas. The direction-agnostic problem is closed for SF01.
- **C12 #4 PARTIALLY UNRESOLVED — Byte highlight position.** `draw_byte()` places the specular glow at upper-left of Byte's body. The CRT screen is to Byte's right (Byte faces left toward Luma). Screen-proximity specular should be on Byte's right/screen-side, not upper-left. Incorrect placement remains.
- **C12 #2 PARTIALLY UNRESOLVED — Left arm cold tint.** The warm atmospheric overlay is a background radial fill applied before character drawing. It does not modulate character paint. Luma's left arm (`CYAN_SKIN`) still carries teal temperature on the lamp-facing side. At the render scale this reads as a cool-tinted arm lit by a warm lamp — a persistent ambient mismatch.
- **Blush correction confirmed** — peach tone is correct. Procedural wobble and variable stroke are perceptible improvements to line quality.

**Bottom line:** SF01 v004 is a clear step forward from v003 with face lighting and rim direction resolved, but Byte's specular placement and the left arm temperature mismatch are still open and degrading the dual-light read.

---

## SF02 — Glitch Storm (v005)
**Score: 68 / WARN**

- **C12 #7 RESOLVED** — Window pane alpha reduced to 115/110 (SOFT_GOLD/WARM_CREAM). Panes no longer compete with the cold storm as a secondary key light. The split pane/cone system is correctly documented.
- **C12 #8 PARTIALLY RESOLVED** — Window glow cones now correct at (200,160,80) alpha max 105. Warm pool geometry lands at street level. Improvement is genuine.
- **C12 #5 STILL OPEN — No cyan specular on character crack-facing side.** `_draw_luma()` applies DRW_HOODIE_SHADOW only on `torso_left` to `cx` (left half = shadow). The right torso (crack-facing side, upper right light source) is flat DRW_HOODIE_STORM with no cyan tint. Building faces receive correct STORM_RIM_CYAN on right edges; characters do not. Internal lighting logic is inconsistent between background and character rendering.
- **C12 #6 STILL OPEN — No magenta fill light on any character surface.** HOT_MAGENTA appears as a line element (crack glow, storefront outline, hair accent DRW_HAIR_MAGENTA=(106,42,58)). It does not appear as a light-temperature contribution on character skin or clothing surfaces. DRW_SKIN_STORM (106,180,174) is a teal-green ambient — no magenta component. If magenta is a fill light, its temperature must appear on the fill sides of characters. It does not.
- **C12 #8 RESIDUAL — Warm cone/ground interaction.** Warm amber cones project to street level but `draw_ground_lighting()` applies only ELEC_CYAN. Warm pool contribution to ground plane is still overwritten by the cyan pass.

**Bottom line:** The window system is meaningfully improved but the three-tier light setup still only exists in the background layer — characters receive none of the magenta fill and none of the crack-side cyan specular, leaving them lit by a different source than everything around them.

---

## SF03 — The Other Side (v005)
**Score: 81 / WARN**

- **UV_PURPLE_DARK saturation fix confirmed** — C28 correction to GL-04a (58,16,96) = 72% saturation is in place. Deep void zones now read as digital void, not grey-purple. This was a genuine improvement.
- **Zero warm light mandate enforced** — `draw_lighting_overlay()` explicitly prohibits warm values. HOODIE_UV_MOD and SKIN_UV_MOD correctly handle pigment warmth. Confetti excludes warm colors. This remains solid.
- **C12 #9 STILL OPEN — Face highlight direction inconsistent with rising left-side cyan key.** SKIN_BOUNCE highlight is applied at top of head. Rising left-side cyan from platform level would key the lower-left face, not the crown. The highlight direction has not been corrected since C12.
- **C12 #10 STILL OPEN — Position-dependent UV atmospheric tint.** SKIN_UV_MOD is a fixed palette value. The UV_PURPLE atmospheric overlay grades from alpha 20 (bottom) to 50 (top). A character standing in a volumetric atmosphere should show more UV tint at altitude. A fixed skin color cannot model this. Not a blocking issue at pitch scale, but the frame would benefit from even a simple two-zone UV mod (lower half of character slightly less tinted than upper).
- Color fidelity tool UV_PURPLE false positive confirmed as gradient edge artifact — not a production error.

**Bottom line:** SF03 v005 holds the strongest lighting logic of the four frames; the zero warm light mandate is technically rigorous, and the saturation fix for the void zones is a real improvement, but the face highlight direction and the atmospheric tint uniformity remain unaddressed from C12.

---

## SF04 — Luma + Byte: The Dynamic (v003)
**Score: 52 / WARN**

- **C12 #11 RESOLVED** — `add_rim_light(side="right")` is now in the procedural draw library with correct spatial masking (right half only). The direction-agnostic problem from C12 is structurally closed.
- **CRITICAL — Value range FAIL: max=198.** The QA tool requires brightest pixel ≥ 225 for a PASS. SF04 v003 tops out at 198 — the frame has no specular highlights, no bright point sources, no area of luminance that reaches white-adjacent values. This means the frame reads flat and low-contrast in value structure. Dual-lit compositions depend on a bright specular zone (from one source) to establish the dominant key. At max=198 the scene is lit entirely in midtone. This is a compositing failure.
- **CRITICAL — Silhouette ambiguous** (QA tool score). Character outlines are not sufficiently separated from background values at the 100×100 silhouette test scale. This is consistent with the flat value range — without bright specular peaks or strong darks separating form from ground, the characters blur into the composition.
- **C12 #13 STILL OPEN — Byte receives no monitor contribution on right side.** Byte's highlight is still placed at upper-left (window-facing), and the shadow is on the right. Byte is physically the closest element to the monitor. Zero monitor contribution on Byte's right side in a frame centered on the Luma/Byte/monitor dynamic.
- **CRITICAL — Generator source files missing.** `LTG_TOOL_styleframe_luma_byte_v001/v002/v003.py` are all forwarding stubs pointing to original files that are no longer on disk. SF04 v003 cannot be re-run or modified. If a lighting fix is needed — and it is — the generator must be rebuilt from scratch. This is a production risk that must be resolved immediately.
- **C12 #14 STILL OPEN — HOODIE_AMBIENT shadow is warm on monitor-facing right side.** `HOODIE_AMBIENT = (179, 98, 80)` is warm orange-brown. The right torso faces the monitor; the shadow there should carry a cool-teal influence from the BYTE_TEAL fill.
- Blush correction to peach confirmed. Byte canonical GL-01b teal below luminance threshold — pending Alex Chen decision. Not attributing a score penalty pending that decision.

**Bottom line:** SF04 v003 has the most serious structural defects of the four frames: a value ceiling at 198 (no specular punch), an ambiguous silhouette, missing monitor contribution on Byte, warm shadow colour on the monitor-facing side, and no generator source to fix any of it — the frame must be rebuilt.

---

## Procedural Draw Library — `add_rim_light()` (v1.2.0)

The `side` parameter implementation is correct and the spatial masking logic is sound. One design limitation remains: "right" means x > canvas_width/2 — it is a canvas-half crop, not an edge-normal filter. A character whose center of mass is in the left half of the canvas will not receive the right rim light on their right-facing surfaces if those surfaces are west of the canvas midpoint. This affects compositions where the character is positioned left-of-center. For SF01, Luma is positioned at approximately W×0.29 — her right torso edge is near x=W×0.35, which is left of the canvas midpoint W×0.50. The `side="right"` spatial mask excludes her right rim entirely.

This is a structural issue in the implementation: the "right" filter should probably be defined relative to the character's bounding box center, not the canvas center. For now the function is an improvement over the previous direction-agnostic version, but it fails for left-of-center character placements.

---

## C12 Issue Resolution Summary

| # | Issue | C12 Rating | C13 Status |
|---|---|---|---|
| 1 | SF01 face: flat horizontal gradient, no vertical lamp component | HIGH | **RESOLVED** — `add_face_lighting()` applied |
| 2 | SF01 left arm: CYAN_SKIN on warm-lamp-facing side | HIGH | STILL OPEN |
| 3 | SF01 lighting overlay: muddied warm/cold overlap at center | MEDIUM | Partially improved |
| 4 | SF01 Byte: highlight at upper-left vs. screen-facing right | HIGH | STILL OPEN |
| 5 | SF02 Luma/Cosmo: no cyan specular on crack-facing right torso | MEDIUM | STILL OPEN |
| 6 | SF02 characters: no magenta fill light on any character surface | HIGH | STILL OPEN |
| 7 | SF02 window system: cone/pane color temperature disconnect | MEDIUM | **RESOLVED** — pane alpha 115/110; cone system intact |
| 8 | SF02 ground: warm cone pools overwritten by cyan ground pass | MEDIUM | Partially improved (cones present, ground pass still cyan-only) |
| 9 | SF03 Luma face: top highlight inconsistent with rising left cyan | MEDIUM | STILL OPEN |
| 10 | SF03 characters: fixed UV palette cannot model position-dependent tint | LOW | STILL OPEN |
| 11 | SF04 `add_rim_light()`: direction-agnostic | HIGH | **RESOLVED** — `side` parameter added; canvas-half limitation noted |
| 12 | SF04 `add_face_lighting()`: shadow warmth unchallenged by cool fill | LOW | Low priority, carries forward |
| 13 | SF04 Byte: zero monitor contribution on right side | HIGH | STILL OPEN |
| 14 | SF04 hoodie shadow: warm colour on monitor-facing side | MEDIUM | STILL OPEN |

**Resolved: 3 of 14 (C12 issues). Partially improved: 2. Still open: 9.**

---

## What Must Be Improved Next Cycle

1. **Rebuild SF04 generator — no delay.** The source files are gone. Every other fix listed below for SF04 is blocked until this is done. Kai or Rin must reconstruct it from the PNG and the v002 generator logic (forwarding stubs still point to it in spirit). Value range must reach 225+ with a proper specular pass. Silhouette must be distinct.

2. **SF02 — Add magenta fill tint to character surfaces.** Compute a magenta-tinted version of DRW_SKIN_STORM and DRW_HOODIE_STORM for the fill side of Luma and Cosmo. This is a half-ellipse overlay on the storm-shadow side painted at alpha 25–40 with a magenta-shifted warm value. Without it, the characters live in a different lighting environment from the buildings around them.

3. **SF02 — Add cyan specular to crack-facing (right) torso side of Luma/Cosmo.** Apply a thin ELEC_CYAN gradient or rim strip on the right torso edge at alpha 30–50. Buildings already receive this treatment; characters must match.

4. **SF01 — Fix Byte specular to screen-facing (right) side.** The CRT is to Byte's right. Move the `draw_filled_glow()` specular hotspot from upper-left to right/center of Byte's body. This is a one-line positional fix.

5. **SF01/SF04 — Warm shadow on wrong side.** In SF01, Luma's left arm carries CYAN_SKIN on the lamp-facing side. In SF04, HOODIE_AMBIENT is warm on the monitor-facing shadow side. Both require the ambient shadow colour to carry the opposite light source's temperature.

6. **`add_rim_light()` — canvas-half crop is insufficient for left-of-center characters.** Consider an `x_pivot` parameter that sets the spatial split at the character's center x rather than canvas/2. Alternatively, document the limitation clearly so callers know to position characters past the canvas midpoint when using directional rim light.

---

*Sven Halvorsen — Lighting, Compositing, and Visual Effects Critic*
*Critique 13 | 2026-03-29*
