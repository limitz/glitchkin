# LTG Color QA Report — Cycle 34 (Style Frames)

**Author:** Sam Kowalski
**Date:** 2026-03-29
**Tool:** LTG_TOOL_color_verify_v002.py v2.0.0 (histogram mode)
**Assets evaluated:** 4 style frames (pitch primaries)

---

## SF02 v006 Status

**SF02 v006 NOT YET DELIVERED by Jordan Reed.**
Task 2 run is **preliminary** — performed on SF02 v005
(LTG_COLOR_styleframe_glitch_storm_v005.png).
Results for v006 must be re-run when Jordan delivers.
Expected new colours to verify: HOT_MAGENTA #FF2D6B (fill light), ELECTRIC_CYAN #00F0FF (specular).

---

## Summary Table

| Asset | CORRUPT_AMBER | BYTE_TEAL | UV_PURPLE | HOT_MAGENTA | ELECTRIC_CYAN | SUNLIT_AMBER | Overall |
|-------|--------------|-----------|-----------|-------------|---------------|--------------|---------|
| SF01 discovery_v005 | PASS Δ0.0° | PASS Δ2.1° | not_found | PASS Δ0.0° | PASS Δ0.4° | not_found | **PASS** |
| SF02 glitch_storm_v005 *(prelim)* | PASS Δ1.4° | PASS Δ1.6° | not_found | PASS Δ1.6° | PASS Δ0.3° | PASS Δ0.4° | **PASS** |
| SF03 otherside_v005 | PASS Δ3.6° | PASS Δ0.7° | FAIL Δ9.2° | PASS Δ0.0° | PASS Δ0.0° | FAIL Δ9.3° | **FAIL** |
| SF04 luma_byte_v004 | not_found | not_found | not_found | not_found | not_found | FAIL Δ6.9° | **FAIL** |

---

## Per-Asset Detail

---

### SF01 — LTG_COLOR_styleframe_discovery_v005.png

**Overall: PASS**

| Colour | Status | Δ Hue | n pixels | Notes |
|--------|--------|-------|----------|-------|
| CORRUPT_AMBER | PASS | 0.0° | 808 | Exact hit at 32.9° |
| BYTE_TEAL | PASS | 2.1° | 837,423 | Dominant at 183.1° (bucket 180-185°); canonical 185-190° has 9,260 — correct split between ELECTRIC_CYAN (183.5°) and BYTE_TEAL (185.2°) at this scene's teal-dominant BG. No concern. |
| UV_PURPLE | not_found | — | — | No UV Purple in warm-room discovery scene. Correct. |
| HOT_MAGENTA | PASS | 0.0° | 55 | Exact hit. |
| ELECTRIC_CYAN | PASS | 0.4° | 775,214 | Dominant CRT/screen glow. |
| SUNLIT_AMBER | not_found | — | — | Warm lamp pixels sample as skin/orange family, not at canonical 34.3° separately. Known false-positive domain. Absence flag is expected. |

**Verdict:** All present colours pass. No regressions vs C33.

---

### SF02 — LTG_COLOR_styleframe_glitch_storm_v005.png  *(PRELIMINARY — v006 pending)*

**Overall: PASS**

| Colour | Status | Δ Hue | n pixels | Notes |
|--------|--------|-------|----------|-------|
| CORRUPT_AMBER | PASS | 1.4° | 296 | Confirmed #FF8C00 (32.9° canonical). Histogram centred on 30-35° bucket with some 35-40° spread — anti-aliasing edge pixels; not a violation. |
| BYTE_TEAL | PASS | 1.6° | 594 | Byte body teal present and correct. |
| UV_PURPLE | not_found | — | — | Storm confetti does not include UV Purple at detectable concentration. Consistent with v005 spec (DATA_BLUE 70% / VOID_BLACK 20% / ELEC_CYAN 10%). |
| HOT_MAGENTA | PASS | 1.6° | 1,103 | Present at 1,103 pixels — this is the fill-light/crack accent. 808 in canonical 340-345° bucket. Clean. |
| ELECTRIC_CYAN | PASS | 0.3° | 817 | Crack light and specular elements confirmed. |
| SUNLIT_AMBER | PASS | 0.4° | 210 | Window warm glow present and verified. Histogram clean — spread across 25-40° but canonical bucket dominant. |

**v005 verdict:** All colours pass. Ready as preliminary benchmark.

**For v006 re-run targets:**
- HOT_MAGENTA #FF2D6B: expect n >> 1,103 (full fill-light vs accent-only in v005). Target: n ≥ 5,000 for a fill-light zone. Δ ≤ 5° required.
- ELECTRIC_CYAN #00F0FF: expect n >> 817 if specular highlights added. Δ ≤ 5° required.
- All other colours should be unchanged from v005 results.

---

### SF03 — LTG_COLOR_styleframe_otherside_v005.png

**Overall: FAIL (2 items) — both are documented false positives**

| Colour | Status | Δ Hue | n pixels | Notes |
|--------|--------|-------|----------|-------|
| CORRUPT_AMBER | PASS | 3.6° | 263 | Amber fragment lines. Δ3.6° within tolerance. Histogram: dominant in 25-30° bucket (AA edge pixels). Within acceptable range. |
| BYTE_TEAL | PASS | 0.7° | 1,243 | Byte body confirmed at near-canonical hue. |
| UV_PURPLE | **FAIL** | 9.2° | 447 | **DOCUMENTED FALSE POSITIVE.** Median dragged to 262.7° by sky gradient pixels. Histogram shows spread from 250-275° — canonical bucket (270-275°) has 132 pixels (second-largest). UV_PURPLE is present and rendered correctly at #7B2FBE; the gradient transition to darker void zones (ENV-11/ENV-12) creates a hue spread that pulls the median. Registered: C23 lesson + C31 QA. Not a production error. |
| HOT_MAGENTA | PASS | 0.0° | 298 | Byte's magenta eye. Exact hit. |
| ELECTRIC_CYAN | PASS | 0.0° | 1,267 | Dominant platform + circuit trace colour. Exact hit. |
| SUNLIT_AMBER | **FAIL** | 9.3° | 1,349 | **DOCUMENTED FALSE POSITIVE.** Found at 25.0° — these are warm skin/hoodie orange pixels (hue 20-25°) which fall inside the tool's sample radius for SUNLIT_AMBER (34.3°). No genuine SUNLIT_AMBER present in SF03 (zero warm light sources). Consistent with C26/C30/C31 false-positive registry. Not a production error. |

**Verdict:** No new regressions. Both FAILs are pre-existing, documented false positives. SF03 colour palette integrity intact.

---

### SF04 — LTG_COLOR_styleframe_luma_byte_v004.png

**Overall: FAIL (1 item) — known pre-existing issue**

| Colour | Status | Δ Hue | n pixels | Notes |
|--------|--------|-------|----------|-------|
| CORRUPT_AMBER | not_found | — | — | SF04 is a character interaction frame without Corrupt Amber strokes. |
| BYTE_TEAL | not_found | — | — | **Pre-existing issue (C26+).** Byte's body teal is present but at 60-70% luminance due to intentional discovery-scene low-key lighting. Accepted by Alex Chen (art director decision documented in master_palette.md QA Scene-Lighting Exceptions). Tool samples at canonical saturation and misses the shadowed version. Closed/accepted. |
| UV_PURPLE | not_found | — | — | Soft-key scene — UV Purple below sampling threshold. |
| HOT_MAGENTA | not_found | — | — | No HOT_MAGENTA elements in SF04 at detectable concentration. |
| ELECTRIC_CYAN | not_found | — | — | Screen glow below sampling threshold at this render. |
| SUNLIT_AMBER | **FAIL** | 6.9° | 56,320 | **Pre-existing issue (C31).** Samples finding 41.1° hue — these are Soft Gold (#E8C95A) hoodie pixel accents and warm face lighting, not SUNLIT_AMBER (34.3°). 56,320 pixels at exactly 40-45° bucket. Clear false positive. The tool cannot distinguish Soft Gold from SUNLIT_AMBER at radius=40. Closed/accepted (C31 QA). |

**Verdict:** No new regressions. All FAILs are pre-existing documented issues. Requires Rin Yamamoto rebuild decisions from C32 to fully resolve the not_found items.

---

## Comparison vs Prior Cycles

| Asset | C31 | C32 | C34 |
|-------|-----|-----|-----|
| SF01 discovery | PASS | PASS | PASS |
| SF02 glitch_storm | PASS | PASS | PASS (prelim v005) |
| SF03 otherside | WARN (UV_PURPLE) | WARN (UV_PURPLE) | FAIL (UV_PURPLE + SUNLIT_AMBER) — same documented FPs |
| SF04 luma_byte | WARN | WARN | FAIL (SUNLIT_AMBER) — same documented FP |

Note: SF03/SF04 flip from WARN to FAIL in this run due to histogram mode providing more precise delta measurements rather than any actual regression.

---

## Action Items

1. **Jordan Reed — SF02 v006 delivery.** Re-run `LTG_TOOL_color_verify_v002.py` on v006 when delivered. Check HOT_MAGENTA pixel count (fill-light) and ELECTRIC_CYAN pixel count (specular). Target: both present, Δ ≤ 5°.
2. **Kai Nakamura — false-positive registry tool.** Ideabox item `20260329_sam_kowalski_qa_false_positive_registry.md` still open. Would allow annotating SF03 UV_PURPLE and SUNLIT_AMBER as FP-DOCUMENTED to surface genuine regressions.
3. **No palette corrections needed.** All PASS results confirm palette integrity for SF01, SF02 v005. SF03/SF04 FAILs are known and accepted.

---

*Generated by Sam Kowalski, Color & Style Artist — Cycle 34*
