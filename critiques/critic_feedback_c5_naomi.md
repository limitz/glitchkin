# Critic Feedback — Cycle 5
## Naomi Bridges, Color Theory Specialist
**Date:** 2026-03-29
**Subject:** Cycle 5 Visual Review — Style Frames, Color Keys, Palette, and Tool Code

---

## Files Reviewed

**Style Frames (text specifications, .md format — no rendered PNGs found in style_frames/ root):**
- `/home/wipkat/team/output/color/style_frames/style_frame_01_discovery.md` (v2.0)
- `/home/wipkat/team/output/color/style_frames/style_frame_02_glitch_storm.md` (v2.0)
- `/home/wipkat/team/output/color/style_frames/style_frame_03_other_side.md` (v2.0)

**Rendered Compositions (PNG, in compositions/ subdirectory):**
- `frame01_discovery_composition.png`
- `frame02_glitch_storm_composition.png`
- `frame03_other_side_composition.png`

**Color Keys (text specification, .md format — no rendered PNGs in color_keys/ root):**
- `/home/wipkat/team/output/color/color_keys/scene_color_keys.md` (v2.0)

**Rendered Key Thumbnails (PNG, in thumbnails/ subdirectory):**
- `key01_sunny_afternoon.png`
- `key02_nighttime_glitch.png`
- `key03_glitch_layer_entry.png`
- `key04_quiet_moment.png`

**Palette:**
- `/home/wipkat/team/output/color/palettes/master_palette.md` (v2.0)

**Production:**
- `/home/wipkat/team/output/production/statement_of_work_cycle5.md`

**Tools:**
- `/home/wipkat/team/output/tools/style_frame_generator.py`
- `/home/wipkat/team/output/tools/color_key_generator.py`

---

## Blocking Issues — Resolved Status

### BLOCKING ISSUE 1: Byte/Screen Figure-Ground Failure (Frame 01)
**Status: RESOLVED — with one residual risk that requires monitoring**

**Evidence of resolution:**
The Cycle 4 critique identified Byte's `#00F0FF` body fill merging with the CRT screen's `#00F0FF` emission as a character-destroying figure-ground failure. Two changes have been implemented:

1. **Byte Teal (`#00D4E8`) replaces Electric Cyan as Byte's body fill.** This is the correct fix. By shifting Byte's fill approximately 6% darker and toward the teal end of the cyan family, the character gains inherent separation from the screen emission even before any outline is applied. GL-01b is now a proper entry in the master palette with complete rationale, shadow companion, and use constraints. This is well-documented work.

2. **Corrupted Amber (`#FF8C00`) 2px outline exception is now implemented.** The `draw_amber_outline()` function in `style_frame_generator.py` is clean and applies to all three frames. The master palette's GL-07 section now carries exhaustive usage guidelines for Corrupted Amber including approved uses, prohibited uses, and the mandatory disambiguation test ("if it could be replaced by Soft Gold without visual disruption, it is being misused"). This is exactly the kind of governance documentation this color needed.

3. **Frame 01 monitor emergence zone darkened.** The code darkens the upper-right quadrant of the screen to `(20, 20, 40)` before placing Byte — creating a local dark pocket so Byte's body reads against a near-void background rather than directly against the Cyan screen fill. Smart compositional thinking.

**Residual risk I am flagging — not a blocker yet, but it will become one:**
The Frame 01 rendered composition uses Byte Teal as the body fill and the Amber outline. In the composition code, the screen is redrawn at full Electric Cyan after the screen glow effect, then the emergence zone is darkened. The Corrupted Amber outline (`draw_amber_outline()` at `width=3`) is applied to Byte's bounding rectangle. However: `draw_amber_outline()` draws successive offset rectangles, not a true stroked silhouette. On an ellipse (Byte's circular body), the offset rectangles produce a squared amber corner at each cardinal point but the curve sides receive uneven outline coverage. At production scale this will produce a noticeably geometric amber halo on a round character. This is a tool precision issue, not a color issue — but it belongs on the Cycle 6 task list.

**Verdict: RESOLVED. The blocking condition (invisible Byte) is corrected. The Amber outline tool needs precision improvement.**

---

### BLOCKING ISSUE 2: Luma Unreadability on Cyan Platform (Frame 03)
**Status: RESOLVED — with a qualification**

**Evidence of resolution:**
The Cycle 4 critique called out warm skin (`#C4A882`-derived tones) placed directly against Electric Cyan platform surfaces as producing chromatic vibration that made Luma unreadable. Two fixes were applied:

1. **Dark separation zone beneath Luma.** The code inserts a near-void ellipse `(20, 8, 30)` and a void-black strip `(10, 8, 20)` directly under Luma's feet, creating a cast shadow anchor on the platform. This is the right approach — a value-dark zone between warm figure and cyan ground breaks the chromatic collision.

2. **Skin is rendered as DRW-11 (`#A87890`)** in Frame 03, not the raw warm tan. The style frame specification correctly documents this UV-modified lavender skin as the Glitch Layer skin standard. In the style frame generator code, the head is drawn with `(168, 120, 144)` which maps to approximately `#A87890` — the correct DRW-11 value. The UV ambient modification means Luma's skin is now lavender-washed, which sits at substantially lower chromatic conflict against the UV Purple ambient than the original warm tan did.

**Qualification:**
The rendered composition shows the platform color as `void_black` (`#0A0A14`) rather than Electric Cyan. The platform base is void black with cyan circuit traces overlaid. This means the fix works partly because the platform ground color has shifted away from full-saturation Cyan. The style frame specification (v2.0) correctly describes a `#0A0A14` platform with circuit traces — so the composition is accurate to the spec. But the separation zone beneath Luma (the near-void shadow) is still needed and correctly applied, because the circuit traces immediately surrounding her feet are `#00F0FF` and without the shadow zone, the trace lines would grid-cut directly through her feet zone.

**Verdict: RESOLVED. Both the figure modification (DRW-11 skin) and the ground modification (separation shadow) are in place. The fix is correct.**

---

## Color Key Fixes — Status Assessment

### Key 01 — Deep Shadow Anchor
**RESOLVED.** `#2A1A10` is now present as furniture shadow, corner anchors, and architectural crevice shadow. The palette strip in the generated thumbnail correctly labels it "DkAnch." The tonal range is compressed from the top but has a true dark value now. The bottom third of the frame reads with depth.

Minor note: the composition code adds the Deep Shadow zones but does not add a midtone step between `#5B8C8A` (Muted Teal, CRT casing) and `#2A1A10`. The jump from the mid-warm tones to the dark anchor is fairly hard. At full illustration this will be handled by intermediate painted values — but the key thumbnail now implicitly suggests a two-step drop (mid-warm to deep dark) rather than a gradual recession. This is a thumbnail simplification and I will accept it.

### Key 02 — Hot Magenta Demotion
**RESOLVED — and this is the most significant improvement in this cycle.**

The Cycle 4 critique was specific: Hot Magenta as a large bottom-of-frame zone was competing with the Cyan crack for dominant attention and splitting the threat read. The fix is cleanly implemented: the main crack is now a wide Electric Cyan line with a Static White center; Hot Magenta is applied as a `width=2` thin edge-burn on the same crack polyline plus twelve 4-pixel accent sparks. That is a correct hierarchy: Cyan owns the crack; Magenta accents the burning edge. The scene_color_keys.md v2.0 also formally documents the 8-color Key 02 exception with explicit Art Director approval noted — the documentation hygiene is correct.

What I want on the record: the `width=2` magenta line drawn over a `width=14` cyan line is functionally invisible at thumbnail scale. In the rendered PNG it will read as a barely-perceptible warm edge on the crack. This may be slightly too restrained — the burning edge of a reality crack should feel dangerous, not merely annotated. I recommend testing at `width=4` in a revision without promoting magenta back to zone-level. The original Cycle 4 problem was magenta as a zone; the correction has gone to magenta as a hair. There is a viable middle position.

### Key 03 — UV Purple / Data Blue Value Separation
**RESOLVED — but the fix introduces a new concern.**

The code creates a four-band sequence: Void Black (top) → Deep UV `#4A1880` → Standard UV `#7B2FBE` → Data Blue `#2B7FFF` → Void Black (foreground). The value ladder is now: approximately 0.06 → 0.17 → 0.28 → 0.54 → 0.06 (relative luminance). Adjacent bands are well-separated. The aurora depth layers are now readable as distinct.

**New concern: `#4A1880` is a freestanding value that does not appear in the master palette.** It exists in both the `color_key_generator.py` palette dict (as `deep_uv_sep`) and in the Key 03 label annotations. It is not documented in `master_palette.md`. An unlisted hex value appearing in rendered assets is precisely the kind of undocumented technical decision that creates painter confusion downstream. GL-04a (`#3A1060`, Deep Digital Void) is the documented shadow companion to UV Purple — but `#4A1880` sits between UV Purple and Deep Digital Void, at a different position than either. This value needs to be either:
(a) Formally added to master_palette.md as a named variant (e.g., "Mid-Void Purple" or "Atmospheric Depth Band"), or
(b) Replaced by a value that already exists in the palette system.

This is a documentation gap, not a blocking issue. But if `#4A1880` shows up in a production paint without being in the master palette, a painter has no reference for what it is, where it came from, or what its shadow companion should be.

### Key 04 — No Changes Needed
The Key 04 code and spec are consistent. The Sunlit Amber removal from ambient fill (corrected in Cycle 2) is confirmed in both the scene_color_keys.md text and the generator code. No issues here.

---

## Corrupted Amber Guidelines — Assessment

**The GL-07 usage guidelines section in master_palette.md is now among the strongest single entries in the document.** The disambiguation test ("if Corrupted Amber could be replaced by Soft Gold without visual disruption, it is being misused") is a practical, production-applicable heuristic that painters can use without referring back to theory. The approved uses are exhaustive and specific. The prohibited uses are unambiguous.

Two issues I am raising:

**Issue 1: Frame 01 — Corrupted Amber outline on Byte in a warm-dominant scene.**
The Byte outline rule states: apply the Corrupted Amber outline "whenever Byte appears in front of a cyan-dominant background." Frame 01 has a cyan-dominant CRT screen zone on the right, but the scene overall is warm-dominant. The style frame spec (v2.0) correctly defines the threshold: cyan-dominant means `#00F0FF` and `#00D4E8` together exceed 35% of background color area. In Frame 01, the screen occupies roughly the right third of the composition. 35% threshold is not obviously met or unmet without a pixel count.

The generator code applies the Amber outline in Frame 01 regardless of whether the threshold condition is met. I cannot determine from the code alone whether the cyan coverage in Frame 01 genuinely exceeds 35%. What I can say is: a Corrupted Amber outline on Byte in a warm interior scene — where most of the background is `#FAF0DC`, `#E8C95A`, and `#B8944A` — risks the prohibited use identified in GL-07: "Do not use in safe, calm Real World scenes unless a specific story event requires a corruption warning." The Amber outline's narrative plausibility ("the Real World homing signal Byte carries, visible under extreme digital stress") is weakened if it appears in scenes that are not digitally stressful.

**Recommendation:** The Cycle 5 note in GL-07 says the outline "must appear in every rendered image" — but that is in tension with the threshold rule in the style frame spec. These two statements need to be reconciled. Either the spec threshold governs (apply only when cyan-dominant threshold is met) or the "every image" mandate governs (but then the threshold rule is meaningless). Pick one and correct the other.

**Issue 2: Frame 03 — Amber outline in a UV Purple-dominant (not cyan-dominant) scene.**
The style frame 03 spec explicitly notes: "Unlike the storm scene (Frame 02), the Glitch Layer ambient is UV Purple, not Cyan-dominant. The Corrupted Amber outline exception does NOT apply here." However, the `style_frame_generator.py` code applies `draw_amber_outline()` to Byte in Frame 03 anyway, with the comment "In Frame 03 the bg is void/purple — Byte Teal still needs protection / Apply Corrupted Amber outline here too as cyan/glitch env."

This is a direct contradiction between the specification and the implementation. The spec says no outline in Frame 03. The code applies it anyway. One of these is wrong. The generator code appears to be applying the outline as a general safety measure for any Glitch environment, not as the specific cyan-dominant protection rule the spec defines.

**This is not a blocking issue in the rendered output** — the amber outline is not harmful to the composition in Frame 03 — but it is a specification-implementation inconsistency that will cause confusion when painters use the spec and the rendered reference in parallel. Fix the discrepancy: either update the spec to acknowledge the outline in UV Purple environments, or remove it from the Frame 03 generator code.

---

## Style Frame Specifications — Color Quality Assessment

### Frame 01 — "The Discovery"
The three-light breakdown (Cyan screen right / Soft Gold window left-rear / Dusty Lavender ambient fill) is textbook three-point lighting using the show's own palette. This is exactly correct color theory practice. The Zone A/B pixel grid separation protocol — switching the hoodie pixel grid from `#00F0FF` to `#F0F0F0` with a 1px `#0A0A14` outline in the screen-glow zone — is a genuinely sophisticated solution to a real problem. It creates a three-layer hierarchy (glow → grid → hoodie base) that reads distinctly at each level.

One issue: the blending mode table specifies "Screen blend mode" for the warm rim light on Luma's left edge (`#E8C95A`). Screen mode with a warm color on a warm character will push luminance but preserve hue correctly. However, the specification also says "No blending modes on the master character fill layers — all character fills are flat Normal-mode fills." A rim light layer is not the same as a fill layer, but the instruction is ambiguous about whether rim light layers are considered "overlay" layers (blending modes permitted) or whether they fall under the "no blending modes on character" prohibition. Clarify: rim light layers are overlay layers; character fill layers are flat. The distinction must be stated explicitly, not implied.

### Frame 02 — "Glitch Storm"
The Byte visibility solution — Corrupted Amber outline PLUS repositioning to the LEFT shoulder (shadow side, away from the crack) — is elegant. Repositioning solves a problem through composition rather than through color alone. The base contrast of Byte's void-black form against the deep hoodie shadow `#3A1A14` is real contrast, not compensated contrast. The amber outline then becomes a refinement, not a crutch. This is good color design thinking.

The storm confetti correction is complete: Acid Green removed from storm particles, restricted to Glitchkin-attributed particles only, with a physics/attribution rule governing the spatial separation between storm particles and character-shed particles. The semantic governance of Acid Green (`#39FF14` = healthy glitch only) is now properly enforced.

One issue I am watching: the generator code renders Cosmo's jacket as `(128, 192, 204)` which is approximately `#80C0CC` (DRW-09 Storm-Modified Jacket). This value appears in the master palette DRW section. However, the `C` dict in `style_frame_generator.py` does not include a named entry for `#80C0CC` — the color is rendered as a raw tuple `(128, 192, 204)`. All other character-critical colors are named in the `C` dict. This is an undocumented inline value in the tool. The `C` dict should include `"jacket_storm_modified": (128, 192, 204)` for consistency and auditability. A painter inspecting the code cannot identify this tuple without independently looking up DRW-09.

### Frame 03 — "The Other Side"
The "warm-color inventory" analysis in the color story section — counting exactly three warm elements (modified hoodie, modified skin, corrupted Real World fragments) and noting that is the totality of warmth in the frame — is exceptional color storytelling. The emotional argument ("you can carry your warmth here, but nothing gives it to you") is expressed through a precise color count. This is the level of intentionality this show requires.

The Glitch Layer atmospheric perspective (close = bright/saturated, distant = purple/dark/void) correctly inverts the Real World atmospheric convention. This is documented in the technical spec notes. Good. Make sure this rule appears in the background artist brief — it is the most important single technical difference between Real World and Glitch Layer background painting.

The skin highlight variant table (DRW-11, DRW-13b for cooler-skin characters) fills a real production gap. Having documented flat hex values for Grandma Miri and background human characters in Glitch Layer scenes prevents inconsistent rendering by different artists.

The one issue: DRW-16 is described as "the most complex surface color in the show" — orange hoodie under Data Stream Blue waterfall light producing `#9A7AA0`. This is a plausible hue mixture but I want to verify the color theory. Orange (`#E8703A`, roughly H:22°) under blue light (`#2B7FFF`, roughly H:220°) should desaturate and shift toward brown-lavender. `#9A7AA0` is approximately H:296°, which is in the blue-purple range. That shift from H:22° to H:296° (a 274° hue rotation) is more than simple desaturation — it implies that the blue light is fully dominating and the orange base is nearly gone from the result. This is plausible for very strong blue lighting, but it means the right shoulder reads as completely different from the rest of the hoodie. Painters should be warned: DRW-16 is not a variation on the orange hoodie color — it is a completely different color. The spec should note this explicitly so painters do not try to blend toward orange and instead paint this as a flat color zone.

---

## Tool Code — Assessment

### style_frame_generator.py

**Strengths:**
- Clean palette dictionary at the top of the file with RGB tuples and inline comments linking to named palette entries. The Corrupted Amber entry includes a brief function comment.
- `draw_amber_outline()` is a properly documented utility function, separate from the frame-generation functions. Reusable and consistent across all three frames.
- The lamp glow in Frame 01 correctly terminates before `W // 2 - 10` — the hard boundary between warm and glitch zones is enforced in code.
- The Frame 03 atmospheric gradient uses inline computation (lerping between void black, UV purple, and data blue) rather than a hardcoded block. This is flexible and easier to tune.

**Problems:**

1. **Byte rendered as ellipse, amber outline applied to bounding rectangle.** The character is drawn as `draw.ellipse(byte_rect)` but `draw_amber_outline()` draws offset `draw.rectangle()` calls against the same bounding rectangle coordinates. The result is a rounded character inside a squared amber outline. This is a shape mismatch. The outline function needs an ellipse variant for circular characters or needs to accept a shape parameter.

2. **Inline unnamed color tuples for character-critical derived colors.** `(128, 192, 204)` for Cosmo's jacket, `(192, 112, 56)` for Luma's hoodie in Frame 03 `(DRW-14)`, `(168, 120, 144)` for DRW-11 skin, `(42, 16, 64)` for far structures. These are all production-critical values that should be named in the `C` dict and cross-referenced to the master palette DRW/ENV codes. The naming convention is established (see other entries); these outliers need to be brought in.

3. **The screen glow in Frame 01 uses inline color computation** (`min(255, 100 + r)`, `min(255, 140 + r)`) rather than interpolating between named palette values. This means the glow gradient is not reproducible from the palette — a painter cannot look at this code and trace the screen glow color back to a documented value. Replace with interpolation between `deep_cyan` and `elec_cyan`.

4. **Frame 02 confetti loop does not include UV Purple.** The confetti colors list is `[C["static_white"], C["elec_cyan"], C["hot_magenta"], C["uv_purple"]]` but the actual rendered loop uses `random.choice([C["static_white"], C["elec_cyan"], C["uv_purple"]])` — Hot Magenta is included in the Key 02 generator's confetti but not confirmed in Frame 02's confetti loop. Check that the Frame 02 confetti specification (storm confetti = Cyan, White, Magenta, UV Purple) is fully honored in the generator code. Hot Magenta must be present in the storm confetti choices per the style frame spec.

### color_key_generator.py

**Strengths:**
- Clear per-key change documentation in comments at the top of each generator function. An engineer or artist reading this code immediately understands what changed and why.
- `palette_strip()` with luminance-based text color selection (dark text on light swatches, light text on dark) is correct accessibility thinking and produces readable labels.
- `load_font()` with fallback path handling is robust.
- The Key 03 band-separation comment block is exceptionally clear documentation of the problem, the measurement (relative luminance values), and the solution. This is reference-quality inline documentation.

**Problems:**

1. **`#4A1880` (`deep_uv_sep`) is an undocumented palette value.** As noted in the Key 03 assessment: this value appears in the tool but not in master_palette.md. It must be either added to the master palette with a proper entry or replaced by a documented value.

2. **`random` module imported inside function bodies** (both files). `import random` appears inside `generate_key02()` and `generate_key03()`. This is not a functionality problem (Python handles repeated imports gracefully) but it is a code quality issue — module imports belong at the top of the file. More importantly, seeded randomness is correctly used in `generate_frame02()` (`random.seed(20)`) but the seed is reset between calls. If functions are called in different orders, the visual output is still deterministic per-function. This is acceptable but should be documented as intentional in a comment.

3. **The Key 01 palette strip shows 9 swatches** (Cream, Gold, Terra, Sage, Lavdr, Cocoa, Skin, Cyan, DkAnch) against the 7-color scene budget rule. The key's own spec section notes "Total: 7 dominant colors — at the upper limit." The palette strip in the thumbnail visually presents 9, which will confuse artists reading the thumbnail as a reference. The Deep Shadow is the correct addition; the Cyan trace is an accent, not a dominant. Consider labeling the Cyan swatch "Cyan*" (accent) and the Deep Shadow "DkAnch*" (added Cy5 fix) to distinguish them from the 7 dominants.

---

## Palette Document — Assessment

The master_palette.md v2.0 is substantially stronger than any previous version. The shadow companion system for every color, the opacity-free flat hex policy, the distinction between Rust Shadow and Skin Shadow (with explicit RGB channel comparisons), and the Forbidden Combinations section (now at 10 rules) represent production-quality documentation.

**Three issues I am formally flagging:**

1. **`#4A1880` undocumented.** This must be added. Suggested placement: as GL-04b, between GL-04 (UV Purple `#7B2FBE`) and GL-04a (Deep Digital Void `#3A1060`). Proposed name: "Atmospheric Depth Purple" or "Mid-Void Band." Role: atmospheric perspective band in the Glitch Layer sky at mid-depth; the layer between ambient UV Purple and the near-void upper sky.

2. **The Byte character specification still lists base fill as `#0A0A14` (Void Black)** in the Section 3 character table. GL-01b (Byte Teal, `#00D4E8`) was added to the palette as Byte's body fill color with the note "Replaces the former Electric Cyan fill per Cycle 5 Art Director decision." The Section 3 character table has not been updated to reflect this change — it still lists Void Black as Byte's base fill, which is the body-form color, not the new fill. The table needs a row: `Body fill | #00D4E8 | Byte Teal — per GL-01b (Cycle 5 revision)` added above or replacing the existing "Body glow (inner)" row positioning. Currently a painter working from Section 3 would use `#0A0A14` as Byte's body fill, which contradicts GL-01b. This is an internal document inconsistency and needs correction.

3. **The "Color Tells Story" narrative sections in the style frames are among the strongest creative writing in this entire project.** I am noting this not as a problem but as a standard: the entire palette document and all technical specs should aspire to this level of intentionality. Every color choice should be explainable in terms of what story it tells, not only what hex code it carries. The team is achieving this in the style frames. Carry it into the color keys and the character specs with equal rigor.

---

## Non-Blocking Issues — Status Summary

| Issue | Cycle 4 Status | Cycle 5 Status |
|---|---|---|
| Key 01 no dark anchor | Critical | RESOLVED — #2A1A10 added |
| Key 02 Magenta competing with Cyan | Critical | RESOLVED — Magenta demoted to 2px accent |
| Key 03 UV Purple / Data Blue merge | Critical | RESOLVED — 4-band value ladder added |
| Key 04 Sunlit Amber as ambient fill | Critical | RESOLVED (Cycle 2) — confirmed clean |
| Acid Green in storm confetti | Critical | RESOLVED — semantic rule enforced |
| Corrupted Amber usage ambiguity | Non-blocking | RESOLVED — GL-07 guidelines are production-ready |
| Byte outline rule: documented but unimplemented | Non-blocking | RESOLVED — implemented in all three frames |
| `#4A1880` undocumented in master palette | NEW | NOT RESOLVED — needs palette entry |
| Byte character table not updated (GL-01b) | NEW | NOT RESOLVED — Void Black still listed as base fill |
| Corrupted Amber threshold vs. "every image" contradiction | NEW | NOT RESOLVED — spec reconciliation needed |
| Frame 03 amber outline contradicts spec | NEW | NOT RESOLVED — spec/code alignment needed |
| `draw_amber_outline()` rectangle vs. ellipse mismatch | NEW | NOT RESOLVED — tool fix needed |
| Unnamed inline color tuples in style_frame_generator.py | NEW | NOT RESOLVED — naming consistency needed |
| DRW-16 hue shift warning missing from spec | NEW | NOT RESOLVED — add explicit painter warning |
| Key 01 palette strip shows 9 swatches vs. 7-color limit | NEW | NOT RESOLVED — labeling clarification needed |

---

## Cycle 6 Tasks

### Priority 1 — Documentation Corrections (must be done before Cycle 6 renders begin)

1. **Add `#4A1880` to master_palette.md as GL-04b** with full entry: name, hex, RGB, role, shadow companion, use-case notes, pairs-with, avoid-using.

2. **Update Section 3 Byte character table** to reflect GL-01b: Byte Teal `#00D4E8` as body fill. The table row for "Base fill" currently reads `#0A0A14` (Void Black) which is now Byte's silhouette line/crevice color, not his primary fill. Separate these clearly.

3. **Reconcile the Corrupted Amber outline rule:** Either (a) the "apply in every rendered image" statement in GL-07 is the operative rule — in which case delete the threshold condition from the style frame spec, OR (b) the threshold condition governs — in which case correct the GL-07 note to say "apply whenever the threshold condition is met per style_frame_02 definition." Do not leave two contradictory rules in parallel documents.

4. **Align Frame 03 spec and generator code on Byte's amber outline.** The spec says no outline; the code applies one. One of them must change. My recommendation: the code should follow the spec. Remove the `draw_amber_outline()` call from `generate_frame03()` since the UV Purple ambient provides adequate contrast per the spec's reasoning.

### Priority 2 — Tool Fixes (Cycle 6 renders)

5. **Fix `draw_amber_outline()` to support ellipse targets.** Either add an `ellipse=True` parameter and call `draw.ellipse()` for the offset passes, or accept a shape type parameter. Byte is circular and deserves a circular outline.

6. **Move all unnamed inline color tuples into the `C` dict in `style_frame_generator.py`.** Minimum: DRW-11 skin, DRW-14 hoodie, DRW-09 jacket, atmospheric structure purple, far structure void. Name them according to the DRW/ENV codes from master_palette.md.

7. **Fix inline screen glow color computation in Frame 01.** Replace the `min(255, 100 + r)` arithmetic with an interpolation between `C["deep_cyan"]` and `C["elec_cyan"]` so the gradient is traceable to named palette values.

8. **Verify Frame 02 confetti includes Hot Magenta.** The storm confetti spec lists four colors (Cyan, White, Magenta, UV Purple). Confirm the generator code's random.choice list includes all four. If Hot Magenta is missing, add it.

9. **Move `import random` to the top of both tool files.** Clean code hygiene; also document that seeded randomness is intentional.

### Priority 3 — Spec Enhancements (Cycle 6 or 7)

10. **Add a painter warning to DRW-16 spec:** "This is not a variation of the orange hoodie — it is a fully distinct color resulting from blue light domination of the orange base. Paint as a flat color zone, not as a blend toward or from hoodie orange."

11. **Label Key 01 palette strip to distinguish 7 dominants from 2 additions.** Mark Cyan as "accent" and Deep Shadow as "Cy5 addition" so artists reading the thumbnail understand the 7-color budget is intact.

12. **Add Byte's amber outline condition to Luma's character painting brief.** Currently the outline rule lives only in GL-07 and the style frame specs. It needs to appear in any artist brief or production checklist where Byte appears in a scene, so it is not missed in production passes.

---

## Overall Assessment

Cycle 5 represents the strongest single-cycle improvement this project has seen. The two blocking issues from Cycle 4 (Byte invisibility, Luma unreadability) are genuinely resolved, not papered over. The Byte Teal introduction is a structurally sound color theory solution — creating a character-specific value that preserves shared visual DNA while enabling figure-ground separation. The Corrupted Amber documentation is now production-grade. The shadow companion system is complete. The opacity-free palette is a significant quality-of-life improvement for the paint department.

The work is still not at the level I require for "best of the best." The undocumented value (`#4A1880`), the internal inconsistency in Byte's character table, the spec/code contradictions on the amber outline, and the tool precision issues with the rectangle-on-ellipse outline are all small things individually. Together they represent a documentation and implementation discipline gap that will compound at production scale. A single undocumented hex value becomes five undocumented hex values becomes a palette that no one can fully trace. This must be corrected before the next cycle.

The color storytelling at the conceptual level is strong. The Frame 01 threshold metaphor, the Frame 02 invasion color argument, and the Frame 03 warm-color inventory are all excellent. The team understands what this show is trying to say with color. What remains is making the documentation and implementation precise enough that every artist can execute that vision without ambiguity.

**Grade: B+** (up from B− in Cycle 4)

The blocking issues are resolved. The palette architecture is strong. The documentation quality is substantially improved. The grade does not reach A because there are four unresolved documentation/implementation inconsistencies that represent work left unfinished, and because the tool has a shape-mismatch defect that will produce incorrect output in production. Fix those and this system is ready for full character and environment illustration.

The show's color identity is real. Now make the documents and tools match the vision without exception.

— Naomi Bridges
Color Theory Specialist
2026-03-29
