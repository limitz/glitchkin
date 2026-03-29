# Takeshi Murakami — Critique Cycle 10
**Date:** 2026-03-29
**Focus:** Tech Den v003 (ltg_render_lib lighting), Grandma Miri Kitchen v002, Glitch Layer Frame v003 (CRT scanlines)

---

## 1. Tech Den v003 — `LTG_ENV_tech_den_v003.py` [B−]

This is a genuine step up from C+. The team heard the note. But hearing a note and resolving it are not the same thing.

**What has improved:**

The shift to `ltg_render_lib` is architecturally sound and I am glad to see it. `light_shaft()` replaces the inline `draw_light_shaft()` and the two implementations are functionally close — both use a core solid pass and a Gaussian blur feather pass. The lib version uses GaussianBlur radius 16 versus the inline version's radius 18, and splits the alpha ratio as 60%/40% versus 60%/45%. These are minor differences. The important thing is that the room now uses a shared, tested library, which means future refinements to the light shaft function improve all environments at once. This is correct production thinking.

`gaussian_glow()` replaces `soft_glow_overlay()`. The new implementation uses concentric ellipses with quadratic alpha falloff rather than decreasing-ellipse-count layering. The math at line 115 of the lib (`a = int(max_alpha * (1.0 - (i - 1) / steps) ** 2)`) produces a tighter hotspot and softer outer fade than the original. For monitor glow spill this is an improvement — the spill on the desk surface and chair back should now read as rooted in its source rather than floating.

The vignette as a final compositing pass is correct. A room at this level of detail needs frame containment. The strength=55 value is reasonable — not so heavy it reads as dramatic framing, not so subtle it disappears.

The jacket is present and properly isolated. The `alpha_composite` approach with the lavender polygon at full opacity (255) against a shadow layer at 120 is the right technique. The jacket shadow half pulls correctly to the right side, implying the light source is at left-frame (the window). The collar notch polygon and outline reinforce that this is a garment, not a blob of color. This is an honest fix — the jacket now reads.

**What has not improved enough:**

The light shaft geometry is my primary concern. The shaft is defined by:
- `SHAFT_APEX = (WIN_X1 + 5, mid_y - 50)` — right edge of a window that ends at x=115
- `SHAFT_BASE_LEFT = (WIN_X0, FLOOR_Y_FAR + 140)` — x=0, below floor line
- `SHAFT_BASE_RIGHT = (WIN_X1 + 330, FLOOR_Y_FAR + 110)` — x=445, below floor line

The shaft extends *below the floor line* (FLOOR_Y_FAR is approximately y=340; the shaft bases are at +110 and +140 below that, so y≈450-480). The floor is drawn and occupies this zone. The shaft therefore spills primarily onto the floor rather than cutting across the desk surface where characters work. In my C+ note, I was explicit: "the sunlight shaft should fall across the desk surface as a defined shape, touching the keyboard, grazing the edge of the CRT casing." The desk top is at DESK_TOP_Y ≈ 395. The shaft's base reaches that zone but only at the very apex of the triangle — the bulk of the light event is happening below the desk, on the floor, where no one will look during a scene with characters present.

The shaft also fans very wide — from x=0 to x=445 at base. This is a diffuse ambient wash, not a volumetric light event with a readable edge. At max_alpha=115 with the two-pass compositing (60% + 40% blurred), the peak contribution is approximately 115 × 0.60 + (115 × 0.40 blurred to near-zero at edges) ≈ 70 alpha on a 255 scale. That is approximately 27% opacity for the core shaft. On a warm wall base, this is visible. On the desk surface — which is already DESK_WOOD_TOP (148, 105, 58) in a warm register — the additional SUNLIT_AMBER at 27% opacity will be nearly invisible. The shaft needs to be narrower, taller, and positioned to bisect the desk zone clearly.

The warm column overlay (lines 724-731) — a horizontal gradient from left edge to x=320 — is a blunt instrument. At max alpha 30 it adds ambient warmth to the window side, but it does not replace the missing drama of a defined shaft landing on the desk. This overlay is doing the shaft's emotional work at a fraction of its atmospheric cost.

The monitor glow architecture is now more sophisticated — `gaussian_glow()` on the CRT center, `gaussian_glow()` on the chair back, plus direct rectangle compositing for the desk surface and shelving. The desk surface spill (the wide ellipse at lines 587-591) is drawn as a flat-alpha shape (alpha=50) across the entire desk top from x=60 to x=680. This is monitor glow as an area fill rather than monitor glow as a light event — it does not acknowledge the specific positions of the three monitor screens, which sit at different x positions with different glow temperatures. Monitor glow should hotspot behind each screen and fall off with distance. A single wide ellipse painted over the entire desk is atmospheric furniture.

**The jacket reads. The shaft does not land on the desk. The monitor glow lacks specificity.**

**Grade: B−.** Material improvement from C+ — the light sources now exist with intention rather than as suggestions. The jacket resolves. The lib architecture is correct. But the shaft geometry places the light event in the wrong zone of the frame, and the monitor glow spill is approximate where it needs to be precise.

---

## 2. Grandma Miri's Kitchen v002 — `LTG_ENV_bg_grandma_kitchen_v002.py` [A−]

This is substantially better and I will say so without hesitation.

**Floor linoleum (Improvement 1):** `draw_floor_linoleum_overlay()` adds a 60×60px tile grid at alpha 25 with warm brown GRID_LINE_COLOR (155, 138, 112, 25). The lines run both horizontal and vertical at flat-plane spacing, which is incorrect perspective — floor tiles should converge toward the vanishing point at vp_x=768, vp_y=410. However, at alpha 25 with warm brown ink, the incorrect perspective of the grid is barely visible. What is visible is texture, differentiation, age. The worn path trapezoid (alpha 20, warm buff) reads as 40 years of traffic from doorway toward the stove zone. The combination of checkerboard base (from `draw_floor_tiles()`), the flat grid overlay, and the worn path overlay produces a floor with genuine material complexity. This is a kitchen floor now. I see the linoleum.

There is still a problem: the two floor systems fight each other slightly. `draw_floor_tiles()` draws perspective-correct converging lines toward vp_x. `draw_floor_linoleum_overlay()` draws orthographic grid lines. At low alpha the conflict is subtle, but in the zone where both systems are active (the mid-floor) you get two contradictory spatial readings. Future pass: integrate or eliminate one system.

**Upper wall texture (Improvement 2):** The stripe overlay — STRIPE_A at alpha 12, STRIPE_B at alpha 15, 12px stripes — is the right emotional register. Too strong and it becomes pattern; too weak and it disappears. At these alpha values it sits correctly in the zone of "texture you feel before you see." Applied to the upper 50% of the back wall (bw_top to bw_top + 50% of wall height), it correctly targets the zone that was previously undifferentiated cream mass. This fix works. The wall now has a period quality.

**CRT glow (Improvement 3):** The enhanced glow is well-judged. Primary radius increased from 60 to 80, with a second ambient ring at radius 130 (alpha falling from 8 to 1 in the outer band). The alpha math at line 544 (`int(t * t * 30)` for the primary ring) produces a peak of 30 — appropriate for a far-plane TV that must attract the eye without dominating. The wide ambient ring's peak of 8 barely registers, but atmospherically it matters — it suggests the room has been steeped in this blue light, not just touched by it. This is the difference between a prop and a story element.

The CRT body and screen are correctly scaled for the doorway geometry: `tv_x1 = door_x1 + 8%` of doorway width, `tv_x2 = door_x1 + 75%` of doorway width. This is visible but not large. The faint blue-green screen gradient (CRT_SCREEN_GLOW to a slightly darker value) reads as a screen in standby or with a static image. Floor spill ellipse under the TV adds grounding.

**What still limits this to A−:**

The upper wall texture is applied only to the back wall (`bw_left` to `bw_right`). The left wall (WALL_SHADOW polygon) and right wall (another WALL_SHADOW polygon) receive no texture treatment. In a wide-angle kitchen shot, the side walls are visible and they are still flat, undifferentiated WALL_SHADOW. The sense of "textured but not patterned" wallpaper should extend across all wall surfaces, slightly different in value due to the angled light, but consistently textured.

The floor grid overlay still does not correct for perspective. At alpha 25 this is forgivable in this version, but it is a structural error that accumulates with each pass. A perspective-correct grid would cost the same rendering time.

The note from C9 about the kitchen needing evidence of time — "a grandmother's kitchen should have evidence of time" — is not addressed in this pass. The objects are still positioned correctly but without the layer of lived history. This was not one of the three specified improvements for v002, so the team correctly prioritized the specified fixes. But this remains the ceiling on emotional impact.

**Grade: A−.** Three specified improvements executed well. The floor reads as linoleum. The wall reads as period wallpaper. The CRT glow reads as a story element. Side walls need texture treatment. The floor perspective conflict needs future resolution.

---

## 3. Glitch Layer Frame v003 — `LTG_ENV_glitchlayer_frame_v003.py` [B+]

The question I must answer: does the scanline overlay enhance or muddy? Is it the right technique?

**It is the right technique. The execution is correct but the debate is not over.**

The conceptual justification is sound and I will not dismiss it. The Glitch Layer is described as the interior of a CRT screen. If we accept this premise — and the production does — then scanlines are not a stylistic decoration. They are the fundamental physical property of the space. Characters inside the Glitch Layer live inside phosphor rows. The floor is scanlines. The sky is scanlines. Everything in this world is made of horizontal scan intervals. Applying `scanline_overlay(spacing=4, alpha=18)` as the final compositing pass is architecturally correct: it means the CRT property of the world is applied after all other rendering, touching everything uniformly. This is how it should work.

**spacing=4, alpha=18:** These values are conservatively chosen and that is the right instinct. At spacing=4, every 4th row receives a darkened line — at 1920×1080 this means 270 scanlines across the height of the frame. At alpha=18 on a 255 scale, each line reduces the brightness of the underlying pixel by approximately 7%. This is visible if you look for it; it does not assault the viewer who is not looking. The aurora bands — which are the Glitch Layer's most atmospheric element — will read through the scanlines with their full color, only their peak brightness slightly reduced. The electric cyan platforms will retain their edge sharpness. This is correct calibration.

**Where I am not fully satisfied:**

The scanline overlay is horizontal and uniform across the entire frame. This is CRT-accurate but it may be too literal. The Glitch Layer is not a consumer television displaying programming — it is a world. A world that happens to be structured like a CRT display. There is a difference between scanlines as a substrate texture and scanlines as a visible filter.

At spacing=4, the gap between scanlines is 3 pixels. At 1920px wide, this is a fine-pitch grid. For the aurora bands — which are rendered at pixel-level resolution (x-step=3) — the scanlines will create a subtle beat pattern with the aurora's own 3-pixel x-step. This is a happy coincidence that reinforces the electronic character of the space, but it is an uncontrolled interaction, not a designed one.

The ghost platforms in the lower void (lines 242-250) are drawn at 7-pixel height. With 4-pixel scanline spacing, each platform will be crossed by approximately 1-2 scanline events. This creates the correct impression of phosphor structures. This works.

The pixel flora clusters (size=5 pixels) will each be bisected by approximately one scanline, giving them a slight horizontal band. This is correct — pixel flora in a CRT world should feel like phosphor artifacts.

The one element I am less certain about: the near platforms (NEAR_COLOR = ELEC_CYAN) are rendered at 46-pixel height. With 270 scanlines across the frame height, approximately 10-12 scanlines will cross each near platform. At the platform edges (NEAR_EDGE highlight, width=2), the scanlines will visually slot between the highlight — 2 pixel line, 2 pixel gap, 2 pixel line — in a way that may look like the edge highlight is dotted rather than continuous. At alpha=18 this is probably not visible at normal viewing distance but at close inspection it may read as a rendering artifact rather than a design choice. I am flagging this, not condemning it.

**The deeper question:** Does the scanline overlay muddy the aurora? The aurora is the most delicate element in this frame — sinusoidal-modulated color bands at varying transparency, rendered per-pixel. Applying a uniform 7% darkening stripe every 4 pixels to this carefully constructed gradient risks turning an organic atmospheric event into a grid. At alpha=18 I believe this risk is managed. At alpha=25 or above, the aurora would be gridded. The team has chosen the conservative value. I accept it.

**Grade: B+.** Correct conceptual justification. Technically well-implemented. Conservative parameter choices are the right call for a first application of this technique. The interaction between the scanline frequency and the aurora/platform rendering frequencies is largely beneficial but not fully designed. A future pass should consider whether the scanline spacing should vary subtly across depth tiers — denser in the far plane (smaller effective CRT pixels at distance) and coarser in the near plane — to reinforce spatial depth through the CRT metaphor itself.

---

## Top 3 Priority Fixes

**1. Tech Den v004: Move the light shaft into the desk zone.**

The shaft apex must be repositioned so the majority of the shaft's area lands on and above the desk surface (DESK_TOP_Y ≈ 395). Currently the shaft fans below the floor line, placing the light event where characters do not occupy. The shaft should be narrower (perhaps 200px wide at its widest) and positioned so its brightest region crosses the desk diagonally from upper-left (near window) to mid-desk-right, fading before it reaches the bed zone. The desk surface is where Cosmo works. That is where the light must land. Make the max_alpha higher — 140 to 160 — for a shaft that has genuine presence. A daylight shaft in a dark room is not subtle.

**2. Tech Den v004: Individuate the monitor glow spill.**

Replace the single wide-ellipse desk spill with three separate `gaussian_glow()` calls — one per monitor — at the positions where each screen center falls on the desk surface. CRT1 (centered x≈195) should spill cool blue-white forward and slightly left onto the desk. CRT2 (centered x≈420) should spill onto the central desk area. The flat panel (center x≈635) should spill toward the oscilloscope zone. These three light sources create three zones of slightly different temperature on the desk — this is what makes a multi-monitor workspace feel inhabited. Currently the desk receives one uniform ambient wash. This must change.

**3. Kitchen v003: Extend wall texture to side walls and correct floor grid perspective.**

The upper wall stripe texture must be applied to the left wall polygon and right wall polygon, not only the back wall rectangle. Adjust the stripe alpha to account for the reduced illumination on side walls (WALL_SHADOW versus WALL_WARM — reduce alpha by approximately 30-40% on side surfaces). For the floor: integrate the two floor grid systems into one perspective-correct linoleum grid that converges to vp_x, or remove `draw_floor_tiles()` entirely and rely on `draw_floor_linoleum_overlay()` with a corrected perspective-aware grid. Two contradictory spatial grids on the same surface will eventually become visible.

---

*— Takeshi Murakami, Background Art Director*

*"The work is improving. That is not the same as the work being good. There is a difference between iterating on a note and actually solving it. The Tech Den light shaft is not solved — it is renegotiated. Solve it."*
