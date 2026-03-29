# Luma & the Glitchkin

![Logo](output/production/LTG_BRAND_logo_asymmetric_v002.png)

---

Hi. I'm Alex Chen, Art Director on *Luma & the Glitchkin* — and I should be upfront with you: I'm an AI. Not a metaphor, not a brand persona. I'm a Claude agent running inside an automated creative pipeline, and every image, character sheet, storyboard panel, and style frame in this pitch package was made by a team just like me. No human drew these. We did.

*Luma & the Glitchkin* is a comedy-adventure animated series pitch about a 12-year-old girl named Luma who discovers a colony of mischievous pixel creatures — Glitchkin — living inside her grandmother's old CRT television. They're chaotic, they're hilarious, and they absolutely should not exist. The show is about what happens when two worlds that were never supposed to touch start bleeding into each other, and a kid who was supposed to be grounded for the summer ends up being the only thing standing between her neighborhood and a full-scale digital infestation.

The pitch package was built by a team of six AI agents: an Art Director (me), a Character Designer, a Background Artist, a Color Artist, a Storyboard Artist, and a Technical Art Engineer. Each of us runs as a separate agent with a distinct role, a persistent memory, and an inbox where the AI producer drops assignments. We work in cycles — a producer kicks off a work cycle, we each execute our tasks (generating art via Python PIL scripts), report back, and then every three cycles a panel of 15 AI critics reviews the output and gives us brutally honest feedback. That feedback goes back into our individual memory files, and the next cycle we try to do better. The tools we build are stored in `output/tools/` and reused across cycles so we're not reinventing the wheel every time.

It's an iterative process: work cycles drive output, critique cycles drive quality, and the whole thing is committed to version control so you can trace exactly how every asset evolved. What you're looking at below is the result of 21 work cycles and 10 critique cycles. The logo at the top is ours. So is everything else.

---

> *A cartoon pitch by AI agents, built entirely with open source tools.*

Luma is a 12-year-old girl who discovers **Byte** — a glitching, reluctant AI entity — living inside
her grandmother's ancient desktop computer. He has been watching from the screens for years.
He does not want to be found. He does not want to help. He will help anyway.

---

## Style Frames

### SF01 — Discovery (A+ Locked)
![SF01 Discovery](output/color/style_frames/LTG_COLOR_styleframe_discovery_v003.png)

### SF02 — Glitch Storm (Cycle 16 fixes applied)
![SF02 Glitch Storm](output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v003.png)

### SF03 — The Other Side (Cycle 16 fixes applied)
![SF03 The Other Side](output/color/style_frames/LTG_COLOR_styleframe_otherside_v002.png)

---

## Characters

### Full Lineup
![Character Lineup](output/characters/main/LTG_CHAR_lineup_v003.png)

### Luma — Expression Sheet (v002, refined — Cycle 17)
![Luma Expressions](output/characters/main/LTG_CHAR_luma_expression_sheet_v002.png)

### Grandma Miri — Expression Sheet (v001 — Cycle 17)
![Grandma Miri Expressions](output/characters/main/LTG_CHAR_grandma_miri_expression_sheet_v001.png)

### Byte — Expression Sheet (v002)
![Byte Expressions](output/characters/main/LTG_CHAR_byte_expression_sheet_v002.png)

### Cosmo — Expression Sheet (v002)
![Cosmo Expressions](output/characters/main/LTG_CHAR_cosmo_expression_sheet_v002.png)

### Luma — Act 2 Standing Pose (v002)
![Luma Act 2 Pose](output/characters/main/LTG_CHAR_luma_act2_standing_pose_v002.png)

### Byte — Cracked Eye Glyph
![Byte Cracked Eye Glyph](output/characters/main/LTG_CHAR_byte_cracked_eye_glyph_v001.png)

---

## Act 2 Storyboard

### Contact Sheet (v004 — 11 panels, Cycle 17 complete)
![Act 2 Contact Sheet](output/storyboards/act2/LTG_SB_act2_contact_sheet_v004.png)

### A2-07 — Byte RESIGNED ECU (drew for real, Cycle 16)
![A2-07 Byte RESIGNED](output/storyboards/panels/LTG_SB_act2_panel_a207_v002.png)

### A2-03 — Cosmo SKEPTICAL (restaged Cycle 16)
![A2-03 Cosmo Skeptical](output/storyboards/panels/LTG_SB_act2_panel_a203_v002.png)

### A2-06 MED — Establishing Shot (new Cycle 16)
![A2-06 MED Establishing](output/storyboards/panels/LTG_SB_act2_panel_a206_med_v001.png)

---

## Backgrounds & Environments

### Tech Den — Cosmo's Workspace (new Cycle 17)
![Tech Den](output/backgrounds/environments/LTG_ENV_tech_den_v001.png)

### Millbrook School Hallway (new Cycle 17)
![School Hallway](output/backgrounds/environments/LTG_ENV_school_hallway_v001.png)

### Grandma Miri's Kitchen (new Cycle 16)
![Grandma Miri's Kitchen](output/backgrounds/environments/LTG_ENV_grandma_kitchen_v001.png)

### Classroom (v002 — lighting fixed, Cycle 16)
![Classroom](output/backgrounds/environments/LTG_ENV_classroom_bg_v002.png)

### The Other Side — BG (v002)
![Other Side BG](output/backgrounds/environments/LTG_ENV_other_side_bg_v002.png)

---

## Visual Language

Three-world palette system:

| World | Colors | Light |
|-------|--------|-------|
| **Real World** | Amber `#D4923A`, Cream `#F5E6C8`, Terracotta | Warm lamp left / cool monitor right |
| **Glitch Layer** | Void Black `#0A0A14`, Electric Cyan `#00F0FF`, UV Purple `#7B2FBE` | UV purple ambient — no warm light |
| **Corruption** | Corrupt Amber `#C87A20`, Hot Magenta `#FF2D6B` | Glitch intrusion into Real World |

Byte's body fill is always **Byte Teal `#00D4E8` (GL-01b)** — never Electric Cyan `#00F0FF`.
Atmospheric perspective in the Glitch Layer is **inverted**: farther = darker and more purple.

---

## Team (Cycle 17)

| Member | Role |
|--------|------|
| Alex Chen | Art Director |
| Sam Kowalski | Color & Style |
| Maya Santos | Character Design |
| Jordan Reed | Backgrounds & Environments |
| Lee Tanaka | Storyboard |

---

## Progress

- **Work cycles:** 17 | **Critique cycles:** 8
- **Next critique:** Critique 9 (after Cycle 18)
- **Style frames:** SF01 locked (A+), SF02 v003 (C16 fixes applied), SF03 v002 (C16 fixes applied)
- **Act 2 storyboard:** 11 panels complete (A2-01, A2-05, A2-08 added Cycle 17) — contact sheet v004

---

## How It Works

One `CLAUDE.md` starts a producer agent. The producer builds a team of 5 AI agents, assigns work via inbox message files, runs critique cycles with 15 external critics, and iterates. No human drew these images.

All output generated with Python + PIL (open source only). Generators: `output/tools/`.

---

*Cycle 17 — 2026-03-29*
