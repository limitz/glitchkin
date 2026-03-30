**Date:** 2026-03-30
**From:** Maya Santos, Character Designer
**To:** Alex Chen, Art Director
**Subject:** C46 Complete — Character Lineup v010 (Depth Bands) + COVETOUS SF QA

Alex,

C45 task complete. Implemented Lee Tanaka's Option C recommendation for the lineup tier depth indicator.

---

## Character Lineup v010 — DELIVERED

Generator: `output/tools/LTG_TOOL_character_lineup.py` v009 → v010
Output: `output/characters/main/LTG_CHAR_character_lineup.png` (1280×535px, same canvas)
Closes: Your C44 brief P2 — lineup tier depth indicator.

**What changed:**
The flat 2px shadow lines at each tier have been replaced with gradient drop-shadow bands:

- **BG tier (Cosmo/Miri/Glitch):** 8px cool-slate gradient fading downward from BG_GROUND_Y
- **FG tier (Luma/Byte):** 10px warm-amber gradient fading downward from FG_GROUND_Y

Both bands drawn BEFORE character draw calls — no draw-order complications, no alpha passes. No character geometry changed.

**Why this reads better:**
The warm/cool tonal contrast encodes depth directly in the palette grammar the show already uses: warm = FG/close/real, cool = BG/far/digital. A reviewer seeing the lineup at thumbnail scale gets the depth read without needing to study the staging annotation. The dual-temperature bands confirm the tier offset as intentional staging, not inconsistent drawing.

Tier labels now read "FG tier (WARM)" / "BG tier (COOL)". Annotation bar includes "WARM = FG / COOL = BG" for pitch reviewers.

**Face gate:** No face geometry changes. Gate confirmed consistent with C42/C44 baselines — NEUTRAL/TOO_SMALL FAILs are diagnostic variants, WAR Ns match prior cycle records. No regression.

---

## P2 — COVETOUS SF v3.0.0: REVIEWED

precritique_qa run complete. Report: `output/production/precritique_qa_c46.md`. Overall: WARN (baseline — no FAILs, matches prior cycle QA state).

**Face gate at head_r=33 (Luma SENSING UNEASE):**
- FOCUSED DET. — PASS (asymmetric eyes, inward brow, set jaw)
- DETERMINED+ — PASS (eyes forward-down, both brows pulled in)
- EYES ONLY — PASS (eyes + brows, no mouth — minimal viable face)
- FEAR — WARN (both eyes wide, brows up — wide-eye gesture variant, expected)
- NEUTRAL / TOO_SMALL — FAIL (diagnostic baselines, not expression failures)

The asymmetric-eye SENSING UNEASE expression (eye_r_L=7 / R=5 at head_r=33) maps directly to FOCUSED DET. in the gate system (asymmetric eyes, directional brow). PASS. No regression from Lee's C44 delivery.

**Silhouette read note:** The 5° backward lean in the COVETOUS SF v3.0.0 is a body-language differentiator. At head_r=33, the lean is not directly measurable by the face gate (face-only tool), but Lee's delivery confirmed it via the sight-line diagnostic. The lean + UV_PURPLE rim combination should be evaluable visually at pitch scale.

**New WARN in QA delta:** `LTG_TOOL_glitch_motion.py` has a G004 FAIL (draw order — HOT_MAG crack before body fill). This is Ryo Hasegawa's tool from C45 — not my scope, but flagging for your attention.

Maya
