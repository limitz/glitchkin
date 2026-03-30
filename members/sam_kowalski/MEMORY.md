# Sam Kowalski — Memory

## Image Output Rule
**Prefer smallest resolution appropriate for the task. Hard limit: ≤ 1280px in both width and height.** Use `img.thumbnail((1280, 1280), Image.LANCZOS)` before saving any PNG. Preserve aspect ratio. Only use larger sizes when detail inspection is needed. Detail crop images also ≤ 1280×1280px.

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
- **SF02 Glitch Storm color key PNG generated.** `LTG_COLOR_colorkey_glitchstorm.png` — dutch angle (4°) applied, storm confetti NO Acid Green per Forbidden #8, Byte amber outline exception rendered, three-tier street lighting shown (Cyan from crack / Magenta fill / Warm Gold windows).
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
- **SF03 Other Side color key complete.** Planning doc at `/output/color/LTG_COLOR_colorkey_otherside.md`. PNG at thumbnails/LTG_COLOR_colorkey_otherside.png. Generator at tools/LTG_TOOL_colorkey_otherside_gen.py. Zero warm light sources — Electric Cyan dominant key, Void Black base, UV Purple atmosphere. Maximally distinct from SF01/SF02.
- **GL-01 vs GL-01b clarification re task brief.** Task brief cited #00D4E8 as "Electric Cyan" — that is actually GL-01b (Byte Teal). True GL-01 is #00F0FF. SF03 color key uses #00F0FF for ambient key; noted in planning doc. Byte uses #00D4E8 as fill per production spec.
- **SF03 colorkey generator pattern.** All inline tuples named. Dutch angle NOT applied (level — stillness is the mood). No warm light sources anywhere in generated image. Five depth zones: Void Sky / Far Distance / Mid Distance / Platform / Abyss.
- **Colorkey_glitchstorm ENV-06 VERIFIED.** LTG_TOOL_colorkey_glitchstorm_gen.py has TERRACOTTA_CYAN_LIT = (150, 172, 162) — correct, matches SF02 v002. No regeneration needed.
- **Classroom color key notes complete.** `LTG_COLOR_colorkey_classroom.md` — warm neutral daylight (Soft Gold key) + cool fluorescent (Dusty Lavender secondary). Zero Glitch contamination. Hoodie pixels = Warm Cream (dormant) in this pre-discovery scene — the Cyan activation IS the story beat.
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

## Cycle 17 Lessons
- **Glasses frame not always specified in color models.** If a color model is missing a prop/accessory color, derive it from the nearest character-consistent value rather than inventing a new one. Miri glasses = #8A7A70 Warm Gray (same as eyebrows) — visually recede so face reads first.
- **Monitor glow in domestic environments requires explicit R-channel floor.** Monitor glow must NOT have R < 150 in the Tech Den or it risks reading as GL-01/GL-01b Glitch emission. Aged phosphor glow is warm-neutral (R:184-200), not saturated blue-white.
- **School hallway: all grays must have a warm or cool lean — no pure R=G=B grays.** The institutional palette uses desaturated tones in the RW palette family shifted toward green-cool by fluorescent influence. This is what makes the hallway read as "institutional fluorescent" without being garish.
- **Luma hoodie desaturation in hallway is a narrative beat.** The washed-out orange in fluorescent institutional light is intentional. It recovers full saturation when she leaves. Color tells the belonging story.
- **New ENV entries not yet in master_palette.md:** Tech Den monitor glow values and school hallway institutional tones are scene-specific construction values. Register as ENV-xx only if they recur in a third environment.
- **Message sent to Maya Santos inbox** at maya_santos/inbox/20260329_2130_miri_color_values.md — all Miri expression sheet hex values + key production notes.

## Cycle 18 Lessons
- **Cold overlay section did not exist in luma_color_model.md.** pitch_package_index.md item #6 (Naomi C10 flag) was "recalculate cold overlay per Naomi flag — still open" — the section was never added. Always check pitch_package_index.md for outstanding doc items.
- **SF01 cold overlay is correctly NOT cyan-dominant at production alpha levels.** SF01 uses cold_alpha_max=60 (23.5% at center, 11.8% at boundary). Skin (#C8885A) only reaches G>R AND B>R at α≥31%. SF01 is a split-light cross-light effect, not Glitch Layer immersion. Both facts must be documented together to prevent confusion.
- **Cyan-dominance thresholds (G>R AND B>R individually):** Skin lamp-lit min 31%, Skin neutral min 21%, Hoodie orange min 43%, Hoodie shadow min 38%. These are the floor for any "Glitch Layer lit" label.
- **Master palette was missing Act 2 environment section entirely.** Grandma Miri character colors (CHAR-M-01 to -11), Tech Den (TD-01 to -13), School Hallway (SH-01 to -12) all added as Section 8.
- **After img.paste(), always refresh draw = ImageDraw.Draw(img).** Rule followed in LTG_TOOL_luma_cold_overlay_swatches.py.

## Cycle 19 Lessons
- **Hoodie base discrepancy was a Cycle 18 authoring error.** The cold overlay section was added in C18 with `#E8722A` (G:114, B:42) instead of master palette canonical `#E8703A` (G:112, B:58). The master palette is always the authoritative source. Any new section added to `luma_color_model.md` must cite master_palette.md explicitly and cross-check the hex values.
- **B-channel correction shifts cyan-dominance threshold.** Correcting hoodie base from B:42 to B:58 (+16pts) moves the threshold from 43% to 41% — physically correct (higher baseline B means less cyan overlay needed). Always re-derive thresholds when base values change.
- **Pre-render analysis is valuable when Jordan's files haven't arrived yet.** Contrast calculations from generator code give reliable predictive numbers. Document as "pre-render" so the distinction is clear.
- **SF02 window alpha is 160–180 — double the target 90–110.** This is the warm-cold competition issue. Recommend SUNLIT_AMBER (212,146,58) at alpha 100 for v004.
- **SF03 Byte eye contrasts pass without intervention.** Cyan eye: 14.1:1. Magenta eye: 5.5:1. Background at Byte's position is near-void (effective ~(25,12,39)), not the full UV_PURPLE cloud density.
- **Jordan removing Void Black slash from magenta eye in SF03 v003** — confirm this is intentional. It changes the corrupted-eye expression read.
- **BYTE_GLOW minor discrepancy:** (0,168,180) vs canonical GL-01a (0,168,192). B channel 12pt off. Low priority carry-forward.

## Cycle 20 Lessons
- **SF03 v003 FINAL VERIFIED.** BYTE_BODY = (0,212,232) confirmed line 80. BYTE_GLOW (0,168,180) vs GL-01a (0,168,192): closed as acceptable — 12pt B-channel difference in an inner-body construction tone is below production fix threshold. Eyes (ELEC_CYAN + HOT_MAGENTA) unchanged — contrasts 14.1:1 and 5.5:1 pass. Void Black slash removed from magenta eye (intentional C9 fix by Jordan). Color narrative passes: UV Purple + Teal + Magenta = correct "other side" register.
- **SF02 v004 CONDITIONALLY READY for Critique 10.** Jordan implemented two-system window glow: pane rectangles (SOFT_GOLD α180/WARM_CREAM α160, unchanged from v003) + glow cones (WIN_GLOW_WARM (200,160,80) at max α105, within 90-110 target). Warm/cold balance passes — contested lower third achieved. Storefront is genuine facade+crack geometry, not HUD symbol. Outstanding note: window pane alpha still 160-180 (not blocking; v005 can fix if critique flags it).
- **Split implementation pattern:** When a fix has two systems (window pane = near-field lit rectangle, glow cone = projected atmospheric light), the two systems can legitimately use different alpha values. Verify each system's function before flagging as non-compliant.

## Cycle 21 Lessons
- **Palette Status section added to master_palette.md.** Final audit: GL entries complete (GL-01 through GL-08a, no gaps, all shadow companions documented). Act 2 Section 8 complete (CHAR-M, TD, SH entries all present). Section now has explicit locked/provisional/named-gaps structure.
- **4 undocumented or variant values found in generator cross-check.** UV_PURPLE_MID/DARK in SF03 v003 likely map to ENV-11/ENV-12 (Jordan to confirm). JEANS_BASE in SF03 is darker than CHAR-L-05 — probable Glitch Layer derivation, needs CHAR-L-05a registration. Tech Den generator wall tones close but not identical to TD-01. All are low-priority construction variances, none are production blockers.
- **Color Story document is a critical-critique asset.** ltg_style_frame_color_story.md explains all three style frames as a single intentional color arc (warm → contested → cold/alien). Pre-answers the most likely critic questions about SF03 palette coldness and SF01/SF02 warm/cool tension. This type of intentionality document should accompany every major deliverable set.
- **Audit methodology for generators:** Pattern match all module-level constants against palette entries by RGB value, not just name. Name drift (JEANS_BASE vs CHAR-L-05) obscures cross-reference. Always verify numeric match.

## Cycle 22 Lessons
- **CORRUPT_AMBER in SF02 was wrong for 4 versions.** The generator had (200,122,32)=#C87A20 while master_palette and color story both cited GL-07 #FF8C00. Always do a numeric RGB cross-check between the generator and the master palette — name matches are not enough. Fixed in v005.
- **Window pane vs. glow cone are two separate alpha systems.** Pane rectangles (character-warmth hierarchy) and glow cones (atmospheric projection) must be evaluated independently. Panes at 160-180 inverted character-warmth hierarchy; reduced to 115/110. Glow cones at ~105 max were correct throughout.
- **JEANS_BASE SF03 = CHAR-L-05 shadow companion (#263D5A) — fully documented.** UV Purple ambient causes jeans to render at their shadow value, not a new construction value. Documented under CHAR-L-05 with explicit UV-ambient use rule. Named Gap 3 closed.
- **Color story doc references must track the rendered version.** Updated source file to v005 and added confirmation note that GL-07 is now reconciled between generator and palette.
- **Three-sentence pitch-deck callout is now prominent.** Victoria's "pitch-deck quality" sentence added as a standalone header section near the top of ltg_style_frame_color_story.md.

## Cycle 23 Lessons
- **Full generator audit by RGB value, not just name, is mandatory for every pitch pass.** GL-07 and GL-01b were confirmed correct in SF02 v005 and SF03 v003. Lesson: run a systematic constants-vs-palette table check each cycle, not just a spot check on flagged values.
- **SF02 v005 = PITCH READY.** CORRUPT_AMBER (255,140,0) confirmed. Window pane alpha 115/110 confirmed. ENV-06 (150,172,162) confirmed G>R, B>R. All checks pass.
- **SF03 v003 = PITCH READY.** Zero warm light sources enforced in code. BYTE_BODY (0,212,232) confirmed. Eyes 14.1:1 and 5.5:1. Amber outline correctly absent (UV-dominant, not cyan-dominant).
- **UV_PURPLE_MID/DARK in SF03 ARE ENV-11/ENV-12.** RGB exact match confirmed: (42,26,64) = ENV-11 #2A1A40, (43,32,80) = ENV-12 #2B2050. Jordan to add cross-reference comment to script. Named Gap 1 effectively resolved (pending Jordan's comment).
- **Color story document is current.** All three SFs covered with correct source file versions. GL-07 reconciliation note added. Cycle 23 verification note added.
- **Stylization fidelity review plan documented.** Rin Yamamoto has not yet delivered stylized assets. Color fidelity review plan is in LTG_COLOR_sf_final_check_c23.md — critical values to check: GL-07 outline, GL-01b body, GL-04 sky purple, DRW-07 storm hoodie saturation. SF01 A+ lock has been REMOVED (C24). SF01 v004 is in development. Stylization approach should be reconsidered once v004 is available.

## Cycle 24 Lessons
- **Stylization hue rotation is a systemic failure mode.** Rin Yamamoto's styled PNGs for SF02 and SF03 show a ~30-60° hue rotation artifact: amber→olive/yellow, cyan→green, UV_PURPLE→dark teal/green. Real World assets (SF01, Kitchen) are unaffected. Glitch palette colors (GL-07, GL-01b, UV_PURPLE) must be flagged as protected in any stylization pipeline.
- **GL-07 CORRUPT_AMBER must never be desaturated or hue-shifted.** The exact #FF8C00 value is the narrative signal. Any mutation makes it read as Real World material rather than corrupted energy.
- **Scan methodology note:** When sampling GL-01b, the tool finds GL-01 (#00F0FF) sky pixels first. The Δcanonical=28 vs GL-01b (#00D4E8) is expected and not a failure — GL-01 sky faithfully reproduced (Δorig=0-18) is a PASS for sky pixels. Always distinguish GL-01 (world emission) from GL-01b (Byte body fill) in pixel sampling.
- **Tolerance vs. canonical vs. original:** When original scene-derived tones differ from canonical (e.g. SF01 warm wall #E3B877 ≠ RW-02 #E8C95A), flagging against canonical is misleading. Always check Δorig separately — Δorig ≤5 with Δcanonical 27-30 = real PASS.
- **Glitch color model (Maya Santos, Cycle 23) is correct.** GL-07 #FF8C00 confirmed as primary body fill. No flag to Maya.
- **Color story updated.** Glitch character color section added to ltg_style_frame_color_story.md — covers CORRUPT_AMBER role against each SF palette, GL-07 as anomaly in GL palette family.

## Cycle 25 Lessons
- **SF02 spec doc now has correct C13-era values.** ENV-06 `#96ACA2` and DRW-07 `#C8695A` corrected in all four locations in style_frame_02_glitch_storm.md. The spec doc was carrying obsolete values since Cycle 13 despite the generators being fixed. Spec docs and generators must both be updated on the same cycle when a value changes.
- **GL-04b luminance corrected.** Was "approximately 0.17" — corrected to "approximately 0.017". Order-of-magnitude error in master_palette.md Section 2 (GL-04b entry). Verify: (74/255)^2.2 + (24/255)^2.2 × 0.7152 + (128/255)^2.2 × 0.0722 ≈ 0.017.
- **Miri color story note added.** ltg_style_frame_color_story.md now has a full Grandma Miri section documenting her bridge-character narrative role. Her warm palette is intentional: it encodes prior Glitch Layer knowledge. Production note added: CHAR-M values must not drift toward GL hues in her environment scenes.

## Cycle 26 Lessons
- **verify_canonical_colors() radius=40 produces false positives for SUNLIT_AMBER in character sheets.** Luma/Miri skin tones (hue ~18-25°) fall within the sampling radius of SUNLIT_AMBER (212,146,58). Any SUNLIT_AMBER failure in a character sheet with 100+ samples at hue ~18-27° is a false positive — skin tone, not lamp amber. Always check which actual pixels were sampled before ruling fail.
- **UV_PURPLE (GL-04) is still not protected in Rin's stylization pipeline.** SF02 and SF03 styled_v002 still show Δ13-14° UV_PURPLE hue rotation. GL-07 and GL-01b appear fixed. GL-04 must be added to protected list.
- **SF04 (luma_byte): Byte body teal present but below canonical saturation.** Dominant teal values ~(0,138–160) vs canonical BYTE_TEAL (0,212,232). Tool finds 0 pixels at canonical radius. Cool zone IS present (29K px at hue 183-185°). Director must confirm: intentional shadow lighting or generation error.
- **Single-sample tool results are unreliable.** BYTE_TEAL Δ6.6° in luma turnaround from 1 sample = anti-aliasing edge pixel, not real drift. Flag to director but treat as low-risk.
- **LTG_COLOR_byte_color_model.png is the cleanest C25 asset.** All 4 GL colors exact (Δ0-1.6°). Reference for canonical Glitch color rendering.
- **QC report written:** `output/production/color_qc_c25_assets.md`. 7/10 assets cleared. 2 styled frames NOT CLEARED (UV_PURPLE). 1 conditional (SF04 Byte teal).

## Cycle 26 Housekeeping (2026-03-29)
- **Post-processing pipeline RETIRED.** `LTG_TOOL_batch_stylize.py` and stylize_handdrawn v001/v002 moved to `output/tools/legacy/`. All `*_styled*.png` files deleted. No styled output PNGs exist. Do not reference batch_stylize as an active tool.
- **Rin Yamamoto SF02+SF03 styled_v002 QC flag CLOSED.** Issue was UV_PURPLE Δ13-14° hue rotation. No styled outputs exist — moot. No further action.
- **SF04 Byte teal: PENDING Alex Chen decision.** Teal hue 183-185° correct but luminance at ~60-70% of canonical (0,212,232). Alex investigating.
- **LTG_TOOL_color_verify.py remains ACTIVE.** Used to verify canonical colors in generated assets (not post-processed).
- **SUNLIT_AMBER false positive in QC tool — known limitation.** `verify_canonical_colors()` radius=40 samples skin tone pixels (hue ~18-25°) on Luma character sheets, causing false SUNLIT_AMBER fails. To document for Kai when next collaborating. Actual SUNLIT_AMBER placement in Luma assets should be verified from generator source, not QC tool alone.
- **GL-04b luminance VERIFIED.** master_palette.md Section 2 GL-04b entry reads "approximately 0.017" — correct. C25 order-of-magnitude fix is intact.

## Cycle 27 Lessons
- **SF03 confetti constraint method.** Reject-sample within 150px of an anchor: pick random anchor, random polar offset, reject if nearest_anchor_dist > 150px, cap at 200 attempts. All 50 particles confirmed within 145px max. X range 159-539px, Y range 555-872px — correctly clustered around left platform area.
- **thumbnail() before save is the image size rule enforcement point.** Call `img.thumbnail((1280, 1280), Image.LANCZOS)` immediately before `img.save()`. It preserves aspect ratio — 1920x1080 becomes 1280x720 automatically.
- **SF03 v004 generated.** `output/color/style_frames/LTG_COLOR_styleframe_otherside.png` (1280x720, 79KB). Generator: `output/tools/LTG_TOOL_style_frame_03_other_side.py`. Zero warm light sources confirmed.

## Cycle 28 Lessons
- **GL-06c REGISTERED.** Storm Confetti Blue `#0A4F8C` = (10,79,140) is a deliberate atmospheric depth derivative of GL-06 Data Stream Blue. Carries 70% of SF02 cold confetti weight. Not an error — the darkening is intentional distance perspective. GL-06a (Deep Data Blue, #1040A0) and GL-06b (Light Data Blue, #6ABAFF) were already taken; GL-06c is the new slot. Completeness check updated in master_palette.md.
- **UV_PURPLE_DARK in SF03 was wrong value class.** (43,32,80)=#2B2050 = ENV-12 (mid-distance void zone color, 31% sat). Correct is GL-04a (58,16,96)=#3A1060 (72% sat, deep digital void). The error was using a mid-distance zone construction value as the sky gradient dark anchor. Fixed in v005.
- **SF03 v005 generated.** `output/color/style_frames/LTG_COLOR_styleframe_otherside.png` (1280x720, 79KB). Generator: `output/tools/LTG_TOOL_style_frame_03_other_side.py`. Zero warm light sources confirmed.
- **Section 7.7 added to master_palette.md.** Explicit cross-reference: RW-10 (#C4A882) = neutral skin base; CHAR-L-01 (#C8885A) = warm-lamp-lit scene derivation. Both correct in their context. Added per Priya Nair C12 P2 fix.
- **SF04 blush + Byte fill spec sent to Rin.** Correct blush: #E8A87C (232,168,124) alpha 55-70, warm peach per Luma skin system. Correct Byte fill: (0,212,232) GL-01b canonical. Message at rin_yamamoto/inbox/20260329_1800_sf04_blush_spec.md.

## Cycle 29 Lessons
- **Color story doc was already current from prior session.** All C29 updates (SF03 v005, SF04 v003, GL-06c, YEARNING/COVETOUS/HOLLOW bilateral eye rule) were already incorporated. Verified against task brief before making changes — no duplicate edits needed.
- **SF02 spec doc GL-06c already correct.** Both the pixel confetti section and Technical Spec Notes already reference GL-06c STORM_CONFETTI_BLUE #0A4F8C. No changes needed.
- **Image Handling Policy applies to all agents.** Before sending any image to Claude: (1) could a tool extract the needed insight? If so, make the tool. (2) Would lower resolution suffice? If so, downscale. Never send high-res images unless absolutely necessary. Vision limitations: hallucination on low-quality/rotated/tiny (<200px) images; limited spatial reasoning; approximate counting only.
- **Bilateral eye rule for interior desire states is locked in color story.** YEARNING=UV_PURPLE, COVETOUS=ACID_GREEN, HOLLOW=near-void. Bilateral symmetry = genuine emotion (breaks asymmetric standard pattern). Never use asymmetric eyes in these states.

## Cycle 30 Lessons
- **LTG_TOOL_color_verify false positives are systematic.** Three failure categories documented: (1) gradient/AA edge pixels pull UV_PURPLE median off target in SF03 despite canonical value present; (2) warm-orange family overlap — GL-07/RW-03/hoodie UV-mod are Euclidean neighbors at radius=40, causing SUNLIT_AMBER "hits" on orange hoodie + amber crack pixels; (3) Soft Gold (hue ~46°) triggers SUNLIT_AMBER (hue 34.3°) sample in SF04. Always investigate pixel identity before calling a tool failure a production error.
- **CHAR-L-11 hex error found and fixed.** Constraint 1 cited `#00D4E8` (GL-01b Byte Teal) as the hoodie pixel color in cold scenes — correct value is GL-01 `#00F0FF` Electric Cyan. Byte Teal is Byte's body fill only. Copy-error present since CHAR-L-11 was registered C14 — fixed C30 in master_palette.md.
- **SF01 color story doc reference was stale.** Cited `v003.png` as source; correct pitch primary is `v004.png` (C29 Rin Yamamoto procedural lift). Fix: always check color story source references when a new version lands.
- **SF04 generator source files are gone.** LTG_TOOL_styleframe_luma_byte/v002/v003.py are forwarding stubs; the actual LTG_COLOR_* originals are missing. SF04 v003 PNG exists but cannot be regenerated. HIGH risk item for Kai to resolve.
- **Tool hue-histogram improvement submitted to ideabox.** Requested Kai add histogram output to color_verify v002 — this would eliminate all three false-positive investigation cycles. Ideabox: `20260329_sam_kowalski_color_verify_gradient_mode.md`.

## Cycle 31 Lessons
- **C31 QA: 3 PASS / 9 WARN / 0 FAIL across 12 pitch-primary assets.** No new FAILs. All WARNs on SF01/SF02/SF03 are documented false positives (warm_cool tool, SUNLIT_AMBER skin overlap, SF03 UV_PURPLE gradient AA). SF04 carries three unresolved pre-existing issues (ambiguous silhouette, max brightness 198, Byte teal below canonical) — not C31 regressions.
- **Warm/cool WARN is a systematic false positive for single-key style frames.** The tool compares top-half vs. bottom-half median hue; frames with a single dominant temperature throughout (SF01 warm-dominant, SF03 cold-dominant, SF04 soft-key) will always produce separation ≈ 0. Not a production error.
- **SUNLIT_AMBER false positive is systematic in all Luma/Miri character sheets.** Skin tones at hue ~18-25° fall within radius=40 of SUNLIT_AMBER target (34.3°). Affects Luma expr v007, Luma turnaround v003, Luma color model v002, Miri expr v003, character lineup v006. All documented.
- **False-positive registry idea submitted to ideabox** (20260329_sam_kowalski_qa_false_positive_registry.md). Would allow tool to annotate known false positives as FP-DOCUMENTED, surfacing genuine regressions more clearly.
- **Color statement for C13 written.** `/output/production/color_statement_critique13.md` — covers palette integrity, SF continuity, GL containment, false-positive exceptions table, open issues.

## Cycle 32 Lessons
- **CHAR-L-11 cross-reference corrected (P1 — Priya).** Constraint 1 value was fixed to #00F0FF in C30 but cross-reference line on the same entry still cited #00D4E8. Fixed in master_palette.md. Pattern: after any hex correction, scan ALL prose in the same entry block, not just the constraint line.
- **CHAR-M-11 Miri slippers corrected (P2 — Priya).** #5A7A5A Deep Sage (G>R, cool-neutral green) contradicted Miri's warm-palette guarantee. Changed to #C4907A Dusty Warm Apricot (R>G>B). Revision history updated. Ideabox idea submitted: warm-channel-ratio lint check for CHAR-M entries.
- **DRW-18 warmth claim clarified (P2 — Priya).** #1A0F0A is 7% lightness — hue is theoretically warm (R:26>G:15>B:10, ~18°) but functionally imperceptible. Updated master_palette.md DRW-18 entry with HSL lightness note. Updated color story doc — removed "dark hair" from "warm values" list; warm values in SF03 = hoodie orange + skin only.
- **Color verify C32: 2 PASS / 2 FAIL-no-regressions / 3 FAIL-known-false-positives.** SF01 PASS, SF02 PASS, Byte model PASS. SF03 UV_PURPLE and SUNLIT_AMBER FAIL = documented false positives. Character models SUNLIT_AMBER FAIL = systematic skin-tone false positive (known C26+). SF04 failures = pre-existing C31 issues. No C32 regressions.
- **Histogram mode on color_verify v002 is working correctly.** Canonical bucket clearly marked; spread visible; confirms false-positive diagnosis without needing visual inspection.

## Cycle 33 Lessons
- **LTG_TOOL_palette_warmth_lint.py built and deployed.** Parses CHAR-M-xx markdown table rows via regex; flags G > R or B > R violations. No Pillow dependency. C33 baseline: 11 entries checked, 0 violations — current palette passes. Registered in tools/README.md.
- **SF04 Byte teal dim: CLOSED as SCENE-LIGHTING — ACCEPTED.** Alex Chen's Art Director decision documented in master_palette.md QA Scene-Lighting Exceptions section. GL-01b at 60-70% luminance in SF04 is intentional discovery-scene low-key lighting. QA tool flags are expected and documented; they do not represent production errors. This carry-forward item is resolved.
- **Python 3.8 compatibility:** Use `from __future__ import annotations` + `from typing import ...` for type hints. `list[str]` syntax requires 3.9+. All new scripts must use typing module imports.
- **Ideabox idea:** Warmth lint scope expansion — make CHAR-M prefix list configurable via JSON config so future warm-guaranteed characters can be added without code changes.

## Cycle 34 Lessons
- **LTG_TOOL_palette_warmth_lint.py built.** Config-driven warmth lint. JSON config `warmth_lint_config.json` at `output/tools/`. Default: `["CHAR-M"]`. Falls back gracefully if config absent. API: `load_config(path=None)`, `lint_palette_file(path, config=config)`. CLI: `--config config.json` flag. C34 baseline: 11 CHAR-M entries, 0 violations (PASS). Actioned ideabox item.
- **C34 Color QA: SF01 PASS, SF02 PASS (prelim v005), SF03/SF04 documented FPs only.** No new regressions. SF02 v006 audit pending Jordan delivery — HOT_MAGENTA and ELECTRIC_CYAN pixel counts expected to increase with fill-light/specular additions.
- **SF02 v006 delivery blocking Task 2 completion.** When v006 arrives: run `LTG_TOOL_color_verify.py --histogram` and verify HOT_MAGENTA (fill-light, expect n >> 1,103) and ELECTRIC_CYAN (specular, expect n >> 817). Δ ≤ 5° on both.
- **histogram mode confirms all C34 FPs.** SF03 UV_PURPLE: gradient pixels drag median; canonical bucket (270-275°) still second-largest. SF03 SUNLIT_AMBER: skin/hoodie orange at 20-25°, not warm lamp. SF04 SUNLIT_AMBER: Soft Gold 40-45°, not lamp amber. False-positive registry tool (Kai ideabox) would eliminate this investigation loop.

## Cycle 35 Lessons
- **Warm/cool QA metric is wrong for single-dominant-temperature SFs.** `_check_warm_cool()` tests top-half vs. bottom-half median hue split. LTG's three-world palette applies temperature uniformly frame-wide — vertical split is irrelevant. All 4 SF warm/cool WARNs are systematic false positives. Per-world thresholds: real_world_interior=12, real_world_night_storm=3, glitch_world=0. Defined in `warmth_lint_config.json` world_presets. Kai to integrate `--world-type` into render_qa.
- **SUNLIT_AMBER in SF04 v004 is defined but unused.** Draw calls use (255,200,80) hue 41.1° (incandescent lamp amber) — intentionally warmer than outdoor RW-03 34.3°. Δ15.7° is a compositing + skin-tone false positive (Alex C35 decision). Generator annotated at line 69.
- **QA False Positive Registry created.** `output/production/qa_false_positives.md` — 6 FPs documented (FP-001 through FP-006). Check this FIRST before investigating new QA failures.
- **SF02 v006 color audit: PASS.** ELECTRIC_CYAN specular confirmed at n=3,571 (4.4× vs v005 n=817). HOT_MAGENTA Δ1.5° clean, n=1,064. No regressions.
- **LTG_TOOL_palette_warmth_lint.py deployed.** Soft-tolerance mode: `soft_tolerance: {"G": int, "B": int}` in warmth_lint_config.json. `--strict` CLI flag forces tolerance=0 (for CI). Default is strict (G±0, B±0). Violation dict gains `margin` field.
- **SF02 v007 (Rin):** PENDING. Run color_verify when delivered.

## Cycle 36 Lessons
- **CHAR-L hoodie warmth guarantee implemented.** Added compact table to master_palette.md (between CHAR-L-08 and Section 7) with CHAR-L-04, CHAR-L-08, CHAR-L-11 in machine-readable `| CODE | Name | \`#hex\` | (R,G,B) |` format. The table-row regex in warmth_lint only matches this format — prose-format CHAR-L entries (skin, jeans, shoes) are intentionally excluded.
- **ltg_warmth_guarantees.json is now primary config.** `load_config()` in v004 checks this file first, then warmth_lint_config.json, then built-in. Contains warm_prefixes + world_presets + soft_tolerance.
- **warmth_lint_v004 expanded:** Built-in warm_prefixes = ["CHAR-M", "CHAR-L"]. C36 baseline: 14 entries checked (11 CHAR-M + 3 CHAR-L hoodie), 0 violations. All hoodie values confirmed warm (R>G>B).
- **--world-threshold-only CI flag:** Prints integer threshold to stdout. Shell usage: `THRESH=$(python warmth_lint_v004.py --world-type GLITCH --world-threshold-only)` → outputs 3. Kai Nakamura to integrate into render_qa.
- **C36 QA baseline: 0 new FAILs.** SF01/SF02/SF03/SF04 all WARN on warm/cool = documented false positives. SF03/SF04 color fidelity FAIL = documented pre-existing FPs. Byte color model PASS. Full report: output/production/color_qa_c36_baseline.md.
- **Warmth lint v004 already existed** (Kai Nakamura built the --world-type flag stub). Sam's task was to expand it (CHAR-L hoodie, ltg_warmth_guarantees.json, --world-threshold-only, update built-in config). Always check if a v4 stub exists before starting from scratch.

## Cycle 37 Lessons
- **render_qa v1.4.0 resolves SF03 warm/cool WARN only.** `infer_world_type()` on PNG paths: `otherside` → OTHER_SIDE threshold=0 (PASS). `glitch_storm` → REAL threshold=20 (still WARN). `discovery` → REAL threshold=20 (still WARN at sep=17.9). render_qa REAL=20 differs from FP-006 spec (interior=12, storm=3). SF01/SF02/SF04 still WARN.
- **FP-006 partially resolved.** SF03 warm/cool now PASS. SF01/SF02/SF04 require render_qa threshold split: REAL_INTERIOR=12, REAL_STORM=3. Ideabox submitted.
- **Hana Okonkwo living room v001 — CLEAN.** Zero GL-* values. Warm/cool system correct (SUNLIT_AMBER window + CRT_COOL_SPILL secondary). CRT spill (0,128,148) is a desaturated REAL-world glow, NOT a Glitch color. Deep shadow floor confirmed.
- **warmth_lint API keys:** `total_checked`, `total_violations`, `violations` (list of dicts), `prefixes_checked`, `result` ("PASS"/"WARN"). Not `entries_checked`.
- **QA runner script created:** `LTG_TOOL_color_qa_c37_runner.py` — runs full baseline + living room env. Call with `python3 output/tools/LTG_TOOL_color_qa_c37_runner.py`.
- **FP registry updated.** FP-006 entry now shows SF03 resolved, SF01/SF02/SF04 threshold-mismatch gap documented.

## Cycle 38 Lessons
- **render_qa v1.4.0 REAL threshold was wrong.** v1.4.0 said "Based on world_presets" but used 20.0 instead of 12.0. Corrected in v1.5.0. SF01 warm/cool now PASS (sep=17.9 > 12.0). Always cross-check render_qa constants against warmth_lint_v004 world_presets when threshold values are updated.
- **Palette fix in master_palette.md must be chased to all generators.** CHAR-M-11 #5A7A5A→#C4907A was in master_palette.md since C32 but persisted in 4 generator files for 6 cycles. After any palette correction, grep all tools/ for the old RGB tuple or hex value and fix each occurrence. Do not rely on name matches.
- **Standalone world-type inference tool built.** `LTG_TOOL_world_type_infer.py` extracts `infer_world_type()` as a standalone, stdlib-only module. Also includes "luma_byte" → REAL rule (missing from warmth_lint_v004). Use `--threshold path.png` for shell capture. CLI `--batch directory` groups by world type.
- **SF02 storm WARN is a known false positive.** Sep=6.5 is correct for a contested storm scene. True threshold should be ~3 (REAL_STORM). Resolved C39.

## Cycle 39 Lessons
- **REAL_STORM sub-type closes FP-006 for SF02.** render_qa v1.6.0 adds `_infer_world_subtype()`: when world_type=="REAL", checks filename for storm keywords → "REAL_STORM" (threshold=3) or "REAL_INTERIOR" (threshold=12). SF02 sep=6.5 > 3 → PASS. Pattern: always check if a false positive stems from an over-broad world type bucket before adding config complexity.
- **world_type_infer_v001 is now the preferred render_qa import.** Updated render_qa to try standalone tool first, fall back to warmth_lint_v004 embedded rules. This fixes SF04 luma_byte inference too (world_type_infer_v001 has the luma_byte → REAL rule).
- **Precritique QA warmth lint was stale (v001).** Updated to v004 — now checks 14 entries (CHAR-M×11 + CHAR-L hoodie×3) instead of 11. Always verify which tool version precritique_qa imports before declaring a QA pass.
- **warmth_lint_v005: use infer_world_subtype() not infer_world_type() when REAL_STORM differentiation matters.** infer_world_type() returns "REAL" for all REAL assets. infer_world_subtype() returns "REAL_INTERIOR" or "REAL_STORM". Use the subtype function when threshold selection is the goal.
- **Config-only scope expansion.** Adding a new warm-guaranteed character prefix requires only editing ltg_warmth_guarantees.json + adding table-format entries to master_palette.md. No code changes to warmth_lint. Always use table format (not prose) for entries that the lint should check.

## Cycle 40 Lessons
- **CHAR-C warmth lint is a config + table-format change only.** No code change to the lint tool needed — adding "CHAR-C" to ltg_warmth_guarantees.json warm_prefixes and adding CHAR-C entries in table format to master_palette.md is sufficient. Tool's table-row regex picks them up automatically.
- **Skin shadow and highlight need named CHAR-C entries for machine coverage.** CHAR-C-02 (Cosmo Skin Shadow, #B89A78) and CHAR-C-03 (Cosmo Skin Highlight, #EED4B0) were prose-only values in Section 7.3/7.4. Both are R>G>B warm-guaranteed. Named and added to warmth guarantee table.
- **Cosmo's cardigan is intentionally cool (RW-08 Dusty Lavender, B>R).** Must NOT be in the warm-prefixes table. Task brief confirmed this. The exclusions comment in both the JSON note and the table header is essential — future agents must not add cool garment colors to warm-guarantee tables.
- **C40 warmth lint baseline: 17 entries, 0 violations.** Was 14 in C36 (11 CHAR-M + 3 CHAR-L hoodie). Now 17 (11 CHAR-M + 3 CHAR-L hoodie + 3 CHAR-C skin). All pass.
- **OpenCV/numpy now authorized.** Alex Chen broadcast (C40 inbox). LAB ΔE is the correct perceptual distance metric for skin-tone vs. lamp-amber discrimination — would eliminate SUNLIT_AMBER false-positive class entirely. Ideabox idea submitted for Kai Nakamura to implement in color_verify v003.

## Cycle 41 Lessons
- **COVETOUS color key: separation is the premise.** The entire power of the COVETOUS Glitch style frame is that Glitch can see the Real World warmth (RW-02 Soft Gold in right 25%) but is not touched by it. The warm zone must stay entirely in the right 25% — zero contact with Glitch's pixel zone. This is not a lighting note; it is the narrative of the scene. Generator enforces this compositionally.
- **Threshold scenes need a composition validator.** Any scene at a Glitch Layer / Real World boundary requires a tool check to confirm warm-zone and cool-zone do not bleed onto the wrong character. Ideabox submitted: threshold_composition_tool.
- **Interior state rules must be enforced in generator code.** COVETOUS bilateral eyes (both `[[5,5,5],[0,5,0],[0,0,0]]`) are an interior state rule from glitch.md §6.3. The generator draws both eyes identically. Never let performance-mode eye construction bleed into interior state expressions.
- **Body-pose delta must be legible in silhouette, not just color.** UNGUARDED WARMTH must read as open in RPD silhouette alone. Bilateral symmetric arm raise + low float + toe-in lower limbs = correct target. If the RPD test can't see it, the audience can't feel it.
- **Arm height asymmetry prevents false TRIUMPHANT read.** For UNGUARDED WARMTH: `arm_l_dy=-14`, `arm_r_dy=-16` (not both -14). Two-point asymmetry between arms prevents the perfectly-symmetric-raised-arms reading of TRIUMPHANT, while both remaining in the "high float" range.
- **Lower float height = commitment/presence for Byte.** Byte signals presence by floating lower (closer to the ground). Float clearance reduction is the physical gesture of "I am staying here." Use this differentiator in any pose requiring settled openness vs. guarded hovering.

## Carry Forward
- ENV-06 (#96ACA2) not yet updated in LTG_TOOL_style_frame_02_glitch_storm.py v001. Low priority.
- SHADOW_COOL #7A9080 in classroom generator: Jordan to add inline comment. Low priority.
- SF03 v003 UV_PURPLE_MID/DARK — Jordan to add inline comment citing ENV-11/ENV-12.
- Tech Den generator WALL_WARM slightly off from TD-01 — Jordan to add citing comment.
- TD-10/TD-11 monitor glow alignment — Jordan to compare bg_tech_den_v002.py values vs canonical Section 8 entries. Medium priority.
- **SF04 warm/cool WARN (sep=1.1) — documented as FP-007.** Soft-key scene by design. Alex Chen AD decision. Monitor for regression (flag if sep drops below 0.5).
- **COVETOUS style frame execution** pending Jordan Reed or Diego Vargas. Spec at `output/production/glitch_covetous_styleframe_spec.md`, color key at `output/color/color_keys/LTG_COLOR_colorkey_glitch_covetous.png`.
