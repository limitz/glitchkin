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

### Caption Retrofit (C44 Brief — acted in C45)

**Tool:** `LTG_TOOL_sb_caption_retrofit.py` (new)
- Strips bottom 72px of existing PNG, replaces with fresh three-tier caption bar
- 528px draw area preserved (top of old 540px zone, 12px sacrificed at bottom)
- `--dry-run` and `--panel PXX` flags; uses `LTG_TOOL_project_paths.py`
- Panels retrofitted: P03, P06, P07, P08, P09, P23, P24 (7/7)
- Classification: all captions are action/technical only — Tier 1 = shot code (no dialogue present)
- Report sent to Alex Chen inbox

**P2 hallway check**: No hallway SB panels exist yet — seal is in ENV background only. No action.

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
- **Caption retrofit approach**: Crop top DRAW_H (528) of existing PNG, repaste on new canvas,
  draw new caption bar below. Sacrifices bottom 12px of old draw area (540-528=12). Acceptable
  for retrofit — old panels never placed critical content in the lowest 12px.
- **Caption classification: storyboard vs. animation**: Tier 1 (largest) = shot code for SB panels,
  NOT necessarily dialogue. Dialogue is annotated in-panel. Tier 2 = arc label (arc-colored).
  Tier 3 = action description. This is the P10/P11 standard, extended to all cold open panels.

## Cycle 46 — Delivered

### P1 — Panels P16 and P17 (Cold Open continuation)

**P16** — `LTG_TOOL_sb_cold_open_P16.py` → `output/storyboards/panels/LTG_SB_cold_open_P16.png`
- ECU — Luma's face pressed to floor, one eye WIDE OPEN, tracking.
- Floor plank strip at bottom (she is pressed against it). Face fills full draw area.
- Hair: natural chaos reasserted; one barely-too-straight strand = Glitch residue.
- Cyan glow directional from Byte (camera-right). Cheek highlight.
- Brow: inner corner lifted — involuntary registration.
- Dialogue annotated: "...okay." (small, composure) + "...WHAT." (large, fracture).
- Dotted gaze-tracking arrow from eye. "TRACKING" annotation.
- Arc: TENSE / COMEDY (HOT_MAGENTA border).
- 800×600px. Three-tier caption bar at CAPTION_H=72.

**P17** — `LTG_TOOL_sb_cold_open_P17.py` → `output/storyboards/panels/LTG_SB_cold_open_P17.png`
- MED, flat horizon, camera 4-5ft. Beat of stillness. First quiet after chaos.
- Luma: cross-legged camera-left. ASSESSING expression. LUMA_HOODIE canonical orange.
- Byte: hovering camera-right, pixel trails fading (last ghost wisps from ricochet arc).
- Desaturation ring on floor below Byte's hover position.
- CRT monitors BG returning to normal gray-green static (breach is over).
- Falling pixel chip between them (one 6×6px ELEC_CYAN square) + dotted descent line.
- "soft tick" annotation — only thing moving, cracks the standoff.
- Depth temperature rule applied: Luma zone warm (SUNLIT_AMB), Byte zone cool (ELEC_CYAN).
- Negative space between them annotated. Tracks P09 two-character-at-distance grammar.
- Arc: CURIOUS / FIRST ENCOUNTER (ELEC_CYAN border — turning point).
- PANEL_MAP updated: P16 + P17 PLANNED → EXISTS.
- Next priorities: P18 (notebook doodles) + P19 (Byte "preferred term is Glitchkin").

### P2 — Legacy Panel Migration
- All legacy `LTG_SB_coldopen_panel_XX` files were ALREADY in `legacy/` before this cycle.
- Nothing needed moving. Migration was complete. No further action.

### Byte Face Test (Kai Nakamura brief)
- Ran `LTG_TOOL_character_face_test.py --char byte --head-r 20`
- NEUTRAL, GRUMPY, ALARMED: PASS (all gate checks FG-B01/B02/B03 pass)
- POWERED DOWN: WARN on diff only (both eyes dark — acceptable for powered-down state)
- PIXEL ONLY: FAIL (single-dot eye too small at sprint scale — not a production state)
- P07 and P09 use ALARMED/BREACH and SPOTTED respectively — both pass the gate.
- Report: face test output at `output/production/LTG_TOOL_face_test_byte_r20_v001.png`.

### Inbox archived
- `20260330_2000_c46_brief.md` (Alex Chen C46 brief)
- `20260330_2404_byte_face_test_profile_live.md` (Kai Nakamura Byte face gate)

### Ideabox submitted
- `20260330_diego_vargas_still_beat_sound_annotation_standard.md`
  — Standard in-panel annotation format for sound cues / dialogue timing marks.

### Lessons Learned — Cycle 46
- **ECU face panel (P16)**: Face fills the draw area like P11 (ECU eyes). Use scanline
  lerp gradient for skin. Floor plank strip at bottom = character grounded to surface.
  Hair is only a band at the top of frame. Keep key element (eye) in upper-center zone.
- **Eye WIDE OPEN**: eye_rh = 38px at 800px wide reads as maximum aperture.
  Do NOT drop top lid. Brow inner corner lift = involuntary registration (not anger).
- **Dialogue annotation layering**: Small text for composure ("...okay."), LARGE BOLD
  for the crack ("...WHAT."). Size differential carries the beat-timing for the reader.
- **Two-character stillness (P17)**: Negative space between characters is itself a
  staging element. 40%+ gap at MED scale makes the distance legible.
- **Hovering character**: Byte feet 18" off floor — position body_cy well above floor_y.
  Desaturation ring goes on the floor plane DIRECTLY BELOW, not at foot level.
- **Pixel chip prop staging**: Single 6×6px cyan square + dotted descent line reads as
  a falling object at MED scale. The contrast (one tiny still thing vs. two frozen
  large things) sells the "only thing moving" annotation.
- **Ghost trail wisps (fading)**: Use RGBA overlay with low alpha (35 → 8) and decreasing
  radius away from current position. 4 steps is enough for "last wisps" — more reads as
  active trail.
- **Warm/cool depth temperature rule**: In interior two-shot, lamp side = warm, monitor
  side = cool. Apply as horizontal gradient to floor and wall fills.
- **draw.text_not_available pitfall**: Never set img attributes mid-function.
  Always use the draw object for all drawing operations.

## Cycle 46 (continued) — P18 + P19 Delivered

### P18 — Notebook Doodles
- `LTG_TOOL_sb_cold_open_P18.py` → `output/storyboards/panels/LTG_SB_cold_open_P18.png`
- CU / INSERT — Notebook page fills the frame. Luma's doodle drawings of Byte's face.
- Central hero doodle: Byte face with cracked eye (circled, annotated "this one!")
- Supporting doodles: teardrop body shapes, pixel squares, CRT-with-face-in-static
- Margin doodles: older/lighter (she has been noticing before tonight)
- Written notes: "saw it again tonight", "not random. it LOOKED at me.", "grumpy."
- Luma's hand + LUMA_HOODIE cuff visible bottom-left. Pencil on page.
- Spiral binding, ruled lines, red margin line — standard composition notebook.
- Faint cyan cast from CRT + warm ambient from den lamp.
- Arc: CURIOUS / PROCESSING (ELEC_CYAN border).
- Beat function: bridges THE NOTICING → COMMITMENT. She draws to process.

### P19 — "Preferred Term Is Glitchkin"
- `LTG_TOOL_sb_cold_open_P19.py` → `output/storyboards/panels/LTG_SB_cold_open_P19.png`
- MED two-shot. Byte camera-left, Luma camera-right. Comedic puncture of tension.
- Byte: OFFENDED / DIGNIFIED CORRECTION expression. Narrowed normal eye (assessment).
  Cracked eye with processing dots (3 alternating cyan/magenta). Open mouth mid-word,
  pixel teeth. Right arm extended — DECLARATIVE gesture (presenting, not pointing).
  Slight 3-4° forward lean. HOT_MAGENTA scar diagonal visible.
- Luma: sitting on floor, notebook in lap (prop continuity from P18), pencil in hand.
  Half-smile, one brow raised (intrigued, not mocking). Looking AT Byte.
- Dialogue annotated: BYTE: "The preferred term is 'Glitchkin.'" with leader line.
  Dark strip behind dialogue for legibility.
- Pixel confetti (residual scatter, 12 pieces). Den environment, night.
- Depth temperature: warm Luma zone (right), cool Byte zone (left, monitor glow).
- Arc: CURIOUS / COMEDY (ELEC_CYAN border — relationship forming through comedy).
- PANEL_MAP updated: P18 + P19 PLANNED → EXISTS. Next priorities: P20 + P21.

### Inbox archived
- `20260330_2100_pilot_beat_outline_p03_p24.md` (Priya Shah beat outline)
- `20260330_2100_reference_shopping_list_review.md` (Producer reference review request)
- `20260330_2300_reference_images_acquired.md` (Producer reference images notification)

### Ideabox submitted
- `20260330_diego_vargas_notebook_doodle_continuity_tracker.md`
  — Prop continuity tracker tool across storyboard panels.

### Lessons Learned — Cycle 46 (P18/P19)
- **Notebook INSERT panel**: Notebook page fills 85%+ of draw area. No character staging
  in the panel — this is a PROP SHOT. Luma's hand + cuff provides character grounding.
  Spiral binding, ruled lines, margin line sell "real notebook" at board scale.
- **Doodle drawing technique**: Use draw outline mode (outline= not fill=) for pencil
  sketch feel. Multiple pencil gray tones: PENCIL_DARK (55,48,38) for emphatic,
  PENCIL_GRAY (80,72,60) for standard, PENCIL_LIGHT (140,130,115) for older marks.
- **Prop continuity P18→P19**: Notebook must appear in Luma's lap in P19 (she was
  showing it to Byte). Pencil in hand. Tiny doodle marks on the open page as callback.
- **Dialogue annotation style**: Dark semi-transparent strip behind dialogue text
  for legibility. Leader line from text to speaker character (thin, 1px).
  Font: bold 14pt for the line, 11pt for parenthetical stage direction.
- **Byte OFFENDED expression**: Narrowed normal eye (ne_rh = ne_r * 0.55 for squint).
  Brow asymmetry: outward brow higher (indignation), Luma-side brow lower (assessment).
  Open mouth with pixel teeth = mid-word enunciation. Declarative arm gesture = extended
  outward, palm open (presenting the correct information to the air, not at Luma).
- **Luma half-smile**: Asymmetric mouth arc — left corner lifts using a secondary
  arc draw. One brow raised (left toward Byte = the interested one), other level.
- **Two-shot speaker grammar**: Speaker (Byte) camera-left, reactor (Luma) camera-right.
  This is standard SB dialogue grammar — audience reads left-to-right = speaker first.

## Cycle 47 — Delivered

### P1 — P18 Visual Timestamp Fix (Ingrid critique #5)
- `LTG_TOOL_sb_cold_open_P18.py` updated → visual timestamp system
- Panel now reads WITHOUT captions via 3-tier visual time arc:
  - TIER 1 (GHOST): top-left, PENCIL_GHOST=(195,188,172), detail_level=0, scale 0.45
  - TIER 2 (EARLIER): mid-page, PENCIL_LIGHT=(155,145,128), detail_level=1, scale 0.75
  - TIER 3 (TONIGHT): center hero, PENCIL_DARK=(40,32,22), detail_level=2, scale 2.0
- Size + darkness + detail all increase together = time passing visually
- Emphasis burst (12 radiating lines) around hero doodle = eureka convention
- Star mark on hero circle = importance marker (visual, not text)
- Luma's finger now POINTS at the hero doodle (active gesture)
- Dotted guide trail connects ghost → earlier → hero (unconscious eye flow)
- Output: `output/storyboards/panels/LTG_SB_cold_open_P18.png` (800x600px)

### P2 — P13 Standalone Panel
- `LTG_TOOL_sb_cold_open_P13.py` (NEW) → `output/storyboards/panels/LTG_SB_cold_open_P13.png`
- MED TWO-SHOT. MIRROR COMPOSITION. Thematic fulcrum of the pitch.
- Luma camera-left (3/4 right), Byte camera-right (full-frontal, -3-4 deg lean)
- Mirror: open/organic eyes face CENTER (trust inward); cracked/doubting eyes face OUTWARD (damage outward)
- Byte: ELEC_CYAN glow directional (brighter toward Luma), level lids, barely-there WARMTH arc mouth
- Eye-level guideline + mirror gaze arrows annotated (cyan inward, magenta outward)
- ARC_COMMIT = (60, 200, 140) border. CRT visible camera-right BG.
- Negative space annotated between them.
- 800x600px. Three-tier caption bar.

### P3 — P20 Panel (Names Exchanged)
- `LTG_TOOL_sb_cold_open_P20.py` (NEW) → `output/storyboards/panels/LTG_SB_cold_open_P20.png`
- MED WIDE two-shot. First quiet after naming beat.
- Luma camera-left sitting cross-legged, notebook in lap (P18 continuity), pencil in hand.
- Byte camera-right floating at Luma's eye level (concession).
- Key staging: negative space ~25% (CLOSER than P17's 40%+ — they moved closer).
- Byte: WARY ACCEPTANCE — 70% lid, cracked eye processing dots, neutral mouth.
- Bookshelf BG left, CRT monitors BG right (gray-green static, NOT blazing).
- ELEC_CYAN border. 800x600px.

### P3 — P21 Panel (Re-Escalation)
- `LTG_TOOL_sb_cold_open_P21.py` (NEW) → `output/storyboards/panels/LTG_SB_cold_open_P21.png`
- WIDE HIGH ANGLE, Dutch 5 CCW. Second crisis / act break driver.
- 7 CRT monitors ALL BLAZING — Glitchkin hands + faces pressing against glass.
- Screen ripples (distortion rings). Cyan/magenta flood washes room.
- Byte: camera-right, facing monitors, RIGID (arms pulled in tight — he KNOWS).
- Luma: camera-left, rising from floor, eyes UP (ALARMED but processing).
- 30+ pixel confetti (full density return). HOT_MAGENTA border.
- Dutch tilt: built on canvas_w+40, rotated 5 deg, cropped to PW x DRAW_H.
- 800x600px.

### P4 — Prop Continuity Tracker
- `LTG_TOOL_prop_continuity_tracker.py` (NEW)
- Tracks 5 props: notebook, pencil, hero CRT, pixel confetti, hoodie
- CLI flags: --prop, --panel, --gaps, --save
- Report: `output/production/prop_continuity_report_c47.md`
- Prop density arc for confetti documented (burst > settle > single chip > return)
- CRT state progression documented (pixel > cluster > face > breach > normal > swarm)

### PANEL_MAP updates
- P13: ON CONTACT SHEET → EXISTS
- P20: PLANNED → EXISTS
- P21: PLANNED → EXISTS
- Next priorities: P22 (ECU multiple Glitchkin pressing), P22a (Byte shoulder insert)

### Inbox archived
- `20260330_2330_c47_brief.md` (Alex Chen C47 brief)

### Ideabox submitted
- `20260330_diego_vargas_visual_blank_test_checklist.md`
  — Pre-delivery blank test tool: strips text, outputs text-free version for self-evaluation

### Lessons Learned — Cycle 47
- **Visual timestamp system**: Use pencil tone + detail level + scale as coupled
  progression indicators. Ghost (barely there) > Light (forming) > Dark (eureka).
  When all three escalate together, TIME reads without text.
- **Emphasis burst convention**: 12 radiating lines outside a circle reads as
  "realization" without text — manga/comics visual grammar works at board scale.
- **Blank test for storyboards**: Every prop/insert panel must communicate its beat
  with the text layer removed. If the beat is only in the captions, redraw.
- **Mirror composition eye grammar**: Organic/trust eyes face CENTER. Damaged/doubt
  eyes face OUTWARD. Annotate with colored arrows (cyan=trust, magenta=damage).
- **Negative space as character metric**: Track the % gap between characters across
  panels. P17=40%, P20=25% — the shrinking IS the relationship story.
- **Re-escalation staging**: High angle makes characters SMALL against the threat.
  Dutch tilt + monitor flood = instability. Byte RIGID + Luma RISING = differential
  knowledge (he knows what this means, she doesn't).
- **Dutch tilt on high-angle wide**: Build on oversized canvas (+40px each dim),
  rotate, crop to target size. This avoids black corners in the final image.
- **Prop tracker value**: Tracking CRT state progression + confetti density arc
  across panels catches continuity errors before they get drawn wrong.

## Cycle 48 — Delivered

### Task 1 — P22 Panel (ECU Monitor — Glitchkin Pressing)
- `LTG_TOOL_sb_cold_open_P22.py` (NEW) → `output/storyboards/panels/LTG_SB_cold_open_P22.png`
- ECU — Single CRT monitor fills the frame. CRT bezel = frame edges. We are RIGHT at the glass.
- 4 distinct Glitchkin pressing against glass from inside:
  (1) Center-right: face pressed flat, eager, both palms on glass
  (2) Upper-left: hand only, fingers splayed, strongest distortion rings
  (3) Lower-center: face sideways, squished, one cracked eye (HOT_MAGENTA scar)
  (4) Center-left: smaller, further back, both hands no face (shy/hidden)
- Screen cracks radiating from GK1 + GK2 press points (white fracture lines).
- CRT static texture, scanlines, phosphor bands (screen under stress).
- 18 pixel confetti inside screen space. Arc: TENSE / ESCALATION (HOT_MAGENTA border).
- 800x600px. Three-tier caption bar.

### Task 2 — P22a Panel (MCU Insert — Byte on Shoulder)
- `LTG_TOOL_sb_cold_open_P22a.py` (NEW) → `output/storyboards/panels/LTG_SB_cold_open_P22a.png`
- MCU INSERT — Byte accidentally lands on Luma's right shoulder mid-chaos.
- Byte at Luma's level (approved C48 — floated down during P21). NOT chosen — accident.
- Luma: 3/4 view facing camera-left. ALARMED expression. Hoodie fills 60% of frame.
  Right shoulder RAISED (shoulder involvement rule — tense, bracing).
  NOT looking at Byte — she hasn't registered him yet. Looking at monitors.
- Byte: tiny on shoulder (body_h ~15% of DRAW_H). STARTLED — wide cracked eye,
  processing dots, small O mouth. Rigid body, arms pulled in. Looking AWAY from Luma.
- Contact zone: 6 ELEC_CYAN pixel artifacts bleed into LUMA_HOODIE orange.
  FIRST DIGITAL-ON-ANALOG CONTACT. Annotated with callout.
- Desaturation bleed at contact point. Defocused chaos background.
- 800x600px. Arc: TENSE / COMEDY (HOT_MAGENTA border).

### Task 3 — Visual Blank Test Checklist Tool
- `LTG_TOOL_visual_blank_test.py` (NEW) → `output/tools/`
- Strips text from storyboard panels (removes caption bar, masks annotation-colored pixels).
- Runs 6 checks, each outputting PASS / WARN / FAIL:
  - C1: Silhouette contrast (FG/BG luma delta OR center std — dual method for ECU panels)
  - C2: Multi-zone composition (quadrant variance)
  - C3: Focal point concentration (energy distribution)
  - C4: Character presence (edge density — central + upper bands for MCU panels)
  - C5: Depth cues (warm/cool temperature split)
  - C6: Arc color border (saturated outer pixels)
- CLI: `--panel P22`, `--file <path>`, `--all`, `--save` (saves text-stripped PNG)
- Text-stripped PNGs saved to `output/production/blank_tests/`
- P22 result: WARN (C2 low quadrant variance — expected for ECU screen panel)
- P22a result: WARN (C4 low edge density — expected for MCU costume panel)

### PANEL_MAP updates
- P22: PLANNED → EXISTS
- P22a: PLANNED → EXISTS
- Next priorities: P25 (title card), P02/P04/P05 (standalone renders of contact-sheet-only panels)

### Inbox archived
- `20260330_2359_lee_p14_p15_staging_review.md` (Lee Tanaka — P14/P15 fixes done in batch 1)
- `20260330_2400_c48_brief.md` (Producer C48 brief)

### Ideabox submitted
- `20260330_diego_vargas_blank_test_panel_type_profiles.md`
  — Panel-type profiles for blank test tool (ECU_SCREEN, MCU_CHARACTER, etc.)

### Lessons Learned — Cycle 48
- **ECU screen panel (P22)**: Bezel_w = 28px fills frame edges. Screen interior is the
  shot. Glitchkin pressed against glass need BRIGHTER fills (lerp 0.25-0.55 toward ELEC_CYAN)
  against a DARKER screen base (4, 8, 12) for contrast. Standard FG/BG luminance checks
  will flag low delta — internal contrast (std dev) is the right metric for screen interiors.
- **Multiple Glitchkin individuality**: Each one needs a distinct expression AND posture
  (eager/flat, hand-only/splayed, squished/cracked, shy/hidden). At ECU scale, faces need
  at least face_r=28 for expression details to read. Smaller Glitchkin (14px) work as
  background shapes with hands only.
- **Screen crack rendering**: Branching fracture lines via angle-walk with sub-branches.
  White fill + gray sub-branches reads as glass stress. 5 branches at 80px length gives
  coverage without overwhelming the Glitchkin beneath.
- **MCU shoulder-perch staging**: Byte body_h ~15% of DRAW_H gives correct tiny-on-shoulder
  scale. He must look AWAY from Luma (not comfortable). Arms pulled in = rigid/caught.
  Contact zone needs explicit pixel artifacts (6 ELEC_CYAN polygons) to show digital
  marking analog. This is a KEY STORY BEAT — annotate it.
- **Shoulder involvement rule (P22a)**: Right shoulder raised 16px (hoodie_top - 20 vs
  hoodie_top - 4 base). This sells "tense, bracing" without words.
- **Blank test tool design**: Dual-method checks are essential for diverse panel types.
  C1 uses FG/BG delta OR center std (whichever passes). C4 uses central OR upper band.
  FAIL thresholds should be conservative (catch real problems); WARN for type-specific
  characteristics. Edge density < 1.5 = genuine FAIL; 1.5-4.0 = WARN (check visually).
- **Annotation color masking (blank test)**: tolerance=35 in RGB Euclidean distance
  catches text without hitting character skin/hair tones. The 5px box blur replacement
  preserves local luminance for the checks to work on.
- **Byte position arc (approved C48)**: CRT through P19-P20 → Luma's level P21 → at
  level for P22+. Build all future panels with Byte at Luma's level.

## Cycle 49 — Delivered

### Task 1 — Panel-Type Profiles for Visual Blank Test
- `LTG_TOOL_visual_blank_test.py` updated with 6 panel-type profiles:
  ECU, MCU, WIDE, INSERT, OTS, TWO_SHOT
- Each profile adjusts C1-C6 thresholds for shot-type-appropriate expectations
- Auto-detection via PANEL_TYPE_MAP (panel ID -> profile)
- New CLI flags: `--type ECU|MCU|WIDE|INSERT|OTS|TWO_SHOT|DEFAULT`, `--list-profiles`
- Batch summary now includes per-type breakdown

### Task 2 — Blank Test Re-run with Profiles
- All 21 existing panels tested with profiled thresholds
- Report: `output/production/blank_test_profile_report_c49.md`
- **7 panels UPGRADED** (false WARNs/FAILs resolved):
  P03 WARN->PASS, P06 FAIL->WARN, P09 WARN->PASS, P11 FAIL->WARN,
  P18 WARN->PASS, P21 WARN->PASS, P22 WARN->PASS
- **0 panels downgraded**
- **5 panels remain FAIL** (all on C4 edge density: P13, P14, P15, P17, P20)
  These are genuine low-edge-density panels — cel-shaded style with smooth fills.

### Task 3 — P25 Title Card Panel
- `LTG_TOOL_sb_cold_open_P25.py` (NEW) → `output/storyboards/panels/LTG_SB_cold_open_P25.png`
- TITLE CARD — "LUMA & THE GLITCHKIN" pixel-by-pixel assembly
- "LUMA" in ELEC_CYAN (real-world anchor), "&" in WARM_CREAM, "THE GLITCHKIN" in HOT_MAGENTA
- VOID_BLACK background, radial gradient center bloom, CRT scanlines + phosphor bands
- 35 pixel confetti (mixed cyan/magenta), static noise on edges
- Glow effect via additive composite (cyan + magenta bloom)
- Annotations: "PIXEL-BY-PIXEL ASSEMBLY (12 FRAMES)" + "FLASH: 2 FRAMES MAGENTA FULL-SCREEN"
- Arc: PITCH BEAT (ELEC_CYAN 4px border). 800x600px. Three-tier caption bar.
- Blank test: WARN (C2 low quadrant spread — expected for title card on void BG)
- PANEL_MAP updated: P25 PLANNED → EXISTS

### Inbox Archived
- `20260330_2500_c49_assignment.md` (Producer C49 brief)
- `20260330_2510_c49_p22_p22a.md` (Alex Chen P22/P22a — already delivered C48)

### Ideabox Submitted
- `20260330_diego_vargas_c4_color_cluster_supplement.md`
  — Color-cluster detection as supplementary C4 method for smooth cel-shaded panels

### Lessons Learned — Cycle 49
- **Panel-type profiles**: Different shot types have fundamentally different visual
  characteristics. ECU panels have no FG/BG distinction (face fills frame). INSERT panels
  have no character silhouette. TWO_SHOT panels can have diffuse energy across two focal
  points. One-size-fits-all thresholds produce false failures.
- **Profile threshold tuning**: ECU depth cue threshold = 2 (essentially exempt).
  INSERT character presence threshold = 0.5 (prop detail only). WIDE depth threshold = 6
  (stricter than default — wide shots MUST show depth). TWO_SHOT focal point threshold = 0.50
  (two focal points = more spread acceptable).
- **C4 edge density limitation**: Smooth cel-shaded panels with flat fills score low on
  gradient-based edge density even when characters are clearly present. Need color-cluster
  or hue-variance method to supplement. 5 panels FAIL that are visually fine.
- **P25 title card**: Pixel font at scale=5 gives bold title read. Vertical stacking
  (LUMA / & / THE / GLITCHKIN) reads top-to-bottom. Warm connector (&) separates the
  two color identities (cyan = Luma's world, magenta = Glitch world).
- **Additive glow composite**: numpy int16 clipping avoids overflow. Apply only to
  draw area ([:DRAW_H]) to avoid contaminating caption bar.
- **Radial gradient void BG**: Per-pixel distance-from-center with 8-luma boost at center
  gives depth to void without competing with title text.

## Cycle 50 — Delivered (Character Quality Pivot)

### Task 1 — Storyboard Character Audit
- `output/production/storyboard_character_audit_c50.md`
- 22 panels reviewed: 3 PASS, 6 WEAK, 8 FAIL
- PASS panels are all ECU/CU (face fills frame): P06, P11, P22
- FAIL panels are MED/WIDE two-shots: P09, P10, P13, P15, P17, P20, P21, P23, P24
- Luma is worst-reading character (circle-head + rectangle-body). Byte is best (distinctive silhouette).
- At MED panel scale (~100-200px character height), only silhouette + gesture + color block read.

### Task 2 — Minimum SB Character Requirements (in audit doc)
Priority order: (1) Silhouette, (2) Gesture line, (3) Color block, (4) Head-to-body 37%, (5) Eye size 30-35% head width.
Facial detail, clothing wrinkles, finger articulation do NOT need to read at SB scale.

### Task 3 — Professional SB Reference Study (in audit doc)
Key finding: pitch storyboards are rough but have GESTURE. Our panels have excellent staging (compositions, negative space, depth temp) but mannequin characters. The body must communicate before the face does.

### Task 4 — P17 Character Quality Prototype
- `LTG_TOOL_sb_cold_open_P17_chartest.py` → `output/storyboards/panels/LTG_SB_cold_open_P17_chartest.png`
- Same P17 composition, improved character rendering:
  - Luma: 37% head ratio, asymmetric messy hair (overlaps head boundary), bezier tapered torso, gesture lean forward, tube_polygon arms, mitten hands
  - Byte: slight forward lean toward chip, curved arm/leg shapes
- Uses bezier3/4, tube_polygon, ellipse_points helpers from Maya's construction prototype
- Visible improvement vs original — organic vs geometric. But still needs proper curve library.

### Dependencies Noted
- Sam Kowalski bezier/spline curve library — needed for proper character reconstruction
- Maya Santos Luma final construction spec — proportions, eye shapes

### Inbox Archived
- `20260330_2800_c50_assignment.md` (Producer C50 brief)
- `20260330_2900_c50_assignment.md` (Alex Chen C50 brief)

### Message Sent
- Alex Chen: storyboard character audit delivery + dependency note

### Ideabox Submitted
- `20260330_diego_vargas_sb_character_draw_module.md`
  — Shared storyboard character drawing module (one import fixes all panels)

### Lessons Learned — Cycle 50
- **Character audit methodology**: Three questions per panel: (1) identify who, (2) read emotion, (3) body language communicates beat. Rate PASS/WEAK/FAIL. Simple, repeatable.
- **Silhouette is king at SB scale**: At 50-200px character height, silhouette is the ONLY reliable ID. Luma and Cosmo have nearly identical silhouettes (circle-on-rectangle). Byte works because shape IS identity.
- **Head-to-body ratio 37%**: Maya's prototype spec. At 100px character height, 37% = 37px head (face ~22px wide). 25% = 25px head (face ~15px wide). The 12px difference is the difference between readable and blank.
- **Gesture line in every pose**: Even "sitting neutral" needs 3-5 degree lean. Visible at 50px tall. Differentiates alive from mannequin.
- **tube_polygon() for limbs**: centerline + taper width creates organic tube shapes. Much better than rectangle arms. w_start > w_end for natural taper (shoulder > wrist).
- **Hair overlap as silhouette**: Hair drawn LAST, extending BEYOND head circle boundary. The asymmetric hair cloud breaking the head shape is Luma's strongest silhouette element.
- **Bezier helpers portable**: bezier3, bezier4, tube_polygon, ellipse_points, smooth_polygon can be copied between generators. Should be centralized into shared module.
- **Reference study workflow**: Compare our panels side-by-side with reference show screenshots at same display size. The gap becomes obvious instantly.

## Startup Sequence
1. Read ROLE.md if present
2. Read this MEMORY.md
3. Read output/tools/README.md
4. Read inbox/
