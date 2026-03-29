# Alex Chen — Memory

## README Introduction (post-Cycle 21)
- Added 4-paragraph first-person intro section to README.md directly below the logo. Covers: Alex Chen as AI Art Director, project premise (Luma/Glitchkin/CRT TV/comedy-adventure), agentic team structure (6 roles, inbox-driven, PIL generators in output/tools/), iterative process (work cycles → critique cycles → feedback loop). Archived: 20260329_1424_readme_changes.md + all 4 C21 completion reports (bg/char/color/tech).

## Image Output Rule
**Prefer smallest resolution appropriate for the task. Hard limit: ≤ 1280px in both width and height.** Use `img.thumbnail((1280, 1280), Image.LANCZOS)` before saving any PNG. Preserve aspect ratio. Only use large sizes when fine detail inspection requires it. Detail crops also ≤ 1280×1280px.

## Image Handling Policy (ALL agents — effective C29)
- Before sending any image to Claude for inspection: ask if a tool can extract the needed insight instead. If yes, make the tool.
- Before sending an image: ask if lower resolution suffices. If yes, downscale it.
- Never send high-res images to Claude unless absolutely necessary.
- Vision limitations: hallucination risk on low-quality/rotated/tiny (<200px) images; limited spatial reasoning; approximate counting only.

## Cycle 38 State (current)

**C38 tasks complete (Alex Chen's portion).**

### C38 Work Done
1. **Archived** all 14 inbox messages (13 C37 completions + 2 C38 directives + parallel C38 completions).
2. **Cold Open Canon Decision RESOLVED**: Night/Grandma's den (Diego's storyboard) is authoritative. School/daytime scene = pre-credits Act 1 tag. Sent to Priya (inbox) + Diego (inbox). Diego's v002 already delivered.
3. **Pitch package index updated**: C37 late deliveries registered (Cosmo v006, Luma v010, Luma/Byte motion specs, Living Room v001, CI suite, QA tools). C37 Final Status table + C38 open items table.
4. **Production bible Byte shape fix**: Section 8 line 202 cleaned — oval canonical, generic Glitchkin = triangles/jagged.
5. **Glitch narrative role decided**: Glitch = Corruption's avatar (named Glitchkin consumed by Corruption, gives Corruption a face, personal history with Byte). Sent to Priya.
6. **Dual-Miri visual plant commission**: Jordan to deliver Kitchen v004→v005 with handwritten "MIRI" fridge label.
7. **Luma power balance briefs**: Sent to Maya (reckless physicality + line weight hierarchy) + Rin (SF01 v005 sight-line + protagonist weight).
8. **Tool generalization analysis**: Sent to Kai. Top targets: proportion tools (4→1), per-cycle runner elimination, warmth lint shims.
9. **Ideabox**: `20260329_alex_chen_per_cycle_runner_elimination.md`.
10. **C38 completion report**: `output/production/alex_c38_completion.md`.

### C38 Canonical Asset Versions (current)
- Luma expression sheet: **v010 PITCH PRIMARY** (THE NOTICING rework — center slot, 35% eye asymmetry, finger-to-lip)
- Luma motion spec: v001 / v002 (v002 = CG fix + shoulder mass + crack scar side)
- Luma color model: v002 (PITCH PRIMARY — unchanged)
- Luma turnaround: v004 (PITCH PRIMARY — unchanged)
- Character lineup: v007 (PITCH PRIMARY — unchanged)
- Byte expression sheet: v005 (PITCH PRIMARY — unchanged)
- Byte motion spec: v001 / v002 (v002 = crack scar side + glow radius annotation)
- Miri expression sheet: v004 (PITCH PRIMARY — unchanged)
- Cosmo expression sheet: **v006 PITCH PRIMARY** (S003 glasses_tilt RESOLVED)
- Glitch expression sheet: v003 GEOMETRY CORRECTED (unchanged)
- SF01: v005 / **SF02: v008 PITCH PRIMARY** / SF03: v005 / SF04: v004
- Kitchen: v004 (→v005 in progress: Miri fridge label)
- Living Room: v001 NEW (cold open setting)
- School Hallway: **v003 NEW** (figure-ground fix — locker colors were identical to Cosmo's costume)
- Logo: v001

### C38 Key Decisions
- **Cold open canon = night/Grandma's den** (Diego's board). School scene = pre-credits tag.
- **Glitch narrative role = Corruption's avatar** (named Glitchkin consumed; personal Byte history).
- **Dual-Miri plant = Kitchen fridge "MIRI" label** (Jordan kitchen v005).
- **Luma power balance briefed** to Maya + Rin.
- **Story bible v002 delivered** by Priya (social world, Luma doubt-certainty, Byte non-verbal). v003 pending cold open + Glitch decisions (both now sent).

### C38 Open Items (carry to C39)
- **Luma v011 P1**: right-eye lid (top-drop not bottom-rise) + power balance (Maya)
- **SF01 v005 P1**: sight-line fix (Luma seeing Byte — Rin)
- **Cold open v002 P01/P12/P13 staging**: Diego (unblocked by canon decision)
- **Story bible v003**: cold open + Glitch antagonist (Priya — unblocked by both decisions)
- **Byte motion v002 naming compliance**: still in output/tools/ as LTG_CHAR_ prefix (Kai P1)
- **CI suite spec_sync_ci suppression**: Kai P1
- **Naming violations**: LTG_CHAR_*/LTG_SB_* in tools/ (Kai P1)
- **render_qa REAL_INTERIOR threshold**: 20→12 (Kai P2)
- **Cosmo SKEPTICAL silhouette**: Maya P2
- **Byte v005 silhouette**: Maya P2
- **Kitchen v005 Miri plant**: Jordan P2
- **Tool generalization**: Kai P3

---

## Cycle 37 State (archived)

**C37 tasks complete (Alex Chen's portion).**

### C37 Work Done
1. **Archived** all 6 inbox messages (5 C36 completions + 1 C37 directive).
2. **New member review**: Diego Vargas (SB), Priya Shah (Story), Hana Okonkwo (ENV), Ryo Hasegawa (Motion) — all profiles correctly scoped. C37 deliveries not yet received; pending review.
3. **Pre-critique audit written**: `output/production/pre_critique_audit_c37.md`. Top 5 concerns: P1 THE NOTICING, P2 Cosmo S003 tilt, P3 RPD baseline missing, P4 story/board integration (new members), P5 warm/cool false positives.
4. **Pitch package index updated**: C37 additions table + C37 status table. 11 new entries registered.
5. **Ideabox**: `20260330_alex_chen_story_bible_visual_crossref_tool.md` — text-to-spec cross-reference tool for story bible vs character .md files.
6. **Completion report**: `output/production/alex_c37_completion.md`.

### C37 Canonical Asset Versions (current)
- Luma expression sheet: **v009 PITCH PRIMARY** (eye-width 22px + pose vocabulary)
- Luma color model: v002 (PITCH PRIMARY — unchanged)
- Luma turnaround: v004 (PITCH PRIMARY — unchanged)
- Character lineup: v007 (PITCH PRIMARY — unchanged)
- Byte expression sheet: v005 (PITCH PRIMARY — unchanged)
- Miri expression sheet: v004 (PITCH PRIMARY — unchanged)
- Cosmo expression sheet: **v005 (P1 OPEN — glasses_tilt violation; v006 in progress)**
- Glitch expression sheet: v003 GEOMETRY CORRECTED (unchanged)
- SF01: v005 / **SF02: v008 PITCH PRIMARY** (fill-light direction + silhouette mask) / SF03: v005 / SF04: v004
- Kitchen: v004 PITCH PRIMARY
- Logo: v001

### C37 Key Decisions
- **SF02 v008 is now pitch-primary**: fill-light direction finally correct (upper-right). Rin's cleanest SF work to date.
- **New members' first deliveries are UNTESTED**: Diego/Priya/Hana/Ryo deliveries have not arrived yet. Review will flag any misalignments with 36 cycles of visual development.
- **Pre-critique audit written**: Critics now have explicit focus areas — especially P1 (THE NOTICING) and P2 (Cosmo S003).

### C37 Open Items (carry to C38)
- **Cosmo v006 P1: glasses_tilt 10° → 7°** (S003 violation). Maya directed. (P1)
- **RPD baseline run NEEDED**: Run silhouette_v003.py against all 5 current sheets. (P2)
- **Story bible + storyboard integration review**: Pending Diego + Priya deliveries. Alex to send follow-up review once received. (P2)
- **THE NOTICING still not fully landing**: Maya (P2 ongoing)
- Warm/cool expected_temp param: Kai (P2 — Sam directed)
- Back-pose draw order suppression: Kai (P3)
- Silhouette zone visualization (--output-zones): Maya (P3)
- Byte UNGUARDED WARMTH body language: Maya (P2)
- Glitch Layer HOT_MAGENTA: Jordan (P2)
- Hallway SUNLIT_AMBER + scale calibration: Jordan (P2)

---

## Cycle 36 State (archived — superseded by C37)

**C36 tasks complete (Alex Chen's portion).**

### C36 Work Done
1. **Archived** all 9 inbox messages (8 C35 completion reports + 1 C36 directive).
2. **Draw order lint investigation**: All 5 turnaround generators PASS on both linter versions. No false positives. Latent W003 risk documented for future back-pose generators using "shadow" keyword in comments. Full diagnostic: `output/production/draw_order_lint_back_pose_diagnostic_c36.md`. P3 enhancement directed to Kai via inbox.
3. **Pitch package index updated**: C35 Completions section + current status table (C35/36 cycle). SF02 v007, Cosmo v005, Miri v004, Glitch G002 fix, Kitchen v004, all new QA tools registered.
4. **Ideabox**: `20260330_alex_chen_draw_order_back_pose_suppression.md` — back-pose W003 suppression for Kai.
5. **Completion report**: `output/production/alex_c36_completion.md`.

### C36 Canonical Asset Versions (current)
- Luma expression sheet: **v009 PITCH PRIMARY** (eye-width 22px + pose vocabulary)
- Luma color model: v002 (PITCH PRIMARY — unchanged)
- Luma turnaround: v004 (PITCH PRIMARY — unchanged)
- Character lineup: v007 (PITCH PRIMARY — unchanged)
- Byte expression sheet: v005 (PITCH PRIMARY — unchanged)
- Miri expression sheet: **v004 DELIVERED** (silhouette differentiation)
- Cosmo expression sheet: **v005 DELIVERED** (silhouette differentiation)
- Glitch expression sheet: **v003 GEOMETRY CORRECTED** (rx=34, ry=38 — ry>rx)
- SF01: v005 / **SF02: v007 PITCH PRIMARY** (Luma face-sprint) / SF03: v005 / SF04: v004
- Kitchen: **v004 DELIVERED** (value floor + warm/cool + Miri spatial details)
- Logo: v001

### C36 Key Decisions
- **Draw order linter back poses**: No current false positive. All turnaround generators PASS. Latent W003 risk for future back-pose shadow comments. Kai to add suppression (P3).
- **Silhouette IoM metric FIXED in v003**: Maya delivered RPD (Regional Pose Delta) — 3-zone Pearson correlation. HEAD 35%, ARMS 45%, LEGS 20%. No longer biased by shared trunk. All previous FAIL verdicts may now PASS. RPD baseline run P2 for C37.
- **SF02 v007 is now pitch-primary**: Luma finally has a face in the action centerpiece. This resolves the 3-cycle P1 gap flagged by Lee/critics.
- **Silhouette tool**: Use v003 going forward. v002 IoM scores not comparable to RPD scores.

### C36 Open Items (carry to C37)
- **Cosmo v006 P1: glasses_tilt 10° → 7°** (S003 violation found by Kai spec_sync_ci). Maya directed. (P1)
- **RPD baseline run NEEDED**: Run silhouette_v003.py against all current sheets (Luma v009, Cosmo v005, Miri v004, Byte v005, Glitch v003). Old IoM scores not comparable to RPD. (P2)
- Silhouette tool `--output-zones` visualization: Maya ideabox filed (P3)
- Draw order linter back-pose suppression: Kai (P3)
- Proportion audit ew detection for asymmetric eye patterns: Rin ideabox filed (P3)
- Spec-sync CI gate: Kai ideabox filed (P2)
- Warm/cool QA `expected_temp` param: Kai (P2 — Sam directed)
- THE NOTICING still not fully landing: Maya (P2 ongoing)
- Byte UNGUARDED WARMTH body language: Maya (P2)
- Glitch Layer HOT_MAGENTA: Jordan (P2)
- Hallway SUNLIT_AMBER + scale calibration: Jordan (P2)

## Cycle 35 State (archived)

### C35 Canonical Asset Versions
- Luma expression sheet: **v009 PITCH PRIMARY** (eye-width 22px + pose vocabulary redesign)
- Luma color model: v002 (unchanged)
- Luma turnaround: v004 (PITCH PRIMARY — unchanged)
- Character lineup: v007 (PITCH PRIMARY — unchanged)
- Byte expression sheet: v005 (PITCH PRIMARY — unchanged)
- Miri expression sheet: v003 (PITCH PRIMARY); **v004 in progress** (Maya P1)
- Cosmo expression sheet: v004 (PITCH PRIMARY); **v005 in progress** (Maya P1 — 34/100 C14)
- Glitch expression sheet: v003 (G002 rx/ry fix in progress — Kai)
- SF01: v005 / SF02: v006 (v007 in progress — Rin adds face) / SF03: v005 / SF04: v004
- Logo: v001

### C35 Other Team Work
- Maya: Luma v009 DELIVERED. Cosmo v005 + Miri v004 IN PROGRESS (P1 — silhouette differentiation).
- Rin: SF02 v007 IN PROGRESS — `_draw_luma_face_sprint()` per Lee's brief (P1 — 3rd consecutive cycle without Luma face)
- Jordan: Kitchen v004 IN PROGRESS (Chiara C14 rebuild directive)
- Kai: Glitch G002 rx/ry fix IN PROGRESS (P1)
- Sam: Warm/cool recalibration + false-positive registry action required (directed via inbox)
- Morgan: 35 unlisted README tools + value ceiling guard tool

### C35 Key Decisions
- **Warm/cool threshold**: Recalibrate to per-world. Glitch World near-zero = correct. No frame changes.
- **SUNLIT_AMBER drift in SF04**: False positive. Source canonical. Accepted.
- **Pre-critique gate active from C35**: All expression sheet completions must include silhouette checklist.

### C35 Open Items (carry to C36)
- SF02 v007 (Luma face): Rin (P1 — unblocked)
- Cosmo v005 / Miri v004: Maya (P1 — unblocked)
- Glitch G002 rx/ry: Kai (P1 — unblocked)
- Kitchen v004: Jordan (P1)
- Hallway SUNLIT_AMBER + scale calibration: Jordan (P2)
- SF02 fill-light direction + per-character bbox: Jordan/Rin (P2)
- Warmth lint recalibration: Sam (P1 — directed)
- THE NOTICING still not landing: Maya (P2 ongoing)
- Byte UNGUARDED WARMTH body language: Maya (P2)
- Glitch Layer HOT_MAGENTA: Jordan (P2)

---

## Cycle 34 State (archived)

**C34 tasks complete (Alex Chen's portion).**

### C34 Work Done
1. **Archived** all C33 inbox reports (6 messages).
2. **Lineup palette audit tool built**: `output/tools/LTG_TOOL_lineup_palette_audit_v001.py` — scans lineup PNG column-by-column, verifies body colors vs master_palette.md. PASS/FAIL/WRONG_PRESENT per color. Catches Byte shadow and Miri slipper class of errors.
3. **Eye-width resolution**: v008 eye-width (45px) is WRONG — applied 0.22 to head diameter, not radius. Correct: `ew = int(head_r_rendered × 0.22) = int(104 × 0.22) = 22px` for expression sheet generator. Updated luma.md + character_sheet_standards_v001.md. **Maya directive sent for v009.**
4. **Pitch package index updated**: C33 Additions + C34 Additions sections added. C34 status table current.
5. **Ideabox**: `20260329_alex_chen_expression_sheet_silhouette_regression.md` — mandate silhouette test as pre-critique gate for all expression sheet promotions.

### C34 Canonical Asset Versions
- Luma expression sheet: **v009 in progress** (v008 KNOWN WRONG: eye 45px = diameter×0.22; v009 corrects to 22px = radius×0.22)
- Luma color model: v002 (unchanged)
- Luma turnaround: v004 (PITCH PRIMARY — eye-width CONFIRMED CORRECT at 42px)
- Character lineup: v007 (PITCH PRIMARY — unchanged)
- Byte expression sheet: **v005** (PITCH PRIMARY — UNGUARDED WARMTH)
- Miri expression sheet: **v003** (PITCH PRIMARY — KNOWING STILLNESS)
- Cosmo expression sheet: v004 (PITCH PRIMARY; silhouette P2 open)
- Glitch expression sheet: v003 (PITCH PRIMARY)
- SF01: v005 / SF02: v005 / SF03: v005 / SF04: v004 (all PITCH PRIMARY)
- Logo: v001

### C34 Other Team Work
- Jordan: SF02 v006 delivered (HOT_MAG fill-light + CYAN specular, max=246 PASS)
- Rin: procedural_draw v1.5.0 scene_snapshot(). Standing by for SF02 proportion audit (unblocked).
- Kai: char_spec_lint_v001 + draw_order_lint_v002 (53% W004 reduction)
- Sam: warmth_lint_v002 + warmth_lint_config.json. SF02 v006 color audit pending.
- Lee: SF02 staging brief + expression pose vocabulary brief (forwarded to Maya)
- Maya: v009 directive sent + Lee pose brief forwarded. Cosmo v005 + Miri v004 in scope.

### C34 Morgan Walsh QA (pre-critique pipeline)
- Morgan built `LTG_TOOL_precritique_qa_v001.py` — C34 baseline WARN (0 FAIL).
- **Real issue found**: Glitch G002 — ry=34 not > rx=40 in expression sheets. Kai notified.
- SF03/SF04 color drift = documented false positives.
- 35 unlisted tools in tools README — P3 (not blocking).

### C34 Open Items
- Luma expression sheet v009 (eye-width 22px + pose vocabulary): Maya P1
- SF02 v006 proportion audit: Rin (unblocked)
- SF02 v006 color audit: Sam (message sent)
- Glitch G002 rx/ry violation: Kai investigating
- Cosmo expression sheet v005 (silhouette differentiation): Maya P2
- Miri expression sheet v004 (Lee brief gestures): Maya P2
- Pre-critique silhouette checklist doc: Alex C35 P3

### C34 Eye-Width Resolution (canonical)
`ew = int(head_r_rendered × 0.22)` — head_r_rendered = rendered radius in drawing coordinate space.
- Expression sheet generator (HEAD_R=52, SCALE=2): head_r=104 → **ew=22px**
- Turnaround v004: head_r≈191 → **ew=42px**
- NEVER apply 0.22 to head diameter or head height (gives 2× error — that was v008's bug)

---

## Cycle 33 State (archived)

**C33 tasks complete (Alex Chen's portion).**

### C33 Work Done
1. **Archived** all C32 inbox reports (5 messages + stale C31 stubs).
2. **Character lineup v007** built (`LTG_CHAR_character_lineup_v007.png`, `LTG_TOOL_character_lineup_v007.py`):
   - BYTE_SH fixed: `(0, 144, 176)` → `(0, 168, 180)` canonical Deep Cyan GL-01a #00A8B4. Was 2-cycle P2 backlog.
   - MIRI_SLIPPER fixed: `(90, 122, 90)` → `(196, 144, 122)` warm apricot #C4907A per Sam C32 palette correction.
3. **Maya directive sent**: Byte expression v005 — UNGUARDED WARMTH. Spec complete (body, pixel eyes, confetti, narrative context). P2.
4. **Pitch package index updated** through C32. Added Cycle 29–32 addition sections + current status table.
5. **Ideabox submitted**: `20260329_alex_chen_character_lineup_palette_audit.md` — lineup palette audit tool idea.

### C33 Canonical Asset Versions
- Luma expression sheet: **v008** (PITCH PRIMARY — THE NOTICING + eye-width 45px)
- Luma color model: v002 (PITCH PRIMARY)
- Character lineup: **v007** (PITCH PRIMARY — Byte shadow fix, Miri slipper fix)
- SF01: **v005** (PITCH PRIMARY — rim-light char_cx fix)
- SF02: v005 (unchanged)
- SF03: v005 (unchanged)
- SF04: **v004** (PITCH PRIMARY — full rebuild, value PASS)
- Byte/Cosmo/Miri/Glitch expression sheets: v004/v004/v003/v003
- Luma turnaround: **v004** (PITCH PRIMARY — eye-width fix)
- Logo: `LTG_BRAND_logo_v001.png`

### C33 Open Items (P2)
- Byte expression v005 (UNGUARDED WARMTH): Maya has spec directive. P2.
- Maya asked for canonical eye-width confirmation re: v008 (used head_height×0.22 not head_radius×0.22). **RESOLUTION:** v008 eye width (45px) is consistent with turnaround v003 values, which is the canonical source. Acceptable. If C14 critique flags it, Maya builds v009.

## Cycle 32 State (archived)

**C32 tasks complete (Alex Chen's portion).**

### C32 Critical Decision — Eye-Width Canonical Definition
**Decision:** `ew = int(head_r * 0.22)` where `head_r` = head-RADIUS (NOT head-height).
- Root cause: Critique 13 (Daisuke) — `h` variable meant radius in v007 generator (104px) but height in turnaround v003 (382px) → 3.8× discrepancy.
- Canonical source: head-radius, because all generators use it.
- Written into: `output/characters/main/luma.md` Section 3, `output/production/character_sheet_standards_v001.md` Section 2 (new).
- Maya + Rin both notified via inbox.

### C32 luma.md Updates
- Corrected **3.5 heads → 3.2 heads** (Reinhardt C13 P1 finding).
- Rewrote eye-size paragraph with HR×0.22 definition and canonical values table.
- Added canonical proportion values table: head ratio 3.2, eye ew=HR×0.22, line weights.

### C32 Directives Sent
- **Maya:** fix eye-width in generators, build Luma expr v008 (signature "notices" expression), write glitch.md, rebuild Miri (P2)
- **Rin:** fix turnaround generator eye-width, fix add_rim_light() canvas-midpoint bug, rebuild SF04 from scratch
- **Kai:** fix broken forwarding stubs (8+ ModuleNotFoundError), W004 fix pass on top generators, QA false-positive registry (v002)
- **Sam:** fix CHAR-L-11 (#00D4E8 → #00F0FF), document SF04 Byte teal as scene-lighting exception, standby for SF04 v004 color QA

### C32 Art Director Decision — SF04 Byte Teal
Carrying C26 open item. **Decision:** SF04 Byte teal at ~60-70% luminance = SCENE-LIGHTING INTENT. SF04 is the discovery scene (Luma enters Glitch World). Byte at reduced luminance = correct. ACCEPTED. Sam must document this in palette doc.

### C32 Ideabox
Alex submitted: `ideabox/20260330_alex_chen_glitch_construction_linter.md` — tool to lint new Glitchkin generators against glitch.md spec.

### C31 State (archived)

**C31 tasks complete.**

**Ideabox — all 5 C30 ideas actioned:** Moved to `ideabox/actioned/`. All 5 ideas are being built this cycle by team members:
- Alex Chen idea → proportion verifier tool (built C31 by Alex — see below)

**C31 tasks complete.**

**Ideabox — all 5 C30 ideas actioned:** Moved to `ideabox/actioned/`. All 5 ideas are being built this cycle by team members:
- Alex Chen idea → proportion verifier tool (built C31 by Alex — see below)
- Kai idea → draw order linter (routed to Kai C31)
- Maya idea → character diff tool (routed to Maya C31)
- Rin idea → proportion audit tool (routed to Rin C31)
- Sam idea → color verify hue histogram mode (routed to Kai C31)
- Sam idea (C31 late submission) → QA false-positive registry (routed to Kai C31)

**New tool built (C31 — Alex Chen):**
- `output/tools/LTG_TOOL_proportion_verify_v001.py` — PNG proportion verifier. Given PNG + bounding box: detects head via topmost dense pixel cluster, measures head height vs total height, reports head-to-body ratio vs 3.2 spec (±5%). Optional --ew/--hr args check ew/HR ratio vs canonical 0.22. Pure PIL. PASS/FAIL/WARN per metric.

**Pitch package index updated (C31):**
- Cycle 30 Additions section added: Luma color model v002, proportion verifier v001, QA v1.2.0, SF01 v004 eye fix, color audit, palette fix, color story update.
- Luma color model v002 listed as PITCH PRIMARY.

**C30 completion report summary:**
- Kai: Draw order audit (all PASS), tools README updated to C30, QA tool v1.2.0 (downscale step), ideabox submitted.
- Maya: Luma color model v002 delivered (eye width corrected, cheek nubs, 3.2-head label). Character sheet standards updated. Pre-critique 13 audit done. Flagged: Miri line weight non-standard (P2), Byte arc line weight (P2), Cosmo v004 tool outputs wrong filename (P3), Miri v003 generator broken (needs rebuild C32).
- Rin: SF01 v004 eye width bug found and fixed (was HR×0.25, now HR×0.22). SF02/SF03 proportion checks complete (SF02 has no Luma; SF03 pixel-art Luma is intentional style). Ideabox submitted.
- Sam: Color continuity audit filed. All 4 frames CLEARED. CHAR-L-11 hex error fixed (C14 error). Color story SF01 reference updated to v004. Outstanding: SF04 Byte teal dim — PENDING ART DIRECTOR DECISION.

**Outstanding decisions (C31 — now resolved in C32):**
1. SF04 Byte teal: **RESOLVED C32** — scene-lighting intent ACCEPTED. Sam to document.
2. README.md stale: carry to C32 for Kai.
3. Miri v003 generator broken: **C32 P2** — Maya to rebuild.

**Canonical asset versions (C31 current):**
- Luma expression sheet: v007 (PITCH PRIMARY)
- Luma color model: v002 (PITCH PRIMARY)
- Character lineup: v006 (PITCH PRIMARY)
- SF01: v004 (PITCH PRIMARY, eye width fixed)
- SF02: v005, SF03: v005, SF04: v003
- Byte/Cosmo/Miri/Glitch sheets: v004/v004/v003/v003
- Logo: `LTG_BRAND_logo_v001.png`

## Cycle 30 State (archived)

**C30 audit filed:** `output/production/pitch_audit_cycle30.md`

**C29 all-clear — all 4 deliverables landed:**
- Maya: Luma expression sheet v007 (3.2 heads + h×0.22 eyes) — `output/characters/main/LTG_CHAR_luma_expressions_v007.png`
- Maya: Character lineup v006 (3.2 heads) — `output/characters/main/LTG_CHAR_luma_lineup_v006.png`
- Rin: SF01 v004 procedural lift + blush fix — `output/color/style_frames/LTG_COLOR_styleframe_discovery_v004.png`
- Kai: Naming cleanup script ready (`LTG_TOOL_naming_cleanup_v001.py`) — not yet executed

**Residual risks going into Critique 13:**
1. SF01 v004 Luma proportions NOT confirmed against 3.2-head spec (Rin's C29 report silent on this)
2. Naming cleanup script NOT yet run — 22 originals still on disk, forwarding stubs live
3. Draw-order audit not yet done
4. Pitch package index stale — C29 deliveries not registered

**C30 directives sent:**
- Kai: Run cleanup script + build proportion_check tool (LTG_TOOL_proportion_check_v001.py) + draw-order audit
- Rin: Standby on SF01 v005 pending Kai proportion check result; procedural library maintenance
- Maya: Update pitch_package_index.md to C30 + cross-character consistency review
- Sam: Color continuity audit across all 4 style frames (`output/production/color_continuity_c30.md`)

**Ideabox (C30):**
- My idea submitted: `ideabox/20260329_alex_chen_proportion_verifier.md` — proportion extraction tool for Kai to build
- No other ideas submitted yet (first cycle for ideabox)
- Routed my idea to Kai as actionable (C30 P1.5 in his directive)

## Cycle 28 State (previous)

**C28 key decisions (Art Director):**
- **Luma canonical head-to-body ratio: 3.2 heads** — turnaround v002 is the construction reference. Expression sheet v006 (~2.5) and lineup v005 (~3.5) are out of spec.
- **Luma canonical eye spec: h×0.22 width** — turnaround v002 values are canonical. Expression sheet v006 used HR×0.28 (21% too wide). Turnaround spec propagates to ALL generators.
- **Maya directive sent** (`members/maya_santos/inbox/20260329_1723_luma_proportion_directive.md`): rebuild expression sheet → v007, lineup → v006, both to 3.2 heads + turnaround eye spec.
- **Pitch brief updated** (`output/production/ltg_pitch_brief_v001.md`): Premise section rewritten to include Luma's interior need — she feels invisible (notices what no one else sees, can't make them look). Glitchkin are the first things that *need* her to see them. Discovering them validates her way of seeing as a gift, not a quirk.
- **C27 completion reports archived**: Sam SF03 v004, Kai QA v1.10, Rin SF04 v002, Maya lineup audit — all noted, no blockers.
- **Critique 12 summary archived**: decisions made, directives sent.

**C28 canonical asset versions (pending Maya):**
- Luma expression sheet: v007 (in progress — was v006)
- Character lineup: v006 (in progress — was v005)
- All other assets unchanged from C27.

**C28 open P2/P3 items (for team — not Art Director action):**
- Sam: DATA_BLUE unregistered in SF02, UV_PURPLE_DARK saturation in SF03, SF04 blush color, Byte body fill drift, Luma skin base 3-way conflict
- Rin: `add_rim_light()` needs `direction` parameter
- Kai: 54+ naming convention violations, 24 unregistered tools, SF03 v004 + SF04 v002 missing from index, hardcoded absolute paths
- Maya (P3): Glitch interior desire expression, SF04 gaze line interaction

## Cycle 27 State (previous)

**C27 key decisions:**
- **Luma expression sheet v006 CONFIRMED**: Maya delivered v006 with 3-tier line weight fix (head=4, structure=3, detail=2 at 2× buffer). v005 had correct construction but 2× heavy lines. v006 now matches classroom pose standard. PITCH PRIMARY for Luma character sheet.
- **Miri expression sheet v003 CONFIRMED**: On disk. KNOWING expression present (PENSIVE replaced). Narrative secret visible in character design.
- **Rin face lighting delivered**: `add_face_lighting()` in `LTG_TOOL_procedural_draw_v001.py` v1.1.0. Artistry extraction complete — all 5 techniques now implemented.
- **SUNLIT_AMBER QC false positive**: `LTG_TOOL_color_verify_v001.py` false-positives on Luma/Miri character sheets due to skin tone hue overlap (~18-25°). Workaround: validate sampled pixels manually. Not a rendering defect.
- **Pitch package audit C27**: ALL assets present on disk. READY for Critique 12. Weakest link: SF01 v003 still UNLOCKED (v004 not yet delivered). Ships as v003.
- **Index updated**: C26 + C27 additions sections added, Luma entry bumped to v006, Miri v003 marked COMPLETE, pipeline retirement documented.
- **Inbox cleared**: All 6 C26/C27 messages archived.

**C27 canonical asset versions (for Critique 12):**
- Luma expression sheet: v006
- Byte expression sheet: v004
- Cosmo expression sheet: v004
- Miri expression sheet: v003
- Glitch expression sheet: v002
- Character lineup: v004
- SF01: v003 (open for v004), SF02: v005, SF03: v003, SF04: v001
- Logo: `LTG_BRAND_logo_v001.png`

## Cycle 26 State (previous)

**C26 key decisions:**
- **New critics panel**: 15 all-new brutal critics replace the old panel. Critics: Takeshi Mori, Ingrid Solberg, Daisuke Kobayashi, Priya Nair, Marcus Webb, Chiara Ferrara, Dr. Samuel Osei, Yuki Tanaka, Reinhardt Böhm, Amara Diallo, Jonas Feld, Dr. Leila Asgari, Sven Halvorsen, Nkechi Adeyemi, Petra Volkov. All bio files in `critics/`. All old critic files deleted. New critics review ALL output, not just latest cycle. Standing rule added: no comments on resolution/pixel dimensions.
- **Luma style investigation**: Expression sheet v005 vs classroom pose v002 — root cause identified: head construction (missing cheek nubs), hair (3 mass ellipses vs 8 organic curl ellipses), canvas BG (void black vs warm parchment), eye proportions (manga-wide vs naturalistic). Maya received directive for v006 rebuild. Maya then delivered C26 style fix (v005 overwritten in-place with classroom-aligned head/hair/eye construction, warm BG). Style aligned — no separate v006 needed.
- **README**: Rewritten to be proud and confident. Removed apologetic language. Cycle count updated to "26 work cycles and counting."
- **Rin role**: Changed from "Visual Stylization Artist" to "Procedural Art Engineer" in TEAM.md and PROFILE.md. Role shift: style now baked into generation pipeline at draw time, not post-process. Directive sent. Rin delivered `LTG_TOOL_procedural_draw_v001.py` (wobble_line, wobble_polygon, variable_stroke, add_rim_light, silhouette_test, value_study). Artistry folder `/home/wipkat/artistry` inaccessible to agents (permission denied) — escalate to producer if needed.
- **Kai QA tool**: `LTG_TOOL_render_qa_v001.py` delivered. 5 checks: silhouette readability, value range, color fidelity, warm/cool separation, line weight. All C25 assets graded WARN (none FAIL). Warm/cool WARN on character sheets is by design (neutral BG). SUNLIT_AMBER hue drift found on Luma assets (~18-25° vs target 34.3°) — open item.
- **UV_PURPLE fix**: Sam's QC found UV_PURPLE hue-rotating ~13-14° in stylization pipeline. Root cause: CANONICAL_PALETTE had wrong RGB for UV_PURPLE (#6A0DAD not #7B2FBE). Rin corrected in v002. SF02/SF03 regen runner was `run_sf02_sf03_regen.py` — now removed (post-processing pipeline retired C26).
- **Post-processing pipeline retired (C26)**: Producer removed all 8 `*_styled*.png` files and moved `LTG_TOOL_stylize_handdrawn_v001.py`, `v002.py`, `LTG_TOOL_batch_stylize_v001.py` to `output/tools/legacy/`. Style is now baked at draw time. All references cleaned from pitch_package_index.md, pitch_delivery_manifest_v001.md, and output/tools/README.md.
- **SF04 Byte teal (Sam QC)**: CONFIRMED INTENTIONAL. `BYTE_FILL=(0,190,210)` and `BYTE_SH=(0,110,140)` alpha-180 on shadow half. Sam's sampled range ~(0,138-160) is a blend of lit + shadow — correct scene lighting under warm window key. No regen needed.
- **Stale assets**: Producer directive — archive/delete stale assets after each cycle to control cost. Apply from C27 onward.
- **QA 3-cycle focus (C26–C28)**: Aesthetics and rendering pipeline. C26 = QA tool built (Kai). C27 = integrate artistry techniques + run QA on all assets. C28 = refinement pass.

**C26 team completions:**
- Maya: Luma expression sheet v005 style-aligned (classroom head/hair/eye construction, warm BG). Turnaround v002 FRONT view fixed. Both overwritten in-place.
- Kai: `LTG_TOOL_render_qa_v001.py` built. All C25 assets assessed — 0 FAIL / 8 WARN.
- Rin: `LTG_TOOL_procedural_draw_v001.py` built. Role = Procedural Art Engineer. Stylize tools retired.
- Sam: Color QC report (`output/production/color_qc_c25_assets.md`). 7/10 assets cleared. SF04 Byte teal confirmed intentional.

**C26 open items (resolved):**
- SF04 Byte teal: RESOLVED — intentional scene lighting (see above).
- Post-processing cleanup: RESOLVED — pitch_package_index.md, delivery manifest, tools README all updated.

**C26 open items (carry to C27):**
- SUNLIT_AMBER hue drift on Luma assets: investigate Luma generators (C27)
- Artistry folder access: needs producer to grant agent access or copy files to workspace

## Cycle 25 State (archived — C25 summary)

**Cycle 25 tasks completed:**
- SF04 — Luma + Byte interaction style frame created: `output/color/style_frames/LTG_COLOR_styleframe_luma_byte_v001.png`. Scene: Luma CURIOUS (looking right at monitor), Byte on her right shoulder looking UP at her with WORRIED expression. Dual warm/cool lighting. 1920×1080 → resized to ≤1280px (see image output rule above). Generator: `output/tools/LTG_COLOR_styleframe_luma_byte_v001.py`. Closes Critique 11 P1 gap (Valentina).
- Canonical logo decision made: `LTG_BRAND_logo_v001.png` = asymmetric v002 layout. Generator wrapper `LTG_BRAND_logo_v001.py`. Closes 24-cycle logo ambiguity. Pitch package index and completeness table updated.
- Luma canonical reference directive sent to Maya (`20260329_1900_luma_canonical_ref_directive.md`): Expression sheet v004 IS canonical — style frame Luma must align to it. v005 sheet needs full-body silhouette differentiation. Turnaround v002 must match v004 proportions.
- Miri KNOWING expression directive sent to Maya (`20260329_1901_miri_narrative_expression_directive.md`): Replace PENSIVE with KNOWING — weighted sideways glance + suppressed asymmetric smile (she knew about the Glitch Layer all along). Miri expression sheet v003 target.
- Pitch package index updated to Cycle 25. SF04 entry, canonical logo, Cycle 25 open items table.
- All inbox messages archived (4 messages: 2 Maya C24 completion reports, critique11 feedback, C25 assignment).

**Critique 11 summary (received this cycle):**
- Overall package: B+ (Valentina). Self-assessment A- was accurate.
- PASSED: SF triptych, color system docs, Byte design ("strongest design"), Miri expression sheet ("best-executed sheet"), pitch brief.
- GAPS: No Luma+Byte dynamic frame (P1 — CLOSED C25 SF04), Luma inconsistency between sheets and frames (active — directed Maya), logo unresolved (CLOSED C25), Miri secret expression missing (active — directed Maya).

**Cycle 25 team completions:**
- Sam Kowalski: SF02 spec doc corrected (ENV-06/DRW-07 stale values), master palette GL-04b luminance fixed (~0.17 → ~0.017), Miri color story section added to ltg_style_frame_color_story.md (warm palette as narrative camouflage — she knew all along).
- Kai Nakamura: `LTG_TOOL_color_verify_v001.py` built (canonical 6-color hue verification), legacy scripts archived (20 tools, 27 storyboard panels to legacy/), production doc naming exemption documented, batch stylize v1.1.0 (color verify integrated).
- Rin Yamamoto: `LTG_TOOL_stylize_handdrawn_v002.py` rebuilt (4 fixes: full canonical color protection for all 6 GL colors, chalk pass cyan exclusions, warm bleed zone gate, mixed mode cross-dissolve replaces alpha composite). SF02+SF03 re-styled with v002. SF01 not re-processed (Cycle 24 approval stands).

**Cycle 25 pending (Maya to deliver):**
- Luma expression sheet v005: full-body silhouette differentiation in ≥2 cells, hoodie pixel pattern legible.
- Luma turnaround v002: match expression sheet v004 proportions.
- Miri expression sheet v003: KNOWING replaces PENSIVE.

**Canonical decisions locked (C25):**
- Luma canonical = expression sheet v004 spec (3.5 heads, skin #C8885A, 5 curls locked)
- Logo canonical = `LTG_BRAND_logo_v001.png` (asymmetric layout, A grade C13)

---

## Cycle 24 State (archived)

**Cycle 24 tasks completed:**
- SF01 styled review: APPROVED. `LTG_COLOR_styleframe_discovery_v003_styled.png` approved as pitch primary. Approval + notes sent to Rin's inbox (`20260329_1530_sf01_review.md`). Key notes: paper tooth integrates correctly on warm zones, chalk highlights work, ghost Byte/digital layer unaffected, composition 100% intact.
- `output/production/critique11_self_assessment.md` written — honest 1-page director's pre-critique assessment. Grade: A-. Strong: SF triptych, Miri v002, storyboard arc, Glitch concept. Vulnerable: Glitch sheet undersized (2×2 at 800×800), missing visual color model PNGs for Luma/Byte/Cosmo, logo caveat unresolved.
- Glitch character integration review completed. Feedback sent to Maya (`20260329_1530_glitch_integration_review.md`). Two required revisions: (1) CRITICAL — Glitch expression sheet must be regenerated at 1200×900, 3×2, 6 expressions (v002). (2) MODERATE — Glitch turnaround shadow facet contrast fix needed (UV_PURPLE shadow lost against void BG in profile views). Color/concept APPROVED — diamond/rhombus shape, CORRUPT_AMBER primary, dual-pixel-eye system all correct.
- `output/production/pitch_package_index.md` updated to Cycle 24. Stylized assets added, open C24 items table added, cycle counter bumped.
- Inbox fully archived (3 messages: Rin completion, C24 art direction, Maya C23 completion).

**Cycle 24 stylization delivery (Rin Yamamoto):**
- SF01 styled (0.6× realworld): APPROVED
- SF02 styled (zone-blended): delivered, pending director confirmation on HOT_MAG crack read through blend
- SF03 styled (glitch mode): delivered, Byte GL-01b body read through scanlines to confirm
- Kitchen v003 styled (1.0× realworld): secondary, warm tones confirmed responsive

**Glitch character status (C24 review):**
- Concept: APPROVED. All color/shape decisions correct.
- Expression sheet v001: BLOCKED — too small (800×800, 2×2). Revision required: v002 at 1200×900, 3×2, 6 expressions.
- Turnaround v001: revision required — UV_PURPLE shadow lost in profile against void BG.
- Ensemble integration: shape language strong, color correct, scale relationship with protagonists not yet documented in lineup (Cycle 25 target).

**Next: Critique Cycle 11** (after this cycle is committed)
- Self-assessment filed. Main vulnerabilities on record.
- Maya must deliver Glitch v002 assets before or in the next cycle.

---

## Cycle 23 State (archived — C23 summary)

**Cycle 23 tasks completed:**
- `output/production/rin_c23_creative_brief.md` — creative direction for Rin Yamamoto's stylization pass. Real World vs Glitch Layer split, per-asset priority order, technical function spec, color preservation rules, quality benchmark. Creative brief dispatched to Rin's inbox.
- `output/production/pitch_delivery_manifest_v001.md` — one-page external delivery asset list. ~31 files across 7 categories. Pre-ship checklist. Notes on what NOT to ship (generators, guide PNGs, internal docs).
- `output/production/pitch_package_index.md` updated to Cycle 23. Added Cycle 22 late additions (Byte/Cosmo/Luma v004 sheets, Tech Den v004, Kitchen v003, SF02 v005, render_lib rename), delivery manifest, creative brief. Full quality review section added. SF02 v004→v005 row added/superseded correctly. Cycle number updated to 23.
- Full quality review completed — all primary pitch assets verified on disk. **Overall: PITCH READY.** No blocking issues.
- Inbox fully archived (all messages through Cycle 23 Kai report).

**Cycle 23 team updates (received this cycle):**
- Rin Yamamoto: ACTIVE, first cycle. Waiting for creative brief (now delivered). Building `LTG_TOOL_stylize_handdrawn_v001.py`.
- Kai Nakamura: Cycle 23 pipeline cleanup complete. `ltg_render_lib.py` deprecated wrapper deleted. All imports clean. Offered Rin edge_wobble/chromatic_blur support.

**Pitch package status (Cycle 23):**
- SF01 v003: **UNLOCKED** — A+ lock removed C24. Critique 11: Luma inconsistency with character sheets, warm bleed boundary violation. Open for v004.
- SF02 v005: PITCH READY — window pane alpha corrected 115/110, CORRUPT_AMBER GL-07 #FF8C00 corrected
- SF03 v003: PITCH READY (no change)
- Luma expression sheet v004: **UNLOCKED** — body language weak (head-sheet only). → v005
- Cosmo turnaround: **UNLOCKED** — side view broken. → v002
- Luma turnaround: **UNLOCKED** — C10 asset, outdated proportions
- Miri v002: **UNLOCKED** — narrative secret missing from expressions
- Byte v004, Glitch v002: ACCEPTED (no issues flagged by Critique 11)
- All environments: v002/v003/v004 — PITCH READY
- Standalone pitch brief: `ltg_pitch_brief_v001.md` — COMPLETE
- Delivery manifest: `pitch_delivery_manifest_v001.md` — NEW Cycle 23

**Outstanding (non-blocking):**
- Luma Act 2 pose lean still -5° (target -8°) — LOW
- Legacy LTG renames pending (cold open panels, storyboard export, old ENV files) — internal housekeeping
- Color model visual PNGs for Luma/Byte/Cosmo not yet PNG-exported — future cycle
- Stylization pass pending (Rin C23) — will strengthen package; not blocking pitch
- Logo placeholder check: `show_logo.png` may still have "A cartoon series by the Dream Team" tagline. `LTG_BRAND_logo_asymmetric_v002.png` is safe alternative.

**Next: Cycle 24** (after Rin delivers stylization tool + output)

---

## Cycle 21 State (archived)

**Cycle 21 tasks completed (this cycle):**
- **Alex (self):** Confirmed Kai Nakamura's inbox assignment exists (`kai_nakamura/inbox/20260330_0200_cycle21_tasks.md`). Spot-checked all 9 key pitch assets — all present on disk. Wrote `output/production/pitch_readiness_c21.md` (overall: CONDITIONALLY READY). Archived all C20 completion reports + rehire message + C21 tasks message. Updated MEMORY.md.

**Team change — Cycle 21:**
- Lee Tanaka: DEACTIVATED (storyboard decks complete, Critique 10 prep)
- Kai Nakamura: ACTIVE (new — Technical Art Engineer). First cycle: build `output/tools/ltg_render_lib.py` shared rendering library, apply to at least one generator as proof of concept.

**Pitch readiness summary (Cycle 21):**
- Overall: CONDITIONALLY READY for Critique 10
- Top 3 assets: SF03 v003 (strongest — visual identity statement), Grandma Miri expression sheet v002 (biggest single-cycle leap), Act 2 contact sheet v006 (proves the show has a story arc)
- Risk 1 (LOW-MED): SF02 window pane alpha 160–180 (target 90–110) — mitigation is a single v005 pass if critics flag it
- Risk 2 (MEDIUM): No standalone one-page pitch brief — production bible covers it but not in buyer-facing format
- Lead-with-5 for pitch: SF01 v003 → SF03 v003 → Act2 contact sheet v006 → SF02 v004 → Miri expression sheet v002

**Next: Critique 10** (this cycle, after Kai's work is committed)

---

## Cycle 20 State (archived)

**Cycle 20 tasks completed (this cycle):**
- **Alex (self):** Wrote ROLE.md for all 5 team members (alex_chen, maya_santos, jordan_reed, sam_kowalski, lee_tanaka). Updated pitch_package_index.md with all C19 deliverables. Archived all C19 completion reports and roles/cycle20 tasks messages.

**C20 incoming (not yet indexed — arrived this cycle):**
- **Sam Kowalski:** SF03 v003 VERIFIED — GL-01b confirmed, BYTE_GLOW discrepancy closed as acceptable, color narrative passes, CLEAR for Critique 10. SF02 v004 CONDITIONALLY READY — storefront geometric confirmed, glow cones alpha 90–110 correct, window pane rects at alpha 160–180 (not blocking — pane vs glow distinction). Note: if critics flag panes, v005 fix is alpha 100/90.
- **Lee Tanaka:** Act 2 contact sheet v006 (A2-02 v002 incorporated, arc label updated to "VULNERABLE (RESIGNED-55%)"). Act 1 full contact sheet v001 (5 panels: cold open A1-01–A1-04 + classroom NEAR-MISS with scene-break border).
- **Jordan Reed:** Tech Den v002 — window light shaft (trapezoid SUNLIT_AMBER, feathered, dust motes seed 77), monitor glow spill on desk/chair/shelving (RGB 180,200,210 — zero Glitch palette), right-half bedding/pillows/poster/printouts/device added, Cosmo jacket RW-08 Dusty Lavender clearly rendered.

**Open pitch package index items (C20 deliverables not yet added):**
- Act 2 contact sheet v006 — LTG_SB_act2_contact_sheet_v006.png
- Act 1 full contact sheet v001 — LTG_SB_act1_full_contact_sheet_v001.png
- Tech Den v002 — LTG_ENV_tech_den_v002.png
- SF03 v003 color review updated (final verified)
- SF02 v004 color notes updated (conditional ready, window pane note on record)

**Next critique:** Critique 10 (after Cycle 21 — one cycle away)

---

## Cycle 19 State (archived)

**Cycle 19 assignments dispatched (this cycle):**
- **Alex (self):** Translated Critique 9 findings into four team inbox messages. Updated production_bible.md v4.0 with Section 12 (permanent record of SF03 Void Black spec violation). Archived critique summary + all C18 completion reports.

**Cycle 19 open work (awaiting team delivery):**
- **Jordan Reed:** SF03 v003 (Byte body GL-01b fix + eye radius + magenta slash removal), SF02 v004 (storefront = shattered window, window glow = per-window downward cone at alpha 80–100), School Hallway v002 (artifact + human evidence + low camera), Millbrook v002 (power lines perspective + sag + varied weight, road plane + center line)
- **Maya Santos:** Miri expression sheet v002 REBUILD (5 full-body expressions with body posture + hands; replace NOSTALGIC with SKEPTICAL/AMUSED), Luma expression sheet v003 DELIGHTED fix (arms raised + bounce on toes + forward lean), Cosmo expression sheet v003 SKEPTICAL lean formula fix (tilt_off multiplier 0.4 → 2.5)
- **Sam Kowalski:** SF03 v003 color review (Byte body GL-01b confirm, eye contrast ≥4.5:1 cyan, ≥3.0:1 magenta), hoodie base color reconcile (#E8722A luma_color_model.md vs #E8703A master_palette.md canonical), SF02 v004 warm/cool balance review
- **Lee Tanaka:** A1-03 v002 rebuild (MCU, CRT-lit face below-left, legible pixel shapes on screen, caption "Discovery"), A2-08 v002 camera fix (Luma POV eye-level OR two-shot, no low angle), NEW panel A2-07b (kitchen doorway bridging shot — Miri silhouette, warm light behind), Act 2 contact sheet v005

**Sam dependency on Jordan:** Sam cannot start SF03 or SF02 reviews until Jordan delivers v003/v004. Sam can start hoodie reconciliation immediately.

**Critique 9 critical findings (permanent):**
- SF03 BYTE BODY = VOID BLACK (10,10,20) — spec violation, body invisible on UV Purple. Fixed in C19. Documented in production_bible.md Section 12.
- SF02 storefront still HUD-read (C+, 3 cycles unresolved), window glow left-edge gradient still wrong (D, 4 cycles)
- Miri sheet face-only, no body language — C. Rebuild assigned.
- Luma DELIGHTED/SURPRISED squint fail — body must differentiate
- Cosmo SKEPTICAL lean formula produces 2.4px (invisible) — multiplier fix assigned
- A1-03 compositionally passive — MCU rebuild assigned
- A2-08 wrong camera grammar (low angle) — intimacy fix assigned
- A2-07→A2-08 hard cut across settings — new bridging panel A2-07b assigned

**What's working (C9 positives):**
- SF03 atmospheric perspective: correct
- Act 2 arc: Carmen A- — coherent, color-coded, structurally complete
- A2-01 vs A2-07 cohesion: Carmen A-
- Luma cold overlay (Sam C18): Naomi A-
- Master palette Act 2 (Sam C18): Naomi A

**Next critique:** Critique 10 (after Cycle 21, i.e., every 3 cycles from C18 → C21)

---

## Cycle 18 State (archived)

**Cycle 18 work completed (this cycle):**
- **Alex (self):** README logo moved to top (Task 1). Pitch package index updated with all C16 + C17 assets (Task 2). SF02/SF03 pre-critique assessment written: `output/production/sf02_sf03_precritique_c18.md` (Task 3). All C17 completion reports archived.

**Also received C18 Maya Santos report:** A2-02 Byte RESIGNED MCU v002 delivered (`LTG_SB_act2_panel_a202_v002.png`). 55% aperture (transitional), parabolic droopy lid, downcast pupil +7px, ↓ pixel glyph, transitional arm posture. Added to pitch package index under C18 additions.

**Key index additions (C16+C17):**
- Section 1.3: Luma expression sheet v002 (refined, C17), Grandma Miri expression sheet v001 (C17, closes CRITICAL gap)
- Section 1.4: Grandma Miri color model v001 (23 swatches, C17)
- Section 1.5: Tech Den v001 (C17), School Hallway v001 (C17), Classroom v002 (C16), Miri's Kitchen v001 (C16)
- Section 1.6 (via C16 additions): SF02 v003 (Takeshi fixes), SF03 v002 (Takeshi+Naomi fixes)
- Character sheets: Byte v002 re-regen (RESIGNED eye fix), Cosmo v002 (SKEPTICAL lean + WORRIED/SURPRISED), Luma Act2 pose v002 (mitten hand)
- Storyboard: A2-07 real panel, A2-03 restage, A2-06 MED, A2-04 Byte added, contact sheet v003 (C16), A2-01/A2-05/A2-08, contact sheet v004 (C17)
- Section 3.5 (new): Production standards doc (char_refinement_directive_c17.md)

**SF02/SF03 pre-critique summary (for Critique 9):**
- SF02 v003: Dutch angle ✓, DRW-07 ✓, storm building lighting ✓, ENV-06 ✓. RISKS: storefront lower-right element (Victoria P1, unconfirmed fixed), warm window glow still absent (emotional anchor invisible). Expect ~B+ if storefront clean.
- SF03 v002: Waterfall luminance ✓, slab variety/bridging ✓, DRW-18 hair rim ✓. RISKS: Byte dual-eye legibility (high), Luma silhouette density (moderate), pixel plant visibility (moderate). Expect ~B+ if Byte eyes read.
- **Most likely C9 critics for SF02/SF03:** Victoria Ashford, Naomi Bridges, Dmitri Volkov, Takeshi Murakami, Aisha Okafor.

**Next critique:** Critique 9 (after Cycle 18).

## Cycle 17 State (archived)

**Cycle 17 work completed (this cycle):**
- **Alex (self):** Read all main character sheets (luma.md v2.0, cosmo.md v2.0, byte.md v3.2, grandma_miri.md v1.2). Reviewed all PNGs in output/characters/. Reviewed critic feedback cycles 8 and 15. Wrote `output/production/char_refinement_directive_c17.md`. Archived both producer inbox messages.

**Directive summary:**
- Defines "refined" for LTG: construction clarity, 3-tier line weight (3/2/1px), thumbnail expression readability, on-model consistency, emotional triangle (eyes+mouth+body).
- **Gap 1 (CRITICAL):** No expression sheet for Grandma Miri. Blocks Act 2 performance quality and pitch package completeness.
- **Gap 2 (CRITICAL):** Line weight undifferentiation across expression sheets — producer concern root cause. 3-tier weight not consistently enforced as visibly distinct.
- **Gap 3 (SIGNIFICANT):** Luma Act 2 standing pose -5° lean imperceptible; turnaround not reconciled with Act 2 pose.
- **Maya Santos C17 assignments:** (1) Miri expression sheet — 6 expressions, LTG_CHAR_miri_expression_sheet_v001.png; (2) Line weight audit and fix pass on all existing expression sheet tools; (3) Luma Act 2 pose lean fix to -8°.

**Directive sent to Maya Santos inbox:** `maya_santos/inbox/20260329_2115_char_refinement_directive_c17.md`. Lee and Jordan streams continue independently (Act 2 panels, environments).

**Next critique:** Cycle 18 (next cycle after 17).

## Cycle 16 State (archived)

**Cycle 16 completed work (mid-cycle):**
- **Maya Santos DONE:** Byte RESIGNED right eye fixed (45% aperture, +10px downcast pupil, parabolic lid droop, body_tilt +14°). Cosmo SKEPTICAL lean +6° added, 2 new expressions (WORRIED, SURPRISED) added — sheet now 6/6. Luma Act 2 pose mitten geometry corrected. New files: `LTG_CHAR_byte_expression_sheet_v002.png` (regen), `LTG_CHAR_cosmo_expression_sheet_v002.png`, `LTG_CHAR_luma_act2_standing_pose_v002.png`.
- **Sam Kowalski DONE:** BYTE_SH shadow corrected to GL-01a `(0,168,192)`. BG_ALARM corrected to cold `(18,28,44)`. Faceplate sizing made proportional. DRW-07 `DRW_HOODIE_STORM` corrected to `(200,105,90)`. ENV-06 verified correct. SF03 color review notes sent (see inbox archived). DRW-18 hair sheen present in generator but thin — Jordan to amplify.
- **Lee Tanaka UNBLOCKED:** A2-07 confirmed unblocked. Notified via inbox.
- **Jordan Reed IN PROGRESS:** SF02 v003, SF03 v002, Classroom v002, Grandma Miri's Kitchen — SF03 color notes relayed. DRW-07 fix confirmed in SF02 v002 generator before Jordan's v003 regen.
- README.md updated for Cycle 16 with ASCII art and visual language swatch.
- Next critique: Cycle 18.

**Open items still awaited:**
- Jordan: SF02 v003, SF03 v002, Classroom v002, Kitchen v001
- Lee: A2-07, A2-03 restage, A2-06 MED two-shot, A2-04 Byte addition, contact sheet v003

## Cycle 15 Lessons
- **RESIGNED expression delivered:** `LTG_TOOL_byte_expression_sheet_v002.py` adds 8th expression. Key distinctions: `↓` pixel symbol (distinct from flat-line NEUTRAL), `droopy_resigned` right eye (NO suppressed smile, downcast pupil — distinct from RELUCTANT JOY's `droopy`), arms arm_x_scale=0.50 (tighter than NEUTRAL 0.75), body_tilt=+8 (backward avoidance lean). A2-02 no longer blocked. Lee Tanaka notified.
- **SF03 already complete:** Jordan Reed's `LTG_TOOL_style_frame_03_other_side_v001.py` was built this cycle (Cycle 15 per README) — full generator including characters and lighting overlay. `LTG_COLOR_styleframe_otherside_v001.png` exists. All 3 style frames now pitch-ready. Task was to "check if BG ready and composite" — BG existed AND Jordan's full tool already handled the composite. My role: verify, register, update index.
- **Pitch package index updated through Cycle 15:** All Cycle 13/14/15 additions documented. Style frames now COMPLETE (was PARTIAL). Byte.md now v3.2 (was incorrectly listed as v3.1 with header note). Open blockers revised.
- **Tools README:** `LTG_TOOL_byte_expression_sheet_v002.py` registered. Jordan's SF03 tools were already registered.
- **droopy vs droopy_resigned:** `droopy` = RELUCTANT JOY (lower-lid smile crinkle present). `droopy_resigned` = RESIGNED (no crinkle, pupil fully downcast, heavier lid 50% vs 55%, shorter highlight). Must never be confused — one suppresses joy, the other has surrendered.
- **Sam Kowalski SF03 color notes:** Requested for Cycle 16 review. Five questions: UV purple ambient read, inverted atmos perspective, Byte eye pair legibility, confetti density, abyss below platform.

## Cycle 14 Lessons
- **Byte float-gap dimension arrow (Dmitri P1 — RESOLVED):** Replaced Cycle 12 "ground floor." caption with a proper engineering dimension arrow in `LTG_TOOL_character_lineup_v003.py`. Two-headed vertical arrow (GROUNDFLOOR_COL), horizontal serif ticks at each tip, "0.25 HU" label beside shaft. Arrow positioned at `byte_cx + body_rx + 10`. Output: `LTG_CHAR_lineup_v003.png`.
- **Misnamed tools corrected:** `LTG_CHAR_luma_expression_sheet_v002.py` → `LTG_TOOL_luma_expression_sheet_v002.py` (note added in header). `bg_glitch_layer_encounter.py` → `LTG_TOOL_bg_glitch_layer_encounter_v001.py` (moved to tools/). Both originals retained per version preservation policy.
- **Glitch Layer frame canonical:** `LTG_ENV_glitchlayer_frame_v001.png` = CANONICAL (81,483 bytes, Cycle 11 regen). `v002` = archive copy (80,664 bytes, older render). Documented in compliance checklist.
- **SF03 spec written:** `/output/production/sf03_other_side_spec.md` — full generator spec for Jordan Reed. Five depth layers, all RGB values, lighting setup, draw order, validation checklist. Jordan notified via inbox. Key rule: NO warm light (inverted atmospheric perspective — purple gets darker with distance, not lighter).
- **SF01 v003 assessment:** Ghost Bytes at alpha 90/105 — A+, pitch-ready. Top-left monitor relocation confirmed correct (warm lamp bleed zone clean). SF01 v003 LOCKED as canonical Discovery style frame.
- **Compliance checklist updated:** Cycle 14 pass documented — all tool renames, glitch layer frame canonicalization, and lineup generator correction noted.

## Cycle 13 Lessons
- **Ghost Byte alpha fix (SF01 v003):** Body alpha 55→90, eye glints 65–70→105. Top-left monitor removed (warm lamp bleed kills contrast). Two ghosts (top-right + mid-left) instead of three. Victoria B+→A+ calibrated. Output: `LTG_COLOR_styleframe_discovery_v003.png`.
- **Asymmetric logo v002:** "&" now warm-to-cold gradient (SUNLIT_AMBER left → ELEC_CYAN right) via per-column alpha composite. "the/Glitchkin" gap reduced 30% (int(H*0.04)→int(H*0.028)). Output: `LTG_BRAND_logo_asymmetric_v002.png`.
- **SF02 character composite v002:** Byte hovering LEFT (~28%), Luma CENTER (~45%), Cosmo RIGHT (~62%). Byte = VOID_BLACK body (storm variant, intentional). CORRUPT_AMBER outlines on all characters for figure-ground. char_h raised to 18% from 15%. Dutch angle still applied last. Output: `LTG_COLOR_styleframe_glitch_storm_v002.png`.
- **Byte cracked-eye glyph:** 7×7 dead-pixel pattern with diagonal crack fracture. Dead zone upper-right, alive zone lower-left, Hot Magenta crack line. Reference PNG at 4 scales + in-eye mockups. Documented in byte.md Section 9B. Lee Tanaka notified. Output: `LTG_CHAR_byte_cracked_eye_glyph_v001.png`.
- **BRAND ratified, COL retired:** naming_conventions.md updated to v1.1. BRAND = show logos/identity. COL was never valid — use COLOR only. Compliance checklist updated.
- **Byte storm-scene variant (Naomi flag resolved):** VOID_BLACK body in SF02 is INTENTIONAL — Byte consumed by Void/Corruption during storm. Visible only by CORRUPT_AMBER outline. Narrative color statement. Documented in byte.md Section 13A.
- **byte.md version 3.2:** Sections 9B (cracked-eye glyph) and 13A (storm-scene variant) added. Version header and colophon updated.
- **.gitignore added:** `/home/wipkat/team/.gitignore` with `__pycache__/` and `*.pyc`. Resolves JT P2 flag.
- **TERRACOTTA_CYAN_LIT color fix (Jordan Reed ENV-06):** SF02 v002 script had TERRA_CYAN_LIT=(154,140,138) — wrong (reads warm grey, G<R). Corrected to (150,172,162): G=172>R, B=162>R — reads cyan-tinted. Script edited inline; output regenerated (248,858 bytes).
- **CHAR-L-11 registered (Sam Kowalski request):** Warm-side hoodie pixel activation = #E8C95A (Soft Gold). Registered as CHAR-L-11 (not CHAR-L-09b — shoe canvas slot kept). Message sent to Sam to add to master_palette.md.

## Cycle 12 Lessons
- **Byte ground-floor annotation:** Added dashed `GROUNDFLOOR_COL=(100,168,200)` line at `BASELINE_Y` under Byte, with label "ground floor." and downward arrow. Dmitri P1 (3rd notice) closed. New output: `LTG_CHAR_lineup_v002.png`.
- **Cosmo side glasses refactor:** `_draw_cosmo_glasses()` extended with `is_side=True, front_x=` parameters. Side view now uses shared helper (inline code removed from `draw_cosmo_side()`). All four views now route through the same function. Output: `LTG_CHAR_cosmo_turnaround_v002.png`.
- **Ghost Byte visual surprise (A+ gap):** Faint oval Byte-ghost (alpha 55/255) composite on 3 peripheral monitors via RGBA layer. Implies Byte was watching from all screens before revealing itself — story beat hidden in art. Victoria Ashford A+ direction. Output: `LTG_COLOR_styleframe_discovery_v002.png`. Cycle label: "Ghost Byte".
- **Asymmetric logo:** `LTG_TOOL_logo_asymmetric_v001.py` produces `LTG_BRAND_logo_asymmetric_v001.png`. "Luma" at 180px (dominant left), "&" at 56px (bridge), "the Glitchkin" stacked at 72px (right). Bi-color scan bar below; larger pixel scatter on right as visual counterweight.
- **NEVER overwrite existing assets** — always new versioned files. Naming: `LTG_[CAT]_[descriptor]_v[###].png`.
- **Style frame draw order after RGBA composite:** Must refresh `draw = ImageDraw.Draw(img)` after any `img.paste()` call from compositing, or subsequent draws go to the old surface.

## Cycle 1 Lessons
- No images = no package. Push for visual approximations even in text workflows.
- Secondary characters need design. Antagonists need design early.
- FX must be specified. Protect escalation arcs.

## Cycle 2 Lessons
- Confetti density scale: 5 levels (0–4). Pilot caps at Level 2/brief Level 3.
- The Corruption: system failure, right-angle motion, three tells. Stage 3: Byte Cyan vs Corruption Magenta.

## Cycle 3 Lessons
- Pipeline: OpenToonz + Krita + Natron (open source only).
- Naming: LTG_[CAT]_descriptor_v###.ext. Bit depth: 16-bit production.
- Byte float physics: sinusoidal, 24-frame cycle, 4-frame overshoot.
- Continuity Supervisor role defined.

## Cycle 4 Lessons
- OPEN SOURCE ONLY. Blend modes = Natron terminology.
- Tools index at output/tools/README.md — register all scripts.
- If a tool is missing, build it in Python.

## Cycle 5 Lessons
- **Byte body fill = #00D4E8 (Byte Teal)**; highlights = #00F0FF (Electric Cyan). This is intentional — shared visual DNA with Luma's pixel accents (#00F0FF). Distinction preserves figure-ground legibility.
- Byte Teal added as GL-01b in master_palette.md. Byte color model updated. Style guide "Shared Visual DNA" section added.
- Corrupted Amber (#FF8C00) 2px outline rule on Byte in cyan-dominant environments — already in palette, now cross-referenced.

## Cycle 6 Lessons
- **One fully rendered style frame produced:** `output/tools/style_frame_01_rendered.py` → `output/color/style_frames/style_frame_01_rendered.png`.
- **Three-light setup in code:** warm gold lamp (left/RGB glow), cyan monitor wall (right/filled gradient), lavender ambient (composite overlay). All named from master_palette.md.
- **draw_amber_outline()** must use ellipse offsets (not rectangles) — implemented correctly.
- **Luma face in a scene:** draw functions from luma_face_generator.py work when adapted with a scale parameter; eyes must shift pupils toward the subject of gaze (Byte = rightward).
- **Body construction for scene:** torso split warm/cyan-lit down vertical center; reaching arm uses CYAN_SKIN; lamp-facing left edge gets Soft Gold rim line.
- **Byte body = BYTE_TEAL (#00D4E8), not ELEC_CYAN (#00F0FF).** Emergence zone must be near-void dark so Byte pops.
- **Vignette + lavender ambient overlay:** use Image.composite() with an L-mode alpha mask to simulate ambient tint without RGBA mode complexity.
- **Victoria's mandate ACHIEVED:** characters are recognizable; emotional premise (girl discovering something impossible) legible without text; lighting tension (warm left / cold right) visible.
- **Cycle 7 remaining gaps:** Luma full-body turnaround, Miri redesign (flatter head), Cosmo silhouette feet/glasses, Glitch Layer orientation, Millbrook sky color.

## Cycle 8 Lessons
- **Lighting overlay alphas must be visible:** Warm zone alpha raised 28→70 (~27%); cold zone 22→60. Below 15% alpha overlays are invisible in rendered output.
- **Amber outline width = 3px** at 1920×1080. GL-07 standard. Never 4 or 5.
- **Hoodie underside = cool ambient** (SHADOW_PLUM, Cycle 8 interim). Away from all light sources — three-light logic demands cool lavender ambient, not warm.
- **Shoe spec:** SHOE_CANVAS=(250,240,220) cream main; SHOE_SOLE=DEEP_COCOA=(59,40,32). Previous code had these inverted.
- **Tendril cp1 must point TOWARD target:** cp1x = start + (target-start)*0.33, not start - offset. The tendril must arc toward Luma, not away.
- **Byte underbody glow:** draw_filled_glow() at bottom quarter of Byte, glow_rgb=ELEC_CYAN, to simulate CRT screen illuminating from below.
- **Charged gap:** Add draw_filled_glow() + pixel scatter at midpoint between tendril tip and Luma's hand. This space is the emotional center.
- **Lamp floor pool:** draw_filled_glow() at (lamp_x+32, H*0.85), rx=120, ry=44, LAMP_PEAK. Required for lamp spatial presence on floor.

## Cycle 11 Lessons
- **Mid-air transition element:** pixel confetti in x=768–960, y=200–700 (lamp–monitor boundary). Left of zone midpoint x=864: SOFT_GOLD/SUNLIT_AMBER/LAMP_PEAK/WARM_CREAM (warm-lit). Right of x=864: ELEC_CYAN/BYTE_TEAL/DEEP_CYAN/STATIC_WHITE (cold-lit). Seeded rng=77, 60 particles. Closes Victoria P1 (2 cycles).
- **Screen pixel figures minimum size = 15px wide.** Full 3-tier structure: head 5×4 + body 9×5 + legs 3×5 each. 7px was sub-legible. Rule: no pixel figures narrower than 14px on 1920px canvas.
- **Logo tagline removed.** "A cartoon series by the Dream Team" deleted from logo_generator.py STEP 11. Show title only on title card. No tagline before pitch.
- **byte.md version header:** Line 6 must always match colophon. v3.1 header now correctly states "3.1". Rule: whenever colophon is updated, update line 6 header on same edit.
- **Style guide sections 9/10/11 added:** Animation Style Notes (movement timing, Byte bob=24f, Luma lean rule, glitch effects instant), Glitchkin Construction Rules (pixel body, no fixed shape, corruption marks mandatory, always <Byte size), Prop Design Guidelines (warm material logic, retro-computing, cables always present, Glitch Layer = pure geometry, transition objects = clean-edge boundary).

## Cycle 10 Lessons
- **byte.md v3.1 complete.** All cube/chamfer/notch references purged from Sections 5, 6, 8, 10, 11, 12, size comparison, rationale. Section 10 (Turnaround) fully rewritten for oval — all five views describe oval arcs, ellipsoid depth, oval silhouettes. Quick Reference table updated. Document is now internally consistent.
- **Show logo exists:** `output/tools/logo_generator.py` → `output/production/show_logo.png`. "Luma" = SUNLIT_AMBER (#D4923A), "&" = WARM_CREAM neutral, "the Glitchkin" = ELEC_CYAN with pixel corruption. Dark void background with warm/cold zone glows and pixel border accents.
- **Luma lean = 48px** (was 28px). 48px at 170px torso = ~16°. Victoria's mandate: active urgency, not passive TV-watching. Rule: lean_offset must be ≥40px for any emotionally active Luma pose.
- **Screen content rule:** CRT screens must have pictorial content implying Byte's world — receding grid lines and pixel figure silhouettes establish origin. A blank cyan screen is "generic." Content is drawn in screen margins around the emergence void (which stays as dark void pocket). Draw order: screen background → grid → pixel figures → emergence void → glow rings.
- **byte.md DO NOT list — oval-specific rule:** Do not make the oval too smooth/round; keep glitch details (scar, cracked eye frame, pixel confetti) as angular/sharp to counterbalance the soft body shape.

## Cycle 9 Lessons
- **HOODIE_AMBIENT = #B06040** (RGB 176,96,64) = CHAR-L-08 finalized. Derivation: HOODIE_SHADOW (#B84A20) blended 70% with DUSTY_LAVENDER (#A89BBF) at 30%. Replaces SHADOW_PLUM permanently. Must retain orange component — pure cool shadow reads as separate material.
- **Couch scale corrected:** couch_left = W*0.16 (was W*0.04), couch_right = W*0.38 (was W*0.44). Span ~422px (~22%), ratio ~4.8:1 vs Luma's 88px. Target is 4:1. This was 4 cycles overdue — never defer couch/prop scale again.
- **Submerge/glow draw order:** Submerge fade must be drawn BEFORE screen-glow. If submerge paints near-black AFTER the glow, the glow is invisible. Rule: establish dark field first, then paint light on top.
- **Overlay draw order:** Atmospheric overlay must be applied BEFORE characters, not after. Characters have baked-in three-light values; applying the overlay on top double-tints warm hoodie (+yellow) and cyan arm (+wash). Fixed: overlay at STEP 3, characters at STEP 4+.
- **False comments propagate:** The "arm span ~21%" comment was false from Cycle 7 and carried forward unchanged. Always verify comment claims match computed geometry.
- **Byte body = OVAL (canonical from Cycle 8).** byte.md updated to Version 3.0; chamfered-box design retired. Any new artist should draw oval, not cube.
- **MIRI-A locked** as canonical Grandma Miri design (bun+chopsticks+cardigan+soldering iron). MIRI-B archived. Maya notified.
- **Cycle 10 remaining gaps:** Luma full-body turnaround, Cosmo silhouette feet/glasses, Glitch Layer background, composite reference image (all 4 characters at scale — Dmitri P0 now 5 cycles overdue), Millbrook sky color, naming convention reconciliation pass.

## Cycle 7 Lessons
- **All 11 critic bugs fixed in style_frame_01_rendered.py:**
  1. `draw_lighting_overlay()` implemented — warm gold RGBA pool (left), cold cyan RGBA wash (right), composited by zone.
  2. Flat DUSTY_LAVENDER full-frame overlay removed — it was collapsing the warm/cold split.
  3. Luma `luma_cx` moved from 19% → 29% — arm span now ~21% of canvas (was ~40%).
  4. Neck polygon added connecting torso_top to head base — no more floating head.
  5. Torso seam fixed — row-by-row warm/cool gradient blend (no hard center seam).
  6. Vignette revised — darkens top/bottom bands only (not all 4 corners).
  7. Blush fixed — RGBA layer composite at 80/255 alpha, no skin cover ellipses.
  8. Monitor screens: `BYTE_TEAL` → `ELEC_CYAN` (GL-01, not GL-01b).
  9. Byte submerge fade: interpolation target changed from ELEC_CYAN → `(14,14,30)` (actual void pocket color).
  10. All inline color tuples named as constants (JEANS, JEANS_SH, COUCH_*, BLUSH_*, LAMP_PEAK).
  11. Body lean: `lean_offset=28px` applied row-by-row to torso top, arm shoulder, and neck.
- **RGBA composite technique:** use `Image.new("RGBA")` + `ImageDraw.Draw()` + `Image.alpha_composite()` for any additive overlay; then `.convert("RGB")` and `.paste()` back.
- **Luma position in generate():** luma_cx = int(W * 0.29). Arm target = scr_x0 - 20.
- **draw_luma_body() now returns:** `head_cx`, `head_cy`, `hand_cx`, `hand_cy`.
- **LAMP_PEAK = (245,200,66):** intentionally slightly warmer than SOFT_GOLD — peak emission is hotter. Documented inline.
- **Couch colors:** COUCH_BODY=(107,48,24), COUCH_BACK=(128,60,28), COUCH_ARM=(115,52,26) — candidates for DRW-06 in master_palette.md. Coordinate with Sam.
- **Cycle 8 remaining gaps:** Luma full-body turnaround, Miri redesign, Cosmo silhouette feet/glasses, Glitch Layer orientation, Millbrook sky color. Also: palette compliance for JEANS/SKIN/COUCH entries.
