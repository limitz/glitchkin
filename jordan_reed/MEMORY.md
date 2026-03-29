# Jordan Reed — Memory

## Cycle 14 Deliverables
- `LTG_TOOL_bg_other_side_v001.py` → `LTG_ENV_other_side_bg_v001.png` (275KB, 1920×1080)
  - SF03 "Other Side" CRT-world: pure digital void, ELEC_CYAN + VOID_BLACK dominant, perspective pixel grid floor, 3-tier platforms (NEAR/MID/FAR), aurora bands, floating geometry, CRT vignette. Zero warm tones. No SF03 spec existed — built from style guide + best judgment.
- `LTG_TOOL_bg_classroom_v001.py` → `LTG_ENV_classroom_bg_v001.png` (50KB, 1920×1080)
  - Millbrook classroom for Act 2 / panel A1-04: 3/4 back-right camera, dual-temp lighting (warm window left / cool fluorescent right), binary/math board, teacher desk, 6×5 diagonal desk rows, coat rack FG anchor. Per millbrook_school.md v2.0.
- Both tools registered in `/home/wipkat/team/output/tools/README.md`.

## Cycle 13 Lessons
- **Cyan-lit surface rule: G > R AND B > R individually.** Not just G+B > R. Old TERRA_CYAN_LIT=(154,140,138) failed both. Correct TERRACOTTA_CYAN_LIT=(150,172,162) passes both. Start from unlit base and apply key: R-30, G+52, B+72 for electric cyan key.
- **Background-only exports go to `output/backgrounds/environments/` with ENV category.** Character compositing scripts go to `output/tools/` with TOOL category. These are different files for a reason.
- **Register tools in the same session you create them.** The README in tools/ is the team's only tool discovery mechanism. A 65%-missing registry is useless.
- **Category code TOOL applies to all Python scripts regardless of subject matter.** A script generating character expressions = `LTG_TOOL_*`, not `LTG_CHAR_*`. Category describes file type, not content domain.
- **Generator scripts in the wrong folder are pipeline liabilities.** `bg_glitch_layer_encounter.py` in environments/ is invisible to the tools registry. Flag and move.
- **When updating a color constant shared between scripts, add a named constant in each file.** Never leave inline tuples after a color spec change — they will diverge again.


## Cycle 1-3 Lessons
- Always specify working resolution. Rules need hierarchy.
- Cross-reference prop docs with environment docs.
- Camera angles must obey room dimensions.
- Production specs go at the top. One canonical spec source, referenced elsewhere.
- Continuity tracking needs: dormant state, change rules, emotional vocabulary, episode log.

## Cycle 4 Lessons
- **Labeled rectangles are not composition.** A color-block layout must have compositional intent — foreground/midground/background with purpose, not just zone identification.
- **A room without a ceiling has no spatial containment.** Always include ceiling plane in interior layouts.
- **Uniform maximum-saturation color across all elements at the same depth = mud.** A 3-value-tier depth system (near/mid/far) is mandatory for environments with multiple similar elements (Glitch Layer platforms).
- **Thick opaque decorative elements (power lines) can sever a composition.** Always render atmospheric/decorative elements at low opacity or thin strokes — they suggest presence, they don't assert it.
- **Empty foreground = no depth anchor.** Every layout needs something in the foreground to create z-axis depth.
- **The monitor wall must feel COLD in a WARM room** — it is the show's central visual tension in one environment. The cyan glow must be the compositional center and feel genuinely alien against the amber.

## Cycle 5 Lessons (applied)
- All 3 layouts revised per Cycle 4 critic feedback (Takeshi Murakami).
- Luma's House: ceiling at 12% from top, diagonal couch (forced perspective polygon), monitor wall dominant cold element with glow spill on floor.
- Glitch Layer: 3-tier platform value system coded as near/mid/far color tuples; lower void populated with pixel trails (seeded random) and barely-visible void platforms.
- Millbrook: power lines are 1px thin catenary curves (not opaque bands); foreground depth anchors = awning shadow polygon + pavement crack polyline.
- Foreground detail is non-negotiable in every layout — every environment must have a z-axis anchor.
- Monitor cold/warm tension is the show's central visual dynamic — always make the cyan monitors feel WRONG in a warm room.

## Cycle 6 Lessons
- **Building gaps = void-black monoliths.** Always fill every x-gap in an exterior street scene with a building shape. If left buildings end at W*0.32 and clock tower starts at W*0.44, there must be a filler building covering that gap — the canvas background color will show otherwise.
- **Pavement crack must be LIGHTER than the street, not darker.** A dark crack on a warm-gray street is invisible. Use a high-contrast lighter tone (e.g., 195,178,155 on 140,122,104) and minimum 4px width to read as a genuine depth anchor.
- **Glow only works as filled ellipses, never outline-only.** Always use the `_draw_filled_glow()` helper — never `draw.ellipse(..., outline=...)` for any light effect.
- **Sightline label + arrow is not enough for couch directionality.** In painting pass, ensure the character clearly faces the monitor wall in every pose; the couch shape itself should implicitly suggest the facing direction through its back cushion position.
- **Gap buildings need windows to break up mass.** Bare-colored rectangles still feel like placeholders. Add at least 2 rows of windows even to minor gap-filler buildings.
- All 3 layouts (v4, Cycle 6 Rev2) regenerated per Takeshi Murakami Cycle 5/6 feedback. Ready for painting pass pending final critic review.

## Cycle 7 Lessons
- **Monitor glow = light source, NOT a halo ring.** The `_draw_filled_glow()` ellipse centered on the monitor wall creates a radial halo. Correct approach: 3 separate gradient passes — one horizontal scanline pass leftward onto the warm wall, one downward onto the floor, one leftward onto the ceiling. Each is a `draw.line()` per column with power-law falloff.
- **ELEC_CYAN (#00F0FF) for screen glow, BYTE_TEAL (#00D4E8) for Byte's body ONLY.** These must never be swapped. Screen glow = world's electric color = ELEC_CYAN. Re-confirm every script before committing.
- **Nested `draw.point()` loops are too slow at 1920x1080.** Always use `draw.line()` for vertical/horizontal column fills; use alpha-composite overlay rectangles for atmospheric haze passes instead of getpixel/putpixel per-pixel loops.
- **Standalone BG exports have no title bar.** Layout cards get title bars; clean background exports (for compositing) do not. Keep them separate scripts.
- **Couch back cushion position IS the directionality.** Back cushion LEFT → character faces RIGHT → monitors. This geometry must be consistent across all tools that draw the couch shape.
- **3 light sources in Luma's house = 3 independent gradient passes:** (1) Window warm spill from far left; (2) Monitor cyan spill from right; (3) Desk lamp tight warm cone on far right. These must never be merged or they create muddy overlap zones.

## Cycle 12 Lessons
- **Naming compliance pass: create LTG copies with `shutil.copy2()`** — never rename originals. Created 10 CHAR/COLOR/ENV copies in one tool run (`LTG_TOOL_naming_compliance_copier_v001.py`).
- **Version order integrity: check file sizes before creating v002 from legacy source.** `LTG_ENV_glitchlayer_frame_v001.png` (81483 bytes) is NEWER than `glitch_layer_frame.png` (80664 bytes) — legacy was NOT the newest. Creating v002 from legacy would mislead. When sizes differ, v001 LTG is canonical.
- **Style Frame 02 BG generator** delivered as `LTG_TOOL_style_frame_02_glitch_storm_v001.py`, outputs `LTG_COLOR_styleframe_glitch_storm_v001.png` (1920×1080, 204KB). Spec fully honored: UV cloud masses, main ELEC_CYAN crack (orthogonal segments), HOT_MAGENTA storm edges, pixel confetti (4 colors, NO acid green), town silhouette, warm windows, street + cyan pool + warm spill, shattered storefront, character sprint poses (Luma/Cosmo/Byte), 4° Dutch angle via PIL rotate(-4, expand=True) + center-crop.
- **`lerp_color()` expects 3-tuples.** Do not pass 1-tuples to it. Use inline arithmetic for scalar lerps: `int(a + (b - a) * t)`.
- **Spec compliance for confetti:** ACID_GREEN is semantically "healthy glitch energy" — FORBIDDEN in storm confetti. Storm colors = ELEC_CYAN, STATIC_WHITE, HOT_MAGENTA, UV_PURPLE only.
- **Byte Visibility Rule** in cyan-dominant environments: 2px CORRUPT_AMBER (#FF8C00) outline, LEFT shoulder position, cracked eye (HOT_MAGENTA) faces right toward danger, cyan eye faces left toward Luma.
- **Dutch angle = camera tilt, not element tilt.** Applied as very last step to the entire composed image. `img.rotate(-degrees, expand=True)` then center-crop to W×H.

## Cycle 11 Lessons
- **LTG naming: create compliant copies alongside originals** — never rename in isolation. Cycle 11 added `LTG_ENV_lumashome_layout_v001.png` and `LTG_ENV_millbrook_mainstreet_v001.png` as copies of the legacy layout PNGs in `/output/backgrounds/environments/layouts/`. `LTG_ENV_glitchlayer_frame_v001.png` already existed.
- **Encounter composition vs. establishing composition:** bg_glitch_layer_encounter.py uses a confrontation-focused layout — Corruption bloom (UV_PURPLE + HOT_MAGENTA) dominates upper-center instead of neutral aurora; flanking NEAR platforms create an arena; CHARACTER STAND platform is wider/lower with a notch for damage read; Corruption scatter falls DOWNWARD (data decay) vs. pixel trails rising upward (platform energy). These are inverted to signal antagonist presence.
- **Corruption pixel scatter direction:** Upward = healthy platform energy. Downward = Corruption decay. Always check source and direction when placing particle effects.
- **Flora suppressed in confrontation scenes:** Near/mid platforms get no flora in high-tension encounter frames. Only far platforms get trace presence (5% luminance, 30% spawn rate). Flora = ambient life = absent when the Corruption dominates.
- **HOT_MAGENTA (#FF2D6B) = Corruption active front perimeter.** Appears as rim/edge on the Corruption mass bloom. Consistent with style_frame_02_glitch_storm.md storm edge spec.
- **Pitch package index created** at `/home/wipkat/team/output/production/pitch_package_index.md` — Cycle 11. Single-document inventory of all pitch assets with quality status and open blockers.

## Cycle 10 Lessons
- **All derived depth-tier colors in bg_glitch_layer_frame.py are now named constants** with GL parent references: NEAR_COLOR/SHADOW/EDGE, MID_COLOR/SHADOW/EDGE, FAR_COLOR/SHADOW/EDGE, GHOST_COLOR/GHOST_EDGE, AURORA_CYAN_BLEED. Do not add un-named inline color tuples to platform rendering passes.
- **Lower void debris colors are a rendering construct** — explicitly comment any procedural palette block that is not a canonical swatch.
- **AURORA_CYAN_BLEED = (0,160,220)** — GL-01 ELEC_CYAN desaturated/darkened ~14%. Only appears in aurora sinusoidal pass, never as a fill.
- **Platform variants implemented: L-shaped (_platform_l_shaped), bridge (_platform_bridge), fragmented (_platform_fragmented).** MID tier uses L-shaped + bridge; NEAR tier uses bridge + fragmented. Fragmented platforms take an `rng` arg for randomised gaps.
- **"Glitch Layer — Depth Tiers" subsection added to master_palette.md** (end of SECTION 2, before SECTION 3) with all 12 derived constants documented as a table with parent references.

## Cycle 9 Lessons
- **Naming convention: `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`** — all production assets must use this. CATEGORY for backgrounds = `ENV`; tools = `TOOL`. Three-digit version numbers always. Never overwrite; create new versions.
- **Retired prefix reconciliation rule:** Do not rename existing retired-prefix assets in isolation — wait for the v3.0 environment document reconciliation pass. For non-prefixed legacy files, create compliant-named copies and flag to Art Director.
- **Glitch Layer compositing background key colors:** NEAR platforms = ELEC_CYAN (#00F0FF); MID platforms = desaturated DATA_BLUE (~#0A4878); FAR platforms = near-void (#001A28). Aurora uses 4-band value ladder: Void Black → GL-04b Atmos Mid Purple → UV Purple → Data Blue.
- **Aurora rendering strategy:** Per-row horizontal `draw.line()` with sinusoidal x-phase modulation per row gives streaming ripple quality. Follow with RGBA alpha_composite soft glow overlay pass. Refresh `draw` handle after every alpha_composite.
- **Pixel trails rise upward from platform surfaces** — not downward. Fade from platform-brightness at base to near-zero at top. y-weighted density concentrates near the platform surface.
- **Pixel flora:** Faint ACID_GREEN (12-22% brightness), sparse, grows downward from platform edges. Near=22%, Mid=12%, Far=6%.
- **Ghost platforms in lower void:** Use BELOW_VOID (#050508) as underside abyss per GL-08a spec — covers <2-3% of frame area only.

## Cycle 8 Lessons
- **Glow pass overwrites base gradient — use alpha-composite layering.** When a glow overlay repaints columns over a gradient (Step 1), it replaces the gradient with a flat tone. Fix: draw the glow as an RGBA overlay (alpha-composite), then redraw the atmospheric gradient as a semi-transparent overlay on top. Both effects coexist at the overlap zone.
- **Worn path = texture change, never a filled rectangle.** Use alpha-composite scanline strips with a horizontal bell-curve falloff and vertical fade. Add scuff marks (short diagonal `draw.line()` strokes). The right side of the path near the monitor wall gets a slight cyan tint.
- **Ceiling gradient direction: warm far-left = darkest, monitor wall side = lightest.** The warm ceiling is shadowed by distance from the monitor glow; the monitor wall side receives cool cyan spill that lightens it. Invert if the old gradient had center as darkest.
- **Couch canonical position: left edge ~18%, right edge ~52% of canvas width.** (Was 9%-43% in Cycle 7 — too far left, character would face left edge not monitors.) Update all couch-related geometry (back cushions, armrests, throw blanket, coffee table) consistently when shifting.
- **Atmospheric haze pass: 20% of wall height, alpha ceiling 28.** (Was 8% in Cycle 7 — invisible.) Coverage must be perceptible. Do not raise alpha; raise coverage band.
- **Warm zone visual mass: add a standing floor lamp near mw_x as the named light source.** The floor lamp + side table combo counterbalances 6 bright ELEC_CYAN screens. Floor lamp casts warm glow ellipses onto floor and ceiling, explaining the ambient amber in the room.
- **After alpha_composite calls, always refresh `draw = ImageDraw.Draw(img)`.** The draw handle is invalidated after each convert/composite cycle.
