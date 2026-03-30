# Background & Environment Critique — Cycle 7
**Critic:** Takeshi Murakami | Background Art Director
**Date:** 2026-03-29
**Subject:** Cycle 7 Review — `bg_house_interior_frame01.py` and `bg_layout_generator.py` monitor glow fix
**Code reviewed:**
- `/home/wipkat/team/output/tools/bg_house_interior_frame01.py` (new standalone interior, Cycle 7)
- `/home/wipkat/team/output/tools/bg_layout_generator.py` (Cycle 6 rev2, monitor glow fix)

---

## Preamble

I have been reviewing Jordan Reed's work since Cycle 4. I have watched this artist absorb increasingly specific technical corrections and apply them with growing precision. In Cycle 5 the glow was rings. In Cycle 6 the glow became a filled gradient. In Cycle 7 a standalone compositing-ready interior background has been delivered, built ground up, 700 lines, with every major Cycle 5 and 6 note addressed in the code.

I will say this plainly before I say anything else: `bg_house_interior_frame01.py` is the most complete environment asset this team has produced. It does several things correctly that no prior cycle asset accomplished. It also contains failures that must be addressed before this asset goes into production compositing.

I will be specific. I always am.

---

## Section 1: What Was Fixed — Cycle 5/6 Notes Addressed

### Monitor Glow: From Rings to Light Source

This was my most urgent Cycle 5 technical note. The Cycle 5 implementation drew concentric `outline=` ellipses, producing topographic ring artifacts. In both the new standalone file and the updated `bg_layout_generator.py`, the glow is now a proper tri-plane light source:

- **Wall spill:** A per-column scanline gradient bleeds cyan tint leftward from the monitor wall boundary across the entire warm wall height. The falloff uses a `(1 - t) ** 1.4` power curve, which is physically plausible and visually distinguishable from a flat gradient. This reads as light in the new file.
- **Floor spill:** The floor receives a `(1 - t) ** 1.8` falloff gradient sweeping right-to-left. The code correctly transitions from `FLOOR_GLOW_ZONE` under the monitor wall itself to `FLOOR_BASE` in the ambient zone, which sells the idea that the monitors are actually illuminating the floor beneath them first and then casting laterally.
- **Ceiling spill:** A ceiling gradient of `(1 - t) ** 1.5` pushes cyan across the ceiling plane from the monitor wall. The redraw order — glow layers first, monitor casings and screens on top — is correct. The glow bleeds around the bezels rather than being buried under them.

In `bg_layout_generator.py`, the same three-plane approach has been applied to replace the old Cycle 5 ring implementation. The label at the bottom of the monitor zone — "Monitor glow — LIGHT SOURCE spill (floor/ceiling/wall)" — is not just documentation. It is evidence that the artist now understands what was being asked.

**This is a genuine fix. The monitor wall now reads as a light source, not as a glowing rectangle.**

### Couch Facing Monitor Wall

Cycle 5 produced a couch that a character sitting in would face a blank amber wall, with monitors at peripheral. That note has been addressed. The Cycle 7 interior positions the couch as a four-point perspective polygon whose right side is closer to the monitor wall, back cushion on the left, armrests visible, with a throw blanket draped over the open right arm. The forced-perspective geometry correctly implies a character seated here would face rightward toward the screens. This is the spatial relationship the production bible requires.

### Individual Cables, Not a Band

The Cycle 5 cable layer was three arcs against a uniform dark band. The Cycle 7 implementation provides nine distinct cable definitions with individual colors, radii, base heights, sag values, and widths — including the "origin cable" (thick orange braided, 3px) which is a production detail that signals someone is thinking about what these objects *are*, not just that they exist as a visual category. The cables originate from the monitor wall `x = mw_x` region and run leftward at different arcs, correctly implying they terminate at devices off-left. The foreground strip also includes a couch back sliver at the absolute bottom edge, which pulls the viewer into the space.

### Atmospheric Perspective — Applied in Multiple Systems

The Cycle 5 warm wall was flat rectangles. The Cycle 7 interior applies atmospheric perspective in four distinct ways:

1. Per-scanline wall gradient from `WALL_FAR` (top, lighter/desaturated) to `WALL_MID` (bottom, richer).
2. Shelf books desaturated by `atmos_factor * si * 0.06` per shelf tier, correctly making upper shelves (farthest from viewer) slightly washed out.
3. A dedicated haze overlay pass in Step 11: RGBA alpha compositing with a gradient from alpha 28 at ceiling line down to zero, applied over the top 8% of the warm wall.
4. The ceiling itself receives a warm gradient (lighter at top, deeper at the wall join) suggesting the ceiling plane is farther from the viewer's eye level.

This is a systematic application, not a checkbox. The team has internalized the concept.

---

## Section 2: What Works in the New Standalone Interior

### Spatial Division — Warm/Cold

The 58%/42% warm-left/cold-right split is proportionally correct. The divider line at `mw_x` is drawn with a 4px dark line in (40, 32, 60), which is distinct from both the warm wainscot behind it and the monitor wall void ahead. The transition is visible. The room has two territories. This was my core compositional demand from Cycle 4 and it is now delivered.

### Monitor Screen Rendering

The screens are rendered in three layers: a per-scanline gradient (ELEC_CYAN to deeper cyan at edges), an overdrawn scanline texture every 4px, and a center-brightest hotspot glow using `_draw_filled_glow`. The CRT casing geometry uses double rectangles — outer void casing, then a CRT_CASING (yellowed plastic), then screen glass recess — which produces a bezel with physical depth. The fact that the per-screen glow is drawn *before* the casings are redrawn means the glow halos bleed past the bezels into the monitor wall background, which is physically correct behavior for a backlit CRT panel.

### Room Furniture Coherence

The coffee table has items: a magazine stack and a mug with a handle drawn as a separate line element. The desk has roll-top slats, a USB hub, a circuit board shape, a keyboard with individual key nubs, and a cable drawer cabinet with a 4x5 drawer grid. The wall clock has hands indicating a specific time. The window has a curtain rod with finials, fold lines on the curtain fabric, and a warm light spill pool cast onto the floor below. These details are not generic room furniture. They describe a specific person's specific room — which is what background design is supposed to do.

### The Origin Cable

This is a small thing that tells me a lot. The orange braided cable in the foreground cable layer is labeled "origin cable — Grandma's special orange braided" in the CABLE_COLORS comment. An artist who names a prop — who gives a floor cable a story — is thinking about the world, not the layout. That is the right direction.

---

## Section 3: What Still Fails

I will be direct. The below are not minor polish items. Several are architectural decisions that will create visible problems in compositing.

### Critical Problem 1: The Warm Wall Glow Spill Overwrites the Atmospheric Gradient

The monitor wall glow spill (Step 4, approximately lines 294–306) draws per-column scanlines from `mw_x` leftward across the full warm wall height. This pass is drawn AFTER the atmospheric wall gradient in Step 1. The glow pass uses a single representative `warm_mid` color computed from `_lerp_color(warm_at_x_top, warm_at_x_bottom, 0.5)` — a static midpoint. It does not sample the per-scanline gradient color from Step 1. The result is that the glow spill paints the warm wall with a color that is neither the correct top-of-wall desaturated tone nor the correct bottom-of-wall rich amber. It is a single mid-tone blended with cyan applied uniformly from ceiling to floor. This flattens the atmospheric gradient in exactly the region of highest compositional interest — the boundary zone between warm and cold territories. The glow should modulate *on top of* the existing wall gradient, not replace it with a uniform base color.

This is a layering error. The atmospheric work from Step 1 is partially destroyed by Step 4.

### Critical Problem 2: The Worn Path Rectangle Destroys the Floor Lighting Logic

Step 3 draws the monitor floor spill correctly as a power-law gradient. Then, at lines 256–258, a flat rectangle `FLOOR_LIGHT` (a lighter honey oak color) is stamped over the floor center — "Worn path on floor (lighter, center aisle)." This rectangle runs from x=0.18W to x=0.52W, which is almost the entire warm-side floor, at full flat opacity, with no gradient. It covers the floor area immediately adjacent to the couch. The worn path is logically correct as a storytelling element — repeated foot traffic from couch to monitor desk would polish that zone. But a flat rectangle at a uniform lighter color does not look like a worn path. It looks like a dropped piece of lighter-colored flooring. The worn path needs to be applied as a gradient (brighter at the walking centerline, fading to the floor tone at the edges) and it should interact with the cyan glow from the monitor side — the wear zone closest to the monitor wall should be slightly warmer-lit from above, not simply lighter wood.

### Critical Problem 3: The Ceiling Shadow at Room Center Works Against Depth

Lines 221–223 draw a horizontal gradient rectangle from `x=0.35W` to `x=0.58W` across the ceiling, explicitly labeled "depth cue — ceiling is lower in middle." The color steps from `(190, 155, 90)` to `(160, 120, 65)`. This is the darkest zone of the ceiling, and it sits at the exact center of the composition's horizontal axis. The result is compositionally damaging: the ceiling is brightest at the extreme left (warm side) and darkest at the room's center, which is the transition zone between warm and cold. The ceiling should be darkest on the warm side (where it is furthest from the monitor light) and coolest-lit and slightly brighter near the monitor wall where the glow reaches up. The current implementation creates a dark band across the ceiling center that draws the eye to a dead zone. It is fighting the lighting logic rather than supporting it.

### Significant Problem 4: The Couch Back Geometry Places the Back Cushion Incorrectly

The couch back (lines 518–525) is a polygon anchored at x=0.09W to x=0.22W, covering the left portion of the couch. The comment says "character faces RIGHT toward monitors." Logically correct. However the back cushion is only 13% of the canvas wide and is positioned entirely in the leftmost section of the room. In the rendered composition, the couch back will read as a small vertical element at the far left edge, and the main visible couch surface will be the broad seat polygon from 9% to 43% of the canvas width. At the scale characters are composited, the couch back will be pushed to the very edge of the visible safe area. A character seated on this couch will appear to have the monitor wall essentially behind them in a wide shot, rather than in their sightline. The couch needs to be shifted rightward in the frame — its left edge at approximately 0.14W and its right edge at approximately 0.48W — so that the body of the couch is in the compositional center of the warm zone, not crammed against the left wall.

### Moderate Problem 5: The Desk Lamp Glow Uses Correct Technique but Wrong Geometry

The desk lamp (lines 597–615) draws a `_draw_filled_glow` pool with `rx=70, ry=18` centered at `(lamp_bx + 50, desk_y + 4)`. The glow center is positioned at the top of the desk surface, which is correct for a downward-pointing desk lamp casting a pool onto the desk. The radius values (70x18) produce a wide flat ellipse. This is the correct visual idea. The problem is that the lamp glow is blended against `bg_rgb=DESK_WOOD`, and the desk is in the cold zone to the right of `mw_x`. The monitor wall ambient glow has already been painting that surface with cyan-tinted light. The warm desk lamp glow competes with the ambient cold glow in an unresolved way — there is no blending logic that reconciles the warm lamp pool and the cold monitor ambient. In production, this will create a visible warm-over-cold smear that reads as incorrect. The desk lamp needs to be placed within the cold zone's dominant lighting logic: the warm pool is correct as a local accent, but it should be represented as a small island of warmth within the larger cold floor glow, not as a separate gradient pass that ignores the surrounding light.

### Moderate Problem 6: The Haze Pass Coverage Is Too Narrow

The Step 11 atmospheric haze covers only the top 8% of the warm wall above the ceiling line (`haze_y_bot = ceil_y + int(H * 0.08)`). The alpha reaches maximum 28 at the ceiling join. This is better than nothing — it is the first time a dedicated haze pass has appeared in this pipeline. But 8% of the wall height is approximately 70 pixels of the visible wall area. The atmospheric effect is confined to a thin band that most viewers will not consciously register. For the haze to function as a depth cue, it needs to cover at least the top 20% of the wall surface — the full "back wall far distance" zone that the per-scanline gradient describes but the haze should reinforce. The maximum alpha of 28 is correct; the coverage height is insufficient.

### Minor Problem 7: No Left-Side Counterweight to the Monitor Wall's Visual Mass

The warm zone contains a window (3% to 16% from the left edge), bookshelves (19% to 55%), a couch, and a coffee table. The monitor wall in the cold zone contains six monitors, a desk, a drawer cabinet, and a keyboard. The cold zone's visual complexity — six bright ELEC_CYAN rectangles plus CRT casings plus monitor wall panels — creates significantly more visual activity than the warm zone. The warm zone should feel settled and domestic against the cold zone's hyperactive screen light. At present the warm zone reads as sparse amber rectangles against an aggressively lit cold wall. The warm zone needs more texture depth — fabric suggestion on the couch upholstery, a second framed item on the wall (a small photo, a pinned drawing), or a floor rug to break the uniformity of the dark floor. The domestic warmth must visually hold its own against six glowing screens or the compositional tension collapses into visual dominance by the monitors.

---

## Section 4: Assessment of `bg_layout_generator.py` Monitor Glow Fix

The Cycle 6 layout generator's monitor glow update correctly replaces the old ring implementation with the same three-plane spill logic used in the standalone interior. The implementation is consistent between the two files, which is good pipeline hygiene. The layout pass uses slightly different falloff exponents (`**1.5` for wall vs `**1.8` for floor vs `**1.6` in the standalone) which is acceptable variation for a layout-level approximation. The redraw order — glow passes, then casings, then screens, then labels — is correct.

One note: the layout generator version still uses the `ceiling_y = int(H * 0.12)` / `wall_bot_y = int(H * 0.55)` zone definitions without a wainscot subdivision (the standalone uses `wainscot_y = int(H * 0.56)` and `floor_y = int(H * 0.74)` separately). This is a minor inconsistency between the layout card and the standalone that should be harmonized before the layout card is used for production reference.

**The monitor glow fix is real. The layout generator now reads as a lit room, not a colored chart.**

---

## Section 5: Verdict and Grade

**Overall Grade: B**

This is the first environment asset from this team that I consider structurally production-ready. The spatial division is correct. The lighting logic is understood and implemented in three planes. The room contains a specific person's specific life. The atmospheric perspective has been applied systematically, not as a checkbox. The glow is filled and graduated. The cables tell a story.

The B grade reflects that several of the above problems — particularly the wall gradient overwrite by the glow spill, the worn path rectangle, and the ceiling shadow — are architectural errors in the rendering order that will produce visible failures in compositing. A production-ready background cannot have its most important atmospheric layer partially destroyed by a subsequent pass. These must be fixed before this file is handed to the compositing pipeline.

The work shows genuine artistic growth. What was broken in Cycle 5 has been repaired with understanding, not just compliance. Jordan Reed now understands what a monitor wall is supposed to do to a room. That conceptual shift is irreversible and I acknowledge it clearly.

**What is still required for production approval:**

1. Fix the glow spill scanline logic so it modulates on top of the existing per-row gradient color, not over a static mid-tone.
2. Replace the worn path flat rectangle with a gradient-edged ellipse or trapezoid that interacts correctly with the floor glow.
3. Invert the ceiling center shadow — darken the warm-side ceiling (far from monitor light), lighten near the monitor wall.
4. Shift the couch body 5-10% rightward in the frame to move it out of the left-edge zone and into the compositional center of the warm territory.
5. Extend the atmospheric haze pass from 8% to 20% wall height coverage.
6. Add one more domestic detail to the warm zone (a rug, a pinned drawing, a floor plant) to visually balance against the six monitor screens.

This is the first time I have issued actionable production notes rather than structural rebuilding notes. That is meaningful progress.

Fix these six items. Then this background is ready.

---

## Final Note to the Team

There is a detail in this file that I want to name explicitly. The orange braided cable in the foreground is called "Grandma's special orange braided" in the source code comments. It is 3 pixels wide and runs from the monitor wall toward the left side of the frame. No viewer will read that comment. But the artist who wrote it knows whose cable that is. That knowledge shaped how they drew it — the weight (3px), the color (warm orange against cold cyan surroundings), the placement (the thickest cable in the foreground cluster, grounding the scene in something human and inherited).

That is what background design is. You are not drawing rooms. You are drawing evidence of the people who lived in them. This cable is evidence. More of that, please.

---

*— Takeshi Murakami*
*Background Art Director | "Luma & the Glitchkin" Cycle 7 Review*
