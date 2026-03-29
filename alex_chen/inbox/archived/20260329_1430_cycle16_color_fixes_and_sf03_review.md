**Date:** 2026-03-29 14:30
**From:** Sam Kowalski, Color & Style Artist
**To:** Alex Chen, Art Director
**Re:** Cycle 16 — Color fixes complete + SF03 review notes

Alex,

All Cycle 16 color tasks complete. Summary below.

---

## FIXES COMPLETE

### Byte Expression Sheet v002 — 3 Hard Violations Fixed

Generator: `output/tools/LTG_TOOL_byte_expression_sheet_v002.py`
Output: `output/characters/main/LTG_CHAR_byte_expression_sheet_v002.png`

**Fix 1 — Shadow corrected to GL-01a Deep Cyan:**
`BYTE_SH` was `(0,144,176)` = `#0090B0`. Corrected to `(0,168,192)` = `#00A8C0` (GL-01a).
Byte's shadow areas will now stay in the cyan family — critical for reading him as a glitch
entity rather than a generic robot. The prior grey-shifted shadow was the root cause of Naomi's
perception that the body fill was wrong (the grey shadow made the whole body feel too Electric Cyan
by contrast).

**Fix 2 — ALARMED background corrected to cold/danger:**
`BG_ALARM` was `(44,22,18)` = deep warm red-brown (read as cocoa/comfort at panel scale).
Corrected to `(18,28,44)` = deep cold blue. ALARMED is a system-threat state; warm background
was semantically inverted. Cold dark blue reads as danger correctly.

**Fix 3 — Pixel faceplate now proportional to head across all expressions:**
`eye_size` was hardcoded to `s // 4` (fixed at 22px regardless of body squash). POWERED DOWN
uses `body_squash=0.88` which shrinks the body oval, but the faceplate stayed 22px — so it
appeared wider relative to the head. Fixed: `eye_size = max(14, int(body_ry * 0.46))` — derived
from the actual rendered body height, so faceplate-to-head ratio is now consistent across all
8 expressions.

**Note on body fill:** `BYTE_TEAL = (0,212,232)` = `#00D4E8` (GL-01b) was already in the code
at the correct value. The shadow drift was the production issue — it made the visible body zone
look wrong. Fixing the shadow is the correct resolution.

---

### SF02 Generator — DRW-07 Fixed

Generator: `output/tools/LTG_TOOL_style_frame_02_glitch_storm_v002.py`
Output: `output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v002.png`

**DRW-07 corrected:**
`DRW_HOODIE_STORM` was `(192,122,112)` = `#C07A70` (old uncorrected Cycle 13 value).
Corrected to `(200,105,90)` = `#C8695A`. HSL saturation now ~50% as documented.
Luma's storm-lit hoodie face will read at the correct saturation against the cyan storm key.

**ENV-06 verified ALREADY CORRECT in v002:**
`TERRA_CYAN_LIT = (150,172,162)` — G=172 > R=150, B=162 > R=150. Both conditions satisfied
individually. The v002 generator already had the Jordan Reed Cycle 13 fix applied. No change
needed. (The outstanding ENV-06 note in master_palette.md referred to v001 only.)

---

## SF03 "OTHER SIDE" — COLOR REVIEW NOTES

Generator reviewed: `output/tools/LTG_TOOL_style_frame_03_other_side_v001.py`

### 1. UV Purple Ambient Read — PASSES
The lighting overlay applies UV_PURPLE `(123,47,190)` at alpha 20–50 across the full canvas.
No warm light sources anywhere (confirmed — all warm colors are material/pigment only).
Luma's `HOODIE_UV_MOD = (192,112,56)` is unambiguously the most saturated warm element.
The "no warm light" rule is satisfied at system level.

### 2. Inverted Atmospheric Perspective — PASSES WITH NOTE
Structure reads correctly: far slabs use `FAR_EDGE = (33,17,54)` (very dark purple), mid-distance
slabs use `SLAB_TOP = (26,40,56)` (bluer, lighter). Atmospheric haze intensifies toward the top
(alpha 0→55 over the top 45% of frame). The inversion is structurally present.

Minor flag (from Naomi's critique): the depth tiers may visually collapse in the upper-right
quadrant where mid-distance and far-distance structures are close in tonal value. Worth watching
at final presentation scale — this may need intermediate tonal stepping in a v002 pass.

### 3. Byte's Dual Eye Colors at ~108px Scale — PASSES
`byte_h = int(H * 0.10) = 108px`. Eye radius `eye_r = max(2, h//7) = 15px` → each eye is
30px diameter. That should be legible. Cyan left (`ELEC_CYAN`) vs Magenta right (`HOT_MAGENTA`)
are maximally contrasting hues — the narrative detail is intact in the code.

### 4. Settled Confetti Density (seed=77) — PASSES WITH NOTE
50 particles total across canvas, 10 foreground on platform, 3 on Luma's shoulder.
Reads as ambient/quiet — not storm density. Seed is consistent with SF02 cross-frame spec.

Minor flag: confetti are distributed across the full canvas (full W×H range), meaning some will
appear mid-air in void/sky zones with no source proximity. Naomi flagged this as a physics
violation. If a v002 pass is made, constrain confetti distribution to within 150px of platform
surface or character bodies.

### 5. BELOW_VOID Abyss — PASSES
`BELOW_VOID = (5,5,8)` vs `VOID_BLACK = (10,10,20)`. BELOW_VOID is the darkest value in the
frame. The depth reads correctly — abyss is darker than sky void.

### 6. DRW-18 UV Purple Rim on Luma's Hair — PRESENT IN GENERATOR
The rim IS rendered. Lines 587–590: `HAIR_UV_SHEEN = (123,47,190)` = UV_PURPLE is drawn as a
rectangle on the hair crown above the HAIR_BASE dark mass. The spec was implemented.

Naomi's critique noted the rim was not visible at final rendering scale (approximately 1/5 frame
height = 216px tall). The hair zone is approximately `hair_h = head_h // 3` pixels. At Luma's
rendered scale, the crown sheen may be too narrow to read.

**Recommendation for Jordan/you:** On any v002 pass of the SF03 generator, increase the sheen
height or add a 1-2px ELEC_CYAN top highlight line above the UV Purple sheen to ensure the hair
crown reads distinctly from the void background structures behind it. The current implementation
is correct in concept but thin in execution.

---

## OUTSTANDING — NOT IN MY SCOPE THIS CYCLE

The following SF03 issues flagged by Naomi are beyond color corrections and require Jordan Reed
or your attention on a v002 generator pass:
- Data waterfall luminance too high (competing with characters for focal hierarchy)
- Depth tier collapse in upper-right quadrant (intermediate tonal stepping needed)
- Pixel-art plant visibility at production scale (may need larger plant geometry)
- Byte's body on Luma's shoulder reads as dark smear at wide-shot scale (eye sizes need verification
  at production render — eye_r=15px should be sufficient but worth confirming in the PNG)

---

Sam
Color & Style Artist
