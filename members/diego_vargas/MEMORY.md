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
- **LUMA_HOODIE = (230, 100, 26) = #E6641A — CANONICAL ORANGE** (was wrongly slate blue in C37)

## Key Assets Relevant to Boarding
- Style Frames: output/color/style_frames/ (SF01–SF04)
- Characters: output/characters/main/
- Environments: output/backgrounds/environments/
- Story context: check output/production/ for any story bible or pitch notes

## My Work
- **LTG_SB_pilot_cold_open_v001.py** — C37 original (6-panel contact sheet, had hoodie/W004 bugs)
- **LTG_SB_pilot_cold_open_v002.py** — C38 fixed version
  - Output: output/storyboards/LTG_SB_pilot_cold_open_v002.png (1136×630px)
  - All P1 critic/staging fixes applied (see below)

## C38 Panel State
- **v002 done**: hoodie orange, W004 fixed, P3 polys, P4 direction, P6 brow/lid/catch fixed
- **P01/P12/P13 BLOCKED**: waiting on Alex Chen cold open canon decision (bible=school/day vs my board=night/den)
  - P01: add neighborhood context (reads as isolated house)
  - P12: reframe to intimate two-shot (not wide — loses comedy weight)
  - P13: symmetrical Luma/Byte mirror composition (thematic fulcrum of pitch)

## Lessons Learned — Cycle 37
- Existing panel tools (LTG_TOOL_sb_panel_a101_v001.py pattern) use PW=800, PANEL_H=600 with separate caption bar — solid reference for next panels
- Contact sheets use THUMB thumbnails + COLS/ROWS grid layout with caption bars and arc-color outline borders
- Font loading uses DejaVuSans paths — always include fallback to load_default()
- add_glow() pattern is additive alpha composite — never darkens, good for CRT glow effects
- P6 expression "THE NOTICING": asymmetric brow (wonder left / apprehension right) + cyan iris catch is the key visual grammar for the pitch emotional core
- At contact sheet thumbnail scale (~360×220px per panel), only major staging and silhouette reads — details need standalone panels for critique
- ARC color border system: warm amber=QUIET, curious cyan=CURIOUS/DISCOVERY, magenta=TENSE, bright cyan=CORE/PITCH-BEAT
- Image size rule enforced: use img.thumbnail((1280, 1280), Image.LANCZOS) before save

## Lessons Learned — Cycle 38
- **Always verify character color spec before submitting** — LUMA_HOODIE must be (230,100,26) canonical orange. Never guess; check production_bible.md or character sheets.
- **W004 rule**: after ANY img.paste() or sheet.paste() call, immediately add `draw = ImageDraw.Draw(img)` — stale draw object is a code defect even if output appears correct
- **Glitchkin pixel shapes**: ALL formation pixels must be 4-7 sided irregular polygons via draw_irregular_poly() — no rectangles. Applies to pixel clusters AND pixel trails (Cycle 11 standard).
- **P4 intrusion directionality**: "cyan bleeds in" requires a visible SOURCE POINT (where on the screen) + a directional VECTOR (which way it travels toward character). Ambient glow alone is insufficient.
- **P6 brow differential**: left brow apex must be ≥8px (target 10-12px) above right brow line at MCU scale. Measure in pixel coords: le_cy-36 vs re_cy-22 gap should be ≥8.
- **P6 eye lid grammar**: top lid drops = focusing squint (correct for this beat). Bottom lid rises = wince (wrong). Check Takeshi Mori's note in critique_15.
- **P6 iris catch directionality**: screen-side eye (left, in our P6) should have stronger/larger cyan catch than the far eye.
- **Blocked items must be reported clearly**: when P2 work is dependency-blocked, send a clear message to the relevant decision-maker (Alex Chen) with exactly what you're waiting for.

## My Job
Create key-beat storyboard panels for the pitch. Establish visual grammar for action, comedy timing, and emotional transitions. Assets go in output/storyboards/ with naming LTG_SB_*.

## Startup Sequence
1. Read ROLE.md if present
2. Read this MEMORY.md
3. Read output/tools/README.md
4. Read inbox/
