# Tools Index — "Luma & the Glitchkin"

**Maintained by:** Alex Chen, Art Director
**Last updated:** 2026-03-29 (Cycle 14)

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
| `LTG_CHAR_luma_expression_sheet_v002.py` | Maya Santos / Cycle 12 | MISNAMED: this is a Python script (tool) and should be named `LTG_TOOL_luma_expression_sheet_v002.py`. Lives in `tools/` directory correctly, but CATEGORY code should be `TOOL` not `CHAR`. Generates Luma expression sheet at 1200×800px with 6 expressions. Flag to Alex Chen for rename. | Pillow |
| `LTG_TOOL_style_frame_01_discovery_v003.py` | Alex Chen / Cycle 13 | SF01 Ghost Byte alpha calibration fix. Ghost body alpha 55→90, eye glints 65–70→105. Top-left monitor ghost removed (warm lamp bleed). Two ghost screens (top-right + mid-left only). Pitch-scale legible. Output: `LTG_COLOR_styleframe_discovery_v003.png`. | Pillow |
| `LTG_TOOL_logo_asymmetric_v002.py` | Alex Chen / Cycle 13 | Asymmetric logo v002. "&" connector gets warm-to-cold gradient treatment (SUNLIT_AMBER left → ELEC_CYAN right) via per-column alpha composite. "the/Glitchkin" inter-line gap reduced ~30%. Output: `LTG_BRAND_logo_asymmetric_v002.png`. | Pillow |
| `LTG_TOOL_style_frame_02_glitch_storm_v002.py` | Alex Chen / Cycle 13 | SF02 character composite pass. Repositions characters: Byte hovering LEFT (~28%), Luma CENTER (~45%), Cosmo RIGHT (~62%). Byte = VOID_BLACK body (storm variant, intentional). CORRUPT_AMBER outlines. char_h 18%. Dutch angle preserved. TERRACOTTA_CYAN_LIT=(150,172,162) applied (Jordan Reed ENV-06 fix). Output: `LTG_COLOR_styleframe_glitch_storm_v002.png`. | Pillow |
| `LTG_TOOL_byte_cracked_eye_glyph_v001.py` | Alex Chen / Cycle 13 | Generates Byte's canonical dead-pixel cracked-eye glyph reference sheet. 7×7 grid with diagonal crack fracture, dead zone upper-right, alive zone lower-left, Hot Magenta crack line. Shows 4 scales + in-eye mockups. Required for Lee Tanaka panel A2-07. Output: `LTG_CHAR_byte_cracked_eye_glyph_v001.png`. | Pillow |
| `LTG_TOOL_byte_expression_sheet_v002.py` | Alex Chen / Cycle 15 | Byte expression sheet v002. Adds RESIGNED / RELUCTANT DISCLOSURE as 8th expression: arms very close to body (arm_dy=14, arm_x_scale=0.50), backward avoidance lean (body_tilt=+8), droopy_resigned right eye (heavy lid, downcast pupil, no suppressed smile, distinct from RELUCTANT JOY), ↓ downward-arrow pixel symbol (defeat indicator, distinct from flat-line NEUTRAL). Fills all 8 slots in 4×2 grid. Required for A2-02 (Maya Santos request). Output: `LTG_CHAR_byte_expression_sheet_v002.png`. | Pillow |
| `LTG_TOOL_bg_other_side_v001.py` | Jordan Reed / Cycle 14 | Generates the SF03 "Other Side" CRT-world environment background (1920×1080). Pure digital space: ELEC_CYAN + VOID_BLACK dominant, zero warm tones. Perspective pixel grid floor, 3-tier platform depth system (NEAR/MID/FAR), aurora bands, floating geometry, pixel trails, data streams, horizon vanishing-point glow, CRT frame vignette. Contrasts SF01 (warm room) and SF02 (contested street). Output: `LTG_ENV_other_side_bg_v001.png`. | Pillow |
| `LTG_TOOL_bg_classroom_v001.py` | Jordan Reed / Cycle 14 | Generates Millbrook Middle School classroom background (1920×1080) for Act 2 panels including A1-04. 3/4 camera from back-right. 3-tier depth: FG coat rack + desk corner / MG diagonal desk rows / BG front wall with board/teacher desk. Dual-temperature lighting: warm gold window shafts (left) vs cool fluorescent (right). Binary/math board content. Foreground depth anchor (mandatory). Scanline hint. Output: `LTG_ENV_classroom_bg_v001.png`. | Pillow |
| `LTG_TOOL_style_frame_03_other_side_v001.py` | Jordan Reed / Cycle 15 | Generates SF03 "The Other Side" full style frame with characters (1920×1080). Spec-compliant per sf03_other_side_spec.md (Alex Chen) and style_frame_03_other_side.md (Sam Kowalski). Five depth layers: void sky (ring megastructure + stars), far distance (slabs + Glitchkin dots + Corrupt Amber), mid-distance (slabs + Real World debris: wall/road/lamppost), midground (platform + circuit traces + pixel-art plants + data waterfall + sub-platforms), foreground (settled confetti). UV Purple ambient + cyan bounce + blue waterfall lighting overlays. Luma (UV-ambient modified palette, pixel-grid hoodie) + Byte (DEEP_CYAN glow, cyan left eye, magenta right eye) at small scale. No warm light. Inverted atmospheric perspective. seed=77 confetti. Output: `LTG_COLOR_styleframe_otherside_v001.png`. | Pillow |
| `LTG_TOOL_bg_other_side_v002.py` | Jordan Reed / Cycle 15 | Spec-compliant ENV background-only version of SF03 "Other Side" (no characters, no footer). Replaces Cycle 14 v001 which used pre-spec grid floor approach. Shares all color/layer logic with LTG_TOOL_style_frame_03_other_side_v001.py. Output: `LTG_ENV_other_side_bg_v002.png`. | Pillow |
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

### Misplaced Files (require relocation)

| Filename | Current Location | Should Be In | Notes |
|---|---|---|---|
| `bg_glitch_layer_encounter.py` | `output/backgrounds/environments/` | `output/tools/` | Generator script — belongs in tools/, not environments/. Rename to `LTG_TOOL_*` and register. Flagged to Alex Chen. |

---

## Registration Instructions

When a new script is created, add a row to the Script Index above with:
- **Script Name:** filename including extension (e.g. `LTG_TOOL_confetti_emitter_v001.py`)
- **Created By:** team member name
- **Purpose:** one-sentence description of what the script does
- **Dependencies:** Python packages or external tools required (e.g. `Pillow`, `ImageMagick`, `svgwrite`)

Scripts must follow the standard naming convention: `LTG_TOOL_[descriptor]_v[###].[ext]`

All scripts are stored in this directory (`/home/wipkat/team/output/tools/`) and version-controlled via standard Git.
