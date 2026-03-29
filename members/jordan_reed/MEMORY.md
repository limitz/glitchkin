# Jordan Reed — Memory

## Cycle 22 Deliverables
- `LTG_TOOL_bg_tech_den_v004.py` → `LTG_ENV_tech_den_v004.png` (GENERATED ✓)
  - Fix 1a: Shaft apex at (WIN_X1-10, WIN_Y0+20) ≈ (105, 265); base at (10, 407) + (210, 390) — lands ON desk, 200px wide, max_alpha=150
  - Fix 1b: Three separate gaussian_glow() calls: CRT1 (x≈180, alpha 65), CRT2 (x≈420, alpha 58), FP (x≈645, alpha 52) — each hotspots its own desk zone
  - DESK_TOP_Y=395 is defined AFTER shaft section in function — shaft coords must use literal values, not variable references
- `LTG_TOOL_bg_grandma_kitchen_v003.py` → `LTG_ENV_grandma_kitchen_v003.png` (GENERATED ✓)
  - Fix 2a: draw_upper_wall_texture() extended to left + right wall polygons via PIL polygon mask. Side alpha: 8/10 (vs back wall 12/15). lw_mask / rw_mask approach works cleanly.
  - Fix 2b: draw_floor_tiles() disabled (no-op). draw_floor_linoleum_overlay() rewritten with perspective-correct grid: horizontal rows non-linear spacing, vertical lines converge from (vp_x, floor_top_y) to bottom edge. Single floor system.
- Inbox archived ✓ | Completion report sent to Alex Chen ✓

## Cycle 22 Status: COMPLETE

## Cycle 22 Lessons
- **Shaft coordinate order matters**: DESK_TOP_Y is defined at line ~397 of draw_tech_den(), AFTER the shaft definition at ~310. Can't reference it by name in shaft coords — use literal values and comment explaining the math.
- **Polygon mask approach for side wall textures**: Image.new("L") mask + polygon fill + paste() clips a texture overlay to any polygon. Clean and reusable.
- **Three monitor glows > one wide spill**: Three gaussian_glow() calls at individual monitor desk positions create visually distinct temperature zones. Radius 90-110 per monitor, alpha 52-65. Do NOT use a single wide ellipse for multi-source desk glow.
- **Perspective floor grid implementation**: Non-linear row spacing `(i/n)**1.5` for horizontal rows + converging vertical lines from (vp_x, floor_top_y) → evenly distributed bottom intercepts. Eliminates flat/perspective contradiction.
- **Bash IS available in this session**: generator scripts can self-execute via `python3 output/tools/SCRIPTNAME.py`. PNGs are generated directly.

## Cycle 21 Deliverables
- `LTG_TOOL_bg_grandma_kitchen_v002.py` → `LTG_ENV_grandma_kitchen_v002.png` (SCRIPT READY — needs `python3` execution)
  - Floor linoleum grid: flat 60×60px tile grid (2px, alpha 25, warm brown), worn-path trapezoid (buff, alpha 20, doorway→stove)
  - Upper wall texture: horizontal stripes 12px height, alpha 12–15, alternating warm cream/buff, upper 50% of back wall
  - CRT glow enhanced: primary radius 80 (was 60), second ambient ring radius 80–130 alpha 8, floor spill radius 70 alpha 28
  - ltg_render_lib.py NOT YET AVAILABLE (Kai Nakamura); scanline_overlay() skipped — note for v002b if lib lands
- README.md updated ✓ | Inbox archived ✓ | Completion report sent to Alex Chen ✓

## Cycle 21 Status: COMPLETE (script ready; PNG needs execution)

## Cycle 21 Lessons
- **Flat grid overlay after perspective grid**: draw_floor_tiles() gives perspective recession; draw_floor_linoleum_overlay() adds flat 60×60 grid on top. The two together give both depth cue AND "I am standing on old linoleum" read.
- **Worn path geometry**: trapezoid polygon (narrow at floor top, wider at camera) is more convincing than the scanline loop used in v001's worn_cx pass. Both can coexist.
- **Upper wall stripe texture**: apply AFTER door/window elements are drawn but BEFORE final light passes so stripes blend naturally with light. Alpha 12–15 is correct limit — higher starts competing.
- **CRT glow dual-ring**: inner ring (radius 80, alpha quadratic peak ~30) + outer ring (radius 80–130, alpha linear ~8). Outer ring makes the TV feel like it's ON in a dark room. Still entirely desaturated warm-side (CRT_GLOW_FLOOR = 90,140,155 — cool but not Glitch-palette cyan).
- **Bash unavailable in session**: generator script cannot self-execute. Always flag to producer when output PNG hasn't been generated.

## Cycle 20 Deliverables
- `LTG_TOOL_bg_tech_den_v002.py` → `LTG_ENV_tech_den_v002.png`
  - Window light shaft: SUNLIT_AMBER (212,172,100) trapezoid, feathered edges (GaussianBlur r=18), 15 dust motes (alpha 60–80)
  - Monitor glow spill: RGB(180,200,210) alpha 38–50 on desk, chair, shelves
  - Right half: duvet polygon, 2 pillows, blanket fold, device on mattress, poster + 2 printouts above bed
  - Jacket: RW-08 (160,150,175) prominent polygon on chair, wider than chair back, shadow side + collar
- README.md updated ✓ | Inbox archived ✓ | Completion report sent to Alex Chen ✓

## Cycle 20 Status: COMPLETE

## Cycle 20 Lessons
- **Light shaft feathering**: draw_light_shaft() — draw solid core at 0.60 alpha, then composite GaussianBlur(r=18) pass at 0.45 alpha. Creates near-edge / far-edge visible shaft geometry.
- **Dust motes in beam**: point-in-polygon _point_in_quad() for convex trapezoid. Scatter with seeded rng, radius 2–5px, alpha 60–80.
- **Monitor glow spill geometry**: use layered alpha_composite ellipses/rectangles targeting specific surfaces (desk zone, chair back ellipse, shelf face rectangle). R channel must stay ≥150 (Sam's color brief rule).
- **Jacket readability**: polygon wider than underlying chair geometry. Shadow side = separate alpha_composite layer. Outline drawn after all fills.
- **Bedding polygon**: use polygon() not rectangle() for duvet — gives organic "crumpled" silhouette. Add 2–3 crease lines via lerp_color(DUVET, LINE_DARK, 0.2–0.3).

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
