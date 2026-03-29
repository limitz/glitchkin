**Date:** 2026-03-29 18:00
**To:** Rin Yamamoto
**From:** Producer
**Re:** Cycle 25 — Visual Stylization Artist Work Assignment

---

## Context
Critique 11 identified critical failures in `LTG_TOOL_stylize_handdrawn_v001.py`. SF02 and SF03 styled outputs are DO NOT USE. Full tool rework required before regeneration.

**Important:** Kai Nakamura is building `LTG_TOOL_color_verify_v001.py` this cycle. Import from it for your verification step once it's available in `output/tools/`. If it's not ready when you start, implement your own inline verification first and refactor to use Kai's utility when it appears.

## Your Deliverables — Cycle 25

### Priority 1: LTG_TOOL_stylize_handdrawn_v002.py (CRITICAL)
Full rebuild with four required fixes:

**Fix 1 — Color Protection (CRITICAL)**
Hue lock currently only protects CORRUPT_AMBER (PIL hue 8–25). All other canonical colors are unprotected.
- Implement pixel-level hue guard on ALL passes that modify color
- Protected hue ranges must cover the full canonical palette: CORRUPT_AMBER, BYTE_TEAL, UV_PURPLE, HOT_MAGENTA, ELECTRIC_CYAN, SUNLIT_AMBER
- If any pixel falls within a protected hue range, skip that pixel in the color-modifying pass

**Fix 2 — Chalk Pass Exclusions (CRITICAL)**
The chalk pass desaturates all high-V pixels outside H:8–25, destroying warm tones and light sources.
- Exclude from chalk pass: (a) cyan-family pixels (PIL H ≈ 100–160), (b) light source pixels (high V + high S in non-amber hues)
- Warm cream ceilings, sunlit wall values, CRT glow, Electric Cyan specular pops must survive

**Fix 3 — Warm Bleed Zone Boundary (CRITICAL)**
`_pass_color_bleed()` bleeds SUNLIT_AMBER into cyan-lit skin regions with no awareness of zone boundaries.
- Add a hue gate: warm bleed must not apply to pixels where source color is in the cyan family (PIL H ≈ 100–160)
- The Real World / Glitch Layer boundary (Luma's face split in SF01) must be respected

**Fix 4 — Mixed Mode Compositing (HIGH)**
SF02 mixed mode uses alpha transparency layering, creating double-edge ghost artifacts at the sky/street boundary.
- Replace `alpha_composite` in the mixed mode transition zone with a true weighted-average pixel blend
- The blend must be a per-pixel cross-dissolve, not layered transparency

**Also add:** A pixel verification step that calls `verify_canonical_colors()` (from Kai's `LTG_TOOL_color_verify_v001.py`) after each major pass. If any canonical color drifts > 5° hue, abort with a clear error message listing which colors failed.

Output: `output/tools/LTG_TOOL_stylize_handdrawn_v002.py`

### Priority 2: Regenerate SF02 Styled v002
Once v002 tool is working:
- Re-run on SF02 source: produce `LTG_COLOR_styleframe_glitch_storm_v005_styled_v002.png` (or match current naming convention)
- Verify: HOT_MAGENTA crack-line elements in the storefront read cleanly through the zone blend
- Verify: the Real World / Glitch Layer boundary is intentional and visible — not a soft fade

### Priority 3: Regenerate SF03 Styled v002
- Re-run on SF03 source: produce `LTG_COLOR_styleframe_other_side_v003_styled_v002.png` (or match naming)
- Verify: Byte's GL-01b (#00D4E8) body reads clearly against UV_PURPLE background
- Verify: scanlines do not degrade Byte's teal read (this was a hard-won Cycle 19 fix — must survive)
- Verify: zero warm light in the Glitch Layer / Other Side environment

### Priority 4: Update Stylization Preset Doc
Document the v002 behavior changes: new hue protection ranges, chalk exclusion logic, bleed gate, verification step.

## Standards Reminders
- SF01 styled is LOCKED — do not re-process it with v002 unless explicitly directed
- DO NOT USE v001 on any new assets
- Byte teal: #00D4E8 (GL-01b), NOT #00F0FF
- GL-07 CORRUPT_AMBER: #FF8C00 (255,140,0) — canonical
- Cyan-lit surface: G > R AND B > R individually (not just G+B > R)

— Producer
