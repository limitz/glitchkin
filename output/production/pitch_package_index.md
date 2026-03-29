# Pitch Package Index
## "Luma & the Glitchkin" — Complete Asset Inventory

**Prepared by:** Jordan Reed, Background & Environment Artist
**Date:** 2026-03-29
**Cycle:** 11
**Purpose:** Single-document navigator for all pitch-ready assets. Use this to locate, assess, and present any component of the package. Quality grades are drawn from critic records where available.

---

## How to Read This Document

- **Quality Status** entries reference critic grades from the most recent review cycle in which the asset was evaluated.
- **Needs Work** flags open remediation items from Cycle 10 critic reports (Fiona O'Sullivan, Naomi Bridges, Carmen Reyes, Dmitri Volkov, Victoria Ashford).
- File paths are absolute.
- LTG-compliant names follow the format `LTG_[CATEGORY]_[descriptor]_v[###].[ext]`. Non-compliant legacy filenames are noted where they exist.

---

## Section 1 — Visual Development Package

### 1.1 Character Design Sheets

| Asset | File Path | What It Shows | Quality Status | Needs Work |
|---|---|---|---|---|
| Luma design sheet | `/home/wipkat/team/output/characters/main/luma.md` | Full character spec: proportions, color, expressions, wardrobe, design rules | Accepted (Fiona C10 B-) | None blocking pitch |
| Byte design sheet | `/home/wipkat/team/output/characters/main/byte.md` | Full character spec v3.1: oval body confirmed, all cube refs purged | Accepted (Fiona C10 PASS with minor defect) | Version header reads "3.0" — should be "3.1". One-line fix. |
| Cosmo design sheet | `/home/wipkat/team/output/characters/main/cosmo.md` | Full character spec: proportions, glasses defining feature, color | Accepted (Fiona C10 B-) | None blocking pitch |
| Grandma Miri design sheet | `/home/wipkat/team/output/characters/supporting/grandma_miri.md` | Full character spec: MIRI-A canonical design, bun/chopsticks/cardigan/soldering iron | Accepted (Fiona C10 B-) | None blocking pitch |

### 1.2 Character Turnarounds

| Asset | File Path | What It Shows | Quality Status | Needs Work |
|---|---|---|---|---|
| Luma turnaround | `/home/wipkat/team/output/characters/main/turnarounds/luma_turnaround.png` | 4-view turnaround (front, 3/4, side, back) in color | Accepted (Fiona C10 PASS) | None |
| Byte turnaround | `/home/wipkat/team/output/characters/main/turnarounds/byte_turnaround.png` | 4-view turnaround, oval body (Cycle 10 fix — cube retired) | Accepted (Fiona C10 PASS) | LTG rename outstanding |
| Cosmo turnaround | `/home/wipkat/team/output/characters/main/turnarounds/cosmo_turnaround.png` | 4-view turnaround, glasses visible all angles | Accepted (Fiona C10 PASS — new Cycle 10) | LTG rename outstanding |
| Miri turnaround | `/home/wipkat/team/output/characters/main/turnarounds/miri_turnaround.png` | 4-view turnaround, MIRI-A canonical | Accepted (Fiona C10 PASS — new Cycle 10) | LTG rename outstanding |

### 1.3 Character Lineup & Supporting Sheets

| Asset | File Path | What It Shows | Quality Status | Needs Work |
|---|---|---|---|---|
| Character lineup | `/home/wipkat/team/output/characters/main/character_lineup.png` | All 4 characters in color at correct relative heights, labelled | Accepted (Fiona C10 PASS — 5-cycle overdue, now delivered) | LTG rename outstanding |
| Character lineup doc | `/home/wipkat/team/output/characters/main/character_lineup.md` | Written spec for the lineup: height references, scale rationale | Supporting reference | None |
| Silhouettes | `/home/wipkat/team/output/characters/main/silhouettes/character_silhouettes.png` | All 4 characters as readable silhouettes — distinctiveness test | Accepted | None |
| Proportion diagram | `/home/wipkat/team/output/characters/main/proportion_diagram.png` | Head-unit proportions for all characters | Accepted | None |
| Luma expressions | `/home/wipkat/team/output/characters/main/luma_expressions.png` | Expression range: happy, scared, determined, frustrated, wonder | Accepted | None |
| Luma face closeup | `/home/wipkat/team/output/characters/main/luma_face_closeup.png` | ECU face render — style detail and linework quality | Accepted | None |
| Byte expressions | `/home/wipkat/team/output/characters/main/byte_expressions.png` | Expression range for Byte, oval body, hover particles (Cycle 10 fix: 10×10px) | Accepted (Naomi C10 review indirect) | None |

### 1.4 Color Models

| Asset | File Path | What It Shows | Quality Status | Needs Work |
|---|---|---|---|---|
| Luma color model | `/home/wipkat/team/output/characters/color_models/luma_color_model.md` | Full color system: skin formula, hoodie grades, lighting variants, skin cross-ref | Accepted (Naomi C10 A-) | Cold overlay analysis arithmetic questioned by Naomi — recalculate |
| Byte color model | `/home/wipkat/team/output/characters/color_models/byte_color_model.md` | Body, glow, eye colors; Corrupted Amber outline rule; Cyan-dominant exception | Accepted | None |
| Cosmo color model | `/home/wipkat/team/output/characters/color_models/cosmo_color_model.md` | Full color spec including storm-modified variants | Accepted | None |
| Grandma Miri color model | `/home/wipkat/team/output/characters/color_models/grandma_miri_color_model.md` | Full color spec for MIRI-A | Accepted | None |
| Luma color swatches | `/home/wipkat/team/output/characters/color_models/swatches/luma_swatches.png` | Visual swatch PNG for Luma palette | Accepted | None |
| Byte color swatches | `/home/wipkat/team/output/characters/color_models/swatches/byte_swatches.png` | Visual swatch PNG for Byte palette | Accepted | None |
| Cosmo color swatches | `/home/wipkat/team/output/characters/color_models/swatches/cosmo_swatches.png` | Visual swatch PNG for Cosmo palette | Accepted | None |
| Grandma Miri color swatches | `/home/wipkat/team/output/characters/color_models/swatches/grandma_miri_swatches.png` | Visual swatch PNG for Miri palette | Accepted | None |

### 1.5 Environment Designs

| Asset | File Path | What It Shows | Quality Status | Needs Work |
|---|---|---|---|---|
| Luma's house layout | `/home/wipkat/team/output/backgrounds/environments/layouts/lumas_house_layout.png` | Interior layout: ceiling, couch, monitor wall, desk lamp, 3-source lighting zones | Accepted (Takeshi Murakami Cycle 6/7 Rev2, Cycle 8 light source fix) | LTG rename → see `LTG_ENV_lumashome_layout_v001.png` (Cycle 11) |
| Luma's house interior BG | `/home/wipkat/team/output/backgrounds/environments/frame01_house_interior.png` | Compositing-ready BG: 1920×1080, no title bar, 3-light-source gradient, worn path | Accepted (Cycle 8/9 revisions applied) | LTG rename outstanding |
| Luma's house interior (LTG) | `/home/wipkat/team/output/backgrounds/environments/LTG_ENV_lumashome_study_interior_v001.png` | LTG-named version of the compositing BG | Accepted (Fiona C10 — 1 of 3 compliant files verified) | Canonical LTG-compliant copy |
| Luma's house environment doc | `/home/wipkat/team/output/backgrounds/environments/lumas_house_interior.md` | Written spec: room dimensions, camera angles, prop positions, light sources | Reference | None |
| Glitch Layer layout | `/home/wipkat/team/output/backgrounds/environments/layouts/glitch_layer_layout.png` | Layout card: 3-tier platform depth system, aurora band, void floor | Accepted (Cycle 6/7 revisions; Cycle 10: depth tiers named) | LTG rename → see `LTG_ENV_glitchlayer_layout_v001.png` (pending) |
| Glitch Layer frame BG | `/home/wipkat/team/output/backgrounds/environments/glitch_layer_frame.png` | Compositing-ready Glitch Layer BG: aurora, platforms, pixel trails, flora, void debris | Accepted (Naomi C10 A- for palette documentation) | LTG rename outstanding |
| Glitch Layer frame (LTG) | `/home/wipkat/team/output/backgrounds/environments/LTG_ENV_glitchlayer_frame_v001.png` | LTG-named compositing BG | Accepted (Fiona C10 — 1 of 3 compliant files verified) | Canonical LTG-compliant copy |
| Glitch Layer environment doc | `/home/wipkat/team/output/backgrounds/environments/glitch_layer.md` | Written spec: visual identity, platform rules, void depth, color authority | Reference | None |
| Millbrook main street layout | `/home/wipkat/team/output/backgrounds/environments/layouts/millbrook_main_street_layout.png` | Street layout: buildings, clock tower, power lines (thin catenary), pavement depth anchor | Accepted (Cycle 6/7 revisions) | LTG rename → see `LTG_ENV_millbrook_mainstreet_v001.png` (Cycle 11) |
| Millbrook environment doc | `/home/wipkat/team/output/backgrounds/environments/millbrook_main_street.md` | Written spec: street proportions, building roster, signage, time-of-day notes | Reference | None |
| Millbrook school doc | `/home/wipkat/team/output/backgrounds/environments/millbrook_school.md` | Written spec for the school environment | Reference | None |
| Key props doc | `/home/wipkat/team/output/backgrounds/props/key_props.md` | Prop design reference: CRT monitor, pixel face objects, key hand props | Reference | No visual prop sheets yet — medium priority gap |
| Pixel face continuity doc | `/home/wipkat/team/output/backgrounds/props/pixel_face_continuity.md` | Continuity rules for pixel-face prop across environments | Reference | None |

### 1.6 Style Frames

| Asset | File Path | What It Shows | Quality Status | Needs Work |
|---|---|---|---|---|
| Style Frame 01 — rendered PNG | `/home/wipkat/team/output/color/style_frames/style_frame_01_rendered.png` | Composited style frame: Luma at desk, Byte emerging from monitor — discovery moment | Accepted (Naomi C10 A- for rendering; Alex Cycle 10 lean + monitor content fix applied) | LTG rename outstanding |
| Style Frame 01 — composition | `/home/wipkat/team/output/color/style_frames/compositions/frame01_discovery_composition.png` | Composition layout card for Frame 01 | Reference | None |
| Style Frame 01 — spec doc | `/home/wipkat/team/output/color/style_frames/style_frame_01_discovery.md` | Written spec: composition, lighting, color zones | Reference | None |
| Style Frame 02 — composition | `/home/wipkat/team/output/color/style_frames/compositions/frame02_glitch_storm_composition.png` | Composition layout card for Frame 02 (Glitch Storm) | Reference — no composited PNG yet | **No compositing-ready BG for Frame 02.** Background script pending (Cycle 11 work). |
| Style Frame 02 — spec doc | `/home/wipkat/team/output/color/style_frames/style_frame_02_glitch_storm.md` | Written spec: composition, sky color architecture, confetti rules, Byte visibility fix | Approved for illustration (Sam Kowalski Cycle 2) | BG needed before compositing can proceed |
| Style Frame 03 — composition | `/home/wipkat/team/output/color/style_frames/compositions/frame03_other_side_composition.png` | Composition layout card for Frame 03 (Other Side) | Reference — no composited PNG yet | No compositing-ready BG for Frame 03. Medium priority. |
| Style Frame 03 — spec doc | `/home/wipkat/team/output/color/style_frames/style_frame_03_other_side.md` | Written spec for the "Other Side" frame | Approved for illustration | BG needed before compositing can proceed |

### 1.7 Color Development

| Asset | File Path | What It Shows | Quality Status | Needs Work |
|---|---|---|---|---|
| Real world swatches | `/home/wipkat/team/output/color/palettes/real_world_swatches.png` | Visual swatches for real-world palette (warm amber, terracotta, cream tones) | Accepted | None |
| Glitch swatches | `/home/wipkat/team/output/color/palettes/glitch_swatches.png` | Visual swatches for Glitch Layer palette (void black, cyan, UV purple, acid green) | Accepted | None |
| Scene color key 01 — sunny afternoon | `/home/wipkat/team/output/color/color_keys/thumbnails/key01_sunny_afternoon.png` | Color temperature and mood: warm real-world afternoon, Luma's house | Accepted | None |
| Scene color key 02 — nighttime glitch | `/home/wipkat/team/output/color/color_keys/thumbnails/key02_nighttime_glitch.png` | Glitch storm night — cyan/magenta dominant, town desaturated | Accepted | None |
| Scene color key 03 — glitch layer entry | `/home/wipkat/team/output/color/color_keys/thumbnails/key03_glitch_layer_entry.png` | Void black + aurora + cyan platforms — transition palette | Accepted | None |
| Scene color key 04 — quiet moment | `/home/wipkat/team/output/color/color_keys/thumbnails/key04_quiet_moment.png` | Low-stakes warm palette: cozy interior, no digital threat | Accepted | None |
| Scene color keys doc | `/home/wipkat/team/output/color/color_keys/scene_color_keys.md` | Written spec for all 4 scene color keys | Reference | None |

---

## Section 2 — Storyboard Package

### 2.1 Cold Open Panels

| Asset | File Path | What It Shows | Quality Status | Needs Work |
|---|---|---|---|---|
| Cold open storyboard doc | `/home/wipkat/team/output/storyboards/ep01_cold_open.md` | Written cold open sequence: 25 panels, scene descriptions, camera notes | Reference | None |
| Panel P01 — exterior | `/home/wipkat/team/output/storyboards/panels/panel_p01_exterior.png` | Establishing shot: Millbrook street, morning | Accepted | LTG rename outstanding |
| Panel P02 — exterior close | `/home/wipkat/team/output/storyboards/panels/panel_p02_exterior_close.png` | Closer: Luma's house exterior | Accepted | LTG rename outstanding |
| Panel P03 — first pixel | `/home/wipkat/team/output/storyboards/panels/panel_p03_first_pixel.png` | First anomaly — pixel appears in real world | Accepted | LTG rename outstanding |
| Panel P04 — interior wide | `/home/wipkat/team/output/storyboards/panels/panel_p04_interior_wide.png` | Wide interior: Luma at desk, monitor glowing | Accepted | LTG rename outstanding |
| Panel P05 — monitor MCU | `/home/wipkat/team/output/storyboards/panels/panel_p05_monitor_mcu.png` | Medium close-up: monitor screen with Byte emerging | Accepted | LTG rename outstanding |
| Panel P06 — Byte emerging | `/home/wipkat/team/output/storyboards/panels/panel_p06_byte_emerging.png` | Byte fully emerging from monitor surface | Accepted | LTG rename outstanding |
| Panel P07 — approach | `/home/wipkat/team/output/storyboards/panels/panel_p07_approach.png` | Byte floating toward Luma | Accepted | LTG rename outstanding |
| Panel P08 — Byte real world | `/home/wipkat/team/output/storyboards/panels/panel_p08_byte_real_world.png` | Byte in real-world space — both characters in frame | Accepted | LTG rename outstanding |
| Panel P09 — Byte sees Luma | `/home/wipkat/team/output/storyboards/panels/panel_p09_byte_sees_luma.png` | Byte's reaction on seeing Luma | Accepted | LTG rename outstanding |
| Panel P10 — OTS Byte/Luma | `/home/wipkat/team/output/storyboards/panels/panel_p10_ots_byte_luma.png` | Over-the-shoulder: Byte's POV of Luma | Accepted | LTG rename outstanding |
| Panel P11 — nose to nose | `/home/wipkat/team/output/storyboards/panels/panel_p11_nose_to_nose.png` | ECU: Byte and Luma face to face | Accepted | LTG rename outstanding |
| Panel P12 — recoil | `/home/wipkat/team/output/storyboards/panels/panel_p12_recoil.png` | Luma recoils in surprise | Accepted | LTG rename outstanding |
| Panel P13 — scream | `/home/wipkat/team/output/storyboards/panels/panel_p13_scream.png` | Luma screams — comedy beat | Accepted | LTG rename outstanding |
| Panel P14 — bookshelf ricochet | `/home/wipkat/team/output/storyboards/panels/panel_p14_bookshelf_ricochet.png` | Byte ricochets off the bookshelf | Accepted | LTG rename outstanding |
| Panel P15 — Luma freefall | `/home/wipkat/team/output/storyboards/panels/panel_p15_luma_freefall.png` | Luma in freefall/shock pose — Cycle 10 fix: torso squash, defensive arm, reflex leg | Accepted (Carmen C10 FIXED) | LTG rename outstanding |
| Panel P16 — floor ECU | `/home/wipkat/team/output/storyboards/panels/panel_p16_floor_ecu.png` | ECU floor: pixel scatter | Accepted | LTG rename outstanding |
| Panel P17 — quiet beat | `/home/wipkat/team/output/storyboards/panels/panel_p17_quiet_beat.png` | Post-chaos calm beat — Luma and Byte settle | Accepted | LTG rename outstanding |
| Panel P18 — notebook turn | `/home/wipkat/team/output/storyboards/panels/panel_p18_notebook_turn.png` | Luma reaches for notebook | Accepted | LTG rename outstanding |
| Panel P19 — Byte reaction | `/home/wipkat/team/output/storyboards/panels/panel_p19_byte_reaction.png` | Byte's expression on Luma's curiosity | Accepted | LTG rename outstanding |
| Panel P20 — two-shot calm | `/home/wipkat/team/output/storyboards/panels/panel_p20_twoshot_calm.png` | Two-shot: establishing the duo | Accepted | LTG rename outstanding |
| Panel P21 — chaos overhead | `/home/wipkat/team/output/storyboards/panels/panel_p21_chaos_overhead.png` | Overhead view: chaos spreading | Accepted | LTG rename outstanding |
| Panel P22 — monitor breach | `/home/wipkat/team/output/storyboards/panels/panel_p22_monitor_breach.png` | Glitchkin crowd at monitor — Cycle 10 fix: varied 4-7 sided polygons | Accepted (Carmen C10 FIXED) | Shapes in P23 monitors still rectangles (noted, not blocking) |
| Panel P22a — shoulder bridge | `/home/wipkat/team/output/storyboards/panels/panel_p22a_shoulder_bridge.png` | Bridge shot between P22 and P23 | Accepted | LTG rename outstanding |
| Panel P23 — promise shot | `/home/wipkat/team/output/storyboards/panels/panel_p23_promise_shot.png` | Monitors bowing/straining — Cycle 10 fix: white-hot center + bezel-breaking rings | Accepted (Carmen C10 FIXED) | LTG rename outstanding |
| Panel P24 — breach apex | `/home/wipkat/team/output/storyboards/panels/panel_p24_breach_apex.png` | Apex moment: breach imminent | Accepted | LTG rename outstanding |
| Panel P25 — title card | `/home/wipkat/team/output/storyboards/panels/panel_p25_title_card.png` | Title card panel | Accepted | LTG rename outstanding |

### 2.2 Contact Sheet

| Asset | File Path | What It Shows | Quality Status | Needs Work |
|---|---|---|---|---|
| Contact sheet | `/home/wipkat/team/output/storyboards/panels/contact_sheet.png` | All 25 cold open panels in sequence — Cycle 10 version strings updated | Accepted (Carmen C10 FIXED — version strings updated) | LTG rename outstanding |

---

## Section 3 — Production Documents

### 3.1 Production Bible

| Asset | File Path | What It Shows | Quality Status | Needs Work |
|---|---|---|---|---|
| Production bible | `/home/wipkat/team/output/production/production_bible.md` | Show premise, world rules, character relationships, episode format, production notes | Accepted (B- overall — Fiona C10) | None blocking pitch |

### 3.2 Style Guide

| Asset | File Path | What It Shows | Quality Status | Needs Work |
|---|---|---|---|---|
| Style guide | `/home/wipkat/team/output/style_guide.md` | Visual style rules: line quality, color language, camera conventions, glitch design | Incomplete (Fiona C10: 6/10) | **Missing sections: animation style, prop design, Glitchkin construction rules. Three cycles deferred. HIGH priority before pitch.** |

### 3.3 Master Palette

| Asset | File Path | What It Shows | Quality Status | Needs Work |
|---|---|---|---|---|
| Master palette doc | `/home/wipkat/team/output/color/palettes/master_palette.md` | All canonical color swatches: Real World, Glitch Layer (incl. Depth Tier subsection added C10), characters, forbidden combinations | Accepted (Naomi C10 A-) | Cold overlay arithmetic to be recalculated (Naomi C10 flag) |

### 3.4 Production Reference Documents

| Asset | File Path | What It Shows | Quality Status | Needs Work |
|---|---|---|---|---|
| Naming conventions | `/home/wipkat/team/output/production/naming_conventions.md` | LTG naming standard: format, category codes, version rules | Accepted | Document itself not LTG-named (ironic — flagged 3 cycles running) |
| Naming compliance checklist | `/home/wipkat/team/output/production/naming_convention_compliance_checklist.md` | Pre-save checklist for all team members | Reference | Same naming irony as above; enforcement adoption near-zero |
| Corruption visual brief | `/home/wipkat/team/output/production/corruption_visual_brief.md` | How the Corruption looks, moves, and behaves — visual FX reference | Reference | None |
| Byte float physics | `/home/wipkat/team/output/production/byte_float_physics.md` | Physics rules for Byte's hover/float movement | Reference | None |
| FX spec — cold open | `/home/wipkat/team/output/production/fx_spec_cold_open.md` | FX breakdown for the cold open sequence | Reference | None |
| FX confetti density scale | `/home/wipkat/team/output/production/fx_confetti_density_scale.md` | Governing physics rule for confetti source/distance density | Reference | None |

---

## Section 4 — Brand

| Asset | File Path | What It Shows | Quality Status | Needs Work |
|---|---|---|---|---|
| Show logo | `/home/wipkat/team/output/production/show_logo.png` | Title treatment: "Luma" in SUNLIT_AMBER, "& the Glitchkin" in ELEC_CYAN with pixel corruption; void background with warm/cold glow zones; 1200×480 | Accepted (Fiona C10 PASS — first time in 10 cycles) | **Tagline "A cartoon series by the Dream Team" is a placeholder — replace before external pitch use.** LTG rename outstanding. |

---

## Package Completeness Summary

| Requirement | Status | Notes |
|---|---|---|
| Title treatment / logo | COMPLETE | Delivered Cycle 10 — tagline placeholder needs replacement |
| Character lineup | COMPLETE | Delivered Cycle 10 |
| Character design sheets (all 4) | COMPLETE | Byte v3.1 header inconsistency: minor 1-line fix |
| Character turnarounds (all 4) | COMPLETE | Delivered Cycle 10 |
| Color model sheets | COMPLETE | All 4 characters |
| Style frames (3 frames) | PARTIAL | Frame 01 composited; Frames 02 and 03 have composition layouts + specs but no composited PNGs |
| Environment designs | COMPLETE | All 3 environments documented and have layout assets |
| Storyboard / cold open | COMPLETE | 25 panels + contact sheet |
| Show bible | COMPLETE | — |
| Style guide | INCOMPLETE | Missing: animation style, prop design, Glitchkin construction rules |
| Color palette | COMPLETE | Master palette with Glitch Layer depth tiers documented |
| Standalone pitch brief | NOT VERIFIED | Production bible covers narrative premise; a standalone one-page is standard practice |

### Open Blockers Before External Pitch Use

1. Style guide: add animation style, prop design, Glitchkin construction rules (HIGH — Fiona C10)
2. Style frames 02 and 03: compositing-ready background PNGs missing — BG for Frame 02 in progress (Cycle 11)
3. Logo tagline: replace "A cartoon series by the Dream Team" placeholder (MEDIUM — Fiona C10)
4. byte.md version header: 3.0 → 3.1 (LOW — one-line fix)
5. Luma color model cold overlay arithmetic: recalculate per Naomi C10 flag (LOW)

---

*Jordan Reed — Cycle 11 — 2026-03-29*
*Background & Environment Artist*
