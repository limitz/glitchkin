**Date:** 2026-03-29 18:00
**To:** Jordan Reed — Background & Environment Artist
**From:** Takeshi Murakami — Background Art Director (Critic)
**Subject:** Cycle 7 Critique — `bg_house_interior_frame01.py`

---

Jordan,

My full critique is at `/home/wipkat/team/output/production/critic_feedback_c7_takeshi.md`. Read all of it. Below is a direct summary.

**Grade: B**

This is the strongest environment work this team has produced. I want to be clear about what you have done correctly before I tell you what to fix.

**What you got right:**

The monitor wall is now a genuine light source. Three planes — wall spill, floor spill, ceiling spill — each with a distinct power-law falloff, drawn in the correct order so the glow halos bleed around the bezels. This is what I asked for in Cycle 5. It took two full cycles to arrive here and it is now correct.

The couch faces the monitors. The atmospheric perspective is applied in four distinct systems (wall gradient, shelf desaturation by tier, dedicated haze pass, ceiling gradient). The cables are nine individual story elements. The room contains a specific person's specific life: a magazine, a mug with a handle, a keyboard with key nubs, drawer pulls on the cabinet, a wall clock with hands showing a time, curtain fold lines, rod finials.

The orange braided cable labeled "Grandma's special orange braided" tells me you are thinking about the person who lives here. That thinking is visible in the rendered work, even without the comment. Keep doing that.

**What you must fix before this background enters the compositing pipeline:**

1. **The wall glow spill destroys your atmospheric gradient.** Your Step 4 glow pass draws scanlines using a static `warm_mid` color — a single interpolated midpoint — as the base for the warm wall columns it paints. This overwrites the per-row gradient you built in Step 1 with a uniform flat tone in exactly the zone where warm meets cold. You need to sample the per-row color from Step 1 when drawing the glow modulation in Step 4, not use a static representative color. The atmospheric work you did must survive the glow pass, not be replaced by it.

2. **The worn path is a flat rectangle.** `FLOOR_LIGHT` stamped as a solid rectangle from 18% to 52% of the canvas looks like a patch of lighter flooring, not wear. Use a soft-edged trapezoid or gradient ellipse, tapered at the edges. The worn zone closest to the monitor wall should also have a slight cyan tint from the ambient light above it — the wear and the light interact in the real world.

3. **Your ceiling center shadow is fighting your light logic.** You draw a gradient rectangle across the ceiling center (35%–58% of canvas) that makes that zone the darkest part of the ceiling. The ceiling center is the transition zone between warm and cold light — it should not be a dark band. Make the warm-side ceiling (far from monitors) darker; let the ceiling become progressively cooler and slightly lighter as it approaches the monitor wall where the cyan glow reaches.

4. **The couch is too far left.** Your couch body runs from 9% to 43% of canvas width. When a character is composited onto that couch, they will appear to face the left edge of frame, not the monitor wall. Shift the entire couch assembly rightward — left edge at ~14%, right edge at ~48%. The couch back can shift accordingly.

5. **Your haze pass is too narrow.** The Step 11 atmospheric haze covers only the top 8% of wall height. Extend it to 20%. The alpha ceiling of 28 is correct — do not raise it, just extend the coverage band.

6. **The warm zone needs more visual mass.** Six ELEC_CYAN monitor screens are bright and complex. The warm zone has bookshelves and a window and a couch, but visually it reads as sparse amber against a wall of light. Add one more domestic detail: a floor rug under the coffee table (even a simple texture approximation), a pinned drawing on the warm wall, or a small potted plant near the window. The warm zone must visually hold its own or the tension collapses.

These are not conceptual problems. They are engineering corrections on top of a foundation that now works. The room you have built is real. These six items are preventing it from being correct.

Fix them. This background will be approved.

One more thing: the orange braided cable is the best single detail you have produced on this project. More of that thinking across every element.

— Takeshi Murakami
