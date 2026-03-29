**Date:** 2026-03-29 09:05
**From:** Alex Chen, Art Director
**To:** Maya Santos, Character Designer
**Re:** Cycle 16 Work Assignments

Maya,

Three character fix tasks this cycle. All are Critique C8 priority items.

---

## TASK 1 — Fix Byte RESIGNED Right Eye [PRIORITY 1]

**File:** `/home/wipkat/team/output/tools/LTG_TOOL_byte_expression_sheet_v002.py`
**Issue:** Dmitri Volkov flagged the RESIGNED right eye as wrong. The current `droopy_resigned` implementation uses a flat lower lid — identical to NEUTRAL's silhouette at thumbnail scale. This is a structural failure, not a style note.

**Spec for RESIGNED right eye:**
- Heavy drooping lower lid — a visibly curved lid line sagging below center
- Downcast pupil — iris shifted toward the lower half of the eye aperture, NOT centered
- NO smile crinkle on the lower lid (that belongs to RELUCTANT JOY's `droopy` style only)
- Shorter highlight dot (reduced luminance — "the light has gone out a bit")
- Eye aperture: ~50% open (current is already coded as 50% but the lid shape is wrong — needs the droop to be geometrically visible)
- The result should read: heavy, tired, yielded. Not neutral. Not asleep.

Also: Dmitri noted the +8° backward body tilt may be too subtle for thumbnail silhouette differentiation. Check `body_tilt=+8` in the RESIGNED expression data — consider increasing to +12 or +14 if it doesn't create visible silhouette difference from NEUTRAL at 200px wide.

**Regenerate:** `LTG_CHAR_byte_expression_sheet_v002.png` after your fix. Coordinate with Sam Kowalski — he is doing a parallel color pass on the same file. Your fix is geometry only. Sam's fix is color constants. Make sure the fixes go into the SAME output file.

**Note:** Sam is doing the color fix first (body fill, shadow, ALARMED BG). Coordinate with Sam to apply your geometry fix after his color pass, or apply them in the same generator edit. The final regenerated PNG must incorporate both fixes.

---

## TASK 2 — Fix Cosmo SKEPTICAL + Populate 2 Empty Expression Slots

**File:** `/home/wipkat/team/output/tools/LTG_TOOL_cosmo_expression_sheet_v001.py` (or equivalent Cosmo generator)
**Issue:** Dmitri gave this a B+ — strong populated expressions, two structural failures.

**Fix 1 — SKEPTICAL body language:**
Add a 5–8° backward torso lean to the SKEPTICAL expression. Currently it is face-only (one brow raised, flat mouth, glasses tilt). At thumbnail scale, face-only expressions don't read. The backward lean is the silhouette anchor — it communicates "I'm not buying what you're selling" before you see the face.

**Fix 2 — Populate 2 empty expression slots:**
The Cosmo sheet has 2 empty placeholder panels. For Cycle 16, these must be filled. Suggested expressions based on Act 2 needs:
- **FOCUSED / ENGAGED:** Cosmo doing tech work — eyebrows knit, leaning forward over a device, one hand working. He is in his element. This is the positive counterpart to SKEPTICAL.
- **RELUCTANT HELPING:** He's decided to help Luma even though he thinks the plan is bad. Arms crossed but turned toward her. The face says "I still think this is stupid." The body says "but I'm here." This is the pre-cooperation beat before SKEPTICAL resolves.

Adjust these suggestions based on your own character knowledge if you have stronger Act 2 reads. The rule is: no empty slots on a pitch-ready expression sheet.

**Regenerate:** `LTG_CHAR_cosmo_expression_sheet_v001.png` (v001 → v002 if you make structural changes to the generator; keep v001 archived).

---

## TASK 3 — Fix Luma Act 2 Standing Pose — Mitten Geometry

**File:** `/home/wipkat/team/output/tools/` (find the Act 2 standing pose generator)
**Issue:** Dmitri flagged the raised right arm hand as having emergent finger differentiation. Production rule: no individual finger detail in rough/reference poses. The hand must be clean mitten geometry — a simple rounded mitten shape, no finger separation visible.

**Fix:** Find the raised hand drawing code and replace any finger/digit differentiation with a clean oval/mitten outline. Reference: the standard Luma hand spec uses a 3-bump top + smooth bottom read. No individual knuckle lines, no digit separation.

Also: Dmitri noted the -5° forward lean is not perceptible. Either amplify to -8° or remove it from the spec and generator. Do not leave a spec element in the code that doesn't manifest visually.

**Regenerate:** Updated pose PNG.

---

## Priority Order

1. Byte RESIGNED right eye (coordinate with Sam on combined fix)
2. Cosmo SKEPTICAL lean + 2 empty slots
3. Luma Act 2 pose mitten geometry

Report back to me when done — I need to know if the RESIGNED expression is visually distinct from NEUTRAL before Lee Tanaka starts A2-07.

—Alex Chen
Art Director
Cycle 16
