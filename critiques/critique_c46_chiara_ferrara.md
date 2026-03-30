# Critique C46 — Background Environments & Style Frames
## Critic: Chiara Ferrara — Background Art & Environment Design

**Date:** 2026-03-30
**Cycle:** 46
**Scope:** Complete pitch — all environment backgrounds, style frames with environments, and environment-related production specs
**Assets reviewed:** Classroom v004, School Hallway v005, Grandma Living Room v003, Grandma Kitchen v007, Luma Study Interior, Tech Den v007, Millbrook Main Street, Glitch Layer ENV/Encounter/Frame, Other Side ENV; SF01–SF06 (Discovery, Glitch Storm, Other Side, Resolution, The Passing, The Hand-Off); COVETOUS style frame; CRT Glow Profile data; CORRUPT_AMBER Fringe Spec
**Tools used:** LTG_TOOL_render_qa.py, LTG_TOOL_sobel_vp_detect.py (with vp_spec_config.json)

---

## Preamble — What Has Changed Since C16

My C16 critique (Cycle 39) issued priority actions on five environments. I am reviewing the results of those actions alongside all new/updated assets.

**C16 priority action outcomes:**
1. School Hallway SUNLIT_AMBER drift — RESOLVED. v005 render_qa shows warm/cool 34.8 PASS and line weight 0 outliers PASS. The hallway and its v004 variant appear identical; I presume v005 is the canonical output now.
2. Kitchen atmospheric recession — IMPROVED. v007 now shows line_weight 0 outliers (was 3), value min=21. Paper texture and vignette passes are working.
3. Living Room perspective inconsistency — PARTIALLY ADDRESSED. v003 has CRT repositioned to center (good) and reading lamp moved left. But the fundamental flat-wall vs converging-floor VP conflict I flagged persists (see below).
4. Tech Den floor perspective — RESOLVED STRUCTURALLY. v007 migrated to output_dir(), warm/cool 102.9 PASS. The separation is now very high — possibly over-corrected. See detailed review.
5. Millbrook Main Street value floor — UNRESOLVED. Value min=45, still fails the min<=30 spec. This has now persisted through three critique cycles.

---

## 1 — CLASSROOM v004

**QA:** WARN | value min=14 max=251 PASS | warm/cool 17.0 PASS | line weight outliers=1 PASS | color fidelity WARN | VP detect FAIL (conf=0.064)

Score: 68/100
- I found 2 perspective concerns. The desk rows should converge to VP_X=192 but read as uniform rectangles scattered on the floor with no size diminution or spacing convergence toward the vanishing point. The checkerboard floor tiles do converge, but the desks sitting on them do not — they are the same size at every depth. This breaks the floor plane's credibility.
- The large elliptical vignette overlay is visually dominant and clips the upper corners of the room, giving the impression of a fisheye lens applied post-render rather than an atmospheric effect. Vignette should darken corners, not crop architectural geometry.
- The red vertical element at center-right reads as a structural column but it does not connect to the ceiling or floor in a structurally coherent way. If it is a column, it needs a base and a capital or bracket. If it is a pipe, it should be thinner and less visually dominant.
- Warm/cool separation at 17.0 is healthy. The dual-temperature split (warm ceiling/window top vs cool floor bottom) is working.
- Bottom line: The floor plane is convincing; the objects sitting on it are not participating in the same perspective system.

---

## 2 — SCHOOL HALLWAY v005

**QA:** WARN | value min=19 max=237 PASS | warm/cool 34.8 PASS | line weight outliers=0 PASS | color fidelity WARN | VP detect FAIL (conf=0.037)

Score: 74/100
- This is the strongest one-point perspective composition in the suite. Floor tile convergence to center VP is consistent. Both wall planes recede correctly. The locker banks diminish in apparent size as they recede. The T-intersection window at the far end anchors the VP with real architectural logic. This hallway can be walked through.
- I found 1 perspective concern: the left-wall door (light blue rectangle with triangular markers) does not diminish proportionally with depth — it appears the same height as the foreground lockers despite being set deeper into the corridor. Its bottom edge does not sit on the converging floor plane.
- The SUNLIT_AMBER warm shaft from the upper-left window is now compositionally effective as a foreground warm anchor. The fluorescent cool cast on the right side creates genuine dual-temperature space.
- The backpack (lower right) and bulletin board items (upper left) are correctly placed as inhabitant evidence — this space is used by children. Good environmental storytelling.
- The school seal and far window read correctly as depth anchors. Atmospheric haze at the far end is present but could be pushed further — the far-end wall values should be 15-20% lighter than they currently are.
- Bottom line: The best interior perspective in the project; minor depth-scaling inconsistency on the left door and insufficient atmospheric recession at the far end keep it from top marks.

---

## 3 — GRANDMA'S LIVING ROOM v003

**QA:** WARN | value min=26 max=254 PASS | warm/cool 47.3 PASS | line weight outliers=2 PASS | color fidelity WARN | VP detect FAIL (conf=0.048)

Score: 62/100
- I found 3 perspective errors. They are as follows: (1) The back wall reads as completely flat-on (no convergence, no recession, rectangular fill) while the floor shows convergent lines radiating from the CRT stand area. These two planes do not agree on camera position. A viewer looking at this room sees two different cameras simultaneously. (2) The bookshelf/curtain unit on the left is drawn in flat elevation — no foreshortening, no converging verticals — while adjacent objects on the floor plane show perspective convergence. (3) The family photo frames on the right wall are drawn as identical-sized rectangles with equal spacing, showing no size diminution with depth. Even at this mild 3/4 angle, the rightmost frame should be visibly smaller than the leftmost.
- The C46 CRT reposition to center (stand W*0.38-0.52) is the correct staging decision for SF06. The warm/cool separation at 47.3 is now very strong — the SUNLIT_AMBER left / CRT_COOL_SPILL right split reads clearly.
- The reading lamp repositioned to left side (W*0.20) provides a warm focus for Miri's staging zone. Good.
- The rug on the floor is the only object that attempts to show perspective foreshortening, and it succeeds — the far edge is narrower than the near edge. This makes the non-foreshortened furniture look worse by comparison.
- Value range is healthy at min=26, max=254 — the CRT screen reaches near-white and deep shadows exist.
- **The flat back wall problem I flagged in C16 persists.** Three critique cycles without resolution. This is the Miri family living room — the emotional center of the show's generational theme. The back wall must work in perspective or the room falls apart when characters are composited into it.
- Bottom line: Strong color and light logic; the perspective inconsistency between the flat back wall and the converging floor plane remains the critical structural problem, now in its fourth review cycle.

---

## 4 — GRANDMA'S KITCHEN v007

**QA:** WARN | value min=21 max=228 PASS | warm/cool 32.9 PASS | line weight outliers=0 PASS | color fidelity WARN | VP detect FAIL (conf=0.063)

Score: 72/100
- The paper_texture + vignette + flatten_rgba_to_rgb passes added in C44 have resolved the line weight outlier problem (was 3, now 0). This is a real improvement.
- Warm/cool separation at 32.9 remains strong. The morning sunlight vs cool floor zone differentiation is working.
- Value ceiling at 228 is lower than ideal — the window (a primary light source) and the CRT through the doorway should have specular hotspots approaching 255. Without them, the light sources feel painted rather than emitting.
- The flat-elevation drawing style for cabinets and appliances is consistent with the show's stylization — I accept this as a deliberate choice given the overall simplification level. However, the countertop edge should converge toward VP_X=512 from both sides, and currently it reads as a single horizontal line.
- The CORRUPT_AMBER fringe spec (C46) is now formalized as a production standard. I reviewed the spec document — it is thorough and correct in its placement logic (CRT glow boundary, alpha ceiling 15%, rendering order). However, I cannot visually confirm the fringe in the kitchen PNG at this resolution. At 4px height and 15% alpha, it may be below the visual detection threshold at 1280px. This is acceptable — the spec states it should be "felt before it is consciously identified."
- Bottom line: A solid working kitchen with resolved QA issues; the value ceiling and countertop perspective convergence are the remaining gaps.

---

## 5 — LUMA'S STUDY INTERIOR

**QA:** WARN | value min=28 max=248 PASS | warm/cool 33.1 PASS | line weight outliers=2 PASS | color fidelity WARN | VP detect FAIL (conf=0.032)

Score: 65/100
- I found 2 perspective errors. (1) The bookshelf is drawn in flat elevation — a rectangular grid of colored book spines with no convergence toward VP_X=230, VP_Y=273. The shelf is the largest furniture object in the room and it should show the most perspective distortion at this 3/4 angle. (2) The desk/CRT area on the right half reads as a separate flat-plane composition pasted onto a different background. The desk surface is a horizontal band, the CRT sits on it without any converging edges, and the window (a blue rectangle) floats above without connection to the wall plane.
- The three-light system (CRT key, warm bedside lamp, cool night window) is conceptually correct and the warm/cool separation at 33.1 confirms it is working at a color-metric level. The CRT glow is the dominant cool source and it should be — this is the inciting-incident room where the screen comes alive.
- The vignette is extremely heavy — the elliptical darkening effect clips all four corners and makes the room feel circular rather than rectangular. A bedroom is a box. The vignette should soften corners, not reshape them.
- The Miri knitted toy Easter egg and framed photo are good environmental storytelling details that connect this room to the generational narrative.
- Bottom line: Correct light logic and narrative details; the flat-elevation furniture and heavy vignette undermine the spatial coherence of what should be the show's most intimately understood room.

---

## 6 — TECH DEN v007

**QA:** WARN | value min=11 max=254 PASS | warm/cool 102.9 PASS | line weight outliers=1 PASS | color fidelity WARN | VP detect FAIL (conf=0.059)

Score: 60/100
- Warm/cool separation at 102.9 is the highest in the suite by a wide margin (next highest: Living Room at 47.3). This is a 2x overshoot. The metric measures median hue difference between top and bottom halves; a separation this extreme means the top and bottom are almost chromatically unrelated. Cosmo's den has warm windows AND cool monitors — both should be present in both halves. The current extreme split suggests the warm and cool zones are stacked in horizontal bands rather than organically mixed through the space.
- Value range min=11 max=254 is the widest in the suite. The deep darks are good. But min=11 is so dark that areas of the image may read as pure black on uncalibrated screens. This is borderline — keep the deep shadows but ensure they carry some color information.
- I found 2 perspective errors. (1) The monitor bank reads as a flat elevation — four identical circles (monitors) arranged in a grid with no size diminution or convergence. The monitors should be drawn in perspective consistent with VP_X=820. (2) The chair/desk area shows no depth — the chair, desk surface, and monitor stands all sit on the same visual plane with no overlap or occlusion hierarchy.
- The migration to output_dir() is a pipeline improvement but has no visual impact. The underlying spatial problems from C16 — flat floor planks, non-converging furniture — remain structurally unchanged.
- Bottom line: Metric improvements mask persistent perspective failures; the extreme warm/cool split and the flat furniture elevation make this the weakest Real World interior in the suite.

---

## 7 — MILLBROOK MAIN STREET

**QA:** WARN | value min=45 max=239 PASS (value range 194 — renders_qa flags this as FAIL for pass=False) | warm/cool 21.2 PASS | line weight outliers=1 PASS | color fidelity WARN | VP detect FAIL (conf=0.047)

Score: 55/100
- **Value floor at 45 — third consecutive critique cycle without resolution.** The spec requires min<=30 for shadow anchoring. An exterior afternoon scene should have shadows under awnings, in doorway recesses, and behind tree trunks that reach into the low-value range. At min=45, there are no real shadows in this scene. Everything is lit. A town with no shadows is a town with no sun — despite the warm afternoon sky and golden tree foliage saying otherwise.
- The power line catenary curves and road plane are architecturally correct improvements from earlier versions. Road perspective with center line convergence works.
- The buildings read as a flat frieze — a stage backdrop rather than a receding street. Buildings should diminish in size toward the VP at x=742. The far-end buildings are the same height as the near buildings. There is no atmospheric recession: no value desaturation, no edge softening, no haze at the far end. Millbrook's main street extends to infinity at identical contrast.
- The autumn trees are the strongest environmental storytelling element — they say season, they say small town, they say lived-in. But they are drawn at identical scale regardless of depth position, which contradicts the street's perspective recession.
- Bottom line: The weakest environment in the suite — value floor unresolved across three cycles, no atmospheric recession, no depth-scaled elements. This street cannot be believed.

---

## 8 — GLITCH LAYER ENVIRONMENTS (Other Side, Encounter, Frame)

**Other Side ENV:**
Score: 70/100
- The platform tier system (NEAR cyan, MID desaturated, FAR near-void) is the correct approach to non-perspective depth in a digital space. The inverted atmospheric perspective (brighter elements closer, dimmer farther) is the right creative choice for a world that does not follow real-world physics.
- The data waterfall (blue vertical column) is a strong architectural landmark that anchors spatial orientation. A viewer can locate themselves relative to the waterfall.
- The UV_PURPLE sky gradient works as an infinite-space backdrop. The floating rectangular slabs provide scale reference.
- The orange/amber warm element (Real World debris) creates a narrative contrast point. Its position mid-frame at a platform junction reads correctly as "foreign object in digital space."
- Remaining gap: the lower-left platform with circuit traces and pixel flora is dense with detail while the right half is sparse. The asymmetry is not compositionally motivated — it reads as unfinished rather than intentional.
- Bottom line: The best Glitch Layer environment; the tier depth system works and the inverted atmospheric logic is consistent.

**Glitch Layer Encounter:**
Score: 58/100
- The three-tier platform system is present but the tiers are not visually differentiated enough. The NEAR tier (large cyan bar) dominates the frame; the MID and FAR tiers are small, scattered, and read as decoration rather than navigable space.
- The purple/magenta aurora at top is the only atmospheric depth cue beyond scale. More atmospheric differentiation is needed between tiers.
- Bottom line: Functional but spatially thin; the encounter space needs more tier differentiation.

**Glitch Layer Frame:**
Score: 52/100
- Similar to Encounter but with even less spatial differentiation. The platforms float in void with no clear spatial relationship. There is no environmental storytelling — nothing tells you what this space is for or why it exists. It is a platform floating in purple-black.
- Bottom line: The weakest Glitch environment; needs environmental specificity and tier depth cues.

---

## 9 — STYLE FRAMES — Environment Assessment

**SF01 "Discovery" (Luma Study):**
Score: 66/100
- The study background in this style frame is a different asset from LTG_ENV_luma_study_interior.png — it appears to be the older legacy version (LTG_ENV_lumashome_study_interior.png). The newer study ENV has a bookshelf, night window, and CRT; this SF01 background shows a different furniture arrangement. **Consistency flag: which study interior is canonical for SF01?** If the Hana Okonkwo C42 rebuild is canonical, SF01 should use it.
- The CRT glow reads correctly as the scene's dramatic focal point. Luma's position in the warm zone reaching toward the CRT/cool zone is correct character-environment integration.
- Bottom line: Functional but the background asset may be stale relative to the canonical study interior.

**SF02 "Glitch Storm":**
Score: 62/100
- The exterior street scene at night with Glitch storm overhead. Buildings recede with some depth but the ground plane is a flat horizontal band. Characters stand on a thin ledge with no visible ground recession. The cityscape silhouette provides depth layering (foreground dark buildings, mid confetti, background storm sky) but the ground plane undermines it.
- The confetti burst in the upper right is a strong atmospheric element. The building silhouettes create a convincing contested-space composition.
- Bottom line: Strong atmospheric staging; the flat ground plane is the environment's main spatial weakness.

**SF04 "Resolution" (Kitchen):**
Score: 68/100
- The kitchen background here is simplified from the full kitchen ENV — flat warm bands with a dark CRT doorway zone. The warm/cool split is clear and the CORRUPT_AMBER fringe spec applies here (this is the canonical reference implementation).
- Luma's placement in the warm foreground with the CRT threshold in the background is correct depth staging. The character occupies the right spatial tier.
- The upper and lower dark bands (black bars) consume a significant portion of the frame. This may be intentional (letterbox for cinematic feel) but it wastes vertical space where kitchen architecture could provide context.
- Bottom line: Correct light and staging logic; the simplified background trades spatial richness for clarity.

**SF05 "The Passing" (Kitchen):**
Score: 64/100
- Miri and Luma in the kitchen morning scene. The warm/cool split from the top warm gradient to the cool lower zone works. But both characters appear to float — their feet do not connect to a visible floor plane. The kitchen architecture is reduced to horizontal bands with no furniture, no countertop, no window — just temperature zones.
- The CRT visible through the doorway (background center) maintains the show's central object. Good.
- Bottom line: The temperature-zone approach works for color mood but the characters need a floor to stand on.

**SF06 "The Hand-Off" (Living Room):**
Score: 70/100
- The strongest style frame for environment-character integration. Miri and Luma flank the centered CRT in the living room. The warm/cool left-right split (SUNLIT_AMBER L / CRT_COOL_SPILL R) is clear and character-motivated: Miri in the warm traditional zone, Luma in the cool digital-adjacent zone.
- The living room background is simplified but legible — bookshelf on left, CRT center, family photos right, rug on floor. The floor shows perspective convergence lines radiating from the CRT base, which is a good spatial anchor.
- Both characters' feet are on the floor plane. Their scale relative to the CRT and room is proportionally correct.
- The reading lamp repositioned to the left (per v003 update) provides a motivated warm source for Miri's staging zone.
- Remaining gap: the back wall above the CRT is flat and featureless. In a character-driven style frame, the wall behind the characters should carry emotional information — Miri's history, family photos at visible scale, a clock showing time of day.
- Bottom line: The best character-environment integration in the suite; the warm/cool staging is narratively motivated and spatially coherent.

**COVETOUS Style Frame (Glitch Layer):**
Score: 72/100
- Three-character triangulation (Glitch L, Byte center, Luma R) on a single platform with UV_PURPLE void. The ACID_GREEN sight-line from Glitch to Luma is an effective spatial and narrative annotation. Byte's barrier positioning between them is correct.
- The horizontal cyan platform lines provide a ground reference. The dark platform slabs in the background provide depth layering. The space is minimal but the character staging makes it work.
- Luma's warm orange reads correctly as "foreign warmth in cold space" per the show's temperature logic.
- Bottom line: Effective minimalist staging; the character triangulation carries the spatial logic that the sparse environment does not.

---

## 10 — CRT GLOW PROFILES (New C46 Spec Data)

Score: N/A (specification data, not visual asset)
- The CRT glow profile extraction tool has produced empirical data: median FWHM 27.4% diagonal, median amplitude 49.4, median CCT 13070K across 10 good-fit reference photos. This gives the team a measurable target for CRT glow rendering.
- The recommended generator params (sigma_frac=0.1165, fwhm_frac=0.2744) should be cross-checked against the existing CRT glow implementations in the study, living room, and kitchen generators. If the current generators are using significantly different sigma values, the CRT glow will feel inconsistent between environments.
- Bottom line: Valuable reference data; the team should audit existing CRT glow implementations against these measured parameters.

---

## 11 — CORRUPT_AMBER FRINGE SPEC (New C46 Spec)

Score: N/A (specification document, not visual asset)
- The spec is thorough, well-structured, and addresses the right questions: what it is, when it appears, how it renders, and how it interacts with the QA pipeline. The distinction from lamp amber (same hex, different narrative role) and from The Corruption (different palette entirely) is correctly drawn.
- The alpha ceiling (15%), band height (sp(6)=4px at 1280x720), and lateral inset (sp(4)) are conservative — appropriately subtle for a contamination detail.
- The rendering order (after CRT glow, before characters) is correct for compositing integrity.
- **One concern:** the spec defines CORRUPT_AMBER as GL-07 (#FF8C00) — a Glitch Layer palette entry intentionally placed in a Real World scene. This is the first formal exception to the "zero Glitch palette in Real World" rule. The spec acknowledges this but the QA tool exemption needs to be implemented before the next precritique run, or it will flag as a palette violation.
- Bottom line: A well-reasoned production spec that codifies a narratively important visual detail.

---

## 12 — VP DETECTION TOOL ASSESSMENT

All 7 Real World environments returned VP detect FAIL (confidence 0.032-0.064, all below 0.15 threshold). The tool uses Sobel edge detection and HoughLinesP to find line convergence — this approach struggles with PIL-generated procedural images because the edges are algorithmically regular rather than painted. The tool is correctly identifying that the generated environments do not produce strong convergent-line signals, which correlates with my visual assessment that most environments have flat-elevation furniture that does not converge to the stated vanishing points.

**Recommendation:** The VP detect tool confirms my per-asset findings. The Real World interiors need their furniture, shelving, and props drawn with perspective convergence matching the floor plane. The floor planes are generally correct; everything sitting on them is not.

---

## SUMMARY — Priority Actions

| Priority | Asset | Issue | Impact |
|---|---|---|---|
| P0 | Millbrook Main Street | Value floor 45, no shadows, no atmospheric recession — 3 cycles unresolved | Pitch-critical exterior is not believable |
| P0 | Living Room v003 | Flat back wall vs converging floor — 4 cycles unresolved | Emotional center of the show has broken perspective |
| P1 | All Real World interiors | Furniture drawn in flat elevation, not in perspective | Every interior has objects that do not participate in the room's spatial system |
| P1 | Classroom v004 | Desks not diminishing with depth; vignette clips architecture | Space readable at floor level but not at furniture level |
| P2 | Tech Den v007 | Warm/cool 102.9 is over-corrected; monitor bank in flat elevation | Cosmo's space still does not work spatially |
| P2 | Luma Study | Bookshelf flat elevation; vignette too heavy | Inciting-incident room needs spatial coherence |
| P2 | SF01 | Background asset may not match canonical study interior (C42 rebuild) | Asset consistency across the pitch |
| P3 | Glitch Layer Frame | Weakest GL environment; no tier differentiation or storytelling | Upgrade or retire |

---

**Overall assessment:** The show's environments have made measurable progress on color metrics (warm/cool separation, value ranges, canonical color anchoring) since C16. The color infrastructure is now solid. The persistent weakness is spatial: furniture, shelves, monitors, and props are drawn in flat elevation while the floor planes beneath them converge correctly. This contradiction is present in every Real World interior. A viewer will feel something is wrong with these rooms without being able to articulate why. The fix is systematic: every piece of furniture needs to converge to the room's vanishing point. This is not a style choice — the show has not committed to a non-realistic perspective system — it is an error, and it is the single most important improvement the background team can make.
