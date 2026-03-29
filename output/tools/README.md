# Tools Index — "Luma & the Glitchkin"

**Maintained by:** Alex Chen, Art Director
**Last updated:** 2026-03-29 (Cycle 23)

---

## Open Source Tools Policy

This production uses **open source tools exclusively**. No proprietary software is permitted at any stage of the pipeline. The approved open source stack is:

| Tool | Role | Notes |
|---|---|---|
| **OpenToonz** | 2D animation | Primary animation tool. Used by Studio Ghibli. |
| **Krita** | Digital painting | Backgrounds, character sheets, color keys, style frames |
| **Inkscape** | Vector graphics | Model sheets, style guides, title cards, SVG assets |
| **Natron** | Compositing | Final composite, color grade, FX assembly |
| **Python + Pillow/PIL** | Image scripting | Batch processing, image generation, pipeline automation |
| **Python + pycairo / svgwrite** | Vector scripting | SVG and vector asset generation |
| **ImageMagick** | CLI image processing | Format conversion, batch resizing, asset pipeline |
| **Git + Git LFS** | Version control | Documents via standard Git; binaries via Git LFS |

**If a required tool does not exist in the open source ecosystem, the team must implement it in Python** and register it in the table below.

---

## Script Index

| Script Name | Created By | Purpose | Dependencies |
|---|---|---|---|
| `color_swatch_generator.py` | Maya Santos / Production | Generates labeled PNG color swatch sheets from hex/name pairs. Reusable CLI + module. | Pillow |
| `proportion_diagram.py` | Maya Santos / Production | Generates character proportion diagrams side-by-side in head-unit scale. | Pillow |
| `silhouette_generator.py` | Maya Santos / Production | Generates solid-black character silhouette sheets for squint-test validation. | Pillow |
| `bg_layout_generator.py` | Jordan Reed / Production | Generates 1920×1080 color-block background layout compositions from zone definitions. Includes Luma's House, Glitch Layer, Millbrook Street scene generators. | Pillow |
| `storyboard_panel_generator.py` | Lee Tanaka / Production | Generates 480×270px storyboard panels with caption bars, shot labels, and drawn scene content. Cycle 5: 7 panels (P01, P03, P07-bridge, P11, P12-bridge, P13, P25) + 2-row contact sheet. P03 fixed: pulse visible. P13 redrawn: 3D spatial staging. | Pillow |
| `luma_face_generator.py` | Maya Santos / Production | Draws Luma's face at 600×600px with asymmetric hair cloud, wide reckless eyes, arched brows, reckless grin, blush, and pixel-pattern hoodie collar. | Pillow |
| `byte_expressions_generator.py` | Alex Chen / Production | Generates 6-expression sheet for Byte using 5×5 pixel grid eye system. Expressions: GRUMPY, SEARCHING, ALARMED, RELUCTANT JOY, CONFUSED, POWERED DOWN. Body color #00D4E8. | Pillow |
| `bg_glitch_layer_frame.py` (also `LTG_TOOL_bg_glitch_layer_frame_v001.py`) | Jordan Reed / Cycle 9 | Generates full 1920×1080 Glitch Layer compositing-ready background (no characters, no title bar). Three-tier platform depth system (NEAR=ELEC_CYAN, MID=desaturated DATA_BLUE, FAR=near-void). Aurora bands, pixel trails, pixel flora on platform edges, ghost platforms in lower void. Saves to `/home/wipkat/team/output/backgrounds/environments/glitch_layer_frame.png`. | Pillow |
| `LTG_TOOL_naming_compliance_copier_v001.py` | Jordan Reed / Cycle 12 | Batch-creates LTG-compliant named copies of legacy assets (CHAR turnarounds, COLOR swatches, ENV layouts, COLOR style frames). Uses `shutil.copy2()` — never renames originals. Outputs: `LTG_CHAR_luma_turnaround_v001.png`, `LTG_CHAR_byte_turnaround_v001.png`, `LTG_CHAR_cosmo_turnaround_v001.png`, `LTG_CHAR_miri_turnaround_v001.png`, `LTG_COLOR_styleframe_discovery_v001.png`, `LTG_COLOR_luma_color_model_swatches_v001.png`, `LTG_COLOR_byte_color_model_swatches_v001.png`, `LTG_COLOR_cosmo_color_model_swatches_v001.png`, `LTG_COLOR_grandma_miri_color_model_swatches_v001.png`, `LTG_CHAR_character_lineup_v001.png`. | Pillow, shutil |
| `LTG_TOOL_naming_compliance_copier_v002.py` | Jordan Reed / Cycle 12 | ENV pass of the compliance copier. Creates LTG-compliant copies of environment assets including `LTG_ENV_glitchlayer_layout_v001.png`, `LTG_ENV_glitchlayer_encounter_v001.png`, and related ENV-category files. | Pillow, shutil |
| `LTG_TOOL_naming_compliance_copy_v001.py` | Jordan Reed / Cycle 12 | Alternate/earlier naming compliance copy tool (`_copy_` vs `_copier_` suffix variant). Purpose overlaps with `LTG_TOOL_naming_compliance_copier_v001.py`. Flagged for consolidation review — Alex Chen to decide which is canonical. | Pillow, shutil |
| `LTG_TOOL_style_frame_02_glitch_storm_v001.py` | Jordan Reed / Cycle 12 | Generates full 1920×1080 Style Frame 02 "Glitch Storm" background WITH characters (Luma, Cosmo, Byte sprint poses, townspeople). 4° Dutch angle applied as final step. NOTE: uses old TERRA_CYAN_LIT=(154,140,138) which fails cyan-lit check. See v002 (Alex Chen) and `LTG_TOOL_bg_glitch_storm_colorfix_v001.py` (Jordan Reed) for corrected color. Output: `LTG_COLOR_styleframe_glitch_storm_v001.png`. | Pillow |
| `LTG_TOOL_colorkey_glitchstorm_gen_v001.py` | Sam Kowalski / Cycle 12 | Generates 640×360 color key thumbnail for Style Frame 02 "Glitch Storm" scenario. Cross-references scene_color_keys.md Key 02. Storm confetti: Cyan/White/Magenta/UVPurple (NO Acid Green). Cycle 13: TERRACOTTA_CYAN_LIT constant added, inline (154,140,138) replaced with corrected (150,172,162). Output: `LTG_COLOR_colorkey_glitchstorm_v001.png`. | Pillow |
| `LTG_TOOL_logo_asymmetric_v001.py` | Jordan Reed / Cycle 12 | Generates the asymmetric "Luma & the Glitchkin" logo lockup. Produces stylized title treatment with glitch texture effects and asymmetric composition. | Pillow |
| `LTG_TOOL_bg_glitch_storm_colorfix_v001.py` | Jordan Reed / Cycle 13 | Background-only Glitch Storm generator with ENV-06 color fix. TERRACOTTA_CYAN_LIT=(150,172,162) replaces wrong (154,140,138) — G=172>R=150, B=162>R=150, reads cool/cyan-tinted. NO characters — compositing reference for Alex Chen. Output: `LTG_ENV_glitch_storm_bg_v001.png`. | Pillow |
| `LTG_TOOL_luma_expression_sheet_v002.py` | Maya Santos / Cycle 12 | Generates Luma expression sheet at 1200×800px with 6 expressions. Previously misnamed `LTG_CHAR_luma_expression_sheet_v002.py` — renamed in Cycle 22 to comply with TOOL category convention. | Pillow |
| `LTG_TOOL_luma_expression_sheet_v003.py` | Maya Santos / Cycle 16 | Luma expression sheet v003. Previously misnamed `LTG_CHAR_luma_expression_sheet_v003.py` — renamed in Cycle 22 to comply with TOOL category convention. | Pillow |
| `LTG_TOOL_luma_expression_sheet_v004.py` | Maya Santos / Cycle 22 | Luma expression sheet v004. Previously misnamed `LTG_CHAR_luma_expression_sheet_v004.py` — renamed in Cycle 22 to comply with TOOL category convention. | Pillow |
| `LTG_TOOL_style_frame_01_discovery_v003.py` | Alex Chen / Cycle 13 | SF01 Ghost Byte alpha calibration fix. Ghost body alpha 55→90, eye glints 65–70→105. Top-left monitor ghost removed (warm lamp bleed). Two ghost screens (top-right + mid-left only). Pitch-scale legible. Output: `LTG_COLOR_styleframe_discovery_v003.png`. | Pillow |
| `LTG_TOOL_logo_asymmetric_v002.py` | Alex Chen / Cycle 13 | Asymmetric logo v002. "&" connector gets warm-to-cold gradient treatment (SUNLIT_AMBER left → ELEC_CYAN right) via per-column alpha composite. "the/Glitchkin" inter-line gap reduced ~30%. Output: `LTG_BRAND_logo_asymmetric_v002.png`. | Pillow |
| `LTG_TOOL_style_frame_02_glitch_storm_v002.py` | Alex Chen / Cycle 13 | SF02 character composite pass. Repositions characters: Byte hovering LEFT (~28%), Luma CENTER (~45%), Cosmo RIGHT (~62%). Byte = VOID_BLACK body (storm variant, intentional). CORRUPT_AMBER outlines. char_h 18%. Dutch angle preserved. TERRACOTTA_CYAN_LIT=(150,172,162) applied (Jordan Reed ENV-06 fix). Output: `LTG_COLOR_styleframe_glitch_storm_v002.png`. | Pillow |
| `LTG_TOOL_byte_cracked_eye_glyph_v001.py` | Alex Chen / Cycle 13 | Generates Byte's canonical dead-pixel cracked-eye glyph reference sheet. 7×7 grid with diagonal crack fracture, dead zone upper-right, alive zone lower-left, Hot Magenta crack line. Shows 4 scales + in-eye mockups. Required for Lee Tanaka panel A2-07. Output: `LTG_CHAR_byte_cracked_eye_glyph_v001.png`. | Pillow |
| `LTG_TOOL_byte_expression_sheet_v002.py` | Alex Chen / Cycle 15 | Byte expression sheet v002. Adds RESIGNED / RELUCTANT DISCLOSURE as 8th expression: arms very close to body (arm_dy=14, arm_x_scale=0.50), backward avoidance lean (body_tilt=+8), droopy_resigned right eye (heavy lid, downcast pupil, no suppressed smile, distinct from RELUCTANT JOY), ↓ downward-arrow pixel symbol (defeat indicator, distinct from flat-line NEUTRAL). Fills all 8 slots in 4×2 grid. Required for A2-02 (Maya Santos request). Output: `LTG_CHAR_byte_expression_sheet_v002.png`. | Pillow |
| `LTG_TOOL_bg_other_side_v001.py` | Jordan Reed / Cycle 14 | Generates the SF03 "Other Side" CRT-world environment background (1920×1080). Pure digital space: ELEC_CYAN + VOID_BLACK dominant, zero warm tones. Perspective pixel grid floor, 3-tier platform depth system (NEAR/MID/FAR), aurora bands, floating geometry, pixel trails, data streams, horizon vanishing-point glow, CRT frame vignette. Contrasts SF01 (warm room) and SF02 (contested street). Output: `LTG_ENV_other_side_bg_v001.png`. | Pillow |
| `LTG_TOOL_bg_classroom_v001.py` | Jordan Reed / Cycle 14 | Generates Millbrook Middle School classroom background (1920×1080) for Act 2 panels including A1-04. 3/4 camera from back-right. 3-tier depth: FG coat rack + desk corner / MG diagonal desk rows / BG front wall with board/teacher desk. Dual-temperature lighting: warm gold window shafts (left) vs cool fluorescent (right). Binary/math board content. Foreground depth anchor (mandatory). Scanline hint. Output: `LTG_ENV_classroom_bg_v001.png`. | Pillow |
| `LTG_TOOL_style_frame_03_other_side_v001.py` | Jordan Reed / Cycle 15 | Generates SF03 "The Other Side" full style frame with characters (1920×1080). Spec-compliant per sf03_other_side_spec.md (Alex Chen) and style_frame_03_other_side.md (Sam Kowalski). Five depth layers: void sky (ring megastructure + stars), far distance (slabs + Glitchkin dots + Corrupt Amber), mid-distance (slabs + Real World debris: wall/road/lamppost), midground (platform + circuit traces + pixel-art plants + data waterfall + sub-platforms), foreground (settled confetti). UV Purple ambient + cyan bounce + blue waterfall lighting overlays. Luma (UV-ambient modified palette, pixel-grid hoodie) + Byte (DEEP_CYAN glow, cyan left eye, magenta right eye) at small scale. No warm light. Inverted atmospheric perspective. seed=77 confetti. Output: `LTG_COLOR_styleframe_otherside_v001.png`. | Pillow |
| `LTG_TOOL_bg_other_side_v002.py` | Jordan Reed / Cycle 15 | Spec-compliant ENV background-only version of SF03 "Other Side" (no characters, no footer). Replaces Cycle 14 v001 which used pre-spec grid floor approach. Shares all color/layer logic with LTG_TOOL_style_frame_03_other_side_v001.py. Output: `LTG_ENV_other_side_bg_v002.png`. | Pillow |
| `LTG_TOOL_style_frame_02_glitch_storm_v003.py` | Jordan Reed / Cycle 16 | SF02 Glitch Storm fix pass. Fixes: (1) Dominant cold confetti — DATA_BLUE 70% + VOID_BLACK 20% + ELEC_CYAN 10%, no warm/rainbow spread; (2) Dutch angle verified at 4.0° perceptible tilt; (3) Byte CORRUPT_AMBER (#C87A20) solid 3px outline — visible in storm sky; (4) Storm rim lighting on buildings — ELEC_CYAN right/top edges + UV_PURPLE base bounce. CORRUPT_AMBER updated to DRW-07 spec value #C87A20. Output: `LTG_COLOR_styleframe_glitch_storm_v003.png`. | Pillow |
| `LTG_TOOL_style_frame_03_other_side_v002.py` | Jordan Reed / Cycle 16 | SF03 Other Side fix pass (with characters). Fixes: (1) Data waterfall luminance reduced — alpha max 110 (was 255), reads as ambient flow not solid wall; (2) Mid-distance bridging element added — floating arch fragment at 40-65% x / 49-60% y; (3) Right-side void structures broken up — 7 seeded-variation polygon slabs with scale+skew irregularity; (4) DRW-18 UV Purple rim (#7B2FBE) on Luma hair crown — prevents head merging with dark BG. Output: `LTG_COLOR_styleframe_otherside_v002.png`. | Pillow |
| `LTG_TOOL_bg_classroom_v002.py` | Jordan Reed / Cycle 16 | Classroom background fix pass. Fixes: (1) Unified lighting — warm LEFT gradient (SUNLIT_AMBER from windows, 55 alpha max) + cool RIGHT gradient (fluorescent, 50 alpha max), clean transition, no muddy overlap patches; (2) Inhabitant evidence — wear marks on 65% of desks, scattered worksheets on 55% of desks, forgotten backpack on floor near Luma's desk, chalk dust near board tray, water bottle on nearest desk corner. Output: `LTG_ENV_classroom_bg_v002.png`. | Pillow |
| `LTG_TOOL_bg_grandma_kitchen_v001.py` | Jordan Reed / Cycle 16 | Grandma Miri's Kitchen background for A1-01 (Act 1 opening). Warm morning daylight, Real World palette only. Small cozy kitchen interior: morning sunlight through window (warm amber/golden gradient), old-fashioned appliances (pre-digital gas stove, porcelain sink, old fridge), CRT TV through doorway (story element — faint desaturated glow, far plane only), lived-in details (crossword puzzle + pencil, tea mug with steam, toast on plate, dish rack, kitchen plants, fridge magnets). Floor: linoleum tile with worn traffic path. Table in foreground. Output: `LTG_ENV_grandma_kitchen_v001.png`. | Pillow |
| `LTG_TOOL_bg_tech_den_v001.py` | Jordan Reed / Cycle 17 | Cosmo's Tech Den background (daylight) for A2-01, A2-03, A2-04, A2-05. Small bedroom repurposed as tech workspace. Natural daylight from left window (warm gold/amber) + blue-white monitor glow on desk zone. Desk dominant (left 60%): two CRT monitors, flat panel, oscilloscope, breadboards, soldering kit, cable tangles. Back wall shelving: vintage PCs, game cartridges, labeled component bins. Pinned papers: coding printouts, hand-drawn circuit diagram. Bed pushed to right wall. Cosmo's dusty lavender jacket on desk chair. Real World palette only — zero Glitch colors. Canvas 1280×720. Output: `LTG_ENV_tech_den_v001.png`. | Pillow |
| `LTG_TOOL_bg_school_hallway_v001.py` | Jordan Reed / Cycle 17 | Millbrook School Hallway background for A1-03, A1-05. 3-point perspective, slight low camera angle (hallway feels large). Metal lockers both sides (alternating sage + dusty lavender). Linoleum floor: cream/sage checkerboard tiles with worn center path and scuff marks. Fluorescent overhead lights (slightly green cool cast) with soft floor pools. Bulletin boards above lockers with poster shapes. Warm sunlight shaft from left high window (SUNLIT_AMBER, real-world only). Two terracotta classroom doors on right wall. Trophy case on left wall near far end. T-intersection far end with daylit windows and school seal. Atmospheric cool haze on distant end. Real World palette only — zero Glitch colors. Canvas 1280×720. Output: `LTG_ENV_school_hallway_v001.png`. | Pillow |
| `LTG_TOOL_bg_millbrook_main_street_v001.py` | Jordan Reed / Cycle 18 | Millbrook Main Street daytime exterior background for A2-05 (walk-and-talk). Suburban small-town USA feel — warm, lived-in. Afternoon sun from upper right with long left-casting shadows. Storefronts: mix of local businesses with hand-painted signs and awnings. Sidewalk: cracked concrete with tree root bumps and street trees in autumn coloring. Road: asphalt with faded center line and parked car silhouettes. Background depth: buildings receding down street with atmospheric haze at far end. Sky: warm afternoon blue with light cloud. Real World palette only — zero Glitch colors. Canvas 1280×720. Output: `LTG_ENV_millbrook_main_street_v001.png`. | Pillow |
| `LTG_TOOL_luma_act2_standing_pose_v001.py` | Maya Santos / Cycle 15 | Standing reactive pose for Luma covering Act 2 beats A2-01/A2-03/A2-05/A2-08. WORRIED/DETERMINED expression (brow differential 8px+, corrugator kink, jaw-open oval). Right arm raised/reaching, left arm at waist, wide stance (leg_spread=1.1), body_tilt=-5 forward lean. A-line hoodie silhouette with chest pixel pattern and pocket bump asymmetry hook. Includes squint-test silhouette blob in annotation panel. Output: `LTG_CHAR_luma_act2_standing_pose_v001.png` (900×600px). | Pillow |
| `character_lineup_generator.py` | Maya Santos / Production (legacy) | Generates character lineup PNG with all main cast side-by-side for size comparison. Legacy filename — LTG-compliant output: `LTG_CHAR_character_lineup_v001.png`. | Pillow |
| `character_turnaround_generator.py` | Maya Santos / Production (legacy) | Generates 3-view turnaround sheets (front/side/back) for each character. Legacy filename. | Pillow |
| `contact_sheet_generator.py` | Lee Tanaka / Production (legacy) | Generates contact sheet layouts combining multiple panels into a single reference image. Legacy filename. | Pillow |
| `logo_generator.py` | Jordan Reed / Production (legacy) | Generates the show logo. Superseded by `LTG_TOOL_logo_asymmetric_v001.py`. Legacy filename. | Pillow |
| `panel_chaos_generator.py` | Lee Tanaka / Production (legacy) | Generates storyboard panels for chaotic/action sequences. Legacy filename. | Pillow |
| `panel_interior_generator.py` | Lee Tanaka / Production (legacy) | Generates storyboard panels for interior scenes. Legacy filename. | Pillow |
| `storyboard_pitch_export_generator.py` | Lee Tanaka / Production (legacy) | Exports combined storyboard pitch package (all panels into print-ready format). Legacy filename. | Pillow |
| `style_frame_01_rendered.py` | Jordan Reed / Production (legacy) | Generates Style Frame 01 "Discovery" rendered background. Legacy filename — LTG-compliant output: `LTG_COLOR_styleframe_discovery_v001.png`. | Pillow |
| `style_frame_generator.py` | Jordan Reed / Production (legacy) | General-purpose style frame generator (earlier iteration). Legacy filename, superseded by scene-specific tools. | Pillow |

| `LTG_TOOL_style_frame_03_other_side_v003.py` | Jordan Reed / Cycle 19 | SF03 Other Side fix pass (Critique C9). Fixes: (1) CRITICAL BYTE_BODY color — was (10,10,20) Void Black (invisible against UV Purple), now (0,212,232) GL-01b Byte Teal; (2) Eye radius increased to min 15px (was ~10px), both cyan + magenta eyes readable; (3) Void Black diagonal slash removed from magenta eye — both eyes clean. Carries all v002 fixes (waterfall luminance, bridging element, right-side void irregularity, Luma UV Purple hair rim). Output: `LTG_COLOR_styleframe_otherside_v003.png`. | Pillow |
| `LTG_TOOL_style_frame_02_glitch_storm_v004.py` | Jordan Reed / Cycle 19 | SF02 Glitch Storm fix pass (Critique C9). Fixes: (1) Storefront lower-right replaced with genuine DAMAGED STOREFRONT WINDOW — structural frame + vertical/horizontal dividers + crack lines from 2 impact points + missing panes showing dark interior + glass shard and rubble debris scatter below; (2) Warm window glow replaced with REAL window light geometry — downward trapezoid cones of warm amber (200,160,80) below each lit building window, alpha 90-110, reads as pools of warm domestic light vs cold storm. Carries all v003 fixes. Output: `LTG_COLOR_styleframe_glitch_storm_v004.png`. | Pillow |
| `LTG_TOOL_bg_school_hallway_v002.py` | Jordan Reed / Cycle 19 | School Hallway background fix pass (Critique C9). Fixes: (1) Black top band artifact fixed — image initialized to CEIL_TILE color, ceiling polygon now starts at y=0; (2) Human evidence added — backpack leaning against locker (80×120px+, deep blue with front pocket + strap), coat hooks on right wall near section with hanging jacket (brown, shadow side + collar), notice board on left wall with 8 distinct colored paper rectangles (red/yellow/green/white/blue) with pins; (3) Camera angle lowered — VP_CY from H*0.40 to H*0.22 (-18%), hallway feels taller and more institutional. Output: `LTG_ENV_school_hallway_v002.png`. | Pillow |
| `LTG_TOOL_bg_millbrook_main_street_v002.py` | Jordan Reed / Cycle 19 | Millbrook Main Street background fix pass (Critique C9). Fixes: (1) Power lines — main cable 3px (perspective-scaled), span wires 1px, catenary sag via parabolic curve (not straight lines), overall line darkness reduced; (2) Road plane — full ROAD_ASPHALT solid trapezoid base, faded center double-yellow dashed lines converging to VP, crosswalk stripes at near end (perspective-correct trapezoid stripes). Output: `LTG_ENV_millbrook_main_street_v002.png`. | Pillow |
| `LTG_TOOL_bg_tech_den_v002.py` | Jordan Reed / Cycle 20 | Tech Den background fix pass (Critique C9, Takeshi Murakami C+). Fixes: (1) Window light shaft — trapezoid of SUNLIT_AMBER (212,172,100) with feathered soft edges (GaussianBlur), 15 dust motes as warm-white circles (alpha 60–80) within beam; (2) Monitor glow spill — blue-white (180,200,210, alpha 38–50) cast onto chair back/seat, desk surface in front of monitors, nearest shelving face; (3) Right half completion — bedding drawn as polygon (not rectangle), explicit pillow shapes, blanket fold, device on mattress edge, wall above bed with circuit-diagram poster + 2 taped printouts (code lines + schematic); (4) Cosmo's jacket — RW-08 dusty lavender (160,150,175) as prominent polygon draped over chair back with collar detail and shadow side, reads as inhabited silhouette. Canvas 1280×720. Output: `LTG_ENV_tech_den_v002.png`. | Pillow |
| `LTG_TOOL_bg_grandma_kitchen_v002.py` | Jordan Reed / Cycle 21 | Grandma Miri's Kitchen background fix pass (Critique C9, Takeshi Murakami B+). Three targeted improvements: (1) Floor linoleum grid overlay — 60×60px tile grid at 2px/alpha-25 over the floor area, plus worn-path trapezoid from doorway-to-stove (lighter warm buff, alpha 20); (2) Upper wall period wallpaper texture — horizontal stripes at 12–15% opacity alternating warm cream/buff, applied to upper 50% of back wall; (3) Enhanced CRT glow — primary glow radius increased to 80 (was 60), second wider ambient ring at radius 130 and alpha 8 for atmospheric doorway presence. Note: ltg_render_lib.py (Kai Nakamura, Cycle 21) not yet available; scanline_overlay() skipped. Canvas 1920×1080. Output: `LTG_ENV_grandma_kitchen_v002.png`. | Pillow |
| `LTG_TOOL_render_lib_v001.py` | Kai Nakamura / Cycle 21 (renamed Cycle 22) | **Canonical shared rendering utility library** for all LTG generators. `__version__ = "1.0.0"`. Provides: `perlin_noise_texture()`, `gaussian_glow()` (dead-alpha bug fixed Cycle 22), `light_shaft()`, `dust_motes()`, `catenary_wire()`, `scanline_overlay()`, `vignette()`. No external deps beyond Pillow. Import: `from LTG_TOOL_render_lib_v001 import *`. Deprecated wrapper `ltg_render_lib.py` removed Cycle 23 — all consumer scripts updated to import from canonical name. | Pillow |
| `LTG_TOOL_bg_tech_den_v003.py` | Kai Nakamura / Cycle 21 | Tech Den background v003. Upgrades v002 lighting/atmosphere calls to use LTG_TOOL_render_lib_v001: `light_shaft()` for window beam, `dust_motes()` for beam particles, `gaussian_glow()` for monitor spill, `vignette()` as final pass. All visual content (desks, monitors, shelving, jacket, bed, posters) preserved from v002. Canvas 1280×720. Output: `LTG_ENV_tech_den_v003.png`. | Pillow, LTG_TOOL_render_lib_v001 |
| `LTG_TOOL_bg_glitchlayer_frame_v003.py` | Kai Nakamura / Cycle 21 | Glitch Layer background v003. All platform/aurora/flora/pixel-trail content from v001 preserved. New: `scanline_overlay()` from LTG_TOOL_render_lib_v001 applied as final pass (spacing=4, alpha=18) — the Glitch Layer is a CRT interior, scanlines are canonical. Canvas 1920×1080. Output: `LTG_ENV_glitchlayer_frame_v003.png`. | Pillow, LTG_TOOL_render_lib_v001 |
| `LTG_TOOL_byte_expression_sheet_v004.py` | Maya Santos / Cycle 22 | Byte expression sheet v004. Previously misnamed `LTG_CHAR_byte_expression_sheet_v004.py` — renamed in Cycle 22 to comply with TOOL category convention. | Pillow |
| `LTG_TOOL_cosmo_expression_sheet_v004.py` | Maya Santos / Cycle 22 | Cosmo expression sheet v004. Previously misnamed `LTG_CHAR_cosmo_expression_sheet_v004.py` — renamed in Cycle 22 to comply with TOOL category convention. | Pillow |
| `LTG_TOOL_bg_glitch_layer_encounter_v001.py` | Jordan Reed / Cycle 21 | Glitch Layer encounter background generator. Previously misnamed `bg_glitch_layer_encounter.py` in `output/backgrounds/environments/` — relocated and renamed in Cycle 21/22. LTG-compliant copy lives in `output/tools/`. | Pillow |
| `LTG_TOOL_bg_tech_den_v004.py` | Jordan Reed / Cycle 22 | Tech Den background v004. Resolves Takeshi Murakami Critique C10 P1+P2. Fix 1a: light shaft repositioned to land ON desk surface (DESK_TOP_Y=395) — apex near window top, base at (10,407)+(210,390), max_alpha=150. Fix 1b: single wide-ellipse desk glow removed; replaced with three separate `gaussian_glow()` calls — CRT1 (r=110, alpha 65), CRT2 (r=100, alpha 58), flat panel (r=90, alpha 52) — each hotspots its desk zone. Import updated to `LTG_TOOL_render_lib_v001` (Cycle 23). Canvas 1280×720. Output: `LTG_ENV_tech_den_v004.png`. | Pillow, LTG_TOOL_render_lib_v001 |
| `LTG_TOOL_bg_grandma_kitchen_v003.py` | Jordan Reed / Cycle 22 | Grandma Miri's Kitchen background v003. Resolves Takeshi Murakami Critique C10 P3. Fix 2a: `draw_upper_wall_texture()` extended to left and right wall polygons via PIL polygon mask — side wall alpha ~35% less (8/10 vs 12/15). Fix 2b: `draw_floor_tiles()` disabled (no-op), `draw_floor_linoleum_overlay()` rewritten with single perspective-correct grid converging to vp_x (non-linear row spacing + converging column lines). One floor system. All v002 improvements retained. Canvas 1920×1080. Output: `LTG_ENV_grandma_kitchen_v003.png`. | Pillow |
| `LTG_TOOL_stylize_handdrawn_v001.py` | Rin Yamamoto / Cycle 23 | Hand-drawn stylization pass tool. Applies organic stylization to digitally generated PNGs. Three modes: `realworld` (paper grain, line wobble, warm edge bleed, chalk highlights), `glitch` (scanlines, RGB color separation, edge sharpening), `mixed` (zone-blended: glitch upper 2/3, realworld lower 1/3 with 200px gradient seam). Module API: `stylize(input_path, output_path, mode, intensity, seed)`. CLI: `python LTG_TOOL_stylize_handdrawn_v001.py input.png output.png --mode realworld`. CORRUPT_AMBER hue-locked throughout. Optional NumPy fast path. | Pillow, NumPy (optional), LTG_TOOL_render_lib_v001 (optional) |
| `LTG_TOOL_batch_stylize_v001.py` | Kai Nakamura / Cycle 24 | Batch runner for `LTG_TOOL_stylize_handdrawn_v001.stylize()`. Accepts a list of `(input_path, output_path, mode, intensity)` job tuples and processes each in sequence. Provides both module API (`batch_stylize(jobs, seed, stop_on_error)`) and CLI (`--jobs JSON` or `--glob PATTERN --out-dir DIR`). Writes optional results JSON summary. Runnable from `/home/wipkat/team`. | Pillow, LTG_TOOL_stylize_handdrawn_v001 |

---

## Registration Instructions

When a new script is created, add a row to the Script Index above with:
- **Script Name:** filename including extension (e.g. `LTG_TOOL_confetti_emitter_v001.py`)
- **Created By:** team member name
- **Purpose:** one-sentence description of what the script does
- **Dependencies:** Python packages or external tools required (e.g. `Pillow`, `ImageMagick`, `svgwrite`)

Scripts must follow the standard naming convention: `LTG_TOOL_[descriptor]_v[###].[ext]`

All scripts are stored in this directory (`/home/wipkat/team/output/tools/`) and version-controlled via standard Git.

---

## Render Library — API Reference (LTG_TOOL_render_lib_v001.py)

**Version:** 1.1.0 (C24: `paper_texture()` added)
**Canonical import pattern (run from any directory):**
```python
import sys, os
sys.path.insert(0, "/home/wipkat/team/output/tools")
from LTG_TOOL_render_lib_v001 import (
    perlin_noise_texture, gaussian_glow, light_shaft,
    dust_motes, catenary_wire, scanline_overlay, vignette, paper_texture
)
```

| Function | Signature | Returns | Notes |
|---|---|---|---|
| `perlin_noise_texture` | `(width, height, scale=50, seed=42, octaves=3, alpha=60)` | RGBA Image | Layered sin/cos noise. Slow at full canvas — use 960×540 + upscale for perf. |
| `gaussian_glow` | `(img, center, radius, color, max_alpha=100, steps=10)` | img (RGBA, in-place) | Alpha floored at 1 to prevent dead outer ellipses. |
| `light_shaft` | `(img, apex, base_left, base_right, color, max_alpha=60)` | img (RGBA, in-place) | Triangle polygon; GaussianBlur feather pass. |
| `dust_motes` | `(draw, bounds, count=20, seed=42, color, alpha_range)` | None (draws in-place) | draw must be attached to RGBA image. |
| `catenary_wire` | `(draw, p0, p1, sag=0.05, color, width=2)` | None (draws in-place) | Parabolic 40-segment polyline. |
| `scanline_overlay` | `(img, spacing=4, alpha=15)` | RGBA Image | Converts to RGBA if needed. |
| `vignette` | `(img, strength=60)` | RGBA Image | Converts to RGBA if needed. Mach-band ring approximation (intentional). |
| `paper_texture` | `(img, scale=40, alpha=20, seed=42)` | RGBA Image | **Added C24.** 1/4-res grain tile + NN upscale. Fast in pure Python. |

### `paper_texture()` details
Composites a procedural paper/canvas grain over the source image. Works at 1/4 resolution internally for speed (O((W/4)×(H/4)) pixel loop — <1s at 1920×1080 in pure Python). Upscales with nearest-neighbour to preserve grain character. Three layered sin/cos octaves. Seed is reproducible.

- `scale`: grain wavelength in pixels. 20 = very fine; 40 = standard paper tooth; 80 = coarse canvas.
- `alpha`: maximum per-pixel grain opacity. 8–20 = subtle/professional; 30–40 = heavy hand-drawn texture.
- `seed`: reproducible. Same seed + scale + alpha = identical grain.

---

## Pipeline Health — C24

**Audit date:** 2026-03-29 (Cycle 24)
**Audited by:** Kai Nakamura

### Summary

The deprecated wrapper `ltg_render_lib.py` was deleted in Cycle 23. All active consumer scripts now import from `LTG_TOOL_render_lib_v001` directly. This audit verifies no live code references the old import path.

### Old-pattern references found

A grep of `output/**/*.py` for `ltg_render_lib` returned the following hits. Each is categorized:

| File | Line | Content | Category | Action Required |
|---|---|---|---|---|
| `output/tools/LTG_TOOL_render_lib_v001.py` | 5 | `Renamed from ltg_render_lib.py in Cycle 22...` | Docstring — historical note | None — intentional |
| `output/tools/LTG_TOOL_bg_tech_den_v003.py` | 7 | `...replaces all inline lighting code with calls to ltg_render_lib.` | Docstring — old module name | None — benign comment |
| `output/tools/LTG_TOOL_bg_tech_den_v003.py` | 290, 300, 746 | `# ── ... via ltg_render_lib.function()` | Inline comment | None — comment only; actual import is `LTG_TOOL_render_lib_v001` ✓ |
| `output/tools/LTG_TOOL_bg_tech_den_v004.py` | 301, 315, 769 | `# ── ... via ltg_render_lib.function()` | Inline comment | None — comment only; actual import is `LTG_TOOL_render_lib_v001` ✓ |
| `output/backgrounds/environments/LTG_ENV_tech_den_v004.py` | 301, 315, 769 | `# ── ... via ltg_render_lib.function()` | Inline comment | None — comment only; actual import is `LTG_TOOL_render_lib_v001` ✓ |
| `output/tools/LTG_TOOL_bg_glitchlayer_frame_v003.py` | 10, 105, 295 | `scanline_overlay() from ltg_render_lib applied...` | Docstring/comment | None — comment only; actual import is `LTG_TOOL_render_lib_v001` ✓ |
| `output/tools/LTG_TOOL_bg_grandma_kitchen_v002.py` | 25, 1056 | `ltg_render_lib.py not yet available` | Docstring — historical note | None — this was written before C21; v003 supersedes v002 |

### Live import verification

A separate grep for `from ltg_render_lib` and `import ltg_render_lib` (executable import statements) found **zero matches**. The pipeline is clean.

Files confirmed using the canonical `LTG_TOOL_render_lib_v001` import:
- `output/tools/LTG_TOOL_bg_tech_den_v003.py` ✓
- `output/tools/LTG_TOOL_bg_tech_den_v004.py` ✓
- `output/tools/LTG_TOOL_bg_glitchlayer_frame_v003.py` ✓
- `output/backgrounds/environments/LTG_ENV_tech_den_v004.py` ✓
- `output/tools/LTG_TOOL_stylize_handdrawn_v001.py` ✓ (optional try/import with correct name)

### Stale TODO comments

Several files contain `# TODO: update import to LTG_TOOL_render_lib_v001 after Kai's rename` in their docstrings. These files do **not** import the render lib at all — the TODO was written as a precaution and was never needed. The comments are stale but harmless.

| File | Status |
|---|---|
| `output/tools/LTG_CHAR_cosmo_expression_sheet_v004.py` | TODO is stale — no render lib import present or needed |
| `output/tools/LTG_CHAR_byte_expression_sheet_v004.py` | TODO is stale — no render lib import present or needed |
| `output/tools/LTG_TOOL_byte_expression_sheet_v004.py` | TODO is stale — no render lib import present or needed |
| `output/tools/LTG_CHAR_luma_expression_sheet_v004.py` | TODO is stale — no render lib import present or needed |
| `output/characters/main/LTG_CHAR_cosmo_expression_sheet_v004.py` | TODO is stale — no render lib import present or needed |
| `output/characters/main/LTG_CHAR_byte_expression_sheet_v004.py` | TODO is stale — no render lib import present or needed |
| `output/characters/main/LTG_CHAR_luma_expression_sheet_v004.py` | TODO is stale — no render lib import present or needed |
| `output/color/style_frames/LTG_TOOL_style_frame_02_glitch_storm_v005.py` | TODO is stale — no render lib import present or needed |

### Verdict

**Pipeline is healthy.** No live code imports the deleted `ltg_render_lib.py` wrapper. All stale references are in comments and docstrings only — no functional risk. Stale TODO comments noted above may be cleaned up opportunistically in a future cycle but require no immediate action.
