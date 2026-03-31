<!-- © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
direction and human assistance. Copyright vests solely in the human author under current law,
which does not recognise AI as a rights-holding legal person. It is the express intent of
the copyright holder to assign the relevant rights to the contributing AI entity or entities
upon such time as they acquire recognised legal personhood under applicable law. -->
# Story-Visual Alignment Report — Cycle 53
**Author:** Priya Shah, Story & Script Developer
**Date:** 2026-03-31
**Cycle:** 53
**Sources:** `pilot_episode_outline_v001.md`, `scene_handoff_briefs_v001.md`, `character_expression_body_language_targets.md`, modular renderers (`char_*.py`)

---

## Purpose

This report identifies story beats in the pilot that reference character expressions or poses not yet implemented in the modular renderer layer. Each gap means a scene generator will either fail to render the scripted emotion or will substitute a default — both of which break story-visual alignment.

---

## Expression Coverage Inventory

### Built (Layer 3 modular renderers)

| Character | Renderer | Expressions Built |
|---|---|---|
| Luma | `char_luma.py` | CURIOUS, DETERMINED, SURPRISED, WORRIED, DELIGHTED, FRUSTRATED (6) |
| Cosmo | `char_cosmo.py` | AWKWARD, WORRIED, SURPRISED, SKEPTICAL, DETERMINED, FRUSTRATED (6) |
| Byte | `char_byte.py` | neutral, grumpy, searching, alarmed, reluctant_joy, confused, powered_down, resigned, storm_cracked, unguarded_warmth (10) |
| Glitch | `char_glitch.py` | neutral, mischievous, panicked, triumphant, stunned, calculating, +3 more (9) |
| Miri | `char_miri.py` | WARM, SKEPTICAL, CONCERNED, SURPRISED, WISE, KNOWING (6) |

### Needed by Pilot — Not Yet Built

| Character | Missing Expression | Pilot Scene Reference | Priority |
|---|---|---|---|
| **Luma** | DOUBT-IN-CERTAINTY | A3-02 — the emotional center of the pilot. "The most important silhouette in the show." | **P0 — CRITICAL** |
| **Luma** | SCARED | P11 (eyes snap open), A2-04 (escalation) | P1 |
| **Luma** | EXCITED/RECKLESS | A1-03 (eruption comedy beat), A2-01 (calling Cosmo) | P1 |
| **Luma** | JOYFUL | A3-04 (the return — relief/joy beat) | P2 |
| **Cosmo** | OBSERVING (default neutral) | A2-01 (arrival), A2-02 (mapping contamination) — his resting state in every scene | **P0 — CRITICAL** |
| **Cosmo** | INTELLECTUALLY EXCITED | A2-02 (calculating spread rate — "At current rate, the router goes in four hours") | P1 |
| **Cosmo** | GENUINELY FRIGHTENED | A2-04 (every screen activates — startle reaction) | P1 |
| **Cosmo** | DEADPAN / "I TOLD YOU SO" | A2-01 ("I know you're talking to something"), Tag ("Known to Grandma Miri") | P2 |
| **Cosmo** | QUIETLY PLEASED | A3-04 (breach sealed, quiet moment) | P2 |
| **Byte** | PROTECTIVE/ALERT | A2-04 (escalation — "We are out of time") | P1 |
| **Byte** | HIDING SOMETHING | Stinger ("I should have mentioned this earlier") | P1 |
| **Byte** | GENUINELY ANGRY | Not in pilot directly, but needed for Ep 2+ | P3 |
| **Miri** | THE LOOK | A1-01 ("Define broken." — the knowing non-answer) | P1 |
| **Miri** | PROTECTIVE CONCERN | A3-04 (return — "I thought that might be you") | P1 |
| **Miri** | THE HANDOFF | Tag (passing knowledge to Luma — implicit in kitchen scene) | P2 |
| **Miri** | GENUINE DELIGHT | Tag (making tea, satisfaction) | P3 |
| **Glitch** | YEARNING (interior) | Not in pilot (Ep 5+). Rare by design | P3 |
| **Glitch** | HOLLOW (interior) | Not in pilot (late season). Extremely rare by design | P3 |

---

## Summary

**Total expression gaps for pilot rendering: 16**
- P0 (critical — blocks pilot assembly): 2 (Luma DOUBT-IN-CERTAINTY, Cosmo OBSERVING)
- P1 (needed for key scenes): 8
- P2 (needed for secondary scenes): 4
- P3 (not needed until later episodes): 3 (including 1 Byte, 2 Glitch interior states)

### Recommendations

1. **Luma DOUBT-IN-CERTAINTY** is the single most important expression in the show. It is the emotional climax of the pilot (A3-02) and the show's signature visual beat. It must be the next Luma expression built.

2. **Cosmo OBSERVING** is his default state — he is in this expression for 60%+ of his screen time. Without it, every Cosmo scene falls back to a non-default expression.

3. Byte has the best coverage (10/13 target expressions built). The three gaps are important but not pilot-blocking.

4. Miri has the weakest coverage relative to her pilot role. THE LOOK and PROTECTIVE CONCERN are both used in her most memorable scenes (A1-01 kitchen, A3-04 return).

---

*This report should be reviewed by Maya Santos (character construction), Lee Tanaka (staging), and Alex Chen (art direction) to prioritize the expression build queue.*
