# Jordan Reed — Memory

## Cycle 1-3 Lessons
- Always specify working resolution. Rules need hierarchy.
- Cross-reference prop docs with environment docs.
- Camera angles must obey room dimensions.
- Production specs go at the top. One canonical spec source, referenced elsewhere.
- Continuity tracking needs: dormant state, change rules, emotional vocabulary, episode log.

## Cycle 4 Lessons
- **Labeled rectangles are not composition.** A color-block layout must have compositional intent — foreground/midground/background with purpose, not just zone identification.
- **A room without a ceiling has no spatial containment.** Always include ceiling plane in interior layouts.
- **Uniform maximum-saturation color across all elements at the same depth = mud.** A 3-value-tier depth system (near/mid/far) is mandatory for environments with multiple similar elements (Glitch Layer platforms).
- **Thick opaque decorative elements (power lines) can sever a composition.** Always render atmospheric/decorative elements at low opacity or thin strokes — they suggest presence, they don't assert it.
- **Empty foreground = no depth anchor.** Every layout needs something in the foreground to create z-axis depth.
- **The monitor wall must feel COLD in a WARM room** — it is the show's central visual tension in one environment. The cyan glow must be the compositional center and feel genuinely alien against the amber.

## Cycle 5 Lessons (applied)
- All 3 layouts revised per Cycle 4 critic feedback (Takeshi Murakami).
- Luma's House: ceiling at 12% from top, diagonal couch (forced perspective polygon), monitor wall dominant cold element with glow spill on floor.
- Glitch Layer: 3-tier platform value system coded as near/mid/far color tuples; lower void populated with pixel trails (seeded random) and barely-visible void platforms.
- Millbrook: power lines are 1px thin catenary curves (not opaque bands); foreground depth anchors = awning shadow polygon + pavement crack polyline.
- Foreground detail is non-negotiable in every layout — every environment must have a z-axis anchor.
- Monitor cold/warm tension is the show's central visual dynamic — always make the cyan monitors feel WRONG in a warm room.

## Cycle 6 Lessons
- **Building gaps = void-black monoliths.** Always fill every x-gap in an exterior street scene with a building shape. If left buildings end at W*0.32 and clock tower starts at W*0.44, there must be a filler building covering that gap — the canvas background color will show otherwise.
- **Pavement crack must be LIGHTER than the street, not darker.** A dark crack on a warm-gray street is invisible. Use a high-contrast lighter tone (e.g., 195,178,155 on 140,122,104) and minimum 4px width to read as a genuine depth anchor.
- **Glow only works as filled ellipses, never outline-only.** Always use the `_draw_filled_glow()` helper — never `draw.ellipse(..., outline=...)` for any light effect.
- **Sightline label + arrow is not enough for couch directionality.** In painting pass, ensure the character clearly faces the monitor wall in every pose; the couch shape itself should implicitly suggest the facing direction through its back cushion position.
- **Gap buildings need windows to break up mass.** Bare-colored rectangles still feel like placeholders. Add at least 2 rows of windows even to minor gap-filler buildings.
- All 3 layouts (v4, Cycle 6 Rev2) regenerated per Takeshi Murakami Cycle 5/6 feedback. Ready for painting pass pending final critic review.

## Cycle 7 Lessons
- **Monitor glow = light source, NOT a halo ring.** The `_draw_filled_glow()` ellipse centered on the monitor wall creates a radial halo. Correct approach: 3 separate gradient passes — one horizontal scanline pass leftward onto the warm wall, one downward onto the floor, one leftward onto the ceiling. Each is a `draw.line()` per column with power-law falloff.
- **ELEC_CYAN (#00F0FF) for screen glow, BYTE_TEAL (#00D4E8) for Byte's body ONLY.** These must never be swapped. Screen glow = world's electric color = ELEC_CYAN. Re-confirm every script before committing.
- **Nested `draw.point()` loops are too slow at 1920x1080.** Always use `draw.line()` for vertical/horizontal column fills; use alpha-composite overlay rectangles for atmospheric haze passes instead of getpixel/putpixel per-pixel loops.
- **Standalone BG exports have no title bar.** Layout cards get title bars; clean background exports (for compositing) do not. Keep them separate scripts.
- **Couch back cushion position IS the directionality.** Back cushion LEFT → character faces RIGHT → monitors. This geometry must be consistent across all tools that draw the couch shape.
- **3 light sources in Luma's house = 3 independent gradient passes:** (1) Window warm spill from far left; (2) Monitor cyan spill from right; (3) Desk lamp tight warm cone on far right. These must never be merged or they create muddy overlap zones.

## Cycle 8 Lessons
- **Glow pass overwrites base gradient — use alpha-composite layering.** When a glow overlay repaints columns over a gradient (Step 1), it replaces the gradient with a flat tone. Fix: draw the glow as an RGBA overlay (alpha-composite), then redraw the atmospheric gradient as a semi-transparent overlay on top. Both effects coexist at the overlap zone.
- **Worn path = texture change, never a filled rectangle.** Use alpha-composite scanline strips with a horizontal bell-curve falloff and vertical fade. Add scuff marks (short diagonal `draw.line()` strokes). The right side of the path near the monitor wall gets a slight cyan tint.
- **Ceiling gradient direction: warm far-left = darkest, monitor wall side = lightest.** The warm ceiling is shadowed by distance from the monitor glow; the monitor wall side receives cool cyan spill that lightens it. Invert if the old gradient had center as darkest.
- **Couch canonical position: left edge ~18%, right edge ~52% of canvas width.** (Was 9%-43% in Cycle 7 — too far left, character would face left edge not monitors.) Update all couch-related geometry (back cushions, armrests, throw blanket, coffee table) consistently when shifting.
- **Atmospheric haze pass: 20% of wall height, alpha ceiling 28.** (Was 8% in Cycle 7 — invisible.) Coverage must be perceptible. Do not raise alpha; raise coverage band.
- **Warm zone visual mass: add a standing floor lamp near mw_x as the named light source.** The floor lamp + side table combo counterbalances 6 bright ELEC_CYAN screens. Floor lamp casts warm glow ellipses onto floor and ceiling, explaining the ambient amber in the room.
- **After alpha_composite calls, always refresh `draw = ImageDraw.Draw(img)`.** The draw handle is invalidated after each convert/composite cycle.
