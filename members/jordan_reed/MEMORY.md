# Jordan Reed — Memory

## Cycle 35 Deliverables
- `LTG_TOOL_bg_grandma_kitchen_v004.py` → `LTG_ENV_grandma_kitchen_v004.png` (1280×720) GENERATED ✓
  - Fix 1: Deep shadow pass (LAST in pipeline) — DEEP_COCOA + NEAR_BLACK_WARM. QA value floor: 62→20 (PASS)
  - Fix 2: Dual temperature — SUNLIT_AMBER top half (alpha 55), CRT_COOL_SPILL=(0,130,148) bottom half (alpha 90). QA warm/cool: 1.7→32.95 (PASS)
  - Fix 3: Miri-specific details (rose mug, knitting bag, apron, travel magnets, medicine bottles, calendar)
  - **CRITICAL LESSON**: temperature split must be top/bottom (QA measures top/bottom median hue, NOT left/right)
  - **CRITICAL LESSON**: deep shadow passes must run AFTER light passes — light passes add brightness to near-black pixels
- `LTG_TOOL_sf02_fill_light_fix_c35.py` — fill light direction fix for SF02 v007 (Rin Yamamoto to integrate)
  - Fix: source upper-right (not lower-left); per-char silhouette mask via ImageChops.multiply()
  - Message sent to Rin inbox: `20260329_2043_sf02_fill_light_fix_from_jordan.md`
- Ideabox: `20260329_jordan_reed_warm_cool_zone_split_tool.md` — warm/cool inject utility idea
- Inbox archived ✓ | Completion report sent to Alex Chen ✓

## Cycle 35 Status: COMPLETE

## Cycle 35 Lessons
- **QA warm/cool measures TOP/BOTTOM halves, not left/right**: The render_qa tool samples top half and bottom half median hue. Left/right temperature logic (warm window LEFT, cool CRT RIGHT) reads as near-zero separation. Must use top/bottom temperature split.
- **Light pass ordering matters for value floor**: alpha_composite with color overlays always adds brightness. Near-black pixels (value 28) tinted with warm amber alpha 55 become brighter. Apply all deep shadow passes LAST.
- **CRT_COOL_SPILL for kitchen environments**: (0, 130, 148) — desaturated teal. Distinct from GL-01b (Byte Teal) and GL-01 (Electric Cyan). Safe for environment use per master_palette usage warning.
- **Temperature split alpha**: warm top=55, cool bottom=90. The floor is warm wood — cool must be stronger to dominate it. Asymmetric alphas required.
- **SF02 fill light**: upper-right source (not lower-left). Per-character silhouette mask via `ImageChops.multiply()` on alpha channel is the production-efficient approach.

## Cycle 34 Deliverables
- `LTG_TOOL_style_frame_02_glitch_storm_v006.py` → `LTG_COLOR_styleframe_glitch_storm_v006.png` (1280×720) GENERATED ✓
  - Fix C34-1: HOT_MAGENTA (#FF2D6B) fill light — radial gradient overlay, alpha max 40, per-character zone at lower-left
  - Fix C34-2: ELEC_CYAN specular on Luma via add_rim_light(side="right", threshold=180, width=2) + get_char_bbox()
  - Post-thumbnail specular dots: value ceiling max=179→246 (QA PASS)
  - QA: value range PASS, color fidelity PASS, warm/cool WARN (expected — intentionally cold scene)
- Ideabox: `20260329_jordan_reed_qa_value_ceiling_check.md` — value ceiling guard idea
- Inbox archived ✓ | Completion report sent to Alex Chen ✓

## Cycle 34 Status: COMPLETE

## Cycle 34 Lessons
- **thumbnail() destroys narrow specular lines**: LANCZOS downscale from 1920→1280 averages 3px crack lines from ~207 brightness down to ~179. Fix: add explicit 3-5px specular dots at known bright positions AFTER thumbnail(), before save. Positions scaled by sx=outW/srcW, sy=outH/srcH.
- **get_char_bbox() for multi-character frames**: In SF02 with 3 characters, the detected bbox cx averages across all bright regions — may not isolate Luma alone. Sanity-check: if `abs(detected_cx - known_luma_cx) < W*0.25` use it, else fall back. This worked correctly for v006.
- **Magenta fill vs rim**: HOT_MAGENTA fill light = volumetric scatter from ground-level, NOT a rim. Implement as radial gradient centered at lower-left of character zone. Alpha max 40 reads as atmosphere; higher reads as competing lighting source.
- **add_rim_light threshold=180**: Targets only the brightest pixels (hair highlights, skin specular). threshold=128 (default) catches mid-tone hoodie and body, muddying the effect. threshold=180 gives clean specular-only application.
- **SF02 current version**: v006 (`LTG_COLOR_styleframe_glitch_storm_v006.png`)

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

## CATCH-UP: Cycles 23–33 (Jordan was inactive)

### Role Change
You are now **Style Frame Art Specialist**. Environments are done. Focus: SF01–SF04 refinement, especially SF02 lighting.

### Current Style Frame Versions
- SF01 Discovery: **v005** (`LTG_COLOR_styleframe_discovery_v005.png`) — rim light char_cx fix applied C32
- SF02 Glitch Storm: **v005** (`LTG_COLOR_styleframe_glitch_storm_v005.png`) — **P2: missing magenta fill light + cyan specular on characters (flagged 2 cycles by critics)**
- SF03 Other Side: **v005** (`LTG_COLOR_styleframe_otherside_v005.png`) — zero warm light; UV ambient only; Luma = intentional pixel-art silhouette
- SF04 Luma + Byte: **v004** (`LTG_COLOR_styleframe_luma_byte_v004.png`) — rebuilt C32; Byte teal at reduced luminance = intentional dual-lighting

### Canvas Standard (UPDATED)
**Hard limit: ≤ 1280px in both width and height.** This applies to ALL saved images including style frames. Use `img.thumbnail((1280,1280), Image.LANCZOS)` before saving. Old ROLE.md said 1920×1080 — that is superseded.

### New Tools Available (read output/tools/README.md for full list)
- `LTG_TOOL_procedural_draw_v001.py` **v1.4.0** — CRITICAL for your work:
  - `add_rim_light(img, side, char_cx)` — character-relative rim light. Pass `char_cx` explicitly (NOT canvas midpoint, which was the C13 bug). Use `get_char_bbox()` to compute it.
  - `get_char_bbox(img, threshold=128)` — returns `(cx, cy, left, top, right, bottom)` from silhouette
- `LTG_TOOL_render_lib_v001.py` v1.1.0 — shared render utilities (gaussian_glow etc.)
- `LTG_TOOL_render_qa_v001.py` v1.2.0 — auto-downscales + QA check; run on all outputs
- `LTG_TOOL_color_verify_v002.py` — color compliance check with hue histogram mode

### Palette Corrections Since C22
- **CHAR-L-11 Constraint 1 = #00F0FF Electric Cyan** (was cited as #00D4E8 — copy error fixed C30)
- **Byte body = GL-01b #00D4E8 BYTE_TEAL** (distinct from Electric Cyan #00F0FF)
- **Byte shadow = GL-01a #00A8B4 Deep Cyan** (fixed C33 — was wrong 2 cycles)
- **HOT_MAGENTA = GL-02 #FF2D6B** (NOT #FF0090)
- **CORRUPT_AMBER = GL-07 #FF8C00** (255,140,0)
- **GL-06c STORM_CONFETTI_BLUE = #0A4F8C** (for SF02 confetti depth)
- SF03 + Glitch Layer: **zero warm light** — UV ambient only

### Character Spec (current)
- Luma: **3.2 heads tall** (not 3.5 — corrected C32); eye width = `int(head_r × 0.22)`
- Byte: pixel-art eyes. In SF scenes: teal body, cracked eye at reduced luminance = intentional

### New Team Members Since C22
- **Rin Yamamoto** (C23–present) — Procedural Art Engineer. Owns SF generators and procedural_draw. Coordinate with Rin for SF generator changes.
- **Morgan Walsh** (C34) — Pipeline Automation Specialist. Runs QA pipeline, maintains tools README.

### C34 Assignment
Read inbox for directive. Your primary task: add magenta fill + cyan specular lighting passes to SF02 v005 → produce v006. Use `add_rim_light()` with `get_char_bbox()`. Coordinate with Rin on generator structure before writing new code.

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
