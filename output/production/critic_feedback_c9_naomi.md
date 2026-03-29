# Critic Feedback — Cycle 9
## Naomi Bridges, Color Theory Specialist
**Date:** 2026-03-29 22:00
**Subject:** Cycle 9 Visual Review — style_frame_01_rendered.py, master_palette.md (Sections 5/6/7), bg_glitch_layer_frame.py

---

## Files Reviewed

- `/home/wipkat/team/output/tools/style_frame_01_rendered.py` (Cycle 9 revision)
- `/home/wipkat/team/output/color/palettes/master_palette.md` (Sections 5, 6, 7)
- `/home/wipkat/team/output/production/statement_of_work_cycle9.md`
- `/home/wipkat/team/output/tools/bg_glitch_layer_frame.py` (new this cycle)
- `/home/wipkat/team/output/production/critic_feedback_c8_naomi.md` (reference — my Cycle 8 report)

---

## Part 1 — Cycle 8 Issue Verification

Six issues from my Cycle 8 critique required direct action this cycle. I am verifying each against the code and documentation.

---

### ITEM C8-1: CHAR-L-08 Finalized — `#B06040` HOODIE_AMBIENT, not SHADOW_PLUM?

**Cycle 8 status: PLACEHOLDER — SHADOW_PLUM interim, hex TBD**
**Cycle 9 status: FULLY RESOLVED**

Evidence in `style_frame_01_rendered.py`, lines 81–87:
```python
# ── Derived hoodie ambient — CHAR-L-08 (Alex Chen Cycle 9) ───────────────────
# Hoodie underside faces down, away from lamp and monitor. Receives lavender ambient only.
# Derived: HOODIE_SHADOW (#B84A20, RGB 184,74,32) blended with DUSTY_LAVENDER (#A89BBF)
# at 70/30 ratio → RGB(176,96,64) = #B06040.
# Reads as orange hoodie fabric under lavender ambient fill — not an architectural shadow.
# Replaces SHADOW_PLUM which lacked orange component and read as a separate material.
HOODIE_AMBIENT  = (176,  96,  64)   # CHAR-L-08 (#B06040) — hoodie underside, lavender ambient tinted
```

Evidence at draw site, lines 589–599: the hoodie underside polygon fills with `HOODIE_AMBIENT`. `SHADOW_PLUM` is still defined at line 54 (as a palette member, correctly) but is no longer referenced on the underside polygon. The replacement is clean and the derivation rationale is inline.

Evidence in `master_palette.md` CHAR-L-08 (lines 1049–1059): the entry documents the finalized hex `#B06040`, provides the 70/30 blend derivation, explains why SHADOW_PLUM was wrong as a permanent solution, and marks the Cycle 8 placeholder as retired.

**Color theory assessment:** `#B06040` is RGB (176, 96, 64). Let me verify the derivation claim. HOODIE_SHADOW = (184, 74, 32). DUSTY_LAVENDER = (168, 155, 191). A 70/30 blend: R = 184*0.7 + 168*0.3 = 128.8 + 50.4 = 179.2; G = 74*0.7 + 155*0.3 = 51.8 + 46.5 = 98.3; B = 32*0.7 + 191*0.3 = 22.4 + 57.3 = 79.7. This gives approximately (179, 98, 80). The code value is (176, 96, 64). There is a discrepancy of approximately R:-3, G:-2, B:-16. The blue channel diverges from the formula by 16 points — a non-trivial deviation that makes the value meaningfully warmer and less lavender-influenced than a strict 70/30 blend would produce.

**This is a real discrepancy.** The documentation says 70/30 yields (176, 96, 64) — but actual 70/30 arithmetic gives approximately (179, 98, 80). The delivered hex is warmer and darker in blue than the stated derivation. Either the blend ratio is not exactly 70/30, or a rounding or gamma correction step occurred. The delivered value is not wrong on color theory grounds — it is acceptable as a lavender-ambient-tinted hoodie shadow. But the documentation claims an arithmetic derivation that does not check out. This needs to be reconciled: either document the actual ratio used, or correct the hex to match the stated 70/30 derivation.

This is now a Priority 3 documentation accuracy issue, not a color defect.

**This issue is substantially resolved. One documentation accuracy note remains.**

---

### ITEM C8-2: SHOE_CANVAS/SHOE_SOLE Local Aliases Removed?

**Cycle 8 status: DEFECT — local aliases for module constants**
**Cycle 9 status: FULLY RESOLVED**

Evidence at lines 554–565 in `draw_luma_body()`:
```python
# Aliases removed (Cycle 9): SHOE_CANVAS and SHOE_SOLE were local duplicates of module constants.
# Left shoe
draw.rectangle([luma_x - 60, y_base - 10, luma_x - 8, y_base + 22],
               fill=WARM_CREAM)
draw.rectangle([luma_x - 62, y_base + 16, luma_x - 6, y_base + 26],
               fill=DEEP_COCOA)
# Right shoe
draw.rectangle([luma_x + 2,  y_base - 10, luma_x + 58, y_base + 20],
               fill=WARM_CREAM)
draw.rectangle([luma_x,      y_base + 16, luma_x + 60, y_base + 26],
               fill=DEEP_COCOA)
```

The local variables are gone. `WARM_CREAM` (RW-01) and `DEEP_COCOA` (RW-12) are referenced directly. The comment explicitly attributes the change to Cycle 9 cleanup and states the reason.

Evidence in `master_palette.md` CHAR-L-09 and CHAR-L-10 (lines 1027–1045): both entries are now present in Section 5, documenting that Luma's shoe canvas = RW-01 and sole = RW-12. The entries state explicitly "references the RW-01 module constant directly; do not create a separate shoe-specific alias."

This is clean. This issue is closed.

---

### ITEM C8-3: CABLE_NEUTRAL_PLUM Named Constant at Module Level?

**Cycle 8 status: DEFECT — inline tuple (80, 64, 100) at line 470; PROP-07 had no hex**
**Cycle 9 status: FULLY RESOLVED**

Evidence at line 110 in `style_frame_01_rendered.py`:
```python
CABLE_NEUTRAL_PLUM = ( 80,  64, 100) # Desaturated Shadow Plum mid — PROP-07 (#504064)
                                    # Replaces former (100,100,100) neutral grey (no palette home).
```

Evidence at line 486: the fg_cables array now references `CABLE_NEUTRAL_PLUM` by name rather than the raw tuple.

Evidence in `master_palette.md` PROP-07 (lines 926–936): the constant name is documented, the hex `#504064` is specified, the derivation note is present, and the Cycle 9 finalization is attributed.

This issue is closed.

---

### ITEM C8-4: Cold Overlay Alpha (C8-4) — Verified/Adjusted?

**Cycle 8 status: MONITORING CONCERN — cold overlay at alpha_max=60 may over-correct**
**Cycle 9 status: NOT ADDRESSED — alpha unchanged, no render review documented**

Evidence at lines 1083–1085 in `style_frame_01_rendered.py`:
```python
# Cycle 8 fix (Victoria + Naomi): raised from alpha=22 to alpha=60
# Old alpha of 22 (~9%) contributed nothing structural to the frame.
alpha = int(60 * (1 - t))
```

The cold overlay alpha remains at 60. The SOW for Cycle 9 makes no mention of render review for the warm/cold boundary zone. My Cycle 8 concern was that a 60-alpha cold wash against a 70-alpha warm wash, with the cold covering a larger area footprint (rx = W*0.55, ry = H*0.65 with an 80px left spill into warm territory), creates a grey mid-zone on Luma's body.

I raised this as a monitoring concern, not a defect. The SOW should have documented whether this was checked. It was not. This moves from a monitoring concern to an open action item.

**Required action (C9-4 forward):** Render the frame, examine Luma's body at the compositional center (approximately x = W*0.4–0.5). If the skin and hoodie surfaces in that zone read as blue-grey rather than the warm/cool split, reduce the cold overlay alpha from 60 to 40–45. This has been open since Cycle 8. It cannot carry over again.

---

### ITEM C8-5 (Implicit): PROP-07 — Hex Finalized in master_palette.md?

**Cycle 8 status: DEFECT — PROP-07 had no hex; "desaturated Shadow Plum mid" with no value**
**Cycle 9 status: FULLY RESOLVED** (addressed in C8-3 above)

---

### ITEM C8-6 (Implicit): Section 7 Skin System — Does It Resolve the Three-Value Discrepancy?

**Cycle 8 status: REQUIRED — Fiona O'Sullivan's three-value skin discrepancy unresolved**
**Cycle 9 status: FULLY RESOLVED — with one remaining action item**

The three-value discrepancy was: `master_palette.md` RW-10 = `#C4A882`, `luma_color_model.md` = `#C8885A`, `style_frame_01_rendered.py` = `#C8885A` (via SKIN constant). These three sources gave painters three different answers to "what is Luma's skin color?"

Section 7 resolves this with a two-tier system (documented at lines 1065–1157):
- **Tier 1:** `#C4A882` (RW-10) remains the canonical neutral-light base. Correct for unspecified lighting.
- **Tier 2:** `#C8885A` (CHAR-L-01) is the scene-specific derivation for Frame 01's warm lamp setup. It is not a contradiction — it is what `#C4A882` looks like under Soft Gold key light.

The warm/cool skin tables in sections 7.4 and 7.5 are thorough and correct. The decision tree (RW-10 → scene-specific CHAR-L-xx → DRW-xx per environment) is now legible to a painter.

**Remaining action item (documented in Section 7.6):** The skin entry in `luma_color_model.md` should add a cross-reference note stating that `#C8885A` is the lamp-lit derivation of `#C4A882`. This was explicitly flagged in Section 7.6. It is not a palette defect — it is a documentation hygiene task. I expect it completed in Cycle 10.

**The skin discrepancy is resolved at the palette level. The cross-reference note in luma_color_model.md is outstanding.**

---

## Part 2 — New Work: bg_glitch_layer_frame.py

This is Jordan Reed's Cycle 9 contribution. I am evaluating it against the Glitch Layer color specifications in `master_palette.md`.

---

### Assessment 1: Core Palette Mapping

The script's palette block at lines 42–72 maps as follows:

| Code Constant | RGB | Palette Reference | Hex Match? |
|---|---|---|---|
| `VOID_BLACK` | (10, 10, 20) | GL-08 `#0A0A14` | CORRECT |
| `BELOW_VOID` | (5, 5, 8) | GL-08a `#050508` | CORRECT |
| `ELEC_CYAN` | (0, 240, 255) | GL-01 `#00F0FF` | CORRECT |
| `DEEP_CYAN` | (0, 168, 180) | GL-01a/GL-02 area | Approximate — GL-02 is `#00A8B4` = (0, 168, 180). CORRECT |
| `UV_PURPLE` | (123, 47, 190) | GL-04 `#7B2FBE` | CORRECT |
| `DEEP_VOID` | (58, 16, 96) | GL-04a `#3A1060` | CORRECT |
| `ATMOS_MID_PURPLE` | (74, 24, 128) | GL-04b `#4A1880` | CORRECT |
| `DATA_BLUE` | (43, 127, 255) | GL-06 `#2B7FFF` | CORRECT |
| `DEEP_DATA_BLUE` | (16, 64, 160) | GL-06a `#1040A0` | CORRECT |
| `ACID_GREEN` | (57, 255, 20) | GL-03 `#39FF14` | CORRECT |

Every primary palette constant in `bg_glitch_layer_frame.py` traces directly to a named, documented GL-xx palette entry. There are no orphan inline tuples among the named constants. This is the cleanest palette mapping I have seen from this team.

**This is genuinely good practice.**

---

### Assessment 2: Derived Depth Tier Colors

The three-tier platform depth system (NEAR/MID/FAR) uses derived values that are NOT direct GL-xx constants:

- `NEAR_COLOR = ELEC_CYAN` — direct GL-01 reference. Correct.
- `NEAR_SHADOW = DEEP_CYAN` — GL-02 shadow companion. Correct.
- `NEAR_EDGE = (180, 255, 255)` — bright edge highlight on NEAR platforms. This is **undocumented** in master_palette.md. It is brighter and more desaturated than GL-01 (`#00F0FF`). The value (180, 255, 255) is approximately 70% white mixed into ELEC_CYAN — it reads as a near-white edge glow, which is correct visually (a bright platform edge hit by its own ELEC_CYAN emission). However, there is no palette entry for this value and no documentation comment at the point of definition.
- `MID_COLOR = (10, 72, 120)` — described as "desaturated DATA_BLUE, mid-depth." DATA_BLUE is (43, 127, 255). The desaturation and darkening are significant: R drops from 43 to 10, G from 127 to 72, B from 255 to 120. The result is a dark teal-grey, which is correct for depth recession. But this value is undocumented.
- `MID_SHADOW = (6, 40, 72)` — further darkened from MID_COLOR. Undocumented.
- `MID_EDGE = (20, 110, 160)` — edge highlight on mid platforms. Undocumented.
- `FAR_COLOR = (0, 26, 40)` — near-void far color. Described inline as "near-void, far depth." Close to GL-08a but distinct — GL-08a is (5, 5, 8), whereas this is (0, 26, 40) with a strong blue-green component. This is actually closer to the ENV-10 value (`#0A1420` = (10, 20, 32)) than to GL-08a. Undocumented.
- `FAR_SHADOW`, `FAR_EDGE`, `GHOST_COLOR`, `GHOST_EDGE` — all undocumented inline derivations.

**Issue C9-1:** The depth tier derived colors (MID_COLOR, MID_SHADOW, MID_EDGE, FAR_COLOR, FAR_SHADOW, FAR_EDGE, NEAR_EDGE, GHOST_COLOR, GHOST_EDGE) are unnamed relative to the master palette and have no documentation comments explaining their derivation. For a compositing-export background, these values will be used by other artists compositing characters over this layer. A painter or comper who needs to match these values has no palette reference to check against.

The fix is straightforward: either register these as ENV-xx sub-entries in master_palette.md Section 4 (which already has ENV-08 through ENV-12 for Frame 03 Glitch Layer values), or add inline derivation comments noting which GL-xx parent they step down from and how.

**This is a Priority 2 issue for Jordan: document the depth tier derivation chain.**

---

### Assessment 3: Aurora Inline Tuple at Line 149

The aurora spec at lines 144–150 contains one undocumented inline tuple:

```python
aurora_spec = [
    (0.00, 0.12,  UV_PURPLE,       110),
    (0.05, 0.18,  ATMOS_MID_PURPLE, 90),
    (0.11, 0.24,  DATA_BLUE,        70),
    (0.19, 0.30,  (0, 160, 220),    50),   # cyan-blue bleed at bottom
]
```

The fourth aurora band uses `(0, 160, 220)` — an inline tuple with only a brief comment "cyan-blue bleed at bottom." This value sits between GL-02 Deep Cyan (`#00A8B4` = 0, 168, 180) and GL-06 Data Stream Blue (`#2B7FFF` = 43, 127, 255) but does not match either. It is a mid-depth cyan-blue bleeding down from the DATA_BLUE band into the void.

Visually, this is correct — the fourth aurora band should blend DATA_BLUE toward the cyan void atmosphere. But there is no named constant and no palette registration.

**Issue C9-2:** The inline `(0, 160, 220)` aurora blend value must be either named as a local constant with a derivation note (e.g., `AURORA_CYAN_BLEED = (0, 160, 220)  # GL-02/GL-06 atmospheric blend — aurora base zone`), or registered in master_palette.md as a GL-04/GL-06 blend entry.

Priority 3. It is a small element at low alpha (max 50), but the pattern of naming everything except one inline tuple has been a recurring theme on this project. It needs to stop.

---

### Assessment 4: Pixel Trail Color Derivation

Lines 250–258 generate pixel trails with:
```python
base_br = rng.randint(50, 120)
t_col = (0, base_br, int(base_br * 1.05))
```

And the draw call uses `(0, fade, int(fade * 1.05))` per pixel. This is a procedural derivation from ELEC_CYAN's hue (G channel dominant, minimal B) with random brightness, faded over trail length. It is not a direct palette value.

From a color theory standpoint, this is acceptable for a particle trail effect — using a procedurally varied brightness within the ELEC_CYAN hue family is standard practice for glitch environments. The cap at brightness 120 keeps the trails below the full ELEC_CYAN luminance (240), which correctly makes them read as "emissions fading into void" rather than full-power data streams.

I accept this as a well-motivated procedural element, not a palette defect.

---

### Assessment 5: Lower Void Debris Color Choices

Lines 265–270 use four hardcoded debris colors:
```python
t_col_choice = rng.choice([
    (0, 45, 65),
    (0, 30, 48),
    (20, 8, 50),
    (0, 18, 28),
])
```

These are extremely dark near-void values — all substantially below 10% luminance. They read as barely-visible debris in the lower void. The hue families are: cyan-teal (first two), deep UV purple (third), and near-void (fourth). All are consistent with the Glitch Layer color logic. The (20, 8, 50) has a UV_PURPLE DNA, which is correct for shadow-zone debris in the digital void.

These values are undocumented inline tuples. However, given that they are essentially randomized noise in the lower void at very low luminance, and given their purely atmospheric function, I accept them as rendering constructs rather than palette entries — analogous to the `LAMP_PEAK` value in style_frame_01_rendered.py which is also a rendering construct noted as intentionally absent from the palette.

**This is acceptable provided Jordan adds a comment at this block noting that these are rendering construct values (void debris noise, no palette home by design) — following the precedent set by the LAMP_PEAK documentation in style_frame_01_rendered.py.**

---

### Assessment 6: HOT_MAGENTA Absent from bg_glitch_layer_frame.py

The master_palette.md notes that HOT_MAGENTA (`#FF2D6B`) is used for "error states, dangerous glitch energy, the crackling edges of a corrupting portal" and is the Glitch Layer's second most important color after ELEC_CYAN. It does not appear in `bg_glitch_layer_frame.py` at all.

This is not a defect for this specific asset — a background Glitch Layer environment without active corruption events would not necessarily include Hot Magenta. The docstring describes this as a neutral "void black base, 3-tier platforms, aurora, pixel flora, ghost platforms, pixel trails" background, not a corruption event scene. The absence is contextually appropriate.

**However:** The docstring's palette list should note that HOT_MAGENTA is intentionally absent ("No corruption events in this shot — HOT_MAGENTA not used; for corruption events in this environment, reference GL-03 in master_palette.md"). This prevents a future artist from assuming they can freely modify this file without needing to add Hot Magenta.

---

## Part 3 — Remaining Open Issues

---

### ISSUE C9-1 (New): Depth Tier Derived Colors Undocumented

**Priority 2**

`bg_glitch_layer_frame.py` defines nine derived depth colors (MID_COLOR, MID_SHADOW, MID_EDGE, FAR_COLOR, FAR_SHADOW, FAR_EDGE, NEAR_EDGE, GHOST_COLOR, GHOST_EDGE) with only brief inline labels. These values are not documented in master_palette.md. A comper using this layer as a background plate will have no palette reference for matching these tones when adding characters or props.

**Required fix:** Jordan Reed should either:
(a) Add inline derivation comments at the definition site for each value, stating the GL-xx parent and transformation applied (e.g., `MID_COLOR = (10, 72, 120)  # DATA_BLUE GL-06 desaturated 75%/darkened 50% — mid-depth recession`), or
(b) Register the depth tier values as ENV-xx sub-entries in master_palette.md Section 4 (Glitch Layer column, alongside ENV-09 and ENV-10).

Option (a) is the minimum acceptable fix.

---

### ISSUE C9-2 (New): Aurora Inline Tuple (0, 160, 220) — No Name, No Documentation

**Priority 3**

The fourth aurora band color `(0, 160, 220)` is an undocumented inline tuple. It must be named at the top of the file as a local constant with a derivation note, or registered in master_palette.md.

---

### ISSUE C9-3 (New): Lower Void Debris — Add Rendering Construct Note

**Priority 3**

The four hardcoded lower void debris colors must be annotated as rendering construct values (following the LAMP_PEAK precedent) to prevent future palette confusion.

---

### ISSUE C9-4 (Carried from C8-4): Cold Overlay Alpha — Render Review Outstanding

**Priority 2**

Cold overlay alpha_max=60 has not been reviewed against the rendered output. The team must verify that the warm/cold overlay boundary does not produce a grey mid-zone on Luma's body. If it does, reduce cold alpha to 40–45. This item cannot carry into Cycle 11.

---

### ISSUE C9-5 (New): CHAR-L-08 Derivation Arithmetic Discrepancy

**Priority 3**

The documentation states that a 70/30 blend of HOODIE_SHADOW and DUSTY_LAVENDER yields (176, 96, 64). Actual arithmetic gives approximately (179, 98, 80). The blue channel discrepancy is 16 points — more than rounding. Either the blend ratio used was not exactly 70/30, or a correction was applied. The documentation must accurately reflect the actual derivation.

---

## Part 4 — What Is Working Well

I want to be precise about what has genuinely improved.

**The Cycle 8 cleanup is complete and correct.** All Priority 1 and 3 items from my Cycle 8 report have been addressed:
- CHAR-L-08 finalized with a principled derived value.
- SHOE_CANVAS and SHOE_SOLE local aliases eliminated; direct constants used.
- CABLE_NEUTRAL_PLUM named at module level; PROP-07 registered in master_palette.md.
- CHAR-L-09 and CHAR-L-10 added to Section 5 — shoe colors now findable in the palette.

**Section 7 is the most significant documentation advance this project has seen.** The two-tier skin system is correctly structured, the derivation hierarchy is clear, and the resolution of the three-value discrepancy is intellectually honest — it names the ambiguity, explains why both values are correct in their respective contexts, and gives painters a clear decision rule. The warm/cool skin tables in 7.4 and 7.5 are production-ready. A painter rendering a Glitch Layer scene for the first time now knows exactly which skin values to use without making it up.

**`bg_glitch_layer_frame.py` is a well-structured script.** The palette constants block maps correctly to master_palette.md for all primary named colors. The three-tier depth system is conceptually correct and the 3D depth recession (NEAR full ELEC_CYAN → MID desaturated DATA_BLUE → FAR near-void) directly implements the platform depth principle from master_palette.md Section 4 ENV-09/ENV-10. The aurora is built from GL-04/GL-04b/GL-06 in the correct sequence. The pixel flora uses ACID_GREEN at correctly dimmed brightness tiers (22%/12%/6% — a well-executed value ladder for atmospheric distance). The GL-08a abyss shadow under ghost platforms shows Jordan has read the palette specification.

**The master_palette.md is now at the threshold of production-readiness.** Sections 1 through 7 are complete. The character spec (Sections 5), prop registry (Section 6), and skin system (Section 7) are all documented. A production painter could use this document for approximately 92% of their decisions on Frames 01 and 03 without guessing.

---

## Part 5 — Can the Palette Reach a Full A This Cycle?

Almost.

My A minus from Cycle 8 was earned by completing the structural work. The structural work is now done. What remains are:

1. **CHAR-L-08 derivation discrepancy** (Priority 3 — small, fixable in an hour)
2. **Cold overlay render review** (Priority 2 — requires rendering and checking)
3. **bg_glitch_layer_frame.py depth tier documentation** (Priority 2 — Jordan's task)
4. **Aurora inline tuple naming** (Priority 3)
5. **Void debris annotation** (Priority 3)

Items 1, 4, and 5 are trivial documentation fixes. Items 2 and 3 require actual work.

The full A is withheld this cycle on two grounds:

**Ground 1:** The cold overlay alpha issue has now been open since Cycle 8 and has been neither resolved nor formally checked. Carrying a "monitoring concern" across two cycles without a render review is not professional practice. A monitoring concern requires a monitor.

**Ground 2:** `bg_glitch_layer_frame.py` is new and valuable but delivers undocumented derived values. The depth tier colors will be used by other artists compositing over this background. Leaving them undocumented creates a risk that a character painted over a MID platform will use ELEC_CYAN instead of the correct desaturated value, breaking the depth read. Jordan needs to close this in Cycle 10.

The palette itself — `master_palette.md` — is at A quality on its own terms. The code implementation introduces enough unresolved loose ends to hold the composite work at A minus. One focused cycle of documentation completion will earn the A.

---

## Grade: A-

Held from A by:
- Cold overlay render review still outstanding (open two cycles)
- Depth tier derived colors in bg_glitch_layer_frame.py undocumented
- CHAR-L-08 derivation arithmetic does not match stated formula

The A minus is solid. The team's best work to date. The palette document alone is A quality. Code documentation discipline needs one more pass.

---

## Cycle 10 Task List

### Priority 2 — Should Fix

1. **Render and review cold overlay boundary.** Alex Chen: render `style_frame_01_rendered.py` and examine Luma's body at the compositional center. If warm/cold boundary creates a grey mid-zone, reduce cold overlay alpha from 60 to 40–45. Document the result in the SOW. This cannot carry into Cycle 11.

2. **Document depth tier derived colors.** Jordan Reed: add inline derivation comments to the nine depth tier constants in `bg_glitch_layer_frame.py` (NEAR_EDGE, MID_COLOR, MID_SHADOW, MID_EDGE, FAR_COLOR, FAR_SHADOW, FAR_EDGE, GHOST_COLOR, GHOST_EDGE). State the GL-xx parent and the transformation applied. Alternatively, register as ENV-xx entries in master_palette.md Section 4.

### Priority 3 — Housekeeping

3. **Reconcile CHAR-L-08 derivation documentation.** Sam Kowalski: the stated 70/30 blend gives (179, 98, 80) — not (176, 96, 64) as documented. Either confirm the actual ratio used and update the documentation, or correct the hex to match the stated formula. The discrepancy is in the blue channel (16 points) and affects the cool-influence read of the value.

4. **Name the aurora inline tuple.** Jordan Reed: replace `(0, 160, 220)` in the aurora_spec with a named local constant at the top of `bg_glitch_layer_frame.py`. Add a derivation note referencing GL-06 and GL-02 as parent hues.

5. **Annotate lower void debris as rendering construct.** Jordan Reed: add a comment to the void debris section stating these are rendering construct values without a palette home, following the precedent of LAMP_PEAK in style_frame_01_rendered.py.

6. **Add luma_color_model.md cross-reference note.** Sam Kowalski: the skin entry in `luma_color_model.md` should add: "Base = Warm Caramel under lamp-lit Frame 01 conditions. Neutral-light canonical base = #C4A882 (RW-10). See master_palette.md Section 7." Documented in Section 7.6 as outstanding.

---

— Naomi Bridges
Color Theory Specialist
2026-03-29 22:00
