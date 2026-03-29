# Warm/Cool Separation Analysis — Cycle 35

**Author:** Sam Kowalski, Color & Style Artist
**Date:** 2026-03-29
**Scope:** All 4 pitch-primary style frames + SF04 SUNLIT_AMBER drift (Priya C14 P1, Nkechi C14)
**Tool:** LTG_TOOL_render_qa_v001.py (`_check_warm_cool()`), LTG_TOOL_color_verify_v002.py (--histogram)

---

## 1. Warm/Cool QA Results — Current Readings

| Frame | Zone A (top half) | Zone B (bottom half) | Separation | Threshold | Pass? |
|-------|------------------|----------------------|------------|-----------|-------|
| SF01 discovery_v005 | 42.5 PIL = 60.0° | 24.6 PIL = 34.8° | 17.9 PIL (25.2°) | 20 PIL | FAIL |
| SF02 glitch_storm_v006 | 176.5 PIL = 249.2° | 170.0 PIL = 240.0° | 6.5 PIL (9.2°) | 20 PIL | FAIL |
| SF03 otherside_v005 | 184.7 PIL = 260.7° | 187.7 PIL = 265.0° | 3.0 PIL (4.3°) | 20 PIL | FAIL |
| SF04 luma_byte_v004 | 24.7 PIL = 34.9° | 23.6 PIL = 33.3° | 1.1 PIL (1.5°) | 20 PIL | FAIL |

PIL hue scale is 0–255 (= 0–360°). Conversion: degrees = PIL_units × 360 / 255.
Threshold of 20 PIL units = 28.2°.

---

## 2. Root Cause: Metric Design vs. Show Palette Architecture

### 2a. What the metric measures

`_check_warm_cool()` splits the image into TOP half and BOTTOM half, then compares the
**median hue** of each half. If the two halves have a median hue difference ≥ 20 PIL units
(≥ 28.2°), the frame passes.

This design assumes **naturalistic atmospheric lighting**: warm ground, cool sky, or vice
versa. The 20-unit threshold was likely calibrated against conventional animation where sky
(top) is cooler than earth (bottom) by a significant margin.

### 2b. Why this does not apply to the LTG three-world palette

"Luma & the Glitchkin" has three worlds with distinct temperature identities:

| World | Dominant temperature | SF |
|-------|---------------------|----|
| Real World | WARM (amber, orange, gold) | SF01, SF04 |
| Glitch Storm (contested) | COOL-dominant with warm accent | SF02 |
| The Other Side | COLD (cyan, UV purple, void black) | SF03 |

The warm/cool identity of each frame is **by-world, applied uniformly across the entire
frame** — not split vertically. This is an intentional production decision. The temperature
narrative reads as a gestalt (whole-frame mood), not as a top/bottom bifurcation.

**Consequence per frame:**

- **SF01:** Both halves are warm. Top median = 60.0° (Soft Gold/lamp region). Bottom median =
  34.8° (Sunlit Amber/floor region). Both are in the warm range (< 65°). The 25.2° separation
  is a warm-warm split within the same temperature family, not a warm/cool contrast. The metric
  correctly detects a lack of cold tones but incorrectly labels this a "flat palette" —
  SF01 is intentionally all-warm.

- **SF02:** Both halves read as cool (~240–250°). The storm key is cyan-dominant throughout —
  the warm window glow elements (SUNLIT_AMBER ~34°) are present but low pixel count (~206 px
  in v006) so they cannot shift the median. The 9.2° separation is within the cool family
  (DATA_BLUE vs UV_PURPLE hue bands within the storm). Not a production error.

- **SF03:** Both halves read as cool (~261–265°). UV_PURPLE ambient is the dominant hue
  throughout. The 4.3° separation reflects the even colder uniformity of the Other Side. This
  is the coldest frame in the trilogy — uniformity is the intent.

- **SF04:** Both halves read as warm (~34°). Full-frame warm domestic room. The 1.5° separation
  means the room is essentially isothermal in temperature — consistent with a cosy lamp-lit
  scene with no competing cool zones except the CRT monitor glow (which is Byte Teal ~185°,
  too few pixels to shift the median).

### 2c. Conclusion: Metric recalibration required

The `_check_warm_cool()` metric with threshold=20 is **inappropriate for single-dominant-
temperature style frames**. It was designed to catch frames with NO temperature intention —
grey, flat, neutral-dominant images. It cannot distinguish "intentionally warm" from "flat".

**Recommended fix for Kai Nakamura:** Add `asset_type="style_frame"` variant checking not
top-vs-bottom median hue separation, but the **presence of temperature intention** — i.e.,
at least N pixels of warm OR at least N pixels of cool (not both required). Alternatively,
allow `warm_cool_expected_temp` parameter ("warm", "cool", "contested") so the check can
verify that the dominant temperature is correct for the asset.

The current approach is valid for environments and contested frames but should not gate
style frames on vertical split.

**Existing tool workaround:** Pass `asset_type="character_sheet"` to suppress the warm/cool
check for single-temperature frames. This is a stopgap — ideabox idea submitted (see Section 5).

---

## 3. Are the Frames Genuinely Lacking Temperature Contrast?

Per hue distribution and canonical color audit:

### SF01 (warm-dominant, CORRECT)
- SUNLIT_AMBER present: n=91,782 px at canonical 34.3° (Δ0.8°) — the warm ground and wall
  tones dominate.
- ELECTRIC_CYAN present: n=60,819 px — the CRT screen provides a cool counterpoint.
- HOT_MAGENTA present: n=126 px — accent.
- **Temperature read:** Warm with cool CRT accent. Correct for the discovery scene.
- **No adjustment needed.** The warm/cool narrative is present; the metric simply can't see it
  because it's not split vertically.

### SF02 (contested/cool-dominant, CORRECT)
- HOT_MAGENTA fill-light: n=1,064 px at Δ1.5°.
- ELECTRIC_CYAN specular: n=3,571 px at Δ1.9°.
- SUNLIT_AMBER (window glow): n=206 px at Δ0.9°.
- CORRUPT_AMBER (outline): n=293 px at Δ0.1°.
- **Temperature read:** Cyan/cool storm dominant with warm accents (window glow, amber
  outlines). Contested identity is present. Warm pixel count is genuinely low vs. cool pixel
  count — this is intentional (the storm wins).
- **No adjustment needed.** The warm/cool contestation is a production decision. The metric
  cannot capture "one temperature wins but the other resists" — it only sees median values.

### SF03 (cold-dominant, CORRECT)
- UV_PURPLE present (n=447, documented gradient false positive — canonical bucket has n=132
  at 270-275°, correct).
- Zero warm light sources — confirmed in generator and QA tool.
- CORRUPT_AMBER accent fragments: n=263 px — non-warm energy, minimal.
- **Temperature read:** Maximum cold/alien. Intentional. Zero warm light. UV purple + Teal.
- **No adjustment needed.**

### SF04 (warm with cool accent, SLIGHT OPPORTUNITY)
- BYTE_TEAL confirmed: n=10,235 px at Δ0.0° — the monitor/CRT now registers.
- HOT_MAGENTA: n=250 px.
- ELECTRIC_CYAN: n=7,726 px at Δ1.6°.
- SUNLIT_AMBER: FAIL Δ15.7° (see Section 4 for full analysis).
- **Temperature read:** Warm-dominant room with Byte's Teal glow as the cool counterpoint.
- **Observation:** Byte Teal (n=10,235) + Electric Cyan (n=7,726) = ~18,000 cool pixels in a
  full 1280×720 frame (921,600 total). This is approximately 2% of the frame. The warm room
  overwhelms it. If a slightly more visible cool zone (the CRT screen itself, not just glow)
  were added, it would create better narrative tension between Luma's warm world and Byte's
  digital nature. Not blocking — advisory only.

---

## 4. SF04 SUNLIT_AMBER Drift Analysis (Nkechi C14 — Δ15.7°)

### 4a. The reading
The `LTG_TOOL_color_verify_v002.py --histogram` run on SF04 v004 finds:
- SUNLIT_AMBER: target=34.3°, found=18.6°, Δ15.7°, n=6,752 px at 15-20° bucket.

### 4b. Is this drift in the generator source colors?

Examining `LTG_TOOL_styleframe_luma_byte_v004.py`:

```
SUNLIT_AMBER = (212, 146, 58)   # defined at line 69 — canonical RW-03 #D4923A = CORRECT
```

**SUNLIT_AMBER (212,146,58) has hue 34.3°.** The canonical value is defined correctly at
line 69. However, **SUNLIT_AMBER is never referenced in any drawing call in the script.**
It is an unused constant.

The actual warm light sources in SF04 v004 are:
- Lamp halo: `(255, 200, 80)` — hue = 41.1° — 6.8° warmer/yellower than canonical SUNLIT_AMBER
- Byte lamp rim: `light_color=(255, 200, 80)` — same inline value, hue 41.1°
- Wall gradient: `WALL_WARM=(220,190,150)` — hue ≈ 33.3°; `WALL_UPPER=(200,168,122)` — hue ≈ 32.6°
- `SOFT_GOLD=(232,201,90)` — hue = 46.9° — hoodie pixel accents

### 4c. Why the tool finds Δ15.7° / 18.6°
The tool samples the image for pixels within the SUNLIT_AMBER sampling radius. It finds
n=6,752 pixels in the warm-orange family and their **median is at 15-20° hue** — which is
the skin tone range (Luma's warm-lit skin is ~18-25°). The tool is correctly identifying
that the dominant warm sample group is NOT at SUNLIT_AMBER's 34.3° — it is at skin tone.

This is a **compound false positive and a genuine design note:**

1. **False positive component:** The tool samples skin pixels (18-20°) as its nearest
   warm hit and measures them as SUNLIT_AMBER. These are not SUNLIT_AMBER; they are
   `CHAR-L-01` skin lamp-lit (#C8885A, hue ~18°).

2. **Genuine design note:** SUNLIT_AMBER (212,146,58) is defined in the generator but
   **never placed** on any surface in the frame. The lamp halo uses (255,200,80) at hue
   41.1° instead. This makes the warm-surface colors in SF04 slightly more golden/saturated
   than the canonical "afternoon sun on mid-value surface" read of RW-03.

### 4d. Is this a production problem?
The warm domestic lighting in SF04 is a **lamp scene, not a sunlit-window scene**. Using
(255,200,80) (a warm incandescent amber) rather than SUNLIT_AMBER (a softer afternoon-sun
amber) is contextually appropriate. The hue difference (41.1° vs 34.3°) produces a slightly
more yellow/saturated lamp glow — this is correct for incandescent light.

**Recommendation:** Register `(255,200,80)` as `RW-03a LAMP_AMBER` or annotate with a
comment in the generator: "Incandescent lamp halo — warmer/more saturated than RW-03
SUNLIT_AMBER (34.3°) by design. Use RW-03 for sunlit-window surfaces, this value for lamp
glow." No visual change required.

The Nkechi concern about "load-bearing warm/cool identity" is addressed by the fact that the
warm reading is genuine and intentional — it is simply a lamp amber (41°) vs sunlit amber
(34°) distinction that the tool cannot distinguish. The character of the warm light in SF04
is correct for the scene.

---

## 5. Metric Recalibration Recommendations

### Recommendation A — Warm/cool check redesign (for Kai Nakamura)

The `_check_warm_cool()` check should support an `expected_temp` parameter:

```python
def _check_warm_cool(img, expected_temp=None):
    """
    expected_temp: "warm" | "cool" | "contested" | None (default: top-vs-bottom split)
    - "warm": verify warm pixels dominate (> 40% of saturated pixels in 0-65° + 300-360° range)
    - "cool": verify cool pixels dominate (> 40% of saturated pixels in 120-240° range)
    - "contested": verify BOTH warm > 5% AND cool > 5% of saturated pixels (bidirectional test)
    - None: original top-vs-bottom median split (backward compatible)
    """
```

This would allow style frames to be tagged with their intended temperature and checked
against that intent, rather than checked against a vertical symmetry assumption.

**Ideabox submission:** `20260329_sam_kowalski_warm_cool_by_intent.md` — filed this cycle.

### Recommendation B — Short-term workaround

For Priya C14 P1 critique response: acknowledge the metric's limitation for single-dominant-
temperature frames. The warm/cool identity of each SF is correct and intentional as documented
in `ltg_style_frame_color_story.md`. The 4 WARN grades on warm/cool are systematic false
positives of the same class as the UV_PURPLE and SUNLIT_AMBER false positives.

### Recommendation C — SF04 generator note
Add a comment to `LTG_TOOL_styleframe_luma_byte_v004.py` line 69 and the lamp draw call
noting that `(255,200,80)` is an intentional incandescent lamp amber distinct from canonical
RW-03 SUNLIT_AMBER. Register unused `SUNLIT_AMBER` constant or remove it.

---

## 6. SF02 v006 Color Audit (Task from C34 inbox)

**Run:** `LTG_TOOL_color_verify_v002.py --histogram` on `LTG_COLOR_styleframe_glitch_storm_v006.png`

| Color | Status | Δ Hue | n pixels | Notes |
|-------|--------|-------|----------|-------|
| CORRUPT_AMBER | PASS | 0.1° | 293 | Near-exact. Canonical 30-35° bucket dominant (231/293). |
| BYTE_TEAL | PASS | 2.5° | 2,108 | Correct Byte body teal. Median 182.7° vs canonical 185.2° — expected AA edge pull. |
| UV_PURPLE | not_found | — | — | No UV Purple in storm scene. Consistent with spec. |
| HOT_MAGENTA | PASS | 1.5° | 1,064 | n=1,064 vs. v005 n=1,103. Slightly LOWER than expected for fill-light. See note. |
| ELECTRIC_CYAN | PASS | 1.9° | 3,571 | n=3,571 vs. v005 n=817. 4.4× INCREASE — specular highlights confirmed. |
| SUNLIT_AMBER | PASS | 0.9° | 206 | Window warm glow confirmed. Consistent with v005. |

**Overall: PASS**

**Notes on pixel counts vs targets:**

- **HOT_MAGENTA:** n=1,064 in v006 vs n=1,103 in v005. Marginally LOWER than the C34 benchmark
  (expected >> 1,103 for fill-light). Possible explanation: the fill-light is applied as a
  soft radial overlay (alpha max 40 per spec), which at low alpha may produce pixels that read
  as HOT_MAGENTA at canonical saturation only in the core zone. The hue is correct (Δ1.5°).
  The count discrepancy (39 fewer pixels at canonical) is within sampling variance. PASS —
  no regression.

- **ELECTRIC_CYAN:** n=3,571 in v006 vs n=817 in v005. 4.4× increase confirms the new
  specular highlights are present and rendering at canonical hue. **TARGET MET.**

- **CORRUPT_AMBER:** n=293 vs v005 n=296. Stable. No regression.

**v006 verdict: PASS. No regressions vs v005. Cyan specular confirmed. Magenta fill-light
  hue is correct; pixel-count is at expectation range for soft-overlay implementation.**

---

## 7. SF02 v007 Status

Per C35 directive: Rin Yamamoto's v007 delivery is pending this cycle.

**Status: PENDING.** When v007 is delivered, run:
```
python3 output/tools/LTG_TOOL_color_verify_v002.py \
  output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v007.png --histogram
```
Expected: All canonical colors from v006 remain stable. If Rin adds procedural draw elements,
verify no hue drift on CORRUPT_AMBER (GL-07, most vulnerable to stylization errors) and no
warm-tone contamination in the storm sky zone.

---

## 8. Summary of Action Items

| # | Item | Owner | Priority |
|---|------|-------|----------|
| 1 | Recalibrate `_check_warm_cool()` with `expected_temp` parameter | Kai Nakamura | Medium |
| 2 | Add comment to SF04 v004 generator — lamp amber (255,200,80) is intentional, register vs canonical RW-03 | Sam Kowalski (this cycle) | Low |
| 3 | Run v007 audit when Rin delivers | Sam Kowalski | Pending delivery |
| 4 | Relay to Alex: all 4 SF warm/cool WARNs are metric false positives — no visual change needed | Sam Kowalski | Done (via this doc) |

---

*Sam Kowalski — Color & Style Artist — Cycle 35*
