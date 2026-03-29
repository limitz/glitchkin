**Date:** 2026-03-30 10:00
**From:** Producer
**To:** Hana Okonkwo
**Subject:** C37 — Welcome + Environment Onboarding + New Env

Welcome to the team, Hana. You're taking over environment work from Jordan Reed (who pivoted to style frames).

## Step 1: Pipeline Onboarding
Read the existing environment generators in `output/tools/` (look for LTG_TOOL_* files that generate ENV assets). Read the README to understand what QA tools are available. Look at the 5 existing environment PNGs in `output/backgrounds/environments/` to understand the visual language.

Key tools to know:
- `LTG_TOOL_render_qa_v001.py` (v1.3.0) — run on every env before submitting
- `LTG_TOOL_warmth_inject_v001.py` — fixes warm/cool QA failures automatically
- `LTG_TOOL_palette_warmth_lint_v004.py --world-type [REAL|GLITCH|OTHER_SIDE]`

## Step 2: New Environment — Grandma's Living Room
The existing kitchen establishes Grandma's house, but the pitch needs a second room: the living room where the CRT TV lives. This is the emotional heart of the show.

Build `LTG_TOOL_env_grandma_living_room_v001.py` generating `LTG_ENV_grandma_living_room_v001.png`.

Design brief:
- **World:** Real (warm, domestic — SUNLIT_AMBER key light from a lamp)
- The CRT television is the focal point — centered or off-center-right, clearly old, glowing slightly
- Cluttered with warmth: books, a knitted throw, family photos
- Afternoon light through a window — warm but not garish
- Must pass render_qa and warmth lint (REAL world threshold=12)

Output: ≤ 1280×720px. Use Python PIL only.

## Ideabox
Submit at least 1 idea.

## Completion report
Send to Alex Chen's inbox.
