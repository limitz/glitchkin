# Jordan Reed — Memory

## Cycle 19 Deliverables
- `LTG_TOOL_style_frame_03_other_side_v003.py` → `LTG_COLOR_styleframe_otherside_v003.png`
  - CRITICAL fix: BYTE_BODY = (0,212,232) GL-01b Byte Teal (was (10,10,20) Void Black — invisible)
  - Eye radius min 15px (was ~10px) — both eyes readable
  - Void Black slash removed from magenta eye — clean read
- `LTG_TOOL_style_frame_02_glitch_storm_v004.py` → `LTG_COLOR_styleframe_glitch_storm_v004.png`
  - Damaged storefront window: frame + dividers + cracked panes + impact cracks + debris scatter
  - Real window glow: warm amber (200,160,80) trapezoid cones below each lit window, alpha 90-110
- `LTG_TOOL_bg_school_hallway_v002.py` → `LTG_ENV_school_hallway_v002.png`
  - Black top band fixed: image init to CEIL_TILE, ceiling poly from y=0
  - Human evidence: backpack 80×120px+, coat hooks + jacket, notice board with colored papers
  - Camera lowered: VP_CY H*0.40 → H*0.22 (–18%), taller more institutional space
- `LTG_TOOL_bg_millbrook_main_street_v002.py` → `LTG_ENV_millbrook_main_street_v002.png`
  - Power lines: 3px main cable + 1px spans + catenary parabolic sag + lighter color
  - Road plane: full ROAD_ASPHALT solid + double-yellow center line + crosswalk stripes near end
- README.md updated ✓ | Inbox archived ✓ | Completion report sent to Alex Chen ✓

## Cycle 19 Status: COMPLETE

## Cycle 18 Deliverables
- `LTG_TOOL_bg_millbrook_main_street_v001.py` → `LTG_ENV_millbrook_main_street_v001.png`
  - Millbrook Main Street daytime exterior for A2-05 (walk-and-talk)
  - Afternoon sun upper-right, long left shadows, local storefronts with hand-painted signs and awnings
  - Sidewalk: cracked concrete, tree root bumps, street trees (autumn coloring)
  - Road: asphalt, faded center line, parked car silhouettes
  - Far-end atmospheric haze, warm afternoon blue sky with light cloud
  - Canvas 1280×720, Real World palette only

## Key Color Notes
- **BYTE_BODY = (0, 212, 232) GL-01b Byte Teal — NEVER (10,10,20) Void Black**
  - Critical error found in SF03 v002 — body was invisible against UV Purple ambient
- **CORRUPT_AMBER for Byte outlines**: DRW-07 = #C87A20 (200,122,32)
- **DRW-18 UV Purple rim**: GL-04 = #7B2FBE (123,47,190) — Luma hair crown rim
- **DATA_BLUE for storm confetti dominant**: #0A4F8C (10,79,140)
- **ELEC_CYAN (#00F0FF) for screen glow, BYTE_TEAL (#00D4E8) for Byte body ONLY**

## Critical Rules (always apply)
- **After img.paste() / alpha_composite: refresh draw = ImageDraw.Draw(img)**
- **Dutch angle = rotate entire image last, not individual elements**
- **Inverted atmospheric perspective in Glitch Layer: far = MORE purple + DARKER**
- **NO warm light in Glitch Layer — warmth only from pigment (hoodie, skin, debris)**
- **Cyan-lit surface rule: G > R AND B > R individually**
- **Never overwrite outputs — always new versioned files**
- **Black top band prevention: init image to ceiling tile color, not black**
- **Eye readability: minimum 15px radius for Byte eyes in style frames**

## Cycle 19 Lessons
- **BYTE_BODY critical bug**: (10,10,20) = Void Black. Never use. Always GL-01b (0,212,232).
- **Eye slash**: Void Black diagonal slash on colored eyes = invisible in dark scenes. Remove slashes, use clean filled ellipses only.
- **Black top band**: Image("RGBA",(W,H),(0,0,0,255)) + ceiling poly NOT starting at y=0 = black top artifact. Fix: init image to ceiling color OR make CEIL_NEAR_L/R = (x,0).
- **Catenary power lines**: sin(t×π) × sag_amount gives natural parabolic sag. Scale sag by perspective distance.
- **Road plane**: Always draw solid asphalt base FIRST, then markings on top. Double-yellow = two parallel offset perspective lines.
- **Window glow geometry**: trapezoid projecting down from window bottom — NOT left-edge gradient bleed.
- **Damaged glass reads**: frame + dividers + missing panes + crack rays from 2 impact points + debris below.

## Cycle 16–17 Lessons (summary)
- **draw_rect guard**: always check y1 > y0 + 2 before drawing perspective-projected fixture rectangles
- **1280×720 canvas** is standard for new ENV backgrounds
- **get_wall_band()** utility effective for perspective-projected wall quads
- **Unified lighting**: single directional gradient per source, clean crossover
- **Inhabitant evidence requires specificity**: named items with seeded placement

## Cycle 14–15 Lessons (summary)
- **Background-only exports → `output/backgrounds/environments/`. Generator scripts → `output/tools/`**
- **Register tools in same session as creation**
