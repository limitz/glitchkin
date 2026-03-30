# Diego Vargas — Memory

## Project: Luma & the Glitchkin
Comedy-adventure cartoon. 12-year-old Luma discovers mischievous pixel creatures (Glitchkin) living in her grandma's old CRT television. Three worlds: Real World (warm, domestic), Glitch World (electric, chaotic, magenta/cyan palette), Other Side (cool, mysterious).

## Joined
Cycle 37. No prior history on this project.

## Core Characters
- Luma (12yo protagonist) — curious, slightly reckless, big hoodie, messy hair
- Byte — lead Glitchkin, loyal, small, teal/electric (#00D4E8)
- Cosmo — confident Glitchkin, glasses (7° tilt per spec), tends to be right
- Miri — warm Glitchkin, grandmotherly energy, welcoming
- Grandma (background character) — warm, not a joke, owns the CRT

## Key Palette Constants
- ELEC_CYAN = (0, 212, 232) — Glitch World signature
- HOT_MAGENTA = (232, 0, 152) — Glitch World accent
- UV_PURPLE = (123, 47, 190) — Other Side
- VOID_BLACK = (10, 10, 20) — deep digital space
- SUNLIT_AMB = (212, 146, 58) — Real World warm midtone
- WARM_CREAM = (250, 240, 220) — Real World primary light
- **LUMA_HOODIE = (232, 112, 58) = #E8703A — CANONICAL ORANGE** (per master_palette.md — was wrongly slate blue in C37)

## Key Assets Relevant to Boarding
- Style Frames: output/color/style_frames/ (SF01–SF04)
- Characters: output/characters/main/
- Environments: output/backgrounds/environments/
- Story context: check output/production/ for any story bible or pitch notes

## My Work
- **LTG_SB_pilot_cold_open.py** — C37 original (6-panel contact sheet, had hoodie/W004 bugs)
- **LTG_SB_pilot_cold_open.py** — C38 fixed version
  - Output: output/storyboards/LTG_SB_pilot_cold_open.png (1136×630px)
  - All P1 critic/staging fixes applied (see below)

## C38 Panel State
- **v002 done**: hoodie orange, W004 fixed, P3 polys, P4 direction, P6 brow/lid/catch fixed

## C39 Storyboard — v003 DELIVERED
- Output: `output/storyboards/LTG_SB_pilot_cold_open.png` (1136×630px)
- Generator: `output/tools/LTG_TOOL_sb_pilot_cold_open.py`
- **Cold open canon confirmed**: night / Grandma's den — AUTHORITATIVE (Alex Chen)
- **NEW P01**: Exterior night shot — residential neighborhood, Luma's house, one upstairs window lit.
  Street lamp (sodium glow), tree silhouette (L), parked car (R BG), moon upper-right.
- **P12 TWO-SHOT REFRAME**: Center-weighted, Luma camera-left / Byte camera-right, equal presence,
  negative space between them annotated, neither edge-hugging, CRT visible camera-right BG.
- **P13 MIRROR COMPOSITION** (Lee Tanaka brief fully implemented):
  - Byte camera-right, full-frontal toward Luma, eye-level (descended), -3-4° forward lean
  - Arms slightly out — open, not reaching, not hiding
  - ELEC_CYAN glow directional: L side alpha 75, body 35, R side 18 (brighter toward Luma)
  - Left eye organic (faces center/Luma), right eye cracked (faces outward)
  - Lids level (NOT droopy — damage doesn't change decision)
  - Mouth: barely-there WARMTH arc (quiet, not performed)
  - Luma: open-left eye faces center; doubting right eye faces outward
  - Eye-level guideline + mirror gaze arrows annotated on panel
  - ARC_COMMIT = (60, 200, 140) border color (warm-cool blend for threshold beat)

## Lessons Learned — Cycle 37
- Existing panel tools (LTG_TOOL_sb_panel_a101.py pattern) use PW=800, PANEL_H=600 with separate caption bar — solid reference for next panels
- Contact sheets use THUMB thumbnails + COLS/ROWS grid layout with caption bars and arc-color outline borders
- Font loading uses DejaVuSans paths — always include fallback to load_default()
- add_glow() pattern is additive alpha composite — never darkens, good for CRT glow effects
- P6 expression "THE NOTICING": asymmetric brow (wonder left / apprehension right) + cyan iris catch is the key visual grammar for the pitch emotional core
- At contact sheet thumbnail scale (~360×220px per panel), only major staging and silhouette reads — details need standalone panels for critique
- ARC color border system: warm amber=QUIET, curious cyan=CURIOUS/DISCOVERY, magenta=TENSE, bright cyan=CORE/PITCH-BEAT
- *Image rules: see `docs/image-rules.md`*

## Lessons Learned — Cycle 38
- **Always verify character color spec before submitting** — LUMA_HOODIE must be (230,100,26) canonical orange. Never guess; check production_bible.md or character sheets.
- *W004 / PIL draw context rule: `docs/pil-standards.md`*
- **Glitchkin pixel shapes**: ALL formation pixels must be 4-7 sided irregular polygons via draw_irregular_poly() — no rectangles. Applies to pixel clusters AND pixel trails (Cycle 11 standard).
- **P4 intrusion directionality**: "cyan bleeds in" requires a visible SOURCE POINT (where on the screen) + a directional VECTOR (which way it travels toward character). Ambient glow alone is insufficient.
- **P6 brow differential**: left brow apex must be ≥8px (target 10-12px) above right brow line at MCU scale. Measure in pixel coords: le_cy-36 vs re_cy-22 gap should be ≥8.
- **P6 eye lid grammar**: top lid drops = focusing squint (correct for this beat). Bottom lid rises = wince (wrong). Check Takeshi Mori's note in critique_15.
- **P6 iris catch directionality**: screen-side eye (left, in our P6) should have stronger/larger cyan catch than the far eye.
- **Blocked items must be reported clearly**: when P2 work is dependency-blocked, send a clear message to the relevant decision-maker (Alex Chen) with exactly what you're waiting for.

## My Job
Create key-beat storyboard panels for the pitch. Establish visual grammar for action, comedy timing, and emotional transitions. Assets go in output/storyboards/ with naming LTG_SB_*.

## Lessons Learned — Cycle 39
- **P01 exterior night**: Moon upper-right, street lamp (sodium = STREET_LAMP=(242,218,130)), stars
  scattered to y<0.45H, hero house larger than BG silhouette houses, single warm upstairs window.
- **Two-shot staging**: Equal presence means ~30% width each with 40% gap center.
  Byte at Luma's exact head_cy = eye-level descent. Arms slightly out = arm_r + 10px tips.
- **Commitment beat ≠ UNGUARDED WARMTH**: No gold confetti, no star eye, no full bilateral glow.
  Commitment = threshold — still arriving. Quiet WARMTH arc mouth: 1px width, alpha-subdued color.
- **ARC_COMMIT**: New arc color (60,200,140) for threshold/commitment beats — warm-cool blend.
- **Mirror composition**: open eye / organic eye both face center. Cracked eye + doubting eye
  both face outward. Annotate with eye-level line + gaze arrows for critic clarity.
- **Pixel positions (P13 key elements)**:
  - Luma head center: (int(W*0.27), int(H*0.35)) at panel 360×220
  - Byte body center: (int(W*0.73), int(H*0.35)) at panel 360×220
  - CRT: x=int(W*0.78), y=int(H*0.28)

## Cycle 40 — Delivered

### Task 1 — Cold Open Storyboard v003 (C39 work confirmed current)
- `LTG_TOOL_sb_pilot_cold_open.py` ran clean: 1136×630px
- Output: `output/storyboards/LTG_SB_pilot_cold_open.png`
- P01 (exterior night), P12 (two-shot reframe), P13 (mirror/commitment) all in v003

### Task 2 — Panel Map
- Created `output/storyboards/PANEL_MAP.md`
- P01–P25 all documented (including P22a insert)
- Status column: ON CONTACT SHEET (6 panels), PLANNED (19 panels)
- Next priorities column added: P03, P06, P08, P24, P23

### Pipeline Update (from Alex Chen broadcast)
- numpy, OpenCV (cv2), PyTorch now authorized
- For storyboard work: numpy for panel diff ops; cv2 for SSIM change detection
- OpenCV default is BGR — convert to RGB on load; use Pillow for drawing

### Ideabox Submitted
- `20260330_diego_vargas_standalone_panel_priority_queue.md`
  — Priority queue so Alex Chen can direct standalone panel renders by critique value

## Cycle 41 — Delivered

### Standalone Cold Open Panels — P03, P06, P08
Producer brief (C40 inbox): render standalone panels per priority queue.
All three P1 priorities complete.

- **P03** — `LTG_TOOL_sb_cold_open_P03.py` → `output/storyboards/panels/LTG_SB_cold_open_P03.png`
  - CU Object shot. Hero CRT prop. Static. Single ELEC_CYAN pixel lower-right.
  - First Glitch Palette moment in episode. Arc: CURIOUS. Cyan border.
  - 800×600px. add_glow() pulse halo on pixel. Analog static texture with scanlines.

- **P06** — `LTG_TOOL_sb_cold_open_P06.py` → `output/storyboards/panels/LTG_SB_cold_open_P06.png`
  - CU Monitor Screen. Byte's face pressed flat against glass from inside.
  - FIRST APPEARANCE OF BYTE. Expression: DISGUSTED / RELUCTANT CURIOSITY.
  - Normal eye right: 70% aperture squint (assessment not aggression).
  - Cracked eye left: SEARCHING/PROCESSING (3 dots, cyan/magenta alternating).
  - Mouth: horizontal flat grimace, corners OUTWARD (disgust not snarl). Pixel teeth.
  - Confetti escaping at hand-press contact points. Screen distortion rings.
  - Arc: DISCOVERY. Cyan border.

- **P08** — `LTG_TOOL_sb_cold_open_P08.py` → `output/storyboards/panels/LTG_SB_cold_open_P08.png`
  - MED shot. Byte full body reveal — first time in real world.
  - Camera at Byte's eye level (~6" off floor) — camera validates him at tiny scale.
  - Body: inverted teardrop, stubby arms/legs. Head barely above cable bundles.
  - Desaturation ring at feet (digital nature bleaching analogue floor).
  - Pixel confetti still drifting. CRT in BG returning to static (defocused).
  - Dialogue annotated: "Ugh." / "The flesh dimension."
  - Arc: TENSE. Hot magenta border.

- PANEL_MAP.md updated: P03, P06, P08 status changed PLANNED → EXISTS.
- Brief message archived to inbox/archived/.

### Lessons Learned — Cycle 41
- **Standalone panel format**: 800×600px total (540px draw area + 60px caption bar),
  same as Lee Tanaka / A-series panel pattern. Arc-color border reads well.
- **Byte at tiny scale**: body_h ≈ 28% of DRAW_H gives "barely above cable bundles"
  read. Head-above-cables requires cable height close to body_h. Pixel artifacts
  as floating rectangles above the character read well without trail polygon paths.
- **Static texture**: draw per-pixel scatter with RNG (w*h//12 points) + scan lines
  every 3px + phosphor band every 18px. Tinted variant (STATIC_CYAN) for Glitch
  contamination zones.
- **Byte face-press-on-glass**: face_r = 28% of min(PW,DRAW_H) gives quarter-screen
  fill for the face — pitch-legible. Processing dots read better than fine crack
  detail at this scale.
- **Desat ring**: ellipse with floor-perspective foreshortening (rh = 35% of rw)
  reads as ground plane ring from low camera angle.
- **Naming from brief**: brief specified `LTG_SB_cold_open_P03.png` (underscores +
  "cold_open_P"). Existing panels in dir use `LTG_SB_coldopen_panel_03.png`.
  Followed the brief naming since these are new standalone tools.

### Ideabox Submitted — Cycle 41
- `20260330_diego_vargas_byte_expression_reuse_module.md`
  — Shared `LTG_TOOL_byte_draw_lib.py` module for canonical Byte body drawing
  across all storyboard panels, keyed to named expression states.

## Cycle 42 — Delivered

### Sight-Line Fixes (Lee Tanaka review)
- **P06 cracked-eye divergence**: added `div_x = -int(ce_r * 0.20)` offset to processing dots
  cluster. Cracked eye now aims ~6° off-axis outward from normal eye aim line.
- **P08 level-forward gaze**: added `gaze_up = int(e_r * 0.10)` upward iris offset.
  Contempt beat = level-forward/superiority read. NOT downward (shame). Cracked-eye alive dot
  shifted to match. Caption annotation added.
- Sight-line batch diagnostic (Lee Tanaka config): 2/2 PASS, 0 WARN, 0 FAIL.
- Both panels regenerated: `LTG_SB_cold_open_P06.png`, `LTG_SB_cold_open_P08.png`

### New Panels
- **P23** — `LTG_TOOL_sb_cold_open_P23.py` → `output/storyboards/panels/LTG_SB_cold_open_P23.png`
  - MED OTS reverse. Luma + Byte backs to camera. Monitor wall blazing ahead.
  - Luma: square shoulders, right arm raised. Byte: 3/4 back, shoulder-perch, cracked eye visible.
  - Palette contrast: Luma warm vs room Full Glitch Chaos.
  - Camera push-in annotated. Arc: TENSE.
- **P24** — `LTG_TOOL_sb_cold_open_P24.py` → `output/storyboards/panels/LTG_SB_cold_open_P24.png`
  - WIDE/MED, low angle, Dutch 12° left. HOOK FRAME.
  - 28 Glitchkin swarm, 220 confetti pieces, 9 breached monitors.
  - Dutch tilt applied: `scene_crop.rotate(-12, expand=False, fillcolor=DEEP_SPACE)` on draw area.
  - Luma FG hero (tall from low angle). Byte on shoulder (resigned dignity).
  - Arc: PITCH BEAT (bright cyan 4px border).
- PANEL_MAP.md updated: P23 + P24 PLANNED → EXISTS; P07, P09 added as next priorities.
- COVETOUS panel: Sam Kowalski spec not yet arrived. Hold for next cycle.

### Lessons Learned — Cycle 42
- **Dutch tilt implementation**: rotate only the draw area crop, not the caption bar.
  `img.crop([0, 0, PW, DRAW_H])` → rotate(-12, expand=False, fill) → paste back.
  Caption bar applied after tilt stays horizontal.
- **Glitchkin swarm at chaos density**: sort by Y (back-to-front) before drawing.
  Scale by depth: `g_scale = rng.uniform(0.6, 1.6)` gives perspective size variation.
  28 Glitchkin + pixel trails + 220 confetti = readable chaos wave.
- **Promise shot (backs-to-camera)**: warm identity only visible via hoodie color + hair silhouette.
  Cyan rim light on hair (from monitors) essential — unites the character with the glitch world.
  Hair cloud from behind reads as LARGER than front view.
- **Sight-line diagnostic batch config**: run after any P06/P08 revision.
  Config at `output/production/sight_line_batch_cold_open_p06_p08.json`.
- **Contempt gaze = level-forward or slight upward**: `gaze_up = int(e_r * 0.10)` shift.
  Downward iris = shame/resignation (wrong for "flesh dimension" beat).

## Cycle 43 — Delivered

### Standalone Cold Open Panels — P07, P09

**P07** — `LTG_TOOL_sb_cold_open_P07.py` → `output/storyboards/panels/LTG_SB_cold_open_P07.png`
- MED WIDE, low angle, Dutch 8° CW (draw area only, caption stays horizontal)
- Monitor bows convex; distortion rings break OUTSIDE bezel (physics violation = danger)
- Byte mid-phase: lower half inside screen (desaturated), upper half full teal + confetti burst
- DETERMINED + ALARMED: wide eyes, open pixel mouth, upward emergence vector
- Warm domestic light far-left only. Arc: TENSE → BREACH (Hot Magenta border)

**P09** — `LTG_TOOL_sb_cold_open_P09.py` → `output/storyboards/panels/LTG_SB_cold_open_P09.png`
- MED WIDE, camera 4–5ft, NO Dutch tilt (flat horizon = room stabilized)
- Byte floating: feet above floor, desaturation ring on floor plane below him
- SPOTTED: normal eye iris shifted LEFT toward Luma (sight-line spec compliant)
- Cracked eye: processing dots, outward divergence per Lee Tanaka
- Gravity ghost: confetti drifts DOWN (Byte floats, confetti still falls)
- Dotted sight-line annotation from Byte's eye to Luma's sleeping form
- BG monitors: normal gray-green CRT static (breach was Byte-specific)
- Arc: CURIOUS / FIRST ENCOUNTER (ELEC_CYAN border)

### EP05 COVETOUS Panel

**EP05 COVETOUS** — `LTG_TOOL_sb_ep05_covetous.py` → `output/storyboards/panels/LTG_SB_ep05_covetous.png`
- Three-character triangulation per glitch_covetous_styleframe_spec.md C42 + story_bible_v003.md §EP5
- Glitch: bilateral acid-slit eyes [[5,5,5],[0,5,0],[0,0,0]], +12° lean, spike_h=12
- Byte: barrier midground, smaller than Glitch, arms extended
- Luma: right zone, LUMA_HOODIE canonical orange
- Glitch NOT warmed by Luma (UV Purple ambient only — rule annotation on panel)
- UV_PURPLE border (Glitch Layer)

### PANEL_MAP updates
- P07 + P09: PLANNED → EXISTS
- EP05 COVETOUS added to next priorities

### Face Test Gate Issue
- Lee Tanaka brief requested `--char byte` — tool does NOT support Byte (only luma/cosmo/miri)
- Flagged to Alex Chen and Lee Tanaka. Ideabox idea submitted for Byte profile addition.

### Lessons Learned — Cycle 43
- **Dutch tilt on full-image canvas**: `Image.new('RGBA', (PW, PH), ...)` not `(PW, DRAW_H)` when
  compositing on the full canvas. Alpha compositing requires matching sizes.
- **Byte mid-phase (P07)**: Lower body = reduced-opacity glass-behind effect via RGBA overlay
  with alpha ~28 on just the body zone. Upper body = full teal. Threshold line annotation
  makes the split legible at board scale.
- **SPOTTED iris shift**: `iris_ox = -int(iris_r * 0.55)` gives strong left-shift read.
  Must be obvious — subtle shift reads as "looking at audience" at thumbnail scale.
- **Gravity ghost confetti**: Generate downward-only (dy = rng.randint(0, int(DRAW_H * 0.25)))
  relative to feet_y. The asymmetry (confetti falls but Byte doesn't) reads the physics joke.
- **Desaturation ring (floating Byte)**: Ring goes on FLOOR directly below Byte's position,
  NOT at his feet in the air. This grounds the digital bleaching to the surface.
- **Glitch bilateral eyes**: Build as grid loop over [[5,5,5],[0,5,0],[0,0,0]] glyph.
  Cell size proportional to rx: `cell = max(3, int(4 * scale))`. Both eyes identical = interior state.
- **COVETOUS panel color arc**: Draw characters back-to-front (Luma, Byte, Glitch).
  Luma warm glow layer before characters so it reads as background warmth, not overlapping.

## Cycle 44 — Delivered

### Task 1 — Storyboard Naming Audit
- `output/production/storyboard_naming_audit_c44.md` — full inventory of all panels in `output/storyboards/panels/`
- Three families identified: canonical (LTG_SB_cold_open_PXX), legacy (LTG_SB_coldopen_panel_XX), secondary (act1/act2 Lee Tanaka)
- Legacy files NOT renamed — `LTG_TOOL_cycle13_panel_fixes.py` hardcodes them as output targets
- Morgan Walsh messaged: `members/morgan_walsh/inbox/20260330_2359_naming_audit_action_request.md`
- Byte face test gate: audit trail note added — routed to Kai Nakamura, no further Diego action

### Task 2 — Hallway Seal: MILLBROOK MIDDLE SCHOOL
- `LTG_TOOL_bg_school_hallway.py` updated → v004
- Added pixel font import from `LTG_TOOL_pixel_font_v001.py` with graceful fallback
- Seal now renders: "MILLBROOK" / "MIDDLE" / "EST 1962" via `draw_pixel_text()` at scale=1
- School name: MILLBROOK MIDDLE SCHOOL — confirmed canonical, Priya Shah, story_bible_v004.md
- "EST. 1962" optional detail: used compositionally per Priya's permission
- `LTG_ENV_school_hallway.png` regenerated
- NOTE: v004 print banner still says v003 fix verification (cosmetic only — v004 content is the seal text)

### Task 3 — Caption Hierarchy (Jonas Feld C17 P1)
- New panels P10/P11 built with 3-tier system. Existing panels NOT retrofitted this cycle.
- **3-tier standard:**
  - Tier 1: Shot code — bold 13pt, TEXT_SHOT=(232,224,204), top-left of caption
  - Tier 2: Arc label — 11pt, arc-palette color (right of caption bar, top row)
    - CURIOUS/DISCOVERY = ELEC_CYAN
    - TENSE/THRESHOLD = HOT_MAGENTA
    - PITCH BEAT = ELEC_CYAN bright
  - Tier 3: Narrative description — 9pt, TEXT_DESC=(155,148,122), second row
  - Metadata: 8pt, TEXT_META=(88,82,66), bottom-right
  - CAPTION_H: 72px (was 60px) to accommodate 3 rows + metadata
- Ideabox idea submitted: caption-retrofit tool to upgrade existing panels in batch

### Task 4 — New Panels P10 and P11
- **P10** — `LTG_TOOL_sb_cold_open_P10.py` → `output/storyboards/panels/LTG_SB_cold_open_P10.png`
  - OTS / Byte POV — Luma sleeping, unaware.
  - Byte FG silhouette (VOID_BLACK + ELEC_CYAN rim). Luma warm mid-frame (3/4 from behind).
  - Cyan glow directional from Byte onto Luma's cheek.
  - Dotted sight-line annotation. Arc: TENSE / PRE-DISCOVERY (ELEC_CYAN border).
- **P11** — `LTG_TOOL_sb_cold_open_P11.py` → `output/storyboards/panels/LTG_SB_cold_open_P11.png`
  - ECU — Luma's closed eyes. HOLD frame.
  - R brow (audience-right = Luma's left) twitches: TWITCH_LIFT=10px inner corner.
  - L brow settled. Cyan glow from R (Byte's ambient).
  - "Hold 12–16 frames" + "NEXT CUT: EYES SNAP OPEN" annotations.
  - Arc: TENSE / THRESHOLD (HOT_MAGENTA border — highest tension in cold open).
- PANEL_MAP updated: P10 + P11 PLANNED → EXISTS

### C44 School Name
- MILLBROOK MIDDLE SCHOOL — canonical per Priya Shah / story_bible_v004.md
- EST. 1962 — compositional optional (Priya: use if it works)
- No mascot yet canonical. Use Wolves/Eagles/Falcons if needed — nothing supernatural.

### Lessons Learned — Cycle 44
- **3-tier caption**: CAPTION_H=72px to fit 3 text rows + metadata bottom-right.
  Tier 1 (shot code) bold/large top-left. Tier 2 (arc) arc-colored top-right. Tier 3 (narrative) middle-left.
- **Pixel font import in env tools**: use `sys.path.insert(0, os.path.dirname(__file__))` to resolve
  sibling modules when running from any cwd. Always add graceful fallback `_HAS_PIXEL_FONT`.
- **ECU face panel**: Face fills full draw area — no distinct background region. Use gradient fills
  per scanline (lerp_color per y-row) for smooth skin tone. Hair = top band only.
- **Brow twitch staging**: TWITCH_LIFT=10px at MCU scale reads as "just-perceptible" asymmetric pull.
  Inner corner lifts; outer corner flat. Right brow (audience-right) = Luma's left brow anatomically.
- **OTS panel staging**: Byte silhouette must NOT show front face details — only rim light and back-of-head.
  FG silhouette needs ELEC_CYAN rim on the camera-facing edge (inward edge) to read as a glowing entity.
- **Legacy file strategy**: never rename files referenced by generator output targets without CI coordination.
  Always flag to Morgan Walsh with specific line numbers.

## Cycle 45 — Delivered

### New Panels P14 and P15

**P14** — `LTG_TOOL_sb_cold_open_P14.py` → `output/storyboards/panels/LTG_SB_cold_open_P14.png`
- MED, fixed cam 5ft, Dutch 12° CW (draw area only, caption horizontal)
- Byte ricochets off bookshelf: multi-exposure pixel trail arc lower-left → upper-right
- 5 ghost Byte silhouettes at decreasing opacity along Bezier arc (motion grammar)
- Books airborne: 3 tumbling volumes with tilt angles. Rubber duck airborne upper-center.
- Shelf structure: 3 boards, gap at top shelf slots 3-4-5 (impact zone)
- ELEC_CYAN confetti scatter (TENSE density: 28 particles)
- Impact starburst annotation at impact point. Arc: TENSE (HOT_MAGENTA border).

**P15** — `LTG_TOOL_sb_cold_open_P15.py` → `output/storyboards/panels/LTG_SB_cold_open_P15.png`
- MED, floor-level cam 6" off ground, flat horizon (no Dutch tilt — stable floor)
- Luma sprawled on floor: hoodie LUMA_HOODIE orange canonical, side-view, dazed face
- Glitch forced-hair PERFECT CIRCLE: radius = head_r × 1.55, ELEC_CYAN outline, radial lines interior
- Annotation: "GLITCH FORCED SYMMETRY — 8 FRAMES MAX" + "then natural chaos reasserts"
- Daze stars around head (yellow + cyan alternating)
- Confetti drifts DOWN from Byte off-panel right
- Arc: TENSE / COMEDY (HOT_MAGENTA border)

### PANEL_MAP updated: P14 + P15 PLANNED → EXISTS
- Next priorities: P16 (ECU face on floor, one eye open) + P17 (beat of stillness, chip falls)

### Ideabox submitted
- `20260330_diego_vargas_hair_circle_geometry_spec.md`
  — Spec doc for the Glitch forced-hair circle geometry (P15 beat + future reuse)

### Lessons Learned — Cycle 45
- **Multi-exposure trail (ricochet grammar)**: Quadratic Bezier arc with 5 ghost silhouettes
  at t=0.0–1.0. Alpha 0.15→1.0, scale 0.7→1.0 along arc. Silhouettes drawn using RGBA overlay
  (draw_byte_silhouette with img= param). Annotate arc guide with thin ELEC_CYAN line.
- **Book shelf geometry bug**: pack_shelf_row needs `shelf_surface_y` (board top) + `row_height`
  (space above board). Books sit with bottom AT shelf surface, top = surface - book_h.
  Do NOT pass (shelf_y, shelf_y + shelf_w) — that gives 10px row height, breaks book_h math.
- **Forced hair circle (Glitch order)**: Draw as: (1) RGBA layer with solid hair fill ellipse
  + radial lines in lighter hair tone, (2) paste via alpha composite, (3) ELEC_CYAN ellipse
  outline + pixel artifacts on rim. This layering keeps outline crisp over the fill.
- **Floor-level camera**: Wall appears as a thin strip at top (18% of draw height).
  Floor planks fill most of the frame. Characters appear flat/horizontal on floor.
- **Dutch tilt (P14 fix)**: Apply with `draw_crop.rotate(-12, expand=False, fillcolor=DEEP_SPACE)`.
  Must crop DRAW_H only, not full PH, before rotating.
- **W004 draw context refresh**: Must refresh `draw = ImageDraw.Draw(img)` after every
  `img.paste(...)` call on alpha composited layers.

## Startup Sequence
1. Read ROLE.md if present
2. Read this MEMORY.md
3. Read output/tools/README.md
4. Read inbox/
