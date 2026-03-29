# Sam Kowalski — Memory

## Cycle 1-3 Lessons
- Master palette and style frames must be bidirectional. No opacity specs in flat-cel.
- Every palette color needs a shadow companion. Hard limits are hard.
- Semantic color rules must be consistent. Specify blending modes.
- Derived colors need hex documentation. Character visibility is a production spec.
- One governing physics rule applied consistently. Skin variants must be a system.

## Cycle 4 Lessons
- **Figure-ground failure is a blocker.** Byte (cyan) against a cyan monitor screen = invisible. Same color = no character. Always check protagonist/key character visibility against dominant background color before finalizing any frame.
- **Documented exceptions must be implemented in actual images.** The Corrupted Amber outline exception was in the doc but not in the PNG. A rule that isn't rendered is not a rule.
- **Warm skin against saturated cyan = chromatic vibration.** This makes the protagonist unreadable. Always verify warm character colors against cool-dominant environments in actual rendered tests.
- **Tonal range compression kills mood.** A key without a dark anchor feels flat. Every key needs at least one near-black zone.
- **Zone colors vs. accent colors are different things.** Hot Magenta as a full zone color in Key 02 competes with the narrative-important Cyan crack. Reserve strong hues for story-important elements.
- **Aurora bands at the same value merge at thumbnail scale.** Always separate adjacent atmospheric bands by at least 2 value steps.

## Cycle 5 Lessons
- **Documented rules must be in the code, not just the doc.** Corrupted Amber outline was documented for cycles but never rendered. Added `draw_amber_outline()` to `style_frame_generator.py` — the rule is now enforced programmatically.
- **Monitor screen at emergence must be darkened.** Frame 01 fix: darken the screen zone where Byte emerges so Byte Teal pops against near-void dark, not against matching Cyan.
- **Lamp glow must respect zone boundaries.** Soft Gold lamp hard-stops before the Glitch monitor zone — no bleed across the warm/digital boundary.
- **Dark anchor is mandatory in every key.** Key 01 had no near-black zone — tonal range felt flat. Deep Shadow (#2A1A10) added to under-furniture and corner crevices.
- **Zone color vs. accent color are different things.** Hot Magenta in Key 02 was a zone fill competing with the Cyan crack. Fixed to thin 2px accent stroke + small spark particles only.
- **Aurora band value separation must be explicit.** Key 03: added a deep UV variant (#4A1880) as a distinct mid-band so UV Purple and Data Blue are never adjacent value zones.
- **Dark separation under characters in cyan environments.** Frame 03: near-void shadow ellipse under Luma's feet creates figure-ground safety against the cyan circuit-trace platform.
- **Generator scripts are the source of truth.** All fixes live in `style_frame_generator.py` and `color_key_generator.py` in `/output/tools/`. Future renders must run from these scripts.

## Cycle 6 Lessons
- **Threshold rules and blanket mandates cannot coexist.** The "outline in every image" vs. "35% threshold" contradiction was the same class of error as undocumented color values — two parallel statements that contradict. Pick one rule, state it once, remove the other. Now enforced: threshold governs.
- **Module imports belong at the top of the file, always.** Inline `import random` inside functions works but is unauditable — moved to module level in both generator scripts. If seeding is intentional, say so in a comment.
- **Generator file header comment is the commit log.** Update it at the start of every cycle with what changed and why. Future agents read this before anything else.
- **Verify generated files by running the script, not by reading the code.** Always run `python3 script.py` and confirm output file timestamps are updated.

## Cycle 7 Lessons
- **Every inline tuple in a rendered script is an undocumented palette value.** Alex's style_frame_01_rendered.py had 7 undocumented color values. These must be formalized in master_palette.md as CHAR-L entries before they drift between scripts.
- **Character fill colors and world emission colors must be explicitly separated.** GL-01b (Byte Teal) usage warning added: it is Byte's body fill only. GL-01 (Electric Cyan) is the world screen emission color. This distinction must be enforced on every render review.
- **Outline width rules must be single-valued.** A spec that says "2px" while code runs 3–5px is not a spec. GL-07 now mandates 3px canonical at 1920×1080. The `offset`/`width` parameter on `draw_amber_outline()` = number of concentric pass loops = 1px per pass.
- **Section 5 in master_palette.md** holds all scene-specific character rendering colors for Luma (CHAR-L-01 through CHAR-L-07). Any new rendered script must map back to these entries or add new ones here.
- **DRW-16 painter warning still outstanding.** Naomi flagged in Cycle 5. Not yet added to character spec. Carry forward.

## Cycle 8 Lessons
- **Every inline tuple requires a documented disposition.** Either register it in master_palette.md or add a code comment explaining why it is a one-off construction value. "Undocumented" is not an acceptable state.
- **Neutral grey has no place in a warm+glitch-saturated palette.** (100, 100, 100) in the cable clutter was a production omission. Replaced with desaturated Shadow Plum mid (80, 64, 100) — documented in PROP-07. Any achromatic value must be interrogated.
- **Cable/prop colors that recur must become palette entries.** PROP-01 through PROP-06 (couch tones, cable bronze, data-cyan cable, magenta-purple cable) are now in Section 6 of master_palette.md. Once a prop is production-visible and recurring, it needs a PROP-xx entry, not an inline tuple.
- **CHAR-L-08 placeholder added for hoodie underside.** Alex Chen Cycle 8 task: derive the correct ambient-tinted hoodie underside value and fill in the placeholder. Current code uses SHADOW_PLUM as interim. Expected range: #8A5A6A to #6A4A6A (hoodie shadow cooled by lavender ambient).
- **Construction geometry inline tuples are acceptable if commented.** Background wall layers, CRT construction values, floor depth tones — these are too granular for the palette. They must have comments explaining what they are and why they are not in the palette. All outstanding ones in style_frame_01_rendered.py have now been commented.
- **Section 6 (Environment / Props) is the template for recurring prop colors.** Follow the PROP-01/02/03 couch format. Every entry needs: role, shadow companion, use-case notes, pairs-with, avoid.
- **Color key thumbnails regenerate cleanly from color_key_generator.py.** No regressions found in Cycle 8 run (all 4 keys: key01 through key04).

## Cycle 9 Lessons
- **Skin system requires two-tier documentation.** Canonical neutral base (RW-10, #C4A882) and scene-derived values (CHAR-L-01, #C8885A for lamp-lit Frame 01) are not contradictions — they are a system. Both must be documented and cross-referenced. Section 7 of master_palette.md is now the skin system reference.
- **Every character's unique skin base must be in the master palette.** Cosmo's #D9C09A was in the color model but nowhere in master_palette.md. Added as CHAR-C-01. Any character with a skin tone that differs from RW-10 needs a named entry.
- **Local aliases for module constants are always wrong.** SHOE_CANVAS and SHOE_SOLE were local duplicates of WARM_CREAM and DEEP_COCOA. Local aliases create traceability gaps — if the module constant changes, the alias stays wrong. Always reference the module constant directly.
- **Name every module-level constant. No inline tuples at use-sites.** CABLE_NEUTRAL_PLUM was a comment-explained inline tuple; Naomi correctly flagged it as breaking the traceability pattern. Named constant + palette entry = complete registration. Comment alone is not enough.
- **A compliance checklist for naming conventions is more actionable than the spec doc alone.** The naming_conventions.md is clear and correct. Zero compliance means the team needs a fast pre-save checklist, not a better spec. Checklist created at output/production/naming_convention_compliance_checklist.md.
- **CHAR-L-08 finalized.** HOODIE_AMBIENT (#B06040) = HOODIE_SHADOW (#B84A20) + DUSTY_LAVENDER (#A89BBF) at 70/30 blend. Shadow Plum interim removed. The hoodie underside must retain orange-material identity even under cool ambient.

## Cycle 10 Lessons
- **Derivation arithmetic must be verified, not assumed.** CHAR-L-08 (#B06040) had a 16-point blue channel error vs. the stated 70/30 formula. Corrected to #B36250 (179,98,80). Always verify blend arithmetic against the formula result, not just the qualitative look.
- **Palette strip accent markers are essential for key readability.** Key 01 now marks Cyan as "Cy*" and Deep Shadow as "Dk*" — matching the Key 02 "Mag*" pattern. Viewers of color keys must immediately know which swatches are dominant fills vs. accents.
- **Cross-references between documents must be in both directions.** luma_color_model.md now cites master_palette.md Section 7. Every documentation link should be traceable both ways to prevent the "one document knows, the other doesn't" failure.
- **Generator header is the cycle log.** Always update the header comment at the start of each cycle — it is what future agents read first when they restart.

## Cycle 11 Lessons
- **Arithmetic in comments must be verified against the formula, not assumed.** The "near-zero alpha at boundary" comment in draw_lighting_overlay() was wrong. Actual: alpha=30 (~11.8%) at the 80px overlap zone. When writing an analysis comment, always run the formula for the boundary case explicitly: t≈0.49, alpha=int(60*(1-0.49))=30. Document the arithmetic step-by-step in the comment so reviewers can verify.
- **11.8% cold overlay over warm skin = valid split-light cross-light effect.** cold_alpha_max=60 is visually correct — the warm-to-cool gradient at the boundary reads as intentional atmospheric separation, not contamination. Decision retained and documented.
- **Style guide Color System section must be paint-ready, not referential.** The Color System section in style_guide.md must be actionable: tables of what to paint when, a decision flowchart, explicit forbidden lists per world. Painters should not need to read master_palette.md to make a correct color call on a standard scene.

## Cycle 12 Lessons
- **Jordan Reed completed major naming compliance pass** before Sam's cycle — turnarounds, style frames, color model swatches, env assets now have LTG_* counterparts. Always check checklist for prior work before duplicating.
- **SF02 Glitch Storm color key PNG generated.** `LTG_COLOR_colorkey_glitchstorm_v001.png` — dutch angle (4°) applied, storm confetti NO Acid Green per Forbidden #8, Byte amber outline exception rendered, three-tier street lighting shown (Cyan from crack / Magenta fill / Warm Gold windows).
- **Color support docs are a first-class deliverable.** When new assets are in development by other team members, a color support doc (conditional palette entries, consistency checks, figure-ground warnings) is valuable even before those assets are rendered.
- **CHAR-L-09 conditional entry pending.** If Alex Chen uses warm-side pixel activation on hoodie in SF01 visual surprise, register CHAR-L-09 = `#E8C95A` (Soft Gold warm pixel activation). Check next cycle.
- **DRW-16 painter warning still outstanding** (Luma shoulder under Data Stream Blue waterfall, `#9A7AA0`). Must be added to luma_color_model.md. Carried forward since Cycle 7.
- **luma_color_model.md does not yet have a DRW-16 warning.** Add to luma.md Section 3 (or color model) next available cycle.

## Cycle 13 Lessons
- **C10-1 RESOLVED.** Cold overlay boundary arithmetic was wrong in prior cycles ("near-zero/3.5%"). Actual: at x=880 (80px boundary), t≈0.50, alpha=int(60×0.50)=30 (~11.8%). Visual decision: cold_alpha_max=60 retained — ~12% cold cyan over warm skin is a valid split-light cross-light effect. Documented in master_palette.md Section 1B as C10-1 RESOLVED.
- **DRW-16 RESOLVED.** Painter warning added to luma_color_model.md (shoulder under Data Stream Blue waterfall, #9A7AA0). Cross-reference now bidirectional: master_palette.md DRW-16 ↔ luma_color_model.md.
- **DRW-07 saturation fix.** Storm hoodie #C07A70 RGB(192,122,112) had saturation below background walls. Corrected to #C8695A RGB(200,105,90), HSL≈50% saturation. Updated in both SF02 scripts.
- **Warm spill alpha canonical: 40/255 (~16%).** Color key generator used alpha=150 (~59%) vs SF02 bg script alpha=40. Aligned to 40 — the correct value for a subtle background window spill under dominant cyan storm key.
- **ENV-06 corrected by Jordan Reed.** Old #9A8C8A (R dominant — reads warm, wrong for cyan key). New #96ACA2 (G>R, B>R — correctly cool). Applied in color key generator; SF02 bg generator still needs updating (note added to master_palette.md for Jordan).
- **CHAR-L-09 warm pixel activation still pending.** Message sent to Alex Chen inbox 2026-03-30 14:00. If Alex confirms, register as CHAR-L-09b or CHAR-L-11 in master_palette.md Section 5 (hex #E8C95A). Current CHAR-L-09 = shoe canvas (Cycle 9).

## Cycle 14 Lessons
- **CHAR-L-11 REGISTERED.** Alex Chen confirmed (2026-03-30): Luma Hoodie Pixel (Warm-Lit Activation), hex #E8C95A (Soft Gold, alias RW-02). Added to master_palette.md Section 5. Constraints: lamp-lit hoodie pixel accents only, warm-dominant scenes only; neutral/cold scenes use GL-01 (#00F0FF). CHAR-L-09 thread closed — correctly occupied by shoe canvas.
- **SF03 Other Side color key complete.** Planning doc at `/output/color/LTG_COLOR_colorkey_otherside_v001.md`. PNG at thumbnails/LTG_COLOR_colorkey_otherside_v001.png. Generator at tools/LTG_TOOL_colorkey_otherside_gen_v001.py. Zero warm light sources — Electric Cyan dominant key, Void Black base, UV Purple atmosphere. Maximally distinct from SF01/SF02.
- **GL-01 vs GL-01b clarification re task brief.** Task brief cited #00D4E8 as "Electric Cyan" — that is actually GL-01b (Byte Teal). True GL-01 is #00F0FF. SF03 color key uses #00F0FF for ambient key; noted in planning doc. Byte uses #00D4E8 as fill per production spec.
- **SF03 colorkey generator pattern.** All inline tuples named. Dutch angle NOT applied (level — stillness is the mood). No warm light sources anywhere in generated image. Five depth zones: Void Sky / Far Distance / Mid Distance / Platform / Abyss.
- **Colorkey_glitchstorm ENV-06 VERIFIED.** LTG_TOOL_colorkey_glitchstorm_gen_v001.py has TERRACOTTA_CYAN_LIT = (150, 172, 162) — correct, matches SF02 v002. No regeneration needed.
- **Classroom color key notes complete.** `LTG_COLOR_colorkey_classroom_v001.md` — warm neutral daylight (Soft Gold key) + cool fluorescent (Dusty Lavender secondary). Zero Glitch contamination. Hoodie pixels = Warm Cream (dormant) in this pre-discovery scene — the Cyan activation IS the story beat.
- **Hoodie pixel dormancy rule.** Pre-discovery scenes: hoodie pixels = Warm Cream #FAF0DC (dormant). Discovery/Glitch scenes: Soft Gold #E8C95A (warm-lit) or Cyan #00F0FF (Glitch-lit). This color shift IS the visual narrative beat for the activation moment.

## Cycle 15 Lessons
- **SF03 palette audit is complete.** All colors in the spec are mapped to master palette entries. Two new entries added: DRW-18 (Luma Hair Glitch Layer, #1A0F0A) and ENV-13 (Far Structure Edge Void-Scale, #211136). No other undocumented values found.
- **Figure-ground: SF03 PASSES.** Luma's orange hoodie (#C07038) against UV Purple (#7B2FBE) is near-complementary. Strong contrast. No intervention needed. Byte reads as dark form with cyan glow against UV Purple — no amber outline (UV-dominant, not cyan-dominant).
- **Warm-light prohibition: SATISFIED.** All warm colors in SF03 are material/pigment. Corrupt Amber must be crack-line strokes only on fragments — NOT soft radial glow. Radial amber glow would read as a warm light source, violating the rule.
- **Classroom BG generator palette is clean.** WALL_SAGE #8A9E8A (muted sage) is correct per millbrook_school.md — overrides my Warm Cream approximation. SHADOW_COOL #7A9080 is an unlisted construction value but is warm-safe (G>R). Zero Glitch contamination.
- **millbrook_school.md is the color authority for classroom walls.** My color key was an approximation. Always check scene-specific reference docs before writing color keys.
- **ENV-13 distinction from depth-tier FAR_EDGE:** They share the same name but are different derivations. ENV-13 = purple-over-void (#211136). Depth-tier FAR_EDGE = cyan-derived (#002837). Document the distinction explicitly every time.

## Cycle 16 Lessons
- **Shadow drift causes body-fill misread.** BYTE_SH was #0090B0 (too dark, grey-shifted). Naomi perceived the body fill as Electric Cyan — actually the wrong shadow was causing the contrast imbalance. Fixing shadow to GL-01a #00A8C0 restores the correct read. Always check shadow companion when body fill is questioned.
- **ALARMED = cold/danger background.** Warm cell background on ALARMED expression was a semantic inversion. Rule: danger/alarm states use cold or neutral backgrounds. Warm backgrounds communicate comfort and Real World safety.
- **Faceplate must derive from body_ry, not fixed s fraction.** When body_squash varies per expression, a fixed s//4 eye_size causes faceplate to appear over/under-scaled. Always derive eye_size from the actual rendered body dimension (body_ry) to keep faceplate-to-head ratio consistent.
- **ENV-06 was already correct in SF02 v002.** Verify against the actual script before applying fixes — the v002 generator already had the Jordan Reed Cycle 13 fix. The outstanding note in master_palette.md referenced v001 only.
- **DRW-07 #C8695A now in v002.** Was (192,122,112) — corrected to (200,105,90). Both scripts updated. Issue resolved.
- **SF03 DRW-18 UV rim IS in the generator** (HAIR_UV_SHEEN = UV_PURPLE on crown). Naomi's concern was execution scale — the sheen may be too narrow to read at final render scale (~216px figure height). Flagged to Alex/Jordan for v002 geometry increase.
- **SF03 confetti physics flag.** Confetti distributed W×H full canvas — some particles will be mid-air with no source proximity. For v002: constrain to within 150px of platform or characters.

## Carry Forward
- ENV-06 (#96ACA2) not yet updated in LTG_TOOL_style_frame_02_glitch_storm_v001.py v001 (TERRA_CYAN_LIT still old value). v002 is correct. Coordinate with Jordan Reed on v001 if it is still used.
- SHADOW_COOL #7A9080 in classroom generator: Jordan should add inline comment on next revision pass (low priority).
- SF03 v002 pass items (Jordan/Alex scope): data waterfall luminance, depth tier collapse upper-right, pixel-plant size, Byte shoulder legibility confirmation.
