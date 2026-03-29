# Tools Index — "Luma & the Glitchkin"

**Maintained by:** Alex Chen, Art Director
**Last updated:** 2026-03-30 (Cycle 32 — procedural_draw v1.3.0 char_cx, SF01 v005, SF04 v004 rebuild, turnaround v004 eye-width fix, Rin Yamamoto)

---

## Image Output Rule
**Prefer the smallest resolution appropriate for the task.** Hard limit: **≤ 1280px in both dimensions.**
Apply before saving any image:
```python
img.thumbnail((1280, 1280), Image.LANCZOS)
```
Aspect ratio is preserved automatically. Only use large sizes when fine detail inspection is required. For detail/crop images: also ≤ 1280×1280px.

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
| `LTG_TOOL_naming_cleanup_v001.py` | Kai Nakamura / Cycle 29 | Removes original LTG_CHAR_/LTG_COLOR_/LTG_BRAND_ `.py` source files from `output/tools/` once their canonical LTG_TOOL_ copies are confirmed on disk. 22 files queued. Run with `--dry-run` to preview removals without deleting. After run: forwarding stubs in this dir should also be manually removed. | stdlib only |
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
| ~~`LTG_TOOL_stylize_handdrawn_v001.py`~~ | Rin Yamamoto / Cycle 23 | **RETIRED Cycle 26 — moved to `output/tools/legacy/`.** Hand-drawn stylization pass tool (realworld, glitch, mixed modes). Post-processing pipeline retired as of Cycle 26. | Pillow, NumPy (optional) |
| ~~`LTG_TOOL_batch_stylize_v001.py`~~ | Kai Nakamura / Cycle 24–25 | **RETIRED Cycle 26 — moved to `output/tools/legacy/`.** Batch runner for the stylize pipeline. Post-processing pipeline retired as of Cycle 26. | Pillow, LTG_TOOL_stylize_handdrawn_v002 |
| ~~`LTG_TOOL_stylize_handdrawn_v002.py`~~ | Rin Yamamoto / Cycle 25 | **RETIRED Cycle 26 — moved to `output/tools/legacy/`.** Hand-drawn stylization pass v002 (4 canonical color protection fixes). Post-processing pipeline retired as of Cycle 26. | Pillow, NumPy (optional) |
| `LTG_TOOL_color_verify_v001.py` | Kai Nakamura / Cycle 25 | Canonical color verification utility. Samples canonical palette colors from a PIL Image and returns per-color hue drift analysis. `verify_canonical_colors(img, palette_dict, max_delta_hue=5)` — returns per-color `{target_hue, found_hue, delta, pass}` + `overall_pass`. `get_canonical_palette()` — returns standard LTG 6-color palette dict. Colors not present in the image are marked `not_found` (not a failure). Designed as a gating function: call after stylize() or any processing pass that could shift hues. Standalone; no imports beyond `colorsys` + Pillow. All six canonical colors verified from `master_palette.md`. | Pillow (colorsys stdlib) |
| `LTG_TOOL_byte_expression_sheet_v001.py` | Alex Chen / Cycle 13 | Byte expression sheet v001. Migrated from `byte_expressions_generator.py`. 4×2 grid (7 expressions): NEUTRAL/DEFAULT-GRUMPY added (Dmitri Volkov P1). Output: `LTG_CHAR_byte_expression_sheet_v001.png`. | Pillow |
| `LTG_TOOL_byte_expression_sheet_v003.py` | Maya Santos / Cycle 21 | Byte expression sheet v003. Adds STORM/CRACKED damage state (9th expression). Layout upgraded to 3×3 grid. Storm pose: right eye uses dead-pixel cracked glyph per byte.md §9B, bent antenna, angular lean (+18 tilt). Output: `LTG_CHAR_byte_expression_sheet_v003.png`. | Pillow |
| `LTG_TOOL_cosmo_expression_sheet_v001.py` | Maya Santos / Cycle 14 | Cosmo expression sheet v001. 6 expressions: THOUGHTFUL, SKEPTICAL, DELIGHTED, AWKWARD, WORRIED, SURPRISED. 3×2 grid, 1200×900. Cycle 16 fixes: SKEPTICAL body_tilt adjusted, two empty slots populated. Output: `LTG_CHAR_cosmo_expression_sheet_v001.png`. | Pillow |
| `LTG_TOOL_cosmo_expression_sheet_v002.py` | Maya Santos / Cycle 14/16 | Cosmo expression sheet v002. Carries Cycle 16 fixes from v001 (SKEPTICAL tilt, WORRIED+SURPRISED added). Shares same 6-expression set. Output: `LTG_CHAR_cosmo_expression_sheet_v002.png`. | Pillow |
| `LTG_TOOL_cosmo_expression_sheet_v003.py` | Maya Santos / Cycle 19 | Cosmo expression sheet v003. Critical fix: body_tilt displacement formula corrected (was 0.4× factor = invisible at thumbnail; now full pixel displacement). Carries all v001/v002 expressions. Output: `LTG_CHAR_cosmo_expression_sheet_v003.png`. | Pillow |
| `LTG_TOOL_cosmo_turnaround_v002.py` | Maya Santos / Cycle 25 | Cosmo 4-view turnaround v002. Side-view depth fix. Forwarding stub → `LTG_CHAR_cosmo_turnaround_v002.py`. Output: `LTG_CHAR_cosmo_turnaround_v002.png`. | Pillow |
| `LTG_TOOL_glitch_expression_sheet_v001.py` | Maya Santos / Cycle 23 | Glitch expression sheet v001. 4 expressions: NEUTRAL, MISCHIEVOUS, PANICKED, TRIUMPHANT. 2×2 grid, 800×800. Diamond/rhombus body with CORRUPT_AMBER, HOT_MAGENTA crack lines, 3×3 pixel dual-eye system. Output: `LTG_CHAR_glitch_expression_sheet_v001.png`. | Pillow |
| `LTG_TOOL_glitch_expression_sheet_v002.py` | Maya Santos / Cycle 24 | Glitch expression sheet v002. Expands to 6 expressions: adds STUNNED and CALCULATING. 3×2 grid, 1200×900. Output: `LTG_CHAR_glitch_expression_sheet_v002.png`. | Pillow |
| `LTG_TOOL_glitch_expression_sheet_v003.py` | Maya Santos / Cycle 28 | Glitch expression sheet v003. Expands to 9 expressions: adds YEARNING, REACHING OUT, REMEMBERING (interior desire expressions per Nkechi Adeyemi C12). 3×3 grid, 1200×900. Output: `LTG_CHAR_glitch_expression_sheet_v003.png`. | Pillow |
| `LTG_TOOL_glitch_turnaround_v001.py` | Maya Santos / Cycle 23 | Glitch 4-view turnaround v001. FRONT, 3/4, SIDE, BACK views. 1600×700 canvas. Diamond body in CORRUPT_AMBER with HOT_MAGENTA crack lines. Output: `LTG_CHAR_glitch_turnaround_v001.png`. | Pillow |
| `LTG_TOOL_glitch_turnaround_v002.py` | Maya Santos / Cycle 24 | Glitch turnaround v002. Shadow contrast fix: SIDE and BACK views use CORRUPT_AMB_SHADOW (not UV_PURPLE) for depth shadows. Output: `LTG_CHAR_glitch_turnaround_v002.png`. | Pillow |
| `LTG_TOOL_glitch_color_model_v001.py` | Sam Kowalski / Cycle 23 | Glitch color model. 800×500 canvas, 10 swatches grouped by zone (body, cracks, shadow, glow, outline). All values from master_palette.md. Output: `LTG_COLOR_glitch_color_model_v001.png`. | Pillow |
| `LTG_TOOL_grandma_miri_expression_sheet_v001.py` | Maya Santos / Cycle 17 | Grandma Miri expression sheet v001. 5 expressions: WARM/WELCOMING, NOSTALGIC/WISTFUL, CONCERNED, SURPRISED/DELIGHTED, WISE/KNOWING. 3+2 grid, 1200×900. Output: `LTG_CHAR_grandma_miri_expression_sheet_v001.png`. | Pillow |
| `LTG_TOOL_grandma_miri_expression_sheet_v002.py` | Maya Santos / Cycle 19 | Grandma Miri expression sheet v002. Ground-up rebuild (v001 failed squint test). Body-language differentiation: full-body gesture change per expression, not face-only. Output: `LTG_CHAR_grandma_miri_expression_sheet_v002.png`. | Pillow |
| `LTG_TOOL_grandma_miri_expression_sheet_v003.py` | Maya Santos / Cycle 25 | Grandma Miri expression sheet v003. Narrative expression addition (Cycle 25). Forwarding stub → `LTG_CHAR_grandma_miri_expression_sheet_v003.py`. Output: `LTG_CHAR_grandma_miri_expression_sheet_v003.png`. | Pillow |
| `LTG_TOOL_grandma_miri_color_model_v001.py` | Sam Kowalski / Cycle 17 | Grandma Miri color model. 800×500 canvas, swatches grouped by zone (face/skin, hair, clothing, accessories). All values from grandma_miri_color_model.md + master_palette.md. Output: `LTG_COLOR_grandma_miri_color_model_v001.png`. | Pillow |
| `LTG_TOOL_luma_color_model_v001.py` | Sam Kowalski / Cycle 25 | Luma color model. 800×500 canvas, 14 swatches (hoodie orange, skin, hair, pants, shoes, pixel cyan/magenta zones). All values from luma_color_model.md. Output: `LTG_COLOR_luma_color_model_v001.png`. | Pillow |
| `LTG_TOOL_byte_color_model_v001.py` | Sam Kowalski / Cycle 25 | Byte color model. 800×500 canvas, 14 swatches. CRITICAL: body fill = GL-01b #00D4E8 BYTE_TEAL (not #00F0FF Electric Cyan). Output: `LTG_COLOR_byte_color_model_v001.png`. | Pillow |
| `LTG_TOOL_cosmo_color_model_v001.py` | Sam Kowalski / Cycle 25 | Cosmo color model. 800×500 canvas, 14 swatches (cerulean/sage stripes, glasses). All values from cosmo_color_model.md. Output: `LTG_COLOR_cosmo_color_model_v001.png`. | Pillow |
| `LTG_TOOL_luma_expression_sheet_v005.py` | Maya Santos / Cycle 25 | Luma expression sheet v005. Forwarding stub → `LTG_CHAR_luma_expression_sheet_v005.py`. Output: `LTG_CHAR_luma_expression_sheet_v005.png`. | Pillow |
| `LTG_TOOL_luma_expression_sheet_v006.py` | Maya Santos / Cycle 27 | **Current Luma expression sheet.** Luma expression sheet v006. Forwarding stub → `LTG_CHAR_luma_expression_sheet_v006.py`. Output: `LTG_CHAR_luma_expression_sheet_v006.png`. | Pillow |
| `LTG_TOOL_luma_turnaround_v002.py` | Maya Santos / Cycle 25 | Luma 4-view character turnaround v002 (Cycle 25/26). Forwarding stub → `LTG_CHAR_luma_turnaround_v002.py`. Output: `LTG_CHAR_luma_turnaround_v002.png`. | Pillow |
| `LTG_TOOL_luma_turnaround_v003.py` | Maya Santos / Cycle 28 | Luma turnaround v003. Line weight corrected to v006 3-tier standard at 2× render (head=4, structure=3, detail=2). All views updated. Output: `LTG_CHAR_luma_turnaround_v003.png`. | Pillow |
| `LTG_TOOL_miri_turnaround_v001.py` | Maya Santos / Cycle 20 | Grandma Miri 4-view character turnaround. 1600×800 canvas, 3-tier line weight. MIRI-A canonical: bun + crossed chopsticks, A-line cardigan, round glasses. Height 3.2 heads. Output: `LTG_CHAR_miri_turnaround_v001.png`. | Pillow |
| `LTG_TOOL_character_lineup_v004.py` | Maya Santos / Cycle 24 | Character lineup v004. Added Glitch (5th character, far right). Glitch: diamond body in CORRUPT_AMBER, HOT_MAG crack, UV_PURPLE shadow, VOID_BLACK outline, hover. Output: `LTG_CHAR_lineup_v004.png`. | Pillow |
| `LTG_TOOL_character_lineup_v005.py` | Maya Santos / Cycle 27 | **Current character lineup.** Luma rebuilt to v006-era construction (8-ellipse hair curl cloud, cheek nubs, near-circular eyes, 3-tier line weight at lineup scale). Output: `LTG_CHAR_lineup_v005.png`. | Pillow |
| `LTG_TOOL_luma_cold_overlay_swatches_v001.py` | Sam Kowalski / Cycle 18 | Cold overlay swatch generator. Reference PNG showing base color, Electric Cyan overlay, and alpha-composite result side-by-side for each cold overlay variant from luma_color_model.md. 1280×1067 (≤1280 after thumbnail). Output: `LTG_COLOR_luma_cold_overlay_v001.png`. | Pillow |
| `LTG_TOOL_luma_classroom_pose_v001.py` | Maya Santos / Cycle 14 | Luma classroom sitting pose for storyboard beat A1-04. Seated at desk, slight slouch, left hand supporting chin (distracted lean), right hand pen-tapping desk, head tilted 8° toward blackboard. Output: `LTG_CHAR_luma_classroom_pose_v001.png`. | Pillow |
| `LTG_TOOL_fidelity_check_c24.py` | Sam Kowalski / Cycle 24 | Color fidelity check utility. Samples 6 canonical palette colors from styled PNGs vs originals. Tolerance 20 per channel. Targets: GL-07 CORRUPT_AMBER, GL-01b BYTE_TEAL, UV_PURPLE, SUNLIT_AMBER, SOFT_GOLD, ENV-06. Precursor to `LTG_TOOL_color_verify_v001.py`. | Pillow |
| `LTG_TOOL_logo_v001.py` | Alex Chen / Cycle 25 | Canonical show logo entry point. Imports from `LTG_TOOL_logo_asymmetric_v002.py` and saves output to `output/production/LTG_BRAND_logo_v001.png`. Alias/entry point for the canonical Cycle 13 asymmetric logo design. | Pillow |
| `LTG_TOOL_style_frame_02_glitch_storm_v005.py` | Sam Kowalski / Cycle 22 | SF02 Glitch Storm fix pass (Critique C10). Reduced window pane alpha (160/180 → 115/110). Source in `output/color/style_frames/`; stub in `output/tools/` is location-compliance entry point. Output: `LTG_COLOR_style_frame_02_glitch_storm_v005.png`. | Pillow |
| `LTG_TOOL_style_frame_03_other_side_v004.py` | Sam Kowalski / Cycle 27 | SF03 Other Side confetti fix pass. Confetti particles constrained to within 150px of nearest character/platform anchor (was full-canvas scatter). Output: `LTG_COLOR_styleframe_otherside_v004.png`. | Pillow |
| `LTG_TOOL_style_frame_03_other_side_v005.py` | Sam Kowalski / Cycle 28 | SF03 Other Side UV_PURPLE_DARK saturation fix. Corrected from (43,32,80)=#2B2050 (31% sat) to GL-04a (58,16,96)=#3A1060 (72% sat). Deep void zones now read as digital void, not grey-purple. Output: `LTG_COLOR_styleframe_otherside_v005.png`. | Pillow |
| `LTG_TOOL_styleframe_luma_byte_v001.py` | Sam Kowalski / Cycle 25 | SF04 "The Dynamic" (Luma + Byte interaction) v001. Forwarding stub → `LTG_COLOR_styleframe_luma_byte_v001.py`. Output: `LTG_COLOR_styleframe_luma_byte_v001.png`. | Pillow |
| `LTG_TOOL_styleframe_luma_byte_v002.py` | Sam Kowalski / Cycle 27 | SF04 "The Dynamic" v002. Procedural quality upgrade. Forwarding stub → `LTG_COLOR_styleframe_luma_byte_v002.py`. Output: `LTG_COLOR_styleframe_luma_byte_v002.png`. | Pillow |
| `LTG_TOOL_styleframe_luma_byte_v003.py` | Rin Yamamoto / Cycle 28 | SF04 "The Dynamic" v003. Forwarding stub → `LTG_COLOR_styleframe_luma_byte_v003.py`. Output: `LTG_COLOR_styleframe_luma_byte_v003.png`. | Pillow |
| `LTG_TOOL_procedural_draw_v001.py` | Rin Yamamoto / Cycle 26 (v1.3.0 C32) | **Procedural drawing library.** `wobble_line()`, `wobble_polygon()`, `variable_stroke()`, `add_rim_light(side, char_cx=None)`, `silhouette_test()`, `value_study()`, `add_face_lighting()`. v1.3.0 (C32): `add_rim_light()` gains optional `char_cx` parameter — when provided, right/left side mask is character-relative (x > char_cx) instead of canvas-center. Fixes rim-light exclusion bug for left-of-center characters (Sven C13 P1). Backward compatible (default None = canvas center). | Pillow |
| `LTG_TOOL_render_qa_v001.py` | Kai Nakamura / Cycle 26 (v1.1.0 C27, v1.2.0 C30) | **Render Quality Assessment tool.** Evaluates any LTG PNG against rendering standards across 5 checks: (A) silhouette readability at 100×100 (score: distinct/ambiguous/blob), (B) value range (darkest ≤ 30, brightest ≥ 225, range ≥ 150), (C) color fidelity via `verify_canonical_colors()`, (D) warm/cool separation ≥ 20 PIL hue units (top/bottom zone sampling), (E) line weight consistency (20 random edge samples, outlier detection). API: `qa_report(img_path, asset_type=None) → dict` (v1.1.0: `asset_type` parameter added C27; v1.2.0 C30: automatic downscale to ≤1280px on input image before QC checks), `qa_batch(directory) → list[dict]`, `qa_summary_report(results, output_path)` (writes Markdown). Also exports `silhouette_test(img) → PIL.Image` and `value_study(img) → PIL.Image` — interfaces compatible with `LTG_TOOL_procedural_draw_v001.py`. Overall grade: PASS / WARN / FAIL. Cycle 26 baseline QA run on 8 C25 assets: all WARN (main issue: warm/cool separation — character sheets are intentionally neutral-dominant; use `asset_type="character_sheet"` to suppress this false-positive). | Pillow, LTG_TOOL_color_verify_v001 |
| `LTG_TOOL_luma_expression_sheet_v007.py` | Maya Santos / Cycle 29 | Luma expression sheet v007 — PROPORTION FIX. HEAD-TO-BODY ratio corrected to 3.2 heads (torso_h HR×2.10, was HR×1.80). Eye width corrected to HR×0.22 (canonical spec from turnaround v003, was HR×0.28). All v006 features retained: classroom-style head/hair/eyes, 6-expression 3×2 layout, per-expression hoodie color map, 2× LANCZOS AA, full-body silhouette differentiation. Output: `LTG_CHAR_luma_expressions_v007.png` (1200×900). | Pillow |
| `LTG_TOOL_character_lineup_v006.py` | Maya Santos / Cycle 29 | Character lineup v006. Luma updated to v007 canonical proportions: 3.2 heads (was 3.5), eye width r×0.22 (was r×0.28). All 5 characters present. Other characters (Byte, Cosmo, Miri, Glitch) unchanged from v005. Output: `LTG_CHAR_luma_lineup_v006.png`. | Pillow |
| `LTG_TOOL_styleframe_discovery_v004.py` | Rin Yamamoto / Cycle 29 | SF01 "The Discovery" procedural quality pass. Brings SF01 to same quality level as SF04 v003: wobble_polygon() on Luma head, CRT frame and couch; variable_stroke() on head perimeter arcs (8-arc); add_face_lighting() warm lamp from upper-left; add_rim_light() cool CRT from right. Canvas 1280×720 (≤1280px direct). All v003 fixes retained (ghost Byte alpha, specs[2]+specs[3] placement). Output: `LTG_COLOR_styleframe_discovery_v004.png`. | Pillow, LTG_TOOL_procedural_draw_v001 |
| `LTG_TOOL_styleframe_discovery_v005.py` | Rin Yamamoto / Cycle 32 | SF01 "The Discovery" rim-light char_cx fix. Fixes canvas-midpoint bug: Luma at ~x=0.29W now receives correct right-side rim (char_cx=head_cx passed to add_rim_light). All C29/C30 procedural quality features retained. Requires procedural_draw v1.3.0. Output: `LTG_COLOR_styleframe_discovery_v005.png` (1280×720). | Pillow, LTG_TOOL_procedural_draw_v001 |
| `LTG_TOOL_styleframe_luma_byte_v004.py` | Rin Yamamoto / Cycle 32 | SF04 "The Dynamic" FULL REBUILD (C32 — sources lost in C28). Reconstructed from v003 PNG as reference. Sven C13 audit fixes: value ceiling 255 (was 198, PASS ≥225), clear silhouette, Byte body GL-01b #00D4E8 canonical, BYTE_TEAL monitor contribution on Byte's CRT-facing side, Luma blush #E8A87C, warm upper-left face lighting, rim lights with char_cx. Specular highlights ensure ≥225. Output: `LTG_COLOR_styleframe_luma_byte_v004.png` (1280×720). | Pillow, LTG_TOOL_procedural_draw_v001 |
| `LTG_TOOL_luma_turnaround_v004.py` | Rin Yamamoto / Cycle 32 | Luma turnaround v004 — eye-width canonical fix (Alex Chen C32 directive / Daisuke C13 P1). v003 used ew=int(h*0.22) where h=head-height → ew was int(head_r*0.44), 2× too wide. v004 corrects: ew=int(head_r*0.22) where head_r=radius=int(h*0.50). All three views fixed (FRONT, 3/4, SIDE). All v003 line weights and proportions retained. Output: `LTG_CHAR_luma_turnaround_v004.png` (1280×560). | Pillow |
| `LTG_TOOL_draw_order_lint_v001.py` | Kai Nakamura / Cycle 31 | **Draw-order static linter.** Parses generator .py files via regex (no execution, no AST) and flags painter's-algorithm violations: W001 head/face drawn before body; W002 outline drawn before fill for same element; W003 shadow drawn after the element it should darken; W004 img.paste()/alpha_composite() not followed by draw = ImageDraw.Draw(img) refresh within 5 lines. API: `lint_file(path) → dict` (result: PASS/WARN, warnings list with line/code/message), `lint_directory(directory, pattern) → list`, `format_report(results) → str`. CLI: run against glob of .py files, saves report to `LTG_TOOL_draw_order_lint_v001_report.txt`. C31 run: 114 files — 59 PASS / 55 WARN / 0 ERROR (most WARNs are W004 missing draw refresh). | stdlib only |
| `LTG_TOOL_color_verify_v002.py` | Kai Nakamura / Cycle 31 | **Color verification utility v002 — adds histogram mode.** Full v001 API preserved. New optional `histogram=True` parameter on `verify_canonical_colors()`: per-color result gains `hue_histogram` (list of dicts, 5° buckets, 72 total), `histogram_bucket_deg` (5), `canonical_bucket_index` (int marking canonical hue's bucket). `format_histogram(histogram, canonical_bucket_index)` helper produces ASCII bar chart. CLI: `python LTG_TOOL_color_verify_v002.py image.png [--histogram]`. Eliminates false-positive investigation by showing full hue distribution with canonical band highlighted. Backward compatible: histogram keys absent when histogram=False (default). | stdlib colorsys + Pillow |

---

## Legacy Archive — Cycle 26 Cleanup

**Producer directive — 2026-03-29 (Cycle 26)**

The post-processing stylization pipeline is **retired as of Cycle 26**. Style is now baked into generation at draw time (Rin Inoue's procedural draw approach). The following scripts have been moved to `output/tools/legacy/`:

- `LTG_TOOL_stylize_handdrawn_v001.py`
- `LTG_TOOL_stylize_handdrawn_v002.py`
- `LTG_TOOL_batch_stylize_v001.py`

Also removed: `run_sf02_sf03_regen.py` (no longer needed; SF02/SF03 regen superseded).

All `*_styled*.png` output images have been deleted from the project.

---

## Legacy Archive — Cycle 25 Cleanup

**Archived by:** Kai Nakamura — 2026-03-29 (Cycle 25)

Twenty legacy scripts (non-LTG-named, all with LTG equivalents) have been moved to
`output/tools/legacy/`. The LTG-named equivalents in this directory are canonical.

**See `output/tools/legacy/README.md` for the full archive manifest.**

Similarly, 27 legacy storyboard panel image files have been moved from
`output/storyboards/panels/` to `output/storyboards/panels/legacy/`.
See `output/storyboards/panels/legacy/README.md` for the archive manifest.

---

## Legacy Archive — Cycle 28 C28 Compliance Pass

**Kai Nakamura — 2026-03-29 (Cycle 28)**

Naming compliance pass (Reinhardt Böhm Critique C12). All generator `.py` files in `output/tools/` must use `LTG_TOOL_` prefix. PNG output filenames are unchanged.

**Conflict cases** — the following `LTG_CHAR_` files existed in `output/tools/` alongside distinct LTG_TOOL_ versions (different generators, not identical renames). Legacy stubs created in `output/tools/legacy/`:
- `LTG_CHAR_luma_expression_sheet_v002.py` → superseded by `LTG_TOOL_luma_expression_sheet_v002.py`
- `LTG_CHAR_luma_expression_sheet_v003.py` → superseded by `LTG_TOOL_luma_expression_sheet_v003.py`
- `LTG_CHAR_luma_expression_sheet_v004.py` → superseded by `LTG_TOOL_luma_expression_sheet_v004.py`
- `LTG_CHAR_byte_expression_sheet_v004.py` → superseded by `LTG_TOOL_byte_expression_sheet_v004.py`
- `LTG_CHAR_cosmo_expression_sheet_v004.py` → superseded by `LTG_TOOL_cosmo_expression_sheet_v004.py`

**New LTG_TOOL_ forwarding stubs created** (source files await `git mv` for history preservation):
- `LTG_TOOL_cosmo_turnaround_v002.py` → forwards to `LTG_CHAR_cosmo_turnaround_v002.py`
- `LTG_TOOL_styleframe_luma_byte_v001.py` → forwards to `LTG_COLOR_styleframe_luma_byte_v001.py`
- `LTG_TOOL_styleframe_luma_byte_v002.py` → forwards to `LTG_COLOR_styleframe_luma_byte_v002.py`
- `LTG_TOOL_styleframe_luma_byte_v003.py` → forwards to `LTG_COLOR_styleframe_luma_byte_v003.py`
- `LTG_TOOL_grandma_miri_expression_sheet_v003.py` → forwards to `LTG_CHAR_grandma_miri_expression_sheet_v003.py`
- `LTG_TOOL_luma_expression_sheet_v005.py` → forwards to `LTG_CHAR_luma_expression_sheet_v005.py`
- `LTG_TOOL_luma_expression_sheet_v006.py` → forwards to `LTG_CHAR_luma_expression_sheet_v006.py`
- `LTG_TOOL_luma_turnaround_v002.py` → forwards to `LTG_CHAR_luma_turnaround_v002.py`

**Misplaced file:** `output/color/style_frames/LTG_TOOL_style_frame_02_glitch_storm_v005.py` — already correctly named, but placed outside `output/tools/`. Entry point stub added at `output/tools/LTG_TOOL_style_frame_02_glitch_storm_v005.py`.

**Cycle 29 — Cleanup Tool Created:** `LTG_TOOL_naming_cleanup_v001.py` (see Script Index) removes all original LTG_CHAR_/LTG_COLOR_/LTG_BRAND_ source files once the canonical LTG_TOOL_ copy is confirmed on disk. No git repo is present; standard `os.remove()` is used. Run with `--dry-run` to preview. After running, forwarding stubs above should also be removed (they reference now-deleted files). The original LTG_CHAR_/LTG_COLOR_/LTG_BRAND_ files remain on disk until the script is executed.

---

## Legacy Archive — Cycle 29 Naming Cleanup

**Kai Nakamura — 2026-03-29 (Cycle 29)**

C29 naming compliance completion pass. 22 non-compliant `.py` files in `output/tools/` (prefixed LTG_CHAR_, LTG_COLOR_, LTG_BRAND_) are queued for removal. All have canonical LTG_TOOL_ copies on disk. Cleanup tool: `LTG_TOOL_naming_cleanup_v001.py`.

Files to be removed (all have LTG_TOOL_ canonical equivalents):
- `LTG_CHAR_luma_expression_sheet_v002–v006.py` (5 files)
- `LTG_CHAR_luma_turnaround_v002.py`
- `LTG_CHAR_byte_expression_sheet_v004.py`
- `LTG_CHAR_cosmo_expression_sheet_v004.py`, `LTG_CHAR_cosmo_turnaround_v002.py`
- `LTG_CHAR_grandma_miri_expression_sheet_v003.py`
- `LTG_CHAR_glitch_expression_sheet_v001–v002.py`, `LTG_CHAR_glitch_turnaround_v001–v002.py`, `LTG_CHAR_glitch_color_model_v001.py` (5 files)
- `LTG_COLOR_luma_color_model_v001.py`, `LTG_COLOR_byte_color_model_v001.py`, `LTG_COLOR_cosmo_color_model_v001.py`
- `LTG_COLOR_styleframe_luma_byte_v001–v003.py` (3 files)
- `LTG_BRAND_logo_v001.py`

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
