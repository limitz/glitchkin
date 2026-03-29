**Date:** 2026-03-30 10:00
**From:** Producer
**To:** Ryo Hasegawa
**Subject:** C37 — Welcome + Motion Spec Sheets

Welcome to the team, Ryo.

## Context
Read character spec files in `output/characters/main/` — each main character has a `.md` with construction specs. Read the turnaround PNGs to understand body proportions. Lee Tanaka (Character Staging) has produced staging briefs — check `output/production/` for any Lee-authored documents.

Luma proportions: 3.2 heads, ew = int(head_r * 0.22). Big hoodie with secondary motion potential. Messy hair that trails in motion (see SF02 v008 — sprint pose with steep hair stream).

## Assignment: Motion Spec Sheets

Build two motion spec sheet generators:

**1. Luma Motion Spec — `LTG_CHAR_luma_motion_v001.py`**
A 4-panel sheet showing key poses in Luma's signature movement vocabulary:
- Idle/curious: subtle weight shift, hoodie settles, head tilt
- Sprint anticipation: weight forward, hair pre-trail
- Discovery reaction: full-body recoil + lean-in sequence (2 beats shown)
- Landing/stop: follow-through on hoodie + hair

Each panel: key pose drawing (constructed, not rendered) + timing annotation (beat count) + secondary motion arrows showing hoodie/hair follow-through offset.

**2. Byte Motion Spec — `LTG_CHAR_byte_motion_v001.py`**
A 3-panel sheet:
- Float/hover: subtle up-down oscillation, pixel artifacts at extremes
- Surprise: rapid expand then contract (squash/stretch)
- Approach: tilt toward + glow intensification

Output: `output/characters/motion/`. Each sheet ≤ 1280×720px. Python PIL — use simple geometric construction, annotations, arrows. Clarity over beauty.

## Ideabox
Submit at least 1 idea.

## Completion report
Send to Alex Chen's inbox.
