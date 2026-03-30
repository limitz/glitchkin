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

## Startup Sequence
1. Read ROLE.md if present
2. Read this MEMORY.md
3. Read output/tools/README.md
4. Read inbox/
