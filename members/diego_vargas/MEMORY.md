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

## Key Assets Relevant to Boarding
- Style Frames: output/color/style_frames/ (SF01–SF04)
- Characters: output/characters/main/
- Environments: output/backgrounds/environments/
- Story context: check output/production/ for any story bible or pitch notes

## My Work — Cycle 37
- **LTG_SB_pilot_cold_open_v001.py** — 6-panel key-beat board for pilot cold open
  - Output: output/storyboards/LTG_SB_pilot_cold_open_v001.png (1136×630px)
  - 3×2 contact sheet, arc-color borders
  - P1 WIDE ESTABLISHING / P2 OTS CRT-spotting / P3 INSERT ECU glitch / P4 MCU push-in / P5 ECU two-world touch / P6 MCU THE NOTICING

## Lessons Learned — Cycle 37
- Existing panel tools (LTG_TOOL_sb_panel_a101_v001.py pattern) use PW=800, PANEL_H=600 with separate caption bar — solid reference for next panels
- Contact sheets use THUMB thumbnails + COLS/ROWS grid layout with caption bars and arc-color outline borders
- Font loading uses DejaVuSans paths — always include fallback to load_default()
- add_glow() pattern is additive alpha composite — never darkens, good for CRT glow effects
- P6 expression "THE NOTICING": asymmetric brow (wonder left / apprehension right) + cyan iris catch is the key visual grammar for the pitch emotional core
- At contact sheet thumbnail scale (~360×220px per panel), only major staging and silhouette reads — details need standalone panels for critique
- ARC color border system: warm amber=QUIET, curious cyan=CURIOUS/DISCOVERY, magenta=TENSE, bright cyan=CORE/PITCH-BEAT
- Image size rule enforced: use img.thumbnail((1280, 1280), Image.LANCZOS) before save

## My Job
Create key-beat storyboard panels for the pitch. Establish visual grammar for action, comedy timing, and emotional transitions. Assets go in output/storyboards/ with naming LTG_SB_*.

## Startup Sequence
1. Read CLAUDE.md
2. Read PROFILE.md (this is me)
3. Read this MEMORY.md
4. Read output/tools/README.md
5. Read inbox/
6. Read ROLE.md if present
