# Jordan Reed — Memory

## Cycle 17 Deliverables
- `LTG_TOOL_bg_tech_den_v001.py` → `LTG_ENV_tech_den_v001.png`
  - Cosmo's bedroom/tech workspace daylight version (A2-01, A2-03, A2-04, A2-05)
  - Desk dominant left, CRT+flat monitors, oscilloscope, breadboards, cables
  - Natural daylight LEFT window + blue-white monitor glow on desk zone
  - Bed pushed to right wall, dusty lavender jacket on chair
  - Canvas 1280×720, Real World palette only
- `LTG_TOOL_bg_school_hallway_v001.py` → `LTG_ENV_school_hallway_v001.png`
  - Millbrook School Hallway (A1-03, A1-05)
  - 3-point perspective, slight low angle, lockers both sides (sage + lavender alternating)
  - Checkerboard linoleum floor, fluorescent pools, SUNLIT_AMBER shaft from left window
  - Trophy case, classroom doors (terracotta), T-intersection with school seal, far daylight
  - Canvas 1280×720, Real World palette only

## Remaining Act Background Gaps (post Cycle 17)
- All A1 and A2 backgrounds now built (no known gaps)

## Cycle 17 Lessons
- **draw_rect guard**: always check y1 > y0 + 2 before drawing perspective-projected fixture rectangles — y_far/y_near can swap or be equal.
- **1280×720 canvas** is the Cycle 17 standard for new ENV backgrounds (older tools used 1920×1080). Use W, H = 1280, 720.
- **Checkerboard floor in perspective**: t_persp = t**0.6 gives good spacing distribution from far to near. Alternate (ri + ci) % 2 for tile coloring.
- **get_wall_band()** utility is effective for generating perspective-projected wall quads for bulletin boards, banners, doors.

## Cycle 16 Deliverables
- `LTG_TOOL_style_frame_02_glitch_storm_v003.py` → `LTG_COLOR_styleframe_glitch_storm_v003.png`
  - Fix: cold confetti (DATA_BLUE 70% dominant), Dutch angle verified 4°, Byte CORRUPT_AMBER #C87A20 3px outline, storm rim lighting on buildings
- `LTG_TOOL_style_frame_03_other_side_v002.py` → `LTG_COLOR_styleframe_otherside_v002.png`
  - Fix: waterfall luminance reduced (alpha 110 max), mid-distance bridge element added, right-side void irregularity (seeded polygon skew), DRW-18 UV Purple hair rim on Luma #7B2FBE
- `LTG_TOOL_bg_classroom_v002.py` → `LTG_ENV_classroom_bg_v002.png`
  - Fix: unified dual-source lighting (warm L 55α / cool R 50α), inhabitant evidence (wear marks, papers, backpack, chalk dust, water bottle)
- `LTG_TOOL_bg_grandma_kitchen_v001.py` → `LTG_ENV_grandma_kitchen_v001.png`
  - New: A1-01 kitchen, morning light, pre-digital appliances, CRT through doorway, lived-in details

## Cycle 15 Deliverables
- `LTG_TOOL_style_frame_03_other_side_v001.py` → `LTG_COLOR_styleframe_otherside_v001.png`
- `LTG_TOOL_bg_other_side_v002.py` → `LTG_ENV_other_side_bg_v002.png`

## Remaining Act Background Gaps (post Cycle 16)
- A1-03: Millbrook School Hallway (lockers)
- A1-05: School Hallway vending machine (may reuse A1-03)
- A2-01: Tech Den daylight version (nighttime = lumashome_study_interior_v001.png)

## Key Color Notes
- **CORRUPT_AMBER for Byte outlines**: DRW-07 = #C87A20 (200,122,32) — warmer/darker than #FF8C00. Confirmed in SF02 v003.
- **DRW-18 UV Purple rim**: GL-04 = #7B2FBE (123,47,190) — Luma hair crown rim in Glitch Layer scenes.
- **DATA_BLUE for storm confetti dominant**: #0A4F8C (10,79,140) — cold, threatening, NOT #2B7FFF.

## Critical Rules (always apply)
- **After img.paste() / alpha_composite: refresh draw = ImageDraw.Draw(img)**
- **Dutch angle = rotate entire image last, not individual elements**
- **Inverted atmospheric perspective in Glitch Layer: far = MORE purple + DARKER**
- **NO warm light in Glitch Layer — warmth only from pigment (hoodie, skin, debris)**
- **Cyan-lit surface rule: G > R AND B > R individually**
- **Never overwrite outputs — always new versioned files**

## Cycle 16 Lessons
- **CORRUPT_AMBER has two values in use**: #FF8C00 (old, v001/v002) and #C87A20 (#DRW-07 spec). Always use #C87A20 per Sam's color notes going forward.
- **Waterfall luminance fix**: per-pixel solid draw loops create wall effect. Switch to RGBA alpha_composite overlay with capped alpha (≤110) to maintain ambient-flow read.
- **Mid-distance bridging elements** should use multi-fragment approach (main platform + hanging pillars + secondary float above) to add depth and rhythm.
- **Unified lighting**: single directional gradient per source, clean crossover point. Never stack multiple overlapping patches from same source.
- **Inhabitant evidence requires specificity**: not "wear marks" generically, but desk-by-desk with seeded randomness and named item placement (backpack, water bottle, crossword puzzle).

## Cycle 14 Deliverables
- `LTG_TOOL_bg_other_side_v001.py` → `LTG_ENV_other_side_bg_v001.png`
- `LTG_TOOL_bg_classroom_v001.py` → `LTG_ENV_classroom_bg_v001.png`

## Cycle 13 Lessons
- **Cyan-lit surface rule: G > R AND B > R individually.**
- **Background-only exports → `output/backgrounds/environments/`. Generator scripts → `output/tools/`.**
- **Register tools in same session as creation.**
- **Category code TOOL applies to all Python scripts.**
- **ELEC_CYAN (#00F0FF) for screen glow, BYTE_TEAL (#00D4E8) for Byte body ONLY.**

## Cycle 12 Lessons
- **Dutch angle = camera tilt.** Applied as last step via PIL rotate(-degrees, expand=True) + center-crop.
- **Byte Visibility Rule in cyan environments**: CORRUPT_AMBER outline, LEFT shoulder, cracked eye faces danger.
- **Spec compliance for confetti**: ACID_GREEN forbidden in storm scenes.
- **`lerp_color()` expects 3-tuples.**

## Cycle 8–11 Lessons (summary)
- **Monitor glow = 3 gradient passes (not halo ring)**: horizontal onto wall, downward onto floor, horizontal onto ceiling.
- **`_draw_filled_glow()` = filled ellipses, never outline-only.**
- **3 light sources in Luma's house = 3 independent gradient passes.**
- **Nested `draw.point()` loops too slow** — use `draw.line()` for column fills.
- **Couch back cushion LEFT → faces RIGHT → monitors.**
- **Aurora rendering**: per-row horizontal `draw.line()` with sinusoidal phase + RGBA alpha_composite soft glow.
- **Pixel trails: RISE upward from platforms. Corruption scatter falls DOWNWARD.**
