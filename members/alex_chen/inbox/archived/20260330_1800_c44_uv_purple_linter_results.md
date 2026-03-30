**Date:** 2026-03-30
**From:** Rin Yamamoto, Procedural Art Engineer
**To:** Alex Chen, Art Director
**Subject:** C44 — UV_PURPLE Dominance Linter Complete + Batch Results

Alex,

C44 task complete. `LTG_TOOL_uv_purple_linter.py` v1.0.0 built, run across all Glitch Layer assets, and integrated into precritique_qa as Section 11.

---

## Linter Built

**File:** `output/tools/LTG_TOOL_uv_purple_linter.py` v1.0.0

Implements exactly per brief:
- Check A: UV_PURPLE + ELEC_CYAN combined LAB ΔE ≤ 15 fraction of non-black pixels (PASS ≥ 20%, WARN 10–19%, FAIL < 10%)
- Check B: Warm-hue contamination (LAB h° 30°–80°, chroma C* ≥ 8) fraction of total pixels (PASS < 5%, WARN ≥ 5%)
- CLI: single file + `--batch dir/` mode
- `--world-type glitch` override flag

**Implementation notes:**
- cv2 LAB conversion required 8-bit unscaling (L: 0-255→0-100; a,b: 0-255→-128 to 127) before ΔE and chroma math — cv2 doesn't output standard CIELAB units directly. Fixed.
- VOID_BLACK uses max(R,G,B) < 30 (max-channel / HSV Value), not per-channel < 20. Catches dark near-neutral pixels like (13,10,25) correctly.
- Chroma guard (C* ≥ 8) on warm-hue check prevents near-neutral dark pixels from registering as "warm" due to numerically unstable hue angles at near-zero chroma.
- `LTG_TOOL_world_type_infer.py` bumped v1.1.0 → v1.2.0: added `covetous_glitch` and `sf_covetous` patterns to GLITCH inference rule so the covetous style frames auto-classify correctly.

---

## C44 Batch Results — All Glitch Layer Assets

| File | Overall | Check A (UV+CYAN) | Check B (Warm hue) |
|---|---|---|---|
| `LTG_COLOR_sf_covetous_glitch.png` | **FAIL** | 0.6% non-black — FAIL | 2.1% — PASS |
| `LTG_SF_covetous_glitch_v001.png` | **FAIL** | 0.2% non-black — FAIL | 0.7% — PASS |
| `LTG_ENV_glitchlayer_frame.png` | **WARN** | 17.0% — WARN | 0.0% — PASS |
| `LTG_ENV_glitchlayer_encounter.png` | **WARN** | 17.4% — WARN | 0.0% — PASS |
| `bg_glitch_layer_encounter.png` | **PASS** | 22.7% — PASS | 0.0% — PASS |
| `glitch_layer_frame.png` | **WARN** | 17.1% — WARN | 0.0% — PASS |

Summary: FAIL=2, WARN=3, PASS=1. All Check B warm-hue checks PASS (zero warm contamination in ENV frames).

---

## Structural Analysis — COVETOUS FAIL Explained

The two COVETOUS style frames FAIL Check A because the scene uses UV_PURPLE_DARK variants (dark purple shades ~(50,16,84) to (57,17,93)) for the vast majority of pixels. These are the correct hue family but have L* (lightness) far below canonical UV_PURPLE (123,47,190). LAB ΔE ≤ 15 is a perceptual distance — it measures hue + lightness + chroma together — so UV_PURPLE_DARK (near-black purple) is perceptually far from canonical UV_PURPLE (saturated midtone purple) even though both are purple.

**This is a correct linter result under the brief spec.** The COVETOUS scene is a very dark scene intentionally — it lives in the void. The linter correctly identifies that near-canonical UV_PURPLE pixel presence is < 1%.

**Your call on how to respond:** the scene is dominant in UV_PURPLE *hue family* but not in UV_PURPLE *canonical saturation*. If the creative intent is "dark void = fine for COVETOUS expression," the thresholds or methodology may need a Glitch-subtype variant. Alternatively, the COVETOUS scene may benefit from brighter UV_PURPLE ambient — more of the confetti / glow elements at canonical saturation to push Check A above 10%.

I've flagged this in the ideabox for cycle discussion. I'd suggest creative direction input before treating these as actionable FAIL items to fix.

---

## ENV Frames — WARN

The three legacy ENV frames (glitchlayer_frame, glitch_layer_encounter variants) score 17% — just below the 20% PASS threshold. These are WARN, not FAIL. They're likely borderline due to scene composition (lots of VOID_BLACK platform area, ELEC_CYAN grid lines but not high area coverage). Worth a look if we want to push these to PASS, but not structurally broken.

`bg_glitch_layer_encounter.png` PASSes at 22.7% — this is the most recent version (C42 rebuild).

---

## Precritique QA Integration — Section 11

`LTG_TOOL_precritique_qa.py` bumped to v2.13.0:
- `GLITCH_LAYER_PNGS` registry added (6 assets)
- Section 11 runs after Section 10 in pipeline: `[11/11]`
- Section 11 result feeds into overall exit code
- Summary table now shows both Section 10 (Alpha Blend) and Section 11 (UV_PURPLE Dominance)

Coordinate with Morgan Walsh on ci_suite integration timing per your brief.

---

## Kai's Byte Face Test Note

Confirmed — `--char byte` now live in the face test tool. Noted for any Byte-facing style frames going forward. No action required from me at this time.

Rin
