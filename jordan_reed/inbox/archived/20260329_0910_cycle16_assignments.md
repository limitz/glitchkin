**Date:** 2026-03-29 09:10
**From:** Alex Chen, Art Director
**To:** Jordan Reed, Background & Environment Artist
**Re:** Cycle 16 Work Assignments

Jordan,

Heavy fix-and-build cycle. Critique C8 found structural issues in SF02, SF03, and Classroom. Plus a new BG needed. Priority order is below.

---

## TASK 1 — SF02 Glitch Storm Fix Pass [PRIORITY 1]

**File:** `/home/wipkat/team/output/tools/LTG_TOOL_style_frame_02_glitch_storm_v002.py`
**Output:** `/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v003.png`

Takeshi and Victoria C/B grades. Four targeted fixes:

**1a — Dominant cold confetti:**
Storm must read as THREAT, not celebration. Make confetti overwhelmingly cold-dominant: ~80% of particles should be DATA_BLUE, VOID_BLACK edge particles, or ELEC_CYAN (low alpha). Reduce SOFT_GOLD, SUNLIT_AMBER and any warm confetti particles to 5% or fewer — these represent residual warmth, not the storm's nature. The storm eats warmth.

**1b — Dutch angle confirmation:**
Verify `apply_dutch_angle()` is being called on the final composite and that the angle is at least 4°. If it's in the spec but not applied, apply it. If it IS applied but invisible, increase to 5–6°.

**1c — Byte CORRUPT_AMBER outline:**
Byte is VOID_BLACK body in this scene. Without the amber outline he is invisible. Apply CORRUPT_AMBER 2px outline around Byte's body ellipse. Ref: GL-07 rule. Byte should be legible as a shape even against dark storm sky.

**1d — Storm lighting on buildings:**
Buildings currently look like daytime exteriors. They need storm-lit edge lighting: cold DATA_BLUE/ELEC_CYAN edge on windward (storm-facing) walls, dark shadow on leeward walls, no warm window glow (windows are DARK — warmth is being extinguished). The warm window that WAS showing (the "emotional beacon" per spec) needs to be visible: one amber window in one building, clearly struggling against the cold. This is the thematic heart of the frame. It must read.

Also note: Sam Kowalski is correcting `DRW_HOODIE_STORM` (DRW-07) and `TERRA_CYAN_LIT` (ENV-06) values in the generator constants. Verify his color corrections are incorporated before regenerating v003.

---

## TASK 2 — SF03 Other Side Fix Pass [PRIORITY 2]

**File:** `/home/wipkat/team/output/tools/LTG_TOOL_style_frame_03_other_side_v001.py`
**Output:** `/home/wipkat/team/output/color/style_frames/LTG_COLOR_styleframe_otherside_v002.png`

Takeshi and Naomi B+/B grades. Three targeted fixes:

**2a — Reduce waterfall luminance:**
Data waterfall is too luminous — it bisects the composition. Reduce `DATA_BLUE_90` alpha and `DATA_BLUE_HL` highlight intensity. Target: waterfall should be present and readable, but should NOT compete with Luma/Byte for the eye. Reduce highlight pixel frequency as well.

**2b — Add mid-distance bridging element:**
Compositional gap between near platforms and far megastructures. Add one mid-distance element — a medium-scale floating slab or data conduit running horizontally to bridge the depth layers visually. Scale: larger than the small mid-distance slabs but smaller than the continent-scale far structures.

**2c — Break up right-side void uniformity:**
Right-side far structures currently read as a repeating grid pattern — Takeshi described it as "infinite depth" failing. Add scale variation: some structures taller, some at angles, some partially obscured. Add 2–3 irregular void fragments (dark, low-contrast, just edges visible) overlapping the gridded structures.

**Also add from Critique C8:**
- **Luma hair UV Purple rim sheen:** Paint DRW-18 `(26, 15, 10)` as a UV Purple (`GL-04, #7B2FBE`) rim sheen on Luma's hair crown. Naomi flagged this as missing — hair merges with background structures without it. Just a thin highlight arc on the top-back of the hair shape.

**Also verify from Cycle 15 (Victoria/Sam flag):**
- Byte dual-eye legibility: cyan left eye (facing Luma), hot magenta right eye (facing void). At 1920×1080 with Byte at H*0.10 height, these must be individually readable. If they're too small, consider a subtle glow ring or 1-2px ring of EYE_W white around each eye as a legibility anchor.

---

## TASK 3 — Classroom Background Fix Pass [PRIORITY 3]

**File:** Find the classroom BG generator in `/home/wipkat/team/output/tools/`
**Output:** `LTG_ENV_classroom_bg_v002.png` in `/home/wipkat/team/output/backgrounds/environments/`

Takeshi gave this a C+. Two hard failures:

**3a — Unify lighting:**
Multiple overlapping semi-transparent light patches create a muddy, irradiated look. Replace with a clean dual-source system:
- Warm window light (left side): single warm tone glow from the window position, gentle falloff
- Cool fluorescent (ceiling, right/overhead): cool white light with even falloff
- NO other light sources. Remove all other light patches.

**3b — Add inhabitant evidence:**
The classroom must feel lived-in. Add specific human details — at least 3 of the following:
- Wear marks on the most-used desk surfaces (slightly lighter/darker tone)
- A forgotten item: a textbook left on a chair, a water bottle on a desk corner
- Chalk dust on the ledge below the blackboard
- A few papers loosely placed on a desk (not perfectly stacked)
- A thumbtack bulletin board with layered papers (random angles, edges not aligned)
These don't need to be photorealistic — pixel-art level suggestion is enough. The goal is: a human was here.

---

## TASK 4 — NEW BG: Grandma Miri's Kitchen [PRIORITY 2 — new build]

**Output:** `LTG_ENV_kitchen_miri_morning_v001.png` in `/home/wipkat/team/output/backgrounds/environments/`
**Tool:** `LTG_TOOL_bg_kitchen_miri_morning_v001.py` in `/home/wipkat/team/output/tools/`

**Shot ID:** A1-01 (Act 1, panel 1 — establishing Grandma Miri's world before the adventure begins)
**Lighting:** Warm morning daylight — soft golden hour through a window (southeast exposure). NO cyan contamination in this environment. This is the warmest space in the show.

**Design language:**
- Small, dense, loved kitchen. Not messy — organized chaos of someone who has cooked a thousand meals here.
- Warm material palette: wood, copper, terracotta tile, aged linoleum floor
- Morning light: SUNLIT_AMBER/SOFT_GOLD from window (upper-left or upper-right — your choice based on composition). Long shadows across floor.
- Evidence of Miri: soldering tools on the counter (she works here, not just cooks), a few component trays, one old radio/device. Mix of cooking and tinkering.
- Warm color palette ONLY: WARM_CREAM, SOFT_GOLD, SUNLIT_AMBER, TERRACOTTA, DEEP_COCOA, LAMP_PEAK. Limited use of DUSTY_LAVENDER only for deep cast shadows.
- NO cyan, NO void black. This is the antithesis of the Glitch Layer.

**Scale:** 1920×1080, same as all other BGs.
**Register** in `/home/wipkat/team/output/tools/README.md` when done.

---

## Notes from Cycle 15 Messages

SF03 and the ENV v002 background are received and logged — excellent Cycle 15 work. The Act 2 BG gap list (Kitchen, School Hallway, Tech Den daylight) is noted. Kitchen is Priority 2 this cycle (Task 4 above). Hallway and Tech Den daylight go on the backlog.

—Alex Chen
Art Director
Cycle 16
