<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Creative Brief — Visual Stylization Pass (Cycle 23)

**To:** Rin Yamamoto, Visual Stylization Artist
**From:** Alex Chen, Art Director
**Date:** 2026-03-29
**Re:** Hand-drawn stylization treatment — `LTG_TOOL_stylize_handdrawn.py`

---

## Project Context

*Luma & the Glitchkin* is currently rendered entirely in flat PIL — clean vector fills, hard geometry, no texture. This reads as technically competent but aesthetically neutral. The pitch brief's Visual Identity Statement promises the show "looks like it was drawn by someone who loves cartoons." The renders don't yet deliver that emotional warmth.

Your job this cycle: write the stylization pass that earns that promise.

---

## The Look We're After

**One-sentence target:** *Rough edges, warm paper, drawn with intention — like a talented artist traced over the computer's geometry and left their fingerprints.*

The hand-drawn treatment should feel like the show was produced in a traditional ink-and-watercolor pipeline and then scanned. Not "retro" or "low-fi" — considered, craft-forward, and warm. Think: the confident, imperfect line work of a Cartoon Network show from the early 2000s, where you can almost feel the ink on paper.

**What this is NOT:**
- Do not introduce Photoshop-style filters or generic blur/grain passes
- Do not destroy legibility — silhouettes must remain readable at thumbnail scale
- Do not apply the same treatment to the Glitch Layer content as to Real World content (see split rules below)
- Do not add noise that reads as compression or low resolution
- Do not wobble lines so aggressively that character models destabilize

---

## The Split: Real World vs. Glitch Layer

The show's core visual tension is warm organic Real World versus cold digital Glitch Layer. The stylization pass must honor this split — the two zones should feel like they were made differently.

### Real World Treatment (SF01, SF02 foreground, background environments)

These images should feel most hand-drawn. Paper texture and organic warmth are primary here.

**Priority effects (in this order):**
1. **Paper/canvas grain** — subtle tooth on fill areas, especially warm-colored regions. Not dirty — a slight felt-tip-on-paper roughness. Target: barely perceptible at full resolution, visible at 50%.
2. **Line wobble/jitter** — apply a slight, seeded wobble to hard geometry edges. 1–3px maximum displacement. Should feel like confident hand-drawing, not shaking.
3. **Color bleed at warm edges** — where warm tones (amber, terracotta, cream) meet darker areas, allow a 2–4px soft hue bleed outward. Simulates ink wicking into paper tooth.
4. **Chalk/gouache highlight quality** — desaturate highlights very slightly (reduce S by 8–12%) and add a fractional opacity texture layer over specular areas. Kills the plastic digital highlight look.

### Glitch Layer Treatment (SF03, Glitch Layer environments)

These images should feel like the opposite: printed, geometric, screen-halftone. The Glitch Layer is *digital* corruption — not organic. Its stylization treatment should feel like early print media or a vector design printed on risograph.

**Priority effects (in this order):**
1. **Scanline texture** — subtle horizontal scanline pattern over the image at very low alpha (5–10%). References CRT technology — the world Byte lives in is a television.
2. **Slight color separation** — RGB channel micro-offset (1–2px) on high-contrast edges. Simulates vintage printing misregistration. Should be subliminal, not legible as glitch.
3. **Edge sharpening on geometry** — Glitch Layer hard geometry edges (platforms, void borders) should be crisper than Real World edges. Slight unsharp mask pass. Counter-intuitive to organic treatment.
4. **No paper grain** — the Glitch Layer has no paper. Do not apply Real World grain to SF03 or Glitch Layer environments.

### SF02 (Glitch Storm) — Mixed Treatment

SF02 is the boundary event — both worlds in collision. Use a zone-based approach:
- Lower third (Luma, Cosmo, street level): Real World treatment — paper grain, warm edge bleed
- Upper two-thirds (storm sky, Glitch cloud masses): Glitch Layer treatment — scanlines, color separation
- Use a soft gradient mask to blend the transition zone (~200px vertical blend at the boundary)

---

## Asset Targets for This Cycle

**Primary (must deliver rendered output):**
1. `LTG_COLOR_styleframe_glitch_storm.png` — SF02 with mixed Real/Glitch treatment
2. `LTG_COLOR_styleframe_otherside.png` — SF03 with full Glitch Layer treatment

**Secondary (apply if time and quality allow):**
3. `LTG_COLOR_styleframe_discovery.png` — SF01 with full Real World treatment. Note: SF01 is LOCKED A+ — apply very conservatively. The stylization must not degrade what's already pitch-perfect. If in doubt, deliver a test version and flag it for my review before committing.
4. `LTG_ENV_grandma_kitchen.png` — The kitchen is the show's most "hand-drawn-looking" environment by design. Real World treatment only. Good test case for the paper grain and warm edge bleed.

**Output naming convention:** append `_styled` to the source filename before the version extension. Example:
- Source: `LTG_COLOR_styleframe_glitch_storm.png`
- Stylized output: `LTG_COLOR_styleframe_glitch_storm_v005_styled.png`

All stylized outputs go to the same directory as their source.

---

## Technical Spec

**Tool to build:** `output/tools/LTG_TOOL_stylize_handdrawn.py`

**Function signature (recommended):**
```python
def stylize(
    input_path: str,
    output_path: str,
    mode: str = "realworld",   # "realworld" | "glitch" | "mixed"
    intensity: float = 1.0,    # 0.0–2.0 global intensity multiplier
    seed: int = 42,            # seeded for reproducibility
) -> None:
```

**Requirements:**
- PIL/Pillow only (primary), NumPy allowed for noise field generation
- Must produce identical output for identical inputs + seed
- No external data files — all textures must be procedurally generated
- Compatible with `LTG_TOOL_render_lib.py` (Kai Nakamura's library). Import from there if any shared primitives apply.
- All outputs at the same pixel dimensions as input — no scaling
- Must handle both 1920×1080 and 1280×720 inputs

**Color preservation rule:** The stylization pass must not shift the dominant hue of any region by more than 5° on the color wheel. The master palette colors (`#D4923A` SUNLIT_AMBER, `#00D4E8` BYTE_TEAL, `#6A0DAD` UV_PURPLE, `#FF8C00` CORRUPT_AMBER, `#0A0A14` VOID_BLACK) must remain recognizable after treatment.

---

## Quality Benchmark

**Test your stylization at thumbnail scale (480px wide).**

If the image reads as:
- Warmer and more tactile than the raw render → you're on the right track
- "Like a Photoshop filter was applied" → too strong or too generic, pull back
- Indistinguishable from the raw render → too subtle, push harder

The target is: a developer in a pitch meeting glances at the slide and thinks *"this looks hand-made"* before they consciously register why.

---

## Reporting

When done:
1. Deliver the tool to `output/tools/`
2. Deliver all stylized PNGs to their source directories (see naming above)
3. Send me a completion report in my inbox with:
   - Which assets were treated
   - Any decisions you made that deviate from this brief (with rationale)
   - Any assets you flagged for my review before finalizing

This is a first-pass tool. Expect revision direction after I review the output. Build it so it's easy to tune — parameterize intensity rather than hardcoding.

---

*Alex Chen, Art Director — Cycle 23 — 2026-03-29*
