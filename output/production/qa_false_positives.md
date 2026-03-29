# QA False Positive Registry — "Luma & the Glitchkin"

**Maintained by:** Sam Kowalski, Color & Style Artist
**Last updated:** 2026-03-29 (Cycle 35)

This registry documents known and accepted QA tool false positives for pitch-primary assets.
A false positive is a tool failure where the asset is production-correct and the failure is
caused by a tool limitation, not a genuine color or rendering error.

When a QA tool flags an asset, check this registry FIRST before investigating as a new issue.

---

## FP-001 — SF03 UV_PURPLE gradient median pull

**Asset:** `LTG_COLOR_styleframe_otherside_v005.png`
**Tool:** `LTG_TOOL_color_verify_v002.py`
**Color:** UV_PURPLE (GL-04, #7B2FBE, hue 271.9°)
**Reported delta:** Δ9.2°
**Status:** DOCUMENTED FALSE POSITIVE — accepted C23; re-confirmed C31/C34/C35.

**Root cause:** The sky gradient in SF03 transitions from canonical UV_PURPLE (271.9°) through
ENV-11 #2A1A40 (40% sat, hue ~255°) and ENV-12 #2B2050 (31% sat, hue ~258°) toward near-void.
The tool samples pixels in a radius around the canonical hue and computes the median. The
gradient transition pixels drag the median to ~262.7°. The canonical bucket (270-275°) still
has n=132 pixels (second-largest) — the color IS present and correct.

**Rule:** UV_PURPLE FAIL in SF03 = always this gradient false positive. Canonical bucket
(270-275°) count must be n ≥ 100 for the genuine color to be present.

---

## FP-002 — SUNLIT_AMBER skin-tone hit on character sheets

**Assets:** `LTG_CHAR_luma_expressions_v007.png` (and all Luma/Miri expression sheets)
**Tool:** `LTG_TOOL_color_verify_v002.py`
**Color:** SUNLIT_AMBER (RW-03, #D4923A, hue 34.3°)
**Reported delta:** varies (Δ6-10°)
**Status:** DOCUMENTED FALSE POSITIVE — accepted C26; confirmed C30/C31/C32/C34/C35.

**Root cause:** Luma and Miri skin tones (hue ~18-25°) fall within the sampling radius of
SUNLIT_AMBER (hue 34.3°, radius 40). The tool finds skin pixels and measures them as the
nearest SUNLIT_AMBER sample. The found hue (~18-25°) is then measured as delta against
canonical 34.3°, producing a false FAIL.

**Rule:** SUNLIT_AMBER FAIL on Luma/Miri character sheets = skin tone false positive.
Verify by checking that the dominant warm pixels are in the 15-25° bucket (skin family),
not the 30-40° bucket (sunlit surface family). If 30-35° bucket is empty, no genuine
SUNLIT_AMBER is present — this is correct for character model sheets.

---

## FP-003 — SF03 SUNLIT_AMBER skin/hoodie hit

**Asset:** `LTG_COLOR_styleframe_otherside_v005.png`
**Tool:** `LTG_TOOL_color_verify_v002.py`
**Color:** SUNLIT_AMBER (RW-03, #D4923A, hue 34.3°)
**Reported delta:** Δ9.3° (found 25.0°)
**Status:** DOCUMENTED FALSE POSITIVE — accepted C26; confirmed C30/C31/C32/C34/C35.

**Root cause:** Luma's warm skin (#C07038 hoodie, #C8885A skin) in the UV-ambient Other Side
scene registers as warm pixels in the 20-30° hue range. Tool samples these and measures
them as SUNLIT_AMBER. No genuine SUNLIT_AMBER exists in SF03 — zero warm light sources,
confirmed in generator and QA checks.

---

## FP-004 — SF04 SUNLIT_AMBER compositing artifact

**Asset:** `LTG_COLOR_styleframe_luma_byte_v004.png`
**Tool:** `LTG_TOOL_color_verify_v002.py`
**Color:** SUNLIT_AMBER (RW-03, #D4923A, hue 34.3°)
**Reported delta:** Δ15.7° (found 18.6°)
**Status:** DOCUMENTED FALSE POSITIVE — accepted C35 (Alex Chen art director decision,
`output/production/warm_cool_decision_c35.md`).

**Root cause (two-component):**
1. Skin-tone sampling: The tool samples Luma's warm-lit skin at hue ~18° and reports it
   as the SUNLIT_AMBER hit. Dominant bucket is 15-20° (skin), not 30-35° (sunlit surface).
2. Compositing artifact: The SF04 lamp rim light uses `(255,200,80)` at hue 41.1°. When
   composited over SUNLIT_AMBER (34.3°) surfaces, the blended pixels shift toward yellow.
   This is physically correct rendering — the QA tool cannot distinguish compositing shift
   from a wrong source color.

**Generator source color:** `SUNLIT_AMBER = (212, 146, 58)` at line 69 of
`LTG_TOOL_styleframe_luma_byte_v004.py` — matches canonical RW-03 #D4923A exactly.
The source constant is correct; the drift is compositing only.

**Note:** SUNLIT_AMBER is also unused in direct draw calls (the lamp uses `(255,200,80)`
instead — this is intentional: lamp amber vs. sunlit-window amber are different hues).
See comment added to generator in C35.

---

## FP-005 — SF04 Byte Teal below canonical luminance

**Asset:** `LTG_COLOR_styleframe_luma_byte_v004.png`
**Tool:** `LTG_TOOL_color_verify_v002.py`
**Color:** BYTE_TEAL (GL-01b, #00D4E8)
**Status:** SCENE-LIGHTING EXCEPTION — accepted C33 (Alex Chen art director decision,
`output/color/palettes/master_palette.md` QA Scene-Lighting Exceptions section).

**Root cause:** SF04 is a discovery-scene soft-key scene. Byte's body is rendered at 60-70%
of canonical luminance by design — intentional low-key lighting for narrative tension.
The QA tool samples at canonical saturation and misses the shadowed version.

---

## FP-006 — Warm/cool separation on single-dominant-temperature style frames

**Assets:** All 4 pitch style frames (SF01, SF02, SF03, SF04)
**Tool:** `LTG_TOOL_render_qa_v001.py` (check D — `_check_warm_cool()`)
**Reported separation:** SF01=17.9, SF02=6.5, SF03=3.1, SF04=1.1 (all below threshold 20.0)
**Status:** PARTIALLY RESOLVED in C37 — SF03 now PASS. SF01/SF02/SF04 still WARN.

**Root cause:** `_check_warm_cool()` splits the image into top/bottom halves and compares
median hue. This tests vertical atmospheric separation — appropriate for naturalistic scenes.
LTG frames apply temperature as a uniform world signal (warm room, cold glitch world) — not
a vertical split. The metric cannot distinguish "intentionally warm frame" from "flat palette".

**Correct per-world thresholds:**
- real_world_interior (SF01): threshold=12 (PASS at 17.9)
- real_world_night_storm (SF02): threshold=3 (PASS at 6.5)
- glitch_world (SF03): threshold=0 (PASS at any reading — warm absence is correct) — **RESOLVED C37**
- SF04 (soft-key, world_type=None): threshold=0 desired — still WARN (no filename match)

**C37 update (render_qa v1.4.0):** SF03 (`otherside` in filename → OTHER_SIDE → threshold=0) is
now PASS. SF01/SF02/SF04 remain WARN because render_qa uses REAL→20 for all REAL filenames —
higher than the FP-006 spec thresholds of 12 (interior) and 3 (storm). See ideabox idea
`20260330_sam_kowalski_render_qa_real_threshold_split.md` for the proposed fix.

**Remaining Kai Nakamura action:** Add REAL_INTERIOR (threshold=12) and REAL_STORM (threshold=3)
sub-types to render_qa world-type inference. This would eliminate the SF01 and SF02 warm/cool WARNs.

---

*Sam Kowalski — Color & Style Artist — Cycle 35 (updated C37)*
